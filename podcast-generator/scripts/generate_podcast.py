#!/usr/bin/env python3
"""
Main podcast generation orchestrator.
Coordinates chunking, TTS generation, caching, and audio stitching.
"""

import os
import sys
import yaml
import argparse
import re
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent))

from chunker import PodcastChunker, Chunk
from cache_manager import CacheManager
from tts_generator import TTSGenerator
from audio_stitcher import AudioStitcher
from log_utils import (
    log_generation_start,
    log_chunk_tts,
    log_generation_complete,
    log_error,
    log_warning
)
from validate_chunks import validate_chunks


class PodcastGenerator:
    """Main orchestrator for podcast generation."""
    
    def __init__(self, config_path: str = "config.yaml"):
        # Load environment variables from .env file
        load_dotenv()
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.chunker = PodcastChunker(
            min_words=self.config["chunking"]["min_words"],
            max_words=self.config["chunking"]["max_words"]
        )
        
        self.cache_manager = CacheManager(
            cache_dir=self.config["paths"]["cache_dir"],
            manifest_file=self.config["paths"]["manifest_file"]
        )
        
        self.tts_generator = TTSGenerator(config=self.config)
        
        self.audio_stitcher = AudioStitcher(
            crossfade_ms=self.config["audio"]["chunk_overlap_ms"]
        )
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def generate_podcast(self, script_path: Path, episode_id: Optional[str] = None,
                        force_regenerate: bool = False) -> Dict:
        """
        Generate a podcast from a raw script file.

        Args:
            script_path: Path to the podcast script (txt file in "Speaker 1: text" format)
            episode_id: Unique identifier for the episode
            force_regenerate: Force regeneration of all chunks

        Returns:
            Dict with generation results
        """
        print(f"\n🎙️  Generating podcast from: {script_path}")

        # Track generation start time
        generation_start_time = time.time()

        # Generate episode ID if not provided
        if not episode_id:
            episode_id = script_path.stem

        # Log generation start
        log_generation_start(episode_id, str(script_path), force_regenerate)

        # Read raw script (already in "Speaker 1: text" format)
        with open(script_path, 'r') as f:
            script_text = f.read()

        # Step 1: Chunk the script using dialogue chunker
        print("\n📝 Chunking script...")

        from dialogue_chunker import DialogueChunker, DialogueChunk
        dialogue_chunker = DialogueChunker(
            target_words=self.config["chunking"].get("target_words", 100),
            max_words=self.config["chunking"]["max_words"]
        )
        dialogue_chunks = dialogue_chunker.chunk_script(script_text)

        # Convert to regular chunks for compatibility
        chunks = []
        for dc in dialogue_chunks:
            from chunker import Chunk
            chunk = Chunk(
                id=dc.id,
                speaker=dc.primary_speaker,
                text=dc.get_text(),
                hash=dc.hash,
                word_count=dc.word_count
            )
            chunks.append(chunk)

        print(f"Created {len(chunks)} chunks")

        # Validate chunk ordering (safety check)
        for i, chunk in enumerate(chunks):
            if chunk.id != i:
                raise ValueError(
                    f"Chunk ordering validation failed: chunk at index {i} has id {chunk.id}. "
                    "This indicates a bug in the chunking logic."
                )

        # Step 2: Generate audio for each chunk
        print("\n🎵 Generating audio chunks...")
        chunk_paths = []
        regenerated_count = 0
        cached_count = 0
        failed_count = 0
        total_characters = 0
        total_cost = 0.0

        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}: {chunk.speaker} ({chunk.word_count} words)")

            # Get expected voice for this speaker
            expected_voice = self.tts_generator.voice_mapping.get(chunk.speaker, "unknown")

            # Check cache and validate voice consistency
            is_cached = self.cache_manager.is_chunk_cached(episode_id, chunk.hash)
            voice_valid = self.cache_manager.is_chunk_voice_valid(episode_id, chunk.hash, expected_voice)

            if not force_regenerate and is_cached and voice_valid:
                print(f"  ✓ Using cached version (voice: {expected_voice})")
                cached_count += 1

                # Log cached chunk
                log_chunk_tts(
                    chunk_id=i + 1,
                    speaker=chunk.speaker,
                    status="cached",
                    cached=True
                )
            else:
                if is_cached and not voice_valid:
                    print(f"  ⚠️  Cache invalid: voice changed (regenerating)")

                # Generate audio
                output_path = self.cache_manager.get_chunk_path(episode_id, chunk.hash)

                try:
                    metadata = self.tts_generator.generate_with_retry(
                        text=chunk.text,
                        speaker=chunk.speaker,
                        output_path=output_path,
                        max_retries=self.config["processing"]["max_retries"]
                    )

                    # Register in cache with voice information
                    chunk_data = chunk.to_dict()
                    chunk_data["duration"] = metadata["duration"]
                    chunk_data["voice"] = metadata.get("voice", expected_voice)
                    self.cache_manager.register_chunk(episode_id, chunk_data)

                    regenerated_count += 1
                    print(f"  ✓ Generated ({metadata['duration']:.1f}s, voice: {metadata.get('voice', expected_voice)})")

                    # Track usage metrics
                    char_count = metadata.get("character_count", 0)
                    cost = metadata.get("estimated_cost_usd", 0.0)
                    total_characters += char_count
                    total_cost += cost

                    # Log successful chunk generation
                    log_chunk_tts(
                        chunk_id=i + 1,
                        speaker=chunk.speaker,
                        status="success",
                        character_count=char_count,
                        word_count=chunk.word_count,
                        voice=metadata.get("voice", expected_voice),
                        duration_seconds=metadata["duration"],
                        generation_time_seconds=metadata.get("generation_time", 0),
                        estimated_cost_usd=cost,
                        cached=False,
                        attempt=metadata.get("retry_attempt", 1)
                    )

                except Exception as e:
                    failed_count += 1
                    print(f"  ✗ Failed to generate: {e}")

                    # Log failed chunk
                    log_chunk_tts(
                        chunk_id=i + 1,
                        speaker=chunk.speaker,
                        status="failed",
                        error=str(e)
                    )

                    log_error(episode_id, "chunk_generation_failed", str(e), {
                        "chunk_id": i + 1,
                        "speaker": chunk.speaker,
                        "word_count": chunk.word_count
                    })

                    raise

            chunk_paths.append(self.cache_manager.get_chunk_path(episode_id, chunk.hash))

        # Print cache reuse summary
        print(f"\n📊 Cache Summary: Regenerated {regenerated_count}/{len(chunks)} chunks, " +
              f"reused {cached_count}/{len(chunks)} from cache")

        # Print cost summary
        if regenerated_count > 0:
            # Calculate estimated total episode cost (including cached chunks)
            # Estimate cached chunk costs based on average character count
            avg_chars_per_chunk = total_characters / regenerated_count if regenerated_count > 0 else 200
            estimated_cached_chars = int(avg_chars_per_chunk * cached_count)
            estimated_cached_cost = estimated_cached_chars * 0.000015  # Google TTS rate
            total_episode_cost = total_cost + estimated_cached_cost

            cost_per_minute = total_cost / (sum([c.word_count for c in chunks]) / 150) if chunks else 0

            print(f"\n💰 TTS API Usage Summary:")
            print(f"  Characters (this run): {total_characters:,}")
            print(f"  Generated chunks: {regenerated_count}")
            print(f"  Cached chunks: {cached_count}")
            print(f"  Cost (this run): ${total_cost:.5f}")
            print(f"  Estimated total episode cost: ${total_episode_cost:.5f}")
            print(f"  Cost per minute: ${cost_per_minute:.5f}/min")
        elif cached_count > 0:
            # All chunks cached - estimate total episode cost
            estimated_total_chars = sum([len(c.text) for c in chunks])
            estimated_total_cost = estimated_total_chars * 0.000015  # Google TTS rate

            print(f"\n💰 TTS API Usage Summary:")
            print(f"  All chunks loaded from cache - no generation cost")
            print(f"  Cached chunks: {cached_count}")
            print(f"  Estimated total episode cost: ${estimated_total_cost:.5f}")

        # Step 2.5: Validate chunks for silence/placeholder audio
        print("\n🔍 Validating generated chunks...")
        validation_results = validate_chunks(chunk_paths, verbose=False)

        if not validation_results['validation_passed']:
            problematic_count = validation_results['problematic_chunks']
            print(f"\n❌ FATAL: {problematic_count} chunks are mostly silent (placeholder audio)")
            print(f"   This indicates TTS generation failures.")
            print(f"\n   Problematic chunks:")
            for problem in validation_results['problems'][:10]:  # Show first 10
                silence_pct = problem.get('silence_ratio', 0) * 100
                error_msg = problem.get('error', f"{silence_pct:.0f}% silent")
                print(f"     - Chunk {problem['index']}: {error_msg}")

            log_error(episode_id, "validation_failed", f"{problematic_count} chunks are placeholder audio", {
                "problematic_chunks": problematic_count,
                "total_chunks": validation_results['total_chunks']
            })

            raise RuntimeError(
                f"Episode generation failed: {problematic_count}/{validation_results['total_chunks']} "
                f"chunks are placeholder audio.\n"
                f"This indicates TTS generation failures - check the logs for details."
            )

        print(f"  ✓ All {validation_results['valid_chunks']} chunks validated successfully")

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

        # Step 3: Clean orphaned chunks
        active_hashes = [chunk.hash for chunk in chunks]
        self.cache_manager.clean_orphaned_chunks(episode_id, active_hashes)
        
        # Step 4: Set up output directories
        output_base_dir = Path(self.config["paths"]["output_dir"]).parent
        output_latest_dir = output_base_dir / "output_latest"
        output_history_dir = output_base_dir / "output_history"

        # Create directories if they don't exist
        output_latest_dir.mkdir(exist_ok=True)
        output_history_dir.mkdir(exist_ok=True)

        # Check if episode already exists in output_latest
        latest_episode_path = output_latest_dir / f"{episode_id}.mp3"
        if latest_episode_path.exists():
            # Move existing version to history with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            history_filename = f"{episode_id}_{timestamp}.mp3"
            history_path = output_history_dir / history_filename
            print(f"\n📦 Moving previous version to history: {history_filename}")
            latest_episode_path.rename(history_path)

        # Step 5: Stitch chunks together
        print("\n🔗 Stitching audio chunks...")
        temp_filename = f"temp_{episode_id}.mp3"
        temp_path = output_latest_dir / temp_filename

        # Prepare metadata
        metadata = {
            "title": f"Platform Engineering Playbook - {episode_id}",
            "artist": "Platform Engineering Playbook",
            "album": "Platform Engineering Playbook Podcast",
            "date": datetime.now().strftime("%Y"),
            "comment": "Generated using Google AI Studio TTS"
        }

        stitch_result = self.audio_stitcher.stitch_chunks(
            chunk_paths=chunk_paths,
            output_path=temp_path,
            metadata=metadata
        )

        # Step 6: Add intro and outro
        print("\n🎵 Adding intro and outro...")
        # Get the project root directory (parent of podcast-generator)
        script_dir = Path(__file__).parent.parent
        intro_path = script_dir / "tros" / "intro.mp3"
        outro_path = script_dir / "tros" / "outro.mp3"

        # Check if intro/outro files exist
        if not intro_path.exists():
            print(f"  ⚠️  Warning: Intro file not found at {intro_path}")
            intro_path = None
        if not outro_path.exists():
            print(f"  ⚠️  Warning: Outro file not found at {outro_path}")
            outro_path = None

        output_path = latest_episode_path  # Use clean filename in output_latest

        if intro_path or outro_path:
            with_music_path = self.audio_stitcher.add_intro_outro(
                main_audio=temp_path,
                intro_path=intro_path,
                outro_path=outro_path,
                output_path=output_path
            )
            # Clean up temp file
            temp_path.unlink()
            print(f"  ✓ Added intro and outro")
        else:
            # No intro/outro, just rename temp file
            temp_path.rename(output_path)
            print(f"  ⚠️  Skipping intro/outro (files not found)")

        # Step 7: Normalize audio
        print("\n🎚️  Normalizing audio levels...")
        normalized_path = self.audio_stitcher.normalize_audio(output_path)

        # Replace original with normalized version
        if normalized_path != output_path:
            output_path.unlink()
            normalized_path.rename(output_path)

        # Step 7.5: Validate voice consistency
        print("\n🔍 Validating voice consistency...")
        voice_validation = self.cache_manager.validate_voice_consistency(
            episode_id,
            self.tts_generator.voice_mapping
        )

        if voice_validation['mismatches']:
            print(f"  ⚠️  WARNING: {len(voice_validation['mismatches'])} voice mismatches detected!")
            for mismatch in voice_validation['mismatches']:
                print(f"    Chunk {mismatch['chunk_id']} ({mismatch['speaker']}): "
                      f"expected {mismatch['expected']}, got {mismatch['actual']}")
        elif voice_validation['unknown_voices']:
            print(f"  ⚠️  {len(voice_validation['unknown_voices'])} chunks with unknown voices (old cache)")
        else:
            print(f"  ✓ All voices consistent")

        # Step 8: Generate metadata .txt file
        print("\n📝 Generating episode metadata...")
        metadata_path = output_latest_dir / f"{episode_id}.txt"
        self._generate_metadata_file(
            episode_id=episode_id,
            script_path=script_path,
            output_path=metadata_path,
            duration_minutes=None  # Will be calculated below
        )

        # Get final statistics
        total_duration = sum(
            self.cache_manager.get_episode_manifest(episode_id)["chunks"][chunk.hash].get("duration", 0)
            for chunk in chunks
        )
        
        cache_stats = self.cache_manager.get_cache_stats(episode_id)
        
        result = {
            "episode_id": episode_id,
            "output_file": str(output_path),
            "total_chunks": len(chunks),
            "regenerated_chunks": regenerated_count,
            "cached_chunks": cached_count,
            "total_duration_minutes": round(total_duration / 60, 1),
            "output_size_mb": stitch_result["output_size_mb"],
            "cache_stats": cache_stats
        }

        # Step 9: Generate video (MP4) from audio
        print("\n🎬 Generating video...")
        video_path = output_path.with_suffix('.mp4')
        try:
            import subprocess
            subprocess.run([
                sys.executable,
                str(Path(__file__).parent / "generate_video.py"),
                str(output_path)
            ], check=True, capture_output=False)

            if video_path.exists():
                video_size_mb = round(video_path.stat().st_size / 1024 / 1024, 2)
                print(f"  ✓ Video generated: {video_path.name} ({video_size_mb} MB)")
                result["video_file"] = str(video_path)
                result["video_size_mb"] = video_size_mb
            else:
                print(f"  ⚠️  Video file not found after generation")
        except Exception as e:
            print(f"  ⚠️  Video generation failed: {e}")
            print(f"     You can manually generate with: python3 scripts/generate_video.py {output_path}")

        # Calculate total generation time
        total_generation_time = time.time() - generation_start_time

        # Log generation complete
        log_generation_complete(
            episode_id=episode_id,
            total_chunks=len(chunks),
            successful_chunks=len(chunks) - failed_count,
            failed_chunks=failed_count,
            cached_chunks=cached_count,
            total_characters=total_characters,
            total_duration_seconds=total_duration,
            estimated_total_cost_usd=total_cost,
            generation_time_seconds=total_generation_time,
            validation_passed=validation_results.get('validation_passed', True),
            output_file=str(output_path)
        )

        print("\n✅ Podcast generation complete!")
        print(f"📁 Audio: {output_path}")
        if "video_file" in result:
            print(f"🎬 Video: {video_path}")
        print(f"⏱️  Duration: {result['total_duration_minutes']} minutes")
        print(f"💾 Audio size: {result['output_size_mb']} MB")
        if "video_size_mb" in result:
            print(f"💾 Video size: {result['video_size_mb']} MB")
        print(f"🔄 Chunks: {regenerated_count} generated, {cached_count} cached")
        print(f"⏱️  Generation time: {total_generation_time / 60:.1f} minutes")

        return result

    def _generate_metadata_file(self, episode_id: str, script_path: Path,
                                output_path: Path, duration_minutes: Optional[float] = None):
        """Generate episode metadata .txt file for distribution."""
        import subprocess

        # Read script to extract title and content
        with open(script_path, 'r') as f:
            script_content = f.read()

        # Extract episode title from episode_id
        # Convert: 00001-ai-platform-engineering-episode → AI Platform Engineering Episode
        title_parts = episode_id.split('-')[1:]  # Remove number prefix
        title = ' '.join(word.capitalize() for word in title_parts)

        # Try to find corresponding episode page for better metadata
        docs_dir = script_path.parent.parent.parent / "docs" / "podcasts"
        episode_page_path = docs_dir / f"{'-'.join(title_parts)}.md"

        # Generate episode slug for URL (include episode number)
        episode_slug = episode_id

        # Get actual MP3 duration using ffprobe
        mp3_path = output_path.parent / f"{episode_id}.mp3"
        duration_str = "00:00:00"

        if mp3_path.exists():
            try:
                result = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_path)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    total_seconds = float(result.stdout.strip())
                    hours = int(total_seconds // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    seconds = int(total_seconds % 60)
                    duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            except Exception as e:
                print(f"  ⚠️  Could not get MP3 duration: {e}")
                # Fallback to estimated duration from chunks
                try:
                    total_duration = sum(
                        self.cache_manager.get_episode_manifest(episode_id)["chunks"][hash].get("duration", 0)
                        for hash in self.cache_manager.get_episode_manifest(episode_id)["chunks"]
                    )
                    hours = int(total_duration // 3600)
                    minutes = int((total_duration % 3600) // 60)
                    seconds = int(total_duration % 60)
                    duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                except:
                    pass

        # Generate metadata content
        metadata = f"""Title: {title}

Description:
[Episode description - edit this to add a compelling hook and explain what listeners will learn]

🔗 Full episode page: https://platformengineeringplaybook.com/podcasts/{episode_slug}

📝 See a mistake or have insights to add? This podcast is community-driven - open a PR on GitHub!

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

        # Write metadata file
        with open(output_path, 'w') as f:
            f.write(metadata)

        print(f"  ✓ Created metadata file: {output_path.name} (Duration: {duration_str})")

    def batch_generate(self, script_directory: Path, pattern: str = "*.md",
                      force_regenerate: bool = False) -> List[Dict]:
        """Generate podcasts for multiple scripts."""
        results = []
        
        scripts = list(script_directory.glob(pattern))
        print(f"Found {len(scripts)} scripts to process")
        
        for script_path in scripts:
            try:
                result = self.generate_podcast(
                    script_path=script_path,
                    force_regenerate=force_regenerate
                )
                results.append(result)
            except Exception as e:
                print(f"Failed to generate {script_path}: {e}")
                results.append({
                    "episode_id": script_path.stem,
                    "error": str(e)
                })
        
        return results
    


def main():
    """Command-line interface for podcast generation."""
    parser = argparse.ArgumentParser(
        description="Generate podcasts from text scripts using Google AI Studio"
    )
    
    parser.add_argument(
        "script",
        type=Path,
        help="Path to the podcast script (txt file in 'Speaker 1: text' format)"
    )

    parser.add_argument(
        "--episode-id",
        type=str,
        help="Unique episode identifier (defaults to script filename)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force regeneration of all chunks (ignore cache)"
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file"
    )

    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all txt files in the directory"
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    if not os.getenv("GOOGLE_AI_API_KEY"):
        print("Error: GOOGLE_AI_API_KEY not found")
        print("\nOptions to set your Google AI Studio API key:")
        print("1. Create a .env file with: GOOGLE_AI_API_KEY=your-key-here")
        print("2. Set environment variable: export GOOGLE_AI_API_KEY='your-key-here'")
        print("3. Get your key from: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    # Initialize generator
    generator = PodcastGenerator(config_path=args.config)
    
    # Generate podcast(s)
    if args.batch:
        if args.script.is_dir():
            results = generator.batch_generate(
                script_directory=args.script,
                force_regenerate=args.force
            )
            
            # Print summary
            print("\n📊 Batch Generation Summary:")
            success_count = sum(1 for r in results if "error" not in r)
            print(f"✓ Success: {success_count}/{len(results)}")
            
            for result in results:
                if "error" in result:
                    print(f"✗ {result['episode_id']}: {result['error']}")
        else:
            print("Error: --batch requires a directory path")
            sys.exit(1)
    else:
        if not args.script.exists():
            print(f"Error: Script file not found: {args.script}")
            sys.exit(1)
        
        generator.generate_podcast(
            script_path=args.script,
            episode_id=args.episode_id,
            force_regenerate=args.force
        )


if __name__ == "__main__":
    main()