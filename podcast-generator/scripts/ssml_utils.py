#!/usr/bin/env python3
"""
Utility functions for handling SSML tags in podcast scripts.
"""

import re
from pathlib import Path
from typing import Dict


def strip_ssml_tags(text: str) -> str:
    """
    Remove all SSML/pause tags from text for display purposes.

    Supported tags:
    - [pause]
    - [pause short]
    - [pause long]

    Args:
        text: Text containing SSML tags

    Returns:
        Text with SSML tags removed
    """
    # Remove all pause tags
    text = re.sub(r'\[pause\s*(?:short|long)?\]', '', text)

    # Clean up any double spaces left by tag removal
    text = re.sub(r'\s{2,}', ' ', text)

    # Clean up spaces before punctuation
    text = re.sub(r'\s+([,.])', r'\1', text)

    return text.strip()


def process_script_for_display(script_path: Path) -> str:
    """
    Read a podcast script and return it with SSML tags stripped for blog display.

    Args:
        script_path: Path to the podcast script file

    Returns:
        Script content with SSML tags removed
    """
    with open(script_path, 'r') as f:
        content = f.read()

    return strip_ssml_tags(content)


def format_script_for_markdown(script_path: Path) -> str:
    """
    Convert a podcast script to markdown format with SSML tags stripped.

    Format:
    - Speaker names become bold markdown
    - Dialogue is properly formatted
    - SSML tags are removed

    Args:
        script_path: Path to the podcast script file

    Returns:
        Markdown-formatted script
    """
    with open(script_path, 'r') as f:
        content = f.read()

    # Strip SSML tags
    content = strip_ssml_tags(content)

    # Convert speaker format to markdown
    # "Speaker 1:" or "Speaker 2:" becomes "**Speaker 1**:" or "**Speaker 2**:"
    lines = []
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            lines.append('')
            continue

        # Match speaker pattern and convert to bold
        speaker_match = re.match(r'^(Speaker \d+):\s*(.*)$', line)
        if speaker_match:
            speaker = speaker_match.group(1)
            dialogue = speaker_match.group(2)
            lines.append(f'**{speaker}**: {dialogue}')
            lines.append('')  # Add blank line after each speaker's dialogue
        else:
            lines.append(line)

    return '\n'.join(lines).strip()


def validate_ssml_tags(script_path: Path) -> dict:
    """
    Validate SSML tags in a script and report statistics.

    Args:
        script_path: Path to the podcast script file

    Returns:
        Dict with validation results and statistics
    """
    with open(script_path, 'r') as f:
        content = f.read()

    # Count different pause types
    pause_count = len(re.findall(r'\[pause\]', content))
    pause_short_count = len(re.findall(r'\[pause short\]', content))
    pause_long_count = len(re.findall(r'\[pause long\]', content))

    # Find any malformed tags
    malformed = re.findall(r'\[pause [^\]]+\]', content)
    # Filter out valid tags
    valid_patterns = ['[pause short]', '[pause long]']
    malformed = [tag for tag in malformed if tag not in valid_patterns]

    return {
        'total_pauses': pause_count + pause_short_count + pause_long_count,
        'pause': pause_count,
        'pause_short': pause_short_count,
        'pause_long': pause_long_count,
        'malformed_tags': malformed,
        'is_valid': len(malformed) == 0
    }


def main():
    """Test the SSML utilities."""
    # Test text with SSML tags
    test_text = """Speaker 1: This is a test. [pause] Here's another sentence. [pause short] And one more. [pause long] Final sentence."""

    print("Original text:")
    print(test_text)
    print("\nStripped text:")
    print(strip_ssml_tags(test_text))

    print("\n" + "="*80 + "\n")

    # Test with actual script file if available
    script_dir = Path("../docs/podcasts/scripts")
    if script_dir.exists():
        scripts = list(script_dir.glob("*.txt"))
        if scripts:
            test_script = scripts[0]
            print(f"Testing with: {test_script.name}")

            validation = validate_ssml_tags(test_script)
            print(f"\nValidation results:")
            print(f"  Total pauses: {validation['total_pauses']}")
            print(f"  [pause]: {validation['pause']}")
            print(f"  [pause short]: {validation['pause_short']}")
            print(f"  [pause long]: {validation['pause_long']}")
            print(f"  Valid: {validation['is_valid']}")

            if validation['malformed_tags']:
                print(f"  Malformed tags: {validation['malformed_tags']}")


if __name__ == "__main__":
    main()
