# OpenStack

<GitHubButtons />
## 📚 Learning Resources

### 📖 Essential Documentation
- [OpenStack Documentation](https://docs.openstack.org/) - Official comprehensive documentation
- [Installation Guide](https://docs.openstack.org/install-guide/) - Step-by-step deployment instructions
- [Administrator Guide](https://docs.openstack.org/admin-guide/) - Operations and management guide
- [API Reference](https://docs.openstack.org/api-guide/quick-start/) - Complete API documentation

### 📝 Specialized Guides
- [OpenStack Architecture](https://docs.openstack.org/arch-guide/) - Design principles and patterns
- [Security Guide](https://docs.openstack.org/security-guide/) - Hardening and security best practices
- [Operations Guide](https://docs.openstack.org/operations-guide/) - Day-to-day administration
- [High Availability Guide](https://docs.openstack.org/ha-guide/) - Building resilient cloud infrastructure

### 🎥 Video Tutorials
- [OpenStack Foundation Summit](https://www.youtube.com/user/OpenStackFoundation) - Conference presentations and demos
- [OpenStack Tutorial Series](https://www.youtube.com/playlist?list=PLOuHvpVx7kYkZGx_jQn7Ej8WA5g2RCuRH) - Getting started tutorials
- [OpenStack Deep Dive](https://www.youtube.com/watch?v=videoid) - Architecture overview (60 min)

### 🎓 Professional Courses
- [OpenStack Administration](https://training.linuxfoundation.org/training/openstack-administration-with-ansible/) - Linux Foundation certification
- [Red Hat OpenStack](https://www.redhat.com/en/services/training/cl210-red-hat-openstack-administration-i) - Paid comprehensive training
- [Mirantis OpenStack](https://www.mirantis.com/training/) - Paid professional certification

### 📚 Books
- "OpenStack Cloud Computing" by John Garbutt - [Purchase on Amazon](https://www.amazon.com/dp/1787125521)
- "Learning OpenStack Networking" by James Denton - [Purchase on Amazon](https://www.amazon.com/dp/1785287725)
- "OpenStack in Action" by V.K. Cody Bumgardner - [Purchase on Amazon](https://www.amazon.com/dp/1617292162)

### 🛠️ Interactive Tools
- [DevStack](https://docs.openstack.org/devstack/latest/) - All-in-one development environment
- [TryStack](http://trystack.org/) - Free OpenStack testing environment
- [OpenStack Horizon](https://docs.openstack.org/horizon/latest/) - Web-based dashboard

### 🚀 Ecosystem Tools
- [Kolla](https://github.com/openstack/kolla) - Container-based OpenStack deployment
- [TripleO](https://docs.openstack.org/tripleo-docs/latest/) - OpenStack on OpenStack deployment
- [OpenStack Ansible](https://docs.openstack.org/openstack-ansible/latest/) - Ansible-based deployment
- [Fuel](https://wiki.openstack.org/wiki/Fuel) - Deployment and lifecycle management

### 🌐 Community & Support
- [OpenStack Community](https://www.openstack.org/community/) - Official community resources
- [OpenStack Mailing Lists](http://lists.openstack.org/) - Development and user discussions
- [OpenStack IRC](https://docs.openstack.org/contributors/common/irc.html) - Real-time community chat

## Understanding OpenStack: Private Cloud Infrastructure Platform

OpenStack is an open-source cloud computing platform that provides Infrastructure-as-a-Service (IaaS) capabilities. It consists of interrelated components that control hardware pools of processing, storage, and networking resources throughout a data center, enabling organizations to build and manage private and public clouds using standard hardware.

### How OpenStack Works
OpenStack operates through a collection of interconnected services that work together to provide cloud infrastructure capabilities. Each service handles a specific aspect of cloud computing - compute, networking, storage, identity, and orchestration. These services communicate through well-defined APIs, creating a modular and scalable architecture.

The platform abstracts physical hardware into virtual resources that can be provisioned on-demand. Users interact with OpenStack through web interfaces, command-line tools, or APIs to create virtual machines, configure networks, and manage storage, just like public cloud services.

### The OpenStack Ecosystem
OpenStack's ecosystem includes core services like Nova (compute), Neutron (networking), Swift (object storage), and Cinder (block storage). Additional services provide orchestration (Heat), telemetry (Ceilometer), and container management (Magnum).

The ecosystem extends through deployment tools like Kolla for containerized deployments, TripleO for bare metal provisioning, and various distributions from vendors like Red Hat, SUSE, and Mirantis. This rich ecosystem enables organizations to choose deployment methods that fit their needs.

### Why OpenStack Powers Private Clouds
OpenStack has become the standard for private cloud infrastructure due to its open-source nature, vendor neutrality, and comprehensive feature set. Unlike proprietary solutions, OpenStack provides the freedom to customize and extend functionality without vendor lock-in.

The platform offers the same capabilities as public clouds while maintaining data sovereignty and control. This makes it ideal for organizations with strict compliance requirements or those needing customized cloud functionality.

### Mental Model for Success
Think of OpenStack like building your own city infrastructure. Instead of relying on external utilities (public cloud), you're creating your own power grid (compute), water system (storage), road network (networking), and city services (additional components).

Just as city infrastructure requires planning, coordination, and maintenance, OpenStack requires careful design and ongoing operations. But like owning city infrastructure, you have complete control and can customize it for your specific needs.

### Where to Start Your Journey
1. **Try DevStack locally** - Set up a development environment to explore features
2. **Learn core services** - Understand Nova, Neutron, Glance, and Keystone
3. **Deploy a test cluster** - Use packaged distributions for initial deployment
4. **Practice with Horizon** - Use the web interface for common operations
5. **Explore APIs** - Understand programmatic access patterns
6. **Plan production deployment** - Design for high availability and scalability

### Key Concepts to Master
- **Service architecture** - How OpenStack components interact
- **Identity and access** - Keystone authentication and authorization
- **Compute management** - Virtual machine lifecycle and flavors
- **Network design** - Virtual networks, security groups, and floating IPs
- **Storage options** - Block, object, and filesystem storage patterns
- **High availability** - Building resilient cloud infrastructure
- **Monitoring** - Observability and performance management
- **Scaling strategies** - Growing and managing large deployments

Start with understanding the core services and their relationships, then progress to deployment and operational concerns. Focus on the specific services most relevant to your use case rather than trying to master everything at once.

## Core Components

### Keystone (Identity Service)
```python
from keystoneauth1 import loading, session
from keystoneclient.v3 import client as keystone_client

# Authentication setup
def get_keystone_session():
    """Create authenticated Keystone session"""
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(
        auth_url='http://controller:5000/v3',
        username='admin',
        password='admin_pass',
        project_name='admin',
        project_domain_name='Default',
        user_domain_name='Default'
    )
    sess = session.Session(auth=auth)
    return sess

# Create project and users
def setup_project(project_name, description):
    """Create a new project with users and roles"""
    sess = get_keystone_session()
    keystone = keystone_client.Client(session=sess)
    
    # Create project
    project = keystone.projects.create(
        name=project_name,
        domain='default',
        description=description,
        enabled=True
    )
    
    # Create user
    user = keystone.users.create(
        name=f"{project_name}_admin",
        domain='default',
        password='secure_password',
        email=f"admin@{project_name}.local",
        enabled=True
    )
    
    # Assign role
    admin_role = keystone.roles.find(name='admin')
    keystone.roles.grant(
        role=admin_role,
        user=user,
        project=project
    )
    
    return {
        'project_id': project.id,
        'user_id': user.id
    }
```

### Nova (Compute Service)
```python
from novaclient import client as nova_client

class NovaManager:
    """Manage OpenStack compute resources"""
    
    def __init__(self, session):
        self.nova = nova_client.Client('2.1', session=session)
    
    def create_instance(self, name, flavor, image, network_id, key_name=None):
        """Launch a new instance"""
        # Get flavor and image
        flavor_obj = self.nova.flavors.find(name=flavor)
        image_obj = self.nova.glance.find_image(image)
        
        # Network configuration
        nics = [{'net-id': network_id}]
        
        # User data for cloud-init
        user_data = '''#!/bin/bash
        apt-get update
        apt-get install -y nginx
        echo "OpenStack Instance" > /var/www/html/index.html
        systemctl start nginx
        '''
        
        # Create instance
        instance = self.nova.servers.create(
            name=name,
            image=image_obj,
            flavor=flavor_obj,
            key_name=key_name,
            nics=nics,
            userdata=user_data
        )
        
        # Wait for active state
        while instance.status != 'ACTIVE':
            time.sleep(5)
            instance = self.nova.servers.get(instance.id)
            if instance.status == 'ERROR':
                raise Exception(f"Instance creation failed: {instance.fault}")
        
        return instance
    
    def create_flavor(self, name, ram, vcpus, disk, ephemeral=0):
        """Create custom flavor"""
        flavor = self.nova.flavors.create(
            name=name,
            ram=ram,
            vcpus=vcpus,
            disk=disk,
            ephemeral=ephemeral,
            swap=0,
            rxtx_factor=1.0,
            is_public=True
        )
        
        # Set extra specs for performance tuning
        flavor.set_keys({
            'hw:cpu_policy': 'dedicated',
            'hw:numa_nodes': '1',
            'hw:mem_page_size': 'large'
        })
        
        return flavor
```

### Neutron (Networking Service)
```python
from neutronclient.v2_0 import client as neutron_client

class NeutronManager:
    """Manage OpenStack networking"""
    
    def __init__(self, session):
        self.neutron = neutron_client.Client(session=session)
    
    def create_network_topology(self, project_id, external_network_id):
        """Create complete network topology for a project"""
        
        # Create internal network
        network = self.neutron.create_network({
            'network': {
                'name': 'internal-net',
                'tenant_id': project_id,
                'admin_state_up': True
            }
        })['network']
        
        # Create subnet
        subnet = self.neutron.create_subnet({
            'subnet': {
                'network_id': network['id'],
                'name': 'internal-subnet',
                'cidr': '192.168.1.0/24',
                'ip_version': 4,
                'enable_dhcp': True,
                'dns_nameservers': ['8.8.8.8', '8.8.4.4'],
                'allocation_pools': [{
                    'start': '192.168.1.10',
                    'end': '192.168.1.200'
                }]
            }
        })['subnet']
        
        # Create router
        router = self.neutron.create_router({
            'router': {
                'name': 'project-router',
                'tenant_id': project_id,
                'external_gateway_info': {
                    'network_id': external_network_id
                }
            }
        })['router']
        
        # Attach subnet to router
        self.neutron.add_interface_router(
            router['id'],
            {'subnet_id': subnet['id']}
        )
        
        # Create security group
        security_group = self.create_security_group(project_id)
        
        return {
            'network_id': network['id'],
            'subnet_id': subnet['id'],
            'router_id': router['id'],
            'security_group_id': security_group['id']
        }
    
    def create_security_group(self, project_id):
        """Create security group with common rules"""
        # Create security group
        sg = self.neutron.create_security_group({
            'security_group': {
                'name': 'default-web',
                'description': 'Security group for web servers',
                'tenant_id': project_id
            }
        })['security_group']
        
        # Add rules
        rules = [
            {'protocol': 'tcp', 'port_min': 22, 'port_max': 22},    # SSH
            {'protocol': 'tcp', 'port_min': 80, 'port_max': 80},    # HTTP
            {'protocol': 'tcp', 'port_min': 443, 'port_max': 443},  # HTTPS
            {'protocol': 'icmp', 'port_min': None, 'port_max': None} # ICMP
        ]
        
        for rule in rules:
            self.neutron.create_security_group_rule({
                'security_group_rule': {
                    'security_group_id': sg['id'],
                    'direction': 'ingress',
                    'ethertype': 'IPv4',
                    'protocol': rule['protocol'],
                    'port_range_min': rule['port_min'],
                    'port_range_max': rule['port_max'],
                    'remote_ip_prefix': '0.0.0.0/0'
                }
            })
        
        return sg
    
    def create_load_balancer(self, subnet_id, pool_members):
        """Create Neutron LBaaS v2 load balancer"""
        # Create load balancer
        lb = self.neutron.create_loadbalancer({
            'loadbalancer': {
                'name': 'web-lb',
                'vip_subnet_id': subnet_id,
                'admin_state_up': True
            }
        })['loadbalancer']
        
        # Wait for provisioning
        self._wait_for_lb_active(lb['id'])
        
        # Create listener
        listener = self.neutron.create_listener({
            'listener': {
                'name': 'web-listener',
                'loadbalancer_id': lb['id'],
                'protocol': 'HTTP',
                'protocol_port': 80,
                'admin_state_up': True
            }
        })['listener']
        
        # Create pool
        pool = self.neutron.create_lbaas_pool({
            'pool': {
                'name': 'web-pool',
                'listener_id': listener['id'],
                'protocol': 'HTTP',
                'lb_algorithm': 'ROUND_ROBIN',
                'admin_state_up': True
            }
        })['pool']
        
        # Add members
        for member in pool_members:
            self.neutron.create_lbaas_member({
                'member': {
                    'pool_id': pool['id'],
                    'address': member['address'],
                    'protocol_port': member['port'],
                    'weight': 1,
                    'admin_state_up': True
                }
            })
        
        # Create health monitor
        self.neutron.create_lbaas_healthmonitor({
            'healthmonitor': {
                'pool_id': pool['id'],
                'type': 'HTTP',
                'delay': 5,
                'timeout': 3,
                'max_retries': 3,
                'http_method': 'GET',
                'url_path': '/health',
                'expected_codes': '200',
                'admin_state_up': True
            }
        })
        
        return lb
```

### Cinder (Block Storage Service)
```python
from cinderclient import client as cinder_client

class CinderManager:
    """Manage OpenStack block storage"""
    
    def __init__(self, session):
        self.cinder = cinder_client.Client('3', session=session)
    
    def create_volume(self, name, size, volume_type=None, availability_zone=None):
        """Create a new volume"""
        volume = self.cinder.volumes.create(
            size=size,
            name=name,
            volume_type=volume_type,
            availability_zone=availability_zone,
            metadata={
                'created_by': 'automation',
                'purpose': 'data-storage'
            }
        )
        
        # Wait for available state
        while volume.status != 'available':
            time.sleep(2)
            volume = self.cinder.volumes.get(volume.id)
            if volume.status == 'error':
                raise Exception(f"Volume creation failed: {volume.id}")
        
        return volume
    
    def create_volume_from_snapshot(self, snapshot_id, name, size=None):
        """Create volume from snapshot"""
        snapshot = self.cinder.volume_snapshots.get(snapshot_id)
        
        volume = self.cinder.volumes.create(
            size=size or snapshot.size,
            snapshot_id=snapshot_id,
            name=name
        )
        
        return volume
    
    def attach_volume(self, server_id, volume_id, device=None):
        """Attach volume to instance"""
        nova = nova_client.Client('2.1', session=self.session)
        
        # Attach volume
        nova.volumes.create_server_volume(
            server_id,
            volume_id,
            device=device  # e.g., '/dev/vdb'
        )
        
        # Update volume metadata
        volume = self.cinder.volumes.get(volume_id)
        volume.update(metadata={
            'attached_to': server_id,
            'attach_time': datetime.utcnow().isoformat()
        })
        
        return True
    
    def create_backup(self, volume_id, name, incremental=False):
        """Create volume backup"""
        backup = self.cinder.backups.create(
            volume_id=volume_id,
            name=name,
            incremental=incremental,
            description=f"Backup of volume {volume_id}"
        )
        
        return backup
```

### Swift (Object Storage Service)
```python
from swiftclient import client as swift_client

class SwiftManager:
    """Manage OpenStack object storage"""
    
    def __init__(self, session):
        self.session = session
        self.swift = swift_client.Connection(session=session)
    
    def create_container(self, container_name, public=False):
        """Create storage container"""
        headers = {}
        if public:
            headers['X-Container-Read'] = '.r:*,.rlistings'
        
        self.swift.put_container(
            container_name,
            headers=headers
        )
        
        # Set container metadata
        self.swift.post_container(
            container_name,
            headers={
                'X-Container-Meta-Created-By': 'automation',
                'X-Container-Meta-Purpose': 'application-data'
            }
        )
        
        return container_name
    
    def upload_large_file(self, container, file_path, object_name):
        """Upload large file with segmentation"""
        segment_size = 1024 * 1024 * 1024  # 1GB segments
        
        with open(file_path, 'rb') as f:
            # Create segments container
            segments_container = f"{container}_segments"
            self.create_container(segments_container)
            
            segment_num = 0
            manifest = []
            
            while True:
                segment_data = f.read(segment_size)
                if not segment_data:
                    break
                
                segment_name = f"{object_name}/{segment_num:06d}"
                
                # Upload segment
                self.swift.put_object(
                    segments_container,
                    segment_name,
                    contents=segment_data
                )
                
                manifest.append({
                    'path': f"{segments_container}/{segment_name}",
                    'size_bytes': len(segment_data),
                    'etag': hashlib.md5(segment_data).hexdigest()
                })
                
                segment_num += 1
            
            # Create manifest
            self.swift.put_object(
                container,
                object_name,
                contents=json.dumps(manifest),
                headers={'X-Object-Manifest': f"{segments_container}/{object_name}/"}
            )
        
        return object_name
    
    def setup_cdn(self, container):
        """Enable CDN for container"""
        # This would integrate with a CDN provider
        cdn_config = {
            'cdn_enabled': True,
            'cdn_uri': f"https://cdn.example.com/{container}",
            'cdn_ttl': 86400,  # 24 hours
            'cdn_log_retention': True
        }
        
        self.swift.post_container(
            container,
            headers={
                'X-Container-Meta-CDN-Enabled': 'true',
                'X-Container-Meta-CDN-URI': cdn_config['cdn_uri'],
                'X-Container-Meta-CDN-TTL': str(cdn_config['cdn_ttl'])
            }
        )
        
        return cdn_config
```

### Glance (Image Service)
```python
from glanceclient import client as glance_client

class GlanceManager:
    """Manage OpenStack images"""
    
    def __init__(self, session):
        self.glance = glance_client.Client('2', session=session)
    
    def create_image_from_file(self, name, file_path, disk_format='qcow2', 
                              container_format='bare', visibility='private'):
        """Upload image from file"""
        # Create image metadata
        image = self.glance.images.create(
            name=name,
            disk_format=disk_format,
            container_format=container_format,
            visibility=visibility,
            min_disk=10,  # Minimum disk size in GB
            min_ram=1024,  # Minimum RAM in MB
            properties={
                'architecture': 'x86_64',
                'hypervisor_type': 'kvm',
                'os_type': 'linux'
            }
        )
        
        # Upload image data
        with open(file_path, 'rb') as f:
            self.glance.images.upload(image.id, f)
        
        # Update image status
        self.glance.images.update(
            image.id,
            tags=['production', 'ubuntu-20.04']
        )
        
        return image
    
    def create_image_from_instance(self, instance_id, image_name):
        """Create image from running instance"""
        nova = nova_client.Client('2.1', session=self.session)
        
        # Create snapshot
        image_id = nova.servers.create_image(
            instance_id,
            image_name,
            metadata={
                'created_from': instance_id,
                'created_at': datetime.utcnow().isoformat()
            }
        )
        
        # Wait for image to be active
        image = self.glance.images.get(image_id)
        while image.status != 'active':
            time.sleep(5)
            image = self.glance.images.get(image_id)
            if image.status == 'error':
                raise Exception(f"Image creation failed: {image_id}")
        
        return image
```

### Heat (Orchestration Service)
```yaml
# Heat Template Example
heat_template_version: 2018-08-31

description: Deploy a multi-tier web application

parameters:
  key_name:
    type: string
    description: SSH key pair name
  image_id:
    type: string
    description: Image ID for instances
  external_network_id:
    type: string
    description: External network ID

resources:
  # Network resources
  private_network:
    type: OS::Neutron::Net
    properties:
      name: app_network

  private_subnet:
    type: OS::Neutron::Subnet
    properties:
      network: { get_resource: private_network }
      cidr: 10.0.0.0/24
      dns_nameservers:
        - 8.8.8.8
        - 8.8.4.4

  router:
    type: OS::Neutron::Router
    properties:
      external_gateway_info:
        network: { get_param: external_network_id }

  router_interface:
    type: OS::Neutron::RouterInterface
    properties:
      router: { get_resource: router }
      subnet: { get_resource: private_subnet }

  # Security groups
  web_security_group:
    type: OS::Neutron::SecurityGroup
    properties:
      name: web_sg
      rules:
        - protocol: tcp
          port_range_min: 80
          port_range_max: 80
        - protocol: tcp
          port_range_min: 443
          port_range_max: 443
        - protocol: tcp
          port_range_min: 22
          port_range_max: 22

  # Load balancer
  load_balancer:
    type: OS::Octavia::LoadBalancer
    properties:
      vip_subnet: { get_resource: private_subnet }

  listener:
    type: OS::Octavia::Listener
    properties:
      loadbalancer: { get_resource: load_balancer }
      protocol: HTTP
      protocol_port: 80

  pool:
    type: OS::Octavia::Pool
    properties:
      listener: { get_resource: listener }
      lb_algorithm: ROUND_ROBIN
      protocol: HTTP

  # Auto-scaling group
  asg:
    type: OS::Heat::AutoScalingGroup
    properties:
      min_size: 2
      max_size: 10
      resource:
        type: web_server.yaml
        properties:
          key_name: { get_param: key_name }
          image: { get_param: image_id }
          flavor: m1.medium
          network: { get_resource: private_network }
          subnet: { get_resource: private_subnet }
          security_groups:
            - { get_resource: web_security_group }
          pool_id: { get_resource: pool }
          metadata:
            metering.server_group: { get_param: "OS::stack_id" }

  # Scaling policies
  scale_up_policy:
    type: OS::Heat::ScalingPolicy
    properties:
      adjustment_type: change_in_capacity
      auto_scaling_group_id: { get_resource: asg }
      cooldown: 60
      scaling_adjustment: 1

  scale_down_policy:
    type: OS::Heat::ScalingPolicy
    properties:
      adjustment_type: change_in_capacity
      auto_scaling_group_id: { get_resource: asg }
      cooldown: 60
      scaling_adjustment: -1

  # Ceilometer alarms
  cpu_alarm_high:
    type: OS::Aodh::GnocchiAggregationByResourcesAlarm
    properties:
      meter_name: cpu_util
      statistic: avg
      period: 300
      evaluation_periods: 1
      threshold: 80
      comparison_operator: gt
      alarm_actions:
        - { get_attr: [scale_up_policy, signal_url] }
      resource_type: instance
      query:
        str_replace:
          template: '{"=": {"server_group": "stack_id"}}'
          params:
            stack_id: { get_param: "OS::stack_id" }

outputs:
  load_balancer_ip:
    description: IP address of load balancer
    value: { get_attr: [load_balancer, vip_address] }
```

### Advanced Heat Orchestration
```python
from heatclient import client as heat_client
import yaml

class HeatOrchestrator:
    """Advanced Heat orchestration management"""
    
    def __init__(self, session):
        self.heat = heat_client.Client('1', session=session)
    
    def deploy_stack(self, stack_name, template_file, environment_file=None, parameters={}):
        """Deploy Heat stack"""
        # Load template
        with open(template_file, 'r') as f:
            template = yaml.safe_load(f)
        
        # Load environment if provided
        environment = {}
        if environment_file:
            with open(environment_file, 'r') as f:
                environment = yaml.safe_load(f)
        
        # Create stack
        stack = self.heat.stacks.create(
            stack_name=stack_name,
            template=yaml.dump(template),
            environment=yaml.dump(environment),
            parameters=parameters,
            timeout_mins=60,
            rollback_on_failure=True,
            disable_rollback=False
        )
        
        # Monitor stack creation
        stack_id = stack['stack']['id']
        return self.monitor_stack(stack_name, stack_id)
    
    def monitor_stack(self, stack_name, stack_id):
        """Monitor stack deployment progress"""
        while True:
            stack = self.heat.stacks.get(stack_id)
            
            if stack.status == 'CREATE_COMPLETE':
                return {
                    'status': 'success',
                    'outputs': stack.outputs,
                    'resources': self._get_stack_resources(stack_id)
                }
            elif stack.status == 'CREATE_FAILED':
                return {
                    'status': 'failed',
                    'reason': stack.stack_status_reason,
                    'events': self._get_stack_events(stack_id)
                }
            
            time.sleep(10)
    
    def update_stack(self, stack_id, template_file, parameters={}):
        """Update existing stack"""
        with open(template_file, 'r') as f:
            template = yaml.safe_load(f)
        
        self.heat.stacks.update(
            stack_id,
            template=yaml.dump(template),
            parameters=parameters,
            existing_parameters=True
        )
        
        return self.monitor_stack_update(stack_id)
```

## Advanced Features

### Ceilometer (Telemetry Service)
```python
from ceilometerclient import client as ceilometer_client

class TelemetryManager:
    """Manage OpenStack telemetry and monitoring"""
    
    def __init__(self, session):
        self.ceilometer = ceilometer_client.Client('2', session=session)
    
    def create_alarm(self, name, meter_name, threshold, comparison_operator='gt'):
        """Create monitoring alarm"""
        alarm = self.ceilometer.alarms.create(
            name=name,
            type='threshold',
            meter_name=meter_name,
            statistic='avg',
            period=300,
            evaluation_periods=1,
            threshold=threshold,
            comparison_operator=comparison_operator,
            alarm_actions=['http://webhook.example.com/scale-up'],
            ok_actions=['http://webhook.example.com/scale-normal'],
            insufficient_data_actions=['http://webhook.example.com/scale-unknown']
        )
        
        return alarm
    
    def get_resource_metrics(self, resource_id, meter_name, period=3600):
        """Get metrics for a resource"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(seconds=period)
        
        samples = self.ceilometer.statistics.list(
            meter_name=meter_name,
            q=[
                {'field': 'resource_id', 'op': 'eq', 'value': resource_id},
                {'field': 'timestamp', 'op': 'ge', 'value': start_time.isoformat()},
                {'field': 'timestamp', 'op': 'le', 'value': end_time.isoformat()}
            ],
            period=300,
            aggregation='avg'
        )
        
        return [{
            'timestamp': s.period_start,
            'avg': s.avg,
            'min': s.min,
            'max': s.max,
            'count': s.count
        } for s in samples]
```

### Ironic (Bare Metal Service)
```python
from ironicclient import client as ironic_client

class IronicManager:
    """Manage bare metal provisioning"""
    
    def __init__(self, session):
        self.ironic = ironic_client.Client('1', session=session)
    
    def enroll_node(self, driver, driver_info, properties):
        """Enroll a bare metal node"""
        node = self.ironic.node.create(
            driver=driver,  # e.g., 'ipmi'
            driver_info=driver_info,
            properties=properties,
            network_interface='neutron',
            resource_class='baremetal-large'
        )
        
        # Create ports for the node
        for mac in properties.get('mac_addresses', []):
            self.ironic.port.create(
                node_uuid=node.uuid,
                address=mac
            )
        
        # Move node through states
        self.ironic.node.set_provision_state(node.uuid, 'manage')
        self.ironic.node.set_provision_state(node.uuid, 'inspect')
        
        return node
    
    def deploy_bare_metal(self, node_uuid, image_uuid, network_uuid):
        """Deploy OS on bare metal node"""
        # Set deploy configuration
        patch = [
            {'op': 'add', 'path': '/instance_info/image_source', 'value': image_uuid},
            {'op': 'add', 'path': '/instance_info/root_gb', 'value': 100},
            {'op': 'add', 'path': '/instance_info/swap_mb', 'value': 4096}
        ]
        
        self.ironic.node.update(node_uuid, patch)
        
        # Create network attachment
        self.create_vif_attachment(node_uuid, network_uuid)
        
        # Deploy
        self.ironic.node.set_provision_state(node_uuid, 'provide')
        self.ironic.node.set_provision_state(node_uuid, 'active')
        
        return self.wait_for_provisioning(node_uuid)
```

### Manila (Shared File System Service)
```python
from manilaclient import client as manila_client

class ManilaManager:
    """Manage shared file systems"""
    
    def __init__(self, session):
        self.manila = manila_client.Client('2', session=session)
    
    def create_share(self, name, size, share_proto='NFS', share_type=None):
        """Create a shared file system"""
        share = self.manila.shares.create(
            share_proto=share_proto,
            size=size,
            name=name,
            share_type=share_type,
            metadata={
                'purpose': 'shared-storage',
                'team': 'platform'
            }
        )
        
        # Wait for available status
        while share.status != 'available':
            time.sleep(5)
            share = self.manila.shares.get(share.id)
            if share.status == 'error':
                raise Exception(f"Share creation failed: {share.id}")
        
        return share
    
    def grant_access(self, share_id, access_type='ip', access_to='10.0.0.0/24'):
        """Grant access to share"""
        access = self.manila.shares.allow(
            share_id,
            access_type=access_type,
            access_to=access_to,
            access_level='rw'
        )
        
        return access
    
    def create_share_replica(self, share_id, availability_zone):
        """Create share replica for HA"""
        replica = self.manila.share_replicas.create(
            share_id,
            availability_zone=availability_zone
        )
        
        return replica
```

## Production Deployment

### High Availability Configuration
```python
class OpenStackHA:
    """High availability configuration for OpenStack"""
    
    def __init__(self):
        self.config = {
            'controllers': ['controller1', 'controller2', 'controller3'],
            'vip': '10.0.0.100',
            'database_vip': '10.0.0.101',
            'message_queue_vip': '10.0.0.102'
        }
    
    def configure_haproxy(self):
        """HAProxy configuration for OpenStack services"""
        haproxy_config = """
global
    daemon
    maxconn 4000
    log /dev/log local0

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option httplog
    option redispatch
    retries 3

# Keystone API
listen keystone_api
    bind *:5000
    balance roundrobin
    option httpchk GET /v3
    {% for controller in controllers %}
    server {{ controller }} {{ controller }}:5000 check inter 2000 rise 2 fall 5
    {% endfor %}

# Nova API
listen nova_api
    bind *:8774
    balance roundrobin
    option httpchk GET /
    {% for controller in controllers %}
    server {{ controller }} {{ controller }}:8774 check inter 2000 rise 2 fall 5
    {% endfor %}

# Neutron API
listen neutron_api
    bind *:9696
    balance roundrobin
    option httpchk GET /
    {% for controller in controllers %}
    server {{ controller }} {{ controller }}:9696 check inter 2000 rise 2 fall 5
    {% endfor %}

# Glance API
listen glance_api
    bind *:9292
    balance roundrobin
    option httpchk GET /versions
    {% for controller in controllers %}
    server {{ controller }} {{ controller }}:9292 check inter 2000 rise 2 fall 5
    {% endfor %}

# Horizon Dashboard
listen horizon
    bind *:80
    balance source
    option httpchk GET /auth/login/
    cookie SERVERID insert indirect nocache
    {% for controller in controllers %}
    server {{ controller }} {{ controller }}:80 check inter 2000 rise 2 fall 5 cookie {{ controller }}
    {% endfor %}
"""
        return haproxy_config
    
    def configure_galera_cluster(self):
        """Configure Galera cluster for MySQL"""
        galera_config = """
[mysqld]
binlog_format=ROW
default-storage-engine=innodb
innodb_autoinc_lock_mode=2
bind-address=0.0.0.0

# Galera Provider Configuration
wsrep_on=ON
wsrep_provider=/usr/lib/galera/libgalera_smm.so
wsrep_provider_options="gcache.size=1G"

# Galera Cluster Configuration
wsrep_cluster_name="openstack_cluster"
wsrep_cluster_address="gcomm://10.0.0.11,10.0.0.12,10.0.0.13"

# Galera Synchronization Configuration
wsrep_sst_method=rsync

# Galera Node Configuration
wsrep_node_address="10.0.0.11"
wsrep_node_name="controller1"
"""
        return galera_config
```

### Performance Tuning
```python
class PerformanceTuning:
    """OpenStack performance optimization"""
    
    def optimize_nova_compute(self):
        """Nova compute optimization settings"""
        nova_conf = {
            'DEFAULT': {
                'cpu_allocation_ratio': 16.0,
                'ram_allocation_ratio': 1.5,
                'disk_allocation_ratio': 1.0,
                'reserved_host_memory_mb': 512,
                'reserved_host_cpus': 1
            },
            'libvirt': {
                'virt_type': 'kvm',
                'cpu_mode': 'host-passthrough',
                'disk_cachemodes': 'network=writeback',
                'live_migration_bandwidth': 0,
                'live_migration_completion_timeout': 800,
                'live_migration_progress_timeout': 150
            },
            'scheduler': {
                'driver': 'filter_scheduler',
                'available_filters': 'nova.scheduler.filters.all_filters',
                'enabled_filters': [
                    'AvailabilityZoneFilter',
                    'ComputeFilter',
                    'ComputeCapabilitiesFilter',
                    'ImagePropertiesFilter',
                    'ServerGroupAntiAffinityFilter',
                    'ServerGroupAffinityFilter',
                    'PciPassthroughFilter',
                    'NUMATopologyFilter',
                    'AggregateInstanceExtraSpecsFilter'
                ]
            }
        }
        return nova_conf
    
    def optimize_neutron(self):
        """Neutron optimization for large scale"""
        neutron_conf = {
            'DEFAULT': {
                'api_workers': 8,
                'rpc_workers': 8,
                'rpc_state_report_workers': 4,
                'agent_down_time': 75
            },
            'database': {
                'connection': 'mysql+pymysql://neutron:password@vip/neutron',
                'max_pool_size': 100,
                'max_overflow': 50,
                'pool_timeout': 30
            },
            'oslo_messaging_rabbit': {
                'rabbit_ha_queues': True,
                'amqp_durable_queues': True,
                'rabbit_retry_interval': 1,
                'rabbit_retry_backoff': 2,
                'rabbit_max_retries': 0
            }
        }
        return neutron_conf
```

### Monitoring and Logging
```python
class OpenStackMonitoring:
    """Comprehensive monitoring for OpenStack"""
    
    def setup_prometheus_exporters(self):
        """Configure Prometheus exporters for OpenStack"""
        exporters = {
            'openstack_exporter': {
                'port': 9183,
                'config': {
                    'cloud': 'default',
                    'refresh_interval': 60,
                    'metrics': [
                        'nova_instances',
                        'neutron_networks',
                        'cinder_volumes',
                        'glance_images',
                        'swift_containers'
                    ]
                }
            },
            'libvirt_exporter': {
                'port': 9177,
                'config': {
                    'libvirt_uri': 'qemu:///system'
                }
            },
            'mysql_exporter': {
                'port': 9104,
                'config': {
                    'data_source_name': 'exporter:password@tcp(vip:3306)/'
                }
            }
        }
        return exporters
    
    def create_monitoring_dashboards(self):
        """Grafana dashboards for OpenStack"""
        dashboards = {
            'compute_overview': {
                'title': 'OpenStack Compute Overview',
                'panels': [
                    {
                        'title': 'Total Instances',
                        'query': 'sum(openstack_nova_instances)'
                    },
                    {
                        'title': 'CPU Allocation',
                        'query': 'sum(openstack_nova_vcpus_used) / sum(openstack_nova_vcpus_available)'
                    },
                    {
                        'title': 'Memory Usage',
                        'query': 'sum(openstack_nova_memory_used_bytes) / sum(openstack_nova_memory_available_bytes)'
                    }
                ]
            },
            'network_overview': {
                'title': 'OpenStack Network Overview',
                'panels': [
                    {
                        'title': 'Active Networks',
                        'query': 'count(openstack_neutron_networks)'
                    },
                    {
                        'title': 'Floating IPs',
                        'query': 'count(openstack_neutron_floating_ips)'
                    },
                    {
                        'title': 'Security Groups',
                        'query': 'count(openstack_neutron_security_groups)'
                    }
                ]
            }
        }
        return dashboards
```

## Best Practices Summary

1. **Architecture**: Deploy control plane in HA mode with at least 3 controllers
2. **Networking**: Use VLAN or VXLAN for tenant isolation, implement proper security groups
3. **Storage**: Choose appropriate storage backends (Ceph for unified storage is popular)
4. **Performance**: Tune database connections, message queue, and API workers
5. **Security**: Enable SSL/TLS for all endpoints, use Keystone federation for enterprise SSO
6. **Monitoring**: Implement comprehensive monitoring with metrics, logs, and traces
7. **Backup**: Regular backups of databases and critical configurations
8. **Updates**: Plan rolling updates with proper testing in staging environment

---

### 📡 Stay Updated

**Release Notes**: [OpenStack Releases](https://releases.openstack.org/) • [Security Advisories](https://security.openstack.org/) • [Project Updates](https://governance.openstack.org/tc/)

**Project News**: [OpenStack Blog](https://www.openstack.org/blog/) • [Superuser Magazine](http://superuser.openstack.org/) • [Foundation News](https://www.openstack.org/news/)

**Community**: [Mailing Lists](http://lists.openstack.org/) • [IRC Channels](https://docs.openstack.org/contributors/common/irc.html) • [OpenStack Summit](https://www.openstack.org/summit/)