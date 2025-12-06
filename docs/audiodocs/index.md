---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎧 AudioDocs"
slug: /audiodocs
---

# AudioDocs - Listen to Documentation

<GitHubButtons />

**AudioDocs** transforms official project documentation into high-quality audio content you can listen to while commuting, exercising, or doing chores. Learn platform engineering tools by ear.

Each AudioDocs episode is version-specific, so you always know exactly which release the documentation covers. When a new version drops, we'll publish a fresh AudioDocs episode to keep you current.

**Format**: Single-presenter educational audio, ~10-75 minutes depending on documentation depth

---

## Available Tools

<details>
<summary><strong>CoreDNS</strong> - Kubernetes DNS Server (CNCF Graduated)</summary>

CoreDNS is a flexible, extensible DNS server that serves as the default DNS provider for Kubernetes clusters. Built on a plugin architecture, it handles service discovery, external DNS resolution, and custom DNS policies.

| Version | Duration | Released | AudioDocs |
|---------|----------|----------|-----------|
| [v1.13.1](/audiodocs/coredns/v1.13.1) | 72 min | October 2025 | ✅ Available |

**Topics Covered**: Plugin architecture, Corefile configuration, Kubernetes integration, caching, forwarding, health checks, metrics, DNS security (DNSSEC, DNS over TLS), and 15+ essential plugins explained.

</details>

<details>
<summary><strong>kubectx / kubens</strong> - Kubernetes Context & Namespace Switcher</summary>

kubectx and kubens are essential CLI tools for anyone working with multiple Kubernetes clusters or namespaces. Switch contexts and namespaces instantly with tab completion and fuzzy search.

| Version | Duration | Released | AudioDocs |
|---------|----------|----------|-----------|
| [v0.9.5](/audiodocs/kubectx/v0.9.5) | 10 min | September 2023 | ✅ Available |

**Topics Covered**: Installation, basic usage, fuzzy finder integration (fzf), shell completion, aliases, tips and tricks for multi-cluster workflows.

</details>

---

## Coming Soon

We're actively working on AudioDocs for these tools:

- **Helm** - Kubernetes Package Manager
- **ArgoCD** - GitOps Continuous Delivery
- **Prometheus** - Monitoring & Alerting
- **Terraform** - Infrastructure as Code

---

## How It Works

1. **Source**: We parse official project documentation from GitHub releases
2. **Script**: AI transforms docs into educational audio scripts optimized for listening
3. **Validation**: Scripts are fact-checked against source documentation
4. **Audio**: Generated using Gemini 2.5 TTS with the Algieba voice
5. **Video**: MP4 versions available for YouTube with visual background

All scripts are open source. Find issues? [Open a PR on GitHub](https://github.com/vibesre/Platform-Engineering-Playbook).

---

## Subscribe

AudioDocs are published as part of the Platform Engineering Playbook content. Subscribe to stay updated:

<PodcastSubscribeButtons />
