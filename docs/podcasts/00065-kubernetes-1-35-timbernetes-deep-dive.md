---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #065: Kubernetes 1.35 Deep Dive"
slug: 00065-kubernetes-1-35-timbernetes-deep-dive
---

# Episode #065: Kubernetes 1.35 Timbernetes Deep Dive

<GitHubButtons/>

<iframe width="100%" style={{aspectRatio: '16/9', marginBottom: '1rem'}} src="https://www.youtube.com/embed/rixhTwyXH2k" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

**Duration**: 20 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Platform engineers, Kubernetes operators, SREs

## Episode Summary

Kubernetes 1.35 "Timbernetes" dropped on December 17, 2025, and this is one of those releases that fundamentally changes how we operate clusters. This deep dive covers 60 enhancements, 3 breaking changes that will bite you if you're not prepared, and a headline feature six years in the making: In-Place Pod Resize graduating to GA.

## Key Takeaways

- **Breaking Change #1**: cgroup v1 is REMOVED (not deprecated) - kubelet will refuse to start on cgroup v1 nodes
- **Breaking Change #2**: containerd 1.x reaches end of support - upgrade to containerd 2.0+ before upgrading Kubernetes
- **Breaking Change #3**: IPVS mode in kube-proxy is deprecated - migrate to nftables mode (deadline ~1.38)
- **In-Place Pod Resize GA** (KEP-1287): 6 years from proposal to stable - resize CPU/memory without pod restart
- **Pod Certificates Beta** (KEP-4317): Native workload identity with kubelet-managed mTLS certificates
- **Gang Scheduling Alpha** (KEP-4671): Native all-or-nothing scheduling for AI/ML workloads via Workload/PodGroup API
- **DRA (Dynamic Resource Allocation)**: Now stable and locked to enabled - cannot be disabled
- **Node Declared Features** (KEP-5328): Nodes report supported features for version-skew-aware scheduling
- **Practical Advice**: Prioritize infrastructure modernization (cgroup v2, containerd 2.0, nftables) before adopting new features

## Resources

- [Kubernetes 1.35 Release Blog](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/) - Official release announcement
- [KEP-1287: In-Place Pod Resize](https://github.com/kubernetes/enhancements/issues/1287) - Feature proposal and design
- [KEP-4317: Pod Certificates](https://github.com/kubernetes/enhancements/issues/4317) - Workload identity specification
- [KEP-4671: Gang Scheduling](https://github.com/kubernetes/enhancements/issues/4671) - Native gang scheduling design
- [cgroup v2 Documentation](https://kubernetes.io/docs/concepts/architecture/cgroups/) - Migration guide

## Transcript

**Jordan**: Kubernetes 1.35 dropped on December seventeenth, and this is one of those releases that fundamentally changes how we operate clusters. Today we're doing a deep dive into Timbernetes, the World Tree Release. Sixty enhancements, three breaking changes that will bite you if you're not prepared, and a headline feature six years in the making. Let's break it all down.

**Alex**: The release name is poetic. Timbernetes, inspired by Yggdrasil, the Norse world tree. The logo shows Earth at the center of a glowing tree, surrounded by three squirrels representing the release crew roles. Reviewers carry scrolls, warriors defend with shields, and rogues illuminate the path with lanterns. It's a beautiful metaphor for how Kubernetes development works.

**Jordan**: But let's get past the poetry and into what matters operationally. Sixty total enhancements: seventeen graduating to stable, nineteen entering beta, twenty-two new alpha features. This is a substantial release. But before we celebrate the new features, we need to talk about what's being removed. Because if you don't prepare for these breaking changes, your clusters won't even start.

**Alex**: Starting with the biggest one: cgroup v1 is gone. Not deprecated. Removed. The kubelet will refuse to start on nodes running cgroup v1. This is a hard failure, not a warning. If you're running older Linux distributions that default to cgroup v1, your nodes are going to fail after the upgrade.

**Jordan**: Let me be specific about what this means technically. When the kubelet starts, it checks the cgroup version. In one point thirty-five, the failCgroupV1 flag is set to true by default. If you're on cgroup v1, the kubelet exits with an error. You can check your current version by running stat minus fc percent T slash sys slash fs slash cgroup. If it returns cgroup2fs, you're fine. If it returns tmpfs, you have a problem.

**Alex**: There is an escape hatch. You can set failCgroupV1 to false in the kubelet configuration file. But this is operationally dangerous. It's deferring the inevitable, and you lose access to features that require cgroup v2: Memory QoS, certain swap configurations, and PSI metrics. The right answer is to upgrade your node operating systems.

**Jordan**: The second breaking change: containerd 1.x reaches end of support. Kubernetes 1.35 is the last release that will work with containerd 1.7 or earlier. If you upgrade Kubernetes without upgrading containerd, your kubelet might not even start. The runtime discovery mechanism relies on features that older containerd versions don't support.

**Alex**: There's a metric you should be watching right now: kubelet underscore cri underscore losing underscore support. This will tell you which nodes in your cluster are running containerd versions that need to be upgraded. If you haven't already migrated to containerd 2.0 or later, that should be your immediate action item.

**Jordan**: The third breaking change is a deprecation rather than a removal, but it signals where Kubernetes networking is headed. IPVS mode in kube-proxy is now deprecated. You'll get a warning on startup, but it still works. The migration deadline is approximately 1.38, which gives you about a year.

**Alex**: Let me explain why IPVS is being deprecated. IPVS mode was introduced back in Kubernetes 1.8 as a high-performance alternative to iptables. And it succeeded in that goal. Better rule synchronization, higher throughput. But the kernel IPVS API turned out to be a poor match for the Kubernetes Services API. Edge cases around service functionality were never implemented correctly.

**Jordan**: The technical debt accumulated to the point where maintaining feature parity became impractical. The recommendation now is nftables mode. It's essentially a replacement for both iptables and IPVS, with better performance than either. It requires kernel 5.13 or later, which most modern distributions have.

**Alex**: So to summarize the upgrade checklist before we move on: verify cgroup v2 on every node, confirm containerd 2.0 or later, and start testing nftables mode in your staging environments. If you're running IPVS, begin planning your migration now.

**Jordan**: Now let's talk about the headline feature. In-place Pod resource updates have graduated to GA. This is KEP 1287, and it's been in development since 2019. Six years from proposal to stable release. This is the end of the kill-and-recreate era for vertical scaling.

**Alex**: Let me explain what this means practically. Previously, if you needed to change the CPU or memory allocation for a running container, you had to delete the Pod and create a new one. For stateless workloads, that's inconvenient but manageable. For stateful applications, long-running batch jobs, or AI training workloads, it's disruptive and sometimes impossible.

**Jordan**: With in-place Pod resize, you update the container's resource requests and limits in the Pod spec, and Kubernetes modifies the cgroup settings directly on the running container. The application continues running without interruption. No restart, no migration, no disruption.

**Alex**: There are two key concepts to understand. First, the container's spec dot resources field is now mutable for CPU and memory. This is where you specify what you want. Second, the status dot containerStatuses dot resources field shows what's actually configured. These might differ if the resize is pending or if the node can't accommodate the request.

**Jordan**: The implementation uses a new resize subresource on the Pod API. When you update the desired resources, the kubelet receives the change and attempts to resize the cgroup. If successful, the actual resources are updated to match. If the node doesn't have capacity, the resize is deferred and reattempted based on priority.

**Alex**: In 1.35, deferred resizes are prioritized by PriorityClass first, then QoS class, then how long the resize has been waiting. So if you have a critical production workload competing with a low-priority batch job for resources, the production workload gets priority.

**Jordan**: One major improvement from beta to GA: memory limit decreases are now supported. Previously, you could only increase memory limits. Now you can shrink over-provisioned Pods without recreation. The kubelet performs a best-effort check to see if the current memory usage exceeds the new limit, but this isn't guaranteed. Your application still needs to handle potential OOM scenarios.

**Alex**: Let's talk about use cases. Game servers adjusting resources based on player count. Pre-warmed workers that shrink when unused and inflate on first request. AI training jobs that need more resources during certain phases. JIT-compiled applications that need extra CPU at startup but can scale down once compilation is complete.

**Jordan**: The limitations are important to understand. In-place resize is currently prohibited when using Linux swap, static CPU Manager, or static Memory Manager. Only CPU and memory can be resized. Other resources remain immutable. And this requires cgroup v2, which ties back to our earlier discussion about the cgroup v1 removal.

**Alex**: The ecosystem integration is growing. VPA, the Vertical Pod Autoscaler, now has an InPlaceOrRecreate mode that graduated to beta. Ray Autoscaler plans to leverage this for training workload efficiency. There are known issues around kubelet-scheduler race conditions that the SIG is actively working on.

**Jordan**: Now let's shift to another major advancement: Pod Certificates, KEP 4317, which reached beta in 1.35. This is native workload identity for Kubernetes, and it dramatically simplifies service mesh and zero-trust architectures.

**Alex**: The problem this solves: when you're running microservices, Pods often need cryptographic identity to authenticate with each other using mutual TLS. Historically, you needed external projects like SPIFFE slash SPIRE or cert-manager to provision and rotate certificates. ServiceAccount tokens are designed for API server authentication, not general workload identity.

**Jordan**: With Pod Certificates, the kubelet itself generates keys and requests certificates via a new PodCertificateRequest API. The credentials are written directly to the Pod's filesystem through a projected volume. This happens automatically with managed rotation. No sidecars, no external controllers, no complex configuration.

**Alex**: The security model is solid. The kube-apiserver enforces node restriction at admission time. This eliminates the most common pitfall for third-party signers: accidentally violating node isolation boundaries. The certificates enable pure mTLS flows with no bearer tokens in the issuance path.

**Jordan**: For platform teams, this means you can implement zero-trust pod-to-pod communication without installing cert-manager or SPIRE. The feature is beta and enabled by default. It's ready for production testing, though you should validate it works with your specific security requirements.

**Alex**: Let's move to AI workloads. Kubernetes 1.35 introduces native gang scheduling support through a new Workload API and PodGroup concept. This is KEP 4671, and it's currently alpha.

**Jordan**: Gang scheduling implements an all-or-nothing strategy. A group of Pods is scheduled only if the cluster has sufficient resources for all members simultaneously. This is essential for distributed AI training, where you can't make progress if only half your workers are scheduled.

**Alex**: Previously, gang scheduling required external extensions like Volcano or Kueue. Those tools are still valuable for queue management and fair-share policies. But now Kubernetes handles the gang semantics natively. The scheduler waits until all pods in a group reach the same scheduling stage. If timeout occurs, all pods release their resources.

**Jordan**: The implementation introduces a Workload custom resource. Each Workload can contain multiple PodGroups, and each group can be independently gang-scheduled or not. Pods reference their Workload and PodGroup through a new WorkloadReference field that's immutable once set.

**Alex**: It's worth noting that the native implementation is basic compared to Volcano or Kueue. There's no queue management or fair-share policies in the core scheduler. For serious AI supercomputing, you'll still want Volcano or Kueue managing the queue strategy. The difference is now Kubernetes handles gang semantics natively, and your external orchestrator handles scheduling policy. Division of labor.

**Jordan**: Related to this, the Job API managedBy field has graduated to GA. This allows external controllers like Kueue to handle Job status synchronization. When a Job is created with a managedBy annotation, the built-in Job controller ignores it, letting the external controller manage the lifecycle.

**Alex**: Let's briefly cover some of the alpha features worth watching. There are twenty-two new alpha features, but a few stand out for platform engineering.

**Jordan**: Node Declared Features, KEP 5328, addresses version skew during cluster upgrades. Nodes now report their supported Kubernetes features via a new status.declaredFeatures field. The scheduler can use this to ensure pods are only placed on nodes that meet all feature requirements.

**Alex**: This solves a real operational problem. During rolling upgrades, you might have control plane nodes on 1.35 and worker nodes still on 1.34. Some pods might require 1.35 features. Without declared features, the scheduler has no way to know which nodes can support which capabilities.

**Jordan**: Device Binding Conditions, KEP 5007, defers pod binding until external resources like GPUs or FPGAs confirm readiness. This prevents premature binding and improves reliability for asynchronous or failure-prone resources. Essential for AI infrastructure.

**Alex**: Partitionable Devices, KEP 4815, enables dynamic device partitioning within the DRA framework. Vendors can advertise overlapping partitions that are created on-demand after allocation. Think GPU slicing where you create the partition only when the workload needs it.

**Jordan**: Extended Toleration Operators, KEP 5471, adds numeric comparison operators to taints and tolerations. You can now specify Greater Than or Less Than in addition to Equal and Exists. This enables SLA-based placement where pods require nodes with cost-reliability scores above a threshold.

**Alex**: Speaking of DRA, Dynamic Resource Allocation is now fully stable and locked to enabled. The feature gate cannot be disabled. This is the foundation for GPU scheduling, FPGA allocation, and any custom device types. If you're running AI workloads, DRA should be part of your operational knowledge.

**Jordan**: Let me walk through a practical upgrade checklist for platform teams. First, audit your infrastructure. Run the cgroup version check on every node. Check containerd versions. Identify any nodes running IPVS mode.

**Alex**: Second, test the breaking changes in a non-production environment. Verify your node images work with the kubelet's cgroup v2 requirement. Confirm containerd 2.0 or later is functioning correctly. Test nftables mode if you're currently on IPVS.

**Jordan**: Third, evaluate the new features for your use cases. If you're running VPA, test the in-place resize functionality. If you're doing pod-to-pod authentication, explore Pod Certificates. If you have AI training workloads, understand the gang scheduling API.

**Alex**: Fourth, update your operational runbooks. The in-place resize introduces new failure modes. Your monitoring should track the resize subresource. Your alerting should catch deferred resizes that never complete.

**Jordan**: Fifth, plan your containerd and kube-proxy migrations. You have runway on both. Containerd 1.x works in 1.35 but not beyond. IPVS works until approximately 1.38. Don't wait until the deadline.

**Alex**: The theme of this release is operational maturity. Features that have been alpha for years are finally graduating. In-place resize, six years. Pod certificates, the culmination of years of workload identity work. Gang scheduling, moving from external tools to native support.

**Jordan**: The breaking changes also signal maturity. Cgroup v2 has been the recommended configuration for years. Containerd 2.0 has been stable for a long time. Kubernetes is no longer supporting legacy configurations indefinitely. The platform is moving forward.

**Alex**: For platform engineers, the message is clear. Keep your infrastructure current. The kubernetes project is willing to break backwards compatibility when the benefits to the ecosystem outweigh the migration costs. If you're running old node images or container runtimes, you're accumulating technical debt.

**Jordan**: The in-place resize feature deserves extra attention. For years, vertical scaling meant pod recreation. That assumption is baked into how we design applications, how we configure VPA, how we think about stateful workloads. That assumption is no longer valid.

**Alex**: This opens up new patterns. Workloads that self-adjust resources based on internal metrics. Operators that right-size pods without disruption. Batch jobs that request more resources during expensive phases. The possibilities expand significantly.

**Jordan**: Gang scheduling is equally transformative for AI infrastructure. Previously, getting gang semantics meant adopting Volcano or Kueue and accepting their scheduling paradigms. Now you have options. Use native gang scheduling for simple cases. Layer Kueue on top for queue management. The architecture is more flexible.

**Alex**: Pod Certificates simplify security architectures. Service meshes that previously required complex sidecar injection and external certificate authorities can now leverage native kubelet-managed certificates. Zero-trust networking becomes easier to implement correctly.

**Jordan**: My practical advice: don't rush to adopt everything at once. Prioritize the breaking changes first. Get your nodes on cgroup v2 and containerd 2.0. Start testing nftables mode. Once your foundation is solid, experiment with the new features in development environments.

**Alex**: Kubernetes 1.35 Timbernetes represents a maturation point. The platform is no longer just adding features. It's rationalizing existing capabilities, graduating long-standing proposals, and removing legacy baggage. The World Tree is growing stronger, but it's also pruning dead branches.

**Jordan**: That's our deep dive on Kubernetes 1.35. The release blog post on kubernetes.io has additional details and links to individual feature announcements. If you're managing Kubernetes clusters, this release demands attention to both the new capabilities and the breaking changes. Plan your upgrades carefully, test thoroughly, and embrace the operational improvements that six years of development have delivered.

**Alex**: The Kubernetes project continues to balance innovation with stability. Each release brings new capabilities while respecting the operational realities of production clusters. 1.35 is a particularly well-executed version of that balance. The breaking changes are well-telegraphed, the stable features are battle-tested, and the alpha previews show the direction for future releases.

**Jordan**: For platform engineering teams, the path forward is clear. Modernize your node infrastructure, embrace in-place scaling, explore native workload identity, and prepare for gang scheduling. Kubernetes 1.35 isn't just an upgrade. It's an opportunity to rethink how you operate your clusters.
