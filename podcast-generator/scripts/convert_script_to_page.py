#!/usr/bin/env python3
"""
Convert podcast script (.txt) to episode page format (.md).

Strips SSML tags and formats for web display.
"""

import re
import sys
from pathlib import Path


def strip_ssml_tags(text: str) -> str:
    """Remove all SSML tags from text."""

    # Remove <phoneme> tags
    text = re.sub(r'<phoneme[^>]*>([^<]+)</phoneme>', r'\1', text)

    # Remove <say-as> tags
    text = re.sub(r'<say-as[^>]*>([^<]+)</say-as>', r'\1', text)

    # Remove pause tags
    text = re.sub(r'\[pause(?:\s+\w+)?\]', '', text)

    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text


def convert_script_to_dialogue(script_path: Path) -> str:
    """Convert script file to episode page dialogue format."""

    with open(script_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    dialogue = []
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Parse speaker and dialogue
        if ':' in line:
            parts = line.split(':', 1)
            speaker = parts[0].strip()
            text = parts[1].strip() if len(parts) > 1 else ""

            # Strip SSML tags
            text = strip_ssml_tags(text)

            # Format as markdown
            dialogue.append(f"**{speaker}**: {text}\n")

    return '\n'.join(dialogue)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 convert_script_to_page.py <script.txt> <episode.md>")
        sys.exit(1)

    script_path = Path(sys.argv[1])
    episode_path = Path(sys.argv[2])

    if not script_path.exists():
        print(f"Error: Script file not found: {script_path}")
        sys.exit(1)

    # Convert script to dialogue
    dialogue = convert_script_to_dialogue(script_path)

    # Read existing episode page to get frontmatter and metadata
    with open(episode_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract frontmatter and metadata section
    frontmatter_match = re.search(r'^(---\n.*?---\n)', content, re.DOTALL)
    metadata_match = re.search(
        r'(# .*?\n\n## The Platform Engineering Playbook Podcast.*?---\n)',
        content,
        re.DOTALL
    )

    if not frontmatter_match or not metadata_match:
        print("Error: Could not find frontmatter or metadata section in episode page")
        sys.exit(1)

    frontmatter = frontmatter_match.group(1)
    metadata = metadata_match.group(1)

    # Build new content
    new_content = frontmatter + '\n' + metadata + '\n' + dialogue

    # Write updated episode page
    with open(episode_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ Updated {episode_path}")
    print(f"  Converted {len(dialogue.split('**'))} speaker entries")


if __name__ == "__main__":
    main()
