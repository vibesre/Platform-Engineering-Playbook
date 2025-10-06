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

## The Platform Engineering Playbook - Podcast Script Guide

Create natural conversations between two experienced engineers for senior platform professionals (5+ years) seeking strategic insights on technology choices, market dynamics, and skill optimization.

### Core Requirements

**Audience**: Senior platform engineers, SREs, DevOps engineers who want nuanced comparisons and business context, not basic tutorials.

**Conversational Style**: True dialogue with natural interruptions, respectful disagreement, shared discoveries, and technical depth from production experience.

### Episode Structure (12-15 minutes)

1. **Cold Open Hook** (30s): Start mid-conversation with intriguing technical insight
2. **Landscape Overview** (3-4 min): Current state, market dynamics, design philosophy evolution
3. **Technical Deep Dive** (4-5 min): Compare 2-3 solutions from engineering and business perspectives
4. **Underdogs & Specialists** (2-3 min): Niche players, regional leaders, emerging solutions
5. **Skills Evolution** (3-4 min): What's table stakes, losing relevance, rising importance
6. **Practical Wisdom** (2 min): Architectural mistakes, evaluation frameworks, boring tech principle
7. **Closing Thoughts** (1 min): Key insight, actionable takeaway

### Natural Conversation Techniques

- **Building Momentum**: "You mentioned X earlier..." → "Oh yeah, that's a perfect example..."
- **Respectful Disagreement**: "I'm not sure I fully agree..." → "How so?" → Context-specific perspectives
- **Shared Learning**: "Wait, they're doing WHAT...?" → "I know, right? It sounds crazy until..."
- **Technical Storytelling**: Reference real incidents, production failures, architectural decisions

### Always Cover

1. **Design Philosophy**: Original problems and solutions
2. **Evolution**: How they've adapted to changing needs  
3. **Trade-offs**: What you give up for benefits
4. **Operational Reality**: Production experience
5. **Team Impact**: Organizational effects
6. **Future Direction**: Where technology is heading

### Avoid

- Basic explanations, absolute statements, marketing speak
- Installation guides, outdated information
- Focus on features over strategic implications

### Research Sources

- Production postmortems, engineering blogs from scale companies
- GitHub issues, practitioner conference talks (not vendor pitches)
- Job postings, compensation data for skill demand analysis

### Show Branding

**Name**: The Platform Engineering Playbook  
**Tagline**: "Where we dissect the technologies, trends, and decisions that shape platform engineering at scale"

**Standard Intro**:
```
Speaker 1: [Cold open hook - mid-conversation technical insight]
Speaker 2: [Build on hook] Welcome to The Platform Engineering Playbook - I'm Jordan.
Speaker 1: I'm Alex. This is the show where we dissect the technologies, trends, and decisions that shape platform engineering at scale.
Speaker 2: [Episode preview]
```

**Standard Outro**:
```
Speaker 2: [Key takeaway from conversation]
Speaker 1: The fundamentals of good engineering remain constant, even as the landscape evolves.
Speaker 2: That's what we're here for - cutting through the noise to help you make better decisions for your teams and your career.
Speaker 1: Thanks for tuning in to The Platform Engineering Playbook. Keep building thoughtfully.
Speaker 2: Until next time.
```

**Episode Naming**: "[Technology] - The Real Story Behind [Key Insight]"

**Voice**: Two experienced engineers having a coffee chat about strategic technology decisions

### Script Format & TTS Guidelines

**Raw Script Format** (stored in `docs/podcasts/scripts/`):
```
Speaker 1: [First speaker's dialogue]
Speaker 2: [Second speaker's dialogue]
Speaker 1: [Continuation...]
```

**Pause Tags** (Chirp3-HD Markup):
- System automatically adds `[pause]` between speaker changes
- Manual tags available: `[pause short]`, `[pause]`, `[pause long]`
- Example: "Let me think, [pause long] yes, that makes sense."
- Use sparingly - only for emphasis or dramatic effect

**Chunking Rules**:
- Chunks NEVER break within a speaker's segment
- Only chunk at speaker boundaries (Speaker 1 → Speaker 2 transitions)
- Target: 100 words, Max: 200 words per chunk
- Preserves natural conversation flow

**TTS Best Practices** (Google Cloud Chirp3-HD):
- Uses `markup` field (not `text`) to support pause tags
- Sample rate: 24kHz (natural Chirp3-HD rate)
- Audio profile: `headphone-class-device` (optimized for podcast listening)
- Voices: Jordan (Kore), Alex (Orus) - both 9/10 quality
- Speaking rates: Jordan 0.95x, Alex 1.0x
- NO speaker names spoken in audio (handled by voice selection)

**Generation Command**:
```bash
cd podcast-generator
python3 scripts/generate_podcast.py ../docs/podcasts/scripts/episode-name.txt --force
```

---

## Podcast Episode Page Format (docs/podcasts/*.md)

**REQUIRED** format for all published podcast episode pages. All episodes MUST follow this exact structure:

### Frontmatter
```yaml
---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ [Episode Title]"
---
```

### Page Header (EXACT format)
```markdown
# [Full Episode Title] - [Subtitle]

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** [X-Y minutes or X minutes]
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post/technical guide]**: [Link Title](URL) - Brief description of related content.

---
```

### Required Elements Checklist
- [ ] Frontmatter with `sidebar_label: "🎙️ [Title]"`
- [ ] H1 title with full episode name
- [ ] `## The Platform Engineering Playbook Podcast`
- [ ] `<GitHubButtons />` on its own line
- [ ] `**Duration:**` with NO trailing spaces
- [ ] `**Speakers:** Alex and Jordan`
- [ ] `**Target Audience:**` exact text as above
- [ ] Blockquote with 📝 emoji (consistent across all episodes)
- [ ] Horizontal rule `---` after metadata

### Content Sections
Follow the dialogue from the script with section headers like:
- `### Cold Open`
- `### [Topic Name]`
- `### Closing Thoughts`

Format dialogue as:
```markdown
**Alex**: Dialogue text here.

**Jordan**: Response text here.
```

### File Organization
- **MD file**: `docs/podcasts/episode-name.md` (no prefix)
- **Script file**: `docs/podcasts/scripts/00001-episode-name.txt` (with 5-digit prefix)
- **Metadata file**: `docs/podcasts/metadata/episode-name.json` (no prefix)

### Creating New Episodes
1. Increment episode number: `00004`, `00005`, etc.
2. Create script: `docs/podcasts/scripts/00004-new-episode.txt`
3. Create metadata: `docs/podcasts/metadata/new-episode.json`
4. Create MD page: `docs/podcasts/new-episode.md` (use template above)
5. Add to sidebar: `sidebars.ts` → `podcasts/new-episode`
6. **CRITICAL**: Cross-link podcast and blog post (see below)

### Cross-Linking Requirement (MANDATORY)

**When creating a podcast episode with a corresponding blog post, you MUST cross-link them in both directions:**

#### In the Blog Post (after intro, before Quick Answer):
```markdown
> 🎙️ **Listen to the podcast episode**: [Episode Title](/podcasts/episode-name) - Brief description highlighting conversation format and key topics.
```

**Example:**
```markdown
> 🎙️ **Listen to the podcast episode**: [PaaS Showdown 2025: Flightcontrol vs Vercel vs Railway vs Render vs Fly.io](/podcasts/paas-showdown-episode) - A deep dive conversation exploring these platforms with real-world pricing examples and decision frameworks.
```

#### In the Podcast Page (in metadata section after speakers):
```markdown
> 📝 **Read the [full blog post](/blog/blog-post-slug)**: Brief description highlighting written format and comprehensive analysis.
```

**Example:**
```markdown
> 📝 **Read the [full blog post](/blog/2025-10-paas-showdown-flightcontrol-vercel-railway-render-fly)**: Deep dive into pricing, technical trade-offs, and decision frameworks for choosing the right PaaS platform.
```

**Why This Matters:**
- Gives users choice of format (audio vs written)
- Improves SEO through internal linking
- Increases content engagement and time on site
- Creates a cohesive content experience

**Checklist for New Content:**
- [ ] Blog post links to podcast episode (if one exists)
- [ ] Podcast page links to blog post (if one exists)
- [ ] Links use emoji indicators (🎙️ for podcast, 📝 for blog)
- [ ] Descriptions are unique and value-focused
- [ ] Links tested and working

---

*End of Podcast Script Guide*