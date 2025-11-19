---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 #10: Production Checklists"
slug: /courses/kubernetes-production-mastery/lesson-10
---

# Lesson 10: Production Checklists

## Kubernetes Production Mastery Course

<GitHubButtons />

<iframe width="560" height="315" src="https://www.youtube.com/embed/fdPd3DB9v3A" title="Lesson 10: Production Checklists - Kubernetes Production Mastery" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

**Course**: [Kubernetes Production Mastery](/courses/kubernetes-production-mastery)
**Episode**: 10 of 10
**Duration**: ~18 minutes
**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

## Learning Objectives

By the end of this lesson, you'll be able to:
- Design multi-cluster management strategies using hub-and-spoke GitOps and policy enforcement
- Apply production patterns consistently across fleets using standardized base configs and observability federation
- Synthesize all ten episodes into a cohesive production operations framework

## Prerequisites

- [Lesson 1: Production Mindset](./lesson-01)
- [Lesson 2: Resource Management](./lesson-02)
- [Lesson 3: Security Foundations](./lesson-03)
- [Lesson 4: Health Checks & Probes](./lesson-04)
- [Lesson 5: Stateful Workloads](./lesson-05)
- [Lesson 6: Networking & Services](./lesson-06)
- [Lesson 7: Observability](./lesson-07)
- [Lesson 8: CI/CD Integration](./lesson-08)
- [Lesson 9: Troubleshooting](./lesson-09)

---

## Transcript

Welcome to Episode 10 of Kubernetes Production Mastery. The final episode. Last time, we covered GitOps and deployment automation. Git as your source of truth. ArgoCD or Flux. Automated sync to clusters. But we focused on deploying to clusters, not managing the clusters themselves.

Here's what happens in the real world. You start with one cluster. Simple. Then you need staging for testing. Then dev for development. Then per-team clusters because teams want isolation. Then production in multiple regions for disaster recovery and latency. US-East, US-West, Europe, Asia. Then a DR cluster. Twenty clusters later, you're managing a fleet. How do you do this without losing your mind?

Average organization with fifty-plus engineers? Twenty-plus clusters across four or more environments. This isn't theoretical. This is the norm. And managing twenty clusters manually? That's where everything we've covered in this course comes together.

Today we're tackling multi-cluster management at scale. By the end, you'll design strategies using hub-and-spoke GitOps and policy enforcement. You'll apply production patterns consistently using everything from Episodes One through Nine. And you'll synthesize all ten episodes into a cohesive production operations framework.

### Why Organizations Have Many Clusters

Let me show you why organizations end up with twenty-plus clusters. Isolation comes first. Dev teams want their own clusters. They don't want to step on each other's deployments. Compliance requires it. PCI data can't mix with non-PCI data. Separate clusters for regulatory boundaries. Availability demands it. Multi-region for disaster recovery and lower latency. US-East for American users. Europe for GDPR compliance and European users. Asia for customers there. Blast radius containment. One cluster compromise doesn't take down everything. Scale limits force it. Single cluster etcd maxes out around five thousand nodes. Practical limit is lower.

Typical example. E-commerce company with twenty-four clusters. Four dev clusters, one per team. Two staging clusters. Integration testing and pre-production validation. Six production clusters. Two per region across US, Europe, and Asia. Three disaster recovery clusters. One CI/CD cluster for build pipelines. Eight ephemeral clusters for per-pull-request environments and testing. This is normal for companies at scale.

### Multi-Cluster Management Challenges

The management challenges are brutal. Configuration drift happens first. Without GitOps, clusters diverge. Dev cluster has different RBAC than production. Staging has different network policies. Nobody knows what production actually looks like. Cost visibility disappears. Episode Eight's cost optimization multiplied by twenty clusters. Which cluster is expensive? Which team is over-provisioning? Kubecost per cluster doesn't aggregate. You can't see the whole picture. RBAC sprawl explodes. Twenty clusters means twenty sets of role bindings. New team member joins. You need to update twenty clusters manually. Error-prone and slow.

Deployment consistency breaks down. Update works in dev. Works in staging. Fails in production US-East. Why? Configuration difference nobody documented. Some clusters have the update, some don't. Security posture becomes unmaintainable. CVE announced. You need to patch twenty clusters. Which ones are vulnerable? Which ones are patched? Manual tracking fails.

Episode Eight's cost waste? Multi-cluster compounds it. Can't optimize what you can't measure. Can't measure across twenty separate systems.

### Hub-and-Spoke GitOps Architecture

The solution is GitOps fleet management with hub-and-spoke architecture. Think of an airport hub distributing flights to spoke cities. Centralized Git repository. Distributed ArgoCD or Flux instances watching it. The hub is your Git repository. Single source of truth for all clusters. Directory structure with base configuration common to everything. Overlays for dev, staging, and production. Base contains common config. Network policies, RBAC, monitoring setup. Overlays contain environment-specific patches. Replica counts, resource limits, API endpoints.

Each cluster is a spoke. ArgoCD or Flux instance watching Git. Syncs specific path for its environment. Dev clusters watch overlays/dev. Production clusters watch overlays/prod. Automatic reconciliation every few minutes. Drift prevention built in.

Remember Episode Nine's Kustomize overlays? This is how you use them at scale. Same base configuration. Different overlays per environment. Change base config in Git? All clusters update automatically. Change production overlay? Only production clusters update.

### App-of-Apps Pattern

ArgoCD's app-of-apps pattern solves bootstrapping. Problem: bootstrap twenty clusters with fifty applications each. That's one thousand manual Application custom resources. Not sustainable. Solution: app-of-apps. One Application that creates other Applications. Root Application points to Git directory containing Application manifests. ArgoCD deploys root Application. Root Application creates child Applications. Monitoring stack, logging stack, app one, app two, everything. Bootstrap entire cluster from single manifest.

Use case: new production region in Asia. Deploy root Application. ArgoCD automatically deploys all fifty applications with production Asia configuration. Cluster ready in minutes, not days.

Episode Nine covered ArgoCD's app-of-apps versus Flux's Kustomization with HelmRelease tree. Same concept, different implementation.

### Policy Enforcement at Scale

Policy enforcement at scale becomes critical. You can't manually audit twenty clusters for compliance. Do all pods have resource limits? Are any containers running as root? Do all ingresses have TLS? Manual checking doesn't scale. Policy as code solves this. Open Policy Agent with Gatekeeper or Kyverno.

OPA and Gatekeeper use Rego policy language. Gatekeeper enforces at admission. Blocks non-compliant resources before they're created. Example policy: deny pods without resource limits. Audit mode reports violations without blocking. Kyverno uses YAML for policies. Easier than Rego. Can enforce, audit, or mutate. Mutate means auto-fix. Container missing resource limits? Kyverno adds defaults automatically.

Use cases bring together previous episodes. Enforce Episode Two's resource limits across all clusters. Enforce Episode Three's RBAC standards. No cluster-admin to regular users. Enforce Episode Six's NetworkPolicies. Deny-all by default. Enforce Episode Eight's cost controls. Namespace ResourceQuotas everywhere.

Deployment: policy custom resources in Git base. GitOps deploys to all clusters. Policy violations visible in dashboard. Standards from earlier episodes now enforced automatically at scale.

### Disaster Recovery with Velero

Disaster recovery needs to actually work. Velero backs up Kubernetes resources, persistent volumes, and cluster state. Deployments, services, ConfigMaps, secrets. Everything. Persistent volume snapshots through cloud provider integration. Cluster state including namespaces, RBAC, custom resource definitions. Schedule daily backups to object storage. S3, Google Cloud Storage, Azure Blob. Metadata stored with backup. What's included, when it was taken.

Restore process for total cluster loss. Region failure, etcd corruption, whatever. Create new cluster. Install Velero. Run velero restore create from latest backup. Cluster restored with resources, persistent volumes, state. All intact.

RTO and RPO matter. Recovery Time Objective: how long to restore? Fifteen to thirty minutes typical. Recovery Point Objective: how much data loss? Daily backup means twenty-four hours maximum loss. Episode Five mentioned Velero. StatefulSet data protected. Not just infrastructure, but actual state.

### Multi-Region Failover

Multi-region failover uses active-active or active-passive patterns. Active-active runs both regions serving traffic. Database replication, async or sync. DNS load balancing through GeoDNS or traffic manager. Failure? Redirect traffic to healthy region. Active-passive has primary region serving traffic. Secondary region on standby. Velero backups ready to restore. Failure triggers failover to secondary. Restore from backup, update DNS.

Decision framework: active-active is expensive. Double resources. Complex because of data consistency. But low RTO. Active-passive is cheaper. Pay only during failure. Simpler. Higher RTO because of restore time. Episode Eight's cost optimization applies. Active-active doubles cost. Active-passive pays only when you need it.

### Standardized Base Configs

Standardized base configs work like golden images. Base configuration all clusters share. RBAC, NetworkPolicies, monitoring, logging, cost controls. Enforcement through GitOps plus policy as code ensures consistency. Drift detected and corrected automatically. Benefits: onboard new cluster in minutes. Apply base, add environment overlay, done. Audit compliance across fleet through policy reports.

### Progressive Rollouts

Progressive rollouts follow a pattern. Test to staging to production canary to production full. Merge to test branch, deploy to test clusters. Merge to staging branch, deploy to staging clusters. Merge to production branch, canary deploy to one production cluster using Episode Nine's Argo Rollouts. Metrics healthy? Deploy to remaining production clusters. Episode Seven's Prometheus validates canary. Episode Nine's deployment strategies applied across the fleet.

### Observability Federation

Observability federation solves the twenty Prometheus problem. Twenty Prometheus instances, twenty Grafana dashboards. Can't see fleet-wide metrics. Central Prometheus with Thanos aggregates metrics from all cluster Prometheus instances. Single query interface. Cross-cluster dashboards. Use case: show me CPU usage across all production clusters. Which cluster is highest? Episode Seven's Prometheus architecture. Federation at scale.

### Cost Allocation

Cost allocation uses Kubecost aggregation across clusters. Visibility into cost per team, per environment, per cluster. Accountability through showback reports. Your team's dev clusters cost this much per month. Episode Eight's cost optimization at scale. Can't optimize without visibility.

### Course Synthesis: Rapid Active Recall

Now let's synthesize the entire course. Rapid active recall across all episodes. Episode One: what's the production mindset? What are the six readiness checklist items? Production mindset means designing for failure. Assuming things will break. Six checklist items: resource requests and limits, health checks, RBAC and secrets, multi-replica deployments, observability, automated deployment.

Episode Two: how do you prevent OOMKilled pods? What's the difference between requests and limits? Set appropriate resource limits. Requests reserve capacity for scheduling. Limits cap maximum usage. Set both. Monitor actual usage and right-size.

Episode Three: name three RBAC mistakes. Why shouldn't developers have cluster-admin? Mistake one: giving cluster-admin to everyone. Mistake two: storing secrets in ConfigMaps. Mistake three: no NetworkPolicies. Developers shouldn't have cluster-admin because least privilege. They need namespace access, not cluster control. Blast radius containment.

Episode Four: you see CrashLoopBackOff. What's your debugging workflow? kubectl describe pod shows events. kubectl logs shows application logs. Check restart count. Check liveness probe configuration. Check resource limits. Systematic approach from Episode Four's troubleshooting section.

Episode Five: StatefulSets versus Deployments. When do you use each? StatefulSets for stateful applications needing stable network identity, ordered deployment, and persistent storage per pod. Databases, distributed systems. Deployments for stateless applications. Web servers, APIs. Everything else.

Episode Six: when do you need a service mesh? When is it over-engineering? Need service mesh for compliance requiring mTLS everywhere. Fifty-plus microservices with complex routing. Zero-trust networking. Over-engineering for fewer than twenty services, simple architectures, when you already have good observability.

Episode Seven: what are the four golden signals? How do you use them? Latency, traffic, errors, saturation. Use them for alerting. Monitor these four. They cover ninety percent of issues. Everything else is noise.

Episode Eight: what are the top three sources of Kubernetes cost waste? Over-provisioned resource requests, biggest at forty to sixty percent. Idle resources running twenty-four seven. No autoscaling, paying for peak always.

Episode Nine: ArgoCD versus Flux. Which for a fifty-person team? Why? ArgoCD for large team. UI for visibility. Multi-tenancy with RBAC. Enterprise features out of box. Flux works but needs more setup for that scale.

Episode Ten: why do organizations have twenty-plus clusters? How do you manage them? Isolation, compliance, availability, blast radius, scale limits. Manage with hub-and-spoke GitOps, policy as code, disaster recovery with Velero, observability federation.

### The Complete Production Checklist

The complete production checklist ties everything together. Resource requests and limits from Episode Two. Set requests for scheduling. Set limits to prevent noisy neighbors. Right-size with Episode Seven's Prometheus and Episode Eight's VPA. Health checks from Episode Four. Startup probe for slow initialization. Readiness probe for traffic gating. Liveness probe for restart, used carefully. RBAC and secrets from Episode Three. Least privilege, no cluster-admin to users. Secrets not in ConfigMaps. NetworkPolicies for isolation.

Multi-replica deployments from Episodes One and Nine. Minimum two replicas. Three for critical services. PodDisruptionBudgets. Episode Nine's deployment strategies, canary for critical services. Observability from Episode Seven. Prometheus metrics with golden signals. Log aggregation with Loki or ELK. Distributed tracing for microservices. Automated deployment from Episode Nine. GitOps with ArgoCD or Flux. No manual kubectl in production. Audit trail through Git history. Plus Episode Ten: multi-cluster management, policy enforcement, disaster recovery.

### Complex Integration Scenario

Here's a complex integration scenario. You're deploying a stateful PostgreSQL cluster for e-commerce checkout. Episode Five: use StatefulSet with PVC per pod. Episode Two: right-size resources, start conservative, use Episode Eight's VPA. Episode Four: health checks, startup sixty seconds, readiness five seconds, liveness thirty seconds. Episode Seven: Prometheus monitoring, saturation metrics for connection pool and disk usage. Episode Three: RBAC, database team only, proper secrets management. Episode Six: ClusterIP Service, internal only, no Ingress. Episode Eight: cost controls, ResourceQuota on database namespace. Episode Nine: GitOps deployment using Helm chart with production Kustomize overlay. Episode Ten: Velero daily backups, disaster recovery plan tested quarterly. This is production mastery. All concepts integrated.

### Common Mistakes at Scale

Common mistakes at scale. No standardized base config leads to configuration drift, compliance failures, inconsistent behavior. Fix: golden base config in Git, enforced with policy as code. Manual disaster recovery testing means untested plans fail during actual disasters. Fix: quarterly DR drills, restore from Velero to test cluster. No cost allocation means you can't identify expensive clusters or teams. Optimization impossible. Fix: Kubecost federation, showback reports per team. GitOps without policy enforcement lets developers bypass standards. No resource limits, root containers. Fix: OPA Gatekeeper or Kyverno enforcing production standards. Treating all clusters manually doesn't scale past five clusters. Fix: automation through GitOps, policy as code, observability federation.

### Complete Cluster Design Checklist

You're designing a new production cluster from scratch. Complete checklist and decision process. Start with base config from Git. RBAC, NetworkPolicies, ResourceQuotas, monitoring. Deploy via GitOps using ArgoCD app-of-apps. Enforce policies with Kyverno. Resource limits, no root containers, TLS required. Configure Velero for daily backups. Set up Prometheus federation to central observability. Deploy applications using Episode Nine's patterns. Monitor with Episode Seven's golden signals. Right-size with Episode Eight's strategies. This is the framework. Everything from ten episodes applied.

### Reflection

What was the most valuable concept you learned in this course? For me, it's the production mindset from Episode One. Everything else flows from that. Resources, security, observability, cost, automation. All serve production reliability.

### Next Steps

Your next steps beyond this course. Certifications validate your knowledge. CKA, Certified Kubernetes Administrator, covers Episodes One through Six heavily. Resources, storage, networking, troubleshooting. Focus on cluster operations and workload management. Industry-recognized credential. CKAD, Certified Kubernetes Application Developer, covers application deployment. Episodes Two, Four, Five, Nine. Developer-oriented. CKS, Certified Kubernetes Security Specialist, covers Episode Three plus advanced security. Cluster hardening, supply chain security. Security specialization.

Advanced topics to explore. Custom operators extend Kubernetes with application-specific controllers. Database operators, backup operators. eBPF networking for advanced capabilities. Cilium deep dive, packet filtering, observability without sidecars. Platform engineering builds internal developer platforms on Kubernetes. Abstractions, self-service, golden paths. Service mesh deep dive into Istio or Linkerd production deployment. mTLS, traffic management, multi-cluster mesh. Multi-tenancy for hard isolation. vCluster, Loft, per-tenant namespaces.

Continuous learning resources. Kubernetes official docs, always up to date. CNCF landscape to discover new tools. KubeCon talks, conference recordings. Production engineering blogs from companies sharing real-world experiences. Practice in home labs. k3s, Raspberry Pi clusters. Contribute to open source. Kubernetes, ArgoCD, Prometheus. Mentor others. Teaching solidifies knowledge.

### What You've Mastered

What you've mastered. Foundation: production mindset, resource management, security from Episodes One through Three. Operations: troubleshooting, storage, networking from Episodes Four through Six. Platform: observability and cost optimization from Episodes Seven and Eight. Automation: GitOps and deployment strategies from Episode Nine. Scale: multi-cluster management and disaster recovery from Episode Ten.

The journey started with Episode One asking why production is different. Episodes Two through Six gave you building blocks. Resources, security, storage, networking. Episodes Seven and Eight provided operational excellence. Observability, cost control. Episode Nine delivered automation through GitOps. Episode Ten brought it to scale with fleet management.

Your production operations framework is complete. Not just how to deploy, but how to run reliably at scale with observability, cost control, and automation. You're ready for production Kubernetes.

Congratulations on completing Kubernetes Production Mastery.

---

## Navigation

⬅️ **Previous**: [Lesson 9: Troubleshooting](./lesson-09)

📚 **[Back to Course Overview](/courses/kubernetes-production-mastery)**
