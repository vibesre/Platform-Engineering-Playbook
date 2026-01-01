---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #076: Alert Fatigue to Signal-Driven Ops"
slug: 00076-alert-fatigue-signal-driven-observability
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #076: From Alert Fatigue to Signal-Driven Ops - The Observability Shift

<GitHubButtons />

**Duration**: 22 minutes | **Speakers**: Jordan & Alex

**Target Audience**: Senior platform engineers, SREs, and DevOps engineers managing observability at scale

---

## Synopsis

Why do 73% of organizations experience outages from alerts they ignored? This episode breaks down the technical shift from reactive thresholds to SLO-driven observability. Learn multi-window burn-rate alerting patterns straight from the Google SRE workbook, AIOps implementations that actually work in production, and an 8-week migration path to cut alert noise by 80%.

<iframe width="100%" height="315" src="https://www.youtube.com/embed/nx0XgbtnsPc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

## Chapter Markers

- **00:00** - Introduction & The Alert Fatigue Paradox
- **01:30** - News Segment: Grafana Mimir CVEs, OpenTelemetry at Scale
- **03:00** - Scale of the Problem: 2000+ Weekly Alerts, 3% Actionable
- **05:00** - Technical Causes: Static Thresholds, Compound Rules, Alert Storms
- **08:00** - Signals vs Alerts: The Fundamental Difference
- **10:00** - SLO-Driven Observability: SLI, SLO, Error Budgets
- **13:00** - Multi-Window, Multi-Burn-Rate Alert Patterns
- **15:30** - AIOps That Works: Anomaly Detection, Event Correlation
- **18:00** - The 2025 Signal-Driven Observability Stack
- **20:00** - 8-Week Migration Path
- **21:30** - Three Principles for 2026

---

## News Segment (December 31, 2025)

- **Grafana Mimir 2.17.4**: Patches two Go CVEs (CVE-2025-61729, CVE-2025-61727) - update immediately if running in production
- **[OpenTelemetry Enterprise Reality](https://thenewstack.io/)**: Major streaming company running 10,000 OTel instances with 40 dedicated staff. Quote: "Everywhere I go that has OpenTelemetry, you have 20-30 person teams."

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Outages from ignored alerts | 73% | Splunk State of Observability 2025 |
| Weekly alerts per team | 2,000+ | Industry surveys |
| Actionable alert rate | 3% | Industry surveys |
| Alerts simply ignored (mid-size companies) | 27% | Industry surveys |
| OpenTelemetry adoption | 48% | Splunk 2025 |
| AI-driven observability in production | 64% | Cloud-native enterprises |
| Software engineers reporting burnout | 83% | Industry surveys |
| SREs spending 50%+ on toil | 57% | DORA 2025 |
| Unplanned downtime cost | $5,600/minute | Industry average |
| Alert noise reduction achievable | 80% | Thoughtworks case study |
| Manual investigation time reduction (AIOps) | 40% | Industry research |

---

## Technical Concepts Covered

### Three Patterns Causing Alert Fatigue

1. **Static Thresholds**: Set once, never tuned, drift into irrelevance
2. **Compound Rule Blind Spots**: "CPU > 80 AND memory > 90" misses real issues
3. **Alert Storms**: One root cause triggers 50+ cascading alerts

### SLO-Driven Observability Components

- **SLI (Service Level Indicator)**: User-facing measurement (e.g., P99 latency)
- **SLO (Service Level Objective)**: Target from product requirements (e.g., 99.9% under 200ms)
- **Error Budget**: Allowable failure (0.1% = ~43 minutes/month)

### Multi-Window, Multi-Burn-Rate Alerting

| Burn Rate | Window | Budget Consumption | Action |
|-----------|--------|-------------------|--------|
| 14.4x | 2 min | 2% in 2 hours | Page immediately (critical) |
| 6x | 15 min | 2% in 6 hours | Page (warning) |
| 3x | 1 hour | 2% in 24 hours | Create ticket |

### AIOps Patterns That Work

1. **Anomaly Detection**: Time-series models (Prophet, Isolation Forest) learn "normal" patterns
2. **Event Correlation**: Topology-aware grouping reduces 50 alerts to 1 incident
3. **Root Cause Acceleration**: Automated context gathering before on-call opens alert

---

## 2025 Signal-Driven Observability Stack

| Layer | Purpose | Options |
|-------|---------|---------|
| Unified Telemetry | Single SDK for traces, metrics, logs | OpenTelemetry |
| Intelligent Alerting | SLO engine, correlation engine | Grafana SLO, Datadog SLO, Nobl9 |
| Context Enrichment | Automated runbooks, deploy correlation | Platform-specific |
| SLO Management | Error budget tracking | Pyrra, Sloth (open source) |

---

## 8-Week Migration Path

**Weeks 1-2: SLO Audit**
- Identify top 5 services by alert volume
- Map alerts to user-facing impact
- Draft SLOs from product requirements

**Weeks 3-4: Pilot**
- Pick highest alert fatigue service
- Implement multi-window, multi-burn-rate alerts
- Keep old alerts in warning mode for comparison

**Weeks 5-8: Measure & Iterate**
- Track: pages/week, actionable rate, MTTR
- Target: 30-50% actionable alert rate
- Iterate SLO targets based on incidents

---

## Three Principles for 2026

1. **Error budgets over thresholds**: If you can't tie an alert to an SLO, question whether it should page
2. **Context before page**: Every alert should answer: what happened, what's affected, what should I do first
3. **Measure alert quality**: Track actionable rate - if under 30%, fix the alerts, not the humans

---

## Resources Mentioned

- [Google SRE Workbook: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Pyrra](https://github.com/pyrra-dev/pyrra) - SLO management for Prometheus
- [Sloth](https://github.com/slok/sloth) - SLO generator for Prometheus
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- Grafana, Datadog, Nobl9 for SLO platforms

---

## Transcript

**Alex**: This is the Platform Engineering Playbook Daily Podcast—today's news and a deep dive to help you stay ahead in platform engineering.

Today we're closing out twenty twenty-five with a topic that's been simmering all year: alert fatigue. Specifically, why seventy-three percent of organizations experience outages from alerts they ignored or suppressed. Not because they lacked monitoring—because they had too much of it.

**Jordan**: And that stat from Splunk's State of Observability twenty twenty-five report is the perfect paradox. We've never had more visibility into our systems. OpenTelemetry adoption is at forty-eight percent. AI-driven observability is in production at sixty-four percent of cloud-native enterprises. Yet alert fatigue is still the number one obstacle to faster incident response, outpacing everything else by two to one.

**Alex**: Before we dig into that, let's hit some news. First up—a bit meta given our topic—Grafana Mimir two point seventeen point four dropped, patching two Go CVEs. CVE twenty twenty-five sixty-one seven twenty-nine and CVE twenty twenty-five sixty-one seven twenty-seven. If you're running Mimir in production, update today.

**Jordan**: And staying on the observability theme, there's a really sharp piece from The New Stack titled "From Group Science Project to Enterprise Service: Rethinking OpenTelemetry." The numbers they cite are wild. One major streaming company went from using New Relic and Datadog to running ten thousand OTel instances in-house, with forty people dedicated just to maintaining the stack.

**Alex**: Forty people. That's not observability, that's a department.

**Jordan**: Exactly. And the author notes this is common. Quote: "Everywhere I go that has OpenTelemetry, you have twenty or thirty person teams." And even hundred-million-dollar companies need two or three dedicated OTel experts. The data volume explosion is creating four to five X increases in telemetry, which is unsustainable with traditional backends like Splunk or Elastic.

**Alex**: Which ties directly into today's main topic. More data, more alerts, but are teams actually responding faster? Let's find out.

Let me set up the scale of the problem. According to recent research, teams receive over two thousand alerts weekly. Only three percent need immediate action. Among companies with five hundred to fifteen hundred employees, twenty-seven percent of alerts are simply ignored or never investigated.

**Jordan**: Wait—not triaged and closed. Just... ignored?

**Alex**: Ignored. And when you look at what healthy systems achieve—thirty to fifty percent actionable alert rates—most teams are running at under ten percent actionable. That means nine out of ten alerts are noise.

**Jordan**: And the human cost is measurable. Eighty-three percent of software engineers report burnout. Fifty-seven percent of SREs still spend more than half their week on toil, despite AI tool adoption. And here's the business case: unplanned downtime costs five thousand six hundred dollars per minute on average.

**Alex**: The Grafana survey found that alert fatigue is the number one obstacle to faster incident response across almost all organizational levels. And when they asked about SLO adoption, the most common goal was reduced MTTR at thirty-three percent, followed by better accountability, then reduced alert noise at sixteen percent.

**Jordan**: So there's acknowledgment that alert noise is a problem. But what's causing it technically? Let's go deep here because I think most teams don't actually understand the mechanics.

**Alex**: Three main patterns, and they compound each other. First, static thresholds. CPU greater than eighty percent, page on-call. These get set once during initial deployment, never tuned, and drift into irrelevance as workloads evolve. The traffic pattern from six months ago isn't today's traffic pattern.

**Jordan**: And that eighty percent number—where did it even come from?

**Alex**: Usually someone's gut during the initial setup. Or worse, copied from a blog post that was written for completely different hardware and workloads. A database server running at eighty percent CPU might be perfectly healthy if it's batch processing overnight jobs. A web server at eighty percent during peak traffic might be fine, but the same server at eighty percent at two AM is probably a problem.

**Jordan**: So the threshold itself is meaningless without context.

**Alex**: Right. And compound rules feel smart but create blind spots. CPU greater than eighty AND memory greater than ninety. Sounds surgical, but now you miss the scenario where CPU is at ninety-five but memory is only at eighty-eight. Or the reverse—memory is at ninety-nine percent but CPU is only at seventy, so no alert fires.

**Jordan**: Second pattern?

**Alex**: The golden signal fallacy. Latency, traffic, errors, saturation—the SRE handbook's four golden signals—only work if you've baselined what "normal" looks like for your specific system. Without that baseline, you're setting arbitrary thresholds again. And most teams don't have baselines that account for time-of-day, day-of-week, or seasonal patterns.

**Jordan**: So Monday morning at nine AM looks different from Sunday at three AM, and your alert rules need to know that.

**Alex**: Exactly. A twenty percent spike in latency on Black Friday is expected. The same spike on a random Tuesday might be a real problem.

**Jordan**: And third pattern is alert storms. This one really burns people.

**Alex**: Alert storms are when one root cause triggers a cascade. Say your primary database goes read-only. Every service that writes to that database now throws errors. Every retry mechanism fires. Every health check fails. The on-call gets paged fifty times in five minutes for what is actually one incident.

**Jordan**: I've seen hundred-alert storms from a single network partition.

**Alex**: And here's what makes it worse: during an alert storm, the real signal gets buried. The one alert that actually tells you "database went read-only" is page fifty-three in your PagerDuty queue. By the time you find it, you've already wasted twenty minutes triaging phantom alerts.

**Jordan**: So the very mechanism designed to get human attention is preventing humans from understanding what's happening.

**Alex**: That's the paradox. And this is why the industry is moving from alerts to signals, and from reactive thresholds to SLO-driven observability. Let me explain what that actually means technically.

**Jordan**: Break it down. What's the actual difference between an alert and a signal?

**Alex**: An alert is binary. Threshold crossed, human attention demanded. It's reactive by design. A signal is a contextual indicator that something has changed. It requires interpretation. It can be correlated with other signals.

Here's a concrete example. The alert approach: if CPU usage greater than eighty percent, then page on-call. The signal approach: if CPU usage deviates more than two standard deviations from a seven-day rolling baseline, AND that deviation correlates with increased error rate, AND it's affecting SLO burn rate—then classify severity and enrich context.

**Jordan**: So signals are richer but also more complex to implement.

**Alex**: Right. And the key enabling concept is SLO-driven observability. Instead of alerting on infrastructure metrics, you alert on user impact. This is a fundamental shift in how you think about monitoring.

**Jordan**: Walk through the technical layers in detail.

**Alex**: Three components. First, the SLI—Service Level Indicator. That's your measurement. It has to be something that matters to users, not just something that's easy to measure. For example, request latency at the ninety-ninth percentile. Or success rate of checkout transactions. Or time from order placement to confirmation email.

Second, the SLO—Service Level Objective. That's your target. Ninety-nine point nine percent of requests complete under two hundred milliseconds. The key insight here is that this number should come from product requirements and user research, not from ops guesses about what feels right.

Third, the error budget. This is the game-changer. If your SLO is ninety-nine point nine percent success rate, your error budget is point one percent. Over a thirty-day month, that's roughly forty-three minutes of total downtime or degradation you can "spend."

**Jordan**: And the magic happens in how you consume that error budget.

**Alex**: Exactly. Instead of "latency greater than two hundred milliseconds equals page," you track error budget burn rate. This is where the math gets interesting. A slow burn—consuming error budget at one X rate—means you're on track to exactly exhaust your budget by month end. That's investigate tomorrow. A fast burn—ten X rate—means you'll exhaust your error budget in three days instead of thirty. Page now. A critical burn—one hundred X rate—means you'll blow through your entire monthly budget in seven hours. All hands.

**Jordan**: Can you give me an actual implementation pattern?

**Alex**: Sure. This is the multi-window, multi-burn-rate alert pattern from the Google SRE workbook. The insight is that you need multiple time windows because different burn rates manifest at different timescales.

In Prometheus, you'd set up something like this. First, define your SLI using recording rules. Track request success rate over one-minute, five-minute, and thirty-minute windows. Then calculate burn rate as the ratio of observed error rate to your error budget.

The alert rule looks like: alert named SLO Burn Rate Fast, expression that divides your five-minute error rate by your remaining error budget. If that ratio exceeds fourteen point four for two minutes, page with severity critical. If it exceeds six for fifteen minutes, page with severity warning. If it exceeds three for an hour, create a ticket.

**Jordan**: Why fourteen point four specifically?

**Alex**: It's math based on budget consumption. If you're consuming two percent of your monthly error budget in two hours, that's a fourteen point four X burn rate. The six and three burn rates are calibrated for six-hour and twenty-four-hour consumption respectively. The numbers are designed so that each tier catches a specific class of problem: sudden spikes, fast degradation, and slow creep.

**Jordan**: So the system knows the difference between "this is bad but can wait until morning" versus "wake someone up now."

**Alex**: Precisely. And here's why this works better than static thresholds. Error budgets prevent "cry wolf" scenarios because they're tied to actual user impact. If users aren't affected, you're not burning budget. If users are affected, you know exactly how much runway you have before you breach your commitments.

Window-based rates catch both fast and slow problems. A three-hour window catches things that a five-minute window would miss, and vice versa. And critically—SLOs come from product requirements, not ops guesses. When product says "users expect checkout to complete in under two seconds ninety-nine percent of the time," that becomes your SLO. Everyone is aligned on what "good" means.

**Jordan**: Now let's talk about the AI layer. AIOps has been hyped for years. What's actually working in twenty twenty-five?

**Alex**: Three patterns that deliver real results, and I want to go deep on the implementation because this is where the marketing claims diverge from reality.

First, anomaly detection. Time-series models like Prophet, Isolation Forest, or Facebook Kats learn what "normal" looks like for your system, including seasonal variations. Monday morning traffic looks different from Sunday at three AM. End-of-month billing runs look different from mid-month.

The implementation typically works like this: you feed the model several weeks of historical data. It learns the patterns—hourly cycles, daily cycles, weekly cycles, even monthly patterns. Then it continuously compares current observations against predicted values. When the deviation exceeds a configurable number of standard deviations, it flags an anomaly.

**Jordan**: So instead of saying "latency greater than two hundred milliseconds," you're saying "latency is two standard deviations higher than expected for this time on this day of the week."

**Alex**: Exactly. And the models catch things static thresholds miss, like gradual degradation over weeks. If your P99 latency increases by five milliseconds every day for three weeks, a static threshold won't fire until you're way over the line. An anomaly detector notices the trend early.

The gotcha is that these models need clean training data and ongoing maintenance. If you train on data that includes incidents, the model learns that incidents are normal. You also need to retrain periodically as your system evolves.

Second pattern: event correlation. Modern platforms have topology awareness—they know that pod connects to node connects to cluster, that service A depends on service B depends on database C.

**Jordan**: How does that actually work technically?

**Alex**: It's built on a knowledge graph or dependency map. Some platforms discover this automatically through network flow analysis or tracing. Others require explicit configuration. When an alert fires, the correlation engine looks at the topology and asks: are there other alerts on related components? Is there a common ancestor that could explain all of them?

So when a node has memory pressure and fifty pods start failing, instead of getting fifty separate alerts, you get one incident: "Node X memory pressure causing cascading pod failures." The fifty individual alerts are suppressed or attached as context.

**Jordan**: That's huge for reducing noise during actual incidents.

**Alex**: Third pattern: root cause analysis acceleration. AI automatically gathers context—logs, metrics, traces, recent deploys—before the on-call even looks at the incident. Research shows this reduces manual investigation time by forty percent.

The implementation here is basically an automated runbook. When an alert fires, the system automatically queries: what changed in the last hour? Were there any deploys? What do the logs say around the alert timestamp? What does the trace look like for a sample of failing requests?

This context is attached to the alert before it pages anyone. So when the on-call opens PagerDuty, they don't start from zero—they start with a hypothesis.

**Jordan**: Real results in production?

**Alex**: Thoughtworks published a case study about building a proactive observability stack with Datadog on EKS. They achieved eighty percent reduction in alert noise and fifty percent reduction in MTTR using monitors-as-code, unified tagging, chaos validation, and SLO-based alert design.

But here's the reality check. They also note this took several months of dedicated engineering effort. You don't get these results by just enabling a feature toggle.

**Jordan**: There's a catch, right? I've heard people talk about "Alert Fatigue two point zero."

**Alex**: Yeah, this is the twenty twenty-five reality check. AI hallucinations in incident detection create mistrust. The correlation engine sometimes groups unrelated alerts because they happened at the same time. The anomaly detector sometimes flags normal behavior as anomalous.

Engineers end up double-checking every AI-generated insight manually—which is a new form of toil. The twenty twenty-five State of DevOps Report notes that SREs are realizing AI has shifted the type of toil, not eliminated it.

The answer isn't to remove humans from the loop. It's AI for enrichment and correlation, human for judgment. The AI suggests "these alerts might be related," and the human decides whether that's actually true.

**Jordan**: Let's get practical. What does the twenty twenty-five signal-driven observability stack actually look like?

**Alex**: Layer one: unified telemetry with OpenTelemetry. Single SDK for traces, metrics, logs. The challenge is scale—those twenty to forty person teams we mentioned earlier. The solution is start with auto-instrumentation, which gives you eighty percent of the value with twenty percent of the effort. Add manual spans only for critical paths where you need more granularity.

Layer two: intelligent alerting platform. SLO engine that calculates burn rates, not thresholds. Correlation engine with topology awareness. Options include Grafana SLO—which is open source, Datadog SLO—which is managed, Nobl9—which specializes in SLO management, and Google Cloud SLO if you're on GCP.

Layer three: context enrichment. Automated runbook attachment so every alert comes with relevant documentation. Recent deployment correlation so you immediately know if something changed. On-call context like who's primary, who's secondary, and who has historical knowledge of this service.

**Jordan**: What's the migration path for a team currently drowning in alerts?

**Alex**: Week one and two: SLO audit. Identify your top five services by alert volume. Map existing alerts to user-facing impact—you'll find that many alerts don't actually correlate with user-visible problems. Draft SLOs based on actual requirements—ask product what users expect, don't guess.

Weeks three and four: pilot. Pick one service with the highest alert fatigue. Implement multi-window, multi-burn-rate alerts for that service. Keep old alerts in warning mode—don't page on them—so you can compare signal quality side by side.

Weeks five through eight: measure and iterate. Track pages per week, actionable alert ratio, and MTTR. Your goal is thirty to fifty percent actionable rate. Iterate SLO targets based on what you learn from actual incidents.

The key is not to do a big-bang migration. Run both systems in parallel and compare results. This gives you confidence that the new system is actually better before you decommission the old one.

**Jordan**: Let's talk tooling honestly. What are the trade-offs?

**Alex**: Open source stack: OpenTelemetry Collector, Prometheus, Grafana. Alertmanager with SLO-based routing. Pyrra or Sloth for SLO management. Cost is free, but expect twenty plus hours per week ops burden for a medium-sized deployment.

Managed stack: Datadog, New Relic, Splunk, Elastic. Built-in SLO management and AIOps features. Trade-off is fifty thousand to five hundred thousand dollars per year depending on data volume. But you're buying time—your team focuses on application logic, not observability infrastructure.

What most teams actually do is hybrid: OpenTelemetry for collection because it gives you portability and vendor independence. Managed backend for storage and analysis because running Prometheus at scale is hard. Custom SLO dashboards via Grafana because it integrates with everything.

**Jordan**: So to summarize the paradigm shift.

**Alex**: Old model: detect everything, alert on everything, hope humans filter the noise. New model: define what matters through SLOs, measure deviation from those objectives, alert on user impact not infrastructure metrics.

**Jordan**: Three principles for twenty twenty-six.

**Alex**: One: error budgets over thresholds. If you can't tie an alert to an SLO, question whether it should page. Thresholds that don't correlate with user impact are noise generators.

Two: context before page. Every alert should answer three questions before waking someone up: what happened, what's affected, and what should I do first? If the on-call has to spend ten minutes gathering context, that's ten minutes of MTTR you could have saved.

Three: measure alert quality. Track your actionable rate—the percentage of alerts that resulted in actual remediation work. If it's under thirty percent, you have a signal-to-noise problem. Fix the alerts, not the humans.

**Jordan**: The teams winning at observability aren't the ones with the most dashboards. They're the ones who can answer "are we meeting our commitments to users" with a single glance.

**Alex**: If this breakdown helped clarify how to move from alert fatigue to signal-driven ops, subscribing helps us know to make more content like this.

**Jordan**: That's the shift from visibility to signal. The tools are ready. The patterns are proven. The only question is whether you're willing to rethink what "good monitoring" means. Happy New Year—let's make twenty twenty-six the year of actionable observability.

---

## Related Episodes

- [Episode #048: Developer Experience Metrics Beyond DORA](/podcasts/00048-developer-experience-metrics-beyond-dora)
- [Episode #047: Cloudflare's December 2025 Outage and Infrastructure Trust](/podcasts/00047-cloudflare-december-2025-outage-trust-crisis)

---

## Stay Connected

Found this valuable? Here's how to stay current:

- **Subscribe**: [YouTube](https://www.youtube.com/@PlatformEngineeringPlaybook) | [Apple Podcasts](https://podcasts.apple.com/us/podcast/platform-engineering-playbook/id1234567890) | [Spotify](https://open.spotify.com/show/yourshowid)
- **Contribute**: See a mistake? [Open a PR on GitHub](https://github.com/platformengineeringplaybook/platformengineeringplaybook)
