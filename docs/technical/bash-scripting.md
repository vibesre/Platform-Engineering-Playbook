---
title: "Bash Scripting"
description: "Master shell scripting with Bash for automation, system administration, and DevOps workflows"
---

# Bash Scripting

Bash scripting is an essential skill for platform engineers, enabling automation of repetitive tasks, system administration, and complex deployment workflows. As the default shell on most Linux distributions, Bash provides a powerful scripting environment that bridges the gap between simple command execution and full programming. This guide covers everything from basic syntax to advanced techniques, helping you write efficient, maintainable, and robust shell scripts.

## Core Concepts and Features

### Shell Fundamentals
Bash (Bourne Again Shell) is both an interactive command interpreter and a scripting language:
- **Command Interpreter**: Processes user commands in real-time
- **Scripting Language**: Executes sequences of commands from files
- **POSIX Compliant**: Ensures portability across Unix-like systems
- **Feature-Rich**: Supports advanced programming constructs

### Key Language Features
1. **Variables and Data Types**
   - String manipulation
   - Numeric operations
   - Arrays (indexed and associative)
   - Environment variables

2. **Control Structures**
   - Conditional statements (if/elif/else)
   - Loops (for, while, until)
   - Case statements
   - Function definitions

3. **Input/Output**
   - Redirection and pipes
   - Here documents
   - Process substitution
   - File descriptors

4. **Pattern Matching**
   - Glob patterns
   - Regular expressions
   - Parameter expansion
   - Brace expansion

5. **Process Control**
   - Job control
   - Signal handling
   - Subshells and command substitution
   - Background processes

## Common Use Cases

### Automation and DevOps
- CI/CD pipeline scripts
- Deployment automation
- Configuration management
- Environment setup

### System Administration
- User management automation
- Backup and restore procedures
- Log rotation and cleanup
- System monitoring scripts

### Data Processing
- Log file analysis
- Text processing and transformation
- Report generation
- Batch file operations

### Infrastructure Management
- Server provisioning
- Service health checks
- Resource monitoring
- Automated remediation

## Getting Started Example

Here's a comprehensive example demonstrating various Bash features:

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

check_prerequisites() {
    log INFO "Checking prerequisites..."
    
    # Check required commands
    local required_commands=("git" "docker" "docker-compose" "curl")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log ERROR "Required command not found: $cmd"
            return 1
        fi
    done
    
    # Check disk space
    local available_space=$(df -BG /var | tail -1 | awk '{print $4}' | sed 's/G//')
    if [[ $available_space -lt 10 ]]; then
        log ERROR "Insufficient disk space: ${available_space}GB available (10GB required)"
        return 1
    fi
    
    # Check if services are running
    if ! systemctl is-active --quiet docker; then
        log WARN "Docker service is not running. Starting..."
        sudo systemctl start docker
    fi
    
    log INFO "Prerequisites check passed"
    return 0
}

backup_current_deployment() {
    local env="$1"
    local backup_path="${BACKUP_DIR}/${env}-$(date +%Y%m%d-%H%M%S)"
    
    log INFO "Creating backup at $backup_path..."
    
    mkdir -p "$backup_path"
    
    # Backup application files
    if [[ -d "/opt/app/$env" ]]; then
        cp -r "/opt/app/$env" "$backup_path/"
    fi
    
    # Backup database
    if docker ps --format '{{.Names}}' | grep -q "${env}-db"; then
        docker exec "${env}-db" pg_dump -U appuser appdb > "$backup_path/database.sql"
    fi
    
    # Create backup manifest
    cat > "$backup_path/manifest.json" <<EOF
{
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "environment": "$env",
    "backup_size": "$(du -sh "$backup_path" | cut -f1)",
    "files": $(find "$backup_path" -type f | wc -l)
}
EOF
    
    log INFO "Backup completed successfully"
}

deploy_application() {
    local env="$1"
    local version="$2"
    
    log INFO "Deploying version $version to $env environment..."
    
    # Create deployment directory
    local deploy_dir="/opt/app/$env"
    mkdir -p "$deploy_dir"
    cd "$deploy_dir"
    
    # Clone or update repository
    if [[ ! -d ".git" ]]; then
        git clone https://github.com/company/app.git .
    else
        git fetch origin
    fi
    
    # Checkout specific version
    git checkout "$version"
    
    # Load environment-specific configuration
    local config_file="config/${env}.env"
    if [[ -f "$config_file" ]]; then
        export $(grep -v '^#' "$config_file" | xargs)
    fi
    
    # Build and deploy with Docker Compose
    docker-compose -f "docker-compose.yml" -f "docker-compose.${env}.yml" down
    docker-compose -f "docker-compose.yml" -f "docker-compose.${env}.yml" build
    docker-compose -f "docker-compose.yml" -f "docker-compose.${env}.yml" up -d
    
    # Wait for services to be healthy
    local retries=30
    while ((retries > 0)); do
        if curl -sf "http://localhost:8080/health" > /dev/null; then
            log INFO "Application is healthy"
            break
        fi
        ((retries--))
        log INFO "Waiting for application to start... ($retries retries left)"
        sleep 5
    done
    
    if ((retries == 0)); then
        log ERROR "Application failed to start"
        return 1
    fi
    
    return 0
}

cleanup_old_deployments() {
    log INFO "Cleaning up old backups..."
    
    # Keep only last 5 backups per environment
    find "$BACKUP_DIR" -maxdepth 1 -type d -name "*-*" | sort -r | tail -n +6 | xargs -r rm -rf
    
    # Remove old Docker images
    docker image prune -af --filter "until=168h" > /dev/null 2>&1
    
    log INFO "Cleanup completed"
}

send_notification() {
    local status="$1"
    local env="$2"
    local version="$3"
    
    # Send Slack notification (example)
    if [[ -n "${SLACK_WEBHOOK_URL:-}" ]]; then
        local color=$([ "$status" = "success" ] && echo "good" || echo "danger")
        local message=$([ "$status" = "success" ] && echo "Deployment successful" || echo "Deployment failed")
        
        curl -X POST -H 'Content-type: application/json' \
            --data "{
                \"attachments\": [{
                    \"color\": \"$color\",
                    \"title\": \"Deployment Notification\",
                    \"text\": \"$message\",
                    \"fields\": [
                        {\"title\": \"Environment\", \"value\": \"$env\", \"short\": true},
                        {\"title\": \"Version\", \"value\": \"$version\", \"short\": true}
                    ]
                }]
            }" \
            "$SLACK_WEBHOOK_URL" > /dev/null 2>&1
    fi
}

# Main execution
main() {
    # Parse arguments
    local environment="${1:-$DEFAULT_ENV}"
    local version="${2:-$DEFAULT_VERSION}"
    
    log INFO "Starting deployment process..."
    log INFO "Environment: $environment"
    log INFO "Version: $version"
    
    # Validate inputs
    if ! validate_environment "$environment"; then
        exit 1
    fi
    
    # Check prerequisites
    if ! check_prerequisites; then
        exit 1
    fi
    
    # Create backup
    backup_current_deployment "$environment"
    
    # Deploy application
    if deploy_application "$environment" "$version"; then
        log INFO "Deployment completed successfully"
        send_notification "success" "$environment" "$version"
        cleanup_old_deployments
        exit 0
    else
        log ERROR "Deployment failed"
        send_notification "failure" "$environment" "$version"
        exit 1
    fi
}

# Trap signals for cleanup
trap 'log ERROR "Script interrupted"; exit 130' INT TERM

# Execute main function
main "$@"
```

## Best Practices

### 1. Script Structure and Style
```bash
#!/usr/bin/env bash
# Script description and usage information

set -euo pipefail  # Strict mode
IFS=$'\n\t'       # Set Internal Field Separator

# Constants (readonly variables)
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Global variables (use sparingly)
DEBUG="${DEBUG:-false}"

# Function definitions
function usage() {
    cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS] ARGUMENTS

Options:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output
    -d, --debug     Enable debug mode
EOF
}

# Main logic at the bottom
main() {
    # Script logic here
    :
}

main "$@"
```

### 2. Error Handling
```bash
# Enable strict error handling
set -euo pipefail

# Custom error handler
error_handler() {
    local line_number="$1"
    local error_code="$2"
    echo "Error on line $line_number: Command exited with status $error_code"
    # Cleanup operations
    cleanup
    exit "$error_code"
}

trap 'error_handler ${LINENO} $?' ERR

# Cleanup function
cleanup() {
    # Remove temporary files
    rm -f /tmp/script-*
    # Kill background processes
    jobs -p | xargs -r kill
}

trap cleanup EXIT
```

### 3. Input Validation
```bash
# Validate arguments
validate_input() {
    local input="$1"
    
    # Check if empty
    if [[ -z "$input" ]]; then
        echo "Error: Input cannot be empty" >&2
        return 1
    fi
    
    # Check if file exists
    if [[ ! -f "$input" ]]; then
        echo "Error: File does not exist: $input" >&2
        return 1
    fi
    
    # Validate format (example: IP address)
    if [[ ! "$input" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        echo "Error: Invalid IP address format" >&2
        return 1
    fi
    
    return 0
}

# Safe variable expansion
safe_echo() {
    printf '%s\n' "$1"
}
```

### 4. Logging and Debugging
```bash
# Debug function
debug() {
    if [[ "${DEBUG}" == "true" ]]; then
        echo "[DEBUG] $*" >&2
    fi
}

# Logging with levels
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] [$level] $message" | tee -a "${LOG_FILE:-/dev/null}"
    
    # Also log to syslog if available
    if command -v logger &> /dev/null; then
        logger -t "$SCRIPT_NAME" -p "user.$level" "$message"
    fi
}

# Usage
debug "Variable X = $x"
log INFO "Starting process..."
log ERROR "Failed to connect to database"
```

## Common Commands and Operations

### String Manipulation
```bash
# String length
string="Hello World"
echo ${#string}  # 11

# Substring extraction
echo ${string:0:5}   # Hello
echo ${string:6}     # World

# String replacement
echo ${string/World/Universe}  # Hello Universe
echo ${string//l/L}           # HeLLo WorLd

# Case conversion
echo ${string^^}  # HELLO WORLD
echo ${string,,}  # hello world

# Trim whitespace
trim() {
    local var="$*"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    echo -n "$var"
}

# Split string into array
IFS=',' read -ra ARRAY <<< "one,two,three"
for item in "${ARRAY[@]}"; do
    echo "$item"
done
```

### Array Operations
```bash
# Indexed arrays
declare -a fruits=("apple" "banana" "orange")
fruits+=("grape")  # Append
echo ${fruits[1]}  # banana
echo ${#fruits[@]}  # Array length
echo ${fruits[@]}   # All elements

# Associative arrays
declare -A colors=(
    ["red"]="#FF0000"
    ["green"]="#00FF00"
    ["blue"]="#0000FF"
)
echo ${colors["red"]}  # #FF0000
echo ${!colors[@]}     # All keys

# Array iteration
for fruit in "${fruits[@]}"; do
    echo "I like $fruit"
done

for color in "${!colors[@]}"; do
    echo "$color = ${colors[$color]}"
done
```

### File Operations
```bash
# Read file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < input.txt

# Process file with specific delimiter
while IFS=',' read -r name age city; do
    echo "Name: $name, Age: $age, City: $city"
done < data.csv

# Write to file with here document
cat > config.ini <<EOF
[database]
host=localhost
port=5432
user=admin
EOF

# Atomic file write
temp_file=$(mktemp)
echo "data" > "$temp_file"
mv "$temp_file" "final_file.txt"

# File locking
{
    flock -n 200 || { echo "Could not acquire lock"; exit 1; }
    # Critical section
    echo "Processing with exclusive lock..."
} 200>/var/lock/script.lock
```

### Process Management
```bash
# Run command with timeout
timeout 30s long_running_command || echo "Command timed out"

# Background processes
command1 &
pid1=$!
command2 &
pid2=$!

# Wait for specific process
wait $pid1
echo "Command1 exit code: $?"

# Wait for all background jobs
wait

# Process substitution
diff <(sort file1.txt) <(sort file2.txt)

# Parallel execution
parallel_exec() {
    local max_jobs="${1:-4}"
    while IFS= read -r item; do
        while (( $(jobs -r | wc -l) >= max_jobs )); do
            sleep 0.1
        done
        process_item "$item" &
    done
    wait
}
```

### Advanced Techniques
```bash
# Named pipes (FIFOs)
mkfifo /tmp/mypipe
# Terminal 1: echo "Hello" > /tmp/mypipe
# Terminal 2: cat < /tmp/mypipe

# Coprocess
coproc BC { bc; }
echo "2+2" >&${BC[1]}
read result <&${BC[0]}
echo "Result: $result"

# Here strings
grep "pattern" <<< "$variable"

# Command grouping
{ echo "Header"; cat data.txt; echo "Footer"; } > output.txt

# Arithmetic operations
((x = 10 + 5 * 2))
echo $((16#FF))  # Hex to decimal
echo $((2#1010)) # Binary to decimal

# Pattern matching with extglob
shopt -s extglob
case "$file" in
    *.@(jpg|jpeg|png|gif))
        echo "Image file"
        ;;
    *.@(mp3|wav|ogg))
        echo "Audio file"
        ;;
esac
```

## Interview Tips

### Key Topics to Master
1. **Shell Basics**: Understand shells, subshells, and process execution
2. **Scripting Fundamentals**: Variables, functions, control flow
3. **Text Processing**: sed, awk, grep mastery
4. **Error Handling**: Exit codes, traps, signal handling
5. **Best Practices**: Code organization, debugging, security
6. **Performance**: Optimization techniques, efficient algorithms

### Common Interview Questions
1. "What's the difference between $* and $@?"
   ```bash
   # $* treats all arguments as a single string
   # $@ preserves individual arguments
   function test_args() {
       echo "Using \$*:"
       for arg in "$*"; do echo "  $arg"; done
       echo "Using \$@:"
       for arg in "$@"; do echo "  $arg"; done
   }
   test_args "arg 1" "arg 2" "arg 3"
   ```

2. "How do you handle errors in Bash scripts?"
   - Use `set -e` to exit on error
   - Implement error handlers with trap
   - Check return codes explicitly
   - Use defensive programming

3. "Explain the difference between [ ], [[ ]], and (( ))"
   - `[ ]`: POSIX compliant test command
   - `[[ ]]`: Bash conditional expression
   - `(( ))`: Arithmetic evaluation

4. "How do you debug Bash scripts?"
   ```bash
   set -x  # Enable debug mode
   PS4='${LINENO}: '  # Show line numbers
   bash -n script.sh  # Syntax check
   shellcheck script.sh  # Static analysis
   ```

### Practical Challenges
Be prepared to:
- Write a log rotation script
- Parse CSV files and generate reports
- Implement a deployment automation script
- Create a system monitoring tool
- Build a backup solution

## Essential Resources

### Books
1. **"Learning the bash Shell"** by Cameron Newham
   - Comprehensive Bash reference
   - In-depth coverage of advanced features

2. **"Classic Shell Scripting"** by Arnold Robbins and Nelson Beebe
   - POSIX shell scripting focus
   - Portable scripting techniques

3. **"Pro Bash Programming"** by Chris Johnson
   - Advanced scripting techniques
   - Real-world examples

4. **"Wicked Cool Shell Scripts"** by Dave Taylor
   - Practical script examples
   - Problem-solving approach

5. **"bash Cookbook"** by Carl Albing and JP Vossen
   - Solutions to common problems
   - Ready-to-use scripts

### Videos and Courses
1. **"Bash Scripting and Shell Programming"** - Linux Academy
   - Comprehensive video course
   - Hands-on labs

2. **"Advanced Bash Scripting"** - Pluralsight
   - Deep dive into advanced topics
   - Real-world scenarios

3. **"Shell Scripting Tutorial"** - Derek Banas (YouTube)
   - Fast-paced comprehensive tutorial
   - Good for quick learning

4. **"The Bash Guide"** - Maarten Billemont
   - Interactive online guide
   - Best practices focus

### Online Resources and Documentation
1. **Bash Reference Manual**
   - Official GNU Bash documentation
   - Complete language reference

2. **Advanced Bash-Scripting Guide**
   - Extensive tutorial and reference
   - Hundreds of examples

3. **ShellCheck Wiki**
   - Common mistakes and fixes
   - Best practices

4. **Greg's Wiki (Wooledge)**
   - Community-maintained Bash guide
   - FAQ and pitfalls

5. **Bash Hackers Wiki**
   - Modern Bash scripting
   - Tips and tricks

### Tools and Utilities
1. **ShellCheck**: Static analysis tool for shell scripts
2. **bashdb**: Bash debugger
3. **bats**: Bash Automated Testing System
4. **shfmt**: Shell script formatter
5. **explainshell.com**: Interactive command explanation
6. **bash-completion**: Programmable completion

### Communities and Forums
1. **r/bash**: Reddit Bash community
2. **Stack Overflow [bash] tag**: Q&A resource
3. **#bash on Libera.Chat**: IRC channel
4. **Bash-hackers community**: Advanced scripting
5. **Unix & Linux Stack Exchange**: Shell scripting Q&A

### Practice Resources
1. **HackerRank Shell Challenges**: Coding challenges
2. **Bash scripting cheatsheet**: Quick reference
3. **Exercism Bash Track**: Mentored exercises
4. **Codewars**: Shell kata challenges
5. **Linux Shell Scripting Tutorial**: Beginner-friendly guide

Remember, Bash scripting is as much about understanding the Unix philosophy as it is about syntax. Focus on writing clear, maintainable scripts that follow the principle of doing one thing well. Practice regularly, read other people's scripts, and always consider portability and error handling in your solutions.