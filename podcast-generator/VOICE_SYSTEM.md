# Voice Consistency System

This document explains the voice consistency system that ensures all podcast episodes use correct and consistent voices for each speaker.

## Problem Statement

**Issue**: Random voice inconsistencies where a single chunk in an episode uses a different voice than the rest, breaking the listening experience.

**Root Causes**:
1. Hardcoded voice mappings instead of config-driven
2. Silent fallbacks to "default" voice when speaker lookup failed
3. No validation that cached chunks use correct voices
4. Alternative voice fallbacks that change voices without warning
5. No tracking of which voice was actually used for each chunk

## Solution Overview

The voice consistency system implements:

1. **Config-Driven Voice Selection**: All voices defined in `config.yaml`
2. **Fail-Loud Validation**: No silent fallbacks - errors are raised immediately
3. **Voice Tracking**: Every cached chunk stores which voice was used
4. **Cache Invalidation**: Cached chunks invalidated when voice config changes
5. **Consistency Validation**: Automatic checks and reporting tools

## Configuration

### config.yaml Format

```yaml
speakers:
  jordan:
    voice: "en-US-Chirp3-HD-Kore"  # Primary voice
    speed: 0.95
    pitch: 0
    volume_gain_db: 0.0
    alternatives:  # Optional fallback chain
      - "en-US-Chirp3-HD-Charon"
      - "en-US-Journey-D"
  alex:
    voice: "en-US-Chirp3-HD-Algieba"
    speed: 1.0
    pitch: 0
    volume_gain_db: 0.0
    alternatives:
      - "en-US-Chirp3-HD-Aoede"
      - "en-US-Journey-F"
```

**Requirements**:
- Each speaker MUST have a `voice` field
- Voice names must match Google Cloud TTS API voices exactly
- Alternatives are optional (use for error recovery only)

## Voice Selection Process

### 1. Startup Validation

When `generate_podcast.py` starts:

```
✓ Loaded voice mapping from config: {'jordan': 'en-US-Chirp3-HD-Kore', 'alex': 'en-US-Chirp3-HD-Algieba'}

🔍 Validating voice configuration...
  ✓ jordan: en-US-Chirp3-HD-Kore
  ✓ alex: en-US-Chirp3-HD-Algieba
✓ All voices validated successfully
```

**Failure Mode**: Script exits immediately if any voice doesn't exist in Google Cloud TTS.

### 2. Speaker Name Normalization

All speaker names are normalized before voice lookup:

- `"Jordan"` → `"jordan"`
- `"ALEX"` → `"alex"`
- `"Speaker 1"` → `"jordan"`
- `"Speaker 2"` → `"alex"`

This ensures consistent lookups regardless of capitalization or script format.

### 3. Strict Voice Lookup

```python
# BEFORE (silent fallback):
voice_name = self.voice_mapping.get(speaker, self.voice_mapping["default"])

# AFTER (fail loudly):
if speaker_normalized not in self.voice_mapping:
    raise ValueError(f"Unknown speaker: '{speaker}' ...")
voice_name = self.voice_mapping[speaker_normalized]
```

**Benefit**: Unknown speakers cause immediate failure with clear error message, preventing silent voice changes.

### 4. Alternative Voice Handling

If primary voice generation fails (rare API errors), alternatives are tried:

```
❌ Error generating audio: API error
⚠️  PRIMARY VOICE FAILED - Attempting alternative voices...
   This may cause voice inconsistency in the episode!
  Trying alternative voice: en-US-Chirp3-HD-Charon
  ✓ SUCCESS with alternative voice: en-US-Chirp3-HD-Charon
  ⚠️  WARNING: Voice changed from en-US-Chirp3-HD-Kore to en-US-Chirp3-HD-Charon
      This chunk will sound different from other jordan chunks!
```

**Important**: Alternative voices are logged prominently so issues are visible immediately.

## Cache Management

### Voice Metadata Storage

Every chunk in `cache/manifest.json` includes voice information:

```json
{
  "episodes": {
    "00002-cloud-providers-episode": {
      "chunks": {
        "abc123...": {
          "id": 0,
          "speaker": "jordan",
          "voice": "en-US-Chirp3-HD-Kore",
          "text_preview": "Today we're diving into...",
          "word_count": 15,
          "duration": 3.5,
          "generated_at": "2025-10-20T12:00:00"
        }
      }
    }
  }
}
```

### Cache Validation

When loading a chunk from cache, the system:

1. Checks if chunk file exists
2. Checks if voice matches current config
3. If voice changed → invalidates cache, regenerates chunk

```python
is_cached = cache_manager.is_chunk_cached(episode_id, chunk_hash)
voice_valid = cache_manager.is_chunk_voice_valid(episode_id, chunk_hash, expected_voice)

if is_cached and not voice_valid:
    print(f"  ⚠️  Cache invalid: voice changed (regenerating)")
    # Regenerate chunk with new voice
```

## Validation Tools

### 1. Voice Consistency Report

```bash
cd podcast-generator
python3 scripts/voice_report.py 00002-cloud-providers-episode
```

Output:
```
======================================================================
📊 VOICE CONSISTENCY REPORT: 00002-cloud-providers-episode
======================================================================

📈 SUMMARY:
  Total chunks: 108
  Last updated: 2025-10-20T10:58:19

🎯 EXPECTED CONFIGURATION:
  alex: en-US-Chirp3-HD-Algieba
  jordan: en-US-Chirp3-HD-Kore

👥 SPEAKER STATISTICS:

  ALEX:
    Total chunks: 54
    Voices used:
      ✓ en-US-Chirp3-HD-Algieba: 54 chunks (100.0%)

  JORDAN:
    Total chunks: 54
    Voices used:
      ✓ en-US-Chirp3-HD-Kore: 54 chunks (100.0%)

======================================================================
✅ VERDICT: ALL VOICES CONSISTENT
======================================================================
```

**Use Cases**:
- Check existing episodes for voice consistency
- Diagnose voice mismatch issues
- Verify regeneration worked correctly

### 2. Voice Validation Script

```bash
cd podcast-generator
python3 scripts/validate_voices.py 00002-cloud-providers-episode
```

Simpler output focused on pass/fail:

```
🔍 Validating voice consistency for episode: 00002-cloud-providers-episode
Expected voice mapping: {'jordan': 'en-US-Chirp3-HD-Kore', 'alex': 'en-US-Chirp3-HD-Algieba'}

📊 Validation Results:
  Total chunks: 108
  Mismatches: 0
  Unknown voices: 0

✅ Voice consistency: PASS
```

**Exit Codes**:
- `0` = All voices consistent
- `1` = Voice mismatches detected

**Use Cases**:
- Pre-flight checks before publishing
- CI/CD integration
- Batch validation of all episodes

### 3. List Available Voices

```bash
cd podcast-generator
python3 scripts/list_voices.py --chirp
```

Lists all Chirp3-HD voices available in Google Cloud TTS:

```
Chirp3-HD voices for en-US:

Algieba:
  - en-US-Chirp3-HD-Algieba                (MALE, 24000 Hz)

Aoede:
  - en-US-Chirp3-HD-Aoede                  (FEMALE, 24000 Hz)

Kore:
  - en-US-Chirp3-HD-Kore                   (FEMALE, 24000 Hz)

...
```

**Use Cases**:
- Finding new voices to test
- Verifying voice names are correct
- Checking voice availability

## Workflow for Episode Generation

### Normal Generation (with cache)

```bash
cd podcast-generator
python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00005-episode.txt
```

- Uses cached chunks where possible
- Validates voice consistency before using cache
- Regenerates chunks if voice config changed
- Reports voice consistency at end

### Force Regeneration

```bash
python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00005-episode.txt --force
```

- Regenerates ALL chunks (ignores cache)
- Updates voice metadata for all chunks
- Ensures 100% consistency with current config

**When to use --force**:
- Voice config changed (switched to different voices)
- Voice inconsistencies detected in validation
- Major TTS settings changed (speed, pitch, etc.)
- Cache corruption suspected

### Post-Generation Validation

After generating, validate voices:

```bash
python3 scripts/voice_report.py 00005-episode
```

Should show:
- ✅ All voices consistent
- No mismatches
- No unknown voices

## Troubleshooting

### Issue: "Unknown speaker" error

```
ValueError: Unknown speaker: 'Alex' (normalized: 'alex').
Valid speakers: ['jordan', 'alex'].
Check config.yaml speakers section.
```

**Cause**: Speaker not configured in `config.yaml`

**Fix**:
1. Add speaker to `config.yaml`
2. Or fix typo in script (e.g., "Alex" should work after normalization)

### Issue: "Invalid voice configuration"

```
✗ jordan: en-US-Chirp3-HD-Kore (NOT FOUND)
ValueError: Invalid voice configuration detected.
Run: python3 scripts/list_voices.py
```

**Cause**: Voice name doesn't exist in Google Cloud TTS

**Fix**:
1. Run `python3 scripts/list_voices.py --chirp`
2. Find correct voice name
3. Update `config.yaml`

### Issue: Voice mismatches detected

```
⚠️  WARNING: 5 voice mismatches detected!
  Chunk 23 (jordan): expected en-US-Chirp3-HD-Kore, got en-US-Journey-D
  ...
```

**Cause**: Episode generated with old voice config, now config changed

**Fix**:
```bash
python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00005-episode.txt --force
```

### Issue: Alternative voice used

```
⚠️  WARNING: Voice changed from en-US-Chirp3-HD-Kore to en-US-Chirp3-HD-Charon
    This chunk will sound different from other jordan chunks!
```

**Cause**: Primary voice API call failed, alternative voice used

**Options**:
1. **Accept it**: If difference is minor and episode sounds OK
2. **Regenerate**: Run again to try with primary voice
3. **Change config**: If problem persists, make alternative the primary

## Best Practices

### 1. Validate Before Publishing

Always run voice report before publishing:

```bash
python3 scripts/voice_report.py 00005-episode
```

Only publish if verdict is "✅ ALL VOICES CONSISTENT"

### 2. Test Voice Changes

When changing voices in config:

```bash
# 1. Generate test episode with new voices
python3 scripts/generate_podcast.py ../docs/podcasts/scripts/test-episode.txt --force

# 2. Listen to output
mpv output_latest/test-episode.mp3

# 3. If satisfied, regenerate all episodes
for script in ../docs/podcasts/scripts/*.txt; do
    python3 scripts/generate_podcast.py "$script" --force
done
```

### 3. Monitor Alternative Voice Usage

If you see frequent alternative voice warnings:

1. Primary voice may be unstable
2. Consider promoting alternative to primary in config
3. Or add more alternatives to fallback chain

### 4. Keep Voice Metadata

Never manually delete chunks from cache without updating manifest.json. Use the cache manager's `clean_orphaned_chunks()` instead.

## Technical Details

### Voice Normalization Logic

See [cloud_tts_generator.py:104-122](../scripts/cloud_tts_generator.py#L104-L122):

```python
def _normalize_speaker_name(self, speaker: str) -> str:
    normalized = speaker.lower().strip()
    if normalized == "speaker 1":
        normalized = "jordan"
    elif normalized == "speaker 2":
        normalized = "alex"
    return normalized
```

### Cache Validation Logic

See [cache_manager.py:112-137](../scripts/cache_manager.py#L112-L137):

```python
def is_chunk_voice_valid(self, episode_id: str, chunk_hash: str, expected_voice: str) -> bool:
    chunk_metadata = episode_manifest["chunks"][chunk_hash]
    cached_voice = chunk_metadata.get("voice", "unknown")

    # If voice is unknown (old cache), assume valid for now
    if cached_voice == "unknown":
        return True

    # Check if voices match
    return cached_voice == expected_voice
```

## Migration from Old System

Existing episodes have `"voice": "unknown"` in cache metadata.

**Options**:

1. **Lazy migration**: Regenerate episodes as needed
   - Unknown voices are tolerated (backward compatibility)
   - Regenerate only when editing or updating

2. **Batch migration**: Regenerate all episodes
   ```bash
   cd podcast-generator
   for script in ../docs/podcasts/scripts/*.txt; do
       python3 scripts/generate_podcast.py "$script" --force
   done
   ```

3. **Validate first, regenerate if needed**:
   ```bash
   python3 scripts/validate_voices.py --all
   # Shows which episodes need regeneration
   ```

## Future Improvements

Potential enhancements:

- [ ] Audio fingerprinting to detect actual voice used
- [ ] Automatic voice quality scoring
- [ ] A/B testing framework for comparing voices
- [ ] Voice consistency CI/CD checks
- [ ] Dashboard for voice analytics across all episodes
