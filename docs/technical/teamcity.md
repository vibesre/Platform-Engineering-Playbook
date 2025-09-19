# TeamCity Technical Documentation

## Overview

TeamCity is a powerful, Java-based continuous integration and continuous delivery (CI/CD) server developed by JetBrains. It provides a comprehensive build management and continuous integration platform with advanced features for enterprise environments, offering both on-premises and cloud deployment options.

## Architecture

### Core Components

#### 1. **TeamCity Server**
- **Central Management Hub**: Coordinates all CI/CD activities
- **Web Interface**: Rich UI for configuration and monitoring
- **Database Backend**: Stores configurations, build history, and artifacts
- **Build Queue Manager**: Intelligent job scheduling and distribution
- **VCS Integration Layer**: Handles source control operations

#### 2. **Build Agents**
- **Agent Pool Architecture**: Scalable distributed build infrastructure
- **Agent Types**:
  - **Default Agents**: Standard build environments
  - **Cloud Agents**: Dynamic scaling with cloud providers
  - **Composite Agents**: Multi-capability environments
- **Agent Requirements**: Capability-based job routing
- **Agent Priority**: Weighted distribution algorithms

#### 3. **Data Storage**
```
TeamCity Data Directory Structure:
├── config/              # Server configuration
├── system/              # Internal data and caches
├── artifacts/           # Build artifacts storage
├── backup/              # Backup data
├── logs/                # Server and agent logs
└── plugins/             # Installed plugins
```

### Deployment Architecture

#### 1. **Standalone Deployment**
- Single server instance
- Embedded HSQLDB database
- Suitable for small teams
- Quick setup and evaluation

#### 2. **Professional Deployment**
```
┌─────────────────┐     ┌─────────────────┐
│  TeamCity       │────▶│  External DB    │
│  Server         │     │  (PostgreSQL/   │
│                 │     │   MySQL/MSSQL)  │
└────────┬────────┘     └─────────────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│Agent 1│ │Agent 2│ ... │Agent N│
└───────┘ └───────┘     └───────┘
```

#### 3. **High Availability Setup**
```
        ┌──────────────┐
        │ Load Balancer│
        └──────┬───────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼───────┐      ┌─────▼─────┐
│ Primary   │      │ Secondary │
│ Server    │◀────▶│ Server    │
└─────┬─────┘      └───────────┘
      │
┌─────▼─────┐
│ Shared DB │
│ Cluster   │
└───────────┘
```

#### 4. **Cloud-Native Deployment**
- Kubernetes deployment options
- Docker containerization
- TeamCity Cloud managed service
- Auto-scaling agent pools

## Pipeline Configuration

### Build Configuration Concepts

#### 1. **Projects and Build Configurations**
```kotlin
// Kotlin DSL configuration
import jetbrains.buildServer.configs.kotlin.v2019_2.*
import jetbrains.buildServer.configs.kotlin.v2019_2.buildSteps.*
import jetbrains.buildServer.configs.kotlin.v2019_2.triggers.*

version = "2021.2"

project {
    buildType(Build)
    buildType(Test)
    buildType(Deploy)
    
    // Build chain dependencies
    sequential {
        buildType(Build)
        parallel {
            buildType(Test)
            buildType(SecurityScan)
        }
        buildType(Deploy)
    }
}

object Build : BuildType({
    name = "Build Application"
    
    vcs {
        root(GitRepo)
    }
    
    steps {
        gradle {
            tasks = "clean build"
            buildFile = "build.gradle"
            jdkHome = "%java.home%"
        }
    }
    
    artifactRules = """
        build/libs/*.jar => artifacts/
        build/reports/** => reports.zip
    """
})
```

#### 2. **Version Control Settings**
```kotlin
object GitRepo : VcsRoot({
    name = "Application Repository"
    type = "git"
    url = "https://github.com/organization/repository.git"
    branch = "refs/heads/main"
    
    authMethod = password {
        userName = "git"
        password = "credentialsJSON:github-token"
    }
    
    // Advanced Git settings
    checkoutPolicy = AgentCheckoutPolicy.USE_MIRRORS
    cleanPolicy = CleanPolicy.ALWAYS
    useMirrors = true
})
```

### Build Steps and Features

#### 1. **Multi-Language Support**
```kotlin
steps {
    // Java/Kotlin
    gradle {
        tasks = "build test"
        gradleParams = "--parallel --build-cache"
    }
    
    // .NET
    dotnetBuild {
        projects = "src/MyApp.sln"
        configuration = "Release"
        sdk = "6.0"
    }
    
    // Node.js
    nodeJS {
        shellScript = """
            npm ci
            npm run build
            npm test
        """
    }
    
    // Python
    python {
        command = script {
            content = """
                pip install -r requirements.txt
                pytest tests/
                python setup.py bdist_wheel
            """
        }
    }
    
    // Docker
    dockerCommand {
        commandType = build {
            source = file {
                path = "Dockerfile"
            }
            namesAndTags = "myapp:${build.number}"
        }
    }
}
```

#### 2. **Build Features**
```kotlin
features {
    // Pull Request integration
    pullRequests {
        provider = github {
            authType = token {
                token = "credentialsJSON:github-token"
            }
            filterAuthorRole = PullRequests.GitHubRoleFilter.MEMBER
        }
    }
    
    // Commit status publisher
    commitStatusPublisher {
        publisher = github {
            githubUrl = "https://api.github.com"
            authType = personalToken {
                token = "credentialsJSON:github-token"
            }
        }
    }
    
    // Build failure conditions
    failureConditions {
        executionTimeoutMin = 30
        testFailure = true
        nonZeroExitCode = true
        
        failOnMetricChange {
            metric = BuildFailureOnMetric.MetricType.TEST_COUNT
            threshold = 10
            units = BuildFailureOnMetric.MetricUnit.PERCENTS
            comparison = BuildFailureOnMetric.MetricComparison.LESS
        }
    }
    
    // Performance monitoring
    perfmon {
    }
    
    // Notifications
    notifications {
        notifierSettings = slackNotifier {
            connection = "PROJECT_SLACK"
            sendTo = "#builds"
            messageFormat = verboseMessageFormat {
                addStatusText = true
                maximumNumberOfChanges = 10
            }
        }
    }
}
```

### Build Triggers

```kotlin
triggers {
    // VCS trigger
    vcs {
        branchFilter = """
            +:*
            -:pull/*
            -:experimental/*
        """
        
        triggerRules = """
            +:**/src/**
            -:**/docs/**
            -:**.md
        """
    }
    
    // Schedule trigger
    schedule {
        schedulingPolicy = daily {
            hour = 2
            minute = 30
        }
        branchFilter = "+:main"
        triggerBuild = always()
        withPendingChangesOnly = false
    }
    
    // Build finish trigger
    finishBuildTrigger {
        buildType = "${Build.id}"
        successfulOnly = true
    }
    
    // Maven snapshot dependency
    mavenSnapshot {
        skipIfRunning = true
    }
}
```

## Integrations

### Version Control Systems

#### 1. **Git Integration**
- GitHub, GitLab, Bitbucket support
- Azure DevOps Repos
- Perforce Helix Core
- Subversion (SVN)
- Mercurial

#### 2. **Advanced VCS Features**
```kotlin
// Branch specification
vcs {
    branchSpec = """
        +:refs/heads/*
        +:refs/pull/*/head
        -:refs/heads/experimental/*
    """
    
    // Checkout rules
    checkoutRules = """
        +:src => source
        -:src/generated
        +:config => .
    """
}
```

### Build Tools Integration

#### 1. **JetBrains IDE Integration**
- IntelliJ IDEA
- WebStorm
- Rider
- PyCharm
- Remote run capability
- Personal builds

#### 2. **Build Tool Support**
```kotlin
// Maven
steps {
    maven {
        goals = "clean install"
        pomLocation = "pom.xml"
        mavenVersion = bundled_3_6()
        
        runnerArgs = """
            -DskipTests=false
            -Dmaven.test.failure.ignore=true
        """
    }
}

// Gradle with Kotlin DSL
steps {
    gradle {
        tasks = "clean build"
        buildFile = "build.gradle.kts"
        enableStacktrace = true
        jdkHome = "%java11.home%"
    }
}

// MSBuild
steps {
    msBuild {
        path = "MyProject.sln"
        version = MSBuildVersion.V16_0
        toolsVersion = MSBuildToolsVersion.V16_0
        targets = "Clean,Build"
        args = "/p:Configuration=Release"
    }
}
```

### Cloud and Container Platforms

#### 1. **Docker Integration**
```kotlin
// Docker build and push
steps {
    dockerCommand {
        commandType = build {
            source = file {
                path = "Dockerfile"
            }
            contextDir = "."
            namesAndTags = """
                myregistry.azurecr.io/myapp:%build.number%
                myregistry.azurecr.io/myapp:latest
            """
        }
    }
    
    dockerCommand {
        commandType = push {
            namesAndTags = """
                myregistry.azurecr.io/myapp:%build.number%
                myregistry.azurecr.io/myapp:latest
            """
            removeImageAfterPush = true
        }
    }
}
```

#### 2. **Kubernetes Deployment**
```kotlin
steps {
    script {
        name = "Deploy to Kubernetes"
        scriptContent = """
            kubectl config use-context production
            kubectl set image deployment/myapp myapp=myregistry.azurecr.io/myapp:%build.number%
            kubectl rollout status deployment/myapp
        """
    }
}
```

#### 3. **Cloud Provider Integration**
- **AWS**: EC2, ECS, Lambda deployment
- **Azure**: App Service, AKS, Functions
- **Google Cloud**: GKE, Cloud Run, App Engine
- **Cloud agent provisioning**: Dynamic scaling

### Testing and Quality Tools

#### 1. **Test Framework Integration**
```kotlin
// JUnit test reporting
features {
    xmlReport {
        reportType = XmlReport.XmlReportType.JUNIT
        directories = "build/test-results/test"
    }
}

// Code coverage
steps {
    gradle {
        tasks = "test jacocoTestReport"
        coverageEngine = jacoco {
            classpath = "+:build/classes/java/main/**"
            excludeClasses = "*Test*"
        }
    }
}
```

#### 2. **Static Analysis Tools**
```kotlin
steps {
    // SonarQube analysis
    script {
        name = "SonarQube Analysis"
        scriptContent = """
            ./gradlew sonarqube \
                -Dsonar.projectKey=myproject \
                -Dsonar.host.url=%sonar.host.url% \
                -Dsonar.login=%sonar.token%
        """
    }
    
    // Security scanning
    script {
        name = "OWASP Dependency Check"
        scriptContent = """
            ./gradlew dependencyCheckAnalyze
        """
    }
}
```

## Enterprise Features

### Security and Access Control

#### 1. **Authentication Methods**
- **Built-in Authentication**: Native user management
- **LDAP/Active Directory**: Enterprise directory integration
- **SAML 2.0**: Single Sign-On support
- **OAuth 2.0**: GitHub, Google, Bitbucket
- **Two-Factor Authentication**: Enhanced security

#### 2. **Role-Based Access Control**
```kotlin
// Project-level permissions
project {
    features {
        roleAssignment {
            roleId = "PROJECT_DEVELOPER"
            principals = listOf(
                "user:john.doe",
                "group:developers"
            )
        }
    }
}

// Build configuration permissions
buildType {
    features {
        approval {
            approvalRules = "user:lead.developer"
            manualRunsApproved = true
        }
    }
}
```

#### 3. **Audit and Compliance**
- Comprehensive audit logging
- Change tracking
- User action history
- Configuration versioning
- Compliance reporting

### High Availability and Scalability

#### 1. **Multi-Node Setup**
```yaml
# docker-compose.yml for HA setup
version: '3.8'
services:
  teamcity-server-1:
    image: jetbrains/teamcity-server
    environment:
      - TEAMCITY_SERVER_OPTS=-Dteamcity.server.nodeId=main
      - TEAMCITY_DATA_PATH=/data/teamcity_server/datadir
    volumes:
      - shared-data:/data/teamcity_server/datadir
      - shared-logs:/opt/teamcity/logs
    
  teamcity-server-2:
    image: jetbrains/teamcity-server
    environment:
      - TEAMCITY_SERVER_OPTS=-Dteamcity.server.nodeId=secondary
      - TEAMCITY_SERVER_MODE=secondary
      - TEAMCITY_DATA_PATH=/data/teamcity_server/datadir
    volumes:
      - shared-data:/data/teamcity_server/datadir
      - shared-logs:/opt/teamcity/logs
    
  database:
    image: postgres:13
    environment:
      - POSTGRES_DB=teamcity
      - POSTGRES_USER=teamcity
      - POSTGRES_PASSWORD=teamcity
    volumes:
      - db-data:/var/lib/postgresql/data
```

#### 2. **Agent Scaling Strategies**
```kotlin
// Cloud profile configuration
project {
    features {
        cloudProfile {
            id = "aws-agents"
            type = "EC2"
            param("cloud.amazon.image.id", "ami-12345678")
            param("cloud.amazon.instance.type", "m5.large")
            param("cloud.amazon.idle.time", "30")
            param("cloud.amazon.instances.limit", "10")
        }
    }
}
```

### Build Optimization

#### 1. **Build Cache**
```kotlin
features {
    buildCache {
        name = "Gradle Build Cache"
        rules = """
            +:**/build-cache/**
            +:.gradle/caches/build-cache-*/**
        """
        
        // Publish settings
        publish = true
        publishCondition = "successful"
        
        // Use settings
        use = true
        useCondition = "any"
    }
}
```

#### 2. **Parallel Execution**
```kotlin
// Parallel test execution
steps {
    gradle {
        tasks = "test"
        gradleParams = """
            --parallel
            --max-workers=4
            -Ptest.parallel=true
        """
    }
}

// Matrix builds
object MatrixBuild : BuildType({
    name = "Matrix Build"
    
    params {
        select("os", "linux", listOf("linux", "windows", "mac"))
        select("jdk", "11", listOf("8", "11", "17"))
    }
    
    steps {
        script {
            scriptContent = """
                echo "Building on %os% with JDK %jdk%"
            """
        }
    }
})
```

### Advanced Features

#### 1. **Build Chains and Dependencies**
```kotlin
// Snapshot dependencies
dependencies {
    snapshot(Build) {
        reuseBuilds = ReuseBuilds.NO
        onDependencyFailure = FailureAction.FAIL_TO_START
        synchronizeRevisions = true
    }
    
    artifacts(Build) {
        buildRule = lastSuccessful()
        artifactRules = """
            artifacts/*.jar => lib/
            reports.zip!** => test-reports/
        """
    }
}
```

#### 2. **Meta-Runners**
```xml
<!-- Meta-runner definition -->
<meta-runner name="Docker Build and Push">
  <description>Builds and pushes Docker images</description>
  <settings>
    <parameters>
      <param name="docker.image.name" value="" spec="text display='normal' label='Image Name' description='Docker image name'"/>
      <param name="docker.registry" value="" spec="text display='normal' label='Registry URL'"/>
    </parameters>
    <build-runners>
      <runner name="Build Image" type="DockerCommand">
        <parameters>
          <param name="docker.command.type" value="build"/>
          <param name="docker.image.namesAndTags" value="%docker.registry%/%docker.image.name%:%build.number%"/>
        </parameters>
      </runner>
      <runner name="Push Image" type="DockerCommand">
        <parameters>
          <param name="docker.command.type" value="push"/>
          <param name="docker.push.remove" value="true"/>
        </parameters>
      </runner>
    </build-runners>
  </settings>
</meta-runner>
```

#### 3. **Service Messages**
```kotlin
steps {
    script {
        scriptContent = """
            echo "##teamcity[buildStatus text='Build successful']"
            echo "##teamcity[buildNumber '2.0.%build.counter%']"
            echo "##teamcity[publishArtifacts 'dist/*.jar => artifacts/']"
            echo "##teamcity[testStarted name='myTest']"
            echo "##teamcity[testFinished name='myTest' duration='1000']"
        """
    }
}
```

### REST API

#### 1. **Build Management**
```bash
# Trigger a build
curl -X POST \
  "https://teamcity.example.com/app/rest/buildQueue" \
  -H "Authorization: Bearer $TC_TOKEN" \
  -H "Content-Type: application/xml" \
  -d '<build>
        <buildType id="MyBuildConfig"/>
        <properties>
          <property name="env.DEPLOY_ENV" value="staging"/>
        </properties>
      </build>'

# Get build status
curl -X GET \
  "https://teamcity.example.com/app/rest/builds/id:12345" \
  -H "Authorization: Bearer $TC_TOKEN" \
  -H "Accept: application/json"
```

#### 2. **Configuration Management**
```bash
# Create project from API
curl -X POST \
  "https://teamcity.example.com/app/rest/projects" \
  -H "Authorization: Bearer $TC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "MyProject",
    "name": "My Project",
    "parentProject": {
      "id": "_Root"
    }
  }'
```

### Monitoring and Analytics

#### 1. **Build Metrics**
```kotlin
// Custom metrics collection
steps {
    script {
        scriptContent = """
            # Report custom metrics
            echo "##teamcity[buildStatisticValue key='coverage' value='85.7']"
            echo "##teamcity[buildStatisticValue key='warnings' value='12']"
        """
    }
}

// Metric-based failure conditions
features {
    failureConditions {
        failOnMetricChange {
            metric = BuildFailureOnMetric.MetricType.COVERAGE_PERCENTAGE
            threshold = 80
            units = BuildFailureOnMetric.MetricUnit.DEFAULT_UNIT
            comparison = BuildFailureOnMetric.MetricComparison.LESS
        }
    }
}
```

#### 2. **Investigation and Reporting**
- Build time trends
- Success rate analysis
- Test failure tracking
- Resource usage monitoring
- Queue wait time analysis

## Best Practices

### Project Organization

1. **Template Hierarchy**
   ```kotlin
   // Base template for all projects
   object BaseTemplate : Template({
       name = "Base Build Template"
       
       features {
           dockerSupport {
               cleanupPushedImages = true
           }
           perfmon {
           }
       }
       
       failureConditions {
           executionTimeoutMin = 60
       }
   })
   ```

2. **Configuration as Code**
   - Use Kotlin DSL for version control
   - Implement code review for build changes
   - Maintain separate VCS root for settings

### Performance Optimization

1. **Agent Utilization**
   - Configure agent pools by capability
   - Use cloud agents for peak loads
   - Implement agent prioritization

2. **Build Optimization**
   - Enable build caching
   - Use incremental compilation
   - Parallelize independent steps

### Security Best Practices

1. **Credential Management**
   - Use TeamCity's secure parameters
   - Implement least privilege access
   - Regular credential rotation

2. **Network Security**
   - Enable HTTPS for server
   - Use VPN for agent communication
   - Implement IP whitelisting

## Migration and Integration

### Migration from Other CI Systems

#### 1. **From Jenkins**
```kotlin
// Jenkins pipeline equivalent
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }
}

// TeamCity equivalent
object Build : BuildType({
    steps {
        maven {
            goals = "clean package"
        }
    }
})
```

#### 2. **Import Tools**
- Pipeline converters
- Configuration importers
- Historical data migration

### IDE Integration

#### 1. **IntelliJ IDEA Plugin**
- Remote run from IDE
- Build status monitoring
- Personal build execution
- Code inspection results

#### 2. **Visual Studio Plugin**
- Team Explorer integration
- Build triggering
- Work item linking

## Troubleshooting

### Common Issues

1. **Build Agent Problems**
   - Agent disconnection
   - Capability mismatches
   - Resource constraints

2. **Performance Issues**
   - Database optimization
   - Artifact cleanup
   - Build queue optimization

3. **VCS Integration**
   - Authentication failures
   - Checkout problems
   - Branch detection issues

### Diagnostic Tools

1. **TeamCity Diagnostics**
   - Thread dumps
   - Memory analysis
   - Performance snapshots

2. **Logging Configuration**
   ```xml
   <!-- teamcity-server-log4j.xml -->
   <Configuration>
     <Loggers>
       <Logger name="jetbrains.buildServer" level="DEBUG"/>
       <Logger name="jetbrains.buildServer.VCS" level="TRACE"/>
     </Loggers>
   </Configuration>
   ```

## Conclusion

TeamCity provides a robust, feature-rich CI/CD platform with strong enterprise capabilities, extensive customization options, and excellent IDE integration. Its flexibility in deployment options, from simple standalone setups to complex high-availability configurations, makes it suitable for organizations of any size. The platform's focus on build intelligence, comprehensive API, and configuration as code capabilities position it as a powerful choice for modern software delivery pipelines.