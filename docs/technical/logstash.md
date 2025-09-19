# Logstash

## Overview

Logstash is a server-side data processing pipeline that ingests data from a multitude of sources simultaneously, transforms it, and then sends it to your favorite "stash." Built on the JRuby framework, Logstash is part of the Elastic Stack and excels at log parsing, transformation, and enrichment before data reaches Elasticsearch or other outputs.

## Architecture

### Core Components

#### 1. Input Plugins
- **Purpose**: Collect data from various sources
- **Types**: File, beats, kafka, HTTP, TCP, UDP, database, cloud services
- **Buffering**: Handles input buffering and backpressure

#### 2. Filter Plugins
- **Purpose**: Parse, transform, and enrich data
- **Types**: Grok, mutate, date, geoip, ruby, aggregate
- **Processing**: Pipeline-based processing with conditional logic

#### 3. Output Plugins
- **Purpose**: Send processed data to destinations
- **Types**: Elasticsearch, kafka, file, HTTP, cloud services
- **Delivery**: Supports at-least-once delivery guarantees

#### 4. Codec Plugins
- **Purpose**: Handle data serialization/deserialization
- **Types**: JSON, plain, multiline, avro, msgpack
- **Integration**: Works with input and output plugins

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Logstash Pipeline                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   INPUTS    │    │   FILTERS   │    │   OUTPUTS   │  │
│  │             │    │             │    │             │  │
│  │ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │  │
│  │ │  Beats  │ │    │ │  Grok   │ │    │ │ Elastic │ │  │
│  │ └─────────┘ │    │ └─────────┘ │    │ │ search  │ │  │
│  │ ┌─────────┐ │    │ ┌─────────┐ │    │ └─────────┘ │  │
│  │ │  Kafka  │ │───▶│ │ Mutate  │ │───▶│ ┌─────────┐ │  │
│  │ └─────────┘ │    │ └─────────┘ │    │ │  Kafka  │ │  │
│  │ ┌─────────┐ │    │ ┌─────────┐ │    │ └─────────┘ │  │
│  │ │  Files  │ │    │ │  Date   │ │    │ ┌─────────┐ │  │
│  │ └─────────┘ │    │ └─────────┘ │    │ │   S3    │ │  │
│  └─────────────┘    └─────────────┘    │ └─────────┘ │  │
│                                         └─────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Configuration Examples

### Basic Pipeline Configuration

```ruby
# /etc/logstash/conf.d/main.conf
input {
  beats {
    port => 5044
    host => "0.0.0.0"
    client_inactivity_timeout => 300
    include_codec_tag => false
  }
  
  kafka {
    bootstrap_servers => "kafka-01:9092,kafka-02:9092,kafka-03:9092"
    topics => ["logs", "metrics", "events"]
    group_id => "logstash-consumer-group"
    consumer_threads => 4
    poll_timeout_ms => 100
    session_timeout_ms => 30000
    max_poll_records => 1000
    auto_offset_reset => "latest"
    codec => "json"
    
    # Security
    security_protocol => "SASL_SSL"
    sasl_mechanism => "PLAIN"
    sasl_jaas_config => "org.apache.kafka.common.security.plain.PlainLoginModule required username='logstash' password='${KAFKA_PASSWORD}';"
    ssl_truststore_location => "/etc/logstash/certs/kafka.truststore.jks"
    ssl_truststore_password => "${KAFKA_TRUSTSTORE_PASSWORD}"
  }
  
  file {
    path => ["/var/log/apps/*.log", "/var/log/system/*.log"]
    start_position => "beginning"
    sincedb_path => "/var/lib/logstash/sincedb"
    discover_interval => 15
    stat_interval => 1
    codec => multiline {
      pattern => "^%{TIMESTAMP_ISO8601}"
      negate => true
      what => "previous"
    }
  }
}

filter {
  # Add pipeline metadata
  mutate {
    add_field => { "[@metadata][pipeline]" => "main" }
    add_field => { "[@metadata][processed_at]" => "%{+ISO8601}" }
  }
  
  # Parse different log types
  if [fields][log_type] == "nginx" {
    grok {
      match => { "message" => "%{NGINXACCESS}" }
      add_tag => ["nginx", "access_log"]
    }
  } else if [fields][log_type] == "application" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} \[%{LOGLEVEL:level}\] %{DATA:logger} - %{GREEDYDATA:message}" }
      overwrite => ["message"]
      add_tag => ["application", "structured"]
    }
  } else {
    # Default parsing for unstructured logs
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{GREEDYDATA:raw_message}" }
      add_tag => ["unstructured"]
    }
  }
  
  # Parse timestamp
  date {
    match => [ "timestamp", "yyyy-MM-dd HH:mm:ss.SSS", "yyyy-MM-dd'T'HH:mm:ss.SSSZ", "ISO8601" ]
    target => "@timestamp"
    remove_field => ["timestamp"]
  }
  
  # Enrich with GeoIP
  if [client_ip] {
    geoip {
      source => "client_ip"
      target => "geoip"
      database => "/etc/logstash/geoip/GeoLite2-City.mmdb"
    }
  }
  
  # Add host information
  mutate {
    add_field => { "host_info" => "%{host}" }
    add_field => { "pipeline_worker" => "%{[@metadata][pipeline_worker]}" }
  }
  
  # Clean up fields
  mutate {
    remove_field => ["@version", "offset", "input_type", "beat"]
    strip => ["message"]
  }
}

output {
  # Route to different Elasticsearch indices based on log type
  if "nginx" in [tags] {
    elasticsearch {
      hosts => ["https://es-01:9200", "https://es-02:9200", "https://es-03:9200"]
      index => "nginx-logs-%{+YYYY.MM.dd}"
      template_name => "nginx-logs"
      template => "/etc/logstash/templates/nginx-template.json"
      
      # Security
      ssl => true
      ssl_certificate_verification => true
      cacert => "/etc/logstash/certs/ca.crt"
      user => "logstash_writer"
      password => "${ELASTICSEARCH_PASSWORD}"
      
      # Performance
      bulk_path => "/_bulk"
      flush_size => 1000
      idle_flush_time => 5
    }
  } else if "application" in [tags] {
    elasticsearch {
      hosts => ["https://es-01:9200", "https://es-02:9200", "https://es-03:9200"]
      index => "app-logs-%{[fields][app_name]}-%{+YYYY.MM.dd}"
      template_name => "app-logs"
      template => "/etc/logstash/templates/app-template.json"
      
      # Security
      ssl => true
      ssl_certificate_verification => true
      cacert => "/etc/logstash/certs/ca.crt"
      user => "logstash_writer"
      password => "${ELASTICSEARCH_PASSWORD}"
    }
  } else {
    # Default output for unclassified logs
    elasticsearch {
      hosts => ["https://es-01:9200", "https://es-02:9200", "https://es-03:9200"]
      index => "misc-logs-%{+YYYY.MM.dd}"
    }
  }
  
  # Dead letter queue for failed events
  if "_grokparsefailure" in [tags] {
    file {
      path => "/var/log/logstash/failed-events-%{+YYYY-MM-dd}.log"
      codec => "json_lines"
    }
  }
  
  # Monitoring output
  if [@metadata][pipeline] == "main" {
    statsd {
      host => "statsd.monitoring.local"
      port => 8125
      increment => ["logstash.events.processed"]
      gauge => { "logstash.queue.size" => "%{[@metadata][queue_size]}" }
    }
  }
}
```

### Advanced Multi-Pipeline Configuration

```yaml
# /etc/logstash/pipelines.yml
- pipeline.id: beats-pipeline
  path.config: "/etc/logstash/conf.d/beats-pipeline.conf"
  pipeline.workers: 4
  pipeline.batch.size: 1000
  pipeline.batch.delay: 5
  queue.type: persisted
  queue.max_bytes: 1gb
  queue.checkpoint.writes: 1024

- pipeline.id: kafka-pipeline
  path.config: "/etc/logstash/conf.d/kafka-pipeline.conf"
  pipeline.workers: 8
  pipeline.batch.size: 2000
  pipeline.batch.delay: 10
  queue.type: persisted
  queue.max_bytes: 2gb

- pipeline.id: slow-processing
  path.config: "/etc/logstash/conf.d/slow-pipeline.conf"
  pipeline.workers: 2
  pipeline.batch.size: 100
  pipeline.batch.delay: 50
  queue.type: memory
```

### JVM Configuration (jvm.options)

```bash
# Heap size (50-75% of available memory)
-Xms8g
-Xmx8g

# G1GC Configuration
-XX:+UseG1GC
-XX:G1HeapRegionSize=16m
-XX:G1ReservePercent=25
-XX:InitiatingHeapOccupancyPercent=30
-XX:G1MixedGCCountTarget=8
-XX:G1NewSizePercent=10
-XX:G1MaxNewSizePercent=40

# GC logging
-Xlog:gc*,gc+age=trace,safepoint:file=/var/log/logstash/gc.log:utctime,pid,tags:filecount=32,filesize=64m

# Performance tuning
-XX:+AlwaysPreTouch
-XX:-OmitStackTraceInFastThrow
-XX:+UseTLAB
-XX:+ResizeTLAB

# Memory management
-XX:+ExitOnOutOfMemoryError
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/lib/logstash/heap-dump.hprof

# Disable JIT compilation for reproducible performance
-XX:+UnlockExperimentalVMOptions
-XX:+UseTransparentHugePages

# JRuby specific optimizations
-Djruby.compile.mode=OFF
-Djruby.thread.pool.enabled=true
-Djruby.thread.pool.max=16
```

### Logstash Settings (logstash.yml)

```yaml
# Node identification
node.name: logstash-node-01
path.data: /var/lib/logstash
path.logs: /var/log/logstash
path.settings: /etc/logstash

# Pipeline settings
pipeline.workers: 8
pipeline.batch.size: 1000
pipeline.batch.delay: 5
pipeline.unsafe_shutdown: false

# Queue settings
queue.type: persisted
queue.max_bytes: 2gb
queue.checkpoint.acks: 1024
queue.checkpoint.writes: 1024
queue.checkpoint.interval: 1000

# HTTP API
http.host: "0.0.0.0"
http.port: 9600
api.enabled: true
api.http.host: "0.0.0.0"
api.http.port: 9600
api.auth.type: basic
api.auth.basic.username: "logstash-api"
api.auth.basic.password: "${LOGSTASH_API_PASSWORD}"

# Monitoring
monitoring.enabled: true
monitoring.elasticsearch.hosts: ["https://es-monitoring-01:9200", "https://es-monitoring-02:9200"]
monitoring.elasticsearch.username: "logstash_monitoring"
monitoring.elasticsearch.password: "${MONITORING_PASSWORD}"
monitoring.elasticsearch.ssl.certificate_authority: "/etc/logstash/certs/ca.crt"

# Persistent queue settings
queue.drain: true
queue.checkpoint.retry: true

# Dead letter queue
dead_letter_queue.enable: true
dead_letter_queue.max_bytes: 1gb

# Log settings
log.level: info
log.format: json
slowlog.threshold.warn: 2s
slowlog.threshold.info: 1s
slowlog.threshold.debug: 500ms
slowlog.threshold.trace: 100ms

# Config reload
config.reload.automatic: true
config.reload.interval: 3s

# Plugin management
allow_superuser: false
```

## Performance Tuning

### 1. Pipeline Optimization

```ruby
# Conditional processing to reduce CPU usage
filter {
  if [log_level] == "DEBUG" and [environment] == "production" {
    drop { }
  }
  
  # Use efficient field references
  if [message] =~ /ERROR/ {
    mutate {
      add_tag => ["error"]
      add_field => { "severity" => "high" }
    }
  }
  
  # Avoid expensive operations in hot path
  if [user_agent] and [user_agent] != "-" {
    useragent {
      source => "user_agent"
      target => "ua"
    }
  }
  
  # Use ruby filter for complex logic
  ruby {
    code => "
      if event.get('response_time').to_i > 5000
        event.set('slow_request', true)
        event.set('alert_level', 'warning')
      end
    "
  }
}
```

### 2. Memory Management

```bash
#!/bin/bash
# Calculate optimal heap size
TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
HEAP_SIZE=$((TOTAL_RAM * 3 / 4))
if [ $HEAP_SIZE -gt 32 ]; then
    HEAP_SIZE=32
fi

echo "Setting Logstash heap size to ${HEAP_SIZE}GB"
echo "-Xms${HEAP_SIZE}g" >> /etc/logstash/jvm.options
echo "-Xmx${HEAP_SIZE}g" >> /etc/logstash/jvm.options
```

### 3. Queue Tuning

```yaml
# High throughput configuration
queue.type: persisted
queue.max_bytes: 4gb
queue.checkpoint.acks: 2048
queue.checkpoint.writes: 2048
queue.checkpoint.interval: 1000
pipeline.batch.size: 2000
pipeline.batch.delay: 10

# Low latency configuration
queue.type: memory
pipeline.batch.size: 125
pipeline.batch.delay: 1
pipeline.workers: 4
```

### 4. Input/Output Optimization

```ruby
# Optimized Kafka input
input {
  kafka {
    bootstrap_servers => "kafka-01:9092,kafka-02:9092,kafka-03:9092"
    topics => ["logs"]
    consumer_threads => 8
    fetch_min_bytes => 1024
    fetch_max_wait_ms => 500
    max_partition_fetch_bytes => 1048576
    max_poll_records => 2000
    session_timeout_ms => 30000
    heartbeat_interval_ms => 3000
    check_crcs => false
    enable_auto_commit => true
    auto_commit_interval_ms => 1000
  }
}

# Optimized Elasticsearch output
output {
  elasticsearch {
    hosts => ["https://es-01:9200", "https://es-02:9200", "https://es-03:9200"]
    workers => 4
    bulk_path => "/_bulk"
    flush_size => 2000
    idle_flush_time => 5
    max_retries => 3
    retry_max_interval => 5
    template_overwrite => false
    
    # Connection pooling
    pool_max => 1000
    pool_max_per_route => 100
    validate_after_inactivity => 200
    http_compression => true
    
    # Async processing
    action => "index"
    doc_as_upsert => false
  }
}
```

## Integration Patterns

### 1. Beats Integration

```yaml
# Filebeat configuration for Logstash
output.logstash:
  hosts: ["logstash-01:5044", "logstash-02:5044", "logstash-03:5044"]
  worker: 2
  compression_level: 3
  bulk_max_size: 2048
  slow_start: true
  ttl: 30s
  pipelining: 2
  
  # Load balancing
  loadbalance: true
  
  # SSL configuration
  ssl.enabled: true
  ssl.certificate_authorities: ["/etc/beats/ca.crt"]
  ssl.certificate: "/etc/beats/beats.crt"
  ssl.key: "/etc/beats/beats.key"
  ssl.verification_mode: "strict"

# Logstash beats input
input {
  beats {
    port => 5044
    host => "0.0.0.0"
    include_codec_tag => false
    enrich => ["source_metadata"]
    ssl => true
    ssl_certificate => "/etc/logstash/certs/logstash.crt"
    ssl_key => "/etc/logstash/certs/logstash.key"
    ssl_verify_mode => "force_peer"
    ssl_peer_metadata => true
  }
}
```

### 2. Docker Integration

```yaml
# Docker Compose for Logstash
version: '3.8'
services:
  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    container_name: logstash
    environment:
      - "LS_JAVA_OPTS=-Xmx2g -Xms2g"
      - "ELASTICSEARCH_PASSWORD=${ELASTICSEARCH_PASSWORD}"
      - "KAFKA_PASSWORD=${KAFKA_PASSWORD}"
    volumes:
      - ./logstash/config:/usr/share/logstash/config:ro
      - ./logstash/pipeline:/usr/share/logstash/pipeline:ro
      - ./logstash/certs:/usr/share/logstash/config/certs:ro
      - ./logstash/templates:/usr/share/logstash/templates:ro
      - logstash-data:/usr/share/logstash/data
      - /var/log/apps:/var/log/apps:ro
    ports:
      - "5044:5044"
      - "9600:9600"
    networks:
      - elastic
    depends_on:
      - elasticsearch
      - kafka
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9600"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  logstash-data:
    driver: local

networks:
  elastic:
    driver: bridge
```

### 3. Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: logstash
  namespace: logging
spec:
  serviceName: logstash
  replicas: 3
  selector:
    matchLabels:
      app: logstash
  template:
    metadata:
      labels:
        app: logstash
    spec:
      containers:
      - name: logstash
        image: docker.elastic.co/logstash/logstash:8.11.0
        ports:
        - containerPort: 5044
          name: beats
        - containerPort: 9600
          name: http
        env:
        - name: LS_JAVA_OPTS
          value: "-Xmx4g -Xms4g"
        - name: ELASTICSEARCH_PASSWORD
          valueFrom:
            secretKeyRef:
              name: logstash-secrets
              key: elasticsearch-password
        resources:
          requests:
            memory: 4Gi
            cpu: 2
          limits:
            memory: 8Gi
            cpu: 4
        volumeMounts:
        - name: config
          mountPath: /usr/share/logstash/config
          readOnly: true
        - name: pipeline
          mountPath: /usr/share/logstash/pipeline
          readOnly: true
        - name: data
          mountPath: /usr/share/logstash/data
        livenessProbe:
          httpGet:
            path: /
            port: 9600
          initialDelaySeconds: 60
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 9600
          initialDelaySeconds: 30
          periodSeconds: 5
      volumes:
      - name: config
        configMap:
          name: logstash-config
      - name: pipeline
        configMap:
          name: logstash-pipeline
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 100Gi

---
apiVersion: v1
kind: Service
metadata:
  name: logstash
  namespace: logging
spec:
  selector:
    app: logstash
  ports:
  - name: beats
    port: 5044
    targetPort: 5044
  - name: http
    port: 9600
    targetPort: 9600
  type: ClusterIP
```

### 4. Application Integration (Python)

```python
import json
import socket
import logging
from datetime import datetime
from typing import Dict, Any, Optional

class LogstashHandler(logging.Handler):
    """Custom logging handler for Logstash TCP input"""
    
    def __init__(self, host: str, port: int, application: str = "python-app"):
        super().__init__()
        self.host = host
        self.port = port
        self.application = application
        self.socket = None
        
    def emit(self, record):
        """Send log record to Logstash"""
        try:
            if not self.socket:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
            
            log_entry = {
                "@timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
                "application": self.application,
                "host": socket.gethostname(),
                "path": record.pathname,
                "line": record.lineno,
                "function": record.funcName
            }
            
            # Add exception information if present
            if record.exc_info:
                log_entry["exception"] = self.format(record)
            
            # Add extra fields
            if hasattr(record, 'user_id'):
                log_entry["user_id"] = record.user_id
            if hasattr(record, 'request_id'):
                log_entry["request_id"] = record.request_id
            
            message = json.dumps(log_entry) + '\n'
            self.socket.send(message.encode('utf-8'))
            
        except Exception as e:
            # Fallback to standard logging
            print(f"Failed to send log to Logstash: {e}")
            
    def close(self):
        """Close the socket connection"""
        if self.socket:
            self.socket.close()
            self.socket = None

# Usage example
def setup_logging():
    logger = logging.getLogger("myapp")
    logger.setLevel(logging.INFO)
    
    # Add Logstash handler
    logstash_handler = LogstashHandler("logstash.example.com", 5959)
    logstash_handler.setLevel(logging.INFO)
    
    # Add console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(logstash_handler)
    logger.addHandler(console_handler)
    
    return logger

# Example usage with extra fields
logger = setup_logging()
logger.info("User logged in", extra={"user_id": 12345, "request_id": "req-abc123"})
```

## Production Deployment Strategies

### 1. High Availability Setup

```yaml
# Load balancer configuration (HAProxy)
global
    log stdout local0
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

defaults
    mode tcp
    log global
    option tcplog
    option dontlognull
    timeout connect 5000
    timeout client 50000
    timeout server 50000

# Logstash beats input load balancer
frontend logstash_beats
    bind *:5044
    mode tcp
    default_backend logstash_beats_backend

backend logstash_beats_backend
    mode tcp
    balance roundrobin
    option tcp-check
    tcp-check connect port 5044
    server logstash-01 10.0.1.10:5044 check
    server logstash-02 10.0.1.11:5044 check
    server logstash-03 10.0.1.12:5044 check

# Logstash HTTP API load balancer
frontend logstash_api
    bind *:9600
    mode http
    default_backend logstash_api_backend

backend logstash_api_backend
    mode http
    balance roundrobin
    option httpchk GET /
    http-check expect status 200
    server logstash-01 10.0.1.10:9600 check
    server logstash-02 10.0.1.11:9600 check
    server logstash-03 10.0.1.12:9600 check
```

### 2. Monitoring and Alerting

```yaml
# Prometheus monitoring rules
groups:
- name: logstash
  rules:
  - alert: LogstashDown
    expr: up{job="logstash"} == 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Logstash instance is down"
      description: "Logstash instance {{ $labels.instance }} has been down for more than 5 minutes"

  - alert: LogstashHighCPU
    expr: rate(process_cpu_seconds_total{job="logstash"}[5m]) * 100 > 80
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "Logstash high CPU usage"
      description: "Logstash instance {{ $labels.instance }} CPU usage is above 80%"

  - alert: LogstashHighMemory
    expr: (process_resident_memory_bytes{job="logstash"} / process_virtual_memory_max_bytes{job="logstash"}) * 100 > 85
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Logstash high memory usage"
      description: "Logstash instance {{ $labels.instance }} memory usage is above 85%"

  - alert: LogstashQueueFull
    expr: logstash_queue_events_count{job="logstash"} > 500000
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Logstash queue is full"
      description: "Logstash instance {{ $labels.instance }} queue has {{ $value }} events"

  - alert: LogstashSlowProcessing
    expr: logstash_pipeline_duration_seconds{job="logstash"} > 30
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Logstash slow processing"
      description: "Logstash pipeline {{ $labels.pipeline }} processing time is {{ $value }} seconds"
```

### 3. Security Configuration

```ruby
# Security-hardened configuration
input {
  beats {
    port => 5044
    host => "0.0.0.0"
    ssl => true
    ssl_certificate => "/etc/logstash/certs/logstash.crt"
    ssl_key => "/etc/logstash/certs/logstash.key"
    ssl_certificate_authorities => ["/etc/logstash/certs/ca.crt"]
    ssl_verify_mode => "force_peer"
    ssl_peer_metadata => true
    include_codec_tag => false
  }
}

filter {
  # Remove sensitive data
  mutate {
    remove_field => ["password", "ssn", "credit_card", "api_key"]
  }
  
  # Anonymize IP addresses
  mutate {
    gsub => [
      "client_ip", "\.\d+$", ".xxx",
      "x_forwarded_for", "\.\d+$", ".xxx"
    ]
  }
  
  # Add security headers
  mutate {
    add_field => { "security_processed" => "true" }
    add_field => { "data_classification" => "internal" }
  }
}

output {
  elasticsearch {
    hosts => ["https://es-01:9200", "https://es-02:9200", "https://es-03:9200"]
    ssl => true
    ssl_certificate_verification => true
    cacert => "/etc/logstash/certs/ca.crt"
    keystore => "/etc/logstash/certs/logstash.p12"
    keystore_password => "${KEYSTORE_PASSWORD}"
    user => "logstash_writer"
    password => "${ELASTICSEARCH_PASSWORD}"
    
    # Use HTTPS only
    ssl_supported_protocols => ["TLSv1.2", "TLSv1.3"]
  }
}
```

### 4. Backup and Recovery

```bash
#!/bin/bash
# Logstash backup script

BACKUP_DIR="/backups/logstash"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="${BACKUP_DIR}/logstash_backup_${DATE}"

echo "Starting Logstash backup at ${DATE}"

# Create backup directory
mkdir -p "${BACKUP_PATH}"

# Backup configuration files
echo "Backing up configuration files..."
tar -czf "${BACKUP_PATH}/config.tar.gz" \
  /etc/logstash/logstash.yml \
  /etc/logstash/jvm.options \
  /etc/logstash/log4j2.properties \
  /etc/logstash/pipelines.yml \
  /etc/logstash/conf.d/ \
  /etc/logstash/templates/

# Backup persistent queue data
echo "Backing up persistent queue data..."
systemctl stop logstash
tar -czf "${BACKUP_PATH}/queue_data.tar.gz" /var/lib/logstash/queue/
systemctl start logstash

# Backup certificates and keys
echo "Backing up certificates..."
tar -czf "${BACKUP_PATH}/certs.tar.gz" /etc/logstash/certs/

# Create metadata file
cat > "${BACKUP_PATH}/metadata.json" << EOF
{
  "backup_date": "${DATE}",
  "logstash_version": "$(logstash --version)",
  "config_hash": "$(find /etc/logstash -type f -name '*.conf' -exec md5sum {} \; | md5sum)",
  "backup_size": "$(du -sh ${BACKUP_PATH} | cut -f1)"
}
EOF

# Cleanup old backups (keep last 7 days)
find "${BACKUP_DIR}" -type d -name "logstash_backup_*" -mtime +7 -exec rm -rf {} \;

echo "Backup completed: ${BACKUP_PATH}"
```

## Best Practices

### 1. Pipeline Design
- Use multiple pipelines for different data sources
- Implement proper error handling and dead letter queues
- Keep filter logic simple and efficient
- Use conditional processing to avoid unnecessary operations
- Monitor pipeline performance and bottlenecks

### 2. Resource Management
- Allocate 50-75% of available memory to heap
- Use persistent queues for durability
- Configure appropriate batch sizes based on throughput needs
- Monitor JVM garbage collection
- Use dedicated nodes for different workloads

### 3. Security
- Always use TLS/SSL for data in transit
- Implement proper authentication and authorization
- Remove or mask sensitive data in filters
- Use secure credential management
- Regular security updates and patches

### 4. Monitoring
- Monitor pipeline throughput and latency
- Track queue sizes and processing times
- Set up alerts for critical metrics
- Monitor JVM health and garbage collection
- Use Elastic Stack monitoring or external tools

### 5. Troubleshooting
- Enable detailed logging for debugging
- Use pipeline-to-pipeline communication for complex flows
- Implement proper field naming conventions
- Test configurations in development environment
- Document custom patterns and filters

## Comprehensive Resources

### 📚 Official Documentation & References
- [Logstash Official Documentation](https://www.elastic.co/guide/en/logstash/current/)
- [Logstash Configuration Reference](https://www.elastic.co/guide/en/logstash/current/configuration-file-structure.html)
- [Logstash Plugin Documentation](https://www.elastic.co/guide/en/logstash/current/input-plugins.html)
- [Logstash Performance Tuning](https://www.elastic.co/guide/en/logstash/current/tuning-logstash.html)
- [Grok Pattern Library](https://grokdebug.herokuapp.com/patterns)

### 🎓 Learning Resources
- [Elastic Certified Engineer Program](https://www.elastic.co/training/certification)
- [Logstash Training Courses](https://www.elastic.co/training/)
- [Getting Started with Logstash](https://www.elastic.co/guide/en/logstash/current/getting-started-with-logstash.html)
- [ELK Stack Tutorial](https://www.elastic.co/what-is/elk-stack)

### 🛠️ Essential Tools
- [Grok Debugger](https://grokdebug.herokuapp.com/) - Test grok patterns online
- [Kibana Dev Tools](https://www.elastic.co/guide/en/kibana/current/console-kibana.html) - Query and test data
- [Logstash Docker Images](https://www.docker.elastic.co/r/logstash) - Official Docker containers
- [Elastic Stack Docker Compose](https://github.com/deviantony/docker-elk) - Complete ELK setup
- [Filebeat](https://www.elastic.co/beats/filebeat) - Lightweight log shipper

### 🏗️ Projects & Examples
- [Logstash Configuration Examples](https://github.com/elastic/logstash/tree/main/docs/static/configuration)
- [ELK Stack Examples](https://github.com/deviantony/docker-elk)
- [Log Analysis Patterns](https://github.com/logstash-plugins/logstash-patterns-core/tree/main/patterns)
- [Logstash Pipeline Examples](https://www.elastic.co/blog/structured-logging-filebeat)

### 👥 Community & Support
- [Elastic Community Forum](https://discuss.elastic.co/c/logstash/14)
- [Stack Overflow - logstash](https://stackoverflow.com/questions/tagged/logstash)
- [Logstash Reddit](https://www.reddit.com/r/elasticsearch/)
- [Elastic Slack Community](https://ela.st/slack)
- [GitHub - Logstash Issues](https://github.com/elastic/logstash/issues)

### 📊 Monitoring & Observability
- [Logstash Monitoring APIs](https://www.elastic.co/guide/en/logstash/current/monitoring-logstash.html)
- [Metricbeat for Logstash](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-module-logstash.html)
- [Elastic Stack Monitoring](https://www.elastic.co/guide/en/elasticsearch/reference/current/monitor-elasticsearch-cluster.html)
- [Grafana Logstash Dashboards](https://grafana.com/grafana/dashboards/?search=logstash)

### 🔐 Security Resources
- [Logstash Security Guide](https://www.elastic.co/guide/en/logstash/current/ls-security.html)
- [Keystore for Secure Settings](https://www.elastic.co/guide/en/logstash/current/keystore.html)
- [TLS/SSL Configuration](https://www.elastic.co/guide/en/logstash/current/ls-security.html#ls-http-ssl)
- [Pipeline-to-Pipeline Security](https://www.elastic.co/guide/en/logstash/current/pipeline-to-pipeline.html)

### 📈 Advanced Topics
- [Multiple Pipeline Configuration](https://www.elastic.co/guide/en/logstash/current/multiple-pipelines.html)
- [Pipeline-to-Pipeline Communication](https://www.elastic.co/guide/en/logstash/current/pipeline-to-pipeline.html)
- [Persistent Queues](https://www.elastic.co/guide/en/logstash/current/persistent-queues.html)
- [Dead Letter Queues](https://www.elastic.co/guide/en/logstash/current/dead-letter-queues.html)
- [Java Execution Engine](https://www.elastic.co/guide/en/logstash/current/java-execution.html)

### 🎥 Video Content
- [Elastic YouTube Channel](https://www.youtube.com/c/elasticsearch)
- [ELK Stack Tutorial Videos](https://www.youtube.com/playlist?list=PLhLSfisesZIvgGh_VoFFsHhIQf7L4aHS5)
- [Logstash Deep Dive](https://www.elastic.co/elasticon/conf/2020/sf/logstash-deep-dive)
- [Data Processing with Logstash](https://www.youtube.com/watch?v=uxjJz7kCBRM)

### 📖 Books & Publications
- "Learning Elastic Stack 7.0" by Pranav Shukla
- "Mastering Elastic Stack" by Yuvraj Gupta
- "Elasticsearch: The Definitive Guide" (includes Logstash chapters)
- "Learning ELK Stack" by Savi Mathur
- [Elastic Blog - Logstash Articles](https://www.elastic.co/blog/category/logstash)

### 🔌 Plugin Development
- [Logstash Plugin Development Guide](https://www.elastic.co/guide/en/logstash/current/contributing-to-logstash.html)
- [Custom Plugin Examples](https://github.com/logstash-plugins)
- [Plugin Generator](https://www.elastic.co/guide/en/logstash/current/plugin-generator.html)
- [Community Plugins](https://github.com/logstash-plugins)