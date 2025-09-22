# ArgoCD - Declarative GitOps for Kubernetes

ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes. It follows the GitOps pattern of using Git repositories as the source of truth for defining the desired application state.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **ArgoCD Tutorial for Beginners - GitOps CD for Kubernetes**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 1 hour](https://www.youtube.com/watch?v=MeU5_k9ssrs)
- **Why it's great**: Comprehensive introduction to ArgoCD and GitOps principles

#### **Complete GitOps Course - ArgoCD**
- **Channel**: DevOps Journey
- **Link**: [YouTube - 2 hours](https://www.youtube.com/watch?v=2WSJF7d8dws)
- **Why it's great**: Hands-on tutorial covering installation to production setup

#### **ArgoCD Deep Dive**
- **Channel**: CNCF
- **Link**: [YouTube - 45 minutes](https://www.youtube.com/watch?v=aWDIQMbp1cc)
- **Why it's great**: Technical deep dive by ArgoCD maintainers

### 📖 Essential Documentation

#### **ArgoCD Official Documentation**
- **Link**: [argo-cd.readthedocs.io](https://argo-cd.readthedocs.io/)
- **Why it's great**: Comprehensive official documentation with getting started guides

#### **GitOps Guide**
- **Link**: [argoproj.github.io/argo-cd/](https://argoproj.github.io/argo-cd/)
- **Why it's great**: Complete guide to GitOps principles and practices

#### **ArgoCD Best Practices**
- **Link**: [argo-cd.readthedocs.io/en/stable/user-guide/best_practices/](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- **Why it's great**: Production-ready configuration patterns and security practices

### 📝 Must-Read Blogs & Articles

#### **Argo Project Blog**
- **Source**: Argo Project
- **Link**: [argoproj.io/blog/](https://argoproj.io/blog/)
- **Why it's great**: Official updates and technical insights from maintainers

#### **GitOps with ArgoCD Guide**
- **Source**: Codefresh
- **Link**: [codefresh.io/learn/argo-cd/](https://codefresh.io/learn/argo-cd/)
- **Why it's great**: Practical guide to implementing GitOps workflows

#### **ArgoCD vs Flux Comparison**
- **Source**: Weave Works
- **Link**: [weave.works/blog/gitops-with-flux-v2](https://www.weave.works/blog/gitops-with-flux-v2)
- **Why it's great**: Comparison of GitOps tools and their strengths

### 🎓 Structured Courses

#### **GitOps Fundamentals**
- **Platform**: Linux Foundation (LFS169)
- **Link**: [training.linuxfoundation.org/training/gitops-fundamentals/](https://training.linuxfoundation.org/training/gitops-fundamentals/)
- **Cost**: Free
- **Why it's great**: Official CNCF course covering GitOps principles and tools

#### **Kubernetes GitOps with ArgoCD**
- **Platform**: A Cloud Guru
- **Link**: [acloudguru.com/course/kubernetes-gitops-with-argocd](https://acloudguru.com/course/kubernetes-gitops-with-argocd)
- **Cost**: Paid
- **Why it's great**: Hands-on labs with real-world scenarios

### 🛠️ Tools & Platforms

#### **ArgoCD Demo Environment**
- **Link**: [killercoda.com/argoproj](https://killercoda.com/argoproj)
- **Why it's great**: Interactive demos and tutorials in browser

#### **ArgoCD CLI**
- **Link**: [argo-cd.readthedocs.io/en/stable/cli_installation/](https://argo-cd.readthedocs.io/en/stable/cli_installation/)
- **Why it's great**: Command-line interface for ArgoCD management

#### **ArgoCD Autopilot**
- **Link**: [argocd-autopilot.readthedocs.io](https://argocd-autopilot.readthedocs.io/)
- **Why it's great**: Tool for bootstrapping ArgoCD with GitOps repository structure

## Overview

ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes. It follows the GitOps pattern of using Git repositories as the source of truth for defining the desired application state.

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                           ArgoCD Server                          │
├─────────────────────────┬───────────────────────────────────────┤
│      API Server         │            Repo Server               │
│  • REST/gRPC API       │  • Git repository access            │
│  • Web UI backend      │  • Manifest generation              │
│  • RBAC               │  • Caching layer                   │
├─────────────────────────┼───────────────────────────────────────┤
│   Application Controller │         Redis                       │
│  • K8s resource watch   │  • Cache storage                   │
│  • Sync operations      │  • Session management              │
│  • Health assessment    │  • Operation locks                 │
└─────────────────────────┴───────────────────────────────────────┘
                                    │
                                    ▼
                        ┌─────────────────────────┐
                        │   Target Kubernetes     │
                        │      Clusters          │
                        └─────────────────────────┘
```

### Key Concepts

1. **Application**: A group of Kubernetes resources defined by a manifest
2. **Application Source**: Location of the desired state (Git repository)
3. **Target State**: The desired state of an application
4. **Live State**: The current state in the Kubernetes cluster
5. **Sync Status**: Whether the live state matches the target state
6. **Health Status**: Whether the application is running correctly

## Installation

### Prerequisites

```bash
# Kubernetes cluster 1.19+
kubectl version --client

# kubectl configured to target cluster
kubectl cluster-info
```

### Install ArgoCD

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods to be ready
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s

# Install ArgoCD CLI
brew install argocd  # macOS
# or download from https://github.com/argoproj/argo-cd/releases
```

### Initial Setup

```bash
# Port forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d

# Login via CLI
argocd login localhost:8080 \
  --username admin \
  --password <initial-password> \
  --insecure

# Change admin password
argocd account update-password

# Delete initial secret
kubectl -n argocd delete secret argocd-initial-admin-secret
```

## Configuration Examples

### Application Definition

```yaml
# app-of-apps.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/gitops-config
    targetRevision: main
    path: applications
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### AppProject Configuration

```yaml
# project.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: production
  namespace: argocd
spec:
  description: Production applications
  
  # Source repositories
  sourceRepos:
  - 'https://github.com/myorg/*'
  
  # Destination clusters and namespaces
  destinations:
  - namespace: 'prod-*'
    server: https://kubernetes.default.svc
  - namespace: 'monitoring'
    server: https://kubernetes.default.svc
    
  # Cluster resource whitelist
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace
  - group: rbac.authorization.k8s.io
    kind: ClusterRole
  - group: rbac.authorization.k8s.io
    kind: ClusterRoleBinding
    
  # Namespace resource whitelist
  namespaceResourceWhitelist:
  - group: '*'
    kind: '*'
    
  # Roles
  roles:
  - name: admin
    policies:
    - p, proj:production:admin, applications, *, production/*, allow
    groups:
    - myorg:platform-team
    
  - name: developer
    policies:
    - p, proj:production:developer, applications, get, production/*, allow
    - p, proj:production:developer, applications, sync, production/*, allow
    groups:
    - myorg:dev-team
```

### Repository Credentials

```yaml
# repo-creds.yaml
apiVersion: v1
kind: Secret
metadata:
  name: github-creds
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
type: Opaque
stringData:
  type: git
  url: https://github.com/myorg
  username: git
  password: <github-token>
```

### Helm Values Override

```yaml
# helm-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx-ingress
  namespace: argocd
spec:
  project: infrastructure
  source:
    repoURL: https://kubernetes.github.io/ingress-nginx
    targetRevision: 4.0.6
    chart: ingress-nginx
    helm:
      releaseName: nginx-ingress
      values: |
        controller:
          replicaCount: 3
          service:
            type: LoadBalancer
            annotations:
              service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
          resources:
            limits:
              cpu: 1000m
              memory: 1Gi
            requests:
              cpu: 500m
              memory: 512Mi
          autoscaling:
            enabled: true
            minReplicas: 3
            maxReplicas: 10
            targetCPUUtilizationPercentage: 75
  destination:
    server: https://kubernetes.default.svc
    namespace: ingress-nginx
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

## Production Patterns

### High Availability Setup

```yaml
# argocd-ha-values.yaml
redis-ha:
  enabled: true
  
controller:
  replicas: 3
  env:
  - name: ARGOCD_CONTROLLER_REPLICAS
    value: "3"
  resources:
    limits:
      cpu: 2
      memory: 4Gi
    requests:
      cpu: 1
      memory: 2Gi
      
server:
  replicas: 3
  resources:
    limits:
      cpu: 1
      memory: 2Gi
    requests:
      cpu: 500m
      memory: 1Gi
  ingress:
    enabled: true
    hosts:
    - argocd.example.com
    tls:
    - secretName: argocd-tls
      hosts:
      - argocd.example.com
      
repoServer:
  replicas: 3
  resources:
    limits:
      cpu: 1
      memory: 2Gi
    requests:
      cpu: 500m
      memory: 1Gi
```

### Multi-Cluster Management

```yaml
# cluster-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: prod-cluster
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: production
  server: https://prod.k8s.example.com
  config: |
    {
      "bearerToken": "<service-account-token>",
      "tlsClientConfig": {
        "insecure": false,
        "caData": "<base64-ca-cert>"
      }
    }
```

### GitOps Repository Structure

```
gitops-config/
├── applications/           # App of apps
│   ├── base/
│   │   ├── namespaces.yaml
│   │   └── argocd-apps.yaml
│   └── overlays/
│       ├── development/
│       ├── staging/
│       └── production/
├── infrastructure/         # Platform components
│   ├── cert-manager/
│   ├── external-dns/
│   ├── ingress-nginx/
│   └── monitoring/
├── services/              # Application services
│   ├── api-gateway/
│   ├── user-service/
│   └── payment-service/
└── clusters/              # Cluster-specific configs
    ├── dev-cluster/
    ├── staging-cluster/
    └── prod-cluster/
```

### Progressive Delivery with Argo Rollouts

```yaml
# rollout.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: api-service
spec:
  replicas: 10
  strategy:
    canary:
      maxSurge: "25%"
      maxUnavailable: 0
      steps:
      - setWeight: 10
      - pause: {duration: 10m}
      - setWeight: 20
      - pause: {duration: 10m}
      - setWeight: 40
      - pause: {duration: 10m}
      - setWeight: 60
      - pause: {duration: 10m}
      - setWeight: 80
      - pause: {duration: 10m}
      canaryService: api-service-canary
      stableService: api-service-stable
      trafficRouting:
        nginx:
          stableIngress: api-service-ingress
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
    spec:
      containers:
      - name: api
        image: myorg/api:v2.0.0
        ports:
        - containerPort: 8080
```

### RBAC Configuration

```yaml
# argocd-rbac-cm.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.default: role:readonly
  policy.csv: |
    # Platform Admin - full access
    p, role:platform-admin, applications, *, */*, allow
    p, role:platform-admin, clusters, *, *, allow
    p, role:platform-admin, repositories, *, *, allow
    p, role:platform-admin, certificates, *, *, allow
    p, role:platform-admin, projects, *, *, allow
    
    # Developer - limited access
    p, role:developer, applications, get, */*, allow
    p, role:developer, applications, sync, */*, allow
    p, role:developer, applications, action/*, */*, allow
    p, role:developer, logs, get, */*, allow
    p, role:developer, exec, create, */*, allow
    
    # Viewer - read only
    p, role:viewer, applications, get, */*, allow
    p, role:viewer, projects, get, *, allow
    
    # Group bindings
    g, myorg:platform-team, role:platform-admin
    g, myorg:dev-team, role:developer
    g, myorg:support-team, role:viewer
```

### Notification Configuration

```yaml
# argocd-notifications-cm.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.slack: |
    token: $slack-token
  template.app-deployed: |
    message: |
      Application {{.app.metadata.name}} is now running new version.
      {{if eq .serviceType "slack"}}:white_check_mark:{{end}} Application {{.app.metadata.name}} is now running new version.
    slack:
      attachments: |
        [{
          "title": "{{ .app.metadata.name}}",
          "title_link":"{{.context.argocdUrl}}/applications/{{.app.metadata.name}}",
          "color": "#18be52",
          "fields": [
          {
            "title": "Sync Status",
            "value": "{{.app.status.sync.status}}",
            "short": true
          },
          {
            "title": "Repository",
            "value": "{{.app.spec.source.repoURL}}",
            "short": true
          }
          {{range $index, $c := .app.status.conditions}}
          {{if not $index}},{{end}}
          {{if $index}},{{end}}
          {
            "title": "{{$c.type}}",
            "value": "{{$c.message}}",
            "short": true
          }
          {{end}}
          ]
        }]
  trigger.on-deployed: |
    - when: app.status.operationState.phase in ['Succeeded'] and app.status.health.status == 'Healthy'
      send: [app-deployed]
  subscriptions: |
    - recipients:
      - slack:deployments
      triggers:
      - on-deployed
```

### Resource Customization

```yaml
# argocd-cm.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  resource.customizations.health.certmanager.k8s.io_Certificate: |
    hs = {}
    if obj.status ~= nil then
      if obj.status.conditions ~= nil then
        for i, condition in ipairs(obj.status.conditions) do
          if condition.type == "Ready" and condition.status == "False" then
            hs.status = "Degraded"
            hs.message = condition.message
            return hs
          end
          if condition.type == "Ready" and condition.status == "True" then
            hs.status = "Healthy"
            hs.message = condition.message
            return hs
          end
        end
      end
    end
    hs.status = "Progressing"
    hs.message = "Waiting for certificate"
    return hs
  
  resource.customizations.ignoreDifferences.apps_Deployment: |
    jsonPointers:
    - /spec/replicas
  
  resource.exclusions: |
    - apiGroups:
      - cilium.io
      kinds:
      - CiliumIdentity
      clusters:
      - "*"
```

## Monitoring and Observability

### Prometheus Metrics

```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: argocd-metrics
  namespace: argocd
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: argocd-metrics
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "ArgoCD",
    "panels": [
      {
        "title": "Apps by Sync Status",
        "targets": [
          {
            "expr": "sum by (sync_status) (argocd_app_info)"
          }
        ]
      },
      {
        "title": "Apps by Health Status",
        "targets": [
          {
            "expr": "sum by (health_status) (argocd_app_info)"
          }
        ]
      },
      {
        "title": "Sync Operations",
        "targets": [
          {
            "expr": "sum(increase(argocd_app_sync_total[5m])) by (name, namespace)"
          }
        ]
      }
    ]
  }
}
```

## Security Best Practices

1. **Enable RBAC**: Use fine-grained RBAC policies
2. **Use AppProjects**: Isolate applications and limit access
3. **Encrypt Secrets**: Use sealed-secrets or external secret operators
4. **Network Policies**: Restrict ArgoCD component communication
5. **Audit Logging**: Enable and monitor audit logs
6. **Git Webhook Secrets**: Use webhook secrets for repository events
7. **TLS Everywhere**: Enable TLS for all communications
8. **Service Account Tokens**: Rotate tokens regularly

## Troubleshooting

### Common Issues

```bash
# Check ArgoCD server logs
kubectl logs -n argocd deployment/argocd-server

# Check application controller logs
kubectl logs -n argocd deployment/argocd-application-controller

# Force refresh application
argocd app get <app-name> --refresh

# Hard refresh (bypass cache)
argocd app get <app-name> --hard-refresh

# Manual sync with prune
argocd app sync <app-name> --prune

# Debug sync issues
argocd app sync <app-name> --dry-run

# Check resource differences
argocd app diff <app-name>
```

## Integration Examples

### CI/CD Pipeline Integration

```yaml
# .gitlab-ci.yml
deploy:
  stage: deploy
  script:
    - argocd app sync $APP_NAME --auth-token $ARGOCD_TOKEN
    - argocd app wait $APP_NAME --health --timeout 300
  only:
    - main
```

### Webhook Configuration

```bash
# Configure GitHub webhook
curl -X POST https://argocd.example.com/api/v1/applications/<app>/events \
  -H "Authorization: Bearer $ARGOCD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"revision": "HEAD"}'
```