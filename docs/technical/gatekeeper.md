# Gatekeeper

Gatekeeper is a Kubernetes admission controller that enforces policies using the Open Policy Agent (OPA) Rego language. It validates, mutates, and generates configuration for Kubernetes resources.

## Installation

### Helm Installation
```bash
# Add Gatekeeper Helm repository
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm repo update

# Install Gatekeeper
helm install gatekeeper gatekeeper/gatekeeper \
  --namespace gatekeeper-system \
  --create-namespace \
  --set replicas=3 \
  --set auditInterval=60 \
  --set constraintViolationsLimit=20

# Verify installation
kubectl get pods -n gatekeeper-system
kubectl get crd | grep gatekeeper
```

### Manifest Installation
```bash
# Install latest stable release
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.14/deploy/gatekeeper.yaml

# Or install specific version
VERSION=v3.14.0
kubectl apply -f https://github.com/open-policy-agent/gatekeeper/releases/download/${VERSION}/gatekeeper.yaml

# Check installation status
kubectl get pods -n gatekeeper-system
kubectl get validatingadmissionwebhooks
kubectl get mutatingadmissionwebhooks
```

### Development Installation
```bash
# Clone repository
git clone https://github.com/open-policy-agent/gatekeeper.git
cd gatekeeper

# Build and deploy
make docker-build IMG=gatekeeper:dev
make deploy IMG=gatekeeper:dev

# Run tests
make test
make test-e2e
```

## Basic Configuration

### Constraint Templates
```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        type: object
        properties:
          labels:
            type: array
            items:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg}] {
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required[_]
          not provided[missing]
          msg := sprintf("You must provide labels: %v", [missing])
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: must-have-owner
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
      - apiGroups: [""]
        kinds: ["Service", "ConfigMap"]
  parameters:
    labels: ["owner", "env"]
```

### Resource Requirements
```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8sresourcerequirements
spec:
  crd:
    spec:
      names:
        kind: K8sResourceRequirements
      validation:
        type: object
        properties:
          cpu:
            type: string
          memory:
            type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sresourcerequirements

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.resources.requests.cpu
          msg := "Container missing CPU requests"
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.resources.requests.memory
          msg := "Container missing memory requests"
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          cpu_limit := container.resources.limits.cpu
          cpu_request := container.resources.requests.cpu
          to_number(cpu_limit) < to_number(cpu_request)
          msg := "CPU limit must be greater than or equal to request"
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sResourceRequirements
metadata:
  name: pod-resources
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
      - apiGroups: ["apps"]
        kinds: ["Deployment", "ReplicaSet", "StatefulSet"]
  parameters:
    cpu: "100m"
    memory: "64Mi"
```

### Security Policies
```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8ssecuritycontext
spec:
  crd:
    spec:
      names:
        kind: K8sSecurityContext
      validation:
        type: object
        properties:
          runAsNonRoot:
            type: boolean
          readOnlyRootFilesystem:
            type: boolean
          allowPrivilegeEscalation:
            type: boolean
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8ssecuritycontext

        violation[{"msg": msg}] {
          input.parameters.runAsNonRoot
          container := input.review.object.spec.containers[_]
          container.securityContext.runAsUser == 0
          msg := "Container must not run as root user"
        }

        violation[{"msg": msg}] {
          input.parameters.readOnlyRootFilesystem
          container := input.review.object.spec.containers[_]
          not container.securityContext.readOnlyRootFilesystem
          msg := "Container must set readOnlyRootFilesystem to true"
        }

        violation[{"msg": msg}] {
          not input.parameters.allowPrivilegeEscalation
          container := input.review.object.spec.containers[_]
          container.securityContext.allowPrivilegeEscalation
          msg := "Container must not allow privilege escalation"
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sSecurityContext
metadata:
  name: security-context-required
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
      - apiGroups: ["apps"]
        kinds: ["Deployment", "DaemonSet", "StatefulSet"]
  parameters:
    runAsNonRoot: true
    readOnlyRootFilesystem: true
    allowPrivilegeEscalation: false
```

## Advanced Policy Examples

### Network Policies
```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequirenetworkpolicy
spec:
  crd:
    spec:
      names:
        kind: K8sRequireNetworkPolicy
      validation:
        type: object
        properties:
          exemptNamespaces:
            type: array
            items:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequirenetworkpolicy

        violation[{"msg": msg}] {
          input.review.kind.kind == "Namespace"
          namespace := input.review.object.metadata.name
          not is_exempt(namespace)
          not has_network_policy(namespace)
          msg := sprintf("Namespace '%v' must have a NetworkPolicy", [namespace])
        }

        is_exempt(namespace) {
          exempt := input.parameters.exemptNamespaces[_]
          namespace == exempt
        }

        has_network_policy(namespace) {
          data.inventory.namespace[namespace]["networking.k8s.io/v1"]["NetworkPolicy"][_]
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequireNetworkPolicy
metadata:
  name: require-network-policy
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Namespace"]
  parameters:
    exemptNamespaces: ["kube-system", "gatekeeper-system", "kube-public"]
```

### Image Security
```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8simagesecurity
spec:
  crd:
    spec:
      names:
        kind: K8sImageSecurity
      validation:
        type: object
        properties:
          allowedRegistries:
            type: array
            items:
              type: string
          blockedTags:
            type: array
            items:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8simagesecurity

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          image := container.image
          not starts_with_allowed_registry(image)
          msg := sprintf("Image '%v' is not from an allowed registry", [image])
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          image := container.image
          has_blocked_tag(image)
          msg := sprintf("Image '%v' uses a blocked tag", [image])
        }

        starts_with_allowed_registry(image) {
          allowed := input.parameters.allowedRegistries[_]
          startswith(image, allowed)
        }

        has_blocked_tag(image) {
          blocked := input.parameters.blockedTags[_]
          endswith(image, blocked)
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sImageSecurity
metadata:
  name: image-security-policy
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment", "DaemonSet", "StatefulSet"]
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    allowedRegistries:
      - "docker.io/library/"
      - "gcr.io/my-project/"
      - "my-registry.com/"
    blockedTags:
      - ":latest"
      - ":master"
      - ":main"
```

### Resource Quotas and Limits
```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8sresourcelimits
spec:
  crd:
    spec:
      names:
        kind: K8sResourceLimits
      validation:
        type: object
        properties:
          maxCpuRequest:
            type: string
          maxMemoryRequest:
            type: string
          maxCpuLimit:
            type: string
          maxMemoryLimit:
            type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sresourcelimits

        import future.keywords.in

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          cpu_request := container.resources.requests.cpu
          max_cpu := input.parameters.maxCpuRequest
          cpu_request_millicores := to_millicores(cpu_request)
          max_cpu_millicores := to_millicores(max_cpu)
          cpu_request_millicores > max_cpu_millicores
          msg := sprintf("CPU request %v exceeds maximum %v", [cpu_request, max_cpu])
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          memory_request := container.resources.requests.memory
          max_memory := input.parameters.maxMemoryRequest
          memory_request_bytes := to_bytes(memory_request)
          max_memory_bytes := to_bytes(max_memory)
          memory_request_bytes > max_memory_bytes
          msg := sprintf("Memory request %v exceeds maximum %v", [memory_request, max_memory])
        }

        to_millicores(cpu) = millicores {
          endswith(cpu, "m")
          millicores := to_number(trim_suffix(cpu, "m"))
        }

        to_millicores(cpu) = millicores {
          not endswith(cpu, "m")
          millicores := to_number(cpu) * 1000
        }

        to_bytes(memory) = bytes {
          endswith(memory, "Mi")
          bytes := to_number(trim_suffix(memory, "Mi")) * 1024 * 1024
        }

        to_bytes(memory) = bytes {
          endswith(memory, "Gi")
          bytes := to_number(trim_suffix(memory, "Gi")) * 1024 * 1024 * 1024
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sResourceLimits
metadata:
  name: resource-limits
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment", "StatefulSet"]
  parameters:
    maxCpuRequest: "2"
    maxMemoryRequest: "4Gi"
    maxCpuLimit: "4"
    maxMemoryLimit: "8Gi"
```

## Mutation Policies

### Assign Labels
```yaml
apiVersion: mutations.gatekeeper.sh/v1alpha1
kind: Assign
metadata:
  name: add-default-labels
spec:
  applyTo:
    - groups: ["apps"]
      kinds: ["Deployment"]
      versions: ["v1"]
  match:
    scope: Namespaced
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  location: "metadata.labels.managed-by"
  parameters:
    assign:
      value: "gatekeeper"
---
apiVersion: mutations.gatekeeper.sh/v1alpha1
kind: Assign
metadata:
  name: add-security-context
spec:
  applyTo:
    - groups: [""]
      kinds: ["Pod"]
      versions: ["v1"]
  match:
    scope: Namespaced
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  location: "spec.securityContext.runAsNonRoot"
  parameters:
    assign:
      value: true
```

### Modify Values
```yaml
apiVersion: mutations.gatekeeper.sh/v1alpha1
kind: ModifySet
metadata:
  name: add-toleration
spec:
  applyTo:
    - groups: ["apps"]
      kinds: ["Deployment"]
      versions: ["v1"]
  match:
    scope: Namespaced
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  location: "spec.template.spec.tolerations"
  parameters:
    operation: merge
    values:
      - key: "node-type"
        operator: "Equal"
        value: "compute"
        effect: "NoSchedule"
---
apiVersion: mutations.gatekeeper.sh/v1alpha1
kind: ModifySet
metadata:
  name: add-node-selector
spec:
  applyTo:
    - groups: ["apps"]
      kinds: ["Deployment"]
      versions: ["v1"]
  match:
    scope: Namespaced
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  location: "spec.template.spec.nodeSelector"
  parameters:
    operation: merge
    values:
      node-type: "compute"
      availability-zone: "us-west-2a"
```

### Assign If Not Present
```yaml
apiVersion: mutations.gatekeeper.sh/v1alpha1
kind: AssignMetadata
metadata:
  name: add-namespace-labels
spec:
  match:
    scope: Namespaced
    kinds:
      - apiGroups: [""]
        kinds: ["Namespace"]
  location: "metadata.labels"
  parameters:
    assign:
      team: "platform"
      managed-by: "gatekeeper"
      compliance: "required"
```

## Configuration and Sync

### Config Resource
```yaml
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
  namespace: gatekeeper-system
spec:
  match:
    - excludedNamespaces: ["kube-system", "gatekeeper-system"]
      processes: ["*"]
    - excludedNamespaces: ["kube-public"]
      processes: ["webhook"]
  validation:
    traces:
      - user:
          kind:
            group: "*"
            version: "*"
            kind: "*"
        kind:
          group: "*"
          version: "*"
          kind: "*"
  parameters:
    assign:
      externalData:
        provider: "external-data-provider"
        failurePolicy: "Fail"
  readiness:
    statsEnabled: true
```

### Sync Configuration
```yaml
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
  namespace: gatekeeper-system
spec:
  sync:
    syncOnly:
      - group: ""
        version: "v1"
        kind: "Namespace"
      - group: ""
        version: "v1"
        kind: "Pod"
      - group: "apps"
        version: "v1"
        kind: "Deployment"
      - group: "networking.k8s.io"
        version: "v1"
        kind: "NetworkPolicy"
  match:
    - excludedNamespaces: ["kube-system", "gatekeeper-system"]
      processes: ["*"]
  validation:
    traces:
      - user:
          kind:
            group: "*"
            version: "*"
            kind: "*"
        kind:
          group: "*"
          version: "*"
          kind: "*"
```

## Monitoring and Observability

### Prometheus Metrics
```yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: gatekeeper-metrics
  namespace: gatekeeper-system
spec:
  selector:
    matchLabels:
      control-plane: audit-controller
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: gatekeeper-alerts
  namespace: gatekeeper-system
spec:
  groups:
  - name: gatekeeper
    rules:
    - alert: GatekeeperConstraintViolations
      expr: increase(gatekeeper_violations_total[5m]) > 0
      for: 0m
      labels:
        severity: warning
      annotations:
        summary: "Gatekeeper constraint violations detected"
        description: "{{ $labels.instance }} has {{ $value }} constraint violations"
    
    - alert: GatekeeperAuditErrors
      expr: increase(gatekeeper_audit_errors_total[5m]) > 0
      for: 0m
      labels:
        severity: critical
      annotations:
        summary: "Gatekeeper audit errors detected"
        description: "{{ $labels.instance }} has {{ $value }} audit errors"
```

### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "Gatekeeper Policy Enforcement",
    "panels": [
      {
        "title": "Constraint Violations",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(gatekeeper_violations_total[5m])",
            "legendFormat": "{{constraint_kind}} - {{constraint_name}}"
          }
        ],
        "yAxes": [
          {
            "label": "Violations per second"
          }
        ]
      },
      {
        "title": "Webhook Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(gatekeeper_webhook_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(gatekeeper_webhook_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ]
      },
      {
        "title": "Audit Discoveries",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(gatekeeper_audit_last_run_discoveries_total[5m])",
            "legendFormat": "Discoveries"
          }
        ]
      }
    ]
  }
}
```

### Log Analysis
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-gatekeeper-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/pods/gatekeeper-system_gatekeeper-*/*/*.log
      pos_file /var/log/fluentd-gatekeeper.log.pos
      tag gatekeeper.*
      format json
      time_key time
      time_format %Y-%m-%dT%H:%M:%S.%NZ
    </source>
    
    <filter gatekeeper.**>
      @type parser
      key_name log
      reserve_data true
      <parse>
        @type json
      </parse>
    </filter>
    
    <filter gatekeeper.**>
      @type record_transformer
      <record>
        service gatekeeper
        component ${tag_parts[1]}
      </record>
    </filter>
    
    <match gatekeeper.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      index_name gatekeeper-logs
      type_name _doc
    </match>
```

## Testing and Validation

### Policy Testing Framework
```python
import yaml
import subprocess
import tempfile
import os

class GatekeeperTester:
    def __init__(self, kubeconfig=None):
        self.kubeconfig = kubeconfig
        
    def apply_constraint_template(self, template_yaml):
        """Apply constraint template"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(template_yaml, f)
            f.flush()
            
            cmd = ['kubectl', 'apply', '-f', f.name]
            if self.kubeconfig:
                cmd.extend(['--kubeconfig', self.kubeconfig])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            os.unlink(f.name)
            
            return result.returncode == 0, result.stdout, result.stderr
    
    def test_constraint(self, constraint_yaml, test_resource_yaml, expect_violation=True):
        """Test constraint against a resource"""
        # Apply constraint
        success, stdout, stderr = self.apply_constraint_template(constraint_yaml)
        if not success:
            return False, f"Failed to apply constraint: {stderr}"
        
        # Try to apply test resource
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_resource_yaml, f)
            f.flush()
            
            cmd = ['kubectl', 'apply', '-f', f.name, '--dry-run=server']
            if self.kubeconfig:
                cmd.extend(['--kubeconfig', self.kubeconfig])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            os.unlink(f.name)
            
            if expect_violation:
                return result.returncode != 0, result.stderr
            else:
                return result.returncode == 0, result.stdout
    
    def get_constraint_violations(self, constraint_name):
        """Get current violations for a constraint"""
        cmd = ['kubectl', 'get', 'constraint', constraint_name, '-o', 'json']
        if self.kubeconfig:
            cmd.extend(['--kubeconfig', self.kubeconfig])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            import json
            constraint = json.loads(result.stdout)
            return constraint.get('status', {}).get('violations', [])
        return []
    
    def run_policy_test_suite(self, test_cases):
        """Run a suite of policy tests"""
        results = []
        
        for test_case in test_cases:
            name = test_case['name']
            constraint = test_case['constraint']
            resource = test_case['resource']
            expect_violation = test_case.get('expect_violation', True)
            
            success, message = self.test_constraint(constraint, resource, expect_violation)
            results.append({
                'name': name,
                'success': success,
                'message': message,
                'expected_violation': expect_violation
            })
        
        return results

# Usage
tester = GatekeeperTester()

# Test required labels policy
test_cases = [
    {
        'name': 'Deployment without required labels should be rejected',
        'constraint': {
            'apiVersion': 'constraints.gatekeeper.sh/v1beta1',
            'kind': 'K8sRequiredLabels',
            'metadata': {'name': 'test-labels'},
            'spec': {
                'match': {
                    'kinds': [{'apiGroups': ['apps'], 'kinds': ['Deployment']}]
                },
                'parameters': {'labels': ['owner', 'env']}
            }
        },
        'resource': {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {'name': 'test-deployment', 'namespace': 'default'},
            'spec': {
                'selector': {'matchLabels': {'app': 'test'}},
                'template': {
                    'metadata': {'labels': {'app': 'test'}},
                    'spec': {'containers': [{'name': 'test', 'image': 'nginx'}]}
                }
            }
        },
        'expect_violation': True
    }
]

results = tester.run_policy_test_suite(test_cases)
for result in results:
    print(f"Test: {result['name']}")
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print()
```

### Dry Run Validation
```bash
#!/bin/bash
# validate-policies.sh

set -e

NAMESPACE=${1:-default}
POLICY_DIR=${2:-./policies}

echo "Validating Gatekeeper policies..."

# Function to test policy
test_policy() {
    local policy_file=$1
    local test_file=$2
    local expect_fail=${3:-true}
    
    echo "Testing policy: $(basename $policy_file)"
    
    # Apply constraint template and constraint
    kubectl apply -f "$policy_file"
    
    # Wait for constraint to be ready
    sleep 5
    
    # Test with sample resource
    if kubectl apply -f "$test_file" --dry-run=server &>/dev/null; then
        if [ "$expect_fail" = "true" ]; then
            echo "  ❌ Expected violation but resource was accepted"
            return 1
        else
            echo "  ✅ Resource accepted as expected"
            return 0
        fi
    else
        if [ "$expect_fail" = "true" ]; then
            echo "  ✅ Resource rejected as expected"
            return 0
        else
            echo "  ❌ Expected acceptance but resource was rejected"
            return 1
        fi
    fi
}

# Test each policy
for policy_file in "$POLICY_DIR"/*.yaml; do
    if [ -f "$policy_file" ]; then
        test_dir="${policy_file%.yaml}_tests"
        if [ -d "$test_dir" ]; then
            for test_file in "$test_dir"/*.yaml; do
                test_policy "$policy_file" "$test_file"
            done
        fi
    fi
done

echo "Policy validation completed!"
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Gatekeeper Policy Validation

on:
  push:
    paths:
      - 'policies/**'
  pull_request:
    paths:
      - 'policies/**'

jobs:
  validate-policies:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Setup kubectl
      uses: azure/setup-kubectl@v3
    
    - name: Create kind cluster
      uses: helm/kind-action@v1.4.0
      with:
        cluster_name: policy-test
    
    - name: Install Gatekeeper
      run: |
        kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.14/deploy/gatekeeper.yaml
        kubectl wait --for=condition=Ready pods --all -n gatekeeper-system --timeout=300s
    
    - name: Validate Constraint Templates
      run: |
        for template in policies/templates/*.yaml; do
          echo "Validating $template"
          kubectl apply -f "$template" --dry-run=server
        done
    
    - name: Test Policies
      run: |
        # Apply all constraint templates
        kubectl apply -f policies/templates/
        
        # Apply all constraints
        kubectl apply -f policies/constraints/
        
        # Wait for constraints to be ready
        sleep 30
        
        # Run tests
        ./scripts/test-policies.sh
    
    - name: Check for violations
      run: |
        violations=$(kubectl get constraints -o json | jq '.items[] | select(.status.violations != null) | .status.violations | length' | paste -sd+ - | bc)
        if [ "$violations" -gt 0 ]; then
          echo "Found $violations policy violations"
          kubectl get constraints -o yaml
          exit 1
        fi
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    environment {
        KUBECONFIG = credentials('kubeconfig')
        CLUSTER_NAME = 'policy-test'
    }
    
    stages {
        stage('Setup Test Environment') {
            steps {
                script {
                    sh '''
                        # Create test cluster
                        kind create cluster --name $CLUSTER_NAME
                        
                        # Install Gatekeeper
                        kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.14/deploy/gatekeeper.yaml
                        kubectl wait --for=condition=Ready pods --all -n gatekeeper-system --timeout=300s
                    '''
                }
            }
        }
        
        stage('Validate Templates') {
            steps {
                script {
                    sh '''
                        echo "Validating constraint templates..."
                        for template in policies/templates/*.yaml; do
                            echo "Validating $template"
                            kubectl apply -f "$template" --dry-run=server
                        done
                    '''
                }
            }
        }
        
        stage('Deploy Policies') {
            steps {
                script {
                    sh '''
                        # Apply constraint templates
                        kubectl apply -f policies/templates/
                        
                        # Apply constraints
                        kubectl apply -f policies/constraints/
                        
                        # Wait for readiness
                        sleep 30
                        
                        # Verify constraint status
                        kubectl get constraints
                    '''
                }
            }
        }
        
        stage('Test Policies') {
            steps {
                script {
                    sh '''
                        # Run policy tests
                        ./scripts/test-policies.sh
                        
                        # Check for any violations
                        violations=$(kubectl get constraints -o json | jq '.items[] | select(.status.violations != null) | .status.violations | length' | paste -sd+ - | bc)
                        if [ "$violations" -gt 0 ]; then
                            echo "Found $violations policy violations"
                            kubectl get constraints -o yaml
                            exit 1
                        fi
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                sh 'kind delete cluster --name $CLUSTER_NAME || true'
            }
        }
        success {
            echo 'Policy validation passed!'
        }
        failure {
            echo 'Policy validation failed!'
        }
    }
}
```

## Best Practices and Troubleshooting

### Performance Optimization
```yaml
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
  namespace: gatekeeper-system
spec:
  # Exclude system namespaces from validation
  match:
    - excludedNamespaces: 
        - "kube-system"
        - "gatekeeper-system" 
        - "kube-public"
        - "kube-node-lease"
      processes: ["*"]
  
  # Optimize sync resources
  sync:
    syncOnly:
      - group: ""
        version: "v1"
        kind: "Pod"
      - group: "apps"
        version: "v1"
        kind: "Deployment"
      - group: ""
        version: "v1"
        kind: "Service"
  
  # Enable metrics for monitoring
  readiness:
    statsEnabled: true
  
  # Configure audit frequency
  parameters:
    audit:
      auditInterval: 60
      constraintViolationsLimit: 100
```

### Debugging Policies
```bash
#!/bin/bash
# debug-gatekeeper.sh

# Check Gatekeeper status
echo "=== Gatekeeper System Status ==="
kubectl get pods -n gatekeeper-system
kubectl get validatingadmissionwebhooks
kubectl get mutatingadmissionwebhooks

# Check constraint templates
echo "=== Constraint Templates ==="
kubectl get constrainttemplates
kubectl describe constrainttemplates

# Check constraints
echo "=== Constraints ==="
kubectl get constraints --all-namespaces
kubectl describe constraints

# Check for violations
echo "=== Current Violations ==="
kubectl get constraints -o json | jq '.items[] | select(.status.violations != null) | {name: .metadata.name, violations: .status.violations}'

# Check webhook logs
echo "=== Webhook Logs ==="
kubectl logs -n gatekeeper-system -l control-plane=controller-manager --tail=50

# Check audit logs
echo "=== Audit Logs ==="
kubectl logs -n gatekeeper-system -l control-plane=audit-controller --tail=50

# Test webhook connectivity
echo "=== Webhook Connectivity ==="
kubectl get validatingadmissionwebhooks -o json | jq '.items[] | select(.metadata.name | contains("gatekeeper")) | .webhooks[].clientConfig'
```

### Common Issues and Solutions
```yaml
# Issue: Constraint not enforcing
# Solution: Check constraint status
apiVersion: v1
kind: ConfigMap
metadata:
  name: troubleshooting-guide
data:
  common-issues.md: |
    # Gatekeeper Troubleshooting Guide
    
    ## Constraint Not Enforcing
    ```bash
    # Check constraint status
    kubectl describe constraint <constraint-name>
    
    # Check if resources are synced
    kubectl get config config -n gatekeeper-system -o yaml
    
    # Verify webhook is running
    kubectl get validatingadmissionwebhooks
    ```
    
    ## Performance Issues
    ```yaml
    # Reduce sync scope
    spec:
      sync:
        syncOnly:
          - group: "apps"
            version: "v1"
            kind: "Deployment"
    
    # Exclude more namespaces
    spec:
      match:
        - excludedNamespaces: ["kube-system", "monitoring"]
          processes: ["*"]
    ```
    
    ## Debugging Rego Policies
    ```bash
    # Test Rego online
    # Use OPA Playground: https://play.openpolicyagent.org/
    
    # Check constraint template validation
    kubectl apply -f constraint-template.yaml --dry-run=server
    
    # View webhook decision logs
    kubectl logs -n gatekeeper-system -l control-plane=controller-manager | grep admission
    ```
```

## Resources

- [Gatekeeper Documentation](https://open-policy-agent.github.io/gatekeeper/)
- [GitHub Repository](https://github.com/open-policy-agent/gatekeeper)
- [OPA Rego Language](https://www.openpolicyagent.org/docs/latest/policy-language/)
- [Policy Library](https://github.com/open-policy-agent/gatekeeper-library)
- [Constraint Templates](https://open-policy-agent.github.io/gatekeeper/website/docs/constrainttemplates)
- [Mutation](https://open-policy-agent.github.io/gatekeeper/website/docs/mutation)
- [Metrics and Monitoring](https://open-policy-agent.github.io/gatekeeper/website/docs/metrics)
- [Best Practices](https://open-policy-agent.github.io/gatekeeper/website/docs/debug)
- [Community Support](https://github.com/open-policy-agent/gatekeeper/discussions)
- [OPA Slack Channel](https://openpolicyagent.slack.com/)