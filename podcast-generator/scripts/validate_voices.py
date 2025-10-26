#!/usr/bin/env python3
"""
Voice consistency validation tool.
Checks that all cached chunks in an episode use the expected voices.
"""

import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent))

from cache_manager import CacheManager


def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def normalize_speaker_name(speaker: str) -> str:
    """Normalize speaker name (same logic as cloud_tts_generator.py)."""
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


def validate_episode(episode_id: str, config_path: str = "config.yaml") -> Dict:
    """
    Validate voice consistency for an episode.

    Args:
        episode_id: Episode identifier
        config_path: Path to config file

    Returns:
        Dict with validation results
    """
    print(f"\n🔍 Validating voice consistency for episode: {episode_id}")

    # Load config
    config = load_config(config_path)

    # Get voice mapping
    voice_mapping = get_voice_mapping(config)
    print(f"Expected voice mapping: {voice_mapping}")

    # Initialize cache manager
    cache_manager = CacheManager(
        cache_dir=config["paths"]["cache_dir"],
        manifest_file=config["paths"]["manifest_file"]
    )

    # Validate
    result = cache_manager.validate_voice_consistency(episode_id, voice_mapping)

    print(f"\n📊 Validation Results:")
    print(f"  Total chunks: {result['total_chunks']}")
    print(f"  Mismatches: {len(result['mismatches'])}")
    print(f"  Unknown voices: {len(result['unknown_voices'])}")

    if result['mismatches']:
        print(f"\n❌ VOICE MISMATCHES DETECTED:")
        for mismatch in result['mismatches']:
            print(f"  Chunk {mismatch['chunk_id']} ({mismatch['speaker']}):")
            print(f"    Expected: {mismatch['expected']}")
            print(f"    Actual: {mismatch['actual']}")
            print(f"    Hash: {mismatch['hash']}")

    if result['unknown_voices']:
        print(f"\n⚠️  CHUNKS WITH UNKNOWN VOICES (old cache):")
        for unknown in result['unknown_voices']:
            print(f"  Chunk {unknown['chunk_id']} ({unknown['speaker']}): {unknown['hash']}")

    if result['is_valid'] and not result['unknown_voices']:
        print(f"\n✅ Voice consistency: PASS")
        return result
    elif result['is_valid'] and result['unknown_voices']:
        print(f"\n⚠️  Voice consistency: PASS (with warnings)")
        print(f"   Consider regenerating chunks with unknown voices")
        return result
    else:
        print(f"\n❌ Voice consistency: FAIL")
        print(f"   You must regenerate the episode with --force")
        return result


def main():
    """Command-line interface for voice validation."""
    parser = argparse.ArgumentParser(
        description="Validate voice consistency in podcast episodes"
    )

    parser.add_argument(
        "episode_id",
        type=str,
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
        help="Validate all episodes in cache"
    )

    args = parser.parse_args()

    if args.all:
        # Load config
        config = load_config(args.config)
        cache_manager = CacheManager(
            cache_dir=config["paths"]["cache_dir"],
            manifest_file=config["paths"]["manifest_file"]
        )

        print("\n🔍 Validating all episodes...")

        episodes = cache_manager.manifest.get("episodes", {}).keys()
        if not episodes:
            print("No episodes found in cache")
            sys.exit(0)

        all_valid = True
        for episode_id in episodes:
            result = validate_episode(episode_id, args.config)
            if not result['is_valid']:
                all_valid = False
            print("\n" + "=" * 60)

        if all_valid:
            print("\n✅ All episodes have consistent voices")
            sys.exit(0)
        else:
            print("\n❌ Some episodes have voice inconsistencies")
            sys.exit(1)
    else:
        result = validate_episode(args.episode_id, args.config)
        sys.exit(0 if result['is_valid'] else 1)


if __name__ == "__main__":
    main()
