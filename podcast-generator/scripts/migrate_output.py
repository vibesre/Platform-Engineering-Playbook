#!/usr/bin/env python3
"""
Migrate episodes from old output/ directory to new structure.
- Newest version of each episode goes to output_latest/ with clean name
- All older versions go to output_history/ with timestamps
"""

import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def extract_episode_info(filename):
    """Extract episode ID and timestamp from filename."""
    # Match patterns like: 00001-episode-name_20251010_110205.mp3
    match = re.match(r'^(.+?)_(\d{8}_\d{6})\.mp3$', filename)
    if match:
        episode_id = match.group(1)
        timestamp = match.group(2)
        return episode_id, timestamp
    return None, None

def migrate_episodes():
    """Migrate episodes from output/ to output_latest/ and output_history/."""

    # Setup directories
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "output"
    output_latest_dir = base_dir / "output_latest"
    output_history_dir = base_dir / "output_history"

    # Create directories if they don't exist
    output_latest_dir.mkdir(exist_ok=True)
    output_history_dir.mkdir(exist_ok=True)

    # Find all mp3 files in output/
    mp3_files = list(output_dir.glob("*.mp3"))

    if not mp3_files:
        print("No mp3 files found in output/ directory")
        return

    print(f"Found {len(mp3_files)} episodes in output/\n")

    # Group files by episode ID
    episodes = defaultdict(list)
    for filepath in mp3_files:
        episode_id, timestamp = extract_episode_info(filepath.name)
        if episode_id and timestamp:
            episodes[episode_id].append((filepath, timestamp))
        else:
            print(f"⚠️  Skipping file with unexpected format: {filepath.name}")

    # Process each episode
    total_latest = 0
    total_history = 0

    for episode_id, files in sorted(episodes.items()):
        print(f"\n📁 Processing: {episode_id}")
        print(f"   Found {len(files)} version(s)")

        # Sort by timestamp (newest first)
        files.sort(key=lambda x: x[1], reverse=True)

        # Check if latest version already exists in output_latest
        latest_path = output_latest_dir / f"{episode_id}.mp3"
        if latest_path.exists():
            print(f"   ✓ Latest version already exists in output_latest/")
            # Move all files from output/ to history
            for filepath, timestamp in files:
                dest = output_history_dir / filepath.name
                print(f"   📦 Moving to history: {filepath.name}")
                filepath.rename(dest)
                total_history += 1
        else:
            # Move newest to output_latest with clean name
            newest_file, newest_timestamp = files[0]
            print(f"   ✨ Moving to output_latest/: {episode_id}.mp3 (from {newest_file.name})")
            newest_file.rename(latest_path)
            total_latest += 1

            # Move older versions to history
            for filepath, timestamp in files[1:]:
                dest = output_history_dir / filepath.name
                print(f"   📦 Moving to history: {filepath.name}")
                filepath.rename(dest)
                total_history += 1

    print(f"\n✅ Migration complete!")
    print(f"📊 Summary:")
    print(f"   - {total_latest} episodes in output_latest/")
    print(f"   - {total_history} episodes moved to output_history/")

    # Check if output/ is now empty
    remaining = list(output_dir.glob("*.mp3"))
    if remaining:
        print(f"\n⚠️  Warning: {len(remaining)} files still in output/")
    else:
        print(f"\n✓ output/ directory is now empty (ready to be removed)")

if __name__ == "__main__":
    migrate_episodes()
