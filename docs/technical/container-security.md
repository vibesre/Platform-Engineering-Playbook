# Container Security Best Practices and Tools

## Overview

Container security encompasses the entire lifecycle of containerized applications, from development through deployment and runtime. This guide provides comprehensive best practices, tools, and implementation patterns for securing containers in production environments.

## Container Security Layers

```
┌─────────────────────────────────────────────┐
│             Host OS Security                 │
├─────────────────────────────────────────────┤
│           Container Runtime                  │
├─────────────────────────────────────────────┤
│         Container Orchestration              │
├─────────────────────────────────────────────┤
│            Container Images                  │
├─────────────────────────────────────────────┤
│             Applications                     │
└─────────────────────────────────────────────┘
```

## Image Security

### 1. Base Image Selection

```dockerfile
# Good: Use specific, minimal base images
FROM alpine:3.18.4

# Better: Use distroless images
FROM gcr.io/distroless/static-debian11

# Best: Use scratch for static binaries
FROM scratch
```

### 2. Multi-Stage Builds

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Final stage
FROM scratch
COPY --from=builder /app/main /main
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 1001
ENTRYPOINT ["/main"]
```

### 3. Image Scanning

#### Trivy Integration

```yaml
# GitLab CI image scanning
image-scan:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - trivy image --format json --output trivy-report.json $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  artifacts:
    reports:
      container_scanning: trivy-report.json
```

#### Grype Configuration

```yaml
# .grype.yaml
check-for-app-update: true
db:
  auto-update: true
  cache-dir: "/tmp/grype-db"

ignore:
  - vulnerability: CVE-2021-12345
    fix-state: wont-fix
    package:
      name: libssl
      version: 1.1.1
```

### 4. Image Signing

```bash
# Cosign image signing
# Generate keypair
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key $REGISTRY/myapp:v1.0.0

# Verify signature
cosign verify --key cosign.pub $REGISTRY/myapp:v1.0.0
```

## Runtime Security

### 1. Security Contexts

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /app/cache
  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
```

### 2. Pod Security Standards

```yaml
# Pod Security Policy (deprecated, use Pod Security Standards)
apiVersion: v1
kind: Namespace
metadata:
  name: secure-namespace
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### 3. Runtime Protection with Falco

```yaml
# Falco DaemonSet
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: falco
  namespace: falco
spec:
  selector:
    matchLabels:
      app: falco
  template:
    metadata:
      labels:
        app: falco
    spec:
      serviceAccountName: falco
      containers:
      - name: falco
        image: falcosecurity/falco:latest
        securityContext:
          privileged: true
        volumeMounts:
        - name: config-volume
          mountPath: /etc/falco
        - name: proc-fs
          mountPath: /host/proc
          readOnly: true
        - name: docker-socket
          mountPath: /host/var/run/docker.sock
          readOnly: true
      volumes:
      - name: config-volume
        configMap:
          name: falco-config
      - name: proc-fs
        hostPath:
          path: /proc
      - name: docker-socket
        hostPath:
          path: /var/run/docker.sock
```

#### Falco Rules

```yaml
# Custom Falco rules
- rule: Unauthorized Process in Container
  desc: Detect unauthorized processes running in containers
  condition: >
    spawned_process and container and
    not proc.name in (allowed_processes)
  output: >
    Unauthorized process started in container
    (user=%user.name command=%proc.cmdline container=%container.name)
  priority: WARNING
  tags: [container, process]

- list: allowed_processes
  items: [nginx, node, python, java]
```

## Network Security

### 1. Network Policies

```yaml
# Default deny all traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
# Allow specific traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: production
      podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: production
      podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

### 2. Service Mesh Security

```yaml
# Istio mTLS configuration
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT

---
# Authorization policy
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: frontend-ingress
  namespace: production
spec:
  selector:
    matchLabels:
      app: frontend
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/backend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

## Secrets Management

### 1. External Secrets Operator

```yaml
# SecretStore configuration
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.company.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "app-role"
          serviceAccountRef:
            name: "app-sa"

---
# ExternalSecret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  refreshInterval: 15s
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
  - secretKey: database-password
    remoteRef:
      key: app/database
      property: password
```

### 2. Sealed Secrets

```yaml
# Sealed Secret example
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysecret
  namespace: production
spec:
  encryptedData:
    password: AgBvA8JqMz2kV2wK8Hj6X9rPL8Qpw...
  template:
    metadata:
      name: mysecret
      namespace: production
    type: Opaque
```

## Vulnerability Management

### 1. Continuous Scanning Pipeline

```yaml
# GitHub Actions workflow
name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'  # Daily scan

jobs:
  container-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build image
      run: docker build -t ${{ github.repository }}:${{ github.sha }} .
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ github.repository }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Run Grype vulnerability scanner
      uses: anchore/scan-action@v3
      with:
        image: ${{ github.repository }}:${{ github.sha }}
        fail-build: true
        severity-cutoff: high
```

### 2. Admission Control with OPA

```yaml
# ImagePolicyWebhook configuration
apiVersion: v1
kind: Config
clusters:
- name: image-bouncer-webhook
  cluster:
    certificate-authority: /etc/kubernetes/image-bouncer/ca.crt
    server: https://image-bouncer.kube-system.svc:443/image_policy
contexts:
- name: image-bouncer-webhook
  context:
    cluster: image-bouncer-webhook
    user: api-server
current-context: image-bouncer-webhook
users:
- name: api-server
  user:
    client-certificate: /etc/kubernetes/image-bouncer/client.crt
    client-key: /etc/kubernetes/image-bouncer/client.key
```

## Security Tools Integration

### 1. Kube-bench

```bash
# Run CIS Kubernetes Benchmark
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml

# Check results
kubectl logs -l app=kube-bench

# Custom configuration
apiVersion: batch/v1
kind: Job
metadata:
  name: kube-bench-custom
spec:
  template:
    spec:
      containers:
      - name: kube-bench
        image: aquasec/kube-bench:latest
        command: ["kube-bench"]
        args: ["node", "--benchmark", "cis-1.6"]
        volumeMounts:
        - name: var-lib-kubelet
          mountPath: /var/lib/kubelet
          readOnly: true
        - name: etc-systemd
          mountPath: /etc/systemd
          readOnly: true
        - name: etc-kubernetes
          mountPath: /etc/kubernetes
          readOnly: true
      volumes:
      - name: var-lib-kubelet
        hostPath:
          path: /var/lib/kubelet
      - name: etc-systemd
        hostPath:
          path: /etc/systemd
      - name: etc-kubernetes
        hostPath:
          path: /etc/kubernetes
      restartPolicy: Never
```

### 2. Kubesec

```yaml
# Kubesec analysis in CI/CD
kubesec-scan:
  stage: security
  script:
    - curl -X POST --data-binary @deployment.yaml https://v2.kubesec.io/scan
    - |
      score=$(curl -X POST --data-binary @deployment.yaml https://v2.kubesec.io/scan | jq '.[0].score')
      if [ "$score" -lt "5" ]; then
        echo "Security score too low: $score"
        exit 1
      fi
```

### 3. RBAC Audit

```yaml
# ServiceAccount with minimal permissions
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["app-secrets"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rolebinding
  namespace: production
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: app-role
subjects:
- kind: ServiceAccount
  name: app-sa
  namespace: production
```

## Compliance and Auditing

### 1. Audit Logging

```yaml
# Audit policy
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  # Log pod creation at Metadata level
  - level: Metadata
    omitStages:
    - RequestReceived
    resources:
    - group: ""
      resources: ["pods"]
    namespaces: ["production", "staging"]
    
  # Log secret access at RequestResponse level
  - level: RequestResponse
    omitStages:
    - RequestReceived
    resources:
    - group: ""
      resources: ["secrets"]
    
  # Log everything else at Metadata level
  - level: Metadata
    omitStages:
    - RequestReceived
```

### 2. Compliance Scanning with Polaris

```yaml
# Polaris configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: polaris-config
  namespace: polaris
data:
  config.yaml: |
    checks:
      cpuRequestsMissing: warning
      cpuLimitsMissing: error
      memoryRequestsMissing: warning
      memoryLimitsMissing: error
      readinessProbeMissing: warning
      livenessProbeMissing: warning
      pullPolicyNotAlways: ignore
      tagNotSpecified: error
      hostNetworkSet: error
      hostPIDSet: error
      notReadOnlyRootFilesystem: warning
      runAsRootAllowed: error
      runAsPrivileged: error
      dangerousCapabilities: error
      insecureCapabilities: warning
    exemptions:
      - controllerNames:
        - kube-system
        - kube-proxy
        - kube-dns
        rules:
        - hostNetworkSet
```

## Production Security Patterns

### 1. Zero Trust Architecture

```yaml
# Calico GlobalNetworkPolicy for zero trust
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: deny-all-traffic
spec:
  tier: security
  order: 1000
  selector: all()
  types:
  - Ingress
  - Egress
  ingress:
  - action: Deny
  egress:
  - action: Deny
```

### 2. Container Isolation

```yaml
# gVisor runtime class
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
---
# Pod using gVisor
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  runtimeClassName: gvisor
  containers:
  - name: app
    image: myapp:latest
```

### 3. Workload Identity

```yaml
# Workload Identity binding (GKE example)
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production
  annotations:
    iam.gke.io/gcp-service-account: app@project-id.iam.gserviceaccount.com
```

## Monitoring and Incident Response

### 1. Security Monitoring Stack

```yaml
# Prometheus ServiceMonitor for security metrics
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: falco-exporter
  namespace: falco
spec:
  selector:
    matchLabels:
      app: falco-exporter
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### 2. Alerting Rules

```yaml
# PrometheusRule for security alerts
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: security-alerts
  namespace: monitoring
spec:
  groups:
  - name: container-security
    interval: 30s
    rules:
    - alert: ContainerPrivilegedMode
      expr: |
        kube_pod_container_security_context_privileged{namespace!~"kube-.*"} > 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "Container running in privileged mode"
        description: "Container {{ $labels.container }} in pod {{ $labels.pod }} is running in privileged mode"
    
    - alert: ContainerRunningAsRoot
      expr: |
        kube_pod_container_security_context_run_as_user{namespace!~"kube-.*"} == 0
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Container running as root"
        description: "Container {{ $labels.container }} in pod {{ $labels.pod }} is running as root user"
```

## Security Checklist

### Development Phase
- [ ] Use minimal base images
- [ ] Implement multi-stage builds
- [ ] Run as non-root user
- [ ] Scan images for vulnerabilities
- [ ] Sign container images
- [ ] Use specific image tags, not latest

### Deployment Phase
- [ ] Implement Pod Security Standards
- [ ] Configure RBAC with least privilege
- [ ] Use Network Policies
- [ ] Enable audit logging
- [ ] Implement admission control
- [ ] Configure resource limits

### Runtime Phase
- [ ] Enable runtime protection (Falco)
- [ ] Implement network segmentation
- [ ] Monitor security events
- [ ] Regular vulnerability scanning
- [ ] Incident response procedures
- [ ] Regular security audits

## Conclusion

Container security requires a comprehensive, defense-in-depth approach spanning the entire container lifecycle. By implementing these best practices and leveraging the security tools ecosystem, organizations can significantly reduce their attack surface while maintaining the agility and efficiency that containers provide.