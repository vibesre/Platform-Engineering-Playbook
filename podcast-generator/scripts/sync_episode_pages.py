#!/usr/bin/env python3
"""
Sync podcast episode markdown pages from raw scripts.
Strips SSML tags from scripts for clean blog display.
"""

import re
import json
from pathlib import Path
import argparse
from ssml_utils import strip_ssml_tags


def get_episode_metadata(episode_base_name: str, metadata_dir: Path) -> dict:
    """Load episode metadata from JSON file."""
    metadata_file = metadata_dir / f"{episode_base_name}.json"
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            return json.load(f)
    return {}


def parse_script_sections(script_content: str) -> list:
    """
    Parse script into logical sections based on speaker transitions and topic shifts.

    Returns list of sections with title and dialogues.
    """
    # Strip SSML tags first
    clean_content = strip_ssml_tags(script_content)

    lines = clean_content.strip().split('\n')

    sections = []
    current_section = None
    current_dialogues = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this is a speaker line
        speaker_match = re.match(r'^(Speaker \d+):\s*(.*)$', line)
        if speaker_match:
            speaker = speaker_match.group(1)
            dialogue = speaker_match.group(2)

            # Map Speaker 1/2 to actual names (based on intro convention)
            if speaker == "Speaker 1":
                speaker_name = "Jordan"
            else:
                speaker_name = "Alex"

            current_dialogues.append({
                'speaker': speaker_name,
                'text': dialogue
            })

    # Group dialogues into sections (every 8-12 exchanges)
    if current_dialogues:
        sections.append({
            'title': 'Episode Transcript',
            'dialogues': current_dialogues
        })

    return sections


def format_dialogue_markdown(dialogue: dict) -> str:
    """Format a single dialogue exchange as markdown."""
    return f"**{dialogue['speaker']}**: {dialogue['text']}\n"


def generate_episode_page(script_path: Path, metadata_dir: Path, output_dir: Path) -> Path:
    """
    Generate episode markdown page from script file.

    Args:
        script_path: Path to raw script file
        metadata_dir: Directory containing episode metadata JSON files
        output_dir: Directory to write markdown file

    Returns:
        Path to generated markdown file
    """
    # Extract episode base name (without number prefix)
    # e.g., "00001-ai-platform-engineering-episode.txt" -> "ai-platform-engineering-episode"
    filename = script_path.stem
    match = re.match(r'^\d+-(.+)$', filename)
    if match:
        episode_base_name = match.group(1)
    else:
        episode_base_name = filename

    print(f"Processing: {script_path.name} → {episode_base_name}.md")

    # Load metadata
    metadata = get_episode_metadata(episode_base_name, metadata_dir)

    # Read script
    with open(script_path, 'r') as f:
        script_content = f.read()

    # Parse sections
    sections = parse_script_sections(script_content)

    # Build markdown content
    md_lines = []

    # Frontmatter
    md_lines.append("---")
    md_lines.append("displayed_sidebar: tutorialSidebar")
    md_lines.append("hide_table_of_contents: false")

    title = metadata.get('title', episode_base_name.replace('-', ' ').title())
    md_lines.append(f"sidebar_label: \"🎙️ {title}\"")
    md_lines.append("---")
    md_lines.append("")

    # Header
    full_title = metadata.get('full_title', title)
    subtitle = metadata.get('subtitle', '')
    if subtitle:
        md_lines.append(f"# {full_title} - {subtitle}")
    else:
        md_lines.append(f"# {full_title}")
    md_lines.append("")
    md_lines.append("## The Platform Engineering Playbook Podcast")
    md_lines.append("")
    md_lines.append("<GitHubButtons />")
    md_lines.append("")

    # Metadata section
    duration = metadata.get('duration', '12-15 minutes')
    md_lines.append(f"**Duration:** {duration}")
    md_lines.append("**Speakers:** Alex and Jordan")
    md_lines.append("**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience")
    md_lines.append("")

    # Blog post link if available
    blog_link = metadata.get('blog_link')
    if blog_link:
        blog_title = metadata.get('blog_title', 'Read the full blog post')
        blog_desc = metadata.get('blog_description', 'Comprehensive written analysis')
        md_lines.append(f"> 📝 **{blog_title}**: [{blog_desc}]({blog_link})")
        md_lines.append("")

    md_lines.append("---")
    md_lines.append("")

    # Content sections
    for section in sections:
        if section['title'] != 'Episode Transcript':
            md_lines.append(f"### {section['title']}")
            md_lines.append("")

        for dialogue in section['dialogues']:
            md_lines.append(format_dialogue_markdown(dialogue))

    # Write output file
    output_path = output_dir / f"{episode_base_name}.md"
    with open(output_path, 'w') as f:
        f.write('\n'.join(md_lines))

    print(f"  ✓ Generated: {output_path.name}")

    return output_path


def main():
    """Sync episode pages from raw scripts."""
    parser = argparse.ArgumentParser(
        description="Generate podcast episode pages from raw scripts (with SSML tags stripped)"
    )

    parser.add_argument(
        "scripts_dir",
        type=Path,
        nargs='?',
        default=Path("../docs/podcasts/scripts"),
        help="Directory containing podcast scripts"
    )

    parser.add_argument(
        "--metadata-dir",
        type=Path,
        default=Path("../docs/podcasts/metadata"),
        help="Directory containing episode metadata JSON files"
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("../docs/podcasts"),
        help="Directory to write episode markdown files"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Process a specific script file instead of entire directory"
    )

    args = parser.parse_args()

    # Validate directories
    if not args.scripts_dir.exists():
        print(f"Error: Scripts directory not found: {args.scripts_dir}")
        return

    if not args.metadata_dir.exists():
        print(f"Warning: Metadata directory not found: {args.metadata_dir}")
        print("Continuing without metadata...")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Process files
    if args.file:
        script_path = Path(args.file)
        if not script_path.exists():
            print(f"Error: File not found: {script_path}")
            return

        generate_episode_page(script_path, args.metadata_dir, args.output_dir)

    else:
        scripts = sorted(args.scripts_dir.glob("*.txt"))
        if not scripts:
            print(f"No script files found in {args.scripts_dir}")
            return

        print(f"Found {len(scripts)} script files\n")

        for script_path in scripts:
            try:
                generate_episode_page(script_path, args.metadata_dir, args.output_dir)
            except Exception as e:
                print(f"  ✗ Error processing {script_path.name}: {e}")

        print(f"\n✅ Synced {len(scripts)} episode pages to {args.output_dir}")


if __name__ == "__main__":
    main()
