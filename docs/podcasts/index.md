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

## 🎥 Latest Episode: #023 - DNS for Platform Engineering

**23 minutes** • Nov 9, 2025 • Alex and Jordan

<div style={{maxWidth: '640px', margin: '0 auto 1.5rem'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/qcDPewcDW6g"
      title="DNS for Platform Engineering: The Silent Killer"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

A forty-year-old protocol keeps taking down billion-dollar infrastructure. We dissect the October 2024 AWS outage that lasted 15+ hours due to a DNS race condition in DynamoDB's automation system. Explore CoreDNS plugin architecture, discover why Kubernetes' ndots:5 default creates 5x query amplification for external domains, and learn the five-layer defensive playbook: optimization (reduce query volume), failover (GSLB with health checks), security (DNSSEC + DoH), monitoring (latency and error rates), and chaos testing.

**Key Topics**: DNS mechanics, CoreDNS, ExternalDNS, ndots trap, TTL strategies, GSLB failover, AWS outage analysis

[📝 Full episode page →](/podcasts/00023-dns-platform-engineering)

<PodcastSubscribeButtons />

---

## 📖 Courses

Structured, multi-episode educational series designed for deep learning and skill mastery. Each course uses single-presenter lecture format optimized for retention with learning science principles (spaced repetition, active recall, progressive complexity).

### Kubernetes Production Mastery

Transform from a Kubernetes user into a production Kubernetes engineer. Learn how to run Kubernetes at scale with confidence through real-world failure patterns, systematic debugging, and battle-tested best practices.

- **10 lessons** • ~3 hours • Intermediate to Advanced
- **Prerequisites**: Basic Kubernetes knowledge (pods, deployments, services)
- **You'll Learn**: Production mindset and failure patterns • Resource management and QoS • RBAC and secrets security • Systematic debugging workflows • Stateful workloads and networking

[→ View Kubernetes Production Mastery Course](/podcasts/courses/kubernetes-production-mastery)

**🎥 YouTube Playlist**:

<div style={{maxWidth: '640px', margin: '1rem auto'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/videoseries?list=PLIjf2e3L8dZz3m5Qc5OFRUDSqeSsZHdcD"
      title="Kubernetes Production Mastery Course Playlist"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

### Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale

Master the LEGO architecture approach to multi-region systems. Learn the real 2.5-7.5x cost multiplier, compose building blocks (Aurora Global Database, EKS, Transit Gateway, DynamoDB Global Tables), and build production-grade architectures that match your actual needs—not aspirational ones.

- **16 lessons** (ALL PUBLISHED ✅) • ~4 hours • Advanced
- **Prerequisites**: 5+ years production AWS/Kubernetes experience, distributed systems knowledge
- **You'll Learn**: Real multi-region costs and trade-offs • Hot-hot/hot-warm/hot-cold patterns • AWS building blocks as composable pieces • Data consistency and replication strategies • Compliance and regulatory requirements

[→ View Multi-Region Mastery Course](/courses/multi-region-mastery)

---

## All Episodes

Pure chronological list of all podcast episodes and published course lessons. Episodes in reverse order (newest first).

- 🎙️ **[#023: DNS for Platform Engineering](/podcasts/00023-dns-platform-engineering)** (23 min) - A forty-year-old protocol keeps taking down billion-dollar infrastructure. October 2024 AWS outage: 15 hours from a DNS race condition. CoreDNS, ndots:5 trap, and the five-layer defensive playbook

- 🎙️ **[#022: eBPF in Kubernetes](/podcasts/00022-ebpf-kubernetes)** (25 min) - Your Kubernetes cluster is a black box—Prometheus shows symptoms, not causes. eBPF turns the Linux kernel into a programmable platform for observability, networking, and security

- 🎙️ **[#021: Time Series Language Models](/podcasts/00021-time-series-language-models)** (20 min) - AI that reads your infrastructure metrics like language, explains anomalies in plain English, and predicts failures without training on your data. This technology exists now, but companies won't deploy it to production yet. Why?

- 🎙️ **[#020: Kubernetes IaC & GitOps - The Workflow Paradox](/podcasts/00020-kubernetes-iac-gitops)** (20 min) - 77% GitOps adoption yet deployments still take days. Why workflow design beats tool selection—ArgoCD vs Flux is a false choice, successful teams run both

- 🎙️ **[#019: The FinOps AI Paradox](/podcasts/00019-finops-ai-paradox)** (12 min) - Companies invest $500K in AI FinOps tools, identify $3M in savings, but implement only 6%. Why sophisticated AI fails to reduce cloud waste and what the successful 6% actually do differently

- 📖 **[#016: Kubernetes Production Mastery - Lesson 03](/podcasts/00016-kubernetes-production-mastery-lesson-03)** (43 min) - Implement namespace-scoped RBAC roles, secure secrets management with Sealed Secrets/External Secrets, and remediate the 5 most common RBAC misconfigurations

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
