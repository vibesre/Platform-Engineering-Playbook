# OWASP ZAP

OWASP ZAP (Zed Attack Proxy) is an open-source web application security scanner used for finding vulnerabilities in web applications during development and testing.

## Installation

### Desktop Installation
```bash
# Download and install on Linux
wget https://github.com/zaproxy/zaproxy/releases/download/v2.14.0/ZAP_2_14_0_unix.sh
chmod +x ZAP_2_14_0_unix.sh
./ZAP_2_14_0_unix.sh

# Install on macOS via Homebrew
brew install --cask owasp-zap

# Install on Windows via Chocolatey
choco install zap

# Verify installation
zap.sh -version
```

### Docker
```bash
# Run ZAP in headless mode
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://example.com

# Run with UI (requires X11 forwarding)
docker run -u zap -p 8080:8080 -p 8090:8090 \
  -v $(pwd):/zap/wrk/:rw \
  -t owasp/zap2docker-stable zap-webswing.sh

# Run ZAP daemon
docker run -p 8080:8080 -d owasp/zap2docker-stable \
  zap.sh -daemon -host 0.0.0.0 -port 8080 \
  -config api.addrs.addr.name=.* \
  -config api.addrs.addr.regex=true
```

### Command Line Tools
```bash
# Install ZAP CLI
pip install zapcli

# Install Python OWASP ZAP API
pip install python-owasp-zap-v2.4

# Verify CLI installation
zap-cli --help
```

## Basic Usage

### GUI Mode
```bash
# Start ZAP with GUI
zap.sh

# Start with specific memory allocation
zap.sh -Xmx4g

# Start with custom configuration
zap.sh -config view.mode=safe -config connection.dnsTtlSuccessfulQueries=60
```

### Headless Mode
```bash
# Start ZAP daemon
zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true

# Quick baseline scan
zap-baseline.py -t https://example.com

# Full scan
zap-full-scan.py -t https://example.com

# API scan
zap-api-scan.py -t https://example.com/api/openapi.json -f openapi
```

### Command Line Interface
```bash
# Basic vulnerability scan
zap-cli quick-scan --self-contained --start-options '-config api.disablekey=true' https://example.com

# Spider and scan
zap-cli --zap-url http://localhost:8080 open-url https://example.com
zap-cli --zap-url http://localhost:8080 spider https://example.com
zap-cli --zap-url http://localhost:8080 active-scan https://example.com

# Generate report
zap-cli --zap-url http://localhost:8080 report -o zap-report.html -f html
```

## Configuration

### ZAP Configuration File
```xml
<!-- zap.conf -->
<config>
  <view>
    <mode>standard</mode>
  </view>
  <api>
    <disablekey>false</disablekey>
    <key>your-api-key</key>
    <addrs>
      <addr>
        <name>localhost</name>
        <regex>false</regex>
      </addr>
    </addrs>
  </api>
  <spider>
    <maxDepth>5</maxDepth>
    <maxChildren>10</maxChildren>
    <postForm>true</postForm>
    <processForm>true</processForm>
  </spider>
  <ascan>
    <hostPerScan>2</hostPerScan>
    <threadPerHost>2</threadPerHost>
    <maxRuleDurationInMins>0</maxRuleDurationInMins>
    <maxScanDurationInMins>0</maxScanDurationInMins>
  </ascan>
  <httpsender>
    <useragent>Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36</useragent>
  </httpsender>
  <connection>
    <timeoutInSecs>60</timeoutInSecs>
    <proxyChain>
      <enabled>false</enabled>
      <hostName></hostName>
      <port>8080</port>
    </proxyChain>
  </connection>
</config>
```

### Authentication Configuration
```python
# authentication.py
import time
from zapv2 import ZAPv2

class ZAPAuthConfig:
    def __init__(self, zap_url='http://localhost:8080', api_key=None):
        self.zap = ZAPv2(proxies={'http': zap_url, 'https': zap_url}, apikey=api_key)
        
    def configure_form_auth(self, login_url, username, password, 
                           username_field='username', password_field='password'):
        """Configure form-based authentication"""
        
        # Create context
        context_name = 'AuthContext'
        context_id = self.zap.context.new_context(context_name)
        
        # Include URL in context
        self.zap.context.include_in_context(context_name, '.*')
        
        # Configure authentication
        auth_method_name = 'formBasedAuthentication'
        login_request_data = f'{username_field}={username}&{password_field}={password}'
        
        self.zap.authentication.set_authentication_method(
            contextid=context_id,
            authmethodname=auth_method_name,
            authmethodconfigparams=f'loginUrl={login_url}&loginRequestData={login_request_data}'
        )
        
        # Create user
        user_id = self.zap.users.new_user(context_id, 'testuser')
        self.zap.users.set_authentication_credentials(
            contextid=context_id,
            userid=user_id,
            authcredentialsconfigparams=f'username={username}&password={password}'
        )
        
        self.zap.users.set_user_enabled(context_id, user_id, 'true')
        
        return context_id, user_id
    
    def configure_jwt_auth(self, jwt_token, header_name='Authorization'):
        """Configure JWT authentication"""
        
        context_name = 'JWTContext'
        context_id = self.zap.context.new_context(context_name)
        
        # Set authorization header
        self.zap.replacer.add_rule(
            description='JWT Auth Header',
            enabled='true',
            matchtype='REQ_HEADER',
            matchregex='false',
            matchstring=header_name,
            replacement=f'Bearer {jwt_token}'
        )
        
        return context_id
    
    def configure_oauth2(self, client_id, client_secret, auth_url, token_url, scope='openid'):
        """Configure OAuth2 authentication"""
        
        context_name = 'OAuth2Context'
        context_id = self.zap.context.new_context(context_name)
        
        auth_config = f'clientId={client_id}&clientSecret={client_secret}&' \
                     f'authUrl={auth_url}&tokenUrl={token_url}&scope={scope}'
        
        self.zap.authentication.set_authentication_method(
            contextid=context_id,
            authmethodname='oauth2Authentication',
            authmethodconfigparams=auth_config
        )
        
        return context_id

# Usage
auth_config = ZAPAuthConfig()
context_id, user_id = auth_config.configure_form_auth(
    login_url='https://example.com/login',
    username='testuser',
    password='testpass'
)
```

## Scanning Strategies

### Automated Scanning
```python
import time
from zapv2 import ZAPv2

class ZAPScanner:
    def __init__(self, target_url, zap_url='http://localhost:8080', api_key=None):
        self.target_url = target_url
        self.zap = ZAPv2(proxies={'http': zap_url, 'https': zap_url}, apikey=api_key)
        
    def passive_scan(self):
        """Run passive scan"""
        print(f'Starting passive scan of {self.target_url}')
        
        # Access the target URL to populate the sites tree
        self.zap.urlopen(self.target_url)
        time.sleep(2)
        
        # Give the passive scanner time to finish
        while int(self.zap.pscan.records_to_scan) > 0:
            print(f'Passive scan in progress. Records left: {self.zap.pscan.records_to_scan}')
            time.sleep(2)
        
        print('Passive scan completed')
        return self.zap.core.alerts()
    
    def spider_scan(self, max_depth=5):
        """Run spider scan"""
        print(f'Starting spider scan of {self.target_url}')
        
        scan_id = self.zap.spider.scan(self.target_url, maxchildren=10, recurse=True)
        
        while int(self.zap.spider.status(scan_id)) < 100:
            progress = self.zap.spider.status(scan_id)
            print(f'Spider progress: {progress}%')
            time.sleep(1)
        
        print('Spider scan completed')
        return self.zap.spider.results(scan_id)
    
    def ajax_spider_scan(self):
        """Run AJAX spider scan"""
        print(f'Starting AJAX spider scan of {self.target_url}')
        
        self.zap.ajaxSpider.scan(self.target_url)
        
        while self.zap.ajaxSpider.status == 'running':
            print(f'AJAX spider running. URLs found: {self.zap.ajaxSpider.number_of_results}')
            time.sleep(2)
        
        print('AJAX spider completed')
        return self.zap.ajaxSpider.results()
    
    def active_scan(self, policy_name=None):
        """Run active scan"""
        print(f'Starting active scan of {self.target_url}')
        
        if policy_name:
            self.zap.ascan.set_scan_policy_name(policy_name)
        
        scan_id = self.zap.ascan.scan(self.target_url)
        
        while int(self.zap.ascan.status(scan_id)) < 100:
            progress = self.zap.ascan.status(scan_id)
            print(f'Active scan progress: {progress}%')
            time.sleep(5)
        
        print('Active scan completed')
        return self.zap.core.alerts()
    
    def comprehensive_scan(self):
        """Run comprehensive scan"""
        results = {}
        
        # Passive scan
        results['passive'] = self.passive_scan()
        
        # Spider scan
        results['spider_urls'] = self.spider_scan()
        
        # AJAX spider scan
        results['ajax_urls'] = self.ajax_spider_scan()
        
        # Active scan
        results['active'] = self.active_scan()
        
        return results
    
    def generate_report(self, format='html', output_file='zap_report'):
        """Generate scan report"""
        if format.lower() == 'html':
            report = self.zap.core.htmlreport()
            with open(f'{output_file}.html', 'w') as f:
                f.write(report)
        elif format.lower() == 'xml':
            report = self.zap.core.xmlreport()
            with open(f'{output_file}.xml', 'w') as f:
                f.write(report)
        elif format.lower() == 'json':
            report = self.zap.core.jsonreport()
            with open(f'{output_file}.json', 'w') as f:
                f.write(report)
        
        print(f'Report saved as {output_file}.{format}')

# Usage
scanner = ZAPScanner('https://example.com')
results = scanner.comprehensive_scan()
scanner.generate_report(format='html', output_file='security_report')
```

### API Security Testing
```python
import json
import requests
from zapv2 import ZAPv2

class ZAPAPITester:
    def __init__(self, zap_url='http://localhost:8080', api_key=None):
        self.zap = ZAPv2(proxies={'http': zap_url, 'https': zap_url}, apikey=api_key)
        
    def import_openapi_spec(self, spec_url_or_file, target_url):
        """Import OpenAPI/Swagger specification"""
        if spec_url_or_file.startswith('http'):
            # Import from URL
            self.zap.openapi.import_url(spec_url_or_file, target_url)
        else:
            # Import from file
            with open(spec_url_or_file, 'r') as f:
                spec_content = f.read()
            self.zap.openapi.import_file(spec_content, target_url)
        
        print(f'OpenAPI spec imported for {target_url}')
    
    def configure_api_auth(self, auth_header, auth_value):
        """Configure API authentication"""
        self.zap.script.load(
            scriptname='api_auth',
            scripttype='httpsender',
            scriptengine='Oracle Nashorn',
            scriptfile=f'''
            function sendingRequest(msg, initiator, helper) {{
                msg.getRequestHeader().setHeader("{auth_header}", "{auth_value}");
            }}
            
            function responseReceived(msg, initiator, helper) {{
                // Handle response if needed
            }}
            '''
        )
        self.zap.script.enable('api_auth')
    
    def test_api_endpoints(self, base_url, endpoints):
        """Test specific API endpoints"""
        results = []
        
        for endpoint in endpoints:
            url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            
            # Access endpoint
            self.zap.urlopen(url)
            
            # Run active scan on endpoint
            scan_id = self.zap.ascan.scan(url)
            
            while int(self.zap.ascan.status(scan_id)) < 100:
                time.sleep(1)
            
            # Get alerts for this endpoint
            alerts = [alert for alert in self.zap.core.alerts() if url in alert['url']]
            results.append({
                'endpoint': endpoint,
                'url': url,
                'alerts': alerts
            })
        
        return results
    
    def test_jwt_security(self, jwt_token):
        """Test JWT token security"""
        issues = []
        
        try:
            # Parse JWT without verification
            import base64
            header_b64, payload_b64, signature = jwt_token.split('.')
            
            # Decode header and payload
            header = json.loads(base64.b64decode(header_b64 + '=='))
            payload = json.loads(base64.b64decode(payload_b64 + '=='))
            
            # Check for common JWT vulnerabilities
            if header.get('alg') == 'none':
                issues.append('JWT uses "none" algorithm - highly insecure')
            
            if header.get('alg') == 'HS256' and 'kid' in header:
                issues.append('JWT uses HMAC with key ID - potential key confusion')
            
            if 'exp' not in payload:
                issues.append('JWT does not have expiration claim')
            
            if payload.get('aud') is None:
                issues.append('JWT does not specify audience')
            
        except Exception as e:
            issues.append(f'Failed to parse JWT: {str(e)}')
        
        return issues

# Usage
api_tester = ZAPAPITester()
api_tester.import_openapi_spec('https://api.example.com/swagger.json', 'https://api.example.com')
api_tester.configure_api_auth('Authorization', 'Bearer your-token')

endpoints = ['/users', '/products', '/orders']
results = api_tester.test_api_endpoints('https://api.example.com', endpoints)
```

## CI/CD Integration

### GitHub Actions
```yaml
name: OWASP ZAP Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'

jobs:
  zap_baseline:
    runs-on: ubuntu-latest
    name: Baseline Scan
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: ZAP Baseline Scan
      uses: zaproxy/action-baseline@v0.9.0
      with:
        target: 'https://example.com'
        rules_file_name: '.zap/rules.tsv'
        cmd_options: '-a'
    
    - name: Upload ZAP Results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: zap-baseline-report
        path: report_html.html

  zap_full_scan:
    runs-on: ubuntu-latest
    name: Full Scan
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: ZAP Full Scan
      uses: zaproxy/action-full-scan@v0.7.0
      with:
        target: 'https://example.com'
        rules_file_name: '.zap/rules.tsv'
        cmd_options: '-a -j'
    
    - name: Upload ZAP Results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: zap-full-report
        path: report_html.html

  zap_api_scan:
    runs-on: ubuntu-latest
    name: API Scan
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: ZAP API Scan
      uses: zaproxy/action-api-scan@v0.6.0
      with:
        target: 'https://api.example.com'
        format: 'openapi'
        api_spec: 'https://api.example.com/swagger.json'
        cmd_options: '-a'
    
    - name: Upload ZAP Results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: zap-api-report
        path: report_html.html
```

### GitLab CI
```yaml
stages:
  - security

variables:
  ZAP_VERSION: "2.14.0"

.zap_template: &zap_template
  image: owasp/zap2docker-stable:$ZAP_VERSION
  before_script:
    - mkdir -p /zap/wrk/reports

zap_baseline:
  <<: *zap_template
  stage: security
  script:
    - zap-baseline.py -t $TARGET_URL -r baseline_report.html -x baseline_report.xml || true
  artifacts:
    reports:
      junit: baseline_report.xml
    paths:
      - baseline_report.html
    expire_in: 1 week
  only:
    - merge_requests
    - main

zap_full_scan:
  <<: *zap_template
  stage: security
  script:
    - zap-full-scan.py -t $TARGET_URL -r full_report.html -x full_report.xml || true
  artifacts:
    reports:
      junit: full_report.xml
    paths:
      - full_report.html
    expire_in: 1 week
  only:
    - schedules
    - main
  when: manual

zap_api_scan:
  <<: *zap_template
  stage: security
  script:
    - zap-api-scan.py -t $API_TARGET_URL -f openapi -r api_report.html -x api_report.xml || true
  artifacts:
    reports:
      junit: api_report.xml
    paths:
      - api_report.html
    expire_in: 1 week
  only:
    - merge_requests
    - main
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    environment {
        ZAP_VERSION = '2.14.0'
        TARGET_URL = 'https://example.com'
        API_URL = 'https://api.example.com'
    }
    
    stages {
        stage('OWASP ZAP Security Scan') {
            parallel {
                stage('Baseline Scan') {
                    steps {
                        script {
                            docker.image("owasp/zap2docker-stable:${ZAP_VERSION}").inside('-u zap') {
                                sh '''
                                    zap-baseline.py -t $TARGET_URL \
                                        -r baseline_report.html \
                                        -x baseline_report.xml || true
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'baseline_report.*', fingerprint: true
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: '.',
                                reportFiles: 'baseline_report.html',
                                reportName: 'ZAP Baseline Report'
                            ])
                        }
                    }
                }
                
                stage('API Scan') {
                    steps {
                        script {
                            docker.image("owasp/zap2docker-stable:${ZAP_VERSION}").inside('-u zap') {
                                sh '''
                                    zap-api-scan.py -t $API_URL \
                                        -f openapi \
                                        -r api_report.html \
                                        -x api_report.xml || true
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'api_report.*', fingerprint: true
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: '.',
                                reportFiles: 'api_report.html',
                                reportName: 'ZAP API Report'
                            ])
                        }
                    }
                }
            }
        }
        
        stage('Full Scan') {
            when {
                anyOf {
                    branch 'main'
                    triggeredBy 'TimerTrigger'
                }
            }
            steps {
                script {
                    docker.image("owasp/zap2docker-stable:${ZAP_VERSION}").inside('-u zap') {
                        sh '''
                            zap-full-scan.py -t $TARGET_URL \
                                -r full_report.html \
                                -x full_report.xml || true
                        '''
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'full_report.*', fingerprint: true
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'full_report.html',
                        reportName: 'ZAP Full Report'
                    ])
                }
            }
        }
    }
    
    post {
        always {
            // Parse results and send notifications
            script {
                def zapResults = readFile('baseline_report.xml')
                if (zapResults.contains('riskcode="3"')) {
                    currentBuild.result = 'UNSTABLE'
                    echo 'High risk vulnerabilities found!'
                }
            }
        }
    }
}
```

## Kubernetes Integration

### ZAP Operator
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zap-operator
  namespace: security
spec:
  replicas: 1
  selector:
    matchLabels:
      app: zap-operator
  template:
    metadata:
      labels:
        app: zap-operator
    spec:
      serviceAccountName: zap-operator
      containers:
      - name: zap-operator
        image: owasp/zap2docker-stable:2.14.0
        command: ["/bin/sh"]
        args:
        - -c
        - |
          zap.sh -daemon -host 0.0.0.0 -port 8080 \
            -config api.addrs.addr.name=.* \
            -config api.addrs.addr.regex=true \
            -config api.disablekey=true
        ports:
        - containerPort: 8080
          name: zap-api
        resources:
          requests:
            cpu: 200m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 2Gi
        livenessProbe:
          httpGet:
            path: /JSON/core/view/version/
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /JSON/core/view/version/
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: zap-service
  namespace: security
spec:
  selector:
    app: zap-operator
  ports:
  - port: 8080
    targetPort: 8080
    name: zap-api
  type: ClusterIP
```

### Security Scan CronJob
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: security-scan
  namespace: security
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: zap-scanner
            image: owasp/zap2docker-stable:2.14.0
            command: ["/bin/sh"]
            args:
            - -c
            - |
              # Run baseline scan
              zap-baseline.py -t $TARGET_URL -r /reports/baseline.html -x /reports/baseline.xml
              
              # Run API scan if OpenAPI spec is available
              if [ ! -z "$API_SPEC_URL" ]; then
                zap-api-scan.py -t $API_TARGET_URL -f openapi -r /reports/api.html -x /reports/api.xml
              fi
              
              # Upload reports to S3 or storage
              if [ ! -z "$UPLOAD_COMMAND" ]; then
                eval $UPLOAD_COMMAND
              fi
            env:
            - name: TARGET_URL
              value: "https://example.com"
            - name: API_TARGET_URL
              value: "https://api.example.com"
            - name: API_SPEC_URL
              value: "https://api.example.com/swagger.json"
            - name: UPLOAD_COMMAND
              value: "aws s3 cp /reports/ s3://security-reports/ --recursive"
            volumeMounts:
            - name: reports
              mountPath: /reports
            resources:
              requests:
                cpu: 500m
                memory: 1Gi
              limits:
                cpu: 2000m
                memory: 4Gi
          volumes:
          - name: reports
            emptyDir: {}
```

## Advanced Features

### Custom Scripts
```javascript
// Authentication script
function authenticate(helper, paramsValues, credentials) {
    var loginUrl = paramsValues.get("loginUrl");
    var username = credentials.getParam("username");
    var password = credentials.getParam("password");
    
    var loginRequest = helper.prepareMessage();
    loginRequest.setRequestHeader(
        "POST " + loginUrl + " HTTP/1.1\r\n" +
        "Host: example.com\r\n" +
        "Content-Type: application/x-www-form-urlencoded\r\n"
    );
    
    var loginBody = "username=" + username + "&password=" + password;
    loginRequest.setRequestBody(loginBody);
    
    helper.sendAndReceive(loginRequest);
    
    return loginRequest;
}

function getRequiredParamsNames() {
    return ["loginUrl"];
}

function getCredentialsParamsNames() {
    return ["username", "password"];
}
```

### Custom Scan Rules
```python
# custom_scan_rule.py
from zapv2 import ZAPv2

class CustomSecurityRule:
    def __init__(self, zap_proxy):
        self.zap = zap_proxy
        
    def check_security_headers(self, url):
        """Check for security headers"""
        response = self.zap.core.send_request(url)
        headers = response.get('responseHeader', '')
        
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000',
            'Content-Security-Policy': None,
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
        
        missing_headers = []
        for header, expected_value in security_headers.items():
            if header not in headers:
                missing_headers.append(header)
        
        return missing_headers
    
    def check_cookie_security(self, url):
        """Check cookie security attributes"""
        response = self.zap.core.send_request(url)
        cookies = response.get('cookieParams', [])
        
        insecure_cookies = []
        for cookie in cookies:
            if not cookie.get('secure'):
                insecure_cookies.append(f"Cookie '{cookie['name']}' missing Secure flag")
            if not cookie.get('httpOnly'):
                insecure_cookies.append(f"Cookie '{cookie['name']}' missing HttpOnly flag")
            if cookie.get('sameSite') not in ['Strict', 'Lax']:
                insecure_cookies.append(f"Cookie '{cookie['name']}' missing SameSite attribute")
        
        return insecure_cookies
    
    def check_ssl_configuration(self, url):
        """Check SSL/TLS configuration"""
        import ssl
        import socket
        from urllib.parse import urlparse
        
        parsed_url = urlparse(url)
        if parsed_url.scheme != 'https':
            return ['Site not using HTTPS']
        
        issues = []
        try:
            context = ssl.create_default_context()
            with socket.create_connection((parsed_url.hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=parsed_url.hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                    # Check cipher strength
                    if cipher and cipher[2] < 128:
                        issues.append(f'Weak cipher: {cipher[0]} ({cipher[2]} bits)')
                    
                    # Check certificate
                    if cert:
                        import datetime
                        not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                        if not_after < datetime.datetime.now() + datetime.timedelta(days=30):
                            issues.append('Certificate expires within 30 days')
        
        except Exception as e:
            issues.append(f'SSL check failed: {str(e)}')
        
        return issues

# Usage
custom_rule = CustomSecurityRule(zap)
security_issues = {
    'missing_headers': custom_rule.check_security_headers('https://example.com'),
    'insecure_cookies': custom_rule.check_cookie_security('https://example.com'),
    'ssl_issues': custom_rule.check_ssl_configuration('https://example.com')
}
```

### Report Generation and Analysis
```python
import json
import xml.etree.ElementTree as ET
from datetime import datetime

class ZAPReportAnalyzer:
    def __init__(self):
        self.risk_levels = {
            '0': 'Informational',
            '1': 'Low',
            '2': 'Medium',
            '3': 'High'
        }
    
    def parse_xml_report(self, xml_file):
        """Parse ZAP XML report"""
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        alerts = []
        for alert in root.findall('.//alertitem'):
            alert_data = {
                'name': alert.find('name').text if alert.find('name') is not None else '',
                'riskcode': alert.find('riskcode').text if alert.find('riskcode') is not None else '0',
                'confidence': alert.find('confidence').text if alert.find('confidence') is not None else '0',
                'riskdesc': alert.find('riskdesc').text if alert.find('riskdesc') is not None else '',
                'desc': alert.find('desc').text if alert.find('desc') is not None else '',
                'solution': alert.find('solution').text if alert.find('solution') is not None else '',
                'reference': alert.find('reference').text if alert.find('reference') is not None else '',
                'instances': []
            }
            
            for instance in alert.findall('.//instance'):
                instance_data = {
                    'uri': instance.find('uri').text if instance.find('uri') is not None else '',
                    'method': instance.find('method').text if instance.find('method') is not None else '',
                    'param': instance.find('param').text if instance.find('param') is not None else '',
                    'evidence': instance.find('evidence').text if instance.find('evidence') is not None else ''
                }
                alert_data['instances'].append(instance_data)
            
            alerts.append(alert_data)
        
        return alerts
    
    def generate_summary(self, alerts):
        """Generate security summary"""
        summary = {
            'total_alerts': len(alerts),
            'risk_breakdown': {'0': 0, '1': 0, '2': 0, '3': 0},
            'top_vulnerabilities': {},
            'affected_urls': set()
        }
        
        for alert in alerts:
            risk_code = alert.get('riskcode', '0')
            summary['risk_breakdown'][risk_code] += 1
            
            vuln_name = alert.get('name', 'Unknown')
            if vuln_name not in summary['top_vulnerabilities']:
                summary['top_vulnerabilities'][vuln_name] = 0
            summary['top_vulnerabilities'][vuln_name] += 1
            
            for instance in alert.get('instances', []):
                summary['affected_urls'].add(instance.get('uri', ''))
        
        summary['affected_urls'] = list(summary['affected_urls'])
        return summary
    
    def generate_dashboard_data(self, alerts):
        """Generate data for security dashboard"""
        summary = self.generate_summary(alerts)
        
        dashboard_data = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'total_vulnerabilities': summary['total_alerts'],
                'high_risk': summary['risk_breakdown']['3'],
                'medium_risk': summary['risk_breakdown']['2'],
                'low_risk': summary['risk_breakdown']['1'],
                'info': summary['risk_breakdown']['0'],
                'unique_urls_affected': len(summary['affected_urls'])
            },
            'top_vulnerabilities': sorted(
                summary['top_vulnerabilities'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10],
            'risk_distribution': [
                {'risk': self.risk_levels[k], 'count': v}
                for k, v in summary['risk_breakdown'].items()
            ]
        }
        
        return dashboard_data
    
    def export_to_csv(self, alerts, filename='zap_report.csv'):
        """Export alerts to CSV"""
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'risk_level', 'confidence', 'description', 'solution', 'url', 'parameter']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for alert in alerts:
                for instance in alert.get('instances', [{}]):
                    writer.writerow({
                        'name': alert.get('name', ''),
                        'risk_level': self.risk_levels.get(alert.get('riskcode', '0'), 'Unknown'),
                        'confidence': alert.get('confidence', ''),
                        'description': alert.get('desc', ''),
                        'solution': alert.get('solution', ''),
                        'url': instance.get('uri', ''),
                        'parameter': instance.get('param', '')
                    })

# Usage
analyzer = ZAPReportAnalyzer()
alerts = analyzer.parse_xml_report('zap_report.xml')
summary = analyzer.generate_summary(alerts)
dashboard_data = analyzer.generate_dashboard_data(alerts)
analyzer.export_to_csv(alerts, 'security_findings.csv')
```

## Best Practices

### Configuration Best Practices
```yaml
# .zap/rules.tsv - Rule configuration file
10011	IGNORE	(Cookie Without Secure Flag - Low)
10015	IGNORE	(Incomplete or No Cache-control and Pragma HTTP Header Set - Low)
10021	IGNORE	(X-Content-Type-Options Header Missing - Low)
10023	IGNORE	(Information Disclosure - Debug Error Messages - Low)
10025	IGNORE	(Information Disclosure - Sensitive Information in URL - Informational)
10026	IGNORE	(HTTP Parameter Override - Medium)
10027	IGNORE	(Information Disclosure - Suspicious Comments - Informational)
10032	IGNORE	(Viewstate Scanner - Informational)
10035	IGNORE	(Strict-Transport-Security Header Not Set - Low)
10036	IGNORE	(Server Leaks Version Information via "Server" HTTP Response Header Field - Low)
10037	IGNORE	(Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s) - Low)
10040	IGNORE	(Secure Pages Include Mixed Content - Medium)
10043	IGNORE	(User Controllable JavaScript Event (XSS) - High)
10044	IGNORE	(Big Redirect Detected (Potential Sensitive Information Leak) - Informational)
10045	IGNORE	(Source Code Disclosure - /WEB-INF folder - High)
10047	IGNORE	(CSRF Token Scanner - Informational)
10048	IGNORE	(Remote Code Execution - Shell Shock - High)
10049	IGNORE	(Content Cacheability - Informational)
10050	IGNORE	(Retrieved from Cache - Informational)
10051	IGNORE	(Relative Path Overwrite - High)
10052	IGNORE	(X-ChromeLogger-Data Header Information Leak - Medium)
10054	IGNORE	(Cookie Without SameSite Attribute - Low)
10055	IGNORE	(CSP Scanner - Medium)
10056	IGNORE	(X-Debug-Token Information Leak - Medium)
10057	IGNORE	(Username Hash Found - Informational)
10061	IGNORE	(X-AspNet-Version Response Header Scanner - Low)
10062	IGNORE	(PII Scanner - Informational)
10063	IGNORE	(Feature Policy Header Not Set - Low)
10096	IGNORE	(Timestamp Disclosure - Low)
10097	IGNORE	(Hash Disclosure - Informational)
10098	IGNORE	(Cross-Domain Misconfiguration - Medium)
10099	IGNORE	(Source Code Disclosure - Git - Medium)
10100	IGNORE	(Weak Authentication Method - High)
10101	IGNORE	(Insecure HTTP Method - Medium)
10102	IGNORE	(HTTP Only Site - Informational)
10103	IGNORE	(Clickjacking Protection Scanner - Medium)
10104	IGNORE	(User Agent Fuzzer - Informational)
10105	IGNORE	(Weak Authentication Method - High)
10106	IGNORE	(HTTP Only Site - Informational)
10107	IGNORE	(Httpoxy - Proxy Header Misuse - High)
10108	IGNORE	(Reverse Tabnabbing - Informational)
10109	IGNORE	(Modern Web Application - Informational)
10110	IGNORE	(Dangerous JS Functions - Low)
10111	IGNORE	(Authentication Request Identified - Informational)
```

### Security Testing Automation
```bash
#!/bin/bash
# comprehensive-security-scan.sh

set -e

TARGET_URL="${1:-https://example.com}"
API_URL="${2:-https://api.example.com}"
REPORTS_DIR="./security-reports"
ZAP_PORT="8080"

echo "Starting comprehensive security scan for $TARGET_URL"

# Create reports directory
mkdir -p "$REPORTS_DIR"

# Start ZAP daemon
echo "Starting ZAP daemon..."
docker run -d --name zap-daemon \
  -p $ZAP_PORT:8080 \
  -v $(pwd)/$REPORTS_DIR:/zap/reports \
  owasp/zap2docker-stable \
  zap.sh -daemon -host 0.0.0.0 -port 8080 \
  -config api.addrs.addr.name=.* \
  -config api.addrs.addr.regex=true \
  -config api.disablekey=true

# Wait for ZAP to start
echo "Waiting for ZAP to start..."
until curl -s http://localhost:$ZAP_PORT > /dev/null; do
  sleep 2
done

# Run baseline scan
echo "Running baseline scan..."
docker run --rm --network host \
  -v $(pwd)/$REPORTS_DIR:/zap/reports \
  owasp/zap2docker-stable \
  zap-baseline.py -t $TARGET_URL \
  -r /zap/reports/baseline-report.html \
  -x /zap/reports/baseline-report.xml

# Run API scan if API URL provided
if [ "$API_URL" != "https://api.example.com" ]; then
  echo "Running API scan..."
  docker run --rm --network host \
    -v $(pwd)/$REPORTS_DIR:/zap/reports \
    owasp/zap2docker-stable \
    zap-api-scan.py -t $API_URL \
    -f openapi \
    -r /zap/reports/api-report.html \
    -x /zap/reports/api-report.xml
fi

# Run full scan on main branch or manually
if [ "$CI_COMMIT_REF_NAME" = "main" ] || [ "$FULL_SCAN" = "true" ]; then
  echo "Running full scan..."
  docker run --rm --network host \
    -v $(pwd)/$REPORTS_DIR:/zap/reports \
    owasp/zap2docker-stable \
    zap-full-scan.py -t $TARGET_URL \
    -r /zap/reports/full-report.html \
    -x /zap/reports/full-report.xml
fi

# Stop ZAP daemon
echo "Stopping ZAP daemon..."
docker stop zap-daemon
docker rm zap-daemon

# Process reports
echo "Processing reports..."
python3 process_zap_reports.py $REPORTS_DIR

echo "Security scan completed. Reports available in $REPORTS_DIR"
```

## Resources

- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
- [ZAP User Guide](https://www.zaproxy.org/docs/desktop/)
- [ZAP API Documentation](https://www.zaproxy.org/docs/api/)
- [Docker Images](https://hub.docker.com/u/owasp)
- [GitHub Actions](https://github.com/zaproxy/action-baseline)
- [ZAP Extensions](https://www.zaproxy.org/addons/)
- [Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [ZAP Scripting](https://www.zaproxy.org/docs/scripting/)
- [Community Support](https://github.com/zaproxy/zaproxy/discussions)
- [Training Resources](https://www.zaproxy.org/getting-started/)