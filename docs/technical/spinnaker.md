# Spinnaker - Multi-Cloud Continuous Delivery Platform

## Overview

Spinnaker is an open-source, multi-cloud continuous delivery platform for releasing software changes with high velocity and confidence. Originally developed at Netflix, it supports deployment to multiple cloud providers and integrates with various CI systems.

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                       Spinnaker Architecture                     │
├─────────────────────────┬───────────────────────────────────────┤
│         Deck            │              Gate                     │
│   • Web UI             │   • REST API Gateway                 │
│   • Pipeline viz       │   • Authentication                  │
│   • Infrastructure     │   • Authorization                   │
│     management         │   • API aggregation                 │
├─────────────────────────┼───────────────────────────────────────┤
│         Orca            │            Clouddriver               │
│   • Orchestration      │   • Cloud provider integration      │
│   • Pipeline exec      │   • Account management              │
│   • Stage management   │   • Resource deployment             │
│   • Task coordination  │   • Caching layer                   │
├─────────────────────────┼───────────────────────────────────────┤
│         Echo            │              Front50                 │
│   • Event processing   │   • Metadata persistence            │
│   • Notifications      │   • Pipeline storage                │
│   • Webhook triggers   │   • Application config              │
│   • Scheduled triggers │   • Notification preferences        │
├─────────────────────────┼───────────────────────────────────────┤
│      Rosco              │              Igor                    │
│   • Image baking       │   • CI integration                  │
│   • Packer wrapper     │   • SCM polling                     │
│   • AMI/Image creation │   • Build artifact tracking         │
│                        │   • Docker registry monitoring      │
├─────────────────────────┼───────────────────────────────────────┤
│       Kayenta           │              Fiat                    │
│   • Automated Canary   │   • Authorization service           │
│     Analysis           │   • RBAC enforcement                │
│   • Metric comparison  │   • Permission synchronization      │
│   • Judge service      │   • Service accounts                │
└─────────────────────────┴───────────────────────────────────────┘
                                    │
                                    ▼
            ┌─────────────────────────────────────────┐
            │          Cloud Providers                │
            │  AWS | GCP | Azure | Kubernetes | CF   │
            └─────────────────────────────────────────┘
```

### Data Flow

```
User → Deck → Gate → Orca → Clouddriver → Cloud Provider
                       ↓
                    Echo → Notifications/Webhooks
                       ↓
                   Front50 → Persistent Storage
```

## Installation

### Prerequisites

```bash
# Kubernetes cluster (1.20+) with adequate resources
# - 8+ cores
# - 32GB+ RAM
# - 100GB+ storage

# Halyard (Spinnaker's configuration tool)
curl -O https://raw.githubusercontent.com/spinnaker/halyard/master/install/debian/InstallHalyard.sh
sudo bash InstallHalyard.sh

# Verify Halyard installation
hal -v
```

### Kubernetes Installation with Halyard

```bash
# Set up Kubernetes provider
kubectl config use-context <your-cluster>

# Configure Spinnaker version
hal config version edit --version 1.30.0

# Configure storage (S3 example)
hal config storage s3 edit \
  --access-key-id $AWS_ACCESS_KEY_ID \
  --secret-access-key \
  --region us-east-1 \
  --bucket spinnaker-artifacts

hal config storage edit --type s3

# Configure Kubernetes account
hal config provider kubernetes account add my-k8s-account \
  --provider-version v2 \
  --context $(kubectl config current-context)

hal config features edit --artifacts true

# Configure deployment type
hal config deploy edit --type distributed --account-name my-k8s-account

# Deploy Spinnaker
hal deploy apply

# Expose Spinnaker UI
kubectl -n spinnaker port-forward service/spin-deck 9000:9000
kubectl -n spinnaker port-forward service/spin-gate 8084:8084
```

### Operator-based Installation

```yaml
# spinnaker-operator/operator.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: spinnaker-operator
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spinnaker-operator
  namespace: spinnaker-operator
spec:
  replicas: 1
  selector:
    matchLabels:
      name: spinnaker-operator
  template:
    metadata:
      labels:
        name: spinnaker-operator
    spec:
      serviceAccountName: spinnaker-operator
      containers:
      - name: spinnaker-operator
        image: armory/halyard:operator-latest
        command:
        - /opt/spinnaker/operator/bin/manager
        imagePullPolicy: Always
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: OPERATOR_NAME
          value: "spinnaker-operator"
```

## Configuration Examples

### SpinnakerService Configuration

```yaml
# spinnakerservice.yaml
apiVersion: spinnaker.io/v1alpha2
kind: SpinnakerService
metadata:
  name: spinnaker
  namespace: spinnaker
spec:
  spinnakerConfig:
    config:
      version: 1.30.0
      persistentStorage:
        persistentStoreType: s3
        s3:
          bucket: my-spinnaker-bucket
          rootFolder: front50
          region: us-east-1
          accessKeyId: encrypted:k8s!n:spin-secrets!k:aws-access-key-id
          secretAccessKey: encrypted:k8s!n:spin-secrets!k:aws-secret-access-key
      
      features:
        artifacts: true
        pipelineTemplates: true
        managedPipelineTemplatesV2UI: true
        gremlin: true
      
      metricStores:
        prometheus:
          enabled: true
          add_source_metalabels: true
        
      canary:
        enabled: true
        serviceIntegrations:
        - name: prometheus
          enabled: true
          accounts:
          - name: prometheus-account
            endpoint:
              baseUrl: http://prometheus:9090
        - name: aws
          enabled: true
          accounts:
          - name: cloudwatch-account
            bucket: kayenta-bucket
            region: us-east-1
      
      notifications:
        slack:
          enabled: true
          token: encrypted:k8s!n:spin-secrets!k:slack-token
      
    profiles:
      clouddriver:
        kubernetes:
          accounts:
          - name: prod-k8s
            requiredGroupMembership: []
            providerVersion: V2
            permissions:
              READ:
              - engineering
              WRITE:
              - engineering
            dockerRegistries:
            - accountName: dockerhub
            - accountName: gcr
            configureImagePullSecrets: true
            cacheThreads: 1
            namespaces:
            - production
            - staging
            kubeconfigFile: encrypted:k8s!n:kubeconfigs!k:prod
            
          - name: dev-k8s
            requiredGroupMembership: []
            providerVersion: V2
            dockerRegistries:
            - accountName: dockerhub
            configureImagePullSecrets: true
            namespaces:
            - development
            kubeconfigFile: encrypted:k8s!n:kubeconfigs!k:dev
        
        dockerRegistry:
          accounts:
          - name: dockerhub
            address: index.docker.io
            repositories:
            - myorg/webapp
            - myorg/api
          - name: gcr
            address: gcr.io
            username: _json_key
            password: encrypted:k8s!n:gcr-secrets!k:key.json
      
      gate:
        security:
          oauth2:
            enabled: true
            provider: GOOGLE
            clientId: encrypted:k8s!n:oauth-secrets!k:client-id
            clientSecret: encrypted:k8s!n:oauth-secrets!k:client-secret
            userInfoRequirements:
              email: ".*@mycompany.com"
      
      echo:
        scheduler:
          enabled: true
        
  expose:
    type: service
    service:
      type: LoadBalancer
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
  
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "1000m"
```

### Pipeline Template

```json
{
  "schema": "v2",
  "variables": [
    {
      "type": "string",
      "defaultValue": "myapp",
      "description": "Application name",
      "name": "application"
    },
    {
      "type": "string", 
      "defaultValue": "main",
      "description": "Git branch",
      "name": "branch"
    }
  ],
  "id": "deployTemplate",
  "metadata": {
    "name": "Kubernetes Deployment Template",
    "description": "Standard deployment pipeline with canary",
    "owner": "platform-team"
  },
  "protect": false,
  "stages": [
    {
      "account": "jenkins",
      "job": "Build-${templateVariables.application}",
      "master": "jenkins-master",
      "name": "Build",
      "parameters": {
        "BRANCH": "${templateVariables.branch}"
      },
      "propertyFile": "build.properties",
      "type": "jenkins"
    },
    {
      "account": "prod-k8s",
      "cloudProvider": "kubernetes",
      "manifests": [
        {
          "apiVersion": "apps/v1",
          "kind": "Deployment",
          "metadata": {
            "name": "${templateVariables.application}-canary",
            "labels": {
              "app": "${templateVariables.application}",
              "version": "canary"
            }
          },
          "spec": {
            "replicas": 1,
            "selector": {
              "matchLabels": {
                "app": "${templateVariables.application}",
                "version": "canary"
              }
            },
            "template": {
              "metadata": {
                "labels": {
                  "app": "${templateVariables.application}",
                  "version": "canary"
                }
              },
              "spec": {
                "containers": [
                  {
                    "name": "${templateVariables.application}",
                    "image": "myorg/${templateVariables.application}:${trigger.properties.BUILD_NUMBER}",
                    "ports": [
                      {
                        "containerPort": 8080
                      }
                    ]
                  }
                ]
              }
            }
          }
        }
      ],
      "moniker": {
        "app": "${templateVariables.application}"
      },
      "name": "Deploy Canary",
      "namespaceOverride": "production",
      "type": "deployManifest"
    },
    {
      "analysisType": "realTime",
      "canaryConfig": {
        "beginCanaryAnalysisAfterMins": "5",
        "canaryAnalysisIntervalMins": "30",
        "canaryConfigId": "standard-canary-config",
        "lifetimeDuration": "PT1H",
        "metricsAccountName": "prometheus-account",
        "scopes": [
          {
            "extendedScopeParams": {},
            "scopeName": "default"
          }
        ],
        "scoreThresholds": {
          "marginal": "75",
          "pass": "90"
        },
        "storageAccountName": "s3-storage"
      },
      "name": "Canary Analysis",
      "type": "kayentaCanary"
    },
    {
      "account": "prod-k8s",
      "cloudProvider": "kubernetes",
      "manifestName": "deployment ${templateVariables.application}",
      "name": "Promote to Production",
      "namespaceOverride": "production",
      "options": {
        "mergeStrategy": "strategic",
        "record": true
      },
      "patchBody": [
        {
          "spec": {
            "template": {
              "spec": {
                "containers": [
                  {
                    "name": "${templateVariables.application}",
                    "image": "myorg/${templateVariables.application}:${trigger.properties.BUILD_NUMBER}"
                  }
                ]
              }
            }
          }
        }
      ],
      "source": "text",
      "type": "patchManifest"
    }
  ]
}
```

### Application Configuration

```json
{
  "name": "sample-app",
  "email": "platform-team@example.com",
  "description": "Sample microservice application",
  "cloudProviders": [
    "kubernetes"
  ],
  "trafficGuards": [],
  "instancePort": 8080,
  "permissions": {
    "READ": [
      "engineering",
      "qa"
    ],
    "WRITE": [
      "engineering"
    ]
  },
  "notifications": {
    "slack": [
      {
        "address": "spinnaker-notifications",
        "level": "pipeline",
        "type": "slack",
        "when": [
          "pipeline.starting",
          "pipeline.complete",
          "pipeline.failed"
        ]
      }
    ],
    "email": [
      {
        "address": "platform-team@example.com",
        "level": "application",
        "type": "email",
        "when": [
          "pipeline.failed"
        ]
      }
    ]
  }
}
```

## Production Patterns

### Multi-Region Deployment

```json
{
  "name": "Multi-Region Deployment",
  "stages": [
    {
      "name": "Deploy to US-East",
      "type": "deploy",
      "clusters": [
        {
          "account": "aws-prod",
          "region": "us-east-1",
          "strategy": "redblack",
          "targetHealthyDeployPercentage": 100,
          "details": "Deploy to primary region",
          "cloudProvider": "aws",
          "serverGroup": {
            "instanceType": "m5.large",
            "targetGroups": ["app-tg-us-east-1"],
            "securityGroups": ["app-sg"],
            "capacity": {
              "min": 3,
              "max": 10,
              "desired": 3
            },
            "availabilityZones": {
              "us-east-1": ["us-east-1a", "us-east-1b", "us-east-1c"]
            }
          }
        }
      ]
    },
    {
      "name": "Wait for US-East Health",
      "type": "wait",
      "waitTime": 300
    },
    {
      "name": "Deploy to US-West",
      "type": "deploy",
      "clusters": [
        {
          "account": "aws-prod",
          "region": "us-west-2",
          "strategy": "redblack",
          "targetHealthyDeployPercentage": 100,
          "cloudProvider": "aws",
          "serverGroup": {
            "instanceType": "m5.large",
            "targetGroups": ["app-tg-us-west-2"],
            "securityGroups": ["app-sg"],
            "capacity": {
              "min": 3,
              "max": 10,
              "desired": 3
            }
          }
        }
      ]
    },
    {
      "name": "Deploy to EU",
      "type": "deploy",
      "stageEnabled": {
        "expression": "${#stage('Deploy to US-West')['status'] == 'SUCCEEDED'}",
        "type": "expression"
      },
      "clusters": [
        {
          "account": "aws-prod",
          "region": "eu-west-1",
          "strategy": "redblack",
          "cloudProvider": "aws"
        }
      ]
    }
  ]
}
```

### Blue-Green Deployment with Validation

```json
{
  "name": "Blue-Green Deployment",
  "stages": [
    {
      "name": "Deploy Green",
      "type": "deploy",
      "clusters": [{
        "account": "kubernetes-prod",
        "application": "myapp",
        "cloudProvider": "kubernetes",
        "containers": [{
          "args": [],
          "command": [],
          "imageDescription": {
            "account": "dockerhub",
            "fromTrigger": true,
            "organization": "myorg",
            "registry": "index.docker.io",
            "repository": "myorg/myapp",
            "tag": "^.*"
          },
          "name": "myapp",
          "ports": [{
            "containerPort": 8080,
            "name": "http",
            "protocol": "TCP"
          }]
        }],
        "deployment": {
          "enabled": true,
          "minReadySeconds": 0,
          "paused": false,
          "progressRollbackSeconds": 0,
          "revisionHistoryLimit": 2,
          "rollbackRevision": 0
        },
        "namespace": "production",
        "replicaSet": {
          "annotations": {
            "deployment": "green"
          }
        },
        "strategy": "none",
        "targetSize": 3,
        "terminationGracePeriodSeconds": 30
      }]
    },
    {
      "name": "Run Integration Tests",
      "type": "jenkins",
      "master": "jenkins-master",
      "job": "integration-tests",
      "parameters": {
        "ENDPOINT": "http://myapp-green.production.svc.cluster.local",
        "ENVIRONMENT": "production"
      }
    },
    {
      "name": "Manual Validation",
      "type": "manualJudgment",
      "judgmentInputs": [
        {
          "value": "Continue with deployment"
        },
        {
          "value": "Rollback"
        }
      ],
      "notifications": [{
        "address": "platform-approvers",
        "level": "stage",
        "type": "slack",
        "when": ["manualJudgment"]
      }]
    },
    {
      "name": "Switch Traffic to Green",
      "type": "deployManifest",
      "account": "kubernetes-prod",
      "cloudProvider": "kubernetes",
      "manifests": [{
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
          "name": "myapp",
          "namespace": "production"
        },
        "spec": {
          "selector": {
            "app": "myapp",
            "deployment": "green"
          },
          "ports": [{
            "port": 80,
            "targetPort": 8080
          }]
        }
      }],
      "moniker": {
        "app": "myapp"
      },
      "skipExpressionEvaluation": false,
      "source": "text"
    },
    {
      "name": "Disable Blue",
      "type": "disableCluster",
      "cluster": "myapp-blue",
      "cloudProvider": "kubernetes",
      "credentials": "kubernetes-prod",
      "moniker": {
        "app": "myapp"
      },
      "namespace": "production",
      "remainingEnabledServerGroups": 1
    }
  ]
}
```

### Automated Canary Analysis

```yaml
# canary-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: standard-canary-config
  namespace: spinnaker
data:
  canary.json: |
    {
      "name": "standard-canary-config",
      "description": "Standard canary analysis configuration",
      "configVersion": "1.0",
      "applications": ["myapp"],
      "judge": {
        "name": "NetflixACAJudge-v1.0",
        "judgeConfigurations": {}
      },
      "metrics": [
        {
          "name": "Request Rate",
          "query": {
            "type": "prometheus",
            "serviceType": "prometheus",
            "metricName": "request_rate",
            "queryTemplate": "sum(rate(http_requests_total{job=\"${scope}\",status=~\"2..\"}[5m]))"
          },
          "groups": ["Group 1"],
          "analysisConfigurations": {
            "canary": {
              "direction": "increase",
              "nanStrategy": "replace"
            }
          },
          "scopeName": "default"
        },
        {
          "name": "Error Rate",
          "query": {
            "type": "prometheus",
            "metricName": "error_rate",
            "queryTemplate": "sum(rate(http_requests_total{job=\"${scope}\",status=~\"5..\"}[5m])) / sum(rate(http_requests_total{job=\"${scope}\"}[5m]))"
          },
          "groups": ["Group 1"],
          "analysisConfigurations": {
            "canary": {
              "direction": "decrease",
              "critical": true,
              "mustHaveData": true,
              "nanStrategy": "remove"
            }
          }
        },
        {
          "name": "Latency P95",
          "query": {
            "type": "prometheus",
            "metricName": "latency_p95",
            "queryTemplate": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job=\"${scope}\"}[5m])) by (le))"
          },
          "groups": ["Group 2"],
          "analysisConfigurations": {
            "canary": {
              "direction": "decrease"
            }
          }
        }
      ],
      "classifier": {
        "groupWeights": {
          "Group 1": 60,
          "Group 2": 40
        }
      },
      "templates": {}
    }
```

### Pipeline Expressions

```json
{
  "name": "Advanced Pipeline",
  "stages": [
    {
      "name": "Evaluate Deployment",
      "type": "evaluateVariables",
      "variables": [
        {
          "key": "deploymentRegions",
          "value": "${parameters.regions.split(',')}"
        },
        {
          "key": "isProduction",
          "value": "${parameters.environment == 'production'}"
        },
        {
          "key": "deploymentStrategy",
          "value": "${isProduction ? 'redblack' : 'highlander'}"
        }
      ]
    },
    {
      "name": "Check Prerequisites",
      "type": "checkPreconditions",
      "preconditions": [
        {
          "context": {
            "expression": "${#stage('Build')['outputs']['buildNumber'] != null}"
          },
          "failPipeline": true,
          "type": "expression"
        },
        {
          "context": {
            "stageName": "Security Scan",
            "stageStatus": "SUCCEEDED"
          },
          "failPipeline": true,
          "type": "stageStatus"
        }
      ]
    },
    {
      "name": "Dynamic Deployment",
      "type": "deploy",
      "clusters": [
        {
          "account": "kubernetes-${parameters.environment}",
          "application": "${application}",
          "strategy": "${deploymentStrategy}",
          "targetHealthyDeployPercentage": "${isProduction ? 100 : 95}",
          "capacity": {
            "min": "${isProduction ? 3 : 1}",
            "max": "${isProduction ? 10 : 3}",
            "desired": "${isProduction ? 3 : 1}"
          }
        }
      ],
      "restrictExecutionDuringTimeWindow": "${isProduction}",
      "restrictedExecutionWindow": {
        "whitelist": [
          {
            "startTime": 14,
            "endTime": 18,
            "days": [2, 3, 4, 5]
          }
        ]
      }
    }
  ],
  "parameterConfig": [
    {
      "name": "environment",
      "label": "Environment",
      "required": true,
      "options": [
        {"value": "development"},
        {"value": "staging"},
        {"value": "production"}
      ]
    },
    {
      "name": "regions",
      "label": "Deployment Regions",
      "description": "Comma-separated list of regions",
      "default": "us-east-1,us-west-2"
    }
  ]
}
```

## Security Best Practices

### Authentication Configuration

```yaml
# oauth-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: halyard-config
  namespace: spinnaker
data:
  gate-local.yml: |
    security:
      authn:
        oauth2:
          enabled: true
          client:
            clientId: ${CLIENT_ID}
            clientSecret: ${CLIENT_SECRET}
            accessTokenUri: https://oauth.provider.com/token
            userAuthorizationUri: https://oauth.provider.com/authorize
            scope: openid email profile
          resource:
            userInfoUri: https://oauth.provider.com/userinfo
          userInfoMapping:
            email: email
            firstName: given_name
            lastName: family_name
            username: preferred_username
      authz:
        groupMembership:
          service: EXTERNAL
          external:
            url: https://authz.provider.com/groups
            httpMethod: GET
            headers:
              Authorization: Bearer ${AUTH_TOKEN}
        enabled: true
```

### RBAC Configuration

```yaml
# fiat-local.yml
auth:
  groupMembership:
    service: EXTERNAL
  permissions:
    provider: AGGREGATE
    source:
      application:
        enabled: true
      google_groups:
        enabled: false
      github_teams:
        enabled: true
        organization: myorg
        baseUrl: https://api.github.com
        accessToken: ${GITHUB_TOKEN}
  enabled: true
  
server:
  session:
    timeoutInSeconds: 3600
    
spring:
  redis:
    connection: redis://redis:6379
```

### Network Security

```yaml
# network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: spinnaker-internal
  namespace: spinnaker
spec:
  podSelector:
    matchLabels:
      app: spinnaker
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: spinnaker
    - podSelector:
        matchLabels:
          app: spinnaker
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
      podSelector:
        matchLabels:
          app.kubernetes.io/name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8084  # Gate API
  egress:
  - to:
    - namespaceSelector: {}
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 169.254.169.254/32
```

## Monitoring and Observability

### Prometheus Integration

```yaml
# prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: spinnaker-monitoring
  namespace: spinnaker
data:
  spinnaker-monitoring.yml: |
    management:
      metrics:
        export:
          prometheus:
            enabled: true
    
    spectator:
      applicationName: ${spring.application.name}
      webEndpoint:
        enabled: true
      metrics:
        export:
          prometheus:
            enabled: true
            step: PT30S
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Spinnaker Operations",
    "panels": [
      {
        "title": "Pipeline Executions",
        "targets": [
          {
            "expr": "sum(rate(orca_pipeline_executions_total[5m])) by (status)"
          }
        ]
      },
      {
        "title": "Stage Duration",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(orca_stage_duration_seconds_bucket[5m])) by (stage_type, le))"
          }
        ]
      },
      {
        "title": "Clouddriver Cache Age",
        "targets": [
          {
            "expr": "clouddriver_cache_age_seconds{}"
          }
        ]
      },
      {
        "title": "Gate Request Rate",
        "targets": [
          {
            "expr": "sum(rate(gate_requests_total[5m])) by (status)"
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting

### Common Issues and Solutions

```bash
# Check Spinnaker services
kubectl get pods -n spinnaker
kubectl logs -n spinnaker deployment/spin-clouddriver

# Halyard troubleshooting
hal deploy connect
kubectl exec -it deployment/spin-halyard -n spinnaker -- hal deploy details

# Clear Clouddriver cache
kubectl exec -it deployment/spin-clouddriver -n spinnaker -- \
  curl -X POST http://localhost:7002/cache/evict/kubernetes

# Check Redis connectivity
kubectl exec -it deployment/spin-gate -n spinnaker -- \
  redis-cli -h spin-redis ping

# Debug pipeline execution
curl http://localhost:8084/applications/{app}/pipelines/{id}/executions/{executionId}

# Force refresh application
curl -X POST http://localhost:8084/applications/{app}/refresh
```

### Performance Tuning

```yaml
# clouddriver-local.yml
sql:
  enabled: true
  taskRepository:
    enabled: true
  cache:
    enabled: true
    readBatchSize: 500
    writeBatchSize: 500
  scheduler:
    enabled: true
  connectionPools:
    default:
      maxPoolSize: 20
      connectionTimeout: 5000
  migration:
    jdbcUrl: jdbc:mysql://mysql:3306/clouddriver
    user: clouddriver
    password: ${MYSQL_PASSWORD}

redis:
  enabled: false
  
kubernetes:
  cache:
    evictAfter: 300000  # 5 minutes
  caching:
    agent:
      intervalSeconds: 30
      maxThreads: 20
  
server:
  tomcat:
    max-threads: 200
    accept-count: 100
```

## Integration Examples

### Jenkins Integration

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
                sh 'docker build -t myapp:${BUILD_NUMBER} .'
                sh 'docker push myregistry/myapp:${BUILD_NUMBER}'
            }
        }
        
        stage('Trigger Spinnaker') {
            steps {
                script {
                    def payload = [
                        application: "myapp",
                        pipeline: "deploy-pipeline",
                        parameters: [
                            version: "${BUILD_NUMBER}",
                            branch: "${GIT_BRANCH}"
                        ]
                    ]
                    
                    httpRequest(
                        url: "http://spinnaker-gate:8084/pipelines/myapp/deploy-pipeline",
                        httpMode: 'POST',
                        contentType: 'APPLICATION_JSON',
                        requestBody: groovy.json.JsonOutput.toJson(payload),
                        authentication: 'spinnaker-webhook'
                    )
                }
            }
        }
    }
}
```

### Terraform Integration

```hcl
# spinnaker-app.tf
resource "spinnaker_application" "myapp" {
  name        = "myapp"
  email       = "platform@example.com"
  description = "My Application"
  
  cloud_providers = [
    "kubernetes",
    "aws"
  ]
  
  instance_port = 8080
}

resource "spinnaker_pipeline" "deploy" {
  application = spinnaker_application.myapp.name
  name        = "terraform-deploy"
  
  pipeline = jsonencode({
    keepWaitingPipelines = false
    limitConcurrent      = true
    
    stages = [
      {
        name = "Deploy from Terraform"
        type = "deploy"
        clusters = [{
          account = "kubernetes-prod"
          application = "myapp"
          cloudProvider = "kubernetes"
        }]
      }
    ]
  })
}
```