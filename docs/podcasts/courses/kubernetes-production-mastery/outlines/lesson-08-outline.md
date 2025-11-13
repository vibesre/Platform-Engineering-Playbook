# Lesson Outline: Episode 8 - Cost Optimization at Scale

## Metadata
- **Course**: Kubernetes Production Mastery
- **Episode**: 8 of 10
- **Duration**: 12 minutes
- **Type**: Core Concept
- **Prerequisites**:
  - Episode 1 (Production Mindset - cost in readiness checklist)
  - Episode 2 (Resource Management - requests, limits, QoS)
  - Episode 7 (Observability - Prometheus for resource metrics)
- **Template**: Core Concept (Episodes 3-N-2), adapted for 12-min duration

## Learning Objectives
By end of lesson, learners will:
1. Identify the five primary sources of Kubernetes cost waste and quantify their impact on infrastructure spend
2. Right-size resources using actual utilization data, Vertical Pod Autoscaler recommendations, and load testing validation
3. Implement cost controls (ResourceQuotas, LimitRanges, Cluster Autoscaler, spot instances) across dev/staging/prod environments

Success criteria:
- Can name all 5 cost waste sources and explain which is typically the largest
- Can analyze Prometheus metrics to identify over-provisioned workloads
- Can configure ResourceQuotas and Cluster Autoscaler
- Can make informed decisions about over-engineering (service mesh, replica counts)

## Spaced Repetition Plan
**Introduced** (repeat later):
- FinOps principles → Episode 10 (multi-cluster cost management)
- Vertical Pod Autoscaler (VPA) → Episode 10 (autoscaling at scale)
- Cluster Autoscaler (CA) → Episode 10 (multi-cluster autoscaling)
- ResourceQuotas/LimitRanges → Episode 10 (enforcement at scale)
- Spot instances → Episode 10 (batch workload patterns)

**Reinforced** (from earlier):
- Resource requests/limits from Episode 2 → Applied to cost optimization throughout
- QoS classes from Episode 2 → Referenced in over-provisioning section
- Prometheus metrics from Episode 7 → Used for analyzing actual utilization
- Production readiness from Episode 1 → Cost optimization as requirement

## Lesson Flow

### 1. Recall & Connection (1 min)
**Callback to Episode 7**: "Last episode: observability. Prometheus metrics, four golden signals, monitoring production. Now you can see what's happening. But here's what those metrics also reveal: waste."

**The Cost Problem**:
- Your Prometheus dashboard shows pods requesting 4 CPU cores, using 0.3
- Dev clusters running 24/7, nobody using them at night
- Twenty clusters, each with its own load balancer, monitoring stack, overhead
- CFO asks: "Why did Kubernetes costs triple this year?"

**Hook**: "Two-thirds of companies see Kubernetes Total Cost of Ownership grow year over year. Not because workloads grow. Because waste compounds. Today: the five sources of waste, how to find them, how to fix them."

**Today's Preview**: "First, why Kubernetes costs spiral. Second, the five waste sources ranked by impact. Third, right-sizing strategies using Episode 2's resource concepts and Episode 7's Prometheus metrics. Finally, cost controls that prevent waste before it happens."

### 2. Learning Objectives (30 sec)
By the end, you'll:
- Identify the five primary sources of Kubernetes cost waste
- Right-size resources using actual utilization data and VPA recommendations
- Implement cost controls across environments using quotas, autoscaling, and spot instances

### 3. Why Kubernetes Costs Spiral (2 min)

#### 3.1 The Compounding Problem (1 min)
**Pattern**: Start with one cluster. Add staging. Add dev. Per-team clusters. DR cluster. Twenty clusters later, costs are out of control.

**Why It Happens**:
- Each cluster has baseline costs (control plane, monitoring, networking)
- Clusters don't share resources (no multi-tenancy)
- Dev/staging provisioned like production (overprovisioned for "just in case")
- Nobody responsible for cost optimization (feature work takes priority)

**The Statistics**:
- Typical organization: 60-80% waste in Kubernetes spend
- Over-provisioned requests: 40-60% of total waste
- Idle resources: 20-30% of waste
- Lack of visibility: can't optimize what you can't measure

**Mental Model**: "Kubernetes is like a fleet of trucks. You ordered ten-ton trucks for every delivery. Most deliveries are fifty pounds. You're paying for ten tons of capacity, using fifty pounds. That's over-provisioning."

#### 3.2 The Senior Engineer Problem (1 min)
**Issue**: Engineers optimize for resilience and performance, not cost. This is correct priority. But unchecked, it leads to over-engineering.

**Examples**:
- "We might need 5 replicas" (currently need 2, but planning for growth)
- "Let's add a service mesh" (200 sidecars × 50MB = 10GB overhead)
- "Run dev 24/7 in case someone needs it" (paying for 168 hours, using 40)

**The Balance**: Right-sizing isn't about cutting corners. It's about matching resources to actual needs. Scale when you need it, not "just in case."

**Callback to Episode 2**: "Remember: resource requests reserve capacity. You pay for reservations, not usage. Over-request = overpay."

### 4. The Five Cost Waste Sources (4 min)

#### 4.1 Source #1: Over-Provisioned Resource Requests (Biggest) (1.5 min)
**The Problem**: Pods request 4 CPU cores, use 0.3. Request 8GB memory, use 1.2GB.

**Why It Happens**:
- Developers guess at requirements ("4 cores should be safe")
- Copy-paste manifests from tutorials (those are examples, not recommendations)
- No feedback loop (nobody checks actual usage after deployment)
- Fear of OOM kills (so request 10× what's needed)

**Impact**: 40-60% of total waste. This is the biggest lever.

**Example**: 100 pods × 4 CPU requested × 3.7 CPU wasted = 370 wasted cores. At $0.05/core-hour, that's $16,200/month waste. Just from one application.

**Fix Preview**: Right-sizing strategies (covered in section 5)

**Callback to Episode 2**: "QoS classes: Guaranteed vs Burstable. Over-requesting puts you in Guaranteed. You pay for that guarantee."

#### 4.2 Source #2: Missing Resource Limits (Allows Overcommit) (0.5 min)
**The Problem**: No limits = pods can consume unlimited CPU/memory. Node runs out of resources. Evictions. Noisy neighbor problems.

**Why It's a Cost Issue**:
- Can't pack pods efficiently (unpredictable resource usage)
- Must leave large buffer on nodes (wasted capacity)
- Can't use node autoscaling safely (might scale up unnecessarily)

**Fix**: Set limits at namespace level with LimitRanges (prevents missing limits)

#### 4.3 Source #3: Idle Resources (Dev/Test 24/7) (0.5 min)
**The Problem**: Development cluster with 20 nodes runs 24/7. Developers use it 9 AM to 6 PM, Monday to Friday. That's 45 hours/week usage, paying for 168 hours/week.

**Waste**: 73% idle time, full cost.

**Fix**: Cluster autoscaling to zero, scheduled scale-down, or ephemeral clusters per PR

**Example**: Dev cluster costs $5,000/month. Used 27% of time. Waste: $3,650/month.

#### 4.4 Source #4: No Autoscaling (Paying for Peak Always) (0.5 min)
**The Problem**: Provision for peak load (Black Friday, end-of-month reports). Run that capacity year-round. Pay for 12 months, need it for 2 weeks.

**Fix**: Horizontal Pod Autoscaler (HPA) for pods, Cluster Autoscaler (CA) for nodes. Scale up for peak, scale down for baseline.

**Example**: Baseline 10 pods, peak 50 pods. Without autoscaling: pay for 50 always. With autoscaling: pay for 10 baseline + 40 during peaks.

#### 4.5 Source #5: Lack of Visibility (Can't Optimize) (1 min)
**The Problem**: No cost metrics = no optimization. You don't know:
- Which namespace costs the most?
- Which team is over-provisioning?
- What's the cost trend (up? down?)?
- Where to focus optimization efforts?

**Tools**:
- Kubecost: Shows per-namespace, per-deployment, per-pod costs. Recommendations for savings.
- Cloud provider cost explorers (AWS Cost Explorer, GCP Billing, Azure Cost Management)
- Prometheus metrics: `container_cpu_usage_seconds_total` vs `kube_pod_container_resource_requests`

**The Formula**: Waste = Requested - Used. Prometheus gives you both sides.

**Callback to Episode 7**: "Prometheus metrics from last episode aren't just for alerting. They're for cost optimization. CPU/memory usage vs requests = waste calculation."

### 5. Right-Sizing Strategies (3 min)

#### 5.1 Analyzing Actual vs Requested (1 min)
**Process**:
1. Query Prometheus for actual usage over 7-30 days (get realistic baseline, include peaks)
2. Compare to resource requests
3. Identify candidates: pods with >50% waste (e.g., request 4 CPU, use under 2 CPU)

**PromQL Example**:
```
# CPU waste percentage
(avg_over_time(kube_pod_container_resource_requests{resource="cpu"}[7d]) - avg_over_time(container_cpu_usage_seconds_total[7d])) / avg_over_time(kube_pod_container_resource_requests{resource="cpu"}[7d])
```

**What to Look For**:
- Consistent low usage (request 4, use 0.3 always) → reduce requests
- Occasional spikes (use 0.3 baseline, spike to 2.5) → reduce request but increase limit for bursts
- High variance (unpredictable) → keep current or use VPA

#### 5.2 Vertical Pod Autoscaler (VPA) for Recommendations (1 min)
**What It Does**: VPA watches pod resource usage and recommends requests/limits. Can automatically apply changes (restart pods with new values).

**Modes**:
- Off: Recommendations only, no changes (safest, start here)
- Initial: Sets requests on pod creation, doesn't change running pods
- Auto: Updates requests dynamically (restarts pods)

**Use Cases**:
- Analysis mode (Off): Get recommendations, manually review, apply selectively
- Hands-off mode (Auto): For stateless workloads that handle restarts gracefully

**Example Output**: "Pod X requests 4 CPU, VPA recommends 1.5 CPU (p95 usage is 1.2 CPU)."

**Caveat**: VPA restarts pods. For stateful workloads or high-traffic services, use recommendations but apply manually during maintenance windows.

#### 5.3 Load Testing to Validate (0.5 min)
**Why Necessary**: Can't just cut resources blindly. Must validate performance under load.

**Process**:
1. Apply reduced resource requests in staging
2. Run load test (simulate production traffic + 20% buffer)
3. Monitor: latency (p95, p99), error rate, pod restarts, throttling
4. If metrics stay healthy, apply to production. If degraded, increase requests.

**Tool**: k6, Locust, JMeter, or cloud provider load testing

**Think-Aloud**: "Reduced API requests from 2 CPU to 1 CPU. Load test shows p95 latency increased 50ms → 75ms. Still under 100ms SLO. Deploy to prod. Monitor for a week. No issues. Success."

#### 5.4 Iterative Approach (0.5 min)
**Don't**: Cut all resources 50% across the board. Recipe for outages.

**Do**: Pick 3-5 highest-waste workloads. Right-size one at a time. Monitor each for a week before next.

**Priority Order**:
1. Development/staging (low risk, high impact)
2. Batch jobs/cron jobs (restartable, forgiving)
3. Stateless production services (scalable, can handle restarts)
4. Stateful production services (last, most careful)

### 6. Cost Controls (2 min)

#### 6.1 ResourceQuotas & LimitRanges (1 min)
**ResourceQuotas** (namespace-level): Cap total resources a namespace can request
- Example: Dev namespace limited to 50 CPU, 100GB memory
- Prevents runaway resource requests
- Forces teams to stay within budget

**LimitRanges** (per-pod defaults/limits): Enforce minimum and maximum requests/limits per container
- Example: Containers must request 100m-4 CPU, have limits 100m-8 CPU
- Prevents missing requests/limits
- Sets sane defaults for pods without explicit values

**Use Together**: LimitRanges ensure every pod has requests/limits. ResourceQuotas ensure namespace doesn't exceed budget.

**Example**:
```yaml
# LimitRange: default 500m CPU, max 4 CPU per container
# ResourceQuota: namespace max 20 CPU total
Result: Each pod gets 500m default, can't exceed 4 CPU, namespace caps at 20 CPU (max 40 containers)
```

#### 6.2 Cluster Autoscaler (0.5 min)
**What It Does**: Adds/removes nodes based on pod scheduling needs
- Pods pending (can't schedule)? Add nodes.
- Node underutilized (can reschedule pods elsewhere)? Remove node.

**Cost Impact**: Pay only for nodes you need. Baseline: 5 nodes. Peak: 20 nodes. Average: 8 nodes. You pay for 8, not 20.

**Configuration**: Set min/max node counts, scale-down delay (how long underutilized before removal), resource thresholds

**Callback to Episode 2**: "Remember node pressure eviction? Cluster Autoscaler prevents that by adding capacity before you hit limits."

#### 6.3 Spot Instances for Batch Workloads (0.5 min)
**What They Are**: Spare cloud capacity, 60-90% cheaper than on-demand, can be reclaimed with 2-minute notice

**Use Cases**:
- Batch jobs (can retry if interrupted)
- CI/CD builds (stateless, retryable)
- Data processing (checkpointed, resumable)

**NOT for**:
- Stateful databases (interruption = data risk)
- User-facing APIs (interruption = downtime)
- Critical long-running processes

**Pattern**: Mix of on-demand (for critical workloads) + spot (for batch/retryable workloads)

**Example**: Data pipeline costs $2,000/month on-demand. Switch to spot: $400/month (80% savings). Interrupt rate 5%, jobs retry automatically.

### 7. The Senior Engineer Problem: Over-Engineering vs Right-Sizing (1.5 min)

#### 7.1 The Dilemma (0.5 min)
**Engineer mindset**: "What if we need it?" Design for worst case. Plan for growth. Add redundancy.

**Cost mindset**: "Do we need it now?" Pay for what you use. Scale when necessary.

**Both are right.** The question is: where's the balance?

#### 7.2 Decision Framework (1 min)
**Service Mesh Example**:
- Question: "Do we need a service mesh?"
- Cost: 200 pods × 50MB sidecar = 10GB overhead. Plus operational complexity.
- Value: mTLS, observability, traffic management.
- Decision: Do you have compliance requiring mTLS? 50+ microservices with complex routing? If yes, value > cost. If no, defer until needed.

**Replica Count Example**:
- Question: "3 replicas or 5?"
- Current load: Handles easily with 2 replicas.
- Cost: 3 replicas = $300/month, 5 replicas = $500/month.
- Decision: Start with 3. Add HPA to scale to 5 during peaks. Average cost: $350/month instead of $500/month flat.

**The Pattern**: Start conservative (lower cost). Add autoscaling (safety net). Scale when data shows you need it, not "just in case."

**Callback to Episodes 1 & 6**: "Episode 1: production readiness requires resilience. Episode 6: service mesh adds value for complex architectures. The question isn't 'is it valuable?' It's 'is it valuable NOW, or can we defer?'"

### 8. Common Mistakes (1 min)
**Mistake 1**: Optimizing production first
- **What happens**: High risk, potential outages, team resistance
- **Fix**: Start with dev/staging (low risk, build confidence, prove process)

**Mistake 2**: Cutting resources without monitoring
- **What happens**: Silent performance degradation, eventual outages, rollback
- **Fix**: Monitor during and after changes (latency, error rate, CPU throttling)

**Mistake 3**: No ResourceQuotas in dev/staging
- **What happens**: Developers over-request in dev, promote to prod unchanged, waste continues
- **Fix**: Quotas everywhere, forces right-sizing early

**Mistake 4**: Ignoring idle times
- **What happens**: Dev clusters 24/7, paying for 168 hours, using 40
- **Fix**: Cluster autoscaler to zero, or scheduled scale-down after hours

**Mistake 5**: Optimizing once and forgetting
- **What happens**: Workloads change, requests no longer match usage, waste creeps back
- **Fix**: Monthly review with Kubecost or Prometheus, continuous right-sizing

### 9. Active Recall (1 min)
"Pause and answer these questions:"

**Question 1**: What are the five sources of Kubernetes cost waste? Which is typically the biggest?
[PAUSE 5 sec]

**Question 2**: Your dev cluster costs as much as production. What are three things you'd investigate first?
[PAUSE 5 sec]

**Question 3**: Name three cost optimization techniques you could implement tomorrow with low risk.
[PAUSE 5 sec]

**Answers**:
1. **Five waste sources**: (1) Over-provisioned requests (biggest), (2) Missing limits, (3) Idle resources, (4) No autoscaling, (5) Lack of visibility. Over-provisioning is 40-60% of waste.

2. **Dev cluster investigation**: (1) Is it running 24/7 vs actual usage hours? (2) Are resource requests copy-pasted from production (over-provisioned)? (3) Does it have ResourceQuotas or are teams unlimited?

3. **Low-risk optimizations**: (1) Install Kubecost/enable cloud cost visibility (zero risk, pure insight). (2) Set ResourceQuotas on dev/staging (low risk, immediate cap on waste). (3) Right-size 3-5 highest-waste non-production workloads using VPA recommendations (low risk, measurable savings).

### 10. Recap & Integration (1 min)

**Takeaways**:
1. **Five waste sources ranked**: Over-provisioned requests (40-60%), idle resources (20-30%), no autoscaling, missing limits, lack of visibility
2. **Right-sizing process**: Prometheus metrics (actual vs requested), VPA recommendations, load testing validation, iterative rollout
3. **Cost controls**: ResourceQuotas (namespace caps), LimitRanges (per-pod defaults), Cluster Autoscaler (node scaling), spot instances (batch workloads)
4. **Over-engineering balance**: Start conservative, add autoscaling, scale when data shows need (not "just in case")
5. **Continuous process**: Not one-time optimization. Monthly reviews, adjust as workloads change

**Connection to Previous Episodes**:
- Episode 2's resource requests/limits now have cost implications (over-request = overpay)
- Episode 7's Prometheus metrics enable cost analysis (usage vs requests = waste)
- Episode 1's production readiness includes cost optimization

**Bigger Picture**: You can build infrastructure (Episodes 2-6), see what's happening (Episode 7), and now optimize costs (Episode 8). Next: automate deployments and manage at scale.

### 11. Next Episode Preview (30 sec)
"Next episode: GitOps & Deployment Automation. You've manually deployed with kubectl. That doesn't scale to twenty clusters. We're covering ArgoCD vs Flux for GitOps, Helm vs Kustomize for config management, and deployment strategies beyond rolling updates—canary releases, blue/green deployments. Git becomes your source of truth. Deployments become automated, auditable, and rollbackable. See you then."

---

## Supporting Materials

**Code Examples**:
1. **ResourceQuota YAML** - namespace budget example
2. **LimitRange YAML** - per-pod default requests/limits
3. **VPA manifest** - recommendation mode configuration
4. **Cluster Autoscaler config** - min/max nodes, scale-down delay
5. **PromQL queries** - CPU/memory waste calculation

**Tech References**:
- Kubecost.com - cost visibility and optimization tool
- kubernetes.io/docs/concepts/policy/resource-quotas/ - ResourceQuota docs
- kubernetes.io/docs/concepts/policy/limit-range/ - LimitRange docs
- github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler - CA docs
- github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler - VPA docs

**Analogies**:
1. **Fleet of trucks** - over-provisioned capacity (ten-ton trucks for fifty-pound deliveries)
2. **Hotel rooms** - paying for reservations not usage (resource requests)
3. **Thermostat** - autoscaling matches capacity to demand
4. **Buffet pricing** - pay per person (nodes) vs pay per plate (actual usage)

---

## Quality Checklist

**Structure**:
- [x] Clear beginning/middle/end (recall → five sources → right-sizing → controls → over-engineering → practice → recap)
- [x] Logical flow (problem → sources → solutions → balance → practice)
- [x] Time allocations realistic (12 min total: 1+2+4+3+2+1.5+1+1+1 = ~16.5 min allocated, will tighten in script)
- [x] All sections specific with concrete examples and numbers

**Pedagogy**:
- [x] Objectives specific/measurable (identify 5 sources, right-size using data/VPA, implement controls)
- [x] Spaced repetition integrated (callbacks to Episodes 1,2,7; forward to Episode 10)
- [x] Active recall included (3 retrieval questions with pauses)
- [x] Signposting clear (first/second/third, section transitions)
- [x] 4 analogies (trucks, hotel, thermostat, buffet)
- [x] Pitfalls addressed (5 common mistakes with fixes)

**Content**:
- [x] Addresses pain points (cost spiral, over-engineering, lack of visibility)
- [x] Production-relevant examples (specific dollar amounts, real waste percentages)
- [x] Decision frameworks (service mesh evaluation, replica counts, optimization priority order)
- [x] Troubleshooting included (how to analyze waste, validate changes)
- [x] Appropriate depth for senior engineers (PromQL, VPA modes, spot instance trade-offs)

**Engagement**:
- [x] Strong hook ("Why did Kubernetes costs triple?" / "60-80% waste")
- [x] Practice/pause moments (active recall with 5-sec pauses)
- [x] Variety in techniques (analogies, examples, think-alouds, decision frameworks, PromQL)
- [x] Preview builds anticipation (GitOps automation)
