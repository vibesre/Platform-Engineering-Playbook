---
title: AWS (Amazon Web Services)
description: Master the world's leading cloud platform for platform engineering
---

# AWS (Amazon Web Services)

AWS is the market leader in cloud computing. As a platform engineer, deep AWS knowledge enables you to build scalable, reliable infrastructure for any workload.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **AWS Certified Solutions Architect - Full Course**
- **Channel**: freeCodeCamp
- **Link**: [YouTube - 10 hours](https://www.youtube.com/watch?v=Ia-UEYYR44s)
- **Why it's great**: Comprehensive coverage of core AWS services

#### **AWS Tutorial For Beginners**
- **Channel**: Simplilearn
- **Link**: [YouTube - 5 hours](https://www.youtube.com/watch?v=k1RI5locZE4)
- **Why it's great**: Well-structured introduction to AWS fundamentals

#### **AWS re:Invent Videos**
- **Channel**: AWS Events
- **Link**: [YouTube Channel](https://www.youtube.com/c/AWSEventsChannel)
- **Why it's great**: Deep dives from AWS engineers and architects

### 📖 Essential Documentation

#### **AWS Documentation**
- **Link**: [docs.aws.amazon.com](https://docs.aws.amazon.com/)
- **Why it's great**: Comprehensive, always up-to-date

#### **AWS Well-Architected Framework**
- **Link**: [aws.amazon.com/architecture/well-architected/](https://aws.amazon.com/architecture/well-architected/)
- **Why it's great**: Best practices for building on AWS

#### **AWS Architecture Center**
- **Link**: [aws.amazon.com/architecture/](https://aws.amazon.com/architecture/)
- **Why it's great**: Reference architectures and whitepapers

### 📝 Must-Read Blogs & Articles

#### **AWS Blog**
- **Link**: [aws.amazon.com/blogs/aws/](https://aws.amazon.com/blogs/aws/)
- **Why it's great**: Official announcements and deep technical content

#### **A Cloud Guru Blog**
- **Link**: [acloudguru.com/blog/engineering](https://acloudguru.com/blog/engineering)
- **Why it's great**: Practical tutorials and exam prep

#### **Adrian Cantrill's Resources**
- **Link**: [learn.cantrill.io](https://learn.cantrill.io/)
- **Why it's great**: Deep technical content from AWS expert

### 🎓 Structured Courses

#### **AWS Skill Builder**
- **Link**: [explore.skillbuilder.aws](https://explore.skillbuilder.aws/)
- **Cost**: Free tier available
- **Why it's great**: Official AWS training with hands-on labs

#### **CloudAcademy AWS Learning Paths**
- **Link**: [cloudacademy.com/learning-paths/aws/](https://cloudacademy.com/learning-paths/aws/)
- **Why it's great**: Structured paths for different roles

### 🔧 Interactive Labs

#### **AWS Free Tier**
- **Link**: [aws.amazon.com/free/](https://aws.amazon.com/free/)
- **Why it's great**: Real AWS environment with free resources

#### **AWS Workshops**
- **Link**: [workshops.aws](https://workshops.aws/)
- **Why it's great**: Self-paced workshops on specific topics

#### **Qwiklabs**
- **Link**: [qwiklabs.com](https://www.qwiklabs.com/)
- **Why it's great**: Guided labs with temporary AWS accounts

### 🛠️ Essential Tools & Platforms

#### **AWS CLI**
- **Link**: [aws.amazon.com/cli/](https://aws.amazon.com/cli/)
- **Why it's great**: Essential command-line tool for AWS automation

#### **AWS CloudShell**
- **Link**: [aws.amazon.com/cloudshell/](https://aws.amazon.com/cloudshell/)
- **Why it's great**: Browser-based shell with pre-configured AWS CLI

#### **AWS Systems Manager Session Manager**
- **Link**: [aws.amazon.com/systems-manager/](https://aws.amazon.com/systems-manager/)
- **Why it's great**: Secure shell access without SSH keys or bastion hosts

#### **AWS Cloud9**
- **Link**: [aws.amazon.com/cloud9/](https://aws.amazon.com/cloud9/)
- **Why it's great**: Cloud-based IDE for development

#### **LocalStack**
- **Link**: [localstack.cloud](https://localstack.cloud/)
- **Why it's great**: Local AWS cloud stack for development and testing

### 👥 Communities & Forums

#### **AWS re:Post**
- **Link**: [repost.aws](https://repost.aws/)
- **Why it's great**: Official AWS community Q&A platform

#### **r/aws Reddit**
- **Link**: [reddit.com/r/aws](https://www.reddit.com/r/aws/)
- **Why it's great**: Active community discussions and real-world experiences

#### **AWS Community Builders**
- **Link**: [aws.amazon.com/developer/community/community-builders/](https://aws.amazon.com/developer/community/community-builders/)
- **Why it's great**: Connect with AWS experts and enthusiasts

#### **AWS User Groups**
- **Link**: [aws.amazon.com/developer/community/usergroups/](https://aws.amazon.com/developer/community/usergroups/)
- **Why it's great**: Local meetups and networking opportunities

#### **ServerlessLand**
- **Link**: [serverlessland.com](https://serverlessland.com/)
- **Why it's great**: Patterns, tools, and community for serverless on AWS

#### **AWS Heroes**
- **Link**: [aws.amazon.com/developer/community/heroes/](https://aws.amazon.com/developer/community/heroes/)
- **Why it's great**: Learn from recognized AWS experts

## 🎯 Key Services to Master

### Compute Services

#### EC2 (Elastic Compute Cloud)
```bash
# Launch EC2 instance via CLI
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name MyKeyPair \
  --security-group-ids sg-1234567890abcdef0 \
  --subnet-id subnet-6e7f829e \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyInstance}]'

# User data script for initialization
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello from AWS</h1>" > /var/www/html/index.html
```

#### Lambda
```python
# Lambda function example
import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Process S3 event
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Process the object
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read()
        
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }
```

### Storage Services

#### S3 (Simple Storage Service)
```bash
# S3 operations
aws s3 cp file.txt s3://my-bucket/
aws s3 sync ./local-dir s3://my-bucket/remote-dir
aws s3 ls s3://my-bucket/ --recursive

# S3 bucket policy
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::123456789012:user/user-name"},
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

#### EBS (Elastic Block Store)
- Volume types: gp3, gp2, io1, io2
- Snapshots and lifecycle management
- Encryption at rest
- Multi-Attach for io1/io2

### Networking

#### VPC (Virtual Private Cloud)
```terraform
# VPC setup with Terraform
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}
```

### Database Services

#### RDS (Relational Database Service)
- Multi-AZ deployments
- Read replicas
- Automated backups
- Performance Insights

#### DynamoDB
```python
# DynamoDB operations
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

# Put item
table.put_item(
    Item={
        'username': 'john_doe',
        'email': 'john@example.com',
        'age': 30
    }
)

# Query
response = table.query(
    KeyConditionExpression=Key('username').eq('john_doe')
)
```

### Container Services

#### ECS (Elastic Container Service)
```json
{
  "family": "web-app",
  "taskRoleArn": "arn:aws:iam::123456789012:role/ecsTaskRole",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsExecutionRole",
  "networkMode": "awsvpc",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "nginx:latest",
      "memory": 512,
      "cpu": 256,
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/web-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### EKS (Elastic Kubernetes Service)
```bash
# Create EKS cluster
eksctl create cluster \
  --name my-cluster \
  --region us-east-1 \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 4 \
  --managed

# Deploy application
kubectl apply -f deployment.yaml
kubectl expose deployment nginx --port=80 --type=LoadBalancer
```

## 💡 Interview Tips

### Common Interview Questions

1. **Explain the difference between EC2, ECS, and Lambda**
   - EC2: Virtual machines, full control
   - ECS: Container orchestration
   - Lambda: Serverless functions

2. **How do you secure an AWS environment?**
   - IAM roles and policies
   - Security Groups and NACLs
   - VPC design
   - Encryption at rest and in transit
   - AWS Organizations and SCPs

3. **Describe high availability in AWS**
   - Multi-AZ deployments
   - Auto Scaling Groups
   - Elastic Load Balancers
   - Route 53 health checks

4. **What's the difference between vertical and horizontal scaling?**
   - Vertical: Larger instance types
   - Horizontal: More instances
   - Auto Scaling for horizontal

5. **How do you optimize AWS costs?**
   - Right-sizing instances
   - Reserved Instances/Savings Plans
   - Spot Instances
   - S3 lifecycle policies
   - Cost allocation tags

### Practical Scenarios
- "Design a three-tier web application"
- "Implement disaster recovery"
- "Secure a multi-account setup"
- "Optimize for cost and performance"
- "Migrate on-premises to AWS"

## 🏆 Hands-On Practice

### Build These Projects

1. **Highly Available Web App**
   - Multi-AZ RDS
   - Auto Scaling Group
   - Application Load Balancer
   - CloudFront CDN
   - Route 53 DNS

2. **Serverless API**
   - API Gateway
   - Lambda functions
   - DynamoDB
   - Cognito authentication
   - X-Ray tracing

3. **Data Pipeline**
   - Kinesis ingestion
   - Lambda processing
   - S3 data lake
   - Athena queries
   - QuickSight dashboards

4. **Container Platform**
   - EKS cluster
   - ECR registries
   - Service mesh
   - Monitoring stack
   - GitOps deployment

### Certification Path
1. **Cloud Practitioner** - Foundation
2. **Solutions Architect Associate** - Core
3. **Developer Associate** - Application focus
4. **SysOps Administrator** - Operations
5. **Solutions Architect Professional** - Advanced
6. **DevOps Engineer Professional** - Specialized

## 📊 Learning Path

### Week 1-2: Core Services
- EC2 and VPC
- S3 and EBS
- IAM fundamentals
- Basic networking

### Week 3-4: Application Services
- RDS and DynamoDB
- Lambda and API Gateway
- SQS and SNS
- CloudWatch

### Week 5-6: Advanced Services
- ECS and EKS
- CloudFormation
- Organizations
- Security services

### Week 7-8: Production Skills
- High availability
- Disaster recovery
- Cost optimization
- Performance tuning

## AWS CDK (Cloud Development Kit)

AWS CDK allows you to define cloud infrastructure using familiar programming languages like TypeScript, Python, Java, and C#.

### Key CDK Concepts

```typescript
// Example CDK Stack
import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import * as lambda from '@aws-cdk/aws-lambda';
import * as apigateway from '@aws-cdk/aws-apigateway';

export class MyStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create S3 bucket
    const bucket = new s3.Bucket(this, 'MyBucket', {
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // Create Lambda function
    const handler = new lambda.Function(this, 'MyHandler', {
      runtime: lambda.Runtime.NODEJS_14_X,
      code: lambda.Code.fromAsset('lambda'),
      handler: 'index.handler',
      environment: {
        BUCKET_NAME: bucket.bucketName,
      },
    });

    // Grant Lambda permissions to access S3
    bucket.grantReadWrite(handler);

    // Create API Gateway
    const api = new apigateway.RestApi(this, 'MyApi', {
      restApiName: 'My Service',
    });

    const integration = new apigateway.LambdaIntegration(handler);
    api.root.addMethod('GET', integration);
  }
}
```

### CDK Best Practices

```typescript
// Use constructs for reusability
export class DatabaseConstruct extends cdk.Construct {
  public readonly instance: rds.DatabaseInstance;

  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);

    this.instance = new rds.DatabaseInstance(this, 'Database', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_13_7,
      }),
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
      vpc: vpc,
      credentials: rds.Credentials.fromGeneratedSecret('postgres'),
      deletionProtection: true,
    });
  }
}
```

## AWS Messaging Services

### Amazon SQS (Simple Queue Service)

```python
import boto3
import json

sqs = boto3.client('sqs')

# Create queue
queue_url = sqs.create_queue(
    QueueName='my-queue',
    Attributes={
        'DelaySeconds': '5',
        'MessageRetentionPeriod': '86400',
        'VisibilityTimeoutSeconds': '30',
    }
)['QueueUrl']

# Send message
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps({
        'orderId': '12345',
        'customerId': 'cust-456',
        'amount': 99.99
    }),
    MessageAttributes={
        'Priority': {
            'StringValue': 'High',
            'DataType': 'String'
        }
    }
)

# Receive and process messages
while True:
    messages = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=20,
    ).get('Messages', [])
    
    for message in messages:
        # Process message
        data = json.loads(message['Body'])
        print(f"Processing order: {data['orderId']}")
        
        # Delete message after processing
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
```

### Amazon SNS (Simple Notification Service)

```python
import boto3

sns = boto3.client('sns')

# Create topic
topic_arn = sns.create_topic(Name='order-notifications')['TopicArn']

# Subscribe email endpoint
sns.subscribe(
    TopicArn=topic_arn,
    Protocol='email',
    Endpoint='admin@company.com'
)

# Subscribe SQS queue
sns.subscribe(
    TopicArn=topic_arn,
    Protocol='sqs',
    Endpoint='arn:aws:sqs:us-east-1:123456789012:order-processing-queue'
)

# Publish message
sns.publish(
    TopicArn=topic_arn,
    Message=json.dumps({
        'orderId': '12345',
        'status': 'completed',
        'timestamp': datetime.utcnow().isoformat()
    }),
    Subject='Order Status Update',
    MessageAttributes={
        'event_type': {
            'DataType': 'String',
            'StringValue': 'order_completed'
        }
    }
)
```

### Amazon EventBridge

```python
import boto3

eventbridge = boto3.client('events')

# Create custom event bus
eventbridge.create_event_bus(Name='my-application-events')

# Create rule to route events
eventbridge.put_rule(
    Name='order-events-rule',
    EventPattern=json.dumps({
        'source': ['my.application'],
        'detail-type': ['Order Status Change'],
        'detail': {
            'status': ['completed', 'cancelled']
        }
    }),
    State='ENABLED',
    EventBusName='my-application-events'
)

# Add target (Lambda function)
eventbridge.put_targets(
    Rule='order-events-rule',
    EventBusName='my-application-events',
    Targets=[
        {
            'Id': '1',
            'Arn': 'arn:aws:lambda:us-east-1:123456789012:function:process-order-events',
        }
    ]
)

# Send custom event
eventbridge.put_events(
    Entries=[
        {
            'Source': 'my.application',
            'DetailType': 'Order Status Change',
            'Detail': json.dumps({
                'orderId': '12345',
                'status': 'completed',
                'customerId': 'cust-456'
            }),
            'EventBusName': 'my-application-events'
        }
    ]
)
```

## AWS Secrets Management

### AWS Secrets Manager

```python
import boto3
import json

secrets_client = boto3.client('secretsmanager')

# Create secret
secrets_client.create_secret(
    Name='prod/myapp/database',
    Description='Database credentials for production',
    SecretString=json.dumps({
        'username': 'dbuser',
        'password': 'super-secure-password',
        'host': 'prod-db.cluster-xyz.us-east-1.rds.amazonaws.com',
        'port': 5432,
        'dbname': 'myapp'
    })
)

# Retrieve secret
def get_secret(secret_name):
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        raise e

# Use in application
db_credentials = get_secret('prod/myapp/database')
connection_string = f"postgresql://{db_credentials['username']}:{db_credentials['password']}@{db_credentials['host']}:{db_credentials['port']}/{db_credentials['dbname']}"
```

### AWS Systems Manager Parameter Store

```python
import boto3

ssm = boto3.client('ssm')

# Store parameter
ssm.put_parameter(
    Name='/myapp/prod/database/host',
    Value='prod-db.cluster-xyz.us-east-1.rds.amazonaws.com',
    Type='String',
    Tier='Standard',
    Tags=[
        {
            'Key': 'Environment',
            'Value': 'Production'
        },
        {
            'Key': 'Application',
            'Value': 'MyApp'
        }
    ]
)

# Store secure parameter
ssm.put_parameter(
    Name='/myapp/prod/database/password',
    Value='super-secure-password',
    Type='SecureString',
    KeyId='alias/aws/ssm',  # Use AWS managed key
    Tier='Standard'
)

# Retrieve parameter
def get_parameter(name, decrypt=False):
    response = ssm.get_parameter(
        Name=name,
        WithDecryption=decrypt
    )
    return response['Parameter']['Value']

# Retrieve multiple parameters
def get_parameters_by_path(path):
    response = ssm.get_parameters_by_path(
        Path=path,
        Recursive=True,
        WithDecryption=True
    )
    return {param['Name']: param['Value'] for param in response['Parameters']}

# Usage
db_host = get_parameter('/myapp/prod/database/host')
db_password = get_parameter('/myapp/prod/database/password', decrypt=True)
all_db_config = get_parameters_by_path('/myapp/prod/database/')
```

### IAM Best Practices for Secrets

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:prod/myapp/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParameters",
        "ssm:GetParametersByPath"
      ],
      "Resource": [
        "arn:aws:ssm:us-east-1:123456789012:parameter/myapp/prod/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt"
      ],
      "Resource": "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012",
      "Condition": {
        "StringEquals": {
          "kms:ViaService": [
            "secretsmanager.us-east-1.amazonaws.com",
            "ssm.us-east-1.amazonaws.com"
          ]
        }
      }
    }
  ]
}
```

---

**Next Steps**: After mastering AWS fundamentals and advanced services, explore [Terraform](/technical/terraform) for infrastructure as code or [Docker](/technical/docker) and [Kubernetes](/technical/kubernetes) for container platforms.