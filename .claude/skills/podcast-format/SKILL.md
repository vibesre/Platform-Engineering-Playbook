---
name: Podcast Format
description: Add SSML pause tags and pronunciation tags to validated scripts, preparing them for TTS generation while creating clean versions for episode pages.
allowed-tools: Read, Edit, Bash, Glob
---

# Podcast Format

Format validated podcast scripts for text-to-speech generation by adding SSML pause tags and pronunciation guidance, while creating clean versions for publication.

## When to Use This Skill

Use this skill when:
- User says: "Format podcast for TTS", "Add SSML tags to podcast"
- Script has been validated (validation report exists)
- Before generating audio with generate_podcast.py

**Prerequisites**: Script must be validated first (use podcast-validate skill).

## Formatting Overview

### Two Outputs Required

1. **Production Script** (`docs/podcasts/scripts/00XXX-name.txt`):
   - With `[pause]` tags for natural pacing
   - With `<phoneme>` IPA pronunciation tags
   - With `<say-as>` tags for acronyms
   - Used for TTS generation

2. **Episode Page** (`docs/podcasts/00XXX-name.md`):
   - Clean dialogue without ANY tags
   - Formatted with `**Jordan**:` and `**Alex**:`
   - Ready for reader consumption

### Tag Types

**SSML Pause Tags** (for pacing):
- `[pause short]` → After list items, minor pauses
- `[pause]` → After statistics, rhetorical questions
- `[pause long]` → After dramatic reveals, major transitions

**Pronunciation Tags** (for accuracy):
- `<phoneme alphabet="ipa" ph="...">Term</phoneme>` → IPA pronunciation
- `<say-as interpret-as="characters">AWS</say-as>` → Letter-by-letter

## SSML Pause Tags

### Strategic Placement

**After Statistics/Percentages**:
```
Alex: Team efficiency improved 50%, [pause] but here's the stat that blew my mind - [pause] false positive alerts dropped 96%.
```

**After Rhetorical Questions**:
```
Jordan: What's the catch? [pause] Well, there are a few things to consider.
```

**After Dramatic Reveals**:
```
Alex: And here's the kicker - [pause] the "expensive" option saved them one hundred seventy-five thousand dollars per year.
```

**After Contrast Words**:
```
Jordan: Most teams start with managed services. But, [pause] there's a point where you need more control.
```

**In Lists**:
```
Alex: First, [pause short] reduce deployment time. Second, [pause short] improve observability. Third, [pause] enable team autonomy.
```

**After Emphatic Statements**:
```
Jordan: That's transformational. [pause] And it's happening right now across the industry.
```

### Pause Tag Guidelines

**DO**:
- Use pauses to create natural rhythm
- Place after key insights for emphasis
- Use before important transitions
- Help TTS "breathe" naturally
- **MANDATORY**: Add `[pause long]` at the very end of the script (after final dialogue, before outro MP3) to prevent jarring transition into outro

**DON'T**:
- Overuse (sounds robotic)
- Pause mid-sentence without reason
- Use inconsistently (confuses flow)
- Replace natural sentence breaks

**Target**: 15-25 pause tags per 12-minute episode

**Ending Silence** (REQUIRED):
Every episode MUST end with `[pause long]` tag (~1 second silence) after the final line of dialogue. This prevents jarring transitions when the outro MP3 begins. The generate_podcast.py script automatically appends intro.mp3 and outro.mp3, so the script should end cleanly with a pause tag.

## Pronunciation Tags

### MANDATORY Pronunciation Tags

Consult `podcast-generator/PRONUNCIATION_GUIDE.md` for complete reference.

**Common Terms That MUST Be Tagged**:

**Container/Orchestration**:
- Kubernetes → `<phoneme alphabet="ipa" ph="ˌkubɚˈnɛtɪs">Kubernetes</phoneme>`
- K8s → `<phoneme alphabet="ipa" ph="keɪ eɪts">K8s</phoneme>`
- kubectl → `<phoneme alphabet="ipa" ph="ˈkjubˌkʌtəl">kubectl</phoneme>`

**Databases**:
- PostgreSQL/Postgres → `<phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs">Postgres</phoneme>`
- MySQL → `<phoneme alphabet="ipa" ph="maɪ ˈɛskjuːˈɛl">MySQL</phoneme>`
- Redis → `<phoneme alphabet="ipa" ph="ˈrɛdɪs">Redis</phoneme>`

**Cloud/Platforms**:
- Azure → `<phoneme alphabet="ipa" ph="ˈæʒɚ">Azure</phoneme>`
- Heroku → `<phoneme alphabet="ipa" ph="hɛˈroʊkuː">Heroku</phoneme>`
- Vercel → `<phoneme alphabet="ipa" ph="ˈvɜrsəl">Vercel</phoneme>`
- Nginx → `<phoneme alphabet="ipa" ph="ˈɛndʒɪn ˈɛks">Nginx</phoneme>`

**Data Formats**:
- YAML → `<phoneme alphabet="ipa" ph="ˈjæməl">YAML</phoneme>`

**Operations/Security**:
- MLOps → `<phoneme alphabet="ipa" ph="ɛm ɛl ɑps">MLOps</phoneme>`
- AIOps → `<phoneme alphabet="ipa" ph="eɪ aɪ ɑps">AIOps</phoneme>`
- DevOps → `<phoneme alphabet="ipa" ph="dɛv ɑps">DevOps</phoneme>`
- SOC 2 → "sock two" (no tag needed)
- HIPAA → "hippa" (no tag needed)
- RBAC → "arr bak" (no tag needed)

**Acronyms (say-as tags)**:
```xml
<say-as interpret-as="characters">AWS</say-as>
<say-as interpret-as="characters">GCP</say-as>
<say-as interpret-as="characters">API</say-as>
<say-as interpret-as="characters">GPU</say-as>
<say-as interpret-as="characters">CPU</say-as>
<say-as interpret-as="characters">RAM</say-as>
<say-as interpret-as="characters">SLA</say-as>
<say-as interpret-as="characters">SLO</say-as>
```

**When to Tag**:
- EVERY occurrence of terms in PRONUNCIATION_GUIDE.md
- First occurrence of less common technical terms
- Any word that TTS commonly mispronounces

### Testing Pronunciations

If uncertain about pronunciation:
1. Check `podcast-generator/PRONUNCIATION_GUIDE.md`
2. Test with small TTS sample
3. Add to guide if new term

## Formatting Workflow

### Step 1: Backup Original Script
```bash
cp docs/podcasts/scripts/00XXX-name.txt docs/podcasts/scripts/00XXX-name.txt.backup
```

### Step 2: Add SSML Pause Tags

**Option A: Automated** (recommended starting point):
```bash
cd podcast-generator
python3 scripts/add_ssml_tags.py ../docs/podcasts/scripts --file 00XXX-name.txt
```

**Option B: Manual**:
- Read through script
- Add `[pause]`, `[pause short]`, `[pause long]` strategically
- Follow placement guidelines above

### Step 3: Add Pronunciation Tags

**Option A: Automated** (handles common terms):
```bash
cd podcast-generator
python3 scripts/add_pronunciation_tags.py ../docs/podcasts/scripts --file 00XXX-name.txt
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
- [ ] Speaker names are `Jordan:` and `Alex:` (not Speaker 1/2)

**Common Adjustments**:
- Remove excessive pauses (sounds robotic)
- Add pauses before key insights
- Fix numbers: "$397" → "three hundred ninety-seven dollars"
- Fix years: "2025" → "twenty twenty-five"

### Step 5: Validate Formatting

```bash
cd podcast-generator
python3 scripts/ssml_utils.py ../docs/podcasts/scripts/00XXX-name.txt
```

This validates:
- ✓ Proper `[pause]` syntax
- ✓ Correct `<phoneme>` tag structure
- ✓ Valid `<say-as>` tags
- ✓ No unclosed XML tags
- ✓ Speaker names correct

### Step 6: Create Clean Episode Page Version

**Strip ALL tags for episode page**:

```bash
cd podcast-generator
python3 scripts/ssml_utils.py --strip ../docs/podcasts/scripts/00XXX-name.txt > /tmp/clean-dialogue.txt
```

This removes:
- `[pause]`, `[pause short]`, `[pause long]`
- `<phoneme>...</phoneme>`
- `<say-as>...</say-as>`
- All other SSML markup

**Format for episode page**:
- Change `Jordan:` → `**Jordan**:`
- Change `Alex:` → `**Alex**:`
- Keep blank lines between speakers

## Common Formatting Issues

### Issue 1: Numbers
**Wrong**: "Costs $397 per month"
**Right**: "Costs three hundred ninety-seven dollars per month"

### Issue 2: Duplicate Pronunciation Tags
**Wrong**:
```xml
<phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs">Postgres</phoneme> is great.
Later... <phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs">Postgres</phoneme> again.
```

**Acceptable**: Tag every occurrence (TTS processes line-by-line)

### Issue 3: Nested Tags
**Wrong**:
```xml
<phoneme alphabet="ipa" ph="..."><say-as interpret-as="characters">API</say-as></phoneme>
```

**Right**: Use ONE tag type per term

### Issue 4: Missing Space After Pause Tag
**Wrong**: `[pause]Jordan: Next topic`
**Right**: `[pause] Jordan: Next topic`

## Testing TTS Output

After formatting, test a sample:

```bash
cd podcast-generator
# Test just the first 5 chunks
python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00XXX-name.txt --max-chunks 5
```

**Listen for**:
- Natural pacing (pauses effective?)
- Correct pronunciations (tags working?)
- Overall flow (conversational?)

**If issues**:
- Adjust pause placement
- Fix pronunciation tags
- Regenerate chunks selectively

## Output Checklist

Before moving to publishing:

**Production Script** (`docs/podcasts/scripts/00XXX-name.txt`):
- [ ] Has `[pause]` tags (15-25 total)
- [ ] Has pronunciation tags on all MANDATORY terms
- [ ] Numbers spelled out
- [ ] Years written phonetically
- [ ] Speaker names: `Jordan:` and `Alex:`
- [ ] Validated with ssml_utils.py
- [ ] Test TTS generation successful

**Episode Page Content** (for later publishing):
- [ ] Clean dialogue (no SSML tags)
- [ ] Speaker names: `**Jordan**:` and `**Alex**:`
- [ ] Blank lines between speakers
- [ ] Ready to paste into episode markdown

## Automation Scripts Reference

### add_ssml_tags.py
**Purpose**: Automatically add pause tags based on sentence structure

**Usage**:
```bash
python3 scripts/add_ssml_tags.py ../docs/podcasts/scripts [--file 00XXX-name.txt]
```

**What it does**:
- Adds `[pause]` after periods, question marks
- Adds `[pause short]` in lists
- Adds `[pause long]` after dramatic statements

### add_pronunciation_tags.py
**Purpose**: Automatically tag technical terms from PRONUNCIATION_GUIDE.md

**Usage**:
```bash
python3 scripts/add_pronunciation_tags.py ../docs/podcasts/scripts [--file 00XXX-name.txt]
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
python3 scripts/ssml_utils.py ../docs/podcasts/scripts/00XXX-name.txt

# Strip tags for episode page
python3 scripts/ssml_utils.py --strip ../docs/podcasts/scripts/00XXX-name.txt
```

---

## Instructions for Claude

When this skill is invoked:

1. **Verify script is validated**:
   - Check for validation report
   - If not validated, use podcast-validate skill first

2. **Backup original script**:
   ```bash
   cp docs/podcasts/scripts/00XXX-name.txt docs/podcasts/scripts/00XXX-name.txt.backup
   ```

3. **Add pause tags**:
   - Run automated script: `add_ssml_tags.py`
   - Review and adjust manually
   - Aim for 15-25 total pauses
   - **CRITICAL**: Manually add `[pause long]` at the very end of the script (after final dialogue line)

4. **Add pronunciation tags**:
   - Run automated script: `add_pronunciation_tags.py`
   - Check PRONUNCIATION_GUIDE.md for any missed terms
   - Verify all MANDATORY terms tagged

5. **Validate formatting**:
   ```bash
   python3 scripts/ssml_utils.py ../docs/podcasts/scripts/00XXX-name.txt
   ```

6. **Test TTS generation** (first 5 chunks):
   ```bash
   python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00XXX-name.txt --max-chunks 5
   ```

7. **Create clean version** for episode page:
   ```bash
   python3 scripts/ssml_utils.py --strip ../docs/podcasts/scripts/00XXX-name.txt
   ```

8. **Report to user**:
   - Formatting complete
   - Number of pauses added
   - Pronunciation tags added
   - Test TTS results (first 5 chunks)
   - Clean version ready for episode page
   - Next step: Use podcast-publish skill

**Remember**: Tags serve the TTS, not the reader. Episode pages must be clean and readable.
