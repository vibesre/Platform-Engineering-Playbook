# Lesson Outline: Episode 9 - GitOps & Deployment Automation

## Metadata
- **Course**: Kubernetes Production Mastery
- **Episode**: 9 of 10
- **Duration**: 15 minutes
- **Type**: Core Concept
- **Prerequisites**: Episodes 1-8 (especially Episode 1 for production anti-patterns, Episode 8 for multi-cluster cost considerations)
- **Template**: Core Concept (Episodes 3-N-2)

## Learning Objectives
By end of lesson, learners will:
1. Implement GitOps principles (Git as source of truth, declarative config, automated sync) using ArgoCD or Flux
2. Choose between Helm and Kustomize for configuration management based on templating needs and team preferences
3. Configure deployment strategies beyond rolling updates (canary releases, blue/green) using Argo Rollouts or native Kubernetes

Success criteria:
- Can explain why manual kubectl doesn't scale to 20+ clusters and how GitOps solves this
- Can choose ArgoCD vs Flux based on team size, UI needs, and complexity tolerance
- Can configure canary deployment with progressive traffic shifting
- Can design CI/CD pipeline that updates Git and lets GitOps tool handle deployment

## Spaced Repetition Plan
**Introduced** (repeat later):
- GitOps principles → Episode 10 (multi-cluster GitOps fleet management)
- ArgoCD/Flux → Episode 10 (hub-and-spoke GitOps architecture)
- Helm/Kustomize → Episode 10 (environment-specific overlays)
- Deployment strategies → Episode 10 (consistent rollout patterns across clusters)

**Reinforced** (from earlier):
- Production readiness from Episode 1 → GitOps achieves consistency across environments
- Multi-cluster costs from Episode 8 → GitOps prevents configuration drift that wastes resources
- Observability from Episode 7 → Deployment strategies need metrics for validation

## Lesson Flow

### 1. Recall & Connection (1.5 min)
**Callback to Episode 8**: "Last episode: cost optimization. Right-sizing, autoscaling, quotas. You're paying for what you need. But here's what happens next: your team needs to deploy an update. To twenty clusters. Dev, staging, three prod regions, DR, per-team clusters. How do you deploy consistently?"

**The Manual Deployment Problem**:
- kubectl apply to cluster 1... cluster 2... cluster 3...
- Midway through, you realize there's a typo in the YAML
- Some clusters have the old version, some have the new version, some have the broken version
- Configuration drift: clusters that should be identical aren't
- No audit trail: who deployed what, when, why?
- No rollback strategy: how do you undo this across 20 clusters?

**Hook**: "Manual kubectl doesn't scale. Episode One called it an anti-pattern. Today: GitOps—Git becomes your source of truth. ArgoCD or Flux automates deployment. Helm or Kustomize manages config. And deployment strategies go beyond rolling updates to canary and blue/green."

**Preview**: "First, GitOps principles and why they matter. Second, ArgoCD versus Flux decision framework. Third, Helm versus Kustomize for configuration. Finally, deployment strategies that validate before full rollout."

### 2. Learning Objectives (30 sec)
By the end, you'll:
- Implement GitOps with ArgoCD or Flux
- Choose Helm vs Kustomize based on needs
- Configure canary and blue/green deployments

### 3. GitOps Principles (3 min)

#### 3.1 The Core Concept (1 min)
**Git as Source of Truth**: Your desired state lives in Git. Not in someone's laptop. Not in a wiki. Not in tribal knowledge. Git repository contains all Kubernetes manifests—deployments, services, config maps, everything.

**Declarative Configuration**: You declare what you want (3 replicas of nginx:1.21), not how to get there (kubectl scale, kubectl set image). The GitOps tool figures out how.

**Automated Sync**: GitOps tool (ArgoCD/Flux) watches Git repository. Detects changes. Applies them to clusters automatically. No human in the loop for deployment.

**Self-Healing**: Cluster state drifts from Git (someone kubectl edits a deployment)? GitOps tool reverts to Git state. Git is always right.

#### 3.2 Why Manual kubectl Doesn't Scale (1 min)
**At 1 Cluster**: kubectl apply works fine. Quick, simple, direct.

**At 5 Clusters**: Still manageable with shell scripts. Loop through clusters, apply manifests. Tedious but doable.

**At 20+ Clusters**: Breaks down completely.
- Time: 20 clusters × 5 min per deployment = 100 minutes
- Errors: Manual process means typos, wrong files, skipped clusters
- Drift: Clusters slowly diverge (different versions, config differences)
- Audit: No record of who changed what when
- Rollback: Manual rollback to 20 clusters during incident? Too slow.

**The GitOps Solution**:
- Commit change to Git (takes 30 seconds)
- GitOps tool deploys to all 20 clusters automatically (takes 2-5 minutes)
- Audit trail: Git history shows who, what, when, why
- Rollback: `git revert`, GitOps redeploys previous state to all clusters
- Drift prevention: GitOps continuously reconciles cluster state to Git

#### 3.3 Additional Benefits (1 min)
**Version Control**: All changes tracked. Branching for features. Pull requests for review. Merge commits for approval trail.

**Disaster Recovery**: Entire cluster config in Git. Lose cluster? Recreate from Git. Minutes, not days.

**Security**: No developer needs direct kubectl access to production. Git PR approval required. GitOps tool has credentials, not humans.

**Consistency**: All environments (dev/staging/prod) from same Git structure. Differences are explicit (environment-specific Kustomize overlays).

**Callback to Episode 1**: "Production readiness checklist item: repeatable deployments. GitOps achieves this. No manual steps. No 'works on my machine.' Git defines production."

### 4. ArgoCD vs Flux (5 min)

#### 4.1 ArgoCD Characteristics (2 min)
**What It Is**: CNCF graduated GitOps tool with web UI, multi-tenancy, and extensive RBAC.

**Key Features**:
- **Web UI**: Visual dashboard showing all applications, sync status, health, deployment history
- **Multi-Tenancy**: Projects separate teams, namespaces, Git repos with granular RBAC
- **Sync Waves**: Control deployment order (database before app)
- **Hooks**: Pre-sync, post-sync scripts (run migrations, smoke tests)
- **App-of-Apps**: ArgoCD can deploy ArgoCD applications (bootstrap entire environments)
- **Health Assessments**: Custom health checks beyond Kubernetes readiness

**Strengths**:
- UI reduces learning curve (developers can see deployment status without CLI)
- Enterprise features (SSO, audit logs, RBAC) out of box
- Larger ecosystem (plugins, integrations, community support)
- Multi-cluster support from day 1

**Weaknesses**:
- Heavier weight (more components, more resource usage)
- Higher operational complexity (more to configure, more to troubleshoot)
- Opinionated structure (may not fit all workflows)

**Best For**:
- Large teams (50+ engineers) needing multi-tenancy
- Organizations requiring UI for visibility and debugging
- Multi-cluster deployments from day 1
- Teams wanting comprehensive RBAC and audit

#### 4.2 Flux Characteristics (1.5 min)
**What It Is**: CNCF graduated GitOps toolkit, CLI-driven, GitOps-native design.

**Key Features**:
- **Lightweight**: Minimal footprint, less resource usage
- **GitOps-Native**: Git is UI (no web dashboard by default)
- **Kustomize Integration**: Built-in support for Kustomize overlays
- **Helm Controller**: Native Helm chart deployment
- **Notification System**: Webhook alerts to Slack, PagerDuty, etc.
- **OCI Support**: Store manifests in OCI registries (not just Git)

**Strengths**:
- Simpler architecture (fewer moving parts)
- Lower resource usage (good for smaller clusters, edge deployments)
- CLI-first (automation-friendly, fits GitOps philosophy)
- Flexible (toolkit approach, use components you need)

**Weaknesses**:
- No built-in UI (third-party UIs exist: Weave GitOps, others)
- Less opinionated (more setup required)
- Steeper learning curve for teams wanting UI

**Best For**:
- Teams comfortable with CLI and Git-centric workflows
- Automation-first organizations (CI/CD pipelines, infrastructure as code)
- Resource-constrained environments
- Teams wanting lightweight, composable GitOps

**2024 Note**: Weaveworks (Flux creators) shut down, but Flux is CNCF-backed and actively maintained by community.

#### 4.3 Decision Framework (1.5 min)
**Choose ArgoCD if**:
- Large team (50+ engineers) needs visibility and self-service
- UI requirement for developers/ops/management
- Multi-tenancy with strict RBAC required
- Enterprise features (SSO, audit) needed day 1

**Choose Flux if**:
- Small to medium team comfortable with CLI/Git
- Automation-first culture (CI/CD pipelines, IaC)
- Lightweight footprint desired (edge, resource-constrained)
- Prefer toolkit approach (composable, flexible)

**Both Are Good**: This isn't "one right answer." Both are CNCF graduated, production-proven, actively maintained. Choose based on team culture and requirements.

**Can Switch Later**: Migration from ArgoCD to Flux (or vice versa) is possible. Git manifests are portable. Don't overthink initial choice.

### 5. Helm vs Kustomize (3 min)

#### 5.1 Helm Overview (1 min)
**What It Is**: Kubernetes package manager with templating engine.

**How It Works**: Charts are packages with templates. Values files customize deployments. Helm renders templates → generates manifests → applies to cluster.

**Strengths**:
- **Templating**: Variables, conditionals, loops (DRY principle)
- **Package Manager**: Install, upgrade, rollback applications as units
- **Charts Ecosystem**: Thousands of pre-built charts (Bitnami, official charts)
- **Versioning**: Charts have versions, track application releases
- **Dependency Management**: Charts can depend on other charts

**Use Cases**:
- Complex applications with many configuration options
- Need to install third-party software (PostgreSQL chart, Redis chart)
- Want versioned releases with rollback capability
- Multiple environments with significant config differences

**Example**: Deploy PostgreSQL with different sizes per environment. Helm chart with values-dev.yaml (small), values-prod.yaml (HA, large).

#### 5.2 Kustomize Overview (1 min)
**What It Is**: Template-free configuration management using overlays.

**How It Works**: Base manifests (common config) + overlays (environment-specific patches). Kustomize merges base + overlay → generates final manifests.

**Strengths**:
- **No Templating**: Raw YAML, easier to read/understand
- **Overlays**: Patch base config for environments (dev/staging/prod)
- **Native to kubectl**: `kubectl apply -k` works without additional tools
- **Composable**: Overlay on overlay (base → team overlay → environment overlay)
- **Simpler Mental Model**: "Patch these fields" vs "Template logic"

**Use Cases**:
- Simpler applications (microservices, standard deployments)
- Prefer declarative patches over templating
- Environment differences are minor (replica count, resource limits, image tags)
- Want no dependencies (kubectl built-in)

**Example**: Base deployment (3 replicas). Dev overlay (1 replica). Prod overlay (5 replicas, more resources).

#### 5.3 Helm vs Kustomize Decision (1 min)
**Use Helm When**:
- Complex app with many config knobs (databases, monitoring stacks)
- Installing third-party charts (don't reinvent wheel)
- Need versioned releases and rollback
- Team comfortable with templating logic

**Use Kustomize When**:
- Simpler apps (typical microservices)
- Prefer raw YAML over templates
- Environment differences are minor
- Want no additional tools (kubectl native)

**Can Use Both**: Helm chart as base → Kustomize overlay for environment-specific patches. Not either/or.

**Pattern**: Many teams start with Kustomize (simpler), add Helm when complexity demands it (databases, complex apps).

### 6. Deployment Strategies (3 min)

#### 6.1 Rolling Updates (Default) (0.5 min)
**How It Works**: Gradually replace old pods with new pods. MaxSurge (extra pods during rollout), MaxUnavailable (max pods down during rollout).

**Pros**: Built-in, simple, zero-downtime
**Cons**: Old and new versions coexist during rollout. No traffic control. All-or-nothing (can't shift 10% traffic).

**Use For**: Most deployments. Simple, reliable.

#### 6.2 Blue/Green Deployments (1 min)
**How It Works**: Two identical environments. Blue (current production). Green (new version). Deploy to green. Test. Switch traffic from blue to green instantly (update Service selector or Ingress). Keep blue running for quick rollback.

**Pros**: Instant cutover. Easy rollback (switch back to blue). Test new version in production-like environment before traffic.

**Cons**: Double resources during transition (run blue + green simultaneously). Instant switch means instant impact if issues.

**Implementation**: Two Deployments (app-blue, app-green). Service selector switches between them. Or Ingress weighted routing.

**Use For**: High-risk changes, need instant rollback, can afford double resources.

#### 6.3 Canary Deployments (1 min)
**How It Works**: Deploy new version to small subset (canary). Shift 10% traffic to canary. Monitor metrics (latency, errors). If healthy, increase to 25%, then 50%, then 100%. If errors, rollback.

**Pros**: Progressive validation. Limit blast radius (only 10% affected). Metrics-driven decision.

**Cons**: More complex setup. Requires traffic splitting (Ingress, service mesh, or Argo Rollouts).

**Implementation Options**:
- Ingress weighted routing (limited control)
- Service mesh (Istio, Linkerd) for fine-grained traffic splitting
- **Argo Rollouts** (recommended): Progressive delivery controller, automated canary with metrics analysis

**Argo Rollouts** adds:
- Automated traffic shifting (0% → 10% → 25% → 50% → 100%)
- Metrics analysis (query Prometheus, abort if errors spike)
- Pause points (manual approval before increasing traffic)
- Automated rollback on failure

**Use For**: Critical services, need validation before full rollout, have metrics infrastructure (Episode 7's Prometheus).

#### 6.4 Decision Framework (0.5 min)
**Rolling Updates**: Default for most apps. Simple, reliable, built-in.

**Blue/Green**: High-risk changes needing instant rollback. Can afford double resources. Database migrations (deploy green, test, switch).

**Canary**: Critical services. Need progressive validation. Have metrics (Prometheus). Use Argo Rollouts for automation.

### 7. CI/CD Integration (1 min)

**Traditional CI/CD**: CI pipeline builds image → pushes to registry → kubectl applies manifest to cluster. **Problem**: CI has cluster credentials. CI must know about all clusters. Deployment tied to CI success.

**GitOps CI/CD**: CI pipeline builds image → pushes to registry → updates Git manifest (image tag) → commits to Git. **ArgoCD/Flux** detects Git change → deploys to clusters. **Benefits**: CI doesn't need cluster access. Single workflow for all clusters. Deployment decoupled from CI.

**Image Promotion Pattern**:
- Dev Git branch → ArgoCD deploys to dev cluster
- Merge to staging branch → ArgoCD deploys to staging
- Tag release → Update prod branch → ArgoCD deploys to prod
- Git structure enforces promotion flow

**Callback to Episode 7**: "Canary deployments need metrics validation. Prometheus from Episode 7 provides latency/error data for automated rollout decisions."

### 8. Common Mistakes (1.5 min)

**Mistake 1**: Storing secrets in Git
- **What happens**: Credentials exposed, security breach
- **Fix**: Use sealed secrets (encrypt before Git), external secret management (Vault, cloud provider), or secret generators (ArgoCD, Flux)

**Mistake 2**: No drift prevention
- **What happens**: Someone kubectl edits deployment, cluster diverges from Git
- **Fix**: Enable auto-sync in ArgoCD/Flux (GitOps tool reverts manual changes)

**Mistake 3**: Deploying to production without testing GitOps workflow
- **What happens**: GitOps misconfiguration, production deployment fails, no rollback plan
- **Fix**: Test GitOps in dev/staging first. Verify sync works. Test rollback (git revert).

**Mistake 4**: Overly complex Helm templates
- **What happens**: Unmaintainable templates, debugging nightmares, team avoids making changes
- **Fix**: Keep templates simple. Prefer Kustomize overlays for simple differences. Use Helm only when complexity justified.

**Mistake 5**: No environment parity
- **What happens**: Dev works, staging works, production fails (different configs)
- **Fix**: Same base manifests across environments. Environment differences through Kustomize overlays or Helm values only.

### 9. Active Recall (1.5 min)
"Pause and answer these questions:"

**Question 1**: Why is manual kubectl to 20 clusters an anti-pattern? How does GitOps solve this?
[PAUSE 5 sec]

**Question 2**: ArgoCD or Flux: which would you choose for a 50-person engineering team that wants deployment visibility and multi-tenancy? Why?
[PAUSE 5 sec]

**Question 3**: When would you use a canary deployment instead of rolling update? What infrastructure is required?
[PAUSE 5 sec]

**Answers**:
1. **Manual kubectl doesn't scale**: 20 clusters × 5 min = 100 minutes. Prone to errors (typos, skipped clusters). No audit trail. No rollback strategy. Configuration drift. **GitOps solution**: Commit to Git (30 sec), ArgoCD/Flux deploys to all clusters automatically (2-5 min). Git history = audit trail. Rollback = git revert. Continuous reconciliation prevents drift.

2. **Choose ArgoCD**: 50-person team is large, benefits from UI for visibility. Multi-tenancy with RBAC needed for team isolation. ArgoCD provides web UI, projects for multi-tenancy, extensive RBAC out of box. Flux would work but requires third-party UI and more setup for multi-tenancy.

3. **Canary when**: Critical services where progressive validation needed. Can't risk all-or-nothing rollout. **Required infrastructure**: Metrics (Prometheus from Episode 7) to validate canary health. Traffic splitting (Argo Rollouts, or service mesh like Istio). Time to monitor progressive rollout (not urgent hotfixes).

### 10. Recap & Integration (1.5 min)

**Takeaways**:
1. **GitOps principles**: Git as source of truth, declarative config, automated sync, self-healing. Manual kubectl doesn't scale to 20+ clusters.
2. **ArgoCD vs Flux**: ArgoCD for large teams wanting UI/multi-tenancy. Flux for automation-first teams wanting lightweight. Both CNCF graduated and production-proven.
3. **Helm vs Kustomize**: Helm for complex apps, templating, third-party charts. Kustomize for simpler apps, overlays, no templating. Can use both.
4. **Deployment strategies**: Rolling (default), Blue/Green (instant switch, easy rollback), Canary (progressive with validation using Argo Rollouts).
5. **CI/CD pattern**: Build image → update Git → GitOps deploys. CI doesn't need cluster credentials.

**Connection to Previous Episodes**:
- Episode 1: GitOps achieves repeatable deployments (production readiness)
- Episode 7: Canary deployments use Prometheus metrics for validation
- Episode 8: GitOps prevents configuration drift that causes cost waste

**Bigger Picture**: You can build infrastructure, observe it, optimize costs, and now automate deployments. Final episode: managing this at multi-cluster scale.

### 11. Next Episode Preview (30 sec)
"Final episode: Multi-Cluster Management & Course Synthesis. Twenty-plus clusters across dev, staging, prod, DR. How do you manage them without going insane? Hub-and-spoke GitOps. Policy enforcement with OPA and Kyverno. Disaster recovery with Velero. And synthesizing all ten episodes into a cohesive production operations framework. We're bringing it all together. See you then."

---

## Supporting Materials

**Code Examples**:
1. **ArgoCD Application manifest** - Git repo, sync policy, health checks
2. **Flux Kustomization** - Git source, path, prune settings
3. **Helm chart with values overlays** - values-dev.yaml, values-prod.yaml
4. **Kustomize base + overlays** - base/, overlays/dev/, overlays/prod/
5. **Argo Rollouts Canary** - steps, metrics analysis, automated rollback

**Tech References**:
- argoproj.github.io/argo-cd/ - ArgoCD documentation
- fluxcd.io/docs/ - Flux documentation
- helm.sh/docs/ - Helm documentation
- kustomize.io/ - Kustomize documentation
- argoproj.github.io/argo-rollouts/ - Argo Rollouts for progressive delivery

**Analogies**:
1. **Git as source of truth** - Building blueprints (Git) vs building state (cluster)
2. **GitOps sync** - Thermostat continuously adjusting to setpoint
3. **Helm templates** - Mail merge (template + data = customized output)
4. **Kustomize overlays** - Transparent overlays on base drawing
5. **Canary deployment** - Coal mine canary (test with small subset before all)

---

## Quality Checklist

**Structure**:
- [x] Clear beginning/middle/end (recall → GitOps → tools → strategies → CI/CD → practice → recap)
- [x] Logical flow (why GitOps → how to implement → deployment patterns)
- [x] Time allocations realistic (15 min: 1.5+3+5+3+1+1.5+1.5+1.5 = ~18 min allocated, will tighten in script)
- [x] All sections specific with concrete comparisons and examples

**Pedagogy**:
- [x] Objectives specific/measurable (implement GitOps with ArgoCD/Flux, choose Helm vs Kustomize, configure canary)
- [x] Spaced repetition integrated (callbacks to Episodes 1,7,8; forward to Episode 10)
- [x] Active recall included (3 retrieval questions with pauses)
- [x] Signposting clear (first/second/third, section transitions)
- [x] 5 analogies (blueprints, thermostat, mail merge, overlays, canary)
- [x] Pitfalls addressed (5 common mistakes with fixes)

**Content**:
- [x] Addresses pain points (manual kubectl doesn't scale, configuration drift, complex deployments)
- [x] Production-relevant examples (20-cluster deployments, multi-tenancy, enterprise RBAC)
- [x] Decision frameworks (ArgoCD vs Flux, Helm vs Kustomize, deployment strategy selection)
- [x] Troubleshooting included (drift prevention, secret management, testing workflows)
- [x] Appropriate depth for senior engineers (app-of-apps, sync waves, Argo Rollouts)

**Engagement**:
- [x] Strong hook (manual deployment to 20 clusters nightmare, configuration drift)
- [x] Practice/pause moments (active recall with 5-sec pauses)
- [x] Variety in techniques (analogies, comparisons, decision frameworks, examples)
- [x] Preview builds anticipation (multi-cluster management, course synthesis)
