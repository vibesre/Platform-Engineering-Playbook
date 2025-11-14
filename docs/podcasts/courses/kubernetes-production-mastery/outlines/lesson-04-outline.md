# Lesson 4: Health Checks & Probes - Outline

## Course Information
**Course**: Kubernetes Production Mastery
**Episode**: 4 of 10
**Duration**: 18 minutes
**Format**: Single presenter (Autonoe, educational)
**Target Audience**: Senior platform engineers, SREs, DevOps engineers (5+ years experience)

## Learning Objectives

By the end of this lesson, you'll be able to:
1. Configure the three types of Kubernetes probes (startup, readiness, liveness) with production-appropriate thresholds
2. Diagnose why pods are stuck in CrashLoopBackOff or marked NotReady
3. Design health endpoints that actually validate application health - not just process existence

## Prerequisites
- Lesson 1: Production Mindset
- Lesson 2: Resource Management (understanding OOMKilled and exit codes)
- Lesson 3: Security Foundations

## Pedagogical Approach

### Teaching Techniques
- **Real-world failure story**: $2.3M fintech outage from misconfigured liveness probe
- **Three distinct questions framework**: Startup, Readiness, Liveness
- **Contrast pattern**: When to use each probe type
- **Active recall prompts**: Database down scenarios, restart loop diagnosis
- **Common mistakes catalog**: Five production anti-patterns

### Spaced Repetition
- **Reinforces from previous episodes**:
  - Episode 1: Health checks as production mindset item #2
  - Episode 2: OOMKilled and exit code 137
  - Episode 2: Resource constraints and QoS classes
- **Introduces for future episodes**:
  - kubectl troubleshooting workflow (foundation for Episode 5+)
  - Service endpoints and traffic routing (Episode 6 networking)
  - Dependencies vs application health (Episode 7 observability)

### Active Recall Moments
1. **Opening**: "Try to recall: what happens when a pod exceeds its memory limit?"
2. **Mid-lesson**: "Should database being down fail your liveness probe?"
3. **Mid-lesson**: "Should database being down fail your readiness probe?"
4. **End quiz**:
   - Pod keeps restarting every 2 minutes - which probe?
   - App takes 3 minutes to warm cache - which probe protects it?
   - Database down - which probe should fail?

---

## Content Structure

### Section 1: Introduction & The $2.3M Mistake (3 min)
**Opening hook**: Real fintech outage from misconfigured liveness probe
- Spaced repetition callback to Episode 2: OOMKilled with exit code 137
- Learning objectives statement
- The real story: App completely deadlocked but process still running
- Key insight: Probe checked process existence, not actual health

### Section 2: The Three Questions Framework (4 min)
**Mental model**: Each probe asks a fundamentally different question

#### Startup Probe
- Question: "Are you done initializing?"
- Purpose: Protects slow-starting containers
- Example: Java app with 2-minute Spring boot time
- When it runs: Only during initialization

#### Readiness Probe
- Question: "Can you handle traffic right now?"
- Purpose: Controls service endpoint registration
- Acts as circuit breaker for traffic
- Can transition between ready/not ready multiple times

#### Liveness Probe
- Question: "Are you still alive or do you need a restart?"
- Purpose: Restart decision (nuclear option)
- Only triggers when application itself is broken
- Be conservative with this one

**Why three probes?** Walking through why a single health check doesn't work
- Scenario: App needs 90 seconds to start, liveness probe at 30 seconds
- Result: Restart loop - app never gets chance to become healthy
- Solution: Startup probe delays other probes until initialization complete

### Section 3: Liveness vs Readiness - The Critical Distinction (4 min)
**Key teaching moment**: Database down scenario

#### The Question
"Your database is down. Should this fail your liveness probe?"
- **Answer: Absolutely not**
- Your application is healthy - database has the problem
- Restarting your app won't fix the database
- Makes recovery WORSE: thundering herd when database recovers

#### Second Question
"Should database down fail your readiness probe?"
- **Answer: Yes!**
- Can't handle traffic without database
- Want Kubernetes to stop routing traffic until database recovers
- **Key distinction**: Readiness = capability, Liveness = application health

### Section 4: Probe Mechanisms & Configuration (3 min)
**Three ways to check health**:

#### HTTP GET (most common)
- Kubernetes calls endpoint, expects 200-399 status
- Not just about returning 200 - validate actual application health
- Opportunity to check dependencies (for readiness only)

#### TCP Socket
- Kubernetes opens TCP connection to port
- If connects, you're healthy
- Useful for databases, non-HTTP services

#### Exec
- Runs command inside container
- Exit code 0 = healthy
- Must be lightweight (runs frequently)

**Timing Parameters (5 parameters)**:
- `initialDelaySeconds`: When to start checking after container starts
- `periodSeconds`: How often to check
- `timeoutSeconds`: How long to wait for response
- `successThreshold`: Consecutive successes before healthy
- `failureThreshold`: Consecutive failures before action

**What actually happens**:
- **Readiness failure**: Pod marked NotReady → removed from service endpoints → no new traffic
- **Liveness failure**: kubelet restarts pod → SIGTERM → SIGKILL if needed → new container → startup probe → readiness/liveness

### Section 5: Real-World Example Configuration (3 min)
**E-commerce API with database dependency**

#### Startup Probe Configuration
```
startupProbe:
  httpGet:
    path: /health/startup
    port: 8080
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 30  # 5 minutes max for startup
```
**Checks**: App context loaded, database migrations complete, cache warmed, external clients initialized

#### Readiness Probe Configuration
```
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  periodSeconds: 5  # More frequent - can change quickly
  timeoutSeconds: 2
  successThreshold: 1  # Ready as soon as one success
  failureThreshold: 3  # Three failures = stop traffic
```
**Checks**: Database pool available, external services reachable, no circuit breakers open, not in maintenance mode

#### Liveness Probe Configuration
```
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 60  # Let startup/readiness stabilize
  periodSeconds: 10
  timeoutSeconds: 5  # More generous - restart is disruptive
  failureThreshold: 3
```
**Checks (shallow only)**: Application threads not deadlocked, event loop responsive, memory not critically exhausted, can perform basic operation

**Critical principle**: Liveness endpoint must be shallow - NO external dependencies

### Section 6: Five Common Mistakes (3 min)
**Production anti-patterns that cause outages**

#### Mistake #1: Liveness Checks External Dependencies
- Scenario: Database down, liveness fails, app restarts
- Result: Restart loop prevents recovery
- Fix: Liveness checks ONLY the application itself

#### Mistake #2: Identical Readiness and Liveness Probes
- If they're the same, why have both?
- Means you're not thinking about different purposes
- Fix: Readiness = "Can I serve?" / Liveness = "Am I frozen?"

#### Mistake #3: Aggressive Liveness Probe Timing
- Example: failureThreshold=1, period=5s, timeout=1s
- One GC pause or network hiccup = unnecessary restart
- Fix: Be generous with liveness timing - restarts are disruptive

#### Mistake #4: No Startup Probe for Slow-Starting Apps
- Java app takes 90s to start, liveness kicks in at 30s
- Result: Permanent restart loop
- Fix: Always use startup probe for apps >30s initialization

#### Mistake #5: Expensive Health Check Computation
- Health endpoint queries database, aggregates metrics, validates everything
- Takes 5 seconds, called every 5 seconds by three probes
- Result: Self-DOS with your own health checks
- Fix: Health checks must be lightweight (milliseconds)

### Section 7: Debugging Workflows (2 min)
**Systematic approaches to common failures**

#### CrashLoopBackOff Debugging
1. `kubectl describe pod` - check probe failure events
2. `kubectl exec` - test endpoint manually from inside pod
3. Compare probe timing vs actual startup time
4. Review container logs for exit codes (1=app error, 137=OOMKilled, 143=SIGTERM)

#### NotReady Pods Debugging
1. Check readiness probe events in pod description
2. Verify endpoint accessible from within pod
3. Check if dependencies available (database up? external services reachable?)
4. Review service endpoint registration: `kubectl get endpoints`

### Section 8: Production Patterns (1 min)
**Key pattern**: Shallow vs Deep Health Checks
- **Shallow (for liveness)**: Is process responsive? Basic memory check. Simple response.
- **Deep (for readiness)**: Validate functionality. Check dependencies. Ensure can handle real requests.
- **Critical rule**: Never use deep checks for liveness

### Section 9: Active Recall Quiz (2 min)
**Pause for self-assessment**

Three questions:
1. Pod keeps restarting every 2 minutes - which probe is misconfigured?
2. App takes 3 minutes to warm cache on startup - which probe type protects it?
3. Database is down - should this fail liveness, readiness, or both?

**Answers provided**:
1. Liveness probe (only one that triggers restarts)
2. Startup probe (protects slow initialization)
3. Readiness only (never liveness for external dependencies)

### Section 10: Synthesis & Forward Connection (1 min)
**Key takeaways**:
- Three types of probes with three distinct purposes
- Liveness is nuclear option - be conservative
- Never check external dependencies in liveness
- Health endpoints must be lightweight
- Failed probes are #3 cause of Kubernetes outages

**Connection to previous episodes**:
- Episode 1: Health checks as production mindset defense
- Episode 2: Works with resource limits for recovery

**Connection to next episode**:
- Preview: Kubernetes networking and service discovery
- Why pods can't reach each other
- ClusterIP vs NodePort vs LoadBalancer
- How DNS actually works (builds on health checks - healthy pod needs traffic)

---

## Teaching Notes

### Analogies & Examples
- **Startup probe**: Like waiting for coffee machine to heat up before using it
- **Readiness probe**: Like "Open/Closed" sign on store - still exists but not serving customers
- **Liveness probe**: Like checking if employee is unconscious - only intervene for serious issues

### Emphasis Points
- "This is probably the most important lesson today" (lightweight health checks)
- "I can't emphasize this enough" (liveness should be shallow)
- "This is the kind of mistake that seems obvious in hindsight but happens all the time" (real-world validation)

### Pause Points for Reflection
- After posing questions (database down scenarios)
- Before revealing answers to quiz questions
- After describing critical mistakes

---

## Success Criteria

Students should be able to:
- [ ] Explain the purpose of each probe type
- [ ] Configure appropriate timeouts and thresholds for production
- [ ] Distinguish between liveness and readiness check requirements
- [ ] Identify common misconfigurations from probe definitions
- [ ] Debug CrashLoopBackOff and NotReady states
- [ ] Design health endpoints that validate actual functionality
