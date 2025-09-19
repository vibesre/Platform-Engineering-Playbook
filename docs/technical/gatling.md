# Gatling

Gatling is a high-performance load testing framework designed for ease of use, maintainability, and high performance. It uses Scala, Akka, and Netty to deliver maximum performance with minimal resource consumption.

## Installation

### Local Installation
```bash
# Download and install
wget https://repo1.maven.org/maven2/io/gatling/highcharts/gatling-charts-highcharts-bundle/3.9.5/gatling-charts-highcharts-bundle-3.9.5-bundle.zip
unzip gatling-charts-highcharts-bundle-3.9.5-bundle.zip
sudo mv gatling-charts-highcharts-bundle-3.9.5 /opt/gatling
sudo ln -s /opt/gatling/bin/gatling.sh /usr/local/bin/gatling

# Install via package managers
# macOS with Homebrew
brew install gatling

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install openjdk-11-jdk
wget -O- https://repo1.maven.org/maven2/io/gatling/highcharts/gatling-charts-highcharts-bundle/3.9.5/gatling-charts-highcharts-bundle-3.9.5-bundle.zip | sudo unzip -d /opt/

# Verify installation
gatling --version
```

### SBT/Maven Project Setup
```scala
// build.sbt
name := "gatling-load-tests"
version := "1.0.0"
scalaVersion := "2.13.8"

enablePlugins(GatlingPlugin)

libraryDependencies ++= Seq(
  "io.gatling.highcharts" % "gatling-charts-highcharts" % "3.9.5" % "test",
  "io.gatling" % "gatling-test-framework" % "3.9.5" % "test"
)

// Gatling configuration
Gatling / scalaSource := sourceDirectory.value / "gatling" / "scala"
Gatling / resourceDirectory := sourceDirectory.value / "gatling" / "resources"
```

```xml
<!-- pom.xml -->
<properties>
    <gatling.version>3.9.5</gatling.version>
    <gatling-maven-plugin.version>4.3.7</gatling-maven-plugin.version>
    <scala.version>2.13.8</scala.version>
</properties>

<dependencies>
    <dependency>
        <groupId>io.gatling.highcharts</groupId>
        <artifactId>gatling-charts-highcharts</artifactId>
        <version>${gatling.version}</version>
        <scope>test</scope>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>io.gatling</groupId>
            <artifactId>gatling-maven-plugin</artifactId>
            <version>${gatling-maven-plugin.version}</version>
        </plugin>
    </plugins>
</build>
```

### Docker
```bash
# Run Gatling in Docker
docker run --rm -v $(pwd):/opt/gatling/user-files denvazh/gatling:latest -s BasicLoadTest

# Custom Dockerfile
FROM denvazh/gatling:latest
COPY tests/ /opt/gatling/user-files/simulations/
COPY data/ /opt/gatling/user-files/resources/data/
COPY conf/ /opt/gatling/conf/

# Run with environment variables
docker run --rm \
  -e GATLING_BASEURL=https://api.example.com \
  -e GATLING_USERS=100 \
  -e GATLING_DURATION=300 \
  -v $(pwd)/results:/opt/gatling/results \
  custom-gatling -s LoadTestSimulation
```

## Basic Load Test

### Simple HTTP Load Test
```scala
// BasicLoadTest.scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class BasicLoadTest extends Simulation {

  // HTTP configuration
  val httpProtocol = http
    .baseUrl("https://api.example.com")
    .acceptHeader("application/json")
    .contentTypeHeader("application/json")
    .userAgentHeader("Gatling Load Test")

  // Scenario definition
  val scn = scenario("Basic Load Test")
    .exec(http("Get Users")
      .get("/api/users")
      .check(status.is(200))
      .check(jsonPath("$.data").exists)
      .check(responseTimeInMillis.lt(2000))
    )
    .pause(1, 3) // Random pause between 1-3 seconds

  // Load configuration
  setUp(
    scn.inject(
      rampUsers(50) during (2.minutes),    // Ramp up to 50 users over 2 minutes
      constantUsersPerSec(10) during (5.minutes), // 10 users per second for 5 minutes
      rampUsers(0) during (1.minute)       // Ramp down over 1 minute
    )
  ).protocols(httpProtocol)
   .assertions(
     global.responseTime.max.lt(5000),    // Max response time < 5s
     global.responseTime.percentile3.lt(2000), // 95th percentile < 2s
     global.successfulRequests.percent.gt(95)   // Success rate > 95%
   )
}
```

### API Test Suite
```scala
// ApiTestSuite.scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class ApiTestSuite extends Simulation {

  val httpProtocol = http
    .baseUrl(System.getProperty("baseUrl", "https://api.example.com"))
    .acceptHeader("application/json")
    .contentTypeHeader("application/json")
    .authorizationHeader(s"Bearer ${System.getProperty("authToken", "default-token")}")

  // Authentication scenario
  val authScenario = scenario("Authentication")
    .exec(http("Login")
      .post("/auth/login")
      .body(StringBody("""{"username": "testuser", "password": "testpass"}"""))
      .check(status.is(200))
      .check(jsonPath("$.access_token").saveAs("authToken"))
    )
    .exec(session => {
      println(s"Auth token: ${session("authToken").as[String]}")
      session
    })

  // User management scenario
  val userScenario = scenario("User Management")
    .exec(http("Get User List")
      .get("/api/users")
      .check(status.is(200))
      .check(jsonPath("$.data[*].id").findAll.saveAs("userIds"))
    )
    .exec(http("Create User")
      .post("/api/users")
      .body(StringBody(session => s"""
        {
          "name": "User ${scala.util.Random.nextInt(1000)}",
          "email": "user${scala.util.Random.nextInt(1000)}@example.com",
          "role": "user"
        }
      """))
      .check(status.is(201))
      .check(jsonPath("$.id").saveAs("newUserId"))
    )
    .exec(http("Get Created User")
      .get("/api/users/${newUserId}")
      .check(status.is(200))
      .check(jsonPath("$.name").exists)
    )
    .exec(http("Update User")
      .put("/api/users/${newUserId}")
      .body(StringBody("""{"name": "Updated User"}"""))
      .check(status.is(200))
    )
    .doIf(session => session.contains("userIds")) {
      exec(http("Get Random User")
        .get("/api/users/${userIds.random()}")
        .check(status.in(200, 404))
      )
    }

  // Product catalog scenario
  val productScenario = scenario("Product Catalog")
    .exec(http("Get Products")
      .get("/api/products")
      .queryParam("page", "1")
      .queryParam("limit", "20")
      .check(status.is(200))
      .check(jsonPath("$.data[*].id").findAll.saveAs("productIds"))
    )
    .exec(http("Search Products")
      .get("/api/products/search")
      .queryParam("q", "laptop")
      .check(status.is(200))
    )
    .doIf(session => session.contains("productIds") && session("productIds").as[Vector[String]].nonEmpty) {
      exec(http("Get Product Details")
        .get("/api/products/${productIds.random()}")
        .check(status.is(200))
      )
    }

  // Load simulation
  setUp(
    authScenario.inject(atOnceUsers(1)),
    userScenario.inject(
      rampUsersPerSec(1) to 10 during (2.minutes),
      constantUsersPerSec(10) during (5.minutes),
      rampUsersPerSec(10) to 0 during (1.minute)
    ),
    productScenario.inject(
      rampUsersPerSec(2) to 20 during (2.minutes),
      constantUsersPerSec(20) during (5.minutes),
      rampUsersPerSec(20) to 0 during (1.minute)
    )
  ).protocols(httpProtocol)
   .assertions(
     global.responseTime.percentile3.lt(2000),
     global.successfulRequests.percent.gt(95),
     forAll.failedRequests.count.lt(100)
   )
}
```

## Advanced Features

### Data Feeders
```scala
// data-feeders.scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._

class DataDrivenTest extends Simulation {

  // CSV feeder
  val csvFeeder = csv("users.csv").random
  
  // JSON feeder
  val jsonFeeder = jsonFile("products.json").circular
  
  // Custom feeder
  val customFeeder = Iterator.continually(Map(
    "userId" -> scala.util.Random.nextInt(1000),
    "email" -> s"user${scala.util.Random.nextInt(1000)}@example.com",
    "timestamp" -> System.currentTimeMillis()
  ))

  // Array feeder
  val statusFeeder = Array(
    Map("status" -> "active"),
    Map("status" -> "inactive"), 
    Map("status" -> "pending")
  ).random

  val httpProtocol = http.baseUrl("https://api.example.com")

  val scn = scenario("Data Driven Test")
    .feed(csvFeeder)
    .feed(customFeeder)
    .exec(http("Get User by ID")
      .get("/api/users/${userId}")
      .check(status.is(200))
    )
    .feed(jsonFeeder)
    .exec(http("Create Order")
      .post("/api/orders")
      .body(StringBody("""
        {
          "userId": ${userId},
          "productId": ${productId},
          "quantity": ${quantity},
          "email": "${email}",
          "timestamp": ${timestamp}
        }
      """))
      .check(status.is(201))
    )
    .feed(statusFeeder)
    .exec(http("Filter Users by Status")
      .get("/api/users")
      .queryParam("status", "${status}")
      .check(status.is(200))
    )

  setUp(scn.inject(constantUsersPerSec(5) during (2.minutes)))
    .protocols(httpProtocol)
}
```

### Custom Checks and Extractors
```scala
// advanced-checks.scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._

class AdvancedChecks extends Simulation {

  val httpProtocol = http.baseUrl("https://api.example.com")

  val scn = scenario("Advanced Checks")
    .exec(http("Complex API Response")
      .get("/api/users")
      .check(
        status.is(200),
        header("Content-Type").is("application/json"),
        responseTimeInMillis.lt(1000),
        
        // JSON path checks
        jsonPath("$.data").exists,
        jsonPath("$.data[*]").count.gte(1),
        jsonPath("$.data[0].id").saveAs("firstUserId"),
        jsonPath("$.data[*].email").findAll.saveAs("allEmails"),
        
        // Regex checks
        regex("""email":"([^"]+)"""").findAll.saveAs("emailsRegex"),
        
        // Custom checks
        bodyString.transform(_.length).lt(50000),
        
        // CSS selector (for HTML responses)
        css("title").saveAs("pageTitle")
      )
    )
    .exec(http("Validate User Details")
      .get("/api/users/${firstUserId}")
      .check(
        status.is(200),
        jsonPath("$.id").is("${firstUserId}"),
        jsonPath("$.email").in("${allEmails}"),
        
        // Conditional checks
        checkIf(jsonPath("$.role").is("admin")) {
          jsonPath("$.permissions").exists
        },
        
        // Custom validation
        jsonPath("$.created_at").validate(
          "timestamp should be valid",
          timestamp => {
            try {
              java.time.Instant.parse(timestamp.toString)
              true
            } catch {
              case _: Exception => false
            }
          }
        )
      )
    )
    .exec(session => {
      val emails = session("allEmails").as[Vector[String]]
      println(s"Found ${emails.length} user emails")
      session.set("emailCount", emails.length)
    })

  setUp(scn.inject(atOnceUsers(1))).protocols(httpProtocol)
}
```

### Error Handling and Retry Logic
```scala
// error-handling.scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._

class ErrorHandlingTest extends Simulation {

  val httpProtocol = http
    .baseUrl("https://api.example.com")
    .disableFollowRedirect // Handle redirects manually

  val scn = scenario("Error Handling")
    .exec(
      tryMax(3) { // Retry up to 3 times
        exec(http("Unreliable API Call")
          .get("/api/unreliable-endpoint")
          .check(status.in(200, 201, 202))
          .checkIf(status.is(200)) {
            jsonPath("$.data").exists
          }
        )
      }.exitHereIfFailed // Stop scenario if all retries fail
    )
    .exec(http("Handle Different Status Codes")
      .get("/api/users")
      .check(status.not(500)) // Fail only on server errors
      .checkIf(status.is(200)) {
        jsonPath("$.data").saveAs("userData")
      }
      .checkIf(status.is(404)) {
        bodyString.saveAs("errorMessage")
      }
    )
    .doIf(session => session.contains("userData")) {
      exec(http("Process User Data")
        .post("/api/process")
        .body(StringBody("${userData}"))
        .check(status.is(200))
      )
    }
    .doIf(session => session.contains("errorMessage")) {
      exec(session => {
        println(s"Error occurred: ${session("errorMessage").as[String]}")
        session
      })
    }
    // Graceful degradation
    .doIfOrElse(session => session("userData").asOption[String].isDefined) {
      exec(http("Full Feature Access")
        .get("/api/premium-features")
        .check(status.is(200))
      )
    } {
      exec(http("Basic Feature Access")
        .get("/api/basic-features")
        .check(status.is(200))
      )
    }

  setUp(scn.inject(constantUsersPerSec(2) during (1.minute)))
    .protocols(httpProtocol)
}
```

## Load Testing Patterns

### Spike Testing
```scala
// spike-test.scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._

class SpikeTest extends Simulation {

  val httpProtocol = http.baseUrl("https://api.example.com")

  val spikeScenario = scenario("Spike Test")
    .exec(http("Health Check")
      .get("/health")
      .check(status.is(200))
    )

  setUp(
    spikeScenario.inject(
      nothingFor(10.seconds),                    // No load
      atOnceUsers(200),                          // Immediate spike
      nothingFor(30.seconds),                    // Hold spike
      atOnceUsers(200),                          // Another spike
      nothingFor(30.seconds),                    // Hold
      rampUsers(0) during (10.seconds)           // Ramp down
    )
  ).protocols(httpProtocol)
   .assertions(
     global.responseTime.percentile3.lt(5000),  // Allow higher response times
     global.successfulRequests.percent.gt(80)   // Accept some failures
   )
}
```

### Stress Testing
```scala
// stress-test.scala
class StressTest extends Simulation {

  val httpProtocol = http.baseUrl("https://api.example.com")

  val stressScenario = scenario("Stress Test")
    .exec(http("API Endpoint")
      .get("/api/data")
      .check(status.in(200, 429, 503)) // Accept rate limiting and service unavailable
    )

  setUp(
    stressScenario.inject(
      rampUsersPerSec(1) to 50 during (5.minutes),   // Gradually increase load
      constantUsersPerSec(50) during (10.minutes),   // Sustain high load
      rampUsersPerSec(50) to 100 during (5.minutes), // Push to extreme load
      constantUsersPerSec(100) during (10.minutes),  // Sustain extreme load
      rampUsersPerSec(100) to 0 during (5.minutes)   // Ramp down
    )
  ).protocols(httpProtocol)
   .assertions(
     global.responseTime.mean.lt(10000),        // Mean response time
     global.responseTime.percentile4.lt(20000), // 99th percentile
     forAll.failedRequests.percent.lt(50)       // Allow high failure rate
   )
}
```

### Volume Testing
```scala
// volume-test.scala
class VolumeTest extends Simulation {

  val httpProtocol = http.baseUrl("https://api.example.com")

  val volumeScenario = scenario("Volume Test")
    .during(60.minutes) { // Run for extended period
      exec(http("Create Large Dataset")
        .post("/api/bulk-data")
        .body(RawFileBody("large-dataset.json"))
        .check(status.is(201))
      )
      .pause(30.seconds) // Allow processing time
    }

  setUp(
    volumeScenario.inject(constantUsersPerSec(5) during (60.minutes))
  ).protocols(httpProtocol)
   .maxDuration(65.minutes) // Safety timeout
   .assertions(
     global.responseTime.percentile3.lt(30000), // Allow longer processing
     global.successfulRequests.percent.gt(95)
   )
}
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Gatling Load Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch:
    inputs:
      simulation:
        description: 'Simulation to run'
        required: true
        default: 'BasicLoadTest'
      users:
        description: 'Number of users'
        required: false
        default: '50'

jobs:
  gatling-test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Setup Java
      uses: actions/setup-java@v3
      with:
        java-version: '11'
        distribution: 'temurin'
    
    - name: Setup SBT
      uses: olafurpg/setup-scala@v13
      with:
        java-version: '11'
    
    - name: Cache SBT
      uses: actions/cache@v3
      with:
        path: |
          ~/.ivy2/cache
          ~/.sbt
        key: ${{ runner.os }}-sbt-${{ hashFiles('**/build.sbt') }}
    
    - name: Run Gatling Tests
      run: |
        SIMULATION=${{ github.event.inputs.simulation || 'BasicLoadTest' }}
        USERS=${{ github.event.inputs.users || '50' }}
        
        sbt "Gatling/testOnly *${SIMULATION}" \
          -Dgatling.core.directory.results=target/gatling \
          -DbaseUrl=${{ secrets.API_BASE_URL }} \
          -DauthToken=${{ secrets.API_AUTH_TOKEN }} \
          -Dusers=${USERS}
      env:
        SBT_OPTS: "-Xmx2G"
    
    - name: Parse Results
      run: |
        # Find the latest results directory
        RESULTS_DIR=$(find target/gatling -name "*${SIMULATION}*" -type d | head -1)
        
        if [ -d "$RESULTS_DIR" ]; then
          # Extract key metrics from global_stats.json
          STATS_FILE="$RESULTS_DIR/js/global_stats.json"
          
          if [ -f "$STATS_FILE" ]; then
            MEAN_RESPONSE_TIME=$(jq -r '.contents.meanResponseTime.total' "$STATS_FILE")
            P95_RESPONSE_TIME=$(jq -r '.contents.percentiles3.total' "$STATS_FILE")
            ERROR_RATE=$(jq -r '.contents.numberOfRequests.ko / .contents.numberOfRequests.total * 100' "$STATS_FILE")
            
            echo "Mean Response Time: ${MEAN_RESPONSE_TIME}ms"
            echo "95th Percentile: ${P95_RESPONSE_TIME}ms"
            echo "Error Rate: ${ERROR_RATE}%"
            
            # Set GitHub Actions outputs
            echo "mean_response_time=${MEAN_RESPONSE_TIME}" >> $GITHUB_OUTPUT
            echo "p95_response_time=${P95_RESPONSE_TIME}" >> $GITHUB_OUTPUT
            echo "error_rate=${ERROR_RATE}" >> $GITHUB_OUTPUT
            
            # Check thresholds
            if (( $(echo "$P95_RESPONSE_TIME > 2000" | bc -l) )); then
              echo "::error::95th percentile response time exceeded 2000ms"
              exit 1
            fi
            
            if (( $(echo "$ERROR_RATE > 5" | bc -l) )); then
              echo "::error::Error rate exceeded 5%"
              exit 1
            fi
          fi
        fi
    
    - name: Upload Gatling Report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: gatling-report
        path: target/gatling/
        retention-days: 30
    
    - name: Comment PR
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const path = require('path');
          
          // Find report index.html
          const findReportFile = (dir) => {
            const files = fs.readdirSync(dir);
            for (const file of files) {
              const fullPath = path.join(dir, file);
              if (fs.statSync(fullPath).isDirectory()) {
                const result = findReportFile(fullPath);
                if (result) return result;
              } else if (file === 'index.html') {
                return fullPath;
              }
            }
            return null;
          };
          
          const reportFile = findReportFile('target/gatling');
          
          if (reportFile) {
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🚀 Gatling Load Test Results
              
              The load test has completed. Download the artifacts to view the detailed report.
              
              **Key Metrics:**
              - Mean Response Time: ${{ steps.gatling.outputs.mean_response_time }}ms
              - 95th Percentile: ${{ steps.gatling.outputs.p95_response_time }}ms
              - Error Rate: ${{ steps.gatling.outputs.error_rate }}%`
            });
          }
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'SIMULATION',
            choices: ['BasicLoadTest', 'ApiTestSuite', 'StressTest', 'SpikeTest'],
            description: 'Gatling simulation to run'
        )
        string(
            name: 'USERS',
            defaultValue: '50',
            description: 'Number of concurrent users'
        )
        string(
            name: 'DURATION',
            defaultValue: '300',
            description: 'Test duration in seconds'
        )
        booleanParam(
            name: 'PUBLISH_REPORT',
            defaultValue: true,
            description: 'Publish HTML report'
        )
    }
    
    environment {
        GATLING_HOME = '/opt/gatling'
        BASE_URL = credentials('api-base-url')
        AUTH_TOKEN = credentials('api-auth-token')
        SBT_OPTS = '-Xmx4g -XX:MaxMetaspaceSize=512m'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Prepare Environment') {
            steps {
                script {
                    sh '''
                        # Create results directory
                        mkdir -p target/gatling
                        
                        # Validate Scala/SBT setup
                        sbt clean compile
                    '''
                }
            }
        }
        
        stage('Run Load Test') {
            steps {
                script {
                    sh """
                        sbt "Gatling/testOnly *${params.SIMULATION}" \\
                          -DbaseUrl=${BASE_URL} \\
                          -DauthToken=${AUTH_TOKEN} \\
                          -Dusers=${params.USERS} \\
                          -Dduration=${params.DURATION}
                    """
                }
            }
        }
        
        stage('Process Results') {
            steps {
                script {
                    sh '''
                        # Find the latest results directory
                        RESULTS_DIR=$(find target/gatling -name "*${SIMULATION}*" -type d | sort | tail -1)
                        
                        if [ -d "$RESULTS_DIR" ]; then
                            echo "Results directory: $RESULTS_DIR"
                            
                            # Copy results to standard location
                            cp -r "$RESULTS_DIR" target/gatling/latest-report
                            
                            # Extract metrics
                            if [ -f "$RESULTS_DIR/js/global_stats.json" ]; then
                                python3 scripts/parse_gatling_results.py "$RESULTS_DIR/js/global_stats.json"
                            fi
                        else
                            echo "No results directory found"
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
                archiveArtifacts artifacts: 'target/gatling/**/*', fingerprint: true
                
                // Publish HTML report
                if (params.PUBLISH_REPORT) {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'target/gatling/latest-report',
                        reportFiles: 'index.html',
                        reportName: 'Gatling Performance Report'
                    ])
                }
                
                // Send notifications based on results
                def resultsFile = 'target/gatling/latest-report/js/global_stats.json'
                if (fileExists(resultsFile)) {
                    def results = readJSON file: resultsFile
                    def errorRate = (results.contents.numberOfRequests.ko / results.contents.numberOfRequests.total) * 100
                    def meanResponseTime = results.contents.meanResponseTime.total
                    
                    if (errorRate > 5 || meanResponseTime > 2000) {
                        emailext(
                            subject: "Load Test Alert: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                            body: """
                                Load test completed with concerning metrics:
                                
                                Error Rate: ${errorRate}%
                                Mean Response Time: ${meanResponseTime}ms
                                
                                View report: ${env.BUILD_URL}Gatling_Performance_Report/
                            """,
                            to: "${env.CHANGE_AUTHOR_EMAIL}"
                        )
                    }
                }
            }
        }
    }
}
```

## Monitoring and Analytics

### Custom Metrics
```scala
// custom-metrics.scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._

class CustomMetricsTest extends Simulation {

  val httpProtocol = http.baseUrl("https://api.example.com")

  val scn = scenario("Custom Metrics")
    .exec(http("Timed Request")
      .get("/api/slow-endpoint")
      .check(status.is(200))
      .check(responseTimeInMillis.saveAs("responseTime"))
    )
    .exec(session => {
      val responseTime = session("responseTime").as[Int]
      
      // Custom metrics based on response time
      if (responseTime > 5000) {
        session.markAsSucceeded // Still mark as successful but log separately
      } else {
        session.markAsSucceeded
      }
    })
    // Custom request with business logic validation
    .exec(http("Business Logic Validation")
      .get("/api/business-data")
      .check(status.is(200))
      .check(jsonPath("$.calculation_result").saveAs("result"))
    )
    .exec(session => {
      val result = session("result").as[Double]
      val expected = 42.0
      
      // Business logic assertion
      if (math.abs(result - expected) < 0.01) {
        session.markAsSucceeded
      } else {
        session.markAsFailed(s"Business logic failed: expected $expected, got $result")
      }
    })

  setUp(scn.inject(constantUsersPerSec(1) during (1.minute)))
    .protocols(httpProtocol)
}
```

### Real-time Monitoring Integration
```scala
// monitoring-integration.scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._

class MonitoringIntegration extends Simulation {

  val httpProtocol = http
    .baseUrl("https://api.example.com")
    .header("X-Load-Test", "gatling")
    .header("X-Test-ID", java.util.UUID.randomUUID().toString)

  // Scenario with monitoring hooks
  val scn = scenario("Monitored Load Test")
    .exec(http("Monitored Request")
      .get("/api/monitored-endpoint")
      .check(status.is(200))
      .check(header("X-Request-ID").saveAs("requestId"))
      .check(responseTimeInMillis.saveAs("responseTime"))
    )
    .exec(session => {
      val requestId = session("requestId").as[String]
      val responseTime = session("responseTime").as[Int]
      
      // Send metrics to external monitoring system
      // This could be StatsD, InfluxDB, CloudWatch, etc.
      println(s"METRIC: request_id=$requestId, response_time=$responseTime")
      
      session
    })
    .doIf(session => session("responseTime").as[Int] > 2000) {
      exec(session => {
        // Alert on slow requests
        println(s"ALERT: Slow request detected: ${session("responseTime").as[Int]}ms")
        session
      })
    }

  setUp(scn.inject(constantUsersPerSec(10) during (2.minutes)))
    .protocols(httpProtocol)
}
```

## Configuration

### Gatling Configuration
```hocon
# gatling.conf
gatling {
  core {
    outputDirectoryBaseName = "gatling"
    runDescription = "Load Test"
    encoding = "utf-8"
    simulationClass = ""
    
    extract {
      regex {
        cacheMaxCapacity = 200
      }
      xpath {
        cacheMaxCapacity = 200
      }
      jsonPath {
        cacheMaxCapacity = 200
        preferJackson = false
      }
      css {
        cacheMaxCapacity = 200
      }
    }
    
    directory {
      simulations = "user-files/simulations"
      resources = "user-files/resources"
      results = "results"
      binaries = ""
    }
  }
  
  http {
    connectionTimeout = 60000
    readTimeout = 60000
    pooledConnectionIdleTimeout = 60000
    maxConnectionsPerHost = -1
    
    ssl {
      useOpenSsl = true
      useOpenSslFinalizers = false
      handshakeTimeout = 10000
      useInsecureTrustManager = false
      enabledProtocols = []
      enabledCipherSuites = []
      sessionCacheSize = 0
      sessionTimeout = 0
    }
    
    ahc {
      keepAlive = true
      maxConnectionsPerHost = -1
      maxConnectionsTotal = -1
      maxConnectionLifetime = -1
      idleConnectionInPoolTimeout = 60000
      maxRedirects = 5
      requestTimeout = 60000
      useProxyProperties = false
    }
  }
  
  jms {
    replyTimeoutScanPeriod = 1000
  }
  
  data {
    writers = [console, file]
    console {
      light = false
      writePeriod = 5
    }
    file {
      bufferSize = 8192
    }
    leak {
      noActivityTimeout = 30
    }
    graphite {
      light = false
      host = "localhost"
      port = 2003
      protocol = "tcp"
      rootPathPrefix = "gatling"
      bufferSize = 8192
      writePeriod = 1
    }
  }
  
  charting {
    noReports = false
    maxPlotPerSeries = 1000
    useGroupDurationMetric = false
    indicators {
      lowerBound = 800
      higherBound = 1200
      percentile1 = 50
      percentile2 = 75
      percentile3 = 95
      percentile4 = 99
    }
  }
}
```

## Resources

- [Gatling Documentation](https://gatling.io/docs/gatling/)
- [Gatling Academy](https://gatling.io/academy/)
- [Gatling GitHub](https://github.com/gatling/gatling)
- [Scala Documentation](https://docs.scala-lang.org/)
- [Performance Testing Guide](https://gatling.io/docs/gatling/guides/performance_testing/)
- [Best Practices](https://gatling.io/docs/gatling/guides/advanced_tutorial/)
- [Gatling Extensions](https://gatling.io/docs/gatling/extensions/)
- [Community Forum](https://community.gatling.io/)
- [Enterprise Features](https://gatling.io/enterprise/)
- [Load Testing Examples](https://github.com/gatling/gatling-maven-plugin-demo)