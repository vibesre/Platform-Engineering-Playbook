# Tekton - Cloud-Native CI/CD for Kubernetes

## Overview

Tekton is a powerful and flexible open-source framework for creating CI/CD systems, allowing developers to build, test, and deploy across cloud providers and on-premises systems. It provides Kubernetes-native pipelines with reusable components.

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        Tekton Components                         │
├─────────────────────────┬───────────────────────────────────────┤
│    Tekton Pipelines     │         Tekton Triggers             │
│  • Tasks & TaskRuns     │  • EventListeners                  │
│  • Pipelines &          │  • TriggerTemplates                │
│    PipelineRuns         │  • TriggerBindings                 │
│  • Workspaces          │  • Interceptors                    │
│  • Results             │  • ClusterInterceptors             │
├─────────────────────────┼───────────────────────────────────────┤
│    Tekton Dashboard     │         Tekton Chains               │
│  • Web UI              │  • Supply chain security           │
│  • Pipeline viz        │  • Artifact signing                │
│  • Log streaming       │  • Attestation                     │
│  • Resource mgmt       │  • Provenance                      │
├─────────────────────────┼───────────────────────────────────────┤
│    Tekton CLI (tkn)     │         Tekton Hub/Catalog          │
│  • Pipeline control    │  • Reusable tasks                  │
│  • Log access         │  • Community contributions         │
│  • Resource CRUD      │  • Task discovery                  │
└─────────────────────────┴───────────────────────────────────────┘
                                    │
                                    ▼
                        ┌─────────────────────────┐
                        │    Kubernetes Pods      │
                        │   (Task Execution)      │
                        └─────────────────────────┘
```

### Key Concepts

1. **Task**: A collection of steps that perform a specific function
2. **Pipeline**: A collection of tasks in a specific order
3. **TaskRun**: An instantiation of a Task
4. **PipelineRun**: An instantiation of a Pipeline
5. **Workspace**: Shared storage between tasks
6. **PipelineResource**: Inputs and outputs to Tasks (deprecated)
7. **EventListener**: Receives incoming events
8. **TriggerTemplate**: Template for creating resources
9. **TriggerBinding**: Extracts data from events

## Installation

### Prerequisites

```bash
# Kubernetes 1.24+
kubectl version --client

# Check cluster access
kubectl cluster-info
```

### Install Tekton Pipelines

```bash
# Install latest Tekton Pipelines
kubectl apply --filename \
  https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml

# Monitor installation
kubectl get pods -n tekton-pipelines -w

# Verify installation
tkn version
```

### Install Tekton Triggers

```bash
# Install Tekton Triggers
kubectl apply --filename \
  https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml

# Install Interceptors
kubectl apply --filename \
  https://storage.googleapis.com/tekton-releases/triggers/latest/interceptors.yaml
```

### Install Tekton Dashboard

```bash
# Install Dashboard
kubectl apply --filename \
  https://storage.googleapis.com/tekton-releases/dashboard/latest/release.yaml

# Access Dashboard
kubectl port-forward -n tekton-pipelines service/tekton-dashboard 9097:9097

# Browse to http://localhost:9097
```

### Install Tekton CLI

```bash
# macOS
brew install tektoncd/tools/tektoncd-cli

# Linux
curl -LO https://github.com/tektoncd/cli/releases/latest/download/tkn_0.32.0_Linux_x86_64.tar.gz
tar xvzf tkn_0.32.0_Linux_x86_64.tar.gz -C /usr/local/bin tkn

# Verify
tkn version
```

## Configuration Examples

### Basic Task Definition

```yaml
# tasks/build-push.yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: build-push
  namespace: default
spec:
  description: Build and push Docker image
  params:
  - name: IMAGE
    description: Name of image to build
    type: string
  - name: DOCKERFILE
    description: Path to Dockerfile
    type: string
    default: ./Dockerfile
  - name: CONTEXT
    description: Build context
    type: string
    default: .
  workspaces:
  - name: source
    description: Source code
  - name: dockerconfig
    description: Docker config
    optional: true
  results:
  - name: IMAGE_DIGEST
    description: Digest of the image just built
  steps:
  - name: build-and-push
    image: gcr.io/kaniko-project/executor:latest
    workingDir: $(workspaces.source.path)
    env:
    - name: DOCKER_CONFIG
      value: $(workspaces.dockerconfig.path)
    command:
    - /kaniko/executor
    args:
    - --dockerfile=$(params.DOCKERFILE)
    - --context=$(workspaces.source.path)/$(params.CONTEXT)
    - --destination=$(params.IMAGE)
    - --digest-file=$(results.IMAGE_DIGEST.path)
    - --cache=true
    - --cache-ttl=24h
    resources:
      requests:
        cpu: 500m
        memory: 1Gi
      limits:
        cpu: 2
        memory: 4Gi
```

### Pipeline Definition

```yaml
# pipelines/ci-pipeline.yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: ci-pipeline
  namespace: default
spec:
  description: CI pipeline for microservices
  params:
  - name: repo-url
    type: string
    description: Git repository URL
  - name: revision
    type: string
    description: Git revision
    default: main
  - name: image-name
    type: string
    description: Docker image name
  workspaces:
  - name: shared-data
    description: Shared workspace
  - name: docker-credentials
    description: Docker registry credentials
  - name: kubeconfig
    description: Kubernetes config
  tasks:
  - name: fetch-source
    taskRef:
      name: git-clone
      kind: ClusterTask
    workspaces:
    - name: output
      workspace: shared-data
    params:
    - name: url
      value: $(params.repo-url)
    - name: revision
      value: $(params.revision)
  
  - name: run-tests
    runAfter: ["fetch-source"]
    taskRef:
      name: run-unit-tests
    workspaces:
    - name: source
      workspace: shared-data
  
  - name: code-analysis
    runAfter: ["fetch-source"]
    taskRef:
      name: sonarqube-scan
    workspaces:
    - name: source
      workspace: shared-data
    params:
    - name: sonar-project-key
      value: $(params.repo-url)
  
  - name: build-image
    runAfter: ["run-tests", "code-analysis"]
    taskRef:
      name: build-push
    workspaces:
    - name: source
      workspace: shared-data
    - name: dockerconfig
      workspace: docker-credentials
    params:
    - name: IMAGE
      value: $(params.image-name):$(tasks.fetch-source.results.commit)
  
  - name: security-scan
    runAfter: ["build-image"]
    taskRef:
      name: trivy-scan
    params:
    - name: image
      value: $(params.image-name):$(tasks.fetch-source.results.commit)
  
  - name: deploy-staging
    runAfter: ["security-scan"]
    taskRef:
      name: kubernetes-deploy
    workspaces:
    - name: source
      workspace: shared-data
    - name: kubeconfig
      workspace: kubeconfig
    params:
    - name: namespace
      value: staging
    - name: image
      value: $(params.image-name):$(tasks.fetch-source.results.commit)
  
  finally:
  - name: notify
    taskRef:
      name: send-notification
    params:
    - name: webhook-url
      value: "https://hooks.slack.com/services/XXX"
    - name: message
      value: "Pipeline $(context.pipelineRun.name) completed"
```

### Trigger Configuration

```yaml
# triggers/github-trigger.yaml
apiVersion: triggers.tekton.dev/v1beta1
kind: EventListener
metadata:
  name: github-listener
  namespace: default
spec:
  serviceAccountName: tekton-triggers-sa
  triggers:
  - name: github-push
    interceptors:
    - ref:
        name: github
      params:
      - name: secretRef
        value:
          secretName: github-webhook-secret
          secretKey: token
      - name: eventTypes
        value: ["push", "pull_request"]
    - ref:
        name: cel
      params:
      - name: filter
        value: >-
          body.ref == 'refs/heads/main' ||
          body.pull_request.base.ref == 'main'
    bindings:
    - ref: github-push-binding
    template:
      ref: ci-pipeline-template
---
apiVersion: triggers.tekton.dev/v1beta1
kind: TriggerBinding
metadata:
  name: github-push-binding
  namespace: default
spec:
  params:
  - name: git-repo-url
    value: $(body.repository.clone_url)
  - name: git-revision
    value: $(body.after)
  - name: git-repo-name
    value: $(body.repository.name)
  - name: git-author
    value: $(body.pusher.name)
---
apiVersion: triggers.tekton.dev/v1beta1
kind: TriggerTemplate
metadata:
  name: ci-pipeline-template
  namespace: default
spec:
  params:
  - name: git-repo-url
  - name: git-revision
  - name: git-repo-name
  resourcetemplates:
  - apiVersion: tekton.dev/v1beta1
    kind: PipelineRun
    metadata:
      generateName: ci-pipeline-run-
      labels:
        tekton.dev/pipeline: ci-pipeline
    spec:
      pipelineRef:
        name: ci-pipeline
      params:
      - name: repo-url
        value: $(tt.params.git-repo-url)
      - name: revision
        value: $(tt.params.git-revision)
      - name: image-name
        value: myregistry.io/$(tt.params.git-repo-name)
      workspaces:
      - name: shared-data
        volumeClaimTemplate:
          spec:
            accessModes:
            - ReadWriteOnce
            resources:
              requests:
                storage: 1Gi
      - name: docker-credentials
        secret:
          secretName: docker-credentials
      - name: kubeconfig
        secret:
          secretName: kubeconfig
      timeout: 1h
```

## Production Patterns

### Multi-Stage Pipeline

```yaml
# pipelines/multi-stage.yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: multi-stage-pipeline
spec:
  params:
  - name: app-name
  - name: git-url
  - name: git-revision
  workspaces:
  - name: shared-workspace
  - name: maven-cache
  - name: docker-credentials
  
  tasks:
  # Build Stage
  - name: fetch-repo
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
  
  - name: maven-build
    runAfter: ["fetch-repo"]
    taskRef:
      name: maven
      kind: ClusterTask
    workspaces:
    - name: source
      workspace: shared-workspace
    - name: maven-cache
      workspace: maven-cache
    params:
    - name: GOALS
      value: ["clean", "package", "-DskipTests"]
  
  # Test Stage
  - name: unit-tests
    runAfter: ["maven-build"]
    taskRef:
      name: maven
      kind: ClusterTask
    workspaces:
    - name: source
      workspace: shared-workspace
    - name: maven-cache
      workspace: maven-cache
    params:
    - name: GOALS
      value: ["test"]
  
  - name: integration-tests
    runAfter: ["unit-tests"]
    taskRef:
      name: maven
      kind: ClusterTask
    workspaces:
    - name: source
      workspace: shared-workspace
    - name: maven-cache
      workspace: maven-cache
    params:
    - name: GOALS
      value: ["verify", "-Pintegration-tests"]
  
  # Security Stage
  - name: sonar-scan
    runAfter: ["unit-tests"]
    taskRef:
      name: sonarqube-scanner
    workspaces:
    - name: source
      workspace: shared-workspace
    params:
    - name: sonar-host-url
      value: "https://sonar.example.com"
    - name: sonar-project-key
      value: $(params.app-name)
  
  - name: dependency-check
    runAfter: ["maven-build"]
    taskRef:
      name: owasp-dependency-check
    workspaces:
    - name: source
      workspace: shared-workspace
  
  # Build & Publish Stage
  - name: build-image
    runAfter: ["integration-tests", "sonar-scan"]
    taskRef:
      name: buildah
      kind: ClusterTask
    workspaces:
    - name: source
      workspace: shared-workspace
    params:
    - name: IMAGE
      value: "registry.example.com/$(params.app-name):$(tasks.fetch-repo.results.commit)"
    - name: TLSVERIFY
      value: "false"
  
  - name: scan-image
    runAfter: ["build-image"]
    taskRef:
      name: trivy-scanner
    params:
    - name: image-ref
      value: "registry.example.com/$(params.app-name):$(tasks.fetch-repo.results.commit)"
    - name: exit-code
      value: "1"
  
  # Deploy Stages
  - name: deploy-dev
    runAfter: ["scan-image"]
    taskRef:
      name: kustomize-deploy
    params:
    - name: namespace
      value: development
    - name: image
      value: "registry.example.com/$(params.app-name):$(tasks.fetch-repo.results.commit)"
  
  - name: run-smoke-tests
    runAfter: ["deploy-dev"]
    taskRef:
      name: smoke-tests
    params:
    - name: endpoint
      value: "https://dev.$(params.app-name).example.com"
  
  - name: deploy-staging
    runAfter: ["run-smoke-tests"]
    when:
    - input: "$(params.git-revision)"
      operator: in
      values: ["main", "master"]
    taskRef:
      name: kustomize-deploy
    params:
    - name: namespace
      value: staging
    - name: image
      value: "registry.example.com/$(params.app-name):$(tasks.fetch-repo.results.commit)"
  
  - name: performance-tests
    runAfter: ["deploy-staging"]
    taskRef:
      name: k6-load-test
    params:
    - name: script
      value: "performance-test.js"
    - name: endpoint
      value: "https://staging.$(params.app-name).example.com"
  
  - name: manual-approval
    runAfter: ["performance-tests"]
    taskRef:
      name: manual-approval
    params:
    - name: approvers
      value: ["platform-team", "product-owner"]
    - name: message
      value: "Approve deployment to production?"
  
  - name: deploy-production
    runAfter: ["manual-approval"]
    taskRef:
      name: blue-green-deploy
    params:
    - name: namespace
      value: production
    - name: image
      value: "registry.example.com/$(params.app-name):$(tasks.fetch-repo.results.commit)"
```

### Custom Task for Approval

```yaml
# tasks/manual-approval.yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: manual-approval
spec:
  params:
  - name: approvers
    type: array
    description: List of approvers
  - name: message
    type: string
    description: Approval message
    default: "Manual approval required"
  - name: timeout
    type: string
    description: Timeout for approval
    default: "3600"
  results:
  - name: approved-by
    description: User who approved
  - name: approval-time
    description: Time of approval
  steps:
  - name: create-approval-request
    image: curlimages/curl:latest
    script: |
      #!/bin/sh
      set -e
      
      # Create approval request
      APPROVAL_ID=$(curl -X POST https://approval-service.example.com/api/approvals \
        -H "Content-Type: application/json" \
        -d '{
          "approvers": $(params.approvers),
          "message": "$(params.message)",
          "pipeline": "$(context.pipelineRun.name)",
          "timeout": $(params.timeout)
        }' | jq -r '.id')
      
      echo "Approval request created: $APPROVAL_ID"
      echo $APPROVAL_ID > /workspace/approval-id
  
  - name: wait-for-approval
    image: curlimages/curl:latest
    script: |
      #!/bin/sh
      set -e
      
      APPROVAL_ID=$(cat /workspace/approval-id)
      TIMEOUT=$(params.timeout)
      ELAPSED=0
      
      while [ $ELAPSED -lt $TIMEOUT ]; do
        STATUS=$(curl -s https://approval-service.example.com/api/approvals/$APPROVAL_ID | jq -r '.status')
        
        if [ "$STATUS" = "approved" ]; then
          APPROVER=$(curl -s https://approval-service.example.com/api/approvals/$APPROVAL_ID | jq -r '.approvedBy')
          APPROVAL_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
          
          echo -n "$APPROVER" > $(results.approved-by.path)
          echo -n "$APPROVAL_TIME" > $(results.approval-time.path)
          
          echo "Approved by: $APPROVER at $APPROVAL_TIME"
          exit 0
        elif [ "$STATUS" = "rejected" ]; then
          echo "Approval rejected"
          exit 1
        fi
        
        echo "Waiting for approval... ($ELAPSED/$TIMEOUT seconds)"
        sleep 30
        ELAPSED=$((ELAPSED + 30))
      done
      
      echo "Approval timeout reached"
      exit 1
```

### Workspace Strategies

```yaml
# pipelines/workspace-example.yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: workspace-strategies
spec:
  workspaces:
  # Persistent workspace for source code
  - name: source-ws
    description: Source code workspace
  
  # Cache workspaces
  - name: maven-cache-ws
    description: Maven dependencies cache
  - name: npm-cache-ws
    description: NPM packages cache
  
  # Credentials workspaces
  - name: git-credentials-ws
    description: Git credentials
    optional: true
  - name: docker-credentials-ws
    description: Docker registry credentials
  
  # Temporary workspace
  - name: temp-ws
    description: Temporary build artifacts
  
  tasks:
  - name: clone-repo
    taskRef:
      name: git-clone
    workspaces:
    - name: output
      workspace: source-ws
    - name: ssh-directory
      workspace: git-credentials-ws
  
  - name: build-backend
    taskRef:
      name: maven-build
    workspaces:
    - name: source
      workspace: source-ws
      subPath: backend
    - name: maven-cache
      workspace: maven-cache-ws
  
  - name: build-frontend
    taskRef:
      name: npm-build
    workspaces:
    - name: source
      workspace: source-ws
      subPath: frontend
    - name: npm-cache
      workspace: npm-cache-ws
---
# PipelineRun with workspace bindings
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: workspace-strategies-run
spec:
  pipelineRef:
    name: workspace-strategies
  workspaces:
  # PVC for source
  - name: source-ws
    persistentVolumeClaim:
      claimName: source-pvc
  
  # PVC for caches (retained between runs)
  - name: maven-cache-ws
    persistentVolumeClaim:
      claimName: maven-cache-pvc
  - name: npm-cache-ws
    persistentVolumeClaim:
      claimName: npm-cache-pvc
  
  # Secret-based workspaces
  - name: git-credentials-ws
    secret:
      secretName: git-ssh-credentials
  - name: docker-credentials-ws
    secret:
      secretName: docker-config
  
  # EmptyDir for temporary data
  - name: temp-ws
    emptyDir: {}
```

### Tekton Chains Configuration

```yaml
# chains/signing-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: signing-secrets
  namespace: tekton-chains
data:
  cosign.key: <base64-encoded-private-key>
  cosign.pub: <base64-encoded-public-key>
---
# chains/chains-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: chains-config
  namespace: tekton-chains
data:
  artifacts.taskrun.format: "in-toto"
  artifacts.taskrun.storage: "oci"
  artifacts.taskrun.signer: "x509"
  artifacts.pipelinerun.format: "in-toto"
  artifacts.pipelinerun.storage: "oci"
  artifacts.pipelinerun.signer: "x509"
  artifacts.oci.storage: "oci"
  artifacts.oci.format: "simplesigning"
  artifacts.oci.signer: "x509"
  transparency.enabled: "true"
  transparency.url: "https://rekor.sigstore.dev"
```

## Security Best Practices

### RBAC Configuration

```yaml
# rbac/tekton-rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tekton-pipeline-sa
  namespace: ci-cd
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: tekton-pipeline-role
  namespace: ci-cd
rules:
- apiGroups: ["tekton.dev"]
  resources: ["tasks", "taskruns", "pipelines", "pipelineruns"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["secrets", "configmaps", "persistentvolumeclaims"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: tekton-pipeline-binding
  namespace: ci-cd
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: tekton-pipeline-role
subjects:
- kind: ServiceAccount
  name: tekton-pipeline-sa
  namespace: ci-cd
```

### Network Policies

```yaml
# network-policies/tekton-netpol.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tekton-pipelines
  namespace: tekton-pipelines
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/part-of: tekton-pipelines
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: tekton-pipelines
    - podSelector: {}
  - from:
    - namespaceSelector:
        matchLabels:
          name: ci-cd
  egress:
  - to:
    - namespaceSelector: {}
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 169.254.169.254/32
```

## Monitoring and Observability

### Prometheus Metrics

```yaml
# monitoring/servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: tekton-pipelines
  namespace: tekton-pipelines
spec:
  selector:
    matchLabels:
      app.kubernetes.io/part-of: tekton-pipelines
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Tekton Pipelines",
    "panels": [
      {
        "title": "PipelineRun Duration",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(tekton_pipelines_controller_pipelinerun_duration_seconds_bucket[5m])) by (le))"
          }
        ]
      },
      {
        "title": "TaskRun Status",
        "targets": [
          {
            "expr": "sum by (status) (tekton_pipelines_controller_taskrun_count)"
          }
        ]
      },
      {
        "title": "Running Pipelines",
        "targets": [
          {
            "expr": "sum(tekton_pipelines_controller_running_pipelineruns_count)"
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting

### Common Commands

```bash
# List all Tekton resources
tkn pipeline list
tkn task list
tkn taskrun list
tkn pipelinerun list

# Get pipeline run details
tkn pipelinerun describe <name>
tkn pipelinerun logs <name>

# Get task run logs
tkn taskrun logs <name>

# Cancel a pipeline run
tkn pipelinerun cancel <name>

# Delete completed runs
tkn pipelinerun delete --all --keep 5

# Start a pipeline
tkn pipeline start ci-pipeline \
  --param repo-url=https://github.com/myorg/app \
  --param revision=main \
  --workspace name=shared-data,claimName=pvc \
  --showlog

# Debug a failed task
kubectl describe taskrun <name>
kubectl logs -l tekton.dev/taskRun=<name> --all-containers

# Check events
kubectl get events --field-selector involvedObject.name=<name>
```

## Integration Examples

### GitLab Integration

```yaml
# .gitlab-ci.yml
trigger-tekton:
  stage: trigger
  script:
    - |
      kubectl create -f - <<EOF
      apiVersion: tekton.dev/v1beta1
      kind: PipelineRun
      metadata:
        generateName: gitlab-triggered-
      spec:
        pipelineRef:
          name: ci-pipeline
        params:
        - name: repo-url
          value: $CI_PROJECT_URL
        - name: revision
          value: $CI_COMMIT_SHA
        workspaces:
        - name: shared-data
          volumeClaimTemplate:
            spec:
              accessModes:
              - ReadWriteOnce
              resources:
                requests:
                  storage: 5Gi
      EOF
```

### ArgoCD Integration

```yaml
# argocd-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: tekton-app
  finalizers:
  - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/k8s-config
    targetRevision: main
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
  # Post sync hook to trigger Tekton
  syncPolicy:
    syncOptions:
    - CreateNamespace=true
  postSync:
    - apiVersion: batch/v1
      kind: Job
      metadata:
        name: trigger-smoke-tests
      spec:
        template:
          spec:
            containers:
            - name: trigger
              image: bitnami/kubectl
              command:
              - sh
              - -c
              - |
                kubectl create -f - <<EOF
                apiVersion: tekton.dev/v1beta1
                kind: TaskRun
                metadata:
                  generateName: smoke-tests-
                spec:
                  taskRef:
                    name: smoke-tests
                  params:
                  - name: endpoint
                    value: https://app.example.com
                EOF
```