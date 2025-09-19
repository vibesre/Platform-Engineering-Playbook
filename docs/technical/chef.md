# Chef: Policy-Based Configuration Management

## Overview

Chef is a powerful configuration management tool that uses a policy-based approach to automate infrastructure. Using Ruby as its configuration language, Chef treats infrastructure as code, enabling version control, testing, and collaborative infrastructure development. Chef excels at managing complex, heterogeneous environments with its flexible cookbook system.

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Chef Server                               │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │   Erchef     │  │  PostgreSQL  │  │    Elasticsearch       │  │
│  │   (API)      │  │  (Data Store)│  │    (Search)            │  │
│  └──────┬───────┘  └──────┬───────┘  └───────────┬────────────┘  │
│         │                  │                       │                │
│  ┌──────┴──────────────────┴───────────────────────┴────────────┐ │
│  │                        Nginx (Router)                         │ │
│  └───────────────────────────┬──────────────────────────────────┘ │
└─────────────────────────────┼──────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────┴────────┐    ┌───────┴────────┐   ┌──────┴──────────┐
│  Chef Client   │    │ Chef Workstation│   │   Chef Client   │
│    (Node)      │    │  (Development)  │   │     (Node)      │
│  ┌──────────┐  │    │  ┌──────────┐  │   │  ┌──────────┐  │
│  │   Ohai   │  │    │  │  Knife   │  │   │  │   Ohai   │  │
│  │(Attributes)  │    │  │  (CLI)   │  │   │  │(Attributes)  │
│  └──────────┘  │    │  └──────────┘  │   │  └──────────┘  │
│  ┌──────────┐  │    │  ┌──────────┐  │   │  ┌──────────┐  │
│  │Chef-Client│ │    │  │ ChefSpec │  │   │  │Chef-Client│ │
│  │ (Runner)  │ │    │  │ (Testing) │  │   │  │ (Runner)  │ │
│  └──────────┘  │    │  └──────────┘  │   │  └──────────┘  │
└────────────────┘    └─────────────────┘   └─────────────────┘
```

### Chef Resource Model

```ruby
# Resource Declaration Model
resource_type 'resource_name' do
  property1 value1
  property2 value2
  action :action_name
  notifies :action, 'resource[name]', :timing
  only_if { condition }
  not_if { condition }
end
```

## Practical Examples

### Basic Cookbook Structure

```ruby
# cookbooks/webapp/metadata.rb
name 'webapp'
maintainer 'Platform Team'
maintainer_email 'platform@example.com'
license 'Apache-2.0'
description 'Configures web application stack'
version '2.1.0'

depends 'nginx', '~> 10.0'
depends 'nodejs', '~> 7.0'
depends 'postgresql', '~> 8.0'

supports 'ubuntu', '>= 18.04'
supports 'centos', '>= 7.0'

chef_version '>= 15.0'
```

```ruby
# cookbooks/webapp/recipes/default.rb
#
# Cookbook:: webapp
# Recipe:: default
#

# Include platform-specific setup
include_recipe "webapp::#{node['platform_family']}"

# Install base packages
package %w(git curl wget vim) do
  action :install
end

# Create application user
user node['webapp']['user'] do
  comment 'Web Application User'
  home node['webapp']['home']
  shell '/bin/bash'
  manage_home true
  action :create
end

# Create directory structure
%w[releases shared shared/config shared/log shared/pids].each do |dir|
  directory "#{node['webapp']['deploy_to']}/#{dir}" do
    owner node['webapp']['user']
    group node['webapp']['group']
    mode '0755'
    recursive true
    action :create
  end
end

# Include component recipes
include_recipe 'webapp::nginx'
include_recipe 'webapp::nodejs'
include_recipe 'webapp::app'
include_recipe 'webapp::monitoring'
```

### Advanced Custom Resource

```ruby
# cookbooks/webapp/resources/deployment.rb
resource_name :webapp_deployment
provides :webapp_deployment
unified_mode true

property :app_name, String, name_property: true
property :version, String, required: true
property :port, Integer, default: 3000
property :environment, Hash, default: {}
property :health_check_path, String, default: '/health'
property :deployment_strategy, String, default: 'rolling', equal_to: %w(rolling blue_green canary)

action :deploy do
  # Create release directory
  release_path = "#{new_resource.app_name}/releases/#{new_resource.version}"
  
  directory release_path do
    owner node['webapp']['user']
    group node['webapp']['group']
    mode '0755'
    recursive true
    action :create
  end
  
  # Download and extract application
  remote_file "#{release_path}/app.tar.gz" do
    source "https://artifacts.example.com/#{new_resource.app_name}/#{new_resource.version}.tar.gz"
    owner node['webapp']['user']
    group node['webapp']['group']
    mode '0644'
    action :create
    notifies :run, 'execute[extract_app]', :immediately
  end
  
  execute 'extract_app' do
    command "tar -xzf app.tar.gz"
    cwd release_path
    user node['webapp']['user']
    action :nothing
  end
  
  # Generate configuration
  template "#{release_path}/config/app.yml" do
    source 'app.yml.erb'
    owner node['webapp']['user']
    group node['webapp']['group']
    mode '0640'
    variables(
      port: new_resource.port,
      environment: new_resource.environment,
      version: new_resource.version
    )
  end
  
  # Deployment strategy
  case new_resource.deployment_strategy
  when 'blue_green'
    blue_green_deploy
  when 'canary'
    canary_deploy
  else
    rolling_deploy
  end
end

action :rollback do
  # Implementation for rollback
  previous_version = get_previous_version(new_resource.app_name)
  
  link "#{new_resource.app_name}/current" do
    to "#{new_resource.app_name}/releases/#{previous_version}"
    owner node['webapp']['user']
    group node['webapp']['group']
    action :create
    notifies :restart, "service[#{new_resource.app_name}]", :immediately
  end
end

action_class do
  def blue_green_deploy
    # Prepare inactive environment
    inactive_port = new_resource.port == 3000 ? 3001 : 3000
    
    # Deploy to inactive
    systemd_unit "#{new_resource.app_name}-#{inactive_port}" do
      content lazy {
        {
          'Unit' => {
            'Description' => "#{new_resource.app_name} (Port #{inactive_port})",
            'After' => 'network.target'
          },
          'Service' => {
            'Type' => 'simple',
            'User' => node['webapp']['user'],
            'WorkingDirectory' => "#{release_path}",
            'Environment' => [
              "PORT=#{inactive_port}",
              "NODE_ENV=production"
            ],
            'ExecStart' => '/usr/bin/node app.js',
            'Restart' => 'always'
          },
          'Install' => {
            'WantedBy' => 'multi-user.target'
          }
        }
      }
      action [:create, :start]
    end
    
    # Health check
    ruby_block 'health_check' do
      block do
        require 'net/http'
        uri = URI("http://localhost:#{inactive_port}#{new_resource.health_check_path}")
        
        30.times do
          begin
            response = Net::HTTP.get_response(uri)
            break if response.code == '200'
          rescue
            sleep 2
          end
        end
      end
    end
    
    # Switch nginx upstream
    template '/etc/nginx/conf.d/upstream.conf' do
      source 'nginx_upstream.erb'
      variables(
        app_name: new_resource.app_name,
        port: inactive_port
      )
      notifies :reload, 'service[nginx]', :immediately
    end
  end
  
  def get_previous_version(app_name)
    # Logic to determine previous version
    Dir.glob("#{app_name}/releases/*").sort[-2] || 'unknown'
  end
end
```

### Environment-Specific Configurations

```ruby
# cookbooks/webapp/attributes/default.rb
default['webapp']['user'] = 'webapp'
default['webapp']['group'] = 'webapp'
default['webapp']['deploy_to'] = '/opt/webapp'

# Environment-specific settings
case node.chef_environment
when 'production'
  default['webapp']['server_count'] = 4
  default['webapp']['memory_limit'] = '2G'
  default['webapp']['log_level'] = 'info'
when 'staging'
  default['webapp']['server_count'] = 2
  default['webapp']['memory_limit'] = '1G'
  default['webapp']['log_level'] = 'debug'
else
  default['webapp']['server_count'] = 1
  default['webapp']['memory_limit'] = '512M'
  default['webapp']['log_level'] = 'debug'
end

# Platform-specific settings
case node['platform_family']
when 'debian'
  default['webapp']['packages'] = %w(build-essential libssl-dev)
  default['webapp']['service_manager'] = 'systemd'
when 'rhel'
  default['webapp']['packages'] = %w(gcc-c++ openssl-devel)
  default['webapp']['service_manager'] = 'systemd'
end
```

### Data Bags and Encrypted Secrets

```ruby
# cookbooks/webapp/recipes/database.rb
# Load encrypted data bag
db_creds = Chef::EncryptedDataBagItem.load('credentials', 'database')

# Configure database connection
template "#{node['webapp']['deploy_to']}/shared/config/database.yml" do
  source 'database.yml.erb'
  owner node['webapp']['user']
  group node['webapp']['group']
  mode '0640'
  variables(
    host: db_creds['host'],
    port: db_creds['port'],
    database: db_creds['database'],
    username: db_creds['username'],
    password: db_creds['password'],
    pool: node['webapp']['db_pool_size']
  )
  notifies :restart, 'service[webapp]', :delayed
end

# Using Chef Vault (more secure alternative)
chef_gem 'chef-vault' do
  compile_time true
end

require 'chef-vault'

item = ChefVault::Item.load('secrets', 'api_keys')
api_key = item['stripe_key']

file "#{node['webapp']['deploy_to']}/shared/config/api_keys.yml" do
  content({ stripe: api_key }.to_yaml)
  owner node['webapp']['user']
  group node['webapp']['group']
  mode '0600'
  sensitive true
end
```

### Complex Orchestration with Chef

```ruby
# cookbooks/webapp/recipes/orchestrated_deploy.rb
# Orchestrated deployment across multiple nodes

# Step 1: Prepare all nodes
ruby_block 'prepare_deployment' do
  block do
    Chef::Log.info "Preparing deployment for version #{node['webapp']['deploy_version']}"
    
    # Search for all web nodes
    web_nodes = search(:node, 'role:web AND chef_environment:production')
    
    # Store deployment state
    node.run_state['deployment'] = {
      version: node['webapp']['deploy_version'],
      nodes: web_nodes.map(&:name),
      start_time: Time.now
    }
  end
end

# Step 2: Sequential deployment with verification
ruby_block 'orchestrate_deployment' do
  block do
    deployment = node.run_state['deployment']
    failed_nodes = []
    
    deployment[:nodes].each_with_index do |node_name, index|
      Chef::Log.info "Deploying to #{node_name} (#{index + 1}/#{deployment[:nodes].length})"
      
      # Remove from load balancer
      execute "remove_from_lb_#{node_name}" do
        command "aws elb deregister-instances-from-load-balancer \
                 --load-balancer-name prod-webapp \
                 --instances #{node_name}"
      end
      
      # Deploy to node
      execute "deploy_to_#{node_name}" do
        command "knife ssh 'name:#{node_name}' \
                 'sudo chef-client -o webapp::deploy' \
                 -x deploy -i ~/.ssh/deploy_key"
        timeout 600
      end
      
      # Verify deployment
      ruby_block "verify_#{node_name}" do
        block do
          require 'net/http'
          
          healthy = false
          30.times do
            begin
              uri = URI("http://#{node_name}:3000/health")
              response = Net::HTTP.get_response(uri)
              if response.code == '200'
                healthy = true
                break
              end
            rescue
              sleep 5
            end
          end
          
          if healthy
            # Add back to load balancer
            `aws elb register-instances-with-load-balancer \
             --load-balancer-name prod-webapp \
             --instances #{node_name}`
          else
            failed_nodes << node_name
          end
        end
      end
      
      # Pause between nodes
      ruby_block "pause_#{index}" do
        block do
          sleep 30 unless index == deployment[:nodes].length - 1
        end
      end
    end
    
    # Handle failures
    unless failed_nodes.empty?
      raise "Deployment failed on nodes: #{failed_nodes.join(', ')}"
    end
  end
end
```

## Best Practices

### 1. Cookbook Development Workflow

```ruby
# .kitchen.yml for Test Kitchen
---
driver:
  name: vagrant
  
provisioner:
  name: chef_zero
  product_name: chef
  install_strategy: always
  
verifier:
  name: inspec
  
platforms:
  - name: ubuntu-20.04
  - name: centos-7
  
suites:
  - name: default
    run_list:
      - recipe[webapp::default]
    attributes:
      webapp:
        version: '1.0.0'
        port: 3000
  
  - name: production
    run_list:
      - recipe[webapp::default]
    attributes:
      webapp:
        environment: production
        enable_monitoring: true
```

### 2. Testing with ChefSpec

```ruby
# spec/unit/recipes/default_spec.rb
require 'spec_helper'

describe 'webapp::default' do
  let(:chef_run) do
    ChefSpec::ServerRunner.new(platform: 'ubuntu', version: '20.04') do |node|
      node.automatic['memory']['total'] = '2048MB'
      node.override['webapp']['version'] = '1.2.3'
    end.converge(described_recipe)
  end
  
  it 'creates webapp user' do
    expect(chef_run).to create_user('webapp').with(
      home: '/home/webapp',
      shell: '/bin/bash'
    )
  end
  
  it 'installs required packages' do
    expect(chef_run).to install_package(%w(git curl wget vim))
  end
  
  it 'creates application directories' do
    %w[releases shared shared/config].each do |dir|
      expect(chef_run).to create_directory("/opt/webapp/#{dir}").with(
        owner: 'webapp',
        group: 'webapp',
        mode: '0755'
      )
    end
  end
  
  it 'includes nginx recipe' do
    expect(chef_run).to include_recipe('webapp::nginx')
  end
  
  context 'on production environment' do
    let(:chef_run) do
      ChefSpec::ServerRunner.new do |node|
        node.chef_environment = 'production'
      end.converge(described_recipe)
    end
    
    it 'sets production memory limit' do
      expect(chef_run.node['webapp']['memory_limit']).to eq('2G')
    end
  end
end
```

### 3. InSpec Integration Tests

```ruby
# test/integration/default/default_test.rb
describe user('webapp') do
  it { should exist }
  its('home') { should eq '/home/webapp' }
  its('shell') { should eq '/bin/bash' }
end

describe directory('/opt/webapp') do
  it { should exist }
  it { should be_directory }
  it { should be_owned_by 'webapp' }
  it { should be_grouped_into 'webapp' }
end

describe package('nginx') do
  it { should be_installed }
end

describe service('nginx') do
  it { should be_enabled }
  it { should be_running }
end

describe port(80) do
  it { should be_listening }
  its('protocols') { should include 'tcp' }
end

describe http('http://localhost/health') do
  its('status') { should eq 200 }
  its('body') { should include 'OK' }
end

# Security tests
describe file('/opt/webapp/shared/config/database.yml') do
  it { should exist }
  it { should be_owned_by 'webapp' }
  its('mode') { should cmp '0640' }
  its('content') { should_not include 'password: password' }
end
```

### 4. Policy Files

```ruby
# Policyfile.rb
name 'webapp_policy'

default_source :supermarket

run_list 'webapp::default', 'monitoring::agent'

cookbook 'webapp', path: '.'
cookbook 'monitoring', git: 'https://github.com/company/chef-monitoring.git'

# Version constraints
cookbook 'nginx', '~> 10.0'
cookbook 'postgresql', '~> 8.0', :supermarket

# Environment-specific attributes
default['webapp']['version'] = '2.0.0'

# Named run lists for different scenarios
named_run_list 'deploy', 'webapp::deploy'
named_run_list 'rollback', 'webapp::rollback'

# Include policy group specific attributes
include_policy 'base_policy', git: 'https://github.com/company/chef-policies.git', path: 'policies/base.rb'
```

## Production Deployment Patterns

### 1. Chef Automate Integration

```ruby
# chef-automate configuration
automate_config = {
  'url' => 'https://automate.example.com',
  'token' => Chef::EncryptedDataBagItem.load('automate', 'token')['token'],
  'verify_ssl' => true
}

# Report handler for Automate
chef_handler 'Chef::Handler::AutomateReport' do
  source 'chef/handler/automate_report'
  arguments [automate_config]
  action :enable
end

# Compliance scanning
include_recipe 'audit::default'

# InSpec profiles for compliance
default['audit']['profiles'] = [
  {
    'name' => 'cis-ubuntu-18.04-level1',
    'compliance' => 'admin/cis-ubuntu-18.04-level1'
  },
  {
    'name' => 'company-baseline',
    'git' => 'https://github.com/company/inspec-baseline.git'
  }
]
```

### 2. Multi-Region Deployment

```ruby
# cookbooks/webapp/recipes/multi_region.rb
# Dynamic region configuration
region = node['ec2']['placement_availability_zone'].chop

# Region-specific settings
region_config = data_bag_item('regions', region)

# Configure region-specific database
node.override['webapp']['database']['host'] = region_config['db_endpoint']
node.override['webapp']['cache']['endpoint'] = region_config['redis_endpoint']

# Set up cross-region replication
if node['webapp']['enable_replication']
  remote_regions = region_config['peer_regions']
  
  remote_regions.each do |remote_region|
    # Configure VPN or peering connection
    execute "setup_peering_to_#{remote_region}" do
      command "aws ec2 create-vpc-peering-connection \
               --vpc-id #{node['ec2']['vpc_id']} \
               --peer-vpc-id #{data_bag_item('regions', remote_region)['vpc_id']} \
               --peer-region #{remote_region}"
      not_if "aws ec2 describe-vpc-peering-connections \
              --filters Name=status-code,Values=active \
              --query 'VpcPeeringConnections[?PeerVpcInfo.Region==`#{remote_region}`]' \
              --output text | grep active"
    end
  end
end

# Deploy application with region awareness
webapp_deployment node['webapp']['name'] do
  version node['webapp']['version']
  environment(
    'AWS_REGION' => region,
    'REPLICA_REGIONS' => remote_regions.join(',')
  )
  action :deploy
end
```

### 3. Habitat Integration

```ruby
# cookbooks/webapp/recipes/habitat.rb
# Install Habitat
hab_install 'install habitat'

# Configure Habitat Supervisor
hab_sup 'default' do
  permanent_peer true
  listen_ctl '0.0.0.0:9632'
  listen_gossip '0.0.0.0:9638'
  listen_http '0.0.0.0:9631'
  
  # Join ring
  peer node['habitat']['initial_peer'] if node['habitat']['initial_peer']
  
  action [:run]
end

# Load application package
hab_package 'company/webapp' do
  version node['webapp']['habitat_version']
  channel node['webapp']['habitat_channel']
  action :install
end

# Configure and start service
hab_service 'company/webapp' do
  strategy 'rolling'
  topology 'leader'
  
  # Bind to dependencies
  bind [
    'database:postgresql.default',
    'cache:redis.default'
  ]
  
  # Configuration
  config(
    'port' => node['webapp']['port'],
    'log_level' => node['webapp']['log_level']
  )
  
  action [:load, :start]
end
```

### 4. Container Orchestration

```ruby
# cookbooks/webapp/recipes/kubernetes.rb
# Deploy to Kubernetes using Chef
k8s_namespace 'webapp' do
  api_url node['kubernetes']['api_endpoint']
  client_certificate node['kubernetes']['client_cert']
  client_key node['kubernetes']['client_key']
  action :create
end

# Create ConfigMap from Chef attributes
k8s_config_map 'webapp-config' do
  namespace 'webapp'
  data(
    'app.yml' => {
      'database' => {
        'host' => node['webapp']['database']['host'],
        'pool' => node['webapp']['database']['pool']
      },
      'cache' => {
        'url' => node['webapp']['cache']['url']
      }
    }.to_yaml
  )
end

# Deploy application
k8s_deployment 'webapp' do
  namespace 'webapp'
  replicas node['webapp']['replicas']
  
  container 'webapp' do
    image "registry.example.com/webapp:#{node['webapp']['version']}"
    port 3000
    
    env [
      { name: 'NODE_ENV', value: node.chef_environment },
      { name: 'PORT', value: '3000' }
    ]
    
    volume_mount 'config' do
      mount_path '/app/config'
      read_only true
    end
    
    resources(
      limits: {
        cpu: node['webapp']['cpu_limit'],
        memory: node['webapp']['memory_limit']
      },
      requests: {
        cpu: node['webapp']['cpu_request'],
        memory: node['webapp']['memory_request']
      }
    )
  end
  
  volume 'config' do
    config_map 'webapp-config'
  end
end

# Create service
k8s_service 'webapp' do
  namespace 'webapp'
  port 80
  target_port 3000
  type 'LoadBalancer'
  selector app: 'webapp'
end
```

## Performance Optimization

### 1. Chef Client Configuration

```ruby
# /etc/chef/client.rb
log_level :info
log_location '/var/log/chef/client.log'
chef_server_url 'https://chef.example.com/organizations/company'

# Performance tuning
node_name 'web-prod-01'
environment 'production'

# Ohai plugins to disable for faster runs
ohai.disabled_plugins = [:Passwd, :Sessions, :Interrupts]

# Splay to prevent thundering herd
splay 300
interval 1800

# Configure reporting
enable_reporting false
exception_handlers << Chef::Handler::ErrorReport.new()

# Resource cloning
resource_cloning false

# Minimal Ohai
minimal_ohai true
```

### 2. Cookbook Optimization

```ruby
# Use lazy evaluation for expensive operations
template '/etc/app/config.yml' do
  source 'config.yml.erb'
  variables lazy {
    {
      # Only query when needed
      database_host: search(:node, 'role:database').first['ipaddress'],
      cache_nodes: search(:node, 'role:cache').map { |n| n['ipaddress'] }
    }
  }
end

# Compile-time vs converge-time
# Install at compile time when needed for other resources
package 'build-essential' do
  action :nothing
end.run_action(:install)

# Use notifications efficiently
template '/etc/nginx/nginx.conf' do
  source 'nginx.conf.erb'
  notifies :reload, 'service[nginx]', :delayed
end

# Batch operations
%w[app1 app2 app3].each do |app|
  service app do
    action :nothing
  end
end

execute 'restart all apps' do
  command 'systemctl restart app*'
  action :nothing
  subscribes :run, 'template[/etc/shared/config.yml]', :delayed
end
```

### 3. Search Optimization

```ruby
# Cache search results
class Chef::Recipe::SearchCache
  def self.search_with_cache(type, query)
    @cache ||= {}
    cache_key = "#{type}:#{query}"
    
    @cache[cache_key] ||= search(type, query)
  end
end

# Use partial search for large results
partial_search(:node, 'role:web',
  keys: {
    'name' => ['name'],
    'ip' => ['ipaddress'],
    'port' => ['webapp', 'port']
  }
) do |result|
  # Process each result
end
```

## Monitoring and Observability

### Chef Handler for Metrics

```ruby
# files/default/handlers/metrics_handler.rb
require 'chef/handler'
require 'net/http'

class MetricsHandler < Chef::Handler
  def report
    metrics = {
      success: success?,
      elapsed_time: elapsed_time,
      updated_resources: updated_resources.length,
      node: node.name,
      environment: node.chef_environment,
      run_id: run_id
    }
    
    # Send to monitoring system
    uri = URI('http://metrics.example.com/api/chef')
    http = Net::HTTP.new(uri.host, uri.port)
    request = Net::HTTP::Post.new(uri.path)
    request.content_type = 'application/json'
    request.body = metrics.to_json
    
    http.request(request)
  rescue => e
    Chef::Log.error("Failed to send metrics: #{e.message}")
  end
end

# Install handler
chef_handler 'MetricsHandler' do
  source "#{node['chef_handler']['handler_path']}/metrics_handler.rb"
  action :enable
  supports report: true, exception: true
end
```

### Integration with APM

```ruby
# cookbooks/webapp/recipes/monitoring.rb
# Application Performance Monitoring
package 'datadog-agent'

template '/etc/datadog-agent/datadog.yaml' do
  source 'datadog.yaml.erb'
  variables(
    api_key: Chef::EncryptedDataBagItem.load('monitoring', 'datadog')['api_key'],
    tags: [
      "chef_environment:#{node.chef_environment}",
      "chef_node:#{node.name}",
      "region:#{node['ec2']['region']}"
    ]
  )
  notifies :restart, 'service[datadog-agent]'
end

# Custom Chef metrics
template '/etc/datadog-agent/conf.d/chef.d/conf.yaml' do
  source 'datadog_chef.yaml.erb'
  notifies :restart, 'service[datadog-agent]'
end

service 'datadog-agent' do
  action [:enable, :start]
end
```

## Security Best Practices

### 1. Secrets Management

```ruby
# Use HashiCorp Vault
chef_gem 'vault' do
  compile_time true
end

require 'vault'

# Configure Vault
Vault.configure do |config|
  config.address = node['vault']['address']
  config.token = ENV['VAULT_TOKEN']
  config.ssl_verify = true
end

# Retrieve secrets
db_password = Vault.logical.read('secret/data/database')[:data][:password]

template '/etc/app/database.yml' do
  source 'database.yml.erb'
  variables password: db_password
  sensitive true
end
```

### 2. Compliance and Security Hardening

```ruby
# cookbooks/security/recipes/hardening.rb
# CIS Benchmark implementation

# SSH Hardening
template '/etc/ssh/sshd_config' do
  source 'sshd_config.erb'
  owner 'root'
  group 'root'
  mode '0600'
  variables(
    permit_root_login: 'no',
    password_authentication: 'no',
    x11_forwarding: 'no',
    max_auth_tries: 4,
    client_alive_interval: 300,
    client_alive_count_max: 0
  )
  notifies :restart, 'service[sshd]'
end

# Kernel parameters
sysctl 'network_hardening' do
  key_values(
    'net.ipv4.ip_forward' => 0,
    'net.ipv4.conf.all.accept_source_route' => 0,
    'net.ipv4.conf.all.accept_redirects' => 0,
    'net.ipv4.conf.all.secure_redirects' => 0,
    'net.ipv4.conf.all.log_martians' => 1,
    'net.ipv4.conf.default.log_martians' => 1,
    'net.ipv4.icmp_echo_ignore_broadcasts' => 1,
    'net.ipv4.tcp_syncookies' => 1
  )
end

# File permissions audit
%w[/etc/passwd /etc/shadow /etc/group /etc/gshadow].each do |file|
  file file do
    owner 'root'
    group 'root'
    mode file.include?('shadow') ? '0000' : '0644'
  end
end
```

### 3. Attribute Filtering

```ruby
# Filter sensitive attributes from Chef Server
# /etc/chef/client.rb
automatic_attribute_blacklist = [
  'passwd',
  'shadow',
  'ssh_host_key',
  'ssh_host_rsa_key',
  'ssh_host_dsa_key',
  'credentials'
]

# Cookbook attribute filtering
node.run_state['secret_data'] = 'sensitive_value'  # Won't be saved
node.normal['public_data'] = 'non_sensitive'       # Will be saved
```

## Troubleshooting

### Debug Techniques

```ruby
# Enable debug logging
log 'debug_info' do
  message "Current attributes: #{node['webapp'].to_hash}"
  level :debug
end

# Conditional debugging
ruby_block 'debug_search' do
  block do
    require 'pp'
    results = search(:node, 'role:database')
    pp results
  end
  only_if { ENV['DEBUG'] == 'true' }
end

# Resource inspection
log "Template variables" do
  message lazy { "Variables: #{resources('template[/etc/app.conf]').variables}" }
  level :info
end
```

### Common Issues and Solutions

1. **Dependency Resolution**
```ruby
# Use lazy evaluation
package 'software' do
  version lazy { node['software']['version'] }
end

# Compile-time installation
build_essential 'install' do
  compile_time true
end
```

2. **Notification Timing**
```ruby
# Immediate vs delayed notifications
template '/etc/service.conf' do
  notifies :stop, 'service[app]', :immediately  # Stop immediately
  notifies :start, 'service[app]', :delayed     # Start at end of run
end
```

3. **Resource Cloning**
```ruby
# Avoid resource cloning issues
edit_resource(:service, 'nginx') do
  action [:enable, :start]
  reload_command '/usr/sbin/nginx -s reload'
end
```

## Integration Examples

### GitOps Workflow

```ruby
# Jenkinsfile for Chef cookbook
pipeline {
  agent any
  
  stages {
    stage('Lint') {
      steps {
        sh 'cookstyle -D'
        sh 'foodcritic . -f any'
      }
    }
    
    stage('Unit Tests') {
      steps {
        sh 'chef exec rspec'
      }
    }
    
    stage('Integration Tests') {
      parallel {
        stage('Ubuntu') {
          steps {
            sh 'kitchen test ubuntu'
          }
        }
        stage('CentOS') {
          steps {
            sh 'kitchen test centos'
          }
        }
      }
    }
    
    stage('Upload') {
      when { branch 'main' }
      steps {
        sh 'knife cookbook upload webapp'
      }
    }
  }
}
```

## Conclusion

Chef's policy-based approach to configuration management, combined with its powerful Ruby DSL, makes it an excellent choice for managing complex infrastructure. Its mature ecosystem, extensive testing capabilities, and integration options enable teams to build maintainable, scalable infrastructure automation. By following these patterns and best practices, organizations can leverage Chef to create robust, compliant, and efficient infrastructure management solutions.