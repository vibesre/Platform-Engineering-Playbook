# SonarQube

SonarQube is a static code analysis tool that continuously inspects code quality and security vulnerabilities in your codebase, providing detailed reports and metrics.

## Installation

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgresql:
    image: postgres:13
    container_name: sonarqube-db
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
      POSTGRES_DB: sonarqube
    volumes:
      - postgresql_data:/var/lib/postgresql/data
    networks:
      - sonarqube

  sonarqube:
    image: sonarqube:10.1-community
    container_name: sonarqube
    depends_on:
      - postgresql
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://postgresql:5432/sonarqube
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: sonar
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_logs:/opt/sonarqube/logs
      - sonarqube_extensions:/opt/sonarqube/extensions
    ports:
      - "9000:9000"
    networks:
      - sonarqube
    ulimits:
      nofile:
        soft: 131072
        hard: 131072
      nproc: 8192

volumes:
  postgresql_data:
  sonarqube_data:
  sonarqube_logs:
  sonarqube_extensions:

networks:
  sonarqube:
    driver: bridge
```

### Kubernetes Deployment
```yaml
# sonarqube-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: sonarqube
---
# postgresql.yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgresql-secret
  namespace: sonarqube
type: Opaque
data:
  postgres-password: c29uYXI=  # sonar
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgresql-pvc
  namespace: sonarqube
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql
  namespace: sonarqube
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgresql
        image: postgres:13
        env:
        - name: POSTGRES_USER
          value: sonar
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgresql-secret
              key: postgres-password
        - name: POSTGRES_DB
          value: sonarqube
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgresql-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 1000m
            memory: 1Gi
      volumes:
      - name: postgresql-storage
        persistentVolumeClaim:
          claimName: postgresql-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgresql-service
  namespace: sonarqube
spec:
  selector:
    app: postgresql
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP
---
# sonarqube.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sonarqube-config
  namespace: sonarqube
data:
  sonar.properties: |
    sonar.jdbc.url=jdbc:postgresql://postgresql-service:5432/sonarqube
    sonar.jdbc.username=sonar
    sonar.web.host=0.0.0.0
    sonar.web.port=9000
    sonar.web.context=/
    sonar.ce.workerCount=4
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: sonarqube-data-pvc
  namespace: sonarqube
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: sonarqube-logs-pvc
  namespace: sonarqube
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sonarqube
  namespace: sonarqube
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sonarqube
  template:
    metadata:
      labels:
        app: sonarqube
    spec:
      initContainers:
      - name: init-sysctl
        image: busybox:1.35
        command: ['sh', '-c']
        args:
        - |
          sysctl -w vm.max_map_count=524288
          sysctl -w fs.file-max=131072
        securityContext:
          privileged: true
      containers:
      - name: sonarqube
        image: sonarqube:10.1-community
        env:
        - name: SONAR_JDBC_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgresql-secret
              key: postgres-password
        ports:
        - containerPort: 9000
        volumeMounts:
        - name: sonarqube-data
          mountPath: /opt/sonarqube/data
        - name: sonarqube-logs
          mountPath: /opt/sonarqube/logs
        - name: sonarqube-config
          mountPath: /opt/sonarqube/conf/sonar.properties
          subPath: sonar.properties
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        livenessProbe:
          httpGet:
            path: /api/system/status
            port: 9000
          initialDelaySeconds: 120
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /api/system/status
            port: 9000
          initialDelaySeconds: 60
          periodSeconds: 10
      volumes:
      - name: sonarqube-data
        persistentVolumeClaim:
          claimName: sonarqube-data-pvc
      - name: sonarqube-logs
        persistentVolumeClaim:
          claimName: sonarqube-logs-pvc
      - name: sonarqube-config
        configMap:
          name: sonarqube-config
---
apiVersion: v1
kind: Service
metadata:
  name: sonarqube-service
  namespace: sonarqube
spec:
  selector:
    app: sonarqube
  ports:
  - port: 9000
    targetPort: 9000
  type: LoadBalancer
```

## Scanner Installation

### SonarScanner CLI
```bash
# Download and install SonarScanner
curl -O https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip
unzip sonar-scanner-cli-4.8.0.2856-linux.zip
sudo mv sonar-scanner-4.8.0.2856-linux /opt/sonar-scanner
sudo ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/local/bin/sonar-scanner

# Verify installation
sonar-scanner --version
```

### Configuration
```properties
# sonar-project.properties
sonar.projectKey=my-project
sonar.projectName=My Project
sonar.projectVersion=1.0

# Source directories
sonar.sources=src
sonar.tests=tests
sonar.exclusions=node_modules/**,dist/**,build/**,*.min.js
sonar.test.inclusions=**/*test*/**,**/*Test*

# SonarQube server
sonar.host.url=http://localhost:9000
sonar.login=your-token-here

# Language-specific settings
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.python.coverage.reportPaths=coverage.xml
sonar.java.binaries=target/classes
sonar.java.test.binaries=target/test-classes
sonar.java.coveragePlugin=jacoco
sonar.jacoco.reportPaths=target/jacoco.exec

# Code analysis settings
sonar.qualitygate.wait=true
sonar.qualitygate.timeout=300
```

## Project Setup and Configuration

### Basic Project Analysis
```bash
# Create project configuration
cat > sonar-project.properties << EOF
sonar.projectKey=my-application
sonar.projectName=My Application
sonar.projectVersion=1.0.0
sonar.sources=src
sonar.tests=tests
sonar.exclusions=node_modules/**,build/**,dist/**
sonar.host.url=http://localhost:9000
sonar.login=your-auth-token
EOF

# Run analysis
sonar-scanner

# Or with specific properties
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-auth-token
```

### Multi-Module Project
```properties
# Root project properties
sonar.projectKey=multi-module-project
sonar.projectName=Multi Module Project
sonar.projectVersion=1.0.0

# Module definitions
sonar.modules=backend,frontend,shared

# Backend module
backend.sonar.projectName=Backend
backend.sonar.sources=backend/src
backend.sonar.tests=backend/tests
backend.sonar.java.binaries=backend/target/classes
backend.sonar.exclusions=**/*generated*/**

# Frontend module
frontend.sonar.projectName=Frontend
frontend.sonar.sources=frontend/src
frontend.sonar.tests=frontend/tests
frontend.sonar.exclusions=node_modules/**,build/**
frontend.sonar.javascript.lcov.reportPaths=frontend/coverage/lcov.info

# Shared module
shared.sonar.projectName=Shared
shared.sonar.sources=shared/src
shared.sonar.tests=shared/tests
```

### Language-Specific Configuration

#### Java/Maven
```xml
<!-- pom.xml -->
<properties>
    <sonar.projectKey>java-project</sonar.projectKey>
    <sonar.projectName>Java Project</sonar.projectName>
    <sonar.host.url>http://localhost:9000</sonar.host.url>
    <sonar.login>your-auth-token</sonar.login>
    <sonar.coverage.jacoco.xmlReportPaths>target/site/jacoco/jacoco.xml</sonar.coverage.jacoco.xmlReportPaths>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.sonarsource.scanner.maven</groupId>
            <artifactId>sonar-maven-plugin</artifactId>
            <version>3.9.1.2184</version>
        </plugin>
        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.8</version>
            <executions>
                <execution>
                    <id>prepare-agent</id>
                    <goals>
                        <goal>prepare-agent</goal>
                    </goals>
                </execution>
                <execution>
                    <id>report</id>
                    <phase>test</phase>
                    <goals>
                        <goal>report</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

```bash
# Run Maven analysis
mvn clean verify sonar:sonar
```

#### Node.js/JavaScript
```json
{
  "name": "my-node-app",
  "scripts": {
    "test": "jest --coverage",
    "sonar": "sonar-scanner",
    "test:sonar": "npm test && npm run sonar"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "@jest/types": "^29.0.0"
  },
  "jest": {
    "collectCoverage": true,
    "coverageDirectory": "coverage",
    "coverageReporters": ["lcov", "text", "html"],
    "testMatch": ["**/__tests__/**/*.js", "**/?(*.)+(spec|test).js"]
  }
}
```

```properties
# sonar-project.properties for Node.js
sonar.projectKey=node-project
sonar.projectName=Node.js Project
sonar.sources=src
sonar.tests=tests,src/**/__tests__
sonar.exclusions=node_modules/**,coverage/**,dist/**
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.testExecutionReportPaths=test-report.xml
```

#### Python
```properties
# sonar-project.properties for Python
sonar.projectKey=python-project
sonar.projectName=Python Project
sonar.sources=src
sonar.tests=tests
sonar.exclusions=**/__pycache__/**,**/venv/**,**/.pytest_cache/**
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.xunit.reportPath=test-results.xml
```

```python
# pytest.ini or setup.cfg
[tool:pytest]
addopts = --cov=src --cov-report=xml --junitxml=test-results.xml
testpaths = tests
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/sonarqube.yml
name: SonarQube Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0  # Shallow clones should be disabled for better analysis
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm run test:coverage
    
    - name: SonarQube Scan
      uses: sonarqube-quality-gate-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      with:
        projectBaseDir: .
        args: >
          -Dsonar.projectKey=${{ github.repository }}
          -Dsonar.organization=my-org
          -Dsonar.host.url=https://sonarqube.company.com
          -Dsonar.login=${{ secrets.SONAR_TOKEN }}
          -Dsonar.sources=src
          -Dsonar.tests=tests
          -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info
          -Dsonar.coverage.exclusions=**/*.test.js,**/*.spec.js
    
    - name: Check Quality Gate
      run: |
        # Wait for Quality Gate result
        QUALITY_GATE_STATUS=$(curl -s -u ${{ secrets.SONAR_TOKEN }}: \
          "https://sonarqube.company.com/api/qualitygates/project_status?projectKey=${{ github.repository }}" \
          | jq -r '.projectStatus.status')
        
        echo "Quality Gate Status: $QUALITY_GATE_STATUS"
        
        if [ "$QUALITY_GATE_STATUS" != "OK" ]; then
          echo "Quality Gate failed"
          exit 1
        fi
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    tools {
        nodejs 'NodeJS-18'
        maven 'Maven-3.8'
    }
    
    environment {
        SONAR_TOKEN = credentials('sonar-token')
        SONAR_HOST_URL = 'https://sonarqube.company.com'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                script {
                    if (fileExists('package.json')) {
                        sh 'npm ci'
                        sh 'npm run build'
                    } else if (fileExists('pom.xml')) {
                        sh 'mvn clean compile'
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    if (fileExists('package.json')) {
                        sh 'npm run test:coverage'
                    } else if (fileExists('pom.xml')) {
                        sh 'mvn test jacoco:report'
                    }
                }
            }
            post {
                always {
                    publishTestResults testResultsPattern: '**/test-results.xml'
                    publishCoverage adapters: [
                        jacocoAdapter('**/jacoco.xml'),
                        lcovAdapter('**/lcov.info')
                    ]
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        if (fileExists('package.json')) {
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=${env.JOB_NAME} \
                                -Dsonar.projectName="${env.JOB_NAME}" \
                                -Dsonar.sources=src \
                                -Dsonar.tests=tests \
                                -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info \
                                -Dsonar.exclusions=node_modules/**,build/**,dist/**
                            """
                        } else if (fileExists('pom.xml')) {
                            sh 'mvn sonar:sonar'
                        }
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            emailext (
                subject: "SonarQube Analysis Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "SonarQube analysis failed for ${env.BUILD_URL}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}
```

### GitLab CI
```yaml
# .gitlab-ci.yml
stages:
  - test
  - sonarqube
  - quality-gate

variables:
  SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"
  GIT_DEPTH: "0"

cache:
  paths:
    - .sonar/cache

test:
  stage: test
  image: node:18
  script:
    - npm ci
    - npm run test:coverage
  artifacts:
    reports:
      junit: test-results.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/
    expire_in: 1 hour

sonarqube-check:
  stage: sonarqube
  image: 
    name: sonarsource/sonar-scanner-cli:latest
    entrypoint: [""]
  variables:
    SONAR_HOST_URL: "https://sonarqube.company.com"
    SONAR_TOKEN: "$SONAR_TOKEN"
  script:
    - sonar-scanner
      -Dsonar.projectKey=$CI_PROJECT_PATH_SLUG
      -Dsonar.projectName="$CI_PROJECT_NAME"
      -Dsonar.sources=src
      -Dsonar.tests=tests
      -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info
      -Dsonar.qualitygate.wait=true
  dependencies:
    - test
  only:
    - merge_requests
    - main
    - develop
```

## API Integration and Automation

### Python SonarQube API Client
```python
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

class SonarQubeAPI:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.auth = (token, '')
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def get_projects(self) -> List[Dict]:
        """Get all projects"""
        response = self.session.get(f"{self.base_url}/api/projects/search")
        response.raise_for_status()
        return response.json()['components']
    
    def get_project_quality_gate(self, project_key: str) -> Dict:
        """Get quality gate status for project"""
        response = self.session.get(
            f"{self.base_url}/api/qualitygates/project_status",
            params={'projectKey': project_key}
        )
        response.raise_for_status()
        return response.json()
    
    def get_project_measures(self, project_key: str, metrics: List[str]) -> Dict:
        """Get specific measures for a project"""
        response = self.session.get(
            f"{self.base_url}/api/measures/component",
            params={
                'component': project_key,
                'metricKeys': ','.join(metrics)
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_project_issues(self, project_key: str, severity: Optional[str] = None) -> List[Dict]:
        """Get issues for a project"""
        params = {'componentKeys': project_key, 'ps': 500}
        if severity:
            params['severities'] = severity
        
        response = self.session.get(f"{self.base_url}/api/issues/search", params=params)
        response.raise_for_status()
        return response.json()['issues']
    
    def create_quality_gate(self, name: str) -> Dict:
        """Create a new quality gate"""
        response = self.session.post(
            f"{self.base_url}/api/qualitygates/create",
            data={'name': name}
        )
        response.raise_for_status()
        return response.json()
    
    def add_condition_to_quality_gate(self, gate_id: str, metric: str, 
                                     operator: str, threshold: str) -> Dict:
        """Add condition to quality gate"""
        response = self.session.post(
            f"{self.base_url}/api/qualitygates/create_condition",
            data={
                'gateId': gate_id,
                'metric': metric,
                'op': operator,
                'error': threshold
            }
        )
        response.raise_for_status()
        return response.json()
    
    def set_project_quality_gate(self, project_key: str, gate_id: str) -> None:
        """Associate project with quality gate"""
        response = self.session.post(
            f"{self.base_url}/api/qualitygates/select",
            data={
                'projectKey': project_key,
                'gateId': gate_id
            }
        )
        response.raise_for_status()
    
    def create_webhook(self, name: str, url: str, project_key: Optional[str] = None) -> Dict:
        """Create webhook"""
        data = {'name': name, 'url': url}
        if project_key:
            data['project'] = project_key
        
        response = self.session.post(f"{self.base_url}/api/webhooks/create", data=data)
        response.raise_for_status()
        return response.json()
    
    def get_metrics_history(self, project_key: str, metrics: List[str], 
                           from_date: Optional[str] = None) -> Dict:
        """Get metrics history for a project"""
        params = {
            'component': project_key,
            'metrics': ','.join(metrics)
        }
        if from_date:
            params['from'] = from_date
        
        response = self.session.get(
            f"{self.base_url}/api/measures/search_history", 
            params=params
        )
        response.raise_for_status()
        return response.json()

# Usage example
def generate_quality_report(sonar_api: SonarQubeAPI, project_key: str):
    """Generate comprehensive quality report"""
    
    # Key metrics to collect
    metrics = [
        'ncloc',           # Lines of code
        'coverage',        # Code coverage
        'duplicated_lines_density',  # Code duplication
        'vulnerabilities', # Security vulnerabilities
        'bugs',           # Bug count
        'code_smells',    # Code smells
        'sqale_index',    # Technical debt
        'reliability_rating',  # Reliability rating
        'security_rating',     # Security rating
        'sqale_rating'    # Maintainability rating
    ]
    
    # Get current measures
    measures_data = sonar_api.get_project_measures(project_key, metrics)
    measures = {m['metric']: m.get('value', '0') for m in measures_data['component']['measures']}
    
    # Get quality gate status
    quality_gate = sonar_api.get_project_quality_gate(project_key)
    
    # Get critical issues
    critical_issues = sonar_api.get_project_issues(project_key, 'CRITICAL')
    high_issues = sonar_api.get_project_issues(project_key, 'MAJOR')
    
    report = {
        'project_key': project_key,
        'timestamp': datetime.now().isoformat(),
        'quality_gate': {
            'status': quality_gate['projectStatus']['status'],
            'conditions': quality_gate['projectStatus'].get('conditions', [])
        },
        'metrics': {
            'lines_of_code': int(measures.get('ncloc', 0)),
            'coverage': float(measures.get('coverage', 0)),
            'duplicated_lines_density': float(measures.get('duplicated_lines_density', 0)),
            'vulnerabilities': int(measures.get('vulnerabilities', 0)),
            'bugs': int(measures.get('bugs', 0)),
            'code_smells': int(measures.get('code_smells', 0)),
            'technical_debt': measures.get('sqale_index', '0'),
            'reliability_rating': measures.get('reliability_rating', 'A'),
            'security_rating': measures.get('security_rating', 'A'),
            'maintainability_rating': measures.get('sqale_rating', 'A')
        },
        'issues': {
            'critical_count': len(critical_issues),
            'major_count': len(high_issues),
            'critical_issues': critical_issues[:10],  # Top 10 critical issues
            'major_issues': high_issues[:10]          # Top 10 major issues
        }
    }
    
    return report

# Initialize API client
sonar_api = SonarQubeAPI('https://sonarqube.company.com', 'your-auth-token')

# Generate report
report = generate_quality_report(sonar_api, 'my-project-key')
print(json.dumps(report, indent=2))
```

### Quality Gate Management
```python
class QualityGateManager:
    def __init__(self, sonar_api: SonarQubeAPI):
        self.api = sonar_api
    
    def create_standard_quality_gate(self, name: str = "Company Standard") -> str:
        """Create a standard quality gate with common conditions"""
        
        # Create quality gate
        gate = self.api.create_quality_gate(name)
        gate_id = gate['id']
        
        # Add conditions
        conditions = [
            ('coverage', 'LT', '80.0'),           # Coverage < 80%
            ('duplicated_lines_density', 'GT', '5.0'),  # Duplication > 5%
            ('vulnerabilities', 'GT', '0'),       # No vulnerabilities
            ('bugs', 'GT', '0'),                  # No bugs
            ('security_rating', 'GT', '1'),       # Security rating worse than A
            ('reliability_rating', 'GT', '1'),    # Reliability rating worse than A
            ('sqale_rating', 'GT', '2'),          # Maintainability rating worse than B
        ]
        
        for metric, operator, threshold in conditions:
            try:
                self.api.add_condition_to_quality_gate(gate_id, metric, operator, threshold)
                print(f"Added condition: {metric} {operator} {threshold}")
            except Exception as e:
                print(f"Failed to add condition {metric}: {e}")
        
        return gate_id
    
    def apply_quality_gate_to_projects(self, gate_id: str, project_keys: List[str]):
        """Apply quality gate to multiple projects"""
        for project_key in project_keys:
            try:
                self.api.set_project_quality_gate(project_key, gate_id)
                print(f"Applied quality gate to {project_key}")
            except Exception as e:
                print(f"Failed to apply quality gate to {project_key}: {e}")

# Usage
gate_manager = QualityGateManager(sonar_api)
gate_id = gate_manager.create_standard_quality_gate("Strict Quality Gate")
gate_manager.apply_quality_gate_to_projects(gate_id, ['project1', 'project2'])
```

## Webhook Integration

### Flask Webhook Handler
```python
from flask import Flask, request, jsonify
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

class SonarQubeWebhookHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def handle_quality_gate_event(self, payload):
        """Handle quality gate status change"""
        project = payload.get('project', {})
        quality_gate = payload.get('qualityGate', {})
        
        project_key = project.get('key')
        project_name = project.get('name')
        status = quality_gate.get('status')
        
        self.logger.info(f"Quality Gate event for {project_name}: {status}")
        
        if status == 'ERROR':
            self.send_failure_notification(project_name, project_key, quality_gate)
        elif status == 'OK':
            self.send_success_notification(project_name, project_key)
    
    def send_failure_notification(self, project_name, project_key, quality_gate):
        """Send notification for quality gate failure"""
        conditions = quality_gate.get('conditions', [])
        failed_conditions = [c for c in conditions if c.get('status') == 'ERROR']
        
        message = f"🚨 Quality Gate FAILED for {project_name}\n\n"
        message += "Failed conditions:\n"
        
        for condition in failed_conditions:
            metric = condition.get('metricKey')
            operator = condition.get('operator')
            threshold = condition.get('errorThreshold')
            value = condition.get('value')
            
            message += f"• {metric}: {value} {operator} {threshold}\n"
        
        # Send to Slack, Teams, email, etc.
        self.send_to_slack(message, project_key)
    
    def send_success_notification(self, project_name, project_key):
        """Send notification for quality gate success"""
        message = f"✅ Quality Gate PASSED for {project_name}"
        self.send_to_slack(message, project_key, success=True)
    
    def send_to_slack(self, message, project_key, success=False):
        """Send message to Slack"""
        # Implementation for Slack webhook
        import requests
        
        webhook_url = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
        color = "good" if success else "danger"
        
        payload = {
            "attachments": [{
                "color": color,
                "text": message,
                "fields": [{
                    "title": "Project",
                    "value": project_key,
                    "short": True
                }]
            }]
        }
        
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Failed to send Slack notification: {e}")

webhook_handler = SonarQubeWebhookHandler()

@app.route('/webhook/sonarqube', methods=['POST'])
def sonarqube_webhook():
    try:
        payload = request.get_json()
        
        if not payload:
            return jsonify({"error": "No payload received"}), 400
        
        # Log the webhook event
        app.logger.info(f"Received SonarQube webhook: {json.dumps(payload, indent=2)}")
        
        # Handle quality gate events
        if 'qualityGate' in payload:
            webhook_handler.handle_quality_gate_event(payload)
        
        return jsonify({"status": "processed"}), 200
        
    except Exception as e:
        app.logger.error(f"Webhook processing failed: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Advanced Configuration

### Custom Quality Profiles
```python
def create_custom_quality_profile(sonar_api: SonarQubeAPI, language: str, name: str):
    """Create custom quality profile"""
    
    # Create profile
    response = sonar_api.session.post(
        f"{sonar_api.base_url}/api/qualityprofiles/create",
        data={'language': language, 'name': name}
    )
    response.raise_for_status()
    
    profile_key = response.json()['profile']['key']
    
    # Activate specific rules
    rules_to_activate = [
        ('javascript:S1481', 'MAJOR'),  # Unused local variables
        ('javascript:S1854', 'MAJOR'),  # Dead stores should be removed
        ('javascript:S3776', 'CRITICAL'),  # Cognitive complexity
        ('javascript:S4423', 'CRITICAL'),  # Weak SSL/TLS protocols
    ]
    
    for rule_key, severity in rules_to_activate:
        try:
            sonar_api.session.post(
                f"{sonar_api.base_url}/api/qualityprofiles/activate_rule",
                data={
                    'key': profile_key,
                    'rule': rule_key,
                    'severity': severity
                }
            )
            print(f"Activated rule {rule_key} with severity {severity}")
        except Exception as e:
            print(f"Failed to activate rule {rule_key}: {e}")
    
    return profile_key
```

### Bulk Project Management
```python
def bulk_project_setup(sonar_api: SonarQubeAPI, projects: List[Dict]):
    """Setup multiple projects with standard configuration"""
    
    # Create standard quality gate
    gate_manager = QualityGateManager(sonar_api)
    quality_gate_id = gate_manager.create_standard_quality_gate()
    
    for project_config in projects:
        project_key = project_config['key']
        
        try:
            # Set quality gate
            sonar_api.set_project_quality_gate(project_key, quality_gate_id)
            
            # Create webhook
            webhook_url = f"https://webhook.company.com/sonarqube/{project_key}"
            sonar_api.create_webhook(
                name=f"Webhook-{project_key}",
                url=webhook_url,
                project_key=project_key
            )
            
            print(f"Configured project: {project_key}")
            
        except Exception as e:
            print(f"Failed to configure project {project_key}: {e}")

# Example usage
projects = [
    {'key': 'frontend-app', 'name': 'Frontend Application'},
    {'key': 'backend-api', 'name': 'Backend API'},
    {'key': 'mobile-app', 'name': 'Mobile Application'}
]

bulk_project_setup(sonar_api, projects)
```

## Monitoring and Reporting

### Quality Metrics Dashboard
```python
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

class SonarQubeDashboard:
    def __init__(self, sonar_api: SonarQubeAPI):
        self.api = sonar_api
    
    def generate_portfolio_report(self, project_keys: List[str]):
        """Generate portfolio-wide quality report"""
        
        portfolio_data = []
        
        for project_key in project_keys:
            try:
                # Get current metrics
                metrics = ['ncloc', 'coverage', 'vulnerabilities', 'bugs', 'code_smells']
                measures = self.api.get_project_measures(project_key, metrics)
                
                project_metrics = {}
                for measure in measures['component']['measures']:
                    project_metrics[measure['metric']] = float(measure.get('value', 0))
                
                # Get quality gate status
                quality_gate = self.api.get_project_quality_gate(project_key)
                
                portfolio_data.append({
                    'project': project_key,
                    'lines_of_code': project_metrics.get('ncloc', 0),
                    'coverage': project_metrics.get('coverage', 0),
                    'vulnerabilities': project_metrics.get('vulnerabilities', 0),
                    'bugs': project_metrics.get('bugs', 0),
                    'code_smells': project_metrics.get('code_smells', 0),
                    'quality_gate': quality_gate['projectStatus']['status']
                })
                
            except Exception as e:
                print(f"Error processing {project_key}: {e}")
        
        df = pd.DataFrame(portfolio_data)
        return df
    
    def create_coverage_chart(self, df):
        """Create test coverage chart"""
        plt.figure(figsize=(12, 6))
        
        colors = ['green' if qg == 'OK' else 'red' for qg in df['quality_gate']]
        bars = plt.bar(df['project'], df['coverage'], color=colors, alpha=0.7)
        
        plt.axhline(y=80, color='orange', linestyle='--', label='Target (80%)')
        plt.title('Test Coverage by Project')
        plt.xlabel('Project')
        plt.ylabel('Coverage (%)')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig('coverage_chart.png')
        plt.show()
    
    def create_quality_overview(self, df):
        """Create quality overview chart"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Coverage distribution
        ax1.hist(df['coverage'], bins=10, alpha=0.7, color='blue')
        ax1.set_title('Coverage Distribution')
        ax1.set_xlabel('Coverage (%)')
        ax1.set_ylabel('Number of Projects')
        
        # Quality gate status
        qg_counts = df['quality_gate'].value_counts()
        ax2.pie(qg_counts.values, labels=qg_counts.index, autopct='%1.1f%%')
        ax2.set_title('Quality Gate Status')
        
        # Vulnerabilities vs Project Size
        ax3.scatter(df['lines_of_code'], df['vulnerabilities'], alpha=0.7)
        ax3.set_title('Vulnerabilities vs Project Size')
        ax3.set_xlabel('Lines of Code')
        ax3.set_ylabel('Vulnerabilities')
        
        # Technical debt overview
        ax4.bar(df['project'], df['code_smells'], alpha=0.7, color='orange')
        ax4.set_title('Code Smells by Project')
        ax4.set_xlabel('Project')
        ax4.set_ylabel('Code Smells')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('quality_overview.png')
        plt.show()
    
    def generate_trend_analysis(self, project_key: str, days: int = 30):
        """Generate trend analysis for a project"""
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        metrics = ['coverage', 'vulnerabilities', 'bugs', 'code_smells']
        history = self.api.get_metrics_history(project_key, metrics, from_date)
        
        # Process history data
        trend_data = {}
        for measure in history['measures']:
            metric = measure['metric']
            trend_data[metric] = []
            
            for history_point in measure['history']:
                trend_data[metric].append({
                    'date': datetime.strptime(history_point['date'], '%Y-%m-%dT%H:%M:%S%z'),
                    'value': float(history_point.get('value', 0))
                })
        
        # Create trend charts
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.flatten()
        
        for i, (metric, data) in enumerate(trend_data.items()):
            if data:
                dates = [point['date'] for point in data]
                values = [point['value'] for point in data]
                
                axes[i].plot(dates, values, marker='o')
                axes[i].set_title(f'{metric.title()} Trend')
                axes[i].set_xlabel('Date')
                axes[i].set_ylabel(metric.title())
                axes[i].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{project_key}_trends.png')
        plt.show()

# Usage
dashboard = SonarQubeDashboard(sonar_api)
projects = ['project1', 'project2', 'project3']

# Generate reports
df = dashboard.generate_portfolio_report(projects)
dashboard.create_coverage_chart(df)
dashboard.create_quality_overview(df)
dashboard.generate_trend_analysis('project1')
```

## Best Practices

### Project Configuration Standards
```properties
# Standard sonar-project.properties template
sonar.projectKey=${PROJECT_KEY}
sonar.projectName=${PROJECT_NAME}
sonar.projectVersion=${VERSION}

# Source configuration
sonar.sources=src
sonar.tests=tests
sonar.exclusions=**/node_modules/**,**/build/**,**/dist/**,**/*.min.js,**/vendor/**
sonar.test.inclusions=**/*test*/**,**/*Test*,**/*.spec.*,**/*.test.*

# Coverage configuration
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.python.coverage.reportPaths=coverage.xml
sonar.java.coveragePlugin=jacoco
sonar.jacoco.reportPaths=target/jacoco.exec

# Quality gate settings
sonar.qualitygate.wait=true
sonar.qualitygate.timeout=300

# Additional settings
sonar.sourceEncoding=UTF-8
sonar.scm.provider=git
```

### Security Configuration
```bash
# Secure SonarQube installation
# 1. Change default credentials
# 2. Configure HTTPS
# 3. Set up proper authentication
# 4. Configure network security

# Update sonar.properties for security
echo "sonar.web.https.port=9443" >> /opt/sonarqube/conf/sonar.properties
echo "sonar.web.https.keyAlias=sonarqube" >> /opt/sonarqube/conf/sonar.properties
echo "sonar.web.https.keyStore=/opt/sonarqube/conf/sonarqube.jks" >> /opt/sonarqube/conf/sonar.properties
echo "sonar.web.https.keyStorePassword=your-password" >> /opt/sonarqube/conf/sonar.properties

# Force HTTPS
echo "sonar.web.http.port=-1" >> /opt/sonarqube/conf/sonar.properties

# Configure LDAP authentication
echo "sonar.security.realm=LDAP" >> /opt/sonarqube/conf/sonar.properties
echo "ldap.url=ldap://ldap.company.com:389" >> /opt/sonarqube/conf/sonar.properties
echo "ldap.bindDn=cn=sonar,ou=users,dc=company,dc=com" >> /opt/sonarqube/conf/sonar.properties
```

## Resources

- [SonarQube Documentation](https://docs.sonarqube.org/)
- [SonarQube REST API](https://next.sonarqube.com/sonarqube/web_api)
- [Quality Gate Configuration](https://docs.sonarqube.org/latest/user-guide/quality-gates/)
- [SonarScanner Documentation](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/)
- [Community Plugins](https://docs.sonarqube.org/display/PLUG/Plugin+Library)
- [Quality Profiles](https://docs.sonarqube.org/latest/instance-administration/quality-profiles/)
- [Security Configuration](https://docs.sonarqube.org/latest/instance-administration/security/)
- [SonarQube Community](https://community.sonarsource.com/)
- [Best Practices Guide](https://docs.sonarqube.org/latest/analysis/overview/)
- [Webhooks Documentation](https://docs.sonarqube.org/latest/project-administration/webhooks/)