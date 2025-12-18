# Episode #062: Kubernetes 1.35 "Timbernetes" - The End of the Pod Restart Era

## Viral Angle
"In-Place Vertical Scaling goes GA in Kubernetes 1.35 - you NEVER have to restart pods to change CPU/memory again. Plus: cgroup v1 is REMOVED (not deprecated - GONE), containerd 1.x reaches EOL, and native Pod certificates eliminate cert-manager for workload identity."

## Target Duration: 15-20 minutes

---

## NEWS SEGMENT (3-4 min)

### 1. Docker Hardened Images Now FREE
- Docker releases 1,000+ hardened container images under Apache 2.0
- 95% CVE reduction compared to community images
- Distroless runtime, full SBOM, SLSA Level 3 provenance
- Includes hardened MCP servers (Grafana, MongoDB, GitHub)
- No subscription required - just authenticate with Docker Hub
- URL: https://www.docker.com/blog/docker-hardened-images-for-every-developer/

### 2. GitHub Actions Pricing Changes (January 2026)
- Up to 39% cost reduction on hosted runners
- New $0.002/minute platform charge (included in reduced rates)
- Self-hosted runner billing POSTPONED indefinitely after community backlash
- 96% of customers see no bill changes
- Public repos remain FREE
- URL: https://resources.github.com/actions/2026-pricing-changes-for-github-actions/

### 3. First Linux Kernel Rust CVE
- CVE-2025-68260: Race condition in Android Binder Rust rewrite
- Affects Linux 6.18+ with Rust Binder driver
- Results in crash (DoS) - NOT remote code execution
- Vulnerability in unsafe code blocks
- Greg Kroah-Hartman: "Routine consequence of expanding Rust integration"
- URL: https://www.phoronix.com/news/First-Linux-Rust-CVE

### 4. KubeVirt Security Audit Complete
- OSTIF/Quarkslab audit: 37 days, 15 findings
- 1 High, 7 Medium, 4 Low, 3 Informational
- Strong architecture: "sandboxing and isolation limit exploit impact"
- CVE-2025-64324 identified and remediated
- URL: https://www.cncf.io/blog/2025/12/17/kubevirt-undergoes-ostif-security-audit/

---

## MAIN TOPIC: Kubernetes 1.35 "Timbernetes" (12-15 min)

### Opening Hook (30s)
- "If you've ever had to restart a production pod just to give it more memory, that era is officially over."
- K8s 1.35 released December 17, 2025
- 60 enhancements: 17 Stable, 19 Beta, 22 Alpha
- Codename "Timbernetes" from Norse mythology's Yggdrasil (World Tree)

### Section 1: In-Place Pod Vertical Scaling Goes GA (3-4 min)
**KEP #1287 - The Headline Feature**
- Before: Change CPU/memory = delete pod, create new pod, lose connections, downtime
- After: Patch pod spec, kubelet adjusts cgroups, container keeps running
- Technical: `.spec.containers[*].resources` now mutable
- New fields: `.status.resize` (InProgress/Deferred/Infeasible/Proposed)
- Works with: CPU, memory requests/limits
- NOT supported yet: ephemeral storage, extended resources

**Why This Matters for Platform Engineers:**
- Stateful workloads (databases, caches) - no more planned downtime for scaling
- Batch processing - adjust resources mid-job based on actual needs
- Cost optimization - right-size pods without disruption
- VPA (Vertical Pod Autoscaler) can now apply recommendations without restarts

**Technical Deep Dive:**
- Kubelet handles resize via cgroup manipulation
- Container runtime interface (CRI) extended for resize operations
- Pod conditions track resize state
- QoS class can change during resize (Guaranteed → Burstable)

### Section 2: The Breaking Changes - What's REMOVED (3-4 min)

**cgroup v1 Support REMOVED (Not Deprecated - GONE)**
- If your nodes still use cgroup v1, upgrade BLOCKED
- Check: `stat -fc %T /sys/fs/cgroup/`
- v1 shows `tmpfs`, v2 shows `cgroup2fs`
- Most modern distros (Ubuntu 22.04+, RHEL 9+, Debian 12+) already default to v2
- Impact: Legacy systems, older container runtimes

**containerd 1.x Reaches End of Life**
- containerd 2.0 required for K8s 1.35
- Breaking CRI changes in containerd 2.0
- Check your runtime version before upgrading

**IPVS Mode Formally Deprecated**
- kube-proxy IPVS mode marked deprecated
- Recommendation: Use iptables or migrate to Cilium/other CNI-native proxying
- Not removed yet, but sunset timeline established

### Section 3: Security Improvements (2-3 min)

**Pod Certificates for Workload Identity (Beta) - KEP #4317**
- Native mTLS without cert-manager or SPIFFE/SPIRE
- Kubelet generates keys, requests certs via PodCertificateRequest
- API server enforces node restriction at admission
- Credentials written directly to pod filesystem
- Automated rotation built-in
- Use case: Service mesh, zero-trust architectures

**Node Declared Features Before Scheduling (Alpha) - KEP #5328**
- Problem: New control plane can schedule pods to old nodes lacking features
- Solution: Node declares `.status.declaredFeatures`
- Scheduler/admission can enforce compatibility
- Critical for heterogeneous clusters, skew policy compliance

### Section 4: Networking and Scheduling (2-3 min)

**PreferSameNode Traffic Distribution (GA) - KEP #3015**
- New `trafficDistribution: PreferSameNode` strictly prioritizes local endpoints
- `PreferClose` renamed to `PreferSameZone` (backward compatible)
- Explicit control: node-local vs zone-local vs any endpoint
- Impact: Lower latency, reduced cross-zone traffic costs

**Job API `managedBy` Mechanism (GA) - KEP #4368**
- `.spec.managedBy` allows external controller to handle Job status
- Use case: MultiKueue multi-cluster dispatch
- Prevents conflicts between built-in Job controller and custom schedulers

**Gang Scheduling for AI Workloads (Alpha)**
- Schedule multiple pods atomically or not at all
- Critical for distributed ML training (need all GPUs available)
- Works with DRA for GPU resource allocation

### Section 5: DRA and AI Infrastructure (2 min)

**Dynamic Resource Allocation Updates**
- DRA Core went GA in 1.34, feature gate now LOCKED in 1.35 (cannot disable)
- New alpha: Device Binding Conditions (KEP #5007)
  - Defer pod binding until external resources confirmed ready
  - Use case: Fabric-attached GPUs, FPGAs
- New alpha: Partitionable Devices (KEP #4815)
  - Dynamic device partitioning within DRA structured parameters
  - Vendors can advertise overlapping partitions created on-demand

### Section 6: Other Notable Changes (1-2 min)

**Pod `.metadata.generation` Field (GA) - KEP #5067**
- Tracks spec changes like Deployments already do
- `.status.observedGeneration` confirms kubelet processed change
- Essential for In-Place Pod Vertical Scaling verification

**NUMA Node Limit Configurable (GA) - KEP #4622**
- `max-allowable-numa-nodes` option (was hard-coded to 8)
- Supports modern high-end servers with >8 NUMA nodes

**Expose Node Topology Labels via Downward API (Beta)**
- Access `topology.kubernetes.io/zone` and `region` in pods
- No RBAC needed, no API server queries
- Safer topology-aware applications

---

## PRACTICAL GUIDANCE (2-3 min)

### Upgrade Checklist
1. **cgroup version**: Verify all nodes use cgroup v2
2. **Container runtime**: Ensure containerd 2.0+ or compatible CRI
3. **IPVS usage**: Plan migration if using kube-proxy IPVS mode
4. **Test In-Place Scaling**: Validate with non-critical workloads first
5. **Review VPA settings**: In-place scaling changes VPA behavior

### When to Upgrade
- **Wait for 1.35.1**: First patch typically within 2 weeks
- **Staging first**: Test breaking changes in non-production
- **Managed K8s**: EKS/GKE/AKS typically 2-4 months behind

### What to Try First
- In-Place Pod Vertical Scaling on dev clusters
- PreferSameNode for latency-sensitive services
- Pod Certificates if evaluating workload identity solutions

---

## CLOSING (30s)

Key takeaway: Kubernetes 1.35 is a maturity release. In-place scaling removes a fundamental operational pain point, while the deprecations show the project cleaning up technical debt.

The message to platform teams: 2025 was the year Kubernetes stopped asking you to accept Pod restarts as the cost of doing business.

---

## SOURCES
- https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/
- https://github.com/kubernetes/kubernetes/releases/tag/v1.35.0
- https://thenewstack.io/kubernetes-1-35-timbernetes-introduces-vertical-scaling/
- https://cloudsmith.com/blog/kubernetes-1-35-what-you-need-to-know
- https://scaleops.com/blog/kubernetes-1-35-release-overview/
- https://www.techzine.eu/news/applications/137373/kubernetes-v1-35-more-secure-more-flexible-no-more-to-ingress-nginx/
