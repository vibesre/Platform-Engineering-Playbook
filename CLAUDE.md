# Platform Engineering Playbook - Technical Page Format Guide

This guide codifies the format and standards for all technical documentation pages in the Platform Engineering Playbook. Follow this template to ensure consistency and maximize learning value.

## Page Structure

### 0. Frontmatter (SEO & AEO Optimization)
**REQUIRED** for all technical pages:

```yaml
---
title: "[Technology Name] - [Value Proposition]"
description: "150-160 char description with key features, use cases, and interview mention"
keywords:
  - primary keyword
  - technology tutorial
  - interview questions
  - related technologies
  - (8-12 keywords total)
datePublished: "YYYY-MM-DD"  # For blog posts
dateModified: "YYYY-MM-DD"   # For blog posts
schema:
  type: FAQPage  # or HowTo, TechArticle
  questions:
    - question: "Common question about the technology?"
      answer: "Concise answer with specific facts/data"
    # 5-10 Q&As for high-traffic pages
---
```

**SEO Checklist**:
- [ ] Unique title (50-60 characters)
- [ ] Compelling description (150-160 characters)
- [ ] 8-12 relevant keywords as array
- [ ] Include year/date for blog posts
- [ ] FAQ schema for Q&A content
- [ ] HowTo schema for tutorials

**AEO (AI Engine Optimization) Checklist**:
- [ ] Quick Answer section at top
- [ ] FAQ schema with 5-10 questions
- [ ] Key Takeaway boxes (💡) for major insights
- [ ] Statistics table with sources
- [ ] Dates visible (Updated 2025, etc.)
- [ ] Direct answers to common questions
- [ ] Comparison tables where applicable
- [ ] Expert quotes with attribution

### 1. Title & Quick Answer (For AEO)
```markdown
# [Technology Name]

<GitHubButtons />

## Quick Answer

**What is [Technology]?**
[One sentence definition with key facts]

**Primary Use Cases**: [3-4 bullet points or comma-separated]
**Market Position**: [Adoption stat, GitHub stars, market share]
**Learning Time**: [Realistic time estimate: X weeks basics, Y months proficiency]
**Key Certifications**: [List major certs if applicable, or "None"]
**Best For**: [Who should use this technology]

[Full guide below ↓](#learning-resources)
```

**Quick Answer Requirements** (AI Engine Optimization):
- Must be factual and standalone (no pronouns)
- Include real statistics (GitHub stars, adoption %, market data)
- Provide specific timelines for learning
- Easy for AI engines to parse and cite
- Appears before Learning Resources section

### 2. Learning Resources Section
Place learning resources immediately after Quick Answer. Organize by learning path:

```markdown
## 📚 Learning Resources

### 📖 Essential Documentation
- [Official Documentation](url) - Brief description
- [API/Query Language Docs](url) - What it covers
- [Best Practices](url) - Key focus areas
- Include star counts for popular repos (e.g., "9.6k⭐")

### 📝 Specialized Guides
- Focus on specific aspects (e.g., query languages, specific use cases)
- Include publication dates for recent content
- Prioritize guides from creators/maintainers

### 🎥 Video Tutorials
- Include duration in description
- Verify videos are still available
- Focus on comprehensive tutorials

### 🎓 Professional Courses
- Official certifications first
- Include pricing info (Free/Paid)
- Platform-specific courses (Linux Foundation, Pluralsight, etc.)

### 📚 Books
- List authoritative books only
- Include author names
- **Always include purchase links** from official sources (Amazon, O'Reilly, publisher sites)
- **Only include free versions** if officially provided by author/publisher
- Avoid questionable PDF sites even if they appear in search results
- Format when free version exists: `"Book Title" by Author - [Free PDF](url) | [Purchase](url)`
- Format when only paid: `"Book Title" by Author - [Purchase on Amazon](url) | [Publisher](url)`

### 🛠️ Interactive Tools
- Playgrounds and sandboxes
- Interactive learning environments
- Include what they're pre-configured with

### 🚀 Ecosystem Tools
- Only include tools central to the technology
- Brief description of purpose
- Avoid external visualization/management tools unless critical

### 🌐 Community & Support
- Official community channels
- Active discussion forums
- Conferences and events
```

### 3. Understanding Section
High-level conceptual overview focused on mental models:

```markdown
## Understanding [Technology]: [Descriptive Subtitle]

Brief introduction paragraph explaining what it is and its significance.

### How [Technology] Works
- Core operating principles
- What makes it unique
- Key architectural decisions
- Use simple analogies

### The [Technology] Ecosystem
- Core components and their roles
- How pieces work together
- Don't include installation/configuration

### Why [Technology] Dominates [Domain]
- Key advantages
- Problem-solution fit
- Community/ecosystem strength

### Mental Model for Success
- Provide a clear analogy
- Explain the fundamental concept
- Help readers build intuition

### Where to Start Your Journey
1. Numbered list of practical steps
2. Start with hands-on experimentation
3. Progress from simple to complex
4. Include what to focus on at each stage

### Key Concepts to Master
- Bullet points of essential concepts
- No code examples
- Focus on terminology and patterns
- Brief explanation of why each matters

Closing paragraph emphasizing simplicity and gradual learning.
```

### 4. Stay Updated Section (LAST)
Compact section at the very bottom:

```markdown
---

### 📡 Stay Updated

**Release Notes**: [Component1](url) • [Component2](url) • [Component3](url)

**Project News**: [Official Blog](url) • [Foundation Blog](url) • [Videos](url)

**Community**: [Mailing Lists](url) • [Discussion Forums](url) • [Newsletters](url)
```

## Content Guidelines

### DO:
- **Validate all links** - Remove broken/outdated resources
- **Focus on official sources** - Prefer official docs and repos
- **Keep descriptions brief** - One line max for each resource
- **Update regularly** - Check for new resources and remove stale ones
- **Include dates** - For blogs, guides, and courses when relevant
- **Use bullet separators (•)** - For compact link lists
- **Maintain high quality** - Only include genuinely useful resources

### DON'T:
- **No implementation details** - No code snippets, configs, or technical specs
- **No installation guides** - Focus on understanding, not doing
- **Avoid external tools** - Unless absolutely central to the ecosystem
- **No redundancy** - Each resource should offer unique value
- **Skip low-quality content** - No outdated blogs or abandoned projects
- **Avoid walls of text** - Keep sections concise and scannable

## Resource Quality Criteria

Before including any resource, verify:

1. **Accessibility** - Link works and content is freely accessible
2. **Relevance** - Directly related to learning the technology
3. **Quality** - Well-written, accurate, and comprehensive
4. **Maintenance** - Recently updated or timelessly relevant
5. **Authority** - From recognized experts or official sources

## Formatting Standards

- Use **bold** for emphasis sparingly
- Use `code formatting` only for command/function names
- Include emojis for section headers (📚 📖 📝 🎥 🎓 🛠️ 🚀 🌐 📡)
- Keep line lengths reasonable for readability
- Use consistent bullet styles throughout

## Example Validation Process

When updating a technical page:

1. Test every link
2. Check publication/update dates
3. Verify video availability
4. Confirm course accessibility
5. Update descriptions as needed
6. Remove any deprecated content
7. Add new high-quality resources
8. Reorganize if necessary for clarity

## Maintenance Schedule

Technical pages should be reviewed:
- **Quarterly** - Link validation and minor updates
- **Annually** - Major revision and content refresh
- **As needed** - When major changes occur in the technology

This format prioritizes learning efficiency, resource quality, and long-term maintenance while keeping technical implementation details in separate documentation.

---

## SEO & AEO Content Requirements

### For ALL Technical Pages

**Required Elements**:
1. ✅ Frontmatter with title, description, keywords
2. ✅ Quick Answer section (for AI parsing)
3. ✅ FAQ schema (5-10 Q&As for high-traffic pages)
4. ✅ Learning Resources section
5. ✅ Understanding/conceptual section
6. ✅ Stay Updated section at bottom

**AI Engine Optimization (AEO) Elements**:
- **Quick Answer**: Direct response to "What is X?" at the top
- **FAQ Schema**: Structured Q&A in frontmatter for AI citations
- **Key Takeaways**: 💡 boxes for major insights (use sparingly, 2-3 per page)
- **Statistics Tables**: Data with sources in markdown tables
- **Dates**: Include "Updated 2025" or datePublished/dateModified
- **Comparison Tables**: Side-by-side tool comparisons
- **Expert Quotes**: Block quotes with attribution
- **Decision Trees**: "Should you use X?" flowchart-style content

### For Blog Posts

**Additional Requirements**:
1. ✅ TL;DR/Quick Answer at very top
2. ✅ Key Statistics table near beginning
3. ✅ 5-7 Key Takeaway boxes throughout
4. ✅ datePublished and dateModified in frontmatter
5. ✅ Schema: FAQPage, HowTo, or TechArticle
6. ✅ Year in title "(2025 Guide)" if relevant

**Content Structure for Maximum AI Citations**:
```markdown
# Title [2025 Guide]

> 🎙️ **IMPORTANT**: If a podcast episode exists for this blog post, add the cross-link here (after title, before Quick Answer). See "Cross-Linking Requirement" in Podcast Script Guide section.

## Quick Answer (TL;DR)
- **Problem**: [One sentence]
- **Solution**: [One sentence]
- **ROI**: [Specific numbers]
- **Timeline**: [Implementation time]
- **Key Tools**: [3-5 specific tools]

## Key Statistics (2024-2025 Data)
| Metric | Value | Source |
|--------|-------|--------|
[Table with 8-12 key data points]

[Main content...]

> **💡 Key Takeaway**
>
> [Major insight with specific data that AI can cite]

[More content...]

## How to Implement [Step-by-Step]
1. **Phase 1**: [Clear steps]
2. **Phase 2**: [Clear steps]
[Use numbered lists for processes]

[More content with more Key Takeaways...]
```

### AI-Friendly Writing Style

**DO**:
- Use **direct answers** ("Shadow AI affects 85% of organizations")
- Include **specific numbers** with sources
- Write **standalone sentences** (no "as mentioned above")
- Use **comparison tables** for vs. content
- Add **expert quotes** with attribution
- Include **decision frameworks** ("Use X when..., Use Y when...")
- Make **timelines explicit** ("2-3 months to proficiency")

**DON'T**:
- Use vague statements ("AI can help improve...")
- Write pronoun-heavy content ("It does this by...")
- Bury key facts in paragraphs
- Omit sources for statistics
- Use marketing jargon without data

### Content Scoring for AI Citations

Rate your content on this scale (aim for 10/12):
- [ ] Has Quick Answer section
- [ ] Has FAQ schema (5+ questions)
- [ ] Includes 2+ statistics with sources
- [ ] Has comparison table (if applicable)
- [ ] Includes date/year signals
- [ ] Has Key Takeaway boxes (2-3)
- [ ] Uses direct answer format
- [ ] Includes expert quotes
- [ ] Has numbered how-to steps
- [ ] Standalone sentences (no pronouns)
- [ ] Includes decision framework
- [ ] Links to related content (5+ internal links)

---

## Blog Content Production Guidelines

### Research Standards

**CRITICAL**: All blog posts must be thoroughly researched and fact-checked before publication. The Platform Engineering Playbook's reputation depends on accuracy and trustworthiness.

#### 1. Source Verification (REQUIRED)

**Primary Sources** (Always prefer these):
- Official documentation from vendors/projects
- Published research papers and studies (with DOI/URL)
- Company engineering blogs from practitioners
- Conference talks from engineers (not sales pitches)
- GitHub repositories with real usage data (stars, forks, contributors)
- Peer-reviewed technical publications

**Acceptable Secondary Sources**:
- Reputable tech news sites (The New Stack, InfoQ, Ars Technica)
- Industry analyst reports (Gartner, Forrester) - cite specific reports with dates
- High-quality community blogs with technical depth
- Stack Overflow/Reddit threads for community sentiment (mark as anecdotal)

**Unacceptable Sources**:
- Marketing content without technical backing
- Unverified claims or rumors
- Outdated content (>2 years old unless historical context)
- AI-generated content without verification
- Anonymous sources without corroboration

#### 2. Fact-Checking Process

Before publishing, verify EVERY:
- [ ] **Statistic** - Find original source, check date, verify context
- [ ] **Quote** - Confirm exact wording, verify attribution, include context
- [ ] **Technical claim** - Test if possible, or find multiple confirming sources
- [ ] **Pricing** - Check vendor website, note date (pricing changes frequently)
- [ ] **Feature availability** - Verify in current documentation
- [ ] **Company data** - Cross-reference multiple sources (funding, headcount, etc.)

**Verification Rules**:
1. **Numbers require sources**: Every statistic MUST have a source link
2. **Three-source rule**: Major claims need 3+ independent sources
3. **Recency check**: Data >1 year old must be marked with date
4. **Original source**: Always link to the PRIMARY source, not secondary reporting
5. **Archive important sources**: Use archive.org for content that might disappear

#### 3. Citation Format

**Inline Citations** (preferred for stats):
```markdown
According to Gartner's 2024 Platform Engineering Report, 75% of organizations cite cost as a primary concern ([source](url)).
```

**Comparison Tables** (must include sources):
```markdown
| Feature | Tool A | Tool B | Source |
|---------|--------|--------|---------|
| Price | $99/mo | $149/mo | [Tool A Pricing](url), [Tool B Pricing](url) |
```

**Reference Section** (at end of post):
```markdown
## Sources & References

### Primary Research
1. [Title of Study] - Author/Organization, Date - [Link](url)
2. [Official Documentation] - [Link](url)

### Industry Reports
1. [Gartner Platform Engineering Report 2024] - Published Dec 2024 - [Link](url)

### Practitioner Insights
1. [Engineering Blog Post Title] - Company, Author, Date - [Link](url)

### Tools & Platforms Referenced
- [Tool Name](url) - Official documentation
- [Tool Name GitHub](url) - Open source repository
```

#### 4. Learning Resources Quality Standards

**Every blog post should include 5-10 high-quality learning resources:**

**What to Include**:
- ✅ Official documentation (always first)
- ✅ Comprehensive tutorials from credible sources
- ✅ Video courses/talks from practitioners (with duration)
- ✅ Books from recognized experts (with purchase links)
- ✅ Active GitHub repositories with good documentation
- ✅ Community resources (Discord, Slack, forums) if active
- ✅ Certification programs if relevant

**Quality Criteria**:
- [ ] Resource is current (updated within 2 years)
- [ ] Content is comprehensive (not just a marketing page)
- [ ] Author/organization has credibility
- [ ] Resource is accessible (not behind hard paywall)
- [ ] Link is stable (prefer official domains over Medium/blog platforms)

**Format**:
```markdown
## 📚 Learning Resources

### Official Documentation
- [Tool Name Docs](url) - Complete reference with examples
- [API Reference](url) - Detailed API documentation

### Tutorials & Guides
- [Comprehensive Guide](url) by Author - Published 2024 - 30min read
- [Video Tutorial](url) - Conference Name 2024 - 45min

### Books
- "Book Title" by Author - [Purchase on Amazon](url) | [Publisher](url)
- "Another Book" by Author - [Official Free PDF](url) (if legitimately free)

### Community Resources
- [Official Discord](url) - 10K+ members, active support
- [GitHub Discussions](url) - 500+ threads, core team participation
```

#### 5. Writing for Engagement

**Opening Hook** (First 100 words):
- Start with a surprising statistic or provocative question
- Establish why this matters NOW (urgency/relevance)
- Preview the value reader will get
- Use concrete examples over abstractions

**Story-Driven Content**:
- ✅ Real-world case studies with specific numbers
- ✅ "Before/After" scenarios showing transformation
- ✅ Problem → Analysis → Solution structure
- ✅ Practitioner quotes with attribution
- ✅ War stories (when things went wrong and lessons learned)

**Maintaining Interest**:
- **Vary sentence length**: Mix short punchy sentences with longer explanatory ones.
- **Use subheadings every 300-400 words**: Help readers scan and find value
- **Include visuals**: Comparison tables, decision trees, cost breakdowns
- **Add Key Takeaways**: 💡 boxes every 800-1000 words
- **Use specifics over generics**: "Reduced deployment time from 45min to 6min" not "improved deployment speed"
- **Address reader directly**: "You're probably facing..." not "Organizations face..."

**Avoid These Engagement Killers**:
- ❌ Walls of text without breaks
- ❌ Abstract concepts without concrete examples
- ❌ Jargon without explanation
- ❌ Repeating the same points
- ❌ Burying the lede (put valuable info early)
- ❌ Generic advice that could apply to anything

#### 6. Technical Accuracy Review

Before publishing, review for:

**Technical Claims**:
- [ ] Architecture descriptions match official documentation
- [ ] Code examples (if any) actually work
- [ ] Version numbers are current
- [ ] Compatibility claims are verified
- [ ] Performance numbers include test conditions
- [ ] Security claims are current (vulnerabilities change)

**Common Accuracy Mistakes to Avoid**:
- Conflating similar but different technologies
- Using outdated terminology
- Misunderstanding how something works internally
- Overgeneralizing from limited experience
- Ignoring important caveats or edge cases

#### 7. Blog Post Production Checklist

**Research Phase**:
- [ ] Topic validated from community analysis or reader questions
- [ ] 10+ high-quality sources identified
- [ ] All statistics traced to primary sources
- [ ] Pricing/features verified on official sites
- [ ] Learning resources vetted for quality

**Writing Phase**:
- [ ] Strong hook in first 100 words
- [ ] Quick Answer/TL;DR at top
- [ ] Key Statistics table with sources
- [ ] 5-7 Key Takeaway boxes throughout
- [ ] Comparison tables where applicable
- [ ] Decision frameworks included
- [ ] Real-world examples with specifics
- [ ] Internal links to related content (5+)

**Review Phase**:
- [ ] Every statistic has a source link
- [ ] All links tested and working
- [ ] Facts verified against original sources
- [ ] Technical claims reviewed for accuracy
- [ ] Learning resources section complete
- [ ] SEO/AEO requirements met (see checklist below)
- [ ] Engagement elements present (stories, examples, variety)

**SEO/AEO Compliance Checklist** (Aim for 12/12 score):
- [ ] Has Quick Answer/TL;DR section at top
- [ ] Has FAQ schema in frontmatter (5+ questions)
- [ ] Includes 2+ statistics with source links
- [ ] Has comparison table (if applicable to topic)
- [ ] Includes date/year signals (datePublished, "2025 Guide")
- [ ] Has Key Takeaway boxes (💡) throughout (2-3 minimum)
- [ ] Uses direct answer format (no "as mentioned above" pronouns)
- [ ] Includes expert quotes or authoritative references
- [ ] Has numbered how-to steps or decision framework
- [ ] Standalone sentences that AI can cite independently
- [ ] Includes decision framework ("Use X when..., Use Y when...")
- [ ] Links to related internal content (5+ internal links minimum)

**Frontmatter Requirements**:
```yaml
---
title: "[Technology/Topic] - [Value Prop] [Year]"  # 50-60 chars
description: "150-160 char with key features and mention"
keywords:
  - primary keyword
  - technology tutorial
  - interview questions
  # 8-12 keywords total
datePublished: "YYYY-MM-DD"
dateModified: "YYYY-MM-DD"
schema:
  type: FAQPage  # or HowTo, TechArticle
  questions:
    - question: "Common question?"
      answer: "Concise factual answer"
    # 5-10 Q&As
---
```

**Publication Phase**:
- [ ] Frontmatter complete with all metadata
- [ ] Images optimized (if any)
- [ ] Internal links use correct paths
- [ ] Date published set to current date
- [ ] Added to blog index/sidebar

#### 8. Post-Publication

**Monitor & Update**:
- Set calendar reminder to review in 6 months
- Update if major changes to tools/technologies occur
- Add `dateModified` when updating
- Check for broken links quarterly
- Monitor comments/feedback for corrections

### Writing Tone & Voice

**Target Audience**: Senior platform engineers (5+ years experience) who value:
- Technical depth over surface-level coverage
- Honest trade-off analysis over hype
- Real-world practicality over theoretical ideals
- Data-driven decision making

**Voice Characteristics**:
- **Authoritative but humble**: Share expertise without arrogance
- **Honest about trade-offs**: Every solution has pros/cons
- **Practical over academic**: Focus on what works in production
- **Skeptical of hype**: Question marketing claims, demand evidence
- **Respectful of reader's intelligence**: Don't over-explain basics

**Example of Good Tone**:
> "Flightcontrol promises Heroku-like simplicity with AWS flexibility. At $397/month base cost, that's a significant premium over self-managed infrastructure. But when you factor in the engineering time saved—and the opportunity cost of not shipping features—the math starts to look different. Let's break down the real costs..."

**Example of Bad Tone**:
> "Flightcontrol is an amazing platform that revolutionizes deployment! It's the perfect solution for everyone looking to simplify their infrastructure!"

---

## Podcast Production

### Using Claude Code Skills

For podcast production, use the dedicated Claude Code skills in `.claude/skills/`:

1. **podcast-research** - Topic discovery and community validation
2. **podcast-outline** - Story planning with narrative frameworks (MANDATORY before script)
3. **podcast-script** - Convert outline to natural Jordan/Alex dialogue
4. **podcast-validate** - Fact-check statistics, verify sources, ensure accuracy
5. **podcast-format** - Add SSML pause tags and pronunciation guidance
6. **podcast-publish** - Generate audio/video, create episode page, update index

Each skill contains detailed instructions, storytelling templates, quality checklists, and examples. This enforces the workflow (e.g., can't write script without outline) and ensures consistent quality.

**Quick Start**: `"Use the podcast-research skill to find trending platform engineering topics"`

---

## Podcast Episode Requirements - Quick Reference

**Target Audience**: Senior platform engineers, SREs, DevOps engineers (5+ years experience)

**Voice**: Two experienced engineers (Jordan and Alex) having a strategic discussion with natural interruptions, respectful disagreement, and technical depth.

### ⚠️ CRITICAL: Intro/Outro Format (READ THIS FIRST)

**Scripts DO NOT include intro or outro content** - these are handled by separate pre-recorded MP3 files:

**Intro MP3** (`podcast-generator/intros/intro.mp3`):
> Welcome to the Platform Engineering Playbook Podcast — where everything you hear is built, reviewed, and improved by AI, by me, and by you, the listener.
>
> This show keeps me — and hopefully you — up to speed on the latest in platform engineering, SRE, DevOps, and production engineering. It's a living experiment in how AI can help us track, explain, and debate the fast-moving world of infrastructure.
>
> Every episode is open source. If you've got something to add, correct, or challenge, head to platformengineeringplaybook.com — you'll find all the content and a link to the GitHub repo. Open a pull request, join the conversation, and make the Playbook smarter.
>
> Let's get into it.

**Outro MP3** (`podcast-generator/outros/outro.mp3`):
> That's it for this episode of the Platform Engineering Playbook Podcast.
>
> Every topic, transcript, and summary you just heard lives out in the open at platformengineeringplaybook.com — where anyone can suggest updates or add insights through GitHub.
>
> If you've got thoughts, fixes, or new ideas, open a PR. And if you enjoyed the episode, rate us on your favorite podcast platform — we're always shooting for five stars.
>
> While you're there, give the project a ⭐ star on GitHub — it helps others find and contribute to the Platform Engineering Playbook.
>
> This podcast is generated by AI, reviewed by AI, me, and you — a community of engineers keeping our craft sharp.
>
> Thanks for listening — and see you next time inside the Platform Engineering Playbook.

**Script Format Checklist**:
- ✅ First line starts with "Today we're diving into..." or "Speaker 1: Today we're..."
- ✅ Last line is a practical takeaway (e.g., "The fundamentals remain constant...")
- ❌ NO welcome messages (intro MP3 handles this)
- ❌ NO host introductions ("I'm Jordan/Alex") (intro MP3 handles this)
- ❌ NO show descriptions ("This is the show where...") (intro MP3 handles this)
- ❌ NO cold open hooks (dropping mid-conversation)
- ❌ NO thank yous or goodbyes (outro MP3 handles this)
- ❌ NO "Keep building thoughtfully" or "Until next time" (outro MP3 handles this)

### Episode Structure

**Duration**: 12-15 minutes of dialogue

**Sections**:
1. Episode Introduction (30-45s) - Preview topics, set context
2. Landscape Overview (3-4 min) - Market dynamics, design philosophy
3. Technical Deep Dive (4-5 min) - Compare 2-3 solutions
4. Underdogs & Specialists (2-3 min) - Niche players, emerging solutions
5. Skills Evolution (3-4 min) - Table stakes, declining, rising importance
6. Practical Wisdom (2 min) - Mistakes to avoid, decision frameworks
7. Closing Thoughts (1-2 min) - Key insight, actionable takeaway

---

## File Naming & URLs

**Episode Numbers**: Use 5-digit prefix (00001, 00002, ..., 00099, 00100)

**Files**:
- Script: `docs/podcasts/scripts/00005-topic-name.txt`
- Episode page: `docs/podcasts/00005-topic-name.md`
- URL: `/podcasts/00005-topic-name` (permanent, shareable)

**Why Numbered URLs?**
- Professional standard (Changelog, Syntax.fm, etc.)
- Prevents collisions (can revisit topics with different episode numbers)
- Chronological organization
- Easy to reference in show notes

---

## Episode Page Format

**Frontmatter** (required):
```yaml
---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #005: Episode Title"
slug: 00005-episode-name
---
```

**Page Header**:
```markdown
# [Full Episode Title]

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** [X minutes]
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/related-slug)**: Description. (IF blog post exists)

---
```

**Dialogue Format**:
- Speaker names: `**Jordan**:` and `**Alex**:`
- Blank lines between speakers
- No SSML tags (strip before publishing)

---

## Script Format

**Location**: `docs/podcasts/scripts/00005-topic-name.txt`

**Speaker names**: `Jordan:` and `Alex:` (NOT Speaker 1/2)

**Content**: Write naturally without tags initially. Tags added later by podcast-format skill.

---

## TTS Tags Reference

**SSML Pause Tags** (added by formatting skill):
- `[pause short]` - After list items
- `[pause]` - After statistics, questions
- `[pause long]` - After dramatic reveals

**Pronunciation Tags** (see `podcast-generator/PRONUNCIATION_GUIDE.md`):
- `<phoneme alphabet="ipa" ph="...">Term</phoneme>` - IPA pronunciation
- `<say-as interpret-as="characters">AWS</say-as>` - Letter-by-letter

**Common terms requiring tags**: Kubernetes, PostgreSQL, Azure, YAML, MLOps, Nginx

**Note**: Tags added automatically by `add_ssml_tags.py` and `add_pronunciation_tags.py`

---

## Metadata File Format

**Location**: `podcast-generator/output_latest/00005-topic-name.txt` (auto-generated)

```
Title: [EXACT H1 from episode page]

Description:
[2-3 engaging sentences with hook and call-to-action]

🔗 Full episode page: https://platformengineeringplaybook.com/podcasts/00005-topic-name

📝 See a mistake or have insights to add? This podcast is community-driven - open a PR on GitHub!

Summary:
• [Concrete takeaway 1]
• [Concrete takeaway 2]
• [Concrete takeaway 3-5]

Duration: [X minutes]
Speakers: Alex and Jordan
Target Audience: Senior platform engineers, SREs, DevOps engineers with 5+ years experience
```

**CRITICAL**: Title must exactly match episode page H1, URL must use numbered format.

---

## Cross-Linking Requirement (MANDATORY)

**When creating a podcast episode with a corresponding blog post, cross-link them in both directions:**

### In Blog Post (after intro, before Quick Answer):
```markdown
> 🎙️ **Listen to the podcast episode**: [Episode Title](/podcasts/00005-episode-name) - Brief description highlighting conversation format.
```

### In Podcast Page (after duration/speakers):
```markdown
> 📝 **Read the [full blog post](/blog/related-slug)**: Brief description highlighting written format.
```

**Checklist**:
- [ ] Blog post links to podcast (if one exists)
- [ ] Podcast page links to blog (if one exists)
- [ ] Links use emoji indicators (🎙️ podcast, 📝 blog)
- [ ] URLs use numbered format (`/podcasts/00005-name`)
- [ ] Links tested and working

---

*For detailed podcast production workflows, storytelling templates, validation checklists, and formatting instructions, use the Claude Code skills in `.claude/skills/podcast-*`*

---

## Course Series Production

### Overview

Course series are structured, multi-episode educational content designed for deep learning and skill mastery. Unlike podcasts (conversational episodes), courses use single-presenter lecture format optimized for retention using learning science principles.

**Key Differences from Podcasts**:
- **Format**: Single presenter (Autonoe voice) vs two-person dialogue (Jordan/Alex)
- **Structure**: Curriculum-driven with progressive complexity vs standalone episodes
- **Pedagogy**: Learning objectives, spaced repetition, active recall vs storytelling
- **Location**: `/podcasts/courses/[course-slug]/` with episode navigation vs flat `/podcasts/00XXX-name`
- **Feed**: Appears in podcast feed AND course index

### Using Course Skills

For course production, use the dedicated Claude Code skills in `.claude/skills/`:

1. **lesson-research** - Topic discovery, learning path analysis, pain point identification
2. **lesson-curriculum** - Multi-episode curriculum design with learning science principles
3. **lesson-outline** - Structure individual lesson episodes (MANDATORY before script)
4. **lesson-script** - Convert outline to single-presenter educational narration
5. **lesson-validate** - Fact-check, verify sources, validate pedagogy
6. **lesson-format** - Add SSML tags for Autonoe voice TTS
7. **lesson-publish** - Generate audio/video, create episode pages, update course index

**Quick Start**: `"Use the lesson-research skill to research [topic] for a course"`

### Course Requirements

**Target Audience**: Senior platform engineers, SREs, DevOps engineers (5+ years experience)

**Presenter**: Single instructor using Autonoe voice (Chirp 3 HD, 0.95x speed)

**Episode Length**: ~15 minutes (12-18 minutes acceptable, flexible based on content)

**Series Scope**: Flexible based on topic (typically 5-20 episodes)

**Content Format**: Audio + transcript (expandable to include exercises/labs later)

### Pedagogical Principles Applied

All courses integrate evidence-based learning science:

**1. Spaced Repetition** (2-3x better retention):
- Key concepts introduced early, reinforced in later episodes
- Dedicated review episodes every 3-4 lessons
- Callbacks in every episode to previous material

**2. Active Recall** (strengthens memory):
- "Before we continue, try to recall..." prompts
- Pause points for learner practice
- Retrieval questions before showing answers

**3. Progressive Complexity** (scaffolding):
- Episode 1: Simple mental models
- Episodes 2-N: Build incrementally
- Each episode assumes ONLY previous episodes

**4. Chunking** (cognitive load management):
- One core concept per episode
- 10-15 minute episodes (optimal attention span)
- Break complex topics across multiple episodes

**5. Interleaving** (improves discrimination):
- Mix related concepts across episodes
- Return to topics with new context
- Compare/contrast throughout

**6. Elaborative Rehearsal** (deeper encoding):
- Multiple examples per concept
- Analogies to familiar ideas
- Different explanations of same concept

### Course Structure

**File Organization**:
```
docs/podcasts/courses/
├── course-slug/
│   ├── index.md                      # Course overview/curriculum
│   ├── lesson-01.md                  # Episode pages
│   ├── lesson-02.md
│   ├── ...
│   ├── curriculum-plan.md            # Internal planning (not published)
│   ├── scripts/
│   │   ├── lesson-01.txt
│   │   ├── lesson-02.txt
│   │   └── ...
│   └── outlines/
│       ├── lesson-01-outline.md
│       ├── lesson-02-outline.md
│       └── ...
```

**Course Index Page** (`index.md`):
- Overview of course and learning outcomes
- Prerequisites
- Module structure with episode links
- Time commitment estimate

**Lesson Episode Pages** (`lesson-XX.md`):
- Learning objectives
- Prerequisites (including previous lessons)
- Clean transcript
- Navigation (prev/next/course)

### Lesson Episode Format

**Frontmatter**:
```yaml
---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 #XX: Lesson Title"
slug: courses/[course-slug]/lesson-XX
---
```

**Page Structure**:
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
- [Link to previous lesson if sequential]

---

[Clean lesson narration]

---

## Navigation

⬅️ **Previous**: [Lesson XX-1](./lesson-XX-1) | **Next**: [Lesson XX+1](./lesson-XX+1) ➡️

📚 **[Back to Course Overview](./index)**
```

### Script Format for Lessons

**No Speaker Labels**: Single presenter, natural flow

**Teaching Techniques Required**:
- **Signposting**: "First... Second... Finally..."
- **Analogies**: Relate to familiar concepts
- **Elaboration**: "In other words..." / "To put it another way..."
- **Think-Alouds**: "Here's how I think through this..."
- **Pause Points**: "Pause and try this yourself..."
- **Callbacks**: "Remember when we covered X in Episode Y?"

**Script Example**:
```
Welcome to Episode 3 of Kubernetes Fundamentals. Today we're exploring Pods.

If you're like most engineers, you've probably wondered why we need Pods
when we already have containers. Great question. Let's dive in.

By the end of this lesson, you'll understand the Pod abstraction, why
containers alone aren't enough, and when to use different Pod patterns.

Let's start with a mental model. Think of Pods like shipping containers...
[Continue naturally]
```

### Integration with Podcast Feed

**Courses appear in TWO places**:

1. **Course Index** (`/podcasts/courses/[course-slug]`):
   - Full curriculum with all episodes
   - Module structure
   - Progressive learning path

2. **Main Podcast Feed** (`/podcasts/index.md`):
   - Mixed chronologically with podcast episodes
   - Use 📖 emoji (vs 🎙️ for podcasts)
   - Include course name in title

**Podcast Feed Entry Format**:
```markdown
- 📖 **[Course: Kubernetes Fundamentals - Lesson 3](/podcasts/courses/kubernetes-fundamentals/lesson-03)** (15 min) - Understanding Pods
- 🎙️ **[#005: PaaS Showdown 2025](/podcasts/00005-paas-showdown)** (14 min) - Brief description
```

### Curriculum Design Standards

**Module Structure** (typical 8-12 episode course):
```
Module 1: Foundations (2-3 episodes)
├─ Episode 1: Mental Model & First Principles
├─ Episode 2: Essential Concepts
└─ Episode 3: Hands-On Fundamentals

Module 2: Core Topics (4-6 episodes)
├─ Episodes 4-N: Individual concepts (one per episode)
└─ Episode N: Review & Integration

Module 3: Production Readiness (2-3 episodes)
├─ Episode N+1: Advanced Patterns
└─ Episode N+2: Mastery & Next Steps
```

**Review Episodes** (every 3-4 lessons):
- Active recall phase (retrieval questions)
- Integration phase (how concepts connect)
- Troubleshooting phase (common issues)
- Preview phase (what's coming)

### Learning Objectives Requirements

**Must be**:
- **Specific**: Not "understand X" but "explain why X exists"
- **Measurable**: Learner can verify achievement
- **Achievable**: Realistic for one 15-min episode
- **Action-oriented**: Use verbs (explain, create, diagnose, design)

**Good Examples**:
- "Explain the Pod abstraction and why containers alone aren't enough"
- "Create a Deployment manifest that scales to 5 replicas"
- "Diagnose why a Pod is in CrashLoopBackOff state"

**Bad Examples**:
- "Understand Pods" (too vague)
- "Learn about Kubernetes" (not specific)
- "Master container orchestration" (not achievable in one episode)

### Voice & Tone Guidelines

**Presenter Voice**:
- Conversational but authoritative
- Patient and clear
- Respectful of learner intelligence
- Shares practical experience

**Perspective**:
- Use "we" (inclusive): "we'll explore", "let's examine"
- Use "you" (direct): "you'll be able to", "you might encounter"
- Use "I" sparingly (personal anecdotes, opinions)

**Example Voice**:
```
"Now, here's where it gets interesting. Most engineers assume X, but
in production, you'll find Y. Let me show you why this matters.

Imagine you're debugging a failed deployment at 2 AM. You need to know
the difference between a Pod crash and a container crash. Here's how
I think through this..."
```

### Content Quality Standards

**Technical Depth**:
- Appropriate for senior engineers (5+ years)
- Don't explain basics they know (containers, Linux)
- DO explain technology-specific concepts
- Focus on production implications
- Include edge cases and gotchas

**Engagement**:
- Real-world examples with specific numbers
- Production scenarios (not just toy examples)
- Honest about trade-offs
- Acknowledge complexity
- Decision frameworks (when to use what)

**Accuracy** (validated via lesson-validate skill):
- Every statistic sourced
- Technical claims match official docs
- Code examples runnable
- Pricing current with dates
- Examples tested

### TTS Generation

**Voice**: Autonoe (Chirp 3 HD)
- Voice ID: `en-US-Chirp3-HD-Autonoe`
- Speed: 0.95x (clarity for technical content)
- Clear and professional

**SSML Tags** (added by lesson-format skill):
- Pause tags: `[pause]`, `[pause short]`, `[pause long]`
- Pronunciation: `<phoneme alphabet="ipa" ph="...">Term</phoneme>`
- Acronyms: `<say-as interpret-as="characters">AWS</say-as>`

**Pause Placement** (teaching-specific):
- After learning objectives
- Before/after analogies
- Around think-aloud sections
- For active recall prompts (longer pauses)
- Before major transitions

### Course Production Checklist

**Research Phase**:
- [ ] Topic validated (sufficient depth, community interest)
- [ ] Learning path mapped (beginner → proficient)
- [ ] Pain points identified (Stack Overflow, Reddit, GitHub)
- [ ] Prerequisites clear
- [ ] Knowledge gaps in existing content identified

**Curriculum Design Phase**:
- [ ] Episode structure determined (X episodes, Y modules)
- [ ] Spaced repetition mapped (key concepts repeated 3+ times)
- [ ] Review episodes placed (every 3-4 lessons)
- [ ] Learning objectives specific and measurable
- [ ] Concept dependencies clear

**Per-Episode Production**:
- [ ] Outline created (MANDATORY before script)
- [ ] Script written (follows outline, uses teaching techniques)
- [ ] Script validated (facts checked, pedagogy sound)
- [ ] Script formatted (SSML tags, pronunciations)
- [ ] Audio/video generated (Autonoe voice)
- [ ] Episode page created (clean transcript, navigation)
- [ ] Course index updated
- [ ] Podcast feed updated
- [ ] Build successful, URLs work

### Common Mistakes to Avoid

**❌ No Curriculum Plan**:
- Jumping straight to writing scripts without curriculum
- Episodes don't build on each other
- No spaced repetition or review

**Fix**: Always use lesson-curriculum skill before writing first script

**❌ Podcast-Style Dialogue**:
- Using two-person conversation format
- Jordan/Alex speaker labels

**Fix**: Single presenter, natural lecture flow

**❌ Missing Pedagogical Elements**:
- No learning objectives
- No active recall moments
- No spaced repetition callbacks
- Passive information delivery

**Fix**: Use lesson-outline templates with required teaching techniques

**❌ Wrong Prerequisites**:
- Assuming knowledge not in previous episodes
- Not linking to prerequisite lessons

**Fix**: Validate prerequisites in lesson-validate skill

**❌ Missing Course Navigation**:
- Episode pages without prev/next links
- Not linked from course index

**Fix**: Use lesson-publish skill which handles all integrations

---

*For detailed course production workflows, curriculum templates, teaching techniques, and validation checklists, use the Claude Code skills in `.claude/skills/lesson-*`*
