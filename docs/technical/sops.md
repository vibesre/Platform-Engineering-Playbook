# SOPS (Secrets OPerationS)

SOPS is an editor of encrypted files that supports YAML, JSON, ENV, INI and BINARY formats and encrypts with AWS KMS, GCP KMS, Azure Key Vault, age, and PGP.

## Installation

### Binary Installation
```bash
# Linux
curl -LO https://github.com/mozilla/sops/releases/latest/download/sops-v3.8.1.linux.amd64
chmod +x sops-v3.8.1.linux.amd64
sudo mv sops-v3.8.1.linux.amd64 /usr/local/bin/sops

# macOS
brew install sops

# Or download directly
curl -LO https://github.com/mozilla/sops/releases/latest/download/sops-v3.8.1.darwin.amd64
chmod +x sops-v3.8.1.darwin.amd64
sudo mv sops-v3.8.1.darwin.amd64 /usr/local/bin/sops

# Verify installation
sops --version
```

### Package Manager Installation
```bash
# Ubuntu/Debian
wget -qO - https://apt.fury.io/mozilla/gpg.key | sudo apt-key add -
echo "deb https://apt.fury.io/mozilla/ /" | sudo tee /etc/apt/sources.list.d/fury.list
sudo apt update && sudo apt install sops

# CentOS/RHEL
sudo yum install https://github.com/mozilla/sops/releases/latest/download/sops-3.8.1-1.x86_64.rpm

# Arch Linux
yay -S sops
```

## Key Management Setup

### AWS KMS Configuration
```bash
# Create KMS key for SOPS
aws kms create-key \
  --description "SOPS encryption key for secrets" \
  --usage ENCRYPT_DECRYPT \
  --key-spec SYMMETRIC_DEFAULT

# Create alias for easier reference
aws kms create-alias \
  --alias-name alias/sops-secrets \
  --target-key-id arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012

# Set IAM permissions
cat > sops-kms-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:ReEncrypt*",
        "kms:GenerateDataKey*",
        "kms:DescribeKey"
      ],
      "Resource": "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012"
    }
  ]
}
EOF

aws iam create-policy \
  --policy-name SOPSKMSPolicy \
  --policy-document file://sops-kms-policy.json
```

### GCP KMS Configuration
```bash
# Enable Cloud KMS API
gcloud services enable cloudkms.googleapis.com

# Create key ring
gcloud kms keyrings create sops-keyring \
  --location=global

# Create encryption key
gcloud kms keys create sops-key \
  --location=global \
  --keyring=sops-keyring \
  --purpose=encryption

# Get key resource name
gcloud kms keys list \
  --location=global \
  --keyring=sops-keyring

# Grant access to service account
gcloud kms keys add-iam-policy-binding sops-key \
  --location=global \
  --keyring=sops-keyring \
  --member=serviceAccount:your-service-account@project-id.iam.gserviceaccount.com \
  --role=roles/cloudkms.cryptoKeyEncrypterDecrypter
```

### Age Key Configuration
```bash
# Generate age key pair
age-keygen -o keys.txt

# View public key
cat keys.txt | grep "public key"

# Set environment variable
export SOPS_AGE_KEY_FILE=./keys.txt

# Or use age recipients
export SOPS_AGE_RECIPIENTS=age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### PGP Configuration
```bash
# Generate PGP key
gpg --full-generate-key

# List keys
gpg --list-secret-keys --keyid-format LONG

# Export public key
gpg --armor --export KEY_ID > public.asc

# Import public key on another machine
gpg --import public.asc

# Trust the key
gpg --edit-key KEY_ID
# Type: trust
# Select: 5 (I trust ultimately)
# Type: quit
```

## Configuration Files

### SOPS Configuration File
```yaml
# .sops.yaml
creation_rules:
  # Default rule for all files
  - path_regex: \.yaml$
    kms: 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012'
    aws_profile: default
    
  # Specific rule for production secrets
  - path_regex: prod/.*\.yaml$
    kms: 'arn:aws:kms:us-east-1:123456789012:key/prod-key-id'
    aws_profile: production
    
  # Development environment with age
  - path_regex: dev/.*\.yaml$
    age: 'age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    
  # JSON files with GCP KMS
  - path_regex: \.json$
    gcp_kms: 'projects/my-project/locations/global/keyRings/sops-keyring/cryptoKeys/sops-key'
    
  # Environment files with PGP
  - path_regex: \.env$
    pgp: 'FBC7B9E2A4F9289AC0C1D4843D16CEE4A27381B4'
    
  # Multiple keys for high availability
  - path_regex: critical/.*\.yaml$
    kms: 'arn:aws:kms:us-east-1:123456789012:key/key1,arn:aws:kms:us-west-2:123456789012:key/key2'
    pgp: 'KEY1_FINGERPRINT,KEY2_FINGERPRINT'
    
  # Encrypted suffix rule
  - encrypted_regex: '^(password|secret|key|token)$'
    kms: 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012'
```

### Environment-specific Configuration
```yaml
# config/prod/.sops.yaml
creation_rules:
  - kms: 'arn:aws:kms:us-east-1:123456789012:key/prod-key'
    aws_profile: production
    encrypted_regex: '^(password|secret|key|token|DATABASE_URL|API_KEY)$'
    
# config/staging/.sops.yaml  
creation_rules:
  - kms: 'arn:aws:kms:us-east-1:123456789012:key/staging-key'
    aws_profile: staging
    encrypted_regex: '^(password|secret|key|token)$'
    
# config/dev/.sops.yaml
creation_rules:
  - age: 'age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    encrypted_regex: '^(password|secret|key|token)$'
```

## Basic Operations

### Creating and Editing Encrypted Files
```bash
# Create new encrypted YAML file
sops secrets.yaml

# This opens your editor with a template:
example_key: example_value
#EOS

# After saving, the file becomes encrypted:
example_key: ENC[AES256_GCM,data:Tr7o1F8=,iv:HzBZXSQlXwVhpJY=,aad:1234=,tag:tAg==]
sops:
    kms:
        - arn: arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012
          created_at: '2024-01-15T10:30:00Z'
          enc: AQECAHhM...
    gcp_kms: []
    azure_kv: []
    lastmodified: '2024-01-15T10:30:00Z'
    mac: ENC[AES256_GCM,data:MaCVaLuE=,type:str]
    pgp: []
    version: 3.8.1

# Edit existing encrypted file
sops secrets.yaml

# Create encrypted JSON file
sops secrets.json

# Create encrypted environment file
sops .env.encrypted
```

### Working with Different File Formats
```bash
# YAML file
cat > secrets.yaml << EOF
database:
  host: localhost
  port: 5432
  username: admin
  password: secret123
api_keys:
  stripe: sk_test_123456
  sendgrid: SG.abcdef123456
oauth:
  client_id: oauth_client_123
  client_secret: oauth_secret_456
EOF

# Encrypt the file
sops -e -i secrets.yaml

# JSON file
cat > secrets.json << EOF
{
  "database": {
    "password": "secret123",
    "connection_string": "postgresql://user:pass@host:5432/db"
  },
  "api_keys": {
    "stripe": "sk_test_123456",
    "aws_access_key": "AKIAIOSFODNN7EXAMPLE"
  }
}
EOF

# Encrypt JSON
sops -e -i secrets.json

# Environment file
cat > .env.encrypted << EOF
DATABASE_PASSWORD=secret123
API_KEY=sk_test_123456
JWT_SECRET=super-secret-jwt-key
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
EOF

# Encrypt environment file
sops -e -i .env.encrypted

# INI file
cat > config.ini << EOF
[database]
password = secret123
connection_string = postgresql://user:pass@host:5432/db

[api]
stripe_key = sk_test_123456
sendgrid_key = SG.abcdef123456
EOF

# Encrypt INI file
sops -e -i config.ini
```

### Decryption and Viewing
```bash
# Decrypt and view content
sops -d secrets.yaml

# Decrypt to stdout
sops -d secrets.yaml > decrypted-secrets.yaml

# Decrypt in place (dangerous!)
sops -d -i secrets.yaml

# Extract specific values
sops -d --extract '["database"]["password"]' secrets.yaml
sops -d --extract '["api_keys"]["stripe"]' secrets.json

# Decrypt and pipe to other commands
sops -d secrets.yaml | grep password
sops -d .env.encrypted | source /dev/stdin
```

## Advanced Usage

### Partial Encryption
```yaml
# Only encrypt specific fields
# .sops.yaml
creation_rules:
  - path_regex: \.yaml$
    kms: 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012'
    encrypted_regex: '^(password|secret|key|token|private_key)$'

# Example file (config.yaml)
app_name: myapp
version: 1.0.0
debug: true
database:
  host: localhost
  port: 5432
  username: admin
  password: secret123  # This will be encrypted
api_settings:
  timeout: 30
  retry_count: 3
  api_key: sk_test_123456  # This will be encrypted
logging:
  level: info
  file: /var/log/app.log
```

### Key Rotation
```bash
# Add new key to existing file
sops -r -k 'arn:aws:kms:us-east-1:123456789012:key/new-key-id' secrets.yaml

# Remove old key
sops -r --rm-kms 'arn:aws:kms:us-east-1:123456789012:key/old-key-id' secrets.yaml

# Rotate to new PGP key
sops -r --rm-pgp 'OLD_KEY_FINGERPRINT' --add-pgp 'NEW_KEY_FINGERPRINT' secrets.yaml

# Rotate with age
sops -r --rm-age 'old-age-key' --add-age 'new-age-key' secrets.yaml
```

### Tree Operations
```bash
# Set specific tree path
sops --set '["database"]["password"] "new-password"' secrets.yaml

# Unset tree path
sops --unset '["api_keys"]["deprecated_key"]' secrets.yaml

# Show tree structure
sops --tree secrets.yaml

# Show tree with types
sops --tree --show-tree-types secrets.yaml
```

## Integration with Applications

### Shell Integration
```bash
#!/bin/bash
# load-secrets.sh

# Load encrypted environment variables
eval "$(sops -d .env.encrypted)"

# Use the variables
echo "Connecting to database at $DATABASE_HOST"
psql "$DATABASE_CONNECTION_STRING"

# Alternative: Export to current shell
set -a  # Mark variables for export
source <(sops -d .env.encrypted)
set +a  # Unmark variables for export
```

### Docker Integration
```dockerfile
# Dockerfile
FROM alpine:latest

# Install sops
RUN apk add --no-cache curl && \
    curl -LO https://github.com/mozilla/sops/releases/latest/download/sops-v3.8.1.linux.amd64 && \
    chmod +x sops-v3.8.1.linux.amd64 && \
    mv sops-v3.8.1.linux.amd64 /usr/local/bin/sops

# Copy encrypted secrets
COPY secrets.yaml /app/

# Copy age key or configure AWS credentials
COPY keys.txt /app/

# Start script that decrypts secrets
COPY start.sh /app/
RUN chmod +x /app/start.sh

WORKDIR /app
CMD ["./start.sh"]
```

```bash
#!/bin/bash
# start.sh

# Set age key file
export SOPS_AGE_KEY_FILE=/app/keys.txt

# Decrypt secrets and export as environment variables
eval "$(sops -d --output-type dotenv secrets.yaml)"

# Start your application
exec your-app
```

### Kubernetes Integration
```yaml
# secret-generator.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sops-decrypt-script
data:
  decrypt.sh: |
    #!/bin/bash
    export SOPS_AGE_KEY_FILE=/keys/age-key.txt
    sops -d /encrypted-secrets/secrets.yaml > /decrypted-secrets/secrets.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: age-key
type: Opaque
data:
  age-key.txt: <base64-encoded-age-private-key>
---
apiVersion: batch/v1
kind: Job
metadata:
  name: decrypt-secrets
spec:
  template:
    spec:
      initContainers:
      - name: sops-decrypt
        image: alpine:latest
        command: ["/bin/sh"]
        args: ["/scripts/decrypt.sh"]
        volumeMounts:
        - name: scripts
          mountPath: /scripts
        - name: age-key
          mountPath: /keys
        - name: encrypted-secrets
          mountPath: /encrypted-secrets
        - name: decrypted-secrets
          mountPath: /decrypted-secrets
      containers:
      - name: app
        image: your-app:latest
        volumeMounts:
        - name: decrypted-secrets
          mountPath: /app/secrets
      volumes:
      - name: scripts
        configMap:
          name: sops-decrypt-script
          defaultMode: 0755
      - name: age-key
        secret:
          secretName: age-key
      - name: encrypted-secrets
        configMap:
          name: encrypted-secrets
      - name: decrypted-secrets
        emptyDir: {}
      restartPolicy: Never
```

### Python Integration
```python
import subprocess
import json
import yaml
import os
from pathlib import Path

class SOPSManager:
    def __init__(self, sops_binary='sops'):
        self.sops_binary = sops_binary
    
    def decrypt_file(self, file_path):
        """Decrypt SOPS file and return content"""
        try:
            result = subprocess.run(
                [self.sops_binary, '-d', file_path],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to decrypt {file_path}: {e.stderr}")
    
    def decrypt_yaml(self, file_path):
        """Decrypt YAML file and return as dict"""
        content = self.decrypt_file(file_path)
        return yaml.safe_load(content)
    
    def decrypt_json(self, file_path):
        """Decrypt JSON file and return as dict"""
        content = self.decrypt_file(file_path)
        return json.loads(content)
    
    def decrypt_env(self, file_path):
        """Decrypt environment file and return as dict"""
        content = self.decrypt_file(file_path)
        env_vars = {}
        for line in content.strip().split('\n'):
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
        return env_vars
    
    def load_into_environment(self, file_path):
        """Load decrypted environment variables into os.environ"""
        env_vars = self.decrypt_env(file_path)
        os.environ.update(env_vars)
    
    def encrypt_file(self, file_path, content=None):
        """Encrypt file in place or with new content"""
        if content:
            # Write content to file first
            with open(file_path, 'w') as f:
                if isinstance(content, dict):
                    yaml.dump(content, f)
                else:
                    f.write(content)
        
        try:
            subprocess.run(
                [self.sops_binary, '-e', '-i', file_path],
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to encrypt {file_path}: {e}")
    
    def update_secret(self, file_path, key_path, new_value):
        """Update a specific secret value"""
        try:
            subprocess.run(
                [self.sops_binary, '--set', f'["{key_path}"] "{new_value}"', file_path],
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to update secret: {e}")

# Usage example
sops = SOPSManager()

# Load configuration
config = sops.decrypt_yaml('config/secrets.yaml')
database_password = config['database']['password']

# Load environment variables
sops.load_into_environment('.env.encrypted')
api_key = os.getenv('API_KEY')

# Application configuration class
class Config:
    def __init__(self):
        self.sops = SOPSManager()
        self._secrets = None
    
    @property
    def secrets(self):
        if self._secrets is None:
            self._secrets = self.sops.decrypt_yaml('secrets.yaml')
        return self._secrets
    
    @property
    def database_url(self):
        db = self.secrets['database']
        return f"postgresql://{db['username']}:{db['password']}@{db['host']}:{db['port']}/{db['name']}"
    
    @property
    def api_keys(self):
        return self.secrets['api_keys']
    
    def refresh_secrets(self):
        """Refresh secrets cache"""
        self._secrets = None

# Usage
config = Config()
print(f"Database URL: {config.database_url}")
print(f"Stripe API Key: {config.api_keys['stripe']}")
```

### Node.js Integration
```javascript
const { execSync } = require('child_process');
const fs = require('fs');
const yaml = require('js-yaml');

class SOPSManager {
    constructor(sopsBinary = 'sops') {
        this.sopsBinary = sopsBinary;
    }

    decryptFile(filePath) {
        try {
            const result = execSync(`${this.sopsBinary} -d "${filePath}"`, { encoding: 'utf8' });
            return result;
        } catch (error) {
            throw new Error(`Failed to decrypt ${filePath}: ${error.message}`);
        }
    }

    decryptYaml(filePath) {
        const content = this.decryptFile(filePath);
        return yaml.load(content);
    }

    decryptJson(filePath) {
        const content = this.decryptFile(filePath);
        return JSON.parse(content);
    }

    decryptEnv(filePath) {
        const content = this.decryptFile(filePath);
        const envVars = {};
        
        content.split('\n').forEach(line => {
            const trimmed = line.trim();
            if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
                const [key, ...valueParts] = trimmed.split('=');
                envVars[key.trim()] = valueParts.join('=').trim();
            }
        });
        
        return envVars;
    }

    loadIntoEnvironment(filePath) {
        const envVars = this.decryptEnv(filePath);
        Object.assign(process.env, envVars);
    }

    encryptFile(filePath, content = null) {
        if (content) {
            if (typeof content === 'object') {
                fs.writeFileSync(filePath, yaml.dump(content));
            } else {
                fs.writeFileSync(filePath, content);
            }
        }

        try {
            execSync(`${this.sopsBinary} -e -i "${filePath}"`);
        } catch (error) {
            throw new Error(`Failed to encrypt ${filePath}: ${error.message}`);
        }
    }

    updateSecret(filePath, keyPath, newValue) {
        try {
            execSync(`${this.sopsBinary} --set '["${keyPath}"] "${newValue}"' "${filePath}"`);
        } catch (error) {
            throw new Error(`Failed to update secret: ${error.message}`);
        }
    }
}

// Configuration manager
class Config {
    constructor() {
        this.sops = new SOPSManager();
        this._secrets = null;
    }

    get secrets() {
        if (!this._secrets) {
            this._secrets = this.sops.decryptYaml('secrets.yaml');
        }
        return this._secrets;
    }

    get databaseUrl() {
        const db = this.secrets.database;
        return `postgresql://${db.username}:${db.password}@${db.host}:${db.port}/${db.name}`;
    }

    get apiKeys() {
        return this.secrets.api_keys;
    }

    refreshSecrets() {
        this._secrets = null;
    }
}

// Express middleware for SOPS integration
function sopsMiddleware(secretsFile) {
    const sops = new SOPSManager();
    
    return (req, res, next) => {
        try {
            const secrets = sops.decryptYaml(secretsFile);
            req.secrets = secrets;
            next();
        } catch (error) {
            console.error('Failed to load secrets:', error);
            res.status(500).json({ error: 'Configuration error' });
        }
    };
}

// Usage
const config = new Config();

// Load environment variables
config.sops.loadIntoEnvironment('.env.encrypted');

console.log('Database URL:', config.databaseUrl);
console.log('API Keys:', config.apiKeys);

module.exports = { SOPSManager, Config, sopsMiddleware };
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy with SOPS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install SOPS
      run: |
        curl -LO https://github.com/mozilla/sops/releases/latest/download/sops-v3.8.1.linux.amd64
        chmod +x sops-v3.8.1.linux.amd64
        sudo mv sops-v3.8.1.linux.amd64 /usr/local/bin/sops
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Decrypt secrets
      run: |
        sops -d secrets/prod.yaml > decrypted-secrets.yaml
    
    - name: Deploy application
      run: |
        # Use decrypted secrets for deployment
        export $(cat decrypted-secrets.yaml | grep -v '^#' | xargs)
        ./deploy.sh
    
    - name: Cleanup
      if: always()
      run: |
        rm -f decrypted-secrets.yaml
```

### GitLab CI
```yaml
# .gitlab-ci.yml
stages:
  - deploy

variables:
  SOPS_VERSION: "3.8.1"

.sops_install: &sops_install
  - curl -LO "https://github.com/mozilla/sops/releases/download/v${SOPS_VERSION}/sops-v${SOPS_VERSION}.linux.amd64"
  - chmod +x "sops-v${SOPS_VERSION}.linux.amd64"
  - mv "sops-v${SOPS_VERSION}.linux.amd64" /usr/local/bin/sops

deploy_production:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
    - *sops_install
  script:
    - export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
    - export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
    - sops -d secrets/prod.yaml > /tmp/secrets.yaml
    - export $(cat /tmp/secrets.yaml | grep -v '^#' | xargs)
    - ./deploy.sh
  after_script:
    - rm -f /tmp/secrets.yaml
  only:
    - main
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
    }
    
    stages {
        stage('Install SOPS') {
            steps {
                script {
                    sh '''
                        curl -LO https://github.com/mozilla/sops/releases/latest/download/sops-v3.8.1.linux.amd64
                        chmod +x sops-v3.8.1.linux.amd64
                        sudo mv sops-v3.8.1.linux.amd64 /usr/local/bin/sops
                    '''
                }
            }
        }
        
        stage('Decrypt Secrets') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding', 
                     credentialsId: 'aws-credentials']
                ]) {
                    script {
                        sh '''
                            sops -d secrets/prod.yaml > decrypted-secrets.yaml
                            set -a
                            source decrypted-secrets.yaml
                            set +a
                        '''
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    sh './deploy.sh'
                }
            }
        }
    }
    
    post {
        always {
            script {
                sh 'rm -f decrypted-secrets.yaml'
            }
        }
    }
}
```

## Best Practices

### Security Best Practices
```bash
# 1. Use least privilege IAM policies
# 2. Rotate encryption keys regularly
# 3. Use different keys for different environments
# 4. Never commit decrypted files
# 5. Use .gitignore to prevent accidental commits

# .gitignore
*.decrypted.*
decrypted-*
secrets.yaml.dec
config.json.dec

# 6. Audit access to encryption keys
# 7. Use resource-based policies for fine-grained access
# 8. Monitor SOPS operations in CI/CD
```

### File Organization
```
project/
├── secrets/
│   ├── .sops.yaml
│   ├── prod/
│   │   ├── database.yaml
│   │   ├── api-keys.yaml
│   │   └── certificates.yaml
│   ├── staging/
│   │   ├── database.yaml
│   │   └── api-keys.yaml
│   └── dev/
│       ├── database.yaml
│       └── api-keys.yaml
├── scripts/
│   ├── decrypt-secrets.sh
│   ├── rotate-keys.sh
│   └── backup-secrets.sh
└── .gitignore
```

### Automation Scripts
```bash
#!/bin/bash
# scripts/rotate-keys.sh

set -e

OLD_KEY="arn:aws:kms:us-east-1:123456789012:key/old-key-id"
NEW_KEY="arn:aws:kms:us-east-1:123456789012:key/new-key-id"

echo "Rotating SOPS keys from $OLD_KEY to $NEW_KEY"

find secrets/ -name "*.yaml" -type f | while read -r file; do
    echo "Processing $file"
    
    # Check if file is encrypted with old key
    if sops metadata "$file" | grep -q "$OLD_KEY"; then
        echo "  Rotating key for $file"
        sops -r --rm-kms "$OLD_KEY" --add-kms "$NEW_KEY" "$file"
    else
        echo "  Skipping $file (not encrypted with old key)"
    fi
done

echo "Key rotation completed"
```

## Resources

- [SOPS GitHub Repository](https://github.com/mozilla/sops)
- [SOPS Documentation](https://github.com/mozilla/sops/blob/main/README.rst)
- [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)
- [GCP Cloud KMS Documentation](https://cloud.google.com/kms/docs)
- [Azure Key Vault Documentation](https://docs.microsoft.com/en-us/azure/key-vault/)
- [Age Encryption Tool](https://github.com/FiloSottile/age)
- [PGP/GPG Documentation](https://gnupg.org/documentation/)
- [SOPS Best Practices Blog](https://blog.mozilla.org/security/2015/11/17/managing-secrets-with-sops/)
- [Kubernetes Secrets Management](https://kubernetes.io/docs/concepts/configuration/secret/)
- [SOPS Terraform Provider](https://registry.terraform.io/providers/carlpett/sops/latest/docs)