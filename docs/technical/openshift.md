# OpenShift - Enterprise Kubernetes Platform by Red Hat

## Overview

OpenShift is Red Hat's enterprise-grade Kubernetes platform that provides a complete container application platform for both on-premises and cloud deployments. Built on top of Kubernetes, OpenShift adds developer and operations-centric tools, enterprise-grade security, and automated operations to enable organizations to develop, deploy, and manage container-based applications at scale.

## Architecture

### Platform Architecture

```
┌─────────────────────────────────────────────────────┐
│              OpenShift Web Console                  │
├─────────────────────────────────────────────────────┤
│         OpenShift API / Route Layer                 │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────┐  ┌───────────────┐ │
│  │   Projects   │  │  Builds   │  │   Templates   │ │
│  │  (Namespace) │  │  (S2I)    │  │   Operators   │ │
│  └─────────────┘  └──────────┘  └───────────────┘ │
├─────────────────────────────────────────────────────┤
│              Kubernetes Control Plane               │
│  ┌─────────────┐  ┌──────────┐  ┌───────────────┐ │
│  │  API Server │  │Controller │  │   Scheduler   │ │
│  │             │  │  Manager  │  │               │ │
│  └─────────────┘  └──────────┘  └───────────────┘ │
├─────────────────────────────────────────────────────┤
│                  Worker Nodes                       │
│  ┌─────────────┐  ┌──────────┐  ┌───────────────┐ │
│  │   CRI-O     │  │   SDN     │  │   Storage     │ │
│  │  Runtime    │  │ (OVN/OVS) │  │   (CSI)       │ │
│  └─────────────┘  └──────────┘  └───────────────┘ │
├─────────────────────────────────────────────────────┤
│          RHEL CoreOS / RHEL (Immutable OS)         │
└─────────────────────────────────────────────────────┘
```

### Key Components

- **RHEL CoreOS**: Immutable operating system optimized for containers
- **CRI-O**: Lightweight container runtime for Kubernetes
- **OpenShift SDN**: Software-defined networking with multiple plugin options
- **Integrated Registry**: Built-in container image registry
- **Source-to-Image (S2I)**: Build containers directly from source code
- **Operators**: Automated application lifecycle management
- **Web Console**: Comprehensive UI for developers and administrators

## Installation and Configuration

### OpenShift Installation Methods

#### 1. Installer-Provisioned Infrastructure (IPI)
```bash
# Download installer
wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-install-linux.tar.gz
tar xvf openshift-install-linux.tar.gz

# Create install config
./openshift-install create install-config --dir=<installation_directory>
```

#### Example install-config.yaml
```yaml
apiVersion: v1
baseDomain: example.com
metadata:
  name: production
compute:
- architecture: amd64
  hyperthreading: Enabled
  name: worker
  replicas: 3
  platform:
    aws:
      type: m5.xlarge
      zones:
      - us-east-1a
      - us-east-1b
      - us-east-1c
controlPlane:
  architecture: amd64
  hyperthreading: Enabled
  name: master
  replicas: 3
  platform:
    aws:
      type: m5.xlarge
      zones:
      - us-east-1a
      - us-east-1b
      - us-east-1c
platform:
  aws:
    region: us-east-1
pullSecret: '<pull_secret>'
sshKey: '<ssh_public_key>'
```

#### 2. User-Provisioned Infrastructure (UPI)
```bash
# Generate manifests
./openshift-install create manifests --dir=<installation_directory>

# Generate ignition configs
./openshift-install create ignition-configs --dir=<installation_directory>

# Deploy infrastructure and bootstrap
# (Infrastructure-specific steps)

# Complete installation
./openshift-install wait-for bootstrap-complete --dir=<installation_directory>
./openshift-install wait-for install-complete --dir=<installation_directory>
```

### Post-Installation Configuration

#### Configure Authentication
```yaml
# oauth-htpasswd.yaml
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: htpasswd_provider
    mappingMethod: claim
    type: HTPasswd
    htpasswd:
      fileData:
        name: htpass-secret
```

```bash
# Create users
htpasswd -c -B -b htpasswd admin password123
htpasswd -B -b htpasswd developer dev123

# Create secret
oc create secret generic htpass-secret --from-file=htpasswd -n openshift-config

# Apply OAuth config
oc apply -f oauth-htpasswd.yaml
```

#### Configure Storage
```yaml
# storage-class.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```

## Developer Features

### Source-to-Image (S2I) Builds

#### Create S2I Build
```yaml
# nodejs-build.yaml
apiVersion: build.openshift.io/v1
kind: BuildConfig
metadata:
  name: nodejs-app
spec:
  source:
    type: Git
    git:
      uri: https://github.com/example/nodejs-app
      ref: main
  strategy:
    type: Source
    sourceStrategy:
      from:
        kind: ImageStreamTag
        name: nodejs:14-ubi8
        namespace: openshift
  output:
    to:
      kind: ImageStreamTag
      name: nodejs-app:latest
  triggers:
  - type: GitHub
    github:
      secret: webhook-secret
  - type: ConfigChange
```

```bash
# Start build
oc new-app nodejs~https://github.com/example/nodejs-app

# Or using BuildConfig
oc create -f nodejs-build.yaml
oc start-build nodejs-app

# Follow build logs
oc logs -f bc/nodejs-app
```

### OpenShift Templates

#### Application Template
```yaml
# app-template.yaml
apiVersion: template.openshift.io/v1
kind: Template
metadata:
  name: nodejs-mongodb-example
  annotations:
    description: "Node.js application with MongoDB"
parameters:
- name: APPLICATION_NAME
  description: "Application name"
  required: true
- name: MONGODB_USER
  description: "MongoDB username"
  generate: expression
  from: "user[A-Z0-9]{3}"
- name: MONGODB_PASSWORD
  description: "MongoDB password"
  generate: expression
  from: "[a-zA-Z0-9]{12}"
objects:
- apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: ${APPLICATION_NAME}
  spec:
    replicas: 2
    selector:
      matchLabels:
        app: ${APPLICATION_NAME}
    template:
      metadata:
        labels:
          app: ${APPLICATION_NAME}
      spec:
        containers:
        - name: nodejs
          image: nodejs:14
          env:
          - name: MONGODB_USER
            value: ${MONGODB_USER}
          - name: MONGODB_PASSWORD
            value: ${MONGODB_PASSWORD}
- apiVersion: v1
  kind: Service
  metadata:
    name: ${APPLICATION_NAME}
  spec:
    selector:
      app: ${APPLICATION_NAME}
    ports:
    - port: 8080
      targetPort: 8080
```

```bash
# Process and create template
oc process -f app-template.yaml -p APPLICATION_NAME=myapp | oc create -f -

# List templates
oc get templates -n openshift
```

### Developer Console Features

#### Web Terminal
```bash
# Install Web Terminal Operator
oc apply -f - <<EOF
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: web-terminal
  namespace: openshift-operators
spec:
  channel: fast
  name: web-terminal
  source: redhat-operators
  sourceNamespace: openshift-marketplace
EOF
```

#### Developer Catalog
```bash
# Add custom catalog source
oc apply -f - <<EOF
apiVersion: operators.coreos.com/v1alpha1
kind: CatalogSource
metadata:
  name: custom-catalog
  namespace: openshift-marketplace
spec:
  sourceType: grpc
  image: quay.io/example/custom-catalog:latest
  displayName: Custom Operators
  publisher: Example Corp
EOF
```

## Security Features

### Security Context Constraints (SCC)

#### Default SCCs
```bash
# List SCCs
oc get scc

# Describe restricted SCC
oc describe scc restricted

# Create custom SCC
cat <<EOF | oc create -f -
apiVersion: security.openshift.io/v1
kind: SecurityContextConstraints
metadata:
  name: custom-scc
allowPrivilegedContainer: false
allowHostNetwork: false
allowHostPorts: false
allowHostPID: false
allowHostIPC: false
readOnlyRootFilesystem: false
requiredDropCapabilities:
- KILL
- MKNOD
- SETUID
- SETGID
runAsUser:
  type: MustRunAsRange
  uidRangeMin: 1000
  uidRangeMax: 2000
seLinuxContext:
  type: MustRunAs
fsGroup:
  type: RunAsAny
supplementalGroups:
  type: RunAsAny
EOF
```

#### Assign SCC to Service Account
```bash
# Create service account
oc create serviceaccount custom-sa

# Add SCC to service account
oc adm policy add-scc-to-user custom-scc -z custom-sa

# Use in deployment
oc set serviceaccount deployment/myapp custom-sa
```

### Network Policies

#### Ingress Control
```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    - namespaceSelector:
        matchLabels:
          name: production
    ports:
    - protocol: TCP
      port: 8080
```

#### Egress Control
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: restrict-egress
spec:
  podSelector:
    matchLabels:
      app: secure-app
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          app: logging
  - to:
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
```

### Image Security

#### Image Signing and Scanning
```bash
# Configure image signature verification
oc apply -f - <<EOF
apiVersion: config.openshift.io/v1
kind: Image
metadata:
  name: cluster
spec:
  registrySources:
    insecureRegistries:
    - registry.example.com
    blockedRegistries:
    - untrusted.registry.com
    allowedRegistries:
    - quay.io
    - registry.redhat.io
    - docker.io
EOF
```

#### Container Security Operator
```bash
# Install Container Security Operator
oc apply -f - <<EOF
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: container-security-operator
  namespace: openshift-operators
spec:
  channel: stable
  name: container-security-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
EOF

# View vulnerabilities
oc get imagemanifestvuln -n <namespace>
```

## Operators and Automation

### Operator Lifecycle Manager (OLM)

#### Install Operator via CLI
```bash
# Create OperatorGroup
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: my-operatorgroup
  namespace: my-namespace
spec:
  targetNamespaces:
  - my-namespace
EOF

# Create Subscription
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: postgresql
  namespace: my-namespace
spec:
  channel: stable
  name: postgresql
  source: certified-operators
  sourceNamespace: openshift-marketplace
EOF
```

### Custom Operator Development

#### Operator SDK Project
```bash
# Install Operator SDK
wget https://github.com/operator-framework/operator-sdk/releases/download/v1.32.0/operator-sdk_linux_amd64
chmod +x operator-sdk_linux_amd64
sudo mv operator-sdk_linux_amd64 /usr/local/bin/operator-sdk

# Create new operator
operator-sdk init --domain example.com --repo github.com/example/memcached-operator

# Create API
operator-sdk create api --group cache --version v1alpha1 --kind Memcached --resource --controller

# Generate manifests
make manifests

# Build and push operator image
make docker-build docker-push IMG=quay.io/example/memcached-operator:v0.0.1
```

#### Deploy Custom Operator
```bash
# Deploy CRDs
make install

# Deploy operator
make deploy IMG=quay.io/example/memcached-operator:v0.0.1

# Create CR instance
cat <<EOF | oc apply -f -
apiVersion: cache.example.com/v1alpha1
kind: Memcached
metadata:
  name: memcached-sample
spec:
  size: 3
EOF
```

## Performance Optimization

### Node Tuning

#### Node Tuning Operator
```yaml
# performance-profile.yaml
apiVersion: performance.openshift.io/v2
kind: PerformanceProfile
metadata:
  name: performance-patch
spec:
  cpu:
    isolated: "2-19,22-39"
    reserved: "0-1,20-21"
  hugepages:
    defaultHugepagesSize: "1G"
    pages:
    - size: "1G"
      count: 16
      node: 0
  realTimeKernel:
    enabled: true
  numa:
    topologyPolicy: "restricted"
  nodeSelector:
    node-role.kubernetes.io/worker-cnf: ""
```

### Resource Management

#### Cluster Resource Quotas
```yaml
apiVersion: quota.openshift.io/v1
kind: ClusterResourceQuota
metadata:
  name: developer-quota
spec:
  quota:
    hard:
      persistentvolumeclaims: "10"
      requests.storage: "50Gi"
      requests.cpu: "20"
      requests.memory: "40Gi"
  selector:
    annotations:
      team: development
```

#### Limit Ranges
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: compute-resources
spec:
  limits:
  - max:
      cpu: "2"
      memory: "4Gi"
    min:
      cpu: "100m"
      memory: "128Mi"
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "200m"
      memory: "256Mi"
    type: Container
  - max:
      storage: "10Gi"
    min:
      storage: "1Gi"
    type: PersistentVolumeClaim
```

### Application Performance

#### Horizontal Pod Autoscaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

## CI/CD Integration

### OpenShift Pipelines (Tekton)

#### Pipeline Definition
```yaml
# pipeline.yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: build-and-deploy
spec:
  workspaces:
  - name: shared-workspace
  params:
  - name: git-url
    type: string
  - name: git-revision
    type: string
    default: main
  - name: IMAGE
    type: string
  tasks:
  - name: fetch-source
    taskRef:
      name: git-clone
      kind: ClusterTask
    workspaces:
    - name: output
      workspace: shared-workspace
    params:
    - name: url
      value: $(params.git-url)
    - name: revision
      value: $(params.git-revision)
  - name: build-image
    taskRef:
      name: buildah
      kind: ClusterTask
    runAfter:
    - fetch-source
    workspaces:
    - name: source
      workspace: shared-workspace
    params:
    - name: IMAGE
      value: $(params.IMAGE)
  - name: deploy
    taskRef:
      name: openshift-client
      kind: ClusterTask
    runAfter:
    - build-image
    params:
    - name: SCRIPT
      value: |
        oc rollout status deployment/$(params.app-name)
```

#### PipelineRun
```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: build-deploy-run
spec:
  pipelineRef:
    name: build-and-deploy
  params:
  - name: git-url
    value: https://github.com/example/app
  - name: IMAGE
    value: image-registry.openshift-image-registry.svc:5000/project/app:latest
  workspaces:
  - name: shared-workspace
    persistentVolumeClaim:
      claimName: pipeline-workspace
```

### GitOps with OpenShift

#### ArgoCD Integration
```yaml
# argocd-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: production-app
  namespace: openshift-gitops
spec:
  project: default
  source:
    repoURL: https://github.com/example/app-config
    targetRevision: HEAD
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

## Monitoring and Logging

### Cluster Monitoring

#### Custom Metrics
```yaml
# servicemonitor.yaml
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

#### Custom Alerts
```yaml
# prometheusrule.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: app-alerts
spec:
  groups:
  - name: app.rules
    interval: 30s
    rules:
    - alert: HighMemoryUsage
      expr: container_memory_usage_bytes{pod=~"myapp-.*"} / container_spec_memory_limit_bytes > 0.9
      for: 5m
      annotations:
        summary: "High memory usage detected"
        description: "Pod {{ $labels.pod }} memory usage is above 90%"
```

### Centralized Logging

#### Configure Log Forwarding
```yaml
# clusterlogforwarder.yaml
apiVersion: logging.openshift.io/v1
kind: ClusterLogForwarder
metadata:
  name: instance
  namespace: openshift-logging
spec:
  outputs:
  - name: elasticsearch
    type: elasticsearch
    url: https://elasticsearch.example.com:9200
    secret:
      name: elasticsearch-secret
  - name: splunk
    type: splunk
    url: https://splunk.example.com:8088
    secret:
      name: splunk-secret
  pipelines:
  - name: application-logs
    inputRefs:
    - application
    outputRefs:
    - elasticsearch
    labels:
      environment: production
  - name: audit-logs
    inputRefs:
    - audit
    outputRefs:
    - splunk
```

## Troubleshooting

### Common Issues

#### 1. Node Not Ready
```bash
# Check node status
oc get nodes
oc describe node <node-name>

# Check kubelet logs
oc adm node-logs <node-name> -u kubelet

# Check system services
oc debug node/<node-name>
chroot /host
systemctl status kubelet
systemctl status crio
```

#### 2. Pod Scheduling Issues
```bash
# Check pod events
oc describe pod <pod-name>

# Check scheduler logs
oc logs -n openshift-kube-scheduler openshift-kube-scheduler-<master-node>

# Check resource availability
oc adm top nodes
oc describe node <node-name> | grep -A 5 "Allocated resources"
```

#### 3. Registry Issues
```bash
# Check registry pods
oc get pods -n openshift-image-registry

# Check registry route
oc get route -n openshift-image-registry

# Test registry access
podman login -u $(oc whoami) -p $(oc whoami -t) default-route-openshift-image-registry.apps.<cluster-domain>

# Check registry storage
oc get pvc -n openshift-image-registry
```

### Debug Commands

```bash
# Start debug pod
oc debug node/<node-name>

# Run diagnostic tool
oc adm diagnostics

# Collect must-gather data
oc adm must-gather

# Check cluster operators
oc get clusteroperators

# View cluster version
oc get clusterversion
```

## Best Practices for Production

### 1. Cluster Hardening

```bash
# Disable self-provisioning
oc patch clusterrolebinding.rbac self-provisioners -p '{"subjects": null}'

# Configure audit logging
oc patch apiserver cluster --type=merge -p '
spec:
  audit:
    profile: Default'

# Enable etcd encryption
oc patch apiserver cluster --type=merge -p '
spec:
  encryption:
    type: aescbc'
```

### 2. Backup and Restore

```bash
# Backup etcd
sudo -E /usr/local/bin/cluster-backup.sh /home/core/backup

# Backup projects
for project in $(oc get projects -o name | cut -d/ -f2); do
  oc get all,pvc,configmap,secret,ingress,route -n $project -o yaml > backup-$project.yaml
done

# Backup persistent volumes
oc get pv -o yaml > backup-pv.yaml
```

### 3. Upgrade Strategy

```bash
# Check available updates
oc adm upgrade

# Start upgrade
oc adm upgrade --to=4.12.10

# Monitor upgrade progress
oc get clusterversion -w

# Pause machine config updates
oc patch machineconfigpool worker --type merge --patch '{"spec":{"paused":true}}'
```

### 4. Capacity Planning

```yaml
# cluster-autoscaler.yaml
apiVersion: autoscaling.openshift.io/v1
kind: ClusterAutoscaler
metadata:
  name: default
spec:
  resourceLimits:
    maxNodesTotal: 24
    cores:
      min: 8
      max: 128
    memory:
      min: 32
      max: 512
  scaleDown:
    enabled: true
    delayAfterAdd: 10m
    delayAfterDelete: 5m
    delayAfterFailure: 3m
```

### 5. Multi-Tenancy

```bash
# Create project template
oc create -f - <<EOF
apiVersion: template.openshift.io/v1
kind: Template
metadata:
  name: project-request
  namespace: openshift-config
objects:
- apiVersion: project.openshift.io/v1
  kind: Project
  metadata:
    name: ${PROJECT_NAME}
    annotations:
      openshift.io/requester: ${PROJECT_REQUESTING_USER}
- apiVersion: rbac.authorization.k8s.io/v1
  kind: RoleBinding
  metadata:
    name: admin
    namespace: ${PROJECT_NAME}
  roleRef:
    apiGroup: rbac.authorization.k8s.io
    kind: ClusterRole
    name: admin
  subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: User
    name: ${PROJECT_ADMIN_USER}
- apiVersion: v1
  kind: LimitRange
  metadata:
    name: project-limits
    namespace: ${PROJECT_NAME}
  spec:
    limits:
    - max:
        cpu: 2
        memory: 4Gi
      min:
        cpu: 100m
        memory: 128Mi
      type: Container
- apiVersion: v1
  kind: ResourceQuota
  metadata:
    name: project-quota
    namespace: ${PROJECT_NAME}
  spec:
    hard:
      persistentvolumeclaims: "5"
      requests.storage: "20Gi"
      requests.cpu: "10"
      requests.memory: "20Gi"
parameters:
- name: PROJECT_NAME
- name: PROJECT_REQUESTING_USER
- name: PROJECT_ADMIN_USER
EOF
```

## Resources

### Official Documentation
- [OpenShift Documentation](https://docs.openshift.com/)
- [OpenShift Container Platform](https://www.redhat.com/en/technologies/cloud-computing/openshift/container-platform)
- [OpenShift API Reference](https://docs.openshift.com/container-platform/latest/rest_api/index.html)

### Tools and CLIs
- [oc CLI Reference](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)
- [OpenShift Web Console](https://docs.openshift.com/container-platform/latest/web_console/web-console.html)
- [OpenShift Developer CLI (odo)](https://odo.dev/)

### Learning Resources
- [OpenShift Interactive Learning Portal](https://learn.openshift.com/)
- [Red Hat Developer Program](https://developers.redhat.com/)
- [OpenShift Commons](https://commons.openshift.org/)
- [Katacoda OpenShift Courses](https://www.katacoda.com/openshift)

### Community and Support
- [OpenShift Blog](https://www.openshift.com/blog)
- [OpenShift YouTube Channel](https://www.youtube.com/user/rhopenshift)
- [Stack Overflow OpenShift Tag](https://stackoverflow.com/questions/tagged/openshift)
- [Red Hat Support Portal](https://access.redhat.com/)

### Ecosystem and Partners
- [OperatorHub.io](https://operatorhub.io/)
- [Red Hat Marketplace](https://marketplace.redhat.com/)
- [Red Hat Ecosystem Catalog](https://catalog.redhat.com/)
- [OpenShift Partner Solutions](https://www.openshift.com/partners)