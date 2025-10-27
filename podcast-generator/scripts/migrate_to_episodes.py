#!/usr/bin/env python3
"""
Migrate podcast files from flat output_latest/output_history structure
to organized episodes/{episode-id}/ structure.

New structure:
  episodes/
    00001-episode-name/
      00001-episode-name.mp3
      00001-episode-name.mp4
      00001-episode-name.txt
      history/
        20251010_123456/
          00001-episode-name.mp3
          00001-episode-name.mp4
          00001-episode-name.txt
"""

import os
import shutil
import re
from pathlib import Path
from collections import defaultdict

def main():
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent

    output_latest = base_dir / "output_latest"
    output_history = base_dir / "output_history"
    episodes_dir = base_dir / "episodes"

    print("🔄 Migrating podcast files to new episode-based structure...")
    print(f"   From: {output_latest} and {output_history}")
    print(f"   To: {episodes_dir}")

    if not output_latest.exists():
        print(f"\n❌ Error: {output_latest} does not exist")
        return 1

    # Create episodes directory
    episodes_dir.mkdir(exist_ok=True)
    print(f"\n✅ Created {episodes_dir}")

    # Step 1: Migrate latest files from output_latest
    print("\n📦 Step 1: Migrating latest files...")
    latest_files = list(output_latest.glob("*"))
    episode_ids = set()

    for file_path in latest_files:
        if file_path.is_file():
            # Extract episode ID (everything before the extension)
            episode_id = file_path.stem
            extension = file_path.suffix

            # Skip files that don't match expected extensions
            if extension not in ['.mp3', '.mp4', '.txt', '.wav']:
                print(f"  ⏭️  Skipping {file_path.name} (unexpected extension)")
                continue

            episode_ids.add(episode_id)

            # Create episode directory
            episode_dir = episodes_dir / episode_id
            episode_dir.mkdir(exist_ok=True)

            # Move file to episode directory
            dest_path = episode_dir / file_path.name
            print(f"  📁 {episode_id}/ ← {file_path.name}")
            shutil.move(str(file_path), str(dest_path))

    print(f"\n✅ Migrated {len(latest_files)} latest files to {len(episode_ids)} episode directories")

    # Step 2: Migrate history files from output_history
    if output_history.exists():
        print("\n📦 Step 2: Migrating historical files...")
        history_files = list(output_history.glob("*"))

        # Group history files by episode ID
        history_by_episode = defaultdict(list)

        for file_path in history_files:
            if file_path.is_file():
                # Extract episode ID and timestamp
                # Format: 00001-episode-name_20251010_123456.mp3
                match = re.match(r'(.+?)_(\d{8}_\d{6})(\.\w+)$', file_path.name)
                if match:
                    episode_id, timestamp, extension = match.groups()
                    history_by_episode[episode_id].append((file_path, timestamp, extension))
                else:
                    print(f"  ⚠️  Could not parse timestamp from {file_path.name}, skipping")

        # Move history files to episode-specific history directories
        for episode_id, files in history_by_episode.items():
            episode_dir = episodes_dir / episode_id
            episode_dir.mkdir(exist_ok=True)

            for file_path, timestamp, extension in files:
                # Create timestamp directory under episode history
                history_dir = episode_dir / "history" / timestamp
                history_dir.mkdir(parents=True, exist_ok=True)

                # Destination filename (without timestamp)
                dest_filename = f"{episode_id}{extension}"
                dest_path = history_dir / dest_filename

                print(f"  📁 {episode_id}/history/{timestamp}/ ← {file_path.name}")
                shutil.move(str(file_path), str(dest_path))

        print(f"\n✅ Migrated historical files for {len(history_by_episode)} episodes")
    else:
        print(f"\n⏭️  No output_history directory found, skipping historical migration")

    # Step 3: Summary
    print("\n" + "="*70)
    print("📊 MIGRATION SUMMARY")
    print("="*70)

    for episode_id in sorted(episode_ids):
        episode_dir = episodes_dir / episode_id
        if episode_dir.exists():
            # Count files in episode directory (non-history)
            latest_count = len([f for f in episode_dir.iterdir() if f.is_file()])

            # Count history timestamps
            history_dir = episode_dir / "history"
            history_count = 0
            if history_dir.exists():
                history_count = len([d for d in history_dir.iterdir() if d.is_dir()])

            print(f"  {episode_id}:")
            print(f"    ├─ Latest files: {latest_count}")
            print(f"    └─ History versions: {history_count}")

    print("\n" + "="*70)
    print("✅ Migration complete!")
    print("\nNext steps:")
    print("  1. Verify the new structure looks correct")
    print("  2. Update scripts to use new paths")
    print("  3. Delete empty output_latest/ and output_history/ directories")
    print("="*70)

    return 0

if __name__ == "__main__":
    exit(main())
