---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #051: AWS re:Invent 2025 - EKS & Cloud Operations"
slug: 00051-aws-reinvent-2025-eks-cloud-operations
keywords: [AWS re:Invent 2025, EKS, Amazon EKS, Kubernetes, EKS Ultra Scale, EKS Capabilities, Argo CD, AWS Controllers for Kubernetes, ACK, EKS MCP Server, CloudWatch, DevOps Agent, AIOps, cloud operations, observability, platform engineering]
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #051: AWS re:Invent 2025 - EKS & Cloud Operations

<GitHubButtons />

**Duration**: 18 minutes | **Speakers**: Jordan & Alex
**Series**: AWS re:Invent 2025 (Part 3 of 4)
**Target Audience**: Platform Engineers, SREs, DevOps Engineers, Cloud Architects

## Episode Overview

AWS transforms Kubernetes into an AI infrastructure platform. EKS Ultra Scale supports 100,000 nodes per cluster—enabling 1.6 million Trainium accelerators in a single cluster. EKS Capabilities brings managed Argo CD, AWS Controllers for Kubernetes, and Kube Resource Orchestrator. The EKS MCP Server lets you manage clusters with natural language instead of kubectl. CloudWatch gets generative AI observability for LangChain and CrewAI agents, while DevOps Agent acts as an autonomous on-call engineer. This is the infrastructure that will run the next generation of AI workloads.

---

## Key Announcements Covered

### EKS Ultra Scale (100K Nodes)
- **Scale**: Up to 100,000 worker nodes per cluster (vs. 15K GKE, 5K AKS)
- **Accelerators**: 1.6 million Trainium chips or 800K NVIDIA GPUs
- **Technical Innovation**: etcd Raft replaced with AWS "journal" system
- **Performance**: 500 pods/second scheduling at 100K scale
- **Customer**: Anthropic improved latency KPIs from 35% to 90%+

### EKS Capabilities
- **Managed Argo CD**: GitOps without operational overhead
- **AWS Controllers for Kubernetes (ACK)**: 200+ CRDs for 50+ AWS services
- **Kube Resource Orchestrator (KRO)**: Platform abstractions for developers
- **Architecture**: Runs in AWS service-owned accounts

### EKS MCP Server (Preview)
- Natural language Kubernetes management
- No kubectl or kubeconfig required
- Integrates with Kiro, Cursor, Cline, Amazon Q
- CloudTrail integration for audit logging

### EKS Provisioned Control Plane
- T-shirt sizes: XL, 2XL, 4XL
- 4XL: 6,800 concurrent API requests, 400 pods/sec
- Supports up to 40K nodes, 640K pods
- Pricing: $1.65/hr (XL) to $6.90/hr (4XL)

### Cloud Operations
- **CloudWatch Gen AI Observability**: LangChain, LangGraph, CrewAI support
- **DevOps Agent (Preview)**: Autonomous on-call engineer (Kindle: 80% time savings)
- **CloudWatch MCP Servers**: AI assistant integration with observability data
- **Unified Data Store**: S3 Tables with OCSF and Apache Iceberg
- **Application Signals**: GitHub Action for PR observability

---

## Timestamps

- **00:00** - Series Introduction (Part 3 of 4)
- **00:45** - News: cert-manager CVE patches, Canonical K8s 15-year LTS
- **03:30** - News: OpenTofu 1.11, Cloudflare IaC, Go Secret Mode
- **05:00** - EKS Ultra Scale: 100K Nodes Deep Dive
- **08:30** - The etcd Revolution: Journal and In-Memory Storage
- **10:30** - EKS Capabilities: Managed Argo CD, ACK, KRO
- **14:00** - EKS MCP Server: Natural Language Kubernetes
- **16:30** - Provisioned Control Plane: Performance Tiers
- **17:30** - CloudWatch Gen AI Observability
- **19:00** - DevOps Agent and Unified Data Store
- **20:30** - Key Takeaways for Platform Engineers

---

## News Segment Links

### Top Story
- [cert-manager v1.19.2](https://github.com/cert-manager/cert-manager/releases/tag/v1.19.2) - CVE patches for Go standard library vulnerabilities

### Quick Hits
- [Canonical Extends Kubernetes Long-Term Support to 15 Years](https://thenewstack.io/canonical-extends-kubernetes-long-term-support-to-15-years/)
- [OpenTofu 1.11](https://github.com/opentofu/opentofu/releases/tag/v1.11.0) - Ephemeral resources and enabled meta-argument
- [Shifting left at enterprise scale: how we manage Cloudflare with Infrastructure as Code](https://blog.cloudflare.com/shift-left-enterprise-scale/)
- [Pulumi replaceWith Resource Option](https://www.pulumi.com/blog/dependent-resource-replacements/)
- [Go proposal: Secret mode](https://antonz.org/accepted/runtime-secret/)

---

## Sources

### EKS Announcements
- [Amazon EKS enables ultra scale AI/ML workloads with support for 100K nodes](https://aws.amazon.com/blogs/containers/amazon-eks-enables-ultra-scale-ai-ml-workloads-with-support-for-100k-nodes-per-cluster/)
- [Announcing Amazon EKS Capabilities](https://aws.amazon.com/blogs/aws/announcing-amazon-eks-capabilities-for-workload-orchestration-and-cloud-resource-management/)
- [Amazon EKS introduces Provisioned Control Plane](https://aws.amazon.com/blogs/containers/amazon-eks-introduces-provisioned-control-plane/)
- [Introducing the fully managed Amazon EKS MCP Server](https://aws.amazon.com/blogs/containers/introducing-the-fully-managed-amazon-eks-mcp-server-preview/)
- [Under the hood: Amazon EKS ultra scale clusters](https://aws.amazon.com/blogs/containers/under-the-hood-amazon-eks-ultra-scale-clusters/)

### Cloud Operations
- [2025 Top 10 Announcements for AWS Cloud Operations](https://aws.amazon.com/blogs/mt/2025-top-10-announcements-for-aws-cloud-operations/)
- [Embracing AI-driven operations and observability at re:Invent 2025](https://aws.amazon.com/blogs/mt/embracing-ai-driven-operations-and-observability-at-reinvent-2025/)

---

## Transcript

**Jordan**: Welcome to part three of our four-part AWS re:Invent twenty twenty-five series. In episode forty-nine, we covered agentic AI and frontier agents. Episode fifty dove into Graviton five, Trainium three, and Lambda Durable Functions. Today, we're covering what I think is the most consequential announcement for platform engineers: how AWS is transforming EKS from a container orchestrator into a full AI infrastructure platform. But first, let's check what else is happening in platform engineering.

**Alex**: And there's actually some urgent news today. cert-manager version one point nineteen point two just dropped, and it's patching two CVEs in the Go standard library. CVE twenty twenty-five sixty-one seven two seven and CVE twenty twenty-five sixty-one seven two nine. If you're running Trivy scans, these will get flagged on your next run.

**Jordan**: This is a patch now situation, not a next sprint situation. The good news is it's a straightforward version bump with no breaking changes. And if you're still on the one point eighteen branch, version one point eighteen point four backports the same fixes.

**Alex**: In other news, Canonical just extended Kubernetes long-term support to fifteen years. Fifteen years. They're doing this through Ubuntu Pro plus a Legacy add-on, and they're clearly targeting enterprises that need mainframe-level support cycles.

**Jordan**: That's fascinating positioning. Meanwhile, OpenTofu one point eleven dropped with a feature I've been waiting for: ephemeral resources. You can now handle secrets without them persisting to state files. They also added an enabled meta-argument to replace those awkward count conditionals we've all written.

**Alex**: Cloudflare published a detailed post about how they manage hundreds of internal accounts with Infrastructure as Code. They're implementing shift-left security to prevent misconfigurations that could propagate globally in seconds. Worth reading if you're running IaC at scale.

**Jordan**: And one more quick hit: there's a Go proposal gaining traction for runtime secret mode. It would protect sensitive values from memory dumps and debugging. Important for anyone handling credentials in Go services.

**Alex**: Alright, let's dive into re:Invent. Jordan, when you say EKS is becoming an AI infrastructure platform, what does that actually mean?

**Jordan**: It means AWS made four massive announcements that fundamentally change what EKS can do. First, EKS Ultra Scale, which supports one hundred thousand nodes in a single cluster. Second, EKS Capabilities, which brings managed Argo CD, ACK, and KRO. Third, the EKS MCP Server for natural language cluster management. And fourth, Provisioned Control Plane with guaranteed performance tiers.

**Alex**: Let's start with Ultra Scale because the numbers are staggering. One hundred thousand nodes per cluster. To put that in context, Google Kubernetes Engine maxes out at fifteen thousand nodes per standard cluster. Azure Kubernetes Service caps at five thousand.

**Jordan**: Right. AWS now has a six to twenty X advantage in cluster scale. But the real number that matters isn't nodes, it's accelerators. One hundred thousand nodes means you can run up to one point six million AWS Trainium accelerators in a single cluster. Or eight hundred thousand NVIDIA GPUs.

**Alex**: That's the scale you need for training trillion-parameter models. And these AI workloads fundamentally can't be distributed across multiple clusters easily. The training job needs all accelerators available within one logical cluster.

**Jordan**: Here's where it gets technically interesting. The bottleneck at scale has always been etcd. The Kubernetes control plane stores all cluster state in etcd, and etcd uses Raft consensus for replication. Raft works great at normal scale, but it becomes the limiting factor when you're trying to coordinate one hundred thousand nodes.

**Alex**: So what did AWS do?

**Jordan**: They completely overhauled etcd. They replaced the Raft-based consensus backend with something they call journal. This is an internal component AWS has been building for over a decade. It provides ultra-fast, ordered data replication with multi-Availability Zone durability.

**Alex**: So they essentially swapped out the replication engine under etcd.

**Jordan**: Exactly. And they went further. They moved etcd's entire backend database to in-memory storage using tmpfs. This gives order-of-magnitude performance wins. Higher read-write throughput, predictable latencies, faster maintenance operations. They also doubled the maximum database size to twenty gigabytes.

**Alex**: What about pod scheduling at that scale? The scheduler becomes a bottleneck too.

**Jordan**: AWS optimized the scheduler plugins and node filtering parameters specifically for large-scale workloads. The result: they achieved five hundred pods per second scheduling throughput even at one hundred thousand node scale.

**Alex**: That's impressive. Are there real customers running at this scale?

**Jordan**: Yes. Anthropic is using EKS Ultra Scale to train Claude. They reported that their end-user latency KPIs improved from an average of thirty-five percent to consistently above ninety percent. Amazon is also using it for training Nova models.

**Alex**: Let's move to EKS Capabilities because this affects more teams directly. What problem is this solving?

**Jordan**: Platform teams have been running Argo CD for GitOps and ACK for managing AWS resources from Kubernetes. But maintaining these systems is real work. You need to patch them, upgrade them, ensure compatibility, handle scaling. EKS Capabilities makes all of that AWS's problem.

**Alex**: So AWS is now managing Argo CD for you?

**Jordan**: Yes. And it's not just running in your cluster. These capabilities actually run in AWS service-owned accounts that are fully abstracted from you. AWS handles infrastructure scaling, patching, updates, and compatibility analysis.

**Alex**: Let's break down the three capabilities. First is Argo CD.

**Jordan**: Argo CD is the most popular GitOps tool for Kubernetes. The twenty twenty-four CNCF survey showed forty-five percent of Kubernetes users are running Argo CD in production or planning to. With EKS Capabilities, you get a fully managed Argo CD instance that can deploy applications across multiple clusters. Git becomes your source of truth, and Argo automatically remediates drift.

**Alex**: Second is ACK, AWS Controllers for Kubernetes.

**Jordan**: ACK lets you manage AWS resources using Kubernetes Custom Resource Definitions. The managed version provides over two hundred CRDs for more than fifty AWS services. You can create S3 buckets, RDS databases, IAM roles, all from YAML. No need to install or maintain controllers yourself.

**Alex**: And third is KRO, Kube Resource Orchestrator.

**Jordan**: KRO is about abstraction. Platform teams can create reusable resource bundles that hide complexity. Developers consume these abstractions without needing to understand the underlying details. It's how you build your internal developer platform on Kubernetes.

**Alex**: What does the multi-cluster architecture look like?

**Jordan**: You run all three capabilities in a centrally managed cluster. Argo CD on that management cluster deploys applications to workload clusters across different regions or accounts. ACK provisions AWS resources for all clusters. KRO creates portable platform abstractions that work everywhere. It's a clean separation of concerns.

**Alex**: How does pricing work?

**Jordan**: Per-capability, per-hour billing with no upfront commitments. You're charged for each capability resource for each hour it's active. There are also additional charges for the specific Kubernetes resources managed by the capabilities.

**Alex**: Now let's talk about the EKS MCP Server because this feels like a glimpse of the future. What is MCP?

**Jordan**: MCP stands for Model Context Protocol. It's an open-source standard that gives AI models secure access to external tools and data sources. Think of it as a standardized interface that enriches AI applications with real-time, contextual knowledge.

**Alex**: And AWS built an MCP server for EKS?

**Jordan**: Yes. The EKS MCP Server lets you manage Kubernetes clusters using natural language instead of kubectl. You can say show me all pods not in running state, and it just works. You can say create a new EKS cluster named demo cluster with VPC and Auto Mode, and it does it.

**Alex**: No kubectl, no kubeconfig?

**Jordan**: Exactly. You can get logs, check deployments, create clusters, all through conversation. The server translates natural language into AWS and Kubernetes API calls behind the scenes.

**Alex**: What about security and enterprise requirements?

**Jordan**: The MCP server is hosted in AWS cloud, so there's no local installation or maintenance. You get automatic updates, patching, AWS IAM integration for security, and CloudTrail integration for audit logging. Plus, it draws on a knowledge base built from AWS's operational experience managing millions of Kubernetes clusters.

**Alex**: What AI tools does it integrate with?

**Jordan**: It works with Kiro, which is AWS's IDE and CLI. Also Cursor, Cline, and you can use it with Amazon Q Developer. Or you can build your own agents that interface with EKS clusters through the MCP server.

**Alex**: This changes who can operate Kubernetes clusters.

**Jordan**: That's the key insight. AWS was one of the first managed Kubernetes providers to implement MCP. They're betting that conversational AI turns multi-step manual tasks into simple requests. The barrier to Kubernetes operations just dropped significantly.

**Alex**: Let's cover Provisioned Control Plane before we move to cloud operations. What problem does this solve?

**Jordan**: Standard EKS control planes have variable performance. Under burst loads, you can get unpredictable behavior. Enterprises need guaranteed SLAs, especially for production workloads. Provisioned Control Plane lets you pre-allocate control plane capacity with well-defined performance characteristics.

**Alex**: How do the tiers work?

**Jordan**: They use T-shirt sizing: XL, two XL, and four XL. Each tier defines capacity through three attributes. First, API request concurrency, which is how many requests the API server can handle simultaneously. Second, pod scheduling rate in pods per second. Third, cluster database size for etcd.

**Alex**: What can the four XL tier do?

**Jordan**: Four XL supports up to sixty-eight hundred concurrent API requests and four hundred pods scheduled per second. In stress testing, AWS showed it can support forty thousand nodes and six hundred forty thousand pods. That's an eight X improvement over standard control planes.

**Alex**: What does it cost?

**Jordan**: XL starts at one dollar sixty-five per hour. Four XL is six dollars ninety per hour. That's in addition to standard or extended support hourly charges. You can switch tiers as workloads change, or revert to standard control plane during quieter periods.

**Alex**: Now let's shift to cloud operations because AWS made equally significant announcements there. Starting with CloudWatch.

**Jordan**: CloudWatch now has comprehensive observability for generative AI applications and agents. You get built-in insights into latency, token usage, and errors across your AI stack. No custom instrumentation required.

**Alex**: What frameworks does it support?

**Jordan**: It works with Amazon Bedrock AgentCore natively. But it's also compatible with open-source agentic frameworks like LangChain, LangGraph, and CrewAI. You can monitor model invocations, trace agent workflows end-to-end, and identify performance bottlenecks.

**Alex**: This is critical as more teams deploy AI agents.

**Jordan**: Exactly. Agent observability has been a gap. You deploy an agent, and when something goes wrong, you're debugging in the dark. Now you have proper tracing and metrics out of the box.

**Alex**: What about the DevOps Agent?

**Jordan**: The AWS DevOps Agent is in preview, and it's essentially an autonomous on-call engineer. It analyzes data across CloudWatch, GitHub, ServiceNow, and other tools to identify root causes and coordinate incident response.

**Alex**: Has anyone measured the impact?

**Jordan**: The Kindle team reported eighty percent time savings using CloudWatch Investigations, which is the underlying technology. The DevOps Agent goes further by acting proactively. It correlates telemetry, identifies root causes, and reduces operational burdens so teams can focus on higher-value work.

**Alex**: CloudWatch also got MCP servers?

**Jordan**: Yes. The MCP servers for CloudWatch bridge AI assistants to your observability data. They provide standardized access to metrics, logs, alarms, traces, and service health data. You can build autonomous operational workflows and integrate CloudWatch with AI-powered development tools.

**Alex**: What about data management?

**Jordan**: CloudWatch introduced a unified data store for operations, security, and compliance data. It automates collection from AWS and third-party sources like CrowdStrike, Microsoft Office three sixty-five, and SentinelOne. Everything gets stored in S3 Tables with OCSF and Apache Iceberg support.

**Alex**: That simplifies the log aggregation problem.

**Jordan**: Significantly. Automatic normalization across sources, native analytics integration, built-in support for industry-standard formats. And the first copy of centralized logs incurs no additional ingestion charges. It's actually cost-efficient for multi-account log management.

**Alex**: What else is new in observability?

**Jordan**: Application Signals now has a GitHub Action that provides observability insights during pull requests and CI/CD pipelines. Developers can identify performance regressions without leaving their development environment. There's also auto-discovery that visualizes application topology without requiring instrumentation.

**Alex**: And database insights?

**Jordan**: CloudWatch Database Insights now supports cross-account and cross-region monitoring. You can get centralized visibility into database performance across your entire AWS organization. It supports RDS, Aurora, and DynamoDB from a single monitoring account.

**Alex**: Let's wrap up with what all this means for platform engineers.

**Jordan**: There are four big takeaways. First, scale is no longer a constraint. One hundred thousand nodes opens new architecture patterns that simply weren't possible before.

**Alex**: Second?

**Jordan**: GitOps becomes turnkey. EKS Capabilities eliminates the maintenance burden of running Argo CD and ACK. That's real operational toil that goes away.

**Alex**: Third?

**Jordan**: Natural language ops is real. The MCP Server changes who can operate clusters. We're moving from kubectl mastery to conversational cluster management.

**Alex**: And fourth?

**Jordan**: Observability goes proactive. DevOps Agent as your first line of defense, gen AI tracing out of the box, unified data management. The operations experience is fundamentally changing.

**Alex**: What's the overall pattern here?

**Jordan**: EKS is evolving from a container orchestration service into a fully managed AI cloud platform. AWS is betting that Kubernetes will anchor the next decade of AI infrastructure. Every announcement we covered today focuses on AI workload enablement.

**Alex**: Next episode, we're wrapping up our re:Invent coverage with part four. Data and AI services. S3 Tables, Zero ETL, and how AWS is rethinking the data stack for AI workloads.

**Jordan**: The infrastructure announcements we covered today set the foundation. For platform engineers, the question isn't whether to adopt these capabilities. It's how fast you can integrate them into your platform strategy. Because the teams that master AI infrastructure will define the next era of software delivery.

---

## Related Episodes

- [Episode #049: AWS re:Invent 2025 - The Agentic AI Revolution](/podcasts/00049-aws-reinvent-2025-agentic-ai-revolution) (Part 1 of 4)
- [Episode #050: AWS re:Invent 2025 - Infrastructure & Developer Experience](/podcasts/00050-aws-reinvent-2025-infrastructure-developer-experience) (Part 2 of 4)
- Episode #052: AWS re:Invent 2025 - Data & AI Services (Part 4 of 4) - Coming Soon
