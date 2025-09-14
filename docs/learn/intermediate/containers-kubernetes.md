---
title: Containers & Kubernetes
sidebar_position: 2
tags: [intermediate, docker, kubernetes, containers]
---

# 🐳 Containers & Kubernetes

**Prerequisites**: Cloud fundamentals, basic Linux  
**Time to Complete**: ⏱️ 6-8 hours

## Introduction

Containers and Kubernetes are fundamental to modern platform engineering. This guide covers everything from Docker basics to production-ready Kubernetes deployments.

## Containers Fundamentals

### What are Containers?

Containers package applications with their dependencies, providing:
- **Consistency**: Same behavior across environments
- **Isolation**: Process and resource isolation
- **Portability**: Run anywhere
- **Efficiency**: Lighter than VMs

### Docker Deep Dive

#### Docker Architecture
```
┌─────────────────────────────────────┐
│          Docker Client              │
│     (docker build, run, pull)       │
└────────────────┬────────────────────┘
                 │ REST API
┌────────────────▼────────────────────┐
│          Docker Daemon              │
│         (dockerd)                   │
├─────────────────────────────────────┤
│  Images  │ Containers │  Networks   │
│  Storage │ Volumes    │  Plugins    │
└─────────────────────────────────────┘
```

#### Essential Docker Commands

```bash
# Image operations
docker build -t myapp:v1 .
docker push myapp:v1
docker pull nginx:latest
docker images

# Container operations
docker run -d -p 8080:80 --name web nginx
docker ps -a
docker logs web
docker exec -it web bash
docker stop web
docker rm web

# Cleanup
docker system prune -a
docker volume prune
```

#### Writing Effective Dockerfiles

```dockerfile
# Multi-stage build example
FROM golang:1.19 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Final stage
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
```

Best practices:
- Use specific base image tags
- Minimize layers
- Order commands by change frequency
- Use .dockerignore
- Run as non-root user
- Scan for vulnerabilities

#### Container Security

```bash
# Security scanning
docker scan myapp:v1

# Run as non-root
FROM node:16-alpine
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Read-only filesystem
docker run --read-only myapp:v1
```

## Kubernetes Fundamentals

### Architecture Overview

```
Control Plane
├── API Server (kube-apiserver)
├── Scheduler (kube-scheduler)
├── Controller Manager
├── etcd (key-value store)
└── Cloud Controller Manager

Worker Nodes
├── kubelet
├── kube-proxy
└── Container Runtime
```

### Core Concepts

#### Pods
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

#### Deployments
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: myapp:v1
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### Services
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
  type: LoadBalancer
```

### Kubernetes Networking

#### Service Types
- **ClusterIP**: Internal cluster communication
- **NodePort**: Exposes service on node ports
- **LoadBalancer**: Cloud provider load balancer
- **ExternalName**: Maps to external DNS name

#### Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

### Storage in Kubernetes

#### Persistent Volumes
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:14
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

### Configuration Management

#### ConfigMaps and Secrets
```yaml
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "postgres://localhost:5432/myapp"
  log_level: "info"

---
# Secret
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  api_key: "your-secret-api-key"
  db_password: "super-secret-password"

---
# Using in Pod
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:v1
    env:
    - name: DATABASE_URL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database_url
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: api_key
```

### Advanced Kubernetes Patterns

#### Sidecar Pattern
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  - name: app
    image: myapp:v1
    ports:
    - containerPort: 8080
  - name: logging-agent
    image: fluentd:latest
    volumeMounts:
    - name: logs
      mountPath: /var/log
  volumes:
  - name: logs
    emptyDir: {}
```

#### Init Containers
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  initContainers:
  - name: init-db
    image: busybox:1.28
    command: ['sh', '-c', 'until nc -z db-service 5432; do sleep 1; done']
  containers:
  - name: myapp
    image: myapp:v1
```

## Kubernetes Operations

### Cluster Management

#### kubectl Essential Commands
```bash
# Cluster info
kubectl cluster-info
kubectl get nodes
kubectl top nodes
kubectl top pods

# Resource management
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml
kubectl scale deployment web --replicas=5
kubectl rollout status deployment/web
kubectl rollout undo deployment/web

# Debugging
kubectl describe pod web-xxx
kubectl logs web-xxx -c container-name
kubectl exec -it web-xxx -- /bin/bash
kubectl port-forward pod/web-xxx 8080:80

# Namespace operations
kubectl create namespace production
kubectl config set-context --current --namespace=production
```

### Security Best Practices

#### RBAC (Role-Based Access Control)
```yaml
# ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production

---
# Role
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list"]

---
# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rolebinding
  namespace: production
subjects:
- kind: ServiceAccount
  name: app-sa
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

#### Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-netpol
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

## Production Considerations

### High Availability

#### Multi-Master Setup
```yaml
# Deploy across availability zones
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 6
  template:
    spec:
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: web
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - web
            topologyKey: kubernetes.io/hostname
```

### Monitoring and Observability

#### Prometheus Metrics
```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-metrics
  labels:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
spec:
  selector:
    app: myapp
  ports:
  - name: metrics
    port: 9090
```

### Resource Management

#### Resource Quotas
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: production
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    limits.cpu: "200"
    limits.memory: 400Gi
    persistentvolumeclaims: "10"
```

## Interview Preparation

### Common Kubernetes Interview Questions

**Q: Explain the Kubernetes architecture**
Cover:
- Control plane components (API server, scheduler, controller manager, etcd)
- Node components (kubelet, kube-proxy, container runtime)
- Add-ons (DNS, dashboard, monitoring)

**Q: How does Kubernetes networking work?**
Explain:
- Cluster networking requirements
- Service discovery and DNS
- Ingress controllers
- Network policies

**Q: Describe a challenging Kubernetes issue you've solved**
Structure your answer:
- Situation: Production cluster issue
- Task: Your responsibility
- Action: Steps taken to diagnose and fix
- Result: Outcome and lessons learned

### Hands-On Scenarios

**Scenario 1: Debug a failing deployment**
```bash
# Check deployment status
kubectl get deployment web-app
kubectl describe deployment web-app

# Check pods
kubectl get pods -l app=web
kubectl describe pod web-app-xxx

# Check logs
kubectl logs web-app-xxx --previous

# Common issues:
# - Image pull errors
# - Resource constraints
# - Liveness probe failures
# - Configuration errors
```

**Scenario 2: Scale an application**
```bash
# Horizontal scaling
kubectl scale deployment web --replicas=10

# Autoscaling
kubectl autoscale deployment web \
  --min=2 --max=10 --cpu-percent=80

# Vertical scaling (requires VPA)
# Update resource requests/limits
```

## Practice Projects

### Project 1: Local Kubernetes Development
1. Install kind or minikube
2. Deploy a multi-tier application
3. Implement service discovery
4. Add persistent storage
5. Configure ingress

### Project 2: Production-Ready Deployment
1. Create Helm charts
2. Implement GitOps with ArgoCD
3. Set up monitoring with Prometheus
4. Configure autoscaling
5. Implement security policies

### Project 3: Kubernetes Operator
1. Choose a use case (backup, scaling, etc.)
2. Use Operator SDK or Kubebuilder
3. Implement reconciliation logic
4. Add validation webhooks
5. Write tests

## Next Steps

You're ready to continue with:
- [CI/CD & Automation →](cicd-automation)
- [Observability & Monitoring →](observability)

## Quick Reference

### kubectl Cheat Sheet
```bash
# Contexts
kubectl config get-contexts
kubectl config use-context prod

# Quick edits
kubectl edit deployment web
kubectl patch svc web -p '{"spec":{"type":"LoadBalancer"}}'

# Useful aliases
alias k=kubectl
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'
alias kaf='kubectl apply -f'
```

### Debugging Commands
```bash
# Resource usage
kubectl top nodes
kubectl top pods --all-namespaces

# Events
kubectl get events --sort-by=.metadata.creationTimestamp

# Describe resources
kubectl describe node worker-1
kubectl describe pod web-xxx
```

## Additional Resources

- 📚 **Book**: [Kubernetes in Action](https://www.manning.com/books/kubernetes-in-action-second-edition)
- 🎓 **Certification**: [CKA Exam Guide](https://www.cncf.io/certification/cka/)
- 🎮 **Practice**: [Killercoda Kubernetes](https://killercoda.com/kubernetes)
- 📺 **Video**: [Kubernetes Course - TechWorld with Nana](https://www.youtube.com/watch?v=X48VuDVv0do)