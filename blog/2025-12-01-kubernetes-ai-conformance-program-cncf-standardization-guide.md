---
title: "CNCF Kubernetes AI Conformance Program: The Complete Guide for Platform Teams"
description: "CNCF launched the Certified Kubernetes AI Conformance Program at KubeCon 2025. Learn what it means for platform teams, the 5 core requirements, and which vendors are certified."
slug: kubernetes-ai-conformance-program-cncf-standardization-guide
authors: [vibesre]
tags: [kubernetes, ai, machine-learning, platform-engineering, cncf, kubecon]
keywords: [kubernetes ai conformance, cncf ai certification, kubernetes ml workloads, DRA dynamic resource allocation, kubernetes gpu scheduling, ai platform standardization, kubecon 2025, kubernetes ai certification]
image: /img/blog/kubernetes-ai-conformance.png
date: 2025-12-01
dateModified: 2025-12-01
schema:
  type: FAQPage
  questions:
    - question: "What is the CNCF Kubernetes AI Conformance Program?"
      answer: "The Certified Kubernetes AI Conformance Program is a CNCF initiative launched November 11, 2025 that establishes community-defined standards for running AI workloads on Kubernetes. It defines minimum capabilities including Dynamic Resource Allocation (DRA), GPU integration, and AI framework support."
    - question: "Which vendors are certified for Kubernetes AI Conformance?"
      answer: "Initial certified vendors include AWS (EKS), Google Cloud (GKE), Microsoft Azure, Red Hat (OpenShift), Oracle Cloud, CoreWeave, Akamai, Giant Swarm, Kubermatic, Sidero Labs, and VMware/Broadcom (vSphere Kubernetes Service)."
    - question: "What are the core requirements for Kubernetes AI Conformance certification?"
      answer: "The five core requirements are: Dynamic Resource Allocation (DRA) for GPUs/TPUs, intelligent autoscaling for accelerators, rich accelerator metrics, AI operator support (Kubeflow, Ray), and gang scheduling for distributed jobs."
    - question: "Why does Kubernetes AI Conformance matter for platform teams?"
      answer: "It reduces vendor lock-in by ensuring AI workloads behave predictably across certified platforms. Platform teams can select infrastructure based on price and features rather than worrying about compatibility issues."
    - question: "What is Dynamic Resource Allocation (DRA) in Kubernetes?"
      answer: "DRA is a Kubernetes feature reaching GA in v1.34 that provides flexible, fine-grained resource requests for accelerators. Unlike device plugins, DRA enables complex requirements like '2 GPUs from same node with NVLink interconnect and minimum 40GB VRAM.'"
    - question: "How does Kubernetes AI Conformance differ from ISO 42001?"
      answer: "ISO 42001 focuses on AI management and governance policies. Kubernetes AI Conformance is purely technical, defining APIs, capabilities, and configurations clusters must support to run AI/ML workloads efficiently."
    - question: "When will Kubernetes AI Conformance v2.0 be released?"
      answer: "CNCF announced that v2.0 roadmap development has started, with the release expected in 2026. The v1.0 program launched November 2025 at KubeCon Atlanta."
---

# CNCF Kubernetes AI Conformance Program: The Complete Guide for Platform Teams

The "Wild West" of AI infrastructure just ended. At KubeCon Atlanta on November 11, 2025, CNCF launched the [Certified Kubernetes AI Conformance Program](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program-to-standardize-ai-workloads-on-kubernetes/)—establishing the first industry standard for running AI workloads on Kubernetes. With 82% of organizations building custom AI solutions and 58% using Kubernetes for those workloads, the fragmentation risk was real. Now there's a baseline.

## TL;DR

- **What**: CNCF certification program establishing minimum capabilities for running AI/ML workloads on Kubernetes
- **When**: v1.0 launched November 11, 2025 at KubeCon Atlanta; v2.0 roadmap started for 2026
- **Who**: 11+ vendors certified including AWS, Google, Microsoft, Red Hat, Oracle, CoreWeave
- **Core Requirements**: Dynamic Resource Allocation (DRA), GPU autoscaling, accelerator metrics, AI operator support, gang scheduling
- **Impact**: Reduces vendor lock-in, guarantees interoperability, enables multi-cloud AI strategies
- **Action**: Check if your platform is certified before selecting AI infrastructure

> 🎙️ **Listen to the podcast episode**: [Episode #043: Kubernetes AI Conformance - The End of AI Infrastructure Chaos](/podcasts/00043-kubernetes-ai-conformance-program) - Jordan and Alex break down the new CNCF certification and what it means for platform teams.

<div class="video-container">
<iframe width="100%" height="400" src="https://www.youtube.com/embed/kU8Gz1pHLyg" title="Kubernetes AI Conformance Program Explained" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Organizations building custom AI | 82% | [Linux Foundation Sovereign AI Research, Nov 2025](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program-to-standardize-ai-workloads-on-kubernetes/) |
| Enterprises using K8s for AI | 58% | [Linux Foundation Sovereign AI Research, Nov 2025](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program-to-standardize-ai-workloads-on-kubernetes/) |
| Open source critical to AI strategy | 90% | [Linux Foundation Sovereign AI Research, Nov 2025](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program-to-standardize-ai-workloads-on-kubernetes/) |
| Initial certified vendors | 11+ | [CNCF Announcement, Nov 2025](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program-to-standardize-ai-workloads-on-kubernetes/) |
| AI/ML workload growth on K8s (next 12mo) | 90% expect increase | [Spectro Cloud State of K8s 2025](https://www.spectrocloud.com/state-of-kubernetes-2025) |
| GPU utilization improvement (DRA vs device plugins) | 45-60% → 70-85% | [The New Stack DRA Guide](https://thenewstack.io/kubernetes-primer-dynamic-resource-allocation-dra-for-gpu-workloads/) |
| Existing certified K8s distributions | 100+ | [CNCF Conformance Program](https://www.cncf.io/training/certification/software-conformance/) |

## The Problem: AI Infrastructure Fragmentation

Before this program, every cloud provider and Kubernetes distribution implemented AI capabilities differently. GPU scheduling worked one way on GKE, another way on EKS, and a third way on OpenShift. Training a model on one platform and deploying for inference on another meant rewriting infrastructure code.

The consequences for platform teams were significant:

1. **Vendor Lock-in**: Once you optimized for one platform's GPU scheduling, migration became expensive
2. **Unpredictable Behavior**: AI frameworks like Kubeflow and Ray behaved differently across environments
3. **Resource Waste**: Without standardized DRA, GPU utilization hovered at 45-60%
4. **Skill Fragmentation**: Teams needed platform-specific expertise rather than portable Kubernetes skills

:::tip Key Takeaway
The Kubernetes AI Conformance Program does for AI workloads what the original Kubernetes Conformance Program did for container orchestration—it guarantees that certified platforms behave identically for core capabilities.
:::

## What the Program Certifies

The certification validates five core capabilities that every AI-capable Kubernetes platform must implement consistently.

### 1. Dynamic Resource Allocation (DRA)

DRA is the foundation of the conformance program. Traditional Kubernetes device plugins offer limited resource requests—you ask for "2 GPUs" and get whatever's available. DRA enables complex requirements:

```yaml
# Traditional device plugin (limited)
resources:
  limits:
    nvidia.com/gpu: 2

# DRA-enabled (rich requirements)
resourceClaims:
  - name: gpu-claim
    spec:
      deviceClassName: nvidia-gpu
      requests:
        - count: 2
          constraints:
            - interconnect: nvlink
            - memory: {min: "40Gi"}
            - locality: same-node
```

According to [The New Stack](https://thenewstack.io/kubernetes-primer-dynamic-resource-allocation-dra-for-gpu-workloads/), DRA reaching GA in Kubernetes 1.34 improves GPU utilization from 45-60% with device plugins to 70-85%, reduces job queue times from 15-45 minutes to 3-10 minutes, and cuts monthly GPU costs by 30-40%.

### 2. Intelligent Autoscaling

Certified platforms must implement two-level autoscaling for AI workloads:

- **Cluster Autoscaling**: Automatically adjusts node pools with accelerators based on pending pods
- **Horizontal Pod Autoscaling**: Scales workloads based on custom metrics like GPU utilization

This matters because AI workloads have bursty resource requirements. Training jobs need massive GPU clusters for hours, then nothing. Inference services need to scale from zero to thousands of replicas based on traffic.

### 3. Rich Accelerator Metrics

Platforms must expose detailed performance metrics for GPUs, TPUs, and other accelerators. Generic "utilization percentage" isn't sufficient—conformant platforms provide:

- Memory usage and bandwidth
- Compute utilization by workload
- Temperature and power consumption
- NVLink/interconnect statistics for multi-GPU jobs

Without standardized metrics, autoscaling decisions and capacity planning become guesswork.

### 4. AI Operator Support

Complex AI frameworks like Kubeflow and Ray run as Kubernetes Operators using Custom Resource Definitions (CRDs). The conformance program ensures these operators function correctly by validating:

- CRD installation and lifecycle management
- Operator webhook functionality
- Resource quota enforcement for operator-managed resources

If the core platform isn't robust, AI operators fail in unpredictable ways.

### 5. Gang Scheduling

Distributed AI training jobs require all worker pods to start simultaneously. If 7 of 8 GPUs are available but the 8th isn't, traditional Kubernetes scheduling starts 7 pods that sit idle waiting for the 8th. Gang scheduling (via [Kueue](https://kueue.sigs.k8s.io/) or Volcano) ensures jobs only start when all resources are available.

:::tip Key Takeaway
Gang scheduling prevents resource deadlocks in distributed training. Without it, partially-scheduled jobs waste expensive GPU time waiting for stragglers.
:::

## Certified Vendors (November 2025)

The v1.0 release certifies these platforms:

| Vendor | Product | Notes |
|--------|---------|-------|
| **AWS** | Amazon EKS | Full DRA support, integrated with EC2 GPU instances |
| **Google Cloud** | GKE | First mover, detailed [implementation blog](https://opensource.googleblog.com/2025/11/ai-conformant-clusters-in-gke.html) |
| **Microsoft** | Azure Kubernetes Service | Integrated with Azure ML |
| **Red Hat** | OpenShift | Enterprise focus, RHEL AI integration |
| **Oracle** | OCI Kubernetes Engine | OCI GPU shapes supported |
| **Broadcom/VMware** | vSphere Kubernetes Service | On-premises AI workloads |
| **CoreWeave** | CoreWeave Kubernetes | GPU cloud specialist |
| **Akamai** | Akamai Inference Cloud | Edge AI inference |
| **Giant Swarm** | Giant Swarm Platform | Managed K8s provider |
| **Kubermatic** | KKP | Multi-cluster management |
| **Sidero Labs** | Talos Linux | Secure, immutable K8s |

### Notable Absence: NVIDIA

NVIDIA isn't on the certified list, but that's expected. Chris Aniszczyk (CNCF CTO) [clarified to TechTarget](https://www.techtarget.com/searchitoperations/news/366634474/CNCF-Kubernetes-AI-program-faces-scrutiny-from-IT-analysts): "They're not on the list, but they don't really have a product that would qualify. They don't have a Kubernetes-as-a-Service product similar to those being certified."

NVIDIA participates in the working group and their [ComputeDomains feature](https://cloudnativenow.com/features/nvidias-computedomains-aims-to-simplify-multi-node-nvlink-for-kubernetes/) integrates with conformant platforms, but the certification targets platform providers, not hardware vendors.

## How This Differs from ISO 42001

A common question: "How does this relate to ISO 42001 AI management certification?"

| Aspect | Kubernetes AI Conformance | ISO 42001 |
|--------|---------------------------|-----------|
| **Focus** | Technical capabilities | Management & governance |
| **Validates** | APIs, configurations, workload behavior | Policies, processes, documentation |
| **Target** | Platform infrastructure | Organizational AI practices |
| **Scope** | Kubernetes-specific | Technology-agnostic |

ISO 42001 certifies that your organization manages AI responsibly. Kubernetes AI Conformance certifies that your infrastructure runs AI workloads correctly. You likely need both for enterprise AI deployments.

:::tip Key Takeaway
ISO 42001 answers "Do we manage AI responsibly?" Kubernetes AI Conformance answers "Does our infrastructure run AI correctly?" These are complementary, not competing standards.
:::

## Practical Implications for Platform Teams

### Vendor Selection

The certification changes how you evaluate AI infrastructure. Instead of detailed POCs testing GPU scheduling behavior across vendors, you can trust that conformant platforms handle core capabilities identically. Selection criteria shift to:

- **Price**: GPU instance costs vary significantly across providers
- **Ecosystem**: Integration with your existing tools (MLflow, Weights & Biases, etc.)
- **Support**: SLAs and enterprise support options
- **Geography**: Data residency requirements

### Multi-Cloud AI Strategy

The program enables genuine multi-cloud AI deployments:

- **Training**: Use the cheapest GPU cloud (often CoreWeave or Lambda Labs)
- **Inference**: Deploy to whichever cloud serves your users fastest
- **Burst**: Overflow to alternative providers during peak demand

This was previously difficult because workload manifests needed platform-specific modifications. With conformance, the same Kubernetes resources work everywhere.

### Migration Planning

If your current platform isn't certified, the conformance gap identifies specific capabilities to evaluate:

1. Does your platform support DRA or only legacy device plugins?
2. Can you request GPUs with specific interconnect requirements?
3. Are gang scheduling solutions (Kueue, Volcano) supported?
4. Do AI operators (Kubeflow, Ray) function correctly?

Non-conformant platforms may still work for simple use cases, but expect friction as workloads become more sophisticated.

## Decision Framework: When Conformance Matters

**Certification is critical when:**
- Running distributed training jobs across multiple GPUs/nodes
- Deploying AI workloads across multiple clouds or regions
- Using complex AI frameworks (Kubeflow, Ray, KServe)
- GPU cost optimization is a priority
- Portability between platforms is required

**Certification is less critical when:**
- Running single-GPU inference workloads
- Locked into a single cloud provider for other reasons
- Using managed AI services (SageMaker, Vertex AI) rather than raw Kubernetes
- Workloads don't require GPU/TPU acceleration

## What's Coming in v2.0

CNCF announced that v2.0 roadmap development has started, with an expected 2026 release. Based on working group discussions, likely additions include:

- **Topology-aware scheduling**: Requirements for NUMA node, PCIe root, and network fabric alignment
- **Multi-node NVLink**: Standardized support for NVIDIA's ComputeDomains
- **Model serving standards**: Common interfaces for inference workloads
- **Cost attribution**: Standardized GPU cost tracking and chargeback

The v1.0 program intentionally started with fundamentals. As Chris Aniszczyk noted: "It starts with a simple focus on the kind of things you really need to make AI workloads work well on Kubernetes."

:::tip Key Takeaway
Don't wait for v2.0 to adopt conformant platforms. The v1.0 capabilities address the most common AI infrastructure pain points. Additional features will extend the standard, not replace it.
:::

## Getting Your Platform Certified

If you provide a Kubernetes platform with AI capabilities, certification is straightforward:

1. **Review requirements**: Check the [GitHub repository](https://github.com/cncf/k8s-ai-conformance) for current test criteria
2. **Run conformance tests**: Automated test suite validates capability implementation
3. **Submit results**: Pull request to the CNCF repository with test output
4. **Review process**: CNCF bot verifies results, human review for edge cases

The process mirrors the existing Kubernetes Conformance Program that has certified 100+ distributions since 2017.

## Actions for Platform Teams

### Immediate (This Week)

1. Check if your current platform is [AI conformant](https://github.com/cncf/k8s-ai-conformance)
2. Inventory AI workloads by capability requirements (DRA, gang scheduling, etc.)
3. Identify gaps between current platform and conformance requirements

### Short-Term (This Quarter)

1. If non-conformant: Evaluate migration to certified platform
2. If conformant: Validate that conformance capabilities are enabled
3. Update internal platform documentation with conformance status

### Long-Term (2025-2026)

1. Build vendor selection criteria around conformance certification
2. Develop multi-cloud AI strategy leveraging platform portability
3. Track v2.0 requirements for topology-aware scheduling

## Related Content

- [Episode #035: KubeCon 2025 Part 1 - AI Goes Native](/podcasts/00035-kubecon-2025-ai-native) - AI announcements at KubeCon
- [The $4,350/Month GPU Waste Problem](/blog/kubernetes-gpu-resource-management-finops-ai-workloads-2025) - GPU cost optimization strategies
- [Kubernetes Overview 2025](/podcasts/00014-kubernetes-overview-2025) - Kubernetes ecosystem overview
- [KubeCon Atlanta 2025 Recap](/blog/kubecon-atlanta-2025-recap) - Full conference coverage where AI Conformance was announced
- [Platform Engineering Anti-Patterns](/blog/platform-engineering-anti-patterns) - Common mistakes when building platform capabilities

## Learn More

### Official Resources
- [CNCF Kubernetes AI Conformance Program](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program-to-standardize-ai-workloads-on-kubernetes/) - Official announcement
- [GitHub: cncf/k8s-ai-conformance](https://github.com/cncf/k8s-ai-conformance) - Test suite and certified products
- [Working Group Charter](https://www.cncf.io/blog/2025/08/01/help-us-build-the-kubernetes-conformance-for-ai/) - How the program was developed

### Technical Deep Dives
- [GKE AI Conformance Implementation](https://opensource.googleblog.com/2025/11/ai-conformant-clusters-in-gke.html) - Google's technical details
- [Dynamic Resource Allocation Guide](https://thenewstack.io/kubernetes-primer-dynamic-resource-allocation-dra-for-gpu-workloads/) - DRA explained
- [Topology-Aware Scheduling](https://pacoxu.wordpress.com/2025/11/28/smarter-scheduling-for-ai-workloads-topology-aware-scheduling/) - v2.0 preview

### Industry Analysis
- [TechTarget Analysis](https://www.techtarget.com/searchitoperations/news/366634474/CNCF-Kubernetes-AI-program-faces-scrutiny-from-IT-analysts) - Analyst perspectives on the program
- [Cloud Native Now Coverage](https://cloudnativenow.com/features/cncf-adds-program-to-standardize-ai-workloads-on-kubernetes-clusters/) - Industry reaction

---

*The Kubernetes AI Conformance Program represents the maturation of AI infrastructure. For the first time, platform teams have a vendor-neutral standard to evaluate AI capabilities. As Chris Aniszczyk put it: "Teams need consistent infrastructure they can rely on." Now they have it.*
