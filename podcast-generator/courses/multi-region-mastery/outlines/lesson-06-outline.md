# Lesson Outline: Episode 6 - DynamoDB Global Tables: Active-Active Data Replication

## Metadata
**Course**: Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale
**Episode**: 6 of 16
**Duration**: 15 minutes
**Episode Type**: Core Concept
**Prerequisites**: Episodes 1-5, Basic understanding of DynamoDB, Understanding of Aurora Global Database from Episode 3
**Template Used**: Template 2 (Core Concept Lesson)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. Explain how DynamoDB Global Tables achieve active-active replication with sub-second lag across regions
2. Design conflict resolution strategies for multi-region writes (last-writer-wins vs custom resolution)
3. Decide when to use DynamoDB over Aurora based on access patterns, consistency requirements, and cost
4. Calculate the hidden costs of Global Tables that can reach $25K+ monthly for high-traffic applications

Success criteria:
- Can explain the difference between active-passive (Aurora) and active-active (DynamoDB) replication
- Can design conflict resolution for concurrent writes to the same item
- Can choose between Aurora and DynamoDB based on workload characteristics
- Can estimate DynamoDB Global Tables costs accurately (including replication, WCUs, RCUs)

## Spaced Repetition Plan

**Concepts Introduced** (will be repeated in later episodes):
- Active-active replication model - Will reinforce in Episode 10 (Data Consistency Models)
- Conflict resolution strategies - Will reinforce in Episode 10 (CAP theorem)
- DynamoDB cost model - Will reinforce in Episode 9 (Cost Management)

**Concepts Reinforced** (from previous episodes):
- Aurora active-passive from Episode 3 - Contrast with DynamoDB active-active
- Hot-warm vs hot-hot patterns from Episode 2 - Show where DynamoDB enables hot-hot
- Network architecture from Episode 5 - Global Tables replicate over these networks
- CCC Triangle from Episode 1 - DynamoDB trades cost for capability

## Lesson Flow

### 1. Recall & Connection (1-2 min)

**Active Recall Prompt**:
"Let's build on what you've learned. Pause and try to remember: In Episode 3, how does Aurora replicate across regions? And can both regions accept writes?"

[PAUSE 3 seconds]

**Answers & Connection**:
"Aurora: Storage-layer replication, 45-85ms lag, active-passive. Only the primary accepts writes. Secondary is read-only until promoted.

This works great for hot-warm. But what if you need hot-hot? What if you need US-EAST-1 AND US-WEST-2 both accepting writes simultaneously?

Aurora can't do this. The primary writer is in one region. You can't write to the secondary without promoting it first.

Today you're learning about DynamoDB Global Tables - active-active replication where every region accepts writes. This is fundamentally different from everything we've covered so far."

**Today's Focus**:
"By the end of this lesson, you'll understand how DynamoDB achieves multi-region writes, how to handle conflicts when two regions write to the same item, and most importantly - when this is worth the cost and complexity."

---

### 2. Learning Objectives (30 sec)

"What you'll master today:
- How DynamoDB Global Tables achieve active-active replication with sub-second lag
- Conflict resolution strategies when two regions write simultaneously
- When to use DynamoDB over Aurora (and critically, when NOT to)
- The hidden costs that can hit twenty-five thousand dollars monthly"

---

### 3. Active-Active Replication Model (2-3 min)

**Teaching Approach**: Contrast with Aurora, concrete scenario

**The Fundamental Difference**:
"Aurora: One writer, one reader. Active-passive.
DynamoDB Global Tables: Multiple writers, multiple readers. Active-active.

This changes everything."

**Concrete Scenario**:
"Picture a global gaming application. Players in US-EAST-1 and EU-WEST-1 simultaneously. Player in New York updates their score. Player in London updates their inventory. Both writes happen at the same moment to different items in the same table.

With Aurora: You'd need to route all writes to US-EAST-1. The London player's write has to travel across the Atlantic, hit US-EAST-1 Aurora primary, then replicate back. That's 150-200ms round trip. For a real-time game, that's noticeable lag.

With DynamoDB Global Tables: The London player writes to EU-WEST-1. The New York player writes to US-EAST-1. Both writes succeed locally in ~10-20ms. Then DynamoDB replicates asynchronously in the background. Sub-second replication (typically 1-3 seconds)."

**How It Actually Works**:
- Create DynamoDB table in primary region
- Enable Global Tables, add replica regions
- Every region becomes a full replica with read/write capability
- Writes go to local region (low latency)
- DynamoDB replicates to other regions asynchronously
- Uses last-writer-wins conflict resolution by default

**Key Architecture Points**:
- Each region has complete copy of data
- Writes are local (fast)
- Replication is asynchronous (eventual consistency)
- No primary/secondary distinction - all regions equal
- Replication lag: typically 1-3 seconds (not 45-85ms like Aurora, but acceptable for many workloads)

**Why Replication is Slower Than Aurora**:
"Aurora: 45-85ms because it's shipping minimal redo logs at storage layer.
DynamoDB: 1-3 seconds because it's replicating full items at application layer.

But you get multi-region writes. That's the trade-off."

---

### 4. The Conflict Problem (3-4 min)

**Teaching Approach**: Real failure scenario, then solutions

**The Scenario That Breaks Everything**:
"Here's where active-active gets tricky.

User updates their profile in US-EAST-1: Set email to 'new@email.com'
Same user, same moment, updates profile in US-WEST-2: Set email to 'different@email.com'

Both writes succeed locally. Both regions think they have the correct value.

Now DynamoDB replicates. US-EAST-1 sends 'new@email.com' to US-WEST-2. US-WEST-2 sends 'different@email.com' to US-EAST-1.

Which value wins?

This is the conflict resolution problem. And getting it wrong causes data corruption."

**Solution 1: Last-Writer-Wins (Default)**:
"DynamoDB uses timestamp-based conflict resolution. Each write gets a timestamp. When conflicts occur, the write with the latest timestamp wins.

In our example: If US-EAST-1 write happened at 10:00:00.100 and US-WEST-2 write happened at 10:00:00.150, US-WEST-2 wins. 'different@email.com' becomes the final value in both regions.

Advantages:
- Automatic, no custom logic required
- Deterministic (same conflict always resolves same way)
- No application changes needed

Limitations:
- Clock skew between regions can cause wrong winner
- Lost updates - one write gets silently discarded
- No way to preserve both values"

**Clock Skew Problem**:
"AWS synchronizes clocks via NTP, but they can drift. If US-EAST-1 clock is 2 seconds ahead of US-WEST-2 clock, US-EAST-1 writes always win even if they happened second. This causes subtle data loss that's hard to debug."

**Solution 2: Application-Level Conflict Resolution**:
"Don't let conflicts happen in the first place. Design your data model to avoid them.

Strategy 1 - Partition by region:
User data lives in their home region. Users don't roam between regions mid-session. No conflicts because each user only writes to their home region.

Strategy 2 - Merge semantics:
Instead of overwriting, merge. For a shopping cart, append items rather than replacing the entire cart. Use DynamoDB's atomic increment for counters.

Strategy 3 - Read-modify-write with version checks:
Read current version number. Modify data. Write with expected version. If version changed, retry. This detects conflicts and lets application decide what to do."

**Real Production Pattern**:
"E-commerce with global customers:
- User's 'home region' is where they registered
- Shopping cart updates go to home region (sticky sessions from Episode 4)
- Inventory and catalog replicated globally (read-only from user perspective, updated by backend)
- Orders write to home region, replicate globally for fulfillment

This design minimizes cross-region conflicts while still providing global access."

---

### 5. DynamoDB vs Aurora: Decision Framework (3-4 min)

**Teaching Approach**: Comparison table, decision tree

**When to Use DynamoDB Global Tables**:
"Use DynamoDB when:
- You need active-active writes across regions (hot-hot pattern)
- Access patterns are key-value or single-item lookups (DynamoDB strength)
- You can tolerate eventual consistency (1-3 second lag acceptable)
- You need unlimited scale (DynamoDB auto-scales to millions of requests/sec)
- Your data model fits NoSQL (denormalized, no complex joins)"

**Real Use Cases**:
- Session stores (user sessions read/written globally)
- Gaming leaderboards (players update scores globally)
- IoT device state (devices send data from anywhere)
- Shopping carts (users shop from any region)
- User preferences/settings (low-conflict profile data)

**When to Use Aurora Global Database**:
"Use Aurora when:
- You need relational data model (complex queries, joins, transactions)
- You're okay with active-passive (hot-warm is sufficient)
- You need strong consistency (not eventual)
- Your access patterns require SQL flexibility
- You want lower replication lag (45-85ms vs 1-3 seconds)"

**Real Use Cases**:
- Order management (transactional integrity required)
- Financial records (strong consistency critical)
- Inventory systems (ACID transactions needed)
- User authentication (relational user/role/permission data)

**The Cost Trap**:
"This is where DynamoDB gets expensive fast. Aurora pricing is predictable: instance cost plus storage plus data transfer. DynamoDB pricing scales with traffic: Write Capacity Units (WCUs) and Read Capacity Units (RCUs) multiplied by number of regions.

Example calculation:
- Application writes 1,000 items/sec, reads 5,000 items/sec
- Each item 1 KB
- 3 regions (US-EAST-1, US-WEST-2, EU-WEST-1)

Writes: 1,000 WCUs/sec in each region (because all regions accept writes)
Reads: 5,000 RCUs/sec in each region
Replication: 1,000 WCUs × 2 (replicating to 2 other regions)

Total per region:
- 1,000 WCUs for application writes = $6,000/month
- 2,000 WCUs for replication writes = $12,000/month
- 5,000 RCUs for reads = $3,000/month
- Storage: 100 GB × $0.25 = $25/month

Per region: $21,025/month
Three regions: $63,075/month

Aurora equivalent: ~$5,000-8,000/month for comparable scale.

The DynamoDB cost is 8-10x higher. You're paying for auto-scaling, zero-admin, and active-active capability."

---

### 6. Cost Optimization Strategies (1-2 min)

**Teaching Approach**: Practical techniques

**Strategy 1: On-Demand vs Provisioned**:
"On-demand: Pay per request, no capacity planning. Good for unpredictable traffic.
Provisioned: Reserve capacity, get discounts. Good for steady traffic.

For global tables, provisioned can save 50% if traffic is predictable."

**Strategy 2: Read Replicas Without Writes**:
"Not all regions need to accept writes. Make some regions read-only for cost savings. Application routes writes to primary region, reads go local."

**Strategy 3: TTL for Ephemeral Data**:
"Session data, temporary state - use Time-To-Live to auto-delete. Reduces storage and replication costs."

**Strategy 4: Right-Size Items**:
"WCU = bytes / 1KB (rounded up). A 1.5 KB item costs 2 WCUs. A 1.0 KB item costs 1 WCU. Optimize item size to stay under 1 KB boundaries."

---

### 7. Common Mistakes (1-2 min)

**Mistake 1: Treating Global Tables Like Single-Region**:
- What: Assume strong consistency across regions
- Reality: Eventual consistency, 1-3 second lag
- Fix: Design for eventual consistency, use version checks

**Mistake 2: Not Planning for Conflicts**:
- What: Use default last-writer-wins without understanding implications
- Reality: Silent data loss, wrong values persisting
- Fix: Design data model to minimize conflicts, use merge semantics

**Mistake 3: Cost Blindness**:
- What: Enable Global Tables without calculating replication costs
- Reality: $60K/month bills for high-traffic tables
- Fix: Calculate WCUs including replication multiplier, use provisioned capacity

**Mistake 4: Using DynamoDB When Aurora Would Work**:
- What: Choose DynamoDB for hot-warm pattern (only need active-passive)
- Cost: Paying 8-10x more for capability you don't need
- Fix: Use Aurora for hot-warm, DynamoDB only for hot-hot

---

### 8. Active Recall Moment (1 min)

**Retrieval Prompt**:
"Before we wrap up, pause and answer:
1. What's the key difference between Aurora Global Database and DynamoDB Global Tables in terms of write capability?
2. Your application writes 500 items/sec with 2 KB items. You have 2 regions. How many WCUs needed per region?
3. When would you use DynamoDB over Aurora?"

[PAUSE 5 seconds]

**Answers**:
"1. Aurora: Active-passive. Only primary accepts writes. DynamoDB: Active-active. All regions accept writes simultaneously.

2. Each 2 KB item needs 2 WCUs (rounded up from 1 KB). 500 items/sec × 2 WCUs = 1,000 WCUs for application writes. Plus 500 WCUs replication to the other region. Total: 1,500 WCUs per region.

3. Use DynamoDB when you need hot-hot active-active writes, can tolerate eventual consistency, have key-value access patterns, and need unlimited auto-scaling. Don't use if you need relational model, strong consistency, or can get by with hot-warm (Aurora is cheaper)."

---

### 9. Recap & Synthesis (1-2 min)

**Key Takeaways**:
1. **Active-active replication**: DynamoDB Global Tables allow writes in all regions simultaneously. Aurora only allows writes in primary.
2. **Conflict resolution**: Default is last-writer-wins based on timestamp. Application-level resolution is better - design to avoid conflicts.
3. **Replication lag**: 1-3 seconds typical (slower than Aurora's 45-85ms) but acceptable for many use cases.
4. **Cost multiplier**: Replication adds N-1 WCUs per region where N is region count. 3 regions = 2x replication cost.
5. **Use cases**: Hot-hot patterns, key-value workloads, eventual consistency acceptable. Don't use for hot-warm (Aurora cheaper) or relational data (Aurora better fit).

**Connection to Bigger Picture**:
"Remember Episode 2? Hot-hot pattern with subsecond RTO? DynamoDB Global Tables is how you implement that for NoSQL workloads. But it costs 8-10x more than Aurora hot-warm. The CCC Triangle from Episode 1: you're trading cost for capability.

Episodes 3-6 gave you the data layer options:
- Aurora Global Database: Active-passive, relational, 45-85ms lag, $5-8K/month
- DynamoDB Global Tables: Active-active, NoSQL, 1-3s lag, $25-60K/month

Choose based on your actual requirements, not aspirational architecture."

**Spaced Repetition**:
"We'll revisit DynamoDB costs in Episode 9 (Cost Management) with optimization strategies. In Episode 10 (Data Consistency Models), we'll explore the CAP theorem and why DynamoDB chose availability over consistency. And in Episode 15 (Anti-Patterns), we'll see what happens when teams use Global Tables wrong."

---

### 10. Next Episode Preview (30 sec)

"Next time: Observability at Scale - Centralized logging and distributed tracing.

You've got Aurora replicating data. DynamoDB replicating data. EKS clusters running workloads. Network layer connecting everything.

How do you troubleshoot when things break? When a request fails, which region was it in? Which service failed? How do you trace a request across regions?

You'll learn:
- Centralized logging with CloudWatch Logs Insights and S3
- Distributed tracing with X-Ray for multi-region request paths
- Cross-region metrics aggregation and alerting
- The observability patterns that prevented 2 AM pages

Because multi-region without observability is flying blind. When production breaks, you need to know where and why - fast.

See you in Episode 7."

---

## Supporting Materials

**Technical References**:
- DynamoDB Global Tables Documentation: Replication behavior, conflict resolution
- DynamoDB Pricing Calculator: WCU/RCU costs with replication
- Aurora vs DynamoDB Comparison: Access patterns, consistency models

**Analogies to Use**:
- Active-active: Multiple bank branches accepting deposits simultaneously (vs active-passive: one branch open, others closed)
- Last-writer-wins: Auction where latest bid wins (clock skew = someone's clock running fast)
- Conflict resolution: Merge vs overwrite (Git merge vs force push)

**Cost Calculations**:
- WCU formula: Bytes / 1KB (rounded up)
- Replication multiplier: (N-1) where N = region count
- Example breakdowns for 2, 3, 5 region deployments

---

## Quality Checklist

**Structure**:
- [x] Clear beginning, middle, end
- [x] Logical flow (Aurora comparison → active-active → conflicts → decision framework → costs)
- [x] Time allocations realistic (total 15 min)
- [x] All sections have specific content

**Pedagogy**:
- [x] Learning objectives specific and measurable
- [x] Spaced repetition integrated (Aurora, hot-warm/hot-hot, network callbacks)
- [x] Active recall moment included
- [x] Signposting throughout
- [x] Multiple analogies (bank branches, auction, Git merge)
- [x] Common pitfalls addressed

**Content**:
- [x] Addresses real production patterns
- [x] Decision frameworks (Aurora vs DynamoDB)
- [x] Cost calculations with real numbers
- [x] Conflict resolution strategies
- [x] Appropriate depth for senior engineers

**Engagement**:
- [x] Strong hook (contrast with Aurora limitations)
- [x] Real production example (gaming, e-commerce)
- [x] Practice moment (cost calculations)
- [x] Preview builds anticipation (observability)
