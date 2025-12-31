---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #075: Security Ops Specialty"
slug: 00075-security-ops-specialty-platform-engineers
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #075: Security Ops Specialty: The Underrated Skill Every Platform Engineer Needs in 2026

<GitHubButtons />

**Duration**: 19 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Platform engineers, SREs, DevOps professionals

<iframe width="100%" style={{aspectRatio: '16/9', marginBottom: '1rem'}} src="https://www.youtube.com/embed/bBxogTsOrd8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

> 📰 **News Segment**: This episode covers 3 platform engineering news items before the main topic.

## News Segment

| Story | Source | Why It Matters |
|-------|--------|----------------|
| [Kubernetes Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) | Kubernetes SIGs | Open-source controller for securely running AI-generated code on K8s using gVisor isolation |
| [Backstage 2025 Year in Review](https://backstage.io/blog/2025/12/20/backstage-2025-wrapped/) | Backstage | 3.4K adopters, 89% IDP market share, 250+ plugins, new frontend system adoption-ready |
| [API Key/Certificate Expiry Management](https://www.reddit.com/r/devops/comments/xxxx) | Reddit | Organizations still tracking credentials manually; highlights need for secrets lifecycle automation |

---

Platform engineers who understand security operations—secrets management, vulnerability scanning, and compliance automation—are commanding premium salaries in 2026. This episode breaks down the security ops specialty: what it includes, why organizations are desperate for it, and how to build these skills alongside your existing platform engineering expertise.

## The Five Security Ops Domains

| Domain | Key Tools | What Platform Engineers Do |
|--------|-----------|---------------------------|
| **Supply Chain Security** | Sigstore, Trivy, Grype, SLSA | Sign/verify container images, scan vulnerabilities, generate SBOMs |
| **Secrets Management** | HashiCorp Vault, SOPS, AWS Secrets Manager | Dynamic secrets, automatic rotation, audit trails |
| **Runtime Security** | Falco, eBPF, gVisor, seccomp | Detect anomalies, enforce policies at runtime |
| **Identity & Access** | SPIFFE, SPIRE | Workload identity, zero-trust networking |
| **Compliance as Code** | OPA, Gatekeeper, Kyverno | Policy enforcement, automated compliance |

## Supply Chain Security Deep Dive

### Sigstore Architecture

| Component | Purpose |
|-----------|---------|
| **Cosign** | Container image signing with keyless signatures tied to OIDC identity |
| **Rekor** | Transparency log recording every signature (like Certificate Transparency) |
| **Fulcio** | Certificate authority issuing short-lived certificates (10 min) |
| **Policy Controller** | Kubernetes admission webhook validating signatures before pod creation |

**Key insight**: No long-lived private keys to manage. Your identity provider (GitHub, Google, corporate OIDC) is the root of trust.

## Secrets Management with Vault

### Dynamic Secrets Flow

1. Pod authenticates to Vault using Kubernetes service account token
2. Vault validates token against K8s API
3. Vault creates temporary database credential (1-hour expiry)
4. Pod receives credential; Vault logs access with full audit trail
5. No static credentials exist; rotation is automatic

**Platform engineering approach**: Secrets as a platform capability—developers request through API/portal, platform provisions short-lived, auto-rotating secrets tied to workload identity.

## Runtime Security with eBPF

### How Falco Works

| Step | Description |
|------|-------------|
| **Hook** | eBPF probes attach to system calls |
| **Capture** | Every file open, network connection, command execution captured with context |
| **Context** | Process hierarchy, container ID, K8s metadata included |
| **Evaluate** | Rules detect anomalies (shell in container, unexpected network, credential access) |
| **Alert** | Send to Slack, PagerDuty, or trigger K8s response (kill pod) |

### Example Detection Rule

Detect shell spawned in container:
- Watch for `execve` syscalls where process is bash/sh/zsh
- Filter where container ID is not host
- Add exceptions for legitimate debug sidecars

## Policy as Code with OPA/Gatekeeper

### How It Works

1. Gatekeeper admission controller intercepts K8s resource creation
2. Sends request to OPA with full object and context
3. OPA evaluates policies written in Rego
4. If violation found, Gatekeeper rejects with violation message
5. Policies stored as K8s CRDs—version-controlled like any config

**What you can enforce**: Network segmentation, security contexts, resource configs, encryption at rest, access patterns.

## Skill Building Path

| Phase | Focus | Actions |
|-------|-------|---------|
| **Start** | Supply Chain Security | Add Trivy scanning to CI, implement Sigstore signing, understand SBOMs |
| **Foundation** | Policy as Code | Write OPA policies for admission controllers, learn Rego |
| **Intermediate** | Secrets Management | Implement Vault with dynamic secrets, understand PKI/certificate rotation |
| **Advanced** | Identity & Access | Deploy SPIFFE/SPIRE for workload identity |
| **Expert** | Runtime Security | Falco deployment, eBPF programming for observability |

## Quick Wins for This Week

1. **Add Trivy scanning** to one CI pipeline (~1 hour)
2. **Write one OPA policy** for K8s (e.g., require resource limits, disallow privileged containers)
3. **Deploy Falco in audit mode** on non-production cluster—observe what it detects

## Salary Impact

| Skill Combination | Premium |
|-------------------|---------|
| Platform Engineering alone | Baseline |
| Platform Engineering + Security Ops | 10-20% higher |

**Key insight**: Many security engineers lack platform/infrastructure depth. Many platform engineers lack security depth. Bridging that gap is career gold.

## Certifications

| Certification | Focus |
|---------------|-------|
| **CKS** (Certified Kubernetes Security Specialist) | Covers many of these areas in K8s context |
| **HashiCorp Vault Associate** | Secrets management fundamentals |
| **SANS Cloud Security** | Comprehensive but expensive |

**Reality check**: Hands-on experience matters most. Build a lab, implement these tools, break things, fix them.

## Key Takeaways

1. **Platform is the new perimeter**—you're responsible for security posture of everything you provision
2. **Five domains to master**: Supply chain, secrets, runtime, identity, compliance as code
3. **Sigstore enables keyless signing**—OIDC identity as root of trust
4. **Vault dynamic secrets** eliminate static credentials and manual rotation
5. **eBPF/Falco** detect threats in real-time at kernel level
6. **OPA/Gatekeeper** codify compliance requirements as enforceable policies
7. **Start with Trivy + one OPA policy**—quick wins with visible impact

## Resources

- [Sigstore](https://sigstore.dev/)
- [HashiCorp Vault](https://www.vaultproject.io/)
- [Falco](https://falco.org/)
- [Open Policy Agent](https://www.openpolicyagent.org/)
- [SPIFFE/SPIRE](https://spiffe.io/)
- [Trivy](https://trivy.dev/)
- [Kubernetes Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox)

## Related Episodes

- [Episode #072: Platform Engineering Salary Report 2026](/podcasts/00072-platform-engineering-salary-skills-2026)
- [Episode #066: CNPE Certification Study Guide](/podcasts/00066-cnpe-certification-study-guide)
- [Episode #063: Docker Hardened Images](/podcasts/00063-docker-hardened-images-free-security)
- [Episode #074: Agentic AI Foundation & MCP](/podcasts/00074-agentic-ai-foundation-mcp-platform-engineers)
