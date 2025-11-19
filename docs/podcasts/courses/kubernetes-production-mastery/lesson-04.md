---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 #04: Health Checks & Probes"
slug: /courses/kubernetes-production-mastery/lesson-04
---

# Lesson 4: Health Checks & Probes

## Kubernetes Production Mastery Course

<GitHubButtons />

<iframe width="560" height="315" src="https://www.youtube.com/embed/Sko4YBSL7qY" title="Lesson 4: Health Checks & Probes - Kubernetes Production Mastery" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

**Course**: [Kubernetes Production Mastery](/courses/kubernetes-production-mastery)
**Episode**: 4 of 10
**Duration**: 18 minutes
**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

## Learning Objectives

By the end of this lesson, you'll be able to:
- Configure the three types of Kubernetes probes (startup, readiness, liveness) with production-appropriate thresholds
- Diagnose why pods are stuck in CrashLoopBackOff or marked NotReady
- Design health endpoints that actually validate application health - not just process existence

## Prerequisites

- [Lesson 1: Production Mindset](./lesson-01)
- [Lesson 2: Resource Management](./lesson-02)
- [Lesson 3: Security Foundations](./lesson-03)

---

## Transcript

Welcome to Episode 4 of Kubernetes Production Mastery. In the last episode, we mastered RBAC and secrets management - securing your cluster and protecting sensitive data. Before we continue, try to recall: what's the principle of least privilege in RBAC? That's right - grant only the minimum permissions needed for a role to function.

But here's what we didn't discuss: how does Kubernetes decide when to restart a pod? Or more importantly, how does it know if your application is actually healthy after it restarts? That's where today's topic comes in - health checks and probes. By the end of this lesson, you'll be able to configure the three types of Kubernetes probes with production-appropriate thresholds, diagnose why pods are stuck in CrashLoopBackOff or marked NotReady, and design health endpoints that actually validate application health - not just process existence.

### The $2.3M Mistake

Let me tell you about last week at a major fintech company. They had a 47-minute outage that cost them 2.3 million dollars in SLA penalties.

The root cause? A misconfigured liveness probe. The probe was checking if the process existed, not if it could actually process transactions. The application was completely deadlocked, threads frozen, unable to handle a single request. But Kubernetes thought everything was fine because the process was still running. This is the kind of mistake that seems obvious in hindsight but happens all the time in production.

### Three Fundamentally Different Questions

Here's the thing about probes - they're Kubernetes asking your application three fundamentally different questions. And if you give the wrong answer to any of them, you're going to have a bad time.

The **startup probe** asks: "Are you done initializing?" This protects slow-starting containers. Think about that Java application with a two-minute boot time while it loads Spring context, warms up connection pools, and builds its cache.

The **readiness probe** asks: "Can you handle traffic right now?" This controls whether your pod receives requests from the service. It's your circuit breaker.

The **liveness probe** asks: "Are you still alive or do you need a restart?" This is the nuclear option. When this fails, Kubernetes kills your container and starts fresh.

Now you might be thinking - why three different probes? Can't we just have one health check?

Here's why that doesn't work. Imagine your application starts up. It needs to connect to a database, warm up its cache, maybe download some configuration. That takes time. If your liveness probe kicks in after 30 seconds but your app needs 90 seconds to start, you've created a restart loop. The app never gets a chance to become healthy. That's what the startup probe prevents. It gives your application time to initialize before the other probes even begin checking.

Once your app is running, you need to know two different things. First, is it healthy enough to handle traffic? That's readiness. Second, is it so broken it needs to be restarted? That's liveness. And here's the critical distinction that trips up even experienced engineers: these are NOT the same question.

### The Critical Distinction: Database Down Scenario

Your database might be down. Should that fail your liveness probe?

Absolutely not. Your application is healthy - it's the database that's having problems. Restarting your app won't fix the database. In fact, it'll make things worse when the database comes back and suddenly has a thundering herd of restarting applications all trying to reconnect at once.

But should the database being down fail your readiness probe? Yes! You can't handle traffic if you can't reach your database. You want Kubernetes to stop routing traffic to you until the database recovers. See the difference? Readiness is about capability. Liveness is about the application itself.

### How Probes Work: Three Mechanisms

Let's talk about how these probes actually work under the hood. You've got three mechanisms to choose from.

**HTTP GET** is the most common. Kubernetes calls your endpoint and expects a 200 to 399 status code. Anything else is a failure. Simple, right? But here's what people miss - this isn't just about returning 200 OK. This is your chance to actually validate that your application works.

**TCP Socket** is simpler - Kubernetes just tries to open a TCP connection to your specified port. If it connects, you're healthy. This is useful for databases or other TCP services that don't speak HTTP.

**Exec** runs a command inside your container. If it exits with code 0, you're healthy. This is powerful but be careful - you're running this command frequently, so it needs to be lightweight.

### Timing Parameters

Now let's talk about timing, because this is where things get really interesting. You've got five timing parameters to work with.

- **initialDelaySeconds** tells Kubernetes when to start checking after the container starts
- **periodSeconds** is how often to check
- **timeoutSeconds** is how long to wait for a response
- **successThreshold** is how many successes before you're considered healthy
- **failureThreshold** is how many failures before Kubernetes takes action

Here's what actually happens when a readiness probe fails. After failureThreshold consecutive failures, your pod gets marked NotReady. The endpoints controller sees this and removes your pod from the service endpoints. The ingress controller updates its backend pool. No new traffic routes to your pod. Existing connections might persist depending on your setup, but you're effectively out of the load balancer.

For a liveness probe failure, it's more dramatic. After failureThreshold failures, the kubelet initiates a pod restart. Your container gets a SIGTERM signal. If it doesn't exit gracefully within the terminationGracePeriodSeconds, it gets SIGKILL. Then Kubernetes starts a new container. If you have a startup probe, that runs first. Only after the startup probe succeeds do the readiness and liveness probes begin.

### Real-World Example: E-Commerce API

Let me show you what this looks like in practice with a real-world example - an e-commerce API with a database dependency.

**Startup Probe Configuration:**

For your startup probe, you want to check that everything's initialized. Application context loaded? Database migrations completed? Cache warmed if that's required? External service clients initialized?

```yaml
startupProbe:
  httpGet:
    path: /health/startup
    port: 8080
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 30  # 5 minutes max for startup
```

That's generous, but production applications with large caches or complex initialization might need it.

**Readiness Probe Configuration:**

Your readiness probe is different. This checks if you can handle traffic RIGHT NOW. Database connection pool has available connections? Required external services reachable? No circuit breakers open? Not in maintenance mode?

```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  periodSeconds: 5       # More frequent - can change quickly
  timeoutSeconds: 2
  successThreshold: 1    # Ready as soon as one success
  failureThreshold: 3    # Three failures = stop traffic
```

**Liveness Probe Configuration:**

And here's the critical one - your liveness probe. This should be shallow. I can't emphasize this enough. Your liveness probe should ONLY check if the application itself is healthy. Not dependencies. Not external services. Just the app.

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 60  # Let startup/readiness stabilize
  periodSeconds: 10
  timeoutSeconds: 5        # More generous - restart is disruptive
  failureThreshold: 3
```

What should this liveness endpoint actually check? Application threads not deadlocked. Event loop responsive. Memory not critically exhausted. Can perform a basic operation like returning the health status. That's it. Nothing more.

### Five Common Mistakes in Production

Now let me tell you about the five most common mistakes I see in production. These are the ones that cause outages.

**Mistake #1: Liveness Probe Checks External Dependencies**

Your app is healthy but the database is down. Liveness probe fails, triggers a restart. App restarts, database is still down, probe fails again. Congratulations, you've created a restart loop that makes recovery impossible. When the database finally recovers, your app is mid-restart and can't serve traffic. The fix? Liveness should ONLY check the application itself. Use readiness for dependencies.

**Mistake #2: Identical Readiness and Liveness Probes**

If they're the same, why have both? This usually means you're not thinking about their different purposes. Readiness answers "Can I serve traffic?" Liveness answers "Am I frozen?"

**Mistake #3: Aggressive Liveness Probe Timing**

FailureThreshold of 1, period of 5 seconds, timeout of 1 second. This killed production last Tuesday at a client's site. One slow garbage collection, one network hiccup, and boom - unnecessary restart. Your liveness probe just caused more problems than it solved. The fix? Be generous with liveness timing. Restarts are disruptive. You want to be really sure the application is broken before you pull that trigger.

**Mistake #4: No Startup Probe for Slow-Starting Applications**

Your Java app takes 90 seconds to start. The liveness probe kicks in after 30 seconds and kills it. The app restarts, takes 90 seconds again, gets killed after 30. Restart loop. The fix? Always use a startup probe for applications with initialization over 30 seconds. Give them time to actually start.

**Mistake #5: Expensive Health Check Computation**

The health endpoint queries the entire database, aggregates metrics, validates every connection. Takes 5 seconds to respond. Gets called every 5 seconds by three different probes. You've just DOSed yourself with your own health checks. The fix? Health checks must be lightweight - milliseconds, not seconds.

### Production Pattern: Shallow vs Deep Health Checks

Let's talk about patterns for production. The key pattern you need to understand is shallow versus deep health checks.

**Shallow checks** are for liveness - is the process responsive? Basic memory check. Can I return a simple response? That's it.

**Deep checks** are for readiness - can I actually do my job? Validate functionality. Check dependencies. Ensure I can handle real requests.

Never, and I mean never, use deep checks for liveness unless you want cascading failures across your entire system.

### Debugging Workflows

When you're debugging a CrashLoopBackOff, here's your workflow:

1. Check the probe configuration with `kubectl describe pod`. Look for probe failure events - they'll say something like "Liveness probe failed: Get http://..."
2. Test the endpoint manually from inside the pod with `kubectl exec`. Sometimes the endpoint works, but not on the port or path you configured.
3. Check probe timing versus actual startup time. Your app might need 45 seconds but your startup probe only gives it 30.
4. Review the container logs. Sometimes the container is crashing before the probe even runs. Exit code 1 means your app errored. Exit code 137 means OOMKilled. Exit code 143 means SIGTERM.

For NotReady pods, it's a different investigation:

1. Check readiness probe events in the pod description. These will tell you exactly what's failing.
2. Verify the endpoint is actually accessible from within the pod. Sometimes it's a networking issue, not a health issue.
3. Check if dependencies are available. Is your database up? Can you reach external services?
4. Review service endpoint registration with `kubectl get endpoints`. You should see your pod IP there if it's ready.

### Active Recall Quiz

Alright, pause the audio and answer these questions:

1. Your pod keeps restarting every 2 minutes. Which probe is most likely misconfigured?
2. Your application takes 3 minutes to warm its cache on startup. Which probe type should you use to protect it?
3. The database is down. Should this fail your liveness probe, readiness probe, or both?

**Answers:**

1. If your pod keeps restarting, it's the liveness probe. That's the only probe that triggers restarts. Readiness just stops traffic. Startup just delays the other probes.
2. For an app that takes 3 minutes to warm cache, you need a startup probe. It protects slow initialization from the other probes. Set the failure threshold high enough to give it time.
3. Database down should fail ONLY your readiness probe. Never liveness. Liveness checking external dependencies causes cascading failures. Your app is healthy even if the database isn't.

### Key Takeaways

Let's bring this all together. You've learned three types of probes with three distinct purposes. Startup for initialization, readiness for traffic control, liveness for restart decisions.

Remember that liveness probes are nuclear options. Be conservative with timing and checks. An unnecessary restart is worse than delayed detection. Never check external dependencies in liveness probes. That's what readiness is for.

This is probably the most important lesson today: **Health endpoints must be lightweight.** They're called frequently - every few seconds by multiple probes. If your health check takes a second to respond, you're doing it wrong.

Failed probes are the number three cause of production Kubernetes outages, right after resource limits and network policies. This connects directly to the production mindset we discussed in Episode 1. Health checks are your first line of defense. They work with the resource limits from Episode 2 - a pod that's OOMKilled needs proper health checks to recover correctly.

Remember those five failure patterns from Episode 1? Improper health checks contribute to three of them: cascade failures, thundering herd, and cold start problems.

### Next Episode

Next time, we're exploring StatefulSets and persistent storage. You'll learn when to use StatefulSets versus Deployments, how Persistent Volumes and Claims actually work, and the common storage failures that trip up even experienced teams. This builds directly on today's health checks - stateful applications need even more careful probe configuration because they have state to protect.

See you in the next lesson.

---

## Navigation

⬅️ **Previous**: [Lesson 3: Security Foundations](./lesson-03) | **Next**: [Lesson 5: Stateful Workloads](./lesson-05) ➡️

📚 **[Back to Course Overview](/courses/kubernetes-production-mastery)**
