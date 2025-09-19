---
title: "Linux Security Hardening"
description: "Comprehensive guide to securing Linux systems - from access controls to intrusion detection"
---

# Linux Security Hardening

Linux security hardening is a critical responsibility for platform engineers, protecting infrastructure from threats while maintaining operational efficiency. This comprehensive guide covers security fundamentals, hardening techniques, compliance requirements, and incident response procedures. Understanding these concepts enables platform engineers to build defense-in-depth strategies that protect against both external attacks and insider threats while meeting regulatory requirements.

## Core Concepts and Features

### Security Fundamentals
Linux security operates on multiple layers:
- **Access Control**: DAC (Discretionary) and MAC (Mandatory)
- **Authentication**: Multi-factor, certificates, keys
- **Authorization**: Permissions, capabilities, SELinux/AppArmor
- **Auditing**: System calls, file access, user actions
- **Encryption**: At-rest and in-transit protection

### Defense in Depth Layers
1. **Network Security**
   - Firewalls (iptables/nftables)
   - Network segmentation
   - VPN and encrypted tunnels
   - IDS/IPS systems

2. **Host Security**
   - Kernel hardening
   - Service minimization
   - File integrity monitoring
   - Malware detection

3. **Application Security**
   - Input validation
   - Secure coding practices
   - Runtime protection
   - Container security

4. **Data Security**
   - Encryption standards
   - Key management
   - Secure deletion
   - Backup protection

## Common Use Cases

### Infrastructure Protection
- Securing production servers
- Hardening container hosts
- Protecting CI/CD pipelines
- Securing cloud instances

### Compliance Requirements
- PCI DSS compliance
- HIPAA security rules
- SOC 2 requirements
- GDPR data protection

### Threat Mitigation
- Preventing unauthorized access
- Detecting intrusions
- Responding to incidents
- Forensic analysis

### Security Operations
- Vulnerability management
- Patch management
- Security monitoring
- Incident response

## Getting Started Example

Here's a comprehensive Linux security hardening script:

```bash
#!/bin/bash
#
# Linux Security Hardening Script
# Implements CIS benchmark recommendations and security best practices

set -euo pipefail

# Configuration
BACKUP_DIR="/root/security-backup-$(date +%Y%m%d-%H%M%S)"
LOG_FILE="/var/log/security-hardening.log"
AUDIT_RULES="/etc/audit/rules.d/hardening.rules"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging function
log() {
    local level=$1
    shift
    local message="$@"
    echo -e "${!level}[$level]${NC} $message" | tee -a "$LOG_FILE"
    logger -t "security-hardening" -p "security.$level" "$message"
}

# Create backup
create_backup() {
    log "GREEN" "Creating configuration backup..."
    mkdir -p "$BACKUP_DIR"
    
    # Backup important files
    local files=(
        "/etc/passwd" "/etc/shadow" "/etc/group"
        "/etc/ssh/sshd_config" "/etc/sudoers"
        "/etc/sysctl.conf" "/etc/security/limits.conf"
        "/etc/pam.d/" "/etc/audit/"
    )
    
    for file in "${files[@]}"; do
        if [[ -e "$file" ]]; then
            cp -a "$file" "$BACKUP_DIR/"
        fi
    done
    
    log "GREEN" "Backup created at: $BACKUP_DIR"
}

# User and Authentication Hardening
harden_users_auth() {
    log "YELLOW" "Hardening user accounts and authentication..."
    
    # Set password policy
    cat > /etc/security/pwquality.conf << 'EOF'
# Password quality requirements
minlen = 14
minclass = 4
maxrepeat = 2
maxsequence = 3
lcredit = -1
ucredit = -1
dcredit = -1
ocredit = -1
difok = 3
gecoscheck = 1
dictcheck = 1
usercheck = 1
enforcing = 1
EOF
    
    # Configure PAM
    cat > /etc/pam.d/common-password << 'EOF'
# Password policies
password    requisite    pam_pwquality.so retry=3
password    required     pam_pwhistory.so remember=24 enforce_for_root
password    [success=1 default=ignore]    pam_unix.so obscure use_authtok try_first_pass yescrypt rounds=11
password    requisite    pam_deny.so
password    required     pam_permit.so
EOF
    
    # Account lockout policy
    cat > /etc/pam.d/common-auth << 'EOF'
# Authentication with lockout
auth    required    pam_tally2.so deny=5 unlock_time=900 onerr=fail audit silent
auth    [success=1 default=ignore]    pam_unix.so nullok_secure
auth    requisite    pam_deny.so
auth    required    pam_permit.so
auth    optional    pam_cap.so
EOF
    
    # Set password aging
    sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' /etc/login.defs
    sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS   7/' /etc/login.defs
    sed -i 's/^PASS_WARN_AGE.*/PASS_WARN_AGE   14/' /etc/login.defs
    
    # Set umask
    sed -i 's/^UMASK.*/UMASK   077/' /etc/login.defs
    
    # Disable unused system accounts
    for user in games news uucp proxy list irc gnats; do
        if id "$user" &>/dev/null; then
            usermod -L -s /usr/sbin/nologin "$user" 2>/dev/null || true
        fi
    done
    
    # Find and lock accounts with empty passwords
    awk -F: '($2 == "" ) { print $1 }' /etc/shadow | while read -r user; do
        if [[ -n "$user" ]]; then
            log "RED" "Locking account with empty password: $user"
            passwd -l "$user"
        fi
    done
    
    # Ensure root is the only UID 0 account
    awk -F: '($3 == 0) { print $1 }' /etc/passwd | grep -v '^root$' | while read -r user; do
        log "RED" "Found non-root UID 0 account: $user"
        # Don't automatically delete - just alert
    done
    
    log "GREEN" "User and authentication hardening complete"
}

# SSH Hardening
harden_ssh() {
    log "YELLOW" "Hardening SSH configuration..."
    
    # Backup original config
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
    
    # Apply secure SSH settings
    cat > /etc/ssh/sshd_config.d/99-hardening.conf << 'EOF'
# SSH Hardening Configuration

# Protocol and Ciphers
Protocol 2
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com

# Authentication
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes
AuthenticationMethods publickey
MaxAuthTries 3
MaxSessions 2

# Access Control
AllowUsers *@10.0.0.0/8 *@192.168.0.0/16
DenyUsers root admin
AllowGroups ssh-users

# Security Features
StrictModes yes
IgnoreRhosts yes
HostbasedAuthentication no
X11Forwarding no
PermitUserEnvironment no
PermitTunnel no
DebianBanner no
TCPKeepAlive no
Compression no
ClientAliveInterval 300
ClientAliveCountMax 0
MaxStartups 2:30:10

# Logging
SyslogFacility AUTH
LogLevel VERBOSE

# File Transfer
Subsystem sftp /usr/lib/openssh/sftp-server -f AUTHPRIV -l INFO
EOF
    
    # Generate strong host keys if needed
    ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""
    ssh-keygen -t rsa -b 4096 -f /etc/ssh/ssh_host_rsa_key -N ""
    
    # Remove weak host keys
    rm -f /etc/ssh/ssh_host_dsa_key* /etc/ssh/ssh_host_ecdsa_key*
    
    # Set correct permissions
    chown root:root /etc/ssh/sshd_config
    chmod 600 /etc/ssh/sshd_config
    
    # Create ssh-users group if it doesn't exist
    groupadd -r ssh-users 2>/dev/null || true
    
    # Test configuration
    if sshd -t; then
        systemctl restart sshd
        log "GREEN" "SSH hardening complete"
    else
        log "RED" "SSH configuration test failed!"
        exit 1
    fi
}

# Kernel Hardening
harden_kernel() {
    log "YELLOW" "Applying kernel hardening parameters..."
    
    cat > /etc/sysctl.d/99-security.conf << 'EOF'
# Kernel Security Hardening

# Network Security
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.default.secure_redirects = 0
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.tcp_syncookies = 1
net.ipv6.conf.all.accept_ra = 0
net.ipv6.conf.default.accept_ra = 0

# Kernel Security
kernel.randomize_va_space = 2
kernel.sysrq = 0
kernel.core_uses_pid = 1
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1
kernel.printk = 3 3 3 3
kernel.unprivileged_bpf_disabled = 1
net.core.bpf_jit_harden = 2
kernel.yama.ptrace_scope = 3
kernel.unprivileged_userns_clone = 0
kernel.kexec_load_disabled = 1
kernel.modules_disabled = 0
kernel.perf_event_paranoid = 3
vm.unprivileged_userfaultfd = 0

# Process Security
fs.protected_hardlinks = 1
fs.protected_symlinks = 1
fs.protected_fifos = 2
fs.protected_regular = 2
fs.suid_dumpable = 0

# Additional Mitigations
kernel.pid_max = 65536
kernel.panic = 60
kernel.panic_on_oops = 1
vm.swappiness = 1
vm.vfs_cache_pressure = 50
EOF
    
    # Apply settings
    sysctl -p /etc/sysctl.d/99-security.conf
    
    # Disable unused network protocols
    cat > /etc/modprobe.d/blacklist-rare-network.conf << 'EOF'
# Disable rare network protocols
blacklist dccp
blacklist sctp
blacklist rds
blacklist tipc
blacklist n-hdlc
blacklist ax25
blacklist netrom
blacklist x25
blacklist rose
blacklist decnet
blacklist econet
blacklist af_802154
blacklist ipx
blacklist appletalk
blacklist psnap
blacklist p8023
blacklist p8022
blacklist can
blacklist atm
EOF
    
    # Disable uncommon filesystems
    cat > /etc/modprobe.d/blacklist-filesystems.conf << 'EOF'
# Disable uncommon filesystems
blacklist cramfs
blacklist freevxfs
blacklist jffs2
blacklist hfs
blacklist hfsplus
blacklist squashfs
blacklist udf
blacklist vfat
install cramfs /bin/false
install freevxfs /bin/false
install jffs2 /bin/false
install hfs /bin/false
install hfsplus /bin/false
install squashfs /bin/false
install udf /bin/false
install vfat /bin/false
EOF
    
    log "GREEN" "Kernel hardening complete"
}

# Firewall Configuration
configure_firewall() {
    log "YELLOW" "Configuring firewall rules..."
    
    # Install and enable firewall
    if command -v ufw >/dev/null 2>&1; then
        # UFW configuration
        ufw --force reset
        ufw default deny incoming
        ufw default allow outgoing
        ufw allow 22/tcp comment "SSH"
        ufw logging on
        ufw --force enable
    else
        # iptables configuration
        cat > /etc/iptables/rules.v4 << 'EOF'
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]

# Loopback
-A INPUT -i lo -j ACCEPT
-A OUTPUT -o lo -j ACCEPT
-A INPUT -s 127.0.0.0/8 ! -i lo -j DROP

# Established connections
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# SSH (rate limited)
-A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
-A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 -j DROP
-A INPUT -p tcp --dport 22 -j ACCEPT

# ICMP (rate limited)
-A INPUT -p icmp --icmp-type echo-request -m limit --limit 5/s -j ACCEPT
-A INPUT -p icmp --icmp-type echo-reply -j ACCEPT
-A INPUT -p icmp --icmp-type destination-unreachable -j ACCEPT
-A INPUT -p icmp --icmp-type time-exceeded -j ACCEPT

# Drop invalid packets
-A INPUT -m conntrack --ctstate INVALID -j DROP

# Log dropped packets
-A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-dropped: " --log-level 4

COMMIT

*raw
:PREROUTING ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]

# DDoS protection
-A PREROUTING -m conntrack --ctstate INVALID -j DROP
-A PREROUTING -p tcp ! --syn -m conntrack --ctstate NEW -j DROP
-A PREROUTING -p tcp --tcp-flags ALL ALL -j DROP
-A PREROUTING -p tcp --tcp-flags ALL NONE -j DROP

COMMIT
EOF
        
        # Apply rules
        iptables-restore < /etc/iptables/rules.v4
        
        # Make persistent
        cat > /etc/systemd/system/iptables.service << 'EOF'
[Unit]
Description=IPv4 Packet Filtering Framework
Before=network-pre.target
Wants=network-pre.target

[Service]
Type=oneshot
ExecStart=/sbin/iptables-restore /etc/iptables/rules.v4
ExecReload=/sbin/iptables-restore /etc/iptables/rules.v4
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
        systemctl enable iptables.service
    fi
    
    log "GREEN" "Firewall configuration complete"
}

# Audit Configuration
configure_audit() {
    log "YELLOW" "Configuring audit system..."
    
    # Install auditd if not present
    if ! command -v auditctl >/dev/null 2>&1; then
        apt-get install -y auditd audispd-plugins
    fi
    
    # Configure audit rules
    cat > "$AUDIT_RULES" << 'EOF'
# Delete all existing rules
-D

# Buffer Size
-b 8192

# Failure Mode
-f 1

# Audit the audit logs
-w /var/log/audit/ -k auditlog

# Audit system configurations
-w /etc/audit/ -p wa -k auditconfig
-w /etc/libaudit.conf -p wa -k auditconfig
-w /etc/audisp/ -p wa -k audispconfig
-w /sbin/auditctl -p x -k audittools
-w /sbin/auditd -p x -k audittools

# Authentication and authorization
-w /etc/sudoers -p wa -k sudo_modification
-w /etc/sudoers.d/ -p wa -k sudo_modification
-w /usr/bin/passwd -p x -k passwd_modification
-w /usr/bin/su -p x -k su_execution
-w /usr/bin/sudo -p x -k sudo_execution
-w /etc/shadow -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/passwd -p wa -k identity
-w /etc/gshadow -p wa -k identity

# System startup scripts
-w /etc/rc.local -p wa -k init
-w /etc/systemd/ -p wa -k systemd
-w /lib/systemd/ -p wa -k systemd

# SSH configuration
-w /etc/ssh/sshd_config -p wa -k sshd_config

# Kernel modules
-w /sbin/insmod -p x -k modules
-w /sbin/rmmod -p x -k modules
-w /sbin/modprobe -p x -k modules
-a always,exit -F arch=b64 -S init_module,delete_module,finit_module -k modules

# Time changes
-a always,exit -F arch=b64 -S adjtimex,settimeofday -k time_change
-a always,exit -F arch=b64 -S clock_settime -k time_change
-w /etc/localtime -p wa -k time_change

# Network configuration
-a always,exit -F arch=b64 -S sethostname,setdomainname -k network_modifications
-w /etc/hosts -p wa -k network_modifications
-w /etc/network/ -p wa -k network_modifications
-w /etc/sysconfig/network -p wa -k network_modifications

# File operations
-a always,exit -F arch=b64 -S unlink,unlinkat,rename,renameat -F auid>=1000 -F auid!=4294967295 -k delete
-a always,exit -F arch=b64 -S chmod,fchmod,fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_modification
-a always,exit -F arch=b64 -S chown,fchown,fchownat,lchown -F auid>=1000 -F auid!=4294967295 -k perm_modification
-a always,exit -F arch=b64 -S setxattr,lsetxattr,fsetxattr,removexattr,lremovexattr,fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_modification

# Process tracking
-a always,exit -F arch=b64 -S kill -k process_termination
-a always,exit -F arch=b64 -S execve -C uid!=euid -F key=privesc
-a always,exit -F arch=b64 -S execve -C gid!=egid -F key=privesc

# Make configuration immutable
-e 2
EOF
    
    # Load audit rules
    auditctl -R "$AUDIT_RULES"
    
    # Configure audit daemon
    sed -i 's/^space_left_action.*/space_left_action = SYSLOG/' /etc/audit/auditd.conf
    sed -i 's/^admin_space_left_action.*/admin_space_left_action = HALT/' /etc/audit/auditd.conf
    sed -i 's/^max_log_file_action.*/max_log_file_action = ROTATE/' /etc/audit/auditd.conf
    sed -i 's/^num_logs.*/num_logs = 10/' /etc/audit/auditd.conf
    
    # Enable and restart audit
    systemctl enable auditd
    systemctl restart auditd
    
    log "GREEN" "Audit configuration complete"
}

# File Permissions and AIDE
secure_file_permissions() {
    log "YELLOW" "Securing file permissions..."
    
    # Set secure permissions on sensitive files
    local files=(
        "/etc/passwd:644"
        "/etc/shadow:640"
        "/etc/group:644"
        "/etc/gshadow:640"
        "/etc/sudoers:440"
        "/etc/ssh/sshd_config:600"
        "/etc/crontab:600"
        "/etc/cron.hourly:700"
        "/etc/cron.daily:700"
        "/etc/cron.weekly:700"
        "/etc/cron.monthly:700"
        "/etc/cron.d:700"
        "/var/log:755"
        "/var/log/audit:750"
    )
    
    for file_perm in "${files[@]}"; do
        IFS=':' read -r file perm <<< "$file_perm"
        if [[ -e "$file" ]]; then
            chmod "$perm" "$file"
            log "GREEN" "Set permissions $perm on $file"
        fi
    done
    
    # Find and fix world-writable files
    log "YELLOW" "Checking for world-writable files..."
    find / -xdev -type f -perm -002 2>/dev/null | while read -r file; do
        if [[ ! "$file" =~ ^/proc|^/sys|^/dev|^/tmp|^/var/tmp ]]; then
            log "RED" "Found world-writable file: $file"
            chmod o-w "$file"
        fi
    done
    
    # Find and fix unowned files
    find / -xdev \( -nouser -o -nogroup \) 2>/dev/null | while read -r file; do
        log "RED" "Found unowned file: $file"
        chown root:root "$file"
    done
    
    # Install and configure AIDE
    if ! command -v aide >/dev/null 2>&1; then
        apt-get install -y aide
    fi
    
    # Configure AIDE
    cat > /etc/aide/aide.conf.d/99-custom << 'EOF'
# Custom AIDE rules
/bin p+i+n+u+g+s+b+m+c+md5+sha256
/sbin p+i+n+u+g+s+b+m+c+md5+sha256
/usr/bin p+i+n+u+g+s+b+m+c+md5+sha256
/usr/sbin p+i+n+u+g+s+b+m+c+md5+sha256
/lib p+i+n+u+g+s+b+m+c+md5+sha256
/lib64 p+i+n+u+g+s+b+m+c+md5+sha256
/etc p+i+n+u+g+s+b+m+c+md5+sha256
!/var/log
!/var/cache
!/var/tmp
EOF
    
    # Initialize AIDE database
    log "YELLOW" "Initializing AIDE database (this may take a while)..."
    aideinit
    cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db
    
    # Schedule AIDE checks
    cat > /etc/cron.daily/aide-check << 'EOF'
#!/bin/bash
/usr/bin/aide --check | /usr/bin/mail -s "AIDE Report for $(hostname)" root
EOF
    chmod 755 /etc/cron.daily/aide-check
    
    log "GREEN" "File permissions secured"
}

# SELinux/AppArmor Configuration
configure_mac() {
    log "YELLOW" "Configuring Mandatory Access Control..."
    
    # Check which MAC system is available
    if command -v getenforce >/dev/null 2>&1; then
        # SELinux
        log "YELLOW" "Configuring SELinux..."
        
        # Set to enforcing mode
        setenforce 1 2>/dev/null || true
        sed -i 's/^SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config
        
        # Restore contexts
        restorecon -R /etc /var /home
        
        log "GREEN" "SELinux configured in enforcing mode"
        
    elif command -v aa-status >/dev/null 2>&1; then
        # AppArmor
        log "YELLOW" "Configuring AppArmor..."
        
        # Enable AppArmor
        systemctl enable apparmor
        systemctl start apparmor
        
        # Set profiles to enforce mode
        aa-enforce /etc/apparmor.d/*
        
        log "GREEN" "AppArmor configured and enforced"
    else
        log "RED" "No MAC system found. Consider installing SELinux or AppArmor."
    fi
}

# Security Tools Installation
install_security_tools() {
    log "YELLOW" "Installing security tools..."
    
    # Update package database
    apt-get update
    
    # Install security packages
    local packages=(
        "fail2ban"          # Intrusion prevention
        "rkhunter"          # Rootkit scanner
        "chkrootkit"        # Another rootkit scanner
        "lynis"             # Security auditing
        "unhide"            # Hidden process detector
        "acct"              # Process accounting
        "sysstat"           # System monitoring
        "libpam-tmpdir"     # Secure temp directories
        "apt-listbugs"      # Check for bugs before upgrade
        "apt-listchanges"   # Review changes before upgrade
        "needrestart"       # Check for services needing restart
        "debsums"           # Verify package integrity
    )
    
    for package in "${packages[@]}"; do
        if ! dpkg -l "$package" >/dev/null 2>&1; then
            apt-get install -y "$package" || log "RED" "Failed to install $package"
        fi
    done
    
    # Configure fail2ban
    cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
destemail = root@localhost
sendername = Fail2Ban
action = %(action_mwl)s

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
backend = %(sshd_backend)s

[sshd-ddos]
enabled = true
port = ssh
logpath = %(sshd_log)s
backend = %(sshd_backend)s
EOF
    
    systemctl enable fail2ban
    systemctl restart fail2ban
    
    # Configure process accounting
    systemctl enable acct
    systemctl start acct
    
    log "GREEN" "Security tools installed and configured"
}

# Generate Security Report
generate_security_report() {
    local report_file="/root/security-report-$(date +%Y%m%d-%H%M%S).txt"
    
    log "YELLOW" "Generating security report..."
    
    {
        echo "=== Linux Security Hardening Report ==="
        echo "Date: $(date)"
        echo "Hostname: $(hostname)"
        echo
        
        echo "=== User Accounts ==="
        echo "Users with UID 0:"
        awk -F: '($3 == 0) { print $1 }' /etc/passwd
        echo
        echo "Users with empty passwords:"
        awk -F: '($2 == "" ) { print $1 }' /etc/shadow || echo "None found"
        echo
        
        echo "=== SSH Configuration ==="
        sshd -T | grep -E "permitrootlogin|passwordauthentication|pubkeyauthentication"
        echo
        
        echo "=== Kernel Parameters ==="
        sysctl -a 2>/dev/null | grep -E "randomize_va_space|ptrace_scope|dmesg_restrict"
        echo
        
        echo "=== Firewall Status ==="
        if command -v ufw >/dev/null 2>&1; then
            ufw status verbose
        else
            iptables -L -n -v
        fi
        echo
        
        echo "=== Running Services ==="
        systemctl list-units --type=service --state=running --no-pager
        echo
        
        echo "=== Open Ports ==="
        ss -tuln
        echo
        
        echo "=== Recent Authentication Failures ==="
        journalctl -u ssh -p warning --since "1 day ago" --no-pager | head -20
        echo
        
        echo "=== Scheduled Tasks ==="
        echo "System crontab:"
        cat /etc/crontab
        echo
        echo "User crontabs:"
        for user in $(cut -f1 -d: /etc/passwd); do
            crontab -u "$user" -l 2>/dev/null && echo "User: $user"
        done
        echo
        
        echo "=== SUID/SGID Files ==="
        find / -type f \( -perm -4000 -o -perm -2000 \) -exec ls -l {} \; 2>/dev/null | head -20
        echo
        
        echo "=== Security Tool Status ==="
        if command -v fail2ban-client >/dev/null 2>&1; then
            echo "Fail2ban status:"
            fail2ban-client status
        fi
        
        if command -v aa-status >/dev/null 2>&1; then
            echo "AppArmor status:"
            aa-status --complaining
        fi
        
        if command -v getenforce >/dev/null 2>&1; then
            echo "SELinux status: $(getenforce)"
        fi
    } > "$report_file"
    
    log "GREEN" "Security report generated: $report_file"
}

# Main execution
main() {
    if [[ $EUID -ne 0 ]]; then
        echo "This script must be run as root"
        exit 1
    fi
    
    log "YELLOW" "Starting Linux security hardening..."
    
    # Create backup first
    create_backup
    
    # Execute hardening steps
    harden_users_auth
    harden_ssh
    harden_kernel
    configure_firewall
    configure_audit
    secure_file_permissions
    configure_mac
    install_security_tools
    
    # Generate report
    generate_security_report
    
    log "GREEN" "Security hardening complete!"
    log "YELLOW" "Please review the security report and reboot the system"
    
    # Remind about important next steps
    cat << EOF

=== Important Next Steps ===
1. Review the security report in /root/
2. Test SSH access before closing current session
3. Configure specific firewall rules for your services
4. Set up centralized logging
5. Configure backup procedures
6. Schedule regular security audits
7. Reboot the system to apply all changes

EOF
}

# Run main function
main
```

## Best Practices

### 1. Access Control and Authentication
```bash
# Multi-factor authentication setup
configure_2fa() {
    # Install Google Authenticator
    apt-get install -y libpam-google-authenticator
    
    # Configure PAM for SSH
    cat >> /etc/pam.d/sshd << 'EOF'
# Two-factor authentication
auth required pam_google_authenticator.so nullok
EOF
    
    # Enable in SSH
    sed -i 's/^ChallengeResponseAuthentication.*/ChallengeResponseAuthentication yes/' /etc/ssh/sshd_config
    sed -i 's/^AuthenticationMethods.*/AuthenticationMethods publickey,keyboard-interactive/' /etc/ssh/sshd_config
    
    # User setup script
    cat > /usr/local/bin/setup-2fa << 'EOF'
#!/bin/bash
user="${1:-$USER}"
su - "$user" -c "google-authenticator -t -d -f -r 3 -R 30 -w 3"
echo "2FA setup complete for user: $user"
EOF
    chmod +x /usr/local/bin/setup-2fa
}

# Certificate-based authentication
setup_cert_auth() {
    # Create CA structure
    mkdir -p /etc/pki/CA/{certs,private,crl}
    
    # Generate CA key and certificate
    openssl genrsa -aes256 -out /etc/pki/CA/private/ca.key 4096
    openssl req -new -x509 -days 3650 -key /etc/pki/CA/private/ca.key \
        -out /etc/pki/CA/certs/ca.crt \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=Internal CA"
    
    # Configure SSH for certificate authentication
    cat >> /etc/ssh/sshd_config << EOF
TrustedUserCAKeys /etc/ssh/ca.pub
AuthorizedKeysFile none
EOF
    
    # Script to sign user certificates
    cat > /usr/local/bin/sign-ssh-cert << 'EOF'
#!/bin/bash
user=$1
validity=${2:-"1d"}
ssh-keygen -s /etc/ssh/ca -I "$user" -n "$user" -V "+$validity" "$user.pub"
EOF
    chmod +x /usr/local/bin/sign-ssh-cert
}
```

### 2. Network Security
```bash
# Advanced firewall rules with rate limiting
configure_advanced_firewall() {
    # DDoS protection with iptables
    cat > /usr/local/bin/setup-ddos-protection << 'EOF'
#!/bin/bash

# Connection limit per IP
iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 100 -j REJECT
iptables -A INPUT -p tcp --dport 443 -m connlimit --connlimit-above 100 -j REJECT

# SYN flood protection
iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j RETURN
iptables -A INPUT -p tcp --syn -j DROP

# Port scan detection
iptables -N PORT_SCANNING
iptables -A PORT_SCANNING -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s -j RETURN
iptables -A PORT_SCANNING -j DROP

# Invalid packet dropping
iptables -A INPUT -m state --state INVALID -j DROP
iptables -A FORWARD -m state --state INVALID -j DROP
iptables -A OUTPUT -m state --state INVALID -j DROP

# Rate limiting for SSH
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP

# ICMP rate limiting
iptables -A INPUT -p icmp -m limit --limit 1/s --limit-burst 1 -j ACCEPT
iptables -A INPUT -p icmp -j DROP
EOF
    chmod +x /usr/local/bin/setup-ddos-protection
    
    # Network segmentation with VLANs
    cat > /etc/netplan/01-vlans.yaml << 'EOF'
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
  vlans:
    vlan10:
      id: 10
      link: eth0
      addresses: [10.10.10.1/24]
    vlan20:
      id: 20
      link: eth0
      addresses: [10.20.20.1/24]
EOF
}

# IDS/IPS setup with Suricata
setup_suricata() {
    apt-get install -y suricata
    
    # Basic configuration
    cat > /etc/suricata/suricata.yaml << 'EOF'
vars:
  address-groups:
    HOME_NET: "[10.0.0.0/8,192.168.0.0/16,172.16.0.0/12]"
    EXTERNAL_NET: "!$HOME_NET"

af-packet:
  - interface: eth0
    threads: 4
    cluster-type: cluster_flow
    defrag: yes

logging:
  default-log-level: notice
  outputs:
  - fast:
      enabled: yes
      filename: fast.log
  - eve-log:
      enabled: yes
      filetype: json
      filename: eve.json

rule-files:
  - suricata.rules
EOF
    
    # Enable and start
    systemctl enable suricata
    systemctl start suricata
}
```

### 3. System Integrity Monitoring
```bash
# OSSEC installation and configuration
setup_ossec() {
    # Download and install OSSEC
    cd /tmp
    wget https://github.com/ossec/ossec-hids/releases/download/3.6.0/ossec-hids-3.6.0.tar.gz
    tar -xzf ossec-hids-3.6.0.tar.gz
    cd ossec-hids-3.6.0
    
    # Automated installation
    cat > /tmp/ossec-preloaded.conf << 'EOF'
USER_LANGUAGE="en"
USER_NO_STOP="y"
USER_INSTALL_TYPE="local"
USER_DIR="/var/ossec"
USER_ENABLE_SYSLOG="y"
USER_ENABLE_ROOTCHECK="y"
USER_UPDATE_RULES="y"
USER_ENABLE_EMAIL="y"
USER_EMAIL_ADDRESS="security@example.com"
USER_EMAIL_SMTP="localhost"
EOF
    
    ./install.sh < /tmp/ossec-preloaded.conf
    
    # Custom rules
    cat > /var/ossec/rules/local_rules.xml << 'EOF'
<group name="local,">
  <rule id="100001" level="10">
    <if_sid>5712</if_sid>
    <match>sudo</match>
    <description>SUDO command executed</description>
  </rule>
  
  <rule id="100002" level="12">
    <if_sid>5501</if_sid>
    <srcip>!10.0.0.0/8</srcip>
    <description>SSH login from external network</description>
  </rule>
</group>
EOF
    
    # Start OSSEC
    /var/ossec/bin/ossec-control start
}

# Custom file integrity monitoring
create_fim_script() {
    cat > /usr/local/bin/fim-check << 'EOF'
#!/bin/bash
#
# File Integrity Monitoring Script

FIM_DB="/var/lib/fim/checksums.db"
ALERT_LOG="/var/log/fim-alerts.log"
DIRS_TO_MONITOR="/etc /bin /sbin /usr/bin /usr/sbin /lib /usr/lib"

# Create hash database
create_baseline() {
    mkdir -p $(dirname "$FIM_DB")
    > "$FIM_DB"
    
    for dir in $DIRS_TO_MONITOR; do
        find "$dir" -type f -exec sha256sum {} \; >> "$FIM_DB" 2>/dev/null
    done
    
    echo "Baseline created with $(wc -l < "$FIM_DB") files"
}

# Check for changes
check_integrity() {
    local temp_db=$(mktemp)
    local changes=0
    
    for dir in $DIRS_TO_MONITOR; do
        find "$dir" -type f -exec sha256sum {} \; >> "$temp_db" 2>/dev/null
    done
    
    # Compare with baseline
    while IFS=' ' read -r hash file; do
        if ! grep -q "^$hash  $file$" "$FIM_DB"; then
            echo "[$(date)] MODIFIED: $file" >> "$ALERT_LOG"
            ((changes++))
        fi
    done < "$temp_db"
    
    # Check for deleted files
    while IFS=' ' read -r hash file; do
        if [[ ! -f "$file" ]]; then
            echo "[$(date)] DELETED: $file" >> "$ALERT_LOG"
            ((changes++))
        fi
    done < "$FIM_DB"
    
    rm -f "$temp_db"
    
    if [[ $changes -gt 0 ]]; then
        echo "Found $changes file integrity violations. Check $ALERT_LOG"
        return 1
    fi
    
    return 0
}

case "${1:-check}" in
    baseline)
        create_baseline
        ;;
    check)
        check_integrity
        ;;
    *)
        echo "Usage: $0 {baseline|check}"
        ;;
esac
EOF
    
    chmod +x /usr/local/bin/fim-check
    
    # Schedule regular checks
    echo "0 * * * * /usr/local/bin/fim-check check" | crontab -
}
```

### 4. Incident Response
```bash
# Incident response toolkit
create_ir_toolkit() {
    mkdir -p /opt/ir-toolkit/{scripts,evidence,reports}
    
    # Evidence collection script
    cat > /opt/ir-toolkit/scripts/collect-evidence.sh << 'EOF'
#!/bin/bash
#
# Incident Response Evidence Collection

CASE_ID="${1:-$(date +%Y%m%d-%H%M%S)}"
EVIDENCE_DIR="/opt/ir-toolkit/evidence/$CASE_ID"
mkdir -p "$EVIDENCE_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$EVIDENCE_DIR/collection.log"
}

# System information
collect_system_info() {
    log "Collecting system information..."
    
    # Basic system info
    date > "$EVIDENCE_DIR/date.txt"
    hostname > "$EVIDENCE_DIR/hostname.txt"
    uname -a > "$EVIDENCE_DIR/uname.txt"
    uptime > "$EVIDENCE_DIR/uptime.txt"
    
    # Running processes
    ps auxww > "$EVIDENCE_DIR/ps-aux.txt"
    ps -ef --forest > "$EVIDENCE_DIR/ps-tree.txt"
    
    # Network connections
    ss -tanup > "$EVIDENCE_DIR/connections.txt"
    netstat -rn > "$EVIDENCE_DIR/routes.txt"
    arp -an > "$EVIDENCE_DIR/arp.txt"
    
    # Open files
    lsof -n > "$EVIDENCE_DIR/lsof.txt"
    
    # Loaded modules
    lsmod > "$EVIDENCE_DIR/lsmod.txt"
    
    # Users and groups
    cp /etc/passwd "$EVIDENCE_DIR/"
    cp /etc/shadow "$EVIDENCE_DIR/" 2>/dev/null
    cp /etc/group "$EVIDENCE_DIR/"
    lastlog > "$EVIDENCE_DIR/lastlog.txt"
    who -a > "$EVIDENCE_DIR/who.txt"
    w > "$EVIDENCE_DIR/w.txt"
}

# Memory collection
collect_memory() {
    log "Collecting memory dump..."
    
    if command -v LiME >/dev/null 2>&1; then
        insmod /path/to/lime.ko "path=$EVIDENCE_DIR/memory.lime format=lime"
    else
        log "WARNING: LiME not available for memory collection"
    fi
}

# Log collection
collect_logs() {
    log "Collecting system logs..."
    
    # System logs
    mkdir -p "$EVIDENCE_DIR/logs"
    cp -r /var/log/* "$EVIDENCE_DIR/logs/" 2>/dev/null
    
    # Journal logs
    journalctl --all --output=export > "$EVIDENCE_DIR/journal.export"
    
    # Audit logs
    if [[ -d /var/log/audit ]]; then
        cp -r /var/log/audit "$EVIDENCE_DIR/"
    fi
}

# Timeline generation
generate_timeline() {
    log "Generating timeline..."
    
    # MAC times
    find / -xdev -printf "%T@ %A@ %C@ %p\n" 2>/dev/null | \
        sort -n > "$EVIDENCE_DIR/timeline-raw.txt"
    
    # Process timeline from logs
    grep -h "started\|stopped\|failed" "$EVIDENCE_DIR/logs/syslog"* | \
        sort > "$EVIDENCE_DIR/process-timeline.txt"
}

# Package verification
verify_packages() {
    log "Verifying installed packages..."
    
    if command -v rpm >/dev/null 2>&1; then
        rpm -Va > "$EVIDENCE_DIR/rpm-verify.txt" 2>&1
    elif command -v debsums >/dev/null 2>&1; then
        debsums -c > "$EVIDENCE_DIR/debsums-changed.txt" 2>&1
        debsums -a > "$EVIDENCE_DIR/debsums-all.txt" 2>&1
    fi
}

# Create report
create_report() {
    cat > "$EVIDENCE_DIR/incident-report.md" << EOF
# Incident Response Report

**Case ID:** $CASE_ID  
**Date:** $(date)  
**System:** $(hostname)

## Executive Summary

Evidence collection completed for incident response case $CASE_ID.

## Evidence Collected

- System information
- Process listings
- Network connections
- Open files
- System logs
- Package integrity

## Initial Findings

### Suspicious Processes
$(grep -E "nc |/tmp/|/var/tmp/|curl|wget" "$EVIDENCE_DIR/ps-aux.txt" | head -10)

### Unusual Network Connections
$(grep -E "ESTABLISHED|LISTEN" "$EVIDENCE_DIR/connections.txt" | grep -v "127.0.0.1" | head -10)

### Recent Authentication
$(grep "Accepted\|Failed" "$EVIDENCE_DIR/logs/auth.log" | tail -20)

## Recommendations

1. Isolate the system from network
2. Preserve evidence before any remediation
3. Analyze memory dump for malware
4. Review timeline for initial compromise

EOF
}

# Main collection
main() {
    log "Starting evidence collection for case: $CASE_ID"
    
    collect_system_info
    collect_memory
    collect_logs
    generate_timeline
    verify_packages
    create_report
    
    # Create archive
    cd /opt/ir-toolkit/evidence
    tar czf "$CASE_ID.tar.gz" "$CASE_ID/"
    
    log "Evidence collection complete: $EVIDENCE_DIR"
    log "Archive created: /opt/ir-toolkit/evidence/$CASE_ID.tar.gz"
}

main
EOF
    
    chmod +x /opt/ir-toolkit/scripts/collect-evidence.sh
}
```

## Common Commands and Operations

### Security Auditing
```bash
# System security audit
lynis audit system

# Check for rootkits
rkhunter --check --skip-keypress
chkrootkit

# Find SUID/SGID binaries
find / -type f \( -perm -4000 -o -perm -2000 \) -exec ls -l {} \; 2>/dev/null

# Check for world-writable directories
find / -type d -perm -002 ! -perm -1000 2>/dev/null

# List all cron jobs
for user in $(cut -f1 -d: /etc/passwd); do
    echo "=== Crontab for $user ==="
    crontab -u "$user" -l 2>/dev/null
done

# Check listening services
ss -tulpn
lsof -i -P -n

# Review sudo access
grep -v '^#' /etc/sudoers | grep -v '^$'
ls -la /etc/sudoers.d/
```

### User and Access Management
```bash
# User account review
awk -F: '($3 >= 1000) {print $1}' /etc/passwd
awk -F: '($3 == 0) {print $1}' /etc/passwd

# Check password policies
chage -l username
grep "^PASS" /etc/login.defs

# Find users with no password
awk -F: '($2 == "") {print $1}' /etc/shadow

# List failed login attempts
grep "Failed password" /var/log/auth.log | tail -20
lastb | head -20

# Lock/unlock accounts
passwd -l username
passwd -u username

# Force password change
chage -d 0 username
```

### Firewall Management
```bash
# iptables rules
iptables -L -v -n --line-numbers
iptables -t nat -L -v -n
iptables -t mangle -L -v -n

# Save/restore rules
iptables-save > /etc/iptables/rules.v4
iptables-restore < /etc/iptables/rules.v4

# UFW management
ufw status verbose
ufw show raw
ufw allow from 10.0.0.0/8 to any port 22
ufw delete allow 80

# nftables (modern replacement)
nft list ruleset
nft add rule inet filter input tcp dport 22 accept
```

### Log Analysis
```bash
# Authentication logs
grep "sshd" /var/log/auth.log | grep -E "Accepted|Failed"
journalctl -u sshd --since "1 hour ago"

# Sudo usage
grep sudo /var/log/auth.log | grep COMMAND

# System errors
journalctl -p err --since today

# Audit log queries
ausearch -m USER_LOGIN -sv no
ausearch -f /etc/passwd -i
aureport -au

# Log file integrity
grep -v "^#" /etc/rsyslog.conf | grep -v "^$"
```

### Security Monitoring
```bash
# Real-time file monitoring
inotifywait -m -r /etc --format '%w%f %e' 

# Process monitoring
while true; do
    ps aux | awk '{print $11}' | sort | uniq -c | sort -rn | head -20
    sleep 5
    clear
done

# Network monitoring
tcpdump -i any -n -c 1000 'not port 22'
tshark -i eth0 -Y "http.request"

# System call monitoring
strace -e trace=network -p $PID
strace -e trace=file -p $PID
```

## Interview Tips

### Key Topics to Master
1. **Linux Security Models**: DAC vs MAC, capabilities, SELinux/AppArmor
2. **Cryptography**: Encryption types, key management, certificates
3. **Network Security**: Firewall rules, VPNs, network segmentation
4. **Incident Response**: Evidence collection, forensics, remediation
5. **Compliance**: Understanding frameworks (PCI DSS, HIPAA, SOC 2)
6. **Threat Landscape**: Common attack vectors, defense strategies

### Common Interview Questions
1. "Describe your approach to hardening a Linux server"
   - Start with minimal installation
   - Apply security updates
   - Configure firewall and access controls
   - Implement monitoring and logging
   - Regular security audits

2. "How do you investigate a potential security breach?"
   - Isolate the system
   - Collect evidence (logs, memory, files)
   - Analyze timeline
   - Identify indicators of compromise
   - Document findings

3. "Explain the difference between SELinux and AppArmor"
   - SELinux: Label-based MAC, more granular
   - AppArmor: Path-based MAC, easier to manage
   - Both provide mandatory access control
   - Choice depends on requirements

4. "How do you secure SSH access?"
   - Disable root login
   - Use key-based authentication
   - Implement 2FA
   - Restrict source IPs
   - Use non-standard ports (controversial)

### Practical Scenarios
Be prepared to:
- Write firewall rules for specific scenarios
- Analyze log files for security events
- Design a security architecture
- Respond to a security incident
- Implement compliance requirements

## Essential Resources

### Books
1. **"Linux Security Cookbook"** by Daniel Barrett
   - Practical security recipes
   - Real-world scenarios

2. **"Practical Linux Security Cookbook"** by Tajinder Kalsi
   - Step-by-step security guides
   - Modern tools and techniques

3. **"Linux Hardening in Hostile Networks"** by Kyle Rankin
   - Defense strategies
   - Incident response

4. **"SELinux System Administration"** by Sven Vermeulen
   - Comprehensive SELinux guide
   - Policy development

5. **"Applied Network Security Monitoring"** by Chris Sanders
   - Detection and analysis
   - Security operations

### Certifications and Training
1. **CompTIA Security+**: Foundation security concepts
2. **Linux Professional Institute Security**: Linux-specific security
3. **SANS SEC506**: Securing Linux/Unix
4. **Red Hat Security**: RHEL security specialization
5. **CIS Controls**: Security best practices

### Online Resources
1. **CIS Benchmarks**: Security configuration guides
2. **OWASP**: Application security resources
3. **NIST Cybersecurity Framework**: Security standards
4. **Linux Security**: kernel.org security resources
5. **CVE Database**: Vulnerability tracking

### Tools and Frameworks
1. **Security Scanners**: Nessus, OpenVAS, Lynis
2. **IDS/IPS**: Snort, Suricata, OSSEC
3. **SIEM**: Elastic Stack, Splunk, Graylog
4. **Forensics**: Volatility, Autopsy, SIFT
5. **Penetration Testing**: Kali Linux, Metasploit

### Communities and Forums
1. **r/netsec**: Network security discussions
2. **Security StackExchange**: Q&A platform
3. **SANS Internet Storm Center**: Threat intelligence
4. **Linux Security Mailing Lists**: Kernel security
5. **Local Security Groups**: ISACA, (ISC)², ISSA chapters

### Blogs and Podcasts
1. **Krebs on Security**: Security news and analysis
2. **SANS StormCast**: Daily security podcast
3. **Linux Security Weekly**: Video podcast
4. **Darknet Diaries**: Security stories
5. **Schneier on Security**: Security analysis

Remember, Linux security is an ongoing process, not a destination. Stay informed about new threats, regularly update your systems, and maintain a security-first mindset. Always balance security requirements with operational needs, and document your security decisions for future reference and compliance requirements.