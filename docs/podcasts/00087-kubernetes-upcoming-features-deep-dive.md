---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #087: Kubernetes Upcoming Features Deep Dive"
slug: 00087-kubernetes-upcoming-features-deep-dive
---

# Episode #087: Kubernetes Upcoming Features Deep Dive - Extended Toleration Operators and Mutable PV Node Affinity

<GitHubButtons/>

**Duration**: 41 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Platform engineers, DevOps engineers, SREs, Kubernetes administrators

> 📰 **News Segment**: This episode covers OpenEverest, GKE Agent Sandbox, MongoBleed vulnerability, and predictive capacity planning before the main topic.

<iframe width="100%" style={{aspectRatio: '16/9', marginTop: '1rem', marginBottom: '1rem'}} src="https://www.youtube.com/embed/UHBWGQJg7a4" title="Episode #087: Kubernetes Upcoming Features Deep Dive - Extended Toleration Operators" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Episode Summary

There's a Kubernetes cluster out there right now burning ten thousand dollars a month on GPU nodes that sit idle sixty percent of the time. Why? Because the scheduler can't say "only schedule pods on nodes with MORE than four GPUs." It's 2026, and our scheduler still can't count. But that's about to change.

This episode dives deep into two alpha features in Kubernetes 1.35 that represent a fundamental shift in how Kubernetes handles scheduling and storage: **Extended Toleration Operators** (KEP-5471) that finally let the scheduler do math, and **Mutable PersistentVolume Node Affinity** (KEP-5381) that lets storage topology adapt to reality. Plus, we connect this to the bigger picture: Kubernetes evolving from reactive feedback loops to truly predictive infrastructure.

## News Segment

**OpenEverest** - Percona's database platform goes open governance with multi-vendor support. Now supporting MySQL, PostgreSQL, MongoDB, and Valkey with modular architecture. Positioning for CNCF involvement and ecosystem growth.

**GKE Agent Sandbox** - Google launches kernel-level isolation for AI agent code execution using gVisor. Features pre-warmed sandbox pools with sub-second latency and Pod Snapshots for near-instant restore. Being built as an open-source Kubernetes SIG Apps subproject.

**MongoBleed (CVE-2025-14847)** - High-severity vulnerability affecting MongoDB's zlib-based network message decompression. CVSS 8.7, unauthenticated remote exploitation. Approximately 87,000 potentially exposed servers worldwide. Patch immediately.

**Predictive Capacity Planning** - Industry shift from reactive to proactive infrastructure. Machine learning models identify anomalies and predict capacity issues before they impact users.

## Key Takeaways

- **Extended Toleration Operators (Gt, Lt)**: New operators for numeric threshold-based scheduling - "I can tolerate risk up to 5%" or "need at least 4 GPUs"
- **Taints vs NodeAffinity**: Taints provide secure-by-default, node-centric control with eviction capabilities that NodeAffinity lacks
- **Mutable PV Node Affinity**: Storage topology that adapts without pod/PV recreation - critical for volume migrations
- **CSI Driver Integration**: Providers must implement nodeAffinity modification for full support
- **Validation Framework**: MutableNodeAffinity capability flag in CSIDriver spec controls permission
- **Kubernetes Evolution**: From reactive feedback loops to anticipation-based infrastructure

## Platform Team Action Items

1. **Enable feature gates** for testing: `TaintTolerationWithOperators` and `MutablePersistentVolumeNodeAffinity`
2. **Audit current taints** for numeric threshold candidates (GPU count, spot risk, cost tiers)
3. **Check CSI driver support** for mutableNodeAffinity capability
4. **Test Extended Tolerations** in non-production clusters before alpha graduation
5. **Document migration playbook** for volume nodeAffinity updates

## Resources

- [KEP-5471: Extended Toleration Operators](https://github.com/kubernetes/enhancements/tree/master/keps/sig-scheduling/5471-extended-toleration-operators) - Scheduling enhancement proposal
- [KEP-5381: Mutable PV Node Affinity](https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/5381-mutable-pv-node-affinity) - Storage enhancement proposal
- [OpenEverest](https://www.openeverest.io/) - Multi-database platform for Kubernetes
- [GKE Agent Sandbox](https://cloud.google.com/kubernetes-engine/docs/concepts/sandbox) - AI agent isolation documentation
- [MongoBleed CVE Details](https://www.infoq.com/news/2026/01/mongodb-mongobleed-vulnerability/) - Vulnerability coverage

## Transcript

**Jordan**: There's a Kubernetes cluster out there right now burning ten thousand dollars a month on GPU nodes that sit idle sixty percent of the time. Why? Because the scheduler can't say "only schedule pods on nodes with MORE than four GPUs." It's twenty twenty-six, and our scheduler still can't count. But that's about to change. Today we're talking about two alpha features in Kubernetes one point three five that represent a fundamental shift in how Kubernetes handles scheduling and storage. Extended Toleration Operators that finally let the scheduler do math, and Mutable PersistentVolume Node Affinity that lets storage topology adapt to reality. Plus, we'll connect this to the bigger picture: Kubernetes evolving from reactive feedback loops to truly predictive infrastructure.

**Alex**: Welcome to the Platform Engineering Playbook Daily Podcast. Today's news and a deep dive to help you stay ahead in platform engineering.

**Jordan**: Today we're diving into Kubernetes upcoming features, specifically Extended Toleration Operators for numeric comparisons and Mutable PersistentVolume Node Affinity. Both are alpha in Kubernetes one point three five, both solve real operational pain points, and both are part of Kubernetes becoming smarter and more adaptive. Let's start with the news.

**Alex**: First up, Percona just made a major strategic shift with their database platform. Percona Everest is becoming OpenEverest, with open governance and multi-vendor support. They've formed a new company called Solanica to lead development, and they're positioning it as the first truly open-source multi-database platform for Kubernetes.

**Jordan**: This supports MySQL, PostgreSQL, MongoDB, and Valkey, right? And it's modular architecture, so you can mix and match database engines and storage backends.

**Alex**: Exactly. The big deal here is open governance. Database operators have been maturing, but most were single-vendor solutions. OpenEverest is positioning for CNCF involvement and ecosystem growth. For platform engineers, this means you can standardize database provisioning across technologies without vendor lock-in.

**Jordan**: The modular approach is key. You're not buying into one vendor's entire stack. You can use the operator that fits your database engine, the storage backend that fits your infrastructure, and the deployment strategy that fits your risk profile. That's the maturity we need in the database operator space.

**Alex**: Next, on the security front, Google just launched Agent Sandbox for GKE, and this addresses one of the biggest risks in AI agent deployments: how do you safely execute untrusted code generated by large language models?

**Jordan**: Standard containers share the host kernel, which is a single point of failure. If an AI agent generates malicious code and you execute it in a regular container, you're one kernel exploit away from cluster compromise.

**Alex**: Agent Sandbox uses gVisor to provide kernel-level isolation. It splits the workload into two components: the Sentry, which intercepts all system calls and acts as a fake kernel, and the Gofer, which brokers all file system operations. The untrusted code never touches the host operating system.

**Jordan**: And for workloads that need even stronger isolation, they offer Kata Containers, which runs each pod in its own lightweight virtual machine with hardware-enforced isolation.

**Alex**: The performance optimization here is impressive. They support pre-warmed sandbox pools that deliver sub-second latency, which is a ninety percent improvement over cold starts. Plus, Pod Snapshots technology lets you save the state of running sandboxes and restore them near-instantly when an agent needs them.

**Jordan**: That's the key to making this practical. If every AI agent invocation required spinning up a VM, you'd be waiting minutes. But with pre-warmed pools and snapshot restore, you're getting VM-like isolation at container speed.

**Alex**: And it's being built as an open-source Kubernetes SIG Apps subproject, hosted under kubernetes-sigs slash agent-sandbox, so it'll be usable on any conformant Kubernetes cluster, not just GKE.

**Jordan**: Though the highest-performance features like Pod Snapshots and managed pre-warmed pools are GKE-exclusive, at least initially.

**Alex**: Now, security alert: we've got a high-severity MongoDB vulnerability with active exploitation in the wild. CVE two zero two five dash one four eight four seven, dubbed MongoBleed after the Heartbleed vulnerability.

**Jordan**: This affects MongoDB's zlib-based network message decompression, and it's been in the code since twenty seventeen. The flaw is in improper length handling during decompression. When processing undersized or malformed payloads, the system returns the allocated buffer size rather than the actual decompressed data length, which exposes adjacent heap memory to attackers.

**Alex**: CVSS score eight point seven, high severity. This is unauthenticated remote exploitation with low complexity. No authentication or user interaction required.

**Jordan**: And the real-world risk is significant. Approximately eighty-seven thousand potentially exposed servers worldwide according to Censys. Forty-two percent of cloud environments contain at least one vulnerable MongoDB instance. And active exploitation is confirmed.

**Alex**: Action items for platform engineers: update immediately to patched versions. MongoDB four point four through eight point zero are supported and have patches. If you can't patch immediately, disable compression as a temporary mitigation, and restrict network access to MongoDB instances. And note that end-of-life versions like three point six, four point zero, and four point two will not receive patches.

**Jordan**: This is similar to Heartbleed in that it's a memory exposure flaw in a compression library. Credentials, tokens, session data, any confidential information in MongoDB's memory is at risk. Treat this as critical.

**Alex**: Next, predictive capacity planning. This ties directly into our main topic today. The industry is shifting from reactive to proactive infrastructure.

**Jordan**: Traditional autoscaling in Kubernetes is reactive. The Horizontal Pod Autoscaler responds AFTER a CPU spike occurs. The cluster autoscaler adds nodes AFTER pods are pending. Everything is a feedback loop: problem happens, system reacts, eventually becomes stable.

**Alex**: Predictive scaling analyzes historical patterns, forecasts demand, and scales preemptively. Machine learning models identify anomalies and predict capacity issues before they impact users. This is what people are calling "self-driving infrastructure": clusters that self-correct inefficiencies autonomously.

**Jordan**: Some teams are using reinforcement learning for autoscaling, which provides learned anticipation based on observed trends. It's not true prediction, it's anticipation: the system learns that every Monday at nine AM, traffic spikes, so it scales up at eight forty-five.

**Alex**: And this is the context for today's features. Kubernetes is moving from feedback loops to anticipation. Extended Toleration Operators enable smarter initial placement based on thresholds. Mutable PersistentVolume Node Affinity enables dynamic optimization as storage topology changes.

**Jordan**: It's all connected. The platform is getting smarter.

**Alex**: And finally, a reminder about platform engineering fundamentals. Your internal tools are products, and developers are your customers. Building in isolation without user input leads to adoption flatlines. Forcing adoption through mandates creates resentment and shadow IT.

**Jordan**: Build something developers want to use, and adoption takes care of itself. Validate assumptions with real users before building. All these Kubernetes features we're discussing today are useless if platform teams don't build tools that solve real problems.

**Alex**: Features enable capabilities, but adoption requires solving actual pain points. Keep that in mind as we discuss these upcoming features.

**Jordan**: Alright, let's dive into the first major feature: Extended Toleration Operators. But before we get into what's new, we need to talk about how Kubernetes scheduling works today, because the current system reveals fundamental limitations.

**Alex**: So taints and tolerations are Kubernetes's way of controlling pod placement. A node taint marks a node as unsuitable for most pods. A pod toleration says "I can tolerate this taint, so it's okay to schedule me there."

**Jordan**: And today, there are two operators for tolerations: Equal, which requires an exact match of both key and value, and Exists, which just checks if the key exists regardless of value.

**Alex**: Let's say a node has a taint: gpu equals true, with effect NoSchedule. To schedule a pod on that node, the pod needs a toleration with key gpu, operator Equal, value true, and effect NoSchedule. Exact match required.

**Jordan**: But here's the limitation: this is binary. Either you have GPUs or you don't. Either you're a spot instance or on-demand. There's no nuance, no thresholds, no numeric comparison.

**Alex**: Right. The Exists operator is more permissive. It just says "any value is fine as long as the key exists." So you could have gpu equals true or gpu equals false or gpu equals banana, and a pod with operator Exists on key gpu would tolerate all of them.

**Jordan**: Which brings us to the real-world problem: imagine you have a heterogeneous GPU cluster. Some nodes have two GPUs, some have four, some have eight. You want to say "this training job needs at LEAST four GPUs per node." How do you express that with Equal or Exists?

**Alex**: You can't. The value is numeric, so Equal doesn't work unless you create separate tolerations for every possible value. And Exists is too permissive; it would match any node with the gpu-count key, regardless of whether it has two or eight GPUs.

**Jordan**: The current workaround is to create separate node pools with labels, then use complex NodeAffinity expressions, and maintain this manually as your cluster grows. It's operational overhead that doesn't scale.

**Alex**: And this problem shows up everywhere you have numeric thresholds, not just GPUs.

**Jordan**: Exactly. Spot instances with failure probability zero to one hundred. You want to say "I can tolerate up to five percent failure rate." Cost optimization: "schedule batch jobs on nodes cheaper than fifty cents per hour." Performance guarantees: "need nodes with disk IOPS above ten thousand." Memory ratios: "require nodes with at least four gigabytes of RAM per CPU core."

**Alex**: All of these are numeric comparisons, and Kubernetes can't express them with taints and tolerations today.

**Jordan**: Now, you might ask: doesn't NodeAffinity support numeric comparisons? It has greater than and less than operators.

**Alex**: It does, but NodeAffinity lacks the operational benefits that taints and tolerations provide. NodeAffinity is per-pod. To keep most pods away from risky nodes, you'd need to edit every single workload. That's hundreds or thousands of pod specs.

**Jordan**: Taints invert the control model. The node declares its characteristics via taints. Most pods can't schedule there by default. Only pods with explicit tolerations can opt in. It's secure by default.

**Alex**: And taints support the NoExecute effect with tolerationSeconds, which enables eviction. NodeAffinity has no eviction capability. If a spot instance receives a termination notice, you can update the taint, and pods without matching tolerations get evicted based on tolerationSeconds. That's graceful draining based on dynamic conditions.

**Jordan**: You can't do that with NodeAffinity. It's evaluated at scheduling time only, not continuously.

**Alex**: So Kubernetes one point three five introduces KEP five four seven one: Extended Toleration Operators for Threshold-Based Placement. This is alpha, feature gate disabled by default.

**Jordan**: Two new operators: Gt, which stands for greater than, and Lt, which stands for less than. But the semantics are about what the pod can tolerate, not a direct comparison.

**Alex**: Let's break that down. Gt means the toleration matches if the taint's numeric value is LESS than the toleration's value. Lt means the toleration matches if the taint's numeric value is GREATER than the toleration's value.

**Jordan**: Wait, that sounds backwards. Gt matches when the taint is less than the toleration?

**Alex**: It's about the pod's tolerance threshold. Gt means "I can tolerate risk UP TO this level." So a pod with operator Gt and value ten says "I can handle nodes with risk one through nine, but not ten or higher." The taint value must be less than the tolerance threshold for a match.

**Jordan**: Okay, so it's not "taint is greater than value," it's "I can tolerate values up to this threshold, which means taints below this."

---

*[Full transcript continues - approximately 5,600 words of technical discussion on Extended Toleration Operators, Mutable PersistentVolume Node Affinity, implementation details, and practical applications]*
