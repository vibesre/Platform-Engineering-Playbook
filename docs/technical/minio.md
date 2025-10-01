---
title: "MinIO - High-Performance Object Storage"
description: "Master MinIO for S3-compatible storage: deploy distributed object storage, learn data protection, multi-tenancy, and cloud-native backup strategies."
keywords:
  - MinIO
  - object storage
  - S3 compatible
  - distributed storage
  - MinIO tutorial
  - cloud storage
  - MinIO cluster
  - data storage
  - backup storage
  - Kubernetes storage
  - self-hosted storage
  - S3 alternative
---

# MinIO

<GitHubButtons />
## 📚 Learning Resources

### 📖 Essential Documentation
- [MinIO Documentation](https://min.io/docs/) - Comprehensive official documentation with tutorials and examples
- [MinIO API Reference](https://docs.min.io/minio/baremetal/reference/minio-server/minio-server.html) - Complete API documentation
- [MinIO Best Practices](https://min.io/docs/minio/linux/operations/performance-tuning.html) - Performance optimization and production guidelines
- [MinIO Client Guide](https://min.io/docs/minio/linux/reference/minio-mc.html) - Command-line client documentation

### 📝 Specialized Guides
- [MinIO Multi-Site Replication](https://min.io/docs/minio/linux/administration/site-replication.html) - Cross-site data replication
- [MinIO Kubernetes Operator](https://github.com/minio/operator) - 18k⭐ Kubernetes deployment and management
- [MinIO Security Guide](https://min.io/docs/minio/linux/administration/identity-access-management.html) - IAM, encryption, and security best practices
- [MinIO High Availability](https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-multi-node-multi-drive.html) - Multi-node cluster deployment

### 🎥 Video Tutorials
- [MinIO Crash Course](https://www.youtube.com/watch?v=OJ_9GM2MZhQ) - Introduction to MinIO fundamentals (45 min)
- [MinIO Kubernetes Integration](https://www.youtube.com/watch?v=aXIXjGOCjmg) - Deploying MinIO on Kubernetes (30 min)
- [MinIO Performance Optimization](https://www.youtube.com/watch?v=4GNhpZAEYsY) - Tuning for production workloads (25 min)

### 🎓 Professional Courses
- [MinIO University](https://university.min.io/) - Free official training courses
- [Object Storage with MinIO](https://www.udemy.com/course/object-storage-with-minio/) - Paid comprehensive course
- [Cloud Native Storage](https://training.linuxfoundation.org/training/kubernetes-fundamentals/) - Linux Foundation (includes MinIO)

### 📚 Books
- "Learning Object Storage with MinIO" by Abhinav Shrivastava - [Purchase on Amazon](https://www.amazon.com/dp/1484268962)
- "Modern Data Engineering with MinIO" - [Free PDF](https://min.io/resources/docs/Modern-Data-Engineering-with-MinIO-eBook.pdf) | [Purchase](https://www.amazon.com/dp/B08XYQZ7TN)
- "Cloud Native Data Management" by Janakiram MSV - [Purchase on Amazon](https://www.amazon.com/dp/1492048275)

### 🛠️ Interactive Tools
- [MinIO Playground](https://play.min.io/) - Online demo environment with sample data
- [MinIO Console](https://github.com/minio/console) - Web-based administration interface
- [MinIO Browser](https://min.io/docs/minio/linux/administration/minio-console.html) - Built-in web interface for bucket management

### 🚀 Ecosystem Tools
- [mc (MinIO Client)](https://github.com/minio/mc) - 2.8k⭐ Command-line client for MinIO
- [MinIO SDKs](https://min.io/docs/minio/linux/developers/minio-drivers.html) - Multiple language bindings
- [Velero](https://velero.io/) - Kubernetes backup solution with MinIO integration
- [Rook](https://rook.io/) - Cloud-native storage orchestrator with MinIO support

### 🌐 Community & Support
- [MinIO Community](https://slack.min.io/) - Official Slack community
- [MinIO GitHub](https://github.com/minio/minio) - 46k⭐ Source code and issues
- [MinIO Blog](https://blog.min.io/) - Technical insights and updates

## Understanding MinIO: High-Performance S3-Compatible Object Storage

MinIO is a high-performance, S3-compatible object storage solution that delivers scalable, secure, and cost-effective storage infrastructure for cloud-native workloads. It's designed for private and hybrid cloud environments where organizations need Amazon S3 compatibility without vendor lock-in.

### How MinIO Works
MinIO operates as a distributed object storage system built for cloud-native environments. It stores objects (files) in buckets using a flat namespace, similar to Amazon S3. The system uses erasure coding for data protection, automatically distributing data across multiple drives and nodes for resilience and performance.

MinIO's architecture is designed for high throughput and low latency. It can run as a single-node deployment for development or scale to massive multi-petabyte clusters. The storage engine uses inline erasure coding, meaning data is encoded as it's written, eliminating the overhead of separate parity calculations.

### The MinIO Ecosystem
MinIO consists of several key components working together. The MinIO server provides the core object storage functionality with S3-compatible APIs. The MinIO Client (mc) offers command-line management capabilities. MinIO Console provides a web-based administrative interface for monitoring and management.

The ecosystem includes SDKs for popular programming languages, Kubernetes operators for cloud-native deployments, and integrations with backup solutions like Velero. MinIO also provides gateway modes for legacy filesystems and notification systems for event-driven architectures.

### Why MinIO Dominates Private Cloud Storage
MinIO has become the de facto standard for private cloud object storage due to its S3 compatibility, performance, and simplicity. Unlike traditional storage solutions that require complex setup and maintenance, MinIO can be deployed in minutes and managed through simple configuration files.

The software-defined approach means it runs on commodity hardware, dramatically reducing costs compared to proprietary storage appliances. Its cloud-native design makes it perfect for Kubernetes environments, while the S3 compatibility ensures applications work without modification.

### Mental Model for Success
Think of MinIO like building your own Amazon S3 service. Instead of sending data to AWS, you're creating an S3-compatible service in your own infrastructure. It's like having a local post office that uses the same addressing system as the national postal service - all your applications think they're talking to S3, but the data stays in your control.

This approach gives you the benefits of cloud storage (scalability, APIs, tooling) while maintaining data sovereignty and reducing costs for large-scale storage needs.

### Where to Start Your Journey
1. **Deploy a single-node instance** - Start with Docker or binary installation for development
2. **Explore with MinIO Client** - Use mc commands to create buckets and upload objects
3. **Test S3 compatibility** - Try existing S3 tools and applications against MinIO
4. **Set up monitoring** - Configure Prometheus metrics and health checks
5. **Plan for production** - Design multi-node clusters with erasure coding
6. **Implement security** - Configure TLS, IAM policies, and access controls

### Key Concepts to Master
- **S3 compatibility** - Understanding which S3 features MinIO supports
- **Erasure coding** - Data protection and performance implications
- **Distributed clusters** - Multi-node deployments and data distribution
- **Performance tuning** - Optimizing throughput and latency
- **Security models** - IAM, bucket policies, and encryption
- **Monitoring and observability** - Metrics, logging, and alerting
- **Backup and replication** - Site replication and disaster recovery
- **Kubernetes integration** - Operators, CSI drivers, and cloud-native patterns

Start with understanding object storage concepts, then progress to MinIO-specific features like erasure coding and distributed deployments. Focus on operational aspects like monitoring and security for production readiness.

## Installation

### Docker Installation
```bash
# Run MinIO server with Docker
docker run -p 9000:9000 -p 9001:9001 \
  --name minio \
  -v /mnt/data:/data \
  -e "MINIO_ROOT_USER=minio" \
  -e "MINIO_ROOT_PASSWORD=minio123" \
  quay.io/minio/minio server /data --console-address ":9001"

# Run with Docker Compose
cat > docker-compose.yml << EOF
version: '3.8'
services:
  minio:
    image: quay.io/minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    environment:
      MINIO_ROOT_USER: minio
      MINIO_ROOT_PASSWORD: minio123
    command: server /data --console-address ":9001"
    
volumes:
  minio_data:
EOF

docker-compose up -d
```

### Kubernetes Installation
```yaml
# minio-deployment.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: minio
---
apiVersion: v1
kind: Secret
metadata:
  name: minio-secret
  namespace: minio
type: Opaque
data:
  rootUser: bWluaW8=      # minio (base64)
  rootPassword: bWluaW8xMjM=  # minio123 (base64)
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: minio-pvc
  namespace: minio
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: minio
  namespace: minio
spec:
  replicas: 1
  selector:
    matchLabels:
      app: minio
  template:
    metadata:
      labels:
        app: minio
    spec:
      containers:
      - name: minio
        image: quay.io/minio/minio:latest
        args:
        - server
        - /data
        - --console-address
        - ":9001"
        env:
        - name: MINIO_ROOT_USER
          valueFrom:
            secretKeyRef:
              name: minio-secret
              key: rootUser
        - name: MINIO_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: minio-secret
              key: rootPassword
        ports:
        - containerPort: 9000
          name: api
        - containerPort: 9001
          name: console
        volumeMounts:
        - name: data
          mountPath: /data
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /minio/health/live
            port: 9000
          initialDelaySeconds: 30
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /minio/health/ready
            port: 9000
          initialDelaySeconds: 5
          periodSeconds: 10
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: minio-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: minio-service
  namespace: minio
spec:
  type: LoadBalancer
  ports:
  - port: 9000
    targetPort: 9000
    protocol: TCP
    name: api
  - port: 9001
    targetPort: 9001
    protocol: TCP
    name: console
  selector:
    app: minio

# Apply the configuration
kubectl apply -f minio-deployment.yaml
```

### Binary Installation
```bash
# Linux/macOS
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo mv minio /usr/local/bin/

# Create data directory
sudo mkdir -p /opt/minio/data
sudo chown $USER:$USER /opt/minio/data

# Start MinIO server
MINIO_ROOT_USER=minio MINIO_ROOT_PASSWORD=minio123 \
  minio server /opt/minio/data --console-address ":9001"

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://dl.min.io/server/minio/release/windows-amd64/minio.exe" -OutFile "minio.exe"
.\minio.exe server C:\minio-data --console-address ":9001"
```

## Basic Configuration

### Server Configuration
```bash
# Environment variables configuration
export MINIO_ROOT_USER=admin
export MINIO_ROOT_PASSWORD=secure_password_123
export MINIO_REGION=us-east-1
export MINIO_BROWSER=on
export MINIO_DOMAIN=minio.example.com

# Advanced configuration
export MINIO_CACHE_DRIVES="/tmp/cache1,/tmp/cache2"
export MINIO_CACHE_EXCLUDE="*.tmp"
export MINIO_COMPRESS_ENABLE=true
export MINIO_COMPRESS_EXTENSIONS=".pdf,.doc,.docx"
export MINIO_ENCRYPT_ENABLE=true

# Start server with configuration
minio server /data1 /data2 /data3 /data4 --console-address ":9001"
```

### Configuration File
```json
{
  "version": "33",
  "credential": {
    "accessKey": "minio",
    "secretKey": "minio123"
  },
  "region": "us-east-1",
  "browser": "on",
  "domain": "",
  "storageclass": {
    "standard": "",
    "rrs": "EC:2"
  },
  "cache": {
    "drives": [],
    "expiry": 90,
    "quota": 80,
    "exclude": [],
    "after": 0,
    "watermark": {
      "low": 70,
      "high": 80
    }
  },
  "kms": {
    "vault": {
      "endpoint": "",
      "auth": {
        "type": "",
        "approle": {
          "id": "",
          "secret": ""
        }
      },
      "key-id": "",
      "namespace": ""
    }
  },
  "notify": {
    "amqp": {},
    "nats": {},
    "elasticsearch": {},
    "redis": {},
    "postgresql": {},
    "kafka": {},
    "webhook": {},
    "mysql": {}
  }
}
```

## Client Usage

### MinIO Client (mc)
```bash
# Install MinIO Client
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/

# Configure client
mc alias set myminio http://localhost:9000 minio minio123

# Basic operations
# Create bucket
mc mb myminio/mybucket

# List buckets
mc ls myminio

# Upload file
mc cp local-file.txt myminio/mybucket/

# Download file
mc cp myminio/mybucket/file.txt ./downloaded-file.txt

# Sync directory
mc mirror ./local-dir myminio/mybucket/backup/

# Set bucket policy
mc policy set public myminio/mybucket

# Generate pre-signed URL
mc share download myminio/mybucket/file.txt --expire=7d
```

### Python SDK
```python
# requirements.txt
minio>=7.1.0
python-dotenv>=0.19.0

# minio_client.py
from minio import Minio
from minio.error import S3Error
import os
from datetime import datetime, timedelta

class MinIOClient:
    def __init__(self, endpoint, access_key, secret_key, secure=True):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
    
    def create_bucket(self, bucket_name, region="us-east-1"):
        """Create a bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name, location=region)
                print(f"Bucket '{bucket_name}' created successfully")
            else:
                print(f"Bucket '{bucket_name}' already exists")
        except S3Error as e:
            print(f"Error creating bucket: {e}")
    
    def upload_file(self, bucket_name, object_name, file_path, content_type=None):
        """Upload a file to MinIO"""
        try:
            result = self.client.fput_object(
                bucket_name, 
                object_name, 
                file_path,
                content_type=content_type
            )
            print(f"File uploaded successfully: {result.object_name}")
            return result
        except S3Error as e:
            print(f"Error uploading file: {e}")
            return None
    
    def download_file(self, bucket_name, object_name, file_path):
        """Download a file from MinIO"""
        try:
            self.client.fget_object(bucket_name, object_name, file_path)
            print(f"File downloaded successfully: {file_path}")
        except S3Error as e:
            print(f"Error downloading file: {e}")
    
    def list_objects(self, bucket_name, prefix=None, recursive=True):
        """List objects in a bucket"""
        try:
            objects = self.client.list_objects(
                bucket_name, 
                prefix=prefix, 
                recursive=recursive
            )
            return list(objects)
        except S3Error as e:
            print(f"Error listing objects: {e}")
            return []
    
    def delete_object(self, bucket_name, object_name):
        """Delete an object"""
        try:
            self.client.remove_object(bucket_name, object_name)
            print(f"Object '{object_name}' deleted successfully")
        except S3Error as e:
            print(f"Error deleting object: {e}")
    
    def generate_presigned_url(self, bucket_name, object_name, expires=timedelta(hours=1)):
        """Generate a presigned URL for object access"""
        try:
            url = self.client.presigned_get_object(
                bucket_name, 
                object_name, 
                expires=expires
            )
            return url
        except S3Error as e:
            print(f"Error generating presigned URL: {e}")
            return None
    
    def set_bucket_policy(self, bucket_name, policy):
        """Set bucket policy"""
        try:
            self.client.set_bucket_policy(bucket_name, policy)
            print(f"Policy set for bucket '{bucket_name}'")
        except S3Error as e:
            print(f"Error setting bucket policy: {e}")

# Usage example
if __name__ == "__main__":
    # Initialize client
    minio_client = MinIOClient(
        endpoint="localhost:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False  # Set to True for HTTPS
    )
    
    # Create bucket
    bucket_name = "test-bucket"
    minio_client.create_bucket(bucket_name)
    
    # Upload file
    minio_client.upload_file(
        bucket_name, 
        "documents/sample.txt", 
        "./sample.txt",
        content_type="text/plain"
    )
    
    # List objects
    objects = minio_client.list_objects(bucket_name)
    for obj in objects:
        print(f"Object: {obj.object_name}, Size: {obj.size}, Modified: {obj.last_modified}")
    
    # Generate presigned URL
    url = minio_client.generate_presigned_url(bucket_name, "documents/sample.txt")
    if url:
        print(f"Presigned URL: {url}")
```

### JavaScript/Node.js SDK
```javascript
// package.json
{
  "dependencies": {
    "minio": "^7.1.0",
    "dotenv": "^16.0.0"
  }
}

// minio-client.js
const Minio = require('minio');
require('dotenv').config();

class MinIOClient {
    constructor(endpoint, port, useSSL, accessKey, secretKey) {
        this.minioClient = new Minio.Client({
            endPoint: endpoint,
            port: port,
            useSSL: useSSL,
            accessKey: accessKey,
            secretKey: secretKey
        });
    }
    
    async createBucket(bucketName, region = 'us-east-1') {
        try {
            const exists = await this.minioClient.bucketExists(bucketName);
            if (!exists) {
                await this.minioClient.makeBucket(bucketName, region);
                console.log(`Bucket '${bucketName}' created successfully`);
            } else {
                console.log(`Bucket '${bucketName}' already exists`);
            }
        } catch (error) {
            console.error('Error creating bucket:', error);
        }
    }
    
    async uploadFile(bucketName, objectName, filePath, metaData = {}) {
        try {
            const result = await this.minioClient.fPutObject(
                bucketName, 
                objectName, 
                filePath, 
                metaData
            );
            console.log(`File uploaded successfully: ${objectName}`);
            return result;
        } catch (error) {
            console.error('Error uploading file:', error);
            throw error;
        }
    }
    
    async uploadStream(bucketName, objectName, stream, size, metaData = {}) {
        try {
            const result = await this.minioClient.putObject(
                bucketName, 
                objectName, 
                stream, 
                size, 
                metaData
            );
            console.log(`Stream uploaded successfully: ${objectName}`);
            return result;
        } catch (error) {
            console.error('Error uploading stream:', error);
            throw error;
        }
    }
    
    async downloadFile(bucketName, objectName, filePath) {
        try {
            await this.minioClient.fGetObject(bucketName, objectName, filePath);
            console.log(`File downloaded successfully: ${filePath}`);
        } catch (error) {
            console.error('Error downloading file:', error);
            throw error;
        }
    }
    
    async listObjects(bucketName, prefix = '', recursive = true) {
        try {
            const objects = [];
            const stream = this.minioClient.listObjects(bucketName, prefix, recursive);
            
            return new Promise((resolve, reject) => {
                stream.on('data', (obj) => objects.push(obj));
                stream.on('end', () => resolve(objects));
                stream.on('error', reject);
            });
        } catch (error) {
            console.error('Error listing objects:', error);
            throw error;
        }
    }
    
    async deleteObject(bucketName, objectName) {
        try {
            await this.minioClient.removeObject(bucketName, objectName);
            console.log(`Object '${objectName}' deleted successfully`);
        } catch (error) {
            console.error('Error deleting object:', error);
            throw error;
        }
    }
    
    async generatePresignedUrl(bucketName, objectName, expiry = 24 * 60 * 60) {
        try {
            const url = await this.minioClient.presignedGetObject(
                bucketName, 
                objectName, 
                expiry
            );
            return url;
        } catch (error) {
            console.error('Error generating presigned URL:', error);
            throw error;
        }
    }
    
    async setBucketNotification(bucketName, config) {
        try {
            await this.minioClient.setBucketNotification(bucketName, config);
            console.log(`Notification set for bucket '${bucketName}'`);
        } catch (error) {
            console.error('Error setting bucket notification:', error);
            throw error;
        }
    }
}

// Usage example
async function main() {
    const client = new MinIOClient(
        'localhost',
        9000,
        false, // useSSL
        'minio',
        'minio123'
    );
    
    try {
        // Create bucket
        await client.createBucket('my-app-bucket');
        
        // Upload file
        await client.uploadFile(
            'my-app-bucket',
            'uploads/document.pdf',
            './local-document.pdf',
            { 'Content-Type': 'application/pdf' }
        );
        
        // List objects
        const objects = await client.listObjects('my-app-bucket');
        console.log('Objects in bucket:', objects);
        
        // Generate presigned URL (valid for 1 hour)
        const url = await client.generatePresignedUrl(
            'my-app-bucket',
            'uploads/document.pdf',
            3600
        );
        console.log('Presigned URL:', url);
        
    } catch (error) {
        console.error('Application error:', error);
    }
}

main();
```

## Advanced Features

### Distributed Deployment
```bash
# Multi-node MinIO cluster setup
# Node 1
MINIO_ROOT_USER=minio MINIO_ROOT_PASSWORD=minio123 \
  minio server http://node{1...4}/data{1...2} \
  --console-address ":9001"

# Node 2
MINIO_ROOT_USER=minio MINIO_ROOT_PASSWORD=minio123 \
  minio server http://node{1...4}/data{1...2} \
  --console-address ":9001"

# Node 3
MINIO_ROOT_USER=minio MINIO_ROOT_PASSWORD=minio123 \
  minio server http://node{1...4}/data{1...2} \
  --console-address ":9001"

# Node 4
MINIO_ROOT_USER=minio MINIO_ROOT_PASSWORD=minio123 \
  minio server http://node{1...4}/data{1...2} \
  --console-address ":9001"
```

### Load Balancer Configuration
```nginx
# nginx.conf
upstream minio_servers {
    server node1:9000;
    server node2:9000;
    server node3:9000;
    server node4:9000;
}

upstream minio_console {
    server node1:9001;
    server node2:9001;
    server node3:9001;
    server node4:9001;
}

server {
    listen 80;
    server_name minio.example.com;
    
    # API endpoints
    location / {
        proxy_pass http://minio_servers;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        client_max_body_size 1000m;
        proxy_connect_timeout 300;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        chunked_transfer_encoding off;
    }
}

server {
    listen 80;
    server_name console.minio.example.com;
    
    # Console endpoints
    location / {
        proxy_pass http://minio_console;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-NginX-Proxy true;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Monitoring and Metrics
```yaml
# prometheus-config.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'minio'
    metrics_path: /minio/v2/metrics/cluster
    scheme: http
    static_configs:
      - targets: ['localhost:9000']
    scrape_interval: 5s

# Docker Compose with monitoring
version: '3.8'
services:
  minio:
    image: quay.io/minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    environment:
      MINIO_ROOT_USER: minio
      MINIO_ROOT_PASSWORD: minio123
      MINIO_PROMETHEUS_AUTH_TYPE: public
    command: server /data --console-address ":9001"
    
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  minio_data:
  prometheus_data:
  grafana_data:
```

## Security Configuration

### TLS/SSL Setup
```bash
# Generate self-signed certificates
mkdir -p ~/.minio/certs
openssl req -new -x509 -days 365 -nodes \
  -out ~/.minio/certs/public.crt \
  -keyout ~/.minio/certs/private.key \
  -subj "/C=US/ST=CA/L=San Francisco/O=Example/CN=minio.example.com"

# Start MinIO with TLS
MINIO_ROOT_USER=minio MINIO_ROOT_PASSWORD=minio123 \
  minio server /data --console-address ":9001"
```

### IAM Policies
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "StringEquals": {
          "s3:prefix": ["documents/", "images/"]
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket"
      ]
    }
  ]
}
```

### Bucket Policies
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-public-bucket/*"
    },
    {
      "Sid": "AllowUploadForAuthenticatedUsers",
      "Effect": "Allow",
      "Principal": {
        "AWS": ["arn:aws:iam::123456789012:user/uploader"]
      },
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl"
      ],
      "Resource": "arn:aws:s3:::my-upload-bucket/*"
    }
  ]
}
```

## Event Notifications

### Webhook Configuration
```python
# webhook_server.py
from flask import Flask, request, jsonify
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/minio/webhook', methods=['POST'])
def handle_minio_event():
    try:
        event_data = request.get_json()
        
        for record in event_data.get('Records', []):
            event_name = record.get('eventName')
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            object_size = record['s3']['object']['size']
            
            logging.info(f"Event: {event_name}")
            logging.info(f"Bucket: {bucket_name}")
            logging.info(f"Object: {object_key}")
            logging.info(f"Size: {object_size} bytes")
            
            # Process based on event type
            if event_name.startswith('s3:ObjectCreated'):
                handle_object_created(bucket_name, object_key, object_size)
            elif event_name.startswith('s3:ObjectRemoved'):
                handle_object_removed(bucket_name, object_key)
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def handle_object_created(bucket, key, size):
    # Process new object creation
    if key.endswith('.jpg') or key.endswith('.png'):
        # Trigger image processing
        print(f"Processing image: {key}")
    elif key.endswith('.pdf'):
        # Trigger document indexing
        print(f"Indexing document: {key}")

def handle_object_removed(bucket, key):
    # Process object removal
    print(f"Object removed: {key}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Configure Webhook with mc
```bash
# Configure webhook notification
mc admin config set myminio notify_webhook:webhook1 \
  endpoint="http://localhost:5000/minio/webhook" \
  auth_token=""

# Restart MinIO service
mc admin service restart myminio

# Set bucket notification
mc event add myminio/my-bucket arn:minio:sqs::webhook1:webhook \
  --event put,delete \
  --prefix documents/ \
  --suffix .pdf
```

## Performance Optimization

### Caching Configuration
```bash
# Enable disk caching
export MINIO_CACHE_DRIVES="/cache1,/cache2"
export MINIO_CACHE_QUOTA=80
export MINIO_CACHE_AFTER=3
export MINIO_CACHE_WATERMARK_LOW=70
export MINIO_CACHE_WATERMARK_HIGH=90

# Exclude certain file types from cache
export MINIO_CACHE_EXCLUDE="*.tmp,*.log"

# Enable compression
export MINIO_COMPRESS_ENABLE=true
export MINIO_COMPRESS_EXTENSIONS=".txt,.log,.csv,.json,.xml"
export MINIO_COMPRESS_MIME_TYPES="text/*,application/json,application/xml"
```

### Erasure Coding
```bash
# Deploy with erasure coding (4 drives minimum)
minio server /disk1 /disk2 /disk3 /disk4

# Multi-node erasure coding (16 drives across 4 nodes)
minio server http://node{1...4}/disk{1...4}
```

## Backup and Disaster Recovery

### Site Replication
```bash
# Configure site replication between two MinIO deployments
mc admin replicate add myminio1 myminio2

# Check replication status
mc admin replicate info myminio1

# Remove site replication
mc admin replicate rm myminio1 myminio2
```

### Bucket Replication
```bash
# Enable versioning (required for replication)
mc version enable myminio/source-bucket
mc version enable myminio/target-bucket

# Configure replication
mc replicate add myminio/source-bucket \
  --remote-bucket http://minio:minio123@target-minio:9000/target-bucket \
  --replicate "delete,delete-marker,replica-metadata-sync"

# Check replication status
mc replicate status myminio/source-bucket
```

## Troubleshooting

### Health Checks
```bash
# Check cluster health
mc admin info myminio

# Check disk usage
mc admin info myminio --json | jq '.info.backend.standardSCData'

# Monitor real-time events
mc admin trace myminio

# Check configuration
mc admin config get myminio

# View server logs
mc admin logs myminio

# Perform system health check
mc admin heal myminio --recursive --verbose
```

### Performance Testing
```python
# performance_test.py
import concurrent.futures
import time
import boto3
from botocore.config import Config

def upload_test_file(s3_client, bucket, key, data_size):
    try:
        start_time = time.time()
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=b'0' * data_size
        )
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        return None

def performance_test():
    # Configure S3 client for MinIO
    s3_client = boto3.client(
        's3',
        endpoint_url='http://localhost:9000',
        aws_access_key_id='minio',
        aws_secret_access_key='minio123',
        config=Config(
            region_name='us-east-1',
            retries={'max_attempts': 3},
            max_pool_connections=50
        )
    )
    
    bucket_name = 'performance-test'
    
    # Create bucket
    try:
        s3_client.create_bucket(Bucket=bucket_name)
    except:
        pass  # Bucket already exists
    
    # Test parameters
    num_files = 100
    file_size = 1024 * 1024  # 1MB
    max_workers = 10
    
    # Parallel upload test
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(upload_test_file, s3_client, bucket_name, f'test-{i}.bin', file_size)
            for i in range(num_files)
        ]
        
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    end_time = time.time()
    total_time = end_time - start_time
    successful_uploads = len([r for r in results if r is not None])
    
    print(f"Performance Test Results:")
    print(f"Total files: {num_files}")
    print(f"Successful uploads: {successful_uploads}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Throughput: {successful_uploads / total_time:.2f} files/second")
    print(f"Data rate: {(successful_uploads * file_size) / (1024 * 1024 * total_time):.2f} MB/second")

if __name__ == "__main__":
    performance_test()
```

---

### 📡 Stay Updated

**Release Notes**: [MinIO Releases](https://github.com/minio/minio/releases) • [MinIO Client](https://github.com/minio/mc/releases) • [Operator](https://github.com/minio/operator/releases)

**Project News**: [MinIO Blog](https://blog.min.io/) • [MinIO University](https://university.min.io/) • [Release Videos](https://www.youtube.com/c/MinioInc)

**Community**: [Slack Community](https://slack.min.io/) • [GitHub Discussions](https://github.com/minio/minio/discussions) • [MinIO Newsletter](https://min.io/newsletter)