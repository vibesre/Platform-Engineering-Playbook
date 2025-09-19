# Helm - Kubernetes Package Manager

## Overview

Helm is the package manager for Kubernetes, simplifying the deployment and management of applications. It uses a packaging format called charts, which are collections of files that describe a related set of Kubernetes resources.

## Core Concepts

### Charts
A Helm chart is a bundle of information necessary to create an instance of a Kubernetes application:
- **Templates**: Kubernetes manifest files with templating directives
- **Values**: Configuration values that can be injected into templates
- **Dependencies**: Other charts that this chart depends on
- **Metadata**: Information about the chart (version, description, maintainers)

### Releases
A release is an instance of a chart running in a Kubernetes cluster. One chart can be installed multiple times into the same cluster, and each can be independently managed and upgraded.

### Repositories
Helm repositories are locations where packaged charts can be stored and shared. Similar to apt or yum repositories for Linux distributions.

## Installation and Setup

```bash
# Install Helm on macOS
brew install helm

# Install Helm on Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify installation
helm version

# Add official Helm stable charts repo
helm repo add stable https://charts.helm.sh/stable
helm repo update
```

## Basic Commands

```bash
# Search for charts
helm search hub wordpress
helm search repo nginx

# Install a chart
helm install my-release bitnami/nginx

# List releases
helm list
helm list --all-namespaces

# Get release status
helm status my-release

# Upgrade a release
helm upgrade my-release bitnami/nginx --set replicaCount=3

# Rollback a release
helm rollback my-release 1

# Uninstall a release
helm uninstall my-release
```

## Creating Custom Charts

### Chart Structure

```
mychart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── charts/            # Chart dependencies
├── templates/         # Template files
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── _helpers.tpl   # Template helpers
│   └── NOTES.txt      # Post-install notes
└── .helmignore        # Patterns to ignore
```

### Example Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.0"
maintainers:
  - name: Your Name
    email: your.email@example.com
dependencies:
  - name: postgresql
    version: "11.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

### Example values.yaml

```yaml
replicaCount: 2

image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: "1.0.0"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

postgresql:
  enabled: true
  auth:
    username: myapp
    database: myapp_db
```

### Example Template (deployment.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
          readinessProbe:
            httpGet:
              path: /ready
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ include "myapp.fullname" . }}-db
                  key: url
```

## Advanced Features

### Hooks

Helm hooks allow you to intervene at certain points in a release's lifecycle:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ .Release.Name }}-db-migrate"
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: db-migrate
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command: ["/bin/sh", "-c", "rake db:migrate"]
```

### Subchart Configuration

```yaml
# Parent chart values.yaml
postgresql:
  enabled: true
  global:
    postgresql:
      auth:
        postgresPassword: "mysecretpassword"
        username: "myapp"
        password: "myapppassword"
        database: "myapp_db"
  primary:
    persistence:
      size: 10Gi
```

### Using Helm Secrets

```bash
# Install helm-secrets plugin
helm plugin install https://github.com/jkroepke/helm-secrets

# Encrypt values file
helm secrets enc secrets.yaml

# Install chart with encrypted values
helm secrets install my-release ./mychart -f secrets.yaml
```

## Best Practices

### 1. Chart Development

```bash
# Lint your chart
helm lint ./mychart

# Dry run installation
helm install my-release ./mychart --dry-run --debug

# Package chart
helm package ./mychart

# Create chart museum
helm repo index --url https://charts.example.com .
```

### 2. Values Management

```yaml
# values-dev.yaml
environment: development
replicas: 1
resources:
  limits:
    memory: 512Mi
    cpu: 250m

# values-prod.yaml
environment: production
replicas: 3
resources:
  limits:
    memory: 2Gi
    cpu: 1000m

# Install with environment-specific values
helm install my-app ./mychart -f values-prod.yaml
```

### 3. Template Functions

```yaml
# _helpers.tpl
{{/*
Expand the name of the chart.
*/}}
{{- define "myapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "myapp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.chart" . }}
{{ include "myapp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

## Production Use Cases

### 1. Multi-Environment Deployment

```bash
# Create namespace-specific releases
helm install app-dev ./app -n development -f values-dev.yaml
helm install app-staging ./app -n staging -f values-staging.yaml
helm install app-prod ./app -n production -f values-prod.yaml
```

### 2. Blue-Green Deployment

```yaml
# blue-green-values.yaml
blueGreen:
  enabled: true
  productionSlot: blue
  previewSlot: green

# Switch traffic
helm upgrade my-app ./app --set blueGreen.productionSlot=green
```

### 3. GitOps Integration

```yaml
# ArgoCD Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/company/charts
    targetRevision: HEAD
    path: stable/my-app
    helm:
      valueFiles:
        - values-prod.yaml
      parameters:
        - name: image.tag
          value: "1.2.3"
```

### 4. CI/CD Pipeline Integration

```yaml
# .gitlab-ci.yml
deploy:
  stage: deploy
  script:
    - helm upgrade --install
        $APP_NAME
        ./chart
        --namespace $NAMESPACE
        --set image.tag=$CI_COMMIT_SHA
        --set ingress.host=$APP_HOST
        --wait
        --timeout 5m
```

## Troubleshooting

### Common Issues and Solutions

```bash
# Debug template rendering
helm template my-release ./mychart --debug

# Check manifest generation
helm get manifest my-release

# View computed values
helm get values my-release

# Check hooks
helm get hooks my-release

# Force update when pods are stuck
helm upgrade my-release ./mychart --force

# Fix failed release
helm rollback my-release 1
helm delete my-release --purge  # For Helm 2
helm uninstall my-release       # For Helm 3
```

### Health Checks

```yaml
# Robust health checks in templates
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 3
```

## Security Best Practices

### 1. RBAC for Helm

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: helm-user
  namespace: my-namespace
rules:
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: helm-user-binding
  namespace: my-namespace
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: helm-user
subjects:
  - kind: ServiceAccount
    name: helm-user
    namespace: my-namespace
```

### 2. Chart Signing

```bash
# Generate GPG key
gpg --full-generate-key

# Sign chart
helm package --sign --key 'John Doe' --keyring ~/.gnupg/pubring.gpg ./mychart

# Verify chart
helm verify mychart-0.1.0.tgz --keyring ~/.gnupg/pubring.gpg
```

### 3. Security Scanning

```bash
# Scan charts for security issues
helm plugin install https://github.com/fairwindsops/nova
nova find --wide

# Policy enforcement with OPA
helm plugin install https://github.com/open-policy-agent/conftest-helm-plugin
helm conftest my-chart/
```

## Conclusion

Helm simplifies Kubernetes application deployment and management through its templating system and package management capabilities. By following best practices and understanding its features, teams can efficiently manage complex Kubernetes deployments across multiple environments while maintaining consistency and reliability.