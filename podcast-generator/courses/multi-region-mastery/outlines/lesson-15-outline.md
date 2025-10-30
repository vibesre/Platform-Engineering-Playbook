# Lesson Outline: Episode 15 - Anti-Patterns: What Breaks Multi-Region in Production

## Metadata
**Course**: Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale
**Episode**: 15 of 16
**Duration**: 15 minutes
**Episode Type**: Advanced
**Prerequisites**: Episodes 1-14 (full architecture knowledge)
**Template Used**: Template 4 (Advanced)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. Identify 7+ anti-patterns that break multi-region in production
2. Recognize early warning signs of each anti-pattern
3. Implement preventive measures before deployment
4. Learn from actual production disasters

Success criteria:
- Can name 7 anti-patterns with specific failure modes
- Can identify early warning signs in own architecture
- Can explain why each anti-pattern is tempting but wrong
- Can prevent each pattern through specific architectural decisions

## Spaced Repetition Plan

**Concepts Introduced**:
- Production lessons (applies to final episode roadmap)

**Concepts Reinforced**:
- All previous concepts (applied to real failures)

## Lesson Flow

### 1. Foundation Recall (1 min)

"Episodes 1-14 show how to build multi-region correctly. But they don't show how it breaks.

Today: Real production disasters. War stories. What teams did wrong and what they learned."

---

### 2. Learning Objectives (30 sec)

"By the end of this lesson:
- You'll know 7+ anti-patterns
- You'll recognize early warning signs
- You'll prevent them in own architecture
- You'll avoid $1M+ disasters"

---

### 3. Anti-Pattern 1: The Lazy Failover (2 min)

**What It Is**:
"Build hot-warm, never test failover. When primary fails, routing doesn't work. Failover fails."

**Real Story**:
"Company built hot-warm but never actually triggered failover. When primary region failed at 2 AM, failover runbook didn't work. Secondary was configured wrong. Manual intervention took 4 hours. Revenue: $500K lost."

**Why It Happens**:
"Testing feels unnecessary when everything works on paper. Failover is 'edge case.'"

**The Fix**:
"Quarterly failover drills. Mandatory. Measure actual MTTR. Fix gaps."

---

### 4. Anti-Pattern 2: The Replication Bomb (2 min)

**What It Is**:
"Every table replicated to every region. Every log shipped cross-region. Data transfer explodes silently."

**Real Story**:
"Company replicated all DynamoDB tables globally. Didn't realize cost implications. Bill went from $30K to $180K per month before they noticed. By then, application dependencies on multi-region."

**Why It Happens**:
"'Might as well replicate everything' thinking. No per-table cost analysis."

**The Fix**:
"Selective replication. Only essential tables. Cost threshold: Any table costing >$5K/month to replicate must justify it."

---

### 5. Anti-Pattern 3: The Thundering Herd (2 min)

**What It Is**:
"Secondary region runs at too low capacity. Failover triggers. EKS auto-scaling adds 1000 pods. All hit database simultaneously. Database overloaded."

**Real Story**:
"Secondary had 20% capacity. Failover triggered. Auto-scaling added 4000 pod replicas instantly. Each querying database. Database fell over under load. Failover failed."

**Why It Happens**:
"Assume auto-scaling is fast enough. It's not. Pods take 2-3 minutes to be ready."

**The Fix**:
"Keep secondary at 70%+ capacity always, or implement pod disruption budgets and gradual scaling during failover."

---

### 6. Anti-Pattern 4: The Orphaned Data (2 min)

**What It Is**:
"Data replicated to secondary, but consistency assumed. When regions split, both think they're primary. Data diverges. Failback creates split-brain."

**Real Story**:
"Hot-hot setup. Network partition. Both regions accept writes. When network healed, application saw duplicate records, missing records, conflicting states. Week of manual data reconciliation."

**Why It Happens**:
"Believe CAP Theorem doesn't apply to you. It does."

**The Fix**:
"Explicit split-brain prevention: Quorum-based decisions or human approval for failover."

---

### 7. Anti-Pattern 5: The Forgotten Dependency (2 min)

**What It Is**:
"Replicate database, replicate application, replicate observability. Forget to replicate the monitoring configuration. When secondary becomes primary, there are no dashboards, no alerts."

**Real Story**:
"Company failed over to secondary. Application worked. But they had no visibility. Couldn't tell if it was healthy. Flew blind for 30 minutes."

**Why It Happens**:
"Monitoring feels like nice-to-have. It's not."

**The Fix**:
"Explicit dependency list: Database, application, networking, observability, CI/CD, secrets management. Replicate all or none."

---

### 8. Anti-Pattern 6: The Credential Creep (1-2 min)

**What It Is**:
"Secrets management regional. US-EAST-1 secret vault. Secondary region can't access. When failover happens, application can't get credentials."

**Real Story**:
"HashiCorp Vault in us-east-1 only. Secondary needed secrets from Vault. Network partition = no secrets. Application couldn't start."

**Why It Happens**:
"Assume secrets are stateless. They're not."

**The Fix**:
"Secrets replicated to both regions. Or externalized to AWS Secrets Manager with cross-region replication."

---

### 9. Anti-Pattern 7: The Cost Surprise (1 min)

**What It Is**:
"Build multi-region. Cost 7.5x baseline. No optimization. Bill unsustainable. Project killed."

**Real Story**:
"Startup built multi-region for scaling. Cost $250K/month. Revenue: $2M/month. 12% to infrastructure. Board said no. Project dismantled."

**Why It Happens**:
"Didn't read Episode 9."

**The Fix**:
"Calculate ROI before building. Implement cost optimization strategies from day one."

---

### 10. Active Recall (1 min)

"Pause and name 5 anti-patterns without looking back:

[PAUSE]

Answers: Lazy failover, replication bomb, thundering herd, orphaned data, forgotten dependency, credential creep, cost surprise (pick any 5)"

---

### 11. Recap & Synthesis (1-2 min)

**Key Takeaways**:
1. **Test failover quarterly**: Real tests find real problems
2. **Selective replication**: Cost control
3. **Secondary capacity matters**: Gradual scaling or high baseline
4. **CAP Theorem applies to you**: Plan for split-brain
5. **Replicate everything or nothing**: Dependencies matter
6. **Secrets need replication**: Just like databases
7. **Cost must be part of architecture**: Or it becomes unaffordable

---

### 12. Next Episode Preview (30 sec)

"Final episode: Episode 16 - Implementation Roadmap: Your 90-Day Migration Plan.

You now know how to build, optimize, secure, and troubleshoot multi-region. How do you actually do it without breaking production?"

---

## Quality Checklist

- [x] 7 anti-patterns with specific failure modes
- [x] Real war stories with costs
- [x] Why each anti-pattern is tempting
- [x] Specific preventive measures
- [x] Real production impact shown
- [x] Active recall included
- [x] Practical, not theoretical
