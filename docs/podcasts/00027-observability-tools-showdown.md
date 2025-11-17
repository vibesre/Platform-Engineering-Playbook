---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #027: Observability Tools Showdown"
slug: 00027-observability-tools-showdown
---

# The Open Source Observability Showdown: When "Free" Costs $12K/Month

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 20 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

<div style={{maxWidth: '640px', margin: '1.5rem auto'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/LYDumT3xmrM"
      title="The Open Source Observability Showdown: When Free Costs $12K/Month"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

---

**Jordan**: Today we're diving into the open source observability showdown. Prometheus, Grafana, Loki, Tempo. Everyone says they're free, everyone says they avoid vendor lock-in. But here's what's wild. Datadog just posted over two billion dollars in revenue for twenty twenty-three. If Prometheus is the industry standard and it's free, where's all that money coming from?

**Alex**: And it's not just Datadog. I was looking at Shopify's engineering blog. They run a dedicated observability team just to manage their Prometheus federation. A whole team. For a "free" tool.

**Jordan**: Right, so something doesn't add up here. Either open source observability isn't actually free, or there's a massive operational cost that nobody talks about until you're already committed.

**Alex**: It's definitely the second one. And I think the problem is that the conventional wisdom is backwards. Everyone says "start with open source, only pay for a vendor if you can't scale it." But, that ignores this massive complexity curve that sneaks up on you.

**Jordan**: Okay, so let's break this down. We're talking about the full observability stack. Metrics, logs, and traces. What are the main players in the open source world?

**Alex**: So for metrics, it's Prometheus. That's the gold standard. For visualization, Grafana. For logs, you've got Loki competing with the heavier ELK stack or OpenSearch. For distributed tracing, Jaeger or Tempo. And then OpenTelemetry won the instrumentation war. It's vendor-neutral, everyone's adopted it.

**Jordan**: And on paper, that sounds great. You pick the best tool for each job, you wire them together, you're done.

**Alex**: Yeah, except there are three distinct tiers of complexity here, and most teams don't realize which tier they're in until they've already invested months of work. Tier one is single cluster Prometheus. That actually works beautifully. Tier two is multi-cluster federation, where complexity spikes hard. And tier three is multi-tenant at scale, which basically requires a dedicated observability team.

**Jordan**: Let's start with tier one then. When does the simple Prometheus setup actually work?

**Alex**: When you've got one Kubernetes cluster, maybe a hundred to five hundred services, and your team is comfortable with YAML and Go. Prometheus uses a pull-based model. It has service discovery built in. You configure it to scrape metrics from your endpoints, it stores them locally with about two weeks of retention typically, and you query with PromQL.

**Jordan**: And the pull-based model, how does that actually work under the hood?

**Alex**: So Prometheus discovers targets through Kubernetes service discovery, DNS, or static configs. Then it pulls metrics from each target on a schedule, usually every fifteen or thirty seconds. The target exposes metrics on an HTTP endpoint in a specific text format. Prometheus scrapes that endpoint, parses the metrics, and stores them in its time-series database. The key advantage is that Prometheus controls the scraping, so it can handle targets going down gracefully. It just marks them as unreachable and keeps trying.

**Jordan**: Versus push-based where the services send metrics and you lose data if the collector's down.

**Alex**: Exactly. And for a single cluster, this is genuinely elegant. You install Prometheus with a Helm chart, configure a few service monitors, maybe set up some alerts in Alertmanager, connect Grafana as a data source, and you're operational in a day or two.

**Jordan**: So what breaks it?

**Alex**: Multi-cluster. Long-term storage. And high cardinality. The moment you need to federate metrics across multiple clusters, you need something like Thanos, Cortex, or Mimir. Those add a whole layer of architectural complexity. You're suddenly dealing with object storage for long-term retention, usually S3 or compatible. You need sidecar containers or remote write configuration. You're managing a distributed query layer.

**Jordan**: And high cardinality, that's when you have too many unique label combinations?

**Alex**: Right. Prometheus stores metrics as time series identified by metric name plus labels. If you have a metric like HTTP requests with labels for endpoint, method, status code, user ID, you can explode into millions of unique series. Prometheus's storage engine doesn't handle that well. Performance tanks, memory usage spikes, queries time out.

**Jordan**: So that's where something like VictoriaMetrics comes in?

**Alex**: Yeah, VictoriaMetrics is this interesting wildcard. It's a drop-in replacement for Prometheus. Same query language, same scrape config format. But it's got much better compression. Organizations report forty to sixty percent storage reduction just by switching from Prometheus to VictoriaMetrics. And it handles high cardinality way better. It's a single binary, so operationally it's simpler than running Prometheus plus Thanos.

**Jordan**: What's the trade-off?

**Alex**: You lose some ecosystem tooling. Prometheus has this massive ecosystem. Every vendor supports it, every tool integrates with it. VictoriaMetrics is catching up, but there are still gaps. And you're betting on a smaller project. Prometheus is CNCF graduated with huge corporate backing. VictoriaMetrics is more of a scrappy underdog.

**Jordan**: Okay, so that's metrics. Let's talk logs. Why is this such a mess?

**Alex**: Because logging is fundamentally different from metrics. With metrics, you're aggregating numbers over time. With logs, you're searching for needles in haystacks. And the traditional solution was Elasticsearch, which is powerful but operationally heavy.

**Jordan**: JVM tuning, cluster management, all that.

**Alex**: Right. So Loki came along with this promise. "Like Prometheus but for logs." The idea is simple. Instead of indexing the entire log content like Elasticsearch does, Loki only indexes labels. The actual log lines are stored in cheap object storage. You query with LogQL, which looks like PromQL. And because you're not indexing everything, storage costs are way lower. Organizations report up to ten times cheaper storage costs than Elasticsearch or OpenSearch.

**Jordan**: But there's a catch.

**Alex**: There's always a catch. Loki works great if your logs are structured and you have good labels. If you're running Kubernetes and your logs have namespace, pod, container labels, Loki is excellent. But, if you need full-text search, Loki struggles. And query performance degrades with high volume. Benchmarks show significantly slower query times than OpenSearch for complex searches, especially those needle-in-haystack queries across large log volumes.

**Jordan**: So when do teams regret choosing Loki?

**Alex**: When debugging requires full-text search. Like you're trying to find a specific error message buried in millions of log lines, and you don't know which labels to filter on. Or when your logs are unstructured. Legacy apps that dump text without structured fields. Or when you need advanced analytics. OpenSearch has aggregation pipelines, machine learning features, all this power that Loki just doesn't have.

**Jordan**: So the design trade-off is Loki optimized for label-based filtering at the cost of full-text search performance.

**Alex**: Exactly. And that works if you control your logging format. If you're starting fresh with structured logging, Loki is a great choice. But if you're dealing with legacy systems or need powerful search, OpenSearch is still the better tool, even though it's heavier to operate.

**Jordan**: Let's hit tracing before we get into the integration nightmare. Jaeger versus Tempo.

**Alex**: So OpenTelemetry won the instrumentation war. Everyone agreed that instrumenting your code shouldn't lock you into a vendor. But the backend is still fragmented. Jaeger is the CNCF graduated project. It's proven at scale. Uber processes ten billion spans per day on Jaeger. But they had to build a custom storage backend using Cassandra and dedicate a team to it.

**Jordan**: Ten billion spans per day. That's insane.

**Alex**: And that highlights the core challenge with tracing. Sampling. If you trace every request, your storage costs explode. If you sample too aggressively, you miss the critical traces when something goes wrong. Getting sampling right is hard. Too low, you lose visibility. Too high, you're drowning in data.

**Jordan**: And Tempo is Grafana's answer?

**Alex**: Tempo is object storage native, just like Loki. It integrates with Prometheus and Loki to give you this single pane of glass in Grafana. You can jump from a metric spike to related logs to traces. That integration story is compelling.

**Jordan**: But it's still maturing compared to Jaeger.

**Alex**: Yeah, Jaeger's been in production at scale for years. Tempo's newer. And you still have the same sampling complexity, the same challenge of propagating trace context across all your services. That's not a backend problem, that's an instrumentation problem. Every service in your stack needs to understand trace context headers and forward them correctly.

**Jordan**: Okay, so we've got Prometheus for metrics, maybe VictoriaMetrics if you need better compression. Loki for logs if they're structured, OpenSearch if you need full-text search. Jaeger or Tempo for traces. And OpenTelemetry for instrumentation. In theory, you wire these together and you have a complete observability stack.

**Alex**: In theory.

**Jordan**: I'm sensing the integration tax is where this falls apart.

**Alex**: Completely. You're managing five or more different configuration systems. Prometheus has service discovery configs. Grafana has data source configs. Loki has tenant configs if you're doing multi-tenancy. Tempo has storage configs. OpenTelemetry Collector has pipeline configs. And they all have different formats, different conventions.

**Jordan**: And version compatibility?

**Alex**: That's the other nightmare. Grafana ten point X works with Prometheus two point X, Loki two point nine or later, Tempo two point X. If you're not careful with your Helm chart versions, things break in subtle ways. A dashboard that worked last month suddenly doesn't because you upgraded Grafana but not Loki.

**Jordan**: What about authentication and authorization across all these components?

**Alex**: That's another layer of complexity. If you want unified SSO, you need additional tooling. Each component has its own auth model. Grafana can handle auth for its UI, but Prometheus and Loki and Tempo all need separate configuration. And if you're running multi-tenant, you need to ensure tenant isolation across the entire stack.

**Jordan**: And alerting?

**Alex**: Do you use Prometheus Alertmanager, or Grafana's built-in alerting, or both? They overlap but aren't quite the same. Alertmanager is more mature for Prometheus-based alerts, but Grafana alerting can unify alerts from multiple data sources. Except then you have two systems to maintain.

**Jordan**: So how much time are teams actually spending on this integration work?

**Alex**: Recent observability surveys show teams spending significant time managing these tooling integrations. When you factor in configuration updates, version compatibility issues, authentication setup, and troubleshooting broken dashboards, it adds up fast. We're talking one to two days a week just keeping the observability stack running instead of shipping features.

**Jordan**: Okay, so let's cut through this. When does open source observability actually make sense, and when should you just pay for Datadog?

**Alex**: I think there are three clear tiers based on operational maturity. Tier one is startups or small teams. One to five engineers, one to three clusters. The sweet spot is Prometheus plus Grafana plus Loki. You can self-host on a single instance, or use managed options. Operational overhead is minimal, the team learning curve is manageable, costs are trivial.

**Jordan**: And the red flag at this tier?

**Alex**: If you're spending more than ten percent of your engineer time on observability ops, you're doing something wrong. At this scale, it should just work.

**Jordan**: Tier two?

**Alex**: Tier two is growth or mid-size companies. Five to twenty engineers, five to twenty clusters, you're starting to think about multi-tenancy. This is the critical decision point. Do you build a scalability layer like Thanos, Mimir, or Cortex? Or do you migrate to a commercial platform?

**Jordan**: And how do you make that call?

**Alex**: Build makes sense if you have at least one dedicated platform engineer who can own it, you have a centralized platform team, and you have high-cardinality use cases that would blow up commercial pricing. Like if you're tracking millions of unique time series, Datadog's pricing model would crush you.

**Jordan**: But buy makes sense if?

**Alex**: If engineering time is more valuable spent on product features. If you want a unified experience without the integration tax. If you need advanced features like application performance monitoring, continuous profiling, security monitoring. Commercial platforms have years of investment in those areas.

**Jordan**: What about a hybrid approach?

**Alex**: Grafana Cloud is interesting here. It's managed Prometheus, Loki, and Tempo, but it's still open source compatible. You get the operational simplicity of a managed service, but you're not locked into a proprietary platform. You can migrate back to self-hosted if needed.

**Jordan**: And tier three is enterprise scale?

**Alex**: Tier three is twenty plus engineers, fifty plus clusters, multi-region, compliance requirements. At this point, the reality is you either have a dedicated observability team of three to ten engineers, or you pay the commercial premium. There's no middle ground.

**Jordan**: And the examples are companies like Shopify, Uber, Cloudflare.

**Alex**: Right. But look at their team sizes. Shopify has a dedicated observability team. Uber built custom backends for Jaeger. These are companies where observability is a platform differentiator. They need data residency control, they have expertise to optimize at the margins, and they can afford the investment.

**Jordan**: So let's make this concrete. What's the actual cost comparison?

**Alex**: Okay, so single-cluster Prometheus requires about five hours per month of engineer time for maintenance, updates, troubleshooting. At a loaded cost of one fifty per hour, that's seven fifty to fifteen hundred dollars per month equivalent.

**Jordan**: And multi-cluster with Thanos?

**Alex**: That jumps to forty to eighty hours per month. Now you're at six to twelve thousand dollars per month in engineer time. Meanwhile, Datadog or New Relic might be fifteen to a hundred dollars per host per month, but zero ops overhead. The break-even point is usually twenty to thirty hosts for single cluster, but over a hundred hosts for multi-cluster before self-hosted wins on total cost.

**Jordan**: So the "free" option costs six to twelve K per month once you account for engineer time.

**Alex**: And that's assuming things go smoothly. If you hit a major incident and your observability stack is part of the problem, the cost spikes even higher.

**Jordan**: Alright, so what can listeners actually do with this information?

**Alex**: First, start simple. Prometheus plus Grafana on a single cluster. Resist the urge to add complexity until it actually hurts. I see teams over-architect from day one because they're planning for scale they might never reach.

**Jordan**: And measure the operational burden.

**Alex**: Yeah, track the hours you're spending on observability tooling every month. Calculate the loaded cost. That number needs to be visible when you're making build versus buy decisions. Most teams don't track it and then wonder why they're always behind on feature work.

**Jordan**: When should teams consider scaling up the self-hosted stack?

**Alex**: When you're adding Thanos, Cortex, or Mimir, assign dedicated ownership. Don't make it a side project for someone who's also responsible for CI/CD and Kubernetes upgrades. It needs focus. Or seriously consider Grafana Cloud as a middle ground. You keep the open source compatibility but offload the operational burden.

**Jordan**: What about VictoriaMetrics? When does that make sense?

**Alex**: If Prometheus storage costs are spiking, try VictoriaMetrics before jumping to a commercial platform. It's a smaller lift than migrating to Datadog, and you might solve the problem with better compression and high-cardinality handling. Think of it as the wildcard option when Prometheus is ninety percent of what you need but storage is killing you.

**Jordan**: And the hybrid strategy?

**Alex**: For a lot of teams, the right answer is open source for metrics because it's mature, and commercial for logs and traces because the operational burden is higher. Metrics with Prometheus are well understood. Logs and traces are where the integration tax really hurts, so paying for a vendor there might be the right trade-off.

**Jordan**: I think the key insight here is that open source observability isn't about avoiding costs. It's about choosing which costs you pay.

**Alex**: Exactly. You either pay a vendor, or you pay in engineer time. And the real question is which investment aligns with your team's maturity and priorities. If you're five engineers trying to ship a product, paying Datadog to handle observability makes sense. If you're fifty engineers and observability is a competitive advantage, building on open source makes sense.

**Jordan**: And the middle ground is where most teams screw this up.

**Alex**: Yeah, they underestimate the operational complexity. They see Prometheus is free, Grafana is free, Loki is free. They start building. And then six months later they realize two engineers are spending half their time keeping the stack running, and they can't justify the migration cost to a vendor.

**Jordan**: So know your tier, calculate the true cost, and scale deliberately.

**Alex**: And be honest about your operational maturity. The free tier, single cluster Prometheus, is genuinely great. The scale tier, federation and multi-tenancy and long-term storage, demands engineering capacity that most teams don't have. Open source observability delivers on the avoid vendor lock-in promise, but only if you can afford the operational investment.

**Jordan**: That's the throughline. Open source isn't about being free. It's about matching the architectural complexity to your operational maturity.
