---
title: Cloud Platforms Deep Dive
sidebar_position: 4
---

# Cloud Platforms Deep Dive for Platform Engineers

A comprehensive guide to AWS, GCP, and Azure from a platform engineering perspective, focusing on infrastructure automation, reliability, and scale.

## Cloud Platform Comparison

### Key Services Mapping

| Service Type | AWS | GCP | Azure |
|-------------|-----|-----|-------|
| Compute | EC2 | Compute Engine | Virtual Machines |
| Containers | ECS/EKS | GKE | AKS |
| Serverless | Lambda | Cloud Functions | Functions |
| Object Storage | S3 | Cloud Storage | Blob Storage |
| Block Storage | EBS | Persistent Disk | Managed Disks |
| Database (SQL) | RDS | Cloud SQL | SQL Database |
| NoSQL | DynamoDB | Firestore/Bigtable | Cosmos DB |
| Message Queue | SQS | Pub/Sub | Service Bus |
| CDN | CloudFront | Cloud CDN | CDN |
| Load Balancer | ELB/ALB/NLB | Cloud Load Balancing | Load Balancer |
| VPC | VPC | VPC | Virtual Network |
| IAM | IAM | Cloud IAM | Azure AD/RBAC |
| Monitoring | CloudWatch | Cloud Monitoring | Monitor |
| Logs | CloudWatch Logs | Cloud Logging | Log Analytics |

## AWS Deep Dive

### Compute and Networking

**EC2 Instance Optimization:**
```bash
# Instance metadata service v2 (IMDSv2)
aws ec2 modify-instance-metadata-options \
    --instance-id i-1234567890abcdef0 \
    --http-tokens required \
    --http-endpoint enabled

# Spot instance management
aws ec2 request-spot-fleet \
    --spot-fleet-request-config file://config.json
```

**VPC Design Patterns:**
```yaml
# Multi-AZ VPC with public/private subnets
Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
  
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
  
  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.11.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
```

**Advanced Networking:**
```bash
# Transit Gateway for multi-VPC
aws ec2 create-transit-gateway \
    --description "Central hub for VPC connectivity" \
    --options=AmazonSideAsn=64512,DefaultRouteTableAssociation=enable

# VPC Peering
aws ec2 create-vpc-peering-connection \
    --vpc-id vpc-1a2b3c4d \
    --peer-vpc-id vpc-5e6f7g8h \
    --peer-region us-west-2
```

**Resources:**
- 📖 [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- 📚 [AWS Certified Solutions Architect Study Guide](https://www.wiley.com/en-us/AWS+Certified+Solutions+Architect+Study+Guide%3A+Associate+SAA+C03+Exam%2C+4th+Edition-p-9781119982265)
- 🎥 [AWS re:Invent Videos](https://www.youtube.com/user/AmazonWebServices)
- 📖 [AWS Architecture Center](https://aws.amazon.com/architecture/)

### Container Services

**EKS Platform Engineering:**
```yaml
# EKS cluster with managed node groups
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: production-cluster
  region: us-west-2
  version: "1.27"

vpc:
  subnets:
    private:
      us-west-2a: { id: subnet-1 }
      us-west-2b: { id: subnet-2 }
      us-west-2c: { id: subnet-3 }

managedNodeGroups:
  - name: general-workloads
    instanceType: m5.large
    minSize: 3
    maxSize: 10
    desiredCapacity: 5
    volumeSize: 100
    volumeType: gp3
    privateNetworking: true
    iam:
      withAddonPolicies:
        imageBuilder: true
        autoScaler: true
        ebs: true
        efs: true
        cloudWatch: true
```

**ECS Service Mesh:**
```json
{
  "family": "service-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "proxyConfiguration": {
    "type": "APPMESH",
    "containerName": "envoy",
    "properties": [
      {"name": "ProxyIngressPort", "value": "15000"},
      {"name": "ProxyEgressPort", "value": "15001"},
      {"name": "AppPorts", "value": "8080"},
      {"name": "EgressIgnoredIPs", "value": "169.254.170.2,169.254.169.254"}
    ]
  }
}
```

### Serverless Platform

**Lambda Best Practices:**
```python
# Lambda with connection pooling
import boto3
from botocore.config import Config

# Initialize outside handler for connection reuse
config = Config(
    region_name='us-west-2',
    retries={'max_attempts': 2}
)
dynamodb = boto3.resource('dynamodb', config=config)
table = dynamodb.Table('my-table')

def lambda_handler(event, context):
    # Reuse connection
    response = table.get_item(
        Key={'id': event['id']}
    )
    return response['Item']
```

**Step Functions for Orchestration:**
```json
{
  "Comment": "ETL Pipeline State Machine",
  "StartAt": "ExtractData",
  "States": {
    "ExtractData": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:extract-data",
      "Next": "TransformData",
      "Retry": [{
        "ErrorEquals": ["States.TaskFailed"],
        "IntervalSeconds": 2,
        "MaxAttempts": 3,
        "BackoffRate": 2
      }]
    },
    "TransformData": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "TransformBatch1",
          "States": {
            "TransformBatch1": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:transform",
              "End": true
            }
          }
        }
      ],
      "Next": "LoadData"
    }
  }
}
```

### Storage and Databases

**S3 Lifecycle Management:**
```json
{
  "Rules": [{
    "Id": "ArchiveOldLogs",
    "Status": "Enabled",
    "Prefix": "logs/",
    "Transitions": [{
      "Days": 30,
      "StorageClass": "STANDARD_IA"
    }, {
      "Days": 90,
      "StorageClass": "GLACIER"
    }],
    "Expiration": {
      "Days": 365
    }
  }]
}
```

**DynamoDB Design Patterns:**
```python
# Single table design
table_design = {
    "TableName": "platform-table",
    "KeySchema": [
        {"AttributeName": "PK", "KeyType": "HASH"},
        {"AttributeName": "SK", "KeyType": "RANGE"}
    ],
    "GlobalSecondaryIndexes": [{
        "IndexName": "GSI1",
        "Keys": [
            {"AttributeName": "GSI1PK", "KeyType": "HASH"},
            {"AttributeName": "GSI1SK", "KeyType": "RANGE"}
        ],
        "Projection": {"ProjectionType": "ALL"}
    }],
    "BillingMode": "PAY_PER_REQUEST"
}
```

### Security and Compliance

**IAM Best Practices:**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "AWS": "arn:aws:iam::ACCOUNT:role/platform-engineer"
    },
    "Action": "sts:AssumeRole",
    "Condition": {
      "StringEquals": {
        "sts:ExternalId": "unique-external-id"
      },
      "IpAddress": {
        "aws:SourceIp": ["10.0.0.0/8"]
      }
    }
  }]
}
```

**Resources:**
- 📖 [AWS Security Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- 🎥 [AWS Security Hub](https://www.youtube.com/watch?v=HsWtPG_rTak)
- 📚 [AWS Security Cookbook](https://www.packtpub.com/product/aws-security-cookbook/9781838826253)

## GCP Deep Dive

### Compute and Networking

**Compute Engine Automation:**
```bash
# Create instance template with startup script
gcloud compute instance-templates create platform-template \
    --machine-type=n2-standard-4 \
    --network-interface=network=default,network-tier=PREMIUM \
    --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install -y monitoring-agent
    ' \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --scopes=https://www.googleapis.com/auth/cloud-platform

# Managed instance group with autoscaling
gcloud compute instance-groups managed create platform-mig \
    --template=platform-template \
    --size=3 \
    --zones=us-central1-a,us-central1-b,us-central1-c
```

**VPC Design:**
```yaml
# Shared VPC configuration
resources:
- name: host-vpc
  type: compute.v1.network
  properties:
    autoCreateSubnetworks: false
    
- name: prod-subnet
  type: compute.v1.subnetwork
  properties:
    network: $(ref.host-vpc.selfLink)
    ipCidrRange: 10.0.1.0/24
    region: us-central1
    privateIpGoogleAccess: true
    secondaryIpRanges:
    - rangeName: pods
      ipCidrRange: 10.1.0.0/16
    - rangeName: services
      ipCidrRange: 10.2.0.0/16
```

**Global Load Balancing:**
```bash
# Cloud CDN with Cloud Armor
gcloud compute backend-services create web-backend \
    --protocol=HTTP \
    --port-name=http \
    --health-checks=http-health-check \
    --global \
    --enable-cdn \
    --cache-mode=CACHE_ALL_STATIC

gcloud compute security-policies create block-bad-actors \
    --description "Block known malicious IPs"

gcloud compute security-policies rules create 1000 \
    --security-policy block-bad-actors \
    --expression "origin.region_code == 'XX'" \
    --action "deny-403"
```

**Resources:**
- 📖 [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- 📚 [Google Cloud Certified Professional Cloud Architect](https://www.wiley.com/en-us/Official+Google+Cloud+Certified+Professional+Cloud+Architect+Study+Guide%2C+2nd+Edition-p-9781119871057)
- 🎥 [Google Cloud Next Videos](https://www.youtube.com/googlecloudplatform)
- 📖 [GCP Best Practices](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations)

### GKE Platform Engineering

**GKE Autopilot:**
```yaml
# Optimized GKE cluster
apiVersion: container.cnrm.cloud.google.com/v1beta1
kind: ContainerCluster
metadata:
  name: platform-cluster
spec:
  location: us-central1
  autopilot:
    enabled: true
  releaseChannel:
    channel: REGULAR
  workloadIdentityConfig:
    workloadPool: PROJECT_ID.svc.id.goog
  addonsConfig:
    httpLoadBalancing:
      disabled: false
    horizontalPodAutoscaling:
      disabled: false
```

**Workload Identity:**
```bash
# Configure workload identity
kubectl create serviceaccount gcs-access \
    --namespace production

gcloud iam service-accounts create gcs-access-sa \
    --display-name "GCS Access Service Account"

gcloud iam service-accounts add-iam-policy-binding \
    gcs-access-sa@PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:PROJECT_ID.svc.id.goog[production/gcs-access]"

kubectl annotate serviceaccount gcs-access \
    --namespace production \
    iam.gke.io/gcp-service-account=gcs-access-sa@PROJECT_ID.iam.gserviceaccount.com
```

### Data Platform

**BigQuery for Analytics:**
```sql
-- Partitioned table with clustering
CREATE TABLE platform.events
PARTITION BY DATE(timestamp)
CLUSTER BY user_id, event_type
AS
SELECT * FROM platform.raw_events;

-- Materialized view for real-time dashboards
CREATE MATERIALIZED VIEW platform.hourly_metrics
PARTITION BY DATE(hour)
CLUSTER BY service_name
AS
SELECT
  TIMESTAMP_TRUNC(timestamp, HOUR) as hour,
  service_name,
  COUNT(*) as request_count,
  APPROX_QUANTILES(latency_ms, 100)[OFFSET(95)] as p95_latency
FROM platform.events
WHERE timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY hour, service_name;
```

**Dataflow Streaming:**
```java
// Streaming pipeline with windowing
Pipeline pipeline = Pipeline.create(options);

pipeline
    .apply("ReadFromPubSub", 
        PubsubIO.readMessages().fromSubscription(subscription))
    .apply("ParseEvents", 
        ParDo.of(new ParseEventFn()))
    .apply("WindowEvents", 
        Window.<Event>into(
            FixedWindows.of(Duration.standardMinutes(5)))
            .triggering(
                AfterWatermark.pastEndOfWindow()
                    .withEarlyFirings(
                        AfterProcessingTime.pastFirstElementInPane()
                            .plusDelayOf(Duration.standardSeconds(30))))
            .withAllowedLateness(Duration.standardMinutes(2))
            .discardingFiredPanes())
    .apply("AggregateMetrics", 
        Combine.perKey(new MetricsAggregator()))
    .apply("WriteToBigQuery", 
        BigQueryIO.writeTableRows()
            .to(table)
            .withCreateDisposition(CreateDisposition.CREATE_IF_NEEDED)
            .withWriteDisposition(WriteDisposition.WRITE_APPEND));
```

## Azure Deep Dive

### Compute and Networking

**Virtual Machine Scale Sets:**
```json
{
  "type": "Microsoft.Compute/virtualMachineScaleSets",
  "apiVersion": "2021-04-01",
  "name": "platform-vmss",
  "location": "[resourceGroup().location]",
  "sku": {
    "name": "Standard_D4s_v3",
    "capacity": 3
  },
  "properties": {
    "overprovision": true,
    "upgradePolicy": {
      "mode": "Rolling",
      "rollingUpgradePolicy": {
        "maxBatchInstancePercent": 20,
        "maxUnhealthyInstancePercent": 20,
        "maxUnhealthyUpgradedInstancePercent": 5,
        "pauseTimeBetweenBatches": "PT10S"
      }
    },
    "virtualMachineProfile": {
      "storageProfile": {
        "imageReference": {
          "publisher": "Canonical",
          "offer": "UbuntuServer",
          "sku": "18.04-LTS",
          "version": "latest"
        }
      },
      "osProfile": {
        "computerNamePrefix": "platform",
        "adminUsername": "azureuser",
        "customData": "[base64(variables('cloudInit'))]"
      },
      "networkProfile": {
        "networkInterfaceConfigurations": [{
          "name": "nic",
          "properties": {
            "primary": true,
            "ipConfigurations": [{
              "name": "ipconfig",
              "properties": {
                "subnet": {
                  "id": "[resourceId('Microsoft.Network/virtualNetworks/subnets', 'vnet', 'subnet')]"
                },
                "loadBalancerBackendAddressPools": [{
                  "id": "[resourceId('Microsoft.Network/loadBalancers/backendAddressPools', 'lb', 'backend')]"
                }]
              }
            }]
          }
        }]
      }
    }
  }
}
```

**Virtual Network Architecture:**
```bicep
// Hub-spoke network topology
resource hubVnet 'Microsoft.Network/virtualNetworks@2021-02-01' = {
  name: 'hub-vnet'
  location: resourceGroup().location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'GatewaySubnet'
        properties: {
          addressPrefix: '10.0.0.0/27'
        }
      }
      {
        name: 'AzureFirewallSubnet'
        properties: {
          addressPrefix: '10.0.1.0/26'
        }
      }
    ]
  }
}

resource spokeVnet 'Microsoft.Network/virtualNetworks@2021-02-01' = {
  name: 'spoke-vnet'
  location: resourceGroup().location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.1.0.0/16'
      ]
    }
  }
}

resource vnetPeering 'Microsoft.Network/virtualNetworks/virtualNetworkPeerings@2021-02-01' = {
  parent: hubVnet
  name: 'hub-to-spoke'
  properties: {
    remoteVirtualNetwork: {
      id: spokeVnet.id
    }
    allowVirtualNetworkAccess: true
    allowForwardedTraffic: true
    allowGatewayTransit: true
  }
}
```

**Resources:**
- 📖 [Azure Architecture Center](https://docs.microsoft.com/en-us/azure/architecture/)
- 📚 [Azure Solutions Architect Expert Guide](https://www.packtpub.com/product/microsoft-azure-architect-technologies-and-design-complete-study-guide/9781838988180)
- 🎥 [Azure Friday](https://azure.microsoft.com/en-us/resources/videos/azure-friday/)
- 📖 [Azure Well-Architected Framework](https://docs.microsoft.com/en-us/azure/architecture/framework/)

### AKS Platform Engineering

**AKS with Azure Arc:**
```bash
# Create AKS cluster with advanced networking
az aks create \
    --resource-group platform-rg \
    --name platform-aks \
    --node-count 3 \
    --enable-managed-identity \
    --network-plugin azure \
    --network-policy calico \
    --enable-addons monitoring,azure-policy \
    --generate-ssh-keys \
    --attach-acr platform-acr \
    --enable-cluster-autoscaler \
    --min-count 3 \
    --max-count 10

# Enable GitOps
az k8s-configuration flux create \
    --name platform-gitops \
    --cluster-name platform-aks \
    --resource-group platform-rg \
    --namespace flux-system \
    --cluster-type managedClusters \
    --scope cluster \
    --url https://github.com/company/k8s-config \
    --branch main \
    --kustomization name=infra path=./infrastructure prune=true \
    --kustomization name=apps path=./apps/production prune=true dependsOn=infra
```

### Azure DevOps and Automation

**Azure DevOps Pipelines:**
```yaml
# Multi-stage pipeline with approval gates
trigger:
  branches:
    include:
    - main

stages:
- stage: Build
  jobs:
  - job: BuildContainer
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: Docker@2
      inputs:
        containerRegistry: 'platform-acr'
        repository: 'platform/app'
        command: 'buildAndPush'
        Dockerfile: '**/Dockerfile'
        tags: |
          $(Build.BuildId)
          latest

- stage: DeployDev
  dependsOn: Build
  jobs:
  - deployment: DeployToDev
    pool:
      vmImage: 'ubuntu-latest'
    environment: 'development'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: KubernetesManifest@0
            inputs:
              action: 'deploy'
              kubernetesServiceConnection: 'dev-aks'
              manifests: |
                manifests/deployment.yaml
                manifests/service.yaml
              containers: |
                platform-acr.azurecr.io/platform/app:$(Build.BuildId)

- stage: DeployProd
  dependsOn: DeployDev
  jobs:
  - deployment: DeployToProd
    pool:
      vmImage: 'ubuntu-latest'
    environment: 'production'
    strategy:
      runOnce:
        preDeploy:
          steps:
          - task: ManualValidation@0
            timeoutInMinutes: 1440
            inputs:
              notifyUsers: 'platform-team@company.com'
              instructions: 'Validate dev deployment before promoting to production'
        deploy:
          steps:
          - task: KubernetesManifest@0
            inputs:
              action: 'deploy'
              kubernetesServiceConnection: 'prod-aks'
              manifests: |
                manifests/deployment.yaml
                manifests/service.yaml
              containers: |
                platform-acr.azurecr.io/platform/app:$(Build.BuildId)
```

## Multi-Cloud Strategies

### Cloud-Agnostic Architecture

**Terraform Multi-Cloud Module:**
```hcl
# Main module supporting multiple providers
variable "cloud_provider" {
  type = string
  validation {
    condition = contains(["aws", "gcp", "azure"], var.cloud_provider)
    error_message = "Cloud provider must be aws, gcp, or azure."
  }
}

module "compute" {
  source = "./modules/${var.cloud_provider}/compute"
  
  instance_count = var.instance_count
  instance_type  = local.instance_types[var.cloud_provider]
  network_id     = module.network.network_id
}

locals {
  instance_types = {
    aws   = "m5.large"
    gcp   = "n2-standard-4"
    azure = "Standard_D4s_v3"
  }
}
```

### Cost Optimization Across Clouds

**Cost Monitoring and Optimization:**
```python
# Multi-cloud cost analyzer
import boto3
from google.cloud import billing_v1
from azure.mgmt.consumption import ConsumptionManagementClient

class MultiCloudCostAnalyzer:
    def get_aws_costs(self, start_date, end_date):
        ce_client = boto3.client('ce')
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ]
        )
        return response['ResultsByTime']
    
    def get_gcp_costs(self, billing_account):
        client = billing_v1.CloudBillingClient()
        # Implementation for GCP billing API
        pass
    
    def get_azure_costs(self, subscription_id):
        consumption_client = ConsumptionManagementClient(
            credential, subscription_id
        )
        # Implementation for Azure consumption API
        pass
```

## Platform Engineering Interview Scenarios

### Common Cloud Platform Questions

1. **Design a multi-region deployment**
   - Active-active vs active-passive
   - Data replication strategies
   - Failover mechanisms

2. **Implement disaster recovery**
   - RTO and RPO requirements
   - Backup strategies
   - Cross-region replication

3. **Optimize cloud costs**
   - Reserved instances vs spot/preemptible
   - Auto-scaling strategies
   - Storage tiering

4. **Secure cloud infrastructure**
   - Network segmentation
   - Identity and access management
   - Encryption at rest and in transit

5. **Build CI/CD pipelines**
   - Multi-cloud deployment
   - Blue-green deployments
   - Canary releases

### Hands-On Labs

**AWS:**
- 🎮 [AWS Workshops](https://workshops.aws/)
- 🎮 [AWS Hands-On Labs](https://aws.amazon.com/training/hands-on/)

**GCP:**
- 🎮 [Google Cloud Skills Boost](https://www.cloudskillsboost.google/)
- 🎮 [GCP Codelabs](https://codelabs.developers.google.com/cloud)

**Azure:**
- 🎮 [Microsoft Learn](https://docs.microsoft.com/en-us/learn/)
- 🎮 [Azure Labs](https://github.com/MicrosoftLearning)

## Certifications and Learning Paths

### AWS Certifications
- 🎓 [AWS Solutions Architect Associate](https://aws.amazon.com/certification/certified-solutions-architect-associate/)
- 🎓 [AWS DevOps Engineer Professional](https://aws.amazon.com/certification/certified-devops-engineer-professional/)
- 🎓 [AWS Advanced Networking Specialty](https://aws.amazon.com/certification/certified-advanced-networking-specialty/)

### GCP Certifications
- 🎓 [Google Cloud Professional Cloud Architect](https://cloud.google.com/certification/cloud-architect)
- 🎓 [Google Cloud Professional DevOps Engineer](https://cloud.google.com/certification/cloud-devops-engineer)
- 🎓 [Google Cloud Professional Cloud Network Engineer](https://cloud.google.com/certification/cloud-network-engineer)

### Azure Certifications
- 🎓 [Azure Solutions Architect Expert](https://docs.microsoft.com/en-us/certifications/azure-solutions-architect/)
- 🎓 [Azure DevOps Engineer Expert](https://docs.microsoft.com/en-us/certifications/azure-devops/)
- 🎓 [Azure Network Engineer Associate](https://docs.microsoft.com/en-us/certifications/azure-network-engineer-associate/)

## Key Takeaways

1. **Know the equivalents**: Understand how services map across clouds
2. **Focus on patterns**: Architectural patterns apply across all platforms
3. **Automation first**: Use IaC and APIs for everything
4. **Cost awareness**: Understand pricing models and optimization strategies
5. **Security by design**: Implement security at every layer
6. **Stay current**: Cloud services evolve rapidly - keep learning

Remember: Platform engineering in the cloud is about building reliable, scalable, and cost-effective infrastructure that empowers development teams to deliver value quickly and safely.