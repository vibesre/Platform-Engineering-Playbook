# Fluentd

## Overview

Fluentd is an open-source unified logging layer that collects, processes, and forwards log data from various sources to multiple destinations. It's essential for platform engineers to centralize log management, transform data in real-time, and ensure reliable log delivery across distributed systems.

## Key Features

- **Unified Logging**: Collect logs from multiple sources
- **Plugin Architecture**: 1000+ community plugins
- **Flexible Routing**: Route data based on tags and filters
- **Reliable Delivery**: Built-in buffering and retry mechanisms
- **JSON-based Configuration**: Easy to read and maintain

## Installation

### Docker Installation
```bash
# Create Fluentd configuration
cat > fluent.conf << EOF
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<match **>
  @type stdout
</match>
EOF

# Run Fluentd container
docker run -d \
  --name fluentd \
  -p 24224:24224 \
  -v $(pwd)/fluent.conf:/fluentd/etc/fluent.conf \
  fluent/fluentd:latest
```

### Kubernetes DaemonSet
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      serviceAccount: fluentd
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        - name: FLUENT_ELASTICSEARCH_SCHEME
          value: "http"
        resources:
          limits:
            memory: 512Mi
            cpu: 500m
          requests:
            memory: 200Mi
            cpu: 100m
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        - name: config
          mountPath: /fluentd/etc
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
      - name: config
        configMap:
          name: fluentd-config
      tolerations:
      - operator: Exists
        effect: NoSchedule
      - operator: Exists
        effect: NoExecute
```

## Configuration

### Basic Configuration
```ruby
# fluent.conf
<system>
  log_level info
</system>

# Input sources
<source>
  @type tail
  path /var/log/nginx/access.log
  pos_file /var/log/fluentd/nginx-access.log.pos
  tag nginx.access
  format nginx
</source>

<source>
  @type tail
  path /var/log/app/*.log
  pos_file /var/log/fluentd/app.log.pos
  tag app.*
  format json
  time_key timestamp
  time_format %Y-%m-%dT%H:%M:%S.%L%z
</source>

# Forward input for other Fluentd instances
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

# HTTP input for applications
<source>
  @type http
  port 9880
  bind 0.0.0.0
  body_size_limit 32m
  keepalive_timeout 10s
</source>

# Filters for data transformation
<filter nginx.access>
  @type parser
  key_name message
  reserve_data true
  <parse>
    @type nginx
  </parse>
</filter>

<filter app.**>
  @type record_transformer
  <record>
    hostname "#{Socket.gethostname}"
    environment "#{ENV['ENVIRONMENT'] || 'development'}"
  </record>
</filter>

# Output destinations
<match nginx.access>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name nginx-access
  type_name _doc
  
  <buffer>
    @type file
    path /var/log/fluentd/nginx-access-buffer
    flush_interval 10s
    chunk_limit_size 8m
    total_limit_size 512m
    retry_forever true
    retry_max_interval 30
  </buffer>
</match>

<match app.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name application-logs
  type_name _doc
  
  <buffer>
    @type file
    path /var/log/fluentd/app-buffer
    flush_interval 5s
    chunk_limit_size 8m
    total_limit_size 512m
  </buffer>
</match>
```

## Common Use Cases

### Application Log Processing
```ruby
# Application logs with structured processing
<source>
  @type tail
  path /var/log/app/application.log
  pos_file /var/log/fluentd/application.log.pos
  tag app.rails
  format multiline
  format_firstline /\d{4}-\d{2}-\d{2}/
  format1 /^(?<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(?<level>\w+)\] (?<message>.*)/
  time_format %Y-%m-%d %H:%M:%S
</source>

<filter app.rails>
  @type grep
  <regexp>
    key level
    pattern ^(WARN|ERROR|FATAL)$
  </regexp>
</filter>

<filter app.rails>
  @type record_transformer
  <record>
    service "rails-app"
    datacenter "#{ENV['DATACENTER']}"
    alert_required "${if record['level'] == 'ERROR' || record['level'] == 'FATAL'; then 'true'; else 'false'; end}"
  </record>
</filter>

<match app.rails>
  @type copy
  
  <store>
    @type elasticsearch
    host elasticsearch
    port 9200
    index_name rails-logs-%Y.%m.%d
    type_name _doc
  </store>
  
  <store>
    @type file
    path /var/log/fluentd/rails-backup
    time_slice_format %Y%m%d
    time_slice_wait 10m
    time_format %Y%m%dT%H%M%S%z
    compress gzip
  </store>
</match>
```

### Security Log Analysis
```ruby
# Security logs with threat detection
<source>
  @type tail
  path /var/log/auth.log
  pos_file /var/log/fluentd/auth.log.pos
  tag security.auth
  format syslog
</source>

<filter security.auth>
  @type parser
  key_name message
  reserve_data true
  <parse>
    @type regexp
    expression /^(?<program>\w+)(\[(?<pid>\d+)\])?: (?<details>.*)/
  </parse>
</filter>

<filter security.auth>
  @type grep
  <regexp>
    key details
    pattern (Failed password|Invalid user|authentication failure)
  </regexp>
</filter>

<filter security.auth>
  @type record_transformer
  <record>
    alert_type "security_incident"
    severity "high"
    requires_investigation "true"
  </record>
</filter>

<match security.auth>
  @type copy
  
  <store>
    @type elasticsearch
    host security-elasticsearch
    port 9200
    index_name security-logs-%Y.%m.%d
    type_name _doc
  </store>
  
  <store>
    @type http
    endpoint_url http://alertmanager:9093/api/v1/alerts
    http_method post
    serializer json
    headers {"Content-Type":"application/json"}
  </store>
</match>
```

### Multi-destination Routing
```ruby
# Route logs to different destinations based on content
<source>
  @type forward
  port 24224
</source>

# Route by log level
<match app.**>
  @type rewrite_tag_filter
  <rule>
    key level
    pattern ^ERROR$
    tag error.${tag}
  </rule>
  <rule>
    key level
    pattern ^WARN$
    tag warning.${tag}
  </rule>
  <rule>
    key level
    pattern ^INFO$
    tag info.${tag}
  </rule>
</match>

# Critical errors to immediate alerting
<match error.**>
  @type copy
  
  <store>
    @type elasticsearch
    host elasticsearch
    port 9200
    index_name error-logs-%Y.%m.%d
    type_name _doc
  </store>
  
  <store>
    @type slack
    webhook_url "#{ENV['SLACK_WEBHOOK_URL']}"
    channel "#alerts"
    username fluentd
    color danger
    message "Error in %s: %s"
    message_keys tag,message
  </store>
</match>

# Warnings to monitoring system
<match warning.**>
  @type prometheus
  <metric>
    name fluentd_warning_logs_total
    type counter
    desc Total number of warning logs
    <labels>
      service ${record['service']}
      level ${record['level']}
    </labels>
  </metric>
  
  <metric>
    name fluentd_log_entries
    type counter
    desc Total number of log entries
  </metric>
</match>

# Regular logs to standard storage
<match info.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name application-logs-%Y.%m.%d
  type_name _doc
  
  <buffer time>
    timekey 3600
    timekey_wait 600
    timekey_use_utc true
  </buffer>
</match>
```

## Plugins and Extensions

### Popular Input Plugins
```ruby
# Kafka input
<source>
  @type kafka_group
  brokers kafka1:9092,kafka2:9092
  consumer_group fluentd-consumer
  topics logs
  format json
</source>

# SQL database input
<source>
  @type sql
  host mysql
  port 3306
  database app_db
  username fluentd
  password secret
  select_interval 60s
  select_limit 500
  state_file /var/log/fluentd/sql.state
  
  <table>
    table audit_logs
    tag mysql.audit
    update_column updated_at
  </table>
</source>

# CloudWatch Logs input
<source>
  @type cloudwatch_logs
  region us-east-1
  log_group_name /aws/lambda/my-function
  log_stream_name_prefix 2023
  state_file /var/log/fluentd/cloudwatch.state
  auto_create_stream true
</source>
```

### Output Plugins
```ruby
# S3 output with compression
<match archive.**>
  @type s3
  aws_key_id "#{ENV['AWS_ACCESS_KEY_ID']}"
  aws_sec_key "#{ENV['AWS_SECRET_ACCESS_KEY']}"
  s3_bucket log-archive
  s3_region us-east-1
  path logs/year=%Y/month=%m/day=%d/
  s3_object_key_format %{path}%{time_slice}_%{index}.%{file_extension}
  time_slice_format %Y%m%d-%H
  compress gzip
  
  <buffer time>
    timekey 3600
    timekey_wait 600
    chunk_limit_size 256m
  </buffer>
  
  <format>
    @type json
  </format>
</match>

# Kafka output
<match metrics.**>
  @type kafka2
  brokers kafka1:9092,kafka2:9092
  topic_key topic
  default_topic metrics
  
  <format>
    @type json
  </format>
  
  <buffer topic>
    flush_interval 3s
  </buffer>
</match>

# InfluxDB output
<match metrics.**>
  @type influxdb
  host influxdb
  port 8086
  dbname metrics
  measurement application_metrics
  tag_keys service,environment
  
  <buffer>
    flush_interval 10s
  </buffer>
</match>
```

## Performance Optimization

### Buffer Configuration
```ruby
# Optimized buffer settings
<match **>
  @type elasticsearch
  host elasticsearch
  port 9200
  
  <buffer>
    @type file
    path /var/log/fluentd/buffer
    
    # Performance settings
    chunk_limit_size 8MB
    total_limit_size 512MB
    flush_mode interval
    flush_interval 5s
    flush_thread_count 8
    
    # Reliability settings
    retry_type exponential_backoff
    retry_wait 1s
    retry_max_interval 60s
    retry_timeout 72h
    overflow_action block
  </buffer>
</match>
```

### Worker Configuration
```ruby
# Multi-worker setup
<system>
  workers 4
  root_dir /var/log/fluentd
</system>

<worker 0-3>
  <source>
    @type forward
    port "#{24224 + worker_id}"
  </source>
</worker>
```

## Monitoring and Troubleshooting

### Monitoring Configuration
```ruby
# Built-in monitoring
<source>
  @type monitor_agent
  bind 0.0.0.0
  port 24220
  include_config false
</source>

# Prometheus metrics
<source>
  @type prometheus
  bind 0.0.0.0
  port 24231
  metrics_path /metrics
</source>

<source>
  @type prometheus_monitor
  <labels>
    host "#{Socket.gethostname}"
  </labels>
</source>

<source>
  @type prometheus_output_monitor
  <labels>
    host "#{Socket.gethostname}"
  </labels>
</source>
```

### Health Checks
```bash
# Check Fluentd status
curl http://localhost:24220/api/plugins.json

# Check buffer status
curl http://localhost:24220/api/plugins.json | jq '.plugins[] | select(.type=="output") | .buffer'

# Prometheus metrics
curl http://localhost:24231/metrics
```

## Best Practices

- Use appropriate buffer configurations for reliability and performance
- Implement proper log rotation and retention policies
- Monitor buffer queue sizes and flush rates
- Use structured logging (JSON) when possible
- Implement log sampling for high-volume applications
- Set up proper error handling and dead letter queues
- Regular monitoring of Fluentd resource usage
- Use tags consistently for routing and filtering

## Great Resources

- [Fluentd Documentation](https://docs.fluentd.org/) - Official comprehensive documentation
- [Fluentd Plugin Registry](https://www.fluentd.org/plugins) - Complete plugin directory
- [Fluentd Configuration Guide](https://docs.fluentd.org/configuration) - Configuration reference
- [Fluentd GitHub](https://github.com/fluent/fluentd) - Source code and community
- [Fluent Bit vs Fluentd](https://docs.fluentbit.io/manual/about/fluentd-and-fluent-bit) - Comparison guide
- [Fluentd Best Practices](https://docs.fluentd.org/best-practices) - Performance and reliability tips
- [Fluentd Community](https://discuss.fluentd.org/) - Forums and community support
- [Awesome Fluentd](https://github.com/fluent/awesome-fluentd) - Curated resources and examples