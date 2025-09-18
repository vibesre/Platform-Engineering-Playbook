---
title: Kubernetes
description: Master container orchestration at scale with Kubernetes
---

# Kubernetes

Kubernetes is the de facto standard for container orchestration. As a platform engineer, deep Kubernetes knowledge is essential for building scalable, resilient infrastructure.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **Kubernetes Tutorial for Beginners - Full Course**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 4 hours](https://www.youtube.com/watch?v=X48VuDVv0do)
- **Why it's great**: Comprehensive introduction with hands-on demos

#### **Kubernetes Course - Full Beginners Tutorial**
- **Channel**: freeCodeCamp (by Bogdan Stashchuk)
- **Link**: [YouTube - 3.5 hours](https://www.youtube.com/watch?v=d6WC5n9G_sM)
- **Why it's great**: Well-structured with practical examples

#### **Kube by Example**
- **Channel**: Red Hat Developer
- **Link**: [YouTube Playlist](https://www.youtube.com/playlist?list=PLaR6Rq6Z4IqfGCkI28cUMbNhPhsnj4nq3)
- **Why it's great**: Short, focused videos on specific topics

### 📖 Essential Documentation

#### **Kubernetes Official Documentation**
- **Link**: [kubernetes.io/docs/](https://kubernetes.io/docs/)
- **Why it's great**: Comprehensive, always current, includes tutorials

#### **Kubernetes The Hard Way**
- **Author**: Kelsey Hightower
- **Link**: [github.com/kelseyhightower/kubernetes-the-hard-way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- **Why it's great**: Learn by building Kubernetes from scratch

#### **Kubernetes API Reference**
- **Link**: [kubernetes.io/docs/reference/kubernetes-api/](https://kubernetes.io/docs/reference/kubernetes-api/)
- **Why it's great**: Complete API documentation for all resources

### 📝 Must-Read Blogs & Articles

#### **Kubernetes Blog**
- **Link**: [kubernetes.io/blog/](https://kubernetes.io/blog/)
- **Why it's great**: Official updates and deep technical posts

#### **Learn k8s Security**
- **Link**: [learnk8s.io/production-best-practices](https://learnk8s.io/production-best-practices)
- **Why it's great**: Production-ready security practices

#### **The New Stack - Kubernetes**
- **Link**: [thenewstack.io/category/kubernetes/](https://thenewstack.io/category/kubernetes/)
- **Why it's great**: Industry trends and real-world use cases

### 🎓 Structured Courses

#### **Certified Kubernetes Administrator (CKA) Preparation**
- **Instructor**: Mumshad Mannambeth
- **Platform**: KodeKloud
- **Link**: [kodekloud.com/courses/certified-kubernetes-administrator-cka/](https://kodekloud.com/courses/certified-kubernetes-administrator-cka/)
- **Why it's great**: Hands-on labs, exam-focused content

#### **Kubernetes Fundamentals (LFS258)**
- **Provider**: Linux Foundation
- **Link**: [training.linuxfoundation.org/training/kubernetes-fundamentals/](https://training.linuxfoundation.org/training/kubernetes-fundamentals/)
- **Why it's great**: Official Linux Foundation training

### 🔧 Interactive Labs

#### **Killercoda Kubernetes**
- **Link**: [killercoda.com/kubernetes](https://killercoda.com/kubernetes)
- **Why it's great**: Free browser-based Kubernetes clusters

#### **Play with Kubernetes**
- **Link**: [labs.play-with-k8s.com](https://labs.play-with-k8s.com/)
- **Why it's great**: Free 4-hour Kubernetes sessions

#### **Kubernetes by Example**
- **Link**: [kubernetesbyexample.com](https://kubernetesbyexample.com/)
- **Why it's great**: Simple, practical examples

## 🎯 Key Concepts to Master

### Core Components

#### Control Plane
- **API Server**: Central management point
- **etcd**: Distributed key-value store
- **Scheduler**: Places pods on nodes
- **Controller Manager**: Runs controllers
- **Cloud Controller Manager**: Cloud-specific logic

#### Node Components
- **kubelet**: Node agent
- **kube-proxy**: Network proxy
- **Container Runtime**: Docker/containerd/CRI-O

### Essential Resources

#### Workloads
```yaml
# Deployment Example
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
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "250m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

#### Networking
```yaml
# Service Example
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer

---
# Ingress Example
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
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

### Essential kubectl Commands
```bash
# Cluster Info
kubectl cluster-info
kubectl get nodes
kubectl describe node node-name

# Working with Resources
kubectl apply -f manifest.yaml
kubectl get pods -n namespace
kubectl describe pod pod-name
kubectl logs pod-name -c container-name
kubectl exec -it pod-name -- /bin/bash

# Debugging
kubectl get events --sort-by='.lastTimestamp'
kubectl top nodes
kubectl top pods
kubectl port-forward pod-name 8080:80

# Managing Resources
kubectl scale deployment web-app --replicas=5
kubectl rollout status deployment/web-app
kubectl rollout undo deployment/web-app
kubectl delete -f manifest.yaml
```

### Advanced Concepts

#### Storage
- PersistentVolumes (PV)
- PersistentVolumeClaims (PVC)
- StorageClasses
- Volume snapshots

#### Security
- RBAC (Role-Based Access Control)
- Network Policies
- Pod Security Standards
- Secrets and ConfigMaps
- Service Accounts

#### Observability
- Metrics Server
- Prometheus integration
- Logging strategies
- Distributed tracing

## 💡 Interview Tips

### Common Interview Questions

1. **Explain Kubernetes architecture**
   - Master/Control plane components
   - Node components
   - Communication flow
   - etcd's role

2. **How does Kubernetes networking work?**
   - Cluster networking requirements
   - Service types (ClusterIP, NodePort, LoadBalancer)
   - Ingress controllers
   - Network policies

3. **Describe the pod lifecycle**
   - Pending → Running → Succeeded/Failed
   - Init containers
   - Readiness/Liveness probes
   - Graceful shutdown

4. **How do you handle persistent storage?**
   - PV/PVC model
   - Dynamic provisioning
   - Storage classes
   - Volume types

5. **Explain Kubernetes security best practices**
   - RBAC implementation
   - Network policies
   - Pod security standards
   - Image scanning
   - Secrets management

### Practical Scenarios
- "Deploy a highly available application"
- "Troubleshoot a pod that won't start"
- "Implement auto-scaling based on metrics"
- "Set up blue-green deployments"
- "Secure multi-tenant clusters"

## 🏆 Hands-On Practice

### Build These Projects

1. **Production-Grade Cluster**
   - Multi-master setup
   - Implement RBAC
   - Configure monitoring
   - Set up backup/restore

2. **GitOps Pipeline**
   - ArgoCD/Flux setup
   - Automated deployments
   - Progressive rollouts
   - Rollback strategies

3. **Service Mesh Implementation**
   - Install Istio/Linkerd
   - Traffic management
   - Security policies
   - Observability

4. **Stateful Application**
   - Deploy database with persistence
   - Implement backup strategies
   - Handle node failures
   - Performance tuning

### CKA Exam Preparation
- **Practice Environment**: [killer.sh](https://killer.sh)
- **Time Management**: 2 hours for ~17 questions
- **Key Areas**: 
  - Cluster architecture (25%)
  - Workloads & Scheduling (15%)
  - Services & Networking (20%)
  - Storage (10%)
  - Troubleshooting (30%)

## 📊 Learning Path

### Week 1-2: Fundamentals
- Core concepts
- Basic objects (Pods, Services, Deployments)
- kubectl mastery
- Local development (minikube/kind)

### Week 3-4: Application Deployment
- Multi-container pods
- ConfigMaps and Secrets
- Health checks
- Resource management

### Week 5-6: Production Topics
- RBAC and security
- Networking deep dive
- Storage solutions
- Monitoring and logging

### Week 7-8: Advanced Topics
- Operators and CRDs
- Helm charts
- CI/CD integration
- Multi-cluster management

---

**Next Steps**: After mastering Kubernetes basics, explore [Helm](/technical/helm) for package management and [Service Mesh](/technical/service-mesh) for advanced traffic management.