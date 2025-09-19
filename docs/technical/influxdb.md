# InfluxDB

## Overview

InfluxDB is a high-performance time series database designed to handle high write and query loads for metrics, events, and real-time analytics. It's purpose-built for collecting, storing, processing, and visualizing time series data from various sources including DevOps monitoring, application metrics, IoT sensors, and real-time analytics.

### Key Features

- **Purpose-built for time series** - Optimized data structures and storage engine
- **SQL-like query language** - InfluxQL for familiar querying (v1.x)
- **Flux query language** - Powerful functional data scripting language (v2.x)
- **High write throughput** - Handles millions of points per second
- **Data compression** - Efficient storage with configurable retention policies
- **Built-in HTTP API** - RESTful interface for all operations
- **Continuous queries** - Automatic data aggregation and downsampling
- **Kapacitor integration** - Stream processing and alerting

## Architecture Overview

### InfluxDB 2.x Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Telegraf/     │────▶│   InfluxDB 2.x  │◀────│ Grafana/Chronograf│
│   Collectors    │     │                 │     │   Visualization  │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                ▼                ▼                ▼
        ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
        │    TSM      │  │    Tasks    │  │  Flux Query │
        │   Engine    │  │   Engine    │  │   Engine    │
        └─────────────┘  └─────────────┘  └─────────────┘
```

### InfluxDB OSS vs Enterprise Clustering

```
OSS Single Node:
┌─────────────────┐
│   InfluxDB OSS  │
│  ┌───────────┐  │
│  │ Database  │  │
│  └───────────┘  │
└─────────────────┘

Enterprise Cluster:
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Meta Node 1   │────▶│   Meta Node 2   │────▶│   Meta Node 3   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                                 │
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Data Node 1   │     │   Data Node 2   │     │   Data Node 3   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Installation and Configuration

### Docker Installation (InfluxDB 2.x)

```bash
# Run InfluxDB 2.x
docker run -d \
  --name influxdb \
  -p 8086:8086 \
  -v influxdb2-data:/var/lib/influxdb2 \
  -v influxdb2-config:/etc/influxdb2 \
  -e DOCKER_INFLUXDB_INIT_MODE=setup \
  -e DOCKER_INFLUXDB_INIT_USERNAME=admin \
  -e DOCKER_INFLUXDB_INIT_PASSWORD=secure-password \
  -e DOCKER_INFLUXDB_INIT_ORG=myorg \
  -e DOCKER_INFLUXDB_INIT_BUCKET=mybucket \
  -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token \
  influxdb:2.7

# Docker Compose setup
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  influxdb:
    image: influxdb:2.7
    container_name: influxdb
    ports:
      - "8086:8086"
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=secure-password
      - DOCKER_INFLUXDB_INIT_ORG=platform-engineering
      - DOCKER_INFLUXDB_INIT_BUCKET=metrics
      - DOCKER_INFLUXDB_INIT_RETENTION=30d
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token
      - INFLUXD_STORAGE_CACHE_MAX_MEMORY_SIZE=2G
      - INFLUXD_STORAGE_CACHE_SNAPSHOT_MEMORY_SIZE=256M
      - INFLUXD_STORAGE_WAL_FSYNC_DELAY=100ms
    volumes:
      - influxdb_data:/var/lib/influxdb2
      - influxdb_config:/etc/influxdb2
      - ./scripts:/docker-entrypoint-initdb.d
    restart: unless-stopped

  telegraf:
    image: telegraf:latest
    container_name: telegraf
    volumes:
      - ./telegraf.conf:/etc/telegraf/telegraf.conf:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    depends_on:
      - influxdb
    restart: unless-stopped

  chronograf:
    image: chronograf:latest
    container_name: chronograf
    ports:
      - "8888:8888"
    environment:
      - INFLUXDB_URL=http://influxdb:8086
      - INFLUXDB_TOKEN=my-super-secret-auth-token
      - INFLUXDB_ORG=platform-engineering
    depends_on:
      - influxdb
    restart: unless-stopped

volumes:
  influxdb_data:
  influxdb_config:
EOF
```

### Kubernetes Installation with Helm

```bash
# Add InfluxData Helm repository
helm repo add influxdata https://helm.influxdata.com/
helm repo update

# Install InfluxDB 2.x
helm install influxdb influxdata/influxdb2 \
  --namespace monitoring \
  --create-namespace \
  --values values.yaml
```

Example `values.yaml`:
```yaml
image:
  tag: 2.7

adminUser:
  organization: platform-engineering
  bucket: metrics
  user: admin
  retention_policy: 30d
  password: secure-password
  token: my-super-secret-auth-token

persistence:
  enabled: true
  size: 100Gi
  storageClass: fast-ssd

resources:
  limits:
    cpu: 4
    memory: 8Gi
  requests:
    cpu: 2
    memory: 4Gi

ingress:
  enabled: true
  className: nginx
  hostname: influxdb.example.com
  tls: true
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod

livenessProbe:
  enabled: true
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  enabled: true
  initialDelaySeconds: 5
  periodSeconds: 10

## InfluxDB configuration
config:
  http:
    bind-address: ":8086"
    auth-enabled: true
    log-enabled: true
    write-tracing: false
    pprof-enabled: true
    pprof-auth-enabled: true
    debug-pprof-enabled: false
    https-enabled: false
  storage:
    cache-max-memory-size: 2147483648  # 2GB
    cache-snapshot-memory-size: 268435456  # 256MB
    cache-snapshot-write-cold-duration: 10m0s
    compact-full-write-cold-duration: 4h0m0s
  query:
    concurrency-limit: 10
    queue-size: 10
```

### Configuration File (InfluxDB 1.x)

```toml
# /etc/influxdb/influxdb.conf
[meta]
  dir = "/var/lib/influxdb/meta"

[data]
  dir = "/var/lib/influxdb/data"
  wal-dir = "/var/lib/influxdb/wal"
  series-id-set-cache-size = 100
  cache-max-memory-size = 1073741824  # 1GB
  cache-snapshot-memory-size = 26214400  # 25MB
  compact-full-write-cold-duration = "4h"
  max-concurrent-compactions = 0
  max-index-log-file-size = 1048576
  trace-logging-enabled = false
  query-log-enabled = true

[retention]
  enabled = true
  check-interval = "30m"

[shard-precreation]
  enabled = true
  check-interval = "10m"
  advance-period = "30m"

[http]
  enabled = true
  bind-address = ":8086"
  auth-enabled = true
  log-enabled = true
  write-tracing = false
  pprof-enabled = true
  pprof-auth-enabled = true
  debug-pprof-enabled = false
  https-enabled = false
  max-row-limit = 0
  max-connection-limit = 0
  unix-socket-enabled = false
  bind-socket = "/var/run/influxdb.sock"
  max-body-size = 25000000
  access-log-path = ""
  access-log-status-filters = []
  max-concurrent-write-limit = 0
  max-enqueued-write-limit = 0
  enqueued-write-timeout = 30000000000

[continuous_queries]
  enabled = true
  log-enabled = true
  query-stats-enabled = false
  run-interval = "1s"

[logging]
  format = "auto"
  level = "info"
  suppress-logo = false
```

## Query Language and Examples

### Flux Query Language (InfluxDB 2.x)

```flux
// Basic query
from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "cpu")
  |> filter(fn: (r) => r["_field"] == "usage_user")
  |> yield(name: "mean")

// Aggregation
from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "http_requests")
  |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
  |> yield(name: "mean")

// Join multiple measurements
cpu = from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "cpu")
  |> filter(fn: (r) => r["_field"] == "usage_user")

mem = from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "mem")
  |> filter(fn: (r) => r["_field"] == "used_percent")

join(tables: {cpu: cpu, mem: mem}, on: ["_time", "host"])
  |> map(fn: (r) => ({r with _value: r._value_cpu + r._value_mem}))
  |> yield(name: "combined")

// Moving average
from(bucket: "metrics")
  |> range(start: -24h)
  |> filter(fn: (r) => r["_measurement"] == "temperature")
  |> movingAverage(n: 10)
  |> yield(name: "moving_avg")

// Anomaly detection
from(bucket: "metrics")
  |> range(start: -7d)
  |> filter(fn: (r) => r["_measurement"] == "http_requests")
  |> aggregateWindow(every: 1h, fn: mean)
  |> movingAverage(n: 24)
  |> map(fn: (r) => ({r with 
      baseline: r._value,
      _value: r._value
  }))
  |> difference()
  |> map(fn: (r) => ({r with anomaly: math.abs(r._value) > 100}))

// Custom functions
square = (n) => n * n
  
from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "cpu")
  |> map(fn: (r) => ({r with _value: square(n: r._value)}))
```

### InfluxQL (InfluxDB 1.x)

```sql
-- Basic queries
SELECT * FROM cpu WHERE time > now() - 1h
SELECT mean("value") FROM temperature WHERE time > now() - 24h GROUP BY time(1h)
SELECT last("value") FROM memory GROUP BY "host"

-- Aggregations
SELECT mean("value"), max("value"), min("value") 
FROM cpu 
WHERE time > now() - 1h 
GROUP BY time(5m), "host"

-- Continuous queries
CREATE CONTINUOUS QUERY "cq_5m" ON "mydb"
BEGIN
  SELECT mean("value") INTO "average"."5m".:MEASUREMENT 
  FROM "raw"./.*/ 
  GROUP BY time(5m), *
END

-- Retention policies
CREATE RETENTION POLICY "one_week" ON "mydb" DURATION 7d REPLICATION 1 DEFAULT
CREATE RETENTION POLICY "one_year" ON "mydb" DURATION 52w REPLICATION 1

-- Subqueries
SELECT mean("max") FROM (
  SELECT max("value") FROM "cpu" 
  WHERE time > now() - 1d 
  GROUP BY time(1h), "host"
) WHERE time > now() - 12h GROUP BY time(1h)
```

## Integration Patterns

### Telegraf Configuration

```toml
# telegraf.conf
[global_tags]
  environment = "production"
  datacenter = "us-east-1"

[agent]
  interval = "10s"
  round_interval = true
  metric_batch_size = 1000
  metric_buffer_limit = 10000
  collection_jitter = "0s"
  flush_interval = "10s"
  flush_jitter = "0s"
  precision = "0s"
  hostname = ""
  omit_hostname = false

# Output to InfluxDB 2.x
[[outputs.influxdb_v2]]
  urls = ["http://influxdb:8086"]
  token = "my-super-secret-auth-token"
  organization = "platform-engineering"
  bucket = "metrics"
  
# Input plugins
[[inputs.cpu]]
  percpu = true
  totalcpu = true
  collect_cpu_time = false
  report_active = false

[[inputs.disk]]
  ignore_fs = ["tmpfs", "devtmpfs", "devfs", "iso9660", "overlay", "aufs", "squashfs"]

[[inputs.docker]]
  endpoint = "unix:///var/run/docker.sock"
  gather_services = false
  container_names = []
  source_tag = false
  container_name_include = []
  container_name_exclude = []
  container_state_include = ["running"]
  timeout = "5s"
  perdevice_include = ["cpu", "blkio", "network"]
  total = false

[[inputs.kubernetes]]
  url = "http://localhost:10255"
  bearer_token = "/var/run/secrets/kubernetes.io/serviceaccount/token"
  insecure_skip_verify = true

# Processors
[[processors.strings]]
  [[processors.strings.replace]]
    field_key = "*"
    old = " "
    new = "_"

[[processors.enum]]
  [[processors.enum.mapping]]
    field = "status"
    [processors.enum.mapping.value_mappings]
      200 = 1
      404 = 2
      500 = 3
```

### Kapacitor Integration

```javascript
// CPU alert task
dbrp "metrics"."autogen"

var trigger = 80
var period = 5m
var every = 30s

stream
    |from()
        .measurement('cpu')
        .groupBy('host')
    |window()
        .period(period)
        .every(every)
    |mean('usage_user')
        .as('cpu')
    |alert()
        .id('high-cpu-{{ index .Tags "host" }}')
        .message('High CPU usage on {{ index .Tags "host" }}: {{ .Level }} - {{ .Fields.cpu }}%')
        .warn(lambda: "cpu" > trigger)
        .crit(lambda: "cpu" > 90)
        .stateChangesOnly()
        .log('/var/log/kapacitor/alerts.log')
        .slack()
        .channel('#alerts')
        .pagerDuty2()
        .routingKey('YOUR_PAGERDUTY_ROUTING_KEY')
```

### Grafana Data Source

```yaml
apiVersion: 1
datasources:
  - name: InfluxDB-2
    type: influxdb
    access: proxy
    url: http://influxdb:8086
    jsonData:
      version: Flux
      organization: platform-engineering
      defaultBucket: metrics
      tlsSkipVerify: true
    secureJsonData:
      token: my-super-secret-auth-token
    
  - name: InfluxDB-1
    type: influxdb
    access: proxy
    url: http://influxdb-v1:8086
    database: metrics
    user: admin
    jsonData:
      httpMode: POST
      keepCookies: []
    secureJsonData:
      password: secure-password
```

### Client Library Examples

```python
# Python client example
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Initialize client
client = InfluxDBClient(
    url="http://localhost:8086",
    token="my-super-secret-auth-token",
    org="platform-engineering"
)

# Write data
write_api = client.write_api(write_options=SYNCHRONOUS)

# Write single point
point = Point("temperature") \
    .tag("location", "Prague") \
    .field("value", 25.3) \
    .time(datetime.utcnow())

write_api.write(bucket="metrics", record=point)

# Write multiple points
points = []
for i in range(100):
    point = Point("cpu") \
        .tag("host", f"server{i % 10}") \
        .field("usage", random.uniform(0, 100))
    points.append(point)

write_api.write(bucket="metrics", record=points)

# Query data
query_api = client.query_api()

query = '''
from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "temperature")
  |> aggregateWindow(every: 5m, fn: mean)
'''

result = query_api.query(query)
for table in result:
    for record in table.records:
        print(f"{record.get_time()}: {record.get_value()}")
```

## Performance Optimization

### Write Performance

```toml
# InfluxDB 2.x optimization settings
[storage-engine]
  cache-max-memory-size = 2147483648  # 2GB
  cache-snapshot-memory-size = 268435456  # 256MB
  cache-snapshot-write-cold-duration = "10m"
  compact-throughput = 50331648  # 48MB/s
  max-concurrent-compactions = 4
  compact-full-write-cold-duration = "4h"
  max-index-log-file-size = 1048576
  series-id-set-cache-size = 100

# Batch writing configuration
[[outputs.influxdb_v2]]
  # Batching
  metric_batch_size = 5000
  metric_buffer_limit = 50000
  
  # Timeouts
  timeout = "30s"
  
  # Retry configuration
  max_retry_interval = "30s"
  max_retry_time = "5m"
  exponential_base = 2
```

### Query Performance

```flux
// Use pushdown predicates
from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu" and r.host == "server01")
  // Filter early to reduce data processing

// Use aggregateWindow for downsampling
from(bucket: "metrics")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "temperature")
  |> aggregateWindow(every: 5m, fn: mean)
  // Reduces points before further processing

// Limit cardinality
from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "http_requests")
  |> group(columns: ["endpoint"])
  |> limit(n: 100)
```

### Storage Optimization

```bash
# Shard group duration based on retention
# Short retention (< 2 days): 1 hour
# Medium retention (< 6 months): 1 day  
# Long retention (> 6 months): 7 days

# Create optimized retention policies
influx bucket create \
  --name metrics-1w \
  --org platform-engineering \
  --retention 7d \
  --shard-group-duration 1d

influx bucket create \
  --name metrics-1y \
  --org platform-engineering \
  --retention 365d \
  --shard-group-duration 7d

# Downsampling task
influx task create --org platform-engineering --file downsample.flux
```

```flux
// downsample.flux
option task = {
    name: "Downsample to hourly",
    every: 1h,
}

from(bucket: "metrics")
    |> range(start: -task.every)
    |> filter(fn: (r) => r._measurement == "cpu" or r._measurement == "memory")
    |> aggregateWindow(every: 1h, fn: mean)
    |> to(bucket: "metrics-1y", org: "platform-engineering")
```

## Best Practices

### 1. Schema Design

```flux
// Good: Use tags for metadata, fields for values
Point("temperature")
  .tag("location", "Prague")  // Low cardinality
  .tag("sensor_id", "A001")   // Low cardinality
  .field("value", 25.3)       // Actual measurement
  .field("humidity", 65.2)    // Related measurement

// Bad: High cardinality tags
Point("temperature")
  .tag("timestamp", "2024-01-15-10:30:00")  // Don't use timestamp as tag
  .tag("uuid", "550e8400-e29b-41d4-a716")   // Avoid UUIDs as tags
  .field("value", 25.3)
```

### 2. Data Retention

```bash
#!/bin/bash
# Retention policy management

# Create tiered retention
influx bucket create --name raw --retention 24h
influx bucket create --name aggregated-5m --retention 7d
influx bucket create --name aggregated-1h --retention 30d
influx bucket create --name aggregated-1d --retention 365d

# Create downsampling tasks
cat > downsample-5m.flux <<EOF
option task = {name: "downsample-5m", every: 5m}

from(bucket: "raw")
    |> range(start: -5m)
    |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
    |> to(bucket: "aggregated-5m")
EOF

influx task create --file downsample-5m.flux
```

### 3. Security Configuration

```yaml
# Configure authentication and authorization
---
apiVersion: v1
kind: Secret
metadata:
  name: influxdb-auth
type: Opaque
stringData:
  admin-token: "my-super-secret-auth-token"
  admin-password: "secure-password"
  
---
# Create read-only user for Grafana
influx auth create \
  --org platform-engineering \
  --description "Grafana read-only access" \
  --read-bucket metrics \
  --read-dashboards \
  --read-tasks

# Create write-only token for Telegraf
influx auth create \
  --org platform-engineering \
  --description "Telegraf write access" \
  --write-bucket metrics
```

### 4. Monitoring InfluxDB

```flux
// Monitor cardinality
import "influxdata/influxdb/v1"

v1.cardinality(
    bucket: "metrics",
    start: -1h,
    predicate: (r) => true,
)

// Monitor query performance
from(bucket: "_monitoring")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "query_log")
    |> filter(fn: (r) => r._field == "responseSize" or r._field == "compileTime" or r._field == "executeTime")
    |> aggregateWindow(every: 5m, fn: mean)

// Monitor storage metrics
from(bucket: "_monitoring")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "storage_shard_disk_size" or r._measurement == "storage_cache_size")
    |> last()
```

## Production Deployment Patterns

### High Availability Setup (Enterprise)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: influxdb-meta-config
data:
  influxdb-meta.conf: |
    [meta]
    dir = "/var/lib/influxdb/meta"
    
    [enterprise]
    license-key = "YOUR_LICENSE_KEY"
    license-path = "/etc/influxdb/license.json"
    
    [coordinator]
    write-timeout = "10s"
    max-concurrent-queries = 0
    query-timeout = "0s"
    log-queries-after = "0s"
    
    [raft]
    election-timeout = "1s"
    heartbeat-timeout = "1s"
    leader-lease-timeout = "500ms"
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: influxdb-meta
spec:
  serviceName: influxdb-meta
  replicas: 3
  selector:
    matchLabels:
      app: influxdb-meta
  template:
    metadata:
      labels:
        app: influxdb-meta
    spec:
      containers:
      - name: influxdb-meta
        image: influxdb:1.8-meta
        ports:
        - containerPort: 8091
          name: meta
        - containerPort: 8089
          name: raft
        volumeMounts:
        - name: config
          mountPath: /etc/influxdb
        - name: data
          mountPath: /var/lib/influxdb
        env:
        - name: INFLUXDB_ENTERPRISE_LICENSE_KEY
          valueFrom:
            secretKeyRef:
              name: influxdb-license
              key: license-key
      volumes:
      - name: config
        configMap:
          name: influxdb-meta-config
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: influxdb-data
spec:
  serviceName: influxdb-data
  replicas: 3
  selector:
    matchLabels:
      app: influxdb-data
  template:
    metadata:
      labels:
        app: influxdb-data
    spec:
      containers:
      - name: influxdb-data
        image: influxdb:1.8-data
        ports:
        - containerPort: 8086
          name: api
        - containerPort: 8088
          name: rpc
        volumeMounts:
        - name: data
          mountPath: /var/lib/influxdb
        env:
        - name: INFLUXDB_META_BIND_ADDRESS
          value: "influxdb-meta:8091"
        resources:
          requests:
            memory: 4Gi
            cpu: 2
          limits:
            memory: 8Gi
            cpu: 4
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 500Gi
```

### Backup and Restore

```bash
#!/bin/bash
# Backup script for InfluxDB 2.x

BACKUP_DIR="/backup/influxdb"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
INFLUX_HOST="http://localhost:8086"
INFLUX_TOKEN="my-super-secret-auth-token"

# Create backup
influx backup $BACKUP_DIR/backup_$TIMESTAMP \
  --host $INFLUX_HOST \
  --token $INFLUX_TOKEN

# Backup to S3
aws s3 sync $BACKUP_DIR/backup_$TIMESTAMP s3://my-bucket/influxdb-backups/backup_$TIMESTAMP

# Restore from backup
influx restore $BACKUP_DIR/backup_$TIMESTAMP \
  --host $INFLUX_HOST \
  --token $INFLUX_TOKEN \
  --full

# Continuous backup with retention
cat > /etc/cron.d/influxdb-backup <<EOF
0 2 * * * root /usr/local/bin/influx-backup.sh
0 3 * * * root find /backup/influxdb -name "backup_*" -mtime +7 -delete
EOF
```

### Load Balancing Configuration

```yaml
apiVersion: v1
kind: Service
metadata:
  name: influxdb-lb
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  type: LoadBalancer
  selector:
    app: influxdb-data
  ports:
  - port: 8086
    targetPort: 8086
    protocol: TCP
  sessionAffinity: ClientIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: influxdb
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "32m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "600"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - influxdb.example.com
    secretName: influxdb-tls
  rules:
  - host: influxdb.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: influxdb-lb
            port:
              number: 8086
```

## Comprehensive Resources

### Official Documentation
- [InfluxDB Documentation](https://docs.influxdata.com/)
- [Flux Language Documentation](https://docs.influxdata.com/flux/)
- [InfluxDB University](https://university.influxdata.com/)
- [InfluxDB Cloud](https://www.influxdata.com/products/influxdb-cloud/)

### Books and Guides
- "Getting Started with InfluxDB" by InfluxData
- "Time Series Databases: New Ways to Store and Access Data" by Ted Dunning
- [InfluxDB Best Practices](https://docs.influxdata.com/influxdb/v2/write-data/best-practices/)
- [Schema Design Guide](https://docs.influxdata.com/influxdb/v2/write-data/best-practices/schema-design/)

### Tools and Ecosystem
- [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) - Data collection agent
- [Chronograf](https://www.influxdata.com/time-series-platform/chronograf/) - Visualization interface
- [Kapacitor](https://www.influxdata.com/time-series-platform/kapacitor/) - Real-time streaming data processing
- [Flux](https://www.influxdata.com/products/flux/) - Data scripting language
- [InfluxDB Templates](https://github.com/influxdata/community-templates) - Pre-built dashboards and configurations

### Community Resources
- [InfluxData Community](https://community.influxdata.com/)
- [InfluxDB Slack](https://influxdata.com/slack)
- [GitHub Discussions](https://github.com/influxdata/influxdb/discussions)
- [InfluxDays Conference](https://www.influxdays.com/)

### Client Libraries
- [Python Client](https://github.com/influxdata/influxdb-client-python)
- [Go Client](https://github.com/influxdata/influxdb-client-go)
- [Java Client](https://github.com/influxdata/influxdb-client-java)
- [JavaScript Client](https://github.com/influxdata/influxdb-client-js)
- [Ruby Client](https://github.com/influxdata/influxdb-client-ruby)
- [PHP Client](https://github.com/influxdata/influxdb-client-php)

### Migration and Compatibility
- [Migrating from 1.x to 2.x](https://docs.influxdata.com/influxdb/v2/upgrade/v1-to-v2/)
- [InfluxQL to Flux Guide](https://docs.influxdata.com/influxdb/v2/query-data/influxql/)
- [Prometheus Remote Write](https://docs.influxdata.com/influxdb/v2/write-data/developer-tools/prometheus/)
- [Graphite Protocol Support](https://docs.influxdata.com/influxdb/v1/supported_protocols/graphite/)

### Performance Resources
- [Hardware Sizing Guidelines](https://docs.influxdata.com/influxdb/v2/install/requirements/)
- [Query Performance Tuning](https://docs.influxdata.com/influxdb/v2/query-data/optimize-queries/)
- [Write Performance Best Practices](https://docs.influxdata.com/influxdb/v2/write-data/best-practices/optimize-writes/)
- [Cardinality Management](https://docs.influxdata.com/influxdb/v2/reference/glossary/#cardinality)