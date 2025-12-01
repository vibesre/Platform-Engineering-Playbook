---
title: "Episode #042: Helm 4 Deep Dive - The Complete Guide to the Biggest Update in 6 Years"
description: "A comprehensive guide to Helm 4.0: Server-Side Apply, WebAssembly plugins, breaking changes, migration timelines, and how it compares to Kustomize and alternatives."
slug: 00042-helm-4-comprehensive-guide
sidebar_label: "🎙️ #042: Helm 4 Deep Dive"
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #042: Helm 4 Deep Dive - The Complete Guide to the Biggest Update in 6 Years

<GitHubButtons />

**Duration**: 24 minutes

**Speakers**: Jordan (Kore) and Alex (Algieba)

**Target Audience**: Platform engineers, SREs, DevOps engineers using Helm

> 📝 **Read the [comprehensive blog post](/blog/helm-4-release-server-side-apply-wasm-plugins-migration-guide-2025)**: Complete migration guide with breaking changes inventory, comparison tables, and step-by-step checklists.

---

## Watch the Episode

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube.com/embed/qYuDY3AWBOg" title="Episode #042: Helm 4 Deep Dive - The Complete Guide to the Biggest Update in 6 Years" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

---

## Episode Summary

Helm 4.0.0 dropped at KubeCon Atlanta on November 12, 2025—the first major version in six years. This extended deep-dive episode covers everything platform engineers need to know: the technical details of Server-Side Apply, the WebAssembly plugin revolution, every breaking change categorized by impact, how Helm 4 compares to Kustomize and alternatives, and a detailed 12-week migration guide.

---

## Key Topics

- **The 6-Year Journey**: Why Helm 4 took so long (SSA maturity, GitOps coordination, plugin security)
- **Server-Side Apply Deep Dive**: How SSA replaces three-way merge, managedFields explained, performance gains
- **WebAssembly Plugins**: The kstatus plugin, Extism runtime, migration from Go binaries
- **Complete Breaking Changes**: High/Medium/Low impact changes with migration steps
- **Helm 4 vs Alternatives**: Comparison with Kustomize, Carvel, and Jsonnet
- **12-Week Migration Guide**: Phase-by-phase rollout with common errors to avoid
- **Community Sentiment**: Early adopter feedback and adoption timeline predictions

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Helm adoption | 75-87% | CNCF Annual Survey 2024 |
| Time since Helm 3 | 6 years | Nov 2019 to Nov 2025 |
| SSA performance gain | 40-60% faster | Kubernetes SIG-CLI benchmarks |
| Helm 3 support | Until Nov 2026 | helm.sh official |
| GitHub stars | 28,000+ | github.com/helm/helm |
| Chart ecosystem | 20,000+ | Artifact Hub |

---

## Episode Transcript

**Jordan**: Today we're doing something different. This is an extended deep-dive episode because two weeks ago at KubeCon Atlanta, Helm 4.0 dropped. And this isn't just any update. It's the first major version in six years. Six years, Alex. That's longer than some Kubernetes clusters have been running.

**Alex**: And we're not exaggerating the importance here. Helm powers somewhere between 75 and 87 percent of Kubernetes deployments according to the CNCF's 2024 survey. It's the de facto standard for packaging applications. So when Helm makes a major change, platform teams everywhere need to pay attention.

**Jordan**: Exactly. So in this episode, we're covering everything. The six-year journey from Helm 3. A technical deep-dive into Server-Side Apply. The WebAssembly plugin revolution. Every breaking change you need to know about. How Helm 4 compares to alternatives. And a detailed migration guide with timelines.

**Alex**: Let's start at the beginning. Why did Helm 4 take six years? To understand that, we need to walk through the full Helm history.

**Jordan**: Helm was created in 2015 by a company called Deis, which was later acquired by Microsoft. In 2016, Helm 2 introduced Tiller, that infamous in-cluster component that gave everyone security nightmares.

**Alex**: Oh, Tiller. For those who don't remember, Tiller was a server-side component that ran inside your cluster with effectively cluster-admin privileges. It was a security audit's worst nightmare. Every security team hated it.

**Jordan**: Then in 2018, Helm became a CNCF incubating project. And in November 2019, Helm 3.0 finally removed Tiller. That was a massive migration. Some teams took years to move from Helm 2 to Helm 3 because Tiller was so deeply embedded in their workflows.

**Alex**: And that experience taught the Helm maintainers something important. Breaking changes need to be worth the pain. You can't just ship breaking changes for minor improvements. The value has to justify the migration cost.

**Jordan**: From 2020 to 2024, we got incremental Helm 3.x releases. Improvements here and there. And then on November 12th, 2025, at KubeCon Atlanta, Helm 4.0 landed. Exactly ten years after Helm was created.

**Alex**: So why six years between major versions? Three main reasons. First, Server-Side Apply needed to mature. SSA hit general availability in Kubernetes 1.22 in August 2021, but the ecosystem needed time to adopt consistent patterns.

**Jordan**: Second, coordination with GitOps tools. ArgoCD and Flux both adopted SSA before Helm did. The maintainers wanted Helm's implementation to work seamlessly with existing GitOps workflows, not create new conflicts.

**Alex**: And third, plugin security. The old post-renderer model allowed arbitrary binary execution. That's a security nightmare. Designing and implementing the WebAssembly sandbox took time, but it was necessary.

**Jordan**: Now let's talk about the headline feature. Server-Side Apply. This is the change that will affect every single Helm user, and it's fundamentally good news.

**Alex**: To understand why SSA matters, we need to explain what it replaces. Helm 3 used something called three-way merge. Here's how it worked. When you ran helm upgrade, Helm would fetch the current resource state from the API server. Then it would read the last-applied-configuration annotation. Then it would calculate the diff between your desired state, the current state, and what was previously applied. Finally, it would apply that diff.

**Jordan**: The problem is that last-applied-configuration annotation. It only tracks what the last apply set. It doesn't track who owns which fields. If another tool, like ArgoCD or kubectl or an HPA, modifies the resource, Helm doesn't know which fields belong to whom.

**Alex**: This created the infamous GitOps war story that played out in organizations everywhere. Picture this scenario. A platform team configures ArgoCD to use Server-Side Apply by default, which is the modern best practice. A developer runs helm upgrade to deploy a hotfix.

**Jordan**: ArgoCD's next reconciliation loop runs. It looks at the resource and sees "drift." Fields have changed outside of Git. Alerts fire. The developer asks "who changed my deployment?" And the answer is... nobody really did. The tools were fighting over field ownership.

**Alex**: I've seen this exact scenario cause hours of debugging. Teams would think they had a rogue process modifying resources. They'd check audit logs, review RBAC, investigate service accounts. All because Helm and ArgoCD couldn't agree on who owned which fields.

**Jordan**: Server-Side Apply fixes this completely. Here's how it works. Instead of tracking changes in a client-side annotation, SSA tracks field ownership at the API server level. There's a new metadata field called managedFields that shows exactly who owns what.

**Alex**: So when Helm applies a resource with SSA, it declares "I'm the helm manager, and I own these specific fields." When ArgoCD reconciles, it declares "I'm argocd-controller, and I own these fields." When an HPA scales the deployment, it takes ownership of the replicas field.

**Jordan**: Everyone respects each other's boundaries. If Helm tries to modify a field owned by another manager, the API server can detect the conflict and either reject it or require a force override.

**Alex**: Let me walk through what managedFields actually looks like. It's a list in the resource metadata. Each entry has a manager name, the operation type, and a fieldsV1 structure that shows exactly which fields that manager owns.

**Jordan**: So you might see helm owning the labels, the container specs, and the image tags. ArgoCD owning the replicas count. And the HPA owning observed metrics. Clear boundaries, no confusion.

**Alex**: This brings us to performance. SSA isn't just about correctness. It's also faster.

**Jordan**: With three-way merge, Helm makes at least two API calls per resource. A GET to fetch the current state, then a PATCH or PUT to apply changes. For a release with 50 resources, that's at least 100 API calls.

**Alex**: With SSA, Helm makes one API call per resource. A PATCH with the full object. 50 resources equals 50 API calls. That's half the API traffic.

**Jordan**: In practice, teams report 40 to 60 percent faster deployment times. At scale, when you're deploying hundreds of releases per day, that adds up to hours of saved time and significantly reduced API server load.

**Alex**: And there's another benefit. SSA makes dry-run more accurate because it actually simulates the apply on the server side, not just the client side.

**Jordan**: Now let's talk about the change that's causing the most migration pain. WebAssembly plugins. This is the highest-friction breaking change in Helm 4.

**Alex**: Let me explain what post-renderers were and why they're being replaced. In Helm 3, you could specify a post-renderer, which was an executable that would receive the rendered manifests on stdin and output modified manifests on stdout. People used this for all sorts of things. Adding labels, injecting sidecars, transforming resources.

**Jordan**: The problem is that "executable" meant any binary. A shell script. A Go program. A Python script. Whatever you wanted to run. No sandboxing. Full access to the host filesystem. Full network access. Full access to environment variables.

**Alex**: From a security perspective, this was terrifying. If you pulled a Helm chart from an untrusted source and it specified a post-renderer, that renderer could do anything. Exfiltrate secrets. Download malware. Phone home to a command and control server.

**Jordan**: Helm 4 replaces this with WebAssembly plugins using the Extism runtime. WASM modules run in a sandbox. They have no filesystem access unless explicitly granted. No network access unless explicitly granted. They're portable across operating systems. And they can be distributed via OCI registries alongside your charts.

**Alex**: This is objectively better for security. But here's the migration pain. If you have custom post-renderers, they need to be rewritten. Your shell scripts won't work. Your Go binaries won't work. Everything needs to become a WASM module.

**Jordan**: Let's talk about what you need to do if you have post-renderers. First, audit your existing post-renderers. What do they actually do? Some might be simple, like adding a label to every resource. Others might be complex, like calling external APIs or performing cryptographic operations.

**Alex**: Second, choose an implementation language. Extism supports multiple languages. Rust gives you the best performance but has a steeper learning curve. Go is familiar to Kubernetes teams and has good Extism support. JavaScript is easiest for simple transformations.

**Jordan**: Third, implement and test. The Extism documentation is good, but expect a learning curve. WASM has different constraints than native code. You'll need to think about memory management differently.

**Alex**: Fourth, distribute via OCI. Your plugins should be pushed to an OCI registry so they can be pulled alongside charts. This creates a clean supply chain where everything comes from the same trusted registry.

**Jordan**: Now, there's one official Helm 4 plugin that demonstrates the value of this system. It's called kstatus. Before, when you ran helm install with the --wait flag, Helm would only check that resources existed in the API server. Pod created? Great, we're done. But the pod might be crash-looping. The service might have no endpoints.

**Alex**: With the kstatus plugin, you can add annotations to your resources. helm.sh/readiness-success specifies a condition that must be true for the resource to be considered ready. helm.sh/readiness-failure specifies conditions that mean the resource has failed.

**Jordan**: Helm now waits for actual readiness, not just existence. This catches the entire category of "deployment succeeded but nothing works" problems.

**Alex**: Let's go through all the breaking changes systematically. We'll categorize them by impact level.

**Jordan**: High impact changes first. Number one, post-renderers require WASM. We just covered this. Your Go binaries and shell scripts will not work with Helm 4.

**Alex**: Number two, Server-Side Apply behavioral differences. SSA is more strict about field ownership. Some patterns that worked with three-way merge will fail. Controllers that assume they own all fields will have problems. Operators that patch resources without declaring ownership will conflict.

**Jordan**: Number three, annotation changes. The last-applied-configuration annotation is no longer used. Any tooling that parses this annotation needs to migrate to using managedFields instead.

**Alex**: Medium impact changes. Number one, CLI flag renames. The --dry-run flag now defaults to server mode, not client mode. If you were using --dry-run and relying on client-side behavior, you need to explicitly specify --dry-run=client.

**Jordan**: The --force flag is renamed to --force-replace to clarify what it actually does. Your CI/CD pipelines need to be updated.

**Alex**: Number two, the plugin SDK is restructured. Third-party plugins built on the Helm 3 SDK may not work. Before assuming your plugins work, check with the plugin maintainers for Helm 4 compatibility.

**Jordan**: Number three, deprecated APIs are removed. Legacy v3 APIs that were deprecated in earlier releases are now gone. Chart developers using deprecated fields need to update.

**Alex**: Low impact changes that are still notable. Content-based caching now uses hash-based caching instead of version-based. This eliminates cache collisions when you reuse chart versions with different content, which is common in development.

**Jordan**: OCI digest support. You can now reference charts by digest, not just tag. helm install myapp oci://registry.example.com/charts/myapp@sha256... This is important for supply chain security because digest references are immutable.

**Alex**: Multi-document values files. You can now have multiple YAML documents in a single values file. This enables cleaner organization of complex value sets.

**Jordan**: Now let's put Helm 4 in context with the alternatives. The Kubernetes templating landscape has several options.

**Alex**: Helm is a package manager with templating. You write Go templates that generate Kubernetes manifests, combined with values that customize those templates. Helm handles packaging, versioning, and release management.

**Jordan**: Kustomize is patch-based. You start with base manifests and apply overlays that modify them. No templating language. You're just patching YAML with more YAML. It's built into kubectl.

**Alex**: Carvel, specifically ytt and kapp, uses Starlark for templating. Starlark is a Python-like language that's more expressive than Go templates. kapp handles the apply process with sophisticated ordering and wait logic.

**Jordan**: Jsonnet is a full programming language for generating configuration. It has functions, conditionals, loops, all the constructs you'd expect from a programming language. But the learning curve is steep.

**Alex**: Here's the thing. Before Helm 4, one of the main arguments against Helm was "Kustomize uses SSA, Helm causes merge conflicts." That argument is now obsolete. Both use the same underlying mechanism.

**Jordan**: So the choice now comes down to templating preference. Do you prefer Go templates or patches? Ecosystem leverage. Helm has 20,000 plus charts on Artifact Hub. Kustomize doesn't have a package ecosystem; you're building from scratch. And organizational momentum. What does your team already know?

**Alex**: When should you choose Helm 4? If you have an existing investment in Helm charts, which most organizations do. If your team knows Go templating. If you need semantic versioning and rollback for packages. If you're using ArgoCD or Flux with Helm sources.

**Jordan**: When might alternatives be better? Kustomize if you prefer patching over templating and want native kubectl integration. Carvel if you need Starlark programmability. Jsonnet if you need full language capabilities and have the expertise.

**Alex**: Now let's get practical. Here's a detailed migration guide with timelines.

**Jordan**: Phase 1 is Assessment, which should take one to two weeks. Inventory all your Helm releases. Run helm list -A across every cluster. Document which Helm version each cluster is running. Identify every custom post-renderer in your organization. Review third-party plugin dependencies.

**Alex**: Create a spreadsheet or database tracking release name, namespace, cluster, chart version, Helm version, post-renderer usage, and criticality. You need visibility before you can plan.

**Jordan**: Phase 2 is SSA Testing, weeks three through six. Helm 3.16 and later supports SSA as an opt-in flag. Start testing with helm upgrade --server-side on non-production releases.

**Alex**: What should you watch for? Drift detection changes in ArgoCD or Flux. If you're using GitOps, your reconciliation behavior might change. HPA and VPA interactions. Autoscalers might conflict with field ownership. Custom controllers that assume they own all fields.

**Jordan**: Also check your monitoring. If you have dashboards or alerts that parse the last-applied-configuration annotation, they'll break. You need to migrate to using managedFields.

**Alex**: Phase 3 is WASM Plugin Migration, running in parallel with SSA testing, weeks four through eight. Audit your existing post-renderers. What do they actually do? Can any be eliminated? Some post-renderers were workarounds for Helm limitations that might not exist anymore.

**Jordan**: Categorize by complexity. Simple transformations like adding labels are easy to port. Complex logic like external API calls or encryption operations require more work.

**Alex**: Choose your implementation language. Build your plugins using the Extism SDK. Test extensively. WASM has different performance characteristics and constraints than native code.

**Jordan**: Phase 4 is Staged Rollout, weeks eight through twelve. Start with development clusters. Install Helm 4 alongside Helm 3 using different binary names. Migrate non-critical releases. Validate that monitoring, alerting, and CI/CD all work correctly.

**Alex**: Move to staging next. Use production-like workloads. Run through your entire deployment pipeline. Benchmark performance. Compare deployment times between Helm 3 and Helm 4.

**Jordan**: Finally, production. Start with low-risk releases. Maintain rollback capability by keeping the Helm 3 CLI available. Monitor closely for unexpected behavior. Gradual rollout over multiple deployment cycles.

**Alex**: Let's talk about common migration errors we're already seeing in the community.

**Jordan**: Error number one: forgetting to update CI/CD pipelines. The --dry-run flag behavior changed. --force is now --force-replace. Every pipeline using these flags needs updates.

**Alex**: Error number two: HPA conflicts with SSA. If your HPA is managing replicas and your Helm chart also sets replicas, you'll have ownership conflicts. You might need to remove the replicas field from your chart and let HPA own it entirely.

**Jordan**: Error number three: third-party plugins not yet compatible. Not every plugin maintainer has shipped Helm 4 support yet. Check compatibility before migrating.

**Alex**: Error number four: monitoring expecting last-applied-configuration. If you have tooling that parses this annotation for change tracking or auditing, it will break. Migrate to managedFields or find alternative approaches.

**Jordan**: Now let's talk about what the community is saying. We've been monitoring discussions since the release.

**Alex**: Early adopter feedback is mostly positive. Performance improvements are validated. Teams are seeing 40 to 60 percent faster deployment times, just as promised. The SSA migration has been smoother than expected for teams already using ArgoCD or Flux.

**Jordan**: The WASM plugin learning curve is steeper than expected. Teams that have never worked with WebAssembly are finding it challenging. The tooling is there, but it requires learning new concepts.

**Alex**: The skeptics have valid points too. "SSA should have been the default years ago." That's fair. Helm could have adopted SSA earlier. But coordination with the ecosystem took time.

**Jordan**: "WASM plugins are overkill for simple post-rendering." Also fair. If you just want to add a label to every resource, rewriting a shell one-liner as a WASM module feels heavy. But the security benefits are real.

**Alex**: "Breaking post-renderers will delay adoption for many organizations." This is probably the most significant concern. Organizations with complex post-render pipelines face months of migration work.

**Jordan**: Based on historical patterns and current signals, here's our adoption timeline prediction. Months one through three: early adopters, greenfield projects, and organizations with minimal post-renderer usage.

**Alex**: Months three through six: GitOps-first teams. If you're already using ArgoCD or Flux with SSA, the transition is relatively smooth. Your tooling already speaks SSA.

**Jordan**: Months six through twelve: mainstream adoption. The plugin ecosystem matures. Third-party compatibility improves. Documentation and community resources expand.

**Alex**: Months twelve and beyond: legacy migrations and late adopters. Organizations with complex legacy setups. Highly regulated industries with slow change processes.

**Jordan**: Remember, Helm 3 receives security patches until November 11th, 2026. That's a full year of runway. There's no emergency.

**Alex**: Let's wrap up with key takeaways and practical actions.

**Jordan**: Takeaway number one: Server-Side Apply is the headline. GitOps peace is finally achieved. Helm, ArgoCD, Flux, and kubectl now speak the same field ownership language. This is objectively good for everyone.

**Alex**: Takeaway number two: WASM plugins represent the highest friction but best security. The migration cost is real, but arbitrary binary execution was a security liability that needed to be fixed.

**Jordan**: Takeaway number three: you have a twelve-month runway. Helm 3 support extends to November 2026. Plan carefully rather than rushing.

**Alex**: Takeaway number four: test SSA now with Helm 3.16. You don't need Helm 4 to start testing. Run helm upgrade --server-side on non-production releases today.

**Jordan**: Takeaway number five: Helm 4 strengthens the Kubernetes package management position. With SSA alignment and improved security, Helm is better positioned than ever as the standard.

**Alex**: For practical actions this week, test the --server-side flag on a non-production release. See how it behaves. Check if your monitoring breaks.

**Jordan**: This month, inventory your post-renderers. How many do you have? How complex are they? What languages would you use to rewrite them?

**Alex**: Q1 2026, plan your migration timeline. Map out the eight to twelve week migration across your clusters. Identify dependencies and risks.

**Jordan**: H1 2026, execute your production migration. With the plugin ecosystem more mature and community documentation expanded, this is the sweet spot for most organizations.

**Alex**: For those wanting to go deeper, we published a comprehensive blog post at platform-engineering-playbook.io/blog/helm-4-release. It includes the complete breaking changes inventory, comparison tables, and step-by-step migration checklists.

**Jordan**: Helm 4 represents a maturation milestone. After ten years, Kubernetes package management is aligned with modern GitOps patterns. The migration has friction, especially around plugins, but the destination is worth it.

**Alex**: The field ownership wars are over. Everyone can finally deploy in peace.

---

## Resources

### Official Documentation
- [Helm 4.0 Release Blog](https://helm.sh/blog/helm-4-released/)
- [CNCF Helm 10-Year Announcement](https://www.cncf.io/announcements/2025/11/12/helm-marks-10-years-with-release-of-version-4/)
- [Kubernetes Server-Side Apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/)
- [Extism WebAssembly Runtime](https://extism.org/)

### Alternatives
- [Kustomize Documentation](https://kustomize.io/)
- [Carvel (ytt/kapp)](https://carvel.dev/)
- [Artifact Hub](https://artifacthub.io/)

### Related Content
- [Helm 4 Blog Post](/blog/helm-4-release-server-side-apply-wasm-plugins-migration-guide-2025) - Complete migration guide

---

## Related Episodes

- [Episode #032: Terraform vs OpenTofu](/podcasts/00032-terraform-opentofu-debate) - Similar major version migration dynamics
- [Episode #040: Platform Engineering Anti-Patterns](/podcasts/00040-platform-engineering-anti-patterns) - Avoid template sprawl
- [Episode #035: KubeCon 2025 Part 1](/podcasts/00035-kubecon-2025-ai-native) - Helm 4 announcement context
