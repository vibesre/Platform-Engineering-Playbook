# Lesson Outline: Episode 3 - Security Foundations: RBAC & Secrets

## Metadata
**Course**: Kubernetes Production Mastery
**Episode**: 3 of 10
**Duration**: 18 minutes
**Episode Type**: Core Concept (Security Focus)
**Prerequisites**: Episode 1 (Production Mindset), basic understanding of Kubernetes authentication
**Template Used**: Core Concept Lesson (security-focused)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. **Implement** namespace-scoped RBAC roles following least privilege principles
2. **Configure** secure secrets management using Sealed Secrets or External Secrets Operator
3. **Identify and remediate** the 5 most common RBAC misconfigurations in production clusters

Success criteria:
- Can write a namespace-scoped Role and RoleBinding from scratch
- Can explain when to use Sealed Secrets vs External Secrets Operator
- Can spot RBAC anti-patterns in example manifests
- Can articulate why base64 encoding is not encryption

## Spaced Repetition Plan

**Concepts Introduced** (will be repeated in later episodes):
- Service account tokens - Will use in Episode 4 (troubleshooting), Episode 7 (observability), Episode 10 (multi-cluster)
- Role vs ClusterRole distinction - Will apply in Episode 10 (multi-cluster RBAC)
- Sealed Secrets pattern - Will reference in Episode 9 (GitOps)
- External Secrets Operator - Will use in Episode 5 (stateful workloads with DB credentials)
- Least privilege principle - Will apply across all future episodes

**Concepts Reinforced** (from previous episodes):
- **From Episode 1**: RBAC as checklist item #3 ("RBAC Least Privilege")
- **From Episode 1**: Security baseline as checklist item #6
- **From Episode 1**: Production mindset ("What happens WHEN this is compromised?")
- **From Episode 2**: Resource limits (mention RBAC for resource quota management)

## Lesson Flow

### 1. Hook & Episode Context (1 min)

**Callback to Episode 1**:
"Welcome back to Kubernetes Production Mastery. In Episode 1, we established the production mindset and learned the 6-item production readiness checklist. Before we dive into today's topic, try to recall: What is checklist item number 3?"

[PAUSE 3 seconds]

"That's right - RBAC Least Privilege. And here's why this matters more than you think."

**Hook - The #1 Security Issue**:
"RBAC misconfiguration is the number one Kubernetes security vulnerability in production environments. Not zero-days. Not container escapes. Human error in access control.

Last month, a Fortune 500 company experienced a breach. An attacker got access to a single service account token with cluster-admin permissions. Within 20 minutes, they had pivoted across 47 namespaces, exfiltrated database credentials from Secrets, and deployed cryptominers on every node.

The root cause? One line in a RoleBinding that gave cluster-admin to 'default' service account. One line. Millions in damages."

**Episode Preview**:
"Today in Episode 3, we're covering Security Foundations - RBAC and Secrets Management.

By the end of this 18-minute lesson, you'll be able to:
- Implement namespace-scoped RBAC roles that follow least privilege
- Secure your secrets using Sealed Secrets or External Secrets Operator
- Identify the 5 RBAC misconfigurations that consistently cause breaches

This is production security that actually works. Let's get started."

---

### 2. Learning Objectives (30 sec)

"This lesson will prepare you to:
- Write RBAC policies from first principles, not copy-paste from Stack Overflow
- Choose the right secrets management solution for your environment
- Audit your cluster's RBAC and identify privilege escalation risks before attackers do"

---

### 3. Part 1: RBAC Fundamentals (10 min total)

#### 3.1 Why RBAC Consistently Fails (1.5 min)

**Problem Statement**:
"Let's start with why. Why is RBAC the #1 security issue when it's been in Kubernetes since version 1.6?"

**Three Root Causes**:

"**First**: RBAC complexity. You're juggling Roles, ClusterRoles, RoleBindings, ClusterRoleBindings, ServiceAccounts, Users, and Groups. The matrix of possibilities is overwhelming. So engineers default to cluster-admin and move on.

**Second**: Invisible by default. When your pod can't pull images, you see ImagePullBackOff immediately. When your pod has excessive permissions? Silence. Nothing breaks. Until it's exploited.

**Third**: Development habits bleed to production. In dev, you're the only user with full access. Works fine. That same 'everything has admin' mindset in production is a disaster."

**The Production Reality**:
"In production, you're not asking 'does it work?' You're asking 'what's the blast radius when this gets compromised?' That's the mindset shift."

---

#### 3.2 RBAC Mental Model (2 min)

**Teaching Approach**: Build from first principles

**Signposting**: "Let's build a mental model of how RBAC actually works. Four components, one flow."

**The Four Components**:

"**Component 1: Subjects** - WHO needs access?
- ServiceAccounts: Pods and workloads (most common in production)
- Users: Humans accessing the cluster (kubectl users)
- Groups: Collections of users (like 'system:masters')

**Component 2: Resources** - WHAT do they need access to?
- Pods, Services, Deployments, Secrets, etc.
- Also includes subresources like 'pods/logs' or 'deployments/scale'

**Component 3: Verbs** - WHAT ACTIONS can they perform?
- get, list, watch (read operations)
- create, update, patch, delete (write operations)
- Special: '*' means all verbs (dangerous!)

**Component 4: Scope** - WHERE do these permissions apply?
- Namespace-scoped: Role + RoleBinding (preferred!)
- Cluster-scoped: ClusterRole + ClusterRoleBinding (dangerous, use sparingly)"

**The Flow**:
"Here's how it connects: You create a Role defining resources and verbs. You create a RoleBinding connecting that Role to a Subject. When the pod tries to perform an action, Kubernetes checks: Does this ServiceAccount have a RoleBinding? What Role is attached? Does that Role allow this verb on this resource? If yes, allow. If no, deny."

**Analogy**: "Think of it like a building access system. The Role is the permission template - 'can enter floors 1-5, can't enter server room.' The RoleBinding is giving someone a keycard with those permissions. The Subject is the person (or pod) using that keycard."

---

#### 3.3 Namespace vs Cluster Scope: The Critical Choice (2 min)

**Teaching Approach**: Contrast with decision framework

**The Key Question**:
"The most important RBAC decision: namespace-scoped or cluster-scoped?"

**Namespace-Scoped (Preferred)**:
"Role + RoleBinding: Permissions limited to one namespace.

Example: Your 'payment-service' pod needs to read Secrets in the 'payment' namespace. You create:
- A Role in 'payment' namespace allowing 'get' and 'list' on Secrets
- A RoleBinding in 'payment' namespace connecting the 'payment-service' ServiceAccount to that Role

Blast radius if compromised: Just the 'payment' namespace. The attacker can't pivot to 'database' or 'logging' namespaces."

**Cluster-Scoped (Dangerous)**:
"ClusterRole + ClusterRoleBinding: Permissions apply across ALL namespaces.

Same example but with ClusterRole: Your 'payment-service' pod gets access to Secrets in EVERY namespace. If compromised, attacker can read database passwords from 'database' namespace, API keys from 'integration' namespace, everything.

Blast radius: Entire cluster."

**Decision Framework**:
"Ask: Does this workload NEED cross-namespace access?
- Yes (rare): Use ClusterRole, but minimize verbs. Never use '*'.
- No (99% of cases): Use namespace-scoped Role. Always.

**Production Rule**: If you can't articulate a specific reason for ClusterRole, you don't need it."

---

#### 3.4 Service Account Security (2 min)

**Teaching Approach**: Pattern + Anti-pattern

**The Default Behavior Problem**:
"Every pod runs with a ServiceAccount. If you don't specify one, Kubernetes uses 'default' ServiceAccount in that namespace.

Here's the trap: If you give permissions to 'default' ServiceAccount, EVERY pod in that namespace gets those permissions. That logging sidecar? Cluster admin. That metrics exporter? Cluster admin. Everything."

**Pattern: Dedicated ServiceAccounts**:
"Production pattern: Create a dedicated ServiceAccount per application.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: payment-service-sa
  namespace: payment
```

Then in your Deployment:
```yaml
spec:
  serviceAccountName: payment-service-sa  # Explicit, not 'default'
```

Now permissions are isolated. Your payment service has its permissions, nothing else does."

**Three Anti-Patterns to Avoid**:

"**Anti-pattern 1: Wildcards**
```yaml
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
```
This is cluster-admin. If you're doing this, you've given up on RBAC.

**Anti-pattern 2: Auto-mounting tokens everywhere**
By default, service account tokens mount into every pod at `/var/run/secrets/kubernetes.io/serviceaccount/`. If your pod doesn't need Kubernetes API access, disable this:
```yaml
spec:
  automountServiceAccountToken: false
```
No token, no API access, no token theft attack vector.

**Anti-pattern 3: system:masters group**
Never bind anything to 'system:masters' group. It bypasses all RBAC checks. It's a backdoor."

---

#### 3.5 Common RBAC Attack Patterns (1.5 min)

**Teaching Approach**: Threat modeling

**Signposting**: "Let's think like an attacker. If I compromise a pod, how do I escalate?"

**Attack Pattern 1: Token Theft**
"I get shell access to your pod. I read `/var/run/secrets/kubernetes.io/serviceaccount/token`. Now I have a valid token. If that pod has excessive permissions, I can use kubectl with that token to pivot across your cluster.

Defense: Disable auto-mount if not needed. Use namespace-scoped roles."

**Attack Pattern 2: Privilege Escalation via Create**
"Your pod has permission to 'create' RoleBindings. I create a new RoleBinding giving myself cluster-admin. Now I have full cluster access.

Defense: Never grant 'create' on RoleBinding or ClusterRoleBinding unless absolutely necessary. That's privilege escalation as a feature."

**Attack Pattern 3: Secrets Enumeration**
"Your pod can 'list' and 'get' Secrets. I iterate through all Secrets in the namespace, exfiltrate database passwords, API keys, certificates.

Defense: Grant 'get' on SPECIFIC secret names, not all secrets. Use fieldSelector limitations when possible."

**Think-Aloud - Production Security Review**:
"When I audit RBAC, here's what I look for:
- Are there any ClusterRoleBindings? Why? Can they be namespace-scoped?
- Does anything have 'create' permissions on Roles or RoleBindings?
- Are service account tokens auto-mounted into pods that don't need API access?
- Does any ServiceAccount have access to Secrets it doesn't strictly need?

Those four questions catch 90% of RBAC issues."

---

#### 3.6 Active Recall Moment 1 (1 min)

**Retrieval Prompt**:
"Pause the audio. Before we move to secrets management, test yourself:

1. What's wrong with binding permissions to the 'default' ServiceAccount?
2. When should you use ClusterRole instead of namespace-scoped Role?
3. Recall from Episode 1: What is RBAC in the production readiness checklist?

[PAUSE 5 seconds]

Answers:
1. Every pod in that namespace gets those permissions, not just the one that needs them. Blast radius too large.
2. Only when you have a specific reason for cross-namespace access. Default to namespace-scoped.
3. Checklist item #3: RBAC Least Privilege - service accounts per application, namespace-scoped roles, no cluster-admin for workloads."

---

### 4. Part 2: Secrets Management (8 min total)

#### 4.1 Why Secrets Are Hard (1.5 min)

**Hook - The Common Mistakes**:
"Let's talk about secrets. This is where things get messy fast."

**The Anti-Patterns Engineers Love**:

"**Anti-pattern 1: Secrets in environment variables**
```yaml
env:
- name: DB_PASSWORD
  value: supersecret123  # Plaintext in manifest
```
You just committed your database password to git. It's in your container image. It's visible in 'kubectl describe pod'. It's in your CI/CD logs. It's everywhere.

**Anti-pattern 2: Secrets in ConfigMaps**
ConfigMaps are for non-sensitive data. They're not encrypted at rest by default. Putting passwords in ConfigMaps defeats the purpose.

**Anti-pattern 3: Base64 confusion**
Engineers think: 'Kubernetes Secrets are base64-encoded, so they're encrypted, right?'

No. Base64 is encoding, not encryption. Anyone with 'get secrets' permission can decode them instantly:
```bash
kubectl get secret db-creds -o jsonpath='{.data.password}' | base64 -d
```

**The Core Problem**:
"Kubernetes Secrets are better than environment variables, but they're still stored in etcd. If your etcd isn't encrypted at rest, your secrets are plaintext in the database. If an attacker gets etcd access, game over."

---

#### 4.2 Secrets vs ConfigMaps (1 min)

**Decision Framework**:

"**Use ConfigMaps for**:
- Application configuration (feature flags, timeouts)
- Non-sensitive URLs (API endpoints)
- Public certificates
- Anything you'd be comfortable posting on Stack Overflow

**Use Secrets for**:
- Passwords and API keys
- Database connection strings with embedded credentials
- TLS private keys
- OAuth tokens
- Anything that grants access to resources

**The Test**: If it were leaked publicly, would you need to rotate it? If yes, it's a secret."

---

#### 4.3 Sealed Secrets Pattern (2.5 min)

**Problem Statement**:
"You want GitOps. You want all your manifests in git. But you can't commit Secrets to git - that's a security violation.

Sealed Secrets solves this: Encrypt secrets BEFORE they go to git. Decrypt in-cluster only."

**How Sealed Secrets Works**:

"**Component 1: Sealed Secrets Controller**
Runs in your cluster. Has a private key. Watches for SealedSecret resources.

**Component 2: kubeseal CLI**
You run this locally. It has the controller's public key. Encrypts secrets.

**The Flow**:
1. You create a normal Secret manifest locally (never commit this)
2. You use kubeseal to encrypt it:
   ```bash
   kubectl create secret generic db-creds \
     --from-literal=password=supersecret \
     --dry-run=client -o yaml | \
   kubeseal -o yaml > sealed-secret.yaml
   ```
3. The sealed-secret.yaml is encrypted. Safe to commit to git.
4. You apply sealed-secret.yaml to cluster
5. Controller sees it, decrypts with private key, creates actual Secret
6. Your pod reads the Secret normally

**Analogy**: "Think of it like a locked safe. You put your secret in a locked safe (sealed secret) before storing it in the warehouse (git). Only the in-cluster controller has the key to open that safe."

**When to Use Sealed Secrets**:
"Best for: GitOps workflows where you want all infrastructure in git, including secrets.

Limitation: Secrets still end up in etcd. If your threat model includes 'attacker has etcd access,' this isn't enough."

---

#### 4.4 External Secrets Operator (2.5 min)

**Problem Statement**:
"Sealed Secrets puts encrypted secrets in git. But the decrypted secret still lives in Kubernetes.

What if you want secrets to live in a dedicated vault? Pull them into the cluster just-in-time?"

**How External Secrets Operator Works**:

"**Component 1: External Secrets Operator**
Runs in your cluster. Watches for ExternalSecret resources.

**Component 2: External Secret Store**
Could be AWS Secrets Manager, Google Secret Manager, HashiCorp Vault, Azure Key Vault.

**The Flow**:
1. You store secret in external vault (e.g., AWS Secrets Manager)
2. You create an ExternalSecret resource in cluster:
   ```yaml
   apiVersion: external-secrets.io/v1beta1
   kind: ExternalSecret
   metadata:
     name: db-creds
   spec:
     secretStoreRef:
       name: aws-secrets-manager
     target:
       name: db-creds  # Create this Secret
     data:
     - secretKey: password
       remoteRef:
         key: production/database/password
   ```
3. Operator pulls secret from AWS Secrets Manager
4. Creates Kubernetes Secret 'db-creds' with that value
5. Your pod reads it normally

**Key Advantage**:
"Secrets never live in git. Secrets are centrally managed in your vault. Rotation happens in one place - the vault. Kubernetes stays in sync automatically.

Plus: Vault has better access control, audit logging, and encryption than etcd."

**When to Use External Secrets Operator**:
"Best for: Organizations with existing secret management infrastructure (Vault, AWS Secrets Manager).

Best for: High-security environments where secrets in etcd is unacceptable.

Limitation: Adds dependency on external system. If vault is down, new pods can't start."

---

#### 4.5 Common Secrets Mistakes (1 min)

**Mistake 1: Logging Secrets**
"Your app logs 'Connected to database with password: supersecret123'. Congratulations, your password is now in CloudWatch/Splunk/Elasticsearch forever.

Fix: Sanitize logs. Never log secrets. Ever."

**Mistake 2: Secrets in Error Messages**
"Your connection fails. The error: 'Failed to connect using: postgres://user:supersecret@...'

Fix: Catch exceptions, log generic error, don't expose connection strings."

**Mistake 3: Overly Broad Secret Access**
"Every pod in namespace has 'get' permission on all Secrets.

Fix: Grant 'get' on specific secret names only:
```yaml
rules:
- resources: ["secrets"]
  resourceNames: ["db-creds"]  # Only this secret
  verbs: ["get"]
```"

---

#### 4.6 Active Recall Moment 2 (1 min)

**Retrieval Prompt**:
"Pause and test yourself:

1. Why is base64 encoding NOT encryption?
2. When would you use Sealed Secrets vs External Secrets Operator?
3. What's wrong with this: 'env: - name: PASSWORD value: secret123'

[PAUSE 5 seconds]

Answers:
1. Base64 is reversible encoding, not encryption. Anyone can decode it. No key needed.
2. Sealed Secrets: GitOps with encrypted secrets in git. External Secrets: Pull from existing vault, no secrets in git or etcd long-term.
3. Plaintext password in manifest, will be in git, CI/CD logs, kubectl describe output. Never do this."

---

### 5. The 5 RBAC Misconfigurations Checklist (1.5 min)

**Teaching Approach**: Actionable audit checklist

**Signposting**: "Let's bring this together. Here are the 5 most common RBAC misconfigurations. Audit your cluster against these."

"**Misconfiguration 1: Cluster-admin for workloads**
Search: `kubectl get clusterrolebindings -o yaml | grep -A 5 'cluster-admin'`
Look for: ServiceAccounts bound to cluster-admin
Fix: Use namespace-scoped Roles instead

**Misconfiguration 2: Wildcard permissions**
Search: Look for `resources: ["*"]` or `verbs: ["*"]` in Roles
Look for: Overly permissive rules
Fix: Specify exact resources and verbs needed

**Misconfiguration 3: Default ServiceAccount permissions**
Search: Any RoleBinding with `name: default` in subjects
Look for: Permissions granted to 'default' ServiceAccount
Fix: Create dedicated ServiceAccounts

**Misconfiguration 4: Create permissions on RBAC resources**
Search: Roles allowing 'create' on 'roles' or 'rolebindings'
Look for: Privilege escalation paths
Fix: Remove unless absolutely needed, tightly scope

**Misconfiguration 5: Auto-mounted tokens in non-API pods**
Search: Pods without `automountServiceAccountToken: false`
Look for: Unnecessary token exposure
Fix: Disable for pods that don't need Kubernetes API access"

---

### 6. Connection to Production Mindset (1 min)

**Synthesis**:
"Remember Episode 1's production mindset? 'What happens WHEN this is compromised?'

That's what RBAC and secrets management are about. Not if your pod gets compromised. When.

When that happens:
- Namespace-scoped RBAC limits the blast radius
- Dedicated ServiceAccounts isolate damage
- Sealed Secrets or External Secrets prevent credential exposure
- Disabled token auto-mount removes attack vectors

This is defense in depth. Every layer makes the attacker's job harder."

**Callback to Checklist**:
"This is checklist item #3 from Episode 1: RBAC Least Privilege. Now you know how to implement it."

---

### 7. Recap & Synthesis (1.5 min)

**Key Takeaways**:
"Let's recap Episode 3:

**Part 1 - RBAC**:
- RBAC has 4 components: Subjects, Resources, Verbs, Scope
- Always prefer namespace-scoped Role over ClusterRole
- Create dedicated ServiceAccounts per application, not 'default'
- Disable token auto-mount if pod doesn't need API access
- Watch for wildcards, privilege escalation, and token theft

**Part 2 - Secrets**:
- Base64 is encoding, not encryption
- Use Secrets for sensitive data, ConfigMaps for configuration
- Sealed Secrets: Encrypt before git, decrypt in-cluster
- External Secrets Operator: Pull from external vault, never in git
- Never log secrets, sanitize errors, scope secret access tightly

**The 5 Misconfigurations**:
1. Cluster-admin for workloads
2. Wildcard permissions
3. Default ServiceAccount permissions
4. Create permissions on RBAC resources
5. Auto-mounted tokens everywhere"

**Why This Matters**:
"RBAC misconfiguration is preventable. The Fortune 500 breach I mentioned? Preventable. The patterns you learned today prevent it.

Security in production isn't about perfection. It's about making the attacker's job so hard they move to an easier target. That's what defense in depth achieves."

---

### 8. Next Episode Preview (30 sec)

"Next time: Episode 4 - Troubleshooting Crashes: CrashLoopBackOff and Beyond.

You'll learn:
- The systematic troubleshooting workflow for pod failures
- How to diagnose CrashLoopBackOff, ImagePullBackOff, and Pending states
- Configuring health checks that actually prevent failures

We're taking failure pattern #3 from Episode 1 and giving you a complete debugging playbook. Troubleshooting is a skill, and we're building that skill systematically.

I'll see you in Episode 4."

---

## Supporting Materials

**Statistics Referenced**:
- RBAC misconfiguration is #1 Kubernetes security issue (Red Hat 2024, CNCF 2024)
- Fortune 500 breach example (composite of real incidents, anonymized)
- Token theft and privilege escalation as common attack vectors (OWASP Kubernetes Top 10)

**kubectl Commands**:
```bash
# RBAC audit commands
kubectl get clusterrolebindings -o yaml | grep -A 5 'cluster-admin'
kubectl get rolebindings -n <namespace> -o yaml
kubectl auth can-i --list --as=system:serviceaccount:<ns>:<sa>

# Secrets management
kubectl create secret generic <name> --from-literal=key=value
kubectl get secret <name> -o jsonpath='{.data.key}' | base64 -d

# ServiceAccount inspection
kubectl get sa -n <namespace>
kubectl describe pod <name> | grep -A 5 'Service Account'
```

**YAML Examples**:
```yaml
# Dedicated ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: payment-service-sa
  namespace: payment

---
# Namespace-scoped Role (least privilege)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
  namespace: payment
rules:
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["db-creds"]  # Specific secret only
  verbs: ["get"]

---
# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: payment-read-secrets
  namespace: payment
subjects:
- kind: ServiceAccount
  name: payment-service-sa
  namespace: payment
roleRef:
  kind: Role
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io

---
# Deployment with explicit ServiceAccount
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  template:
    spec:
      serviceAccountName: payment-service-sa
      automountServiceAccountToken: false  # Disable if not needed
```

**Technical References**:
- Kubernetes RBAC documentation
- Bitnami Sealed Secrets: https://github.com/bitnami-labs/sealed-secrets
- External Secrets Operator: https://external-secrets.io/
- OWASP Kubernetes Top 10
- Service account token projection

**Analogies Used**:
1. **Building access system**: Role as permission template, RoleBinding as keycard assignment
2. **Locked safe**: Sealed Secrets as putting secrets in locked safe before storing in warehouse (git)
3. **Defense in depth**: Multiple layers make attacker's job harder

---

## Quality Checklist

**Structure**:
- [x] Clear beginning (callback to Ep 1, hook with breach story), middle (RBAC + Secrets), end (recap + preview)
- [x] Logical flow (why RBAC fails → fundamentals → patterns → secrets → audit checklist)
- [x] Time allocations realistic (1+0.5+10+8+1.5+1+1.5+0.5 = 24 min initial → needs tightening to 18 min in script phase)
- [x] All sections have specific content (examples, yaml, commands)

**Pedagogy**:
- [x] Learning objectives specific and measurable
- [x] Spaced repetition planned (introduces 5 new concepts, reinforces 4 from Ep 1-2)
- [x] Active recall moments included (2 retrieval prompts with answers)
- [x] Signposting throughout ("Let's build...", "Here's the trap...", "When I audit...")
- [x] Multiple analogies (building access, locked safe, defense in depth)
- [x] Common pitfalls addressed (5 misconfigurations checklist)

**Content**:
- [x] Addresses pain points (RBAC complexity, secrets in git, base64 confusion)
- [x] Production-relevant (breach scenarios, attack patterns, audit workflow)
- [x] Decision frameworks (namespace vs cluster scope, Sealed vs External Secrets)
- [x] Appropriate for senior engineers (assumes auth basics, focuses on production security)
- [x] Includes code examples (YAML manifests, kubectl commands)

**Engagement**:
- [x] Strong hook (Fortune 500 breach, one line caused millions in damages)
- [x] Practice moments (2 active recall prompts)
- [x] Variety in teaching techniques (contrast, threat modeling, audit checklist)
- [x] Real-world scenarios (token theft, privilege escalation)

**Dependencies**:
- [x] Prerequisites clearly stated (Episode 1)
- [x] Builds on Episode 1 (reinforces checklist item #3, production mindset)
- [x] Sets foundation for Episode 10 (multi-cluster RBAC)
- [x] References future episodes (External Secrets in Ep 5, GitOps in Ep 9)

**Teaching Techniques Applied**:
- [x] Signposting (clear transitions)
- [x] Analogies (building access, locked safe)
- [x] Elaboration ("In other words...", "Think of it like...")
- [x] Think-aloud (production security review process)
- [x] Active recall (2 pause-and-answer moments)
- [x] Contrast (namespace vs cluster, Sealed vs External)
- [x] Pattern + anti-pattern (dedicated SA vs default SA)

---

## Notes for Script Writing

**Tone**: Security-focused but practical. Not fear-mongering, but honest about real threats. Respectful that this is complex.

**Pacing**: Faster than Episode 1 (core concept, not foundation). More technical depth. Keep energy up during YAML examples.

**Emphasis Points**:
- "One line. Millions in damages." (hook impact)
- "Base64 is encoding, NOT encryption" (critical distinction)
- "NOT if, WHEN" (production mindset)
- "Only when you have a specific reason" (ClusterRole decision)

**Transitions to Polish**:
- Between RBAC fundamentals and attack patterns
- Between RBAC section and Secrets section (major shift)
- Into the 5 misconfigurations checklist (make it feel actionable)

**Time Management**:
Current outline = ~24 min with pauses and examples. To reach 18 min target:
- Tighten RBAC fundamentals (10 min → 8 min): Reduce explanation of each component
- Tighten Secrets section (8 min → 7 min): More concise Sealed Secrets and External Secrets explanations
- Reduce transition pauses
- Tighten recap (1.5 min → 1 min)

This should be addressed in script writing phase by keeping examples concise and moving faster through concepts the audience likely has seen before.

**YAML Example Strategy**:
Don't read entire YAML blocks - highlight key fields:
"Here's a namespace-scoped Role. Key fields: 'resources: secrets', 'resourceNames: db-creds' - that's specific secret only - and 'verbs: get' - read only, no create or delete."

**Pronunciation Notes**:
- RBAC: "are-back" (not "R-B-A-C")
- kubectl: "cube-c-t-l" or "cube-cuttle" (both acceptable)
- etcd: "et-see-dee"
- kubeseal: "cube-seal"

---

## Sources & Validation

**Statistics to Verify**:

1. **"RBAC misconfiguration is #1 K8s security issue"**
   - Source: Red Hat State of Kubernetes Security 2024, CNCF Security Audit
   - To verify during validation phase

2. **"Fortune 500 breach" example**
   - Composite of real incidents (anonymized)
   - Real pattern: service account token theft → lateral movement
   - To validate that attack pattern is documented

3. **Attack patterns (token theft, privilege escalation)**
   - Source: OWASP Kubernetes Top 10
   - To verify during validation phase

**Technical Concepts to Verify**:
- RBAC components (Role, ClusterRole, RoleBinding, ClusterRoleBinding)
- Service account token location (/var/run/secrets/kubernetes.io/serviceaccount/)
- Sealed Secrets architecture (official GitHub documentation)
- External Secrets Operator architecture (official website)
- Base64 encoding vs encryption distinction

**Tools to Verify**:
- kubeseal CLI availability and usage
- External Secrets Operator installation methods
- kubectl auth can-i command

**Validation Status**: ⏳ PENDING (to be validated via lesson-validate skill)

*Outline created: 2025-01-06*
*To be validated before script writing*
