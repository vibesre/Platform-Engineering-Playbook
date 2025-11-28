# Episode #039: Black Friday War Stories - Lessons from E-Commerce's Worst Days

## Episode Framework: Economic Detective

### Central Mystery/Tension
Why do major retailers with unlimited budgets still crash on Black Friday year after year? The answer reveals fundamental truths about distributed systems, human error, and why "throwing money at the problem" doesn't work.

## Episode Structure

### Act 1: The Opening Hook (1-2 min)
**The Pattern**: Every year, despite knowing exactly when Black Friday will happen, major retailers crash.

Key Hook Points:
- 2018: Walmart, J.Crew, Best Buy, Lowe's, Ulta all crashed
- 2020: 48 major brands experienced outages during BFCM
- 2023: Harvey Norman lost 60% of online sales
- 2024: Cloudflare outage froze 99.3% of Shopify stores (6M+ domains)

The question: If you know the traffic is coming a year in advance, why can't you prepare?

### Act 2: The Hall of Fame Crashes (4-5 min)

#### Segment 1: The $775,000 Five-Hour Window
**J.Crew Black Friday 2018**
- Site crashed periodically across 5 hours
- 323,000 shoppers affected
- $775,000 in lost sales
- "Hang on a Sec" screen became infamous

#### Segment 2: The $9 Million Walmart Wednesday
**Walmart Thanksgiving Eve 2018**
- Issues started Wednesday, November 21 at 10pm ET
- 3.6 million shoppers affected
- $9 million in lost sales
- Problems before Black Friday even started

#### Segment 3: The Mobile Traffic Surprise
**Best Buy Black Friday 2014**
- "Concentrated spike in mobile traffic triggered issues"
- Site taken offline for ~1 hour
- Lesson: Infrastructure optimized for desktop, mobile was 78% of traffic
- Same pattern seen at Fastly 2023 (optimized for 60% mobile, got 78%)

#### Segment 4: The Cascading Failures
**Target Cyber Monday 2015**
- Offered 15% off virtually everything
- Traffic exceeded their "biggest day ever" from Thursday
- Site fluctuated between error messages and normal operations
- Had to plead for patience on social media

### Act 3: The Famous Non-Black-Friday Disasters (3-4 min)

#### The $150 Million Typo
**AWS S3 Outage - February 28, 2017**
- One engineer, one typo, 4 hours and 17 minutes of chaos
- Intended to remove "a few servers" from billing system
- Actually removed critical subsystem servers
- Impact: Netflix, Airbnb, Slack, Docker, Expedia, 100,000+ sites
- S&P 500 companies lost $150 million (Cyence estimate)
- AWS's own status dashboard was down (relied on S3)
- Recovery slow because "subsystems hadn't been restarted in years"

**Key Takeaways:**
1. Even AWS doesn't restart their critical systems regularly
2. Safeguards against "minimum capacity" were missing
3. Single region dependency = single point of failure

#### The GitLab Database Deletion
**GitLab.com - January 31, 2017**
- Engineer meant to wipe secondary database, wiped primary
- 300GB of live production data deleted
- Lost: 5,000 projects, 700 user accounts
- 5 backup systems - NONE working
  - PostgreSQL version mismatch (9.2 vs 9.6)
  - Backup failures were silent (DMARC email issues)
  - No one owned backup validation
- Saved by luck: 6-hour-old snapshot taken for testing
- 18-hour recovery, live-streamed to 5,000 viewers

**Key Takeaways:**
1. If you don't test restores, backups don't exist
2. Backups need explicit ownership
3. Transparency during incidents builds trust

### Act 4: The k8s.af Collection (2-3 min)
**Kubernetes Failure Stories**
- Community collection maintained by Henning Jacobs (Zalando)
- Categories of failures:
  - CPU limits causing high latency
  - IP ceilings preventing autoscaling
  - Missing application logs
  - Killed pods, 502 errors
  - Control plane failures

**Notable k8s.af stories:**
- Target: Cascading failures
- Monzo: Major outage affecting payments
- JW Player: Cryptocurrency miner in internal clusters
- Zalando: AWS, Ingress, CronJob, etcd, flannel issues

**The distributed systems truth:** "A Kubernetes API server outage should not affect running workloads, but it did."

### Act 5: Why This Keeps Happening (2-3 min)

#### The Fundamental Problems

1. **Complexity Growth**
   - Retail sites have gotten more complex over time
   - More sluggish, more prone to bugs
   - Mobile traffic explosion wasn't predicted

2. **Load Testing Gap**
   - "If you have not load tested at 5x normal traffic, your site will probably fail" - Bob Buffone, CTO Yottaa
   - Most companies test at 2x, get hit with 10x

3. **Third-Party Dependencies**
   - Cloudflare outage 2024: One CDN, 6M Shopify stores
   - PayPal 2015: 70% of users couldn't pay
   - Single points of failure in the supply chain

4. **The Rarity Problem**
   - AWS: "Subsystems hadn't been restarted in years"
   - GitLab: "No one owned backup validation"
   - Skills atrophy when you don't practice

### Act 6: The Platform Engineer's Playbook (2-3 min)

**Pre-Traffic Season Checklist:**

1. **Load Test at 5-10x**
   - Not 2x, not "expected peak"
   - Test the failure modes, not just success

2. **Multi-CDN/Multi-Cloud Strategy**
   - Never be at the mercy of single provider
   - Cross-cloud failovers

3. **Test Your Restores**
   - Monthly restore drills
   - Explicit ownership of backup validation
   - Alerts on silent failures

4. **Practice Chaos**
   - Regularly restart systems that "never restart"
   - Game days before peak traffic
   - Know your recovery time under pressure

5. **Mobile-First Infrastructure**
   - 78%+ of traffic is mobile
   - Test mobile experience under load

6. **Safeguards on Dangerous Commands**
   - Minimum capacity checks
   - Slow rollout of removals
   - Confirmation for destructive operations

### Closing (1 min)

The uncomfortable truth: These outages aren't caused by lack of budget or talent. They're caused by complexity, assumptions, and the gap between "should work" and "actually tested."

Every one of these incidents could have been prevented by practices platform engineers know well: test your restores, load test beyond expectations, own your dependencies, and practice failure.

As we head into another Black Friday season, ask yourself: When was the last time your team actually restored from backup? When did you last restart that system that "never needs restarting"?

The best time to find out your backups don't work is not during an incident.

---

## Sources

### Black Friday Outages
- [Retail TouchPoints: 2018 BFCM Outages](https://www.retailtouchpoints.com/features/news-briefs/site-outages-plague-walmart-j-crew-lowe-s-best-buy-office-depot-during-black-friday-weekend)
- [Fast Company: 48 Retail Sites with Issues 2020](https://www.fastcompany.com/90580744/black-friday-and-cyber-monday-outages-angered-customers-on-these-48-retail-sites)
- [CBS News: Best Buy 2014 Crash](https://www.cbsnews.com/news/best-buys-site-crashes-at-the-worst-possible-time/)
- [TechCrunch: Target 2015 Outage](https://techcrunch.com/2015/11/30/target-com-latest-to-crash-from-increased-online-traffic/)
- [Kinsta: Black Friday Downtime Costs](https://kinsta.com/blog/black-friday-website-downtime/)
- [eMarketer: Cloudflare 2024 Outage](https://www.emarketer.com/content/cloudflare-outage-disrupts-black-friday)

### AWS S3 Outage
- [NPR: The $150 Million Typo](https://www.npr.org/sections/thetwo-way/2017/03/03/518322734/amazon-and-the-150-million-typo)
- [AWS Official Postmortem](https://aws.amazon.com/message/41926/)
- [Gremlin: After the Retrospective](https://www.gremlin.com/blog/the-2017-amazon-s-3-outage)
- [MIT Technology Review: Big Cloud Problem](https://www.technologyreview.com/2017/03/03/153431/amazons-150-million-typo-is-a-lightning-rod-for-a-big-cloud-problem/)

### GitLab Incident
- [GitLab Official Postmortem](https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/)
- [TechCrunch: Backup Failure](https://techcrunch.com/2017/02/01/gitlab-suffers-major-backup-failure-after-data-deletion-incident/)
- [Bytes Sized Design: How GitLab Lost 300GB](https://bytesizeddesign.substack.com/p/how-gitlab-lost-300gb-of-production)

### Kubernetes Failures
- [k8s.af - Kubernetes Failure Stories](https://k8s.af/)
- [GitHub: kubernetes-failure-stories](https://github.com/hjacobs/kubernetes-failure-stories)
- [Cloud Native Now: 5 Failure Stories](https://cloudnativenow.com/editorial-calendar/best-of-2021/how-not-to-use-kubernetes-5-failure-stories/)

### Cost Statistics
- Gartner: Average IT downtime cost $5,600/minute
- Uptime Institute 2024: 16% of outages cost more than $1 million
- Acronis: 60% of downtime events cost more than $100,000 (up 39% since 2019)
- 2023 BFCM: $38 billion spent between Thanksgiving and Cyber Monday

---

## Episode Metadata

**Title:** Black Friday War Stories: Lessons from E-Commerce's Worst Days
**Duration:** ~12-15 minutes
**Speakers:** Jordan and Alex
**Target Audience:** Platform engineers, SREs, DevOps engineers preparing for high-traffic events

**Key Takeaways:**
1. Load test at 5-10x expected traffic, not 2x
2. Test your backup restores monthly - if untested, they don't exist
3. Multi-CDN/multi-cloud strategies prevent single-provider failures
4. Regularly restart systems that "never need restarting"
5. Dangerous commands need safeguards (minimum capacity, slow rollout)
6. Mobile is 78%+ of traffic - test mobile experience under load
