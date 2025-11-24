---
title: "Kubernetes GPU Resource Management: FinOps Best Practices for AI Workloads (2025 Guide)"
description: "Cut Kubernetes GPU costs 60% with proper resource management. H100s at $5K/month, 70% idle waste, and MIG/time-slicing strategies that actually work for AI workloads."
keywords:
  - kubernetes gpu resource management
  - finops for ai workloads
  - gpu cost optimization
  - kubernetes gpu scheduling
  - multi-instance gpu kubernetes
  - gpu requests limits
  - ai workload optimization
  - kubernetes gpu utilization
  - aws eks gpu cost allocation
  - nvidia mig kubernetes
  - gpu time-slicing
  - reduce gpu costs machine learning
datePublished: "2025-11-24"
dateModified: "2025-11-24"
slug: kubernetes-gpu-resource-management-finops-ai-workloads-2025
schema:
  type: FAQPage
  questions:
    - question: "How do you set GPU requests and limits in Kubernetes?"
      answer: "In Kubernetes, GPUs must be specified only in the limits section of pod resource specifications. Kubernetes automatically uses the limit value as the request. You cannot specify GPU requests without limits, and if specifying both, the values must be equal. Example: resources: { limits: { nvidia.com/gpu: 1 } }."
    - question: "What is the average GPU utilization rate in Kubernetes clusters?"
      answer: "Analysis of over 4,000 Kubernetes clusters showed average GPU utilization of only 13%, with most organizations achieving less than 30% utilization across machine learning workloads. Organizations typically waste 60-70% of their GPU budget on idle resources."
    - question: "How much can you save with Kubernetes GPU cost optimization?"
      answer: "GPU time-slicing can reduce costs by 75% per developer by sharing a single H100 among four developers. Combined with Spot instances (70-90% savings), total GPU expenses can be cut by as much as 93%. Proper utilization strategies can cut cloud GPU costs by up to 40%."
    - question: "What is Multi-Instance GPU (MIG) and how does it reduce costs?"
      answer: "MIG is NVIDIA's hardware-level feature for Ampere and later GPUs that divides a single physical GPU into up to seven isolated instances with dedicated compute cores, memory, and cache. MIG enables fine-grained resource sharing, allowing multiple workloads to run simultaneously on one GPU, significantly improving utilization and reducing costs."
    - question: "How does AWS EKS support GPU cost allocation per pod?"
      answer: "As of September 2025, AWS Split Cost Allocation Data for Amazon EKS supports accelerated computing workloads (NVIDIA, AMD GPUs, Trainium, Inferentia). Pod-level costs are calculated based on split-usage ratios multiplied by cost per GPU-Hour, allowing teams to track GPU costs at the container level across all commercial AWS regions at no additional cost."
    - question: "What are common Kubernetes GPU resource management anti-patterns?"
      answer: "Common anti-patterns include not setting GPU limits (causing scheduling failures), overprovisioning with round numbers (500m CPU, 1GB RAM without load testing), failing to use node taints for GPU nodes (allowing non-GPU workloads on expensive hardware), and not implementing monitoring to detect idle GPU time."
    - question: "How can model quantization reduce GPU inference costs?"
      answer: "Quantization reduces precision from 32-bit floating point to 8-bit integers, achieving 4-8x model compression with 1-2% accuracy loss. Production-grade optimization combining quantization with pruning achieves 8-15x compression with under 1% degradation. OpenAI achieved 40% inference cost reduction through pruning and quantization techniques."
    - question: "What is GPU time-slicing in Kubernetes?"
      answer: "GPU time-slicing allows multiple workloads to sequentially share GPU resources without hardware partitioning. Kubernetes schedules different containers to use the same GPU at different time intervals. While simpler than MIG, time-slicing provides no isolation between workloads and may cause performance variability. Best for development environments where isolation isn't critical."
    - question: "What FinOps metrics should platform engineers track for AI workloads?"
      answer: "Platform engineers should track Cost Per Inference (total inference costs divided by requests), GPU Utilization Efficiency (actual usage divided by provisioned capacity), Cost Per Unit of Work (e.g., cost per 100K tokens), idle GPU hours per namespace, and spot instance adoption rate. AWS EKS teams can use Split Cost Allocation tags like aws:eks:namespace and aws:eks:workload-name."
    - question: "How much do H100 and A100 GPUs cost in 2025?"
      answer: "In 2025, H100 GPUs cost $2.10-4.09 per hour (approximately $5,000/month on AWS), down from $8/hour in 2024. A100 GPUs (80GB) range from $0.66-4.00 per hour depending on provider. Specialized GPU providers offer 45-61% savings versus major clouds. Regional selection can yield 2-5x cost differences."
---

# Kubernetes GPU Resource Management: FinOps Best Practices for AI Workloads (2025 Guide)

<GitHubButtons />

Your H100 GPU costs $5,000 per month on AWS. Analysis of 4,000+ Kubernetes clusters reveals you're using it at 13% capacity. That's $4,350 wasted every month—per GPU. Scale that across ten GPUs in your AI training cluster, and you're burning $43,500 monthly on idle capacity. Multiply by a hundred-node cluster serving production ML inference? The waste becomes existential.

Organizations waste 60-70% of their GPU budget this way. Yet platform engineers using Multi-Instance GPU (MIG) and time-slicing techniques cut costs by 75-93% while improving utilization to 60-85%. The difference isn't the hardware—it's Kubernetes resource management.

> 🎙️ **Listen to the podcast episode**: [#034: The GPU Waste Problem](/podcasts/00034-kubernetes-gpu-cost-waste-finops) - Why Kubernetes architecture creates 87% GPU idle time, the five-layer optimization framework (MIG, time-slicing, VPA, Spot, regional arbitrage), and 90-day implementation playbook with real case study: 20 H100s → 7 H100s ($100K → $35K/month).

## Quick Answer (TL;DR)

**Problem**: Organizations waste 60-70% of GPU budgets on idle Kubernetes resources, with average utilization under 30% despite H100 GPUs costing $5,000/month.

**Root Cause**: Kubernetes treats GPUs as non-divisible resources without proper requests/limits configuration, node taints, or utilization monitoring, leading to massive overprovisioning and idle capacity.

**Key Statistics**:
- H100 GPUs: $2.10-4.09/hour (~$5K/month AWS), A100: $0.66-4.00/hour
- Average GPU utilization: 13% across 4,000+ clusters, under 30% for most ML workloads
- Cost reduction potential: 75% with time-slicing (4 devs sharing 1 H100), 93% combined with Spot instances
- MIG enables up to 7 isolated instances per GPU, improving utilization to 60-85%
- AWS EKS Split Cost Allocation (Sept 2025) enables pod-level GPU cost tracking across all regions

**Success Metrics**: Production clusters achieve 60-85% GPU utilization with MIG/time-slicing, idle GPU hours reduced by 70%, regional arbitrage saves 2-5x on identical workloads.

**When NOT to use GPU sharing**: Real-time inference with strict latency SLAs (under 100ms), workloads requiring full GPU memory (80GB models), compliance requiring hardware isolation, critical production workloads where performance variability is unacceptable.

<iframe width="560" height="315" src="https://www.youtube.com/embed/LJBT-a9CuXw" title="The $4,350/Month GPU Waste Problem: How Kubernetes Architecture Creates Massive Cost Inefficiency" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Key Statistics (2024-2025 Data)

| Metric | Value | Source | Context |
|--------|-------|--------|---------|
| GPU Waste | 60-70% of GPU budget wasted on idle resources | [Wesco AI Infrastructure 2025](https://www.wesco.com/us/en/knowledge-hub/articles/ai-infrastructure-optimization-maximize-gpu-utilization-with-mig-and-kubernetes.html) | Organizations pay for full capacity while using fraction |
| Average GPU Utilization | 13% across 4,000+ K8s clusters; under 30% for most ML workloads | [Cast.AI Analysis](https://cast.ai/blog/gpu-cost-optimization-sharing-automation/), [Mirantis](https://www.mirantis.com/blog/improving-gpu-utilization-strategies-and-best-practices/) | Single H100 at 13% wastes $4,350/month |
| H100 Pricing (2025) | $2.10-4.09/hour (~$5,000/month AWS) | [Cast.AI GPU Report](https://cast.ai/reports/gpu-price-2025/), [GMI Cloud](https://www.gmicloud.ai/blog/how-much-does-the-nvidia-h100-gpu-cost-in-2025-buy-vs-rent-analysis) | Down from $8/hour in 2024 |
| A100 Pricing (2025) | $0.66-4.00/hour depending on provider | [ThunderCompute](https://www.thundercompute.com/blog/nvidia-h100-pricing) | Specialized providers 45-61% cheaper than AWS/GCP/Azure |
| Time-Slicing Savings | 75% cost reduction per developer (4 sharing 1 H100) | [Cast.AI](https://cast.ai/blog/gpu-cost-optimization-sharing-automation/) | Combined with Spot: 93% total savings |
| MIG Isolation | Up to 7 independent GPU instances per physical GPU | [NVIDIA GPU Operator Docs](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html) | Ampere/Hopper architecture feature |
| Regional Arbitrage | 2-5x cost savings by provisioning in optimal regions | [Cast.AI GPU Report](https://cast.ai/reports/gpu-price-2025/) | Same H100, different region pricing |
| Spot Instance Discount | 70-90% savings vs on-demand pricing | [DigitalOcean](https://www.digitalocean.com/resources/articles/optimize-gpu-costs) | Requires checkpoint/restart tolerance |
| Production Utilization | 60-85% sustained with proper optimization | [Debugg.ai](https://debugg.ai/resources/kubernetes-gpu-scheduling-2025-kueue-volcano-mig) | Idle GPU hours reduced 70% |
| Model Quantization Savings | 40% inference cost reduction (OpenAI case study) | [MLSysBook](https://www.mlsysbook.ai/contents/core/optimizations/optimizations.html) | 8-15x compression, under 1% accuracy loss |
| AWS EKS GPU Cost Allocation | Pod-level tracking available Sept 2025, all commercial regions | [AWS Announcement](https://aws.amazon.com/about-aws/whats-new/2025/09/split-cost-allocation-data-amazon-eks-nvidia-amd-gpu-trainium-inferentia-ec2/) | No additional cost, supports custom labels |
| AI Spend Growth | $62,964/month (2024) → $85,521 projected (2025), 36% YoY | [Medium FinOps Analysis](https://tahaazher27.medium.com/the-economics-of-cloud-native-ai-a-finops-perspective-8266a840ee85) | Urgency for cost optimization |

## The $5,000/Month Problem—Why GPUs Sit Idle

Picture this: A well-funded AI startup deploys 20 H100 GPUs for model training and inference. Monthly GPU bill: $100,000. Average utilization across the cluster: 18%. They're effectively paying $82,000 per month for GPUs that sit idle 82% of the time.

This isn't an edge case. It's the norm.

### The Kubernetes Non-Divisibility Problem

Unlike CPU and memory, Kubernetes treats GPUs as atomic resources—you get the whole GPU or nothing. The default scheduler can't split an H100 across workloads. A single training job requests `nvidia.com/gpu: 1`, uses 20% of the GPU's capacity, and blocks other workloads for hours.

From the [Kubernetes official documentation](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/): "Containers (and Pods) do not share GPUs. There's no overcommitting of GPUs. It is not possible to request a fraction of a GPU."

This architectural decision made sense for gaming workloads where full GPU access is required. For AI/ML workloads with variable GPU utilization, it creates massive inefficiency.

### The Requests/Limits Anti-Pattern

In [Kubernetes Production Mastery Lesson 02](/podcasts/00010-kubernetes-production-mastery-lesson-02), we covered how 67% of teams experience OOMKilled incidents from missing resource limits. With GPUs, the anti-pattern is worse—and more expensive.

Developers request GPUs without proper limits, or set both requests and limits equal without load testing, leading to massive overprovisioning. Example: A team requests `nvidia.com/gpu: 1` with `memory: 16GB` when the workload actually needs 4GB. They've just wasted 12GB per pod. Multiply by 50 pods: 600GB of wasted memory capacity.

According to [nOps research on Kubernetes overprovisioning](https://www.nops.io/blog/how-to-stop-overprovisioning-in-kubernetes/), developers choose "easy, round numbers for resource requests and limits—such as 500 millicores or 1GB of memory" without load testing. At $5,000/month per H100, this uninformed guesswork becomes catastrophically expensive.

### The Node Taint Failure

GPU nodes cost 10-20x more than CPU nodes. Without proper taints and tolerations, Kubernetes happily schedules non-GPU workloads—logging sidecars, monitoring agents, cron jobs—on expensive H100 instances.

Analysis from [Cast.AI's 4,000+ cluster study](https://cast.ai/blog/gpu-cost-optimization-sharing-automation/) found that in misconfigured clusters, 30% of pods running on GPU nodes don't use GPUs at all. Pure waste.

A platform engineer at a machine learning startup told me: "We thought we had a capacity problem. We needed more GPUs, right? Wrong. We had a scheduling problem. Thirty percent of our GPU node capacity was consumed by pods that never touched the GPU. Once we fixed taints and tolerations, we recovered six H100s worth of capacity—$30,000 per month—without buying a single new GPU."

**Real Numbers**: Before optimization, this startup ran 20 H100s at 18% utilization, costing $100K/month. After implementing proper node taints, right-sizing workloads based on VPA recommendations, and enabling MIG for production inference, they reduced to 7 H100s at 72% utilization, costing $35K/month. Same production workload, $65K/month savings.

## The Investigation—Three Discoveries That Explain GPU Waste

### Discovery 1: GPU Resources Are Not Like CPU/Memory

Kubernetes GPU scheduling operates under completely different rules than CPU/memory, breaking assumptions platform engineers carry from traditional resource management.

From the [official Kubernetes GPU scheduling guide](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/):

- **GPUs must be specified only in the `limits` section**. Kubernetes automatically sets request = limit.
- **You cannot request fractional GPUs**. No `nvidia.com/gpu: 0.5` allowed.
- **No overcommitment**. One pod = one full GPU lock, even if using 5% capacity.

Consider this common pattern that works perfectly for CPU and memory:

```yaml
resources:
  requests:
    memory: "4Gi"
    cpu: "1000m"
    nvidia.com/gpu: 1
  limits:
    memory: "8Gi"
    cpu: "2000m"
    nvidia.com/gpu: 1
```

This locks the entire GPU to the pod. If the workload uses 2GB of the H100's 80GB GPU memory, the remaining 78GB sits idle, completely unusable by other pods. The Kubernetes scheduler sees the GPU as "allocated" and won't schedule other GPU-requesting pods on that node.

A [Stack Overflow question](https://stackoverflow.com/questions/72956641/kubernetes-giving-each-pod-access-to-gpu) with 50+ views captures the common pain point: "Kubernetes giving each pod access to GPU." The answer: "Each pod gets exclusive GPU access unless you're using MIG or time-slicing device plugins."

This isn't a bug. It's by design. But it explains why GPU utilization hovers at 13% while CPU utilization can safely run at 70-80% in the same clusters.

> **💡 Key Takeaway**
>
> Kubernetes GPUs are atomic resources without native sharing. A pod requesting nvidia.com/gpu: 1 locks the entire GPU even if using 5% capacity. Organizations waste 60-70% of GPU budgets because default Kubernetes behavior prevents multiple workloads from sharing underutilized GPUs. MIG and time-slicing device plugins are required to enable GPU sharing.

### Discovery 2: The Hidden Cost of Round-Number Overprovisioning

Platform teams default to "safe" round numbers for GPU workloads without load testing, creating 3-5x overprovisioning that compounds with GPU exclusivity.

The pattern is everywhere:
- `memory: 16GB` (when P99 usage is 4.2GB)
- `cpu: "4000m"` (when P95 usage is 1,200m)
- `nvidia.com/gpu: 1` (when workload could share via MIG)

According to [nOps container rightsizing analysis](https://www.nops.io/blog/efficient-resource-utilization-and-rightsizing-in-kubernetes-part-1-container-rightsizing/), load testing typically reveals actual P99 usage at 3-4x lower than requested resources. At 100 pods, a cluster sized for 1,600GB RAM actually needs 420GB. With GPUs, you can't overcommit, so this translates directly to wasted hardware.

**The Measurement Gap**: Most teams deploy without the Vertical Pod Autoscaler (VPA) in recommendation mode. They guess at resource requirements based on intuition or overly conservative estimates. VPA captures P50/P95/P99 metrics over weeks across training and inference cycles, revealing actual resource consumption.

**Counterintuitive Finding**: Teams fear underprovisioning because OOMKilled incidents are visible and painful. So they overprovision by 300-400% to be "safe." But with GPUs at $5,000/month, overprovisioning costs more than occasional pod restarts.

Do the math:
- **Conservative approach**: 3x overprovisioned H100 = $15,000/month
- **Properly sized approach**: Right-sized based on P99 + 2 OOMKilled restarts/month (10min downtime each) = $5,000/month + negligible SLA impact

For non-critical ML training workloads, the business case is clear: Accept occasional restarts, save $10,000/month per GPU.

**Real Example**: An ML training pipeline:

Before (conservative guesses):
```yaml
resources:
  limits:
    memory: "32Gi"
    cpu: "8000m"
    nvidia.com/gpu: 1
```
Result: Blocks full H100, uses 8GB RAM, 2 CPU cores. Massive waste.

After (VPA-guided + MIG 1g.10gb profile):
```yaml
resources:
  limits:
    memory: "10Gi"
    cpu: "3000m"
    nvidia.com/mig-1g.10gb: 1
```
Result: Same H100 now serves 7 training jobs instead of 1. Cost per job drops from $5,000/month to $714/month (7x improvement).

> **💡 Key Takeaway**
>
> Round-number overprovisioning (16GB, 32GB memory requests without load testing) combined with GPU exclusivity creates 3-5x waste. Platform teams using Vertical Pod Autoscaler in recommendation mode to capture P95/P99 metrics over two weeks can right-size GPU workloads, enabling seven training jobs per H100 instead of one through Multi-Instance GPU profiles matched to actual resource consumption.

### Discovery 3: Regional Arbitrage and Spot Instances Are Underutilized

Platform teams anchor on AWS us-east-1 pricing, missing 2-5x cost differences across regions and 70-90% Spot instance savings because "production needs reliability."

**The Pricing Reality**: According to the [Cast.AI 2025 GPU Price Report](https://cast.ai/reports/gpu-price-2025/), H100 pricing varies dramatically:
- Specialized providers: $2.10/hour
- AWS on-demand (us-east-1): $4.09/hour
- Regional variance: us-east-1 vs us-west-2 vs eu-central-1 can differ 40-60%

Teams provisioning in optimal regions save 2-5x compared to average prices. That's not a typo—two to five times.

**The Spot Instance Myth**: "Spot instances get interrupted, we can't use them for training."

Reality check from [DigitalOcean's GPU optimization guide](https://www.digitalocean.com/resources/articles/optimize-gpu-costs):
- Modern ML frameworks (PyTorch, TensorFlow) support checkpointing every N steps
- Average Spot interruption: once every 6-20 hours (varies by region)
- Training job with hourly checkpoints: loses maximum 1 hour progress on interruption
- **Cost difference**: $0.60/hour Spot vs $4.00/hour on-demand for A100

Even with 20% interruption overhead, Spot costs $0.72 effective vs $4.00 on-demand = 82% savings.

According to [RunPod's analysis](https://www.runpod.io/articles/guides/reduce-cloud-gpu-expenses-without-sacrificing-performance), spot instances can be "40-70% cheaper" and should be used for "workloads that can handle interruption like batch processing with checkpoints."

**Regional Arbitrage in Practice**:

Team A trains models in us-east-1:
- H100 at $4.09/hour
- $98/day per GPU
- 10 GPUs × 30 days = $29,400/month

Team B trains identical models in eu-central-1:
- H100 at $2.60/hour
- $62/day per GPU
- 10 GPUs × 30 days = $18,600/month

**Difference**: $10,800/month savings by choosing a different region.

The constraint is data gravity—training data lives in us-east-1 S3. The solution: One-time data transfer cost ($500 for 10TB at $0.05/GB) amortized over months pays for itself in 1.4 days of regional savings.

**Hybrid Strategy** (Best Practice from [FinOps Foundation](https://www.finops.org/wg/finops-for-ai-overview/)):

1. **Development/Experimentation**: Spot instances, lowest-cost regions, time-slicing for rapid iteration
2. **Training**: Spot instances with checkpointing, region-optimized
3. **Inference (non-critical)**: Spot with graceful degradation
4. **Inference (production SLA)**: On-demand or reserved instances in primary region

**Real Example**: E-commerce recommendation engine:

Before (100% on-demand, us-east-1):
- 12 A100s × $4.00/hour × 720 hours = $28,800/month

After (70% Spot + 30% on-demand + eu-central-1 for training):
- Training: 8 A100s Spot × $0.80/hour × 720 hours = $4,608/month
- Inference: 4 A100s on-demand × $2.60/hour × 720 hours = $7,488/month (eu-central-1 rate)
- **Total**: $12,096/month

**Savings**: $16,704/month (58% reduction) with zero customer-facing SLA impact. Training jobs checkpoint hourly. Inference runs on on-demand instances in primary region for guaranteed availability.

> **💡 Key Takeaway**
>
> Platform teams anchoring on AWS us-east-1 on-demand pricing miss 2-5x regional cost differences and 70-90% Spot instance savings. Modern ML frameworks support checkpointing, making Spot interruptions (average once per 6-20 hours) manageable. Hybrid strategies using Spot instances for training plus regional arbitrage reduce GPU costs by 60-70% without impacting production SLAs.

## The Solution Framework—Five-Layered GPU Cost Optimization

Effective GPU cost optimization isn't a single tool or technique. It's a five-layered approach that addresses resource configuration, hardware sharing, development efficiency, cost visibility, and workload optimization.

### Layer 1: Kubernetes Resource Configuration

The foundation. Get this wrong, and nothing else matters.

**1. Proper GPU Requests/Limits**:

```yaml
resources:
  limits:
    nvidia.com/gpu: 1
    memory: "10Gi"  # P99 + 20% headroom from VPA
    cpu: "3000m"    # P95 from load testing
```

From [Kubernetes official docs](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/): No `requests` needed for GPUs—Kubernetes auto-sets GPU request = limit. This is different from CPU/memory patterns.

**2. Node Taints for GPU Nodes**:

```yaml
taints:
- key: "nvidia.com/gpu"
  operator: "Equal"
  value: "true"
  effect: "NoSchedule"
```

Prevents non-GPU workloads from consuming expensive GPU node capacity. According to [Stack Overflow discussions](https://stackoverflow.com/questions/53859237/kubernetes-scheduling-for-expensive-resources), "Taints and Tolerations are the recommended way, with the docs explicitly talking about the GPU use case."

**3. Pod Tolerations for GPU Workloads**:

```yaml
tolerations:
- key: "nvidia.com/gpu"
  operator: "Equal"
  value: "true"
  effect: "NoSchedule"
```

Only pods with this toleration can schedule on GPU-tainted nodes.

**4. Node Affinity for GPU Type Matching**:

```yaml
nodeAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
    nodeSelectorTerms:
    - matchExpressions:
      - key: "nvidia.com/gpu.product"
        operator: In
        values: ["NVIDIA-H100-80GB"]
```

Ensures workloads land on correct GPU type. Critical when mixing H100, A100, and T4 instances in the same cluster.

**Validation**: Run `kubectl get nodes -o yaml | grep nvidia.com/gpu` to verify GPU resources appear under `status.allocatable` and `status.capacity` for each node.

> **💡 Key Takeaway**
>
> Proper Kubernetes GPU configuration requires four elements: GPU limits (no requests needed), node taints on GPU nodes to prevent non-GPU workloads, pod tolerations for GPU workloads, and node affinity for GPU type matching. Platform teams implementing this baseline prevent 30% of GPU waste from misscheduled workloads before optimizing for sharing.

### Layer 2: Multi-Instance GPU (MIG) for Hardware Isolation

Multi-Instance GPU is NVIDIA's hardware-level feature for Ampere (A100, A30) and Hopper (H100) GPUs that divides a single physical GPU into up to 7 isolated instances with dedicated compute cores, memory, and cache.

From the [NVIDIA GPU Operator documentation](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html): "MIG allows a single GPU to be partitioned into multiple GPU instances, each with its own dedicated hardware resources including streaming multiprocessors (SMs) and memory."

**MIG Profiles for A100 (80GB)**:

| Profile | GPU Compute | GPU Memory | Instances per A100 | Use Case |
|---------|-------------|------------|-------------------|----------|
| 1g.10gb | 1/7 GPU | 10GB | 7 | Small model training, development |
| 2g.20gb | 2/7 GPU | 20GB | 3 | Medium models, batch inference |
| 3g.40gb | 3/7 GPU | 40GB | 2 | Large model fine-tuning |
| 7g.80gb | Full GPU | 80GB | 1 | Full-scale training |

**Implementation Steps**:

1. **Install NVIDIA GPU Operator with MIG strategy**:

```yaml
mig:
  strategy: "mixed"  # Allows different profiles per node
```

2. **Configure MIG profiles per node**:

```bash
nvidia-smi mig -cgi 1g.10gb,1g.10gb,1g.10gb,1g.10gb,1g.10gb,1g.10gb,1g.10gb
```

This creates 7 independent 1g.10gb MIG instances on a single A100.

3. **Kubernetes automatically discovers MIG instances**:

```yaml
resources:
  limits:
    nvidia.com/mig-1g.10gb: 1
```

Each MIG instance appears as a schedulable resource in Kubernetes.

**When to Use MIG**:

✅ **Best for**:
- Production inference workloads requiring isolation
- Multi-tenant clusters with security requirements
- Workloads needing guaranteed performance (no noisy neighbor effects)
- Models under 40GB that don't need full GPU compute

❌ **Not suitable for**:
- Models over 40GB requiring full GPU memory
- Workloads needing maximum GPU compute (distributed training)
- Development environments where MIG overhead isn't justified

**Real Example**: SaaS ML platform serving 50 enterprise customers, each running isolated inference workloads.

Before MIG:
- 50 dedicated A100s (one per customer for isolation)
- $0.66/hour × 50 GPUs × 720 hours = $23,760/month minimum (specialized provider rate)
- At AWS rates ($4.00/hour): $144,000/month

After MIG with 1g.10gb profiles:
- 8 A100s with 7 MIG instances each = 56 isolated GPU instances
- $0.66/hour × 8 GPUs × 720 hours = $3,802/month
- Hardware isolation maintained via MIG

**Savings**: $19,958/month (84% reduction) with maintained security boundaries between customers.

### Layer 3: Time-Slicing for Development Environments

Time-slicing is a simpler GPU sharing approach that allows multiple pods to share a single GPU sequentially without hardware partitioning. Unlike MIG, there's no isolation—workloads share the full GPU on a time-division basis.

From [Cast.AI's analysis](https://cast.ai/blog/gpu-cost-optimization-sharing-automation/): "By time-slicing GPUs, costs per developer can be reduced by 75%, and when combined with Spot GPUs (up to 60% savings), total GPU expenses can be cut by as much as 93% per developer."

**Configuration with NVIDIA Device Plugin**:

```yaml
# time-slicing-config.yaml
version: v1
sharing:
  timeSlicing:
    resources:
    - name: nvidia.com/gpu
      replicas: 4  # 4 pods share 1 GPU
```

Apply the config:
```bash
kubectl create configmap time-slicing-config -n gpu-operator \
  --from-file=time-slicing-config.yaml
```

The device plugin makes Kubernetes believe there are 4 GPUs available when physically there's 1. The scheduler can assign 4 different pods to the same physical GPU.

**Best Practices**:

✅ **Development only**: Never use for production inference with SLAs
✅ **Homogeneous workloads**: Don't mix training and inference—causes unpredictable latency
✅ **CPU-bound tasks**: Best for data preprocessing, augmentation (not GPU-intensive operations)

❌ **Avoid for**:
- Production serving with latency requirements
- Mixed training + inference on same GPU
- Security-sensitive multi-tenant scenarios

**Cost Impact**: 4 data scientists sharing 1 H100 for development = $1,250/developer/month vs $5,000 dedicated = 75% savings per developer.

According to [PerfectScale's Kubernetes GPU guide](https://www.perfectscale.io/blog/kubernetes-gpu): "Time-slicing is best for development and testing workloads where lower performance is acceptable, not for production workloads requiring predictable latency."

> **💡 Key Takeaway**
>
> Multi-Instance GPU provides hardware isolation with up to seven instances per A100, ideal for production multi-tenant workloads requiring guaranteed performance. Time-slicing enables four-plus pods to share GPUs sequentially without isolation, reducing development costs by 75% per developer. Platform teams use MIG for production inference and time-slicing for development, never mixing the two due to different security and performance characteristics.

### Layer 4: FinOps Visibility and Pod-Level Cost Tracking

You can't optimize what you can't measure. AWS EKS Split Cost Allocation Data, announced in [September 2025](https://aws.amazon.com/about-aws/whats-new/2025/09/split-cost-allocation-data-amazon-eks-nvidia-amd-gpu-trainium-inferentia-ec2/), enables pod-level GPU cost tracking across all commercial regions at no additional cost.

**How It Works**:

Pod-level costs are calculated: `(split-usage ratio) × (cost per GPU-Hour)`

If there's unused resource capacity, the unused instance cost is proportionally distributed to each pod based on usage. This means you see both:
1. Direct costs from what each pod consumes
2. Share of idle capacity waste

**Setup Steps**:

1. **Enable Split Cost Allocation** in AWS Cost Management Console

2. **Activate cost allocation tags**:
   - `aws:eks:cluster-name`
   - `aws:eks:namespace`
   - `aws:eks:workload-name`
   - `aws:eks:node`

3. **Import custom Kubernetes labels** (up to 50):

```yaml
labels:
  cost-center: "ml-research"
  team: "recommendations"
  environment: "production"
```

4. **View in AWS Cost and Usage Report** (CUR 2.0) with pod-level breakdowns

**FinOps Metrics Dashboard** (from [FinOps Foundation AI guidelines](https://www.finops.org/wg/finops-for-ai-overview/)):

| Metric | Calculation | Target | Action Threshold |
|--------|-------------|--------|------------------|
| GPU Utilization % | (Used GPU-Hours) / (Allocated GPU-Hours) | 60-85% | Under 40%: Investigate idle workloads |
| Cost Per Inference | Total GPU Cost / Request Count | Varies by model | Above P95: Optimize batch size or quantize |
| Idle GPU Hours | GPU-Hours at under 10% utilization | Under 10% of total | Above 20%: Enable time-slicing or MIG |
| Spot Adoption Rate | Spot GPU Hours / Total GPU Hours | Above 50% for training | Under 30%: Review fault-tolerant workloads |
| Cost Per Unit Work | Cost / 100K tokens (or domain metric) | Track trend | 20% increase: Review utilization |

The [FinOps Foundation](https://www.finops.org/wg/finops-for-ai-overview/) recommends tracking "Cost Per Inference = Total inference costs ÷ number of requests" and "GPU Utilization Efficiency = actual usage ÷ provisioned capacity" as core metrics.

### Layer 5: Model Optimization to Reduce GPU Requirements

Sometimes the best GPU optimization is needing fewer GPUs. Model optimization techniques reduce GPU memory and compute requirements without sacrificing ML model quality.

**Quantization**: According to [MLSysBook.ai](https://www.mlsysbook.ai/contents/core/optimizations/optimizations.html), quantization "reduces the precision of numbers used to represent model weights" from 32-bit floating point to 8-bit integers, achieving "4-8x compression with 1-2% accuracy loss." Production-grade optimization combining quantization with pruning achieves "8-15x compression with less than 1% accuracy degradation."

**Pruning**: Removes parameters within a model that have minimal impact on predictions. [Deepgram's model optimization guide](https://deepgram.com/learn/model-pruning-distillation-and-quantization-part-1) notes that "pruned models can be compressed more effectively" and result in "reduced energy consumption and cost savings."

**Distillation**: Train a smaller "student" model to mimic a larger "teacher" model's behavior. The student model requires fewer GPU resources for inference while maintaining acceptable quality.

**OpenAI Case Study**: Achieved [40% inference cost reduction](https://www.mlsysbook.ai/contents/core/optimizations/optimizations.html) through pruning and quantization techniques.

**When to Optimize**:

✅ **High-volume inference**: Over 1M requests/day where compression pays for engineering time
✅ **Edge deployment**: Memory constraints require smaller models
✅ **Cost-sensitive applications**: Tight margins where 40% reduction is material

**Tools**:
- **DeepSpeed**: Microsoft's optimization library for model compression
- **NVIDIA TensorRT**: Inference optimization specifically for NVIDIA GPUs
- **Hugging Face Optimum**: Model optimization framework for deployment

**Example**: GPT-3-175B → distilled 6B model
- 29x smaller
- 8% quality drop for Q&A tasks
- 96% inference cost reduction

For a workload serving 10M queries/day, this translates from needing 20 A100s to needing 1 A100—from $57,600/month to $2,880/month.

## Practical Implementation—90-Day Playbook

Theory doesn't pay the cloud bill. Here's the realistic timeline for implementing GPU cost optimization in a production Kubernetes environment.

### First 30 Days: Foundation & Measurement

**Week 1: Audit Current State**

Day 1-2: **GPU Inventory**
```bash
kubectl get nodes -L nvidia.com/gpu.product -L nvidia.com/gpu.count
```
Document: GPU types, quantity per node, total cluster capacity.

Day 3-4: **Cost Baseline**
Extract last 3 months GPU spend from cloud billing. Break down by:
- Total GPU spend
- Cost per cluster/namespace
- On-demand vs Spot distribution

Day 5-7: **Utilization Analysis**
Deploy [NVIDIA DCGM Exporter](https://github.com/NVIDIA/dcgm-exporter) for GPU metrics:
```bash
kubectl create namespace gpu-operator-resources
helm install dcgm-exporter nvidia/dcgm-exporter -n gpu-operator-resources
```

Query Prometheus for GPUs with under 30% utilization for over 6 hours in the last week. This is your waste identification.

**Week 2: Implement Resource Management Baseline**

Day 8-10: **Node Taints**
Add `nvidia.com/gpu=true:NoSchedule` to all GPU nodes:
```bash
kubectl taint nodes -l nvidia.com/gpu.product nonempty \
  nvidia.com/gpu=true:NoSchedule
```

Day 11-12: **Admission Controller**
Deploy [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/) policy requiring GPU limits:
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-gpu-limits
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    labels: ["nvidia.com/gpu"]
```

Day 13-14: **Validation**
Test that non-GPU pods can't schedule on GPU nodes. Deploy test workload without tolerations, verify it remains Pending with message about node taints.

**Week 3: Deploy Vertical Pod Autoscaler**

Day 15-17: **Install VPA**
```bash
kubectl apply -f https://github.com/kubernetes/autoscaler/releases/download/vertical-pod-autoscaler-1.1.0/vpa-v1.1.0.yaml
```

Day 18-21: **Enable Recommendation Mode**
For all GPU workloads, create VPA objects in "Off" mode (recommendations only, no auto-updates):
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: gpu-workload-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: ml-training
  updatePolicy:
    updateMode: "Off"  # Recommendation mode only
```

**Week 4: Enable Cost Tracking**

Day 22-24: **AWS EKS Split Cost Allocation**
1. Navigate to AWS Cost Management Console
2. Enable "Split Cost Allocation Data"
3. Activate cost allocation tags

Day 25-27: **Add Custom Labels**
Update all GPU workload deployments with:
```yaml
labels:
  cost-center: "ml-platform"
  team: "recommendations"
  environment: "production"
```

Day 28-30: **Build Dashboard**
Create Grafana dashboard with:
- GPU utilization % per namespace
- Cost per namespace (from AWS CUR)
- Idle GPU hours (under 10% util)
- Top 10 most expensive workloads

**Monday Action by Day 30**: Have baseline metrics (current utilization %, cost per workload, waste identification) and foundational controls (taints, admission policies, VPA collecting data).

### Days 31-60: Optimization & GPU Sharing

**Week 5: Right-Size Based on VPA Data**

Day 31-33: **Analyze VPA Recommendations**
```bash
kubectl describe vpa gpu-workload-vpa
```
Review P95/P99 recommendations for all workloads. Look for gaps between current requests and recommendations.

Day 34-37: **Apply Right-Sizing**
Update deployment manifests with VPA recommendations + 20% headroom:
```yaml
resources:
  limits:
    memory: "10Gi"  # VPA recommended 8.2Gi, added 20%
    cpu: "3000m"    # VPA recommended 2.4 cores
    nvidia.com/gpu: 1
```

Roll out changes gradually—10% of workloads per day.

Day 38-40: **Monitor for OOMKilled**
Watch for exit code 137. If a workload OOMKills more than twice, increase memory by 10% increments until stable.

**Week 6-7: Implement MIG for Production Inference**

Day 41-44: **Install NVIDIA GPU Operator with MIG**
```bash
helm install gpu-operator nvidia/gpu-operator \
  -n gpu-operator \
  --set mig.strategy=mixed
```

Day 45-48: **Configure MIG Profiles**
Start with 1g.10gb profiles for inference workloads under 10GB GPU memory:
```bash
nvidia-smi mig -cgi 1g.10gb,1g.10gb,1g.10gb,1g.10gb,1g.10gb,1g.10gb,1g.10gb
```

Day 49-53: **Migrate Workloads**
Update production inference deployments:
```yaml
resources:
  limits:
    nvidia.com/mig-1g.10gb: 1
```

Day 54-56: **Validation**
Verify performance SLAs maintained. Compare p50/p95/p99 latency before and after MIG. Rollback if degradation exceeds 5%.

**Week 8: Enable Time-Slicing for Development**

Day 57-59: **Identify Dev Clusters**
Non-production environments, data science experimentation clusters.

Day 60: **Apply Time-Slicing Config**
```bash
kubectl create configmap time-slicing-config \
  -n gpu-operator \
  --from-file=time-slicing-config.yaml
```

Set replicas=4 (4 users share 1 GPU) or replicas=8 for lighter workloads.

**Monday Action by Day 60**: Have 50%+ workloads right-sized based on VPA data, production inference using MIG where applicable, development clusters using time-slicing.

### Days 61-90: Advanced Optimization & Spot Adoption

**Week 9: Regional Arbitrage Analysis**

Day 61-65: **Pricing Research**
Compare H100/A100 costs across regions using [Cast.AI GPU Price Report](https://cast.ai/reports/gpu-price-2025/) data.

Day 66-68: **Data Transfer Cost Calculation**
Estimate cost to migrate training data to lower-cost region:
```
Data size (TB) × $0.05/GB = One-time cost
Compare to monthly savings × 12 months
```

Day 69-70: **ROI Calculation**
Break-even point = Data transfer cost ÷ Monthly savings

**Week 10-11: Spot Instance Pilot**

Day 71-74: **Select Pilot Workload**
Choose training job with:
- Checkpointing every 1-2 hours
- Non-critical timeline (tolerates restarts)
- GPU-intensive (high cost to optimize)

Day 75-79: **Deploy on Spot**
```yaml
nodeSelector:
  eks.amazonaws.com/capacityType: SPOT
tolerations:
- key: "nvidia.com/gpu"
  operator: "Equal"
  value: "true"
  effect: "NoSchedule"
```

Day 80-84: **Monitor Interruptions**
Track:
- Interruption frequency (how many per week)
- Recovery time (checkpoint restore + resume)
- Cost savings vs on-demand

Day 85-90: **Expand Rollout**
If successful (under 3 interruptions/week, under 15min recovery), roll out to 50% of training workloads.

**Week 12: Model Optimization Initiative**

Day 85-87: **Identify High-Volume Models**
Query metrics for models serving over 100K inferences/day. These have highest ROI for optimization.

Day 88-90: **Quantization Experiment**
Use TensorRT or Hugging Face Optimum to quantize model from FP32 to INT8:
```python
from optimum.onnxruntime import ORTQuantizer
quantizer = ORTQuantizer.from_pretrained("model_name")
quantizer.quantize(save_dir="quantized_model")
```

A/B test: Compare accuracy drop vs inference speed improvement and cost reduction.

**Monday Action by Day 90**: Have complete optimization stack implemented, Spot adoption at 30-50% for training workloads, cost tracking dashboard showing utilization improvements from 13-30% baseline to 60-85% target range.

### Red Flags—Warning Signs of Implementation Failure

⚠️ **GPU Utilization Dropping Below 20%**: If utilization decreases after MIG implementation, profiles may be too large. Reduce from 3g.40gb to 2g.20gb or 1g.10gb.

⚠️ **Increased OOMKilled Incidents**: Over-aggressive right-sizing. Add 10-20% more memory headroom to VPA-recommended values.

⚠️ **Spot Interruption Cascade**: More than 5 interruptions per hour indicates wrong region or instance type. Switch regions or use on-demand.

⚠️ **MIG Performance Degradation**: If latency increases above 10% after MIG, workload may need full GPU compute. Not all workloads are MIG-suitable.

⚠️ **Cost Increase After Optimization**: Check for unused MIG instances or misconfigured node autoscaling creating idle nodes.

### Common Mistakes

**❌ Mistake 1**: Enabling MIG on development clusters
- **Why Bad**: MIG adds scheduling complexity and overhead for workloads that don't need isolation
- **Fix**: Use time-slicing for dev environments, reserve MIG for production

**❌ Mistake 2**: Applying time-slicing to production inference
- **Why Bad**: No performance isolation, unpredictable latency breaks SLAs
- **Fix**: Use MIG or dedicated GPUs for production, time-slicing only for development

**❌ Mistake 3**: Setting VPA to "Auto" mode immediately
- **Why Bad**: VPA can kill pods during active training runs, losing hours of progress
- **Fix**: Run in recommendation mode for 2+ weeks, manually apply changes during maintenance windows

**❌ Mistake 4**: Ignoring data transfer costs in regional arbitrage
- **Why Bad**: $10,000 to transfer 50TB of training data can wipe out 6+ months of regional savings
- **Fix**: Calculate full cost including data transfer, factor in ongoing sync costs

**❌ Mistake 5**: Over-consolidating with aggressive MIG profiles
- **Why Bad**: 7× 1g.10gb instances may individually hit memory limits, causing frequent OOMKills
- **Fix**: Start with 2g.20gb or 3g.40gb profiles, optimize down gradually based on monitoring

> **💡 Key Takeaway**
>
> Successful GPU cost optimization follows a 90-day implementation timeline: foundation and measurement (Days 1-30), optimization and GPU sharing (Days 31-60), advanced optimization and Spot adoption (Days 61-90). Platform teams rushing to enable MIG or time-slicing without baseline metrics, VPA data collection, and proper node taints create more problems than they solve. Budget three months to achieve 60-85% utilization targets sustainably.

## Practical Actions This Week

### For Individual Engineers

**This Week**:
- Review your GPU-requesting pods: `kubectl get pods -o yaml | grep nvidia.com/gpu`
- Check if you're using the full GPU: Are you really using 80GB or just 4GB?
- Add resource limits if missing (admission controller will catch this soon)

**Next Month**:
- Instrument your training jobs with checkpointing every 1-2 hours
- Test Spot instances for one non-critical training job
- Measure actual GPU memory usage during training/inference

### For Platform Teams

**This Week**:
1. **Audit GPU waste**: Deploy DCGM Exporter, identify pods using under 30% of GPU capacity
2. **Apply node taints**: Prevent non-GPU workloads from consuming GPU nodes
3. **Deploy VPA**: Start collecting resource usage data (2-week minimum before acting)

**This Month**:
1. **Enable AWS EKS Split Cost Allocation** (if using EKS) for pod-level GPU cost tracking
2. **Pilot MIG**: Select 3-5 production inference workloads, test 1g.10gb or 2g.20gb profiles
3. **Document costs**: Create dashboard showing current GPU spend, utilization %, and waste identified

**Next Quarter**:
1. **Roll out MIG** to 50% of production inference workloads
2. **Implement Spot** for 30-50% of training workloads
3. **Target 60-85%** sustained GPU utilization across the cluster

### For Leadership

**Argument for Investment**:

Current state: $100K/month GPU spend at 18% utilization = $82K/month wasted capacity.

90-day optimization program:
- **Cost**: 1 senior platform engineer × 3 months at $150K salary = $37,500 labor
- **Plus**: $10K vendor support (Solo.io, Tetrate, or NVIDIA consulting)
- **Total Investment**: $47,500

Expected outcomes:
- Reduce GPU count from 20 H100s to 7 H100s via MIG and right-sizing
- Improve utilization from 18% to 70%
- New monthly cost: $35K (down from $100K)
- **Monthly Savings**: $65K
- **Annual Savings**: $780K

**Payback Period**: 0.73 months (investment recovered in 22 days)

**Ask**: Approve 90-day GPU optimization initiative with dedicated platform engineer and $10K vendor support budget.

**Timeline**:
- Month 1: Foundation (taints, VPA, cost tracking)
- Month 2: MIG rollout for production inference
- Month 3: Spot adoption for training, regional optimization
- Month 4+: Sustained 60-85% utilization, $780K annual savings realized

## 📚 Learning Resources

### Official Documentation
- [Kubernetes Schedule GPUs (Official)](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/) - Authoritative guide for GPU scheduling and device plugin configuration
- [NVIDIA GPU Operator Documentation](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html) - MIG configuration, time-slicing, and monitoring setup for Kubernetes
- [FinOps Foundation: FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/) - Best practices for AI/ML workload cost management
- [AWS Split Cost Allocation for Amazon EKS](https://aws.amazon.com/blogs/aws-cloud-financial-management/improve-cost-visibility-of-machine-learning-workloads-on-amazon-eks-with-aws-split-cost-allocation-data/) - September 2025 guide for pod-level GPU cost tracking

### Technical Guides & Tutorials
- [Kubernetes GPU Resource Management Best Practices (PerfectScale, 2025)](https://www.perfectscale.io/blog/kubernetes-gpu) - Comprehensive guide covering MIG, time-slicing, node affinity, and cost optimization (40-minute read)
- [GPU Cost Optimization: Sharing and Automation (Cast.AI, 2025)](https://cast.ai/blog/gpu-cost-optimization-sharing-automation/) - Technical deep dive on MIG vs time-slicing with real cost savings data
- [7 Strategies for GPU Cost Optimization (DigitalOcean, 2025)](https://www.digitalocean.com/resources/articles/optimize-gpu-costs) - Practical implementation guide for spot instances, right-sizing, and regional arbitrage

### Research & Case Studies
- [Google DeepMind: 40% Data Center Cooling Cost Reduction](https://deepmind.google/discover/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/) - AI-powered optimization demonstrating infrastructure efficiency gains
- [AlphaEvolve: 23% Kernel Speedup for Gemini Training](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) - Real-world GPU optimization with FlashAttention 32.5% speedup
- [Cast.AI 2025 GPU Price Report](https://cast.ai/reports/gpu-price-2025/) - H100 and A100 pricing across 66 cloud regions with regional arbitrage analysis

### Tools & Platforms
- [NVIDIA DCGM Exporter for Prometheus](https://github.com/NVIDIA/dcgm-exporter) - GPU metrics collection for Kubernetes monitoring and utilization tracking
- [Vertical Pod Autoscaler (VPA)](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler) - Automated resource request recommendations based on actual usage patterns
- [Kueue](https://kueue.sigs.k8s.io/) - Kubernetes job queueing with GPU-aware scheduling, gang scheduling, and resource quotas for multi-tenant clusters
- [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/) - Policy enforcement for Kubernetes requiring GPU limits and node taint validation

### Books & Video Courses
- [Machine Learning Engineering by Andriy Burkov (2020)](https://www.amazon.com/Machine-Learning-Engineering-Andriy-Burkov/dp/1777005469) - Chapter 8 covers infrastructure and GPU resource management for ML workloads ($45)

### Community Resources
- [CNCF Slack #gpu-operator Channel](https://cloud-native.slack.com/) - Active community (2,000+ members) for NVIDIA GPU Operator and MIG troubleshooting
- [r/kubernetes GPU Discussions](https://reddit.com/r/kubernetes) - Real-world case studies from platform engineers managing production GPU clusters
- [Stack Overflow: kubernetes+gpu Tag](https://stackoverflow.com/questions/tagged/kubernetes+gpu) - 500+ answered questions on GPU scheduling and resource management

## Related Content

**Platform Engineering & FinOps**:
- [FinOps Gets AI: How AWS, Google, and Azure Are Automating Cost Optimization](/blog/2025-11-08-finops-ai-automation-aws-google-azure-2025) - Why organizations struggle to implement AI cost savings despite sophisticated tools
- [Episode #019: The FinOps AI Paradox](/podcasts/00019-finops-ai-paradox) - Why sophisticated AI that works perfectly still fails to reduce cloud waste
- [Platform Engineering Economics: Hidden Costs and ROI](/blog/2025-01-platform-engineering-economics-hidden-costs-roi) - Build vs buy decisions for platform tools

**Kubernetes Production Best Practices**:
- [Kubernetes Production Mastery Lesson 02: Resource Management](/podcasts/00010-kubernetes-production-mastery-lesson-02) - Foundational requests/limits concepts, OOMKilled debugging, QoS classes
- [Kubernetes Technical Page](/technical/kubernetes) - Core Kubernetes concepts and production patterns
- [The Kubernetes Complexity Backlash](/blog/2025-01-16-kubernetes-complexity-backlash-simpler-infrastructure) - When Kubernetes costs outweigh benefits, including GPU cost considerations
