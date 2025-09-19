# Bash

## Overview

Bash (Bourne Again Shell) is the default shell for most Linux distributions and macOS. It's essential for platform engineers for automation, system administration, and creating deployment scripts. Mastering Bash enables efficient server management and infrastructure automation.

## Key Features

- **Ubiquitous**: Available on virtually all Unix-like systems
- **Powerful**: Rich set of built-in commands and utilities
- **Scripting**: Automate repetitive tasks and complex workflows
- **Integration**: Works seamlessly with system tools and utilities
- **Interactive**: Both command-line interface and scripting language

## Common Use Cases

### System Monitoring Script
```bash
#!/bin/bash

# System health check script
echo "=== System Health Check ==="
echo "Date: $(date)"
echo

# CPU usage
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4 "%"}'

# Memory usage
echo "Memory Usage:"
free -h | awk 'NR==2{printf "Memory Usage: %s/%s (%.2f%%)\n", $3,$2,$3*100/$2 }'

# Disk usage
echo "Disk Usage:"
df -h | awk '$NF=="/"{printf "Disk Usage: %d/%dGB (%s)\n", $3,$2,$5}'

# Load average
echo "Load Average:"
uptime | awk -F'load average:' '{ print $2 }'
```

### Deployment Script
```bash
#!/bin/bash

set -euo pipefail  # Exit on error, undefined vars, pipe failures

APP_NAME="my-application"
VERSION="${1:-latest}"
DEPLOY_ENV="${2:-staging}"

echo "Deploying $APP_NAME version $VERSION to $DEPLOY_ENV"

# Pull latest code
git fetch origin
git checkout "v$VERSION"

# Build and test
docker build -t "$APP_NAME:$VERSION" .
docker run --rm "$APP_NAME:$VERSION" npm test

# Deploy
kubectl set image deployment/$APP_NAME container=$APP_NAME:$VERSION -n $DEPLOY_ENV
kubectl rollout status deployment/$APP_NAME -n $DEPLOY_ENV

echo "Deployment completed successfully!"
```

### Log Analysis
```bash
#!/bin/bash

LOG_FILE="/var/log/nginx/access.log"
DATE_PATTERN="${1:-$(date +%d/%b/%Y)}"

echo "Analyzing logs for $DATE_PATTERN"

# Top 10 IP addresses
echo "Top 10 IP addresses:"
grep "$DATE_PATTERN" "$LOG_FILE" | awk '{print $1}' | sort | uniq -c | sort -nr | head -10

# Response codes summary
echo -e "\nResponse codes:"
grep "$DATE_PATTERN" "$LOG_FILE" | awk '{print $9}' | sort | uniq -c | sort -nr

# Top requested URLs
echo -e "\nTop 10 requested URLs:"
grep "$DATE_PATTERN" "$LOG_FILE" | awk '{print $7}' | sort | uniq -c | sort -nr | head -10
```

## Essential Commands

### File Operations
```bash
# Find files
find /path -name "*.log" -mtime +7  # Files older than 7 days
find /path -type f -size +100M      # Files larger than 100MB

# Archive and compress
tar -czf backup.tar.gz /path/to/data
tar -xzf backup.tar.gz

# File manipulation
grep -r "ERROR" /var/log/           # Recursive search
sed -i 's/old/new/g' file.txt       # Replace text
awk '{print $1, $3}' file.txt       # Print specific columns
```

### Process Management
```bash
# Process monitoring
ps aux | grep nginx
pgrep -f "java.*tomcat"
pkill -f "defunct"

# System resources
htop                    # Interactive process viewer
iotop                   # I/O monitoring
netstat -tulpn         # Network connections
```

### Text Processing
```bash
# Log processing pipeline
cat access.log | grep "GET" | awk '{print $1}' | sort | uniq -c | sort -nr

# JSON parsing with jq
curl -s api/users | jq '.[] | select(.active == true) | .name'

# CSV processing
cut -d',' -f1,3 data.csv | sort | uniq
```

## Best Practices

- Always use `set -euo pipefail` at the beginning of scripts
- Quote variables: `"$variable"` instead of `$variable`
- Use `[[ ]]` for conditionals instead of `[ ]`
- Check command success with `if command; then`
- Use functions for reusable code blocks
- Add proper error handling and logging

## Advanced Features

### Functions and Error Handling
```bash
#!/bin/bash

# Error handling function
error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Backup function with error checking
backup_database() {
    local db_name="$1"
    local backup_file="/backup/${db_name}_$(date +%Y%m%d).sql"
    
    log "Starting backup of $db_name"
    
    if ! pg_dump "$db_name" > "$backup_file"; then
        error_exit "Failed to backup database $db_name"
    fi
    
    log "Backup completed: $backup_file"
}
```

## Great Resources

- [Bash Manual](https://www.gnu.org/software/bash/manual/) - Official GNU Bash reference manual
- [ShellCheck](https://www.shellcheck.net/) - Online shell script analyzer and linter
- [Bash Guide for Beginners](https://tldp.org/LDP/Bash-Beginners-Guide/html/) - Comprehensive beginner guide
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/) - In-depth scripting techniques
- [explainshell.com](https://explainshell.com/) - Interactive command breakdown tool
- [Bash Pitfalls](https://mywiki.wooledge.org/BashPitfalls) - Common mistakes and how to avoid them
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) - Best practices for shell scripting