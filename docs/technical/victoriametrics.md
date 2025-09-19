# VictoriaMetrics

## Overview

VictoriaMetrics is a fast, cost-effective, and scalable monitoring solution and time series database. It's designed as a long-term storage solution for Prometheus and supports PromQL for querying. VictoriaMetrics can be used as a drop-in replacement for Prometheus in many cases while providing better compression, higher ingestion rates, and lower resource usage.

### Key Features

- **High performance** - Handles millions of metrics per second on a single node
- **Cost-effective** - Up to 70x better compression than Prometheus
- **PromQL compatible** - Works with existing Grafana dashboards and queries
- **Multi-tenancy** - Built-in support for multiple isolated tenants
- **Global query view** - Query across multiple Prometheus instances
- **Downsampling** - Automatic retention policies with different resolutions
- **High availability** - Replication and clustering support
- **Multiple protocols** - Supports Prometheus, InfluxDB, Graphite, OpenTSDB

## Architecture Overview

### Single-Node Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Prometheus    │────▶│ VictoriaMetrics │◀────│    Grafana      │
│   Remote Write  │     │   Single Node   │     │     Queries     │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Local Storage  │
                        │  (Time Series)   │
                        └─────────────────┘
```

### Cluster Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    vminsert     │     │    vminsert     │     │    vminsert     │
│  (Ingestion)    │     │  (Ingestion)    │     │  (Ingestion)    │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                                 │
         ┌───────────────────────┴───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   vmstorage     │     │   vmstorage     │     │   vmstorage     │
│   (Storage)     │     │   (Storage)     │     │   (Storage)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                                 │
┌─────────────────┐     ┌────────┴────────┐     ┌─────────────────┐
│    vmselect     │     │    vmselect     │     │    vmselect     │
│    (Query)      │     │    (Query)      │     │    (Query)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Installation and Configuration

### Single-Node Docker Installation

```bash
# Run VictoriaMetrics single node
docker run -d \
  --name victoriametrics \
  -p 8428:8428 \
  -v vm-data:/victoria-metrics-data \
  victoriametrics/victoria-metrics:latest \
  -storageDataPath=/victoria-metrics-data \
  -httpListenAddr=:8428 \
  -retentionPeriod=12m

# Docker Compose setup
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  victoriametrics:
    image: victoriametrics/victoria-metrics:latest
    container_name: victoriametrics
    ports:
      - "8428:8428"
    volumes:
      - vm_data:/victoria-metrics-data
    command:
      - "-storageDataPath=/victoria-metrics-data"
      - "-httpListenAddr=:8428"
      - "-retentionPeriod=12m"
      - "-memory.allowedPercent=80"
      - "-search.maxUniqueTimeseries=500000"
      - "-search.maxQueryDuration=120s"
    restart: unless-stopped

  vmagent:
    image: victoriametrics/vmagent:latest
    container_name: vmagent
    ports:
      - "8429:8429"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - vmagent_data:/vmagent-data
    command:
      - "-promscrape.config=/etc/prometheus/prometheus.yml"
      - "-remoteWrite.url=http://victoriametrics:8428/api/v1/write"
      - "-remoteWrite.maxDiskUsagePerURL=1GB"
    depends_on:
      - victoriametrics
    restart: unless-stopped

  vmalert:
    image: victoriametrics/vmalert:latest
    container_name: vmalert
    ports:
      - "8880:8880"
    volumes:
      - ./alerts:/etc/alerts
    command:
      - "-datasource.url=http://victoriametrics:8428"
      - "-notifier.url=http://alertmanager:9093"
      - "-rule=/etc/alerts/*.yml"
      - "-evaluationInterval=30s"
    depends_on:
      - victoriametrics
    restart: unless-stopped

volumes:
  vm_data:
  vmagent_data:
EOF
```

### Kubernetes Installation with Helm

```bash
# Add VictoriaMetrics Helm repository
helm repo add vm https://victoriametrics.github.io/helm-charts/
helm repo update

# Install VictoriaMetrics single node
helm install vmsingle vm/victoria-metrics-single \
  --namespace monitoring \
  --create-namespace \
  --values values-single.yaml

# Install VictoriaMetrics cluster
helm install vmcluster vm/victoria-metrics-cluster \
  --namespace monitoring \
  --create-namespace \
  --values values-cluster.yaml
```

Example `values-single.yaml`:
```yaml
server:
  retentionPeriod: 12m
  storageDataPath: /storage
  resources:
    requests:
      memory: 2Gi
      cpu: 1
    limits:
      memory: 4Gi
      cpu: 2
  persistentVolume:
    enabled: true
    size: 100Gi
    storageClass: fast-ssd
  
  extraArgs:
    memory.allowedPercent: "80"
    search.maxUniqueTimeseries: "500000"
    search.maxQueryDuration: "120s"
    search.maxPointsPerTimeseries: "100000"
    dedup.minScrapeInterval: "15s"

service:
  type: ClusterIP
  port: 8428

ingress:
  enabled: true
  ingressClassName: nginx
  hosts:
    - name: vm.example.com
      path: /
  tls:
    - secretName: vm-tls
      hosts:
        - vm.example.com

serviceMonitor:
  enabled: true
  interval: 30s
```

Example `values-cluster.yaml`:
```yaml
vmselect:
  replicaCount: 3
  resources:
    requests:
      memory: 1Gi
      cpu: 500m
    limits:
      memory: 2Gi
      cpu: 1
  extraArgs:
    search.maxQueryDuration: "120s"
    search.maxPointsPerTimeseries: "100000"
  
vminsert:
  replicaCount: 3
  resources:
    requests:
      memory: 1Gi
      cpu: 500m
    limits:
      memory: 2Gi
      cpu: 1
  extraArgs:
    maxLabelsPerTimeseries: "30"
    
vmstorage:
  replicaCount: 3
  retentionPeriod: 12m
  resources:
    requests:
      memory: 2Gi
      cpu: 1
    limits:
      memory: 4Gi
      cpu: 2
  persistentVolume:
    enabled: true
    size: 200Gi
    storageClass: fast-ssd
  extraArgs:
    dedup.minScrapeInterval: "15s"
    memory.allowedPercent: "80"
```

## Query Language and Examples

### MetricsQL Overview

MetricsQL is a PromQL-like query language with additional features:

```promql
# Basic queries (PromQL compatible)
up
http_requests_total{status="200"}
rate(http_requests_total[5m])
sum(rate(http_requests_total[5m])) by (job)

# MetricsQL extensions
# Range functions
range_avg(temperature[1h])
range_max(cpu_usage[1h])
range_min(memory_free[1h])
range_quantile(0.95, request_duration[1h])

# Transform functions
histogram_avg(rate(http_request_duration_bucket[5m]))
histogram_stddev(rate(http_request_duration_bucket[5m]))

# Rollup functions
rollup_rate(http_requests_total[5m])
rollup_increase(http_requests_total[5m])
rollup_delta(gauge_metric[5m])

# WITH expressions for query optimization
WITH (
  requests_rate = rate(http_requests_total[5m])
)
sum(requests_rate) by (job) / sum(requests_rate)
```

### Advanced Queries

```promql
# Anomaly detection using z-score
WITH (
  series_avg = avg_over_time(metric[1h]),
  series_stddev = stddev_over_time(metric[1h])
)
abs(metric - series_avg) > 3 * series_stddev

# Rate with automatic interval adjustment
rate(metric[$__interval])

# Comparing current vs previous period
WITH (
  curr = rate(metric[5m]),
  prev = rate(metric[5m] offset 1h)
)
(curr - prev) / prev * 100

# Top K time series by value change
topk_max(5, delta(metric[1h]))

# Smooth spikes and anomalies
smooth_exponential(metric, 0.3)

# Fill gaps in data
interpolate(metric)
default_rollup(metric[5m])
```

### Subqueries and Optimizations

```promql
# Subquery example - alert on rate increase
rate(http_errors_total[5m])[30m:5m] > 0.1

# Memory-efficient histogram calculations
histogram_quantile(0.95, 
  sum(increase(http_request_duration_bucket[5m])) by (le)
)

# Optimize queries with recording rules via vmalert
groups:
  - name: recording_rules
    interval: 30s
    rules:
      - record: job:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)
      
      - record: instance:cpu:rate5m
        expr: 100 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance) * 100
```

## Integration Patterns

### Prometheus Remote Write

```yaml
# prometheus.yml
remote_write:
  - url: http://victoriametrics:8428/api/v1/write
    queue_config:
      capacity: 10000
      max_shards: 200
      min_shards: 1
      max_samples_per_send: 5000
      batch_send_deadline: 5s
    metadata_config:
      send: true
      send_interval: 1m
      max_samples_per_send: 500

remote_read:
  - url: http://victoriametrics:8428/api/v1/read
```

### VMAgent Configuration

```yaml
# vmagent scrape configuration
global:
  scrape_interval: 15s
  external_labels:
    datacenter: dc1
    replica: '0'

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
    
    # Stream parsing for efficiency
    stream_parse: true
    
    # Scrape large targets
    scrape_timeout: 30s
    sample_limit: 100000

# Remote write with sharding
remote_write:
  - url: http://vminsert-0:8480/insert/0/prometheus/api/v1/write
  - url: http://vminsert-1:8480/insert/0/prometheus/api/v1/write
  - url: http://vminsert-2:8480/insert/0/prometheus/api/v1/write
```

### Multi-Tenancy Setup

```bash
# Insert data for tenant
curl -X POST http://victoriametrics:8428/insert/accountID/prometheus/api/v1/write \
  -H 'Content-Type: application/x-protobuf' \
  -H 'Content-Encoding: snappy' \
  --data-binary @metrics.pb

# Query tenant data
curl http://victoriametrics:8428/select/accountID/prometheus/api/v1/query \
  -d 'query=up'

# VMAuth configuration for multi-tenancy
users:
  - username: tenant1
    password: password1
    url_prefix: "http://vmselect:8481/select/1/prometheus"
  
  - username: tenant2
    password: password2
    url_prefix: "http://vmselect:8481/select/2/prometheus"
    max_concurrent_requests: 10
```

### Grafana Integration

```yaml
# Grafana datasource configuration
apiVersion: 1
datasources:
  - name: VictoriaMetrics
    type: prometheus
    access: proxy
    url: http://victoriametrics:8428
    jsonData:
      httpMethod: POST
      customQueryParameters: "extra_label=environment=production"
    version: 1
    editable: true
    
  - name: VictoriaMetrics-Cluster
    type: prometheus
    access: proxy
    url: http://vmselect:8481/select/0/prometheus
    jsonData:
      httpMethod: POST
    version: 1
    editable: true
```

## Performance Optimization

### Storage Optimization

```bash
# Command-line flags for optimization
-dedup.minScrapeInterval=15s    # Deduplication for HA pairs
-retentionPeriod=12m             # 12 months retention
-storageDataPath=/storage        # Fast SSD storage
-memory.allowedPercent=80        # Use 80% of available memory
-search.maxUniqueTimeseries=5000000  # Increase for large environments
-search.maxSamplesPerQuery=1e9   # Allow large queries
```

### Query Optimization

```yaml
# VMSelect tuning for cluster
extraArgs:
  search.maxConcurrentRequests: 32
  search.maxQueueDuration: 30s
  search.maxQueryDuration: 120s
  search.maxPointsPerTimeseries: 100000
  search.latencyOffset: 30s
  search.cacheDataPath: /cache
  search.cacheSizeGB: 10
```

### Downsampling Configuration

```yaml
# vmagent downsampling rules
downsample:
  - interval: 5m
    retention: 30d
    
  - interval: 1h
    retention: 180d
    
  - interval: 1d
    retention: 2y

# Applied via command line
-downsampling.period=30d:5m,180d:1h,2y:1d
```

### Resource Planning

```yaml
# Storage requirements calculation
# Storage = ingestion_rate * bytes_per_sample * retention_seconds * (1 + replication_factor)
# 
# Example:
# 1M samples/sec * 1.5 bytes/sample * 365*24*3600 sec * 2 = ~95TB/year

# Memory requirements
# Memory = active_time_series * 1KB
# 
# Example:
# 10M active series * 1KB = 10GB RAM minimum

# CPU requirements
# CPU = ingestion_rate / 100K samples per core
# 
# Example:
# 1M samples/sec / 100K = 10 CPU cores
```

## Best Practices

### 1. Data Ingestion

```yaml
# Use stream aggregation for pre-aggregation
stream_aggregation:
  - match: "cpu_usage"
    interval: 1m
    outputs: ["avg", "min", "max", "p99"]
    
  - match: "http_requests_total"
    interval: 1m
    without: ["instance"]
    outputs: ["sum", "rate"]
```

### 2. Cardinality Control

```bash
# Monitor cardinality
curl -s http://victoriametrics:8428/api/v1/status/tsdb | jq '.data.seriesCountByMetricName' | sort -rnk2 | head -20

# Label filtering at ingestion
-relabelConfig=/etc/vmagent/relabel.yml

# relabel.yml
- source_labels: [__name__]
  regex: "temp.*"
  action: drop
  
- source_labels: [env]
  regex: "dev|staging"
  action: keep
```

### 3. Backup and Restore

```bash
#!/bin/bash
# Backup script using vmbackup

BACKUP_DIR="/backup/victoriametrics"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create snapshot
vmbackup -storageDataPath=/victoria-metrics-data \
  -snapshot.createURL=http://localhost:8428/snapshot/create \
  -dst=fs:///$BACKUP_DIR/backup_$TIMESTAMP

# Restore from backup
vmrestore -src=fs:///$BACKUP_DIR/backup_$TIMESTAMP \
  -storageDataPath=/victoria-metrics-data

# S3 backup
vmbackup -storageDataPath=/victoria-metrics-data \
  -snapshot.createURL=http://localhost:8428/snapshot/create \
  -dst=s3://bucket/path/backup_$TIMESTAMP \
  -customS3Endpoint=s3.amazonaws.com
```

### 4. Monitoring VictoriaMetrics

```promql
# Key metrics to monitor
# Ingestion rate
rate(vm_rows_inserted_total[5m])

# Active time series
vm_cache_entries{type="storage/tsid"}

# Query performance
histogram_quantile(0.99, rate(vm_request_duration_seconds_bucket{path="/api/v1/query"}[5m]))

# Disk space usage
vm_data_size_bytes / vm_free_disk_space_bytes

# Memory usage
process_resident_memory_bytes / vm_available_memory_bytes
```

## Production Deployment Patterns

### High Availability Cluster

```yaml
apiVersion: v1
kind: Service
metadata:
  name: vminsert
  namespace: monitoring
spec:
  clusterIP: None
  selector:
    app: vminsert
  ports:
    - name: http
      port: 8480
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vminsert
  namespace: monitoring
spec:
  serviceName: vminsert
  replicas: 3
  selector:
    matchLabels:
      app: vminsert
  template:
    metadata:
      labels:
        app: vminsert
    spec:
      containers:
        - name: vminsert
          image: victoriametrics/vminsert:latest
          args:
            - -storageNode=vmstorage-0.vmstorage:8400
            - -storageNode=vmstorage-1.vmstorage:8400
            - -storageNode=vmstorage-2.vmstorage:8400
            - -replicationFactor=2
            - -maxLabelsPerTimeseries=30
          ports:
            - containerPort: 8480
              name: http
          resources:
            requests:
              cpu: 1
              memory: 2Gi
            limits:
              cpu: 2
              memory: 4Gi
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vmstorage
  namespace: monitoring
spec:
  serviceName: vmstorage
  replicas: 3
  selector:
    matchLabels:
      app: vmstorage
  template:
    metadata:
      labels:
        app: vmstorage
    spec:
      containers:
        - name: vmstorage
          image: victoriametrics/vmstorage:latest
          args:
            - -retentionPeriod=12m
            - -storageDataPath=/storage
            - -dedup.minScrapeInterval=15s
            - -memory.allowedPercent=80
          ports:
            - containerPort: 8482
              name: http
            - containerPort: 8400
              name: vmselect
            - containerPort: 8401
              name: vminsert
          volumeMounts:
            - name: storage
              mountPath: /storage
          resources:
            requests:
              cpu: 2
              memory: 4Gi
            limits:
              cpu: 4
              memory: 8Gi
  volumeClaimTemplates:
    - metadata:
        name: storage
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 500Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vmselect
  namespace: monitoring
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vmselect
  template:
    metadata:
      labels:
        app: vmselect
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - vmselect
              topologyKey: kubernetes.io/hostname
      containers:
        - name: vmselect
          image: victoriametrics/vmselect:latest
          args:
            - -storageNode=vmstorage-0.vmstorage:8401
            - -storageNode=vmstorage-1.vmstorage:8401
            - -storageNode=vmstorage-2.vmstorage:8401
            - -dedup.minScrapeInterval=15s
            - -search.maxQueryDuration=120s
            - -replicationFactor=2
            - -search.maxConcurrentRequests=32
          ports:
            - containerPort: 8481
              name: http
          resources:
            requests:
              cpu: 1
              memory: 2Gi
            limits:
              cpu: 2
              memory: 4Gi
```

### Load Balancing Configuration

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: victoriametrics
  namespace: monitoring
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "600"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - vm.example.com
      secretName: vm-tls
  rules:
    - host: vm.example.com
      http:
        paths:
          # Write path - load balance across vminsert
          - path: /insert
            pathType: Prefix
            backend:
              service:
                name: vminsert
                port:
                  number: 8480
          # Read path - load balance across vmselect
          - path: /select
            pathType: Prefix
            backend:
              service:
                name: vmselect
                port:
                  number: 8481
```

### Security Configuration

```yaml
# VMAuth configuration for authentication
users:
  - username: admin
    password: "admin-password-hash"
    url_prefix: "http://vmselect:8481"
    
  - bearer_token: "secret-token"
    url_prefix: "http://vmselect:8481/select/5/prometheus"

  - username: grafana
    password: "grafana-password-hash"  
    url_prefix: "http://vmselect:8481"
    max_concurrent_requests: 10

# TLS configuration
tls:
  cert_file: /etc/ssl/server.crt
  key_file: /etc/ssl/server.key
  min_version: "1.2"
  cipher_suites:
    - TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
    - TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

## Comprehensive Resources

### Official Documentation
- [VictoriaMetrics Documentation](https://docs.victoriametrics.com/)
- [MetricsQL Documentation](https://docs.victoriametrics.com/MetricsQL.html)
- [VictoriaMetrics Blog](https://victoriametrics.com/blog/)
- [VictoriaMetrics GitHub](https://github.com/VictoriaMetrics/VictoriaMetrics)

### Tools and Ecosystem
- [vmctl](https://docs.victoriametrics.com/vmctl.html) - Data migration tool
- [vmalert](https://docs.victoriametrics.com/vmalert.html) - Alerting engine
- [vmagent](https://docs.victoriametrics.com/vmagent.html) - Metrics collection agent
- [vmauth](https://docs.victoriametrics.com/vmauth.html) - Authentication proxy
- [vmbackup/vmrestore](https://docs.victoriametrics.com/vmbackup.html) - Backup tools
- [VictoriaMetrics Operator](https://docs.victoriametrics.com/operator/VictoriaMetrics-Operator.html)

### Community Resources
- [VictoriaMetrics Community](https://victoriametrics.com/community/)
- [Slack Channel](https://slack.victoriametrics.com/)
- [Telegram Community](https://t.me/VictoriaMetrics_en)
- [Google Groups](https://groups.google.com/g/victoriametrics-users)

### Performance Comparisons
- [VictoriaMetrics vs Prometheus](https://docs.victoriametrics.com/FAQ.html#what-is-the-difference-between-victoriametrics-and-prometheus)
- [Benchmark Results](https://victoriametrics.com/blog/measuring-vertical-scalability/)
- [TSBS Benchmark](https://github.com/VictoriaMetrics/VictoriaMetrics/wiki/TSBS-benchmark-results)
- [Case Studies](https://docs.victoriametrics.com/CaseStudies.html)

### Migration Guides
- [Migrating from Prometheus](https://docs.victoriametrics.com/#how-to-migrate-from-prometheus)
- [Migrating from InfluxDB](https://docs.victoriametrics.com/#how-to-migrate-from-influxdb)
- [Migrating from Graphite](https://docs.victoriametrics.com/#how-to-migrate-from-graphite)
- [Migrating from OpenTSDB](https://docs.victoriametrics.com/#how-to-migrate-from-opentsdb)

### Best Practices Guides
- [Capacity Planning](https://docs.victoriametrics.com/#capacity-planning)
- [Monitoring Best Practices](https://docs.victoriametrics.com/BestPractices.html)
- [Security Best Practices](https://docs.victoriametrics.com/#security)
- [High Availability Setup](https://docs.victoriametrics.com/Cluster-VictoriaMetrics.html#high-availability)

### Related Projects
- [VictoriaLogs](https://docs.victoriametrics.com/VictoriaLogs/) - Log management system
- [Promscale](https://github.com/timescale/promscale) - Alternative Prometheus storage
- [Thanos](https://thanos.io/) - Highly available Prometheus setup
- [Cortex](https://cortexmetrics.io/) - Horizontally scalable Prometheus
- [M3](https://m3db.io/) - Distributed time series database