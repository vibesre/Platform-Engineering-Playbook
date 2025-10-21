---
name: Podcast Research
description: Research and validate podcast topics by analyzing community discussions, trending technologies, and market dynamics for the Platform Engineering Playbook podcast.
allowed-tools: WebSearch, WebFetch, Grep, Read, Glob
---

# Podcast Research

Research and validate potential podcast topics for the Platform Engineering Playbook by analyzing community sentiment, identifying pain points, and gathering supporting data.

## When to Use This Skill

Use this skill when:
- Starting a new podcast episode and need to identify relevant topics
- User asks: "What should I cover in the next podcast?" or "Find trending platform engineering topics"
- Validating if a topic has enough depth and community interest
- Gathering evidence to support episode themes

## Target Audience

Senior platform engineers, SREs, DevOps engineers (5+ years experience) who value:
- Technical depth over surface-level coverage
- Honest trade-off analysis over hype
- Real-world practicality over theoretical ideals
- Data-driven decision making

## Research Process

### 1. Identify Topic Categories

Focus on these areas:
- **Technology Comparisons**: Cloud platforms, PaaS solutions, observability tools, CI/CD platforms
- **Market Dynamics**: Pricing wars, consolidation trends, emerging vs established players
- **Skills Evolution**: What's table stakes, what's declining, what's rising
- **Architectural Patterns**: Design philosophy evolution, production lessons learned
- **Business Context**: Build vs buy decisions, TCO analysis, team impact

### 2. Community Analysis

Search for discussions in:
- **Reddit**: r/devops, r/kubernetes, r/aws, r/sre
- **Hacker News**: Technology launches, post-mortems, "Ask HN" threads
- **GitHub Issues**: Popular repositories, feature requests, pain points
- **Engineering Blogs**: Companies at scale sharing production insights
- **Conference Talks**: Practitioner talks (NOT vendor pitches)

### 3. Look for Signal Patterns

Strong topics have:
- **Recent urgency**: "We're facing this NOW" discussions (last 3-6 months)
- **Emotional language**: Frustration, surprise, excitement in comments
- **Disagreement**: Multiple perspectives, respectful debate
- **Concrete examples**: "At $COMPANY we saw X" with specific numbers
- **Repeat mentions**: Same pain points across multiple forums

Weak topics have:
- Only vendor marketing content
- No practitioner discussion or real-world examples
- Consensus without nuance ("everyone agrees X is best")
- Theoretical only (no production experience)

### 4. Validate Depth

A good topic should support 12-15 minutes of discussion covering:
- Design philosophy and evolution
- 2-3 specific solutions/approaches to compare
- Trade-offs and operational reality
- Team/organizational impact
- Skills implications
- Future direction

### 5. Gather Supporting Evidence

Collect:
- **Statistics**: Adoption numbers, market share, growth rates (with sources)
- **Pricing data**: Real costs from vendor sites (note the date)
- **Technical details**: Architecture differences, feature comparisons
- **Case studies**: Real companies with specific outcomes
- **Expert opinions**: Quotes from practitioners (with attribution)

## Output Format

Produce a **Topic Brief** with this structure:

```markdown
# Podcast Topic Brief: [Topic Name]

## Summary
[2-3 sentences: What this topic is about and why it matters NOW]

## Target Audience Relevance
[Why senior platform engineers care about this]

## Community Signal Strength
- **Reddit discussions**: [X threads, key themes]
- **Hacker News**: [X stories, top comment themes]
- **GitHub issues**: [Repos and pain points]
- **Engineering blogs**: [Companies discussing this]

## Key Tensions/Questions to Explore
1. [Question that creates natural debate]
2. [Trade-off worth exploring]
3. [Surprising insight or counterintuitive finding]

## Supporting Data
- [Statistic with source link]
- [Pricing example with source link]
- [Adoption metric with source link]

## Potential Episode Structure
- **Landscape Overview**: [What we'd cover]
- **Technical Deep Dive**: [2-3 solutions to compare]
- **Skills Evolution**: [What this means for careers]
- **Practical Wisdom**: [Decision frameworks, mistakes to avoid]

## Sources to Consult
- [Engineering blog URL with brief description]
- [Reddit thread URL with key insight]
- [GitHub repo/issue URL with context]
- [Conference talk URL with speaker/topic]

## Topic Strength Assessment
**Depth**: [1-5 rating] - Can support 12-15 min discussion
**Timeliness**: [1-5 rating] - Relevant NOW, not 2 years ago
**Debate**: [1-5 rating] - Multiple valid perspectives
**Actionability**: [1-5 rating] - Listeners can apply insights

**Overall**: [STRONG/MODERATE/WEAK] - [Recommendation]
```

## Quality Checks

Before finalizing research:
- [ ] At least 3 independent sources of community discussion
- [ ] At least 2 primary sources (official docs, company blogs)
- [ ] Specific statistics with source links
- [ ] Clear tension/debate that creates conversation
- [ ] Relevant to senior engineers (not beginner topics)
- [ ] Timely (discussed in last 6 months)

## Research Sources to Use

**Community Platforms**:
- Reddit: r/devops, r/kubernetes, r/aws, r/sre, r/terraform
- Hacker News: Use "site:news.ycombinator.com [topic]"
- GitHub: Issues, discussions in major repos

**Industry Sources**:
- The New Stack, InfoQ, Ars Technica (tech journalism)
- Vendor engineering blogs (AWS, Google, Microsoft, HashiCorp)
- Scale companies (Airbnb, Uber, Netflix engineering blogs)
- CNCF blog, KubeCon talks

**Data Sources**:
- GitHub stars/forks/contributors for popularity
- Job postings for skill demand
- Vendor pricing pages (always note the date)
- Published case studies with metrics

## Anti-Patterns to Avoid

- Relying solely on vendor marketing content
- Topics with only theoretical discussion (no production use)
- Rehashing 101-level content ("What is Kubernetes?")
- Topics where consensus is complete (no debate = boring)
- Trends that peaked 2+ years ago

## Example Research Output

**Topic**: "PaaS Showdown 2025: Modern Heroku Alternatives"

**Community Signal**: 15+ Reddit threads in r/devops debating Flightcontrol, Vercel, Railway pricing vs AWS complexity. Common theme: "How can I justify $400/month to my CTO?"

**Key Tension**: Apparent high cost vs hidden costs of self-managed infrastructure. Economic detective story potential.

**Supporting Data**:
- Flightcontrol pricing: $397/month (verified 2025-10-15)
- Reddit thread: "Paid $15K in engineer time vs $400 platform fee" (125 upvotes)
- 5 engineering blogs discussing PaaS ROI with specific numbers

**Episode Angle**: Economic detective story - why the "expensive" option often saves money when you factor in total cost.

**Strength**: 5/5 depth, 5/5 timeliness, 4/5 debate, 5/5 actionability = STRONG

---

## Instructions for Claude

When this skill is invoked:

1. Ask the user if they have a specific topic in mind or want you to discover trending topics
2. Search community platforms (Reddit, HN, GitHub) for recent discussions
3. Identify patterns in community sentiment and pain points
4. Gather supporting data (statistics, pricing, case studies)
5. Validate the topic has sufficient depth and timeliness
6. Produce a Topic Brief following the format above
7. Give a clear recommendation: STRONG/MODERATE/WEAK

Always prioritize:
- Primary sources over secondary reporting
- Practitioner insights over vendor marketing
- Recent discussions (last 6 months) over historical
- Concrete examples with numbers over generic claims

The research phase sets the foundation for a compelling, relevant episode. Don't rush it.
