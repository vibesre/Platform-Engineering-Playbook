---
title: Linux Systems
sidebar_position: 2
---

# Linux Systems for Platform Engineers

<GitHubButtons />
Master Linux fundamentals and internals for platform engineering interviews.

## 🎯 Interview Focus Areas

### Most Asked Topics
1. **Process Management** - How processes work, debugging, signals
2. **Memory Management** - Virtual memory, OOM killer, troubleshooting
3. **File Systems** - Permissions, inodes, performance
4. **Networking** - TCP/IP stack, troubleshooting, iptables
5. **System Performance** - Identifying bottlenecks, optimization

## Essential Commands

### Process Management

```bash
# View processes
ps aux                      # All processes with details
ps -ef --forest            # Process tree
top -H -p <pid>            # Show threads for process
htop                       # Interactive process viewer

# Process control
kill -l                    # List all signals
kill -TERM <pid>          # Graceful termination (15)
kill -KILL <pid>          # Force kill (9)
killall <name>            # Kill by process name
pkill -f pattern          # Kill by pattern

# Process debugging
strace -p <pid>           # Trace system calls
strace -c command         # Count system calls
ltrace command            # Library call tracing
lsof -p <pid>            # Files opened by process
pstack <pid>             # Print stack trace

# Background jobs
command &                 # Run in background
jobs                     # List background jobs
fg %1                    # Bring to foreground
bg %1                    # Continue in background
nohup command &          # Survive logout
disown %1                # Remove from job table
```

### Memory Management

```bash
# Memory information
free -h                   # Human-readable memory
vmstat 1                 # Virtual memory stats
cat /proc/meminfo        # Detailed memory info
smem -rs swap            # Memory by swap usage
pmap -x <pid>           # Process memory mapping

# Memory debugging
valgrind --leak-check=full ./program
dmesg | grep -i "out of memory"
cat /proc/<pid>/status | grep -i vm
echo 3 > /proc/sys/vm/drop_caches  # Clear cache
```

### File Systems & Storage

```bash
# Disk usage
df -h                    # File system usage
df -i                    # Inode usage
du -sh /*               # Directory sizes
du -sh * | sort -h      # Sorted by size
ncdu /                  # Interactive disk usage

# File operations
find / -type f -size +100M 2>/dev/null    # Large files
find / -type f -mtime +30 -delete         # Delete old files
lsof +L1                                   # Deleted but open files
stat file.txt                              # File metadata

# File permissions
chmod 755 file          # rwxr-xr-x
chmod u+s file         # Set SUID
chmod g+s dir          # Set SGID
chmod +t dir           # Sticky bit
umask 022              # Default permissions

# I/O monitoring
iostat -xz 1           # Extended I/O stats
iotop -o               # I/O by process
blktrace -d /dev/sda   # Block layer tracing
```

### Networking

```bash
# Network configuration
ip addr show            # Show IP addresses
ip route show          # Routing table
ip link show           # Network interfaces
ss -tulpn             # Listening ports (modern)
netstat -tulpn        # Listening ports (legacy)

# Connection debugging
ss -an | grep ESTAB    # Established connections
lsof -i :80           # Process on port
tcpdump -i eth0 -nn port 80              # Packet capture
tcpdump -w capture.pcap -s0              # Save full packets
nc -zv host 80                           # Port connectivity

# DNS troubleshooting
dig +trace google.com   # DNS resolution path
nslookup google.com    # Simple DNS lookup
host -t A google.com   # Specific record type
cat /etc/resolv.conf   # DNS servers

# Network performance
iperf3 -s              # Server mode
iperf3 -c server       # Client test
mtr google.com         # Combined ping/traceroute
ping -c 4 -i 0.2 host  # Fast ping
```

## System Internals

### Boot Process

```
1. BIOS/UEFI → POST
2. Bootloader (GRUB2) → Load kernel
3. Kernel initialization → Mount root filesystem
4. Init system (systemd) → Start services
5. Login prompt
```

**Interview Question**: "What happens when a Linux system boots?"

### Process States

```bash
# Process states in ps output
R - Running or runnable
S - Sleeping (interruptible)
D - Sleeping (uninterruptible, usually I/O)
T - Stopped (SIGSTOP or Ctrl+Z)
Z - Zombie (terminated but not reaped)

# Check process state
ps aux | awk '$8 ~ /^Z/ { print }'  # Find zombies
```

### Virtual Memory

```bash
# Memory layout
cat /proc/<pid>/maps    # Process memory map
pmap -x <pid>          # Detailed memory usage

# Important files
/proc/sys/vm/swappiness         # Swap tendency (0-100)
/proc/sys/vm/overcommit_memory  # Memory overcommit
/proc/sys/vm/min_free_kbytes    # Reserved memory
```

## Performance Troubleshooting

### High CPU Usage

```bash
# 1. Identify the culprit
top -b -n 1 | head -20
ps aux --sort=-%cpu | head

# 2. Analyze the process
strace -c -p <pid>              # System call profile
perf top -p <pid>               # CPU profiling
cat /proc/<pid>/status

# 3. Check for issues
dmesg | tail                    # Kernel messages
journalctl -u service-name      # Service logs
```

### Memory Issues

```bash
# 1. Check memory pressure
free -h
vmstat 1 5
cat /proc/pressure/memory

# 2. Find memory hogs
ps aux --sort=-%mem | head
smem -rs swap -k

# 3. Investigate OOM
dmesg | grep -i "killed process"
journalctl -u systemd-oomd
```

### Disk I/O Problems

```bash
# 1. Check I/O wait
top                    # Look for %wa
iostat -xz 1          # Detailed I/O stats

# 2. Find I/O intensive processes
iotop -o
pidstat -d 1

# 3. Analyze specific disk
hdparm -tT /dev/sda   # Disk speed test
smartctl -a /dev/sda  # Disk health
```

### Network Issues

```bash
# 1. Check connectivity
ping -c 4 8.8.8.8              # Internet connectivity
traceroute google.com          # Path to destination
mtr --report google.com        # Detailed path analysis

# 2. Check DNS
time nslookup google.com       # DNS response time
dig @8.8.8.8 google.com       # Test specific DNS

# 3. Check ports/firewall
sudo iptables -L -n -v         # Firewall rules
ss -tulpn                      # Listening ports
telnet host port               # Test specific port
```

## Common Interview Questions

### Q1: "How do you find what process is using a file?"
```bash
lsof /path/to/file
fuser -v /path/to/file
```

### Q2: "How do you debug a process that won't die?"
```bash
# Check state
ps aux | grep <process>

# If in D state (uninterruptible sleep)
ls -l /proc/<pid>/fd/       # Check file descriptors
cat /proc/<pid>/stack       # Kernel stack trace

# Force kill parent
pstree -p <pid>            # Find parent
kill -9 <parent_pid>
```

### Q3: "How do you find deleted but open files?"
```bash
lsof +L1                   # Files with 0 links
lsof | grep deleted
df -h                      # Compare with du
```

### Q4: "System is slow, how do you investigate?"
```bash
# 1. Check load and CPU
uptime
top

# 2. Check memory
free -h
vmstat 1

# 3. Check I/O
iostat -xz 1
iotop

# 4. Check network
ss -s
netstat -i

# 5. Check logs
dmesg | tail
journalctl -xe
```

### Q5: "How do you optimize Linux performance?"
```bash
# CPU
# - Use nice/renice for priority
# - CPU affinity with taskset
# - Disable unnecessary services

# Memory
echo 10 > /proc/sys/vm/swappiness     # Reduce swapping
echo 3 > /proc/sys/vm/drop_caches     # Clear cache

# Disk
# - Use noatime mount option
# - Adjust I/O scheduler
echo deadline > /sys/block/sda/queue/scheduler

# Network
# - Increase socket buffers
sysctl -w net.core.rmem_max=134217728
# - Enable TCP fast open
sysctl -w net.ipv4.tcp_fastopen=3
```

## Advanced Topics

### Systemd

```bash
# Service management
systemctl start/stop/restart service
systemctl enable/disable service
systemctl status service
systemctl daemon-reload

# Logs
journalctl -u service
journalctl -f               # Follow
journalctl --since "1 hour ago"
journalctl -p err          # Error priority

# Analyze boot
systemd-analyze
systemd-analyze blame       # Boot time by service
systemd-analyze critical-chain
```

### Security

```bash
# SELinux (RHEL/CentOS)
getenforce
setenforce 0/1
ausearch -m avc            # Audit logs
sealert -a /var/log/audit/audit.log

# AppArmor (Ubuntu)
aa-status
aa-complain /path/to/profile
aa-enforce /path/to/profile

# Capabilities
getcap /usr/bin/ping
setcap cap_net_raw+ep /usr/bin/ping
```

### Kernel Parameters

```bash
# View/modify kernel parameters
sysctl -a                          # All parameters
sysctl net.ipv4.ip_forward        # Specific parameter
sysctl -w net.ipv4.ip_forward=1   # Temporary change

# Permanent changes in /etc/sysctl.conf
net.ipv4.ip_forward = 1
vm.swappiness = 10

# Apply changes
sysctl -p
```

## Hands-On Practice

### Exercise 1: Process Investigation
1. Start a CPU-intensive process: `yes > /dev/null &`
2. Find its PID using different methods
3. Check its CPU usage
4. Trace its system calls
5. Change its priority
6. Kill it gracefully

### Exercise 2: Memory Analysis
1. Write a program that leaks memory
2. Monitor system memory while it runs
3. Identify the leak using tools
4. Find when OOM killer activates
5. Analyze the dmesg output

### Exercise 3: Performance Tuning
1. Create I/O load: `dd if=/dev/zero of=test bs=1M count=1000`
2. Monitor I/O performance
3. Change I/O scheduler
4. Compare performance
5. Clean up test files

## Quick Reference

### Emergency Commands
```bash
# System hanging
Alt + SysRq + REISUB    # Safe reboot

# Disk full
du -sh /* | sort -h     # Find large directories
find / -size +1G        # Find large files
lsof +L1               # Deleted open files

# High load
ps aux --sort=-%cpu | head
kill -STOP <pid>       # Pause process
kill -CONT <pid>       # Resume process

# Network down
ip link set eth0 up
systemctl restart NetworkManager
dhclient -r && dhclient
```

## Resources for Deep Learning

- 📚 [The Linux Programming Interface](https://man7.org/tlpi/) - The definitive guide
- 📖 [Linux Performance by Brendan Gregg](https://www.brendangregg.com/linuxperf.html)
- 🎥 [Linux System Programming](https://www.youtube.com/playlist?list=PLvv0ScY6vfd8qupx8UhlPcNvFjKGfELRe)
- 🎓 [Linux Foundation Training](https://training.linuxfoundation.org/)

---

*Pro tip: In interviews, always explain your troubleshooting methodology. Show how you systematically narrow down issues rather than just memorizing commands.*