---
title: Proxmox VE (Virtual Environment)
description: Master open source virtualization with Proxmox for platform engineering
---

# Proxmox Virtual Environment

Proxmox VE is a complete open source platform for enterprise virtualization. It integrates KVM hypervisor and LXC containers, software-defined storage and networking, high-availability clustering, and built-in backup/restore in a single platform.

## 🎯 Key Features

### Core Components
- **KVM Virtualization** - Full virtualization with hardware acceleration
- **LXC Containers** - Lightweight Linux containers
- **Proxmox Cluster** - High-availability multi-node clusters
- **Storage Options** - Local, shared, distributed storage support
- **Built-in Backup** - Integrated backup and restore solution
- **Web Management** - Full-featured web-based management interface

### Why Platform Engineers Love It
- **Cost-Effective** - Enterprise features without licensing costs
- **API-First Design** - Complete REST API for automation
- **ZFS Integration** - Built-in ZFS support for storage
- **Live Migration** - Move VMs without downtime
- **Container Support** - Run both VMs and containers

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                Proxmox Cluster                  │
├─────────────────┬────────────────┬──────────────┤
│   Node 1        │    Node 2      │    Node 3    │
│                 │                │              │
│  ┌──────────┐   │  ┌──────────┐ │ ┌──────────┐ │
│  │    VM    │   │  │    VM    │ │ │   LXC    │ │
│  └──────────┘   │  └──────────┘ │ └──────────┘ │
│  ┌──────────┐   │  ┌──────────┐ │ ┌──────────┐ │
│  │   LXC    │   │  │    VM    │ │ │    VM    │ │
│  └──────────┘   │  └──────────┘ │ └──────────┘ │
│                 │                │              │
│  Storage: ZFS   │ Storage: Ceph │ Storage: NFS │
└─────────────────┴────────────────┴──────────────┘
         │              │                │
         └──────────────┴────────────────┘
                Cluster Network (Corosync)
```

## 🚀 Getting Started

### Installation

```bash
# Download Proxmox VE ISO
wget https://www.proxmox.com/en/downloads

# After installation, access web interface
https://your-server-ip:8006

# Default login: root
# Password: set during installation
```

### Basic CLI Commands

```bash
# VM Management
qm list                          # List all VMs
qm create 100                    # Create VM with ID 100
qm start 100                     # Start VM
qm stop 100                      # Stop VM
qm migrate 100 node2             # Migrate VM to node2

# Container Management
pct list                         # List all containers
pct create 200 template.tar.gz   # Create container
pct start 200                    # Start container
pct enter 200                    # Enter container

# Storage Management
pvesm status                     # Show storage status
pvesm add nfs mynfs --server 10.0.0.10 --export /export

# Cluster Management
pvecm status                     # Show cluster status
pvecm nodes                      # List cluster nodes
```

## 💻 Code Examples

### Creating a VM with Python

```python
import requests
import json

class ProxmoxAPI:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.token = None
        self.ticket = None
        
    def login(self):
        """Authenticate with Proxmox"""
        url = f"https://{self.host}:8006/api2/json/access/ticket"
        data = {
            'username': self.user,
            'password': self.password
        }
        
        response = requests.post(url, data=data, verify=False)
        result = response.json()['data']
        self.ticket = result['ticket']
        self.token = result['CSRFPreventionToken']
        
    def create_vm(self, node, vmid, name, memory=2048, cores=2):
        """Create a new VM"""
        url = f"https://{self.host}:8006/api2/json/nodes/{node}/qemu"
        
        headers = {
            'CSRFPreventionToken': self.token,
            'Cookie': f"PVEAuthCookie={self.ticket}"
        }
        
        data = {
            'vmid': vmid,
            'name': name,
            'memory': memory,
            'cores': cores,
            'sockets': 1,
            'cpu': 'host',
            'net0': 'virtio,bridge=vmbr0',
            'ide2': 'local-lvm:cloudinit',
            'bootdisk': 'scsi0',
            'ostype': 'l26',
            'scsi0': f'local-lvm:32,discard=on'
        }
        
        response = requests.post(
            url, 
            headers=headers, 
            data=data, 
            verify=False
        )
        return response.json()

# Usage
api = ProxmoxAPI('proxmox.example.com', 'root@pam', 'password')
api.login()
result = api.create_vm('node1', 100, 'test-vm', memory=4096)
print(f"VM created: {result}")
```

### Terraform Configuration

```hcl
terraform {
  required_providers {
    proxmox = {
      source = "Telmate/proxmox"
      version = "2.9.14"
    }
  }
}

provider "proxmox" {
  pm_api_url = "https://proxmox.example.com:8006/api2/json"
  pm_user = "terraform@pve"
  pm_password = "terraform-password"
  pm_tls_insecure = true
}

# Create VM from template
resource "proxmox_vm_qemu" "web_server" {
  name        = "web-server-01"
  target_node = "node1"
  clone       = "ubuntu-template"
  
  cores   = 2
  sockets = 1
  memory  = 4096
  
  network {
    model  = "virtio"
    bridge = "vmbr0"
  }
  
  disk {
    type    = "scsi"
    storage = "local-lvm"
    size    = "32G"
  }
  
  # Cloud-init settings
  ciuser     = "ubuntu"
  cipassword = "changeme"
  ipconfig0  = "ip=10.0.0.100/24,gw=10.0.0.1"
  
  sshkeys = file("~/.ssh/id_rsa.pub")
}
```

### Ansible Playbook

```yaml
---
- name: Manage Proxmox Infrastructure
  hosts: proxmox
  tasks:
    - name: Create LXC container
      community.general.proxmox:
        api_user: root@pam
        api_password: "{{ proxmox_password }}"
        api_host: proxmox.example.com
        node: node1
        hostname: webapp-container
        ostemplate: 'local:vztmpl/ubuntu-20.04-standard_20.04-1_amd64.tar.gz'
        password: changeme
        cores: 2
        memory: 2048
        swap: 512
        disk: 8
        netif: '{"net0":"name=eth0,ip=dhcp,bridge=vmbr0"}'
        state: present
        
    - name: Start container
      community.general.proxmox:
        api_user: root@pam
        api_password: "{{ proxmox_password }}"
        api_host: proxmox.example.com
        node: node1
        hostname: webapp-container
        state: started
```

## 🏆 Best Practices

### Storage Configuration

```bash
# ZFS Pool Creation
zpool create -f -o ashift=12 rpool mirror /dev/sda /dev/sdb
zfs set compression=lz4 rpool
zfs create rpool/data

# Add ZFS storage to Proxmox
pvesm add zfspool local-zfs --pool rpool/data

# Ceph Configuration for distributed storage
pveceph init --network 10.10.10.0/24
pveceph mon create
pveceph mgr create
pveceph osd create /dev/sdc
```

### High Availability Setup

```bash
# Create cluster
pvecm create my-cluster

# Join node to cluster
pvecm add 10.0.0.1

# Configure HA for VM
ha-manager add vm:100 --state started --max_restart 3

# Configure fencing
echo "fence_virtd {
  modules {
    multicast {
      interface = vmbr0
    }
  }
}" > /etc/fence_virt.conf
```

### Backup Strategy

```bash
# Configure backup schedule
cat > /etc/vzdump.conf << EOF
tmpdir: /var/tmp
dumpdir: /var/lib/vz/dump
storage: backup-storage
mode: snapshot
compress: zstd
pigz: 4
zstd: 4
EOF

# Create backup job
vzdump 100 --compress zstd --storage backup-nfs --mode snapshot

# Automate with cron
echo "0 2 * * * root vzdump --all --compress zstd --storage backup-nfs --mode snapshot --mailto admin@example.com" >> /etc/crontab
```

## 🔧 Advanced Configuration

### Network Configuration

```bash
# VLAN-aware bridge
auto vmbr0
iface vmbr0 inet static
    address 10.0.0.1/24
    bridge-ports eno1
    bridge-stp off
    bridge-fd 0
    bridge-vlan-aware yes
    bridge-vids 2-4094

# Bond configuration for redundancy
auto bond0
iface bond0 inet manual
    bond-slaves eno1 eno2
    bond-miimon 100
    bond-mode active-backup

auto vmbr0
iface vmbr0 inet static
    address 10.0.0.1/24
    bridge-ports bond0
    bridge-stp off
    bridge-fd 0
```

### Custom Storage Integration

```python
#!/usr/bin/env python3
# Custom storage plugin for Proxmox

import json
import subprocess

class CustomStorage:
    def __init__(self, config):
        self.config = config
        
    def list_volumes(self):
        """List all volumes in custom storage"""
        cmd = ['custom-storage-cli', 'list', '--format=json']
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)
        
    def create_volume(self, name, size):
        """Create new volume"""
        cmd = [
            'custom-storage-cli', 'create',
            '--name', name,
            '--size', size
        ]
        subprocess.run(cmd, check=True)
        
    def delete_volume(self, name):
        """Delete volume"""
        cmd = ['custom-storage-cli', 'delete', '--name', name]
        subprocess.run(cmd, check=True)

# Register with Proxmox storage system
if __name__ == "__main__":
    storage = CustomStorage(config)
    # Integration logic here
```

## 📊 Monitoring & Metrics

### Prometheus Integration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'proxmox'
    static_configs:
      - targets:
          - 'node1:9100'
          - 'node2:9100'
          - 'node3:9100'
    
  - job_name: 'pve-exporter'
    static_configs:
      - targets: ['localhost:9221']
```

### Monitoring Script

```bash
#!/bin/bash
# Monitor Proxmox cluster health

check_cluster() {
    pvecm status | grep -q "Quorate: Yes"
    return $?
}

check_storage() {
    local threshold=90
    pvesm status | awk '{if ($4+0 > threshold) print "WARNING: " $1 " usage " $4 "%"}'
}

check_vms() {
    qm list | grep -c "running"
}

# Main monitoring loop
while true; do
    if ! check_cluster; then
        echo "ALERT: Cluster lost quorum!"
        # Send alert
    fi
    
    check_storage
    
    vm_count=$(check_vms)
    echo "Running VMs: $vm_count"
    
    sleep 60
done
```

## 🔒 Security Hardening

### Firewall Configuration

```bash
# Enable cluster firewall
pvecm set --firewall 1

# Configure firewall rules
cat > /etc/pve/firewall/cluster.fw << EOF
[OPTIONS]
enable: 1
policy_in: DROP
policy_out: ACCEPT

[RULES]
# Management access
IN ACCEPT -source 10.0.0.0/24 -p tcp -dport 8006 # Web UI
IN ACCEPT -source 10.0.0.0/24 -p tcp -dport 22   # SSH

# Cluster communication
IN ACCEPT -source 10.0.0.0/24 -p udp -dport 5404-5405 # Corosync
IN ACCEPT -source 10.0.0.0/24 -p tcp -dport 2224      # PCSD

# Storage protocols
IN ACCEPT -source 10.0.0.0/24 -p tcp -dport 111   # NFS
IN ACCEPT -source 10.0.0.0/24 -p tcp -dport 2049  # NFS
IN ACCEPT -source 10.0.0.0/24 -p tcp -dport 3260  # iSCSI
IN ACCEPT -source 10.0.0.0/24 -p tcp -dport 6789  # Ceph Monitor
EOF
```

### User Management

```bash
# Create user with limited permissions
pveum useradd developer@pve
pveum passwd developer@pve

# Create role with specific permissions
pveum roleadd VMOperator -privs "VM.Console,VM.PowerMgmt,VM.Monitor"

# Assign role to user for specific resources
pveum aclmod /vms/100 -user developer@pve -role VMOperator
```

## 💡 Interview Tips

### Common Interview Questions

1. **What's the difference between KVM and LXC in Proxmox?**
   - KVM: Full virtualization, isolated kernel, any OS
   - LXC: Container-based, shared kernel, Linux only
   - Performance and use case considerations

2. **How does Proxmox handle storage?**
   - Local storage (LVM, ZFS, directory)
   - Shared storage (NFS, iSCSI, Ceph)
   - Storage migration and replication

3. **Explain Proxmox clustering**
   - Corosync for cluster communication
   - Minimum 3 nodes for quorum
   - Shared storage requirements
   - Fencing for split-brain prevention

4. **How do you backup VMs in Proxmox?**
   - Snapshot vs suspend vs stop modes
   - vzdump command and options
   - Backup storage and retention
   - Restore procedures

### Practical Scenarios

- "Design a highly available Proxmox cluster"
- "Migrate from VMware to Proxmox"
- "Implement disaster recovery"
- "Optimize storage performance"
- "Secure a multi-tenant environment"

## 📚 Essential Resources

### 📖 Official Documentation
- **[Proxmox VE Documentation](https://pve.proxmox.com/pve-docs/)** - Comprehensive official docs
- **[Proxmox Wiki](https://pve.proxmox.com/wiki/Main_Page)** - Community wiki
- **[API Documentation](https://pve.proxmox.com/pve-docs/api-viewer/)** - REST API reference

### 🎥 Video Resources
- **[LearnLinuxTV Proxmox Series](https://www.youtube.com/playlist?list=PLT98CRl2KxKHnlbYhtABg6cF50bYa8Ulo)** - Comprehensive tutorial series
- **[Techno Tim](https://www.youtube.com/c/TechnoTim)** - Proxmox tutorials and projects
- **[Proxmox VE YouTube](https://www.youtube.com/c/ProxmoxVE)** - Official channel

### 🎓 Training & Courses
- **[Proxmox Training](https://www.proxmox.com/en/training)** - Official training courses
- **[Udemy Proxmox Courses](https://www.udemy.com/topic/proxmox/)** - Various skill levels
- **[Linux Academy](https://linuxacademy.com)** - Virtualization courses

### 📝 Blogs & Articles
- **[Proxmox Blog](https://www.proxmox.com/en/news/blog)** - Official blog
- **[ServeTheHome](https://www.servethehome.com)** - Hardware and Proxmox guides
- **[TurnKey Linux](https://www.turnkeylinux.org)** - Proxmox templates

### 🛠️ Tools & Utilities
- **[Proxmox Backup Server](https://pbs.proxmox.com)** - Enterprise backup solution
- **[Proxmox Mail Gateway](https://pmg.proxmox.com)** - Email security
- **[ProxLB](https://github.com/BeryJu/ProxLB)** - Load balancer for Proxmox
- **[cv4pve-cli](https://github.com/Corsinvest/cv4pve-cli)** - CLI tools

### 👥 Community
- **[Proxmox Forum](https://forum.proxmox.com)** - Official community forum
- **[r/Proxmox](https://reddit.com/r/proxmox)** - Reddit community
- **[Proxmox Discord](https://discord.gg/proxmox)** - Community Discord
- **[GitHub Awesome-Proxmox](https://github.com/awesome-proxmox/awesome-proxmox)** - Curated resources

### 🏆 Certifications
- **[Proxmox Certified Professional](https://www.proxmox.com/en/training/certification)** - Official certification
- **Linux Foundation Virtualization** - Related certifications
- **Red Hat Virtualization** - Transferable skills

---

**Next Steps**: After mastering Proxmox, explore [OpenStack](/technical/openstack) for larger scale deployments or [Kubernetes](/technical/kubernetes) for container orchestration.