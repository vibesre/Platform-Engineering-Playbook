# Infracost

Infracost is an open-source tool that provides cost estimates for infrastructure changes before deployment. It helps platform engineers understand the financial impact of infrastructure modifications, enabling cost-conscious decision-making and budget management in cloud environments.

## Overview

Infracost is widely used in platform engineering for:
- Estimating cloud infrastructure costs before deployment
- Preventing cost surprises in CI/CD pipelines
- Tracking cost changes in pull requests
- Optimizing cloud spending through cost awareness
- Implementing FinOps practices in development workflows

## Key Features

- **Multi-Cloud Support**: AWS, Azure, Google Cloud Platform
- **Infrastructure as Code**: Terraform, Terragrunt, AWS CloudFormation
- **CI/CD Integration**: GitHub Actions, GitLab CI, Azure DevOps
- **Cost Breakdown**: Detailed cost analysis by resource type
- **Diff Views**: Cost comparisons between infrastructure versions
- **Policy Engine**: Custom cost policies and guardrails

## Installation and Setup

### Binary Installation
```bash
# macOS (Homebrew)
brew install infracost

# Linux
curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh

# Windows (PowerShell)
iwr -useb https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.ps1 | iex

# Docker
docker pull infracost/infracost

# Verify installation
infracost --version
```

### Authentication Setup
```bash
# Register for free API key
infracost auth login

# Or set API key manually
export INFRACOST_API_KEY="your-api-key"

# Validate authentication
infracost configure get api_key
```

### Configuration File
```yaml
# .infracost/config.yml
version: "0.1"

projects:
  - path: terraform/environments/production
    name: production-infrastructure
    terraform_plan_flags: -var-file=production.tfvars
    
  - path: terraform/environments/staging
    name: staging-infrastructure
    terraform_plan_flags: -var-file=staging.tfvars
    
  - path: terraform/modules/networking
    name: networking-module
    skip_autodetect: true

currency: USD
pricing_api_endpoint: https://pricing.api.infracost.io
```

## Basic Usage

### Terraform Cost Estimation
```bash
# Generate cost estimate for Terraform configuration
infracost breakdown --path terraform/

# With specific var file
infracost breakdown --path terraform/ --terraform-var-file=production.tfvars

# Show costs in table format
infracost breakdown --path terraform/ --format table

# Show costs in JSON format
infracost breakdown --path terraform/ --format json

# Save output to file
infracost breakdown --path terraform/ --out-file costs.json

# Compare with previous plan
infracost diff --path terraform/ --compare-to infracost-base.json
```

### Multi-Project Analysis
```bash
# Use configuration file for multiple projects
infracost breakdown --config-file .infracost/config.yml

# Generate costs for specific projects
infracost breakdown --config-file .infracost/config.yml --project-names production-infrastructure

# Generate HTML report
infracost breakdown --config-file .infracost/config.yml --format html --out-file cost-report.html
```

### Cost Policies
```bash
# Check against cost policies
infracost breakdown --path terraform/ --policy-path policies/

# Policy file example (policy.rego)
package infracost

deny[msg] {
    input.projects[_].breakdown.totalMonthlyCost > 1000
    msg := "Monthly cost exceeds $1000 limit"
}

warn[msg] {
    input.projects[_].breakdown.totalMonthlyCost > 500
    msg := "Monthly cost is approaching $1000 limit"
}
```

## Terraform Integration

### Terraform Cost Analysis
```hcl
# Example Terraform configuration for cost analysis
# main.tf
provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region"
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  default     = "production"
}

variable "instance_count" {
  description = "Number of EC2 instances"
  default     = 3
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t3.medium"
}

# VPC and Networking
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name        = "${var.environment}-igw"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  count = 2
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name        = "${var.environment}-public-${count.index + 1}"
    Environment = var.environment
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
  
  enable_deletion_protection = var.environment == "production"
  
  tags = {
    Name        = "${var.environment}-alb"
    Environment = var.environment
  }
}

# EC2 Instances
resource "aws_instance" "web" {
  count = var.instance_count
  
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public[count.index % length(aws_subnet.public)].id
  
  vpc_security_group_ids = [aws_security_group.web.id]
  
  root_block_device {
    volume_type = "gp3"
    volume_size = 20
    encrypted   = true
  }
  
  tags = {
    Name        = "${var.environment}-web-${count.index + 1}"
    Environment = var.environment
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# RDS Database
resource "aws_db_instance" "main" {
  identifier = "${var.environment}-database"
  
  engine         = "postgres"
  engine_version = "14.9"
  instance_class = var.environment == "production" ? "db.r5.large" : "db.t3.micro"
  
  allocated_storage     = var.environment == "production" ? 100 : 20
  max_allocated_storage = var.environment == "production" ? 1000 : 100
  storage_type          = "gp2"
  storage_encrypted     = true
  
  db_name  = "myapp"
  username = "postgres"
  password = "changeme123!"  # Use AWS Secrets Manager in production
  
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = var.environment == "production" ? 7 : 1
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = var.environment != "production"
  
  tags = {
    Name        = "${var.environment}-database"
    Environment = var.environment
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.environment}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id
  
  tags = {
    Name        = "${var.environment}-db-subnet-group"
    Environment = var.environment
  }
}

resource "aws_subnet" "private" {
  count = 2
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name        = "${var.environment}-private-${count.index + 1}"
    Environment = var.environment
  }
}

# S3 Bucket
resource "aws_s3_bucket" "storage" {
  bucket = "${var.environment}-app-storage-${random_id.bucket_suffix.hex}"
  
  tags = {
    Name        = "${var.environment}-storage"
    Environment = var.environment
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 8
}

resource "aws_s3_bucket_versioning" "storage" {
  bucket = aws_s3_bucket.storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "storage" {
  bucket = aws_s3_bucket.storage.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "/aws/ec2/${var.environment}/app"
  retention_in_days = var.environment == "production" ? 30 : 7
  
  tags = {
    Name        = "${var.environment}-app-logs"
    Environment = var.environment
  }
}

# Security Groups
resource "aws_security_group" "alb" {
  name_prefix = "${var.environment}-alb-"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
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
  
  tags = {
    Name        = "${var.environment}-alb-sg"
    Environment = var.environment
  }
}

resource "aws_security_group" "web" {
  name_prefix = "${var.environment}-web-"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name        = "${var.environment}-web-sg"
    Environment = var.environment
  }
}

resource "aws_security_group" "db" {
  name_prefix = "${var.environment}-db-"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }
  
  tags = {
    Name        = "${var.environment}-db-sg"
    Environment = var.environment
  }
}

# Outputs
output "monthly_cost_estimate" {
  description = "Run 'infracost breakdown --path .' to see cost estimate"
  value       = "Run infracost to see cost breakdown"
}

output "load_balancer_dns" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "database_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}
```

### Cost Optimization Examples
```bash
# Analyze current costs
infracost breakdown --path terraform/ --format table

# Compare different instance types
# production.tfvars
instance_type = "t3.large"
instance_count = 3

# staging.tfvars  
instance_type = "t3.medium"
instance_count = 2

# Compare environments
infracost breakdown --path terraform/ --terraform-var-file=production.tfvars > production-costs.json
infracost breakdown --path terraform/ --terraform-var-file=staging.tfvars > staging-costs.json

# Generate comparison
infracost diff --path terraform/ \
  --terraform-var-file=staging.tfvars \
  --compare-to production-costs.json
```

## CI/CD Integration

### GitHub Actions Integration
```yaml
# .github/workflows/infracost.yml
name: Infracost

on:
  pull_request:
    types: [opened, synchronize]
    paths:
      - 'terraform/**'
      - '.github/workflows/infracost.yml'

env:
  TF_ROOT: terraform/

jobs:
  infracost:
    name: Infracost
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - name: Setup Infracost
        uses: infracost/actions/setup@v2
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      - name: Checkout base branch
        uses: actions/checkout@v3
        with:
          ref: '${{ github.event.pull_request.base.ref }}'

      - name: Generate Infracost cost estimate baseline
        run: |
          infracost breakdown --path=${TF_ROOT} \
                              --format=json \
                              --out-file=/tmp/infracost-base.json

      - name: Checkout PR branch
        uses: actions/checkout@v3

      - name: Generate Infracost diff
        run: |
          infracost diff --path=${TF_ROOT} \
                        --format=json \
                        --compare-to=/tmp/infracost-base.json \
                        --out-file=/tmp/infracost.json

      - name: Post Infracost comment
        run: |
          infracost comment github --path=/tmp/infracost.json \
                                   --repo=$GITHUB_REPOSITORY \
                                   --github-token=${{github.token}} \
                                   --pull-request=${{github.event.pull_request.number}} \
                                   --behavior=update

      - name: Check cost increase
        run: |
          cost_increase=$(jq '.diffTotalMonthlyCost' /tmp/infracost.json | tr -d '"')
          echo "Cost increase: $cost_increase"
          
          # Fail if cost increase is more than $100
          if (( $(echo "$cost_increase > 100" | bc -l) )); then
            echo "::error::Cost increase of $${cost_increase} exceeds $100 threshold"
            exit 1
          fi
```

### GitLab CI Integration
```yaml
# .gitlab-ci.yml
stages:
  - validate
  - plan
  - cost-estimate

variables:
  TF_ROOT: terraform/
  TF_ADDRESS: ${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/terraform/state/production

infracost:
  stage: cost-estimate
  image: infracost/infracost:ci-0.10
  services:
    - docker:dind
  before_script:
    - infracost configure set api_key ${INFRACOST_API_KEY}
  script:
    # Generate cost estimate
    - infracost breakdown --path=${TF_ROOT} --format=json --out-file=infracost.json
    
    # Post comment on merge request
    - |
      if [ "$CI_PIPELINE_SOURCE" = "merge_request_event" ]; then
        infracost comment gitlab --path=infracost.json \
                                --repo=${CI_PROJECT_PATH} \
                                --gitlab-token=${GITLAB_TOKEN} \
                                --merge-request=${CI_MERGE_REQUEST_IID}
      fi
    
    # Check cost thresholds
    - |
      total_cost=$(jq '.totalMonthlyCost' infracost.json | tr -d '"')
      if (( $(echo "$total_cost > 1000" | bc -l) )); then
        echo "Monthly cost of $${total_cost} exceeds $1000 threshold"
        exit 1
      fi
  artifacts:
    reports:
      terraform: infracost.json
    paths:
      - infracost.json
  only:
    refs:
      - merge_requests
      - main
    changes:
      - terraform/**/*
```

### Azure DevOps Integration
```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - terraform/*

pr:
  branches:
    include:
      - main
  paths:
    include:
      - terraform/*

variables:
  TF_ROOT: terraform/

stages:
  - stage: InfracostEstimate
    displayName: 'Infrastructure Cost Estimate'
    jobs:
      - job: Infracost
        displayName: 'Run Infracost'
        pool:
          vmImage: 'ubuntu-latest'
        
        steps:
          - task: Bash@3
            displayName: 'Setup Infracost'
            inputs:
              targetType: 'inline'
              script: |
                curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh
                sudo mv infracost /usr/local/bin/
                infracost configure set api_key $(INFRACOST_API_KEY)

          - task: Bash@3
            displayName: 'Generate Cost Estimate'
            inputs:
              targetType: 'inline'
              script: |
                infracost breakdown --path=$(TF_ROOT) \
                                  --format=json \
                                  --out-file=infracost.json
                
                # Generate table format for display
                infracost breakdown --path=$(TF_ROOT) \
                                  --format=table \
                                  --out-file=infracost-table.txt

          - task: PublishBuildArtifacts@1
            displayName: 'Publish Cost Estimate'
            inputs:
              pathToPublish: 'infracost.json'
              artifactName: 'infracost-estimate'

          - task: Bash@3
            displayName: 'Display Cost Estimate'
            inputs:
              targetType: 'inline'
              script: |
                echo "## Infrastructure Cost Estimate"
                cat infracost-table.txt
                
                # Check if PR and comment
                if [ "$BUILD_REASON" = "PullRequest" ]; then
                  total_cost=$(jq '.totalMonthlyCost' infracost.json | tr -d '"')
                  echo "##vso[task.setvariable variable=TotalMonthlyCost]$total_cost"
                  
                  if (( $(echo "$total_cost > 500" | bc -l) )); then
                    echo "##vso[task.logissue type=warning]Monthly cost of $${total_cost} is approaching budget limits"
                  fi
                fi
```

## Advanced Features

### Cost Policies and Guardrails
```rego
# policies/cost-policies.rego
package infracost

import future.keywords.in

# Deny if monthly cost exceeds budget
deny[msg] {
    monthly_cost := input.projects[_].breakdown.totalMonthlyCost
    monthly_cost > 1000
    msg := sprintf("Monthly cost $%.2f exceeds $1000 budget", [monthly_cost])
}

# Warn about expensive instance types
warn[msg] {
    resource := input.projects[_].breakdown.resources[_]
    resource.name == "aws_instance"
    resource.costComponents[_].name == "Instance usage (Linux/UNIX, on-demand)"
    resource.monthlyCost > 100
    msg := sprintf("Instance %s costs $%.2f/month - consider smaller instance type", [resource.address, resource.monthlyCost])
}

# Require encryption for storage
deny[msg] {
    resource := input.projects[_].breakdown.resources[_]
    resource.name in ["aws_ebs_volume", "aws_s3_bucket"]
    not resource.tags.encrypted
    msg := sprintf("Resource %s must be encrypted", [resource.address])
}

# Warn about unused resources
warn[msg] {
    resource := input.projects[_].breakdown.resources[_]
    resource.monthlyCost > 0
    resource.tags.usage == "unused"
    msg := sprintf("Resource %s appears to be unused but has cost $%.2f/month", [resource.address, resource.monthlyCost])
}

# Environment-specific cost limits
deny[msg] {
    project := input.projects[_]
    project.metadata.terraform_workspace == "production"
    project.breakdown.totalMonthlyCost > 5000
    msg := "Production environment cost exceeds $5000/month limit"
}

warn[msg] {
    project := input.projects[_]
    project.metadata.terraform_workspace == "staging"
    project.breakdown.totalMonthlyCost > 500
    msg := "Staging environment cost exceeds $500/month recommended limit"
}
```

### Custom Resource Pricing
```yaml
# pricing.yml - Custom pricing for private cloud or special rates
apiVersion: v1
kind: ConfigMap
metadata:
  name: infracost-pricing
data:
  custom-pricing.json: |
    {
      "products": [
        {
          "vendorName": "aws",
          "service": "AmazonEC2",
          "productFamily": "Compute Instance",
          "region": "us-west-2",
          "attributes": {
            "instanceType": "t3.custom",
            "tenancy": "Shared",
            "operating-system": "Linux"
          },
          "prices": [
            {
              "USD": "0.05"
            }
          ]
        }
      ]
    }
```

### Cost Optimization Scripts
```python
#!/usr/bin/env python3
"""
Infracost analysis and optimization suggestions
"""

import json
import subprocess
import sys
from typing import Dict, List, Any

class InfracostAnalyzer:
    def __init__(self, terraform_path: str):
        self.terraform_path = terraform_path
        self.cost_data = None
        
    def generate_cost_breakdown(self) -> Dict[str, Any]:
        """Generate Infracost breakdown"""
        try:
            result = subprocess.run([
                'infracost', 'breakdown',
                '--path', self.terraform_path,
                '--format', 'json'
            ], capture_output=True, text=True, check=True)
            
            self.cost_data = json.loads(result.stdout)
            return self.cost_data
            
        except subprocess.CalledProcessError as e:
            print(f"Error running Infracost: {e.stderr}")
            sys.exit(1)
    
    def analyze_expensive_resources(self, threshold: float = 50.0) -> List[Dict[str, Any]]:
        """Find resources costing more than threshold per month"""
        if not self.cost_data:
            self.generate_cost_breakdown()
        
        expensive_resources = []
        
        for project in self.cost_data.get('projects', []):
            for resource in project.get('breakdown', {}).get('resources', []):
                monthly_cost = resource.get('monthlyCost', 0)
                
                if monthly_cost > threshold:
                    expensive_resources.append({
                        'address': resource.get('address'),
                        'name': resource.get('name'),
                        'monthly_cost': monthly_cost,
                        'cost_components': resource.get('costComponents', []),
                        'project': project.get('name')
                    })
        
        return sorted(expensive_resources, key=lambda x: x['monthly_cost'], reverse=True)
    
    def suggest_optimizations(self) -> List[Dict[str, str]]:
        """Suggest cost optimizations"""
        suggestions = []
        expensive_resources = self.analyze_expensive_resources()
        
        for resource in expensive_resources:
            resource_type = resource['name']
            address = resource['address']
            monthly_cost = resource['monthly_cost']
            
            if resource_type == 'aws_instance':
                suggestions.append({
                    'resource': address,
                    'current_cost': f"${monthly_cost:.2f}/month",
                    'suggestion': 'Consider using Reserved Instances for 1-3 year terms to save up to 75%',
                    'priority': 'high' if monthly_cost > 200 else 'medium'
                })
                
                suggestions.append({
                    'resource': address,
                    'current_cost': f"${monthly_cost:.2f}/month",
                    'suggestion': 'Evaluate if smaller instance type meets requirements',
                    'priority': 'medium'
                })
            
            elif resource_type == 'aws_db_instance':
                suggestions.append({
                    'resource': address,
                    'current_cost': f"${monthly_cost:.2f}/month",
                    'suggestion': 'Consider RDS Reserved Instances for predictable workloads',
                    'priority': 'high' if monthly_cost > 100 else 'medium'
                })
            
            elif resource_type == 'aws_nat_gateway':
                suggestions.append({
                    'resource': address,
                    'current_cost': f"${monthly_cost:.2f}/month",
                    'suggestion': 'Consider NAT instances for lower-traffic scenarios',
                    'priority': 'medium'
                })
        
        return suggestions
    
    def compare_environments(self, other_path: str) -> Dict[str, Any]:
        """Compare costs between two environments"""
        try:
            result = subprocess.run([
                'infracost', 'diff',
                '--path', self.terraform_path,
                '--compare-to-path', other_path,
                '--format', 'json'
            ], capture_output=True, text=True, check=True)
            
            return json.loads(result.stdout)
            
        except subprocess.CalledProcessError as e:
            print(f"Error comparing environments: {e.stderr}")
            return {}
    
    def generate_cost_report(self, output_file: str = None):
        """Generate comprehensive cost report"""
        if not self.cost_data:
            self.generate_cost_breakdown()
        
        report_lines = []
        report_lines.append("# Infrastructure Cost Analysis Report\n")
        
        # Summary
        total_monthly_cost = sum(
            project.get('breakdown', {}).get('totalMonthlyCost', 0)
            for project in self.cost_data.get('projects', [])
        )
        
        report_lines.append(f"## Summary")
        report_lines.append(f"- **Total Monthly Cost**: ${total_monthly_cost:.2f}")
        report_lines.append(f"- **Annual Estimate**: ${total_monthly_cost * 12:.2f}")
        report_lines.append("")
        
        # Expensive resources
        expensive_resources = self.analyze_expensive_resources(25.0)
        if expensive_resources:
            report_lines.append("## Top Cost Drivers")
            report_lines.append("| Resource | Type | Monthly Cost |")
            report_lines.append("|----------|------|--------------|")
            
            for resource in expensive_resources[:10]:
                report_lines.append(
                    f"| {resource['address']} | {resource['name']} | ${resource['monthly_cost']:.2f} |"
                )
            report_lines.append("")
        
        # Optimizations
        suggestions = self.suggest_optimizations()
        if suggestions:
            report_lines.append("## Cost Optimization Suggestions")
            
            high_priority = [s for s in suggestions if s['priority'] == 'high']
            medium_priority = [s for s in suggestions if s['priority'] == 'medium']
            
            if high_priority:
                report_lines.append("### High Priority")
                for suggestion in high_priority:
                    report_lines.append(f"- **{suggestion['resource']}** ({suggestion['current_cost']})")
                    report_lines.append(f"  - {suggestion['suggestion']}")
                report_lines.append("")
            
            if medium_priority:
                report_lines.append("### Medium Priority")
                for suggestion in medium_priority:
                    report_lines.append(f"- **{suggestion['resource']}** ({suggestion['current_cost']})")
                    report_lines.append(f"  - {suggestion['suggestion']}")
                report_lines.append("")
        
        # Cost by service
        service_costs = {}
        for project in self.cost_data.get('projects', []):
            for resource in project.get('breakdown', {}).get('resources', []):
                service = resource.get('name', 'unknown')
                monthly_cost = resource.get('monthlyCost', 0)
                
                if service not in service_costs:
                    service_costs[service] = 0
                service_costs[service] += monthly_cost
        
        if service_costs:
            report_lines.append("## Cost by Service")
            report_lines.append("| Service | Monthly Cost | Percentage |")
            report_lines.append("|---------|--------------|------------|")
            
            sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
            for service, cost in sorted_services:
                percentage = (cost / total_monthly_cost) * 100 if total_monthly_cost > 0 else 0
                report_lines.append(f"| {service} | ${cost:.2f} | {percentage:.1f}% |")
        
        report_content = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_content)
            print(f"Cost report saved to {output_file}")
        else:
            print(report_content)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 infracost_analyzer.py <terraform_path> [output_file]")
        sys.exit(1)
    
    terraform_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    analyzer = InfracostAnalyzer(terraform_path)
    analyzer.generate_cost_report(output_file)

if __name__ == '__main__':
    main()
```

### Usage
```bash
# Run cost analysis
python3 infracost_analyzer.py terraform/ cost-report.md

# Compare environments
infracost diff --path terraform/ \
  --terraform-var-file=staging.tfvars \
  --compare-to-path terraform-production/ \
  --format=table

# Check against policies
infracost breakdown --path terraform/ \
  --policy-path policies/ \
  --format=json
```

## Monitoring and Alerting

### Cost Monitoring Dashboard
```python
#!/usr/bin/env python3
"""
Cost monitoring and alerting system
"""

import json
import subprocess
import smtplib
import os
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from datetime import datetime, timedelta
import requests

class CostMonitor:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.smtp_config = self.config.get('smtp', {})
        self.slack_config = self.config.get('slack', {})
        self.thresholds = self.config.get('thresholds', {})
        
    def get_current_costs(self, project_path: str) -> dict:
        """Get current infrastructure costs"""
        try:
            result = subprocess.run([
                'infracost', 'breakdown',
                '--path', project_path,
                '--format', 'json'
            ], capture_output=True, text=True, check=True)
            
            return json.loads(result.stdout)
            
        except subprocess.CalledProcessError as e:
            print(f"Error getting costs: {e.stderr}")
            return {}
    
    def check_cost_thresholds(self, project_path: str) -> list:
        """Check if costs exceed thresholds"""
        cost_data = self.get_current_costs(project_path)
        alerts = []
        
        for project in cost_data.get('projects', []):
            project_name = project.get('name', 'unknown')
            monthly_cost = project.get('breakdown', {}).get('totalMonthlyCost', 0)
            
            # Check project-specific thresholds
            project_thresholds = self.thresholds.get(project_name, {})
            
            # Check monthly threshold
            monthly_threshold = project_thresholds.get('monthly', 
                                                     self.thresholds.get('default_monthly', 1000))
            
            if monthly_cost > monthly_threshold:
                alerts.append({
                    'type': 'monthly_threshold_exceeded',
                    'project': project_name,
                    'current_cost': monthly_cost,
                    'threshold': monthly_threshold,
                    'severity': 'high'
                })
            
            # Check warning threshold (80% of limit)
            warning_threshold = monthly_threshold * 0.8
            if monthly_cost > warning_threshold and monthly_cost <= monthly_threshold:
                alerts.append({
                    'type': 'monthly_threshold_warning',
                    'project': project_name,
                    'current_cost': monthly_cost,
                    'threshold': monthly_threshold,
                    'severity': 'medium'
                })
        
        return alerts
    
    def send_email_alert(self, alerts: list):
        """Send email alerts"""
        if not alerts or not self.smtp_config:
            return
        
        msg = MimeMultipart()
        msg['From'] = self.smtp_config['from']
        msg['To'] = ', '.join(self.smtp_config['to'])
        msg['Subject'] = 'Infrastructure Cost Alert'
        
        body = "Infrastructure Cost Alerts:\n\n"
        
        for alert in alerts:
            body += f"Project: {alert['project']}\n"
            body += f"Alert: {alert['type']}\n"
            body += f"Current Cost: ${alert['current_cost']:.2f}/month\n"
            body += f"Threshold: ${alert['threshold']:.2f}/month\n"
            body += f"Severity: {alert['severity']}\n\n"
        
        msg.attach(MimeText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port'])
            if self.smtp_config.get('use_tls'):
                server.starttls()
            if self.smtp_config.get('username'):
                server.login(self.smtp_config['username'], self.smtp_config['password'])
            
            server.send_message(msg)
            server.quit()
            print("Email alert sent successfully")
            
        except Exception as e:
            print(f"Failed to send email alert: {e}")
    
    def send_slack_alert(self, alerts: list):
        """Send Slack alerts"""
        if not alerts or not self.slack_config.get('webhook_url'):
            return
        
        color_map = {
            'high': 'danger',
            'medium': 'warning',
            'low': 'good'
        }
        
        attachments = []
        
        for alert in alerts:
            color = color_map.get(alert['severity'], 'warning')
            
            attachment = {
                'color': color,
                'title': f"Cost Alert: {alert['project']}",
                'fields': [
                    {
                        'title': 'Alert Type',
                        'value': alert['type'],
                        'short': True
                    },
                    {
                        'title': 'Current Cost',
                        'value': f"${alert['current_cost']:.2f}/month",
                        'short': True
                    },
                    {
                        'title': 'Threshold',
                        'value': f"${alert['threshold']:.2f}/month",
                        'short': True
                    },
                    {
                        'title': 'Severity',
                        'value': alert['severity'],
                        'short': True
                    }
                ],
                'timestamp': datetime.utcnow().isoformat()
            }
            
            attachments.append(attachment)
        
        payload = {
            'text': 'Infrastructure Cost Alerts',
            'attachments': attachments
        }
        
        try:
            response = requests.post(self.slack_config['webhook_url'], json=payload)
            response.raise_for_status()
            print("Slack alert sent successfully")
            
        except requests.RequestException as e:
            print(f"Failed to send Slack alert: {e}")
    
    def run_monitoring(self, project_paths: list):
        """Run cost monitoring for all projects"""
        all_alerts = []
        
        for project_path in project_paths:
            alerts = self.check_cost_thresholds(project_path)
            all_alerts.extend(alerts)
        
        if all_alerts:
            print(f"Found {len(all_alerts)} cost alerts")
            
            self.send_email_alert(all_alerts)
            self.send_slack_alert(all_alerts)
        else:
            print("No cost alerts found")

# Configuration file example
config_example = {
    "smtp": {
        "host": "smtp.gmail.com",
        "port": 587,
        "use_tls": True,
        "username": "alerts@company.com",
        "password": "app_password",
        "from": "alerts@company.com",
        "to": ["devops@company.com", "finance@company.com"]
    },
    "slack": {
        "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    },
    "thresholds": {
        "production-infrastructure": {
            "monthly": 2000
        },
        "staging-infrastructure": {
            "monthly": 500
        },
        "default_monthly": 1000
    }
}

# Usage
if __name__ == '__main__':
    monitor = CostMonitor('cost-monitor-config.json')
    project_paths = [
        'terraform/environments/production',
        'terraform/environments/staging'
    ]
    monitor.run_monitoring(project_paths)
```

## Best Practices

### Cost Optimization Strategies
```bash
# 1. Regular cost reviews
# Run weekly cost analysis
infracost breakdown --path terraform/ --format=table > weekly-costs.txt

# Compare with previous week
infracost diff --path terraform/ --compare-to last-week-costs.json

# 2. Environment-specific configurations
# Use smaller instances for non-production
# staging.tfvars
instance_type = "t3.small"
storage_size = 20

# production.tfvars
instance_type = "t3.large" 
storage_size = 100

# 3. Reserved Instance analysis
# Check which resources would benefit from reserved instances
infracost breakdown --path terraform/ --format=json | \
  jq '.projects[].breakdown.resources[] | select(.name == "aws_instance") | {address, monthlyCost}'

# 4. Unused resource detection
# Tag resources for tracking
resource "aws_instance" "web" {
  # ... configuration ...
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    Usage       = "active"  # active, testing, unused
    Owner       = "team-platform"
    CostCenter  = "engineering"
  }
}
```

### Integration with FinOps
```python
# finops-integration.py
"""
FinOps integration for cost management
"""

class FinOpsIntegration:
    def __init__(self):
        self.cost_allocation_tags = [
            'Environment',
            'Project', 
            'Team',
            'CostCenter',
            'Owner'
        ]
    
    def validate_cost_allocation_tags(self, terraform_plan):
        """Validate that resources have proper cost allocation tags"""
        missing_tags = []
        
        for resource in terraform_plan.get('planned_values', {}).get('root_module', {}).get('resources', []):
            resource_tags = resource.get('values', {}).get('tags', {})
            
            for required_tag in self.cost_allocation_tags:
                if required_tag not in resource_tags:
                    missing_tags.append({
                        'resource': resource.get('address'),
                        'missing_tag': required_tag
                    })
        
        return missing_tags
    
    def generate_cost_allocation_report(self, cost_data):
        """Generate cost allocation report by tags"""
        allocation = {}
        
        for project in cost_data.get('projects', []):
            for resource in project.get('breakdown', {}).get('resources', []):
                tags = resource.get('tags', {})
                monthly_cost = resource.get('monthlyCost', 0)
                
                # Allocate by cost center
                cost_center = tags.get('CostCenter', 'unallocated')
                if cost_center not in allocation:
                    allocation[cost_center] = {
                        'total_cost': 0,
                        'resources': 0,
                        'projects': set()
                    }
                
                allocation[cost_center]['total_cost'] += monthly_cost
                allocation[cost_center]['resources'] += 1
                allocation[cost_center]['projects'].add(project.get('name'))
        
        return allocation
```

## Resources

- [Infracost Documentation](https://www.infracost.io/docs/) - Official Infracost documentation
- [Infracost GitHub Repository](https://github.com/infracost/infracost) - Source code and examples
- [Terraform Cost Estimation](https://www.terraform.io/docs/cloud/cost-estimation/) - Terraform Cloud cost estimation
- [AWS Pricing Calculator](https://calculator.aws/) - AWS pricing reference
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) - Azure pricing reference
- [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator) - GCP pricing reference
- [FinOps Foundation](https://www.finops.org/) - Cloud financial management best practices
- [Cloud Cost Optimization](https://aws.amazon.com/aws-cost-management/) - AWS cost management tools
- [Infrastructure Cost Management](https://cloud.google.com/cost-management) - Google Cloud cost management
- [Open Policy Agent](https://www.openpolicyagent.org/) - Policy engine for cost governance