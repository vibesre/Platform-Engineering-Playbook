---
title: "NGINX Web Server"
description: "Master NGINX as a web server, reverse proxy, load balancer, and API gateway"
---

# NGINX Web Server

NGINX is a high-performance web server, reverse proxy, load balancer, and API gateway. Known for its efficiency, stability, and rich feature set, NGINX powers many of the world's busiest websites. Platform engineers use NGINX for serving static content, proxying applications, load balancing, and implementing complex routing rules.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **NGINX Crash Course**
- **Channel**: Traversy Media
- **Link**: [YouTube - 1 hour](https://www.youtube.com/watch?v=7VAI73roXaY)
- **Why it's great**: Perfect introduction covering web server and reverse proxy basics

#### **NGINX Tutorial for Beginners**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 45 minutes](https://www.youtube.com/watch?v=7YcW25PHnAA)
- **Why it's great**: Comprehensive overview with practical configuration examples

#### **NGINX Load Balancing Deep Dive**
- **Channel**: Hussein Nasser
- **Link**: [YouTube - 1.5 hours](https://www.youtube.com/watch?v=spbkCihFpQ8)
- **Why it's great**: Advanced load balancing concepts and implementations

### 📖 Essential Documentation

#### **NGINX Official Documentation**
- **Link**: [nginx.org/en/docs/](http://nginx.org/en/docs/)
- **Why it's great**: Comprehensive official reference with all directives and modules

#### **NGINX Beginner's Guide**
- **Link**: [nginx.org/en/docs/beginners_guide.html](http://nginx.org/en/docs/beginners_guide.html)
- **Why it's great**: Perfect starting point with basic configuration examples

#### **NGINX Admin Guide**
- **Link**: [docs.nginx.com/nginx/admin-guide/](https://docs.nginx.com/nginx/admin-guide/)
- **Why it's great**: Production-focused configuration patterns and best practices

### 📝 Must-Read Blogs & Articles

#### **NGINX Blog**
- **Source**: NGINX Inc.
- **Link**: [nginx.com/blog/](https://www.nginx.com/blog/)
- **Why it's great**: Official updates, performance tips, and use case studies

#### **NGINX Configuration Best Practices**
- **Source**: DigitalOcean
- **Link**: [digitalocean.com/community/tutorials/nginx-essentials](https://www.digitalocean.com/community/tutorials/nginx-essentials-installation-and-configuration-fundamentals)
- **Why it's great**: Practical security and performance optimization guide

#### **NGINX Performance Tuning**
- **Source**: NGINX
- **Link**: [nginx.com/blog/tuning-nginx/](https://www.nginx.com/blog/tuning-nginx/)
- **Why it's great**: Essential performance optimization techniques

### 🎓 Structured Courses

#### **NGINX Fundamentals**
- **Platform**: Linux Academy
- **Link**: [acloudguru.com/course/nginx-fundamentals](https://acloudguru.com/course/nginx-fundamentals)
- **Cost**: Paid
- **Why it's great**: Hands-on course covering web server to advanced proxy configurations

#### **Mastering NGINX**
- **Platform**: Udemy
- **Link**: [udemy.com/course/nginx-crash-course/](https://www.udemy.com/course/nginx-crash-course/)
- **Cost**: Paid
- **Why it's great**: Complete course from basics to production deployment

### 🛠️ Tools & Platforms

#### **NGINX Config Generator**
- **Link**: [nginxconfig.io](https://nginxconfig.io/)
- **Why it's great**: Interactive tool for generating optimized NGINX configurations

#### **NGINX Unit**
- **Link**: [unit.nginx.org](https://unit.nginx.org/)
- **Why it's great**: Dynamic application server for running multiple application frameworks

#### **NGINX Playground**
- **Link**: [github.com/trimstray/nginx-admins-handbook](https://github.com/trimstray/nginx-admins-handbook)
- **Why it's great**: Comprehensive guide and reference for NGINX administrators

## Introduction

NGINX is a high-performance web server, reverse proxy, load balancer, and API gateway. Known for its efficiency, stability, and rich feature set, NGINX powers many of the world's busiest websites. Platform engineers use NGINX for serving static content, proxying applications, load balancing, and implementing complex routing rules.

## Core Concepts

### NGINX Architecture
```
Master Process (root)
    ├── Worker Process 1 (handles requests)
    ├── Worker Process 2 (handles requests)
    ├── Worker Process N (handles requests)
    └── Cache Manager Process

Event-Driven Model:
- Asynchronous, non-blocking I/O
- Single worker handles thousands of connections
- Efficient memory usage
- High concurrency support
```

### Configuration Structure
```nginx
# Main context
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Events context
events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

# HTTP context
http {
    # Server context
    server {
        # Location context
        location / {
            # Directives
        }
    }
}
```

### Request Processing Order
1. **Server Selection**: Match server_name with Host header
2. **Location Matching**: Find best matching location block
3. **Rewrite Phase**: Process rewrite rules
4. **Access Phase**: Authentication and authorization
5. **Content Phase**: Generate or proxy content
6. **Log Phase**: Write access logs

## Common Use Cases

### 1. Web Server Configuration
```nginx
# Static website serving
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.html index.htm;

    # Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;

    # Cache control for static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|pdf|doc|docx)$ {
        expires 7d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

### 2. Reverse Proxy Configuration
```nginx
# Application reverse proxy
upstream backend {
    server 127.0.0.1:3000 weight=3;
    server 127.0.0.1:3001 weight=2;
    server 127.0.0.1:3002 backup;
    
    # Health checks
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    # SSL configuration
    ssl_certificate /etc/nginx/ssl/cert.crt;
    ssl_certificate_key /etc/nginx/ssl/cert.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        
        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        
        # Connection settings
        proxy_set_header Connection "";
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;
        
        # When backend is down
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
        proxy_next_upstream_tries 3;
    }

    # WebSocket support
    location /ws/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

### 3. Load Balancer Configuration
```nginx
# Advanced load balancing
upstream api_servers {
    # Load balancing methods
    # round-robin (default)
    # least_conn;
    # ip_hash;
    # hash $request_uri consistent;
    
    least_conn;
    
    # Server definitions with options
    server backend1.example.com:8080 max_fails=3 fail_timeout=30s;
    server backend2.example.com:8080 max_fails=3 fail_timeout=30s;
    server backend3.example.com:8080 max_fails=3 fail_timeout=30s weight=2;
    server backend4.example.com:8080 backup;
    
    # Connection pooling
    keepalive 64;
    keepalive_requests 100;
}

# Health check location (NGINX Plus feature, but can be simulated)
server {
    listen 127.0.0.1:8080;
    location /health {
        access_log off;
        return 200 "healthy\n";
    }
}

# Main server block
server {
    listen 80;
    server_name lb.example.com;

    # Custom load balancing based on request
    location /api/v1/ {
        proxy_pass http://api_servers;
        
        # Sticky sessions with cookies
        proxy_cookie_path / "/; HTTPOnly; Secure";
        
        # Circuit breaker pattern
        proxy_next_upstream error timeout http_500 http_502 http_503;
        proxy_next_upstream_tries 2;
        proxy_next_upstream_timeout 10s;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;
    limit_req_status 429;
}
```

## Getting Started Examples

### Basic Installation and Setup
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install epel-release
sudo yum install nginx

# Start and enable service
sudo systemctl start nginx
sudo systemctl enable nginx

# Test configuration
sudo nginx -t

# Reload configuration
sudo nginx -s reload

# View error logs
sudo tail -f /var/log/nginx/error.log
```

### SSL/TLS Configuration with Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renewal test
sudo certbot renew --dry-run
```

```nginx
# Modern SSL configuration
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com;

    # Certificate files from Certbot
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # Modern SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # SSL session caching
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}
```

### API Gateway Configuration
```nginx
# API Gateway with authentication and rate limiting
map $http_authorization $auth_status {
    default 0;
    "~*Bearer .+" 1;
}

# Rate limiting zones
limit_req_zone $binary_remote_addr zone=general_limit:10m rate=100r/s;
limit_req_zone $http_authorization zone=auth_limit:10m rate=1000r/s;

upstream microservice_a {
    server service-a:8080;
    keepalive 32;
}

upstream microservice_b {
    server service-b:8081;
    keepalive 32;
}

server {
    listen 80;
    server_name api.example.com;

    # API versioning
    location ~ ^/api/v1/service-a/(.*)$ {
        # Authentication check
        if ($auth_status = 0) {
            return 401 '{"error": "Unauthorized"}';
        }
        
        # Rate limiting
        limit_req zone=auth_limit burst=20 nodelay;
        
        # Proxy to microservice
        proxy_pass http://microservice_a/$1$is_args$args;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # CORS headers
        add_header Access-Control-Allow-Origin "$http_origin" always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Authorization, Content-Type" always;
        
        if ($request_method = OPTIONS) {
            return 204;
        }
    }

    location ~ ^/api/v1/service-b/(.*)$ {
        limit_req zone=general_limit burst=10 nodelay;
        proxy_pass http://microservice_b/$1$is_args$args;
        
        # Response transformation
        sub_filter_once off;
        sub_filter 'internal-host' 'api.example.com';
    }

    # API documentation
    location /api/docs {
        root /var/www/api-docs;
        try_files /index.html =404;
    }
}
```

## Best Practices

### 1. Performance Optimization
```nginx
# Worker processes optimization
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 65535;
    use epoll;
    multi_accept on;
}

http {
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    # Keepalive
    keepalive_timeout 65;
    keepalive_requests 100;
    
    # Buffers
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 8k;
    output_buffers 1 32k;
    postpone_output 1460;
    
    # Timeouts
    client_header_timeout 60;
    client_body_timeout 60;
    reset_timedout_connection on;
    send_timeout 60;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/xhtml+xml application/x-font-ttf application/x-font-opentype application/vnd.ms-fontobject image/svg+xml;
    gzip_disable "msie6";
    
    # Open file cache
    open_file_cache max=200000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;
}
```

### 2. Security Hardening
```nginx
# Security headers and configurations
server {
    # Hide NGINX version
    server_tokens off;
    
    # Prevent clickjacking
    add_header X-Frame-Options "SAMEORIGIN" always;
    
    # Prevent content type sniffing
    add_header X-Content-Type-Options "nosniff" always;
    
    # XSS protection
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Content Security Policy
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.example.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://api.example.com" always;
    
    # Referrer Policy
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Permissions Policy
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    
    # Block access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Block access to backup files
    location ~ ~$ {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    location /login {
        limit_req zone=login burst=5;
    }
}
```

### 3. Monitoring and Logging
```nginx
# Enhanced logging format
http {
    log_format main_ext '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for" '
                        '$request_time $upstream_response_time $pipe $upstream_cache_status';

    access_log /var/log/nginx/access.log main_ext;
    error_log /var/log/nginx/error.log warn;

    # Conditional logging
    map $request_uri $loggable {
        default 1;
        ~*\.(ico|css|js|gif|jpg|jpeg|png|svg|woff|ttf|eot)$ 0;
        /health 0;
        /metrics 0;
    }

    access_log /var/log/nginx/access.log main_ext if=$loggable;
}

# Status page for monitoring
server {
    listen 127.0.0.1:8080;
    server_name localhost;

    location /nginx_status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        deny all;
    }

    location /metrics {
        # Prometheus format metrics
        content_by_lua_block {
            local metric_requests = ngx.shared.metrics:get("requests") or 0
            local metric_errors = ngx.shared.metrics:get("errors") or 0
            local metric_bytes = ngx.shared.metrics:get("bytes_sent") or 0
            
            ngx.say("# HELP nginx_requests_total Total number of requests")
            ngx.say("# TYPE nginx_requests_total counter")
            ngx.say("nginx_requests_total ", metric_requests)
            
            ngx.say("# HELP nginx_errors_total Total number of errors")
            ngx.say("# TYPE nginx_errors_total counter")
            ngx.say("nginx_errors_total ", metric_errors)
            
            ngx.say("# HELP nginx_bytes_sent_total Total bytes sent")
            ngx.say("# TYPE nginx_bytes_sent_total counter")
            ngx.say("nginx_bytes_sent_total ", metric_bytes)
        }
    }
}
```

## Commands and Configuration

### Essential NGINX Commands
```bash
# Service management
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl reload nginx  # Graceful reload
sudo systemctl restart nginx

# Configuration testing
nginx -t                    # Test configuration
nginx -T                    # Test and dump configuration

# Signal control
nginx -s stop              # Fast shutdown
nginx -s quit              # Graceful shutdown
nginx -s reload            # Reload configuration
nginx -s reopen            # Reopen log files

# Version and modules
nginx -v                   # Version
nginx -V                   # Version with configure options

# Log rotation
sudo kill -USR1 $(cat /var/run/nginx.pid)

# Debug mode
nginx -g "daemon off;"     # Run in foreground
nginx -g "error_log stderr debug;"  # Debug logging
```

### Configuration Testing and Debugging
```bash
# Validate specific configuration file
nginx -t -c /etc/nginx/nginx.conf

# Test with different prefix path
nginx -t -p /usr/local/nginx/

# Enable debug logging for specific connection
# In nginx.conf:
events {
    debug_connection 192.168.1.1;
    debug_connection 192.168.1.0/24;
}

# Real-time log monitoring
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log | grep -v "200"

# Parse access logs
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -20

# Monitor active connections
watch -n1 'curl -s http://localhost:8080/nginx_status'
```

### Performance Analysis
```bash
# Benchmark with ApacheBench
ab -n 10000 -c 100 -k http://localhost/

# Benchmark with wrk
wrk -t12 -c400 -d30s --latency http://localhost/

# Analyze NGINX performance
# Check worker processes
ps aux | grep nginx

# Check open files limit
cat /proc/$(cat /var/run/nginx.pid)/limits | grep "open files"

# Monitor connections
ss -ant | grep :80 | awk '{print $1}' | sort | uniq -c

# Cache hit ratio (if using proxy_cache)
awk '{if($upstream_cache_status ~ /HIT/) hit++; total++} END {print hit/total*100}' /var/log/nginx/access.log
```

## Interview Tips

### Key Questions to Prepare
1. **NGINX vs Apache**: Architecture differences, when to use each
2. **Load balancing algorithms**: Round-robin, least connections, IP hash
3. **Reverse proxy vs forward proxy**: Differences and use cases
4. **HTTP/2 and HTTP/3**: Support in NGINX, benefits
5. **Caching strategies**: Proxy cache, fastcgi cache, cache invalidation

### Practical Scenarios
- "Configure NGINX for high-traffic website"
- "Implement blue-green deployment with NGINX"
- "Set up SSL/TLS with perfect forward secrecy"
- "Debug 502 Bad Gateway errors"
- "Optimize NGINX for microservices architecture"

### Common Pitfalls
- Not understanding location matching precedence
- Forgetting trailing slashes in proxy_pass
- Incorrect buffer sizes causing errors
- Not implementing proper health checks
- Missing security headers in production

## Resources

### Official Documentation
- [NGINX Documentation](https://nginx.org/en/docs/)
- [NGINX Admin Guide](https://docs.nginx.com/nginx/admin-guide/)
- [NGINX Module Reference](http://nginx.org/en/docs/http/ngx_http_core_module.html)
- [NGINX Best Practices](https://www.nginx.com/blog/avoiding-top-10-nginx-configuration-mistakes/)

### Books and Guides
- "NGINX HTTP Server" by Clement Nedelcu
- "Mastering NGINX" by Dimitri Aivaliotis
- [NGINX Cookbook (O'Reilly)](https://www.nginx.com/resources/library/complete-nginx-cookbook/)
- [High Performance Browser Networking](https://hpbn.co/)

### Tools and Modules
- [OpenResty - NGINX with Lua](https://openresty.org/)
- [ModSecurity for NGINX](https://www.nginx.com/products/nginx-waf/)
- [NGINX Amplify - Monitoring](https://www.nginx.com/products/nginx-amplify/)
- [nginx-prometheus-exporter](https://github.com/nginxinc/nginx-prometheus-exporter)

### Configuration Generators
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [NGINX Config Generator](https://www.digitalocean.com/community/tools/nginx)
- [NGINXConfig.io](https://www.nginxconfig.io/)
- [NGINX Location Match Tester](https://nginx.viraptor.info/)

### Community and Learning
- [NGINX Blog](https://www.nginx.com/blog/)
- [r/nginx Reddit Community](https://www.reddit.com/r/nginx/)
- [NGINX Mailing Lists](https://mailman.nginx.org/mailman/listinfo)
- [Stack Overflow NGINX Tag](https://stackoverflow.com/questions/tagged/nginx)

### Performance and Security
- [NGINX Performance Tuning](https://www.nginx.com/blog/tuning-nginx/)
- [Web Server Security Guide](https://www.acunetix.com/blog/web-security-zone/hardening-nginx/)
- [OWASP NGINX Hardening](https://cheatsheetseries.owasp.org/cheatsheets/Nginx_Configuration_Cheat_Sheet.html)
- [NGINX Rate Limiting](https://www.nginx.com/blog/rate-limiting-nginx/)