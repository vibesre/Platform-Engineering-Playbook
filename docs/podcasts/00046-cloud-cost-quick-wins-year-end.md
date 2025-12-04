---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #046: Cloud Cost Quick Wins for Year-End"
slug: 00046-cloud-cost-quick-wins-year-end
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #046: Cloud Cost Quick Wins for Year-End

<GitHubButtons />

**Duration**: 12 minutes | **Speakers**: Jordan & Alex

**Target Audience**: Platform engineers, FinOps practitioners, and engineering leaders looking to demonstrate cloud savings before budget season ends

---

## Synopsis

Global cloud spend hits $720 billion in 2025, with organizations wasting 20-30% on unused resources. This episode delivers six actionable quick wins you can implement this week to show immediate savings before the fiscal year closes - from scheduling non-prod environments (70% savings) to hunting zombie resources ($500-2,000/month per account).

---

## Chapter Markers

- **00:00** - Introduction & News Segment
- **01:30** - The $720B Problem: Cloud Waste at Scale
- **02:45** - Quick Win #1: Scheduling (70% savings)
- **04:00** - Quick Win #2: Right-Sizing (25-40% per instance)
- **05:15** - Quick Win #3: Commitment Play (up to 72% discount)
- **06:30** - Quick Win #4: Spot Instances (60-90% savings)
- **07:45** - Quick Win #5: Storage Tiering
- **08:45** - Quick Win #6: Zombie Hunt
- **09:45** - Cross-Team Coordination
- **10:30** - Leadership Pitch Framework
- **11:15** - Monday Morning Checklist
- **12:00** - Closing

---

## News Segment (December 4, 2025)

- **Envoy v1.36.3 Security Patches**: Three CVEs including request smuggling and JWT auth crash - patch today
- **Loki Operator 0.9.0**: Automatic NetworkPolicy deployment and new critical alerts
- **AWS Graviton5 M9g Instances**: 25-35% performance improvements over Graviton4 (preview)
- **Uncloud**: New tool for deploying containers without Kubernetes complexity

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Global Cloud Spend (2025) | $720 billion | Industry projections |
| Waste Rate | 20-30% | FinOps Foundation |
| Scheduling Savings | 70% on non-prod | AWS case studies |
| Reserved Instance Discount | Up to 72% | Cloud provider pricing |
| Spot Instance Savings | 60-90% | Cloud provider docs |
| FinOps Market Value | $5.5 billion | FinOps Foundation |
| FinOps Market Growth | 34.8% CAGR | FinOps Foundation |

---

## The Six Quick Wins

### 1. Scheduling Non-Production (70% savings)
Dev/staging environments running 24/7 but used 8-10 hours/day. Automated shutdown overnight = 70% cost reduction.

### 2. Right-Sizing (25-40% per instance)
40% of instances are oversized. Review top 10 costliest, check 30-day utilization, downsize by one tier.

### 3. Commitment Play (up to 72% discount)
Reserved Instances/Savings Plans for steady workloads. 70% coverage is optimal. Lock in now for January savings.

### 4. Spot Instances (60-90% savings)
Perfect for CI/CD runners, batch processing, dev environments. Example: $500/month → $75/month.

### 5. Storage Tiering (dramatic savings)
60-70% of data accessed <once/month. Move to Glacier/Archive. Hot: $23/TB/month. Archive: <$1/TB/month.

### 6. Zombie Hunt ($500-2,000/month per account)
Orphaned EBS volumes, unused IPs, forgotten snapshots, empty load balancers. Use Cost Explorer/Advisor/Recommender.

---

## Monday Morning Checklist

1. **Run cost analyzer** - 30 minutes (free, built-in)
2. **Identify top 5 zombies** - 1 hour
3. **Schedule one non-prod env** - 2 hours
4. **Present to manager** - 30 minutes

---

## Transcript

**Jordan:** Today we're tackling something every platform team deals with at year-end: cloud costs. And we've got six quick wins you can implement this week. But first, let's check the pulse of platform engineering.

**Jordan:** Security alert for anyone running Envoy. Version one point thirty-six point three just dropped with patches for three CVEs, including a request smuggling vulnerability and a JWT auth crash that could take down your proxy. If you're running Envoy in production, and let's be honest, most service meshes are, patch today, not next sprint. There's also a backport to one point thirty-five point seven if you're not on the latest branch.

**Jordan:** In observability news, the Loki Operator hit zero point nine point zero with automatic NetworkPolicy deployment and new critical alerts for ingester flush failures. Worth checking if you're running Loki in production.

**Jordan:** For the cloud infrastructure crowd, AWS announced Graviton five based M nine G instances in preview. They're claiming twenty-five to thirty-five percent performance improvements over Graviton four. Significant for organizations already running ARM workloads at scale.

**Jordan:** And speaking of cost optimization, which is our main topic today, there's a new tool called Uncloud for deploying containers across servers without Kubernetes complexity. It's relevant for teams questioning K eight s overhead for simpler workloads. Sometimes the cheapest container orchestrator is no orchestrator at all.

**Jordan:** That's the news. And now, let's talk about cloud cost quick wins for year-end.

**Jordan:** Global cloud spend is projected to hit seven hundred twenty billion dollars in twenty twenty-five. That's up from about six hundred billion last year, a twenty percent jump in a single year.

**Alex:** And here's the kicker that should make every CFO nervous: organizations waste twenty to thirty percent of that on resources nobody's using. Do the math, and that's potentially two hundred billion dollars just evaporating into unused compute and forgotten storage.

**Jordan:** But year-end is actually the perfect time to tackle this. Budgets are being reviewed. Finance is asking why cloud costs keep climbing. And any savings you demonstrate now become ammunition for next year's platform investment.

**Alex:** Plus, unspent budget often gets clawed back. Show savings, and you prove your team knows how to optimize. That builds trust for future asks.

**Jordan:** So let's get practical. We've identified six quick wins that most teams can implement this week. Not next quarter, not after a big FinOps initiative. This week.

**Alex:** And we're ordering these from easiest to implement to most impactful. Start at the top, work your way down.

**Jordan:** Quick win number one: the scheduling win. This alone can save seventy percent on non-production environments.

**Alex:** Here's the reality. Most dev and staging environments run twenty-four seven, but developers actually use them eight to ten hours a day, five days a week. That means you're paying for fourteen to sixteen hours of idle time every day, plus weekends.

**Jordan:** The fix is dead simple. Automated scheduling. AWS has Instance Scheduler, Azure has Automation runbooks, GCP has native scheduling. Set your dev cluster to shut down at seven PM and spin up at seven AM.

**Alex:** Real example: A dev cluster costing three thousand dollars a month drops to nine hundred with scheduling. That's twenty-five thousand a year saved on one environment.

**Jordan:** The pushback you'll get is "but what if someone needs it at night?"

**Alex:** And the answer is: build in an override. A Slack command or a simple web form that extends the schedule for four hours. In practice, it gets used maybe twice a month.

**Jordan:** Quick win number two: the right-sizing reality check. This is where you find money hiding in plain sight.

**Alex:** Studies consistently show forty percent of cloud instances are oversized for their workload. Most applications use less than thirty percent of provisioned CPU and memory.

**Jordan:** The quick win here is simple. Pull up your cloud cost dashboard. Look at your top ten costliest instances. Check their utilization over the past thirty days.

**Alex:** If you see consistent utilization below thirty percent, that instance is a candidate for downsizing by one tier. An m five dot x large running at twenty percent utilization? Drop it to m five dot large.

**Jordan:** Savings are typically twenty-five to forty percent per right-sized instance. And modern clouds make this nearly zero-risk. You can resize in minutes if something breaks.

**Alex:** The key is having monitoring in place. You need to know utilization before you make the call. If you're not measuring, you're guessing.

**Jordan:** Quick win number three: the commitment play. This is where the big percentage savings live.

**Alex:** Reserved Instances and Savings Plans offer up to seventy-two percent discount versus on-demand pricing. That's not a typo. Seventy-two percent.

**Jordan:** The trade-off is commitment. You're promising to pay for a certain amount of compute for one or three years. Get it wrong, and you're paying for resources you don't use.

**Alex:** So the quick analysis is: what's been running steady for six months or more? Those workloads are prime candidates. Your production database, your core API servers, your monitoring stack.

**Jordan:** Year-end timing matters here. Lock in one-year commitments now, and you start seeing savings in January. That's a great way to start the fiscal year.

**Alex:** But don't over-commit. The rule of thumb is seventy percent coverage is usually optimal. Leave thirty percent on-demand for flexibility and growth.

**Jordan:** Quick win number four: Spot and Preemptible instances for fault-tolerant workloads. This is the sixty to ninety percent savings tier.

**Alex:** Spot instances are unused capacity that cloud providers sell at massive discounts. The catch is they can be reclaimed with little notice.

**Jordan:** Which sounds scary until you identify the right workloads. CI/CD runners are perfect. Batch processing jobs. Dev environments. Anything that can handle interruption and restart.

**Alex:** Real math here: A team running their build infrastructure on on-demand instances for five hundred dollars a month switched to spot. New cost: seventy-five dollars a month. Same builds, same speed, eighty-five percent savings.

**Jordan:** The implementation is straightforward too. Most CI/CD platforms have native spot support now. GitHub Actions, GitLab CI, Jenkins with the right plugins. It's often just a configuration flag.

**Jordan:** Quick win number five: storage tiering. This is where we stop lighting money on fire.

**Alex:** Most organizations keep everything in hot storage. Every log file, every backup, every artifact. But sixty to seventy percent of data is accessed less than once per month.

**Jordan:** That data should be in cold storage. S3 Glacier, Azure Archive, GCP Coldline. The cost difference is dramatic. Hot storage might be twenty-three dollars per terabyte per month. Glacier Deep Archive is under a dollar.

**Alex:** The quick action is to audit your S3 buckets or Blob containers. AWS has S3 Storage Analytics built in. It shows you access patterns. Move anything untouched for ninety days to a cheaper tier.

**Jordan:** And set up lifecycle policies so it happens automatically going forward. Data older than thirty days moves to Infrequent Access. Older than ninety days moves to Glacier. Set it and forget it.

**Jordan:** Quick win number six: the zombie hunt. This is weirdly satisfying.

**Alex:** Zombie resources are the orphaned infrastructure that nobody remembers creating. Unattached EBS volumes from terminated instances. Elastic IPs that aren't associated with anything. Snapshots from servers that no longer exist. Load balancers pointing to empty target groups.

**Jordan:** Every cloud provider has tools for this now. AWS Cost Explorer, Azure Advisor, GCP Recommender. They'll flag unused resources directly.

**Alex:** Typical find: five hundred to two thousand dollars per month in zombie resources per AWS account. And large organizations often have dozens of accounts.

**Jordan:** The satisfaction of deleting a year-old EBS volume that's been charging you fifteen dollars a month for nothing? Chef's kiss.

**Alex:** Just verify before you delete. Check with the team. Check the tags. Make sure it's actually abandoned, not just dormant.

**Jordan:** Now, here's the complication. All of these wins require some cross-team coordination. Developers get attached to their resources. They'll say "I might need that someday."

**Alex:** Which is why framing matters. You're not taking away resources. You're optimizing spend so the team has budget for the things they actually need.

**Jordan:** And each win you implement builds credibility. Demonstrate savings on dev environments, and suddenly leadership trusts you to look at production optimization.

**Jordan:** Let's talk about how to present this to leadership. Because finding savings is only half the battle.

**Alex:** The pitch structure is: we identified X dollars in immediate savings, here's our ninety-day optimization roadmap, and investment in FinOps tooling pays back three to five X.

**Jordan:** The FinOps market is valued at five point five billion dollars in twenty twenty-five with thirty-five percent year-over-year growth. That's not hype. That's organizations recognizing that cloud cost management is a real discipline.

**Alex:** Teams with dedicated FinOps practices see twenty to thirty percent better optimization outcomes. It's not just about tools. It's about having someone whose job is to watch the spend.

**Jordan:** So here's your Monday morning checklist. Four items, maybe three hours total.

**Alex:** First, run your cloud provider's cost analyzer. It's free, it's built in, and it will immediately show you the obvious waste. Thirty minutes.

**Jordan:** Second, identify your top five zombie resources. Unattached volumes, unused IPs, orphaned snapshots. One hour to find them, decide which are safe to delete.

**Alex:** Third, schedule one non-production environment. Pick your lowest-risk dev cluster and set up automatic shutdown overnight. Two hours to implement and test.

**Jordan:** Fourth, present your findings to your manager. Here's what I found, here's the potential savings, here's what I'd need to do more. Thirty minutes.

**Alex:** You do those four things, and you walk into year-end reviews with a concrete story. "I found fifteen thousand in annual savings in three hours. Imagine what I could do with proper tooling and time."

**Jordan:** Let's bring it back to that number we started with. Seven hundred twenty billion dollars in global cloud spend this year.

**Alex:** Your slice of that pie, whatever it is, you now know how to shrink it. Twenty to thirty percent waste isn't inevitable. It's just undiscovered opportunity.

**Jordan:** And the platform engineers who can articulate the business value of optimization? Those are the ones who get budget for the projects that actually matter.

**Alex:** Start with scheduling. Move to right-sizing. Build credibility. Then tackle the bigger optimizations with leadership buy-in.

**Jordan:** The fundamentals haven't changed. Visibility leads to action. Action leads to savings. Savings leads to trust. And trust leads to investment in your platform.

**Alex:** Happy optimizing, and happy year-end. You've got this.
