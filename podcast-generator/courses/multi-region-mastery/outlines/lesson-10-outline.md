# Lesson Outline: Episode 10 - Data Consistency Models: CAP Theorem in Production

## Metadata
**Course**: Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale
**Episode**: 10 of 16
**Duration**: 15 minutes
**Episode Type**: Core Concept
**Prerequisites**: Episodes 1-9, understanding of distributed systems basics
**Template Used**: Template 2 (Core Concept)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. Explain CAP Theorem (Consistency, Availability, Partition Tolerance) and why you can only have two
2. Apply CAP tradeoffs to specific AWS services: Aurora (CP), DynamoDB (AP), S3 (AP)
3. Identify split-brain scenarios in multi-region architectures and prevention strategies
4. Design consistency strategies appropriate for each data type (transactions, user sessions, cache)

Success criteria:
- Can explain why Aurora Global Database is CP and DynamoDB Global Tables are AP
- Can identify split-brain risk in hot-hot architectures
- Can design appropriate consistency model for user data, transaction data, and cache data
- Can explain eventual consistency windows and their business implications

## Spaced Repetition Plan

**Concepts Introduced**:
- Split-brain scenarios (will detail in Episode 12 DR testing)
- Consistency windows (will apply in Episode 13 compliance requirements)

**Concepts Reinforced**:
- Aurora replication from Episode 3 (consistency guarantees)
- DynamoDB from Episode 6 (eventual consistency model)
- Cost tradeoffs from Episode 9 (consistency vs provisioning)

## Lesson Flow

### 1. Recall & Connection (1-2 min)

"You've built multi-region. Aurora replicating transactions between regions. DynamoDB Global Tables spreading reads and writes. But here's the uncomfortable question: When the regions diverge, which one is right?

Today you're learning CAP Theorem - and why it's the most important decision you'll make in multi-region architecture."

---

### 2. Learning Objectives (30 sec)

"By the end of this lesson:
- You'll understand CAP Theorem and why it's unavoidable
- You'll know which AWS services are which side of CAP
- You'll identify split-brain risks in your architecture
- You'll design consistency strategies for different data types"

---

### 3. CAP Theorem - The Fundamental Truth (3 min)

**Teaching Approach**: Explanation + analogy

"CAP Theorem says: In a distributed system, pick two of three:
- Consistency (all nodes see same data)
- Availability (system always responds)
- Partition Tolerance (system continues during network split)

You can't have all three. Ever. It's mathematics, not opinion."

**Why It Matters**:
"When US-EAST-1 and US-WEST-2 lose network connectivity, you must choose. Do you keep both regions running (availability) knowing they might diverge (consistency)? Or do you stop one region (consistency) knowing you lose availability?

This choice determines your entire multi-region strategy."

**The Three Positions**:

**CP (Consistency + Partition)**: "When regions split, keep one running, stop the other. All data stays consistent because only one region is alive. Aurora Global Database with manual failover = CP. You acknowledge the partition happened and fail over explicitly."

**AP (Availability + Partition)**: "When regions split, both keep running. Clients can always connect. But they might see different data. DynamoDB Global Tables = AP. Each region accepts writes independently. You resolve conflicts later."

**CA (Consistency + Availability)**: "Requires no network partitions. Not relevant for multi-region. Single-region databases are effectively CA."

**The Production Reality**:
"Network partitions WILL happen. You cannot choose CA. You must be either CP (Aurora) or AP (DynamoDB). Choose based on your data type, not what sounds nice."

---

### 4. Aurora Global Database - CP in Production (2 min)

**Teaching Approach**: Technical deep dive

"Aurora Global Database is CP. One writer in primary region. Secondary is read-only. During network partition, secondary stops accepting writes. Data stays consistent.

When partition heals or primary fails, secondary promotes to writer. No conflicts because there were never two writers."

**Cost of CP**:
- Write latency: You must write to primary (possibly cross-region)
- Failover time: Takes time to promote secondary
- Limited scale: Only primary region accepts writes

**When CP is Right**:
"Financial transactions. Customer accounts. Inventory. Anything where wrong data is worse than no data.

You accept write latency to guarantee consistency."

---

### 5. DynamoDB Global Tables - AP in Production (2 min)

**Teaching Approach**: Technical deep dive

"DynamoDB Global Tables is AP. Both regions accept writes independently. During network partition, both regions continue. Writes succeed locally and replicate asynchronously to other regions.

Conflict resolution: Last-write-wins timestamps. Both writes can succeed, latest one wins."

**Cost of AP**:
- Split brain: Regions can diverge temporarily
- Conflict resolution required: Last-write-wins isn't always correct
- Eventual consistency: Windows of inconsistency possible

**When AP is Right**:
"User session data. Shopping carts. Recommendations. Anything where slightly stale data is acceptable but availability is critical.

You accept eventual inconsistency to guarantee availability."

**Real Example**:
"User in California adds item to cart at 3 PM Pacific. User in Europe adds different item at 3 PM UTC (same clock time, different moment). DynamoDB writes both. Each region sees its write immediately, replicates after 40ms.

Net result: Both users get both items in their cart after replication. Not wrong, but unexpected. This is acceptable for shopping carts. Not acceptable for inventory count."

---

### 6. S3 - Tricky AP (1 min)

**Teaching Approach**: Special case explanation

"S3 is... complicated. It's AP with eventual strong consistency.

Within a region: Strong consistency (new writes visible immediately). Between regions: Eventually consistent (replication takes time).

For multi-region applications: Treat S3 as AP. Cross-region replication has windows where regions disagree."

---

### 7. Split-Brain Scenarios and Prevention (2 min)

**Teaching Approach**: Risk identification + mitigation

**The Risk**:
"When US-EAST-1 and US-WEST-2 lose connectivity, both regions believe they're healthy. If you're not careful, you can end up with two 'primary' instances making conflicting decisions."

**Real Scenario**:
"Hot-warm architecture. Primary US-EAST-1, secondary US-WEST-2. Network partition occurs. Health checks fail between regions. Route53 detects primary is unreachable. Failover routine promotes secondary.

But primary was actually healthy - just network partition. Now you have two primaries. Both accepting writes. Data diverges."

**Prevention Strategies**:

**1. Human approval for failover**: Require two senior engineers to approve failover. Verify true failure vs partition. Slower (adds 5-10 min) but prevents split-brain.

**2. Quorum-based decisions**: Need majority of systems to agree. With two regions: can't achieve quorum. Need three regions minimum. Three regions with quorum = safety.

**3. Fencing/Lease-based protection**: Primary region holds a lease. When lease expires, only then can secondary take over. Prevents both from being active.

**4. Witness/arbiter region**: Third region votes on who should be primary. Two regions can't have split-brain if third region is the tiebreaker.

---

### 8. Consistency Strategy by Data Type (1 min)

"Apply CAP based on data type:

**Strong Consistency Required**: Aurora CP. Financial transactions, inventory, authorizations. Write latency acceptable.

**Eventual Consistency Acceptable**: DynamoDB AP. User sessions, recommendations, analytics. Availability critical.

**Immutable/Reference Data**: S3 AP. Reference tables, historical data, logs. Replication latency irrelevant."

---

### 9. Active Recall (1 min)

"Pause and answer:
1. What does CAP Theorem say you can't have?
2. Is Aurora Global Database CP or AP? Why?
3. What's the split-brain risk in hot-hot architectures?

[PAUSE 5 seconds]

Answers:
1. All three: Consistency, Availability, Partition Tolerance. During network partition, you must sacrifice one.
2. CP. Primary region is sole writer. Secondary read-only. No conflicts because writes only happen in one region.
3. Both regions might accept writes simultaneously if they believe they're both primary. This requires fencing/quorum prevention or human approval."

---

### 10. Recap & Synthesis (1-2 min)

**Key Takeaways**:
1. **CAP Theorem is law**: Choose two, not three
2. **Aurora is CP**: Consistency guaranteed, partition tolerance accepted
3. **DynamoDB is AP**: Availability guaranteed, eventual consistency accepted
4. **Choose based on data type**: Not on what sounds nice
5. **Split-brain prevention is critical**: Require explicit failover approval or quorum

---

### 11. Next Episode Preview (30 sec)

"Next: Episode 11 - Multi-Region Kubernetes Patterns: Service Mesh & Federation.

You understand consistency models. Now: How do your applications actually talk across regions reliably? Service meshes, cluster federation, cross-region discovery. This is where Kubernetes becomes sophisticated."

---

## Quality Checklist

- [x] Prerequisites clear
- [x] Learning objectives measurable
- [x] CAP Theorem explained with clarity
- [x] Specific AWS services mapped to CAP positions
- [x] Real production scenario (shopping cart)
- [x] Split-brain risk identified and prevented
- [x] Decision framework (data type → consistency model)
- [x] Active recall included
