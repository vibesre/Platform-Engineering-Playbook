# Fluent Bit

## Overview

Fluent Bit is a lightweight, high-performance log processor and forwarder designed for cloud and containerized environments. It's essential for platform engineers who need efficient log collection with minimal resource footprint and cloud-native integrations.

## Key Features

- **Ultra Lightweight**: &lt;1MB memory footprint
- **High Performance**: Written in C for maximum efficiency
- **Cloud Native**: Built for containers and Kubernetes
- **Vendor Agnostic**: 100+ plugins for inputs and outputs
- **Stream Processing**: Real-time data processing and filtering

## Installation

### Docker Installation
```bash
# Create Fluent Bit configuration
cat > fluent-bit.conf << EOF
[SERVICE]
    Flush         1
    Log_Level     info
    Daemon        off
    Parsers_File  parsers.conf
    HTTP_Server   On
    HTTP_Listen   0.0.0.0
    HTTP_Port     2020

[INPUT]
    Name              tail
    Path              /var/log/*.log
    Parser            docker
    Tag               host.*
    Refresh_Interval  5

[OUTPUT]
    Name  stdout
    Match *
EOF

# Run Fluent Bit container
docker run -d \
  --name fluent-bit \
  -p 2020:2020 \
  -v $(pwd)/fluent-bit.conf:/fluent-bit/etc/fluent-bit.conf \
  -v /var/log:/var/log:ro \
  fluent/fluent-bit:latest
```

### Kubernetes DaemonSet
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluent-bit
  namespace: logging
spec:
  selector:
    matchLabels:
      name: fluent-bit
  template:
    metadata:
      labels:
        name: fluent-bit
    spec:
      serviceAccount: fluent-bit
      containers:
      - name: fluent-bit
        image: fluent/fluent-bit:latest
        ports:
        - containerPort: 2020
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        resources:
          limits:
            memory: 128Mi
            cpu: 100m
          requests:
            memory: 64Mi
            cpu: 50m
        volumeMounts:
        - name: varlog
          mountPath: /var/log
          readOnly: true
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        - name: fluent-bit-config
          mountPath: /fluent-bit/etc/
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
      - name: fluent-bit-config
        configMap:
          name: fluent-bit-config
      tolerations:
      - operator: Exists
        effect: NoSchedule
      - operator: Exists
        effect: NoExecute
```

## Configuration

### Basic Configuration
```ini
# fluent-bit.conf
[SERVICE]
    Flush         5
    Log_Level     info
    Daemon        off
    Parsers_File  parsers.conf
    HTTP_Server   On
    HTTP_Listen   0.0.0.0
    HTTP_Port     2020
    Health_Check  On

# Container logs input
[INPUT]
    Name              tail
    Path              /var/log/containers/*.log
    Parser            cri
    Tag               kube.*
    Refresh_Interval  5
    Mem_Buf_Limit     50MB
    Skip_Long_Lines   On
    Skip_Empty_Lines  On

# System logs input  
[INPUT]
    Name            systemd
    Tag             host.*
    Systemd_Filter  _SYSTEMD_UNIT=kubelet.service
    Systemd_Filter  _SYSTEMD_UNIT=docker.service
    Read_From_Tail  On

# HTTP input for applications
[INPUT]
    Name   http
    Listen 0.0.0.0
    Port   9880
    Tag    http_logs

# Kubernetes metadata filter
[FILTER]
    Name                kubernetes
    Match               kube.*
    Kube_URL            https://kubernetes.default.svc:443
    Kube_CA_File        /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    Kube_Token_File     /var/run/secrets/kubernetes.io/serviceaccount/token
    Kube_Tag_Prefix     kube.var.log.containers.
    Merge_Log           On
    Keep_Log            Off
    K8S-Logging.Parser  On
    K8S-Logging.Exclude Off
    Annotations         Off
    Labels              On

# JSON parser filter
[FILTER]
    Name         parser
    Match        kube.*
    Key_Name     log
    Parser       json
    Reserve_Data On
    Preserve_Key On

# Add hostname
[FILTER]
    Name    modify
    Match   *
    Add     hostname ${HOSTNAME}
    Add     cluster_name production

# Elasticsearch output
[OUTPUT]
    Name            es
    Match           kube.*
    Host            elasticsearch
    Port            9200
    Index           fluent-bit
    Type            _doc
    Logstash_Format On
    Logstash_Prefix kubernetes
    Logstash_DateFormat %Y.%m.%d
    Time_Key        @timestamp
    Time_Key_Format %Y-%m-%dT%H:%M:%S.%L%z
    Retry_Limit     5

# Prometheus metrics output
[OUTPUT]
    Name            prometheus_exporter
    Match           *
    Host            0.0.0.0
    Port            2021
```

### Parser Configuration
```ini
# parsers.conf
[PARSER]
    Name        docker
    Format      json
    Time_Key    time
    Time_Format %Y-%m-%dT%H:%M:%S.%L
    Time_Keep   On

[PARSER]
    Name        cri
    Format      regex
    Regex       ^(?<time>[^ ]+) (?<stream>stdout|stderr) (?<logtag>[^ ]*) (?<message>.*)
    Time_Key    time
    Time_Format %Y-%m-%dT%H:%M:%S.%L%z

[PARSER]
    Name        json
    Format      json
    Time_Key    timestamp
    Time_Format %Y-%m-%dT%H:%M:%S.%L%z
    Time_Keep   On

[PARSER]
    Name        nginx
    Format      regex
    Regex       ^(?<remote>[^ ]*) (?<host>[^ ]*) (?<user>[^ ]*) \[(?<time>[^\]]*)\] "(?<method>\S+)(?: +(?<path>[^\"]*?)(?: +\S*)?)?" (?<code>[^ ]*) (?<size>[^ ]*)(?: "(?<referer>[^\"]*)" "(?<agent>[^\"]*)")
    Time_Key    time
    Time_Format %d/%b/%Y:%H:%M:%S %z

[PARSER]
    Name        apache
    Format      regex
    Regex       ^(?<host>[^ ]*) [^ ]* (?<user>[^ ]*) \[(?<time>[^\]]*)\] "(?<method>\S+)(?: +(?<path>[^ ]*) +\S*)?" (?<code>[^ ]*) (?<size>[^ ]*)(?: "(?<referer>[^\"]*)" "(?<agent>[^\"]*)")
    Time_Key    time
    Time_Format %d/%b/%Y:%H:%M:%S %z

[PARSER]
    Name        syslog-rfc5424
    Format      regex
    Regex       ^\<(?<pri>[0-9]{1,5})\>1 (?<time>[^ ]+) (?<host>[^ ]+) (?<ident>[^ ]+) (?<pid>[-0-9]+) (?<msgid>[^ ]+) (?<extradata>(\-|\[.+\])) (?<message>.+)$
    Time_Key    time
    Time_Format %Y-%m-%dT%H:%M:%S.%L%z
```

## Common Use Cases

### Kubernetes Log Collection
```ini
# Comprehensive Kubernetes logging
[SERVICE]
    Flush         5
    Log_Level     info
    Daemon        off
    Parsers_File  parsers.conf
    HTTP_Server   On
    HTTP_Port     2020
    Health_Check  On

# Container logs
[INPUT]
    Name              tail
    Path              /var/log/containers/*.log
    Parser            cri
    Tag               kube.*
    Refresh_Interval  5
    Mem_Buf_Limit     50MB
    Skip_Long_Lines   On
    DB                /var/log/flb_kube.db
    DB.Sync           Normal

# Kubernetes metadata enrichment
[FILTER]
    Name                kubernetes
    Match               kube.*
    Kube_URL            https://kubernetes.default.svc:443
    Kube_CA_File        /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    Kube_Token_File     /var/run/secrets/kubernetes.io/serviceaccount/token
    Merge_Log           On
    Keep_Log            Off
    K8S-Logging.Parser  On
    K8S-Logging.Exclude Off
    Annotations         Off
    Labels              On
    Buffer_Size         256k

# Parse application logs
[FILTER]
    Name         parser
    Match        kube.*nginx*
    Key_Name     log
    Parser       nginx
    Reserve_Data On

[FILTER]
    Name         parser
    Match        kube.*app*
    Key_Name     log
    Parser       json
    Reserve_Data On

# Add cluster information
[FILTER]
    Name    modify
    Match   kube.*
    Add     cluster_name ${CLUSTER_NAME}
    Add     environment ${ENVIRONMENT}
    Add     region ${AWS_REGION}

# Route to different outputs based on namespace
[FILTER]
    Name    rewrite_tag
    Match   kube.*
    Rule    $kubernetes['namespace_name'] ^(kube-system|kube-public)$ system.$TAG false
    Rule    $kubernetes['namespace_name'] ^(monitoring|logging)$ infrastructure.$TAG false
    Rule    $kubernetes['namespace_name'] .* application.$TAG false

# System logs to dedicated index
[OUTPUT]
    Name            es
    Match           system.*
    Host            ${FLUENT_ELASTICSEARCH_HOST}
    Port            ${FLUENT_ELASTICSEARCH_PORT}
    Index           k8s-system
    Type            _doc
    Logstash_Format On
    Logstash_Prefix k8s-system
    Retry_Limit     5

# Infrastructure logs
[OUTPUT]
    Name            es
    Match           infrastructure.*
    Host            ${FLUENT_ELASTICSEARCH_HOST}
    Port            ${FLUENT_ELASTICSEARCH_PORT}
    Index           k8s-infrastructure
    Type            _doc
    Logstash_Format On
    Logstash_Prefix k8s-infrastructure
    Retry_Limit     5

# Application logs
[OUTPUT]
    Name            es
    Match           application.*
    Host            ${FLUENT_ELASTICSEARCH_HOST}
    Port            ${FLUENT_ELASTICSEARCH_PORT}
    Index           k8s-applications
    Type            _doc
    Logstash_Format On
    Logstash_Prefix k8s-applications
    Retry_Limit     5
```

### Multi-destination Log Forwarding
```ini
# Forward to multiple destinations
[INPUT]
    Name   tail
    Path   /var/log/app/*.log
    Parser json
    Tag    app.*

# Filter critical errors
[FILTER]
    Name    grep
    Match   app.*
    Regex   level ^(ERROR|FATAL)$

# Add routing tags
[FILTER]
    Name    rewrite_tag
    Match   app.*
    Rule    $level ^ERROR$ error.$TAG false
    Rule    $level ^FATAL$ critical.$TAG false
    Rule    $level .* normal.$TAG false

# Normal logs to Elasticsearch
[OUTPUT]
    Name  es
    Match normal.*
    Host  elasticsearch
    Port  9200
    Index application-logs

# Error logs to both Elasticsearch and S3
[OUTPUT]
    Name   es
    Match  error.*
    Host   elasticsearch
    Port   9200
    Index  error-logs

[OUTPUT]
    Name                         s3
    Match                        error.*
    bucket                       error-logs-backup
    region                       us-east-1
    total_file_size              50M
    upload_timeout               10m
    s3_key_format                /year=%Y/month=%m/day=%d/hour=%H/error-logs-%Y%m%d-%H%M%S
    s3_key_format_tag_delimiters ._

# Critical logs to alerting system
[OUTPUT]
    Name  http
    Match critical.*
    Host  alertmanager
    Port  9093
    URI   /api/v1/alerts
    Format json
```

## Cloud Integrations

### AWS CloudWatch
```ini
# CloudWatch Logs output
[OUTPUT]
    Name                     cloudwatch
    Match                    *
    region                   us-east-1
    log_group_name          /aws/fluent-bit
    log_stream_name         ${hostname}
    auto_create_group       On
    log_retention_days      30
```

### AWS S3
```ini
# S3 output with partitioning
[OUTPUT]
    Name                         s3
    Match                        *
    bucket                       my-log-bucket
    region                       us-east-1
    total_file_size              50M
    upload_timeout               10m
    use_put_object               On
    s3_key_format                /logs/year=%Y/month=%m/day=%d/hour=%H/%Y%m%d-%H%M%S
    s3_key_format_tag_delimiters ._
    compression                  gzip
```

### Google Cloud Logging
```ini
# Stackdriver output
[OUTPUT]
    Name        stackdriver
    Match       *
    google_service_credentials /path/to/credentials.json
    project_id  my-gcp-project
    resource    k8s_container
```

## Stream Processing

### Data Enrichment
```ini
# Lua script for custom processing
[FILTER]
    Name    lua
    Match   *
    Script  /fluent-bit/scripts/enrich.lua
    Call    enrich_logs

# Example Lua script (enrich.lua)
function enrich_logs(tag, timestamp, record)
    -- Add custom fields
    record["processed_by"] = "fluent-bit"
    record["processing_time"] = os.time()
    
    -- Mask sensitive data
    if record["password"] then
        record["password"] = "[REDACTED]"
    end
    
    -- Parse user agent
    if record["user_agent"] then
        record["is_mobile"] = string.match(record["user_agent"], "Mobile") ~= nil
    end
    
    return 2, timestamp, record
end
```

### Metrics Generation
```ini
# Generate metrics from logs
[FILTER]
    Name    grep
    Match   nginx.*
    Regex   status ^[45]\d\d$

[FILTER]
    Name       modify
    Match      nginx.*
    Add        metric_name http_errors_total
    Add        metric_type counter
    Add        metric_help Total HTTP errors

[OUTPUT]
    Name  prometheus_exporter
    Match nginx.*
    Host  0.0.0.0
    Port  2021
```

## Performance Tuning

### Memory Management
```ini
[SERVICE]
    # Memory limits
    Mem_Buf_Limit      32MB
    
    # Buffer flush settings
    Flush              5
    Grace              5
    
    # Worker settings
    HC_Errors_Count    5
    HC_Retry_Failure_Count 5
    HC_Period          60

[INPUT]
    Name              tail
    Path              /var/log/*.log
    Mem_Buf_Limit     5MB
    Skip_Long_Lines   On
    Skip_Empty_Lines  On
    Buffer_Chunk_Size 32k
    Buffer_Max_Size   64k
    Refresh_Interval  5
```

### Output Buffering
```ini
[OUTPUT]
    Name                es
    Match               *
    Host                elasticsearch
    Port                9200
    
    # Performance settings
    Buffer_Size         4096
    Workers             2
    
    # Retry settings
    Retry_Limit         5
    
    # Batch settings
    Suppress_Type_Name  On
```

## Monitoring and Health Checks

### Built-in Monitoring
```bash
# Health check endpoint
curl http://localhost:2020/

# Metrics endpoint
curl http://localhost:2020/api/v1/metrics

# Storage metrics
curl http://localhost:2020/api/v1/storage

# Uptime information
curl http://localhost:2020/api/v1/uptime
```

### Prometheus Integration
```ini
# Prometheus metrics output
[OUTPUT]
    Name  prometheus_exporter
    Match *
    Host  0.0.0.0
    Port  2021
    
[OUTPUT]
    Name  prometheus_remote_write
    Match metrics.*
    Host  prometheus
    Port  9090
    Uri   /api/v1/write
```

## Best Practices

- Use appropriate parsers for structured logging
- Implement proper memory limits and buffer management
- Monitor Fluent Bit resource usage and performance
- Use database files for tail inputs to handle restarts
- Implement log sampling for high-volume applications
- Configure appropriate retry limits and timeouts
- Use health checks for container orchestration
- Regular monitoring of processing rates and errors

## Great Resources

- [Fluent Bit Documentation](https://docs.fluentbit.io/) - Official comprehensive documentation
- [Fluent Bit GitHub](https://github.com/fluent/fluent-bit) - Source code and community
- [Fluent Bit vs Fluentd](https://docs.fluentbit.io/manual/about/fluentd-and-fluent-bit) - Comparison guide
- [Fluent Bit Kubernetes Guide](https://docs.fluentbit.io/manual/installation/kubernetes) - K8s deployment guide
- [Fluent Bit Configuration Examples](https://github.com/fluent/fluent-bit/tree/master/conf) - Example configurations
- [CNCF Fluent Bit](https://www.cncf.io/projects/fluent-bit/) - Cloud Native Computing Foundation project page
- [Fluent Bit Community](https://discuss.fluentd.org/c/fluent-bit/) - Forums and community support
- [Awesome Fluent Bit](https://github.com/fluent/awesome-fluent-bit) - Curated resources and tools