# GitLab CI/CD - GitLab's Integrated CI/CD

## Overview

GitLab CI/CD is a powerful, integrated continuous integration and deployment tool built into GitLab. It uses YAML configuration files to define pipelines, supports complex workflows, and provides features like Auto DevOps, security scanning, and deployment environments.

## Core Concepts

### Pipeline Architecture

```yaml
# .gitlab-ci.yml
stages:          # Pipeline stages (run sequentially)
  - build
  - test
  - deploy

variables:       # Global variables
  DOCKER_DRIVER: overlay2
  CACHE_DIR: .cache

before_script:   # Run before each job
  - echo "Starting job"

after_script:    # Run after each job
  - echo "Job complete"

default:         # Default job configuration
  image: node:18-alpine
  retry: 2
  timeout: 1 hour
```

### Job Definition

```yaml
job_name:
  stage: test                    # Stage assignment
  image: node:18                 # Docker image
  services:                      # Service containers
    - postgres:latest
  variables:                     # Job variables
    NODE_ENV: test
  cache:                        # Caching configuration
    paths:
      - node_modules/
  artifacts:                    # Job artifacts
    paths:
      - dist/
    expire_in: 1 week
  script:                       # Commands to run
    - npm test
  only:                        # Run conditions
    - main
  except:                      # Skip conditions
    - tags
  when: on_success             # When to run
  allow_failure: false         # Job can fail
  dependencies:                # Job dependencies
    - build_job
  needs:                       # DAG dependencies
    - build_job
```

## Basic CI/CD Pipelines

### Node.js Application

```yaml
image: node:18-alpine

stages:
  - install
  - build
  - test
  - deploy

variables:
  npm_config_cache: "$CI_PROJECT_DIR/.npm"
  CYPRESS_CACHE_FOLDER: "$CI_PROJECT_DIR/cache/Cypress"

cache:
  key:
    files:
      - package-lock.json
  paths:
    - .npm
    - cache/Cypress
    - node_modules

install:
  stage: install
  script:
    - npm ci --cache .npm --prefer-offline
  artifacts:
    paths:
      - node_modules
    expire_in: 1 hour

lint:
  stage: build
  needs: ["install"]
  script:
    - npm run lint
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

build:
  stage: build
  needs: ["install"]
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

test:unit:
  stage: test
  needs: ["install"]
  script:
    - npm run test:unit -- --coverage
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
      junit: junit.xml

test:e2e:
  stage: test
  needs: ["install", "build"]
  image: cypress/browsers:node18.12.0-chrome107
  script:
    - npm run test:e2e
  artifacts:
    when: always
    paths:
      - cypress/screenshots
      - cypress/videos
    expire_in: 1 week

deploy:staging:
  stage: deploy
  needs: ["build", "test:unit"]
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - npm run deploy:staging
  only:
    - develop

deploy:production:
  stage: deploy
  needs: ["build", "test:unit", "test:e2e"]
  environment:
    name: production
    url: https://example.com
  script:
    - npm run deploy:production
  when: manual
  only:
    - main
```

### Docker-based Pipeline

```yaml
image: docker:latest

services:
  - docker:dind

stages:
  - build
  - test
  - scan
  - deploy

variables:
  DOCKER_HOST: tcp://docker:2375
  DOCKER_TLS_CERTDIR: ""
  CONTAINER_TEST_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG
  CONTAINER_RELEASE_IMAGE: $CI_REGISTRY_IMAGE:latest
  CONTAINER_TAGGED_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_TAG

before_script:
  - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

build:
  stage: build
  script:
    - docker build --pull -t $CONTAINER_TEST_IMAGE .
    - docker push $CONTAINER_TEST_IMAGE

test:
  stage: test
  script:
    - docker pull $CONTAINER_TEST_IMAGE
    - docker run $CONTAINER_TEST_IMAGE npm test

security_scan:
  stage: scan
  image: registry.gitlab.com/security-products/analyzers/trivy:latest
  script:
    - trivy image --exit-code 0 --no-progress --format template --template "@contrib/gitlab.tpl" -o gl-container-scanning-report.json $CONTAINER_TEST_IMAGE
    - trivy image --exit-code 1 --severity CRITICAL --no-progress $CONTAINER_TEST_IMAGE
  artifacts:
    reports:
      container_scanning: gl-container-scanning-report.json

release:
  stage: deploy
  script:
    - docker pull $CONTAINER_TEST_IMAGE
    - docker tag $CONTAINER_TEST_IMAGE $CONTAINER_RELEASE_IMAGE
    - docker push $CONTAINER_RELEASE_IMAGE
  only:
    - main

release-tag:
  stage: deploy
  script:
    - docker pull $CONTAINER_TEST_IMAGE
    - docker tag $CONTAINER_TEST_IMAGE $CONTAINER_TAGGED_IMAGE
    - docker push $CONTAINER_TAGGED_IMAGE
  only:
    - tags
```

## Advanced Features

### Multi-Project Pipelines

```yaml
# Trigger downstream pipeline
trigger_downstream:
  stage: deploy
  trigger:
    project: my-group/deployment-project
    branch: main
    strategy: depend  # Wait for completion
  variables:
    UPSTREAM_VERSION: $CI_COMMIT_SHA

# Parent-child pipelines
generate_config:
  stage: build
  script:
    - ./generate-ci-config.sh > generated-ci.yml
  artifacts:
    paths:
      - generated-ci.yml

child_pipeline:
  stage: test
  trigger:
    include:
      - artifact: generated-ci.yml
        job: generate_config
    strategy: depend
```

### Dynamic Pipelines

```yaml
# Dynamic job generation
.job_template:
  script:
    - echo "Running tests for $MODULE"
  only:
    - merge_requests

generate_jobs:
  stage: .pre
  script:
    - |
      cat > generated-jobs.yml << EOF
      stages:
        - test
      EOF
      for module in $(find . -name "package.json" -not -path "./node_modules/*" | xargs dirname); do
        cat >> generated-jobs.yml << EOF
      
      test:${module}:
        extends: .job_template
        stage: test
        variables:
          MODULE: ${module}
        script:
          - cd ${module}
          - npm test
      EOF
      done
  artifacts:
    paths:
      - generated-jobs.yml

trigger_dynamic:
  stage: .pre
  needs: ["generate_jobs"]
  trigger:
    include:
      - artifact: generated-jobs.yml
        job: generate_jobs
```

### Parallel Matrix Jobs

```yaml
test:
  stage: test
  image: $IMAGE
  script:
    - npm test
  parallel:
    matrix:
      - IMAGE: ['node:16', 'node:18', 'node:20']
        OS: ['alpine', 'bullseye']
  variables:
    NODE_IMAGE: $IMAGE-$OS

# Results in 6 jobs:
# test: [node:16-alpine]
# test: [node:16-bullseye]
# test: [node:18-alpine]
# test: [node:18-bullseye]
# test: [node:20-alpine]
# test: [node:20-bullseye]

browser_test:
  stage: test
  parallel:
    matrix:
      - BROWSER: ['chrome', 'firefox', 'safari']
        VIEWPORT: ['mobile', 'tablet', 'desktop']
  script:
    - npm run test:e2e -- --browser $BROWSER --viewport $VIEWPORT
```

### DAG Pipelines

```yaml
stages:
  - build
  - test
  - deploy

# Independent build jobs
build:frontend:
  stage: build
  script:
    - cd frontend && npm run build

build:backend:
  stage: build
  script:
    - cd backend && npm run build

build:docs:
  stage: build
  script:
    - npm run docs:build

# Tests with needs (DAG)
test:frontend:
  stage: test
  needs: ["build:frontend"]
  script:
    - cd frontend && npm test

test:backend:
  stage: test
  needs: ["build:backend"]
  script:
    - cd backend && npm test

test:integration:
  stage: test
  needs: ["build:frontend", "build:backend"]
  script:
    - npm run test:integration

# Deploy only after specific tests
deploy:staging:
  stage: deploy
  needs:
    - job: test:frontend
    - job: test:backend
    - job: test:integration
      artifacts: true
  script:
    - ./deploy.sh staging
```

## GitLab-Specific Features

### Environments and Deployments

```yaml
deploy:review:
  stage: deploy
  script:
    - ./deploy-review.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_COMMIT_REF_SLUG.review.example.com
    on_stop: stop:review
    auto_stop_in: 1 week
  only:
    - merge_requests

stop:review:
  stage: deploy
  script:
    - ./stop-review.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    action: stop
  when: manual
  only:
    - merge_requests

deploy:production:
  stage: deploy
  script:
    - ./deploy-prod.sh
  environment:
    name: production
    url: https://example.com
    kubernetes:
      namespace: production
  resource_group: production  # Ensure only one deployment at a time
  only:
    - main
```

### Security Scanning

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/License-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: DAST.gitlab-ci.yml

# Custom security job
custom_security_scan:
  stage: test
  image: owasp/zap2docker-stable
  script:
    - zap-baseline.py -t https://staging.example.com -g gen.conf -r zap-report.html
  artifacts:
    paths:
      - zap-report.html
    expire_in: 1 week
  allow_failure: true

# Override SAST settings
sast:
  variables:
    SAST_EXCLUDED_PATHS: "spec,test,vendor,node_modules"
    SAST_EXCLUDED_ANALYZERS: "eslint,nodejs-scan"
```

### Code Quality

```yaml
include:
  - template: Code-Quality.gitlab-ci.yml

code_quality:
  artifacts:
    paths:
      - gl-code-quality-report.json
    reports:
      codequality: gl-code-quality-report.json

# Custom code quality checks
eslint:
  stage: test
  script:
    - npm run lint -- --format gitlab
  artifacts:
    reports:
      codequality: eslint-report.json

sonarqube:
  stage: test
  image: sonarsource/sonar-scanner-cli:latest
  variables:
    SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"
    GIT_DEPTH: "0"
  cache:
    key: "${CI_JOB_NAME}"
    paths:
      - .sonar/cache
  script:
    - sonar-scanner
      -Dsonar.projectKey=$CI_PROJECT_PATH_SLUG
      -Dsonar.sources=.
      -Dsonar.host.url=$SONAR_HOST_URL
      -Dsonar.login=$SONAR_TOKEN
  allow_failure: true
```

## Caching Strategies

### Advanced Caching

```yaml
# Global cache configuration
cache: &global_cache
  key:
    files:
      - package-lock.json
      - yarn.lock
  paths:
    - node_modules/
    - .yarn/
    - .cache/
  policy: pull-push

# Job-specific cache
build:
  cache:
    <<: *global_cache
    policy: pull-push  # Default: download and upload

test:
  cache:
    <<: *global_cache
    policy: pull  # Only download, don't upload

# Multiple cache keys with fallback
complex_cache:
  cache:
    - key: "$CI_COMMIT_REF_SLUG-$CI_JOB_NAME"
      paths:
        - build/
    - key: "$CI_COMMIT_REF_SLUG"
      paths:
        - node_modules/
    - key: main
      paths:
        - node_modules/

# Distributed cache with S3
variables:
  CACHE_DRIVER: s3
  CACHE_S3_BUCKET_LOCATION: us-east-1
  CACHE_S3_BUCKET_NAME: gitlab-runner-cache
  CACHE_SHARED: "true"
```

### Artifact Management

```yaml
build:
  script:
    - make build
  artifacts:
    name: "$CI_JOB_NAME-$CI_COMMIT_REF_SLUG"
    paths:
      - dist/
      - build/
    exclude:
      - build/**/*.log
    reports:
      dotenv: build.env
      junit: test-results.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    expose_as: 'Build artifacts'
    when: on_success
    expire_in: 1 week

# Pass artifacts between stages
test:
  dependencies:
    - build  # Only download artifacts from 'build' job
  script:
    - ls -la dist/  # Artifacts are available

# Use artifacts from other pipelines
external_artifacts:
  needs:
    - project: other-group/other-project
      job: build
      ref: main
      artifacts: true
```

## GitLab Runners

### Runner Configuration

```yaml
# Runner tags
test:unit:
  tags:
    - docker
    - linux
    - shared

test:ios:
  tags:
    - ios
    - xcode-13
    - metal

# Runner-specific image
deploy:
  image: alpine:latest
  tags:
    - shell
  script:
    - ./deploy.sh

# Kubernetes runner
k8s_job:
  tags:
    - kubernetes
  image: bitnami/kubectl:latest
  script:
    - kubectl get pods
```

### Custom Runner Setup

```toml
# /etc/gitlab-runner/config.toml
concurrent = 4
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "docker-runner"
  url = "https://gitlab.com/"
  token = "TOKEN"
  executor = "docker"
  
  [runners.custom_build_dir]
    enabled = true
  
  [runners.docker]
    tls_verify = false
    image = "docker:latest"
    privileged = true
    disable_cache = false
    volumes = ["/cache", "/var/run/docker.sock:/var/run/docker.sock"]
    shm_size = 0
  
  [runners.cache]
    Type = "s3"
    Shared = true
    
    [runners.cache.s3]
      ServerAddress = "s3.amazonaws.com"
      AccessKey = "ACCESS_KEY"
      SecretKey = "SECRET_KEY"
      BucketName = "runner-cache"
      BucketLocation = "us-east-1"

[[runners]]
  name = "kubernetes-runner"
  url = "https://gitlab.com/"
  token = "TOKEN"
  executor = "kubernetes"
  
  [runners.kubernetes]
    namespace = "gitlab-runner"
    image = "alpine:latest"
    cpu_limit = "1"
    memory_limit = "1Gi"
    service_cpu_limit = "1"
    service_memory_limit = "1Gi"
    helper_cpu_limit = "500m"
    helper_memory_limit = "100Mi"
```

## Advanced Workflows

### Review Apps

```yaml
.review:
  image: alpine:latest
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_COMMIT_REF_SLUG.review.example.com
    on_stop: stop_review
    auto_stop_in: 2 days
  rules:
    - if: $CI_MERGE_REQUEST_ID
      when: manual

deploy_review:
  extends: .review
  stage: deploy
  script:
    - echo "Deploy to review environment"
    - ./scripts/deploy-review.sh
  environment:
    action: start

stop_review:
  extends: .review
  stage: deploy
  variables:
    GIT_STRATEGY: none
  script:
    - echo "Stop review environment"
    - ./scripts/stop-review.sh
  environment:
    action: stop
  when: manual
```

### Auto DevOps

```yaml
# .gitlab-ci.yml for custom Auto DevOps
include:
  - template: Auto-DevOps.gitlab-ci.yml

variables:
  POSTGRES_ENABLED: "false"
  KUBERNETES_MEMORY_REQUEST: "300Mi"
  KUBERNETES_MEMORY_LIMIT: "500Mi"
  
  # Customize stages
  STAGING_ENABLED: "false"
  CANARY_ENABLED: "true"
  INCREMENTAL_ROLLOUT_ENABLED: "true"
  
  # Security scanning
  CONTAINER_SCANNING_DISABLED: "false"
  DAST_DISABLED: "true"
  DEPENDENCY_SCANNING_DISABLED: "false"
  LICENSE_MANAGEMENT_DISABLED: "false"
  SAST_DISABLED: "false"
  SECRET_DETECTION_DISABLED: "false"

# Override specific jobs
build:
  variables:
    DOCKER_BUILDKIT: 1
  before_script:
    - echo "Custom build setup"

production:
  environment:
    name: production
    url: https://app.example.com
  when: manual
```

### Release Management

```yaml
stages:
  - build
  - test
  - release

variables:
  CONTAINER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

release:
  stage: release
  image: registry.gitlab.com/gitlab-org/release-cli:latest
  rules:
    - if: $CI_COMMIT_TAG
  script:
    - echo "Creating release for $CI_COMMIT_TAG"
  release:
    tag_name: $CI_COMMIT_TAG
    name: 'Release $CI_COMMIT_TAG'
    description: |
      ## Release $CI_COMMIT_TAG
      
      ### Features
      - Feature 1
      - Feature 2
      
      ### Fixes
      - Fix 1
      - Fix 2
    assets:
      links:
        - name: 'Linux Binary'
          url: 'https://example.com/releases/linux/$CI_COMMIT_TAG'
        - name: 'Windows Binary'
          url: 'https://example.com/releases/windows/$CI_COMMIT_TAG'
        - name: 'MacOS Binary'
          url: 'https://example.com/releases/macos/$CI_COMMIT_TAG'

# Semantic release
semantic_release:
  stage: release
  image: node:18
  before_script:
    - npm install -g semantic-release @semantic-release/gitlab
  script:
    - semantic-release
  only:
    - main
```

## Performance Optimization

### Pipeline Optimization

```yaml
# Fail fast
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH

# Resource optimization
default:
  interruptible: true  # Allow auto-cancellation
  retry:
    max: 2
    when:
      - unknown_failure
      - api_failure
      - runner_system_failure

# Parallel execution
test:
  parallel: 3
  script:
    - npm run test -- --shard=$CI_NODE_INDEX/$CI_NODE_TOTAL

# Job dependencies optimization
fast_test:
  stage: test
  script:
    - npm run test:unit
  needs: []  # Start immediately

integration_test:
  stage: test
  needs: ["build"]  # Only needs build
  script:
    - npm run test:integration
```

### Resource Management

```yaml
# Resource limits
heavy_job:
  script:
    - ./intensive-task.sh
  resource_group: production
  timeout: 2 hours
  tags:
    - high-memory
  variables:
    KUBERNETES_CPU_REQUEST: "2000m"
    KUBERNETES_CPU_LIMIT: "4000m"
    KUBERNETES_MEMORY_REQUEST: "4Gi"
    KUBERNETES_MEMORY_LIMIT: "8Gi"

# Scheduled pipelines
scheduled_cleanup:
  only:
    - schedules
  script:
    - ./cleanup-old-data.sh

# Manual interventions
deploy_production:
  stage: deploy
  when: manual
  allow_failure: false
  environment:
    name: production
  only:
    - main
```

## Troubleshooting

### Debug Techniques

```yaml
debug_job:
  stage: test
  script:
    - echo "=== Environment Variables ==="
    - export | grep CI_
    - echo "=== System Information ==="
    - uname -a
    - df -h
    - free -m
    - echo "=== Directory Structure ==="
    - pwd
    - ls -la
    - echo "=== Git Information ==="
    - git log -1
    - git status
    - git remote -v
  when: manual

# Interactive debug
debug_interactive:
  stage: debug
  image: alpine:latest
  script:
    - apk add --no-cache curl
    - curl -sL https://github.com/shipwright-io/build/releases/download/v0.11.0/tmate_2.4.0_linux_amd64.tar.gz | tar xz
    - ./tmate -F
  timeout: 30 minutes
  when: manual
```

### Common Issues

```yaml
# Fix submodules
variables:
  GIT_SUBMODULE_STRATEGY: recursive
  GIT_DEPTH: 0  # Full clone

# Handle large repos
variables:
  GIT_STRATEGY: fetch  # Instead of clone
  GIT_CHECKOUT: "false"  # Skip checkout
  
# Custom checkout
before_script:
  - git checkout -B "$CI_COMMIT_REF_NAME" "$CI_COMMIT_SHA"

# Fix permissions
fix_permissions:
  before_script:
    - chmod +x ./scripts/*.sh
    - find . -type f -name "*.sh" -exec chmod +x {} \;

# Timeout handling
long_running_job:
  timeout: 3 hours
  retry:
    max: 1
    when: 
      - job_execution_timeout
```

## Best Practices

### Pipeline Structure

```yaml
# Well-organized pipeline
workflow:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      variables:
        DEPLOY_ENV: "production"
    - if: $CI_COMMIT_BRANCH == "develop"
      variables:
        DEPLOY_ENV: "staging"
    - if: $CI_MERGE_REQUEST_IID
      variables:
        DEPLOY_ENV: "review"

.default_rules:
  rules:
    - if: $CI_PIPELINE_SOURCE == "push"
    - if: $CI_PIPELINE_SOURCE == "web"
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

stages:
  - validate
  - build
  - test
  - security
  - deploy
  - cleanup

# Validation stage
lint:
  extends: .default_rules
  stage: validate
  script:
    - npm run lint

# Conditional deployment
deploy:
  extends: .default_rules
  stage: deploy
  script:
    - echo "Deploying to $DEPLOY_ENV"
  environment:
    name: $DEPLOY_ENV
  rules:
    - if: $DEPLOY_ENV == "production"
      when: manual
    - when: on_success
```

### Security Best Practices

```yaml
# Secure variables
deploy:
  script:
    - 'echo "Deploy key: $DEPLOY_KEY" | base64 -d > deploy.key'
    - chmod 600 deploy.key
    - ssh -i deploy.key user@server "deploy.sh"
  after_script:
    - rm -f deploy.key

# Protected environments
production:
  environment:
    name: production
    deployment_tier: production
  only:
    - main
  when: manual

# Masked variables
variables:
  DATABASE_URL: $DATABASE_URL  # Masked in settings
  API_KEY: $API_KEY           # Masked in settings
```

## Integration Examples

### Kubernetes Integration

```yaml
.kube_config:
  before_script:
    - kubectl config set-cluster k8s --server="$KUBE_URL" --insecure-skip-tls-verify=true
    - kubectl config set-credentials gitlab --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=gitlab --namespace="$KUBE_NAMESPACE"
    - kubectl config use-context default

deploy_k8s:
  extends: .kube_config
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - kubectl rollout status deployment/app
  environment:
    name: production
    kubernetes:
      namespace: production
```

### Terraform Integration

```yaml
.terraform:
  image: hashicorp/terraform:1.5
  before_script:
    - terraform init -backend-config="bucket=$TF_STATE_BUCKET"
  cache:
    paths:
      - .terraform

plan:
  extends: .terraform
  stage: plan
  script:
    - terraform plan -out=plan.tfplan
  artifacts:
    paths:
      - plan.tfplan

apply:
  extends: .terraform
  stage: deploy
  dependencies:
    - plan
  script:
    - terraform apply plan.tfplan
  when: manual
  only:
    - main
```

## Performance Metrics

```yaml
# Pipeline metrics collection
.metrics:
  after_script:
    - |
      echo "Job Metrics:"
      echo "Duration: $(($(date +%s) - $CI_JOB_STARTED_AT))"
      echo "Status: $CI_JOB_STATUS"
      curl -X POST https://metrics.example.com/gitlab \
        -H "Content-Type: application/json" \
        -d "{
          \"pipeline_id\": \"$CI_PIPELINE_ID\",
          \"job_name\": \"$CI_JOB_NAME\",
          \"duration\": $(($(date +%s) - $CI_JOB_STARTED_AT)),
          \"status\": \"$CI_JOB_STATUS\"
        }"

test:
  extends: .metrics
  script:
    - npm test
```

## Best Practices Summary

1. **Use DAG**: Define `needs` for parallel execution
2. **Cache Wisely**: Use file-based cache keys
3. **Fail Fast**: Use `interruptible: true`
4. **Resource Groups**: Prevent concurrent deployments
5. **Templates**: Use includes and extends
6. **Rules over Only/Except**: More flexible conditions
7. **Artifacts Expiration**: Set reasonable expiry
8. **Security Scanning**: Enable built-in scanners
9. **Environment Management**: Use review apps
10. **Monitor Performance**: Track pipeline metrics

## Resources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab CI/CD Examples](https://gitlab.com/gitlab-examples)
- [GitLab CI/CD Templates](https://gitlab.com/gitlab-org/gitlab-foss/tree/master/lib/gitlab/ci/templates)
- [GitLab Runner Documentation](https://docs.gitlab.com/runner/)
- [GitLab Auto DevOps](https://docs.gitlab.com/ee/topics/autodevops/)