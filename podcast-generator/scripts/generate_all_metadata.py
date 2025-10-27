#!/usr/bin/env python3
"""
Generate metadata .txt files for all existing episodes in episodes/*/ directories.
"""

import re
from pathlib import Path
from typing import Optional

def get_episode_duration(mp3_path: Path) -> Optional[float]:
    """Get duration of mp3 file in minutes using ffprobe."""
    import subprocess
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(mp3_path)],
            capture_output=True,
            text=True,
            check=True
        )
        duration_seconds = float(result.stdout.strip())
        return round(duration_seconds / 60, 1)
    except:
        return None

def extract_episode_title(episode_id: str) -> str:
    """Convert episode ID to title."""
    # Remove numeric prefix if present
    parts = episode_id.split('-')
    if parts[0].isdigit():
        title_parts = parts[1:]
    else:
        title_parts = parts

    return ' '.join(word.capitalize() for word in title_parts)

def generate_metadata_content(episode_id: str, duration_minutes: Optional[float]) -> str:
    """Generate metadata content for an episode."""

    title = extract_episode_title(episode_id)

    # Use full episode ID for URL (including episode number)
    # This matches the numbered URL format: /podcasts/00005-topic-name
    episode_slug = episode_id

    duration_str = f"{duration_minutes} minutes" if duration_minutes else "[Duration unknown]"

    return f"""Title: {title}

Description:
[Episode description - edit this to add a compelling hook and explain what listeners will learn]

🔗 Full episode page: https://platformengineeringplaybook.com/podcasts/{episode_slug}

📝 See a mistake or have insights to add? This podcast is community-driven - open a PR on GitHub to contribute your perspective!

Summary:
• [Key takeaway 1]
• [Key takeaway 2]
• [Key takeaway 3]
• [Key takeaway 4]
• [Key takeaway 5]

Duration: {duration_str}

Speakers: Alex and Jordan
Target Audience: Senior platform engineers, SREs, DevOps engineers with 5+ years experience
"""

def generate_all_metadata():
    """Generate metadata files for all episodes in episodes/*/ directories."""

    base_dir = Path(__file__).parent.parent
    episodes_dir = base_dir / "episodes"

    if not episodes_dir.exists():
        print(f"❌ Error: {episodes_dir} does not exist")
        return

    # Find all episode directories
    episode_dirs = sorted([d for d in episodes_dir.iterdir() if d.is_dir()])

    if not episode_dirs:
        print("No episode directories found in episodes/")
        return

    # Collect all MP3 files from episode directories (not from history/)
    mp3_files = []
    for episode_dir in episode_dirs:
        for mp3 in episode_dir.glob('*.mp3'):
            # Skip files in history subdirectories
            if 'history' not in mp3.parts:
                mp3_files.append(mp3)

    if not mp3_files:
        print("No mp3 files found in episode directories")
        return

    print(f"Found {len(mp3_files)} episodes in episodes/*/\n")

    generated = 0
    skipped = 0

    for mp3_path in sorted(mp3_files):
        episode_id = mp3_path.stem
        # Place metadata in the same directory as the MP3
        txt_path = mp3_path.parent / f"{episode_id}.txt"

        # Check if metadata file already exists
        if txt_path.exists():
            print(f"⏭️  Skipping {episode_id}.txt (already exists)")
            skipped += 1
            continue

        # Get duration
        duration = get_episode_duration(mp3_path)

        # Generate metadata
        metadata = generate_metadata_content(episode_id, duration)

        # Write file
        with open(txt_path, 'w') as f:
            f.write(metadata)

        print(f"✅ Generated {episode_id}.txt ({duration} min)")
        generated += 1

    print(f"\n📊 Summary:")
    print(f"   ✨ Generated: {generated} files")
    print(f"   ⏭️  Skipped: {skipped} files (already exist)")
    print(f"\n💡 Note: Edit the .txt files to add compelling descriptions and summaries!")

if __name__ == "__main__":
    generate_all_metadata()
