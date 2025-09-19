# Snyk

Snyk is a security platform that helps developers find, fix, and monitor vulnerabilities in open source dependencies, container images, and infrastructure as code.

## Installation

### CLI Installation
```bash
# Install via npm
npm install -g snyk

# Install via Homebrew (macOS)
brew tap snyk/tap
brew install snyk

# Install via curl
curl --compressed https://static.snyk.io/cli/latest/snyk-linux -o snyk
chmod +x ./snyk
sudo mv ./snyk /usr/local/bin/

# Install via binary download
curl -Lo ./snyk "https://github.com/snyk/snyk/releases/latest/download/snyk-linux"
chmod +x ./snyk
sudo mv ./snyk /usr/local/bin/

# Verify installation
snyk --version
```

### Docker
```bash
# Run Snyk in Docker
docker run --rm -it \
  -v $(pwd):/project \
  -w /project \
  snyk/snyk:latest test

# Alpine-based image
docker run --rm -it \
  -v $(pwd):/project \
  -w /project \
  snyk/snyk-cli:alpine test
```

## Authentication and Setup

### CLI Authentication
```bash
# Authenticate with Snyk
snyk auth

# Or authenticate with token
snyk config set api=your-api-token

# Verify authentication
snyk config get api

# Test authentication
snyk test --dry-run
```

### Configuration
```bash
# Set organization
snyk config set org=your-organization-id

# Set API endpoint (for on-premises)
snyk config set endpoint=https://snyk.mycompany.com/api

# View all configuration
snyk config
```

## Vulnerability Scanning

### Dependency Scanning
```bash
# Test for vulnerabilities in current project
snyk test

# Test specific package manager
snyk test --package-manager=npm
snyk test --package-manager=yarn
snyk test --package-manager=pip
snyk test --package-manager=gradle
snyk test --package-manager=maven

# Test with specific manifest file
snyk test --file=package.json
snyk test --file=requirements.txt
snyk test --file=pom.xml
snyk test --file=build.gradle

# Test with severity threshold
snyk test --severity-threshold=high
snyk test --severity-threshold=medium

# Test and monitor
snyk test && snyk monitor

# Test with JSON output
snyk test --json > vulnerability-report.json

# Test with SARIF output
snyk test --sarif > snyk-results.sarif
```

### Container Image Scanning
```bash
# Test Docker image
snyk container test node:16-alpine

# Test with Dockerfile
snyk container test myapp:latest --file=Dockerfile

# Test and get base image recommendations
snyk container test myapp:latest --print-deps

# Test with severity threshold
snyk container test myapp:latest --severity-threshold=high

# Monitor container image
snyk container monitor myapp:latest

# Test local Docker image
docker build -t myapp .
snyk container test myapp --file=Dockerfile
```

### Infrastructure as Code Scanning
```bash
# Test Terraform files
snyk iac test terraform/

# Test Kubernetes manifests
snyk iac test k8s/

# Test CloudFormation templates
snyk iac test cloudformation/

# Test with specific file
snyk iac test infrastructure.tf

# Test with rules
snyk iac test --rules=./custom-rules

# Test with SARIF output
snyk iac test --sarif > iac-results.sarif
```

### Code Quality Scanning
```bash
# Test for code issues
snyk code test

# Test specific files
snyk code test src/

# Test with SARIF output
snyk code test --sarif > code-results.sarif

# Test with severity threshold
snyk code test --severity-threshold=high
```

## Project Configuration

### .snyk Configuration File
```yaml
# .snyk
version: v1.0.0

# Language settings
language-settings:
  javascript:
    packageManager: npm
  python:
    packageManager: pip

# Ignore specific vulnerabilities
ignore:
  'SNYK-JS-LODASH-567746':
    - '*':
        reason: "False positive - not exploitable in our context"
        expires: '2024-12-31T23:59:59.999Z'
  'SNYK-PYTHON-URLLIB3-1533435':
    - '*':
        reason: "Patched in internal fork"

# Patches to apply
patches: {}

# Exclude paths from scanning
exclude:
  global:
    - node_modules/
    - '*.test.js'
    - test/
    - '**/*.spec.ts'
    - vendor/
    - .git/
```

### Container-specific Configuration
```yaml
# .snyk for container scanning
version: v1.0.0

# Container image configuration
image:
  base-image-remediation:
    advice: true

# Ignore vulnerabilities in base image
ignore:
  'SNYK-ALPINE311-OPENSSL-1090048':
    - '*':
        reason: "Base image vulnerability - waiting for upstream fix"
        expires: '2024-06-30T23:59:59.999Z'

# Exclude paths
exclude:
  global:
    - '/tmp/**'
    - '/var/cache/**'
    - '/usr/share/doc/**'
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/snyk.yml
name: Snyk Security

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  snyk:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run Snyk to check for vulnerabilities
      uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      with:
        args: --severity-threshold=high
    
    - name: Upload Snyk results to GitHub Code Scanning
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: snyk.sarif

  snyk-container:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t myapp:${{ github.sha }} .
    
    - name: Run Snyk to check Docker image for vulnerabilities
      uses: snyk/actions/docker@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      with:
        image: myapp:${{ github.sha }}
        args: --file=Dockerfile --severity-threshold=high

  snyk-iac:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Snyk to check Infrastructure as Code
      uses: snyk/actions/iac@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      with:
        args: --severity-threshold=medium
```

### GitLab CI
```yaml
# .gitlab-ci.yml
stages:
  - security

variables:
  SNYK_TOKEN: $SNYK_TOKEN

.snyk_template: &snyk_template
  image: snyk/snyk-cli:alpine
  before_script:
    - snyk auth $SNYK_TOKEN

snyk_test:
  <<: *snyk_template
  stage: security
  script:
    - snyk test --severity-threshold=high
    - snyk monitor
  artifacts:
    reports:
      junit: snyk-report.xml
    paths:
      - snyk-report.json
    expire_in: 1 week
  only:
    - merge_requests
    - main

snyk_container:
  <<: *snyk_template
  stage: security
  services:
    - docker:dind
  script:
    - docker build -t $CI_PROJECT_NAME:$CI_COMMIT_SHA .
    - snyk container test $CI_PROJECT_NAME:$CI_COMMIT_SHA --file=Dockerfile
  only:
    - merge_requests
    - main

snyk_iac:
  <<: *snyk_template
  stage: security
  script:
    - snyk iac test --severity-threshold=medium --sarif > snyk-iac.sarif
  artifacts:
    reports:
      sast: snyk-iac.sarif
  only:
    - merge_requests
    - main
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    environment {
        SNYK_TOKEN = credentials('snyk-api-token')
    }
    
    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    sh 'npm ci'
                }
            }
        }
        
        stage('Snyk Dependency Scan') {
            steps {
                script {
                    sh '''
                        snyk test --severity-threshold=high --json > snyk-deps.json || true
                        snyk monitor
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'snyk-deps.json', fingerprint: true
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t myapp:${BUILD_NUMBER} .'
                }
            }
        }
        
        stage('Snyk Container Scan') {
            steps {
                script {
                    sh '''
                        snyk container test myapp:${BUILD_NUMBER} \
                            --file=Dockerfile \
                            --severity-threshold=high \
                            --json > snyk-container.json || true
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'snyk-container.json', fingerprint: true
                }
            }
        }
        
        stage('Snyk IaC Scan') {
            steps {
                script {
                    sh '''
                        snyk iac test infrastructure/ \
                            --severity-threshold=medium \
                            --json > snyk-iac.json || true
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'snyk-iac.json', fingerprint: true
                }
            }
        }
    }
    
    post {
        always {
            // Parse Snyk results and create reports
            script {
                def snykResults = readJSON file: 'snyk-deps.json'
                currentBuild.description = "Vulnerabilities: ${snykResults.uniqueCount}"
            }
        }
    }
}
```

## Advanced Usage

### Custom Policies
```json
{
  "version": "v1.0.0",
  "ignore": {},
  "patches": {},
  "policy": {
    "rules": [
      {
        "id": "custom-rule-1",
        "severity": "high",
        "type": "vulnerability",
        "conditions": [
          {
            "attribute": "package",
            "operator": "equals",
            "value": "lodash"
          },
          {
            "attribute": "version",
            "operator": "semver-range",
            "value": "<4.17.12"
          }
        ],
        "action": "fail"
      }
    ]
  }
}
```

### API Integration
```python
import requests
import json
from datetime import datetime, timedelta

class SnykAPI:
    def __init__(self, api_token, org_id=None):
        self.api_token = api_token
        self.org_id = org_id
        self.base_url = "https://snyk.io/api/v1"
        self.headers = {
            "Authorization": f"token {api_token}",
            "Content-Type": "application/json"
        }
    
    def get_projects(self):
        """Get all projects in organization"""
        url = f"{self.base_url}/org/{self.org_id}/projects"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_project_issues(self, project_id):
        """Get issues for a specific project"""
        url = f"{self.base_url}/org/{self.org_id}/project/{project_id}/issues"
        response = requests.post(url, headers=self.headers, json={
            "filters": {
                "severities": ["high", "critical"],
                "types": ["vuln"]
            }
        })
        response.raise_for_status()
        return response.json()
    
    def get_vulnerabilities_summary(self):
        """Get vulnerability summary across all projects"""
        projects = self.get_projects()
        summary = {
            "total_projects": len(projects["projects"]),
            "vulnerabilities": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "projects_with_issues": 0
        }
        
        for project in projects["projects"]:
            try:
                issues = self.get_project_issues(project["id"])
                if issues["issues"]:
                    summary["projects_with_issues"] += 1
                    for issue in issues["issues"]:
                        severity = issue["issueData"]["severity"]
                        summary["vulnerabilities"][severity] += 1
            except Exception as e:
                print(f"Error getting issues for project {project['name']}: {e}")
        
        return summary
    
    def ignore_issue(self, org_id, project_id, issue_id, reason, expires=None):
        """Ignore a specific issue"""
        url = f"{self.base_url}/org/{org_id}/project/{project_id}/ignore/{issue_id}"
        
        data = {
            "ignorePath": "*",
            "reason": reason,
            "reasonType": "not-vulnerable"
        }
        
        if expires:
            data["expires"] = expires
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def create_webhook(self, url, secret=None):
        """Create webhook for notifications"""
        webhook_url = f"{self.base_url}/org/{self.org_id}/webhooks"
        
        data = {
            "url": url,
            "secret": secret
        }
        
        response = requests.post(webhook_url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

# Usage
snyk_api = SnykAPI("your-api-token", "your-org-id")
summary = snyk_api.get_vulnerabilities_summary()
print(f"Total vulnerabilities: {summary['vulnerabilities']}")
```

### Webhook Handler
```python
from flask import Flask, request, jsonify
import hashlib
import hmac
import json

app = Flask(__name__)

class SnykWebhookHandler:
    def __init__(self, secret):
        self.secret = secret
    
    def verify_signature(self, payload, signature):
        """Verify webhook signature"""
        expected_signature = hmac.new(
            self.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def handle_vulnerability_alert(self, data):
        """Handle new vulnerability alert"""
        project = data.get("project", {})
        newIssues = data.get("newIssues", [])
        
        print(f"New vulnerabilities in {project.get('name')}: {len(newIssues)}")
        
        for issue in newIssues:
            severity = issue.get("issueData", {}).get("severity")
            title = issue.get("issueData", {}).get("title")
            package = issue.get("pkgName")
            
            print(f"  {severity.upper()}: {title} in {package}")
            
            # Send alert to Slack, email, etc.
            if severity in ["high", "critical"]:
                self.send_critical_alert(project["name"], issue)
    
    def send_critical_alert(self, project_name, issue):
        """Send critical vulnerability alert"""
        # Implementation for sending alerts
        print(f"CRITICAL ALERT: {project_name} - {issue['issueData']['title']}")

webhook_handler = SnykWebhookHandler("your-webhook-secret")

@app.route('/webhook/snyk', methods=['POST'])
def snyk_webhook():
    signature = request.headers.get('X-Snyk-Signature')
    payload = request.get_data(as_text=True)
    
    if not webhook_handler.verify_signature(payload, signature):
        return jsonify({"error": "Invalid signature"}), 401
    
    data = request.get_json()
    
    if data.get("newIssues"):
        webhook_handler.handle_vulnerability_alert(data)
    
    return jsonify({"status": "processed"})

if __name__ == '__main__':
    app.run(port=5000)
```

## Kubernetes Integration

### Operator Deployment
```yaml
# snyk-operator.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: snyk-system
---
apiVersion: v1
kind: Secret
metadata:
  name: snyk-secret
  namespace: snyk-system
type: Opaque
data:
  integrationId: <base64-encoded-integration-id>
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: snyk-operator
  namespace: snyk-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: snyk-operator
  template:
    metadata:
      labels:
        app: snyk-operator
    spec:
      serviceAccountName: snyk-operator
      containers:
      - name: snyk-operator
        image: snyk/kubernetes-operator:latest
        env:
        - name: INTEGRATION_ID
          valueFrom:
            secretKeyRef:
              name: snyk-secret
              key: integrationId
        - name: CLUSTER_NAME
          value: "production-cluster"
        - name: WORKERS_COUNT
          value: "10"
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: snyk-operator
  namespace: snyk-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: snyk-operator
rules:
- apiGroups: [""]
  resources: ["pods", "nodes", "namespaces"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets", "daemonsets", "statefulsets"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["batch"]
  resources: ["jobs", "cronjobs"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: snyk-operator
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: snyk-operator
subjects:
- kind: ServiceAccount
  name: snyk-operator
  namespace: snyk-system
```

### Admission Controller
```yaml
# snyk-admission-controller.yaml
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingAdmissionWebhook
metadata:
  name: snyk-admission-controller
webhooks:
- name: snyk.admission.controller
  clientConfig:
    service:
      name: snyk-admission-controller
      namespace: snyk-system
      path: /mutate
  rules:
  - operations: ["CREATE", "UPDATE"]
    apiGroups: [""]
    apiVersions: ["v1"]
    resources: ["pods"]
  admissionReviewVersions: ["v1", "v1beta1"]
  sideEffects: None
  failurePolicy: Fail
---
apiVersion: v1
kind: Service
metadata:
  name: snyk-admission-controller
  namespace: snyk-system
spec:
  selector:
    app: snyk-admission-controller
  ports:
  - port: 443
    targetPort: 8443
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: snyk-admission-controller
  namespace: snyk-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: snyk-admission-controller
  template:
    metadata:
      labels:
        app: snyk-admission-controller
    spec:
      containers:
      - name: admission-controller
        image: snyk/admission-controller:latest
        ports:
        - containerPort: 8443
        env:
        - name: SNYK_TOKEN
          valueFrom:
            secretKeyRef:
              name: snyk-secret
              key: token
        - name: TLS_CERT_FILE
          value: /etc/certs/tls.crt
        - name: TLS_PRIVATE_KEY_FILE
          value: /etc/certs/tls.key
        volumeMounts:
        - name: certs
          mountPath: /etc/certs
          readOnly: true
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
      volumes:
      - name: certs
        secret:
          secretName: snyk-admission-controller-certs
```

## Monitoring and Reporting

### Custom Dashboard
```python
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

class SnykDashboard:
    def __init__(self, snyk_api):
        self.api = snyk_api
    
    def generate_vulnerability_report(self):
        """Generate comprehensive vulnerability report"""
        projects = self.api.get_projects()
        
        report_data = []
        for project in projects["projects"]:
            try:
                issues = self.api.get_project_issues(project["id"])
                
                vulnerabilities = {"critical": 0, "high": 0, "medium": 0, "low": 0}
                for issue in issues.get("issues", []):
                    severity = issue["issueData"]["severity"]
                    vulnerabilities[severity] += 1
                
                report_data.append({
                    "project": project["name"],
                    "language": project.get("language", "Unknown"),
                    "critical": vulnerabilities["critical"],
                    "high": vulnerabilities["high"],
                    "medium": vulnerabilities["medium"],
                    "low": vulnerabilities["low"],
                    "total": sum(vulnerabilities.values())
                })
            except Exception as e:
                print(f"Error processing {project['name']}: {e}")
        
        df = pd.DataFrame(report_data)
        return df
    
    def create_severity_chart(self, df):
        """Create severity distribution chart"""
        severity_totals = df[["critical", "high", "medium", "low"]].sum()
        
        plt.figure(figsize=(10, 6))
        colors = ["#d63384", "#fd7e14", "#ffc107", "#198754"]
        severity_totals.plot(kind="bar", color=colors)
        plt.title("Vulnerability Distribution by Severity")
        plt.xlabel("Severity")
        plt.ylabel("Count")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig("vulnerability_severity.png")
        plt.show()
    
    def create_project_comparison(self, df):
        """Create project comparison chart"""
        top_projects = df.nlargest(10, "total")
        
        plt.figure(figsize=(12, 8))
        x = range(len(top_projects))
        width = 0.2
        
        plt.bar([i - 1.5*width for i in x], top_projects["critical"], width, label="Critical", color="#d63384")
        plt.bar([i - 0.5*width for i in x], top_projects["high"], width, label="High", color="#fd7e14")
        plt.bar([i + 0.5*width for i in x], top_projects["medium"], width, label="Medium", color="#ffc107")
        plt.bar([i + 1.5*width for i in x], top_projects["low"], width, label="Low", color="#198754")
        
        plt.xlabel("Projects")
        plt.ylabel("Vulnerability Count")
        plt.title("Top 10 Projects by Vulnerability Count")
        plt.xticks(x, top_projects["project"], rotation=45, ha="right")
        plt.legend()
        plt.tight_layout()
        plt.savefig("project_comparison.png")
        plt.show()
    
    def generate_html_report(self, df):
        """Generate HTML report"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Snyk Security Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .header { background-color: #4c1; color: white; padding: 20px; }
                .summary { background-color: #f8f9fa; padding: 20px; margin: 20px 0; }
                .critical { color: #d63384; font-weight: bold; }
                .high { color: #fd7e14; font-weight: bold; }
                .medium { color: #ffc107; font-weight: bold; }
                .low { color: #198754; font-weight: bold; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Snyk Security Report</h1>
                <p>Generated on: {timestamp}</p>
            </div>
            
            <div class="summary">
                <h2>Summary</h2>
                <p>Total Projects: {total_projects}</p>
                <p>Total Vulnerabilities: {total_vulns}</p>
                <ul>
                    <li class="critical">Critical: {critical}</li>
                    <li class="high">High: {high}</li>
                    <li class="medium">Medium: {medium}</li>
                    <li class="low">Low: {low}</li>
                </ul>
            </div>
            
            <h2>Project Details</h2>
            {table}
        </body>
        </html>
        """
        
        summary = {
            "total_projects": len(df),
            "total_vulns": df["total"].sum(),
            "critical": df["critical"].sum(),
            "high": df["high"].sum(),
            "medium": df["medium"].sum(),
            "low": df["low"].sum(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "table": df.to_html(classes="table table-striped", escape=False)
        }
        
        html_content = html_template.format(**summary)
        
        with open("snyk_report.html", "w") as f:
            f.write(html_content)
        
        print("HTML report generated: snyk_report.html")

# Usage
dashboard = SnykDashboard(snyk_api)
df = dashboard.generate_vulnerability_report()
dashboard.create_severity_chart(df)
dashboard.create_project_comparison(df)
dashboard.generate_html_report(df)
```

## Best Practices

### Security Policy Configuration
```yaml
# .snyk policy configuration
version: v1.0.0

# Fail builds on high/critical vulnerabilities
fail-on:
  - high
  - critical

# Language-specific settings
language-settings:
  javascript:
    packageManager: npm
    devDependencies: false
  python:
    packageManager: pip
    includeDevDeps: false

# Global ignores (use sparingly)
ignore:
  # Only ignore after careful review
  'SNYK-JS-EXAMPLE-123456':
    - '*':
        reason: "Not exploitable in our use case"
        expires: '2024-06-30T23:59:59.999Z'
        created: '2024-01-15T10:30:00.000Z'

# Patches (automatically applied fixes)
patches: {}
```

### Automation Scripts
```bash
#!/bin/bash
# snyk-scan.sh - Comprehensive security scanning

set -e

PROJECT_NAME="myapp"
SEVERITY_THRESHOLD="medium"
REPORT_DIR="./security-reports"

# Create reports directory
mkdir -p "$REPORT_DIR"

echo "Starting Snyk security scan for $PROJECT_NAME..."

# Dependency scanning
echo "Scanning dependencies..."
snyk test \
  --severity-threshold="$SEVERITY_THRESHOLD" \
  --json > "$REPORT_DIR/dependencies.json" || true

# Container scanning (if Dockerfile exists)
if [ -f "Dockerfile" ]; then
    echo "Scanning container image..."
    docker build -t "$PROJECT_NAME:scan" .
    snyk container test "$PROJECT_NAME:scan" \
      --file=Dockerfile \
      --severity-threshold="$SEVERITY_THRESHOLD" \
      --json > "$REPORT_DIR/container.json" || true
fi

# Infrastructure as Code scanning
if [ -d "terraform" ] || [ -d "k8s" ] || [ -f "*.tf" ]; then
    echo "Scanning Infrastructure as Code..."
    snyk iac test \
      --severity-threshold="$SEVERITY_THRESHOLD" \
      --json > "$REPORT_DIR/iac.json" || true
fi

# Code quality scanning
echo "Scanning code quality..."
snyk code test \
  --severity-threshold="$SEVERITY_THRESHOLD" \
  --json > "$REPORT_DIR/code.json" || true

# Generate summary report
echo "Generating summary report..."
python3 -c "
import json
import os

report_dir = '$REPORT_DIR'
files = ['dependencies.json', 'container.json', 'iac.json', 'code.json']

summary = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}

for file in files:
    file_path = os.path.join(report_dir, file)
    if os.path.exists(file_path):
        with open(file_path) as f:
            try:
                data = json.load(f)
                if 'vulnerabilities' in data:
                    for vuln in data['vulnerabilities']:
                        severity = vuln.get('severity', 'unknown')
                        if severity in summary:
                            summary[severity] += 1
            except:
                pass

print(f'Security Scan Summary:')
print(f'Critical: {summary[\"critical\"]}')
print(f'High: {summary[\"high\"]}')
print(f'Medium: {summary[\"medium\"]}')
print(f'Low: {summary[\"low\"]}')

# Exit with error if critical or high vulnerabilities found
exit_code = 1 if summary['critical'] > 0 or summary['high'] > 0 else 0
exit(exit_code)
"

echo "Scan completed. Reports saved to $REPORT_DIR"
```

## Resources

- [Snyk Documentation](https://docs.snyk.io/)
- [Snyk CLI Reference](https://docs.snyk.io/snyk-cli)
- [Snyk API Documentation](https://snyk.docs.apiary.io/)
- [Snyk Kubernetes Operator](https://github.com/snyk/kubernetes-operator)
- [Security Best Practices](https://snyk.io/learn/)
- [Vulnerability Database](https://snyk.io/vuln/)
- [Snyk Advisor](https://snyk.io/advisor/)
- [Community Support](https://support.snyk.io/)
- [Snyk GitHub Actions](https://github.com/snyk/actions)
- [Snyk Training](https://learn.snyk.io/)