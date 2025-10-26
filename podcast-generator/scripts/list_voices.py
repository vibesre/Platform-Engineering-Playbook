#!/usr/bin/env python3
"""
List available voices from Google Cloud Text-to-Speech API.
Useful for finding and verifying voice names.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent))

try:
    from google.cloud import texttospeech
except ImportError:
    print("Error: google-cloud-texttospeech not installed")
    print("Install with: pip install google-cloud-texttospeech")
    sys.exit(1)


def list_voices(language_code: str = "en-US", filter_chirp: bool = False):
    """List available voices."""
    try:
        client = texttospeech.TextToSpeechClient()

        # List voices
        voices = client.list_voices(language_code=language_code)

        # Filter for Chirp3-HD if requested
        if filter_chirp:
            filtered_voices = [v for v in voices.voices if "Chirp3-HD" in v.name]
            print(f"\nChirp3-HD voices for {language_code}:")
        else:
            filtered_voices = voices.voices
            print(f"\nAll voices for {language_code}:")

        # Group by voice family
        voice_families = {}
        for voice in filtered_voices:
            family = voice.name.split('-')[-1] if '-' in voice.name else voice.name
            if family not in voice_families:
                voice_families[family] = []
            voice_families[family].append(voice)

        # Display voices
        for family, voices_list in sorted(voice_families.items()):
            print(f"\n{family}:")
            for voice in voices_list:
                gender = voice.ssml_gender.name
                sample_rate = voice.natural_sample_rate_hertz
                print(f"  - {voice.name:40s} ({gender}, {sample_rate} Hz)")

    except Exception as e:
        print(f"Error listing voices: {e}")
        print("\nMake sure Google Cloud credentials are configured:")
        print("1. export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json")
        print("2. OR: gcloud auth application-default login")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="List Google Cloud TTS voices")
    parser.add_argument(
        "--language",
        type=str,
        default="en-US",
        help="Language code (default: en-US)"
    )
    parser.add_argument(
        "--chirp",
        action="store_true",
        help="Show only Chirp3-HD voices"
    )

    args = parser.parse_args()
    list_voices(args.language, args.chirp)
