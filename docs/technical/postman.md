# Postman

Postman is a comprehensive API development environment that simplifies the process of developing, testing, documenting, and sharing APIs. It provides tools for API testing, automation, monitoring, and collaboration.

## Installation

### Desktop Application
```bash
# Download from official website
# https://www.postman.com/downloads/

# Install on macOS via Homebrew
brew install --cask postman

# Install on Windows via Chocolatey
choco install postman

# Install on Ubuntu/Debian
wget https://dl.pstmn.io/download/latest/linux64 -O postman-linux-x64.tar.gz
tar -xzf postman-linux-x64.tar.gz
sudo mv Postman /opt/
sudo ln -s /opt/Postman/Postman /usr/local/bin/postman
```

### CLI (Newman)
```bash
# Install Newman for command-line execution
npm install -g newman

# Install additional reporters
npm install -g newman-reporter-html
npm install -g newman-reporter-htmlextra
npm install -g newman-reporter-confluence

# Verify installation
newman --version
```

## Basic Usage

### Creating Collections
```javascript
// Collection structure example
{
  "info": {
    "name": "API Test Suite",
    "description": "Comprehensive API testing collection",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{authToken}}",
        "type": "string"
      }
    ]
  },
  "variable": [
    {
      "key": "baseUrl",
      "value": "https://api.example.com",
      "type": "string"
    },
    {
      "key": "version",
      "value": "v1",
      "type": "string"
    }
  ]
}
```

### Environment Configuration
```json
{
  "name": "Development",
  "values": [
    {
      "key": "baseUrl",
      "value": "https://dev-api.example.com",
      "enabled": true
    },
    {
      "key": "authToken",
      "value": "dev-token-123",
      "enabled": true,
      "type": "secret"
    },
    {
      "key": "userId",
      "value": "test-user-123",
      "enabled": true
    },
    {
      "key": "timeout",
      "value": "5000",
      "enabled": true
    }
  ]
}
```

### Request Examples
```javascript
// GET Request with authentication
pm.sendRequest({
    url: pm.environment.get("baseUrl") + "/api/users",
    method: 'GET',
    header: {
        'Authorization': 'Bearer ' + pm.environment.get("authToken"),
        'Content-Type': 'application/json'
    }
}, function (err, response) {
    console.log(response.json());
});

// POST Request with dynamic data
const requestBody = {
    name: pm.variables.replaceIn("{{$randomFullName}}"),
    email: pm.variables.replaceIn("{{$randomEmail}}"),
    age: pm.variables.replaceIn("{{$randomInt}}"),
    timestamp: new Date().toISOString()
};

pm.sendRequest({
    url: pm.environment.get("baseUrl") + "/api/users",
    method: 'POST',
    header: {
        'Authorization': 'Bearer ' + pm.environment.get("authToken"),
        'Content-Type': 'application/json'
    },
    body: {
        mode: 'raw',
        raw: JSON.stringify(requestBody)
    }
}, function (err, response) {
    if (response.code === 201) {
        pm.environment.set("newUserId", response.json().id);
    }
});
```

## Testing and Assertions

### Basic Test Scripts
```javascript
// Pre-request Script
// Set authentication token
pm.sendRequest({
    url: pm.environment.get("authUrl") + "/oauth/token",
    method: 'POST',
    header: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: {
        mode: 'urlencoded',
        urlencoded: [
            {key: "grant_type", value: "client_credentials"},
            {key: "client_id", value: pm.environment.get("clientId")},
            {key: "client_secret", value: pm.environment.get("clientSecret")}
        ]
    }
}, function (err, response) {
    if (response.code === 200) {
        const token = response.json().access_token;
        pm.environment.set("authToken", token);
    }
});

// Test Script (Post-response)
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

pm.test("Response has required headers", function () {
    pm.response.to.have.header("Content-Type");
    pm.response.to.have.header("X-Rate-Limit-Remaining");
});

pm.test("Response body contains expected data", function () {
    const responseJson = pm.response.json();
    
    pm.expect(responseJson).to.have.property('data');
    pm.expect(responseJson.data).to.be.an('array');
    pm.expect(responseJson.data.length).to.be.greaterThan(0);
    
    // Validate first item structure
    const firstItem = responseJson.data[0];
    pm.expect(firstItem).to.have.property('id');
    pm.expect(firstItem).to.have.property('name');
    pm.expect(firstItem).to.have.property('email');
    pm.expect(firstItem.email).to.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
});

pm.test("Response schema validation", function () {
    const schema = {
        type: "object",
        properties: {
            data: {
                type: "array",
                items: {
                    type: "object",
                    properties: {
                        id: { type: "string" },
                        name: { type: "string" },
                        email: { type: "string", format: "email" },
                        created_at: { type: "string", format: "date-time" }
                    },
                    required: ["id", "name", "email"]
                }
            },
            pagination: {
                type: "object",
                properties: {
                    page: { type: "number" },
                    per_page: { type: "number" },
                    total: { type: "number" }
                }
            }
        },
        required: ["data"]
    };
    
    pm.response.to.have.jsonSchema(schema);
});
```

### Advanced Testing Patterns
```javascript
// Dynamic variable creation
pm.test("Extract and store user ID", function () {
    const responseJson = pm.response.json();
    if (responseJson.data && responseJson.data.length > 0) {
        pm.environment.set("testUserId", responseJson.data[0].id);
        pm.globals.set("lastUserCreated", responseJson.data[0].id);
    }
});

// Conditional testing
pm.test("Conditional validation based on response", function () {
    const responseJson = pm.response.json();
    
    if (responseJson.type === "premium") {
        pm.expect(responseJson).to.have.property('features');
        pm.expect(responseJson.features).to.include('advanced_analytics');
    } else if (responseJson.type === "basic") {
        pm.expect(responseJson.features).to.not.include('advanced_analytics');
    }
});

// Array validation
pm.test("Validate array contents", function () {
    const responseJson = pm.response.json();
    
    pm.expect(responseJson.users).to.be.an('array');
    
    responseJson.users.forEach((user, index) => {
        pm.test(`User ${index} has valid structure`, function () {
            pm.expect(user).to.have.property('id').that.is.a('string');
            pm.expect(user).to.have.property('email').that.matches(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
            pm.expect(user).to.have.property('status').that.is.oneOf(['active', 'inactive', 'pending']);
        });
    });
});

// Error handling tests
pm.test("Handle error responses gracefully", function () {
    if (pm.response.code >= 400) {
        const errorResponse = pm.response.json();
        pm.expect(errorResponse).to.have.property('error');
        pm.expect(errorResponse).to.have.property('message');
        pm.expect(errorResponse.error).to.be.a('string');
        
        // Set flag for subsequent requests
        pm.environment.set("hasError", "true");
        pm.environment.set("errorCode", pm.response.code.toString());
    } else {
        pm.environment.unset("hasError");
        pm.environment.unset("errorCode");
    }
});
```

## Automation and CI/CD

### Newman Command Line
```bash
# Run collection
newman run collection.json -e environment.json

# Run with specific options
newman run collection.json \
  --environment environment.json \
  --globals globals.json \
  --iteration-count 10 \
  --delay-request 1000 \
  --timeout-request 30000 \
  --reporters cli,html,json \
  --reporter-html-export report.html \
  --reporter-json-export results.json

# Run specific folder
newman run collection.json -e environment.json --folder "User Management"

# Run with data file for data-driven testing
newman run collection.json -e environment.json -d testdata.csv

# Run with custom reporter
newman run collection.json \
  --reporters htmlextra \
  --reporter-htmlextra-export report.html \
  --reporter-htmlextra-darkTheme
```

### GitHub Actions Integration
```yaml
name: API Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 */6 * * *'  # Run every 6 hours

jobs:
  api-tests:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        environment: [development, staging, production]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install Newman
      run: |
        npm install -g newman
        npm install -g newman-reporter-htmlextra
    
    - name: Create environment file
      run: |
        cat > ${{ matrix.environment }}.json << EOF
        {
          "name": "${{ matrix.environment }}",
          "values": [
            {
              "key": "baseUrl",
              "value": "${{ secrets[format('{0}_BASE_URL', matrix.environment)] }}",
              "enabled": true
            },
            {
              "key": "authToken",
              "value": "${{ secrets[format('{0}_AUTH_TOKEN', matrix.environment)] }}",
              "enabled": true
            }
          ]
        }
        EOF
    
    - name: Run API Tests
      run: |
        newman run tests/api-collection.json \
          --environment ${{ matrix.environment }}.json \
          --reporters cli,htmlextra,json \
          --reporter-htmlextra-export reports/api-test-report-${{ matrix.environment }}.html \
          --reporter-json-export reports/api-test-results-${{ matrix.environment }}.json \
          --color on
    
    - name: Upload test reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: api-test-reports-${{ matrix.environment }}
        path: reports/
    
    - name: Parse test results
      if: always()
      run: |
        if [ -f "reports/api-test-results-${{ matrix.environment }}.json" ]; then
          FAILURES=$(jq '.run.stats.assertions.failed' reports/api-test-results-${{ matrix.environment }}.json)
          TOTAL=$(jq '.run.stats.assertions.total' reports/api-test-results-${{ matrix.environment }}.json)
          echo "::notice::API Tests for ${{ matrix.environment }}: $((TOTAL - FAILURES))/$TOTAL passed"
          
          if [ "$FAILURES" -gt 0 ]; then
            echo "::error::$FAILURES API test(s) failed in ${{ matrix.environment }}"
            exit 1
          fi
        fi
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['development', 'staging', 'production'],
            description: 'Environment to test'
        )
        booleanParam(
            name: 'RUN_LOAD_TESTS',
            defaultValue: false,
            description: 'Run load tests with multiple iterations'
        )
    }
    
    environment {
        NEWMAN_VERSION = '5.3.2'
    }
    
    stages {
        stage('Setup') {
            steps {
                script {
                    sh 'npm install -g newman@${NEWMAN_VERSION}'
                    sh 'npm install -g newman-reporter-htmlextra'
                    sh 'mkdir -p reports'
                }
            }
        }
        
        stage('Prepare Environment') {
            steps {
                script {
                    def envConfig = [
                        name: params.ENVIRONMENT,
                        values: [
                            [
                                key: "baseUrl",
                                value: env["${params.ENVIRONMENT.toUpperCase()}_BASE_URL"],
                                enabled: true
                            ],
                            [
                                key: "authToken", 
                                value: env["${params.ENVIRONMENT.toUpperCase()}_AUTH_TOKEN"],
                                enabled: true
                            ]
                        ]
                    ]
                    
                    writeJSON file: "${params.ENVIRONMENT}.json", json: envConfig
                }
            }
        }
        
        stage('API Tests') {
            parallel {
                stage('Functional Tests') {
                    steps {
                        script {
                            sh """
                                newman run tests/functional-tests.json \\
                                  --environment ${params.ENVIRONMENT}.json \\
                                  --reporters cli,htmlextra,json \\
                                  --reporter-htmlextra-export reports/functional-report.html \\
                                  --reporter-json-export reports/functional-results.json \\
                                  --color on
                            """
                        }
                    }
                }
                
                stage('Security Tests') {
                    steps {
                        script {
                            sh """
                                newman run tests/security-tests.json \\
                                  --environment ${params.ENVIRONMENT}.json \\
                                  --reporters cli,htmlextra,json \\
                                  --reporter-htmlextra-export reports/security-report.html \\
                                  --reporter-json-export reports/security-results.json \\
                                  --color on
                            """
                        }
                    }
                }
                
                stage('Contract Tests') {
                    steps {
                        script {
                            sh """
                                newman run tests/contract-tests.json \\
                                  --environment ${params.ENVIRONMENT}.json \\
                                  --reporters cli,htmlextra,json \\
                                  --reporter-htmlextra-export reports/contract-report.html \\
                                  --reporter-json-export reports/contract-results.json \\
                                  --color on
                            """
                        }
                    }
                }
            }
        }
        
        stage('Load Tests') {
            when {
                expression { params.RUN_LOAD_TESTS }
            }
            steps {
                script {
                    sh """
                        newman run tests/load-tests.json \\
                          --environment ${params.ENVIRONMENT}.json \\
                          --iteration-count 100 \\
                          --delay-request 100 \\
                          --reporters cli,htmlextra,json \\
                          --reporter-htmlextra-export reports/load-report.html \\
                          --reporter-json-export reports/load-results.json \\
                          --color on
                    """
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Archive reports
                archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
                
                // Publish HTML reports
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: '*.html',
                    reportName: 'API Test Reports'
                ])
                
                // Parse and display results
                def results = [:]
                def reportFiles = ['functional-results.json', 'security-results.json', 'contract-results.json']
                
                reportFiles.each { fileName ->
                    if (fileExists("reports/${fileName}")) {
                        def result = readJSON file: "reports/${fileName}"
                        def testType = fileName.replace('-results.json', '')
                        results[testType] = [
                            total: result.run.stats.assertions.total,
                            failed: result.run.stats.assertions.failed,
                            passed: result.run.stats.assertions.total - result.run.stats.assertions.failed
                        ]
                    }
                }
                
                // Create summary
                def summary = results.collect { type, stats ->
                    "${type}: ${stats.passed}/${stats.total} passed"
                }.join(', ')
                
                currentBuild.description = "API Tests - ${summary}"
                
                // Fail build if any tests failed
                def totalFailures = results.values().sum { it.failed } ?: 0
                if (totalFailures > 0) {
                    error("${totalFailures} API test(s) failed")
                }
            }
        }
    }
}
```

## Data-Driven Testing

### CSV Data Files
```csv
# testdata.csv
username,email,password,expectedStatus
john_doe,john@example.com,password123,201
jane_smith,jane@example.com,securepass456,201
invalid_user,invalid-email,weak,400
```

### JSON Data Files
```json
[
  {
    "scenario": "successful_login",
    "username": "testuser1",
    "password": "correctpassword",
    "expectedStatus": 200,
    "expectedMessage": "Login successful"
  },
  {
    "scenario": "invalid_credentials", 
    "username": "testuser1",
    "password": "wrongpassword",
    "expectedStatus": 401,
    "expectedMessage": "Invalid credentials"
  },
  {
    "scenario": "missing_username",
    "username": "",
    "password": "password123",
    "expectedStatus": 400,
    "expectedMessage": "Username required"
  }
]
```

### Data-Driven Test Scripts
```javascript
// Using data in request body
const testData = pm.iterationData.toObject();

pm.sendRequest({
    url: pm.environment.get("baseUrl") + "/api/auth/login",
    method: 'POST',
    header: {
        'Content-Type': 'application/json'
    },
    body: {
        mode: 'raw',
        raw: JSON.stringify({
            username: testData.username,
            password: testData.password
        })
    }
}, function (err, response) {
    pm.test(`${testData.scenario} - Status code check`, function () {
        pm.expect(response.code).to.equal(testData.expectedStatus);
    });
    
    pm.test(`${testData.scenario} - Message check`, function () {
        const responseJson = response.json();
        pm.expect(responseJson.message).to.equal(testData.expectedMessage);
    });
});
```

## Mock Servers

### Creating Mock Servers
```javascript
// Mock server configuration
{
  "name": "User API Mock",
  "description": "Mock server for user management API",
  "config": {
    "headers": [
      {
        "key": "Content-Type",
        "value": "application/json"
      },
      {
        "key": "X-Mock-Response-Code",
        "value": "{{responseCode}}"
      }
    ],
    "delay": {
      "type": "fixed",
      "value": 100
    }
  }
}

// Mock response examples
const mockResponses = {
  "GET /api/users": {
    "status": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "data": [
        {
          "id": "{{$guid}}",
          "name": "{{$randomFullName}}",
          "email": "{{$randomEmail}}",
          "created_at": "{{$isoTimestamp}}"
        }
      ],
      "pagination": {
        "page": 1,
        "per_page": 10,
        "total": 1
      }
    }
  },
  
  "POST /api/users": {
    "status": 201,
    "headers": {
      "Content-Type": "application/json",
      "Location": "/api/users/{{$guid}}"
    },
    "body": {
      "id": "{{$guid}}",
      "name": "{{name}}",
      "email": "{{email}}",
      "created_at": "{{$isoTimestamp}}",
      "updated_at": "{{$isoTimestamp}}"
    }
  },
  
  "GET /api/users/:id": {
    "status": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "id": "{{id}}",
      "name": "{{$randomFullName}}",
      "email": "{{$randomEmail}}",
      "profile": {
        "bio": "{{$randomLoremSentence}}",
        "avatar": "https://randomuser.me/api/portraits/{{$randomGender}}/{{$randomInt}}.jpg"
      },
      "created_at": "{{$isoTimestamp}}",
      "updated_at": "{{$isoTimestamp}}"
    }
  }
};
```

### Dynamic Mock Responses
```javascript
// Pre-request script for dynamic mocking
const mockData = {
    users: [
        { id: 1, name: "John Doe", email: "john@example.com", status: "active" },
        { id: 2, name: "Jane Smith", email: "jane@example.com", status: "inactive" },
        { id: 3, name: "Bob Johnson", email: "bob@example.com", status: "pending" }
    ]
};

// Store mock data in environment
pm.environment.set("mockUsers", JSON.stringify(mockData.users));

// Dynamic response based on query parameters
const url = new URL(pm.request.url);
const status = url.searchParams.get('status');
const page = parseInt(url.searchParams.get('page')) || 1;
const limit = parseInt(url.searchParams.get('limit')) || 10;

let filteredUsers = mockData.users;
if (status) {
    filteredUsers = mockData.users.filter(user => user.status === status);
}

// Pagination
const startIndex = (page - 1) * limit;
const endIndex = startIndex + limit;
const paginatedUsers = filteredUsers.slice(startIndex, endIndex);

const response = {
    data: paginatedUsers,
    pagination: {
        page: page,
        per_page: limit,
        total: filteredUsers.length,
        total_pages: Math.ceil(filteredUsers.length / limit)
    }
};

pm.environment.set("mockResponse", JSON.stringify(response));
```

## API Documentation

### Automatic Documentation Generation
```javascript
// Documentation script
pm.test("Generate API documentation", function () {
    const request = pm.request;
    const response = pm.response;
    
    const documentation = {
        endpoint: {
            method: request.method,
            url: request.url.toString(),
            description: pm.info.requestName || "API endpoint"
        },
        headers: {
            request: request.headers.toObject(),
            response: response.headers.toObject()
        },
        body: {
            request: request.body ? request.body.raw : null,
            response: response.text()
        },
        examples: {
            request: {
                method: request.method,
                url: request.url.toString(),
                headers: request.headers.toObject(),
                body: request.body ? JSON.parse(request.body.raw) : null
            },
            response: {
                status: response.code,
                headers: response.headers.toObject(),
                body: response.json()
            }
        },
        tests: pm.test.list(),
        timestamp: new Date().toISOString()
    };
    
    // Store documentation
    pm.environment.set(`doc_${request.method}_${request.url.getPath()}`, 
                      JSON.stringify(documentation));
});
```

### OpenAPI Spec Generation
```javascript
// Generate OpenAPI specification
const generateOpenAPISpec = () => {
    const spec = {
        openapi: "3.0.0",
        info: {
            title: "API Documentation",
            version: "1.0.0",
            description: "Auto-generated API documentation from Postman tests"
        },
        servers: [
            {
                url: pm.environment.get("baseUrl"),
                description: "API Server"
            }
        ],
        paths: {},
        components: {
            schemas: {},
            securitySchemes: {
                bearerAuth: {
                    type: "http",
                    scheme: "bearer",
                    bearerFormat: "JWT"
                }
            }
        }
    };
    
    // Extract path information from current request
    const path = pm.request.url.getPath();
    const method = pm.request.method.toLowerCase();
    
    if (!spec.paths[path]) {
        spec.paths[path] = {};
    }
    
    spec.paths[path][method] = {
        summary: pm.info.requestName,
        description: pm.request.description || `${method.toUpperCase()} ${path}`,
        parameters: extractParameters(),
        requestBody: extractRequestBody(),
        responses: extractResponses(),
        security: [{ bearerAuth: [] }]
    };
    
    return spec;
};

const extractParameters = () => {
    const params = [];
    const url = pm.request.url;
    
    // Query parameters
    url.query.each(param => {
        params.push({
            name: param.key,
            in: "query",
            required: false,
            schema: { type: "string" },
            example: param.value
        });
    });
    
    // Path parameters
    const pathParams = url.getPath().match(/:(\w+)/g);
    if (pathParams) {
        pathParams.forEach(param => {
            params.push({
                name: param.substring(1),
                in: "path",
                required: true,
                schema: { type: "string" }
            });
        });
    }
    
    return params;
};
```

## Performance Testing

### Load Testing with Newman
```javascript
// Load test configuration
const loadTestConfig = {
    collection: "load-test-collection.json",
    environment: "production.json",
    iterationCount: 1000,
    delay: 50, // ms between requests
    timeout: 30000, // 30 second timeout
    reporters: ["cli", "json"],
    reporterOptions: {
        json: {
            export: "load-test-results.json"
        }
    }
};

// Performance monitoring script
pm.test("Response time performance", function () {
    const responseTime = pm.response.responseTime;
    const maxResponseTime = pm.environment.get("maxResponseTime") || 2000;
    
    pm.expect(responseTime).to.be.below(maxResponseTime, 
        `Response time ${responseTime}ms exceeded maximum ${maxResponseTime}ms`);
    
    // Log performance metrics
    console.log(`Response Time: ${responseTime}ms`);
    console.log(`Content Size: ${pm.response.responseSize} bytes`);
    
    // Store metrics for analysis
    const metrics = JSON.parse(pm.environment.get("performanceMetrics") || "[]");
    metrics.push({
        timestamp: new Date().toISOString(),
        endpoint: pm.request.url.toString(),
        method: pm.request.method,
        responseTime: responseTime,
        responseSize: pm.response.responseSize,
        statusCode: pm.response.code
    });
    
    // Keep only last 100 measurements
    if (metrics.length > 100) {
        metrics.shift();
    }
    
    pm.environment.set("performanceMetrics", JSON.stringify(metrics));
});

// Memory usage monitoring
pm.test("Memory usage check", function () {
    const beforeMemory = pm.environment.get("beforeMemory");
    const currentMemory = process.memoryUsage();
    
    if (beforeMemory) {
        const memoryDiff = currentMemory.heapUsed - JSON.parse(beforeMemory).heapUsed;
        console.log(`Memory diff: ${memoryDiff} bytes`);
        
        // Alert if memory usage increased significantly
        if (memoryDiff > 10 * 1024 * 1024) { // 10MB
            console.warn("High memory usage detected");
        }
    }
    
    pm.environment.set("beforeMemory", JSON.stringify(currentMemory));
});
```

## Security Testing

### Authentication Testing
```javascript
// OAuth 2.0 flow testing
pm.test("OAuth 2.0 authentication flow", function () {
    // Step 1: Get authorization code
    pm.sendRequest({
        url: pm.environment.get("authUrl") + "/oauth/authorize",
        method: 'GET',
        header: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {
            mode: 'urlencoded',
            urlencoded: [
                {key: "response_type", value: "code"},
                {key: "client_id", value: pm.environment.get("clientId")},
                {key: "redirect_uri", value: pm.environment.get("redirectUri")},
                {key: "scope", value: "read write"}
            ]
        }
    }, function (err, response) {
        // Extract authorization code from redirect
        const authCode = extractAuthCodeFromResponse(response);
        pm.environment.set("authCode", authCode);
        
        // Step 2: Exchange code for token
        pm.sendRequest({
            url: pm.environment.get("authUrl") + "/oauth/token",
            method: 'POST',
            header: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: {
                mode: 'urlencoded',
                urlencoded: [
                    {key: "grant_type", value: "authorization_code"},
                    {key: "code", value: authCode},
                    {key: "client_id", value: pm.environment.get("clientId")},
                    {key: "client_secret", value: pm.environment.get("clientSecret")},
                    {key: "redirect_uri", value: pm.environment.get("redirectUri")}
                ]
            }
        }, function (err, tokenResponse) {
            pm.test("Token exchange successful", function () {
                pm.expect(tokenResponse.code).to.equal(200);
                
                const tokenData = tokenResponse.json();
                pm.expect(tokenData).to.have.property('access_token');
                pm.expect(tokenData).to.have.property('token_type');
                pm.expect(tokenData.token_type).to.equal('Bearer');
                
                pm.environment.set("accessToken", tokenData.access_token);
                if (tokenData.refresh_token) {
                    pm.environment.set("refreshToken", tokenData.refresh_token);
                }
            });
        });
    });
});

// JWT token validation
pm.test("JWT token validation", function () {
    const token = pm.environment.get("accessToken");
    
    if (token) {
        // Decode JWT (note: this doesn't verify signature)
        const payload = JSON.parse(atob(token.split('.')[1]));
        
        pm.test("JWT has required claims", function () {
            pm.expect(payload).to.have.property('sub'); // Subject
            pm.expect(payload).to.have.property('exp'); // Expiration
            pm.expect(payload).to.have.property('iat'); // Issued at
        });
        
        pm.test("JWT is not expired", function () {
            const currentTime = Math.floor(Date.now() / 1000);
            pm.expect(payload.exp).to.be.greaterThan(currentTime);
        });
        
        pm.test("JWT has valid issuer", function () {
            pm.expect(payload.iss).to.equal(pm.environment.get("expectedIssuer"));
        });
    }
});
```

### Security Headers Testing
```javascript
pm.test("Security headers validation", function () {
    const securityHeaders = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': ['DENY', 'SAMEORIGIN'],
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': /max-age=\d+/,
        'Content-Security-Policy': /.+/,
        'Referrer-Policy': ['strict-origin-when-cross-origin', 'no-referrer', 'strict-origin']
    };
    
    Object.keys(securityHeaders).forEach(headerName => {
        const expectedValue = securityHeaders[headerName];
        const actualValue = pm.response.headers.get(headerName);
        
        pm.test(`${headerName} header is present`, function () {
            pm.expect(actualValue).to.not.be.null;
        });
        
        if (actualValue) {
            if (Array.isArray(expectedValue)) {
                pm.test(`${headerName} has valid value`, function () {
                    pm.expect(expectedValue).to.include(actualValue);
                });
            } else if (expectedValue instanceof RegExp) {
                pm.test(`${headerName} matches pattern`, function () {
                    pm.expect(actualValue).to.match(expectedValue);
                });
            } else if (typeof expectedValue === 'string') {
                pm.test(`${headerName} has correct value`, function () {
                    pm.expect(actualValue).to.equal(expectedValue);
                });
            }
        }
    });
});

// Input validation testing
pm.test("SQL injection protection", function () {
    const maliciousInputs = [
        "'; DROP TABLE users; --",
        "1' OR '1'='1",
        "admin'/*",
        "1; EXEC xp_cmdshell('dir')",
        "1' UNION SELECT null,null,null--"
    ];
    
    maliciousInputs.forEach((maliciousInput, index) => {
        pm.sendRequest({
            url: pm.environment.get("baseUrl") + "/api/users/search",
            method: 'GET',
            header: {
                'Authorization': 'Bearer ' + pm.environment.get("authToken")
            },
            url: pm.environment.get("baseUrl") + "/api/users/search?q=" + encodeURIComponent(maliciousInput)
        }, function (err, response) {
            pm.test(`SQL injection test ${index + 1}`, function () {
                // Should not return 500 error or expose database errors
                pm.expect(response.code).to.not.equal(500);
                
                const responseText = response.text().toLowerCase();
                const sqlErrorKeywords = ['sql', 'mysql', 'postgresql', 'oracle', 'syntax error', 'column', 'table'];
                
                sqlErrorKeywords.forEach(keyword => {
                    pm.expect(responseText).to.not.include(keyword);
                });
            });
        });
    });
});
```

## Resources

- [Postman Documentation](https://learning.postman.com/docs/)
- [Newman Documentation](https://github.com/postmanlabs/newman)
- [Postman API](https://docs.api.getpostman.com/)
- [Collection Format](https://schema.postman.com/collection/v2.1.0/docs/index.html)
- [Postman Scripts](https://learning.postman.com/docs/writing-scripts/intro-to-scripts/)
- [Testing Examples](https://github.com/postmanlabs/postman-docs)
- [Mock Servers](https://learning.postman.com/docs/designing-and-developing-your-api/mocking-data/setting-up-mock/)
- [Monitors](https://learning.postman.com/docs/monitoring-your-api/intro-monitors/)
- [Workspaces](https://learning.postman.com/docs/collaborating-in-postman/using-workspaces/creating-workspaces/)
- [Community Forum](https://community.postman.com/)