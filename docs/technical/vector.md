# Vector

## Overview

Vector is a high-performance observability data pipeline that collects, transforms, and routes logs, metrics, and traces. Built in Rust, it's designed for platform engineers who need reliable, fast data processing with built-in reliability features and vendor-neutral data handling.

## Key Features

- **High Performance**: Built in Rust for speed and memory safety
- **Unified Pipeline**: Handle logs, metrics, and traces in one tool
- **Reliability**: Built-in retries, buffering, and acknowledgments
- **Vendor Neutral**: No lock-in to specific vendors or formats
- **Real-time Processing**: Stream processing with complex transformations

## Installation

### Docker Installation
```bash
# Create Vector configuration
cat > vector.toml << EOF
[sources.demo_logs]
type = "demo_logs"
format = "syslog"
interval = 1

[transforms.remap_logs]
type = "remap"
inputs = ["demo_logs"]
source = '''
. = parse_syslog!(.message)
.custom_field = "processed_by_vector"
.timestamp = now()
'''

[sinks.console]
type = "console"
inputs = ["remap_logs"]
encoding.codec = "json"
EOF

# Run Vector container
docker run -d \
  --name vector \
  -p 8686:8686 \
  -v $(pwd)/vector.toml:/etc/vector/vector.toml \
  timberio/vector:latest
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: vector
  namespace: logging
spec:
  selector:
    matchLabels:
      name: vector
  template:
    metadata:
      labels:
        name: vector
    spec:
      serviceAccount: vector
      containers:
      - name: vector
        image: timberio/vector:latest
        args:
          - --config-dir
          - /etc/vector/
        env:
        - name: VECTOR_SELF_NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: VECTOR_SELF_POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: VECTOR_SELF_POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        resources:
          limits:
            memory: 512Mi
            cpu: 500m
          requests:
            memory: 256Mi
            cpu: 200m
        volumeMounts:
        - name: config
          mountPath: /etc/vector
        - name: varlog
          mountPath: /var/log
          readOnly: true
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: vector-config
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
      tolerations:
      - operator: Exists
        effect: NoSchedule
      - operator: Exists
        effect: NoExecute
```

## Configuration

### Basic Log Processing
```toml
# vector.toml
[api]
enabled = true
address = "0.0.0.0:8686"

# Data directory for buffers
data_dir = "/var/lib/vector"

# File input source
[sources.file_logs]
type = "file"
includes = ["/var/log/*.log"]
read_from = "beginning"

# Kubernetes logs source
[sources.kubernetes_logs]
type = "kubernetes_logs"
auto_partial_merge = true
extra_label_selector = "app!=vector"

# HTTP input for applications
[sources.http_logs]
type = "http"
address = "0.0.0.0:8080"
encoding = "json"

# Transform logs with VRL (Vector Remap Language)
[transforms.parse_logs]
type = "remap"
inputs = ["file_logs", "kubernetes_logs"]
source = '''
# Parse timestamp
if exists(.timestamp) {
  .timestamp = parse_timestamp!(.timestamp, "%Y-%m-%dT%H:%M:%S%.fZ")
} else {
  .timestamp = now()
}

# Parse log level
if exists(.level) {
  .level = upcase(.level)
}

# Add metadata
.processed_by = "vector"
.environment = get_env_var!("ENVIRONMENT")
.hostname = get_hostname!()

# Parse JSON logs
if is_string(.message) && starts_with(.message, "{") {
  parsed = parse_json(.message) ?? {}
  . = merge(., parsed)
}

# Extract error information
if .level == "ERROR" {
  .alert_required = true
  .severity = "high"
}
'''

# Filter sensitive data
[transforms.filter_sensitive]
type = "remap"
inputs = ["parse_logs"]
source = '''
# Remove sensitive fields
if exists(.password) { del(.password) }
if exists(.token) { del(.token) }
if exists(.api_key) { del(.api_key) }

# Mask email addresses
if exists(.email) {
  .email = replace(.email, r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "[EMAIL_MASKED]")
}

# Mask credit card numbers
if exists(.credit_card) {
  .credit_card = replace(.credit_card, r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', "[CARD_MASKED]")
}
'''

# Route logs based on content
[transforms.route_logs]
type = "route"
inputs = ["filter_sensitive"]

[transforms.route_logs.route]
error_logs = '.level == "ERROR" || .level == "FATAL"'
warning_logs = '.level == "WARN"'
info_logs = '.level == "INFO" || .level == "DEBUG"'
security_logs = 'includes(.tags, "security") || includes(.message, "authentication")'

# Elasticsearch output for regular logs
[sinks.elasticsearch_info]
type = "elasticsearch"
inputs = ["route_logs.info_logs"]
endpoints = ["http://elasticsearch:9200"]
index = "application-logs-%Y.%m.%d"
doc_type = "_doc"
compression = "gzip"

# Elasticsearch output for errors
[sinks.elasticsearch_errors]
type = "elasticsearch"
inputs = ["route_logs.error_logs"]
endpoints = ["http://elasticsearch:9200"]
index = "error-logs-%Y.%m.%d"
doc_type = "_doc"
compression = "gzip"

# Security logs to dedicated index
[sinks.elasticsearch_security]
type = "elasticsearch"
inputs = ["route_logs.security_logs"]
endpoints = ["http://elasticsearch:9200"]
index = "security-logs-%Y.%m.%d"
doc_type = "_doc"
compression = "gzip"

# S3 backup for all logs
[sinks.s3_backup]
type = "aws_s3"
inputs = ["filter_sensitive"]
bucket = "log-backup-bucket"
region = "us-east-1"
key_prefix = "logs/year=%Y/month=%m/day=%d/"
compression = "gzip"
encoding.codec = "json"

# Metrics sink
[sinks.prometheus_metrics]
type = "prometheus_exporter"
inputs = ["internal_metrics"]
address = "0.0.0.0:9598"
```

## Advanced Use Cases

### Metrics Processing
```toml
# Collect system metrics
[sources.host_metrics]
type = "host_metrics"
collectors = ["cpu", "memory", "disk", "network", "filesystem"]

# Prometheus metrics input
[sources.prometheus_metrics]
type = "prometheus_scrape"
endpoints = ["http://node-exporter:9100/metrics"]
scrape_interval_secs = 30

# Transform metrics
[transforms.enrich_metrics]
type = "remap"
inputs = ["host_metrics", "prometheus_metrics"]
source = '''
# Add common labels
.tags.environment = get_env_var!("ENVIRONMENT")
.tags.cluster = get_env_var!("CLUSTER_NAME")
.tags.region = get_env_var!("AWS_REGION")

# Convert units
if .name == "memory_used_bytes" {
  .value = .value / 1024 / 1024 / 1024  # Convert to GB
  .name = "memory_used_gb"
}

# Calculate rates
if starts_with(.name, "cpu_") {
  .tags.cpu_type = "system"
}
'''

# InfluxDB output for metrics
[sinks.influxdb_metrics]
type = "influxdb_metrics"
inputs = ["enrich_metrics"]
endpoint = "http://influxdb:8086"
database = "metrics"
namespace = "vector"

# Prometheus remote write
[sinks.prometheus_remote_write]
type = "prometheus_remote_write"
inputs = ["enrich_metrics"]
endpoint = "http://prometheus:9090/api/v1/write"
```

### Complex Log Parsing
```toml
# Parse various log formats
[transforms.parse_application_logs]
type = "remap"
inputs = ["kubernetes_logs"]
source = '''
# Parse nginx access logs
if .kubernetes.container_name == "nginx" {
  parsed = parse_regex!(.message, r'^(?P<remote_addr>[\d\.]+) - (?P<remote_user>\S+) \[(?P<time_local>[^\]]+)\] "(?P<method>\S+) (?P<request_uri>\S+) (?P<server_protocol>\S+)" (?P<status>\d+) (?P<body_bytes_sent>\d+) "(?P<http_referer>[^"]*)" "(?P<http_user_agent>[^"]*)"')
  . = merge(., parsed)
  .status = to_int(.status) ?? 0
  .body_bytes_sent = to_int(.body_bytes_sent) ?? 0
}

# Parse Apache access logs
if .kubernetes.container_name == "apache" {
  parsed = parse_common_log!(.message)
  . = merge(., parsed)
}

# Parse application JSON logs
if .kubernetes.container_name == "app" {
  if starts_with(.message, "{") {
    json_parsed = parse_json!(.message)
    . = merge(., json_parsed)
    
    # Parse stack traces
    if exists(.stack_trace) {
      .stack_trace_lines = split(.stack_trace, "\n")
      .stack_trace_count = length(.stack_trace_lines)
    }
  }
}

# GeoIP enrichment
if exists(.remote_addr) {
  geoip = get_enrichment_table_record!("geoip", { "ip": .remote_addr }) ?? {}
  .geoip = geoip
}
'''

# Sample high-volume logs
[transforms.sample_logs]
type = "sample"
inputs = ["parse_application_logs"]
rate = 10  # Keep 1 in 10 logs
exclude = '.level == "ERROR" || .level == "FATAL"'  # Never sample errors

# Aggregate logs for alerting
[transforms.aggregate_errors]
type = "aggregate"
inputs = ["parse_application_logs"]
interval = 60  # 1-minute windows

[transforms.aggregate_errors.aggregate]
field = "error_count"
function = "count"
condition = '.level == "ERROR"'

# Generate alerts for high error rates
[transforms.error_alerts]
type = "remap"
inputs = ["aggregate_errors"]
source = '''
if .error_count > 10 {
  .alert_type = "high_error_rate"
  .alert_severity = "critical"
  .alert_message = "High error rate detected: " + to_string(.error_count) + " errors in 1 minute"
}
'''
```

### Multi-destination Routing
```toml
# Intelligent routing based on log content
[transforms.intelligent_routing]
type = "route"
inputs = ["parse_logs"]

[transforms.intelligent_routing.route]
# Critical errors to immediate alerting
critical_errors = '.level == "FATAL" || (.level == "ERROR" && includes(.message, "database"))'

# Security events
security_events = 'includes(.message, "authentication") || includes(.message, "authorization") || includes(.message, "security")'

# Performance logs
performance_logs = 'exists(.response_time) || exists(.duration) || includes(.message, "performance")'

# Audit logs
audit_logs = 'includes(.tags, "audit") || .kubernetes.namespace_name == "audit"'

# Regular application logs
app_logs = 'true'  # Catch-all

# Critical error handling
[sinks.critical_alerts]
type = "http"
inputs = ["intelligent_routing.critical_errors"]
uri = "http://alertmanager:9093/api/v1/alerts"
method = "post"
encoding.codec = "json"

[sinks.slack_critical]
type = "http"
inputs = ["intelligent_routing.critical_errors"]
uri = "${SLACK_WEBHOOK_URL}"
method = "post"
encoding.codec = "json"

# Security logs to SIEM
[sinks.security_siem]
type = "splunk_hec"
inputs = ["intelligent_routing.security_events"]
endpoint = "http://splunk:8088"
token = "${SPLUNK_HEC_TOKEN}"
index = "security"
sourcetype = "application:security"

# Performance logs to specialized storage
[sinks.performance_influx]
type = "influxdb_logs"
inputs = ["intelligent_routing.performance_logs"]
endpoint = "http://influxdb:8086"
database = "performance"
measurement = "response_times"

# Audit logs with compliance requirements
[sinks.audit_s3]
type = "aws_s3"
inputs = ["intelligent_routing.audit_logs"]
bucket = "compliance-audit-logs"
region = "us-east-1"
key_prefix = "audit/year=%Y/month=%m/day=%d/hour=%H/"
compression = "gzip"
encoding.codec = "json"

# Regular logs to standard pipeline
[sinks.elasticsearch_standard]
type = "elasticsearch"
inputs = ["intelligent_routing.app_logs"]
endpoints = ["http://elasticsearch:9200"]
index = "application-logs-%Y.%m.%d"
doc_type = "_doc"
```

## Vector Remap Language (VRL)

### Common VRL Functions
```ruby
# String operations
upcase(.message)                    # Convert to uppercase
downcase(.level)                    # Convert to lowercase
trim(.user_input)                   # Remove whitespace
replace(.message, "old", "new")     # Replace text
split(.tags, ",")                   # Split string to array
join(["a", "b", "c"], "-")          # Join array to string

# Type conversions
to_string(.status_code)             # Convert to string
to_int(.response_time)              # Convert to integer
to_float(.cpu_usage)                # Convert to float
to_bool(.is_active)                 # Convert to boolean

# Date/time operations
now()                               # Current timestamp
parse_timestamp(.timestamp, "%Y-%m-%d %H:%M:%S")
format_timestamp(.timestamp, "%Y-%m-%d")

# JSON operations
parse_json(.message)                # Parse JSON string
to_json(.)                          # Convert to JSON string

# Array operations
length(.tags)                       # Get array length
push(.tags, "new_tag")              # Add to array
get(.tags, 0)                       # Get array element

# Object operations
keys(.)                             # Get object keys
values(.)                           # Get object values
has(.field)                         # Check if field exists
del(.password)                      # Delete field
merge(., {"new_field": "value"})    # Merge objects

# Conditional operations
if exists(.level) { upcase(.level) } else { "UNKNOWN" }
.priority = if .level == "ERROR" { "high" } else { "low" }

# Pattern matching
match(.message, r'error: (.+)') ?? []
includes(.message, "database")
starts_with(.path, "/api/")
ends_with(.file, ".log")
```

### Advanced VRL Examples
```ruby
# Complex log parsing and enrichment
source = '''
# Parse structured logs
if starts_with(.message, "{") {
  parsed = parse_json(.message) ?? {}
  . = merge(., parsed)
}

# Extract request ID from various formats
.request_id = (
  .request_id ??                                    # Use existing if available
  match(.message, r'request[_-]?id[=:]\s*([^\s,}]+)').[0] ??  # Extract from message
  uuid_v4()                                         # Generate new if not found
)

# Normalize log levels
.level = (
  if .level == "err" || .level == "error" { "ERROR" }
  else if .level == "warn" || .level == "warning" { "WARN" }
  else if .level == "info" || .level == "information" { "INFO" }
  else if .level == "debug" || .level == "trace" { "DEBUG" }
  else { upcase(.level) ?? "UNKNOWN" }
)

# Calculate response time category
if exists(.response_time) {
  .response_category = (
    if .response_time < 100 { "fast" }
    else if .response_time < 500 { "normal" }
    else if .response_time < 1000 { "slow" }
    else { "very_slow" }
  )
}

# Detect suspicious patterns
.is_suspicious = (
  includes(.message, "sql injection") ||
  includes(.message, "xss attack") ||
  includes(.user_agent, "sqlmap") ||
  includes(.user_agent, "nikto")
)

# Extract database query info
if includes(.message, "SELECT") || includes(.message, "INSERT") || includes(.message, "UPDATE") || includes(.message, "DELETE") {
  .query_type = (
    if includes(.message, "SELECT") { "select" }
    else if includes(.message, "INSERT") { "insert" }
    else if includes(.message, "UPDATE") { "update" }
    else if includes(.message, "DELETE") { "delete" }
    else { "unknown" }
  )
  
  # Extract table names (simplified)
  tables = match(.message, r'(?i)(?:from|into|update|join)\s+([a-zA-Z_][a-zA-Z0-9_]*)')
  .affected_tables = unique(tables)
}

# Geolocation enrichment
if exists(.client_ip) {
  geoip = get_enrichment_table_record!("geoip", { "ip": .client_ip }) ?? {}
  .geo = {
    "country": geoip.country,
    "city": geoip.city,
    "coordinates": [geoip.longitude, geoip.latitude]
  }
}
'''
```

## Monitoring and Observability

### Internal Metrics
```toml
# Vector's internal metrics
[sources.internal_metrics]
type = "internal_metrics"

# Expose metrics for Prometheus
[sinks.prometheus_internal]
type = "prometheus_exporter"
inputs = ["internal_metrics"]
address = "0.0.0.0:9598"
default_namespace = "vector"

# Log Vector's internal events
[sources.internal_logs]
type = "internal_logs"

[sinks.vector_logs]
type = "console"
inputs = ["internal_logs"]
encoding.codec = "json"
```

### Health Checks
```bash
# Health check endpoint
curl http://localhost:8686/health

# GraphQL API for introspection
curl -X POST http://localhost:8686/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ components { sources { componentType } } }"}}'

# Check component status
vector top

# Validate configuration
vector validate /etc/vector/vector.toml
```

## Best Practices

- Use VRL for efficient data transformation and filtering
- Implement proper error handling and dead letter queues
- Monitor Vector's internal metrics and performance
- Use appropriate buffer configurations for reliability
- Implement data sampling for high-volume environments
- Use enrichment tables for reference data lookups
- Regular testing of configuration changes
- Implement proper secret management for credentials

## Great Resources

- [Vector Documentation](https://vector.dev/docs/) - Official comprehensive documentation
- [Vector Remap Language](https://vector.dev/docs/reference/vrl/) - VRL language reference
- [Vector GitHub](https://github.com/vectordotdev/vector) - Source code and community
- [Vector Configuration Examples](https://github.com/vectordotdev/vector/tree/master/config/examples) - Example configurations
- [Vector Community](https://chat.vector.dev/) - Discord community support
- [Vector Blog](https://vector.dev/blog/) - Technical articles and updates
- [Vector vs Other Tools](https://vector.dev/docs/about/under-the-hood/comparison/) - Comparison with alternatives
- [Vector Performance](https://vector.dev/docs/about/under-the-hood/performance/) - Performance benchmarks and optimization