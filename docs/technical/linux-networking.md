---
title: "Linux Networking"
description: "Master Linux networking - from TCP/IP fundamentals to advanced routing and security with iptables"
---

# Linux Networking

Linux networking is a cornerstone skill for platform engineers, encompassing everything from basic connectivity to complex routing, security policies, and performance optimization. This comprehensive guide covers TCP/IP fundamentals, network configuration, routing protocols, firewall management with iptables/nftables, and advanced networking concepts. Understanding these topics enables platform engineers to design, implement, and troubleshoot network infrastructure effectively in modern cloud and on-premises environments.

## Core Concepts and Features

### Linux Network Stack
The Linux network stack consists of multiple layers:
- **Network Interface Layer**: Physical and virtual interfaces
- **Network Layer**: IP protocol handling, routing
- **Transport Layer**: TCP, UDP, and other protocols
- **Socket Layer**: Application interface to networking
- **Netfilter Framework**: Packet filtering and manipulation

### Key Networking Components
1. **Network Interfaces**
   - Physical interfaces (eth0, ens33)
   - Virtual interfaces (lo, tun, tap, veth)
   - Bridge interfaces
   - VLAN interfaces
   - Bond/team interfaces

2. **Routing Subsystem**
   - Routing tables
   - Policy-based routing
   - Dynamic routing protocols
   - Multipath routing

3. **Netfilter/iptables**
   - Packet filtering
   - NAT (Network Address Translation)
   - Packet mangling
   - Connection tracking

4. **Network Namespaces**
   - Isolated network stacks
   - Container networking
   - Virtual routing

## Common Use Cases

### Infrastructure Networking
- Configuring server network interfaces
- Setting up VLANs for network segmentation
- Implementing high availability with bonding
- Managing routing between subnets

### Security Implementation
- Firewall rules and policies
- Network access control
- DDoS protection
- VPN configuration

### Container and Cloud Networking
- Docker network management
- Kubernetes networking
- Cloud VPC configuration
- Software-defined networking

### Performance Optimization
- Network tuning for high throughput
- Latency optimization
- Load balancing
- Traffic shaping and QoS

## Getting Started Example

Here's a comprehensive example demonstrating various Linux networking configurations:

```bash
#!/bin/bash
#
# Comprehensive Linux Networking Configuration Script
# Demonstrates interface management, routing, and firewall setup

set -euo pipefail

# Configuration
PRIMARY_INTERFACE="eth0"
SECONDARY_INTERFACE="eth1"
BRIDGE_NAME="br0"
VLAN_ID="100"
BOND_NAME="bond0"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# Error handling
error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
    exit 1
}

# Check prerequisites
check_prerequisites() {
    local tools=("ip" "iptables" "tc" "bridge" "vconfig")
    
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &>/dev/null; then
            log "Installing $tool..."
            apt-get install -y "$(get_package_name "$tool")" || \
                error "Failed to install $tool"
        fi
    done
}

get_package_name() {
    case "$1" in
        "ip") echo "iproute2" ;;
        "tc") echo "iproute2" ;;
        "bridge") echo "bridge-utils" ;;
        "vconfig") echo "vlan" ;;
        *) echo "$1" ;;
    esac
}

# Network Interface Configuration
configure_network_interfaces() {
    log "Configuring network interfaces..."
    
    # Display current interfaces
    log "Current network interfaces:"
    ip addr show
    
    # Configure primary interface with static IP
    cat > /etc/network/interfaces.d/primary << EOF
auto $PRIMARY_INTERFACE
iface $PRIMARY_INTERFACE inet static
    address 192.168.1.10
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4
    mtu 9000
EOF
    
    # Configure secondary interface
    cat > /etc/network/interfaces.d/secondary << EOF
auto $SECONDARY_INTERFACE
iface $SECONDARY_INTERFACE inet static
    address 10.0.0.10
    netmask 255.255.255.0
EOF
    
    # Apply configuration
    ifdown $PRIMARY_INTERFACE && ifup $PRIMARY_INTERFACE || true
    ifdown $SECONDARY_INTERFACE && ifup $SECONDARY_INTERFACE || true
    
    # Using ip command for immediate configuration
    ip addr add 192.168.1.10/24 dev $PRIMARY_INTERFACE 2>/dev/null || true
    ip link set $PRIMARY_INTERFACE up
    ip route add default via 192.168.1.1 dev $PRIMARY_INTERFACE 2>/dev/null || true
}

# VLAN Configuration
configure_vlan() {
    log "Configuring VLAN interfaces..."
    
    # Load 8021q module
    modprobe 8021q
    echo "8021q" >> /etc/modules
    
    # Create VLAN interface
    ip link add link $PRIMARY_INTERFACE name ${PRIMARY_INTERFACE}.${VLAN_ID} type vlan id $VLAN_ID
    
    # Configure VLAN interface
    ip addr add 192.168.100.10/24 dev ${PRIMARY_INTERFACE}.${VLAN_ID}
    ip link set ${PRIMARY_INTERFACE}.${VLAN_ID} up
    
    # Make persistent
    cat > /etc/network/interfaces.d/vlan${VLAN_ID} << EOF
auto ${PRIMARY_INTERFACE}.${VLAN_ID}
iface ${PRIMARY_INTERFACE}.${VLAN_ID} inet static
    address 192.168.100.10
    netmask 255.255.255.0
    vlan-raw-device $PRIMARY_INTERFACE
EOF
    
    log "VLAN $VLAN_ID configured on $PRIMARY_INTERFACE"
}

# Bridge Configuration
configure_bridge() {
    log "Configuring bridge interface..."
    
    # Create bridge
    ip link add name $BRIDGE_NAME type bridge
    ip link set $BRIDGE_NAME up
    
    # Add interfaces to bridge
    ip link set $SECONDARY_INTERFACE master $BRIDGE_NAME
    
    # Configure bridge IP
    ip addr add 172.16.0.1/24 dev $BRIDGE_NAME
    
    # Bridge settings
    echo 0 > /sys/class/net/$BRIDGE_NAME/bridge/stp_state
    echo 0 > /sys/devices/virtual/net/$BRIDGE_NAME/bridge/bridge_id
    
    # Make persistent
    cat > /etc/network/interfaces.d/bridge << EOF
auto $BRIDGE_NAME
iface $BRIDGE_NAME inet static
    address 172.16.0.1
    netmask 255.255.255.0
    bridge_ports $SECONDARY_INTERFACE
    bridge_stp off
    bridge_fd 0
    bridge_maxwait 0
EOF
    
    log "Bridge $BRIDGE_NAME configured"
}

# Bonding Configuration
configure_bonding() {
    log "Configuring network bonding..."
    
    # Load bonding module
    modprobe bonding
    echo "bonding" >> /etc/modules
    
    # Create bond interface
    ip link add $BOND_NAME type bond
    ip link set $BOND_NAME type bond mode active-backup
    
    # Add slaves to bond
    ip link set eth2 down 2>/dev/null || true
    ip link set eth3 down 2>/dev/null || true
    ip link set eth2 master $BOND_NAME 2>/dev/null || true
    ip link set eth3 master $BOND_NAME 2>/dev/null || true
    
    # Configure bond IP
    ip addr add 192.168.2.10/24 dev $BOND_NAME
    ip link set $BOND_NAME up
    
    # Make persistent
    cat > /etc/network/interfaces.d/bond0 << EOF
auto $BOND_NAME
iface $BOND_NAME inet static
    address 192.168.2.10
    netmask 255.255.255.0
    bond-slaves eth2 eth3
    bond-mode active-backup
    bond-miimon 100
    bond-downdelay 200
    bond-updelay 200
EOF
    
    log "Bond $BOND_NAME configured in active-backup mode"
}

# Advanced Routing Configuration
configure_routing() {
    log "Configuring advanced routing..."
    
    # Enable IP forwarding
    echo "net.ipv4.ip_forward=1" > /etc/sysctl.d/routing.conf
    echo "net.ipv6.conf.all.forwarding=1" >> /etc/sysctl.d/routing.conf
    sysctl -p /etc/sysctl.d/routing.conf
    
    # Create additional routing tables
    echo "100 dmz" >> /etc/iproute2/rt_tables
    echo "101 vpn" >> /etc/iproute2/rt_tables
    
    # Add routes to custom tables
    ip route add 10.0.0.0/24 dev $SECONDARY_INTERFACE table dmz
    ip route add default via 10.0.0.1 table dmz
    
    # Policy-based routing
    ip rule add from 10.0.0.0/24 table dmz
    ip rule add to 10.0.0.0/24 table dmz
    
    # Source-based routing example
    ip rule add from 192.168.100.0/24 table vpn priority 100
    
    # Equal-Cost Multi-Path (ECMP) routing
    ip route add default \
        nexthop via 192.168.1.1 dev $PRIMARY_INTERFACE weight 1 \
        nexthop via 10.0.0.1 dev $SECONDARY_INTERFACE weight 1
    
    # Static routes
    ip route add 172.16.0.0/12 via 192.168.1.254
    ip route add 10.10.0.0/16 via 10.0.0.254
    
    # Display routing tables
    log "Main routing table:"
    ip route show
    
    log "Policy routing rules:"
    ip rule show
}

# iptables Firewall Configuration
configure_iptables() {
    log "Configuring iptables firewall..."
    
    # Backup current rules
    iptables-save > /etc/iptables/rules.backup
    
    # Flush existing rules
    iptables -F
    iptables -X
    iptables -t nat -F
    iptables -t nat -X
    iptables -t mangle -F
    iptables -t mangle -X
    
    # Default policies
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT ACCEPT
    
    # Loopback traffic
    iptables -A INPUT -i lo -j ACCEPT
    iptables -A OUTPUT -o lo -j ACCEPT
    
    # Established connections
    iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    
    # ICMP
    iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 5/second -j ACCEPT
    iptables -A INPUT -p icmp --icmp-type echo-reply -j ACCEPT
    iptables -A INPUT -p icmp --icmp-type destination-unreachable -j ACCEPT
    iptables -A INPUT -p icmp --icmp-type time-exceeded -j ACCEPT
    
    # SSH (with rate limiting)
    iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
    iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update \
        --seconds 60 --hitcount 4 -j LOG --log-prefix "SSH-BRUTEFORCE: "
    iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update \
        --seconds 60 --hitcount 4 -j DROP
    iptables -A INPUT -p tcp --dport 22 -j ACCEPT
    
    # HTTP/HTTPS
    iptables -A INPUT -p tcp --dport 80 -j ACCEPT
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT
    
    # DNS
    iptables -A INPUT -p udp --dport 53 -j ACCEPT
    iptables -A INPUT -p tcp --dport 53 -j ACCEPT
    
    # NAT configuration
    iptables -t nat -A POSTROUTING -s 192.168.100.0/24 -o $PRIMARY_INTERFACE -j MASQUERADE
    iptables -A FORWARD -i ${PRIMARY_INTERFACE}.${VLAN_ID} -o $PRIMARY_INTERFACE -j ACCEPT
    iptables -A FORWARD -i $PRIMARY_INTERFACE -o ${PRIMARY_INTERFACE}.${VLAN_ID} \
        -m state --state RELATED,ESTABLISHED -j ACCEPT
    
    # Port forwarding example
    iptables -t nat -A PREROUTING -i $PRIMARY_INTERFACE -p tcp --dport 8080 \
        -j DNAT --to-destination 192.168.100.20:80
    iptables -A FORWARD -p tcp -d 192.168.100.20 --dport 80 \
        -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
    
    # DDoS protection
    iptables -N DDOS_PROTECT
    iptables -A INPUT -j DDOS_PROTECT
    
    # SYN flood protection
    iptables -A DDOS_PROTECT -p tcp --syn -m limit --limit 10/s --limit-burst 20 -j RETURN
    iptables -A DDOS_PROTECT -p tcp --syn -j DROP
    
    # Connection limit per IP
    iptables -A INPUT -p tcp --syn --dport 80 -m connlimit --connlimit-above 20 -j DROP
    
    # Log dropped packets
    iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-dropped: " --log-level 4
    iptables -A FORWARD -m limit --limit 5/min -j LOG --log-prefix "iptables-forward-dropped: " --log-level 4
    
    # Save rules
    iptables-save > /etc/iptables/rules.v4
    
    log "iptables firewall configured"
}

# nftables Configuration (Modern Alternative)
configure_nftables() {
    log "Configuring nftables (modern iptables replacement)..."
    
    # Create nftables configuration
    cat > /etc/nftables.conf << 'EOF'
#!/usr/sbin/nft -f

flush ruleset

# Define variables
define WAN_IF = eth0
define LAN_IF = eth1
define LAN_NET = 192.168.1.0/24

# Create tables
table inet filter {
    chain input {
        type filter hook input priority filter; policy drop;
        
        # Accept loopback
        iif "lo" accept
        
        # Accept established connections
        ct state established,related accept
        
        # Drop invalid connections
        ct state invalid drop
        
        # Accept ICMP
        ip protocol icmp icmp type { echo-request, echo-reply, destination-unreachable, time-exceeded } limit rate 5/second accept
        ip6 nexthdr icmpv6 icmpv6 type { echo-request, echo-reply, destination-unreachable, time-exceeded } limit rate 5/second accept
        
        # SSH with rate limiting
        tcp dport 22 ct state new limit rate 3/minute accept
        
        # HTTP/HTTPS
        tcp dport { 80, 443 } accept
        
        # Log and drop
        limit rate 5/minute log prefix "nftables-input-dropped: "
        drop
    }
    
    chain forward {
        type filter hook forward priority filter; policy drop;
        
        # Accept established connections
        ct state established,related accept
        
        # Accept from LAN to WAN
        iifname $LAN_IF oifname $WAN_IF accept
        
        # Log and drop
        limit rate 5/minute log prefix "nftables-forward-dropped: "
        drop
    }
    
    chain output {
        type filter hook output priority filter; policy accept;
    }
}

table ip nat {
    chain prerouting {
        type nat hook prerouting priority dstnat;
        
        # Port forwarding
        iifname $WAN_IF tcp dport 8080 dnat to 192.168.1.20:80
    }
    
    chain postrouting {
        type nat hook postrouting priority srcnat;
        
        # Masquerade
        oifname $WAN_IF masquerade
    }
}
EOF
    
    # Load nftables rules
    nft -f /etc/nftables.conf
    
    log "nftables configured"
}

# Traffic Control and QoS
configure_traffic_control() {
    log "Configuring traffic control and QoS..."
    
    # Clear existing qdisc
    tc qdisc del dev $PRIMARY_INTERFACE root 2>/dev/null || true
    
    # HTB (Hierarchical Token Bucket) setup
    tc qdisc add dev $PRIMARY_INTERFACE root handle 1: htb default 30
    
    # Root class (total bandwidth)
    tc class add dev $PRIMARY_INTERFACE parent 1: classid 1:1 htb rate 1000mbit
    
    # High priority class (VoIP, SSH)
    tc class add dev $PRIMARY_INTERFACE parent 1:1 classid 1:10 htb rate 100mbit ceil 200mbit prio 1
    
    # Normal priority class (HTTP, HTTPS)
    tc class add dev $PRIMARY_INTERFACE parent 1:1 classid 1:20 htb rate 600mbit ceil 900mbit prio 2
    
    # Low priority class (bulk traffic)
    tc class add dev $PRIMARY_INTERFACE parent 1:1 classid 1:30 htb rate 300mbit ceil 500mbit prio 3
    
    # SFQ (Stochastic Fair Queuing) for each class
    tc qdisc add dev $PRIMARY_INTERFACE parent 1:10 handle 10: sfq perturb 10
    tc qdisc add dev $PRIMARY_INTERFACE parent 1:20 handle 20: sfq perturb 10
    tc qdisc add dev $PRIMARY_INTERFACE parent 1:30 handle 30: sfq perturb 10
    
    # Classification filters
    # SSH to high priority
    tc filter add dev $PRIMARY_INTERFACE protocol ip parent 1:0 prio 1 u32 \
        match ip dport 22 0xffff flowid 1:10
    
    # HTTP/HTTPS to normal priority
    tc filter add dev $PRIMARY_INTERFACE protocol ip parent 1:0 prio 2 u32 \
        match ip dport 80 0xffff flowid 1:20
    tc filter add dev $PRIMARY_INTERFACE protocol ip parent 1:0 prio 2 u32 \
        match ip dport 443 0xffff flowid 1:20
    
    # Everything else to low priority (default)
    
    log "Traffic control configured"
}

# Network Monitoring Setup
setup_network_monitoring() {
    log "Setting up network monitoring..."
    
    # Create monitoring script
    cat > /usr/local/bin/network-monitor.sh << 'EOF'
#!/bin/bash

# Network monitoring script
LOG_DIR="/var/log/network-monitor"
mkdir -p "$LOG_DIR"

# Function to get interface statistics
get_interface_stats() {
    local interface=$1
    local stats=$(ip -s link show $interface)
    echo "$stats"
}

# Function to monitor bandwidth
monitor_bandwidth() {
    local interface=$1
    local old_rx=$(cat /sys/class/net/$interface/statistics/rx_bytes)
    local old_tx=$(cat /sys/class/net/$interface/statistics/tx_bytes)
    
    sleep 1
    
    local new_rx=$(cat /sys/class/net/$interface/statistics/rx_bytes)
    local new_tx=$(cat /sys/class/net/$interface/statistics/tx_bytes)
    
    local rx_bps=$(( ($new_rx - $old_rx) * 8 ))
    local tx_bps=$(( ($new_tx - $old_tx) * 8 ))
    
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $interface: RX: $((rx_bps/1024/1024)) Mbps, TX: $((tx_bps/1024/1024)) Mbps"
}

# Function to check connectivity
check_connectivity() {
    local targets=("8.8.8.8" "1.1.1.1" "google.com")
    
    for target in "${targets[@]}"; do
        if ping -c 1 -W 1 "$target" > /dev/null 2>&1; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') - Connectivity to $target: OK"
        else
            echo "$(date '+%Y-%m-%d %H:%M:%S') - Connectivity to $target: FAILED" >&2
        fi
    done
}

# Function to monitor connections
monitor_connections() {
    local conn_count=$(ss -tan | grep ESTAB | wc -l)
    local listen_count=$(ss -tln | grep LISTEN | wc -l)
    
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Active connections: $conn_count, Listening ports: $listen_count"
    
    # Top talkers
    echo "Top connections by count:"
    ss -tan | grep ESTAB | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -5
}

# Main monitoring loop
while true; do
    {
        echo "=== Network Monitor Report ==="
        monitor_bandwidth eth0
        check_connectivity
        monitor_connections
        echo
    } | tee -a "$LOG_DIR/monitor-$(date +%Y%m%d).log"
    
    sleep 60
done
EOF
    
    chmod +x /usr/local/bin/network-monitor.sh
    
    # Create systemd service
    cat > /etc/systemd/system/network-monitor.service << EOF
[Unit]
Description=Network Monitoring Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/network-monitor.sh
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable network-monitor.service
    systemctl start network-monitor.service
    
    log "Network monitoring setup complete"
}

# Network Troubleshooting Tools
create_troubleshooting_toolkit() {
    log "Creating network troubleshooting toolkit..."
    
    cat > /usr/local/bin/net-troubleshoot.sh << 'EOF'
#!/bin/bash

# Network troubleshooting toolkit

echo "=== Network Troubleshooting Report ==="
echo "Date: $(date)"
echo

# Interface status
echo "=== Interface Status ==="
ip addr show
echo

# Routing table
echo "=== Routing Table ==="
ip route show
ip rule show
echo

# DNS configuration
echo "=== DNS Configuration ==="
cat /etc/resolv.conf
echo

# Connection statistics
echo "=== Connection Statistics ==="
ss -s
echo

# Listening ports
echo "=== Listening Ports ==="
ss -tuln
echo

# ARP table
echo "=== ARP Table ==="
ip neigh show
echo

# iptables rules
echo "=== Firewall Rules ==="
iptables -L -n -v
echo

# Network performance
echo "=== Network Performance ==="
for iface in $(ls /sys/class/net | grep -v lo); do
    echo "Interface: $iface"
    ethtool $iface 2>/dev/null | grep -E "Speed:|Duplex:|Link detected:"
    echo
done

# TCP tuning parameters
echo "=== TCP Parameters ==="
sysctl net.ipv4.tcp_congestion_control
sysctl net.core.rmem_max
sysctl net.core.wmem_max
echo

# Recent kernel messages
echo "=== Recent Network-Related Kernel Messages ==="
dmesg | grep -E "eth|link|carrier" | tail -20
EOF
    
    chmod +x /usr/local/bin/net-troubleshoot.sh
    
    log "Troubleshooting toolkit created"
}

# Main execution
main() {
    log "Starting comprehensive network configuration..."
    
    check_prerequisites
    configure_network_interfaces
    configure_vlan
    configure_bridge
    configure_bonding
    configure_routing
    configure_iptables
    configure_nftables
    configure_traffic_control
    setup_network_monitoring
    create_troubleshooting_toolkit
    
    log "Network configuration complete!"
    
    # Display summary
    echo
    log "Configuration Summary:"
    log "- Primary Interface: $PRIMARY_INTERFACE (192.168.1.10/24)"
    log "- VLAN $VLAN_ID: ${PRIMARY_INTERFACE}.${VLAN_ID} (192.168.100.10/24)"
    log "- Bridge: $BRIDGE_NAME (172.16.0.1/24)"
    log "- Bond: $BOND_NAME (192.168.2.10/24)"
    log "- Firewall: Configured with iptables and nftables"
    log "- Traffic Control: QoS rules applied"
    log "- Monitoring: Network monitor service running"
}

# Run main function
main
```

## Best Practices

### 1. Network Design and Architecture
```bash
# Network segmentation setup
implement_network_segmentation() {
    # Create VLANs for different purposes
    local vlans=(
        "10:management"
        "20:production"
        "30:development"
        "40:dmz"
        "50:storage"
    )
    
    for vlan_info in "${vlans[@]}"; do
        IFS=':' read -r vlan_id vlan_name <<< "$vlan_info"
        
        # Create VLAN interface
        ip link add link eth0 name eth0.$vlan_id type vlan id $vlan_id
        ip link set eth0.$vlan_id up
        
        # Configure IP based on VLAN
        case $vlan_name in
            "management")
                ip addr add 10.0.10.1/24 dev eth0.$vlan_id
                ;;
            "production")
                ip addr add 10.0.20.1/24 dev eth0.$vlan_id
                ;;
            "development")
                ip addr add 10.0.30.1/24 dev eth0.$vlan_id
                ;;
            "dmz")
                ip addr add 10.0.40.1/24 dev eth0.$vlan_id
                ;;
            "storage")
                ip addr add 10.0.50.1/24 dev eth0.$vlan_id
                ;;
        esac
        
        echo "VLAN $vlan_id ($vlan_name) configured"
    done
    
    # Inter-VLAN routing with security policies
    configure_inter_vlan_routing() {
        # Allow management to all
        iptables -A FORWARD -i eth0.10 -j ACCEPT
        
        # Production can't reach development
        iptables -A FORWARD -i eth0.20 -o eth0.30 -j DROP
        
        # DMZ restricted access
        iptables -A FORWARD -i eth0.40 -o eth0.20 -p tcp --dport 443 -j ACCEPT
        iptables -A FORWARD -i eth0.40 -j DROP
        
        # Storage network isolated except from production
        iptables -A FORWARD -i eth0.50 -j DROP
        iptables -A FORWARD -o eth0.50 -s 10.0.20.0/24 -j ACCEPT
    }
}

# High availability network configuration
setup_ha_networking() {
    # Configure keepalived for VRRP
    cat > /etc/keepalived/keepalived.conf << 'EOF'
global_defs {
    router_id LVS_PRIMARY
}

vrrp_script check_nginx {
    script "/usr/bin/pgrep nginx"
    interval 2
    weight -20
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    advert_int 1
    
    authentication {
        auth_type PASS
        auth_pass secretpass
    }
    
    virtual_ipaddress {
        192.168.1.100/24 dev eth0
    }
    
    track_script {
        check_nginx
    }
    
    notify_master "/usr/local/bin/notify_master.sh"
    notify_backup "/usr/local/bin/notify_backup.sh"
    notify_fault "/usr/local/bin/notify_fault.sh"
}
EOF
}
```

### 2. Security Hardening
```bash
# Comprehensive firewall security
implement_security_policies() {
    # DDoS protection with iptables
    setup_ddos_protection() {
        # Create DDoS protection chain
        iptables -N DDOS_PROTECT
        
        # Limit new connections per second
        iptables -A DDOS_PROTECT -p tcp --syn -m limit --limit 25/s --limit-burst 50 -j RETURN
        iptables -A DDOS_PROTECT -p tcp --syn -j DROP
        
        # ICMP flood protection
        iptables -A DDOS_PROTECT -p icmp -m limit --limit 10/s --limit-burst 20 -j RETURN
        iptables -A DDOS_PROTECT -p icmp -j DROP
        
        # UDP flood protection
        iptables -A DDOS_PROTECT -p udp -m limit --limit 100/s --limit-burst 200 -j RETURN
        iptables -A DDOS_PROTECT -p udp -j DROP
        
        # Apply to INPUT chain
        iptables -I INPUT 1 -j DDOS_PROTECT
    }
    
    # Port knocking setup
    setup_port_knocking() {
        # Create chains for port knocking
        iptables -N KNOCKING
        iptables -N GATE1
        iptables -N GATE2
        iptables -N GATE3
        iptables -N PASSED
        
        # First knock
        iptables -A GATE1 -p tcp --dport 1111 -m recent --name AUTH1 --set -j DROP
        iptables -A GATE1 -j DROP
        
        # Second knock
        iptables -A GATE2 -m recent --name AUTH1 --rcheck --seconds 10 -j GATE3
        iptables -A GATE2 -j GATE1
        
        # Third knock
        iptables -A GATE3 -p tcp --dport 2222 -m recent --name AUTH2 --set -j DROP
        iptables -A GATE3 -j GATE1
        
        # Final knock opens SSH
        iptables -A PASSED -m recent --name AUTH2 --rcheck --seconds 10 -p tcp --dport 3333 \
            -m recent --name HEAVEN --set -j DROP
        iptables -A PASSED -j GATE1
        
        # Allow SSH if knocked correctly
        iptables -A INPUT -m recent --name HEAVEN --rcheck --seconds 30 -p tcp --dport 22 -j ACCEPT
        
        # Send new connections through knocking
        iptables -A INPUT -p tcp --dport 22 -j KNOCKING
    }
    
    # Network hardening sysctl parameters
    apply_network_hardening() {
        cat > /etc/sysctl.d/network-security.conf << 'EOF'
# IP Spoofing protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0

# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0

# Disable source packet routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Log Martians
net.ipv4.conf.all.log_martians = 1

# Ignore ICMP ping requests
net.ipv4.icmp_echo_ignore_broadcasts = 1

# SYN flood protection
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 4096
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 2

# Time-wait assassination hazards protection
net.ipv4.tcp_rfc1337 = 1

# TCP timestamps
net.ipv4.tcp_timestamps = 0

# Increase TCP window scaling
net.ipv4.tcp_window_scaling = 1

# Increase the tcp-time-wait buckets pool size
net.ipv4.tcp_max_tw_buckets = 1440000
EOF
        
        sysctl -p /etc/sysctl.d/network-security.conf
    }
}
```

### 3. Performance Optimization
```bash
# Network performance tuning
optimize_network_performance() {
    # TCP optimization
    cat > /etc/sysctl.d/tcp-tuning.conf << 'EOF'
# TCP buffer sizes
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728

# TCP congestion control
net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq

# Connection tracking
net.netfilter.nf_conntrack_max = 1000000
net.nf_conntrack_max = 1000000
net.netfilter.nf_conntrack_tcp_timeout_established = 1800
net.netfilter.nf_conntrack_tcp_timeout_close_wait = 60
net.netfilter.nf_conntrack_tcp_timeout_fin_wait = 120
net.netfilter.nf_conntrack_tcp_timeout_time_wait = 120

# Increase network device backlog
net.core.netdev_max_backlog = 5000

# Increase TCP backlog
net.ipv4.tcp_max_syn_backlog = 4096

# Enable TCP fast open
net.ipv4.tcp_fastopen = 3

# TCP keepalive tuning
net.ipv4.tcp_keepalive_time = 60
net.ipv4.tcp_keepalive_intvl = 10
net.ipv4.tcp_keepalive_probes = 6

# Enable MTU probing
net.ipv4.tcp_mtu_probing = 1

# TCP FIN timeout
net.ipv4.tcp_fin_timeout = 10

# Reuse sockets in TIME_WAIT state
net.ipv4.tcp_tw_reuse = 1

# Number of times SYNACKs sent
net.ipv4.tcp_synack_retries = 2
EOF
    
    sysctl -p /etc/sysctl.d/tcp-tuning.conf
    
    # NIC optimization
    optimize_nic() {
        local interface=$1
        
        # Increase ring buffer sizes
        ethtool -G $interface rx 4096 tx 4096 2>/dev/null || true
        
        # Enable offloading features
        ethtool -K $interface tso on gso on gro on 2>/dev/null || true
        
        # Set interrupt coalescing
        ethtool -C $interface rx-usecs 10 tx-usecs 10 2>/dev/null || true
        
        # Enable jumbo frames
        ip link set $interface mtu 9000 2>/dev/null || true
        
        # CPU affinity for interrupts
        set_irq_affinity() {
            local irqs=$(grep $interface /proc/interrupts | awk '{print $1}' | tr -d ':')
            local cpu=0
            
            for irq in $irqs; do
                echo $cpu > /proc/irq/$irq/smp_affinity_list
                cpu=$(( (cpu + 1) % $(nproc) ))
            done
        }
    }
}

# Network monitoring and analytics
setup_network_analytics() {
    # Create packet capture script
    cat > /usr/local/bin/packet-analyzer.sh << 'EOF'
#!/bin/bash

# Advanced packet analysis
analyze_traffic() {
    local interface=$1
    local duration=${2:-60}
    
    # Capture packets
    tcpdump -i $interface -w /tmp/capture.pcap -G $duration -W 1 &
    local tcpdump_pid=$!
    
    sleep $((duration + 1))
    
    # Analyze capture
    echo "=== Traffic Analysis ==="
    
    # Protocol distribution
    echo "Protocol Distribution:"
    tshark -r /tmp/capture.pcap -T fields -e ip.proto | sort | uniq -c | sort -rn
    
    # Top talkers
    echo -e "\nTop Source IPs:"
    tshark -r /tmp/capture.pcap -T fields -e ip.src | sort | uniq -c | sort -rn | head -10
    
    echo -e "\nTop Destination IPs:"
    tshark -r /tmp/capture.pcap -T fields -e ip.dst | sort | uniq -c | sort -rn | head -10
    
    # Port analysis
    echo -e "\nTop Destination Ports:"
    tshark -r /tmp/capture.pcap -T fields -e tcp.dstport -e udp.dstport | \
        grep -v "^$" | sort | uniq -c | sort -rn | head -10
    
    # Bandwidth analysis
    echo -e "\nBandwidth by conversation:"
    tshark -r /tmp/capture.pcap -z conv,ip -q
    
    rm -f /tmp/capture.pcap
}

# Real-time monitoring
monitor_realtime() {
    watch -n 1 '
        echo "=== Network Statistics ==="
        ss -s
        echo -e "\n=== Interface Statistics ==="
        ip -s link show
        echo -e "\n=== TCP State ==="
        ss -tan | awk "{print \$1}" | sort | uniq -c
    '
}

case "$1" in
    analyze)
        analyze_traffic ${2:-eth0} ${3:-60}
        ;;
    monitor)
        monitor_realtime
        ;;
    *)
        echo "Usage: $0 {analyze|monitor} [interface] [duration]"
        ;;
esac
EOF
    
    chmod +x /usr/local/bin/packet-analyzer.sh
}
```

### 4. Container and Cloud Networking
```bash
# Docker networking configuration
setup_docker_networking() {
    # Create custom bridge network
    docker network create \
        --driver bridge \
        --subnet=172.20.0.0/16 \
        --ip-range=172.20.240.0/20 \
        --gateway=172.20.0.1 \
        --opt com.docker.network.bridge.name=docker-custom \
        custom-network
    
    # Configure Docker daemon networking
    cat > /etc/docker/daemon.json << 'EOF'
{
    "bridge": "none",
    "iptables": true,
    "ip-forward": true,
    "ip-masq": true,
    "userland-proxy": false,
    "userland-proxy-path": "/usr/libexec/docker-proxy",
    "bip": "172.17.0.1/16",
    "fixed-cidr": "172.17.0.0/17",
    "default-address-pools": [
        {
            "base": "172.18.0.0/16",
            "size": 24
        }
    ],
    "dns": ["8.8.8.8", "8.8.4.4"],
    "dns-opts": ["ndots:0"],
    "max-concurrent-downloads": 10,
    "max-concurrent-uploads": 5
}
EOF
    
    # Kubernetes CNI setup
    setup_kubernetes_cni() {
        # Calico installation
        kubectl apply -f https://docs.projectcalico.org/manifests/tigera-operator.yaml
        
        # Custom Calico configuration
        cat > calico-config.yaml << 'EOF'
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    bgp: Enabled
    ipPools:
    - blockSize: 26
      cidr: 10.244.0.0/16
      encapsulation: VXLANCrossSubnet
      natOutgoing: Enabled
      nodeSelector: all()
    mtu: 1440
  registry: quay.io/
EOF
        kubectl apply -f calico-config.yaml
    }
}
```

## Common Commands and Operations

### Interface Management
```bash
# View interfaces
ip link show
ip addr show
ifconfig -a

# Configure interface
ip addr add 192.168.1.10/24 dev eth0
ip link set eth0 up
ip link set eth0 mtu 9000

# Create virtual interfaces
ip link add veth0 type veth peer name veth1
ip link add br0 type bridge
ip link add link eth0 name eth0.100 type vlan id 100

# Delete interfaces
ip link delete veth0
ip link delete br0

# Interface statistics
ip -s link show eth0
ethtool eth0
ethtool -S eth0
```

### Routing Operations
```bash
# View routing table
ip route show
route -n
ip route show table all

# Add routes
ip route add 10.0.0.0/24 via 192.168.1.1
ip route add default via 192.168.1.1 dev eth0
ip route add 172.16.0.0/12 dev eth0 metric 100

# Delete routes
ip route del 10.0.0.0/24
ip route flush 10.0.0.0/24

# Policy routing
ip rule add from 192.168.1.0/24 table 100
ip rule add to 10.0.0.0/24 table 200
ip rule show

# Route metrics
ip route add 0.0.0.0/0 via 192.168.1.1 metric 100
```

### iptables/netfilter
```bash
# View rules
iptables -L -n -v
iptables -t nat -L -n -v
iptables-save

# Basic rules
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT
iptables -I INPUT 1 -i lo -j ACCEPT

# NAT operations
iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j MASQUERADE
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to 192.168.1.100:8080

# Connection tracking
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -m conntrack --ctstate NEW -p tcp --dport 80 -j ACCEPT

# Rate limiting
iptables -A INPUT -p icmp -m limit --limit 5/s -j ACCEPT
iptables -A INPUT -p tcp --syn -m limit --limit 10/s -j ACCEPT

# Logging
iptables -A INPUT -j LOG --log-prefix "Dropped: " --log-level 4
```

### Network Diagnostics
```bash
# Connectivity testing
ping -c 4 google.com
ping6 -c 4 google.com
traceroute google.com
mtr google.com

# DNS testing
nslookup google.com
dig google.com
host google.com
dig +trace google.com

# Port testing
telnet host 80
nc -zv host 22
nmap -p 80,443 host

# Socket statistics
ss -tunapl
ss -s
netstat -tunapl

# Packet capture
tcpdump -i eth0 -nn
tcpdump -i eth0 host 192.168.1.1
tcpdump -i eth0 port 80 -w capture.pcap
```

### Performance Testing
```bash
# Bandwidth testing
iperf3 -s                    # Server
iperf3 -c server -t 30       # Client

# Latency testing
ping -f -c 1000 host
hping3 -c 1000 -S -p 80 host

# Network stress testing
netperf -H server -t TCP_STREAM
nuttcp -S                    # Server
nuttcp server               # Client

# MTU discovery
ping -M do -s 1472 host     # Don't fragment
tracepath host              # Path MTU discovery
```

## Interview Tips

### Key Topics to Master
1. **OSI Model**: Understand all 7 layers and their functions
2. **TCP/IP Stack**: Deep knowledge of protocols and headers
3. **Routing Protocols**: Static, OSPF, BGP basics
4. **Network Security**: Firewalls, VPNs, security best practices
5. **Troubleshooting**: Systematic approach to network issues
6. **Container Networking**: Docker, Kubernetes networking models

### Common Interview Questions
1. "Explain the TCP three-way handshake"
   - SYN: Client initiates connection
   - SYN-ACK: Server acknowledges and responds
   - ACK: Client acknowledges server response
   - Connection established

2. "How does ARP work?"
   - Address Resolution Protocol
   - Maps IP addresses to MAC addresses
   - Broadcast request, unicast reply
   - ARP cache stores mappings

3. "Difference between TCP and UDP"
   - TCP: Reliable, ordered, connection-oriented
   - UDP: Unreliable, unordered, connectionless
   - TCP has flow control and congestion control
   - UDP has lower overhead

4. "How do you troubleshoot network connectivity?"
   - Check physical connectivity
   - Verify IP configuration
   - Test local connectivity (ping gateway)
   - Check routing table
   - Test DNS resolution
   - Verify firewall rules

### Practical Scenarios
Be prepared to:
- Design a network architecture
- Configure VLANs and routing
- Write firewall rules
- Troubleshoot connectivity issues
- Optimize network performance

## Essential Resources

### Books
1. **"TCP/IP Illustrated"** by W. Richard Stevens
   - Comprehensive TCP/IP reference
   - Protocol deep dive

2. **"Linux Network Administrator's Guide"** by Tony Bautts
   - Practical Linux networking
   - Real-world examples

3. **"Network Warrior"** by Gary A. Donahue
   - Network engineering practices
   - Enterprise scenarios

4. **"UNIX Network Programming"** by W. Richard Stevens
   - Socket programming
   - Network application development

5. **"Linux Kernel Networking"** by Rami Rosen
   - Kernel networking internals
   - Implementation details

### Online Documentation
1. **Linux Network Administrators Guide**: tldp.org
2. **iproute2 documentation**: Official documentation
3. **Netfilter documentation**: netfilter.org
4. **systemd.network**: Modern network configuration
5. **tc (Traffic Control) HOWTO**: Linux traffic control

### Courses and Certifications
1. **Linux Networking and Troubleshooting**: Linux Foundation
2. **LPIC-3 300**: Linux Enterprise Professional Certification
3. **Red Hat Certified Engineer (RHCE)**: Includes networking
4. **Network+ Certification**: CompTIA networking basics
5. **Cisco CCNA**: Network fundamentals (vendor-specific)

### Tools and Utilities
1. **Wireshark**: Packet analysis GUI
2. **tcpdump**: Command-line packet capture
3. **nmap**: Network discovery and security auditing
4. **iperf3**: Network performance measurement
5. **mtr**: Network diagnostic tool combining ping and traceroute
6. **netcat**: Swiss army knife for networking

### Communities and Forums
1. **r/networking**: Reddit networking community
2. **ServerFault**: Q&A for system administrators
3. **Linux Advanced Routing & Traffic Control**: lartc.org
4. **Netfilter mailing lists**: Development discussions
5. **Network Engineering Stack Exchange**: Professional Q&A

### Blogs and Resources
1. **PacketLife.net**: Network protocol references
2. **Linux Network Performance**: Brendan Gregg's resources
3. **Cloudflare Blog**: Modern networking topics
4. **IPSpace.net**: Network architecture blog
5. **Cumulus Networks Blog**: Open networking

Remember, Linux networking is vast and constantly evolving. Focus on understanding fundamental concepts while staying updated with modern practices like software-defined networking, container networking, and cloud-native approaches. Practical experience with troubleshooting and performance optimization is invaluable for mastering Linux networking.