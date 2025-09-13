---
title: Kubernetes Mastery
sidebar_position: 3
---

# Kubernetes Mastery for Platform Engineers

An in-depth guide to Kubernetes architecture, operations, and platform engineering on K8s.

## Kubernetes Architecture Deep Dive

### Control Plane Components

**API Server (kube-apiserver)**
- Central management point
- RESTful API interface
- Authentication and authorization
- Admission controllers

```yaml
# API server key features
- RBAC (Role-Based Access Control)
- Admission webhooks
- API aggregation
- OpenAPI schema validation
```

**etcd**
- Distributed key-value store
- Cluster state storage
- Consistency via Raft consensus
- Watch functionality for changes

```bash
# etcd operations
etcdctl get / --prefix --keys-only
etcdctl snapshot save backup.db
etcdctl member list
```

**Scheduler (kube-scheduler)**
- Pod placement decisions
- Resource requirements evaluation
- Affinity/anti-affinity rules
- Custom schedulers

```yaml
# Scheduling example
apiVersion: v1
kind: Pod
spec:
  nodeSelector:
    disktype: ssd
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - topologyKey: kubernetes.io/hostname
```

**Controller Manager**
- Runs controller loops
- Maintains desired state
- Built-in controllers:
  - ReplicaSet
  - Deployment
  - StatefulSet
  - DaemonSet
  - Job/CronJob

**Resources:**
- 📖 [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- 🎥 [Kubernetes Architecture Explained](https://www.youtube.com/watch?v=M7t-g35jMuM)
- 📚 [Kubernetes Up & Running](https://www.oreilly.com/library/view/kubernetes-up-and/9781491935668/)

### Data Plane Components

**kubelet**
- Node agent
- Pod lifecycle management
- Container runtime interface (CRI)
- Health checking

```bash
# kubelet debugging
journalctl -u kubelet -f
kubectl get --raw /api/v1/nodes/<node>/proxy/stats/summary
```

**kube-proxy**
- Network proxy
- Service abstraction implementation
- iptables/IPVS modes
- Connection tracking

```bash
# kube-proxy modes
kubectl get configmap kube-proxy -n kube-system -o yaml
# Check iptables rules
iptables-save | grep KUBE-SERVICES
```

**Container Runtime**
- Docker (deprecated)
- containerd
- CRI-O
- Runtime classes

```yaml
# RuntimeClass example
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
```

## Advanced Networking

### Network Models

**Cluster Networking Requirements:**
1. All pods can communicate without NAT
2. All nodes can communicate with pods without NAT
3. Pod sees its own IP address

**CNI Plugins Comparison:**

| Plugin | Mode | Performance | Features |
|--------|------|-------------|----------|
| Calico | L3 | High | Network policies, BGP |
| Flannel | Overlay | Medium | Simple, VXLAN |
| Cilium | eBPF | Very High | L7 policies, observability |
| Weave | Overlay | Medium | Encryption, multicast |

### Service Types and Ingress

**Service Types:**
```yaml
# ClusterIP - Internal only
apiVersion: v1
kind: Service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80

# LoadBalancer - Cloud provider LB
spec:
  type: LoadBalancer
  loadBalancerIP: 1.2.3.4

# NodePort - External access via node ports
spec:
  type: NodePort
  ports:
  - port: 80
    nodePort: 30080
```

**Ingress Controllers:**
```yaml
# Ingress with path-based routing
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

**Resources:**
- 📖 [Kubernetes Networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
- 🎥 [Container Networking From Scratch](https://www.youtube.com/watch?v=B6FsWNUnRo0)
- 📖 [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

### Network Policies

```yaml
# Deny all ingress traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress

# Allow specific traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080
```

## Storage Architecture

### Storage Classes and Dynamic Provisioning

```yaml
# StorageClass definition
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
volumeBindingMode: WaitForFirstConsumer
```

### Persistent Volumes and Claims

```yaml
# PVC with specific requirements
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: database-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: fast-ssd
  selector:
    matchLabels:
      tier: production
```

### CSI (Container Storage Interface)

**CSI Driver Implementation:**
- Identity Service
- Controller Service
- Node Service

```yaml
# CSI Driver deployment
apiVersion: storage.k8s.io/v1
kind: CSIDriver
metadata:
  name: csi.example.com
spec:
  attachRequired: true
  podInfoOnMount: true
  volumeLifecycleModes:
  - Persistent
  - Ephemeral
```

**Resources:**
- 📖 [Kubernetes Storage](https://kubernetes.io/docs/concepts/storage/)
- 🎥 [Storage Deep Dive](https://www.youtube.com/watch?v=yqiTA9cyIyA)
- 📖 [CSI Specification](https://github.com/container-storage-interface/spec)

## Security Best Practices

### RBAC (Role-Based Access Control)

```yaml
# ClusterRole for platform team
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: platform-engineer
rules:
- apiGroups: ["*"]
  resources: ["nodes", "persistentvolumes"]
  verbs: ["*"]
- apiGroups: ["apps"]
  resources: ["deployments", "daemonsets", "statefulsets"]
  verbs: ["get", "list", "watch"]

# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: platform-engineer-binding
  namespace: production
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: platform-engineer
subjects:
- kind: User
  name: john@example.com
```

### Pod Security Standards

```yaml
# Pod Security Policy (deprecated, use Pod Security Standards)
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
```

### Secrets Management

```yaml
# External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "demo"
```

**Resources:**
- 📖 [Kubernetes Security](https://kubernetes.io/docs/concepts/security/)
- 🎥 [Kubernetes Security Best Practices](https://www.youtube.com/watch?v=oBf5lrmquYI)
- 📚 [Kubernetes Security - Operating Kubernetes Clusters and Applications Safely](https://www.oreilly.com/library/view/kubernetes-security/9781492046219/)

## Observability and Monitoring

### Metrics Architecture

```yaml
# Prometheus ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-metrics
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### Logging Architecture

**Logging Patterns:**
1. Node-level logging
2. Sidecar container pattern
3. DaemonSet collectors

```yaml
# Fluentd DaemonSet config
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      <parse>
        @type json
        time_format %Y-%m-%dT%H:%M:%S.%N%z
      </parse>
    </source>
```

### Distributed Tracing

```yaml
# OpenTelemetry Collector
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
data:
  otel-collector-config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
          http:
    processors:
      batch:
    exporters:
      jaeger:
        endpoint: jaeger-collector:14250
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [batch]
          exporters: [jaeger]
```

## Advanced Deployment Patterns

### GitOps with ArgoCD

```yaml
# ArgoCD Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: production-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/company/k8s-manifests
    targetRevision: HEAD
    path: production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Progressive Delivery with Flagger

```yaml
# Canary deployment
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: myapp
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  progressDeadlineSeconds: 60
  service:
    port: 80
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
```

## Platform Engineering on Kubernetes

### Multi-Tenancy Patterns

**Namespace Isolation:**
```yaml
# ResourceQuota per namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
  namespace: team-a
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    persistentvolumeclaims: "10"
```

**Network Isolation:**
```yaml
# Default deny all NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Custom Resource Definitions (CRDs)

```yaml
# Platform service CRD
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: platformservices.platform.io
spec:
  group: platform.io
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              tier:
                type: string
                enum: ["production", "staging", "development"]
              autoscaling:
                type: boolean
              monitoring:
                type: boolean
```

### Operator Development

```go
// Operator reconciliation loop
func (r *PlatformServiceReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var platformService v1.PlatformService
    if err := r.Get(ctx, req.NamespacedName, &platformService); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // Ensure deployment exists
    deployment := r.deploymentForPlatformService(&platformService)
    if err := r.Create(ctx, deployment); err != nil {
        return ctrl.Result{}, err
    }
    
    // Update status
    platformService.Status.Ready = true
    if err := r.Status().Update(ctx, &platformService); err != nil {
        return ctrl.Result{}, err
    }
    
    return ctrl.Result{RequeueAfter: time.Minute}, nil
}
```

## Troubleshooting Guide

### Common Issues and Solutions

**1. Pod Stuck in Pending:**
```bash
kubectl describe pod <pod-name>
kubectl get events --sort-by='.lastTimestamp'
kubectl get nodes -o wide
kubectl describe node <node-name>
```

**2. CrashLoopBackOff:**
```bash
kubectl logs <pod-name> --previous
kubectl describe pod <pod-name>
kubectl exec -it <pod-name> -- /bin/sh
```

**3. Service Discovery Issues:**
```bash
kubectl get endpoints
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- bash
nslookup kubernetes.default
```

**4. Performance Issues:**
```bash
kubectl top nodes
kubectl top pods --all-namespaces
kubectl get hpa
kubectl describe hpa <hpa-name>
```

### Debugging Tools

```bash
# kubectl plugins
kubectl krew install debug
kubectl debug node/<node-name> -it --image=ubuntu

# Network debugging
kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot
kubectl exec -it tmp-shell -- tcpdump -i any -w trace.pcap

# Resource analysis
kubectl get pods --all-namespaces -o json | jq '.items[] | {namespace: .metadata.namespace, name: .metadata.name, cpu: .spec.containers[].resources.requests.cpu, memory: .spec.containers[].resources.requests.memory}'
```

## Production Best Practices

### High Availability

1. **Control Plane HA:**
   - Multiple API servers behind LB
   - etcd cluster with odd number of nodes
   - Leader election for controllers

2. **Data Plane HA:**
   - Multiple nodes across AZs
   - Pod disruption budgets
   - Node affinity rules

```yaml
# PodDisruptionBudget
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
```

### Resource Management

```yaml
# Resource limits and requests
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

# Vertical Pod Autoscaler
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: app-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: app
  updatePolicy:
    updateMode: "Auto"
```

## Certification and Learning Path

### Certifications
- 🎓 [CKA (Certified Kubernetes Administrator)](https://www.cncf.io/certification/cka/)
- 🎓 [CKAD (Certified Kubernetes Application Developer)](https://www.cncf.io/certification/ckad/)
- 🎓 [CKS (Certified Kubernetes Security Specialist)](https://www.cncf.io/certification/cks/)

### Learning Resources
- 📚 [Kubernetes in Action](https://www.manning.com/books/kubernetes-in-action-second-edition)
- 📚 [Production Kubernetes](https://www.oreilly.com/library/view/production-kubernetes/9781492092298/)
- 🎥 [Kubernetes Course - TechWorld with Nana](https://www.youtube.com/watch?v=X48VuAPVBBg)
- 🎮 [Kubernetes the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- 📖 [Kubernetes Documentation](https://kubernetes.io/docs/)
- 🎯 [KillerCoda Interactive Scenarios](https://killercoda.com/kubernetes)

### Community Resources
- 💬 [Kubernetes Slack](https://kubernetes.slack.com)
- 📖 [CNCF Blog](https://www.cncf.io/blog/)
- 🎥 [KubeCon Talks](https://www.youtube.com/c/cloudnativefdn)

Remember: Kubernetes is rapidly evolving. Stay updated with the latest releases and best practices through official documentation and community resources.