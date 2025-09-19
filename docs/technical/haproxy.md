---
title: "HAProxy"
description: "High-performance TCP/HTTP load balancer and proxy server"
sidebar_label: "HAProxy"
---

# HAProxy

## Introduction

HAProxy (High Availability Proxy) is a free, open-source software that provides high availability load balancing and proxying for TCP and HTTP-based applications. It's known for its reliability, high performance, and extensive feature set, making it a popular choice for handling millions of concurrent connections.

### Key Features
- Layer 4 (TCP) and Layer 7 (HTTP) load balancing
- SSL/TLS termination and offloading
- Health checking and automatic failover
- Connection persistence and session affinity
- Rate limiting and request filtering
- Extensive monitoring and statistics
- Zero-downtime reloads
- Content switching and routing

## Core Concepts

### 1. **Proxies**
- **Frontend**: Defines how requests should be accepted
- **Backend**: Defines servers and load balancing algorithms
- **Listen**: Combines frontend and backend (simplified mode)
- **Defaults**: Global settings inherited by proxies

### 2. **Load Balancing Algorithms**
- **roundrobin**: Distributes requests evenly
- **leastconn**: Routes to server with fewest connections
- **source**: Hashes source IP for persistence
- **uri**: Hashes URI for cache-friendly distribution
- **hdr**: Uses HTTP header for routing decisions

### 3. **Health Checks**
- **TCP checks**: Simple port connectivity
- **HTTP checks**: Response code validation
- **Advanced checks**: Custom health endpoints
- **Agent checks**: External health status

### 4. **ACLs (Access Control Lists)**
- Pattern matching for routing decisions
- Header-based routing
- Path-based routing
- Source IP filtering

## Common Use Cases

### 1. **Web Application Load Balancing**
```
global
    maxconn 4096
    log 127.0.0.1:514 local0
    chroot /var/lib/haproxy
    user haproxy
    group haproxy
    daemon

defaults
    log global
    mode http
    option httplog
    option dontlognull
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend web_frontend
    bind *:80
    bind *:443 ssl crt /etc/haproxy/certs/site.pem
    redirect scheme https if !{ ssl_fc }
    
    # ACL definitions
    acl is_api path_beg /api
    acl is_admin path_beg /admin
    
    # Routing rules
    use_backend api_servers if is_api
    use_backend admin_servers if is_admin
    default_backend web_servers

backend web_servers
    balance roundrobin
    option httpchk HEAD /health HTTP/1.1\r\nHost:localhost
    server web1 10.0.1.10:8080 check
    server web2 10.0.1.11:8080 check
    server web3 10.0.1.12:8080 check

backend api_servers
    balance leastconn
    option httpchk GET /api/health
    http-request set-header X-Forwarded-Port %[dst_port]
    http-request add-header X-Forwarded-Proto https if { ssl_fc }
    server api1 10.0.2.10:8081 check
    server api2 10.0.2.11:8081 check

backend admin_servers
    balance source
    stick-table type ip size 200k expire 30m
    stick on src
    server admin1 10.0.3.10:8082 check
    server admin2 10.0.3.11:8082 check
```

### 2. **Database Connection Pooling**
```
global
    maxconn 4096

defaults
    mode tcp
    timeout connect 5000ms
    timeout client 60000ms
    timeout server 60000ms

listen mysql_cluster
    bind *:3306
    mode tcp
    option tcplog
    option mysql-check user haproxy
    balance leastconn
    server mysql1 10.0.4.10:3306 check
    server mysql2 10.0.4.11:3306 check backup
    server mysql3 10.0.4.12:3306 check backup

listen postgres_cluster
    bind *:5432
    mode tcp
    option pgsql-check user haproxy
    balance roundrobin
    server pg1 10.0.5.10:5432 check
    server pg2 10.0.5.11:5432 check
    server pg3 10.0.5.12:5432 check
```

### 3. **WebSocket Support**
```
frontend websocket_frontend
    bind *:8080
    mode http
    timeout client 3600s
    timeout server 3600s
    
    # WebSocket detection
    acl is_websocket hdr(Upgrade) -i WebSocket
    acl is_websocket hdr_beg(Host) -i ws
    
    use_backend websocket_servers if is_websocket
    default_backend http_servers

backend websocket_servers
    balance source
    timeout tunnel 3600s
    option http-server-close
    option forwardfor
    server ws1 10.0.6.10:8080 check
    server ws2 10.0.6.11:8080 check

backend http_servers
    balance roundrobin
    server web1 10.0.7.10:8080 check
    server web2 10.0.7.11:8080 check
```

### 4. **Rate Limiting**
```
frontend rate_limited_api
    bind *:80
    mode http
    
    # Rate limiting table
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    
    # Deny if over 100 requests per 10 seconds
    http-request deny if { sc_http_req_rate(0) gt 100 }
    
    # Rate limit headers
    http-response set-header X-RateLimit-Limit 100
    http-response set-header X-RateLimit-Remaining %[sc_http_req_rate(0),sub(100)]
    
    default_backend api_servers

backend api_servers
    server api1 10.0.8.10:8080 check
    server api2 10.0.8.11:8080 check
```

## Configuration Examples

### 1. **SSL/TLS Configuration**
```
global
    ssl-default-bind-ciphers ECDHE+AESGCM:ECDHE+AES256:!aNULL:!MD5:!DSS
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets
    tune.ssl.default-dh-param 2048

frontend https_frontend
    bind *:443 ssl crt /etc/haproxy/certs/ alpn h2,http/1.1
    mode http
    option forwardfor
    
    # HSTS header
    http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    
    # SSL redirect
    redirect scheme https code 301 if !{ ssl_fc }
    
    default_backend web_servers
```

### 2. **Logging Configuration**
```
global
    log 127.0.0.1:514 local0
    log 127.0.0.1:514 local1 notice

defaults
    log global
    option httplog
    option dontlognull
    option log-separate-errors
    
    # Custom log format
    log-format "%ci:%cp [%t] %ft %b/%s %Tq/%Tw/%Tc/%Tr/%Ta %ST %B %CC %CS %tsc %ac/%fc/%bc/%sc/%rc %sq/%bq %hr %hs %{+Q}r"

frontend web_frontend
    bind *:80
    capture request header Host len 32
    capture request header User-Agent len 64
    capture response header Content-Type len 32
    default_backend web_servers
```

### 3. **Advanced Health Checks**
```
backend api_servers
    option httpchk
    http-check send meth GET uri /health ver HTTP/1.1 hdr Host api.example.com
    http-check expect status 200
    http-check expect header Content-Type -m sub application/json
    http-check expect string {"status":"healthy"}
    
    server api1 10.0.9.10:8080 check inter 2s fall 3 rise 2
    server api2 10.0.9.11:8080 check inter 2s fall 3 rise 2
```

## Best Practices

### 1. **Performance Optimization**
```bash
# System tuning
echo "net.ipv4.ip_local_port_range = 1024 65535" >> /etc/sysctl.conf
echo "net.ipv4.tcp_tw_reuse = 1" >> /etc/sysctl.conf
echo "net.core.somaxconn = 65535" >> /etc/sysctl.conf
sysctl -p

# HAProxy tuning
global
    maxconn 100000
    nbproc 4
    cpu-map 1 0
    cpu-map 2 1
    cpu-map 3 2
    cpu-map 4 3
    tune.bufsize 32768
    tune.maxrewrite 1024
```

### 2. **Security Hardening**
```
global
    chroot /var/lib/haproxy
    user haproxy
    group haproxy
    daemon
    
defaults
    # Hide HAProxy version
    option dontlognull
    option redispatch
    option contstats
    
frontend secure_frontend
    bind *:443 ssl crt /etc/haproxy/certs/site.pem
    
    # Security headers
    http-response set-header X-Content-Type-Options "nosniff"
    http-response set-header X-Frame-Options "DENY"
    http-response set-header X-XSS-Protection "1; mode=block"
    http-response set-header Referrer-Policy "no-referrer-when-downgrade"
    
    # IP whitelist
    acl allowed_ips src 192.168.1.0/24 10.0.0.0/8
    http-request deny if !allowed_ips
```

### 3. **Zero-Downtime Deployments**
```bash
# Configuration validation
haproxy -c -f /etc/haproxy/haproxy.cfg

# Graceful reload
systemctl reload haproxy

# Using HAProxy socket for runtime changes
echo "disable server backend_name/server_name" | socat stdio /var/run/haproxy/admin.sock
# Deploy new version
echo "enable server backend_name/server_name" | socat stdio /var/run/haproxy/admin.sock
```

## Common Commands

### Basic Operations
```bash
# Start HAProxy
systemctl start haproxy

# Stop HAProxy
systemctl stop haproxy

# Reload configuration (zero-downtime)
systemctl reload haproxy

# Check configuration syntax
haproxy -c -f /etc/haproxy/haproxy.cfg

# Test configuration with verbose output
haproxy -f /etc/haproxy/haproxy.cfg -V

# Run in foreground for debugging
haproxy -f /etc/haproxy/haproxy.cfg -db
```

### Runtime Management
```bash
# Show server states
echo "show servers state" | socat stdio /var/run/haproxy/admin.sock

# Show statistics
echo "show stat" | socat stdio /var/run/haproxy/admin.sock

# Show current sessions
echo "show sess" | socat stdio /var/run/haproxy/admin.sock

# Disable server
echo "disable server backend/server1" | socat stdio /var/run/haproxy/admin.sock

# Enable server
echo "enable server backend/server1" | socat stdio /var/run/haproxy/admin.sock

# Set server weight
echo "set weight backend/server1 50" | socat stdio /var/run/haproxy/admin.sock

# Clear counters
echo "clear counters" | socat stdio /var/run/haproxy/admin.sock
```

### Monitoring
```bash
# View logs
tail -f /var/log/haproxy.log

# Monitor statistics via HTTP
curl http://localhost:8404/stats

# Export metrics for Prometheus
curl http://localhost:8404/metrics

# Check backend health
echo "show backend" | socat stdio /var/run/haproxy/admin.sock

# Show errors
echo "show errors" | socat stdio /var/run/haproxy/admin.sock
```

## Interview Questions

### Basic Level
1. **Q: What is HAProxy and what are its primary use cases?**
   A: HAProxy is a high-performance load balancer and proxy server for TCP and HTTP applications. Primary use cases include web application load balancing, SSL termination, content switching, and providing high availability for services.

2. **Q: Explain the difference between frontend and backend in HAProxy.**
   A: Frontend defines how requests are received (bind address, port, protocol), while backend defines where requests are forwarded (servers, load balancing algorithm, health checks).

3. **Q: What load balancing algorithms does HAProxy support?**
   A: Common algorithms include roundrobin (equal distribution), leastconn (fewest connections), source (IP hash), uri (URI hash), and hdr (header-based).

### Intermediate Level
4. **Q: How do you implement session persistence in HAProxy?**
   A: Use stick tables with various persistence methods: source IP (`stick on src`), cookies (`cookie SERVERID insert`), or application session IDs extracted from headers or URLs.

5. **Q: Explain HAProxy's health checking mechanism.**
   A: HAProxy performs active health checks using TCP connections or HTTP requests. You can configure check intervals, failure thresholds, and custom check endpoints. Failed servers are automatically removed from rotation.

6. **Q: How does HAProxy handle SSL/TLS termination?**
   A: HAProxy can terminate SSL/TLS at the frontend, decrypt traffic, apply rules, then either forward plain HTTP to backends or re-encrypt for end-to-end encryption.

### Advanced Level
7. **Q: How do you achieve zero-downtime deployments with HAProxy?**
   A: Use graceful reloads (`systemctl reload`), runtime API for server management, blue-green deployments with backend switching, or gradually shift traffic using weight adjustments.

8. **Q: Explain HAProxy's connection pooling and multiplexing capabilities.**
   A: HAProxy can reuse backend connections (http-reuse), multiplex HTTP/2 connections, and maintain persistent connections to reduce overhead and improve performance.

9. **Q: How would you implement rate limiting per IP address in HAProxy?**
   A: Use stick-tables to track request rates per source IP, then apply ACLs to deny or throttle requests exceeding thresholds. Can also add rate limit headers for client awareness.

### Scenario-Based
10. **Q: Design a highly available HAProxy setup for a critical web application.**
    A: Implement active-passive HAProxy pair with keepalived/VRRP for failover, shared configuration management, synchronized stick-tables, monitoring with automatic failover triggers, and geographic distribution for disaster recovery.

## Resources

### Official Documentation
- [HAProxy Documentation](https://www.haproxy.org/documentation.html)
- [HAProxy Configuration Manual](http://cbonte.github.io/haproxy-dconv/)
- [HAProxy Blog](https://www.haproxy.com/blog/)
- [HAProxy GitHub Repository](https://github.com/haproxy/haproxy)

### Learning Resources
- [HAProxy Fundamentals](https://www.haproxy.com/documentation/haproxy/fundamentals/)
- [HAProxy Best Practices](https://www.haproxy.com/documentation/haproxy/best-practices/)
- [Load Balancing with HAProxy](https://serversforhackers.com/c/load-balancing-with-haproxy)
- [HAProxy Runtime API Guide](https://www.haproxy.com/blog/dynamic-configuration-haproxy-runtime-api/)

### Tools and Utilities
- [HATop - Real-time HAProxy Statistics](https://github.com/jhunt/hatop)
- [HAProxy Stats Page](http://demo.haproxy.org/)
- [HAProxy Config Generator](https://serversforhackers.com/c/using-haproxys-config-generator)
- [HAProxy Syntax Highlighting](https://github.com/haproxytech/haproxy-syntax-highlighting)

### Community
- [HAProxy Discourse Forum](https://discourse.haproxy.org/)
- [HAProxy Slack Community](https://slack.haproxy.org/)
- [HAProxy on Stack Overflow](https://stackoverflow.com/questions/tagged/haproxy)
- [HAProxy Mailing Lists](https://www.haproxy.org/community.html)

### Books and Courses
- "Load Balancing with HAProxy" by Nick Ramirez
- "HAProxy Starter Guide" by Severalnines
- [HAProxy Deep Dive Course](https://www.udemy.com/course/haproxy-deep-dive/)
- [High Performance Load Balancing](https://www.nginx.com/resources/library/high-performance-load-balancing/)

### Performance and Monitoring
- [HAProxy Prometheus Exporter](https://github.com/prometheus/haproxy_exporter)
- [Monitoring HAProxy with Datadog](https://www.datadoghq.com/blog/monitoring-haproxy-performance-metrics/)
- [HAProxy Performance Tuning Guide](https://www.haproxy.com/blog/haproxy-performance-tuning/)
- [HAProxy Benchmarking Tools](https://github.com/observing/haproxy-benchmark)