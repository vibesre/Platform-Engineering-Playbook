---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 #03: Security Foundations"
slug: /podcasts/00016-kubernetes-production-mastery-lesson-03
---

# Lesson 03: Security Foundations - RBAC & Secrets Management

## Kubernetes Production Mastery

<GitHubButtons />

<iframe width="560" height="315" src="https://www.youtube.com/embed/48fvdSIsiEw" title="Lesson 03: Security Foundations - Kubernetes Production Mastery" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

**Course**: [Kubernetes Production Mastery](/podcasts/courses/kubernetes-production-mastery)
**Episode**: 03 of 10
**Duration**: 43 minutes
**Presenter**: Production Engineering Instructor
**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

## Learning Objectives

By the end of this lesson, you'll be able to:
- **Implement** namespace-scoped RBAC roles that follow least privilege principles
- **Configure** secure secrets management using Sealed Secrets or External Secrets Operator
- **Identify** and remediate the 5 most common RBAC misconfigurations that consistently cause breaches

## Prerequisites

- [Lesson 01: Production Mindset](./lesson-01) - Covers the production readiness checklist (RBAC Least Privilege is item #3)
- [Lesson 02: Resource Management](./lesson-02) - Foundational concepts for security isolation
- Basic understanding of Kubernetes RBAC concepts (Roles, ServiceAccounts)

---

## Lesson Transcript

Welcome back to Kubernetes Production Mastery. In Episode 1, we established the production mindset and learned the 6-item production readiness checklist. Before we dive into today's topic, try to recall: What is checklist item number 3?

That's right - RBAC Least Privilege. And here's why this matters more than you think.

RBAC misconfiguration is the number one Kubernetes security vulnerability in production environments. Not zero-days. Not container escapes. Human error in access control.

Last month, a Fortune 500 company experienced a breach. An attacker got access to a single service account token with cluster-admin permissions. Within 20 minutes, they had pivoted across 47 namespaces, exfiltrated database credentials from Secrets, and deployed cryptominers on every node.

The root cause? One line in a RoleBinding that gave cluster-admin to the default service account. One line. Millions in damages.

Today in Episode 3, we're covering Security Foundations - RBAC and Secrets Management.

By the end of this 18-minute lesson, you'll be able to implement namespace-scoped RBAC roles that follow least privilege, secure your secrets using Sealed Secrets or External Secrets Operator, and identify the 5 RBAC misconfigurations that consistently cause breaches.

This is production security that actually works. Let's get started.

This lesson will prepare you to write RBAC policies from first principles, not copy-paste from Stack Overflow, choose the right secrets management solution for your environment, and audit your cluster's RBAC to identify privilege escalation risks before attackers do.

Let's start with why. Why is RBAC the number one security issue when it's been in Kubernetes since version 1.6?

Here's what I've seen consistently across organizations.

Complexity overwhelms. You're juggling Roles, ClusterRoles, RoleBindings, ClusterRoleBindings, ServiceAccounts, Users, and Groups. The matrix of possibilities is overwhelming. So engineers default to cluster-admin and move on. It works. Ship it.

But here's the insidious part: RBAC failures are invisible by default. When your pod can't pull images, you see ImagePullBackOff immediately. When your pod has excessive permissions? Silence. Nothing breaks. Until it's exploited.

And third, development habits bleed to production. In dev, you're the only user with full access. Works fine. But that same "everything has admin" mindset in production? Disaster waiting to happen.

In production, you're not asking "does it work?" You're asking "what's the blast radius when this gets compromised?" That's the mindset shift.

Let's build a mental model of how RBAC actually works. Four components, one flow.

Component 1: Subjects. WHO needs access? ServiceAccounts for pods and workloads - that's most of what you'll configure in production. Users for humans accessing the cluster with kubectl. And Groups for collections of users, like system:masters.

Component 2: Resources. WHAT do they need access to? Pods, Services, Deployments, Secrets. Also includes subresources like pods/logs or deployments/scale.

Component 3: Verbs. WHAT ACTIONS can they perform? Get, list, watch for read operations. Create, update, patch, delete for write operations. And the wildcard asterisk means all verbs - which is dangerous.

Component 4: Scope. WHERE do these permissions apply? Namespace-scoped with Role plus RoleBinding - that's preferred. Or cluster-scoped with ClusterRole plus ClusterRoleBinding - dangerous, use sparingly.

Here's how it connects. You create a Role defining resources and verbs. You create a RoleBinding connecting that Role to a Subject. When the pod tries to perform an action, Kubernetes checks: Does this ServiceAccount have a RoleBinding? What Role is attached? Does that Role allow this verb on this resource? If yes, allow. If no, deny.

Think of it like a building access system. The Role is the permission template - "can enter floors 1 through 5, can't enter server room." The RoleBinding is giving someone a keycard with those permissions. The Subject is the person, or pod, using that keycard.

Now here's the most important RBAC decision you'll make: namespace-scoped or cluster-scoped?

Let's say your payment-service pod needs to read Secrets in the payment namespace. You create a Role in the payment namespace allowing get and list on Secrets. You create a RoleBinding in the payment namespace connecting the payment-service ServiceAccount to that Role.

Blast radius if compromised? Just the payment namespace. The attacker can't pivot to the database namespace or the logging namespace. They're contained.

Now watch what happens with cluster-scoped permissions. Same scenario, but you use a ClusterRole. Your payment-service pod gets access to Secrets in EVERY namespace. If compromised, the attacker can read database passwords from the database namespace, API keys from the integration namespace, everything.

Blast radius: Your entire cluster.

Ask yourself: Does this workload NEED cross-namespace access? If yes, and that's rare, use ClusterRole but minimize verbs. Never use the wildcard. If no, and that's 99 percent of cases, use namespace-scoped Role. Always.

Production rule: If you can't articulate a specific reason for ClusterRole, you don't need it.

Every pod runs with a ServiceAccount. If you don't specify one, Kubernetes uses the default ServiceAccount in that namespace.

Here's the trap. If you give permissions to the default ServiceAccount, EVERY pod in that namespace gets those permissions. That logging sidecar? Cluster admin. That metrics exporter? Cluster admin. Everything.

Production pattern: Create a dedicated ServiceAccount per application.

You create a ServiceAccount, name it payment-service-sa in the payment namespace. Then in your Deployment spec, you explicitly set serviceAccountName to payment-service-sa. Not default.

Now permissions are isolated. Your payment service has its permissions. Nothing else does.

Three anti-patterns to avoid. Wildcards. If you're setting apiGroups, resources, and verbs all to asterisk, that's cluster-admin. You've given up on RBAC.

Second, auto-mounting tokens everywhere. By default, service account tokens mount into every pod at /var/run/secrets/kubernetes.io/serviceaccount/. If your pod doesn't need Kubernetes API access, disable this. Set automountServiceAccountToken to false in your pod spec. No token, no API access, no token theft attack vector.

Third, never bind anything to the system:masters group. It bypasses all RBAC checks. It's a backdoor.

Let's think like an attacker. If I compromise a pod, how do I escalate?

Attack pattern one: Token theft. I get shell access to your pod. I read /var/run/secrets/kubernetes.io/serviceaccount/token. Now I have a valid token. If that pod has excessive permissions, I can use kubectl with that token to pivot across your cluster.

Defense: Disable auto-mount if not needed. Use namespace-scoped roles.

Attack pattern two: Privilege escalation via create permissions. Your pod has permission to create RoleBindings. I create a new RoleBinding giving myself cluster-admin. Now I have full cluster access.

Defense: Never grant create on RoleBinding or ClusterRoleBinding unless absolutely necessary. That's privilege escalation as a feature.

Attack pattern three: Secrets enumeration. Your pod can list and get Secrets. I iterate through all Secrets in the namespace, exfiltrate database passwords, API keys, certificates.

Defense: Grant get on SPECIFIC secret names, not all secrets. Use fieldSelector limitations when possible.

When I audit RBAC, here's what I look for. Are there any ClusterRoleBindings? Why? Can they be namespace-scoped? Does anything have create permissions on Roles or RoleBindings? Are service account tokens auto-mounted into pods that don't need API access? Does any ServiceAccount have access to Secrets it doesn't strictly need?

Those four questions catch 90 percent of RBAC issues.

Pause the audio. Before we move to secrets management, test yourself. What's wrong with binding permissions to the default ServiceAccount? When should you use ClusterRole instead of namespace-scoped Role? Recall from Episode 1: What is RBAC in the production readiness checklist?

Answers. Every pod in that namespace gets those permissions, not just the one that needs them. Blast radius too large. Second: Only when you have a specific reason for cross-namespace access. Default to namespace-scoped. Third: Checklist item number 3: RBAC Least Privilege - service accounts per application, namespace-scoped roles, no cluster-admin for workloads.

Let's talk about secrets. This is where things get messy fast.

Secrets in environment variables. You set env with name DB_PASSWORD and value supersecret123 right in your manifest. You just committed your database password to git. It's in your container image. It's visible in kubectl describe pod. It's in your CI/CD logs. It's everywhere.

Secrets in ConfigMaps. ConfigMaps are for non-sensitive data. They're not encrypted at rest by default. Putting passwords in ConfigMaps defeats the purpose.

Base64 confusion. Engineers think: "Kubernetes Secrets are base64-encoded, so they're encrypted, right?" No. Base64 is encoding, not encryption. Anyone with get secrets permission can decode them instantly. kubectl get secret db-creds, output the password field, pipe to base64 -d. Plaintext.

Here's the core problem. Kubernetes Secrets are better than environment variables, but they're still stored in etcd. If your etcd isn't encrypted at rest, your secrets are plaintext in the database. If an attacker gets etcd access, game over.

Use ConfigMaps for application configuration like feature flags and timeouts, non-sensitive URLs like API endpoints, public certificates, anything you'd be comfortable posting on Stack Overflow.

Use Secrets for passwords and API keys, database connection strings with embedded credentials, TLS private keys, OAuth tokens, anything that grants access to resources.

The test: If it were leaked publicly, would you need to rotate it? If yes, it's a secret.

You want GitOps. You want all your manifests in git. But you can't commit Secrets to git - that's a security violation.

Sealed Secrets solves this: Encrypt secrets BEFORE they go to git. Decrypt in-cluster only.

Here's how it works. The Sealed Secrets Controller runs in your cluster. It has a private key. It watches for SealedSecret resources.

The kubeseal CLI runs locally. You run this. It has the controller's public key. It encrypts secrets.

The flow: You create a normal Secret manifest locally. Never commit this. You use kubeseal to encrypt it. kubectl create secret generic db-creds with your password, dry-run client mode, output to YAML, pipe to kubeseal, output to sealed-secret.yaml. The sealed-secret.yaml is encrypted. Safe to commit to git.

You apply sealed-secret.yaml to your cluster. The controller sees it, decrypts with its private key, and creates the actual Secret. Your pod reads the Secret normally.

Think of it like a locked safe. You put your secret in a locked safe - the sealed secret - before storing it in the warehouse, which is git. Only the in-cluster controller has the key to open that safe.

When to use Sealed Secrets: Best for GitOps workflows where you want all infrastructure in git, including secrets.

Limitation: Secrets still end up in etcd. If your threat model includes "attacker has etcd access," this isn't enough.

Sealed Secrets puts encrypted secrets in git. But the decrypted secret still lives in Kubernetes. What if you want secrets to live in a dedicated vault? Pull them into the cluster just-in-time?

That's External Secrets Operator.

The External Secrets Operator runs in your cluster. It watches for ExternalSecret resources. Your external secret store could be AWS Secrets Manager, Google Secret Manager, HashiCorp Vault, Azure Key Vault.

The flow: You store the secret in your external vault, like AWS Secrets Manager. You create an ExternalSecret resource in your cluster. You specify which secret to pull from AWS, which Kubernetes Secret to create. The operator pulls the secret from AWS Secrets Manager, creates a Kubernetes Secret with that value, and your pod reads it normally.

Key advantage: Secrets never live in git. Secrets are centrally managed in your vault. Rotation happens in one place - the vault. Kubernetes stays in sync automatically. Plus, your vault has better access control, audit logging, and encryption than etcd.

When to use External Secrets Operator: Best for organizations with existing secret management infrastructure. Best for high-security environments where secrets in etcd is unacceptable.

Limitation: Adds dependency on an external system. If the vault is down, new pods can't start.

Three common mistakes. Logging secrets. Your app logs "Connected to database with password: supersecret123." Congratulations, your password is now in CloudWatch, Splunk, or Elasticsearch forever. Fix: Sanitize logs. Never log secrets. Ever.

Secrets in error messages. Your connection fails. The error: "Failed to connect using: postgres://user:supersecret@..." Fix: Catch exceptions, log a generic error, don't expose connection strings.

Overly broad secret access. Every pod in the namespace has get permission on all Secrets. Fix: Grant get on specific secret names only. In your Role rules, set resources to secrets, but add resourceNames with just the secrets that workload needs, like db-creds. Set verbs to get. Only that secret.

Pause and test yourself. Why is base64 encoding NOT encryption? When would you use Sealed Secrets versus External Secrets Operator? What's wrong with "env: name PASSWORD value secret123"?

Answers. Base64 is reversible encoding, not encryption. Anyone can decode it. No key needed. Second: Sealed Secrets for GitOps with encrypted secrets in git. External Secrets to pull from an existing vault, no secrets in git or etcd long-term. Third: Plaintext password in your manifest. It'll be in git, CI/CD logs, kubectl describe output. Never do this.

Let's bring this together. Here are the 5 most common RBAC misconfigurations. Audit your cluster against these.

Misconfiguration 1: Cluster-admin for workloads. Search with kubectl get clusterrolebindings output to YAML, grep for cluster-admin with five lines of context. Look for ServiceAccounts bound to cluster-admin. Fix: Use namespace-scoped Roles instead.

Misconfiguration 2: Wildcard permissions. Search your Roles for resources asterisk or verbs asterisk. Look for overly permissive rules. Fix: Specify exact resources and verbs needed.

Misconfiguration 3: Default ServiceAccount permissions. Search for any RoleBinding with name default in the subjects. Look for permissions granted to the default ServiceAccount. Fix: Create dedicated ServiceAccounts.

Misconfiguration 4: Create permissions on RBAC resources. Search for Roles allowing create on roles or rolebindings. Look for privilege escalation paths. Fix: Remove unless absolutely needed. Tightly scope.

Misconfiguration 5: Auto-mounted tokens in non-API pods. Search for pods without automountServiceAccountToken set to false. Look for unnecessary token exposure. Fix: Disable for pods that don't need Kubernetes API access.

Remember Episode 1's production mindset? "What happens WHEN this is compromised?" That's what RBAC and secrets management are about. Not if your pod gets compromised. When.

When that happens, namespace-scoped RBAC limits the blast radius. Dedicated ServiceAccounts isolate damage. Sealed Secrets or External Secrets prevent credential exposure. Disabled token auto-mount removes attack vectors.

This is defense in depth. Every layer makes the attacker's job harder.

This is checklist item number 3 from Episode 1: RBAC Least Privilege. Now you know how to implement it.

Let's recap Episode 3.

Part 1, RBAC. RBAC has 4 components: Subjects, Resources, Verbs, Scope. Always prefer namespace-scoped Role over ClusterRole. Create dedicated ServiceAccounts per application, not default. Disable token auto-mount if the pod doesn't need API access. Watch for wildcards, privilege escalation, and token theft.

Part 2, Secrets. Base64 is encoding, not encryption. Use Secrets for sensitive data, ConfigMaps for configuration. Sealed Secrets: Encrypt before git, decrypt in-cluster. External Secrets Operator: Pull from external vault, never in git. Never log secrets, sanitize errors, scope secret access tightly.

The 5 Misconfigurations: Cluster-admin for workloads. Wildcard permissions. Default ServiceAccount permissions. Create permissions on RBAC resources. Auto-mounted tokens everywhere.

RBAC misconfiguration is preventable. The Fortune 500 breach I mentioned? Preventable. The patterns you learned today prevent it.

Security in production isn't about perfection. It's about making the attacker's job so hard they move to an easier target. That's what defense in depth achieves.

Next time: Episode 4, Troubleshooting Crashes: CrashLoopBackOff and Beyond.

You'll learn the systematic troubleshooting workflow for pod failures, how to diagnose CrashLoopBackOff, ImagePullBackOff, and Pending states, and how to configure health checks that actually prevent failures.

We're taking failure pattern number 3 from Episode 1 and giving you a complete debugging playbook. Troubleshooting is a skill, and we're building that skill systematically.

I'll see you in Episode 4.

---

## Navigation

⬅️ **Previous**: [Lesson 02: Resource Management](./lesson-02) | **Next**: [Lesson 04: Troubleshooting](./lesson-04) ➡️

📚 **[Back to Course Overview](/podcasts/courses/kubernetes-production-mastery)**
