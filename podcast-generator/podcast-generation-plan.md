# Podcast Generation System Plan

## Overview
Build a system to generate high-quality podcast audio from text scripts using Google AI Studio's text-to-speech capabilities, with intelligent chunking for efficient regeneration and duration limit management.

## Architecture

### Phase 1: Local Script Development

#### 1. Chunking Strategy
- **Chunk by semantic boundaries**: Split at paragraph breaks or natural pauses
- **Target chunk duration**: 30-60 seconds (approximately 80-150 words)
- **Metadata per chunk**:
  - Content hash (SHA-256)
  - Text content
  - Duration estimate
  - Speaker assignment
  - Chunk order index

#### 2. Core Components

```
podcast-generator/
├── scripts/
│   ├── generate_podcast.py       # Main orchestrator
│   ├── chunker.py               # Text chunking logic
│   ├── tts_generator.py         # Google AI Studio interface
│   ├── audio_stitcher.py        # Combine chunks
│   └── cache_manager.py         # Handle chunk caching
├── cache/
│   ├── chunks/                  # Individual audio chunks
│   │   └── {episode_id}/
│   │       └── chunk_{hash}.mp3
│   └── manifest.json            # Chunk metadata
├── output/
│   └── {episode_name}.mp3       # Final stitched audio
└── config.yaml                  # Configuration

```

#### 3. Implementation Steps

**Step 1: Text Chunker**
- Parse podcast scripts (markdown format)
- Identify speaker changes (Speaker 1:, Speaker 2:)
- Split into semantic chunks
- Generate content hashes
- Create chunk manifest

**Step 2: Google AI Studio Integration**
- Use Google AI Studio API for TTS
- Support multiple voices for different speakers
- Configure voice parameters (speed, pitch, emphasis)
- Handle rate limiting with exponential backoff
- Estimate duration before generation

**Step 3: Cache Management**
- Check chunk hash against cache
- Skip regeneration for unchanged chunks
- Update only modified chunks
- Clean orphaned chunks

**Step 4: Audio Processing**
- Use ffmpeg for audio stitching
- Add subtle crossfades between chunks
- Normalize audio levels
- Generate final podcast file

### Phase 2: GitHub Actions Integration

#### 1. Storage Strategy

**Option A: GitHub Releases (Recommended)**
- Store chunks as release assets
- Use semantic versioning for episodes
- Automatic cleanup of old versions
- No repository bloat

**Option B: Git LFS**
- Track audio files with Git LFS
- Version control for all chunks
- Higher storage costs

**Option C: GitHub Actions Artifacts**
- Temporary storage (90 days)
- Good for intermediate builds
- Not suitable for long-term storage

#### 2. Workflow Design

```yaml
name: Generate Podcast
on:
  push:
    paths:
      - 'content/podcast-episodes/**/*.md'
  workflow_dispatch:
    inputs:
      episode:
        description: 'Episode to regenerate'
        required: false

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        
      - name: Install dependencies
        run: |
          pip install google-generativeai pydub ffmpeg-python
          sudo apt-get install ffmpeg
          
      - name: Download cached chunks
        uses: actions/download-artifact@v3
        with:
          name: podcast-chunks
          path: cache/chunks
          
      - name: Generate podcast
        env:
          GOOGLE_AI_API_KEY: ${{ secrets.GOOGLE_AI_API_KEY }}
        run: python scripts/generate_podcast.py
        
      - name: Upload chunks
        uses: actions/upload-artifact@v3
        with:
          name: podcast-chunks
          path: cache/chunks
          
      - name: Create release
        uses: softprops/action-gh-release@v1
        with:
          files: output/*.mp3
          tag_name: podcast-${{ github.run_number }}
```

## Technical Details

### Chunk Detection Algorithm
```python
def should_regenerate_chunk(chunk_text, manifest):
    current_hash = hashlib.sha256(chunk_text.encode()).hexdigest()
    return current_hash != manifest.get(chunk_id, {}).get('hash')
```

### Voice Configuration
```yaml
speakers:
  jordan:
    voice: "en-US-Journey-D"  # Male voice
    speed: 1.0
    pitch: 0
  alex:
    voice: "en-US-Journey-F"  # Female voice
    speed: 1.0
    pitch: 0
    
audio_settings:
  sample_rate: 44100
  bitrate: "128k"
  format: "mp3"
```

### Chunking Rules
1. Never split mid-sentence
2. Prefer paragraph boundaries
3. Keep speaker turns together when possible
4. Target 30-60 second chunks
5. Maximum chunk size: 90 seconds

## Benefits

1. **Efficiency**: Only regenerate changed content
2. **Scalability**: Handle long podcasts without timeout
3. **Version Control**: Track all changes to audio
4. **Cost Optimization**: Minimize API calls
5. **Flexibility**: Easy to adjust voices or regenerate sections

## Next Steps

1. Implement local script with basic chunking
2. Test with sample podcast episode
3. Add Google AI Studio integration
4. Implement caching system
5. Create GitHub Action workflow
6. Set up release automation
7. Add monitoring and error handling

## Considerations

- **API Limits**: Google AI Studio rate limits
- **Storage Costs**: GitHub LFS or release storage
- **Audio Quality**: Ensure consistent quality across chunks
- **Error Handling**: Graceful degradation if TTS fails
- **Security**: Protect API keys in GitHub Secrets