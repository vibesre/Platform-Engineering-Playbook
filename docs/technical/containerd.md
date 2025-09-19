# containerd - Industry-Standard Container Runtime

## Overview

containerd is an industry-standard container runtime that provides a reliable and high-performance foundation for container platforms. Originally developed by Docker Inc. and donated to the Cloud Native Computing Foundation (CNCF), containerd focuses on simplicity, robustness, and portability.

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────┐
│                   Client (ctr, nerdctl)             │
├─────────────────────────────────────────────────────┤
│                   containerd API                     │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────┐  ┌───────────────┐ │
│  │   Content    │  │ Snapshots│  │    Runtime    │ │
│  │   Store      │  │          │  │   (shim API)  │ │
│  └─────────────┘  └──────────┘  └───────────────┘ │
├─────────────────────────────────────────────────────┤
│                    Metadata Store                    │
├─────────────────────────────────────────────────────┤
│              OS (Linux, Windows, etc.)              │
└─────────────────────────────────────────────────────┘
```

### Key Features

- **OCI Compliance**: Full support for OCI runtime and image specifications
- **Snapshots**: Advanced snapshot management for efficient container filesystems
- **Content Store**: Deduplicated content storage for images and layers
- **Runtime Plugins**: Support for multiple runtime implementations (runc, kata, gVisor)
- **Namespace Isolation**: Multi-tenancy support through namespaces

## Installation and Configuration

### Installing containerd

#### Ubuntu/Debian
```bash
# Add Docker's official GPG key
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install containerd
sudo apt-get update
sudo apt-get install containerd.io
```

#### RHEL/CentOS
```bash
# Install required packages
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

# Add repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install containerd
sudo yum install containerd.io
```

### Configuration

#### Default Configuration
```bash
# Generate default configuration
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml

# Enable containerd
sudo systemctl enable containerd
sudo systemctl start containerd
```

#### Custom Configuration Example
```toml
# /etc/containerd/config.toml
version = 2

[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
    sandbox_image = "registry.k8s.io/pause:3.9"
    
    [plugins."io.containerd.grpc.v1.cri".containerd]
      default_runtime_name = "runc"
      
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          runtime_type = "io.containerd.runc.v2"
          
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            SystemdCgroup = true
            
    [plugins."io.containerd.grpc.v1.cri".registry]
      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
          endpoint = ["https://registry-1.docker.io"]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."myregistry.io:5000"]
          endpoint = ["http://myregistry.io:5000"]
          
  [plugins."io.containerd.gc.v1.scheduler"]
    pause_threshold = 0.02
    deletion_threshold = 0
    mutation_threshold = 100
    schedule_delay = "0s"
    startup_delay = "100ms"
```

## Kubernetes Integration

### Configure Kubernetes to Use containerd

#### 1. Configure containerd for Kubernetes
```bash
# Ensure systemd cgroup driver
cat <<EOF | sudo tee /etc/containerd/config.toml
version = 2
[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
    [plugins."io.containerd.grpc.v1.cri".containerd]
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            SystemdCgroup = true
EOF

sudo systemctl restart containerd
```

#### 2. Configure kubelet
```bash
# /var/lib/kubelet/kubeadm-flags.env
KUBELET_KUBEADM_ARGS="--container-runtime=remote --container-runtime-endpoint=unix:///run/containerd/containerd.sock"
```

#### 3. Initialize Kubernetes cluster
```bash
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --cri-socket unix:///run/containerd/containerd.sock
```

### crictl Configuration
```bash
# Configure crictl to work with containerd
cat <<EOF | sudo tee /etc/crictl.yaml
runtime-endpoint: unix:///run/containerd/containerd.sock
image-endpoint: unix:///run/containerd/containerd.sock
timeout: 10
debug: false
EOF
```

## Security Features

### Rootless containerd

#### Installation
```bash
# Install rootless dependencies
sudo apt-get install -y uidmap

# Install rootless containerd
containerd-rootless-setuptool.sh install

# Add to PATH
export PATH=$HOME/bin:$PATH
```

#### Configuration
```bash
# ~/.config/containerd/config.toml
version = 2
root = "/home/user/.local/share/containerd"
state = "/run/user/1000/containerd"

[grpc]
  address = "/run/user/1000/containerd/containerd.sock"
```

### Security Policies

#### AppArmor Integration
```toml
# Runtime configuration with AppArmor
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
  SystemdCgroup = true
  # AppArmor profile
  AppArmorProfile = "containerd-default"
```

#### SELinux Support
```bash
# Enable SELinux for containerd
sudo semanage fcontext -a -t container_runtime_exec_t /usr/bin/containerd
sudo restorecon -v /usr/bin/containerd
```

### Image Verification
```toml
# Enable image signature verification
[plugins."io.containerd.grpc.v1.cri".registry]
  [plugins."io.containerd.grpc.v1.cri".registry.configs]
    [plugins."io.containerd.grpc.v1.cri".registry.configs."myregistry.io"]
      [plugins."io.containerd.grpc.v1.cri".registry.configs."myregistry.io".tls]
        ca_file = "/etc/containerd/certs/ca.crt"
        cert_file = "/etc/containerd/certs/client.crt"
        key_file = "/etc/containerd/certs/client.key"
```

## Performance Optimization

### Runtime Performance

#### 1. Optimize Snapshotter
```toml
# Use native snapshotter for better performance
[plugins."io.containerd.grpc.v1.cri".containerd]
  snapshotter = "native"
  
[plugins."io.containerd.snapshotter.v1.native"]
  root_path = "/var/lib/containerd/io.containerd.snapshotter.v1.native"
```

#### 2. Configure Runtime Options
```toml
[plugins."io.containerd.runtime.v1.linux"]
  runtime = "runc"
  runtime_root = "/run/containerd/runc"
  no_shim = false
  shim = "containerd-shim"
  shim_debug = false
```

#### 3. Garbage Collection Tuning
```toml
[plugins."io.containerd.gc.v1.scheduler"]
  pause_threshold = 0.02
  deletion_threshold = 0
  mutation_threshold = 100
  schedule_delay = "0s"
  startup_delay = "100ms"
```

### Resource Limits
```toml
# Set resource limits for containerd
[plugins."io.containerd.grpc.v1.cri".containerd.default_runtime]
  runtime_type = "io.containerd.runtime.v1.linux"
  runtime_engine = ""
  runtime_root = ""
  privileged_without_host_devices = false
  base_runtime_spec = ""
  
  [plugins."io.containerd.grpc.v1.cri".containerd.default_runtime.options]
    # CPU quota
    CpuQuota = 100000
    # Memory limit
    MemoryLimit = 2147483648
```

## Common Operations

### Container Management

#### Using ctr (containerd CLI)
```bash
# Pull an image
sudo ctr images pull docker.io/library/nginx:latest

# List images
sudo ctr images ls

# Run a container
sudo ctr run -d docker.io/library/nginx:latest nginx-test

# List containers
sudo ctr containers ls

# Execute command in container
sudo ctr task exec -t --exec-id bash-1 nginx-test bash

# Stop container
sudo ctr task kill nginx-test

# Remove container
sudo ctr containers rm nginx-test
```

#### Using nerdctl (Docker-compatible CLI)
```bash
# Install nerdctl
wget https://github.com/containerd/nerdctl/releases/download/v1.7.0/nerdctl-1.7.0-linux-amd64.tar.gz
sudo tar Cxzvf /usr/local/bin nerdctl-1.7.0-linux-amd64.tar.gz

# Docker-like commands
nerdctl pull nginx
nerdctl run -d --name nginx -p 80:80 nginx
nerdctl ps
nerdctl exec -it nginx bash
nerdctl stop nginx
nerdctl rm nginx
```

### Namespace Management
```bash
# List namespaces
sudo ctr namespaces ls

# Create namespace
sudo ctr namespaces create prod

# Use specific namespace
sudo ctr -n prod images pull nginx:latest

# Remove namespace
sudo ctr namespaces rm prod
```

### Snapshot Management
```bash
# List snapshots
sudo ctr snapshots ls

# Create snapshot
sudo ctr snapshots prepare mysnapshot

# View snapshot info
sudo ctr snapshots info mysnapshot

# Remove snapshot
sudo ctr snapshots rm mysnapshot
```

## Troubleshooting

### Common Issues and Solutions

#### 1. containerd.sock Permission Denied
```bash
# Check socket permissions
ls -la /run/containerd/containerd.sock

# Add user to docker group (if exists)
sudo usermod -aG docker $USER

# Or adjust permissions
sudo chmod 666 /run/containerd/containerd.sock
```

#### 2. Failed to Start Container
```bash
# Check containerd logs
sudo journalctl -u containerd -f

# Verify runtime configuration
sudo ctr plugins ls

# Check available runtimes
sudo ctr runtime ls
```

#### 3. Image Pull Failures
```bash
# Test connectivity
sudo ctr images pull --debug docker.io/library/hello-world:latest

# Check registry configuration
cat /etc/containerd/config.toml | grep -A 10 registry

# Verify DNS resolution
nslookup registry-1.docker.io
```

### Debugging Tools

#### Enable Debug Logging
```toml
# /etc/containerd/config.toml
[debug]
  level = "debug"
  format = "json"
  address = "/run/containerd/debug.sock"
```

#### Metrics Collection
```bash
# Enable metrics endpoint
[metrics]
  address = "127.0.0.1:1338"
  grpc_histogram = false

# Query metrics
curl http://localhost:1338/v1/metrics
```

## Best Practices for Production

### 1. High Availability Configuration
```toml
# Configure for HA
[plugins."io.containerd.grpc.v1.cri"]
  max_container_log_line_size = 16384
  max_concurrent_downloads = 5
  
[plugins."io.containerd.grpc.v1.cri".containerd]
  snapshotter = "overlayfs"
  default_runtime_name = "runc"
  disable_snapshot_annotations = false
```

### 2. Monitoring and Alerting
```yaml
# Prometheus configuration
- job_name: 'containerd'
  static_configs:
    - targets: ['localhost:1338']
  metric_relabel_configs:
    - source_labels: [__name__]
      regex: 'container_.*'
      action: keep
```

### 3. Backup and Recovery
```bash
#!/bin/bash
# Backup containerd data
BACKUP_DIR="/backup/containerd/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup images
sudo ctr images export $BACKUP_DIR/images.tar $(sudo ctr images ls -q)

# Backup configuration
sudo cp -r /etc/containerd $BACKUP_DIR/
sudo cp -r /var/lib/containerd $BACKUP_DIR/
```

### 4. Security Hardening
```toml
# Restrict runtime capabilities
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
  SystemdCgroup = true
  # Drop all capabilities by default
  cap_drop = ["ALL"]
  # Add only required capabilities
  cap_add = ["NET_BIND_SERVICE", "SYS_TIME"]
```

### 5. Resource Management
```bash
# Set system limits
cat <<EOF | sudo tee /etc/systemd/system/containerd.service.d/limits.conf
[Service]
LimitNOFILE=1048576
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity
Delegate=yes
EOF

sudo systemctl daemon-reload
sudo systemctl restart containerd
```

## Migration from Docker

### Docker to containerd Migration Steps

1. **Export Docker Images**
```bash
# Save Docker images
docker save -o images.tar $(docker images -q)

# Import to containerd
sudo ctr images import images.tar
```

2. **Convert Docker Compose**
```bash
# Use nerdctl compose
nerdctl compose -f docker-compose.yml up
```

3. **Update Scripts**
```bash
# Replace Docker commands
# docker run → nerdctl run
# docker ps → nerdctl ps
# docker exec → nerdctl exec
```

## Resources

### Official Documentation
- [containerd Documentation](https://containerd.io/docs/)
- [containerd GitHub Repository](https://github.com/containerd/containerd)
- [containerd API Documentation](https://github.com/containerd/containerd/blob/main/api/README.md)

### Tools and Utilities
- [nerdctl - Docker-compatible CLI](https://github.com/containerd/nerdctl)
- [ctr - containerd CLI](https://github.com/containerd/containerd/tree/main/cmd/ctr)
- [crictl - CRI-compatible CLI](https://github.com/kubernetes-sigs/cri-tools)

### Community Resources
- [CNCF containerd Project](https://www.cncf.io/projects/containerd/)
- [containerd Slack Channel](https://cloud-native.slack.com/messages/containerd)
- [Stack Overflow containerd Tag](https://stackoverflow.com/questions/tagged/containerd)

### Learning Resources
- [containerd: An Introduction](https://www.docker.com/blog/containerd-ga-features-2/)
- [Deep Dive into containerd](https://iximiuz.com/en/posts/containerd-command-line-clients/)
- [containerd vs Docker: Understanding the Differences](https://phoenixnap.com/kb/docker-vs-containerd)

### Performance and Benchmarking
- [containerd Performance Tuning Guide](https://github.com/containerd/containerd/blob/main/docs/ops.md)
- [Container Runtime Benchmark](https://github.com/containers/crun/blob/main/docs/performance.md)