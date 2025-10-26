# Podcast Generator

A sophisticated podcast generation system that converts text scripts into high-quality audio using Google AI Studio's text-to-speech capabilities. Features intelligent chunking, caching, and audio processing for efficient regeneration.

## Features

- **Intelligent Chunking**: Splits scripts into semantic chunks to avoid API duration limits
- **Smart Caching**: Only regenerates changed chunks, preserving unchanged audio
- **Multi-Speaker Support**: Different voices for different speakers
- **Audio Processing**: Automatic stitching, crossfades, and normalization
- **Batch Processing**: Generate multiple episodes at once
- **GitHub Actions Ready**: Designed for CI/CD integration

## Setup

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install ffmpeg (required for audio processing)
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### 2. Configure Google AI Studio

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Option A**: Create a `.env` file (recommended for local development):
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```
3. **Option B**: Set environment variable:
   ```bash
   export GOOGLE_AI_API_KEY='your-api-key-here'
   ```

### 3. Configure Settings

Edit `config.yaml` to customize:
- Speaker voices and settings
- Audio quality parameters
- Chunking thresholds
- Processing options

## Usage

### Generate a Single Podcast

```bash
# Basic usage
python scripts/generate_podcast.py sample-episode.md

# With custom episode ID
python scripts/generate_podcast.py sample-episode.md --episode-id "ep001-kubernetes"

# Force regeneration (ignore cache)
python scripts/generate_podcast.py sample-episode.md --force
```

### Batch Processing

```bash
# Process all markdown files in a directory
python scripts/generate_podcast.py /path/to/episodes/ --batch
```

### Script Format

Podcast scripts should be markdown files with clear speaker indicators:

```markdown
Speaker 1: Welcome to the show! I'm Jordan.

Speaker 2: And I'm Alex. Today we're discussing...

Jordan: [Can also use speaker names directly]

Alex: That's a great point about...
```

## Script Formats

The generator supports two episode formats:

1. **Simple Dialogue Format**: Direct speaker dialogue for immediate processing
2. **Documentation Format**: Rich markdown with auto-dialogue extraction

See [EPISODE_FORMATS.md](EPISODE_FORMATS.md) for detailed format guide.

## Video Generation

Convert podcast audio files to video format with a looping background animation:

```bash
# Generate video for a single episode
python3 scripts/generate_video.py output_latest/00001-episode-name.mp3

# Generate videos for all episodes
python3 scripts/generate_video.py --all

# Use custom output path
python3 scripts/generate_video.py output_latest/00001-episode-name.mp3 --output custom.mp4
```

**Features:**
- Automatic video looping to match audio duration
- 1920x1080 Full HD resolution
- H.264/AAC encoding optimized for streaming
- Background video: `assets/background.mp4`

See [VIDEO_GENERATION.md](VIDEO_GENERATION.md) for complete documentation.

## How It Works

1. **Format Detection**: Automatically detects documentation vs dialogue format
2. **Dialogue Extraction**: Extracts speaker turns from rich documentation
3. **Chunking**: Scripts are split into ~45-second chunks at natural boundaries
4. **Hashing**: Each chunk gets a unique hash based on content
5. **Caching**: Only chunks with changed hashes are regenerated  
6. **Generation**: Google AI Studio converts text to speech
7. **Stitching**: ffmpeg combines chunks with subtle crossfades
8. **Normalization**: Audio levels are balanced for consistency

## Output Structure

```
podcast-generator/
├── cache/
│   ├── chunks/
│   │   └── episode-name/
│   │       ├── chunk_abc123.mp3
│   │       └── chunk_def456.mp3
│   └── manifest.json         # Chunk metadata
└── output/
    └── episode-name_20240315_143022.mp3
```

## Advanced Features

### Custom Voices

Add new speakers in `config.yaml`:

```yaml
speakers:
  narrator:
    voice: "en-US-Studio-M"
    speed: 0.95
    pitch: -2
```

### Chunk Size Tuning

Adjust chunk sizes for different content types:

```yaml
chunking:
  min_words: 80      # Minimum chunk size
  max_words: 150     # Maximum chunk size
  target_duration_seconds: 45
```

## Troubleshooting

### API Key Issues
- Ensure `GOOGLE_AI_API_KEY` is set correctly
- Check API quota limits in Google Console

### Audio Quality
- Verify ffmpeg is installed: `ffmpeg -version`
- Check audio settings in `config.yaml`

### Chunking Problems
- Review chunk boundaries in the manifest
- Adjust min/max word settings
- Use `--force` to regenerate all chunks

## Production Notes

### Google Cloud TTS

For production use, consider Google Cloud Text-to-Speech API:

1. Enable the API in Google Cloud Console
2. Install additional dependency:
   ```bash
   pip install google-cloud-texttospeech
   ```
3. Update `tts_generator.py` to use `GoogleCloudTTSGenerator`

### GitHub Actions Integration

See `podcast-generation-plan.md` for detailed GitHub Actions setup including:
- Automated generation on script changes
- Chunk caching across runs
- Release creation for episodes

## Text-to-Speech Options

The system supports multiple TTS providers:

1. **Google Cloud TTS** (Recommended) - High-quality Journey/Studio voices
2. **Google AI Studio** - Coming soon with Gemini models
3. **Placeholder Audio** - Default for testing without API setup

See [TTS_SETUP.md](TTS_SETUP.md) for detailed setup instructions.

## Limitations

- Gemini TTS not yet available in public SDK
- Maximum chunk duration limited by API constraints (5000 chars)
- TTS APIs require authentication setup

## Next Steps

1. Integrate production TTS API
2. Add support for background music
3. Implement voice cloning capabilities
4. Create web interface for script management
5. Add analytics and monitoring

## Contributing

1. Test changes locally first
2. Ensure all chunks regenerate correctly
3. Verify audio quality after changes
4. Update tests and documentation