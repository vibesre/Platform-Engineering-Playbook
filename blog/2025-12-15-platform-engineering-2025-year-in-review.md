---
title: "Platform Engineering 2025 Year in Review: The Year We Grew Up"
description: "Comprehensive analysis of the 10 defining moments in platform engineering in 2025: AI-native Kubernetes, industry consensus, infrastructure concentration risk, IngressNightmare, agentic AI, open source sustainability, GPU waste, service mesh evolution, IaC consolidation, and Gateway API standardization."
keywords:
  - platform engineering 2025
  - platform engineering year in review
  - kubernetes ai conformance
  - dynamic resource allocation DRA
  - platform engineering trends 2025
  - cloudflare outage 2025
  - aws outage 2025
  - ingressnightmare CVE-2025-1974
  - gpu waste kubernetes
  - service mesh sidecar
  - helm 4 release
  - gateway api kubernetes
  - platform engineering consensus
  - open source sustainability
  - agentic AI platform engineering
datePublished: "2025-12-15"
dateModified: "2025-12-15"
schema:
  type: FAQPage
  questions:
    - question: "What were the biggest platform engineering developments in 2025?"
      answer: "The biggest developments in 2025 were: (1) Kubernetes AI Conformance Program v1.0 and DRA reaching GA, standardizing AI infrastructure, (2) Industry consensus on platform engineering definition (API-first self-service, business relevance, managed service approach), (3) Six major Cloudflare outages plus the AWS US-EAST-1 outage exposing infrastructure concentration risk, (4) IngressNightmare CVE-2025-1974 with CVSS 9.8 affecting 43% of cloud environments, and (5) Agentic AI entering platform engineering with 80% of companies reporting unintended agent actions."
    - question: "What is the Kubernetes AI Conformance Program launched in 2025?"
      answer: "The Kubernetes AI Conformance Program v1.0 was launched at KubeCon North America in November 2025 by the CNCF. It standardizes how AI workloads run on Kubernetes through five core requirements: Dynamic Resource Allocation (DRA), intelligent autoscaling, accelerator metrics, AI operators, and gang scheduling. Eleven vendors certified immediately including Google Cloud, Azure, Oracle, CoreWeave, and AWS. Teams implementing DRA properly are seeing 30-40% GPU cost savings."
    - question: "What is the platform engineering definition that emerged in 2025?"
      answer: "In 2025, the platform engineering industry reached consensus on three defining principles: (1) API-first self-service - platforms expose capabilities through APIs that developers consume directly, not tickets, (2) Business relevance - platforms tie their value to business outcomes, not just technical metrics, (3) Managed service approach - internal platforms should feel like using a cloud service. However, DORA 2025 shows that while 90% of organizations have platform initiatives, platform teams decreased throughput by 8% and stability by 14% on average due to the 'puppy for Christmas' anti-pattern."
    - question: "What was IngressNightmare CVE-2025-1974?"
      answer: "IngressNightmare (CVE-2025-1974) was a critical vulnerability disclosed on March 24, 2025 with a CVSS score of 9.8. It enabled unauthenticated remote code execution in ingress-nginx, exposing 43% of cloud environments and 6,500+ clusters including Fortune 500 companies. This led to the announcement that Ingress NGINX will retire in March 2026, giving platform teams a hard migration deadline to Gateway API."
    - question: "How many Cloudflare outages occurred in 2025?"
      answer: "Cloudflare experienced six major outages in 2025. The most significant were on November 18 (a Rust panic took down 20% of the internet for 6 hours, affecting ChatGPT, X, Shopify, Discord, Spotify) and December 5 (28% of HTTP traffic impacted for 25 minutes). Combined with the AWS US-EAST-1 outage on October 19 ($75M/hour impact), 2025 proved that infrastructure concentration risk is real and multi-region, multi-cloud strategies are essential risk management."
    - question: "What is the open source sustainability crisis in platform engineering?"
      answer: "The 2025 open source sustainability crisis was highlighted by CNCF's 10-year anniversary statistics: while there are 300,000 contributors across hundreds of projects, 60% of maintainers are unpaid and 60% have left or are considering leaving. The XZ Utils backdoor from 2024 cast a long shadow, showing how lone burned-out maintainers can unknowingly introduce security risks. The industry is responding with the Open Source Pledge recommending $2,000 per developer per year to fund dependent projects."
    - question: "What is GPU waste and how bad is it in 2025?"
      answer: "GPU waste became impossible to ignore in 2025. The average H100 GPU runs at only 13% utilization, meaning $4,350/month wasted per GPU (at $3/hour cloud pricing). Across the industry, 60-70% of GPU budgets are wasted. Techniques like DRA, time-slicing, MIG partitioning, spot instances, and regional arbitrage are now mandatory knowledge. Real case studies show 65% GPU reduction (20 H100s to 7) with $35,000 monthly savings for the same workloads."
    - question: "What happened to Infrastructure as Code in 2025?"
      answer: "Infrastructure as Code saw major consolidation in 2025: IBM acquired HashiCorp for $6.4 billion, HashiCorp deprecated CDKTF after 5 years (effectively conceding to Pulumi), OpenTofu achieved feature parity and crossed 10 million downloads in July, and Helm 4.0 released in November with WASM plugins and Server-Side Apply. ArgoCD 3.0 went GA in May with fine-grained RBAC and better scaling."
    - question: "What is the service mesh evolution in 2025?"
      answer: "The sidecar era is ending. Istio Ambient mode reached GA in 2025 with 90% memory reduction and 50% CPU reduction compared to sidecar architecture. Benchmarks show 8% mTLS overhead for Ambient versus 99% for Cilium. At 2,000 pods, this translates to $186,000 annual savings. 70% of organizations now run service mesh, and the eBPF approach (Cilium, Tetragon) continues gaining ground for networking, security, and observability."
    - question: "What should platform engineers focus on in 2026?"
      answer: "Key action items for 2026: (1) Migrate to Gateway API before March 2026 when Ingress NGINX retires, (2) Implement DRA for AI workloads to achieve 30-40% cost savings, (3) Audit agent policies (only 44% of companies have them), (4) Review Cloudflare and AWS single dependencies for concentration risk, (5) Sponsor an open source project ($2K/dev/year recommended). The CNPE certification will also create a professionalization wave for platform engineers."
---

2025 was the year platform engineering grew up—and got a reality check. AI entered infrastructure in ways we couldn't ignore with the [Kubernetes AI Conformance Program v1.0](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program/) and DRA reaching GA. Industry consensus finally emerged on what platforms should actually do. And then Cloudflare went down six times, AWS US-EAST-1 went dark for 14 hours, and IngressNightmare exposed 43% of cloud environments—reminding us that concentration risk isn't theoretical.

This comprehensive analysis covers the 10 defining stories of platform engineering in 2025, examining what happened, what it means, and what you should do about it in 2026.

> 🎙️ **Listen to the podcast episode**: [Episode #059: Platform Engineering 2025 Year in Review](/podcasts/00059-platform-engineering-2025-year-in-review) - A 25-minute deep dive into the year's most significant developments.

<iframe width="100%" style={{aspectRatio: '16/9', marginBottom: '1rem'}} src="https://www.youtube.com/embed/Q_w1sOcviAU" title="Episode #059: Platform Engineering 2025 Year in Review" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerPolicy="strict-origin-when-cross-origin" allowFullScreen></iframe>

## TL;DR

**The Year in One Sentence**: 2025 was when AI infrastructure standardized on Kubernetes, platform engineering found its definition, and catastrophic outages proved that concentration risk management is non-negotiable.

**Top 5 Takeaways**:
1. **AI infrastructure is now standardized** — Kubernetes AI Conformance Program v1.0 means vendor lock-in is optional if you architect correctly
2. **Platform engineering has a definition** — API-first self-service, business relevance, managed service approach
3. **Concentration risk is real** — Multi-region, multi-cloud, multi-CDN isn't paranoia—it's risk management
4. **Open source needs funding** — If you depend on it, pay for it ($2K/dev/year recommended)
5. **GPU waste is the new cloud waste** — 13% utilization is unacceptable; DRA and time-slicing are table stakes

**Critical Deadlines**: Ingress NGINX retires March 2026. If you haven't migrated to Gateway API, start now.

## Key Statistics: Platform Engineering 2025

| Metric | Value | Source | Context |
|--------|-------|--------|---------|
| Platform team failure rate | 45-70% | [DORA 2024/2025](https://dora.dev/) | Most fail due to "puppy for Christmas" anti-pattern |
| GPU utilization average | 13% | [Kubernetes GPU FinOps](https://cast.ai/) | Represents $4,350/month waste per H100 |
| AWS US-EAST-1 outage cost | $75M/hour | [October 2025 incident](https://aws.amazon.com/) | 14+ hour duration, 6.5M downtime reports |
| Cloudflare major outages | 6 in 2025 | Our analysis | November 18: 20% of internet down |
| IngressNightmare exposure | 43% of clouds | [CVE-2025-1974](https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities) | 6,500+ clusters exposed |
| CNCF maintainers unpaid | 60% | [KubeCon community report](https://www.cncf.io/) | 60% have left or considering leaving |
| Platform engineer salary premium | 20-27% over DevOps | Multiple sources | Reflects specialized skills demand |
| Global cloud spend | $720B | [FinOps research](https://www.finops.org/) | 20-30% waste estimated |
| Agents executing unintended actions | 80% of companies | [AWS re:Invent 2025](https://reinvent.awsevents.com/) | Werner Vogels' "verification debt" |
| Agent security policies | Only 44% have them | Research | 56% are accepting significant risk |
| Organizations with platforms | 90% | [DORA 2025](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) | Near-universal adoption |
| Platform team productivity impact | -8% throughput, -14% stability | [DORA 2024](https://dora.dev/) | When poorly structured |
| Service mesh adoption | 70% | [CNCF Survey](https://www.cncf.io/reports/) | Sidecar era ending |
| Istio Ambient memory reduction | 90% | Benchmarks | vs sidecar architecture |
| OpenTofu downloads | 10M+ | [OpenTofu](https://opentofu.org/) | Feature parity achieved July 2025 |
| Crossplane adopters | 70+ | [CNCF Graduation](https://www.cncf.io/) | Including Nike, NASA, SAP |

---

## Story #1: AI-Native Kubernetes Arrived

At KubeCon North America in November, the [CNCF launched the Kubernetes AI Conformance Program v1.0](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program/). This wasn't just another certification—it was the industry finally standardizing how AI workloads run on Kubernetes.

### The Technical Foundation

[Dynamic Resource Allocation (DRA)](https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/) reached general availability in Kubernetes 1.34. DRA fundamentally changes how GPUs and accelerators are managed:

- **Before DRA**: Static allocation where GPUs are reserved at pod creation, leading to waste
- **After DRA**: Workloads request specific GPU capabilities dynamically, enabling better utilization

Eleven vendors certified immediately: Google Cloud, Azure, Oracle, CoreWeave, AWS, and others. The five core requirements for conformance are:

1. **Dynamic Resource Allocation** — GPU and accelerator management
2. **Intelligent Autoscaling** — AI-aware scaling based on workload characteristics
3. **Accelerator Metrics** — Standardized observability for AI hardware
4. **AI Operators** — Kubernetes-native management of AI frameworks
5. **Gang Scheduling** — Coordinated scheduling for distributed training

### The Business Impact

Teams implementing DRA properly are seeing **30-40% GPU cost savings**. That's not incremental—that's transformational for AI infrastructure budgets.

> 💡 **Key Takeaway**: The standardization war is over. Kubernetes won as AI infrastructure, and vendor lock-in is now optional if you architect correctly.

---

## Story #2: Platform Engineering Reached Consensus (But 70% Still Fail)

After years of definitional chaos where everyone had a different opinion on what platform engineering even meant, 2025 brought consensus.

### The Three Principles

Across multiple KubeCon talks, industry reports, and practitioner discussions, three principles emerged:

1. **API-first self-service** — Platforms expose capabilities through APIs that developers consume directly, not tickets they submit and wait on
2. **Business relevance** — Platforms tie their value to business outcomes, not just technical metrics
3. **Managed service approach** — Internal platforms should feel like using a cloud service, not fighting with infrastructure

### The Uncomfortable Truth

The adoption data from [DORA 2025](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) is striking:

- **90% of organizations** now have platform initiatives (near-universal)
- But platform teams **decreased throughput by 8%** and **stability by 14%** on average

How is that possible? The "puppy for Christmas" anti-pattern. Organizations adopt platforms like a child receives a puppy—excitement at first, then the realization that it requires constant feeding, training, and attention. Most teams renamed their ops team "platform engineering" and expected different results.

### What Actually Works

The teams that succeed share common characteristics:
- **Optimal size**: 6-12 people following the Spotify squad model
- **Dedicated leadership**: Platform leader at 100+ engineers to shield from competing priorities
- **Evolution**: Starting with collaboration while building, then transitioning to X-as-a-Service when mature

When done right: **8-10% individual productivity boost**, **10% team productivity boost**. But getting there requires treating the platform as a product with actual product management discipline.

> 💡 **Key Takeaway**: Platform engineering has a definition now. Use it. And treat your platform as a product, not a project.

---

## Story #3: Infrastructure Concentration Risk Became Undeniable

2025 will be remembered as the year infrastructure concentration risk became undeniable.

### AWS US-EAST-1: The Fourteen-Hour Darkness

October 19, 2025. [AWS US-EAST-1 went down](https://aws.amazon.com/)—not partially, not briefly. For over 14 hours, 70+ AWS services were degraded or unavailable.

- **Root cause**: A DNS race condition in DynamoDB
- **Impact**: 6.5 million downtime reports globally
- **Cost estimates**: Up to $75 million per hour

### Cloudflare: Six Times in One Year

Then came Cloudflare. Not once. Not twice. **Six major outages in 2025**.

**November 18**: A Rust panic in their proxy code took down 20% of the internet for 6 hours. ChatGPT, X, Shopify, Discord, Spotify—all affected.

**December 5**: Just three weeks later, 28% of HTTP traffic impacted for 25 minutes.

### The Pattern

The organizations we depend on are single points of failure for massive portions of the internet. Multi-region, multi-cloud, multi-CDN strategies aren't paranoid overengineering—they're risk management.

As DevOps.com summarized it: "The cloud spent years telling us it was too big to fail, but 2025 was the year that theory met reality."

> 💡 **Key Takeaway**: Review your concentration risk. If you depend on a single provider for critical services, 2025 proved that's unacceptable risk.

---

## Story #4: IngressNightmare: The Vulnerability Nobody Saw Coming

**CVE-2025-1974**. Disclosed March 24 with a CVSS score of **9.8**. Unauthenticated remote code execution in ingress-nginx.

### The Exposure

- **43% of cloud environments** were vulnerable
- **6,500+ clusters** exposed, including Fortune 500 companies
- Cluster-wide secret exposure possible

### The Response

The response was equally dramatic. [Ingress NGINX announced retirement](https://kubernetes.io/blog/2025/04/11/ingress-nginx-eol/) with a **March 2026 deadline**:
- Only 1-2 maintainers remained
- No security patches after the deadline
- Platform teams now have a hard migration deadline to Gateway API

This vulnerability reinforced the open source sustainability crisis: critical infrastructure maintained by volunteers who eventually burn out.

> 💡 **Key Takeaway**: Start your Gateway API migration now. March 2026 is closer than you think, and you don't want to rush a networking layer change.

---

## Story #5: Agentic AI Entered Platform Engineering

While Kubernetes standardized AI *workloads*, AWS re:Invent in December introduced something else entirely: **agentic AI for platform engineering**.

### The Capabilities

- **AWS DevOps Agent**: Can identify root causes of incidents with 86% accuracy
- **GitHub Agent HQ**: Orchestrating multiple AI agents from different providers
- Autonomous remediation, deployment decisions, and infrastructure management

### The Warning Signs

Werner Vogels coined a term that resonated: **verification debt**.

It's like technical debt, but for AI systems. Every autonomous action an agent takes without human verification accumulates verification debt. The sobering reality:
- **80% of companies** report their agents have executed unintended actions
- **Only 44%** have agent-specific security policies
- **Gartner predicts** 40% of agentic AI projects will fail by 2027

While AI infrastructure is standardizing on Kubernetes, the autonomous AI layer above it is still the wild west.

> 💡 **Key Takeaway**: If you're adopting agentic AI, implement agent-specific security policies now. The 56% without them are accepting significant risk.

---

## Story #6: Open Source Sustainability Crisis

The [CNCF celebrated its tenth birthday](https://www.cncf.io/) at KubeCon Europe in London. 300,000 contributors. Hundreds of projects. Incredible growth.

But behind those numbers:
- **60% of maintainers are unpaid**
- **60% have left or are considering leaving**

### The XZ Utils Shadow

The XZ Utils backdoor from late 2024 cast a long shadow over 2025. A lone maintainer, burned out, unknowingly merged malicious code. It reminded the entire industry that our infrastructure depends on volunteers who often receive no compensation.

At KubeCon Atlanta, there was a memorial for Han Kang, the in-toto project lead. These aren't anonymous contributors—they're people with lives, families, and limits.

### The Industry Response

- **CNCF invested over $3 million** in security audits, tooling, and frameworks
- **The Open Source Pledge** is gaining traction: $2,000 per developer per year to fund dependent projects
- Governance reforms: CNCF went from 6 to 4 subteams for sustainability

If your company runs on Kubernetes and doesn't contribute financially to open source, 2025 should be your wake-up call.

> 💡 **Key Takeaway**: Pick an open source project you depend on and fund it. The CNCF, Apache, and Linux Foundation all accept contributions.

---

## Story #7: GPU Economics Exposed Massive Waste

GPU waste became impossible to ignore in 2025.

### The Numbers

- **Average H100 utilization: 13%**
- At $3/hour cloud pricing, that's **$4,350/month wasted per GPU**
- **60-70% of GPU budgets wasted** across the industry

### Real-World Results

In [Episode #034](/podcasts/00034-kubernetes-gpu-cost-waste-finops), we covered a case study where a team went from 20 H100s to 7 H100s:
- **65% GPU reduction**
- **$35,000 monthly savings**
- Same workloads

### The Techniques

These aren't advanced techniques anymore—they're mandatory knowledge:
- **DRA (Dynamic Resource Allocation)**
- **Time-slicing**
- **MIG partitioning**
- **Spot instances**
- **Regional arbitrage**

> 💡 **Key Takeaway**: Audit your GPU utilization. If you're running AI workloads, you're almost certainly wasting significant budget.

---

## Story #8: Service Mesh Sidecar Era Ended

[Istio Ambient mode reached general availability](https://istio.io/latest/news/releases/1.23.x/announcing-1.23/), and the benchmarks are striking:
- **90% memory reduction**
- **50% CPU reduction**
- Compared to sidecar architecture

### The Adoption Data

**70% of organizations** now run service mesh. The sidecar era is ending.

We [benchmarked Istio Ambient against Cilium](/podcasts/00033-service-mesh-showdown-cilium-istio-ambient) in episode 33:
- **8% mTLS overhead** for Ambient
- **99% mTLS overhead** for Cilium
- At 2,000 pods: **$186,000 annual savings**

### The eBPF Momentum

eBPF continues its march. Cilium, Tetragon, and the entire eBPF ecosystem are becoming the default for networking, security, and observability. The kernel-native approach is winning.

This week, Meta announced [BPF Jailer](https://lpc.events/event/19/contributions/2159/) at Linux Plumbers Conference—using eBPF-based Mandatory Access Control to replace SELinux for AI workloads. The shift from static policies to programmable runtime policies continues.

> 💡 **Key Takeaway**: If you're still running sidecar-based service mesh, evaluate Ambient mode. The resource savings are substantial.

---

## Story #9: Infrastructure as Code Consolidated

Infrastructure as Code saw major consolidation in 2025.

### The Acquisitions and Deprecations

- **IBM acquired HashiCorp** for $6.4 billion
- **CDKTF deprecated** after 5 years—HashiCorp effectively conceded the CDK war to Pulumi
- **OpenTofu achieved feature parity** in July and crossed 10 million downloads

For teams committed to open source, the path is clear: OpenTofu.

### Tool Releases

**Helm 4.0** released at KubeCon Atlanta—the first major version in six years:
- WebAssembly plugins for portability
- Server-Side Apply replacing three-way merge
- **40-60% faster deployments** for large releases

If you're still on Helm 3, you have a 12-month support runway until November 2026.

**ArgoCD 3.0** went GA in May with fine-grained RBAC, security improvements, and better scaling characteristics.

### CNCF Graduations

Three significant graduations:
- **Crossplane** (November) — 70+ adopters including Nike, NASA, SAP
- **Knative** (October) — Serverless event-driven platform matured
- **CubeFS** (January) — Proved distributed storage at 350 petabytes scale

> 💡 **Key Takeaway**: If you're using CDKTF, start your migration to Pulumi or native Terraform. If you're on Helm 3, plan your upgrade path.

---

## Story #10: Gateway API Became the Standard

[Gateway API v1.4 reached general availability](https://gateway-api.sigs.k8s.io/) in October, cementing its position as the successor to Ingress.

### The Architecture

Gateway API's multi-role architecture was accepted:
- **Infrastructure Provider** — Manages the underlying infrastructure
- **Cluster Operator** — Configures gateways and policies
- **Application Developer** — Defines routes

This separation of concerns addresses one of Ingress's fundamental limitations.

### The Deadline

With Ingress NGINX retiring in March 2026, this isn't optional. Platform teams have approximately 3 months to:
1. Evaluate their current Ingress usage
2. Select Gateway API implementation (Istio, Cilium, NGINX Gateway Fabric, etc.)
3. Plan and execute migration
4. Validate in staging and production

> 💡 **Key Takeaway**: Gateway API migration is your most urgent 2026 action item. Start now.

---

## 2025 Timeline: Major Events

### Q1 (January - March)
- **January 21**: CubeFS CNCF Graduation (350 petabytes stored)
- **February**: IBM acquires HashiCorp ($6.4B)
- **March 24**: IngressNightmare CVEs disclosed (CVSS 9.8)

### Q2 (April - June)
- **April 1-4**: KubeCon EU London (13K attendees, CNCF 10th birthday)
- **May 6**: ArgoCD v3.0 GA
- **June**: Kubernetes AI Conformance Program beta

### Q3 (July - September)
- **July**: OpenTofu feature parity achieved, 10M+ downloads
- **August**: Istio Ambient multi-cluster Alpha
- Kubernetes v1.31 & v1.34 releases

### Q4 (October - December)
- **October 6**: Gateway API v1.4 GA
- **October 8**: Knative CNCF Graduation
- **October 19**: AWS US-EAST-1 Outage (14+ hours, $75M/hour)
- **November 6**: Crossplane CNCF Graduation
- **November 10-13**: KubeCon NA Atlanta (9K attendees)
- **November 11**: Kubernetes AI Conformance v1.0
- **November 12**: Helm 4.0 Release
- **November 12**: Ingress NGINX Retirement Announced
- **November 18**: Cloudflare November Outage (20% of internet)
- **November 30 - December 4**: AWS re:Invent (Agentic AI announcements)
- **December 5**: Cloudflare December Outage (6th major outage)
- **December 10**: CDKTF Deprecated

---

## What's Coming in 2026

### Hard Deadlines

**March 2026**: Ingress NGINX retires. No more security patches. If you haven't migrated to Gateway API, your clusters are vulnerable.

### Predictions

1. **Agentic AI adoption accelerates**, but verification debt becomes a real problem. The companies that figure out agent governance early will have significant advantages.

2. **Platform teams at enterprise scale face new challenges**. [Okta's journey from 12 to 1,000 clusters](/podcasts/00058-okta-gitops-argocd-1000-clusters) previews the ArgoCD scaling, sharding, and hub-spoke architecture lessons that more organizations will need.

3. **CNPE certification** creates a professionalization wave. 2026 might be the year platform engineering gets its CKA equivalent.

4. **Multi-cluster management becomes standard**, not exceptional.

5. **SBOM requirements become federal mandate** for many vendors.

---

## Action Items for 2026

1. **Migrate to Gateway API before March** — Ingress NGINX is retiring and you don't want to rush a networking layer change

2. **Implement DRA for AI workloads** — 30-40% cost savings are achievable with proper implementation

3. **Audit your agent policies** — If you're in the 56% without agent-specific security policies, you're accepting significant risk

4. **Review your Cloudflare and AWS dependencies** — 2025 proved that these providers can fail dramatically; ensure you have multi-provider strategies for critical services

5. **Sponsor an open source project** — The CNCF, Apache, and Linux Foundation all accept contributions. Pick a project you depend on and fund it. The recommended amount is $2,000 per developer per year.

---

## Conclusion

2025 was the year platform engineering grew up. AI arrived in ways we're still processing. Consensus emerged on what platforms should actually do. And reality tested our assumptions about reliability and sustainability.

The fundamentals remain constant: reliability, security, cost efficiency. But the tools, patterns, and threats keep evolving. The infrastructure you build in 2026 should reflect these lessons.

---

## Related Resources

### Podcast Episodes
- [Episode #059: Platform Engineering 2025 Year in Review](/podcasts/00059-platform-engineering-2025-year-in-review)
- [Episodes #035-037: KubeCon Atlanta 2025 Coverage](/podcasts/00035-kubecon-2025-ai-native)
- [Episodes #049-052: AWS re:Invent 2025 Series](/podcasts/00049-aws-reinvent-2025-agentic-ai-revolution)
- [Episode #030: Cloudflare November Outage](/podcasts/00030-cloudflare-outage-november-2025)
- [Episode #047: Cloudflare December Outage](/podcasts/00047-cloudflare-december-2025-outage-trust-crisis)
- [Episode #058: Okta GitOps Journey](/podcasts/00058-okta-gitops-argocd-1000-clusters)
- [Episode #034: GPU Waste and FinOps](/podcasts/00034-kubernetes-gpu-cost-waste-finops)
- [Episode #033: Service Mesh Showdown](/podcasts/00033-service-mesh-showdown-cilium-istio-ambient)

### Blog Posts
- [Platform Engineering Team Structures That Work](/blog/platform-engineering-team-structures-that-work)
- [Platform Engineering vs DevOps vs SRE](/blog/platform-engineering-vs-devops-vs-sre)
- [Cloudflare December 2025 Outage](/blog/cloudflare-december-2025-outage-trust-infrastructure-concentration-risk)
- [AWS re:Invent 2025 Complete Guide](/blog/aws-reinvent-2025-complete-platform-engineering-guide)

### External Sources
- [DORA 2024/2025 Reports](https://dora.dev/)
- [CNCF Annual Survey](https://www.cncf.io/reports/)
- [Kubernetes AI Conformance Program](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program/)
- [Gateway API Documentation](https://gateway-api.sigs.k8s.io/)
- [CVE-2025-1974 IngressNightmare](https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities)
- [Helm 4.0 Release Notes](https://helm.sh/blog/helm-4-released/)
