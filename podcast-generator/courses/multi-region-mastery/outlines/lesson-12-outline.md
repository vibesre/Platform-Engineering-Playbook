# Lesson Outline: Episode 12 - Disaster Recovery: Failover Procedures & Chaos Engineering

## Metadata
**Course**: Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale
**Episode**: 12 of 16
**Duration**: 15 minutes
**Episode Type**: Core Concept
**Prerequisites**: Episodes 1-11 (entire architecture)
**Template Used**: Template 2 (Core Concept)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. Design repeatable failover procedures with clear decision points
2. Implement chaos engineering tests for multi-region architecture
3. Identify failure points that break your hot-warm/hot-hot setup
4. Calculate mean time to recovery (MTTR) in production

Success criteria:
- Can write runbook with clear failover steps
- Can design chaos test that breaks something real
- Can identify 5+ failure scenarios in own architecture
- Can measure actual MTTR vs theoretical RTO

## Spaced Repetition Plan

**Concepts Introduced**:
- Chaos engineering testing (will apply in Episode 14 security testing)

**Concepts Reinforced**:
- Route53 failover from Episode 8 (actually executing)
- CAP consistency from Episode 10 (split-brain during failure)
- Service mesh from Episode 11 (mesh behavior during failure)

## Lesson Flow

### 1. Recall & Connection (1-2 min)

"You've built everything: Aurora, DynamoDB, networking, DNS failover, service mesh. On paper, you can survive entire region failure.

But have you actually tested it? [pause long] Most companies haven't. When real failure happens, their runbook breaks.

Today: How to actually test and validate your multi-region setup."

---

### 2. Learning Objectives (30 sec)

"By the end of this lesson:
- You'll design failover procedures that actually work
- You'll set up chaos engineering to find weaknesses
- You'll measure real vs theoretical RTO
- You'll know the 5 failure scenarios that break multi-region"

---

### 3. Failover Procedures - The Runbook (3 min)

**Teaching Approach**: Step-by-step runbook design

**Components**:
1. **Detection phase**: How do we know primary region failed?
2. **Validation phase**: Is it really failed or network partition?
3. **Decision phase**: Approve failover or hold?
4. **Execution phase**: Actually promote secondary
5. **Verification phase**: Is secondary now healthy?
6. **Rollback phase**: How do we reverse if we made wrong decision?

**Real Runbook Example**:

```
## Failover Runbook

### Phase 1: Detection (Automatic)
- Route53 health checks fail 3x (90 seconds)
- Alarm triggers in PagerDuty
- On-call engineer gets paged

### Phase 2: Validation (Manual)
- Engineer checks AWS console: Is us-east-1 truly down?
- Checks CloudWatch: Application errors or infrastructure issue?
- Checks Status Page: Is this AWS-wide or regional?
- Decision point: Proceed or investigate further?

### Phase 3: Approval (Manual with 2 engineers)
- Engineer 1 initiates failover approval request
- Engineer 2 approves (requires 2 to prevent mistakes)
- Both acknowledge risk: Data between health check and failover lost

### Phase 4: Execution (Automated after approval)
- Promote Aurora Global Database secondary to writer
  - Command: AWS RDS modify-db-cluster
  - Timeout: 2 minutes
- Update Route53 to stop health checks on us-east-1
- Trigger EKS secondary scaling (20% to 100%)
- Notify customers via status page

### Phase 5: Verification (Manual)
- Verify Aurora promotion successful
- Verify applications in us-west-2 healthy
- Verify customer traffic routing to us-west-2
- Monitor error rates for 5 minutes

### Phase 6: Rollback (If needed)
- If us-east-1 recovers: Don't automatically failback
- Wait 30 minutes to ensure stability
- Plan maintenance window for failback
- Demote us-west-2 secondary, promote us-east-1
```

---

### 4. Chaos Engineering - Breaking Your Setup (3-4 min)

**Teaching Approach**: Testing methodology

**Types of Tests**:

**1. Network partition**:
"Block traffic between regions. What happens? Services timeout? Data gets inconsistent?"

**2. Database failover**:
"Force Aurora failover in middle of load test. Do clients recover?"

**3. Service mesh failure**:
"Kill service mesh. Does traffic still route?"

**4. DNS failure**:
"Return wrong IP from Route53. How long until detected?"

**5. Load test during failover**:
"Heavy load + simultaneous failover. What breaks first?"

**Execution**:
"Run these quarterly, escalating severity:
- Month 1: Kill one pod. Does liveness detect it?
- Month 2: Kill availability zone. Does app recover?
- Month 3: Network partition. Does failover work?
- Month 4: Coordinated failure (AZ + database). Full failover test."

**Measuring Results**:
"Record actual MTTR vs theoretical RTO.
Theoretical RTO (from Episode 2): 5 minutes
Actual RTO (from chaos test): Maybe 7-8 minutes
Gap: 2-3 minutes. Why? Investigate. Fix."

---

### 5. Five Failure Scenarios That Break Multi-Region (2 min)

**1. Cascading failures**:
"Failure in one service cascades to others. Load increases on secondary region. Secondary can't handle it. Entire system goes down."

**Prevention**: Circuit breakers, bulkheads, graceful degradation.

**2. Database replication lag**:
"US-EAST-1 fails with 45 seconds of unreplicated writes. Secondary loses data. Customers see missing information."

**Prevention**: Accept data loss as cost of failover. Document it.

**3. DNS cache inconsistency**:
"Some users' DNS resolvers cache old IP. They keep hitting failed primary. Recovery takes hours."

**Prevention**: Lower TTL. Use Global Accelerator. Monitor cache behavior.

**4. Failback split-brain**:
"You fail back to primary while it's half-recovered. Two primaries fighting."

**Prevention**: Automatic failback disabled. Manual process only.

**5. Operator error**:
"Wrong region promoted. Wrong data deleted. Wrong load balancer updated."

**Prevention**: Runbooks with explicit checkpoints. Two-person approval. Dry-runs quarterly.

---

### 6. Measuring Real RTO (1 min)

"Your theoretical RTO: 5 minutes (health check + promotion + DNS).
Your actual RTO: Time from failure start to first successful user request.

Measure in chaos test:
- Start: Kill primary region
- End: First request succeeds in secondary
- Record: Actual seconds
- Gap: Why is actual different from theoretical?

Example: Theoretical 5 min, actual 7.5 min = 2.5 min unexplained. Probably DNS cache or auto-scaling lag. Investigate and fix."

---

### 7. Active Recall (1 min)

"Pause:
1. What are the 6 phases of a failover runbook?
2. Why do you need chaos engineering if you have hot-warm?
3. What's the difference between theoretical and actual RTO?

[PAUSE]

Answers:
1. Detection, validation, approval, execution, verification, rollback
2. Because actual systems break in ways your theory doesn't predict
3. Theoretical = how long failover should take. Actual = how long it actually takes in real test. Gap reveals problems."

---

### 8. Recap & Synthesis (1-2 min)

**Key Takeaways**:
1. **Runbooks prevent operator error**: Clear steps, decision points, approvals
2. **Chaos engineering finds real problems**: Theory ≠ practice
3. **Quarterly escalating severity tests**: Build confidence in system
4. **Measure actual vs theoretical RTO**: Fix gaps
5. **Multi-region fails in unexpected ways**: Plan for it

---

### 9. Next Episode Preview (30 sec)

"Next: Episode 13 - Financial Services Compliance: SEC SCI, MiFID II, Crypto.

If you're in regulated industry, your multi-region architecture must meet compliance. And compliance sometimes conflicts with technical elegance."

---

## Quality Checklist

- [x] Runbook specific and detailed
- [x] Chaos engineering approach systematic
- [x] Five failure scenarios with prevention
- [x] Real vs theoretical RTO comparison
- [x] Quarterly testing plan included
- [x] Decision points explicit
- [x] Active recall included
