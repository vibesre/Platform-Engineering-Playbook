# Service Discovery

## Overview

Service discovery enables automatic detection of services and their network locations in distributed systems, essential for microservices architectures and dynamic infrastructure.

## Core Technologies

### Consul

HashiCorp's service mesh solution with built-in service discovery, health checking, and key-value storage.

#### Key Features
- Multi-datacenter support
- Service mesh with Connect
- Health checking
- Key-value storage
- DNS and HTTP APIs
- ACL system

#### Configuration Example

**Consul Server Configuration (`/etc/consul.d/server.json`)**:
```json
{
  "datacenter": "dc1",
  "data_dir": "/opt/consul",
  "log_level": "INFO",
  "node_name": "consul-server-1",
  "server": true,
  "bootstrap_expect": 3,
  "encrypt": "Luj2FZXHnPUHRyHjPwBRTw==",
  "ca_file": "/etc/consul.d/consul-agent-ca.pem",
  "cert_file": "/etc/consul.d/dc1-server-consul-0.pem",
  "key_file": "/etc/consul.d/dc1-server-consul-0-key.pem",
  "verify_incoming": true,
  "verify_outgoing": true,
  "verify_server_hostname": true,
  "retry_join": ["consul-server-1", "consul-server-2", "consul-server-3"],
  "ui_config": {
    "enabled": true
  },
  "connect": {
    "enabled": true
  },
  "ports": {
    "grpc": 8502
  },
  "acl": {
    "enabled": true,
    "default_policy": "allow",
    "enable_token_persistence": true
  },
  "performance": {
    "raft_multiplier": 1
  }
}
```

**Service Registration**:
```json
{
  "service": {
    "name": "web-api",
    "tags": ["primary", "v1"],
    "port": 8080,
    "meta": {
      "version": "1.2.3",
      "protocol": "http"
    },
    "check": {
      "http": "http://localhost:8080/health",
      "interval": "10s",
      "timeout": "5s"
    },
    "weights": {
      "passing": 10,
      "warning": 1
    },
    "enable_tag_override": false,
    "connect": {
      "sidecar_service": {
        "port": 20000,
        "proxy": {
          "upstreams": [
            {
              "destination_name": "database",
              "local_bind_port": 5432
            }
          ]
        }
      }
    }
  }
}
```

**Consul Template Example**:
```hcl
# nginx.conf.ctmpl
upstream backend {
  {{range service "web-api"}}
  server {{.Address}}:{{.Port}} weight={{with .ServiceMeta.weight}}{{.}}{{else}}1{{end}};
  {{else}}
  server 127.0.0.1:65535; # force a 502
  {{end}}
}

server {
  listen 80;
  server_name api.example.com;

  location / {
    proxy_pass http://backend;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $http_host;
  }

  location /health {
    access_log off;
    return 200 "healthy\n";
  }
}
```

**Consul Connect Service Mesh**:
```hcl
# service-intentions.hcl
Kind = "service-intentions"
Name = "web-api"
Sources = [
  {
    Name = "frontend"
    Action = "allow"
  },
  {
    Name = "*"
    Action = "deny"
  }
]

# proxy-defaults.hcl
Kind = "proxy-defaults"
Name = "global"
Config {
  protocol = "http"
  envoy_tracing_json = <<EOF
  {
    "http": {
      "name": "envoy.tracers.zipkin",
      "typedConfig": {
        "@type": "type.googleapis.com/envoy.config.trace.v3.ZipkinConfig",
        "collector_cluster": "zipkin",
        "collector_endpoint_version": "HTTP_JSON",
        "collector_endpoint": "/api/v2/spans"
      }
    }
  }
  EOF
}
```

### CoreDNS

Flexible, extensible DNS server with plugin architecture, commonly used in Kubernetes.

#### Key Features
- Plugin-based architecture
- Service discovery integration
- Metrics and observability
- Zone transfer support
- DNS-over-TLS/HTTPS
- Caching and forwarding

#### Configuration Example

**CoreDNS Corefile**:
```corefile
. {
    # Enable error logging
    errors
    
    # Health check endpoint
    health {
        lameduck 5s
    }
    
    # Prometheus metrics
    prometheus :9153
    
    # DNS-over-HTTPS
    https://.:443 {
        tls /etc/coredns/cert.pem /etc/coredns/key.pem
    }
    
    # Service discovery for Kubernetes
    kubernetes cluster.local in-addr.arpa ip6.arpa {
        endpoint https://kubernetes.default.svc
        pods insecure
        fallthrough in-addr.arpa ip6.arpa
        ttl 30
    }
    
    # Consul service discovery
    consul {
        endpoint consul.service.consul:8600
        scheme https
        token "consul-dns-token"
    }
    
    # Cache responses
    cache {
        success 9984 30
        denial 9984 5
        prefetch 10 1m 10%
    }
    
    # Forward to upstream DNS
    forward . /etc/resolv.conf {
        max_concurrent 1000
        policy random
        health_check 5s
    }
    
    # Load balancing
    loadbalance round_robin
    
    # Query logging
    log . {
        class all
    }
    
    # DNSSEC validation
    dnssec {
        trust_anchors /etc/coredns/trust-anchors
    }
    
    # Rate limiting
    ratelimit {
        zones-per-second 30
        responses-per-second 20
    }
}

# Custom zone for internal services
internal.company.com {
    file /etc/coredns/zones/internal.company.com.zone
    
    # Zone transfer
    transfer {
        to * {
            key "transfer-key"
        }
    }
}

# Split-horizon DNS
external.company.com {
    file /etc/coredns/zones/external.company.com.zone {
        upstream
    }
}

# Federation with other clusters
federation cluster.local {
    prod prod.federation.io
    staging staging.federation.io
}
```

**Custom Plugin Example**:
```go
// custom_plugin.go
package custom

import (
    "context"
    "github.com/coredns/coredns/plugin"
    "github.com/miekg/dns"
)

type Custom struct {
    Next plugin.Handler
}

func (c Custom) ServeDNS(ctx context.Context, w dns.ResponseWriter, r *dns.Msg) (int, error) {
    // Custom logic for service discovery
    if r.Question[0].Name == "_services._tcp.example.com." {
        m := new(dns.Msg)
        m.SetReply(r)
        
        // Add SRV records
        rr := &dns.SRV{
            Hdr: dns.RR_Header{
                Name:   r.Question[0].Name,
                Rrtype: dns.TypeSRV,
                Class:  dns.ClassINET,
                Ttl:    300,
            },
            Priority: 10,
            Weight:   5,
            Port:     8080,
            Target:   "service-1.example.com.",
        }
        m.Answer = append(m.Answer, rr)
        
        w.WriteMsg(m)
        return dns.RcodeSuccess, nil
    }
    
    return plugin.NextOrFailure(c.Name(), c.Next, ctx, w, r)
}

func (c Custom) Name() string {
    return "custom"
}
```

### etcd

Distributed reliable key-value store for configuration and service discovery.

#### Key Features
- Distributed consensus (Raft)
- Watch mechanism
- Transactions
- Leases and TTLs
- Multi-version concurrency control
- gRPC API

#### Configuration Example

**etcd Configuration (`/etc/etcd/etcd.conf.yml`)**:
```yaml
name: 'etcd-node-1'
data-dir: '/var/lib/etcd'

# Cluster configuration
initial-advertise-peer-urls: 'https://10.0.1.10:2380'
listen-peer-urls: 'https://10.0.1.10:2380'
listen-client-urls: 'https://10.0.1.10:2379,https://127.0.0.1:2379'
advertise-client-urls: 'https://10.0.1.10:2379'
initial-cluster-token: 'etcd-cluster-prod'
initial-cluster: 'etcd-node-1=https://10.0.1.10:2380,etcd-node-2=https://10.0.1.11:2380,etcd-node-3=https://10.0.1.12:2380'
initial-cluster-state: 'new'

# Security
client-transport-security:
  cert-file: '/etc/etcd/certs/server.crt'
  key-file: '/etc/etcd/certs/server.key'
  client-cert-auth: true
  trusted-ca-file: '/etc/etcd/certs/ca.crt'

peer-transport-security:
  cert-file: '/etc/etcd/certs/peer.crt'
  key-file: '/etc/etcd/certs/peer.key'
  client-cert-auth: true
  trusted-ca-file: '/etc/etcd/certs/ca.crt'

# Performance tuning
quota-backend-bytes: 8589934592
max-txn-ops: 128
max-request-bytes: 1572864

# Compaction
auto-compaction-mode: periodic
auto-compaction-retention: "24h"

# Monitoring
metrics: extensive
```

**Service Registration with etcd**:
```python
import etcd3
import json
import socket
import time
from threading import Thread

class ServiceRegistry:
    def __init__(self, etcd_host='localhost', etcd_port=2379):
        self.etcd = etcd3.client(host=etcd_host, port=etcd_port)
        self.lease = None
        self.service_key = None
        
    def register_service(self, service_name, service_id, host, port, 
                        metadata=None, ttl=30):
        """Register a service with etcd"""
        # Create lease for automatic expiration
        self.lease = self.etcd.lease(ttl)
        
        # Service information
        service_info = {
            'id': service_id,
            'name': service_name,
            'host': host,
            'port': port,
            'timestamp': int(time.time()),
            'metadata': metadata or {}
        }
        
        # Register with lease
        self.service_key = f'/services/{service_name}/{service_id}'
        self.etcd.put(
            self.service_key,
            json.dumps(service_info),
            lease=self.lease
        )
        
        # Start keepalive thread
        self._start_keepalive()
        
    def _start_keepalive(self):
        """Keep the lease alive"""
        def keepalive():
            while self.lease:
                try:
                    self.etcd.refresh_lease(self.lease)
                    time.sleep(10)
                except Exception as e:
                    print(f"Keepalive error: {e}")
                    break
                    
        Thread(target=keepalive, daemon=True).start()
        
    def discover_services(self, service_name):
        """Discover all instances of a service"""
        services = []
        prefix = f'/services/{service_name}/'
        
        for value, metadata in self.etcd.get_prefix(prefix):
            if value:
                service_info = json.loads(value)
                services.append(service_info)
                
        return services
        
    def watch_services(self, service_name, callback):
        """Watch for service changes"""
        prefix = f'/services/{service_name}/'
        
        events_iterator, cancel = self.etcd.watch_prefix(prefix)
        
        for event in events_iterator:
            if isinstance(event, etcd3.events.PutEvent):
                service_info = json.loads(event.value)
                callback('add', service_info)
            elif isinstance(event, etcd3.events.DeleteEvent):
                callback('remove', event.key.decode())
                
    def health_check(self, service_key, health_endpoint):
        """Update service health status"""
        while True:
            try:
                # Check health endpoint
                response = requests.get(health_endpoint, timeout=5)
                health_status = 'healthy' if response.status_code == 200 else 'unhealthy'
                
                # Update health status in etcd
                self.etcd.put(
                    f'{service_key}/health',
                    health_status,
                    lease=self.lease
                )
                
                time.sleep(10)
            except Exception as e:
                self.etcd.put(
                    f'{service_key}/health',
                    'unhealthy',
                    lease=self.lease
                )
                time.sleep(10)

# Usage example
if __name__ == '__main__':
    registry = ServiceRegistry()
    
    # Register service
    registry.register_service(
        service_name='api-service',
        service_id=f'api-{socket.gethostname()}',
        host=socket.gethostname(),
        port=8080,
        metadata={
            'version': '1.2.3',
            'region': 'us-east-1',
            'tags': ['http', 'rest']
        }
    )
    
    # Discover services
    services = registry.discover_services('api-service')
    print(f"Found {len(services)} api-service instances")
    
    # Watch for changes
    def on_service_change(event_type, service_info):
        print(f"Service {event_type}: {service_info}")
        
    registry.watch_services('api-service', on_service_change)
```

## Best Practices

### High Availability

1. **Consul HA Setup**
   ```hcl
   # Consul server configuration for HA
   datacenter = "dc1"
   data_dir = "/opt/consul"
   log_level = "INFO"
   server = true
   bootstrap_expect = 3
   
   # Raft performance tuning
   performance {
     raft_multiplier = 1
     leave_drain_time = "5s"
     rpc_hold_timeout = "7s"
   }
   
   # Autopilot for automatic cluster management
   autopilot {
     cleanup_dead_servers = true
     last_contact_threshold = "200ms"
     max_trailing_logs = 250
     min_quorum = 3
     server_stabilization_time = "10s"
   }
   
   # Enable redundancy zones
   node_meta {
     zone = "zone-a"
   }
   ```

2. **etcd Cluster Best Practices**
   ```yaml
   # Recommended cluster size: 3, 5, or 7 nodes
   cluster_size: 5
   
   # Disk requirements
   disk:
     type: SSD
     iops: 8000
     throughput: "100MB/s"
   
   # Network tuning
   heartbeat-interval: 100
   election-timeout: 1000
   
   # Snapshot policy
   snapshot-count: 10000
   ```

### Security Configuration

1. **mTLS Configuration**
   ```yaml
   # Consul TLS configuration
   verify_incoming: true
   verify_outgoing: true
   verify_server_hostname: true
   
   ca_file: "/etc/consul.d/consul-agent-ca.pem"
   cert_file: "/etc/consul.d/dc1-server-consul-0.pem"
   key_file: "/etc/consul.d/dc1-server-consul-0-key.pem"
   
   # Auto-encrypt for clients
   auto_encrypt:
     allow_tls: true
   ```

2. **ACL Policies**
   ```hcl
   # Consul ACL policy
   node_prefix "" {
     policy = "read"
   }
   
   service_prefix "" {
     policy = "read"
   }
   
   service "web-api" {
     policy = "write"
   }
   
   key_prefix "config/" {
     policy = "read"
   }
   ```

### Performance Optimization

1. **DNS Caching Strategy**
   ```yaml
   coredns:
     cache:
       size: 10000
       positive_ttl: 300
       negative_ttl: 30
       prefetch:
         percentage: 20
         duration: 1m
   ```

2. **Connection Pooling**
   ```go
   // etcd client with connection pooling
   import (
       "go.etcd.io/etcd/client/v3"
       "google.golang.org/grpc"
   )
   
   func NewETCDClient() (*clientv3.Client, error) {
       return clientv3.New(clientv3.Config{
           Endpoints:   []string{"localhost:2379"},
           DialTimeout: 5 * time.Second,
           DialOptions: []grpc.DialOption{
               grpc.WithInitialWindowSize(1 << 30),
               grpc.WithInitialConnWindowSize(1 << 30),
               grpc.WithKeepaliveParams(keepalive.ClientParameters{
                   Time:                10 * time.Second,
                   Timeout:             3 * time.Second,
                   PermitWithoutStream: true,
               }),
           },
       })
   }
   ```

## Common Patterns

### Health Checking

```go
// Comprehensive health checking implementation
package health

import (
    "context"
    "fmt"
    "net/http"
    "time"
)

type HealthChecker struct {
    checks []Check
}

type Check struct {
    Name     string
    Type     string
    Interval time.Duration
    Timeout  time.Duration
    Checker  func() error
}

func (h *HealthChecker) RunChecks(ctx context.Context) {
    for _, check := range h.checks {
        go h.runCheck(ctx, check)
    }
}

func (h *HealthChecker) runCheck(ctx context.Context, check Check) {
    ticker := time.NewTicker(check.Interval)
    defer ticker.Stop()
    
    for {
        select {
        case <-ctx.Done():
            return
        case <-ticker.C:
            ctx, cancel := context.WithTimeout(ctx, check.Timeout)
            err := check.Checker()
            cancel()
            
            h.updateStatus(check.Name, err)
        }
    }
}

// Example checks
var defaultChecks = []Check{
    {
        Name:     "http-endpoint",
        Type:     "http",
        Interval: 10 * time.Second,
        Timeout:  5 * time.Second,
        Checker: func() error {
            resp, err := http.Get("http://localhost:8080/health")
            if err != nil {
                return err
            }
            defer resp.Body.Close()
            
            if resp.StatusCode != http.StatusOK {
                return fmt.Errorf("unhealthy: %d", resp.StatusCode)
            }
            return nil
        },
    },
    {
        Name:     "database",
        Type:     "tcp",
        Interval: 15 * time.Second,
        Timeout:  3 * time.Second,
        Checker: func() error {
            // Database health check logic
            return nil
        },
    },
}
```

### Service Mesh Integration

```yaml
# Consul Connect service mesh configuration
Kind: "service-defaults"
Name: "web"
Protocol: "http"
MeshGateway:
  Mode: "local"
ExternalSNI: "web.example.com"

---
Kind: "service-resolver"
Name: "web"
DefaultSubset: "v1"
Subsets:
  v1:
    Filter: "Service.Meta.version == v1"
  v2:
    Filter: "Service.Meta.version == v2"
    
---
Kind: "service-router"
Name: "web"
Routes:
  - Match:
      HTTP:
        PathPrefix: "/api/v2"
    Destination:
      Service: "web"
      Subset: "v2"
  - Match:
      HTTP:
        Header:
          - Name: "x-version"
            Exact: "v2"
    Destination:
      Service: "web"
      Subset: "v2"
```

### Load Balancing Strategies

```python
# Client-side load balancing with service discovery
import random
import time
from collections import defaultdict

class ServiceBalancer:
    def __init__(self, discovery_client):
        self.discovery = discovery_client
        self.instances = defaultdict(list)
        self.last_update = defaultdict(float)
        self.update_interval = 30  # seconds
        
    def get_instance(self, service_name, strategy='round-robin'):
        """Get a service instance using specified strategy"""
        self._refresh_instances(service_name)
        
        instances = self.instances[service_name]
        if not instances:
            raise Exception(f"No healthy instances for {service_name}")
            
        if strategy == 'round-robin':
            return self._round_robin(service_name)
        elif strategy == 'random':
            return random.choice(instances)
        elif strategy == 'least-connections':
            return self._least_connections(instances)
        elif strategy == 'weighted':
            return self._weighted_random(instances)
            
    def _refresh_instances(self, service_name):
        """Refresh service instances if needed"""
        if time.time() - self.last_update[service_name] > self.update_interval:
            instances = self.discovery.get_healthy_instances(service_name)
            self.instances[service_name] = instances
            self.last_update[service_name] = time.time()
            
    def _round_robin(self, service_name):
        """Round-robin selection"""
        if not hasattr(self, '_rr_counters'):
            self._rr_counters = defaultdict(int)
            
        instances = self.instances[service_name]
        index = self._rr_counters[service_name] % len(instances)
        self._rr_counters[service_name] += 1
        
        return instances[index]
        
    def _weighted_random(self, instances):
        """Weighted random selection based on instance weight"""
        weights = [inst.get('weight', 1) for inst in instances]
        return random.choices(instances, weights=weights)[0]
```

## Monitoring and Troubleshooting

### Metrics Collection

```yaml
# Prometheus configuration for service discovery monitoring
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'consul'
    consul_sd_configs:
      - server: 'consul.service.consul:8500'
        services: ['consul']
    relabel_configs:
      - source_labels: [__meta_consul_service]
        target_label: service
        
  - job_name: 'etcd'
    static_configs:
      - targets: ['etcd-1:2379', 'etcd-2:2379', 'etcd-3:2379']
        
  - job_name: 'coredns'
    static_configs:
      - targets: ['coredns:9153']
```

### Debug Tools

```bash
#!/bin/bash
# Service discovery debugging script

# Consul debugging
consul_debug() {
    echo "=== Consul Cluster Status ==="
    consul members
    consul operator raft list-peers
    
    echo -e "\n=== Consul Services ==="
    consul catalog services
    
    echo -e "\n=== Service Instances ==="
    for service in $(consul catalog services | grep -v consul); do
        echo "Service: $service"
        consul catalog nodes -service=$service
    done
}

# etcd debugging
etcd_debug() {
    echo "=== etcd Cluster Status ==="
    etcdctl endpoint status --endpoints=$ENDPOINTS --write-out=table
    
    echo -e "\n=== etcd Members ==="
    etcdctl member list --endpoints=$ENDPOINTS --write-out=table
    
    echo -e "\n=== Service Keys ==="
    etcdctl get /services/ --prefix --endpoints=$ENDPOINTS
}

# CoreDNS debugging
coredns_debug() {
    echo "=== CoreDNS Health ==="
    curl -s http://localhost:8080/health
    
    echo -e "\n=== CoreDNS Metrics ==="
    curl -s http://localhost:9153/metrics | grep -E "coredns_(dns_request|cache|forward)"
    
    echo -e "\n=== DNS Resolution Test ==="
    dig @localhost service.consul +short
}
```

## Integration Examples

### Kubernetes Service Discovery

```yaml
# CoreDNS configuration for Kubernetes
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
            lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods insecure
            fallthrough in-addr.arpa ip6.arpa
            ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
    
    consul.local:53 {
        errors
        cache 30
        forward . 10.0.0.10:8600
    }
```

### Docker Swarm Integration

```yaml
version: '3.8'

services:
  consul:
    image: consul:1.12
    command: agent -server -bootstrap-expect=3 -ui
    networks:
      - consul
    deploy:
      mode: global
      placement:
        constraints:
          - node.role == manager
          
  registrator:
    image: gliderlabs/registrator:latest
    command: -internal consul://consul:8500
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock
    deploy:
      mode: global
      
  web-app:
    image: nginx:alpine
    networks:
      - consul
    deploy:
      replicas: 3
      labels:
        - "SERVICE_NAME=web"
        - "SERVICE_TAGS=http,frontend"
        - "SERVICE_CHECK_HTTP=/health"
        - "SERVICE_CHECK_INTERVAL=10s"
```

### Service Discovery Client Libraries

```go
// Go client for service discovery
package discovery

import (
    "fmt"
    "github.com/hashicorp/consul/api"
    "math/rand"
    "sync"
    "time"
)

type ServiceDiscovery struct {
    consul    *api.Client
    cache     map[string][]*api.ServiceEntry
    cacheLock sync.RWMutex
    ttl       time.Duration
}

func NewServiceDiscovery(consulAddr string) (*ServiceDiscovery, error) {
    config := api.DefaultConfig()
    config.Address = consulAddr
    
    client, err := api.NewClient(config)
    if err != nil {
        return nil, err
    }
    
    sd := &ServiceDiscovery{
        consul: client,
        cache:  make(map[string][]*api.ServiceEntry),
        ttl:    30 * time.Second,
    }
    
    // Start cache refresh
    go sd.refreshCache()
    
    return sd, nil
}

func (sd *ServiceDiscovery) GetService(name string) (*api.ServiceEntry, error) {
    sd.cacheLock.RLock()
    services, exists := sd.cache[name]
    sd.cacheLock.RUnlock()
    
    if !exists || len(services) == 0 {
        // Cache miss, fetch directly
        services, _, err := sd.consul.Health().Service(name, "", true, nil)
        if err != nil {
            return nil, err
        }
        
        if len(services) == 0 {
            return nil, fmt.Errorf("no healthy instances of %s", name)
        }
        
        // Update cache
        sd.cacheLock.Lock()
        sd.cache[name] = services
        sd.cacheLock.Unlock()
    }
    
    // Random selection
    return services[rand.Intn(len(services))], nil
}

func (sd *ServiceDiscovery) refreshCache() {
    ticker := time.NewTicker(sd.ttl)
    defer ticker.Stop()
    
    for range ticker.C {
        services, _, err := sd.consul.Catalog().Services(nil)
        if err != nil {
            continue
        }
        
        for service := range services {
            entries, _, err := sd.consul.Health().Service(service, "", true, nil)
            if err == nil {
                sd.cacheLock.Lock()
                sd.cache[service] = entries
                sd.cacheLock.Unlock()
            }
        }
    }
}
```