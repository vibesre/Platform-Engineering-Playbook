# VPN Technologies

## Overview

Virtual Private Networks (VPNs) create secure, encrypted connections over public networks, enabling remote access to private resources and secure communication between distributed systems.

## Core Technologies

### WireGuard

Modern, lightweight VPN protocol focusing on simplicity and performance.

#### Key Features
- Minimal codebase (~4,000 lines)
- State-of-the-art cryptography
- UDP-based protocol
- Built into Linux kernel 5.6+
- Peer-to-peer architecture

#### Configuration Example

**Server Configuration (`/etc/wireguard/wg0.conf`)**:
```ini
[Interface]
# Server private key
PrivateKey = kBbKUhFw2P8XpFpGn1xGqPZ3Y3mL5Tz8nR4qN9Y5tGo=
# Server IP in VPN subnet
Address = 10.0.0.1/24
# Listen port
ListenPort = 51820
# Post-up rules for NAT
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Client public key
PublicKey = H6StMJOYIjfqTDi6Uc8AL0YUO/ehqQSJ7+8DTLXI1ks=
# Allowed IPs for this peer
AllowedIPs = 10.0.0.2/32
```

**Client Configuration**:
```ini
[Interface]
# Client private key
PrivateKey = aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890ABCDEF=
# Client IP in VPN subnet
Address = 10.0.0.2/24
# DNS server (optional)
DNS = 1.1.1.1

[Peer]
# Server public key
PublicKey = xTIlBM5d0+LthW5Y3uhB0IWJ5eAxJXkFnTvMdx9ysFo=
# Server endpoint
Endpoint = vpn.example.com:51820
# Route all traffic through VPN
AllowedIPs = 0.0.0.0/0
# Keep connection alive
PersistentKeepalive = 25
```

### OpenVPN

Mature, highly configurable SSL/TLS-based VPN solution.

#### Key Features
- SSL/TLS encryption
- TCP/UDP transport options
- Certificate-based authentication
- Push/pull configuration
- Multi-platform support

#### Configuration Example

**Server Configuration (`/etc/openvpn/server.conf`)**:
```conf
# Network settings
port 1194
proto udp
dev tun

# Certificate settings
ca ca.crt
cert server.crt
key server.key
dh dh2048.pem
tls-auth ta.key 0

# Network topology
server 10.8.0.0 255.255.255.0
topology subnet

# Push routes to client
push "route 192.168.1.0 255.255.255.0"
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"

# Connection settings
keepalive 10 120
cipher AES-256-GCM
auth SHA256
persist-key
persist-tun

# User privilege downgrade
user nobody
group nogroup

# Logging
status /var/log/openvpn/openvpn-status.log
log-append /var/log/openvpn/openvpn.log
verb 3

# Client configuration directory
client-config-dir /etc/openvpn/ccd

# Enable compression
compress lz4-v2
push "compress lz4-v2"
```

**Client Configuration**:
```conf
client
dev tun
proto udp

remote vpn.example.com 1194
resolv-retry infinite
nobind

# Certificates
ca ca.crt
cert client.crt
key client.key
tls-auth ta.key 1

# Security
cipher AES-256-GCM
auth SHA256
persist-key
persist-tun

# Compression
compress lz4-v2

# Logging
verb 3
```

### IPSec

Industry-standard protocol suite for secure IP communications.

#### Key Features
- Kernel-level implementation
- IKEv1/IKEv2 key exchange
- ESP/AH protocols
- Perfect forward secrecy
- Multiple cipher support

#### StrongSwan Configuration Example

**Server Configuration (`/etc/ipsec.conf`)**:
```conf
config setup
    charondebug="ike 2, knl 2, cfg 2, net 2"
    uniqueids=no

conn %default
    keyexchange=ikev2
    ike=aes256-sha256-modp2048!
    esp=aes256-sha256!
    dpdaction=clear
    dpddelay=60s
    dpdtimeout=300s
    authby=psk
    auto=add
    rekey=no
    reauth=no
    fragmentation=yes
    forceencaps=yes

conn roadwarrior
    left=%any
    leftid=@vpn.example.com
    leftsubnet=0.0.0.0/0
    leftfirewall=yes
    right=%any
    rightid=%any
    rightsubnet=10.10.0.0/24
    rightsourceip=10.10.0.0/24
    rightdns=8.8.8.8,8.8.4.4
```

**Secrets File (`/etc/ipsec.secrets`)**:
```
# PSK for all connections
: PSK "your-secure-pre-shared-key-here"

# Certificate-based authentication
: RSA server-key.pem

# EAP authentication
user1 : EAP "password123"
user2 : EAP "password456"
```

## Best Practices

### Security Considerations

1. **Strong Encryption**
   ```yaml
   wireguard:
     crypto:
       - ChaCha20Poly1305
       - Curve25519
       - BLAKE2s
   
   openvpn:
     cipher: AES-256-GCM
     auth: SHA256
     tls-version-min: "1.2"
   
   ipsec:
     ike: aes256-sha256-modp2048
     esp: aes256-sha256
   ```

2. **Key Management**
   ```bash
   # Generate WireGuard keys
   wg genkey | tee privatekey | wg pubkey > publickey
   
   # Generate OpenVPN certificates
   ./easyrsa init-pki
   ./easyrsa build-ca
   ./easyrsa gen-req server nopass
   ./easyrsa sign-req server server
   
   # Generate IPSec certificates
   ipsec pki --gen --type rsa --size 4096 --outform pem > ca-key.pem
   ipsec pki --self --ca --lifetime 3650 --in ca-key.pem \
       --type rsa --dn "CN=VPN CA" --outform pem > ca-cert.pem
   ```

### Performance Optimization

1. **WireGuard Optimization**
   ```bash
   # Enable GSO/GRO
   ethtool -K wg0 gso on
   ethtool -K wg0 gro on
   
   # CPU affinity for crypto
   echo 2 > /proc/irq/24/smp_affinity
   
   # Increase buffer sizes
   sysctl -w net.core.rmem_max=134217728
   sysctl -w net.core.wmem_max=134217728
   ```

2. **OpenVPN Optimization**
   ```conf
   # Server optimization
   sndbuf 524288
   rcvbuf 524288
   push "sndbuf 524288"
   push "rcvbuf 524288"
   
   # Fast I/O
   fast-io
   
   # Multithreading (commercial version)
   threads 4
   ```

### High Availability

1. **Load Balancing Setup**
   ```yaml
   # HAProxy configuration for OpenVPN
   frontend vpn_frontend
     bind *:1194
     mode tcp
     default_backend vpn_servers
   
   backend vpn_servers
     mode tcp
     balance roundrobin
     server vpn1 10.0.1.10:1194 check
     server vpn2 10.0.1.11:1194 check
   ```

2. **Failover Configuration**
   ```bash
   # Keepalived for VIP management
   vrrp_instance VPN_VIP {
     state MASTER
     interface eth0
     virtual_router_id 51
     priority 100
     advert_int 1
     
     authentication {
       auth_type PASS
       auth_pass vpn_secret
     }
     
     virtual_ipaddress {
       192.168.1.100
     }
   }
   ```

## Common Patterns

### Site-to-Site VPN

```conf
# WireGuard site-to-site
[Interface]
PrivateKey = <site-a-private-key>
Address = 10.254.0.1/30
ListenPort = 51820

[Peer]
PublicKey = <site-b-public-key>
Endpoint = site-b.example.com:51820
AllowedIPs = 10.254.0.2/32, 192.168.2.0/24
PersistentKeepalive = 25
```

### Split Tunnel Configuration

```conf
# OpenVPN split tunnel
push "route 10.0.0.0 255.0.0.0"
push "route 172.16.0.0 255.240.0.0"
# Don't route all traffic through VPN
# push "redirect-gateway def1"
```

### Multi-Factor Authentication

```conf
# OpenVPN with LDAP + OTP
plugin /usr/lib/openvpn/openvpn-auth-pam.so "openvpn-mfa"
client-cert-not-required
username-as-common-name

# PAM configuration (/etc/pam.d/openvpn-mfa)
auth required pam_google_authenticator.so
auth required pam_ldap.so
account required pam_ldap.so
```

## Monitoring and Troubleshooting

### Monitoring Setup

1. **Prometheus Metrics**
   ```yaml
   # WireGuard exporter
   - job_name: 'wireguard'
     static_configs:
       - targets: ['localhost:9586']
   
   # OpenVPN exporter
   - job_name: 'openvpn'
     static_configs:
       - targets: ['localhost:9176']
   ```

2. **Connection Monitoring**
   ```bash
   # WireGuard status
   wg show
   wg show wg0 dump | column -t
   
   # OpenVPN status
   cat /var/log/openvpn/openvpn-status.log
   
   # IPSec status
   ipsec status
   ipsec statusall
   ```

### Common Issues

1. **MTU Problems**
   ```bash
   # Calculate optimal MTU
   ping -M do -s 1472 remote-host
   
   # Set MTU in WireGuard
   [Interface]
   MTU = 1420
   
   # Set MTU in OpenVPN
   tun-mtu 1400
   mssfix 1350
   ```

2. **NAT Traversal**
   ```conf
   # IPSec NAT-T
   nat_traversal=yes
   forceencaps=yes
   
   # WireGuard behind NAT
   PersistentKeepalive = 25
   ```

## Integration Examples

### Kubernetes Integration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: wireguard-config
data:
  wg0.conf: |
    [Interface]
    PrivateKey = $(WG_PRIVATE_KEY)
    Address = 10.0.0.2/24
    
    [Peer]
    PublicKey = $(WG_SERVER_PUBLIC_KEY)
    Endpoint = vpn.example.com:51820
    AllowedIPs = 10.0.0.0/24, 192.168.0.0/16
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: wireguard
spec:
  template:
    spec:
      containers:
      - name: wireguard
        image: linuxserver/wireguard:latest
        securityContext:
          capabilities:
            add:
              - NET_ADMIN
              - SYS_MODULE
        volumeMounts:
        - name: config
          mountPath: /config
```

### Docker Compose Setup

```yaml
version: '3.8'

services:
  wireguard:
    image: linuxserver/wireguard:latest
    container_name: wireguard
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=UTC
      - PEERS=5
      - PEERDNS=auto
      - INTERNAL_SUBNET=10.0.0.0
    volumes:
      - ./config:/config
      - /lib/modules:/lib/modules
    ports:
      - 51820:51820/udp
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
    restart: unless-stopped

  openvpn:
    image: kylemanna/openvpn
    container_name: openvpn
    cap_add:
      - NET_ADMIN
    ports:
      - "1194:1194/udp"
    volumes:
      - ./openvpn-data:/etc/openvpn
    restart: unless-stopped
```

## Security Hardening

### Firewall Rules

```bash
# WireGuard firewall rules
iptables -A INPUT -i wg0 -j ACCEPT
iptables -A FORWARD -i wg0 -j ACCEPT
iptables -A FORWARD -o wg0 -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# OpenVPN firewall rules
iptables -A INPUT -i tun0 -j ACCEPT
iptables -A FORWARD -i tun0 -j ACCEPT
iptables -A FORWARD -o tun0 -j ACCEPT
iptables -A OUTPUT -o tun0 -j ACCEPT

# IPSec firewall rules
iptables -A INPUT -p esp -j ACCEPT
iptables -A INPUT -p ah -j ACCEPT
iptables -A INPUT -p udp --dport 500 -j ACCEPT
iptables -A INPUT -p udp --dport 4500 -j ACCEPT
```

### Certificate Management

```bash
# Automated certificate renewal
#!/bin/bash
# renew-vpn-certs.sh

EASYRSA_PATH="/etc/openvpn/easy-rsa"
DAYS_BEFORE_EXPIRY=30

cd $EASYRSA_PATH

# Check certificate expiration
for cert in pki/issued/*.crt; do
    if openssl x509 -checkend $(($DAYS_BEFORE_EXPIRY * 86400)) -noout -in "$cert"; then
        echo "Certificate $cert is still valid"
    else
        echo "Certificate $cert needs renewal"
        # Renewal logic here
    fi
done
```

## Performance Benchmarking

### Speed Testing

```bash
# WireGuard performance test
iperf3 -c 10.0.0.1 -t 60 -P 4

# OpenVPN performance test
iperf3 -c 10.8.0.1 -t 60 -P 4 -R

# Latency testing
mtr --report --report-cycles 100 vpn-endpoint
```

### Optimization Results

```yaml
performance_metrics:
  wireguard:
    throughput: "950 Mbps"
    latency: "0.5ms"
    cpu_usage: "5%"
  
  openvpn:
    aes_256_gcm:
      throughput: "400 Mbps"
      latency: "2ms"
      cpu_usage: "25%"
  
  ipsec:
    aes_256_sha256:
      throughput: "600 Mbps"
      latency: "1ms"
      cpu_usage: "15%"
```