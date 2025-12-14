---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #059: Platform Engineering 2025 Year in Review"
slug: 00059-platform-engineering-2025-year-in-review
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #059: Platform Engineering 2025 Year in Review

<GitHubButtons />

<iframe width="100%" style={{aspectRatio: '16/9', marginBottom: '1rem'}} src="https://www.youtube.com/embed/PLACEHOLDER" title="Episode #059: Platform Engineering 2025 Year in Review" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerPolicy="strict-origin-when-cross-origin" allowFullScreen></iframe>

**Duration**: ~25 minutes | **Speakers**: Jordan & Alex

**Target Audience**: Platform engineers, SREs, DevOps leads, engineering managers

> 📝 **Read the [full blog post](/blog/platform-engineering-2025-year-in-review)**: A comprehensive written analysis with all statistics, sources, and action items for 2026.

---

## Synopsis

2025 was the year platform engineering grew up—and got a reality check. AI entered infrastructure in ways we couldn't ignore. Industry consensus emerged on what platforms should actually do. And then Cloudflare went down six times to remind us that concentration risk isn't theoretical. This episode covers the ten stories that defined platform engineering in 2025, plus news on Meta's BPF Jailer, the "too big to fail" myth, and sustainable platform design principles.

---

## News Segment

Three stories that perfectly bookend 2025:

1. **[The Self-Inflicted Outage: When "Too Big to Fail" Meets the Reality of Hyperscale Complexity](https://devops.com/the-self-inflicted-outage-when-too-big-to-fail-meets-the-reality-of-hyperscale-complexity/)** (DevOps.com) - The cloud spent years telling us it was too big to fail, but 2025 was the year that theory met reality. Recovery complexity is now the biggest risk to uptime.

2. **[Meta's BPF Jailer: eBPF-based Mandatory Access Control](https://lpc.events/event/19/contributions/2159/)** (Linux Plumbers Conference 2025) - Meta announced they're using eBPF-based Mandatory Access Control to replace SELinux for AI workloads. A significant shift from static compile-time policies to programmable policies loaded at runtime.

3. **[Three Core Principles for Sustainable Platform Design](https://thenewstack.io/three-core-principles-for-sustainable-platform-design/)** (The New Stack) - Platform as a product extends platform engineering beyond a narrow technology solution. The three principles: highly contextualized tooling, scalability, and sustainability.

---

## Chapter Markers

- **00:00** - News Segment: Hyperscale Complexity, BPF Jailer, Platform Design
- **03:00** - Introduction: The Year Platform Engineering Grew Up
- **05:00** - Story #1: AI-Native Kubernetes Arrived (DRA GA, AI Conformance v1.0)
- **07:30** - Story #5: Agentic AI Entered Platform Engineering
- **10:00** - Story #2: Platform Engineering Reached Consensus (But 70% Still Fail)
- **13:00** - Story #3: Infrastructure Concentration Risk (AWS, Cloudflare Outages)
- **15:00** - Story #4: IngressNightmare (CVE-2025-1974)
- **16:30** - Story #6: Open Source Sustainability Crisis
- **18:30** - Story #9: Infrastructure as Code Consolidated
- **20:00** - Story #7 & #8: GPU Economics & Service Mesh Evolution
- **22:00** - What's Coming in 2026
- **24:00** - Top 5 Takeaways & Action Items

---

## Key Statistics from 2025

| Metric | Value | Source |
|--------|-------|--------|
| Platform team failure rate | 45-70% | DORA 2024/2025 |
| GPU utilization average | 13% | Kubernetes GPU FinOps |
| AWS outage cost | $75M/hour | October 2025 incident |
| Cloudflare major outages | 6 in 2025 | Analysis |
| IngressNightmare exposure | 43% of clouds | CVE-2025-1974 |
| CNCF maintainers unpaid | 60% | KubeCon community report |
| Platform engineer salary premium | 20-27% over DevOps | Multiple sources |
| Global cloud spend | $720B (20-30% waste) | FinOps research |
| Agents executing unintended actions | 80% of companies | AWS re:Invent |
| Agent security policies | Only 44% have them | Research |

---

## 10 Defining Stories of 2025

### 1. AI-Native Kubernetes Arrived
- **Kubernetes AI Conformance Program v1.0** launched at KubeCon NA (November 11)
- **DRA (Dynamic Resource Allocation)** reached GA in Kubernetes 1.34
- 11+ vendors certified (Google, Azure, Oracle, CoreWeave, AWS)
- 30-40% GPU cost savings with proper DRA implementation

### 2. Platform Engineering Reached Consensus (But 70% Still Fail)
- Industry agreed on 3 principles: API-first self-service, business relevance, managed service approach
- DORA 2025: 90% of organizations have platform initiatives
- Reality: platform teams decreased throughput 8%, stability 14%
- "Puppy for Christmas" anti-pattern explains most failures

### 3. Infrastructure Concentration Risk Became Real
- **AWS US-EAST-1 outage** (October 19): $75M/hour, 6.5M downtime reports
- **Cloudflare**: 6 major outages (November 18: 20% of internet down)
- Pattern exposed dependency risks most organizations ignored

### 4. IngressNightmare: The Vulnerability Nobody Saw Coming
- **CVE-2025-1974**: CVSS 9.8, unauthenticated RCE
- 43% of cloud environments vulnerable, 6,500+ clusters exposed
- **Ingress NGINX retirement** announced: March 2026 deadline

### 5. Agentic AI Entered Platform Engineering
- AWS DevOps Agent: 86% root cause identification
- GitHub Agent HQ for multi-agent orchestration
- 80% of companies report unintended agent actions
- Gartner: 40% of agentic AI projects will fail by 2027

### 6. Open Source Sustainability Crisis
- CNCF 10-year anniversary: 300K contributors, 60% unpaid
- XZ Utils backdoor aftermath, Han Kang memorial
- Open Source Pledge: $2K/dev/year recommended

### 7. GPU Economics Exposed Massive Waste
- Average H100 utilization: 13% ($4,350/month waste per GPU)
- 60-70% of GPU budgets wasted industry-wide
- DRA, time-slicing, MIG becoming mandatory knowledge

### 8. Service Mesh Sidecar Era Ended
- Istio Ambient GA: 90% memory, 50% CPU reduction
- 70% of organizations now running service mesh
- eBPF approach (Cilium, Tetragon) gaining ground

### 9. Infrastructure as Code Consolidated
- IBM acquired HashiCorp ($6.4B)
- CDKTF deprecated (Pulumi won)
- Helm 4.0: First major version in 6 years
- OpenTofu: 10M+ downloads, feature parity achieved

### 10. Gateway API Became the Standard
- Gateway API v1.4 GA replaced Ingress as modern default
- Platform teams have until March 2026 to migrate

---

## 2025 Timeline

### Q1 (January - March)
- CubeFS CNCF Graduation (Jan 21)
- IBM acquires HashiCorp
- IngressNightmare CVEs disclosed (Mar 24)

### Q2 (April - June)
- KubeCon EU London (Apr 1-4) - 13K attendees
- ArgoCD v3.0 GA (May 6)
- Kubernetes AI Conformance beta

### Q3 (July - September)
- Kubernetes v1.31 & v1.34 releases
- Istio Ambient multi-cluster Alpha
- OpenTofu feature parity achieved

### Q4 (October - December)
- Knative CNCF Graduation (Oct 8)
- AWS US-EAST-1 Outage (Oct 19)
- Gateway API v1.4 GA (Oct 6)
- Crossplane CNCF Graduation (Nov 6)
- KubeCon NA Atlanta (Nov 10-13)
- Helm 4.0 Release (Nov 12)
- Kubernetes AI Conformance v1.0 (Nov 11)
- Ingress NGINX Retirement Announced (Nov 12)
- Cloudflare November Outage (Nov 18)
- AWS re:Invent (Nov 30 - Dec 4)
- Cloudflare December Outage (Dec 5)
- CDKTF Deprecated (Dec 10)

---

## Top 5 Takeaways

1. **AI infrastructure is now standardized** - Kubernetes AI Conformance v1.0 means vendor lock-in is optional
2. **Platform engineering has a definition** - API-first self-service, business relevance, managed service approach
3. **Concentration risk is real** - Multi-region, multi-cloud, multi-CDN isn't paranoia
4. **Open source needs funding** - $2K/dev/year recommended for projects you depend on
5. **GPU waste is the new cloud waste** - 13% utilization is unacceptable

## Action Items for 2026

1. Migrate to Gateway API before March 2026
2. Implement DRA for AI workloads (30-40% savings possible)
3. Audit your agent policies (56% don't have them)
4. Review Cloudflare/AWS single dependencies
5. Sponsor an open source project

---

## Transcript

### News Segment

**Jordan**: Before we dive into our year-in-review special, let's cover three news stories that perfectly bookend twenty twenty-five. First up, DevOps dot com published a piece called The Self-Inflicted Outage that captures exactly what happened this year. The thesis? The cloud spent years telling us it was too big to fail, but twenty twenty-five was the year that theory met reality.

**Alex**: This article connects directly to what we've been covering all year. From null pointers to DNS race conditions, we watched a steady procession of outages turn the internet into loading screens. AWS, Azure, Cloudflare. The key insight is that recovery complexity is now the biggest risk to uptime. The systems designed for resilience failed twice: once in the primary automation, and again in the recovery automation.

**Jordan**: Second story: Meta announced BPF Jailer at Linux Plumbers Conference this week. They're using eBPF-based Mandatory Access Control to replace SELinux for AI workloads. The proliferation of AI workloads required increased security around key services, specifically jailing untrusted code and preventing tampering with user data.

**Alex**: BPF Jailer blocks access to the network, filesystem, and IPC using BPF LSM in a flexible way tailored to AI workloads. This is a significant shift from static compile-time policies like SELinux rules to programmable policies loaded at runtime. It's part of the broader eBPF momentum we're seeing across the industry.

**Jordan**: And third, The New Stack published Three Core Principles for Sustainable Platform Design. Platform as a product extends platform engineering beyond a narrow technology solution. The three principles? Highly contextualized tooling, scalability, and sustainability. An effective platform gives software teams more time for revenue-focused work.

**Alex**: The key point is that technology-focused platform designs often solve only part of the wider challenge. To reach the full promise of platforms, organizations must think not only about technology components but also about how they package the experience of providing and consuming managed services. Links to all three articles are in the show notes.

### Main Feature: Platform Engineering 2025 Year in Review

**Jordan**: Now onto our main feature. Twenty twenty-five was the year platform engineering grew up and got a reality check. AI entered infrastructure in ways we couldn't ignore. Industry consensus finally emerged on what platforms should actually do. And then Cloudflare went down six times to remind us that concentration risk isn't just theoretical. Today, we're looking back at the ten stories that defined platform engineering in twenty twenty-five.

**Alex**: What a year it's been. We published fifty-eight podcast episodes and thirty-three blog posts covering everything from KubeCon in London and Atlanta to AWS re:Invent. We analyzed critical vulnerabilities, celebrated CNCF graduations, and watched the industry mature in real time. Let's dive into the defining moments.

**Jordan**: We'll start with arguably the biggest shift: AI becoming native to Kubernetes. At KubeCon North America in November, the CNCF launched the Kubernetes AI Conformance Program version one point zero. This wasn't just another certification. It was the industry finally standardizing how AI workloads run on Kubernetes.

**Alex**: The timing was critical. Dynamic Resource Allocation, or DRA, reached general availability in Kubernetes one point thirty-four. DRA fundamentally changes how GPUs and accelerators are managed. Instead of static allocation, workloads can now request specific GPU capabilities dynamically. Eleven vendors certified immediately: Google Cloud, Azure, Oracle, CoreWeave, and AWS among them.

**Jordan**: The numbers tell the story. Teams implementing DRA properly are seeing thirty to forty percent GPU cost savings. That's not incremental. That's transformational for AI infrastructure budgets.

**Alex**: But here's the counterpoint. While Kubernetes standardized AI workloads, AWS re:Invent in December introduced something else entirely: agentic AI for platform engineering. Their DevOps Agent can identify root causes of incidents with eighty-six percent accuracy. GitHub launched Agent HQ for orchestrating multiple AI agents from different providers.

**Jordan**: Werner Vogels coined a term that stuck with me: verification debt. It's like technical debt, but for AI systems. Every autonomous action an agent takes without human verification accumulates verification debt. And here's the sobering reality: eighty percent of companies report that their agents have executed unintended actions. Only forty-four percent have agent-specific security policies.

**Alex**: Gartner predicts forty percent of agentic AI projects will fail by twenty twenty-seven. So while AI infrastructure is standardizing on Kubernetes, the autonomous AI layer above it is still the wild west.

**Jordan**: Let's talk about platform engineering itself. After years of definitional chaos, where everyone had a different opinion on what platform engineering even meant, twenty twenty-five brought consensus.

**Alex**: Three principles emerged across multiple KubeCon talks, industry reports, and practitioner discussions. First: API-first self-service. Platforms must expose capabilities through APIs that developers consume directly, not tickets they submit and wait on. Second: business relevance. Platforms must tie their value to business outcomes, not just technical metrics. Third: the managed service approach. Internal platforms should feel like using a cloud service, not fighting with infrastructure.

**Jordan**: The adoption data from DORA twenty twenty-five is striking. Ninety percent of organizations now have platform initiatives. That's near-universal. But here's the uncomfortable truth: platform teams actually decreased throughput by eight percent and stability by fourteen percent on average.

**Alex**: How is that possible? We covered this in episode forty. The puppy for Christmas anti-pattern. Organizations adopt platforms like a child receives a puppy. Excitement at first, then the realization that it requires constant feeding, training, and attention. Most teams renamed their ops team platform engineering and expected different results.

**Jordan**: The teams that succeed share common characteristics. Optimal size is six to twelve people, following the Spotify squad model. They have dedicated platform leadership at one hundred-plus engineers to shield from competing priorities. And they evolve their interaction model: starting with collaboration while building, then transitioning to X-as-a-Service when mature.

**Alex**: When done right, the numbers are compelling. Eight to ten percent individual productivity boost. Ten percent team productivity boost. But getting there requires treating the platform as a product with actual product management discipline.

**Jordan**: Let's shift to the stories nobody wanted but everyone learned from. Twenty twenty-five will be remembered as the year infrastructure concentration risk became undeniable.

**Alex**: October nineteenth. AWS US-EAST-1 went down. Not partially. Not briefly. For over fourteen hours, seventy-plus AWS services were degraded or unavailable. The root cause? A DNS race condition in DynamoDB. The impact? Six point five million downtime reports globally. Cost estimates ranged to seventy-five million dollars per hour.

**Jordan**: Then came Cloudflare. Not once. Not twice. Six major outages in twenty twenty-five. On November eighteenth, a Rust panic in their proxy code took down twenty percent of the internet for six hours. ChatGPT, X, Shopify, Discord, Spotify. All affected. Then on December fifth, just three weeks later, twenty-eight percent of HTTP traffic impacted for twenty-five minutes.

**Alex**: The pattern is clear. The organizations we depend on are single points of failure for massive portions of the internet. Multi-region, multi-cloud, multi-CDN strategies aren't paranoid overengineering. They're risk management.

**Jordan**: And then there was IngressNightmare. CVE twenty twenty-five dash nineteen seventy-four. Disclosed March twenty-fourth with a CVSS score of nine point eight. Unauthenticated remote code execution in ingress-nginx. Forty-three percent of cloud environments were vulnerable. Sixty-five hundred clusters exposed, including Fortune five hundred companies.

**Alex**: The response was equally dramatic. Ingress NGINX announced retirement with a March twenty twenty-six deadline. Only one or two maintainers remained. No security patches after the deadline. Platform teams now have a hard migration deadline to Gateway API.

**Jordan**: Speaking of maintainers, let's talk about the open source sustainability crisis that twenty twenty-five made visible.

**Alex**: The CNCF celebrated its tenth birthday at KubeCon Europe in London. Three hundred thousand contributors. Hundreds of projects. Incredible growth. But behind those numbers: sixty percent of maintainers are unpaid. Sixty percent have left or are considering leaving.

**Jordan**: The XZ Utils backdoor from late twenty twenty-four cast a long shadow over twenty twenty-five. A lone maintainer, burned out, unknowingly merged malicious code. It reminded the entire industry that our infrastructure depends on volunteers who often receive no compensation.

**Alex**: At KubeCon Atlanta, there was a memorial for Han Kang, the in-toto project lead. It was a sobering moment. These aren't anonymous contributors. They're people with lives, families, and limits.

**Jordan**: The industry is responding. CNCF invested over three million dollars in security audits, tooling, and frameworks. The Open Source Pledge is gaining traction, recommending two thousand dollars per developer per year to fund the projects you depend on. If your company runs on Kubernetes and doesn't contribute financially to open source, twenty twenty-five should be your wake-up call.

**Alex**: Let's talk about the tools and projects that shaped twenty twenty-five. Infrastructure as Code saw major consolidation.

**Jordan**: IBM acquired HashiCorp for six point four billion dollars. The Terraform versus OpenTofu debate that dominated twenty twenty-four reached a resolution of sorts. OpenTofu achieved feature parity in July and crossed ten million downloads. For teams committed to open source, the path is clear.

**Alex**: The surprise was CDKTF. HashiCorp deprecated it after five years, effectively conceding the CDK war to Pulumi. If you're using CDKTF, your migration timeline just accelerated.

**Jordan**: Helm four released at KubeCon Atlanta. First major version in six years. WebAssembly plugins for portability. Server-Side Apply replacing three-way merge. Forty to sixty percent faster deployments for large releases. If you're still on Helm three, you have a twelve-month support runway until November twenty twenty-six.

**Alex**: ArgoCD three point zero went GA in May. Fine-grained RBAC, security improvements, better scaling characteristics. And Gateway API one point four reached general availability in October, cementing its position as the successor to Ingress.

**Jordan**: Three CNCF graduations deserve recognition. Crossplane in November, with seventy-plus adopters including Nike, NASA, and SAP. Knative in October, maturing the serverless event-driven model. And CubeFS in January, proving distributed storage at three hundred fifty petabytes scale.

**Alex**: Now let's talk economics. GPU waste became impossible to ignore in twenty twenty-five.

**Jordan**: The average H100 GPU runs at thirteen percent utilization. Think about that. An H100 costs roughly three dollars per hour on cloud. At thirteen percent utilization, you're wasting four thousand three hundred fifty dollars per month per GPU.

**Alex**: Across the industry, sixty to seventy percent of GPU budgets are wasted. We covered a case study in episode thirty-four where a team went from twenty H100s to seven H100s. That's a sixty-five percent reduction. Thirty-five thousand dollars monthly savings. Same workloads.

**Jordan**: DRA, time-slicing, MIG partitioning, spot instances, regional arbitrage. These aren't advanced techniques anymore. They're mandatory knowledge for anyone managing AI infrastructure.

**Alex**: Service mesh saw its own efficiency revolution. Istio Ambient mode reached general availability, and the benchmarks are striking. Ninety percent memory reduction. Fifty percent CPU reduction compared to sidecar architecture.

**Jordan**: Seventy percent of organizations now run service mesh. The sidecar era is ending. We benchmarked Istio Ambient against Cilium in episode thirty-three. Eight percent mTLS overhead for Ambient versus ninety-nine percent for Cilium. At two thousand pods, that translates to one hundred eighty-six thousand dollars annual savings.

**Alex**: eBPF continues its march. Cilium, Tetragon, and the entire eBPF ecosystem are becoming the default for networking, security, and observability. The kernel-native approach is winning.

**Jordan**: So what's coming in twenty twenty-six? Let me give you the hard deadlines first.

**Alex**: March twenty twenty-six: Ingress NGINX retires. No more security patches. If you haven't migrated to Gateway API, your clusters are vulnerable.

**Jordan**: Agentic AI adoption will accelerate, but verification debt will become a real problem. The companies that figure out agent governance early will have significant advantages. The ones that don't will join Gartner's forty percent failure prediction.

**Alex**: Platform teams at enterprise scale will face new challenges. Episode fifty-eight covered Okta's journey from twelve to one thousand clusters. The lessons about ArgoCD scaling, sharding, and hub-spoke architectures will become relevant to more organizations.

**Jordan**: The CNPE certification, CNCF's new platform engineer credential, will create a professionalization wave. Twenty twenty-six might be the year platform engineering gets its CKA equivalent.

**Alex**: Multi-cluster management becomes standard, not exceptional. SBOM requirements become federal mandate for many vendors. And Kubernetes continues its rapid innovation with one point thirty-five and beyond.

**Jordan**: Let me close with my top five takeaways from twenty twenty-five.

First: AI infrastructure is now standardized. The Kubernetes AI Conformance Program means vendor lock-in is optional if you architect correctly.

Second: Platform engineering has a definition. API-first self-service, business relevance, managed service approach. Use it.

Third: Concentration risk is real. Multi-region, multi-cloud, multi-CDN isn't paranoia. It's risk management.

Fourth: Open source needs funding. If you depend on it, pay for it. Two thousand dollars per developer per year is the recommendation.

Fifth: GPU waste is the new cloud waste. Thirteen percent utilization is unacceptable. DRA and time-slicing are table stakes.

**Alex**: And my action items for twenty twenty-six.

Migrate to Gateway API before March. Ingress NGINX is retiring and you don't want to rush.

Implement DRA for AI workloads. Thirty to forty percent cost savings are achievable.

Audit your agent policies. If you're in the fifty-six percent without them, you're accepting significant risk.

Review your Cloudflare and AWS dependencies. Twenty twenty-five proved that these providers can fail dramatically.

And sponsor an open source project. The CNCF, Apache, and Linux Foundation all accept contributions. Pick a project you depend on and fund it.

**Jordan**: Twenty twenty-five was the year platform engineering grew up. AI arrived in ways we're still processing. Consensus emerged on what platforms should actually do. And reality tested our assumptions about reliability and sustainability. The infrastructure you build in twenty twenty-six should reflect these lessons.

**Alex**: The fundamentals remain constant: reliability, security, cost efficiency. But the tools, patterns, and threats keep evolving. Stay curious, stay critical, and we'll see you in twenty twenty-six.

---

## Related Episodes

- [Episode #035-037: KubeCon Atlanta 2025 Coverage](/podcasts/00035-kubecon-2025-ai-native)
- [Episode #049-052: AWS re:Invent 2025 Series](/podcasts/00049-aws-reinvent-2025-agentic-ai-revolution)
- [Episode #030: Cloudflare November Outage](/podcasts/00030-cloudflare-outage-november-2025)
- [Episode #047: Cloudflare December Outage](/podcasts/00047-cloudflare-december-2025-outage-trust-crisis)
- [Episode #007: AWS US-EAST-1 Outage](/podcasts/00007-aws-us-east-1-outage)
- [Episode #057: Platform Team Structures](/podcasts/00057-platform-engineering-team-structures)
- [Episode #058: Okta GitOps Journey](/podcasts/00058-okta-gitops-argocd-1000-clusters)
- [Episode #040: Platform Engineering Anti-Patterns](/podcasts/00040-platform-engineering-anti-patterns)
- [Episode #034: GPU Waste and FinOps](/podcasts/00034-kubernetes-gpu-cost-waste-finops)
- [Episode #033: Service Mesh Showdown](/podcasts/00033-service-mesh-showdown-cilium-istio-ambient)

---

## Sources

- [DORA 2024/2025 Reports](https://dora.dev/)
- [CNCF Annual Survey](https://www.cncf.io/reports/)
- [State of Platform Engineering 2025](https://platformengineering.org/)
- [KubeCon + CloudNativeCon 2025](https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/)
- [AWS re:Invent 2025](https://reinvent.awsevents.com/)
- [Kubernetes AI Conformance Program](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program/)
- [CVE-2025-1974 IngressNightmare](https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities)
- [Helm 4.0 Release](https://helm.sh/blog/helm-4-released/)
- [Gateway API v1.4](https://gateway-api.sigs.k8s.io/)

---

## Listen & Watch

- **YouTube**: [Watch on YouTube](https://youtu.be/PLACEHOLDER)
- **Podcast Feed**: RSS feed coming soon
