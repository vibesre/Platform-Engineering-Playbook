#!/usr/bin/env python3
"""
Voice consistency report generator.
Generates detailed reports about voice usage in podcast episodes.
"""

import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict
from collections import Counter

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent))

from cache_manager import CacheManager


def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def normalize_speaker_name(speaker: str) -> str:
    """Normalize speaker name."""
    normalized = speaker.lower().strip()
    if normalized == "speaker 1":
        return "jordan"
    elif normalized == "speaker 2":
        return "alex"
    return normalized


def get_voice_mapping(config: Dict) -> Dict[str, str]:
    """Extract voice mapping from config."""
    voice_mapping = {}
    for speaker_name, speaker_config in config.get("speakers", {}).items():
        normalized_name = normalize_speaker_name(speaker_name)
        voice_mapping[normalized_name] = speaker_config["voice"]
    return voice_mapping


def generate_episode_report(episode_id: str, config_path: str = "config.yaml"):
    """Generate detailed voice report for an episode."""
    print(f"\n{'=' * 70}")
    print(f"📊 VOICE CONSISTENCY REPORT: {episode_id}")
    print(f"{'=' * 70}")

    # Load config
    config = load_config(config_path)
    voice_mapping = get_voice_mapping(config)

    # Initialize cache manager
    cache_manager = CacheManager(
        cache_dir=config["paths"]["cache_dir"],
        manifest_file=config["paths"]["manifest_file"]
    )

    # Get episode manifest
    episode_manifest = cache_manager.get_episode_manifest(episode_id)

    if not episode_manifest["chunks"]:
        print("\n⚠️  No chunks found for this episode")
        return

    # Analyze voice usage
    total_chunks = len(episode_manifest["chunks"])
    speaker_stats = {}
    voice_usage = Counter()
    mismatches = []
    unknown_voices = []

    for chunk_hash, chunk_metadata in episode_manifest["chunks"].items():
        speaker = chunk_metadata.get("speaker", "unknown")
        voice = chunk_metadata.get("voice", "unknown")
        chunk_id = chunk_metadata.get("id")

        # Track speaker stats
        if speaker not in speaker_stats:
            speaker_stats[speaker] = {
                "count": 0,
                "voices": Counter(),
                "chunks": []
            }

        speaker_stats[speaker]["count"] += 1
        speaker_stats[speaker]["voices"][voice] += 1
        speaker_stats[speaker]["chunks"].append(chunk_id)

        # Track overall voice usage
        voice_usage[voice] += 1

        # Check for mismatches
        expected_voice = voice_mapping.get(speaker)
        if voice == "unknown":
            unknown_voices.append({
                "chunk_id": chunk_id,
                "speaker": speaker,
                "hash": chunk_hash
            })
        elif expected_voice and voice != expected_voice:
            mismatches.append({
                "chunk_id": chunk_id,
                "speaker": speaker,
                "expected": expected_voice,
                "actual": voice,
                "hash": chunk_hash
            })

    # Print summary
    print(f"\n📈 SUMMARY:")
    print(f"  Total chunks: {total_chunks}")
    print(f"  Last updated: {episode_manifest.get('last_updated', 'unknown')}")

    # Print expected configuration
    print(f"\n🎯 EXPECTED CONFIGURATION:")
    for speaker, voice in sorted(voice_mapping.items()):
        print(f"  {speaker}: {voice}")

    # Print speaker statistics
    print(f"\n👥 SPEAKER STATISTICS:")
    for speaker, stats in sorted(speaker_stats.items()):
        print(f"\n  {speaker.upper()}:")
        print(f"    Total chunks: {stats['count']}")
        print(f"    Voices used:")
        for voice, count in stats['voices'].most_common():
            percentage = (count / stats['count']) * 100
            status = "✓" if voice == voice_mapping.get(speaker) else "✗"
            print(f"      {status} {voice}: {count} chunks ({percentage:.1f}%)")

    # Print overall voice usage
    print(f"\n🎙️  OVERALL VOICE USAGE:")
    for voice, count in voice_usage.most_common():
        percentage = (count / total_chunks) * 100
        print(f"  {voice}: {count} chunks ({percentage:.1f}%)")

    # Print issues
    if mismatches:
        print(f"\n❌ VOICE MISMATCHES ({len(mismatches)}):")
        for mismatch in sorted(mismatches, key=lambda x: x['chunk_id']):
            print(f"  Chunk {mismatch['chunk_id']:3d} ({mismatch['speaker']:6s}): "
                  f"expected {mismatch['expected']}, got {mismatch['actual']}")

    if unknown_voices:
        print(f"\n⚠️  UNKNOWN VOICES ({len(unknown_voices)}):")
        print(f"  {len(unknown_voices)} chunks with unknown voices (old cache format)")
        print(f"  Run with --force to regenerate these chunks")

    # Print verdict
    print(f"\n{'=' * 70}")
    if mismatches:
        print("❌ VERDICT: VOICE INCONSISTENCIES DETECTED")
        print("   ACTION REQUIRED: Regenerate episode with --force")
    elif unknown_voices:
        print("⚠️  VERDICT: SOME VOICES UNKNOWN (old cache)")
        print("   RECOMMENDED: Regenerate episode with --force")
    else:
        print("✅ VERDICT: ALL VOICES CONSISTENT")
    print(f"{'=' * 70}\n")


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate voice consistency reports for podcast episodes"
    )

    parser.add_argument(
        "episode_id",
        type=str,
        nargs="?",
        help="Episode identifier (e.g., '00002-cloud-providers-episode')"
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate reports for all episodes"
    )

    args = parser.parse_args()

    if args.all:
        # Load config
        config = load_config(args.config)
        cache_manager = CacheManager(
            cache_dir=config["paths"]["cache_dir"],
            manifest_file=config["paths"]["manifest_file"]
        )

        episodes = cache_manager.manifest.get("episodes", {}).keys()
        if not episodes:
            print("No episodes found in cache")
            sys.exit(0)

        for episode_id in sorted(episodes):
            generate_episode_report(episode_id, args.config)

    elif args.episode_id:
        generate_episode_report(args.episode_id, args.config)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
