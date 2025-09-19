# Cloud Custodian

Cloud Custodian is an open-source cloud governance and management tool that enables organizations to manage their cloud resources and compliance at scale. It provides a rules engine for defining and enforcing policies across AWS, Azure, and Google Cloud Platform, making it essential for cloud security, cost management, and compliance in platform engineering.

## Overview

Cloud Custodian is widely used in platform engineering for:
- Automated cloud resource governance and compliance
- Cost optimization through resource lifecycle management
- Security policy enforcement and remediation
- Resource tagging and organization enforcement
- Automated cleanup of unused or non-compliant resources

## Key Features

- **Multi-Cloud Support**: AWS, Azure, Google Cloud Platform
- **Policy-as-Code**: YAML-based policy definitions
- **Real-Time and Scheduled Execution**: Event-driven and cron-based policies
- **Extensive Resource Support**: 200+ AWS services, Azure, and GCP resources
- **Rich Actions**: Stop, terminate, notify, tag, encrypt, and more
- **Integration**: Lambda, Azure Functions, Google Cloud Functions

## Installation and Setup

### Local Installation
```bash
# Install via pip
pip install c7n

# Install with specific cloud provider support
pip install c7n[aws]
pip install c7n[azure] 
pip install c7n[gcp]

# Install all providers
pip install c7n[all]

# Verify installation
custodian version
```

### Docker Installation
```bash
# Pull official image
docker pull cloudcustodian/c7n

# Run with AWS credentials
docker run --rm -it \
  -v $(pwd):/policies \
  -v ~/.aws:/root/.aws \
  cloudcustodian/c7n:latest \
  custodian run --dry-run /policies/policy.yml
```

### AWS Setup
```bash
# Configure AWS credentials
aws configure

# Create IAM role for Cloud Custodian (if using Lambda)
aws iam create-role --role-name CloudCustodianRole \
  --assume-role-policy-document file://trust-policy.json

aws iam attach-role-policy --role-name CloudCustodianRole \
  --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess

# trust-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## Basic Policy Structure

### Policy Anatomy
```yaml
# Basic policy structure
policies:
  - name: policy-name
    description: "Policy description"
    resource: aws.ec2              # Resource type
    mode:                          # Execution mode
      type: cloudtrail             # Event-driven
      events:
        - RunInstances
    filters:                       # Resource selection criteria
      - "tag:Environment": absent
    actions:                       # Actions to take
      - type: tag
        tags:
          Environment: untagged
```

### Simple Example Policies
```yaml
# policy-examples.yml
policies:
  # Tag untagged EC2 instances
  - name: tag-untagged-instances
    description: "Tag EC2 instances missing Environment tag"
    resource: aws.ec2
    filters:
      - "tag:Environment": absent
      - "State.Name": running
    actions:
      - type: tag
        tags:
          Environment: "untagged"
          CreatedBy: "cloud-custodian"

  # Stop instances after hours
  - name: stop-instances-after-hours
    description: "Stop non-production instances after business hours"
    resource: aws.ec2
    mode:
      type: periodic
      schedule: "cron(0 19 * * MON-FRI *)"  # 7 PM Mon-Fri
    filters:
      - "tag:Environment": ["dev", "test", "staging"]
      - "State.Name": running
    actions:
      - type: stop

  # Delete old snapshots
  - name: delete-old-snapshots
    description: "Delete EBS snapshots older than 30 days"
    resource: aws.ebs-snapshot
    filters:
      - type: age
        days: 30
        op: greater-than
      - "tag:KeepForever": absent
    actions:
      - type: delete

  # Encrypt unencrypted S3 buckets
  - name: encrypt-s3-buckets
    description: "Enable encryption on S3 buckets"
    resource: aws.s3
    filters:
      - type: bucket-encryption
        state: false
    actions:
      - type: encryption
        enabled: true
```

## Advanced Policy Examples

### Security and Compliance Policies
```yaml
# security-policies.yml
policies:
  # Enforce security group compliance
  - name: security-group-compliance
    description: "Remediate overly permissive security groups"
    resource: aws.security-group
    mode:
      type: cloudtrail
      events:
        - AuthorizeSecurityGroupIngress
        - AuthorizeSecurityGroupEgress
    filters:
      - type: ingress
        Ports: [22, 3389]
        Cidr: "0.0.0.0/0"
    actions:
      - type: remove-permissions
        ingress: matched
      - type: notify
        to:
          - security@company.com
        subject: "Security Group Violation Remediated"
        template: security-violation.html

  # Require MFA for privileged users
  - name: enforce-mfa-privileged-users
    description: "Ensure privileged IAM users have MFA enabled"
    resource: aws.iam-user
    filters:
      - type: policy
        key: "attached"
        value: true
        op: in
        value_type: swap
        value_from:
          expr: "PolicyNames[?contains(@, 'Admin')]"
      - type: mfa-device
        state: false
    actions:
      - type: notify
        to:
          - security@company.com
        subject: "MFA Required for Privileged User"

  # Encrypt unencrypted EBS volumes
  - name: encrypt-ebs-volumes
    description: "Encrypt unencrypted EBS volumes"
    resource: aws.ebs
    filters:
      - Encrypted: false
      - State: available
    actions:
      - type: encrypt-instance-storage
        key: alias/aws/ebs

  # Detect public RDS instances
  - name: detect-public-rds
    description: "Alert on publicly accessible RDS instances"
    resource: aws.rds
    filters:
      - PubliclyAccessible: true
    actions:
      - type: modify-db
        apply_immediately: true
        publicly_accessible: false
      - type: notify
        to:
          - security@company.com
        subject: "Public RDS Instance Secured"

  # Remove unused IAM roles
  - name: cleanup-unused-iam-roles
    description: "Remove IAM roles unused for 90 days"
    resource: aws.iam-role
    filters:
      - type: unused
        days: 90
      - type: service-role
        services: []  # Exclude service roles
    actions:
      - type: delete
```

### Cost Optimization Policies
```yaml
# cost-optimization-policies.yml
policies:
  # Right-size underutilized instances
  - name: rightsize-underutilized-instances
    description: "Recommend smaller instance types for underutilized EC2"
    resource: aws.ec2
    filters:
      - "State.Name": running
      - type: metrics
        name: CPUUtilization
        days: 14
        period: 86400
        statistics: Average
        value: 20
        op: less-than
    actions:
      - type: tag
        tags:
          RightsizeCandidate: "true"
          CurrentUtilization: "low"
      - type: notify
        to:
          - finops@company.com
        subject: "Right-sizing Opportunity"

  # Delete unattached EBS volumes
  - name: delete-unattached-volumes
    description: "Delete EBS volumes unattached for 7 days"
    resource: aws.ebs
    filters:
      - State: available
      - type: age
        days: 7
        op: greater-than
    actions:
      - type: delete

  # Stop idle RDS instances
  - name: stop-idle-rds
    description: "Stop RDS instances with no connections"
    resource: aws.rds
    filters:
      - DBInstanceStatus: available
      - type: metrics
        name: DatabaseConnections
        days: 7
        period: 86400
        statistics: Maximum
        value: 0
        op: equal
    actions:
      - type: stop

  # Clean up old AMIs
  - name: cleanup-old-amis
    description: "Deregister AMIs older than 6 months"
    resource: aws.ami
    filters:
      - type: age
        days: 180
        op: greater-than
      - type: unused
        days: 30
    actions:
      - type: deregister
        delete-snapshots: true

  # Optimize S3 storage classes
  - name: optimize-s3-storage-class
    description: "Move old S3 objects to cheaper storage classes"
    resource: aws.s3
    actions:
      - type: configure-lifecycle
        rules:
          - id: optimize-storage
            status: Enabled
            transitions:
              - days: 30
                storage_class: STANDARD_IA
              - days: 90
                storage_class: GLACIER
              - days: 365
                storage_class: DEEP_ARCHIVE
```

### Resource Tagging Policies
```yaml
# tagging-policies.yml
policies:
  # Enforce mandatory tags
  - name: enforce-mandatory-tags
    description: "Ensure all resources have mandatory tags"
    resource: aws.ec2
    mode:
      type: cloudtrail
      events:
        - RunInstances
    filters:
      - or:
          - "tag:Environment": absent
          - "tag:Owner": absent
          - "tag:Project": absent
          - "tag:CostCenter": absent
    actions:
      - type: stop
      - type: notify
        to:
          - "tag:Owner"
          - governance@company.com
        subject: "Resource Missing Mandatory Tags"

  # Auto-tag from instance metadata
  - name: auto-tag-from-metadata
    description: "Auto-tag resources based on metadata"
    resource: aws.ec2
    mode:
      type: cloudtrail
      events:
        - RunInstances
    actions:
      - type: auto-tag-user
        tag: CreatedBy
      - type: tag
        tags:
          AutoTagged: "true"
          CreationDate: "{now:%Y-%m-%d}"

  # Propagate tags to volumes
  - name: propagate-tags-to-volumes
    description: "Copy instance tags to attached EBS volumes"
    resource: aws.ebs
    filters:
      - type: instance
        key: "tag:Environment"
        value: present
    actions:
      - type: copy-instance-tags
        tags:
          - Environment
          - Owner
          - Project
          - CostCenter

  # Tag resources from CloudFormation stacks
  - name: tag-from-cloudformation
    description: "Tag resources based on CloudFormation stack"
    resource: aws.ec2
    filters:
      - "tag:aws:cloudformation:stack-name": present
    actions:
      - type: tag
        tags:
          ManagedBy: "CloudFormation"
          StackName: "tag:aws:cloudformation:stack-name"
```

## Execution Modes

### Local Execution
```bash
# Dry run (preview changes without executing)
custodian run --dry-run policy.yml

# Execute policy
custodian run policy.yml

# Execute specific policy
custodian run --policy-filter tag-untagged-instances policy.yml

# Execute with custom output directory
custodian run --output-dir ./results policy.yml

# Verbose output
custodian run -v policy.yml
```

### Lambda Mode (Event-Driven)
```yaml
# lambda-policy.yml
policies:
  - name: realtime-security-remediation
    description: "Real-time security group remediation"
    resource: aws.security-group
    mode:
      type: cloudtrail
      events:
        - AuthorizeSecurityGroupIngress
      role: arn:aws:iam::123456789012:role/CloudCustodianRole
      runtime: python3.9
      timeout: 300
      memory: 512
    filters:
      - type: ingress
        Ports: [22, 3389]
        Cidr: "0.0.0.0/0"
    actions:
      - type: remove-permissions
        ingress: matched
```

```bash
# Deploy to Lambda
custodian run --assume arn:aws:iam::123456789012:role/CloudCustodianRole lambda-policy.yml

# Check Lambda function
aws lambda list-functions --query 'Functions[?starts_with(FunctionName, `custodian`)]'
```

### Periodic Mode (Scheduled)
```yaml
# scheduled-policy.yml
policies:
  - name: daily-cleanup
    description: "Daily resource cleanup"
    resource: aws.ec2
    mode:
      type: periodic
      schedule: "cron(0 6 * * * *)"  # Daily at 6 AM UTC
      role: arn:aws:iam::123456789012:role/CloudCustodianRole
    filters:
      - "State.Name": stopped
      - type: age
        days: 7
        op: greater-than
    actions:
      - type: terminate
```

## Multi-Cloud Policies

### Azure Policies
```yaml
# azure-policies.yml
policies:
  # Stop deallocated VMs
  - name: cleanup-deallocated-vms
    description: "Remove VMs that have been deallocated for 7 days"
    resource: azure.vm
    filters:
      - type: instance-view
        key: statuses.0.code
        op: eq
        value: "PowerState/deallocated"
      - type: age
        days: 7
        op: greater-than
    actions:
      - type: delete

  # Enforce resource group tagging
  - name: enforce-rg-tagging
    description: "Ensure resource groups have required tags"
    resource: azure.resourcegroup
    filters:
      - or:
          - "tag:Environment": absent
          - "tag:Owner": absent
    actions:
      - type: tag
        tags:
          Environment: "untagged"
          RequiresReview: "true"

  # Secure storage accounts
  - name: secure-storage-accounts
    description: "Ensure storage accounts use HTTPS only"
    resource: azure.storage
    filters:
      - type: value
        key: properties.supportsHttpsTrafficOnly
        value: false
    actions:
      - type: modify
        https_only: true
```

### Google Cloud Policies
```yaml
# gcp-policies.yml
policies:
  # Clean up compute instances
  - name: cleanup-idle-instances
    description: "Stop idle Compute Engine instances"
    resource: gcp.instance
    filters:
      - status: RUNNING
      - type: metrics
        name: compute.googleapis.com/instance/cpu/utilization
        days: 7
        value: 0.05
        op: less-than
    actions:
      - type: stop

  # Enforce bucket encryption
  - name: enforce-bucket-encryption
    description: "Ensure GCS buckets are encrypted"
    resource: gcp.storage-bucket
    filters:
      - type: value
        key: encryption
        value: absent
    actions:
      - type: set-encryption
        key: projects/{project}/locations/global/keyRings/my-ring/cryptoKeys/my-key
```

## Notifications and Reporting

### Email Notifications
```yaml
# notification-policy.yml
policies:
  - name: security-violation-alert
    description: "Alert on security violations"
    resource: aws.security-group
    filters:
      - type: ingress
        Ports: [22]
        Cidr: "0.0.0.0/0"
    actions:
      - type: notify
        violation_desc: "Security group allows SSH from anywhere"
        action_desc: "Remove overly permissive rules"
        to:
          - security@company.com
          - "tag:Owner"
        subject: "Security Violation: {resource_type} {resource_id}"
        template: security-alert.html
        transport:
          type: ses
          region: us-east-1
```

### Slack Notifications
```yaml
# slack-notification.yml
policies:
  - name: cost-alert
    description: "Alert on high-cost resources"
    resource: aws.ec2
    filters:
      - type: instance-age
        days: 30
        op: greater-than
      - "State.Name": running
    actions:
      - type: notify
        to:
          - "#finops"
        subject: "Long-running instance detected"
        message: |
          Instance {InstanceId} has been running for more than 30 days.
          Current cost estimate: ${cost_estimate}/month
        transport:
          type: sns
          topic: arn:aws:sns:us-east-1:123456789012:slack-notifications
```

### Custom Notification Templates
```html
<!-- security-alert.html -->
<html>
<head>
    <title>Security Alert</title>
</head>
<body>
    <h2>Security Violation Detected</h2>
    
    <p><strong>Resource:</strong> {{ resource_id }}</p>
    <p><strong>Type:</strong> {{ resource_type }}</p>
    <p><strong>Region:</strong> {{ region }}</p>
    <p><strong>Account:</strong> {{ account_id }}</p>
    
    <h3>Violation Details</h3>
    <p>{{ violation_desc }}</p>
    
    <h3>Action Taken</h3>
    <p>{{ action_desc }}</p>
    
    <h3>Resource Tags</h3>
    <ul>
    {% for key, value in tags.items() %}
        <li><strong>{{ key }}:</strong> {{ value }}</li>
    {% endfor %}
    </ul>
    
    <p>Please review and take appropriate action if needed.</p>
    
    <p><em>This alert was generated by Cloud Custodian</em></p>
</body>
</html>
```

## Monitoring and Metrics

### CloudWatch Integration
```python
#!/usr/bin/env python3
"""
Cloud Custodian metrics and monitoring
"""

import boto3
import json
from datetime import datetime, timedelta

class CustodianMonitor:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.logs = boto3.client('logs')
        
    def get_policy_execution_metrics(self, days=7):
        """Get Cloud Custodian policy execution metrics"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        
        # Get Lambda function metrics for custodian policies
        lambda_client = boto3.client('lambda')
        functions = lambda_client.list_functions()
        
        custodian_functions = [
            f for f in functions['Functions'] 
            if f['FunctionName'].startswith('custodian-')
        ]
        
        metrics = {}
        
        for function in custodian_functions:
            function_name = function['FunctionName']
            
            # Get invocation count
            invocations = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Invocations',
                Dimensions=[
                    {'Name': 'FunctionName', 'Value': function_name}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Sum']
            )
            
            # Get error count
            errors = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Errors',
                Dimensions=[
                    {'Name': 'FunctionName', 'Value': function_name}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Sum']
            )
            
            # Get duration
            duration = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Duration',
                Dimensions=[
                    {'Name': 'FunctionName', 'Value': function_name}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average']
            )
            
            metrics[function_name] = {
                'invocations': sum(point['Sum'] for point in invocations['Datapoints']),
                'errors': sum(point['Sum'] for point in errors['Datapoints']),
                'avg_duration': sum(point['Average'] for point in duration['Datapoints']) / len(duration['Datapoints']) if duration['Datapoints'] else 0
            }
        
        return metrics
    
    def publish_custom_metrics(self, policy_name, resources_processed, actions_taken):
        """Publish custom metrics for policy execution"""
        
        self.cloudwatch.put_metric_data(
            Namespace='CloudCustodian',
            MetricData=[
                {
                    'MetricName': 'ResourcesProcessed',
                    'Dimensions': [
                        {'Name': 'PolicyName', 'Value': policy_name}
                    ],
                    'Value': resources_processed,
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                },
                {
                    'MetricName': 'ActionsTaken',
                    'Dimensions': [
                        {'Name': 'PolicyName', 'Value': policy_name}
                    ],
                    'Value': actions_taken,
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                }
            ]
        )
    
    def get_policy_logs(self, policy_name, hours=24):
        """Get logs for a specific policy"""
        log_group = f'/aws/lambda/custodian-{policy_name}'
        
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            response = self.logs.filter_log_events(
                logGroupName=log_group,
                startTime=int(start_time.timestamp() * 1000),
                endTime=int(end_time.timestamp() * 1000)
            )
            
            return response['events']
            
        except self.logs.exceptions.ResourceNotFoundException:
            return []
    
    def create_dashboard(self):
        """Create CloudWatch dashboard for Cloud Custodian metrics"""
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/Lambda", "Invocations", "FunctionName", "custodian-security-group-compliance"],
                            [".", "Errors", ".", "."],
                            ["CloudCustodian", "ResourcesProcessed", "PolicyName", "security-group-compliance"],
                            [".", "ActionsTaken", ".", "."]
                        ],
                        "period": 300,
                        "stat": "Sum",
                        "region": "us-east-1",
                        "title": "Cloud Custodian Policy Execution"
                    }
                },
                {
                    "type": "log",
                    "properties": {
                        "query": "SOURCE '/aws/lambda/custodian-security-group-compliance' | fields @timestamp, @message\n| filter @message like /ERROR/\n| sort @timestamp desc\n| limit 20",
                        "region": "us-east-1",
                        "title": "Recent Errors"
                    }
                }
            ]
        }
        
        self.cloudwatch.put_dashboard(
            DashboardName='CloudCustodian',
            DashboardBody=json.dumps(dashboard_body)
        )

# Usage
monitor = CustodianMonitor()
metrics = monitor.get_policy_execution_metrics()
print(json.dumps(metrics, indent=2))
```

### Policy Compliance Reporting
```python
#!/usr/bin/env python3
"""
Cloud Custodian compliance reporting
"""

import boto3
import json
import csv
from datetime import datetime
from collections import defaultdict

class ComplianceReporter:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.ec2 = boto3.client('ec2')
        self.iam = boto3.client('iam')
        
    def generate_compliance_report(self, bucket_name, report_prefix):
        """Generate comprehensive compliance report"""
        
        report_data = {
            'generated_at': datetime.utcnow().isoformat(),
            'compliance_checks': []
        }
        
        # Check EC2 compliance
        ec2_compliance = self.check_ec2_compliance()
        report_data['compliance_checks'].append({
            'category': 'EC2',
            'results': ec2_compliance
        })
        
        # Check IAM compliance
        iam_compliance = self.check_iam_compliance()
        report_data['compliance_checks'].append({
            'category': 'IAM',
            'results': iam_compliance
        })
        
        # Check S3 compliance
        s3_compliance = self.check_s3_compliance()
        report_data['compliance_checks'].append({
            'category': 'S3',
            'results': s3_compliance
        })
        
        # Upload report to S3
        report_key = f"{report_prefix}/compliance-report-{datetime.utcnow().strftime('%Y-%m-%d')}.json"
        
        self.s3.put_object(
            Bucket=bucket_name,
            Key=report_key,
            Body=json.dumps(report_data, indent=2),
            ContentType='application/json'
        )
        
        # Generate CSV summary
        self.generate_csv_summary(report_data, bucket_name, report_prefix)
        
        return report_data
    
    def check_ec2_compliance(self):
        """Check EC2 instance compliance"""
        results = {
            'total_instances': 0,
            'compliant_instances': 0,
            'violations': []
        }
        
        paginator = self.ec2.get_paginator('describe_instances')
        
        for page in paginator.paginate():
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    results['total_instances'] += 1
                    instance_id = instance['InstanceId']
                    
                    violations = []
                    
                    # Check for required tags
                    tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                    required_tags = ['Environment', 'Owner', 'Project']
                    
                    for tag in required_tags:
                        if tag not in tags:
                            violations.append(f"Missing required tag: {tag}")
                    
                    # Check if encrypted
                    for bdm in instance.get('BlockDeviceMappings', []):
                        if 'Ebs' in bdm and not bdm['Ebs'].get('Encrypted', False):
                            violations.append("Unencrypted EBS volume")
                    
                    # Check security groups
                    for sg in instance.get('SecurityGroups', []):
                        sg_details = self.ec2.describe_security_groups(
                            GroupIds=[sg['GroupId']]
                        )['SecurityGroups'][0]
                        
                        for rule in sg_details.get('IpPermissions', []):
                            for ip_range in rule.get('IpRanges', []):
                                if ip_range.get('CidrIp') == '0.0.0.0/0':
                                    if rule.get('FromPort') in [22, 3389]:
                                        violations.append(f"Overly permissive security group: {sg['GroupId']}")
                    
                    if violations:
                        results['violations'].append({
                            'resource_id': instance_id,
                            'resource_type': 'EC2 Instance',
                            'violations': violations,
                            'tags': tags
                        })
                    else:
                        results['compliant_instances'] += 1
        
        results['compliance_rate'] = (results['compliant_instances'] / results['total_instances']) * 100 if results['total_instances'] > 0 else 100
        
        return results
    
    def check_iam_compliance(self):
        """Check IAM compliance"""
        results = {
            'total_users': 0,
            'compliant_users': 0,
            'violations': []
        }
        
        paginator = self.iam.get_paginator('list_users')
        
        for page in paginator.paginate():
            for user in page['Users']:
                results['total_users'] += 1
                user_name = user['UserName']
                violations = []
                
                # Check for MFA
                mfa_devices = self.iam.list_mfa_devices(UserName=user_name)
                if not mfa_devices['MFADevices']:
                    violations.append("MFA not enabled")
                
                # Check for console access without recent activity
                try:
                    login_profile = self.iam.get_login_profile(UserName=user_name)
                    # Check last activity
                    user_detail = self.iam.get_user(UserName=user_name)
                    last_used = user_detail['User'].get('PasswordLastUsed')
                    
                    if last_used and (datetime.utcnow() - last_used.replace(tzinfo=None)).days > 90:
                        violations.append("Console access not used in 90 days")
                        
                except self.iam.exceptions.NoSuchEntityException:
                    pass  # User doesn't have console access
                
                # Check for overly permissive policies
                attached_policies = self.iam.list_attached_user_policies(UserName=user_name)
                for policy in attached_policies['AttachedPolicies']:
                    if 'Admin' in policy['PolicyName']:
                        violations.append(f"Admin policy attached: {policy['PolicyName']}")
                
                if violations:
                    results['violations'].append({
                        'resource_id': user_name,
                        'resource_type': 'IAM User',
                        'violations': violations
                    })
                else:
                    results['compliant_users'] += 1
        
        results['compliance_rate'] = (results['compliant_users'] / results['total_users']) * 100 if results['total_users'] > 0 else 100
        
        return results
    
    def check_s3_compliance(self):
        """Check S3 bucket compliance"""
        results = {
            'total_buckets': 0,
            'compliant_buckets': 0,
            'violations': []
        }
        
        buckets = self.s3.list_buckets()['Buckets']
        
        for bucket in buckets:
            results['total_buckets'] += 1
            bucket_name = bucket['Name']
            violations = []
            
            try:
                # Check encryption
                try:
                    encryption = self.s3.get_bucket_encryption(Bucket=bucket_name)
                except self.s3.exceptions.ClientError:
                    violations.append("Bucket encryption not enabled")
                
                # Check public access
                try:
                    public_access = self.s3.get_public_access_block(Bucket=bucket_name)
                    config = public_access['PublicAccessBlockConfiguration']
                    
                    if not all([
                        config.get('BlockPublicAcls', False),
                        config.get('IgnorePublicAcls', False),
                        config.get('BlockPublicPolicy', False),
                        config.get('RestrictPublicBuckets', False)
                    ]):
                        violations.append("Public access not fully blocked")
                        
                except self.s3.exceptions.ClientError:
                    violations.append("Public access block not configured")
                
                # Check versioning
                try:
                    versioning = self.s3.get_bucket_versioning(Bucket=bucket_name)
                    if versioning.get('Status') != 'Enabled':
                        violations.append("Versioning not enabled")
                except self.s3.exceptions.ClientError:
                    violations.append("Unable to check versioning")
                
                if violations:
                    results['violations'].append({
                        'resource_id': bucket_name,
                        'resource_type': 'S3 Bucket',
                        'violations': violations
                    })
                else:
                    results['compliant_buckets'] += 1
                    
            except Exception as e:
                violations.append(f"Error checking bucket: {str(e)}")
                results['violations'].append({
                    'resource_id': bucket_name,
                    'resource_type': 'S3 Bucket',
                    'violations': violations
                })
        
        results['compliance_rate'] = (results['compliant_buckets'] / results['total_buckets']) * 100 if results['total_buckets'] > 0 else 100
        
        return results
    
    def generate_csv_summary(self, report_data, bucket_name, report_prefix):
        """Generate CSV summary of compliance violations"""
        csv_data = []
        
        for check in report_data['compliance_checks']:
            category = check['category']
            results = check['results']
            
            # Add summary row
            csv_data.append({
                'Category': category,
                'Resource ID': 'SUMMARY',
                'Resource Type': 'Summary',
                'Compliance Rate': f"{results['compliance_rate']:.1f}%",
                'Total Resources': results.get('total_instances', results.get('total_users', results.get('total_buckets', 0))),
                'Violations': '',
                'Tags': ''
            })
            
            # Add violation rows
            for violation in results.get('violations', []):
                csv_data.append({
                    'Category': category,
                    'Resource ID': violation['resource_id'],
                    'Resource Type': violation['resource_type'],
                    'Compliance Rate': '',
                    'Total Resources': '',
                    'Violations': '; '.join(violation['violations']),
                    'Tags': json.dumps(violation.get('tags', {}))
                })
        
        # Write CSV to string
        import io
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=['Category', 'Resource ID', 'Resource Type', 'Compliance Rate', 'Total Resources', 'Violations', 'Tags'])
        writer.writeheader()
        writer.writerows(csv_data)
        
        # Upload CSV to S3
        csv_key = f"{report_prefix}/compliance-summary-{datetime.utcnow().strftime('%Y-%m-%d')}.csv"
        
        self.s3.put_object(
            Bucket=bucket_name,
            Key=csv_key,
            Body=output.getvalue(),
            ContentType='text/csv'
        )

# Usage
reporter = ComplianceReporter()
report = reporter.generate_compliance_report('compliance-reports-bucket', 'daily-reports')
print(f"Compliance report generated with {len(report['compliance_checks'])} categories")
```

## Best Practices

### Policy Development
```yaml
# best-practices-policies.yml
policies:
  # Use descriptive names and documentation
  - name: enforce-encryption-ebs-volumes
    description: |
      Ensures all EBS volumes are encrypted for data protection.
      This policy runs on volume creation events and encrypts
      unencrypted volumes automatically.
    resource: aws.ebs
    mode:
      type: cloudtrail
      events:
        - CreateVolume
      role: arn:aws:iam::123456789012:role/CloudCustodianRole
    filters:
      - Encrypted: false
    actions:
      - type: encrypt-instance-storage
        key: alias/aws/ebs
      - type: tag
        tags:
          EncryptedBy: cloud-custodian
          EncryptionDate: "{now:%Y-%m-%d}"

  # Use dry-run mode for testing
  - name: test-policy-dry-run
    description: "Test policy with dry-run mode enabled"
    resource: aws.ec2
    mode:
      type: periodic
      schedule: "cron(0 12 * * MON *)"  # Weekly on Monday at noon
      execution-options:
        output_dir: s3://custodian-logs/dry-run-results/
    filters:
      - "tag:Environment": ["test", "dev"]
      - "State.Name": stopped
      - type: age
        days: 14
        op: greater-than
    actions:
      - type: terminate
        dry-run: true  # Preview actions without executing
```

### Error Handling and Resilience
```yaml
# error-handling-policies.yml
policies:
  - name: resilient-policy-example
    description: "Policy with proper error handling"
    resource: aws.ec2
    mode:
      type: periodic
      schedule: "cron(0 */6 * * * *)"  # Every 6 hours
      execution-options:
        metrics_enabled: true
        log_group: /cloud-custodian/policies
        output_dir: s3://custodian-logs/
        assume_role: arn:aws:iam::123456789012:role/CloudCustodianRole
    filters:
      - "State.Name": running
      - type: age
        days: 1
        op: greater-than
    actions:
      - type: notify
        violation_desc: "Long-running instance detected"
        action_desc: "Instance will be stopped if not tagged as persistent"
        to:
          - "tag:Owner"
          - default-recipient@company.com
        subject: "Action Required: {resource_type} {resource_id}"
        template: warning-template.html
        transport:
          type: ses
          region: us-east-1
      - type: tag
        tags:
          StopWarning: "{now:%Y-%m-%d}"
          NotificationSent: "true"
```

### Security and Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CloudCustodianReadPermissions",
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "iam:List*",
        "iam:Get*",
        "s3:List*",
        "s3:Get*",
        "rds:Describe*",
        "cloudwatch:Get*",
        "cloudwatch:List*",
        "cloudtrail:LookupEvents",
        "logs:Describe*",
        "logs:Get*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CloudCustodianActionPermissions",
      "Effect": "Allow",
      "Action": [
        "ec2:StopInstances",
        "ec2:TerminateInstances",
        "ec2:CreateTags",
        "ec2:DeleteTags",
        "ec2:ModifyInstanceAttribute",
        "s3:PutBucketEncryption",
        "s3:PutBucketVersioning",
        "s3:PutPublicAccessBlock",
        "rds:StopDBInstance",
        "rds:ModifyDBInstance",
        "ses:SendEmail",
        "sns:Publish"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": ["us-east-1", "us-west-2"]
        }
      }
    },
    {
      "Sid": "CloudCustodianLogging",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:log-group:/cloud-custodian/*"
    }
  ]
}
```

## Resources

- [Cloud Custodian Documentation](https://cloudcustodian.io/docs/) - Official Cloud Custodian documentation
- [Cloud Custodian GitHub Repository](https://github.com/cloud-custodian/cloud-custodian) - Source code and examples
- [Policy Library](https://cloudcustodian.io/docs/policy/index.html) - Comprehensive policy examples
- [AWS Resource Reference](https://cloudcustodian.io/docs/aws/resources/index.html) - AWS resource types and filters
- [Azure Resource Reference](https://cloudcustodian.io/docs/azure/resources/index.html) - Azure resource types and filters
- [GCP Resource Reference](https://cloudcustodian.io/docs/gcp/resources/index.html) - GCP resource types and filters
- [Cloud Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/) - AWS security guidelines
- [FinOps Foundation](https://www.finops.org/) - Cloud financial management practices
- [Center for Internet Security](https://www.cisecurity.org/cis-benchmarks) - Security benchmarks
- [Cloud Governance Patterns](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/govern/) - Cloud governance frameworks