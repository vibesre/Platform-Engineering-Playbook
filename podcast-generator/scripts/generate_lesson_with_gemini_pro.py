#!/usr/bin/env python3
"""
Generate lesson audio using Gemini Pro to enhance the script, then Google Cloud TTS.
This approach uses Gemini Pro's instruction-following to add natural teaching cadence,
then generates high-quality audio with Chirp 3 HD.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import re

# Load environment variables
load_dotenv()

# Instructor persona for Gemini Pro enhancement
INSTRUCTOR_ENHANCEMENT_PROMPT = """You are rewriting a technical lesson script to add natural teaching cadence and emphasis.

**Your task**: Add subtle markdown formatting to indicate where the instructor should:
- **Bold** key technical terms for emphasis
- *Italics* for conceptual explanations
- Add "(pause)" where the instructor should pause for effect
- Add "(dramatic pause)" before revealing critical information
- Keep all technical content EXACTLY as written - don't change facts, numbers, or explanations

**Teaching style markers to add**:
- Before failure scenarios: "(dramatic pause)"
- After key statistics: "(pause)"
- Before numbered steps: "(pause - let it sink in)"
- After rhetorical questions: "(pause for reflection)"

**What NOT to change**:
- Technical terms (Kubernetes, SIGKILL, OOMKilled, etc.)
- Numbers and statistics
- Code examples or commands
- The actual content or meaning

**Example input**:
"Exit code 137—OOMKilled—is the single most common production failure in Kubernetes."

**Example output**:
"Exit code **137** *(dramatic pause)* **OOMKilled** *(pause)* is the single most common production failure in **Kubernetes**."

Now enhance this lesson script:

"""


def enhance_script_with_gemini_pro(script_text: str, api_key: str) -> str:
    """Use Gemini Pro to enhance script with teaching cadence markers."""
    genai.configure(api_key=api_key)
    # Use gemini-2.5-pro for best instruction following
    model = genai.GenerativeModel('gemini-2.5-pro')

    print("📝 Enhancing script with Gemini Pro teaching persona...")

    # Split into manageable chunks (Gemini Pro has token limits)
    max_words = 2000
    words = script_text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    enhanced_chunks = []

    for i, chunk in enumerate(chunks, 1):
        print(f"  Processing chunk {i}/{len(chunks)}...")

        try:
            response = model.generate_content(
                INSTRUCTOR_ENHANCEMENT_PROMPT + chunk,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,  # Lower temperature for consistency
                    top_p=0.8,
                )
            )

            enhanced_text = response.text
            enhanced_chunks.append(enhanced_text)
            print(f"    ✓ Enhanced {len(chunk.split())} words")

        except Exception as e:
            print(f"    ⚠️  Error enhancing chunk {i}: {e}")
            print(f"    Using original chunk")
            enhanced_chunks.append(chunk)

    return '\n\n'.join(enhanced_chunks)


def convert_markdown_to_ssml(text: str) -> str:
    """Convert markdown teaching markers to SSML pause tags."""
    # Convert pause markers
    text = re.sub(r'\(dramatic pause\)', '[pause long]', text)
    text = re.sub(r'\(pause for reflection\)', '[pause]', text)
    text = re.sub(r'\(pause - let it sink in\)', '[pause]', text)
    text = re.sub(r'\(pause\)', '[pause short]', text)

    # Remove markdown emphasis (Chirp 3 will use intonation naturally)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italics

    return text


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_lesson_with_gemini_pro.py <script_path> <output_prefix>")
        print("  Will generate: <output_prefix>-enhanced-script.txt and <output_prefix>.mp3")
        sys.exit(1)

    script_path = Path(sys.argv[1])
    output_prefix = sys.argv[2]

    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        sys.exit(1)

    # Get API key
    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key:
        print("Error: GOOGLE_AI_API_KEY not set")
        sys.exit(1)

    # Read original script
    print(f"📖 Reading script: {script_path}")
    with open(script_path, 'r') as f:
        original_script = f.read()

    # Remove existing SSML tags and speaker labels
    script_text = re.sub(r'^Autonoe:\s*', '', original_script, flags=re.MULTILINE)
    script_text = re.sub(r'<phoneme[^>]*>([^<]+)</phoneme>', r'\1', script_text)
    script_text = re.sub(r'<say-as[^>]*>([^<]+)</say-as>', r'\1', script_text)
    script_text = re.sub(r'\[pause[^\]]*\]', '', script_text)

    print(f"   Script: {len(script_text.split())} words")

    # Enhance with Gemini Pro
    enhanced_script = enhance_script_with_gemini_pro(script_text, api_key)

    # Convert markdown markers to SSML
    print("\n🎨 Converting teaching markers to SSML...")
    ssml_script = convert_markdown_to_ssml(enhanced_script)

    # Add speaker label back
    ssml_lines = []
    for line in ssml_script.split('\n'):
        if line.strip():
            ssml_lines.append(f"Autonoe: {line}")
        else:
            ssml_lines.append('')

    ssml_script = '\n'.join(ssml_lines)

    # Save enhanced script
    enhanced_script_path = f"{output_prefix}-gemini-enhanced.txt"
    print(f"\n💾 Saving enhanced script: {enhanced_script_path}")
    with open(enhanced_script_path, 'w') as f:
        f.write(ssml_script)

    print(f"\n✅ Enhanced script ready!")
    print(f"   Original: {len(original_script.split())} words")
    print(f"   Enhanced: {len(enhanced_script.split())} words")
    print(f"\n🎙️  To generate audio with Chirp 3 HD:")
    print(f"   cd podcast-generator")
    print(f"   python3 scripts/generate_podcast.py {enhanced_script_path} --lesson --episode-id lesson-02-gemini-enhanced")


if __name__ == "__main__":
    main()
