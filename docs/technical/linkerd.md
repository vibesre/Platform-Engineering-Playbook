# Linkerd Service Mesh

## Overview

Linkerd is an ultralight, security-first service mesh for Kubernetes. It provides runtime observability, reliability, and security without requiring code changes. Known for its simplicity, minimal resource footprint, and focus on operational simplicity, Linkerd pioneered the service mesh category.

## Architecture

### Design Principles
- **Simplicity**: Minimal configuration with sensible defaults
- **Performance**: Ultralight Rust-based data plane (linkerd2-proxy)
- **Security**: Automatic mTLS with zero configuration
- **Reliability**: Built-in retries, timeouts, and load balancing

### Core Components

#### Control Plane
- **Destination**: Service discovery and endpoint information
- **Identity**: Certificate management and mTLS
- **Proxy Injector**: Automatic sidecar injection
- **Policy Controller**: Fine-grained authorization policies
- **Web**: Dashboard and metrics aggregation

#### Data Plane
- **linkerd2-proxy**: Ultralight Rust proxy
  - Transparent HTTP/2 and TCP proxying
  - Automatic protocol detection
  - Built-in metrics and tracing

### Architecture Overview
```
┌─────────────┐     ┌─────────────┐
│   Service   │────▶│ linkerd2-   │
│     Pod     │     │   proxy     │
└─────────────┘     └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │Control Plane│
                    │ Components  │
                    └─────────────┘
```

## Installation

### Prerequisites
- Kubernetes cluster (1.21+)
- kubectl configured
- Stable network connectivity

### CLI Installation
```bash
# Install Linkerd CLI
curl -sL https://run.linkerd.io/install | sh

# Add to PATH
export PATH=$PATH:$HOME/.linkerd2/bin

# Verify installation
linkerd version
```

### Pre-Installation Checks
```bash
# Check cluster compatibility
linkerd check --pre

# Validate cluster configuration
linkerd check --proxy
```

### Control Plane Installation
```bash
# Generate installation manifest
linkerd install | kubectl apply -f -

# Wait for control plane
linkerd check

# Install visualization extensions
linkerd viz install | kubectl apply -f -
linkerd viz check
```

### High Availability Installation
```bash
# Generate HA installation
linkerd install --ha | kubectl apply -f -

# With custom values
linkerd install --ha \
  --set controllerReplicas=3 \
  --set identity.issuer.scheme=kubernetes.io/tls \
  | kubectl apply -f -
```

### Helm Installation
```bash
# Add Linkerd Helm repository
helm repo add linkerd https://helm.linkerd.io/stable

# Install CRDs
helm install linkerd-crds linkerd/linkerd-crds \
  -n linkerd --create-namespace

# Install control plane
helm install linkerd-control-plane \
  -n linkerd \
  --set-file identityTrustAnchorsPEM=ca.crt \
  --set-file identity.issuer.tls.crtPEM=issuer.crt \
  --set-file identity.issuer.tls.keyPEM=issuer.key \
  linkerd/linkerd-control-plane
```

## Traffic Management

### Service Profiles
Define service behavior and routes:

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: webapp
  namespace: production
spec:
  routes:
  - name: GET_users
    condition:
      method: GET
      pathRegex: "/users/[^/]+"
    responseClasses:
    - condition:
        status:
          min: 200
          max: 299
      isFailure: false
  - name: POST_users
    condition:
      method: POST
      pathRegex: "/users"
    timeout: 30s
  retryBudget:
    retryRatio: 0.2
    minRetriesPerSecond: 10
    ttl: 10s
```

### Traffic Split (Canary Deployment)
```yaml
apiVersion: split.smi-spec.io/v1alpha1
kind: TrafficSplit
metadata:
  name: webapp-rollout
  namespace: production
spec:
  service: webapp
  backends:
  - service: webapp-v1
    weight: 900
  - service: webapp-v2
    weight: 100
```

### Load Balancing
```yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp
  annotations:
    linkerd.io/load-balancer: ewma  # Options: ewma, p2c, round-robin
spec:
  selector:
    app: webapp
  ports:
  - port: 80
```

### Circuit Breaking
```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: backend
  namespace: production
spec:
  routes:
  - name: api_route
    condition:
      method: GET
      pathRegex: "/api/.*"
    responseClasses:
    - condition:
        status:
          min: 500
          max: 599
      isFailure: true
  retryBudget:
    retryRatio: 0.1
    minRetriesPerSecond: 5
    ttl: 10s
```

### Retries and Timeouts
```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: api-service
spec:
  routes:
  - name: critical_endpoint
    condition:
      pathRegex: "/api/critical"
    timeout: 5s
    isRetryable: true
  - name: bulk_operation
    condition:
      pathRegex: "/api/bulk"
    timeout: 60s
    isRetryable: false
```

## Security

### Automatic mTLS
Linkerd automatically enables mTLS with zero configuration:

```bash
# Check mTLS status
linkerd viz edges -n production

# View TLS details
linkerd viz tap deploy/webapp -n production | grep tls
```

### Policy Configuration
```yaml
# Server authorization
apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata:
  name: api-server
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  port: 8080
  proxyProtocol: "HTTP/2"
---
# Server authorization
apiVersion: policy.linkerd.io/v1beta1
kind: ServerAuthorization
metadata:
  name: api-authz
  namespace: production
spec:
  server:
    name: api-server
  client:
    meshTLS:
      serviceAccounts:
      - name: frontend
        namespace: production
      - name: backend
        namespace: production
```

### Network Policies
```yaml
apiVersion: policy.linkerd.io/v1beta1
kind: NetworkAuthentication
metadata:
  name: cluster-network
  namespace: linkerd
spec:
  networks:
  - cidr: 10.0.0.0/8
  - cidr: 172.16.0.0/12
  - cidr: 192.168.0.0/16
```

### Service Account Binding
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: webapp
  namespace: production
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  namespace: production
spec:
  template:
    spec:
      serviceAccountName: webapp
```

## Observability

### Golden Metrics
Linkerd automatically collects:
- Success Rate (%)
- Request Rate (RPS)
- Latency (P50, P95, P99)

### Prometheus Integration
```yaml
# ServiceMonitor for Prometheus Operator
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: linkerd-metrics
  namespace: linkerd-viz
spec:
  selector:
    matchLabels:
      component: proxy
  endpoints:
  - port: admin-http
    interval: 30s
    path: /metrics
```

### Grafana Dashboards
```bash
# Access Linkerd dashboard
linkerd viz dashboard

# Port-forward Grafana
kubectl -n linkerd-viz port-forward svc/grafana 3000:80
```

### Distributed Tracing
```yaml
# Enable tracing in installation
linkerd install \
  --set global.proxy.trace.collector=jaeger.tracing:55678 \
  | kubectl apply -f -

# Or configure post-installation
kubectl annotate namespace production \
  config.linkerd.io/trace-collector=jaeger.tracing:55678
```

### Live Traffic Inspection
```bash
# Tap real-time traffic
linkerd viz tap deploy/webapp -n production

# Filter by path
linkerd viz tap deploy/webapp -n production --path /api

# Watch specific status codes
linkerd viz tap deploy/webapp -n production --response-status 500-599
```

### Service Topology
```bash
# View service dependencies
linkerd viz stat -n production deploy

# Edge relationships
linkerd viz edges -n production deployment

# Top routes
linkerd viz routes svc/webapp -n production
```

## Production Deployment Patterns

### Multi-Cluster Configuration
```bash
# Install multi-cluster components
linkerd --context=east multicluster install | \
  kubectl --context=west apply -f -

# Link clusters
linkerd --context=east multicluster link \
  --cluster-name east \
  --service-account-name linkerd-multicluster | \
  kubectl --context=west apply -f -
```

### GitOps with Flux
```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: HelmRepository
metadata:
  name: linkerd
  namespace: flux-system
spec:
  interval: 1h
  url: https://helm.linkerd.io/stable
---
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: linkerd-control-plane
  namespace: flux-system
spec:
  releaseName: linkerd-control-plane
  targetNamespace: linkerd
  chart:
    spec:
      chart: linkerd-control-plane
      sourceRef:
        kind: HelmRepository
        name: linkerd
  values:
    controllerReplicas: 3
    proxy:
      resources:
        cpu:
          request: 100m
          limit: 250m
        memory:
          request: 64Mi
          limit: 128Mi
```

### Progressive Delivery with Flagger
```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: webapp
  namespace: production
spec:
  provider: linkerd
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webapp
  progressDeadlineSeconds: 60
  service:
    port: 80
    targetPort: 8080
  analysis:
    interval: 30s
    threshold: 5
    maxWeight: 50
    stepWeight: 5
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 30s
```

### Resource Optimization
```yaml
# Proxy resource configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  namespace: production
  annotations:
    config.linkerd.io/proxy-cpu-request: "50m"
    config.linkerd.io/proxy-cpu-limit: "100m"
    config.linkerd.io/proxy-memory-request: "32Mi"
    config.linkerd.io/proxy-memory-limit: "64Mi"
spec:
  template:
    metadata:
      annotations:
        linkerd.io/inject: enabled
```

### High Availability Configuration
```yaml
# Control plane HA settings
apiVersion: v1
kind: ConfigMap
metadata:
  name: linkerd-config-overrides
  namespace: linkerd
data:
  values: |
    controllerReplicas: 3
    enablePodAntiAffinity: true
    resources:
      cpu:
        request: 100m
        limit: 500m
      memory:
        request: 128Mi
        limit: 512Mi
```

## Best Practices

### Injection Strategy
```yaml
# Namespace-level injection
apiVersion: v1
kind: Namespace
metadata:
  name: production
  annotations:
    linkerd.io/inject: enabled
```

### Monitoring and Alerting
```yaml
# Prometheus alerts
groups:
- name: linkerd
  rules:
  - alert: LinkerdHighErrorRate
    expr: |
      sum(rate(response_total{direction="inbound",tls="true",status_code!~"2.."}[5m])) by (namespace, deployment)
      /
      sum(rate(response_total{direction="inbound",tls="true"}[5m])) by (namespace, deployment)
      > 0.05
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High error rate in {{ $labels.namespace }}/{{ $labels.deployment }}"
```

### Security Hardening
```bash
# Enable strict mTLS validation
linkerd install \
  --proxy-require-identity-on-inbound-ports=all \
  --cluster-networks=10.0.0.0/8,172.16.0.0/12 \
  | kubectl apply -f -
```

### Troubleshooting Commands
```bash
# Check proxy logs
kubectl logs <pod-name> -c linkerd-proxy -n production

# Debug injection issues
kubectl get pods -n production -o yaml | linkerd inject --debug -

# Validate service profiles
linkerd profile --open-api swagger.json webapp -n production

# Check control plane health
linkerd check

# View proxy metrics
linkerd viz stat deploy -n production
```

## Integration Examples

### CI/CD Pipeline
```yaml
# GitHub Actions workflow
- name: Validate Linkerd
  run: |
    linkerd check --pre
    linkerd check

- name: Deploy with injection
  run: |
    kubectl apply -f manifests/ | linkerd inject -
```

### Service Profile Generation
```bash
# Generate from OpenAPI spec
linkerd profile --open-api api-spec.yaml webapp -n production | \
  kubectl apply -f -

# Generate from live traffic
linkerd viz profile webapp -n production --tap deploy/webapp --tap-duration 10s | \
  kubectl apply -f -
```

### Cost Analysis
```bash
# Resource usage report
kubectl top pods -n production --containers | grep linkerd-proxy

# Aggregate proxy metrics
linkerd viz stat deploy -n production -o json | \
  jq '.[] | {name: .name, cpu: .tcp_open_connections, memory: .memory_usage}'
```

## Performance Tuning

### Proxy Configuration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: linkerd-proxy-config
  namespace: production
data:
  config.yaml: |
    proxyCPURequest: 50m
    proxyCPULimit: 100m
    proxyMemoryRequest: 32Mi
    proxyMemoryLimit: 64Mi
    inboundConnectTimeout: 100ms
    outboundConnectTimeout: 1s
```

### Protocol Detection
```yaml
# Skip protocol detection for known ports
metadata:
  annotations:
    config.linkerd.io/skip-inbound-ports: "4222,5432"
    config.linkerd.io/skip-outbound-ports: "3306,6379"
```

### Connection Pooling
```yaml
# Tune HTTP/2 settings
metadata:
  annotations:
    config.linkerd.io/proxy-outbound-max-idle-conns-per-host: "100"
    config.linkerd.io/proxy-outbound-max-requests-per-connection: "2"
```