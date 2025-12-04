---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ Podcast"
---

# The Platform Engineering Playbook Podcast

<GitHubButtons />

Welcome to The Platform Engineering Playbook Podcast — where everything you hear is built, reviewed, and improved by AI, by me, and by you, the listener.

This show keeps me — and hopefully you — up to speed on the latest in platform engineering, SRE, DevOps, and production engineering. It's a living experiment in how AI can help us track, explain, and debate the fast-moving world of infrastructure.

Every episode is open source. If you've got something to add, correct, or challenge, head to [GitHub](https://github.com/vibesre/Platform-Engineering-Playbook) — open a pull request, join the conversation, and make the Playbook smarter.

**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience seeking strategic insights on technology choices, market dynamics, and skill optimization.

---

## 🎥 Latest Episode: #046 - Cloud Cost Quick Wins for Year-End

**FinOps** • **12 minutes** • December 4, 2025 • Jordan and Alex

:::tip Six Quick Wins You Can Implement This Week

Global cloud spend hits $720 billion in 2025—and organizations waste 20-30% on unused resources. Year-end is the perfect time to show savings before budgets reset. Six actionable wins from scheduling (70% savings) to zombie hunting ($500-2K/month per account).

:::

**The Six Wins**: 1) Scheduling non-prod (70% savings), 2) Right-sizing (25-40% per instance), 3) Reserved Instances (up to 72% off), 4) Spot instances (60-90% savings), 5) Storage tiering, 6) Zombie resource hunt.

**Monday Checklist**: Run cost analyzer (30 min) → Find top 5 zombies (1 hr) → Schedule one non-prod env (2 hrs) → Present to manager (30 min).

**News Segment**: Envoy v1.36.3 CVEs (patch now), Loki Operator 0.9.0, AWS Graviton5 M9g preview, Uncloud for K8s-free deployments.

[📝 Full episode page →](/podcasts/00046-cloud-cost-quick-wins-year-end) • [📄 Previous episode: #045](/podcasts/00045-platform-engineering-vs-devops-vs-sre)

<PodcastSubscribeButtons />

---

## All Episodes

Pure chronological list of all podcast episodes and published course lessons. Episodes in reverse order (newest first).

- 🎙️ **[#046: Cloud Cost Quick Wins for Year-End](/podcasts/00046-cloud-cost-quick-wins-year-end)** (12 min) - Global cloud spend hits $720B in 2025, with 20-30% wasted on unused resources. Six quick wins you can implement this week: scheduling non-prod (70% savings), right-sizing (25-40% per instance), Reserved Instances (up to 72% off), Spot instances (60-90%), storage tiering, and zombie hunting ($500-2K/month per account). Monday checklist included. News: Envoy v1.36.3 CVEs, Loki Operator 0.9.0, AWS Graviton5 M9g preview.

- 🎙️ **[#045: Platform Engineering vs DevOps vs SRE - The Identity Crisis](/podcasts/00045-platform-engineering-vs-devops-vs-sre)** (17 min) - Platform Engineer roles pay 20% more than DevOps roles, but job descriptions are 90% identical. Is this title inflation? We trace the origin stories: DevOps (2009) was a movement, not a job title. SRE (2003/2016) added Google's 50% engineering time rule. Platform Engineering (2018-2020) brought product thinking. Decision framework: DevOps culture first, then SRE for reliability pain, then Platform Engineering for cognitive load. The 20% premium pays for product thinking, not the title. Includes December 3, 2025 news: PgBouncer CVE-2025-12819, MinIO Docker CVE controversy, GitHub CI/CD OTel guide.

- 🎙️ **[#044: Platform Engineering Certification Tier List 2025](/podcasts/00044-platform-engineering-certification-tier-list)** (30 min) - Are certifications worth it? We rank 25+ certifications using a data-driven 60/40 framework (60% skill-building, 40% market signal). CKA ($445, 66% pass rate, 45K+ job postings) remains gold standard. Platform engineers earn $172K vs DevOps $152K (13% premium). AWS SA Associate overrated (500K+ holders). CNPE early adopters get 12-18 month advantage. Optimal stack: CKA + one cloud Professional + one specialty cert (~$1,200, 7-9 months). Includes AWS Re:Invent 2025 news segment.

- 🎙️ **[#043: Kubernetes AI Conformance - The End of AI Infrastructure Chaos](/podcasts/00043-kubernetes-ai-conformance-program)** (17 min) - CNCF launched the Certified Kubernetes AI Conformance Program at KubeCon Atlanta (November 11, 2025)—the first vendor-neutral standard for AI workloads on Kubernetes. Five core certification requirements: Dynamic Resource Allocation (DRA), intelligent autoscaling, rich accelerator metrics, AI operator support (Kubeflow, Ray), and gang scheduling via Kueue/Volcano. 11+ vendors certified including AWS EKS, Google GKE, Microsoft Azure, Red Hat OpenShift, CoreWeave. DRA improves GPU utilization from 45-60% to 70-85%, reducing monthly GPU costs by 30-40%. Decision framework for when certification is critical vs less critical. ISO 42001 comparison (governance vs technical). v2.0 roadmap includes topology-aware scheduling and cost attribution.

- 🎙️ **[#042: Helm 4 Deep Dive - The Complete Guide to the Biggest Update in 6 Years](/podcasts/00042-helm-4-comprehensive-guide)** (24 min) - Helm 4.0 dropped at KubeCon Atlanta 2025—the first major version in 6 years. Server-Side Apply replaces three-way merge, ending GitOps ownership conflicts. SSA delivers 40-60% faster deployments. WASM plugins via Extism bring sandboxed security but require post-renderer migration. 12-month runway with Helm 3 support until November 2026. Breaking changes: CLI flag renames (--dry-run=server, --force-replace), annotation changes. Complete migration guide with SSA testing, WASM plugin porting, and staged rollout strategy.

- 🎙️ **[#041: CNPE Certification Guide - The First Platform Engineering Credential](/podcasts/00041-cnpe-certification-guide)** (15 min) - Complete guide to CNCF's new Certified Cloud Native Platform Engineer exam. Five domains: GitOps/CD (25%), Platform APIs (25%), Observability (20%), Architecture (15%), Security (15%). Beta testers report 29% scores—no Killer.sh simulator until Q1 2026. Platform engineers earn $219K average (20% more than DevOps). Three certification paths: Traditional (CKA→CKS→CNPA→CNPE), Fast-track (CNPA→CNPE), Full Coverage (Kubestronaut→CNPE). CNPE required for Golden Kubestronaut after March 1, 2026. Tools to know: ArgoCD, Flux, Backstage, Crossplane, OpenTelemetry, Kyverno.

- 🎙️ **[#040: 10 Platform Engineering Anti-Patterns That Kill Developer Productivity](/podcasts/00040-platform-engineering-anti-patterns)** (13 min) - DORA 2024 found organizations with platform teams saw throughput decrease by 8% and stability decrease by 14%. Why are so many platform investments backfiring? 10 anti-patterns: Ticket Ops (bottleneck factory), Ivory Tower Platform (disconnected from reality), Platform as Bucket (scope creep), Mandatory Adoption (forced usage), Golden Cage (over-standardization), Over-Engineered Monolith (complexity enemy), Front-End First (35% still use spreadsheets), Biggest Bang Trap (starting hard), Day 1 Obsession (under 1% of lifecycle), Build It And They Will Come (no marketing). What successful teams do: Spotify's Backstage users 2.3x more GitHub active, Zalando's first step was cultural, teams with stable priorities face 40% less burnout, adoption strategies yield 30% higher ROI. Audit checklist: devs waiting >1 day? platform team pair-programmed with devs? scope grown 3x? one-size-fits-all templates? beautiful portal but Slack for help?

- 🎙️ **[#039: Black Friday War Stories: Lessons from E-Commerce's Worst Days](/podcasts/00039-black-friday-war-stories)** (12 min) - Black Friday special diving into the graveyard of e-commerce outages. Hall of Fame crashes: J.Crew ($775K lost in 5 hours, 323,000 shoppers), Walmart ($9M before Black Friday started), Best Buy 2014 (78% mobile traffic surprise), Cloudflare 2024 (99.3% of Shopify stores frozen). Famous non-Black-Friday disasters: AWS S3 2017 ($150M typo, 4+ hours, 100,000+ sites), GitLab 2017 (5 backup systems none working, 300GB deleted). k8s.af Kubernetes failure stories. Platform engineer's playbook: load test at 5-10x (not 2x), multi-CDN/multi-cloud, monthly restore tests, chaos practice, mobile-first design, dangerous command safeguards.

- 🎙️ **[#038: Giving Thanks to Your Dependencies: A Platform Engineer's Gratitude Guide](/podcasts/00038-thanksgiving-oss-gratitude)** (10 min) - Thanksgiving special on thanking open source maintainers. 60% of maintainers unpaid. 60% have left or considered leaving. Gratitude tools: npx thanks, npm fund, cargo-thanks, thanks-stars. Happiness Packets for anonymous thank-you notes. Beyond stars: why specific use case emails matter more. Company-level: Open Source Pledge ($2K/dev/year), GitHub Sponsors, Maintainer Month. Your 5-minute Thanksgiving challenge: run npx thanks, pick one dependency, send a thank-you email, donate $5-10, star the repos.

- 🎙️ **[#037: KubeCon Atlanta 2025 Part 3: Community at 10 Years - The Sustainability Question](/podcasts/00037-kubecon-2025-community-sustainability)** (14 min) - CNCF celebrates 10 years with 300,000 contributors—but the sustainability crisis is real. 60% of maintainers unpaid. 60% have left or considered leaving. XZ Utils backdoor showed what happens when isolated maintainers burn out. Han Kang tribute reminds us of the human cost. Technical sessions revealed: CiliumCon (TikTok IPv6 migration, 60K node clusters), in-toto graduation for supply chain attestation, Gateway API convergence, OpenTelemetry eBPF maturity. Open Source Pledge ($2,000/developer/year minimum) and Kubernetes governance improvements (6→4 subteams) offer hope. Framework: audit dependencies for maintainer health, join Open Source Pledge, invest in the people who write the code.

- 🎙️ **[#036: KubeCon Atlanta 2025 Part 2: Platform Engineering Consensus and Community Reality Check](/podcasts/00036-kubecon-2025-platform-engineering)** (17 min) - After years of definitional chaos, platform engineering reached consensus at KubeCon 2025: three principles (API-first self-service, business relevance, managed service approach), real-world adoption at Intuit/Bloomberg/ByteDance scale, and honest burnout conversations. The "puppy for Christmas" anti-pattern explains 70% platform team failure. Intuit migrated Mailchimp's 11M users invisibly. Bloomberg ran K8s for 9 years. ByteDance's AI Brix is 80% external contributors. EU CRA clarified: individuals NOT liable, Dec 2027 deadline manageable. Cat Cosgrove (K8s Steering Committee) reveals "ready to abandon ship" from work overload. CNCF's 200+ projects raises sustainability questions. Kubernetes reduced dependencies 416→247 through discipline. Framework for platform teams: 3-5 year timeline, managed service commitment, business metrics, SBOM generation, community health investment.

- 🎙️ **[#035: KubeCon Atlanta 2025 Part 1: AI Goes Native and the 30K Core Lesson](/podcasts/00035-kubecon-2025-ai-native)** (19 min) - Google donates a GPU driver live on stage. OpenAI saves $2.16M/month with one line of code. Kubernetes rollback finally works after 10 years. What changed at KubeCon Atlanta 2025 that proves Kubernetes isn't adapting to AI—it's being rebuilt for it. Dynamic Resource Allocation reaches GA in Kubernetes 1.34, preventing 10-40% GPU performance loss from NUMA misalignment ($200K/day waste at 100-node scale). Workload API arrives in alpha for gang-scheduling multi-pod AI training. OpenAI freed 30,000 CPU cores by disabling inotify in Fluent Bit after profiling revealed 35% CPU time on fstat64. Skip-version upgrades now supported with 99.99% success rate. Monday action plan: test DRA in development, profile your highest-CPU service with perf or eBPF, check for NUMA misalignment in GPU workloads.

- 🎙️ **[#034: The $4,350/Month GPU Waste Problem](/podcasts/00034-kubernetes-gpu-cost-waste-finops)** (28 min) - Your H100 costs $5,000/month but runs at 13% utilization—wasting $4,350 monthly per GPU. Analysis of 4,000+ Kubernetes clusters reveals why Kubernetes treats GPUs as atomic resources, and the five-layer optimization framework (MIG, time-slicing, VPA, Spot, regional arbitrage) that recovers 75-93% of lost capacity in 90 days. Real case study: 20 H100s → 7 H100s ($100K → $35K/month, 65% reduction). Multi-Instance GPU enables 84% savings for multi-tenant SaaS workloads. AWS EKS Split Cost Allocation launched Sept 2025 for pod-level GPU tracking. Complete 90-day implementation playbook with $780K annual savings target for 20-GPU clusters.

- 🎙️ **[#033: Service Mesh Showdown: Why User-Space Beat eBPF](/podcasts/00033-service-mesh-showdown-cilium-istio-ambient)** (20 min) - Kernel-level eBPF should beat user-space proxies—but Istio Ambient delivers 8% mTLS overhead while Cilium shows 99%. Academic benchmarks reveal why architecture boundaries matter more than execution location. 50,000-pod stability testing shows Cilium's distributed control plane crashed the API server under churn while Istio's centralized architecture handled it. Decision framework for choosing based on cluster size, traffic patterns (L4 vs L7), and cost analysis ($186K/year savings for 2,000-pod clusters).

- 🎙️ **[#032: The Terraform vs OpenTofu Debate](/podcasts/00032-terraform-opentofu-debate)** (17 min) - HashiCorp's license change and IBM's $6.4B acquisition created the "you must migrate" narrative—but 70% of teams using Terraform in-house aren't legally affected. Fidelity's 50,000 state file migration case study, three-factor decision framework (Cloud lock-in, compliance, vendor tolerance), and why migration is 90% organizational change management. OpenTofu 1.7+ delivers state encryption after 5+ years of Terraform community requests.

- 🎙️ **[#031: Agentic DevOps - GitHub Agent HQ](/podcasts/00031-agentic-devops-github-agent-hq)** (18 min) - GitHub Universe 2025 announced Agent HQ—mission control for orchestrating AI agents from OpenAI, Anthropic, Google, and more. Azure SRE Agent saved Microsoft 20,000+ engineering hours. But 80% of companies report agents executing unintended actions, and only 44% have agent-specific security policies. Tiered adoption framework for deploying agents without creating catastrophic risk.

- 🎙️ **[#030: Cloudflare Outage November 2025](/podcasts/00030-cloudflare-outage-november-2025)** (13 min) - A routine database permissions change triggered Cloudflare's worst outage since 2019—taking down ChatGPT, X, Shopify, Discord, and 20% of the internet for 6 hours. Technical chain reaction from ClickHouse metadata exposure to FL2 Rust proxy panic when ~60 features became >200 and exceeded hardcoded limit. Third major cloud outage in 30 days raises infrastructure concentration risk questions.

- 🎙️ **[#029: Ingress NGINX Retirement](/podcasts/00029-ingress-nginx-retirement)** (13 min) - The de facto standard Kubernetes ingress controller is being retired in March 2026 with no security patches after. Only 1-2 maintainers for years, InGate replacement failed, and platform teams have four months to migrate. Four-phase migration framework to Gateway API with controller comparison and immediate actions.

- 🎙️ **[#028: OpenTelemetry eBPF Instrumentation](/podcasts/00028-opentelemetry-ebpf-instrumentation)** (14 min) - Complete observability without code changes sounds too good to be true—but kernel-level eBPF delivers under 2% CPU overhead. How Grafana's May 2025 Beyla donation to OpenTelemetry makes this mainstream, the TLS encryption catch nobody talks about, and decision framework for eBPF vs SDK instrumentation.

- 🎙️ **[#027: The Open Source Observability Showdown](/podcasts/00027-observability-tools-showdown)** (20 min) - When "free" Prometheus costs $6-12K/month in engineer time. Shopify's dedicated observability team, VictoriaMetrics' 40-60% storage wins, Loki's 10x cheaper storage with 3-5x slower queries, and the three-tier operational maturity framework for Prometheus/Grafana/Loki/Tempo build vs buy decisions. $2B+ Datadog revenue explained.

- 🎙️ **[#026: The Kubernetes Complexity Backlash](/podcasts/00026-kubernetes-complexity-backlash)** (13 min) - 92% market share meets 88% cost increases and 25% shrinking deployments. The 3-5x cost underestimation problem, 200-node rule, and when Docker Swarm/Nomad/ECS/PaaS beat Kubernetes. 37signals saved $10M+ leaving AWS, teams finally did the math

- 🎙️ **[#025: SRE Reliability Principles - The 26% Problem](/podcasts/00025-sre-reliability-principles)** (15 min) - Only 26% of organizations use SLOs despite 49% saying they're more relevant. Error budgets remain timeless, Platform Engineering and SRE are complementary, and AI/ML needs adapted reliability principles. Practical playbook for starting from zero or fixing ignored SLOs

- 🎙️ **[#024: Internal Developer Portal Showdown 2025](/podcasts/00024-internal-developer-portals-showdown)** (15 min) - Backstage costs $150K per 20 developers in hidden engineering time. Commercial platforms are 8-16x cheaper for most teams. Real pricing, timelines, and decision framework by team size

- 🎙️ **[#023: DNS for Platform Engineering](/podcasts/00023-dns-platform-engineering)** (23 min) - A forty-year-old protocol keeps taking down billion-dollar infrastructure. October 2025 AWS outage: 15 hours from a DNS race condition. CoreDNS, ndots:5 trap, and the five-layer defensive playbook

- 🎙️ **[#022: eBPF in Kubernetes](/podcasts/00022-ebpf-kubernetes)** (25 min) - Your Kubernetes cluster is a black box—Prometheus shows symptoms, not causes. eBPF turns the Linux kernel into a programmable platform for observability, networking, and security

- 🎙️ **[#021: Time Series Language Models](/podcasts/00021-time-series-language-models)** (20 min) - AI that reads your infrastructure metrics like language, explains anomalies in plain English, and predicts failures without training on your data. This technology exists now, but companies won't deploy it to production yet. Why?

- 🎙️ **[#020: Kubernetes IaC & GitOps - The Workflow Paradox](/podcasts/00020-kubernetes-iac-gitops)** (20 min) - 77% GitOps adoption yet deployments still take days. Why workflow design beats tool selection—ArgoCD vs Flux is a false choice, successful teams run both

- 🎙️ **[#019: The FinOps AI Paradox](/podcasts/00019-finops-ai-paradox)** (12 min) - Companies invest $500K in AI FinOps tools, identify $3M in savings, but implement only 6%. Why sophisticated AI fails to reduce cloud waste and what the successful 6% actually do differently

- 📖 **[#016: Kubernetes Production Mastery - Lesson 03](/courses/kubernetes-production-mastery/lesson-03)** (43 min) - Implement namespace-scoped RBAC roles, secure secrets management with Sealed Secrets/External Secrets, and remediate the 5 most common RBAC misconfigurations

- 🎙️ **[#015: The Cloud Repatriation Debate](/podcasts/00015-cloud-repatriation-debate)** (13 min) - AWS charges 10-100x more than it should? Real companies saving millions by leaving the cloud, hidden costs exposed, decision frameworks for when cloud makes sense

- 🎙️ **[#014: Kubernetes in 2025: The Maturity Paradox](/podcasts/00014-kubernetes-overview-2025)** (15 min) - 92% market share meets "do we need this?" backlash. Service mesh revolution, AI/ML integration, when to skip K8s for simpler alternatives

- 🎙️ **[#013: Backstage in Production: The 10% Adoption Problem](/podcasts/00013-backstage-adoption)** (16 min) - The real $1M+ cost, why adoption stalls at 10%, and honest comparison with Port, Cortex, and custom portals

- 🎙️ **[#012: Platform Engineering ROI Calculator](/podcasts/00012-platform-roi-calculator)** (15 min) - Prove platform value to executives: ROI formula, DORA→business translation, and stakeholder templates that saved teams from disbandment

- 🎙️ **[#011: Why 70% of Platform Engineering Teams Fail](/podcasts/00011-platform-failures)** (12 min) - The critical PM gap, metrics blindness, and the 5 predictive metrics that separate success from $3.75M failures

- 📖 **[#010: Kubernetes Production Mastery - Lesson 02](/podcasts/00010-kubernetes-production-mastery-lesson-02)** (19 min) - Master requests vs limits, QoS classes, and the 5-step debugging workflow for OOMKilled pods

- 📖 **[#009: Kubernetes Production Mastery - Lesson 01](/podcasts/00009-kubernetes-production-mastery-lesson-01)** (17 min) - Learn the 5 failure patterns that break systems at scale and the 6-item production readiness checklist

- 🎙️ **[#008: GCP State of the Union 2025](/podcasts/00008-gcp-state-of-the-union-2025)** (17 min) - When depth beats breadth: GCP's 32% growth vs AWS's 17%. 3x network performance advantages and automatic sustained use discounts

- 🎙️ **[#007: AWS Outage October 2025](/podcasts/00007-aws-outage-october-2025)** (16 min) - The $75M/hour lesson: DNS race condition in DynamoDB cascaded into 70+ AWS services down, affecting 1000+ companies

- 🎙️ **[#006: AWS State of the Union 2025](/podcasts/00006-aws-state-of-the-union-2025)** (29 min) - Navigate 200+ AWS services with strategic clarity. Which 20 services matter, career tier frameworks, cost optimization strategies

- 🎙️ **[#005: Platform Tools Tier List 2025](/podcasts/00005-platform-tools-tier-list)** (13 min) - Which skills command $24K+ higher salaries? Analyze 220+ tools, commoditization trap, S-tier specializations earning $130K-152K

- 🎙️ **[#004: PaaS Showdown 2025](/podcasts/00004-paas-showdown)** (14 min) - Flightcontrol vs Vercel vs Railway vs Render vs Fly.io. Deep dive into 2025 PaaS landscape with pricing models and decision frameworks

- 🎙️ **[#003: Platform Economics](/podcasts/00003-platform-economics)** (18 min) - Hidden costs and ROI of platform engineering. From cloud costs to engineering time, build vs buy decisions and opportunity costs

- 🎙️ **[#002: Cloud Providers](/podcasts/00002-cloud-providers)** (20 min) - AWS vs Azure vs GCP deep dive. Comprehensive comparison of strengths, weaknesses, pricing models, and decision frameworks

- 🎙️ **[#001: AI Platform Engineering](/podcasts/00001-ai-platform-engineering)** (15 min) - Shadow AI and governance. The AI platform engineering crisis 85% of organizations face right now and how to build platforms that support AI workloads

---

## Subscribe & Listen

The Platform Engineering Playbook Podcast is available on all major podcast platforms. Episodes are also available directly on this site.

## Contribute

Every topic, transcript, and summary you hear lives out in the open. If you've got thoughts, fixes, or new ideas, [open a PR on GitHub](https://github.com/vibesre/Platform-Engineering-Playbook/pulls).

And if you enjoyed the show, give the project a ⭐ star on GitHub — it helps others find and contribute to the Platform Engineering Playbook.
