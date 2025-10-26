#!/usr/bin/env python3
"""
Generate video versions of podcast episodes by overlaying audio on a looping background video.

Usage:
    python3 scripts/generate_video.py path/to/episode.mp3
    python3 scripts/generate_video.py path/to/episode.mp3 --output custom_output.mp4
    python3 scripts/generate_video.py --all  # Process all MP3s in output_latest/
"""

import argparse
import subprocess
import sys
from pathlib import Path


def get_audio_duration(audio_path):
    """Get duration of audio file in seconds using ffprobe."""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(audio_path)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error getting audio duration: {e}", file=sys.stderr)
        sys.exit(1)


def get_video_duration(video_path):
    """Get duration of video file in seconds using ffprobe."""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(video_path)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error getting video duration: {e}", file=sys.stderr)
        sys.exit(1)


def generate_video(audio_path, background_video, output_path):
    """
    Generate video by overlaying audio on looping background video.

    Args:
        audio_path: Path to MP3 audio file
        background_video: Path to background MP4 video
        output_path: Path for output MP4 video
    """
    audio_path = Path(audio_path)
    background_video = Path(background_video)
    output_path = Path(output_path)

    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    if not background_video.exists():
        print(f"Error: Background video not found: {background_video}", file=sys.stderr)
        sys.exit(1)

    # Get durations
    audio_duration = get_audio_duration(audio_path)
    video_duration = get_video_duration(background_video)

    # Calculate how many times to loop the video
    loop_count = int(audio_duration / video_duration) + 1

    print(f"Audio duration: {audio_duration:.2f}s")
    print(f"Video duration: {video_duration:.2f}s")
    print(f"Looping video {loop_count} times")
    print(f"Generating video: {output_path}")

    # FFmpeg command to:
    # 1. Loop the video
    # 2. Remove original video audio
    # 3. Add podcast audio
    # 4. Set duration to match audio
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output file
        '-stream_loop', str(loop_count),  # Loop video
        '-i', str(background_video),  # Input video
        '-i', str(audio_path),  # Input audio
        '-map', '0:v',  # Use video from first input
        '-map', '1:a',  # Use audio from second input
        '-c:v', 'libx264',  # Video codec
        '-preset', 'medium',  # Encoding speed/quality balance
        '-crf', '23',  # Quality (lower = better, 23 is default)
        '-c:a', 'aac',  # Audio codec
        '-b:a', '192k',  # Audio bitrate
        '-shortest',  # End when shortest stream ends (audio)
        '-movflags', '+faststart',  # Enable streaming
        str(output_path)
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Video generated successfully: {output_path}")

        # Get output file size
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"   File size: {size_mb:.2f} MB")

    except subprocess.CalledProcessError as e:
        print(f"Error generating video: {e}", file=sys.stderr)
        sys.exit(1)


def process_all_mp3s(output_dir, background_video):
    """Process all MP3 files in output_latest/ directory."""
    output_dir = Path(output_dir)
    mp3_files = sorted(output_dir.glob('*.mp3'))

    if not mp3_files:
        print(f"No MP3 files found in {output_dir}")
        return

    print(f"Found {len(mp3_files)} MP3 files to process\n")

    for i, mp3_file in enumerate(mp3_files, 1):
        print(f"\n[{i}/{len(mp3_files)}] Processing: {mp3_file.name}")
        print("=" * 60)

        # Generate output filename (replace .mp3 with .mp4)
        output_file = mp3_file.with_suffix('.mp4')

        # Skip if video already exists
        if output_file.exists():
            print(f"⏭️  Video already exists: {output_file.name}")
            continue

        generate_video(mp3_file, background_video, output_file)

    print("\n" + "=" * 60)
    print("✅ All videos generated!")


def main():
    parser = argparse.ArgumentParser(
        description='Generate video versions of podcast episodes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate video for a single episode
  python3 scripts/generate_video.py output_latest/00001-episode.mp3

  # Generate video with custom output name
  python3 scripts/generate_video.py output_latest/00001-episode.mp3 --output custom.mp4

  # Generate videos for all episodes
  python3 scripts/generate_video.py --all

  # Generate videos for all episodes in specific directory
  python3 scripts/generate_video.py --all --dir output_history/2024-10-19
        """
    )

    parser.add_argument(
        'audio_file',
        nargs='?',
        help='Path to MP3 audio file'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output video file path (default: same as input with .mp4 extension)'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Process all MP3 files in output directory'
    )

    parser.add_argument(
        '--dir',
        default='output_latest',
        help='Directory containing MP3 files (default: output_latest)'
    )

    parser.add_argument(
        '--background',
        default='assets/background.mp4',
        help='Background video file (default: assets/background.mp4)'
    )

    args = parser.parse_args()

    # Get the podcast-generator root directory
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    background_video = root_dir / args.background

    if args.all:
        # Process all MP3s in directory
        output_dir = root_dir / args.dir
        process_all_mp3s(output_dir, background_video)
    else:
        # Process single file
        if not args.audio_file:
            parser.error("Either provide an audio file or use --all flag")

        audio_path = Path(args.audio_file)

        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = audio_path.with_suffix('.mp4')

        generate_video(audio_path, background_video, output_path)


if __name__ == '__main__':
    main()
