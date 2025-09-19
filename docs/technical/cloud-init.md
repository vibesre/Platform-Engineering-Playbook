# Cloud-init: Cloud Instance Initialization

## Overview

Cloud-init is the industry standard multi-distribution method for cross-platform cloud instance initialization. It runs during the initial boot of a cloud instance and performs configuration tasks such as setting up users, installing packages, writing files, and configuring network settings. Cloud-init supports all major cloud providers and can work with private cloud solutions.

## Architecture

### Boot Process and Stages

```
┌─────────────────────────────────────────────────────────────┐
│                     System Boot Process                      │
├─────────────────────────────────────────────────────────────┤
│  BIOS/UEFI → Bootloader → Kernel → Init System → Cloud-init│
└─────────────────────────────────────────────────────────────┘
                                                      │
┌─────────────────────────────────────────────────────┴────────┐
│                    Cloud-init Boot Stages                    │
│                                                              │
│  ┌───────────────┐  ┌────────────────┐  ┌────────────────┐ │
│  │ 1. Generator  │  │ 2. Local Stage │  │ 3. Init Stage  │ │
│  │  (systemd)    │→ │  (filesystem)  │→ │  (network)     │ │
│  └───────────────┘  └────────────────┘  └────────────────┘ │
│                                                    ↓         │
│  ┌───────────────┐  ┌────────────────┐                     │
│  │ 5. Final Stage│ ←│ 4. Config Stage│                     │
│  │  (scripts)    │  │  (user-data)   │                     │
│  └───────────────┘  └────────────────┘                     │
└──────────────────────────────────────────────────────────────┘
```

### Data Sources Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Cloud-init Core                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Data Source Detection                   │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────┼──────────────────────────────┐   │
│  │                      ↓                               │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐│   │
│  │  │  AWS    │  │  Azure  │  │  GCP    │  │OpenStack││   │
│  │  │  EC2    │  │         │  │  GCE    │  │         ││   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬───┘│   │
│  │       │            │            │            │      │   │
│  └───────┼────────────┼────────────┼────────────┼──────┘   │
│          ↓            ↓            ↓            ↓           │
│     ┌────────────────────────────────────────────────┐     │
│     │         Metadata Service (169.254.169.254)     │     │
│     │  • Instance ID    • User Data                  │     │
│     │  • SSH Keys       • Vendor Data                │     │
│     │  • Network Config • Meta Data                  │     │
│     └────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Practical Examples

### Basic Cloud-config

```yaml
#cloud-config
# Basic instance configuration

# Update and upgrade packages
package_update: true
package_upgrade: true
package_reboot_if_required: true

# Configure users
users:
  - default
  - name: devops
    groups: [sudo, docker]
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh_authorized_keys:
      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAB...

# Install packages
packages:
  - docker.io
  - docker-compose
  - git
  - vim
  - htop
  - curl
  - jq
  - python3-pip

# Write files
write_files:
  - path: /etc/motd
    content: |
      ################################################
      #     Welcome to Production Web Server         #
      #     Managed by Cloud-init and Terraform      #
      ################################################
    
  - path: /etc/docker/daemon.json
    content: |
      {
        "log-driver": "json-file",
        "log-opts": {
          "max-size": "10m",
          "max-file": "3"
        },
        "storage-driver": "overlay2"
      }
    permissions: '0644'

# Run commands
runcmd:
  - systemctl enable docker
  - systemctl start docker
  - usermod -aG docker ubuntu
  - curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  - chmod +x /usr/local/bin/docker-compose

# Configure SSH
ssh_pwauth: false
disable_root: true

# Set timezone
timezone: UTC

# Configure NTP
ntp:
  enabled: true
  servers:
    - ntp.ubuntu.com
    - time.nist.gov
```

### Advanced Network Configuration

```yaml
#cloud-config
# Advanced networking setup

# Network configuration (Netplan format for Ubuntu)
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
      dhcp6: false
    eth1:
      addresses:
        - 10.0.1.10/24
      gateway4: 10.0.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
      routes:
        - to: 10.0.2.0/24
          via: 10.0.1.1
          metric: 100

# Configure hostname and hosts file
hostname: web-prod-01
fqdn: web-prod-01.example.com
manage_etc_hosts: true

# Advanced write_files with templates
write_files:
  - path: /etc/netplan/60-static.yaml
    content: |
      network:
        version: 2
        ethernets:
          eth1:
            addresses: [${ip_address}/24]
            gateway4: ${gateway}
            nameservers:
              addresses: ${dns_servers}
    defer: true

  - path: /usr/local/bin/setup-networking.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      # Setup advanced networking
      
      # Enable IP forwarding
      echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
      sysctl -p
      
      # Configure iptables
      iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
      iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
      iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
      
      # Save iptables rules
      iptables-save > /etc/iptables/rules.v4

# Boot commands (run earlier in boot process)
bootcmd:
  - echo "Starting network configuration..." > /var/log/cloud-init-network.log

# Run networking setup
runcmd:
  - /usr/local/bin/setup-networking.sh
  - netplan apply
```

### Container Orchestration Setup

```yaml
#cloud-config
# Kubernetes node initialization

# Install Docker and Kubernetes packages
package_update: true
packages:
  - apt-transport-https
  - ca-certificates
  - curl
  - gnupg
  - lsb-release

write_files:
  # Docker repository setup
  - path: /etc/apt/sources.list.d/docker.list
    content: |
      deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu focal stable

  # Kubernetes repository setup  
  - path: /etc/apt/sources.list.d/kubernetes.list
    content: |
      deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main

  # Kubernetes configuration
  - path: /etc/modules-load.d/k8s.conf
    content: |
      overlay
      br_netfilter

  - path: /etc/sysctl.d/k8s.conf
    content: |
      net.bridge.bridge-nf-call-iptables  = 1
      net.bridge.bridge-nf-call-ip6tables = 1
      net.ipv4.ip_forward                 = 1

  # Containerd configuration
  - path: /etc/containerd/config.toml
    content: |
      version = 2
      [plugins]
        [plugins."io.containerd.grpc.v1.cri"]
          [plugins."io.containerd.grpc.v1.cri".containerd]
            [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
              [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
                runtime_type = "io.containerd.runc.v2"
                [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
                  SystemdCgroup = true

  # Kubeadm configuration
  - path: /etc/kubernetes/kubeadm-config.yaml
    content: |
      apiVersion: kubeadm.k8s.io/v1beta3
      kind: InitConfiguration
      nodeRegistration:
        kubeletExtraArgs:
          cloud-provider: "external"
      ---
      apiVersion: kubeadm.k8s.io/v1beta3
      kind: ClusterConfiguration
      kubernetesVersion: v1.27.0
      networking:
        podSubnet: "10.244.0.0/16"
        serviceSubnet: "10.96.0.0/12"

runcmd:
  # Add Docker GPG key
  - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  
  # Add Kubernetes GPG key
  - curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/kubernetes-archive-keyring.gpg
  
  # Update apt and install packages
  - apt-get update
  - apt-get install -y containerd.io kubelet kubeadm kubectl
  - apt-mark hold kubelet kubeadm kubectl
  
  # Configure containerd
  - containerd config default | tee /etc/containerd/config.toml
  - systemctl restart containerd
  
  # Load kernel modules
  - modprobe overlay
  - modprobe br_netfilter
  - sysctl --system
  
  # Initialize Kubernetes (for master node)
  - |
    if [ "${node_role}" = "master" ]; then
      kubeadm init --config=/etc/kubernetes/kubeadm-config.yaml
      mkdir -p /home/ubuntu/.kube
      cp -i /etc/kubernetes/admin.conf /home/ubuntu/.kube/config
      chown ubuntu:ubuntu /home/ubuntu/.kube/config
      
      # Install CNI plugin (Calico)
      kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
    fi

  # Join cluster (for worker nodes)
  - |
    if [ "${node_role}" = "worker" ]; then
      kubeadm join ${master_ip}:6443 --token ${join_token} \
        --discovery-token-ca-cert-hash sha256:${discovery_token_hash}
    fi
```

### Application Deployment

```yaml
#cloud-config
# Deploy web application with monitoring

merge_how:
  - name: list
    settings: [append]
  - name: dict
    settings: [no_replace, recurse_list]

users:
  - default
  - name: app
    system: true
    shell: /bin/false

write_files:
  # Application service
  - path: /etc/systemd/system/webapp.service
    content: |
      [Unit]
      Description=Web Application
      After=network.target
      
      [Service]
      Type=simple
      User=app
      Group=app
      WorkingDirectory=/opt/webapp
      Environment="PORT=3000"
      Environment="NODE_ENV=production"
      ExecStart=/usr/bin/node /opt/webapp/server.js
      Restart=always
      RestartSec=10
      
      # Security settings
      NoNewPrivileges=true
      PrivateTmp=true
      ProtectSystem=strict
      ProtectHome=true
      ReadWritePaths=/opt/webapp/data
      
      [Install]
      WantedBy=multi-user.target

  # Nginx configuration
  - path: /etc/nginx/sites-available/webapp
    content: |
      upstream webapp {
        server 127.0.0.1:3000;
        keepalive 64;
      }
      
      server {
        listen 80;
        server_name ${domain_name};
        
        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
      }
      
      server {
        listen 443 ssl http2;
        server_name ${domain_name};
        
        ssl_certificate /etc/letsencrypt/live/${domain_name}/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/${domain_name}/privkey.pem;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
        
        location / {
          proxy_pass http://webapp;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection 'upgrade';
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
          proxy_cache_bypass $http_upgrade;
        }
        
        location /health {
          access_log off;
          return 200 "healthy\n";
        }
      }

  # Prometheus node exporter
  - path: /etc/systemd/system/node_exporter.service
    content: |
      [Unit]
      Description=Prometheus Node Exporter
      After=network.target
      
      [Service]
      Type=simple
      User=prometheus
      Group=prometheus
      ExecStart=/usr/local/bin/node_exporter \
        --collector.filesystem.mount-points-exclude='^/(sys|proc|dev|host|etc)($$|/)' \
        --collector.netclass.ignored-devices='^(veth.*|docker.*|br-.*)$$'
      Restart=on-failure
      RestartSec=5
      
      [Install]
      WantedBy=multi-user.target

packages:
  - nginx
  - nodejs
  - npm
  - certbot
  - python3-certbot-nginx

runcmd:
  # Create application directory
  - mkdir -p /opt/webapp/data
  - chown -R app:app /opt/webapp
  
  # Deploy application
  - |
    cd /opt/webapp
    curl -L "${app_artifact_url}" | tar xz
    npm install --production
    
  # Setup SSL certificate
  - |
    certbot certonly --nginx \
      --non-interactive \
      --agree-tos \
      --email ${admin_email} \
      --domains ${domain_name}
  
  # Enable Nginx site
  - ln -s /etc/nginx/sites-available/webapp /etc/nginx/sites-enabled/
  - nginx -t && systemctl restart nginx
  
  # Install and configure Prometheus node exporter
  - |
    useradd --no-create-home --shell /bin/false prometheus
    curl -L https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz | tar xz -C /tmp
    mv /tmp/node_exporter-*/node_exporter /usr/local/bin/
    chown prometheus:prometheus /usr/local/bin/node_exporter
  
  # Start services
  - systemctl daemon-reload
  - systemctl enable --now webapp.service
  - systemctl enable --now node_exporter.service

# Run scripts on every boot
bootcmd:
  - echo "Starting application deployment..." >> /var/log/cloud-init-app.log

# Final message
final_message: |
  Cloud-init completed in $UPTIME seconds
  Webapp URL: https://${domain_name}
  Node Exporter: http://$INSTANCE_IP:9100/metrics
```

### Multi-Part User Data

```yaml
Content-Type: multipart/mixed; boundary="==BOUNDARY=="
MIME-Version: 1.0

--==BOUNDARY==
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.yaml"

#cloud-config
# Part 1: Cloud-config for basic setup

users:
  - default
  - name: admin
    groups: [sudo]
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']

packages:
  - git
  - python3
  - python3-pip

--==BOUNDARY==
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="setup.sh"

#!/bin/bash
# Part 2: Shell script for complex setup

set -e

echo "Starting custom setup script..."

# Install Docker
curl -fsSL https://get.docker.com | sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create application directories
mkdir -p /opt/app/{config,data,logs}

# Clone application repository
git clone https://github.com/company/app.git /opt/app/src

# Set up environment
cat > /opt/app/.env <<EOF
NODE_ENV=production
DATABASE_URL=${database_url}
REDIS_URL=${redis_url}
SECRET_KEY=${secret_key}
EOF

# Start application
cd /opt/app/src
docker-compose up -d

echo "Custom setup completed!"

--==BOUNDARY==
Content-Type: text/cloud-boothook; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="boothook.sh"

#!/bin/bash
# Part 3: Boot hook (runs on every boot)

# Mount EBS volume if attached
if [ -e /dev/xvdf ]; then
    mkdir -p /data
    mount /dev/xvdf /data || mkfs.ext4 /dev/xvdf && mount /dev/xvdf /data
    echo "/dev/xvdf /data ext4 defaults,nofail 0 2" >> /etc/fstab
fi

--==BOUNDARY==
Content-Type: text/jinja2; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="config.j2"

## template: jinja
# Part 4: Jinja2 template
{%- set hostname = v1.local_hostname -%}
{%- set fqdn = v1.fqdn -%}
{%- set region = v1.availability_zone[:-1] -%}

write_files:
  - path: /etc/application.conf
    content: |
      hostname: {{ hostname }}
      fqdn: {{ fqdn }}
      region: {{ region }}
      instance_id: {{ v1.instance_id }}
      local_ipv4: {{ v1.local_ipv4 }}

--==BOUNDARY==--
```

## Best Practices

### 1. Modular Configuration

```yaml
#cloud-config
# Use includes for modular configuration

include_once:
  - https://config.example.com/cloud-init/base.yaml
  - https://config.example.com/cloud-init/security.yaml
  - https://config.example.com/cloud-init/monitoring.yaml

# Merge user data
merge_how:
  - name: list
    settings: [append]
  - name: dict
    settings: [no_replace, recurse_list]

# Local overrides
packages:
  - specific-package-for-this-instance

write_files:
  - path: /etc/instance-specific.conf
    content: |
      # Instance-specific configuration
      role: ${instance_role}
      environment: ${environment}
```

### 2. Idempotent Operations

```yaml
#cloud-config
# Ensure idempotent operations

runcmd:
  # Check before creating
  - |
    if [ ! -f /opt/app/installed ]; then
      echo "Installing application..."
      curl -L "${app_url}" | tar xz -C /opt/app
      touch /opt/app/installed
    fi
  
  # Use systemctl conditional restart
  - systemctl is-active nginx || systemctl start nginx
  
  # Conditional configuration
  - |
    if ! grep -q "custom_config" /etc/app.conf; then
      echo "custom_config=true" >> /etc/app.conf
    fi

# Use defer for files that need variable substitution
write_files:
  - path: /etc/app/config.yaml
    content: |
      instance_id: $INSTANCE_ID
      region: $REGION
    defer: true
```

### 3. Error Handling

```yaml
#cloud-config
# Robust error handling

write_files:
  - path: /usr/local/bin/safe-deploy.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      set -euo pipefail
      
      # Logging function
      log() {
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a /var/log/cloud-init-deploy.log
      }
      
      # Error handler
      error_handler() {
        log "ERROR: Command failed at line $1"
        # Send alert
        curl -X POST https://alerts.example.com/webhook \
          -H "Content-Type: application/json" \
          -d "{\"text\": \"Cloud-init failed on $(hostname): $2\"}"
        exit 1
      }
      
      trap 'error_handler $LINENO "$BASH_COMMAND"' ERR
      
      # Deployment steps
      log "Starting deployment..."
      
      # Download with retry
      for i in {1..5}; do
        if curl -fsSL "${app_url}" -o /tmp/app.tar.gz; then
          break
        fi
        log "Download attempt $i failed, retrying..."
        sleep 10
      done
      
      # Verify download
      if [ ! -f /tmp/app.tar.gz ]; then
        log "ERROR: Failed to download application"
        exit 1
      fi
      
      # Extract and verify
      tar -tzf /tmp/app.tar.gz > /dev/null || {
        log "ERROR: Invalid archive"
        exit 1
      }
      
      tar -xzf /tmp/app.tar.gz -C /opt/app
      
      log "Deployment completed successfully"

runcmd:
  - /usr/local/bin/safe-deploy.sh 2>&1 | tee -a /var/log/cloud-init-deploy.log
```

### 4. Secrets Management

```yaml
#cloud-config
# Secure secrets handling

write_files:
  # Use AWS Secrets Manager
  - path: /usr/local/bin/fetch-secrets.sh
    permissions: '0700'
    owner: root:root
    content: |
      #!/bin/bash
      
      # Fetch from AWS Secrets Manager
      DB_SECRET=$(aws secretsmanager get-secret-value \
        --secret-id prod/db/password \
        --query SecretString \
        --output text)
      
      # Write to secure location
      mkdir -p /etc/secrets
      chmod 700 /etc/secrets
      echo "DB_PASSWORD=${DB_SECRET}" > /etc/secrets/db
      chmod 600 /etc/secrets/db
      
      # Fetch from HashiCorp Vault
      export VAULT_ADDR="https://vault.example.com"
      export VAULT_TOKEN=$(aws ssm get-parameter \
        --name /vault/token \
        --with-decryption \
        --query Parameter.Value \
        --output text)
      
      API_KEY=$(vault kv get -field=api_key secret/app)
      echo "API_KEY=${API_KEY}" > /etc/secrets/api
      chmod 600 /etc/secrets/api

# Don't log sensitive data
runcmd:
  - /usr/local/bin/fetch-secrets.sh
  - 'source /etc/secrets/db && export DB_PASSWORD'
  - 'source /etc/secrets/api && export API_KEY'
  # Use secrets without logging
  - 'envsubst < /opt/app/config.template > /opt/app/config.json'
```

## Production Deployment Patterns

### 1. Auto-Scaling Group Configuration

```yaml
#cloud-config
# ASG instance configuration

write_files:
  - path: /usr/local/bin/asg-lifecycle.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      
      # Get instance metadata
      INSTANCE_ID=$(ec2-metadata --instance-id | cut -d " " -f 2)
      REGION=$(ec2-metadata --availability-zone | cut -d " " -f 2 | sed 's/.$//')
      ASG_NAME=$(aws autoscaling describe-auto-scaling-instances \
        --instance-ids $INSTANCE_ID \
        --region $REGION \
        --query "AutoScalingInstances[0].AutoScalingGroupName" \
        --output text)
      
      # Complete lifecycle action
      complete_lifecycle() {
        aws autoscaling complete-lifecycle-action \
          --lifecycle-action-result $1 \
          --lifecycle-hook-name $2 \
          --auto-scaling-group-name $ASG_NAME \
          --instance-id $INSTANCE_ID \
          --region $REGION
      }
      
      # Health check
      health_check() {
        for i in {1..30}; do
          if curl -f http://localhost/health; then
            return 0
          fi
          sleep 10
        done
        return 1
      }
      
      # Main lifecycle handling
      if [ "$1" = "launching" ]; then
        if health_check; then
          complete_lifecycle "CONTINUE" "LaunchingLifecycleHook"
        else
          complete_lifecycle "ABANDON" "LaunchingLifecycleHook"
        fi
      elif [ "$1" = "terminating" ]; then
        # Graceful shutdown
        systemctl stop webapp
        sleep 30
        complete_lifecycle "CONTINUE" "TerminatingLifecycleHook"
      fi

runcmd:
  # Configure CloudWatch agent
  - |
    cat > /opt/aws/amazon-cloudwatch-agent/etc/config.json <<EOF
    {
      "metrics": {
        "namespace": "WebApp",
        "metrics_collected": {
          "cpu": {
            "measurement": [
              {"name": "cpu_usage_idle", "rename": "CPU_IDLE"},
              "cpu_usage_iowait"
            ],
            "totalcpu": false
          },
          "disk": {
            "measurement": [
              "used_percent"
            ],
            "resources": [
              "*"
            ]
          },
          "mem": {
            "measurement": [
              "mem_used_percent"
            ]
          }
        }
      },
      "logs": {
        "logs_collected": {
          "files": {
            "collect_list": [
              {
                "file_path": "/var/log/webapp/*.log",
                "log_group_name": "/aws/ec2/webapp",
                "log_stream_name": "{instance_id}"
              }
            ]
          }
        }
      }
    }
    EOF
  
  # Start CloudWatch agent
  - /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
      -a query -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/config.json -s
  
  # Handle launch lifecycle
  - /usr/local/bin/asg-lifecycle.sh launching &
```

### 2. Immutable Infrastructure

```yaml
#cloud-config
# Immutable infrastructure setup

bootcmd:
  # Make filesystem read-only except specific paths
  - echo "tmpfs /tmp tmpfs defaults,noatime,mode=1777 0 0" >> /etc/fstab
  - echo "tmpfs /var/tmp tmpfs defaults,noatime,mode=1777 0 0" >> /etc/fstab

write_files:
  - path: /etc/systemd/system/make-readonly.service
    content: |
      [Unit]
      Description=Make filesystem read-only
      Before=multi-user.target
      
      [Service]
      Type=oneshot
      ExecStart=/usr/local/bin/make-readonly.sh
      RemainAfterExit=yes
      
      [Install]
      WantedBy=multi-user.target

  - path: /usr/local/bin/make-readonly.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      
      # Remount root as read-only
      mount -o remount,ro /
      
      # Create overlayfs for writable directories
      for dir in /etc /var/log /var/lib; do
        mkdir -p /overlay/upper/$dir /overlay/work/$dir
        mount -t overlay overlay \
          -o lowerdir=$dir,upperdir=/overlay/upper/$dir,workdir=/overlay/work/$dir \
          $dir
      done

# Pull application from immutable source
runcmd:
  # Download pre-built application image
  - |
    IMAGE_URL="https://artifacts.example.com/webapp/v${VERSION}/image.squashfs"
    curl -fsSL "$IMAGE_URL" -o /opt/webapp.squashfs
    
  # Mount squashfs image
  - mkdir -p /opt/webapp
  - mount -t squashfs -o loop /opt/webapp.squashfs /opt/webapp
  
  # Verify integrity
  - |
    EXPECTED_SHA256="${IMAGE_SHA256}"
    ACTUAL_SHA256=$(sha256sum /opt/webapp.squashfs | cut -d' ' -f1)
    if [ "$EXPECTED_SHA256" != "$ACTUAL_SHA256" ]; then
      echo "ERROR: Image integrity check failed"
      exit 1
    fi
  
  # Enable read-only filesystem
  - systemctl enable make-readonly.service
```

### 3. Service Mesh Integration

```yaml
#cloud-config
# Istio/Envoy sidecar setup

write_files:
  - path: /etc/systemd/system/envoy.service
    content: |
      [Unit]
      Description=Envoy Proxy
      After=network-online.target
      Wants=network-online.target
      
      [Service]
      Type=simple
      User=envoy
      Group=envoy
      ExecStart=/usr/local/bin/envoy \
        -c /etc/envoy/envoy.yaml \
        --service-cluster ${SERVICE_NAME} \
        --service-node ${INSTANCE_ID}
      Restart=always
      RestartSec=5
      
      [Install]
      WantedBy=multi-user.target

  - path: /etc/envoy/envoy.yaml
    content: |
      node:
        cluster: ${SERVICE_NAME}
        id: ${INSTANCE_ID}
      
      admin:
        address:
          socket_address:
            protocol: TCP
            address: 127.0.0.1
            port_value: 9901
      
      static_resources:
        listeners:
        - name: listener_0
          address:
            socket_address:
              protocol: TCP
              address: 0.0.0.0
              port_value: 80
          filter_chains:
          - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: ingress_http
                route_config:
                  name: local_route
                  virtual_hosts:
                  - name: local_service
                    domains: ["*"]
                    routes:
                    - match:
                        prefix: "/"
                      route:
                        cluster: local_service
                http_filters:
                - name: envoy.filters.http.router
                  typed_config:
                    "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
        
        clusters:
        - name: local_service
          connect_timeout: 5s
          type: STATIC
          lb_policy: ROUND_ROBIN
          load_assignment:
            cluster_name: local_service
            endpoints:
            - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: 127.0.0.1
                      port_value: 3000

runcmd:
  # Create envoy user
  - useradd -r -s /bin/false envoy
  
  # Install Envoy
  - |
    curl -L https://github.com/envoyproxy/envoy/releases/download/v1.27.0/envoy-1.27.0-linux-x86_64 -o /usr/local/bin/envoy
    chmod +x /usr/local/bin/envoy
  
  # Configure iptables for traffic interception
  - |
    # Redirect inbound traffic to Envoy
    iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 15001
    
    # Redirect outbound traffic to Envoy
    iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner envoy -j REDIRECT --to-port 15001
  
  # Start services
  - systemctl daemon-reload
  - systemctl enable --now envoy
```

### 4. Compliance and Hardening

```yaml
#cloud-config
# CIS benchmark compliance

# Disable root login
disable_root: true
ssh_pwauth: false

write_files:
  # SSH hardening
  - path: /etc/ssh/sshd_config.d/hardening.conf
    content: |
      Protocol 2
      PermitRootLogin no
      PasswordAuthentication no
      PermitEmptyPasswords no
      MaxAuthTries 4
      ClientAliveInterval 300
      ClientAliveCountMax 0
      LoginGraceTime 60
      Banner /etc/ssh/banner
      X11Forwarding no
      MaxStartups 10:30:60
      MaxSessions 4
      AllowUsers ubuntu admin

  # Audit rules
  - path: /etc/audit/rules.d/cis.rules
    content: |
      # Monitor user/group modifications
      -w /etc/group -p wa -k identity
      -w /etc/passwd -p wa -k identity
      -w /etc/shadow -p wa -k identity
      
      # Monitor sudo commands
      -w /usr/bin/sudo -p x -k actions
      
      # Monitor SSH configuration
      -w /etc/ssh/sshd_config -p wa -k sshd_config
      
      # Monitor system calls
      -a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change
      -a always,exit -F arch=b64 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod

  # Sysctl hardening
  - path: /etc/sysctl.d/99-hardening.conf
    content: |
      # IP forwarding
      net.ipv4.ip_forward = 0
      net.ipv6.conf.all.forwarding = 0
      
      # Send redirects
      net.ipv4.conf.all.send_redirects = 0
      net.ipv4.conf.default.send_redirects = 0
      
      # Source packet verification
      net.ipv4.conf.all.rp_filter = 1
      net.ipv4.conf.default.rp_filter = 1
      
      # Accept redirects
      net.ipv4.conf.all.accept_redirects = 0
      net.ipv6.conf.all.accept_redirects = 0
      
      # Secure redirects
      net.ipv4.conf.all.secure_redirects = 0
      
      # Packet forwarding
      net.ipv4.conf.all.accept_source_route = 0
      net.ipv6.conf.all.accept_source_route = 0
      
      # Log Martians
      net.ipv4.conf.all.log_martians = 1
      net.ipv4.conf.default.log_martians = 1
      
      # Ignore ICMP redirects
      net.ipv4.conf.all.accept_redirects = 0
      net.ipv6.conf.all.accept_redirects = 0
      
      # Ignore send redirects
      net.ipv4.conf.all.send_redirects = 0
      
      # Disable source packet routing
      net.ipv4.conf.all.accept_source_route = 0
      net.ipv6.conf.all.accept_source_route = 0
      
      # SYN flood protection
      net.ipv4.tcp_syncookies = 1
      net.ipv4.tcp_max_syn_backlog = 2048
      net.ipv4.tcp_synack_retries = 2
      net.ipv4.tcp_syn_retries = 5
      
      # Log Martians
      net.ipv4.conf.all.log_martians = 1
      net.ipv4.icmp_ignore_bogus_error_responses = 1
      
      # Ignore ICMP ping requests
      net.ipv4.icmp_echo_ignore_broadcasts = 1

packages:
  - auditd
  - aide
  - rkhunter
  - fail2ban

runcmd:
  # Configure fail2ban
  - |
    cat > /etc/fail2ban/jail.local <<EOF
    [DEFAULT]
    bantime = 3600
    findtime = 600
    maxretry = 5
    
    [sshd]
    enabled = true
    port = ssh
    logpath = %(sshd_log)s
    backend = %(sshd_backend)s
    EOF
  
  # Initialize AIDE
  - aideinit
  - mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
  
  # Start security services
  - systemctl enable --now auditd
  - systemctl enable --now fail2ban
  
  # Set secure permissions
  - chmod 644 /etc/passwd
  - chmod 600 /etc/shadow
  - chmod 644 /etc/group
  - chmod 600 /etc/gshadow
  
  # Remove unnecessary packages
  - apt-get remove -y telnet rsh-client rsh-redone-client
```

## Performance Optimization

### 1. Parallel Execution

```yaml
#cloud-config
# Optimize boot time with parallel execution

write_files:
  - path: /usr/local/bin/parallel-setup.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      
      # Function to run tasks in parallel
      run_parallel() {
        local pids=()
        
        # Task 1: Install packages
        (
          echo "Starting package installation..."
          apt-get update && apt-get install -y nginx nodejs npm
          echo "Package installation completed"
        ) &
        pids+=($!)
        
        # Task 2: Configure network
        (
          echo "Starting network configuration..."
          # Network setup commands
          echo "Network configuration completed"
        ) &
        pids+=($!)
        
        # Task 3: Download application
        (
          echo "Starting application download..."
          curl -L "${APP_URL}" | tar xz -C /opt/app
          echo "Application download completed"
        ) &
        pids+=($!)
        
        # Wait for all tasks
        for pid in ${pids[@]}; do
          wait $pid
        done
      }
      
      run_parallel

# Use bootcmd for early execution
bootcmd:
  # Start background downloads early
  - curl -L "${APP_URL}" -o /tmp/app.tar.gz &

# Defer file writes until variables are available
write_files:
  - path: /etc/app/config.json
    defer: true
    content: |
      {
        "instance_id": "$INSTANCE_ID",
        "region": "$REGION"
      }
```

### 2. Caching Strategies

```yaml
#cloud-config
# Implement caching for faster rebuilds

write_files:
  - path: /usr/local/bin/cached-install.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      
      CACHE_DIR="/var/cache/cloud-init-cache"
      mkdir -p "$CACHE_DIR"
      
      # Check if package is cached
      install_with_cache() {
        local url=$1
        local name=$2
        local cache_file="$CACHE_DIR/$name"
        
        if [ -f "$cache_file" ]; then
          echo "Using cached $name"
          cp "$cache_file" /tmp/
        else
          echo "Downloading $name"
          curl -L "$url" -o "$cache_file"
          cp "$cache_file" /tmp/
        fi
      }
      
      # Cache APT packages
      if [ -f "$CACHE_DIR/apt-cache.tar.gz" ]; then
        tar -xzf "$CACHE_DIR/apt-cache.tar.gz" -C /var/cache/apt/
      fi
      
      apt-get update
      apt-get install -y --download-only nginx nodejs npm
      
      # Save APT cache
      tar -czf "$CACHE_DIR/apt-cache.tar.gz" /var/cache/apt/archives/*.deb

# Mount cache volume if available
bootcmd:
  - |
    if [ -e /dev/xvdh ]; then
      mount /dev/xvdh /var/cache/cloud-init-cache || true
    fi
```

## Monitoring and Debugging

### 1. Cloud-init Status and Logs

```yaml
#cloud-config
# Enhanced logging and monitoring

write_files:
  - path: /usr/local/bin/cloud-init-monitor.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      
      # Monitor cloud-init progress
      monitor_cloud_init() {
        local log_file="/var/log/cloud-init-monitor.log"
        
        # Check cloud-init status
        while true; do
          status=$(cloud-init status)
          echo "[$(date)] Cloud-init status: $status" >> "$log_file"
          
          if [[ $status == *"done"* ]]; then
            echo "[$(date)] Cloud-init completed successfully" >> "$log_file"
            break
          elif [[ $status == *"error"* ]]; then
            echo "[$(date)] Cloud-init failed!" >> "$log_file"
            # Collect debug information
            cloud-init collect-logs
            # Send alert
            curl -X POST https://alerts.example.com/webhook \
              -d "Cloud-init failed on $(hostname)"
            break
          fi
          
          sleep 10
        done
      }
      
      # Collect performance metrics
      collect_metrics() {
        local start_time=$(date +%s)
        local metrics_file="/var/log/cloud-init-metrics.json"
        
        # Wait for cloud-init to complete
        cloud-init status --wait
        
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        # Gather metrics
        cat > "$metrics_file" <<EOF
      {
        "hostname": "$(hostname)",
        "instance_id": "$(ec2-metadata --instance-id | cut -d' ' -f2)",
        "duration_seconds": $duration,
        "stages": $(cloud-init analyze show -i /var/log/cloud-init.log --format json),
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
      }
      EOF
        
        # Send metrics to monitoring system
        curl -X POST https://metrics.example.com/api/cloud-init \
          -H "Content-Type: application/json" \
          -d @"$metrics_file"
      }

runcmd:
  # Start monitoring in background
  - /usr/local/bin/cloud-init-monitor.sh &
  
  # Enable cloud-init debugging
  - |
    cat >> /etc/cloud/cloud.cfg.d/05_logging.cfg <<EOF
    # Increase logging verbosity
    log_cfgs:
      - [ *log_base, *log_syslog ]
    
    # Debug level
    debug:
      verbose: true
    EOF

# Phone home when complete
phone_home:
  url: https://deployment.example.com/api/cloud-init/complete
  post: ["instance_id", "hostname", "pub_key_rsa"]
  tries: 5
```

### 2. Health Checks

```yaml
#cloud-config
# Comprehensive health checking

write_files:
  - path: /usr/local/bin/health-check.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      
      HEALTH_FILE="/var/run/instance-health"
      
      # Check system resources
      check_system() {
        local status="ok"
        local messages=()
        
        # Check disk space
        if [ $(df -h / | awk 'NR==2 {print $(NF-1)}' | sed 's/%//') -gt 90 ]; then
          status="warning"
          messages+=("Disk space low")
        fi
        
        # Check memory
        if [ $(free | awk '/^Mem:/ {print int($3/$2 * 100)}') -gt 90 ]; then
          status="warning"
          messages+=("Memory usage high")
        fi
        
        # Check load average
        if [ $(uptime | awk -F'load average:' '{print int($2)}') -gt $(nproc) ]; then
          status="warning"
          messages+=("Load average high")
        fi
        
        echo "$status:system:${messages[*]}"
      }
      
      # Check services
      check_services() {
        local status="ok"
        local failed_services=()
        
        for service in nginx webapp node_exporter; do
          if ! systemctl is-active --quiet $service; then
            status="critical"
            failed_services+=($service)
          fi
        done
        
        echo "$status:services:${failed_services[*]}"
      }
      
      # Check application
      check_application() {
        local status="ok"
        
        if ! curl -sf http://localhost/health > /dev/null; then
          status="critical"
          echo "$status:application:Health endpoint failed"
        else
          echo "$status:application:Healthy"
        fi
      }
      
      # Main health check
      {
        echo "timestamp:$(date -u +%Y-%m-%dT%H:%M:%SZ)"
        check_system
        check_services
        check_application
      } > "$HEALTH_FILE"

# Setup health check cron
runcmd:
  - echo "*/5 * * * * root /usr/local/bin/health-check.sh" > /etc/cron.d/health-check
  - chmod 644 /etc/cron.d/health-check
```

## Security Considerations

### 1. Secure User Data Handling

```yaml
#cloud-config
# Secure handling of sensitive data

write_files:
  # Script to fetch and decrypt user data
  - path: /usr/local/bin/secure-userdata.sh
    permissions: '0700'
    owner: root:root
    content: |
      #!/bin/bash
      
      # Fetch encrypted user data
      ENCRYPTED_DATA=$(curl -s http://169.254.169.254/latest/user-data)
      
      # Decrypt using KMS
      DECRYPTED_DATA=$(echo "$ENCRYPTED_DATA" | base64 -d | \
        aws kms decrypt --region ${AWS_REGION} \
        --ciphertext-blob fileb:///dev/stdin \
        --query Plaintext --output text | base64 -d)
      
      # Process decrypted data
      echo "$DECRYPTED_DATA" | cloud-init --file -

# Clear sensitive data after use
runcmd:
  - shred -u /var/lib/cloud/instance/user-data.txt
  - shred -u /var/lib/cloud/instance/user-data.txt.i
  - history -c
```

### 2. Network Security

```yaml
#cloud-config
# Network security configuration

write_files:
  - path: /usr/local/bin/configure-firewall.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      
      # Default policies
      iptables -P INPUT DROP
      iptables -P FORWARD DROP
      iptables -P OUTPUT ACCEPT
      
      # Allow loopback
      iptables -A INPUT -i lo -j ACCEPT
      iptables -A OUTPUT -o lo -j ACCEPT
      
      # Allow established connections
      iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
      
      # Allow SSH from specific IPs
      for ip in ${ADMIN_IPS}; do
        iptables -A INPUT -p tcp -s $ip --dport 22 -j ACCEPT
      done
      
      # Allow HTTP/HTTPS
      iptables -A INPUT -p tcp --dport 80 -j ACCEPT
      iptables -A INPUT -p tcp --dport 443 -j ACCEPT
      
      # Rate limiting
      iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m limit --limit 3/min -j ACCEPT
      
      # Save rules
      iptables-save > /etc/iptables/rules.v4
      ip6tables-save > /etc/iptables/rules.v6

packages:
  - iptables-persistent

runcmd:
  - /usr/local/bin/configure-firewall.sh
```

## Troubleshooting

### Common Issues and Solutions

1. **User Data Not Executing**
```yaml
#cloud-config
# Debug user data execution

write_files:
  - path: /var/log/cloud-init-debug.log
    content: |
      Cloud-init debug started at $(date)

runcmd:
  # Enable debug output
  - sed -i 's/^GRUB_CMDLINE_LINUX=.*/GRUB_CMDLINE_LINUX="console=tty0 console=ttyS0,115200n8 cloud-init=debug"/' /etc/default/grub
  - update-grub
  
  # Check cloud-init status
  - cloud-init status --long
  
  # Analyze boot performance
  - cloud-init analyze show
  - cloud-init analyze blame
```

2. **Network Configuration Issues**
```yaml
#cloud-config
# Network troubleshooting

runcmd:
  # Wait for network
  - |
    for i in {1..30}; do
      if ping -c1 google.com &>/dev/null; then
        echo "Network is up"
        break
      fi
      echo "Waiting for network... ($i/30)"
      sleep 2
    done
  
  # Debug network configuration
  - ip addr show >> /var/log/network-debug.log
  - ip route show >> /var/log/network-debug.log
  - cat /etc/resolv.conf >> /var/log/network-debug.log
```

3. **Package Installation Failures**
```yaml
#cloud-config
# Robust package installation

runcmd:
  # Fix potential dpkg issues
  - dpkg --configure -a
  
  # Update with retries
  - |
    for i in {1..5}; do
      if apt-get update; then
        break
      fi
      echo "apt-get update failed, retry $i/5"
      sleep 10
    done
  
  # Install with error handling
  - |
    PACKAGES="nginx nodejs npm"
    for package in $PACKAGES; do
      if ! apt-get install -y $package; then
        echo "Failed to install $package" >> /var/log/cloud-init-errors.log
        # Try alternative sources
        apt-get install -y -t $(lsb_release -cs)-backports $package || true
      fi
    done
```

## Integration Examples

### Terraform Integration

```hcl
# Terraform template for cloud-init

data "template_file" "cloud_init" {
  template = file("${path.module}/cloud-init.yaml")
  
  vars = {
    hostname        = var.instance_name
    domain_name     = var.domain_name
    environment     = var.environment
    app_version     = var.app_version
    database_url    = data.aws_ssm_parameter.db_url.value
    admin_ssh_keys  = join("\n", var.admin_ssh_keys)
  }
}

data "template_cloudinit_config" "config" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    content      = data.template_file.cloud_init.rendered
  }

  part {
    content_type = "text/x-shellscript"
    content      = file("${path.module}/scripts/setup.sh")
  }
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name              = var.key_name
  vpc_security_group_ids = [aws_security_group.web.id]
  
  user_data = data.template_cloudinit_config.config.rendered
  
  root_block_device {
    volume_type = "gp3"
    volume_size = 30
    encrypted   = true
  }
  
  tags = {
    Name        = var.instance_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

### Packer Integration

```json
{
  "builders": [{
    "type": "amazon-ebs",
    "region": "us-east-1",
    "source_ami": "ami-0c02fb55956c7d316",
    "instance_type": "t3.medium",
    "ssh_username": "ubuntu",
    "ami_name": "webapp-{{timestamp}}",
    "user_data_file": "./cloud-init.yaml"
  }],
  
  "provisioners": [{
    "type": "shell",
    "inline": [
      "cloud-init status --wait",
      "sudo cloud-init clean"
    ]
  }]
}
```

## Conclusion

Cloud-init provides a powerful, standardized way to initialize cloud instances across different platforms. Its declarative approach, combined with extensive module support, enables teams to bootstrap instances consistently and reliably. By following these patterns and best practices, organizations can leverage cloud-init to create maintainable, secure, and efficient cloud infrastructure initialization processes.