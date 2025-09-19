# CloudFormation - AWS Native Infrastructure as Code

## Overview

AWS CloudFormation is Amazon's native Infrastructure as Code service that enables you to model and provision AWS resources using declarative JSON or YAML templates. It provides a common language for describing and provisioning all the infrastructure resources in your cloud environment.

## Architecture

### Core Components

1. **CloudFormation Service**
   - Template validation and parsing
   - Resource dependency resolution
   - Stack orchestration engine
   - Drift detection and remediation
   - Change set management

2. **Stack Architecture**
   - Stacks: Collection of AWS resources
   - Nested stacks: Modular template composition
   - Stack sets: Multi-account/region deployment
   - Stack policies: Update protection

3. **Template Components**
   - Parameters: Dynamic input values
   - Resources: AWS service definitions
   - Outputs: Stack return values
   - Mappings: Static configuration data
   - Conditions: Conditional resource creation
   - Transforms: Macro processing

4. **Resource Providers**
   - AWS native resources
   - Custom resources via Lambda
   - Third-party resource providers
   - AWS CloudFormation Registry

## Language Support

### YAML Templates
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Production VPC with public and private subnets'

# Input parameters
Parameters:
  EnvironmentName:
    Type: String
    Default: Production
    Description: Environment name prefix
    
  VpcCIDR:
    Type: String
    Default: 10.0.0.0/16
    Description: CIDR block for VPC
    AllowedPattern: ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$
    
  AvailabilityZones:
    Type: CommaDelimitedList
    Default: "us-east-1a,us-east-1b"
    Description: List of Availability Zones

# Mappings for configuration
Mappings:
  SubnetConfig:
    Public:
      CIDR: [10.0.0.0/24, 10.0.1.0/24, 10.0.2.0/24]
    Private:
      CIDR: [10.0.100.0/24, 10.0.101.0/24, 10.0.102.0/24]

# Conditional logic
Conditions:
  CreateNATGateway: !Equals [!Ref EnvironmentName, Production]
  Has3AZs: !Equals [!Select [2, !Ref AvailabilityZones], !Ref "AWS::NoValue"]

# Resources section
Resources:
  # VPC
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCIDR
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-VPC

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-IGW

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  # Public Subnets
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [0, !Ref AvailabilityZones]
      CidrBlock: !Select [0, !FindInMap [SubnetConfig, Public, CIDR]]
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-Public-Subnet-1
        - Key: kubernetes.io/role/elb
          Value: 1

  PublicSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [1, !Ref AvailabilityZones]
      CidrBlock: !Select [1, !FindInMap [SubnetConfig, Public, CIDR]]
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-Public-Subnet-2

  # NAT Gateways (conditional)
  NATGateway1EIP:
    Type: AWS::EC2::EIP
    Condition: CreateNATGateway
    DependsOn: AttachGateway
    Properties:
      Domain: vpc

  NATGateway1:
    Type: AWS::EC2::NatGateway
    Condition: CreateNATGateway
    Properties:
      AllocationId: !GetAtt NATGateway1EIP.AllocationId
      SubnetId: !Ref PublicSubnet1

  # Route Tables
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-Public-Routes

  PublicRoute:
    Type: AWS::EC2::Route
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  # Subnet Route Table Associations
  PublicSubnetRouteTableAssociation1:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet1
      RouteTableId: !Ref PublicRouteTable

# Outputs
Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub ${EnvironmentName}-VPC-ID

  PublicSubnets:
    Description: List of public subnets
    Value: !Join [",", [!Ref PublicSubnet1, !Ref PublicSubnet2]]
    Export:
      Name: !Sub ${EnvironmentName}-PUBLIC-SUBNETS
```

### JSON Templates
```json
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "ECS Fargate Service with ALB",
  
  "Parameters": {
    "ServiceName": {
      "Type": "String",
      "Description": "Name of the ECS service"
    },
    "ContainerImage": {
      "Type": "String",
      "Description": "Docker image URL"
    },
    "ContainerPort": {
      "Type": "Number",
      "Default": 80,
      "Description": "Container port"
    },
    "DesiredCount": {
      "Type": "Number",
      "Default": 2,
      "MinValue": 1,
      "MaxValue": 10
    }
  },
  
  "Resources": {
    "TaskDefinition": {
      "Type": "AWS::ECS::TaskDefinition",
      "Properties": {
        "Family": {"Ref": "ServiceName"},
        "NetworkMode": "awsvpc",
        "RequiresCompatibilities": ["FARGATE"],
        "Cpu": "256",
        "Memory": "512",
        "ContainerDefinitions": [
          {
            "Name": {"Ref": "ServiceName"},
            "Image": {"Ref": "ContainerImage"},
            "PortMappings": [
              {
                "ContainerPort": {"Ref": "ContainerPort"},
                "Protocol": "tcp"
              }
            ],
            "LogConfiguration": {
              "LogDriver": "awslogs",
              "Options": {
                "awslogs-group": {"Ref": "LogGroup"},
                "awslogs-region": {"Ref": "AWS::Region"},
                "awslogs-stream-prefix": "ecs"
              }
            }
          }
        ]
      }
    },
    
    "Service": {
      "Type": "AWS::ECS::Service",
      "DependsOn": "ALBListener",
      "Properties": {
        "ServiceName": {"Ref": "ServiceName"},
        "Cluster": {"Ref": "ECSCluster"},
        "TaskDefinition": {"Ref": "TaskDefinition"},
        "DesiredCount": {"Ref": "DesiredCount"},
        "LaunchType": "FARGATE",
        "NetworkConfiguration": {
          "AwsvpcConfiguration": {
            "AssignPublicIp": "ENABLED",
            "SecurityGroups": [{"Ref": "ServiceSecurityGroup"}],
            "Subnets": {"Ref": "SubnetIds"}
          }
        },
        "LoadBalancers": [
          {
            "ContainerName": {"Ref": "ServiceName"},
            "ContainerPort": {"Ref": "ContainerPort"},
            "TargetGroupArn": {"Ref": "TargetGroup"}
          }
        ]
      }
    }
  }
}
```

## Practical Examples

### Multi-Tier Web Application
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: 'Three-tier web application with RDS and ElastiCache'

Parameters:
  DatabasePassword:
    Type: String
    NoEcho: true
    MinLength: 8
    Description: Master password for RDS instance

Resources:
  # Application Load Balancer
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Type: application
      Scheme: internet-facing
      IpAddressType: ipv4
      Subnets: !Split [",", !ImportValue PublicSubnets]
      SecurityGroups:
        - !Ref ALBSecurityGroup
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-ALB

  # Auto Scaling Group
  WebServerGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      VPCZoneIdentifier: !Split [",", !ImportValue PrivateSubnets]
      LaunchTemplate:
        LaunchTemplateId: !Ref WebServerTemplate
        Version: !GetAtt WebServerTemplate.LatestVersionNumber
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 4
      TargetGroupARNs:
        - !Ref TargetGroup
      HealthCheckType: ELB
      HealthCheckGracePeriod: 300
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-WebServer
          PropagateAtLaunch: true

  WebServerTemplate:
    Type: AWS::EC2::LaunchTemplate
    Properties:
      LaunchTemplateName: !Sub ${AWS::StackName}-WebServer
      LaunchTemplateData:
        ImageId: !FindInMap [RegionMap, !Ref 'AWS::Region', AMI]
        InstanceType: t3.medium
        SecurityGroupIds:
          - !Ref WebServerSecurityGroup
        IamInstanceProfile:
          Arn: !GetAtt InstanceProfile.Arn
        UserData:
          Fn::Base64: !Sub |
            #!/bin/bash
            yum update -y
            yum install -y httpd php php-mysql
            
            # Configure application
            cat > /var/www/html/config.php << EOF
            <?php
            define('DB_HOST', '${DatabaseCluster.Endpoint.Address}');
            define('DB_NAME', 'webapp');
            define('DB_USER', 'admin');
            define('DB_PASS', '${DatabasePassword}');
            define('CACHE_HOST', '${CacheCluster.RedisEndpoint.Address}');
            define('CACHE_PORT', '${CacheCluster.RedisEndpoint.Port}');
            ?>
            EOF
            
            systemctl start httpd
            systemctl enable httpd

  # RDS Aurora Cluster
  DatabaseCluster:
    Type: AWS::RDS::DBCluster
    Properties:
      Engine: aurora-mysql
      EngineVersion: 5.7.mysql_aurora.2.10.1
      MasterUsername: admin
      MasterUserPassword: !Ref DatabasePassword
      DatabaseName: webapp
      DBClusterParameterGroupName: !Ref DBClusterParameterGroup
      DBSubnetGroupName: !Ref DBSubnetGroup
      VpcSecurityGroupIds:
        - !Ref DatabaseSecurityGroup
      BackupRetentionPeriod: 7
      PreferredBackupWindow: "03:00-04:00"
      PreferredMaintenanceWindow: "sun:04:00-sun:05:00"
      EnableCloudwatchLogsExports:
        - error
        - general
        - slowquery

  DatabaseInstance1:
    Type: AWS::RDS::DBInstance
    Properties:
      DBClusterIdentifier: !Ref DatabaseCluster
      DBInstanceClass: db.r5.large
      Engine: aurora-mysql
      DBSubnetGroupName: !Ref DBSubnetGroup

  DatabaseInstance2:
    Type: AWS::RDS::DBInstance
    Properties:
      DBClusterIdentifier: !Ref DatabaseCluster
      DBInstanceClass: db.r5.large
      Engine: aurora-mysql
      DBSubnetGroupName: !Ref DBSubnetGroup

  # ElastiCache Redis
  CacheCluster:
    Type: AWS::ElastiCache::ReplicationGroup
    Properties:
      ReplicationGroupId: !Sub ${AWS::StackName}-redis
      ReplicationGroupDescription: Redis cache for web application
      Engine: redis
      EngineVersion: 6.2
      CacheNodeType: cache.r6g.large
      NumCacheClusters: 2
      AutomaticFailoverEnabled: true
      MultiAZEnabled: true
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      SecurityGroupIds:
        - !Ref CacheSecurityGroup
      AtRestEncryptionEnabled: true
      TransitEncryptionEnabled: true
      SnapshotRetentionLimit: 5
      SnapshotWindow: "03:00-05:00"

  # Auto Scaling Policies
  ScaleUpPolicy:
    Type: AWS::AutoScaling::ScalingPolicy
    Properties:
      AdjustmentType: ChangeInCapacity
      AutoScalingGroupName: !Ref WebServerGroup
      Cooldown: 60
      ScalingAdjustment: 2

  ScaleDownPolicy:
    Type: AWS::AutoScaling::ScalingPolicy
    Properties:
      AdjustmentType: ChangeInCapacity
      AutoScalingGroupName: !Ref WebServerGroup
      Cooldown: 300
      ScalingAdjustment: -1

  # CloudWatch Alarms
  HighCPUAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmDescription: Trigger scale up when CPU > 70%
      MetricName: CPUUtilization
      Namespace: AWS/EC2
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 70
      AlarmActions:
        - !Ref ScaleUpPolicy
      Dimensions:
        - Name: AutoScalingGroupName
          Value: !Ref WebServerGroup
      ComparisonOperator: GreaterThanThreshold

Outputs:
  LoadBalancerDNS:
    Description: DNS name of the load balancer
    Value: !GetAtt ApplicationLoadBalancer.DNSName
  
  DatabaseEndpoint:
    Description: Aurora cluster endpoint
    Value: !GetAtt DatabaseCluster.Endpoint.Address
```

### Nested Stack Architecture
```yaml
# Master template
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Master stack for microservices architecture'

Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]
    Default: dev

Resources:
  # Network Stack
  NetworkStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/cf-templates/network.yaml
      Parameters:
        EnvironmentName: !Ref Environment
        VpcCIDR: 10.0.0.0/16
        PublicSubnetCount: 3
        PrivateSubnetCount: 3
      Tags:
        - Key: Component
          Value: Network

  # Security Stack
  SecurityStack:
    Type: AWS::CloudFormation::Stack
    DependsOn: NetworkStack
    Properties:
      TemplateURL: https://s3.amazonaws.com/cf-templates/security.yaml
      Parameters:
        VpcId: !GetAtt NetworkStack.Outputs.VpcId
        Environment: !Ref Environment
      Tags:
        - Key: Component
          Value: Security

  # Compute Stack
  ComputeStack:
    Type: AWS::CloudFormation::Stack
    DependsOn: [NetworkStack, SecurityStack]
    Properties:
      TemplateURL: https://s3.amazonaws.com/cf-templates/compute.yaml
      Parameters:
        VpcId: !GetAtt NetworkStack.Outputs.VpcId
        PrivateSubnets: !GetAtt NetworkStack.Outputs.PrivateSubnets
        ECSSecurityGroup: !GetAtt SecurityStack.Outputs.ECSSecurityGroup
        Environment: !Ref Environment
      Tags:
        - Key: Component
          Value: Compute

  # Application Stacks
  UserServiceStack:
    Type: AWS::CloudFormation::Stack
    DependsOn: ComputeStack
    Properties:
      TemplateURL: https://s3.amazonaws.com/cf-templates/service.yaml
      Parameters:
        ServiceName: user-service
        ClusterArn: !GetAtt ComputeStack.Outputs.ECSCluster
        TargetGroupArn: !GetAtt ComputeStack.Outputs.UserServiceTargetGroup
        ContainerImage: !Sub ${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/user-service:latest
        Environment: !Ref Environment

  OrderServiceStack:
    Type: AWS::CloudFormation::Stack
    DependsOn: ComputeStack
    Properties:
      TemplateURL: https://s3.amazonaws.com/cf-templates/service.yaml
      Parameters:
        ServiceName: order-service
        ClusterArn: !GetAtt ComputeStack.Outputs.ECSCluster
        TargetGroupArn: !GetAtt ComputeStack.Outputs.OrderServiceTargetGroup
        ContainerImage: !Sub ${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/order-service:latest
        Environment: !Ref Environment

Outputs:
  VpcId:
    Description: VPC ID
    Value: !GetAtt NetworkStack.Outputs.VpcId
    Export:
      Name: !Sub ${AWS::StackName}-VpcId

  LoadBalancerUrl:
    Description: Application Load Balancer URL
    Value: !GetAtt ComputeStack.Outputs.LoadBalancerUrl
```

### Custom Resources with Lambda
```yaml
Resources:
  # Custom resource Lambda function
  CustomResourceFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub ${AWS::StackName}-CustomResource
      Runtime: python3.9
      Handler: index.handler
      Role: !GetAtt CustomResourceRole.Arn
      Code:
        ZipFile: |
          import json
          import cfnresponse
          import boto3
          import hashlib
          
          def handler(event, context):
              try:
                  request_type = event['RequestType']
                  resource_properties = event['ResourceProperties']
                  
                  if request_type == 'Create':
                      # Generate unique ID
                      unique_id = hashlib.md5(
                          json.dumps(resource_properties, sort_keys=True).encode()
                      ).hexdigest()[:8]
                      
                      # Perform custom logic
                      result = create_custom_resource(resource_properties)
                      
                      cfnresponse.send(event, context, cfnresponse.SUCCESS, {
                          'UniqueId': unique_id,
                          'Result': result
                      }, unique_id)
                      
                  elif request_type == 'Update':
                      # Update logic
                      result = update_custom_resource(
                          event['PhysicalResourceId'],
                          resource_properties
                      )
                      cfnresponse.send(event, context, cfnresponse.SUCCESS, {
                          'Result': result
                      }, event['PhysicalResourceId'])
                      
                  elif request_type == 'Delete':
                      # Cleanup logic
                      delete_custom_resource(event['PhysicalResourceId'])
                      cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
                      
              except Exception as e:
                  print(f"Error: {str(e)}")
                  cfnresponse.send(event, context, cfnresponse.FAILED, {
                      'Error': str(e)
                  })
          
          def create_custom_resource(properties):
              # Custom creation logic
              return "Created successfully"
          
          def update_custom_resource(resource_id, properties):
              # Custom update logic
              return "Updated successfully"
          
          def delete_custom_resource(resource_id):
              # Custom deletion logic
              pass

  # Custom resource usage
  MyCustomResource:
    Type: Custom::MyResource
    Properties:
      ServiceToken: !GetAtt CustomResourceFunction.Arn
      ConfigurationData:
        Key1: Value1
        Key2: Value2
      DependentResource: !Ref SomeOtherResource
```

### StackSets for Multi-Account Deployment
```yaml
# StackSet template for security baseline
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Security baseline for all accounts'

Resources:
  # CloudTrail for all regions
  CloudTrail:
    Type: AWS::CloudTrail::Trail
    Properties:
      TrailName: !Sub ${AWS::AccountId}-security-trail
      S3BucketName: !Ref TrailBucket
      IncludeGlobalServiceEvents: true
      IsLogging: true
      IsMultiRegionTrail: true
      EnableLogFileValidation: true
      EventSelectors:
        - IncludeManagementEvents: true
          ReadWriteType: All
          DataResources:
            - Type: AWS::S3::Object
              Values: ["arn:aws:s3:::*/*"]

  # Config Rules
  RequiredTagsRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: required-tags
      Description: Ensure all resources have required tags
      Source:
        Owner: AWS
        SourceIdentifier: REQUIRED_TAGS
      InputParameters:
        tag1Key: Environment
        tag2Key: Owner
        tag3Key: CostCenter

  # GuardDuty
  GuardDutyDetector:
    Type: AWS::GuardDuty::Detector
    Properties:
      Enable: true
      FindingPublishingFrequency: FIFTEEN_MINUTES

  # Security Hub
  SecurityHub:
    Type: AWS::SecurityHub::Hub
    Properties:
      Tags:
        Environment: Production
```

## Best Practices

### 1. Template Organization
```yaml
# Well-structured template
AWSTemplateFormatVersion: '2010-09-09'
Description: |
  This template creates a highly available web application infrastructure
  with auto-scaling, load balancing, and database resources.
  
  Dependencies:
  - Network stack must be deployed first
  - Requires existing S3 bucket for static assets

Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: "Network Configuration"
        Parameters:
          - VpcId
          - SubnetIds
      - Label:
          default: "Application Configuration"
        Parameters:
          - InstanceType
          - KeyName
          - ApplicationPort
      - Label:
          default: "Database Configuration"
        Parameters:
          - DBInstanceClass
          - DBPassword
    ParameterLabels:
      VpcId:
        default: "Which VPC should this be deployed to?"

Parameters:
  # Parameters with constraints and patterns
  InstanceType:
    Type: String
    Default: t3.medium
    AllowedValues:
      - t3.micro
      - t3.small
      - t3.medium
      - t3.large
    ConstraintDescription: Must be a valid EC2 instance type
```

### 2. Cross-Stack References
```yaml
# Export values from one stack
Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub ${AWS::StackName}-VPC-ID

  DatabaseEndpoint:
    Description: RDS endpoint
    Value: !GetAtt Database.Endpoint.Address
    Export:
      Name: !Sub ${AWS::StackName}-DB-Endpoint

# Import in another stack
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      SubnetId:
        Fn::ImportValue: !Sub ${NetworkStackName}-PrivateSubnet1
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          export DB_HOST=${Fn::ImportValue: !Sub ${DataStackName}-DB-Endpoint}
```

### 3. Change Sets
```bash
# Create change set
aws cloudformation create-change-set \
  --stack-name production-stack \
  --change-set-name update-v2 \
  --template-body file://template.yaml \
  --parameters file://parameters.json \
  --capabilities CAPABILITY_NAMED_IAM

# Review changes
aws cloudformation describe-change-set \
  --change-set-name update-v2 \
  --stack-name production-stack

# Execute change set
aws cloudformation execute-change-set \
  --change-set-name update-v2 \
  --stack-name production-stack
```

### 4. Drift Detection
```yaml
# Lambda function for automated drift detection
DriftDetectionFunction:
  Type: AWS::Lambda::Function
  Properties:
    FunctionName: CloudFormationDriftDetector
    Runtime: python3.9
    Handler: index.handler
    Code:
      ZipFile: |
        import boto3
        import json
        
        cf = boto3.client('cloudformation')
        sns = boto3.client('sns')
        
        def handler(event, context):
            # List all stacks
            stacks = cf.list_stacks(
                StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE']
            )
            
            drifted_stacks = []
            
            for stack in stacks['StackSummaries']:
                # Detect drift
                cf.detect_stack_drift(StackName=stack['StackName'])
                
                # Check drift status
                drift_info = cf.describe_stack_drift_detection_status(
                    StackDriftDetectionId=detection_id
                )
                
                if drift_info['StackDriftStatus'] == 'DRIFTED':
                    drifted_stacks.append({
                        'StackName': stack['StackName'],
                        'DriftedResources': drift_info['DriftedStackResourceCount']
                    })
            
            if drifted_stacks:
                # Send notification
                sns.publish(
                    TopicArn=os.environ['SNS_TOPIC_ARN'],
                    Subject='CloudFormation Drift Detected',
                    Message=json.dumps(drifted_stacks, indent=2)
                )
            
            return {
                'statusCode': 200,
                'body': json.dumps(f'Checked {len(stacks)} stacks')
            }
```

### 5. Stack Policies
```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "Update:*",
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": [
        "Update:Replace",
        "Update:Delete"
      ],
      "Resource": "LogicalResourceId/ProductionDatabase"
    },
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "Update:*",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "ResourceType": [
            "AWS::RDS::DBInstance",
            "AWS::EC2::Instance"
          ]
        }
      }
    }
  ]
}
```

## Integration Patterns

### 1. CI/CD Pipeline Integration
```yaml
# CodePipeline for CloudFormation
CodePipeline:
  Type: AWS::CodePipeline::Pipeline
  Properties:
    RoleArn: !GetAtt CodePipelineRole.Arn
    Stages:
      - Name: Source
        Actions:
          - Name: SourceAction
            ActionTypeId:
              Category: Source
              Owner: ThirdParty
              Provider: GitHub
              Version: 1
            Configuration:
              Owner: !Ref GitHubOwner
              Repo: !Ref GitHubRepo
              Branch: !Ref GitHubBranch
              OAuthToken: !Ref GitHubOAuthToken
            OutputArtifacts:
              - Name: SourceCode

      - Name: Test
        Actions:
          - Name: ValidateTemplate
            ActionTypeId:
              Category: Test
              Owner: AWS
              Provider: CloudFormation
              Version: 1
            Configuration:
              ActionMode: VALIDATE_TEMPLATE
              TemplatePath: SourceCode::infrastructure/template.yaml
            InputArtifacts:
              - Name: SourceCode

      - Name: DeployToDev
        Actions:
          - Name: CreateChangeSet
            ActionTypeId:
              Category: Deploy
              Owner: AWS
              Provider: CloudFormation
              Version: 1
            Configuration:
              ActionMode: CREATE_UPDATE
              StackName: !Sub ${ApplicationName}-dev
              TemplatePath: SourceCode::infrastructure/template.yaml
              Capabilities: CAPABILITY_NAMED_IAM
              ParameterOverrides: |
                {
                  "Environment": "dev",
                  "InstanceCount": "1"
                }
              RoleArn: !GetAtt CloudFormationRole.Arn

      - Name: ManualApproval
        Actions:
          - Name: ApproveProduction
            ActionTypeId:
              Category: Approval
              Owner: AWS
              Provider: Manual
              Version: 1
            Configuration:
              CustomData: Please review dev deployment and approve for production

      - Name: DeployToProd
        Actions:
          - Name: CreateProdChangeSet
            ActionTypeId:
              Category: Deploy
              Owner: AWS
              Provider: CloudFormation
              Version: 1
            Configuration:
              ActionMode: CREATE_CHANGESET
              StackName: !Sub ${ApplicationName}-prod
              ChangeSetName: prod-changeset
              TemplatePath: SourceCode::infrastructure/template.yaml
              Capabilities: CAPABILITY_NAMED_IAM
              ParameterOverrides: |
                {
                  "Environment": "prod",
                  "InstanceCount": "3"
                }
              RoleArn: !GetAtt CloudFormationRole.Arn

          - Name: ExecuteChangeSet
            ActionTypeId:
              Category: Deploy
              Owner: AWS
              Provider: CloudFormation
              Version: 1
            Configuration:
              ActionMode: EXECUTE_CHANGESET
              StackName: !Sub ${ApplicationName}-prod
              ChangeSetName: prod-changeset
```

### 2. Service Catalog Integration
```yaml
# Service Catalog Product
ServiceCatalogProduct:
  Type: AWS::ServiceCatalog::CloudFormationProduct
  Properties:
    Name: StandardWebApplication
    Description: Standard three-tier web application
    Owner: Platform Team
    ProvisioningArtifactParameters:
      - Name: v1.0
        Description: Initial version
        Info:
          LoadTemplateFromURL: https://s3.amazonaws.com/templates/web-app.yaml
        Type: CLOUD_FORMATION_TEMPLATE

# Portfolio
ServiceCatalogPortfolio:
  Type: AWS::ServiceCatalog::Portfolio
  Properties:
    DisplayName: Application Templates
    Description: Approved application patterns
    ProviderName: Platform Team

# Product Association
ProductAssociation:
  Type: AWS::ServiceCatalog::PortfolioProductAssociation
  Properties:
    PortfolioId: !Ref ServiceCatalogPortfolio
    ProductId: !Ref ServiceCatalogProduct

# Principal Association
PortfolioPrincipalAssociation:
  Type: AWS::ServiceCatalog::PortfolioPrincipalAssociation
  Properties:
    PortfolioId: !Ref ServiceCatalogPortfolio
    PrincipalARN: !Sub arn:aws:iam::${AWS::AccountId}:role/DeveloperRole
    PrincipalType: IAM

# Launch Constraint
LaunchConstraint:
  Type: AWS::ServiceCatalog::LaunchRoleConstraint
  Properties:
    PortfolioId: !Ref ServiceCatalogPortfolio
    ProductId: !Ref ServiceCatalogProduct
    RoleArn: !GetAtt ServiceCatalogLaunchRole.Arn
```

### 3. Systems Manager Integration
```yaml
# Parameter Store integration
DatabasePassword:
  Type: AWS::SSM::Parameter::Value<String>
  Default: /myapp/prod/db/password
  NoEcho: true

# Using parameters in resources
Database:
  Type: AWS::RDS::DBInstance
  Properties:
    MasterUserPassword: !Ref DatabasePassword
    
# Automation Document
PatchingAutomation:
  Type: AWS::SSM::Document
  Properties:
    DocumentType: Automation
    Content:
      schemaVersion: 0.3
      description: Automated patching with CloudFormation update
      mainSteps:
        - name: UpdateCloudFormationStack
          action: aws:executeAwsApi
          inputs:
            Service: cloudformation
            Api: UpdateStack
            StackName: !Ref AWS::StackName
            UsePreviousTemplate: true
            Parameters:
              - ParameterKey: AMIId
                ParameterValue: '{{getLatestAMI.ImageId}}'
```

### 4. Cost Optimization
```yaml
# Scheduled scaling for non-production
ScheduledScaleDown:
  Type: AWS::AutoScaling::ScheduledAction
  Properties:
    AutoScalingGroupName: !Ref AutoScalingGroup
    MinSize: 0
    MaxSize: 0
    Recurrence: "0 19 * * 1-5"  # 7 PM weekdays

ScheduledScaleUp:
  Type: AWS::AutoScaling::ScheduledAction
  Properties:
    AutoScalingGroupName: !Ref AutoScalingGroup
    MinSize: 2
    MaxSize: 4
    Recurrence: "0 7 * * 1-5"   # 7 AM weekdays

# Cost allocation tags transform
Transform: AWS::CloudFormation::AutoTag

# Budget alerts
BudgetAlert:
  Type: AWS::Budgets::Budget
  Properties:
    Budget:
      BudgetName: !Sub ${AWS::StackName}-budget
      BudgetLimit:
        Amount: 1000
        Unit: USD
      TimeUnit: MONTHLY
      CostFilters:
        TagKeyValue:
          - !Sub "aws:cloudformation:stack-name${AWS::StackName}"
    NotificationsWithSubscribers:
      - Notification:
          NotificationType: ACTUAL
          ComparisonOperator: GREATER_THAN
          Threshold: 80
        Subscribers:
          - SubscriptionType: EMAIL
            Address: platform-team@company.com
```

### 5. Monitoring and Alerting
```yaml
# Stack event notifications
StackEventTopic:
  Type: AWS::SNS::Topic
  Properties:
    DisplayName: CloudFormation Stack Events
    Subscription:
      - Endpoint: platform-team@company.com
        Protocol: email

StackEventRule:
  Type: AWS::Events::Rule
  Properties:
    Description: Capture all CloudFormation stack events
    EventPattern:
      source:
        - aws.cloudformation
      detail-type:
        - CloudFormation Stack Status Change
    State: ENABLED
    Targets:
      - Arn: !Ref StackEventTopic
        Id: "1"

# Custom metrics
StackCreationMetric:
  Type: AWS::Logs::MetricFilter
  Properties:
    FilterPattern: "[time, request_id, event_type=CREATE_COMPLETE, ...]"
    LogGroupName: /aws/cloudformation/stack-events
    MetricTransformations:
      - MetricName: StackCreations
        MetricNamespace: CloudFormation
        MetricValue: "1"

# Dashboard
CloudFormationDashboard:
  Type: AWS::CloudWatch::Dashboard
  Properties:
    DashboardName: CloudFormation-Operations
    DashboardBody: !Sub |
      {
        "widgets": [
          {
            "type": "metric",
            "properties": {
              "metrics": [
                ["CloudFormation", "StackCreations", {"stat": "Sum"}],
                [".", "StackUpdates", {"stat": "Sum"}],
                [".", "StackDeletions", {"stat": "Sum"}]
              ],
              "period": 300,
              "stat": "Average",
              "region": "${AWS::Region}",
              "title": "Stack Operations"
            }
          }
        ]
      }
```

## Troubleshooting

### Common Issues

1. **Circular Dependencies**
```yaml
# Problem: Circular dependency
ResourceA:
  Type: AWS::Something
  Properties:
    Reference: !Ref ResourceB

ResourceB:
  Type: AWS::Something
  Properties:
    Reference: !Ref ResourceA

# Solution: Use DependsOn or restructure
ResourceA:
  Type: AWS::Something
  Properties:
    Reference: !GetAtt ResourceB.Arn
  DependsOn: ResourceB

ResourceB:
  Type: AWS::Something
```

2. **Update Rollback Failed**
```bash
# Continue update rollback
aws cloudformation continue-update-rollback \
  --stack-name my-stack \
  --resources-to-skip "ProblematicResource"

# Delete stack with retained resources
aws cloudformation delete-stack \
  --stack-name my-stack \
  --retain-resources "ImportantDatabase"
```

3. **Import Existing Resources**
```yaml
# Create template matching existing resource
Resources:
  ExistingBucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    Properties:
      BucketName: my-existing-bucket
      # Match ALL properties of existing bucket

# Import command
aws cloudformation create-change-set \
  --stack-name import-stack \
  --change-set-name import-resources \
  --change-set-type IMPORT \
  --resources-to-import file://resources-to-import.json \
  --template-body file://template.yaml
```

### Debug Techniques

```bash
# Enable detailed logging
aws cloudformation describe-stack-events \
  --stack-name my-stack \
  --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`]'

# Validate template
aws cloudformation validate-template \
  --template-body file://template.yaml

# Test with limited scope
aws cloudformation create-stack \
  --stack-name test-stack \
  --template-body file://template.yaml \
  --disable-rollback
```

## Conclusion

AWS CloudFormation provides a robust, native solution for Infrastructure as Code on AWS. Its deep integration with AWS services, comprehensive resource coverage, and declarative approach make it an excellent choice for AWS-centric deployments.

Key advantages include:
- Native AWS integration and service coverage
- No additional tools or languages to learn
- Automatic rollback and state management
- Built-in drift detection and remediation
- Strong security and compliance features

Whether you're managing simple single-region deployments or complex multi-account architectures, CloudFormation provides the tools and patterns needed for reliable, repeatable infrastructure deployment.