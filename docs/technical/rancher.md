# Rancher

## Overview

Rancher is an open-source multi-cluster Kubernetes management platform that simplifies the deployment and operation of Kubernetes clusters across any infrastructure. It provides a unified control plane for managing multiple Kubernetes clusters, whether they're on-premises, in the cloud, or at the edge.

## Architecture

### Core Components

#### Rancher Server
- **Management Plane**: Centralized control for all managed clusters
- **API Server**: RESTful API for cluster operations
- **Authentication Gateway**: Unified authentication across clusters
- **UI Dashboard**: Web-based management interface

#### Cluster Types
```yaml
# Managed Kubernetes Services
- Amazon EKS
- Google GKE
- Azure AKS
- Digital Ocean Kubernetes
- Linode Kubernetes Engine

# Rancher Kubernetes Engine (RKE)
- RKE1: Original Rancher distribution
- RKE2: Security-focused Kubernetes distribution
- K3s: Lightweight Kubernetes (integrated)

# Imported Clusters
- Any CNCF-compliant Kubernetes cluster
```

### Architecture Patterns

#### Hub and Spoke Model
```
┌─────────────────┐
│ Rancher Server  │
│  (Management)   │
└────────┬────────┘
         │
    ┌────┴────┬────────┬──────────┐
    │         │        │          │
┌───▼──┐ ┌───▼──┐ ┌───▼──┐  ┌───▼──┐
│ EKS  │ │ GKE  │ │ RKE2 │  │ K3s  │
└──────┘ └──────┘ └──────┘  └──────┘
```

#### High Availability Setup
```yaml
# Rancher HA Architecture
rancher_ha:
  load_balancer:
    - nginx
    - haproxy
  
  rancher_nodes:
    - rancher-1: etcd, control plane
    - rancher-2: etcd, control plane
    - rancher-3: etcd, control plane
  
  database:
    type: external
    options:
      - mysql
      - postgresql
```

## Installation

### Docker Installation (Single Node)
```bash
# Quick start for development
docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  --privileged \
  rancher/rancher:latest

# With persistent data
docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  -v /opt/rancher:/var/lib/rancher \
  --privileged \
  rancher/rancher:latest
```

### Kubernetes Installation (HA)
```bash
# Add Rancher Helm repository
helm repo add rancher-latest \
  https://releases.rancher.com/server-charts/latest
helm repo update

# Install cert-manager (required)
kubectl apply -f \
  https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create namespace
kubectl create namespace cattle-system

# Install Rancher
helm install rancher rancher-latest/rancher \
  --namespace cattle-system \
  --set hostname=rancher.example.com \
  --set bootstrapPassword=admin \
  --set ingress.tls.source=letsEncrypt \
  --set letsEncrypt.email=admin@example.com
```

### Air-Gapped Installation
```bash
# Download Rancher images
./rancher-save-images.sh --image-list ./rancher-images.txt

# Load images in air-gapped environment
./rancher-load-images.sh --image-list ./rancher-images.txt \
  --registry private-registry.example.com

# Install with private registry
helm install rancher ./rancher-<VERSION>.tgz \
  --namespace cattle-system \
  --set hostname=rancher.example.com \
  --set rancherImage=private-registry.example.com/rancher/rancher \
  --set systemDefaultRegistry=private-registry.example.com
```

## Cluster Management

### Creating Clusters

#### Custom Cluster
```bash
# Generate cluster configuration
cat <<EOF > cluster.yaml
nodes:
  - address: 10.0.1.10
    user: ubuntu
    role: [controlplane, etcd]
  - address: 10.0.1.11
    user: ubuntu
    role: [controlplane, etcd]
  - address: 10.0.1.12
    user: ubuntu
    role: [controlplane, etcd]
  - address: 10.0.1.20
    user: ubuntu
    role: [worker]
  - address: 10.0.1.21
    user: ubuntu
    role: [worker]

kubernetes:
  version: v1.28.5-rancher1
  network:
    plugin: canal
    options:
      flannel_backend_type: vxlan

services:
  etcd:
    backup_config:
      enabled: true
      interval_hours: 12
      retention: 6
EOF

# Create cluster using RKE
rke up --config cluster.yaml
```

#### Cloud Provider Clusters
```yaml
# EKS Cluster Configuration
apiVersion: eks.cattle.io/v1
kind: EKSClusterConfig
metadata:
  name: production-eks
spec:
  region: us-west-2
  kubernetesVersion: "1.28"
  nodeGroups:
    - name: worker-group
      instanceType: t3.medium
      desiredSize: 3
      minSize: 1
      maxSize: 5
  addons:
    - name: vpc-cni
    - name: kube-proxy
    - name: coredns
```

### Cluster Operations

#### Backup and Restore
```bash
# Configure automated backups
cat <<EOF | kubectl apply -f -
apiVersion: resources.cattle.io/v1
kind: Backup
metadata:
  name: daily-backup
spec:
  clusterName: production-cluster
  schedule: "0 2 * * *"
  retentionCount: 7
  storageLocation:
    s3:
      endpoint: s3.amazonaws.com
      bucketName: rancher-backups
      region: us-west-2
EOF

# Manual backup
kubectl create backup manual-backup-$(date +%Y%m%d)

# Restore from backup
kubectl create restore --from-backup daily-backup-20240115
```

#### Cluster Upgrades
```bash
# Check available versions
rancher clusters list-versions

# Upgrade cluster
rancher clusters upgrade production-cluster \
  --kubernetes-version v1.28.6-rancher1

# Rolling upgrade configuration
cat <<EOF > upgrade-strategy.yaml
apiVersion: rke.cattle.io/v1
kind: ClusterUpgrade
spec:
  strategy:
    maxUnavailable: 1
    drain:
      enabled: true
      timeout: 300
      gracePeriod: 30
EOF
```

### Multi-Cluster Management

#### Fleet GitOps
```yaml
# fleet.yaml - Multi-cluster deployment
defaultNamespace: production
helm:
  chart: ./charts/app
  releaseName: my-app
  values:
    replicas: 3

targetCustomizations:
  - name: staging
    clusterSelector:
      matchLabels:
        env: staging
    helm:
      values:
        replicas: 1
  
  - name: edge
    clusterSelector:
      matchLabels:
        location: edge
    helm:
      values:
        resources:
          limits:
            memory: 512Mi
```

#### Global DNS
```yaml
apiVersion: externaldns.cattle.io/v1beta1
kind: GlobalDNS
metadata:
  name: production-app
spec:
  hostname: app.example.com
  endpoints:
    - clusterName: us-west-cluster
      weight: 50
    - clusterName: us-east-cluster
      weight: 50
  healthCheck:
    port: 443
    protocol: HTTPS
    path: /health
```

## Security

### RBAC Configuration
```yaml
# Cluster Role Template
apiVersion: management.cattle.io/v3
kind: ClusterRoleTemplate
metadata:
  name: developer-role
spec:
  displayName: "Developer"
  rules:
    - apiGroups: [""]
      resources: ["pods", "services"]
      verbs: ["get", "list", "watch"]
    - apiGroups: ["apps"]
      resources: ["deployments", "replicasets"]
      verbs: ["get", "list", "watch", "create", "update"]
```

### Authentication Providers
```bash
# Configure Active Directory
rancher settings set auth-provider-ldap-enabled true
rancher auth providers ldap configure \
  --server ldap://ad.example.com:389 \
  --service-account-dn "CN=rancher,CN=Users,DC=example,DC=com" \
  --user-search-base "DC=example,DC=com" \
  --group-search-base "DC=example,DC=com"

# Configure SAML/Okta
cat <<EOF | kubectl apply -f -
apiVersion: management.cattle.io/v3
kind: AuthConfig
metadata:
  name: okta-saml
spec:
  type: saml
  enabled: true
  displayNameField: email
  userNameField: email
  idpMetadataContent: |
    <EntityDescriptor>...</EntityDescriptor>
EOF
```

### Network Policies
```yaml
# Project-level network isolation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: project-isolation
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              field.cattle.io/projectId: "p-12345"
```

## Monitoring and Observability

### Rancher Monitoring
```bash
# Install monitoring stack
helm install rancher-monitoring rancher-charts/rancher-monitoring \
  --namespace cattle-monitoring-system \
  --create-namespace \
  --set prometheus.retention=30d \
  --set grafana.persistence.enabled=true \
  --set grafana.persistence.size=10Gi
```

### Custom Dashboards
```yaml
# Grafana ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-overview-dashboard
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "Cluster Overview",
        "panels": [
          {
            "title": "Node Status",
            "targets": [{
              "expr": "up{job='node-exporter'}"
            }]
          },
          {
            "title": "Pod Count by Namespace",
            "targets": [{
              "expr": "count by(namespace) (kube_pod_info)"
            }]
          }
        ]
      }
    }
```

### Logging Integration
```yaml
# ClusterOutput for Elasticsearch
apiVersion: logging.banzaicloud.io/v1beta1
kind: ClusterOutput
metadata:
  name: elasticsearch-output
spec:
  elasticsearch:
    host: elasticsearch.example.com
    port: 9200
    index_name: rancher-${cluster_name}
    type_name: _doc
    buffer:
      timekey: 1h
      timekey_wait: 10m
```

## Use Cases

### Multi-Cloud Kubernetes
```yaml
# Deployment across multiple clouds
apiVersion: fleet.cattle.io/v1alpha1
kind: GitRepo
metadata:
  name: multi-cloud-app
spec:
  repo: https://github.com/company/app
  branch: main
  paths:
    - overlays/aws
    - overlays/azure
    - overlays/gcp
  targets:
    - name: aws-clusters
      clusterSelector:
        matchLabels:
          provider: aws
    - name: azure-clusters
      clusterSelector:
        matchLabels:
          provider: azure
```

### Edge Computing
```yaml
# K3s edge cluster registration
apiVersion: provisioning.cattle.io/v1
kind: Cluster
metadata:
  name: edge-store-001
spec:
  kubernetesVersion: v1.28.5+k3s1
  rkeConfig:
    machineGlobalConfig:
      cluster-cidr: 10.42.0.0/16
      service-cidr: 10.43.0.0/16
    registries:
      configs:
        registry.example.com:
          authConfigSecretName: registry-auth
```

### CI/CD Integration
```groovy
// Jenkins Pipeline
pipeline {
    agent any
    stages {
        stage('Deploy to Rancher') {
            steps {
                script {
                    sh '''
                        rancher login $RANCHER_URL \
                          --token $RANCHER_TOKEN
                        
                        rancher kubectl apply \
                          --cluster production \
                          -f k8s/deployment.yaml
                    '''
                }
            }
        }
    }
}
```

## Production Considerations

### High Availability
```yaml
# Production HA Requirements
production_requirements:
  rancher_server:
    nodes: 3  # Odd number for etcd quorum
    resources:
      cpu: 4
      memory: 8Gi
      storage: 100Gi  # SSD recommended
  
  load_balancer:
    type: Layer 4
    health_checks:
      interval: 10s
      timeout: 5s
      unhealthy_threshold: 3
  
  database:
    type: external
    backup:
      enabled: true
      schedule: "*/6 * * * *"
```

### Disaster Recovery
```bash
# Backup strategy
#!/bin/bash
# rancher-backup.sh

# Backup Rancher data
kubectl create backup rancher-backup-$(date +%Y%m%d-%H%M%S) \
  --namespace cattle-system

# Backup cluster states
for cluster in $(rancher clusters list -q); do
  rancher clusters backup $cluster \
    --output /backups/clusters/$cluster-$(date +%Y%m%d).yaml
done

# Sync to offsite storage
aws s3 sync /backups/ s3://disaster-recovery/rancher/
```

### Performance Tuning
```yaml
# Rancher server tuning
apiVersion: v1
kind: ConfigMap
metadata:
  name: rancher-performance
data:
  rancher-performance.conf: |
    # API Server
    audit-log-maxage: 30
    audit-log-maxbackup: 10
    audit-log-maxsize: 100
    
    # Controller
    concurrent-cluster-sync: 20
    cluster-sync-interval: 30s
    
    # Webhook
    webhook-timeout: 30s
    webhook-retry: 3
```

### Security Hardening
```bash
# CIS Benchmark scan
rancher security scan --cluster production \
  --benchmark cis-1.7 \
  --output-format json > cis-report.json

# Pod Security Standards
kubectl label namespace production \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted
```

### Cost Optimization
```yaml
# Resource quotas per project
apiVersion: v1
kind: ResourceQuota
metadata:
  name: project-quota
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    persistentvolumeclaims: "10"
    services.loadbalancers: "2"
```

## Troubleshooting

### Common Issues
```bash
# Check Rancher logs
kubectl logs -n cattle-system -l app=rancher --tail=100

# Debug cluster agent
kubectl get cluster.management.cattle.io -o yaml
kubectl logs -n cattle-system deployment/cattle-cluster-agent

# Reset admin password
kubectl -n cattle-system exec $(kubectl -n cattle-system get pods -l app=rancher -o name | head -1) -- reset-password
```

### Health Checks
```bash
# Cluster health
curl -k https://rancher.example.com/v3/clusters/c-12345/health

# Component status
kubectl get componentstatuses
kubectl get nodes -o wide
kubectl get pods --all-namespaces | grep -v Running
```

## Best Practices

1. **Cluster Lifecycle**
   - Use GitOps for cluster configurations
   - Implement automated backups
   - Test disaster recovery procedures
   - Monitor cluster health metrics

2. **Security**
   - Enable RBAC and PSPs/PSAs
   - Use external authentication
   - Implement network policies
   - Regular security scans

3. **Operations**
   - Centralize logging and monitoring
   - Automate certificate rotation
   - Plan maintenance windows
   - Document runbooks

4. **Multi-tenancy**
   - Use projects for isolation
   - Implement resource quotas
   - Configure network policies
   - Audit access logs