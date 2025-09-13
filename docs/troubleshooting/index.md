---
title: Troubleshooting & Debugging Guide
sidebar_position: 1
---

# Troubleshooting & Debugging Guide for Platform Engineers

Production issues don't wait for convenient times. This guide covers systematic approaches to troubleshooting, essential tools, and real-world scenarios you'll face as a platform engineer.

## The Troubleshooting Mindset

### Systematic Approach

1. **Observe**: What are the symptoms?
2. **Orient**: What changed recently?
3. **Hypothesize**: What could cause this?
4. **Test**: Verify or eliminate hypotheses
5. **Act**: Implement fixes
6. **Monitor**: Ensure the fix works

### Golden Rules

- **Don't panic**: Stay calm and methodical
- **Preserve evidence**: Don't destroy logs or state
- **Document everything**: Future you will thank you
- **Know when to escalate**: Some issues need more eyes
- **Learn from incidents**: Every outage is a learning opportunity

## Essential Troubleshooting Tools

### System Level Tools

**Process and Resource Monitoring:**
```bash
# Real-time system overview
htop                    # Interactive process viewer
atop                    # Advanced system monitor
glances                 # Cross-platform monitoring

# Quick system health check
uptime                  # Load average
free -h                 # Memory usage
df -h                   # Disk usage
iostat -x 1            # I/O statistics
vmstat 1               # Virtual memory stats
```

**Network Troubleshooting:**
```bash
# Connection testing
ping -c 4 google.com
traceroute google.com
mtr google.com         # Combines ping and traceroute

# DNS debugging
dig example.com
nslookup example.com
host example.com

# Port and connection analysis
netstat -tulpn         # All listening ports
ss -tulpn              # Modern netstat replacement
lsof -i :80            # What's using port 80
nc -zv host 80         # Test port connectivity

# Packet analysis
tcpdump -i any -w capture.pcap
tcpdump -i eth0 host 10.0.0.1
tcpdump -i any port 443 -A    # Show ASCII
```

**Advanced Debugging Tools:**
```bash
# System call tracing
strace -p <pid>
strace -e trace=network command
strace -c command      # Summary statistics

# Library call tracing
ltrace command

# Kernel tracing
perf record -g command
perf report
bpftrace -e 'tracepoint:syscalls:sys_enter_open { printf("%s %s\n", comm, str(args->filename)); }'
```

**Resources:**
- 📖 [Linux Performance Tools](https://www.brendangregg.com/linuxperf.html)
- 🎥 [Debugging with strace](https://www.youtube.com/watch?v=2lKvHjM8R4A)
- 📚 [BPF Performance Tools](https://www.brendangregg.com/bpf-performance-tools-book.html)

### Container and Kubernetes Debugging

**Docker Troubleshooting:**
```bash
# Container inspection
docker inspect <container>
docker logs --tail 50 -f <container>
docker exec -it <container> /bin/bash

# Resource usage
docker stats
docker system df
docker system events

# Network debugging
docker network ls
docker network inspect bridge
docker port <container>
```

**Kubernetes Debugging:**
```bash
# Pod troubleshooting
kubectl describe pod <pod>
kubectl logs <pod> --previous
kubectl logs <pod> -c <container>
kubectl exec -it <pod> -- /bin/bash

# Events and resources
kubectl get events --sort-by='.lastTimestamp'
kubectl top nodes
kubectl top pods --all-namespaces

# Advanced debugging
kubectl debug node/<node> -it --image=ubuntu
kubectl run debug --image=nicolaka/netshoot -it --rm

# Cluster diagnostics
kubectl cluster-info dump --output-directory=/tmp/cluster-dump
kubectl get pods --all-namespaces -o wide
kubectl get svc --all-namespaces
```

**Resources:**
- 📖 [Kubernetes Troubleshooting Guide](https://kubernetes.io/docs/tasks/debug/)
- 🎥 [Kubernetes Debugging Techniques](https://www.youtube.com/watch?v=G8MxIDtjig4)
- 📚 [Kubernetes Patterns](https://www.oreilly.com/library/view/kubernetes-patterns/9781492050278/)

### Application Performance Monitoring

**APM Tools:**
```bash
# JVM applications
jstack <pid>           # Thread dump
jmap -heap <pid>       # Heap summary
jstat -gcutil <pid> 1  # GC statistics
jconsole               # GUI monitoring

# Python applications
py-spy record -o profile.svg --pid <pid>
python -m cProfile script.py
python -m trace --trace script.py

# Go applications
go tool pprof http://localhost:6060/debug/pprof/heap
go tool pprof http://localhost:6060/debug/pprof/profile
go tool trace trace.out
```

## Common Troubleshooting Scenarios

### Scenario 1: High CPU Usage

**Symptoms:**
- System slowness
- High load average
- Unresponsive applications

**Investigation Steps:**
```bash
# 1. Identify the culprit
top -H                 # Show threads
ps aux --sort=-cpu | head -10

# 2. Analyze the process
strace -p <pid> -c     # System call summary
perf top -p <pid>      # CPU profiling

# 3. Check for CPU throttling
cat /sys/fs/cgroup/cpu/cpu.stat | grep throttled

# 4. Thread analysis
ps -eLf | grep <pid>   # All threads
pstack <pid>           # Stack trace
```

**Common Causes:**
- Infinite loops
- Inefficient algorithms
- Garbage collection
- CPU limits/throttling

### Scenario 2: Memory Leak

**Symptoms:**
- Increasing memory usage
- OOM kills
- Swap usage increasing

**Investigation Steps:**
```bash
# 1. Memory overview
free -h
cat /proc/meminfo
vmstat 1

# 2. Find memory hogs
ps aux --sort=-rss | head -10
smem -rs rss -p        # Sorted by RSS

# 3. Process memory analysis
pmap -x <pid>
cat /proc/<pid>/status | grep Vm
cat /proc/<pid>/smaps

# 4. Heap analysis (Java example)
jmap -histo:live <pid>
jmap -dump:live,format=b,file=heap.bin <pid>
```

**Memory Leak Detection:**
```python
# Python memory profiling
from memory_profiler import profile

@profile
def memory_intensive_function():
    # Your code here
    pass

# Run with: python -m memory_profiler script.py
```

### Scenario 3: Disk I/O Issues

**Symptoms:**
- Slow application response
- High I/O wait
- Disk errors in logs

**Investigation Steps:**
```bash
# 1. I/O statistics
iostat -x 1
iotop -o
dstat -d --disk-util

# 2. File system usage
df -h
df -i                  # Inode usage
du -sh /* | sort -hr

# 3. Find I/O intensive processes
pidstat -d 1
iotop -b -o

# 4. Trace I/O operations
blktrace -d /dev/sda -o trace
blkparse trace
```

### Scenario 4: Network Connectivity Issues

**Symptoms:**
- Connection timeouts
- Intermittent failures
- Slow response times

**Investigation Steps:**
```bash
# 1. Basic connectivity
ping -c 10 target.com
mtr --report target.com

# 2. DNS resolution
dig target.com
systemd-resolve --status

# 3. Connection analysis
ss -tan | grep ESTABLISHED
netstat -s             # Protocol statistics

# 4. Packet loss detection
ping -f -c 1000 target.com
iperf3 -c target.com

# 5. Firewall and routing
iptables -L -n -v
ip route show
traceroute -T -p 443 target.com
```

### Scenario 5: Database Performance Issues

**Symptoms:**
- Slow queries
- Connection pool exhaustion
- Lock contention

**PostgreSQL Troubleshooting:**
```sql
-- Active queries
SELECT pid, age(clock_timestamp(), query_start), usename, query 
FROM pg_stat_activity 
WHERE state != 'idle' 
ORDER BY query_start DESC;

-- Lock analysis
SELECT blocked_locks.pid AS blocked_pid,
       blocked_activity.usename AS blocked_user,
       blocking_locks.pid AS blocking_pid,
       blocking_activity.usename AS blocking_user
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- Table bloat
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

**MySQL Troubleshooting:**
```sql
-- Active processes
SHOW FULL PROCESSLIST;

-- Lock information
SELECT * FROM information_schema.innodb_locks;
SELECT * FROM information_schema.innodb_lock_waits;

-- Query analysis
EXPLAIN SELECT * FROM table WHERE condition;
SHOW STATUS LIKE 'Handler_%';
```

## Production Debugging Strategies

### Safe Debugging in Production

**1. Read-Only First:**
- Start with non-intrusive commands
- Avoid modifying state
- Use read replicas when possible

**2. Circuit Breakers:**
```python
# Implement safety mechanisms
import signal
import sys

def timeout_handler(signum, frame):
    print("Debug operation timed out")
    sys.exit(1)

# Set 5-minute timeout for debug operations
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(300)
```

**3. Canary Debugging:**
- Test fixes on one instance first
- Monitor impact before full rollout
- Have rollback plan ready

### Distributed Tracing

**OpenTelemetry Setup:**
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Use in code
with tracer.start_as_current_span("process_request"):
    # Your code here
    pass
```

**Resources:**
- 📖 [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- 🎥 [Distributed Tracing Explained](https://www.youtube.com/watch?v=G8MxIDtjig4)
- 📚 [Distributed Tracing in Practice](https://www.oreilly.com/library/view/distributed-tracing-in/9781492056621/)

## Log Analysis and Correlation

### Centralized Logging

**Log Aggregation Pipeline:**
```yaml
# Filebeat configuration
filebeat.inputs:
- type: container
  paths:
    - '/var/lib/docker/containers/*/*.log'
  processors:
    - add_kubernetes_metadata:
        host: ${NODE_NAME}
        matchers:
        - logs_path:
            logs_path: "/var/lib/docker/containers/"

output.elasticsearch:
  hosts: ['${ELASTICSEARCH_HOST:elasticsearch}:${ELASTICSEARCH_PORT:9200}']
  index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"
```

**Log Correlation Queries:**
```bash
# Elasticsearch query for error spike
curl -X GET "localhost:9200/logs-*/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        {"match": {"level": "ERROR"}},
        {"range": {"@timestamp": {"gte": "now-1h"}}}
      ]
    }
  },
  "aggs": {
    "errors_over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "interval": "5m"
      }
    }
  }
}'
```

### Pattern Recognition

**Common Log Patterns:**
```python
# Log anomaly detection
import re
from collections import Counter

def analyze_logs(log_file):
    error_patterns = Counter()
    
    patterns = [
        (r'OutOfMemoryError', 'OOM'),
        (r'Connection refused', 'Connection Error'),
        (r'Timeout|timed out', 'Timeout'),
        (r'NullPointerException', 'NPE'),
        (r'database is locked', 'DB Lock')
    ]
    
    with open(log_file, 'r') as f:
        for line in f:
            for pattern, category in patterns:
                if re.search(pattern, line, re.I):
                    error_patterns[category] += 1
    
    return error_patterns.most_common(10)
```

## Interview Scenarios

### Common Troubleshooting Questions

1. **"How would you debug a memory leak in production?"**
   - Start with monitoring metrics
   - Use heap dumps carefully
   - Analyze with minimal impact
   - Have rollback strategy

2. **"A service is experiencing intermittent timeouts. How do you investigate?"**
   - Check network path
   - Analyze connection pools
   - Review timeout settings
   - Look for patterns

3. **"The database is slow. What's your approach?"**
   - Check slow query logs
   - Analyze execution plans
   - Review indexes
   - Monitor connections

4. **"How do you handle cascading failures?"**
   - Circuit breakers
   - Bulkheads
   - Timeout tuning
   - Graceful degradation

### Hands-On Scenarios

**Scenario Setup for Practice:**
```bash
# Create a problematic container
docker run -d --name buggy-app \
  --memory="50m" \
  --cpus="0.5" \
  your/buggy-app:latest

# Introduce network latency
tc qdisc add dev eth0 root netem delay 100ms

# Simulate disk pressure
stress-ng --io 4 --timeout 60s

# Generate load
ab -n 10000 -c 100 http://localhost:8080/
```

## Building a Troubleshooting Toolkit

### Essential Scripts

**System Health Check:**
```bash
#!/bin/bash
# health_check.sh - Quick system health assessment

echo "=== System Health Check ==="
echo "Date: $(date)"
echo

echo "--- Load Average ---"
uptime

echo -e "\n--- Memory Usage ---"
free -h

echo -e "\n--- Disk Usage ---"
df -h | grep -vE '^Filesystem|tmpfs|cdrom'

echo -e "\n--- Top CPU Processes ---"
ps aux --sort=-cpu | head -5

echo -e "\n--- Network Connections ---"
ss -tan | grep ESTAB | wc -l
echo "Established connections: $(ss -tan | grep ESTAB | wc -l)"

echo -e "\n--- Recent Errors ---"
journalctl -p err -n 10 --no-pager
```

### Documentation Templates

**Incident Report Template:**
```markdown
# Incident Report: [Title]

**Date**: [YYYY-MM-DD]
**Duration**: [Start time - End time]
**Severity**: [P1/P2/P3]
**Services Affected**: [List services]

## Summary
[Brief description of the incident]

## Timeline
- HH:MM - [Event description]
- HH:MM - [Event description]

## Root Cause
[Detailed explanation of what caused the incident]

## Resolution
[Steps taken to resolve the issue]

## Impact
- [Customer impact]
- [Business impact]

## Lessons Learned
1. [What went well]
2. [What could be improved]

## Action Items
- [ ] [Action item with owner]
- [ ] [Action item with owner]
```

## Resources for Continuous Learning

### Books
- 📚 [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) - Google
- 📚 [Debugging: The 9 Indispensable Rules](https://www.amazon.com/Debugging-Indispensable-Software-Hardware-Problems/dp/0814474578) - David Agans
- 📚 [Effective Debugging](https://www.amazon.com/Effective-Debugging-Specific-Software-Engineering/dp/0134394798) - Diomidis Spinellis

### Online Resources
- 📖 [Brendan Gregg's Performance Site](https://www.brendangregg.com/)
- 🎥 [SREcon Talks](https://www.usenix.org/conferences/byname/925)
- 📖 [Production Readiness Checklist](https://gruntwork.io/devops-checklist/)
- 🎮 [Troubleshooting Scenarios](https://sadservers.com/)

### Tools to Master
- **Monitoring**: Prometheus, Grafana, Datadog
- **Tracing**: Jaeger, Zipkin, AWS X-Ray
- **Logging**: ELK Stack, Fluentd, Splunk
- **Profiling**: pprof, Java Flight Recorder, perf

Remember: The best troubleshooters combine systematic thinking, deep technical knowledge, and excellent communication skills. Every incident is an opportunity to improve your systems and processes.