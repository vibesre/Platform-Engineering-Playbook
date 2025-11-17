---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "DORA Metrics"
slug: /technical/dora-metrics
---

# DORA Metrics: Measuring Platform Engineering Success

<GitHubButtons />

## What Are DORA Metrics?

DORA (DevOps Research and Assessment) metrics are the industry-standard framework for measuring software delivery performance and operational excellence. Developed by the DORA research team (now part of Google Cloud), these metrics are based on years of research across thousands of organizations.

**Why DORA Metrics Matter for Platform Engineering:**

Platform teams exist to improve developer productivity and software delivery performance. DORA metrics provide objective, measurable indicators of whether your platform is actually delivering value or becoming a bottleneck.

> **Critical Insight:** The 2024 DORA Report found that platform teams initially **decreased throughput by 8% and stability by 14%**. Measuring DORA metrics helps you track when you move from the initial complexity phase to delivering real productivity gains.

---

## The Four Key DORA Metrics

### 1. Deployment Frequency

**Definition:** How often your organization successfully releases code to production.

**Why It Matters:**
- Higher deployment frequency enables faster feedback loops
- Correlates with smaller, less risky changes
- Indicates platform enables rapid iteration

**Measurement:**
- Count deployments to production per day/week/month
- Track per team, per service, or organization-wide
- Automated deployments only (exclude manual releases)

**Benchmark Targets:**

| Performance Level | Deployment Frequency |
|-------------------|---------------------|
| Elite | On-demand (multiple per day) |
| High | Between once per day and once per week |
| Medium | Between once per week and once per month |
| Low | Between once per month and once every 6 months |

**Platform Engineering Impact:**
- Platforms should enable on-demand deployments
- CI/CD automation directly impacts this metric
- Self-service capabilities reduce deployment friction

---

### 2. Lead Time for Changes

**Definition:** The time it takes for a code commit to reach production.

**Why It Matters:**
- Shorter lead times enable faster experimentation
- Reduces work-in-progress and context switching
- Measures end-to-end efficiency of delivery pipeline

**Measurement:**
- Start: When code is committed to version control
- End: When code is successfully running in production
- Track median and 95th percentile (outliers matter)

**Benchmark Targets:**

| Performance Level | Lead Time for Changes |
|-------------------|----------------------|
| Elite | Less than 1 hour |
| High | Between 1 day and 1 week |
| Medium | Between 1 week and 1 month |
| Low | Between 1 month and 6 months |

**Platform Engineering Impact:**
- Automated CI/CD reduces wait times
- Self-service infrastructure provisioning eliminates bottlenecks
- Golden paths optimize for common use cases

---

### 3. Change Failure Rate

**Definition:** The percentage of deployments that result in degraded service or require remediation.

**Why It Matters:**
- Balance speed with quality
- Indicates effectiveness of testing and validation
- High failure rates create developer frustration and risk aversion

**Measurement:**
- Count incidents caused by deployments
- Divide by total deployments
- Requires clear incident classification

**Benchmark Targets:**

| Performance Level | Change Failure Rate |
|-------------------|---------------------|
| Elite | 0-15% |
| High | 16-30% |
| Medium | 16-30% (same as high) |
| Low | 31-45%+ |

**Platform Engineering Impact:**
- Automated testing and validation gates
- Progressive delivery (canary, blue-green deployments)
- Observability and monitoring integration
- Rollback capabilities

**Important Note:** Lower isn't always better. A 0% failure rate might indicate teams aren't taking enough risks or innovating.

---

### 4. Time to Restore Service (MTTR)

**Definition:** How long it takes to restore service after an incident or production failure.

**Why It Matters:**
- Failures are inevitable; recovery speed matters more
- Indicates operational maturity and incident response capabilities
- Affects customer trust and business continuity

**Measurement:**
- Start: When incident is detected/reported
- End: When service is fully restored
- Track median and 95th percentile

**Benchmark Targets:**

| Performance Level | Time to Restore Service |
|-------------------|------------------------|
| Elite | Less than 1 hour |
| High | Less than 1 day |
| Medium | Between 1 day and 1 week |
| Low | Between 1 week and 1 month |

**Platform Engineering Impact:**
- Automated rollback and recovery mechanisms
- Comprehensive observability (metrics, logs, traces)
- Incident management workflows
- On-call tooling and runbooks

---

## How to Measure DORA Metrics

### Step 1: Establish Baseline (BEFORE Platform Launch)

**Critical:** 45% of platform teams don't measure anything. You **must** establish baseline metrics before launching your platform to prove ROI.

**Baseline Period:** Measure for 3-6 months before platform goes live

**Data Sources:**
- Version control systems (Git commits, pull requests)
- CI/CD pipelines (Jenkins, GitHub Actions, GitLab CI)
- Deployment tools (Kubernetes, Terraform, Helm)
- Incident management (PagerDuty, Opsgenie, Jira)
- Monitoring/observability (Datadog, New Relic, Grafana)

### Step 2: Automate Data Collection

**Tools for DORA Metrics:**

| Tool | Capabilities | Best For |
|------|-------------|----------|
| [Sleuth](https://www.sleuth.io/) | Automated DORA tracking, integrates with Git/CI/CD | Comprehensive DORA measurement |
| [LinearB](https://linearb.io/) | Engineering metrics, workflow automation | Developer productivity insights |
| [Jellyfish](https://jellyfish.co/) | Engineering management platform | Executive reporting |
| [Haystack](https://www.usehaystack.io/) | DORA metrics, team analytics | Team-level insights |
| [Faros AI](https://www.faros.ai/) | Open-source engineering analytics | Self-hosted solution |
| Custom Dashboards | Build with Grafana, Datadog, etc. | Full control, requires engineering |

### Step 3: Continuous Tracking

**Measurement Cadence:**
- Real-time dashboards for operational monitoring
- Weekly reviews for team retrospectives
- Monthly trends for leadership reporting
- Quarterly deep dives for strategic planning

**Segmentation:**
- Track by team (identify high/low performers)
- Track by service (find bottlenecks)
- Track by environment (prod vs staging patterns)

---

## Common Measurement Challenges

### Challenge 1: Defining "Deployment"

**Problem:** What counts as a deployment? Infrastructure changes? Config changes? Feature flags?

**Solution:**
- Be consistent and document your definition
- Start with application code deployments only
- Expand scope gradually as measurement matures

### Challenge 2: Attributing Incidents

**Problem:** Not all production issues are caused by deployments.

**Solution:**
- Only count incidents caused by recent changes
- Define clear attribution window (e.g., 24 hours post-deploy)
- Exclude infrastructure failures outside team control

### Challenge 3: Gaming the Metrics

**Problem:** Teams optimize for metrics instead of outcomes.

**Solution:**
- Measure all four metrics together (no cherry-picking)
- Focus on trends, not absolute numbers
- Pair quantitative metrics with qualitative feedback (NPS)
- Review outliers (very high or very low)

### Challenge 4: Multi-Service/Microservices Complexity

**Problem:** Hundreds of services make aggregation difficult.

**Solution:**
- Start with critical services (20% that matter most)
- Aggregate by team ownership, not service count
- Use percentile aggregation (median across services)

---

## DORA Metrics for Platform Teams

### Measuring Platform Team Performance

**Platform teams should measure:**

1. **Platform Deployment Frequency**
   - How often platform capabilities ship
   - New features, bug fixes, infrastructure updates

2. **Platform Lead Time**
   - Time from feature request to availability
   - Developer feedback loop speed

3. **Platform Stability**
   - Incidents caused by platform changes
   - Breaking changes impacting developers

4. **Platform Restoration Time**
   - How fast platform issues are resolved
   - Developer blocker resolution speed

### Measuring Platform Impact on Application Teams

**More important:** How does the platform affect application teams' DORA metrics?

**Before/After Comparison:**

| Metric | Before Platform | After Platform | Target |
|--------|----------------|----------------|--------|
| Deployment Frequency | Once per week | Multiple per day | 10x improvement |
| Lead Time | 2 weeks | Under 1 day | 14x improvement |
| Change Failure Rate | 30% | 15% | 2x improvement |
| Time to Restore | 4 hours | Under 1 hour | 4x improvement |

**Warning:** Expect initial regression. The 2024 DORA Report found throughput decreased 8% and stability decreased 14% during platform adoption. Plan for 6-12 month adoption curve.

---

## Beyond DORA: Additional Platform Metrics

While DORA metrics are foundational, platform teams should also track:

### Developer Satisfaction Metrics
- **Developer NPS:** Quarterly surveys (target: over 20)
- **Time to First Value:** Days until new developer is productive (target: under 30 days)
- **Platform Adoption:** Percentage of teams using platform voluntarily (target: over 50%)

### Operational Metrics
- **Onboarding Time:** Hours to deploy first application (target: under 1 day)
- **Ticket Volume:** Platform support requests (lower is better)
- **Documentation Usage:** Page views, search queries (higher is better)

### Business Metrics
- **Cost Efficiency:** Cloud spend per transaction/user
- **Security Compliance:** Time to pass audit
- **ROI:** Productivity gains vs platform cost

---

## Real-World Examples

### Example 1: E-commerce Platform Team

**Before Platform (Baseline - 6 months):**
- Deployment Frequency: 3-4 times per week
- Lead Time: 2-3 days
- Change Failure Rate: 25%
- MTTR: 2 hours

**After Platform (12 months):**
- Deployment Frequency: 50+ times per day (on-demand)
- Lead Time: Under 2 hours
- Change Failure Rate: 12%
- MTTR: 30 minutes

**Business Impact:** Reduced time to market by 75%, increased feature velocity by 10x

### Example 2: Financial Services (Regulatory Environment)

**Before Platform:**
- Deployment Frequency: Monthly releases
- Lead Time: 6 weeks
- Change Failure Rate: 15% (conservative testing)
- MTTR: 24 hours

**After Platform:**
- Deployment Frequency: Weekly releases
- Lead Time: 1 week
- Change Failure Rate: 10%
- MTTR: 4 hours

**Business Impact:** 4x faster delivery while maintaining compliance, improved audit performance

---

## Getting Started: Action Plan

### Week 1: Discovery
- [ ] Identify data sources (Git, CI/CD, incidents)
- [ ] Document current deployment process
- [ ] Interview 5-10 developers about pain points

### Week 2-4: Baseline Measurement
- [ ] Configure automated data collection
- [ ] Measure current DORA metrics (manual if needed)
- [ ] Create dashboard for visibility

### Month 2-3: Analysis
- [ ] Identify bottlenecks in delivery pipeline
- [ ] Benchmark against industry standards
- [ ] Present findings to leadership

### Month 4+: Continuous Improvement
- [ ] Set quarterly improvement targets
- [ ] Review metrics in sprint retrospectives
- [ ] Correlate metrics with platform changes

---

## Resources

### Official DORA Research
- [DORA Official Website](https://dora.dev/)
- [2024 State of DevOps Report](https://dora.dev/research/)
- [DORA Quick Check Tool](https://dora.dev/quickcheck/)

### Books
- "Accelerate: The Science of Lean Software and DevOps" by Nicole Forsgren, Jez Humble, Gene Kim
- "The DevOps Handbook" by Gene Kim, Jez Humble, Patrick Debois, John Willis

### Talks and Articles
- [DORA Metrics: What They Are and Why They Matter](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)
- [How to Misuse DORA Metrics](https://www.infoq.com/articles/misuse-dora-metrics/)

---

## Key Takeaways

1. **Measure Before You Build:** 45% of platform teams can't prove ROI because they never established baselines. Measure DORA metrics for 3-6 months before platform launch.

2. **All Four Metrics Matter:** Don't cherry-pick. High deployment frequency with high failure rate means you're breaking things fast. Balance speed and stability.

3. **Expect Initial Regression:** Platform teams decrease throughput 8% and stability 14% initially. Set stakeholder expectations and plan for 6-12 month adoption curve.

4. **Track Platform Impact:** Your platform's DORA metrics matter less than how you improve application teams' metrics. Measure both.

5. **Pair with Qualitative Feedback:** DORA metrics show what's happening. Developer NPS and interviews explain why. Use both.

6. **Focus on Trends:** Absolute numbers vary by industry and organization. Track improvement over time, not comparison to benchmarks.

---

## Related Content

- [Why 70% of Platform Engineering Teams Fail](/blog/2025-10-28-why-platform-engineering-teams-fail) - The importance of metrics in proving platform ROI
- [Platform Engineering ROI Calculator](/blog/2025-10-28-platform-engineering-roi-calculator) - Calculate the business value of DORA improvements
- [Prometheus Monitoring](/technical/prometheus) - How to instrument systems for DORA metric collection

---

*Last updated: October 30, 2025*
