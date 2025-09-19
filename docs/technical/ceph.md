# Ceph

Ceph is a unified, distributed storage system designed for excellent performance, reliability, and scalability. It provides object, block, and file storage in a single unified cluster, making it ideal for cloud platforms and large-scale deployments.

## Installation

### Cephadm Installation (Recommended)
```bash
# Install cephadm on Ubuntu/Debian
curl --silent --remote-name --location \
  https://github.com/ceph/ceph/raw/pacific/src/cephadm/cephadm
chmod +x cephadm
sudo mv cephadm /usr/local/bin/

# Add Ceph repository and install
./cephadm add-repo --release pacific
./cephadm install

# Bootstrap cluster (on first node)
sudo cephadm bootstrap --mon-ip <MON_IP>

# Example with specific configuration
sudo cephadm bootstrap \
  --mon-ip 192.168.1.100 \
  --cluster-network 192.168.1.0/24 \
  --ssh-user ceph \
  --initial-dashboard-user admin \
  --initial-dashboard-password password123
```

### Container Installation
```bash
# Using podman/docker
sudo podman run --rm -it \
  --net=host \
  -v /etc/ceph:/etc/ceph:z \
  -v /var/lib/ceph:/var/lib/ceph:z \
  -v /var/log/ceph:/var/log/ceph:z \
  quay.io/ceph/ceph:v18 \
  cephadm bootstrap --mon-ip <MON_IP>

# Docker Compose for development
cat > docker-compose.yml << EOF
version: '3.8'
services:
  ceph-mon:
    image: quay.io/ceph/ceph:v18
    container_name: ceph-mon
    environment:
      - MON_IP=192.168.1.100
      - CEPH_PUBLIC_NETWORK=192.168.1.0/24
    volumes:
      - ceph-conf:/etc/ceph
      - ceph-data:/var/lib/ceph
    ports:
      - "6789:6789"
      - "3300:3300"
    command: ceph-mon
    
  ceph-mgr:
    image: quay.io/ceph/ceph:v18
    container_name: ceph-mgr
    depends_on:
      - ceph-mon
    volumes:
      - ceph-conf:/etc/ceph
      - ceph-data:/var/lib/ceph
    ports:
      - "8080:8080"
    command: ceph-mgr
    
  ceph-osd:
    image: quay.io/ceph/ceph:v18
    container_name: ceph-osd
    depends_on:
      - ceph-mon
    volumes:
      - ceph-conf:/etc/ceph
      - ceph-data:/var/lib/ceph
      - /dev:/dev
    privileged: true
    command: ceph-osd

volumes:
  ceph-conf:
  ceph-data:
EOF

docker-compose up -d
```

### Kubernetes Installation (Rook)
```yaml
# rook-operator.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: rook-ceph
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rook-ceph-operator
  namespace: rook-ceph
spec:
  replicas: 1
  selector:
    matchLabels:
      app: rook-ceph-operator
  template:
    metadata:
      labels:
        app: rook-ceph-operator
    spec:
      serviceAccountName: rook-ceph-system
      containers:
      - name: rook-ceph-operator
        image: rook/ceph:v1.12.0
        args: ["ceph", "operator"]
        env:
        - name: ROOK_CURRENT_NAMESPACE_ONLY
          value: "false"
        - name: ROOK_ALLOW_MULTIPLE_FILESYSTEMS
          value: "false"
        - name: ROOK_LOG_LEVEL
          value: "INFO"
        - name: ROOK_CEPH_STATUS_CHECK_INTERVAL
          value: "60s"
        - name: ROOK_MON_HEALTHCHECK_INTERVAL
          value: "45s"
        - name: ROOK_MON_OUT_TIMEOUT
          value: "600s"
        - name: ROOK_DISCOVER_DEVICES_INTERVAL
          value: "60m"
        - name: ROOK_HOSTPATH_REQUIRES_PRIVILEGED
          value: "true"
        - name: ROOK_ENABLE_SELINUX_RELABELING
          value: "true"
        - name: ROOK_ENABLE_FSGROUP
          value: "true"
        - name: ROOK_ENABLE_FLEX_DRIVER
          value: "false"
        - name: ROOK_ENABLE_DISCOVERY_DAEMON
          value: "true"
        - name: ROOK_ENABLE_MACHINE_DISRUPTION_BUDGET
          value: "false"
        - name: ROOK_DISABLE_DEVICE_HOTPLUG
          value: "false"
        - name: CSI_ENABLE_SNAPSHOTTER
          value: "true"
        - name: CSI_ENABLE_CEPHFS_SNAPSHOTTER
          value: "true"
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
          requests:
            cpu: 100m
            memory: 128Mi
---
# Apply Rook CRDs and RBAC first, then:
apiVersion: ceph.rook.io/v1
kind: CephCluster
metadata:
  name: rook-ceph
  namespace: rook-ceph
spec:
  cephVersion:
    image: quay.io/ceph/ceph:v18.2.0
    allowUnsupported: false
  dataDirHostPath: /var/lib/rook
  skipUpgradeChecks: false
  continueUpgradeAfterChecksEvenIfNotHealthy: false
  waitTimeoutForHealthyOSDInMinutes: 10
  mon:
    count: 3
    allowMultiplePerNode: false
  mgr:
    count: 2
    allowMultiplePerNode: false
    modules:
    - name: pg_autoscaler
      enabled: true
  dashboard:
    enabled: true
    port: 7000
    ssl: true
  crashCollector:
    disable: false
  logCollector:
    enabled: true
    periodicity: daily
    maxLogSize: 500M
  cleanupPolicy:
    confirmation: ""
    sanitizeDisks:
      method: quick
      dataSource: zero
      iteration: 1
    allowUninstallWithVolumes: false
  annotations:
  labels:
  placement:
  resources:
    mgr:
      limits:
        cpu: "1000m"
        memory: "1Gi"
      requests:
        cpu: "500m"
        memory: "512Mi"
    mon:
      limits:
        cpu: "2000m"
        memory: "2Gi"
      requests:
        cpu: "1000m"
        memory: "1Gi"
    osd:
      limits:
        cpu: "2000m"
        memory: "4Gi"
      requests:
        cpu: "1000m"
        memory: "2Gi"
  priorityClassNames:
    mon: system-node-critical
    osd: system-node-critical
    mgr: system-cluster-critical
  storage:
    useAllNodes: true
    useAllDevices: true
    deviceFilter: "^sd[b-z]"
    config:
      osdsPerDevice: "1"
    nodes:
    - name: "node1"
      devices:
      - name: "sdb"
      - name: "sdc"
    - name: "node2"
      devices:
      - name: "sdb"
      - name: "sdc"
    - name: "node3"
      devices:
      - name: "sdb"
      - name: "sdc"
  disruptionManagement:
    managePodBudgets: true
    osdMaintenanceTimeout: 30
    pgHealthCheckTimeout: 0
  healthCheck:
    daemonHealth:
      mon:
        disabled: false
        interval: 45s
      osd:
        disabled: false
        interval: 60s
      status:
        disabled: false
        interval: 60s
    livenessProbe:
      mon:
        disabled: false
      mgr:
        disabled: false
      osd:
        disabled: false

# Apply the configuration
kubectl apply -f rook-operator.yaml
```

## Cluster Management

### Adding Nodes
```bash
# Copy SSH key to new node
ssh-copy-id -f -i /etc/ceph/ceph.pub root@<NEW_NODE>

# Add new node to cluster
sudo ceph orch host add <NEW_NODE> <IP_ADDRESS>

# Add with specific labels
sudo ceph orch host add node4 192.168.1.104 --labels _admin,mon,mgr,osd

# List cluster hosts
sudo ceph orch host ls

# Add OSD to new node
sudo ceph orch daemon add osd node4:/dev/sdb
```

### Service Management
```bash
# Deploy MON daemons
sudo ceph orch apply mon --placement="node1,node2,node3"

# Deploy MGR daemons
sudo ceph orch apply mgr --placement="node1,node2"

# Deploy OSDs on all available devices
sudo ceph orch apply osd --all-available-devices

# Deploy specific OSD
sudo ceph orch daemon add osd node1:/dev/sdb

# List all services
sudo ceph orch ls

# Check daemon status
sudo ceph orch ps

# Remove daemon
sudo ceph orch daemon rm osd.1 --force
```

## Storage Pools and Placement Groups

### Pool Management
```bash
# Create replicated pool
sudo ceph osd pool create mypool 128 128 replicated

# Create erasure coded pool
sudo ceph osd pool create ec-pool 128 128 erasure

# Set pool parameters
sudo ceph osd pool set mypool size 3
sudo ceph osd pool set mypool min_size 2
sudo ceph osd pool set mypool pg_autoscale_mode on

# Enable application on pool
sudo ceph osd pool application enable mypool rbd
sudo ceph osd pool application enable mypool rgw
sudo ceph osd pool application enable mypool cephfs

# List pools
sudo ceph osd pool ls
sudo ceph osd pool ls detail

# Pool statistics
sudo ceph osd pool stats
sudo ceph df

# Delete pool (requires confirmation)
sudo ceph osd pool rm mypool mypool --yes-i-really-really-mean-it
```

### Placement Group Management
```bash
# Check PG status
sudo ceph pg stat
sudo ceph pg dump

# PG autoscaling
sudo ceph osd pool autoscale-status
sudo ceph osd pool set mypool target_size_ratio 0.2

# Manual PG adjustment
sudo ceph osd pool set mypool pg_num 256
sudo ceph osd pool set mypool pgp_num 256

# PG repair
sudo ceph pg repair 1.0
sudo ceph pg deep-scrub 1.0
```

## Object Storage (RADOS Gateway)

### RGW Deployment
```bash
# Deploy RGW service
sudo ceph orch apply rgw mystore --placement="2 node1 node2" --port=8080

# Create RGW user
sudo radosgw-admin user create \
  --uid=testuser \
  --display-name="Test User" \
  --email=test@example.com \
  --access-key=ACCESS_KEY \
  --secret-key=SECRET_KEY

# List users
sudo radosgw-admin user list
sudo radosgw-admin user info --uid=testuser

# Create bucket
sudo radosgw-admin bucket create --bucket=testbucket --uid=testuser

# Set bucket quota
sudo radosgw-admin quota set --quota-scope=bucket --bucket=testbucket --max-objects=1000 --max-size=1G
sudo radosgw-admin quota enable --quota-scope=bucket --bucket=testbucket
```

### S3 API Usage
```python
# s3_client.py
import boto3
from botocore.exceptions import ClientError
import logging

class CephS3Client:
    def __init__(self, endpoint_url, access_key, secret_key):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            use_ssl=False,  # Set to True if using HTTPS
            verify=False    # Set to True for SSL verification
        )
    
    def create_bucket(self, bucket_name):
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
            logging.info(f"Bucket '{bucket_name}' created successfully")
        except ClientError as e:
            logging.error(f"Error creating bucket: {e}")
    
    def upload_file(self, file_path, bucket_name, object_key):
        try:
            self.s3_client.upload_file(file_path, bucket_name, object_key)
            logging.info(f"File '{file_path}' uploaded to '{bucket_name}/{object_key}'")
        except ClientError as e:
            logging.error(f"Error uploading file: {e}")
    
    def download_file(self, bucket_name, object_key, file_path):
        try:
            self.s3_client.download_file(bucket_name, object_key, file_path)
            logging.info(f"File downloaded to '{file_path}'")
        except ClientError as e:
            logging.error(f"Error downloading file: {e}")
    
    def list_objects(self, bucket_name):
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            return response.get('Contents', [])
        except ClientError as e:
            logging.error(f"Error listing objects: {e}")
            return []
    
    def delete_object(self, bucket_name, object_key):
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=object_key)
            logging.info(f"Object '{object_key}' deleted from '{bucket_name}'")
        except ClientError as e:
            logging.error(f"Error deleting object: {e}")

# Usage example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    client = CephS3Client(
        endpoint_url='http://192.168.1.100:8080',
        access_key='ACCESS_KEY',
        secret_key='SECRET_KEY'
    )
    
    # Create bucket
    client.create_bucket('test-bucket')
    
    # Upload file
    client.upload_file('./test-file.txt', 'test-bucket', 'files/test-file.txt')
    
    # List objects
    objects = client.list_objects('test-bucket')
    for obj in objects:
        print(f"Object: {obj['Key']}, Size: {obj['Size']}")
    
    # Download file
    client.download_file('test-bucket', 'files/test-file.txt', './downloaded-file.txt')
```

## Block Storage (RBD)

### RBD Pool and Image Management
```bash
# Create RBD pool
sudo ceph osd pool create rbd 128 128 replicated
sudo ceph osd pool application enable rbd rbd
sudo rbd pool init rbd

# Create RBD image
sudo rbd create --size 10G rbd/myimage
sudo rbd create --size 50G --object-size 8M rbd/large-image

# List images
sudo rbd ls rbd
sudo rbd info rbd/myimage

# Resize image
sudo rbd resize --size 20G rbd/myimage

# Create snapshot
sudo rbd snap create rbd/myimage@snapshot1
sudo rbd snap ls rbd/myimage

# Clone from snapshot
sudo rbd snap protect rbd/myimage@snapshot1
sudo rbd clone rbd/myimage@snapshot1 rbd/cloned-image

# Map RBD device
sudo rbd map rbd/myimage
lsblk

# Format and mount
sudo mkfs.ext4 /dev/rbd0
sudo mkdir /mnt/ceph-rbd
sudo mount /dev/rbd0 /mnt/ceph-rbd

# Unmap device
sudo umount /mnt/ceph-rbd
sudo rbd unmap /dev/rbd0
```

### Kubernetes RBD Integration
```yaml
# rbd-storageclass.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rbd-ssd
provisioner: rbd.csi.ceph.com
parameters:
  clusterID: rook-ceph
  pool: replicapool
  imageFormat: "2"
  imageFeatures: layering
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
  csi.storage.k8s.io/controller-expand-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/controller-expand-secret-namespace: rook-ceph
  csi.storage.k8s.io/node-stage-secret-name: rook-csi-rbd-node
  csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph
  csi.storage.k8s.io/fstype: ext4
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: Immediate
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: rbd-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: rbd-ssd
---
apiVersion: v1
kind: Pod
metadata:
  name: rbd-test-pod
spec:
  containers:
  - name: app
    image: nginx:latest
    volumeMounts:
    - name: rbd-storage
      mountPath: /data
  volumes:
  - name: rbd-storage
    persistentVolumeClaim:
      claimName: rbd-pvc

# Apply configuration
kubectl apply -f rbd-storageclass.yaml
```

## File System (CephFS)

### CephFS Setup
```bash
# Create CephFS pools
sudo ceph osd pool create cephfs_data 128 128
sudo ceph osd pool create cephfs_metadata 64 64

# Create CephFS
sudo ceph fs new cephfs cephfs_metadata cephfs_data

# Check filesystem status
sudo ceph fs status cephfs
sudo ceph fs ls

# Deploy MDS daemons
sudo ceph orch apply mds cephfs --placement="3 node1 node2 node3"

# Mount CephFS
sudo mkdir /mnt/cephfs
sudo mount -t ceph \
  node1:6789,node2:6789,node3:6789:/ /mnt/cephfs \
  -o name=admin,secret=$(sudo ceph auth get-key client.admin)

# Mount with fstab entry
echo "node1:6789,node2:6789,node3:6789:/ /mnt/cephfs ceph name=admin,secretfile=/etc/ceph/admin.secret,noatime,_netdev 0 2" | sudo tee -a /etc/fstab
```

### CephFS Client Authentication
```bash
# Create client user for CephFS
sudo ceph auth get-or-create client.cephfs \
  mon 'allow r' \
  mds 'allow rw' \
  osd 'allow rw pool=cephfs_data'

# Get client key
sudo ceph auth get-key client.cephfs > /etc/ceph/cephfs.secret

# Mount with specific user
sudo mount -t ceph \
  node1:6789,node2:6789,node3:6789:/ /mnt/cephfs \
  -o name=cephfs,secretfile=/etc/ceph/cephfs.secret
```

### Kubernetes CephFS Integration
```yaml
# cephfs-storageclass.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: cephfs
provisioner: cephfs.csi.ceph.com
parameters:
  clusterID: rook-ceph
  fsName: myfs
  pool: myfs-replicated
  rootPath: /volumes
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-cephfs-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
  csi.storage.k8s.io/controller-expand-secret-name: rook-csi-cephfs-provisioner
  csi.storage.k8s.io/controller-expand-secret-namespace: rook-ceph
  csi.storage.k8s.io/node-stage-secret-name: rook-csi-cephfs-node
  csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph
reclaimPolicy: Delete
allowVolumeExpansion: true
mountOptions:
  - debug
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cephfs-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  storageClassName: cephfs
```

## Monitoring and Performance

### Native Monitoring
```bash
# Cluster status
sudo ceph status
sudo ceph health detail

# Storage usage
sudo ceph df
sudo ceph osd df

# Performance statistics
sudo ceph osd perf
sudo ceph osd pool stats

# Monitor cluster in real-time
sudo ceph -w

# Check slow operations
sudo ceph daemon osd.0 dump_historic_slow_ops
sudo ceph daemon osd.0 config show | grep osd_op_complaint_time
```

### Prometheus Integration
```yaml
# prometheus-ceph.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ceph-mgr'
    static_configs:
      - targets: ['node1:9283', 'node2:9283']
    honor_labels: true
    
  - job_name: 'ceph-node-exporter'
    static_configs:
      - targets: ['node1:9100', 'node2:9100', 'node3:9100']
    
  - job_name: 'ceph-osd'
    static_configs:
      - targets: ['node1:9284', 'node2:9284', 'node3:9284']

# Enable Prometheus module
sudo ceph mgr module enable prometheus
sudo ceph config set mgr mgr/prometheus/server_addr 0.0.0.0
sudo ceph config set mgr mgr/prometheus/server_port 9283
```

### Performance Tuning
```bash
# OSD performance tuning
sudo ceph config set osd osd_max_backfills 2
sudo ceph config set osd osd_recovery_max_active 2
sudo ceph config set osd osd_recovery_op_priority 2

# Network performance
sudo ceph config set global ms_type async+posix
sudo ceph config set global ms_async_op_threads 3

# BlueStore tuning
sudo ceph config set osd bluestore_cache_size 1073741824  # 1GB
sudo ceph config set osd bluestore_cache_kv_ratio 0.2
sudo ceph config set osd bluestore_cache_meta_ratio 0.8

# Monitor performance impact
sudo ceph daemon osd.0 perf dump
sudo ceph daemon osd.0 config show | grep cache
```

## Backup and Disaster Recovery

### RBD Backup
```bash
# Export RBD image
sudo rbd export rbd/myimage /backup/myimage.img

# Import RBD image
sudo rbd import /backup/myimage.img rbd/restored-image

# Incremental backup using snapshots
sudo rbd snap create rbd/myimage@backup-$(date +%Y%m%d)
sudo rbd export-diff rbd/myimage@backup-$(date +%Y%m%d) /backup/incremental-$(date +%Y%m%d).diff

# Restore incremental backup
sudo rbd import-diff /backup/incremental-$(date +%Y%m%d).diff rbd/restored-image
```

### Pool Backup Script
```bash
#!/bin/bash
# ceph-backup.sh

BACKUP_DIR="/backup/ceph"
DATE=$(date +%Y%m%d_%H%M%S)
CLUSTER_NAME="ceph"

# Create backup directory
mkdir -p "${BACKUP_DIR}/${DATE}"

# Backup cluster configuration
sudo ceph config dump > "${BACKUP_DIR}/${DATE}/cluster-config.json"
sudo ceph osd getcrushmap > "${BACKUP_DIR}/${DATE}/crushmap.bin"
sudo ceph mon getmap > "${BACKUP_DIR}/${DATE}/monmap.bin"

# Backup authentication keys
sudo ceph auth export > "${BACKUP_DIR}/${DATE}/auth-keys.txt"

# Backup pool information
sudo ceph osd pool ls detail > "${BACKUP_DIR}/${DATE}/pools.txt"
sudo ceph pg dump > "${BACKUP_DIR}/${DATE}/pg-dump.json"

# Backup RBD images
for pool in $(sudo ceph osd pool ls | grep rbd); do
    mkdir -p "${BACKUP_DIR}/${DATE}/rbd/${pool}"
    for image in $(sudo rbd ls ${pool}); do
        echo "Backing up RBD image: ${pool}/${image}"
        sudo rbd export ${pool}/${image} "${BACKUP_DIR}/${DATE}/rbd/${pool}/${image}.img"
    done
done

# Create tarball
tar -czf "${BACKUP_DIR}/ceph-backup-${DATE}.tar.gz" -C "${BACKUP_DIR}" "${DATE}"
rm -rf "${BACKUP_DIR}/${DATE}"

echo "Backup completed: ${BACKUP_DIR}/ceph-backup-${DATE}.tar.gz"
```

## Troubleshooting

### Common Issues and Solutions
```bash
# Check cluster health
sudo ceph health detail

# Fix clock skew issues
sudo ntpdate -s time.nist.gov
sudo systemctl restart ceph-mon@$(hostname)

# Repair PGs
sudo ceph pg repair <pg_id>
sudo ceph pg deep-scrub <pg_id>

# OSD troubleshooting
sudo ceph osd tree
sudo ceph osd down <osd_id>
sudo ceph osd up <osd_id>
sudo ceph osd in <osd_id>
sudo ceph osd out <osd_id>

# Remove failed OSD
sudo ceph osd down <osd_id>
sudo ceph osd out <osd_id>
sudo ceph osd rm <osd_id>
sudo ceph auth del osd.<osd_id>
sudo ceph osd crush rm osd.<osd_id>

# Monitor recovery
sudo ceph -s
sudo ceph pg stat

# Check logs
sudo journalctl -u ceph-mon@$(hostname)
sudo journalctl -u ceph-mgr@$(hostname)
sudo journalctl -u ceph-osd@*
```

### Performance Diagnostics
```bash
# I/O performance test
sudo rados bench -p rbd 60 write --no-cleanup
sudo rados bench -p rbd 60 seq
sudo rados bench -p rbd 60 rand

# RBD performance test
sudo rbd create --size 10G rbd/perftest
sudo rbd map rbd/perftest
sudo fio --name=rbd-test --ioengine=libaio --direct=1 --bs=4k --iodepth=32 --rw=randwrite --runtime=60 --filename=/dev/rbd0

# Network latency test
sudo ceph daemon osd.0 dump_ops_in_flight
sudo ceph daemon osd.0 perf dump | grep latency

# Slow request analysis
sudo ceph daemon osd.0 dump_historic_slow_ops
sudo ceph health detail | grep slow
```

### Log Analysis Script
```python
#!/usr/bin/env python3
# ceph_log_analyzer.py

import re
import sys
from collections import defaultdict, Counter
from datetime import datetime

def analyze_ceph_logs(log_file):
    """Analyze Ceph logs for common issues"""
    
    errors = Counter()
    warnings = Counter()
    slow_ops = []
    recovery_events = []
    
    with open(log_file, 'r') as f:
        for line in f:
            # Extract timestamp
            timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            timestamp = timestamp_match.group(1) if timestamp_match else 'Unknown'
            
            # Count errors and warnings
            if ' ERR ' in line:
                error_msg = re.sub(r'.*ERR\s+', '', line).strip()
                errors[error_msg] += 1
            elif ' WARN ' in line:
                warning_msg = re.sub(r'.*WARN\s+', '', line).strip()
                warnings[warning_msg] += 1
            
            # Track slow operations
            if 'slow request' in line.lower():
                slow_ops.append((timestamp, line.strip()))
            
            # Track recovery events
            if any(keyword in line.lower() for keyword in ['recovery', 'backfill', 'rebalance']):
                recovery_events.append((timestamp, line.strip()))
    
    # Generate report
    print("=== CEPH LOG ANALYSIS REPORT ===\n")
    
    print(f"TOP 10 ERRORS:")
    for error, count in errors.most_common(10):
        print(f"  {count:3d}: {error[:80]}...")
    
    print(f"\nTOP 10 WARNINGS:")
    for warning, count in warnings.most_common(10):
        print(f"  {count:3d}: {warning[:80]}...")
    
    print(f"\nSLOW OPERATIONS ({len(slow_ops)} total):")
    for timestamp, op in slow_ops[-5:]:  # Last 5
        print(f"  {timestamp}: {op[:80]}...")
    
    print(f"\nRECOVERY EVENTS ({len(recovery_events)} total):")
    for timestamp, event in recovery_events[-5:]:  # Last 5
        print(f"  {timestamp}: {event[:80]}...")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ceph_log_analyzer.py <log_file>")
        sys.exit(1)
    
    analyze_ceph_logs(sys.argv[1])
```

## Security Configuration

### User Authentication
```bash
# Create restricted user
sudo ceph auth get-or-create client.backup \
  mon 'allow r' \
  osd 'allow rwx pool=backup-pool'

# Create read-only user
sudo ceph auth get-or-create client.readonly \
  mon 'allow r' \
  osd 'allow r' \
  mds 'allow r'

# List auth entries
sudo ceph auth list

# Export user key
sudo ceph auth get client.backup > client.backup.keyring
```

### Network Security
```bash
# Configure cluster and public networks
sudo ceph config set global cluster_network 192.168.2.0/24
sudo ceph config set global public_network 192.168.1.0/24

# Enable message authentication
sudo ceph config set global auth_cluster_required cephx
sudo ceph config set global auth_service_required cephx
sudo ceph config set global auth_client_required cephx

# Configure encryption in transit
sudo ceph config set global ms_cluster_mode secure
sudo ceph config set global ms_service_mode secure
sudo ceph config set global ms_client_mode secure
```

## Resources

- [Ceph Documentation](https://docs.ceph.com/)
- [Ceph Architecture Guide](https://docs.ceph.com/en/latest/architecture/)
- [Cephadm Administration](https://docs.ceph.com/en/latest/cephadm/)
- [Rook Ceph Operator](https://rook.io/docs/rook/latest/ceph-storage.html)
- [Ceph Performance Tuning](https://docs.ceph.com/en/latest/rados/configuration/)
- [Ceph Troubleshooting](https://docs.ceph.com/en/latest/rados/troubleshooting/)
- [Ceph RADOS Gateway](https://docs.ceph.com/en/latest/radosgw/)
- [Ceph Block Device](https://docs.ceph.com/en/latest/rbd/)
- [Ceph File System](https://docs.ceph.com/en/latest/cephfs/)
- [Ceph Community](https://ceph.io/en/community/)