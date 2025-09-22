# Grafana

Grafana is a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources. It's most commonly used for visualizing time series data for infrastructure and application analytics.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **Grafana Tutorial for Beginners - Complete Course**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 1 hour](https://www.youtube.com/watch?v=QDqly_xhF_Y)
- **Why it's great**: Comprehensive introduction covering dashboards, alerts, and data sources

#### **Grafana Crash Course**
- **Channel**: KodeKloud
- **Link**: [YouTube - 45 minutes](https://www.youtube.com/watch?v=hZ0-yNqNpp8)
- **Why it's great**: Quick start guide with practical examples

#### **Advanced Grafana Techniques**
- **Channel**: PromLabs
- **Link**: [YouTube Playlist](https://www.youtube.com/playlist?list=PLDGkOdUX1Ujqe8z6YMDj3RPZHS0mKPdN8)
- **Why it's great**: Deep dive into advanced features by Grafana experts

### 📖 Essential Documentation

#### **Grafana Official Documentation**
- **Link**: [grafana.com/docs/](https://grafana.com/docs/)
- **Why it's great**: Comprehensive official documentation with tutorials and examples

#### **Grafana Best Practices**
- **Link**: [grafana.com/docs/grafana/latest/best-practices/](https://grafana.com/docs/grafana/latest/best-practices/)
- **Why it's great**: Official guidance on dashboard design and performance optimization

#### **Grafana Community Hub**
- **Link**: [grafana.com/grafana/dashboards/](https://grafana.com/grafana/dashboards/)
- **Why it's great**: Thousands of pre-built dashboards for common use cases

### 📝 Must-Read Blogs & Articles

#### **Grafana Blog**
- **Source**: Grafana Labs
- **Link**: [grafana.com/blog/](https://grafana.com/blog/)
- **Why it's great**: Latest features, use cases, and technical deep dives

#### **Grafana Design Principles**
- **Source**: Grafana Labs
- **Link**: [grafana.com/blog/2020/01/24/grafana-dashboard-design-principles/](https://grafana.com/blog/2020/01/24/grafana-dashboard-design-principles/)
- **Why it's great**: Essential guide to creating effective dashboards

#### **Monitoring Mixins**
- **Source**: Monitoring Mixins Community
- **Link**: [monitoring.mixins.dev](https://monitoring.mixins.dev/)
- **Why it's great**: Reusable Grafana dashboards and Prometheus alerts

### 🎓 Structured Courses

#### **Grafana Fundamentals**
- **Platform**: Grafana Education
- **Link**: [grafana.com/education/](https://grafana.com/education/)
- **Cost**: Free
- **Why it's great**: Official training with hands-on labs and certification

#### **Observability Engineering**
- **Platform**: O'Reilly
- **Link**: [learning.oreilly.com](https://learning.oreilly.com/library/view/observability-engineering/9781492076438/)
- **Cost**: Paid
- **Why it's great**: Comprehensive observability concepts including Grafana

### 🛠️ Tools & Platforms

#### **Grafana Play**
- **Link**: [play.grafana.org](https://play.grafana.org/)
- **Why it's great**: Live demo environment with sample data and dashboards

#### **Grafana Cloud**
- **Link**: [grafana.com/products/cloud/](https://grafana.com/products/cloud/)
- **Why it's great**: Hosted Grafana with generous free tier

#### **Awesome Grafana**
- **Link**: [github.com/rfmoz/grafana-dashboards](https://github.com/rfmoz/grafana-dashboards)
- **Why it's great**: Collection of useful Grafana dashboards and resources

## Overview

Grafana is a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources. It's most commonly used for visualizing time series data for infrastructure and application analytics.

### Key Features

- **Multiple data source support** including Prometheus, InfluxDB, Elasticsearch, MySQL, PostgreSQL, and more
- **Advanced visualization options** with numerous panel types and plugins
- **Alerting** with support for multiple notification channels
- **Dashboard templating** with variables for dynamic dashboards
- **Annotations** to mark events on graphs
- **User authentication and authorization** with team-based permissions
- **Plugin ecosystem** for extending functionality
- **API** for programmatic control

## Architecture Overview

### Core Components

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Frontend     │────▶│   Grafana API   │────▶│   Data Sources  │
│   (React/TS)    │     │    Server       │     │  (Prometheus,   │
└─────────────────┘     └────────┬────────┘     │   InfluxDB,     │
                                 │               │   Loki, etc.)   │
                                 ▼               └─────────────────┘
                        ┌─────────────────┐
                        │    Database     │
                        │  (SQLite/MySQL/ │
                        │   PostgreSQL)   │
                        └─────────────────┘
```

### Data Flow

1. **Query Builder**: Constructs queries based on user input
2. **Data Source Proxy**: Routes queries to appropriate data sources
3. **Transform Pipeline**: Processes and transforms query results
4. **Visualization Engine**: Renders data into selected panel types
5. **Alert Engine**: Evaluates alert rules and triggers notifications

## Installation and Configuration

### Docker Installation

```bash
# Run Grafana with Docker
docker run -d \
  --name grafana \
  -p 3000:3000 \
  -v grafana-storage:/var/lib/grafana \
  -e "GF_SECURITY_ADMIN_PASSWORD=secure-password" \
  -e "GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource" \
  grafana/grafana:latest

# Docker Compose setup
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=secure-password
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_SERVER_ROOT_URL=https://grafana.example.com
      - GF_SMTP_ENABLED=true
      - GF_SMTP_HOST=smtp.gmail.com:587
      - GF_SMTP_USER=alerts@example.com
      - GF_SMTP_PASSWORD=smtp-password
      - GF_SMTP_FROM_ADDRESS=alerts@example.com
    volumes:
      - grafana_data:/var/lib/grafana
      - ./provisioning:/etc/grafana/provisioning
    restart: unless-stopped

volumes:
  grafana_data:
EOF
```

### Kubernetes Installation with Helm

```bash
# Add Grafana Helm repository
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Install Grafana
helm install grafana grafana/grafana \
  --namespace monitoring \
  --create-namespace \
  --values values.yaml
```

Example `values.yaml`:
```yaml
adminUser: admin
adminPassword: secure-password

persistence:
  enabled: true
  storageClassName: standard
  size: 10Gi

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  ingressClassName: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - grafana.example.com
  tls:
    - secretName: grafana-tls
      hosts:
        - grafana.example.com

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        url: http://prometheus-server:80
        access: proxy
        isDefault: true
      - name: Loki
        type: loki
        url: http://loki:3100
        access: proxy
      - name: Jaeger
        type: jaeger
        url: http://jaeger-query:16686
        access: proxy

dashboardProviders:
  dashboardproviders.yaml:
    apiVersion: 1
    providers:
      - name: 'default'
        orgId: 1
        folder: ''
        type: file
        disableDeletion: false
        updateIntervalSeconds: 10
        allowUiUpdates: true
        options:
          path: /var/lib/grafana/dashboards/default

dashboards:
  default:
    kubernetes-cluster:
      gnetId: 7249
      revision: 1
      datasource: Prometheus
    node-exporter:
      gnetId: 1860
      revision: 23
      datasource: Prometheus

plugins:
  - grafana-piechart-panel
  - grafana-worldmap-panel
  - grafana-clock-panel
```

### Configuration File

```ini
# /etc/grafana/grafana.ini
[server]
protocol = http
http_port = 3000
domain = grafana.example.com
root_url = %(protocol)s://%(domain)s/
enable_gzip = true

[database]
type = postgres
host = postgres:5432
name = grafana
user = grafana
password = secure-password
ssl_mode = require

[security]
admin_user = admin
admin_password = secure-password
secret_key = SW2YcwTIb9zpOOhoPsMm
disable_gravatar = true
cookie_secure = true
cookie_samesite = strict
allow_embedding = false

[users]
allow_sign_up = false
allow_org_create = false
auto_assign_org = true
auto_assign_org_role = Viewer
default_theme = dark

[auth]
disable_login_form = false
oauth_auto_login = false

[auth.generic_oauth]
enabled = true
name = OAuth
client_id = grafana
client_secret = oauth-secret
scopes = openid email profile
auth_url = https://auth.example.com/oauth/authorize
token_url = https://auth.example.com/oauth/token
api_url = https://auth.example.com/oauth/userinfo
allowed_domains = example.com
role_attribute_path = contains(groups[*], 'admin') && 'Admin' || contains(groups[*], 'editor') && 'Editor' || 'Viewer'

[smtp]
enabled = true
host = smtp.gmail.com:587
user = alerts@example.com
password = smtp-password
from_address = alerts@example.com
from_name = Grafana

[alerting]
enabled = true
execute_alerts = true
evaluation_timeout = 30s
notification_timeout = 30s
max_attempts = 3

[metrics]
enabled = true
interval_seconds = 10

[log]
mode = console file
level = info
filters = rendering:debug
```

## Query Language and Examples

### Prometheus Queries

```promql
# Basic CPU usage
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage percentage
100 * (1 - ((node_memory_MemAvailable_bytes) / (node_memory_MemTotal_bytes)))

# Request rate with template variables
sum(rate(http_requests_total{job="$job", instance="$instance"}[$__interval])) by (status)

# Percentile aggregation
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[$__interval])) by (le)
)
```

### InfluxDB Queries

```sql
-- InfluxQL example
SELECT mean("value") 
FROM "cpu" 
WHERE ("host" =~ /^$host$/) AND $timeFilter 
GROUP BY time($__interval), "cpu" fill(null)

-- Flux example
from(bucket: "metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "cpu")
  |> filter(fn: (r) => r["host"] =~ /${host:regex}/)
  |> aggregateWindow(every: v.windowPeriod, fn: mean)
  |> yield(name: "mean")
```

### Elasticsearch Queries

```json
{
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "$__from",
              "lte": "$__to"
            }
          }
        },
        {
          "term": {
            "kubernetes.namespace": "$namespace"
          }
        }
      ]
    }
  },
  "aggs": {
    "2": {
      "date_histogram": {
        "field": "@timestamp",
        "interval": "$__interval",
        "min_doc_count": 0
      },
      "aggs": {
        "1": {
          "avg": {
            "field": "system.cpu.total.pct"
          }
        }
      }
    }
  }
}
```

## Integration Patterns

### Data Source Configuration

#### Prometheus Integration

```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    jsonData:
      timeInterval: 15s
      queryTimeout: 60s
      httpMethod: POST
    editable: true
```

#### Multi-Datasource Queries

```javascript
// Mixed datasource panel configuration
{
  "datasource": "-- Mixed --",
  "targets": [
    {
      "datasource": "Prometheus",
      "expr": "up{job=\"node\"}",
      "refId": "A"
    },
    {
      "datasource": "Loki",
      "expr": "{job=\"syslog\"} |= \"error\"",
      "refId": "B"
    }
  ]
}
```

### Dashboard Provisioning

```yaml
# /etc/grafana/provisioning/dashboards/dashboard.yml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: 'General'
    type: file
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards

  - name: 'kubernetes'
    orgId: 1
    folder: 'Kubernetes'
    type: file
    options:
      path: /var/lib/grafana/dashboards/kubernetes

  - name: 'applications'
    orgId: 1
    folder: 'Applications'
    type: file
    options:
      path: /var/lib/grafana/dashboards/applications
```

### Alert Configuration

```yaml
# Alert rule example
apiVersion: 1
groups:
  - name: cpu_alerts
    interval: 1m
    rules:
      - uid: cpu_alert_1
        title: High CPU Usage
        condition: cpu_query
        data:
          - refId: cpu_query
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: prometheus_uid
            model:
              expr: |
                100 - (avg by (instance) 
                  (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
              interval: ""
              refId: cpu_query
        noDataState: NoData
        execErrState: Alerting
        for: 5m
        annotations:
          description: CPU usage is above 80% on {{ $labels.instance }}
          runbook_url: https://wiki.example.com/runbooks/high-cpu
          summary: High CPU usage detected
        labels:
          severity: warning
          team: platform
```

### API Integration

```bash
# Create API key
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"deployment-key", "role":"Editor", "secondsToLive":86400}' \
  http://admin:admin@localhost:3000/api/auth/keys

# Import dashboard via API
curl -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d @dashboard.json \
  http://localhost:3000/api/dashboards/db

# Create datasource
curl -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "Prometheus",
    "type": "prometheus",
    "access": "proxy",
    "url": "http://prometheus:9090",
    "basicAuth": false,
    "isDefault": true
  }' \
  http://localhost:3000/api/datasources
```

## Performance Optimization

### Query Optimization

```javascript
// Use recording rules in Prometheus
job:request_rate:5m = sum by (job) (rate(http_requests_total[5m]))

// Grafana query using the recording rule
job:request_rate:5m{job="$job"}

// Query caching configuration
[caching]
enabled = true
ttl = 60s
max_size_mb = 50

// Frontend caching
[dataproxy]
timeout = 30
keep_alive_seconds = 30
```

### Dashboard Optimization

```json
{
  "dashboard": {
    "refresh": "30s",
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "panels": [
      {
        "datasource": "Prometheus",
        "maxDataPoints": 100,
        "interval": "1m",
        "targets": [
          {
            "expr": "rate(metric[5m])",
            "step": 60,
            "intervalFactor": 2
          }
        ]
      }
    ]
  }
}
```

### Resource Configuration

```yaml
# Kubernetes resource limits
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "1"

# Database optimization
[database]
max_open_conn = 100
max_idle_conn = 100
conn_max_lifetime = 14400

# Session optimization
[session]
provider = redis
provider_config = addr=redis:6379,pool_size=100,prefix=grafana_sess:
```

## Best Practices

### 1. Dashboard Design

```json
// Use variables for flexibility
{
  "templating": {
    "list": [
      {
        "name": "datasource",
        "type": "datasource",
        "query": "prometheus",
        "refresh": 1
      },
      {
        "name": "namespace",
        "type": "query",
        "query": "label_values(kube_pod_info, namespace)",
        "refresh": 2
      },
      {
        "name": "pod",
        "type": "query",
        "query": "label_values(kube_pod_info{namespace=\"$namespace\"}, pod)",
        "refresh": 2,
        "multi": true
      }
    ]
  }
}
```

### 2. Panel Organization

```yaml
# Row-based layout for logical grouping
- title: "System Metrics"
  panels:
    - CPU Usage
    - Memory Usage
    - Disk I/O
    - Network Traffic

- title: "Application Metrics"  
  panels:
    - Request Rate
    - Error Rate
    - Response Time
    - Active Connections

- title: "Business Metrics"
  panels:
    - User Activity
    - Transaction Volume
    - Revenue Metrics
    - SLA Compliance
```

### 3. Alert Best Practices

```yaml
# Alert folder structure
alerts/
├── infrastructure/
│   ├── cpu_alerts.yaml
│   ├── memory_alerts.yaml
│   └── disk_alerts.yaml
├── application/
│   ├── availability_alerts.yaml
│   ├── performance_alerts.yaml
│   └── error_alerts.yaml
└── business/
    ├── sla_alerts.yaml
    └── revenue_alerts.yaml
```

### 4. Security Configuration

```ini
# Enable security features
[security]
admin_user = admin
admin_password = ${GF_SECURITY_ADMIN_PASSWORD}
secret_key = ${GF_SECURITY_SECRET_KEY}
disable_gravatar = true
cookie_secure = true
cookie_samesite = strict
strict_transport_security = true
strict_transport_security_max_age_seconds = 86400
strict_transport_security_preload = true
strict_transport_security_subdomains = true
x_content_type_options = true
x_xss_protection = true
content_security_policy = true

[auth.proxy]
enabled = true
header_name = X-WEBAUTH-USER
header_property = username
auto_sign_up = false
sync_ttl = 60
whitelist = 192.168.1.0/24, 10.0.0.0/8
headers = Email:X-User-Email, Name:X-User-Name

[auth.basic]
enabled = false

[auth.anonymous]
enabled = false
```

## Production Deployment Patterns

### High Availability Setup

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: monitoring
spec:
  replicas: 3
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - grafana
              topologyKey: kubernetes.io/hostname
      containers:
        - name: grafana
          image: grafana/grafana:9.3.0
          ports:
            - containerPort: 3000
              name: http
          env:
            - name: GF_DATABASE_TYPE
              value: postgres
            - name: GF_DATABASE_HOST
              value: postgres:5432
            - name: GF_DATABASE_NAME
              value: grafana
            - name: GF_DATABASE_USER
              valueFrom:
                secretKeyRef:
                  name: grafana-db
                  key: username
            - name: GF_DATABASE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: grafana-db
                  key: password
            - name: GF_SESSION_PROVIDER
              value: redis
            - name: GF_SESSION_PROVIDER_CONFIG
              value: "addr=redis:6379,pool_size=100,prefix=grafana_sess:"
          resources:
            requests:
              cpu: 250m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1Gi
          livenessProbe:
            httpGet:
              path: /api/health
              port: 3000
            initialDelaySeconds: 60
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /api/health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          volumeMounts:
            - name: config
              mountPath: /etc/grafana
            - name: dashboards
              mountPath: /var/lib/grafana/dashboards
            - name: datasources
              mountPath: /etc/grafana/provisioning/datasources
            - name: notifiers
              mountPath: /etc/grafana/provisioning/notifiers
      volumes:
        - name: config
          configMap:
            name: grafana-config
        - name: dashboards
          configMap:
            name: grafana-dashboards
        - name: datasources
          secret:
            secretName: grafana-datasources
        - name: notifiers
          configMap:
            name: grafana-notifiers
```

### Load Balancer Configuration

```yaml
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: monitoring
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  selector:
    app: grafana
  ports:
    - port: 443
      targetPort: 3000
      protocol: TCP
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

### Backup and Restore

```bash
#!/bin/bash
# Backup script

BACKUP_DIR="/backup/grafana"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_CONTAINER="postgres"
GRAFANA_DATA="/var/lib/grafana"

# Backup database
docker exec $DB_CONTAINER pg_dump -U grafana grafana > $BACKUP_DIR/db_$TIMESTAMP.sql

# Backup dashboards
kubectl cp monitoring/grafana-0:$GRAFANA_DATA/dashboards $BACKUP_DIR/dashboards_$TIMESTAMP

# Backup configuration
kubectl get configmap -n monitoring grafana-config -o yaml > $BACKUP_DIR/config_$TIMESTAMP.yaml

# Compress backup
tar -czf $BACKUP_DIR/grafana_backup_$TIMESTAMP.tar.gz \
  $BACKUP_DIR/db_$TIMESTAMP.sql \
  $BACKUP_DIR/dashboards_$TIMESTAMP \
  $BACKUP_DIR/config_$TIMESTAMP.yaml

# Clean up old backups (keep last 30 days)
find $BACKUP_DIR -name "grafana_backup_*.tar.gz" -mtime +30 -delete
```

### Monitoring Grafana

```yaml
# ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: grafana
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: grafana
  endpoints:
    - port: http
      path: /metrics
      interval: 30s
```

## Comprehensive Resources

### Official Documentation
- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Grafana Tutorials](https://grafana.com/tutorials/)
- [Grafana Blog](https://grafana.com/blog/)
- [Grafana Cloud](https://grafana.com/products/cloud/)

### Books and Guides
- "Learning Grafana 7.0" by Eric Salituro
- "Grafana 8.x Observability" by Malcolm Maclean
- [Awesome Grafana](https://github.com/zuchka/awesome-grafana)
- [Grafana Best Practices Guide](https://grafana.com/docs/grafana/latest/best-practices/)

### Dashboard Resources
- [Grafana Dashboard Repository](https://grafana.com/grafana/dashboards/)
- [Prometheus Monitoring Mixins](https://monitoring.mixins.dev/)
- [Jsonnet for Grafana](https://grafana.github.io/grafonnet-lib/)
- [Grafana Dashboard Generator](https://github.com/uber/grafana-dash-gen)

### Plugins and Extensions
- [Plugin Catalog](https://grafana.com/grafana/plugins/)
- [Panel Plugins Development](https://grafana.com/docs/grafana/latest/developers/plugins/)
- [Datasource Plugin Development](https://grafana.com/docs/grafana/latest/developers/plugins/create-a-grafana-plugin/)
- [Grafana SDK](https://github.com/grafana/grafana-plugin-sdk-go)

### Community Resources
- [Grafana Community](https://community.grafana.com/)
- [Grafana Slack](https://slack.grafana.com/)
- [GrafanaCON](https://grafana.com/about/events/grafanacon/)
- [Grafana Champions Program](https://grafana.com/community/champions/)

### Training and Certification
- [Grafana University](https://grafana.com/tutorials/)
- [Grafana Fundamentals](https://grafana.com/tutorials/grafana-fundamentals/)
- [Advanced Grafana](https://grafana.com/tutorials/grafana-advanced/)
- [Grafana Cloud Training](https://grafana.com/docs/grafana-cloud/quickstart/)

### Related Tools
- [Loki](https://grafana.com/oss/loki/) - Log aggregation system
- [Tempo](https://grafana.com/oss/tempo/) - Distributed tracing backend
- [Mimir](https://grafana.com/oss/mimir/) - Scalable long-term metrics storage
- [OnCall](https://grafana.com/oss/oncall/) - On-call management
- [k6](https://k6.io/) - Load testing tool
- [Faro](https://grafana.com/oss/faro/) - Frontend observability