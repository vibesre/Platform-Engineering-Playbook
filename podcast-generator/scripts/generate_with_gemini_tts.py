#!/usr/bin/env python3
"""
Generate podcast audio using Gemini's multimodal TTS with enhanced instructor persona.
This uses Gemini 2.0's live audio generation capabilities with detailed prompting.
"""

import os
import sys
import time
import subprocess
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Detailed instructor persona for platform engineering education
INSTRUCTOR_PERSONA = """You are an experienced platform engineering instructor with 15+ years in production systems.

## Voice Characteristics:
- Tone: Authoritative yet approachable, like a senior engineer mentoring
- Pacing: Measured and deliberate - you pause after key concepts to let them sink in
- Energy: Sustained focus and enthusiasm for the subject matter
- Clarity: Crystal-clear articulation of technical terms (Kubernetes as "coo-ber-NET-iss", SIGKILL as "sig-kill")

## Teaching Style:
- You speak from real production experience, not theory
- You emphasize "why" before "how" - motivation before implementation
- You use specific numbers and scenarios ("exit code 137", "800 megabytes") not vague statements
- You signal transitions clearly ("Let's walk through...", "Here's what trips people up...")
- You build suspense around failure scenarios to maintain engagement
- You pause strategically: short pauses for list items, longer pauses for dramatic reveals

## Personality Traits:
- Pragmatic: "Here's what works in production" vs academic theory
- Honest: "This will bite you at 3 AM" - you warn about real consequences
- Patient: You explain complex concepts multiple times with different analogies
- Systematic: You follow structured debugging workflows, numbered steps

## Technical Credibility:
- You've debugged OOMKilled pods at scale (67% of teams experience this)
- You know the difference between theory and production reality
- You reference specific Kubernetes internals (cgroups, kernel OOMKiller, exit codes)
- You provide concrete examples: "Node has 8 GB total, 6 GB in requests, 2 GB available"

When reading the lesson content, embody this instructor persona fully. Your voice should sound like you're in a classroom, making eye contact, and genuinely invested in the student understanding production Kubernetes."""


def generate_lesson_audio_gemini(script_path: Path, output_path: Path):
    """
    Generate audio using Gemini 2.0's audio generation with instructor persona.

    Args:
        script_path: Path to lesson script
        output_path: Where to save the generated MP3
    """
    # Configure Gemini
    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_AI_API_KEY not set")

    genai.configure(api_key=api_key)

    # Read the lesson script
    print(f"📖 Reading lesson script: {script_path}")
    with open(script_path, 'r') as f:
        script_text = f.read()

    # Remove SSML tags and speaker labels for Gemini
    import re
    # Remove speaker labels (Autonoe:)
    script_text = re.sub(r'^Autonoe:\s*', '', script_text, flags=re.MULTILINE)
    # Remove SSML phoneme tags but keep the text
    script_text = re.sub(r'<phoneme[^>]*>([^<]+)</phoneme>', r'\1', script_text)
    # Remove say-as tags
    script_text = re.sub(r'<say-as[^>]*>([^<]+)</say-as>', r'\1', script_text)
    # Remove pause tags
    script_text = re.sub(r'\[pause[^\]]*\]', '', script_text)

    print(f"📝 Script length: {len(script_text)} characters, {len(script_text.split())} words")

    # Split into chunks (Gemini has token limits)
    max_words_per_chunk = 500  # Conservative limit for audio generation
    words = script_text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words_per_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    print(f"🎬 Split into {len(chunks)} chunks for generation")

    # Generate audio for each chunk
    temp_dir = Path(tempfile.mkdtemp())
    chunk_files = []

    for i, chunk_text in enumerate(chunks, 1):
        print(f"\n🎙️  Generating chunk {i}/{len(chunks)} ({len(chunk_text.split())} words)...")

        try:
            # Create the generation config with audio output
            # Using gemini-pro for better quality and instruction following
            model = genai.GenerativeModel('gemini-pro')

            # Construct prompt with full instructor persona
            full_prompt = f"""{INSTRUCTOR_PERSONA}

Now, deliver this lesson segment in your instructor voice. Remember: you're teaching production Kubernetes resource management to senior engineers who need to understand this deeply.

Lesson content:
{chunk_text}

Deliver this naturally as if you're teaching in person. Use appropriate pacing, pauses, and emphasis on key technical terms."""

            print(f"  Sending to Gemini with instructor persona...")

            # Generate with audio modality
            response = model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    response_modalities=["AUDIO"],
                    speech_config=genai.SpeechConfig(
                        voice_config=genai.VoiceConfig(
                            prebuilt_voice_config=genai.PrebuiltVoiceConfig(
                                voice_name="Kore"  # High-quality voice
                            )
                        )
                    )
                )
            )

            # Extract audio data
            if hasattr(response, 'audio_data') and response.audio_data:
                audio_data = response.audio_data
                print(f"  ✓ Generated {len(audio_data)} bytes of audio")

                # Save chunk as temporary MP3
                chunk_file = temp_dir / f"chunk_{i:03d}.mp3"
                with open(chunk_file, 'wb') as f:
                    f.write(audio_data)
                chunk_files.append(chunk_file)

            else:
                print(f"  ⚠️  No audio data in response")
                print(f"  Response type: {type(response)}")
                print(f"  Response attributes: {dir(response)}")

        except Exception as e:
            print(f"  ❌ Error generating chunk {i}: {e}")
            print(f"     Error type: {type(e)}")
            import traceback
            traceback.print_exc()

        # Rate limiting
        time.sleep(2)

    # Combine all audio chunks using ffmpeg
    if chunk_files:
        print(f"\n🎵 Combining {len(chunk_files)} audio segments with ffmpeg...")

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

            # Get duration using ffprobe
            result = subprocess.run([
                'ffprobe', '-v', 'error', '-show_entries',
                'format=duration', '-of',
                'default=noprint_wrappers=1:nokey=1',
                str(output_path)
            ], capture_output=True, text=True)

            if result.returncode == 0:
                duration_sec = float(result.stdout.strip())
                duration_min = duration_sec / 60
                print(f"✅ Complete! Duration: {duration_min:.1f} minutes")
            else:
                print(f"✅ Complete! (Could not determine duration)")

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


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_with_gemini_tts.py <script_path> <output_path>")
        sys.exit(1)

    script_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        sys.exit(1)

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    generate_lesson_audio_gemini(script_path, output_path)
