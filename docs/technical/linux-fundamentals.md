---
title: Linux Fundamentals
description: Master the essential Linux skills every platform engineer needs
---

# Linux Fundamentals

Linux is the foundation of modern infrastructure. Every platform engineer must be proficient in Linux system administration and operations.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **Linux Fundamentals - Full Course for Beginners**
- **Channel**: freeCodeCamp
- **Link**: [YouTube - 5+ hours](https://www.youtube.com/watch?v=sWbUDq4S6Y8)
- **Why it's great**: Comprehensive coverage from absolute basics to advanced topics

#### **Linux System Administration Full Course**
- **Channel**: Geek's Lesson
- **Link**: [YouTube - 3 hours](https://www.youtube.com/watch?v=wsh64rjnRas)
- **Why it's great**: Practical, hands-on approach with real-world scenarios

#### **Linux Command Line Tutorial For Beginners**
- **Channel**: Programming with Mosh
- **Link**: [YouTube - 1 hour](https://www.youtube.com/watch?v=cBokz0LTizk)
- **Why it's great**: Clear, concise explanations perfect for beginners

### 📖 Essential Documentation

#### **The Linux Documentation Project**
- **Link**: [tldp.org](https://tldp.org/)
- **Why it's great**: Comprehensive guides and HOWTOs maintained by the community

#### **Red Hat Enterprise Linux Documentation**
- **Link**: [access.redhat.com/documentation/en-us/red_hat_enterprise_linux/](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/)
- **Why it's great**: Enterprise-grade documentation with best practices

#### **Arch Linux Wiki**
- **Link**: [wiki.archlinux.org](https://wiki.archlinux.org/)
- **Why it's great**: Incredibly detailed, applies to all Linux distributions

### 📝 Must-Read Blogs & Articles

#### **Julia Evans' Linux Comics**
- **Link**: [jvns.ca/blog/2016/07/11/Linux-comics/](https://jvns.ca/blog/2016/07/11/Linux-comics/)
- **Why it's great**: Visual explanations of complex Linux concepts

#### **Brendan Gregg's Linux Performance**
- **Link**: [brendangregg.com/linuxperf.html](https://www.brendangregg.com/linuxperf.html)
- **Why it's great**: Deep dive into Linux performance analysis and tuning

#### **Linux Journey**
- **Link**: [linuxjourney.com](https://linuxjourney.com/)
- **Why it's great**: Interactive, gamified learning path

### 🎓 Structured Courses

#### **Linux Foundation - Introduction to Linux (LFS101x)**
- **Platform**: edX
- **Link**: [edx.org/course/introduction-to-linux](https://www.edx.org/course/introduction-to-linux)
- **Cost**: Free
- **Why it's great**: Created by the Linux Foundation, very comprehensive

#### **Linux Basics Course by Cisco**
- **Platform**: Cisco Networking Academy
- **Link**: [netacad.com/courses/os-it/ndg-linux-unhatched](https://www.netacad.com/courses/os-it/ndg-linux-unhatched)
- **Cost**: Free
- **Why it's great**: Hands-on labs and practical exercises

### 🔧 Interactive Labs

#### **KillerCoda Linux Scenarios**
- **Link**: [killercoda.com/linux](https://killercoda.com/linux)
- **Why it's great**: Free, browser-based Linux environments

#### **Linux Survival**
- **Link**: [linuxsurvival.com](https://linuxsurvival.com/)
- **Why it's great**: Game-like interface for learning commands

## 🎯 Key Concepts to Master

### File System & Navigation
- Directory structure (`/`, `/etc`, `/var`, `/home`, `/usr`)
- File permissions and ownership
- Hard links vs soft links
- Special files (`/dev`, `/proc`, `/sys`)

### Essential Commands
```bash
# Navigation
ls, cd, pwd, find, locate, which

# File Operations  
cp, mv, rm, mkdir, touch, chmod, chown

# Text Processing
cat, less, grep, sed, awk, cut, sort

# System Information
ps, top, htop, df, du, free, uname

# Network
ip, netstat, ss, ping, traceroute, dig

# Package Management
apt/yum/dnf, dpkg/rpm, snap
```

### Process Management
- Process states and lifecycle
- Signals (SIGTERM, SIGKILL, SIGHUP)
- Background jobs (`&`, `jobs`, `fg`, `bg`)
- Process priorities and nice values
- systemd vs init

### Users & Permissions
- User and group management
- File permissions (rwx, octal notation)
- Special permissions (setuid, setgid, sticky bit)
- sudo and su
- PAM (Pluggable Authentication Modules)

### Shell Fundamentals
- Shell types (bash, zsh, sh)
- Environment variables
- Shell expansion and globbing
- Pipes and redirection
- Job control

## 💡 Interview Tips

### Common Interview Questions
1. **Explain the boot process of Linux**
   - BIOS/UEFI → Bootloader → Kernel → Init/systemd → Runlevel/Target

2. **What happens when you type `ls` in the terminal?**
   - Shell interprets command → fork() → exec() → system calls → output

3. **Explain file permissions and how to change them**
   - Read/Write/Execute for User/Group/Others
   - chmod with symbolic (u+x) or octal (755) notation

4. **How do you find which process is using a specific port?**
   - `netstat -tulpn | grep :PORT` or `ss -tulpn | grep :PORT`
   - `lsof -i :PORT`

5. **Explain the difference between hard and soft links**
   - Hard links: same inode, can't cross filesystems
   - Soft links: different inode, can cross filesystems, can break

### Practical Scenarios
- "Debug why a service won't start"
- "Find and fix disk space issues"
- "Troubleshoot high CPU usage"
- "Set up automated log rotation"
- "Secure a Linux server"

## 🏆 Hands-On Practice

### Build These Projects
1. **Automated Server Setup Script**
   - User creation, package installation, security hardening

2. **System Monitoring Dashboard**
   - Collect metrics, create alerts, visualize data

3. **Log Analysis Pipeline**
   - Parse logs, extract insights, automate reporting

4. **Backup and Recovery System**
   - Automated backups, test restores, monitoring

### Practice Environments
- **VirtualBox/VMware**: Run local VMs
- **Vagrant**: Automate VM provisioning
- **AWS EC2 Free Tier**: Cloud-based practice
- **Docker**: Lightweight Linux containers

## 📊 Learning Path

### Week 1-2: Basics
- File system navigation
- Basic commands
- Text editors (vim/nano)
- Package management

### Week 3-4: Intermediate
- Shell scripting basics
- Process management
- User administration
- Basic networking

### Week 5-6: Advanced
- System performance
- Security hardening
- Troubleshooting
- Automation

---

**Next Steps**: Once comfortable with Linux fundamentals, explore [Docker](/technical/docker) to learn containerization or [AWS](/technical/aws) to understand cloud platforms.