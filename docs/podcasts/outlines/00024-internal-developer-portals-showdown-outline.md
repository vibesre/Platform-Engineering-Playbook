# Episode Outline: Internal Developer Portal Showdown 2025

**Episode Number**: #024
**Working Title**: Internal Developer Portal Showdown 2025: Backstage vs Port vs Cortex vs OpsLevel
**Duration Target**: 12-15 minutes
**Speakers**: Jordan (analytical, data-focused) and Alex (practical, implementation-focused)

## Story Planning

**NARRATIVE STRUCTURE**: Economic Detective

**CENTRAL TENSION**: Teams think "open-source Backstage = free" but face $150K per 20 developers in hidden costs. Commercial platforms cost $39-$78/user/month but deliver value in 30-45 days. Which is actually cheaper? When does each make sense?

**THROUGHLINE**: From believing Backstage's "free" licensing saves money, to discovering hidden engineering costs ($150K per 20 devs, 2-5 FTE maintenance), to evaluating commercial alternatives (OpsLevel $39, Cortex $65-69, Port $78), to making the right choice based on team size, technical capability, and timeline.

**EMOTIONAL ARC**:
- **Recognition** (0-2 min): "I've seen this" - The 8% adoption scenario hits home
- **Surprise** (5-8 min): "Wait, THAT's why?" - Backstage costs 16x more than commercial for most teams
- **Empowerment** (11-15 min): "Now I know what to do" - Clear decision framework by team size and needs

## Act Structure

### ACT 1: SETUP - The Pricing Paradox (0-3 min, ~450 words)

**Hook**: Team spent 6 months implementing Backstage. Portal looks beautiful. 47 services cataloged. Adoption? 8%. Three developers use it. CFO asks: "Why didn't we just buy a solution that works?" (Relatable pain point)

**Stakes**: Companies losing $1M annually to tool sprawl (7.4 tools per dev, 6-15 hours/week lost). Internal developer portals promise 60% efficiency gains, 20-55% productivity improvements. But only if teams can successfully implement them. Most Backstage attempts fail with <10% adoption.

**Promise**: Today we're comparing what's actually available in 2025—the real costs, real timelines, real trade-offs. By the end, you'll know exactly which platform fits your team size, technical capability, and timeline.

**Callback Setup**: Reference Episode #013 ("In episode 13 we covered WHY Backstage adoption fails. Today we're talking about what to use INSTEAD.")

**Key Points**:
- Backstage adoption stalls at <10% outside Spotify (Cortex, Gartner 2025)
- Hidden cost: $150K per 20 developers in engineering time (internaldeveloperplatform.org)
- 2-5 FTE minimum for ongoing maintenance (Gartner 2025)
- Commercial platforms: OpsLevel $39/user/month, Cortex $65-69, Port $78
- Implementation: 30-45 days (commercial) vs 6-12 months (Backstage)

**Dialogue Direction**: Jordan starts skeptical ("Surely open-source must be cheaper?"), Alex has the counter-data ready. Natural disagreement that reveals the paradox.

### ACT 2: EXPLORATION - Platform by Platform (3-10 min, ~1,050 words)

**Discovery 1: OpsLevel - The Speed Champion (2 min, ~300 words)**

**What**: Fastest implementation (30-45 days), lowest cost ($39/user/month)

**Why Surprising**: Teams under 200 engineers save 16x compared to Backstage ($93,600 annual vs $1.5M hidden costs)

**Trade-offs**: Less customization, opinionated design, synchronous actions only

**Best For**: Teams needing value fast, budget-conscious, standard workflows

**Key Data**:
- 30-45 days to full deployment
- $39/user/month ($93,600 annually for 200 engineers)
- 60% efficiency gains post-adoption (OpsLevel customers)
- Automated catalog maintenance (solves stale data problem)

**Discovery 2: Port - The Flexibility Champion (2 min, ~300 words)**

**What**: No-code/low-code with customizable data model ("Blueprints")

**Why Interesting**: Maximum customization without Backstage's React/TypeScript coding requirement

**Trade-offs**: Premium pricing ($78/user/month, 2x OpsLevel), 3-6 month implementation, blueprint design effort

**Best For**: Teams needing flexible data model, want customization without coding overhead, have budget

**Key Data**:
- $78/user/month (~$187,200 annually for 200 engineers)
- 3-6 months average implementation
- Real-time data updates (no stale catalog)
- Both sync and async self-service actions

**Discovery 3: Cortex - The Standards Champion (2 min, ~300 words)**

**What**: Engineering excellence and standards enforcement focus

**Why Matters**: Leadership visibility into service maturity, SLOs, security compliance

**Trade-offs**: Semi-rigid data model, 6+ month implementation, higher pricing ($65-69/user/month), Kubernetes-centric

**Best For**: Priority on standards over flexibility, need engineering excellence dashboards for leadership

**Key Data**:
- $65-69/user/month ($156,000-$165,600 annually for 200 engineers)
- 6+ months for large orgs
- Scorecard evaluation every 4 hours
- Focus on reliability and operational maturity

**Discovery 4: Managed Backstage - The Compromise (1.5 min, ~225 words)**

**What**: Hosted Backstage-as-a-service (Roadie, Spotify Portal)

**Critical Limitation**: "You'll encounter many of the same problems as open-source Backstage, such as the rigid data model" (Port analysis)

**Reality Check**: Removes operational burden (hosting, updates) but NOT adoption problems (rigid catalog, stale data, <10% adoption)

**Key Data**:
- ~$22/user/month (Roadie)
- Still 3-6 months implementation
- Still requires React/TypeScript for custom plugins
- Adoption challenges remain unchanged

**Complication - The Real Cost Equation (1 min, ~150 words)**

**Reframe**: It's not "open-source free vs commercial expensive." It's "hidden engineering time vs transparent licensing."

**Math**: 200 engineers:
- Backstage: $0 licensing + $1.5M engineering time = $1.5M total
- OpsLevel: $93,600 licensing + minimal maintenance = $93,600 total
- Port: $187,200 licensing + minimal maintenance = $187,200 total
- Result: Commercial is 8-16x cheaper for teams under 500 engineers

**When Equation Flips**: 1000+ engineers with dedicated 5-person platform team = Backstage becomes cost-competitive through amortization

### ACT 3: RESOLUTION - The Decision Framework (10-15 min, ~750 words)

**Synthesis: It's All About Team Size and Technical Capability (3 min, ~450 words)**

**Decision Dimension 1: Team Size**

**Under 200 Engineers**:
- Commercial strongly recommended (OpsLevel for speed/cost)
- Backstage overhead = 1-2.5% of engineering capacity (too high)
- Math: $1.5M Backstage vs $93,600 OpsLevel = 16x cost difference
- Winner: OpsLevel

**200-500 Engineers**:
- Commercial likely better unless unique needs
- Decision factors: Have frontend team? → Consider Backstage. Need value in 3-6 months? → Commercial
- Winner: Port (flexibility) or OpsLevel (speed)

**500+ Engineers**:
- Backstage viable if requirements met (3-5 FTE platform team, frontend expertise, 12-18 month timeline)
- Proven at Toyota (thousands of engineers, $10M savings)
- Winner: Backstage (if all requirements met) or Cortex (standards at scale)

**1000+ Engineers**:
- Backstage economics improve with scale (platform team amortized)
- Winner: Backstage

**Decision Dimension 2: Technical Capability**

- **Frontend team exists (React + TypeScript)**: Backstage viable
- **Backend-only team**: Avoid Backstage, choose Port or OpsLevel
- **Platform team size**: <2 FTE → commercial only; 2-5 FTE → commercial recommended; 5+ FTE → Backstage viable

**Decision Dimension 3: Timeline**

- **Need value in 4-8 weeks**: Only OpsLevel (30-45 days)
- **Can wait 3-6 months**: Port or managed Backstage
- **12-18 months acceptable**: Backstage (if other requirements met)

**Application: Practical Guidance for Three Common Scenarios (2 min, ~300 words)**

**Scenario 1: 150-person startup, backend-focused team, need portal in Q1**
- Answer: OpsLevel
- Why: 30-45 days deployment, $39/user/month = $70,200 annually, no frontend skills required
- Implementation: 30-day pilot with 20-30 engineers, automate catalog from GitHub, 2-3 self-service actions, roll out if >40% adoption

**Scenario 2: 400-person company, have 2 frontend engineers, unique workflow needs**
- Answer: Port or pilot Backstage
- Why: Port offers no-code customization without Backstage's FTE overhead. If truly unique workflows justify custom plugins, pilot Backstage with 1-2 teams first
- Timeline: 3-6 months Port, 6-12 months Backstage

**Scenario 3: 1200-person enterprise, dedicated 5-person platform team, engineering excellence focus**
- Answer: Backstage or Cortex
- Why: Scale justifies platform team investment, frontend expertise available, unique needs at this scale
- Implementation: 12-18 months Backstage with phased rollout, or Cortex for faster deployment with standards focus

**Empowerment: What to Do Monday Morning (1 min, ~150 words)**

**If You're Evaluating**:
1. Calculate team size → Under 200? → OpsLevel. 200-500? → Evaluate Port vs OpsLevel. 500+? → Pilot Backstage
2. Assess technical capability → No frontend team? → Avoid Backstage
3. Define timeline → Need value in 6-8 weeks? → Only OpsLevel works

**If You're Stuck with Low-Adoption Backstage**:
1. Honest assessment: <15% adoption after 6+ months? → Time to migrate
2. Calculate TCO: 2+ FTE on maintenance = $300K+ annually → Compare to $93K-$187K commercial
3. Run parallel: 30-day pilot with OpsLevel or Port, migrate if adoption exceeds Backstage

**Callback to Episode #013**: "In episode 13 we talked about why Backstage fails. Today we've covered what actually works for different team sizes. The key insight? Open-source free doesn't mean cheap when hidden engineering costs hit $150K per 20 developers."

## Story Elements

**KEY CALLBACKS**:
- Reference Episode #013 in intro ("why" vs "what instead")
- Return to 8% adoption scenario throughout ("This is why that CFO question hurts")
- Pricing paradox revealed in Act 1, resolved in Act 3 ("It's not licensing cost, it's engineering time")

**NARRATIVE TECHNIQUES**:
- **Economic Detective**: Apparent cost ($0 Backstage) → Hidden costs ($150K per 20 devs) → Real calculation (16x cheaper commercial) → Decision framework
- **Anchoring Statistic**: <10% Backstage adoption - return to this throughout as "the metric that matters"
- **Thought Experiment**: Walk through 3 common scenarios with concrete team sizes and recommendations

**SUPPORTING DATA (with sources)**:
- Backstage adoption <10% (Cortex, Gartner 2025)
- Hidden cost $150K per 20 devs (internaldeveloperplatform.org)
- 2-5 FTE maintenance (Gartner 2025)
- OpsLevel $39/user/month, 30-45 days (OpsLevel)
- Port $78/user/month, 3-6 months (OpsLevel comparison)
- Cortex $65-69/user/month, 6+ months (OpsLevel comparison)
- 7.4 tools per dev team (Port State of IDPs 2025)
- 60% efficiency gains (OpsLevel customers)
- Toyota $10M savings (case study from blog)

## Quality Checklist

- [x] **Throughline clear**: "Free" Backstage → Hidden $150K costs → Commercial alternatives → Right choice by team size
- [x] **Hook compelling**: 8% adoption scenario + CFO question = recognition moment
- [x] **Sections build momentum**: Each platform reveal builds toward comprehensive comparison
- [x] **Insights connect**: All data points support central thesis (team size determines right platform)
- [x] **Emotional beats land**: Recognition (failed Backstage), Surprise (16x cost difference), Empowerment (clear decision framework)
- [x] **Callbacks create unity**: Episode #013 reference, 8% adoption returns, pricing paradox resolved
- [x] **Payoff satisfies**: Three concrete scenarios with actionable recommendations
- [x] **Narrative rhythm**: Story not list (Economic Detective structure maintains momentum)
- [x] **Technical depth maintained**: Specific pricing, timelines, team sizes, implementation strategies
- [x] **Listener value clear**: Know exactly which platform to choose based on team size and capabilities

## Dialogue Notes

**Jordan's Voice** (analytical, data-focused):
- Skeptical of "commercial must be expensive" assumption
- Brings data and calculations
- Challenges conventional wisdom
- "Wait, let's do the math here..."

**Alex's Voice** (practical, implementation-focused):
- Sees real-world adoption failures
- Focuses on timelines and maintenance burden
- Brings customer stories and case studies
- "Here's what actually happens at most teams..."

**Natural Tension**:
- Jordan wants maximum flexibility (drawn to Port/Backstage)
- Alex wants speed and certainty (drawn to OpsLevel)
- Resolution: It depends on team size and capability (both are right for different scenarios)

**Pacing**:
- Act 1: Quick setup (3 min) - hook and stakes
- Act 2: Measured exploration (7 min) - each platform gets fair treatment
- Act 3: Decisive resolution (4 min) - clear guidance, practical scenarios

## Cross-Reference Notes

**Companion Blog Post**: `blog/2025-11-14-internal-developer-portals-beyond-backstage.md`
- Comprehensive comparison tables
- Complete pricing breakdown by team size
- Migration strategies for teams stuck on Backstage
- Full decision framework with 5 dimensions

**Related Episode #013**: `00013-backstage-adoption.md`
- Covers WHY Backstage fails (<10% adoption problem)
- This episode (#024) covers WHAT to use instead
- Natural progression: Problem → Solution

**Related Blog Post**: `blog/2025-11-01-backstage-production-10-percent-adoption-problem.md`
- Deep dive on adoption challenges
- Cost analysis and root causes
- Decision framework for when Backstage makes sense

## Success Metrics for This Episode

**Listener Takeaway**: "I now know whether to choose OpsLevel (under 200 engineers), Port (200-500, need flexibility), or Backstage (500+, have platform team)"

**Actionable Outcome**: Calculate team size → Assess technical capability → Choose platform → Run 30-day pilot

**Differentiation from Episode #013**: Episode #013 = WHY problem exists. Episode #024 = WHAT to do instead.

**Differentiation from Generic Comparisons**: Specific pricing, specific timelines, specific team size thresholds, specific decision frameworks (not vague "it depends")
