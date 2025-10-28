---
name: Lesson Publish
description: Complete lesson publishing workflow - generate audio/video with Autonoe voice, create episode page, update course index, add to podcast feed, verify URLs and navigation.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Lesson Publish

Execute the complete publishing workflow for course lesson episodes, from audio generation to website publication with course navigation, podcast feed integration, and all required metadata.

## When to Use This Skill

Use this skill when:
- User says: "Publish lesson", "Generate course audio", "Publish episode"
- Script has been validated and formatted (SSML/pronunciation tags added)
- Ready to publish the complete episode

**Prerequisites**:
- ✅ Script validated (lesson-validate)
- ✅ Script formatted (lesson-format)
- ✅ Script in `docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt`
- ✅ Course curriculum exists (`docs/podcasts/courses/[course-slug]/index.md`)

## Publishing Workflow

### Phase 1: Determine Episode Number

**CRITICAL**: Course lessons must use globally unique 5-digit episode IDs in the podcast feed.

**How to Determine Episode Number**:
1. Check the **main podcast index** at `docs/podcasts/index.md` to find the latest episode number
2. Lessons get sequential episode IDs just like regular podcast episodes
3. Example: If last podcast is 00008, first lesson is 00009, second lesson is 00010

**Episode ID Format**: `00009-[course-slug]-lesson-01`
- 5-digit prefix (00009, 00010, 00011, etc.)
- Course slug (e.g., `kubernetes-production-mastery`)
- Lesson number with two digits (lesson-01, lesson-02, etc.)

**Why**: Lessons appear in the main podcast feed chronologically alongside regular episodes. The 5-digit prefix ensures proper sorting and uniqueness across all content types.

### Phase 2: Generate Audio & Video

**Command**:
```bash
cd podcast-generator
python3 scripts/generate_podcast.py ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt --lesson --episode-id 00009-[course-slug]-lesson-XX
```

**CRITICAL**: The `--lesson` flag is required for educational content. It enables:
- Lesson-specific chunking (150-300 words vs 80-150 for podcasts)
- Longer chunks avoid breaking mid-concept for single-speaker content
- Autonoe voice settings optimized for educational delivery

**What Happens**:
1. **Text-to-Speech Generation**:
   - Script chunked at natural pedagogical boundaries (longer chunks)
   - SSML tags converted to proper format
   - Pronunciation tags applied
   - Autonoe voice: `en-US-Chirp3-HD-Autonoe` (1.0x speed for conversational teaching)

2. **Audio Assembly**:
   - Intro MP3 prepended (course-specific or generic)
   - Lesson chunks stitched together
   - Outro MP3 appended
   - Audio normalized

3. **Video Generation** (automatic, lockstep with audio):
   - MP4 video created with course-specific background (or generic)
   - 1920x1080 Full HD resolution
   - Synchronized with audio
   - Suitable for YouTube, social media

4. **Outputs Created** (`podcast-generator/episodes/00009-[course-slug]-lesson-XX/`):
   - `00009-[course-slug]-lesson-XX.mp3` (audio)
   - `00009-[course-slug]-lesson-XX.mp4` (video)
   - `00009-[course-slug]-lesson-XX.txt` (metadata)

**Directory Structure**:
```
podcast-generator/episodes/
├── 00008-gcp-state-of-the-union-2025/       # Regular podcast
├── 00009-kubernetes-production-mastery-lesson-01/  # Course lesson
├── 00010-kubernetes-production-mastery-lesson-02/  # Course lesson
└── 00011-some-future-content/
```

All files use the full episode ID as their filename for consistency.

**Estimated Time**:
- 12-15 min lesson: ~8 minutes generation
- Larger lessons: proportionally longer

### Phase 3: Create Episode Page

**Location**: `docs/podcasts/courses/[course-slug]/lesson-XX.md`

**CRITICAL**:
- Episode page uses lesson number (lesson-01, lesson-02) within course directory
- Episode ID for generation uses global number (00009, 00010) for podcast feed
- These are different! Don't confuse them.

**Required Frontmatter**:
```yaml
---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 #XX: Lesson Title"
slug: courses/[course-slug]/lesson-XX
---
```

**Episode Page Header Format**:
```markdown
# Lesson XX: [Title]

## [Course Name]

<GitHubButtons />

**Course**: [Link to course index](/podcasts/courses/[course-slug])
**Episode**: XX of N
**Duration**: X minutes
**Presenter**: [Fictional persona name]
**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

## Learning Objectives

By the end of this lesson, you'll be able to:
- [Objective 1]
- [Objective 2]
- [Objective 3]

## Prerequisites

- [Prerequisite 1]
- [Prerequisite 2]
- [Link to previous lesson if sequential]

---
```

**Content Sections**:
- Copy clean narration from formatted script (SSML tags stripped)
- Simple paragraph formatting (no speaker labels for single presenter)
- Add section headers if helpful for readability (## Section Name)
- Maintain natural flow

**Navigation Footer**:
```markdown
---

## Navigation

⬅️ **Previous**: [Lesson XX-1: Title](./lesson-XX-1) | **Next**: [Lesson XX+1: Title](./lesson-XX+1) ➡️

📚 **[Back to Course Overview](./index)**

---

**Questions or feedback?** This course is open source. [Contribute via GitHub](https://github.com/[repo]).
```

**Complete Episode Page Template**:
```markdown
---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 #XX: Lesson Title"
slug: courses/[course-slug]/lesson-XX
---

# Lesson XX: [Full Title]

## [Course Name]

<GitHubButtons />

**Course**: [Link to course index](/podcasts/courses/[course-slug])
**Episode**: XX of N
**Duration**: X minutes
**Presenter**: [Fictional persona name]
**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

## Learning Objectives

By the end of this lesson, you'll be able to:
- [Objective 1]
- [Objective 2]
- [Objective 3]

## Prerequisites

- [Prerequisite 1]
- [Prerequisite 2]
- [Lesson XX-1: Title](./lesson-XX-1) (if sequential)

---

[Clean lesson narration without SSML tags]

[Section headers as needed for readability]

---

## Navigation

⬅️ **Previous**: [Lesson XX-1: Title](./lesson-XX-1) | **Next**: [Lesson XX+1: Title](./lesson-XX+1) ➡️

📚 **[Back to Course Overview](./index)**

---

**Questions or feedback?** This course is open source. [Contribute via GitHub](https://github.com/[repo]).
```

### Phase 3: Update Course Index Page

**Location**: `docs/podcasts/courses/[course-slug]/index.md`

**Find the Episode Entry**:
```markdown
#### 📖 Episode XX: [Title]
**Duration**: [X min] • [📝 Transcript](/podcasts/courses/[course-slug]/lesson-XX)

Learn about:
- [Key point 1]
- [Key point 2]
- [Key point 3]
```

**Update Episode Status**:
If episode was marked as "Coming Soon", update to active link with proper path.

**Example**:
```markdown
### Module 2: Core Concepts (Episodes 3-6)

#### 📖 Episode 3: Understanding Pods
**Duration**: 15 min • [📝 Transcript](/podcasts/courses/kubernetes-fundamentals/lesson-03)

Learn about:
- The Pod abstraction and why containers alone aren't enough
- Single-container vs multi-container Pod patterns
- Pod lifecycle and common debugging scenarios
```

### Phase 4: Add to Podcast Feed

**Location**: `docs/podcasts/index.md`

**Find the Podcast Episodes Section**:
```markdown
## Latest Episodes

- 🎙️ **[#005: PaaS Showdown 2025](/podcasts/00005-paas-showdown)** (14 min) - Brief description
- [Other episodes]
```

**Add Lesson Entry** (mixed chronologically with podcast episodes):
```markdown
## Latest Episodes

- 📖 **[Course: Kubernetes Fundamentals - Lesson 3](/podcasts/courses/kubernetes-fundamentals/lesson-03)** (15 min) - Understanding Pods
- 🎙️ **[#005: PaaS Showdown 2025](/podcasts/00005-paas-showdown)** (14 min) - Brief description
- [Continue...]
```

**Format**:
- Use 📖 emoji for course lessons (vs 🎙️ for podcast episodes)
- Include course name in title
- Chronological order (newest first)
- Brief one-line description

### Phase 5: Verify Metadata File

**Location**: `podcast-generator/episodes/courses/[course-slug]/lesson-XX/lesson-XX.txt`

**Auto-Generated During Audio Creation**

**Required Format**:
```
Title: Lesson XX: [EXACT title from episode page]

Course: [Course Name]

Description:
[2-3 engaging sentences about what this lesson covers]

🔗 Full lesson page: https://platformengineeringplaybook.com/podcasts/courses/[course-slug]/lesson-XX

📚 Course overview: https://platformengineeringplaybook.com/podcasts/courses/[course-slug]

📝 See a mistake or have insights to add? This course is community-driven - open a PR on GitHub to contribute!

Learning Objectives:
• [Objective 1]
• [Objective 2]
• [Objective 3]

Duration: X minutes

Presenter: [Fictional persona name]
Target Audience: Senior platform engineers, SREs, DevOps engineers with 5+ years experience
```

**CRITICAL Checks**:
- [ ] Title EXACTLY matches episode page H1
- [ ] URL uses course-slug format: `/podcasts/courses/[course-slug]/lesson-XX`
- [ ] Learning objectives match episode page
- [ ] Description is engaging (not dry)
- [ ] Course link included

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
# Check lesson page exists at correct URL
ls -la build/podcasts/courses/[course-slug]/lesson-XX/index.html

# Check course index exists
ls -la build/podcasts/courses/[course-slug]/index.html

# Verify navigation links work
grep -r "lesson-XX-1" build/podcasts/courses/[course-slug]/lesson-XX/index.html
```

**Manual Verification**:
```bash
npm run start
# Visit: http://localhost:3000/podcasts/courses/[course-slug]/lesson-XX
```

Check:
- [ ] Lesson page loads correctly
- [ ] Navigation (prev/next) works
- [ ] Course link works
- [ ] Appears in podcast feed
- [ ] Sidebar shows lesson with correct number
- [ ] Learning objectives visible
- [ ] Prerequisites linked correctly

### Phase 7: Pre-Publication Checklist

Complete this checklist before considering lesson published:

**Files Created**:
- [ ] Audio: `podcast-generator/episodes/courses/[course-slug]/lesson-XX/lesson-XX.mp3`
- [ ] Video: `podcast-generator/episodes/courses/[course-slug]/lesson-XX/lesson-XX.mp4`
- [ ] Metadata: `podcast-generator/episodes/courses/[course-slug]/lesson-XX/lesson-XX.txt`
- [ ] Episode page: `docs/podcasts/courses/[course-slug]/lesson-XX.md`
- [ ] Script: `docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt` (with tags)

**Episode Page**:
- [ ] Frontmatter complete with lesson number
- [ ] Slug: `courses/[course-slug]/lesson-XX`
- [ ] Sidebar label: `📖 #XX: Title`
- [ ] `<GitHubButtons />` present
- [ ] Course link, episode count, duration, presenter listed
- [ ] Learning objectives present
- [ ] Prerequisites listed
- [ ] Content clean (no SSML tags)
- [ ] Navigation footer (prev/next/course)

**Course Index Updated**:
- [ ] Episode entry exists in correct module
- [ ] Link works: `/podcasts/courses/[course-slug]/lesson-XX`
- [ ] Duration accurate
- [ ] Key points listed

**Podcast Feed Updated**:
- [ ] Lesson added to `docs/podcasts/index.md`
- [ ] Chronological order (newest first)
- [ ] Uses 📖 emoji
- [ ] Includes course name
- [ ] Link tested

**Metadata File**:
- [ ] Title matches episode page exactly
- [ ] URLs use correct format
- [ ] Learning objectives match
- [ ] Description engaging
- [ ] Duration matches audio length

**Build Verification**:
- [ ] `npm run build` succeeds
- [ ] No MDX errors
- [ ] No broken links
- [ ] Lesson URL works
- [ ] Navigation works (prev/next)
- [ ] Appears in podcast feed
- [ ] Sidebar shows episode

**Audio/Video Quality**:
- [ ] MP3 plays correctly with Autonoe voice
- [ ] MP4 video synced with audio
- [ ] Intro/outro included
- [ ] Pronunciations correct
- [ ] Natural teaching pacing (pauses effective)

## Common Issues & Fixes

### Issue 1: Episode Number Mismatch
**Problem**: Script is `lesson-03.txt`, page is `lesson-04.md`
**Fix**: Rename files to match curriculum plan

### Issue 2: Missing Navigation
**Problem**: No prev/next links in episode page
**Fix**: Add navigation footer with correct links

### Issue 3: Not in Podcast Feed
**Problem**: Lesson only in course, not in main podcast feed
**Fix**: Add entry to `docs/podcasts/index.md` with 📖 emoji

### Issue 4: Course Index Not Updated
**Problem**: Episode page exists but not linked from course index
**Fix**: Update course index.md with episode entry

### Issue 5: Wrong URL Format
**Problem**: Slug is `lesson-XX` instead of `courses/[course-slug]/lesson-XX`
**Fix**: Update slug in frontmatter to include full path

### Issue 6: Tags Visible
**Problem**: Narration shows `[pause]` or `<phoneme>` tags
**Fix**: Use `ssml_utils.py --strip` before copying to episode page

## Course-Specific Customization

### Custom Intro/Outro (Optional)

**Per-Course Audio Files**:
```
podcast-generator/intros/courses/[course-slug]/intro.mp3
podcast-generator/outros/courses/[course-slug]/outro.mp3
```

**Fallback**: Uses generic lesson intro/outro if course-specific doesn't exist

### Custom Video Background (Optional)

**Per-Course Background**:
```
podcast-generator/backgrounds/courses/[course-slug]/background.mp4
```

**Fallback**: Uses generic lesson background if course-specific doesn't exist

## Regenerating Lessons

**For Small Edits** (pronunciation fixes, single lines):
```bash
# Selective regeneration (only changed chunks)
python3 scripts/generate_podcast.py ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt --lesson --episode-id [course-slug]-lesson-XX
```

**For Major Changes** (complete rewrite):
```bash
# Force regeneration (all chunks)
python3 scripts/generate_podcast.py ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt --lesson --episode-id [course-slug]-lesson-XX --force
```

**After Regeneration**:
- Audio/video/metadata updated in `episodes/courses/[course-slug]/lesson-XX/`
- Previous version archived in `episodes/00XXX-name/history/courses/[course-slug]/`
- Episode page only needs updating if narration changed

## Workflow Summary

```
1. GENERATE AUDIO/VIDEO (Autonoe voice)
   ↓
2. CREATE EPISODE PAGE (with navigation)
   ↓
3. UPDATE COURSE INDEX
   ↓
4. ADD TO PODCAST FEED
   ↓
5. VERIFY METADATA
   ↓
6. BUILD & VERIFY
   ↓
7. COMPLETE CHECKLIST
   ↓
8. LESSON PUBLISHED ✓
```

---

## Instructions for Claude

When this skill is invoked:

1. **Verify prerequisites**:
   - Script validated (check for validation report)
   - Script formatted (check for SSML tags)
   - Script location: `docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt`
   - Course index exists: `docs/podcasts/courses/[course-slug]/index.md`

2. **Determine lesson number and course**:
   ```bash
   # Extract from script filename and path
   ls -la docs/podcasts/courses/[course-slug]/scripts/
   ```

3. **Generate audio and video with Autonoe voice** (using --lesson flag):
   ```bash
   cd podcast-generator
   python3 scripts/generate_podcast.py ../docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt --lesson --episode-id [course-slug]-lesson-XX
   ```
   Monitor output for errors. The `--lesson` flag enables lesson-specific chunking and settings.

4. **Create episode page**:
   - Filename: `docs/podcasts/courses/[course-slug]/lesson-XX.md`
   - Frontmatter with lesson number and course path
   - Strip SSML tags from narration
   - Add learning objectives, prerequisites
   - Add navigation footer (prev/next/course)

5. **Update course index**:
   - Find episode entry in correct module
   - Update with link to lesson page
   - Verify duration, key points

6. **Add to podcast feed**:
   - Add to `docs/podcasts/index.md`
   - Use 📖 emoji
   - Include course name
   - Chronological order

7. **Verify metadata file**:
   - Check `episodes/courses/[course-slug]/lesson-XX/lesson-XX.txt`
   - Title matches episode page
   - URLs correct

8. **Build and verify**:
   ```bash
   npm run build
   ```
   Check for errors, test URLs.

9. **Complete checklist** (all items)

10. **Report to user**:
    - Lesson published successfully
    - URLs: `/podcasts/courses/[course-slug]/lesson-XX`
    - Audio/video locations
    - Next steps (next lesson or course completion)

**Remember**: Lessons are part of a course series AND appear in the main podcast feed. Both integrations must work correctly.
