---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #050: AWS re:Invent 2025 - Infrastructure & Developer Experience"
slug: 00050-aws-reinvent-2025-infrastructure-developer-experience
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #050: AWS re:Invent 2025 - Infrastructure & Developer Experience

<GitHubButtons />

<iframe width="100%" style={{aspectRatio: '16/9', marginBottom: '1rem'}} src="https://www.youtube.com/embed/Y2LchNnHaSE" title="Episode #050: AWS re:Invent 2025 - Infrastructure & Developer Experience" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerPolicy="strict-origin-when-cross-origin" allowFullScreen></iframe>

**Duration**: 14 minutes | **Speakers**: Jordan & Alex

**Target Audience**: Platform engineers, SREs, cloud architects evaluating AWS infrastructure investments

**Series**: AWS re:Invent 2025 (Part 2 of 4)

---

## Synopsis

AWS is building a chip empire. Graviton5 delivers 192 cores with 25% better performance. Trainium3 UltraServers cut AI training costs by 50%. Lambda can now run workflows for an entire year. And Werner Vogels delivers his final re:Invent keynote with a framework for thriving in the AI era. This is part two of our four-part AWS re:Invent 2025 series.

---

## Chapter Markers

- **00:00** - Series Introduction (Part 2 of 4)
- **00:30** - News: BellSoft Hardened Container Images (95% fewer CVEs)
- **01:30** - News: GitHub Actions Package Manager Security Gaps
- **02:30** - News: Proxmox Datacenter Manager 1.0 (VMware Escape)
- **03:30** - Graviton5: 192 Cores Deep Dive (40% price-performance)
- **06:00** - Trainium 3 & AI Infrastructure (50% cost reduction)
- **08:00** - Lambda Durable Functions (Year-long workflows)
- **10:00** - Werner Vogels: Renaissance Developer & Verification Debt
- **12:30** - Key Takeaways & Closing

---

## News Segment (December 8, 2025)

- **[BellSoft Hardened Java Images](https://www.infoq.com/news/2025/12/bellsoft-hardened-images/)**: 95% fewer CVEs, built on Alpaquita Linux. Context: typical container images contain 600+ known vulnerabilities, nearly half of Java services contain known-exploited CVEs.
- **[GitHub Actions Package Manager Critique](https://nesbitt.io/2025/12/06/github-actions-package-manager.html)**: No lockfiles, mutable version tags, 54% of composite actions contain security weaknesses. Critical for CI/CD platforms using trusted publishing.
- **[Proxmox Datacenter Manager 1.0](https://www.theregister.com/2025/12/05/proxmox_datacenter_manager_1_stable/)**: VMware escape hatch for Broadcom migration. Centralized management, VM migration between clusters, fleet management. Built in Rust on Debian Trixie.

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Graviton5 cores | 192 | AWS |
| Graviton5 performance improvement | 25% vs Graviton4 | AWS |
| Top 1000 AWS customers using Graviton | 98% | AWS |
| Trainium3 performance vs Trn2 | 4.4x | AWS |
| Trainium3 cost reduction | 50% | AWS |
| Trainium3 PFLOPs per UltraServer | 362 FP8 | AWS |
| Lambda Durable max workflow duration | 1 year | AWS |
| Database Savings Plans (serverless) | up to 35% | AWS |
| Cloud native developers globally | 15.6 million | CNCF/SlashData |

---

## Key Announcements Covered

### Graviton5
- 192 cores, 25% better performance, 33% lower inter-core latency
- 5x larger L3 cache, built on Arm Neoverse V3 (3nm)
- Customer results: SAP (35-60%), Atlassian (30%), Honeycomb (36%)
- Instance types: M9g, C9g, R9g (launching 2026)

### Trainium3 UltraServers
- 4.4x more compute vs Trainium2, 50% cost reduction
- 362 FP8 PFLOPs per UltraServer, 144 chips per server
- 4x better energy efficiency
- Used by: Anthropic, Metagenomi, Ricoh, Decart

### Lambda Durable Functions
- Workflows from seconds to 1 year
- New primitives: `context.step()` for checkpoints, `context.wait()` for suspension
- Built-in retry and error handling
- Simplifies state management vs Step Functions

### Database Savings Plans
- Up to 35% savings (serverless), 20% (provisioned)
- One-year term, no upfront payment required
- Covers Aurora, RDS, DynamoDB, ElastiCache, Neptune, and more

### Werner Vogels: Renaissance Developer Framework
1. **Be Curious**: AI lowers the barrier to learning
2. **Think in Systems**: Architecture matters more than ever
3. **Communicate Precisely**: AI amplifies unclear thinking
4. **Own Your Work**: "Vibe coding is fine... but you own it"
5. **Become a Polymath**: Cross-disciplinary skills differentiate

### Verification Debt (New Concept)
AI generates code faster than humans can comprehend it. Code reviews become "the control point to restore balance."

---

## Transcript

**Jordan**: Welcome to part two of our four-part AWS re:Invent twenty twenty-five series. In episode forty-nine, we covered agentic AI and frontier agents. Today, we're going deep on infrastructure: chips, serverless evolution, and Werner Vogels' framework for thriving in the AI era. But first, let's check what else is happening in platform engineering.

**Jordan**: The CNCF just released their Q4 twenty twenty-five Technology Radar for AI tools in cloud native ecosystems. NVIDIA Triton, Metaflow, and Model Context Protocol are leading in adoption and developer trust. But here's the interesting part. The Agent2Agent protocol received a ninety-four percent recommendation score. That's developers signaling which agentic AI standards they trust for production. If you're building AI agents, these are the patterns to follow.

**Jordan**: And speaking of cloud native, the ecosystem just hit fifteen point six million developers. That's according to CNCF and SlashData's latest survey. Seventy-seven percent of backend developers are now using at least one cloud native technology. And here's a sign of convergence: forty-one percent of AI and ML developers now identify as cloud native. The silos between AI and infrastructure teams are breaking down. That's exactly who AWS is targeting with their re:Invent infrastructure announcements. Let's dig in.

**Alex**: Let's start with silicon. AWS is building its own chip empire, and Graviton five is the latest milestone.

**Jordan**: Why does custom silicon matter so much?

**Alex**: Control and differentiation. When you design your own chips, you control the cost structure. You can optimize for your specific workloads. And you create features competitors can't easily replicate. Here's the key stat: ninety-eight percent of AWS's top one thousand customers are already using Graviton. This isn't experimental anymore. It's mainstream infrastructure.

**Jordan**: What does Graviton five actually deliver?

**Alex**: One hundred ninety-two cores. Twenty-five percent better compute performance compared to Graviton four. Thirty-three percent lower inter-core latency. And a five-times larger L3 cache. It's built on Arm Neoverse V3 architecture using TSMC's three nanometer process. The new instance types, M9g, C9g, and R9g, launch in twenty twenty-six.

**Jordan**: What are customers actually seeing in production?

**Alex**: SAP reported thirty-five to sixty percent performance improvement for S/4HANA workloads. Atlassian saw thirty percent higher performance with significant cost reduction. Honeycomb, the observability company, measured thirty-six percent better throughput. These aren't benchmarks. These are production results.

**Jordan**: So for platform teams, the question is whether their workloads are Graviton-ready?

**Alex**: Exactly. Most container workloads compile seamlessly for ARM. The migration patterns are well-established now. If you're not running Graviton, you're leaving price-performance on the table.

**Jordan**: Let's talk about AI training economics. Trainium three is AWS's answer to GPU constraints.

**Alex**: The challenge is that training large models is expensive. GPU supply is still constrained. AWS is offering an alternative: custom AI chips designed specifically for training workloads.

**Jordan**: What do the numbers look like?

**Alex**: Trainium three UltraServers deliver four point four times more compute performance versus Trainium two. Fifty percent cost reduction for AI training. Three hundred sixty-two FP8 petaflops per UltraServer with up to one hundred forty-four chips. And four times better energy efficiency. EC2 UltraClusters three point zero can connect thousands of UltraServers scaling up to one million chips total.

**Jordan**: Who's actually using this?

**Alex**: Anthropic is using Trainium for Claude training. Metagenomi for genomics research. Ricoh for document processing AI. And Decart achieved four times faster inference for real-time generative video at half the cost of GPUs. AWS also announced Trainium four on the roadmap, which will be NVIDIA NVLink compatible. They're playing the long game.

**Jordan**: And there's an on-premises option now?

**Alex**: AWS AI Factories. Complete Trainium-based training infrastructure for organizations with data sovereignty requirements. You can run AWS's AI compute stack in your own data center.

**Jordan**: Now let's talk about Lambda. AWS just fundamentally changed what serverless can do.

**Alex**: Lambda Durable Functions. The traditional Lambda timeout is fifteen minutes. Complex workflows required Step Functions. Now you can build stateful workflows directly in Lambda that run from seconds to one full year.

**Jordan**: How does it work?

**Alex**: Two new primitives. context dot step creates durable checkpoints. Your function can execute some code, checkpoint the result, and if anything fails, it resumes from that checkpoint. context dot wait suspends execution and resumes when an event arrives. You can wait for human approval. External API callbacks. Timer expirations. All natively in Lambda.

**Jordan**: Can you give us an example?

**Alex**: Picture a data pipeline that fetches data, then waits up to seven days for human approval, then processes the data after approval. In the old world, you'd build a Step Functions state machine, handle the callback pattern, manage the state store. Now it's three lines of code with context dot step and context dot wait.

**Jordan**: What use cases does this unlock?

**Alex**: Human approval workflows. Long-running data pipelines. Multi-day batch processing. Event-driven orchestration. If you're using Step Functions for straightforward state management, Lambda Durable might be simpler. It's not replacing Step Functions for complex orchestration, but it eliminates a lot of boilerplate.

**Jordan**: What else is new in Lambda?

**Alex**: Lambda Managed Instances gives you EC2 compute power with Lambda's simplicity. It's a bridge between serverless and traditional compute. And IPv6 VPC support saves you thirty-plus dollars per month on NAT Gateway costs. That's low-hanging fruit for any VPC running Lambda.

**Jordan**: Let's talk cost optimization. Database Savings Plans.

**Alex**: Up to thirty-five percent savings for serverless databases. Up to twenty percent for provisioned instances. One-year term commitment. Covers Aurora, RDS, DynamoDB, and more.

**Jordan**: How does it work in practice?

**Alex**: You commit to a dollar-per-hour spend. AWS automatically applies that commitment across all covered databases. It's flexible across database types. For most tiers, there's no upfront payment required.

**Jordan**: Platform engineering angle?

**Alex**: This is an easy cost optimization lever. If your database spend is stable and predictable, commit today. Stack it with Reserved Instances where applicable. The ROI calculation is straightforward: stable spend equals immediate savings.

**Jordan**: Now let's talk about Werner Vogels. His final re:Invent keynote after fourteen years.

**Alex**: He opened by saying, quote, this is my final re:Invent keynote. I'm not leaving Amazon or anything like that, but I think that after fourteen re:Invents you guys are owed young, fresh, new voices. End quote. Then he laid out a framework for thriving in the AI era.

**Jordan**: The Renaissance Developer.

**Alex**: Five qualities. First: be curious. AI lowers the barrier to learning new things. You can explore any technology in hours, not months. Second: think in systems. Architecture matters more than ever. AI writes code. You design systems. Third: communicate precisely. AI amplifies unclear thinking. Vague prompts produce vague code. Fourth: own your work. Quote, vibe coding is fine, but only if you pay close attention to what is being built. The work is yours, not that of the tools. You build it, you own it. End quote. Fifth: become a polymath. Cross-disciplinary skills differentiate. Breadth plus depth equals competitive advantage.

**Jordan**: And he introduced a concept every platform engineer needs to understand.

**Alex**: Verification debt. AI generates code faster than humans can comprehend it. That creates a gap between what gets written and what gets understood. The gap keeps growing until something breaks in production.

**Jordan**: So code reviews become more important, not less.

**Alex**: Exactly. Vogels said, quote, we all hate code reviews. It's like being a twelve-year-old and standing in front of the class. But the review becomes the control point to restore balance. End quote. For AI-generated code, human review is the last line of defense.

**Jordan**: The big question everyone asks: will AI take my job?

**Alex**: Vogels' answer: quote, will AI take my job? Maybe. Will AI make me obsolete? Absolutely not. If you evolve. End quote.

**Jordan**: Let's wrap with key takeaways. First, Graviton five is the new default. One hundred ninety-two cores, twenty-five percent faster, and ninety-eight percent of top customers already on Graviton. The ARM migration is no longer optional.

**Alex**: Second, Trainium three changes AI economics. Fifty percent cost reduction for training. If you're evaluating AI infrastructure, Trainium is now a serious alternative to NVIDIA.

**Jordan**: Third, Lambda Durable Functions simplify orchestration. Workflows that run up to a year. No more Step Functions for straightforward state management.

**Alex**: Fourth, Database Savings Plans are easy wins. Thirty-five percent savings on serverless databases. If your database spend is predictable, commit today.

**Jordan**: Fifth, verification debt is real. Werner Vogels' warning: AI speed creates new risks. Code reviews are more important, not less.

**Alex**: Next episode, we're diving into EKS Capabilities. AWS is now managing your Argo CD, Crossplane, and ACK controllers. Combined with one hundred thousand node clusters and natural language Kubernetes management, is this the era of invisible infrastructure?

**Jordan**: The infrastructure decisions you make today compound for years. Choose wisely.

---

## Related Episodes

- [Episode #049: AWS re:Invent 2025 - The Agentic AI Revolution](/podcasts/00049-aws-reinvent-2025-agentic-ai-revolution) (Part 1 of 4)
- [Episode #034: Kubernetes GPU Cost Waste & FinOps](/podcasts/00034-kubernetes-gpu-cost-waste-finops) (Trainium as alternative)

---

## Resources

### AWS Primary Sources
- [AWS Graviton5 Announcement](https://www.aboutamazon.com/news/aws/aws-graviton-5-cpu-amazon-ec2)
- [Trainium3 UltraServers](https://www.aboutamazon.com/news/aws/trainium-3-ultraserver-faster-ai-training-lower-cost)
- [Werner Vogels Keynote](https://siliconangle.com/2025/12/05/amazon-cto-werner-vogels-foresees-rise-renaissance-developer-final-keynote-aws-reinvent/)
- [Database Savings Plans](https://aws.amazon.com/blogs/aws/introducing-database-savings-plans-for-aws-databases/)
