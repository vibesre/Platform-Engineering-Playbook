# Falco - Runtime Security for Containers

## Overview

Falco is an open-source, cloud-native runtime security tool that provides real-time threat detection for containers, Kubernetes, and cloud environments. Originally created by Sysdig and now a CNCF incubation project, Falco detects unexpected application behavior and alerts on threats at runtime by leveraging kernel-level instrumentation.

## Core Concepts

### How Falco Works

Falco uses system call monitoring to detect anomalous behavior:
1. **Kernel Module/eBPF**: Captures system calls at the kernel level
2. **Rules Engine**: Evaluates captured events against security rules
3. **Alerting**: Sends notifications when rules are triggered
4. **Outputs**: Forwards alerts to various destinations (logs, webhooks, etc.)

### Architecture Components

- **Falco Driver**: Kernel module or eBPF probe that captures syscalls
- **Falco Engine**: Core rules engine that processes events
- **Falco Rules**: YAML-based detection rules
- **Falco Libraries**: Shared libraries for event processing
- **Falco Outputs**: Alert forwarding mechanisms

## Installation

### Installing on Kubernetes with Helm

```bash
# Add Falco Helm repository
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update

# Install Falco with default configuration
helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace

# Install with custom values
helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace \
  -f values.yaml
```

### Custom values.yaml

```yaml
# values.yaml
driver:
  kind: ebpf  # Use eBPF instead of kernel module
  ebpf:
    hostNetwork: true
    
falco:
  grpc:
    enabled: true
  grpc_output:
    enabled: true
    
  json_output: true
  json_include_output_property: true
  
  webserver:
    enabled: true
    listen_port: 8765
    
  priority: notice  # Minimum rule priority level to load
  
  file_output:
    enabled: true
    keep_alive: false
    filename: /var/log/falco/events.txt
    
  stdout_output:
    enabled: true
    
  syslog_output:
    enabled: false
    
  program_output:
    enabled: false
    
customRules:
  rules-custom.yaml: |-
    - rule: Unauthorized Process in Container
      desc: Detect unauthorized process execution
      condition: >
        container.id != host and
        proc.name in (unauthorized_processes)
      output: >
        Unauthorized process started in container
        (user=%user.name command=%proc.cmdline container_id=%container.id image=%container.image.repository)
      priority: WARNING
      tags: [container, process, security]
      
    - list: unauthorized_processes
      items: [nc, ncat, netcat, socat]

falcoctl:
  artifact:
    install:
      enabled: true
    follow:
      enabled: true
  indexes:
  - name: falcosecurity
    url: https://falcosecurity.github.io/falcoctl/index.yaml
```

### Installing on Linux Host

```bash
# Ubuntu/Debian
curl -s https://falco.org/repo/falcosecurity-3672BA8F.asc | sudo apt-key add -
echo "deb https://download.falco.org/packages/deb stable main" | sudo tee -a /etc/apt/sources.list.d/falcosecurity.list
sudo apt-get update -y
sudo apt-get install -y falco

# CentOS/RHEL/Fedora
sudo rpm --import https://falco.org/repo/falcosecurity-3672BA8F.asc
sudo curl -s -o /etc/yum.repos.d/falcosecurity.repo https://falco.org/repo/falcosecurity-rpm.repo
sudo yum install -y falco

# Start Falco service
sudo systemctl enable falco
sudo systemctl start falco
```

## Falco Rules

### Rule Structure

```yaml
- rule: rule_name
  desc: Description of what the rule detects
  condition: >
    condition expression using Falco syntax
  output: >
    output format string with event details
  priority: EMERGENCY|ALERT|CRITICAL|ERROR|WARNING|NOTICE|INFO|DEBUG
  enabled: true
  tags: [tag1, tag2]
  source: syscall
  append: false
  exceptions:
    - name: exception_name
      fields: [field1, field2]
      values:
        - [value1, value2]
```

### Default Rules Categories

1. **File Integrity Monitoring**
```yaml
- rule: Write below etc
  desc: Detect writes to /etc directory
  condition: >
    evt.dir = < and 
    fd.name startswith /etc and
    (evt.type = open or evt.type = openat) and
    (evt.arg.flags contains O_WRONLY or evt.arg.flags contains O_RDWR) and
    not fd.name in (allowed_etc_files) and
    not proc.name in (package_mgmt_binaries)
  output: >
    File written under /etc directory (user=%user.name command=%proc.cmdline file=%fd.name)
  priority: ERROR
  tags: [filesystem, mitre_persistence]
```

2. **Network Security**
```yaml
- rule: Unexpected outbound connection
  desc: Detect outbound connections from unexpected processes
  condition: >
    evt.type = connect and 
    evt.dir = < and
    (fd.typechar = 4 or fd.typechar = 6) and
    container and
    not proc.name in (allowed_outbound_processes) and
    not fd.sip in (allowed_outbound_ips)
  output: >
    Unexpected outbound connection (command=%proc.cmdline connection=%fd.name container=%container.info)
  priority: NOTICE
  tags: [network, mitre_command_and_control]
```

3. **Container Security**
```yaml
- rule: Terminal shell in container
  desc: Detect when a shell is spawned in a container
  condition: >
    container.id != host and
    proc.name in (shell_binaries) and
    proc.pname exists and
    not proc.pname in (shell_binaries)
  output: >
    Shell spawned in container (user=%user.name container=%container.info shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline)
  priority: WARNING
  tags: [container, shell, mitre_execution]
  
- list: shell_binaries
  items: [bash, sh, csh, ksh, zsh, tcsh, dash]
```

## Custom Rules Development

### Creating Detection Rules

```yaml
# custom-rules.yaml
- macro: container_started
  condition: >
    ((evt.type = container) or
     (evt.type = execve and evt.dir = < and proc.vpid = 1))
     
- macro: sensitive_mount
  condition: >
    (fd.name startswith /host/etc or
     fd.name startswith /host/var or
     fd.name startswith /host/root)
     
- list: crypto_miners
  items: [xmrig, minerd, minergate, ethminer]
  
- list: admin_binaries
  items: [sudo, su, passwd, chpasswd, useradd, userdel, usermod, groupadd]
  
- rule: Crypto Mining Detection
  desc: Detect crypto mining activities
  condition: >
    container and
    (proc.name in (crypto_miners) or
     proc.cmdline contains "stratum+tcp" or
     proc.cmdline contains "monero" or
     proc.cmdline contains "bitcoin")
  output: >
    Crypto mining detected (user=%user.name command=%proc.cmdline container=%container.info)
  priority: CRITICAL
  tags: [cryptomining, resource_hijacking]
  
- rule: Privilege Escalation Attempt
  desc: Detect potential privilege escalation
  condition: >
    container and
    proc.name in (admin_binaries) and
    not user.name = root and
    not proc.pname in (allowed_parents)
  output: >
    Privilege escalation attempt (user=%user.name command=%proc.cmdline container=%container.info)
  priority: CRITICAL
  tags: [privilege_escalation, mitre_privilege_escalation]
  exceptions:
  - name: known_sudo_users
    fields: [user.name, proc.name]
    values:
      - [jenkins, sudo]
      - [gitlab-runner, sudo]
```

### Testing Rules

```bash
# Test rules file for syntax errors
falco --rules-file custom-rules.yaml --list

# Dry run with specific rules
falco --rules-file custom-rules.yaml -L

# Test with sample events
falco --rules-file custom-rules.yaml -e 'open' -p 'fd.name=/etc/passwd'

# Validate rules
falco --validate custom-rules.yaml
```

## Integration Examples

### 1. Falco Sidekick

```yaml
# falco-sidekick-values.yaml
config:
  webhook:
    url: "http://security-webhook.monitoring.svc.cluster.local/falco"
  slack:
    webhookurl: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    channel: "#security-alerts"
    minimumpriority: "warning"
  elasticsearch:
    hostport: "http://elasticsearch:9200"
    index: "falco"
  prometheus:
    enabled: true
  teams:
    webhookurl: "https://outlook.office.com/webhook/YOUR-WEBHOOK"
    minimumpriority: "critical"
    
# Install Falco Sidekick
helm install falco-sidekick falcosecurity/falco-sidekick \
  --namespace falco \
  -f falco-sidekick-values.yaml
```

### 2. Prometheus Integration

```yaml
# ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: falco-metrics
  namespace: falco
  labels:
    app: falco
spec:
  selector:
    matchLabels:
      app: falco
  endpoints:
  - port: http
    interval: 30s
    path: /metrics
```

### 3. Falco Exporter

```yaml
# Deploy Falco exporter for Prometheus metrics
apiVersion: apps/v1
kind: Deployment
metadata:
  name: falco-exporter
  namespace: falco
spec:
  replicas: 1
  selector:
    matchLabels:
      app: falco-exporter
  template:
    metadata:
      labels:
        app: falco-exporter
    spec:
      containers:
      - name: falco-exporter
        image: falcosecurity/falco-exporter:latest
        ports:
        - containerPort: 9376
          name: metrics
        args:
        - --listen-address=:9376
        - --falco-grpc-unix-socket=/var/run/falco/falco.sock
        volumeMounts:
        - name: falco-socket
          mountPath: /var/run/falco
      volumes:
      - name: falco-socket
        hostPath:
          path: /var/run/falco
```

## Production Use Cases

### 1. Compliance Monitoring

```yaml
# PCI DSS Compliance Rules
- rule: Credit Card Data Access
  desc: Detect access to files containing credit card patterns
  condition: >
    (open_read or open_write) and
    (fd.name pmatch "/var/lib/mysql/*" or
     fd.name pmatch "/data/payments/*") and
    not proc.name in (authorized_cc_processors)
  output: >
    Credit card data accessed (user=%user.name command=%proc.cmdline file=%fd.name)
  priority: CRITICAL
  tags: [pci_dss, compliance, sensitive_data]
  
- list: authorized_cc_processors
  items: [payment_service, billing_daemon]
```

### 2. Kubernetes Security

```yaml
# Kubernetes API Server Access
- rule: K8s API Server Access
  desc: Detect unauthorized access to Kubernetes API
  condition: >
    evt.type = connect and evt.dir = < and
    fd.sport in (6443, 8443) and
    not proc.name in (kubectl, kubelet, kube-proxy) and
    not container.image.repository in (allowed_k8s_images)
  output: >
    Unauthorized K8s API access (user=%user.name command=%proc.cmdline connection=%fd.name)
  priority: WARNING
  tags: [kubernetes, api_access]

# Detect Pod Exec
- rule: Pod Exec Activity
  desc: Detect kubectl exec commands
  condition: >
    evt.type = execve and
    evt.dir = < and
    proc.cmdline contains "kubectl exec" and
    not user.name in (allowed_kubectl_users)
  output: >
    kubectl exec detected (user=%user.name command=%proc.cmdline)
  priority: WARNING
  tags: [kubernetes, kubectl, exec]
```

### 3. Container Drift Detection

```yaml
# Detect Package Installation
- rule: Package Management in Container
  desc: Detect package installation in running containers
  condition: >
    container.id != host and
    proc.name in (package_mgmt_binaries) and
    (proc.args contains "install" or
     proc.args contains "update" or
     proc.args contains "upgrade")
  output: >
    Package management in container (user=%user.name command=%proc.cmdline container=%container.info)
  priority: WARNING
  tags: [container, drift, package_management]
  
- list: package_mgmt_binaries
  items: [apt, apt-get, yum, dnf, rpm, dpkg, apk, pip, pip3, npm, gem]
```

### 4. Threat Detection

```yaml
# Reverse Shell Detection
- rule: Reverse Shell
  desc: Detect reverse shell connections
  condition: >
    evt.type = dup and
    evt.dir = > and
    fd.num in (0, 1, 2) and
    fd.type = ipv4 and
    not proc.name in (allowed_network_tools)
  output: >
    Reverse shell detected (user=%user.name command=%proc.cmdline connection=%fd.name)
  priority: CRITICAL
  tags: [reverse_shell, attack, mitre_command_and_control]

# Data Exfiltration
- rule: Large Data Transfer
  desc: Detect large outbound data transfers
  condition: >
    evt.type = write and
    evt.dir = > and
    fd.type = ipv4 and
    evt.res > 1000000 and
    not proc.name in (backup_tools) and
    not fd.sip in (internal_networks)
  output: >
    Large data transfer detected (user=%user.name command=%proc.cmdline size=%evt.res connection=%fd.name)
  priority: WARNING
  tags: [data_exfiltration, network]
```

## Advanced Configuration

### 1. Performance Tuning

```yaml
# /etc/falco/falco.yaml
# Buffer size for events
syscall_event_buffers: 8

# Drop events if buffer is full
syscall_buf_size_preset: 4

# Number of events per second
syscall_event_drops:
  actions:
    - log
    - alert
  rate: 0.03333
  max_burst: 10

# Output rate limiting
output_timeout: 2000
outputs_rate: 0
outputs_max_burst: 1000

# gRPC server configuration
grpc:
  enabled: true
  bind_address: "0.0.0.0:5060"
  threadiness: 8
  
# Metrics endpoint
webserver:
  enabled: true
  listen_port: 8765
  k8s_healthz_endpoint: /healthz
  ssl_enabled: false
```

### 2. Custom Output Channels

```go
// Custom webhook handler
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
)

type FalcoAlert struct {
    Output       string                 `json:"output"`
    Priority     string                 `json:"priority"`
    Rule         string                 `json:"rule"`
    Time         string                 `json:"time"`
    OutputFields map[string]interface{} `json:"output_fields"`
}

func falcoWebhook(w http.ResponseWriter, r *http.Request) {
    var alert FalcoAlert
    err := json.NewDecoder(r.Body).Decode(&alert)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    
    // Process alert based on priority
    switch alert.Priority {
    case "CRITICAL", "ALERT":
        // Send to incident response system
        triggerIncidentResponse(alert)
    case "WARNING":
        // Log to SIEM
        forwardToSIEM(alert)
    default:
        // Standard logging
        log.Printf("Falco Alert: %s", alert.Output)
    }
    
    w.WriteHeader(http.StatusOK)
}
```

### 3. Multi-tenancy Configuration

```yaml
# Namespace-specific rules
- rule: Namespace Isolation Violation
  desc: Detect cross-namespace access violations
  condition: >
    container.id != host and
    (evt.type = open or evt.type = connect) and
    fd.name contains "/var/run/secrets/kubernetes.io" and
    not container.label[namespace] = fd.label[namespace]
  output: >
    Cross-namespace access detected (user=%user.name ns=%container.label[namespace] target=%fd.name)
  priority: CRITICAL
  tags: [namespace_isolation, multi_tenancy]
```

## Monitoring and Operations

### 1. Health Checks

```bash
# Check Falco service status
systemctl status falco

# Check Falco logs
journalctl -u falco -f

# Kubernetes health check
kubectl -n falco get pods
kubectl -n falco logs -l app=falco --tail=50

# Check loaded rules
kubectl -n falco exec -it falco-xxx -- falco --list
```

### 2. Metrics and Dashboards

```yaml
# Grafana Dashboard JSON snippet
{
  "dashboard": {
    "title": "Falco Security Events",
    "panels": [
      {
        "title": "Events by Priority",
        "targets": [
          {
            "expr": "sum by (priority) (rate(falco_events_total[5m]))"
          }
        ]
      },
      {
        "title": "Top Triggered Rules",
        "targets": [
          {
            "expr": "topk(10, sum by (rule) (rate(falco_events_total[5m])))"
          }
        ]
      },
      {
        "title": "Container Security Events",
        "targets": [
          {
            "expr": "sum by (container_name) (rate(falco_events_total{source=\"syscall\"}[5m]))"
          }
        ]
      }
    ]
  }
}
```

### 3. Alert Fatigue Management

```yaml
# Rate limiting for noisy rules
- rule: Common System Activity
  desc: Expected system behavior that might be noisy
  condition: >
    evt.type = stat and
    proc.name in (monitoring_agents)
  output: "System monitoring activity"
  priority: INFO
  enabled: false  # Disable noisy rules
  
# Time-based exceptions
- rule: Backup Window Activity
  desc: Allow backup operations during maintenance window
  condition: >
    evt.time.hour >= 2 and evt.time.hour <= 4 and
    proc.name in (backup_tools)
  output: "Backup activity during maintenance window"
  priority: INFO
  enabled: true
```

## Troubleshooting

### Common Issues

1. **Driver Loading Issues**
```bash
# Check kernel module
lsmod | grep falco

# Check eBPF probe
ls -la /sys/kernel/debug/tracing/events/falco/

# Manually load driver
falco-driver-loader

# Check driver logs
dmesg | grep falco
```

2. **High CPU Usage**
```yaml
# Reduce event processing load
- rule: High Volume Rule
  enabled: false  # Disable high-volume rules
  
# Adjust buffer sizes
syscall_buf_size_preset: 1  # Reduce buffer size
```

3. **Missing Events**
```bash
# Check event drops
cat /proc/driver/falco/stats

# Increase buffer size
sysctl -w fs.pipe-max-size=8388608
```

### Debug Mode

```bash
# Run Falco in debug mode
falco -o log_level=debug -o log_stderr=true

# Test specific rule
falco -r test-rule.yaml -M 45 -o json_output=true

# Print supported fields
falco --list-fields
```

## Security Best Practices

### 1. Rule Management

```yaml
# Use rule versioning
- rule: Critical Security Rule v2.1
  desc: Updated version with bug fixes
  condition: >
    # Rule conditions
  append: false
  replace: "Critical Security Rule v2.0"
```

### 2. Deployment Security

```yaml
# Security context for Falco pods
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: falco
spec:
  template:
    spec:
      serviceAccount: falco
      containers:
      - name: falco
        securityContext:
          privileged: true  # Required for kernel access
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
            add:
            - SYS_ADMIN
            - SYS_RESOURCE
            - SYS_PTRACE
```

### 3. Secrets Management

```yaml
# External secrets for integrations
apiVersion: v1
kind: Secret
metadata:
  name: falco-integration-secrets
  namespace: falco
type: Opaque
stringData:
  slack-webhook: "https://hooks.slack.com/services/XXX"
  splunk-token: "xxx-xxx-xxx"
  
# Reference in Falco configuration
program_output:
  enabled: true
  program: "jq -r '.output' | curl -X POST -H 'Authorization: Bearer ${SPLUNK_TOKEN}' -d @- https://splunk-hec:8088/services/collector/event"
```

## Conclusion

Falco provides powerful runtime security monitoring for containers and cloud-native environments. By implementing proper rules, integrations, and operational practices, organizations can detect and respond to security threats in real-time, maintain compliance, and protect their containerized applications from various attack vectors. Its flexibility and extensibility make it an essential component of a comprehensive container security strategy.