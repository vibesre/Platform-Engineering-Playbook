# GlusterFS

GlusterFS is a scale-out network-attached storage file system that aggregates various storage servers over network interconnects into one large parallel network file system. It provides enterprise-class features and scalability for unstructured data.

## Installation

### Binary Installation

#### CentOS/RHEL/Fedora
```bash
# Enable GlusterFS repository
sudo yum install centos-release-gluster
# or for RHEL
sudo subscription-manager repos --enable=rhel-7-server-rh-gluster-3-for-rhel-7-server-rpms

# Install GlusterFS server
sudo yum install glusterfs-server

# Start and enable GlusterFS service
sudo systemctl start glusterd
sudo systemctl enable glusterd

# Check service status
sudo systemctl status glusterd
```

#### Ubuntu/Debian
```bash
# Add GlusterFS repository
sudo add-apt-repository ppa:gluster/glusterfs-11
sudo apt update

# Install GlusterFS server
sudo apt install glusterfs-server

# Start and enable GlusterFS service
sudo systemctl start glusterd
sudo systemctl enable glusterd

# Install client tools
sudo apt install glusterfs-client
```

### Container Installation
```bash
# Run GlusterFS in container
docker run -d --name glusterfs \
  --privileged \
  --net=host \
  -v /etc/glusterfs:/etc/glusterfs:z \
  -v /var/lib/glusterd:/var/lib/glusterd:z \
  -v /var/log/glusterfs:/var/log/glusterfs:z \
  -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
  -v /mnt/brick1:/mnt/brick1:z \
  gluster/gluster-centos:latest

# Docker Compose setup
cat > docker-compose.yml << EOF
version: '3.8'
services:
  gluster1:
    image: gluster/gluster-centos:latest
    hostname: gluster1
    privileged: true
    network_mode: host
    volumes:
      - /etc/glusterfs:/etc/glusterfs:z
      - /var/lib/glusterd:/var/lib/glusterd:z
      - /var/log/glusterfs:/var/log/glusterfs:z
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
      - gluster1_brick:/mnt/brick1:z
    environment:
      - GLUSTER_PEER=gluster2
      - GLUSTER_VOL=gv0
      - GLUSTER_BRICK=/mnt/brick1/gv0
    
  gluster2:
    image: gluster/gluster-centos:latest
    hostname: gluster2
    privileged: true
    network_mode: host
    volumes:
      - /etc/glusterfs:/etc/glusterfs:z
      - /var/lib/glusterd:/var/lib/glusterd:z
      - /var/log/glusterfs:/var/log/glusterfs:z
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
      - gluster2_brick:/mnt/brick2:z
    environment:
      - GLUSTER_PEER=gluster1
      - GLUSTER_VOL=gv0
      - GLUSTER_BRICK=/mnt/brick2/gv0

volumes:
  gluster1_brick:
  gluster2_brick:
EOF

docker-compose up -d
```

### Kubernetes Installation (Heketi + GlusterFS)
```yaml
# glusterfs-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: glusterfs
  namespace: glusterfs
  labels:
    glusterfs: daemonset
spec:
  selector:
    matchLabels:
      glusterfs-node: pod
  template:
    metadata:
      name: glusterfs
      labels:
        glusterfs-node: pod
    spec:
      nodeSelector:
        storagenode: glusterfs
      hostNetwork: true
      containers:
      - image: gluster/gluster-centos:latest
        name: glusterfs
        volumeMounts:
        - name: glusterfs-heketi
          mountPath: "/var/lib/heketi"
        - name: glusterfs-run
          mountPath: "/run"
        - name: glusterfs-lvm
          mountPath: "/run/lvm"
        - name: glusterfs-etc
          mountPath: "/etc/glusterfs"
        - name: glusterfs-logs
          mountPath: "/var/log/glusterfs"
        - name: glusterfs-config
          mountPath: "/var/lib/glusterd"
        - name: glusterfs-dev
          mountPath: "/dev"
        - name: glusterfs-misc
          mountPath: "/var/lib/misc/glusterfsd"
        - name: glusterfs-cgroup
          mountPath: "/sys/fs/cgroup"
          readOnly: true
        - name: glusterfs-ssl
          mountPath: "/etc/ssl"
          readOnly: true
        securityContext:
          capabilities: {}
          privileged: true
        readinessProbe:
          timeoutSeconds: 3
          initialDelaySeconds: 40
          exec:
            command:
            - "/bin/bash"
            - "-c"
            - systemctl status glusterd.service
        livenessProbe:
          timeoutSeconds: 3
          initialDelaySeconds: 40
          exec:
            command:
            - "/bin/bash"
            - "-c"
            - systemctl status glusterd.service
        resources:
          requests:
            memory: 100Mi
            cpu: 100m
      volumes:
      - name: glusterfs-heketi
        hostPath:
          path: "/var/lib/heketi"
      - name: glusterfs-run
        hostPath:
          path: "/run"
      - name: glusterfs-lvm
        hostPath:
          path: "/run/lvm"
      - name: glusterfs-etc
        hostPath:
          path: "/etc/glusterfs"
      - name: glusterfs-logs
        hostPath:
          path: "/var/log/glusterfs"
      - name: glusterfs-config
        hostPath:
          path: "/var/lib/glusterd"
      - name: glusterfs-dev
        hostPath:
          path: "/dev"
      - name: glusterfs-misc
        hostPath:
          path: "/var/lib/misc/glusterfsd"
      - name: glusterfs-cgroup
        hostPath:
          path: "/sys/fs/cgroup"
      - name: glusterfs-ssl
        hostPath:
          path: "/etc/ssl"
---
# Heketi Service
apiVersion: v1
kind: Service
metadata:
  name: heketi
  namespace: glusterfs
  labels:
    glusterfs: heketi-service
spec:
  ports:
  - port: 8080
    targetPort: 8080
  selector:
    glusterfs: heketi-pod
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: heketi
  namespace: glusterfs
  labels:
    glusterfs: heketi-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      glusterfs: heketi-pod
  template:
    metadata:
      name: heketi
      labels:
        glusterfs: heketi-pod
    spec:
      serviceAccountName: heketi-service-account
      containers:
      - image: heketi/heketi:dev
        imagePullPolicy: Always
        name: heketi
        env:
        - name: HEKETI_EXECUTOR
          value: kubernetes
        - name: HEKETI_FSTAB
          value: "/var/lib/heketi/fstab"
        - name: HEKETI_SNAPSHOT_LIMIT
          value: '14'
        - name: HEKETI_KUBE_GLUSTER_DAEMONSET
          value: "y"
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: db
          mountPath: "/var/lib/heketi"
        - name: config
          mountPath: "/etc/heketi"
        readinessProbe:
          timeoutSeconds: 3
          initialDelaySeconds: 3
          httpGet:
            path: "/hello"
            port: 8080
        livenessProbe:
          timeoutSeconds: 3
          initialDelaySeconds: 30
          httpGet:
            path: "/hello"
            port: 8080
      volumes:
      - name: db
        hostPath:
          path: "/heketi-storage"
      - name: config
        secret:
          secretName: heketi-config-secret

# Apply the configuration
kubectl apply -f glusterfs-daemonset.yaml
```

## Cluster Setup

### Trusted Storage Pool
```bash
# Prepare brick directories on each node
sudo mkdir -p /mnt/brick1/gv0
sudo mkdir -p /mnt/brick2/gv0

# Probe peer nodes (run from one node)
sudo gluster peer probe node2
sudo gluster peer probe node3
sudo gluster peer probe node4

# Check peer status
sudo gluster peer status
sudo gluster pool list

# Remove peer (if needed)
sudo gluster peer detach node4
```

### Volume Creation and Configuration
```bash
# Create distributed volume
sudo gluster volume create gv0 \
  node1:/mnt/brick1/gv0 \
  node2:/mnt/brick2/gv0

# Create replicated volume
sudo gluster volume create gv1 replica 2 \
  node1:/mnt/brick1/gv1 \
  node2:/mnt/brick2/gv1

# Create distributed-replicated volume
sudo gluster volume create gv2 replica 2 \
  node1:/mnt/brick1/gv2 \
  node2:/mnt/brick2/gv2 \
  node3:/mnt/brick3/gv2 \
  node4:/mnt/brick4/gv2

# Create striped volume
sudo gluster volume create gv3 stripe 2 \
  node1:/mnt/brick1/gv3 \
  node2:/mnt/brick2/gv3

# Create dispersed volume (erasure coding)
sudo gluster volume create gv4 disperse 3 redundancy 1 \
  node1:/mnt/brick1/gv4 \
  node2:/mnt/brick2/gv4 \
  node3:/mnt/brick3/gv4

# Start volume
sudo gluster volume start gv0

# Check volume info
sudo gluster volume info gv0
sudo gluster volume status gv0

# List all volumes
sudo gluster volume list
```

## Client Configuration

### Native GlusterFS Mount
```bash
# Install GlusterFS client
sudo apt install glusterfs-client  # Ubuntu/Debian
sudo yum install glusterfs-fuse    # CentOS/RHEL

# Create mount point
sudo mkdir /mnt/glusterfs

# Mount GlusterFS volume
sudo mount -t glusterfs node1:gv0 /mnt/glusterfs

# Mount with options
sudo mount -t glusterfs \
  -o backup-volfile-servers=node2:node3,log-level=WARNING \
  node1:gv0 /mnt/glusterfs

# Add to fstab for persistent mount
echo "node1:gv0 /mnt/glusterfs glusterfs defaults,_netdev,backup-volfile-servers=node2:node3 0 0" | sudo tee -a /etc/fstab

# Test mount
df -h /mnt/glusterfs
ls -la /mnt/glusterfs
```

### NFS Mount
```bash
# Enable NFS service on GlusterFS
sudo gluster volume set gv0 nfs.disable off
sudo gluster volume set gv0 nfs.addr-namelookup off
sudo gluster volume set gv0 nfs.export-volumes on

# Mount via NFS
sudo mkdir /mnt/nfs-gluster
sudo mount -t nfs -o vers=3 node1:/gv0 /mnt/nfs-gluster

# Add to fstab
echo "node1:/gv0 /mnt/nfs-gluster nfs defaults,_netdev,vers=3 0 0" | sudo tee -a /etc/fstab
```

### SMB/CIFS Mount
```bash
# Enable SMB service
sudo gluster volume set gv0 user.smb enable
sudo gluster volume set gv0 user.cifs enable

# Configure Samba
sudo apt install samba samba-common-bin
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.backup

# Add to smb.conf
cat >> /etc/samba/smb.conf << EOF
[glusterfs]
    comment = GlusterFS Share
    path = /mnt/glusterfs
    browseable = yes
    guest ok = yes
    read only = no
    create mask = 0755
EOF

sudo systemctl restart smbd

# Mount from Windows/Linux clients
# Windows: \\server-ip\glusterfs
# Linux: mount -t cifs //server-ip/glusterfs /mnt/cifs -o username=user
```

## Volume Management

### Volume Operations
```bash
# Stop volume
sudo gluster volume stop gv0

# Delete volume
sudo gluster volume delete gv0

# Add brick to volume
sudo gluster volume add-brick gv0 node3:/mnt/brick3/gv0

# Remove brick from volume
sudo gluster volume remove-brick gv0 node3:/mnt/brick3/gv0 start
sudo gluster volume remove-brick gv0 node3:/mnt/brick3/gv0 status
sudo gluster volume remove-brick gv0 node3:/mnt/brick3/gv0 commit

# Replace brick
sudo gluster volume replace-brick gv0 \
  node2:/mnt/brick2/gv0 \
  node2:/mnt/brick2-new/gv0 \
  commit force

# Rebalance volume
sudo gluster volume rebalance gv0 start
sudo gluster volume rebalance gv0 status
sudo gluster volume rebalance gv0 stop
```

### Volume Tuning
```bash
# Performance tuning options
sudo gluster volume set gv0 performance.cache-size 256MB
sudo gluster volume set gv0 performance.io-thread-count 32
sudo gluster volume set gv0 performance.read-ahead on
sudo gluster volume set gv0 performance.readdir-ahead on
sudo gluster volume set gv0 performance.quick-read on
sudo gluster volume set gv0 performance.write-behind on
sudo gluster volume set gv0 performance.stat-prefetch on

# Network tuning
sudo gluster volume set gv0 network.ping-timeout 42
sudo gluster volume set gv0 network.frame-timeout 600

# Client tuning
sudo gluster volume set gv0 client.event-threads 4
sudo gluster volume set gv0 client.grace-timeout 120

# Server tuning
sudo gluster volume set gv0 server.event-threads 4
sudo gluster volume set gv0 server.outstanding-rpc-limit 128

# View all volume options
sudo gluster volume get gv0 all
```

## High Availability and Replication

### Geo-Replication Setup
```bash
# Create geo-replication session
sudo gluster volume geo-replication gv0 slave-node::slave-vol create push-pem

# Configure SSH keys for geo-replication
sudo gluster system:: execute gsec_create
sudo gluster volume geo-replication gv0 slave-node::slave-vol config use_gsec_create true

# Start geo-replication
sudo gluster volume geo-replication gv0 slave-node::slave-vol start

# Check geo-replication status
sudo gluster volume geo-replication gv0 slave-node::slave-vol status

# Configure geo-replication options
sudo gluster volume geo-replication gv0 slave-node::slave-vol config sync-method rsync
sudo gluster volume geo-replication gv0 slave-node::slave-vol config ignore_deletes true
sudo gluster volume geo-replication gv0 slave-node::slave-vol config checkpoint now

# Stop geo-replication
sudo gluster volume geo-replication gv0 slave-node::slave-vol stop
```

### Self-Healing
```bash
# Check self-heal status
sudo gluster volume heal gv0 info
sudo gluster volume heal gv0 info summary

# Trigger full self-heal
sudo gluster volume heal gv0 full

# Monitor self-heal progress
sudo gluster volume heal gv0 statistics

# Get list of files needing heal
sudo gluster volume heal gv0 info split-brain

# Resolve split-brain (choose source)
sudo gluster volume heal gv0 split-brain source-brick node1:/mnt/brick1/gv0 /path/to/file

# Enable/disable self-heal daemon
sudo gluster volume set gv0 cluster.self-heal-daemon on
sudo gluster volume set gv0 cluster.heal-timeout 600
```

## Monitoring and Troubleshooting

### Volume Health Checks
```bash
# Check volume status
sudo gluster volume status gv0 detail
sudo gluster volume status gv0 clients
sudo gluster volume status gv0 mem
sudo gluster volume status gv0 inode
sudo gluster volume status gv0 fd
sudo gluster volume status gv0 callpool

# Check brick status
sudo gluster volume status gv0 node1:/mnt/brick1/gv0 detail

# Profile volume operations
sudo gluster volume profile gv0 start
sudo gluster volume profile gv0 info
sudo gluster volume profile gv0 info cumulative
sudo gluster volume profile gv0 stop

# Volume top operations
sudo gluster volume top gv0 open
sudo gluster volume top gv0 read
sudo gluster volume top gv0 write
sudo gluster volume top gv0 opendir
sudo gluster volume top gv0 readdir
```

### Log Analysis
```bash
# View GlusterFS logs
sudo tail -f /var/log/glusterfs/glusterd.log
sudo tail -f /var/log/glusterfs/bricks/mnt-brick1-gv0.log
sudo tail -f /var/log/glusterfs/mnt-glusterfs.log

# Set log levels
sudo gluster volume set gv0 diagnostics.brick-log-level WARNING
sudo gluster volume set gv0 diagnostics.client-log-level INFO

# Log rotation configuration
sudo logrotate -f /etc/logrotate.d/glusterfs
```

### Performance Monitoring Script
```python
#!/usr/bin/env python3
# gluster_monitor.py

import subprocess
import json
import time
import sys
from datetime import datetime

class GlusterMonitor:
    def __init__(self, volume_name):
        self.volume_name = volume_name
    
    def run_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception as e:
            print(f"Error running command: {e}")
            return None
    
    def get_volume_status(self):
        cmd = f"gluster volume status {self.volume_name} detail"
        output = self.run_command(cmd)
        if output:
            return self.parse_volume_status(output)
        return {}
    
    def parse_volume_status(self, output):
        status = {}
        lines = output.split('\n')
        current_brick = None
        
        for line in lines:
            if 'Brick' in line and ':' in line:
                current_brick = line.split(':', 1)[1].strip()
                status[current_brick] = {}
            elif current_brick and ':' in line:
                key, value = line.split(':', 1)
                status[current_brick][key.strip()] = value.strip()
        
        return status
    
    def get_volume_profile(self):
        # Start profiling if not already started
        self.run_command(f"gluster volume profile {self.volume_name} start 2>/dev/null")
        time.sleep(1)
        
        cmd = f"gluster volume profile {self.volume_name} info"
        output = self.run_command(cmd)
        if output:
            return self.parse_profile_info(output)
        return {}
    
    def parse_profile_info(self, output):
        profile = {}
        lines = output.split('\n')
        current_brick = None
        
        for line in lines:
            if 'Brick:' in line:
                current_brick = line.split(':', 1)[1].strip()
                profile[current_brick] = {'fops': {}, 'cumulative': {}}
            elif current_brick and '%' in line and 'AvgLatency' in output:
                parts = line.split()
                if len(parts) >= 7:
                    fop_name = parts[0]
                    hits = parts[1]
                    avg_latency = parts[2]
                    min_latency = parts[3]
                    max_latency = parts[4]
                    
                    profile[current_brick]['fops'][fop_name] = {
                        'hits': hits,
                        'avg_latency': avg_latency,
                        'min_latency': min_latency,
                        'max_latency': max_latency
                    }
        
        return profile
    
    def get_heal_info(self):
        cmd = f"gluster volume heal {self.volume_name} info summary"
        output = self.run_command(cmd)
        if output:
            return self.parse_heal_info(output)
        return {}
    
    def parse_heal_info(self, output):
        heal_info = {}
        lines = output.split('\n')
        
        for line in lines:
            if 'Status:' in line:
                heal_info['status'] = line.split(':', 1)[1].strip()
            elif 'Number of entries:' in line:
                heal_info['entries'] = line.split(':', 1)[1].strip()
        
        return heal_info
    
    def monitor(self, interval=60):
        print(f"Monitoring GlusterFS volume: {self.volume_name}")
        print(f"Refresh interval: {interval} seconds")
        print("-" * 80)
        
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{timestamp}] Volume Status:")
            
            # Get volume status
            status = self.get_volume_status()
            for brick, info in status.items():
                online = info.get('Online', 'N/A')
                disk_space_free = info.get('Disk Space Free', 'N/A')
                total_disk_space = info.get('Total Disk Space', 'N/A')
                print(f"  {brick}: Online={online}, Free={disk_space_free}, Total={total_disk_space}")
            
            # Get performance profile
            profile = self.get_volume_profile()
            if profile:
                print(f"\n[{timestamp}] Performance Metrics:")
                for brick, data in profile.items():
                    if 'fops' in data:
                        top_fops = sorted(data['fops'].items(), 
                                        key=lambda x: int(x[1]['hits']) if x[1]['hits'].isdigit() else 0, 
                                        reverse=True)[:3]
                        print(f"  {brick} - Top FOPs:")
                        for fop, metrics in top_fops:
                            print(f"    {fop}: {metrics['hits']} hits, {metrics['avg_latency']} avg latency")
            
            # Get heal info
            heal_info = self.get_heal_info()
            if heal_info:
                print(f"\n[{timestamp}] Heal Status: {heal_info}")
            
            time.sleep(interval)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gluster_monitor.py <volume_name> [interval]")
        sys.exit(1)
    
    volume_name = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    
    monitor = GlusterMonitor(volume_name)
    try:
        monitor.monitor(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
```

## Security Configuration

### Access Control
```bash
# Set volume authentication
sudo gluster volume set gv0 auth.allow 192.168.1.*
sudo gluster volume set gv0 auth.reject 192.168.2.*

# Enable SSL/TLS
sudo gluster volume set gv0 client.ssl on
sudo gluster volume set gv0 server.ssl on

# Configure SSL certificates
sudo mkdir -p /etc/ssl/glusterfs
sudo openssl genrsa -out /etc/ssl/glusterfs/glusterfs.key 2048
sudo openssl req -new -x509 -key /etc/ssl/glusterfs/glusterfs.key \
  -out /etc/ssl/glusterfs/glusterfs.pem -days 365

# Set certificate paths
sudo gluster volume set gv0 ssl.certificate-depth 2
sudo gluster volume set gv0 ssl.ca-list /etc/ssl/glusterfs/ca.pem
sudo gluster volume set gv0 ssl.cert-file /etc/ssl/glusterfs/glusterfs.pem
sudo gluster volume set gv0 ssl.key-file /etc/ssl/glusterfs/glusterfs.key
```

### User and Group Management
```bash
# Set POSIX ACL support
sudo gluster volume set gv0 server.root-squash enable
sudo gluster volume set gv0 server.anonuid 65534
sudo gluster volume set gv0 server.anongid 65534

# Enable extended attributes for ACLs
sudo gluster volume set gv0 storage.linux-aio on
sudo mount -o remount,acl /mnt/glusterfs

# Set ACLs on mounted filesystem
setfacl -m u:user1:rwx /mnt/glusterfs/dir1
setfacl -m g:group1:r-x /mnt/glusterfs/dir1
getfacl /mnt/glusterfs/dir1
```

## Backup and Recovery

### Volume Backup Script
```bash
#!/bin/bash
# gluster_backup.sh

VOLUME_NAME="gv0"
BACKUP_DIR="/backup/glusterfs"
DATE=$(date +%Y%m%d_%H%M%S)
MOUNT_POINT="/mnt/glusterfs-backup"

# Create backup directory
mkdir -p "${BACKUP_DIR}/${DATE}"

# Create temporary mount point
mkdir -p "${MOUNT_POINT}"

# Mount volume for backup
mount -t glusterfs localhost:${VOLUME_NAME} "${MOUNT_POINT}"

if [ $? -eq 0 ]; then
    echo "Volume mounted successfully"
    
    # Create backup using rsync
    rsync -avz --progress "${MOUNT_POINT}/" "${BACKUP_DIR}/${DATE}/"
    
    # Unmount volume
    umount "${MOUNT_POINT}"
    
    # Create tarball
    cd "${BACKUP_DIR}"
    tar -czf "gluster-${VOLUME_NAME}-${DATE}.tar.gz" "${DATE}"
    rm -rf "${DATE}"
    
    echo "Backup completed: ${BACKUP_DIR}/gluster-${VOLUME_NAME}-${DATE}.tar.gz"
    
    # Cleanup old backups (keep last 7 days)
    find "${BACKUP_DIR}" -name "gluster-${VOLUME_NAME}-*.tar.gz" -mtime +7 -delete
else
    echo "Failed to mount volume for backup"
    exit 1
fi
```

### Snapshot Management
```bash
# Create snapshot
sudo gluster snapshot create snap1 gv0

# List snapshots
sudo gluster snapshot list

# Get snapshot info
sudo gluster snapshot info snap1

# Activate/deactivate snapshot
sudo gluster snapshot activate snap1
sudo gluster snapshot deactivate snap1

# Restore from snapshot
sudo gluster snapshot restore snap1

# Delete snapshot
sudo gluster snapshot delete snap1

# Configure snapshot options
sudo gluster snapshot config auto-delete enable
sudo gluster snapshot config snap-max-hard-limit 10
sudo gluster snapshot config snap-max-soft-limit 8
```

## Kubernetes Integration

### StorageClass Configuration
```yaml
# glusterfs-storageclass.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: glusterfs
provisioner: kubernetes.io/glusterfs
parameters:
  resturl: "http://heketi-service:8080"
  clusterid: "cluster1"
  restauthenabled: "false"
  volumetype: "replicate:2"
  secretNamespace: "glusterfs"
  secretName: "heketi-secret"
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: Immediate
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: glusterfs-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: glusterfs
---
apiVersion: v1
kind: Pod
metadata:
  name: glusterfs-test-pod
spec:
  containers:
  - name: app
    image: nginx:latest
    volumeMounts:
    - name: gluster-storage
      mountPath: /data
    ports:
    - containerPort: 80
  volumes:
  - name: gluster-storage
    persistentVolumeClaim:
      claimName: glusterfs-pvc

# Apply configuration
kubectl apply -f glusterfs-storageclass.yaml
```

### Endpoint Configuration
```yaml
# glusterfs-endpoints.yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: glusterfs-cluster
subsets:
- addresses:
  - ip: 192.168.1.100
  - ip: 192.168.1.101
  - ip: 192.168.1.102
  ports:
  - port: 1
    protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  name: glusterfs-cluster
spec:
  ports:
  - port: 1
    protocol: TCP
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: gluster-pv
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteMany
  glusterfs:
    endpoints: glusterfs-cluster
    path: gv0
    readOnly: false
  persistentVolumeReclaimPolicy: Retain

# Apply configuration
kubectl apply -f glusterfs-endpoints.yaml
```

## Performance Optimization

### System Tuning
```bash
# Filesystem optimizations
echo 'vm.dirty_ratio = 5' >> /etc/sysctl.conf
echo 'vm.dirty_background_ratio = 2' >> /etc/sysctl.conf
echo 'vm.vfs_cache_pressure = 50' >> /etc/sysctl.conf
sudo sysctl -p

# Network optimizations
echo 'net.core.rmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_rmem = 4096 87380 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem = 4096 65536 134217728' >> /etc/sysctl.conf
sudo sysctl -p

# Disk I/O scheduling
echo mq-deadline > /sys/block/sdb/queue/scheduler
echo 8192 > /sys/block/sdb/queue/read_ahead_kb

# Mount options for better performance
mount -o remount,noatime,nodiratime /mnt/brick1
```

### Volume Performance Tuning
```bash
# Client-side optimizations
sudo gluster volume set gv0 performance.cache-size 1GB
sudo gluster volume set gv0 performance.io-thread-count 32
sudo gluster volume set gv0 performance.write-behind on
sudo gluster volume set gv0 performance.read-ahead on
sudo gluster volume set gv0 performance.readdir-ahead on
sudo gluster volume set gv0 performance.quick-read on

# Network optimizations
sudo gluster volume set gv0 network.remote-dio enable
sudo gluster volume set gv0 network.ping-timeout 42
sudo gluster volume set gv0 client.event-threads 4
sudo gluster volume set gv0 server.event-threads 4

# Brick optimizations
sudo gluster volume set gv0 storage.health-check-interval 30
sudo gluster volume set gv0 cluster.lookup-optimize on
```

## Resources

- [GlusterFS Documentation](https://docs.gluster.org/)
- [GlusterFS Administration Guide](https://docs.gluster.org/en/latest/Administrator-Guide/)
- [GlusterFS Troubleshooting](https://docs.gluster.org/en/latest/Troubleshooting/)
- [Heketi Documentation](https://github.com/heketi/heketi/wiki)
- [GlusterFS Performance Tuning](https://docs.gluster.org/en/latest/Administrator-Guide/Performance-Tuning/)
- [GlusterFS Security Guide](https://docs.gluster.org/en/latest/Administrator-Guide/SSL/)
- [GlusterFS Monitoring](https://docs.gluster.org/en/latest/Administrator-Guide/Monitoring-Workload/)
- [GlusterFS Community](https://www.gluster.org/community/)
- [GlusterFS GitHub Repository](https://github.com/gluster/glusterfs)
- [Red Hat Gluster Storage](https://www.redhat.com/en/technologies/storage/gluster)