#!/usr/bin/env python3
"""
Generate two-speaker podcast audio using Gemini's Multi-Speaker TTS API.
Supports natural dialogue between Jordan and Alex with distinct voices.

Based on: https://ai.google.dev/gemini-api/docs/speech-generation
Uses the google-genai SDK (not google-generativeai)
"""

import os
import sys
import re
import time
import subprocess
import tempfile
import wave
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM audio data as a WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def parse_podcast_script(script_text: str) -> list:
    """
    Parse podcast script with Jordan:/Alex: speaker labels into turns.

    Returns:
        List of dicts: [{"speaker": "Jordan", "text": "..."}, ...]
    """
    # Remove SSML tags
    script_text = re.sub(r'<phoneme[^>]*>([^<]+)</phoneme>', r'\1', script_text)
    script_text = re.sub(r'<say-as[^>]*>([^<]+)</say-as>', r'\1', script_text)
    script_text = re.sub(r'\[pause[^\]]*\]', '', script_text)

    turns = []
    current_speaker = None
    current_text = []

    for line in script_text.split('\n'):
        line = line.strip()
        if not line:
            continue

        # Check for speaker label
        match = re.match(r'^(Jordan|Alex):\s*(.*)$', line)
        if match:
            # Save previous turn if exists
            if current_speaker and current_text:
                turns.append({
                    "speaker": current_speaker,
                    "text": ' '.join(current_text).strip()
                })
                current_text = []

            current_speaker = match.group(1)
            text = match.group(2).strip()
            if text:
                current_text.append(text)
        else:
            # Continuation of current speaker's turn
            if current_speaker:
                current_text.append(line)

    # Add final turn
    if current_speaker and current_text:
        turns.append({
            "speaker": current_speaker,
            "text": ' '.join(current_text).strip()
        })

    return turns


def generate_podcast_audio_gemini(script_path: Path, output_path: Path):
    """
    Generate two-speaker podcast audio using Gemini Multi-Speaker TTS.

    Args:
        script_path: Path to podcast script (Jordan:/Alex: format)
        output_path: Where to save the generated MP3
    """
    # Configure Gemini client
    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_AI_API_KEY not set in environment")

    client = genai.Client(api_key=api_key)

    # Read and parse the podcast script
    print(f"📖 Reading podcast script: {script_path}")
    with open(script_path, 'r') as f:
        script_text = f.read()

    turns = parse_podcast_script(script_text)
    print(f"📝 Parsed {len(turns)} speaker turns")
    print(f"   Jordan: {sum(1 for t in turns if t['speaker'] == 'Jordan')} turns")
    print(f"   Alex: {sum(1 for t in turns if t['speaker'] == 'Alex')} turns")

    # Split into chunks (aim for ~1000 words per chunk for context)
    max_words_per_chunk = 1000
    chunks = []
    current_chunk = []
    current_word_count = 0

    for turn in turns:
        word_count = len(turn['text'].split())
        if current_word_count + word_count > max_words_per_chunk and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_word_count = 0

        current_chunk.append(turn)
        current_word_count += word_count

    if current_chunk:
        chunks.append(current_chunk)

    print(f"🎬 Split into {len(chunks)} chunks for generation")

    # Generate audio for each chunk
    temp_dir = Path(tempfile.mkdtemp())
    chunk_files = []
    total_start_time = time.time()

    for i, chunk_turns in enumerate(chunks, 1):
        word_count = sum(len(t['text'].split()) for t in chunk_turns)
        turn_count = len(chunk_turns)
        print(f"\n🎙️  Generating chunk {i}/{len(chunks)} ({turn_count} turns, {word_count} words)...")

        try:
            # Build the dialogue prompt
            dialogue_lines = []
            for turn in chunk_turns:
                dialogue_lines.append(f"{turn['speaker']}: {turn['text']}")

            dialogue_text = '\n'.join(dialogue_lines)

            # Add context for natural TTS
            prompt = f"""TTS the following conversation between Jordan and Alex for a platform engineering podcast:

{dialogue_text}

Context: Jordan asks questions and challenges assumptions (firm, analytical tone). Alex provides detailed explanations with real-world examples (warm, explanatory tone)."""

            print(f"  Sending to Gemini 2.5 Pro TTS...")
            chunk_start = time.time()

            # Generate with multi-speaker configuration
            response = client.models.generate_content(
                model="gemini-2.5-pro-preview-tts",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                            speaker_voice_configs=[
                                types.SpeakerVoiceConfig(
                                    speaker='Jordan',
                                    voice_config=types.VoiceConfig(
                                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                            voice_name='Kore',  # Firm voice
                                        )
                                    )
                                ),
                                types.SpeakerVoiceConfig(
                                    speaker='Alex',
                                    voice_config=types.VoiceConfig(
                                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                            voice_name='Algieba',  # Match Chirp 3 HD
                                        )
                                    )
                                ),
                            ]
                        )
                    )
                )
            )

            # Extract audio data (24kHz PCM)
            audio_data = response.candidates[0].content.parts[0].inline_data.data
            chunk_time = time.time() - chunk_start

            print(f"  ✓ Generated {len(audio_data):,} bytes in {chunk_time:.1f}s")

            # Save as WAV first
            wav_file = temp_dir / f"chunk_{i:03d}.wav"
            wave_file(str(wav_file), audio_data)

            # Convert WAV to MP3 using ffmpeg
            mp3_file = temp_dir / f"chunk_{i:03d}.mp3"
            subprocess.run([
                'ffmpeg', '-y', '-i', str(wav_file),
                '-acodec', 'libmp3lame', '-b:a', '192k',
                str(mp3_file)
            ], check=True, capture_output=True)

            wav_file.unlink()  # Remove WAV to save space
            chunk_files.append(mp3_file)

            # Get duration
            try:
                result = subprocess.run([
                    'ffprobe', '-v', 'error', '-show_entries',
                    'format=duration', '-of',
                    'default=noprint_wrappers=1:nokey=1',
                    str(mp3_file)
                ], capture_output=True, text=True, check=True)
                duration = float(result.stdout.strip())
                print(f"  ⏱️  Duration: {duration:.1f}s")
            except:
                pass

        except Exception as e:
            print(f"  ❌ Error generating chunk {i}: {e}")
            import traceback
            traceback.print_exc()
            continue

        # Rate limiting (be respectful)
        if i < len(chunks):
            time.sleep(2)

    # Combine all MP3 chunks using ffmpeg
    if chunk_files:
        print(f"\n🎵 Combining {len(chunk_files)} audio segments...")

        # Create ffmpeg concat file
        concat_file = temp_dir / "concat.txt"
        with open(concat_file, 'w') as f:
            for chunk_file in chunk_files:
                f.write(f"file '{chunk_file}'\n")

        # Combine with ffmpeg
        try:
            subprocess.run([
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',
                str(output_path)
            ], check=True, capture_output=True, text=True)

            print(f"💾 Exported to: {output_path}")

            # Get final duration and size
            result = subprocess.run([
                'ffprobe', '-v', 'error', '-show_entries',
                'format=duration', '-of',
                'default=noprint_wrappers=1:nokey=1',
                str(output_path)
            ], capture_output=True, text=True)

            if result.returncode == 0:
                duration_sec = float(result.stdout.strip())
                duration_min = duration_sec / 60
                file_size_mb = output_path.stat().st_size / (1024 * 1024)
                total_time = time.time() - total_start_time

                print(f"\n✅ Generation Complete!")
                print(f"   Duration: {duration_min:.1f} minutes ({duration_sec:.0f}s)")
                print(f"   File size: {file_size_mb:.2f} MB")
                print(f"   Generation time: {total_time/60:.1f} minutes")
                print(f"   Speed: {duration_sec/total_time:.2f}x realtime")

        except subprocess.CalledProcessError as e:
            print(f"❌ Error combining audio: {e}")
            print(f"   stdout: {e.stdout}")
            print(f"   stderr: {e.stderr}")

        # Clean up temp files
        for chunk_file in chunk_files:
            chunk_file.unlink()
        concat_file.unlink()
        temp_dir.rmdir()

    else:
        print("❌ No audio segments generated")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_podcast_with_gemini_multispeaker.py <script_path> <output_path>")
        print("")
        print("Arguments:")
        print("  script_path:  Path to podcast script with Jordan:/Alex: speaker labels")
        print("  output_path:  Where to save the generated MP3")
        print("")
        print("Example:")
        print("  python generate_podcast_with_gemini_multispeaker.py \\")
        print("    ../docs/podcasts/scripts/00012-platform-roi-calculator.txt \\")
        print("    episodes/00012-platform-roi-calculator/00012-gemini.mp3")
        sys.exit(1)

    script_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        sys.exit(1)

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"🎙️  Gemini Multi-Speaker TTS Podcast Generator")
    print(f"   Model: gemini-2.5-pro-preview-tts")
    print(f"   Voices: Jordan (Kore), Alex (Algieba)")
    print(f"   Script: {script_path}")
    print(f"   Output: {output_path}")
    print()

    generate_podcast_audio_gemini(script_path, output_path)
