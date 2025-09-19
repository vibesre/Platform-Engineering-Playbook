# DigitalOcean

## Overview

DigitalOcean is a cloud infrastructure provider focused on simplicity and developer experience. Known for its straightforward pricing, intuitive interface, and excellent documentation, DigitalOcean makes it easy for developers and small to medium-sized businesses to deploy and scale applications in the cloud. With its "droplet" virtual machines and managed services, DigitalOcean offers a more approachable alternative to complex enterprise cloud platforms.

### Why DigitalOcean?

- **Simplicity First**: Clean UI, straightforward APIs, no hidden costs
- **Developer Friendly**: Excellent documentation, tutorials, and community
- **Predictable Pricing**: Simple, transparent pricing with no surprises
- **Fast Deployment**: Provision resources in under a minute
- **Global Infrastructure**: 14 data center regions worldwide
- **Great for Startups**: Cost-effective for small to medium workloads

## Key Services

### Compute Services

#### Droplets
Virtual machines that can be deployed in seconds.

```bash
# Install doctl CLI
brew install doctl  # macOS
# or
snap install doctl  # Linux

# Authenticate
doctl auth init

# Create a Droplet
doctl compute droplet create my-droplet \
  --region nyc3 \
  --size s-2vcpu-4gb \
  --image ubuntu-22-04-x64 \
  --ssh-keys $(doctl compute ssh-key list --format ID --no-header)

# List Droplets
doctl compute droplet list

# SSH into Droplet
doctl compute ssh my-droplet

# Create with user data (cloud-init)
doctl compute droplet create web-server \
  --region sfo3 \
  --size s-1vcpu-1gb \
  --image ubuntu-22-04-x64 \
  --user-data-file ./cloud-init.yaml
```

```yaml
# cloud-init.yaml
#cloud-config
package_update: true
packages:
  - nginx
  - certbot
  - python3-certbot-nginx

write_files:
  - path: /var/www/html/index.html
    content: |
      <!DOCTYPE html>
      <html>
      <head><title>Welcome to DigitalOcean</title></head>
      <body><h1>Hello from DigitalOcean!</h1></body>
      </html>

runcmd:
  - systemctl start nginx
  - systemctl enable nginx
  - ufw allow 'Nginx Full'
  - ufw allow OpenSSH
  - ufw --force enable
```

#### App Platform
Platform as a Service for deploying apps from GitHub/GitLab.

```yaml
# app.yaml - App specification
name: sample-nodejs-app
region: nyc
services:
- name: web
  github:
    repo: your-github-username/sample-nodejs
    branch: main
    deploy_on_push: true
  build_command: npm run build
  run_command: npm start
  http_port: 3000
  instance_count: 2
  instance_size_slug: basic-xs
  routes:
  - path: /
  envs:
  - key: NODE_ENV
    value: production
  - key: DATABASE_URL
    scope: RUN_TIME
    value: ${database.DATABASE_URL}

databases:
- name: database
  engine: PG
  version: "12"
  production: false
  cluster_name: sample-nodejs-db
```

```bash
# Deploy app
doctl apps create --spec app.yaml

# Update app
doctl apps update <app-id> --spec app.yaml

# Get app details
doctl apps get <app-id>

# View logs
doctl apps logs <app-id> --type=run --follow
```

#### Kubernetes (DOKS)
Managed Kubernetes service.

```bash
# Create Kubernetes cluster
doctl kubernetes cluster create my-cluster \
  --region nyc1 \
  --version 1.28.2-do.0 \
  --node-pool "name=worker-pool;size=s-2vcpu-4gb;count=3"

# Get kubeconfig
doctl kubernetes cluster kubeconfig save my-cluster

# List clusters
doctl kubernetes cluster list

# Scale node pool
doctl kubernetes cluster node-pool update my-cluster worker-pool \
  --count 5

# Install DigitalOcean CSI driver
kubectl apply -f https://raw.githubusercontent.com/digitalocean/csi-digitalocean/master/deploy/kubernetes/releases/csi-digitalocean-v4.5.0.yaml

# Deploy sample application
kubectl create deployment nginx --image=nginx:alpine
kubectl expose deployment nginx --type=LoadBalancer --port=80
```

```yaml
# kubernetes/app-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: app
        image: registry.digitalocean.com/my-registry/my-app:v1.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
---
apiVersion: v1
kind: Service
metadata:
  name: web-service
  annotations:
    service.beta.kubernetes.io/do-loadbalancer-protocol: "http"
    service.beta.kubernetes.io/do-loadbalancer-healthcheck-path: "/health"
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 8080
```

#### Functions
Serverless compute platform.

```javascript
// packages/sample/hello/hello.js
function main(args) {
    let name = args.name || 'World';
    let place = args.place || 'DigitalOcean';
    return {
        body: `Hello ${name} from ${place}!`,
        statusCode: 200,
        headers: {
            'Content-Type': 'text/plain'
        }
    };
}

exports.main = main;
```

```yaml
# project.yml
parameters:
  message:
    type: string
    description: Default greeting message
    default: "Hello from Functions"
    
packages:
  - name: sample
    functions:
      - name: hello
        runtime: nodejs:14
        parameters:
          name:
            type: string
            default: "Developer"
      - name: process
        runtime: python:3.9
        environment:
          MESSAGE: ${message}
        limits:
          timeout: 30000
          memory: 512
```

```bash
# Deploy functions
doctl serverless deploy . --remote-build

# Invoke function
doctl serverless functions invoke sample/hello -p name:John

# Get function URL
doctl serverless functions get sample/hello --url
```

### Storage Services

#### Spaces (Object Storage)
S3-compatible object storage.

```python
import boto3
from botocore.client import Config

# Configure Spaces client
session = boto3.session.Session()
client = session.client('s3',
    region_name='nyc3',
    endpoint_url='https://nyc3.digitaloceanspaces.com',
    aws_access_key_id='DO_ACCESS_KEY',
    aws_secret_access_key='DO_SECRET_KEY'
)

# Create a Space
client.create_bucket(Bucket='my-space')

# Upload file
client.upload_file('local-file.txt', 'my-space', 'remote-file.txt')

# Generate presigned URL
url = client.generate_presigned_url(
    ClientMethod='get_object',
    Params={'Bucket': 'my-space', 'Key': 'remote-file.txt'},
    ExpiresIn=3600
)

# Set CORS configuration
cors_config = {
    'CORSRules': [{
        'AllowedHeaders': ['*'],
        'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'],
        'AllowedOrigins': ['https://example.com'],
        'ExposeHeaders': ['ETag'],
        'MaxAgeSeconds': 3000
    }]
}
client.put_bucket_cors(Bucket='my-space', CORSConfiguration=cors_config)

# Enable CDN
# This is done through the DigitalOcean API
import requests

headers = {
    'Authorization': f'Bearer {DO_TOKEN}',
    'Content-Type': 'application/json'
}

cdn_config = {
    'origin': 'my-space.nyc3.digitaloceanspaces.com',
    'ttl': 3600,
    'custom_domain': 'cdn.example.com',
    'certificate_id': 'cert-uuid'
}

response = requests.post(
    'https://api.digitalocean.com/v2/cdn/endpoints',
    json=cdn_config,
    headers=headers
)
```

#### Volumes (Block Storage)
Persistent block storage for Droplets.

```bash
# Create volume
doctl compute volume create my-volume \
  --region nyc1 \
  --size 100GiB \
  --desc "Application data volume"

# Attach to Droplet
doctl compute volume-action attach <volume-id> <droplet-id>

# Format and mount (on the Droplet)
sudo mkfs.ext4 /dev/disk/by-id/scsi-0DO_Volume_my-volume
sudo mkdir /mnt/volume
sudo mount -o defaults,nofail,discard,noatime /dev/disk/by-id/scsi-0DO_Volume_my-volume /mnt/volume

# Add to /etc/fstab for persistence
echo '/dev/disk/by-id/scsi-0DO_Volume_my-volume /mnt/volume ext4 defaults,nofail,discard,noatime 0 2' | sudo tee -a /etc/fstab

# Resize volume
doctl compute volume-action resize <volume-id> --size 200GiB
```

### Databases

#### Managed Databases
PostgreSQL, MySQL, Redis, MongoDB.

```bash
# Create PostgreSQL database
doctl databases create my-postgres \
  --engine pg \
  --version 15 \
  --region nyc1 \
  --size db-s-1vcpu-1gb \
  --num-nodes 1

# Get connection details
doctl databases connection my-postgres

# Create database and user
doctl databases user create <db-id> myuser
doctl databases db create <db-id> mydb

# Enable connection pooling
doctl databases pool create <db-id> \
  --name mypool \
  --mode transaction \
  --size 25 \
  --db mydb \
  --user myuser
```

```python
# Python connection example
import psycopg2
from psycopg2 import pool

# Create connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    host="your-db-host.db.ondigitalocean.com",
    port=25060,
    database="mydb",
    user="myuser",
    password="your-password",
    sslmode='require'
)

# Get connection from pool
conn = connection_pool.getconn()
try:
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
finally:
    connection_pool.putconn(conn)
```

#### Redis Configuration

```python
import redis

# Standard connection
r = redis.Redis(
    host='your-redis-host.db.ondigitalocean.com',
    port=25061,
    password='your-password',
    ssl=True,
    ssl_cert_reqs=None
)

# With connection pooling
pool = redis.ConnectionPool(
    host='your-redis-host.db.ondigitalocean.com',
    port=25061,
    password='your-password',
    ssl=True,
    ssl_cert_reqs=None,
    max_connections=50
)
r = redis.Redis(connection_pool=pool)

# Usage examples
r.set('key', 'value', ex=3600)  # Expire after 1 hour
value = r.get('key')

# Pub/Sub
pubsub = r.pubsub()
pubsub.subscribe('channel')

# In another process
r.publish('channel', 'Hello subscribers!')
```

### Networking

#### Load Balancers
Distribute traffic across multiple Droplets.

```bash
# Create load balancer
doctl compute load-balancer create \
  --name my-lb \
  --region nyc3 \
  --forwarding-rules entry_protocol:http,entry_port:80,target_protocol:http,target_port:8080 \
  --health-check protocol:http,port:8080,path:/health,check_interval_seconds:10 \
  --droplet-ids 123456,789012

# Update forwarding rules
doctl compute load-balancer update <lb-id> \
  --forwarding-rules entry_protocol:https,entry_port:443,target_protocol:http,target_port:8080,certificate_id:cert-uuid
```

#### VPC (Virtual Private Cloud)
Private networking for resources.

```bash
# Create VPC
doctl vpcs create \
  --name my-vpc \
  --region nyc3 \
  --ip-range 10.10.0.0/16 \
  --description "Production VPC"

# Create Droplet in VPC
doctl compute droplet create my-droplet \
  --region nyc3 \
  --size s-1vcpu-1gb \
  --image ubuntu-22-04-x64 \
  --vpc-uuid <vpc-uuid>

# List resources in VPC
doctl vpcs list-resources <vpc-uuid>
```

#### Firewalls
Cloud-based firewall rules.

```bash
# Create firewall
doctl compute firewall create \
  --name web-firewall \
  --inbound-rules "protocol:tcp,ports:22,sources:addresses:0.0.0.0/0" \
  --inbound-rules "protocol:tcp,ports:80,sources:addresses:0.0.0.0/0" \
  --inbound-rules "protocol:tcp,ports:443,sources:addresses:0.0.0.0/0" \
  --outbound-rules "protocol:tcp,ports:all,destinations:addresses:0.0.0.0/0" \
  --outbound-rules "protocol:udp,ports:all,destinations:addresses:0.0.0.0/0" \
  --droplet-ids 123456,789012
```

## Infrastructure as Code

### Terraform Example

```hcl
# main.tf
terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
}

provider "digitalocean" {
  token = var.do_token
}

# VPC
resource "digitalocean_vpc" "main" {
  name     = "production-vpc"
  region   = "nyc3"
  ip_range = "10.10.0.0/16"
}

# SSH Key
resource "digitalocean_ssh_key" "default" {
  name       = "terraform-key"
  public_key = file("~/.ssh/id_rsa.pub")
}

# Droplets
resource "digitalocean_droplet" "web" {
  count              = 3
  image              = "ubuntu-22-04-x64"
  name               = "web-${count.index + 1}"
  region             = "nyc3"
  size               = "s-2vcpu-4gb"
  vpc_uuid           = digitalocean_vpc.main.id
  ssh_keys           = [digitalocean_ssh_key.default.fingerprint]
  
  user_data = <<-EOT
    #!/bin/bash
    apt-get update
    apt-get install -y nginx
    
    cat > /var/www/html/index.html <<EOF
    <h1>Server ${count.index + 1}</h1>
    EOF
    
    systemctl restart nginx
  EOT

  lifecycle {
    create_before_destroy = true
  }
}

# Load Balancer
resource "digitalocean_loadbalancer" "web" {
  name        = "web-lb"
  region      = "nyc3"
  vpc_uuid    = digitalocean_vpc.main.id
  
  forwarding_rule {
    entry_port     = 80
    entry_protocol = "http"
    
    target_port     = 80
    target_protocol = "http"
  }
  
  healthcheck {
    port     = 80
    protocol = "http"
    path     = "/"
  }
  
  droplet_ids = digitalocean_droplet.web[*].id
  
  lifecycle {
    create_before_destroy = true
  }
}

# Database Cluster
resource "digitalocean_database_cluster" "postgres" {
  name       = "production-postgres"
  engine     = "pg"
  version    = "15"
  size       = "db-s-1vcpu-2gb"
  region     = "nyc3"
  node_count = 1
  
  private_network_uuid = digitalocean_vpc.main.id
}

# Database Firewall
resource "digitalocean_database_firewall" "postgres" {
  cluster_id = digitalocean_database_cluster.postgres.id
  
  rule {
    type  = "droplet"
    value = digitalocean_droplet.web[0].id
  }
  
  rule {
    type  = "droplet"
    value = digitalocean_droplet.web[1].id
  }
  
  rule {
    type  = "droplet"
    value = digitalocean_droplet.web[2].id
  }
}

# Firewall
resource "digitalocean_firewall" "web" {
  name = "web-firewall"
  
  droplet_ids = digitalocean_droplet.web[*].id
  
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0"]
  }
  
  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0"]
  }
  
  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0"]
  }
  
  inbound_rule {
    protocol                  = "tcp"
    port_range               = "all"
    source_load_balancer_uids = [digitalocean_loadbalancer.web.id]
  }
  
  outbound_rule {
    protocol              = "tcp"
    port_range            = "all"
    destination_addresses = ["0.0.0.0/0"]
  }
  
  outbound_rule {
    protocol              = "udp"
    port_range            = "all"
    destination_addresses = ["0.0.0.0/0"]
  }
}

# Project
resource "digitalocean_project" "production" {
  name        = "Production"
  description = "Production environment resources"
  purpose     = "Web Application"
  environment = "Production"
  
  resources = concat(
    [for d in digitalocean_droplet.web : d.urn],
    [
      digitalocean_loadbalancer.web.urn,
      digitalocean_database_cluster.postgres.urn
    ]
  )
}

# Outputs
output "load_balancer_ip" {
  value       = digitalocean_loadbalancer.web.ip
  description = "The public IP of the load balancer"
}

output "database_uri" {
  value       = digitalocean_database_cluster.postgres.uri
  sensitive   = true
  description = "The connection string for the database"
}
```

### Ansible Example

```yaml
# playbook.yml
---
- name: Configure DigitalOcean Droplets
  hosts: all
  become: yes
  vars:
    app_user: appuser
    app_dir: /var/www/app
    node_version: "18"
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install required packages
      apt:
        name:
          - nginx
          - nodejs
          - npm
          - git
          - python3-pip
          - certbot
          - python3-certbot-nginx
        state: present
    
    - name: Create application user
      user:
        name: "{{ app_user }}"
        shell: /bin/bash
        groups: www-data
        append: yes
    
    - name: Create application directory
      file:
        path: "{{ app_dir }}"
        state: directory
        owner: "{{ app_user }}"
        group: www-data
        mode: '0755'
    
    - name: Configure Nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/app
      notify: restart nginx
    
    - name: Enable Nginx site
      file:
        src: /etc/nginx/sites-available/app
        dest: /etc/nginx/sites-enabled/app
        state: link
    
    - name: Remove default Nginx site
      file:
        path: /etc/nginx/sites-enabled/default
        state: absent
      notify: restart nginx
    
    - name: Setup UFW firewall
      ufw:
        rule: allow
        name: "{{ item }}"
        state: enabled
      loop:
        - OpenSSH
        - 'Nginx Full'
    
    - name: Install PM2 globally
      npm:
        name: pm2
        global: yes
    
    - name: Configure PM2 startup
      command: pm2 startup systemd -u {{ app_user }} --hp /home/{{ app_user }}
      become_user: "{{ app_user }}"
  
  handlers:
    - name: restart nginx
      systemd:
        name: nginx
        state: restarted
        daemon_reload: yes
```

```jinja2
# templates/nginx.conf.j2
server {
    listen 80;
    server_name {{ ansible_default_ipv4.address }};

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias {{ app_dir }}/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

## Best Practices

### Cost Optimization

1. **Right-sizing Droplets**
   ```bash
   # Monitor CPU and memory usage
   doctl compute droplet get <droplet-id> --format ID,Memory,VCPUs,Disk
   
   # Resize Droplet
   doctl compute droplet-action resize <droplet-id> --size s-1vcpu-1gb --wait
   ```

2. **Use Reserved Droplets**
   - 1 or 3-year terms
   - Up to 20% discount
   - Good for predictable workloads

3. **Snapshot Management**
   ```bash
   # Create snapshot
   doctl compute droplet-action snapshot <droplet-id> --snapshot-name "backup-$(date +%Y%m%d)"
   
   # Delete old snapshots
   doctl compute snapshot list --format ID,Name,CreatedAt | grep "backup-" | awk '$3 < "'$(date -d '30 days ago' '+%Y-%m-%d')'" {print $1}' | xargs -I {} doctl compute snapshot delete {} --force
   ```

4. **Bandwidth Pooling**
   - All Droplets share bandwidth allocation
   - Unused bandwidth from one Droplet can be used by others
   - Monitor usage to avoid overage charges

5. **Object Storage Optimization**
   ```python
   # Set lifecycle rules for Spaces
   import boto3
   
   client = boto3.client('s3',
       endpoint_url='https://nyc3.digitaloceanspaces.com',
       aws_access_key_id='DO_ACCESS_KEY',
       aws_secret_access_key='DO_SECRET_KEY'
   )
   
   lifecycle_config = {
       'Rules': [{
           'ID': 'Delete old logs',
           'Status': 'Enabled',
           'Prefix': 'logs/',
           'Expiration': {
               'Days': 30
           }
       }]
   }
   
   client.put_bucket_lifecycle_configuration(
       Bucket='my-space',
       LifecycleConfiguration=lifecycle_config
   )
   ```

### Security Best Practices

1. **SSH Key Management**
   ```bash
   # Use SSH keys only, disable password auth
   sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
   sudo systemctl restart sshd
   
   # Rotate SSH keys
   doctl compute ssh-key create new-key --public-key-file ~/.ssh/new_key.pub
   doctl compute droplet update <droplet-id> --ssh-keys <new-key-id>
   ```

2. **Firewall Configuration**
   ```bash
   # Create strict firewall rules
   doctl compute firewall create \
     --name production-firewall \
     --inbound-rules "protocol:tcp,ports:22,sources:addresses:10.0.0.0/8" \
     --inbound-rules "protocol:tcp,ports:443,sources:addresses:0.0.0.0/0" \
     --outbound-rules "protocol:tcp,ports:443,destinations:addresses:0.0.0.0/0" \
     --outbound-rules "protocol:tcp,ports:80,destinations:addresses:0.0.0.0/0" \
     --outbound-rules "protocol:udp,ports:53,destinations:addresses:0.0.0.0/0"
   ```

3. **VPC Implementation**
   ```bash
   # Isolate resources in VPC
   doctl vpcs create \
     --name secure-vpc \
     --region nyc3 \
     --ip-range 10.0.0.0/16
   
   # Create database in VPC only
   doctl databases create secure-db \
     --engine pg \
     --region nyc3 \
     --private-network-uuid <vpc-uuid>
   ```

4. **Secrets Management**
   ```bash
   # Use environment variables for sensitive data
   doctl apps update <app-id> \
     --env-file .env.production
   
   # Encrypt sensitive files
   openssl enc -aes-256-cbc -salt -in secrets.txt -out secrets.enc -k $PASSWORD
   ```

5. **Monitoring and Alerts**
   ```bash
   # Create monitoring alerts
   doctl monitoring alert create \
     --type "v1/insights/droplet/cpu" \
     --name "High CPU Alert" \
     --description "CPU usage above 80%" \
     --compare GreaterThan \
     --value 80 \
     --window "5m" \
     --entities <droplet-id> \
     --emails "alerts@example.com"
   ```

### Performance Optimization

1. **CDN Configuration**
   ```python
   # Configure Spaces CDN
   import requests
   
   headers = {
       'Authorization': f'Bearer {DO_TOKEN}',
       'Content-Type': 'application/json'
   }
   
   cdn_config = {
       'origin': 'myspace.nyc3.digitaloceanspaces.com',
       'ttl': 86400,
       'custom_domain': 'cdn.example.com',
       'certificate_id': 'cert-uuid'
   }
   
   response = requests.post(
       'https://api.digitalocean.com/v2/cdn/endpoints',
       json=cdn_config,
       headers=headers
   )
   ```

2. **Database Optimization**
   ```sql
   -- PostgreSQL performance tuning
   ALTER SYSTEM SET shared_buffers = '256MB';
   ALTER SYSTEM SET effective_cache_size = '1GB';
   ALTER SYSTEM SET maintenance_work_mem = '64MB';
   ALTER SYSTEM SET checkpoint_completion_target = '0.9';
   ALTER SYSTEM SET wal_buffers = '16MB';
   ALTER SYSTEM SET random_page_cost = '1.1';
   
   -- Create indexes
   CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
   CREATE INDEX CONCURRENTLY idx_orders_created ON orders(created_at);
   
   -- Analyze tables
   ANALYZE users;
   ANALYZE orders;
   ```

3. **Application Performance**
   ```javascript
   // PM2 ecosystem config
   module.exports = {
     apps: [{
       name: 'app',
       script: './server.js',
       instances: 'max',
       exec_mode: 'cluster',
       env: {
         NODE_ENV: 'production',
         PORT: 3000
       },
       error_file: './logs/err.log',
       out_file: './logs/out.log',
       log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
       max_memory_restart: '1G'
     }]
   };
   ```

## Common Architectures

### 1. High-Availability Web Application

```yaml
# Architecture:
# - Load Balancer (entry point)
# - 3+ Web Droplets (different availability zones)
# - Managed PostgreSQL (primary + standby)
# - Redis for caching
# - Spaces for static assets

# Docker Compose for local development
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

```bash
# Deployment script
#!/bin/bash

# Build and push Docker image
docker build -t myapp:latest .
doctl registry login
docker tag myapp:latest registry.digitalocean.com/myregistry/myapp:latest
docker push registry.digitalocean.com/myregistry/myapp:latest

# Update Droplets
for droplet_id in $(doctl compute droplet list --format ID --no-header); do
  doctl compute ssh $droplet_id --ssh-command "
    docker pull registry.digitalocean.com/myregistry/myapp:latest
    docker stop myapp || true
    docker rm myapp || true
    docker run -d --name myapp \
      -p 3000:3000 \
      --restart unless-stopped \
      -e DATABASE_URL=$DATABASE_URL \
      -e REDIS_URL=$REDIS_URL \
      registry.digitalocean.com/myregistry/myapp:latest
  "
done
```

### 2. Kubernetes Microservices

```yaml
# kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: microservices
---
# kubernetes/frontend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: microservices
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: registry.digitalocean.com/myregistry/frontend:v1.0
        ports:
        - containerPort: 3000
        env:
        - name: API_URL
          value: "http://api-service:8080"
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: microservices
  annotations:
    service.beta.kubernetes.io/do-loadbalancer-enable-proxy-protocol: "true"
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 3000
  selector:
    app: frontend
---
# kubernetes/api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: microservices
spec:
  replicas: 5
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: registry.digitalocean.com/myregistry/api:v1.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis.url
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: microservices
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 3. Serverless Event Processing

```javascript
// functions/webhook/index.js
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

exports.main = async (event) => {
  const { headers, body } = event;
  
  // Verify webhook signature
  const signature = headers['x-webhook-signature'];
  if (!verifySignature(body, signature)) {
    return {
      statusCode: 401,
      body: JSON.stringify({ error: 'Invalid signature' })
    };
  }
  
  const data = JSON.parse(body);
  
  try {
    // Process webhook
    await pool.query(
      'INSERT INTO webhooks (type, payload, processed_at) VALUES ($1, $2, NOW())',
      [data.type, JSON.stringify(data)]
    );
    
    // Trigger additional processing
    if (data.type === 'payment.completed') {
      await processPayment(data);
    }
    
    return {
      statusCode: 200,
      body: JSON.stringify({ success: true })
    };
  } catch (error) {
    console.error('Webhook processing error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Processing failed' })
    };
  }
};

function verifySignature(payload, signature) {
  const crypto = require('crypto');
  const expectedSignature = crypto
    .createHmac('sha256', process.env.WEBHOOK_SECRET)
    .update(payload)
    .digest('hex');
  return signature === expectedSignature;
}
```

### 4. Static Site with API

```nginx
# Nginx configuration for static site + API
server {
    listen 80;
    server_name example.com;
    root /var/www/static;

    # Static files
    location / {
        try_files $uri $uri/ /index.html;
        expires 1h;
        add_header Cache-Control "public, must-revalidate";
    }

    # API proxy
    location /api/ {
        proxy_pass http://localhost:3000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

## Monitoring and Logging

### DigitalOcean Monitoring

```python
# Python monitoring client
import requests
from datetime import datetime, timedelta

class DOMonitoring:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.digitalocean.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def get_droplet_metrics(self, droplet_id, metric="cpu", start=None, end=None):
        if not start:
            start = datetime.utcnow() - timedelta(hours=1)
        if not end:
            end = datetime.utcnow()
        
        params = {
            "start": start.isoformat() + "Z",
            "end": end.isoformat() + "Z",
            "host_id": droplet_id
        }
        
        response = requests.get(
            f"{self.base_url}/monitoring/metrics/{metric}",
            headers=self.headers,
            params=params
        )
        
        return response.json()
    
    def create_alert(self, alert_config):
        response = requests.post(
            f"{self.base_url}/monitoring/alerts",
            headers=self.headers,
            json=alert_config
        )
        
        return response.json()

# Usage
monitor = DOMonitoring("your-api-token")

# Get CPU metrics
metrics = monitor.get_droplet_metrics("droplet-id", "cpu")

# Create alert
alert = monitor.create_alert({
    "alerts": {
        "slack": [{
            "channel": "#alerts",
            "url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
        }]
    },
    "compare": "GreaterThan",
    "description": "High memory usage",
    "enabled": True,
    "entities": ["droplet-id"],
    "tags": ["production"],
    "type": "v1/insights/droplet/memory_utilization_percent",
    "value": 90,
    "window": "5m"
})
```

### Custom Logging Solution

```javascript
// Winston logging configuration
const winston = require('winston');
const { format } = winston;

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: format.combine(
    format.timestamp(),
    format.errors({ stack: true }),
    format.json()
  ),
  defaultMeta: { service: 'api' },
  transports: [
    new winston.transports.File({ 
      filename: 'error.log', 
      level: 'error',
      maxsize: 5242880, // 5MB
      maxFiles: 5
    }),
    new winston.transports.File({ 
      filename: 'combined.log',
      maxsize: 5242880, // 5MB
      maxFiles: 5
    })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: format.combine(
      format.colorize(),
      format.simple()
    )
  }));
}

// Log to external service
if (process.env.LOGTAIL_TOKEN) {
  const Logtail = require('@logtail/node');
  const logtail = new Logtail(process.env.LOGTAIL_TOKEN);
  
  logger.add(new winston.transports.Stream({
    stream: logtail.stream()
  }));
}

module.exports = logger;
```

## Interview Preparation

### Common DigitalOcean Interview Questions

1. **What makes DigitalOcean different from AWS/Azure/GCP?**
   - Simplicity and developer experience
   - Transparent, predictable pricing
   - Focused product lineup
   - Excellent documentation and tutorials
   - Better for small to medium workloads

2. **Explain DigitalOcean's networking options**
   - Floating IPs: Reassignable public IPs
   - VPC: Private networking within a region
   - Load Balancers: Regional traffic distribution
   - Firewalls: Cloud-level security rules

3. **How do you handle high availability on DigitalOcean?**
   - Multiple Droplets across availability zones
   - Load Balancer with health checks
   - Managed databases with standby nodes
   - Floating IPs for failover

4. **What are DigitalOcean Spaces?**
   - S3-compatible object storage
   - Built-in CDN capability
   - Simple pricing: $5/month for 250GB
   - Good for static assets, backups

5. **How does App Platform work?**
   - PaaS offering similar to Heroku
   - Automatic builds from Git
   - Built-in CI/CD
   - Automatic SSL certificates
   - Auto-scaling capabilities

### Hands-On Scenarios

1. **Deploy a production-ready web application**
   ```bash
   # Create infrastructure
   doctl compute droplet create web-{1..3} \
     --region nyc3 \
     --size s-2vcpu-4gb \
     --image docker-20-04 \
     --vpc-uuid $VPC_ID
   
   # Setup load balancer
   doctl compute load-balancer create \
     --name production-lb \
     --region nyc3 \
     --droplet-ids $(doctl compute droplet list --format ID --no-header | tr '\n' ',')
   ```

2. **Implement blue-green deployment**
   - Maintain two identical environments
   - Switch load balancer between them
   - Zero-downtime deployments

3. **Setup monitoring and alerting**
   - Enable monitoring on all Droplets
   - Create CPU/memory/disk alerts
   - Setup external monitoring with Prometheus

### Cost Comparison Scenarios

**Q: How would you optimize costs for a startup on DigitalOcean?**

```
Strategy:
1. Start with basic Droplets ($4-6/month)
2. Use managed databases ($15/month) vs self-managed
3. Implement auto-shutdown for dev environments
4. Use Spaces CDN instead of separate CDN service
5. Reserved Droplets for predictable workloads

Example monthly costs:
- 3x $12 Droplets (web servers): $36
- 1x $15 Managed PostgreSQL: $15
- 1x $10 Redis: $10
- Load Balancer: $12
- Spaces + Bandwidth: $5
Total: ~$78/month for HA setup
```

## Resources

### Official Documentation
- [DigitalOcean Documentation](https://docs.digitalocean.com/)
- [API Reference](https://docs.digitalocean.com/reference/api/)
- [Community Tutorials](https://www.digitalocean.com/community/tutorials)
- [Product Documentation](https://docs.digitalocean.com/products/)

### Learning Resources
- [DigitalOcean Learning Hub](https://www.digitalocean.com/community/learning-paths)
- [Free Credit for New Users](https://www.digitalocean.com/try)
- [Navigator Program](https://www.digitalocean.com/navigator) - Free credits for learning
- [Tech Talks](https://www.digitalocean.com/community/tech-talks)

### Tools and SDKs
- [doctl CLI](https://github.com/digitalocean/doctl)
- [Official API Clients](https://github.com/digitalocean)
- [Terraform Provider](https://registry.terraform.io/providers/digitalocean/digitalocean/latest)
- [Kubernetes CSI Driver](https://github.com/digitalocean/csi-digitalocean)

### Community Resources
- [DigitalOcean Community](https://www.digitalocean.com/community)
- [Questions & Answers](https://www.digitalocean.com/community/questions)
- [Reddit - r/digital_ocean](https://www.reddit.com/r/digital_ocean/)
- [GitHub - awesome-digitalocean](https://github.com/jonleibowitz/awesome-digitalocean)

### Marketplace and 1-Click Apps
- [DigitalOcean Marketplace](https://marketplace.digitalocean.com/)
- [1-Click Apps](https://marketplace.digitalocean.com/category/1-click-apps)
- Popular apps: WordPress, GitLab, Docker, OpenVPN

### Migration Resources
- [Migration Guide](https://docs.digitalocean.com/products/droplets/how-to/migrate/)
- [AWS to DigitalOcean](https://www.digitalocean.com/resources/cloud-migration)
- [Import Custom Images](https://docs.digitalocean.com/products/images/custom-images/)

### Monitoring and Management
- [DigitalOcean Monitoring](https://docs.digitalocean.com/products/monitoring/)
- [Third-party Integrations](https://marketplace.digitalocean.com/category/monitoring)
- [Terraform Cloud Integration](https://www.terraform.io/cloud-docs/integrations/digitalocean)

### Support Resources
- [Support Center](https://www.digitalocean.com/support)
- [System Status](https://status.digitalocean.com/)
- [Feature Requests](https://ideas.digitalocean.com/)

### YouTube Channels and Video Resources
- [DigitalOcean YouTube](https://www.youtube.com/digitalocean)
- [Tech with Tim - DigitalOcean Tutorials](https://www.youtube.com/c/TechWithTim)
- [Traversy Media - DigitalOcean Deploy](https://www.youtube.com/c/TraversyMedia)