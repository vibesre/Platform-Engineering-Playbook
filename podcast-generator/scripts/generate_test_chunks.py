#!/usr/bin/env python3
"""
Generate only the first N chunks for testing.
"""

import sys
import yaml
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent))

from dialogue_chunker import DialogueChunker
from cache_manager import CacheManager
from tts_generator import TTSGenerator
from audio_stitcher import AudioStitcher


def generate_test_episode(script_path: Path, num_chunks: int = 10, episode_id: str = "test-episode"):
    """Generate first N chunks only."""

    # Load config
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    print(f"\n🎙️  Generating TEST episode (first {num_chunks} chunks)")
    print(f"📁 Script: {script_path}\n")

    # Read script
    with open(script_path, 'r') as f:
        script_text = f.read()

    # Chunk the script
    print("📝 Chunking script...")
    dialogue_chunker = DialogueChunker(
        target_words=config["chunking"].get("target_words", 100),
        max_words=config["chunking"]["max_words"]
    )
    all_chunks = dialogue_chunker.chunk_script(script_text)

    # Take only first N chunks
    chunks = all_chunks[:num_chunks]
    print(f"Created {len(all_chunks)} total chunks, using first {len(chunks)} for test\n")

    # Validate chunk ordering (safety check)
    for i, chunk in enumerate(chunks):
        if chunk.id != i:
            raise ValueError(
                f"Chunk ordering validation failed: chunk at index {i} has id {chunk.id}. "
                "This indicates a bug in the chunking logic."
            )

    # Initialize components
    cache_manager = CacheManager(
        cache_dir=config["paths"]["cache_dir"],
        manifest_file=config["paths"]["manifest_file"]
    )
    tts_generator = TTSGenerator(config=config)

    # Generate audio for chunks
    print("🎵 Generating audio chunks...")
    chunk_paths = []

    for i, dc in enumerate(chunks):
        from chunker import Chunk
        chunk = Chunk(
            id=dc.id,
            speaker=dc.primary_speaker,
            text=dc.get_text(),
            hash=dc.hash,
            word_count=dc.word_count
        )

        print(f"Processing chunk {i+1}/{len(chunks)}: {chunk.speaker} ({chunk.word_count} words)")

        output_path = cache_manager.get_chunk_path(episode_id, chunk.hash)

        try:
            metadata = tts_generator.generate_with_retry(
                text=chunk.text,
                speaker=chunk.speaker,
                output_path=output_path,
                max_retries=config["processing"]["max_retries"]
            )

            # Register in cache
            chunk_data = chunk.to_dict()
            chunk_data["duration"] = metadata["duration"]
            cache_manager.register_chunk(episode_id, chunk_data)

            print(f"  ✓ Generated ({metadata['duration']:.1f}s)\n")

        except Exception as e:
            print(f"  ✗ Failed: {e}\n")
            raise

        chunk_paths.append(output_path)

    # Verify all chunk files exist before proceeding
    missing_chunks = []
    for i, path in enumerate(chunk_paths):
        if not path.exists():
            missing_chunks.append((i, path))

    if missing_chunks:
        missing_info = ", ".join(f"chunk {i} ({path.name})" for i, path in missing_chunks)
        raise FileNotFoundError(
            f"Cannot stitch podcast: {len(missing_chunks)} chunk file(s) missing: {missing_info}"
        )

    # Stitch chunks together
    print("🔗 Stitching audio chunks...")
    audio_stitcher = AudioStitcher(
        crossfade_ms=config["audio"]["chunk_overlap_ms"]
    )

    output_filename = f"{episode_id}_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    output_path = Path(config["paths"]["output_dir"]) / output_filename

    metadata = {
        "title": f"Test Episode - First {num_chunks} Chunks",
        "artist": "Platform Engineering Playbook",
        "album": "Test Episodes",
        "date": datetime.now().strftime("%Y"),
        "comment": "Test generation"
    }

    stitch_result = audio_stitcher.stitch_chunks(
        chunk_paths=chunk_paths,
        output_path=output_path,
        metadata=metadata
    )

    # Normalize audio
    print("🎚️  Normalizing audio...")
    normalized_path = audio_stitcher.normalize_audio(output_path)

    if normalized_path != output_path:
        output_path.unlink()
        normalized_path.rename(output_path)

    # Get stats
    total_duration = sum(
        cache_manager.get_episode_manifest(episode_id)["chunks"][chunk.hash].get("duration", 0)
        for chunk in chunks
    )

    print("\n✅ Test episode complete!")
    print(f"📁 Output: {output_path}")
    print(f"⏱️  Duration: {total_duration / 60:.1f} minutes")
    print(f"💾 Size: {stitch_result['output_size_mb']} MB")
    print(f"🎵 Chunks: {len(chunks)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate test episode with first N chunks")
    parser.add_argument("script", type=Path, help="Path to script file")
    parser.add_argument("--chunks", type=int, default=10, help="Number of chunks to generate (default: 10)")
    parser.add_argument("--episode-id", type=str, default="test-episode", help="Episode ID for cache")

    args = parser.parse_args()

    generate_test_episode(args.script, args.chunks, args.episode_id)
