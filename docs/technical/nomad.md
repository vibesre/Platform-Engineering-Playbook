# HashiCorp Nomad

## Overview

Nomad is a simple and flexible orchestrator by HashiCorp designed to deploy and manage containers and non-containerized applications across on-premises and cloud environments at scale. It supports multiple workload types including Docker, VMs, Java, and static binaries.

## Architecture

### Core Components

#### Nomad Servers
```
┌─────────────────────────────────────┐
│         Nomad Server Cluster        │
├─────────────┬──────────┬───────────┤
│   Leader    │ Follower │ Follower  │
│   Server    │ Server   │ Server    │
└──────┬──────┴────┬─────┴─────┬─────┘
       │           │           │
       └───────────┴───────────┘
              Raft Consensus
```

#### Nomad Architecture
```yaml
nomad_cluster:
  servers:
    - role: leader
      components:
        - scheduler
        - plan_queue
        - eval_broker
        - deployment_watcher
        - raft_store
    
  clients:
    - role: worker
      components:
        - task_driver
        - fingerprinter
        - client_state_store
        - allocation_runner
  
  integrations:
    service_discovery: consul
    secrets_management: vault
    metrics: prometheus
```

### Job Types

#### Service Jobs
```hcl
job "web-app" {
  type = "service"
  
  group "frontend" {
    count = 3
    
    task "nginx" {
      driver = "docker"
      
      config {
        image = "nginx:1.25"
        ports = ["http"]
      }
    }
  }
}
```

#### Batch Jobs
```hcl
job "data-processor" {
  type = "batch"
  
  periodic {
    cron = "0 * * * *"
  }
  
  group "process" {
    task "etl" {
      driver = "docker"
      
      config {
        image = "company/etl:latest"
      }
    }
  }
}
```

#### System Jobs
```hcl
job "node-exporter" {
  type = "system"
  
  group "monitoring" {
    task "exporter" {
      driver = "docker"
      
      config {
        image = "prom/node-exporter:latest"
        network_mode = "host"
      }
    }
  }
}
```

## Installation

### Binary Installation
```bash
# Download Nomad
NOMAD_VERSION="1.7.3"
wget https://releases.hashicorp.com/nomad/${NOMAD_VERSION}/nomad_${NOMAD_VERSION}_linux_amd64.zip
unzip nomad_${NOMAD_VERSION}_linux_amd64.zip
sudo mv nomad /usr/local/bin/

# Verify installation
nomad version

# Create system user and directories
sudo useradd --system --shell /bin/false nomad
sudo mkdir -p /opt/nomad /etc/nomad
sudo chown nomad:nomad /opt/nomad
```

### Server Configuration
```hcl
# /etc/nomad/server.hcl
datacenter = "dc1"
data_dir = "/opt/nomad"

server {
  enabled = true
  bootstrap_expect = 3
  
  server_join {
    retry_join = ["nomad-server-1", "nomad-server-2", "nomad-server-3"]
    retry_max = 5
    retry_interval = "15s"
  }
  
  raft_protocol = 3
}

# Consul integration
consul {
  address = "127.0.0.1:8500"
  server_service_name = "nomad"
  server_auto_join = true
  client_service_name = "nomad-client"
  client_auto_join = true
}

# Vault integration
vault {
  enabled = true
  address = "http://vault.service.consul:8200"
}

# ACL configuration
acl {
  enabled = true
}

# TLS configuration
tls {
  http = true
  rpc  = true
  
  ca_file   = "/etc/nomad/tls/ca.crt"
  cert_file = "/etc/nomad/tls/server.crt"
  key_file  = "/etc/nomad/tls/server.key"
  
  verify_server_hostname = true
  verify_https_client    = true
}
```

### Client Configuration
```hcl
# /etc/nomad/client.hcl
datacenter = "dc1"
data_dir = "/opt/nomad"

client {
  enabled = true
  servers = ["nomad.service.consul:4647"]
  
  node_class = "compute"
  
  options = {
    "driver.raw_exec.enable" = "0"
    "docker.auth.config" = "/etc/docker/config.json"
    "docker.volumes.enabled" = true
  }
}

# Plugin configuration
plugin "docker" {
  config {
    endpoint = "unix:///var/run/docker.sock"
    
    gc {
      image       = true
      image_delay = "3m"
      container   = true
    }
    
    volumes {
      enabled = true
    }
    
    allow_privileged = false
    allow_caps = ["NET_ADMIN", "SYS_TIME"]
  }
}

# Host volumes
host_volume "data" {
  path      = "/mnt/data"
  read_only = false
}

# Consul integration
consul {
  address = "127.0.0.1:8500"
}

# Telemetry
telemetry {
  publish_allocation_metrics = true
  publish_node_metrics       = true
  prometheus_metrics         = true
}
```

### Systemd Service
```ini
# /etc/systemd/system/nomad.service
[Unit]
Description=Nomad
Documentation=https://nomadproject.io
Wants=network-online.target
After=network-online.target

[Service]
Type=notify
User=nomad
Group=nomad
ExecStart=/usr/local/bin/nomad agent -config=/etc/nomad
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartSec=2
TasksMax=infinity
OOMScoreAdjust=-1000

[Install]
WantedBy=multi-user.target
```

## Job Specifications

### Advanced Job Configuration
```hcl
job "microservice" {
  datacenters = ["dc1", "dc2"]
  type = "service"
  priority = 50
  
  # Constraints
  constraint {
    attribute = "${node.class}"
    operator  = "="
    value     = "compute"
  }
  
  # Spread across availability zones
  spread {
    attribute = "${node.datacenter}"
    target "dc1" {
      percent = 50
    }
    target "dc2" {
      percent = 50
    }
  }
  
  # Update strategy
  update {
    max_parallel      = 2
    min_healthy_time  = "30s"
    healthy_deadline  = "5m"
    progress_deadline = "10m"
    auto_revert       = true
    auto_promote      = true
    canary            = 2
  }
  
  # Multi-region deployment
  multiregion {
    strategy {
      max_parallel = 1
      on_failure   = "fail_all"
    }
    
    region "us-west" {
      count = 3
      datacenters = ["us-west-1"]
    }
    
    region "us-east" {
      count = 3
      datacenters = ["us-east-1"]
    }
  }
  
  group "api" {
    count = 5
    
    # Scaling policy
    scaling {
      enabled = true
      min = 3
      max = 10
      
      policy {
        evaluation_interval = "5s"
        cooldown           = "1m"
        
        check "cpu" {
          source = "prometheus"
          query  = "avg(nomad_client_allocs_cpu_total_percent{task='api'})"
          
          strategy "target-value" {
            target = 70
          }
        }
      }
    }
    
    # Network configuration
    network {
      mode = "bridge"
      port "http" {
        static = 8080
        to     = 8080
      }
    }
    
    # Service discovery
    service {
      name = "api"
      port = "http"
      tags = ["urlprefix-/api"]
      
      check {
        type     = "http"
        path     = "/health"
        interval = "10s"
        timeout  = "2s"
      }
      
      # Consul Connect
      connect {
        sidecar_service {
          proxy {
            upstreams {
              destination_name = "database"
              local_bind_port  = 5432
            }
          }
        }
      }
    }
    
    task "api" {
      driver = "docker"
      
      config {
        image = "company/api:${NOMAD_META_VERSION}"
        ports = ["http"]
      }
      
      # Resources
      resources {
        cpu    = 500
        memory = 256
        
        device "nvidia/gpu" {
          count = 1
          
          constraint {
            attribute = "${device.attr.memory}"
            operator  = ">="
            value     = "4GiB"
          }
        }
      }
      
      # Environment variables
      env {
        LOG_LEVEL = "info"
        PORT      = "${NOMAD_PORT_http}"
      }
      
      # Vault secrets
      vault {
        policies = ["api-policy"]
      }
      
      template {
        data = <<EOH
{{ with secret "database/creds/api" }}
DB_USERNAME={{ .Data.username }}
DB_PASSWORD={{ .Data.password }}
{{ end }}
EOH
        destination = "secrets/db.env"
        env         = true
      }
      
      # Artifacts
      artifact {
        source      = "s3://artifacts/configs/api.yaml"
        destination = "local/config.yaml"
      }
      
      # Logs
      logs {
        max_files     = 10
        max_file_size = 10
      }
    }
  }
}
```

### Template Stanza Examples
```hcl
# Dynamic configuration
template {
  data = <<EOH
server:
  host: 0.0.0.0
  port: {{ env "NOMAD_PORT_http" }}

{{ range service "postgres" }}
database:
  host: {{ .Address }}
  port: {{ .Port }}
{{ end }}
EOH
  destination = "local/config.yaml"
  change_mode = "restart"
  change_signal = "SIGHUP"
}

# Consul KV integration
template {
  data = <<EOH
{{ key "config/app/features" | parseJSON | toJSON }}
EOH
  destination = "local/features.json"
}
```

## Cluster Management

### Bootstrapping
```bash
# Initialize ACL system
nomad acl bootstrap

# Save bootstrap token
export NOMAD_TOKEN="<bootstrap-token>"

# Create management policy
cat <<EOF > management.hcl
namespace "*" {
  policy = "write"
}
node {
  policy = "write"
}
agent {
  policy = "write"
}
operator {
  policy = "write"
}
quota {
  policy = "write"
}
EOF

nomad acl policy apply -description "Management policy" management management.hcl
```

### Cluster Operations
```bash
# Server members
nomad server members

# Node status
nomad node status

# Drain node for maintenance
nomad node drain -enable -deadline 5m <node-id>

# Node eligibility
nomad node eligibility -enable <node-id>

# Garbage collection
nomad system gc

# Reconcile summaries
nomad system reconcile summaries
```

### Federation
```hcl
# federated.hcl
region_servers {
  "us-west" = ["nomad-west-1:4648", "nomad-west-2:4648"]
  "us-east" = ["nomad-east-1:4648", "nomad-east-2:4648"]
  "eu-west" = ["nomad-eu-1:4648", "nomad-eu-2:4648"]
}

# Enable gossip between regions
serf {
  enabled = true
}
```

## Workload Types

### Docker Containers
```hcl
task "webapp" {
  driver = "docker"
  
  config {
    image = "webapp:latest"
    ports = ["http"]
    
    # Docker options
    volumes = [
      "local/config:/etc/app",
      "secrets:/run/secrets:ro"
    ]
    
    mount {
      type     = "bind"
      source   = "secrets/ssl"
      target   = "/etc/ssl/private"
      readonly = true
    }
    
    labels {
      environment = "production"
      service     = "webapp"
    }
    
    # Resource limits
    memory_hard_limit = 512
    
    # Logging
    logging {
      type = "fluentd"
      config {
        fluentd-address = "localhost:24224"
        tag             = "docker.webapp"
      }
    }
  }
}
```

### Java Applications
```hcl
task "java-app" {
  driver = "java"
  
  config {
    class_path = "local/app.jar"
    class      = "com.company.Main"
    args       = ["--server.port=${NOMAD_PORT_http}"]
    jvm_options = ["-Xmx512m", "-Xms256m"]
  }
  
  artifact {
    source = "https://releases.company.com/app/v1.0.0/app.jar"
  }
}
```

### Static Binaries
```hcl
task "binary" {
  driver = "exec"
  
  config {
    command = "local/myapp"
    args    = ["--config", "local/config.json"]
  }
  
  artifact {
    source = "https://releases.company.com/myapp/linux/amd64/myapp"
    mode   = "file"
  }
}
```

### QEMU VMs
```hcl
task "vm" {
  driver = "qemu"
  
  config {
    image_path = "local/ubuntu.qcow2"
    accelerator = "kvm"
    args = [
      "-m", "1024",
      "-smp", "2"
    ]
    port_map {
      ssh = 22
    }
  }
  
  artifact {
    source = "https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img"
  }
}
```

## Service Mesh & Networking

### Consul Connect Integration
```hcl
job "api-gateway" {
  group "gateway" {
    network {
      mode = "bridge"
    }
    
    service {
      name = "api-gateway"
      port = "8080"
      
      connect {
        sidecar_service {
          proxy {
            upstreams {
              destination_name = "backend-api"
              local_bind_port  = 5000
            }
            upstreams {
              destination_name = "auth-service"
              local_bind_port  = 5001
            }
          }
        }
        
        sidecar_task {
          resources {
            cpu    = 50
            memory = 64
          }
        }
      }
    }
    
    task "gateway" {
      driver = "docker"
      
      config {
        image = "api-gateway:latest"
      }
      
      env {
        BACKEND_URL = "http://localhost:5000"
        AUTH_URL    = "http://localhost:5001"
      }
    }
  }
}
```

### CNI Networking
```hcl
# Network isolation with CNI
group "secure" {
  network {
    mode = "cni/cilium"
    port "http" {
      to = 8080
    }
  }
  
  service {
    name = "secure-service"
    port = "http"
    
    check {
      type     = "http"
      path     = "/health"
      interval = "10s"
    }
  }
}
```

## Monitoring & Observability

### Prometheus Integration
```hcl
# Prometheus scraping configuration
telemetry {
  prometheus_metrics = true
  disable_hostname   = true
  publish_allocation_metrics = true
  publish_node_metrics       = true
}

# Prometheus job
job "prometheus" {
  type = "service"
  
  group "monitoring" {
    task "prometheus" {
      driver = "docker"
      
      template {
        data = <<EOH
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'nomad_metrics'
    consul_sd_configs:
      - server: '{{ env "NOMAD_IP_http" }}:8500'
        services: ['nomad-client', 'nomad']
    
    relabel_configs:
      - source_labels: ['__meta_consul_tags']
        regex: '(.*)http(.*)'
        action: keep
    
    scrape_interval: 5s
    metrics_path: /v1/metrics
    params:
      format: ['prometheus']
EOH
        destination = "local/prometheus.yml"
      }
      
      config {
        image = "prom/prometheus:latest"
        volumes = ["local/prometheus.yml:/etc/prometheus/prometheus.yml"]
        ports = ["prometheus"]
      }
    }
  }
}
```

### Logging Pipeline
```hcl
job "logging" {
  type = "system"
  
  group "fluentbit" {
    task "fluentbit" {
      driver = "docker"
      
      config {
        image = "fluent/fluent-bit:latest"
        network_mode = "host"
        
        volumes = [
          "/var/log:/var/log:ro",
          "/opt/nomad/alloc:/var/nomad/alloc:ro"
        ]
      }
      
      template {
        data = <<EOH
[SERVICE]
    Flush        5
    Daemon       off
    Log_Level    info

[INPUT]
    Name              tail
    Path              /var/nomad/alloc/*/alloc/logs/*.stdout.*
    Tag               nomad.stdout.*
    Parser            docker
    Skip_Long_Lines   On
    Refresh_Interval  10

[OUTPUT]
    Name   elasticsearch
    Match  *
    Host   elasticsearch.service.consul
    Port   9200
    Index  nomad-logs
EOH
        destination = "local/fluent-bit.conf"
      }
    }
  }
}
```

## Production Considerations

### High Availability Setup
```hcl
# Server configuration for HA
server {
  enabled = true
  bootstrap_expect = 5  # Use 5 servers for production
  
  # Autopilot configuration
  autopilot {
    cleanup_dead_servers      = true
    last_contact_threshold    = "200ms"
    max_trailing_logs         = 250
    min_quorum                = 3
    server_stabilization_time = "10s"
  }
  
  # Raft configuration
  raft_multiplier = 1  # Performance tuning
  
  # Snapshot configuration
  snapshot_agent {
    interval = "1h"
    retain   = 168  # Keep 1 week of hourly snapshots
    
    storage "s3" {
      bucket = "nomad-snapshots"
      region = "us-west-2"
    }
  }
}
```

### Security Configuration
```hcl
# ACL configuration
acl {
  enabled = true
  token_ttl = "30m"
  policy_ttl = "60m"
  token_replication = true
}

# TLS configuration
tls {
  http = true
  rpc  = true
  
  ca_file   = "/etc/nomad/ca.crt"
  cert_file = "/etc/nomad/server.crt"
  key_file  = "/etc/nomad/server.key"
  
  verify_server_hostname = true
  verify_https_client    = true
  
  # mTLS for clients
  rpc_upgrade_mode = true
}

# Sentinel policies (Enterprise)
sentinel {
  import "sentinel-policies" {
    path = "/etc/nomad/sentinel/"
  }
}
```

### Resource Management
```hcl
# Namespace with quotas
resource "nomad_namespace" "prod" {
  name = "production"
  
  quota {
    limit {
      region = "global"
      
      region_limit {
        cpu = 10000
        memory = 10000
        memory_max = 12000
      }
    }
  }
}

# Node pool configuration
node_pool "gpu" {
  description = "GPU compute nodes"
  
  # Scheduler configuration
  scheduler_config {
    scheduler_algorithm = "spread"
    
    # Preemption
    preemption_config {
      system_scheduler_enabled   = true
      service_scheduler_enabled  = false
      batch_scheduler_enabled    = false
    }
  }
}
```

### Disaster Recovery
```bash
#!/bin/bash
# Backup script

# Create snapshot
nomad operator snapshot save backup-$(date +%Y%m%d-%H%M%S).snap

# Backup ACL tokens
nomad acl token list -json > acl-tokens-backup.json

# Backup job specifications
for job in $(nomad job list -json | jq -r '.[].ID'); do
  nomad job inspect $job > jobs/$job.json
done

# Sync to offsite
aws s3 sync ./backups s3://nomad-dr/backups/
```

### Performance Tuning
```hcl
# Client performance settings
client {
  # Fingerprinting
  fingerprint {
    whitelist = ["cpu", "memory", "disk", "network"]
    blacklist = ["env_aws", "env_gce"]
  }
  
  # GC tuning
  gc_interval = "1m"
  gc_parallel_destroys = 2
  gc_disk_usage_threshold = 80
  gc_inode_usage_threshold = 70
  gc_max_allocs = 100
  
  # Reserved resources
  reserved {
    cpu    = 500
    memory = 512
    disk   = 1024
  }
}

# Server performance
server {
  # Evaluation settings
  num_schedulers = 8
  
  # Job GC
  job_gc_interval = "5m"
  job_gc_threshold = "4h"
  
  # Deployment GC
  deployment_gc_threshold = "1h"
}
```

## Use Cases

### Batch Processing
```hcl
job "etl-pipeline" {
  type = "batch"
  
  periodic {
    cron = "0 2 * * *"
    prohibit_overlap = true
    time_zone = "UTC"
  }
  
  parameterized {
    payload = "optional"
    meta_required = ["source", "destination"]
  }
  
  group "extract" {
    task "extract" {
      driver = "docker"
      
      config {
        image = "etl:extract"
      }
      
      env {
        SOURCE = "${NOMAD_META_source}"
        DEST   = "${NOMAD_META_destination}"
      }
      
      dispatch_payload {
        file = "config.json"
      }
    }
  }
}
```

### Edge Computing
```hcl
job "edge-processor" {
  datacenters = ["edge-*"]
  type = "service"
  
  constraint {
    attribute = "${attr.platform.aws.placement.availability-zone}"
    operator  = "regexp"
    value     = ".*-local-.*"
  }
  
  group "processor" {
    count = 1
    
    restart {
      attempts = 10
      interval = "5m"
      delay    = "25s"
      mode     = "delay"
    }
    
    task "ml-inference" {
      driver = "docker"
      
      config {
        image = "edge-ai:latest"
        devices = [
          {
            host_path = "/dev/video0"
            container_path = "/dev/video0"
          }
        ]
      }
      
      resources {
        cpu    = 1000
        memory = 1024
        
        device "intel/gpu" {
          count = 1
        }
      }
    }
  }
}
```

### Multi-Cloud Deployment
```hcl
job "global-app" {
  multiregion {
    strategy {
      max_parallel = 1
      on_failure   = "fail_all"
    }
    
    region "aws-us-west" {
      count = 5
      datacenters = ["us-west-2a", "us-west-2b"]
      
      meta {
        cloud_provider = "aws"
      }
    }
    
    region "gcp-us-central" {
      count = 3
      datacenters = ["us-central1-a", "us-central1-b"]
      
      meta {
        cloud_provider = "gcp"
      }
    }
    
    region "azure-east" {
      count = 3
      datacenters = ["eastus", "eastus2"]
      
      meta {
        cloud_provider = "azure"
      }
    }
  }
}
```

## Best Practices

1. **Job Design**
   - Use parameterized jobs for flexibility
   - Implement proper health checks
   - Define resource limits accurately
   - Use job priorities appropriately

2. **Security**
   - Enable ACLs in production
   - Use Vault for secrets management
   - Implement mTLS between components
   - Regular security audits

3. **Operations**
   - Monitor cluster health metrics
   - Implement automated backups
   - Plan for capacity management
   - Document runbooks

4. **Performance**
   - Tune garbage collection settings
   - Optimize job placement strategies
   - Monitor resource utilization
   - Use job batching where appropriate