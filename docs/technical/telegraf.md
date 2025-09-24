# Telegraf

## 📚 Learning Resources

### 📖 Essential Documentation
- [Telegraf Official Documentation](https://docs.influxdata.com/telegraf/) - Comprehensive documentation with configuration guides
- [Plugin Directory](https://docs.influxdata.com/telegraf/latest/plugins/) - Complete reference for all input, output, and processor plugins
- [Getting Started Guide](https://docs.influxdata.com/telegraf/latest/get-started/) - Quick start tutorial for metrics collection
- [Configuration Reference](https://docs.influxdata.com/telegraf/latest/configuration/) - Complete configuration syntax and options
- [Best Practices](https://docs.influxdata.com/telegraf/latest/best_practices/) - Production deployment and optimization guide

### 📝 Essential Guides & Community
- [InfluxData Blog - Telegraf](https://www.influxdata.com/blog/category/telegraf/) - Latest features, use cases, and tutorials
- [Telegraf vs Other Agents](https://www.influxdata.com/blog/telegraf-vs-prometheus-node-exporter/) - Comparison with other monitoring agents
- [TICK Stack Guide](https://www.influxdata.com/time-series-platform/) - Understanding Telegraf in the broader ecosystem
- [Awesome Telegraf](https://github.com/influxdata/awesome-telegraf) - Community-curated resources and examples
- [Community Templates](https://github.com/influxdata/community-templates) - Pre-built configurations for common scenarios

### 🎥 Video Tutorials
- [Telegraf Tutorial for Beginners](https://www.youtube.com/watch?v=2SUBRE6wGiA) - InfluxData Official (30 minutes)
- [Complete Monitoring Setup](https://www.youtube.com/watch?v=T0WG4UHBZQE) - TICK stack tutorial (1 hour)
- [Telegraf Plugin Deep Dive](https://www.youtube.com/results?search_query=telegraf+plugins+tutorial) - Plugin configuration and customization
- [InfluxData Webinar Series](https://www.influxdata.com/resources/webinars/) - Regular technical sessions

### 🎓 Professional Courses
- [InfluxDB University](https://university.influxdata.com/) - Free comprehensive training platform
- [Telegraf Training Course](https://university.influxdata.com/courses/telegraf-training/) - Official training (Free)
- [Time Series Data Collection](https://university.influxdata.com/courses/data-collection/) - Advanced collection techniques
- [Monitoring Infrastructure](https://www.pluralsight.com/courses/infrastructure-monitoring-telegraf) - Pluralsight practical course

### 📚 Books
- "Time Series Databases: New Ways to Store and Access Data" by Ted Dunning - [Purchase on Amazon](https://www.amazon.com/Time-Series-Databases-Ways-Access/dp/1491914726)
- "Learning InfluxDB" by Gianluca Arbezzano - [Purchase on Amazon](https://www.amazon.com/Learning-InfluxDB-Gianluca-Arbezzano/dp/1787129411)
- "Monitoring with Prometheus" by James Turnbull - [Purchase on Amazon](https://www.amazon.com/Monitoring-Prometheus-James-Turnbull/dp/B07GS68SQD)

### 🛠️ Interactive Tools
- [Telegraf Configuration Generator](https://docs.influxdata.com/telegraf/latest/configure/) - Web-based configuration builder
- [InfluxDB Cloud Sandbox](https://cloud2.influxdata.com/signup) - Free environment with Telegraf included
- [Docker Compose Examples](https://github.com/influxdata/sandbox) - Ready-to-run development environments
- [Telegraf Playground](https://play.influxdata.com/) - Browser-based experimentation environment
- [Plugin Tester](https://docs.influxdata.com/telegraf/latest/administration/commands/) - Command-line testing tools

### 🚀 Ecosystem Tools
- [InfluxDB](https://www.influxdata.com/products/influxdb/) - Time series database for metrics storage
- [Chronograf](https://www.influxdata.com/time-series-platform/chronograf/) - Visualization and dashboarding
- [Kapacitor](https://www.influxdata.com/time-series-platform/kapacitor/) - Real-time stream processing and alerting
- [Grafana Telegraf Integration](https://grafana.com/docs/grafana/latest/datasources/influxdb/) - Advanced visualization platform
- [Prometheus Remote Write](https://docs.influxdata.com/telegraf/latest/plugins/#output-prometheus_client) - Prometheus ecosystem integration

### 🌐 Community & Support
- [InfluxData Community](https://community.influxdata.com/c/telegraf/) - Official support forum
- [Telegraf Slack Channel](https://influxdata.com/slack) - Real-time community discussions
- [GitHub Telegraf](https://github.com/influxdata/telegraf) - Source code, issues, and feature requests
- [Stack Overflow Telegraf](https://stackoverflow.com/questions/tagged/telegraf) - Technical Q&A and troubleshooting

## Understanding Telegraf: The Universal Metrics Collection Agent

Telegraf is a plugin-driven server agent for collecting, processing, and reporting metrics from virtually any system, service, or third-party API. As the "T" in the TICK Stack, Telegraf serves as the universal data collection layer that bridges the gap between diverse infrastructure components and time series databases, making metrics collection standardized, scalable, and maintainable.

### How Telegraf Works

Telegraf operates on a simple but powerful three-stage pipeline architecture:

1. **Input Stage**: 300+ input plugins collect metrics from systems, applications, sensors, and APIs using native protocols and formats.

2. **Processing Stage**: Optional processor plugins transform, filter, aggregate, and enrich metrics in real-time before output.

3. **Output Stage**: 50+ output plugins send processed metrics to various destinations including time series databases, message queues, and monitoring platforms.

4. **Buffering and Batching**: Built-in memory management ensures reliable delivery with configurable batching and retry mechanisms.

### The Telegraf Ecosystem

Telegraf is more than just a metrics collector—it's a comprehensive data integration platform:

- **Input Plugins**: System metrics (CPU, memory, disk), application metrics (HTTP, database), cloud services (AWS, Azure, GCP), network protocols (SNMP, MQTT)
- **Processor Plugins**: Data transformation (rename, convert), filtering (include/exclude), aggregation (statistics, sampling), enrichment (tags, calculations)
- **Output Plugins**: Time series databases (InfluxDB, Prometheus), message queues (Kafka, AMQP), cloud services (CloudWatch, DataDog)
- **Service Discovery**: Automatic discovery of services in Kubernetes, Consul, and cloud environments
- **Agent Management**: Configuration hot-reloading, internal monitoring, and distributed deployment patterns
- **External Plugins**: Custom plugin development with Go SDK and external process support

### Why Telegraf Dominates Metrics Collection

1. **Universal Compatibility**: 300+ plugins cover virtually every system, service, and protocol
2. **Lightweight Performance**: Minimal resource footprint with efficient Go-based architecture
3. **Operational Simplicity**: Single binary, single configuration file, minimal dependencies
4. **Production Ready**: Built-in buffering, error handling, and high availability patterns
5. **Ecosystem Integration**: Native support for all major monitoring and observability platforms

### Mental Model for Success

Think of Telegraf as a universal translator for metrics. Just as a human translator bridges communication between different languages, Telegraf bridges the metrics gap between diverse systems that speak different "languages" (protocols, formats, APIs) and the monitoring systems that need standardized, consistent data feeds.

Key insight: Telegraf excels when you need to standardize metrics collection across heterogeneous infrastructure while maintaining flexibility for custom requirements and avoiding vendor lock-in.

### Where to Start Your Journey

1. **Understand Metrics Fundamentals**: Learn about time series data, measurement types, and monitoring best practices.

2. **Master Configuration Syntax**: Understand TOML format and Telegraf's plugin configuration patterns.

3. **Explore Core Plugins**: Start with system metrics (CPU, memory, disk) before expanding to application-specific plugins.

4. **Practice Data Processing**: Learn to use processor plugins for filtering, transformation, and enrichment.

5. **Study Output Patterns**: Understand how to route metrics to different destinations based on requirements.

6. **Learn Production Deployment**: Master scaling strategies, high availability, and operational best practices.

### Key Concepts to Master

- **Plugin Architecture**: Understanding input, processor, and output plugin types and their interactions
- **Configuration Management**: TOML syntax, environment variables, and configuration validation
- **Data Model**: Tags, fields, measurements, and timestamps in time series context
- **Buffering and Batching**: Memory management and performance optimization techniques
- **Service Discovery**: Automatic discovery patterns for dynamic environments
- **Error Handling**: Retry logic, dead letter queues, and graceful degradation
- **Security Patterns**: TLS configuration, authentication, and secure credential management
- **Scaling Strategies**: Horizontal deployment, load balancing, and aggregation patterns

Telegraf represents the evolution from custom monitoring scripts to standardized, scalable metrics collection infrastructure. Master the plugin ecosystem, understand production deployment patterns, and gradually build expertise in advanced processing and integration techniques.

## Installation and Configuration

### Docker Installation

```bash
# Run Telegraf with Docker
docker run -d \
  --name telegraf \
  --restart always \
  -v $PWD/telegraf.conf:/etc/telegraf/telegraf.conf:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /sys:/host/sys:ro \
  -v /proc:/host/proc:ro \
  -v /etc:/host/etc:ro \
  --net host \
  --pid host \
  telegraf

# Docker Compose setup
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  telegraf:
    image: telegraf:latest
    container_name: telegraf
    restart: always
    hostname: telegraf-monitoring
    environment:
      - HOST_PROC=/host/proc
      - HOST_SYS=/host/sys
      - HOST_ETC=/host/etc
      - HOST_VAR=/host/var
      - HOST_RUN=/host/run
      - HOST_MOUNT_PREFIX=/host
    volumes:
      - ./telegraf.conf:/etc/telegraf/telegraf.conf:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /sys:/host/sys:ro
      - /proc:/host/proc:ro
      - /etc:/host/etc:ro
      - /var:/host/var:ro
      - /run:/host/run:ro
    network_mode: host
    pid: host
    cap_add:
      - SYS_PTRACE
      - CAP_SYS_ADMIN
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined

  influxdb:
    image: influxdb:2.7
    container_name: influxdb
    restart: always
    ports:
      - "8086:8086"
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=secure-password
      - DOCKER_INFLUXDB_INIT_ORG=platform-engineering
      - DOCKER_INFLUXDB_INIT_BUCKET=metrics
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token
    volumes:
      - influxdb_data:/var/lib/influxdb2

volumes:
  influxdb_data:
EOF
```

### Kubernetes Installation with Helm

```bash
# Add InfluxData Helm repository
helm repo add influxdata https://helm.influxdata.com/
helm repo update

# Install Telegraf DaemonSet
helm install telegraf influxdata/telegraf-ds \
  --namespace monitoring \
  --create-namespace \
  --values values.yaml
```

Example `values.yaml`:
```yaml
## Default values for telegraf DaemonSet
image:
  repo: telegraf
  tag: 1.28-alpine

## Configure the telegraf agent
config:
  agent:
    interval: "10s"
    round_interval: true
    metric_batch_size: 1000
    metric_buffer_limit: 10000
    collection_jitter: "0s"
    flush_interval: "10s"
    flush_jitter: "0s"
    precision: ""
    hostname: "$HOSTNAME"
    omit_hostname: false

  outputs:
    - influxdb_v2:
        urls:
          - "http://influxdb:8086"
        token: "$INFLUX_TOKEN"
        organization: "platform-engineering"
        bucket: "metrics"
        
  inputs:
    - cpu:
        percpu: true
        totalcpu: true
        collect_cpu_time: false
        report_active: false
    - disk:
        ignore_fs:
          - tmpfs
          - devtmpfs
          - devfs
          - iso9660
          - overlay
          - aufs
          - squashfs
    - diskio:
        skip_serial_number: true
    - kernel:
    - mem:
    - net:
        ignore_protocol_stats: false
    - processes:
    - swap:
    - system:
    - docker:
        endpoint: "unix:///var/run/docker.sock"
        gather_services: false
        source_tag: false
        container_name_include: []
        container_name_exclude: []
        timeout: "5s"
        perdevice: true
        total: false
    - kubernetes:
        url: "https://kubernetes.default.svc"
        bearer_token: "/var/run/secrets/kubernetes.io/serviceaccount/token"
        insecure_skip_verify: true

## Environment variables
env:
  - name: HOSTNAME
    valueFrom:
      fieldRef:
        fieldPath: spec.nodeName
  - name: INFLUX_TOKEN
    valueFrom:
      secretKeyRef:
        name: telegraf-secrets
        key: influx-token

## Resource limits
resources:
  requests:
    memory: 128Mi
    cpu: 100m
  limits:
    memory: 256Mi
    cpu: 200m

## Host mounted volumes
volumes:
  - name: sys
    hostPath:
      path: /sys
  - name: proc
    hostPath:
      path: /proc
  - name: docker-socket
    hostPath:
      path: /var/run/docker.sock
  - name: utmp
    hostPath:
      path: /var/run/utmp

mountPoints:
  - name: sys
    mountPath: /host/sys
    readOnly: true
  - name: docker-socket
    mountPath: /var/run/docker.sock
  - name: proc
    mountPath: /host/proc
    readOnly: true
  - name: utmp
    mountPath: /var/run/utmp
    readOnly: true

## Service Account
rbac:
  create: true
  clusterWide: true
  rules:
    - apiGroups: [""]
      resources: ["nodes", "nodes/stats", "nodes/metrics", "nodes/proxy", "pods", "services", "endpoints"]
      verbs: ["get", "list", "watch"]
```

### Basic Configuration

```toml
# telegraf.conf
# Global tags can be specified here in key="value" format.
[global_tags]
  environment = "production"
  region = "us-east-1"

# Configuration for telegraf agent
[agent]
  ## Default data collection interval for all inputs
  interval = "10s"
  
  ## Rounds collection interval to 'interval'
  round_interval = true

  ## Telegraf will send metrics to outputs in batches of at most
  ## metric_batch_size metrics.
  metric_batch_size = 1000

  ## Maximum number of unwritten metrics per output.
  metric_buffer_limit = 10000

  ## Collection jitter is used to jitter the collection by a random amount.
  collection_jitter = "0s"

  ## Default flushing interval for all outputs.
  flush_interval = "10s"
  
  ## Jitter the flush interval by a random amount.
  flush_jitter = "0s"

  ## By default or when set to "0s", precision will be set to the same
  ## timestamp order as the collection interval.
  precision = ""

  ## Override default hostname, if empty use os.Hostname()
  hostname = ""
  
  ## If set to true, do no set the "host" tag in the telegraf agent.
  omit_hostname = false
```

## Input Plugins

### System Metrics

```toml
# CPU metrics
[[inputs.cpu]]
  ## Whether to report per-cpu stats or not
  percpu = true
  ## Whether to report total system cpu stats or not
  totalcpu = true
  ## If true, collect raw CPU time metrics
  collect_cpu_time = false
  ## If true, compute and report the sum of all non-idle CPU states
  report_active = false

# Memory metrics
[[inputs.mem]]

# Disk metrics
[[inputs.disk]]
  ## By default stats will be gathered for all mount points.
  ## Set mount_points will restrict the stats to only the specified mount points.
  # mount_points = ["/"]

  ## Ignore mount points by filesystem type.
  ignore_fs = ["tmpfs", "devtmpfs", "devfs", "iso9660", "overlay", "aufs", "squashfs"]

# Network metrics
[[inputs.net]]
  ## By default, telegraf gathers stats from any up interface
  ## Setting interfaces will tell it to gather these explicit interfaces,
  ## regardless of status.
  # interfaces = ["eth0"]
  
  ## On linux systems telegraf also collects protocol stats.
  ## Setting ignore_protocol_stats to true will skip reporting of protocol metrics.
  # ignore_protocol_stats = false

# Process metrics
[[inputs.processes]]
```

### Container Metrics

```toml
# Docker metrics
[[inputs.docker]]
  ## Docker Endpoint
  endpoint = "unix:///var/run/docker.sock"

  ## Set to true to collect Swarm metrics(desired_replicas, running_replicas)
  gather_services = false

  ## Only collect metrics for these containers, collect all if empty
  container_names = []
  
  ## Deprecated (1.4.0), use container_names
  # container_name_include = []
  # container_name_exclude = []

  ## Container states to include and exclude
  container_state_include = ["created", "restarting", "running", "removing", "paused", "exited", "dead"]
  # container_state_exclude = ["created", "restarting", "removing", "paused", "exited", "dead"]

  ## Timeout for docker list, info, and stats commands
  timeout = "5s"

  ## Whether to report for each container per-device blkio (8:0, 8:1...),
  ## network (eth0, eth1, ...) and cpu (cpu0, cpu1, ...) stats or not
  perdevice = true
  
  ## Whether to report for each container total blkio and network stats or not
  total = false

# Kubernetes metrics
[[inputs.kubernetes]]
  ## URL for the kubelet
  url = "https://kubernetes.default.svc:443"

  ## Use bearer token for authorization
  bearer_token = "/var/run/secrets/kubernetes.io/serviceaccount/token"

  ## Set response_timeout (default 5 seconds)
  response_timeout = "5s"

  ## Optional TLS Config
  # tls_ca = /path/to/cafile
  # tls_cert = /path/to/certfile
  # tls_key = /path/to/keyfile
  ## Use TLS but skip chain & host verification
  insecure_skip_verify = true
```

### Application Metrics

```toml
# HTTP response check
[[inputs.http_response]]
  ## List of URLs to query
  urls = ["https://api.example.com/health"]
  
  ## Set http_proxy (telegraf uses the system wide proxy settings if it's is not set)
  # http_proxy = "http://localhost:8888"

  ## Set response_timeout (default 5 seconds)
  response_timeout = "5s"

  ## HTTP Request Method
  method = "GET"

  ## Whether to follow redirects from the server (defaults to false)
  follow_redirects = false

  ## Optional HTTP Request Body
  # body = '''{"id": 100}'''

  ## Optional HTTP headers
  headers = [
    "Authorization: Bearer $API_TOKEN"
  ]

  ## Interface to use when dialing an address
  # interface = "eth0"

# Prometheus format scraping
[[inputs.prometheus]]
  ## An array of urls to scrape metrics from.
  urls = ["http://localhost:9100/metrics"]

  ## Metric version controls the mapping from Prometheus metrics into
  ## Telegraf metrics.
  metric_version = 2

  ## Interval to rescrape metrics from urls
  interval = "60s"

  ## Timeout for metric scraping
  timeout = "5s"

# StatsD Server
[[inputs.statsd]]
  ## Protocol, must be "tcp", "udp4", "udp6", or "udp" (default=udp)
  protocol = "udp"

  ## Maximum number of concurrent TCP connections to allow
  max_tcp_connections = 250

  ## Enable TCP keep alive probes (default=false)
  tcp_keep_alive = false

  ## Address and port to host UDP listener on
  service_address = ":8125"

  ## The following configuration options control when telegraf clears it's cache
  delete_gauges = true
  delete_counters = true
  delete_sets = true
  delete_timings = true

  ## Percentiles to calculate for timing & histogram stats.
  percentiles = [50.0, 90.0, 99.0, 99.9, 100.0]

  ## Number of UDP messages allowed to queue up, once filled,
  ## the statsd server will start dropping packets
  allowed_pending_messages = 10000

  ## Number of timing/histogram values to track per-measurement in the
  ## calculation of percentiles. Raising this limit increases the accuracy
  ## of percentiles but also increases the memory usage and cpu time.
  percentile_limit = 1000
```

### Custom Script Input

```toml
# Execute a command
[[inputs.exec]]
  ## Commands array
  commands = [
    "/usr/bin/custom-metrics.sh",
    "/usr/bin/python3 /scripts/collect_metrics.py"
  ]

  ## Timeout for each command to complete.
  timeout = "5s"

  ## measurement name suffix (for separating different commands)
  name_suffix = "_custom"

  ## Data format to consume.
  data_format = "influx"

# Read metrics from a file
[[inputs.file]]
  ## Files to parse each interval.  Accept standard unix glob matching rules,
  files = ["/tmp/metrics.json"]

  ## Data format to consume.
  data_format = "json"

  ## Tag keys to extract from file path
  file_tag = "filename"
```

## Output Plugins

### Time Series Databases

```toml
# InfluxDB v2 Output
[[outputs.influxdb_v2]]
  ## The URLs of the InfluxDB cluster nodes.
  urls = ["http://influxdb:8086"]

  ## Token for authentication.
  token = "$INFLUX_TOKEN"

  ## Organization is the name of the organization you wish to write to.
  organization = "platform-engineering"

  ## Destination bucket to write into.
  bucket = "metrics"

  ## The value of this tag will be used to determine the bucket.
  # bucket_tag = ""

  ## If true, the bucket tag will not be added to the metric.
  # exclude_bucket_tag = false

  ## Timeout for HTTP messages.
  timeout = "5s"

  ## Additional HTTP headers
  # http_headers = {"X-Special-Header" = "Special-Value"}

  ## HTTP Proxy override, if unset values the standard proxy environment
  ## variables are consulted to determine which proxy, if any, should be used.
  # http_proxy = "http://corporate.proxy:3128"

# Prometheus Output
[[outputs.prometheus_client]]
  ## Address to listen on
  listen = ":9273"

  ## Metric version controls the mapping from Telegraf metrics into
  ## Prometheus format.
  metric_version = 2

  ## Use HTTP Basic Authentication.
  # basic_username = "Foo"
  # basic_password = "Bar"

  ## If set, the IP Ranges which are allowed to access metrics.
  # ip_range = ["192.168.0.0/24", "192.168.1.0/30"]

  ## Path to publish the metrics on.
  path = "/metrics"

  ## Expiration interval for each metric.
  expiration_interval = "60s"

  ## Collectors to enable, valid entries are "gocollector" and "process".
  collectors_exclude = ["gocollector", "process"]

  ## Send string metrics as Prometheus labels.
  string_as_label = true

  ## If set, enable TLS with the given certificate.
  # tls_cert = "/etc/ssl/telegraf.crt"
  # tls_key = "/etc/ssl/telegraf.key"

# Elasticsearch Output
[[outputs.elasticsearch]]
  ## The full HTTP endpoint URL for your Elasticsearch instance
  urls = ["http://elasticsearch:9200"]
  
  ## Elasticsearch client timeout
  timeout = "5s"
  
  ## Index Config
  ## The target index for metrics
  index_name = "telegraf-%Y.%m.%d"
  
  ## Set to true to have Telegraf manage the index template
  manage_template = true
  
  ## The template name used for telegraf indexes
  template_name = "telegraf"
  
  ## Set to true to overwrite an existing template
  overwrite_template = false
  
  ## Set to true to force ES to use the ID specified in the metric as the document ID
  force_document_id = false

  ## Optional TLS Config
  # tls_ca = "/etc/telegraf/ca.pem"
  # tls_cert = "/etc/telegraf/cert.pem"
  # tls_key = "/etc/telegraf/key.pem"
```

### Message Queues

```toml
# Kafka Output
[[outputs.kafka]]
  ## URLs of kafka brokers
  brokers = ["kafka1:9092", "kafka2:9092", "kafka3:9092"]
  
  ## Kafka topic for producer messages
  topic = "telegraf-metrics"
  
  ## Optional topic suffix configuration.
  ## If the section is omitted, no suffix is used.
  ## Following topic suffix methods are supported:
  ##   measurement - suffix equals to separator + measurement's name
  ##   tags        - suffix equals to separator + specified tags' values
  ##                 separated by "_"
  ##
  ## Suffix equals to "_" + measurement name
  # [outputs.kafka.topic_suffix]
  #   method = "measurement"
  #   separator = "_"
  
  ## Suffix equals to "_" + tag1[0:2] + "_" + tag2[0:2]
  # [outputs.kafka.topic_suffix]
  #   method = "tags"
  #   separator = "_"
  #   keys = ["tag1[:2]", "tag2[:2]"]

  ## Compression codec
  compression_codec = 2 # 0=none, 1=gzip, 2=snappy, 3=lz4, 4=zstd

  ## RequiredAcks is used in Produce Requests to tell the broker how many
  ## replica acknowledgements it must see before responding
  required_acks = -1 # 0=none, 1=leader, -1=all

  ## Maximum number of times to retry sending a metric before failing.
  max_retry = 3

  ## Maximum number of messages to send in a single batch.
  max_message_bytes = 1000000

  ## The maximum permitted size of a message.
  ## Should be set equal to or smaller than the broker's `message.max.bytes`.
  max_message_bytes = 1000000

# AMQP (RabbitMQ) Output
[[outputs.amqp]]
  ## Broker to publish to.
  url = "amqp://guest:guest@localhost:5672/"
  
  ## Exchange to publish to.
  exchange = "telegraf"

  ## Exchange type; common types are "direct", "fanout", "topic", "headers", "x-consistent-hash".
  exchange_type = "topic"

  ## If true, exchange will be passively declared.
  exchange_passive = false

  ## Exchange durability can be either "transient" or "durable".
  exchange_durability = "durable"

  ## Additional exchange arguments.
  # exchange_arguments = { }

  ## Authentication credentials for the PLAIN auth_method.
  # username = ""
  # password = ""

  ## Auth method. PLAIN and EXTERNAL are supported
  # auth_method = "PLAIN"

  ## Metric tag to use as a routing key.
  routing_tag = "host"

  ## Delivery Mode controls if a published message is persistent.
  delivery_mode = 2
```

## Processors

### Data Transformation

```toml
# Rename measurements, tags, and fields
[[processors.rename]]
  ## Specify one sub-table per rename operation.
  [[processors.rename.replace]]
    measurement = "cpu"
    dest = "system_cpu"

  [[processors.rename.replace]]
    tag = "hostname"
    dest = "host"

  [[processors.rename.replace]]
    field = "usage_percentage"
    dest = "usage_pct"

# Convert values to another type
[[processors.converter]]
  [processors.converter.tags]
    ## Tag names to convert to strings
    string = ["environment", "region"]
    
  [processors.converter.fields]
    ## Field names to convert to floats
    float = ["temperature", "humidity"]
    
    ## Field names to convert to integers
    integer = ["count", "size"]
    
    ## Field names to convert to booleans
    boolean = ["active", "enabled"]

# Add or modify tags
[[processors.strings]]
  ## Convert a field value to uppercase
  [[processors.strings.uppercase]]
    field = "status"

  ## Convert a tag value to lowercase
  [[processors.strings.lowercase]]
    tag = "environment"

  ## Trim leading and trailing whitespace
  [[processors.strings.trim]]
    field = "message"

  ## Replace all occurrences of old with new
  [[processors.strings.replace]]
    tag = "path"
    old = "/"
    new = "_"

# Regex processing
[[processors.regex]]
  [[processors.regex.tags]]
    ## Tag to change
    key = "service"
    ## Regular expression to match
    pattern = "^([^_]+)_.*$"
    ## Replacement string
    replacement = "${1}"
```

### Filtering and Aggregation

```toml
# Filter metrics
[[processors.filter]]
  ## Select metrics to pass through
  namepass = ["cpu", "mem", "disk"]
  
  ## Select metrics to drop
  namedrop = ["cpu_guest*"]

  ## Select fields to pass through
  fieldpass = ["usage*", "free"]
  
  ## Select fields to drop
  fielddrop = ["time_*"]

  ## Select tags to pass through
  tagpass = {
    cpu = ["cpu0", "cpu1"]
    host = ["server*"]
  }
  
  ## Select tags to drop
  tagdrop = {
    fstype = ["tmpfs", "devfs"]
  }

# Deduplicate metrics
[[processors.dedup]]
  ## Maximum time to suppress output
  dedup_interval = "600s"

# TopK aggregation
[[processors.topk]]
  ## How many fields to keep
  k = 10
  
  ## Period to calculate TopK over
  period = 10
  
  ## Aggregation to use for the period (sum, mean, min, max)
  aggregation = "mean"
  
  ## Groupby fields
  group_by = ["host", "service"]

# Aggregation
[[processors.basicstats]]
  ## The period on which to flush & reset the aggregator.
  period = "30s"
  
  ## If true, the original metric will be dropped by the
  ## aggregator and will not get sent to the output plugins.
  drop_original = false
  
  ## Configures which basic stats to push as fields
  stats = ["count", "min", "max", "mean", "stdev", "sum"]
```

## Service Discovery

### Kubernetes Service Discovery

```toml
# Discover Kubernetes pods
[[inputs.prometheus]]
  ## Use Kubernetes service discovery
  kubernetes_services = ["http://my-service.my-namespace.svc.cluster.local:9100/metrics"]
  
  ## Use Kubernetes label selector to target pods
  kubernetes_label_selector = "app=my-app,environment=production"
  
  ## Monitor pods in specific namespaces
  kubernetes_namespace = "default"

# Kubernetes pod annotations
# Add these annotations to your pods:
# telegraf.influxdata.com/port: "9100"
# telegraf.influxdata.com/path: "/metrics"
# telegraf.influxdata.com/scheme: "http"
# telegraf.influxdata.com/interval: "30s"
```

### Consul Service Discovery

```toml
[[inputs.consul]]
  ## Consul server address
  address = "consul.service.consul:8500"
  
  ## Datacenter to query
  datacenter = "dc1"
  
  ## Service discovery tag filters
  tag_filter = ["monitoring", "telegraf"]
  
  ## Discover services with health status
  health_check = "passing"
```

## Performance Optimization

### Batching and Buffering

```toml
[agent]
  ## Increase batch size for high-volume metrics
  metric_batch_size = 5000
  
  ## Increase buffer size to handle spikes
  metric_buffer_limit = 50000
  
  ## Adjust flush interval based on output capacity
  flush_interval = "10s"
  
  ## Enable collection timing
  collection_timing_enabled = true
  
  ## Log collection timing
  debug = false
  quiet = false
  
  ## Override default hostname
  hostname = "telegraf-${HOSTNAME}"
  
  ## Round collection interval
  round_interval = true
```

### Memory Management

```toml
# Limit memory usage for specific plugins
[[inputs.tail]]
  ## Files to tail
  files = ["/var/log/application/*.log"]
  
  ## Only tail the last N lines
  from_beginning = false
  
  ## Maximum lines to buffer
  max_undelivered_lines = 1000

# Use sampling for high-volume metrics
[[processors.sample]]
  ## Sample every Nth metric
  sample_rate = 10
  
  ## Only sample specific measurements
  namepass = ["high_volume_metric"]
```

### Output Optimization

```toml
# Optimize InfluxDB output
[[outputs.influxdb_v2]]
  ## Use compression
  content_encoding = "gzip"
  
  ## Increase timeout for large batches
  timeout = "30s"
  
  ## Enable retry logic
  retry_interval = "1s"
  max_retry_interval = "30s"
  max_retry_time = "1m"

# Load balance across multiple outputs
[[outputs.influxdb_v2]]
  urls = ["http://influx1:8086"]
  bucket = "metrics"
  organization = "org"
  token = "$TOKEN"

[[outputs.influxdb_v2]]
  urls = ["http://influx2:8086"]
  bucket = "metrics"
  organization = "org"
  token = "$TOKEN"
```

## Best Practices

### 1. Configuration Management

```toml
# Use environment variables for sensitive data
[[outputs.influxdb_v2]]
  token = "$INFLUX_TOKEN"
  organization = "$INFLUX_ORG"

# Include additional configuration files
[agent]
  ## Include configuration directory
  # config_directory = "/etc/telegraf/telegraf.d"

# Use templates for dynamic configuration
[[inputs.cpu]]
  name_override = "cpu_${DATACENTER}_${ENVIRONMENT}"
```

### 2. Monitoring Telegraf

```toml
# Enable internal metrics
[[inputs.internal]]
  ## Collect internal telegraf metrics
  collect_memstats = true
  
  ## Report per-plugin metrics
  [inputs.internal.tags]
    telegraf_type = "internal"

# Monitor Telegraf process
[[inputs.procstat]]
  pattern = "telegraf"
  
  ## Monitor process metrics
  pid_finder = "pgrep"
  
  ## Include child processes
  include_children = false
```

### 3. Error Handling

```toml
# Configure logging
[agent]
  ## Log at debug level
  debug = false
  
  ## Log only error level messages
  quiet = false
  
  ## Log file
  logfile = "/var/log/telegraf/telegraf.log"
  
  ## Rotate logfile
  logfile_rotation_interval = "1d"
  logfile_rotation_max_size = "100MB"
  logfile_rotation_max_archives = 5

# Handle plugin errors gracefully
[[inputs.ping]]
  urls = ["google.com", "amazon.com"]
  
  ## Number of pings to send per collection
  count = 3
  
  ## Ping timeout
  timeout = 2.0
  
  ## Interface to send ping from
  # interface = "eth0"
  
  ## Log ping errors
  log_errors = true
```

### 4. Security Configuration

```toml
# Use TLS for outputs
[[outputs.influxdb_v2]]
  urls = ["https://influxdb:8086"]
  
  ## Optional TLS Config
  tls_ca = "/etc/telegraf/ca.pem"
  tls_cert = "/etc/telegraf/cert.pem"
  tls_key = "/etc/telegraf/key.pem"
  
  ## Use TLS but skip chain & host verification
  # insecure_skip_verify = false

# Secure input plugins
[[inputs.http_listener_v2]]
  ## Address and port to host HTTP listener on
  service_address = ":8080"
  
  ## HTTPS configuration
  tls_cert = "/etc/telegraf/cert.pem"
  tls_key = "/etc/telegraf/key.pem"
  
  ## Use mutual TLS
  tls_allowed_cacerts = ["/etc/telegraf/ca.pem"]
  
  ## Basic authentication
  basic_username = "telegraf"
  basic_password = "$BASIC_PASSWORD"
```

## Production Deployment Patterns

### Kubernetes DaemonSet

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: telegraf-config
  namespace: monitoring
data:
  telegraf.conf: |
    [global_tags]
      cluster = "production"
    
    [agent]
      interval = "10s"
      round_interval = true
      metric_batch_size = 1000
      metric_buffer_limit = 10000
      collection_jitter = "0s"
      flush_interval = "10s"
      flush_jitter = "0s"
      precision = ""
      hostname = "$HOSTNAME"
      omit_hostname = false
    
    [[outputs.influxdb_v2]]
      urls = ["http://influxdb:8086"]
      token = "$INFLUX_TOKEN"
      organization = "platform-engineering"
      bucket = "metrics"
    
    [[inputs.cpu]]
      percpu = true
      totalcpu = true
    
    [[inputs.disk]]
      ignore_fs = ["tmpfs", "devtmpfs"]
    
    [[inputs.diskio]]
    
    [[inputs.kernel]]
    
    [[inputs.mem]]
    
    [[inputs.processes]]
    
    [[inputs.swap]]
    
    [[inputs.system]]
    
    [[inputs.kubernetes]]
      url = "https://kubernetes.default.svc:443"
      bearer_token = "/var/run/secrets/kubernetes.io/serviceaccount/token"
      insecure_skip_verify = true
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: telegraf
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: telegraf
  template:
    metadata:
      labels:
        app: telegraf
    spec:
      serviceAccountName: telegraf
      hostNetwork: true
      hostPID: true
      containers:
      - name: telegraf
        image: telegraf:1.28-alpine
        env:
        - name: HOSTNAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: HOST_PROC
          value: "/host/proc"
        - name: HOST_SYS
          value: "/host/sys"
        - name: HOST_MOUNT_PREFIX
          value: "/host"
        - name: INFLUX_TOKEN
          valueFrom:
            secretKeyRef:
              name: telegraf-secrets
              key: influx-token
        resources:
          requests:
            memory: 128Mi
            cpu: 100m
          limits:
            memory: 256Mi
            cpu: 200m
        volumeMounts:
        - name: sys
          mountPath: /host/sys
          readOnly: true
        - name: proc
          mountPath: /host/proc
          readOnly: true
        - name: docker-socket
          mountPath: /var/run/docker.sock
        - name: utmp
          mountPath: /var/run/utmp
          readOnly: true
        - name: config
          mountPath: /etc/telegraf
      terminationGracePeriodSeconds: 30
      volumes:
      - name: sys
        hostPath:
          path: /sys
      - name: proc
        hostPath:
          path: /proc
      - name: docker-socket
        hostPath:
          path: /var/run/docker.sock
      - name: utmp
        hostPath:
          path: /var/run/utmp
      - name: config
        configMap:
          name: telegraf-config
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: telegraf
  namespace: monitoring
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: telegraf
rules:
- apiGroups: [""]
  resources: ["nodes", "nodes/stats", "nodes/metrics", "nodes/proxy"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods", "services", "endpoints"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: telegraf
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: telegraf
subjects:
- kind: ServiceAccount
  name: telegraf
  namespace: monitoring
```

### High Availability Configuration

```toml
# Use multiple output destinations for redundancy
[[outputs.influxdb_v2]]
  urls = ["http://influxdb-primary:8086"]
  token = "$INFLUX_TOKEN"
  organization = "platform-engineering"
  bucket = "metrics"
  
  ## If this output fails, continue to next output
  # namepass = ["cpu", "mem", "disk"]

[[outputs.influxdb_v2]]
  urls = ["http://influxdb-secondary:8086"]
  token = "$INFLUX_TOKEN"
  organization = "platform-engineering"
  bucket = "metrics"
  
  ## Only write to secondary if primary fails
  # namedrop = ["cpu", "mem", "disk"]

# Use Kafka for reliable delivery
[[outputs.kafka]]
  brokers = ["kafka1:9092", "kafka2:9092", "kafka3:9092"]
  topic = "telegraf-metrics"
  compression_codec = 2
  required_acks = -1
  max_retry = 3
  
  ## Use consistent hashing for load distribution
  routing_key = "host"
  
  ## Enable idempotent writes
  idempotent_writes = true
```

### Scaling Strategies

```yaml
# Telegraf relay configuration for aggregation
apiVersion: v1
kind: ConfigMap
metadata:
  name: telegraf-relay-config
data:
  telegraf.conf: |
    # Relay configuration
    [[inputs.influxdb_listener]]
      service_address = ":8186"
      
    [[processors.aggregator]]
      period = "30s"
      drop_original = true
      
      [[processors.aggregator.aggregator]]
        measurement = "cpu"
        fields = ["usage_idle", "usage_user", "usage_system"]
        function = "mean"
        
    [[outputs.influxdb_v2]]
      urls = ["http://influxdb:8086"]
      token = "$INFLUX_TOKEN"
      organization = "platform-engineering"
      bucket = "metrics-aggregated"
```

## Comprehensive Resources

### Official Documentation
- [Telegraf Documentation](https://docs.influxdata.com/telegraf/)
- [Plugin Directory](https://docs.influxdata.com/telegraf/latest/plugins/)
- [Configuration Examples](https://github.com/influxdata/telegraf/tree/master/plugins)
- [Telegraf GitHub](https://github.com/influxdata/telegraf)

### Books and Guides
- "Managing Infrastructure with Telegraf" by InfluxData
- [Telegraf Best Practices](https://docs.influxdata.com/telegraf/latest/best_practices/)
- [Performance Tuning Guide](https://docs.influxdata.com/telegraf/latest/administration/performance/)
- [Security Best Practices](https://docs.influxdata.com/telegraf/latest/administration/security/)

### Plugin Development
- [Writing Custom Plugins](https://github.com/influxdata/telegraf/blob/master/CONTRIBUTING.md)
- [External Plugin System](https://github.com/influxdata/telegraf/tree/master/plugins/common/shim)
- [Plugin API Documentation](https://pkg.go.dev/github.com/influxdata/telegraf)
- [Example Plugins](https://github.com/influxdata/telegraf/tree/master/plugins/inputs)

### Community Resources
- [InfluxData Community](https://community.influxdata.com/c/telegraf/)
- [Telegraf Slack Channel](https://influxdata.com/slack)
- [Community Templates](https://github.com/influxdata/community-templates)
- [Awesome Telegraf](https://github.com/influxdata/awesome-telegraf)

### Integration Guides
- [Kubernetes Monitoring](https://docs.influxdata.com/telegraf/latest/guides/kubernetes/)
- [Docker Monitoring](https://docs.influxdata.com/telegraf/latest/guides/docker/)
- [Cloud Provider Integration](https://docs.influxdata.com/telegraf/latest/guides/cloud/)
- [Application Monitoring](https://docs.influxdata.com/telegraf/latest/guides/applications/)

### Training and Certification
- [InfluxDB University](https://university.influxdata.com/)
- [Telegraf Training Course](https://university.influxdata.com/courses/telegraf-training/)
- [Time Series Data Collection](https://university.influxdata.com/courses/data-collection/)
- [Monitoring Best Practices](https://www.influxdata.com/training/)

### Related Tools
- [InfluxDB](https://www.influxdata.com/products/influxdb/) - Time series database
- [Chronograf](https://www.influxdata.com/time-series-platform/chronograf/) - Visualization
- [Kapacitor](https://www.influxdata.com/time-series-platform/kapacitor/) - Real-time streaming
- [Flux](https://www.influxdata.com/products/flux/) - Data scripting language