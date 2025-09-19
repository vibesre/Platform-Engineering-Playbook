# kind (Kubernetes in Docker)

## Overview

kind (Kubernetes IN Docker) is a tool for running local Kubernetes clusters using Docker container "nodes". It was primarily designed for testing Kubernetes itself, but may be used for local development or CI.

## Architecture

### Design Principles
```yaml
kind_architecture:
  core_concepts:
    - Kubernetes nodes as Docker containers
    - kubeadm for cluster bootstrapping
    - Containerd as container runtime
    - Single binary tool
  
  use_cases:
    - Kubernetes development/testing
    - CI/CD pipelines
    - Local development
    - Learning Kubernetes
    
  components:
    - kind CLI tool
    - Node images (kindest/node)
    - kubeadm configuration
    - Container networking
```

### Architecture Overview
```
┌─────────────────────────────────────┐
│         Docker Host                 │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │   kind Control Plane Node   │   │
│  │  ┌─────────┐ ┌──────────┐  │   │
│  │  │ etcd    │ │ API      │  │   │
│  │  └─────────┘ │ Server   │  │   │
│  │  ┌─────────┐ └──────────┘  │   │
│  │  │Scheduler│ ┌──────────┐  │   │
│  │  └─────────┘ │Controller│  │   │
│  │              │ Manager  │  │   │
│  │              └──────────┘  │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────┐ ┌─────────────┐   │
│  │ Worker Node │ │ Worker Node │   │
│  │   kubelet   │ │   kubelet   │   │
│  │   containerd│ │   containerd│   │
│  └─────────────┘ └─────────────┘   │
└─────────────────────────────────────┘
```

### Node Image Structure
```dockerfile
# kindest/node base image structure
FROM ubuntu:22.04

# Install systemd and container runtime
RUN apt-get update && apt-get install -y \
    systemd \
    systemd-sysv \
    containerd \
    kubernetes-cni

# Install Kubernetes components
ADD kubelet kubeadm kubectl /usr/bin/
ADD kubernetes-manifests /etc/kubernetes/

# Configure containerd
ADD containerd-config.toml /etc/containerd/config.toml

# Entry point
ENTRYPOINT ["/sbin/init"]
```

## Installation

### Installing kind
```bash
# Using Go
go install sigs.k8s.io/kind@v0.20.0

# macOS with Homebrew
brew install kind

# Linux binary
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Windows with Chocolatey
choco install kind

# Verify installation
kind version
```

### Prerequisites
```bash
# Docker installation check
docker version

# Recommended Docker settings
cat <<EOF > ~/.docker/daemon.json
{
  "storage-driver": "overlay2",
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  }
}
EOF

# Resource recommendations
# Minimum: 2 CPUs, 2GB RAM
# Recommended: 4 CPUs, 8GB RAM for multi-node clusters
```

## Cluster Creation

### Basic Cluster Creation
```bash
# Create a cluster with default settings
kind create cluster

# Create named cluster
kind create cluster --name development

# Create cluster with specific Kubernetes version
kind create cluster --image kindest/node:v1.28.0

# List clusters
kind get clusters

# Get cluster info
kubectl cluster-info --context kind-development
```

### Multi-Node Clusters
```yaml
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: multi-node
nodes:
- role: control-plane
- role: worker
- role: worker
- role: worker
```

```bash
# Create multi-node cluster
kind create cluster --config kind-config.yaml
```

### HA Control Plane
```yaml
# ha-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: ha-cluster
nodes:
- role: control-plane
- role: control-plane
- role: control-plane
- role: worker
- role: worker
- role: worker

# Load balancer for HA
networking:
  apiServerAddress: "127.0.0.1"
  apiServerPort: 6443
```

### Advanced Configuration
```yaml
# advanced-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: advanced
nodes:
- role: control-plane
  # Node labels
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  # Port mappings
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
  # Mount local directories
  extraMounts:
  - hostPath: /path/to/my-app
    containerPath: /app
- role: worker
  extraMounts:
  - hostPath: /tmp/data
    containerPath: /data

# Cluster networking
networking:
  podSubnet: "10.244.0.0/16"
  serviceSubnet: "10.96.0.0/12"
  disableDefaultCNI: false
  kubeProxyMode: "iptables"

# Feature gates
featureGates:
  EphemeralContainers: true
  ServerSideApply: true

# Runtime configuration
containerdConfigPatches:
- |-
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."localhost:5000"]
    endpoint = ["http://kind-registry:5000"]
```

## Development Workflows

### Local Registry
```bash
# Create registry container
docker run -d --restart=always -p "127.0.0.1:5000:5000" --name kind-registry registry:2

# Create cluster with registry
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
containerdConfigPatches:
- |-
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."localhost:5000"]
    endpoint = ["http://kind-registry:5000"]
nodes:
- role: control-plane
EOF

# Connect registry to cluster network
docker network connect "kind" kind-registry

# Document registry
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-registry-hosting
  namespace: kube-public
data:
  localRegistryHosting.v1: |
    host: "localhost:5000"
    help: "https://kind.sigs.k8s.io/docs/user/local-registry/"
EOF
```

### Loading Images
```bash
# Build and load image
docker build -t my-app:latest .
kind load docker-image my-app:latest

# Load to specific cluster
kind load docker-image my-app:latest --name development

# Load from archive
docker save my-app:latest -o my-app.tar
kind load image-archive my-app.tar

# Verify image is loaded
docker exec -it kind-control-plane crictl images
```

### Ingress Setup
```bash
# Deploy NGINX Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Wait for ingress to be ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

# Create ingress resource
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
spec:
  rules:
  - host: app.local
    http:
      paths:
      - pathType: Prefix
        path: /
        backend:
          service:
            name: app-service
            port:
              number: 80
EOF
```

### Volume Mounts
```yaml
# Development configuration with mounts
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraMounts:
  # Mount source code
  - hostPath: ./src
    containerPath: /workspace
  # Mount config files
  - hostPath: ./config
    containerPath: /etc/app-config
    readOnly: true
  # Mount for persistent data
  - hostPath: ./data
    containerPath: /var/lib/app-data
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/kind-test.yaml
name: Kind Tests
on: [push, pull_request]

jobs:
  kind-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Create kind cluster
      uses: helm/kind-action@v1.8.0
      with:
        cluster_name: kind
        config: .github/kind-config.yaml
        node_image: kindest/node:v1.28.0
        kubectl_version: v1.28.0
    
    - name: Test cluster
      run: |
        kubectl cluster-info
        kubectl get nodes
        kubectl get pods -A
    
    - name: Load images
      run: |
        docker build -t myapp:test .
        kind load docker-image myapp:test
    
    - name: Deploy application
      run: |
        kubectl apply -f manifests/
        kubectl wait --for=condition=ready pod -l app=myapp --timeout=300s
    
    - name: Run tests
      run: |
        kubectl run tests --image=myapp:test --rm -it --restart=Never -- pytest
    
    - name: Get logs on failure
      if: failure()
      run: |
        kubectl get events --all-namespaces
        kubectl get pods --all-namespaces
        kubectl logs -l app=myapp --all-containers
```

### GitLab CI
```yaml
# .gitlab-ci.yml
stages:
  - test
  - integration

variables:
  DOCKER_DRIVER: overlay2
  KIND_VERSION: v0.20.0
  KUBECTL_VERSION: v1.28.0

.kind_template:
  image: docker:24-dind
  services:
    - docker:24-dind
  before_script:
    # Install kind and kubectl
    - wget -O kind https://kind.sigs.k8s.io/dl/${KIND_VERSION}/kind-linux-amd64
    - chmod +x kind
    - mv kind /usr/local/bin/
    - wget -O kubectl https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl
    - chmod +x kubectl
    - mv kubectl /usr/local/bin/
    # Create cluster
    - kind create cluster --config=.gitlab/kind-config.yaml
    - kubectl cluster-info

unit-tests:
  extends: .kind_template
  stage: test
  script:
    - docker build -t app:test .
    - kind load docker-image app:test
    - kubectl apply -f tests/unit/
    - kubectl wait --for=condition=complete job/unit-tests --timeout=300s

integration-tests:
  extends: .kind_template
  stage: integration
  script:
    - docker build -t app:test .
    - kind load docker-image app:test
    - kubectl apply -f manifests/
    - kubectl wait --for=condition=ready pod -l app=myapp --timeout=300s
    - kubectl apply -f tests/integration/
    - kubectl wait --for=condition=complete job/integration-tests --timeout=600s
```

### Jenkins Pipeline
```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:24-dind
    securityContext:
      privileged: true
    volumeMounts:
    - name: docker-sock
      mountPath: /var/run
  volumes:
  - name: docker-sock
    emptyDir: {}
'''
        }
    }
    
    stages {
        stage('Setup Kind') {
            steps {
                container('docker') {
                    sh '''
                        # Install kind
                        wget -O kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
                        chmod +x kind
                        mv kind /usr/local/bin/
                        
                        # Install kubectl
                        wget -O kubectl https://dl.k8s.io/release/v1.28.0/bin/linux/amd64/kubectl
                        chmod +x kubectl
                        mv kubectl /usr/local/bin/
                        
                        # Create cluster
                        kind create cluster --name test-cluster
                    '''
                }
            }
        }
        
        stage('Build and Test') {
            steps {
                container('docker') {
                    sh '''
                        # Build application
                        docker build -t myapp:${BUILD_ID} .
                        
                        # Load to kind
                        kind load docker-image myapp:${BUILD_ID} --name test-cluster
                        
                        # Deploy and test
                        kubectl apply -f k8s/
                        kubectl set image deployment/myapp myapp=myapp:${BUILD_ID}
                        kubectl wait --for=condition=available deployment/myapp
                        
                        # Run tests
                        kubectl run test-${BUILD_ID} \
                            --image=myapp:${BUILD_ID} \
                            --rm -it --restart=Never \
                            -- make test
                    '''
                }
            }
        }
        
        stage('Cleanup') {
            always {
                container('docker') {
                    sh 'kind delete cluster --name test-cluster || true'
                }
            }
        }
    }
}
```

## Testing Scenarios

### Kubernetes Conformance Tests
```bash
# Download sonobuoy
wget https://github.com/vmware-tanzu/sonobuoy/releases/download/v0.57.1/sonobuoy_0.57.1_linux_amd64.tar.gz
tar -xzf sonobuoy_0.57.1_linux_amd64.tar.gz

# Run conformance tests
./sonobuoy run --mode=certified-conformance

# Check status
./sonobuoy status

# Retrieve results
./sonobuoy retrieve .
```

### Chaos Engineering
```yaml
# chaos-mesh installation
apiVersion: v1
kind: Namespace
metadata:
  name: chaos-testing

---
# Network chaos example
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay
  namespace: chaos-testing
spec:
  action: delay
  mode: all
  selector:
    namespaces:
      - default
    labelSelectors:
      app: web
  delay:
    latency: "100ms"
    jitter: "10ms"
  duration: "5m"
```

### Load Testing
```yaml
# k6 load test job
apiVersion: batch/v1
kind: Job
metadata:
  name: k6-load-test
spec:
  template:
    spec:
      containers:
      - name: k6
        image: grafana/k6:latest
        command: ["k6", "run", "/scripts/test.js"]
        volumeMounts:
        - name: test-script
          mountPath: /scripts
      volumes:
      - name: test-script
        configMap:
          name: k6-test
      restartPolicy: Never

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: k6-test
data:
  test.js: |
    import http from 'k6/http';
    import { sleep } from 'k6';
    
    export let options = {
      stages: [
        { duration: '30s', target: 20 },
        { duration: '1m', target: 100 },
        { duration: '30s', target: 0 },
      ],
    };
    
    export default function() {
      http.get('http://app-service');
      sleep(1);
    }
```

## Production Considerations

### Resource Management
```yaml
# Resource-conscious configuration
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  # Limit resources for nodes
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        # Memory management
        eviction-hard: "memory.available<100Mi"
        eviction-soft: "memory.available<200Mi"
        eviction-soft-grace-period: "memory.available=2m"
        # CPU management
        system-reserved: "cpu=200m,memory=200Mi"
        kube-reserved: "cpu=200m,memory=200Mi"
```

### Debugging and Troubleshooting

#### Debug Configuration
```yaml
# debug-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
# Enable more verbose logging
kubeadmConfigPatches:
- |
  kind: ClusterConfiguration
  apiServer:
    extraArgs:
      v: "4"
  controllerManager:
    extraArgs:
      v: "4"
  scheduler:
    extraArgs:
      v: "4"
- |
  kind: InitConfiguration
  nodeRegistration:
    kubeletExtraArgs:
      v: "4"
```

#### Common Debugging Commands
```bash
# Get cluster logs
kind export logs --name=development /tmp/kind-logs

# Debug node issues
docker exec -it kind-control-plane bash
# Inside container:
journalctl -u kubelet
journalctl -u containerd
crictl ps
crictl logs <container-id>

# Debug networking
kubectl run debug --image=nicolaka/netshoot -it --rm
# Inside pod:
nslookup kubernetes.default
curl -k https://kubernetes.default:443/healthz

# Check kind cluster details
docker inspect kind-control-plane
docker logs kind-control-plane
```

### Performance Optimization

#### Fast Cluster Creation
```bash
# Pre-pull images
docker pull kindest/node:v1.28.0

# Create cluster with pre-pulled image
kind create cluster --image kindest/node:v1.28.0 --retain

# Reuse nodes for faster recreation
kind export kubeconfig --name old-cluster
kind delete cluster --name old-cluster --retain
kind create cluster --name new-cluster --retain
```

#### Optimized Development Workflow
```makefile
# Makefile for kind development
.PHONY: cluster create delete load deploy test clean

CLUSTER_NAME ?= dev
K8S_VERSION ?= v1.28.0
APP_IMAGE ?= myapp:latest

cluster: create load deploy

create:
	kind create cluster \
		--name $(CLUSTER_NAME) \
		--image kindest/node:$(K8S_VERSION) \
		--config kind-config.yaml

delete:
	kind delete cluster --name $(CLUSTER_NAME)

load:
	docker build -t $(APP_IMAGE) .
	kind load docker-image $(APP_IMAGE) --name $(CLUSTER_NAME)

deploy:
	kubectl apply -f manifests/
	kubectl wait --for=condition=ready pod -l app=myapp --timeout=300s

test:
	kubectl run test --image=$(APP_IMAGE) --rm -it --restart=Never -- make test

clean: delete
	docker rmi $(APP_IMAGE) || true
```

## Advanced Features

### Multi-Architecture Support
```bash
# Create ARM64 cluster on Apple Silicon
kind create cluster --image kindest/node:v1.28.0@sha256:arm64-hash

# Build multi-arch images
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

### Custom Node Images
```dockerfile
# Dockerfile for custom node image
FROM kindest/node:v1.28.0

# Add custom tools
RUN apt-get update && apt-get install -y \
    vim \
    curl \
    htop \
    net-tools

# Add custom configurations
COPY custom-config /etc/kubernetes/

# Add custom binaries
COPY --from=builder /app/my-controller /usr/local/bin/
```

```bash
# Build and use custom image
docker build -t my-kind-node:latest .
kind create cluster --image my-kind-node:latest
```

### Cluster Templating
```bash
#!/bin/bash
# kind-cluster-template.sh

CLUSTER_TYPE=${1:-dev}
CLUSTER_NAME=${2:-$CLUSTER_TYPE-cluster}

case $CLUSTER_TYPE in
  dev)
    cat <<EOF | kind create cluster --name $CLUSTER_NAME --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
  - containerPort: 443
    hostPort: 443
EOF
    ;;
  
  test)
    cat <<EOF | kind create cluster --name $CLUSTER_NAME --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
networking:
  podSubnet: "10.244.0.0/16"
EOF
    ;;
  
  ha)
    cat <<EOF | kind create cluster --name $CLUSTER_NAME --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: control-plane
- role: control-plane
- role: worker
- role: worker
EOF
    ;;
esac

echo "Cluster $CLUSTER_NAME created with $CLUSTER_TYPE configuration"
```

## Best Practices

1. **Development Workflow**
   - Use Makefiles or scripts for repeatability
   - Pre-load commonly used images
   - Mount source code for live development
   - Use local registries for faster builds

2. **Testing**
   - Isolate tests in separate namespaces
   - Clean up resources after tests
   - Use resource limits
   - Implement proper health checks

3. **CI/CD**
   - Cache kind binary and node images
   - Use specific versions (not latest)
   - Export logs on failure
   - Clean up clusters after use

4. **Performance**
   - Limit node resources appropriately
   - Use SSD storage when possible
   - Pre-pull images
   - Optimize Docker daemon settings