# Lesson Outline: Episode 5 - Network Architecture: Transit Gateway, VPC Peering, and PrivateLink

## Metadata
**Course**: Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale
**Episode**: 5 of 16
**Duration**: 15 minutes
**Episode Type**: Core Concept
**Prerequisites**: Episodes 1-4, AWS VPC networking fundamentals, Understanding of subnets and routing tables
**Template Used**: Template 2 (Core Concept Lesson)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. Explain when to use Transit Gateway versus VPC Peering, and why Transit Gateway scales beyond 100+ VPC connections
2. Design network topology that avoids hidden bottlenecks like bandwidth limits and routing table explosion
3. Implement PrivateLink for secure cross-region service access without exposing traffic to the internet
4. Calculate cross-region data transfer costs that can add $5K-$50K monthly to multi-region architectures

Success criteria:
- Can choose appropriate networking solution based on requirements (Transit Gateway vs VPC Peering vs PrivateLink)
- Can identify network topology mistakes before they cause production outages
- Can estimate data transfer costs accurately for multi-region traffic patterns
- Can design secure cross-region connectivity without internet exposure

## Spaced Repetition Plan

**Concepts Introduced** (will be repeated in later episodes):
- Transit Gateway hub-and-spoke model - Will reinforce in Episode 8 (DNS/Traffic Management), Episode 12 (Disaster Recovery)
- Cross-region data transfer costs - Will reinforce in Episode 9 (Cost Management)
- PrivateLink for secure connectivity - Will reinforce in Episode 14 (Security Architecture)

**Concepts Reinforced** (from previous episodes):
- Aurora Global Database from Episode 3 - Show how Aurora data replicates over these networks
- EKS independent clusters from Episode 4 - Show how clusters communicate via these networks
- Hot-warm pattern from Episode 2 - Apply network design to 5-minute RTO architecture
- CCC Triangle from Episode 1 - Network complexity trades off with capability and cost

## Lesson Flow

### 1. Recall & Connection (1-2 min)

**Active Recall Prompt**:
"Let's connect to what we've built. Pause and try to remember: In Episode 3, how does Aurora replicate data between regions? And in Episode 4, how do independent EKS clusters coordinate?"

[PAUSE 3 seconds]

**Answers & Connection**:
"Aurora: Storage layer ships redo logs across regions. 45-85ms lag includes network latency. EKS: Independent clusters coordinate at infrastructure level - Aurora for data, DNS for traffic, CI/CD for deployments.

But here's what we haven't answered: HOW do they communicate? What network paths do Aurora redo logs take? When your frontend pod in US-EAST-1 calls an API in US-WEST-2, what actually happens?

Today you're learning the network layer. This is the foundation everything else runs on. Get this wrong, and your entire multi-region architecture breaks."

**Today's Focus**:
"By the end of this lesson, you'll know exactly how to connect your multi-region infrastructure without creating hidden bottlenecks or burning cash on data transfer."

---

### 2. Learning Objectives (30 sec)

"What you'll master today:
- When to use Transit Gateway versus VPC Peering, and why Transit Gateway scales
- PrivateLink for secure cross-region service access without internet exposure
- How to design network topology that doesn't create hidden bottlenecks
- The network layer mistakes that killed multi-region projects - and cost $50K+ in unexpected data transfer charges"

---

### 3. The Network Problem Nobody Explains (2-3 min)

**Teaching Approach**: Problem setup with concrete scenario

**The Reality**:
"You've got Aurora in US-EAST-1 and US-WEST-2. You've got EKS clusters in both regions. They're running in separate VPCs. How do they talk?

They can't. Not yet. VPCs are isolated by default. Your Aurora primary in US-EAST-1 VPC can't send redo logs to Aurora secondary in US-WEST-2 VPC. Your EKS pod in one region can't reach services in another region.

You have three options:
1. Public internet (terrible idea - security nightmare, high latency, unpredictable)
2. VPC Peering (direct connection between two VPCs)
3. Transit Gateway (hub-and-spoke connecting many VPCs)
4. PrivateLink (private service endpoints)

The choice determines your scalability, cost, and operational complexity."

**Why This Matters**:
"Wrong network design causes:
- 200ms+ latency spikes (killing your 5-minute RTO)
- $50K/month surprise data transfer bills
- Security exposure (traffic over public internet)
- Routing table limits that break production
- Cross-region bandwidth bottlenecks"

**Hook Example**:
"E-commerce company built hot-warm with VPC Peering. Started with 4 VPCs: primary/secondary in two regions. Simple. Two years later: 40 VPCs (different business units, services, environments). VPC Peering requires N*(N-1)/2 connections. 40 VPCs = 780 peering connections. Each VPC has 125 route table entry limit. They hit the limit. Production broke. Transit Gateway would have cost $300/month. The outage cost $200K."

---

### 4. VPC Peering: Simple But Doesn't Scale (2-3 min)

**Teaching Approach**: Explanation with math demonstration

**What It Is**:
"Direct network connection between two VPCs. Point-to-point. Your US-EAST-1 VPC connects to US-WEST-2 VPC. Traffic flows directly between them. Private IPs work. No internet gateway needed."

**How It Works**:
- One-to-one connection between VPCs
- Can be same region or cross-region
- Traffic never touches public internet
- Low latency (~15ms cross-region for US-EAST-1 to US-WEST-2)
- Charged per GB transferred: $0.02/GB cross-region

**Advantages**:
- Simple setup (AWS console, a few clicks)
- Low latency (direct connection)
- No additional per-hour costs (just data transfer)
- Good for small deployments (2-4 VPCs)

**The Math That Breaks You**:
"2 VPCs: 1 peering connection. Easy.
4 VPCs: 6 peering connections. Still manageable.
10 VPCs: 45 peering connections. Getting messy.
20 VPCs: 190 peering connections. Good luck managing that.
40 VPCs: 780 peering connections. Production outage territory.

Formula: N*(N-1)/2 where N is VPC count.

Each peering connection adds routes to your route tables. VPC route table limit: 125 entries. Hit that limit? Traffic stops routing. Services fail. Your multi-region architecture is down."

**When to Use**:
- Small deployments (≤4 VPCs)
- Simple architectures (primary + secondary regions, minimal services)
- Cost-sensitive (no per-hour charges)
- You know VPC count won't grow significantly

**Real Numbers**:
"Data transfer: $0.02/GB cross-region. If Aurora replicates 100GB/day: $2/day = $60/month. Not terrible. But if you're replicating 1TB/day: $20/day = $600/month just for data transfer. This adds up."

---

### 5. Transit Gateway: Hub-and-Spoke That Scales (3-4 min)

**Teaching Approach**: Comparison with visual description and cost analysis

**What It Is**:
"Think of it like an airport hub. Instead of direct flights between every city (VPC Peering), you route through a central hub. Transit Gateway is that hub. All VPCs connect to Transit Gateway. Transit Gateway routes traffic between them.

N VPCs = N connections (not N*(N-1)/2). 40 VPCs? 40 connections. 100 VPCs? 100 connections. Linear scaling."

**How It Works**:
- Create Transit Gateway (one per region)
- Attach VPCs to Transit Gateway
- Transit Gateway handles routing between VPCs
- Can peer Transit Gateways across regions
- Centralized control plane

**Architecture**:
"US-EAST-1 Transit Gateway connects:
- Production VPC
- Staging VPC
- Monitoring VPC
- Data VPC

US-WEST-2 Transit Gateway connects:
- Production VPC
- Staging VPC
- Monitoring VPC
- Data VPC

Transit Gateway Peering connects US-EAST-1 TGW to US-WEST-2 TGW. Cross-region traffic flows: VPC → TGW → TGW Peering → TGW → VPC."

**Advantages**:
- Scales linearly (N connections not N^2)
- Centralized routing control
- No route table limit issues
- Supports transitive routing
- Can route between VPCs, VPNs, Direct Connect
- Multi-region peering built-in

**Costs**:
"Transit Gateway: $0.05/hour per attachment = $36/month per VPC attached.
10 VPCs attached: $360/month base cost.
Plus data transfer: $0.02/GB cross-region (same as VPC Peering).

VPC Peering: $0/hour base cost, just data transfer.

Crossover point: If you have more than 3-4 VPCs, Transit Gateway operational simplicity justifies the cost."

**Performance**:
"Bandwidth: Up to 50 Gbps per VPC attachment. Enough for most workloads.
Latency: Adds ~1-2ms compared to VPC Peering (negligible for most use cases).
Burst capacity: 100+ Gbps aggregate across all attachments."

**When to Use**:
- More than 4-5 VPCs
- Growth expected (add business units, services, environments)
- Need centralized routing control
- Multi-region architecture with many services
- Transitive routing required (VPC A → VPC B → VPC C)

**Real Production Example**:
"SaaS company, hot-warm architecture:
- US-EAST-1: 12 VPCs (production, staging, per-service VPCs, monitoring)
- US-WEST-2: 12 VPCs (matching architecture)
- Transit Gateway in each region
- TGW Peering between regions

Cost: 24 attachments × $36 = $864/month base. Data transfer: 500GB/day × $0.02 × 30 days = $300/month. Total: $1,164/month.

VPC Peering alternative: 12 VPCs in each region = 24 VPCs total = 276 peering connections to manage. Route table management nightmare. Three production outages in six months from routing misconfigurations.

They paid the $864/month for sanity. Worth it."

---

### 6. PrivateLink: Secure Service Endpoints (2-3 min)

**Teaching Approach**: Real-world application with security focus

**What It Is**:
"Expose services privately without VPC Peering or Transit Gateway. Service provider creates VPC endpoint service. Service consumer creates VPC endpoint. Traffic stays on AWS backbone. Never touches public internet. No VPC CIDR overlap issues."

**How It Works**:
"Service Provider (US-EAST-1):
1. Run service behind Network Load Balancer
2. Create VPC Endpoint Service pointing to NLB
3. Share endpoint service name

Service Consumer (US-WEST-2):
1. Create VPC Endpoint in their VPC
2. Point to provider's endpoint service name
3. Access service via private DNS or IP
4. Traffic flows: Consumer VPC → PrivateLink → Provider VPC"

**Use Cases**:
- Expose APIs or services to other VPCs/regions without full VPC connectivity
- Third-party integrations (share services with partner VPCs)
- Compliance requirements (no internet exposure)
- SaaS service delivery (your product accessed by customer VPCs)

**Advantages**:
- No CIDR overlap issues (each consumer gets unique ENI)
- Scales to thousands of consumers
- Security isolation (consumers can't see each other)
- No route table management
- Cross-region supported

**Limitations**:
- Requires Network Load Balancer ($0.0225/hour ~= $16/month)
- PrivateLink endpoint: $0.01/hour = $7/month per consumer
- Data transfer: $0.01/GB (cheaper than TGW/Peering across regions)
- Only TCP traffic (no UDP, ICMP)

**Cost Example**:
"Monitoring service accessed by 20 VPCs across regions:
- NLB: $16/month
- 20 endpoints × $7 = $140/month
- Data transfer: 50GB/day × $0.01 × 30 = $15/month
Total: $171/month

Alternative (VPC Peering): 20 peering connections, routing complexity, no isolation.
Alternative (Transit Gateway): 20 attachments × $36 = $720/month.

PrivateLink wins for service-oriented architectures."

---

### 7. Network Topology Design Principles (1-2 min)

**Teaching Approach**: Decision framework with practical guidance

**Design Principle 1: Start Simple**:
"Use VPC Peering for initial hot-warm setup (primary + secondary = 2 VPCs per region = 4 total). Add Transit Gateway when you hit 5+ VPCs or foresee growth."

**Design Principle 2: Plan for Data Transfer Costs**:
"Cross-region bandwidth isn't free. $0.02/GB adds up:
- 1TB/month: $20
- 10TB/month: $200
- 100TB/month: $2,000
- 1PB/month: $20,000

If Aurora replicates heavily or EKS has chatty cross-region services, this hits hard."

**Design Principle 3: Avoid Routing Table Explosion**:
"VPC route table limit: 125 entries. With VPC Peering, you need routes to every peered VPC. 40 peered VPCs = 40 routes (plus local, IGW, etc.). Transit Gateway: 1 route (to TGW). Scales infinitely."

**Design Principle 4: Minimize Cross-Region Traffic**:
"Keep traffic local when possible. External DNS and service mesh (from Episode 4) prefer local endpoints. Cross-region is failover only. This reduces data transfer costs and latency."

---

### 8. Common Mistakes That Kill Multi-Region (1-2 min)

**Mistake 1: Using Public Internet for Cross-Region**:
- What: Route cross-region traffic via public IPs
- Why it fails: Security exposure, high latency, unpredictable routing
- Fix: Always use VPC Peering, Transit Gateway, or PrivateLink

**Mistake 2: Ignoring Data Transfer Costs**:
- What: Architect without calculating cross-region bandwidth
- Reality: $50K/month surprise bills for high-traffic architectures
- Fix: Estimate traffic, calculate costs upfront, design to minimize

**Mistake 3: Hitting Route Table Limits**:
- What: Use VPC Peering for 20+ VPCs
- Why it fails: Route table limit (125 entries) causes routing failures
- Fix: Move to Transit Gateway before hitting 10 VPCs

**Mistake 4: No Bandwidth Planning**:
- What: Assume infinite cross-region bandwidth
- Reality: Transit Gateway limited to 50 Gbps per attachment
- Fix: Calculate bandwidth needs, plan for burst traffic

---

### 9. Active Recall Moment (1 min)

**Retrieval Prompt**:
"Before we wrap up, pause and answer:
1. You have 8 VPCs across two regions. Do you use VPC Peering or Transit Gateway? Why?
2. What's the formula for calculating VPC Peering connections?
3. Your Aurora replicates 500GB/day cross-region. What's the monthly data transfer cost?"

[PAUSE 5 seconds]

**Answers**:
"1. Transit Gateway. 8 VPCs approaches the complexity threshold. If you expect growth, TGW scales linearly. Cost: 8 × $36 = $288/month base. Worth it for operational simplicity and avoiding future route table issues.

2. N*(N-1)/2 where N is number of VPCs. 8 VPCs = 8×7/2 = 28 peering connections. Already complex.

3. 500GB/day × 30 days = 15TB/month. At $0.02/GB = $300/month just for Aurora replication. This is why you design to minimize cross-region traffic when possible."

---

### 10. Recap & Synthesis (1-2 min)

**Key Takeaways**:
1. **VPC Peering**: Simple, low-cost, but doesn't scale. Use for ≤4 VPCs.
2. **Transit Gateway**: Hub-and-spoke that scales linearly. Use for 5+ VPCs or expected growth. $36/month per VPC attachment.
3. **PrivateLink**: Service-oriented architecture. Expose APIs privately without full VPC connectivity. Good for multi-consumer services.
4. **Data transfer costs**: $0.02/GB cross-region. Calculate before you build. 1TB/month = $20, 100TB/month = $2,000.
5. **Route table limits**: 125 entries per VPC. VPC Peering hits this fast. Transit Gateway scales infinitely.

**Connection to Bigger Picture**:
"Remember Episode 2? Hot-warm pattern with 5-minute RTO? You need the network layer to support that:
- Aurora replication (Episode 3): Travels over these networks (VPC Peering or Transit Gateway)
- EKS cross-cluster communication (Episode 4): Service mesh traffic flows over these networks
- DNS failover (Episode 4): Depends on network connectivity to reach services

Together: Data layer + Compute layer + Network layer = Complete multi-region architecture."

**Spaced Repetition**:
"We'll revisit Transit Gateway in Episode 8 when we cover DNS and Traffic Management. And in Episode 9 (Cost Management), we'll optimize these network costs. In Episode 14 (Security Architecture), we'll secure these network paths with encryption and private connectivity."

---

### 11. Next Episode Preview (30 sec)

"Next time: DynamoDB Global Tables - Active-active data replication.

Aurora gave you active-passive replication (one writer, one reader). What if you need active-active? Multiple regions accepting writes simultaneously?

You'll learn:
- How DynamoDB Global Tables replicate with sub-second lag globally
- Conflict resolution strategies when two regions write to same item
- When to use DynamoDB over Aurora (and when not to)
- The hidden costs of global tables ($25K+ monthly for high-traffic tables)

Because Aurora isn't the only answer. For certain workloads, DynamoDB's active-active replication is what you need. But it comes with trade-offs.

See you in Episode 6."

---

## Supporting Materials

**Technical References**:
- AWS Transit Gateway Documentation: Bandwidth limits, pricing
- VPC Peering Documentation: Route table limits, cross-region support
- PrivateLink Documentation: Endpoint services, consumer setup
- AWS Data Transfer Pricing: Cross-region rates

**Analogies to Use**:
- Transit Gateway: Airport hub (centralized routing vs point-to-point flights)
- VPC Peering: Direct phone lines (doesn't scale beyond small groups)
- PrivateLink: Private API gateway (expose services without network connectivity)
- Route table limit: Address book with 125 slots (runs out fast with VPC Peering)

**Cost Calculations**:
- VPC Peering: $0 base + $0.02/GB cross-region
- Transit Gateway: $0.05/hour per attachment + $0.02/GB cross-region
- PrivateLink: $0.0225/hour NLB + $0.01/hour per endpoint + $0.01/GB

---

## Quality Checklist

**Structure**:
- [x] Clear beginning, middle, end
- [x] Logical flow (problem → VPC Peering → Transit Gateway → PrivateLink → design principles → mistakes)
- [x] Time allocations realistic (total 15 min)
- [x] All sections have specific content

**Pedagogy**:
- [x] Learning objectives specific and measurable
- [x] Spaced repetition integrated (Aurora, EKS, hot-warm callbacks)
- [x] Active recall moment included
- [x] Signposting throughout
- [x] Multiple analogies (airport hub, phone lines, address book)
- [x] Common pitfalls addressed

**Content**:
- [x] Addresses real production patterns
- [x] Decision frameworks (when to use what)
- [x] Cost calculations with real numbers
- [x] Performance characteristics (bandwidth, latency)
- [x] Appropriate depth for senior engineers

**Engagement**:
- [x] Strong hook (e-commerce outage from route table limits)
- [x] Real production example (SaaS company with 24 VPCs)
- [x] Practice moment (active recall with cost calculations)
- [x] Preview builds anticipation (DynamoDB active-active)
