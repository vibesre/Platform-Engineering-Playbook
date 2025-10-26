# Podcast Episode Formats Guide

The podcast generator supports two formats for episode scripts:

## Format 1: Simple Dialogue Format (Direct)

Best for scripts written specifically for audio generation.

```markdown
Speaker 1: Welcome to our podcast! I'm Jordan.

Speaker 2: And I'm Alex. Today we're discussing cloud architecture.

Jordan: Let's start with the basics...

Alex: Great idea! Cloud computing has transformed how we build applications.
```

**Characteristics:**
- Clean, dialogue-only format
- No metadata or formatting
- Direct speaker indicators
- Ready for immediate processing

## Format 2: Documentation Format (Rich)

Best for episodes that serve dual purpose as documentation and podcast scripts.

```markdown
---
displayed_sidebar: tutorialSidebar
---

# Episode Title

**Duration:** 25-30 minutes  
**Speakers:** Alex and Jordan  
**Target Audience:** Senior engineers

### Introduction

**Jordan:** Welcome to the show...

**Alex:** Thanks for having me...

### Main Discussion

The conversation continues...

---

## Production Notes

Additional context and notes...
```

**Characteristics:**
- Rich formatting with sections
- Metadata and production notes
- Can be displayed as documentation
- Requires dialogue extraction

## Automatic Format Detection

The generator automatically detects documentation format and extracts dialogue when it finds:
- YAML frontmatter (`---`)
- Production notes sections
- Duration/audience metadata
- Multiple formatting markers

## Manual Extraction

Extract dialogue from documentation format:

```bash
# Extract and save dialogue
python scripts/extract_dialogue.py docs/episode.md -o content/episode-dialogue.md

# Preview extraction
python scripts/extract_dialogue.py docs/episode.md --preview

# Generate podcast with extraction
python scripts/generate_podcast.py docs/episode.md --extract-dialogue
```

## Workflow Options

### Option 1: Direct Generation
Write episodes in simple dialogue format for immediate processing:
```bash
python scripts/generate_podcast.py episodes/my-episode.md
```

### Option 2: Documentation + Audio
1. Write rich documentation with embedded dialogue
2. The generator auto-extracts dialogue
3. Both documentation and audio are generated

### Option 3: Separate Files
1. Maintain documentation version in `docs/`
2. Extract dialogue to `content/podcast-episodes/`
3. Generate audio from extracted dialogue

## Best Practices

### For Documentation Format:
- Use bold for speaker names: `**Jordan:**`
- Keep dialogue separate from narrative
- Use clear section breaks
- Include metadata at the top

### For Direct Format:
- Start each turn with `Speaker:` or name
- Use blank lines between speakers
- Keep it conversational
- No special formatting needed

## Example Workflow

```bash
# 1. Extract all dialogues from docs
for doc in ../docs/podcasts/*.md; do
    python scripts/extract_dialogue.py "$doc" \
        -o "../content/podcast-episodes/$(basename "$doc" .md)-dialogue.md"
done

# 2. Generate podcasts from extracted dialogues
python scripts/generate_podcast.py \
    ../content/podcast-episodes/ --batch

# 3. Or generate directly from docs (auto-extract)
python scripts/generate_podcast.py \
    ../docs/podcasts/episode.md
```

## Storage Structure

```
project/
├── docs/podcasts/              # Rich documentation format
│   ├── cloud-providers.md      # Full episode with notes
│   └── platform-economics.md   # Documentation + dialogue
├── content/podcast-episodes/   # Clean dialogue format
│   ├── cloud-providers-dialogue.md
│   └── platform-economics-dialogue.md
└── podcast-generator/
    └── output/                 # Generated audio files
```

This dual-format approach lets you maintain rich documentation for reading while automatically extracting clean dialogue for audio generation!