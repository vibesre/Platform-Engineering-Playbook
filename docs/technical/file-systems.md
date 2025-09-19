---
title: "Linux File Systems"
description: "Deep dive into Linux file systems - ext4, XFS, ZFS, Btrfs and advanced storage management"
---

# Linux File Systems

Understanding Linux file systems is crucial for platform engineers managing storage infrastructure. File systems determine how data is organized, stored, and retrieved, directly impacting performance, reliability, and scalability. This comprehensive guide covers major Linux file systems including ext4, XFS, ZFS, and Btrfs, along with advanced storage management techniques, performance optimization, and troubleshooting strategies essential for modern infrastructure.

## Core Concepts and Features

### File System Fundamentals
A file system provides:
- **Data Organization**: How files and directories are structured
- **Metadata Management**: Permissions, timestamps, ownership
- **Space Allocation**: Block allocation and management
- **Integrity Features**: Journaling, checksums, snapshots
- **Performance Optimization**: Caching, read-ahead, delayed allocation

### Key File System Components
1. **Superblock**: File system metadata
2. **Inodes**: File metadata structures
3. **Data Blocks**: Actual file content
4. **Journal**: Transaction log for consistency
5. **Block Groups**: Logical grouping of blocks

### Major Linux File Systems

#### ext4 (Fourth Extended File System)
- **Mature**: Most widely used Linux file system
- **Journaling**: Ensures consistency after crashes
- **Extents**: Efficient large file handling
- **Backwards Compatible**: With ext3 and ext2
- **Maximum File Size**: 16 TiB
- **Maximum Volume Size**: 1 EiB

#### XFS
- **High Performance**: Optimized for large files
- **Scalable**: Handles massive storage systems
- **Parallel I/O**: Better multi-threaded performance
- **Dynamic Allocation**: Efficient space usage
- **Maximum File Size**: 8 EiB
- **Maximum Volume Size**: 8 EiB

#### ZFS
- **Advanced Features**: Snapshots, clones, replication
- **Data Integrity**: End-to-end checksums
- **Built-in RAID**: RAID-Z implementations
- **Compression**: Multiple algorithms supported
- **Copy-on-Write**: Ensures consistency
- **Pooled Storage**: Flexible volume management

#### Btrfs
- **Modern Design**: Copy-on-write architecture
- **Snapshots**: Instant, space-efficient
- **Subvolumes**: Multiple file system roots
- **Self-Healing**: With checksums and redundancy
- **Online Operations**: Defrag, resize, balance
- **RAID Support**: Built-in RAID levels

## Common Use Cases

### Enterprise Storage
- Database servers requiring consistent performance
- File servers with large capacity needs
- Backup systems with snapshot requirements
- Virtual machine storage

### High-Performance Computing
- Scientific computing with large datasets
- Media production and rendering
- Big data analytics platforms
- Machine learning workloads

### Cloud and Containers
- Container image storage
- Persistent volume management
- Multi-tenant storage isolation
- Distributed storage systems

### Archival and Backup
- Long-term data retention
- Deduplication and compression
- Snapshot-based backups
- Replication targets

## Getting Started Example

Here's a comprehensive example demonstrating file system operations:

```bash
#!/bin/bash
#
# Comprehensive File System Management Script
# Demonstrates creation, optimization, and management of various file systems

set -euo pipefail

# Configuration
DISK_DEVICE="/dev/sdb"
MOUNT_BASE="/mnt"
LOG_FILE="/var/log/filesystem-ops.log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Check prerequisites
check_prerequisites() {
    local required_tools=(mkfs.ext4 mkfs.xfs zfs btrfs)
    
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &>/dev/null; then
            log "WARNING: $tool not found. Some features may be unavailable."
        fi
    done
    
    if [[ ! -b "$DISK_DEVICE" ]]; then
        log "ERROR: Block device $DISK_DEVICE not found"
        exit 1
    fi
}

# ext4 File System Setup
setup_ext4() {
    local partition="${DISK_DEVICE}1"
    local mount_point="$MOUNT_BASE/ext4"
    
    log "Setting up ext4 file system..."
    
    # Create partition
    parted -s "$DISK_DEVICE" mklabel gpt
    parted -s "$DISK_DEVICE" mkpart primary ext4 1MiB 25%
    
    # Create ext4 file system with optimizations
    mkfs.ext4 -E lazy_itable_init=0,lazy_journal_init=0 \
              -O extent,dir_index,filetype,flex_bg,sparse_super2,metadata_csum,64bit \
              -m 1 \
              -L "ext4_data" \
              "$partition"
    
    # Tune file system parameters
    tune2fs -o journal_data_writeback "$partition"
    tune2fs -c 0 -i 0 "$partition"
    
    # Mount with optimized options
    mkdir -p "$mount_point"
    mount -o noatime,nodiratime,journal_checksum,journal_async_commit,data=writeback \
          "$partition" "$mount_point"
    
    # Create fstab entry
    echo "UUID=$(blkid -o value -s UUID $partition) $mount_point ext4 noatime,nodiratime,journal_checksum,journal_async_commit,data=writeback 0 2" >> /etc/fstab
    
    # Display file system information
    log "ext4 file system created:"
    df -h "$mount_point"
    dumpe2fs -h "$partition" | grep -E "Block count|Free blocks|Block size"
    
    # Performance test
    perform_io_test "$mount_point" "ext4"
}

# XFS File System Setup
setup_xfs() {
    local partition="${DISK_DEVICE}2"
    local mount_point="$MOUNT_BASE/xfs"
    
    log "Setting up XFS file system..."
    
    # Create partition
    parted -s "$DISK_DEVICE" mkpart primary xfs 25% 50%
    
    # Create XFS file system with optimizations
    mkfs.xfs -f \
             -L "xfs_data" \
             -d agcount=4,sunit=512,swidth=2048 \
             -l lazy-count=1,size=128m \
             -r extsize=256k \
             "$partition"
    
    # Mount with optimized options
    mkdir -p "$mount_point"
    mount -o noatime,nodiratime,nobarrier,inode64,allocsize=128m \
          "$partition" "$mount_point"
    
    # Set project quotas example
    xfs_quota -x -c "project -s -p /data 42" "$mount_point"
    xfs_quota -x -c "limit -p bhard=10g 42" "$mount_point"
    
    # Display file system information
    log "XFS file system created:"
    xfs_info "$mount_point"
    xfs_db -r -c "sb 0" -c "print" "$partition" | grep -E "dblocks|fdblocks"
    
    # Performance test
    perform_io_test "$mount_point" "xfs"
}

# ZFS Pool Setup
setup_zfs() {
    local partition1="${DISK_DEVICE}3"
    local partition2="${DISK_DEVICE}4"
    local pool_name="datapool"
    local mount_point="$MOUNT_BASE/zfs"
    
    log "Setting up ZFS pool..."
    
    # Create partitions
    parted -s "$DISK_DEVICE" mkpart primary 50% 75%
    parted -s "$DISK_DEVICE" mkpart primary 75% 100%
    
    # Load ZFS module
    modprobe zfs || {
        log "ERROR: ZFS module not available"
        return 1
    }
    
    # Create mirrored pool
    zpool create -f \
          -o ashift=12 \
          -o autoexpand=on \
          -o autoreplace=on \
          -O atime=off \
          -O compression=lz4 \
          -O normalization=formD \
          -O xattr=sa \
          -O acltype=posixacl \
          -O mountpoint="$mount_point" \
          "$pool_name" mirror "$partition1" "$partition2"
    
    # Create datasets with different properties
    zfs create -o recordsize=128k -o compression=gzip-9 "$pool_name/databases"
    zfs create -o recordsize=1M -o compression=lz4 "$pool_name/media"
    zfs create -o recordsize=8k -o compression=lz4 "$pool_name/logs"
    
    # Set quotas and reservations
    zfs set quota=100G "$pool_name/databases"
    zfs set reservation=50G "$pool_name/databases"
    
    # Enable deduplication (use with caution)
    # zfs set dedup=on "$pool_name/media"
    
    # Create snapshots
    zfs snapshot "$pool_name/databases@initial"
    zfs snapshot "$pool_name/media@initial"
    
    # Display pool information
    log "ZFS pool created:"
    zpool status "$pool_name"
    zfs list -t all
    zpool get all "$pool_name" | grep -E "size|free|allocated"
    
    # Performance test
    perform_io_test "$mount_point/databases" "zfs"
}

# Btrfs File System Setup
setup_btrfs() {
    local devices=("${DISK_DEVICE}5" "${DISK_DEVICE}6")
    local mount_point="$MOUNT_BASE/btrfs"
    
    log "Setting up Btrfs file system..."
    
    # Create partitions for Btrfs RAID1
    parted -s "$DISK_DEVICE" mklabel gpt  # Reset if needed
    parted -s "$DISK_DEVICE" mkpart primary 1MiB 50%
    parted -s "$DISK_DEVICE" mkpart primary 50% 100%
    
    # Create Btrfs with RAID1
    mkfs.btrfs -f \
               -L "btrfs_data" \
               -d raid1 \
               -m raid1 \
               "${devices[@]}"
    
    # Mount with optimized options
    mkdir -p "$mount_point"
    mount -o noatime,nodiratime,compress=zstd:3,space_cache=v2,autodefrag \
          "${devices[0]}" "$mount_point"
    
    # Create subvolumes
    btrfs subvolume create "$mount_point/@data"
    btrfs subvolume create "$mount_point/@snapshots"
    btrfs subvolume create "$mount_point/@backups"
    
    # Set default subvolume
    default_subvol_id=$(btrfs subvolume list "$mount_point" | grep "@data" | awk '{print $2}')
    btrfs subvolume set-default "$default_subvol_id" "$mount_point"
    
    # Create snapshot
    btrfs subvolume snapshot "$mount_point/@data" "$mount_point/@snapshots/data-$(date +%Y%m%d-%H%M%S)"
    
    # Enable quotas
    btrfs quota enable "$mount_point"
    btrfs qgroup create 1/0 "$mount_point"
    btrfs qgroup limit 100G 1/0 "$mount_point"
    
    # Display file system information
    log "Btrfs file system created:"
    btrfs filesystem show "$mount_point"
    btrfs filesystem df "$mount_point"
    btrfs device stats "$mount_point"
    
    # Performance test
    perform_io_test "$mount_point/@data" "btrfs"
}

# Performance testing function
perform_io_test() {
    local test_path="$1"
    local fs_type="$2"
    local test_file="$test_path/iotest"
    
    log "Running I/O performance test for $fs_type..."
    
    # Sequential write test
    dd if=/dev/zero of="$test_file" bs=1M count=1024 conv=fdatasync 2>&1 | \
        grep -E "bytes|MB/s" | tee -a "$LOG_FILE"
    
    # Sequential read test
    echo 3 > /proc/sys/vm/drop_caches
    dd if="$test_file" of=/dev/null bs=1M 2>&1 | \
        grep -E "bytes|MB/s" | tee -a "$LOG_FILE"
    
    # Random I/O test with fio
    if command -v fio &>/dev/null; then
        fio --name=random-rw \
            --ioengine=libaio \
            --rw=randrw \
            --bs=4k \
            --direct=1 \
            --size=1G \
            --numjobs=4 \
            --time_based \
            --runtime=60 \
            --group_reporting \
            --filename="$test_file" \
            --output-format=terse | tail -1 | cut -d';' -f8,49 | \
            awk -F';' '{printf "Random Read: %.2f MB/s, Random Write: %.2f MB/s\n", $1/1024, $2/1024}'
    fi
    
    rm -f "$test_file"
}

# Advanced storage management
advanced_storage_demo() {
    log "Demonstrating advanced storage features..."
    
    # LVM setup example
    if command -v lvm &>/dev/null; then
        log "Setting up LVM..."
        
        # Create physical volume
        pvcreate /dev/sdc1
        
        # Create volume group
        vgcreate datavg /dev/sdc1
        
        # Create logical volumes
        lvcreate -L 10G -n lv_data datavg
        lvcreate -L 5G -n lv_logs datavg
        
        # Create file systems on LVs
        mkfs.ext4 /dev/datavg/lv_data
        mkfs.xfs /dev/datavg/lv_logs
        
        # Demonstrate snapshot
        lvcreate -L 1G -s -n lv_data_snap /dev/datavg/lv_data
    fi
    
    # LUKS encryption example
    if command -v cryptsetup &>/dev/null; then
        log "Setting up encrypted volume..."
        
        # Create encrypted container
        echo -n "mypassword" | cryptsetup luksFormat /dev/sdd1 -
        
        # Open encrypted container
        echo -n "mypassword" | cryptsetup luksOpen /dev/sdd1 encrypted_data -
        
        # Create file system on encrypted device
        mkfs.ext4 /dev/mapper/encrypted_data
        
        # Mount encrypted file system
        mkdir -p /mnt/encrypted
        mount /dev/mapper/encrypted_data /mnt/encrypted
    fi
}

# File system maintenance utilities
create_maintenance_scripts() {
    # ext4 maintenance
    cat > /usr/local/bin/ext4-maintenance.sh << 'EOF'
#!/bin/bash
# ext4 file system maintenance

FS_PATH="$1"
DEVICE=$(findmnt -n -o SOURCE "$FS_PATH")

# Check and optimize
e2fsck -f -y "$DEVICE"
tune2fs -O extent,dir_index,filetype "$DEVICE"

# Defragmentation
e4defrag -v "$FS_PATH"

# Show fragmentation status
e4defrag -c "$FS_PATH"
EOF
    
    # XFS maintenance
    cat > /usr/local/bin/xfs-maintenance.sh << 'EOF'
#!/bin/bash
# XFS file system maintenance

FS_PATH="$1"

# Check file system
xfs_repair -n "$FS_PATH"

# Defragmentation
xfs_fsr -v "$FS_PATH"

# Show fragmentation
xfs_db -r -c "frag" $(findmnt -n -o SOURCE "$FS_PATH")
EOF
    
    # ZFS maintenance
    cat > /usr/local/bin/zfs-maintenance.sh << 'EOF'
#!/bin/bash
# ZFS pool maintenance

POOL="$1"

# Scrub pool
zpool scrub "$POOL"

# Check status
zpool status -v "$POOL"

# Clean up snapshots older than 30 days
zfs list -H -t snapshot -o name,creation | while read snap creation; do
    if [[ $(date -d "$creation" +%s) -lt $(date -d "30 days ago" +%s) ]]; then
        echo "Destroying old snapshot: $snap"
        zfs destroy "$snap"
    fi
done
EOF
    
    # Btrfs maintenance
    cat > /usr/local/bin/btrfs-maintenance.sh << 'EOF'
#!/bin/bash
# Btrfs file system maintenance

FS_PATH="$1"

# Scrub file system
btrfs scrub start "$FS_PATH"
btrfs scrub status "$FS_PATH"

# Balance file system
btrfs balance start -dusage=50 -musage=50 "$FS_PATH"

# Defragment
btrfs filesystem defragment -r -v "$FS_PATH"

# Clean up old snapshots
btrfs subvolume list "$FS_PATH" | grep "@snapshots" | while read -r line; do
    snapshot=$(echo "$line" | awk '{print $9}')
    # Add logic to remove old snapshots
done
EOF
    
    chmod +x /usr/local/bin/*-maintenance.sh
}

# Monitoring setup
setup_monitoring() {
    # Create monitoring script
    cat > /usr/local/bin/fs-monitor.sh << 'EOF'
#!/bin/bash
# File system monitoring script

LOG_FILE="/var/log/fs-monitor.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

# Check disk usage
check_disk_usage() {
    df -h | awk 'NR>1 && int($5)>80 {
        print "WARNING: " $6 " is " $5 " full"
    }' | while read line; do
        log "$line"
    done
}

# Check inode usage
check_inode_usage() {
    df -i | awk 'NR>1 && int($5)>80 {
        print "WARNING: " $6 " has " $5 " inodes used"
    }' | while read line; do
        log "$line"
    done
}

# Check file system errors
check_fs_errors() {
    dmesg | grep -E "EXT4-fs error|XFS.*error|BTRFS error" | tail -10 | while read line; do
        log "FS ERROR: $line"
    done
}

# Monitor I/O performance
monitor_io() {
    iostat -x 1 10 | awk '$1 ~ /^sd|^nvme/ && $12 > 90 {
        print "High I/O utilization on " $1 ": " $12 "%"
    }' | while read line; do
        log "$line"
    done
}

# Main monitoring loop
while true; do
    check_disk_usage
    check_inode_usage
    check_fs_errors
    monitor_io
    sleep 300
done
EOF
    
    chmod +x /usr/local/bin/fs-monitor.sh
    
    # Create systemd service
    cat > /etc/systemd/system/fs-monitor.service << 'EOF'
[Unit]
Description=File System Monitor
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/local/bin/fs-monitor.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl enable fs-monitor.service
    systemctl start fs-monitor.service
}

# Main execution
main() {
    log "Starting file system demonstration..."
    
    check_prerequisites
    
    # WARNING: This will partition the disk!
    read -p "This will partition $DISK_DEVICE. Continue? (yes/no): " confirm
    if [[ "$confirm" != "yes" ]]; then
        log "Aborted by user"
        exit 0
    fi
    
    # Setup different file systems
    setup_ext4
    setup_xfs
    setup_zfs
    setup_btrfs
    
    # Advanced features
    advanced_storage_demo
    
    # Create maintenance scripts
    create_maintenance_scripts
    
    # Setup monitoring
    setup_monitoring
    
    log "File system demonstration complete!"
}

# Execute main function
main
```

## Best Practices

### 1. File System Selection
```bash
# Decision matrix for file system selection
select_filesystem() {
    local use_case="$1"
    
    case "$use_case" in
        "general")
            echo "ext4 - Mature, stable, good all-around performance"
            ;;
        "large_files")
            echo "XFS - Optimized for large files and parallel I/O"
            ;;
        "snapshots")
            echo "ZFS or Btrfs - Built-in snapshot support"
            ;;
        "compression")
            echo "ZFS or Btrfs - Native compression support"
            ;;
        "database")
            echo "XFS or ZFS - Better for database workloads"
            ;;
        "virtualization")
            echo "ZFS - Snapshots, clones, and deduplication"
            ;;
    esac
}

# File system benchmarking
benchmark_filesystems() {
    local test_dir="/mnt/benchmark"
    local test_size="10G"
    
    for fs in ext4 xfs btrfs; do
        echo "Benchmarking $fs..."
        
        # Create test file system
        mkfs.$fs /dev/sdb1
        mount /dev/sdb1 "$test_dir"
        
        # Run comprehensive tests
        sysbench fileio \
            --file-total-size="$test_size" \
            --file-test-mode=rndrw \
            --time=300 \
            --max-requests=0 \
            prepare
        
        sysbench fileio \
            --file-total-size="$test_size" \
            --file-test-mode=rndrw \
            --time=300 \
            --max-requests=0 \
            run
        
        sysbench fileio cleanup
        umount "$test_dir"
    done
}
```

### 2. Performance Optimization
```bash
# ext4 optimizations
optimize_ext4() {
    local device="$1"
    
    # Disable access time updates
    tune2fs -o journal_data_writeback "$device"
    
    # Increase journal size for write-heavy workloads
    tune2fs -J size=400 "$device"
    
    # Enable directory indexing
    tune2fs -O dir_index "$device"
    
    # Set reserved blocks percentage
    tune2fs -m 1 "$device"
    
    # Mount options for performance
    echo "UUID=$(blkid -s UUID -o value $device) /data ext4 noatime,nodiratime,journal_async_commit,data=writeback,barrier=0,nobh,errors=remount-ro 0 2"
}

# XFS optimizations
optimize_xfs() {
    local mount_point="$1"
    
    # Set allocation groups for parallel I/O
    mkfs.xfs -d agcount=16 /dev/sdb1
    
    # Mount options for databases
    mount -o noatime,nodiratime,nobarrier,inode64,allocsize=128m,largeio,swalloc /dev/sdb1 "$mount_point"
    
    # Optimize for specific workload
    # For streaming writes
    mount -o allocsize=1g
    
    # For small files
    mount -o allocsize=4k
    
    # Defragmentation for improved performance
    xfs_fsr -v "$mount_point"
}

# ZFS tuning
tune_zfs() {
    local pool="$1"
    
    # ARC (Adaptive Replacement Cache) tuning
    echo "options zfs zfs_arc_max=8589934592" > /etc/modprobe.d/zfs.conf  # 8GB
    echo "options zfs zfs_arc_min=4294967296" >> /etc/modprobe.d/zfs.conf  # 4GB
    
    # Prefetch tuning
    echo "options zfs zfs_prefetch_disable=0" >> /etc/modprobe.d/zfs.conf
    
    # Transaction group timeout
    echo "options zfs zfs_txg_timeout=5" >> /etc/modprobe.d/zfs.conf
    
    # Pool-specific optimizations
    zfs set atime=off "$pool"
    zfs set compression=lz4 "$pool"
    zfs set xattr=sa "$pool"
    zfs set recordsize=128k "$pool"  # For databases
    
    # Enable SSD optimizations if applicable
    zpool set autotrim=on "$pool"
}

# Btrfs optimization
optimize_btrfs() {
    local mount_point="$1"
    
    # Mount options
    mount -o noatime,nodiratime,compress=zstd:3,space_cache=v2,commit=120,ssd,discard=async "$device" "$mount_point"
    
    # Enable automatic defragmentation for specific directories
    btrfs property set "$mount_point/database" compression zstd:1
    
    # Balance for optimal performance
    btrfs balance start -dusage=50 -musage=50 "$mount_point"
    
    # Disable copy-on-write for databases
    chattr +C "$mount_point/database"
}
```

### 3. Monitoring and Maintenance
```bash
# Comprehensive file system monitoring
monitor_filesystem_health() {
    # Create monitoring dashboard
    cat > /usr/local/bin/fs-health-check.sh << 'EOF'
#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== File System Health Check ==="
echo "Time: $(date)"
echo

# Check disk usage
echo "Disk Usage:"
df -h | awk 'NR==1 || $5+0 > 80' | while read line; do
    if [[ $(echo "$line" | awk '{print $5+0}') -gt 90 ]]; then
        echo -e "${RED}$line${NC}"
    elif [[ $(echo "$line" | awk '{print $5+0}') -gt 80 ]]; then
        echo -e "${YELLOW}$line${NC}"
    else
        echo "$line"
    fi
done

echo -e "\nInode Usage:"
df -i | awk 'NR==1 || $5+0 > 80'

# Check for errors in system log
echo -e "\nRecent File System Errors:"
journalctl -p err -t kernel --since "1 day ago" | grep -E "EXT4|XFS|BTRFS|ZFS" | tail -10

# Check SMART status
echo -e "\nSMART Status:"
for disk in $(lsblk -d -n -o NAME | grep -E "sd|nvme"); do
    if smartctl -H /dev/$disk &>/dev/null; then
        status=$(smartctl -H /dev/$disk | grep "SMART overall-health")
        if echo "$status" | grep -q "PASSED"; then
            echo -e "${GREEN}/dev/$disk: PASSED${NC}"
        else
            echo -e "${RED}/dev/$disk: FAILED${NC}"
        fi
    fi
done

# Check mount options
echo -e "\nMount Options:"
mount | grep -E "ext4|xfs|btrfs|zfs" | awk '{print $1, $3, $5, $6}'

# File system specific checks
echo -e "\nFile System Specific Checks:"

# ext4 checks
for fs in $(mount -t ext4 | awk '{print $1}'); do
    echo "ext4: $fs"
    tune2fs -l "$fs" 2>/dev/null | grep -E "Mount count|Maximum mount count|Last checked"
done

# XFS checks
for fs in $(mount -t xfs | awk '{print $3}'); do
    echo "XFS: $fs"
    xfs_info "$fs" | grep -E "data|log"
done

# ZFS checks
if command -v zpool &>/dev/null; then
    echo "ZFS Pools:"
    zpool status | grep -E "pool:|state:|errors:"
fi

# Btrfs checks
for fs in $(mount -t btrfs | awk '{print $3}'); do
    echo "Btrfs: $fs"
    btrfs device stats "$fs"
done
EOF
    
    chmod +x /usr/local/bin/fs-health-check.sh
}

# Automated maintenance
setup_auto_maintenance() {
    # Create maintenance script
    cat > /etc/cron.weekly/fs-maintenance << 'EOF'
#!/bin/bash

LOG="/var/log/fs-maintenance.log"

log() {
    echo "[$(date)] $*" >> "$LOG"
}

# ext4 maintenance
for fs in $(mount -t ext4 | awk '{print $1}'); do
    log "Checking ext4 filesystem: $fs"
    # Run e2fsck in check-only mode
    e2fsck -n "$fs" >> "$LOG" 2>&1
done

# XFS maintenance
for fs in $(mount -t xfs | awk '{print $3}'); do
    log "Checking XFS filesystem: $fs"
    xfs_repair -n "$fs" >> "$LOG" 2>&1
done

# ZFS maintenance
if command -v zpool &>/dev/null; then
    for pool in $(zpool list -H -o name); do
        log "Scrubbing ZFS pool: $pool"
        zpool scrub "$pool"
    done
fi

# Btrfs maintenance
for fs in $(mount -t btrfs | awk '{print $3}'); do
    log "Scrubbing Btrfs filesystem: $fs"
    btrfs scrub start -B "$fs" >> "$LOG" 2>&1
done

# Trim SSDs
log "Running fstrim on all mounted filesystems"
fstrim -av >> "$LOG" 2>&1
EOF
    
    chmod +x /etc/cron.weekly/fs-maintenance
}
```

### 4. Disaster Recovery
```bash
# File system backup strategies
implement_backup_strategy() {
    # ext4 backup with dump
    backup_ext4() {
        local source="$1"
        local destination="$2"
        
        dump -0uan -f "$destination" "$source"
    }
    
    # XFS backup with xfsdump
    backup_xfs() {
        local source="$1"
        local destination="$2"
        
        xfsdump -f "$destination" -L "Full Backup" -M "Backup Media" "$source"
    }
    
    # ZFS backup with send/receive
    backup_zfs() {
        local dataset="$1"
        local destination="$2"
        
        # Create snapshot
        zfs snapshot "$dataset@backup-$(date +%Y%m%d)"
        
        # Send snapshot
        zfs send -R "$dataset@backup-$(date +%Y%m%d)" | \
            gzip > "$destination/zfs-backup-$(date +%Y%m%d).gz"
    }
    
    # Btrfs backup with send/receive
    backup_btrfs() {
        local subvolume="$1"
        local destination="$2"
        
        # Create read-only snapshot
        btrfs subvolume snapshot -r "$subvolume" "$subvolume-backup"
        
        # Send snapshot
        btrfs send "$subvolume-backup" | \
            gzip > "$destination/btrfs-backup-$(date +%Y%m%d).gz"
    }
}

# Recovery procedures
recovery_procedures() {
    # ext4 recovery
    recover_ext4() {
        local device="$1"
        
        # Attempt automatic repair
        e2fsck -p "$device"
        
        # If failed, try manual repair
        if [[ $? -ne 0 ]]; then
            e2fsck -fy "$device"
        fi
        
        # Recover deleted files
        extundelete "$device" --restore-all
    }
    
    # XFS recovery
    recover_xfs() {
        local device="$1"
        
        # Repair filesystem
        xfs_repair "$device"
        
        # Force repair if needed
        xfs_repair -L "$device"  # WARNING: This zeros the log
    }
    
    # ZFS recovery
    recover_zfs() {
        local pool="$1"
        
        # Import pool with recovery mode
        zpool import -F "$pool"
        
        # Rollback to last good snapshot
        zfs rollback "$pool/dataset@last-good"
        
        # Scrub pool
        zpool scrub "$pool"
    }
}
```

## Common Commands and Operations

### File System Management
```bash
# Create file systems
mkfs.ext4 -L mylabel /dev/sdb1
mkfs.xfs -L mylabel /dev/sdb1
mkfs.btrfs -L mylabel /dev/sdb1

# Check file systems
e2fsck -f /dev/sdb1          # ext4
xfs_repair -n /dev/sdb1      # XFS (check only)
btrfs check /dev/sdb1        # Btrfs

# Mount with options
mount -o noatime,nodiratime /dev/sdb1 /mnt
mount -o compress=zstd:3 /dev/sdb1 /mnt  # Btrfs
mount -o discard,ssd /dev/sdb1 /mnt      # SSD optimizations

# File system information
dumpe2fs -h /dev/sdb1        # ext4
xfs_info /mnt               # XFS
btrfs filesystem show /mnt   # Btrfs
zfs list -t all             # ZFS
```

### Performance Analysis
```bash
# I/O statistics
iostat -x 1
iotop -o
dstat -D sda,sdb --disk-util

# File system usage
df -h                       # Human-readable disk usage
df -i                       # Inode usage
du -sh /*                   # Directory sizes
ncdu /                      # Interactive disk usage

# Cache statistics
free -h
vmstat 1
cat /proc/meminfo | grep -E "Cached|Buffers"

# Block device information
lsblk -f                    # File system info
blkid                       # UUID and labels
blockdev --getbsz /dev/sda  # Block size
```

### Advanced Operations
```bash
# Resize file systems
resize2fs /dev/sdb1                    # ext4
xfs_growfs /mnt                        # XFS (online)
btrfs filesystem resize +10G /mnt      # Btrfs

# Change file system parameters
tune2fs -L newlabel /dev/sdb1          # ext4 label
xfs_admin -L newlabel /dev/sdb1        # XFS label
tune2fs -U random /dev/sdb1            # New UUID

# Defragmentation
e4defrag -v /mnt                       # ext4
xfs_fsr -v /mnt                        # XFS
btrfs filesystem defragment -r /mnt    # Btrfs

# File system conversion
btrfs-convert /dev/sdb1                # ext4 to Btrfs
fstransform /dev/sdb1 ext4 xfs        # Generic conversion
```

### ZFS Operations
```bash
# Pool operations
zpool create mypool mirror sdb sdc
zpool status
zpool scrub mypool
zpool history mypool

# Dataset operations
zfs create mypool/dataset
zfs set compression=lz4 mypool/dataset
zfs set quota=100G mypool/dataset
zfs list -t all

# Snapshots and clones
zfs snapshot mypool/dataset@snapshot1
zfs rollback mypool/dataset@snapshot1
zfs clone mypool/dataset@snapshot1 mypool/clone
zfs send mypool/dataset@snapshot1 | ssh remote zfs receive tank/backup

# Performance tuning
zfs set recordsize=128k mypool/database
zfs set atime=off mypool
zfs set primarycache=metadata mypool/logs
```

### Btrfs Operations
```bash
# Subvolume management
btrfs subvolume create /mnt/subvol
btrfs subvolume list /mnt
btrfs subvolume delete /mnt/subvol
btrfs subvolume set-default 256 /mnt

# Snapshots
btrfs subvolume snapshot /mnt/subvol /mnt/snap1
btrfs subvolume snapshot -r /mnt/subvol /mnt/snap-ro
btrfs send /mnt/snap-ro | btrfs receive /backup/

# RAID and device management
btrfs device add /dev/sdd /mnt
btrfs balance start -dconvert=raid1 /mnt
btrfs device remove /dev/sdc /mnt
btrfs filesystem resize -10G /mnt

# Maintenance
btrfs scrub start /mnt
btrfs balance start -dusage=50 /mnt
btrfs check --repair /dev/sdb1
```

## Interview Tips

### Key Topics to Master
1. **File System Internals**: Understand inodes, blocks, journals
2. **Performance Characteristics**: When to use which file system
3. **RAID and Redundancy**: Software RAID, ZFS RAID-Z, Btrfs RAID
4. **Troubleshooting**: Common issues and recovery procedures
5. **Optimization**: Tuning for specific workloads
6. **Modern Features**: Snapshots, compression, deduplication

### Common Interview Questions
1. "Compare ext4, XFS, and ZFS"
   - ext4: General purpose, mature, good for small files
   - XFS: High performance, large files, parallel I/O
   - ZFS: Advanced features, data integrity, snapshots

2. "How do you recover from file system corruption?"
   - Run fsck/repair tools
   - Mount read-only first
   - Backup before repair attempts
   - Use recovery tools like extundelete

3. "Explain Copy-on-Write (CoW) file systems"
   - Never overwrites data in place
   - Creates new blocks for modifications
   - Enables snapshots and data integrity
   - Examples: ZFS, Btrfs

4. "How do you optimize file system performance?"
   - Choose appropriate file system
   - Tune mount options
   - Align to storage geometry
   - Regular maintenance

### Practical Scenarios
Be prepared to:
- Design storage architecture for specific workloads
- Troubleshoot performance issues
- Plan capacity and growth
- Implement backup strategies
- Handle corruption and recovery

## Essential Resources

### Books
1. **"Linux Filesystems"** by William Von Hagen
   - Comprehensive file system coverage
   - Implementation details

2. **"ZFS: The Last Word in Filesystems"** by various authors
   - Deep dive into ZFS
   - Best practices

3. **"Practical File System Design"** by Dominic Giampaolo
   - File system theory
   - Design principles

4. **"Storage Systems"** by Daniel A. Menasce
   - Storage architecture
   - Performance analysis

### Documentation and Guides
1. **Kernel Documentation**: File system documentation
2. **Red Hat Storage Guide**: Enterprise storage practices
3. **ZFS Documentation**: OpenZFS docs
4. **Btrfs Wiki**: Comprehensive Btrfs guide
5. **XFS Documentation**: SGI and kernel docs

### Online Resources
1. **Linux Storage Stack Diagram**: Visual representation
2. **Phoronix File System Benchmarks**: Performance comparisons
3. **StorageReview**: Industry news and benchmarks
4. **Linux Foundation Storage**: Best practices
5. **SNIA (Storage Networking Industry Association)**: Standards

### Tools and Utilities
1. **fio**: Flexible I/O tester
2. **bonnie++**: File system benchmark
3. **iozone**: File system benchmark
4. **blktrace**: Block layer tracing
5. **fsck tools**: File system check utilities
6. **testdisk**: Data recovery

### Communities and Forums
1. **linux-fsdevel**: Kernel file system development
2. **r/storage**: Storage discussions
3. **ServerFault**: Storage Q&A
4. **OpenZFS community**: ZFS discussions
5. **Btrfs mailing list**: Development and support

### Performance Testing Tools
1. **sysbench**: Database and file I/O testing
2. **ioping**: Simple I/O latency measurement
3. **hdparm**: ATA/SATA disk utilities
4. **smartmontools**: S.M.A.R.T. monitoring
5. **iostat**: I/O statistics

Remember, choosing the right file system is crucial for performance and reliability. Consider your specific use case, performance requirements, and feature needs when making decisions. Always test thoroughly before deploying to production, and maintain regular backups regardless of the file system's built-in redundancy features.