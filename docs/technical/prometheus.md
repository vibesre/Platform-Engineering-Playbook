# Prometheus

## Overview

Prometheus is an open-source systems monitoring and alerting toolkit originally built at SoundCloud. It's become the de facto standard for Kubernetes monitoring and is a graduated project of the Cloud Native Computing Foundation (CNCF).

### Key Features

- **Multi-dimensional data model** with time series data identified by metric name and key/value pairs
- **PromQL** - a flexible query language to leverage this dimensionality
- **No reliance on distributed storage** - single server nodes are autonomous
- **Time series collection** via a pull model over HTTP
- **Pushing time series** supported via an intermediary gateway
- **Service discovery** or static configuration for target discovery
- **Multiple modes of graphing and dashboarding** support

## Architecture Overview

### Core Components

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Prometheus    │────▶│   Alertmanager  │────▶│  PagerDuty/     │
│     Server      │     │                 │     │  Slack/Email    │
└────────┬────────┘     └─────────────────┘     └─────────────────┘
         │
         │ Scrape
         │ Metrics
         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Application   │     │   Node          │     │   Kubernetes    │
│   Exporters     │     │   Exporters     │     │   Components    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Data Model

Prometheus stores all data as time series:
- **Metric name**: `api_http_requests_total`
- **Labels**: `method="POST", handler="/messages", status="200"`
- **Timestamp**: Unix timestamp with millisecond precision
- **Value**: Float64

Example metric:
```
api_http_requests_total{method="POST", handler="/messages", status="200"} 1027 1595255917000
```

## Installation and Configuration

### Docker Installation

```bash
# Create prometheus.yml configuration
cat > prometheus.yml <<EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

rule_files:
  - "alerts/*.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
EOF

# Run Prometheus
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v prometheus_data:/prometheus \
  prom/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --web.console.libraries=/usr/share/prometheus/console_libraries \
  --web.console.templates=/usr/share/prometheus/consoles \
  --web.enable-lifecycle
```

### Kubernetes Installation with Helm

```bash
# Add Prometheus community Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --values values.yaml
```

Example `values.yaml`:
```yaml
prometheus:
  prometheusSpec:
    retention: 30d
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: fast-ssd
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 100Gi
    resources:
      requests:
        memory: 2Gi
        cpu: 1
      limits:
        memory: 4Gi
        cpu: 2
    serviceMonitorSelectorNilUsesHelmValues: false
    podMonitorSelectorNilUsesHelmValues: false
    ruleSelectorNilUsesHelmValues: false

grafana:
  enabled: true
  adminPassword: "secure-password"
  persistence:
    enabled: true
    size: 10Gi

alertmanager:
  alertmanagerSpec:
    storage:
      volumeClaimTemplate:
        spec:
          storageClassName: standard
          resources:
            requests:
              storage: 10Gi
```

## PromQL Query Language

### Basic Queries

```promql
# Instant vector - current value
up

# Range vector - values over time
up[5m]

# Rate of increase
rate(http_requests_total[5m])

# Average request duration
avg(http_request_duration_seconds)

# 95th percentile of request durations
histogram_quantile(0.95, rate(http_request_duration_bucket[5m]))
```

### Advanced Queries

```promql
# Top 5 endpoints by request rate
topk(5, sum by (endpoint) (rate(http_requests_total[5m])))

# Alert on high error rate
rate(http_requests_total{status=~"5.."}[5m]) > 0.05

# Memory usage percentage
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

# Predict disk space in 4 hours
predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[1h], 4 * 3600) < 0

# Service availability (%)
100 * (1 - (sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))))
```

### Recording Rules

```yaml
groups:
  - name: example_recording_rules
    interval: 30s
    rules:
      - record: instance:node_cpu:rate5m
        expr: |
          100 - avg by (instance) (
            rate(node_cpu_seconds_total{mode="idle"}[5m])
          ) * 100
      
      - record: job:http_requests:rate5m
        expr: |
          sum by (job) (
            rate(http_requests_total[5m])
          )
      
      - record: job:http_request_duration:p95_5m
        expr: |
          histogram_quantile(0.95, sum by (job, le) (
            rate(http_request_duration_bucket[5m])
          ))
```

## Integration Patterns

### Service Discovery

#### Kubernetes Service Discovery

```yaml
scrape_configs:
  # Scrape all pods with prometheus.io/scrape annotation
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
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name
```

#### Consul Service Discovery

```yaml
scrape_configs:
  - job_name: 'consul'
    consul_sd_configs:
      - server: 'consul.service.consul:8500'
        services: []
    relabel_configs:
      - source_labels: [__meta_consul_service]
        target_label: job
      - source_labels: [__meta_consul_node]
        target_label: instance
      - source_labels: [__meta_consul_tags]
        regex: .*,prometheus,.*
        action: keep
```

### Alerting Rules

```yaml
groups:
  - name: example_alerts
    rules:
      - alert: HighRequestLatency
        expr: |
          histogram_quantile(0.95, sum by (job) (
            rate(http_request_duration_bucket[5m])
          )) > 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High request latency on {{ $labels.job }}"
          description: "95th percentile request latency is {{ $value }}s"
      
      - alert: HighMemoryUsage
        expr: |
          100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) > 90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value }}%"
      
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"
```

### Alertmanager Configuration

```yaml
global:
  resolve_timeout: 5m
  slack_api_url: 'YOUR_SLACK_WEBHOOK_URL'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: pagerduty-critical
    - match:
        severity: warning
      receiver: slack-warnings

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#alerts'
        title: 'Alert: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
  
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_SERVICE_KEY'
        description: '{{ .GroupLabels.alertname }}'
  
  - name: 'slack-warnings'
    slack_configs:
      - channel: '#warnings'
        send_resolved: true

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'cluster', 'service']
```

## Performance Optimization

### Storage Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    replica: '$(POD_NAME)'

# Command-line flags for optimization
storage.tsdb.retention.time: 30d
storage.tsdb.retention.size: 100GB
storage.tsdb.wal-compression: true
storage.tsdb.max-block-duration: 2h
storage.tsdb.min-block-duration: 2h
query.max-concurrency: 20
query.timeout: 2m
```

### Memory Optimization

```bash
# Calculate memory requirements
# Memory = storage.local.memory-chunks * 1024 bytes
# Recommended: 2-3x the ingestion rate in bytes

# Example for 1 million samples/second:
# 1M samples/sec * 16 bytes/sample * 3 = 48MB/sec
# For 1 hour retention in memory: 48MB * 3600 = 172GB
```

### Federation for Scaling

```yaml
# Global Prometheus configuration
scrape_configs:
  - job_name: 'federate'
    scrape_interval: 15s
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{__name__=~"job:.*"}'  # Only federate aggregated metrics
        - 'up{job=~".*"}'
    static_configs:
      - targets:
        - 'prometheus-dc1:9090'
        - 'prometheus-dc2:9090'
```

## Best Practices

### 1. Label Cardinality Management

```promql
# Monitor cardinality
prometheus_tsdb_symbol_table_size_bytes

# Find high cardinality metrics
sort_desc(sum by (__name__)({__name__=~".+"}))

# Use recording rules for high-cardinality aggregations
- record: job:http_requests:rate5m
  expr: sum by (job) (rate(http_requests_total[5m]))
```

### 2. Metric Naming Conventions

```
# Format: <namespace>_<subsystem>_<name>_<unit>

# Good examples:
http_requests_total
http_request_duration_seconds
process_cpu_seconds_total
mysql_connections_active

# Bad examples:
requests  # Missing namespace and unit
cpu_usage  # Ambiguous unit
http.requests.total  # Use underscores, not dots
```

### 3. Instrumentation Best Practices

```go
// Go example with prometheus/client_golang
var (
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )
    
    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request latency",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
)

func init() {
    prometheus.MustRegister(httpRequestsTotal, httpRequestDuration)
}
```

### 4. Alert Design Patterns

```yaml
# Use symptom-based alerts, not cause-based
- alert: HighErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    /
    sum(rate(http_requests_total[5m])) > 0.05
  for: 5m
  annotations:
    summary: "High error rate detected"
    runbook: "https://wiki.company.com/runbooks/high-error-rate"

# Include context in alerts
- alert: DiskWillFillIn4Hours
  expr: |
    predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[1h], 4*3600) < 0
  for: 15m
  labels:
    severity: warning
  annotations:
    summary: "Disk {{ $labels.device }} will fill in 4 hours"
    current_usage: "{{ $value | humanize }}B free"
```

## Production Deployment Patterns

### High Availability Setup

```yaml
# Deploy multiple Prometheus replicas
apiVersion: v1
kind: Service
metadata:
  name: prometheus
  labels:
    app: prometheus
spec:
  type: ClusterIP
  clusterIP: None  # Headless service for statefulset
  ports:
    - port: 9090
      name: web
  selector:
    app: prometheus

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: prometheus
spec:
  serviceName: prometheus
  replicas: 2
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      securityContext:
        fsGroup: 2000
        runAsUser: 1000
        runAsNonRoot: true
      containers:
        - name: prometheus
          image: prom/prometheus:v2.40.0
          args:
            - --config.file=/etc/prometheus/prometheus.yml
            - --storage.tsdb.path=/prometheus
            - --storage.tsdb.retention.time=30d
            - --storage.tsdb.retention.size=100GB
            - --web.enable-lifecycle
            - --web.enable-admin-api
          ports:
            - containerPort: 9090
              name: web
          volumeMounts:
            - name: config
              mountPath: /etc/prometheus
            - name: storage
              mountPath: /prometheus
          resources:
            requests:
              cpu: 2
              memory: 4Gi
            limits:
              cpu: 4
              memory: 8Gi
          livenessProbe:
            httpGet:
              path: /-/healthy
              port: web
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /-/ready
              port: web
            initialDelaySeconds: 30
            periodSeconds: 10
      volumes:
        - name: config
          configMap:
            name: prometheus-config
  volumeClaimTemplates:
    - metadata:
        name: storage
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 100Gi
```

### Remote Storage Integration

```yaml
# Prometheus configuration for remote write
global:
  scrape_interval: 15s

remote_write:
  - url: "http://victoriametrics:8428/api/v1/write"
    queue_config:
      capacity: 10000
      max_shards: 200
      min_shards: 1
      max_samples_per_send: 5000
      batch_send_deadline: 5s
      min_backoff: 30ms
      max_backoff: 100ms
    metadata_config:
      send: true
      send_interval: 1m

remote_read:
  - url: "http://victoriametrics:8428/api/v1/read"
    read_recent: true
```

### Security Configuration

```yaml
# Enable TLS and authentication
web:
  config:
    cert_file: /etc/prometheus/certs/cert.pem
    key_file: /etc/prometheus/certs/key.pem
    client_auth_type: RequireAndVerifyClientCert
    client_ca_file: /etc/prometheus/certs/ca.pem

# Basic authentication
basic_auth_users:
  admin: $2y$10$V2RmZ2wvZ2FzZGZhc2RmYXNkZmFzZGZhc2RmYXNkZg==

# prometheus.yml with auth
scrape_configs:
  - job_name: 'secure-endpoint'
    scheme: https
    tls_config:
      ca_file: /etc/prometheus/certs/ca.pem
      cert_file: /etc/prometheus/certs/cert.pem
      key_file: /etc/prometheus/certs/key.pem
    basic_auth:
      username: prometheus
      password_file: /etc/prometheus/password
    static_configs:
      - targets: ['secure-app:8443']
```

## Comprehensive Resources

### Official Documentation
- [Prometheus Documentation](https://prometheus.io/docs/)
- [PromQL Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Best Practices](https://prometheus.io/docs/practices/)
- [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)

### Books and Guides
- "Prometheus: Up & Running" by Brian Brazil
- "Monitoring with Prometheus" by James Turnbull
- [Robust Perception Blog](https://www.robustperception.io/blog)
- [Prometheus Monitoring: The Definitive Guide](https://devconnected.com/the-definitive-guide-to-prometheus/)

### Tools and Ecosystem
- [Grafana](https://grafana.com/) - Visualization platform
- [Thanos](https://thanos.io/) - Highly available Prometheus setup with long-term storage
- [Cortex](https://cortexmetrics.io/) - Horizontally scalable, multi-tenant Prometheus
- [VictoriaMetrics](https://victoriametrics.com/) - Fast, cost-effective time series database
- [M3](https://m3db.io/) - Uber's distributed time series database
- [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator) - Kubernetes native deployment

### Community Resources
- [Prometheus Users Mailing List](https://groups.google.com/g/prometheus-users)
- [CNCF Slack #prometheus](https://slack.cncf.io/)
- [Awesome Prometheus](https://github.com/roaldnefs/awesome-prometheus)
- [PromCon](https://promcon.io/) - The Prometheus conference

### Training and Certification
- [CNCF Prometheus Certified Associate (PCA)](https://training.linuxfoundation.org/certification/prometheus-certified-associate/)
- [Linux Foundation Training](https://training.linuxfoundation.org/training/monitoring-systems-and-services-with-prometheus/)
- [Cloud Native Computing Foundation Courses](https://www.cncf.io/certification/training/)

### Common Exporters
- [Node Exporter](https://github.com/prometheus/node_exporter) - Hardware and OS metrics
- [Blackbox Exporter](https://github.com/prometheus/blackbox_exporter) - Probe endpoints
- [MySQL Exporter](https://github.com/prometheus/mysqld_exporter) - MySQL server metrics
- [PostgreSQL Exporter](https://github.com/prometheus-community/postgres_exporter) - PostgreSQL metrics
- [Redis Exporter](https://github.com/oliver006/redis_exporter) - Redis metrics
- [Kafka Exporter](https://github.com/danielqsj/kafka_exporter) - Kafka metrics
- [JMX Exporter](https://github.com/prometheus/jmx_exporter) - Java application metrics