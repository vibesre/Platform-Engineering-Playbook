---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 #02: Resource Management"
slug: /podcasts/courses/kubernetes-production-mastery/lesson-02
---

# Lesson 02: Resource Management - Preventing OOMKilled

## Kubernetes Production Mastery

<GitHubButtons />

<iframe width="560" height="315" src="https://www.youtube.com/embed/o7PMifh-Khk" title="Lesson 02: Resource Management - Kubernetes Production Mastery" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

**Course**: [Kubernetes Production Mastery](/podcasts/courses/kubernetes-production-mastery)
**Episode**: 02 of 10
**Duration**: 19 minutes
**Presenter**: Production Engineering Instructor
**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience
**Engagement Quality**: 10/10 (validated)

## Learning Objectives

By the end of this lesson, you'll be able to:
- **Explain** the difference between resource requests and limits, and why Kubernetes needs both
- **Debug** an OOMKilled pod from exit code 137 to root cause using a systematic 5-step workflow
- **Right-size** your containers using load testing data, P50/P95/P99 metrics, and Quality of Service principles

## Prerequisites

- [Lesson 01: Production Mindset](./lesson-01) - Covers the production readiness checklist (resource limits/requests is item #1)
- Basic understanding of Kubernetes Pods and kubectl commands
- Familiarity with production incidents and debugging workflows

---

## Lesson Transcript

In Episode 1, we covered the production readiness checklist. Remember the number one item? Resource limits and requests set. Every container must have both.

But here's the thing—most engineers I talk to can't explain WHY you need both. They know you're supposed to set them. They copy-paste examples from Stack Overflow. But they don't understand the actual mechanism.

Before we dive in, pause and recall from Episode 1: What was the cost of that Black Friday OOMKilled incident? Ninety-four thousand dollars in forty-seven minutes. All because resource limits weren't configured.

Today, we're making sure you never have that problem.

This lesson builds directly on that checklist item. We're going deep. By the end, you'll understand requests vs limits at a level where you can debug OOMKilled errors in production, architect resource allocation for entire clusters, and make intelligent trade-off decisions.

Here's the reality. Exit code 137—OOMKilled—is the single most common production failure in Kubernetes. Sixty-seven percent of teams have experienced it. If you don't master resource management today, you WILL get paged at three AM.

By the end of this fifteen-minute lesson, you'll be able to: Explain the difference between requests and limits, and why Kubernetes needs both. Debug an OOMKilled pod from exit code 137 to root cause using a systematic workflow. And right-size your containers using load testing and Quality of Service principles.

Let's go.

Most engineers think requests and limits do the same thing. They don't.

Requests are for the scheduler. Limits are for the runtime.

Two completely different systems. Two completely different purposes.

Think of resource requests like booking a hotel room.

You request a room with one king bed. The hotel guarantees that room exists and is available for you. That's your request—it's a guarantee from the system that these resources will be available.

But here's the key: Just because you requested a king bed doesn't mean you'll USE the whole room. Maybe you only sleep on half the bed. Maybe you don't use the mini-bar. The hotel still reserves the room for you—that's scheduling.

Resource limits? That's the fire marshal saying this room can hold a maximum of four people. Try to cram in a fifth? Fire code violation. System says no.

In Kubernetes: Requests ensure your pod gets scheduled on a node with sufficient resources. Limits prevent your pod from consuming unlimited resources and crashing other workloads.

Let's get specific. Your API pod.

What this means: The scheduler—Kubernetes finds a node with at least 512 megabytes available memory and 250 millicores available CPU. That's the scheduling guarantee. The runtime—your pod can USE up to 1 gigabyte of memory and 500 millicores of CPU. If it tries to exceed 1 gigabyte? OOMKilled. Exit code 137.

The production reality. Under normal load: uses 400 megabytes. Well within request and limit.

Traffic spike: climbs to 800 megabytes. Still fine—between request at 512 and limit at 1024.

Memory leak or actual spike to 1.1 gigabytes? Kubernetes kills it. Instantly. No negotiation.

So why not just set limits really high and avoid OOMKills? Because you'll overcommit nodes, waste money, and create the noisy neighbor problem. We'll get to that.

When you deploy a pod with resource requests, here's what happens:

Step 1: Kubernetes scheduler looks at all nodes. Step 2: For each node, calculates: Total capacity minus already-requested resources equals available. Step 3: Finds a node where available is greater than or equal to your request. Step 4: Schedules pod on that node.

Concrete example. Node has 8 gigabytes total memory. Existing pods requested: 5 gigabytes. Your pod requests: 2 gigabytes. Math: 8 minus 5 equals 3 gigabytes available. Your 2 gigabyte request fits. Scheduled.

But here's the gotcha: The node might only have 1 gigabyte ACTUALLY FREE right now. Because requests are guarantees, not actual usage. This is overcommitment—and it's intentional.

Limits are enforced by the container runtime—containerd, CRI-O, whatever you're using.

Every container gets a Linux cgroup. The cgroup has memory limits configured. When your process tries to allocate memory beyond the limit, the OOMKiller steps in.

Let's walk through an OOMKill. Your pod is running, using 800 megabytes. Application gets a burst of traffic. Tries to allocate another 300 megabytes. Total: 800 plus 300 equals 1.1 gigabytes. Limit: 1 gigabyte. Kernel checks: Attempted 1.1 gigabytes exceeds limit 1.0 gigabytes. Kernel invokes OOMKiller. Sends SIGKILL—signal 9. Exit code: 128 plus 9 equals 137. Pod status: OOMKilled.

Kubernetes sees the failure. Restart policy: Always. Starts a new pod. If the problem persists? CrashLoopBackOff.

Here's what trips people up. Nodes can be overcommitted on requests but NOT on limits.

Concrete scenario: Node has 8 gigabytes memory. Three pods, each requesting 2 gigabytes, limiting 4 gigabytes. Total requests: 6 gigabytes. Fits on node. Total limits: 12 gigabytes. Doesn't fit.

This is fine. Most pods don't hit their limits. But if ALL THREE pods spike to their limits simultaneously? Node runs out of memory. Kernel starts killing pods. Production outage.

This is why right-sizing matters. This is why monitoring matters. This is why Quality of Service classes exist.

Real incident, twenty twenty-four. Black Friday. E-commerce company. Traffic spiking.

Three AM: Pager goes off. API pods OOMKilling in a cascade. One dies, others get more traffic, they spike, they die. Repeat.

Engineer SSH's in. Panicking. Let's walk through the systematic workflow I wish they'd followed.

Step 1: Identify the symptom. kubectl get pods namespace production. Output shows: api-deployment with restart count 3, status OOMKilled, 5 minutes old. Exit code 137. Memory issue confirmed.

Step 2: Check the events. kubectl describe pod api-deployment namespace production. Events show: OOMKilled—Container exceeded memory limit 1073741824 bytes. Translation: Hit 1 gigabyte limit. But was the limit too low or is there a memory leak?

Step 3: Check actual usage patterns. kubectl top pod shows current usage if the pod is still running. But we need historical data. Check Prometheus or your monitoring system. Query: container memory usage bytes for that pod. Graph shows: Normal 600 megabytes. Spikes to 1.2 gigabytes under load.

Step 4: Analyze the configuration. kubectl get pod with output yaml, grep for resources. Shows requests: 256 megabytes. Limits: 1 gigabyte. Problem identified: Limit is 1 gigabyte. Normal usage 600 megabytes leaves only 400 megabyte headroom. Traffic spike exceeds that.

Step 5: Determine root cause and fix. Two possibilities: Limit too low for legitimate traffic spikes, increase limit. Or memory leak in application, fix application code. In this case: Legitimate traffic spike. Fix: Increase requests to 512 megabytes for better scheduling. Increase limits to 2 gigabytes for headroom. Deploy. Monitor. Problem solved.

Pause here. Before I show you Quality of Service classes, how would YOU debug a pod that's in OOMKilled status right now?

Remember: get pods, describe pod, check events, check monitoring for usage patterns, check YAML for configuration, determine if limit is too low or if there's a leak.

When a node runs out of memory, Kubernetes has to decide which pods to kill. It uses Quality of Service classes.

Three classes: Guaranteed, Burstable, BestEffort.

Class 1: Guaranteed. When: Requests equal limits for BOTH memory and CPU. Behavior: Last to be killed during node memory pressure. These are your critical workloads. Use for: Databases, payment processing, anything that absolutely cannot tolerate OOMKills.

Class 2: Burstable. When: Requests are less than limits. Behavior: Killed before Guaranteed but after BestEffort. Most common class. Use for: Most application workloads. They can burst when needed but have a safety limit.

Class 3: BestEffort. When: No requests or limits set at all. Behavior: First to be killed during node memory pressure. Kubernetes makes no promises. Use for: Batch jobs, non-critical background tasks, things that can tolerate interruption. Pro tip: Almost never use this in production. It's asking for trouble.

The eviction priority. Node runs out of memory. Kubernetes kills pods in this order: First, BestEffort pods—no guarantees, first to go. Second, Burstable pods exceeding requests—using more than guaranteed. Third, Burstable pods within requests. Finally, Guaranteed pods—last resort.

This is why setting requests and limits matters. It's not just resource allocation—it's survival priority during outages.

Set requests and limits too low? OOMKills. Set them too high? Wasted resources, higher costs, poor node utilization.

We need to right-size.

Step 1: Measure current usage. Run in production for a week. Monitor actual memory and CPU usage. P50, that's median, shows typical load. P95 shows high load, not peak. P99 shows peak load, rare spikes. Example metrics: P50 at 400 megabytes. P95 at 800 megabytes. P99 at 1.2 gigabytes.

Step 2: Set requests at P50 to P75, limits at P95 to P99. Requests: Set at typical load, P50 to P75. This ensures good scheduling without over-requesting. Limits: Set at high load with headroom, P95 to P99 plus 20 to 30 percent. From our example: Request 512 megabytes, around P75. Limit 1.5 gigabytes, P99 plus headroom. This allows normal bursting while preventing runaway memory consumption.

Step 3: Load test and validate. Before deploying to production, load test. Simulate three times expected traffic. Monitor memory usage during test. Does it stay within limits? Good. Does it OOMKill? Increase limits and retest. Critical: Test with REALISTIC traffic patterns. Bursts, not constant load.

Real story. Startup, twenty pods, each requesting 4 gigabytes. Actual usage? 800 megabytes average. They're paying for 80 gigabytes requested. Actually using 16 gigabytes. Wasting $2,400 per month on unused capacity. Right-sizing to 1 gigabyte requests, 2 gigabyte limits? Same performance, $1,800 per month savings. At scale, this adds up.

Mistake 1: Setting requests equal to limits for everything. Why it fails: You lose burstability. Everything is Guaranteed QoS. Wastes resources because most workloads don't need their limits constantly. Fix: Use Burstable for most workloads. Requests at typical usage, limits at peak plus headroom.

Mistake 2: No limits at all. Why it fails: One memory leak brings down the entire node. Concrete example: Background worker has a bug. Memory climbs: 1 gigabyte, 2 gigabytes, 4 gigabytes, 8 gigabytes. Consumes entire node. Fourteen other pods on that node start failing. Fix: Always set limits. Even if generous, they're a safety net.

Mistake 3: Not monitoring actual usage before setting values. Why it fails: You're guessing. Either too low, OOMKills, or too high, wasted money. Fix: Deploy with conservative estimates, monitor for a week, adjust based on actual P95, P99 data.

Pause and answer these without looking back: What's the difference between requests and limits? One sentence each. A pod has requests 512 megabytes, limits 1 gigabyte. It's using 750 megabytes. What QoS class? A node runs out of memory. What order are pods killed?

Answers: Requests—scheduler uses them to decide which node has capacity. Limits—runtime enforces them to prevent runaway resource consumption. QoS class is Burstable—requests are less than limits. Eviction order: BestEffort first, then Burstable exceeding requests, then Burstable within requests, finally Guaranteed.

Let's recap what we covered:

One. Requests vs limits: Requests are for scheduling, limits are for enforcement. Two different systems, two different jobs.

Two. The hotel analogy: Requests reserve the room, limits enforce the fire code.

Three. OOMKilled debugging workflow: Five steps—get pods, describe pod, check events, check monitoring, analyze config, determine root cause.

Four. QoS classes: Guaranteed when requests equal limits. Burstable when requests less than limits. BestEffort when none set. Determines eviction priority.

Five. Right-sizing formula: Requests at P50 to P75, limits at P95 to P99 plus twenty to thirty percent headroom. Validate with load testing.

Six. War stories: Ninety-four thousand dollars from missing limits. Twenty-four hundred dollars per month wasted from over-provisioning.

Remember the production readiness checklist from Episode 1? Resource limits and requests—item number one. Now you understand WHY. It's not just a checkbox. It's the difference between stable production and three AM pages.

We'll revisit these concepts in Episode 8 when we cover cost optimization. Right-sizing isn't just about stability—it's also about money. And in Episode 4, we'll use this debugging workflow to troubleshoot CrashLoopBackOff issues.

Next up: Episode 3—Security Foundations: RBAC and Secrets.

You'll learn: Why RBAC misconfigurations are the number one Kubernetes security issue in twenty twenty-five. How to implement least privilege roles that actually work in production. Secrets management patterns using Sealed Secrets and External Secrets Operator.

Remember that crypto miner attack from Episode 1? Forty-three thousand dollar AWS bill from over-privileged service accounts? Episode 3 makes sure that never happens to you.

See you in Episode 3.

---

## Key Takeaways

- **Requests vs Limits**: Requests are for the scheduler (guarantees for node placement), limits are for the runtime (enforcement by kernel OOMKiller). Two different systems, two different purposes.
- **The hotel analogy**: Requests = booking a room (guaranteed reservation), limits = fire code (max occupancy). Helps visualize why you need both.
- **Exit code 137 = OOMKilled**: 128 + 9 (SIGKILL). Most common Kubernetes production failure (67% of teams experience it).
- **5-step debugging workflow**: (1) Identify symptom (kubectl get pods), (2) Check events (kubectl describe), (3) Check usage patterns (Prometheus/monitoring), (4) Analyze config (kubectl get pod -o yaml), (5) Determine root cause and fix.
- **QoS classes determine eviction priority**: Guaranteed (requests=limits) → last killed. Burstable (requests&lt;limits) → middle priority. BestEffort (no requests/limits) → first killed.
- **Right-sizing formula**: Requests at P50-P75 (typical usage), limits at P95-P99 + 20-30% headroom. Validate with load testing at 3x expected traffic.
- **Real costs**: $94K in 47 minutes (missing limits), $2,400/month wasted (over-provisioning), $1,800/month saved (right-sizing).

---

## Navigation

⬅️ **Previous**: [Lesson 01: Production Mindset](./lesson-01) | **Next**: Lesson 03: Security Foundations (Coming Soon) ➡️

📚 **[Back to Course Overview](/podcasts/courses/kubernetes-production-mastery)**
