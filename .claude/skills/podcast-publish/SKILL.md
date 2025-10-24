---
name: Podcast Publish
description: Complete podcast publishing workflow - generate audio/video, create episode page with frontmatter, add cross-links, update index, verify URLs.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Podcast Publish

Execute the complete publishing workflow for podcast episodes, from audio generation to website publication with all required metadata, cross-links, and index updates.

## When to Use This Skill

Use this skill when:
- User says: "Publish podcast episode", "Generate podcast audio", "Create episode page"
- Script has been validated and formatted (SSML/pronunciation tags added)
- Ready to publish the complete episode

**Prerequisites**:
- ✅ Script validated (podcast-validate)
- ✅ Script formatted (podcast-format)
- ✅ Script in `docs/podcasts/scripts/00XXX-name.txt`

## Publishing Workflow

### Phase 1: Generate Audio & Video

**Command**:
```bash
cd podcast-generator
python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00XXX-name.txt
```

**What Happens**:
1. **Text-to-Speech Generation**:
   - Script chunked at speaker boundaries
   - SSML tags converted to proper format
   - Pronunciation tags applied
   - Jordan voice: `en-US-Chirp3-HD-Kore` (0.95x speed)
   - Alex voice: `en-US-Chirp3-HD-Algieba` (1.0x speed)

2. **Audio Assembly**:
   - Intro MP3 prepended (welcome message)
   - Episode chunks stitched together
   - Outro MP3 appended (thanks, call-to-action)
   - Audio normalized

3. **Video Generation** (automatic, lockstep with audio):
   - MP4 video created with looping background
   - 1920x1080 Full HD resolution
   - Synchronized with audio
   - Suitable for YouTube, social media

4. **Outputs Created** (`podcast-generator/output_latest/`):
   - `00XXX-episode-name.mp3` (audio)
   - `00XXX-episode-name.mp4` (video)
   - `00XXX-episode-name.txt` (metadata)

**Estimated Time**:
- Small episode (10 min): ~5 minutes generation
- Average episode (12-15 min): ~8 minutes generation
- Large episode (18 min): ~12 minutes generation

### Phase 2: Create Episode Page

**Location**: `docs/podcasts/00XXX-episode-name.md`

**CRITICAL**: Episode number must match script filename.

**Required Frontmatter**:
```yaml
---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #XXX: Episode Title"
slug: 00XXX-episode-name
---
```

**Episode Number Rules**:
- Use 5-digit prefix (00001, 00002, ..., 00099, 00100)
- Must match script filename
- Example: Script `00005-paas-showdown.txt` → Page `00005-paas-showdown.md`
- Sidebar label shows episode number: `#005:`
- URL will be `/podcasts/00005-paas-showdown`

**Page Header Format**:
```markdown
# [Full Episode Title]

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** [X minutes]
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/related-post-slug)**: Brief description highlighting written format. (IF blog post exists)

---
```

**Content Sections**:
- Copy dialogue from formatted script
- **Strip ALL SSML tags** (use `ssml_utils.py --strip`)
- Change `Jordan:` → `**Jordan**:`
- Change `Alex:` → `**Alex**:`
- Keep section headers from script
- Maintain blank lines between speakers

**Complete Episode Page Template**:
```markdown
---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #XXX: Episode Title"
slug: 00XXX-episode-name
---

# [Full Episode Title] - [Subtitle]

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** [X minutes]
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/related-post-slug)**: Description of blog post. (IF EXISTS)

---

### [Section Title]

**Jordan**: Dialogue here.

**Alex**: Response here.

### [Next Section Title]

**Jordan**: More dialogue.

**Alex**: More response.

[Continue with all sections...]
```

### Phase 3: Complete Metadata File

**Location**: `podcast-generator/output_latest/00XXX-episode-name.txt`

**Auto-Generated During Audio Creation** with:
- ✅ Title extracted from filename
- ✅ URL with episode number prefix
- ✅ **Duration from actual MP3** in hh:mm:ss format (via ffprobe)
- ⚠️ Description and Summary are **placeholders** - must be filled in

**Required Format**:
```
Title: [EXACT H1 from episode page]

Description:
[2-3 engaging sentences with hook and call-to-action]

🔗 Full episode page: https://platformengineeringplaybook.com/podcasts/00XXX-episode-name

📝 See a mistake or have insights to add? This podcast is community-driven - open a PR on GitHub!

Summary:
• [Concrete takeaway 1]
• [Concrete takeaway 2]
• [Concrete takeaway 3]
• [Concrete takeaway 4]
• [Concrete takeaway 5]

Duration: hh:mm:ss
Speakers: Alex and Jordan
Target Audience: Senior platform engineers, SREs, DevOps engineers with 5+ years experience
```

**CRITICAL: Fill In Placeholders**:
- [ ] **Description**: 2-3 engaging sentences with specific numbers/insights
- [ ] **Summary**: 5-7 concrete, actionable takeaways (not generic)
- [ ] Title EXACTLY matches episode page H1
- [ ] URL uses numbered slug format: `/podcasts/00XXX-episode-name`
- [ ] Duration is actual MP3 length in hh:mm:ss (auto-generated)

### Phase 4: Add Cross-Links

**If Related Blog Post Exists**:

**In Episode Page** (after duration/speakers):
```markdown
> 📝 **Read the [full blog post](/blog/blog-post-slug)**: Brief description highlighting written format and comprehensive analysis.
```

**In Blog Post** (after intro, before main content):
```markdown
> 🎙️ **Listen to the podcast episode**: [Episode Title](/podcasts/00XXX-episode-name) - Brief description highlighting conversation format and key topics.
```

**Cross-Link Checklist**:
- [ ] Episode page links to blog (if blog exists)
- [ ] Blog post links to episode (if blog exists)
- [ ] Links use emoji indicators (🎙️ podcast, 📝 blog)
- [ ] Descriptions are unique and value-focused
- [ ] URLs are correct and use numbered format

### Phase 5: Update Podcast Index

**File**: `docs/podcasts/index.md`

**Add Entry** (at top of episode list):
```markdown
- 🎙️ **[#XXX: Episode Title](/podcasts/00XXX-episode-name)** ([X min]) - Brief one-line description
```

**Format Requirements**:
- Episodes listed newest first
- Episode number in title
- Duration in parentheses
- One-line description (not full description)
- Link uses numbered slug format

**Example**:
```markdown
## Episodes

- 🎙️ **[#005: PaaS Showdown 2025](/podcasts/00005-paas-showdown)** (14 min) - Compare Flightcontrol, Vercel, Railway with real pricing and decision frameworks
- 🎙️ **[#004: Platform Economics](/podcasts/00004-platform-economics)** (12 min) - Hidden costs and TCO analysis for platform decisions
```

### Phase 6: Build & Verify

**Build Site**:
```bash
npm run build
```

**Check for Errors**:
- MDX syntax errors
- Broken internal links
- Missing files
- Frontmatter issues

**Verify URLs**:
```bash
# Check episode page exists at correct URL
ls -la build/podcasts/00XXX-episode-name/index.html

# Verify no old URL format (without episode number)
ls -la build/podcasts/episode-name/index.html  # Should NOT exist
```

**Manual Verification**:
```bash
npm run start
# Visit: http://localhost:3000/podcasts/00XXX-episode-name
```

Check:
- [ ] Episode page loads correctly
- [ ] Audio player shows (if embedded)
- [ ] Cross-links work
- [ ] Sidebar shows episode with number
- [ ] Frontmatter renders correctly

### Phase 7: Pre-Publication Checklist

Complete this checklist before considering episode published:

**Files Created**:
- [ ] Audio: `podcast-generator/output_latest/00XXX-name.mp3`
- [ ] Video: `podcast-generator/output_latest/00XXX-name.mp4`
- [ ] Metadata: `podcast-generator/output_latest/00XXX-name.txt`
- [ ] Episode page: `docs/podcasts/00XXX-name.md`
- [ ] Script: `docs/podcasts/scripts/00XXX-name.txt` (with tags)

**Episode Page**:
- [ ] Frontmatter complete with episode number
- [ ] Slug matches filename: `slug: 00XXX-name`
- [ ] Sidebar label: `🎙️ #XXX: Title`
- [ ] `<GitHubButtons />` present
- [ ] Duration, speakers, target audience listed
- [ ] Dialogue clean (no SSML tags)
- [ ] Speaker names bold: `**Jordan**:`, `**Alex**:`

**Metadata File**:
- [ ] Title matches episode page H1 exactly
- [ ] URL uses numbered format: `/podcasts/00XXX-name`
- [ ] Description engaging with call-to-action
- [ ] Summary has 5+ concrete takeaways
- [ ] Duration matches audio length

**Cross-Links** (if applicable):
- [ ] Episode links to blog post
- [ ] Blog post links to episode
- [ ] Links tested and working

**Index Updated**:
- [ ] Episode added to `docs/podcasts/index.md`
- [ ] Listed at top (newest first)
- [ ] Episode number in title
- [ ] Duration included
- [ ] Link uses numbered slug

**Build Verification**:
- [ ] `npm run build` succeeds
- [ ] No MDX errors
- [ ] No broken links
- [ ] Episode URL works: `/podcasts/00XXX-name`
- [ ] Sidebar shows episode

**Audio/Video Quality**:
- [ ] MP3 plays correctly
- [ ] MP4 video synced with audio
- [ ] Intro/outro included
- [ ] Pronunciations correct
- [ ] Natural pacing (pauses effective)

## Common Issues & Fixes

### Issue 1: Episode Number Mismatch
**Problem**: Script is `00005-topic.txt`, page is `00004-topic.md`
**Fix**: Rename files to match, update frontmatter slug

### Issue 2: Missing Cross-Links
**Problem**: Blog post exists but no link in episode page
**Fix**: Add cross-link blockquote in both directions

### Issue 3: Old URL Format
**Problem**: Slug is `topic-name` instead of `00XXX-topic-name`
**Fix**: Update slug in frontmatter to include episode number

### Issue 4: Metadata Title Mismatch
**Problem**: Metadata .txt title differs from episode page H1
**Fix**: Copy H1 exactly into metadata file

### Issue 5: Build Fails
**Problem**: MDX syntax errors or broken links
**Fix**: Check `npm run build` output, fix specific errors

### Issue 6: Tags Visible on Episode Page
**Problem**: Dialogue shows `[pause]` or `<phoneme>` tags
**Fix**: Use `ssml_utils.py --strip` before copying to episode page

## Regenerating Episodes

**For Small Edits** (pronunciation fixes, single lines):
```bash
# Selective regeneration (only changed chunks)
python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00XXX-name.txt
```

**For Major Changes** (voice settings, complete rewrite):
```bash
# Force regeneration (all chunks)
python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00XXX-name.txt --force
```

**Cost Difference**:
- Selective: ~$0.002 for 1 chunk (200 words)
- Force: ~$0.20 for full episode (100+ chunks)

**After Regeneration**:
- Audio/video/metadata updated in `output_latest/`
- Previous version archived in `output_history/`
- Episode page only needs updating if dialogue changed

## Workflow Summary

```
1. GENERATE AUDIO/VIDEO
   ↓
2. CREATE EPISODE PAGE
   ↓
3. VERIFY METADATA
   ↓
4. ADD CROSS-LINKS (if blog exists)
   ↓
5. UPDATE INDEX
   ↓
6. BUILD & VERIFY
   ↓
7. COMPLETE CHECKLIST
   ↓
8. EPISODE PUBLISHED ✓
```

---

## Instructions for Claude

When this skill is invoked:

1. **Verify prerequisites**:
   - Script validated (check for validation report)
   - Script formatted (check for SSML tags)
   - Script location: `docs/podcasts/scripts/00XXX-name.txt`

2. **Determine episode number**:
   ```bash
   ls -la docs/podcasts/scripts/ | grep -E "^[0-9]{5}-"
   ```
   Extract number from filename.

3. **Generate audio and video**:
   ```bash
   cd podcast-generator
   python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00XXX-name.txt
   ```
   Monitor output for errors.

4. **Create episode page**:
   - Filename: `docs/podcasts/00XXX-name.md`
   - Frontmatter with episode number
   - Strip SSML tags from dialogue
   - Format speaker names

5. **Update metadata duration**:
   - Get actual duration from mp3:
     ```bash
     ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \
       podcast-generator/output_latest/00XXX-name.mp3
     ```
   - Convert seconds to MM:SS format
   - Update `Duration:` field in `podcast-generator/output_latest/00XXX-name.txt`
   - Replace estimated duration with actual runtime

6. **Verify metadata file**:
   - Check `output_latest/00XXX-name.txt`
   - Title matches episode page H1
   - URL uses numbered format
   - Duration is actual mp3 length (not estimated)

7. **Add cross-links** (if related blog exists):
   - Episode page → blog post
   - Blog post → episode page

8. **Update index**:
   - Add to `docs/podcasts/index.md`
   - Top of list, with episode number

9. **Build and verify**:
   ```bash
   npm run build
   ```
   Check for errors.

10. **Complete checklist** (all items)

11. **Report to user**:
    - Episode published successfully
    - URLs: `/podcasts/00XXX-name`
    - Audio/video locations
    - Next steps (if any)

**Remember**: Episode numbers create permanent, shareable URLs. Once published, don't change the number.
