---
title: Programming for Platform Engineers
sidebar_position: 3
tags: [beginner, programming, python, go]
---

# 💻 Programming for Platform Engineers

**Prerequisites**: Basic command line knowledge  
**Time to Complete**: ⏱️ 3-4 hours

## Why Programming Matters

Platform engineers need programming skills to:
- Automate repetitive tasks
- Build internal tools and CLIs
- Create operators and controllers
- Write infrastructure as code
- Debug and extend existing systems

## Language Overview

### Languages You'll Use

| Language | Primary Use | When to Use |
|----------|-------------|-------------|
| **Python** | Automation, scripting, tools | Quick scripts, AWS Lambda, data processing |
| **Go** | System tools, Kubernetes operators | Performance-critical tools, cloud-native apps |
| **Bash** | System scripts, glue code | System administration, CI/CD pipelines |
| **YAML/JSON** | Configuration | Kubernetes, CI/CD, IaC |

## Python Fundamentals

### Getting Started with Python

```python
#!/usr/bin/env python3
# Platform engineer's first Python script

import os
import sys
import subprocess

def main():
    """Main function - good practice for scripts"""
    print(f"Running as user: {os.environ.get('USER')}")
    print(f"Python version: {sys.version}")
    
    # Run a system command
    result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
    print(f"Files in current directory:\n{result.stdout}")

if __name__ == "__main__":
    main()
```

### Essential Python Concepts

#### Variables and Data Types

```python
# Basic types
name = "nginx"                  # String
port = 8080                    # Integer  
cpu_limit = 2.5               # Float
is_healthy = True             # Boolean

# Collections
servers = ["web1", "web2", "web3"]          # List
config = {"port": 8080, "host": "0.0.0.0"}  # Dictionary
regions = {"us-east-1", "us-west-2"}        # Set
coordinates = (lat, lon)                     # Tuple

# Type hints (Python 3.5+)
def deploy_service(name: str, replicas: int = 3) -> bool:
    return True
```

#### Control Flow

```python
# Conditionals
if cpu_usage > 80:
    print("High CPU alert!")
elif cpu_usage > 60:
    print("CPU usage elevated")
else:
    print("CPU usage normal")

# Loops
for server in servers:
    print(f"Checking {server}")

# List comprehension
healthy_servers = [s for s in servers if check_health(s)]

# Error handling
try:
    response = requests.get("http://api.example.com")
    response.raise_for_status()
except requests.RequestException as e:
    print(f"API error: {e}")
```

### Python for DevOps Tasks

#### File Operations

```python
import json
import yaml
from pathlib import Path

# Read configuration
def load_config(config_file):
    """Load YAML or JSON config file"""
    path = Path(config_file)
    
    with open(path, 'r') as f:
        if path.suffix == '.yaml' or path.suffix == '.yml':
            return yaml.safe_load(f)
        elif path.suffix == '.json':
            return json.load(f)
    
# Write logs
def write_log(message, log_file="/var/log/deploy.log"):
    """Append message to log file"""
    with open(log_file, 'a') as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - {message}\n")
```

#### System Operations

```python
import subprocess
import platform
import psutil

def get_system_info():
    """Gather system information"""
    info = {
        "hostname": platform.node(),
        "os": platform.system(),
        "architecture": platform.machine(),
        "cpu_count": psutil.cpu_count(),
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "disk_usage": psutil.disk_usage('/').percent
    }
    return info

def run_command(cmd, check=True):
    """Run shell command and return output"""
    result = subprocess.run(
        cmd, 
        shell=True, 
        capture_output=True, 
        text=True,
        check=check
    )
    return result.stdout.strip()

# Example usage
docker_version = run_command("docker --version")
running_containers = run_command("docker ps -q | wc -l")
```

#### HTTP Requests and APIs

```python
import requests
from typing import Dict, List

class KubernetesClient:
    """Simple Kubernetes API client"""
    
    def __init__(self, api_server: str, token: str):
        self.api_server = api_server
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def get_pods(self, namespace: str = "default") -> List[Dict]:
        """Get all pods in namespace"""
        url = f"{self.api_server}/api/v1/namespaces/{namespace}/pods"
        response = requests.get(url, headers=self.headers, verify=False)
        response.raise_for_status()
        return response.json()["items"]
    
    def get_pod_status(self, name: str, namespace: str = "default") -> str:
        """Get pod status"""
        pods = self.get_pods(namespace)
        for pod in pods:
            if pod["metadata"]["name"] == name:
                return pod["status"]["phase"]
        return "Not Found"
```

### Python Best Practices

#### Project Structure

```
my-platform-tool/
├── requirements.txt      # Dependencies
├── setup.py             # Package setup
├── README.md            # Documentation
├── .gitignore          # Git ignore file
├── tests/              # Unit tests
│   └── test_main.py
└── src/                # Source code
    ├── __init__.py
    ├── main.py
    └── utils.py
```

#### Virtual Environments

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Save dependencies
pip freeze > requirements.txt
```

## Go Fundamentals

### Why Go for Platform Engineering?

- **Performance**: Compiled language, great for tools
- **Concurrency**: Built-in goroutines and channels
- **Static binaries**: Easy deployment
- **Cloud-native**: Kubernetes, Docker, Terraform written in Go

### Getting Started with Go

```go
package main

import (
    "fmt"
    "log"
    "os"
    "os/exec"
)

func main() {
    // Print environment info
    hostname, err := os.Hostname()
    if err != nil {
        log.Fatal("Failed to get hostname:", err)
    }
    
    fmt.Printf("Running on: %s\n", hostname)
    fmt.Printf("Go version: %s\n", runtime.Version())
    
    // Run system command
    cmd := exec.Command("ls", "-la")
    output, err := cmd.Output()
    if err != nil {
        log.Fatal("Command failed:", err)
    }
    
    fmt.Printf("Directory contents:\n%s\n", output)
}
```

### Go Basics

#### Variables and Types

```go
package main

// Basic types
var (
    serviceName string = "api-gateway"
    port        int    = 8080
    cpuLimit    float64 = 2.5
    isHealthy   bool   = true
)

// Short declaration
replicas := 3

// Slices and maps
servers := []string{"web1", "web2", "web3"}
config := map[string]interface{}{
    "port": 8080,
    "host": "0.0.0.0",
}

// Structs
type Server struct {
    Name      string
    IP        string
    Port      int
    IsHealthy bool
}

// Methods
func (s *Server) HealthCheck() error {
    // Perform health check
    return nil
}
```

#### Error Handling

```go
// Go uses explicit error handling
func deployService(name string) error {
    if name == "" {
        return fmt.Errorf("service name cannot be empty")
    }
    
    // Deploy logic here
    
    return nil
}

// Usage
if err := deployService("nginx"); err != nil {
    log.Printf("Deployment failed: %v", err)
    return err
}
```

#### Concurrency

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func checkServer(name string, wg *sync.WaitGroup) {
    defer wg.Done()
    
    // Simulate health check
    time.Sleep(1 * time.Second)
    fmt.Printf("Server %s is healthy\n", name)
}

func main() {
    servers := []string{"web1", "web2", "web3"}
    var wg sync.WaitGroup
    
    // Check all servers concurrently
    for _, server := range servers {
        wg.Add(1)
        go checkServer(server, &wg)
    }
    
    wg.Wait()
    fmt.Println("All health checks completed")
}
```

### Go for Platform Tools

#### HTTP Server

```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type HealthResponse struct {
    Status  string `json:"status"`
    Version string `json:"version"`
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    response := HealthResponse{
        Status:  "healthy",
        Version: "1.0.0",
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func main() {
    http.HandleFunc("/health", healthHandler)
    
    log.Println("Server starting on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatal(err)
    }
}
```

#### CLI Tool

```go
package main

import (
    "flag"
    "fmt"
    "os"
)

func main() {
    // Define flags
    var (
        namespace = flag.String("namespace", "default", "Kubernetes namespace")
        output    = flag.String("output", "table", "Output format (table|json)")
        verbose   = flag.Bool("verbose", false, "Verbose output")
    )
    
    flag.Parse()
    
    // Validate flags
    if *output != "table" && *output != "json" {
        fmt.Fprintf(os.Stderr, "Invalid output format: %s\n", *output)
        os.Exit(1)
    }
    
    // Main logic
    fmt.Printf("Listing pods in namespace: %s\n", *namespace)
    
    if *verbose {
        fmt.Println("Running in verbose mode...")
    }
}
```

## Data Structures for Platform Engineers

### Arrays and Lists

```python
# Python
servers = ["web1", "web2", "web3"]
servers.append("web4")
servers.remove("web1")

# Go
servers := []string{"web1", "web2", "web3"}
servers = append(servers, "web4")
```

### Hash Maps / Dictionaries

```python
# Python - Service registry
services = {
    "api": {"host": "api.example.com", "port": 8080},
    "web": {"host": "web.example.com", "port": 80}
}

# Access
api_host = services["api"]["host"]

# Go - Configuration map
config := map[string]string{
    "region": "us-east-1",
    "environment": "production",
}
```

### Queues (FIFO)

```python
from collections import deque

# Job queue
job_queue = deque()
job_queue.append("deploy-frontend")
job_queue.append("deploy-backend")

# Process jobs
while job_queue:
    job = job_queue.popleft()
    process_job(job)
```

### Sets

```python
# Track unique IPs
visitor_ips = set()
visitor_ips.add("192.168.1.1")
visitor_ips.add("192.168.1.2")

# Set operations
production_servers = {"srv1", "srv2", "srv3"}
staging_servers = {"srv2", "srv3", "srv4"}

# Servers in both environments
common = production_servers & staging_servers

# All servers
all_servers = production_servers | staging_servers
```

## API Design Basics

### RESTful Principles

```python
# Simple Flask API
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage
services = {}

@app.route('/services', methods=['GET'])
def list_services():
    return jsonify(list(services.values()))

@app.route('/services/<service_id>', methods=['GET'])
def get_service(service_id):
    service = services.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    return jsonify(service)

@app.route('/services', methods=['POST'])
def create_service():
    data = request.json
    service_id = data.get('id')
    services[service_id] = data
    return jsonify(data), 201

@app.route('/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    if service_id in services:
        del services[service_id]
        return '', 204
    return jsonify({"error": "Service not found"}), 404
```

### API Best Practices

1. **Use proper HTTP methods**
   - GET: Read data
   - POST: Create new resource
   - PUT: Update entire resource
   - PATCH: Partial update
   - DELETE: Remove resource

2. **Status codes**
   - 200: Success
   - 201: Created
   - 400: Bad request
   - 404: Not found
   - 500: Server error

3. **Versioning**
   ```
   /api/v1/services
   /api/v2/services
   ```

## Interview Preparation

### Common Programming Questions

**Q: Write a function to check if a service is healthy**

Python:
```python
import requests

def check_service_health(url, timeout=5):
    """Check if service responds with 200 OK"""
    try:
        response = requests.get(f"{url}/health", timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Test multiple services
services = ["http://api:8080", "http://web:80"]
health_status = {svc: check_service_health(svc) for svc in services}
```

Go:
```go
func checkServiceHealth(url string) bool {
    client := &http.Client{Timeout: 5 * time.Second}
    resp, err := client.Get(url + "/health")
    if err != nil {
        return false
    }
    defer resp.Body.Close()
    return resp.StatusCode == 200
}
```

**Q: Parse a log file and count errors**

```python
def count_errors(log_file):
    """Count error lines in log file"""
    error_count = 0
    error_types = {}
    
    with open(log_file, 'r') as f:
        for line in f:
            if 'ERROR' in line:
                error_count += 1
                # Extract error type (simplified)
                error_type = line.split('ERROR')[1].split()[0]
                error_types[error_type] = error_types.get(error_type, 0) + 1
    
    return error_count, error_types

# Usage
total, types = count_errors("/var/log/app.log")
print(f"Total errors: {total}")
print(f"Error breakdown: {types}")
```

### Coding Challenges

#### Challenge 1: Resource Monitor
Write a script that monitors CPU and memory usage and sends an alert if usage exceeds threshold.

#### Challenge 2: Config Validator
Create a function that validates YAML configuration files against a schema.

#### Challenge 3: Log Aggregator
Build a tool that collects logs from multiple servers and combines them with timestamps.

## Best Practices Summary

### Python Best Practices
1. Use virtual environments
2. Follow PEP 8 style guide
3. Write docstrings
4. Handle exceptions properly
5. Use type hints
6. Test your code

### Go Best Practices
1. Format with `gofmt`
2. Handle all errors
3. Use meaningful variable names
4. Keep functions small
5. Use interfaces
6. Write tests

### General Programming Tips
1. Keep it simple (KISS)
2. Don't repeat yourself (DRY)
3. Write readable code
4. Comment why, not what
5. Version control everything
6. Automate testing

## Practice Projects

### Beginner Projects
1. **System Info Script**: Display CPU, memory, disk usage
2. **Log Parser**: Extract and summarize log information
3. **Config Generator**: Generate YAML/JSON configs from templates

### Intermediate Projects
1. **Health Check Tool**: Monitor multiple endpoints
2. **Backup Script**: Automated backup with retention
3. **CLI Tool**: Interact with cloud provider APIs

### Advanced Projects
1. **Kubernetes Operator**: Manage custom resources
2. **Monitoring Agent**: Collect and ship metrics
3. **Deployment Tool**: Blue-green deployment automation

## Next Steps

You now have the programming foundation for platform engineering! Continue with:
- [Cloud & Infrastructure →](../intermediate/cloud-infrastructure)
- [Automation & Scripting Deep Dive →](../intermediate/automation-scripting)

## Quick Reference

### Python Cheat Sheet
```python
# Common imports
import os, sys, json, yaml
import requests
import subprocess
from pathlib import Path
from datetime import datetime

# Environment variables
api_key = os.environ.get('API_KEY', 'default')

# Run command
result = subprocess.run(['ls', '-l'], capture_output=True, text=True)

# HTTP request
response = requests.get('https://api.example.com')
data = response.json()
```

### Go Cheat Sheet
```go
// Common imports
import (
    "fmt"
    "log"
    "os"
    "net/http"
    "encoding/json"
)

// Environment variables
apiKey := os.Getenv("API_KEY")

// Error handling pattern
if err != nil {
    return fmt.Errorf("failed to X: %w", err)
}

// HTTP client
client := &http.Client{Timeout: 10 * time.Second}
```

## Additional Resources

- 📚 **Python**: [Automate the Boring Stuff](https://automatetheboringstuff.com/)
- 📚 **Go**: [The Go Programming Language](https://www.gopl.io/)
- 🎮 **Practice**: [Exercism](https://exercism.io/)
- 📺 **Python Course**: [Python for DevOps](https://www.youtube.com/watch?v=s3Ejmi9bfkI)
- 📺 **Go Course**: [Learn Go Programming](https://www.youtube.com/watch?v=YS4e4q9oBaU)