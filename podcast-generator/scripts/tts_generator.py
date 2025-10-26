#!/usr/bin/env python3
"""
Google AI Studio Text-to-Speech interface.
Handles TTS generation using Google's Gemini API.
"""

import os
import time
import json
import wave
import subprocess
from pathlib import Path
from typing import Dict, Optional
import google.generativeai as genai
from google.api_core import retry


class TTSGenerator:
    """Interface to Google AI Studio for text-to-speech generation."""
    
    def __init__(self, api_key: Optional[str] = None, config: Dict = None):
        self.api_key = api_key or os.getenv("GOOGLE_AI_API_KEY")
        self.config = config  # Store config for passing to GoogleCloudTTSGenerator

        if not self.api_key:
            raise ValueError("Google AI API key not found. Set GOOGLE_AI_API_KEY environment variable.")

        # Configure the API
        genai.configure(api_key=self.api_key)

        # Map speaker names to Gemini TTS voices
        # Available voices: Puck, Charon, Kore, Fenrir, Aoede
        # Using top-rated voices
        self.voice_mapping = {
            "jordan": "Kore",      # 9/10 rating
            "alex": "Algieba",     # Algieba voice
            "default": "Kore"
        }

        # Rate limiting settings
        self.rate_limit_delay = config.get("processing", {}).get("rate_limit_delay", 0.5) if config else 0.5

        # Initialize TTS model
        self.model_name = 'gemini-2.0-flash-exp'  # Model with TTS support
    
    def generate_audio(self, text: str, speaker: str, output_path: Path) -> Dict:
        """
        Generate audio for given text using Google AI Studio's Gemini TTS.
        
        Args:
            text: The text to convert to speech
            speaker: The speaker identifier
            output_path: Where to save the audio file
            
        Returns:
            Dict with generation metadata (duration, etc.)
        """
        start_time = time.time()
        
        # Get voice for speaker
        voice_name = self.voice_mapping.get(speaker, self.voice_mapping["default"])
        
        print(f"Generating audio for {speaker} (voice: {voice_name}): {text[:50]}...")
        
        # Apply rate limiting
        time.sleep(self.rate_limit_delay)
        
        try:
            # Create the prompt for TTS with style instructions
            prompt = self._create_tts_prompt(text, speaker)
            
            # Try to use Google Cloud TTS if available
            try:
                from cloud_tts_generator import GoogleCloudTTSGenerator

                # Use application default credentials (no API key needed)
                # Pass config so it can load voice mappings
                cloud_tts = GoogleCloudTTSGenerator(config=self.config)
                result = cloud_tts.generate_audio(text, speaker, output_path)
                duration = result["duration"]
                print(f"  ✓ Generated with Google Cloud TTS")
            except ImportError:
                print("\n⚠️  Google Cloud TTS not installed. Install with:")
                print("    pip install google-cloud-texttospeech")
                print("\n  Using placeholder audio for now...")
                self._create_placeholder_audio(output_path, text)
                duration = len(text.split()) / 150 * 60
            except Exception as e:
                if "credentials" in str(e).lower():
                    print("\n⚠️  Google Cloud credentials not configured.")
                    print("  To use real TTS, set up credentials:")
                    print("  1. Install: pip install google-cloud-texttospeech")
                    print("  2. Set up credentials:")
                    print("     - Option A: export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json")
                    print("     - Option B: gcloud auth application-default login")
                    print("\n  Using placeholder audio for now...")
                else:
                    print(f"\n⚠️  TTS error: {e}")
                    print("  Using placeholder audio...")
                self._create_placeholder_audio(output_path, text)
                duration = len(text.split()) / 150 * 60
            
        except Exception as e:
            print(f"TTS generation failed: {e}")
            # Fallback to creating a placeholder file
            print("Creating placeholder audio file...")
            self._create_placeholder_audio(output_path, text)
            duration = len(text.split()) / 150 * 60  # Estimated duration
        
        generation_time = time.time() - start_time
        
        return {
            "duration": duration,
            "generation_time": generation_time,
            "file_size": output_path.stat().st_size if output_path.exists() else 0,
            "voice": voice_name
        }
    
    def _create_tts_prompt(self, text: str, speaker: str) -> str:
        """Create a prompt for TTS with appropriate style instructions."""
        # Add conversational style instructions based on speaker
        if speaker == "jordan":
            style = "Speak in a warm, friendly, and engaging manner as a knowledgeable tech podcast host."
        elif speaker == "alex":
            style = "Speak in a clear, thoughtful, and insightful manner as an experienced engineer sharing expertise."
        else:
            style = "Speak naturally and conversationally."
        
        return f"{style} Say: {text}"
    
    def _save_as_mp3(self, audio_data: bytes, output_path: Path):
        """Save audio data as MP3 file."""
        # For now, save as WAV then convert
        # In production, you might use pydub or ffmpeg for conversion
        temp_wav = output_path.with_suffix('.wav')
        
        # Save WAV data
        with wave.open(str(temp_wav), 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(24000)  # 24kHz sample rate
            wf.writeframes(audio_data)
        
        # Convert to MP3 using ffmpeg
        try:
            import subprocess
            subprocess.run([
                'ffmpeg', '-y', '-i', str(temp_wav),
                '-codec:a', 'libmp3lame', '-b:a', '128k',
                str(output_path)
            ], check=True, capture_output=True)
            temp_wav.unlink()  # Remove temporary WAV file
        except Exception as e:
            print(f"MP3 conversion failed: {e}, keeping WAV format")
            temp_wav.rename(output_path.with_suffix('.wav'))
    
    def _estimate_audio_duration(self, audio_data: bytes) -> float:
        """Estimate duration from audio data."""
        # Assuming 24kHz sample rate, 16-bit mono
        sample_rate = 24000
        bytes_per_sample = 2
        num_samples = len(audio_data) / bytes_per_sample
        duration = num_samples / sample_rate
        return duration
    
    def _create_placeholder_audio(self, output_path: Path, text: str):
        """Create a placeholder audio file for testing."""
        import subprocess
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Estimate duration based on text length (roughly 150 words per minute)
        word_count = len(text.split())
        duration = (word_count / 150) * 60  # Convert to seconds
        duration = max(0.1, duration)  # Minimum 0.1 seconds
        
        # Use ffmpeg to generate silent audio
        try:
            subprocess.run([
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', f'anullsrc=r=44100:cl=stereo:d={duration}',
                '-codec:a', 'libmp3lame',
                '-b:a', '128k',
                str(output_path)
            ], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to create placeholder audio: {e}")
            print(f"Error output: {e.stderr}")
            # Fallback to minimal MP3
            with open(output_path, 'wb') as f:
                f.write(b'ID3\x04\x00\x00\x00\x00\x00\x00')
                f.write(b'\xFF\xFB\x90\x00' * 100)
    
    def generate_with_retry(self, text: str, speaker: str, output_path: Path, max_retries: int = 3) -> Dict:
        """Generate audio with retry logic for handling failures."""
        for attempt in range(max_retries):
            try:
                return self.generate_audio(text, speaker, output_path)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception(f"Failed to generate audio after {max_retries} attempts")


class GoogleCloudTTSGenerator(TTSGenerator):
    """
    Production implementation using Google Cloud Text-to-Speech API.
    This would be used instead of the placeholder TTSGenerator above.
    """
    
    def __init__(self, api_key: Optional[str] = None, config: Dict = None):
        super().__init__(api_key, config)
        # Import would happen here for Google Cloud TTS
        # from google.cloud import texttospeech
        # self.client = texttospeech.TextToSpeechClient()
    
    def generate_audio(self, text: str, speaker: str, output_path: Path) -> Dict:
        """
        Generate audio using Google Cloud Text-to-Speech API.
        
        This is the production implementation that would replace
        the placeholder method above.
        """
        # Production implementation would go here
        # synthesis_input = texttospeech.SynthesisInput(text=text)
        # voice = texttospeech.VoiceSelectionParams(...)
        # audio_config = texttospeech.AudioConfig(...)
        # response = self.client.synthesize_speech(...)
        # etc.
        
        # For now, fall back to placeholder
        return super().generate_audio(text, speaker, output_path)


def main():
    """Test the TTS generator."""
    # Note: This requires a valid Google AI API key
    try:
        generator = TTSGenerator()
        
        test_text = "Hello, this is a test of the text-to-speech system."
        output_path = Path("test_output.mp3")
        
        result = generator.generate_audio(test_text, "jordan", output_path)
        print(f"Generated audio: {result}")
        
        if output_path.exists():
            print(f"Audio file created: {output_path}")
            output_path.unlink()  # Clean up test file
            
    except Exception as e:
        print(f"Test failed: {e}")
        print("Make sure to set GOOGLE_AI_API_KEY environment variable")


if __name__ == "__main__":
    main()