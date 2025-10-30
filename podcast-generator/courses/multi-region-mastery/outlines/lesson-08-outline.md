# Lesson Outline: Episode 8 - DNS and Traffic Management: Route53 & Global Accelerator

## Metadata
**Course**: Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale
**Episode**: 8 of 16
**Duration**: 15 minutes
**Episode Type**: Core Concept
**Prerequisites**: Episodes 1-7 (patterns, data layer, network architecture), understanding of DNS basics, Route53 familiarity
**Template Used**: Template 2 (Core Concept)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. Configure Route53 health checks that detect failures in under 60 seconds
2. Explain failover routing policies and when to use them vs weighted/latency-based routing
3. Calculate appropriate TTL values for your RTO requirements
4. Decide between Route53 (DNS-based) failover and Global Accelerator (anycast) based on failover speed needs

Success criteria:
- Can design a Route53 health check configuration with specific thresholds
- Can explain why latency-based routing breaks hot-warm failover
- Can calculate DNS propagation time and its impact on RTO
- Can calculate Global Accelerator cost vs failover speed benefit

## Spaced Repetition Plan

**Concepts Introduced**:
- Health checks (will apply in Episode 12 for DR testing)
- TTL configuration (will appear in Episode 12 DNS failover scenarios)
- Global Accelerator (will compare with other routing in Episode 14)

**Concepts Reinforced**:
- RTO/RPO from Episodes 1-2 (applied to DNS failover timing)
- Hot-warm pattern from Episode 2 (detailed failover implementation)
- Aurora promotion from Episode 3 (timing coordination)

## Lesson Flow

### 1. Recall & Connection (1-2 min)

**Active Recall Prompt**:
"Before we dive in, pause and think: In Episode 2's hot-warm scenario, we said RTO was about 5 minutes. But how do users actually reach the secondary region when primary fails? We haven't covered that yet. Today you'll find out."

**Connection**:
"This is the control plane for multi-region traffic. Get DNS failover right and failover is transparent. Get it wrong and your hot-warm becomes no-warm during actual failures."

---

### 2. Learning Objectives (30 sec)

"By the end of this lesson, you'll:
- Configure Route53 health checks that detect failure in 60-90 seconds
- Understand failover routing policies and the common mistake (using latency-based instead)
- Calculate TTL impact on your actual RTO
- Decide if you need Global Accelerator or if Route53 is sufficient"

---

### 3. The Problem: DNS Failover (2 min)

**Teaching Approach**: Problem revelation

**The Setup**:
"You've built multi-region infrastructure. Aurora replicating. DynamoDB active-active. EKS clusters running. Network layer connecting them. Observability showing what's happening.

But here's the critical question: When US-EAST-1 fails, how do users actually reach US-WEST-2?"

**The Realization**:
"Your Aurora secondary gets promoted. Your EKS pods are running. Everything is ready. But users are still hitting US-EAST-1 endpoints. Their requests timeout. Revenue drops.

The missing piece is DNS. Route53 health checks, failover policies, TTL configuration. This is your control plane for multi-region traffic."

**Key Insight**:
"Without proper DNS failover, your hot-warm architecture is just expensive infrastructure sitting around."

---

### 4. Route53 Health Checks - Fundamentals (3 min)

**Teaching Approach**: Detailed mechanics

**The Basic Problem with Plain DNS**:
"You create an A record pointing to your US-EAST-1 load balancer. Users resolve your domain, get the US-EAST-1 IP, connect. Simple.

But what happens when US-EAST-1 fails? [pause] With basic DNS, nothing. The A record still points to US-EAST-1. Users keep getting that IP. They try to connect, it times out. DNS doesn't know the endpoint is down."

**How Route53 Health Checks Solve This**:
"Route53 health checks monitor your endpoints. HTTP request every 30 seconds. If three consecutive checks fail, Route53 marks it unhealthy. That's 90 seconds to detect failure.

When the primary is marked unhealthy, Route53 starts returning the secondary IP. Users resolve, get US-WEST-2 IP. They connect to the secondary region. Failover complete."

**Health Check Configuration Details**:

**Check Type**: "HTTPS checks against a dedicated health endpoint. Not your homepage - that's too noisy. Create a lightweight /health endpoint that verifies critical dependencies. Returns 200 if Aurora is reachable, if application can connect, if critical services respond. Returns 500 if anything breaks."

**Frequency**: "Every 30 seconds is standard. Faster checks (every 10 seconds) cost more and increase false positives from transient issues. Slower checks miss failures longer."

**Failure Threshold**: "Three consecutive failures = 90 seconds detection. Two failures = 60 seconds but increases false positive risk. Balance detection speed against stability."

**The Impact on RTO**:
"Failure detection: 90 seconds. Plus Aurora promotion (from Episode 3): ~1 minute. Plus DNS TTL (we'll cover next): 60+ seconds. Total RTO: 3-5 minutes. This matches our hot-warm pattern from Episode 2."

---

### 5. Routing Policies - When to Use What (3 min)

**Teaching Approach**: Comparison and decision framework

**The Six Policies**:

**Failover Routing**:
"Primary and secondary records. Health check on primary only. When primary fails, return secondary. This IS the hot-warm pattern.

Configuration: Two A records, same name. One marked 'primary' with US-EAST-1 IP and health check. One marked 'secondary' with US-WEST-2 IP, no health check. When primary health check fails, Route53 returns secondary."

**Weighted Routing**:
"Split traffic across regions by percentage. 70% to US-EAST-1, 30% to US-WEST-2. Use for gradual migration or load distribution in hot-hot patterns."

**Latency-based Routing**:
"Route users to lowest-latency region. Route53 measures latency from different AWS regions. User in California → US-WEST-2. User in Virginia → US-EAST-1. Good for performance optimization when all regions are active."

**Geolocation Routing**:
"Route based on user's physical location. All European users → EU-WEST-1 regardless of latency. Use for data residency or regional content."

**The CRITICAL MISTAKE**:
"[Emphasis] Teams think: 'Use latency-based for hot-warm. It'll send traffic to the healthy region.' Wrong. Latency-based routes to lowest-latency region. If US-EAST-1 fails but is still responding to DNS queries, users STILL get routed there based on latency. They then fail to connect.

Use FAILOVER routing for hot-warm. Not latency-based. This mistake breaks production failover."

---

### 6. TTL Configuration - The Hidden Failover Cost (2 min)

**Teaching Approach**: Tradeoff analysis

**What TTL Does**:
"Time To Live tells DNS resolvers how long to cache your answer. 60-second TTL means resolvers refresh every 60 seconds. 300-second TTL means they don't refresh for 5 minutes."

**The Tradeoff**:
"Lower TTL = faster failover but higher DNS query volume. 60-second TTL with a million users = lots of re-queries. Higher cost, more load on Route53.

Higher TTL = slower failover, lower cost and load."

**For Hot-Warm**:
"60-120 second TTL balances failover speed and cost. For hot-hot with health checks on all regions, you can use longer TTL since all regions are always healthy."

**Real Math**:
"If your TTL is 300 seconds (5 minutes) and health check detects failure at 90 seconds, users with cached DNS might not learn about the change for another 300 seconds. Total failover time: up to 6 minutes. That breaks your 5-minute RTO from Episode 2."

---

### 7. Global Accelerator - When DNS Failover Isn't Fast Enough (2 min)

**Teaching Approach**: Problem-solution

**The DNS Limitation**:
"DNS failover depends on TTL and resolver behavior. Even with 60-second TTL, some resolvers ignore it. Mobile networks, corporate DNS servers, they cache aggressively. This extends failover time unpredictably."

**The Global Accelerator Solution**:
"Uses anycast IPs. You get two static IPs that announce from all AWS edge locations globally. Users connect to the nearest edge. Edge location maintains persistent connections to your healthy endpoints.

When US-EAST-1 fails, Global Accelerator detects it via health checks. Edge locations stop routing to US-EAST-1. They route to US-WEST-2 instead. No DNS involved. No TTL wait. Subsecond failover."

**How It Works**:
"Create a Global Accelerator accelerator. Add endpoint groups (US-EAST-1 and US-WEST-2). Configure health checks. Global Accelerator assigns you two anycast IPs. Users connect to those IPs. Traffic routes through AWS edge network to healthy endpoints.

When US-EAST-1 health check fails, edge locations immediately stop sending traffic there. New connections go to US-WEST-2. Failover time: under 10 seconds."

**Cost Consideration**:
"About $25/month per accelerator plus $0.08/GB data transfer. For high-traffic sites where subsecond failover matters, this is worth it. For lower-traffic sites where 2-3 minute DNS failover is acceptable, stick with Route53."

**Decision Framework**:
"Use Global Accelerator when:
- You need subsecond failover
- Users have aggressive DNS caching
- You want consistent IPs that don't change
- You're serving TCP/UDP protocols

Stick with Route53 when:
- Cost-sensitive
- 2-3 minute failover acceptable
- HTTP/HTTPS where DNS works well"

---

### 8. Real Production Example (2 min)

**Teaching Approach**: End-to-end scenario

**The Company**: "E-commerce site. Hot-warm with Route53 failover."

**Setup**:
- Primary: US-EAST-1
- Secondary: US-WEST-2
- Health check every 30 seconds against /health endpoint
- 60-second TTL
- Aurora Global Database in Episode 3 handles data layer
- EKS clusters in both regions (20% capacity in secondary)

**Failure Scenario** (Black Friday morning):
- Minute 0: Database issue in US-EAST-1, app starts returning 500 errors
- Minute 1.5: Route53 health check fails (3 × 30s = 90s)
- Minute 2: Route53 marks US-EAST-1 unhealthy
- Minute 3-4: New DNS queries return US-WEST-2 IP
- Minute 5: Existing caches expire (60s TTL), traffic fully shifted
- Minute 6+: EKS auto-scaling from 20% to 100% capacity

**Total RTO**: 5-6 minutes

**Revenue Impact**: Black Friday does $200K/hour. Loss: ~$16,666 during 5 minutes of failover.

**Cost-Benefit**: Hot-warm costs extra $15K/month. One major outage prevented = 4+ years of hot-warm paid for.

---

### 9. Common Mistakes (1 min)

**Mistake 1**: "Using latency-based routing for hot-warm"
- Fix: Use failover routing instead

**Mistake 2**: "TTL too high (300+ seconds) for hot-warm"
- Fix: Use 60-120 second TTL to match RTO requirements

**Mistake 3**: "Health checks on the wrong endpoint"
- Fix: Check real application health, not just "is the server responding"

---

### 10. Active Recall (1 min)

**Retrieval Prompt**:
"Pause and answer:
1. If Route53 health check is 90 seconds and TTL is 60 seconds, what's your minimum failover time?
2. Why is latency-based routing wrong for hot-warm failover?
3. When would you use Global Accelerator instead of Route53?

[PAUSE 5 seconds]

Answers:
1. 90 seconds (health check detection) + 60 seconds (TTL refresh for remaining users) = 150 seconds (2.5 min minimum)
2. Latency-based routes to lowest-latency region regardless of health. If primary is down but responding to DNS, users still get routed there. Use failover routing instead.
3. Need subsecond failover, users with aggressive DNS caching, TCP/UDP protocols, cost can justify $25/month + data transfer"

---

### 11. Recap & Synthesis (1-2 min)

**Key Takeaways**:
1. **Route53 health checks detect failure in 60-90 seconds**: HTTP/HTTPS checks against a health endpoint that verifies critical dependencies
2. **Use failover routing for hot-warm, not latency-based**: This is the most common production mistake
3. **TTL directly impacts your RTO**: 60-120 seconds for hot-warm, longer for hot-hot
4. **Global Accelerator trades cost for speed**: Subsecond failover if you can justify $25+/month
5. **The full failover chain includes detection + promotion + routing**: 90s health check + Aurora promotion + DNS propagation = 3-5 min RTO

**Spaced Repetition Callback**:
"Remember Episode 2's hot-warm pattern with 5-minute RTO? This is how you actually achieve it. Health checks + failover routing + proper TTL = transparent failover for your users."

---

### 12. Next Episode Preview (30 sec)

"Next: Episode 9 - Cost Management: Optimizing the 7.5x Multiplier.

You now know how to build hot-warm and hot-hot. But you've seen that costs multiply. We'll learn which services in your multi-region architecture are the cost killers - and how to optimize them without breaking failover.

See you next time."

---

## Supporting Materials

**Health Check Configuration Template**:
```yaml
Route53 Health Check:
  Type: HTTPS
  Endpoint: your-domain.com/health
  Interval: 30 seconds
  Failure threshold: 3 consecutive failures
  Expected response: 200 OK
```

**Routing Policy Decision Table**:
| Pattern | Routing Policy | Failover Speed | Use Case |
|---------|----------------|-----------------|----------|
| Hot-Warm | Failover | 2-5 min | One active, one standby |
| Hot-Hot | Weighted/Latency | <1 min | Both active, load distributed |
| Geo | Geolocation | 2-5 min | Regional compliance |

---

## Quality Checklist

- [x] Prerequisites clear (Episodes 1-7, DNS basics)
- [x] Learning objectives measurable (configure, calculate, decide)
- [x] Spaced repetition (RTO callback from Episode 2, data layer from Episode 3)
- [x] Common mistake highlighted (latency-based routing for hot-warm)
- [x] Real production example with timing
- [x] Decision framework (Route53 vs Global Accelerator)
- [x] Active recall included
- [x] All sections specific (not vague)
