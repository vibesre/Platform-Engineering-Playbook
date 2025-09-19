---
title: Bash & Shell Scripting
description: Master shell scripting with Bash for automation, system administration, and DevOps workflows
---

# Bash & Shell Scripting

Bash (Bourne Again Shell) is the default shell for most Linux distributions and macOS. It's essential for platform engineers for automation, system administration, and creating deployment scripts. This comprehensive guide covers both interactive Bash usage and advanced scripting techniques for building robust automation solutions.

## Overview

Bash serves dual purposes as both an interactive command interpreter and a powerful scripting language:
- **Interactive Shell**: Command-line interface for system interaction
- **Scripting Language**: Automation of complex workflows and system administration
- **POSIX Compliant**: Ensures portability across Unix-like systems
- **Ubiquitous**: Available on virtually all Unix-like systems
- **Integration**: Works seamlessly with system tools and utilities

## Key Features

- **Command Interpreter**: Processes user commands in real-time
- **Scripting Language**: Executes sequences of commands from files
- **Variables and Arrays**: String manipulation, numeric operations, data structures
- **Control Structures**: Conditional statements, loops, functions
- **Pattern Matching**: Glob patterns, regular expressions, parameter expansion
- **Process Control**: Job control, signal handling, background processes
- **Input/Output**: Redirection, pipes, here documents, process substitution

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

## Comprehensive Deployment Script Example

Here's a production-ready deployment script demonstrating advanced Bash techniques:

```bash
#!/usr/bin/env bash
#
# Application Deployment Script
# This script automates the deployment of a web application
#
# Usage: ./deploy.sh [environment] [version]
# Example: ./deploy.sh production v2.1.0

set -euo pipefail  # Exit on error, undefined variable, pipe failure

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="/var/log/deploy-$(date +%Y%m%d-%H%M%S).log"
readonly BACKUP_DIR="/backup/deployments"

# Default values
DEFAULT_ENV="staging"
DEFAULT_VERSION="latest"

# Functions
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        INFO)
            echo -e "${GREEN}[INFO]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        WARN)
            echo -e "${YELLOW}[WARN]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        ERROR)
            echo -e "${RED}[ERROR]${NC} $message" | tee -a "$LOG_FILE"
            ;;
    esac
}

validate_environment() {
    local env="$1"
    local valid_envs=("development" "staging" "production")
    
    if [[ " ${valid_envs[@]} " =~ " ${env} " ]]; then
        return 0
    else
        log ERROR "Invalid environment: $env"
        log ERROR "Valid environments: ${valid_envs[*]}"
        return 1
    fi
}

deploy_application() {
    local env="$1"
    local version="$2"
    
    log INFO "Deploying version $version to $env environment..."
    
    # Deploy logic here
    return 0
}

# Main execution
main() {
    local environment="${1:-$DEFAULT_ENV}"
    local version="${2:-$DEFAULT_VERSION}"
    
    log INFO "Starting deployment process..."
    
    if ! validate_environment "$environment"; then
        exit 1
    fi
    
    if deploy_application "$environment" "$version"; then
        log INFO "Deployment completed successfully"
        exit 0
    else
        log ERROR "Deployment failed"
        exit 1
    fi
}

# Trap signals for cleanup
trap 'log ERROR "Script interrupted"; exit 130' INT TERM

# Execute main function
main "$@"
```

## Interview Tips

### Common Questions
1. **"What's the difference between $* and $@?"**
   - `$*`: Treats all arguments as a single string
   - `$@`: Preserves individual arguments (preferred)

2. **"How do you handle errors in Bash scripts?"**
   - Use `set -e` to exit on error
   - Implement error handlers with trap
   - Check return codes explicitly

3. **"Explain [ ], [[ ]], and (( ))"**
   - `[ ]`: POSIX test command
   - `[[ ]]`: Bash conditional expression (preferred)
   - `(( ))`: Arithmetic evaluation

4. **"How do you debug Bash scripts?"**
   ```bash
   set -x                # Enable debug mode
   PS4='${LINENO}: '     # Show line numbers
   bash -n script.sh     # Syntax check
   shellcheck script.sh  # Static analysis
   ```

### Practice Challenges
- Write a log rotation script
- Parse CSV files and generate reports
- Create a system monitoring tool
- Build a backup solution
- Implement deployment automation

## Essential Resources

### Documentation & References
- [Bash Manual](https://www.gnu.org/software/bash/manual/) - Official GNU Bash reference manual
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/) - In-depth scripting techniques
- [Bash Guide for Beginners](https://tldp.org/LDP/Bash-Beginners-Guide/html/) - Comprehensive beginner guide
- [Bash Hackers Wiki](https://wiki.bash-hackers.org/) - Modern Bash scripting techniques

### Tools & Utilities
- [ShellCheck](https://www.shellcheck.net/) - Static analysis tool for shell scripts
- [explainshell.com](https://explainshell.com/) - Interactive command breakdown tool
- [bashdb](http://bashdb.sourceforge.net/) - Bash debugger
- [bats](https://github.com/bats-core/bats-core) - Bash Automated Testing System

### Style Guides & Best Practices
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) - Industry best practices
- [Bash Pitfalls](https://mywiki.wooledge.org/BashPitfalls) - Common mistakes and how to avoid them
- [Greg's Wiki](https://mywiki.wooledge.org/BashGuide) - Community-maintained Bash guide

### Books & Learning Resources
- **"Learning the bash Shell"** by Cameron Newham - Comprehensive reference
- **"Classic Shell Scripting"** by Arnold Robbins - POSIX shell scripting
- **"bash Cookbook"** by Carl Albing - Solutions to common problems
- **"Wicked Cool Shell Scripts"** by Dave Taylor - Practical examples

---

**Next Steps**: Master Bash fundamentals before moving to [Linux System Administration](/technical/system-administration) or exploring [Git](/technical/git) for version control automation.