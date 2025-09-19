# Trivy

## Overview

Trivy is a comprehensive vulnerability scanner for containers, file systems, and Git repositories. It's designed to be simple, fast, and reliable for finding vulnerabilities in application dependencies, operating system packages, and infrastructure as code.

## Key Features

- **Multi-Target Scanning**: Containers, filesystems, Git repos, Kubernetes clusters
- **Fast Performance**: High-speed scanning with offline capability
- **Comprehensive Database**: CVE, GitHub Security Advisories, and more
- **Multiple Formats**: JSON, SARIF, GitHub, GitLab output formats
- **CI/CD Integration**: Easy integration with pipelines and workflows

## Common Use Cases

### Container Image Scanning
```bash
# Scan Docker image
trivy image nginx:latest

# Scan with specific severity
trivy image --severity HIGH,CRITICAL nginx:latest

# Output to JSON
trivy image --format json nginx:latest > scan-results.json

# Scan local Docker image
docker build -t myapp:latest .
trivy image myapp:latest
```

### Filesystem Scanning
```bash
# Scan current directory
trivy fs .

# Scan specific directory
trivy fs /path/to/project

# Scan only specific file types
trivy fs --scanners vuln,secret,config .

# Exclude specific paths
trivy fs --skip-dirs node_modules,vendor .
```

### Git Repository Scanning
```bash
# Scan remote repository
trivy repo https://github.com/example/myproject

# Scan specific branch or commit
trivy repo --branch develop https://github.com/example/myproject
trivy repo --commit abc123 https://github.com/example/myproject

# Scan for secrets only
trivy repo --scanners secret https://github.com/example/myproject
```

### Kubernetes Cluster Scanning
```bash
# Scan entire cluster
trivy k8s cluster

# Scan specific namespace
trivy k8s --namespace myapp cluster

# Scan specific workload
trivy k8s deployment/myapp

# Output compliance report
trivy k8s --compliance k8s-cis cluster
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Trivy Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t myapp:${{ github.sha }} .
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'myapp:${{ github.sha }}'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
```

### GitLab CI
```yaml
stages:
  - security

trivy-scan:
  stage: security
  image: aquasecurity/trivy:latest
  script:
    - trivy image --format template --template "@contrib/gitlab.tpl" $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  artifacts:
    reports:
      container_scanning: gl-container-scanning-report.json
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    docker.build("myapp:${env.BUILD_ID}")
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    sh "trivy image --format json --output trivy-report.json myapp:${env.BUILD_ID}"
                    
                    // Fail build on high/critical vulnerabilities
                    def exitCode = sh(
                        script: "trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:${env.BUILD_ID}",
                        returnStatus: true
                    )
                    
                    if (exitCode != 0) {
                        error "High or critical vulnerabilities found!"
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-report.json'
                }
            }
        }
    }
}
```

## Configuration

### Custom Configuration File
```yaml
# trivy.yaml
format: json
output: scan-results.json
severity:
  - HIGH
  - CRITICAL
vulnerability:
  type:
    - os
    - library
ignore-unfixed: true
```

```bash
# Use configuration file
trivy image --config trivy.yaml nginx:latest
```

### Ignore Specific Vulnerabilities
```yaml
# .trivyignore
CVE-2021-12345
CVE-2021-67890
# Ignore specific package
CVE-2021-11111 # pkg:npm/lodash@4.17.20
```

## Advanced Features

### Custom Policies
```rego
# custom-policy.rego
package trivy

deny[msg] {
    input.image.config.user == "root"
    msg := "Container should not run as root user"
}

deny[msg] {
    input.image.config.exposed_ports["22/tcp"]
    msg := "SSH port should not be exposed"
}
```

```bash
# Scan with custom policy
trivy image --policy custom-policy.rego nginx:latest
```

### Database Management
```bash
# Update vulnerability database
trivy image --download-db-only

# Use offline mode
trivy image --offline nginx:latest

# Skip database update
trivy image --skip-update nginx:latest
```

## Monitoring and Reporting

### Automated Reporting
```bash
#!/bin/bash
# Daily security scan script

DATE=$(date +%Y%m%d)
REPORT_DIR="/reports/$DATE"
mkdir -p "$REPORT_DIR"

# Scan all running containers
docker ps --format "table {{.Image}}" | tail -n +2 | while read image; do
    echo "Scanning $image..."
    trivy image --format json "$image" > "$REPORT_DIR/${image//\//_}.json"
done

# Generate summary report
trivy image --format table --severity HIGH,CRITICAL $(docker ps --format "{{.Image}}" | sort | uniq) > "$REPORT_DIR/summary.txt"
```

## Best Practices

- Integrate scanning into CI/CD pipelines early
- Set up automated daily scans for running containers
- Use severity filtering to focus on critical issues
- Maintain ignore files for known acceptable risks
- Regular database updates for latest vulnerability data
- Combine with other security tools for comprehensive coverage
- Monitor and alert on new vulnerabilities in production

## Great Resources

- [Trivy Official Documentation](https://aquasecurity.github.io/trivy/) - Comprehensive documentation and guides
- [Trivy GitHub Repository](https://github.com/aquasecurity/trivy) - Source code, issues, and latest releases
- [Trivy Operator](https://github.com/aquasecurity/trivy-operator) - Kubernetes-native security toolkit
- [Trivy Action](https://github.com/aquasecurity/trivy-action) - GitHub Actions integration
- [Container Security Best Practices](https://aquasecurity.github.io/trivy/latest/docs/coverage/language/) - Language-specific scanning guidance
- [Trivy DB](https://github.com/aquasecurity/trivy-db) - Vulnerability database information
- [DevSec Hardening Framework](https://dev-sec.io/) - Complementary security hardening tools