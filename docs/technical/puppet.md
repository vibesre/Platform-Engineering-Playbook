# Puppet: Declarative Configuration Management

## Overview

Puppet is a mature, declarative configuration management platform that automates infrastructure provisioning, configuration, and management. Using a domain-specific language (DSL), Puppet enables infrastructure as code practices with a focus on desired state configuration. Its model-driven approach and extensive ecosystem make it ideal for managing large, heterogeneous environments.

## Architecture

### Core Components

```
┌──────────────────────────────────────────────────────────────────┐
│                        Puppet Server                             │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────────────┐  │
│  │  Puppet CA   │  │  PuppetDB   │  │  Puppet Server JRuby  │  │
│  │(Certificate) │  │ (PostgreSQL)│  │    (Compiler)         │  │
│  └──────┬───────┘  └──────┬──────┘  └───────────┬──────────┘  │
│         │                  │                      │             │
│  ┌──────┴──────────────────┴──────────────────────┴──────────┐ │
│  │                    HTTP/HTTPS API (8140)                   │ │
│  └────────────────────────────┬───────────────────────────────┘ │
└──────────────────────────────┼───────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────┴──────┐      ┌─────┴──────┐      ┌─────┴──────┐
    │Puppet Agent│      │Puppet Agent│      │Puppet Agent│
    │   (Node)   │      │   (Node)   │      │   (Node)   │
    │ ┌────────┐ │      │ ┌────────┐ │      │ ┌────────┐ │
    │ │ Facter │ │      │ │ Facter │ │      │ │ Facter │ │
    │ └────────┘ │      │ └────────┘ │      │ └────────┘ │
    │ ┌────────┐ │      │ ┌────────┐ │      │ ┌────────┐ │
    │ │Catalog │ │      │ │Catalog │ │      │ │Catalog │ │
    │ └────────┘ │      │ └────────┘ │      │ └────────┘ │
    └────────────┘      └────────────┘      └────────────┘
```

### Puppet Resource Abstraction Layer

```
┌─────────────────────────────────────────────┐
│           Puppet Manifest (DSL)             │
│                                             │
│  package { 'nginx': ensure => 'present' }  │
│  service { 'nginx': ensure => 'running' }  │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────┴────────────────────────┐
│         Resource Abstraction Layer          │
│                                             │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐│
│  │ Package  │ │ Service  │ │    File     ││
│  │ Provider │ │ Provider │ │  Provider   ││
│  └─────┬────┘ └─────┬────┘ └──────┬──────┘│
└────────┼────────────┼──────────────┼───────┘
         │            │              │
    ┌────┴────┐  ┌────┴────┐   ┌────┴────┐
    │   Yum   │  │ Systemd │   │  POSIX  │
    │   Apt   │  │  Init   │   │Windows  │
    │   Pkg   │  │ Upstart │   │   ACL   │
    └─────────┘  └─────────┘   └─────────┘
```

## Practical Examples

### Basic Manifest Structure

```puppet
# manifests/site.pp
node default {
  include base
  include security
}

node 'web*.example.com' {
  include base
  include security
  include nginx
  include webapp
}

node 'db*.example.com' {
  include base
  include security
  include postgresql
}

# Global resource defaults
Package {
  ensure => 'present',
}

Service {
  ensure => 'running',
  enable => true,
}

File {
  owner => 'root',
  group => 'root',
  mode  => '0644',
}
```

### Module Development

```puppet
# modules/webapp/manifests/init.pp
class webapp (
  String $version           = '2.0.0',
  Integer $port            = 3000,
  String $user             = 'webapp',
  String $group            = 'webapp',
  Stdlib::Absolutepath $install_dir = '/opt/webapp',
  Hash $config             = {},
  Boolean $enable_ssl      = true,
  Boolean $enable_monitoring = true,
) {
  
  # Validate parameters
  assert_type(String[1], $version)
  assert_type(Integer[1024, 65535], $port)
  
  # Include sub-classes
  contain webapp::user
  contain webapp::install
  contain webapp::config
  contain webapp::service
  
  # Define relationships
  Class['webapp::user']
  -> Class['webapp::install']
  -> Class['webapp::config']
  ~> Class['webapp::service']
  
  if $enable_ssl {
    contain webapp::ssl
    Class['webapp::ssl'] -> Class['webapp::service']
  }
  
  if $enable_monitoring {
    contain webapp::monitoring
    Class['webapp::service'] -> Class['webapp::monitoring']
  }
}

# modules/webapp/manifests/user.pp
class webapp::user {
  group { $webapp::group:
    ensure => present,
    system => true,
  }
  
  user { $webapp::user:
    ensure     => present,
    gid        => $webapp::group,
    home       => "/home/${webapp::user}",
    managehome => true,
    shell      => '/bin/bash',
    system     => true,
    require    => Group[$webapp::group],
  }
}

# modules/webapp/manifests/install.pp
class webapp::install {
  $release_url = "https://releases.example.com/webapp/v${webapp::version}/webapp.tar.gz"
  $release_dir = "${webapp::install_dir}/releases/${webapp::version}"
  
  # Create directory structure
  $directories = [
    $webapp::install_dir,
    "${webapp::install_dir}/releases",
    "${webapp::install_dir}/shared",
    "${webapp::install_dir}/shared/config",
    "${webapp::install_dir}/shared/log",
    "${webapp::install_dir}/shared/pids",
  ]
  
  file { $directories:
    ensure => directory,
    owner  => $webapp::user,
    group  => $webapp::group,
    mode   => '0755',
  }
  
  # Download and extract release
  archive { "${release_dir}/webapp.tar.gz":
    ensure       => present,
    source       => $release_url,
    extract      => true,
    extract_path => $release_dir,
    creates      => "${release_dir}/bin/webapp",
    cleanup      => true,
    user         => $webapp::user,
    group        => $webapp::group,
    require      => File[$release_dir],
  }
  
  # Create symlink to current release
  file { "${webapp::install_dir}/current":
    ensure  => link,
    target  => $release_dir,
    owner   => $webapp::user,
    group   => $webapp::group,
    require => Archive["${release_dir}/webapp.tar.gz"],
  }
}

# modules/webapp/manifests/config.pp
class webapp::config {
  $config_file = "${webapp::install_dir}/shared/config/app.yml"
  
  # Merge default config with provided config
  $default_config = {
    'server' => {
      'port' => $webapp::port,
      'host' => '0.0.0.0',
    },
    'database' => {
      'pool' => 5,
      'timeout' => 5000,
    },
    'logging' => {
      'level' => 'info',
      'file' => "${webapp::install_dir}/shared/log/app.log",
    },
  }
  
  $final_config = deep_merge($default_config, $webapp::config)
  
  file { $config_file:
    ensure  => file,
    owner   => $webapp::user,
    group   => $webapp::group,
    mode    => '0640',
    content => to_yaml($final_config),
  }
  
  # Environment file for systemd
  file { '/etc/default/webapp':
    ensure  => file,
    content => epp('webapp/environment.epp', {
      'user'        => $webapp::user,
      'install_dir' => $webapp::install_dir,
      'port'        => $webapp::port,
    }),
  }
}
```

### Advanced Resource Types

```puppet
# modules/webapp/lib/puppet/type/webapp_deployment.rb
Puppet::Type.newtype(:webapp_deployment) do
  @doc = "Manages webapp deployments with zero-downtime"
  
  ensurable do
    defaultvalues
    defaultto :present
    
    newvalue(:deployed) do
      provider.deploy
    end
    
    newvalue(:absent) do
      provider.remove
    end
  end
  
  newparam(:name, :namevar => true) do
    desc "The application name"
  end
  
  newparam(:version) do
    desc "Version to deploy"
    validate do |value|
      unless value =~ /^\d+\.\d+\.\d+$/
        raise ArgumentError, "Version must be in format X.Y.Z"
      end
    end
  end
  
  newparam(:strategy) do
    desc "Deployment strategy"
    newvalues(:rolling, :blue_green, :canary)
    defaultto :rolling
  end
  
  newparam(:health_check) do
    desc "Health check configuration"
    validate do |value|
      unless value.is_a?(Hash)
        raise ArgumentError, "Health check must be a hash"
      end
    end
  end
  
  autorequire(:file) do
    ["/opt/#{self[:name]}"]
  end
  
  autorequire(:service) do
    ["#{self[:name]}"]
  end
end

# modules/webapp/lib/puppet/provider/webapp_deployment/default.rb
Puppet::Type.type(:webapp_deployment).provide(:default) do
  desc "Default provider for webapp deployment"
  
  def exists?
    File.exist?("/opt/#{resource[:name]}/current")
  end
  
  def deploy
    case resource[:strategy]
    when :blue_green
      deploy_blue_green
    when :canary
      deploy_canary
    else
      deploy_rolling
    end
  end
  
  def deploy_blue_green
    inactive = get_inactive_color
    
    # Deploy to inactive environment
    deploy_to_environment(inactive)
    
    # Health check
    if health_check_passes?(inactive)
      # Switch active environment
      switch_environment(inactive)
    else
      raise Puppet::Error, "Health check failed for #{inactive} environment"
    end
  end
  
  private
  
  def get_inactive_color
    current = File.read('/etc/webapp/active_env').strip rescue 'blue'
    current == 'blue' ? 'green' : 'blue'
  end
  
  def health_check_passes?(env)
    config = resource[:health_check] || {}
    endpoint = config['endpoint'] || '/health'
    port = env == 'blue' ? 3000 : 3001
    retries = config['retries'] || 30
    
    retries.times do
      begin
        response = Net::HTTP.get_response(URI("http://localhost:#{port}#{endpoint}"))
        return true if response.code == '200'
      rescue
        sleep 2
      end
    end
    false
  end
end
```

### Hiera Data Management

```yaml
# hiera.yaml
---
version: 5
defaults:
  datadir: data
  data_hash: yaml_data

hierarchy:
  - name: "Per-node data"
    path: "nodes/%{facts.networking.fqdn}.yaml"
  
  - name: "Per-environment data"
    path: "environments/%{environment}.yaml"
  
  - name: "Per-OS data"
    paths:
      - "os/%{facts.os.name}/%{facts.os.release.major}.yaml"
      - "os/%{facts.os.name}.yaml"
      - "os/%{facts.os.family}.yaml"
  
  - name: "Per-datacenter data"
    path: "datacenters/%{facts.datacenter}.yaml"
  
  - name: "Common data"
    path: "common.yaml"
  
  - name: "Encrypted data"
    lookup_key: eyaml_lookup_key
    paths:
      - "secrets/%{environment}.eyaml"
      - "secrets/common.eyaml"
    options:
      pkcs7_private_key: /etc/puppetlabs/puppet/keys/private_key.pkcs7.pem
      pkcs7_public_key: /etc/puppetlabs/puppet/keys/public_key.pkcs7.pem
```

```yaml
# data/environments/production.yaml
---
webapp::version: '2.1.0'
webapp::port: 3000
webapp::config:
  database:
    host: 'db-prod.example.com'
    port: 5432
    name: 'webapp_production'
  cache:
    host: 'redis-prod.example.com'
    port: 6379
  
nginx::worker_processes: 'auto'
nginx::worker_connections: 2048

monitoring::enabled: true
monitoring::endpoints:
  - 'prometheus-1.example.com'
  - 'prometheus-2.example.com'
```

### Complex Orchestration

```puppet
# modules/orchestration/plans/rolling_update.pp
plan orchestration::rolling_update (
  TargetSpec $targets,
  String[1] $version,
  Integer $batch_size = 1,
  Integer $batch_delay = 60,
) {
  # Get all target nodes
  $nodes = get_targets($targets)
  
  # Divide into batches
  $batches = $nodes.slice($batch_size)
  
  $batches.each |$index, $batch| {
    # Remove from load balancer
    $batch.each |$node| {
      run_task('haproxy::server', $loadbalancers, 
        server => $node.name,
        backend => 'web-backend',
        action => 'disable'
      )
    }
    
    # Deploy to batch
    apply($batch) {
      class { 'webapp':
        version => $version,
      }
    }
    
    # Health check
    $health_results = run_task('webapp::health_check', $batch)
    $failed = $health_results.filter |$result| { !$result.ok }
    
    if $failed.empty {
      # Add back to load balancer
      $batch.each |$node| {
        run_task('haproxy::server', $loadbalancers,
          server => $node.name,
          backend => 'web-backend', 
          action => 'enable'
        )
      }
      
      # Wait before next batch
      if $index < $batches.length - 1 {
        ctrl::sleep($batch_delay)
      }
    } else {
      fail("Health check failed on nodes: ${failed.map |$r| { $r.target.name }.join(', ')}")
    }
  }
  
  return "Successfully updated ${nodes.length} nodes to version ${version}"
}
```

## Best Practices

### 1. Module Structure

```bash
# Standard module layout
webapp/
├── data/
│   └── common.yaml
├── examples/
│   └── init.pp
├── files/
│   └── scripts/
├── lib/
│   ├── facter/
│   └── puppet/
│       ├── functions/
│       ├── provider/
│       └── type/
├── manifests/
│   ├── init.pp
│   ├── config.pp
│   ├── install.pp
│   └── service.pp
├── spec/
│   ├── classes/
│   ├── defines/
│   └── spec_helper.rb
├── tasks/
│   └── health_check.json
├── templates/
│   └── config.epp
├── Gemfile
├── Rakefile
├── metadata.json
└── README.md
```

### 2. Testing with RSpec

```ruby
# spec/classes/webapp_spec.rb
require 'spec_helper'

describe 'webapp' do
  on_supported_os.each do |os, os_facts|
    context "on #{os}" do
      let(:facts) { os_facts }
      
      context 'with default parameters' do
        it { is_expected.to compile }
        
        it { is_expected.to contain_class('webapp::user') }
        it { is_expected.to contain_class('webapp::install') }
        it { is_expected.to contain_class('webapp::config') }
        it { is_expected.to contain_class('webapp::service') }
        
        it { is_expected.to contain_user('webapp').with(
          'ensure' => 'present',
          'system' => true,
          'home'   => '/home/webapp'
        )}
        
        it { is_expected.to contain_file('/opt/webapp').with(
          'ensure' => 'directory',
          'owner'  => 'webapp',
          'group'  => 'webapp'
        )}
        
        it { is_expected.to contain_service('webapp').with(
          'ensure' => 'running',
          'enable' => true
        )}
      end
      
      context 'with custom parameters' do
        let(:params) {{
          'version' => '3.0.0',
          'port'    => 8080,
          'enable_ssl' => false
        }}
        
        it { is_expected.not_to contain_class('webapp::ssl') }
        
        it { is_expected.to contain_file('/etc/default/webapp').with_content(
          /PORT=8080/
        )}
      end
      
      context 'with invalid parameters' do
        let(:params) {{ 'port' => 'invalid' }}
        
        it { is_expected.to raise_error(Puppet::Error) }
      end
    end
  end
end
```

### 3. Acceptance Testing

```ruby
# spec/acceptance/webapp_spec.rb
require 'spec_helper_acceptance'

describe 'webapp class' do
  context 'default parameters' do
    it 'should apply without errors' do
      pp = <<-EOS
        class { 'webapp':
          version => '2.0.0',
        }
      EOS
      
      apply_manifest(pp, :catch_failures => true)
      apply_manifest(pp, :catch_changes => true)
    end
    
    describe package('webapp') do
      it { should be_installed }
    end
    
    describe service('webapp') do
      it { should be_enabled }
      it { should be_running }
    end
    
    describe port(3000) do
      it { should be_listening }
    end
    
    describe command('curl -s http://localhost:3000/health') do
      its(:exit_status) { should eq 0 }
      its(:stdout) { should match /OK/ }
    end
  end
  
  context 'upgrade scenario' do
    it 'should upgrade successfully' do
      # Initial deployment
      apply_manifest("class { 'webapp': version => '1.0.0' }", :catch_failures => true)
      
      # Upgrade
      apply_manifest("class { 'webapp': version => '2.0.0' }", :catch_failures => true)
      
      # Verify upgrade
      describe file('/opt/webapp/current') do
        it { should be_symlink }
        it { should be_linked_to '/opt/webapp/releases/2.0.0' }
      end
    end
  end
end
```

### 4. Custom Functions

```ruby
# lib/puppet/functions/webapp/generate_config.rb
Puppet::Functions.create_function(:'webapp::generate_config') do
  dispatch :generate_config do
    param 'Hash', :base_config
    param 'String', :environment
    return_type 'Hash'
  end
  
  def generate_config(base_config, environment)
    config = base_config.dup
    
    # Environment-specific modifications
    case environment
    when 'production'
      config['server']['workers'] = facts['processors']['count'] * 2
      config['logging']['level'] = 'warn'
      config['cache']['enabled'] = true
    when 'development'
      config['server']['workers'] = 1
      config['logging']['level'] = 'debug'
      config['cache']['enabled'] = false
    end
    
    # Add computed values
    config['server']['max_connections'] = config['server']['workers'] * 1000
    config['database']['pool_size'] = config['server']['workers'] * 5
    
    config
  end
end
```

## Production Deployment Patterns

### 1. Puppet Enterprise Architecture

```puppet
# manifests/pe_infrastructure.pp
class profile::puppet::master {
  class { 'puppet_enterprise::profile::master':
    r10k_remote => 'https://github.com/company/control-repo.git',
    code_manager_auto_configure => true,
  }
  
  # Configure PuppetDB
  class { 'puppet_enterprise::profile::puppetdb':
    database_host => 'postgresql.example.com',
    database_name => 'puppetdb',
    database_user => 'puppetdb',
    database_password => lookup('puppetdb::database_password'),
  }
  
  # Configure console
  class { 'puppet_enterprise::profile::console':
    console_services_api_ssl_cert => '/etc/puppetlabs/puppet/ssl/certs/console.pem',
    console_services_api_ssl_key => '/etc/puppetlabs/puppet/ssl/private_keys/console.pem',
  }
  
  # High availability configuration
  if $facts['pe_ha_enabled'] {
    class { 'puppet_enterprise::profile::master::ha':
      ha_pool => ['puppet-master-1', 'puppet-master-2'],
      shared_storage => '/shared/puppet',
    }
  }
}
```

### 2. Code Deployment with R10k

```yaml
# Puppetfile
forge "https://forge.puppetlabs.com"

# Puppet modules from the Puppet Forge
mod 'puppetlabs/stdlib', '8.5.0'
mod 'puppetlabs/concat', '7.3.0'
mod 'puppetlabs/firewall', '3.5.0'
mod 'puppetlabs/postgresql', '8.2.0'
mod 'puppet/nginx', '3.3.0'
mod 'puppet/redis', '8.5.0'

# Internal modules
mod 'webapp',
  :git => 'https://github.com/company/puppet-webapp.git',
  :tag => 'v2.1.0'

mod 'monitoring',
  :git => 'https://github.com/company/puppet-monitoring.git',
  :branch => 'production'

# External modules
mod 'prometheus',
  :git => 'https://github.com/voxpupuli/puppet-prometheus.git',
  :tag => 'v12.0.0'
```

```yaml
# r10k.yaml
---
cachedir: '/var/cache/r10k'
sources:
  puppet:
    remote: 'https://github.com/company/control-repo.git'
    basedir: '/etc/puppetlabs/code/environments'
    prefix: false

deploy:
  purge_levels: ['deployment', 'environment', 'puppetfile']
  
git:
  provider: rugged
  private_key: '/root/.ssh/r10k_rsa'
  
forge:
  baseurl: 'https://forgeapi.puppetlabs.com'
```

### 3. Bolt Orchestration

```puppet
# Boltdir/site-modules/deployment/plans/canary.pp
plan deployment::canary (
  String[1] $application,
  String[1] $version,
  TargetSpec $production_targets,
  Integer $canary_percentage = 10,
  Integer $validation_time = 300,
) {
  # Calculate canary size
  $all_targets = get_targets($production_targets)
  $canary_count = ceiling($all_targets.length * $canary_percentage / 100.0)
  $canary_targets = $all_targets.take($canary_count)
  $remaining_targets = $all_targets - $canary_targets
  
  # Deploy to canary
  out::message("Deploying to ${canary_count} canary nodes")
  $canary_results = run_plan('deployment::update', $canary_targets,
    application => $application,
    version => $version
  )
  
  # Monitor canary
  out::message("Monitoring canary deployment for ${validation_time} seconds")
  $start_time = timestamp()
  
  ctrl::do_until() || {
    $elapsed = timestamp() - $start_time
    
    if $elapsed >= $validation_time {
      true
    } else {
      # Check metrics
      $metrics = run_task('monitoring::get_metrics', 'localhost',
        nodes => $canary_targets.map |$t| { $t.name },
        metrics => ['error_rate', 'response_time', 'cpu_usage']
      )
      
      $issues = $metrics.filter |$m| {
        $m['error_rate'] > 0.05 || $m['response_time'] > 1000
      }
      
      if !$issues.empty {
        fail_plan("Canary validation failed: ${issues}")
      }
      
      ctrl::sleep(30)
      false
    }
  }
  
  # Deploy to remaining nodes
  out::message("Canary successful, deploying to remaining ${remaining_targets.length} nodes")
  run_plan('deployment::rolling_update', $remaining_targets,
    application => $application,
    version => $version,
    batch_size => 10
  )
}
```

### 4. Multi-Environment Pipeline

```puppet
# modules/profile/manifests/cd_pipeline.pp
class profile::cd_pipeline {
  $environments = ['development', 'staging', 'production']
  
  # Jenkins pipeline job
  jenkins::job { 'puppet-deployment':
    config => epp('profile/jenkins/puppet_deployment.xml.epp', {
      environments => $environments,
      puppet_server => 'puppet.example.com',
      r10k_key => '/var/lib/jenkins/.ssh/r10k_deploy',
    }),
  }
  
  # GitLab webhook for r10k
  gitlab_project_hook { 'control-repo':
    project => 'infrastructure/control-repo',
    url => 'https://puppet.example.com:8088/code-manager/v1/webhook',
    token => lookup('code_manager::webhook_token'),
    push_events => true,
    tag_push_events => true,
  }
  
  # Automated testing for each environment
  $environments.each |$env| {
    cron { "puppet-test-${env}":
      command => "/opt/puppetlabs/puppet/bin/puppet apply --environment=${env} --noop --summarize | /usr/local/bin/puppet-report",
      hour => '*/4',
      minute => fqdn_rand(60),
    }
  }
}
```

## Performance Optimization

### 1. Server Tuning

```puppet
# manifests/puppet_server_tuning.pp
class profile::puppet::server::tuning {
  # JRuby configuration
  ini_setting { 'puppet_server_jruby_instances':
    ensure  => present,
    path    => '/etc/puppetlabs/puppetserver/conf.d/puppetserver.conf',
    section => 'jruby-puppet',
    setting => 'max-active-instances',
    value   => $facts['processors']['count'] * 2,
  }
  
  # Memory settings
  $total_memory = $facts['memory']['system']['total_bytes']
  $heap_size = $total_memory * 0.7
  
  file { '/etc/default/puppetserver':
    ensure  => file,
    content => epp('profile/puppetserver/default.epp', {
      heap_size => $heap_size,
      max_heap_size => $heap_size,
      reserved_code_cache => '512m',
    }),
    notify  => Service['puppetserver'],
  }
  
  # Enable HTTP caching
  puppet_authorization::rule { 'static_file_cache':
    match_request_path => '^/puppet/v3/file_(metadata|content)/modules/',
    match_request_type => 'regex',
    allow => ['*'],
    sort_order => 500,
    path => '/etc/puppetlabs/puppetserver/conf.d/auth.conf',
  }
}
```

### 2. Catalog Compilation Optimization

```puppet
# modules/profile/manifests/base_optimized.pp
class profile::base_optimized {
  # Use virtual resources to reduce catalog size
  @user { 'app_users':
    ['web_user', 'db_user', 'cache_user'].each |$user| {
      user { $user:
        ensure => present,
        system => true,
        tag => 'app_user',
      }
    }
  }
  
  # Realize only needed users
  User <| tag == 'app_user' and title == $needed_user |>
  
  # Use defined types for repeated patterns
  $packages = lookup('base_packages', Array[String], 'unique')
  ensure_packages($packages, {
    'ensure' => 'present',
    'install_options' => ['--quiet'],
  })
  
  # Optimize file resources
  $config_files = {
    '/etc/motd' => 'profile/motd.epp',
    '/etc/issue' => 'profile/issue.epp',
  }
  
  $config_files.each |$path, $template| {
    file { $path:
      ensure  => file,
      content => epp($template),
      *       => $file_defaults,  # Splat common attributes
    }
  }
}
```

### 3. PuppetDB Query Optimization

```puppet
# lib/puppet/functions/optimized_query.rb
Puppet::Functions.create_function(:optimized_query) do
  dispatch :query_nodes do
    param 'String', :query
    param 'Hash', :options
  end
  
  def query_nodes(query, options)
    # Cache results
    cache_key = "#{query}_#{options.hash}"
    cache_file = "/var/cache/puppet/queries/#{cache_key}"
    
    if File.exist?(cache_file) && (Time.now - File.mtime(cache_file)) < 3600
      return JSON.parse(File.read(cache_file))
    end
    
    # Perform query with specific fields
    fields = options['fields'] || ['certname', 'ipaddress']
    
    results = call_function('puppetdb_query', [
      "nodes[#{fields.join(',')}]{ #{query} }"
    ])
    
    # Cache results
    FileUtils.mkdir_p(File.dirname(cache_file))
    File.write(cache_file, results.to_json)
    
    results
  end
end
```

## Monitoring and Observability

### Puppet Metrics Collection

```puppet
# modules/puppet_metrics/manifests/init.pp
class puppet_metrics (
  String $graphite_host = 'metrics.example.com',
  Integer $graphite_port = 2003,
) {
  # Puppet Server metrics
  ini_setting { 'metrics_enabled':
    ensure  => present,
    path    => '/etc/puppetlabs/puppetserver/conf.d/metrics.conf',
    section => 'metrics',
    setting => 'enabled',
    value   => true,
  }
  
  # Graphite reporter
  file { '/etc/puppetlabs/puppetserver/conf.d/graphite-reporter.conf':
    ensure  => file,
    content => epp('puppet_metrics/graphite-reporter.conf.epp', {
      host => $graphite_host,
      port => $graphite_port,
      prefix => "puppet.${facts['networking']['fqdn']}",
    }),
    notify  => Service['puppetserver'],
  }
  
  # Agent run metrics
  file { '/etc/puppetlabs/puppet/last_run_report.yaml':
    ensure => file,
    mode   => '0644',
  }
  
  # Metrics collection script
  file { '/usr/local/bin/puppet-metrics-collector':
    ensure  => file,
    mode    => '0755',
    content => epp('puppet_metrics/collector.sh.epp'),
  }
  
  cron { 'collect_puppet_metrics':
    command => '/usr/local/bin/puppet-metrics-collector',
    minute  => '*/5',
  }
}
```

### Puppet Report Processor

```ruby
# lib/puppet/reports/monitoring.rb
require 'puppet'
require 'net/http'
require 'json'

Puppet::Reports.register_report(:monitoring) do
  desc "Send Puppet reports to monitoring system"
  
  def process
    # Extract metrics
    metrics = {
      'host' => self.host,
      'environment' => self.environment,
      'status' => self.status,
      'time' => self.time,
      'runtime' => self.metrics['time']['values'].find { |x| x[0] == 'total' }[2],
      'resources' => {
        'total' => self.metrics['resources']['values'].find { |x| x[0] == 'total' }[2],
        'changed' => self.metrics['resources']['values'].find { |x| x[0] == 'changed' }[2],
        'failed' => self.metrics['resources']['values'].find { |x| x[0] == 'failed' }[2],
      },
      'events' => self.metrics['events']['values'].find { |x| x[0] == 'total' }[2],
    }
    
    # Add logs for failures
    if self.status == 'failed'
      metrics['failures'] = self.logs.select { |log| log.level == :err }.map do |log|
        {
          'resource' => log.source,
          'message' => log.message,
        }
      end
    end
    
    # Send to monitoring API
    uri = URI("http://#{Puppet[:monitoring_host]}/api/puppet/reports")
    http = Net::HTTP.new(uri.host, uri.port)
    request = Net::HTTP::Post.new(uri.path, 'Content-Type' => 'application/json')
    request.body = metrics.to_json
    
    response = http.request(request)
    
    if response.code != '200'
      Puppet.err "Failed to send report: #{response.body}"
    end
  rescue => e
    Puppet.err "Report processor error: #{e.message}"
  end
end
```

## Security Best Practices

### 1. Certificate Management

```puppet
# modules/puppet_security/manifests/certificates.pp
class puppet_security::certificates {
  # Automatic certificate signing rules
  file { '/etc/puppetlabs/puppet/autosign.conf':
    ensure  => file,
    owner   => 'puppet',
    group   => 'puppet',
    mode    => '0644',
    content => epp('puppet_security/autosign.conf.epp', {
      allowed_domains => lookup('puppet::autosign::domains', Array, 'unique', []),
      policy_based => true,
    }),
  }
  
  # Policy-based autosigning
  file { '/etc/puppetlabs/puppet/autosign.rb':
    ensure  => file,
    owner   => 'puppet',
    group   => 'puppet',
    mode    => '0755',
    content => epp('puppet_security/autosign.rb.epp'),
  }
  
  ini_setting { 'autosign_policy':
    ensure  => present,
    path    => '/etc/puppetlabs/puppet/puppet.conf',
    section => 'master',
    setting => 'autosign',
    value   => '/etc/puppetlabs/puppet/autosign.rb',
  }
  
  # Certificate expiration monitoring
  cron { 'check_cert_expiration':
    command => '/opt/puppetlabs/puppet/bin/puppet cert list --all | /usr/local/bin/cert-expiry-check',
    hour    => '0',
    minute  => '0',
  }
}
```

### 2. RBAC Configuration

```puppet
# modules/puppet_security/manifests/rbac.pp
class puppet_security::rbac {
  # Create roles
  rbac_role { 'developers':
    ensure => present,
    permissions => [
      {
        'object_type' => 'nodes',
        'action' => 'view_data',
        'instance' => '*',
      },
      {
        'object_type' => 'environment',
        'action' => 'deploy_code',
        'instance' => ['development', 'staging'],
      },
    ],
  }
  
  rbac_role { 'operators':
    ensure => present,
    permissions => [
      {
        'object_type' => 'nodes',
        'action' => ['view_data', 'edit_data', 'run'],
        'instance' => '*',
      },
      {
        'object_type' => 'tasks',
        'action' => 'run',
        'instance' => '*',
      },
    ],
  }
  
  # Create users and assign roles
  $users = lookup('puppet::rbac::users', Hash, 'hash')
  $users.each |$username, $config| {
    rbac_user { $username:
      ensure => present,
      email => $config['email'],
      display_name => $config['display_name'],
      roles => $config['roles'],
    }
  }
}
```

### 3. Secure Secrets Management

```puppet
# Using eyaml for secrets
class secure::secrets {
  $db_password = lookup('database::password') # Automatically decrypted from eyaml
  
  file { '/etc/app/database.conf':
    ensure => file,
    owner => 'app',
    group => 'app',
    mode => '0600',
    content => epp('secure/database.conf.epp', {
      password => $db_password,
    }),
    show_diff => false,  # Don't show passwords in logs
  }
  
  # Vault integration
  $vault_secret = vault_lookup('secret/app/api_key')
  
  file { '/etc/app/api.conf':
    ensure => file,
    owner => 'app',
    group => 'app', 
    mode => '0600',
    content => "API_KEY=${vault_secret}\n",
    show_diff => false,
  }
}
```

## Troubleshooting

### Debug Techniques

```puppet
# Debug manifest
class debug_example {
  # Notice level logging
  notice("Processing node: ${facts['networking']['fqdn']}")
  
  # Debug with structured facts
  $debug_info = {
    'node' => $facts['networking']['fqdn'],
    'environment' => $environment,
    'classes' => $classes,
  }
  notify { 'debug_output':
    message => inline_epp('<%= $debug_info.to_yaml %>', { debug_info => $debug_info }),
  }
  
  # Conditional debugging
  if $facts['kernel'] == 'Linux' {
    exec { 'debug_system_info':
      command => '/usr/bin/env > /tmp/puppet_debug.txt',
      creates => '/tmp/puppet_debug.txt',
    }
  }
}
```

### Common Issues and Solutions

1. **Catalog Compilation Failures**
```bash
# Test catalog compilation
puppet apply --noop --environment=production -e "include role::webserver"

# Debug catalog compilation
puppet master --compile node.example.com --environment=production
```

2. **Certificate Issues**
```bash
# Clean certificate
puppet cert clean node.example.com

# Regenerate certificate on node
rm -rf /etc/puppetlabs/puppet/ssl
puppet agent -t
```

3. **PuppetDB Connection**
```bash
# Test PuppetDB connection
puppet query 'nodes {}'

# Check PuppetDB status
curl -X GET http://localhost:8080/pdb/meta/v1/version
```

## Integration Examples

### CI/CD Pipeline Integration

```groovy
// Jenkinsfile for Puppet deployment
pipeline {
  agent any
  
  environment {
    PUPPET_SERVER = 'puppet.example.com'
    R10K_DEPLOY_KEY = credentials('r10k-deploy-key')
  }
  
  stages {
    stage('Validate') {
      steps {
        sh '''
          # Validate Puppet manifests
          find . -name "*.pp" -exec puppet parser validate {} \\;
          
          # Validate templates
          find . -name "*.epp" -exec puppet epp validate {} \\;
          
          # Lint checking
          puppet-lint --no-autoloader_layout-check .
        '''
      }
    }
    
    stage('Test') {
      parallel {
        stage('Spec Tests') {
          steps {
            sh 'bundle exec rake spec'
          }
        }
        
        stage('Acceptance Tests') {
          steps {
            sh 'bundle exec rake beaker:suites'
          }
        }
      }
    }
    
    stage('Deploy to Dev') {
      when { branch 'develop' }
      steps {
        sh '''
          ssh -i $R10K_DEPLOY_KEY puppet@$PUPPET_SERVER \\
            "r10k deploy environment development -pv"
        '''
      }
    }
    
    stage('Deploy to Prod') {
      when { branch 'main' }
      input { message 'Deploy to production?' }
      steps {
        sh '''
          ssh -i $R10K_DEPLOY_KEY puppet@$PUPPET_SERVER \\
            "r10k deploy environment production -pv"
        '''
      }
    }
  }
  
  post {
    always {
      junit 'spec/reports/*.xml'
      publishHTML([
        reportDir: 'coverage',
        reportFiles: 'index.html',
        reportName: 'Coverage Report'
      ])
    }
  }
}
```

## Conclusion

Puppet's mature ecosystem, declarative approach, and powerful abstractions make it an excellent choice for managing complex infrastructure at scale. Its strong typing, extensive testing capabilities, and enterprise features enable teams to build reliable, maintainable infrastructure as code. By following these patterns and leveraging Puppet's rich feature set, organizations can achieve consistent, policy-driven infrastructure management across diverse environments.