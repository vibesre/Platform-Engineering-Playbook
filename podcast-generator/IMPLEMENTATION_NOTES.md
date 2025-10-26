# Podcast Generator Implementation Notes

## Current Status

### ✅ Completed
- **Chunking System**: Intelligent text splitting based on speaker turns and word count
- **Cache Management**: Content-based hashing for efficient regeneration
- **Audio Processing**: ffmpeg integration for stitching and normalization
- **Local Script**: Full orchestration of the generation pipeline
- **GitHub Actions**: Automated workflow with caching and releases
- **Documentation**: Comprehensive README and setup guides

### ⚠️ Pending Integration
- **Google AI Studio TTS**: Currently using placeholder audio generation
  - Real API integration requires official SDK support for TTS
  - Alternative: Google Cloud Text-to-Speech API (production ready)

## Architecture Decisions

### Chunking Strategy
- **Semantic boundaries**: Splits at speaker changes and paragraph breaks
- **Dynamic sizing**: 80-150 words per chunk (roughly 30-60 seconds)
- **Hash-based caching**: Only regenerates changed content

### Storage Approach
- **Local development**: File-based cache with JSON manifest
- **GitHub Actions**: Artifacts for chunks, releases for final audio
- **Why not Git LFS**: Avoids repository bloat, releases are cleaner

### Audio Processing
- **ffmpeg**: Industry standard, handles all audio operations
- **Normalization**: Two-pass loudnorm for consistent volume
- **Crossfades**: Subtle 50ms overlaps between chunks

## Production Considerations

### Google Cloud TTS Migration
```python
# Current (placeholder)
generator = TTSGenerator()

# Production (Google Cloud)
from google.cloud import texttospeech
generator = GoogleCloudTTSGenerator()
```

### Scaling Strategies
1. **Parallel chunk generation**: Process multiple chunks concurrently
2. **CDN distribution**: Upload to S3/CloudFront for global access
3. **Queue-based processing**: Use SQS/Celery for large batches

### Cost Optimization
- Cache chunks aggressively (current implementation ✓)
- Use lower quality for drafts
- Batch API calls where possible
- Monitor usage with detailed logging

## Testing Strategy

### Unit Tests (to implement)
```python
# test_chunker.py
def test_speaker_detection()
def test_chunk_boundaries()
def test_hash_consistency()

# test_cache.py
def test_cache_hit_detection()
def test_manifest_updates()
def test_orphan_cleanup()
```

### Integration Tests
- Generate sample episode end-to-end
- Verify audio output quality
- Test GitHub Actions workflow

## Known Limitations

1. **TTS Quality**: Placeholder audio until real API integration
2. **Voice Selection**: Limited to predefined speakers
3. **Processing Time**: Sequential chunk generation (can be parallelized)
4. **File Size**: No compression beyond MP3 encoding

## Future Enhancements

### Phase 1 (Next Sprint)
- [ ] Real Google AI Studio TTS integration
- [ ] Parallel chunk processing
- [ ] Progress indicators
- [ ] Error recovery improvements

### Phase 2 (Future)
- [ ] Web UI for script management
- [ ] Voice cloning capabilities
- [ ] Background music integration
- [ ] Multiple language support
- [ ] Real-time preview

### Phase 3 (Long-term)
- [ ] Distributed processing
- [ ] Advanced audio effects
- [ ] AI-powered script enhancement
- [ ] Podcast feed generation

## Debugging Tips

### Common Issues
1. **API Key not found**: Check environment variable
2. **ffmpeg errors**: Verify installation with `ffmpeg -version`
3. **Cache misses**: Check manifest.json for hash mismatches
4. **Audio gaps**: Increase crossfade duration in config

### Useful Commands
```bash
# Test chunking only
python -m scripts.chunker

# Clear cache
rm -rf cache/chunks/* cache/manifest.json

# Generate with verbose logging
PYTHONPATH=scripts python scripts/generate_podcast.py sample-episode.md

# Test GitHub Action locally
act -j generate-podcasts
```

## Performance Metrics

### Current Performance (estimated)
- Chunking: ~1 second per episode
- TTS Generation: ~2 seconds per chunk (with real API)
- Audio Stitching: ~5 seconds per episode
- Total: ~2-3 minutes for 15-minute episode

### Optimization Opportunities
- Parallel chunk generation: 3-5x speedup
- GPU-accelerated TTS: 10x speedup
- Pre-computed voice embeddings: 2x speedup

## Security Considerations

- API keys in environment variables only
- No sensitive data in cache
- Sanitize user input in scripts
- Rate limiting for API calls
- Secure storage for generated audio

## Monitoring & Observability

### Metrics to Track
- Chunks generated vs cached ratio
- API call count and errors
- Processing time per episode
- Storage usage trends
- Cost per episode

### Logging Strategy
```python
import logging

logger = logging.getLogger('podcast_generator')
logger.info(f"Generated chunk {chunk_id} in {duration}s")
logger.error(f"TTS API error: {error}", exc_info=True)
```

## Conclusion

This implementation provides a solid foundation for automated podcast generation with intelligent caching and efficient processing. The modular architecture allows for easy enhancement and scaling as requirements evolve.