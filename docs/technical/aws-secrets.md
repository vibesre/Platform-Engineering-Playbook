# AWS Secrets Manager

AWS Secrets Manager is a fully managed service that helps you protect access to applications, services, and IT resources without the upfront investment and on-going maintenance costs of operating your own infrastructure.

## Core Concepts

### Key Features
- **Automatic Rotation**: Built-in rotation for databases, API keys, and other credentials
- **Fine-grained Access Control**: IAM-based permissions and resource policies  
- **Encryption**: Secrets encrypted at rest using AWS KMS
- **Audit Trail**: Integration with CloudTrail for comprehensive logging
- **Cross-region Replication**: Replicate secrets across multiple regions
- **Lambda Integration**: Trigger functions on secret events

### Supported Secret Types
- Database credentials (RDS, DocumentDB, Redshift)
- API keys and tokens
- SSH keys and certificates
- Application configuration
- Third-party service credentials

## Installation and Setup

### AWS CLI Configuration
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure credentials
aws configure
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region: us-east-1
# Default output format: json

# Test access
aws secretsmanager list-secrets
```

### IAM Policy for Secrets Manager
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "SecretsManagerFullAccess",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret",
        "secretsmanager:PutSecretValue",
        "secretsmanager:CreateSecret",
        "secretsmanager:DeleteSecret",
        "secretsmanager:UpdateSecret",
        "secretsmanager:RestoreSecret",
        "secretsmanager:RotateSecret",
        "secretsmanager:TagResource",
        "secretsmanager:UntagResource",
        "secretsmanager:ListSecrets",
        "secretsmanager:GetResourcePolicy",
        "secretsmanager:PutResourcePolicy"
      ],
      "Resource": "*"
    },
    {
      "Sid": "KMSAccess",
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:Encrypt",
        "kms:GenerateDataKey",
        "kms:DescribeKey"
      ],
      "Resource": "*"
    }
  ]
}
```

## Secret Management Operations

### Creating Secrets
```bash
# Create a simple secret
aws secretsmanager create-secret \
  --name "prod/myapp/database" \
  --description "Database credentials for production application" \
  --secret-string '{"username":"admin","password":"MyS3cur3P@ssw0rd"}'

# Create secret from file
echo '{"api_key":"sk-1234567890","endpoint":"https://api.example.com"}' > secret.json
aws secretsmanager create-secret \
  --name "prod/myapp/api-keys" \
  --secret-string file://secret.json

# Create secret with KMS key
aws secretsmanager create-secret \
  --name "prod/myapp/encryption-keys" \
  --kms-key-id "arn:aws:kms:us-east-1:123456789012:key/abcd1234-a123-456a-a12b-a123b4cd56ef" \
  --secret-string '{"encryption_key":"base64encodedkey"}'

# Create secret with tags
aws secretsmanager create-secret \
  --name "prod/myapp/oauth" \
  --secret-string '{"client_id":"abc123","client_secret":"xyz789"}' \
  --tags '[{"Key":"Environment","Value":"Production"},{"Key":"Application","Value":"MyApp"}]'
```

### Retrieving Secrets
```bash
# Get current secret value
aws secretsmanager get-secret-value \
  --secret-id "prod/myapp/database" \
  --query SecretString --output text

# Get specific version
aws secretsmanager get-secret-value \
  --secret-id "prod/myapp/database" \
  --version-id "AWSCURRENT"

# Get previous version
aws secretsmanager get-secret-value \
  --secret-id "prod/myapp/database" \
  --version-stage "AWSPENDING"

# Parse JSON secret
aws secretsmanager get-secret-value \
  --secret-id "prod/myapp/database" \
  --query SecretString --output text | jq -r '.username'
```

### Updating Secrets
```bash
# Update secret value
aws secretsmanager update-secret \
  --secret-id "prod/myapp/database" \
  --secret-string '{"username":"admin","password":"NewS3cur3P@ssw0rd"}'

# Update from file
aws secretsmanager put-secret-value \
  --secret-id "prod/myapp/api-keys" \
  --secret-string file://updated-secret.json

# Update description and KMS key
aws secretsmanager update-secret \
  --secret-id "prod/myapp/database" \
  --description "Updated database credentials with enhanced security" \
  --kms-key-id "arn:aws:kms:us-east-1:123456789012:key/new-key-id"
```

## Automatic Rotation

### Database Rotation Setup
```bash
# Create rotation for RDS MySQL
aws secretsmanager rotate-secret \
  --secret-id "prod/myapp/database" \
  --rotation-rules AutomaticallyAfterDays=30 \
  --rotation-lambda-arn "arn:aws:lambda:us-east-1:123456789012:function:SecretsManagerRDSMySQLRotationSingleUser"

# Create rotation for RDS PostgreSQL  
aws secretsmanager rotate-secret \
  --secret-id "prod/myapp/postgres" \
  --rotation-rules AutomaticallyAfterDays=30 \
  --rotation-lambda-arn "arn:aws:lambda:us-east-1:123456789012:function:SecretsManagerRDSPostgreSQLRotationSingleUser"

# Custom rotation Lambda
aws secretsmanager rotate-secret \
  --secret-id "prod/myapp/api-keys" \
  --rotation-rules AutomaticallyAfterDays=7 \
  --rotation-lambda-arn "arn:aws:lambda:us-east-1:123456789012:function:CustomApiKeyRotation"
```

### Lambda Rotation Function
```python
import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """AWS Secrets Manager rotation function for API keys"""
    
    client = boto3.client('secretsmanager')
    secret_arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']
    
    # Get secret metadata
    metadata = client.describe_secret(SecretId=secret_arn)
    
    if 'RotationEnabled' not in metadata or not metadata['RotationEnabled']:
        logger.error("Secret %s is not enabled for rotation", secret_arn)
        raise ValueError("Secret is not enabled for rotation")
    
    versions = metadata.get('VersionIdsToStages', {})
    
    if token not in versions:
        logger.error("Secret version %s has no stage for rotation", token)
        raise ValueError("Secret version has no stage for rotation")
    
    if step == "createSecret":
        create_secret(client, secret_arn, token)
    elif step == "setSecret":
        set_secret(client, secret_arn, token)
    elif step == "testSecret":
        test_secret(client, secret_arn, token)
    elif step == "finishSecret":
        finish_secret(client, secret_arn, token)
    else:
        logger.error("Invalid step parameter %s", step)
        raise ValueError("Invalid step parameter")

def create_secret(client, secret_arn, token):
    """Generate new secret version"""
    try:
        # Get current secret
        current_secret = client.get_secret_value(
            SecretId=secret_arn,
            VersionStage="AWSCURRENT"
        )
        
        # Parse current secret
        secret_dict = json.loads(current_secret['SecretString'])
        
        # Generate new API key (example implementation)
        new_api_key = generate_new_api_key(secret_dict.get('provider'))
        secret_dict['api_key'] = new_api_key
        
        # Store new version
        client.put_secret_value(
            SecretId=secret_arn,
            VersionId=token,
            SecretString=json.dumps(secret_dict),
            VersionStages=['AWSPENDING']
        )
        
        logger.info("Created new secret version %s", token)
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceExistsException':
            logger.info("Secret version %s already exists", token)
        else:
            raise e

def set_secret(client, secret_arn, token):
    """Configure the service to use the new secret"""
    try:
        # Get pending secret
        pending_secret = client.get_secret_value(
            SecretId=secret_arn,
            VersionId=token,
            VersionStage="AWSPENDING"
        )
        
        secret_dict = json.loads(pending_secret['SecretString'])
        
        # Update service configuration with new API key
        update_service_config(secret_dict)
        
        logger.info("Updated service configuration with new secret")
        
    except Exception as e:
        logger.error("Failed to set secret: %s", str(e))
        raise e

def test_secret(client, secret_arn, token):
    """Test the new secret"""
    try:
        # Get pending secret
        pending_secret = client.get_secret_value(
            SecretId=secret_arn,
            VersionId=token,
            VersionStage="AWSPENDING"
        )
        
        secret_dict = json.loads(pending_secret['SecretString'])
        
        # Test the new API key
        if test_api_key(secret_dict['api_key']):
            logger.info("New secret version %s tested successfully", token)
        else:
            raise Exception("Secret test failed")
            
    except Exception as e:
        logger.error("Failed to test secret: %s", str(e))
        raise e

def finish_secret(client, secret_arn, token):
    """Finalize the rotation"""
    try:
        # Move AWSCURRENT to AWSPENDING
        client.update_secret_version_stage(
            SecretId=secret_arn,
            VersionStage="AWSCURRENT",
            MoveToVersionId=token,
            RemoveFromVersionId=get_current_version(client, secret_arn)
        )
        
        logger.info("Rotation completed for secret %s", secret_arn)
        
    except Exception as e:
        logger.error("Failed to finish rotation: %s", str(e))
        raise e

def generate_new_api_key(provider):
    """Generate new API key - implement based on your provider"""
    # This is a placeholder - implement actual key generation
    import secrets
    return f"ak_{secrets.token_urlsafe(32)}"

def update_service_config(secret_dict):
    """Update service configuration - implement based on your needs"""
    # Placeholder for service-specific configuration update
    pass

def test_api_key(api_key):
    """Test API key validity - implement based on your service"""
    # Placeholder for API key testing
    return True

def get_current_version(client, secret_arn):
    """Get current version ID"""
    metadata = client.describe_secret(SecretId=secret_arn)
    versions = metadata.get('VersionIdsToStages', {})
    
    for version_id, stages in versions.items():
        if 'AWSCURRENT' in stages:
            return version_id
    
    return None
```

## Application Integration

### Python/Boto3 Integration
```python
import boto3
import json
import logging
from botocore.exceptions import ClientError
from functools import lru_cache
from typing import Dict, Any, Optional

class SecretsManager:
    def __init__(self, region_name: str = 'us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region_name)
        self.logger = logging.getLogger(__name__)
    
    @lru_cache(maxsize=128)
    def get_secret(self, secret_id: str, version_stage: str = 'AWSCURRENT') -> Dict[str, Any]:
        """
        Retrieve and cache secret value
        """
        try:
            response = self.client.get_secret_value(
                SecretId=secret_id,
                VersionStage=version_stage
            )
            
            secret_string = response.get('SecretString')
            if secret_string:
                return json.loads(secret_string)
            
            # Handle binary secrets
            secret_binary = response.get('SecretBinary')
            if secret_binary:
                return {'binary': secret_binary}
                
            raise ValueError("No secret value found")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == 'ResourceNotFoundException':
                self.logger.error(f"Secret {secret_id} not found")
            elif error_code == 'InvalidRequestException':
                self.logger.error(f"Invalid request for secret {secret_id}")
            elif error_code == 'InvalidParameterException':
                self.logger.error(f"Invalid parameter for secret {secret_id}")
            elif error_code == 'DecryptionFailureException':
                self.logger.error(f"Decryption failed for secret {secret_id}")
            elif error_code == 'InternalServiceErrorException':
                self.logger.error(f"Internal service error for secret {secret_id}")
            
            raise e
    
    def get_secret_value(self, secret_id: str, key: str, default: Any = None) -> Any:
        """
        Get specific value from JSON secret
        """
        try:
            secret = self.get_secret(secret_id)
            return secret.get(key, default)
        except Exception as e:
            self.logger.error(f"Failed to get secret value {key} from {secret_id}: {e}")
            return default
    
    def create_secret(self, name: str, secret_value: Dict[str, Any], 
                     description: str = '', kms_key_id: Optional[str] = None,
                     tags: Optional[Dict[str, str]] = None) -> str:
        """
        Create a new secret
        """
        try:
            kwargs = {
                'Name': name,
                'SecretString': json.dumps(secret_value),
                'Description': description
            }
            
            if kms_key_id:
                kwargs['KmsKeyId'] = kms_key_id
            
            if tags:
                kwargs['Tags'] = [{'Key': k, 'Value': v} for k, v in tags.items()]
            
            response = self.client.create_secret(**kwargs)
            self.logger.info(f"Created secret {name}")
            return response['ARN']
            
        except ClientError as e:
            self.logger.error(f"Failed to create secret {name}: {e}")
            raise e
    
    def update_secret(self, secret_id: str, secret_value: Dict[str, Any]) -> None:
        """
        Update secret value
        """
        try:
            self.client.update_secret(
                SecretId=secret_id,
                SecretString=json.dumps(secret_value)
            )
            
            # Clear cache for this secret
            self.get_secret.cache_clear()
            self.logger.info(f"Updated secret {secret_id}")
            
        except ClientError as e:
            self.logger.error(f"Failed to update secret {secret_id}: {e}")
            raise e
    
    def delete_secret(self, secret_id: str, force_delete: bool = False, 
                     recovery_window: int = 30) -> None:
        """
        Delete secret with optional recovery window
        """
        try:
            kwargs = {'SecretId': secret_id}
            
            if force_delete:
                kwargs['ForceDeleteWithoutRecovery'] = True
            else:
                kwargs['RecoveryWindowInDays'] = recovery_window
            
            self.client.delete_secret(**kwargs)
            
            # Clear cache
            self.get_secret.cache_clear()
            self.logger.info(f"Deleted secret {secret_id}")
            
        except ClientError as e:
            self.logger.error(f"Failed to delete secret {secret_id}: {e}")
            raise e
    
    def list_secrets(self, filters: Optional[Dict[str, Any]] = None) -> list:
        """
        List secrets with optional filters
        """
        try:
            kwargs = {}
            if filters:
                kwargs['Filters'] = []
                for key, value in filters.items():
                    kwargs['Filters'].append({
                        'Key': key,
                        'Values': [value] if isinstance(value, str) else value
                    })
            
            paginator = self.client.get_paginator('list_secrets')
            secrets = []
            
            for page in paginator.paginate(**kwargs):
                secrets.extend(page['SecretList'])
            
            return secrets
            
        except ClientError as e:
            self.logger.error(f"Failed to list secrets: {e}")
            raise e

# Usage example
secrets_manager = SecretsManager(region_name='us-east-1')

# Application configuration class
class Config:
    def __init__(self):
        self.secrets = SecretsManager()
        self._db_credentials = None
        self._api_keys = None
    
    @property
    def database_url(self) -> str:
        if not self._db_credentials:
            self._db_credentials = self.secrets.get_secret('prod/myapp/database')
        
        creds = self._db_credentials
        return f"postgresql://{creds['username']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['database']}"
    
    @property
    def api_key(self) -> str:
        if not self._api_keys:
            self._api_keys = self.secrets.get_secret('prod/myapp/api-keys')
        
        return self._api_keys['api_key']
    
    @property
    def jwt_secret(self) -> str:
        return self.secrets.get_secret_value('prod/myapp/auth', 'jwt_secret')
    
    def refresh_secrets(self):
        """Refresh cached secrets"""
        self.secrets.get_secret.cache_clear()
        self._db_credentials = None
        self._api_keys = None

# Usage in application
config = Config()

# Database connection
import psycopg2
conn = psycopg2.connect(config.database_url)

# API client
import requests
headers = {'Authorization': f'Bearer {config.api_key}'}
response = requests.get('https://api.example.com/data', headers=headers)
```

### Node.js Integration
```javascript
const AWS = require('aws-sdk');

class SecretsManager {
    constructor(region = 'us-east-1') {
        this.client = new AWS.SecretsManager({ region });
        this.cache = new Map();
        this.cacheTTL = 300000; // 5 minutes
    }

    async getSecret(secretId, versionStage = 'AWSCURRENT') {
        const cacheKey = `${secretId}:${versionStage}`;
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < this.cacheTTL) {
            return cached.value;
        }

        try {
            const response = await this.client.getSecretValue({
                SecretId: secretId,
                VersionStage: versionStage
            }).promise();

            let secretValue;
            if (response.SecretString) {
                secretValue = JSON.parse(response.SecretString);
            } else if (response.SecretBinary) {
                secretValue = { binary: response.SecretBinary };
            } else {
                throw new Error('No secret value found');
            }

            // Cache the result
            this.cache.set(cacheKey, {
                value: secretValue,
                timestamp: Date.now()
            });

            return secretValue;
        } catch (error) {
            console.error(`Failed to get secret ${secretId}:`, error);
            throw error;
        }
    }

    async getSecretValue(secretId, key, defaultValue = null) {
        try {
            const secret = await this.getSecret(secretId);
            return secret[key] !== undefined ? secret[key] : defaultValue;
        } catch (error) {
            console.error(`Failed to get secret value ${key} from ${secretId}:`, error);
            return defaultValue;
        }
    }

    async createSecret(name, secretValue, options = {}) {
        const params = {
            Name: name,
            SecretString: JSON.stringify(secretValue),
            Description: options.description || '',
            ...options
        };

        if (options.kmsKeyId) {
            params.KmsKeyId = options.kmsKeyId;
        }

        if (options.tags) {
            params.Tags = Object.entries(options.tags).map(([Key, Value]) => ({ Key, Value }));
        }

        try {
            const response = await this.client.createSecret(params).promise();
            console.log(`Created secret ${name}`);
            return response.ARN;
        } catch (error) {
            console.error(`Failed to create secret ${name}:`, error);
            throw error;
        }
    }

    async updateSecret(secretId, secretValue) {
        try {
            await this.client.updateSecret({
                SecretId: secretId,
                SecretString: JSON.stringify(secretValue)
            }).promise();

            // Clear cache
            this.clearCache(secretId);
            console.log(`Updated secret ${secretId}`);
        } catch (error) {
            console.error(`Failed to update secret ${secretId}:`, error);
            throw error;
        }
    }

    async deleteSecret(secretId, options = {}) {
        const params = {
            SecretId: secretId,
            ForceDeleteWithoutRecovery: options.forceDelete || false
        };

        if (!options.forceDelete) {
            params.RecoveryWindowInDays = options.recoveryWindow || 30;
        }

        try {
            await this.client.deleteSecret(params).promise();
            this.clearCache(secretId);
            console.log(`Deleted secret ${secretId}`);
        } catch (error) {
            console.error(`Failed to delete secret ${secretId}:`, error);
            throw error;
        }
    }

    clearCache(secretId = null) {
        if (secretId) {
            // Clear specific secret from cache
            for (const key of this.cache.keys()) {
                if (key.startsWith(`${secretId}:`)) {
                    this.cache.delete(key);
                }
            }
        } else {
            // Clear entire cache
            this.cache.clear();
        }
    }
}

// Configuration management
class Config {
    constructor() {
        this.secrets = new SecretsManager();
    }

    async getDatabaseConfig() {
        const dbSecret = await this.secrets.getSecret('prod/myapp/database');
        return {
            host: dbSecret.host,
            port: dbSecret.port,
            database: dbSecret.database,
            username: dbSecret.username,
            password: dbSecret.password,
            ssl: true
        };
    }

    async getApiKeys() {
        return await this.secrets.getSecret('prod/myapp/api-keys');
    }

    async getJwtSecret() {
        return await this.secrets.getSecretValue('prod/myapp/auth', 'jwt_secret');
    }
}

// Usage example
const config = new Config();

// Express.js middleware for secret-based configuration
async function setupApp() {
    const express = require('express');
    const app = express();

    // Get database configuration
    const dbConfig = await config.getDatabaseConfig();
    console.log('Database configured for host:', dbConfig.host);

    // Get API keys for external services
    const apiKeys = await config.getApiKeys();
    
    // Middleware to add API key to requests
    app.use((req, res, next) => {
        req.apiKey = apiKeys.external_service_key;
        next();
    });

    return app;
}

module.exports = { SecretsManager, Config };
```

## Terraform Configuration

### Basic Secrets Setup
```hcl
# secrets.tf
resource "aws_secretsmanager_secret" "database_credentials" {
  name                    = "prod/myapp/database"
  description             = "Database credentials for production application"
  recovery_window_in_days = 30

  replica {
    region = "us-west-2"
  }

  tags = {
    Environment = "production"
    Application = "myapp"
    SecretType  = "database"
  }
}

resource "aws_secretsmanager_secret_version" "database_credentials" {
  secret_id = aws_secretsmanager_secret.database_credentials.id
  secret_string = jsonencode({
    username = var.db_username
    password = var.db_password
    host     = aws_rds_instance.main.endpoint
    port     = aws_rds_instance.main.port
    database = aws_rds_instance.main.db_name
  })

  lifecycle {
    ignore_changes = [secret_string]
  }
}

resource "aws_secretsmanager_secret" "api_keys" {
  name                    = "prod/myapp/api-keys"
  description             = "API keys for external services"
  kms_key_id              = aws_kms_key.secrets.arn
  recovery_window_in_days = 7

  tags = {
    Environment = "production"
    Application = "myapp"
    SecretType  = "api-keys"
  }
}

resource "aws_secretsmanager_secret_version" "api_keys" {
  secret_id = aws_secretsmanager_secret.api_keys.id
  secret_string = jsonencode({
    external_service_key = var.external_api_key
    payment_gateway_key  = var.payment_api_key
    email_service_key    = var.email_api_key
  })
}

# KMS key for secret encryption
resource "aws_kms_key" "secrets" {
  description             = "KMS key for Secrets Manager"
  deletion_window_in_days = 7

  tags = {
    Name        = "secrets-manager-key"
    Environment = "production"
  }
}

resource "aws_kms_alias" "secrets" {
  name          = "alias/secrets-manager"
  target_key_id = aws_kms_key.secrets.key_id
}

# IAM role for applications
resource "aws_iam_role" "app_secrets_role" {
  name = "app-secrets-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "app_secrets_policy" {
  name        = "app-secrets-policy"
  description = "Policy for application to access secrets"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = [
          aws_secretsmanager_secret.database_credentials.arn,
          aws_secretsmanager_secret.api_keys.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:DescribeKey"
        ]
        Resource = aws_kms_key.secrets.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "app_secrets_policy_attachment" {
  role       = aws_iam_role.app_secrets_role.name
  policy_arn = aws_iam_policy.app_secrets_policy.arn
}
```

### Automatic Rotation Setup
```hcl
# rotation.tf
resource "aws_secretsmanager_secret_rotation" "database_rotation" {
  secret_id           = aws_secretsmanager_secret.database_credentials.id
  rotation_lambda_arn = aws_lambda_function.rds_rotation.arn

  rotation_rules {
    automatically_after_days = 30
  }

  depends_on = [aws_lambda_permission.secrets_manager_rotation]
}

resource "aws_lambda_function" "rds_rotation" {
  filename         = "rds-rotation-function.zip"
  function_name    = "rds-rotation-function"
  role            = aws_iam_role.rotation_lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("rds-rotation-function.zip")
  runtime         = "python3.9"
  timeout         = 30

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.rotation_lambda.id]
  }

  environment {
    variables = {
      SECRETS_MANAGER_ENDPOINT = "https://secretsmanager.${var.aws_region}.amazonaws.com"
    }
  }

  tags = {
    Environment = "production"
    Purpose     = "secret-rotation"
  }
}

resource "aws_iam_role" "rotation_lambda_role" {
  name = "rotation-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "rotation_lambda_policy" {
  name = "rotation-lambda-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:DescribeSecret",
          "secretsmanager:GetSecretValue",
          "secretsmanager:PutSecretValue",
          "secretsmanager:UpdateSecretVersionStage"
        ]
        Resource = aws_secretsmanager_secret.database_credentials.arn
      },
      {
        Effect = "Allow"
        Action = [
          "rds:ModifyDBInstance",
          "rds:DescribeDBInstances"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DeleteNetworkInterface",
          "ec2:DescribeNetworkInterfaces"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rotation_lambda_policy_attachment" {
  role       = aws_iam_role.rotation_lambda_role.name
  policy_arn = aws_iam_policy.rotation_lambda_policy.arn
}

resource "aws_lambda_permission" "secrets_manager_rotation" {
  statement_id  = "AllowExecutionFromSecretsManager"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rds_rotation.function_name
  principal     = "secretsmanager.amazonaws.com"
}

resource "aws_security_group" "rotation_lambda" {
  name_prefix = "rotation-lambda-"
  vpc_id      = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rotation-lambda-sg"
  }
}
```

## Monitoring and Alerting

### CloudWatch Monitoring
```bash
# Create CloudWatch alarms for secrets
aws cloudwatch put-metric-alarm \
  --alarm-name "SecretsManager-RotationFailures" \
  --alarm-description "Alert on secret rotation failures" \
  --metric-name "RotationFailed" \
  --namespace "AWS/SecretsManager" \
  --statistic "Sum" \
  --period 300 \
  --threshold 1 \
  --comparison-operator "GreaterThanOrEqualToThreshold" \
  --evaluation-periods 1 \
  --alarm-actions "arn:aws:sns:us-east-1:123456789012:alerts"

# Monitor secret access patterns
aws cloudwatch put-metric-alarm \
  --alarm-name "SecretsManager-UnusualAccess" \
  --alarm-description "Alert on unusual secret access patterns" \
  --metric-name "GetSecretValue" \
  --namespace "AWS/SecretsManager" \
  --statistic "Sum" \
  --period 3600 \
  --threshold 1000 \
  --comparison-operator "GreaterThanThreshold" \
  --evaluation-periods 1
```

### CloudTrail Logging
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudtrail:LookupEvents"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "cloudtrail:EventName": [
            "GetSecretValue",
            "CreateSecret",
            "DeleteSecret",
            "UpdateSecret",
            "RotateSecret"
          ]
        }
      }
    }
  ]
}
```

## Best Practices

### Security Best Practices
```bash
# Use least privilege IAM policies
# Example: Resource-specific access
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:region:account:secret:prod/myapp/*"
    }
  ]
}

# Enable cross-region replication for critical secrets
aws secretsmanager replicate-secret-to-regions \
  --secret-id "prod/myapp/database" \
  --add-replica-regions Region=us-west-2,KmsKeyId=alias/secrets-west

# Use resource-based policies for cross-account access
aws secretsmanager put-resource-policy \
  --secret-id "prod/myapp/shared-key" \
  --resource-policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": "arn:aws:iam::123456789012:role/CrossAccountRole"
        },
        "Action": "secretsmanager:GetSecretValue",
        "Resource": "*"
      }
    ]
  }'
```

### Cost Optimization
```bash
# Clean up unused secrets
aws secretsmanager list-secrets \
  --query 'SecretList[?LastAccessedDate==null].[Name,ARN]' \
  --output table

# Set appropriate recovery windows
aws secretsmanager delete-secret \
  --secret-id "old/unused/secret" \
  --recovery-window-in-days 7  # Minimum for cost savings

# Use appropriate rotation intervals
# Daily rotation: High security, higher cost
# Monthly rotation: Balanced approach
# Quarterly rotation: Lower cost, adequate for most use cases
```

## Resources

- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/)
- [Secrets Manager Pricing](https://aws.amazon.com/secrets-manager/pricing/)
- [Rotation Templates](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
- [Best Practices Guide](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- [AWS SDK Documentation](https://docs.aws.amazon.com/sdk-for-python/v1/developer-guide/aws-secretsmanager.html)
- [CloudFormation Templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html)
- [Security Best Practices](https://docs.aws.amazon.com/secretsmanager/latest/userguide/security.html)
- [Troubleshooting Guide](https://docs.aws.amazon.com/secretsmanager/latest/userguide/troubleshooting.html)
- [Integration Examples](https://github.com/aws-samples/aws-secrets-manager-rotation-lambdas)
- [Terraform Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/secretsmanager_secret)