# Let's Encrypt

Let's Encrypt is a free, automated, and open certificate authority (CA) that provides free TLS/SSL certificates to enable HTTPS across the web. It's essential for platform engineers to secure applications, APIs, and infrastructure components with automated certificate management.

## Overview

Let's Encrypt is widely used in platform engineering for:
- Securing web applications and APIs with HTTPS
- Automated certificate provisioning and renewal
- Kubernetes ingress controller SSL termination
- Load balancer SSL certificate management
- Infrastructure component security (databases, monitoring tools)

## Key Features

- **Free Certificates**: No cost for SSL/TLS certificates
- **Automated**: ACME protocol for automatic issuance and renewal
- **Domain Validated**: Automatic domain ownership verification
- **Short-lived**: 90-day certificate validity for enhanced security
- **Rate Limits**: Reasonable limits to prevent abuse
- **Cross-Platform**: Works with all major web servers and platforms

## Certificate Types and Validation

### Domain Validation Methods
```bash
# HTTP-01 Challenge
# - Validates domain ownership via HTTP
# - Works for single domains
# - Requires port 80 access

# DNS-01 Challenge  
# - Validates via DNS TXT record
# - Supports wildcard certificates
# - Works behind firewalls

# TLS-ALPN-01 Challenge
# - Validates via TLS handshake
# - Requires port 443 access
# - Good for load balancers
```

### Certificate Types
```bash
# Single Domain Certificate
domain.example.com

# Multi-Domain (SAN) Certificate
domain1.example.com
domain2.example.com
api.example.com

# Wildcard Certificate
*.example.com
```

## Installation and Setup

### Certbot Installation
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx python3-certbot-apache

# CentOS/RHEL/Fedora
sudo yum install certbot python3-certbot-nginx python3-certbot-apache

# macOS (Homebrew)
brew install certbot

# Docker
docker run -it --rm --name certbot \
  -v "/etc/letsencrypt:/etc/letsencrypt" \
  -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
  certbot/certbot certonly
```

### ACME Client Alternatives
```bash
# acme.sh (Shell script, lightweight)
curl https://get.acme.sh | sh
source ~/.bashrc

# Caddy (Built-in automatic HTTPS)
caddy run --config Caddyfile

# cert-manager (Kubernetes native)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

## Basic Certificate Operations

### Manual Certificate Issuance
```bash
# HTTP-01 challenge (standalone)
sudo certbot certonly --standalone -d example.com -d www.example.com

# HTTP-01 challenge (webroot)
sudo certbot certonly --webroot -w /var/www/html -d example.com

# DNS-01 challenge (manual)
sudo certbot certonly --manual --preferred-challenges dns -d example.com -d *.example.com

# Using specific email
sudo certbot certonly --standalone -d example.com --email admin@example.com --agree-tos --non-interactive
```

### Web Server Integration
```bash
# Nginx automatic configuration
sudo certbot --nginx -d example.com -d www.example.com

# Apache automatic configuration
sudo certbot --apache -d example.com -d www.example.com

# Manual Nginx configuration
sudo certbot certonly --nginx -d example.com
# Then manually configure nginx.conf
```

### Certificate Renewal
```bash
# Test renewal (dry run)
sudo certbot renew --dry-run

# Force renewal
sudo certbot renew --force-renewal

# Renew specific certificate
sudo certbot renew --cert-name example.com

# Renew with hooks
sudo certbot renew --deploy-hook "systemctl reload nginx"
```

## Platform Engineering Use Cases

### Kubernetes with cert-manager
```yaml
# ClusterIssuer for Let's Encrypt
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
    - dns01:
        cloudflare:
          email: admin@example.com
          apiTokenSecretRef:
            name: cloudflare-api-token
            key: api-token

---
# Certificate resource
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-com-tls
  namespace: default
spec:
  secretName: example-com-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - example.com
  - www.example.com

---
# Ingress with automatic TLS
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - example.com
    - www.example.com
    secretName: example-com-tls
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

### Docker and Docker Compose
```yaml
# docker-compose.yml with automatic HTTPS
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl:ro
      - certbot-webroot:/var/www/certbot
    depends_on:
      - app

  certbot:
    image: certbot/certbot
    volumes:
      - ./ssl:/etc/letsencrypt
      - certbot-webroot:/var/www/certbot
    command: >-
      sh -c 'trap exit TERM; while :; do
        certbot renew --webroot --webroot-path=/var/www/certbot;
        sleep 12h & wait $${!};
      done'

  app:
    build: .
    expose:
      - "8080"
    environment:
      - NODE_ENV=production

volumes:
  certbot-webroot:
```

### Nginx Configuration
```nginx
# /etc/nginx/sites-available/example.com
server {
    listen 80;
    server_name example.com www.example.com;
    
    # ACME challenge location
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    # Redirect HTTP to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
    
    # SSL Security Headers
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    
    location / {
        proxy_pass http://app:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Automation Scripts
```bash
#!/bin/bash
# ssl-setup.sh - Automated SSL certificate setup

set -e

DOMAIN=$1
EMAIL=$2
WEBROOT=${3:-/var/www/html}

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "Usage: $0 <domain> <email> [webroot]"
    exit 1
fi

echo "Setting up SSL certificate for $DOMAIN"

# Check if certificate already exists
if [ -d "/etc/letsencrypt/live/$DOMAIN" ]; then
    echo "Certificate already exists for $DOMAIN"
    echo "Use --force-renewal to renew"
    exit 0
fi

# Install certbot if not present
if ! command -v certbot &> /dev/null; then
    echo "Installing certbot..."
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
fi

# Obtain certificate
echo "Obtaining certificate for $DOMAIN"
certbot certonly \
    --webroot \
    --webroot-path="$WEBROOT" \
    --email "$EMAIL" \
    --agree-tos \
    --non-interactive \
    --domains "$DOMAIN"

# Set up automatic renewal
if ! crontab -l | grep -q "certbot renew"; then
    echo "Setting up automatic renewal"
    (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet --deploy-hook 'systemctl reload nginx'") | crontab -
fi

echo "SSL certificate setup completed for $DOMAIN"
echo "Certificate location: /etc/letsencrypt/live/$DOMAIN/"
```

### Load Balancer Integration
```bash
#!/bin/bash
# lb-ssl-update.sh - Update load balancer with new certificates

DOMAIN=$1
LB_NAME=$2

if [ -z "$DOMAIN" ] || [ -z "$LB_NAME" ]; then
    echo "Usage: $0 <domain> <lb-name>"
    exit 1
fi

# AWS Application Load Balancer
aws elbv2 modify-listener \
    --listener-arn "$LISTENER_ARN" \
    --certificates CertificateArn="$CERT_ARN"

# Google Cloud Load Balancer
gcloud compute ssl-certificates create "$DOMAIN-cert" \
    --certificate="/etc/letsencrypt/live/$DOMAIN/fullchain.pem" \
    --private-key="/etc/letsencrypt/live/$DOMAIN/privkey.pem"

# HAProxy configuration update
cat > /etc/haproxy/ssl.pem << EOF
$(cat /etc/letsencrypt/live/$DOMAIN/fullchain.pem)
$(cat /etc/letsencrypt/live/$DOMAIN/privkey.pem)
EOF

systemctl reload haproxy
```

## DNS-01 Challenge with Cloud Providers

### Cloudflare DNS
```bash
# Install Cloudflare plugin
pip install certbot-dns-cloudflare

# Create credentials file
cat > /etc/letsencrypt/cloudflare.ini << EOF
dns_cloudflare_api_token = your-api-token
EOF
chmod 600 /etc/letsencrypt/cloudflare.ini

# Obtain wildcard certificate
certbot certonly \
    --dns-cloudflare \
    --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
    --dns-cloudflare-propagation-seconds 60 \
    -d example.com \
    -d *.example.com
```

### AWS Route53
```bash
# Install Route53 plugin
pip install certbot-dns-route53

# Configure AWS credentials (IAM role or credentials file)
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key

# Obtain certificate
certbot certonly \
    --dns-route53 \
    -d example.com \
    -d *.example.com
```

### Google Cloud DNS
```bash
# Install Google Cloud plugin
pip install certbot-dns-google

# Set up service account credentials
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Obtain certificate
certbot certonly \
    --dns-google \
    --dns-google-credentials /path/to/service-account.json \
    -d example.com \
    -d *.example.com
```

## Certificate Monitoring and Management

### Certificate Expiry Monitoring
```bash
#!/bin/bash
# cert-monitor.sh - Monitor certificate expiry

DOMAINS=("example.com" "api.example.com" "www.example.com")
DAYS_WARNING=30

for domain in "${DOMAINS[@]}"; do
    expiry_date=$(echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null | \
                  openssl x509 -noout -dates | grep notAfter | cut -d= -f2)
    
    expiry_epoch=$(date -d "$expiry_date" +%s)
    current_epoch=$(date +%s)
    days_until_expiry=$(( (expiry_epoch - current_epoch) / 86400 ))
    
    if [ $days_until_expiry -lt $DAYS_WARNING ]; then
        echo "WARNING: Certificate for $domain expires in $days_until_expiry days"
        # Send alert (email, Slack, etc.)
    else
        echo "OK: Certificate for $domain expires in $days_until_expiry days"
    fi
done
```

### Certificate Inventory
```bash
#!/bin/bash
# cert-inventory.sh - List all Let's Encrypt certificates

echo "Let's Encrypt Certificate Inventory"
echo "=================================="

for cert_dir in /etc/letsencrypt/live/*/; do
    if [ -d "$cert_dir" ]; then
        domain=$(basename "$cert_dir")
        cert_file="$cert_dir/cert.pem"
        
        if [ -f "$cert_file" ]; then
            echo "Domain: $domain"
            echo "Certificate: $cert_file"
            
            # Get certificate details
            openssl x509 -in "$cert_file" -noout -text | grep -E "(Subject:|Not After|DNS:)"
            echo "---"
        fi
    fi
done
```

### Automated Renewal with Monitoring
```bash
#!/bin/bash
# renew-with-monitoring.sh - Renew certificates with monitoring

LOG_FILE="/var/log/certbot-renewal.log"
WEBHOOK_URL="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"

{
    echo "=== Certbot Renewal Started at $(date) ==="
    
    # Test renewal first
    if certbot renew --dry-run; then
        echo "Dry run successful, proceeding with actual renewal"
        
        # Perform actual renewal
        if certbot renew --deploy-hook "systemctl reload nginx"; then
            echo "Certificate renewal successful"
            
            # Post success message to Slack
            curl -X POST -H 'Content-type: application/json' \
                --data '{"text":"✅ SSL certificates renewed successfully"}' \
                "$WEBHOOK_URL"
        else
            echo "Certificate renewal failed"
            
            # Post failure message to Slack
            curl -X POST -H 'Content-type: application/json' \
                --data '{"text":"❌ SSL certificate renewal failed"}' \
                "$WEBHOOK_URL"
        fi
    else
        echo "Dry run failed"
        
        # Post dry run failure to Slack
        curl -X POST -H 'Content-type: application/json' \
            --data '{"text":"⚠️ SSL certificate renewal dry run failed"}' \
            "$WEBHOOK_URL"
    fi
    
    echo "=== Certbot Renewal Completed at $(date) ==="
} >> "$LOG_FILE" 2>&1
```

## Best Practices

### Security Considerations
```bash
# File permissions
sudo chmod 600 /etc/letsencrypt/live/*/privkey.pem
sudo chown root:root /etc/letsencrypt/live/*/privkey.pem

# Rate limit management
# - 50 certificates per registered domain per week
# - 5 duplicate certificates per week
# - Use staging environment for testing

# Backup certificates
rsync -avz /etc/letsencrypt/ backup-server:/backup/letsencrypt/
```

### Automation Best Practices
```bash
# Use staging for testing
certbot certonly --staging --standalone -d test.example.com

# Implement proper logging
certbot renew --quiet --deploy-hook "logger 'SSL certificates renewed'"

# Use deployment hooks for service reloads
certbot renew --deploy-hook "/usr/local/bin/reload-services.sh"

# Monitor renewal success
certbot renew --post-hook "curl -fsS https://hc-ping.com/your-uuid"
```

### High Availability Setup
```bash
# Shared certificate storage (NFS/EFS)
mount -t nfs certificate-server:/etc/letsencrypt /etc/letsencrypt

# Certificate synchronization between servers
rsync -avz /etc/letsencrypt/ server2:/etc/letsencrypt/
rsync -avz /etc/letsencrypt/ server3:/etc/letsencrypt/

# Load balancer with shared certificates
# Use external certificate management (AWS ACM, GCP SSL)
```

## Troubleshooting

### Common Issues
```bash
# Debug certificate issuance
certbot --verbose certonly --standalone -d example.com

# Check certificate chain
openssl x509 -in /etc/letsencrypt/live/example.com/fullchain.pem -text -noout

# Validate certificate installation
ssl-checker example.com 443

# Test ACME challenge
curl -I http://example.com/.well-known/acme-challenge/test
```

### Rate Limiting
```bash
# Check rate limits
https://crt.sh/?q=example.com

# Use different validation methods
certbot certonly --dns-cloudflare  # Instead of HTTP-01

# Use staging environment for testing
certbot --staging certonly --standalone -d example.com
```

## Resources

- [Let's Encrypt Official Documentation](https://letsencrypt.org/docs/) - Complete Let's Encrypt documentation
- [Certbot User Guide](https://certbot.eff.org/instructions) - Official Certbot installation and usage guide
- [ACME Protocol RFC](https://tools.ietf.org/rfc/rfc8555.txt) - Automatic Certificate Management Environment specification
- [cert-manager Documentation](https://cert-manager.io/docs/) - Kubernetes certificate management
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/) - SSL configuration testing tool
- [Certificate Transparency Logs](https://crt.sh/) - Monitor certificate issuance
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/) - Secure SSL configuration templates
- [Let's Encrypt Community Forum](https://community.letsencrypt.org/) - Community support and discussions
- [ACME Client Implementations](https://letsencrypt.org/docs/client-options/) - Alternative ACME clients
- [Let's Encrypt Rate Limits](https://letsencrypt.org/docs/rate-limits/) - Rate limiting documentation