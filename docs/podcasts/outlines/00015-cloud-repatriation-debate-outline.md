# Episode Outline: The Cloud Repatriation Debate - When AWS Costs 10-100x More Than It Should

## Story Planning

**NARRATIVE STRUCTURE**: Economic Detective Story

**CENTRAL TENSION**: Platform teams discovering their AWS bills are 10-100x higher than alternatives, but leadership fears leaving the cloud. Who's right?

**THROUGHLINE**: From accepting cloud costs as "the price of doing business" to understanding the real economics and making informed infrastructure decisions.

**EMOTIONAL ARC**:
- Recognition moment: "Our AWS bill is how much?! And we're still managing servers anyway..."
- Surprise moment: "Wait, 37signals is saving $2 million per year? And Dropbox saved $75 million?"
- Empowerment moment: "Now I have a framework to evaluate our actual needs vs. what we're paying for."

## Act Structure

### ACT 1: SETUP (2-3 minutes)
- **Hook**: "An engineer sent me an article claiming AWS charges 10 to 100 times more than it should. My first reaction was 'that's ridiculous hyperbole.' Then I pulled up our actual AWS bills next to Hetzner's pricing page..."
- **Stakes**: Platform teams are burning millions on cloud costs while companies are doing layoffs to "improve efficiency"
- **Promise**: We'll uncover the real cost math and build a framework for when cloud makes sense vs. when it's highway robbery

**Key Points**:
- AWS C5 instance with 80 vCPUs: $2,500-3,500/month
- Hetzner bare metal 80 cores: $190/month (that's 18x difference!)
- 86% of CIOs planning some form of cloud repatriation in 2025

### ACT 2: EXPLORATION (5-7 minutes)
- **Discovery 1**: The 37signals exodus - saving $2M/year, still have 8 people on ops team
- **Discovery 2**: The hidden cloud costs nobody talks about - egress fees ($0.09/GB), NAT gateways ($45/month), data transfer between AZs
- **Discovery 3**: The "you're using cloud wrong" gaslighting - even optimized setups cost 5-10x more
- **Complication**: But wait - what about elastic scaling? Global presence? Managed services?

**Key Points**:
- Dropbox saved $74.6 million over 2 years by moving 90% off AWS
- GEICO cut 70% of costs moving from cloud to on-premises
- But Netflix still thrives on AWS - spending $1B+ annually
- The real differentiator: predictable vs. burst workloads

### ACT 3: RESOLUTION (3-4 minutes)
- **Synthesis**: It's not cloud vs. on-prem - it's about matching architecture to economics
- **Application**: Decision framework based on workload predictability, team size, and growth stage
- **Empowerment**: How to run the numbers for YOUR organization (TCO calculation template)

**Key Points**:
- Startups: Stay on cloud until you hit $10K/month bills
- Growth companies: Hybrid approach - predictable workloads on metal, burst on cloud
- Enterprises: Consider repatriation if you have stable, predictable workloads

## Story Elements

**KEY CALLBACKS**:
- Return to the "10-100x" claim from the opening - validate it with real examples
- The AWS bill comparison from Act 1 becomes the framework template in Act 3
- "The price of doing business" transforms into "the price of not doing math"

**NARRATIVE TECHNIQUES**:
- The Anchoring Statistic: "18x markup" becomes recurring reference point
- Case Study Arc: Follow 37signals' journey from all-in on cloud to saving millions
- Devil's Advocate Dance: Jordan defends cloud benefits while Alex exposes hidden costs

**SUPPORTING DATA**:
- 37signals: $2M annual savings, $10M+ over 5 years
- Dropbox: $74.6M saved over 2 years
- GEICO: 70% cost reduction
- AWS egress: $0.09/GB (that's $90 per TB!)
- Hetzner pricing: 80-core server for $190/month
- DigitalOcean: 8 vCPU droplet for $48/month

## Quality Checklist

Before approving this outline:
- [x] Throughline is clear (from accepting high costs to understanding real economics)
- [x] Hook is compelling (personal discovery of shocking price differences)
- [x] Each section builds (setup problem → explore evidence → provide framework)
- [x] Insights connect (each discovery adds to the cost picture)
- [x] Emotional beats land (recognition of problem, surprise at scale, empowerment with framework)
- [x] Callbacks create unity (10-100x claim validated, bill comparison becomes template)
- [x] Payoff satisfies (concrete decision framework delivered)
- [x] Narrative rhythm (detective story structure maintains momentum)
- [x] Technical depth maintained (real numbers, specific services, actual case studies)
- [x] Listener value clear (they can calculate their own TCO and make informed decisions)

## Episode Details

**Episode Number**: 00015
**Duration Target**: 12-15 minutes
**Tone**: Investigative but balanced - not anti-cloud zealotry, but honest about economics
**Key Tension Between Speakers**:
- Jordan: Advocates for cloud benefits (innovation speed, managed services)
- Alex: Exposes hidden costs and questions the value proposition