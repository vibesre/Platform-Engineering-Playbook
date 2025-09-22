# Loki

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **Grafana Loki Tutorial - Complete Log Aggregation Solution**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 1.5 hours](https://www.youtube.com/watch?v=h_GGd7HfKQ8)
- **Why it's great**: Comprehensive introduction to Loki with hands-on setup and configuration

#### **Loki and Promtail for Log Collection**
- **Channel**: DevOps Journey
- **Link**: [YouTube - 45 minutes](https://www.youtube.com/watch?v=CQiawXlgabQ)
- **Why it's great**: Practical guide to setting up log collection with Promtail and Loki

#### **Complete Observability Stack - Prometheus, Loki, Grafana**
- **Channel**: freeCodeCamp
- **Link**: [YouTube - 3 hours](https://www.youtube.com/watch?v=9TJx7QTrTyo)
- **Why it's great**: Full observability stack tutorial including Loki for logging

### 📖 Essential Documentation

#### **Grafana Loki Documentation**
- **Link**: [grafana.com/docs/loki](https://grafana.com/docs/loki/)
- **Why it's great**: Comprehensive official documentation with setup guides and best practices

#### **LogQL Query Language Guide**
- **Link**: [grafana.com/docs/loki/latest/logql](https://grafana.com/docs/loki/latest/logql/)
- **Why it's great**: Complete reference for LogQL syntax and advanced querying techniques

#### **Promtail Configuration Reference**
- **Link**: [grafana.com/docs/loki/latest/clients/promtail](https://grafana.com/docs/loki/latest/clients/promtail/)
- **Why it's great**: Detailed guide for configuring log shipping agent with Promtail

### 📝 Must-Read Blogs & Articles

#### **Grafana Labs Blog - Loki**
- **Source**: Grafana Labs
- **Link**: [grafana.com/blog/tag/loki](https://grafana.com/blog/tag/loki/)
- **Why it's great**: Official updates, case studies, and advanced Loki patterns

#### **Loki Best Practices and Performance**
- **Source**: Grafana Labs
- **Link**: [grafana.com/blog/2020/10/28/loki-2.0-released](https://grafana.com/blog/2020/10/28/loki-2.0-released/)
- **Why it's great**: Performance optimization and best practices for production deployments

#### **Log Aggregation with Loki vs ELK Stack**
- **Source**: Various
- **Link**: [grafana.com/blog/2019/12/16/observability-with-grafana-loki-and-jaeger](https://grafana.com/blog/2019/12/16/observability-with-grafana-loki-and-jaeger/)
- **Why it's great**: Comparative analysis and use case recommendations

### 🎓 Structured Courses

#### **Complete Grafana Course - Loki, Prometheus, Grafana**
- **Platform**: Udemy
- **Link**: [udemy.com/course/grafana-tutorial/](https://www.udemy.com/course/grafana-tutorial/)
- **Cost**: Paid
- **Why it's great**: Hands-on course covering complete observability stack including Loki

#### **Observability Engineering Course**
- **Platform**: Honeycomb.io
- **Link**: [honeycomb.io/resources/observability-engineering-course](https://honeycomb.io/resources/observability-engineering-course/)
- **Cost**: Free
- **Why it's great**: Comprehensive observability principles including log aggregation strategies

### 🛠️ Tools & Platforms

#### **Loki Helm Chart**
- **Link**: [github.com/grafana/helm-charts/tree/main/charts/loki](https://github.com/grafana/helm-charts/tree/main/charts/loki)
- **Why it's great**: Production-ready Kubernetes deployment with best practices

#### **Awesome Loki**
- **Link**: [github.com/grafana/awesome-loki](https://github.com/grafana/awesome-loki)
- **Why it's great**: Community-curated list of Loki tools, integrations, and resources

#### **Grafana Cloud Logs**
- **Link**: [grafana.com/products/cloud/logs](https://grafana.com/products/cloud/logs/)
- **Why it's great**: Managed Loki service with scalability and integration features

## Overview

Loki is a horizontally-scalable, highly-available log aggregation system inspired by Prometheus. It stores only metadata about logs and uses labels for indexing, making it cost-effective for log storage and fast for queries.

## Key Features

- **Cost-Effective**: Stores logs without full-text indexing
- **Label-Based**: Uses labels for indexing, similar to Prometheus
- **Scalable**: Horizontally scalable architecture
- **Grafana Integration**: Native integration with Grafana for visualization
- **Multi-Tenancy**: Support for multiple tenants with isolation

## Common Use Cases

### Basic Deployment with Docker
```bash
# Run Loki
docker run -d --name loki \
  -p 3100:3100 \
  grafana/loki:latest

# Run Promtail (log shipper)
docker run -d --name promtail \
  -v /var/log:/var/log:ro \
  -v $(pwd)/promtail-config.yml:/etc/promtail/config.yml \
  grafana/promtail:latest
```

### Promtail Configuration
```yaml
# promtail-config.yml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*log

  - job_name: containers
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        target_label: 'container'
      - source_labels: ['__meta_docker_container_log_stream']
        target_label: 'stream'
```

### Application Log Collection
```yaml
# Application-specific Promtail config
scrape_configs:
  - job_name: myapp
    static_configs:
      - targets:
          - localhost
        labels:
          job: myapp
          env: production
          __path__: /var/log/myapp/*.log
    pipeline_stages:
      - match:
          selector: '{job="myapp"}'
          stages:
            - json:
                expressions:
                  level: level
                  timestamp: timestamp
                  message: message
                  user_id: user_id
            - labels:
                level:
                user_id:
            - timestamp:
                source: timestamp
                format: RFC3339
```

## Kubernetes Deployment

### Loki Configuration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: loki-config
data:
  loki.yaml: |
    auth_enabled: false
    
    server:
      http_listen_port: 3100
    
    ingester:
      lifecycler:
        address: 127.0.0.1
        ring:
          kvstore:
            store: inmemory
          replication_factor: 1
    
    schema_config:
      configs:
        - from: 2020-10-24
          store: boltdb-shipper
          object_store: filesystem
          schema: v11
          index:
            prefix: index_
            period: 24h
    
    storage_config:
      boltdb_shipper:
        active_index_directory: /loki/boltdb-shipper-active
        cache_location: /loki/boltdb-shipper-cache
        shared_store: filesystem
      filesystem:
        directory: /loki/chunks
    
    limits_config:
      enforce_metric_name: false
      reject_old_samples: true
      reject_old_samples_max_age: 168h
    
    chunk_store_config:
      max_look_back_period: 0s
    
    table_manager:
      retention_deletes_enabled: false
      retention_period: 0s
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loki
spec:
  replicas: 1
  selector:
    matchLabels:
      app: loki
  template:
    metadata:
      labels:
        app: loki
    spec:
      containers:
      - name: loki
        image: grafana/loki:latest
        ports:
        - containerPort: 3100
        volumeMounts:
        - name: config
          mountPath: /etc/loki
        - name: storage
          mountPath: /loki
        command:
        - /usr/bin/loki
        - -config.file=/etc/loki/loki.yaml
      volumes:
      - name: config
        configMap:
          name: loki-config
      - name: storage
        emptyDir: {}
```

### Promtail DaemonSet
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: promtail
spec:
  selector:
    matchLabels:
      app: promtail
  template:
    metadata:
      labels:
        app: promtail
    spec:
      containers:
      - name: promtail
        image: grafana/promtail:latest
        args:
        - -config.file=/etc/promtail/config.yml
        volumeMounts:
        - name: config
          mountPath: /etc/promtail
        - name: varlog
          mountPath: /var/log
          readOnly: true
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: promtail-config
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

## Querying with LogQL

### Basic Queries
```logql
# Stream selector
{job="myapp"}

# Filter by label
{job="myapp", env="production"}

# Line filter
{job="myapp"} |= "error"
{job="myapp"} |~ "error|ERROR"

# Multiple filters
{job="myapp"} |= "error" != "timeout"

# JSON extraction
{job="myapp"} | json | level="error"

# Regular expression
{job="myapp"} | regexp "user_id=(?P<user_id>\\w+)"
```

### Aggregation Queries
```logql
# Count logs per minute
sum(count_over_time({job="myapp"}[1m]))

# Rate of errors
sum(rate({job="myapp"} |= "error" [5m]))

# Top error messages
topk(10, sum by (message) (count_over_time({job="myapp"} |= "error" [1h])))

# Percentiles of response times
quantile_over_time(0.95, {job="myapp"} | json | unwrap response_time [5m])
```

### Advanced LogQL
```logql
# Label extraction and aggregation
{job="myapp"} 
| json 
| level="error" 
| line_format "{{.timestamp}} - {{.message}}"

# Pattern parsing
{job="nginx"} 
| pattern "<method> <uri> <status>"
| status >= 400

# Metric queries
sum by (status) (
  count_over_time(
    {job="nginx"} 
    | pattern "<method> <uri> <status>"
    [5m]
  )
)
```

## Integration with Grafana

### Data Source Configuration
```json
{
  "name": "Loki",
  "type": "loki",
  "url": "http://loki:3100",
  "access": "proxy",
  "basicAuth": false,
  "jsonData": {
    "maxLines": 1000,
    "derivedFields": [
      {
        "matcherRegex": "trace_id=(\\w+)",
        "name": "TraceID",
        "url": "http://jaeger:16686/trace/${__value.raw}"
      }
    ]
  }
}
```

### Dashboard Examples
```json
{
  "dashboard": {
    "title": "Application Logs",
    "panels": [
      {
        "title": "Log Volume",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(count_over_time({job=\"myapp\"}[1h]))",
            "refId": "A"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate({job=\"myapp\"} |= \"error\" [5m]))",
            "refId": "A"
          }
        ]
      },
      {
        "title": "Recent Logs",
        "type": "logs",
        "targets": [
          {
            "expr": "{job=\"myapp\"}",
            "refId": "A"
          }
        ]
      }
    ]
  }
}
```

## Production Configuration

### High Availability Setup
```yaml
# loki-ha.yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9095

distributor:
  ring:
    kvstore:
      store: consul
      consul:
        host: consul:8500

ingester:
  lifecycler:
    ring:
      kvstore:
        store: consul
        consul:
          host: consul:8500
      replication_factor: 3
    num_tokens: 512

storage_config:
  aws:
    s3: s3://my-loki-bucket
    region: us-west-2
  boltdb_shipper:
    active_index_directory: /loki/index
    shared_store: s3

schema_config:
  configs:
  - from: 2020-10-24
    store: boltdb-shipper
    object_store: aws
    schema: v11
    index:
      prefix: loki_index_
      period: 24h
```

### Resource Limits and Retention
```yaml
limits_config:
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20
  max_label_name_length: 1024
  max_label_value_length: 4096
  max_label_names_per_series: 30
  reject_old_samples: true
  reject_old_samples_max_age: 168h
  retention_period: 744h  # 31 days

table_manager:
  retention_deletes_enabled: true
  retention_period: 744h
```

## Monitoring and Alerting

### Metrics and Health Checks
```bash
# Health check
curl http://loki:3100/ready

# Metrics
curl http://loki:3100/metrics

# Ring status
curl http://loki:3100/ring
```

### Alerting Rules
```yaml
groups:
- name: loki_alerts
  rules:
  - alert: LokiProcessTooManyRestarts
    expr: changes(process_start_time_seconds{job=~"loki"}[15m]) > 2
    for: 0m
    labels:
      severity: warning
    annotations:
      summary: Loki process too many restarts

  - alert: LokiRequestErrors
    expr: 100 * sum(rate(loki_request_duration_seconds_count{status_code=~"5.."}[1m])) by (namespace, job, route) / sum(rate(loki_request_duration_seconds_count[1m])) by (namespace, job, route) > 10
    for: 15m
    labels:
      severity: critical
    annotations:
      summary: Loki request errors
```

## Best Practices

- Use meaningful labels for efficient querying
- Avoid high cardinality labels
- Configure appropriate retention policies
- Monitor ingestion rates and storage usage
- Use structured logging when possible
- Implement log sampling for high-volume applications
- Regular backup of index and configuration

## Great Resources

- [Loki Documentation](https://grafana.com/docs/loki/) - Official comprehensive documentation
- [LogQL Guide](https://grafana.com/docs/loki/latest/logql/) - Query language reference
- [Promtail Configuration](https://grafana.com/docs/loki/latest/clients/promtail/) - Log shipping agent setup
- [Loki Helm Chart](https://github.com/grafana/helm-charts/tree/main/charts/loki) - Kubernetes deployment
- [Grafana Loki](https://github.com/grafana/loki) - Source code and issues
- [Log Aggregation Best Practices](https://grafana.com/blog/2020/10/28/loki-2.0-released/) - Design principles and patterns
- [awesome-loki](https://github.com/grafana/awesome-loki) - Community resources and tools