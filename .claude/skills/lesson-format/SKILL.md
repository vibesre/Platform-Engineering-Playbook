---
name: Lesson Format
description: Add SSML pause tags and pronunciation tags to validated lesson scripts, preparing them for TTS generation (Autonoe voice) while creating clean versions for episode pages.
allowed-tools: Read, Edit, Bash, Glob
---

# Lesson Format

Format validated lesson scripts for text-to-speech generation using the Autonoe voice by adding SSML pause tags and pronunciation guidance, while creating clean versions for publication.

## When to Use This Skill

Use this skill when:
- User says: "Format lesson for TTS", "Add SSML tags to course episode"
- Script has been validated (validation report exists)
- Before generating audio with generate_podcast.py (adapted for lessons)

**Prerequisites**: Script must be validated first (use lesson-validate skill).

## Formatting Overview

### NEW: Gemini 2.5 Pro Enhancement (Default)

**IMPORTANT**: As of the latest workflow, lesson scripts are enhanced using **Gemini 2.5 Pro** before SSML formatting:

1. **Enhancement Phase** (NEW - MANDATORY):
   - Use `generate_lesson_with_gemini_pro.py` script
   - Gemini 2.5 Pro adds teaching cadence markers:
     - `(dramatic pause)` before critical information
     - `(pause for reflection)` after rhetorical questions
     - `(pause - let it sink in)` before major concepts
     - `**Bold**` for key technical terms
     - `*Italics*` for conceptual explanations
   - AI-driven placement based on teaching best practices
   - Converts markdown markers → SSML pause tags automatically

2. **SSML Formatting Phase**:
   - Enhancement script auto-converts markers to SSML
   - Adds pronunciation tags for technical terms
   - Outputs production-ready script

### Two Outputs Required

1. **Production Script** (`docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt`):
   - Enhanced with Gemini 2.5 Pro teaching cadence
   - With `[pause]` tags for natural pacing (AI-placed)
   - With `<phoneme>` IPA pronunciation tags
   - With `<say-as>` tags for acronyms
   - Used for TTS generation with Autonoe voice

2. **Episode Page** (`docs/podcasts/courses/[course-slug]/lesson-XX.md`):
   - Clean narration without ANY tags
   - Simple paragraph formatting
   - Ready for reader consumption

### Tag Types

**SSML Pause Tags** (for pacing):
- `[pause short]` → After list items, minor pauses
- `[pause]` → After statistics, rhetorical questions
- `[pause long]` → After dramatic reveals, major transitions

**Pronunciation Tags** (for accuracy):
- `<phoneme alphabet="ipa" ph="...">Term</phoneme>` → IPA pronunciation
- `<say-as interpret-as="characters">AWS</say-as>` → Letter-by-letter

### TTS Voice Configuration

**Single Presenter**: Autonoe voice (Chirp 3 HD)
- Voice ID: `en-US-Chirp3-HD-Autonoe`
- Speed: 0.95x (slightly slower for technical content clarity)
- Stability: High (consistent delivery)

## SSML Pause Tags

### Strategic Placement for Teaching

**After Learning Objectives**:
```
By the end of this lesson, you'll be able to: [pause]
- Explain the Pod abstraction [pause short]
- Create Pod manifests [pause short]
- Debug common Pod issues [pause]
```

**After Key Concepts**:
```
The declarative model is fundamental. [pause] Instead of telling Kubernetes what to do, [pause] you tell it what you want.
```

**Before and After Analogies**:
```
Think of it like a thermostat. [pause] You set the desired temperature, [pause] and the system maintains it automatically.
```

**Around Think-Aloud Sections**:
```
Here's how I'd debug this: [pause long]
First, check the events. [pause short]
Then, examine the logs. [pause short]
Finally, verify the configuration. [pause]
```

**Active Recall Prompts**:
```
Before we continue, pause and think: [pause long] How would YOU structure this?
[Pause 5 seconds]
Here's my recommendation... [pause]
```

**Transitions Between Sections**:
```
Now that we understand X, [pause] let's move on to Y.
```

**Emphasizing Important Points**:
```
This is critical. [pause] If you get this wrong, [pause] your entire cluster could fail.
```

### Pause Tag Guidelines

**DO**:
- Use pauses after questions (give learner time to think)
- Place pauses before major transitions
- Add pauses after statistics for emphasis
- Use longer pauses for active recall moments

**DON'T**:
- Overuse (sounds robotic)
- Pause in the middle of explanations
- Use inconsistently
- Replace natural sentence breathing

**Target**: 20-30 pause tags per 15-minute episode (teaching requires more pauses than conversation)

## Pronunciation Tags

### MANDATORY Pronunciation Tags

Consult `podcast-generator/PRONUNCIATION_GUIDE.md` for complete reference.

**Same terms as podcast episodes PLUS educational terminology**:

**Container/Orchestration**:
- Kubernetes → `<phoneme alphabet="ipa" ph="ˌkubɚˈnɛtɪs">Kubernetes</phoneme>`
- kubectl → `<phoneme alphabet="ipa" ph="ˈkjubˌkʌtəl">kubectl</phoneme>`

**Databases**:
- PostgreSQL → `<phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs">Postgres</phoneme>`
- MySQL → `<phoneme alphabet="ipa" ph="maɪ ˈɛskjuːˈɛl">MySQL</phoneme>`

**Cloud/Platforms**:
- Azure → `<phoneme alphabet="ipa" ph="ˈæʒɚ">Azure</phoneme>`
- Nginx → `<phoneme alphabet="ipa" ph="ˈɛndʒɪn ˈɛks">Nginx</phoneme>`

**Data Formats**:
- YAML → `<phoneme alphabet="ipa" ph="ˈjæməl">YAML</phoneme>`

**Operations**:
- MLOps → `<phoneme alphabet="ipa" ph="ɛm ɛl ɑps">MLOps</phoneme>`
- DevOps → `<phoneme alphabet="ipa" ph="dɛv ɑps">DevOps</phoneme>`

**Acronyms** (say-as tags):
```xml
<say-as interpret-as="characters">AWS</say-as>
<say-as interpret-as="characters">API</say-as>
<say-as interpret-as="characters">CPU</say-as>
<say-as interpret-as="characters">RAM</say-as>
<say-as interpret-as="characters">SLA</say-as>
```

**When to Tag**:
- EVERY occurrence of terms in PRONUNCIATION_GUIDE.md
- First occurrence of less common technical terms
- Any word that TTS commonly mispronounces

## Formatting Workflow

### Step 1: Gemini 2.5 Pro Enhancement (MANDATORY)

**Enhance the script with AI-driven teaching cadence:**

```bash
cd podcast-generator
python3 scripts/generate_lesson_with_gemini_pro.py \
  ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt \
  /tmp/lesson-XX
```

**What this does**:
- Strips existing SSML tags and speaker labels from script
- Sends clean text to Gemini 2.5 Pro in chunks (2000 words each)
- AI adds teaching cadence markers based on instructor persona:
  - `(dramatic pause)` → before critical information
  - `(pause for reflection)` → after rhetorical questions
  - `(pause - let it sink in)` → before major concepts
  - `(pause)` → after key statements
  - `**Bold**` → key technical terms
  - `*Italics*` → conceptual explanations
- Automatically converts markdown markers to SSML:
  - `(dramatic pause)` → `[pause long]`
  - `(pause for reflection)` → `[pause]`
  - `(pause - let it sink in)` → `[pause]`
  - `(pause)` → `[pause short]`
  - Strips `**bold**` and `*italics*` (Chirp 3 uses natural intonation)
- Adds back `Autonoe:` speaker labels
- Saves enhanced script: `/tmp/lesson-XX-gemini-enhanced.txt`

**Instructor Persona** (guides AI placement):
- 15+ years production systems experience
- Measured pacing with strategic pauses
- Emphasizes "why" before "how"
- Uses specific numbers and scenarios
- Pragmatic, honest, patient, systematic

**Review the enhanced script**:
```bash
cat /tmp/lesson-XX-gemini-enhanced.txt
```

**Expected output**:
- Original: ~2000 words
- Enhanced: ~2050 words (5-10% longer with pause markers)
- 20-30 `[pause]` tags strategically placed
- Natural teaching flow with dramatic moments

**Next steps**: Add pronunciation tags and generate audio

### Step 2: Backup Original Script

```bash
cp docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt.backup
```

### Step 3: Add Pronunciation Tags (to enhanced script)

**Work with the Gemini-enhanced script from Step 1** (`/tmp/lesson-XX-gemini-enhanced.txt`):

**Apply pronunciation tags directly to the enhanced script file:**

```bash
cd podcast-generator
python3 scripts/add_pronunciation_tags.py /tmp --file lesson-XX-gemini-enhanced.txt
```

The script automatically tags:
- All MANDATORY terms from PRONUNCIATION_GUIDE.md
- Common acronyms (AWS, GCP, API, etc.)
- Database names (Postgres, MySQL, Redis)
- Platform names (Kubernetes, Azure, Vercel)

**Manual additions** (for edge cases not in PRONUNCIATION_GUIDE.md):
- Check PRONUNCIATION_GUIDE.md for reference
- Add `<phoneme>` tags with IPA for custom terms
- Add `<say-as>` tags for new acronyms

**Result**: Enhanced script with pause tags AND pronunciation tags ready for TTS generation.

### Step 4: Generate Audio with Chirp 3 HD

**Use the fully-tagged enhanced script to generate audio:**

```bash
cd podcast-generator
python3 scripts/generate_podcast.py /tmp/lesson-XX-gemini-enhanced.txt \
  --lesson --episode-id [course-slug]-lesson-XX
```

**What this does**:
- Reads the Gemini-enhanced script with pronunciation tags
- Generates audio using Chirp 3 HD (Autonoe voice, 0.95x speed)
- Saves MP3 and MP4 in `episodes/[episode-id]/`
- Typical duration: 15-20 minutes for lesson content
- Cost: ~$0.20-0.30 per lesson

**Monitor generation**:
```bash
tail -f /tmp/lesson-generation.log
```

**Verify output**:
```bash
ls -lh podcast-generator/episodes/[episode-id]/
ffprobe episodes/[episode-id]/[episode-id].mp3
```

### Step 5: Review Generated Audio

**Listen to the first few minutes**:
```bash
# Play in default audio player
open podcast-generator/episodes/[episode-id]/[episode-id].mp3
```

**Check for**:
- Natural teaching cadence (AI-placed pauses effective?)
- Correct pronunciations (SIGKILL = "sig-kill", Kubernetes = "coo-ber-NET-iss")
- Teaching moments clear (dramatic pauses before critical info)
- Overall flow (authoritative yet approachable)

**If issues found**:
1. Review enhanced script: `cat /tmp/lesson-XX-gemini-enhanced.txt`
2. Identify problems (wrong pause placement, missing pronunciation tag)
3. Manually edit `/tmp/lesson-XX-gemini-enhanced.txt`
4. Regenerate: `python3 scripts/generate_podcast.py /tmp/lesson-XX-gemini-enhanced.txt --lesson --episode-id [id] --force`

### Step 6: Create Clean Episode Page Version

**Strip ALL tags from the enhanced script for the episode page:**

```bash
cd podcast-generator
python3 scripts/ssml_utils.py --strip /tmp/lesson-XX-gemini-enhanced.txt
```

This validates:
- ✓ Proper `[pause]` syntax
- ✓ Correct `<phoneme>` tag structure
- ✓ Valid `<say-as>` tags
- ✓ No unclosed XML tags

### Step 6: Create Clean Episode Page Version

**Strip ALL tags for episode page**:

```bash
cd podcast-generator
python3 scripts/ssml_utils.py --strip ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt > /tmp/clean-lesson.txt
```

This removes:
- `[pause]`, `[pause short]`, `[pause long]`
- `<phoneme>...</phoneme>`
- `<say-as>...</say-as>`
- All other SSML markup

**Format for episode page**:
- Simple paragraph formatting
- No special markers (single presenter, no speaker labels needed)
- Section headers if useful for readability
- Keep natural flow

## Common Formatting Issues

### Issue 1: Numbers
**Wrong**: "Costs $397 per month"
**Right**: "Costs three hundred ninety-seven dollars per month"

### Issue 2: Duplicate Pronunciation Tags
**Acceptable**: Tag every occurrence (TTS processes line-by-line, benefits from consistent tags)

### Issue 3: Nested Tags
**Wrong**:
```xml
<phoneme alphabet="ipa" ph="..."><say-as interpret-as="characters">API</say-as></phoneme>
```

**Right**: Use ONE tag type per term

### Issue 4: Missing Space After Pause Tag
**Wrong**: `[pause]Now let's move on...`
**Right**: `[pause] Now let's move on...`

### Issue 5: Teaching Moment Pauses
**Wrong**: "Pause and think. Here's the answer."
**Right**: "Pause and think. [pause long] Here's the answer."

## Testing TTS Output

After formatting, test a sample:

```bash
cd podcast-generator
# Test just the first 5 chunks with Autonoe voice
python3 scripts/generate_lesson.py ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt --max-chunks 5 --voice autonoe
```

**Listen for**:
- Natural pacing (pauses effective for teaching?)
- Correct pronunciations (tags working?)
- Teaching moments clear (questions, analogies distinct?)
- Overall flow (conversational yet authoritative?)

**If issues**:
- Adjust pause placement (especially teaching moments)
- Fix pronunciation tags
- Regenerate chunks selectively

## Output Checklist

Before moving to publishing:

**Production Script** (`scripts/lesson-XX.txt`):
- [ ] Has `[pause]` tags (20-30 total)
- [ ] Has pronunciation tags on all MANDATORY terms
- [ ] Numbers spelled out
- [ ] Years written phonetically
- [ ] Teaching moments have appropriate pauses
- [ ] Active recall prompts have longer pauses
- [ ] Validated with ssml_utils.py
- [ ] Test TTS generation successful with Autonoe voice

**Episode Page Content** (for later publishing):
- [ ] Clean narration (no SSML tags)
- [ ] Simple paragraph formatting
- [ ] Section headers if helpful
- [ ] Ready to paste into episode markdown

## Voice-Specific Notes

**Autonoe Voice Characteristics**:
- Clear and articulate
- Professional yet approachable
- Good for technical content
- Slightly slower pace (0.95x) helps with comprehension

**Optimization for Autonoe**:
- Use pauses generously (voice handles them well)
- Technical terms benefit from pronunciation tags
- Analogies and explanations come across naturally
- Think-aloud sections sound authentic

## Automation Scripts Reference

### add_ssml_tags.py
**Purpose**: Automatically add pause tags based on sentence structure

**Usage**:
```bash
python3 scripts/add_ssml_tags.py ../docs/podcasts/courses/[course-slug]/scripts --file lesson-XX.txt
```

**What it does**:
- Adds `[pause]` after periods, question marks
- Adds `[pause short]` in lists
- Adds `[pause long]` after "pause and think" patterns

### add_pronunciation_tags.py
**Purpose**: Automatically tag technical terms from PRONUNCIATION_GUIDE.md

**Usage**:
```bash
python3 scripts/add_pronunciation_tags.py ../docs/podcasts/courses/[course-slug]/scripts --file lesson-XX.txt
```

**What it does**:
- Tags Kubernetes, Postgres, Azure, etc. with IPA
- Tags AWS, GCP, API, etc. with say-as
- Preserves existing tags (won't duplicate)

### ssml_utils.py
**Purpose**: Validate and strip SSML tags

**Usage**:
```bash
# Validate tags
python3 scripts/ssml_utils.py ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt

# Strip tags for episode page
python3 scripts/ssml_utils.py --strip ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt
```

---

## Instructions for Claude

When this skill is invoked:

1. **Verify script is validated**:
   - Check for validation report
   - If not validated, use lesson-validate skill first

2. **Backup original script**:
   ```bash
   cp docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt.backup
   ```

3. **Run Gemini 2.5 Pro Enhancement** (MANDATORY):
   ```bash
   cd podcast-generator
   python3 scripts/generate_lesson_with_gemini_pro.py \
     ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt \
     /tmp/lesson-XX
   ```
   - This creates `/tmp/lesson-XX-gemini-enhanced.txt` with AI-placed pause tags
   - Expected output: Original + 5-10% words, 20-30 pause tags

4. **Add pronunciation tags** to enhanced script:
   ```bash
   cd podcast-generator
   python3 scripts/add_pronunciation_tags.py /tmp --file lesson-XX-gemini-enhanced.txt
   ```
   - Check PRONUNCIATION_GUIDE.md for any missed terms
   - Verify all MANDATORY terms tagged (Kubernetes, SIGKILL, etc.)

5. **Generate audio** with Chirp 3 HD:
   ```bash
   cd podcast-generator
   python3 scripts/generate_podcast.py /tmp/lesson-XX-gemini-enhanced.txt \
     --lesson --episode-id [course-slug]-lesson-XX
   ```
   - Monitor with: `tail -f /tmp/lesson-generation.log`
   - Typical duration: 15-20 minutes
   - Cost: ~$0.20-0.30 per lesson

6. **Review generated audio**:
   ```bash
   open podcast-generator/episodes/[episode-id]/[episode-id].mp3
   ```
   - Listen to first few minutes
   - Check: Natural cadence, correct pronunciations, teaching moments clear
   - If issues: Edit `/tmp/lesson-XX-gemini-enhanced.txt` and regenerate with `--force`

7. **Create clean version** for episode page:
   ```bash
   python3 scripts/ssml_utils.py --strip /tmp/lesson-XX-gemini-enhanced.txt > /tmp/clean-lesson.txt
   ```

8. **Report to user**:
   - Gemini enhancement complete (X words → Y words, Z pause tags)
   - Pronunciation tags added (list critical terms)
   - Audio generation complete (duration, file size)
   - Quality check results (cadence, pronunciations)
   - Clean version ready for episode page
   - Next step: Use lesson-publish skill

**Key Changes from Previous Workflow**:
- **NEW Step 3**: Gemini 2.5 Pro enhancement is now MANDATORY before pronunciation tagging
- Pause tags are AI-placed, not manually added
- Work with `/tmp/lesson-XX-gemini-enhanced.txt` instead of original script
- Audio generation happens in Step 5 (not separate tool)

**Remember**: The Gemini-enhanced workflow produces superior teaching cadence with AI-driven pause placement based on instructor persona. Tags serve the TTS (Autonoe voice), not the reader. Episode pages must be clean and readable.
