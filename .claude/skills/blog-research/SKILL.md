# Blog Research

Research and validate blog post topics by analyzing community discussions, identifying pain points, gathering high-quality sources, and performing keyword research for maximum SEO/AEO impact.

## When to Use This Skill

Use this skill when:
- User says: "Research blog topic about [X]", "Find sources for blog post"
- Starting a new blog post project
- Need to validate a topic idea
- Gathering statistics and sources

**Prerequisites**: None - this is the first step in blog production.

## Research Standards

**CRITICAL**: All blog posts must be thoroughly researched and fact-checked before publication. The Platform Engineering Playbook's reputation depends on accuracy and trustworthiness.

###Source Verification (REQUIRED)

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

## Research Workflow

### Phase 1: Topic Validation

**Determine if topic is worth writing about:**

1. **Search for existing content**:
   ```bash
   # Check if topic already exists in blog
   grep -r "topic keyword" blog/
   grep -r "topic keyword" docs/
   ```

2. **Assess market demand**:
   - Search Google for "[topic] 2025" - how many recent results?
   - Check Reddit r/devops, r/kubernetes, r/sre for discussions
   - Search Hacker News for related threads
   - Look at Stack Overflow question frequency

3. **Identify knowledge gaps**:
   - What questions aren't being answered?
   - What misconceptions exist?
   - Where is data missing or outdated?

**Decision Criteria**:
- ✅ Proceed if: Topic has demand, knowledge gap exists, you can add unique value
- ❌ Skip if: Topic saturated, no new insights possible, already covered well

### Phase 2: Source Gathering

**Goal**: Collect 10-20 high-quality sources for a comprehensive blog post.

**Source Checklist** (aim for 3+ in each category):

**Statistics & Data**:
- [ ] Industry reports (Gartner, Forrester, DORA, State of DevOps)
- [ ] Survey results with sample sizes
- [ ] GitHub repository metrics (stars, forks, contributors)
- [ ] Company case studies with numbers

**Technical References**:
- [ ] Official documentation
- [ ] Engineering blog posts from companies using the technology
- [ ] Conference talks (YouTube, with speaker credentials)
- [ ] Technical specifications or RFCs

**Expert Insights**:
- [ ] Quotes from practitioners (with attribution)
- [ ] Real-world failure stories
- [ ] Production experience reports
- [ ] Cost breakdowns with context

**Example Research Report** (from Platform Failures post):
```markdown
## Research Report: Platform Engineering Failures

### Topic Validation
- **Demand**: High - Reddit discussions show confusion about why platforms fail
- **Gap**: Most content focuses on "how to build" not "why they fail"
- **Unique Value**: We can provide data-driven failure analysis with metrics

### Key Statistics Found
1. 60-70% failure rate - Source: Multiple platform engineering reports
2. 45% disbanded within 18 months - Source: [Humanitec/Team Topologies survey]
3. Only 33% have PMs - Source: [CNCF Platform Engineering Report]
4. Spotify 99% adoption vs 10% external - Source: [Spotify Engineering Blog]
5. DORA: 8% throughput drop, 14% stability drop - Source: [2024 DORA Report]

### Sources Collected (14 total)
**Primary Research**:
- 2024 DORA Report
- CNCF Platform Engineering Survey
- Humanitec/Team Topologies Platform Report
- Spotify Engineering Blog (Backstage case study)

**Case Studies**:
- Knight Capital $440M failure
- Multiple anonymous platform team failures (verified through interviews)

**Technical References**:
- Backstage documentation
- Platform as a Product literature

**Status**: Ready for outline phase - sufficient sources, data verified
```

### Phase 3: Keyword Research

**Goal**: Identify 8-12 keywords for SEO optimization and AI engine citations.

**Keyword Categories**:

1. **Primary Keyword** (exact match intent):
   - Example: "why platform engineering teams fail"
   - High search volume, matches user intent directly

2. **Long-Tail Variations** (3-5 keywords):
   - Example: "platform team disbanded"
   - Example: "platform engineering mistakes"
   - Example: "platform engineering anti-patterns"

3. **Question-Based** (2-3 keywords):
   - Example: "how long does it take for a platform team to fail"
   - Example: "what percentage of platform teams have product managers"

4. **Related Technical Terms** (2-3 keywords):
   - Example: "platform engineering ROI"
   - Example: "platform as a product"
   - Example: "platform engineering adoption"

**Keyword Research Process**:

```bash
# 1. Use Google's "People also ask" section
# Search for primary keyword, note related questions

# 2. Check Google autocomplete
# Type primary keyword + "how", "why", "what", etc.

# 3. Analyze competitors
# View source of top-ranking pages, find their keywords

# 4. Use related searches
# Bottom of Google results page

# 5. Check Reddit/Stack Overflow
# See how people actually phrase questions
```

**Keyword Selection Criteria**:
- Specific enough to rank (avoid "platform engineering" alone)
- Matches user intent (informational vs commercial)
- Has search volume (use Google Trends to verify)
- You can provide better answer than current results

**Example Keyword Analysis**:
```
Primary: "why platform engineering teams fail"
- Volume: Medium (500-1K/month estimated)
- Competition: Low (few comprehensive answers)
- Intent: Informational (seeking understanding)
- Value: High (decision-makers searching)

Long-tail: "platform team disbanded"
- Volume: Low (50-100/month)
- Competition: Very low
- Intent: Problem validation
- Value: High (specific pain point)

Question: "what metrics should platform teams measure"
- Volume: Low-Medium
- Competition: Low
- Intent: Solution-seeking
- Value: Very High (actionable)
```

### Phase 4: FAQ Schema Questions

**Goal**: Identify 5-10 common questions for FAQ schema (boosts AI citations).

**FAQ Question Sources**:
1. Google "People also ask" section
2. Reddit threads (r/devops, r/kubernetes, r/sre)
3. Stack Overflow top questions on topic
4. Quora discussions
5. Twitter/X conversations

**FAQ Quality Criteria**:
- Common question (asked frequently)
- Has clear, factual answer
- Can be answered in 2-3 sentences
- Includes specific data/numbers
- AI-friendly (standalone, no pronouns)

**Example FAQ Research**:
```markdown
## FAQ Questions Identified (Platform Failures)

1. "Why do platform engineering teams fail?"
   - Source: Reddit r/devops top question
   - Answer: Data-driven (60-70%, lack of PM)

2. "How long does it take for a platform team to fail?"
   - Source: Stack Overflow discussions
   - Answer: Specific (45% within 18 months)

3. "What percentage of platform teams have product managers?"
   - Source: CNCF report finding
   - Answer: Concrete (33% have, 52% say crucial)

4. "Do platform teams improve developer productivity?"
   - Source: DORA Report surprising finding
   - Answer: Counterintuitive (initially decrease 8%/14%)

5. "When should you NOT build a platform team?"
   - Source: Common mistake in community
   - Answer: Practical (under 100 engineers)

**Status**: 5 strong FAQs identified, ready for frontmatter
```

### Phase 5: Learning Resources Collection

**Goal**: Find 5-10 high-quality resources readers can use to learn more.

**Resource Categories**:

1. **Official Documentation** (1-2):
   - Primary source for the technology
   - API references, guides

2. **Tutorials & Guides** (2-3):
   - Comprehensive walkthroughs
   - Include publication date
   - Prefer recent (within 2 years)

3. **Books** (1-2):
   - Authoritative references
   - **Include purchase links** (Amazon, O'Reilly, publisher)
   - Only include free versions if officially provided

4. **Video Courses/Talks** (1-2):
   - Conference presentations
   - Include duration
   - Verify speaker credentials

5. **Community Resources** (1-2):
   - Active Discord/Slack
   - GitHub Discussions
   - Forums with participation metrics

**Resource Quality Checklist**:
- [ ] Link works and is accessible
- [ ] Content is current (updated within 2 years)
- [ ] Author/organization has credibility
- [ ] Comprehensive (not just marketing)
- [ ] Prefer official domains (not Medium/personal blogs)

**Example Learning Resources Collection**:
```markdown
## Learning Resources (Platform Failures)

### Books
- "Team Topologies" by Matthew Skelton, Manuel Pais - [Amazon](url) | [O'Reilly](url)
- "Platform Engineering on Kubernetes" by Mauricio Salatino - [Manning](url)

### Industry Reports
- DORA State of DevOps Report 2024 - [Free PDF](url)
- CNCF Platform Engineering Survey - [Results](url)

### Case Studies
- Spotify Backstage Journey - [Engineering Blog](url)
- Humanitec Platform Success Stories - [Case Studies](url)

### Tools Referenced
- Backstage - [Official Docs](url) | [GitHub](url) (26k⭐)

**Status**: 8 high-quality resources collected
```

## Research Output Checklist

Before proceeding to outline phase, verify:

**Topic Validation**:
- [ ] Demand validated (search volume, community discussions)
- [ ] Knowledge gap identified
- [ ] Unique value proposition clear

**Sources**:
- [ ] 10+ high-quality sources collected
- [ ] All statistics have primary source links
- [ ] Mix of data, technical refs, and expert insights
- [ ] Pricing/features verified on official sites

**Keywords**:
- [ ] 8-12 keywords identified
- [ ] Primary keyword has search volume
- [ ] Long-tail variations included
- [ ] Question-based keywords found

**FAQ Questions**:
- [ ] 5-10 questions identified
- [ ] All have factual, data-driven answers
- [ ] Sourced from Google/Reddit/Stack Overflow
- [ ] AI-friendly phrasing (standalone)

**Learning Resources**:
- [ ] 5-10 resources vetted
- [ ] All links tested and working
- [ ] Mix of categories (docs, books, videos)
- [ ] Current and credible

**Research Report Created**:
- [ ] Topic validation summary
- [ ] Key statistics list with sources
- [ ] Source categorization
- [ ] Keyword list
- [ ] FAQ questions
- [ ] Learning resources
- [ ] Ready for outline phase

## Example: Complete Research Workflow

**User Request**: "Research blog topic about platform engineering failures"

**Step 1: Topic Validation**
```bash
# Check existing content
grep -r "platform.*fail" blog/
# Result: No existing content on failures

# Assess demand
# Reddit r/devops: Multiple threads asking "why do platforms fail?"
# Stack Overflow: 50+ questions about platform adoption issues
# Decision: High demand, knowledge gap exists - PROCEED
```

**Step 2: Source Gathering** (WebSearch/WebFetch)
- Search: "platform engineering failure rate 2024"
- Search: "platform team disbanded statistics"
- Search: "Spotify Backstage adoption rate"
- Search: "DORA platform engineering report 2024"
- Found: 14 high-quality sources with data

**Step 3: Keyword Research**
- Google autocomplete for "platform engineering"
- Found: "why platform engineering teams fail", "platform team disbanded"
- Reddit analysis: "platform engineering mistakes", "platform engineering anti-patterns"
- Selected: 10 keywords covering informational and problem-solving intent

**Step 4: FAQ Identification**
- Google "People also ask": 3 questions found
- Stack Overflow top questions: 2 questions
- Reddit common themes: 3 questions
- Selected: 8 FAQs with data-driven answers

**Step 5: Learning Resources**
- Official: Backstage docs, Platform Engineering guides
- Books: Team Topologies, Platform Engineering on Kubernetes
- Reports: DORA 2024, CNCF Platform Survey
- Total: 8 vetted resources

**Output**: Research report ready → Proceed to blog-outline skill

---

## Instructions for Claude

When this skill is invoked:

1. **Understand the topic**:
   - Ask clarifying questions if topic is vague
   - Confirm scope (technical depth, target audience)

2. **Validate topic demand**:
   - Search for existing coverage
   - Check community discussions (Reddit, Stack Overflow)
   - Identify knowledge gaps

3. **Gather sources** (aim for 15+):
   - Use WebSearch for recent reports, statistics
   - Use WebFetch for detailed source reading
   - Categorize: Statistics, Technical, Expert insights
   - Verify all links work

4. **Perform keyword research**:
   - Use Google autocomplete
   - Check "People also ask"
   - Analyze Reddit/Stack Overflow phrasing
   - Select 8-12 keywords (primary + long-tail + questions)

5. **Identify FAQ questions**:
   - Extract from Google "People also ask"
   - Find top Stack Overflow/Reddit questions
   - Ensure answers are data-driven
   - Write in AI-friendly format

6. **Collect learning resources**:
   - Official docs first
   - Books with purchase links
   - Recent tutorials/videos
   - Verify all links

7. **Create research report**:
   - Topic validation summary
   - Statistics with sources
   - Keyword list
   - FAQ questions
   - Learning resources
   - Readiness assessment

8. **Report to user**:
   - Research complete with X sources
   - Y keywords identified
   - Z FAQ questions ready
   - Learning resources vetted
   - Next step: Use blog-outline skill

**Remember**: Quality over quantity. 10 excellent sources beat 50 mediocre ones. Every statistic MUST have a verifiable primary source.
