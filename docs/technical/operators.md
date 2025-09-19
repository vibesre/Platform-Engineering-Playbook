# Kubernetes Operators and Operator Framework

## Overview

Kubernetes Operators are application-specific controllers that extend the Kubernetes API to create, configure, and manage instances of complex applications. They encode operational knowledge and automate tasks that would typically require human intervention, following Kubernetes principles and using Custom Resource Definitions (CRDs).

## Core Concepts

### What is an Operator?

An Operator is a method of packaging, deploying, and managing a Kubernetes application. It consists of:
- **Custom Resource Definitions (CRDs)**: Extend Kubernetes API with new resource types
- **Controller**: Watches for changes to custom resources and takes action
- **Operational Knowledge**: Encoded best practices for managing the application

### Operator Pattern

The Operator pattern combines custom resources and custom controllers:
1. Define custom resources that represent your application
2. Implement controllers that watch these resources
3. Controllers reconcile actual state with desired state
4. Encode operational knowledge in the controller logic

## Operator Capability Levels

The Operator Framework defines five capability levels:

1. **Basic Install**: Automated application provisioning and configuration
2. **Seamless Upgrades**: Patch and minor version upgrades
3. **Full Lifecycle**: App lifecycle management, storage lifecycle, backup/recovery
4. **Deep Insights**: Metrics, alerts, log processing, workload analysis
5. **Auto Pilot**: Horizontal/vertical scaling, auto-config tuning, abnormality detection

## Building Operators

### Using Kubebuilder

```bash
# Install kubebuilder
curl -L -o kubebuilder https://go.kubebuilder.io/dl/latest/$(go env GOOS)/$(go env GOARCH)
chmod +x kubebuilder && mv kubebuilder /usr/local/bin/

# Create a new project
mkdir myapp-operator && cd myapp-operator
kubebuilder init --domain example.com --repo github.com/example/myapp-operator

# Create API
kubebuilder create api --group apps --version v1alpha1 --kind MyApp
```

### Basic Operator Structure

```go
// api/v1alpha1/myapp_types.go
package v1alpha1

import (
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// MyAppSpec defines the desired state of MyApp
type MyAppSpec struct {
    // Size is the number of replicas
    Size int32 `json:"size"`
    
    // Version is the application version
    Version string `json:"version"`
    
    // Resources defines resource requirements
    Resources ResourceRequirements `json:"resources,omitempty"`
}

// MyAppStatus defines the observed state of MyApp
type MyAppStatus struct {
    // Conditions represent the latest available observations
    Conditions []metav1.Condition `json:"conditions,omitempty"`
    
    // ReadyReplicas is the number of ready replicas
    ReadyReplicas int32 `json:"readyReplicas,omitempty"`
    
    // Phase represents the current phase
    Phase string `json:"phase,omitempty"`
}

//+kubebuilder:object:root=true
//+kubebuilder:subresource:status
//+kubebuilder:subresource:scale:specpath=.spec.size,statuspath=.status.readyReplicas

// MyApp is the Schema for the myapps API
type MyApp struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   MyAppSpec   `json:"spec,omitempty"`
    Status MyAppStatus `json:"status,omitempty"`
}
```

### Controller Implementation

```go
// controllers/myapp_controller.go
package controllers

import (
    "context"
    "fmt"

    "github.com/go-logr/logr"
    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    "k8s.io/apimachinery/pkg/api/errors"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"

    appsv1alpha1 "github.com/example/myapp-operator/api/v1alpha1"
)

// MyAppReconciler reconciles a MyApp object
type MyAppReconciler struct {
    client.Client
    Log    logr.Logger
    Scheme *runtime.Scheme
}

//+kubebuilder:rbac:groups=apps.example.com,resources=myapps,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=apps.example.com,resources=myapps/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=apps.example.com,resources=myapps/finalizers,verbs=update
//+kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete

func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := r.Log.WithValues("myapp", req.NamespacedName)

    // Fetch the MyApp instance
    myapp := &appsv1alpha1.MyApp{}
    err := r.Get(ctx, req.NamespacedName, myapp)
    if err != nil {
        if errors.IsNotFound(err) {
            log.Info("MyApp resource not found. Ignoring since object must be deleted")
            return ctrl.Result{}, nil
        }
        log.Error(err, "Failed to get MyApp")
        return ctrl.Result{}, err
    }

    // Check if the deployment already exists
    found := &appsv1.Deployment{}
    err = r.Get(ctx, types.NamespacedName{Name: myapp.Name, Namespace: myapp.Namespace}, found)
    if err != nil && errors.IsNotFound(err) {
        // Define a new deployment
        dep := r.deploymentForMyApp(myapp)
        log.Info("Creating a new Deployment", "Deployment.Namespace", dep.Namespace, "Deployment.Name", dep.Name)
        err = r.Create(ctx, dep)
        if err != nil {
            log.Error(err, "Failed to create new Deployment", "Deployment.Namespace", dep.Namespace, "Deployment.Name", dep.Name)
            return ctrl.Result{}, err
        }
        return ctrl.Result{Requeue: true}, nil
    } else if err != nil {
        log.Error(err, "Failed to get Deployment")
        return ctrl.Result{}, err
    }

    // Ensure the deployment size matches the spec
    size := myapp.Spec.Size
    if *found.Spec.Replicas != size {
        found.Spec.Replicas = &size
        err = r.Update(ctx, found)
        if err != nil {
            log.Error(err, "Failed to update Deployment", "Deployment.Namespace", found.Namespace, "Deployment.Name", found.Name)
            return ctrl.Result{}, err
        }
        return ctrl.Result{Requeue: true}, nil
    }

    // Update the MyApp status
    myapp.Status.ReadyReplicas = found.Status.ReadyReplicas
    myapp.Status.Phase = "Running"
    err = r.Status().Update(ctx, myapp)
    if err != nil {
        log.Error(err, "Failed to update MyApp status")
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil
}

func (r *MyAppReconciler) deploymentForMyApp(m *appsv1alpha1.MyApp) *appsv1.Deployment {
    ls := labelsForMyApp(m.Name)
    replicas := m.Spec.Size

    dep := &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name:      m.Name,
            Namespace: m.Namespace,
        },
        Spec: appsv1.DeploymentSpec{
            Replicas: &replicas,
            Selector: &metav1.LabelSelector{
                MatchLabels: ls,
            },
            Template: corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: ls,
                },
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{{
                        Image:   fmt.Sprintf("myapp:%s", m.Spec.Version),
                        Name:    "myapp",
                        Command: []string{"myapp", "start"},
                        Ports: []corev1.ContainerPort{{
                            ContainerPort: 8080,
                            Name:          "http",
                        }},
                    }},
                },
            },
        },
    }

    // Set MyApp instance as the owner and controller
    controllerutil.SetControllerReference(m, dep, r.Scheme)
    return dep
}

func labelsForMyApp(name string) map[string]string {
    return map[string]string{"app": "myapp", "myapp_cr": name}
}

func (r *MyAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&appsv1alpha1.MyApp{}).
        Owns(&appsv1.Deployment{}).
        Complete(r)
}
```

## Using Operator SDK

### Installation and Project Setup

```bash
# Install Operator SDK
curl -LO https://github.com/operator-framework/operator-sdk/releases/latest/download/operator-sdk_linux_amd64
chmod +x operator-sdk_linux_amd64
sudo mv operator-sdk_linux_amd64 /usr/local/bin/operator-sdk

# Create new operator
operator-sdk init --domain example.com --repo github.com/example/myapp-operator
operator-sdk create api --group cache --version v1alpha1 --kind Redis --resource --controller
```

### Ansible-based Operator

```yaml
# roles/redis/tasks/main.yml
---
- name: Create Redis Deployment
  k8s:
    definition:
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: '{{ ansible_operator_meta.name }}-redis'
        namespace: '{{ ansible_operator_meta.namespace }}'
      spec:
        replicas: "{{ size }}"
        selector:
          matchLabels:
            app: redis
        template:
          metadata:
            labels:
              app: redis
          spec:
            containers:
            - name: redis
              image: "redis:{{ redis_version | default('6-alpine') }}"
              ports:
              - containerPort: 6379

- name: Create Redis Service
  k8s:
    definition:
      apiVersion: v1
      kind: Service
      metadata:
        name: '{{ ansible_operator_meta.name }}-redis'
        namespace: '{{ ansible_operator_meta.namespace }}'
      spec:
        selector:
          app: redis
        ports:
        - protocol: TCP
          port: 6379
          targetPort: 6379

# watches.yaml
---
- version: v1alpha1
  group: cache.example.com
  kind: Redis
  role: redis
  reconcilePeriod: 30s
  manageStatus: true
  watchDependentResources: true
  watchClusterScopedResources: false
```

### Helm-based Operator

```yaml
# watches.yaml
---
- version: v1alpha1
  group: charts.example.com
  kind: Nginx
  chart: helm-charts/nginx
  watchDependentResources: true
  overrideValues:
    image.repository: nginx
    image.tag: $RELATED_IMAGE_NGINX
    service.type: ClusterIP
    service.port: 8080
```

## Operator Lifecycle Manager (OLM)

### ClusterServiceVersion (CSV)

```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: ClusterServiceVersion
metadata:
  name: myapp-operator.v0.1.0
  namespace: operators
spec:
  displayName: MyApp Operator
  description: Manages MyApp instances
  maturity: alpha
  version: 0.1.0
  replaces: myapp-operator.v0.0.9
  
  installModes:
  - supported: true
    type: OwnNamespace
  - supported: true
    type: SingleNamespace
  - supported: false
    type: MultiNamespace
  - supported: true
    type: AllNamespaces
  
  customresourcedefinitions:
    owned:
    - name: myapps.apps.example.com
      version: v1alpha1
      kind: MyApp
      displayName: MyApp Application
      description: Represents a MyApp application
  
  install:
    strategy: deployment
    spec:
      permissions:
      - serviceAccountName: myapp-operator
        rules:
        - apiGroups: [""]
          resources: ["pods", "services", "endpoints", "persistentvolumeclaims", "events", "configmaps", "secrets"]
          verbs: ["*"]
        - apiGroups: ["apps"]
          resources: ["deployments", "replicasets", "statefulsets"]
          verbs: ["*"]
      deployments:
      - name: myapp-operator
        spec:
          replicas: 1
          selector:
            matchLabels:
              name: myapp-operator
          template:
            metadata:
              labels:
                name: myapp-operator
            spec:
              serviceAccountName: myapp-operator
              containers:
              - name: myapp-operator
                image: example.com/myapp-operator:v0.1.0
                env:
                - name: WATCH_NAMESPACE
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.annotations['olm.targetNamespaces']
```

### Operator Bundle

```dockerfile
# bundle.Dockerfile
FROM scratch

# Core bundle labels.
LABEL operators.operatorframework.io.bundle.mediatype.v1=registry+v1
LABEL operators.operatorframework.io.bundle.manifests.v1=manifests/
LABEL operators.operatorframework.io.bundle.metadata.v1=metadata/
LABEL operators.operatorframework.io.bundle.package.v1=myapp-operator
LABEL operators.operatorframework.io.bundle.channels.v1=alpha
LABEL operators.operatorframework.io.bundle.channel.default.v1=alpha

# Copy files to locations specified by labels.
COPY manifests /manifests/
COPY metadata /metadata/
```

## Production-Ready Operators

### 1. High Availability Implementation

```go
// High availability with leader election
func main() {
    mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{
        Scheme:             scheme,
        MetricsBindAddress: metricsAddr,
        Port:               9443,
        LeaderElection:     true,
        LeaderElectionID:   "myapp-operator-leader-election",
        LeaderElectionNamespace: "myapp-operator-system",
    })
}
```

### 2. Status Management

```go
type MyAppStatus struct {
    // Phase represents the current lifecycle phase
    Phase MyAppPhase `json:"phase,omitempty"`
    
    // ObservedGeneration reflects the generation of the most recently observed MyApp
    ObservedGeneration int64 `json:"observedGeneration,omitempty"`
    
    // Conditions represent the latest available observations
    Conditions []metav1.Condition `json:"conditions,omitempty"`
    
    // LastBackup contains information about the last backup
    LastBackup *BackupInfo `json:"lastBackup,omitempty"`
    
    // Endpoints lists the service endpoints
    Endpoints []string `json:"endpoints,omitempty"`
}

// Update status with conditions
func (r *MyAppReconciler) updateStatus(ctx context.Context, myapp *v1alpha1.MyApp, condition metav1.Condition) error {
    myapp.Status.ObservedGeneration = myapp.Generation
    meta.SetStatusCondition(&myapp.Status.Conditions, condition)
    return r.Status().Update(ctx, myapp)
}
```

### 3. Webhook Implementation

```go
// Validating webhook
func (r *MyApp) ValidateCreate() error {
    myapplog.Info("validate create", "name", r.Name)
    
    if r.Spec.Size < 1 {
        return errors.New("size must be greater than 0")
    }
    
    if !isValidVersion(r.Spec.Version) {
        return fmt.Errorf("invalid version: %s", r.Spec.Version)
    }
    
    return nil
}

// Mutating webhook
func (r *MyApp) Default() {
    myapplog.Info("default", "name", r.Name)
    
    if r.Spec.Size == 0 {
        r.Spec.Size = 3
    }
    
    if r.Spec.Version == "" {
        r.Spec.Version = "latest"
    }
}
```

### 4. Monitoring and Metrics

```go
import (
    "github.com/prometheus/client_golang/prometheus"
    "sigs.k8s.io/controller-runtime/pkg/metrics"
)

var (
    reconcileCounter = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "myapp_operator_reconcile_total",
            Help: "Total number of reconciliations per controller",
        },
        []string{"controller", "result"},
    )
    
    instanceGauge = prometheus.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "myapp_operator_managed_instances",
            Help: "Number of managed instances",
        },
        []string{"namespace", "phase"},
    )
)

func init() {
    metrics.Registry.MustRegister(reconcileCounter, instanceGauge)
}
```

## Real-World Operator Examples

### 1. Database Operator

```yaml
# PostgreSQL cluster custom resource
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: postgres-cluster
spec:
  instances: 3
  
  postgresql:
    parameters:
      max_connections: "200"
      shared_buffers: "256MB"
      effective_cache_size: "1GB"
  
  bootstrap:
    initdb:
      database: myapp
      owner: myapp
      secret:
        name: myapp-credentials
  
  storage:
    size: 10Gi
    storageClass: fast-ssd
  
  monitoring:
    enabled: true
    customQueriesConfigMap:
      name: postgresql-metrics
      key: custom-queries.yaml
  
  backup:
    enabled: true
    retentionPolicy: "30d"
    target: "s3://backup-bucket/postgres"
    schedule: "0 2 * * *"
```

### 2. Kafka Operator (Strimzi)

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
spec:
  kafka:
    version: 3.2.0
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
      - name: external
        port: 9094
        type: loadbalancer
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      log.retention.hours: 168
    storage:
      type: persistent-claim
      size: 100Gi
      class: fast-ssd
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 10Gi
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

### 3. Service Mesh Operator (Istio)

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: control-plane
spec:
  profile: production
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 1000m
            memory: 1Gi
        hpaSpec:
          minReplicas: 2
          maxReplicas: 5
    ingressGateways:
    - name: istio-ingressgateway
      enabled: true
      k8s:
        service:
          type: LoadBalancer
    egressGateways:
    - name: istio-egressgateway
      enabled: true
  meshConfig:
    defaultConfig:
      proxyStatsMatcher:
        inclusionRegexps:
        - ".*outlier_detection.*"
        - ".*circuit_breakers.*"
      holdApplicationUntilProxyStarts: true
    accessLogFile: /dev/stdout
  values:
    global:
      mtls:
        enabled: true
```

## Best Practices

### 1. Resource Management

```go
// Set resource ownership
func (r *MyAppReconciler) createResource(ctx context.Context, myapp *v1alpha1.MyApp, obj client.Object) error {
    if err := controllerutil.SetControllerReference(myapp, obj, r.Scheme); err != nil {
        return err
    }
    return r.Create(ctx, obj)
}

// Garbage collection with finalizers
const myappFinalizer = "myapp.example.com/finalizer"

func (r *MyAppReconciler) handleFinalizer(ctx context.Context, myapp *v1alpha1.MyApp) error {
    if myapp.ObjectMeta.DeletionTimestamp.IsZero() {
        if !containsString(myapp.GetFinalizers(), myappFinalizer) {
            controllerutil.AddFinalizer(myapp, myappFinalizer)
            return r.Update(ctx, myapp)
        }
    } else {
        if containsString(myapp.GetFinalizers(), myappFinalizer) {
            // Perform cleanup
            if err := r.cleanupExternalResources(myapp); err != nil {
                return err
            }
            controllerutil.RemoveFinalizer(myapp, myappFinalizer)
            return r.Update(ctx, myapp)
        }
    }
    return nil
}
```

### 2. Testing Operators

```go
// Unit test example
func TestMyAppReconciler(t *testing.T) {
    g := NewGomegaWithT(t)
    
    myapp := &v1alpha1.MyApp{
        ObjectMeta: metav1.ObjectMeta{
            Name:      "test-myapp",
            Namespace: "default",
        },
        Spec: v1alpha1.MyAppSpec{
            Size:    3,
            Version: "1.0.0",
        },
    }
    
    // Create fake client
    objs := []runtime.Object{myapp}
    cl := fake.NewClientBuilder().WithRuntimeObjects(objs...).Build()
    
    r := &MyAppReconciler{
        Client: cl,
        Scheme: scheme.Scheme,
    }
    
    req := reconcile.Request{
        NamespacedName: types.NamespacedName{
            Name:      myapp.Name,
            Namespace: myapp.Namespace,
        },
    }
    
    res, err := r.Reconcile(context.TODO(), req)
    g.Expect(err).NotTo(HaveOccurred())
    g.Expect(res.Requeue).To(BeTrue())
}
```

### 3. Operator Upgrades

```yaml
# Handling CRD versioning
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: myapps.apps.example.com
spec:
  versions:
  - name: v1alpha1
    served: true
    storage: false
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              size:
                type: integer
  - name: v1beta1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              replicas:  # renamed from 'size'
                type: integer
  conversion:
    strategy: Webhook
    webhook:
      clientConfig:
        service:
          name: myapp-webhook-service
          namespace: myapp-system
          path: /convert
```

## Troubleshooting

### Common Issues

1. **RBAC Permissions**
```bash
# Check operator permissions
kubectl auth can-i --list --as system:serviceaccount:myapp-system:myapp-controller-manager

# Create necessary RBAC
kubectl create clusterrolebinding myapp-admin --clusterrole=cluster-admin --serviceaccount=myapp-system:myapp-controller-manager
```

2. **Webhook Certificate Issues**
```bash
# Check webhook configuration
kubectl get validatingwebhookconfigurations
kubectl get mutatingwebhookconfigurations

# Verify certificate
kubectl get secret webhook-server-cert -n myapp-system -o yaml
```

3. **Resource Conflicts**
```go
// Handle resource conflicts with retry
if err := r.Update(ctx, resource); err != nil {
    if errors.IsConflict(err) {
        // Re-fetch and retry
        return ctrl.Result{Requeue: true}, nil
    }
    return ctrl.Result{}, err
}
```

### Debugging Tools

```bash
# Operator logs
kubectl logs -n myapp-system deployment/myapp-controller-manager -c manager

# Check operator metrics
kubectl port-forward -n myapp-system deployment/myapp-controller-manager 8080:8080
curl http://localhost:8080/metrics

# Trace reconciliation
kubectl annotate myapp/example debug.trace=true

# Check events
kubectl get events --field-selector involvedObject.name=example
```

## Conclusion

Kubernetes Operators provide a powerful pattern for managing complex applications on Kubernetes. By encoding operational knowledge into software, they enable consistent, automated management of stateful applications, reducing operational overhead and improving reliability. The Operator Framework and its tools make it easier to build, test, and distribute operators, while following best practices ensures production-ready implementations.