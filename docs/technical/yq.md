# yq

yq is a lightweight and portable command-line YAML, JSON, XML, CSV and properties processor. It's the YAML equivalent of `jq` and is essential for platform engineers working with configuration files, CI/CD pipelines, and infrastructure as code.

## Overview

yq is widely used in platform engineering for:
- Processing Kubernetes YAML manifests
- Managing configuration files in CI/CD pipelines
- Extracting and modifying values in deployment scripts
- Converting between YAML, JSON, and other formats
- Automating infrastructure configuration management

## Key Features

- **Multi-Format Support**: YAML, JSON, XML, CSV, properties, TOML
- **Powerful Query Language**: Uses similar syntax to jq
- **In-Place Editing**: Modify files directly
- **Cross-Platform**: Available on Linux, macOS, Windows
- **Lightweight**: Single binary with no dependencies
- **Shell Completion**: Support for bash, zsh, fish

## Installation

### Package Managers
```bash
# macOS (Homebrew)
brew install yq

# Ubuntu/Debian
sudo apt-get install yq

# CentOS/RHEL/Fedora
sudo yum install yq

# Arch Linux
sudo pacman -S yq

# Windows (Chocolatey)
choco install yq

# Windows (Scoop)
scoop install yq
```

### Direct Download
```bash
# Download latest release
VERSION=v4.40.5
BINARY=yq_linux_amd64
wget https://github.com/mikefarah/yq/releases/download/${VERSION}/${BINARY}.tar.gz -O - | tar xz && sudo mv ${BINARY} /usr/bin/yq

# Make executable
sudo chmod +x /usr/bin/yq
```

## Basic Syntax and Operations

### Reading Values
```bash
# Basic value extraction
yq '.name' config.yaml
yq '.database.host' config.yaml
yq '.services[0].name' docker-compose.yml

# Array elements
yq '.items[0]' data.yaml
yq '.items[]' data.yaml           # All items
yq '.items[1:3]' data.yaml        # Slice (items 1-2)

# Multiple values
yq '.name, .version' config.yaml
yq '.database.host, .database.port' config.yaml
```

### Writing/Updating Values
```bash
# Update values in-place
yq -i '.database.host = "localhost"' config.yaml
yq -i '.replicas = 3' deployment.yaml
yq -i '.services.web.ports[0] = "8080:80"' docker-compose.yml

# Add new fields
yq -i '.metadata.labels.environment = "production"' k8s-manifest.yaml
yq -i '.spec.template.spec.containers[0].env[].name = "DEBUG"' deployment.yaml

# Update multiple values
yq -i '.database.host = "prod-db" | .database.port = 5432' config.yaml
```

### Conditional Operations
```bash
# Conditional updates
yq -i '(.metadata.labels.environment // "dev") = "production"' manifest.yaml
yq -i 'select(.kind == "Deployment").spec.replicas = 5' *.yaml

# Conditional selection
yq '.services[] | select(.name == "web")' docker-compose.yml
yq '.items[] | select(.status == "active")' data.yaml
yq '.spec.containers[] | select(.image | contains("nginx"))' deployment.yaml
```

## Platform Engineering Use Cases

### Kubernetes Manifest Processing
```bash
# Extract all container images
yq '.spec.template.spec.containers[].image' deployment.yaml

# Update deployment image
yq -i '.spec.template.spec.containers[0].image = "nginx:1.21"' deployment.yaml

# Set resource limits
yq -i '.spec.template.spec.containers[0].resources.limits.memory = "512Mi"' deployment.yaml
yq -i '.spec.template.spec.containers[0].resources.limits.cpu = "500m"' deployment.yaml

# Add environment variables
yq -i '.spec.template.spec.containers[0].env += [{"name": "DATABASE_URL", "value": "postgresql://..."}]' deployment.yaml

# Update replica count
yq -i '.spec.replicas = 3' deployment.yaml

# Add labels
yq -i '.metadata.labels.version = "v1.2.3"' deployment.yaml
yq -i '.spec.template.metadata.labels.version = "v1.2.3"' deployment.yaml

# Process multiple files
for file in manifests/*.yaml; do
  yq -i '.metadata.namespace = "production"' "$file"
done

# Extract all services and their ports
yq '.spec.ports[].port' service.yaml
yq '.spec.ports[] | .name + ":" + (.port | tostring)' service.yaml
```

### Docker Compose Management
```bash
# Update service image
yq -i '.services.web.image = "nginx:alpine"' docker-compose.yml

# Add environment variables
yq -i '.services.web.environment.DEBUG = "true"' docker-compose.yml

# Update port mappings
yq -i '.services.web.ports = ["8080:80", "8443:443"]' docker-compose.yml

# Add new service
yq -i '.services.redis = {"image": "redis:alpine", "ports": ["6379:6379"]}' docker-compose.yml

# Extract all service names
yq '.services | keys' docker-compose.yml

# Get services using specific image
yq '.services[] | select(.image | contains("postgres")) | key' docker-compose.yml
```

### CI/CD Configuration Processing
```bash
# GitHub Actions workflow processing
yq '.jobs.*.steps[].name' .github/workflows/ci.yml
yq '.jobs.build.steps[] | select(.uses | contains("checkout"))' .github/workflows/ci.yml

# Update workflow triggers
yq -i '.on.push.branches = ["main", "develop"]' .github/workflows/ci.yml

# Add new job step
yq -i '.jobs.test.steps += [{"name": "Run tests", "run": "npm test"}]' .github/workflows/ci.yml

# GitLab CI processing
yq '.stages[]' .gitlab-ci.yml
yq '.*.script[]' .gitlab-ci.yml

# Update stage dependencies
yq -i '.deploy.dependencies = ["build", "test"]' .gitlab-ci.yml
```

### Configuration File Management
```bash
# Application configuration
yq '.database.host' config.yaml
yq -i '.database.host = env(DATABASE_HOST)' config.yaml
yq -i '.debug = (env(DEBUG) // false)' config.yaml

# Merge configurations
yq eval-all 'select(fileIndex == 0) * select(fileIndex == 1)' base-config.yaml env-config.yaml

# Extract secrets (for processing, not storing)
yq '.secrets[].name' secrets.yaml

# Update configuration based on environment
if [ "$ENV" = "production" ]; then
  yq -i '.log_level = "warn" | .debug = false' config.yaml
else
  yq -i '.log_level = "debug" | .debug = true' config.yaml
fi
```

### Infrastructure as Code
```bash
# Ansible playbook processing
yq '.tasks[].name' playbook.yml
yq '.tasks[] | select(.name | contains("install"))' playbook.yml

# Update playbook variables
yq -i '.vars.app_version = "v1.2.3"' playbook.yml

# Helm values processing
yq '.image.tag' values.yaml
yq -i '.image.tag = "v1.2.3"' values.yaml
yq -i '.replicas = 5' values.yaml

# Extract all configmap data
yq '.data' configmap.yaml
yq '.data | keys' configmap.yaml
```

## Advanced Features

### Complex Queries and Transformations
```bash
# Map transformations
yq '.services | to_entries | map({"name": .key, "image": .value.image})' docker-compose.yml

# Group by operations
yq 'group_by(.status) | map({"status": .[0].status, "count": length})' data.yaml

# Sort operations
yq '.items | sort_by(.name)' data.yaml
yq '.services | to_entries | sort_by(.value.image)' docker-compose.yml

# Filter and transform
yq '.spec.containers[] | select(.image | contains("nginx")) | .name' deployment.yaml

# Arithmetic operations
yq '.spec.replicas + 2' deployment.yaml
yq '.resources.limits.memory | sub("Mi"; "") | tonumber' deployment.yaml
```

### Working with Multiple Files
```bash
# Merge multiple YAML files
yq eval-all '. as $item ireduce ({}; . * $item)' config1.yaml config2.yaml

# Process all files in directory
yq '.metadata.name' manifests/*.yaml

# Compare files
yq eval-all 'select(fileIndex == 0) == select(fileIndex == 1)' file1.yaml file2.yaml

# Extract specific content from multiple files
yq '.kind + ": " + .metadata.name' manifests/*.yaml
```

### Format Conversion
```bash
# YAML to JSON
yq -o=json '.' config.yaml

# JSON to YAML
yq -P '.' config.json

# YAML to properties
yq -o=props '.' config.yaml

# XML to YAML
yq -p=xml '.' config.xml

# CSV processing
yq -p=csv -o=json '.' data.csv
```

### Environment Variable Integration
```bash
# Use environment variables
export DB_HOST="localhost"
yq -i '.database.host = env(DB_HOST)' config.yaml

# Default values with environment variables
yq -i '.debug = (env(DEBUG) // false)' config.yaml
yq -i '.port = (env(PORT) // 8080)' config.yaml

# Dynamic configuration
export NAMESPACE="production"
yq -i '.metadata.namespace = env(NAMESPACE)' *.yaml
```

## Scripting and Automation

### Deployment Scripts
```bash
#!/bin/bash
# deploy.sh - Automated deployment script

set -e

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}
NAMESPACE="app-${ENVIRONMENT}"

echo "Deploying version ${VERSION} to ${ENVIRONMENT}"

# Update deployment manifests
yq -i ".spec.template.spec.containers[0].image = \"myapp:${VERSION}\"" k8s/deployment.yaml
yq -i ".metadata.namespace = \"${NAMESPACE}\"" k8s/*.yaml

# Update replica count based on environment
if [ "$ENVIRONMENT" = "production" ]; then
  yq -i '.spec.replicas = 5' k8s/deployment.yaml
else
  yq -i '.spec.replicas = 2' k8s/deployment.yaml
fi

# Apply configurations
kubectl apply -f k8s/

echo "Deployment completed"
```

### Configuration Management
```bash
#!/bin/bash
# config-manager.sh - Configuration management script

ENVIRONMENT=$1
CONFIG_FILE="config/${ENVIRONMENT}.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Environment config not found: $CONFIG_FILE"
  exit 1
fi

# Merge base config with environment config
yq eval-all 'select(fileIndex == 0) * select(fileIndex == 1)' \
  config/base.yaml "$CONFIG_FILE" > final-config.yaml

# Validate configuration
if ! yq '.database.host' final-config.yaml > /dev/null; then
  echo "Invalid configuration: missing database.host"
  exit 1
fi

echo "Configuration generated: final-config.yaml"
```

### Batch Processing
```bash
#!/bin/bash
# update-images.sh - Update container images across manifests

NEW_TAG=$1
IMAGE_PREFIX="myregistry/myapp"

if [ -z "$NEW_TAG" ]; then
  echo "Usage: $0 <new-tag>"
  exit 1
fi

# Update all deployment files
find k8s/ -name "*.yaml" -type f | while read file; do
  if yq '.kind == "Deployment"' "$file" | grep -q true; then
    echo "Updating $file"
    yq -i ".spec.template.spec.containers[].image |= sub(\"${IMAGE_PREFIX}:.*\"; \"${IMAGE_PREFIX}:${NEW_TAG}\")" "$file"
  fi
done

echo "Updated all deployments to use ${IMAGE_PREFIX}:${NEW_TAG}"
```

## Best Practices

### Safe File Editing
```bash
# Always backup before in-place editing
cp config.yaml config.yaml.bak
yq -i '.database.host = "new-host"' config.yaml

# Use validation after editing
yq '.' config.yaml > /dev/null && echo "Valid YAML" || echo "Invalid YAML"

# Atomic updates with temporary files
yq '.database.host = "new-host"' config.yaml > config.yaml.tmp && mv config.yaml.tmp config.yaml
```

### Error Handling
```bash
# Check if file exists and is valid YAML
if [ -f "config.yaml" ] && yq '.' config.yaml > /dev/null 2>&1; then
  yq -i '.updated = now' config.yaml
else
  echo "Invalid or missing YAML file"
  exit 1
fi

# Validate required fields
if ! yq '.database.host' config.yaml > /dev/null; then
  echo "Missing required field: database.host"
  exit 1
fi
```

### Performance Considerations
```bash
# Process large files efficiently
yq --unwrapScalar=false '.large_array[]' big-file.yaml

# Use streaming for very large files
yq -s '.items[]' large-dataset.yaml

# Minimize I/O operations
yq -i '.field1 = "value1" | .field2 = "value2" | .field3 = "value3"' config.yaml
```

## Common Use Cases

### Kubernetes Operations
```bash
# Get all pod names in a namespace
kubectl get pods -o yaml | yq '.items[].metadata.name'

# Extract failing pods
kubectl get pods -o yaml | yq '.items[] | select(.status.phase != "Running") | .metadata.name'

# Update deployment with new image
kubectl get deployment myapp -o yaml | yq '.spec.template.spec.containers[0].image = "myapp:v2"' | kubectl apply -f -
```

### CI/CD Integration
```bash
# Extract version from package.json-like YAML
VERSION=$(yq '.version' package.yaml)
docker build -t "myapp:$VERSION" .

# Update GitOps repository
git clone https://github.com/company/gitops-repo
cd gitops-repo
yq -i ".spec.template.spec.containers[0].image = \"myapp:${VERSION}\"" overlays/production/deployment.yaml
git add . && git commit -m "Update to version $VERSION" && git push
```

## Resources

- [yq Official Documentation](https://mikefarah.gitbook.io/yq/) - Comprehensive yq usage guide
- [yq GitHub Repository](https://github.com/mikefarah/yq) - Source code, releases, and issue tracking
- [yq Cookbook](https://mikefarah.gitbook.io/yq/usage/cookbook) - Common usage patterns and examples
- [YAML Specification](https://yaml.org/spec/1.2.2/) - Official YAML language specification
- [jq Manual](https://stedolan.github.io/jq/manual/) - Similar tool for JSON processing
- [kubectl with yq](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) - Kubernetes CLI integration examples
- [Ansible and yq](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/yq.html) - Ansible yq module documentation
- [yq vs jq Comparison](https://blog.stackademic.com/yq-vs-jq-which-command-line-json-processor-should-you-choose-6e7a1568e5e5) - Tool comparison guide
- [YAML Best Practices](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html) - YAML style and syntax guidelines
- [Shell Scripting with yq](https://www.cyberciti.biz/faq/how-to-parse-yaml-file-in-bash-using-yq/) - Bash integration examples