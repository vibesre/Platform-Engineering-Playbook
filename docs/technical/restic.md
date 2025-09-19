# Restic - Fast, Secure, Efficient Backup Program

Restic is a modern backup program that is fast, efficient, and secure. It provides cross-platform backups with deduplication, encryption, and verification capabilities for various storage backends.

## Architecture

```mermaid
graph TB
    A[Source Data] --> B[Restic Client]
    B --> C[Repository]
    C --> D[Local Storage]
    C --> E[Cloud Storage]
    C --> F[Remote Storage]
    
    G[Snapshot Metadata] --> C
    H[Data Chunks] --> C
    I[Index Files] --> C
    
    J[Encryption Layer] --> C
    K[Deduplication] --> C
    L[Compression] --> C
```

## Installation

### Binary Installation
```bash
# Download latest release
curl -LO https://github.com/restic/restic/releases/latest/download/restic_0.16.2_linux_amd64.bz2
bunzip2 restic_0.16.2_linux_amd64.bz2
chmod +x restic_0.16.2_linux_amd64
sudo mv restic_0.16.2_linux_amd64 /usr/local/bin/restic

# Verify installation
restic version
```

### Package Manager
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install restic

# CentOS/RHEL
sudo yum install restic

# macOS
brew install restic

# Docker
docker pull restic/restic
```

## Configuration

### Environment Variables
```bash
# Repository configuration
export RESTIC_REPOSITORY="/backup/repo"
export RESTIC_PASSWORD="your-secure-password"

# Cloud storage (S3)
export RESTIC_REPOSITORY="s3:s3.amazonaws.com/bucket-name"
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"

# Azure Blob Storage
export RESTIC_REPOSITORY="azure:container-name"
export AZURE_ACCOUNT_NAME="storage-account"
export AZURE_ACCOUNT_KEY="account-key"

# Google Cloud Storage
export RESTIC_REPOSITORY="gs:bucket-name:/path"
export GOOGLE_PROJECT_ID="project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

### Password File
```bash
# Create password file
echo "your-secure-password" > ~/.restic-password
chmod 600 ~/.restic-password

# Use password file
export RESTIC_PASSWORD_FILE="~/.restic-password"
```

## Basic Operations

### Initialize Repository
```bash
# Local repository
restic init --repo /backup/repo

# S3 repository
restic init --repo s3:s3.amazonaws.com/my-backup-bucket

# With password file
restic init --repo /backup/repo --password-file ~/.restic-password
```

### Create Backup
```bash
# Backup single directory
restic backup /home/user/documents --repo /backup/repo

# Backup multiple paths
restic backup /home /etc /var/log --repo /backup/repo

# Backup with tags
restic backup /home/user --tag daily,home --repo /backup/repo

# Exclude patterns
restic backup /home/user \
  --exclude "*.tmp" \
  --exclude "/home/user/.cache" \
  --exclude-file ~/.restic-exclude \
  --repo /backup/repo
```

### List Snapshots
```bash
# List all snapshots
restic snapshots --repo /backup/repo

# List snapshots with specific tag
restic snapshots --tag daily --repo /backup/repo

# List snapshots for specific host
restic snapshots --host myserver --repo /backup/repo
```

### Restore Data
```bash
# Restore latest snapshot
restic restore latest --target /restore/path --repo /backup/repo

# Restore specific snapshot
restic restore 1a2b3c4d --target /restore/path --repo /backup/repo

# Restore specific files
restic restore latest --target /restore/path \
  --include "/home/user/documents" \
  --repo /backup/repo

# Restore to original location
restic restore latest --target / --repo /backup/repo
```

## Advanced Usage

### Exclude Patterns File
```bash
# ~/.restic-exclude
*.log
*.tmp
*.cache
node_modules/
.git/
__pycache__/
*.pyc
.DS_Store
Thumbs.db
```

### Backup Script
```bash
#!/bin/bash
# backup-script.sh

set -e

# Configuration
REPO="/backup/repo"
PASSWORD_FILE="~/.restic-password"
SOURCE_DIRS="/home /etc /var/log"
TAG="$(date +%Y-%m-%d)"

# Pre-backup hook
echo "Starting backup at $(date)"

# Create backup
restic backup $SOURCE_DIRS \
  --repo "$REPO" \
  --password-file "$PASSWORD_FILE" \
  --tag "$TAG" \
  --exclude-file ~/.restic-exclude \
  --one-file-system \
  --verbose

# Verify backup
restic check --repo "$REPO" --password-file "$PASSWORD_FILE"

# Cleanup old snapshots
restic forget \
  --repo "$REPO" \
  --password-file "$PASSWORD_FILE" \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 12 \
  --keep-yearly 3 \
  --prune

echo "Backup completed at $(date)"
```

### Systemd Service
```ini
# /etc/systemd/system/restic-backup.service
[Unit]
Description=Restic Backup
After=network.target

[Service]
Type=oneshot
User=backup
Group=backup
ExecStart=/usr/local/bin/backup-script.sh
Environment=RESTIC_REPOSITORY=/backup/repo
Environment=RESTIC_PASSWORD_FILE=/home/backup/.restic-password
```

```ini
# /etc/systemd/system/restic-backup.timer
[Unit]
Description=Run Restic Backup Daily
Requires=restic-backup.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

### Docker Backup
```dockerfile
# Dockerfile.restic
FROM restic/restic:latest

RUN apk add --no-cache curl

COPY backup-script.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/backup-script.sh

ENTRYPOINT ["/usr/local/bin/backup-script.sh"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  restic-backup:
    build:
      context: .
      dockerfile: Dockerfile.restic
    volumes:
      - /home:/backup/home:ro
      - /etc:/backup/etc:ro
      - backup-repo:/backup/repo
    environment:
      - RESTIC_REPOSITORY=/backup/repo
      - RESTIC_PASSWORD_FILE=/backup/.restic-password
    secrets:
      - restic-password

volumes:
  backup-repo:

secrets:
  restic-password:
    file: ./restic-password.txt
```

## Cloud Storage Integration

### AWS S3 Configuration
```bash
# Environment setup
export RESTIC_REPOSITORY="s3:https://s3.amazonaws.com/my-backup-bucket"
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_DEFAULT_REGION="us-east-1"

# Initialize and backup
restic init
restic backup /home/user --tag s3-backup
```

### Google Cloud Storage
```bash
# Service account setup
export GOOGLE_PROJECT_ID="my-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
export RESTIC_REPOSITORY="gs:my-backup-bucket:/backups"

# Initialize and backup
restic init
restic backup /home/user --tag gcs-backup
```

### Azure Blob Storage
```bash
# Azure configuration
export AZURE_ACCOUNT_NAME="mystorageaccount"
export AZURE_ACCOUNT_KEY="account-key"
export RESTIC_REPOSITORY="azure:backup-container:/backups"

# Initialize and backup
restic init
restic backup /home/user --tag azure-backup
```

## Monitoring and Maintenance

### Check Repository
```bash
# Basic check
restic check --repo /backup/repo

# Read all data
restic check --read-data --repo /backup/repo

# Check specific percentage
restic check --read-data-subset=10% --repo /backup/repo
```

### Repository Statistics
```bash
# Repository stats
restic stats --repo /backup/repo

# Stats by host
restic stats --host myserver --repo /backup/repo

# Stats by tag
restic stats --tag daily --repo /backup/repo
```

### Cleanup Operations
```bash
# Remove old snapshots
restic forget --keep-daily 7 --keep-weekly 4 --repo /backup/repo

# Prune unused data
restic prune --repo /backup/repo

# Combined forget and prune
restic forget --prune --keep-daily 7 --keep-weekly 4 --repo /backup/repo
```

## Python Integration

### Backup Automation
```python
#!/usr/bin/env python3
import subprocess
import os
import logging
from datetime import datetime

class ResticBackup:
    def __init__(self, repo, password_file, source_dirs):
        self.repo = repo
        self.password_file = password_file
        self.source_dirs = source_dirs
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def backup(self, tags=None, exclude_file=None):
        """Create a backup"""
        cmd = [
            'restic', 'backup',
            '--repo', self.repo,
            '--password-file', self.password_file,
            '--one-file-system',
            '--verbose'
        ]
        
        if tags:
            for tag in tags:
                cmd.extend(['--tag', tag])
        
        if exclude_file:
            cmd.extend(['--exclude-file', exclude_file])
        
        cmd.extend(self.source_dirs)
        
        try:
            self.logger.info("Starting backup...")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.logger.info("Backup completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Backup failed: {e.stderr}")
            return False
    
    def list_snapshots(self, tag=None, host=None):
        """List snapshots"""
        cmd = [
            'restic', 'snapshots',
            '--repo', self.repo,
            '--password-file', self.password_file,
            '--json'
        ]
        
        if tag:
            cmd.extend(['--tag', tag])
        if host:
            cmd.extend(['--host', host])
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            import json
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to list snapshots: {e.stderr}")
            return []
    
    def cleanup(self, keep_daily=7, keep_weekly=4, keep_monthly=12):
        """Clean up old snapshots"""
        cmd = [
            'restic', 'forget',
            '--repo', self.repo,
            '--password-file', self.password_file,
            '--keep-daily', str(keep_daily),
            '--keep-weekly', str(keep_weekly),
            '--keep-monthly', str(keep_monthly),
            '--prune'
        ]
        
        try:
            self.logger.info("Starting cleanup...")
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.logger.info("Cleanup completed")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Cleanup failed: {e.stderr}")
            return False

# Usage example
if __name__ == "__main__":
    backup = ResticBackup(
        repo="/backup/repo",
        password_file="/home/backup/.restic-password",
        source_dirs=["/home", "/etc"]
    )
    
    # Create backup
    today = datetime.now().strftime("%Y-%m-%d")
    success = backup.backup(
        tags=[today, "automated"],
        exclude_file="/home/backup/.restic-exclude"
    )
    
    if success:
        # List recent snapshots
        snapshots = backup.list_snapshots(tag="automated")
        print(f"Total snapshots: {len(snapshots)}")
        
        # Cleanup old snapshots
        backup.cleanup()
```

### Health Monitoring
```python
#!/usr/bin/env python3
import subprocess
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

class ResticMonitor:
    def __init__(self, repo, password_file):
        self.repo = repo
        self.password_file = password_file
    
    def check_recent_backup(self, hours=25):
        """Check if backup was created within specified hours"""
        try:
            cmd = [
                'restic', 'snapshots',
                '--repo', self.repo,
                '--password-file', self.password_file,
                '--json'
            ]
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            snapshots = json.loads(result.stdout)
            
            if not snapshots:
                return False, "No snapshots found"
            
            latest = snapshots[-1]
            snapshot_time = datetime.fromisoformat(latest['time'].replace('Z', '+00:00'))
            cutoff_time = datetime.now().replace(tzinfo=snapshot_time.tzinfo) - timedelta(hours=hours)
            
            if snapshot_time > cutoff_time:
                return True, f"Latest backup: {snapshot_time}"
            else:
                return False, f"Latest backup too old: {snapshot_time}"
                
        except Exception as e:
            return False, f"Error checking backups: {str(e)}"
    
    def check_repository_health(self):
        """Check repository integrity"""
        try:
            cmd = [
                'restic', 'check',
                '--repo', self.repo,
                '--password-file', self.password_file
            ]
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return True, "Repository check passed"
            
        except subprocess.CalledProcessError as e:
            return False, f"Repository check failed: {e.stderr}"
    
    def send_alert(self, message, smtp_server, sender, recipients):
        """Send email alert"""
        msg = MIMEText(message)
        msg['Subject'] = 'Restic Backup Alert'
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        
        try:
            with smtplib.SMTP(smtp_server) as server:
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send alert: {e}")
            return False

# Usage
monitor = ResticMonitor("/backup/repo", "/home/backup/.restic-password")

# Check recent backup
backup_ok, backup_msg = monitor.check_recent_backup(25)
if not backup_ok:
    print(f"ALERT: {backup_msg}")

# Check repository health
health_ok, health_msg = monitor.check_repository_health()
if not health_ok:
    print(f"ALERT: {health_msg}")
```

## Best Practices

### Security
- Use strong, unique passwords for repositories
- Store password files with restricted permissions (600)
- Enable encryption for all repositories
- Regularly test restore procedures
- Use separate credentials for backup storage

### Performance
- Use `--one-file-system` to avoid crossing mount points
- Configure appropriate exclude patterns
- Use local cache for better performance
- Consider bandwidth limitations for cloud storage
- Monitor repository size and growth

### Reliability
- Test backups regularly with restore operations
- Monitor backup completion and repository health
- Implement alerting for failed backups
- Keep multiple copies in different locations
- Document recovery procedures

### Retention Policies
```bash
# Conservative retention
restic forget --keep-daily 30 --keep-weekly 12 --keep-monthly 24 --keep-yearly 5

# Aggressive retention
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --keep-yearly 2

# Custom retention by tag
restic forget --tag critical --keep-daily 14 --keep-weekly 8 --keep-monthly 12
```

## Troubleshooting

### Common Issues

**Repository Lock**
```bash
# Remove stale locks
restic unlock --repo /backup/repo

# Force unlock (use with caution)
restic unlock --remove-all --repo /backup/repo
```

**Corrupted Repository**
```bash
# Check and repair
restic check --read-data --repo /backup/repo
restic rebuild-index --repo /backup/repo
```

**Performance Issues**
```bash
# Use local cache
export RESTIC_CACHE_DIR="/tmp/restic-cache"

# Limit bandwidth
restic backup /home --limit-upload 1000 --limit-download 1000

# Parallel processing
restic backup /home --read-concurrency 4
```

### Debugging
```bash
# Verbose output
restic backup /home --verbose --repo /backup/repo

# Debug output
restic backup /home --verbose=2 --repo /backup/repo

# Profile memory usage
restic backup /home --option pack.size=16 --repo /backup/repo
```

## Integration Examples

### GitLab CI/CD
```yaml
# .gitlab-ci.yml
backup:
  stage: backup
  image: restic/restic:latest
  variables:
    RESTIC_REPOSITORY: "s3:$S3_ENDPOINT/$S3_BUCKET"
    RESTIC_PASSWORD: "$RESTIC_PASSWORD"
  script:
    - restic snapshots || restic init
    - restic backup /builds/$CI_PROJECT_PATH
    - restic forget --prune --keep-daily 7
  only:
    - main
```

### Kubernetes CronJob
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: restic-backup
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: restic
            image: restic/restic:latest
            command:
            - /bin/sh
            - -c
            - |
              restic backup /data --tag k8s-backup
              restic forget --prune --keep-daily 7
            env:
            - name: RESTIC_REPOSITORY
              value: "s3:s3.amazonaws.com/backup-bucket"
            - name: RESTIC_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: restic-secret
                  key: password
            volumeMounts:
            - name: data
              mountPath: /data
              readOnly: true
          volumes:
          - name: data
            persistentVolumeClaim:
              claimName: app-data
          restartPolicy: OnFailure
```

## Resources

- [Official Documentation](https://restic.readthedocs.io/)
- [GitHub Repository](https://github.com/restic/restic)
- [Community Forum](https://forum.restic.net/)
- [REST API Documentation](https://restic.readthedocs.io/en/latest/100_references.html#rest-server)
- [Performance Tuning Guide](https://restic.readthedocs.io/en/latest/047_tuning_backup_parameters.html)