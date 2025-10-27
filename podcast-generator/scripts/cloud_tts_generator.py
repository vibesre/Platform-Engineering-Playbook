#!/usr/bin/env python3
"""
Google Cloud Text-to-Speech interface.
Production-ready TTS generation using Google Cloud TTS API.
"""

import os
import time
import re
from pathlib import Path
from typing import Dict, Optional, List
from google.cloud import texttospeech
from google.api_core import retry as api_retry


# GCP Cloud Text-to-Speech pricing (as of 2025, per character)
# https://cloud.google.com/text-to-speech/pricing
TTS_PRICING = {
    "Chirp3-HD": 0.000015,  # $0.000015 per character
    "Neural2": 0.000016,    # $0.000016 per character
    "WaveNet": 0.000016,    # $0.000016 per character
    "Journey": 0.000016,    # $0.000016 per character (Studio voices)
    "Standard": 0.000004,   # $0.000004 per character
}

# Error classification for smart retry logic
RECOVERABLE_ERROR_PATTERNS = [
    "429",  # Rate limit exceeded
    "503",  # Service unavailable
    "500",  # Internal server error
    "timeout",
    "connection",
    "transient",
    "deadline exceeded",
    "temporarily unavailable"
]

UNRECOVERABLE_ERROR_PATTERNS = [
    "config is required",
    "credentials",
    "authentication",
    "permission denied",
    "invalid voice",
    "quota exceeded",  # Quota exhausted (different from rate limit)
    "invalid argument",
    "not found"
]


def is_recoverable_error(error: Exception) -> bool:
    """
    Check if an error is worth retrying.

    Args:
        error: Exception from TTS API call

    Returns:
        True if error is transient/recoverable, False if fatal
    """
    error_str = str(error).lower()

    # Check for unrecoverable patterns first (more specific)
    for pattern in UNRECOVERABLE_ERROR_PATTERNS:
        if pattern.lower() in error_str:
            return False

    # Check for recoverable patterns
    for pattern in RECOVERABLE_ERROR_PATTERNS:
        if pattern.lower() in error_str:
            return True

    # Unknown errors - treat as recoverable (give it a chance)
    return True


def get_voice_pricing(voice_name: str) -> float:
    """
    Get per-character pricing for a voice.

    Args:
        voice_name: Full voice name (e.g. "en-US-Chirp3-HD-Kore")

    Returns:
        Price per character in USD
    """
    # Extract voice type from name
    if "Chirp3-HD" in voice_name or "Chirp3HD" in voice_name:
        return TTS_PRICING["Chirp3-HD"]
    elif "Neural2" in voice_name:
        return TTS_PRICING["Neural2"]
    elif "WaveNet" in voice_name:
        return TTS_PRICING["WaveNet"]
    elif "Journey" in voice_name:
        return TTS_PRICING["Journey"]
    else:
        # Default to Standard pricing
        return TTS_PRICING["Standard"]


class GoogleCloudTTSGenerator:
    """Production TTS generator using Google Cloud Text-to-Speech API."""

    def __init__(self, config: Dict = None, api_key: Optional[str] = None):
        # Store config for voice configuration
        if config is None:
            raise ValueError("Config is required for GoogleCloudTTSGenerator")
        self.config = config

        # Initialize the client
        # Option 1: Use API Key (simplest)
        if api_key or os.getenv("GOOGLE_CLOUD_API_KEY"):
            from google.auth.api_key import Credentials
            from google.cloud import texttospeech_v1

            key = api_key or os.getenv("GOOGLE_CLOUD_API_KEY")
            credentials = Credentials(key)
            self.client = texttospeech_v1.TextToSpeechClient(credentials=credentials)
        else:
            # Option 2: Use default credentials (service account or gcloud auth)
            self.client = texttospeech.TextToSpeechClient()

        # Load voice mapping from config (NO HARDCODING)
        # This ensures voices are explicitly configured and validated
        self.voice_mapping = self._load_voice_mapping_from_config()

        # Load alternative voices from config (optional)
        self.alternative_voices = self._load_alternative_voices_from_config()

        # Load per-speaker audio configuration from config
        self.speaker_audio_config = self._load_audio_config_from_config()

        # Validate voice configuration on startup
        self._validate_voice_configuration()

        # Rate limiting
        self.rate_limit_delay = config.get("processing", {}).get("rate_limit_delay", 0.1) if config else 0.1

    def _load_voice_mapping_from_config(self) -> Dict[str, str]:
        """
        Load voice mapping from config file.

        Returns:
            Dict mapping normalized speaker names to Google Cloud voice names
        """
        if "speakers" not in self.config:
            raise ValueError("Config must contain 'speakers' section")

        voice_mapping = {}
        for speaker_name, speaker_config in self.config["speakers"].items():
            if "voice" not in speaker_config:
                raise ValueError(f"Speaker '{speaker_name}' must have 'voice' configured")

            # Normalize speaker name (lowercase)
            normalized_name = self._normalize_speaker_name(speaker_name)
            voice_mapping[normalized_name] = speaker_config["voice"]

        if not voice_mapping:
            raise ValueError("No speakers configured in config file")

        print(f"✓ Loaded voice mapping from config: {voice_mapping}")
        return voice_mapping

    def _load_alternative_voices_from_config(self) -> Dict[str, List[str]]:
        """Load alternative voices from config (optional fallback chain)."""
        alternative_voices = {}

        for speaker_name, speaker_config in self.config.get("speakers", {}).items():
            normalized_name = self._normalize_speaker_name(speaker_name)
            alternatives = speaker_config.get("alternatives", [])
            if alternatives:
                alternative_voices[normalized_name] = alternatives

        return alternative_voices

    def _load_audio_config_from_config(self) -> Dict[str, Dict]:
        """Load per-speaker audio configuration from config."""
        audio_config = {}

        for speaker_name, speaker_config in self.config.get("speakers", {}).items():
            normalized_name = self._normalize_speaker_name(speaker_name)
            audio_config[normalized_name] = {
                "speaking_rate": speaker_config.get("speed", 1.0),
                "pitch": speaker_config.get("pitch", 0.0),
                "volume_gain_db": speaker_config.get("volume_gain_db", 0.0)
            }

        return audio_config

    def _normalize_speaker_name(self, speaker: str) -> str:
        """
        Normalize speaker name for consistent lookups.

        Args:
            speaker: Raw speaker name (e.g., "Jordan", "JORDAN", "jordan")

        Returns:
            Normalized speaker name (lowercase, stripped)
        """
        normalized = speaker.lower().strip()

        # Map "Speaker 1" and "Speaker 2" to "jordan" and "alex"
        if normalized == "speaker 1":
            normalized = "jordan"
        elif normalized == "speaker 2":
            normalized = "alex"

        return normalized

    def _validate_voice_configuration(self):
        """
        Validate that all configured voices exist in Google Cloud TTS.
        Fails fast if any voice is invalid.
        """
        print("\n🔍 Validating voice configuration...")

        # Get list of available voices
        try:
            voices_response = self.client.list_voices(language_code="en-US")
            available_voices = {voice.name for voice in voices_response.voices}
        except Exception as e:
            print(f"⚠️  Warning: Could not validate voices (API error): {e}")
            print("   Continuing without validation...")
            return

        # Check each configured voice
        all_valid = True
        for speaker, voice_name in self.voice_mapping.items():
            if voice_name in available_voices:
                print(f"  ✓ {speaker}: {voice_name}")
            else:
                print(f"  ✗ {speaker}: {voice_name} (NOT FOUND)")
                all_valid = False

        if not all_valid:
            raise ValueError(
                "Invalid voice configuration detected. "
                "Check that all voices exist in Google Cloud TTS. "
                "Run: python3 scripts/list_voices.py"
            )

        print("✓ All voices validated successfully")

    def _extract_custom_pronunciations(self, text: str) -> tuple:
        """
        Extract pronunciation tags for Chirp3-HD custom_pronunciations API.

        For Chirp3-HD voices, we need to:
        1. Extract <phoneme> and <say-as> tags
        2. Convert them to custom_pronunciations format using proper API objects
        3. Return clean markup text with just [pause] tags

        Args:
            text: Text with SSML pronunciation tags and [pause] tags

        Returns:
            Tuple of (clean_markup_text, CustomPronunciations object or None)
        """
        import re

        # Use dict to deduplicate pronunciations by phrase
        # API requires each phrase to appear only once
        pronunciation_dict = {}
        clean_text = text

        # Extract <phoneme alphabet="ipa" ph="...">Word</phoneme>
        phoneme_pattern = r'<phoneme\s+alphabet="ipa"\s+ph="([^"]+)">([^<]+)</phoneme>'
        for match in re.finditer(phoneme_pattern, text):
            pronunciation = match.group(1)
            phrase = match.group(2)

            # Deduplicate case-insensitively (API treats "kubectl" and "Kubectl" as same)
            phrase_lower = phrase.lower()
            if phrase_lower not in pronunciation_dict:
                pronunciation_dict[phrase_lower] = pronunciation

            # Replace with just the word (preserve original case in text)
            clean_text = clean_text.replace(match.group(0), phrase)

        # Convert deduplicated dict to CustomPronunciationParams list
        # Use lowercase phrases since API is case-insensitive
        custom_params = [
            texttospeech.CustomPronunciationParams(
                phrase=phrase,  # phrase is already lowercase from dict keys
                phonetic_encoding=texttospeech.CustomPronunciationParams.PhoneticEncoding.PHONETIC_ENCODING_IPA,
                pronunciation=pron
            )
            for phrase, pron in pronunciation_dict.items()
        ]

        # Extract <say-as interpret-as="characters">WORD</say-as>
        # For Chirp3-HD, strip these tags and rely on natural acronym handling
        # The API doesn't support spelling out acronyms via custom_pronunciations
        sayas_pattern = r'<say-as\s+interpret-as="characters">([^<]+)</say-as>'
        for match in re.finditer(sayas_pattern, clean_text):
            word = match.group(1)
            # Just replace tag with the word - Chirp3-HD handles acronyms naturally
            clean_text = clean_text.replace(match.group(0), word)

        # CRITICAL: Strip ANY remaining SSML tags to avoid "SSML not supported" error
        # Only [pause] tags should remain for Chirp3-HD markup field
        clean_text = re.sub(r'<[^>]+>', '', clean_text)

        # Create CustomPronunciations object if we have any params
        if custom_params:
            custom_prons = texttospeech.CustomPronunciations(
                pronunciations=custom_params
            )
            return clean_text, custom_prons

        return clean_text, None

    def generate_audio(self, text: str, speaker: str, output_path: Path) -> Dict:
        """
        Generate audio using Google Cloud Text-to-Speech API.

        Args:
            text: The text to convert to speech
            speaker: The speaker identifier
            output_path: Where to save the audio file

        Returns:
            Dict with generation metadata
        """
        start_time = time.time()

        # Normalize speaker name for consistent lookup
        speaker_normalized = self._normalize_speaker_name(speaker)

        # CRITICAL: NO SILENT FALLBACKS - fail loudly if speaker unknown
        if speaker_normalized not in self.voice_mapping:
            raise ValueError(
                f"Unknown speaker: '{speaker}' (normalized: '{speaker_normalized}'). "
                f"Valid speakers: {list(self.voice_mapping.keys())}. "
                f"Check config.yaml speakers section."
            )

        voice_name = self.voice_mapping[speaker_normalized]

        print(f"Generating audio for {speaker_normalized} (voice: {voice_name}): {text[:50]}...")
        
        # Apply rate limiting
        time.sleep(self.rate_limit_delay)
        
        try:
            # Extract custom pronunciations for Chirp3-HD
            markup_text, custom_prons = self._extract_custom_pronunciations(text)

            # Build synthesis input with markup and custom pronunciations
            if custom_prons:
                # Chirp3-HD with custom pronunciations
                synthesis_input = texttospeech.SynthesisInput(
                    markup=markup_text,
                    custom_pronunciations=custom_prons
                )
            else:
                # No custom pronunciations, just markup (for [pause] tags)
                synthesis_input = texttospeech.SynthesisInput(markup=markup_text)
            
            # Build the voice request
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name=voice_name
            )

            # Get speaker-specific audio configuration (use normalized name)
            speaker_config = self.speaker_audio_config.get(speaker_normalized, {
                "speaking_rate": 1.0,
                "pitch": 0.0,
                "volume_gain_db": 0.0
            })

            # Select the type of audio file with speaker-specific settings
            # Optimized for podcast listening (primarily on headphones)
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=speaker_config["speaking_rate"],
                pitch=speaker_config["pitch"],
                volume_gain_db=speaker_config["volume_gain_db"],
                sample_rate_hertz=24000,  # Chirp3-HD natural sample rate for quality
                effects_profile_id=["headphone-class-device"]  # Optimized for podcast listening
            )
            
            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the response to the output file
            with open(output_path, "wb") as out:
                out.write(response.audio_content)
            
            # Estimate duration (Google Cloud TTS doesn't return duration)
            # Rough estimate: ~150 words per minute
            word_count = len(text.split())
            duration = (word_count / 150) * 60  # seconds
            
            print(f"  ✓ Generated successfully")
            
        except Exception as e:
            print(f"❌ Error generating audio: {e}")

            # Try alternative voice if available
            if speaker_normalized in self.alternative_voices:
                print(f"⚠️  PRIMARY VOICE FAILED - Attempting alternative voices...")
                print(f"   This may cause voice inconsistency in the episode!")

                for alt_voice in self.alternative_voices[speaker_normalized]:
                    try:
                        print(f"  Trying alternative voice: {alt_voice}")
                        voice.name = alt_voice
                        response = self.client.synthesize_speech(
                            input=synthesis_input,
                            voice=voice,
                            audio_config=audio_config
                        )
                        with open(output_path, "wb") as out:
                            out.write(response.audio_content)

                        print(f"  ✓ SUCCESS with alternative voice: {alt_voice}")
                        print(f"  ⚠️  WARNING: Voice changed from {voice_name} to {alt_voice}")
                        print(f"      This chunk will sound different from other {speaker_normalized} chunks!")

                        voice_name = alt_voice
                        break
                    except Exception as alt_error:
                        print(f"  ✗ Alternative voice {alt_voice} also failed: {alt_error}")
                        continue
                else:
                    # All alternatives failed
                    raise ValueError(
                        f"All voices failed for speaker '{speaker_normalized}'. "
                        f"Primary: {voice_name}, Alternatives: {self.alternative_voices[speaker_normalized]}"
                    ) from e
            else:
                raise e
            
            word_count = len(text.split())
            duration = (word_count / 150) * 60
        
        generation_time = time.time() - start_time

        # Calculate usage metrics for billing
        character_count = len(text)
        pricing_per_char = get_voice_pricing(voice_name)
        estimated_cost = character_count * pricing_per_char

        # Log usage information
        print(f"  💵 Usage: {character_count} chars → ${estimated_cost:.5f}")

        return {
            "duration": duration,
            "generation_time": generation_time,
            "file_size": output_path.stat().st_size if output_path.exists() else 0,
            "voice": voice_name,
            "word_count": word_count,
            "character_count": character_count,
            "estimated_cost_usd": estimated_cost,
            "tts_status": "success"
        }
    
    def generate_with_retry(self, text: str, speaker: str, output_path: Path, max_retries: int = 3) -> Dict:
        """
        Generate audio with smart retry logic.

        Retries recoverable errors (rate limits, timeouts, transient failures).
        Fails fast on unrecoverable errors (auth, config, quota exhausted).

        Args:
            text: Text to synthesize
            speaker: Speaker identifier
            output_path: Where to save audio
            max_retries: Maximum retry attempts (default: 3)

        Returns:
            Dict with generation metadata

        Raises:
            RuntimeError: If generation fails after retries or on unrecoverable error
        """
        retry_delay = 2.0  # Initial retry delay in seconds
        last_error = None

        for attempt in range(1, max_retries + 1):
            try:
                result = self.generate_audio(text, speaker, output_path)

                # Add attempt number to result
                if attempt > 1:
                    result["retry_attempt"] = attempt

                return result

            except Exception as e:
                last_error = e
                is_recoverable = is_recoverable_error(e)

                # Unrecoverable error - fail immediately
                if not is_recoverable:
                    print(f"\n❌ UNRECOVERABLE ERROR: {e}")
                    print(f"   Cannot proceed with generation - fix the issue and retry")
                    raise RuntimeError(f"TTS generation failed (unrecoverable): {e}") from e

                # Recoverable error - retry
                if attempt < max_retries:
                    print(f"\n⚠️  Attempt {attempt}/{max_retries} failed (recoverable): {e}")
                    print(f"   Retrying in {retry_delay:.1f}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    # Exhausted all retries
                    print(f"\n❌ All {max_retries} attempts failed: {e}")
                    raise RuntimeError(f"TTS generation failed after {max_retries} retries: {e}") from e
    
    def list_available_voices(self, language_code: str = "en-US"):
        """List all available voices for a language."""
        try:
            # List voices
            voices = self.client.list_voices(language_code=language_code)
            
            print(f"\nAvailable voices for {language_code}:")
            for voice in voices.voices:
                # Display the voice information
                print(f"  - {voice.name}")
                print(f"    SSML Gender: {voice.ssml_gender.name}")
                print(f"    Natural Sample Rate: {voice.natural_sample_rate_hertz} Hz")
                
        except Exception as e:
            print(f"Error listing voices: {e}")
            return []


def main():
    """Test the Google Cloud TTS generator."""
    # This requires Google Cloud credentials to be set up
    try:
        generator = GoogleCloudTTSGenerator()
        
        # List available voices
        generator.list_available_voices()
        
        # Test TTS
        test_text = "Hello, this is a test of Google Cloud Text-to-Speech."
        output_path = Path("test_cloud_tts.mp3")
        
        result = generator.generate_audio(test_text, "jordan", output_path)
        print(f"\nGenerated audio: {result}")
        
        if output_path.exists():
            print(f"Audio file created: {output_path}")
            output_path.unlink()  # Clean up
            
    except Exception as e:
        print(f"Test failed: {e}")
        print("\nMake sure to set up Google Cloud credentials:")
        print("1. Create a service account and download the JSON key")
        print("2. Set GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json")
        print("3. Or use: gcloud auth application-default login")


if __name__ == "__main__":
    main()