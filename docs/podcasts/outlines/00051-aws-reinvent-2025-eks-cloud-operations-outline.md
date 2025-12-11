# Episode #051: AWS re:Invent 2025 - EKS & Cloud Operations

**Series**: AWS re:Invent 2025 (Part 3 of 4)
**Target Duration**: 20 minutes (~3800 words)
**Date**: December 9, 2025

## Episode Summary

AWS transforms Kubernetes into an AI infrastructure platform. EKS Ultra Scale supports 100,000 nodes per cluster—enabling 1.6 million Trainium accelerators in a single cluster. EKS Capabilities brings managed Argo CD, AWS Controllers for Kubernetes, and Kube Resource Orchestrator. The EKS MCP Server lets you manage clusters with natural language instead of kubectl. CloudWatch gets generative AI observability for LangChain and CrewAI agents, while DevOps Agent acts as an autonomous on-call engineer. This is the infrastructure that will run the next generation of AI workloads.

---

## News Segment (3-4 minutes)

### Top Story: cert-manager CVE Patches
- cert-manager v1.19.2 patches CVE-2025-61727 and CVE-2025-61729
- Go standard library vulnerabilities - Trivy will flag these
- Patch now, not next sprint - no breaking changes
- v1.18.4 backport available for older branch

### Quick Hits
1. **Canonical K8s 15-Year LTS**: Ubuntu Pro + Legacy add-on, mainframe-level support cycles
2. **OpenTofu 1.11**: Ephemeral resources for secrets (no state persistence), 'enabled' meta-argument
3. **Cloudflare Shift-Left IaC**: Managing hundreds of internal accounts, preventing global misconfigurations
4. **Pulumi replaceWith**: Explicit control over replacement dependencies
5. **Go Secret Mode Proposal**: Runtime protection for sensitive values from memory dumps

---

## Part 1: EKS Ultra Scale - 100,000 Nodes (4-5 minutes)

### The Scale Challenge
- Previous limit: ~5,000 nodes (industry standard)
- New limit: 100,000 worker nodes per cluster
- Enables: 1.6 million AWS Trainium accelerators OR 800,000 NVIDIA GPUs
- Use case: Training trillion-parameter models, advancing AGI

### Technical Deep Dive: The etcd Revolution
- **Problem**: etcd consensus (Raft) becomes bottleneck at scale
- **Solution**: Replaced Raft backend with "journal" - AWS's internal component built over a decade
- **In-Memory Storage**: etcd backend moved to tmpfs
- **Results**:
  - Order-of-magnitude performance improvement
  - Higher read/write throughput
  - Predictable latencies
  - Database size doubled to 20 GB
  - 500 pods/second scheduling at 100K scale

### Real Customer Results
- **Anthropic (Claude)**: Using EKS ultra scale for frontier model training
  - End-user latency KPIs improved from average 35% to consistently above 90%
- **Amazon Nova**: Training on EKS ultra scale clusters

### Competitive Context
- AWS: 100,000 nodes/cluster
- GKE: 15,000 nodes/cluster
- AKS: 5,000 nodes/cluster
- AWS has 6-20x advantage in cluster scale

---

## Part 2: EKS Capabilities - Managed GitOps (4-5 minutes)

### What is EKS Capabilities?
- Extensible set of Kubernetes-native solutions
- Fully managed by AWS (runs in service-owned accounts)
- No more maintaining Argo CD clusters or ACK controllers
- AWS handles updates, patches, compatibility analysis

### Three Core Capabilities

#### 1. Managed Argo CD
- GitOps continuous deployment
- 45%+ of K8s users already using Argo CD (2024 CNCF Survey)
- Single Argo CD instance manages multiple clusters
- Git as source of truth - automatic drift remediation

#### 2. AWS Controllers for Kubernetes (ACK)
- Manage AWS resources with Kubernetes CRDs
- 200+ CRDs for 50+ AWS services
- Create S3 buckets, RDS databases, IAM roles from YAML
- No need to install or maintain controllers

#### 3. Kube Resource Orchestrator (KRO)
- Create reusable resource bundles
- Platform teams create abstractions
- Developers consume without understanding complexity

### Multi-Cluster Architecture Pattern
- Management cluster runs all three capabilities
- Argo CD deploys to workload clusters across regions/accounts
- ACK provisions AWS resources for all clusters
- KRO creates portable platform abstractions

### Pricing
- Per-capability, per-hour billing
- No upfront commitments
- Additional charges for managed Kubernetes resources

---

## Part 3: EKS MCP Server - Natural Language Kubernetes (3-4 minutes)

### The Vision
- Manage Kubernetes without deep expertise
- Natural language instead of kubectl
- Deploy, troubleshoot, upgrade with conversation

### What is MCP?
- Model Context Protocol - open-source standard
- Gives AI models secure access to live cluster data
- Standardized interface for contextual knowledge
- AWS among first managed K8s providers to implement

### Capabilities
- "Show me all pods not in running state"
- "Create a new EKS cluster named demo-cluster with VPC and Auto Mode"
- "Get logs from api-server pod in last 30 minutes"
- No kubectl, no kubeconfig setup required

### Enterprise Features
- Hosted in AWS cloud (no local installation)
- Automatic updates and patching
- AWS IAM integration for security
- CloudTrail integration for audit logging
- Knowledge base from millions of managed clusters

### Integration
- Works with: Kiro (IDE and CLI), Cursor, Cline
- Amazon Q Developer integration
- Build your own agents that interface with EKS

---

## Part 4: EKS Provisioned Control Plane (2-3 minutes)

### The Problem
- Standard control planes have variable performance
- Unpredictable under burst loads
- Can't guarantee SLAs for enterprise workloads

### The Solution: Pre-allocated Capacity
- T-shirt sizing: XL, 2XL, 4XL
- Well-defined performance characteristics
- Can switch tiers as workloads change

### Performance Tiers
| Tier | API Concurrency | Pod Scheduling | Database Size | Price |
|------|-----------------|----------------|---------------|-------|
| XL | Base | Base | Base | $1.65/hr |
| 2XL | Medium | Medium | Medium | ~$3.30/hr |
| 4XL | 6,800 concurrent | 400 pods/sec | 20 GB | $6.90/hr |

### 4XL Capabilities
- Up to 40,000 nodes supported
- Up to 640,000 pods
- 8x improvement over standard control planes
- Full metrics via Prometheus endpoint and CloudWatch

---

## Part 5: Cloud Operations Revolution (4-5 minutes)

### CloudWatch Generative AI Observability
- Built-in insights for AI applications and agents
- Latency, token usage, error tracking across AI stack
- Works with:
  - Amazon Bedrock AgentCore
  - LangChain, LangGraph, CrewAI
- End-to-end agent workflow tracing
- No custom instrumentation required

### AWS DevOps Agent (Preview)
- Acts as autonomous on-call engineer
- Analyzes data across: CloudWatch, GitHub, ServiceNow
- Identifies root causes automatically
- Coordinates incident response
- **Kindle team result**: 80% time savings with CloudWatch Investigations

### CloudWatch MCP Servers
- Bridge AI assistants to observability data
- Standardized access to: metrics, logs, alarms, traces, service health
- Build autonomous operational workflows
- Integrate with AI-powered development tools

### CloudWatch Unified Data Store
- Operations, security, and compliance data in one place
- Automated collection from AWS and third-party sources
- CrowdStrike, Microsoft Office 365, SentinelOne integration
- Stores in S3 Tables with OCSF and Apache Iceberg support
- Reduces data management complexity and costs

### Application Signals Enhancements
- **GitHub Action Integration**: Observability insights during PRs and CI/CD
- **Auto-Discovery**: Visualize application topology without instrumentation
- **Intelligent Grouping**: Services organized by relationships
- **Contextual Insights**: Operational data directly in map view

### Database Insights Cross-Account
- Cross-account and cross-region monitoring
- Centralized visibility across AWS organization
- Supports: Amazon RDS, Aurora, DynamoDB
- Single monitoring account for all databases

---

## Closing: The AI Infrastructure Platform (1-2 minutes)

### The Pattern
- EKS evolving from container orchestration to AI cloud platform
- Kubernetes anchoring next decade of AI infrastructure
- Every announcement focuses on AI workload enablement

### What This Means for Platform Engineers
1. **Scale is no longer a constraint**: 100K nodes opens new architecture patterns
2. **GitOps becomes turnkey**: EKS Capabilities eliminates maintenance burden
3. **Natural language ops is real**: MCP Server changes who can operate clusters
4. **Observability goes proactive**: DevOps Agent as your first line of defense

### Looking Ahead
- Part 4 of re:Invent series: Data & AI Services
- Today's infrastructure announcements set the foundation
- The question isn't whether to adopt - it's how fast

---

## Sources

### EKS Announcements
- [Amazon EKS enables ultra scale AI/ML workloads with support for 100K nodes](https://aws.amazon.com/blogs/containers/amazon-eks-enables-ultra-scale-ai-ml-workloads-with-support-for-100k-nodes-per-cluster/)
- [Announcing Amazon EKS Capabilities](https://aws.amazon.com/blogs/aws/announcing-amazon-eks-capabilities-for-workload-orchestration-and-cloud-resource-management/)
- [Amazon EKS introduces Provisioned Control Plane](https://aws.amazon.com/blogs/containers/amazon-eks-introduces-provisioned-control-plane/)
- [Introducing the fully managed Amazon EKS MCP Server](https://aws.amazon.com/blogs/containers/introducing-the-fully-managed-amazon-eks-mcp-server-preview/)

### Cloud Operations
- [2025 Top 10 Announcements for AWS Cloud Operations](https://aws.amazon.com/blogs/mt/2025-top-10-announcements-for-aws-cloud-operations/)
- [Embracing AI-driven operations and observability at re:Invent 2025](https://aws.amazon.com/blogs/mt/embracing-ai-driven-operations-and-observability-at-reinvent-2025/)

### News Segment
- [cert-manager v1.19.2 Release](https://github.com/cert-manager/cert-manager/releases/tag/v1.19.2)
- [Canonical Extends Kubernetes Long-Term Support to 15 Years](https://thenewstack.io/canonical-extends-kubernetes-long-term-support-to-15-years/)
- [OpenTofu 1.11 Release](https://github.com/opentofu/opentofu/releases/tag/v1.11.0)

---

## Episode Navigation

- **Previous Episode**: [Episode #050: AWS re:Invent 2025 - Infrastructure & Developer Experience](/podcasts/00050-aws-reinvent-2025-infrastructure-developer-experience) (Part 2 of 4)
- **Next Episode**: Episode #052: AWS re:Invent 2025 - Data & AI Services (Part 4 of 4)
