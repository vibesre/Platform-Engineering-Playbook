# Podman - Daemonless Container Engine

<GitHubButtons />
## Overview

Podman (Pod Manager) is a daemonless, open-source container engine designed to develop, manage, and run containers on Linux systems. Developed by Red Hat, Podman provides a Docker-compatible command line interface while offering unique features like rootless containers and systemd integration without requiring a central daemon.

## Architecture

### Daemonless Design

```
┌─────────────────────────────────────────────────────┐
│                   Podman CLI                        │
├─────────────────────────────────────────────────────┤
│                   libpod API                        │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────┐  ┌───────────────┐ │
│  │  Container   │  │   Image   │  │    Network    │ │
│  │  Runtime     │  │   Store   │  │   Management  │ │
│  │  (crun/runc) │  │           │  │   (CNI/Netavark)│ │
│  └─────────────┘  └──────────┘  └───────────────┘ │
├─────────────────────────────────────────────────────┤
│              Storage Backend (overlay)              │
├─────────────────────────────────────────────────────┤
│                 Linux Kernel                        │
│      (namespaces, cgroups, seccomp, SELinux)      │
└─────────────────────────────────────────────────────┘
```

### Key Differences from Docker

- **No Daemon**: Each Podman command runs in its own process
- **Rootless by Default**: Can run containers without root privileges
- **Pod Support**: Native support for Kubernetes-style pods
- **Systemd Integration**: Can generate systemd unit files for containers
- **Docker Compatibility**: Drop-in replacement for most Docker commands

## Installation and Configuration

### Installing Podman

#### Fedora/RHEL/CentOS
```bash
# RHEL 8/CentOS 8/Fedora
sudo dnf install podman

# RHEL 7/CentOS 7
sudo yum install podman
```

#### Ubuntu/Debian
```bash
# Ubuntu 20.04 and later
sudo apt update
sudo apt install podman

# For newer versions from Kubic repository
echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_$(lsb_release -rs)/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
curl -L "https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_$(lsb_release -rs)/Release.key" | sudo apt-key add -
sudo apt update
sudo apt install podman
```

#### macOS
```bash
# Using Homebrew
brew install podman

# Initialize and start Podman machine
podman machine init
podman machine start
```

### Configuration Files

#### System Configuration
```bash
# /etc/containers/registries.conf
unqualified-search-registries = ["docker.io", "quay.io"]

[[registry]]
location = "docker.io"
insecure = false
blocked = false

[[registry.mirror]]
location = "mirror.gcr.io"

# /etc/containers/storage.conf
[storage]
driver = "overlay"
runroot = "/run/containers/storage"
graphroot = "/var/lib/containers/storage"

[storage.options]
size = "10G"
override_kernel_check = "true"
```

#### User Configuration (Rootless)
```bash
# ~/.config/containers/containers.conf
[containers]
userns = "auto"
cgroups = "enabled"
cgroupns = "private"
default_sysctls = [
  "net.ipv4.ping_group_range=0 0",
]

[network]
default_subnet = "10.88.0.0/16"

[engine]
runtime = "crun"
stop_timeout = 10
```

## Rootless Containers

### Setting Up Rootless Podman

#### 1. Enable User Namespaces
```bash
# Check if user namespaces are enabled
sysctl user.max_user_namespaces

# Enable if needed
echo "user.max_user_namespaces=28633" | sudo tee /etc/sysctl.d/99-rootless.conf
sudo sysctl -p /etc/sysctl.d/99-rootless.conf
```

#### 2. Configure subuid and subgid
```bash
# Check current mappings
grep $USER /etc/subuid /etc/subgid

# Add if missing
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER

# Verify
podman unshare cat /proc/self/uid_map
```

#### 3. Configure Storage
```bash
# Reset storage for rootless
podman system reset

# Configure storage location
mkdir -p ~/.config/containers
cat > ~/.config/containers/storage.conf <<EOF
[storage]
driver = "overlay"
runroot = "/run/user/$(id -u)/containers"
graphroot = "$HOME/.local/share/containers/storage"

[storage.options.overlay]
mount_program = "/usr/bin/fuse-overlayfs"
EOF
```

### Rootless Networking

#### Using slirp4netns (default)
```bash
# Run container with port mapping
podman run -d -p 8080:80 nginx

# Check network configuration
podman inspect nginx | jq '.[0].NetworkSettings'
```

#### Using pasta (Performance Mode)
```bash
# Install pasta
sudo dnf install passt

# Configure Podman to use pasta
podman --network-backend=pasta run -d -p 8080:80 nginx
```

## Pod Management

### Creating and Managing Pods

#### Create a Pod
```bash
# Create a new pod
podman pod create --name mypod --publish 8080:80

# Create pod with resource limits
podman pod create --name limited-pod \
  --cpus 2 \
  --memory 2g \
  --publish 8080:80,8443:443
```

#### Add Containers to Pod
```bash
# Add nginx to pod
podman run -d --pod mypod --name nginx nginx:latest

# Add application container
podman run -d --pod mypod --name app \
  -e DATABASE_URL=localhost:5432 \
  myapp:latest
```

#### Pod Operations
```bash
# List pods
podman pod ps

# Inspect pod
podman pod inspect mypod

# Stop/start pod
podman pod stop mypod
podman pod start mypod

# Remove pod and all containers
podman pod rm -f mypod
```

### Kubernetes YAML Support

#### Generate Kubernetes YAML
```bash
# Create pod from Kubernetes YAML
cat <<EOF > nginx-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
  - name: redis
    image: redis:latest
EOF

podman play kube nginx-pod.yaml
```

#### Export to Kubernetes
```bash
# Generate Kubernetes YAML from existing pod
podman generate kube mypod > mypod.yaml

# Generate with persistent volume claims
podman generate kube -s mypod > mypod-with-storage.yaml
```

## Integration with Kubernetes

### Using Podman as CRI

#### Install CRI-O for Kubernetes
```bash
# CRI-O provides Kubernetes runtime using Podman libraries
sudo dnf install cri-o

# Configure CRI-O
sudo systemctl enable --now crio
```

#### Configure Kubernetes to use Podman/CRI-O
```bash
# /var/lib/kubelet/kubeadm-flags.env
KUBELET_KUBEADM_ARGS="--container-runtime=remote --container-runtime-endpoint=unix:///var/run/crio/crio.sock"

# Initialize cluster
kubeadm init --cri-socket unix:///var/run/crio/crio.sock
```

### Building Images for Kubernetes

#### Multi-architecture Builds
```bash
# Build for multiple platforms
podman build --platform linux/amd64,linux/arm64 \
  -t myapp:latest \
  --manifest myapp:latest .

# Push manifest
podman manifest push myapp:latest docker://registry.example.com/myapp:latest
```

## Security Features

### SELinux Integration

#### Container SELinux Contexts
```bash
# Run with specific SELinux context
podman run -d \
  --security-opt label=type:svirt_apache_t \
  httpd

# Disable SELinux separation
podman run -d \
  --security-opt label=disable \
  nginx

# View SELinux labels
podman inspect nginx | jq '.[0].ProcessLabel'
```

### Seccomp Profiles

#### Custom Seccomp Profile
```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": ["accept", "bind", "clone", "close"],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

```bash
# Use custom seccomp profile
podman run --security-opt seccomp=./custom-seccomp.json nginx
```

### User Namespace Remapping

```bash
# Run with specific UID/GID mapping
podman run --uidmap 0:100000:5000 \
  --gidmap 0:100000:5000 \
  alpine id

# Auto user namespace mapping
podman run --userns=auto alpine id
```

### Capabilities Management

```bash
# Drop all capabilities and add specific ones
podman run --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  --cap-add SETUID \
  nginx

# List container capabilities
podman exec nginx capsh --print
```

## Systemd Integration

### Generate Systemd Units

#### Container as Service
```bash
# Create container
podman create --name myapp -p 8080:8080 myapp:latest

# Generate systemd unit
podman generate systemd --new --name myapp > ~/.config/systemd/user/myapp.service

# Enable and start service
systemctl --user enable --now myapp.service
```

#### Pod as Service
```bash
# Generate systemd units for entire pod
podman generate systemd --new --files --name mypod

# Move to systemd directory
mv *.service ~/.config/systemd/user/

# Enable pod service
systemctl --user enable --now pod-mypod.service
```

### Systemd in Containers

```bash
# Run systemd inside container
podman run -d --systemd=always \
  --name systemd-container \
  -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
  fedora:latest /usr/lib/systemd/systemd

# Exec into systemd container
podman exec -it systemd-container /bin/bash
```

## Performance Optimization

### Storage Driver Optimization

#### Native Overlay (Root)
```bash
# Configure native overlay
cat > /etc/containers/storage.conf <<EOF
[storage]
driver = "overlay"
runroot = "/run/containers/storage"
graphroot = "/var/lib/containers/storage"

[storage.options.overlay]
skip_mount_home = "true"
mount_program = ""  # Use kernel overlay
mountopt = "nodev,metacopy=on"
EOF
```

#### FUSE-OverlayFS (Rootless)
```bash
# Install fuse-overlayfs
sudo dnf install fuse-overlayfs

# Configure for performance
cat > ~/.config/containers/storage.conf <<EOF
[storage]
driver = "overlay"

[storage.options.overlay]
mount_program = "/usr/bin/fuse-overlayfs"
mountopt = "nodev,fsync=0,metacopy=on"
EOF
```

### Network Performance

#### Use Host Network
```bash
# Maximum network performance
podman run --network host nginx
```

#### Configure MTU
```bash
# Create network with custom MTU
podman network create --opt mtu=9000 jumbo-net

# Run container on jumbo network
podman run --network jumbo-net alpine ping -c 3 google.com
```

### Resource Limits

```bash
# CPU limits
podman run -d \
  --cpus="2.5" \
  --cpu-shares=512 \
  --cpuset-cpus="0,1" \
  nginx

# Memory limits
podman run -d \
  --memory="1g" \
  --memory-swap="2g" \
  --memory-reservation="750m" \
  nginx

# I/O limits
podman run -d \
  --device-read-bps /dev/sda:10mb \
  --device-write-bps /dev/sda:10mb \
  nginx
```

## Common Operations

### Image Management

```bash
# Search images
podman search nginx --limit 5

# Pull with specific platform
podman pull --platform linux/arm64 nginx

# List images with formatting
podman images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Build with advanced options
podman build \
  --layers \
  --cache-from registry.example.com/cache:latest \
  --build-arg VERSION=1.0 \
  -t myapp:latest .

# Push to registry
podman login registry.example.com
podman push myapp:latest registry.example.com/myapp:latest
```

### Container Operations

```bash
# Run with health check
podman run -d \
  --health-cmd='curl -f http://localhost/ || exit 1' \
  --health-interval=30s \
  --health-retries=3 \
  --health-start-period=30s \
  nginx

# Auto-remove on exit
podman run --rm -it alpine sh

# Run with init process
podman run -d --init nginx

# Export/Import containers
podman export nginx > nginx.tar
podman import nginx.tar mynginx:backup
```

### Volume Management

```bash
# Create named volume
podman volume create mydata

# Mount volume with options
podman run -d \
  -v mydata:/data:Z,U \
  -v /host/path:/container/path:ro,rslave \
  nginx

# Backup volume
podman run --rm \
  -v mydata:/source:ro \
  -v /backup:/backup \
  alpine tar czf /backup/mydata.tar.gz -C /source .
```

## Troubleshooting

### Common Issues

#### 1. Rootless Networking Issues
```bash
# Check slirp4netns
podman info | grep slirp4netns

# Enable port forwarding for rootless
echo "net.ipv4.ip_unprivileged_port_start=80" | sudo tee /etc/sysctl.d/99-rootless.conf
sudo sysctl -p /etc/sysctl.d/99-rootless.conf
```

#### 2. Storage Space Issues
```bash
# Check storage usage
podman system df

# Clean up storage
podman system prune -a --volumes

# Reset storage completely
podman system reset
```

#### 3. Permission Denied Errors
```bash
# Check user namespaces
cat /proc/sys/user/max_user_namespaces

# Verify subuid/subgid mappings
podman unshare cat /proc/self/uid_map

# Fix storage permissions
podman unshare chown -R 0:0 ~/.local/share/containers/storage
```

### Debug Commands

```bash
# Verbose output
podman --log-level debug run alpine echo hello

# Inspect container namespace
podman inspect nginx | jq '.[0].NetworkSettings.SandboxKey'

# Check cgroup configuration
podman exec nginx cat /proc/self/cgroup

# System information
podman system info
```

## Best Practices for Production

### 1. Image Security Scanning

```bash
# Install skopeo for image inspection
sudo dnf install skopeo

# Scan image before running
skopeo inspect docker://nginx:latest

# Use Clair or Trivy for vulnerability scanning
podman run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image nginx:latest
```

### 2. Container Hardening

```yaml
# podman-compose.yml with security settings
version: '3'
services:
  web:
    image: nginx:latest
    security_opt:
      - label:type:svirt_apache_t
      - no-new-privileges
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
```

### 3. Monitoring and Logging

```bash
# JSON logging
podman run -d --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  nginx

# Forward logs to syslog
podman run -d --log-driver syslog \
  --log-opt syslog-address=tcp://192.168.1.100:514 \
  nginx

# Container metrics
podman stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### 4. High Availability with Podman

```bash
#!/bin/bash
# Health check and restart script
CONTAINER_NAME="myapp"

if ! podman healthcheck run $CONTAINER_NAME; then
    echo "Container $CONTAINER_NAME is unhealthy, restarting..."
    podman restart $CONTAINER_NAME
fi

# Auto-restart with systemd
# ~/.config/systemd/user/myapp.service
[Service]
Restart=always
RestartSec=10
StartLimitInterval=400
StartLimitBurst=3
```

### 5. Backup and Disaster Recovery

```bash
#!/bin/bash
# Backup script for Podman containers and volumes

BACKUP_DIR="/backup/podman/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup all container configurations
for container in $(podman ps -aq); do
    podman inspect $container > $BACKUP_DIR/${container}_config.json
done

# Backup all volumes
for volume in $(podman volume ls -q); do
    podman run --rm -v ${volume}:/source:ro \
        -v $BACKUP_DIR:/backup \
        alpine tar czf /backup/${volume}.tar.gz -C /source .
done

# Backup images
podman save -o $BACKUP_DIR/images.tar $(podman images -q)
```

## Docker Compose Compatibility

### Using podman-compose

```bash
# Install podman-compose
pip3 install podman-compose

# Use existing docker-compose.yml
podman-compose up -d

# View logs
podman-compose logs -f

# Scale services
podman-compose up -d --scale web=3
```

### Native Podman Compose Support

```bash
# Using Podman 3.0+ native support
podman compose up

# Custom compose file
podman compose -f production.yml up
```

## Advanced Features

### Checkpoint and Restore

```bash
# Enable checkpoint/restore
sudo dnf install criu

# Checkpoint running container
podman container checkpoint myapp

# Restore container
podman container restore myapp

# Migration between hosts
podman container checkpoint myapp --export=/tmp/checkpoint.tar.gz
# On target host:
podman container restore --import=/tmp/checkpoint.tar.gz
```

### Auto-Updates

```bash
# Label container for auto-updates
podman run -d \
  --label io.containers.autoupdate=registry \
  --name myapp \
  myapp:latest

# Enable auto-update timer
systemctl --user enable --now podman-auto-update.timer

# Manual update check
podman auto-update
```

## Resources

### Official Documentation
- [Podman Documentation](https://docs.podman.io/)
- [Podman GitHub Repository](https://github.com/containers/podman)
- [Red Hat Container Tools](https://developers.redhat.com/products/container-tools)

### Tools and Ecosystem
- [Buildah - Container Image Builder](https://buildah.io/)
- [Skopeo - Container Image Operations](https://github.com/containers/skopeo)
- [podman-compose](https://github.com/containers/podman-compose)

### Community Resources
- [Podman Mailing List](https://lists.podman.io/archives/)
- [Podman IRC Channel](https://web.libera.chat/#podman)
- [Reddit r/podman](https://www.reddit.com/r/podman/)

### Learning Resources
- [Podman Tutorial](https://github.com/containers/podman/blob/main/docs/tutorials/podman_tutorial.md)
- [Podman for Docker Users](https://developers.redhat.com/blog/2019/02/21/podman-and-buildah-for-docker-users)
- [Rootless Containers with Podman](https://www.redhat.com/sysadmin/rootless-podman)

### Enterprise Resources
- [Red Hat Enterprise Linux Container Tools](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/building_running_and_managing_containers/index)
- [OpenShift and Podman Integration](https://docs.openshift.com/container-platform/latest/nodes/containers/nodes-containers-using.html)