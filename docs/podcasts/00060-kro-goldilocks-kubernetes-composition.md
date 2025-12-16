---
title: "Episode #060: Helm Is Too Simple. Crossplane Is Too Complex. Is kro Just Right?"
description: "The Goldilocks problem of Kubernetes composition tools. Decision framework for evaluating kro vs Crossplane vs Helm, plus clearing up the kro/krew confusion."
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #060: kro Goldilocks Guide"
slug: 00060-kro-goldilocks-kubernetes-composition
---

import GitHubButton from 'react-github-btn';

# Episode #060: Helm Is Too Simple. Crossplane Is Too Complex. Is kro Just Right?

<GitHubButton href="https://github.com/platformengplaybook/platform-engineering-playbook" data-icon="octicon-star" data-size="large" data-show-count="true" aria-label="Star platformengplaybook/platform-engineering-playbook on GitHub">Star</GitHubButton>

**Duration**: ~22 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Senior Platform Engineers, DevOps leads evaluating composition tools

<iframe width="100%" style={{aspectRatio: "16/9"}} src="https://www.youtube.com/embed/HjeAlyl5_9U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

## News Segment

### Story 1: Shai-Hulud npm Supply Chain Attack Postmortem
Trigger.dev published the complete postmortem of the Shai-Hulud 2.0 attack - 500+ npm packages compromised, 25,000+ repositories affected. Key defenses: `npm config set ignore-scripts true`, pnpm 10's minimumReleaseAge feature.

- [Trigger.dev Postmortem](https://trigger.dev/blog/shai-hulud-postmortem)

### Story 2: Ingress-nginx Retirement Countdown
March 2026 deadline now just 3 months away. Community actively debating alternatives: Envoy Gateway, F5 NGINX Ingress Controller, Traefik.

### Story 3: Netflix Maestro 100x Faster
Full rewrite achieved 100x performance improvement by removing complex internal databases. Sometimes clean slate beats incremental optimization.

- [Netflix Tech Blog](https://netflixtechblog.com/100x-faster-how-we-supercharged-netflix-maestros-workflow-engine-028e9637f041)

---

## The Goldilocks Problem

**48% of Kubernetes users struggle with tool choice** (up from 29% in 2023). This episode provides a decision framework for the composition tool landscape.

### Clearing Up the Confusion

**kro vs krew - COMPLETELY DIFFERENT TOOLS:**

| Tool | What It Does |
|------|--------------|
| **krew** (K-R-E-W) | kubectl plugin manager (like apt/brew for kubectl) |
| **kro** (K-R-O) | Kubernetes Resource Orchestrator (resource composition) |

Other K-tools: Kratix (multi-cluster orchestration), Kustomize (config overlays), Kyverno (policy engine)

---

## The Three Bears of Kubernetes Composition

### Helm (Too Simple?)
- Template engine, not runtime controller
- Renders once, walks away
- No continuous reconciliation
- **Best for**: Simple deployments, established patterns
- **Falls short**: Dynamic configuration, runtime guarantees

### Crossplane (Too Complex?)
- Full cloud resource provisioning (50+ providers)
- Multi-cloud support
- Steep learning curve
- Two abstractions: CompositeResourceDefinition + Composition
- **Best for**: Cloud resources, multi-cloud strategies
- **Falls short**: Teams just needing K8s-native composition

### kro (Just Right?)
- Single-cluster, K8s-native composition
- One abstraction: ResourceGraphDefinition
- CEL for dynamic configuration
- Continuous reconciliation
- **Best for**: K8s composition without cloud provisioning
- **Falls short**: Multi-cluster, cloud resources, approval workflows

---

## Decision Framework

```
Do you need to provision cloud resources (RDS, S3, etc.)?
├── YES → Use Crossplane or ACK
└── NO → Continue...

Do you need multi-cluster orchestration?
├── YES → Use Kratix
└── NO → Continue...

Do you need approval workflows or external integrations?
├── YES → Look elsewhere (Backstage, custom)
└── NO → Continue...

Do you need continuous reconciliation?
├── NO → Helm or Kustomize are fine
└── YES → kro is a good fit
```

---

## Honest Assessment

Viktor Farcic's criticism: "kro is serving more or less the same function as other tools created a while ago without any compelling improvement."

**Our take**: Fair criticism. kro isn't revolutionary. But it fills a specific gap:
- Simpler than Crossplane when you don't need cloud provisioning
- More powerful than Helm when you need runtime reconciliation
- The middle ground tool that was missing

**Current status**: Alpha (v1alpha1) - wait for v1.0 for production workloads.

---

## Episode Transcript

**Jordan**: Today we're tackling a question that 48 percent of Kubernetes users are struggling with right now. How do you choose the right composition tool when there are so many options? Helm, Crossplane, kro, Kratix, Kustomize. The tool fatigue is real, and it's crushing platform teams.

**Alex**: And that 48 percent figure isn't hyperbole. It's from Spectro Cloud's 2024 survey, up from 29 percent just a year before. The problem is getting worse, not better. But before we dive into the Goldilocks problem of Kubernetes composition, let's cover this week's news.

**Jordan**: Our first story is a sobering one. Trigger.dev published the complete postmortem of the Shai-Hulud 2.0 supply chain attack. Over 500 npm packages compromised, affecting more than 25,000 repositories.

**Alex**: The timeline is what stands out. The attackers spent 17 hours doing reconnaissance before launching just 10 minutes of actual destruction. That reconnaissance-to-action ratio tells you how much planning goes into these attacks.

**Jordan**: The defensive recommendations are practical. Set npm config to ignore scripts by default. Use pnpm 10's new minimum release age feature, which gives the community time to detect malicious packages before your build systems pull them. And implement OIDC publishing for your own packages.

**Alex**: Next up, the ingress-nginx retirement discussion is intensifying. The March 2026 deadline is now just three months away, and teams are actively debating alternatives on Reddit.

**Jordan**: Envoy Gateway, F5 NGINX Ingress Controller, and Traefik seem to be the top contenders. If you haven't started migration planning yet, now is the time. Three months goes fast when you're coordinating infrastructure changes across multiple teams.

**Alex**: And finally, Netflix published a fascinating engineering post about making their Maestro workflow engine 100 times faster. Not 10 percent faster. One hundred times faster.

**Jordan**: The key insight is that they achieved this through a full rewrite, removing complex internal databases that had accumulated over years. It's a reminder that sometimes the right answer is a clean slate rather than incremental optimization. Technical debt compounds.

**Alex**: Alright, let's get into our main topic. Helm is too simple. Crossplane is too complex. Is kro just right? It's the Goldilocks problem of Kubernetes composition.

**Jordan**: And before we go any further, let's clear up a confusion I see constantly. kro and krew are completely different tools. They sound similar, they're both from Kubernetes SIGs, but they solve entirely different problems.

**Alex**: krew, spelled K-R-E-W, is a kubectl plugin manager. Think of it like apt or Homebrew, but for kubectl. It has over 180 plugins available. You run kubectl krew install, then the plugin name. It has nothing to do with resource composition.

**Jordan**: kro, spelled K-R-O, is the Kube Resource Orchestrator. It's a resource composition tool that creates custom APIs from resource bundles. It does continuous reconciliation. It's a SIG Cloud Provider project. Completely different purpose.

**Alex**: And while we're at it, let's distinguish a few other K-tools people confuse. Kratix is for multi-cluster platform orchestration using Promises. Kustomize is overlay-based configuration customization with no runtime component. Kyverno is a policy engine. None of these are interchangeable.

**Jordan**: Now, the Goldilocks problem. Let's start with Helm, which some would say is too simple. Helm is a template engine. It's not a runtime controller. It renders your templates at install time and then walks away. There's no continuous reconciliation.

**Alex**: That's fine for many use cases. Simple deployments, established patterns, teams that don't need runtime guarantees. But when you need dynamic configuration that responds to changes, or you need to ensure your resources stay in the desired state, Helm falls short.

**Jordan**: On the other end of the spectrum is Crossplane. Full cloud resource provisioning. Over 50 providers covering AWS, GCP, Azure, databases, DNS, you name it. Multi-cloud strategies are where Crossplane shines.

**Alex**: But the learning curve is steep. You need to understand CompositeResourceDefinitions and Compositions. That's two abstractions just to create a custom API. And for teams that just need Kubernetes-native composition without cloud provisioning, Crossplane can feel like bringing a crane to hang a picture frame.

**Jordan**: Which brings us to kro. Is it just right? Well, it depends. And I know that's an unsatisfying answer, but it's the honest one.

**Alex**: kro focuses on single-cluster, Kubernetes-native composition. It uses a single abstraction called ResourceGraphDefinition to bundle multiple resources behind one custom API. Less boilerplate than Crossplane. Runtime reconciliation that Helm doesn't have.

**Jordan**: It uses CEL, the Common Expression Language, for dynamic configuration. You can transform user inputs in complex ways without writing custom controllers. And it stays in its lane. No cloud provisioning. No multi-cluster orchestration. Just Kubernetes resource composition done well.

**Alex**: But here's where we need to be honest. Viktor Farcic, a well-known voice in the DevOps community, tested kro and had criticisms. He called it, quote, "serving more or less the same function as other tools created a while ago without any compelling improvement."

**Jordan**: He found specific issues. Missing default values and owner references. Changes from ResourceGroups not propagating properly to existing resources. YAML limitations leading to what he called "abominations."

**Alex**: His conclusion was that kro currently provides only a fraction of Crossplane's features and isn't yet a viable replacement. And honestly? That's fair criticism.

**Jordan**: kro isn't revolutionary. It's not trying to be. It fills a specific gap. Simpler than Crossplane when you don't need cloud provisioning. More powerful than Helm when you need runtime reconciliation. The middle ground tool that was missing.

**Alex**: Now here's what made news this month. AWS adopted kro into EKS Capabilities alongside Argo CD and AWS Controllers for Kubernetes. That's significant because AWS, Google, and Microsoft all co-developed kro. Three competing cloud providers agreeing on a tool is rare.

**Jordan**: The EKS Capabilities model is interesting architecturally. These tools run in AWS service-owned accounts, not in your clusters. AWS manages scaling, patching, and updates. You pay for what you use with no minimum fees. It's the serverless model applied to cluster add-ons.

**Alex**: And the implied architecture here is telling. Crossplane or ACK for cloud resources. kro for Kubernetes composition. Kyverno or OPA for policy. Argo CD or Flux for delivery. The Unix philosophy: tools that do one thing well and work together.

**Jordan**: So let's get practical. Here's a decision framework. First question: do you need to provision cloud resources like RDS databases or S3 buckets? If yes, use Crossplane or ACK. kro can't help you there.

**Alex**: Second question: do you need multi-cluster orchestration? If yes, look at Kratix. kro is single-cluster only.

**Jordan**: Third question: do you need approval workflows or external integrations like ServiceNow? If yes, that's not kro's domain. Look at Backstage or custom solutions.

**Alex**: Fourth question: do you need continuous reconciliation, or is install-time templating enough? If install-time is fine, Helm or Kustomize work great. If you need runtime reconciliation, now kro becomes a good fit.

**Jordan**: When should you use kro? Single-cluster Kubernetes composition. Developer self-service portals. Encoding organizational standards into reusable APIs. Teams that find Crossplane overwhelming but need more than Helm provides.

**Alex**: When should you not use kro? Cloud resource provisioning. Multi-cluster orchestration. Approval workflows. And honestly, production workloads today. kro is still at v1alpha1. Wait for v1.0 before betting critical systems on it.

**Jordan**: So back to our original question. Helm is too simple. Crossplane is too complex. Is kro just right? The answer is: it depends on your Goldilocks zone.

**Alex**: If you're in that sweet spot, single-cluster, Kubernetes-native, runtime reconciliation needed but no cloud provisioning, then yes, kro might be just right for you.

**Jordan**: If you need cloud provisioning or multi-cluster capabilities, kro alone won't help. You'll still need Crossplane or other tools in the mix.

**Alex**: And if Helm is working fine for your team, don't switch just because AWS adopted something new. The right tool is the one that solves your actual problem, not the one with the most hype.

**Jordan**: Here's the takeaway. Map your actual requirements honestly. Start with the simplest tool that meets them. kro sits at middle complexity with middle power. Don't adopt tools because cloud providers do. Adopt them because they solve your problem.

**Alex**: The Kubernetes tool ecosystem will continue to expand. 70 percent of survey respondents expect consolidation, but we're not there yet. The key is having a framework for evaluation, not chasing every new tool that gets cloud provider attention.

**Jordan**: Check the show notes for links to the kro GitHub repo, the CNCF blog post on platform design principles, the AWS EKS Capabilities announcement, and Viktor Farcic's critical analysis. All valuable reading for platform engineers navigating this landscape.

**Alex**: And remember: nearly half of Kubernetes users struggle with tool choice. Having a clear decision framework puts you ahead of the majority. The Goldilocks approach, understanding when tools are too simple, too complex, or just right for your needs, is how you cut through the noise.

**Jordan**: The platform engineering discipline continues to mature. Tools like kro represent that maturation, purpose-built components that stay in their lane and compose with others. That's the Unix philosophy applied to infrastructure, and it's a pattern worth embracing.

---

## Resources

- [kro GitHub Repository](https://github.com/kubernetes-sigs/kro) - 2,600+ stars, 87 contributors
- [CNCF Blog: Building Platforms Using kro](https://www.cncf.io/blog/2025/12/15/building-platforms-using-kro-for-composition/)
- [AWS EKS Capabilities Announcement](https://aws.amazon.com/blogs/aws/announcing-amazon-eks-capabilities-for-workload-orchestration-and-cloud-resource-management/)
- [Google Cloud Blog: Introducing kro](https://cloud.google.com/blog/products/containers-kubernetes/introducing-kube-resource-orchestrator)
- [InfoQ: Cloud Giants Collaborate on kro](https://www.infoq.com/news/2025/02/kube-resource-orchestrator/) - includes Viktor Farcic's analysis
- [krew - kubectl plugin manager](https://krew.sigs.k8s.io/) - different tool!
- [Spectro Cloud Survey: 48% Tool Choice Struggle](https://thenewstack.io/kubernetes-48-of-users-struggle-with-tool-choice/)
- [Trigger.dev Shai-Hulud Postmortem](https://trigger.dev/blog/shai-hulud-postmortem)
- [Netflix Maestro 100x Faster](https://netflixtechblog.com/100x-faster-how-we-supercharged-netflix-maestros-workflow-engine-028e9637f041)
