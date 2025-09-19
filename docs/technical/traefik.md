---
title: "Traefik"
description: "Modern cloud-native edge router and reverse proxy with automatic service discovery"
sidebar_label: "Traefik"
---

# Traefik

## Introduction

Traefik is a modern HTTP reverse proxy and load balancer designed for deploying microservices with ease. It integrates seamlessly with existing infrastructure components and automatically discovers services, making it particularly well-suited for containerized and cloud-native environments.

### Key Features
- Automatic service discovery
- Native integration with orchestrators (Kubernetes, Docker, Consul)
- Dynamic configuration without restarts
- Built-in Let's Encrypt support
- Metrics and distributed tracing
- WebSocket and HTTP/2 support
- Circuit breakers and retry mechanisms
- Canary deployments and traffic mirroring

## Core Concepts

### 1. **Providers**
- **Docker**: Discovers services from Docker labels
- **Kubernetes**: Ingress and CRD support
- **File**: Static configuration from files
- **Consul/Etcd**: Service discovery integration
- **Marathon/Rancher**: Container orchestrator support

### 2. **Routers**
- Define how requests are matched and forwarded
- Support for HTTP/TCP/UDP routing
- Host, path, headers, and query-based matching
- Priority-based rule evaluation

### 3. **Services**
- Represent backend applications
- Load balancing configuration
- Health check definitions
- Sticky sessions support

### 4. **Middlewares**
- Request/response transformation
- Authentication and authorization
- Rate limiting and circuit breaking
- Headers manipulation

## Common Use Cases

### 1. **Docker Integration**
```yaml
# docker-compose.yml
version: '3.8'

services:
  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.tlschallenge=true"
      - "--certificatesresolvers.myresolver.acme.email=admin@example.com"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
      - "./letsencrypt:/letsencrypt"
    networks:
      - traefik-net

  webapp:
    image: nginx:alpine
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.webapp.rule=Host(`app.example.com`)"
      - "traefik.http.routers.webapp.entrypoints=websecure"
      - "traefik.http.routers.webapp.tls.certresolver=myresolver"
      - "traefik.http.middlewares.webapp-auth.basicauth.users=admin:$$2y$$10$$..."
      - "traefik.http.routers.webapp.middlewares=webapp-auth"
      - "traefik.http.services.webapp.loadbalancer.server.port=80"
    networks:
      - traefik-net

  api:
    image: myapi:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.example.com`) && PathPrefix(`/v1`)"
      - "traefik.http.routers.api.entrypoints=websecure"
      - "traefik.http.routers.api.tls=true"
      - "traefik.http.middlewares.api-ratelimit.ratelimit.average=100"
      - "traefik.http.middlewares.api-ratelimit.ratelimit.burst=50"
      - "traefik.http.routers.api.middlewares=api-ratelimit"
    networks:
      - traefik-net

networks:
  traefik-net:
    external: true
```

### 2. **Kubernetes Ingress**
```yaml
# traefik-deployment.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: traefik-ingress-controller
  namespace: kube-system
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: traefik
  namespace: kube-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: traefik
  template:
    metadata:
      labels:
        app: traefik
    spec:
      serviceAccountName: traefik-ingress-controller
      containers:
      - name: traefik
        image: traefik:v2.10
        args:
        - --api.dashboard=true
        - --accesslog=true
        - --entrypoints.web.address=:80
        - --entrypoints.websecure.address=:443
        - --providers.kubernetesingress
        - --providers.kubernetesingress.ingressendpoint.ip=10.0.0.1
        - --metrics.prometheus=true
        - --metrics.prometheus.entryPoint=metrics
        - --entrypoints.metrics.address=:8082
        ports:
        - name: web
          containerPort: 80
        - name: websecure
          containerPort: 443
        - name: dashboard
          containerPort: 8080
---
# Application Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-ingress
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web,websecure
    traefik.ingress.kubernetes.io/router.middlewares: default-redirect-https@kubernetescrd
    traefik.ingress.kubernetes.io/router.tls: "true"
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: webapp-service
            port:
              number: 80
```

### 3. **Advanced Middleware Configuration**
```yaml
# traefik.yml
api:
  dashboard: true
  debug: true

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
          permanent: true
  websecure:
    address: ":443"

providers:
  file:
    directory: /etc/traefik/dynamic
    watch: true

# dynamic/middlewares.yml
http:
  middlewares:
    security-headers:
      headers:
        frameDeny: true
        sslRedirect: true
        browserXssFilter: true
        contentTypeNosniff: true
        forceSTSHeader: true
        stsIncludeSubdomains: true
        stsPreload: true
        stsSeconds: 31536000
        customFrameOptionsValue: "SAMEORIGIN"
        customRequestHeaders:
          X-Forwarded-Proto: https

    rate-limit:
      rateLimit:
        average: 100
        period: 1m
        burst: 50

    circuit-breaker:
      circuitBreaker:
        expression: NetworkErrorRatio() > 0.5

    retry:
      retry:
        attempts: 4
        initialInterval: 100ms

    compress:
      compress:
        excludedContentTypes:
          - text/event-stream
```

### 4. **Service Mesh Integration**
```yaml
# traefik-mesh.yml
apiVersion: v1
kind: Service
metadata:
  name: traefik-mesh
spec:
  ports:
  - port: 8080
    name: api
  - port: 80
    name: web
  - port: 443
    name: websecure
  selector:
    app: traefik-mesh
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: traefik-mesh
spec:
  selector:
    matchLabels:
      app: traefik-mesh
  template:
    metadata:
      labels:
        app: traefik-mesh
    spec:
      containers:
      - name: traefik
        image: traefik:v2.10
        args:
        - --providers.kubernetesingress
        - --providers.kubernetescrd
        - --entrypoints.web.address=:80
        - --entrypoints.websecure.address=:443
        - --pilot.token=<your-pilot-token>
        - --pilot.dashboard=true
        - --metrics.prometheus=true
        - --tracing.jaeger=true
        - --tracing.jaeger.localAgentHostPort=jaeger-agent:6831
```

## Configuration Examples

### 1. **Let's Encrypt with DNS Challenge**
```yaml
# traefik.yml
certificatesResolvers:
  letsencrypt:
    acme:
      email: admin@example.com
      storage: /data/acme.json
      dnsChallenge:
        provider: cloudflare
        delayBeforeCheck: 0
        resolvers:
          - "1.1.1.1:53"
          - "8.8.8.8:53"

# docker-compose.yml with environment
environment:
  - CF_API_EMAIL=admin@example.com
  - CF_API_KEY=your-cloudflare-api-key
```

### 2. **Canary Deployments**
```yaml
# dynamic/canary.yml
http:
  services:
    app-v1:
      loadBalancer:
        servers:
        - url: "http://app-v1:80"
        
    app-v2:
      loadBalancer:
        servers:
        - url: "http://app-v2:80"
        
    app-canary:
      weighted:
        services:
        - name: app-v1
          weight: 90
        - name: app-v2
          weight: 10

  routers:
    app:
      rule: "Host(`app.example.com`)"
      service: app-canary
      entryPoints:
        - websecure
      tls:
        certResolver: letsencrypt
```

### 3. **Authentication with Forward Auth**
```yaml
# dynamic/auth.yml
http:
  middlewares:
    auth-forward:
      forwardAuth:
        address: "http://auth-service:4181"
        trustForwardHeader: true
        authResponseHeaders:
          - "X-Forwarded-User"
          - "X-Auth-User"
          - "X-Secret"

  routers:
    protected-app:
      rule: "Host(`protected.example.com`)"
      service: protected-service
      middlewares:
        - auth-forward
      entryPoints:
        - websecure
      tls:
        certResolver: letsencrypt
```

## Best Practices

### 1. **Security Configuration**
```yaml
# Static configuration
global:
  checkNewVersion: false
  sendAnonymousUsage: false

api:
  dashboard: true
  debug: false
  # Secure dashboard access
  entryPoint: traefik

entryPoints:
  traefik:
    address: ":8080"
    http:
      middlewares:
        - auth@file
        - security-headers@file
  
# Dynamic configuration
http:
  middlewares:
    auth:
      basicAuth:
        users:
          - "admin:$2y$10$..." # Use htpasswd
        removeHeader: true
    
    security-headers:
      headers:
        accessControlAllowMethods:
          - GET
          - OPTIONS
          - PUT
          - POST
          - DELETE
        accessControlAllowOriginList:
          - "https://app.example.com"
        accessControlMaxAge: 100
        addVaryHeader: true
        browserXssFilter: true
        contentTypeNosniff: true
        frameDeny: true
        forceSTSHeader: true
        sslRedirect: true
        stsIncludeSubdomains: true
        stsPreload: true
        stsSeconds: 63072000
        customFrameOptionsValue: SAMEORIGIN
        contentSecurityPolicy: "default-src 'self'"
        referrerPolicy: "same-origin"
        featurePolicy: "camera 'none'; geolocation 'none'; microphone 'none'"
```

### 2. **Performance Optimization**
```yaml
# Static configuration
serversTransport:
  insecureSkipVerify: false
  maxIdleConnsPerHost: 200
  forwardingTimeouts:
    dialTimeout: 30s
    responseHeaderTimeout: 30s
    idleConnTimeout: 90s

# Dynamic configuration
http:
  services:
    app-service:
      loadBalancer:
        servers:
        - url: "http://app:80"
        sticky:
          cookie:
            name: app_session
            secure: true
            httpOnly: true
            sameSite: lax
        healthCheck:
          path: /health
          interval: 10s
          timeout: 3s
          hostname: app.internal
        passHostHeader: true
```

### 3. **Monitoring and Observability**
```yaml
# Static configuration
metrics:
  prometheus:
    buckets:
      - 0.1
      - 0.3
      - 1.2
      - 5.0
    addEntryPointsLabels: true
    addServicesLabels: true
    entryPoint: metrics

tracing:
  jaeger:
    samplingServerURL: http://jaeger:5778/sampling
    samplingType: const
    samplingParam: 1.0
    localAgentHostPort: jaeger:6831
    gen128Bit: true
    propagation: jaeger
    traceContextHeaderName: uber-trace-id

accessLog:
  filePath: /var/log/traefik/access.log
  format: json
  filters:
    statusCodes:
      - "200-299"
      - "400-499"
      - "500-599"
    retryAttempts: true
    minDuration: 10ms
  fields:
    defaultMode: keep
    headers:
      defaultMode: keep
      names:
        User-Agent: keep
        Authorization: drop
```

## Common Commands

### Docker Usage
```bash
# Run Traefik with Docker
docker run -d \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $PWD/traefik.yml:/traefik.yml \
  -v $PWD/acme.json:/acme.json \
  -p 80:80 \
  -p 443:443 \
  -p 8080:8080 \
  traefik:v2.10

# View Traefik logs
docker logs -f traefik

# Reload configuration (dynamic)
# Traefik automatically watches for changes

# Check configuration
docker run --rm -v $PWD/traefik.yml:/traefik.yml traefik:v2.10 version
```

### Kubernetes Commands
```bash
# Install Traefik with Helm
helm repo add traefik https://helm.traefik.io/traefik
helm install traefik traefik/traefik

# Check Traefik pods
kubectl get pods -n traefik

# View Traefik logs
kubectl logs -f deployment/traefik -n traefik

# Access dashboard (port-forward)
kubectl port-forward deployment/traefik 8080:8080 -n traefik

# Apply CRD
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v2.10/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml
```

### Configuration Management
```bash
# Validate configuration
traefik validate /etc/traefik/traefik.yml

# Generate self-signed certificates for testing
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=*.example.com"

# Convert to base64 for Kubernetes secrets
cat tls.crt | base64 -w 0
cat tls.key | base64 -w 0

# Check exposed routes
curl http://localhost:8080/api/http/routers

# Check services health
curl http://localhost:8080/api/http/services
```

## Interview Questions

### Basic Level
1. **Q: What is Traefik and how does it differ from traditional load balancers?**
   A: Traefik is a modern edge router that automatically discovers services and updates its configuration dynamically. Unlike traditional load balancers that require manual configuration, Traefik integrates with orchestrators and uses labels/annotations for configuration.

2. **Q: Explain Traefik's core components: Providers, Routers, Services, and Middlewares.**
   A: Providers discover services (Docker, Kubernetes), Routers match requests and define rules, Services represent backend applications with load balancing, and Middlewares transform requests/responses (auth, rate limiting, headers).

3. **Q: How does Traefik handle SSL/TLS certificates?**
   A: Traefik supports automatic certificate generation via Let's Encrypt, manual certificate configuration, and certificate stores. It can handle ACME challenges (HTTP, TLS, DNS) and automatically renew certificates.

### Intermediate Level
4. **Q: How do you implement blue-green deployments with Traefik?**
   A: Use weighted round-robin with two services, gradually shifting traffic weight from blue to green. Can be implemented with weighted services or by updating router rules to point to different services.

5. **Q: Explain Traefik's service discovery mechanisms.**
   A: Traefik uses providers to discover services: Docker (labels), Kubernetes (Ingress/CRD), Consul/Etcd (key-value), File (static/dynamic config). Each provider watches for changes and updates routes automatically.

6. **Q: How does Traefik handle high availability?**
   A: Deploy multiple Traefik instances behind a load balancer or using Kubernetes deployment. Use external storage for Let's Encrypt certificates, implement health checks, and ensure consistent configuration across instances.

### Advanced Level
7. **Q: Design a complete observability solution for Traefik.**
   A: Implement Prometheus metrics, Jaeger distributed tracing, structured JSON access logs, integration with ELK/Grafana, custom dashboards for SLI/SLO monitoring, and alerting rules for critical metrics.

8. **Q: How would you implement a custom middleware in Traefik?**
   A: While Traefik doesn't support custom middleware plugins directly in v2, you can: use ForwardAuth middleware to external service, chain existing middlewares creatively, or contribute to Traefik's plugin system.

9. **Q: Explain Traefik's circuit breaker implementation.**
   A: Traefik's circuit breaker monitors network errors and latency. When threshold is exceeded (e.g., NetworkErrorRatio() > 0.5), it trips and stops forwarding requests temporarily, protecting backend services from cascading failures.

### Scenario-Based
10. **Q: How would you migrate from nginx-ingress to Traefik in a production Kubernetes cluster?**
    A: Deploy Traefik alongside nginx, use different ingress classes, gradually migrate services by updating ingress annotations, implement monitoring for both, validate routing, update DNS/load balancers, then decommission nginx.

## Resources

### Official Documentation
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Traefik GitHub Repository](https://github.com/traefik/traefik)
- [Traefik Pilot (SaaS Platform)](https://traefik.io/traefik-pilot/)
- [Traefik Plugin Catalog](https://plugins.traefik.io/)

### Learning Resources
- [Traefik Quick Start](https://doc.traefik.io/traefik/getting-started/quick-start/)
- [Traefik Tutorials](https://traefik.io/resources/traefik-tutorials/)
- [Awesome Traefik](https://github.com/containous/awesome-traefik)
- [Traefik Workshop](https://github.com/traefik/workshop)

### Tools and Examples
- [Traefik Helm Chart](https://github.com/traefik/traefik-helm-chart)
- [Traefik Library (Go)](https://github.com/traefik/traefik-library-image)
- [Traefik Config Examples](https://github.com/traefik/traefik-examples)
- [Traefik Migration Tool](https://github.com/traefik/traefik-migration-tool)

### Community
- [Traefik Community Forum](https://community.traefik.io/)
- [Traefik Slack](https://traefik.slack.com/)
- [Stack Overflow - Traefik](https://stackoverflow.com/questions/tagged/traefik)
- [Reddit r/Traefik](https://www.reddit.com/r/Traefik/)

### Integrations
- [Traefik + Docker Guide](https://doc.traefik.io/traefik/providers/docker/)
- [Traefik + Kubernetes Guide](https://doc.traefik.io/traefik/providers/kubernetes-ingress/)
- [Traefik + Consul Integration](https://doc.traefik.io/traefik/providers/consul/)
- [Traefik + Let's Encrypt](https://doc.traefik.io/traefik/https/acme/)

### Performance and Best Practices
- [Traefik Best Practices](https://doc.traefik.io/traefik/operations/best-practices/)
- [Traefik Performance Tuning](https://traefik.io/blog/traefik-performance-tuning/)
- [Production Configuration Guide](https://traefik.io/blog/traefik-production-guide/)
- [Security Best Practices](https://doc.traefik.io/traefik/security/overview/)