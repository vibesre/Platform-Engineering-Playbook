# Ansible: Agentless Automation and Configuration Management

## Overview

Ansible is an open-source automation platform that provides configuration management, application deployment, and task automation. Its agentless architecture and human-readable YAML syntax make it one of the most popular automation tools in modern infrastructure.

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Control Node                            │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Ansible   │  │  Inventory   │  │    Playbooks    │  │
│  │    Core     │  │   Manager    │  │   & Modules     │  │
│  └──────┬──────┘  └──────┬───────┘  └────────┬────────┘  │
│         │                 │                    │           │
│  ┌──────┴─────────────────┴────────────────────┴────────┐ │
│  │              Connection Plugins (SSH/WinRM)           │ │
│  └──────────────────────┬───────────────────────────────┘ │
└─────────────────────────┼───────────────────────────────────┘
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
┌───┴────┐          ┌─────┴────┐          ┌────┴─────┐
│ Node 1 │          │  Node 2  │          │  Node 3  │
│ Linux  │          │ Windows  │          │  Linux   │
└────────┘          └──────────┘          └──────────┘
```

### Key Architectural Principles

1. **Agentless**: No software required on managed nodes
2. **Push-Based**: Control node pushes configurations
3. **Idempotent**: Operations are safe to run multiple times
4. **Declarative**: Describe desired state, not steps

## Practical Examples

### Basic Playbook Structure

```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  vars:
    nginx_version: "1.20.*"
    app_port: 3000
  
  tasks:
    - name: Install Nginx
      package:
        name: "nginx={{ nginx_version }}"
        state: present
      
    - name: Configure Nginx
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: restart nginx
    
    - name: Start and enable Nginx
      service:
        name: nginx
        state: started
        enabled: yes
  
  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
```

### Advanced Role Structure

```yaml
# roles/webapp/tasks/main.yml
---
- name: Include OS-specific variables
  include_vars: "{{ ansible_os_family }}.yml"

- name: Install dependencies
  package:
    name: "{{ item }}"
    state: present
  loop: "{{ webapp_dependencies }}"

- name: Create application user
  user:
    name: "{{ app_user }}"
    system: yes
    shell: /bin/false
    home: "{{ app_home }}"
    create_home: yes

- name: Deploy application
  include_tasks: deploy.yml
  tags: [deploy]

- name: Configure monitoring
  include_tasks: monitoring.yml
  when: monitoring_enabled | default(false)
```

### Dynamic Inventory Script

```python
#!/usr/bin/env python3
import json
import boto3

def get_inventory():
    ec2 = boto3.client('ec2')
    
    inventory = {
        '_meta': {
            'hostvars': {}
        },
        'all': {
            'children': ['aws']
        },
        'aws': {
            'children': ['web', 'db', 'app']
        }
    }
    
    # Get all running instances
    response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            hostname = instance['PublicDnsName']
            instance_id = instance['InstanceId']
            
            # Get tags
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            
            # Add to appropriate groups
            if 'Role' in tags:
                role = tags['Role']
                if role not in inventory:
                    inventory[role] = {'hosts': []}
                inventory[role]['hosts'].append(hostname)
            
            # Add host variables
            inventory['_meta']['hostvars'][hostname] = {
                'ansible_host': instance['PublicIpAddress'],
                'instance_id': instance_id,
                'instance_type': instance['InstanceType'],
                'tags': tags
            }
    
    return inventory

if __name__ == '__main__':
    print(json.dumps(get_inventory(), indent=2))
```

### Complex Deployment Playbook

```yaml
---
- name: Deploy microservices application
  hosts: all
  gather_facts: yes
  
  vars:
    deployment_version: "{{ lookup('env', 'BUILD_VERSION') | default('latest') }}"
    healthcheck_retries: 30
    healthcheck_delay: 10
  
  tasks:
    - name: Pre-deployment health check
      uri:
        url: "http://{{ inventory_hostname }}:{{ app_port }}/health"
        status_code: 200
      register: health_check
      failed_when: false
      changed_when: false
    
    - name: Take node out of load balancer
      uri:
        url: "http://{{ lb_api_endpoint }}/nodes/{{ inventory_hostname }}"
        method: DELETE
      delegate_to: localhost
      when: health_check.status == 200
    
    - name: Stop application
      systemd:
        name: "{{ app_service_name }}"
        state: stopped
      when: health_check.status == 200
    
    - name: Backup current version
      archive:
        path: "{{ app_directory }}"
        dest: "/backup/{{ app_name }}-{{ ansible_date_time.epoch }}.tar.gz"
      when: health_check.status == 200
    
    - name: Deploy new version
      unarchive:
        src: "{{ artifact_url }}/{{ app_name }}-{{ deployment_version }}.tar.gz"
        dest: "{{ app_directory }}"
        remote_src: yes
        owner: "{{ app_user }}"
        group: "{{ app_group }}"
    
    - name: Update configuration
      template:
        src: "config/{{ item }}.j2"
        dest: "{{ app_directory }}/config/{{ item }}"
        owner: "{{ app_user }}"
        group: "{{ app_group }}"
        mode: '0640'
      loop:
        - app.yml
        - database.yml
        - redis.yml
    
    - name: Run database migrations
      command: "{{ app_directory }}/bin/migrate"
      environment:
        DATABASE_URL: "{{ database_url }}"
      run_once: true
      delegate_to: "{{ groups['app'][0] }}"
    
    - name: Start application
      systemd:
        name: "{{ app_service_name }}"
        state: started
        daemon_reload: yes
    
    - name: Wait for application to be healthy
      uri:
        url: "http://{{ inventory_hostname }}:{{ app_port }}/health"
        status_code: 200
      register: result
      until: result.status == 200
      retries: "{{ healthcheck_retries }}"
      delay: "{{ healthcheck_delay }}"
    
    - name: Add node back to load balancer
      uri:
        url: "http://{{ lb_api_endpoint }}/nodes"
        method: POST
        body_format: json
        body:
          hostname: "{{ inventory_hostname }}"
          port: "{{ app_port }}"
      delegate_to: localhost
    
    - name: Verify deployment
      uri:
        url: "http://{{ inventory_hostname }}:{{ app_port }}/version"
      register: version_check
      failed_when: deployment_version not in version_check.content
```

## Best Practices

### 1. Inventory Management

```ini
# production/inventory
[web]
web1.example.com ansible_host=10.0.1.10
web2.example.com ansible_host=10.0.1.11

[db]
db1.example.com ansible_host=10.0.2.10 role=master
db2.example.com ansible_host=10.0.2.11 role=replica

[web:vars]
nginx_worker_processes=auto
nginx_worker_connections=1024

[db:vars]
postgresql_version=14
postgresql_max_connections=200
```

### 2. Vault for Secrets

```bash
# Encrypt sensitive data
ansible-vault encrypt_string 'supersecret' --name 'db_password'

# Use in playbooks
---
- name: Configure database
  hosts: db
  vars_files:
    - vault/production.yml
  
  tasks:
    - name: Set database password
      postgresql_user:
        name: "{{ db_user }}"
        password: "{{ db_password }}"
```

### 3. Testing with Molecule

```yaml
# molecule/default/molecule.yml
---
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: ubuntu-20
    image: ubuntu:20.04
    pre_build_image: true
  - name: centos-8
    image: centos:8
    pre_build_image: true
provisioner:
  name: ansible
  inventory:
    host_vars:
      ubuntu-20:
        ansible_python_interpreter: /usr/bin/python3
verifier:
  name: ansible
```

### 4. Error Handling

```yaml
- name: Robust task execution
  block:
    - name: Risky operation
      command: /opt/app/deploy.sh
      register: deploy_result
      
    - name: Verify deployment
      uri:
        url: "http://localhost:8080/health"
      register: health_check
      
  rescue:
    - name: Rollback on failure
      command: /opt/app/rollback.sh
      
    - name: Send alert
      mail:
        to: ops@example.com
        subject: "Deployment failed on {{ inventory_hostname }}"
        body: "Error: {{ ansible_failed_result.msg }}"
      
  always:
    - name: Clean up temporary files
      file:
        path: /tmp/deployment
        state: absent
```

## Production Deployment Patterns

### 1. Blue-Green Deployment

```yaml
---
- name: Blue-Green Deployment
  hosts: localhost
  vars:
    active_color: "{{ lookup('file', '/etc/active_color') }}"
    new_color: "{{ 'green' if active_color == 'blue' else 'blue' }}"
  
  tasks:
    - name: Deploy to inactive environment
      include_role:
        name: deploy_app
      vars:
        target_env: "{{ new_color }}"
        app_version: "{{ deployment_version }}"
    
    - name: Run smoke tests
      uri:
        url: "http://{{ new_color }}.internal.example.com/health"
        status_code: 200
      retries: 5
      delay: 10
    
    - name: Switch load balancer
      uri:
        url: "http://lb.example.com/api/backend"
        method: PUT
        body_format: json
        body:
          backend: "{{ new_color }}"
    
    - name: Update active color
      copy:
        content: "{{ new_color }}"
        dest: /etc/active_color
```

### 2. Rolling Updates

```yaml
---
- name: Rolling update with serial execution
  hosts: webservers
  serial: 
    - 1
    - 25%
    - 50%
    - 100%
  max_fail_percentage: 20
  
  pre_tasks:
    - name: Remove from load balancer
      haproxy:
        state: disabled
        backend: web-backend
        host: "{{ inventory_hostname }}"
        socket: /var/lib/haproxy/stats
      delegate_to: "{{ item }}"
      loop: "{{ groups['loadbalancers'] }}"
  
  roles:
    - update_application
  
  post_tasks:
    - name: Add back to load balancer
      haproxy:
        state: enabled
        backend: web-backend
        host: "{{ inventory_hostname }}"
        socket: /var/lib/haproxy/stats
      delegate_to: "{{ item }}"
      loop: "{{ groups['loadbalancers'] }}"
```

### 3. GitOps Integration

```yaml
# ansible-pull configuration
---
- name: Configure ansible-pull
  hosts: all
  tasks:
    - name: Install ansible and git
      package:
        name:
          - ansible
          - git
        state: present
    
    - name: Create ansible-pull script
      copy:
        dest: /usr/local/bin/ansible-pull-update
        mode: '0755'
        content: |
          #!/bin/bash
          ansible-pull \
            -U https://github.com/company/infrastructure.git \
            -C {{ git_branch | default('main') }} \
            -i localhost, \
            playbooks/self-update.yml
    
    - name: Setup cron job for ansible-pull
      cron:
        name: "Ansible pull"
        minute: "*/30"
        job: "/usr/local/bin/ansible-pull-update >> /var/log/ansible-pull.log 2>&1"
```

### 4. Multi-Region Deployment

```yaml
---
- name: Deploy to multiple regions
  hosts: localhost
  vars:
    regions:
      - us-east-1
      - eu-west-1
      - ap-southeast-1
  
  tasks:
    - name: Deploy to each region
      include_tasks: deploy_region.yml
      vars:
        region: "{{ item }}"
        inventory_file: "inventory/{{ item }}.yml"
      loop: "{{ regions }}"
      when: item in target_regions | default(regions)
    
    - name: Update global DNS
      route53:
        state: present
        zone: example.com
        record: app.example.com
        type: A
        value: "{{ regional_endpoints }}"
        alias: true
        alias_hosted_zone_id: Z215JYRZR1TBD5
        weight: 100
        identifier: "{{ item.region }}"
      loop: "{{ deployment_results }}"
```

## Performance Optimization

### 1. Fact Caching

```ini
# ansible.cfg
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 86400
```

### 2. Pipelining

```ini
# ansible.cfg
[ssh_connection]
pipelining = True
control_path = /tmp/ansible-ssh-%%h-%%p-%%r
```

### 3. Async Tasks

```yaml
- name: Long running tasks
  command: /opt/scripts/data_migration.sh
  async: 3600
  poll: 0
  register: migration_job

- name: Other tasks while migration runs
  include_tasks: other_tasks.yml

- name: Check migration status
  async_status:
    jid: "{{ migration_job.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 120
  delay: 30
```

## Monitoring and Observability

### Integration with Monitoring Systems

```yaml
- name: Configure Prometheus node exporter
  hosts: all
  roles:
    - prometheus.prometheus.node_exporter
  
  post_tasks:
    - name: Add Ansible metrics
      copy:
        dest: /var/lib/node_exporter/ansible_facts.prom
        content: |
          # HELP ansible_last_run_timestamp Unix timestamp of last Ansible run
          # TYPE ansible_last_run_timestamp gauge
          ansible_last_run_timestamp {{ ansible_date_time.epoch }}
          
          # HELP ansible_last_run_changed Number of changed tasks in last run
          # TYPE ansible_last_run_changed gauge
          ansible_last_run_changed {{ ansible_play_stats.changed | default(0) }}
```

### Callback Plugins for Logging

```python
# callback_plugins/json_logger.py
from ansible.plugins.callback import CallbackBase
import json
import datetime

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'json_logger'

    def v2_runner_on_ok(self, result):
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'host': result._host.name,
            'task': result._task.get_name(),
            'status': 'ok',
            'changed': result._result.get('changed', False)
        }
        self._display.display(json.dumps(log_entry))
```

## Security Best Practices

### 1. Least Privilege Access

```yaml
- name: Configure sudo rules for Ansible
  hosts: all
  tasks:
    - name: Create ansible sudo rule
      copy:
        dest: /etc/sudoers.d/ansible
        content: |
          ansible ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
          ansible ALL=(ALL) NOPASSWD: /usr/bin/systemctl reload nginx
          ansible ALL=(ALL) NOPASSWD: /usr/bin/apt-get update
        validate: 'visudo -cf %s'
```

### 2. Secure Communication

```ini
# ansible.cfg
[defaults]
host_key_checking = True
host_key_auto_add = False

[ssh_connection]
ssh_args = -C -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=yes
```

### 3. Audit Logging

```yaml
- name: Enable audit logging
  hosts: all
  tasks:
    - name: Configure auditd for Ansible
      blockinfile:
        path: /etc/audit/rules.d/ansible.rules
        block: |
          # Log all ansible commands
          -a always,exit -F arch=b64 -S execve -F path=/usr/bin/ansible -k ansible_exec
          -a always,exit -F arch=b64 -S execve -F path=/usr/bin/ansible-playbook -k ansible_exec
      notify: restart auditd
```

## Troubleshooting

### Debug Strategies

```yaml
# Verbose debugging
- name: Debug task
  debug:
    msg: |
      Host: {{ inventory_hostname }}
      Groups: {{ group_names }}
      All variables: {{ hostvars[inventory_hostname] }}
  tags: [never, debug]

# Step-by-step execution
ansible-playbook site.yml --step --start-at-task="Configure database"

# Check mode
ansible-playbook site.yml --check --diff

# Limiting execution
ansible-playbook site.yml --limit "web*:!web3*" --tags configuration
```

### Common Issues and Solutions

1. **SSH Connection Issues**
```bash
# Test connectivity
ansible all -m ping -vvvv

# Use specific SSH key
ansible-playbook site.yml --private-key=~/.ssh/ansible_key
```

2. **Module Failures**
```yaml
# Add error handling
- name: Ensure service is running
  service:
    name: "{{ item }}"
    state: started
  loop:
    - nginx
    - php-fpm
  ignore_errors: yes
  register: service_result

- name: Report failures
  fail:
    msg: "Failed services: {{ service_result.results | selectattr('failed') | map(attribute='item') | list }}"
  when: service_result.results | selectattr('failed') | list | length > 0
```

3. **Performance Issues**
```bash
# Profile playbook execution
ansible-playbook site.yml --profile=prof_output.json

# Analyze slowest tasks
cat prof_output.json | jq '.plays[].tasks[] | select(.duration > 10) | {task: .name, duration: .duration}'
```

## Integration Examples

### CI/CD Pipeline Integration

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - deploy

validate:
  stage: validate
  script:
    - ansible-playbook site.yml --syntax-check
    - ansible-lint playbooks/
    - molecule test

deploy_staging:
  stage: deploy
  script:
    - ansible-playbook -i inventory/staging site.yml
  environment:
    name: staging
  only:
    - develop

deploy_production:
  stage: deploy
  script:
    - ansible-playbook -i inventory/production site.yml --limit "batch1"
    - sleep 300
    - ansible-playbook -i inventory/production site.yml --limit "batch2"
  environment:
    name: production
  only:
    - main
  when: manual
```

## Conclusion

Ansible's simplicity and power make it an excellent choice for configuration management and automation. Its agentless architecture, combined with a vast ecosystem of modules and roles, enables teams to manage infrastructure efficiently at any scale. By following these patterns and best practices, you can build robust, maintainable automation solutions.