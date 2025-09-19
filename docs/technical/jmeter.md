# JMeter

Apache JMeter is an open-source load testing tool designed to analyze and measure the performance of web applications, databases, FTP servers, and other services. It supports various protocols and provides a comprehensive GUI for test creation and execution.

## Installation

### GUI Installation
```bash
# Download from Apache JMeter website
# https://jmeter.apache.org/download_jmeter.cgi

# Install on macOS via Homebrew
brew install jmeter

# Install on Windows
# Download ZIP file and extract
# Ensure Java 8+ is installed

# Install on Linux
cd /opt
sudo wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.5.tgz
sudo tar -xzf apache-jmeter-5.5.tgz
sudo ln -s /opt/apache-jmeter-5.5/bin/jmeter /usr/local/bin/jmeter

# Verify installation
jmeter --version
```

### Docker
```bash
# Run JMeter in headless mode
docker run --rm -v $(pwd):/tests justb4/jmeter -n -t /tests/test-plan.jmx -l /tests/results.jtl

# Run with GUI (requires X11 forwarding)
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd):/tests justb4/jmeter

# Custom Docker image with plugins
FROM justb4/jmeter:latest
RUN wget -O /opt/apache-jmeter/lib/ext/jmeter-plugins-manager.jar \
    https://jmeter-plugins.org/get/

# Run JMeter with custom heap size
docker run --rm -e JVM_ARGS="-Xms1g -Xmx4g" -v $(pwd):/tests justb4/jmeter
```

## Basic Test Plan Structure

### Simple HTTP Test Plan
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.5">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="API Load Test">
      <stringProp name="TestPlan.comments">Basic API load test</stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.arguments" elementType="Arguments" guiclass="ArgumentsPanel">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    <hashTree>
      <!-- Thread Group -->
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Users">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">10</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">50</stringProp>
        <stringProp name="ThreadGroup.ramp_time">300</stringProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
        <stringProp name="ThreadGroup.duration">600</stringProp>
        <stringProp name="ThreadGroup.delay">0</stringProp>
      </ThreadGroup>
      <hashTree>
        <!-- HTTP Request Defaults -->
        <ConfigTestElement guiclass="HttpDefaultsGui" testclass="ConfigTestElement" testname="HTTP Request Defaults">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
            <collectionProp name="Arguments.arguments"/>
          </elementProp>
          <stringProp name="HTTPSampler.domain">api.example.com</stringProp>
          <stringProp name="HTTPSampler.port">443</stringProp>
          <stringProp name="HTTPSampler.protocol">https</stringProp>
          <stringProp name="HTTPSampler.contentEncoding"></stringProp>
          <stringProp name="HTTPSampler.path"></stringProp>
        </ConfigTestElement>
        <hashTree/>
        
        <!-- HTTP Header Manager -->
        <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP Header Manager">
          <collectionProp name="HeaderManager.headers">
            <elementProp name="" elementType="Header">
              <stringProp name="Header.name">Content-Type</stringProp>
              <stringProp name="Header.value">application/json</stringProp>
            </elementProp>
            <elementProp name="" elementType="Header">
              <stringProp name="Header.name">Authorization</stringProp>
              <stringProp name="Header.value">Bearer ${auth_token}</stringProp>
            </elementProp>
          </collectionProp>
        </HeaderManager>
        <hashTree/>
        
        <!-- HTTP Request -->
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="GET /api/users">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
            <collectionProp name="Arguments.arguments"/>
          </elementProp>
          <stringProp name="HTTPSampler.domain"></stringProp>
          <stringProp name="HTTPSampler.port"></stringProp>
          <stringProp name="HTTPSampler.protocol"></stringProp>
          <stringProp name="HTTPSampler.contentEncoding"></stringProp>
          <stringProp name="HTTPSampler.path">/api/users</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout">30000</stringProp>
          <stringProp name="HTTPSampler.response_timeout">30000</stringProp>
        </HTTPSamplerProxy>
        <hashTree>
          <!-- Response Assertion -->
          <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="Response Code Assertion">
            <collectionProp name="Asserion.test_strings">
              <stringProp name="49586">200</stringProp>
            </collectionProp>
            <stringProp name="Assertion.custom_message"></stringProp>
            <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">1</intProp>
          </ResponseAssertion>
          <hashTree/>
          
          <!-- Duration Assertion -->
          <DurationAssertion guiclass="DurationAssertionGui" testclass="DurationAssertion" testname="Duration Assertion">
            <stringProp name="DurationAssertion.duration">2000</stringProp>
          </DurationAssertion>
          <hashTree/>
        </hashTree>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

## Advanced Configuration

### User Defined Variables
```xml
<!-- User Defined Variables -->
<Arguments guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables">
  <collectionProp name="Arguments.arguments">
    <elementProp name="base_url" elementType="Argument">
      <stringProp name="Argument.name">base_url</stringProp>
      <stringProp name="Argument.value">https://api.example.com</stringProp>
      <stringProp name="Argument.metadata">=</stringProp>
    </elementProp>
    <elementProp name="users_endpoint" elementType="Argument">
      <stringProp name="Argument.name">users_endpoint</stringProp>
      <stringProp name="Argument.value">/api/v1/users</stringProp>
      <stringProp name="Argument.metadata">=</stringProp>
    </elementProp>
    <elementProp name="auth_token" elementType="Argument">
      <stringProp name="Argument.name">auth_token</stringProp>
      <stringProp name="Argument.value">${__P(auth.token,default_token)}</stringProp>
      <stringProp name="Argument.metadata">=</stringProp>
    </elementProp>
  </collectionProp>
</Arguments>
```

### CSV Data Set Configuration
```xml
<!-- CSV Data Set Config -->
<CSVDataSet guiclass="TestBeanGUI" testclass="CSVDataSet" testname="User Credentials">
  <stringProp name="filename">users.csv</stringProp>
  <stringProp name="fileEncoding">UTF-8</stringProp>
  <stringProp name="variableNames">username,password,email</stringProp>
  <boolProp name="ignoreFirstLine">true</boolProp>
  <stringProp name="delimiter">,</stringProp>
  <boolProp name="quotedData">false</boolProp>
  <boolProp name="recycle">true</boolProp>
  <boolProp name="stopThread">false</boolProp>
  <stringProp name="shareMode">shareMode.all</stringProp>
</CSVDataSet>
```

### JSON Extractor
```xml
<!-- JSON Extractor -->
<JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="Extract User ID">
  <stringProp name="JSONPostProcessor.referenceNames">user_id</stringProp>
  <stringProp name="JSONPostProcessor.jsonPathExprs">$.data[0].id</stringProp>
  <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
  <stringProp name="JSONPostProcessor.defaultValues">NOT_FOUND</stringProp>
  <boolProp name="JSONPostProcessor.compute_concat">false</boolProp>
</JSONPostProcessor>
```

## Load Testing Patterns

### Stepping Thread Group
```xml
<!-- Stepping Thread Group (requires jp@gc - Stepping Thread Group plugin) -->
<kg.apc.jmeter.threads.SteppingThreadGroup guiclass="kg.apc.jmeter.threads.SteppingThreadGroupGui" testclass="kg.apc.jmeter.threads.SteppingThreadGroup" testname="Stepping Thread Group">
  <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
  <stringProp name="ThreadGroup.num_threads">100</stringProp>
  <stringProp name="Threads initial delay">0</stringProp>
  <stringProp name="Start users count">10</stringProp>
  <stringProp name="Start users count burst">5</stringProp>
  <stringProp name="Start users period">30</stringProp>
  <stringProp name="Stop users count">5</stringProp>
  <stringProp name="Stop users period">30</stringProp>
  <stringProp name="flighttime">300</stringProp>
  <elementProp name="ThreadGroup.main_controller" elementType="LoopController">
    <boolProp name="LoopController.continue_forever">false</boolProp>
    <intProp name="LoopController.loops">-1</intProp>
  </elementProp>
</kg.apc.jmeter.threads.SteppingThreadGroup>
```

### Ultimate Thread Group
```xml
<!-- Ultimate Thread Group (requires jp@gc - Ultimate Thread Group plugin) -->
<kg.apc.jmeter.threads.UltimateThreadGroup guiclass="kg.apc.jmeter.threads.UltimateThreadGroupGui" testclass="kg.apc.jmeter.threads.UltimateThreadGroup" testname="Ultimate Thread Group">
  <collectionProp name="ultimatethreadgroupdata">
    <!-- Stage 1: Ramp up -->
    <collectionProp name="1800859373">
      <stringProp name="1768">50</stringProp>   <!-- threads -->
      <stringProp name="0">0</stringProp>     <!-- initial delay -->
      <stringProp name="48625">120</stringProp> <!-- startup time -->
      <stringProp name="53342">300</stringProp> <!-- hold load time -->
      <stringProp name="1598">10</stringProp>   <!-- shutdown time -->
    </collectionProp>
    <!-- Stage 2: Peak load -->
    <collectionProp name="1800859374">
      <stringProp name="49710">100</stringProp> <!-- threads -->
      <stringProp name="1598">10</stringProp>   <!-- initial delay -->
      <stringProp name="48625">120</stringProp> <!-- startup time -->
      <stringProp name="53342">600</stringProp> <!-- hold load time -->
      <stringProp name="48625">120</stringProp> <!-- shutdown time -->
    </collectionProp>
  </collectionProp>
  <elementProp name="ThreadGroup.main_controller" elementType="LoopController">
    <boolProp name="LoopController.continue_forever">false</boolProp>
    <intProp name="LoopController.loops">-1</intProp>
  </elementProp>
  <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
</kg.apc.jmeter.threads.UltimateThreadGroup>
```

## API Testing Examples

### RESTful API Test Suite
```xml
<!-- Login Request -->
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="POST /auth/login">
  <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
    <collectionProp name="Arguments.arguments">
      <elementProp name="" elementType="HTTPArgument">
        <boolProp name="HTTPArgument.always_encode">false</boolProp>
        <stringProp name="Argument.value">{
  "username": "${username}",
  "password": "${password}"
}</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
  <stringProp name="HTTPSampler.domain"></stringProp>
  <stringProp name="HTTPSampler.port"></stringProp>
  <stringProp name="HTTPSampler.protocol"></stringProp>
  <stringProp name="HTTPSampler.contentEncoding"></stringProp>
  <stringProp name="HTTPSampler.path">/auth/login</stringProp>
  <stringProp name="HTTPSampler.method">POST</stringProp>
</HTTPSamplerProxy>

<!-- Extract token from login response -->
<JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="Extract Auth Token">
  <stringProp name="JSONPostProcessor.referenceNames">auth_token</stringProp>
  <stringProp name="JSONPostProcessor.jsonPathExprs">$.access_token</stringProp>
  <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
  <stringProp name="JSONPostProcessor.defaultValues">NO_TOKEN</stringProp>
</JSONPostProcessor>

<!-- Create User Request -->
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="POST /api/users">
  <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
    <collectionProp name="Arguments.arguments">
      <elementProp name="" elementType="HTTPArgument">
        <boolProp name="HTTPArgument.always_encode">false</boolProp>
        <stringProp name="Argument.value">{
  "name": "${__RandomString(10,abcdefghijklmnopqrstuvwxyz)}",
  "email": "${__time(MM-dd-yyyy,)}@example.com",
  "role": "user"
}</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
  <stringProp name="HTTPSampler.path">/api/users</stringProp>
  <stringProp name="HTTPSampler.method">POST</stringProp>
</HTTPSamplerProxy>
```

### Database Testing
```xml
<!-- JDBC Connection Configuration -->
<JDBCDataSource guiclass="TestBeanGUI" testclass="JDBCDataSource" testname="Database Connection">
  <boolProp name="autocommit">true</boolProp>
  <stringProp name="checkQuery">SELECT 1</stringProp>
  <stringProp name="connectionAge">5000</stringProp>
  <stringProp name="dataSource">mydb</stringProp>
  <stringProp name="dbUrl">jdbc:postgresql://localhost:5432/testdb</stringProp>
  <stringProp name="driver">org.postgresql.Driver</stringProp>
  <stringProp name="password">password</stringProp>
  <stringProp name="poolMax">10</stringProp>
  <stringProp name="timeout">10000</stringProp>
  <stringProp name="trimInterval">60000</stringProp>
  <stringProp name="username">testuser</stringProp>
</JDBCDataSource>

<!-- JDBC Request -->
<JDBCSampler guiclass="TestBeanGUI" testclass="JDBCSampler" testname="Database Query">
  <stringProp name="dataSource">mydb</stringProp>
  <stringProp name="queryType">Select Statement</stringProp>
  <stringProp name="query">SELECT id, name, email, created_at 
FROM users 
WHERE status = 'active' 
ORDER BY created_at DESC 
LIMIT 100</stringProp>
  <stringProp name="queryArguments"></stringProp>
  <stringProp name="queryArgumentsTypes"></stringProp>
  <stringProp name="resultVariable">db_results</stringProp>
  <stringProp name="variableNames">user_id,user_name,user_email,created_date</stringProp>
  <stringProp name="resultSetHandler">Store as String</stringProp>
  <intProp name="queryTimeout">0</intProp>
</JDBCSampler>
```

## Performance Testing Scripts

### Command Line Execution
```bash
#!/bin/bash
# run-load-test.sh

# Set JMeter home
export JMETER_HOME=/opt/apache-jmeter-5.5
export PATH=$JMETER_HOME/bin:$PATH

# Test parameters
TEST_PLAN="load-test.jmx"
RESULT_FILE="results-$(date +%Y%m%d_%H%M%S).jtl"
REPORT_DIR="report-$(date +%Y%m%d_%H%M%S)"
LOG_LEVEL="INFO"

# JVM options
export JVM_ARGS="-Xms1g -Xmx4g -XX:MaxMetaspaceSize=256m"

# Run test in non-GUI mode
jmeter -n \
  -t ${TEST_PLAN} \
  -l ${RESULT_FILE} \
  -e \
  -o ${REPORT_DIR} \
  -Jjmeter.reportgenerator.overall_granularity=60000 \
  -Jjmeter.save.saveservice.output_format=xml \
  -Jjmeter.save.saveservice.response_data=true \
  -Jjmeter.save.saveservice.samplerData=true \
  -Jjmeter.save.saveservice.requestHeaders=true \
  -Jjmeter.save.saveservice.responseHeaders=true \
  -Jlog_level.jmeter=${LOG_LEVEL} \
  -Jbase.url=${BASE_URL:-"https://api.example.com"} \
  -Jauth.token=${AUTH_TOKEN} \
  -Jthread.count=${THREAD_COUNT:-50} \
  -Jramp.duration=${RAMP_DURATION:-300} \
  -Jtest.duration=${TEST_DURATION:-600}

# Check test results
if [ $? -eq 0 ]; then
    echo "Test completed successfully"
    echo "Results: ${RESULT_FILE}"
    echo "Report: ${REPORT_DIR}/index.html"
    
    # Parse results for CI/CD
    ERROR_RATE=$(awk -F',' 'NR>1 && $8=="false" {errors++} NR>1 {total++} END {print (errors/total)*100}' ${RESULT_FILE})
    AVG_RESPONSE_TIME=$(awk -F',' 'NR>1 {sum+=$2; count++} END {print sum/count}' ${RESULT_FILE})
    
    echo "Error Rate: ${ERROR_RATE}%"
    echo "Average Response Time: ${AVG_RESPONSE_TIME}ms"
    
    # Fail if error rate > 5%
    if (( $(echo "${ERROR_RATE} > 5" | bc -l) )); then
        echo "ERROR: Error rate too high (${ERROR_RATE}%)"
        exit 1
    fi
else
    echo "Test failed"
    exit 1
fi
```

### Distributed Testing
```bash
#!/bin/bash
# distributed-test.sh

# Master and slave configuration
MASTER_HOST="master.example.com"
SLAVE_HOSTS="slave1.example.com,slave2.example.com,slave3.example.com"

# Start JMeter in server mode on slaves
ssh_command() {
    local host=$1
    local command=$2
    ssh -o StrictHostKeyChecking=no ${host} "${command}"
}

# Start slaves
for slave in $(echo $SLAVE_HOSTS | tr ',' ' '); do
    echo "Starting JMeter slave on ${slave}"
    ssh_command ${slave} "nohup ${JMETER_HOME}/bin/jmeter-server > jmeter-slave.log 2>&1 &"
done

# Wait for slaves to start
sleep 10

# Run distributed test from master
jmeter -n \
  -t distributed-test.jmx \
  -l distributed-results.jtl \
  -e \
  -o distributed-report \
  -R ${SLAVE_HOSTS} \
  -Jjmeter.engine.remote.batch_queue_size=1000 \
  -Jserver.rmi.ssl.disable=true

# Cleanup slaves
for slave in $(echo $SLAVE_HOSTS | tr ',' ' '); do
    echo "Stopping JMeter slave on ${slave}"
    ssh_command ${slave} "pkill -f jmeter-server"
done
```

## CI/CD Integration

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'TEST_TYPE',
            choices: ['smoke', 'load', 'stress', 'spike'],
            description: 'Type of performance test to run'
        )
        string(
            name: 'THREAD_COUNT',
            defaultValue: '50',
            description: 'Number of concurrent users'
        )
        string(
            name: 'DURATION',
            defaultValue: '300',
            description: 'Test duration in seconds'
        )
    }
    
    environment {
        JMETER_HOME = '/opt/apache-jmeter-5.5'
        BASE_URL = credentials('api-base-url')
        AUTH_TOKEN = credentials('api-auth-token')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                script {
                    sh '''
                        # Create results directory
                        mkdir -p results
                        
                        # Validate test plan
                        ${JMETER_HOME}/bin/jmeter -n -t tests/${TEST_TYPE}-test.jmx -p tests/test.properties -l /dev/null
                    '''
                }
            }
        }
        
        stage('Performance Test') {
            steps {
                script {
                    sh '''
                        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                        RESULT_FILE="results/${TEST_TYPE}-results-${TIMESTAMP}.jtl"
                        REPORT_DIR="results/${TEST_TYPE}-report-${TIMESTAMP}"
                        
                        ${JMETER_HOME}/bin/jmeter -n \
                          -t tests/${TEST_TYPE}-test.jmx \
                          -l ${RESULT_FILE} \
                          -e \
                          -o ${REPORT_DIR} \
                          -Jbase.url=${BASE_URL} \
                          -Jauth.token=${AUTH_TOKEN} \
                          -Jthread.count=${THREAD_COUNT} \
                          -Jtest.duration=${DURATION} \
                          -Jjmeter.reportgenerator.overall_granularity=60000
                        
                        # Store result paths for artifacts
                        echo "${RESULT_FILE}" > result_file.txt
                        echo "${REPORT_DIR}" > report_dir.txt
                    '''
                }
            }
        }
        
        stage('Analyze Results') {
            steps {
                script {
                    sh '''
                        RESULT_FILE=$(cat result_file.txt)
                        
                        # Parse results
                        python3 scripts/parse_jmeter_results.py ${RESULT_FILE} > performance_summary.txt
                        
                        # Check thresholds
                        ERROR_RATE=$(python3 scripts/get_error_rate.py ${RESULT_FILE})
                        AVG_RESPONSE_TIME=$(python3 scripts/get_avg_response_time.py ${RESULT_FILE})
                        P95_RESPONSE_TIME=$(python3 scripts/get_p95_response_time.py ${RESULT_FILE})
                        
                        echo "Error Rate: ${ERROR_RATE}%"
                        echo "Average Response Time: ${AVG_RESPONSE_TIME}ms"
                        echo "95th Percentile Response Time: ${P95_RESPONSE_TIME}ms"
                        
                        # Fail if thresholds exceeded
                        if (( $(echo "${ERROR_RATE} > 5.0" | bc -l) )); then
                            echo "ERROR: Error rate too high"
                            exit 1
                        fi
                        
                        if (( $(echo "${P95_RESPONSE_TIME} > 2000" | bc -l) )); then
                            echo "ERROR: 95th percentile response time too high"
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
                // Archive results
                archiveArtifacts artifacts: 'results/**/*', fingerprint: true
                
                // Publish performance report
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: sh(script: 'cat report_dir.txt', returnStdout: true).trim(),
                    reportFiles: 'index.html',
                    reportName: 'JMeter Performance Report'
                ])
                
                // Send notifications
                if (currentBuild.result == 'FAILURE') {
                    emailext(
                        subject: "Performance Test Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                        body: "Performance test failed. Check the report for details.",
                        to: "${env.CHANGE_AUTHOR_EMAIL}"
                    )
                }
            }
        }
    }
}
```

### GitHub Actions
```yaml
name: Performance Testing

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch:
    inputs:
      test_type:
        description: 'Test type'
        required: true
        default: 'load'
        type: choice
        options:
        - smoke
        - load
        - stress

jobs:
  performance-test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Setup Java
      uses: actions/setup-java@v3
      with:
        java-version: '11'
        distribution: 'temurin'
    
    - name: Download JMeter
      run: |
        wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.5.tgz
        tar -xzf apache-jmeter-5.5.tgz
        sudo mv apache-jmeter-5.5 /opt/
        sudo ln -s /opt/apache-jmeter-5.5/bin/jmeter /usr/local/bin/jmeter
    
    - name: Install JMeter Plugins
      run: |
        cd /opt/apache-jmeter-5.5/lib/ext
        sudo wget https://jmeter-plugins.org/get/
        sudo wget https://jmeter-plugins.org/files/packages/jpgc-graphs-basic-2.0.zip
        sudo unzip jpgc-graphs-basic-2.0.zip
    
    - name: Run Performance Test
      run: |
        TEST_TYPE=${{ github.event.inputs.test_type || 'load' }}
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        
        jmeter -n \
          -t tests/${TEST_TYPE}-test.jmx \
          -l results-${TIMESTAMP}.jtl \
          -e \
          -o report-${TIMESTAMP} \
          -Jbase.url=${{ secrets.API_BASE_URL }} \
          -Jauth.token=${{ secrets.API_AUTH_TOKEN }}
      env:
        JVM_ARGS: "-Xms1g -Xmx2g"
    
    - name: Upload Results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: jmeter-results
        path: |
          results-*.jtl
          report-*/
```

## Monitoring and Reporting

### Custom Listeners
```xml
<!-- Backend Listener for InfluxDB -->
<BackendListener guiclass="BackendListenerGui" testclass="BackendListener" testname="Backend Listener">
  <elementProp name="arguments" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments">
    <collectionProp name="Arguments.arguments">
      <elementProp name="influxdbMetricsSender" elementType="Argument">
        <stringProp name="Argument.name">influxdbMetricsSender</stringProp>
        <stringProp name="Argument.value">org.apache.jmeter.visualizers.backend.influxdb.HttpMetricsSender</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
      <elementProp name="influxdbUrl" elementType="Argument">
        <stringProp name="Argument.name">influxdbUrl</stringProp>
        <stringProp name="Argument.value">http://localhost:8086/write?db=jmeter</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
      <elementProp name="application" elementType="Argument">
        <stringProp name="Argument.name">application</stringProp>
        <stringProp name="Argument.value">MyAPI</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
      <elementProp name="measurement" elementType="Argument">
        <stringProp name="Argument.name">measurement</stringProp>
        <stringProp name="Argument.value">jmeter</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
      <elementProp name="summaryOnly" elementType="Argument">
        <stringProp name="Argument.name">summaryOnly</stringProp>
        <stringProp name="Argument.value">false</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
      <elementProp name="samplersRegex" elementType="Argument">
        <stringProp name="Argument.name">samplersRegex</stringProp>
        <stringProp name="Argument.value">.*</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
      <elementProp name="percentiles" elementType="Argument">
        <stringProp name="Argument.name">percentiles</stringProp>
        <stringProp name="Argument.value">90;95;99</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
  <stringProp name="classname">org.apache.jmeter.visualizers.backend.influxdb.InfluxdbBackendListenerClient</stringProp>
</BackendListener>
```

### Result Analysis Script
```python
#!/usr/bin/env python3
# parse_jmeter_results.py

import sys
import xml.etree.ElementTree as ET
import statistics
from datetime import datetime

def parse_jtl_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    results = []
    for sample in root.findall('.//httpSample') + root.findall('.//sample'):
        result = {
            'timestamp': int(sample.get('ts')),
            'elapsed': int(sample.get('t')),
            'label': sample.get('lb'),
            'response_code': sample.get('rc'),
            'success': sample.get('s') == 'true',
            'thread_name': sample.get('tn'),
            'data_type': sample.get('dt'),
            'bytes': int(sample.get('by', 0)),
            'latency': int(sample.get('lt', 0)),
            'connect_time': int(sample.get('ct', 0)),
        }
        results.append(result)
    
    return results

def analyze_results(results):
    if not results:
        return {}
    
    total_requests = len(results)
    successful_requests = sum(1 for r in results if r['success'])
    failed_requests = total_requests - successful_requests
    error_rate = (failed_requests / total_requests) * 100
    
    response_times = [r['elapsed'] for r in results]
    
    analysis = {
        'total_requests': total_requests,
        'successful_requests': successful_requests,
        'failed_requests': failed_requests,
        'error_rate': error_rate,
        'min_response_time': min(response_times),
        'max_response_time': max(response_times),
        'avg_response_time': statistics.mean(response_times),
        'median_response_time': statistics.median(response_times),
        'p90_response_time': statistics.quantiles(response_times, n=10)[8],
        'p95_response_time': statistics.quantiles(response_times, n=20)[18],
        'p99_response_time': statistics.quantiles(response_times, n=100)[98],
        'throughput': total_requests / ((max([r['timestamp'] for r in results]) - min([r['timestamp'] for r in results])) / 1000),
    }
    
    return analysis

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 parse_jmeter_results.py <jtl_file>")
        sys.exit(1)
    
    jtl_file = sys.argv[1]
    results = parse_jtl_file(jtl_file)
    analysis = analyze_results(results)
    
    print("=== JMeter Test Results Analysis ===")
    print(f"Total Requests: {analysis['total_requests']}")
    print(f"Successful Requests: {analysis['successful_requests']}")
    print(f"Failed Requests: {analysis['failed_requests']}")
    print(f"Error Rate: {analysis['error_rate']:.2f}%")
    print(f"Throughput: {analysis['throughput']:.2f} requests/second")
    print()
    print("=== Response Times (ms) ===")
    print(f"Min: {analysis['min_response_time']}")
    print(f"Max: {analysis['max_response_time']}")
    print(f"Average: {analysis['avg_response_time']:.2f}")
    print(f"Median: {analysis['median_response_time']:.2f}")
    print(f"90th Percentile: {analysis['p90_response_time']:.2f}")
    print(f"95th Percentile: {analysis['p95_response_time']:.2f}")
    print(f"99th Percentile: {analysis['p99_response_time']:.2f}")

if __name__ == "__main__":
    main()
```

## Resources

- [Apache JMeter Documentation](https://jmeter.apache.org/usermanual/index.html)
- [JMeter User Manual](https://jmeter.apache.org/usermanual/get-started.html)
- [JMeter Plugins](https://jmeter-plugins.org/)
- [JMeter Best Practices](https://jmeter.apache.org/usermanual/best-practices.html)
- [Performance Testing Guide](https://jmeter.apache.org/usermanual/test_plan.html)
- [JMeter Functions Reference](https://jmeter.apache.org/usermanual/functions.html)
- [JMeter Property Reference](https://jmeter.apache.org/usermanual/properties_reference.html)
- [BlazeMeter University](https://www.blazemeter.com/university/)
- [JMeter Community](https://jmeter.apache.org/maillist.html)
- [GitHub Examples](https://github.com/apache/jmeter)