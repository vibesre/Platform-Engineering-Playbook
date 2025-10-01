---
title: "Packer - Machine Image Automation"
description: "Master Packer for image automation: build consistent machine images for AWS, Azure, GCP, and VMware. Automate AMI, VM, and container image creation workflows."
keywords:
  - Packer
  - machine images
  - image automation
  - HashiCorp Packer
  - AMI creation
  - VM images
  - Packer tutorial
  - infrastructure automation
  - image building
  - cloud images
  - golden images
  - immutable infrastructure
---

# Packer

<GitHubButtons />
## 📚 Learning Resources

### 📖 Essential Documentation
- [Packer Documentation](https://www.packer.io/docs) - Official comprehensive documentation
- [Builder Reference](https://www.packer.io/docs/builders) - Complete builder documentation for all platforms
- [Provisioner Guide](https://www.packer.io/docs/provisioners) - Configuration management and setup tools
- [Post-Processor Reference](https://www.packer.io/docs/post-processors) - Image optimization and distribution

### 📝 Specialized Guides
- [Packer Best Practices](https://www.packer.io/guides/packer-on-cicd) - CI/CD integration and production patterns
- [HCL2 Templates](https://www.packer.io/guides/hcl) - Modern template syntax and features
- [Multi-Cloud Images](https://learn.hashicorp.com/collections/packer/cloud-production) - Building consistent images across providers
- [Image Testing](https://www.packer.io/docs/provisioners/inspec) - Validation and compliance testing

### 🎥 Video Tutorials
- [Packer Crash Course](https://www.youtube.com/watch?v=videoid) - Getting started with image building (30 min)
- [Advanced Packer Techniques](https://www.youtube.com/watch?v=videoid2) - Production patterns and optimization (45 min)
- [Multi-Cloud with Packer](https://www.youtube.com/watch?v=videoid3) - Cross-platform image strategies (35 min)

### 🎓 Professional Courses
- [HashiCorp Packer](https://learn.hashicorp.com/packer) - Free official tutorials and learning paths
- [Infrastructure as Code](https://www.pluralsight.com/courses/packer-getting-started) - Paid Pluralsight course
- [DevOps Automation](https://acloudguru.com/course/hashicorp-packer) - Paid comprehensive course

### 📚 Books
- "Infrastructure as Code" by Kief Morris - [Purchase on Amazon](https://www.amazon.com/dp/1491924357)
- "Terraform: Up and Running" by Yevgeniy Brikman - [Purchase on Amazon](https://www.amazon.com/dp/1492046906) (includes Packer)
- "Learning DevOps" by Mikael Krief - [Purchase on Amazon](https://www.amazon.com/dp/1838642722)

### 🛠️ Interactive Tools
- [Packer Playground](https://learn.hashicorp.com/tutorials/packer/aws-get-started-build-image) - Hands-on tutorials
- [HCL2 Syntax Highlighting](https://marketplace.visualstudio.com/items?itemName=HashiCorp.HCL) - VS Code extension
- [Packer Validate](https://www.packer.io/docs/commands/validate) - Template validation tools

### 🚀 Ecosystem Tools
- [Ansible](https://docs.ansible.com/ansible/latest/scenario_guides/guide_packer.html) - Configuration management integration
- [Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/ami) - Infrastructure provisioning with custom AMIs
- [InSpec](https://www.inspec.io/) - Infrastructure testing and compliance
- [Vault](https://www.vaultproject.io/docs/secrets/aws) - Secrets management for builds

### 🌐 Community & Support
- [Packer Community](https://discuss.hashicorp.com/c/packer/23) - Official community discussions
- [Packer GitHub](https://github.com/hashicorp/packer) - 15k⭐ Source code and issues
- [HashiCorp Learn](https://learn.hashicorp.com/packer) - Official tutorials and guides

## Understanding Packer: Universal Machine Image Builder

Packer is an open-source tool by HashiCorp that automates the creation of identical machine images for multiple platforms from a single source configuration. It enables teams to build production-ready AMIs, Docker containers, Vagrant boxes, and images for various cloud providers using a declarative approach.

### How Packer Works
Packer operates by launching temporary instances, configuring them according to your specifications, and then creating machine images from the configured instances. The process is completely automated and repeatable, ensuring consistent images across different environments and platforms.

The tool uses builders to launch instances on various platforms, provisioners to configure the instances, and post-processors to optimize and distribute the final images. This pipeline approach makes it easy to create complex, multi-step image building workflows.

### The Packer Ecosystem
Packer's ecosystem includes builders for all major cloud platforms (AWS, Azure, GCP), virtualization platforms (VMware, VirtualBox), and container runtimes (Docker). Provisioners integrate with configuration management tools like Ansible, Chef, and Puppet, while post-processors handle image optimization and distribution.

The ecosystem extends through plugins, custom builders, and integrations with CI/CD pipelines. HashiCorp's broader ecosystem means Packer works seamlessly with Terraform for infrastructure provisioning and Vault for secrets management.

### Why Packer Dominates Image Building
Packer has become the standard for automated image building due to its platform-agnostic approach and declarative configuration. Instead of maintaining separate image building processes for each platform, teams can use a single Packer template to build images everywhere.

The immutable infrastructure pattern that Packer enables reduces configuration drift and improves deployment reliability. By baking configuration into images rather than applying it at runtime, applications start faster and more consistently.

### Mental Model for Success
Think of Packer like a factory assembly line for machine images. You provide the blueprint (template), raw materials (base images), and assembly instructions (provisioners), and Packer produces identical finished products (machine images) for different platforms.

Just like a factory can produce the same product for different markets with slight variations, Packer can create platform-specific images from the same source configuration while respecting platform differences.

### Where to Start Your Journey
1. **Install Packer locally** - Start with the CLI and simple templates
2. **Build your first AMI** - Follow the AWS getting started guide
3. **Add provisioning** - Use shell scripts to configure your images
4. **Try multiple platforms** - Build the same image for different clouds
5. **Integrate with CI/CD** - Automate image building in your pipeline
6. **Add testing** - Validate images before deployment

### Key Concepts to Master
- **Template syntax** - HCL2 configuration and variable management
- **Builder selection** - Choosing the right builder for each platform
- **Provisioning strategies** - Configuration management integration
- **Image optimization** - Size reduction and security hardening
- **Testing and validation** - Ensuring image quality and compliance
- **CI/CD integration** - Automating image builds and distribution
- **Multi-platform builds** - Consistent images across different platforms
- **Security considerations** - Secrets management and secure image building

Start with simple single-platform builds and gradually expand to multi-platform scenarios. Focus on establishing good practices around testing and validation early in your learning journey.

## Architecture

### Core Components

1. **Packer Core Engine**
   - Template parser and validator
   - Build orchestrator
   - Plugin architecture
   - Parallel build execution
   - Post-processor pipeline

2. **Builders**
   - Cloud builders (AWS, Azure, GCP, Digital Ocean)
   - Virtualization builders (VMware, VirtualBox, QEMU)
   - Container builders (Docker, Podman)
   - Bare metal builders (Raspberry Pi, ARM)

3. **Provisioners**
   - Shell scripts
   - Configuration management (Ansible, Chef, Puppet)
   - File uploads
   - PowerShell
   - Windows updates

4. **Post-Processors**
   - Image compression
   - Upload to repositories
   - Image conversion
   - Manifest generation
   - Checksums

## Language Support

### HCL2 (HashiCorp Configuration Language)
```hcl
# Modern Packer template using HCL2
packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
    ansible = {
      version = ">= 1.1.0"
      source  = "github.com/hashicorp/ansible"
    }
  }
}

# Input variables
variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for AMI creation"
}

variable "instance_type" {
  type        = string
  default     = "t3.medium"
  description = "Instance type for building"
}

variable "app_version" {
  type        = string
  description = "Application version to embed in image"
}

variable "base_ami_filter" {
  type = object({
    owners      = list(string)
    name_filter = string
  })
  default = {
    owners      = ["099720109477"] # Canonical
    name_filter = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
  }
}

# Local variables
locals {
  timestamp = regex_replace(timestamp(), "[- TZ:]", "")
  ami_name  = "app-${var.app_version}-${local.timestamp}"
  
  common_tags = {
    Name          = local.ami_name
    BuildDate     = timestamp()
    BuildTool     = "Packer"
    AppVersion    = var.app_version
    BaseOS        = "Ubuntu 22.04"
    ManagedBy     = "Platform Team"
  }
}

# Data source for base AMI
data "amazon-ami" "ubuntu" {
  filters = {
    name                = var.base_ami_filter.name_filter
    root-device-type    = "ebs"
    virtualization-type = "hvm"
  }
  most_recent = true
  owners      = var.base_ami_filter.owners
  region      = var.aws_region
}

# Source block for AWS AMI builder
source "amazon-ebs" "main" {
  ami_name      = local.ami_name
  instance_type = var.instance_type
  region        = var.aws_region
  
  source_ami   = data.amazon-ami.ubuntu.id
  ssh_username = "ubuntu"
  
  # Enhanced networking and storage
  ena_support          = true
  sriov_support        = true
  ebs_optimized        = true
  
  # Root volume configuration
  launch_block_device_mappings {
    device_name           = "/dev/sda1"
    volume_size           = 30
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
    iops                  = 3000
    throughput            = 125
  }
  
  # Additional data volume
  launch_block_device_mappings {
    device_name           = "/dev/sdf"
    volume_size           = 100
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }
  
  # VPC configuration for build
  vpc_filter {
    filters = {
      "tag:Name" : "packer-build-vpc"
      "state" : "available"
    }
  }
  
  subnet_filter {
    filters = {
      "tag:Name" : "packer-build-subnet"
      "state" : "available"
    }
    most_free = true
    random    = false
  }
  
  # Security group configuration
  security_group_filter {
    filters = {
      "tag:Name" : "packer-build-sg"
    }
  }
  
  # AMI configuration
  ami_description = "Application AMI version ${var.app_version}"
  ami_virtualization_type = "hvm"
  
  # Copy to multiple regions
  ami_regions = [
    "us-west-2",
    "eu-west-1"
  ]
  
  # Sharing configuration
  ami_users = []  # AWS account IDs to share with
  ami_groups = [] # "all" for public
  
  # Tags
  tags = local.common_tags
  run_tags = merge(local.common_tags, {
    Purpose = "Packer Build"
  })
  
  # Metadata options
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
}

# Build block
build {
  name = "application-ami"
  sources = [
    "source.amazon-ebs.main"
  ]
  
  # Update system
  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get upgrade -y",
      "sudo apt-get install -y software-properties-common"
    ]
  }
  
  # Install base dependencies
  provisioner "shell" {
    script = "scripts/install-dependencies.sh"
    environment_vars = [
      "APP_VERSION=${var.app_version}",
      "DEBIAN_FRONTEND=noninteractive"
    ]
  }
  
  # Configure system
  provisioner "ansible" {
    playbook_file = "ansible/playbook.yml"
    user          = "ubuntu"
    extra_arguments = [
      "--extra-vars", "app_version=${var.app_version}",
      "--tags", "image-build"
    ]
  }
  
  # Upload application files
  provisioner "file" {
    source      = "app/"
    destination = "/tmp/app"
  }
  
  # Install application
  provisioner "shell" {
    scripts = [
      "scripts/install-app.sh",
      "scripts/configure-app.sh"
    ]
    environment_vars = [
      "APP_DIR=/opt/application",
      "APP_USER=appuser"
    ]
  }
  
  # Security hardening
  provisioner "shell" {
    script = "scripts/security-hardening.sh"
    execute_command = "chmod +x {{ .Path }}; {{ .Vars }} sudo -E bash '{{ .Path }}'"
  }
  
  # Cleanup
  provisioner "shell" {
    inline = [
      "sudo apt-get autoremove -y",
      "sudo apt-get clean",
      "sudo rm -rf /var/lib/apt/lists/*",
      "sudo rm -rf /tmp/*",
      "sudo rm -rf /var/tmp/*",
      "history -c",
      "cat /dev/null > ~/.bash_history"
    ]
  }
  
  # Generate manifest
  post-processor "manifest" {
    output = "manifest.json"
    strip_path = true
    custom_data = {
      app_version = var.app_version
      build_time  = timestamp()
      git_commit  = env("GIT_COMMIT")
    }
  }
  
  # Create AMI changelog
  post-processor "shell-local" {
    inline = [
      "echo 'AMI ${local.ami_name} created successfully' >> build.log",
      "jq -r '.builds[0].artifact_id' manifest.json | cut -d':' -f2 >> ami-ids.txt"
    ]
  }
  
  # Notify completion
  post-processor "shell-local" {
    inline = [
      "curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \\",
      "  -H 'Content-Type: application/json' \\",
      "  -d '{\"text\": \"AMI ${local.ami_name} built successfully in ${var.aws_region}\"}'"
    ]
    only = ["amazon-ebs.main"]
  }
}
```

### JSON Template Format
```json
{
  "variables": {
    "aws_access_key": "{{env `AWS_ACCESS_KEY_ID`}}",
    "aws_secret_key": "{{env `AWS_SECRET_ACCESS_KEY`}}",
    "region": "us-east-1",
    "source_ami": "ami-0c02fb55956c7d316",
    "instance_type": "t3.medium",
    "ssh_username": "ec2-user",
    "ami_name": "custom-app-{{timestamp}}"
  },
  
  "builders": [
    {
      "type": "amazon-ebs",
      "access_key": "{{user `aws_access_key`}}",
      "secret_key": "{{user `aws_secret_key`}}",
      "region": "{{user `region`}}",
      "source_ami": "{{user `source_ami`}}",
      "instance_type": "{{user `instance_type`}}",
      "ssh_username": "{{user `ssh_username`}}",
      "ami_name": "{{user `ami_name`}}",
      "ami_description": "Custom application AMI",
      "tags": {
        "Name": "{{user `ami_name`}}",
        "BuildDate": "{{isotime \"2006-01-02\"}}",
        "BuildTool": "Packer"
      }
    }
  ],
  
  "provisioners": [
    {
      "type": "shell",
      "inline": [
        "sudo yum update -y",
        "sudo yum install -y docker"
      ]
    },
    {
      "type": "file",
      "source": "./app",
      "destination": "/tmp/app"
    },
    {
      "type": "shell",
      "script": "scripts/install.sh"
    }
  ],
  
  "post-processors": [
    {
      "type": "manifest",
      "output": "manifest.json",
      "strip_path": true
    }
  ]
}
```

## Practical Examples

### Multi-Cloud Golden Image Pipeline
```hcl
# Multi-cloud configuration for consistent base images
packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
    azure = {
      version = ">= 1.1.4"
      source  = "github.com/hashicorp/azure"
    }
    googlecompute = {
      version = ">= 1.1.1"
      source  = "github.com/hashicorp/googlecompute"
    }
  }
}

# Shared variables
variable "os_version" {
  type    = string
  default = "ubuntu-22.04"
}

variable "build_version" {
  type        = string
  description = "Version tag for this build"
}

locals {
  build_timestamp = regex_replace(timestamp(), "[- TZ:]", "")
  image_name      = "golden-${var.os_version}-v${var.build_version}-${local.build_timestamp}"
  
  # Common provisioning scripts
  common_scripts = [
    "scripts/base/update-system.sh",
    "scripts/base/install-tools.sh",
    "scripts/base/configure-users.sh",
    "scripts/base/security-hardening.sh"
  ]
}

# AWS AMI Source
source "amazon-ebs" "ubuntu" {
  ami_name      = "aws-${local.image_name}"
  instance_type = "t3.large"
  region        = "us-east-1"
  
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }
  
  ssh_username = "ubuntu"
  
  launch_block_device_mappings {
    device_name           = "/dev/sda1"
    volume_size           = 50
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }
  
  ami_regions = ["us-west-2", "eu-west-1", "ap-southeast-1"]
  
  tags = {
    Name         = "aws-${local.image_name}"
    OS           = var.os_version
    BuildVersion = var.build_version
    BuildDate    = timestamp()
    Builder      = "Packer"
  }
}

# Azure Managed Image Source
source "azure-arm" "ubuntu" {
  client_id       = env("AZURE_CLIENT_ID")
  client_secret   = env("AZURE_CLIENT_SECRET")
  subscription_id = env("AZURE_SUBSCRIPTION_ID")
  tenant_id       = env("AZURE_TENANT_ID")
  
  managed_image_name                = "azure-${local.image_name}"
  managed_image_resource_group_name = "packer-images-rg"
  
  os_type         = "Linux"
  image_publisher = "Canonical"
  image_offer     = "0001-com-ubuntu-server-jammy"
  image_sku       = "22_04-lts-gen2"
  
  azure_tags = {
    Name         = "azure-${local.image_name}"
    OS           = var.os_version
    BuildVersion = var.build_version
    BuildDate    = timestamp()
    Builder      = "Packer"
  }
  
  location = "East US"
  vm_size  = "Standard_D2s_v3"
  
  # Shared Image Gallery destination
  shared_image_gallery_destination {
    subscription         = env("AZURE_SUBSCRIPTION_ID")
    resource_group       = "shared-images-rg"
    gallery_name         = "company_images"
    image_name           = "ubuntu-22-04-golden"
    image_version        = var.build_version
    replication_regions  = ["East US", "West Europe", "Southeast Asia"]
    storage_account_type = "Standard_LRS"
  }
}

# GCP Image Source
source "googlecompute" "ubuntu" {
  project_id   = env("GCP_PROJECT_ID")
  source_image_family = "ubuntu-2204-lts"
  image_name   = "gcp-${local.image_name}"
  image_family = "golden-images"
  
  zone         = "us-central1-a"
  machine_type = "n1-standard-2"
  
  disk_size = 50
  disk_type = "pd-ssd"
  
  ssh_username = "packer"
  
  image_labels = {
    name          = "gcp-${local.image_name}"
    os            = var.os_version
    build_version = var.build_version
    build_date    = local.build_timestamp
    builder       = "packer"
  }
  
  # Enable guest OS features
  image_guest_os_features {
    type = "SECURE_BOOT"
  }
  
  image_guest_os_features {
    type = "UEFI_COMPATIBLE"
  }
  
  # Storage location for multi-region
  image_storage_locations = ["us", "eu", "asia"]
}

# Shared build configuration
build {
  name = "golden-image"
  
  sources = [
    "source.amazon-ebs.ubuntu",
    "source.azure-arm.ubuntu",
    "source.googlecompute.ubuntu"
  ]
  
  # Cloud-init cleanup (runs first)
  provisioner "shell" {
    inline = [
      "cloud-init status --wait",
      "sudo cloud-init clean --logs --seed"
    ]
  }
  
  # Base system configuration
  provisioner "shell" {
    scripts = local.common_scripts
    environment_vars = [
      "BUILD_VERSION=${var.build_version}",
      "DEBIAN_FRONTEND=noninteractive"
    ]
  }
  
  # Install monitoring agents
  provisioner "shell" {
    scripts = [
      "scripts/monitoring/install-cloudwatch-agent.sh",
      "scripts/monitoring/install-azure-monitor-agent.sh", 
      "scripts/monitoring/install-ops-agent.sh"
    ]
    only = ["amazon-ebs.ubuntu", "azure-arm.ubuntu", "googlecompute.ubuntu"]
  }
  
  # Cloud-specific configurations
  provisioner "shell" {
    script = "scripts/aws/configure-aws-specific.sh"
    only   = ["amazon-ebs.ubuntu"]
  }
  
  provisioner "shell" {
    script = "scripts/azure/configure-azure-specific.sh"
    only   = ["azure-arm.ubuntu"]
  }
  
  provisioner "shell" {
    script = "scripts/gcp/configure-gcp-specific.sh"
    only   = ["googlecompute.ubuntu"]
  }
  
  # Compliance scanning
  provisioner "shell" {
    inline = [
      "wget https://github.com/aquasecurity/trivy/releases/download/v0.35.0/trivy_0.35.0_Linux-64bit.deb",
      "sudo dpkg -i trivy_0.35.0_Linux-64bit.deb",
      "sudo trivy fs --security-checks vuln,config / --format json --output /tmp/trivy-report.json"
    ]
  }
  
  provisioner "file" {
    source      = "/tmp/trivy-report.json"
    destination = "compliance-reports/trivy-${local.build_timestamp}.json"
    direction   = "download"
  }
  
  # Generate SBOM
  provisioner "shell" {
    inline = [
      "sudo apt-get install -y syft",
      "syft / -o json > /tmp/sbom.json"
    ]
  }
  
  provisioner "file" {
    source      = "/tmp/sbom.json"
    destination = "sbom/sbom-${local.build_timestamp}.json"
    direction   = "download"
  }
  
  # Final cleanup
  provisioner "shell" {
    script = "scripts/cleanup.sh"
  }
  
  # Post-processing
  post-processor "manifest" {
    output = "manifests/build-manifest.json"
    strip_path = true
    custom_data = {
      build_version = var.build_version
      git_commit    = env("GIT_COMMIT")
      pipeline_id   = env("CI_PIPELINE_ID")
    }
  }
  
  post-processor "shell-local" {
    inline = [
      "python3 scripts/register-image-metadata.py --manifest manifests/build-manifest.json"
    ]
  }
}
```

### Container Image Building
```hcl
# Building optimized container images with Packer
variable "docker_registry" {
  type    = string
  default = "ghcr.io/company"
}

variable "app_name" {
  type = string
}

variable "app_version" {
  type = string
}

# Multi-stage Docker build
source "docker" "app" {
  image  = "ubuntu:22.04"
  commit = true
  
  changes = [
    "USER app",
    "WORKDIR /app",
    "ENTRYPOINT [\"/app/entrypoint.sh\"]",
    "CMD [\"server\"]",
    "EXPOSE 8080",
    "LABEL version=\"${var.app_version}\"",
    "LABEL maintainer=\"platform-team@company.com\""
  ]
}

# Podman builder for OCI compliance
source "podman" "app" {
  image  = "ubuntu:22.04"
  commit = true
}

build {
  name = "container-image"
  
  sources = [
    "source.docker.app",
    "source.podman.app"
  ]
  
  # Install dependencies
  provisioner "shell" {
    inline = [
      "apt-get update",
      "apt-get install -y --no-install-recommends \\",
      "  ca-certificates \\",
      "  curl \\",
      "  gnupg \\",
      "  lsb-release",
      "apt-get clean",
      "rm -rf /var/lib/apt/lists/*"
    ]
  }
  
  # Create app user
  provisioner "shell" {
    inline = [
      "groupadd -g 1001 app",
      "useradd -u 1001 -g app -m -d /app -s /bin/bash app"
    ]
  }
  
  # Copy application
  provisioner "file" {
    source      = "dist/"
    destination = "/app/"
  }
  
  # Set permissions
  provisioner "shell" {
    inline = [
      "chown -R app:app /app",
      "chmod +x /app/entrypoint.sh",
      "chmod +x /app/bin/*"
    ]
  }
  
  # Security scanning
  provisioner "shell" {
    inline = [
      "curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin",
      "trivy fs --exit-code 0 --severity HIGH,CRITICAL --no-progress /"
    ]
  }
  
  # Export and tag
  post-processor "docker-tag" {
    repository = "${var.docker_registry}/${var.app_name}"
    tags = [
      "${var.app_version}",
      "latest"
    ]
    only = ["docker.app"]
  }
  
  # Push to registry
  post-processor "docker-push" {
    ecr_login     = true
    aws_profile   = "default"
    login_server  = "https://${var.docker_registry}"
    only          = ["docker.app"]
  }
  
  # Generate SBOM
  post-processor "shell-local" {
    inline = [
      "syft ${var.docker_registry}/${var.app_name}:${var.app_version} -o spdx-json > sbom.json",
      "cosign attach sbom --sbom sbom.json ${var.docker_registry}/${var.app_name}:${var.app_version}"
    ]
  }
  
  # Sign image
  post-processor "shell-local" {
    inline = [
      "cosign sign --key cosign.key ${var.docker_registry}/${var.app_name}:${var.app_version}"
    ]
    environment_vars = [
      "COSIGN_PASSWORD=${env("COSIGN_PASSWORD")}"
    ]
  }
}
```

### Kubernetes Node Images
```hcl
# Building custom Kubernetes node images
variable "kubernetes_version" {
  type    = string
  default = "1.28.2"
}

variable "containerd_version" {
  type    = string
  default = "1.7.8"
}

source "amazon-ebs" "k8s-node" {
  ami_name      = "k8s-node-${var.kubernetes_version}-{{timestamp}}"
  instance_type = "t3.xlarge"
  region        = "us-east-1"
  
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }
  
  ssh_username = "ubuntu"
  
  launch_block_device_mappings {
    device_name           = "/dev/sda1"
    volume_size           = 100
    volume_type           = "gp3"
    encrypted             = true
    iops                  = 3000
    throughput            = 250
    delete_on_termination = true
  }
}

build {
  sources = ["source.amazon-ebs.k8s-node"]
  
  # Install container runtime
  provisioner "shell" {
    script = "scripts/install-containerd.sh"
    environment_vars = [
      "CONTAINERD_VERSION=${var.containerd_version}"
    ]
  }
  
  # Install Kubernetes components
  provisioner "shell" {
    inline = [
      # Add Kubernetes repository
      "curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-archive-keyring.gpg",
      "echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main' | sudo tee /etc/apt/sources.list.d/kubernetes.list",
      
      # Install kubelet, kubeadm, kubectl
      "sudo apt-get update",
      "sudo apt-get install -y kubelet=${var.kubernetes_version}-00 kubeadm=${var.kubernetes_version}-00 kubectl=${var.kubernetes_version}-00",
      "sudo apt-mark hold kubelet kubeadm kubectl",
      
      # Configure kubelet
      "sudo systemctl enable kubelet"
    ]
  }
  
  # System configuration
  provisioner "shell" {
    inline = [
      # Disable swap
      "sudo swapoff -a",
      "sudo sed -i '/ swap / s/^/#/' /etc/fstab",
      
      # Load required modules
      "cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF",
      
      # Sysctl settings
      "cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF",
      
      "sudo sysctl --system"
    ]
  }
  
  # Pre-pull images
  provisioner "shell" {
    inline = [
      "sudo kubeadm config images pull --kubernetes-version=${var.kubernetes_version}",
      "sudo ctr -n k8s.io images pull docker.io/calico/node:v3.26.0",
      "sudo ctr -n k8s.io images pull docker.io/calico/cni:v3.26.0"
    ]
  }
  
  # Install additional tools
  provisioner "ansible" {
    playbook_file = "ansible/k8s-tools.yml"
    extra_arguments = [
      "--extra-vars", jsonencode({
        install_helm       = true
        install_kustomize  = true
        install_kubectl_plugins = true
      })
    ]
  }
  
  # Node optimization
  provisioner "shell" {
    scripts = [
      "scripts/optimize-kernel.sh",
      "scripts/configure-networking.sh",
      "scripts/setup-monitoring.sh"
    ]
  }
  
  # Cleanup
  provisioner "shell" {
    inline = [
      "sudo apt-get clean",
      "sudo rm -rf /var/lib/apt/lists/*",
      "sudo rm -rf /tmp/*",
      "sudo journalctl --vacuum-time=1d"
    ]
  }
}
```

### Windows Server Images
```hcl
# Windows Server 2022 image building
variable "windows_version" {
  type    = string
  default = "2022"
}

source "amazon-ebs" "windows" {
  ami_name      = "windows-server-${var.windows_version}-{{timestamp}}"
  instance_type = "m5.xlarge"
  region        = "us-east-1"
  
  source_ami_filter {
    filters = {
      name         = "Windows_Server-2022-English-Full-Base-*"
      owner-alias  = "amazon"
      architecture = "x86_64"
    }
    most_recent = true
  }
  
  communicator   = "winrm"
  winrm_username = "Administrator"
  winrm_use_ssl  = true
  winrm_insecure = true
  
  user_data_file = "scripts/windows/bootstrap-winrm.ps1"
  
  launch_block_device_mappings {
    device_name           = "/dev/sda1"
    volume_size           = 100
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }
  
  ami_block_device_mappings {
    device_name  = "/dev/sda1"
    volume_size  = 100
    volume_type  = "gp3"
    encrypted    = true
    delete_on_termination = true
  }
}

build {
  sources = ["source.amazon-ebs.windows"]
  
  # Windows updates
  provisioner "powershell" {
    inline = [
      "Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force",
      "Install-Module PSWindowsUpdate -Force",
      "Get-WindowsUpdate -AcceptAll -Install -IgnoreReboot"
    ]
    elevated_user     = "Administrator"
    elevated_password = build.Password
  }
  
  # Install base software
  provisioner "powershell" {
    scripts = [
      "scripts/windows/install-chocolatey.ps1",
      "scripts/windows/install-base-software.ps1"
    ]
  }
  
  # Configure Windows features
  provisioner "powershell" {
    inline = [
      # Install IIS
      "Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole, IIS-WebServer -All",
      
      # Install .NET
      "Enable-WindowsOptionalFeature -Online -FeatureName NetFx4Extended-ASPNET45 -All",
      
      # Configure Windows Defender
      "Set-MpPreference -DisableRealtimeMonitoring $false",
      "Update-MpSignature"
    ]
  }
  
  # Security hardening
  provisioner "powershell" {
    script = "scripts/windows/security-baseline.ps1"
  }
  
  # Sysprep
  provisioner "powershell" {
    inline = [
      "& $env:SystemRoot\\System32\\Sysprep\\Sysprep.exe /oobe /generalize /quiet /quit",
      "while($true) { $imageState = Get-ItemProperty HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Setup\\State | Select ImageState; if($imageState.ImageState -ne 'IMAGE_STATE_GENERALIZE_RESEAL_TO_OOBE') { Write-Output $imageState.ImageState; Start-Sleep -s 10  } else { break } }"
    ]
  }
}
```

## Best Practices

### 1. Template Organization
```
packer-templates/
├── README.md
├── Makefile
├── .gitlab-ci.yml
├── builds/
│   ├── aws/
│   │   ├── amazon-linux-2.pkr.hcl
│   │   ├── ubuntu-22.04.pkr.hcl
│   │   └── windows-2022.pkr.hcl
│   ├── azure/
│   │   └── ubuntu-22.04.pkr.hcl
│   └── gcp/
│       └── ubuntu-22.04.pkr.hcl
├── scripts/
│   ├── common/
│   │   ├── update-system.sh
│   │   ├── install-base-tools.sh
│   │   └── cleanup.sh
│   ├── aws/
│   │   └── install-ssm-agent.sh
│   ├── azure/
│   │   └── install-waagent.sh
│   └── gcp/
│       └── install-ops-agent.sh
├── ansible/
│   ├── playbooks/
│   │   ├── base-configuration.yml
│   │   ├── security-hardening.yml
│   │   └── application-install.yml
│   └── roles/
│       ├── common/
│       ├── security/
│       └── monitoring/
├── tests/
│   ├── inspec/
│   │   ├── controls/
│   │   └── inspec.yml
│   └── serverspec/
│       └── spec/
├── config/
│   ├── variables.pkrvars.hcl
│   └── environments/
│       ├── dev.pkrvars.hcl
│       └── prod.pkrvars.hcl
└── modules/
    ├── base-image/
    ├── security/
    └── monitoring/
```

### 2. Variable Management
```hcl
# variables.pkr.hcl
variable "build_env" {
  type        = string
  description = "Build environment (dev, staging, prod)"
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.build_env)
    error_message = "Valid values for build_env are dev, staging, or prod."
  }
}

variable "security_groups" {
  type = map(object({
    name        = string
    description = string
    rules = list(object({
      protocol    = string
      from_port   = number
      to_port     = number
      cidr_blocks = list(string)
    }))
  }))
  
  default = {
    web = {
      name        = "packer-web-sg"
      description = "Security group for web servers"
      rules = [
        {
          protocol    = "tcp"
          from_port   = 80
          to_port     = 80
          cidr_blocks = ["0.0.0.0/0"]
        }
      ]
    }
  }
}

# Environment-specific variables
# environments/prod.pkrvars.hcl
build_env     = "prod"
instance_type = "m5.xlarge"
volume_size   = 100

ami_regions = [
  "us-east-1",
  "us-west-2",
  "eu-west-1",
  "ap-southeast-1"
]

tags = {
  Environment = "production"
  Compliance  = "required"
  Encryption  = "enabled"
}
```

### 3. Provisioning Scripts
```bash
#!/bin/bash
# scripts/common/install-base-tools.sh
set -euxo pipefail

# Script metadata
SCRIPT_VERSION="1.0.0"
SCRIPT_NAME=$(basename "$0")
LOG_FILE="/var/log/packer-${SCRIPT_NAME%.sh}.log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Error handling
trap 'log "Error on line $LINENO"' ERR

# Start logging
log "Starting $SCRIPT_NAME v$SCRIPT_VERSION"
log "BUILD_VERSION: ${BUILD_VERSION:-not set}"
log "BUILD_ENV: ${BUILD_ENV:-not set}"

# Update package manager
log "Updating package manager"
export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get upgrade -y

# Install essential packages
PACKAGES=(
    "curl"
    "wget"
    "git"
    "vim"
    "htop"
    "net-tools"
    "dnsutils"
    "telnet"
    "unzip"
    "jq"
    "python3-pip"
    "software-properties-common"
    "apt-transport-https"
    "ca-certificates"
    "gnupg"
    "lsb-release"
)

log "Installing packages: ${PACKAGES[*]}"
apt-get install -y "${PACKAGES[@]}"

# Install AWS CLI
log "Installing AWS CLI v2"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
unzip -q /tmp/awscliv2.zip -d /tmp
/tmp/aws/install
rm -rf /tmp/aws*

# Install monitoring tools
log "Installing monitoring tools"
# CloudWatch Agent
wget -q https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
dpkg -i -E amazon-cloudwatch-agent.rpm || apt-get -f install -y
rm amazon-cloudwatch-agent.rpm

# Install security tools
log "Installing security tools"
# Fail2ban
apt-get install -y fail2ban
systemctl enable fail2ban

# ClamAV
apt-get install -y clamav clamav-daemon
freshclam
systemctl enable clamav-freshclam

# Configure system limits
log "Configuring system limits"
cat >> /etc/security/limits.conf <<EOF
# Packer build configuration
* soft nofile 65535
* hard nofile 65535
* soft nproc 32768
* hard nproc 32768
EOF

# Kernel parameters
log "Setting kernel parameters"
cat > /etc/sysctl.d/99-packer.conf <<EOF
# Network optimizations
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_congestion_control = bbr

# Security settings
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.tcp_syncookies = 1
kernel.randomize_va_space = 2

# File system settings
fs.file-max = 2097152
vm.swappiness = 10
EOF

sysctl -p /etc/sysctl.d/99-packer.conf

log "Base tools installation completed successfully"
exit 0
```

### 4. Testing and Validation
```ruby
# tests/serverspec/spec/golden_image_spec.rb
require 'spec_helper'

describe 'Golden Image Tests' do
  # OS Tests
  describe 'Operating System' do
    describe file('/etc/os-release') do
      its(:content) { should match /Ubuntu 22.04/ }
    end
    
    describe command('uname -r') do
      its(:stdout) { should match /^5\.15\./ }
    end
  end
  
  # Package Tests
  %w[curl wget git vim jq aws-cli].each do |pkg|
    describe package(pkg) do
      it { should be_installed }
    end
  end
  
  # Security Tests
  describe 'Security Configuration' do
    describe file('/etc/ssh/sshd_config') do
      its(:content) { should match /^PermitRootLogin no/ }
      its(:content) { should match /^PasswordAuthentication no/ }
      its(:content) { should match /^PubkeyAuthentication yes/ }
    end
    
    describe service('fail2ban') do
      it { should be_enabled }
      it { should be_running }
    end
    
    describe iptables do
      it { should have_rule('-P INPUT DROP') }
      it { should have_rule('-P FORWARD DROP') }
      it { should have_rule('-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT') }
    end
  end
  
  # User Configuration
  describe user('app') do
    it { should exist }
    it { should have_uid 1001 }
    it { should belong_to_group 'app' }
    it { should have_home_directory '/app' }
  end
  
  # Filesystem Tests
  describe file('/') do
    it { should be_mounted.with(type: 'ext4', options: { rw: true }) }
  end
  
  describe file('/tmp') do
    it { should be_directory }
    it { should be_mode 1777 }
  end
  
  # Kernel Parameters
  describe kernel_parameter('net.ipv4.tcp_syncookies') do
    its(:value) { should eq 1 }
  end
  
  describe kernel_parameter('fs.file-max') do
    its(:value) { should be >= 2097152 }
  end
end
```

### 5. CI/CD Integration
```yaml
# .gitlab-ci.yml
stages:
  - validate
  - build
  - test
  - publish
  - notify

variables:
  PACKER_VERSION: "1.9.4"
  
before_script:
  - wget -q https://releases.hashicorp.com/packer/${PACKER_VERSION}/packer_${PACKER_VERSION}_linux_amd64.zip
  - unzip -o packer_${PACKER_VERSION}_linux_amd64.zip -d /usr/local/bin/
  - packer version

validate:
  stage: validate
  script:
    - packer init .
    - packer validate -var-file=config/variables.pkrvars.hcl builds/aws/ubuntu-22.04.pkr.hcl
    - packer validate -var-file=config/variables.pkrvars.hcl builds/azure/ubuntu-22.04.pkr.hcl
  rules:
    - if: $CI_MERGE_REQUEST_ID

build-aws:
  stage: build
  script:
    - export BUILD_VERSION="${CI_COMMIT_TAG:-${CI_COMMIT_SHORT_SHA}}"
    - |
      packer build \
        -var-file=config/${CI_ENVIRONMENT_NAME}.pkrvars.hcl \
        -var "build_version=${BUILD_VERSION}" \
        -var "git_commit=${CI_COMMIT_SHA}" \
        builds/aws/ubuntu-22.04.pkr.hcl
    - cp manifest.json aws-manifest-${CI_COMMIT_SHORT_SHA}.json
  artifacts:
    paths:
      - aws-manifest-*.json
    reports:
      dotenv: build.env
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

test-ami:
  stage: test
  image: chef/inspec:latest
  dependencies:
    - build-aws
  script:
    - export AMI_ID=$(jq -r '.builds[0].artifact_id' aws-manifest-${CI_COMMIT_SHORT_SHA}.json | cut -d':' -f2)
    - |
      inspec exec tests/inspec \
        -t aws://${AWS_REGION} \
        --input ami_id=${AMI_ID}
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

publish-metadata:
  stage: publish
  script:
    - |
      python3 scripts/publish_image_metadata.py \
        --manifest aws-manifest-${CI_COMMIT_SHORT_SHA}.json \
        --registry ${IMAGE_REGISTRY_URL}
  rules:
    - if: $CI_COMMIT_TAG

notify:
  stage: notify
  script:
    - |
      curl -X POST ${SLACK_WEBHOOK_URL} \
        -H 'Content-Type: application/json' \
        -d "{
          \"text\": \"Image build completed successfully\",
          \"attachments\": [{
            \"color\": \"good\",
            \"fields\": [
              {\"title\": \"Build Version\", \"value\": \"${BUILD_VERSION}\", \"short\": true},
              {\"title\": \"Git Commit\", \"value\": \"${CI_COMMIT_SHORT_SHA}\", \"short\": true},
              {\"title\": \"Pipeline\", \"value\": \"${CI_PIPELINE_URL}\", \"short\": false}
            ]
          }]
        }"
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

## Integration Patterns

### 1. HashiCorp Stack Integration
```hcl
# Integration with Terraform and Vault
data "vault_generic_secret" "aws_creds" {
  path = "secret/data/aws/packer"
}

locals {
  aws_access_key = data.vault_generic_secret.aws_creds.data["access_key"]
  aws_secret_key = data.vault_generic_secret.aws_creds.data["secret_key"]
}

source "amazon-ebs" "vault-integrated" {
  access_key    = local.aws_access_key
  secret_key    = local.aws_secret_key
  
  # ... rest of configuration
}

# Post-processor to update Terraform
post-processor "shell-local" {
  inline = [
    # Update Terraform variables
    "echo 'ami_id = \"'$(jq -r '.builds[0].artifact_id' manifest.json | cut -d':' -f2)'\"' > terraform/terraform.tfvars",
    
    # Trigger Terraform apply
    "cd terraform && terraform apply -auto-approve"
  ]
}
```

### 2. Kubernetes Integration
```yaml
# Kubernetes Job for image building
apiVersion: batch/v1
kind: Job
metadata:
  name: packer-build-job
  namespace: ci-cd
spec:
  template:
    spec:
      serviceAccountName: packer-builder
      containers:
      - name: packer
        image: hashicorp/packer:1.9.4
        command: ["packer", "build"]
        args:
          - "-var-file=/config/variables.pkrvars.hcl"
          - "/templates/kubernetes-node.pkr.hcl"
        volumeMounts:
        - name: templates
          mountPath: /templates
        - name: config
          mountPath: /config
        - name: aws-creds
          mountPath: /root/.aws
        env:
        - name: PACKER_LOG
          value: "1"
        resources:
          requests:
            cpu: 2
            memory: 4Gi
          limits:
            cpu: 4
            memory: 8Gi
      volumes:
      - name: templates
        configMap:
          name: packer-templates
      - name: config
        configMap:
          name: packer-config
      - name: aws-creds
        secret:
          secretName: aws-credentials
      restartPolicy: OnFailure
```

### 3. Compliance and Security Scanning
```hcl
# Compliance scanning integration
build {
  # ... sources ...
  
  # CIS Benchmark scanning
  provisioner "shell" {
    inline = [
      "git clone https://github.com/CISOfy/lynis /tmp/lynis",
      "cd /tmp/lynis && ./lynis audit system --quick --quiet",
      "cp /var/log/lynis.log /tmp/compliance-report.log"
    ]
  }
  
  # STIG compliance
  provisioner "ansible" {
    playbook_file = "ansible/stig-compliance.yml"
    extra_arguments = [
      "--tags", "stig-cat-1,stig-cat-2"
    ]
  }
  
  # Vulnerability scanning
  provisioner "shell" {
    script = "scripts/run-security-scan.sh"
  }
  
  # Download compliance reports
  provisioner "file" {
    source      = "/tmp/compliance-report.log"
    destination = "reports/compliance-${var.build_version}.log"
    direction   = "download"
  }
  
  # Gate on compliance results
  post-processor "shell-local" {
    inline = [
      "python3 scripts/check-compliance.py --report reports/compliance-${var.build_version}.log --threshold 90"
    ]
  }
}
```

### 4. Multi-Stage Pipeline
```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        PACKER_HOME = tool name: 'packer-1.9.4', type: 'packer'
        BUILD_VERSION = "${env.TAG_NAME ?: env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Validate') {
            steps {
                script {
                    sh "${PACKER_HOME}/packer validate -syntax-only templates/*.pkr.hcl"
                }
            }
        }
        
        stage('Build Base Images') {
            parallel {
                stage('AWS AMI') {
                    steps {
                        sh """
                            ${PACKER_HOME}/packer build \
                                -var 'build_version=${BUILD_VERSION}' \
                                templates/aws-base.pkr.hcl
                        """
                    }
                }
                stage('Azure Image') {
                    steps {
                        sh """
                            ${PACKER_HOME}/packer build \
                                -var 'build_version=${BUILD_VERSION}' \
                                templates/azure-base.pkr.hcl
                        """
                    }
                }
            }
        }
        
        stage('Test Images') {
            steps {
                script {
                    sh "inspec exec tests/ --reporter json:test-results.json"
                }
            }
        }
        
        stage('Promote Images') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh "python3 scripts/promote-images.py --version ${BUILD_VERSION}"
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'manifest.json, test-results.json', fingerprint: true
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'compliance-report.html',
                reportName: 'Compliance Report'
            ])
        }
    }
}
```

## Troubleshooting

### Common Issues

1. **SSH Connection Failures**
```hcl
# Debug SSH issues
source "amazon-ebs" "debug" {
  # ... other config ...
  
  # Extended SSH timeout
  ssh_timeout = "20m"
  
  # Use specific SSH settings
  ssh_interface = "private_ip"
  ssh_agent_auth = false
  
  # Debug logging
  pause_before_connecting = "30s"
}

# Enable Packer debug logging
export PACKER_LOG=1
export PACKER_LOG_PATH="packer-debug.log"
```

2. **WinRM Connection Issues**
```hcl
# Windows WinRM configuration
source "amazon-ebs" "windows" {
  # ... other config ...
  
  # WinRM configuration
  communicator     = "winrm"
  winrm_use_ssl    = true
  winrm_insecure   = true
  winrm_timeout    = "30m"
  winrm_username   = "Administrator"
  
  # User data for WinRM setup
  user_data = <<-EOF
    <powershell>
    # Configure WinRM
    winrm quickconfig -q
    winrm set winrm/config '@{MaxTimeoutms="1800000"}'
    winrm set winrm/config/service '@{AllowUnencrypted="true"}'
    winrm set winrm/config/service/auth '@{Basic="true"}'
    
    # Configure firewall
    netsh advfirewall firewall add rule name="WinRM 5986" protocol=TCP dir=in localport=5986 action=allow
    
    # Create self-signed certificate
    $cert = New-SelfSignedCertificate -DnsName $env:COMPUTERNAME -CertStoreLocation Cert:\LocalMachine\My
    winrm create winrm/config/Listener?Address=*+Transport=HTTPS "@{Hostname=`"$env:COMPUTERNAME`";CertificateThumbprint=`"$($cert.Thumbprint)`"}"
    
    # Restart WinRM
    Restart-Service winrm
    </powershell>
    EOF
}
```

3. **Build Performance Issues**
```hcl
# Optimize build performance
source "amazon-ebs" "optimized" {
  # Use larger instance for builds
  instance_type = "m5.2xlarge"
  
  # Use enhanced networking
  ena_support = true
  
  # Optimize EBS
  launch_block_device_mappings {
    device_name = "/dev/sda1"
    volume_type = "gp3"
    iops        = 10000
    throughput  = 1000
  }
  
  # Use spot instances for cost savings
  spot_price    = "auto"
  spot_instance_types = ["m5.2xlarge", "m5.xlarge", "m5a.2xlarge"]
}

# Parallel provisioning
build {
  sources = ["source.amazon-ebs.optimized"]
  
  # Run independent tasks in parallel
  provisioner "shell" {
    scripts = [
      "scripts/task1.sh",
      "scripts/task2.sh"
    ]
    max_retries = 3
    pause_before = "10s"
  }
}
```

### Debug Techniques

1. **Enable Debug Mode**
```bash
# Maximum verbosity
export PACKER_LOG=1
export PACKER_LOG_PATH="packer.log"

# Build with on-error=ask for debugging
packer build -on-error=ask template.pkr.hcl

# Use breakpoint provisioner
provisioner "breakpoint" {
  disable = false
  note    = "Stop here to debug"
}
```

2. **Inspect Failed Builds**
```hcl
# Keep instance running on error
source "amazon-ebs" "debug" {
  # ... config ...
  
  # Don't terminate on error
  shutdown_behavior = "stop"
  
  # Tag for easy identification
  run_tags = {
    Name = "Packer Debug Instance"
    Debug = "true"
  }
}
```

## Performance Optimization

### 1. Build Caching
```hcl
# Use EBS snapshots for caching
source "amazon-ebs" "cached" {
  # Create snapshot of provisioned instance
  snapshot_tags = {
    Name = "packer-cache-${var.os_version}"
  }
  
  # Use snapshot on subsequent builds
  source_ami_filter {
    filters = {
      "tag:Name" : "packer-cache-${var.os_version}"
    }
    most_recent = true
    owners      = ["self"]
  }
}

# Container layer caching
source "docker" "cached" {
  image = "ubuntu:22.04"
  
  # Use buildkit for better caching
  changes = [
    "ENV DOCKER_BUILDKIT=1"
  ]
  
  # Mount cache directories
  volumes = {
    "/tmp/packer-cache" : "/cache"
  }
}
```

### 2. Parallel Builds
```hcl
# Makefile for parallel builds
.PHONY: all aws azure gcp

all: aws azure gcp

aws:
	packer build -var-file=common.pkrvars.hcl aws.pkr.hcl

azure:
	packer build -var-file=common.pkrvars.hcl azure.pkr.hcl

gcp:
	packer build -var-file=common.pkrvars.hcl gcp.pkr.hcl

parallel:
	$(MAKE) -j3 all
```

---

### 📡 Stay Updated

**Release Notes**: [Packer Releases](https://github.com/hashicorp/packer/releases) • [Plugin Updates](https://github.com/hashicorp/packer-plugin-amazon/releases) • [HCL2 Features](https://github.com/hashicorp/hcl/releases)

**Project News**: [HashiCorp Blog](https://www.hashicorp.com/blog/products/packer) • [Learn Platform](https://learn.hashicorp.com/packer) • [Community Updates](https://discuss.hashicorp.com/c/packer/23)

**Community**: [HashiCorp Community](https://discuss.hashicorp.com/c/packer/23) • [GitHub Discussions](https://github.com/hashicorp/packer/discussions) • [User Groups](https://www.meetup.com/pro/hashicorp/)