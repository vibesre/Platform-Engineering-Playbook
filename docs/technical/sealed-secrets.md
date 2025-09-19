# Sealed Secrets

Sealed Secrets is a Kubernetes controller and tool for one-way encrypted Secrets that can be stored safely in Git repositories, even public ones.

## Overview

### Key Concepts
- **Sealed Secrets**: Encrypted versions of Kubernetes Secrets that can be safely stored in Git
- **Bitnami Sealed Secrets Controller**: Kubernetes controller that decrypts SealedSecrets into regular Secrets
- **kubeseal**: CLI tool for creating SealedSecrets from regular Secrets
- **Public/Private Key Encryption**: Uses asymmetric encryption for security
- **Namespace/Name Scoped**: Secrets are bound to specific namespaces and names by default

### Architecture
```
Developer → kubeseal → SealedSecret → Git → Kubernetes Controller → Secret
```

## Installation

### Controller Installation
```bash
# Install using kubectl
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/controller.yaml

# Or install using Helm
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm repo update

helm install sealed-secrets sealed-secrets/sealed-secrets \
  --namespace kube-system \
  --version 2.7.1

# Verify installation
kubectl get pods -n kube-system | grep sealed-secrets
```

### CLI Tool Installation
```bash
# Linux
curl -OL https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/kubeseal-0.18.0-linux-amd64.tar.gz
tar -xvzf kubeseal-0.18.0-linux-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal

# macOS
brew install kubeseal

# Or download directly
curl -OL https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/kubeseal-0.18.0-darwin-amd64.tar.gz
tar -xvzf kubeseal-0.18.0-darwin-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal

# Windows
curl -OL https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/kubeseal-0.18.0-windows-amd64.tar.gz

# Verify installation
kubeseal --version
```

### Custom Installation with Helm
```yaml
# values.yaml
fullnameOverride: "sealed-secrets-controller"

controller:
  create: true
  
secretName: "sealed-secrets-key"

image:
  repository: bitnami/sealed-secrets-controller
  tag: v0.18.0
  pullPolicy: IfNotPresent

resources:
  limits:
    cpu: 2000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 256Mi

nodeSelector: {}
tolerations: []
affinity: {}

rbac:
  create: true
  pspEnabled: false

serviceAccount:
  create: true
  name: ""

servicemonitor:
  create: false
  namespace: monitoring
  labels: {}

networkPolicy:
  create: false

podSecurityPolicy:
  create: false

# Additional environment variables
env: []

# Additional volumes
volumes: []

# Additional volume mounts  
volumeMounts: []

# Pod security context
podSecurityContext:
  fsGroup: 65534

# Container security context
securityContext:
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1001

# Liveness probe
livenessProbe:
  httpGet:
    path: /healthz
    port: http
  initialDelaySeconds: 30
  periodSeconds: 30

# Readiness probe  
readinessProbe:
  httpGet:
    path: /healthz
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
```

```bash
# Install with custom values
helm install sealed-secrets sealed-secrets/sealed-secrets \
  --namespace kube-system \
  --values values.yaml
```

## Basic Usage

### Creating Sealed Secrets
```bash
# Create a regular secret (don't apply this!)
kubectl create secret generic mysecret \
  --from-literal=username=admin \
  --from-literal=password=supersecret \
  --dry-run=client \
  -o yaml > secret.yaml

# Convert to sealed secret
kubeseal --format yaml < secret.yaml > sealed-secret.yaml

# Or in one command
kubectl create secret generic mysecret \
  --from-literal=username=admin \
  --from-literal=password=supersecret \
  --dry-run=client \
  -o yaml | kubeseal --format yaml > sealed-secret.yaml

# Apply the sealed secret
kubectl apply -f sealed-secret.yaml
```

### Working with Files
```bash
# Create secret from files
kubectl create secret generic app-config \
  --from-file=config.json \
  --from-file=database.conf \
  --dry-run=client \
  -o yaml | kubeseal --format yaml > sealed-app-config.yaml

# Create secret from environment file
kubectl create secret generic env-vars \
  --from-env-file=.env \
  --dry-run=client \
  -o yaml | kubeseal --format yaml > sealed-env-vars.yaml

# Create TLS secret
kubectl create secret tls app-tls \
  --cert=tls.crt \
  --key=tls.key \
  --dry-run=client \
  -o yaml | kubeseal --format yaml > sealed-app-tls.yaml
```

### Different Scopes
```bash
# Namespace-wide scope (default)
kubeseal --scope namespace-wide < secret.yaml > sealed-secret.yaml

# Cluster-wide scope
kubeseal --scope cluster-wide < secret.yaml > sealed-secret.yaml

# Strict scope (namespace + name binding)
kubeseal --scope strict < secret.yaml > sealed-secret.yaml
```

## Advanced Usage

### Using Raw Mode
```bash
# Raw mode for single values
echo -n supersecret | kubeseal --raw --name=mysecret --namespace=default

# Use raw value in YAML
cat << EOF > sealed-secret.yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysecret
  namespace: default
spec:
  encryptedData:
    password: $(echo -n supersecret | kubeseal --raw --name=mysecret --namespace=default)
  template:
    metadata:
      name: mysecret
      namespace: default
    type: Opaque
EOF
```

### Certificate Management
```bash
# Fetch the public certificate
kubeseal --fetch-cert > public.pem

# Use offline encryption with certificate
kubeseal --cert public.pem < secret.yaml > sealed-secret.yaml

# Rotate certificates (only do this if needed!)
kubectl delete secret sealed-secrets-key -n kube-system
kubectl delete pod -n kube-system -l name=sealed-secrets-controller

# Or manually create new certificate
openssl req -x509 -days 365 -nodes -newkey rsa:4096 \
  -keyout tls.key -out tls.crt -subj "/CN=sealed-secret/O=sealed-secret"

kubectl create secret tls sealed-secrets-key \
  --cert=tls.crt --key=tls.key \
  --namespace=kube-system
```

## Practical Examples

### Database Credentials
```yaml
# database-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: database-credentials
  namespace: production
type: Opaque
data:
  host: cG9zdGdyZXMuc3ZjLmNsdXN0ZXIubG9jYWw=  # postgres.svc.cluster.local
  port: NTQzMg==  # 5432
  database: bXlhcHA=  # myapp
  username: YWRtaW4=  # admin
  password: c3VwZXJzZWNyZXQ=  # supersecret
```

```bash
# Create sealed secret
kubeseal --format yaml < database-secret.yaml > sealed-database-secret.yaml
```

### API Keys and Tokens
```yaml
# api-keys-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-keys
  namespace: production
type: Opaque
stringData:
  stripe-api-key: "sk_live_..."
  sendgrid-api-key: "SG...."
  jwt-secret: "your-jwt-secret-key"
  oauth-client-id: "oauth-client-id"
  oauth-client-secret: "oauth-client-secret"
```

```bash
# Create sealed secret
kubeseal --format yaml < api-keys-secret.yaml > sealed-api-keys.yaml
```

### TLS Certificates
```bash
# Create TLS secret from cert files
kubectl create secret tls app-tls-cert \
  --cert=app.crt \
  --key=app.key \
  --namespace=production \
  --dry-run=client \
  -o yaml | kubeseal --format yaml > sealed-tls-cert.yaml
```

### Docker Registry Credentials
```bash
# Create docker registry secret
kubectl create secret docker-registry docker-registry-secret \
  --docker-server=registry.example.com \
  --docker-username=username \
  --docker-password=password \
  --docker-email=user@example.com \
  --namespace=production \
  --dry-run=client \
  -o yaml | kubeseal --format yaml > sealed-docker-registry.yaml
```

## Integration Examples

### Deployment with Sealed Secrets
```yaml
# sealed-app-secrets.yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  encryptedData:
    DATABASE_URL: AgBy3i4OJSWK+PiTySYZZA9rO5QtQvKtbQ...
    API_KEY: AgBNFZjQA9rO5QtQvKtbQy4OJSWK+PiTySYZZ...
    JWT_SECRET: AgBKtbQy4OJSWK+PiTySYZZA9rO5QtQv...
  template:
    metadata:
      name: app-secrets
      namespace: production
    type: Opaque
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:v1.0.0
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_URL
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: API_KEY
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: JWT_SECRET
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

### Helm Chart Integration
```yaml
# templates/sealed-secret.yaml
{{- if .Values.sealedSecrets.enabled }}
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: {{ include "myapp.fullname" . }}-secrets
  namespace: {{ .Release.Namespace }}
spec:
  encryptedData:
    {{- range $key, $value := .Values.sealedSecrets.encryptedData }}
    {{ $key }}: {{ $value }}
    {{- end }}
  template:
    metadata:
      name: {{ include "myapp.fullname" . }}-secrets
      namespace: {{ .Release.Namespace }}
    type: Opaque
{{- end }}
```

```yaml
# values.yaml
sealedSecrets:
  enabled: true
  encryptedData:
    DATABASE_URL: "AgBy3i4OJSWK+PiTySYZZA9rO5QtQvKtbQ..."
    API_KEY: "AgBNFZjQA9rO5QtQvKtbQy4OJSWK+PiTySYZZ..."
    JWT_SECRET: "AgBKtbQy4OJSWK+PiTySYZZA9rO5QtQv..."
```

### Init Container Pattern
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-init
  namespace: production
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app-with-init
  template:
    metadata:
      labels:
        app: app-with-init
    spec:
      initContainers:
      - name: setup-config
        image: busybox:1.35
        command: ['sh', '-c']
        args:
        - |
          echo "Setting up configuration..."
          cp /secrets/config.json /app-config/
          chmod 600 /app-config/config.json
        volumeMounts:
        - name: secrets-volume
          mountPath: /secrets
          readOnly: true
        - name: app-config
          mountPath: /app-config
      containers:
      - name: app
        image: myapp:v1.0.0
        volumeMounts:
        - name: app-config
          mountPath: /app/config
          readOnly: true
        env:
        - name: CONFIG_PATH
          value: "/app/config/config.json"
      volumes:
      - name: secrets-volume
        secret:
          secretName: app-config-secret
      - name: app-config
        emptyDir: {}
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy with Sealed Secrets

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install kubeseal
      run: |
        curl -OL https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/kubeseal-0.18.0-linux-amd64.tar.gz
        tar -xvzf kubeseal-0.18.0-linux-amd64.tar.gz kubeseal
        sudo install -m 755 kubeseal /usr/local/bin/kubeseal
    
    - name: Setup kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'v1.25.0'
    
    - name: Configure kubectl
      run: |
        echo "${{ secrets.KUBECONFIG }}" | base64 -d > kubeconfig.yaml
        export KUBECONFIG=kubeconfig.yaml
    
    - name: Create secrets and seal them
      env:
        DATABASE_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}
        API_KEY: ${{ secrets.API_KEY }}
        JWT_SECRET: ${{ secrets.JWT_SECRET }}
      run: |
        # Create secret from environment variables
        kubectl create secret generic app-secrets \
          --from-literal=database-password="$DATABASE_PASSWORD" \
          --from-literal=api-key="$API_KEY" \
          --from-literal=jwt-secret="$JWT_SECRET" \
          --namespace=production \
          --dry-run=client \
          -o yaml | kubeseal --format yaml > k8s/sealed-secrets.yaml
    
    - name: Commit and push sealed secrets
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add k8s/sealed-secrets.yaml
        git commit -m "Update sealed secrets" || exit 0
        git push
    
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/
```

### GitLab CI
```yaml
# .gitlab-ci.yml
stages:
  - seal-secrets
  - deploy

variables:
  KUBESEAL_VERSION: "0.18.0"

.kubeseal_install: &kubeseal_install
  - curl -OL "https://github.com/bitnami-labs/sealed-secrets/releases/download/v${KUBESEAL_VERSION}/kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz"
  - tar -xvzf "kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz" kubeseal
  - chmod +x kubeseal
  - mv kubeseal /usr/local/bin/

seal_secrets:
  stage: seal-secrets
  image: alpine/k8s:1.25.6
  before_script:
    - *kubeseal_install
    - echo "$KUBECONFIG" | base64 -d > kubeconfig.yaml
    - export KUBECONFIG=kubeconfig.yaml
  script:
    - |
      kubectl create secret generic app-secrets \
        --from-literal=database-password="$DATABASE_PASSWORD" \
        --from-literal=api-key="$API_KEY" \
        --from-literal=jwt-secret="$JWT_SECRET" \
        --namespace=production \
        --dry-run=client \
        -o yaml | kubeseal --format yaml > k8s/sealed-secrets.yaml
  artifacts:
    paths:
      - k8s/sealed-secrets.yaml
  only:
    - main

deploy:
  stage: deploy
  image: alpine/k8s:1.25.6
  before_script:
    - echo "$KUBECONFIG" | base64 -d > kubeconfig.yaml
    - export KUBECONFIG=kubeconfig.yaml
  script:
    - kubectl apply -f k8s/
  dependencies:
    - seal_secrets
  only:
    - main
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    environment {
        KUBESEAL_VERSION = '0.18.0'
    }
    
    stages {
        stage('Install Tools') {
            steps {
                script {
                    sh '''
                        curl -OL https://github.com/bitnami-labs/sealed-secrets/releases/download/v${KUBESEAL_VERSION}/kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz
                        tar -xvzf kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz kubeseal
                        chmod +x kubeseal
                        sudo mv kubeseal /usr/local/bin/
                    '''
                }
            }
        }
        
        stage('Seal Secrets') {
            steps {
                withCredentials([
                    string(credentialsId: 'database-password', variable: 'DATABASE_PASSWORD'),
                    string(credentialsId: 'api-key', variable: 'API_KEY'),
                    string(credentialsId: 'jwt-secret', variable: 'JWT_SECRET'),
                    file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')
                ]) {
                    script {
                        sh '''
                            kubectl create secret generic app-secrets \
                              --from-literal=database-password="$DATABASE_PASSWORD" \
                              --from-literal=api-key="$API_KEY" \
                              --from-literal=jwt-secret="$JWT_SECRET" \
                              --namespace=production \
                              --dry-run=client \
                              -o yaml | kubeseal --format yaml > k8s/sealed-secrets.yaml
                        '''
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    script {
                        sh 'kubectl apply -f k8s/'
                    }
                }
            }
        }
    }
}
```

## Automation Scripts

### Secret Rotation Script
```bash
#!/bin/bash
# rotate-sealed-secrets.sh

set -e

NAMESPACE="${1:-default}"
SECRET_NAME="${2:-app-secrets}"

echo "Rotating sealed secret: $SECRET_NAME in namespace: $NAMESPACE"

# Check if kubeseal is available
if ! command -v kubeseal &> /dev/null; then
    echo "kubeseal not found. Please install it first."
    exit 1
fi

# Check if kubectl is configured
if ! kubectl cluster-info &> /dev/null; then
    echo "kubectl is not configured or cluster is not accessible"
    exit 1
fi

# Backup existing sealed secret
echo "Backing up existing sealed secret..."
kubectl get sealedsecret "$SECRET_NAME" -n "$NAMESPACE" -o yaml > "backup-$SECRET_NAME-$(date +%Y%m%d-%H%M%S).yaml"

# Generate new secrets (you would replace this with actual secret generation)
echo "Generating new secrets..."
NEW_PASSWORD=$(openssl rand -base64 32)
NEW_API_KEY="sk_$(openssl rand -hex 16)"
NEW_JWT_SECRET=$(openssl rand -base64 64)

# Create new sealed secret
echo "Creating new sealed secret..."
kubectl create secret generic "$SECRET_NAME" \
  --from-literal=password="$NEW_PASSWORD" \
  --from-literal=api-key="$NEW_API_KEY" \
  --from-literal=jwt-secret="$NEW_JWT_SECRET" \
  --namespace="$NAMESPACE" \
  --dry-run=client \
  -o yaml | kubeseal --format yaml > "new-$SECRET_NAME.yaml"

# Apply new sealed secret
echo "Applying new sealed secret..."
kubectl apply -f "new-$SECRET_NAME.yaml"

# Wait for secret to be created
echo "Waiting for secret to be decrypted..."
kubectl wait --for=condition=Ready secret/"$SECRET_NAME" -n "$NAMESPACE" --timeout=60s

# Restart deployments using this secret
echo "Restarting deployments using this secret..."
DEPLOYMENTS=$(kubectl get deployments -n "$NAMESPACE" -o json | jq -r '.items[] | select(.spec.template.spec.containers[].env[]?.valueFrom.secretKeyRef.name == "'$SECRET_NAME'") | .metadata.name')

for deployment in $DEPLOYMENTS; do
    echo "Restarting deployment: $deployment"
    kubectl rollout restart deployment/"$deployment" -n "$NAMESPACE"
done

echo "Secret rotation completed successfully!"
```

### Bulk Secret Management
```bash
#!/bin/bash
# bulk-seal-secrets.sh

set -e

SECRETS_DIR="${1:-secrets}"
OUTPUT_DIR="${2:-sealed-secrets}"

if [ ! -d "$SECRETS_DIR" ]; then
    echo "Secrets directory not found: $SECRETS_DIR"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "Processing secrets from $SECRETS_DIR to $OUTPUT_DIR"

find "$SECRETS_DIR" -name "*.yaml" -type f | while read -r secret_file; do
    filename=$(basename "$secret_file")
    output_file="$OUTPUT_DIR/sealed-$filename"
    
    echo "Processing: $secret_file -> $output_file"
    
    if kubeseal --format yaml < "$secret_file" > "$output_file"; then
        echo "  ✓ Successfully sealed $filename"
    else
        echo "  ✗ Failed to seal $filename"
    fi
done

echo "Bulk sealing completed!"
```

## Monitoring and Troubleshooting

### Health Checks
```bash
# Check controller status
kubectl get pods -n kube-system -l name=sealed-secrets-controller

# Check controller logs
kubectl logs -n kube-system -l name=sealed-secrets-controller

# Check sealed secret status
kubectl get sealedsecrets -A

# Check if secret was created from sealed secret
kubectl get secrets -A | grep <secret-name>

# Describe sealed secret for troubleshooting
kubectl describe sealedsecret <sealed-secret-name> -n <namespace>
```

### Common Issues and Solutions
```bash
# Issue: Cannot decrypt sealed secret
# Solution: Check if certificate matches
kubeseal --fetch-cert > current-cert.pem
# Compare with the certificate used to encrypt

# Issue: Secret not being created
# Solution: Check controller logs and events
kubectl logs -n kube-system -l name=sealed-secrets-controller --tail=50
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Issue: Wrong namespace or name binding
# Solution: Recreate with correct scope
kubeseal --scope cluster-wide < secret.yaml > sealed-secret.yaml

# Issue: Certificate rotation needed
# Solution: Re-encrypt all secrets with new certificate
find . -name "sealed-*.yaml" -exec sh -c 'kubectl create secret generic temp --from-literal=temp=temp --dry-run=client -o yaml | kubeseal --format yaml > {}' \;
```

### Monitoring with Prometheus
```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: sealed-secrets-controller
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: sealed-secrets-controller
  endpoints:
  - port: http
    interval: 30s
    path: /metrics
```

## Best Practices

### Security Best Practices
```bash
# 1. Use namespace scoping by default
# 2. Rotate certificates periodically
# 3. Backup certificates securely
# 4. Use RBAC to control access
# 5. Monitor sealed secret operations
# 6. Use GitOps workflow for secret management
# 7. Never commit unsealed secrets to Git
```

### GitOps Integration
```
Repository Structure:
├── apps/
│   ├── production/
│   │   ├── app-deployment.yaml
│   │   └── sealed-secrets.yaml
│   ├── staging/
│   │   ├── app-deployment.yaml
│   │   └── sealed-secrets.yaml
│   └── development/
│       ├── app-deployment.yaml
│       └── sealed-secrets.yaml
├── infrastructure/
│   └── sealed-secrets-controller.yaml
└── scripts/
    ├── seal-secrets.sh
    └── rotate-secrets.sh
```

### RBAC Configuration
```yaml
# sealed-secrets-rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: sealed-secrets-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]
- apiGroups: ["bitnami.com"]
  resources: ["sealedsecrets"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: sealed-secrets-writer
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list", "create", "update", "patch"]
- apiGroups: ["bitnami.com"]
  resources: ["sealedsecrets"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: sealed-secrets-developers
  namespace: development
subjects:
- kind: User
  name: developer@company.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: sealed-secrets-writer
  apiGroup: rbac.authorization.k8s.io
```

## Resources

- [Sealed Secrets GitHub Repository](https://github.com/bitnami-labs/sealed-secrets)
- [Sealed Secrets Documentation](https://sealed-secrets.netlify.app/)
- [Bitnami Sealed Secrets Helm Chart](https://github.com/bitnami-labs/sealed-secrets/tree/main/helm/sealed-secrets)
- [Kubernetes Secrets Documentation](https://kubernetes.io/docs/concepts/configuration/secret/)
- [GitOps with Sealed Secrets](https://blog.gitguardian.com/sealed-secrets/)
- [Sealed Secrets vs Other Solutions](https://blog.container-solutions.com/sealed-secrets-versus-vault)
- [Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [Sealed Secrets Tutorial](https://www.weave.works/blog/storing-secure-sealed-secrets-using-gitops)
- [ArgoCD with Sealed Secrets](https://argo-cd.readthedocs.io/en/stable/operator-manual/secret-management/)
- [Flux with Sealed Secrets](https://fluxcd.io/docs/guides/sealed-secrets/)