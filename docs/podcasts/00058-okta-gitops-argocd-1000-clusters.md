---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #058: Okta's GitOps Journey - Scaling ArgoCD from 12 to 1,000 Clusters"
slug: 00058-okta-gitops-argocd-1000-clusters
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #058: Okta's GitOps Journey - Scaling ArgoCD from 12 to 1,000 Clusters

<GitHubButtons />

<iframe width="100%" style={{aspectRatio: '16/9', marginBottom: '1rem'}} src="https://www.youtube.com/embed/Y44Gyfq6qJA" title="Episode #058: Okta's GitOps Journey - Scaling ArgoCD from 12 to 1,000 Clusters" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerPolicy="strict-origin-when-cross-origin" allowFullScreen></iframe>

**Duration**: 15 minutes | **Speakers**: Jordan & Alex

**Target Audience**: Platform engineers, SREs, DevOps leads managing multi-cluster Kubernetes environments

---

## Synopsis

In five years, Okta scaled Auth0's private cloud from 12 to 1,000 Kubernetes clusters using ArgoCD. At KubeCon 2025, Okta engineers Jérémy Albuixech and Kahou Lei shared their hard-won lessons in their talk "One Dozen To One Thousand Clusters." This episode breaks down the challenges, solutions, and practical wisdom for scaling GitOps to enterprise levels.

---

## Chapter Markers

- **00:00** - Introduction: Okta's ambitious GitOps journey
- **00:45** - News: Helm v4.0.4 & v3.19.4 releases
- **01:15** - News: Zero Trust in CI/CD Pipelines
- **01:45** - News: 1 Billion row database migration
- **02:15** - News: Azure HorizonDB
- **02:45** - News: Platform Engineering State 2026
- **03:15** - The Scaling Journey (12 to 1,000 clusters in 5 years)
- **05:00** - Challenge 1: Controller performance degradation
- **06:30** - Challenge 2: Centralized vs distributed topology
- **08:00** - Challenge 3: Application and repository explosion
- **09:30** - Solutions: Controller sharding and ArgoCD Agent
- **11:00** - Lessons Learned (6 key lessons)
- **13:00** - Practical Guidance by Scale (10-50, 100-500, 500+)
- **14:00** - Key Takeaways & Closing

---

## News Segment (December 13, 2025)

- **[Helm v4.0.4](https://github.com/helm/helm/releases/tag/v4.0.4)** and **[v3.19.4](https://github.com/helm/helm/releases/tag/v3.19.4)**: Maintenance releases with bug fixes and stability improvements. For teams managing 1,000 clusters, rock-solid package management is critical.
- **[Zero Trust in CI/CD Pipelines](https://feeds.dzone.com/link/23568/17231602/zero-trust-in-cicd-pipelines-implementation-guide)**: Practical implementation guide covering identity verification, least privilege, and continuous validation. When deploying to 1,000 clusters via ArgoCD, your CI/CD pipeline IS your security perimeter.
- **[1 Billion Row Database Migration](https://substack.com/redirect/419a50fc-6116-44fb-8b4a-1627a137bad1?j=eyJ1IjoiNnd5eXhwIn0.FBzxQNKuUJD1ReVh3WLE8Ysz4ZV-ojfoAmt6-7pu9P8)**: Engineering team shares zero-downtime migration patterns remarkably similar to multi-cluster GitOps challenges.
- **[Microsoft Azure HorizonDB](https://www.infoq.com/news/2025/12/azure-horizondb-postgresql/)**: New Postgres-compatible database service competing with AWS Aurora and Google AlloyDB. Multi-cluster often means multi-cloud.
- **[Platform Engineering State 2026](https://cJq2d04.eu1.hubspotlinks.com/Ctc/LX+113/cJq2d04/MWPgjSZfxrqW4hTbxn3vFfJjW7xsyK95G-RdRN4FBQLC5nXHCW69t95C6lZ3kBW2zb_v79fNWpgW2sl88j3tgKGyW6F2zG132bM-zW63DvF62gBdNxW68dyMT1V56bpW2CKWNs8TFXGfVWY4WC3rW8j4W4m42fh2wz2YqW1wZ7Mj7Hh5krVk3lQ35mlRf6N3ZJD-t6TlmQVcqjZh7zDd0yVNssQ832JH83W3KvhQG9kgWwwN5PQMvS-8Yf4VfYYXm9661v3VmC76H2mKlJwW4Y97h_7HDxj0W47hkJX6yTjrqW8TGDrn83vpmxVvTpGV7F6RvtW3qHRZD7Dcv_GW1vV3k47HZZGQV4t95H7002D7W32F3KG6LzwXNW3nv2rj4XS67GW63zmVZ7zCk8pW1Mwtd35fpF7nF1L5Gh9r9kMW7dR2Dv1lqf7MW8m274Z8STLWFW1NKmFP4xgzDJW1v3vHL985NRZW8_Xflv446SlsW20dD2y9l4rM5W4nzG3v6XVdrYf31JHt204)**: Salary trends, maturity models, and shift toward lower-level infrastructure concerns.

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Starting cluster count (Okta) | 12 | The New Stack |
| Current cluster count (Okta) | 1,000+ | The New Stack |
| Scaling timeline | 5 years | The New Stack |
| Growth multiple | 83x | Calculated |
| ArgoCD apps before UI degradation | &lt;1,000 | ITNEXT load test |
| ArgoCD apps tested at scale | 2,000+ | ITNEXT load test |
| Max sync time (50 clusters, 1,500 apps) | 10 minutes | ITNEXT load test |
| Clusters requiring controller sharding | 100+ | RedHat ArgoCD Agent |

---

## Key Topics Covered

### The Scaling Journey
- Auth0's private cloud growth from 12 to 1,000+ Kubernetes clusters
- Five-year timeline and architectural evolution
- Why Okta bet on ArgoCD (CNCF graduated, pull-based GitOps)

### Challenges at Scale
1. **Controller Performance Degradation**: Single-threaded operations, UI degradation beyond 1,000 apps, 10-minute sync times at scale
2. **Centralized vs Distributed Topology**: Single point of failure, scaling bottlenecks at 100+ clusters
3. **Application and Repository Explosion**: Managing thousands of ArgoCD Application resources, secret management, RBAC complexity
4. **Sync Performance and Network Geography**: Global distribution adds unpredictable latency, zone-aware scheduling needed
5. **Observability Gaps**: Traditional Prometheus metrics insufficient for 1,000 clusters

### Solutions
1. **Controller Sharding**: Horizontal scaling of ArgoCD controllers
2. **ArgoCD Agent (Hub-Spoke Model)**: Agent per cluster, central hub coordination
3. **Application Sets and Templating**: Generate thousands of applications from patterns
4. **Intelligent Repository Structure**: Monorepo vs polyrepo, environment-based branching, cluster-specific overlays
5. **Progressive Rollouts**: Canary deployments across clusters, automated rollback

### Six Lessons Learned
1. **GitOps doesn't solve organizational problems** - Cultural buy-in is harder than technical implementation
2. **Start small, scale incrementally** - Okta went 12→50→200→1,000, not 12→1,000
3. **Load testing is non-negotiable** - Use tools like vcluster to simulate scale
4. **Observability unlocks confidence** - Track sync success rate, p50/p95/p99, application health
5. **ArgoCD isn't the only tool** - Ecosystem matters: Helm, Kustomize, External Secrets, OPA/Kyverno
6. **Plan for Day 2 operations** - Upgrades, migrations, disaster recovery, on-call runbooks

### Practical Guidance by Scale
- **10-50 clusters**: Single ArgoCD instance sufficient, focus on repository structure and RBAC
- **100-500 clusters**: Warning zone - plan for sharding, load test now, consider hub-spoke architecture
- **500+ clusters**: Okta territory - sharding mandatory, dedicated GitOps platform team required

---

## Transcript

**Jordan**: Today we're diving into one of the most ambitious GitOps scaling stories ever told. Okta took Auth0's private cloud from twelve Kubernetes clusters to over one thousand in five years using ArgoCD. It wasn't smooth. It wasn't simple. And the lessons they learned at KubeCon twenty twenty-five are invaluable for anyone managing multi-cluster infrastructure. But first, let's run through some important news from this week.

**Alex**: Helm released two maintenance updates. Version four point zero point four and version three point nineteen point four are both available. These are stability releases with bug fixes. For platform teams managing one thousand clusters like Okta, rock-solid package management isn't optional. Helm remains the backbone of Kubernetes deployments.

**Jordan**: DZone DevOps published a practical guide on Zero Trust in CI/CD Pipelines. It covers identity verification, least privilege access, and continuous validation. Here's why this matters for GitOps: when you're deploying to one thousand clusters via ArgoCD, your CI/CD pipeline is your security perimeter. A compromised pipeline means a compromised fleet. This guide is worth your time.

**Alex**: An engineering team shared how they migrated one billion database records from DB1 to DB2 with zero downtime. The patterns are remarkably similar to multi-cluster GitOps challenges. Incremental migration. Continuous validation. Rollback safety. Whether you're scaling databases or GitOps deployments, the fundamentals are the same.

**Jordan**: Microsoft announced Azure HorizonDB, a new Postgres-compatible database service. It's competing directly with AWS Aurora and Google AlloyDB. For multi-cloud platform teams, this matters. Multi-cluster often means multi-cloud. Database portability is becoming a requirement, not a nice-to-have.

**Alex**: And finally, Platformweekly published the State of Platform Engineering report for twenty twenty-six. Salary trends, maturity models, and a shift toward lower-level infrastructure concerns. Speaking of platform engineering maturity, let's talk about what it takes to scale GitOps to one thousand clusters. This is where theory meets reality.

**Jordan**: Okta engineers Jérémy Albuixech and Kahou Lei gave a talk at KubeCon plus CloudNativeCon in Atlanta. The title says it all: One Dozen To One Thousand Clusters.

**Alex**: Let's set the scene. Auth0 offers private cloud for enterprise customers. These are organizations that need identity and access management but can't use multi-tenant SaaS. In twenty twenty, Auth0 managed twelve Kubernetes clusters. By twenty twenty-five, that number exceeded one thousand. That's eighty-three times cluster growth in five years.

**Jordan**: And they bet everything on ArgoCD.

**Alex**: ArgoCD is a CNCF graduated project. Production-ready. It's a GitOps continuous delivery tool for Kubernetes. The pull-based model is more secure than traditional push-based CI/CD. It has native Kubernetes support, an active community, and a strong ecosystem. But here's the critical detail: ArgoCD was not designed for one thousand clusters.

**Jordan**: What does that mean in practice?

**Alex**: Let's talk about the challenges. First, controller performance degradation. The ArgoCD application controller is single-threaded for many operations. Research from the community shows that UI performance degrades beyond one thousand applications. When you're syncing fifteen hundred apps across fifty clusters, sync times can reach ten minutes. And that's without accounting for network latency. Clusters spread across global regions add unpredictable delays.

**Jordan**: So the first problem is: ArgoCD slows down as you add clusters.

**Alex**: Correct. Second problem: centralized versus distributed topology. Most teams start with a centralized approach. One ArgoCD instance in a management cluster. It deploys to all your clusters. Pros: single pane of glass. Simplified management. Cons: single point of failure. Scaling bottleneck. At one hundred-plus clusters, you hit a wall. You need controller horizontal scaling. You need sharding. And application sync times become unpredictable.

**Jordan**: What's the third challenge?

**Alex**: Application and repository explosion. At one thousand clusters, you're managing thousands of ArgoCD Application resources. Git repository management becomes complex. Secret management at scale is painful. RBAC explodes: who can deploy what to which clusters? Load testing shows that beyond two thousand applications, you see clear performance issues. The UI becomes unusable.

**Jordan**: And you mentioned sync times earlier.

**Alex**: Fourth challenge: sync performance and network geography. If your clusters are distributed globally, network latency varies significantly. Some clusters might sync in seconds. Others take over ten minutes. You need zone-aware scheduling. You need prioritization. You need to understand which clusters are critical and which can wait.

**Jordan**: What about observability?

**Alex**: That's the fifth challenge. At one thousand clusters, how do you answer basic questions? Which applications are out of sync? What's the sync success rate? Where are the bottlenecks? How do you debug a failed sync across one thousand clusters? Traditional Prometheus metrics aren't enough. You need purpose-built observability.

**Jordan**: So those are the challenges. What are the solutions?

**Alex**: Solution one: controller sharding. You split the ArgoCD controllers across multiple replicas. Each replica manages a subset of clusters or applications. Benefit: horizontal scaling of the control plane. Trade-off: increased complexity. You now have to manage sharding logic.

**Jordan**: What about topology changes?

**Alex**: Solution two: the ArgoCD Agent. This is a hub-spoke model. An agent runs in each cluster. The central hub manages coordination. Benefits: reduces network chattiness. Better scaling characteristics. Fault isolation. Red Hat has published research on this for OpenShift GitOps. It's designed specifically for multi-cluster environments.

**Jordan**: How do you manage thousands of Application resources?

**Alex**: Solution three: Application Sets and GitOps templating. Instead of manually creating thousands of Application resources, you generate them from templates. You define patterns once. ArgoCD generates the applications dynamically. This keeps your repository clean. It enforces consistency across clusters. And it's easier to maintain at scale.

**Jordan**: What about repository structure?

**Alex**: Solution four: intelligent repository structure. The monorepo versus polyrepo debate is real. Do you keep everything in one repository? Or split by team, environment, or cluster? The answer depends on your organization. But the best practice is: balance consistency and flexibility. Environment-based branching works for some teams. Cluster-specific overlays work for others. Test your patterns at small scale first.

**Jordan**: And deployment safety?

**Alex**: Solution five: progressive rollouts. Canary deployments across clusters. Roll out to ten clusters. Validate. Expand to fifty. Validate again. This contains the failure blast radius. If something breaks, you've only impacted a small subset. And automated rollback on anomalies is critical. Don't rely on humans to detect failures.

**Jordan**: Let's talk about lessons learned. Okta spent five years on this journey. What did they learn?

**Alex**: Lesson one: GitOps doesn't solve organizational problems. GitOps is a technical pattern, not a silver bullet. You still need clear ownership. You still need RBAC. You still need approval workflows. Cultural buy-in is harder than technical implementation. If your organization isn't ready for GitOps, the tooling won't fix that.

**Jordan**: What about scaling strategy?

**Alex**: Lesson two: start small, scale incrementally. Okta didn't jump from twelve to one thousand clusters overnight. They went twelve to fifty. Then fifty to two hundred. Then two hundred to one thousand. Each stage revealed new bottlenecks. New failure modes. New operational challenges. Don't try to solve for one thousand clusters on day one. Validate your patterns at smaller scale first.

**Jordan**: How do you know your patterns work?

**Alex**: Lesson three: load testing is non-negotiable. You must test application sync performance. UI responsiveness. Controller resource usage. Network bandwidth requirements. Tools like vcluster let you simulate scale. If you wait until production to discover that your ArgoCD setup can't handle the load, you've already lost.

**Jordan**: What metrics matter?

**Alex**: Lesson four: observability unlocks confidence. Track sync success rate per cluster. Time to sync at p50, p95, and p99. Application health across the entire fleet. Git poll frequency and its impact on your repository. Without these metrics, you're flying blind. You can't diagnose issues. You can't predict capacity. You can't make data-driven decisions.

**Jordan**: Is ArgoCD the only tool you need?

**Alex**: Lesson five: ArgoCD isn't the only tool. The ecosystem matters. Helm for packaging. Kustomize for configuration management. External Secrets Operator for secret management. Policy as Code with OPA or Kyverno. GitOps is a pattern. ArgoCD is one implementation. You need the right tools for each layer of the stack.

**Jordan**: What about ongoing operations?

**Alex**: Lesson six: plan for Day 2 operations. Upgrading ArgoCD across sharded controllers. Migrating repositories without downtime. Disaster recovery for one thousand clusters. On-call runbooks for GitOps incidents. Most teams focus on the initial deployment. But you'll spend ninety-five percent of your time on Day 2. Plan accordingly.

**Jordan**: Let's make this practical. What does this mean for teams at different scales?

**Alex**: If you're managing ten to fifty clusters, you're in the sweet spot. A single ArgoCD instance can handle this. Focus on repository structure and RBAC. Invest in observability early. Don't wait until you hit scaling problems. Build the muscle memory now.

**Jordan**: What about one hundred to five hundred clusters?

**Alex**: You're entering the warning zone. Start planning for sharding now. Load test your ArgoCD setup before you hit production issues. Consider hub-spoke architecture with ArgoCD Agents. Automate everything: rollouts, validation, rollback. Manual processes don't scale beyond one hundred clusters.

**Jordan**: And if you're managing five hundred-plus clusters?

**Alex**: You're in Okta territory. Sharding is mandatory. You need to decide: ArgoCD Agent or alternative topologies? You need a dedicated team for the GitOps platform. This isn't a side project. Observability is mission-critical. You cannot operate at this scale without real-time dashboards, automated alerting, and incident response playbooks.

**Jordan**: What are the universal takeaways, regardless of scale?

**Alex**: Five things. First: GitOps is a journey, not a destination. It evolves continuously. Second: incremental validation beats big-bang deployments. Always. Third: observability unlocks operational confidence. You can't improve what you can't measure. Fourth: organizational readiness matters more than technical readiness. Culture eats tooling for breakfast. Fifth: community matters. Learn from teams like Okta. Read their talks. Study their patterns. You don't have to solve these problems alone.

**Jordan**: Let's wrap with key takeaways. First, Okta's five-year journey from twelve to one thousand clusters proves GitOps scales. But it requires continuous evolution, not set-it-and-forget-it.

**Alex**: Second, ArgoCD has known scaling limits. Beyond one thousand applications or one hundred-plus clusters, you'll need sharding, load testing, and architectural changes.

**Jordan**: Third, centralized GitOps becomes a bottleneck. Hub-spoke models with ArgoCD Agents offer better scaling characteristics.

**Alex**: Fourth, observability is the unlock. You can't manage one thousand clusters without real-time sync metrics, health dashboards, and automated alerting.

**Jordan**: Fifth, start small, validate patterns, scale incrementally. Okta didn't solve for one thousand clusters on day one. Neither should you.

**Alex**: The fundamentals of GitOps remain constant. But scaling to one thousand clusters requires intentional architectural choices, continuous load testing, and operational discipline. If you're on this journey, you're not alone.

---

## Sources

- [How Okta Scaled From 12 to 1000 Kubernetes Clusters With Argo CD](https://thenewstack.io/how-okta-scaled-from-12-to-1000-kubernetes-clusters-with-argo-cd/) - The New Stack
- [How We Load Test Argo CD at Scale: 1,000 vClusters with GitOps](https://itnext.io/how-we-load-test-argo-cd-at-scale-1-000-vclusters-with-gitops-on-kubernetes-d8ea2a8935b6) - ITNEXT
- [Multi-cluster GitOps with the Argo CD Agent](https://www.redhat.com/en/blog/multi-cluster-gitops-argo-cd-agent-openshift-gitops) - Red Hat
- KubeCon + CloudNativeCon Atlanta 2025: "One Dozen To One Thousand Clusters" - Jérémy Albuixech & Kahou Lei

---

## Related Episodes

- [Episode #035: KubeCon 2025 - AI-Native Kubernetes](/podcasts/00035-kubecon-2025-ai-native)
- [Episode #036: KubeCon 2025 - Platform Engineering Evolution](/podcasts/00036-kubecon-2025-platform-engineering)

---

## Listen & Watch

- **YouTube**: [Watch on YouTube](https://youtu.be/Y44Gyfq6qJA)
- **Podcast Feed**: RSS feed coming soon
