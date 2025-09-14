---
title: Linux & System Fundamentals
sidebar_position: 2
tags: [beginner, linux, fundamentals]
---

# 🐧 Linux & System Fundamentals

**Prerequisites**: Basic computer knowledge  
**Time to Complete**: ⏱️ 2-3 hours

## Introduction

Linux is the foundation of modern platform engineering. Whether you're working with containers, cloud infrastructure, or CI/CD pipelines, Linux knowledge is essential. This guide covers the fundamentals you need to get started.

## Linux Basics

### What is Linux?

Linux is an open-source operating system kernel created by Linus Torvalds in 1991. Combined with GNU tools, it forms complete operating systems called distributions (distros).

### Popular Distributions

| Distribution | Use Case | Package Manager |
|-------------|----------|-----------------|
| **Ubuntu/Debian** | General purpose, beginner-friendly | apt |
| **RHEL/CentOS/Rocky** | Enterprise servers | yum/dnf |
| **Alpine** | Containers (minimal size) | apk |
| **Amazon Linux** | AWS EC2 instances | yum |

## File System Hierarchy

### Standard Directory Structure

```
/
├── bin/     # Essential user commands
├── boot/    # Boot loader files
├── dev/     # Device files
├── etc/     # System configuration
├── home/    # User home directories
├── lib/     # Shared libraries
├── opt/     # Optional software
├── proc/    # Process information (virtual)
├── root/    # Root user home
├── sbin/    # System binaries
├── tmp/     # Temporary files
├── usr/     # User programs
└── var/     # Variable data (logs, etc.)
```

### Important Paths to Know

- `/etc/passwd` - User accounts
- `/etc/hosts` - Hostname resolution
- `/var/log/` - System logs
- `/etc/systemd/` - Systemd configuration
- `/proc/cpuinfo` - CPU information
- `/proc/meminfo` - Memory information

## Essential Commands

### Navigation and File Operations

```bash
# Navigation
pwd                  # Print working directory
cd /path/to/dir     # Change directory
cd ~                # Go to home directory
cd -                # Go to previous directory

# Listing files
ls                  # List files
ls -la              # List all files with details
ls -lh              # Human-readable sizes
tree                # Directory tree view

# File operations
cp source dest      # Copy file
cp -r dir1 dir2     # Copy directory
mv old new          # Move/rename
rm file             # Remove file
rm -rf dir          # Remove directory (careful!)
mkdir -p /a/b/c     # Create nested directories
touch file          # Create empty file

# File content
cat file            # Display file content
less file           # Page through file
head -n 10 file     # First 10 lines
tail -n 10 file     # Last 10 lines
tail -f file        # Follow file updates
```

### File Permissions

```bash
# Permission format: -rwxrwxrwx
# Type User Group Other

# Change permissions
chmod 755 file      # rwxr-xr-x
chmod +x script.sh  # Add execute permission
chmod -w file       # Remove write permission

# Change ownership
chown user:group file
chown -R user:group dir/

# Special permissions
chmod u+s file      # Set user ID (SUID)
chmod g+s dir       # Set group ID (SGID)
chmod +t dir        # Sticky bit
```

### Process Management

```bash
# View processes
ps aux              # All processes
ps -ef              # Full format
top                 # Interactive process viewer
htop                # Better process viewer

# Process control
kill <pid>          # Terminate process
kill -9 <pid>       # Force kill
killall <name>      # Kill by name
pkill -f pattern    # Kill by pattern

# Background jobs
command &           # Run in background
jobs                # List background jobs
fg %1               # Bring job to foreground
bg %1               # Send job to background
nohup command &     # Run immune to hangups
```

## Text Processing

### Essential Text Tools

```bash
# Search and filter
grep pattern file           # Search for pattern
grep -r pattern dir/        # Recursive search
grep -i pattern file        # Case insensitive
grep -v pattern file        # Invert match
grep -E 'regex' file        # Extended regex

# Text manipulation
sed 's/old/new/g' file      # Replace text
awk '{print $1}' file       # Print first column
cut -d: -f1 /etc/passwd     # Cut by delimiter
sort file                   # Sort lines
uniq file                   # Remove duplicates
wc -l file                  # Count lines
```

### Piping and Redirection

```bash
# Pipes
command1 | command2         # Pipe output
ps aux | grep nginx         # Find nginx processes
cat file | sort | uniq     # Sort and deduplicate

# Redirection
command > file              # Redirect stdout
command 2> file             # Redirect stderr
command &> file             # Redirect both
command >> file             # Append to file
command < file              # Input from file

# Advanced
command 2>&1                # Stderr to stdout
command1 | tee file | command2  # Save and pipe
```

## Networking Basics

### Network Commands

```bash
# Network configuration
ip addr show                # Show IP addresses
ip route show              # Show routing table
ifconfig                   # Legacy IP config
hostname                   # Show hostname

# Connectivity testing
ping google.com            # Test connectivity
ping -c 4 google.com      # Ping 4 times
traceroute google.com     # Trace network path
mtr google.com            # Better traceroute

# DNS
dig google.com            # DNS lookup
nslookup google.com       # Legacy DNS lookup
host google.com           # Simple DNS lookup
cat /etc/resolv.conf      # DNS servers

# Port and connections
netstat -tlnp             # Listening ports
ss -tlnp                  # Modern netstat
lsof -i :80              # Process on port 80
telnet host 80           # Test port connectivity
nc -zv host 80           # Port scan
```

### Common Ports to Know

| Port | Service |
|------|---------|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 27017 | MongoDB |

## Package Management

### Debian/Ubuntu (apt)

```bash
# Update package list
sudo apt update

# Install package
sudo apt install nginx

# Remove package
sudo apt remove nginx
sudo apt purge nginx      # Remove with config

# Search packages
apt search keyword

# Show package info
apt show nginx

# Upgrade system
sudo apt upgrade          # Upgrade packages
sudo apt dist-upgrade     # Smart upgrade
```

### RedHat/CentOS (yum/dnf)

```bash
# Install package
sudo yum install nginx
sudo dnf install nginx    # Newer systems

# Remove package
sudo yum remove nginx

# Search packages
yum search keyword

# List installed
yum list installed

# Update system
sudo yum update
```

## System Services

### Systemd (Modern Systems)

```bash
# Service management
systemctl start nginx       # Start service
systemctl stop nginx        # Stop service
systemctl restart nginx     # Restart service
systemctl reload nginx      # Reload config
systemctl status nginx      # Check status

# Enable/disable at boot
systemctl enable nginx      # Start at boot
systemctl disable nginx     # Don't start at boot

# View logs
journalctl -u nginx         # Service logs
journalctl -f              # Follow all logs
journalctl --since "1 hour ago"
```

### Service Files Location

- `/etc/systemd/system/` - Custom services
- `/lib/systemd/system/` - System services

## Shell Scripting Basics

### Your First Script

```bash
#!/bin/bash
# This is a comment

# Variables
NAME="Platform Engineer"
echo "Hello, $NAME!"

# Conditionals
if [ -f /etc/passwd ]; then
    echo "File exists"
else
    echo "File not found"
fi

# Loops
for i in 1 2 3; do
    echo "Number: $i"
done

# Functions
greet() {
    echo "Hello, $1!"
}

greet "World"
```

### Making Scripts Executable

```bash
chmod +x script.sh
./script.sh
```

### Common Script Patterns

```bash
# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Check if command exists
if ! command -v docker &> /dev/null; then
    echo "Docker not installed"
    exit 1
fi

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
```

## Environment Variables

### Working with Variables

```bash
# Set variable
export VAR_NAME="value"

# View variable
echo $VAR_NAME

# View all variables
env
printenv

# Common variables
echo $PATH          # Executable search path
echo $HOME          # Home directory
echo $USER          # Current user
echo $SHELL         # Current shell
echo $PWD           # Current directory
```

### Persistent Variables

Add to `~/.bashrc` or `~/.bash_profile`:
```bash
export PATH="$PATH:/opt/bin"
export EDITOR="vim"
```

## Interview Preparation

### Common Linux Interview Questions

**Q: How do you find all files larger than 100MB?**
```bash
find / -type f -size +100M 2>/dev/null
```

**Q: How do you check disk usage?**
```bash
df -h              # File system usage
du -sh /var/*      # Directory sizes
```

**Q: How do you find which process is using a file?**
```bash
lsof /path/to/file
fuser /path/to/file
```

**Q: How do you check system resources?**
```bash
free -h            # Memory usage
uptime             # Load average
vmstat 1           # Virtual memory stats
iostat -x 1        # I/O statistics
```

### Troubleshooting Scenarios

**1. "Cannot allocate memory" error**
- Check memory: `free -h`
- Check for memory leaks: `ps aux --sort=-%mem | head`
- Check swap: `swapon -s`

**2. "No space left on device"**
- Check disk space: `df -h`
- Find large files: `du -ah / | sort -rh | head -20`
- Check inodes: `df -i`

**3. High load average**
- Check load: `uptime`
- Find CPU-intensive processes: `top`
- Check I/O wait: `iostat -x 1`

## Practice Exercises

### Exercise 1: File Management
1. Create a directory structure: `/tmp/project/{src,docs,tests}`
2. Create 10 files named `file1.txt` through `file10.txt`
3. Find all `.txt` files and copy them to `/tmp/backup`
4. Change permissions so only you can read/write

### Exercise 2: Process Management
1. Start a long-running process in the background
2. Find its PID using different methods
3. Send it to background/foreground
4. Terminate it gracefully

### Exercise 3: Text Processing
1. Download a log file
2. Extract all IP addresses
3. Count unique IPs
4. Find top 10 most frequent IPs

## Next Steps

Ready to level up? Continue with:
- [Programming for Platform Engineers →](programming-basics)
- [Bash Scripting Deep Dive →](../intermediate/bash-scripting)

## Quick Reference

### Emergency Commands
```bash
# System is slow
top                    # Check CPU/memory
iotop                  # Check disk I/O
netstat -tulpn         # Check network

# Disk full
df -h                  # Check disk space
du -sh /* | sort -h    # Find large directories
find / -size +1G       # Find large files

# Can't connect
ping 8.8.8.8          # Test internet
systemctl status sshd  # Check SSH service
iptables -L           # Check firewall
```

## Additional Resources

- 📚 **Book**: [The Linux Command Line](https://linuxcommand.org/tlcl.php) (Free PDF)
- 🎮 **Interactive**: [Linux Survival](https://linuxsurvival.com/)
- 📖 **Reference**: [Explain Shell](https://explainshell.com/)
- 🎥 **Course**: [Linux Journey](https://linuxjourney.com/)