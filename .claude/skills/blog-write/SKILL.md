# Blog Write

Write comprehensive, fact-checked blog posts optimized for SEO/AEO following the Platform Engineering Playbook's content standards. The Platform Engineering Playbook's reputation depends on technical accuracy and trustworthy information.

## When to Use This Skill

Use this skill when:
- User says: "Write a blog post about...", "Create blog content for..."
- Converting podcast episode or lesson content into long-form article
- Need to create detailed technical content with proper SEO optimization

**Prerequisites**: Research should be completed (use podcast-research or general research). If writing from podcast, outline and script should exist.

## Core Principles

### Why This Matters

**One inaccurate statistic destroys trust.**

The blog targets senior engineers who:
- Spot inaccuracies immediately
- Value data-driven decision making
- Distrust marketing hype
- Rely on us for accurate information

### Writing Standards

1. **Every statistic must be verifiable and sourced**
2. **Technical claims must match official documentation**
3. **Include 5-7 Key Takeaway boxes** throughout (💡)
4. **SEO/AEO optimized** (Quick Answer, FAQ schema, statistics table)
5. **Cross-link to podcast episode** if one exists
6. **Honest about trade-offs** (not one-sided)

## Blog Post Structure (MANDATORY)

### 1. Frontmatter (SEO & AEO Optimization)

```yaml
---
title: "[Technology/Topic] - [Value Prop] [Year if relevant]"  # 50-60 chars
description: "150-160 char with key features and interview mention"
keywords:
  - primary keyword
  - technology tutorial
  - interview questions
  - related technologies
  # 8-12 keywords total
datePublished: "YYYY-MM-DD"
dateModified: "YYYY-MM-DD"
schema:
  type: TechArticle  # or FAQPage, HowTo
  questions:
    - question: "Common question about the technology?"
      answer: "Concise factual answer with specific data"
    # 5-10 Q&As for high-traffic pages
---
```

**Frontmatter Checklist**:
- [ ] Title 50-60 characters
- [ ] Description 150-160 characters
- [ ] 8-12 relevant keywords as array
- [ ] datePublished (current date)
- [ ] dateModified (same as published initially)
- [ ] Schema type (TechArticle, FAQPage, or HowTo)
- [ ] 5-10 FAQ questions with direct answers

### 2. Hook Paragraph (First 100 Words)

Start with:
- Surprising statistic or provocative question
- Establish why this matters NOW
- Preview value reader will get
- Use concrete examples over abstractions

**Example**:
> October 19, 2025, 11:48 PM. Ring doorbells stopped recording. Robinhood froze trading. Roblox kicked off millions of players. All at once.
>
> Six and a half million outage reports flooded Downdetector. This wasn't hardware failure or human error—it was a DNS race condition that exposed a truth most platform engineers didn't want to face.

### 3. Cross-Link to Podcast (If Exists)

**MANDATORY if podcast episode exists**:

```markdown
> 🎙️ **Listen to the podcast episode**: [Episode Title](/podcasts/00XXX-name) - Brief description highlighting conversation format.
```

### 4. Quick Answer (TL;DR)

**Required Elements**:
- **Problem**: One sentence
- **Solution/Root Cause**: One sentence with key technical details
- **Cost/Impact**: Specific numbers
- **Timeline**: Implementation/resolution time
- **Key Takeaway**: Action item or decision point

**Must be**:
- Factual and standalone (no pronouns)
- Include real statistics
- Provide specific timelines
- Easy for AI engines to parse and cite

**Example**:
```markdown
## Quick Answer (TL;DR)

**Problem**: A DNS race condition in DynamoDB triggered a 14-hour outage affecting 70+ AWS services globally.

**Root Cause**: Dual DNS Enactors designed for redundancy created a timing vulnerability. Unusual delays caused one to overwrite active DNS plan with stale data.

**Cost**: $75M/hour aggregate across companies. $728K for a single application's 130-minute outage.

**Timeline**: 14 hours (Oct 19, 11:48 PM to Oct 20, 2:20 PM PDT)

**Key Takeaway**: US-EAST-1 handles 35-40% of global AWS traffic and serves as control plane for most customers. Multi-region workloads still depend on it.
```

### 5. Key Statistics Table (REQUIRED)

**Place immediately after Quick Answer**:

```markdown
## Key Statistics (2024-2025 Data)

| Metric | Value | Source |
|--------|-------|--------|
| Stat 1 | Value with context | [Source Name](url) |
| Stat 2 | Value with context | [Source Name](url) |
# 8-12 rows of key data
```

**Requirements**:
- Every statistic MUST have a source link
- Include dates for time-sensitive data
- Use specific numbers (not "many" or "most")
- Context in value column (e.g., "35-40% of global AWS traffic")

### 6. Main Content Sections

**Structure**:
- H2 headers for major sections
- H3 subheaders every 300-400 words
- One Key Takeaway box every 800-1000 words
- Internal links to related content (5+ minimum)

**Section Types**:
- Timeline/Background
- Technical Deep Dive
- Cost Analysis
- Practical Implications
- Action Items

**Key Takeaway Box Format**:
```markdown
> **💡 Key Takeaway**
>
> [Major insight with specific data that AI can cite. Should be standalone and quotable.]
```

**Requirements for Key Takeaways**:
- 5-7 boxes throughout post
- Each contains ONE major insight
- Include specific data/numbers
- Standalone (no "as mentioned above")
- Actionable or decision-framing

### 7. Practical Action Items

**Include section with concrete steps**:
- For individual engineers
- For platform teams
- For leadership

**Format**:
```markdown
## Practical Actions This Week

### For Individual Engineers
- Specific action 1
- Specific action 2

### For Platform Teams
1. This week: [immediate actions]
2. Next month: [follow-up actions]

### For Leadership
**The Argument**: [Business case]
**The Ask**: [Specific budget/resources]
**The Timeline**: [Phased approach]
```

### 8. Learning Resources (REQUIRED)

**Minimum 5 high-quality resources**:

```markdown
## 📚 Learning Resources

### Official Documentation & Postmortems
- [Resource 1](url) - Brief description

### Technical Analysis
- [Resource 2](url) - What it covers

### Resilience Engineering
- "Book Title" by Author - [Purchase on Amazon](url)

### Community Discussion
- [Forum/Discussion](url) - Brief description
```

**Quality Criteria**:
- [ ] Official docs linked
- [ ] Current (updated within 2 years)
- [ ] Author/org has credibility
- [ ] Accessible (not hard paywall)
- [ ] Books have purchase links

### 9. Related Content Links (End of Post)

**Link to 3-5 related articles**:
```markdown
**Related Content**:
- [Related Technical Page](/technical/topic)
- [Related Blog Post](/blog/related-post)
- [Related Podcast](/podcasts/00XXX-name)
```

## Content Quality Standards

### Writing for Engagement

**Opening Hook**:
- Surprising statistic or provocative question
- Why this matters NOW
- Preview of value
- Concrete examples

**Story-Driven Content**:
- Real-world case studies with specific numbers
- "Before/After" scenarios
- Problem → Analysis → Solution structure
- Practitioner quotes with attribution

**Maintaining Interest**:
- Vary sentence length (mix short and long)
- Subheadings every 300-400 words
- Include visuals (tables, comparisons)
- Key Takeaway boxes every 800-1000 words
- Use specifics over generics
- Address reader directly ("You're probably facing...")

**Avoid**:
- Walls of text without breaks
- Abstract concepts without examples
- Jargon without explanation
- Burying the lede (put value early)

### Voice & Tone (from CLAUDE.md)

**Target Audience**: Senior platform engineers (5+ years experience)

**Voice Characteristics**:
- Authoritative but humble (share expertise without arrogance)
- Honest about trade-offs (every solution has pros/cons)
- Practical over academic (focus on production reality)
- Skeptical of hype (question marketing, demand evidence)
- Respectful of intelligence (don't over-explain basics)

**Example of Good Tone**:
> "Flightcontrol promises Heroku-like simplicity. At $397/month, that's a premium over self-managed infrastructure. But when you factor in engineering time saved—and opportunity cost of not shipping features—the math starts to look different."

**Example of Bad Tone**:
> "Flightcontrol is an amazing platform that revolutionizes deployment! It's the perfect solution for everyone!"

## Fact-Checking Process (MANDATORY)

### Before Publishing

**Verify EVERY**:
- [ ] **Statistic** - Find original source, check date, verify context
- [ ] **Quote** - Confirm exact wording, verify attribution
- [ ] **Technical claim** - Test if possible, or find multiple sources
- [ ] **Pricing** - Check vendor website, note date
- [ ] **Feature availability** - Verify in current documentation
- [ ] **Company data** - Cross-reference multiple sources

**Three-Source Rule**: Major claims need 3+ independent sources

**Recency Check**: Data >1 year old must be marked with date

**Original Source**: Always link to PRIMARY source, not secondary reporting

### Source Quality

**Primary Sources (Prefer These)**:
- Official documentation
- Published research papers (with DOI/URL)
- Company engineering blogs from practitioners
- Conference talks from engineers (not sales)
- GitHub repositories with real usage data

**Acceptable Secondary**:
- Reputable tech news (The New Stack, InfoQ, Ars Technica)
- Industry analyst reports (Gartner, Forrester) with dates
- High-quality community blogs with depth

**Unacceptable**:
- Marketing content without technical backing
- Unverified claims or rumors
- Outdated content (>2 years) as current
- AI-generated content without verification
- Anonymous sources without corroboration

## SEO/AEO Optimization Checklist

**Score your post (aim for 12/12)**:
- [ ] Has Quick Answer/TL;DR at top
- [ ] Has FAQ schema in frontmatter (5+ questions)
- [ ] Includes 2+ statistics with source links in table
- [ ] Has comparison table (if applicable)
- [ ] Includes date/year signals (datePublished, "2025 Guide")
- [ ] Has 5-7 Key Takeaway boxes (💡)
- [ ] Uses direct answer format (standalone sentences)
- [ ] Includes expert quotes or authoritative references
- [ ] Has numbered action items or decision framework
- [ ] Standalone sentences AI can cite independently
- [ ] Includes decision framework ("Use X when...")
- [ ] Links to related internal content (5+ internal links)

## File Naming & Location

**File name format**: `YYYY-MM-DD-title-slug.md`

**Location**: `blog/YYYY-MM-DD-title-slug.md`

**Example**: `blog/2025-10-24-aws-us-east-1-outage-october-2025-postmortem-analysis.md`

## Production Workflow

### Step 1: Research & Source Gathering

**Use existing research if available**:
- Check podcast research notes
- Read podcast outline/script
- Review validation report

**Additional research**:
- Find official documentation
- Locate postmortems/technical analyses
- Gather statistics with sources
- Collect practitioner insights

**Create source list**: Document all URLs for citation

### Step 2: Structure Planning

**Outline major sections**:
- Hook paragraph
- Quick Answer
- Key Statistics table
- 3-5 main content sections
- Practical actions
- Learning resources

**Identify Key Takeaways**: Plan 5-7 major insights to highlight

**Plan internal links**: Which related content to cross-link?

### Step 3: Writing

**Start with frontmatter**: Get SEO right from beginning

**Write hook paragraph**: Spend time on first 100 words

**Fill Quick Answer**: Direct, factual, standalone

**Build statistics table**: Every stat needs a source

**Write main content**:
- One section at a time
- Add Key Takeaway boxes as you go
- Include internal links naturally
- Use subheadings frequently

**Add Learning Resources**: 5-10 high-quality resources

**Write action items**: Specific, concrete, segmented by audience

### Step 4: Review & Polish

**Fact-Check Review**:
- [ ] Every statistic has source link
- [ ] All technical claims verified
- [ ] Pricing current with dates
- [ ] No marketing speak without data

**SEO/AEO Review**:
- [ ] Score 10+/12 on optimization checklist
- [ ] Frontmatter complete
- [ ] FAQ schema populated
- [ ] Key Takeaways throughout

**Engagement Review**:
- [ ] Hook is compelling
- [ ] Subheadings every 300-400 words
- [ ] Specific examples used
- [ ] No walls of text
- [ ] Varied sentence length

**Links Review**:
- [ ] All external links working
- [ ] 5+ internal links included
- [ ] Cross-link to podcast (if exists)
- [ ] Related content linked at end

### Step 5: Cross-Linking

**If podcast episode exists**:
1. Add podcast link in blog post (after hook)
2. Add blog link in podcast episode page
3. Update both with cross-reference

**Format in blog**:
```markdown
> 🎙️ **Listen to the podcast episode**: [Title](/podcasts/00XXX-name) - Description.
```

**Format in podcast**:
```markdown
> 📝 **Read the [full blog post](/blog/YYYY-MM-DD-slug)**: Description.
```

## Common Mistakes to Avoid

**❌ Generic Opening**: "In today's fast-paced world of cloud computing..."
**✅ Specific Hook**: "October 19, 2025, 11:48 PM. Ring doorbells stopped recording..."

**❌ Unsourced Statistics**: "Most companies struggle with..."
**✅ Sourced Data**: "85% of organizations report challenges ([Source](url))"

**❌ Marketing Speak**: "Revolutionary platform that changes everything"
**✅ Honest Assessment**: "Reduces deployment time by 60%, but requires AWS expertise"

**❌ Vague Advice**: "You should consider multi-region architecture"
**✅ Specific Action**: "Schedule a DR drill this week: pretend US-EAST-1 is down. What breaks?"

**❌ Missing Context**: "Costs $397/month"
**✅ With Context**: "At $397/month base cost, compare to $150K/year DevOps engineer"

**❌ No Key Takeaways**: Just paragraphs of text
**✅ Highlighted Insights**: 5-7 💡 boxes with major insights

## Output Checklist

**Before publishing**:

- [ ] Frontmatter complete with all fields
- [ ] 50-60 char title, 150-160 char description
- [ ] 8-12 keywords array
- [ ] 5-10 FAQ questions in schema
- [ ] Hook paragraph (first 100 words) is compelling
- [ ] Cross-link to podcast if exists
- [ ] Quick Answer section complete
- [ ] Key Statistics table with 8-12 rows
- [ ] Every statistic has source link
- [ ] 5-7 Key Takeaway boxes throughout
- [ ] 5+ internal links to related content
- [ ] Practical action items (3 audiences)
- [ ] 5-10 learning resources with descriptions
- [ ] Related content links at end
- [ ] All external links tested
- [ ] Score 10+/12 on SEO/AEO checklist
- [ ] File named YYYY-MM-DD-title-slug.md
- [ ] Saved in blog/ directory

---

## Instructions for Claude

When this skill is invoked:

1. **Check prerequisites**:
   - Is research available? (podcast research, outline, script)
   - Does podcast episode exist? (will need cross-link)
   - What's the topic and angle?

2. **Gather research**:
   - Read podcast outline/script if available
   - Read validation report if available
   - Note all statistics and sources already gathered

3. **Plan structure**:
   - Outline major sections (3-5 main)
   - Identify 5-7 Key Takeaway boxes
   - Plan internal links (5+ minimum)

4. **Write frontmatter**:
   - Create compelling title (50-60 chars)
   - Write description (150-160 chars)
   - List 8-12 keywords
   - Create 5-10 FAQ questions/answers

5. **Write content**:
   - Hook paragraph (100 words)
   - Cross-link to podcast if exists
   - Quick Answer (TL;DR)
   - Key Statistics table (8-12 rows, all sourced)
   - Main content sections with Key Takeaways
   - Practical actions (3 audiences)
   - Learning resources (5-10 items)
   - Related content links

6. **Review**:
   - Run through fact-check checklist
   - Score on SEO/AEO checklist (aim for 10+/12)
   - Verify all links work
   - Check voice/tone matches guidelines

7. **Save file**:
   - Format: blog/YYYY-MM-DD-title-slug.md
   - Use Write tool

8. **Cross-linking** (if podcast exists):
   - Add podcast link in blog post
   - Add blog link in podcast episode page
   - Verify both links work

9. **Report to user**:
   - Blog post location
   - Word count and reading time
   - SEO/AEO score
   - Cross-links added
   - Next steps (review, publish)

**Remember**: One inaccurate statistic destroys trust. Verify everything before publishing.
