# YAML

## Overview

YAML (YAML Ain't Markup Language) is a human-readable data serialization standard that's widely used for configuration files, data exchange, and infrastructure as code. It's essential for platform engineers working with Kubernetes, Docker Compose, CI/CD pipelines, and configuration management.

## Key Features

- **Human-Readable**: Clean, intuitive syntax
- **Hierarchical**: Supports nested data structures
- **Language-Independent**: Works with any programming language
- **Indentation-Based**: Uses spaces for structure (no tabs)
- **Multi-Document**: Multiple documents in one file

## Basic Syntax

### Scalars and Collections
```yaml
# Scalars
string_value: "Hello World"
number: 42
float_number: 3.14
boolean: true
null_value: null
date: 2024-01-01

# Lists
fruits:
  - apple
  - banana
  - orange

# Inline list
colors: [red, green, blue]

# Maps/Dictionaries
person:
  name: John Doe
  age: 30
  email: john@example.com

# Inline map
coordinates: {x: 10, y: 20}
```

### Advanced Features
```yaml
# Multi-line strings
description: |
  This is a multi-line string
  that preserves line breaks
  and formatting.

# Folded strings
summary: >
  This is a long string
  that will be folded into
  a single line.

# Anchors and aliases
defaults: &default_settings
  timeout: 30
  retries: 3
  debug: false

production:
  <<: *default_settings
  debug: false
  host: prod.example.com

development:
  <<: *default_settings
  debug: true
  host: localhost
```

## Platform Engineering Use Cases

### Kubernetes Manifests
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web-app
    environment: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web
        image: nginx:1.21
        ports:
        - containerPort: 80
        env:
        - name: ENV
          value: "production"
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### CI/CD Pipeline (GitHub Actions)
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18'
  REGISTRY: ghcr.io

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
    - run: npm ci
    - run: npm test
    - run: npm run lint

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker image
      run: |
        docker build -t ${{ env.REGISTRY }}/${{ github.repository }}:${{ github.sha }} .
        docker push ${{ env.REGISTRY }}/${{ github.repository }}:${{ github.sha }}
```

### Ansible Playbook
```yaml
---
- name: Deploy web application
  hosts: web_servers
  become: yes
  vars:
    app_name: myapp
    app_version: "{{ github_sha | default('latest') }}"
    app_port: 8080
  
  tasks:
  - name: Update package cache
    package:
      update_cache: yes
  
  - name: Install Docker
    package:
      name: docker.io
      state: present
  
  - name: Pull application image
    docker_image:
      name: "myregistry/{{ app_name }}:{{ app_version }}"
      source: pull
  
  - name: Run application container
    docker_container:
      name: "{{ app_name }}"
      image: "myregistry/{{ app_name }}:{{ app_version }}"
      ports:
        - "{{ app_port }}:{{ app_port }}"
      restart_policy: always
      env:
        APP_ENV: production
        DATABASE_URL: "{{ database_url }}"
```

## Best Practices

### Formatting and Style
```yaml
# Good: Consistent indentation (2 spaces)
services:
  web:
    image: nginx
    ports:
      - "80:80"

# Bad: Mixed indentation
services:
    web:
  image: nginx
      ports:
    - "80:80"

# Good: Quoted strings when needed
version: "3.8"
command: "echo 'Hello World'"

# Good: Meaningful comments
# Database configuration for production
database:
  host: prod-db.example.com
  port: 5432
  # Connection pool settings
  max_connections: 100
  timeout: 30
```

### Validation and Linting
```bash
# Install yamllint
pip install yamllint

# Lint YAML files
yamllint myfile.yaml
yamllint *.yaml

# Custom yamllint config (.yamllint)
rules:
  line-length:
    max: 120
  indentation:
    spaces: 2
  truthy:
    allowed-values: ['true', 'false']
```

## Common Pitfalls

### Indentation Issues
```yaml
# Wrong: Using tabs
services:
	web:  # Tab character - will cause errors
		image: nginx

# Right: Using spaces
services:
  web:  # 2 spaces
    image: nginx  # 4 spaces
```

### String Quoting
```yaml
# Problematic: Unquoted version numbers
version: 3.8  # Interpreted as float 3.8

# Correct: Quoted version
version: "3.8"  # String "3.8"

# Special characters need quotes
password: "p@ssw0rd!"
command: "echo 'hello world'"
```

## Tools and Utilities

### Command Line Tools
```bash
# yq - YAML processor
sudo snap install yq

# Extract values
yq eval '.services.web.image' docker-compose.yml

# Modify YAML
yq eval '.services.web.ports[0] = "8080:80"' -i docker-compose.yml

# Convert YAML to JSON
yq eval -o=json docker-compose.yml
```

### Python Integration
```python
import yaml

# Load YAML
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Access data
print(config['database']['host'])

# Write YAML
data = {'name': 'myapp', 'version': '1.0'}
with open('output.yaml', 'w') as file:
    yaml.dump(data, file, default_flow_style=False)
```

## Great Resources

- [YAML Official Specification](https://yaml.org/spec/) - Complete YAML language specification
- [YAML Lint](http://www.yamllint.com/) - Online YAML validator and formatter
- [yq Documentation](https://mikefarah.gitbook.io/yq/) - Command-line YAML processor
- [yamllint](https://yamllint.readthedocs.io/) - Python-based YAML linter
- [YAML Best Practices](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html) - Ansible YAML style guide
- [Learn YAML](https://learnxinyminutes.com/docs/yaml/) - Quick YAML syntax reference
- [YAML Multiline Strings](https://yaml-multiline.info/) - Interactive guide to YAML strings