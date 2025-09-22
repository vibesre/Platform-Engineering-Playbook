# HashiCorp Vault

HashiCorp Vault is a tool for securely accessing secrets and protecting sensitive data. It provides a unified interface to any secret while providing tight access control and recording a detailed audit log.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **HashiCorp Vault Tutorial for Beginners**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 1 hour](https://www.youtube.com/watch?v=VYfl-DpZ5wM)
- **Why it's great**: Comprehensive introduction to Vault concepts and practical usage

#### **Complete Vault Course - Secrets Management**
- **Channel**: KodeKloud
- **Link**: [YouTube - 2 hours](https://www.youtube.com/watch?v=m1h6gA5GBaE)
- **Why it's great**: Hands-on tutorial covering authentication and secret engines

#### **Vault on Kubernetes**
- **Channel**: HashiCorp
- **Link**: [YouTube - 45 minutes](https://www.youtube.com/watch?v=UZy1hfhJs4Y)
- **Why it's great**: Official guide to deploying Vault in Kubernetes environments

### 📖 Essential Documentation

#### **Vault Official Documentation**
- **Link**: [vaultproject.io/docs](https://www.vaultproject.io/docs)
- **Why it's great**: Comprehensive official documentation with tutorials and API reference

#### **Vault Learning Guide**
- **Link**: [learn.hashicorp.com/vault](https://learn.hashicorp.com/vault)
- **Why it's great**: Step-by-step tutorials from basic to advanced concepts

#### **Vault Production Hardening**
- **Link**: [vaultproject.io/docs/concepts/production](https://www.vaultproject.io/docs/concepts/production)
- **Why it's great**: Essential guide for production deployments and security

### 📝 Must-Read Blogs & Articles

#### **HashiCorp Blog - Vault**
- **Source**: HashiCorp
- **Link**: [hashicorp.com/blog/products/vault](https://www.hashicorp.com/blog/products/vault)
- **Why it's great**: Official updates and advanced use cases from Vault creators

#### **Vault Security Best Practices**
- **Source**: Aqua Security
- **Link**: [aquasec.com/cloud-native-academy/secrets-management/hashicorp-vault/](https://www.aquasec.com/cloud-native-academy/secrets-management/hashicorp-vault/)
- **Why it's great**: Production security patterns and threat model considerations

#### **Dynamic Secrets with Vault**
- **Source**: Medium
- **Link**: [medium.com/hashicorp-engineering/dynamic-database-credentials-with-vault-8e28ab1e84ee](https://medium.com/hashicorp-engineering/dynamic-database-credentials-with-vault-8e28ab1e84ee)
- **Why it's great**: Deep dive into dynamic secret generation patterns

### 🎓 Structured Courses

#### **HashiCorp Certified: Vault Associate**
- **Provider**: HashiCorp
- **Link**: [hashicorp.com/certification/vault-associate](https://www.hashicorp.com/certification/vault-associate)
- **Cost**: Paid certification
- **Why it's great**: Official certification with comprehensive training materials

#### **Securing Infrastructure with HashiCorp Vault**
- **Platform**: Pluralsight
- **Link**: [pluralsight.com/courses/hashicorp-vault-securing-infrastructure](https://www.pluralsight.com/courses/hashicorp-vault-securing-infrastructure)
- **Cost**: Paid
- **Why it's great**: Production-focused course with real-world scenarios

### 🛠️ Tools & Platforms

#### **Vault Playground**
- **Link**: [play.instruqt.com/hashicorp](https://play.instruqt.com/hashicorp)
- **Why it's great**: Interactive Vault tutorials in browser-based environments

#### **Vault Helm Chart**
- **Link**: [github.com/hashicorp/vault-helm](https://github.com/hashicorp/vault-helm)
- **Why it's great**: Official Helm chart for deploying Vault on Kubernetes

#### **Vault Operator**
- **Link**: [github.com/banzaicloud/bank-vaults](https://github.com/banzaicloud/bank-vaults)
- **Why it's great**: Kubernetes operator for managing Vault deployments and configuration

## Overview

HashiCorp Vault is a tool for securely accessing secrets and protecting sensitive data. It provides a unified interface to any secret while providing tight access control and recording a detailed audit log.

## Key Features

- **Secret Management**: Store and access secrets like API keys, passwords, certificates
- **Dynamic Secrets**: Generate secrets on-demand for specific services
- **Data Encryption**: Encrypt/decrypt data without storing it
- **Access Control**: Fine-grained policies and authentication methods
- **Audit Logging**: Complete audit trail of all secret access

## Common Use Cases

### Basic Secret Operations
```bash
# Start Vault dev server
vault server -dev

# Set environment
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='your-root-token'

# Store secrets
vault kv put secret/myapp/db username=dbuser password=supersecret
vault kv put secret/myapp/api key=abc123 endpoint=https://api.example.com

# Retrieve secrets
vault kv get secret/myapp/db
vault kv get -field=password secret/myapp/db
```

### Dynamic Database Secrets
```bash
# Enable database secrets engine
vault secrets enable database

# Configure PostgreSQL connection
vault write database/config/postgresql \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/myapp" \
    allowed_roles="readonly,readwrite" \
    username="vault" \
    password="vaultpass"

# Create role for dynamic credentials
vault write database/roles/readonly \
    db_name=postgresql \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";"

# Generate dynamic credentials
vault read database/creds/readonly
```

### Application Integration
```python
import hvac

# Python client example
client = hvac.Client(url='http://127.0.0.1:8200')
client.token = 'your-app-token'

# Read secret
response = client.secrets.kv.v2.read_secret_version(path='myapp/db')
db_creds = response['data']['data']
username = db_creds['username']
password = db_creds['password']

# Use secret in connection
connection_string = f"postgresql://{username}:{password}@db:5432/myapp"
```

## Authentication Methods

### Kubernetes Auth
```bash
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure Kubernetes auth
vault write auth/kubernetes/config \
    token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    kubernetes_host="https://kubernetes.default.svc" \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

# Create role for service account
vault write auth/kubernetes/role/myapp \
    bound_service_account_names=myapp \
    bound_service_account_namespaces=default \
    policies=myapp-policy \
    ttl=1h
```

### AppRole Auth
```bash
# Enable AppRole auth
vault auth enable approle

# Create role
vault write auth/approle/role/myapp \
    policies="myapp-policy" \
    token_ttl=1h \
    token_max_ttl=4h

# Get role credentials
vault read auth/approle/role/myapp/role-id
vault write -f auth/approle/role/myapp/secret-id
```

## Policies and Access Control

### Policy Definition
```hcl
# myapp-policy.hcl
path "secret/data/myapp/*" {
  capabilities = ["read"]
}

path "database/creds/readonly" {
  capabilities = ["read"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
```

```bash
# Apply policy
vault policy write myapp-policy myapp-policy.hcl

# List policies
vault policy list
```

## Production Setup

### HA Configuration
```hcl
# vault.hcl
ui = true

storage "consul" {
  address = "127.0.0.1:8500"
  path    = "vault/"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_cert_file = "/etc/vault/tls/vault.crt"
  tls_key_file  = "/etc/vault/tls/vault.key"
}

api_addr = "https://vault.example.com:8200"
cluster_addr = "https://vault-internal.example.com:8201"
```

### Auto-Unseal with Cloud KMS
```hcl
# AWS KMS auto-unseal
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "12345678-1234-1234-1234-123456789012"
}
```

## Monitoring and Maintenance

### Health Checks
```bash
# Check Vault status
vault status

# Health endpoint
curl https://vault.example.com:8200/v1/sys/health

# Seal status
vault operator seal-status
```

### Backup and Recovery
```bash
# Create snapshot (Enterprise)
vault operator raft snapshot save backup.snap

# Restore snapshot
vault operator raft snapshot restore backup.snap

# Backup policies and auth methods
vault policy list | xargs -I {} vault policy read {} > policies.hcl
```

## Best Practices

- Use least privilege access with specific policies
- Enable audit logging for compliance
- Implement proper authentication methods for each use case
- Regular secret rotation and credential lifecycle management
- Use auto-unseal for production deployments
- Monitor and alert on unusual access patterns
- Regular backups and disaster recovery testing

## Great Resources

- [Vault Official Documentation](https://www.vaultproject.io/docs) - Comprehensive Vault documentation and guides
- [Vault Learn](https://learn.hashicorp.com/vault) - Interactive tutorials and learning paths
- [Vault API Documentation](https://www.vaultproject.io/api-docs) - Complete REST API reference
- [Vault Helm Chart](https://github.com/hashicorp/vault-helm) - Official Kubernetes deployment
- [Vault Examples](https://github.com/hashicorp/vault-examples) - Practical implementation examples
- [Bank-Vaults](https://github.com/banzaicloud/bank-vaults) - Kubernetes operator for Vault
- [Vault Agent](https://www.vaultproject.io/docs/agent) - Vault agent for secret management automation