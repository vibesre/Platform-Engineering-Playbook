# Episode Outline: Cloud Cost Quick Wins for Year-End

## Story Planning
**NARRATIVE STRUCTURE**: Economic Detective + Before/After
**CENTRAL TENSION**: Companies waste 20-30% of cloud spend on unused resources, and year-end is the perfect time to reclaim that budget before it resets
**THROUGHLINE**: From accepting cloud waste as inevitable to discovering actionable wins you can implement this week before budget resets
**EMOTIONAL ARC**:
- Recognition: "Our cloud bill feels out of control too"
- Surprise: "Wait, 70% savings just from scheduling?"
- Empowerment: "I can pitch these to leadership before year-end"

## Episode Metadata
**Episode Number**: 046
**Slug**: cloud-cost-quick-wins-year-end
**Duration Target**: 12-14 minutes
**News**: Pre-collected for Dec 4, 2025 (ready to insert)

## Act Structure

### ACT 1: SETUP (2-3 min)
- **Hook**: "Global cloud spend hits $720 billion in 2025 - up from $600 billion last year. But here's the kicker: organizations waste 20-30% of that on resources nobody's using. That's potentially $200 billion just... evaporating."
- **Stakes**: Year-end budget season. Unspent budget gets clawed back. Demonstrated savings = next year's platform investment. CFO asking "why is cloud so expensive?"
- **Promise**: Six quick wins you can implement THIS WEEK to show immediate savings before the fiscal year closes

**Key Points**:
- $720B global cloud spend 2025 (up 20% from $600B in 2024)
- 20-30% waste rate across organizations
- Only 3 in 10 orgs have clear visibility into cloud spend
- Compute typically 50-70% of total cloud bill

### ACT 2: EXPLORATION - The Six Quick Wins (6-8 min)

#### Discovery 1: The Scheduling Win (70% savings potential)
- Non-production environments running 24/7 when used 8-10 hours/day
- Automated scheduling for dev/staging = 70% cost reduction
- Tools: AWS Instance Scheduler, Azure Automation, native GCP scheduling
- **Real example**: Dev cluster costs $3,000/month → $900/month with scheduling

#### Discovery 2: Right-Sizing Reality Check
- 40% of cloud instances are oversized for their workload
- Most apps use <30% of provisioned CPU/memory
- Quick win: Review top 10 costliest instances, downsize by one tier
- Savings: 25-40% per right-sized instance

#### Discovery 3: The Commitment Play (Reserved Instances/Savings Plans)
- Up to 72% discount vs on-demand
- Quick analysis: What's been running steady for 6+ months?
- Year-end timing: Lock in 1-year commitments now for immediate 2026 savings
- Caveat: Don't over-commit - 70% coverage is usually optimal

#### Discovery 4: Spot/Preemptible for Fault-Tolerant Workloads
- 60-90% savings for interruptible workloads
- Perfect candidates: CI/CD runners, batch processing, dev environments
- Quick win: Move one CI/CD pipeline to spot instances
- **Real math**: $500/month → $75/month for build infrastructure

#### Discovery 5: Storage Tiering (Stop lighting money on fire)
- Most organizations keep everything in hot storage
- 60-70% of data accessed <once per month
- Quick action: Audit S3/Blob storage, move cold data to Glacier/Archive
- Tool recommendation: AWS S3 Analytics, Azure Storage Insights

#### Discovery 6: The Zombie Hunt (Orphaned Resources)
- Unattached EBS volumes, unused Elastic IPs, orphaned snapshots
- Load balancers pointing to nothing
- Quick scan: AWS Cost Explorer, Azure Advisor, GCP Recommender
- **Typical find**: $500-2,000/month in zombie resources per account

**Complication**: These wins require cross-team coordination. Platform teams need buy-in from dev teams who "might need that resource someday."

### ACT 3: RESOLUTION (3-4 min)
- **Synthesis**: The real framework is visibility → action → governance
  1. Can't optimize what you can't see (tagging, allocation)
  2. Quick wins build credibility for bigger initiatives
  3. Governance prevents regression

- **Application**: Year-end pitch to leadership
  - "We identified $X in immediate savings"
  - "Here's our 90-day optimization roadmap"
  - "Investment in FinOps tooling pays back 3-5x"

- **Empowerment**: Start Monday morning checklist
  1. Run cloud provider's cost analyzer (free)
  2. Identify top 5 zombie resources (1 hour)
  3. Schedule one non-prod environment (2 hours)
  4. Present findings to manager (30 min)

**Key Points**:
- FinOps market valued at $5.5B in 2025, 34.8% CAGR
- Organizations with dedicated FinOps see 20-30% better optimization
- Quick wins build political capital for platform investment

## Story Elements
**KEY CALLBACKS**:
- Return to $720B number at end: "Your slice of that $720B pie - you now know how to shrink it"
- "20-30% waste" becomes "20-30% opportunity"

**NARRATIVE TECHNIQUES**:
- Anchoring Statistic ($720B)
- Before/After micro-stories for each win
- Economic calculation (real dollar amounts)
- Devil's advocate on over-commitment risk

**SUPPORTING DATA**:
- $720B global cloud spend 2025 (industry projections)
- 20-30% waste rate (multiple FinOps reports)
- 70% scheduling savings (AWS case studies)
- 72% reserved instance discount (AWS/Azure/GCP pricing)
- 60-90% spot instance savings (cloud provider documentation)
- $5.5B FinOps market (FinOps Foundation)

## Quality Checklist
- [x] Throughline clear (one sentence)
- [x] Hook compelling ($720B, 20-30% waste)
- [x] Sections build momentum (easy → medium → strategic)
- [x] Insights connect (all lead to visibility→action→governance)
- [x] Emotional beats land (recognition, surprise at 70%, empowerment with Monday checklist)
- [x] Callbacks create unity ($720B returns)
- [x] Payoff satisfies (concrete actions, pitch framework)
- [x] Narrative rhythm (story not list - each win is mini before/after)
- [x] Technical depth appropriate (practical, actionable, not deep infrastructure)
- [x] Listener value clear (6 wins + leadership pitch + Monday checklist)

## Speaker Notes
- Jordan drives the "here's the problem" framing
- Alex provides the "here's how to fix it" solutions
- Keep energy up - this is a practical, action-oriented episode
- Year-end timing adds urgency - lean into it
- End on empowerment: "You've got this"
