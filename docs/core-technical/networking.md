---
title: Networking
sidebar_position: 3
---

# Networking for Platform Engineers

<GitHubButtons />
Master networking concepts and troubleshooting for platform engineering interviews.

## 🎯 Interview Focus Areas

### Most Asked Topics
1. **OSI Model & TCP/IP Stack** - Layer responsibilities and protocols
2. **DNS** - Resolution process, record types, troubleshooting
3. **Load Balancing** - Algorithms, health checks, implementations
4. **HTTP/HTTPS** - Headers, methods, SSL/TLS, HTTP/2
5. **Container Networking** - Bridge, overlay, service mesh

## OSI Model & TCP/IP Stack

### OSI Model Layers

```
7. Application   - HTTP, HTTPS, SSH, FTP
6. Presentation  - SSL/TLS, Compression
5. Session       - NetBIOS, SQL
4. Transport     - TCP, UDP
3. Network       - IP, ICMP, ARP
2. Data Link     - Ethernet, WiFi
1. Physical      - Cables, Hubs
```

### TCP/IP Model (What's Actually Used)

```
4. Application   - HTTP, DNS, SSH
3. Transport     - TCP, UDP
2. Internet      - IP, ICMP, ARP
1. Link          - Ethernet, WiFi
```

### TCP vs UDP

| TCP | UDP |
|-----|-----|
| Connection-oriented | Connectionless |
| Reliable delivery | Best effort |
| Ordered packets | No ordering |
| Flow control | No flow control |
| Higher overhead | Lower overhead |
| HTTP, SSH, FTP | DNS, VoIP, Gaming |

## DNS Deep Dive

### DNS Resolution Process

```
1. Browser cache
2. OS cache (/etc/hosts)
3. Local DNS resolver
4. Root nameserver (.)
5. TLD nameserver (.com)
6. Authoritative nameserver
7. Response cached at each level
```

### DNS Record Types

```bash
A       - IPv4 address (192.168.1.1)
AAAA    - IPv6 address (2001:db8::1)
CNAME   - Canonical name (alias)
MX      - Mail exchange
TXT     - Text data (SPF, DKIM)
NS      - Nameserver
SOA     - Start of authority
PTR     - Reverse DNS
SRV     - Service record
```

### DNS Troubleshooting

```bash
# Basic lookups
dig google.com              # Detailed DNS query
dig +short google.com       # Just the answer
dig @8.8.8.8 google.com    # Query specific server
dig +trace google.com       # Full resolution path

# Record types
dig google.com MX          # Mail servers
dig -x 8.8.8.8            # Reverse lookup
dig google.com ANY        # All records

# Debugging
dig +norecurse google.com  # Non-recursive query
dig +tcp google.com        # Force TCP
host -v google.com         # Verbose output
nslookup -debug google.com # Debug mode

# DNS cache
systemd-resolve --flush-caches  # Clear systemd cache
nscd -i hosts                   # Clear nscd cache
```

## HTTP/HTTPS

### HTTP Methods

```
GET     - Retrieve resource
POST    - Submit data
PUT     - Update resource
DELETE  - Remove resource
HEAD    - Headers only
OPTIONS - Allowed methods
PATCH   - Partial update
```

### Important HTTP Headers

```bash
# Request headers
Host: example.com
User-Agent: Mozilla/5.0
Accept: application/json
Authorization: Bearer token
Content-Type: application/json
X-Forwarded-For: client-ip

# Response headers
Status: 200 OK
Content-Length: 1234
Cache-Control: max-age=3600
Set-Cookie: session=abc123
Location: /new-path (redirects)
```

### HTTPS/TLS

```bash
# TLS handshake process
1. Client Hello (supported ciphers)
2. Server Hello (chosen cipher)
3. Certificate exchange
4. Key exchange
5. Finished messages
6. Encrypted communication

# Test SSL/TLS
openssl s_client -connect example.com:443
curl -v https://example.com
nmap --script ssl-enum-ciphers -p 443 example.com

# Certificate inspection
openssl x509 -in cert.pem -text -noout
openssl s_client -showcerts -connect example.com:443
```

## Load Balancing

### Load Balancing Algorithms

```python
# Round Robin
servers = ['server1', 'server2', 'server3']
current = 0
def round_robin():
    global current
    server = servers[current]
    current = (current + 1) % len(servers)
    return server

# Least Connections
def least_connections():
    return min(servers, key=lambda s: s.active_connections)

# Weighted Round Robin
weights = {'server1': 5, 'server2': 3, 'server3': 2}

# IP Hash (Session Persistence)
def ip_hash(client_ip):
    hash_value = hash(client_ip)
    return servers[hash_value % len(servers)]
```

### Health Checks

```bash
# HTTP health check
curl -f http://server/health || echo "Server down"

# TCP health check
nc -zv server 80 || echo "Port closed"

# Custom health check script
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://server/health)
if [ $response -eq 200 ]; then
    exit 0  # Healthy
else
    exit 1  # Unhealthy
fi
```

### HAProxy Configuration Example

```
global
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend web_frontend
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    option httpchk GET /health
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
    server web3 192.168.1.12:80 check
```

## TCP/IP Networking

### TCP Connection States

```
LISTEN      - Waiting for connection
SYN-SENT    - Connection request sent
SYN-RECV    - Connection request received
ESTABLISHED - Connection active
FIN-WAIT-1  - Connection terminating
FIN-WAIT-2  - Connection terminating
TIME-WAIT   - Connection recently closed
CLOSE-WAIT  - Remote side closed
CLOSED      - Connection closed
```

### TCP Tuning

```bash
# Socket buffer sizes
sysctl net.core.rmem_max=134217728
sysctl net.core.wmem_max=134217728

# TCP specific
sysctl net.ipv4.tcp_rmem="4096 87380 134217728"
sysctl net.ipv4.tcp_wmem="4096 65536 134217728"

# Connection tracking
sysctl net.netfilter.nf_conntrack_max=1048576

# TCP keepalive
sysctl net.ipv4.tcp_keepalive_time=600
sysctl net.ipv4.tcp_keepalive_intvl=60
sysctl net.ipv4.tcp_keepalive_probes=3
```

## Network Troubleshooting

### Connection Debugging

```bash
# Check connectivity
ping -c 4 google.com          # Basic connectivity
ping -s 1472 -M do google.com # MTU discovery
traceroute google.com         # Path discovery
mtr google.com               # Combined ping/traceroute

# Port testing
telnet host 80               # Test TCP port
nc -zv host 80-90           # Port range scan
nmap -p 80,443 host         # Port scan

# Connection analysis
ss -tan                     # All TCP connections
ss -tulpn                   # Listening ports
netstat -an | grep ESTAB    # Established connections
lsof -i :80                # Process using port
```

### Packet Analysis

```bash
# Capture packets
tcpdump -i eth0 -w capture.pcap           # Save to file
tcpdump -i any port 80                    # HTTP traffic
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'  # SYN packets
tcpdump -i eth0 -A host 192.168.1.1      # ASCII output

# Analyze packets
tcpdump -r capture.pcap                   # Read file
tcpdump -r capture.pcap -c 10            # First 10 packets
tshark -r capture.pcap -Y "http"         # HTTP only

# Common filters
'host 192.168.1.1'                       # Specific host
'net 192.168.1.0/24'                     # Network range
'port 80 or port 443'                    # Multiple ports
'tcp[tcpflags] & (tcp-syn|tcp-fin) != 0' # SYN or FIN
```

## Container Networking

### Docker Networking Modes

```bash
# Bridge (default)
docker run --network bridge nginx
# - Containers on same bridge can communicate
# - NAT for external access

# Host
docker run --network host nginx
# - No network isolation
# - Uses host network directly

# None
docker run --network none nginx
# - No network access
# - Complete isolation

# Custom networks
docker network create mynet
docker run --network mynet nginx
```

### Kubernetes Networking

```yaml
# Service types
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP      # Internal only (default)
  # type: NodePort     # Expose on node port
  # type: LoadBalancer # Cloud load balancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-netpol
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 80
```

## Common Interview Questions

### Q1: "Explain what happens when you type google.com in a browser"

```
1. DNS Resolution
   - Check browser cache
   - Check OS cache
   - Query DNS resolver
   - Recursive DNS lookup

2. TCP Connection
   - Three-way handshake (SYN, SYN-ACK, ACK)
   - Establish TCP connection to port 443

3. TLS Handshake
   - Client hello
   - Server hello + certificate
   - Key exchange
   - Encrypted connection established

4. HTTP Request
   - Send GET / HTTP/1.1
   - Include headers (Host, User-Agent, etc.)

5. Server Processing
   - Web server receives request
   - Application processes request
   - Database queries if needed

6. HTTP Response
   - Status code (200 OK)
   - Headers (Content-Type, etc.)
   - HTML body

7. Browser Rendering
   - Parse HTML
   - Request additional resources (CSS, JS, images)
   - Render page
```

### Q2: "How do you troubleshoot slow network performance?"

```bash
# 1. Check basic connectivity
ping -c 10 destination    # Check packet loss
mtr destination          # Path analysis

# 2. Check bandwidth
iperf3 -s               # On server
iperf3 -c server        # On client

# 3. Check latency
ping -c 100 destination | tail -3  # Min/avg/max

# 4. Check DNS
time dig google.com     # DNS response time

# 5. Check TCP performance
ss -i                   # Socket statistics
netstat -s              # Protocol statistics

# 6. Check for errors
ip -s link show         # Interface statistics
ethtool -S eth0         # Driver statistics
```

### Q3: "How do you implement high availability?"

```
1. Load Balancer (Active-Passive or Active-Active)
   - Health checks
   - Failover mechanisms
   - Session persistence

2. Multiple Data Centers
   - Geographic distribution
   - DNS failover
   - Data replication

3. Network Redundancy
   - Multiple network paths
   - BGP for route redundancy
   - VRRP for gateway redundancy

4. Monitoring
   - Real-time health checks
   - Automated failover
   - Alert mechanisms
```

## iptables/netfilter

### Basic iptables

```bash
# List rules
iptables -L -n -v              # All chains
iptables -t nat -L -n -v       # NAT table
iptables -S                    # Rule specifications

# Common rules
# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT

# Drop all other input
iptables -A INPUT -j DROP

# NAT/Port forwarding
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

# Save rules
iptables-save > /etc/iptables/rules.v4
```

## Network Performance

### Bandwidth Testing

```bash
# iperf3 testing
iperf3 -s                    # Server mode
iperf3 -c server            # Basic test
iperf3 -c server -t 30      # 30-second test
iperf3 -c server -P 10      # 10 parallel streams
iperf3 -c server -R         # Reverse mode

# Network throughput
speedtest-cli               # Internet speed
curl -o /dev/null http://speedtest.tele2.net/1GB.zip
```

### Latency Analysis

```bash
# RTT measurement
ping -c 100 host | tail -3

# Jitter measurement
mtr -r -c 100 host

# Application latency
curl -w "DNS: %{time_namelookup}\nConnect: %{time_connect}\nTLS: %{time_appconnect}\nTotal: %{time_total}\n" -o /dev/null -s https://example.com
```

## Quick Reference

### Common Ports
```
20/21 - FTP
22    - SSH
23    - Telnet
25    - SMTP
53    - DNS
80    - HTTP
110   - POP3
143   - IMAP
443   - HTTPS
3306  - MySQL
5432  - PostgreSQL
6379  - Redis
8080  - HTTP Alt
9000  - PHP-FPM
```

### Useful Commands
```bash
# Quick checks
curl -I https://example.com         # HTTP headers only
dig +short example.com             # Quick DNS lookup
ss -tulpn | grep LISTEN           # Listening ports
ip route get 8.8.8.8              # Route to destination
arp -a                            # ARP table
```

## Resources

- 📚 [TCP/IP Illustrated](https://www.amazon.com/TCP-Illustrated-Volume-Implementation/dp/020163354X)
- 📖 [High Performance Browser Networking](https://hpbn.co/) - Free online
- 🎥 [Computer Networking Course](https://www.youtube.com/watch?v=qiQR5rTSshw)
- 🎓 [Cisco Networking Basics](https://www.cisco.com/c/en/us/solutions/small-business/resource-center/networking/networking-basics.html)

---

*Interview tip: When discussing networking, always consider security implications. Show awareness of encryption, authentication, and common attack vectors.*