# VMware vSphere Technical Documentation

## Overview

VMware vSphere is the industry-leading enterprise virtualization platform that provides a powerful, flexible, and secure foundation for business agility. It consists of ESXi (the hypervisor) and vCenter Server (centralized management) along with a suite of features for compute, storage, and network virtualization.

## Core Components

### ESXi Hypervisor
```python
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
import ssl

class ESXiManager:
    """Manage ESXi hosts and operations"""
    
    def __init__(self, host, user, password, port=443):
        # Disable SSL certificate verification for demo
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        self.si = SmartConnect(
            host=host,
            user=user,
            pwd=password,
            port=port,
            sslContext=context
        )
        self.content = self.si.RetrieveContent()
    
    def get_host_info(self, host_name=None):
        """Get ESXi host information"""
        container = self.content.viewManager.CreateContainerView(
            self.content.rootFolder,
            [vim.HostSystem],
            True
        )
        
        for host in container.view:
            if host_name and host.name != host_name:
                continue
                
            info = {
                'name': host.name,
                'vendor': host.hardware.systemInfo.vendor,
                'model': host.hardware.systemInfo.model,
                'cpu_model': host.hardware.cpuPkg[0].description,
                'cpu_cores': host.hardware.cpuInfo.numCpuCores,
                'cpu_threads': host.hardware.cpuInfo.numCpuThreads,
                'cpu_mhz': host.hardware.cpuInfo.hz / 1000000,
                'memory_gb': host.hardware.memorySize / (1024**3),
                'version': host.config.product.version,
                'build': host.config.product.build,
                'connection_state': host.runtime.connectionState,
                'power_state': host.runtime.powerState,
                'maintenance_mode': host.runtime.inMaintenanceMode
            }
            
            return info
        
        container.Destroy()
        return None
    
    def configure_host_network(self, host, vswitch_name, portgroup_name, vlan_id=0):
        """Configure host networking"""
        host_network = host.configManager.networkSystem
        
        # Create vSwitch
        vswitch_spec = vim.host.VirtualSwitch.Specification()
        vswitch_spec.numPorts = 128
        vswitch_spec.mtu = 1500
        
        host_network.AddVirtualSwitch(
            vswitchName=vswitch_name,
            spec=vswitch_spec
        )
        
        # Create port group
        portgroup_spec = vim.host.PortGroup.Specification()
        portgroup_spec.name = portgroup_name
        portgroup_spec.vlanId = vlan_id
        portgroup_spec.vswitchName = vswitch_name
        portgroup_spec.policy = vim.host.NetworkPolicy()
        
        host_network.AddPortGroup(spec=portgroup_spec)
        
        return True
    
    def configure_ntp(self, host, ntp_servers):
        """Configure NTP on ESXi host"""
        date_time_system = host.configManager.dateTimeSystem
        
        # Configure NTP servers
        ntp_config = vim.host.NtpConfig()
        ntp_config.server = ntp_servers
        
        date_time_spec = vim.host.DateTimeConfig()
        date_time_spec.ntpConfig = ntp_config
        
        date_time_system.UpdateDateTimeConfig(config=date_time_spec)
        
        # Start NTP service
        service_system = host.configManager.serviceSystem
        service_system.StartService(id="ntpd")
        
        return True
```

### vCenter Server Management
```python
class vCenterManager:
    """Manage vCenter Server operations"""
    
    def __init__(self, vcenter_host, user, password):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        self.si = SmartConnect(
            host=vcenter_host,
            user=user,
            pwd=password,
            sslContext=context
        )
        self.content = self.si.RetrieveContent()
    
    def create_datacenter(self, name, folder=None):
        """Create a new datacenter"""
        if folder is None:
            folder = self.content.rootFolder
        
        return folder.CreateDatacenter(name=name)
    
    def create_cluster(self, datacenter, cluster_name, drs_enabled=True, ha_enabled=True):
        """Create and configure a cluster"""
        cluster_spec = vim.cluster.ConfigSpecEx()
        
        # DRS Configuration
        if drs_enabled:
            drs_config = vim.cluster.DrsConfigInfo()
            drs_config.enabled = True
            drs_config.vmotionRate = 3  # Normal aggressiveness
            drs_config.defaultVmBehavior = vim.cluster.DrsConfigInfo.DrsBehavior.fullyAutomated
            cluster_spec.drsConfig = drs_config
        
        # HA Configuration
        if ha_enabled:
            ha_config = vim.cluster.DasConfigInfo()
            ha_config.enabled = True
            ha_config.hostMonitoring = vim.cluster.DasConfigInfo.ServiceState.enabled
            ha_config.failoverLevel = 1
            ha_config.admissionControlEnabled = True
            ha_config.vmMonitoring = vim.cluster.DasConfigInfo.VmMonitoringState.vmAndAppMonitoring
            cluster_spec.dasConfig = ha_config
        
        # EVC Mode (Enhanced vMotion Compatibility)
        evc_config = vim.EVCMode()
        evc_config.guaranteedCPUFeatures = []
        evc_config.key = "intel-sandybridge"
        cluster_spec.dpmConfig = vim.cluster.DpmConfigInfo()
        
        host_folder = datacenter.hostFolder
        return host_folder.CreateClusterEx(name=cluster_name, spec=cluster_spec)
    
    def add_host_to_cluster(self, cluster, host_name, username, password):
        """Add ESXi host to cluster"""
        host_connect_spec = vim.host.ConnectSpec()
        host_connect_spec.force = False
        host_connect_spec.hostName = host_name
        host_connect_spec.userName = username
        host_connect_spec.password = password
        host_connect_spec.vmFolder = cluster.parent.parent.vmFolder
        host_connect_spec.sslThumbprint = self.get_ssl_thumbprint(host_name)
        
        task = cluster.AddHost_Task(
            spec=host_connect_spec,
            asConnected=True,
            resourcePool=cluster.resourcePool
        )
        
        return self.wait_for_task(task)
```

### Virtual Machine Management
```python
class VMManager:
    """Manage virtual machine lifecycle"""
    
    def __init__(self, service_instance):
        self.si = service_instance
        self.content = self.si.RetrieveContent()
    
    def create_vm(self, vm_name, datacenter, datastore, network, 
                  cpu=2, memory_gb=4, disk_gb=40, guest_os='centos8_64Guest'):
        """Create a new virtual machine"""
        
        # Get resources
        dc = self.get_obj([vim.Datacenter], datacenter)
        ds = self.get_obj([vim.Datastore], datastore)
        cluster = self.get_obj([vim.ClusterComputeResource], "Cluster")
        network_obj = self.get_obj([vim.Network], network)
        
        # VM configuration
        vm_config = vim.vm.ConfigSpec()
        vm_config.name = vm_name
        vm_config.memoryMB = memory_gb * 1024
        vm_config.numCPUs = cpu
        vm_config.guestId = guest_os
        vm_config.version = 'vmx-15'  # vSphere 6.7+
        
        # CPU configuration
        vm_config.cpuHotAddEnabled = True
        vm_config.memoryHotAddEnabled = True
        
        # Files location
        vm_files = vim.vm.FileInfo()
        vm_files.vmPathName = f"[{datastore}]"
        vm_config.files = vm_files
        
        # Disk controller
        scsi_controller = vim.vm.device.VirtualDeviceSpec()
        scsi_controller.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        scsi_controller.device = vim.vm.device.ParaVirtualSCSIController()
        scsi_controller.device.deviceInfo = vim.Description()
        scsi_controller.device.slotInfo = vim.vm.device.VirtualDevice.PciBusSlotInfo()
        scsi_controller.device.controllerKey = 100
        scsi_controller.device.unitNumber = 3
        scsi_controller.device.busNumber = 0
        scsi_controller.device.hotAddRemove = True
        scsi_controller.device.sharedBus = 'noSharing'
        scsi_controller.device.scsiCtlrUnitNumber = 7
        
        # Disk
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.fileOperation = vim.vm.device.VirtualDeviceSpec.FileOperation.create
        disk_spec.device = vim.vm.device.VirtualDisk()
        disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        disk_spec.device.backing.diskMode = 'persistent'
        disk_spec.device.backing.thinProvisioned = True
        disk_spec.device.backing.datastore = ds
        disk_spec.device.unitNumber = 0
        disk_spec.device.capacityInKB = disk_gb * 1024 * 1024
        disk_spec.device.controllerKey = scsi_controller.device.key
        
        # Network adapter
        nic_spec = vim.vm.device.VirtualDeviceSpec()
        nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        nic_spec.device = vim.vm.device.VirtualVmxnet3()
        nic_spec.device.deviceInfo = vim.Description()
        nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
        nic_spec.device.backing.network = network_obj
        nic_spec.device.backing.deviceName = network
        nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        nic_spec.device.connectable.startConnected = True
        nic_spec.device.connectable.allowGuestControl = True
        
        vm_config.deviceChange = [scsi_controller, disk_spec, nic_spec]
        
        # Create VM
        vm_folder = dc.vmFolder
        resource_pool = cluster.resourcePool
        
        task = vm_folder.CreateVM_Task(
            config=vm_config,
            pool=resource_pool
        )
        
        return self.wait_for_task(task)
    
    def configure_vm_advanced(self, vm, settings):
        """Configure advanced VM settings"""
        spec = vim.vm.ConfigSpec()
        
        # CPU and Memory reservations
        cpu_allocation = vim.ResourceAllocationInfo()
        cpu_allocation.reservation = settings.get('cpu_reservation', 0)
        cpu_allocation.limit = settings.get('cpu_limit', -1)
        cpu_allocation.shares = vim.SharesInfo(
            level=settings.get('cpu_shares_level', 'normal'),
            shares=settings.get('cpu_shares', 1000)
        )
        spec.cpuAllocation = cpu_allocation
        
        memory_allocation = vim.ResourceAllocationInfo()
        memory_allocation.reservation = settings.get('memory_reservation', 0)
        memory_allocation.limit = settings.get('memory_limit', -1)
        memory_allocation.shares = vim.SharesInfo(
            level=settings.get('memory_shares_level', 'normal'),
            shares=settings.get('memory_shares', 10240)
        )
        spec.memoryAllocation = memory_allocation
        
        # Advanced settings
        extra_config = []
        
        # Security hardening
        security_settings = {
            'isolation.tools.copy.disable': 'TRUE',
            'isolation.tools.paste.disable': 'TRUE',
            'isolation.tools.diskShrink.disable': 'TRUE',
            'isolation.tools.diskWiper.disable': 'TRUE',
            'RemoteDisplay.maxConnections': '1',
            'tools.guestlib.enableHostInfo': 'FALSE'
        }
        
        for key, value in security_settings.items():
            option = vim.option.OptionValue()
            option.key = key
            option.value = value
            extra_config.append(option)
        
        # Performance settings
        if settings.get('enable_cpu_performance'):
            perf_option = vim.option.OptionValue()
            perf_option.key = 'sched.cpu.latencySensitivity'
            perf_option.value = 'high'
            extra_config.append(perf_option)
        
        spec.extraConfig = extra_config
        
        # VM Tools settings
        tools_spec = vim.vm.ToolsConfigInfo()
        tools_spec.syncTimeWithHost = True
        tools_spec.toolsUpgradePolicy = 'upgradeAtPowerCycle'
        spec.tools = tools_spec
        
        task = vm.ReconfigVM_Task(spec=spec)
        return self.wait_for_task(task)
```

### Storage Management

#### vSAN Configuration
```python
class vSANManager:
    """Manage VMware vSAN operations"""
    
    def __init__(self, service_instance):
        self.si = service_instance
        self.content = self.si.RetrieveContent()
        self.vsan_config = self.content.vsanConfigSystem
    
    def enable_vsan_on_cluster(self, cluster, disk_claim_mode='automatic'):
        """Enable vSAN on a cluster"""
        vsan_config_spec = vim.vsan.cluster.ConfigInfo()
        vsan_config_spec.enabled = True
        vsan_config_spec.defaultConfig = vim.vsan.cluster.ConfigInfo.HostDefaultInfo()
        
        # Disk claim configuration
        if disk_claim_mode == 'automatic':
            vsan_config_spec.defaultConfig.autoClaimStorage = True
        else:
            vsan_config_spec.defaultConfig.autoClaimStorage = False
        
        # Deduplication and compression
        vsan_config_spec.dataEfficiencyConfig = vim.vsan.DataEfficiencyConfig()
        vsan_config_spec.dataEfficiencyConfig.compressionEnabled = True
        vsan_config_spec.dataEfficiencyConfig.dedupEnabled = True
        
        # Encryption
        vsan_config_spec.dataEncryptionConfig = vim.vsan.DataEncryptionConfig()
        vsan_config_spec.dataEncryptionConfig.encryptionEnabled = False
        
        task = self.vsan_config.ReconfigureEx(
            cluster=cluster,
            vsanReconfigSpec=vsan_config_spec
        )
        
        return self.wait_for_task(task)
    
    def create_vsan_disk_group(self, host, cache_disk, capacity_disks):
        """Create vSAN disk group on host"""
        disk_mapping_spec = vim.vsan.host.DiskMappingCreationSpec()
        
        # Cache tier
        disk_mapping_spec.cacheDisks = [cache_disk]
        
        # Capacity tier
        disk_mapping_spec.capacityDisks = capacity_disks
        
        # Storage policy
        disk_mapping_spec.creationType = 'allFlash'
        
        vsan_system = host.configManager.vsanSystem
        task = vsan_system.AddDisks_Task(spec=disk_mapping_spec)
        
        return self.wait_for_task(task)
```

#### VMFS Datastore Management
```python
def create_vmfs_datastore(self, host, device_path, datastore_name):
    """Create VMFS datastore on host"""
    datastore_system = host.configManager.datastoreSystem
    
    # Query available disks
    available_disks = datastore_system.QueryAvailableDisksForVmfs()
    
    target_disk = None
    for disk in available_disks:
        if disk.devicePath == device_path:
            target_disk = disk
            break
    
    if not target_disk:
        raise Exception(f"Disk {device_path} not found")
    
    # Create VMFS datastore
    vmfs_spec = datastore_system.QueryVmfsDatastoreCreateOptions(
        disk.devicePath
    )[0].spec
    
    vmfs_spec.vmfs.volumeName = datastore_name
    vmfs_spec.vmfs.blockSize = 1048576  # 1MB block size
    
    datastore = datastore_system.CreateVmfsDatastore(spec=vmfs_spec)
    
    return datastore
```

### vSphere Distributed Switch (vDS)
```python
class vDSManager:
    """Manage vSphere Distributed Switches"""
    
    def __init__(self, service_instance):
        self.si = service_instance
        self.content = self.si.RetrieveContent()
    
    def create_distributed_switch(self, datacenter, name, version='7.0.0', uplinks=2):
        """Create a new distributed switch"""
        
        # Create DVS config spec
        dvs_create_spec = vim.DistributedVirtualSwitch.CreateSpec()
        dvs_create_spec.configSpec = vim.dvs.VmwareDistributedVirtualSwitch.ConfigSpec()
        dvs_create_spec.configSpec.name = name
        dvs_create_spec.configSpec.maxMtu = 9000  # Enable jumbo frames
        
        # Product info
        product_spec = vim.dvs.ProductSpec()
        product_spec.version = version
        dvs_create_spec.productSpec = product_spec
        
        # Uplink configuration
        uplink_port_policy = vim.dvs.VmwareDistributedVirtualSwitch.UplinkPortPolicy()
        uplink_port_policy.uplinkPortName = [f"Uplink {i+1}" for i in range(uplinks)]
        dvs_create_spec.configSpec.uplinkPortPolicy = uplink_port_policy
        
        # Create the switch
        network_folder = datacenter.networkFolder
        task = network_folder.CreateDVS_Task(spec=dvs_create_spec)
        
        return self.wait_for_task(task)
    
    def create_dvportgroup(self, dvs, name, vlan_id, num_ports=128):
        """Create distributed port group"""
        
        pg_spec = vim.dvs.DistributedVirtualPortgroup.ConfigSpec()
        pg_spec.name = name
        pg_spec.type = vim.dvs.DistributedVirtualPortgroup.PortgroupType.earlyBinding
        pg_spec.numPorts = num_ports
        
        # VLAN configuration
        vlan_spec = vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec()
        vlan_spec.vlanId = vlan_id
        pg_spec.defaultPortConfig = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()
        pg_spec.defaultPortConfig.vlan = vlan_spec
        
        # Security policy
        security_policy = vim.dvs.VmwareDistributedVirtualSwitch.SecurityPolicy()
        security_policy.allowPromiscuous = vim.BoolPolicy(value=False)
        security_policy.forgedTransmits = vim.BoolPolicy(value=False)
        security_policy.macChanges = vim.BoolPolicy(value=False)
        pg_spec.defaultPortConfig.securityPolicy = security_policy
        
        # Traffic shaping
        traffic_shaping = vim.dvs.DistributedVirtualPort.TrafficShapingPolicy()
        traffic_shaping.enabled = vim.BoolPolicy(value=True)
        traffic_shaping.averageBandwidth = vim.LongPolicy(value=100000000)  # 100 Mbps
        traffic_shaping.peakBandwidth = vim.LongPolicy(value=1000000000)    # 1 Gbps
        traffic_shaping.burstSize = vim.LongPolicy(value=104857600)         # 100 MB
        pg_spec.defaultPortConfig.inShapingPolicy = traffic_shaping
        
        task = dvs.CreateDVPortgroup_Task(spec=pg_spec)
        return self.wait_for_task(task)
    
    def configure_network_io_control(self, dvs):
        """Configure Network I/O Control (NIOC)"""
        
        nioc_spec = vim.dvs.VmwareDistributedVirtualSwitch.ConfigSpec()
        nioc_spec.configVersion = dvs.config.configVersion
        
        # Enable NIOC
        nioc_spec.networkResourceManagementEnabled = True
        
        # Configure resource pools
        resource_pools = []
        
        # vMotion traffic
        vmotion_pool = vim.dvs.NetworkResourcePool.ConfigSpec()
        vmotion_pool.key = "vmotion"
        vmotion_pool.name = "vMotion"
        vmotion_pool.description = "vMotion traffic"
        vmotion_pool.allocationInfo = vim.dvs.NetworkResourcePool.AllocationInfo()
        vmotion_pool.allocationInfo.shares = vim.SharesInfo(level="high", shares=100)
        vmotion_pool.allocationInfo.limit = -1  # Unlimited
        vmotion_pool.allocationInfo.reservation = 1000  # 1 Gbps
        resource_pools.append(vmotion_pool)
        
        # Management traffic
        mgmt_pool = vim.dvs.NetworkResourcePool.ConfigSpec()
        mgmt_pool.key = "management"
        mgmt_pool.name = "Management"
        mgmt_pool.description = "Management traffic"
        mgmt_pool.allocationInfo = vim.dvs.NetworkResourcePool.AllocationInfo()
        mgmt_pool.allocationInfo.shares = vim.SharesInfo(level="normal", shares=50)
        mgmt_pool.allocationInfo.reservation = 100  # 100 Mbps
        resource_pools.append(mgmt_pool)
        
        # VM traffic
        vm_pool = vim.dvs.NetworkResourcePool.ConfigSpec()
        vm_pool.key = "virtualMachine"
        vm_pool.name = "Virtual Machine"
        vm_pool.description = "VM traffic"
        vm_pool.allocationInfo = vim.dvs.NetworkResourcePool.AllocationInfo()
        vm_pool.allocationInfo.shares = vim.SharesInfo(level="high", shares=100)
        resource_pools.append(vm_pool)
        
        nioc_spec.infrastructureTrafficResourceConfig = resource_pools
        
        task = dvs.ReconfigureDvs_Task(spec=nioc_spec)
        return self.wait_for_task(task)
```

### vMotion and DRS
```python
class vMotionManager:
    """Manage vMotion and DRS operations"""
    
    def perform_vmotion(self, vm, target_host, priority='defaultPriority'):
        """Perform vMotion migration"""
        
        # Create migration spec
        migrate_spec = vim.vm.MigrateSpec()
        migrate_spec.host = target_host
        migrate_spec.priority = getattr(
            vim.VirtualMachine.MovePriority, 
            priority
        )
        
        task = vm.MigrateVM_Task(
            spec=migrate_spec
        )
        
        return self.wait_for_task(task)
    
    def configure_drs_rules(self, cluster):
        """Configure DRS affinity rules"""
        
        cluster_spec = vim.cluster.ConfigSpecEx()
        
        # VM-VM affinity rule (keep together)
        affinity_rule = vim.cluster.AffinityRuleSpec()
        affinity_rule.name = "WebApp-Affinity"
        affinity_rule.enabled = True
        affinity_rule.userCreated = True
        affinity_rule.vm = self.get_vms_by_tag("webapp")
        
        # VM-VM anti-affinity rule (keep apart)
        anti_affinity_rule = vim.cluster.AntiAffinityRuleSpec()
        anti_affinity_rule.name = "Database-AntiAffinity"
        anti_affinity_rule.enabled = True
        anti_affinity_rule.userCreated = True
        anti_affinity_rule.vm = self.get_vms_by_tag("database")
        
        # VM-Host affinity rule
        vm_host_rule = vim.cluster.VmHostRuleInfo()
        vm_host_rule.name = "Production-HostAffinity"
        vm_host_rule.enabled = True
        vm_host_rule.userCreated = True
        vm_host_rule.affineHostGroupName = "ProductionHosts"
        vm_host_rule.vmGroupName = "ProductionVMs"
        
        cluster_spec.rulesSpec = [
            vim.cluster.RuleSpec(
                info=affinity_rule,
                operation='add'
            ),
            vim.cluster.RuleSpec(
                info=anti_affinity_rule,
                operation='add'
            ),
            vim.cluster.RuleSpec(
                info=vm_host_rule,
                operation='add'
            )
        ]
        
        task = cluster.ReconfigureComputeResource_Task(
            spec=cluster_spec,
            modify=True
        )
        
        return self.wait_for_task(task)
```

### Backup and Recovery

#### vSphere Data Protection
```python
class BackupManager:
    """Manage VM backups and recovery"""
    
    def create_snapshot(self, vm, snapshot_name, description, memory=True, quiesce=True):
        """Create VM snapshot"""
        
        task = vm.CreateSnapshot_Task(
            name=snapshot_name,
            description=description,
            memory=memory,
            quiesce=quiesce  # File system quiescing for consistency
        )
        
        return self.wait_for_task(task)
    
    def restore_from_snapshot(self, vm, snapshot_name):
        """Restore VM from snapshot"""
        
        snapshot = self.get_snapshot_by_name(vm, snapshot_name)
        if not snapshot:
            raise Exception(f"Snapshot {snapshot_name} not found")
        
        task = snapshot.snapshot.RevertToSnapshot_Task()
        return self.wait_for_task(task)
    
    def setup_replication(self, vm, target_datastore, rpo_minutes=15):
        """Configure vSphere Replication"""
        
        replication_spec = vim.hbr.ReplicationSpec()
        replication_spec.replicationVmSpec = vim.hbr.ReplicationVmSpec()
        replication_spec.replicationVmSpec.vm = vm
        replication_spec.replicationVmSpec.targetDatastore = target_datastore
        replication_spec.replicationVmSpec.rpo = rpo_minutes * 60  # Convert to seconds
        replication_spec.replicationVmSpec.quiesceGuestEnabled = True
        replication_spec.replicationVmSpec.diskSpec = []
        
        # Configure disk replication
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualDisk):
                disk_spec = vim.hbr.ReplicationVmSpec.DiskSpec()
                disk_spec.key = device.key
                disk_spec.enableReplication = True
                replication_spec.replicationVmSpec.diskSpec.append(disk_spec)
        
        # Enable replication
        hbr_manager = self.content.hbrManager
        task = hbr_manager.EnableReplication_Task(spec=replication_spec)
        
        return self.wait_for_task(task)
```

### Security and Compliance

#### vSphere Security Configuration
```python
class SecurityManager:
    """Manage vSphere security settings"""
    
    def harden_esxi_host(self, host):
        """Apply security hardening to ESXi host"""
        
        # Configure advanced security settings
        option_manager = host.configManager.advancedOption
        
        security_settings = [
            # Disable SSH when not needed
            ("UserVars.SuppressShellWarning", 1),
            # Set password complexity
            ("Security.PasswordQualityControl", "min=disabled,disabled,disabled,disabled,15"),
            # Account lockout policy
            ("Security.AccountLockFailures", 3),
            ("Security.AccountUnlockTime", 900),
            # Audit settings
            ("Config.HostAgent.log.level", "info"),
            ("Syslog.global.logDir", "/scratch/log"),
            # Network security
            ("Net.BlockGuestBPDU", 1),
            ("Net.DVFilterBindIpAddress", ""),
            # Secure boot
            ("VMkernel.Boot.execInstalledOnly", "TRUE")
        ]
        
        for key, value in security_settings:
            option = vim.option.OptionValue()
            option.key = key
            option.value = value
            option_manager.UpdateOptions(changedValue=[option])
        
        # Configure firewall rules
        firewall_system = host.configManager.firewallSystem
        
        # Enable only required services
        allowed_services = [
            "sshServer",
            "vpxHeartbeats",
            "CIMHttpServer",
            "CIMHttpsServer",
            "ntpClient"
        ]
        
        for ruleset in firewall_system.firewallInfo.ruleset:
            if ruleset.key not in allowed_services:
                firewall_system.DisableRuleset(id=ruleset.key)
        
        return True
    
    def configure_vcenter_sso(self, identity_source_type='ActiveDirectory'):
        """Configure vCenter Single Sign-On"""
        
        sso_admin = self.content.sessionManager.sessionIsActive
        
        if identity_source_type == 'ActiveDirectory':
            # Configure AD integration
            identity_source = {
                'name': 'example.com',
                'type': 'ActiveDirectory',
                'domainName': 'example.com',
                'primaryServer': 'dc01.example.com',
                'baseDN': 'dc=example,dc=com',
                'username': 'svc_vcenter@example.com',
                'password': 'secure_password'
            }
            
            # Add identity source
            # This would use vCenter SSO API
            
        return True
    
    def enable_encryption(self, vm):
        """Enable VM encryption"""
        
        encryption_spec = vim.vm.ConfigSpec()
        
        # Enable encryption
        crypto_spec = vim.encryption.CryptoSpecEncrypt()
        encryption_spec.crypto = crypto_spec
        
        # Configure key provider
        key_id = vim.encryption.CryptoKeyId()
        key_id.keyId = "example-key-id"
        key_id.providerId = vim.encryption.KeyProviderId()
        key_id.providerId.id = "example-kms-provider"
        
        crypto_spec.cryptoKeyId = key_id
        
        task = vm.ReconfigVM_Task(spec=encryption_spec)
        return self.wait_for_task(task)
```

### Monitoring and Performance

#### vRealize Operations Integration
```python
class PerformanceMonitoring:
    """Monitor vSphere performance"""
    
    def collect_performance_metrics(self, entity, metric_ids, interval=20):
        """Collect performance metrics"""
        
        perf_manager = self.content.perfManager
        
        # Query available metrics
        available_metrics = perf_manager.perfCounter
        
        # Build query spec
        query_spec = vim.PerfQuerySpec()
        query_spec.entity = entity
        query_spec.metricId = metric_ids
        query_spec.intervalId = interval
        query_spec.maxSample = 10
        
        # Query metrics
        results = perf_manager.QueryPerf(querySpec=[query_spec])
        
        metrics_data = []
        for result in results:
            for val in result.value:
                counter_info = next(
                    (c for c in available_metrics if c.key == val.id.counterId),
                    None
                )
                if counter_info:
                    metrics_data.append({
                        'metric': f"{counter_info.groupInfo.key}.{counter_info.nameInfo.key}",
                        'unit': counter_info.unitInfo.label,
                        'values': val.value,
                        'timestamps': result.sampleInfo
                    })
        
        return metrics_data
    
    def setup_alarms(self, entity, alarm_name, metric, threshold):
        """Configure performance alarms"""
        
        alarm_manager = self.content.alarmManager
        
        # Create alarm spec
        alarm_spec = vim.alarm.AlarmSpec()
        alarm_spec.name = alarm_name
        alarm_spec.description = f"Alert when {metric} exceeds {threshold}"
        alarm_spec.enabled = True
        
        # Expression
        metric_alarm = vim.alarm.MetricAlarmExpression()
        metric_alarm.operator = vim.alarm.MetricAlarmExpression.MetricOperator.isAbove
        metric_alarm.threshold = threshold
        metric_alarm.yellow = threshold * 0.8
        metric_alarm.red = threshold
        metric_alarm.metric = self.get_metric_id(metric)
        
        alarm_spec.expression = metric_alarm
        
        # Actions
        email_action = vim.alarm.SendEmailAction()
        email_action.toList = ["ops-team@example.com"]
        email_action.subject = f"{alarm_name} Alert"
        
        alarm_spec.action = vim.alarm.GroupAlarmAction()
        alarm_spec.action.action = [email_action]
        
        alarm = alarm_manager.CreateAlarm(entity=entity, spec=alarm_spec)
        return alarm
```

### Automation with PowerCLI

```powershell
# PowerCLI automation script example
Connect-VIServer -Server vcenter.example.com -User admin@vsphere.local

# Automated VM deployment
function Deploy-VMFromTemplate {
    param(
        [string]$TemplateName,
        [string]$VMName,
        [string]$Cluster,
        [string]$Datastore,
        [string]$NetworkName,
        [hashtable]$CustomSpec
    )
    
    $template = Get-Template -Name $TemplateName
    $vmHost = Get-Cluster $Cluster | Get-VMHost | Get-Random
    $ds = Get-Datastore -Name $Datastore
    
    # Create customization spec
    $spec = New-OSCustomizationSpec -Name "temp-spec" -Type NonPersistent
    Set-OSCustomizationSpec -OSCustomizationSpec $spec `
        -Domain $CustomSpec.Domain `
        -DnsServer $CustomSpec.DnsServers `
        -NamingScheme Fixed -NamingPrefix $VMName
    
    # Deploy VM
    $vm = New-VM -Template $template `
        -Name $VMName `
        -VMHost $vmHost `
        -Datastore $ds `
        -OSCustomizationSpec $spec
    
    # Configure network
    $vm | Get-NetworkAdapter | Set-NetworkAdapter -NetworkName $NetworkName -Confirm:$false
    
    # Power on
    Start-VM -VM $vm
    
    # Clean up
    Remove-OSCustomizationSpec -OSCustomizationSpec $spec -Confirm:$false
    
    return $vm
}

# Bulk operations
function Set-VMResourceAllocation {
    param(
        [string]$Tag,
        [int]$CPUReservationMHz,
        [int]$MemoryReservationGB
    )
    
    Get-Tag -Name $Tag | Get-VM | ForEach-Object {
        $spec = New-Object VMware.Vim.VirtualMachineConfigSpec
        
        # CPU allocation
        $spec.CpuAllocation = New-Object VMware.Vim.ResourceAllocationInfo
        $spec.CpuAllocation.Reservation = $CPUReservationMHz
        
        # Memory allocation
        $spec.MemoryAllocation = New-Object VMware.Vim.ResourceAllocationInfo
        $spec.MemoryAllocation.Reservation = $MemoryReservationGB * 1024
        
        $_.ExtensionData.ReconfigVM($spec)
    }
}
```

### NSX-T Integration

```python
class NSXTIntegration:
    """Integrate vSphere with NSX-T"""
    
    def configure_nsx_transport_zone(self, compute_managers, transport_zone_name):
        """Configure NSX-T transport zone for vSphere cluster"""
        
        # This would use NSX-T API
        nsx_config = {
            'transport_zone': {
                'display_name': transport_zone_name,
                'transport_type': 'OVERLAY',
                'host_switch_mode': 'ENS',
                'nested_nsx': False
            },
            'compute_collections': []
        }
        
        # Add vSphere clusters to transport zone
        for cm in compute_managers:
            nsx_config['compute_collections'].append({
                'compute_manager_id': cm['id'],
                'compute_collection_id': cm['cluster_id']
            })
        
        return nsx_config
    
    def create_logical_switch(self, name, transport_zone_id, vlan_id=None):
        """Create NSX-T logical switch"""
        
        logical_switch = {
            'display_name': name,
            'transport_zone_id': transport_zone_id,
            'replication_mode': 'MTEP',  # Multi-TEP
            'admin_state': 'UP'
        }
        
        if vlan_id:
            logical_switch['vlan'] = vlan_id
        
        # This would make actual NSX-T API call
        return logical_switch
```

## Best Practices Summary

1. **Design**: Follow VMware Validated Designs (VVD) for architecture
2. **Compute**: Right-size VMs, use resource pools, and configure DRS properly
3. **Storage**: Use appropriate storage policies, enable deduplication/compression on vSAN
4. **Networking**: Implement distributed switches, use NIOC for QoS
5. **Security**: Apply hardening guides, use VM encryption, implement micro-segmentation
6. **Availability**: Configure HA, DRS, and implement proper backup strategies
7. **Performance**: Monitor metrics, set appropriate reservations and limits
8. **Automation**: Use PowerCLI, vRO, or APIs for repetitive tasks

## Common Pitfalls to Avoid

1. Overcommitting CPU and memory without proper monitoring
2. Not configuring vMotion network with dedicated bandwidth
3. Ignoring storage performance requirements and not using storage policies
4. Poor snapshot management leading to performance issues
5. Not implementing proper network segmentation
6. Inadequate backup testing and recovery procedures
7. Not keeping vSphere components updated with latest patches