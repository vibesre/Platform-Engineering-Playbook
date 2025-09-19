---
title: "Linux Performance Tuning"
description: "Master Linux performance analysis and optimization techniques for high-performance systems"
---

# Linux Performance Tuning

Linux performance tuning is a critical skill for platform engineers managing production systems at scale. Understanding how to analyze, diagnose, and optimize system performance directly impacts application reliability, user experience, and infrastructure costs. This comprehensive guide covers performance analysis methodologies, tuning techniques, and tools that help platform engineers squeeze maximum performance from their Linux systems while maintaining stability and reliability.

## Core Concepts and Features

### Performance Fundamentals
Linux performance involves multiple interconnected subsystems:
- **CPU**: Process scheduling, context switching, cache efficiency
- **Memory**: Virtual memory, paging, cache management
- **Storage I/O**: Disk throughput, latency, queue depth
- **Network**: Bandwidth, latency, packet processing
- **Application**: Code efficiency, resource utilization

### Key Performance Metrics
1. **Latency**: Time to complete an operation
2. **Throughput**: Operations completed per unit time
3. **Utilization**: Percentage of resource in use
4. **Saturation**: Degree of queued work
5. **Errors**: Failed operations rate

### Performance Analysis Methodologies
1. **USE Method** (Utilization, Saturation, Errors)
   - Check utilization of all resources
   - Examine saturation (queue lengths)
   - Look for errors in logs

2. **RED Method** (Rate, Errors, Duration)
   - Request rate
   - Error rate
   - Duration (latency)

3. **Golden Signals** (Google SRE)
   - Latency
   - Traffic
   - Errors
   - Saturation

## Common Use Cases

### Web Application Optimization
- Reducing page load times
- Optimizing database queries
- Caching strategy implementation
- Connection pooling tuning

### Database Performance
- Query optimization
- Index tuning
- Buffer pool sizing
- I/O pattern optimization

### High-Performance Computing
- CPU affinity configuration
- NUMA optimization
- Memory bandwidth tuning
- Network latency reduction

### Container and Kubernetes
- Resource limits optimization
- cgroup configuration
- Network policy impact
- Storage driver selection

## Getting Started Example

Here's a comprehensive performance analysis and tuning workflow:

```bash
#!/bin/bash
#
# Linux Performance Analysis and Baseline Script
# Captures system performance metrics for analysis

# Configuration
OUTPUT_DIR="/var/log/performance"
DURATION="${1:-60}"  # Default 60 seconds
INTERVAL=1

# Create output directory
mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT_DIR="$OUTPUT_DIR/report-$TIMESTAMP"
mkdir -p "$REPORT_DIR"

echo "Starting performance analysis (${DURATION}s)..."

# System Information
collect_system_info() {
    cat > "$REPORT_DIR/system-info.txt" <<EOF
=== System Information ===
Hostname: $(hostname)
Date: $(date)
Kernel: $(uname -r)
CPU: $(lscpu | grep "Model name" | cut -d: -f2 | xargs)
Cores: $(nproc)
Memory: $(free -h | grep Mem | awk '{print $2}')
Uptime: $(uptime)

=== CPU Information ===
$(lscpu)

=== Memory Information ===
$(free -h)

=== Disk Information ===
$(df -h)
$(lsblk)

=== Network Interfaces ===
$(ip addr)
EOF
}

# CPU Performance
analyze_cpu() {
    echo "Collecting CPU metrics..."
    
    # mpstat for CPU statistics
    mpstat -P ALL $INTERVAL $DURATION > "$REPORT_DIR/cpu-mpstat.txt" 2>&1 &
    
    # Per-process CPU usage
    pidstat -u $INTERVAL $DURATION > "$REPORT_DIR/cpu-pidstat.txt" 2>&1 &
    
    # CPU frequency
    for i in $(seq 1 $DURATION); do
        echo "=== $(date) ===" >> "$REPORT_DIR/cpu-frequency.txt"
        cpupower frequency-info 2>/dev/null >> "$REPORT_DIR/cpu-frequency.txt"
        sleep $INTERVAL
    done &
    
    # perf stat for CPU performance counters
    timeout $DURATION perf stat -a \
        -e cycles,instructions,cache-references,cache-misses,branches,branch-misses \
        -o "$REPORT_DIR/cpu-perf-stat.txt" sleep $DURATION 2>&1 &
}

# Memory Performance
analyze_memory() {
    echo "Collecting memory metrics..."
    
    # vmstat for virtual memory statistics
    vmstat $INTERVAL $DURATION > "$REPORT_DIR/memory-vmstat.txt" 2>&1 &
    
    # Memory usage by process
    for i in $(seq 1 $DURATION); do
        echo "=== $(date) ===" >> "$REPORT_DIR/memory-ps.txt"
        ps aux --sort=-%mem | head -20 >> "$REPORT_DIR/memory-ps.txt"
        sleep $INTERVAL
    done &
    
    # Slab info
    while true; do
        echo "=== $(date) ===" >> "$REPORT_DIR/memory-slabtop.txt"
        slabtop -o -s c | head -20 >> "$REPORT_DIR/memory-slabtop.txt"
        sleep 10
    done &
    SLAB_PID=$!
    
    # Page cache statistics
    for i in $(seq 1 $((DURATION/10))); do
        echo "=== $(date) ===" >> "$REPORT_DIR/memory-cache.txt"
        cat /proc/meminfo | grep -E "Cached|Buffers|Dirty|Writeback" >> "$REPORT_DIR/memory-cache.txt"
        sleep 10
    done &
}

# Disk I/O Performance
analyze_disk() {
    echo "Collecting disk I/O metrics..."
    
    # iostat for disk statistics
    iostat -xz $INTERVAL $DURATION > "$REPORT_DIR/disk-iostat.txt" 2>&1 &
    
    # iotop for per-process I/O (requires root)
    if [[ $EUID -eq 0 ]]; then
        iotop -b -n $DURATION -d $INTERVAL > "$REPORT_DIR/disk-iotop.txt" 2>&1 &
    fi
    
    # Block device queue information
    for dev in $(lsblk -d -n -o NAME); do
        if [[ -e /sys/block/$dev/queue ]]; then
            echo "=== Device: $dev ===" >> "$REPORT_DIR/disk-queue-info.txt"
            for param in scheduler nr_requests read_ahead_kb; do
                if [[ -r /sys/block/$dev/queue/$param ]]; then
                    echo "$param: $(cat /sys/block/$dev/queue/$param)" >> "$REPORT_DIR/disk-queue-info.txt"
                fi
            done
        fi
    done
}

# Network Performance
analyze_network() {
    echo "Collecting network metrics..."
    
    # Network statistics
    sar -n DEV $INTERVAL $DURATION > "$REPORT_DIR/network-sar-dev.txt" 2>&1 &
    sar -n TCP,ETCP $INTERVAL $DURATION > "$REPORT_DIR/network-sar-tcp.txt" 2>&1 &
    
    # ss for socket statistics
    for i in $(seq 1 $((DURATION/5))); do
        echo "=== $(date) ===" >> "$REPORT_DIR/network-ss.txt"
        ss -s >> "$REPORT_DIR/network-ss.txt"
        sleep 5
    done &
    
    # Network interface statistics
    for i in $(seq 1 $DURATION); do
        echo "=== $(date) ===" >> "$REPORT_DIR/network-stats.txt"
        ip -s link >> "$REPORT_DIR/network-stats.txt"
        sleep $INTERVAL
    done &
}

# Application Performance
analyze_application() {
    echo "Collecting application metrics..."
    
    # Top processes by various metrics
    for i in $(seq 1 $((DURATION/10))); do
        echo "=== $(date) ===" >> "$REPORT_DIR/app-top.txt"
        top -b -n 1 | head -30 >> "$REPORT_DIR/app-top.txt"
        sleep 10
    done &
    
    # System calls trace for busy processes (sample)
    if command -v strace &> /dev/null; then
        sleep 5  # Let system stabilize
        # Find top CPU consuming process
        TOP_PID=$(ps aux --sort=-%cpu | grep -v "^USER" | head -1 | awk '{print $2}')
        if [[ -n "$TOP_PID" ]]; then
            timeout 10 strace -c -p "$TOP_PID" 2> "$REPORT_DIR/app-strace-$TOP_PID.txt" || true
        fi
    fi &
}

# Performance Tuning Recommendations
generate_recommendations() {
    cat > "$REPORT_DIR/tuning-recommendations.txt" <<'EOF'
=== Performance Tuning Recommendations ===

Based on common patterns, consider these optimizations:

1. CPU Performance:
   - Enable CPU frequency scaling governor: performance
   - Disable CPU throttling for performance-critical apps
   - Consider CPU affinity for multi-threaded applications
   
2. Memory Performance:
   - Adjust vm.swappiness based on workload (10 for databases)
   - Configure huge pages for large memory applications
   - Tune vm.dirty_ratio and vm.dirty_background_ratio
   
3. Disk I/O Performance:
   - Use appropriate I/O scheduler (none for NVMe, mq-deadline for SSD)
   - Adjust read-ahead settings
   - Enable write-back cache if safe
   
4. Network Performance:
   - Increase network buffer sizes
   - Enable TCP optimization features
   - Consider interrupt affinity for high-traffic systems

5. Kernel Parameters to Consider:
EOF

    # Add current kernel parameters
    sysctl -a 2>/dev/null | grep -E "vm.swappiness|vm.dirty|net.core|net.ipv4.tcp" >> "$REPORT_DIR/tuning-recommendations.txt"
}

# Wait function with progress
wait_with_progress() {
    local duration=$1
    local elapsed=0
    
    while [[ $elapsed -lt $duration ]]; do
        echo -ne "\rProgress: $elapsed/$duration seconds"
        sleep 1
        ((elapsed++))
    done
    echo -e "\nCollection complete!"
}

# Main execution
main() {
    echo "Performance analysis started at $(date)"
    echo "Output directory: $REPORT_DIR"
    
    # Start all collections
    collect_system_info
    analyze_cpu
    analyze_memory
    analyze_disk
    analyze_network
    analyze_application
    
    # Wait for collection to complete
    wait_with_progress $DURATION
    
    # Kill background processes
    jobs -p | xargs -r kill 2>/dev/null
    
    # Generate recommendations
    generate_recommendations
    
    # Create summary report
    cat > "$REPORT_DIR/summary.txt" <<EOF
=== Performance Analysis Summary ===
Date: $(date)
Duration: ${DURATION} seconds
Report Location: $REPORT_DIR

Key Files Generated:
- system-info.txt: System configuration
- cpu-*.txt: CPU performance metrics
- memory-*.txt: Memory usage patterns
- disk-*.txt: Disk I/O statistics
- network-*.txt: Network performance data
- tuning-recommendations.txt: Optimization suggestions

Next Steps:
1. Review CPU utilization in cpu-mpstat.txt
2. Check memory pressure in memory-vmstat.txt
3. Analyze disk latency in disk-iostat.txt
4. Examine network throughput in network-sar-dev.txt
5. Apply relevant tuning recommendations
EOF
    
    echo "Analysis complete! Summary available at: $REPORT_DIR/summary.txt"
}

# Check for required tools
check_requirements() {
    local required_tools=("mpstat" "vmstat" "iostat" "sar")
    local missing_tools=()
    
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        echo "Missing required tools: ${missing_tools[*]}"
        echo "Install sysstat package: sudo apt-get install sysstat"
        exit 1
    fi
}

# Run checks and main
check_requirements
main
```

## Best Practices

### 1. Performance Analysis Workflow
```bash
# 1. Establish baseline performance
baseline_capture() {
    local duration=3600  # 1 hour
    sar -A -o /var/log/sar/baseline-$(date +%Y%m%d).sar $duration
}

# 2. Identify bottlenecks using USE method
use_method_check() {
    echo "=== CPU ==="
    echo "Utilization:"
    mpstat 1 1 | tail -1 | awk '{print 100-$NF"%"}'
    echo "Saturation:"
    uptime | awk '{print "Load average: " $10 $11 $12}'
    echo "Errors:"
    dmesg | grep -i "cpu\|processor" | tail -5
    
    echo -e "\n=== Memory ==="
    echo "Utilization:"
    free | awk '/Mem:/ {printf "%.1f%%\n", $3/$2 * 100}'
    echo "Saturation:"
    vmstat 1 2 | tail -1 | awk '{print "Swap I/O: si=" $7 " so=" $8}'
    echo "Errors:"
    dmesg | grep -i "memory\|oom" | tail -5
    
    echo -e "\n=== Disk ==="
    echo "Utilization:"
    iostat -x 1 2 | grep -A1 avg-cpu
    echo "Saturation:"
    iostat -x 1 2 | awk '/^[a-z]/ && NR>7 {if ($9>20) print $1 ": await=" $9 "ms"}'
    echo "Errors:"
    dmesg | grep -i "error\|fail" | grep -v "ACPI" | tail -5
}
```

### 2. CPU Optimization
```bash
# CPU frequency scaling
# Set performance governor
for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
    echo performance > $cpu
done

# Disable CPU throttling
echo 0 > /sys/devices/system/cpu/intel_pstate/no_turbo

# CPU affinity for critical processes
# Bind process to specific CPUs
taskset -c 0-3 -p $PID

# Isolate CPUs for dedicated workloads
# Add to kernel boot parameters: isolcpus=2,3

# IRQ affinity
# Bind interrupts to specific CPUs
echo 2 > /proc/irq/24/smp_affinity

# NUMA optimization
# Run process on specific NUMA node
numactl --cpunodebind=0 --membind=0 myapp

# Check NUMA statistics
numastat -c
```

### 3. Memory Optimization
```bash
# Huge pages configuration
# Calculate huge pages needed (example: 8GB)
echo $((8*1024*1024/2048)) > /proc/sys/vm/nr_hugepages

# Transparent huge pages
echo always > /sys/kernel/mm/transparent_hugepage/enabled
echo always > /sys/kernel/mm/transparent_hugepage/defrag

# Memory tuning parameters
cat > /etc/sysctl.d/memory-tuning.conf <<EOF
# Swappiness (0-100, lower = less swap usage)
vm.swappiness = 10

# Cache pressure (default 100)
vm.vfs_cache_pressure = 50

# Dirty page settings
vm.dirty_background_ratio = 5
vm.dirty_ratio = 10
vm.dirty_expire_centisecs = 3000
vm.dirty_writeback_centisecs = 500

# OOM killer settings
vm.oom_kill_allocating_task = 1
vm.panic_on_oom = 0

# Shared memory
kernel.shmmax = 68719476736
kernel.shmall = 4294967296
EOF

sysctl -p /etc/sysctl.d/memory-tuning.conf
```

### 4. Disk I/O Optimization
```bash
# I/O scheduler selection
# For NVMe devices
echo none > /sys/block/nvme0n1/queue/scheduler

# For SSD
echo mq-deadline > /sys/block/sda/queue/scheduler

# For HDD
echo bfq > /sys/block/sda/queue/scheduler

# Queue depth and read-ahead
echo 512 > /sys/block/sda/queue/nr_requests
echo 256 > /sys/block/sda/queue/read_ahead_kb

# File system optimization
# Mount options for performance
mount -o noatime,nodiratime,nobarrier /dev/sda1 /data

# XFS tuning
xfs_admin -L "mydata" /dev/sda1
mount -o noatime,nodiratime,inode64,nobarrier /dev/sda1 /data

# ext4 tuning
tune2fs -o journal_data_writeback /dev/sda1
tune2fs -O ^has_journal /dev/sda1  # Disable journal (risky)

# I/O monitoring and analysis
iotop -oPa
dstat -D sda,sdb --disk-util
```

### 5. Network Optimization
```bash
# TCP tuning parameters
cat > /etc/sysctl.d/network-tuning.conf <<EOF
# Core network settings
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.core.rmem_default = 256000
net.core.wmem_default = 256000
net.core.netdev_max_backlog = 5000
net.core.somaxconn = 65535

# TCP settings
net.ipv4.tcp_rmem = 4096 87380 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_mtu_probing = 1
net.ipv4.tcp_fastopen = 3
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 10
net.ipv4.tcp_keepalive_time = 120
net.ipv4.tcp_keepalive_probes = 6
net.ipv4.tcp_keepalive_intvl = 10

# Connection tracking
net.netfilter.nf_conntrack_max = 1000000
net.ipv4.tcp_max_syn_backlog = 8192
EOF

sysctl -p /etc/sysctl.d/network-tuning.conf

# Network interface optimization
# Enable offloading features
ethtool -K eth0 tso on gso on gro on

# Increase ring buffer size
ethtool -G eth0 rx 4096 tx 4096

# CPU affinity for network interrupts
# Find network IRQs
grep eth0 /proc/interrupts
# Set affinity
echo 2 > /proc/irq/24/smp_affinity_list
```

## Common Commands and Operations

### Performance Monitoring Tools
```bash
# Real-time system overview
htop -d 10
glances
dstat -cdngy 1

# CPU analysis
mpstat -P ALL 1
pidstat -u -p $PID 1
perf top
perf record -g -p $PID
perf report

# Memory analysis
vmstat 1
free -m
slabtop
smem -tk
pmap -x $PID

# Disk I/O analysis
iostat -xz 1
iotop -o
ioping -c 10 /data
fio --name=randread --ioengine=libaio --rw=randread --bs=4k --numjobs=4 --time_based --runtime=60

# Network analysis
sar -n DEV 1
nethogs
iftop -i eth0
tcpdump -i eth0 -w capture.pcap
ss -s
nstat
```

### Performance Testing
```bash
# CPU benchmark
sysbench cpu --threads=4 run
stress-ng --cpu 4 --timeout 60s --metrics

# Memory benchmark
sysbench memory --threads=4 run
mbw 1024

# Disk benchmark
fio --name=seqwrite --ioengine=libaio --rw=write --bs=1m --numjobs=1 --size=10g --runtime=60
bonnie++ -d /data -s 16G -n 0 -f -b

# Network benchmark
iperf3 -s  # Server
iperf3 -c server_ip -t 60  # Client
netperf -H server_ip -t TCP_STREAM
```

### Profiling and Tracing
```bash
# System call tracing
strace -c -p $PID
strace -e trace=network -p $PID
strace -T -tt -o output.log command

# Library call tracing
ltrace -c -p $PID
ltrace -T -tt -o output.log command

# Kernel tracing
perf trace -p $PID
trace-cmd record -p function_graph
trace-cmd report

# eBPF tools
bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s %s\n", comm, str(args->filename)); }'
tcptop
biolatency
execsnoop
```

### Advanced Analysis
```bash
# Flame graphs
perf record -F 99 -a -g -- sleep 30
perf script > out.perf
flamegraph.pl out.perf > flamegraph.svg

# Cache analysis
perf stat -e cache-references,cache-misses command
pcm.x

# Lock contention
perf lock record command
perf lock report

# Scheduler analysis
perf sched record sleep 10
perf sched latency

# Power consumption
turbostat --interval 1
powertop
```

## Interview Tips

### Key Topics to Master
1. **Performance Methodologies**: USE, RED, golden signals
2. **Linux Internals**: Scheduler, memory management, I/O subsystem
3. **Monitoring Tools**: Top tools and their specific use cases
4. **Tuning Parameters**: Key sysctl settings and their impact
5. **Troubleshooting**: Systematic approach to performance issues
6. **Capacity Planning**: Predicting and preventing bottlenecks

### Common Interview Questions
1. "How would you troubleshoot a slow application?"
   - Start with the four golden signals
   - Use top-down analysis
   - Check system resources (CPU, memory, disk, network)
   - Application profiling
   - Review recent changes

2. "Explain Linux memory management"
   - Virtual memory and paging
   - Page cache and buffers
   - Memory allocation (malloc, mmap)
   - OOM killer behavior
   - Huge pages

3. "How do you optimize database performance?"
   - Query optimization
   - Index analysis
   - Buffer pool sizing
   - I/O pattern optimization
   - Connection pooling

4. "What's your approach to capacity planning?"
   - Baseline measurement
   - Trend analysis
   - Load testing
   - Resource forecasting
   - Scaling strategies

### Practical Scenarios
Be prepared to:
- Analyze performance data and identify bottlenecks
- Write monitoring scripts
- Explain tuning decisions
- Design performance tests
- Troubleshoot production issues

## Essential Resources

### Books
1. **"Systems Performance: Enterprise and the Cloud"** by Brendan Gregg
   - Comprehensive performance analysis
   - Modern methodologies and tools

2. **"BPF Performance Tools"** by Brendan Gregg
   - Advanced Linux observability
   - eBPF and modern tracing

3. **"Linux Performance Tuning"** by Michael Kerrisk
   - Practical tuning guide
   - Real-world examples

4. **"The Linux Programming Interface"** by Michael Kerrisk
   - Deep understanding of system calls
   - Performance implications

5. **"High Performance Linux Clusters"** by Joseph Sloan
   - Cluster performance optimization
   - Distributed system tuning

### Videos and Courses
1. **"Linux Performance Analysis"** - LinkedIn Learning
   - Practical performance analysis
   - Tool demonstrations

2. **Brendan Gregg's Performance Talks**
   - Conference presentations on YouTube
   - Latest performance techniques

3. **"Linux System Optimization"** - Pluralsight
   - Comprehensive optimization course
   - Hands-on exercises

4. **Performance Engineering Course - MIT**
   - Academic approach to performance
   - Algorithmic optimization

### Online Resources
1. **Brendan Gregg's Website**
   - Performance blog and resources
   - Tool documentation and examples

2. **Linux Performance Wiki**
   - Community-maintained resource
   - Tool comparisons and guides

3. **Red Hat Performance Tuning Guide**
   - Enterprise-focused tuning
   - Official documentation

4. **kernel.org Documentation**
   - Kernel parameter documentation
   - Subsystem guides

5. **LWN.net Performance Articles**
   - Deep technical articles
   - Kernel development insights

### Tools and Utilities
1. **perf**: Linux profiling framework
2. **BCC**: BPF Compiler Collection
3. **sysdig**: System exploration and troubleshooting
4. **Vector**: Performance monitoring framework
5. **Grafana + Prometheus**: Monitoring stack
6. **Intel VTune**: Advanced profiling tool

### Communities and Forums
1. **Linux Performance Facebook Group**: Active community
2. **Performance Matters Slack**: Discussion channel
3. **Stack Overflow [linux-performance]**: Q&A
4. **Reddit r/linuxperformance**: Community discussions
5. **Linux Kernel Mailing List**: Development discussions

### Benchmarking Suites
1. **Phoronix Test Suite**: Comprehensive benchmarking
2. **sysbench**: System benchmark tool
3. **fio**: Flexible I/O tester
4. **SPEC benchmarks**: Industry-standard benchmarks
5. **stress-ng**: Stress testing tool

Remember, performance tuning is both an art and a science. Always measure before and after changes, understand the trade-offs, and consider the entire system rather than optimizing in isolation. Document your changes and their rationale, as performance tuning decisions often need revisiting as workloads evolve.