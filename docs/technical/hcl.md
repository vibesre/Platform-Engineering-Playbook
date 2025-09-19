# HCL

HCL (HashiCorp Configuration Language) is a configuration language designed to be both human and machine-friendly. It's the primary configuration language for HashiCorp tools like Terraform, Consul, Nomad, and Vault, making it essential for infrastructure as code and platform engineering.

## Overview

HCL is widely used in platform engineering for:
- Infrastructure as Code (Terraform)
- Service discovery and configuration (Consul)
- Container orchestration (Nomad)
- Secrets management (Vault)
- Policy as Code (Sentinel)

## Key Features

- **Human-Readable**: Clear, intuitive syntax similar to JSON
- **Machine-Friendly**: Easy to parse and generate programmatically
- **Native Comments**: Supports both line and block comments
- **Interpolation**: Dynamic value substitution
- **Hierarchical**: Supports nested blocks and attributes
- **Type System**: Strong typing with validation

## Basic Syntax

### Attributes and Blocks
```hcl
# Basic attributes
name = "web-server"
port = 8080
enabled = true
tags = ["web", "production"]

# Blocks
resource "aws_instance" "web" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  
  # Nested blocks
  vpc_security_group_ids = [aws_security_group.web.id]
  
  tags = {
    Name        = "WebServer"
    Environment = "production"
  }
}

# Block with labels
variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 1
}
```

### Data Types
```hcl
# Primitive types
string_value = "hello world"
number_value = 42
bool_value   = true

# Collections
list_example = ["item1", "item2", "item3"]
map_example = {
  key1 = "value1"
  key2 = "value2"
}

# Complex objects
server_config = {
  name = "web-01"
  spec = {
    cpu    = 2
    memory = "4GB"
    disk   = "20GB"
  }
  networks = ["public", "private"]
}
```

### Comments and Expressions
```hcl
# Line comment
variable "region" {
  description = "AWS region" # Inline comment
  type        = string
  default     = "us-west-2"
}

/*
Block comment
Multiple lines
*/

# String interpolation
name = "server-${var.environment}-${var.region}"

# Conditional expressions
instance_type = var.environment == "production" ? "t3.large" : "t2.micro"

# Function calls
availability_zones = slice(data.aws_availability_zones.available.names, 0, 2)
```

## Platform Engineering Use Cases

### Terraform Infrastructure
```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "infrastructure/terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# Variables
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be one of: dev, staging, production."
  }
}

variable "instance_specs" {
  description = "Instance specifications by environment"
  type = map(object({
    instance_type = string
    min_size      = number
    max_size      = number
    desired_size  = number
  }))
  default = {
    dev = {
      instance_type = "t3.micro"
      min_size      = 1
      max_size      = 2
      desired_size  = 1
    }
    staging = {
      instance_type = "t3.small"
      min_size      = 1
      max_size      = 3
      desired_size  = 2
    }
    production = {
      instance_type = "t3.medium"
      min_size      = 2
      max_size      = 10
      desired_size  = 3
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# VPC Configuration
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_subnet" "public" {
  count = 2
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.project_name}-public-${count.index + 1}"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count = 2
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name = "${var.project_name}-private-${count.index + 1}"
    Type = "private"
  }
}

# Security Groups
resource "aws_security_group" "web" {
  name_prefix = "${var.project_name}-web-"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    description = "HTTPS"
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
    Name = "${var.project_name}-web-sg"
  }
  
  lifecycle {
    create_before_destroy = true
  }
}

# Launch Template
resource "aws_launch_template" "web" {
  name_prefix   = "${var.project_name}-web-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_specs[var.environment].instance_type
  
  vpc_security_group_ids = [aws_security_group.web.id]
  
  user_data = base64encode(templatefile("${path.module}/userdata.sh", {
    environment = var.environment
    project     = var.project_name
  }))
  
  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.project_name}-web-instance"
    }
  }
  
  lifecycle {
    create_before_destroy = true
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "web" {
  name                = "${var.project_name}-web-asg"
  vpc_zone_identifier = aws_subnet.public[*].id
  target_group_arns   = [aws_lb_target_group.web.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300
  
  min_size         = var.instance_specs[var.environment].min_size
  max_size         = var.instance_specs[var.environment].max_size
  desired_capacity = var.instance_specs[var.environment].desired_size
  
  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Name"
    value               = "${var.project_name}-web-asg"
    propagate_at_launch = false
  }
  
  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 50
    }
  }
}

# Load Balancer
resource "aws_lb" "web" {
  name               = "${var.project_name}-web-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web.id]
  subnets            = aws_subnet.public[*].id
  
  enable_deletion_protection = var.environment == "production"
  
  tags = {
    Name = "${var.project_name}-web-lb"
  }
}

resource "aws_lb_target_group" "web" {
  name     = "${var.project_name}-web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
  
  tags = {
    Name = "${var.project_name}-web-tg"
  }
}

resource "aws_lb_listener" "web" {
  load_balancer_arn = aws_lb.web.arn
  port              = "80"
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

# Outputs
output "load_balancer_dns" {
  description = "DNS name of the load balancer"
  value       = aws_lb.web.dns_name
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}
```

### Consul Configuration
```hcl
# Consul server configuration
datacenter = "dc1"
data_dir   = "/opt/consul/data"
log_level  = "INFO"
node_name  = "consul-server-1"
bind_addr  = "0.0.0.0"

# Server configuration
server = true
bootstrap_expect = 3

# Networking
client_addr = "0.0.0.0"
ui_config {
  enabled = true
}

# Connect service mesh
connect {
  enabled = true
}

# ACL configuration
acl = {
  enabled        = true
  default_policy = "deny"
  enable_token_persistence = true
}

# Service definitions
services {
  name = "web"
  tags = ["production", "v1"]
  port = 8080
  
  check {
    http     = "http://localhost:8080/health"
    interval = "10s"
    timeout  = "3s"
  }
  
  connect {
    sidecar_service {
      proxy {
        upstreams {
          destination_name = "database"
          local_bind_port  = 5432
        }
      }
    }
  }
}

services {
  name = "database"
  tags = ["postgresql", "primary"]
  port = 5432
  
  check {
    tcp      = "localhost:5432"
    interval = "10s"
    timeout  = "3s"
  }
}
```

### Nomad Job Specification
```hcl
job "web-app" {
  datacenters = ["dc1"]
  type        = "service"
  
  update {
    max_parallel      = 2
    min_healthy_time  = "10s"
    healthy_deadline  = "3m"
    progress_deadline = "10m"
    auto_revert       = true
    canary            = 1
  }
  
  group "web" {
    count = 3
    
    network {
      port "http" {
        static = 8080
      }
    }
    
    service {
      name = "web-app"
      port = "http"
      tags = [
        "production",
        "traefik.enable=true",
        "traefik.http.routers.web-app.rule=Host(`app.example.com`)"
      ]
      
      check {
        type     = "http"
        path     = "/health"
        interval = "10s"
        timeout  = "2s"
      }
    }
    
    restart {
      attempts = 3
      interval = "30m"
      delay    = "15s"
      mode     = "fail"
    }
    
    task "web" {
      driver = "docker"
      
      config {
        image = "nginx:1.21"
        ports = ["http"]
        
        volumes = [
          "local:/usr/share/nginx/html"
        ]
      }
      
      template {
        data = <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>{{ env "NOMAD_JOB_NAME" }}</title>
</head>
<body>
    <h1>Hello from {{ env "NOMAD_ALLOC_ID" }}</h1>
    <p>Job: {{ env "NOMAD_JOB_NAME" }}</p>
    <p>Task: {{ env "NOMAD_TASK_NAME" }}</p>
    <p>Version: {{ key "config/app/version" }}</p>
</body>
</html>
EOF
        destination = "local/index.html"
      }
      
      env {
        LOG_LEVEL = "info"
        PORT      = "${NOMAD_PORT_http}"
      }
      
      resources {
        cpu    = 256
        memory = 256
      }
    }
  }
}
```

### Vault Configuration
```hcl
# Storage backend
storage "consul" {
  address = "127.0.0.1:8500"
  path    = "vault/"
}

# Network configuration
listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = 1
}

# UI configuration
ui = true

# API address
api_addr = "http://127.0.0.1:8200"

# Cluster configuration
cluster_addr = "https://127.0.0.1:8201"

# Telemetry
telemetry {
  prometheus_retention_time = "30s"
  disable_hostname = true
}

# Seal configuration (auto-unseal with cloud KMS)
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "12345678-1234-1234-1234-123456789012"
}

# Plugin directory
plugin_directory = "/etc/vault/plugins"
```

## Advanced Features

### Functions and Expressions
```hcl
locals {
  # String functions
  server_name = lower(replace(var.name, "_", "-"))
  
  # Collection functions
  subnet_cidrs = [for i in range(var.subnet_count) : 
    cidrsubnet(var.vpc_cidr, 8, i)
  ]
  
  # Conditional logic
  instance_type = var.environment == "production" ? 
    var.production_instance_type : 
    var.dev_instance_type
  
  # Map transformation
  server_configs = {
    for name, config in var.servers : name => {
      name         = name
      instance_type = config.instance_type
      tags = merge(config.tags, {
        Environment = var.environment
        Project     = var.project_name
      })
    }
  }
  
  # Complex expressions
  availability_zones = slice(
    sort(data.aws_availability_zones.available.names),
    0,
    min(length(data.aws_availability_zones.available.names), 3)
  )
}
```

### Dynamic Blocks
```hcl
resource "aws_security_group" "web" {
  name_prefix = "web-"
  vpc_id      = aws_vpc.main.id
  
  # Dynamic ingress rules
  dynamic "ingress" {
    for_each = var.allowed_ports
    content {
      description = ingress.value.description
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
  
  # Dynamic tags
  dynamic "tags" {
    for_each = var.enable_detailed_tags ? var.detailed_tags : {}
    content {
      key                 = tags.key
      value               = tags.value
      propagate_at_launch = true
    }
  }
}
```

### Modules
```hcl
# Module definition (modules/vpc/main.tf)
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "public_subnets" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
}

variable "private_subnets" {
  description = "List of private subnet CIDR blocks"
  type        = list(string)
}

# Module usage
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets    = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
}

module "database" {
  source = "terraform-aws-modules/rds/aws"
  
  identifier = "${var.project_name}-db"
  
  engine            = "postgres"
  engine_version    = "14.9"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  
  db_name  = var.database_name
  username = var.database_username
  password = var.database_password
  
  vpc_security_group_ids = [module.vpc.database_security_group_id]
  
  tags = local.common_tags
}
```

## Working with HCL

### Validation and Formatting
```bash
# Terraform commands
terraform fmt      # Format HCL files
terraform validate # Validate configuration
terraform plan     # Show execution plan
terraform apply    # Apply changes

# HCL-specific tools
hclfmt file.hcl    # Format HCL file
hclpack file.hcl   # Pack HCL into JSON
```

### Configuration Management
```hcl
# terraform.tfvars
project_name = "my-web-app"
environment  = "production"
region      = "us-west-2"

instance_specs = {
  production = {
    instance_type = "t3.medium"
    min_size      = 2
    max_size      = 10
    desired_size  = 3
  }
}

# Environment-specific configurations
# environments/production.tfvars
database_instance_class = "db.r5.large"
enable_backups         = true
backup_retention_days  = 30
multi_az              = true

# environments/development.tfvars
database_instance_class = "db.t3.micro"
enable_backups         = false
backup_retention_days  = 7
multi_az              = false
```

## Best Practices

### Code Organization
```hcl
# Good: Organized by resource type
# main.tf - Primary resources
# variables.tf - Input variables
# outputs.tf - Output values
# versions.tf - Provider requirements
# locals.tf - Local values

# Good: Clear variable definitions
variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

# Good: Meaningful resource names
resource "aws_instance" "web_server" {
  # Configuration
}

resource "aws_security_group" "web_server_sg" {
  # Configuration
}
```

### State Management
```hcl
# Remote state configuration
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}

# Data source for remote state
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "vpc/terraform.tfstate"
    region = "us-west-2"
  }
}
```

## Common Pitfalls

### Resource Dependencies
```hcl
# Wrong: Implicit dependency may not work
resource "aws_instance" "web" {
  subnet_id = aws_subnet.public.id  # May be created in wrong order
}

# Right: Explicit dependency
resource "aws_instance" "web" {
  subnet_id = aws_subnet.public.id
  
  depends_on = [aws_internet_gateway.main]
}
```

### State Drift
```hcl
# Good: Use lifecycle rules to prevent destruction
resource "aws_instance" "database" {
  # Configuration
  
  lifecycle {
    prevent_destroy = true
    ignore_changes  = [ami]
  }
}
```

## Tools and Integration

### IDE Support
```bash
# VS Code extensions
# - HashiCorp Terraform
# - HCL syntax highlighting

# Vim plugins
# - vim-terraform
# - vim-hcl
```

### CI/CD Integration
```hcl
# GitHub Actions workflow
name: Terraform
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: hashicorp/setup-terraform@v2
    - run: terraform fmt -check
    - run: terraform init
    - run: terraform validate
    - run: terraform plan
```

## Resources

- [HCL Official Documentation](https://github.com/hashicorp/hcl) - HashiCorp Configuration Language specification
- [Terraform Language Reference](https://developer.hashicorp.com/terraform/language) - Complete Terraform HCL guide
- [Consul Configuration Reference](https://developer.hashicorp.com/consul/docs/agent/config) - Consul HCL configuration
- [Nomad Job Specification](https://developer.hashicorp.com/nomad/docs/job-specification) - Nomad HCL job syntax
- [Vault Configuration](https://developer.hashicorp.com/vault/docs/configuration) - Vault HCL configuration reference
- [Terraform Best Practices](https://www.terraform-best-practices.com/) - Community best practices guide
- [HCL Parser](https://pkg.go.dev/github.com/hashicorp/hcl/v2) - Go library for parsing HCL
- [Terragrunt](https://terragrunt.gruntwork.io/) - Terraform wrapper for DRY configurations
- [Terraform Registry](https://registry.terraform.io/) - Official Terraform provider and module registry
- [HCL Language Server](https://github.com/hashicorp/terraform-ls) - Language server for editor integration