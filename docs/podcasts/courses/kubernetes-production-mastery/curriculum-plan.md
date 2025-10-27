# Kubernetes Production Mastery - Curriculum Plan (10 Episodes)

## Course Overview
**Target Audience**: Senior platform engineers, SREs, DevOps engineers (5+ years experience)
**Prerequisites**:
- Basic Kubernetes knowledge (Pods, Deployments, Services)
- Docker container experience
- Production engineering experience
- Command-line proficiency

**Total Duration**: 10 episodes, ~2.5 hours total
**Learning Outcomes**:
- Diagnose and prevent the 5 most common production failure patterns
- Configure production-ready Kubernetes workloads using complete best practices checklist
- Debug CrashLoopBackOff, OOMKilled, and networking issues systematically
- Implement RBAC security with least privilege and secure secrets management
- Deploy and manage stateful workloads (databases, caches) with StatefulSets
- Build comprehensive observability stack (Prometheus, logging, alerting)
- Implement GitOps deployment automation with ArgoCD/Flux
- Optimize Kubernetes costs and manage multi-cluster environments at scale

## Pedagogical Approach

**Spaced Repetition**:
- Resource limits/requests: Ep 1 intro → Ep 2 deep → Ep 8 cost context
- RBAC: Ep 1 intro → Ep 3 deep → Ep 10 multi-cluster
- Production checklist: Ep 1 intro → applied every episode → Ep 10 synthesis
- Health checks: Ep 1 intro → Ep 4 debugging → Ep 10 runbooks
- Storage patterns: Ep 5 intro → Ep 7 monitoring → Ep 10 DR
- GitOps: Ep 9 deep → Ep 10 multi-cluster application

**Active Recall**:
- Every episode starts with "Last time we covered..." callback
- Mid-episode pause points: "Before we continue, recall..."
- End-of-episode retrieval questions (3-5 questions)
- Episode 10 comprehensive review tests retention of all concepts

**Progressive Complexity**:
- Ep 1: Mental model shift (dev → production thinking)
- Eps 2-7: Production operations foundations (one concept per episode)
- Eps 8-10: Operations at scale (synthesis and multi-cluster)

**Interleaving**:
- Security (RBAC, secrets) + Operations (resource mgmt, storage, networking)
- Troubleshooting woven through Eps 4, 6, 7
- Cost optimization revisits resource management
- Multi-cluster integrates all previous concepts

## Episode Breakdown

### MODULE 1: FOUNDATION (Episode 1)

#### Episode 1: Production Mindset - From Dev to Production
**Duration**: 12 min
**Learning Objectives**:
- Explain the critical differences between development and production K8s clusters
- Identify the top 5 production failure patterns (by name, not detail)
- Apply the production mindset framework when evaluating cluster configs

**Covers**:
- Rapid basics refresher (5 min speed run: Pods → Deployments → Services)
- Mental model: Dev cluster vs Production cluster thinking
- The 5 production failure patterns (list and preview, detail in later episodes)
- Production readiness checklist (6 items introduced)

**Spaced Repetition**:
- **Introduces**: Resource limits, RBAC, health checks, storage, networking, observability, cost, GitOps
- **Reinforces**: None (first episode)

**Active Recall Moments**:
- End: "Name the 5 failure patterns without looking back"
- End: "List 3 items from the production checklist"

**Prerequisites**: Basic K8s knowledge (Pods, Deployments, Services)
**Leads to**: Episodes 2-10 (each expands on foundation)

---

### MODULE 2: CORE PRODUCTION PATTERNS (Episodes 2-7)

#### Episode 2: Resource Management - Preventing OOMKilled
**Duration**: 15 min
**Learning Objectives**:
- Distinguish between resource requests and limits and explain their scheduling vs enforcement roles
- Diagnose OOMKilled errors from symptoms to root cause using kubectl workflow
- Right-size container resources using load testing data and QoS principles

**Covers**:
- Understanding requests vs limits (scheduling vs enforcement)
- Why OOMKilled happens (memory pressure, node overcommit, no limits)
- Debugging workflow: From OOMKilled (exit code 137) to root cause
- Quality of Service (QoS) classes (Guaranteed, Burstable, BestEffort)
- Right-sizing: Load testing and capacity planning strategies

**Spaced Repetition**:
- **Introduces**: QoS classes, node resource allocation, capacity planning, load testing
- **Reinforces**: Resource limits (from Ep 1 checklist item #1)

**Active Recall Moments**:
- Start: "Recall from Ep 1: What's the #1 production failure pattern?"
- Mid: "Before I show the solution, how would YOU debug this OOMKilled pod?"
- End: "Explain requests vs limits in your own words"
- End: "What's the QoS class of a pod with limits but no requests?"

**Prerequisites**: Episode 1
**Leads to**: Episode 8 (cost optimization revisits this)

---

#### Episode 3: Security Foundations - RBAC & Secrets
**Duration**: 18 min
**Learning Objectives**:
- Implement namespace-scoped RBAC roles following least privilege principles
- Configure secure secrets management using Sealed Secrets or External Secrets Operator
- Identify and remediate the 5 most common RBAC misconfigurations

**Covers**:
**RBAC (10 min)**:
- Why RBAC is consistently misconfigured (#1 K8s security issue in 2024)
- The principle of least privilege (theory → practice)
- Namespace-scoped vs cluster-scoped roles (Roles vs ClusterRoles)
- Service account security (avoid auto-mount, wildcards, system:masters)
- Common RBAC attack patterns (privilege escalation, token theft)

**Secrets Management (8 min)**:
- Why Secrets in plaintext/git/env vars cause breaches
- Secrets vs ConfigMaps (when to use each)
- Sealed Secrets pattern (encrypt before committing to git)
- External Secrets Operator (pull from vault/AWS Secrets Manager)
- Common mistakes: base64 ≠ encryption, exposed in logs

**Spaced Repetition**:
- **Introduces**: Service account tokens, role vs clusterrole, sealed secrets, external secrets
- **Reinforces**: RBAC from Ep 1 checklist item #3, security baseline item #6

**Active Recall Moments**:
- Start: "Recall: Why is RBAC a production concern, not just dev?"
- Mid: "Pause: What's wrong with this RoleBinding? [shows cluster-admin example]"
- Mid: "Why is base64-encoding NOT encryption?"
- End: "List 3 RBAC misconfigurations to avoid"
- End: "When would you use Sealed Secrets vs External Secrets Operator?"

**Prerequisites**: Episode 1
**Leads to**: Episode 10 (multi-cluster RBAC and policy enforcement)

---

#### Episode 4: Troubleshooting Crashes - CrashLoopBackOff & Beyond
**Duration**: 15 min
**Learning Objectives**:
- Execute systematic troubleshooting workflow for pod failures (describe → logs → events)
- Diagnose CrashLoopBackOff, ImagePullBackOff, and Pending states
- Configure effective health checks (liveness and readiness probes) that prevent false failures

**Covers**:
- The systematic troubleshooting workflow (kubectl describe → logs → events)
- **CrashLoopBackOff**: Application crashes vs infrastructure issues
  - Exit codes (137 = OOMKilled, 1 = app error)
  - Backoff delay pattern (why restarts slow down)
- **ImagePullBackOff**: Registry authentication, image not found, tag issues
- **Pending Pods**: Scheduling failures (resource constraints, node selectors, affinity)
- Health checks that actually work:
  - Liveness probes (restart if unhealthy)
  - Readiness probes (remove from load balancer if not ready)
  - Startup probes (for slow-starting apps)
  - Common mistakes (too aggressive timeouts, wrong endpoints)
- Building a team runbook

**Spaced Repetition**:
- **Introduces**: kubectl debugging workflow, probe configurations, pod lifecycle, exit codes
- **Reinforces**: Health checks (from Ep 1 checklist item #2), resource constraints (from Ep 2)

**Active Recall Moments**:
- Start: "Recall: What's the difference between liveness and readiness probes?"
- Mid: "You see CrashLoopBackOff. What's your first kubectl command?"
- Mid: "Pause: What exit code indicates OOMKilled?"
- End: "Describe the full troubleshooting workflow from first symptom to resolution"

**Prerequisites**: Episodes 1, 2
**Leads to**: Episodes 6-7 (networking and observability extend troubleshooting)

---

#### Episode 5: StatefulSets & Persistent Storage
**Duration**: 15 min
**Learning Objectives**:
- Determine when to use StatefulSets vs Deployments with PVCs
- Configure dynamic volume provisioning with Storage Classes
- Diagnose common storage failures (PVC stuck pending, volume not mounting)

**Covers**:
- **StatefulSets vs Deployments**: When stable network identity matters
  - Databases, caches, message queues need StatefulSets
  - Stable DNS names, ordered deployment/scaling
  - Persistent storage per pod
- **Storage Architecture**:
  - PersistentVolumes (PV) vs PersistentVolumeClaims (PVC)
  - Storage Classes (dynamic provisioning)
  - Access modes: ReadWriteOnce (RWO) vs ReadWriteMany (RWX)
  - CSI drivers and why they matter
- **Common Storage Failures**:
  - PVC stuck in Pending (no PV matches, quota exceeded)
  - Volume not mounting (CSI driver issues, node scope problems)
  - Volume claim templates can't be resized (design limitation)
- **Production Patterns**:
  - Backup strategies (Velero introduction)
  - Database operator patterns (PostgreSQL, MySQL, MongoDB operators)
  - When to use cloud-managed databases vs K8s-hosted

**Spaced Repetition**:
- **Introduces**: StatefulSets, PV/PVC, Storage Classes, CSI drivers, Velero
- **Reinforces**: Pod scheduling (from Ep 4), resource allocation (from Ep 2)

**Active Recall Moments**:
- Start: "Recall: What production workloads need persistence?"
- Mid: "Before we continue: StatefulSets vs Deployments - when do you use which?"
- Mid: "Your PVC is stuck Pending. What are the 3 most common causes?"
- End: "Explain the PV/PVC relationship in your own words"

**Prerequisites**: Episodes 1, 4
**Leads to**: Episode 7 (monitoring storage metrics), Episode 10 (DR and backup at scale)

---

#### Episode 6: Networking & Ingress
**Duration**: 18 min
**Learning Objectives**:
- Explain Kubernetes networking model and CNI plugin responsibilities
- Choose appropriate Service type and Ingress controller for production use cases
- Determine when service mesh adds value vs unnecessary complexity

**Covers**:
**Kubernetes Networking (8 min)**:
- Networking model: flat namespace, every pod gets IP
- L4 (Transport) vs L7 (Application) layer distinction
- CNI plugins: What they do, when they break
  - Calico, Cilium, Flannel, Weave comparison
  - Network policy enforcement (CNI-dependent)
- Service types decision matrix:
  - ClusterIP: Internal only (default)
  - NodePort: Expose on every node (dev/testing)
  - LoadBalancer: Cloud LB (production external)
  - ExternalName: DNS alias

**Ingress Controllers (6 min)**:
- Why you need Ingress (L7 routing, TLS termination)
- Nginx Ingress vs Traefik vs cloud LBs (ALB, GCP LB)
- Path-based and host-based routing
- TLS termination and cert-manager
- Common issues: 502 bad gateway, TLS handshake failures

**Service Mesh (4 min)**:
- When you need service mesh (and when you don't)
  - Observability, mTLS, traffic management
  - Istio vs Linkerd trade-offs
  - Cost of complexity (don't over-engineer)
- Network policies for production isolation

**Spaced Repetition**:
- **Introduces**: CNI, ingress controllers, service mesh, network policies, cert-manager
- **Reinforces**: Networking failure pattern (from Ep 1), troubleshooting (from Ep 4)

**Active Recall Moments**:
- Start: "Recall: What layer does CNI operate at vs service mesh?"
- Mid: "Your pods can't reach a service. Walk through your debugging approach."
- Mid: "When would you use NodePort vs LoadBalancer?"
- End: "You're asked to implement service mesh. What questions do you ask first?"

**Prerequisites**: Episodes 1, 4
**Leads to**: Episode 7 (network observability), Episode 10 (multi-cluster networking)

---

#### Episode 7: Observability - Metrics, Logging, Tracing
**Duration**: 15 min
**Learning Objectives**:
- Deploy Prometheus with persistent storage and service discovery
- Design actionable alerts using golden signals (latency, traffic, errors, saturation)
- Determine when to use metrics vs logs vs traces for debugging

**Covers**:
**Metrics with Prometheus (7 min)**:
- Why default Prometheus install isn't production-ready
  - Needs persistent storage, security, federation
- Prometheus Operator vs Helm deployment patterns
- Service discovery and label design
  - ServiceMonitors (how Prometheus finds targets)
  - Label best practices (avoid high cardinality)
- PromQL basics for troubleshooting:
  - `rate(http_requests_total[5m])`
  - `container_memory_usage_bytes`
- Retention policies and storage costs

**Logging (4 min)**:
- Log aggregation architecture (Loki, ELK stack)
- Structured logging (JSON) vs unstructured
- Log retention and cost management
- Common pattern: Fluentd/Fluent Bit → Loki → Grafana

**Alerting (3 min)**:
- Designing actionable alerts (not noisy)
- Golden signals: Latency, Traffic, Errors, Saturation
- Alertmanager: grouping, routing, silencing
- Alert fatigue prevention

**Tracing (1 min)**:
- When you need distributed tracing (microservices)
- Jaeger/Tempo quick overview
- Metrics vs logs vs traces decision framework

**Spaced Repetition**:
- **Introduces**: Prometheus, PromQL, Alertmanager, Loki, golden signals, tracing
- **Reinforces**: Monitoring from Ep 1 checklist item #5, troubleshooting from Ep 4

**Active Recall Moments**:
- Start: "Recall: Why is observability non-optional in production?"
- Mid: "Before we continue: What are the 4 golden signals?"
- Mid: "You're designing alerts for a web service. What would you alert on?"
- End: "When would you use metrics vs logs vs traces?"

**Prerequisites**: Episodes 1, 4, 5, 6
**Leads to**: Episode 10 (observability at multi-cluster scale)

---

### MODULE 3: OPERATIONS AT SCALE (Episodes 8-10)

#### Episode 8: Cost Optimization at Scale
**Duration**: 12 min
**Learning Objectives**:
- Identify the 5 primary sources of Kubernetes cost waste
- Right-size resources to balance performance and cost using FinOps principles
- Implement cost controls (quotas, limits, autoscaling) across environments

**Covers**:
- Why K8s costs spiral (the 20+ cluster problem, 2/3 see TCO growth)
- **The 5 Cost Waste Sources**:
  1. Over-provisioned resource requests (biggest waste)
  2. Missing resource limits (allowing overcommit)
  3. Idle resources (dev/test running 24/7)
  4. No autoscaling (paying for peak capacity always)
  5. Lack of visibility (can't optimize what you can't measure)
- **Right-sizing strategies** (revisits Episode 2):
  - Analyzing actual vs requested resources
  - Vertical Pod Autoscaler (VPA) for recommendations
  - Load testing to validate changes
- **Cost controls**:
  - Namespace ResourceQuotas and LimitRanges
  - Cluster Autoscaler (scale nodes based on demand)
  - Spot instances for batch workloads
- **FinOps tools**: Kubecost, cloud provider cost explorers
- **The "senior engineer problem"**: Over-engineering costs money
  - Do you really need that service mesh?
  - 3 replicas vs 5 replicas trade-off

**Spaced Repetition**:
- **Introduces**: FinOps, autoscaling, spot instances, quotas, cost visibility
- **Reinforces**: Resource management (from Ep 2), production checklist

**Active Recall Moments**:
- Start: "Recall from Ep 2: What's the impact of missing resource requests on cost?"
- Mid: "Before we continue, name the 5 sources of cost waste"
- Mid: "Your dev clusters cost as much as production. What's your first investigation?"
- End: "Name 3 cost optimization techniques you'd implement tomorrow"

**Prerequisites**: Episodes 1, 2
**Leads to**: Episode 10 (cost management at multi-cluster scale)

---

#### Episode 9: GitOps & Deployment Automation
**Duration**: 15 min
**Learning Objectives**:
- Implement GitOps principles with ArgoCD or Flux
- Choose between Helm and Kustomize for configuration management
- Configure deployment strategies (canary, blue/green) beyond rolling updates

**Covers**:
**GitOps Principles (3 min)**:
- Git as source of truth for infrastructure
- Declarative config + version control + automated sync
- Why manual kubectl doesn't scale to 20+ clusters
- Audit trail and rollback capabilities

**ArgoCD vs Flux (5 min)**:
- **ArgoCD**: Web UI, multi-tenancy, RBAC, larger ecosystem
  - Best for: Large teams, need UI, multi-cluster from day 1
  - Challenges: More complex, heavier weight
- **Flux**: Lightweight, CLI-driven, CNCF graduated
  - Best for: GitOps-native teams, automation-first
  - 2024 note: Weaveworks shutdown, but CNCF-backed
- When to use which (decision framework)

**Helm vs Kustomize (3 min)**:
- **Helm**: Templating, package manager, charts
  - When: Complex apps, need versioning, external charts
- **Kustomize**: Overlays, template-free, native to kubectl
  - When: Simpler needs, prefer declarative, avoid templating
- Can use both (Helm charts + Kustomize overlays)

**Deployment Strategies (3 min)**:
- Rolling updates (default, gradual replacement)
- Blue/Green (two environments, instant switch)
- Canary (gradual traffic shift with validation)
- Argo Rollouts for advanced strategies

**CI/CD Integration (1 min)**:
- Build → Test → Update Git → GitOps tool deploys
- Image promotion across environments

**Spaced Repetition**:
- **Introduces**: GitOps, ArgoCD, Flux, Helm, Kustomize, deployment strategies
- **Reinforces**: Production checklist (GitOps is how you achieve consistency)

**Active Recall Moments**:
- Start: "Recall from Ep 1: Why is 'kubectl apply' in production an anti-pattern?"
- Mid: "ArgoCD or Flux: Which would you choose for a 50-person eng team? Why?"
- Mid: "Pause: When would you use Helm vs Kustomize?"
- End: "Explain GitOps principles in your own words"

**Prerequisites**: Episodes 1-8
**Leads to**: Episode 10 (GitOps for multi-cluster management)

---

#### Episode 10: Multi-Cluster Management & Course Synthesis
**Duration**: 15 min
**Learning Objectives**:
- Design multi-cluster strategies that scale to 20+ clusters
- Apply production patterns consistently across environments using GitOps
- Synthesize all course concepts into cohesive production operations framework

**Covers**:
**Multi-Cluster Realities (3 min)**:
- Average org: 20+ clusters across 4+ environments
- Why multi-cluster: Isolation, compliance, availability, blast radius
- Challenges: Configuration drift, cost visibility, RBAC sprawl

**GitOps for Fleet Management (4 min)**:
- Hub-and-spoke model (centralized Git, distributed ArgoCD/Flux)
- App-of-apps pattern (ArgoCD)
- Kustomize overlays per environment
- Policy enforcement at scale (OPA/Gatekeeper, Kyverno)

**Disaster Recovery (2 min)**:
- Backup strategies (Velero for etcd + volumes)
- RTO/RPO considerations
- Multi-region failover patterns

**Operations Patterns That Scale (2 min)**:
- Standardized base configs (golden images)
- Progressive rollouts (test → staging → prod)
- Observability federation (central Prometheus)
- Cost allocation per team/env

**Course Synthesis (4 min)**:
**Rapid Review** - Active recall across all episodes:
- "What's the production mindset?" (Ep 1)
- "How do you prevent OOMKilled?" (Ep 2)
- "Name 3 RBAC mistakes" (Ep 3)
- "CrashLoopBackOff debugging steps?" (Ep 4)
- "StatefulSets vs Deployments decision?" (Ep 5)
- "When do you need a service mesh?" (Ep 6)
- "What are the golden signals?" (Ep 7)
- "Top 3 cost waste sources?" (Ep 8)
- "ArgoCD vs Flux - when to use which?" (Ep 9)

**The Complete Production Checklist**:
Walk through all 6 items with depth from course:
1. Resources (Ep 2)
2. Health checks (Ep 4)
3. RBAC + Secrets (Ep 3)
4. Multi-replica (Eps 1, 9)
5. Observability (Ep 7)
6. Security baseline (Ep 3, 6)

**Next Steps**:
- CKA certification (covers Episodes 1-6 heavily)
- CKAD certification (app deployment focus)
- CKS certification (security focus, Ep 3)
- Advanced topics: Custom operators, eBPF, platform engineering

**Spaced Repetition**:
- **Introduces**: Fleet management, policy as code, disaster recovery
- **Reinforces**: ALL concepts from Episodes 1-9 (comprehensive synthesis)

**Active Recall Moments**:
- Throughout: Questions from each previous episode
- End: "You're designing a new production cluster from scratch. Walk me through your complete checklist and decision process."
- End: "What was the most valuable concept you learned in this course? Why?"

**Prerequisites**: Episodes 1-9 (requires ALL previous episodes)
**Leads to**: Continuous learning, certifications, advanced topics

---

## Spaced Repetition Map (10 Episodes)

```
Production Mindset (Ep 1)
├─ Referenced: Every episode uses production thinking
├─ Applied: Ep 8 (cost), Ep 9 (GitOps), Ep 10 (scale)
└─ Mastered: Ep 10 (decision-making across all scenarios)

Resource Limits/Requests (Ep 1 intro, Ep 2 deep)
├─ Referenced: Ep 1, Ep 2, Ep 4, Ep 8, Ep 10
├─ Deepened: Ep 8 (cost optimization context)
└─ Mastered: Ep 10 (right-sizing at scale)

RBAC & Security (Ep 1 intro, Ep 3 deep)
├─ Referenced: Ep 1, Ep 3, Ep 10
├─ Applied: Ep 9 (GitOps RBAC), Ep 10 (multi-cluster policies)
└─ Mastered: Ep 10 (policy enforcement at scale)

Health Checks (Ep 1 intro, Ep 4 deep)
├─ Referenced: Ep 1, Ep 4, Ep 9, Ep 10
├─ Debugged: Ep 4 (CrashLoopBackOff)
└─ Mastered: Ep 10 (runbook integration)

StatefulSets & Storage (Ep 5)
├─ Referenced: Ep 5, Ep 7 (monitoring), Ep 10 (DR)
├─ Applied: Ep 10 (backup strategies)
└─ Mastered: Ep 10 (database operations at scale)

Networking (Ep 1 intro, Ep 6 deep)
├─ Referenced: Ep 1, Ep 4, Ep 6, Ep 7, Ep 10
├─ Troubleshot: Ep 4 (connectivity), Ep 6 (ingress issues)
└─ Mastered: Ep 10 (multi-cluster networking)

Observability (Ep 1 intro, Ep 7 deep)
├─ Referenced: Ep 1, Ep 4, Ep 7, Ep 10
├─ Applied: Ep 4 (troubleshooting), Ep 8 (cost visibility)
└─ Mastered: Ep 10 (observability federation)

Cost Optimization (Ep 1 intro, Ep 8 deep)
├─ Referenced: Ep 1, Ep 2, Ep 8, Ep 10
├─ Applied: Ep 8 (FinOps techniques)
└─ Mastered: Ep 10 (cost at multi-cluster scale)

GitOps (Ep 9)
├─ Mentioned: Ep 1 (anti-pattern: manual kubectl)
├─ Deep: Ep 9 (ArgoCD/Flux, deployment strategies)
└─ Mastered: Ep 10 (fleet management)

Production Checklist (Ep 1)
├─ Referenced: Every single episode
├─ Expanded: Eps 2-7 (each adds depth to checklist items)
└─ Mastered: Ep 10 (complete checklist application)
```

## Concept Dependency Graph

```
Episode 1 (Production Mindset)
├─┬─> Episode 2 (Resource Management)
│ │   └─> Episode 8 (Cost Optimization)
│ │
│ ├─> Episode 3 (RBAC & Secrets)
│ │
│ ├─> Episode 4 (Troubleshooting Crashes)
│ │   ├─> Episode 5 (StatefulSets & Storage)
│ │   ├─> Episode 6 (Networking & Ingress)
│ │   └─> Episode 7 (Observability)
│ │
│ └─> Episode 9 (GitOps)
│     └─> Episode 10 (Multi-Cluster & Synthesis)
│         └─ Integrates ALL concepts
```

## Learning Checkpoints

**After Episode 1**:
- [ ] Can explain production vs dev mindset difference
- [ ] Can list 5 production failure patterns
- [ ] Can recite 6-item production readiness checklist

**After Episode 5** (Mid-course):
- [ ] Can debug OOMKilled errors systematically
- [ ] Can implement namespace-scoped RBAC and sealed secrets
- [ ] Can troubleshoot CrashLoopBackOff, ImagePullBackOff, Pending
- [ ] Can identify resource misconfigurations
- [ ] Can design StatefulSet for database workload

**After Episode 7** (Operations Foundations Complete):
- [ ] Can deploy stateful workloads (databases, caches)
- [ ] Can configure ingress with TLS termination
- [ ] Can deploy Prometheus with service discovery
- [ ] Can design actionable alerts using golden signals

**After Episode 10** (Course Complete):
- [ ] Can design production-ready Kubernetes configurations
- [ ] Can debug complex multi-layer problems
- [ ] Can implement GitOps with ArgoCD or Flux
- [ ] Can optimize costs using FinOps techniques
- [ ] Can operate clusters at scale (20+)
- [ ] Can teach production patterns to team members
- [ ] **Ready for CKA certification exam**

## What Makes This 10-Episode Curriculum Complete

**vs 7-Episode Version - Critical Additions**:

1. **Episode 5: StatefulSets** - Database/cache workloads (was completely missing)
2. **Episode 7: Observability** - Prometheus/logging (was "you need monitoring" without teaching how)
3. **Episode 9: GitOps** - ArgoCD/Flux (was mentioned in Ep 7 but not taught)

**Plus Expansions**:
- **Episode 3**: Added secrets management (Sealed Secrets, External Secrets)
- **Episode 6**: Added Ingress controllers and cert-manager
- **Episode 10**: Refocused on multi-cluster (review is in spaced repetition)

**Result**: Complete production operations toolkit, not just failure pattern diagnosis.

## Success Metrics

**Learner Outcomes**:
- Can pass CKA practice exams after course (80%+ success rate)
- Can debug production issues 50% faster (measure MTTR improvement)
- Fewer production incidents from common mistakes
- Team members reference course content in PRs/designs

**Engagement**:
- Episode completion rate >80%
- Return for subsequent episodes >75%
- Community contributions (corrections, additions)
- Certification pass rate for learners

**Business Impact**:
- Reduced K8s-related incidents (measure incident count)
- Faster MTTR (mean time to resolution)
- Lower cloud costs (measure FinOps application)
- Improved security posture (RBAC audit findings)
