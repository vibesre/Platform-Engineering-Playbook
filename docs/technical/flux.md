# Flux - GitOps Toolkit for Kubernetes

## Overview

Flux is a set of continuous and progressive delivery solutions for Kubernetes that are open and extensible. It's the GitOps toolkit that enables you to manage Kubernetes clusters and deliver applications using Git repositories as the source of truth.

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         Flux v2 Components                       │
├─────────────────────────┬───────────────────────────────────────┤
│    Source Controller    │         Kustomize Controller         │
│  • Git repositories     │  • Kustomization reconciliation     │
│  • Helm repositories    │  • Post-build substitutions        │
│  • OCI repositories     │  • Health assessments              │
│  • S3 buckets          │  • Dependency management           │
├─────────────────────────┼───────────────────────────────────────┤
│    Helm Controller      │      Notification Controller        │
│  • Helm releases       │  • Event dispatching               │
│  • Chart dependencies  │  • Alert forwarding                │
│  • Value overrides     │  • Webhook receivers               │
├─────────────────────────┼───────────────────────────────────────┤
│   Image Automation      │        Image Reflector              │
│     Controller         │         Controller                  │
│  • Image updates       │  • Image scanning                  │
│  • Git commits         │  • Tag discovery                   │
│  • Pull requests       │  • Policy matching                 │
└─────────────────────────┴───────────────────────────────────────┘
                                    │
                                    ▼
                        ┌─────────────────────────┐
                        │   Target Kubernetes     │
                        │      Resources         │
                        └─────────────────────────┘
```

### Key Concepts

1. **GitRepository**: Defines a Git repository source
2. **OCIRepository**: Defines an OCI artifact source
3. **HelmRepository**: Defines a Helm chart repository
4. **Kustomization**: Defines what to deploy from sources
5. **HelmRelease**: Defines a Helm chart release
6. **ImageRepository**: Tracks container image tags
7. **ImagePolicy**: Defines image update rules
8. **Alert**: Defines notification rules
9. **Provider**: Defines notification endpoints

## Installation

### Prerequisites

```bash
# Kubernetes cluster 1.20+
kubectl version --client

# GitHub personal access token (for bootstrap)
export GITHUB_TOKEN=<your-token>
export GITHUB_USER=<your-username>
```

### Install Flux CLI

```bash
# macOS
brew install fluxcd/tap/flux

# Linux
curl -s https://fluxcd.io/install.sh | sudo bash

# Verify installation
flux --version
```

### Bootstrap Flux

```bash
# Check prerequisites
flux check --pre

# Bootstrap with GitHub
flux bootstrap github \
  --owner=$GITHUB_USER \
  --repository=fleet-infra \
  --branch=main \
  --path=./clusters/production \
  --personal

# Bootstrap with GitLab
flux bootstrap gitlab \
  --owner=$GITLAB_USER \
  --repository=fleet-infra \
  --branch=main \
  --path=./clusters/production \
  --personal
```

## Configuration Examples

### Git Repository Source

```yaml
# sources/app-repo.yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: app-config
  namespace: flux-system
spec:
  interval: 1m
  ref:
    branch: main
  url: https://github.com/myorg/app-config
  secretRef:
    name: github-credentials
---
apiVersion: v1
kind: Secret
metadata:
  name: github-credentials
  namespace: flux-system
type: Opaque
stringData:
  username: git
  password: ${GITHUB_TOKEN}
```

### Kustomization Deployment

```yaml
# apps/base/kustomization.yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: apps
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: app-config
  path: "./deploy/overlays/production"
  prune: true
  validation: client
  timeout: 5m
  postBuild:
    substitute:
      cluster_name: "production"
      region: "us-east-1"
    substituteFrom:
    - kind: ConfigMap
      name: cluster-vars
    - kind: Secret
      name: cluster-secrets
  healthChecks:
  - apiVersion: apps/v1
    kind: Deployment
    name: webapp
    namespace: default
```

### Helm Release

```yaml
# infrastructure/ingress-nginx/release.yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: HelmRepository
metadata:
  name: ingress-nginx
  namespace: flux-system
spec:
  interval: 1h
  url: https://kubernetes.github.io/ingress-nginx
---
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: ingress-nginx
  namespace: flux-system
spec:
  interval: 1h
  releaseName: ingress-nginx
  targetNamespace: ingress-nginx
  chart:
    spec:
      chart: ingress-nginx
      version: "4.0.6"
      sourceRef:
        kind: HelmRepository
        name: ingress-nginx
  values:
    controller:
      replicaCount: 3
      service:
        type: LoadBalancer
        annotations:
          service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 1000m
          memory: 512Mi
  install:
    createNamespace: true
    remediation:
      retries: 3
  upgrade:
    remediation:
      retries: 3
      remediateLastFailure: true
    cleanupOnFail: true
  rollback:
    timeout: 10m
    recreate: true
    cleanupOnFail: true
```

### Multi-Tenancy Configuration

```yaml
# tenants/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- team-a.yaml
- team-b.yaml
- team-c.yaml

# tenants/base/team-a.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
  labels:
    toolkit.fluxcd.io/tenant: team-a
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: team-a
  namespace: team-a
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: team-a-admin
  namespace: team-a
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: admin
subjects:
- kind: ServiceAccount
  name: team-a
  namespace: team-a
---
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: team-a
  namespace: team-a
spec:
  interval: 1m
  ref:
    branch: main
  url: https://github.com/myorg/team-a-config
  secretRef:
    name: git-credentials
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: team-a-apps
  namespace: team-a
spec:
  interval: 5m
  sourceRef:
    kind: GitRepository
    name: team-a
  path: "./apps"
  prune: true
  serviceAccountName: team-a
  validation: client
```

## Production Patterns

### Repository Structure

```
fleet-infra/
├── clusters/
│   ├── production/
│   │   ├── flux-system/           # Flux components
│   │   │   ├── gotk-components.yaml
│   │   │   └── gotk-sync.yaml
│   │   ├── infrastructure/        # Infrastructure controllers
│   │   │   ├── kustomization.yaml
│   │   │   ├── sources/
│   │   │   └── controllers/
│   │   └── apps/                  # Application workloads
│   │       ├── kustomization.yaml
│   │       ├── base/
│   │       └── production/
│   └── staging/
│       └── ...
├── infrastructure/
│   ├── controllers/
│   │   ├── cert-manager/
│   │   ├── ingress-nginx/
│   │   └── kyverno/
│   └── configs/
│       ├── cluster-issuers/
│       └── network-policies/
└── tenants/
    ├── base/
    ├── production/
    └── staging/
```

### Image Automation

```yaml
# image-automation/webapp.yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: webapp
  namespace: flux-system
spec:
  image: myorg/webapp
  interval: 1m
  provider: generic
  secretRef:
    name: docker-registry-credentials
---
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: webapp
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: webapp
  policy:
    semver:
      range: ">=1.0.0 <2.0.0"
---
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageUpdateAutomation
metadata:
  name: webapp
  namespace: flux-system
spec:
  interval: 1m
  sourceRef:
    kind: GitRepository
    name: app-config
  git:
    checkout:
      ref:
        branch: main
    commit:
      author:
        email: fluxcdbot@users.noreply.github.com
        name: fluxcdbot
      messageTemplate: |
        Automated image update
        
        [ci skip]
    push:
      branch: main
  update:
    path: "./apps/webapp"
    strategy: Setters
```

### Progressive Delivery with Flagger

```yaml
# flagger/webapp-canary.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: webapp
  namespace: production
spec:
  provider: nginx
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webapp
  ingressRef:
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    name: webapp
  service:
    port: 80
    targetPort: http
    gateways:
    - public-gateway
    hosts:
    - app.example.com
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 30s
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 30s
    webhooks:
    - name: acceptance-test
      type: pre-rollout
      url: http://flagger-loadtester.test/
      timeout: 30s
      metadata:
        type: bash
        cmd: "curl -sd 'test' http://webapp-canary.production/health | grep ok"
    - name: load-test
      type: rollout
      url: http://flagger-loadtester.test/
      metadata:
        cmd: "hey -z 2m -q 10 -c 2 http://webapp-canary.production/"
```

### Monitoring and Alerting

```yaml
# monitoring/alerts.yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta2
kind: Provider
metadata:
  name: slack
  namespace: flux-system
spec:
  type: slack
  channel: flux-alerts
  secretRef:
    name: slack-webhook
---
apiVersion: notification.toolkit.fluxcd.io/v1beta2
kind: Alert
metadata:
  name: on-call
  namespace: flux-system
spec:
  providerRef:
    name: slack
  eventSeverity: info
  eventSources:
  - kind: GitRepository
    name: '*'
  - kind: Kustomization
    name: '*'
  - kind: HelmRelease
    name: '*'
  exclusionList:
  - "waiting.*socket"
  summary: |
    Cluster: production
    Message: {{ .Message }}
    Metadata: {{ range .Metadata }}{{ .Key }}={{ .Value }} {{ end }}
---
apiVersion: notification.toolkit.fluxcd.io/v1beta2
kind: Alert
metadata:
  name: infra-alerts
  namespace: flux-system
spec:
  providerRef:
    name: slack
  eventSeverity: error
  eventSources:
  - kind: Kustomization
    name: infrastructure
  - kind: Kustomization
    name: flux-system
```

### Secrets Management

```yaml
# secrets/sealed-secrets.yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: HelmRepository
metadata:
  name: sealed-secrets
  namespace: flux-system
spec:
  interval: 1h
  url: https://bitnami-labs.github.io/sealed-secrets
---
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: sealed-secrets-controller
  namespace: flux-system
spec:
  interval: 1h
  chart:
    spec:
      chart: sealed-secrets
      version: "2.7.1"
      sourceRef:
        kind: HelmRepository
        name: sealed-secrets
  install:
    createNamespace: true
  values:
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
      limits:
        cpu: 200m
        memory: 256Mi
```

### Network Policies

```yaml
# policies/flux-system-netpol.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: flux-controllers
  namespace: flux-system
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/part-of: flux
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          app.kubernetes.io/part-of: flux
  egress:
  - to:
    - namespaceSelector: {}
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - port: 53
      protocol: UDP
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 169.254.169.254/32
```

## Security Best Practices

### RBAC Configuration

```yaml
# rbac/flux-view.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: flux-view
rules:
- apiGroups: ["source.toolkit.fluxcd.io"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["kustomize.toolkit.fluxcd.io"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["helm.toolkit.fluxcd.io"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["notification.toolkit.fluxcd.io"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["image.toolkit.fluxcd.io"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: flux-view-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: flux-view
subjects:
- kind: Group
  name: flux-viewers
  apiGroup: rbac.authorization.k8s.io
```

### Policy Enforcement

```yaml
# policies/kyverno-flux.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: flux-multi-tenancy
spec:
  validationFailureAction: enforce
  background: false
  rules:
  - name: serviceAccountName
    match:
      any:
      - resources:
          kinds:
          - Kustomization
          - HelmRelease
          namespaces:
          - "team-*"
    validate:
      message: ".spec.serviceAccountName is required"
      pattern:
        spec:
          serviceAccountName: "?*"
  - name: sourceNamespace  
    match:
      any:
      - resources:
          kinds:
          - Kustomization
          - HelmRelease
          namespaces:
          - "team-*"
    validate:
      message: "must use GitRepository from the same namespace"
      pattern:
        spec:
          sourceRef:
            namespace: "{{request.object.metadata.namespace}}"
```

## Troubleshooting

### Common Commands

```bash
# Check Flux components
flux check

# Get all Flux resources
flux get all -A

# Get sources
flux get sources git -A
flux get sources helm -A
flux get sources oci -A

# Get deployments
flux get kustomizations -A
flux get helmreleases -A

# Reconcile resources
flux reconcile source git flux-system
flux reconcile kustomization apps

# Suspend/Resume
flux suspend kustomization apps
flux resume kustomization apps

# Check logs
kubectl -n flux-system logs deployment/source-controller
kubectl -n flux-system logs deployment/kustomize-controller
kubectl -n flux-system logs deployment/helm-controller

# Export resources
flux export source git --all > sources.yaml
flux export kustomization --all > kustomizations.yaml

# Diff local vs cluster
flux diff kustomization apps --path ./apps

# Tree view
flux tree kustomization flux-system
```

### Debug Mode

```yaml
# Enable debug logging
apiVersion: apps/v1
kind: Deployment
metadata:
  name: source-controller
  namespace: flux-system
spec:
  template:
    spec:
      containers:
      - name: manager
        args:
        - --log-level=debug
        - --log-encoding=json
```

## Migration from Flux v1

### Migration Steps

```bash
# Install Flux v2
flux install

# Migrate Helm Releases
flux create source helm bitnami \
  --url=https://charts.bitnami.com/bitnami \
  --interval=1h

flux create helmrelease redis \
  --source=HelmRepository/bitnami \
  --chart=redis \
  --chart-version=">14.0.0" \
  --interval=1h

# Migrate Git repositories
flux create source git webapp \
  --url=https://github.com/myorg/webapp \
  --branch=main \
  --interval=1m

flux create kustomization webapp \
  --source=webapp \
  --path="./deploy" \
  --prune=true \
  --interval=10m
```

## Integration Examples

### GitHub Actions

```yaml
# .github/workflows/flux-diff.yaml
name: Flux Diff
on:
  pull_request:
    branches: [main]
    paths: ["clusters/**.yaml"]

jobs:
  diff:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: fluxcd/flux2/action@main
    - run: |
        flux diff kustomization apps \
          --path ./clusters/production \
          --github-token ${{ secrets.GITHUB_TOKEN }}
```

### Prometheus Monitoring

```yaml
# monitoring/podmonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: flux-system
  namespace: flux-system
spec:
  selector:
    matchLabels:
      app.kubernetes.io/part-of: flux
  podMetricsEndpoints:
  - port: http-prom
    interval: 30s
    scrapeTimeout: 10s
```