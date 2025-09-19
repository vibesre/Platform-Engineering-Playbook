# Open Policy Agent (OPA) for Policy as Code

## Overview

Open Policy Agent (OPA) is a general-purpose policy engine that enables unified, context-aware policy enforcement across the entire stack. OPA decouples policy decision-making from policy enforcement, allowing you to define policies as code using a high-level declarative language called Rego.

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

## Conclusion

OPA provides a powerful, flexible framework for implementing policy as code across your infrastructure. By following these patterns and best practices, you can build a robust, scalable policy enforcement system that enhances your security posture while maintaining operational agility.