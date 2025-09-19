# Kyverno

Kyverno is a policy engine designed for Kubernetes that manages security, governance, and compliance through declarative policies written in YAML without requiring a new policy language.

## Installation

### Helm Installation
```bash
# Add Kyverno Helm repository
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

# Install Kyverno
helm install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace \
  --set replicaCount=3 \
  --set serviceAccount.create=true \
  --set webhookConfiguration.replicas=3

# Verify installation
kubectl get pods -n kyverno
kubectl get crd | grep kyverno
```

### Manifest Installation
```bash
# Install latest stable release
kubectl apply -f https://github.com/kyverno/kyverno/releases/latest/download/install.yaml

# Or install specific version
VERSION=v1.10.0
kubectl apply -f https://github.com/kyverno/kyverno/releases/download/${VERSION}/install.yaml

# Check installation status
kubectl get pods -n kyverno
kubectl get validatingadmissionwebhooks
kubectl get mutatingadmissionwebhooks
```

### High Availability Installation
```bash
# Install Kyverno in HA mode
helm install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace \
  --set replicaCount=3 \
  --set initContainer.resources.limits.memory=512Mi \
  --set resources.limits.memory=1Gi \
  --set webhookConfiguration.replicas=3 \
  --set backgroundController.resources.limits.memory=1Gi
```

## Basic Policies

### Validation Policies
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: check-team-label
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Service
          - Deployment
    validate:
      message: "Resource must have 'team' label"
      pattern:
        metadata:
          labels:
            team: "?*"
  - name: check-environment-label
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Service
          - Deployment
    validate:
      message: "Resource must have 'environment' label with valid value"
      pattern:
        metadata:
          labels:
            environment: "dev|staging|prod"
---
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-root-user
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: check-containers
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
          - StatefulSet
          - DaemonSet
    validate:
      message: "Containers must not run as root"
      anyPattern:
      - spec:
          securityContext:
            runAsNonRoot: true
      - spec:
          securityContext:
            runAsUser: ">0"
      - spec:
          containers:
          - securityContext:
              runAsNonRoot: true
      - spec:
          containers:
          - securityContext:
              runAsUser: ">0"
```

### Mutation Policies
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-resources
spec:
  background: false
  rules:
  - name: add-default-requests
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
          - StatefulSet
    mutate:
      patchStrategicMerge:
        spec:
          containers:
          - (name): "*"
            resources:
              requests:
                +(memory): "128Mi"
                +(cpu): "100m"
              limits:
                +(memory): "256Mi"
                +(cpu): "200m"
---
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-security-context
spec:
  background: false
  rules:
  - name: add-safe-defaults
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
          - StatefulSet
    mutate:
      patchStrategicMerge:
        spec:
          securityContext:
            +(runAsNonRoot): true
            +(fsGroup): 2000
          containers:
          - (name): "*"
            securityContext:
              +(allowPrivilegeEscalation): false
              +(capabilities):
                drop:
                - ALL
              +(readOnlyRootFilesystem): true
              +(runAsNonRoot): true
              +(runAsUser): 1000
```

### Generation Policies
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-default-networkpolicy
spec:
  background: true
  rules:
  - name: default-deny-ingress
    match:
      any:
      - resources:
          kinds:
          - Namespace
    exclude:
      any:
      - resources:
          namespaces:
          - kube-system
          - kyverno
          - kube-public
    generate:
      kind: NetworkPolicy
      name: default-deny-ingress
      namespace: "{{request.object.metadata.name}}"
      synchronize: true
      data:
        spec:
          podSelector: {}
          policyTypes:
          - Ingress
---
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-secret
spec:
  background: false
  rules:
  - name: create-default-secret
    match:
      any:
      - resources:
          kinds:
          - Namespace
    exclude:
      any:
      - resources:
          namespaces:
          - kube-system
          - kyverno
    generate:
      kind: Secret
      name: default-secret
      namespace: "{{request.object.metadata.name}}"
      synchronize: true
      data:
        metadata:
          labels:
            managed-by: kyverno
        type: Opaque
        data:
          key: dmFsdWU= # base64 encoded "value"
```

## Advanced Policy Examples

### Image Security
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: image-security
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: check-image-registry
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
          - StatefulSet
          - DaemonSet
    validate:
      message: "Images must be from approved registries"
      pattern:
        spec:
          containers:
          - image: "registry.company.com/*|gcr.io/my-project/*|docker.io/library/*"
  - name: disallow-latest-tag
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
          - StatefulSet
    validate:
      message: "Latest tag is not allowed"
      pattern:
        spec:
          containers:
          - image: "!*:latest"
  - name: require-signature-verification
    match:
      any:
      - resources:
          kinds:
          - Pod
    context:
    - name: keylessEntries
      imageRegistry:
        reference: "{{ element.image }}"
        keyless:
          subject: "*@mycompany.com"
          issuer: "https://accounts.google.com"
    validate:
      message: "Image signature verification failed"
      foreach:
      - list: "request.object.spec.containers"
        deny:
          conditions:
            all:
            - key: "{{ keylessEntries }}"
              operator: AnyNotIn
              value: ["true"]
```

### Resource Limits and Quotas
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: resource-constraints
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: require-resource-requests
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
          - StatefulSet
    validate:
      message: "Resource requests are required"
      pattern:
        spec:
          containers:
          - name: "*"
            resources:
              requests:
                memory: "?*"
                cpu: "?*"
  - name: limit-memory-usage
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Memory request cannot exceed 2Gi"
      deny:
        conditions:
          any:
          - key: "{{ request.object.spec.containers[?contains(@.resources.requests.memory, 'Gi')] | length(@) }}"
            operator: GreaterThan
            value: 0
          - key: "{{ request.object.spec.containers[?to_number(@.resources.requests.memory | split(@, 'Gi')[0]) > `2`] | length(@) }}"
            operator: GreaterThan
            value: 0
  - name: cpu-limit-range
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CPU requests must be between 100m and 2000m"
      foreach:
      - list: "request.object.spec.containers"
        deny:
          conditions:
            any:
            - key: "{{ element.resources.requests.cpu || '0m' | to_number(@) }}"
              operator: LessThan
              value: 100
            - key: "{{ element.resources.requests.cpu || '0m' | to_number(@) }}"
              operator: GreaterThan
              value: 2000
```

### Network Security
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: network-security
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: require-network-policy
    match:
      any:
      - resources:
          kinds:
          - Namespace
    exclude:
      any:
      - resources:
          namespaces:
          - kube-system
          - kyverno
    context:
    - name: networkPolicyCount
      apiCall:
        urlPath: "/api/v1/namespaces/{{request.object.metadata.name}}/networkpolicies"
        jmesPath: "items | length(@)"
    validate:
      message: "Namespace must have at least one NetworkPolicy"
      deny:
        conditions:
          any:
          - key: "{{ networkPolicyCount }}"
            operator: Equals
            value: 0
  - name: disallow-default-service-account
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
          - StatefulSet
    validate:
      message: "Default service account usage is not allowed"
      pattern:
        spec:
          =(serviceAccountName): "!default"
  - name: require-readonly-filesystem
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
          - StatefulSet
    validate:
      message: "Containers must use read-only root filesystem"
      pattern:
        spec:
          containers:
          - securityContext:
              readOnlyRootFilesystem: true
```

### Compliance and Governance
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: compliance-policy
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: require-pod-security-standards
    match:
      any:
      - resources:
          kinds:
          - Namespace
    validate:
      message: "Namespace must have pod security standard labels"
      pattern:
        metadata:
          labels:
            pod-security.kubernetes.io/enforce: "restricted|baseline"
            pod-security.kubernetes.io/audit: "restricted"
            pod-security.kubernetes.io/warn: "restricted"
  - name: enforce-data-classification
    match:
      any:
      - resources:
          kinds:
          - Secret
          - ConfigMap
    validate:
      message: "Data classification label is required"
      pattern:
        metadata:
          labels:
            data-classification: "public|internal|confidential|restricted"
  - name: require-backup-annotation
    match:
      any:
      - resources:
          kinds:
          - PersistentVolumeClaim
    validate:
      message: "PVC must specify backup policy"
      pattern:
        metadata:
          annotations:
            backup.policy: "?*"
```

## Context and External Data

### API Context
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: validate-with-context
spec:
  validationFailureAction: enforce
  rules:
  - name: check-namespace-quota
    match:
      any:
      - resources:
          kinds:
          - Pod
    context:
    - name: namespaceResourceQuota
      apiCall:
        urlPath: "/api/v1/namespaces/{{request.object.metadata.namespace}}/resourcequotas"
        jmesPath: "items[0].status.used"
    - name: namespacePods
      apiCall:
        urlPath: "/api/v1/namespaces/{{request.object.metadata.namespace}}/pods"
        jmesPath: "items | length(@)"
    validate:
      message: "Namespace has reached maximum pod limit"
      deny:
        conditions:
          any:
          - key: "{{ namespacePods }}"
            operator: GreaterThan
            value: 50
```

### ConfigMap Context
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: validate-with-configmap
spec:
  validationFailureAction: enforce
  rules:
  - name: check-allowed-registries
    match:
      any:
      - resources:
          kinds:
          - Pod
    context:
    - name: allowedRegistries
      configMap:
        name: allowed-registries
        namespace: kyverno
    validate:
      message: "Image registry not in allowed list"
      foreach:
      - list: "request.object.spec.containers"
        deny:
          conditions:
            all:
            - key: "{{ element.image | split(@, '/')[0] }}"
              operator: AnyNotIn
              value: "{{ allowedRegistries.data.registries | split(@, ',') }}"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: allowed-registries
  namespace: kyverno
data:
  registries: "docker.io,gcr.io,registry.company.com"
```

### Variable Context
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: validate-with-variables
spec:
  validationFailureAction: enforce
  rules:
  - name: limit-replicas-by-namespace
    match:
      any:
      - resources:
          kinds:
          - Deployment
    context:
    - name: maxReplicas
      variable:
        value: |
          {{
            if (contains(['production', 'prod'], request.object.metadata.namespace))
              then `10`
            else if (contains(['staging', 'stage'], request.object.metadata.namespace))
              then `5`
            else `3`
          }}
    validate:
      message: "Replica count exceeds limit for this namespace"
      deny:
        conditions:
          any:
          - key: "{{ request.object.spec.replicas || `1` }}"
            operator: GreaterThan
            value: "{{ maxReplicas }}"
```

## Policy Testing and Validation

### Test Framework
```python
import yaml
import subprocess
import tempfile
import os
import json

class KyvernoTester:
    def __init__(self, kubeconfig=None):
        self.kubeconfig = kubeconfig
        
    def apply_policy(self, policy_yaml):
        """Apply Kyverno policy"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(policy_yaml, f)
            f.flush()
            
            cmd = ['kubectl', 'apply', '-f', f.name]
            if self.kubeconfig:
                cmd.extend(['--kubeconfig', self.kubeconfig])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            os.unlink(f.name)
            
            return result.returncode == 0, result.stdout, result.stderr
    
    def test_resource_against_policy(self, resource_yaml, expect_pass=False):
        """Test resource against Kyverno policies"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(resource_yaml, f)
            f.flush()
            
            cmd = ['kubectl', 'apply', '-f', f.name, '--dry-run=server']
            if self.kubeconfig:
                cmd.extend(['--kubeconfig', self.kubeconfig])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            os.unlink(f.name)
            
            success = result.returncode == 0
            if expect_pass:
                return success, result.stdout if success else result.stderr
            else:
                return not success, result.stderr if not success else result.stdout
    
    def get_policy_violations(self, policy_name):
        """Get policy violations"""
        cmd = ['kubectl', 'get', 'policyreport', '-o', 'json']
        if self.kubeconfig:
            cmd.extend(['--kubeconfig', self.kubeconfig])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            reports = json.loads(result.stdout)
            violations = []
            for report in reports.get('items', []):
                for result_item in report.get('results', []):
                    if result_item.get('policy') == policy_name and result_item.get('result') == 'fail':
                        violations.append(result_item)
            return violations
        return []
    
    def run_policy_test_suite(self, test_cases):
        """Run comprehensive policy test suite"""
        results = []
        
        for test_case in test_cases:
            name = test_case['name']
            policy = test_case.get('policy')
            resource = test_case['resource']
            expect_pass = test_case.get('expect_pass', False)
            
            # Apply policy if provided
            if policy:
                policy_success, policy_msg, policy_err = self.apply_policy(policy)
                if not policy_success:
                    results.append({
                        'name': name,
                        'success': False,
                        'message': f"Failed to apply policy: {policy_err}",
                        'expected_pass': expect_pass
                    })
                    continue
            
            # Test resource
            success, message = self.test_resource_against_policy(resource, expect_pass)
            results.append({
                'name': name,
                'success': success,
                'message': message,
                'expected_pass': expect_pass
            })
        
        return results

# Usage
tester = KyvernoTester()

test_cases = [
    {
        'name': 'Pod without required labels should fail',
        'policy': {
            'apiVersion': 'kyverno.io/v1',
            'kind': 'ClusterPolicy',
            'metadata': {'name': 'require-labels'},
            'spec': {
                'validationFailureAction': 'enforce',
                'rules': [{
                    'name': 'check-labels',
                    'match': {
                        'any': [{'resources': {'kinds': ['Pod']}}]
                    },
                    'validate': {
                        'message': 'Pod must have team label',
                        'pattern': {
                            'metadata': {
                                'labels': {'team': '?*'}
                            }
                        }
                    }
                }]
            }
        },
        'resource': {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {'name': 'test-pod', 'namespace': 'default'},
            'spec': {'containers': [{'name': 'test', 'image': 'nginx'}]}
        },
        'expect_pass': False
    }
]

results = tester.run_policy_test_suite(test_cases)
for result in results:
    print(f"Test: {result['name']}")
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print()
```

### CLI Testing
```bash
#!/bin/bash
# test-kyverno-policies.sh

set -e

POLICY_DIR=${1:-./policies}
TEST_DIR=${2:-./tests}

echo "Testing Kyverno policies..."

# Function to test policy
test_policy() {
    local policy_file=$1
    local test_file=$2
    local expect_fail=${3:-true}
    
    echo "Testing policy: $(basename $policy_file)"
    
    # Apply policy
    kubectl apply -f "$policy_file"
    
    # Wait for policy to be ready
    sleep 5
    
    # Test with sample resource
    if kubectl apply -f "$test_file" --dry-run=server &>/dev/null; then
        if [ "$expect_fail" = "true" ]; then
            echo "  ❌ Expected failure but resource was accepted"
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
        policy_name=$(basename "$policy_file" .yaml)
        
        # Test positive cases (should pass)
        if [ -f "$TEST_DIR/${policy_name}-pass.yaml" ]; then
            test_policy "$policy_file" "$TEST_DIR/${policy_name}-pass.yaml" false
        fi
        
        # Test negative cases (should fail)
        if [ -f "$TEST_DIR/${policy_name}-fail.yaml" ]; then
            test_policy "$policy_file" "$TEST_DIR/${policy_name}-fail.yaml" true
        fi
    fi
done

echo "Policy testing completed!"

# Generate policy report
echo "Generating policy report..."
kubectl get policyreport -A -o json | jq '.items[] | {namespace: .metadata.namespace, summary: .summary}'
```

## Monitoring and Observability

### Prometheus Metrics
```yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: kyverno-metrics
  namespace: kyverno
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: kyverno
  endpoints:
  - port: metrics-port
    interval: 30s
    path: /metrics
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: kyverno-alerts
  namespace: kyverno
spec:
  groups:
  - name: kyverno
    rules:
    - alert: KyvernoPolicyViolations
      expr: increase(kyverno_policy_execution_duration_seconds_count{policy_validation_mode="enforce",policy_result="fail"}[5m]) > 0
      for: 0m
      labels:
        severity: warning
      annotations:
        summary: "Kyverno policy violations detected"
        description: "Policy {{ $labels.policy_name }} has {{ $value }} violations"
    
    - alert: KyvernoWebhookErrors
      expr: increase(kyverno_http_requests_total{code!~"2.."}[5m]) > 0
      for: 2m
      labels:
        severity: critical
      annotations:
        summary: "Kyverno webhook errors detected"
        description: "Kyverno webhook has {{ $value }} errors"
    
    - alert: KyvernoHighLatency
      expr: histogram_quantile(0.95, rate(kyverno_policy_execution_duration_seconds_bucket[5m])) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Kyverno high policy execution latency"
        description: "95th percentile latency is {{ $value }}s"
```

### Policy Reports Dashboard
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: policy-dashboard
  namespace: kyverno
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "Kyverno Policy Dashboard",
        "panels": [
          {
            "title": "Policy Violations by Namespace",
            "type": "bargauge",
            "targets": [
              {
                "expr": "sum(kyverno_policy_results_total{policy_result=\"fail\"}) by (policy_namespace)",
                "legendFormat": "{{policy_namespace}}"
              }
            ]
          },
          {
            "title": "Policy Execution Time",
            "type": "graph",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(kyverno_policy_execution_duration_seconds_bucket[5m]))",
                "legendFormat": "95th percentile"
              },
              {
                "expr": "histogram_quantile(0.50, rate(kyverno_policy_execution_duration_seconds_bucket[5m]))",
                "legendFormat": "50th percentile"
              }
            ]
          },
          {
            "title": "Webhook Request Rate",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(kyverno_http_requests_total[5m])",
                "legendFormat": "{{method}} {{code}}"
              }
            ]
          }
        ]
      }
    }
```

### Log Collection
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-kyverno
  namespace: logging
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush         1
        Log_Level     info
        Daemon        off
        Parsers_File  parsers.conf
    
    [INPUT]
        Name              tail
        Path              /var/log/pods/kyverno_kyverno-*/*/*.log
        Parser            cri
        Tag               kyverno.*
        Refresh_Interval  5
        Mem_Buf_Limit     32MB
    
    [FILTER]
        Name                parser
        Match               kyverno.*
        Key_Name            log
        Parser              json
        Reserve_Data        On
    
    [FILTER]
        Name                record_modifier
        Match               kyverno.*
        Record              service kyverno
        Record              component policy-engine
    
    [OUTPUT]
        Name  es
        Match kyverno.*
        Host  elasticsearch.logging.svc.cluster.local
        Port  9200
        Index kyverno-logs
        Type  _doc
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Kyverno Policy Validation

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
    
    - name: Install Kyverno
      run: |
        kubectl apply -f https://github.com/kyverno/kyverno/releases/latest/download/install.yaml
        kubectl wait --for=condition=Ready pods --all -n kyverno --timeout=300s
    
    - name: Validate Policies
      run: |
        # Validate policy syntax
        for policy in policies/*.yaml; do
          echo "Validating $policy"
          kubectl apply -f "$policy" --dry-run=server
        done
    
    - name: Test Policies
      run: |
        # Apply all policies
        kubectl apply -f policies/
        
        # Wait for policies to be ready
        sleep 30
        
        # Run tests
        ./scripts/test-policies.sh
    
    - name: Generate Policy Report
      run: |
        # Get policy reports
        kubectl get policyreport -A -o json > policy-report.json
        
        # Check for violations
        violations=$(jq '.items[].summary.fail // 0' policy-report.json | paste -sd+ - | bc)
        if [ "$violations" -gt 0 ]; then
          echo "Found $violations policy violations"
          jq '.items[] | select(.summary.fail > 0)' policy-report.json
          exit 1
        fi
    
    - name: Upload Reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: policy-reports
        path: policy-report.json
```

### GitLab CI
```yaml
stages:
  - validate
  - test
  - deploy

variables:
  KYVERNO_VERSION: "v1.10.0"

.kyverno_template: &kyverno_template
  image: bitnami/kubectl:latest
  before_script:
    - kubectl version --client

validate_policies:
  <<: *kyverno_template
  stage: validate
  script:
    - |
      echo "Validating Kyverno policies..."
      for policy in policies/*.yaml; do
        echo "Validating $policy"
        kubectl apply -f "$policy" --dry-run=server --validate=true
      done
  rules:
    - changes:
        - policies/**/*.yaml

test_policies:
  <<: *kyverno_template
  stage: test
  services:
    - name: kindest/node:v1.27.0
      alias: kubernetes
  script:
    - |
      # Install Kyverno
      kubectl apply -f https://github.com/kyverno/kyverno/releases/download/$KYVERNO_VERSION/install.yaml
      kubectl wait --for=condition=Ready pods --all -n kyverno --timeout=300s
      
      # Apply policies
      kubectl apply -f policies/
      sleep 30
      
      # Run tests
      ./scripts/test-policies.sh
      
      # Generate report
      kubectl get policyreport -A -o json > policy-report.json
  artifacts:
    reports:
      junit: test-results.xml
    paths:
      - policy-report.json
    expire_in: 1 week
  rules:
    - changes:
        - policies/**/*.yaml

deploy_policies:
  <<: *kyverno_template
  stage: deploy
  script:
    - kubectl apply -f policies/
  environment:
    name: production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      changes:
        - policies/**/*.yaml
  when: manual
```

## Configuration and Best Practices

### Resource Configuration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kyverno-config
  namespace: kyverno
data:
  # Global configuration
  excludeGroupRole: "system:serviceaccounts:kyverno,system:serviceaccounts:kube-system"
  excludeUsername: "system:kyverno"
  generateSuccessEvents: "true"
  
  # Resource limits
  resourceFilters: |
    [Event,*,*]
    [*,kube-system,*]
    [*,kube-public,*]
    [*,kyverno,*]
    [Node,*,*]
    [APIService,*,*]
    [TokenReview,*,*]
    [SubjectAccessReview,*,*]
    [SelfSubjectAccessReview,*,*]
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kyverno
  namespace: kyverno
spec:
  template:
    spec:
      containers:
      - name: kyverno
        resources:
          limits:
            memory: "1Gi"
            cpu: "500m"
          requests:
            memory: "512Mi"
            cpu: "200m"
        env:
        - name: KYVERNO_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: INIT_CONFIG
          value: kyverno-config
        - name: METRICS_CONFIG
          value: kyverno-metrics-config
        - name: KYVERNO_POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
```

### Performance Tuning
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kyverno-config
  namespace: kyverno
data:
  # Performance settings
  webhookTimeout: "15"
  clientRateLimitQPS: "20"
  clientRateLimitBurst: "50"
  webhookAnnotations: |
    prometheus.io/scrape: "true"
    prometheus.io/port: "8000"
    prometheus.io/path: "/metrics"
  
  # Resource filters to exclude from processing
  resourceFilters: |
    [Event,*,*]
    [*,kube-system,*]
    [*,kube-public,*]
    [*,kyverno,*]
    [Node,*,*]
    [Lease,*,*]
  
  # Disable features if not needed
  generateValidatingAdmissionPolicy: "false"
  autoUpdateWebhooks: "false"
```

### Security Hardening
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kyverno
  namespace: kyverno
automountServiceAccountToken: false
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kyverno
  namespace: kyverno
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: kyverno
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
        volumeMounts:
        - name: token
          mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          readOnly: true
      volumes:
      - name: token
        projected:
          sources:
          - serviceAccountToken:
              path: token
              expirationSeconds: 3607
          - configMap:
              name: kube-root-ca.crt
              items:
              - key: ca.crt
                path: ca.crt
          - downwardAPI:
              items:
              - path: namespace
                fieldRef:
                  fieldPath: metadata.namespace
```

## Troubleshooting

### Debug Commands
```bash
#!/bin/bash
# debug-kyverno.sh

echo "=== Kyverno System Status ==="
kubectl get pods -n kyverno
kubectl get validatingadmissionwebhooks
kubectl get mutatingadmissionwebhooks

echo "=== Kyverno Policies ==="
kubectl get clusterpolicy
kubectl get policy -A

echo "=== Policy Reports ==="
kubectl get policyreport -A
kubectl get clusterpolicyreport

echo "=== Recent Events ==="
kubectl get events -n kyverno --sort-by='.lastTimestamp'

echo "=== Webhook Logs ==="
kubectl logs -n kyverno -l app.kubernetes.io/name=kyverno --tail=50

echo "=== Policy Violations ==="
kubectl get policyreport -A -o json | jq '.items[] | select(.summary.fail > 0) | {namespace: .metadata.namespace, failures: .summary.fail, results: .results[]}'

echo "=== Configuration ==="
kubectl get configmap kyverno-config -n kyverno -o yaml
```

### Common Issues
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: troubleshooting-guide
  namespace: kyverno
data:
  common-issues.md: |
    # Kyverno Troubleshooting Guide
    
    ## Webhook Not Responding
    ```bash
    # Check webhook configuration
    kubectl get validatingadmissionwebhooks
    kubectl describe validatingadmissionwebhook kyverno-policy-validating-webhook-cfg
    
    # Check certificate
    kubectl get secret kyverno-svc.kyverno.svc.kyverno-tls-ca -n kyverno -o yaml
    
    # Restart Kyverno pods
    kubectl rollout restart deployment/kyverno -n kyverno
    ```
    
    ## Policy Not Working
    ```bash
    # Check policy status
    kubectl describe clusterpolicy <policy-name>
    
    # Check if resource matches policy
    kubectl get policyreport -A
    
    # Test policy with dry-run
    kubectl apply -f resource.yaml --dry-run=server
    ```
    
    ## Performance Issues
    ```yaml
    # Optimize resource filters
    resourceFilters: |
      [Event,*,*]
      [*,kube-system,*]
      [Lease,*,*]
    
    # Increase webhook timeout
    webhookTimeout: "30"
    
    # Adjust rate limits
    clientRateLimitQPS: "50"
    clientRateLimitBurst: "100"
    ```
```

## Resources

- [Kyverno Documentation](https://kyverno.io/docs/)
- [GitHub Repository](https://github.com/kyverno/kyverno)
- [Policy Library](https://github.com/kyverno/policies)
- [CLI Tool](https://github.com/kyverno/kyverno-cli)
- [Helm Charts](https://github.com/kyverno/kyverno/tree/main/charts/kyverno)
- [Community Policies](https://kyverno.io/policies/)
- [Best Practices](https://kyverno.io/docs/writing-policies/best-practices/)
- [Security Guide](https://kyverno.io/docs/security/)
- [Monitoring Guide](https://kyverno.io/docs/monitoring/)
- [Community Support](https://github.com/kyverno/kyverno/discussions)