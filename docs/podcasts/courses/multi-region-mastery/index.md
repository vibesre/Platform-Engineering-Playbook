# Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale

<GitHubButtons />

A comprehensive 16-episode course on building production-grade multi-region architectures. Learn the LEGO architecture approach - master individual building blocks (Aurora Global Database, EKS, Transit Gateway, DynamoDB Global Tables) and understand how to compose them for your specific requirements.

**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years of production experience

**Course Philosophy**: Brutal honesty over marketing hype. We'll show you the real costs, the hidden complexity, and when single-region is actually the better choice. By the end, you'll think of multi-region components as composable building blocks you can assemble to meet your organization's specific needs.

## 🎥 Watch the Full Course

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, margin: '1.5rem 0'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/videoseries?list=PLIjf2e3L8dZxgOr4Equjl_YwMKXTQKCM"
    title="Multi-Region Platform Engineering Course Playlist"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>

<PodcastSubscribeButtons />

## What You'll Learn

- **Cost Reality**: The true 2.5-7.5x cost multiplier (not the 2x vendors claim)
- **Architecture Patterns**: Hot-hot, hot-warm, hot-cold - what companies actually build
- **AWS Building Blocks**: Aurora Global Database, EKS multi-cluster, Transit Gateway, DynamoDB Global Tables
- **Data Strategies**: Consistency models, replication patterns, conflict resolution
- **Network Architecture**: VPC peering, Transit Gateway, PrivateLink, Global Accelerator
- **Observability**: Centralized logging, distributed tracing, cross-region monitoring
- **Kubernetes Patterns**: Federation, cluster meshes, multi-cluster service discovery
- **Compliance**: SEC SCI, MiFID II, crypto regulations (NY BitLicense, EU MiCA)
- **Decision Frameworks**: Calculate your actual needs vs aspirational architecture

## Prerequisites

- 5+ years production experience with AWS
- Working knowledge of Kubernetes
- Understanding of distributed systems concepts
- Familiarity with databases (RDS, DynamoDB)
- Experience with networking (VPC, subnets, routing)

## Course Duration

- **16 episodes** (~15 minutes each)
- **Total**: ~4 hours of content
- **Pacing**: Self-paced, progressive complexity
- **Prerequisites**: Each lesson builds on previous episodes

## Course Structure

### Module 1: Foundations (Episodes 1-3)
Understanding the economic and architectural fundamentals

### Module 2: Core Building Blocks (Episodes 4-8)
Deep dives into individual AWS components

### Module 3: Integration Patterns (Episodes 9-11)
How to compose building blocks for production

### Module 4: Specialized Topics (Episodes 12-14)
Compliance, security, and edge cases

### Module 5: Mastery (Episodes 15-16)
Anti-patterns, troubleshooting, and real-world implementation

---

## 📚 Course Episodes

**Current Status**: All 16 episodes published ✅

### Module 1: Foundations (Episodes 1-3)

#### 📖 [Lesson 1: The Multi-Region Mental Model](/podcasts/courses/multi-region-mastery/lesson-01)
**Duration**: 15 min

Learn about:
- Cost, Complexity, Capability (CCC) Triangle mental model
- True cost multiplier: 2.5x-7.5x (not 2x vendors claim)
- Single Points of Failure in "multi-region" AWS architectures

#### 📖 [Lesson 2: Production Patterns - Hot-Hot, Hot-Warm, Hot-Cold](/podcasts/courses/multi-region-mastery/lesson-02)
**Duration**: 16 min

Learn about:
- RTO/RPO and cost trade-offs for each pattern
- Hot-warm: 5-minute RTO, reasonable cost
- Hot-hot: Subsecond failover, 7.5x cost multiplier

#### 📖 [Lesson 3: Aurora Global Database Deep Dive](/podcasts/courses/multi-region-mastery/lesson-03)
**Duration**: 14 min

Learn about:
- Active-passive replication with 45-85ms lag
- Promotion procedures and RTO calculations
- When Aurora is better than DynamoDB

### Module 2: Core Building Blocks (Episodes 4-8)

#### 📖 [Lesson 4: Kubernetes Multi-Cluster Architecture](/podcasts/courses/multi-region-mastery/lesson-04)
**Duration**: 18 min

Learn about:
- EKS control plane as regional boundary (not multi-region)
- Independent clusters vs federation (why federation failed)
- Cross-cluster service discovery: DNS vs service mesh

#### 📖 [Lesson 5: Network Architecture - Transit Gateway & PrivateLink](/podcasts/courses/multi-region-mastery/lesson-05)
**Duration**: 17 min

Learn about:
- VPC peering limitations at scale
- Transit Gateway for hub-and-spoke multi-region
- PrivateLink for secure cross-region access

#### 📖 [Lesson 6: DynamoDB Global Tables - Active-Active Replication](/podcasts/courses/multi-region-mastery/lesson-06)
**Duration**: 15 min

Learn about:
- Multi-region writes with 1-3 second lag
- Conflict resolution: last-writer-wins vs application-level
- Cost comparison: DynamoDB vs Aurora at scale

#### 📖 [Lesson 7: Observability at Scale](/podcasts/courses/multi-region-mastery/lesson-07)
**Duration**: 16 min

Learn about:
- Centralized logging without data transfer explosion
- Distributed tracing across regions
- Cross-region metrics aggregation

#### 📖 [Lesson 8: DNS & Traffic Management - Route53 & Global Accelerator](/podcasts/courses/multi-region-mastery/lesson-08)
**Duration**: 14 min

Learn about:
- Health checks and failover detection (90 seconds)
- DNS TTL trade-offs (60-300 seconds)
- Global Accelerator: anycast IPs for subsecond routing

### Module 3: Integration Patterns (Episodes 9-11)

#### 📖 [Lesson 9: Cost Management - Optimizing the 7.5x Multiplier](/podcasts/courses/multi-region-mastery/lesson-09)
**Duration**: 16 min

Learn about:
- Four cost categories: compute, data transfer, database, operations
- Seven optimization strategies (locality-aware routing saves 90%)
- Real example: $112K → $36K (67% savings)

#### 📖 [Lesson 10: Data Consistency Models - CAP Theorem in Production](/podcasts/courses/multi-region-mastery/lesson-10)
**Duration**: 13 min

Learn about:
- Aurora: CP (Consistency + Partition tolerance)
- DynamoDB: AP (Availability + Partition tolerance)
- Split-brain prevention: quorum, human approval, fencing

#### 📖 [Lesson 11: Advanced Kubernetes Patterns - Service Mesh & Federation](/podcasts/courses/multi-region-mastery/lesson-11)
**Duration**: 15 min

Learn about:
- Istio multi-cluster: subsecond failover vs DNS's 2+ minutes
- Operational complexity: mesh upgrades, certificate management
- When to use service mesh (hot-hot) vs keep it simple (hot-warm)

### Module 4: Specialized Topics (Episodes 12-14)

#### 📖 [Lesson 12: Disaster Recovery - Failover Procedures & Chaos Engineering](/podcasts/courses/multi-region-mastery/lesson-12)
**Duration**: 17 min

Learn about:
- 6-phase DR runbook: detect, validate, approve, execute, verify, rollback
- Chaos engineering quarterly testing with escalating severity
- Failure scenarios that break multi-region

#### 📖 [Lesson 13: Compliance-Driven Architecture](/podcasts/courses/multi-region-mastery/lesson-13)
**Duration**: 16 min

Learn about:
- SEC SCI 2-4 hour RTO mandates
- MiFID II EU-only data residency ($200K/year cost)
- BitLicense immutable audit trails

#### 📖 [Lesson 14: Security Architecture - Encryption & Key Management](/podcasts/courses/multi-region-mastery/lesson-14)
**Duration**: 18 min

Learn about:
- Encryption at-rest (KMS), in-transit (TLS 1.3), in-use (mTLS)
- Key management trade-offs: per-region vs replicated keys
- Zero-trust networking with VPC endpoints

### Module 5: Mastery (Episodes 15-16)

#### 📖 [Lesson 15: Anti-Patterns - What Breaks Multi-Region](/podcasts/courses/multi-region-mastery/lesson-15)
**Duration**: 15 min

Learn about:
- Six anti-patterns causing production failures
- Real cost impact: $12K → $95K
- Recovery strategies for each pattern

#### 📖 [Lesson 16: Implementation Roadmap - Your 90-Day Plan](/podcasts/courses/multi-region-mastery/lesson-16)
**Duration**: 18 min

Learn about:
- 4-phase rollout: foundation, data layer, compute, validation
- Go-no-go gates at each phase
- Abort criteria when ROI < 5x or costs exceed projections

---

## 🎥 Watch on YouTube

Course playlist coming soon after Episode 2.

---

## Learning Approach

This course uses evidence-based learning science principles:

**Spaced Repetition**: Key concepts (like the CCC Triangle) are introduced early and reinforced 3-5 times throughout the course

**Progressive Complexity**: Each episode builds on previous lessons, adding one new layer of complexity

**Active Recall**: Regular pause points ask you to apply concepts before revealing solutions

**Real Numbers**: Every cost, latency, and performance claim is sourced from production data

**LEGO Architecture**: Think of each AWS service as a composable building block - understand how each piece works and how to fit them together

---

## Navigation

📚 **[Back to All Podcasts](/podcasts)**
