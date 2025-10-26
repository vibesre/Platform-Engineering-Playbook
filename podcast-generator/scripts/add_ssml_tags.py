#!/usr/bin/env python3
"""
Add SSML pause tags to podcast scripts for more natural TTS.

Strategic placement of pause tags:
- After statistics and key numbers (emphasis)
- After rhetorical questions (for effect)
- After lists (to separate items)
- Before major topic transitions
- After "But", "However", "Though" (dramatic pauses)
"""

import re
from pathlib import Path
import argparse


def add_strategic_pauses(text: str) -> str:
    """
    Add strategic pause tags to text for more natural speech.

    Args:
        text: Script text without SSML tags

    Returns:
        Text with SSML pause tags added
    """
    # Don't add tags if they already exist
    if '[pause' in text:
        print("  ⚠️  Script already contains pause tags, skipping")
        return text

    # Pattern 1: After statistics and percentages
    # Example: "productivity went up 55%, everyone was happy"
    text = re.sub(r'(\d+%)', r'\1 [pause]', text)

    # Pattern 2: After dollar amounts
    # Example: "$47,000 a month"
    text = re.sub(r'(\$[\d,]+)', r'\1', text)  # Don't add pause after money yet

    # Pattern 3: After rhetorical questions
    # Example: "What's the catch?"
    text = re.sub(r'(\?)\s+([A-Z])', r'\1 [pause] \2', text)

    # Pattern 4: After dramatic introductions
    # "Here's the kicker", "But here's what's clever", etc.
    text = re.sub(r'(kicker|catch|surprise) -', r'\1 - [pause]', text, flags=re.IGNORECASE)

    # Pattern 5: After contrast words
    text = re.sub(r'(But|However|Though),', r'\1, [pause]', text)
    text = re.sub(r'(\. )(But |However |Though )', r'\1[pause] \2', text)

    # Pattern 6: After "Wait" and similar interruptions
    text = re.sub(r'(Wait|Hold on|Hang on),', r'\1, [pause short]', text)

    # Pattern 7: Before lists (after colons introducing examples)
    text = re.sub(r':\s+"', r': [pause] "', text)

    # Pattern 8: After emphatic statements ending in "."
    # Example: "That's massive."
    emphatic_endings = ['massive', 'huge', 'transformational', 'wild', 'alarming', 'compelling']
    for word in emphatic_endings:
        text = re.sub(rf'({word})\.\s+([A-Z])', r'\1. [pause] \2', text, flags=re.IGNORECASE)

    # Clean up any double pauses
    text = re.sub(r'\[pause\]\s*\[pause\]', '[pause]', text)
    text = re.sub(r'\[pause\]\s*\[pause short\]', '[pause]', text)

    # Clean up spacing around pauses
    text = re.sub(r'\s*\[pause\]\s*', ' [pause] ', text)
    text = re.sub(r'\s*\[pause short\]\s*', ' [pause short] ', text)
    text = re.sub(r'\s*\[pause long\]\s*', ' [pause long] ', text)

    # Clean up multiple spaces
    text = re.sub(r'\s{2,}', ' ', text)

    return text


def process_script_file(script_path: Path, dry_run: bool = False) -> dict:
    """
    Add SSML tags to a podcast script file.

    Args:
        script_path: Path to the script file
        dry_run: If True, don't write changes

    Returns:
        Dict with processing stats
    """
    print(f"\nProcessing: {script_path.name}")

    # Read original content
    with open(script_path, 'r') as f:
        original = f.read()

    # Add strategic pauses
    modified = add_strategic_pauses(original)

    # Count changes
    original_pauses = len(re.findall(r'\[pause', original))
    new_pauses = len(re.findall(r'\[pause', modified))
    added_pauses = new_pauses - original_pauses

    stats = {
        'file': script_path.name,
        'original_pauses': original_pauses,
        'new_pauses': new_pauses,
        'added_pauses': added_pauses,
        'changed': original != modified
    }

    print(f"  Pauses: {original_pauses} → {new_pauses} (+{added_pauses})")

    # Write changes if not dry run
    if not dry_run and stats['changed']:
        # Backup original
        backup_path = script_path.with_suffix('.txt.bak')
        with open(backup_path, 'w') as f:
            f.write(original)
        print(f"  ✓ Backup created: {backup_path.name}")

        # Write modified
        with open(script_path, 'w') as f:
            f.write(modified)
        print(f"  ✓ Updated with SSML tags")
    elif dry_run:
        print(f"  (Dry run - no changes written)")

    return stats


def main():
    """Process podcast scripts to add SSML tags."""
    parser = argparse.ArgumentParser(
        description="Add SSML pause tags to podcast scripts for more natural TTS"
    )

    parser.add_argument(
        "scripts_dir",
        type=Path,
        default=Path("../docs/podcasts/scripts"),
        nargs='?',
        help="Directory containing podcast scripts (default: ../docs/podcasts/scripts)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without writing files"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Process a specific file instead of entire directory"
    )

    args = parser.parse_args()

    if args.file:
        # Process single file
        script_path = Path(args.file)
        if not script_path.exists():
            print(f"Error: File not found: {script_path}")
            return

        stats = process_script_file(script_path, dry_run=args.dry_run)

        print("\n" + "="*80)
        print(f"Summary: Added {stats['added_pauses']} pause tags")

    else:
        # Process directory
        if not args.scripts_dir.exists():
            print(f"Error: Directory not found: {args.scripts_dir}")
            return

        scripts = sorted(args.scripts_dir.glob("*.txt"))
        if not scripts:
            print(f"No script files found in {args.scripts_dir}")
            return

        print(f"Found {len(scripts)} script files")

        all_stats = []
        for script_path in scripts:
            stats = process_script_file(script_path, dry_run=args.dry_run)
            all_stats.append(stats)

        # Print summary
        print("\n" + "="*80)
        print("Summary:")
        total_added = sum(s['added_pauses'] for s in all_stats)
        print(f"  Total files: {len(all_stats)}")
        print(f"  Total pauses added: {total_added}")

        if args.dry_run:
            print("\n  This was a dry run. Use without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
