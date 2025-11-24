---
title: "KubeCon Atlanta 2025: The Year Kubernetes Became an AI-Native Platform"
description: "DRA goes GA, Workload API arrives, 30K cores freed with one line, and platform engineering reaches consensus. Complete KubeCon 2025 recap with 10 major announcements."
keywords:
  - KubeCon 2025
  - Kubernetes AI workloads
  - Dynamic Resource Allocation
  - Workload API
  - platform engineering
  - Kubernetes rollback
  - EU Cyber Resilience Act
  - GPU scheduling
  - CNCF
  - cloud native
  - container orchestration
  - AI infrastructure
datePublished: "2025-11-24"
dateModified: "2025-11-24"
schema:
  type: FAQPage
  questions:
    - question: "What were the biggest announcements at KubeCon Atlanta 2025?"
      answer: "Dynamic Resource Allocation (DRA) reached GA in Kubernetes 1.34, Workload API introduced in alpha for 1.35, Kubernetes rollback achieved 99.99% success rate after 10 years, and platform engineering reached industry consensus on three core principles."
    - question: "How does Dynamic Resource Allocation improve GPU workloads?"
      answer: "DRA enables fine-grained, topology-aware resource allocation preventing 10-40% performance degradation from CPU/GPU misalignment on NUMA systems. It replaces device plugins with a more flexible architecture for AI/ML workloads."
    - question: "What is the Kubernetes Workload API?"
      answer: "Workload API allows Kubernetes to understand groups of pods as a single unit, enabling all-or-nothing gang scheduling essential for large-scale AI training jobs spanning thousands of GPUs across multiple nodes. It's in alpha for Kubernetes 1.35."
    - question: "What did OpenAI's 30,000 core optimization teach platform engineers?"
      answer: "OpenAI freed 30,000 CPU cores by disabling inotify in Fluent Bit after profiling revealed fstat64 consuming 35% of CPU time while processing 10 petabytes of logs daily. The lesson: always profile critical path services."
    - question: "What are the three core principles of platform engineering from KubeCon 2025?"
      answer: "API-first self-service, business relevance (not just technology for technology), and managed service approach. The anti-pattern to avoid is the 'puppy for Christmas' problem—templates without ongoing support."
    - question: "What does the EU Cyber Resilience Act mean for open source maintainers?"
      answer: "Individual contributors are NOT liable under CRA. Maintainers need to provide a security contact and report vulnerabilities when fixed. Full compliance required by December 2027, but manufacturers bear primary responsibility."
    - question: "How did Kubernetes achieve 99.99% upgrade reliability?"
      answer: "After 10 years of work, Kubernetes now supports safe rollback and skip-version upgrades across GKE control planes and nodes. 97% of GKE fleet runs on the most recent 3 Kubernetes versions."
    - question: "What real-world AI infrastructure scale was demonstrated at KubeCon 2025?"
      answer: "OpenAI processes 10 petabytes of logs daily, ByteDance's AI Brix manages thousands of AI accelerators, Pokémon Go handles trillions of scheduling possibilities for geo-temporal ML, and pre-training workloads use every accelerator customers can acquire running for days or weeks."
    - question: "What is CPU DRA and why does it matter?"
      answer: "CPU DRA driver enables topology-aware CPU scheduling, preventing 30-40% performance degradation in HPC workloads. It makes Kubernetes + Slurm integration viable for high-performance computing use cases requiring NUMA alignment."
    - question: "What challenges did the Kubernetes Steering Committee discuss?"
      answer: "Maintainer burnout ('the reward for good work is more work'), difficulty recruiting diverse contributors despite desire, concerns about CNCF having too many projects (200+), and need for better institutional support for leadership roles."
---

November 2025 marks 10 years since the Cloud Native Computing Foundation was born. In 2015, Kubernetes was a radical bet—Google's internal container orchestrator released to the world. Today, it's foundational infrastructure powering everything from Netflix to the International Space Station.

But KubeCon + CloudNativeCon Atlanta 2025 wasn't a victory lap. It was a watershed moment. Dynamic Resource Allocation hit GA. Workload API arrived. OpenAI showed how one line of code freed 30,000 CPU cores. And after a decade of effort, Kubernetes rollback finally works.

The theme? Kubernetes isn't just for microservices anymore. It's an AI-native platform. And the community is grappling with what that means for complexity, maintainability, and the next 10 years.

Here's everything that matters from 49 sessions across 3 days in Atlanta.

> 🎙️ **Listen to the podcast series**: [Part 1: AI Goes Native and the 30K Core Lesson](/podcasts/00035-kubecon-2025-ai-native) - DRA goes GA, CPU DRA for HPC, Workload API, OpenAI's 30K core optimization, and Kubernetes rollback after 10 years (19 min). Part 2 and 3 coming soon covering platform engineering consensus and community sustainability.

## Quick Answer

**Context**: Kubernetes turning 10 years old raises questions about maturity, complexity, and future direction amid explosive AI/ML workload growth.

**Major Developments**: KubeCon Atlanta 2025 showcased production-ready AI infrastructure, platform engineering consensus, and hard-won operational reliability.

**Key Statistics**:
- Dynamic Resource Allocation (DRA) reached GA in Kubernetes 1.34 for production GPU workloads
- Workload API introduced in alpha (1.35) for gang-scheduling multi-pod AI training jobs
- OpenAI freed 30,000 CPU cores with single-line optimization while processing 10PB/day of logs
- Kubernetes rollback achieved 99.99% upgrade success rate after 10 years of development
- 10-40% performance degradation occurs from CPU/GPU misalignment without topology-aware scheduling
- Platform engineering reached industry consensus on three non-negotiable principles
- ByteDance's AI Brix now has 80% external contributors after open sourcing

**Success Pattern**: AI workloads are first-class citizens, operational reliability is table stakes, platform engineering has clear principles, community health requires active investment.

**When NOT to use Kubernetes for AI**: If you don't need multi-node training (single-GPU workloads), lack operational maturity for complex orchestration, or have workloads requiring `<10ms` scheduling latency.

## Key Statistics (KubeCon 2025 Data)

| Metric | Value | Source | Context |
|--------|-------|--------|---------|
| DRA Status | GA in Kubernetes 1.34 | [Kubernetes Network Driver Keynote](https://www.youtube.com/watch?v=1iFYEWx2zC8) | Production-ready for GPU topology awareness |
| Workload API | Alpha in Kubernetes 1.35 | [Multi-host Training Session](https://www.youtube.com/watch?v=RMJYCT31yp4) | Enables gang-scheduling for AI |
| OpenAI CPU Savings | 30,000 cores freed | [Fluent Bit Optimization Keynote](https://www.youtube.com/watch?v=pbOvWxuYPIU) | Single-line code change (disable inotify) |
| OpenAI Log Volume | 10 petabytes/day | [Fluent Bit Optimization Keynote](https://www.youtube.com/watch?v=pbOvWxuYPIU) | Scale of observability infrastructure |
| Performance Impact | 10-40% degradation | [Topology-aware CPU Scheduling](https://www.youtube.com/watch?v=1JO_73pVrLI) | From CPU/GPU misalignment on NUMA |
| Kubernetes Dependencies | 250 (down from 416) | [Dependency Tree Management](https://www.youtube.com/watch?v=3mDu39-LUVg) | 3-year effort to prune |
| Upgrade Success Rate | 99.99% | [Google Accelerating Innovation](https://www.youtube.com/watch?v=lcGvEhDqt8s) | GKE control planes + nodes |
| GKE Version Currency | 97% on recent 3 versions | [Google Accelerating Innovation](https://www.youtube.com/watch?v=lcGvEhDqt8s) | Result of safe rollback capability |
| ByteDance AI Brix Stars | 4,000+ GitHub stars | [Turn Up the Heat Keynote](https://www.youtube.com/watch?v=7KHenRXNGAw) | Since early 2025 open source release |
| ByteDance Contributors | 80% external | [Turn Up the Heat Keynote](https://www.youtube.com/watch?v=7KHenRXNGAw) | After open sourcing internal platform |
| CNCF Projects | 200+ (70 graduated) | [Back to the Future Keynote](https://www.youtube.com/watch?v=GQtaggMzom4) | 10-year growth from 2015 |
| Pokémon Go Scheduling | Trillions of possibilities | [Geo-temporal ML Keynote](https://www.youtube.com/watch?v=NbfyR_tNMXY) | Millions gyms × raid tiers × time |

## The AI-Native Era Arrives

Google's live donation of the DRA-Net driver during a keynote marked a symbolic shift—Kubernetes isn't adapting to AI workloads anymore. It's being rebuilt for them.

### Dynamic Resource Allocation Goes GA

After years in development, Dynamic Resource Allocation (DRA) reached General Availability in Kubernetes 1.34. This isn't just another feature release. It's a fundamental architectural change in how Kubernetes allocates resources.

The problem DRA solves is subtle but expensive. Modern AI workloads require tight coupling between CPUs, GPUs, and memory on NUMA (Non-Uniform Memory Access) systems. When Kubernetes schedules a pod requesting a GPU, the old device plugin architecture might allocate a GPU on one NUMA node but CPUs on another. The performance impact? 10-40% degradation.

"HPC workloads can see 30-40% performance differences on misaligned versus aligned resources," explained Tim Wickberg, CTO of SchedMD (the company behind Slurm, the dominant HPC scheduler). "This 10% latency statistic is a very high level stat for what can happen."

Let's do the math. A pre-training workload on misaligned GPUs consuming $5,000 per day in cloud costs with 40% waste equals $2,000 per day per node thrown away. Scale that to 100 nodes and you're burning $200,000 daily on preventable performance loss.

DRA replaces the rigid device plugin model with a flexible resource allocation system. It understands topology, enables fine-grained scheduling, and allows resource drivers to participate in the scheduling process. The DRA-Net driver donated by Google during the keynote extends this capability to network resources, enabling bandwidth-aware scheduling for distributed training.

> **💡 Key Takeaway**
>
> Dynamic Resource Allocation in Kubernetes 1.34 GA status means GPU topology awareness is production-ready. If running AI/ML workloads on Kubernetes without DRA, you're likely losing 10-40% of purchased compute capacity to NUMA misalignment. Migration from device plugins to DRA should begin in Q1 2025 for organizations with 20+ GPUs.

### Workload API Solves Gang-Scheduling

The Workload API, arriving in alpha for Kubernetes 1.35, addresses one of the most painful operational challenges in large-scale AI training: partial scheduling failures.

Here's the scenario: You submit a 1,000-pod distributed training job. The Kubernetes scheduler, treating each pod independently, successfully schedules 800 pods. But resources for the remaining 200 pods never materialize. Those 800 running pods sit idle, consuming GPU time worth thousands of dollars per hour, waiting for workers that will never arrive.

The Workload API introduces the concept of workload-level scheduling. Kubernetes now understands that certain groups of pods must be scheduled atomically—all or nothing. If the cluster can't accommodate the entire workload, none of it starts. This prevents resource waste from partial failures.

"Pre-training workloads use every accelerator the customer can acquire," explained Eric Tune from Google during a technical session on multi-host training. "Hardware failures happen every couple of days. The time to recover and restart is a significant reduction in cost."

The Workload API integrates with projects like Kueue to provide sophisticated job queuing, preemption policies, and resource quotas across multiple teams sharing a cluster. For organizations running large-scale AI infrastructure, this is transformative.

> **💡 Key Takeaway**
>
> Workload API (alpha in Kubernetes 1.35) is the missing piece for large-scale AI training. Organizations running multi-node training jobs should pilot Workload API in development clusters Q1 2025, plan production adoption by Q3 2025 when it reaches beta. This eliminates partial scheduling failures that waste thousands of dollars in GPU time.

### Real-World AI Scale Numbers

The conference showcased AI infrastructure at a scale that's hard to comprehend:

**OpenAI** processes 10 petabytes of logs daily across their Kubernetes fleet. When they profiled Fluent Bit (their log collector), they discovered fstat64 system calls consuming 35% of CPU time due to inotify watching log files unnecessarily. Disabling inotify freed 30,000 CPU cores—equivalent to a 50% reduction in observability infrastructure costs.

**ByteDance** open sourced AI Brix, their internal AI infrastructure platform, in early 2025. It now manages thousands of AI accelerators in production and has attracted 4,000+ GitHub stars. More impressively, 80% of contributors are now external to ByteDance. "This is the spirit of open collaboration—a diverse global effort to build the foundation of cloud-native AI," said Lee Guang from ByteDance's infrastructure team.

**Pokémon Go** revealed the complexity of their geo-temporal ML scheduling system. With millions of gyms worldwide, 7+ raid difficulty tiers, and decisions made every second, they handle trillions of scheduling possibilities. Their stack: Kubeflow, Ray, PyTorch, running entirely on Kubernetes.

**Airbnb** shared that the majority of their developers now use agentic coding tools in their workflow. This wasn't a side comment—it was presented as a fundamental shift in how platform engineering teams think about developer productivity.

These aren't demos or proofs-of-concept. These are production systems at scale, running on Kubernetes, serving millions of users.

> **💡 Key Takeaway**
>
> AI workloads are no longer experimental edge cases. OpenAI processes 10 petabytes daily, ByteDance manages thousands of accelerators, Pokémon Go handles trillions of ML scheduling decisions. If your platform roadmap doesn't include DRA, Workload API, and topology-aware scheduling, you're planning for yesterday's workloads.

## Platform Engineering Reaches Consensus

After years of definitional debates—"What is platform engineering?" "How is it different from DevOps?" "Is it just rebranded SRE?"—KubeCon 2025 delivered clarity.

### The Three Platform Principles

Multiple sessions across different tracks converged on three non-negotiable principles for platform engineering:

**1. API-First Self-Service**

Not ticket-driven workflows. Not ClickOps through web UIs. Not "ask the platform team" interactions. Every capability must be programmatically accessible. If a developer can't automate it, it's not self-service.

**2. Business Relevance**

Platform teams don't build technology for technology's sake. The platform exists to solve actual business problems, measured in business metrics. Revenue per engineer. Time to market. Customer satisfaction. Not just infrastructure metrics like uptime or CPU utilization.

**3. Managed Service Approach**

This is where most platform initiatives fail. You can't throw templates over the wall and call it a platform. True platform engineering means ongoing operational support, SLAs, and taking responsibility for the services you provide.

"Platform engineering is your specialized internal economy of scale," explained Abby Bangser during a keynote on platform principles. "It's what's unique to your business but common to your teams."

The CNCF formalized this with a new Platform Engineering TCG (Technical Community Group), complete with a dedicated booth at the Project Pavilion. The industry is aligning.

### The "Puppy for Christmas" Anti-Pattern

The conference introduced a memorable metaphor for platform failure: the "puppy for Christmas" problem.

Imagine giving someone a puppy as a gift. Initial excitement, lots of photos, everyone's happy. Two weeks later, the reality sets in. The puppy needs feeding, vet visits, training, cleanup. The recipient wasn't ready for the ongoing operational burden.

Platform teams do this constantly. They create a Helm chart, publish it to an internal catalog, and declare victory. "We've enabled self-service!" Six months later, the template is out of date. Dependencies have CVEs. Best practices have evolved. Teams using the template are on their own.

The solution? An internal marketplace model inspired by app stores. When you publish a capability to the platform catalog, you commit to:
- **Operational support**: Monitoring, incident response, patches
- **Documentation**: Up-to-date guides, examples, troubleshooting
- **SLAs**: Defined uptime, performance, support response times
- **Lifecycle management**: Deprecation notices, migration paths, retirement

"We have a 'done for you' approach at Intuit," explained Mora Kelly, Director of Engineering. "If all services have to have certain things, build it in, make it part of the platform. Do it for your developers."

> **💡 Key Takeaway**
>
> Platform engineering consensus emerged at KubeCon 2025 around three principles: API-first self-service, business relevance, and managed service approach. The anti-pattern to avoid is "puppy for Christmas"—templates without ongoing support. If your platform team provides Helm charts but no operational support, you're creating technical debt, not enabling productivity.

### Real-World Adoption at Scale

The conference featured multiple case studies of platform engineering at significant scale:

**Intuit** is migrating Mailchimp—a 20-year-old monolith serving 11 million users sending 700 million emails per day—onto their developer platform. The remarkable part? "Most developers didn't even notice it was happening." This is platform engineering maturity. Invisible infrastructure changes, zero disruption to product delivery.

**Bloomberg** has run Kubernetes since version 1.3 in 2016. That's nine years of production Kubernetes experience. They created Kserve (formerly KFServing) for model inference, which is now a CNCF incubating project. Their platform team operates thousands of Kubernetes nodes across private and public clouds.

**ByteDance** took the bold step of open sourcing AI Brix, their internal AI infrastructure platform. The result? 80% of contributors are now external to ByteDance. This demonstrates a mature understanding that platform engineering benefits from community collaboration, not proprietary lock-in.

**Airbnb** shared their migration journey from a monolith to microservices using Argo Rollouts for blue-green deployments. More interesting: they're already preparing for the next shift, with most developers using agentic coding tools that will reshape platform requirements.

> **💡 Key Takeaway**
>
> Successful platform engineering requires years of investment and operational maturity. Bloomberg has run Kubernetes since 2016, Intuit migrated an 11-million-user monolith transparently, ByteDance open sourced their internal platform and achieved 80% external contributors. Platform teams expecting results in 6-12 months are setting themselves up for failure.

## Operational Excellence and Performance Wins

The most impactful announcement at KubeCon 2025 wasn't a flashy new feature. It was Kubernetes rollback finally working after 10 years of development.

### Kubernetes Rollback After 10 Years

The announcement came during Google's "Accelerating Innovation" keynote. JG Macleod, Google's Open Source Kubernetes Lead, shared a bittersweet milestone: Kubernetes upgrades now achieve a 99.99% success rate across GKE control planes and nodes, with support for safe rollback and skip-version upgrades.

The timeline is sobering. Kubernetes 1.0 launched in July 2015. For 10 years, cluster upgrades were one-way operations. If an upgrade went wrong, you couldn't roll back—you could only attempt to upgrade further forward to a fixed version. This fundamental limitation prevented many organizations from keeping clusters current.

The breakthrough enables skip-version upgrades. You can now safely upgrade once a year instead of quarterly, reducing operational burden by 75%. GKE's fleet statistics prove it works: 97% of clusters run on one of the three most recent Kubernetes versions.

The announcement included a memorial to Han Kang, who passed away in 2025 and worked extensively on Kubernetes reliability. "This has taken literally a decade of effort...roll back is really here," Macleod said. "When you join this community, you really do join a family. Han Kang's passing really hurts. This [Kubernetes rollback] is a lasting legacy."

> **💡 Key Takeaway**
>
> Kubernetes rollback achieving 99.99% success rate after 10 years of development removes the primary operational barrier to cluster upgrades. GKE's skip-version upgrade capability means organizations can upgrade annually instead of quarterly, reducing operational burden by 75%. Platform teams should pilot skip-version upgrades in non-production clusters Q1 2025.

### The 30,000 Core Lesson

Fabian Ponce from OpenAI's Applied Observability Team delivered one of the conference's most practical sessions: how a single line of code freed 30,000 CPU cores.

The context: OpenAI processes approximately 10 petabytes of logs per day across their Kubernetes fleet using Fluent Bit as the log collector. They noticed Fluent Bit consuming unexpectedly high CPU across the fleet.

The investigation process was textbook:

1. **Observe**: High CPU usage in Fluent Bit processes
2. **Profile**: Use `perf` to identify hot code paths
3. **Analyze**: fstat64 system call consuming 35% of CPU time
4. **Root cause**: inotify watching log files for changes (unnecessary in their architecture)
5. **Fix**: Disable inotify in Fluent Bit configuration
6. **Result**: 50% CPU reduction while processing the same volume

At cloud pricing of approximately $0.10 per core-hour, 30,000 cores × 24 hours × 30 days = $2.16 million per month saved. From one configuration change.

"Sometimes you might just find something surprising," Ponce said with understatement. OpenAI open sourced their findings and is working with the Fluent Bit maintainers on an upstream patch.

The lesson isn't about inotify specifically. It's about profiling. How many platform teams have continuous profiling in place? How many regularly use `perf`, eBPF, or similar tools to understand their critical path services?

> **💡 Key Takeaway**
>
> OpenAI's 30,000 core savings from one line demonstrates profiling's ROI. At $0.10/core-hour, 30K cores × 24 hours × 30 days = $2.16M/month saved. Every platform team should instrument critical path services with perf, eBPF, or continuous profiling. The low-hanging fruit exists—you just need to measure to find it.

### CPU DRA Driver Enables HPC Workloads

While GPU DRA received most attention, the CPU DRA driver is equally transformative for high-performance computing workloads.

The session on topology-aware CPU scheduling featured Tim Wickberg, CTO of SchedMD (the company maintaining Slurm, the dominant HPC scheduler). His presence at a Kubernetes conference signals a major shift: Kubernetes and traditional HPC are converging.

The technical challenge: HPC workloads demand precise control over CPU placement relative to memory and network interfaces. Misalignment between CPUs and memory on NUMA systems causes 30-40% performance degradation in computational fluid dynamics, molecular dynamics, and financial modeling workloads.

The CPU DRA driver provides this topology awareness, making Kubernetes viable for workloads previously requiring Slurm or other HPC schedulers. Several organizations demonstrated Kubernetes + Slurm integration, using Kubernetes for orchestration and Slurm for fine-grained job scheduling within workloads.

This expands Kubernetes beyond web services and AI/ML into scientific computing, weather modeling, drug discovery, and other domains where performance optimization at the hardware level is critical.

> **💡 Key Takeaway**
>
> CPU DRA driver expands Kubernetes beyond AI/ML into high-performance computing. Organizations running scientific computing, computational fluid dynamics, or financial modeling workloads can achieve 30-40% performance gains through NUMA-aware scheduling. This bridges the gap between Kubernetes and traditional HPC schedulers like Slurm.

## Community Health and Future Direction

The Kubernetes Steering Committee held an "Ask the Experts" session that demonstrated both the community's maturity and its challenges.

### Diversity Achievements and Maintainer Burnout

The Steering Committee announced a milestone: for the first time, the committee composition reflects the community's diversity. New members include Cat Cosgrove (Kubernetes 1.30 release lead), Rita Zhang from Microsoft, and others representing various backgrounds and companies.

But the discussion quickly turned to harder topics. Maintainer burnout. Difficulty recruiting contributors, especially from underrepresented groups. The unsustainable workload on core maintainers.

One committee member articulated a systemic problem: "The reward for good work is more work. If you're good at your work, you get even more work assigned."

Cat Cosgrove, newly elected to the Steering Committee, was remarkably honest: "I'm ready to abandon ship. Like, it's so much work."

This isn't complaining. It's a structural issue. Kubernetes governance includes multiple Special Interest Groups (SIGs), working groups, and committees. The work is valuable but endless. The community is grappling with how to sustain leadership without burning out the people willing to step up.

An audience member raised a provocative question: "There's not enough people stepping up...but maybe do we need to look at is there just too much landscape?" The comparison to OpenStack's "big tent" problem was implicit. CNCF now has over 200 projects. Is that sustainable?

The committee didn't have easy answers, but they acknowledged the challenges openly. The discussion focused on:
- **Time-boxed initiatives**: Projects with defined endpoints instead of endless maintenance
- **Better institutional support**: Companies giving employees dedicated time for community work
- **Succession planning**: Explicit mentoring and transition paths
- **Saying no**: Not every feature request needs to be accepted

### EU Cyber Resilience Act Demystified

Greg Kroah-Hartman, a Linux kernel developer, delivered a comprehensive explainer on the EU Cyber Resilience Act (CRA) that addressed widespread concerns in the open source community.

**Key message**: Individual contributors are NOT liable under the CRA.

The law targets manufacturers—companies selling products or services incorporating open source software. If you contribute to Kubernetes, Linux, or any open source project, you don't have new legal obligations.

For open source foundations and project maintainers (stewards in CRA terminology), the requirements are reasonable:
1. **Provide a security contact**: An email address or form for security researchers
2. **Report vulnerabilities when fixed**: Notify a designated EU database
3. **Generate SBOMs**: Provide a Software Bill of Materials listing dependencies

The timeline provides plenty of preparation time:
- **September 2026**: Enforcement begins for manufacturers
- **December 2027**: Full compliance required for open source stewards

Kroah-Hartman emphasized that manufacturers cannot push unreasonable compliance work downstream to open source projects. If they try, the Open Source Security Foundation (OSSF) will provide form letters for maintainers to push back.

"If you're contributing to an open source project, you do not have to worry about it. It's not an issue," Kroah-Hartman explained. "As a steward [foundation/nonprofit], you only have to do two things: provide a contact for security issues, and when you fix them, report it to somebody."

His overall assessment: "The CRA is just a list of ingredients. That's it. A list of software that is in a device or product...This is a good thing. Open source is going to succeed even better."

> **💡 Key Takeaway**
>
> EU Cyber Resilience Act requires security contacts and vulnerability reporting from open source maintainers by December 2027, but individual contributors are explicitly protected from liability. Platform teams should begin SBOM generation now (most tooling already exists), establish security contact processes, and push back on manufacturers demanding excessive compliance work (OSSF will provide form letters).

### Kubernetes Dependency Management Lessons

Jordan Liggitt and Davanum Srinivas (both Kubernetes maintainers) gave a session on managing Kubernetes's dependency tree—a masterclass in technical debt reduction.

The problem: Kubernetes currently has over 250 dependencies and more than 1 million lines of vendored code. "Believe it or not, this is a dramatic improvement from where we were a few years ago," Liggitt said. In 2023, Kubernetes had 416 dependencies.

Reducing from 416 to 247 dependencies took three years of sustained effort, guided by a philosophy they called "Patient. Pragmatic. Persistent."

**Patient**: Work upstream to fix root causes instead of patching locally. This takes longer initially but prevents recurring problems.

**Pragmatic**: Accept that some dependencies are necessary. Focus effort on the most problematic ones.

**Persistent**: Dependency management never ends. Constant vigilance prevents backsliding.

The session highlighted several tools:
- **depth-stat**: Analyzes dependency trees to identify problematic transitive dependencies
- **go mod vendor**: Provides visibility into what's actually being pulled in
- **Automated CI**: Alerts when new dependencies are added, forcing explicit review

One example: Kubernetes had a tangled mess of dependencies on Google's genproto libraries. Untangling this took years of coordination with multiple teams at Google and in the broader Go ecosystem. But once resolved, it eliminated recurring version conflicts and security vulnerabilities.

"Your dependencies' problems become your problems," Liggitt emphasized. Every dependency adds maintenance burden, potential security issues, and upgrade complexity.

> **💡 Key Takeaway**
>
> Kubernetes reduced dependencies from 416 to 247 through 3-year sustained effort, proving dependency management requires long-term commitment. Platform teams should audit dependency trees quarterly, implement automated alerts for new dependencies in CI, and work upstream to fix root causes rather than patching locally. Your dependencies' problems become your operational burden.

## What This Means for Platform Engineers

The announcements at KubeCon 2025 have immediate and strategic implications for platform engineering teams.

### Immediate Action Items (Q1 2025)

**1. Test Kubernetes 1.34 with DRA in Development**

If you run GPU workloads, Dynamic Resource Allocation is production-ready. Set up a development cluster with Kubernetes 1.34, enable DRA, and measure performance improvement from topology-aware scheduling. If you see 10%+ improvement (likely 10-40% based on workload characteristics), plan production migration for Q2 2025.

**2. Profile Your Critical Path Services**

OpenAI's 30,000 core savings demonstrates that low-hanging fruit exists in production systems. Use `perf`, eBPF-based tools like Parca or Pyroscope, or commercial continuous profiling solutions. Target your top 5 CPU-consuming services and identify functions consuming more than 20% of CPU time.

**3. Audit Platform Against Three Principles**

Honestly assess your platform:
- **API-first self-service**: Is everything programmatically accessible, or do developers still file tickets?
- **Business relevance**: Do you measure business metrics (revenue per engineer, time to market) or just infrastructure metrics?
- **Managed service approach**: Do you provide ongoing support and SLAs, or just templates?

Fix one gap per quarter. Platform engineering is a multi-year journey.

**4. Review CRA Compliance Requirements**

You have until December 2027, but start now. Generate SBOMs for critical services using tools like Syft or SPDX generators. Establish a security contact process (security@yourcompany.com). Document your vulnerability reporting workflow. This becomes harder under pressure.

**5. Evaluate Workload API for Multi-Pod Jobs**

If you run AI/ML training jobs or batch processing requiring coordinated pod groups, Workload API (alpha in Kubernetes 1.35) is worth piloting. Wait for beta status (likely Q3 2025) before production deployment, but start experimenting now to understand migration requirements.

### Strategic Considerations (2025-2026)

**AI Workloads Are Standard, Not Edge Cases**

Stop treating AI/ML as special cases requiring custom solutions. DRA, Workload API, and topology awareness should be baseline platform capabilities. If your roadmap doesn't include these, you're planning for yesterday's workloads.

**Topology Awareness Is Mandatory**

The 10-40% performance gap from NUMA misalignment is too large to ignore. Whether GPU workloads (DRA for accelerators) or HPC workloads (CPU DRA driver), topology-aware scheduling is becoming table stakes for performance-sensitive applications.

**Dependency Health Requires Investment**

Follow Kubernetes's example: quarterly dependency audits, upstream fixes instead of local patches, automated detection of new dependencies in CI. Don't wait for a security incident to take dependency management seriously.

**Platform Engineering Has Clear Definition**

The definitional debates are over. Three principles (API-first, business relevance, managed service), one anti-pattern (puppy for Christmas). Industry alignment means you can benchmark against clearer standards.

**Regulatory Landscape Stabilizing**

The EU Cyber Resilience Act sets a precedent. Expect similar requirements globally. SBOM generation, security contacts, and vulnerability reporting will become universal requirements for production systems. Start building these capabilities now.

### Red Flags

**Your platform team if you see these**:
- Providing templates without operational support ("puppy for Christmas")
- No profiling or observability of platform services themselves
- Dependency count increasing quarter-over-quarter without review
- AI/ML workloads treated as special cases requiring one-off solutions
- Upgrade cadence slowing due to fear of failures (rollback capability now exists)

**Your organization if you see these**:
- Platform team expected to deliver transformational results in less than 12 months
- No dedicated time or institutional support for open source maintainers
- Diversity initiatives without addressing burnout and workload sustainability
- Adding CNCF projects to the stack without defined sunset criteria or maintenance plans

### Monday Morning Actions

**This week**:
1. **Schedule dependency audit** (2 hours): Review your top 20 dependencies, identify age and maintenance status
2. **Profile your #1 CPU consumer** (1 hour): Run `perf top` or similar to identify hot code paths
3. **Generate SBOM for flagship service** (1 hour): Use Syft or similar tooling to create initial SBOM

**This month**:
1. **Pilot DRA in development cluster**: If running GPU workloads, test Kubernetes 1.34 with DRA enabled
2. **Self-audit platform against three principles**: API-first, business relevance, managed service—score yourself honestly
3. **Review CRA requirements with legal/security**: Ensure your organization understands obligations and timeline

**This quarter**:
1. **Plan Workload API pilot**: For multi-pod AI training or batch jobs, prepare for Kubernetes 1.35 alpha testing
2. **Implement automated dependency alerts**: Add CI checks that flag new dependencies for review
3. **Establish platform service operational support model**: Define SLAs, on-call rotations, and documentation standards

## Practical Actions This Week

### For Individual Engineers

- **Profile a service you maintain**: Spend 30 minutes with `perf top` or similar tooling. You might find an easy optimization.
- **Generate an SBOM for your microservice**: Use Syft or SPDX tooling to understand your dependencies. CRA compliance starts with visibility.
- **Watch the OpenAI Fluent Bit session**: 11 minutes that could save you thousands of cores.

### For Platform Teams

**This week**:
- Review your top 5 CPU-consuming services and add profiling
- Audit whether your platform provides API-first self-service or ticket-driven workflows
- List all templates/tools you've published without ongoing support ("puppy for Christmas" audit)

**Next month**:
- Set up Kubernetes 1.34 development cluster to test DRA with GPU workloads
- Implement automated dependency alerts in CI/CD pipelines
- Schedule quarterly dependency review meetings with engineering leadership

**This quarter**:
- Define SLAs for platform services and establish support model
- Plan Workload API pilot for multi-pod workloads (alpha in K8s 1.35)
- Establish security contact and vulnerability reporting process for CRA compliance

### For Leadership

**Business case for investment**:

Platform engineering maturity takes 3-5 years (Bloomberg: 9 years on Kubernetes). Organizations expecting 6-12 month ROI will fail.

**Budget ask**:
- **DRA/GPU optimization**: Potential 10-40% performance improvement = $200K-$2M/year savings (depending on GPU spend)
- **Profiling infrastructure**: $50K-$100K for continuous profiling tooling, potential multi-million dollar savings (OpenAI: $2.16M/month from one fix)
- **Platform team expansion**: 2-3 additional engineers to provide managed service support instead of template distribution

**Timeline**:
- Q1 2025: Pilot DRA, implement profiling, begin CRA compliance work
- Q2 2025: Production DRA deployment, dependency management program
- Q3 2025: Workload API pilot (reaches beta), platform SLA program
- Q4 2025: Full platform service model, documented operational support

**Argument**: Kubernetes turned 10 years old in 2025. AI workloads are no longer experimental. Operational maturity (99.99% upgrade success) and topology awareness (DRA) are now table stakes. Investing in platform engineering is investing in the foundation that will power the next decade of product innovation.

## 📚 Learning Resources

### Official Documentation
- [Kubernetes Dynamic Resource Allocation](https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/) - Official DRA documentation
- [Kubernetes Workload API (Kueue)](https://kueue.sigs.k8s.io/) - Job queueing with Workload API support
- [EU Cyber Resilience Act Full Text](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act) - Official CRA documentation

### KubeCon 2025 Sessions (YouTube)
- [Dynamic Resource Allocation & DRA-Net Donation](https://www.youtube.com/watch?v=1iFYEWx2zC8) - Kubernetes Network Driver keynote (12 min)
- [OpenAI's 30K Core Optimization](https://www.youtube.com/watch?v=pbOvWxuYPIU) - Fluent Bit profiling deep dive (11 min)
- [Kubernetes Rollback & Skip-Version Upgrades](https://www.youtube.com/watch?v=lcGvEhDqt8s) - Google innovation keynote (7 min)
- [Platform Engineering Principles](https://www.youtube.com/watch?v=gmAfYEPBYr0) - Abby Bangser on the three principles (20 min)
- [EU CRA for Open Source Maintainers](https://www.youtube.com/watch?v=GSbIp7OxBq4) - Greg Kroah-Hartman explainer (12 min)
- [Kubernetes Steering Committee Q&A](https://www.youtube.com/watch?v=3sRs8paIybM) - Community health discussion (40 min)

### Technical Deep Dives
- [Topology-Aware CPU Scheduling](https://www.youtube.com/watch?v=1JO_73pVrLI) - CPU DRA driver and HPC integration (40 min)
- [Multi-Host AI Training](https://www.youtube.com/watch?v=RMJYCT31yp4) - Workload API use cases (40 min)
- [Kubernetes Dependency Management](https://www.youtube.com/watch?v=3mDu39-LUVg) - Pruning the dependency tree (40 min)
- [Turn Up the Heat: Real-World Adoption](https://www.youtube.com/watch?v=7KHenRXNGAw) - Intuit, Bloomberg, ByteDance case studies (19 min)

### Tools & Platforms
- [Kueue](https://kueue.sigs.k8s.io/) - Kubernetes job queueing implementing Workload API
- [Syft](https://github.com/anchore/syft) - SBOM generation tool for CRA compliance
- [Perf](https://perf.wiki.kernel.org/) - Linux profiling tool used by OpenAI
- [AI Brix](https://github.com/bytedance/aibrix) - ByteDance's open source AI infrastructure (4,000+ stars)
- [Parca](https://www.parca.dev/) - Open source continuous profiling
- [Pyroscope](https://pyroscope.io/) - Open source continuous profiling alternative

### Community Resources
- [CNCF Platform Engineering TCG](https://github.com/cncf/tag-contributor-strategy/tree/main/platforms) - Technical Community Group
- [Platform Engineering Slack](https://platformengineering.org/slack) - Community discussions
- [KubeCon 2025 Full Playlist](https://www.youtube.com/playlist?list=PLj6h78yzYM2PyrvCoOii4rAopBswfz1p7) - All Atlanta sessions
- [CNCF Landscape](https://landscape.cncf.io/) - All 200+ projects visualized

## Related Content

**Podcast Episodes**:
- [Episode #035: KubeCon 2025 Part 1 - AI Goes Native](/podcasts/00035-kubecon-2025-ai-native) - Technical breakthroughs (18 min)
- [Episode #034: The $4,350/Month GPU Waste Problem](/podcasts/00034-kubernetes-gpu-cost-waste-finops) - GPU cost optimization
- [Episode #022: eBPF in Kubernetes](/podcasts/00022-ebpf-kubernetes) - Profiling and observability
- [Episode #024: Internal Developer Portal Showdown](/podcasts/00024-internal-developer-portals-showdown) - Platform engineering tools
- [Episode #025: SRE Reliability Principles](/podcasts/00025-sre-reliability-principles) - Operational excellence
- [Episode #027: Observability Tools Showdown](/podcasts/00027-observability-tools-showdown) - Prometheus, Grafana at scale
- [Episode #020: Kubernetes IaC & GitOps](/podcasts/00020-kubernetes-iac-gitops) - GitOps deployment patterns
- [Episode #011: Why 70% of Platform Teams Fail](/podcasts/00011-platform-failures) - Common failure modes

**Technical Resources**:
- [Kubernetes Production Mastery Course](/courses/kubernetes-production-mastery) - Hands-on learning for production Kubernetes

## Conclusion

KubeCon Atlanta 2025 marked Kubernetes's transition from container orchestrator to AI-native platform. Dynamic Resource Allocation reaching GA, Workload API arriving, and operational maturity achieving 99.99% upgrade success demonstrate a platform ready for the next decade.

But the conference also revealed challenges: maintainer burnout, community sustainability questions, and the tension between innovation and complexity. CNCF's 200+ projects raise questions about focus and maintenance capacity.

The path forward requires balancing three forces:

**Innovation**: AI workloads, topology awareness, and sophisticated scheduling capabilities push Kubernetes's boundaries.

**Operational maturity**: After 10 years, safe upgrades, dependency management, and production reliability are non-negotiable.

**Community health**: Sustainable maintainership, institutional support, and explicit succession planning determine whether Kubernetes thrives for another decade.

Platform engineering teams have clarity now. Three principles. Proven patterns. Production-ready AI infrastructure. The technology is ready. The question is whether organizations will invest the 3-5 years required to build platforms correctly, avoiding the "puppy for Christmas" trap of templates without support.

The next KubeCon will show whether we learned the lessons from Atlanta 2025.
