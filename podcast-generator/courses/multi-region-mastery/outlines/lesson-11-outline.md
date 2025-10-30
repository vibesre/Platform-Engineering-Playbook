# Lesson Outline: Episode 11 - Multi-Region Kubernetes Patterns: Service Mesh & Federation

## Metadata
**Course**: Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale
**Episode**: 11 of 16
**Duration**: 15 minutes
**Episode Type**: Core Concept
**Prerequisites**: Episodes 1-10, Kubernetes experience, familiarity with service meshes
**Template Used**: Template 2 (Core Concept)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. Explain three multi-region Kubernetes patterns: Namespace federation, cluster federation, and mesh routing
2. Design service mesh configuration that prefers local region traffic but fails over gracefully
3. Implement DNS-based service discovery across regions
4. Identify where multi-cluster Kubernetes adds value vs single-cluster hot-warm

Success criteria:
- Can explain when to use federation vs mesh routing
- Can design locality-aware traffic policies
- Can identify failure scenarios in multi-cluster setup
- Can calculate if multi-cluster complexity is worth the benefit

## Spaced Repetition Plan

**Concepts Introduced**:
- Service mesh patterns (will detail in Episode 14 security)
- Multi-cluster complexity (will evaluate in Episode 12 testing)

**Concepts Reinforced**:
- Locality-aware routing from Episode 9 (applied with service mesh)
- CAP Theorem from Episode 10 (applied to service discovery)

## Lesson Flow

### 1. Recall & Connection (1-2 min)

"You have Aurora and DynamoDB replicated. You have network connectivity via Transit Gateway from Episode 5. You have Route53 failover from Episode 8.

But here's where it gets complex: Your Kubernetes clusters in both regions need to talk, share service discovery, and route traffic intelligently.

Today: How to make multi-cluster Kubernetes work without losing your mind."

---

### 2. Learning Objectives (30 sec)

"By the end of this lesson:
- You'll understand three multi-region K8s patterns
- You'll design service mesh for locality-aware traffic
- You'll set up cross-region service discovery
- You'll know when multi-cluster adds value vs overhead"

---

### 3. Three Kubernetes Multi-Region Patterns (3-4 min)

**Pattern 1: Dual Single-Cluster**
"Each region runs independent Kubernetes cluster. Clusters don't communicate. Services in US-EAST-1 only call services in US-EAST-1. Cross-region calls only between data layers (Aurora, DynamoDB).

Simplest pattern. Lowest overhead. Each cluster can fail independently."

**Pattern 2: Cluster Federation with Ingress**
"Clusters share DNS and service discovery. Services can call each other across clusters. Ingress routes traffic between clusters.

More complex than dual-cluster. Adds cross-cluster dependency."

**Pattern 3: Service Mesh (Istio, Linkerd)**
"Service mesh handles all cross-cluster communication, load balancing, failover. Automatic cross-region routing. Circuits breakers for failures.

Most sophisticated. Most overhead. Most resilient."

---

### 4. Service Mesh for Locality-Aware Traffic (3-4 min)

**Teaching Approach**: Configuration example

"Service mesh keeps traffic local: US-EAST-1 pods call US-EAST-1 services, US-WEST-2 pods call US-WEST-2 services.

Only cross-region when primary region fails. This is how Episode 9 achieved 90% data transfer reduction."

**Implementation**:
"Configure destination rules with locality load balancing. Istio example:

priorityLb:
  failover:
    - locality: us-east-1
      percentage: 100
    - locality: us-west-2
      percentage: 100  (fallback)

Result: All traffic stays local. If US-EAST-1 fails, automatically routes to US-WEST-2."

**Virtual Services** (traffic routing):
"Define virtual services that split traffic by region. Forward 95% to local, 5% to remote for health checks."

---

### 5. Cross-Region Service Discovery (2 min)

**Teaching Approach**: DNS integration

"Each cluster registers services with shared DNS. When pod in US-EAST-1 queries 'payment-service.default', DNS returns both regions' instances.

Service mesh chooses local instance first. If local fails, tries remote."

**Implementation**:
"Use ExternalDNS in each cluster to register with Route53. Services automatically discoverable cross-region.

Alternatively: CoreDNS federation. One DNS server with federated views of both clusters."

---

### 6. When Multi-Cluster Adds Value (1-2 min)

**When Worth It**:
- Both regions handle simultaneous traffic (hot-hot)
- Need pod-to-pod cross-region communication
- Service mesh provides observability across clusters
- Shared service discovery reduces latency

**When Not Worth It**:
- Hot-warm: Secondary region is standby. Single-cluster per region is fine
- Observability can be centralized without mesh
- Data layer already handles replication (Aurora, DynamoDB)

**Cost-Benefit**:
"Service mesh overhead: 15-20% additional CPU/memory. Worth it only if you need cross-region pod communication actively."

---

### 7. Common Failure Scenarios (1 min)

"Network partition between clusters: Service mesh health checks discover it. Routes automatically to healthy cluster.

Partial service failure: Load balancing distributes around failures.

Entire cluster gone: Mesh redirects all traffic to remaining cluster."

---

### 8. Active Recall (1 min)

"Pause:
1. When does cluster federation add value over dual single-clusters?
2. How does locality-aware routing reduce data transfer?
3. What happens when network partition occurs between regions?

[PAUSE]

Answers:
1. When both regions actively handle traffic (hot-hot) and services need to communicate across regions
2. Keeps 90%+ traffic local. Only cross-region on failover or explicit cross-cluster calls
3. Service mesh detects health check failures and routes to healthy region automatically"

---

### 9. Recap & Synthesis (1-2 min)

**Key Takeaways**:
1. **Three patterns**: Dual clusters (simplest), federation (moderate), mesh (most sophisticated)
2. **Service mesh enables locality-aware routing**: Automatic failover without application changes
3. **Most multi-region K8s doesn't need mesh complexity**: Hot-warm works fine with dual single-clusters
4. **Cross-region service discovery**: Possible via ExternalDNS or CoreDNS federation

---

### 10. Next Episode Preview (30 sec)

"Next: Episode 12 - Disaster Recovery: Failover Procedures & Chaos Engineering.

We've built the entire multi-region architecture. Now: How do you actually test it? Failover drills. Chaos engineering. What breaks?"

---

## Quality Checklist

- [x] Prerequisites clear
- [x] Learning objectives measurable
- [x] Three patterns explained with pros/cons
- [x] Service mesh configuration specific
- [x] Cost-benefit analysis included
- [x] Common failure scenarios addressed
- [x] When to use vs when not to use
- [x] Active recall included
