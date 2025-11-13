# Lesson Outline: Episode 7 - Observability: Metrics, Logging, Tracing

## Metadata
- **Course**: Kubernetes Production Mastery
- **Episode**: 7 of 10
- **Duration**: 15 minutes
- **Type**: Core Concept
- **Prerequisites**:
  - Episode 1 (Production Mindset - monitoring checklist item)
  - Episode 4 (Troubleshooting - systematic debugging)
  - Episode 5 (StatefulSets - Prometheus storage)
  - Episode 6 (Networking - monitoring targets)
- **Template**: Core Concept (Episodes 3-N-2)

## Learning Objectives
By end of lesson, learners will:
1. Deploy Prometheus with persistent storage and configure service discovery for automatic target detection
2. Design actionable alerts using the four golden signals (latency, traffic, errors, saturation) to prevent alert fatigue
3. Determine when to use metrics vs logs vs traces for specific debugging scenarios

Success criteria:
- Can explain why default Prometheus install fails in production and what's needed
- Can write PromQL queries for the four golden signals
- Can choose between Loki and ELK based on requirements and cost
- Can design a distributed tracing strategy with appropriate sampling rates

## Spaced Repetition Plan
**Introduced** (repeat later):
- Four golden signals → Episode 8 (cost optimization metrics), Episode 10 (multi-cluster observability)
- Prometheus architecture → Episode 8 (monitoring cost metrics), Episode 10 (federation)
- PromQL basics → Episode 8 (resource utilization queries), Episode 10 (cross-cluster queries)
- Log aggregation patterns → Episode 10 (centralized logging at scale)

**Reinforced** (from earlier):
- Production readiness checklist from Episode 1 (item #5: monitoring) → Applied in Prometheus setup section
- StatefulSets from Episode 5 → Applied to Prometheus persistent storage (needs PVC, stable identity)
- Services/Ingress from Episode 6 → Monitoring targets (ServiceMonitors, endpoint scraping)
- Troubleshooting workflow from Episode 4 → Enhanced with observability tools

## Lesson Flow

### 1. Recall & Connection (1.5 min)
**Callback to Episode 6**: "Last episode: networking - Services, Ingress, CNI. You can now route traffic. But here's the question: is it working? What's the latency? Are requests failing? Without observability, you're flying blind."

**The Production Blindness Problem**:
- Your Ingress is routing 10,000 requests/minute - but how many are errors?
- Pod-to-pod latency across your service mesh - what's normal vs concerning?
- Database connections maxed out - when did it start? Which service?

**Today's Preview**: "Three pillars of observability. Metrics for trends. Logs for details. Traces for flows. Plus the four golden signals that prevent 90% of production surprises."

### 2. Learning Objectives (30 sec)
By the end, you'll:
- Deploy production-ready Prometheus with persistent storage and service discovery
- Design actionable alerts using golden signals to avoid alert fatigue
- Choose metrics vs logs vs traces for specific debugging scenarios

### 3. The Observability Mental Model (3 min)
**Analogy**: Airplane cockpit instruments
- **Not this**: Single engine temperature gauge (you're monitoring, but inadequately)
- **This**: Comprehensive dashboard - altitude, speed, fuel, heading, engine temp, hydraulics
- Why? Because production failures are multi-dimensional. CPU might be fine, but memory leaking. Network healthy, but disk full.

**Three Pillars Explained**:
1. **Metrics** (vital signs): Numbers over time. Request rate, error percentage, CPU usage, memory. Answers "What's happening now? What's the trend?"
2. **Logs** (security camera footage): Event records. Error messages, stack traces, audit trails. Answers "What exactly happened at 3:42 AM?"
3. **Traces** (GPS package tracking): Request flow across services. One user request touches 5 microservices - trace shows the path and timing. Answers "Where did this slow request spend its time?"

**When to Use Each** (decision framework):
- Metrics: "Is there a problem?" (detection)
- Logs: "What exactly went wrong?" (diagnosis)
- Traces: "Which service in the chain caused it?" (distributed diagnosis)

**Visual**: Imagine debugging a 502 error.
- Metrics tell you error rate spiked at 3:42 AM (detection)
- Logs show "connection timeout to backend-api" (which service)
- Traces show backend-api spent 29 seconds waiting for database (root cause)

**Why This Matters**: Without all three, you're debugging with missing puzzle pieces. Episode 4's troubleshooting workflow? Observability gives you the data to actually execute it.

### 4. Prometheus: Production-Ready Metrics (7 min)

#### 4.1 Why Default Install Fails (1 min)
**The Mistake**: `helm install prometheus` → works in dev, fails in production

**What's Missing**:
1. No persistent storage - pod restart = lose all metrics
2. No retention policy - fills disk in 2 weeks
3. No security - metrics exposed to cluster
4. No service discovery - manual target configuration

**Callback to Episode 5**: Remember StatefulSets? Prometheus needs persistent storage just like databases. PVC for data, stable identity for federation.

#### 4.2 Production Prometheus Architecture (2 min)
**Setup Pattern**:
- **Prometheus Server**: StatefulSet with PVC (500GB-1TB), retention 15-30 days
- **Service Discovery**: ServiceMonitors (CRDs that tell Prometheus what to scrape)
- **Alertmanager**: Handles alert routing, grouping, silencing
- **Grafana**: Visualization (queries Prometheus via PromQL)

**Deployment Choice**:
- Prometheus Operator (recommended): CRDs for declarative config, automatic target discovery
- Helm chart: Simpler, less features, manual ServiceMonitor creation

**Example**: E-commerce platform
```
Prometheus scrapes:
- kube-state-metrics (pod/deployment/node states)
- node-exporter (host metrics: CPU, memory, disk)
- Ingress controller (request rates, latencies)
- Application pods (custom metrics: cart abandonment rate)
```

#### 4.3 The Four Golden Signals (2 min)
**Framework** (from Google SRE book):
1. **Latency**: How long requests take (p50, p95, p99)
2. **Traffic**: Requests per second, bandwidth
3. **Errors**: Request failure rate (4xx, 5xx)
4. **Saturation**: How full your system is (CPU, memory, disk, connections)

**Why These Four**: Cover 90% of production issues. Everything else is noise.

**PromQL Examples**:
```promql
# Latency (p95)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Traffic
rate(http_requests_total[5m])

# Errors
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# Saturation
container_memory_usage_bytes / container_spec_memory_limit_bytes
```

**Callback to Episode 6**: These queries monitor your Ingress endpoints, Services, pod-to-pod latency. The networking you built last episode.

#### 4.4 Label Design & Cardinality Trap (1.5 min)
**The Problem**: High cardinality kills Prometheus

**What is Cardinality**: Unique combinations of label values
- Low: `{service="api", environment="prod"}` → 10 services × 3 envs = 30 combinations
- High: `{user_id="12345", request_id="abc-def-ghi"}` → millions of combinations

**The Trap**: Adding `user_id` as label = Prometheus runs out of memory. Why? Every unique combo = separate time series.

**Best Practice**:
- ✅ Labels: service, environment, instance, job (low cardinality, high value)
- ❌ Labels: user_id, request_id, email, session_id (high cardinality, kills performance)

**Rule**: If a label has >100 unique values, reconsider. If >10,000, definitely wrong.

#### 4.5 Retention & Storage Costs (0.5 min)
**Production Pattern**:
- Short-term: 15-30 days in Prometheus (recent, high resolution)
- Long-term: 1+ years in Thanos/Cortex (downsampled, cheap storage)

**Cost Awareness**: 1TB retention × 3 replicas = 3TB storage. Plan accordingly.

### 5. Logging: Aggregation & Cost Management (4 min)

#### 5.1 Why Log Aggregation Matters (1 min)
**The Problem Without It**:
- 50 services × 5 pods each = 250 log sources
- Pod restarts = logs gone
- Debugging: SSH to 20 pods, grep, pray

**The Solution**: Centralized log aggregation
- All logs → single query interface
- Persistent storage (logs survive pod restarts)
- Correlation (filter by request ID across services)

#### 5.2 Loki vs ELK Decision (1.5 min)
**Loki** (Grafana's log system):
- ✅ Lightweight, low cost (indexes labels, not content)
- ✅ Integrates with Prometheus/Grafana
- ✅ Good for Kubernetes (tail logs like kubectl)
- ❌ Limited full-text search (no Elasticsearch query power)
- **Best for**: Teams already using Prometheus/Grafana, cost-conscious

**ELK Stack** (Elasticsearch, Logstash, Kibana):
- ✅ Powerful full-text search, complex queries
- ✅ Advanced analytics, dashboards
- ❌ Resource-heavy (Elasticsearch needs 4GB+ memory)
- ❌ Higher cost (indexes everything)
- **Best for**: Large teams, compliance requirements, advanced log analysis

**My Decision Framework**:
- Start with Loki (simpler, cheaper)
- Migrate to ELK if you need: advanced search, compliance, dedicated log analytics team

#### 5.3 Structured Logging (1 min)
**Unstructured** (bad):
```
2025-01-12 14:32:10 ERROR User login failed for john@example.com from IP 203.0.113.5
```
Hard to query: "Show me all login failures from this IP range"

**Structured** (good):
```json
{"timestamp":"2025-01-12T14:32:10Z","level":"ERROR","event":"login_failed","user":"john@example.com","ip":"203.0.113.5"}
```
Easy to query: `{event="login_failed", ip=~"203.0.113.*"}`

**Best Practice**: JSON logging from application, parsed by Fluent Bit, stored in Loki/ELK.

#### 5.4 Log Retention & Cost (0.5 min)
**The Cost Explosion**:
- Logging everything at DEBUG level = 10TB/month
- 7-day retention = manageable
- 90-day retention = massive cost

**Production Pattern**:
- INFO level in production (ERROR/WARN always)
- 7-day retention for general logs
- 30-90 days for audit logs (compliance)
- Archive to S3/GCS for long-term (cheap, searchable if needed)

### 6. Alerting: Actionable, Not Noisy (3 min)

#### 6.1 The Alert Fatigue Problem (1 min)
**Bad Alerting** (what NOT to do):
- Alert on every error (100 alerts/day, ignored)
- Alert on symptoms not causes ("disk usage 70%" - so what?)
- No grouping (same issue = 50 separate alerts)

**Good Alerting**:
- Alert on customer impact (error rate >1%, latency p95 >500ms)
- Alert on imminent failure (disk 90%, will fill in 2 hours)
- Group related alerts (all pods down = one alert, not 20)

#### 6.2 Golden Signals Alerts (1 min)
**Latency Alert**:
```yaml
alert: HighLatency
expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
for: 5m
annotations:
  summary: "API latency p95 > 500ms for 5 minutes"
```

**Error Rate Alert**:
```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.01
for: 5m
annotations:
  summary: "Error rate > 1% for 5 minutes"
```

**Saturation Alert**:
```yaml
alert: HighMemoryUsage
expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
for: 10m
annotations:
  summary: "Pod using > 90% memory for 10 minutes"
```

**Pattern**: Alert on rate of change + duration threshold (avoids transient spikes)

#### 6.3 Alertmanager Routing (1 min)
**Smart Routing**:
- Critical alerts (error rate >5%) → PagerDuty → wake up on-call
- Warning alerts (disk 80%) → Slack → check during business hours
- Info alerts (deployment completed) → Log only

**Grouping**:
- 20 pods crash → one alert "Deployment X unhealthy", not 20 separate

**Silencing**:
- Planned maintenance? Silence alerts for 2 hours
- Known issue? Silence until fix deployed

**Callback to Episode 4**: Troubleshooting workflow enhanced. Alerts tell you WHAT failed. Metrics/logs tell you WHY.

### 7. Distributed Tracing: When You Need It (1.5 min)

#### 7.1 The Microservice Debugging Problem (0.5 min)
**Scenario**: User reports "checkout is slow"
- Request touches: frontend → API gateway → cart service → inventory service → payment service → order service
- Which service is slow? Metrics show all services "healthy"
- This is where tracing saves you

#### 7.2 Tracing Architecture (0.5 min)
**Components**:
- **Instrumentation**: Application code generates spans (timing for each service call)
- **Collector**: Aggregates spans from all services
- **Storage**: Jaeger, Tempo (stores trace data)
- **UI**: Visualize request flow

**Example Trace**:
```
Checkout request (2.3s total):
├─ API Gateway (50ms)
├─ Cart Service (100ms)
├─ Inventory Service (80ms)
├─ Payment Service (1900ms) ← THE PROBLEM
└─ Order Service (170ms)
```

**Decision**: Payment service slow. Check payment service logs/metrics for root cause.

#### 7.3 When to Implement Tracing (0.5 min)
**You Need Tracing If**:
- 10+ microservices
- Complex request flows (can't easily follow the path)
- Latency issues you can't diagnose with metrics alone

**You DON'T Need Tracing If**:
- Monolith or under 5 services
- Simple architectures (can follow request path easily)
- Metrics + logs sufficient

**Sampling Strategy**:
- Don't trace every request (cost/performance)
- Sample 1% of successful requests (trend visibility)
- Sample 100% of errors (debug issues)

**Callback to Episode 6**: Service mesh (Istio) includes tracing automatically. If you implemented service mesh, tracing is already enabled.

### 8. Common Pitfalls (1.5 min)

**Mistake 1**: No Prometheus retention policy
- **What happens**: Metrics fill disk, Prometheus crashes, lose all data
- **Fix**: Set retention (15-30 days) and storage size in StatefulSet PVC
- **Command**: `--storage.tsdb.retention.time=30d --storage.tsdb.retention.size=450GB`

**Mistake 2**: High cardinality labels
- **What happens**: Prometheus OOM, slow queries, can't scrape targets
- **Example**: Adding `user_id` as label → millions of time series
- **Fix**: Use labels for dimensions (service, env), not identifiers (user, request)

**Mistake 3**: Logging everything at DEBUG level
- **What happens**: Log storage costs explode (10TB/month), slow queries
- **Fix**: INFO level in production, ERROR/WARN always, DEBUG only during troubleshooting

**Mistake 4**: No alerting or too many alerts
- **What happens**: Miss critical issues OR ignore all alerts (fatigue)
- **Fix**: Alert on customer impact (golden signals), group related alerts, route by severity

**Mistake 5**: Tracing at 100% sampling rate
- **What happens**: Performance overhead, storage costs, no benefit vs 1% sampling for trends
- **Fix**: 1% sampling for successful requests, 100% for errors

### 9. Active Recall (1.5 min)
"Pause and answer these questions:"

**Question 1**: What are the four golden signals, and why do they matter?
[PAUSE 5 sec]

**Question 2**: You're debugging a slow checkout flow in a microservice architecture. Which observability pillar would you use first, and why?
[PAUSE 5 sec]

**Question 3**: Your Prometheus is running out of memory. What are the two most likely causes?
[PAUSE 5 sec]

**Answers**:
1. **Four golden signals**: Latency (how long), Traffic (how much), Errors (failure rate), Saturation (how full). They cover 90% of production issues - if these look healthy, your system is probably fine.

2. **Slow checkout debugging**: Start with **traces** (see which service in the chain is slow), then **metrics** (check that service's latency/errors), then **logs** (find specific error messages). Traces give you the "where", metrics give you "how bad", logs give you "why".

3. **Prometheus OOM**: (1) High cardinality labels - too many unique time series, or (2) No retention policy - storing too much data. Check label design and set retention limits.

### 10. Recap & Integration (1.5 min)

**Takeaways**:
1. **Three pillars**: Metrics (trends), Logs (details), Traces (flows) - you need all three
2. **Prometheus production setup**: StatefulSet with PVC, retention policy, ServiceMonitors for discovery, avoid high cardinality
3. **Four golden signals**: Latency, Traffic, Errors, Saturation - alert on these, not everything
4. **Logging choice**: Loki for cost/simplicity, ELK for power/compliance
5. **Tracing**: Only for complex microservices (10+), sample smartly (1% success, 100% errors)

**Connection to Previous Episodes**:
- Episode 4's troubleshooting workflow now has data sources (metrics/logs/traces)
- Episode 5's StatefulSets apply to Prometheus storage (PVC, stable identity)
- Episode 6's networking (Services, Ingress) are your monitoring targets

**Bigger Picture**:
You can now build (Episodes 2-3), secure (Episode 3), persist (Episode 5), route traffic (Episode 6), AND see what's happening in production (Episode 7). Next: optimize the cost.

**Callback Preview**: Episode 1's production readiness checklist item #5 was monitoring. Today you learned how to implement it properly.

### 11. Next Episode Preview (30 sec)
"Next episode: Cost Optimization at Scale. You've built production-ready infrastructure. But what's it costing? The five sources of Kubernetes cost waste. Right-sizing strategies. FinOps tools like Kubecost. And the senior engineer problem - over-engineering costs money. We'll use Episode 7's Prometheus to monitor resource utilization and Episode 2's resource concepts to right-size workloads. See you then."

---

## Supporting Materials

**Code Examples**:
1. **Prometheus StatefulSet manifest** - shows PVC, retention, resources
2. **ServiceMonitor CRD** - automatic target discovery
3. **PromQL queries** - four golden signals implementation
4. **Alert rules** - latency/errors/saturation with proper thresholds
5. **Loki stack deployment** - Fluent Bit → Loki → Grafana

**Tech References**:
- prometheus.io/docs - official architecture docs
- grafana.com/docs/loki - Loki setup guide
- sre.google/sre-book - original four golden signals chapter
- prometheus.io/docs/prometheus/latest/querying/basics - PromQL tutorial

**Analogies**:
1. **Cockpit instruments** - comprehensive dashboard vs single gauge
2. **Vital signs** - metrics like pulse/blood pressure/temperature
3. **Security camera** - logs as event footage
4. **GPS package tracking** - traces showing request journey
5. **Alert fatigue** - like car alarm that goes off constantly (ignored)

---

## Quality Checklist

**Structure**:
- [x] Clear beginning/middle/end (recall → teach → practice → recap)
- [x] Logical flow (mental model → Prometheus → logging → alerting → tracing)
- [x] Time allocations realistic (15 min total: 1.5+7+4+3+1.5+1.5+1.5 = ~20 min allocated, will tighten in script)
- [x] All sections specific with concrete examples

**Pedagogy**:
- [x] Objectives specific/measurable (deploy Prometheus with storage, design alerts using golden signals, choose observability pillar)
- [x] Spaced repetition integrated (callbacks to Episodes 1,4,5,6; forward to Episodes 8,10)
- [x] Active recall included (3 retrieval questions with pauses)
- [x] Signposting clear (section transitions, "first/second/third")
- [x] 5 analogies (cockpit, vital signs, camera, GPS, car alarm)
- [x] Pitfalls addressed (5 common mistakes with fixes)

**Content**:
- [x] Addresses pain points (production blindness, alert fatigue, high cardinality, cost explosion)
- [x] Production-relevant examples (e-commerce platform, 502 debugging, checkout tracing)
- [x] Decision frameworks (metrics vs logs vs traces, Loki vs ELK, when to trace, sampling strategy)
- [x] Troubleshooting included (debugging with observability tools)
- [x] Appropriate depth for senior engineers (PromQL, cardinality, retention policies)

**Engagement**:
- [x] Strong hook (flying blind, can't answer basic questions about production)
- [x] Practice/pause moments (active recall with 5-sec pauses)
- [x] Variety in techniques (analogies, examples, think-alouds, decision frameworks)
- [x] Preview builds anticipation (cost optimization using observability data)
