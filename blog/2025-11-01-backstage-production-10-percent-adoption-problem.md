---
slug: backstage-production-10-percent-adoption-problem
title: "Backstage in Production: The 10% Adoption Problem (2025 Reality Check)"
authors: [eric]
tags: [backstage, developer-portal, platform-engineering, idp, adoption, enterprise]
date: 2025-11-01
description: "Honest analysis of Backstage's adoption crisis: why 90% of your organization won't use your portal, the 7-15 FTE maintenance burden, and the decision framework for choosing Backstage vs Port/Cortex/custom alternatives in 2025."
keywords: [backstage production implementation, backstage adoption challenges, backstage vs port, backstage vs cortex, internal developer portal, backstage maintenance cost, developer portal alternatives, backstage enterprise deployment, backstage adoption fails, backstage production ready]
image: /img/blog/2025-11-backstage-adoption.jpg
---

Your team spent nine months implementing Backstage. The portal looks beautiful. You have 47 services cataloged. Internal adoption? **Eight percent**. Three developers use it regularly. The rest go directly to AWS console, kubectl, and GitHub.

Sound familiar? You're not alone. Backstage's own community acknowledges the **10% adoption problem**—average adoption stalls at 10% within organizations, and teams require 7-15 FTE to maintain it. Here's why it happens, and the decision framework I wish we'd had before investing 2 person-years of engineering time.

<!--truncate-->

## The Adoption Crisis Nobody Talks About

Spotify's VP of Engineering has publicly acknowledged it: while Backstage adoption is high internally at Spotify, it often **stalls at less than 10% in other organizations**. This isn't anecdotal—it's documented across the community, from HackerNews discussions to enterprise post-mortems.

### Why This Matters Now

The 2025 market now favors IDPs that deliver immediate value and faster ROI (Gartner's 2025 Market Guide for Internal Developer Portals). Backstage implementations that can't prove value quickly face existential threats—just like the [60-70% of platform teams that get disbanded](/blog/why-platform-engineering-teams-fail) for failing to prove business impact.

## The Real Numbers: What Backstage Actually Costs

Let's cut through the "open source is free" myth. Here's what Backstage actually costs for a mid-size organization (300 developers):

### Initial Implementation (Year 1)
- **Development team:** 7 FTEs (1 PM, 2 frontend, 2 full-stack, 2 DevOps) @ $150K/year each
- **Timeline:** 12 months
- **Total investment:** **$1,050,000**

### Ongoing Costs (Year 2+)
- **Development team:** 4 FTEs @ $600,000/year
- **Maintenance team:** 2 FTEs for platform management @ $300,000/year
- **Annual total:** **$900,000/year**

**Reality check:** Organizations that believe they can get positive ROI from Backstage with just 1-2 engineers have unrealistic expectations. At Spotify with 1,600 engineers, there was a full-time team of **four engineers** working on their IDP.

For an organization with 300 developers, you need between **7 and 15 engineers** to extract value from Backstage.

## Root Causes: Why Adoption Fails

### 1. Technical Complexity Barrier

**The Plugin Maze:**
- 70+ steps to basic setup
- 100+ plugins to evaluate
- React + Node + TypeScript required
- Custom plugin development = significant engineering investment

**Real impact:** Most backend engineers don't have React/TypeScript skills. Your platform team becomes a bottleneck for every integration.

### 2. The Data Quality Death Spiral

Backstage never fully addressed the fundamental challenge: **trusted, always-up-to-date data**. The catalog's data can quickly become stale and untrustworthy.

**The cycle:**
1. Engineers don't trust stale data
2. Engineers don't update the catalog
3. Data gets staler
4. Adoption drops further
5. Leadership questions the investment

### 3. Too Many Choices, Too Little Guidance

With **too much extensibility**, Backstage becomes overwhelming:
- Which plugins should we use?
- How do we configure authentication?
- What's the right deployment architecture?
- How do we handle upgrades?

**Result:** Teams get stuck in proof-of-concept limbo, failing to understand developer pain points and build the thinnest viable platform first.

### 4. Limited Stakeholder Value

Backstage's primary focus on the service catalog means it often fails to provide value to engineering leadership. Without exec-level metrics and insights, adoption remains a developer-only concern—and dies from lack of sponsorship.

## Decision Framework: Should You Use Backstage?

### ✅ When Backstage Makes Sense

Choose Backstage if you meet **ALL** of these criteria:

| Criterion | Threshold | Why It Matters |
|-----------|-----------|----------------|
| **Engineering team size** | 500+ engineers minimum | Smaller teams can't justify the maintenance overhead |
| **Frontend capability** | Strong React/TypeScript skills | Required for plugin development and customization |
| **Platform team commitment** | 7-15 dedicated FTEs | Anything less results in poor experience and low adoption |
| **Service catalog discipline** | Already exists | Backstage won't create discipline—it requires it |
| **Investment timeline** | 3-5 year commitment | ROI takes 18-24 months minimum |
| **Customization needs** | Unique requirements | If you need heavy customization, Backstage's flexibility pays off |

**Example success story:** 500-person company, 5 FTE team, 18-month timeline → **50% adoption** achieved. Key factors: dedicated team, clear use cases, executive sponsorship.

### ❌ When to Choose Alternatives

Avoid Backstage if you have:

- **Under 500 engineers** → Use Port, Cortex, or custom portal
- **Limited frontend skills** → Use no-code alternatives (Port, OpsLevel)
- **Need fast time-to-value** (under 6 months) → Commercial solutions start faster
- **Can't dedicate 7+ FTE** to maintenance → Managed alternatives reduce ops burden
- **No service catalog** → Chicken-egg problem (you need discipline first)
- **Budget constraints** → $900K+/year ongoing cost may not be justifiable

**Example failure story:** 150-person company, 2 FTE, abandoned after 12 months → switched to Port. Key lesson: team too small, timeline too optimistic.

## Comparison: Backstage vs Alternatives (2025)

Here's the honest comparison based on real implementations:

| Criterion | Backstage | Port.io | Cortex | Custom Portal |
|-----------|-----------|---------|--------|---------------|
| **Time to Value** | 12-18 months | 1-3 months | 2-4 months | 3-6 months |
| **Engineering Investment** | 7-15 FTEs | 0.5-1 FTE | 1-2 FTEs | 2-5 FTEs |
| **Annual Cost** | $1.05M-$2.25M | $50K-$200K | $40K-$150K | $300K-$750K |
| **Customization** | Unlimited (React/TS) | Limited (UI builder) | Moderate (API-driven) | Unlimited (your stack) |
| **Skills Required** | React/TypeScript/Node | None (no-code) | Basic API skills | Varies by stack |
| **Data Model** | Fixed entities, extensible | Fully flexible ("bring your own") | Semi-rigid (some fixed) | Fully flexible |
| **K8s Integration** | Plugin-based | Native with live data | Service-level only | Build your own |
| **Catalog Updates** | Custom integrations | Real-time for most sources | Hourly/weekly for some | Real-time (your choice) |
| **Best For** | 500+ eng, high customization | <500 eng, fast time-to-value | 200-1000 eng, service focus | Unique needs, existing tools |
| **Adoption Rate** | 10% average (problem!) | 40-60% typical | 30-50% typical | Varies (30-70%) |
| **Breaking Changes** | Major version every 6-12mo | Rare (managed service) | Rare (managed service) | Your control |

### Key Differentiators

**Port.io:**
- 4x faster implementation vs Backstage
- "Bring your own data model" approach
- Strong self-service actions (GitHub Actions, GitLab, Jenkins)
- No opinions about structure (empty canvas)

**Cortex:**
- Founded by engineers frustrated with service ownership spreadsheets
- Semi-rigid data model (some entities can't be changed)
- Service catalog focus with microservice data tracking
- Simpler than Backstage but less flexible than Port

**Custom Portal:**
- Leverage existing internal tools and API gateway
- Full control over stack and timeline
- No vendor lock-in or external dependencies
- Requires building everything from scratch

## Two Implementation Paths (If You Choose Backstage)

### Path A: Simplify Backstage (Recommended)

If you're committed to Backstage, **radically simplify** your approach:

1. **Start with Software Catalog ONLY**
   - No TechDocs initially
   - No Scaffolder initially
   - No fancy plugins
   - **Just the catalog**

2. **Use Managed Backstage** (Roadie)
   - Reduces ops burden significantly
   - Handles upgrades and security patches
   - Costs ~$50K-$150K/year but saves 2-4 FTE

3. **Limit to 5 Critical Plugins Maximum**
   - GitHub integration
   - Kubernetes visibility
   - PagerDuty on-call
   - Datadog monitoring
   - That's it.

4. **Dedicate 4-7 FTE Minimum**
   - 2-3 FTE: plugin development and customization
   - 2 FTE: platform operations and support
   - 1-2 FTE: data quality and catalog curation

5. **Accept 12-18 Month Timeline to 30% Adoption**
   - Month 1-3: Basic setup and first integrations
   - Month 4-6: Pilot with 2-3 teams
   - Month 7-12: Expand to 10-15% of org
   - Month 13-18: Push to 30% with incentives and evangelism

**Success metrics:**
- 30% adoption = success (not 10%)
- Under 5 sec page load time
- 99.9% uptime
- Under 2% stale catalog data

### Path B: Choose Purpose-Built Alternative

Sometimes the best decision is **not** to use Backstage:

**When Port.io Makes More Sense:**
- Under 500 engineers
- No React/TypeScript expertise
- Need time-to-value under 3 months
- Want no-code customization
- Budget-conscious ($50K-$200K vs $900K+)

**When Cortex Makes More Sense:**
- 200-1000 engineers
- Service catalog primary focus
- Want less flexibility than Port
- Need maturity tracking and scorecards
- Comfortable with semi-rigid data model

**When Custom Portal Makes More Sense:**
- Already have internal tools framework
- Unique requirements Backstage can't meet
- Want full control over stack and dependencies
- Have 2-5 FTE to dedicate
- Integration with proprietary systems

## Implementation Patterns That Actually Work

### Success Pattern: Large Enterprise (500+ Engineers)

**Setup:**
- 5 dedicated FTE platform team
- 18-month timeline from start to 50% adoption
- Managed Backstage (Roadie) to reduce ops burden
- Focus on 5 core plugins
- Executive sponsorship from VP Engineering

**Results:**
- 50% adoption achieved
- 3.2 sec average page load
- 99.95% uptime
- Under 1% stale catalog data
- Positive ROI after 24 months

**Key lesson:** Dedicated team and simplified scope beat "let's implement everything."

### Failure Pattern: Mid-Size Company (150 Engineers)

**Setup:**
- 2 FTE platform team
- 12-month timeline target
- Self-hosted Backstage
- Attempted 20+ plugin integrations
- No executive sponsorship

**Results:**
- 8% adoption after 12 months
- 12+ sec page load time
- 95% uptime (frequent issues)
- 15% stale catalog data
- Abandoned for Port.io

**Key lesson:** Team too small, scope too large, no exec buy-in = failure.

### Hybrid Pattern: Large Enterprise (1000+ Engineers)

**Setup:**
- Backstage for service catalog and API docs
- Cortex for service maturity and scorecards
- Port for self-service actions
- 8 FTE across all platforms

**Results:**
- 65% overall adoption (combined)
- Each tool serves specific use case
- Higher total cost but better user experience
- Positive ROI through specialization

**Key lesson:** Sometimes multiple specialized tools beat one generalist platform.

## Resource Calculator: What You Actually Need

Use this calculator to estimate your Backstage investment:

### Input Variables:
- **Company size:** Number of engineers
- **Frontend capability:** Strong/Moderate/Weak React+TypeScript skills
- **Timeline target:** Months to meaningful adoption
- **Customization needs:** High/Medium/Low

### Output Estimates:

**For 300 Engineers, Moderate Skills, 12-Month Timeline, Medium Customization:**

**Backstage:**
- Team size: 7-10 FTEs
- Year 1 cost: $1.05M-$1.5M
- Ongoing cost: $900K-$1.2M/year
- Time to 30% adoption: 18-24 months
- **Verdict:** Expensive, slow—consider alternatives

**Port.io:**
- Team size: 0.5-1 FTE
- Year 1 cost: $125K-$200K
- Ongoing cost: $75K-$150K/year
- Time to 30% adoption: 6-9 months
- **Verdict:** Fast, affordable—better fit

**Custom Portal:**
- Team size: 2-4 FTEs
- Year 1 cost: $300K-$600K
- Ongoing cost: $300K-$600K/year
- Time to 30% adoption: 12-18 months
- **Verdict:** Control + cost balance

## The Honest Questions You Must Ask

Before committing to Backstage, answer these questions honestly:

### Organizational Readiness

1. **Do we have 7-15 FTE available for 18-24 months?**
   - If no → Choose alternative

2. **Does our engineering team have strong React/TypeScript skills?**
   - If no → Massive friction ahead

3. **Does our service catalog already exist with ownership discipline?**
   - If no → You're building two things at once (hard)

4. **Do we have executive sponsorship and multi-year commitment?**
   - If no → Adoption will fail

5. **Can we accept 18-24 month timeline to 30% adoption?**
   - If no → Choose faster alternative

### Technical Capability

6. **Can we maintain breaking changes every 6-12 months?**
   - If no → Consider managed Backstage or alternatives

7. **Do we have infrastructure for self-hosting (K8s, monitoring, auth)?**
   - If no → Adds months to timeline

8. **Can we build custom plugins if needed?**
   - If no → Limited to existing plugins (may not meet needs)

### Strategic Alignment

9. **Is our goal a service catalog, or a full developer portal?**
   - Service catalog → Cortex may be better
   - Full portal → Backstage or Port

10. **Do we need this to succeed in <6 months?**
    - If yes → Backstage is wrong choice

## What to Do Instead

### If You're Just Starting

**Don't start with Backstage.** Start with:

1. **Document developer pain points** (surveys, interviews)
2. **Build thinnest viable solution** (spreadsheet, wiki, simple UI)
3. **Get to 30% adoption** with simple tool
4. **Then evaluate** if Backstage adds value

**Key principle:** Adoption first, sophistication second.

### If You're Stuck at 10% Adoption

**Pivot strategy:**

1. **Audit what's working** (which teams use it? why?)
2. **Simplify radically** (cut plugins to 5 max)
3. **Fix data quality** (make catalog trustworthy)
4. **Add exec-level metrics** (get leadership buy-in)
5. **Set 6-month deadline** for 30% adoption
6. **If you miss deadline** → Switch to alternative

**Don't fall for sunk cost fallacy.** 9 months invested doesn't mean you should invest 9 more.

### If You're Evaluating Alternatives

**Run parallel POCs:**

1. **Week 1-2:** Deploy Port.io with 1 team
2. **Week 3-4:** Deploy Cortex with 1 team
3. **Week 5-6:** Build custom MVP with 1 team
4. **Week 7-8:** Evaluate adoption, developer feedback, cost

**Winner:** Whatever gets you to 30% adoption fastest.

## Resources and Next Steps

### Recommended Reading

- [Platform Engineering ROI Calculator](/blog/platform-engineering-roi-calculator) - Calculate if Backstage investment makes sense
- [Why Platform Engineering Teams Fail](/blog/why-platform-engineering-teams-fail) - Learn the 5 metrics that predict success
- [Platform Economics](/blog/platform-engineering-economics-hidden-costs-roi) - Understand the $261B tool sprawl problem
- [Backstage Official Docs](https://backstage.io/docs/overview/adopting/) - Adoption strategies from Spotify
- [The Hidden Costs of 'Free' IDPs](https://thenewstack.io/the-hidden-costs-of-free-internal-developer-portals/) - New Stack analysis

### Tools to Evaluate

- **Backstage:** [backstage.io](https://backstage.io)
- **Roadie (Managed Backstage):** [roadie.io](https://roadie.io)
- **Port.io:** [port.io](https://www.port.io)
- **Cortex:** [cortex.io](https://www.cortex.io)
- **OpsLevel:** [opslevel.com](https://www.opslevel.com)

### Community Resources

- **Platform Engineering Slack:** [platformengineering.org/slack](https://platformengineering.org/slack-community)
- **Backstage Discord:** [discord.gg/backstage](https://discord.gg/backstage)
- **HackerNews Discussions:** Search "Backstage adoption" for real stories

## The Bottom Line

Backstage is not a product—it's a **framework that requires product development**. It requires 7-15 FTEs, 18-24 months, and $1M+ investment to get to 30% adoption (not the 10% average).

### Choose Backstage If:
- ✅ 500+ engineers
- ✅ 7-15 FTE available
- ✅ Strong React/TypeScript skills
- ✅ 3-5 year commitment
- ✅ High customization needs

### Choose Alternatives If:
- ❌ Under 500 engineers
- ❌ Under 7 FTE available
- ❌ Limited frontend skills
- ❌ Need ROI under 12 months
- ❌ Want faster time-to-value

**The decision isn't "Backstage vs nothing."** It's "What's the fastest path to meaningful developer portal adoption?"

Sometimes that's Backstage. Often it's not.

---

**What's your experience with Backstage?** Share your adoption stories (success or failure) in the [Platform Engineering community](https://platformengineering.org/slack-community). Let's learn from each other's real-world implementations—not vendor marketing.

**Need help deciding?** Use our [Platform Engineering ROI Calculator](/blog/platform-engineering-roi-calculator) to model your costs and timeline for different options.
