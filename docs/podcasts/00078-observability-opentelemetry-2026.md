---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #078: Can OpenTelemetry Save Observability in 2026?"
slug: 00078-observability-opentelemetry-2026
---

# Episode #078: Can OpenTelemetry Save Observability in 2026?

<GitHubButtons/>

**Duration**: 18 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Platform engineers, DevOps engineers, SREs

> 📰 **News Segment**: This episode covers GitHub Actions 39% pricing reduction and Jaeger v2.14.0 legacy removal before the main topic.

## Episode Summary

OpenTelemetry has won the instrumentation wars with 95% adoption predicted for 2026. But winning data collection doesn't solve observability's real problems: spiraling costs, signal-to-noise ratios declining, and too much distance between seeing a problem and fixing it. This episode breaks down Netflix's evolution to high-cardinality analytics processing 1M+ spans per episode, the cost-control chokepoint OTel enables, and why 40% of organizations are targeting autonomous remediation by end of 2026.

## News Segment

1. **GitHub Actions Pricing Reduced 39%** - Effective January 1, 2026, GitHub-hosted runners see up to 39% price reduction depending on machine type. Changes the build vs. buy calculation for self-hosted runners.

2. **Jaeger v2.14.0 Removes All Legacy v1 Components** - Breaking change requiring migration to v2 unified binary. Legacy `query`, `collector`, and `ingester` components no longer published.

## Key Takeaways

- **OpenTelemetry adoption**: 95% adoption predicted for 2026, but 43% of organizations haven't seen cost savings—often because they treat the collector as passthrough instead of control plane
- **Netflix scale reality**: 1M+ trace spans per episode, evolved from monolithic tracing to high-cardinality analytics with Flink stream processing
- **Cost-control chokepoint**: OTel collector enables sampling, filtering, and routing decisions that reduce costs—57% of organizations report reduced costs with proper strategy
- **Agent-first observability**: 40% targeting autonomous remediation by end 2026. AI agents becoming first-class consumers of observability data
- **SLOs as business language**: Error budgets become budget conversations, reliability being monetized, platform engineers as translators between telemetry and business impact
- **Decision framework**: Audit collector config, measure signal-to-noise ratio, calculate cost per insight, map remediation path latency

## Resources

- [GitHub Actions Pricing Reduction Announcement](https://github.blog/changelog/2026-01-01-reduced-pricing-for-github-hosted-runners-usage) - Official changelog
- [Jaeger v2.14.0 Release Notes](https://github.com/jaegertracing/jaeger/releases/tag/v2.14.0) - Breaking change details
- [Netflix Observability Evolution - InfoQ](https://www.infoq.com/presentations/stream-pipeline-observability/) - High-cardinality analytics deep dive
- [Can OpenTelemetry Save Observability in 2026? - TheNewStack](https://thenewstack.io/can-opentelemetry-save-observability-in-2026/) - 95% adoption analysis
- [APMdigest 2026 Predictions](https://www.apmdigest.com/2026-observability-predictions-1) - Agent-first observability trends
- [Dynatrace 2026 Predictions](https://www.dynatrace.com/news/blog/six-observability-predictions-for-2026/) - Agentic AI complexity
- [Grafana Observability Survey](https://grafana.com/observability-survey/) - SLOs becoming business conversation
- [Honeycomb AI-Native Observability Suite](https://www.honeycomb.io/blog/honeycomb-introduces-developer-interface-future-with-ai-native-observability-suite) - MCP Server integration

## Transcript

**Alex**: Welcome to the Platform Engineering Playbook Daily Podcast—today's news and a deep dive to help you stay ahead in platform engineering.

Today we're asking a provocative question: Can OpenTelemetry save observability in 2026? Netflix processes over one million trace spans per streaming episode—not per day, per episode. When your observability pipeline handles that scale, you're not just collecting data, you're running a data analytics platform. OpenTelemetry has won the instrumentation wars, but the real battle is just beginning.

**Jordan**: Before we dive into that existential question, we've got two news items that set up today's theme perfectly. First up—GitHub Actions just got a lot cheaper.

**Alex**: Thirty-nine percent cheaper, to be exact. GitHub announced reduced pricing for GitHub-hosted runners. For platform teams running heavy CI/CD workloads, this changes the economics significantly.

**Jordan**: Give me the quick math. What does this mean for a typical platform team?

**Alex**: If you're spending ten thousand dollars a month on GitHub Actions, you're now looking at around six thousand. That's forty-eight thousand in annual savings. It also shifts the build versus buy calculation for self-hosted runners—the cost advantage of managing your own infrastructure just got smaller.

**Jordan**: Interesting timing. Lower CI/CD costs might mean teams have more budget for observability tooling. Speaking of which, the second news item is directly relevant—Jaeger two-point-fourteen just dropped, and it's a breaking change.

**Alex**: A significant one. Jaeger has removed all legacy v1 components. Teams running the old architecture must migrate to the v2 unified binary. No more gradual transition—it's migrate or stay on an unsupported version.

**Jordan**: How many teams are still running v1 in production?

**Alex**: More than you'd think. The v1 architecture with separate collector, query, and agent components has been deprecated for over a year, but migration takes time. The unified binary is actually simpler to operate, but it requires reconfiguring your deployment pipelines, updating your Kubernetes manifests, and potentially changing how you handle storage backends.

**Jordan**: This feels like a symptom of a bigger shift in observability. Projects are maturing, consolidating, and forcing decisions that teams have been deferring.

**Alex**: Exactly the right framing for our main topic. The Jaeger migration is one data point, but the broader question is whether OpenTelemetry—now effectively the universal standard for telemetry collection—can actually solve observability's real problems.

**Jordan**: Let's be precise about what we mean by "real problems." OTel has clearly won the instrumentation battle. What hasn't it solved?

**Alex**: Three things. First, cost—observability spend is spiraling for most organizations. Second, signal-to-noise—teams are drowning in data but struggling to find insights. Third, the action gap—there's too much distance between seeing a problem and actually fixing it.

**Jordan**: Those sound like symptoms rather than root causes.

**Alex**: They are. The root cause is that we've conflated data collection with understanding. OpenTelemetry is phenomenal at the first part—it gives you vendor-agnostic, standardized telemetry. But collecting data was never the hard part. The hard part is extracting insight from the data you collect.

**Jordan**: Let's ground this in a real example. You mentioned Netflix and their one million spans per episode. Walk me through what that actually looks like in practice.

**Alex**: Netflix shared their observability evolution at a recent InfoQ presentation, and it's fascinating. They started where most companies start—traditional distributed tracing. Collect spans, visualize request flows, investigate when things break.

**Jordan**: That sounds reasonable. Where did it break down?

**Alex**: Scale. When you're processing millions of spans per minute, traditional trace storage and query patterns don't work. You can't just throw everything into a tracing backend and expect reasonable query performance. So they evolved their architecture.

**Jordan**: Evolved how?

**Alex**: They moved from monolithic tracing to what they call high-cardinality analytics. Instead of treating traces as the primary data model, they treat observability as a stream processing problem. They use Flink pipelines to process telemetry in real-time, computing aggregates and detecting anomalies as data flows through.

**Jordan**: So they're essentially running a data engineering platform, not just an observability stack.

**Alex**: Exactly. They also developed what they call request-first tree visualization—a new UX paradigm for exploring traces. Instead of starting with a service map or dashboard, you start with a specific request and explore its execution tree. It's a fundamentally different interaction model.

**Jordan**: This sounds impressive, but Netflix has hundreds of engineers who can build custom tooling. How does this help the rest of us?

**Alex**: The pattern matters more than the implementation. The insight is that at scale, observability becomes data engineering. OpenTelemetry gives you the raw material—standardized telemetry—but you need an analytics layer on top. Vendor tools are catching up—Grafana's Root Cause Analysis Workbench, Honeycomb's new AI-native features—but there's still a gap between what OTel collects and what you can actually do with it.

**Jordan**: Let's talk about the economics. You mentioned cost as one of the unsolved problems. I've heard claims that OTel reduces observability costs. Is that true?

**Alex**: The data is mixed. According to recent industry surveys, fifty-seven percent of organizations report reduced costs after adopting OpenTelemetry. But that means forty-three percent didn't see savings—and some actually saw costs increase.

**Jordan**: How is that possible? Isn't vendor-agnostic collection supposed to reduce lock-in and enable cost optimization?

**Alex**: In theory, yes. OTel enables what some analysts call a cost-control chokepoint. Because the collector sits between your applications and your backends, you can implement sampling, filtering, and routing at the collector level. You can send high-value traces to an expensive APM tool and send lower-priority data to cheaper storage.

**Jordan**: So the collector becomes your cost control plane.

**Alex**: Exactly. But here's where the forty-three percent who didn't save money went wrong: they treated the collector as a passthrough. Collect everything, send everywhere. OTel without a sampling strategy is actually more expensive than a single-vendor solution, because you're paying for collection overhead without getting the optimization benefits.

**Jordan**: What does a good sampling strategy look like?

**Alex**: It depends on your workload, but the principles are consistent. First, sample intelligently—keep errors and slow requests, sample successful fast requests. Second, use tail-based sampling when you can, so you make sampling decisions after you know the outcome of the request. Third, tier your storage—hot data in fast storage, cold data in cheap storage, with different retention policies.

**Jordan**: That sounds like a lot of operational complexity that OTel supposedly abstracts away.

**Alex**: It does abstract the instrumentation complexity. But it surfaces configuration complexity. You're trading one type of cognitive load for another. The good news is the configuration complexity is more tractable—it's infrastructure engineering rather than code changes across hundreds of services.

**Jordan**: Let's shift to the third problem you mentioned—the action gap. This seems related to the agent-first observability trend I keep hearing about.

**Alex**: It's the defining trend of 2026 observability. The APMdigest predictions survey found that forty percent of organizations are targeting autonomous remediation by the end of this year. Not just alerting—actual automated fix actions triggered by observability signals.

**Jordan**: That sounds terrifying. We're going to let AI agents make production changes based on telemetry?

**Alex**: It sounds terrifying because we're thinking about it wrong. The question isn't whether to automate—we've been automating operational responses for decades with runbooks and autoscalers. The question is whether AI agents can make better decisions faster than on-call humans at three AM.

**Jordan**: And you think the answer is yes?

**Alex**: For certain classes of problems, absolutely. Restart a crashed pod? Scale up during a traffic spike? Roll back a bad deployment that's causing errors? These are patterns where the decision logic is well-understood, just tedious to execute manually. Agents excel at tedious pattern matching.

**Jordan**: What about the harder problems? The ones that require understanding system behavior, not just pattern matching?

**Alex**: That's where the interesting evolution is happening. Honeycomb just announced what they call Honeycomb Intelligence—an AI-native observability suite that goes beyond simple automation. They're building an MCP server for IDE integration, so observability insights flow directly into your development environment.

**Jordan**: Wait, MCP as in the Model Context Protocol?

**Alex**: Exactly. The same protocol that powers Claude's tool use. Honeycomb is treating AI agents as first-class consumers of observability data. It's a fundamental shift in who—or what—is the primary user of your observability platform.

**Jordan**: Dynatrace made similar predictions—they're talking about agentic AI complexity as a new challenge. What do they mean by that?

**Alex**: It's a meta-problem. As AI agents become more prevalent in your systems—deploying code, responding to incidents, managing infrastructure—those agents themselves become sources of observability data. You need to observe your AI agents the same way you observe your services.

**Jordan**: So we're building observability for AI that's consuming observability to manage systems that generate observability. That's... recursive.

**Alex**: Welcome to 2026. Dynatrace also predicts that resilience will become the new benchmark, replacing pure availability. It's not enough that your system is up—it needs to demonstrate graceful degradation, fast recovery, and predictable behavior under failure.

**Jordan**: That ties into something Grafana's been saying about SLOs becoming a business conversation, not just an engineering metric.

**Alex**: This is crucial for platform engineers to understand. SLOs are no longer just internal targets—they're becoming the language that engineering uses to communicate with the business.

**Jordan**: Give me an example of what that looks like in practice.

**Alex**: Error budgets become budget conversations. Finance understands budgets—you have a certain amount to spend, and when it's gone, you make tradeoffs. Translate your SLO into business terms: "We have a four-hour error budget this month. Deploying this risky feature might burn two hours of it. Is the feature value worth that risk?"

**Jordan**: So platform engineers need to become translators.

**Alex**: Exactly. You're translating between telemetry signals and business impact. Building dashboards that executives can understand. Connecting SLOs to customer experience metrics. The platform engineer's value proposition is increasingly about that translation layer, not just the infrastructure underneath.

**Jordan**: Let me summarize where we are. OpenTelemetry won instrumentation. The battles now are insight extraction, cost optimization, and closing the action gap. AI agents are becoming both consumers and subjects of observability. And platform engineers are translators between technical signals and business outcomes.

**Alex**: That's the landscape. But here's what I'd tell someone starting a new observability strategy on Monday.

**Jordan**: Give me the Monday morning checklist.

**Alex**: Four things. First, audit your collector config—is it a cost control plane or just a passthrough? If every trace flows through unchanged, you're leaving money on the table.

**Jordan**: What should I be looking for specifically?

**Alex**: Check your sampling rates, your filtering rules, your routing logic. The collector should be making intelligent decisions about what goes where, not just forwarding everything downstream.

**Jordan**: Okay, what's second?

**Alex**: Measure your signal-to-noise ratio. What percentage of your telemetry actually leads to action? Most teams can't answer this question, but it's the most important metric for observability effectiveness. If ninety-nine percent of your alerts never result in human action, you have a signal-to-noise problem.

**Jordan**: How do you measure that?

**Alex**: Track alert-to-action rate. When an alert fires, does someone do something? If not, why not? Either the alert is noisy, the signal isn't actionable, or your on-call process is broken. Any of those is worth investigating.

**Jordan**: Third item?

**Alex**: Calculate cost per insight, not cost per gigabyte. Most observability cost discussions focus on data volume—how many spans, how many metrics, how much storage. But the real question is: what does it cost you to resolve an incident? If you're spending a hundred thousand a year on observability and resolving fifty production incidents, your cost per insight is two thousand dollars.

**Jordan**: Is that good or bad?

**Alex**: Depends on the incident severity. If those are P1 outages affecting revenue, two thousand dollars is cheap. If they're minor issues that would self-heal anyway, you might be over-investing. The point is to have the conversation in terms that connect to business value.

**Jordan**: And fourth?

**Alex**: Map your remediation path. What's the latency from dashboard to decision to action? If you see an anomaly on a dashboard, how long until a human understands the problem, decides on a fix, and implements it? That's your mean time to remediate, and it's often measured in hours. AI agents can compress that to minutes for well-understood problems.

**Jordan**: So the pitch for agent-first observability is reducing that time-to-action.

**Alex**: Exactly. The human review doesn't go away—it shifts. Humans approve the automation patterns. Humans investigate novel failures. Humans design the response playbooks. But the routine execution—the three AM restarts and rollbacks—that's where agents shine.

**Jordan**: There's an uncomfortable question here. Are we building observability platforms that might make our jobs obsolete?

**Alex**: I hear this concern a lot, and I think it misses the point. The job shifts, but it doesn't disappear. Today, platform engineers spend significant time responding to alerts—the toil of incident response. Tomorrow, platform engineers design the response systems. They architect the observability pipelines. They tune the agent behaviors. That's more interesting work, not less.

**Jordan**: So we become observability architects rather than observability operators.

**Alex**: That's the trajectory. And honestly, it's a better use of human cognitive capacity. Humans are good at understanding complex systems, designing resilient architectures, making nuanced tradeoffs. We're not particularly good at waking up at three AM to run the same restart command we've run a hundred times before.

**Jordan**: Let's bring this back to the central question. Can OpenTelemetry save observability in 2026?

**Alex**: It's already saved instrumentation. The fragmentation of vendor-specific agents and SDKs—that problem is largely solved. But instrumentation was the easy part. The 2026 battle is about what you build on top of OTel.

**Jordan**: And what should we build?

**Alex**: Analytics layers that match your scale. Cost optimization strategies that use the collector as a control plane. Agent integrations that close the action gap. And translation layers that connect technical signals to business outcomes. OTel is the foundation, but the building is still under construction.

**Jordan**: One million spans per episode. That stat from Netflix keeps echoing. That's not an observability problem—that's a data platform.

**Alex**: And that's the mindset shift 2026 requires. Observability at scale is data engineering. OTel gives you standardized data. What you do with it determines whether your observability investment pays off.

**Jordan**: If this helped you think about your observability strategy, subscribing helps us know to make more content like this.

**Alex**: The question isn't whether to adopt OpenTelemetry. It's what you build on top of it. 2026 is the year we find out if the ecosystem can finally close the loop from collection to insight.
