---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #043: K8s AI Conformance"
slug: 00043-kubernetes-ai-conformance-program
---

# Episode #043: Kubernetes AI Conformance - The End of AI Infrastructure Chaos

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** ~17 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience managing AI/ML workloads

> 📝 **Read the [full blog post](/blog/kubernetes-ai-conformance-program-cncf-standardization-guide)**: Complete guide to the CNCF Kubernetes AI Conformance Program, including the 5 core requirements, 11+ certified vendors, and practical implications for platform teams.

---

import GitHubButtons from '@site/src/components/GitHubButtons';

<div class="video-container">
<iframe width="100%" height="400" src="https://www.youtube.com/embed/kU8Gz1pHLyg" title="Episode #043: Kubernetes AI Conformance - The End of AI Infrastructure Chaos" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---

**Jordan**: Today we're covering something that just happened at KubeCon Atlanta. November 11th, 2025. CNCF launched the Certified Kubernetes AI Conformance Program. And this might be the most important announcement for platform teams running AI workloads.

**Alex**: The Wild West of AI infrastructure just ended. That's what people are calling it. Think about what we've been dealing with. Every cloud provider implemented GPU scheduling differently. GKE did it one way, EKS another, OpenShift a third. Training a model on one platform and deploying for inference on another meant rewriting infrastructure code.

**Jordan**: The numbers tell the story. According to the Linux Foundation Sovereign AI Research, 82% of organizations are now building custom AI solutions. 58% are running those workloads on Kubernetes. And 90% say open source is critical to their AI strategy.

**Alex**: But until now, there was no standard for what AI-capable actually means on Kubernetes. And that's been causing real pain.

**Jordan**: Right. Let's break down the four consequences platform teams have been dealing with. First is vendor lock-in. Once you optimized for one platform's GPU scheduling, migration became expensive. You're committed.

**Alex**: Second is unpredictable behavior. AI frameworks like Kubeflow and Ray behaved differently across environments. Same manifests, different results. Same training job, different resource allocation.

**Jordan**: Third, and this one hits the budget directly, resource waste. We talked about this in our GPU FinOps episode. Without standardized Dynamic Resource Allocation, GPU utilization hovers at 45 to 60%. That's almost half your expensive hardware sitting idle.

**Alex**: And fourth is skill fragmentation. Teams needed platform-specific expertise rather than portable Kubernetes skills. Every cloud had its own way of doing things.

**Jordan**: So what does the conformance program actually certify? There are five core capabilities that every AI-capable Kubernetes platform must implement consistently.

**Alex**: Let's start with the foundation: Dynamic Resource Allocation, or DRA. Traditional Kubernetes device plugins give you limited options. You ask for 2 GPUs and you get whatever's available. That's it.

**Jordan**: DRA changes everything. Instead of just saying "give me 2 GPUs," you can specify complex requirements. Two GPUs from the same node, connected with NVLink interconnect, with a minimum of 40 gigabytes VRAM. That precision is critical for distributed training.

**Alex**: And the performance impact is dramatic. According to The New Stack, DRA reaching GA in Kubernetes 1.34 improves GPU utilization from that 45 to 60% range up to 70 to 85%. Job queue times drop from 15 to 45 minutes down to 3 to 10 minutes. Monthly GPU costs drop 30 to 40%.

**Jordan**: Those aren't theoretical numbers. That's real money for platform teams managing expensive AI infrastructure.

**Alex**: The second core requirement is intelligent autoscaling. Two levels. Cluster autoscaling automatically adjusts node pools with accelerators based on pending pods. And horizontal pod autoscaling scales workloads based on custom metrics like GPU utilization.

**Jordan**: This matters because AI workloads are inherently bursty. Training jobs need massive GPU clusters for hours, then nothing. Inference services need to scale from zero to thousands of replicas based on traffic. Without smart autoscaling, you're either overprovisioned or getting crushed by demand spikes.

**Alex**: Third requirement is rich accelerator metrics. Generic utilization percentage isn't enough anymore. Conformant platforms must expose memory usage and bandwidth, compute utilization by workload, temperature and power consumption, and NVLink interconnect statistics for multi-GPU jobs.

**Jordan**: Without standardized metrics, autoscaling decisions and capacity planning become guesswork. You can't optimize what you can't measure.

**Alex**: Fourth is AI operator support. Complex AI frameworks like Kubeflow and Ray run as Kubernetes Operators using Custom Resource Definitions. The conformance program ensures these operators function correctly by validating CRD installation and lifecycle management, webhook functionality, and resource quota enforcement.

**Jordan**: This is subtle but critical. If the core platform isn't robust, AI operators fail in unpredictable ways. You spend weeks debugging what turns out to be a platform issue, not your code.

**Alex**: And the fifth requirement is gang scheduling, typically through Kueue or Volcano. Here's the problem with distributed AI training. You need all worker pods to start simultaneously. If 7 of 8 GPUs are available but the eighth isn't, traditional Kubernetes scheduling starts 7 pods that sit idle waiting.

**Jordan**: That's expensive idling. Gang scheduling ensures jobs only start when all resources are available. All or nothing. It prevents resource deadlocks where partially scheduled jobs waste GPU time waiting for stragglers.

**Alex**: So who's certified? The v1.0 launch includes 11-plus vendors. AWS with EKS, Google Cloud with GKE, Microsoft Azure, Red Hat OpenShift, Oracle OCI, VMware and Broadcom with vSphere Kubernetes Service.

**Jordan**: And then you've got the specialists. CoreWeave, which focuses on GPU cloud. Akamai with their inference cloud for edge AI. Giant Swarm, Kubermatic, and Sidero Labs on the managed Kubernetes side.

**Alex**: One notable absence people are asking about: NVIDIA. But Chris Aniszczyk, the CNCF CTO, clarified this in an interview with TechTarget. He said, quote, "They're not on the list, but they don't really have a product that would qualify. They don't have a Kubernetes-as-a-Service product similar to those being certified."

**Jordan**: NVIDIA participates in the working group. Their ComputeDomains feature integrates with conformant platforms. But the certification targets platform providers, not hardware vendors.

**Alex**: Now here's a question I've been getting: how does this differ from ISO 42001? Because both have AI in the name, people conflate them.

**Jordan**: They're completely different. ISO 42001 focuses on AI management and governance. It validates policies, processes, documentation. It answers the question: does your organization manage AI responsibly?

**Alex**: Kubernetes AI Conformance is purely technical. It validates APIs, configurations, workload behavior. It answers: does your infrastructure run AI correctly?

**Jordan**: ISO 42001 is technology-agnostic and organization-level. Kubernetes AI Conformance is Kubernetes-specific and infrastructure-level. For enterprise AI deployments, you probably need both.

**Alex**: Let's talk practical implications for platform teams. Starting with vendor selection.

**Jordan**: This changes how you evaluate AI infrastructure. Before conformance, you needed detailed proof-of-concept testing for GPU scheduling behavior across vendors. Try each one, document the quirks, figure out compatibility issues.

**Alex**: Now you can trust that conformant platforms handle core capabilities identically. Your selection criteria shift to price, because GPU instance costs vary significantly. Ecosystem integration with your existing tools. Support SLAs. And geography for data residency.

**Jordan**: The conformance check becomes a filter, not a deep investigation. If it's not certified, it's off the list. Then you evaluate on factors that matter to your business.

**Alex**: The program also enables genuine multi-cloud AI strategies. Training on the cheapest GPU cloud, often CoreWeave or Lambda Labs. Deploying inference wherever serves your users fastest. Bursting to alternative providers during peak demand.

**Jordan**: This was difficult before because workload manifests needed platform-specific modifications. With conformance, the same Kubernetes resources work everywhere. Portability becomes real.

**Alex**: For teams on non-conformant platforms, the conformance gap tells you exactly what to evaluate. Does your platform support DRA or only legacy device plugins? Can you request GPUs with specific interconnect requirements? Are gang scheduling solutions supported? Do AI operators function correctly?

**Jordan**: Non-conformant platforms may still work for simple use cases. Single GPU inference jobs, basic training. But expect friction as workloads become more sophisticated.

**Alex**: Here's a decision framework. Certification is critical when you're running distributed training across multiple GPUs or nodes, deploying AI workloads across multiple clouds or regions, using complex AI frameworks like Kubeflow, Ray, or KServe, prioritizing GPU cost optimization, or requiring portability between platforms.

**Jordan**: Certification is less critical for single-GPU inference workloads, when you're locked into a single cloud for other reasons, when using managed AI services like SageMaker or Vertex AI rather than raw Kubernetes, or for workloads that don't require GPU or TPU acceleration.

**Alex**: What's coming in v2.0? CNCF announced that roadmap development has started, with release expected in 2026.

**Jordan**: Based on working group discussions, expect topology-aware scheduling with requirements for NUMA node, PCIe root, and network fabric alignment. Multi-node NVLink standardization through NVIDIA's ComputeDomains. Model serving standards with common interfaces for inference. And cost attribution for standardized GPU tracking and chargeback.

**Alex**: Chris Aniszczyk put it well. Quote: "It starts with a simple focus on the kind of things you really need to make AI workloads work well on Kubernetes." V1.0 is fundamentals. V2.0 will extend, not replace.

**Jordan**: So the practical guidance is: don't wait for v2.0. The v1.0 capabilities address the most common AI infrastructure pain points. Adopt conformant platforms now.

**Alex**: Let's wrap with specific actions. This week, check if your current platform is AI conformant. The GitHub repository at cncf slash k8s-ai-conformance has the list.

**Jordan**: This month, inventory your AI workloads by capability requirements. Which ones need DRA? Which need gang scheduling? Which are using AI operators?

**Alex**: This quarter, if you're on a non-conformant platform, evaluate migration to a certified one. If you're already conformant, validate that the conformance capabilities are actually enabled. Just because the platform is certified doesn't mean you've configured it correctly.

**Jordan**: Looking into 2026, build vendor selection criteria around conformance certification. Develop a multi-cloud AI strategy that leverages platform portability. Track v2.0 requirements, especially topology-aware scheduling.

**Alex**: The bottom line: the Kubernetes AI Conformance Program represents the maturation of AI infrastructure. For the first time, platform teams have a vendor-neutral standard to evaluate AI capabilities.

**Jordan**: As Chris Aniszczyk put it: quote, "Teams need consistent infrastructure they can rely on." Now they have it. The Wild West era is over.

**Alex**: For senior platform engineers and SREs managing AI workloads, this is a fundamental shift. Whether you adopt immediately or wait for v2.0, understanding what conformance means shapes how you evaluate, build, and operate AI infrastructure on Kubernetes.

---

## Key Takeaways

1. **AI Infrastructure Standardization**: CNCF launched the first vendor-neutral standard for AI workloads on Kubernetes (November 11, 2025)

2. **Five Core Requirements**: Dynamic Resource Allocation (DRA), intelligent autoscaling, rich accelerator metrics, AI operator support, and gang scheduling

3. **11+ Certified Vendors**: AWS EKS, Google GKE, Microsoft Azure, Red Hat OpenShift, Oracle OCI, CoreWeave, and more

4. **Multi-Cloud Enabled**: Same Kubernetes resources now work across conformant platforms, enabling genuine portability

5. **Don't Wait for v2.0**: v1.0 addresses core pain points; adopt conformant platforms now

## Resources

- [CNCF Kubernetes AI Conformance Program](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program-to-standardize-ai-workloads-on-kubernetes/)
- [GitHub: cncf/k8s-ai-conformance](https://github.com/cncf/k8s-ai-conformance)
- [GKE AI Conformance Implementation](https://opensource.googleblog.com/2025/11/ai-conformant-clusters-in-gke.html)
- [DRA Guide - The New Stack](https://thenewstack.io/kubernetes-primer-dynamic-resource-allocation-dra-for-gpu-workloads/)
