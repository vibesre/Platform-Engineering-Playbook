---
title: Cloud & Infrastructure
sidebar_position: 1
tags: [intermediate, cloud, aws, gcp, azure, terraform]
---

# ☁️ Cloud & Infrastructure

**Prerequisites**: Linux fundamentals, basic programming  
**Time to Complete**: ⏱️ 4-5 hours

## Introduction

Cloud platforms are the backbone of modern platform engineering. This guide covers the essential cloud services and infrastructure as code practices you need to master.

## Cloud Platform Overview

### The Big Three

| Provider | Market Share | Strengths | Best For |
|----------|-------------|-----------|----------|
| **AWS** | ~32% | Most services, mature ecosystem | Enterprise, startups |
| **Azure** | ~23% | Microsoft integration, hybrid cloud | Enterprise, .NET shops |
| **GCP** | ~10% | Data/ML services, Kubernetes | Analytics, cloud-native |

### Choosing a Cloud Provider

Start with one and deeply understand it before learning others. The concepts transfer well between clouds.

## Core Cloud Services

### Compute Services

#### Virtual Machines
```bash
# AWS EC2
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.micro \
  --key-name my-key \
  --security-group-ids sg-123456

# GCP Compute Engine  
gcloud compute instances create my-instance \
  --machine-type=e2-micro \
  --zone=us-central1-a \
  --image-family=ubuntu-2004-lts

# Azure VM
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image UbuntuLTS \
  --size Standard_B1s
```

#### Container Services
- **AWS**: ECS (proprietary), EKS (Kubernetes)
- **GCP**: GKE (best Kubernetes experience)
- **Azure**: AKS (Kubernetes), Container Instances

#### Serverless
```python
# AWS Lambda function
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

# Deploy with SAM
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.9
```

### Storage Services

#### Object Storage
```python
# S3 example
import boto3

s3 = boto3.client('s3')

# Upload file
s3.upload_file('local-file.txt', 'my-bucket', 'remote-file.txt')

# Generate presigned URL
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket', 'Key': 'file.txt'},
    ExpiresIn=3600
)
```

#### Storage Types Comparison
| Type | Use Case | AWS | GCP | Azure |
|------|----------|-----|-----|-------|
| Object | Unstructured data | S3 | Cloud Storage | Blob Storage |
| Block | VM disks | EBS | Persistent Disk | Managed Disks |
| File | Shared storage | EFS | Filestore | Files |

### Networking

#### Virtual Networks
```hcl
# Terraform VPC example
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}
```

#### Load Balancing
```yaml
# Kubernetes service with load balancer
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: my-app
```

### Database Services

#### Managed Databases
```python
# Connect to RDS
import psycopg2

conn = psycopg2.connect(
    host="mydb.123456.us-east-1.rds.amazonaws.com",
    database="myapp",
    user="dbuser",
    password=os.environ['DB_PASSWORD']
)

# Use connection pooling for production
from psycopg2 import pool

db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # min and max connections
    host="...",
    database="..."
)
```

## Infrastructure as Code (IaC)

### Why IaC?
- **Version Control**: Track infrastructure changes
- **Reproducibility**: Same infrastructure every time
- **Automation**: No manual clicking
- **Documentation**: Code is documentation

### Terraform Fundamentals

#### Basic Structure
```hcl
# providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

# main.tf
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  tags = {
    Name        = "web-server"
    Environment = "production"
  }
}

# outputs.tf
output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

#### Terraform Workflow
```bash
# Initialize terraform
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply

# Destroy resources
terraform destroy
```

### Advanced Terraform Patterns

#### Modules
```hcl
# modules/webserver/main.tf
resource "aws_instance" "this" {
  ami           = var.ami
  instance_type = var.instance_type
  
  vpc_security_group_ids = [aws_security_group.this.id]
  
  user_data = templatefile("${path.module}/user-data.sh", {
    app_port = var.app_port
  })
}

# Using the module
module "web_cluster" {
  source = "./modules/webserver"
  
  instance_count = 3
  instance_type  = "t3.small"
  app_port      = 8080
}
```

#### Remote State
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
    
    # Enable state locking
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

### Alternative IaC Tools

#### Pulumi (Programming Languages)
```python
import pulumi
from pulumi_aws import s3

# Create an S3 bucket
bucket = s3.Bucket('my-bucket',
    website=s3.BucketWebsiteArgs(
        index_document="index.html",
    ))

# Export the bucket name
pulumi.export('bucket_name', bucket.id)
```

#### CloudFormation (AWS Native)
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-unique-bucket-name
      VersioningConfiguration:
        Status: Enabled
```

## Cloud Architecture Patterns

### Multi-Tier Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CloudFront│────▶│   ALB       │────▶│   EC2/ECS   │
│   (CDN)     │     │(Load Balancer)    │  (App Tier)  │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │   RDS       │
                                        │ (Database)  │
                                        └─────────────┘
```

### Microservices on Kubernetes
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: myapp:v1.0
        ports:
        - containerPort: 8080
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: host
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

### Serverless Architecture
```python
# API Gateway + Lambda + DynamoDB
import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    # Parse request
    body = json.loads(event['body'])
    
    # Write to DynamoDB
    table.put_item(
        Item={
            'user_id': body['user_id'],
            'name': body['name'],
            'email': body['email'],
            'created_at': Decimal(time.time())
        }
    )
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'User created'})
    }
```

## Cost Optimization

### Cost Management Strategies

1. **Right-sizing**
   ```python
   # Monitor instance metrics
   import boto3
   
   cloudwatch = boto3.client('cloudwatch')
   
   response = cloudwatch.get_metric_statistics(
       Namespace='AWS/EC2',
       MetricName='CPUUtilization',
       Dimensions=[{'Name': 'InstanceId', 'Value': 'i-1234567'}],
       StartTime=datetime.now() - timedelta(days=7),
       EndTime=datetime.now(),
       Period=3600,
       Statistics=['Average']
   )
   ```

2. **Auto-scaling**
   ```hcl
   resource "aws_autoscaling_group" "app" {
     min_size         = 2
     max_size         = 10
     desired_capacity = 3
     
     target_group_arns = [aws_lb_target_group.app.arn]
     
     launch_template {
       id      = aws_launch_template.app.id
       version = "$Latest"
     }
   }
   
   resource "aws_autoscaling_policy" "scale_up" {
     name                   = "scale-up"
     autoscaling_group_name = aws_autoscaling_group.app.name
     adjustment_type        = "ChangeInCapacity"
     scaling_adjustment     = 2
     cooldown              = 300
   }
   ```

3. **Spot Instances**
   ```yaml
   # EKS with Spot instances
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   metadata:
     name: my-cluster
   nodeGroups:
     - name: spot-nodes
       instanceTypes: ["t3.medium", "t3a.medium"]
       spot: true
       minSize: 2
       maxSize: 10
   ```

## Security Best Practices

### Identity and Access Management

```hcl
# Least privilege IAM role
resource "aws_iam_role" "app_role" {
  name = "app-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "app_policy" {
  name = "app-policy"
  role = aws_iam_role.app_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject"
      ]
      Resource = "arn:aws:s3:::my-app-bucket/*"
    }]
  })
}
```

### Network Security

```hcl
# Security group with minimal access
resource "aws_security_group" "web" {
  name_prefix = "web-sg"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Interview Preparation

### Common Cloud Interview Questions

**Q: How would you design a highly available web application?**

Key points to cover:
- Multi-AZ deployment
- Load balancing (ALB/NLB)
- Auto-scaling groups
- RDS Multi-AZ or Aurora
- CloudFront CDN
- Route 53 health checks

**Q: Explain the shared responsibility model**

AWS Example:
- **AWS Responsibility**: Physical security, hypervisor, network infrastructure
- **Customer Responsibility**: OS patches, application security, data encryption, IAM

**Q: How do you secure sensitive data in the cloud?**

```python
# Encryption at rest
resource "aws_s3_bucket" "secure" {
  bucket = "my-secure-bucket"
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

# Encryption in transit
# Always use HTTPS/TLS
# VPN or Direct Connect for private connectivity
```

### Hands-On Scenarios

**Scenario 1: Migrate a monolith to microservices**
1. Containerize the application
2. Set up container orchestration (EKS/GKE)
3. Implement service discovery
4. Set up API gateway
5. Implement distributed tracing

**Scenario 2: Implement disaster recovery**
1. Set up cross-region replication
2. Automate backups
3. Create runbooks
4. Test failover procedures
5. Monitor RTO/RPO

## Practice Projects

### Project 1: Static Website Hosting
- Host a static site on S3/Cloud Storage
- Set up CloudFront/Cloud CDN
- Configure custom domain
- Implement CI/CD with GitHub Actions

### Project 2: Three-Tier Application
- Deploy web tier (Auto-scaling group)
- Set up application tier (ECS/GKE)
- Configure database tier (RDS/Cloud SQL)
- Implement monitoring and alerting

### Project 3: Infrastructure Pipeline
- Create Terraform modules
- Set up remote state
- Implement GitOps workflow
- Add automated testing

## Next Steps

You're ready to dive deeper! Continue with:
- [Containers & Kubernetes →](containers-kubernetes)
- [CI/CD & Automation →](cicd-automation)

## Quick Reference

### AWS CLI Essentials
```bash
# Configure credentials
aws configure

# List resources
aws ec2 describe-instances
aws s3 ls
aws rds describe-db-instances

# Create resources
aws ec2 run-instances --image-id ami-xxx
aws s3 mb s3://my-bucket
```

### Terraform Commands
```bash
terraform init          # Initialize
terraform plan         # Preview
terraform apply        # Deploy
terraform destroy      # Cleanup
terraform fmt          # Format code
terraform validate     # Validate syntax
```

### Cost Optimization Checklist
- [ ] Use appropriate instance types
- [ ] Enable auto-scaling
- [ ] Consider spot instances
- [ ] Set up budget alerts
- [ ] Tag all resources
- [ ] Review unused resources

## Additional Resources

- 📚 **Book**: [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- 🎥 **Course**: [Cloud Computing Basics](https://www.coursera.org/learn/cloud-computing-basics)
- 🎮 **Practice**: [AWS Free Tier](https://aws.amazon.com/free/)
- 📖 **Documentation**: [Terraform Tutorials](https://learn.hashicorp.com/terraform)