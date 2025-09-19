# K3s - Lightweight Kubernetes

## Overview

K3s is a highly available, certified Kubernetes distribution designed for production workloads in unattended, resource-constrained, remote locations or inside IoT appliances. It's packaged as a single binary less than 100MB and uses less than 512MB of RAM.

## Architecture

### Design Principles
```yaml
k3s_design:
  optimizations:
    - Single binary under 100MB
    - Minimal memory footprint (~512MB)
    - Removed legacy/alpha features
    - SQLite default (etcd optional)
    - Embedded components
  
  embedded_components:
    - containerd
    - flannel
    - coredns
    - traefik
    - local-path-provisioner
    - metrics-server
  
  removed_features:
    - Legacy APIs
    - Non-default features
    - Cloud provider specific code
    - Storage drivers (except required)
```

### Architecture Overview
```
┌─────────────────────────────────────┐
│         K3s Server Node             │
├─────────────────────────────────────┤
│  ┌─────────┐  ┌──────────┐         │
│  │ API     │  │ Scheduler│         │
│  │ Server  │  └──────────┘         │
│  └─────────┘  ┌──────────┐         │
│  ┌─────────┐  │Controller│         │
│  │ etcd/   │  │ Manager  │         │
│  │ SQLite  │  └──────────┘         │
│  └─────────┘                       │
├─────────────────────────────────────┤
│         Embedded Services           │
│  containerd | flannel | coredns    │
│  traefik | local-path | metrics    │
└─────────────────────────────────────┘
         │
         ├──────────┬────────────┐
         │          │            │
    ┌────▼───┐ ┌───▼────┐  ┌───▼────┐
    │ Agent  │ │ Agent  │  │ Agent  │
    │ Node   │ │ Node   │  │ Node   │
    └────────┘ └────────┘  └────────┘
```

### Component Comparison
```yaml
k8s_vs_k3s:
  standard_kubernetes:
    - etcd
    - kube-apiserver
    - kube-scheduler
    - kube-controller-manager
    - kubelet
    - kube-proxy
    - container runtime
    - CNI plugin
    - DNS (CoreDNS)
    - Ingress controller
  
  k3s_embedded:
    - SQLite (default) or etcd
    - All control plane in single process
    - containerd (embedded)
    - flannel (embedded)
    - CoreDNS (embedded)
    - Traefik (embedded)
    - Local-path provisioner
    - Service load balancer
```

## Installation

### Quick Start
```bash
# Single line installation
curl -sfL https://get.k3s.io | sh -

# Installation with specific version
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.28.5+k3s1 sh -

# Check status
sudo systemctl status k3s
sudo k3s kubectl get nodes
```

### Server Installation Options
```bash
# With external database
curl -sfL https://get.k3s.io | sh -s - \
  --datastore-endpoint="mysql://username:password@tcp(hostname:3306)/k3s"

# With embedded etcd (HA)
curl -sfL https://get.k3s.io | sh -s - \
  --cluster-init

# Join additional servers
curl -sfL https://get.k3s.io | sh -s - \
  --server https://server1:6443 \
  --token <node-token>

# Custom installation
curl -sfL https://get.k3s.io | sh -s - \
  --write-kubeconfig-mode 644 \
  --tls-san loadbalancer.example.com \
  --node-taint CriticalAddonsOnly=true:NoExecute \
  --bind-address 0.0.0.0 \
  --advertise-address 10.0.0.1 \
  --node-label "node.kubernetes.io/instance-type=t3.medium"
```

### Agent Installation
```bash
# Join agent to cluster
curl -sfL https://get.k3s.io | K3S_URL=https://server:6443 K3S_TOKEN=<node-token> sh -

# Agent with custom options
curl -sfL https://get.k3s.io | K3S_URL=https://server:6443 K3S_TOKEN=<token> sh -s - \
  --node-label "workload=gpu" \
  --node-taint "gpu=true:NoSchedule"
```

### Air-Gap Installation
```bash
# Download K3s binary and images
wget https://github.com/k3s-io/k3s/releases/download/v1.28.5+k3s1/k3s
wget https://github.com/k3s-io/k3s/releases/download/v1.28.5+k3s1/k3s-airgap-images-amd64.tar.gz

# Setup on air-gapped system
sudo mkdir -p /var/lib/rancher/k3s/agent/images/
sudo cp k3s-airgap-images-amd64.tar.gz /var/lib/rancher/k3s/agent/images/
sudo chmod +x k3s
sudo cp k3s /usr/local/bin/

# Install K3s
sudo k3s server &

# Or use install script offline
INSTALL_K3S_SKIP_DOWNLOAD=true ./install.sh
```

## Configuration

### Server Configuration
```yaml
# /etc/rancher/k3s/config.yaml
write-kubeconfig-mode: "0644"
tls-san:
  - "k3s.example.com"
  - "192.168.1.100"

# Cluster configuration
cluster-cidr: "10.42.0.0/16"
service-cidr: "10.43.0.0/16"
cluster-dns: "10.43.0.10"
cluster-domain: "cluster.local"

# Embedded component configuration
disable:
  - traefik
  - servicelb

# etcd snapshots
etcd-snapshot: true
etcd-snapshot-schedule-cron: "0 */6 * * *"
etcd-snapshot-retention: 5

# Resource limits
kubelet-arg:
  - "eviction-hard=memory.available<100Mi,nodefs.available<10%"
  - "eviction-soft=memory.available<200Mi,nodefs.available<15%"
  - "eviction-soft-grace-period=memory.available=5m,nodefs.available=5m"

# Security
secrets-encryption: true
kube-apiserver-arg:
  - "audit-log-path=/var/log/k3s-audit.log"
  - "audit-log-maxage=30"
  - "audit-log-maxbackup=10"
  - "audit-log-maxsize=100"

# Node labels and taints
node-label:
  - "node-role.kubernetes.io/edge=true"
  - "datacenter=edge-1"
node-taint:
  - "node-role.kubernetes.io/edge:NoSchedule"
```

### Agent Configuration
```yaml
# /etc/rancher/k3s/config.yaml
server: https://k3s-server:6443
token: <node-token>

# Container runtime
container-runtime-endpoint: unix:///run/k3s/containerd/containerd.sock
pause-image: rancher/mirrored-pause:3.6

# Kubelet configuration
kubelet-arg:
  - "max-pods=110"
  - "resolv-conf=/etc/resolv.conf"

# Private registry
private-registry: /etc/rancher/k3s/registries.yaml

# Node labels
node-label:
  - "workload-type=iot"
  - "hardware=raspberrypi"
```

### Registry Configuration
```yaml
# /etc/rancher/k3s/registries.yaml
mirrors:
  docker.io:
    endpoint:
      - "https://registry-1.docker.io"
      - "https://mirror.gcr.io"
  
  "private-registry.example.com:5000":
    endpoint:
      - "https://private-registry.example.com:5000"

configs:
  "private-registry.example.com:5000":
    auth:
      username: user
      password: pass
    tls:
      cert_file: /etc/ssl/certs/registry.crt
      key_file: /etc/ssl/private/registry.key
      ca_file: /etc/ssl/certs/ca-bundle.crt
```

## Cluster Management

### High Availability Setup

#### Embedded etcd HA
```bash
# First server (initializes cluster)
curl -sfL https://get.k3s.io | sh -s - server \
  --cluster-init \
  --tls-san "k3s-vip.example.com"

# Additional servers
K3S_TOKEN=<token> curl -sfL https://get.k3s.io | sh -s - server \
  --server https://k3s-1:6443 \
  --tls-san "k3s-vip.example.com"
```

#### External Database HA
```bash
# MySQL/PostgreSQL setup
CREATE DATABASE k3s;
GRANT ALL ON k3s.* TO 'k3s'@'%' IDENTIFIED BY 'k3s-password';

# K3s servers pointing to external DB
curl -sfL https://get.k3s.io | sh -s - server \
  --datastore-endpoint="mysql://k3s:k3s-password@tcp(mysql.example.com:3306)/k3s" \
  --tls-san "k3s-vip.example.com"
```

#### Load Balancer Configuration
```nginx
# nginx.conf for K3s API load balancing
upstream k3s-servers {
    server k3s-server-1:6443 max_fails=3 fail_timeout=30s;
    server k3s-server-2:6443 max_fails=3 fail_timeout=30s;
    server k3s-server-3:6443 max_fails=3 fail_timeout=30s;
}

server {
    listen 6443;
    proxy_pass k3s-servers;
    proxy_timeout 10m;
    proxy_connect_timeout 1s;
}
```

### Backup and Restore

#### etcd Snapshots
```bash
# Manual snapshot
sudo k3s etcd-snapshot save --name manual-backup

# List snapshots
sudo k3s etcd-snapshot list

# Restore from snapshot
sudo systemctl stop k3s
sudo k3s server \
  --cluster-reset \
  --cluster-reset-restore-path=/var/lib/rancher/k3s/server/db/etcd-old/snapshot-file

# S3 backup configuration
sudo k3s etcd-snapshot save \
  --s3 \
  --s3-bucket=k3s-backups \
  --s3-region=us-west-2 \
  --s3-access-key=<access-key> \
  --s3-secret-key=<secret-key>
```

#### Backup Script
```bash
#!/bin/bash
# k3s-backup.sh

BACKUP_DIR="/backup/k3s"
S3_BUCKET="s3://k3s-backups"
DATE=$(date +%Y%m%d-%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup etcd
k3s etcd-snapshot save --name backup-$DATE

# Backup K3s configuration
tar -czf $BACKUP_DIR/k3s-config-$DATE.tar.gz \
  /etc/rancher/k3s \
  /var/lib/rancher/k3s/server/tls

# Backup critical workloads
kubectl get all --all-namespaces -o yaml > $BACKUP_DIR/resources-$DATE.yaml

# Sync to S3
aws s3 sync $BACKUP_DIR $S3_BUCKET/

# Cleanup old backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Upgrades

#### Automated Upgrades
```yaml
# system-upgrade-controller
apiVersion: v1
kind: Namespace
metadata:
  name: system-upgrade

---
apiVersion: upgrade.cattle.io/v1
kind: Plan
metadata:
  name: server-plan
  namespace: system-upgrade
spec:
  concurrency: 1
  cordon: true
  nodeSelector:
    matchExpressions:
    - key: node-role.kubernetes.io/control-plane
      operator: In
      values:
      - "true"
  serviceAccountName: system-upgrade
  upgrade:
    image: rancher/k3s-upgrade
  version: v1.28.5+k3s1

---
apiVersion: upgrade.cattle.io/v1
kind: Plan
metadata:
  name: agent-plan
  namespace: system-upgrade
spec:
  concurrency: 2
  nodeSelector:
    matchExpressions:
    - key: node-role.kubernetes.io/control-plane
      operator: DoesNotExist
  prepare:
    args:
    - prepare
    - server-plan
    image: rancher/k3s-upgrade
  serviceAccountName: system-upgrade
  upgrade:
    image: rancher/k3s-upgrade
  version: v1.28.5+k3s1
```

#### Manual Upgrade
```bash
# Upgrade server
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.28.5+k3s1 sh -

# Verify upgrade
k3s kubectl get nodes
k3s --version

# Upgrade agents
# On each agent node:
curl -sfL https://get.k3s.io | K3S_URL=https://server:6443 K3S_TOKEN=<token> INSTALL_K3S_VERSION=v1.28.5+k3s1 sh -
```

## Use Cases

### Edge Computing

#### Edge Cluster Configuration
```yaml
# Minimal edge deployment
apiVersion: v1
kind: ConfigMap
metadata:
  name: edge-config
data:
  config.yaml: |
    # K3s edge configuration
    disable:
      - traefik
      - metrics-server
    
    kubelet-arg:
      - "max-pods=20"
      - "image-gc-high-threshold=95"
      - "image-gc-low-threshold=90"
    
    # Reduce resource usage
    kube-apiserver-arg:
      - "watch-cache=false"
      - "default-watch-cache-size=0"
```

#### Edge Workload Example
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: edge-monitor
spec:
  selector:
    matchLabels:
      app: edge-monitor
  template:
    metadata:
      labels:
        app: edge-monitor
    spec:
      hostNetwork: true
      containers:
      - name: monitor
        image: edge/monitor:latest
        resources:
          limits:
            memory: "128Mi"
            cpu: "100m"
        volumeMounts:
        - name: data
          mountPath: /data
        env:
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
      volumes:
      - name: data
        hostPath:
          path: /var/edge/data
```

### IoT Deployments

#### Raspberry Pi Cluster
```bash
# Install K3s on Raspberry Pi
curl -sfL https://get.k3s.io | sh -s - \
  --disable traefik \
  --disable servicelb \
  --write-kubeconfig-mode 644 \
  --kubelet-arg="eviction-hard=memory.available<100Mi" \
  --kubelet-arg="eviction-minimum-reclaim=memory.available=50Mi"

# ARM-specific configuration
cat <<EOF > /etc/rancher/k3s/config.yaml
node-label:
  - "kubernetes.io/arch=arm64"
  - "device-type=raspberrypi"
  - "location=field-device"
EOF
```

#### IoT Gateway Pattern
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: iot-gateway-config
data:
  mosquitto.conf: |
    listener 1883
    protocol mqtt
    listener 9001
    protocol websockets
    allow_anonymous false
    password_file /mosquitto/config/passwd

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iot-gateway
spec:
  replicas: 1
  selector:
    matchLabels:
      app: iot-gateway
  template:
    metadata:
      labels:
        app: iot-gateway
    spec:
      nodeSelector:
        device-type: gateway
      containers:
      - name: mosquitto
        image: eclipse-mosquitto:2.0
        ports:
        - containerPort: 1883
        - containerPort: 9001
        volumeMounts:
        - name: config
          mountPath: /mosquitto/config
        - name: data
          mountPath: /mosquitto/data
      volumes:
      - name: config
        configMap:
          name: iot-gateway-config
      - name: data
        hostPath:
          path: /var/iot/mosquitto
```

### Development Clusters

#### K3d (K3s in Docker)
```bash
# Install k3d
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

# Create development cluster
k3d cluster create dev \
  --servers 3 \
  --agents 2 \
  --port "80:80@loadbalancer" \
  --port "443:443@loadbalancer" \
  --volume /tmp/k3d:/var/lib/rancher/k3s/storage \
  --api-port 6443 \
  --k3s-arg "--disable=traefik@server:0" \
  --k3s-arg "--tls-san=k3d-dev@server:*"

# Create cluster with registry
k3d cluster create dev-with-registry \
  --registry-create dev-registry:0.0.0.0:5000 \
  --registry-use k3d-dev-registry:5000

# Multi-cluster setup
k3d cluster create staging --port 8080:80@loadbalancer
k3d cluster create production --port 8081:80@loadbalancer
```

#### Local Development Environment
```yaml
# skaffold.yaml for K3s development
apiVersion: skaffold/v3
kind: Config
metadata:
  name: k3s-dev
build:
  artifacts:
  - image: myapp
    docker:
      dockerfile: Dockerfile
deploy:
  kubectl:
    manifests:
    - k8s/*.yaml
portForward:
- resourceType: deployment
  resourceName: myapp
  port: 8080
  localPort: 8080
```

## Production Considerations

### Security Hardening

#### CIS Benchmark Compliance
```bash
# Run CIS benchmark scan
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml

# Apply security policies
cat <<EOF | kubectl apply -f -
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
  - ALL
  volumes:
  - 'configMap'
  - 'emptyDir'
  - 'projected'
  - 'secret'
  - 'downwardAPI'
  - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  supplementalGroups:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
EOF
```

#### Network Policies
```yaml
# Default deny all
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
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
  name: web-allow-ingress
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

### Resource Management

#### Resource Limits
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: production
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    limits.cpu: "200"
    limits.memory: 400Gi
    persistentvolumeclaims: "10"
    services.loadbalancers: "2"

---
apiVersion: v1
kind: LimitRange
metadata:
  name: pod-limits
  namespace: production
spec:
  limits:
  - max:
      cpu: "2"
      memory: "4Gi"
    min:
      cpu: "100m"
      memory: "64Mi"
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    type: Pod
```

### Monitoring

#### Lightweight Monitoring Stack
```yaml
# Prometheus configuration for K3s
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 30s
      evaluation_interval: 30s
      external_labels:
        cluster: 'k3s-edge'
    
    scrape_configs:
    - job_name: 'kubernetes-nodes'
      kubernetes_sd_configs:
      - role: node
      relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
    
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

#### Node Exporter DaemonSet
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      hostPID: true
      hostIPC: true
      hostNetwork: true
      containers:
      - name: node-exporter
        image: prom/node-exporter:latest
        args:
        - --path.sysfs=/host/sys
        - --path.rootfs=/host/root
        resources:
          requests:
            cpu: 10m
            memory: 24Mi
          limits:
            cpu: 100m
            memory: 64Mi
        volumeMounts:
        - name: sys
          mountPath: /host/sys
          readOnly: true
        - name: root
          mountPath: /host/root
          readOnly: true
      volumes:
      - name: sys
        hostPath:
          path: /sys
      - name: root
        hostPath:
          path: /
```

### Performance Optimization

#### Tuning for Edge/IoT
```yaml
# K3s server optimizations
server-config:
  kube-apiserver-arg:
    - "max-requests-inflight=100"
    - "max-mutating-requests-inflight=50"
    - "watch-cache=false"
    - "default-not-ready-toleration-seconds=30"
    - "default-unreachable-toleration-seconds=30"
  
  kube-controller-manager-arg:
    - "node-monitor-period=20s"
    - "node-monitor-grace-period=40s"
    - "pod-eviction-timeout=2m"
  
  kubelet-arg:
    - "node-status-update-frequency=20s"
    - "image-pull-progress-deadline=5m"
    - "eviction-pressure-transition-period=30s"
```

#### Storage Optimization
```yaml
# Local path provisioner configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-path-config
  namespace: kube-system
data:
  config.json: |
    {
      "nodePathMap": [
        {
          "node": "DEFAULT_PATH_FOR_NON_LISTED_NODES",
          "paths": ["/var/lib/rancher/k3s/storage"]
        },
        {
          "node": "ssd-node-*",
          "paths": ["/mnt/fast-ssd/k3s-storage"]
        }
      ]
    }
```

## Troubleshooting

### Common Issues

#### Debugging K3s
```bash
# Check K3s logs
journalctl -u k3s -f

# Check specific component logs
k3s kubectl logs -n kube-system deployment/coredns
k3s kubectl logs -n kube-system daemonset/svclb-traefik

# Debug mode
k3s server --debug

# Check certificates
k3s kubectl get csr
openssl x509 -in /var/lib/rancher/k3s/server/tls/server-ca.crt -text -noout
```

#### Network Troubleshooting
```bash
# Check flannel
k3s kubectl -n kube-system logs -l app=flannel

# Test network connectivity
k3s kubectl run test-pod --image=nicolaka/netshoot -it --rm

# Inside the pod
dig kubernetes.default.svc.cluster.local
curl -k https://kubernetes.default:443
```

#### Reset Cluster
```bash
# Uninstall K3s server
/usr/local/bin/k3s-uninstall.sh

# Uninstall K3s agent
/usr/local/bin/k3s-agent-uninstall.sh

# Manual cleanup
sudo rm -rf /var/lib/rancher/k3s
sudo rm -rf /etc/rancher/k3s
sudo rm -f /usr/local/bin/k3s*
```

## Best Practices

1. **Deployment Strategy**
   - Use K3s for edge/IoT workloads
   - Consider resource constraints
   - Plan for intermittent connectivity
   - Implement proper monitoring

2. **Security**
   - Disable unused components
   - Implement network policies
   - Use PodSecurityPolicies/Standards
   - Regular security updates

3. **Resource Management**
   - Set appropriate resource limits
   - Monitor resource usage
   - Implement proper eviction policies
   - Use lightweight images

4. **High Availability**
   - Use embedded etcd for simplicity
   - External database for larger deployments
   - Regular backup schedule
   - Test restore procedures