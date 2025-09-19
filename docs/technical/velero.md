# Velero

## Overview

Velero is an open-source tool for safely backing up and restoring Kubernetes clusters, performing disaster recovery, and migrating cluster resources to other clusters. It's essential for Kubernetes backup and disaster recovery strategies.

## Key Features

- **Cluster Backup**: Complete cluster state backup including resources and volumes
- **Disaster Recovery**: Restore clusters to previous states
- **Resource Migration**: Move resources between clusters
- **Volume Snapshots**: Backup persistent volumes
- **Scheduled Backups**: Automated backup schedules

## Installation and Setup

### Install Velero CLI
```bash
# Download and install Velero CLI
curl -fsSL -o velero-v1.12.0-linux-amd64.tar.gz \
  https://github.com/vmware-tanzu/velero/releases/download/v1.12.0/velero-v1.12.0-linux-amd64.tar.gz
tar -xzf velero-v1.12.0-linux-amd64.tar.gz
sudo mv velero-v1.12.0-linux-amd64/velero /usr/local/bin/

# Verify installation
velero version --client-only
```

### AWS S3 Backend Setup
```bash
# Create S3 bucket
aws s3 mb s3://velero-backups-example

# Create IAM policy
cat > velero-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVolumes",
                "ec2:DescribeSnapshots",
                "ec2:CreateTags",
                "ec2:CreateVolume",
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:PutObject",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts"
            ],
            "Resource": [
                "arn:aws:s3:::velero-backups-example/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::velero-backups-example"
            ]
        }
    ]
}
EOF

# Create IAM user and attach policy
aws iam create-user --user-name velero
aws iam put-user-policy --user-name velero --policy-name VeleroAccessPolicy --policy-document file://velero-policy.json
aws iam create-access-key --user-name velero
```

### Install Velero in Cluster
```bash
# Create credentials file
cat > credentials-velero <<EOF
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
EOF

# Install Velero
velero install \
    --provider aws \
    --plugins velero/velero-plugin-for-aws:v1.8.0 \
    --bucket velero-backups-example \
    --backup-location-config region=us-west-2 \
    --snapshot-location-config region=us-west-2 \
    --secret-file ./credentials-velero
```

## Basic Operations

### Create Backups
```bash
# Backup entire cluster
velero backup create my-backup

# Backup specific namespace
velero backup create namespace-backup --include-namespaces production

# Backup with labels
velero backup create app-backup --selector app=my-app

# Backup excluding resources
velero backup create backup-no-logs --exclude-resources events,logs

# Check backup status
velero backup describe my-backup
velero backup logs my-backup
```

### Restore Operations
```bash
# Restore from backup
velero restore create --from-backup my-backup

# Restore to different namespace
velero restore create --from-backup my-backup \
  --namespace-mappings old-namespace:new-namespace

# Restore with resource mapping
velero restore create --from-backup my-backup \
  --restore-volumes=true \
  --wait

# Check restore status
velero restore describe restore-20231201-120000
velero restore logs restore-20231201-120000
```

### Scheduled Backups
```bash
# Create daily backup schedule
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --ttl 720h

# Create weekly full backup
velero schedule create weekly-full \
  --schedule="0 1 * * 0" \
  --ttl 2160h

# List schedules
velero schedule get

# Pause/unpause schedule
velero schedule pause daily-backup
velero schedule unpause daily-backup
```

## Advanced Configuration

### Custom Resource Definitions
```yaml
# backup-schedule.yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: production-backup
  namespace: velero
spec:
  schedule: "0 3 * * *"  # 3 AM daily
  template:
    includedNamespaces:
    - production
    - monitoring
    excludedResources:
    - events
    - logs
    storageLocation: default
    volumeSnapshotLocations:
    - default
    ttl: 168h  # 7 days
    hooks:
      resources:
      - name: postgres-backup
        includedNamespaces:
        - production
        labelSelector:
          matchLabels:
            app: postgres
        hooks:
        - exec:
            container: postgres
            command:
            - /bin/bash
            - -c
            - "pg_dump mydb > /tmp/backup.sql"
            onError: Continue
```

### Backup Hooks
```yaml
# pre-backup-hook.yaml
apiVersion: v1
kind: Pod
metadata:
  name: database-backup
  namespace: production
  annotations:
    pre.hook.backup.velero.io/command: '["/bin/bash", "-c", "pg_dump mydb > /backup/dump.sql"]'
    pre.hook.backup.velero.io/timeout: 5m
spec:
  containers:
  - name: postgres
    image: postgres:13
    volumeMounts:
    - name: backup-volume
      mountPath: /backup
  volumes:
  - name: backup-volume
    persistentVolumeClaim:
      claimName: backup-pvc
```

### Volume Snapshot Configuration
```yaml
# volume-snapshot-location.yaml
apiVersion: velero.io/v1
kind: VolumeSnapshotLocation
metadata:
  name: aws-snapshots
  namespace: velero
spec:
  provider: aws
  config:
    region: us-west-2
    profile: default
```

## Disaster Recovery Scenarios

### Cluster Migration
```bash
# Source cluster backup
velero backup create migration-backup \
  --include-cluster-resources=true \
  --wait

# Target cluster restore
velero restore create migration-restore \
  --from-backup migration-backup \
  --restore-volumes=true \
  --wait
```

### Namespace Recovery
```bash
# Delete corrupted namespace
kubectl delete namespace production

# Restore namespace from backup
velero restore create namespace-recovery \
  --from-backup latest-backup \
  --include-namespaces production \
  --wait
```

### Selective Resource Recovery
```bash
# Restore only ConfigMaps and Secrets
velero restore create config-restore \
  --from-backup my-backup \
  --include-resources configmaps,secrets \
  --include-namespaces production
```

## Monitoring and Maintenance

### Backup Monitoring
```bash
# List all backups
velero backup get

# Check backup details
velero backup describe my-backup --details

# View backup logs
velero backup logs my-backup

# Delete old backups
velero backup delete old-backup
```

### Cleanup Operations
```bash
# Delete backups older than 30 days
velero backup get --selector 'velero.io/created-date<2023-11-01'

# Cleanup failed backups
for backup in $(velero backup get -o name | grep Failed); do
  velero backup delete $backup
done
```

### Health Checks
```yaml
# monitoring-dashboard.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: velero-monitoring
data:
  alerts.yaml: |
    groups:
    - name: velero
      rules:
      - alert: VeleroBackupFailure
        expr: increase(velero_backup_failure_total[1h]) > 0
        labels:
          severity: critical
        annotations:
          summary: "Velero backup failure detected"
      
      - alert: VeleroScheduleMissed
        expr: time() - velero_backup_last_successful_timestamp > 86400
        labels:
          severity: warning
        annotations:
          summary: "Velero scheduled backup missed"
```

## Best Practices

- Set up automated, scheduled backups for critical workloads
- Test restore procedures regularly
- Use backup hooks for application-consistent backups
- Monitor backup success and failure rates
- Implement proper retention policies
- Store backups in different regions for disaster recovery
- Document restore procedures and runbooks
- Use resource selectors to optimize backup scope

## Integration Examples

### GitOps with ArgoCD
```yaml
# argo-app-backup.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: backup-schedule
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/k8s-configs
    path: velero/schedules
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: velero
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Great Resources

- [Velero Documentation](https://velero.io/docs/) - Official comprehensive documentation
- [Velero GitHub Repository](https://github.com/vmware-tanzu/velero) - Source code and issue tracking
- [Disaster Recovery Guide](https://velero.io/docs/v1.12/disaster-case/) - Step-by-step disaster recovery procedures
- [Plugin Documentation](https://velero.io/plugins/) - Available plugins for different providers
- [Backup Hooks](https://velero.io/docs/v1.12/backup-hooks/) - Application-consistent backup strategies
- [Troubleshooting Guide](https://velero.io/docs/v1.12/troubleshooting/) - Common issues and solutions
- [Community Resources](https://velero.io/resources/) - Webinars, blogs, and case studies