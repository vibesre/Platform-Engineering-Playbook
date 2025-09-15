---
title: Cloud Platforms
sidebar_position: 4
---

# Cloud Platforms for Platform Engineers

Master AWS, GCP, and Azure for platform engineering interviews.

## 🎯 Interview Focus Areas

### Most Asked Topics
1. **Compute Services** - EC2/GCE/VMs, autoscaling, instance types
2. **Networking** - VPC, subnets, load balancers, CDN
3. **Storage** - Object storage, block storage, databases
4. **IAM & Security** - Roles, policies, best practices
5. **Cost Optimization** - Reserved instances, spot, right-sizing

## Service Comparison

### Core Services Mapping

| Service Type | AWS | GCP | Azure |
|-------------|-----|-----|-------|
| **Compute** |
| Virtual Machines | EC2 | Compute Engine | Virtual Machines |
| Containers | ECS/EKS | GKE | AKS |
| Serverless | Lambda | Cloud Functions | Functions |
| Batch | Batch | Batch | Batch |
| **Storage** |
| Object Storage | S3 | Cloud Storage | Blob Storage |
| Block Storage | EBS | Persistent Disk | Managed Disks |
| File Storage | EFS | Filestore | Files |
| Archive | Glacier | Archive Storage | Archive Storage |
| **Database** |
| Relational | RDS | Cloud SQL | SQL Database |
| NoSQL | DynamoDB | Firestore/Bigtable | Cosmos DB |
| Cache | ElastiCache | Memorystore | Cache for Redis |
| **Networking** |
| Virtual Network | VPC | VPC | Virtual Network |
| Load Balancer | ELB/ALB/NLB | Load Balancing | Load Balancer |
| CDN | CloudFront | Cloud CDN | CDN |
| DNS | Route 53 | Cloud DNS | DNS |
| **Messaging** |
| Queue | SQS | Cloud Tasks | Service Bus |
| Pub/Sub | SNS | Pub/Sub | Event Grid |
| Stream | Kinesis | Dataflow | Event Hubs |

## AWS Deep Dive

### EC2 & Compute

```bash
# Launch instance with user data
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.medium \
  --key-name my-key \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678 \
  --user-data file://startup-script.sh \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=web-server}]'

# Auto Scaling Group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name my-asg \
  --launch-template LaunchTemplateName=my-template \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 3 \
  --vpc-zone-identifier "subnet-1,subnet-2,subnet-3"
```

### VPC Networking

```bash
# Create VPC with CIDR
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Create subnets across AZs
aws ec2 create-subnet \
  --vpc-id vpc-12345678 \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a

# Internet Gateway
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway \
  --vpc-id vpc-12345678 \
  --internet-gateway-id igw-12345678

# NAT Gateway for private subnets
aws ec2 create-nat-gateway \
  --subnet-id subnet-12345678 \
  --allocation-id eipalloc-12345678
```

### S3 Storage Patterns

```bash
# Bucket with versioning and encryption
aws s3api create-bucket \
  --bucket my-bucket \
  --region us-east-1

aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled

aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "Archive old logs",
      "Status": "Enabled",
      "Prefix": "logs/",
      "Transitions": [{
        "Days": 30,
        "StorageClass": "STANDARD_IA"
      }, {
        "Days": 90,
        "StorageClass": "GLACIER"
      }]
    }]
  }'
```

### IAM Best Practices

```json
// Least privilege policy
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "s3:GetObject",
      "s3:PutObject"
    ],
    "Resource": "arn:aws:s3:::my-bucket/logs/*",
    "Condition": {
      "StringEquals": {
        "s3:x-amz-server-side-encryption": "AES256"
      }
    }
  }]
}

// Cross-account role trust
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "AWS": "arn:aws:iam::123456789012:root"
    },
    "Action": "sts:AssumeRole",
    "Condition": {
      "StringEquals": {
        "sts:ExternalId": "unique-external-id"
      }
    }
  }]
}
```

### Common Interview Questions - AWS

**Q: Design a highly available web application on AWS**
```
1. Multi-AZ deployment
   - ALB across 3 AZs
   - EC2 instances in Auto Scaling Groups
   - RDS Multi-AZ for database

2. Static content on S3 + CloudFront

3. ElastiCache for session management

4. Route 53 for DNS with health checks

5. CloudWatch for monitoring
```

**Q: How do you secure an S3 bucket?**
```
1. Block public access by default
2. Use bucket policies for access control
3. Enable encryption at rest
4. Enable versioning for data protection
5. Use VPC endpoints for private access
6. Enable CloudTrail logging
7. Use Object Lock for compliance
```

## GCP Deep Dive

### Compute Engine

```bash
# Create instance with startup script
gcloud compute instances create web-server \
  --machine-type=n2-standard-2 \
  --zone=us-central1-a \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --metadata-from-file startup-script=startup.sh \
  --tags=http-server,https-server \
  --network-tier=PREMIUM

# Instance template for MIG
gcloud compute instance-templates create web-template \
  --machine-type=n2-standard-2 \
  --network-interface=network=default,network-tier=PREMIUM \
  --maintenance-policy=MIGRATE \
  --tags=http-server

# Managed Instance Group
gcloud compute instance-groups managed create web-mig \
  --template=web-template \
  --size=3 \
  --zone=us-central1-a
```

### VPC Networking

```bash
# Create custom VPC
gcloud compute networks create my-vpc \
  --subnet-mode=custom \
  --bgp-routing-mode=regional

# Create subnet with secondary ranges
gcloud compute networks subnets create my-subnet \
  --network=my-vpc \
  --region=us-central1 \
  --range=10.0.0.0/24 \
  --secondary-range pods=10.1.0.0/16,services=10.2.0.0/16

# Cloud NAT for private instances
gcloud compute routers create nat-router \
  --network=my-vpc \
  --region=us-central1

gcloud compute routers nats create nat-gateway \
  --router=nat-router \
  --region=us-central1 \
  --nat-all-subnet-ip-ranges \
  --auto-allocate-nat-external-ips
```

### Cloud Storage

```bash
# Create bucket with versioning
gsutil mb -p PROJECT_ID -c STANDARD -l US gs://my-bucket/
gsutil versioning set on gs://my-bucket/

# Lifecycle management
cat > lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [{
      "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
      "condition": {"age": 30}
    }, {
      "action": {"type": "Delete"},
      "condition": {"age": 365}
    }]
  }
}
EOF
gsutil lifecycle set lifecycle.json gs://my-bucket/

# Customer-managed encryption keys
gsutil kms encryption gs://my-bucket/ \
  -k projects/PROJECT_ID/locations/us/keyRings/my-ring/cryptoKeys/my-key
```

### IAM & Security

```bash
# Create service account
gcloud iam service-accounts create app-sa \
  --display-name="Application Service Account"

# Grant roles
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:app-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

# Workload identity for GKE
kubectl create serviceaccount app-ksa
gcloud iam service-accounts add-iam-policy-binding \
  app-sa@PROJECT_ID.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:PROJECT_ID.svc.id.goog[default/app-ksa]"
```

### Common Interview Questions - GCP

**Q: Explain GCP's network architecture**
```
1. Global VPC spanning regions
2. Subnets are regional resources
3. Google's private network backbone
4. Cloud Load Balancing is global
5. Firewall rules are global
6. Routes can be regional or global
```

**Q: How does GCP billing work?**
```
1. Per-second billing for compute
2. Sustained use discounts automatic
3. Committed use discounts for 1-3 years
4. Preemptible VMs up to 80% cheaper
5. Egress charges for data transfer
6. Free tier includes always-free products
```

## Azure Deep Dive

### Virtual Machines

```bash
# Create VM with managed disk
az vm create \
  --resource-group myRG \
  --name myVM \
  --image UbuntuLTS \
  --size Standard_DS2_v2 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --custom-data cloud-init.yml \
  --zone 1

# VM Scale Set
az vmss create \
  --resource-group myRG \
  --name myVMSS \
  --image UbuntuLTS \
  --upgrade-policy-mode automatic \
  --instance-count 3 \
  --admin-username azureuser \
  --generate-ssh-keys
```

### Virtual Networks

```bash
# Create VNet with subnets
az network vnet create \
  --resource-group myRG \
  --name myVNet \
  --address-prefix 10.0.0.0/16 \
  --subnet-name web \
  --subnet-prefix 10.0.1.0/24

az network vnet subnet create \
  --resource-group myRG \
  --vnet-name myVNet \
  --name db \
  --address-prefix 10.0.2.0/24

# Network Security Group
az network nsg create \
  --resource-group myRG \
  --name myNSG

az network nsg rule create \
  --resource-group myRG \
  --nsg-name myNSG \
  --name AllowHTTP \
  --priority 100 \
  --destination-port-ranges 80 443 \
  --access Allow \
  --protocol Tcp
```

### Storage Accounts

```bash
# Create storage account
az storage account create \
  --name mystorageaccount \
  --resource-group myRG \
  --location eastus \
  --sku Standard_LRS \
  --encryption-services blob \
  --https-only true

# Create blob container
az storage container create \
  --name mycontainer \
  --account-name mystorageaccount \
  --public-access off

# Set lifecycle policy
az storage account management-policy create \
  --account-name mystorageaccount \
  --policy @policy.json \
  --resource-group myRG
```

### Azure AD & RBAC

```bash
# Create service principal
az ad sp create-for-rbac \
  --name myServicePrincipal \
  --role Contributor \
  --scopes /subscriptions/SUBSCRIPTION_ID

# Create custom role
az role definition create --role-definition '{
  "Name": "Custom Storage Reader",
  "Description": "Read storage accounts",
  "Actions": [
    "Microsoft.Storage/storageAccounts/read",
    "Microsoft.Storage/storageAccounts/listKeys/action"
  ],
  "AssignableScopes": ["/subscriptions/SUBSCRIPTION_ID"]
}'

# Assign role
az role assignment create \
  --assignee SERVICE_PRINCIPAL_ID \
  --role "Custom Storage Reader" \
  --scope /subscriptions/SUBSCRIPTION_ID
```

### Common Interview Questions - Azure

**Q: Explain Azure Resource Manager (ARM)**
```
1. Deployment and management service
2. Resource groups for logical grouping
3. ARM templates for IaC (JSON/Bicep)
4. Role-based access control
5. Tags for organization
6. Locks for protection
```

**Q: Azure availability concepts?**
```
1. Availability Zones - Physical separation
2. Availability Sets - Fault/Update domains
3. Region Pairs - Disaster recovery
4. Traffic Manager - Global load balancing
5. 99.99% SLA with AZ deployment
```

## Multi-Cloud Architecture

### Terraform Multi-Cloud

```hcl
# Provider configuration
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Multi-cloud module
module "compute" {
  source = "./modules/compute"
  
  providers = {
    aws     = aws
    google  = google
    azurerm = azurerm
  }
  
  cloud_provider = var.cloud_provider
  instance_count = var.instance_count
}
```

### Cost Optimization Strategies

```python
# Cross-cloud cost comparison
def compare_instance_costs():
    costs = {
        'aws': {
            't3.medium': 0.0416,
            'm5.large': 0.096,
            'c5.xlarge': 0.17
        },
        'gcp': {
            'n2-standard-2': 0.0971,
            'n2-standard-4': 0.1942,
            'c2-standard-4': 0.2088
        },
        'azure': {
            'B2s': 0.0416,
            'D2s_v3': 0.096,
            'F4s_v2': 0.169
        }
    }
    return costs

# Recommendations
def optimize_costs():
    strategies = [
        "Use spot/preemptible instances for non-critical workloads",
        "Right-size instances based on actual usage",
        "Use reserved instances for predictable workloads",
        "Implement auto-scaling to match demand",
        "Use appropriate storage tiers",
        "Set up budget alerts and cost anomaly detection"
    ]
    return strategies
```

## Common Interview Topics

### 1. High Availability Design
- Multi-region deployment
- Load balancing strategies
- Database replication
- Disaster recovery planning

### 2. Security Best Practices
- IAM principle of least privilege
- Network segmentation
- Encryption in transit and at rest
- Key management services

### 3. Performance Optimization
- Caching strategies (CDN, Redis)
- Database query optimization
- Auto-scaling policies
- Monitoring and alerting

### 4. Cost Management
- Reserved vs on-demand pricing
- Spot instance strategies
- Storage tiering
- Resource tagging

## Hands-On Practice

### Essential Labs
1. Deploy a 3-tier application
2. Set up cross-region replication
3. Implement auto-scaling
4. Configure VPN/Direct Connect
5. Build CI/CD pipeline

### Free Tier Resources
- **AWS**: 12 months free tier + always free services
- **GCP**: $300 credit + always free tier
- **Azure**: $200 credit + 12 months free services

## Quick Reference

### CLI Commands
```bash
# AWS
aws ec2 describe-instances
aws s3 ls
aws iam list-users

# GCP
gcloud compute instances list
gsutil ls
gcloud iam service-accounts list

# Azure
az vm list
az storage account list
az ad user list
```

## Resources

- 📚 [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- 📚 [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- 📚 [Azure Well-Architected Framework](https://docs.microsoft.com/en-us/azure/architecture/framework/)
- 🎓 [A Cloud Guru](https://acloudguru.com/) - Multi-cloud training
- 🎓 [Cloud Academy](https://cloudacademy.com/) - Hands-on labs

---

*Interview tip: Focus on the cloud platform used by your target company, but understand the concepts that apply across all platforms. Be ready to discuss trade-offs and decision-making criteria.*