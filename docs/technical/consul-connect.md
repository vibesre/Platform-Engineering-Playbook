# Consul Connect Service Mesh

## Overview

Consul Connect is HashiCorp's service mesh solution that provides secure service-to-service connectivity with automatic TLS encryption and identity-based authorization. Built on top of HashiCorp Consul, it integrates service discovery, configuration, and segmentation into a unified platform that works across multiple platforms and runtimes.

## Architecture

### Core Components

#### Control Plane
- **Consul Servers**: Store service registry, configuration, and coordinate the mesh
- **Connect CA**: Built-in certificate authority for service identity
- **Intentions**: Service-to-service authorization rules
- **Configuration Entries**: Centralized mesh configuration

#### Data Plane
- **Envoy Proxy**: Default sidecar proxy (pluggable architecture)
- **Built-in Proxy**: Lightweight alternative for development
- **Native Integration**: SDK for direct application integration

### Architecture Patterns
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Service   │────▶│    Envoy    │────▶│   Consul    │
│     App     │     │   Sidecar   │     │   Servers   │
└─────────────┘     └─────────────┘     └─────────────┘
                            │
                    ┌───────▼────────┐
                    │ Service Mesh   │
                    │ Control Plane  │
                    └────────────────┘
```

### Multi-Runtime Support
- Kubernetes (via Helm chart)
- VMs and bare metal
- Nomad integration
- AWS ECS and Lambda
- Multi-cloud and hybrid deployments

## Installation

### Prerequisites
- Kubernetes 1.22+ (for K8s deployment)
- Helm 3.2+
- Consul 1.14+

### Kubernetes Installation

#### Helm Installation
```bash
# Add HashiCorp Helm repository
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

# Install Consul with Connect enabled
helm install consul hashicorp/consul \
  --set global.name=consul \
  --set global.datacenter=dc1 \
  --set connectInject.enabled=true \
  --set connectInject.default=true \
  --set controller.enabled=true \
  --set ui.enabled=true \
  --set ui.service.type=LoadBalancer
```

#### Production Configuration
```yaml
# values-production.yaml
global:
  name: consul
  datacenter: us-east-1
  gossipEncryption:
    secretName: consul-gossip-encryption-key
    secretKey: key
  tls:
    enabled: true
    enableAutoEncrypt: true
  acls:
    manageSystemACLs: true

server:
  replicas: 5
  bootstrapExpect: 5
  resources:
    requests:
      memory: 256Mi
      cpu: 250m
    limits:
      memory: 512Mi
      cpu: 500m
  affinity: |
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchLabels:
              app: {{ template "consul.name" . }}
              release: "{{ .Release.Name }}"
              component: server

connectInject:
  enabled: true
  default: true
  transparentProxy:
    defaultEnabled: true
  cni:
    enabled: true
  resources:
    requests:
      memory: 128Mi
      cpu: 100m
    limits:
      memory: 256Mi
      cpu: 200m

controller:
  enabled: true

ui:
  enabled: true
  service:
    type: LoadBalancer
```

### VM Installation
```bash
# Install Consul binary
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install consul

# Configure Consul agent
cat > /etc/consul.d/consul.hcl <<EOF
datacenter = "dc1"
data_dir = "/opt/consul"
log_level = "INFO"
server = false
encrypt = "base64_encoded_gossip_key"
retry_join = ["consul-server-1", "consul-server-2", "consul-server-3"]

connect {
  enabled = true
}

ports {
  grpc = 8502
}

enable_central_service_config = true
EOF

# Start Consul
sudo systemctl start consul
```

## Traffic Management

### Service Defaults
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceDefaults
metadata:
  name: frontend
spec:
  protocol: http
  meshGateway:
    mode: local
  expose:
    checks: true
    paths:
      - path: /health
        localPathPort: 8080
        listenerPort: 21500
```

### Service Splitter (Canary Deployment)
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceSplitter
metadata:
  name: api
spec:
  splits:
    - weight: 90
      service: api-v1
    - weight: 10
      service: api-v2
      requestHeaders:
        set:
          x-version: "v2"
```

### Service Router
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceRouter
metadata:
  name: api
spec:
  routes:
    - match:
        http:
          pathPrefix: /admin
          header:
            - name: x-admin-token
              present: true
      destination:
        service: api-admin
    - match:
        http:
          pathPrefix: /v2
      destination:
        service: api-v2
    - destination:
        service: api-v1
```

### Service Resolver
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceResolver
metadata:
  name: api
spec:
  defaultSubset: v1
  subsets:
    v1:
      filter: "Service.Meta.version == v1"
    v2:
      filter: "Service.Meta.version == v2"
  loadBalancer:
    policy: maglev
    hashPolicies:
      - field: header
        fieldValue: x-session-id
  connectTimeout: 15s
  requestTimeout: 30s
```

### Ingress Gateway
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: IngressGateway
metadata:
  name: public-gateway
spec:
  listeners:
    - port: 80
      protocol: http
      services:
        - name: frontend
          hosts: ["app.example.com"]
        - name: api
          hosts: ["api.example.com"]
```

### Mesh Gateway for Multi-DC
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: MeshGateway
metadata:
  name: mesh-gateway
spec:
  replicas: 3
  service:
    type: LoadBalancer
  resources:
    requests:
      memory: 256Mi
      cpu: 250m
    limits:
      memory: 512Mi
      cpu: 500m
```

## Security

### Service Intentions (Zero-Trust Authorization)
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceIntentions
metadata:
  name: frontend-to-api
spec:
  destination:
    name: api
  sources:
    - name: frontend
      permissions:
        - action: allow
          http:
            pathPrefix: /api
            methods: ["GET", "POST"]
        - action: deny
          http:
            pathPrefix: /api/admin
    - name: monitoring
      permissions:
        - action: allow
          http:
            pathExact: /metrics
            methods: ["GET"]
```

### JWT Authentication
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: JWTProvider
metadata:
  name: auth-provider
spec:
  issuer: "https://auth.example.com"
  jsonWebKeySet:
    remote:
      uri: "https://auth.example.com/.well-known/jwks.json"
  audiences:
    - "api.example.com"
  locations:
    - header:
        name: "Authorization"
        valuePrefix: "Bearer "
  forwarding:
    headerName: "X-JWT-Token"
```

### ACL Configuration
```hcl
# Bootstrap ACL system
acl = {
  enabled = true
  default_policy = "deny"
  down_policy = "extend-cache"
  enable_token_persistence = true
}

# Service token policy
service "api" {
  policy = "write"
}

service "frontend" {
  policy = "write"
}

service_prefix "" {
  policy = "read"
}

node_prefix "" {
  policy = "read"
}
```

### Certificate Management
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: ProxyDefaults
metadata:
  name: global
spec:
  config:
    protocol: http
  meshGateway:
    mode: local
  expose:
    checks: true
  accessLogs:
    enabled: true
    jsonFormat: true
```

### Vault Integration
```yaml
# Configure Vault as CA provider
apiVersion: consul.hashicorp.com/v1alpha1
kind: ConnectCA
metadata:
  name: vault-ca
spec:
  provider: vault
  config:
    address: https://vault.example.com:8200
    token: s.1234567890abcdef
    rootPKIPath: pki/
    intermediatePKIPath: pki_int/
```

## Observability

### Metrics with Prometheus
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: ProxyDefaults
metadata:
  name: global
spec:
  config:
    envoy_prometheus_bind_addr: "0.0.0.0:9102"
    envoy_stats_bind_addr: "0.0.0.0:9103"
  expose:
    checks: true
    paths:
      - path: /metrics
        protocol: http
        localPathPort: 9102
        listenerPort: 20200
```

### Distributed Tracing
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: ProxyDefaults
metadata:
  name: global
spec:
  config:
    envoy_tracing_json: |
      {
        "http": {
          "name": "envoy.tracers.zipkin",
          "typedConfig": {
            "@type": "type.googleapis.com/envoy.config.trace.v3.ZipkinConfig",
            "collector_cluster": "zipkin",
            "collector_endpoint_version": "HTTP_JSON",
            "collector_endpoint": "/api/v2/spans",
            "shared_span_context": false
          }
        }
      }
```

### Access Logs
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceDefaults
metadata:
  name: api
spec:
  protocol: http
  accessLogs:
    enabled: true
    disableListenerLogs: false
    type: stdout
    jsonFormat: |
      {
        "timestamp": "%START_TIME%",
        "method": "%REQ(:METHOD)%",
        "path": "%REQ(X-ENVOY-ORIGINAL-PATH?:PATH)%",
        "protocol": "%PROTOCOL%",
        "response_code": "%RESPONSE_CODE%",
        "response_flags": "%RESPONSE_FLAGS%",
        "bytes_received": "%BYTES_RECEIVED%",
        "bytes_sent": "%BYTES_SENT%",
        "duration": "%DURATION%",
        "upstream_service_time": "%RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)%"
      }
```

### Service Topology Visualization
```bash
# Access Consul UI
kubectl port-forward svc/consul-ui 8500:80

# Query service topology
consul catalog services
consul health service api

# View upstream dependencies
consul connect proxy -service frontend -upstream-destinatio
```

## Production Deployment Patterns

### Multi-Region Federation
```yaml
# Primary datacenter configuration
apiVersion: consul.hashicorp.com/v1alpha1
kind: Mesh
metadata:
  name: mesh
spec:
  transparentProxy:
    meshDestinationsOnly: true
  tls:
    incoming:
      tlsMinVersion: TLSv1_2
    outgoing:
      tlsMinVersion: TLSv1_2
---
# Federation through mesh gateways
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceDefaults
metadata:
  name: global
spec:
  meshGateway:
    mode: remote
```

### Disaster Recovery
```bash
# Backup Consul data
consul snapshot save backup.snap

# Restore from snapshot
consul snapshot restore backup.snap

# Automated backup CronJob
kubectl create cronjob consul-backup \
  --image=consul:latest \
  --schedule="0 2 * * *" \
  -- /bin/sh -c "consul snapshot save /backup/consul-$(date +%Y%m%d).snap"
```

### GitOps with ArgoCD
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: consul-config
  namespace: argocd
spec:
  project: infrastructure
  source:
    repoURL: https://github.com/company/consul-configs
    targetRevision: main
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: consul
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

### Progressive Delivery
```yaml
# Traffic splitting with Flagger
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: api
  namespace: production
spec:
  provider: consul
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  progressDeadlineSeconds: 60
  service:
    name: api
    port: 8080
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    webhooks:
    - name: acceptance-test
      type: pre-rollout
      url: http://flagger-loadtester.test/
      timeout: 30s
```

### Performance Optimization
```yaml
# Consul server performance tuning
apiVersion: v1
kind: ConfigMap
metadata:
  name: consul-server-config
data:
  extra.json: |
    {
      "performance": {
        "raft_multiplier": 1,
        "leave_drain_time": "5s",
        "rpc_hold_timeout": "7s"
      },
      "limits": {
        "http_max_conns_per_client": 200
      },
      "dns_config": {
        "cache_max_age": "30s",
        "use_cache": true
      }
    }
```

## Best Practices

### Service Registration
```yaml
# Kubernetes service with Consul annotations
apiVersion: v1
kind: Service
metadata:
  name: api
  annotations:
    consul.hashicorp.com/service-name: "api"
    consul.hashicorp.com/service-port: "8080"
    consul.hashicorp.com/service-tags: "v1,production"
    consul.hashicorp.com/service-meta-version: "1.0.0"
spec:
  selector:
    app: api
  ports:
  - port: 8080
```

### Health Checking
```yaml
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceDefaults
metadata:
  name: api
spec:
  protocol: http
  healthCheck:
    enabled: true
    interval: 10s
    timeout: 5s
    deregisterCriticalServiceAfter: 30m
    http: "/health"
    successBeforePassing: 2
    failuresBeforeCritical: 3
```

### Resource Management
```yaml
# Sidecar proxy resources
apiVersion: v1
kind: Pod
metadata:
  annotations:
    consul.hashicorp.com/connect-inject: "true"
    consul.hashicorp.com/sidecar-proxy-cpu-request: "100m"
    consul.hashicorp.com/sidecar-proxy-cpu-limit: "200m"
    consul.hashicorp.com/sidecar-proxy-memory-request: "128Mi"
    consul.hashicorp.com/sidecar-proxy-memory-limit: "256Mi"
```

### Troubleshooting
```bash
# Check service mesh health
consul members
consul operator raft list-peers

# Debug proxy configuration
consul connect proxy -service frontend -log-level debug

# View intentions
consul intention match frontend

# Check certificates
consul connect ca get-config
consul connect ca list

# Debug service discovery
consul catalog services -detailed
consul health service api -passing

# Proxy metrics
curl http://localhost:19000/stats/prometheus
```

## Integration Examples

### CI/CD Pipeline
```yaml
# GitLab CI example
deploy:
  script:
    - consul kv put config/app/version "$CI_COMMIT_SHA"
    - kubectl set image deployment/api api=api:$CI_COMMIT_SHA
    - consul config write service-splitter-canary.yaml
  environment:
    name: production
```

### Monitoring Stack Integration
```yaml
# Grafana dashboard for Consul
apiVersion: v1
kind: ConfigMap
metadata:
  name: consul-grafana-dashboard
data:
  consul-dashboard.json: |
    {
      "dashboard": {
        "title": "Consul Service Mesh",
        "panels": [
          {
            "targets": [
              {
                "expr": "consul_service_instances{service=\"$service\"}"
              }
            ]
          }
        ]
      }
    }
```

### Cost Optimization
```bash
# Analyze proxy resource usage
kubectl top pods -n production --containers | grep consul-sidecar

# Optimize DNS queries
consul config write - <<EOF
Kind: ProxyDefaults
Name: global
Config:
  local_request_timeout_ms: 5000
  local_idle_timeout_ms: 60000
EOF
```