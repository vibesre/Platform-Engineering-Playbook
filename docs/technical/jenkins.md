# Jenkins - Extensible Automation Server

## Overview

Jenkins is an open-source automation server that enables developers to build, test, and deploy their software. It provides hundreds of plugins to support building, deploying, and automating any project. Jenkins supports both traditional and modern CI/CD patterns including pipelines as code.

## Core Concepts

### Jenkins Architecture

```groovy
// Jenkins ecosystem components
- Jenkins Master: Central control unit
- Jenkins Agents: Distributed build executors
- Plugins: Extended functionality
- Jobs: Basic work units
- Pipelines: Advanced workflows
- Workspaces: Build directories
- Build Queue: Job scheduling
- Executors: Concurrent build slots
```

### Pipeline Types

#### Declarative Pipeline
```groovy
pipeline {
    agent any
    
    environment {
        APP_NAME = 'MyApp'
        VERSION = '1.0.0'
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'make build'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'make test'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh 'make deploy'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

#### Scripted Pipeline
```groovy
node {
    def app
    
    stage('Clone repository') {
        checkout scm
    }
    
    stage('Build image') {
        app = docker.build("myapp:${env.BUILD_ID}")
    }
    
    stage('Test image') {
        app.inside {
            sh 'make test'
        }
    }
    
    stage('Push image') {
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
}
```

## Basic Pipelines

### Multi-Branch Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 60, unit: 'MINUTES')
        timestamps()
        ansiColor('xterm')
    }
    
    environment {
        NODE_VERSION = '18'
        DOCKER_REGISTRY = 'registry.example.com'
        DOCKER_IMAGE = "${DOCKER_REGISTRY}/myapp"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                    env.GIT_BRANCH_NAME = sh(
                        script: "git rev-parse --abbrev-ref HEAD",
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('Build') {
            agent {
                docker {
                    image "node:${NODE_VERSION}-alpine"
                    args '-v $HOME/.npm:/home/node/.npm'
                }
            }
            steps {
                sh '''
                    npm ci
                    npm run build
                '''
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    agent {
                        docker {
                            image "node:${NODE_VERSION}-alpine"
                            args '-v $HOME/.npm:/home/node/.npm'
                        }
                    }
                    steps {
                        sh 'npm run test:unit'
                    }
                    post {
                        always {
                            junit 'test-results/**/*.xml'
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'coverage',
                                reportFiles: 'index.html',
                                reportName: 'Coverage Report'
                            ])
                        }
                    }
                }
                
                stage('Integration Tests') {
                    agent {
                        docker {
                            image "node:${NODE_VERSION}-alpine"
                            args '-v $HOME/.npm:/home/node/.npm'
                        }
                    }
                    steps {
                        sh 'npm run test:integration'
                    }
                }
                
                stage('Linting') {
                    agent {
                        docker {
                            image "node:${NODE_VERSION}-alpine"
                            args '-v $HOME/.npm:/home/node/.npm'
                        }
                    }
                    steps {
                        sh 'npm run lint'
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                    branch pattern: "release/.*", comparator: "REGEXP"
                }
            }
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-registry-credentials') {
                        def customImage = docker.build("${DOCKER_IMAGE}:${GIT_COMMIT_SHORT}")
                        customImage.push()
                        
                        if (env.BRANCH_NAME == 'main') {
                            customImage.push('latest')
                        }
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    def deploymentEnv = 'production'
                    
                    build job: 'deploy-job', parameters: [
                        string(name: 'ENVIRONMENT', value: deploymentEnv),
                        string(name: 'VERSION', value: env.GIT_COMMIT_SHORT)
                    ]
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            slackSend(
                color: 'good',
                message: "Build Successful: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
            )
            emailext(
                subject: "Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: '''${JELLY_SCRIPT, template="html"}''',
                recipientProviders: [developers(), requestor()]
            )
        }
    }
}
```

### Matrix Builds

```groovy
pipeline {
    agent none
    
    stages {
        stage('Matrix Build') {
            matrix {
                agent any
                axes {
                    axis {
                        name 'PLATFORM'
                        values 'linux', 'windows', 'mac'
                    }
                    axis {
                        name 'NODE_VERSION'
                        values '16', '18', '20'
                    }
                }
                excludes {
                    exclude {
                        axis {
                            name 'PLATFORM'
                            values 'windows'
                        }
                        axis {
                            name 'NODE_VERSION'
                            values '16'
                        }
                    }
                }
                stages {
                    stage('Build') {
                        steps {
                            echo "Building on ${PLATFORM} with Node ${NODE_VERSION}"
                            sh """
                                node --version
                                npm --version
                                npm ci
                                npm run build
                            """
                        }
                    }
                    stage('Test') {
                        steps {
                            sh 'npm test'
                        }
                    }
                }
            }
        }
    }
}
```

## Advanced Features

### Shared Libraries

```groovy
// vars/buildPipeline.groovy
def call(Map config) {
    pipeline {
        agent any
        
        environment {
            APP_NAME = config.appName
            BUILD_TOOL = config.buildTool ?: 'npm'
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
                        switch(env.BUILD_TOOL) {
                            case 'npm':
                                sh 'npm ci && npm run build'
                                break
                            case 'maven':
                                sh 'mvn clean package'
                                break
                            case 'gradle':
                                sh './gradlew build'
                                break
                            default:
                                error "Unknown build tool: ${env.BUILD_TOOL}"
                        }
                    }
                }
            }
            
            stage('Test') {
                steps {
                    script {
                        runTests(env.BUILD_TOOL)
                    }
                }
            }
            
            stage('Package') {
                steps {
                    script {
                        packageApplication(config)
                    }
                }
            }
        }
        
        post {
            always {
                cleanWs()
            }
        }
    }
}

def runTests(buildTool) {
    switch(buildTool) {
        case 'npm':
            sh 'npm test'
            break
        case 'maven':
            sh 'mvn test'
            break
        case 'gradle':
            sh './gradlew test'
            break
    }
}

def packageApplication(config) {
    if (config.docker) {
        docker.build("${config.imageName}:${env.BUILD_NUMBER}")
    } else {
        sh 'tar -czf app.tar.gz .'
        archiveArtifacts artifacts: 'app.tar.gz'
    }
}

// Usage in Jenkinsfile
@Library('shared-library') _

buildPipeline(
    appName: 'my-application',
    buildTool: 'npm',
    docker: true,
    imageName: 'myapp'
)
```

### Dynamic Pipelines

```groovy
// Generate stages dynamically
def generateStages(serviceList) {
    def stages = [:]
    
    serviceList.each { service ->
        stages["Build ${service}"] = {
            stage("Build ${service}") {
                dir(service) {
                    sh 'docker build -t ${service}:${BUILD_NUMBER} .'
                }
            }
        }
        
        stages["Test ${service}"] = {
            stage("Test ${service}") {
                dir(service) {
                    sh 'docker run --rm ${service}:${BUILD_NUMBER} npm test'
                }
            }
        }
    }
    
    return stages
}

pipeline {
    agent any
    
    stages {
        stage('Discover Services') {
            steps {
                script {
                    env.SERVICES = sh(
                        script: "find . -name 'Dockerfile' -exec dirname {} \\; | grep -v '\\./\\.' | sed 's|\\./||'",
                        returnStdout: true
                    ).trim().split('\n')
                }
            }
        }
        
        stage('Build and Test Services') {
            steps {
                script {
                    def stages = generateStages(env.SERVICES)
                    parallel stages
                }
            }
        }
    }
}
```

### Blue Ocean Pipeline

```groovy
pipeline {
    agent any
    
    options {
        skipDefaultCheckout()
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build and Test') {
            parallel {
                stage('Frontend') {
                    agent {
                        docker 'node:18-alpine'
                    }
                    steps {
                        dir('frontend') {
                            sh '''
                                npm ci
                                npm run build
                                npm test
                            '''
                        }
                    }
                }
                
                stage('Backend') {
                    agent {
                        docker 'maven:3.8-openjdk-17'
                    }
                    steps {
                        dir('backend') {
                            sh '''
                                mvn clean package
                                mvn test
                            '''
                        }
                    }
                }
                
                stage('Mobile') {
                    agent {
                        label 'mac'
                    }
                    steps {
                        dir('mobile') {
                            sh '''
                                npm ci
                                npm run build:ios
                                npm run build:android
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Integration Tests') {
            agent {
                docker {
                    image 'docker/compose:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh '''
                    docker-compose up -d
                    docker-compose run tests
                '''
            }
            post {
                always {
                    sh 'docker-compose down'
                }
            }
        }
    }
}
```

## Jenkins Configuration

### Pipeline Configuration as Code

```groovy
// jenkins.yaml - Jenkins Configuration as Code
jenkins:
  systemMessage: "Jenkins CI/CD Server"
  numExecutors: 5
  mode: NORMAL
  
  authorizationStrategy:
    roleBased:
      roles:
        global:
          - name: "admin"
            description: "Jenkins administrators"
            permissions:
              - "Overall/Administer"
            assignments:
              - "admin"
          - name: "developer"
            description: "Developers"
            permissions:
              - "Overall/Read"
              - "Job/Build"
              - "Job/Cancel"
              - "Job/Read"
            assignments:
              - "dev-team"
              
  securityRealm:
    ldap:
      configurations:
        - server: "ldap.example.com"
          rootDN: "dc=example,dc=com"
          userSearchBase: "ou=people"
          userSearch: "uid={0}"
          groupSearchBase: "ou=groups"
          
  clouds:
    - docker:
        name: "docker"
        dockerApi:
          dockerHost:
            uri: "unix:///var/run/docker.sock"
        templates:
          - labelString: "docker-agent"
            dockerTemplateBase:
              image: "jenkins/inbound-agent"
              volumes:
                - "/var/run/docker.sock:/var/run/docker.sock"
              
    - kubernetes:
        name: "kubernetes"
        serverUrl: "https://kubernetes.default"
        skipTlsVerify: true
        namespace: "jenkins"
        jenkinsUrl: "http://jenkins:8080"
        podTemplates:
          - name: "k8s-agent"
            label: "k8s-agent"
            containers:
              - name: "jnlp"
                image: "jenkins/inbound-agent"
              - name: "docker"
                image: "docker:dind"
                privileged: true

unclassified:
  location:
    url: "https://jenkins.example.com"
    adminAddress: "admin@example.com"
    
  gitScm:
    globalConfigName: "Jenkins"
    globalConfigEmail: "jenkins@example.com"
    
  mailer:
    smtpHost: "smtp.example.com"
    smtpPort: "587"
    
  slackNotifier:
    teamDomain: "example"
    tokenCredentialId: "slack-token"
```

### Job DSL

```groovy
// jobs/seed-job.groovy
def gitUrl = 'https://github.com/example/repo.git'
def projects = ['frontend', 'backend', 'api']

projects.each { project ->
    multibranchPipelineJob("${project}-pipeline") {
        branchSources {
            github {
                id("${project}-github")
                repoOwner('example')
                repository(project)
                buildOriginBranch(true)
                buildOriginBranchWithPR(false)
                buildOriginPRMerge(true)
                buildOriginPRHead(false)
                buildForkPRMerge(true)
                buildForkPRHead(false)
                scanCredentialsId('github-credentials')
            }
        }
        
        orphanedItemStrategy {
            discardOldItems {
                numToKeep(10)
                daysToKeep(30)
            }
        }
        
        triggers {
            periodic(5)
        }
        
        factory {
            workflowBranchProjectFactory {
                scriptPath('Jenkinsfile')
            }
        }
        
        configure { project ->
            project / 'properties' / 'com.cloudbees.hudson.plugins.folder.properties.EnvVarsFolderProperty' {
                'envVars' {
                    'envVar' {
                        'key'('PROJECT_NAME')
                        'value'(project)
                    }
                }
            }
        }
    }
}

// Create deployment job
pipelineJob('deploy-to-production') {
    description('Deploy application to production')
    
    parameters {
        stringParam('VERSION', '', 'Version to deploy')
        choiceParam('SERVICE', projects, 'Service to deploy')
        booleanParam('DRY_RUN', true, 'Perform dry run')
    }
    
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url(gitUrl)
                        credentials('git-credentials')
                    }
                    branches('*/main')
                }
            }
            scriptPath('deploy/Jenkinsfile')
        }
    }
    
    properties {
        buildDiscarder {
            strategy {
                logRotator {
                    numToKeepStr('50')
                    daysToKeepStr('30')
                }
            }
        }
    }
}
```

## Docker Integration

### Docker Pipeline

```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        DOCKER_CREDENTIALS = 'docker-registry-creds'
        IMAGE_NAME = "${DOCKER_REGISTRY}/myapp"
        IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT.take(7)}"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Build with build arguments
                    def customImage = docker.build(
                        "${IMAGE_NAME}:${IMAGE_TAG}",
                        "--build-arg NODE_VERSION=18 " +
                        "--build-arg BUILD_DATE=${BUILD_TIMESTAMP} " +
                        "--build-arg VCS_REF=${GIT_COMMIT} " +
                        "--label org.label-schema.build-date=${BUILD_TIMESTAMP} " +
                        "--label org.label-schema.vcs-ref=${GIT_COMMIT} " +
                        "--label org.label-schema.version=${IMAGE_TAG} ."
                    )
                    
                    // Run tests inside container
                    customImage.inside {
                        sh 'npm test'
                    }
                    
                    // Push to registry
                    docker.withRegistry("https://${DOCKER_REGISTRY}", DOCKER_CREDENTIALS) {
                        customImage.push()
                        customImage.push('latest')
                    }
                }
            }
        }
        
        stage('Scan Docker Image') {
            agent {
                docker {
                    image 'aquasec/trivy:latest'
                    args '--entrypoint="" -v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh """
                    trivy image --exit-code 0 --no-progress \
                        --format template --template "@contrib/gitlab.tpl" \
                        -o container-scanning-report.json \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                """
                
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'container-scanning-report.json',
                    reportName: 'Trivy Scan Report'
                ])
            }
        }
        
        stage('Deploy with Docker Compose') {
            when {
                branch 'main'
            }
            steps {
                sshagent(['deployment-ssh-key']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no deploy@production-server << EOF
                            cd /opt/application
                            export IMAGE_TAG=${IMAGE_TAG}
                            docker-compose pull
                            docker-compose up -d
                            docker-compose ps
                        EOF
                    '''
                }
            }
        }
    }
}
```

### Docker Swarm Deployment

```groovy
pipeline {
    agent any
    
    stages {
        stage('Deploy to Swarm') {
            steps {
                script {
                    docker.withServer('tcp://swarm-manager:2376', 'swarm-certs') {
                        sh """
                            docker service update \
                                --image ${IMAGE_NAME}:${IMAGE_TAG} \
                                --update-parallelism 2 \
                                --update-delay 10s \
                                --update-failure-action rollback \
                                myapp
                        """
                    }
                }
            }
        }
    }
}
```

## Kubernetes Integration

### Kubernetes Deployment

```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kubectl
    image: bitnami/kubectl:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - name: kubeconfig
      mountPath: /root/.kube
  - name: helm
    image: alpine/helm:latest
    command:
    - cat
    tty: true
  - name: docker
    image: docker:dind
    securityContext:
      privileged: true
    volumeMounts:
    - name: docker-sock
      mountPath: /var/run/docker.sock
  volumes:
  - name: kubeconfig
    secret:
      secretName: kubeconfig
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
'''
        }
    }
    
    stages {
        stage('Build and Push') {
            steps {
                container('docker') {
                    sh '''
                        docker build -t myapp:${BUILD_NUMBER} .
                        docker tag myapp:${BUILD_NUMBER} registry.example.com/myapp:${BUILD_NUMBER}
                        docker push registry.example.com/myapp:${BUILD_NUMBER}
                    '''
                }
            }
        }
        
        stage('Deploy with Kubectl') {
            steps {
                container('kubectl') {
                    sh """
                        kubectl set image deployment/myapp \
                            myapp=registry.example.com/myapp:${BUILD_NUMBER} \
                            --namespace=production
                        
                        kubectl rollout status deployment/myapp \
                            --namespace=production \
                            --timeout=5m
                    """
                }
            }
        }
        
        stage('Deploy with Helm') {
            steps {
                container('helm') {
                    sh """
                        helm upgrade --install myapp ./helm/myapp \
                            --namespace production \
                            --set image.tag=${BUILD_NUMBER} \
                            --set image.repository=registry.example.com/myapp \
                            --wait
                    """
                }
            }
        }
    }
}
```

## Security

### Credentials Management

```groovy
pipeline {
    agent any
    
    stages {
        stage('Using Credentials') {
            steps {
                // Username and password
                withCredentials([
                    usernamePassword(
                        credentialsId: 'database-creds',
                        usernameVariable: 'DB_USER',
                        passwordVariable: 'DB_PASS'
                    )
                ]) {
                    sh 'echo "Connecting to database as $DB_USER"'
                }
                
                // Secret text
                withCredentials([
                    string(credentialsId: 'api-key', variable: 'API_KEY')
                ]) {
                    sh 'curl -H "Authorization: Bearer $API_KEY" https://api.example.com'
                }
                
                // SSH key
                sshagent(['deployment-key']) {
                    sh 'ssh deploy@server "deploy.sh"'
                }
                
                // Multiple credentials
                withCredentials([
                    file(credentialsId: 'ssl-cert', variable: 'SSL_CERT'),
                    file(credentialsId: 'ssl-key', variable: 'SSL_KEY'),
                    string(credentialsId: 'ssl-pass', variable: 'SSL_PASS')
                ]) {
                    sh '''
                        cp $SSL_CERT /etc/ssl/cert.pem
                        cp $SSL_KEY /etc/ssl/key.pem
                        echo $SSL_PASS | openssl rsa -in /etc/ssl/key.pem -out /etc/ssl/key-decrypted.pem
                    '''
                }
            }
        }
    }
}
```

### Security Scanning

```groovy
pipeline {
    agent any
    
    stages {
        stage('SAST Scan') {
            steps {
                script {
                    def scannerHome = tool 'SonarQube Scanner'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=myproject \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=${SONAR_HOST_URL} \
                                -Dsonar.login=${SONAR_AUTH_TOKEN}
                        """
                    }
                }
            }
        }
        
        stage('Dependency Check') {
            steps {
                dependencyCheck additionalArguments: '''
                    --format HTML
                    --format XML
                    --suppression suppression.xml
                ''', odcInstallation: 'dependency-check'
                
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'dependency-check-report.html',
                    reportName: 'Dependency Check Report'
                ])
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
}
```

## Performance Optimization

### Parallel Execution

```groovy
pipeline {
    agent none
    
    stages {
        stage('Parallel Tests') {
            parallel {
                stage('Chrome Tests') {
                    agent {
                        docker 'selenium/standalone-chrome'
                    }
                    steps {
                        sh 'npm run test:e2e -- --browser chrome'
                    }
                }
                
                stage('Firefox Tests') {
                    agent {
                        docker 'selenium/standalone-firefox'
                    }
                    steps {
                        sh 'npm run test:e2e -- --browser firefox'
                    }
                }
                
                stage('Safari Tests') {
                    agent {
                        label 'mac'
                    }
                    steps {
                        sh 'npm run test:e2e -- --browser safari'
                    }
                }
            }
        }
        
        stage('Fan-out/Fan-in') {
            steps {
                script {
                    def deployments = [:]
                    def environments = ['dev', 'staging', 'uat']
                    
                    environments.each { env ->
                        deployments["Deploy to ${env}"] = {
                            build job: 'deploy-job', parameters: [
                                string(name: 'ENVIRONMENT', value: env),
                                string(name: 'VERSION', value: "${BUILD_NUMBER}")
                            ]
                        }
                    }
                    
                    parallel deployments
                }
            }
        }
    }
}
```

### Caching Strategies

```groovy
pipeline {
    agent any
    
    options {
        // Keep only last 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // Don't checkout automatically
        skipDefaultCheckout()
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Use shallow clone
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    extensions: [
                        [$class: 'CloneOption', depth: 1, shallow: true],
                        [$class: 'CheckoutOption', timeout: 10]
                    ],
                    userRemoteConfigs: [[url: 'https://github.com/example/repo.git']]
                ])
            }
        }
        
        stage('Cache Dependencies') {
            steps {
                script {
                    // Cache node_modules
                    def nodeModulesCache = "${WORKSPACE}/.cache/node_modules"
                    def packageLockHash = sh(
                        script: "sha256sum package-lock.json | cut -d' ' -f1",
                        returnStdout: true
                    ).trim()
                    
                    if (fileExists("${nodeModulesCache}/${packageLockHash}.tar.gz")) {
                        sh "tar -xzf ${nodeModulesCache}/${packageLockHash}.tar.gz"
                    } else {
                        sh "npm ci"
                        sh "mkdir -p ${nodeModulesCache}"
                        sh "tar -czf ${nodeModulesCache}/${packageLockHash}.tar.gz node_modules"
                    }
                }
            }
        }
    }
}
```

## Monitoring and Notifications

### Advanced Notifications

```groovy
def notifyBuild(String buildStatus = 'STARTED') {
    buildStatus = buildStatus ?: 'SUCCESS'
    
    def colorName = 'RED'
    def colorCode = '#FF0000'
    def emoji = ':x:'
    
    if (buildStatus == 'STARTED') {
        colorName = 'YELLOW'
        colorCode = '#FFFF00'
        emoji = ':construction:'
    } else if (buildStatus == 'SUCCESS') {
        colorName = 'GREEN'
        colorCode = '#00FF00'
        emoji = ':white_check_mark:'
    }
    
    def message = """
        ${emoji} *${buildStatus}*: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'
        
        *Branch:* ${env.BRANCH_NAME}
        *Commit:* ${env.GIT_COMMIT}
        *Author:* ${env.GIT_AUTHOR}
        
        <${env.BUILD_URL}|Open in Jenkins>
    """
    
    // Slack notification
    slackSend(
        color: colorCode,
        message: message,
        channel: '#ci-notifications',
        teamDomain: 'example',
        tokenCredentialId: 'slack-token'
    )
    
    // Email notification
    if (buildStatus != 'STARTED') {
        emailext(
            subject: "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
            body: """
                <p>${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                <p>Check console output at <a href='${env.BUILD_URL}'>${env.BUILD_URL}</a></p>
            """,
            recipientProviders: [
                developers(),
                requestor(),
                culprits()
            ],
            mimeType: 'text/html'
        )
    }
    
    // MS Teams notification
    office365ConnectorSend(
        webhookUrl: "${TEAMS_WEBHOOK}",
        color: colorCode,
        status: buildStatus,
        message: message
    )
}

pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    notifyBuild('STARTED')
                }
                sh 'make build'
            }
        }
    }
    
    post {
        success {
            notifyBuild('SUCCESS')
        }
        failure {
            notifyBuild('FAILURE')
        }
        unstable {
            notifyBuild('UNSTABLE')
        }
    }
}
```

## Troubleshooting

### Debug Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Debug Information') {
            steps {
                script {
                    // Print all environment variables
                    sh 'printenv | sort'
                    
                    // Print Jenkins specific variables
                    echo "Job Name: ${env.JOB_NAME}"
                    echo "Build Number: ${env.BUILD_NUMBER}"
                    echo "Workspace: ${env.WORKSPACE}"
                    echo "Node Name: ${env.NODE_NAME}"
                    
                    // Print Git information
                    sh '''
                        echo "Git Branch: $(git rev-parse --abbrev-ref HEAD)"
                        echo "Git Commit: $(git rev-parse HEAD)"
                        echo "Git Author: $(git log -1 --pretty=format:'%an <%ae>')"
                    '''
                    
                    // Check available tools
                    sh '''
                        echo "=== Available Tools ==="
                        which docker || echo "Docker not found"
                        which kubectl || echo "Kubectl not found"
                        which helm || echo "Helm not found"
                        java -version || echo "Java not found"
                        node --version || echo "Node not found"
                    '''
                    
                    // Workspace information
                    sh '''
                        echo "=== Workspace Info ==="
                        pwd
                        ls -la
                        df -h .
                        du -sh .
                    '''
                }
            }
        }
        
        stage('Pipeline Replay') {
            when {
                expression { params.DEBUG_MODE == true }
            }
            steps {
                script {
                    // Allow pipeline replay with modifications
                    input message: 'Pause for debugging?', ok: 'Continue'
                    
                    // Start interactive shell
                    sh '''
                        echo "Starting debug shell..."
                        echo "Type 'exit' to continue pipeline"
                        bash -i
                    '''
                }
            }
        }
    }
}
```

## Best Practices

### Pipeline Best Practices

```groovy
// Good pipeline structure
@Library('jenkins-shared-library@v1.0.0') _

pipeline {
    agent {
        label 'linux && docker'
    }
    
    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        skipDefaultCheckout()
    }
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'prod'],
            description: 'Target environment'
        )
        booleanParam(
            name: 'SKIP_TESTS',
            defaultValue: false,
            description: 'Skip running tests'
        )
    }
    
    environment {
        // Use Jenkins credentials
        DOCKER_CREDENTIALS = credentials('docker-hub')
        SONAR_TOKEN = credentials('sonar-token')
        
        // Dynamic environment variables
        VERSION = sh(script: 'git describe --tags --always', returnStdout: true).trim()
        BUILD_TIME = sh(script: 'date -u +%Y%m%d-%H%M%S', returnStdout: true).trim()
    }
    
    stages {
        stage('Preparation') {
            steps {
                cleanWs()
                checkout scm
                stash includes: '**', name: 'source'
            }
        }
        
        stage('Build') {
            steps {
                unstash 'source'
                sh './build.sh'
            }
        }
        
        stage('Test') {
            when {
                expression { params.SKIP_TESTS != true }
            }
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh './test-unit.sh'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh './test-integration.sh'
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                allOf {
                    branch 'main'
                    expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
                }
            }
            steps {
                milestone(1)
                lock(resource: "deploy-${params.ENVIRONMENT}") {
                    sh "./deploy.sh ${params.ENVIRONMENT}"
                }
            }
        }
    }
    
    post {
        always {
            junit '**/target/surefire-reports/*.xml'
            archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true
            deleteDir()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        unstable {
            echo 'Pipeline unstable'
        }
        failure {
            echo 'Pipeline failed'
        }
        changed {
            echo 'Pipeline state changed'
        }
    }
}
```

## Production Patterns

### Blue-Green Deployment

```groovy
def deployBlueGreen(String environment, String version) {
    def currentColor = sh(
        script: "kubectl get service myapp-active -o jsonpath='{.spec.selector.color}'",
        returnStdout: true
    ).trim()
    
    def newColor = currentColor == 'blue' ? 'green' : 'blue'
    
    echo "Current active: ${currentColor}, deploying to: ${newColor}"
    
    // Deploy to inactive color
    sh """
        kubectl set image deployment/myapp-${newColor} \
            myapp=myapp:${version} \
            --namespace=${environment}
        
        kubectl rollout status deployment/myapp-${newColor} \
            --namespace=${environment}
    """
    
    // Run smoke tests
    def serviceIP = sh(
        script: "kubectl get service myapp-${newColor} -o jsonpath='{.status.loadBalancer.ingress[0].ip}'",
        returnStdout: true
    ).trim()
    
    sh "curl -f http://${serviceIP}/health || exit 1"
    
    // Switch traffic
    sh """
        kubectl patch service myapp-active \
            -p '{"spec":{"selector":{"color":"${newColor}"}}}' \
            --namespace=${environment}
    """
    
    echo "Deployment complete. ${newColor} is now active."
}

pipeline {
    agent any
    
    parameters {
        string(name: 'VERSION', description: 'Version to deploy')
    }
    
    stages {
        stage('Deploy Blue-Green') {
            steps {
                script {
                    deployBlueGreen('production', params.VERSION)
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                sh '''
                    for i in {1..10}; do
                        curl -f https://app.example.com/health || exit 1
                        sleep 5
                    done
                '''
            }
        }
        
        stage('Rollback?') {
            input {
                message "Rollback deployment?"
                ok "No, keep current deployment"
                parameters {
                    booleanParam(name: 'ROLLBACK', defaultValue: false)
                }
            }
            when {
                expression { params.ROLLBACK == true }
            }
            steps {
                script {
                    def currentColor = sh(
                        script: "kubectl get service myapp-active -o jsonpath='{.spec.selector.color}'",
                        returnStdout: true
                    ).trim()
                    def previousColor = currentColor == 'blue' ? 'green' : 'blue'
                    
                    sh """
                        kubectl patch service myapp-active \
                            -p '{"spec":{"selector":{"color":"${previousColor}"}}}' \
                            --namespace=production
                    """
                }
            }
        }
    }
}
```

### Canary Deployment

```groovy
def canaryDeploy(String version, int percentage) {
    sh """
        # Update canary deployment
        kubectl set image deployment/myapp-canary myapp=myapp:${version}
        kubectl rollout status deployment/myapp-canary
        
        # Adjust traffic split
        kubectl patch virtualservice myapp --type merge -p '{
            "spec": {
                "http": [{
                    "match": [{"headers": {"canary": {"exact": "true"}}}],
                    "route": [{
                        "destination": {
                            "host": "myapp-canary",
                            "subset": "canary"
                        }
                    }]
                }, {
                    "route": [{
                        "destination": {
                            "host": "myapp-stable",
                            "subset": "stable"
                        },
                        "weight": $((100 - percentage))
                    }, {
                        "destination": {
                            "host": "myapp-canary",
                            "subset": "canary"
                        },
                        "weight": ${percentage}
                    }]
                }]
            }
        }'
    """
}

pipeline {
    agent any
    
    stages {
        stage('Canary Deployment') {
            steps {
                script {
                    // Start with 10% traffic
                    canaryDeploy("${VERSION}", 10)
                    
                    // Monitor for 5 minutes
                    sleep(time: 5, unit: 'MINUTES')
                    
                    // Check metrics
                    def errorRate = sh(
                        script: '''
                            curl -s "http://prometheus:9090/api/v1/query?query=rate(http_requests_total{job='myapp-canary',status=~'5..'}[5m])" |
                            jq -r '.data.result[0].value[1]'
                        ''',
                        returnStdout: true
                    ).trim().toFloat()
                    
                    if (errorRate < 0.01) {
                        // Increase to 50%
                        canaryDeploy("${VERSION}", 50)
                        sleep(time: 5, unit: 'MINUTES')
                        
                        // Full deployment
                        canaryDeploy("${VERSION}", 100)
                    } else {
                        error "High error rate detected: ${errorRate}"
                    }
                }
            }
        }
    }
}
```

## Best Practices Summary

1. **Use Declarative Pipelines**: Easier to read and maintain
2. **Version Control Everything**: Store Jenkinsfile in repo
3. **Use Shared Libraries**: Reuse common patterns
4. **Implement Proper Security**: Use credentials properly
5. **Parallelize When Possible**: Speed up builds
6. **Clean Workspaces**: Avoid stale data issues
7. **Set Timeouts**: Prevent hanging builds
8. **Use Milestones**: Control concurrent deployments
9. **Archive Artifacts**: Keep build outputs
10. **Monitor Pipeline Health**: Track success rates

## Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Pipeline Syntax Reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins Plugins](https://plugins.jenkins.io/)
- [Jenkins Best Practices](https://wiki.jenkins.io/display/JENKINS/Jenkins+Best+Practices)
- [CloudBees Documentation](https://docs.cloudbees.com/)