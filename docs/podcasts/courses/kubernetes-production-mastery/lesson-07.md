---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 #07: Observability"
slug: /courses/kubernetes-production-mastery/lesson-07
---

# Lesson 7: Observability

## Kubernetes Production Mastery Course

<GitHubButtons />

<iframe width="560" height="315" src="https://www.youtube.com/embed/7ORlAvlLfs8" title="Lesson 7: Observability - Kubernetes Production Mastery" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

**Course**: [Kubernetes Production Mastery](/courses/kubernetes-production-mastery)
**Episode**: 7 of 10
**Duration**: ~18 minutes
**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

## Learning Objectives

By the end of this lesson, you'll be able to:
- Understand the three pillars of observability (metrics, logs, traces) and when to use each for debugging
- Deploy production-ready Prometheus with persistent storage, service discovery, and avoid high cardinality label mistakes
- Design actionable alerts using the four golden signals (latency, traffic, errors, saturation)

## Prerequisites

- [Lesson 1: Production Mindset](./lesson-01)
- [Lesson 2: Resource Management](./lesson-02)
- [Lesson 3: Security Foundations](./lesson-03)
- [Lesson 4: Health Checks & Probes](./lesson-04)
- [Lesson 5: Stateful Workloads](./lesson-05)
- [Lesson 6: Networking & Services](./lesson-06)

---

## Transcript

Welcome to Episode 7 of Kubernetes Production Mastery. Last episode, we mastered networking. Services, Ingress controllers, CNI plugins. You can route traffic anywhere. Your architecture is beautiful. But here's the question nobody asks until it's too late: is it actually working?

Your Ingress is routing ten thousand requests per minute. Great. How many are errors? What's the latency? When did the error rate spike from point one percent to five percent? You have no idea. You're flying blind.

Pod-to-pod networking across your service mesh looks healthy. But what's normal latency? Fifty milliseconds? Five hundred? When should you be concerned? Database connections maxed out at three AM last Tuesday. Which service caused it? When did it start? Without observability, these aren't questions you can answer. They're mysteries you debug for hours.

Today we're fixing that. By the end, you'll understand the three pillars of observability—metrics, logs, and traces. You'll deploy production-ready Prometheus with persistent storage and service discovery. You'll design actionable alerts using the four golden signals that prevent ninety percent of production surprises. And you'll know exactly when to use metrics versus logs versus traces for debugging.

### The Three Pillars of Observability

Think of production observability like an airplane cockpit. You don't fly with a single engine temperature gauge. That's monitoring, sure. But it's inadequate. You need comprehensive instrumentation. Altitude, airspeed, fuel level, heading, engine temperature, hydraulic pressure. Why? Because failures are multi-dimensional. Your CPU might be fine, but memory's leaking. Network looks healthy, but disk is full. Application responding, but requests timing out.

This is why we have three pillars of observability. Each answers different questions. Metrics are your vital signs—numbers over time. Request rate, error percentage, CPU usage, memory consumption. Metrics answer "what's happening right now?" and "what's the trend?" They're perfect for detection. Your dashboard shows error rate jumped from zero to five percent. Now you know there's a problem.

Logs are your security camera footage. Event records. Error messages, stack traces, audit trails, application behavior. Logs answer "what exactly happened at three forty-two AM?" They're perfect for diagnosis. Metrics told you errors spiked. Logs show you "connection timeout to backend-api service." Now you know which service.

Traces are GPS package tracking for requests. One user request touches five microservices—trace shows you the complete path and timing for each hop. Traces answer "where did this slow request spend its time?" They're perfect for distributed diagnosis. Logs showed backend-api timing out. Traces show backend-api spent twenty-nine seconds waiting for the database. Now you know the root cause.

### Decision Framework: When to Use Each Pillar

Here's the decision framework. When you're debugging, ask yourself: is there a problem? Use metrics for detection. What exactly went wrong? Use logs for diagnosis. Which service in a multi-service chain caused it? Use traces for distributed diagnosis. You need all three. Without all three, you're debugging with missing puzzle pieces.

Let me make this concrete. It's three forty-two AM. Your monitoring alerts: five hundred two errors spiking. You check metrics—error rate went from point one percent to five percent in two minutes. That's detection. You're awake. Now what? You check logs. Filter by timestamp, filter by status code five hundred two. Logs show "connection timeout to backend-api." That's diagnosis—you know which service. But backend-api is healthy. CPU fine, memory fine. Where's the bottleneck? You pull up traces. One trace shows frontend to API gateway—fifty milliseconds. API gateway to backend-api—one hundred milliseconds. Backend-api to database—twenty-eight thousand milliseconds. There's your problem. Database query taking twenty-eight seconds. Now you can fix it.

Remember Episode Four's troubleshooting workflow? Observability gives you the data to actually execute that workflow. Describe, logs, events—those commands now return useful information because you've instrumented your cluster properly.

### Production Prometheus Setup

Now let's talk about Prometheus. Here's the mistake I see constantly. Someone runs helm install prometheus. Works great in development. Deploy to production. Two weeks later, Prometheus pod restarts. All metrics gone. Why? No persistent storage. Or Prometheus crashes with out of memory errors. Why? No retention policy—metrics filled the disk. Or metrics exposed to the entire cluster with no authentication. Or you manually configure every scrape target and miss half your services.

Default Prometheus installations fail in production. Here's what's missing. First, persistent storage. Remember Episode Five? Prometheus needs the same treatment as databases. StatefulSet with a PersistentVolumeClaim. Five hundred gigabytes to one terabyte. Retention configured for fifteen to thirty days. When the pod restarts, metrics survive.

Second, service discovery. You shouldn't manually list scrape targets. That's unmaintainable. Use ServiceMonitors—custom resources that tell Prometheus what to scrape. Deploy a new service with the right labels? Prometheus automatically discovers it and starts collecting metrics. No manual intervention.

Third, security and resource limits. Prometheus shouldn't be accessible to every pod. And it needs memory limits—otherwise high cardinality labels cause out-of-memory kills.

### Prometheus Architecture

Here's the production architecture. Prometheus Server runs as a StatefulSet with a PVC. Retention policy set to thirty days. Alertmanager handles alert routing, grouping, and silencing. Grafana provides visualization, querying Prometheus with PromQL. And ServiceMonitors provide automatic target discovery.

For deployment, I recommend Prometheus Operator over plain Helm charts. Why? Operator gives you custom resources for declarative configuration. ServiceMonitors, PrometheusRules, Alertmanager config—all Kubernetes resources. Helm charts work, but you'll manually create ServiceMonitors and manage config maps. Operator is more Kubernetes-native.

Let me show you a real example. E-commerce platform. What does Prometheus scrape? Kube-state-metrics for cluster state—pod status, deployment health, node conditions. Node-exporter for host metrics—CPU, memory, disk I/O on every node. Your Ingress controller for HTTP metrics—request rates, latencies, status codes. And your application pods for custom business metrics like cart abandonment rate or checkout completion time.

### The Four Golden Signals

Now here's what matters most—the four golden signals. This framework comes from Google's SRE book. These four metrics cover ninety percent of production issues. Everything else is noise. The signals are latency, traffic, errors, and saturation.

Latency is how long requests take. Not just average—you need percentiles. P fifty, p ninety-five, p ninety-nine. Why percentiles? Average latency might be one hundred milliseconds, but p ninety-nine is five seconds. That means one percent of users wait five seconds. Unacceptable. You need to know.

Traffic is requests per second or bandwidth. Are you handling ten requests per second or ten thousand? This tells you load and helps identify capacity issues.

Errors are request failure rates. Four hundreds, five hundreds, timeouts. Your error rate should be below one percent. Above that, users notice.

Saturation is how full your system is. CPU usage, memory usage, disk usage, database connection pool utilization. Saturation at ninety percent means you're close to capacity. Time to scale or optimize.

These four signals apply to every service. Monitor them, alert on them, and you'll catch problems before customers complain. Let me show you the PromQL queries. For latency, you use histogram quantile function. This calculates the ninety-fifth percentile from Prometheus histogram metrics. For traffic, you use rate of total requests over five minutes. For errors, you calculate error rate as five hundreds divided by total requests. For saturation, you compare current usage to limits—memory usage divided by memory limit.

Remember Episode Six's networking? These queries monitor your Ingress endpoints, your Services, pod-to-pod latency. The infrastructure you built last episode now has visibility.

### Avoiding High Cardinality Labels

Here's where people mess up Prometheus—high cardinality labels. Cardinality is the number of unique combinations of label values. Low cardinality example: you have ten services and three environments. That's thirty combinations. Totally fine. High cardinality example: you add user ID as a label. Now you have millions of combinations because every user gets a separate time series. Prometheus runs out of memory.

Best practice for labels: use them for dimensions with low cardinality. Service name, environment, instance, job. These have limited unique values and high diagnostic value. Don't use labels for identifiers with high cardinality. User ID, request ID, email address, session ID. If a label has more than one hundred unique values, reconsider it. If it has more than ten thousand, it's definitely wrong.

The rule: labels are for aggregation dimensions, not identifiers. You want to aggregate by service or environment. You don't aggregate by user ID—that's a filter in logs, not a metric label.

### Long-Term Storage

One more thing on Prometheus—storage costs. Production pattern is short-term metrics in Prometheus and long-term metrics in Thanos or Cortex. Fifteen to thirty days at full resolution in Prometheus. One year or more in Thanos with downsampling. Why? One terabyte of retention times three replicas equals three terabytes of storage. That gets expensive. Thanos uses object storage like S3—much cheaper for long-term retention.

### Log Aggregation: Loki vs ELK

Now let's talk logging. Without log aggregation, you're in trouble. Fifty services times five pods each equals two hundred fifty log sources. Pod restarts mean logs disappear. Debugging requires SSH to twenty different pods, grep through logs, and pray you find the error before it rotates out.

Centralized log aggregation fixes this. All logs flow to a single queryable system. Logs persist beyond pod lifetimes. You can correlate logs across services using request IDs. Filter by timestamp, service, error level—all in one interface.

The choice is Loki versus ELK stack. Here's my decision framework. Loki is Grafana's log aggregation system. It's lightweight and low cost because it only indexes labels, not log content. It integrates perfectly with Prometheus and Grafana—same query interface, same dashboards. And it's great for Kubernetes because you can tail logs just like kubectl logs. The downside is limited full-text search. You can't do complex Elasticsearch-style queries.

Loki is best for teams already using Prometheus and Grafana, and for cost-conscious organizations. You'll save on infrastructure because Loki doesn't need massive Elasticsearch clusters.

ELK stack is Elasticsearch, Logstash, and Kibana. The benefits are powerful full-text search, complex queries, and advanced analytics with custom dashboards. The downsides are resource-heavy—Elasticsearch needs four gigabytes of memory minimum per node—and higher cost because it indexes everything, not just labels.

ELK is best for large teams with dedicated log analysis staff, compliance requirements for detailed log retention, or when you need advanced search capabilities.

My recommendation? Start with Loki. It's simpler and cheaper. Migrate to ELK later if you hit limits on search capability or need compliance features. Most teams never need ELK's complexity.

### Structured Logging

One critical practice—structured logging. Unstructured logs look like this: "Two zero two five dash zero one dash twelve fourteen thirty-two ten ERROR User login failed for john at example dot com from IP two zero three dot zero dot one one three dot five." You can read it. But querying is painful. How do you find all login failures from a specific IP range? You write complex regex and hope it works.

Structured logs are JSON. Same information, but queryable. You have timestamp, level error, event login failed, user john at example dot com, IP address as separate fields. Now you query with Loki: show me all events where event equals login failed and IP matches this range. Simple, fast, accurate.

Best practice: applications log JSON, Fluent Bit parses and forwards to Loki or Elasticsearch, Grafana or Kibana for querying.

### Log Retention Costs

The cost trap with logging is retention. Logging everything at debug level generates ten terabytes per month. Seven-day retention is manageable. Ninety-day retention costs a fortune. Production pattern: info level for general logs, error and warn always logged, debug only during active troubleshooting. Seven-day retention for general logs, thirty to ninety days for audit logs if compliance requires it, and archive to S3 or Google Cloud Storage for long-term retention. Object storage is cheap and you can search it if needed.

### Alerting Best Practices

Now alerting. This is where most teams fail. Bad alerting looks like this: alert on every single error. You get one hundred alerts per day. Alert fatigue sets in. You ignore them. Alert on symptoms without context—disk usage seventy percent, so what? Is it growing? Will it fill? No grouping—twenty pods crash, you get twenty separate alerts instead of one.

Good alerting focuses on customer impact. Alert when error rate exceeds one percent or latency p ninety-five exceeds five hundred milliseconds. Alert on imminent failure—disk at ninety percent and will fill in two hours based on growth rate. Group related alerts—all pods in a deployment down equals one alert, not twenty.

Let me show you real alert rules. High latency alert: p ninety-five latency exceeds five hundred milliseconds for five minutes. High error rate alert: five hundred errors divided by total requests exceeds one percent for five minutes. High memory alert: pod using more than ninety percent of memory limit for ten minutes.

Notice the pattern? Alerts trigger on rate of change plus duration threshold. This avoids alerting on transient spikes. A single slow request doesn't page you. Five minutes of slow requests does.

### Alertmanager Routing

Alertmanager handles smart routing. Critical alerts—error rate above five percent—go to PagerDuty and wake up on-call. Warning alerts—disk eighty percent—go to Slack for business hours review. Info alerts—deployment completed—just log them. Grouping is key. Twenty pods crash? One alert: "Deployment X unhealthy." Not twenty separate alerts. And silencing for planned maintenance. Deploying a fix? Silence alerts for two hours so you're not paged during the rollout.

Remember Episode Four's troubleshooting workflow? Alerts tell you what failed. Metrics and logs tell you why. This is the complete picture.

### Distributed Tracing

One more pillar—distributed tracing. Here's when you need it. User reports checkout is slow. That request touches six services: frontend, API gateway, cart service, inventory service, payment service, order service. Metrics show all services healthy. CPU fine, memory fine, error rate low. Which service is slow?

This is where tracing saves you. Your application code generates spans—timing information for each service call. A collector aggregates spans from all services. Storage like Jaeger or Tempo stores the trace data. The UI visualizes the complete request flow.

Example trace shows checkout request took two point three seconds total. API gateway took fifty milliseconds. Cart service one hundred milliseconds. Inventory eighty milliseconds. Payment service nineteen hundred milliseconds. Order service one hundred seventy milliseconds. There's your problem. Payment service is slow. Now you check payment service metrics and logs for the root cause.

You need tracing if you have ten or more microservices, complex request flows you can't easily follow, or latency issues you can't diagnose with metrics alone. You don't need tracing for monoliths or fewer than five services, simple architectures where you can follow request paths easily, or when metrics and logs are sufficient.

### Trace Sampling

Sampling strategy matters. Don't trace every request—cost and performance overhead aren't worth it. Sample one percent of successful requests for trend visibility. Sample one hundred percent of errors for debugging. This gives you enough data without killing performance.

Callback to Episode Six: if you implemented a service mesh like Istio, tracing is already enabled. Istio automatically generates spans for every request through the mesh.

### Common Observability Mistakes

Let me walk through common mistakes. Mistake one: no Prometheus retention policy. Metrics fill disk, Prometheus crashes, you lose all data. Fix: set retention to thirty days and storage size in your StatefulSet PVC. The flags are storage dot tsdb dot retention dot time equals thirty d and storage dot tsdb dot retention dot size equals four fifty GB.

Mistake two: high cardinality labels. Prometheus runs out of memory, queries are slow, scraping fails. Example: adding user ID as a label creates millions of time series. Fix: use labels for dimensions like service and environment, not identifiers like user or request.

Mistake three: logging everything at debug level. Log storage costs explode to ten terabytes per month, queries are slow. Fix: info level in production, error and warn always, debug only during troubleshooting.

Mistake four: no alerting or too many alerts. You either miss critical issues or ignore all alerts because of fatigue. Fix: alert on customer impact using golden signals, group related alerts, route by severity.

Mistake five: tracing at one hundred percent sampling. Performance overhead, storage costs, no benefit over one percent sampling for trends. Fix: one percent sampling for successful requests, one hundred percent for errors.

### Active Recall Quiz

Let's pause for active recall. Answer these questions. First, what are the four golden signals and why do they matter? Second, you're debugging a slow checkout flow in a microservice architecture—which observability pillar would you use first and why? Third, your Prometheus is running out of memory—what are the two most likely causes?

**Answers:**

The four golden signals are latency, traffic, errors, and saturation. They matter because they cover ninety percent of production issues. If these four look healthy, your system is probably fine. Everything else is noise.

For debugging slow checkout in microservices, start with traces. Traces show you which service in the chain is slow. Then check that service's metrics for latency and errors. Then check logs for specific error messages. Traces give you the where, metrics give you how bad, logs give you why.

For Prometheus out of memory, two causes. High cardinality labels creating too many unique time series. Or no retention policy, storing too much data. Check label design and set retention limits.

### Key Takeaways

Let's recap. Three pillars of observability: metrics for trends, logs for details, traces for request flows. You need all three. Prometheus production setup requires StatefulSet with PVC, retention policy, ServiceMonitors for automatic discovery, and avoiding high cardinality labels. The four golden signals are latency, traffic, errors, saturation. Alert on these, not everything else. For logging, choose Loki for cost and simplicity, ELK for power and compliance. For tracing, implement it only for complex microservices with ten or more services. Sample smartly—one percent success, one hundred percent errors.

This connects to previous episodes. Episode Four's troubleshooting workflow now has data sources—metrics, logs, and traces. Episode Five's StatefulSets apply to Prometheus storage—it needs PVCs and stable identity just like databases. Episode Six's networking—Services and Ingress—are your monitoring targets. ServiceMonitors discover them automatically.

You can now build production infrastructure, secure it, persist state, route traffic, and see what's happening in production. Next episode, we tackle cost optimization. You've built production-ready systems. But what's it costing? The five sources of Kubernetes cost waste. Right-sizing strategies using FinOps principles. Tools like Kubecost. And the senior engineer problem—over-engineering costs money. We'll use today's Prometheus metrics to monitor resource utilization and Episode Two's resource concepts to right-size workloads. See you then.

---

## Navigation

⬅️ **Previous**: [Lesson 6: Networking & Services](./lesson-06) | **Next**: [Lesson 8: CI/CD Integration](./lesson-08) ➡️

📚 **[Back to Course Overview](/courses/kubernetes-production-mastery)**
