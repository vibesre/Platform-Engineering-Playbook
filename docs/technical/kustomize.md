# Kustomize - Kubernetes Configuration Customization

## Overview

Kustomize is a Kubernetes-native configuration management tool that allows you to customize raw, template-free YAML files for multiple purposes, leaving the original YAML untouched and usable as is. It's built into kubectl and provides a declarative approach to configuration customization.

## Core Concepts

### Bases and Overlays
- **Base**: A directory containing a `kustomization.yaml` file and a set of Kubernetes resources
- **Overlay**: A directory that refers to a base and contains customizations
- **Patches**: Modifications applied to resources to customize them for different environments

### Kustomization File
The `kustomization.yaml` file declares the resources and transformations to apply:
- Resources to include
- Patches to apply
- ConfigMaps and Secrets to generate
- Common labels and annotations
- Namespace transformations

## Installation and Setup

```bash
# Kustomize is built into kubectl (v1.14+)
kubectl kustomize --help

# Install standalone kustomize
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash

# macOS installation
brew install kustomize

# Verify installation
kustomize version
```

## Basic Structure

### Directory Layout

```
app/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    ├── development/
    │   ├── kustomization.yaml
    │   ├── deployment-patch.yaml
    │   └── config.properties
    ├── staging/
    │   ├── kustomization.yaml
    │   ├── deployment-patch.yaml
    │   └── config.properties
    └── production/
        ├── kustomization.yaml
        ├── deployment-patch.yaml
        ├── replica-patch.yaml
        └── config.properties
```

## Creating a Base Configuration

### base/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

commonLabels:
  app: myapp
  version: v1

commonAnnotations:
  managed-by: kustomize
```

### base/deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 8080
        env:
        - name: ENVIRONMENT
          value: "base"
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### base/service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
```

## Environment-Specific Overlays

### overlays/development/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

bases:
  - ../../base

namePrefix: dev-
namespace: development

commonLabels:
  environment: development

patchesStrategicMerge:
  - deployment-patch.yaml

configMapGenerator:
  - name: app-config
    files:
      - config.properties
    options:
      disableNameSuffixHash: false

replicas:
  - name: myapp
    count: 1
```

### overlays/development/deployment-patch.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:dev
        env:
        - name: ENVIRONMENT
          value: "development"
        - name: DEBUG
          value: "true"
        - name: LOG_LEVEL
          value: "debug"
```

### overlays/production/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

bases:
  - ../../base

namespace: production

commonLabels:
  environment: production

patchesStrategicMerge:
  - deployment-patch.yaml
  - replica-patch.yaml

configMapGenerator:
  - name: app-config
    files:
      - config.properties
    options:
      disableNameSuffixHash: true

secretGenerator:
  - name: app-secrets
    envs:
      - secrets.env

images:
  - name: myapp
    newName: myregistry.io/myapp
    newTag: v1.2.3

replicas:
  - name: myapp
    count: 3
```

## Advanced Features

### JSON Patches (RFC 6902)

```yaml
# overlays/production/kustomization.yaml
patchesJson6902:
  - target:
      version: v1
      kind: Deployment
      name: myapp
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
      - op: add
        path: /spec/template/spec/containers/0/env/-
        value:
          name: FEATURE_FLAG
          value: "enabled"
```

### Strategic Merge Patches

```yaml
# resource-limits-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        resources:
          requests:
            memory: "256Mi"
            cpu: "500m"
          limits:
            memory: "512Mi"
            cpu: "1000m"
```

### Inline Patches

```yaml
# kustomization.yaml
patches:
  - target:
      kind: Service
      name: myapp-service
    patch: |-
      apiVersion: v1
      kind: Service
      metadata:
        name: myapp-service
      spec:
        type: LoadBalancer
```

### ConfigMap and Secret Generation

```yaml
# kustomization.yaml
configMapGenerator:
  - name: app-config
    literals:
      - DATABASE_HOST=localhost
      - DATABASE_PORT=5432
    files:
      - application.properties
      - logging.conf

secretGenerator:
  - name: db-credentials
    literals:
      - username=dbuser
      - password=secretpassword
    type: Opaque
  - name: tls-secret
    files:
      - tls.crt=cert.pem
      - tls.key=key.pem
    type: kubernetes.io/tls
```

### Variables and Replacements

```yaml
# kustomization.yaml
vars:
  - name: SERVICE_NAME
    objref:
      kind: Service
      name: myapp-service
      apiVersion: v1

replacements:
  - source:
      kind: ConfigMap
      name: app-config
      fieldPath: data.database_url
    targets:
      - select:
          kind: Deployment
        fieldPaths:
          - spec.template.spec.containers.[name=myapp].env.[name=DATABASE_URL].value
```

## Components (Reusable Configurations)

### components/monitoring/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1alpha1
kind: Component

patches:
  - target:
      kind: Deployment
    patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: not-used
      spec:
        template:
          metadata:
            annotations:
              prometheus.io/scrape: "true"
              prometheus.io/port: "8080"
              prometheus.io/path: "/metrics"
```

### Using Components

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

components:
  - ../../components/monitoring
```

## Practical Examples

### 1. Multi-Environment Configuration

```bash
# Project structure for microservices
microservices/
├── services/
│   ├── api-gateway/
│   │   ├── base/
│   │   └── overlays/
│   ├── auth-service/
│   │   ├── base/
│   │   └── overlays/
│   └── user-service/
│       ├── base/
│       └── overlays/
└── environments/
    ├── dev/
    │   └── kustomization.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

```yaml
# environments/dev/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../services/api-gateway/overlays/dev
  - ../../services/auth-service/overlays/dev
  - ../../services/user-service/overlays/dev

commonLabels:
  environment: dev
  team: platform

namespace: development
```

### 2. Resource Limits and Quotas

```yaml
# components/resource-quotas/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1alpha1
kind: Component

resources:
  - resource-quota.yaml
  - limit-range.yaml

# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    limits.cpu: "200"
    limits.memory: 400Gi
    persistentvolumeclaims: "10"

# limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
spec:
  limits:
  - default:
      cpu: 500m
      memory: 512Mi
    defaultRequest:
      cpu: 100m
      memory: 128Mi
    type: Container
```

### 3. Network Policies

```yaml
# overlays/production/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: myapp-network-policy
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: production
    - podSelector:
        matchLabels:
          app: nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: production
    ports:
    - protocol: TCP
      port: 5432
```

## Best Practices

### 1. Directory Structure

```bash
# Organized structure for large projects
project/
├── base/
│   ├── apps/
│   │   ├── frontend/
│   │   ├── backend/
│   │   └── database/
│   ├── monitoring/
│   ├── networking/
│   └── security/
├── components/
│   ├── istio/
│   ├── logging/
│   └── metrics/
└── overlays/
    ├── dev/
    ├── staging/
    └── production/
```

### 2. Using Kustomize with GitOps

```yaml
# ArgoCD Application using Kustomize
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/company/k8s-configs
    targetRevision: HEAD
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 3. CI/CD Integration

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - deploy

validate:
  stage: validate
  script:
    - kustomize build overlays/dev > /tmp/dev.yaml
    - kubectl apply --dry-run=client -f /tmp/dev.yaml
    - kustomize build overlays/staging > /tmp/staging.yaml
    - kubectl apply --dry-run=client -f /tmp/staging.yaml
    - kustomize build overlays/production > /tmp/production.yaml
    - kubectl apply --dry-run=client -f /tmp/production.yaml

deploy-dev:
  stage: deploy
  script:
    - kustomize build overlays/dev | kubectl apply -f -
  only:
    - develop

deploy-prod:
  stage: deploy
  script:
    - kustomize build overlays/production | kubectl apply -f -
  only:
    - main
```

### 4. Image Management

```yaml
# kustomization.yaml with image transformations
images:
  - name: myapp
    newName: myregistry.io/myapp
    newTag: v1.2.3
  - name: redis
    newName: redis
    newTag: 6.2-alpine
  - name: postgres
    newName: postgres
    newTag: 13.4

# Using environment variables
images:
  - name: myapp
    newName: ${IMAGE_REGISTRY}/myapp
    newTag: ${IMAGE_TAG}
```

## Production Use Cases

### 1. Blue-Green Deployments

```yaml
# overlays/blue/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

nameSuffix: -blue

commonLabels:
  version: blue

# overlays/green/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

nameSuffix: -green

commonLabels:
  version: green
```

### 2. Multi-Region Deployment

```yaml
# overlays/us-east/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

commonLabels:
  region: us-east

patchesStrategicMerge:
  - |-
    apiVersion: v1
    kind: Service
    metadata:
      name: myapp-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-additional-resource-tags: "Region=us-east-1"
```

### 3. Tenant Isolation

```yaml
# tenants/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - namespace.yaml
  - resource-quota.yaml
  - network-policy.yaml

# tenants/tenant-a/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../base

namespace: tenant-a

commonLabels:
  tenant: tenant-a

patchesStrategicMerge:
  - |-
    apiVersion: v1
    kind: ResourceQuota
    metadata:
      name: compute-quota
    spec:
      hard:
        requests.cpu: "50"
        requests.memory: 100Gi
```

## Troubleshooting

### Common Commands

```bash
# Build and view output
kustomize build overlays/production

# Validate output
kustomize build overlays/production | kubectl apply --dry-run=client -f -

# Show differences
kustomize build overlays/production | kubectl diff -f -

# Debug with verbose output
kustomize build overlays/production --enable-helm --load-restrictor LoadRestrictionsNone

# List all resources
kustomize build overlays/production | kubectl get -f - --show-kind
```

### Common Issues

1. **Resource not found**
```bash
# Check paths in kustomization.yaml
# Ensure relative paths are correct
# Use --load-restrictor LoadRestrictionsNone for files outside root
```

2. **Patch conflicts**
```bash
# Use strategic merge patches for arrays
# Check patch target selectors
# Verify resource names match
```

3. **Hash suffix issues**
```yaml
# Disable hash suffix for ConfigMaps/Secrets
configMapGenerator:
  - name: app-config
    files:
      - config.properties
    options:
      disableNameSuffixHash: true
```

## Integration with Other Tools

### Helm and Kustomize

```yaml
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

helmCharts:
  - name: postgresql
    repo: https://charts.bitnami.com/bitnami
    version: 11.9.1
    releaseName: my-postgres
    valuesInline:
      auth:
        database: myapp
        username: myuser
```

### Kustomize with Kubectl

```bash
# Apply directly with kubectl (1.14+)
kubectl apply -k overlays/production/

# Delete resources
kubectl delete -k overlays/production/

# View differences
kubectl diff -k overlays/production/
```

## Conclusion

Kustomize provides a powerful, template-free way to customize Kubernetes configurations for different environments and use cases. Its declarative approach, built-in support in kubectl, and ability to work with plain YAML files make it an excellent choice for managing Kubernetes deployments across multiple environments while maintaining simplicity and reusability.