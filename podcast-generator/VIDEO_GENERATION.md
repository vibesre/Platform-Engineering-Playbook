# Video Generation for Podcast Episodes

This document explains how to generate video versions of podcast episodes by overlaying audio on a looping background animation.

## Overview

The video generation process takes podcast audio files (MP3) and combines them with a looping background video to create video versions suitable for platforms like YouTube, social media, and website embedding.

**Key Features:**
- Automatic video looping to match audio duration
- Removes original video audio
- High-quality H.264 video encoding
- AAC audio at 192kbps
- Fast encoding with good compression
- Optimized for streaming (faststart flag)

## Prerequisites

- FFmpeg installed (for video/audio processing)
- Python 3.x
- Podcast audio files (MP3 format)
- Background video at `podcast-generator/assets/background.mp4`

## Background Video

**Location:** `podcast-generator/assets/background.mp4`

**Specifications:**
- Resolution: 1920x1080 (Full HD)
- Duration: ~7.8 seconds
- Format: MP4 (H.264)
- The video loops automatically to match the audio length

**Source:** Copied from `/Users/ericking/Documents/vibesre/logo/logo_podcast_animated_text.mp4`

## Usage

### Generate Video for Single Episode

```bash
cd podcast-generator

# Basic usage
python3 scripts/generate_video.py output_latest/00001-episode-name.mp3

# Specify custom output path
python3 scripts/generate_video.py output_latest/00001-episode-name.mp3 --output custom_output.mp4

# Use different background video
python3 scripts/generate_video.py output_latest/00001-episode-name.mp3 --background assets/custom_bg.mp4
```

### Generate Videos for All Episodes

Process all MP3 files in `output_latest/`:

```bash
cd podcast-generator
python3 scripts/generate_video.py --all
```

Process all MP3 files in a specific directory:

```bash
cd podcast-generator
python3 scripts/generate_video.py --all --dir output_history/2024-10-19
```

### Command-Line Options

```
usage: generate_video.py [-h] [--output OUTPUT] [--all] [--dir DIR] [--background BACKGROUND] [audio_file]

Generate video versions of podcast episodes

positional arguments:
  audio_file            Path to MP3 audio file

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output video file path (default: same as input with .mp4 extension)
  --all                 Process all MP3 files in output directory
  --dir DIR             Directory containing MP3 files (default: output_latest)
  --background BACKGROUND
                        Background video file (default: assets/background.mp4)
```

## Workflow Integration

### When Generating New Episodes

After generating audio for a new episode:

```bash
# 1. Generate podcast audio (as usual)
cd podcast-generator
python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00005-episode-name.txt

# 2. Generate video version
python3 scripts/generate_video.py output_latest/00005-episode-name.mp3
```

### Batch Generation for Existing Episodes

To create videos for all existing episodes:

```bash
cd podcast-generator
python3 scripts/generate_video.py --all
```

The script automatically skips episodes that already have video files.

## Output

**Location:** Same directory as input MP3 file
**Naming:** Replaces `.mp3` extension with `.mp4`
**Example:** `output_latest/00001-episode-name.mp3` → `output_latest/00001-episode-name.mp4`

### File Sizes

Typical video sizes for different episode lengths:

| Episode Length | Video Size (approx) |
|---------------|---------------------|
| 5 minutes     | ~85 MB              |
| 10 minutes    | ~170 MB             |
| 15 minutes    | ~255 MB             |
| 20 minutes    | ~340 MB             |

**Bitrate:** ~2170 kbps (video + audio combined)

## Video Specifications

**Video Track:**
- Codec: H.264 (libx264)
- Resolution: 1920x1080 (Full HD)
- Frame Rate: 30 fps
- Encoding Preset: medium (balance of speed/quality)
- CRF: 23 (constant quality, 0-51 scale, lower = better)
- Profile: High
- Pixel Format: YUV 4:2:0

**Audio Track:**
- Codec: AAC (LC)
- Bitrate: 192 kbps
- Sample Rate: 48kHz
- Channels: Stereo

**Container:**
- Format: MP4
- Flags: `+faststart` (enables streaming before full download)

## Technical Details

### How It Works

1. **Get Audio Duration:** Uses `ffprobe` to determine MP3 length
2. **Calculate Loops:** Determines how many times to loop background video
3. **Encode Video:** FFmpeg command:
   - Loops background video (`-stream_loop`)
   - Maps video from background, audio from MP3
   - Encodes to H.264/AAC
   - Sets duration to match audio length (`-shortest`)
   - Applies streaming optimization (`-movflags +faststart`)

### FFmpeg Command Structure

```bash
ffmpeg -y \
  -stream_loop <count> \            # Loop video
  -i assets/background.mp4 \        # Input: background video
  -i episode.mp3 \                  # Input: podcast audio
  -map 0:v -map 1:a \              # Map video from input 0, audio from input 1
  -c:v libx264 -preset medium \     # Video codec and encoding speed
  -crf 23 \                         # Quality level
  -c:a aac -b:a 192k \             # Audio codec and bitrate
  -shortest \                       # End when shortest stream ends (audio)
  -movflags +faststart \            # Enable streaming
  output.mp4
```

## Troubleshooting

### FFmpeg Not Found

```bash
# macOS (Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Verify installation
ffmpeg -version
```

### Background Video Missing

```bash
# Check if background video exists
ls -lh podcast-generator/assets/background.mp4

# If missing, copy from source
cp /Users/ericking/Documents/vibesre/logo/logo_podcast_animated_text.mp4 \
   podcast-generator/assets/background.mp4
```

### Large File Sizes

Video files are large due to Full HD resolution and 16-20 minute durations. Options:

1. **Accept the size:** Quality matters for YouTube/streaming
2. **Lower resolution:** Modify script to use `-vf scale=1280:720` for 720p
3. **Increase compression:** Lower CRF value (e.g., `-crf 28`)
4. **Host externally:** Upload to YouTube, embed links instead of self-hosting

### Encoding Too Slow

The script uses `-preset medium` for encoding. Options:

- **Faster encoding:** Change to `-preset fast` or `-preset veryfast` (larger files)
- **Slower encoding:** Change to `-preset slow` (smaller files, better quality)
- **Hardware acceleration:** Add `-hwaccel videotoolbox` (macOS) for GPU encoding

## Distribution

### YouTube Upload

Videos are ready for YouTube upload:
- ✅ Meets technical requirements (1080p, H.264, AAC)
- ✅ Optimized for streaming (faststart)
- ✅ Professional quality

### Social Media

**Recommendations:**
- **LinkedIn:** Use full video (LinkedIn supports long-form)
- **Twitter/X:** Create shorter clips (3-5 min highlights)
- **Instagram:** Create 60s clips + link to full episode
- **Facebook:** Use full video

### Website Embedding

Videos can be:
1. Hosted on YouTube → embed YouTube player
2. Self-hosted (if bandwidth allows)
3. Hosted on video CDN (Vimeo, Cloudflare Stream, etc.)

## .gitignore

Video files (`.mp4`) are excluded from git in `podcast-generator/.gitignore` due to large file sizes.

**Why:** Video files range from 85-340 MB each, too large for git repository.

**Storage Options:**
- Local storage only (regenerate when needed)
- YouTube/Vimeo hosting
- Cloud storage (S3, Google Cloud Storage)
- Video CDN

## Future Enhancements

Potential improvements:

- [ ] Add waveform visualization overlay
- [ ] Support custom thumbnails/chapters
- [ ] Generate shorter clips for social media
- [ ] Add episode title/number overlay
- [ ] Support different aspect ratios (16:9, 1:1, 9:16)
- [ ] Batch processing with progress bars
- [ ] Upload to YouTube via API
- [ ] Generate video descriptions/titles automatically

## References

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [H.264 Encoding Guide](https://trac.ffmpeg.org/wiki/Encode/H.264)
- [AAC Encoding Guide](https://trac.ffmpeg.org/wiki/Encode/AAC)
