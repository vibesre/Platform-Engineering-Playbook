#!/usr/bin/env python3
"""
Validate audio chunks before stitching to detect silent/blank audio.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import List, Tuple, Dict

def get_chunk_duration(file_path: Path) -> float:
    """Get exact duration of audio chunk using ffprobe."""
    try:
        cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', str(file_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return float(data.get('format', {}).get('duration', 0))
        return 0
    except Exception as e:
        print(f"Error getting duration for {file_path}: {e}")
        return 0

def detect_silence_in_chunk(file_path: Path, noise_threshold: str = "-50dB", duration_threshold: float = 1.0) -> List[Tuple[float, float]]:
    """
    Detect silent sections in an audio chunk.

    Args:
        file_path: Path to audio file
        noise_threshold: Audio level below which is considered silence
        duration_threshold: Minimum duration of silence to detect (seconds)

    Returns:
        List of (start_time, end_time) tuples for silent sections
    """
    try:
        cmd = [
            'ffmpeg', '-i', str(file_path),
            '-af', f'silencedetect=noise={noise_threshold}:d={duration_threshold}',
            '-f', 'null', '-'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        # Parse silence detection from stderr
        silence_sections = []
        silence_start = None

        for line in result.stderr.split('\n'):
            if 'silence_start' in line:
                try:
                    time = float(line.split('silence_start: ')[1].split()[0])
                    silence_start = time
                except:
                    pass
            elif 'silence_end' in line and silence_start is not None:
                try:
                    time = float(line.split('silence_end: ')[1].split()[0].replace('|', ''))
                    silence_sections.append((silence_start, time))
                    silence_start = None
                except:
                    pass

        return silence_sections
    except Exception as e:
        print(f"Error detecting silence in {file_path}: {e}")
        return []

def is_chunk_mostly_silent(file_path: Path, silent_threshold: float = 0.8) -> Tuple[bool, Dict]:
    """
    Check if a chunk is mostly silent (indicating a placeholder/failed TTS).

    Args:
        file_path: Path to audio chunk
        silent_threshold: Fraction of audio that must be silent to flag as problematic (0.0-1.0)

    Returns:
        (is_silent, info_dict) where info_dict contains duration and silence details
    """
    duration = get_chunk_duration(file_path)

    if duration == 0:
        return True, {"duration": 0, "error": "Zero duration or unreadable file"}

    silence_sections = detect_silence_in_chunk(file_path, noise_threshold="-50dB", duration_threshold=1.0)

    total_silence = sum(end - start for start, end in silence_sections)
    silence_ratio = total_silence / duration if duration > 0 else 0

    info = {
        "duration": duration,
        "total_silence": total_silence,
        "silence_ratio": silence_ratio,
        "silence_sections": len(silence_sections),
        "is_problematic": silence_ratio >= silent_threshold
    }

    return silence_ratio >= silent_threshold, info

def validate_chunks(chunk_paths: List[Path], verbose: bool = False) -> Dict:
    """
    Validate a list of audio chunks for quality issues.

    Args:
        chunk_paths: List of paths to audio chunks
        verbose: Print detailed info for each chunk

    Returns:
        Dict with validation results
    """
    problematic_chunks = []
    valid_chunks = []

    print(f"\n🔍 Validating {len(chunk_paths)} audio chunks...")

    for i, chunk_path in enumerate(chunk_paths):
        if not chunk_path.exists():
            problematic_chunks.append({
                "index": i,
                "path": str(chunk_path),
                "error": "File does not exist"
            })
            print(f"  ❌ Chunk {i}: File not found - {chunk_path.name}")
            continue

        is_silent, info = is_chunk_mostly_silent(chunk_path)

        if is_silent:
            problematic_chunks.append({
                "index": i,
                "path": str(chunk_path),
                "name": chunk_path.name,
                **info
            })
            print(f"  ⚠️  Chunk {i}: MOSTLY SILENT - {info['duration']:.1f}s total, "
                  f"{info['total_silence']:.1f}s silent ({info['silence_ratio']*100:.0f}%)")
        else:
            valid_chunks.append(i)
            if verbose:
                print(f"  ✓ Chunk {i}: OK - {info['duration']:.1f}s, {info['silence_ratio']*100:.0f}% silent")

    results = {
        "total_chunks": len(chunk_paths),
        "valid_chunks": len(valid_chunks),
        "problematic_chunks": len(problematic_chunks),
        "problems": problematic_chunks,
        "validation_passed": len(problematic_chunks) == 0
    }

    print(f"\n📊 Validation Results:")
    print(f"  Valid chunks: {results['valid_chunks']}/{results['total_chunks']}")
    print(f"  Problematic chunks: {results['problematic_chunks']}")

    if results['problematic_chunks'] > 0:
        print(f"\n⚠️  WARNING: Found {results['problematic_chunks']} problematic chunks that need regeneration!")
        print(f"  These chunks are likely placeholder audio from TTS failures.")

    return results

def main():
    """Test the validation on a specific episode."""
    if len(sys.argv) < 2:
        print("Usage: python validate_chunks.py <episode_id>")
        print("Example: python validate_chunks.py 00002-cloud-providers-episode")
        sys.exit(1)

    episode_id = sys.argv[1]
    chunks_dir = Path(__file__).parent.parent / "cache" / "chunks" / episode_id

    if not chunks_dir.exists():
        print(f"Error: Episode directory not found: {chunks_dir}")
        sys.exit(1)

    chunk_paths = sorted(chunks_dir.glob("chunk_*.mp3"))

    if not chunk_paths:
        print(f"Error: No chunks found in {chunks_dir}")
        sys.exit(1)

    results = validate_chunks(chunk_paths, verbose=True)

    if not results['validation_passed']:
        sys.exit(1)

if __name__ == "__main__":
    main()
