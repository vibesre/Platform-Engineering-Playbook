# etcd

## Overview

etcd is a distributed, reliable key-value store for the most critical data of a distributed system. It's the backbone of Kubernetes and many other cloud-native systems, providing strong consistency and high availability for configuration data and service discovery.

## Key Features

- **Distributed**: Built for clustering with Raft consensus algorithm
- **Consistent**: Strong consistency guarantees across all nodes
- **Reliable**: Fault-tolerant with automatic leader election
- **Fast**: Optimized for fast reads and configuration updates
- **Secure**: TLS encryption and RBAC authentication

## Common Use Cases

### Basic Key-Value Operations
```bash
# Set and get values
etcdctl put /config/database/host "postgres.example.com"
etcdctl put /config/database/port "5432"
etcdctl get /config/database/host

# Get all keys with prefix
etcdctl get /config/database/ --prefix

# Watch for changes
etcdctl watch /config/database/ --prefix
```

### Service Discovery
```bash
# Register service instances
etcdctl put /services/api/instance1 '{"host":"api1.example.com","port":8080}'
etcdctl put /services/api/instance2 '{"host":"api2.example.com","port":8080}'

# Discover services
etcdctl get /services/api/ --prefix

# Service health with TTL
etcdctl put /services/api/instance1 '{"host":"api1.example.com","port":8080}' --lease=7200
```

### Configuration Management
```bash
# Application configuration
etcdctl put /app/myservice/config '{"debug":true,"workers":4,"timeout":30}'

# Feature flags
etcdctl put /features/new_ui "enabled"
etcdctl put /features/beta_api "disabled"

# Environment-specific config
etcdctl put /env/production/database_url "postgres://prod-db:5432/myapp"
etcdctl put /env/staging/database_url "postgres://staging-db:5432/myapp"
```

## Cluster Setup

### Three-Node Cluster
```bash
# Node 1
etcd --name node1 \
  --initial-advertise-peer-urls http://10.0.0.1:2380 \
  --listen-peer-urls http://10.0.0.1:2380 \
  --advertise-client-urls http://10.0.0.1:2379 \
  --listen-client-urls http://10.0.0.1:2379 \
  --initial-cluster node1=http://10.0.0.1:2380,node2=http://10.0.0.2:2380,node3=http://10.0.0.3:2380 \
  --initial-cluster-state new

# Node 2
etcd --name node2 \
  --initial-advertise-peer-urls http://10.0.0.2:2380 \
  --listen-peer-urls http://10.0.0.2:2380 \
  --advertise-client-urls http://10.0.0.2:2379 \
  --listen-client-urls http://10.0.0.2:2379 \
  --initial-cluster node1=http://10.0.0.1:2380,node2=http://10.0.0.2:2380,node3=http://10.0.0.3:2380 \
  --initial-cluster-state new

# Node 3 (similar configuration)
```

### TLS Security
```bash
# Generate certificates and configure TLS
etcd --name node1 \
  --cert-file=/path/to/server.crt \
  --key-file=/path/to/server.key \
  --peer-cert-file=/path/to/peer.crt \
  --peer-key-file=/path/to/peer.key \
  --trusted-ca-file=/path/to/ca.crt \
  --peer-trusted-ca-file=/path/to/ca.crt \
  --client-cert-auth \
  --peer-client-cert-auth
```

## Monitoring and Maintenance

### Cluster Health
```bash
# Check cluster health
etcdctl endpoint health

# Cluster member list
etcdctl member list

# Cluster status
etcdctl endpoint status --write-out=table

# Performance metrics
etcdctl endpoint metrics
```

### Backup and Recovery
```bash
# Create snapshot backup
etcdctl snapshot save backup.db

# Verify snapshot
etcdctl snapshot status backup.db

# Restore from snapshot
etcdctl snapshot restore backup.db \
  --name node1 \
  --initial-cluster node1=http://10.0.0.1:2380 \
  --initial-advertise-peer-urls http://10.0.0.1:2380
```

### Performance Tuning
```bash
# Defragmentation
etcdctl defrag

# Compaction
etcdctl compact 1000

# Alarm management
etcdctl alarm list
etcdctl alarm disarm
```

## Best Practices

- Use odd number of nodes (3, 5, 7) for proper quorum
- Enable TLS encryption for production deployments
- Regular backups with automated snapshot creation
- Monitor cluster health and performance metrics
- Use appropriate hardware (SSD storage recommended)
- Implement proper network security and firewall rules
- Keep etcd version updated for security and performance

## Great Resources

- [etcd Official Documentation](https://etcd.io/docs/) - Comprehensive etcd guide and API reference
- [etcd Operator](https://github.com/coreos/etcd-operator) - Kubernetes operator for etcd clusters
- [etcd Play](http://play.etcd.io/) - Interactive etcd playground for learning
- [etcd Performance Benchmarking](https://etcd.io/docs/v3.5/benchmarks/) - Performance testing and optimization
- [Kubernetes and etcd](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/) - etcd in Kubernetes environments
- [etcd Learning Resources](https://etcd.io/docs/v3.5/learning/) - Official learning materials and tutorials
- [etcd-manager](https://github.com/kopeio/etcd-manager) - Tool for managing etcd clusters