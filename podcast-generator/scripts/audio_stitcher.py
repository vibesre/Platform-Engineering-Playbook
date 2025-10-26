#!/usr/bin/env python3
"""
Audio stitching functionality for combining chunks into final podcast.
Uses ffmpeg for audio processing.
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class AudioStitcher:
    """Handles combining audio chunks into a final podcast file."""
    
    def __init__(self, crossfade_ms: int = 50):
        self.crossfade_ms = crossfade_ms
        self._check_ffmpeg()
    
    def _check_ffmpeg(self):
        """Check if ffmpeg is available."""
        try:
            subprocess.run(["ffmpeg", "-version"], 
                         capture_output=True, 
                         check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("ffmpeg not found. Please install ffmpeg.")
    
    def stitch_chunks(self, chunk_paths: List[Path], output_path: Path, 
                     metadata: Optional[Dict] = None) -> Dict:
        """
        Stitch audio chunks together with crossfades.
        
        Args:
            chunk_paths: List of paths to chunk audio files
            output_path: Path for the final output file
            metadata: Optional metadata to embed in the file
            
        Returns:
            Dict with stitching results
        """
        if not chunk_paths:
            raise ValueError("No chunks provided for stitching")
        
        print(f"Stitching {len(chunk_paths)} chunks...")
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        start_time = datetime.now()
        
        if len(chunk_paths) == 1:
            # Single chunk, just copy
            self._copy_single_chunk(chunk_paths[0], output_path, metadata)
        else:
            # Multiple chunks, stitch with crossfades
            self._stitch_with_crossfades(chunk_paths, output_path, metadata)
        
        duration = (datetime.now() - start_time).total_seconds()
        
        # Get output file info
        output_size = output_path.stat().st_size if output_path.exists() else 0
        
        return {
            "chunks_processed": len(chunk_paths),
            "output_file": str(output_path),
            "output_size_mb": round(output_size / 1024 / 1024, 2),
            "processing_time": round(duration, 2)
        }
    
    def _copy_single_chunk(self, input_path: Path, output_path: Path, 
                          metadata: Optional[Dict] = None):
        """Copy a single chunk with optional metadata."""
        cmd = ["ffmpeg", "-y", "-i", str(input_path)]
        
        # Add metadata if provided
        if metadata:
            for key, value in metadata.items():
                cmd.extend(["-metadata", f"{key}={value}"])
        
        cmd.extend(["-codec", "copy", str(output_path)])
        
        subprocess.run(cmd, check=True, capture_output=True)
    
    def _stitch_with_crossfades(self, chunk_paths: List[Path], output_path: Path,
                               metadata: Optional[Dict] = None):
        """Stitch multiple chunks with crossfades between them."""
        # Create concat file
        concat_file = output_path.parent / f"{output_path.stem}_concat.txt"
        
        with open(concat_file, 'w') as f:
            for chunk_path in chunk_paths:
                f.write(f"file '{chunk_path.absolute()}'\n")
        
        # Build ffmpeg command
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c:a", "libmp3lame",
            "-b:a", "128k",
            "-ar", "44100"
        ]
        
        # Add metadata if provided
        if metadata:
            for key, value in metadata.items():
                cmd.extend(["-metadata", f"{key}={value}"])
        
        cmd.append(str(output_path))
        
        # Run ffmpeg
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg error: {e.stderr}")
            raise
        finally:
            # Clean up concat file
            if concat_file.exists():
                concat_file.unlink()
    
    def add_intro_outro(self, main_audio: Path, intro_path: Optional[Path] = None,
                       outro_path: Optional[Path] = None, output_path: Optional[Path] = None,
                       pause_before_outro: float = 0.75) -> Path:
        """
        Add intro and/or outro music to the podcast.

        Args:
            main_audio: Path to main podcast audio
            intro_path: Optional path to intro music
            outro_path: Optional path to outro music
            output_path: Optional output path
            pause_before_outro: Duration in seconds of silence before outro (default 0.75)
        """
        if not intro_path and not outro_path:
            return main_audio

        if not output_path:
            output_path = main_audio.parent / f"{main_audio.stem}_with_music{main_audio.suffix}"

        # Build complex filter for adding intro/outro
        inputs = []
        filter_complex = []

        input_index = 0
        if intro_path:
            inputs.extend(["-i", str(intro_path)])
            input_index += 1

        inputs.extend(["-i", str(main_audio)])
        main_index = input_index
        input_index += 1

        if outro_path:
            inputs.extend(["-i", str(outro_path)])
            outro_index = input_index

        # Build filter chain
        if intro_path and outro_path:
            # Crossfade intro -> main (smooth start)
            # Add silence, then concat main + silence + outro (clean finish)
            filter_complex = [
                f"[0:a][{main_index}:a]acrossfade=d=1[main];",
                f"aevalsrc=0:d={pause_before_outro}[silence];",
                f"[main][silence][{outro_index}:a]concat=n=3:v=0:a=1[out]"
            ]
            output_label = "[out]"
        elif intro_path:
            # Only intro: crossfade intro -> main
            filter_complex = [f"[0:a][{main_index}:a]acrossfade=d=1[out]"]
            output_label = "[out]"
        else:  # Only outro
            # Add silence, then concat main + silence + outro (no crossfade)
            filter_complex = [
                f"aevalsrc=0:d={pause_before_outro}[silence];",
                f"[{main_index}:a][silence][{outro_index}:a]concat=n=3:v=0:a=1[out]"
            ]
            output_label = "[out]"

        cmd = ["ffmpeg", "-y"] + inputs + [
            "-filter_complex", "".join(filter_complex),
            "-map", output_label,
            "-c:a", "libmp3lame",
            "-b:a", "128k",
            str(output_path)
        ]

        subprocess.run(cmd, check=True, capture_output=True)

        return output_path
    
    def normalize_audio(self, input_path: Path, output_path: Optional[Path] = None) -> Path:
        """Normalize audio levels using ffmpeg loudnorm filter."""
        if not output_path:
            output_path = input_path.parent / f"{input_path.stem}_normalized{input_path.suffix}"
        
        # First pass - analyze
        cmd_analyze = [
            "ffmpeg", "-i", str(input_path),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
            "-f", "null", "-"
        ]
        
        result = subprocess.run(cmd_analyze, capture_output=True, text=True, check=True)
        
        # Extract loudnorm stats from stderr (ffmpeg outputs to stderr)
        lines = result.stderr.split('\n')
        json_start = None
        for i, line in enumerate(lines):
            if line.strip() == '{':
                json_start = i
                break
        
        if json_start:
            json_lines = []
            for line in lines[json_start:]:
                json_lines.append(line)
                if line.strip() == '}':
                    break
            
            try:
                stats = json.loads('\n'.join(json_lines))
                
                # Second pass - apply normalization
                measured_I = stats.get("input_i", "-23")
                measured_TP = stats.get("input_tp", "-1")
                measured_LRA = stats.get("input_lra", "11")
                measured_thresh = stats.get("input_thresh", "-24")
                offset = stats.get("target_offset", "0")
                
                # Handle silent audio (infinite values)
                if measured_I == '-inf' or offset == 'inf':
                    print("Detected silent audio, using simple normalization")
                    return self._simple_normalize(input_path, output_path)
                
                filter_str = (f"loudnorm=I=-16:TP=-1.5:LRA=11:"
                            f"measured_I={measured_I}:"
                            f"measured_TP={measured_TP}:"
                            f"measured_LRA={measured_LRA}:"
                            f"measured_thresh={measured_thresh}:"
                            f"offset={offset}")
                
                cmd_normalize = [
                    "ffmpeg", "-y", "-i", str(input_path),
                    "-af", filter_str,
                    "-c:a", "libmp3lame",
                    "-b:a", "128k",
                    str(output_path)
                ]
                
                subprocess.run(cmd_normalize, check=True, capture_output=True)
            except json.JSONDecodeError:
                # Fallback to simple normalization
                print("Could not parse loudnorm stats, using simple normalization")
                return self._simple_normalize(input_path, output_path)
        else:
            return self._simple_normalize(input_path, output_path)
        
        return output_path
    
    def _simple_normalize(self, input_path: Path, output_path: Path) -> Path:
        """Simple volume normalization fallback."""
        cmd = [
            "ffmpeg", "-y", "-i", str(input_path),
            "-af", "volume=0.9",
            "-c:a", "libmp3lame",
            "-b:a", "128k",
            str(output_path)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path


def main():
    """Test the audio stitcher."""
    stitcher = AudioStitcher()
    
    # Create test chunks (would be actual audio files in production)
    test_chunks = [
        Path("chunk1.mp3"),
        Path("chunk2.mp3"),
        Path("chunk3.mp3")
    ]
    
    # Test with dummy paths (won't actually work without real audio files)
    print("Audio stitcher initialized successfully")
    print(f"Crossfade duration: {stitcher.crossfade_ms}ms")


if __name__ == "__main__":
    main()