---
title: "Network Troubleshooting Tools"
description: "Master network troubleshooting with essential tools, techniques, and methodologies"
---

# Network Troubleshooting Tools

## Introduction

Network troubleshooting is a critical skill for platform engineers. Understanding how to diagnose connectivity issues, analyze packet flows, and identify performance bottlenecks ensures reliable infrastructure operation. This guide covers essential tools and methodologies for effective network troubleshooting.

## Core Concepts

### OSI Model Troubleshooting
```
Layer 7 - Application  | HTTP errors, API issues
Layer 6 - Presentation | Encryption, compression
Layer 5 - Session      | Session establishment
Layer 4 - Transport    | TCP/UDP port issues
Layer 3 - Network      | IP routing, ICMP
Layer 2 - Data Link    | ARP, switching
Layer 1 - Physical     | Cable, hardware
```

### Troubleshooting Methodology
1. **Define the Problem**: Gather symptoms and scope
2. **Gather Information**: Collect logs, metrics, traces
3. **Analyze**: Identify patterns and anomalies
4. **Isolate**: Narrow down the root cause
5. **Test**: Verify hypothesis
6. **Implement**: Apply fix
7. **Document**: Record solution for future reference

### Common Network Issues
- **Connectivity Problems**: Can't reach destination
- **Performance Issues**: Slow response times, high latency
- **Packet Loss**: Dropped packets, retransmissions
- **DNS Resolution**: Name resolution failures
- **Routing Issues**: Incorrect routes, loops
- **Firewall Blocks**: Security rules preventing access

## Common Use Cases

### 1. Diagnosing Connectivity Issues
```bash
# Basic connectivity test
ping -c 4 google.com
ping -c 4 8.8.8.8

# Extended ping with options
ping -c 10 -i 0.2 -s 1000 192.168.1.1
# -c: count
# -i: interval
# -s: packet size

# IPv6 connectivity
ping6 -c 4 2001:4860:4860::8888
ping6 -c 4 google.com

# Continuous ping with timestamp
ping google.com | while read pong; do echo "$(date): $pong"; done

# Ping sweep for network discovery
for i in {1..254}; do
  ping -c 1 -W 1 192.168.1.$i &> /dev/null && echo "192.168.1.$i is up" &
done
wait
```

### 2. Path and Routing Analysis
```bash
# Traceroute with different protocols
traceroute google.com           # UDP (default)
traceroute -I google.com        # ICMP
traceroute -T google.com        # TCP
traceroute -p 443 -T google.com # TCP port 443

# MTR (My TraceRoute) - combines ping and traceroute
mtr --report --report-cycles 100 google.com
mtr --tcp --port 443 google.com

# Show routing table
ip route show
netstat -rn
route -n

# Detailed route information
ip route get 8.8.8.8
```

### 3. Port and Service Testing
```bash
# Test specific port connectivity
nc -zv google.com 80    # Test HTTP
nc -zv google.com 443   # Test HTTPS
nc -zv 192.168.1.1 22   # Test SSH

# Port scanning with timeout
nc -zv -w 3 192.168.1.1 1-1000 2>&1 | grep succeeded

# Test with telnet
telnet google.com 80
# Then type: GET / HTTP/1.0 (press Enter twice)

# Advanced port testing with nmap
nmap -p 80,443 google.com
nmap -p 1-65535 -T4 192.168.1.1  # Full port scan
nmap -sV -p 22,80,443 192.168.1.0/24  # Service version detection

# UDP port testing
nc -u -zv 192.168.1.1 53  # DNS
nmap -sU -p 123 192.168.1.1  # NTP
```

## Getting Started Examples

### Network Interface Analysis
```bash
# Show all network interfaces
ip addr show
ifconfig -a

# Interface statistics
ip -s link show
netstat -i

# Monitor interface traffic in real-time
iftop -i eth0
nload eth0
bmon

# Check interface errors and drops
ip -s -s link show eth0
ethtool -S eth0

# Test network speed between hosts
# Server side:
iperf3 -s

# Client side:
iperf3 -c server_ip -t 30 -P 4
# -t: time in seconds
# -P: parallel streams
```

### DNS Troubleshooting
```bash
# Basic DNS queries
nslookup google.com
host google.com
dig google.com

# Detailed DNS query with trace
dig +trace google.com

# Query specific DNS server
dig @8.8.8.8 google.com
dig @1.1.1.1 google.com

# Check all record types
dig google.com ANY

# Reverse DNS lookup
dig -x 8.8.8.8

# Test DNS response time
time dig google.com
for i in {1..10}; do time dig @8.8.8.8 google.com | grep "Query time"; done

# Check DNS configuration
cat /etc/resolv.conf
systemd-resolve --status
```

### Packet Capture and Analysis
```bash
# Basic packet capture
sudo tcpdump -i eth0
sudo tcpdump -i any  # All interfaces

# Capture with filters
sudo tcpdump -i eth0 host 192.168.1.1
sudo tcpdump -i eth0 port 80
sudo tcpdump -i eth0 'tcp port 443'

# Save to file for analysis
sudo tcpdump -i eth0 -w capture.pcap -c 1000

# Read from file
tcpdump -r capture.pcap

# Advanced filters
# HTTP traffic
sudo tcpdump -i eth0 -s 0 -A 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'

# TCP SYN packets
sudo tcpdump -i eth0 'tcp[tcpflags] & (tcp-syn) != 0'

# DNS queries
sudo tcpdump -i eth0 -n port 53

# Wireshark from command line
tshark -i eth0 -f "tcp port 443"
tshark -r capture.pcap -Y "http.request"
```

## Best Practices

### 1. Systematic Approach
```bash
#!/bin/bash
# Network troubleshooting script

HOSTS="google.com 8.8.8.8 192.168.1.1"
PORTS="80 443 22"

echo "=== Network Troubleshooting Report ==="
echo "Date: $(date)"
echo

# Check interfaces
echo "=== Network Interfaces ==="
ip addr show | grep -E "^[0-9]+:|inet "
echo

# Check routing
echo "=== Routing Table ==="
ip route show
echo

# Check DNS
echo "=== DNS Configuration ==="
cat /etc/resolv.conf
echo

# Test connectivity
echo "=== Connectivity Tests ==="
for host in $HOSTS; do
    echo -n "Ping $host: "
    if ping -c 1 -W 2 $host &> /dev/null; then
        echo "OK"
    else
        echo "FAILED"
    fi
done
echo

# Test ports
echo "=== Port Tests ==="
for host in google.com 192.168.1.1; do
    for port in $PORTS; do
        echo -n "Test $host:$port: "
        if nc -zv -w 2 $host $port &> /dev/null; then
            echo "OPEN"
        else
            echo "CLOSED/FILTERED"
        fi
    done
done
```

### 2. Performance Analysis
```bash
# Network latency testing
ping -c 100 -i 0.2 google.com | tee ping_stats.txt
grep -oP '(?<=time=)[0-9.]+' ping_stats.txt | \
    awk '{sum+=$1; sumsq+=$1*$1} END {print "Mean:", sum/NR, "StdDev:", sqrt(sumsq/NR - (sum/NR)^2)}'

# Bandwidth testing script
#!/bin/bash
echo "Testing bandwidth to multiple servers..."
servers=("speedtest.atlanta.linode.com" "speedtest.london.linode.com" "speedtest.tokyo2.linode.com")

for server in "${servers[@]}"; do
    echo "Testing $server..."
    curl -o /dev/null -w "Download Speed: %{speed_download} bytes/sec\n" \
         http://$server/100MB-atlanta.bin
done

# TCP connection analysis
ss -tan state established
ss -tan state time-wait | wc -l
```

### 3. Automated Monitoring
```python
#!/usr/bin/env python3
import subprocess
import time
import json
from datetime import datetime

def ping_test(host, count=4):
    """Perform ping test and return statistics"""
    try:
        result = subprocess.run(
            ['ping', '-c', str(count), host],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Parse ping statistics
            lines = result.stdout.split('\n')
            for line in lines:
                if 'min/avg/max' in line:
                    stats = line.split('=')[1].strip().split('/')
                    return {
                        'host': host,
                        'status': 'up',
                        'min': float(stats[0]),
                        'avg': float(stats[1]),
                        'max': float(stats[2]),
                        'timestamp': datetime.now().isoformat()
                    }
        
        return {'host': host, 'status': 'down', 'timestamp': datetime.now().isoformat()}
    
    except subprocess.TimeoutExpired:
        return {'host': host, 'status': 'timeout', 'timestamp': datetime.now().isoformat()}

def continuous_monitor(hosts, interval=60):
    """Continuously monitor hosts"""
    while True:
        results = []
        for host in hosts:
            result = ping_test(host)
            results.append(result)
            print(f"{result['timestamp']}: {host} - {result['status']}")
            
            if result['status'] == 'up':
                print(f"  Latency: {result['avg']:.2f}ms")
        
        # Log results
        with open('network_monitor.json', 'a') as f:
            json.dump(results, f)
            f.write('\n')
        
        time.sleep(interval)

if __name__ == '__main__':
    hosts = ['google.com', '8.8.8.8', '192.168.1.1']
    continuous_monitor(hosts)
```

## Commands and Configuration

### Essential Network Commands
```bash
# ARP table management
arp -a                    # Show ARP table
arp -d 192.168.1.100     # Delete ARP entry
ip neigh show            # Modern ARP display

# Network statistics
netstat -tuln            # Listening ports
netstat -tan             # All connections
ss -tuln                 # Modern alternative to netstat
ss -s                    # Socket statistics

# Connection tracking
conntrack -L             # List tracked connections
conntrack -S             # Statistics

# Process to port mapping
lsof -i :80              # What's using port 80
lsof -i @192.168.1.1     # Connections to specific IP
fuser 80/tcp             # Process using port 80
ss -tlnp                 # Listening ports with process

# Network namespace debugging
ip netns list            # List namespaces
ip netns exec ns1 ip addr show
ip netns exec ns1 ping 8.8.8.8
```

### Advanced Troubleshooting Tools
```bash
# MTU discovery
ping -M do -s 1472 google.com  # Don't fragment, 1500-28=1472

# TCP analysis with tcptrace
tcpdump -w trace.pcap
tcptrace trace.pcap

# HTTP debugging
curl -v https://example.com
curl -I https://example.com  # Headers only
curl -w "@curl-format.txt" -o /dev/null -s https://example.com

# curl-format.txt content:
# time_namelookup:  %{time_namelookup}\n
# time_connect:  %{time_connect}\n
# time_appconnect:  %{time_appconnect}\n
# time_pretransfer:  %{time_pretransfer}\n
# time_redirect:  %{time_redirect}\n
# time_starttransfer:  %{time_starttransfer}\n
# time_total:  %{time_total}\n

# SSL/TLS debugging
openssl s_client -connect example.com:443
openssl s_client -showcerts -servername example.com -connect example.com:443

# Network performance tuning check
sysctl net.ipv4.tcp_congestion_control
sysctl net.core.rmem_max
sysctl net.core.wmem_max
```

### Container Network Debugging
```bash
# Docker network troubleshooting
docker network ls
docker network inspect bridge
docker port container_name

# Enter container network namespace
docker exec -it container_name /bin/sh
nsenter -t $(docker inspect -f '{{.State.Pid}}' container_name) -n ip addr

# Kubernetes network debugging
kubectl get svc
kubectl get endpoints
kubectl describe svc service_name

# Test from within pod
kubectl exec -it pod_name -- nslookup kubernetes.default
kubectl exec -it pod_name -- curl service_name

# Network policies
kubectl get networkpolicies
kubectl describe networkpolicy policy_name
```

## Interview Tips

### Key Questions to Prepare
1. **OSI model troubleshooting**: Which layer would you start with for specific issues?
2. **TCP vs UDP**: When to use each, troubleshooting differences
3. **Packet capture analysis**: How to filter and interpret captures
4. **Network performance**: Identify and resolve bottlenecks
5. **Security implications**: Firewall rules, port scanning ethics

### Practical Scenarios
- "Users report intermittent connectivity to a web service"
- "Application experiencing high latency to database"
- "Diagnose why certain clients can't resolve DNS"
- "Debug container networking issues in Kubernetes"
- "Investigate packet loss between data centers"

### Common Pitfalls
- Starting with complex tools instead of basics (ping, traceroute)
- Not checking physical layer (cables, interfaces)
- Ignoring MTU issues in tunneled networks
- Forgetting about DNS as a common failure point
- Not documenting the troubleshooting process

## Resources

### Official Documentation
- [tcpdump Manual](https://www.tcpdump.org/manpages/tcpdump.1.html)
- [Wireshark User Guide](https://www.wireshark.org/docs/wsug_html/)
- [iproute2 Documentation](https://wiki.linuxfoundation.org/networking/iproute2)
- [nmap Reference Guide](https://nmap.org/book/man.html)

### Books and Guides
- "Network Warrior" by Gary A. Donahue
- "Practical Packet Analysis" by Chris Sanders
- "TCP/IP Illustrated" by W. Richard Stevens
- [Brendan Gregg's Network Performance](http://www.brendangregg.com/linuxperf.html)

### Tools and Utilities
- [iperf3 - Network Bandwidth Testing](https://iperf.fr/)
- [mtr - Network Diagnostic Tool](https://github.com/traviscross/mtr)
- [netcat - Network Swiss Army Knife](http://netcat.sourceforge.net/)
- [tcpflow - TCP Flow Recorder](https://github.com/simsong/tcpflow)

### Online Resources
- [PacketLife Capture Library](https://packetlife.net/library/captures/)
- [Network Troubleshooting Tools](https://github.com/jadi/nettools)
- [SANS TCP/IP Cheat Sheet](https://www.sans.org/security-resources/tcpip.pdf)
- [Cisco Troubleshooting Methodology](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/10566-21.html)

### Training and Practice
- [TryHackMe Network Fundamentals](https://tryhackme.com/module/network-fundamentals)
- [Cybrary Network+](https://www.cybrary.it/course/comptia-network-plus/)
- [Linux Academy Networking](https://linuxacademy.com/course/linux-networking/)
- [Wireshark Tutorial](https://www.wireshark.org/docs/wsug_html_chunked/ChapterIntroduction.html)

### Community Forums
- [Server Fault Networking](https://serverfault.com/questions/tagged/networking)
- [r/networking Reddit](https://www.reddit.com/r/networking/)
- [Network Engineering Stack Exchange](https://networkengineering.stackexchange.com/)
- [Packet Pushers Community](https://packetpushers.net/)