# Open Policy Agent (OPA)

<GitHubButtons />
## 📚 Learning Resources

### 📖 Essential Documentation
- [OPA Documentation](https://www.openpolicyagent.org/docs/latest/) - Official comprehensive documentation
- [Rego Language Reference](https://www.openpolicyagent.org/docs/latest/policy-reference/) - Complete policy language guide
- [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/) - Kubernetes-native policy enforcement
- [Policy Testing](https://www.openpolicyagent.org/docs/latest/policy-testing/) - Testing and validation frameworks

### 📝 Specialized Guides
- [Kubernetes Admission Control](https://www.openpolicyagent.org/docs/latest/kubernetes-introduction/) - Policy enforcement in K8s clusters
- [OPA Best Practices](https://www.styra.com/blog/opa-best-practices/) - Policy design and implementation patterns
- [Policy as Code](https://www.openpolicyagent.org/docs/latest/philosophy/) - Principles and methodologies
- [Security Policies](https://github.com/open-policy-agent/library) - Community policy library with examples

### 🎥 Video Tutorials
- [OPA Deep Dive](https://www.youtube.com/watch?v=videoid) - Architecture and use cases (45 min)
- [Rego Language Tutorial](https://www.youtube.com/watch?v=videoid2) - Policy writing fundamentals (35 min)
- [Kubernetes Policy Enforcement](https://www.youtube.com/watch?v=videoid3) - Gatekeeper implementation (40 min)

### 🎓 Professional Courses
- [OPA Fundamentals](https://academy.styra.com/) - Free Styra Academy course
- [Policy as Code with OPA](https://www.udemy.com/course/opa-policy/) - Paid comprehensive training
- [Kubernetes Security](https://training.linuxfoundation.org/training/kubernetes-security-essentials-lfs260/) - Linux Foundation (includes OPA)

### 📚 Books
- "Policy as Code" by Jim Bugwadia - [Purchase on Amazon](https://www.amazon.com/dp/1098139186)
- "Kubernetes Security and Observability" by Brendan Creane - [Purchase on Amazon](https://www.amazon.com/dp/1098105095)
- "Zero Trust Networks" by Evan Gilman - [Purchase on Amazon](https://www.amazon.com/dp/1491962194)

### 🛠️ Interactive Tools
- [OPA Playground](https://play.openpolicyagent.org/) - Interactive Rego policy testing environment
- [OPA CLI](https://www.openpolicyagent.org/docs/latest/cli/) - Command-line policy evaluation and testing
- [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=tsandall.opa) - Rego language support and debugging

### 🚀 Ecosystem Tools
- [OPA Gatekeeper](https://github.com/open-policy-agent/gatekeeper) - 3.5k⭐ Kubernetes policy controller
- [Conftest](https://www.conftest.dev/) - Configuration testing with OPA policies
- [Styra DAS](https://www.styra.com/) - Enterprise policy management platform
- [OPA Envoy Plugin](https://github.com/open-policy-agent/opa-envoy-plugin) - Service mesh policy enforcement

### 🌐 Community & Support
- [OPA Community](https://www.openpolicyagent.org/community/) - Official community resources
- [OPA Slack](https://slack.openpolicyagent.org/) - Community discussions and support
- [Policy Library](https://github.com/open-policy-agent/library) - Community-contributed policies

## Understanding OPA: Policy as Code for Everything

Open Policy Agent (OPA) is a general-purpose policy engine that enables unified, context-aware policy enforcement across the entire stack. OPA decouples policy decision-making from policy enforcement, allowing you to define policies as code using a high-level declarative language called Rego.

### How OPA Works
OPA operates as a lightweight policy engine that evaluates policies written in Rego against structured data. Applications query OPA with JSON input representing the current context, and OPA responds with policy decisions. This decoupling allows the same policy engine to work across different systems and technologies.

The engine is stateless and embeddable, meaning it can run as a sidecar, library, or service. OPA policies are data-driven and declarative, focusing on what should be allowed rather than how to enforce it. This makes policies easier to understand, test, and maintain.

### The OPA Ecosystem
OPA's ecosystem includes tools for different deployment patterns and use cases. Gatekeeper provides Kubernetes-native policy enforcement using Custom Resource Definitions. Conftest enables policy testing for configuration files and infrastructure as code.

The ecosystem spans from admission controllers and API gateways to CI/CD pipelines and infrastructure provisioning. Integration points include Kubernetes, Envoy service mesh, Terraform, Docker, and cloud platforms, making OPA a universal policy layer.

### Why OPA Dominates Policy Enforcement
OPA has become the standard for policy as code due to its flexibility and power. Unlike rigid rule engines tied to specific platforms, OPA provides a universal policy language that works everywhere. Its JSON-based approach makes it natural for modern applications and cloud-native environments.

The separation of policy from enforcement means teams can centralize policy management while distributing enforcement points. This architectural pattern enables consistent security and compliance across heterogeneous environments.

### Mental Model for Success
Think of OPA like a universal translator for rules and policies. Instead of each system having its own way of expressing rules, OPA provides a common language (Rego) that can evaluate policies for any system that speaks JSON.

It's like having a security guard who understands the same rulebook whether they're working at the front door (API gateway), in the building (Kubernetes), or in the parking garage (infrastructure). The rules are consistent, but the enforcement happens where it's needed.

### Where to Start Your Journey
1. **Try the OPA Playground** - Write simple policies online to understand Rego
2. **Learn basic Rego syntax** - Master rules, variables, and data structures
3. **Practice with sample data** - Evaluate policies against JSON input
4. **Deploy OPA locally** - Run the server and make policy queries
5. **Integrate with Kubernetes** - Use Gatekeeper for admission control
6. **Write comprehensive tests** - Ensure policies work correctly

### Key Concepts to Master
- **Rego language** - Policy syntax, rules, and built-in functions
- **Policy evaluation** - How OPA processes queries and returns decisions
- **Data and input** - Structuring context for policy evaluation
- **Testing strategies** - Unit testing and policy validation
- **Bundle management** - Distributing policies across environments
- **Integration patterns** - Embedding OPA in different systems
- **Performance optimization** - Optimizing policies for production workloads
- **Security considerations** - Protecting policy data and decisions

Start with simple allow/deny policies and gradually progress to complex data transformations and multi-input evaluations. Focus on policy design patterns that promote reusability and maintainability.

## Core Concepts

### Policy as Code
- **Declarative Policies**: Define what should be allowed or denied, not how to check it
- **Version Control**: Policies are code, stored in Git repositories
- **Testing**: Unit test policies like any other code
- **Review Process**: Policy changes go through standard code review workflows

### Rego Language
```rego
# Example: Deny containers running as root
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    input.request.object.spec.containers[_].securityContext.runAsUser == 0
    msg := "Containers must not run as root"
}
```

## Architecture

### OPA Components

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Application   │────▶│       OPA       │────▶│     Policies    │
│   (Service)     │◀────│     Engine      │◀────│     (Rego)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                         │
         ▼                       ▼                         ▼
    Input Data            Decision Logs              Policy Bundle
```

### Deployment Models

#### 1. Sidecar Pattern
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-opa
spec:
  containers:
  - name: app
    image: myapp:latest
  - name: opa
    image: openpolicyagent/opa:latest-envoy
    args:
      - "run"
      - "--server"
      - "--config-file=/config/config.yaml"
```

#### 2. Centralized Service
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opa
spec:
  replicas: 3
  selector:
    matchLabels:
      app: opa
  template:
    metadata:
      labels:
        app: opa
    spec:
      containers:
      - name: opa
        image: openpolicyagent/opa:latest
        ports:
        - containerPort: 8181
        args:
          - "run"
          - "--server"
          - "--bundle"
          - "--bundle-url=https://bundle-server.com/bundles/latest"
```

## Kubernetes Integration

### OPA Gatekeeper

OPA Gatekeeper provides native Kubernetes CRDs for policy management:

```yaml
# ConstraintTemplate definition
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required[_]
          not provided[missing]
          msg := sprintf("Label '%v' is required", [missing])
        }
```

### Admission Controller

```yaml
# ValidatingWebhookConfiguration
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: opa-validating-webhook
webhooks:
  - name: validating-webhook.openpolicyagent.org
    clientConfig:
      service:
        name: opa
        namespace: opa-system
        path: "/v1/admit"
    rules:
      - operations: ["CREATE", "UPDATE"]
        apiGroups: ["*"]
        apiVersions: ["*"]
        resources: ["pods", "deployments", "services"]
    admissionReviewVersions: ["v1", "v1beta1"]
```

## Implementation Examples

### 1. Container Image Policy

```rego
package kubernetes.admission

import future.keywords.contains
import future.keywords.if

# Deny containers from untrusted registries
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not trusted_registry(container.image)
    msg := sprintf("Container image '%v' comes from untrusted registry", [container.image])
}

trusted_registry(image) {
    trusted_registries := {
        "gcr.io/my-company/",
        "docker.io/mycompany/",
        "registry.company.com/"
    }
    registry := trusted_registries[_]
    startswith(image, registry)
}
```

### 2. Resource Limits Policy

```rego
package kubernetes.admission

# Require resource limits
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits.memory
    msg := sprintf("Container '%v' must specify memory limits", [container.name])
}

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits.cpu
    msg := sprintf("Container '%v' must specify CPU limits", [container.name])
}

# Enforce maximum resource limits
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    mem_limit := container.resources.limits.memory
    mem_limit_mb := units.parse_bytes(mem_limit) / 1048576
    mem_limit_mb > 8192  # 8GB max
    msg := sprintf("Container '%v' memory limit exceeds maximum of 8GB", [container.name])
}
```

### 3. Network Policy Enforcement

```rego
package kubernetes.admission

# Require NetworkPolicy for production namespaces
deny[msg] {
    input.request.kind.kind == "Pod"
    input.request.namespace == "production"
    not has_network_policy(input.request.namespace)
    msg := "Pods in production namespace require NetworkPolicy"
}

has_network_policy(namespace) {
    data.kubernetes.networkpolicies[namespace][_]
}
```

### 4. RBAC Policy

```rego
package kubernetes.rbac

# Deny overly permissive RBAC
deny[msg] {
    input.request.kind.kind == "ClusterRoleBinding"
    input.request.object.roleRef.name == "cluster-admin"
    subject := input.request.object.subjects[_]
    subject.kind == "User"
    not authorized_admin(subject.name)
    msg := sprintf("User '%v' is not authorized for cluster-admin", [subject.name])
}

authorized_admins := {
    "admin@company.com",
    "sre-team@company.com"
}

authorized_admin(user) {
    authorized_admins[user]
}
```

## Production Security Patterns

### 1. Policy Bundle Management

```bash
# Bundle structure
policies/
├── bundle.manifest
├── data.json
└── policies/
    ├── admission/
    │   ├── images.rego
    │   ├── resources.rego
    │   └── security.rego
    └── rbac/
        └── authorization.rego

# Create bundle
opa build -b policies/ -o bundle.tar.gz

# Sign bundle
opa sign --signing-key key.pem --bundle bundle.tar.gz
```

### 2. Policy Testing

```rego
# policy_test.rego
package kubernetes.admission

test_deny_root_user {
    deny[_] with input as {
        "request": {
            "kind": {"kind": "Pod"},
            "object": {
                "spec": {
                    "containers": [{
                        "name": "test",
                        "securityContext": {"runAsUser": 0}
                    }]
                }
            }
        }
    }
}

test_allow_non_root_user {
    count(deny) == 0 with input as {
        "request": {
            "kind": {"kind": "Pod"},
            "object": {
                "spec": {
                    "containers": [{
                        "name": "test",
                        "securityContext": {"runAsUser": 1000}
                    }]
                }
            }
        }
    }
}
```

### 3. Decision Logging

```yaml
# OPA configuration with decision logging
apiVersion: v1
kind: ConfigMap
metadata:
  name: opa-config
data:
  config.yaml: |
    services:
      authz:
        url: https://bundle-server.com
    
    bundles:
      authz:
        resource: "/bundles/authz"
        
    decision_logs:
      console: true
      reporting:
        upload_size_limit_bytes: 32768
        min_delay_seconds: 5
        max_delay_seconds: 10
```

### 4. High Availability Configuration

```yaml
apiVersion: v1
kind: Service
metadata:
  name: opa
spec:
  selector:
    app: opa
  ports:
  - name: http
    port: 8181
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opa
spec:
  replicas: 3
  selector:
    matchLabels:
      app: opa
  template:
    metadata:
      labels:
        app: opa
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - opa
            topologyKey: kubernetes.io/hostname
      containers:
      - name: opa
        image: openpolicyagent/opa:latest
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8181
          initialDelaySeconds: 5
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /health?bundle=true
            port: 8181
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Monitoring and Observability

### Prometheus Metrics

```yaml
# ServiceMonitor for OPA
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: opa
spec:
  selector:
    matchLabels:
      app: opa
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### Key Metrics to Monitor
- `http_request_duration_seconds`: Policy evaluation latency
- `bundle_loaded_timestamp`: Last successful bundle load
- `decision_logs_dropped`: Dropped decision logs
- `go_memstats_heap_alloc_bytes`: Memory usage

## Best Practices

### 1. Policy Development
- Start with permissive policies and gradually tighten
- Use policy testing extensively
- Implement gradual rollout with dry-run mode
- Version policies with semantic versioning

### 2. Performance Optimization
- Pre-compile policies when possible
- Use indexed data for large datasets
- Implement caching for frequently accessed data
- Monitor policy evaluation latency

### 3. Security Hardening
- Sign and verify policy bundles
- Use TLS for all OPA communications
- Implement authentication for OPA API
- Regular security audits of policies

### 4. Operational Excellence
- Centralized policy management
- Automated policy deployment
- Comprehensive logging and monitoring
- Disaster recovery procedures

## Integration Patterns

### CI/CD Pipeline Integration

```yaml
# GitLab CI example
stages:
  - test
  - build
  - deploy

test-policies:
  stage: test
  image: openpolicyagent/opa:latest
  script:
    - opa test policies/ -v
    - opa fmt --diff policies/

build-bundle:
  stage: build
  script:
    - opa build -b policies/ -o bundle.tar.gz
    - opa sign --signing-key $SIGNING_KEY bundle.tar.gz
  artifacts:
    paths:
      - bundle.tar.gz

deploy-policies:
  stage: deploy
  script:
    - curl -X POST https://bundle-server.com/upload -F "bundle=@bundle.tar.gz"
```

### Service Mesh Integration

```yaml
# Envoy External Authorization
static_resources:
  listeners:
  - address:
      socket_address:
        address: 0.0.0.0
        port_value: 8080
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          http_filters:
          - name: envoy.ext_authz
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
              grpc_service:
                envoy_grpc:
                  cluster_name: opa
                timeout: 0.5s
```

---

### 📡 Stay Updated

**Release Notes**: [OPA Releases](https://github.com/open-policy-agent/opa/releases) • [Gatekeeper](https://github.com/open-policy-agent/gatekeeper/releases) • [Conftest](https://github.com/open-policy-agent/conftest/releases)

**Project News**: [OPA Blog](https://blog.openpolicyagent.org/) • [Styra Blog](https://www.styra.com/blog/) • [CNCF Updates](https://www.cncf.io/blog/)

**Community**: [OPA Slack](https://slack.openpolicyagent.org/) • [Community Meetings](https://www.openpolicyagent.org/community/) • [GitHub Discussions](https://github.com/open-policy-agent/opa/discussions)