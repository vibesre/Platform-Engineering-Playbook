---
name: Reel Audio
description: Generate high-energy TTS audio for short-form reel scripts (30-60s) using Gemini TTS with tone control, fast pacing, minimal pauses, and automatic pronunciation corrections.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Reel Audio Generation

Generate engaging, fast-paced audio for social media reels (YouTube Shorts, Instagram Reels, TikTok) from validated reel scripts using Gemini TTS with natural language tone control optimized for short-form content.

## When to Use This Skill

Use this skill when:
- User says: "Generate reel audio", "Create audio for reels", "TTS for episode reels"
- Reel scripts exist in `podcast-generator/episodes/00XXX-name/reels/`
- Scripts are already written and validated (from reel-script skill)
- Need audio files for video production

**Prerequisites**: Reel scripts must exist and be validated.

## Quick Start

**Example Usage**:
```
"Generate audio for episode 00008 reels"
"Create TTS for the GCP reels"
```

This will process all reel-*.txt files in the episode directory and generate MP3 audio files.

## Audio Characteristics

### Voice Configuration

**Gemini TTS with Tone Control** (default):
- **Model**: gemini-2.5-flash-tts
- **Voice**: Aoede (energetic, clear)
- **Style Prompt**: "Speak energetically and fast like an enthusiastic tech presenter explaining concepts to senior engineers. Build excitement around surprising statistics. Be direct and punchy with minimal pauses."
- **Speed**: 1.0x (natural - Gemini handles pacing via prompt)
- **Language**: en-US

**Why Gemini TTS?**:
- **Tone control**: Natural language prompts for delivery style
- **Markup tags**: `[extremely fast]`, `[emphasis on X]`, `[building excitement]`
- **Natural pacing**: Smarter than speed multipliers
- **Engagement**: Can build energy, emphasize stats, create urgency

**Why Aoede Voice?**:
- Energetic without being shrill
- Clear for technical content
- Good dynamic range for emphasis
- Works well with fast delivery

**Alternative Voices**: Kore (female), Charon (male)

### Pacing Strategy

**Short-Form Optimization with Gemini Markup**:
- **Natural pacing**: Gemini TTS handles speed via style prompt
- **Markup tags** for energy and emphasis
- **Minimal pauses**: Only at pattern interrupts
- **No long pauses**: Kills retention on short-form

**Gemini Markup Tags** (available for enhancement):
- `[extremely fast]` - Speed up delivery for energy
- `[dramatic pause]` - Brief pause for emphasis (0.3s)
- `[emphasis on "term"]` - Stress specific words
- `[building excitement]` - Increase energy
- `[sigh]` - Slight pause with breath
- `[whispering]` - Quieter for "insider info" feel

**Example Usage in Scripts**:
```
[extremely fast] GCP is growing at thirty two percent. [dramatic pause]
AWS? Seventeen percent. [emphasis on "That's nearly double."]
```

**Note**: Start with clean scripts, add markup tags only if needed for specific effect.

## File Organization

### Input Structure

```
podcast-generator/episodes/00008-gcp-state-of-the-union-2025/
├── reels/
│   ├── reel-01-network-performance.txt       (original scripts)
│   ├── reel-02-automatic-discounts.txt
│   ├── reel-03-growth-rate.txt
│   ├── reel-04-breadth-vs-depth.txt
│   ├── reel-05-bigquery-savings.txt
│   └── concepts.md
```

### Output Structure

```
podcast-generator/episodes/00008-gcp-state-of-the-union-2025/
├── reels/
│   ├── audio/
│   │   ├── reel-01-network-performance.mp3              (final audio)
│   │   ├── reel-01-network-performance-formatted.txt   (with SSML tags, for debugging)
│   │   ├── reel-02-automatic-discounts.mp3
│   │   ├── reel-02-automatic-discounts-formatted.txt
│   │   └── ...
│   └── [original scripts, untouched]
```

## Processing Workflow

### Step 1: Locate Episode & Validate

**Find episode directory**:
```bash
# User provides episode number (e.g., "00008")
EPISODE_DIR="podcast-generator/episodes/${EPISODE_NUM}-*"
```

**Check prerequisites**:
1. Episode directory exists
2. `reels/` subdirectory exists
3. At least one `reel-*.txt` file found
4. Each script is 110-140 words (30-60s target)

**If prerequisites fail**:
- Alert user: "No reel scripts found for episode 00008"
- Suggest: "Run reel-script skill first to generate scripts"

### Step 2: Process Each Reel Script

For each `reel-XX-name.txt` file:

**2a. Copy to Processing Location**:
```bash
mkdir -p reels/audio
cp reels/reel-01-network-performance.txt /tmp/reel-01-processing.txt
```

**2b. Add Pronunciation Tags** (automated):

Use existing `add_pronunciation_tags.py` script:
```bash
cd podcast-generator
python3 scripts/add_pronunciation_tags.py \
  --file /tmp/reel-01-processing.txt \
  --verbose
```

This applies all terms from PRONUNCIATION_GUIDE.md:
- `<say-as interpret-as="characters">AWS</say-as>`
- `<phoneme alphabet="ipa" ph="ˌkubɚˈnɛtiz">Kubernetes</phoneme>`
- `<phoneme alphabet="ipa" ph="ˈæʒɚ">Azure</phoneme>`
- etc.

**2c. Add Minimal Pause Tags**:

Only add pauses at pattern interrupts marked in scripts:
- Look for `[Pattern interrupt at Xs]` annotations
- Add `[pause short]` or `[pause]` where specified
- Keep pauses minimal (short-form optimization)

**Example**:
```
Original script line:
  This matters for your data pipelines, your microservices, anything moving significant data between instances.

With pause (at pattern interrupt):
  This matters for your data pipelines, [pause short] your microservices, anything moving significant data between instances.
```

**2d. Save Formatted Script**:
```bash
# Save with SSML tags for debugging
cp /tmp/reel-01-processing.txt \
  reels/audio/reel-01-network-performance-formatted.txt
```

### Step 3: Generate TTS Audio

**Use existing TTS pipeline**:

Create a simple wrapper script or use directly:
```python
from cloud_tts_generator import GoogleCloudTTSGenerator
import yaml

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize TTS with reel_presenter voice
tts = GoogleCloudTTSGenerator(config=config)

# Read formatted script
with open('reels/audio/reel-01-network-performance-formatted.txt', 'r') as f:
    script_text = f.read()

# Generate audio
output_path = 'reels/audio/reel-01-network-performance.mp3'
result = tts.generate_audio(
    text=script_text,
    speaker='reel_presenter',  # Uses config voice
    output_path=output_path
)

print(f"Generated: {output_path}")
print(f"Duration: {result['duration']}s")
print(f"Cost: ${result.get('cost', 0):.4f}")
```

**Voice Configuration** (from config.yaml):
- Model: `gemini-2.5-flash-tts`
- Voice: `Aoede`
- Language: `en-US`
- Style prompt: Energetic tech presenter tone
- Speed: 1.0x (natural)
- Sample rate: 44.1kHz
- Bitrate: 128k MP3

### Step 4: Validate Output

**Quality Checks**:
1. ✅ Audio file exists
2. ✅ Duration is 30-60s (based on word count)
3. ✅ File size reasonable (500KB-1.5MB for 45s)
4. ✅ No TTS errors in logs

**Validation Formula**:
```python
word_count = len(script.split())
# Gemini TTS with energetic prompt typically runs ~165 WPM
expected_duration = word_count / 165
actual_duration = get_audio_duration(output_file)

if abs(expected_duration - actual_duration) > 5:
    print(f"⚠️  Duration mismatch: expected {expected_duration}s, got {actual_duration}s")
```

**Test Pronunciation** (spot check):
Listen to key terms:
- AWS, GCP, Azure (should be spelled out)
- Kubernetes (should be "coo-ber-NET-ees")
- BigQuery (should be clear)

### Step 5: Report Results

**Generation Summary**:
```
✅ Reel Audio Generation Complete

Episode: 00008-gcp-state-of-the-union-2025
Reels Processed: 5/5

Files Generated:
  ✓ reel-01-network-performance.mp3 (42s, 127 words)
  ✓ reel-02-automatic-discounts.mp3 (40s, 116 words)
  ✓ reel-03-growth-rate.mp3 (45s, 140 words)
  ✓ reel-04-breadth-vs-depth.mp3 (43s, 135 words)
  ✓ reel-05-bigquery-savings.mp3 (44s, 139 words)

Total Duration: 3 min 34s
Total Cost: $0.08 (Chirp3-HD pricing)

Output Location: podcast-generator/episodes/00008-.../reels/audio/

Next Steps:
  1. Review audio files for quality
  2. Use for video production with text overlays
  3. Publish to social media platforms
```

## Technical Implementation

### Option 1: Python Script (Recommended)

Create `podcast-generator/scripts/generate_reel_audio.py`:

```python
#!/usr/bin/env python3
"""
Generate TTS audio for reel scripts.
"""
import sys
from pathlib import Path
import yaml
import argparse
from cloud_tts_generator import GoogleCloudTTSGenerator
from add_pronunciation_tags import add_pronunciation_tags

def generate_reel_audio(episode_dir: Path, config_path: Path = Path("config.yaml")):
    """Generate audio for all reel scripts in episode directory."""

    # Load config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Find reel scripts
    reels_dir = episode_dir / "reels"
    if not reels_dir.exists():
        print(f"Error: {reels_dir} not found")
        return

    scripts = sorted(reels_dir.glob("reel-*.txt"))
    if not scripts:
        print(f"No reel scripts found in {reels_dir}")
        return

    print(f"Found {len(scripts)} reel scripts\n")

    # Create audio directory
    audio_dir = reels_dir / "audio"
    audio_dir.mkdir(exist_ok=True)

    # Initialize TTS
    tts = GoogleCloudTTSGenerator(config=config)

    results = []
    total_cost = 0

    for script_path in scripts:
        print(f"Processing: {script_path.name}")

        # Read script
        with open(script_path, 'r') as f:
            original_text = f.read()

        # Strip metadata (lines starting with #, **, ---)
        lines = [l for l in original_text.split('\n')
                 if not l.strip().startswith(('#', '**', '---', '['))]
        script_text = '\n'.join(lines)

        # Add pronunciation tags
        formatted_text, count = add_pronunciation_tags(script_text, verbose=False)
        print(f"  Added {count} pronunciation tags")

        # Add minimal pauses (where pattern interrupts are noted)
        # For now, add short pauses at sentence boundaries
        formatted_text = formatted_text.replace('. ', '. [pause short] ')
        formatted_text = formatted_text.replace('? ', '? [pause short] ')

        # Save formatted version
        formatted_path = audio_dir / f"{script_path.stem}-formatted.txt"
        with open(formatted_path, 'w') as f:
            f.write(formatted_text)

        # Generate audio
        output_path = audio_dir / f"{script_path.stem}.mp3"
        result = tts.generate_audio(
            text=formatted_text,
            speaker='reel_presenter',
            output_path=output_path
        )

        duration = result.get('duration', 0)
        cost = result.get('cost', 0)
        total_cost += cost

        print(f"  ✓ Generated: {output_path.name} ({duration:.1f}s, ${cost:.4f})")

        results.append({
            'name': script_path.stem,
            'duration': duration,
            'cost': cost,
            'output': output_path
        })

    # Print summary
    print(f"\n{'='*80}")
    print(f"✅ Generated {len(results)} reel audio files")
    print(f"Total Duration: {sum(r['duration'] for r in results):.1f}s")
    print(f"Total Cost: ${total_cost:.4f}")
    print(f"\nOutput: {audio_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate reel audio")
    parser.add_argument("episode_dir", type=Path, help="Episode directory")
    parser.add_argument("--config", type=Path, default=Path("config.yaml"))
    args = parser.parse_args()

    generate_reel_audio(args.episode_dir, args.config)
```

**Usage**:
```bash
cd podcast-generator
python3 scripts/generate_reel_audio.py episodes/00008-gcp-state-of-the-union-2025
```

### Option 2: Manual Bash Workflow

If Python script not ready, use manual commands:

```bash
cd podcast-generator
EPISODE="00008-gcp-state-of-the-union-2025"

# Create audio directory
mkdir -p episodes/$EPISODE/reels/audio

# For each reel
for reel in episodes/$EPISODE/reels/reel-*.txt; do
  basename=$(basename "$reel" .txt)

  # Add pronunciation tags
  python3 scripts/add_pronunciation_tags.py --file "$reel"

  # Generate audio (requires custom integration)
  # ... TTS generation command ...

  echo "Processed: $basename"
done
```

## Cost Estimation

**Gemini TTS Pricing**: Check current Google Cloud pricing (typically competitive with Chirp3-HD)

**Estimated Per-Reel Cost**:
- Average reel: 130 words × 6 chars/word = 780 characters
- Estimated cost: ~$0.01-0.02 per reel

**Episode Cost** (5 reels):
- Estimated total: $0.05-0.10

**Very Affordable**: Entire episode's reels cost less than a coffee.

**Note**: Gemini TTS pricing may vary by region. Check latest pricing at https://cloud.google.com/text-to-speech/pricing

## Troubleshooting

### "Config is required" Error

**Problem**: TTS generator can't find config
**Solution**:
```bash
cd podcast-generator  # Run from podcast-generator directory
python3 scripts/generate_reel_audio.py episodes/00008-...
```

### "Voice not found: reel_presenter"

**Problem**: Config doesn't have reel_presenter voice
**Solution**: Check config.yaml has:
```yaml
speakers:
  reel_presenter:
    voice: "Aoede"
    model: "gemini-2.5-flash-tts"
    language_code: "en-US"
    style_prompt: "Speak energetically and fast..."
```

### "No reel scripts found"

**Problem**: Scripts don't exist
**Solution**: Run reel-script skill first:
```
"Use reel-script skill to generate scripts for episode 00008"
```

### Pronunciation Issues

**Problem**: Terms mispronounced (e.g., "AWS" as "awwss")
**Solution**:
1. Check PRONUNCIATION_GUIDE.md has the term
2. Verify pronunciation tags were applied
3. Check formatted script has `<say-as>` or `<phoneme>` tags

### Duration Mismatch

**Problem**: Audio is 60s but should be 40s
**Solution**:
1. Check word count in script (should be 110-140 words)
2. Verify style prompt emphasizes fast delivery
3. Reduce pauses if too many added
4. Consider adding `[extremely fast]` markup tags for tighter timing

## Quality Checklist

Before publishing reel audio:

**Technical Quality**:
- [ ] All audio files generated successfully
- [ ] Duration matches target (30-60s per reel)
- [ ] File format is MP3, 128k bitrate
- [ ] No clipping or distortion

**Content Quality**:
- [ ] Pronunciation correct (spot check key terms)
- [ ] Pacing feels energetic (not too slow)
- [ ] Pauses minimal but effective
- [ ] Voice energy matches short-form style

**Organization**:
- [ ] Files in `reels/audio/` directory
- [ ] Formatted scripts saved for debugging
- [ ] Filenames match reel scripts

**Next Steps Ready**:
- [ ] Audio ready for video production
- [ ] Text overlays match audio timing
- [ ] CTAs clear in audio

## Advanced: Multi-Voice for Pattern Interrupts

**Experimental**: Use different voice for statistics/reveals

**Example**:
```python
# Primary voice: reel_presenter (Aoede)
# Stats voice: jordan (Kore - different voice for contrast)

# In generate_reel_audio.py, detect text overlays:
if '[TEXT OVERLAY:' in line:
    # Use different voice for this line
    speaker = 'jordan'  # Contrast voice
else:
    speaker = 'reel_presenter'  # Main voice
```

**Pros**:
- Pattern interrupt creates engagement
- Statistics feel more emphatic

**Cons**:
- More complex to implement
- Can feel jarring if not done well

**Recommendation**: Start with single voice, experiment later.

## Success Metrics

**Audio Generation Success**:
- ✅ 100% of reel scripts generate audio
- ✅ Average duration: 40-45s (target)
- ✅ Cost per episode: <$0.10
- ✅ Zero pronunciation errors on key terms

**Engagement Metrics** (after publishing):
- Track completion rate (% who watch full reel)
- Compare retention to industry benchmarks (60%+ good)
- Monitor comments about audio quality

## Related Skills

**Prerequisites**:
- **reel-script**: Generate the reel scripts first

**Next Steps**:
- **Video production** (future skill): Add text overlays, B-roll
- **Publishing** (future skill): Upload to social media

## References

- **Voice Documentation**: `podcast-generator/config.yaml` (speakers section)
- **Pronunciation Guide**: `podcast-generator/PRONUNCIATION_GUIDE.md`
- **TTS Generator**: `podcast-generator/scripts/cloud_tts_generator.py`
- **Chirp3-HD Pricing**: https://cloud.google.com/text-to-speech/pricing

---

**Last Updated**: 2025-10-26
**Version**: 1.0.0
