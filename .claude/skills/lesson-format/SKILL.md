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

### Two Outputs Required

1. **Production Script** (`docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt`):
   - With `[pause]` tags for natural pacing
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

### Step 1: Backup Original Script

```bash
cp docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt.backup
```

### Step 2: Add SSML Pause Tags

**Option A: Automated** (recommended starting point):
```bash
cd podcast-generator
python3 scripts/add_ssml_tags.py ../docs/podcasts/courses/[course-slug]/scripts --file lesson-XX.txt
```

**Option B: Manual**:
- Read through script
- Add `[pause]`, `[pause short]`, `[pause long]` strategically
- Follow placement guidelines above
- Extra attention to teaching moments (questions, analogies, transitions)

### Step 3: Add Pronunciation Tags

**Option A: Automated** (handles common terms):
```bash
cd podcast-generator
python3 scripts/add_pronunciation_tags.py ../docs/podcasts/courses/[course-slug]/scripts --file lesson-XX.txt
```

The script automatically tags:
- All MANDATORY terms from PRONUNCIATION_GUIDE.md
- Common acronyms (AWS, GCP, API, etc.)
- Database names (Postgres, MySQL, Redis)
- Platform names (Kubernetes, Azure, Vercel)

**Option B: Manual** (for edge cases):
- Check PRONUNCIATION_GUIDE.md
- Add `<phoneme>` tags with IPA
- Add `<say-as>` tags for acronyms

### Step 4: Review and Adjust

**Manual Review Checklist**:
- [ ] Pause placement sounds natural (read aloud)
- [ ] All technical terms from PRONUNCIATION_GUIDE tagged
- [ ] Numbers spelled out ("three ninety-seven" not "397")
- [ ] Years pronounced correctly ("twenty twenty-five" not "2025")
- [ ] Teaching moments have appropriate pauses
- [ ] Active recall prompts have longer pauses

**Common Adjustments**:
- Add pauses before/after analogies
- Longer pauses for "pause and think" moments
- Fix numbers: "$397" → "three hundred ninety-seven dollars"
- Fix years: "2025" → "twenty twenty-five"

### Step 5: Validate Formatting

```bash
cd podcast-generator
python3 scripts/ssml_utils.py ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt
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

3. **Add pause tags**:
   - Run automated script: `add_ssml_tags.py`
   - Review and adjust manually
   - Pay attention to teaching moments
   - Aim for 20-30 total pauses

4. **Add pronunciation tags**:
   - Run automated script: `add_pronunciation_tags.py`
   - Check PRONUNCIATION_GUIDE.md for any missed terms
   - Verify all MANDATORY terms tagged

5. **Validate formatting**:
   ```bash
   python3 scripts/ssml_utils.py ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt
   ```

6. **Test TTS generation** (first 5 chunks with Autonoe):
   ```bash
   python3 scripts/generate_lesson.py ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt --max-chunks 5 --voice autonoe
   ```

7. **Create clean version** for episode page:
   ```bash
   python3 scripts/ssml_utils.py --strip ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt
   ```

8. **Report to user**:
   - Formatting complete
   - Number of pauses added
   - Pronunciation tags added
   - Test TTS results (first 5 chunks)
   - Clean version ready for episode page
   - Next step: Use lesson-publish skill

**Remember**: Tags serve the TTS (Autonoe voice), not the reader. Episode pages must be clean and readable. Teaching content benefits from more generous pause usage than conversational podcasts.
