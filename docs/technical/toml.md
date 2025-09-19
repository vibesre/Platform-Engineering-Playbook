# TOML

TOML (Tom's Obvious Minimal Language) is a configuration file format that aims to be easy to read and write due to obvious semantics. It's designed to map unambiguously to a hash table and is popular for configuration files in modern development tools.

## Overview

TOML is widely used in platform engineering for:
- Application configuration (Rust Cargo.toml, Python pyproject.toml)
- Infrastructure configuration (Netlify, Cloudflare Workers)
- Tool configuration (Black, Poetry, Hugo)
- Service configuration files

## Key Features

- **Human-Readable**: Clear, intuitive syntax
- **Minimal**: Simple and unambiguous
- **Strongly Typed**: Explicit data types
- **Unicode**: Full Unicode support
- **Hierarchical**: Supports nested structures through tables

## Basic Syntax

### Data Types
```toml
# Strings
title = "TOML Example"
literal_string = 'C:\Users\nodejs\templates'
multiline_basic = """
This is a multiline
basic string
"""
multiline_literal = '''
This is a multiline
literal string
'''

# Integers
port = 8080
hex_value = 0xDEADBEEF
oct_value = 0o755
bin_value = 0b11010110

# Floats
pi = 3.14159
exponential = 5e+22
negative_infinity = -inf
not_a_number = nan

# Booleans
enabled = true
debug = false

# Dates and Times
created_at = 1979-05-27T07:32:00Z
local_date = 1979-05-27
local_time = 07:32:00
local_datetime = 1979-05-27T07:32:00
```

### Arrays
```toml
# Simple arrays
ports = [8080, 8081, 8082]
hosts = ["localhost", "example.com", "api.example.com"]
mixed_array = ["string", 123, true]

# Arrays of arrays
matrix = [[1, 2], [3, 4]]

# Multiline arrays
servers = [
    "alpha",
    "beta",
    "gamma"
]

# Array of tables (inline)
points = [
    { x = 1, y = 2, z = 3 },
    { x = 7, y = 8, z = 9 },
    { x = 2, y = 4, z = 8 }
]
```

### Tables (Objects)
```toml
# Basic table
[database]
host = "localhost"
port = 5432
username = "admin"
password = "secret"
ssl_enabled = true

# Nested tables
[database.connection_pool]
min_connections = 5
max_connections = 20
idle_timeout = 300

# Alternative nested syntax
[logging]
level = "info"
format = "json"

[logging.outputs]
console = true
file = "/var/log/app.log"
syslog = false

# Array of tables
[[servers]]
name = "web-01"
ip = "192.168.1.10"
role = "web"

[[servers]]
name = "web-02" 
ip = "192.168.1.11"
role = "web"

[[servers]]
name = "db-01"
ip = "192.168.1.20"
role = "database"
```

## Platform Engineering Use Cases

### Application Configuration
```toml
[application]
name = "user-service"
version = "1.2.3"
description = "User management microservice"
port = 8080
host = "0.0.0.0"
workers = 4
timeout = 30

[application.features]
authentication = true
rate_limiting = true
metrics = true
health_checks = true

[database]
driver = "postgresql"
host = "localhost"
port = 5432
database = "users"
username = "app_user"
max_connections = 20
ssl_mode = "require"

[database.migrations]
enabled = true
directory = "migrations"
table = "schema_migrations"

[redis]
host = "localhost"
port = 6379
db = 0
password = ""
timeout = 5

[logging]
level = "info"
format = "json"
destination = "stdout"

[logging.fields]
service = "user-service"
version = "1.2.3"
environment = "production"

[metrics]
enabled = true
port = 9090
path = "/metrics"

[metrics.collectors]
go_runtime = true
process = true
http_requests = true

[security]
cors_enabled = true
cors_origins = ["https://example.com", "https://app.example.com"]
rate_limit = 100
rate_window = "1h"

[security.jwt]
secret = "${JWT_SECRET}"
expiry = "24h"
issuer = "user-service"
```

### Docker Compose Alternative (using TOML)
```toml
[services.web]
image = "nginx:alpine"
ports = ["80:80", "443:443"]
depends_on = ["app"]
restart = "unless-stopped"

[services.web.volumes]
nginx_conf = "./nginx.conf:/etc/nginx/nginx.conf:ro"
ssl_certs = "./ssl:/etc/ssl:ro"

[services.app]
build = { context = ".", dockerfile = "Dockerfile" }
ports = ["8080:8080"]
depends_on = ["db", "redis"]
restart = "unless-stopped"

[services.app.environment]
NODE_ENV = "production"
DATABASE_URL = "postgresql://user:pass@db:5432/myapp"
REDIS_URL = "redis://redis:6379"

[services.db]
image = "postgres:15"
restart = "unless-stopped"

[services.db.environment]
POSTGRES_DB = "myapp"
POSTGRES_USER = "user"
POSTGRES_PASSWORD = "password"

[services.db.volumes]
postgres_data = "/var/lib/postgresql/data"

[services.redis]
image = "redis:7-alpine"
restart = "unless-stopped"

[services.redis.command]
args = ["redis-server", "--appendonly", "yes"]

[volumes]
postgres_data = {}
nginx_conf = {}
ssl_certs = {}

[networks.default]
driver = "bridge"
```

### CI/CD Configuration
```toml
[pipeline]
name = "user-service-ci"
version = "1.0"

[pipeline.triggers]
push = ["main", "develop"]
pull_request = ["main"]
schedule = "0 2 * * *"  # Daily at 2 AM

[stages.test]
image = "node:18"
script = [
    "npm ci",
    "npm run lint",
    "npm run test:unit",
    "npm run test:integration"
]

[stages.test.cache]
paths = ["node_modules/", ".npm/"]

[stages.security]
image = "securecodewarrior/docker-image-scanner"
script = [
    "trivy image --exit-code 1 --severity HIGH,CRITICAL $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
]
depends_on = ["build"]

[stages.build]
image = "docker:latest"
script = [
    "docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .",
    "docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
]
depends_on = ["test"]

[stages.deploy.staging]
image = "kubectl:latest"
script = [
    "kubectl set image deployment/user-service user-service=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA",
    "kubectl rollout status deployment/user-service"
]
environment = "staging"
depends_on = ["security"]
only = ["develop"]

[stages.deploy.production]
image = "kubectl:latest"
script = [
    "kubectl set image deployment/user-service user-service=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA",
    "kubectl rollout status deployment/user-service"
]
environment = "production"
depends_on = ["security"]
only = ["main"]
when = "manual"

[notifications.slack]
webhook = "${SLACK_WEBHOOK}"
channel = "#deployments"
on_success = true
on_failure = true
```

### Infrastructure Configuration
```toml
[infrastructure]
project = "my-platform"
region = "us-west-2"
environment = "production"

[kubernetes]
cluster_name = "production-cluster"
version = "1.28"
node_groups = 3

[kubernetes.node_groups.web]
instance_type = "t3.medium"
min_size = 2
max_size = 10
desired_size = 3

[kubernetes.node_groups.web.labels]
role = "web"
environment = "production"

[kubernetes.node_groups.workers]
instance_type = "c5.xlarge"
min_size = 1
max_size = 20
desired_size = 5

[kubernetes.node_groups.workers.labels]
role = "worker"
workload = "compute-intensive"

[networking]
vpc_cidr = "10.0.0.0/16"
availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]

[networking.subnets.public]
cidrs = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]

[networking.subnets.private]
cidrs = ["10.0.10.0/24", "10.0.20.0/24", "10.0.30.0/24"]

[database]
engine = "postgres"
version = "15.4"
instance_class = "db.r5.large"
allocated_storage = 100
backup_retention = 7
multi_az = true

[monitoring]
prometheus_enabled = true
grafana_enabled = true
alertmanager_enabled = true

[monitoring.alerts]
high_cpu_threshold = 80
high_memory_threshold = 85
disk_usage_threshold = 90
response_time_threshold = 500

[security]
ssl_certificate_arn = "arn:aws:acm:us-west-2:123456789012:certificate/12345678-1234-1234-1234-123456789012"
waf_enabled = true
cloudtrail_enabled = true

[security.firewall_rules]
ssh = { port = 22, cidr = "10.0.0.0/16" }
http = { port = 80, cidr = "0.0.0.0/0" }
https = { port = 443, cidr = "0.0.0.0/0" }
```

## Working with TOML

### Python Integration
```python
# requirements.txt
toml>=0.10.2
tomli>=2.0.1  # For Python 3.11+ (built-in tomllib)
tomli-w>=1.0.0  # For writing TOML

# toml_processor.py
import toml
import tomli_w
from pathlib import Path

class TOMLProcessor:
    def __init__(self):
        pass
    
    def load_config(self, file_path):
        """Load TOML configuration file"""
        try:
            with open(file_path, 'r') as f:
                return toml.load(f)
        except toml.TomlDecodeError as e:
            print(f"Error parsing TOML: {e}")
            return None
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
    
    def save_config(self, data, file_path):
        """Save data to TOML file"""
        try:
            with open(file_path, 'wb') as f:
                tomli_w.dump(data, f)
        except Exception as e:
            print(f"Error saving TOML: {e}")
    
    def validate_config(self, file_path):
        """Validate TOML syntax"""
        try:
            with open(file_path, 'r') as f:
                toml.load(f)
            return True, "Valid TOML"
        except toml.TomlDecodeError as e:
            return False, f"Invalid TOML: {e}"
    
    def merge_configs(self, *file_paths):
        """Merge multiple TOML files"""
        merged = {}
        for file_path in file_paths:
            config = self.load_config(file_path)
            if config:
                merged = self._deep_merge(merged, config)
        return merged
    
    def _deep_merge(self, dict1, dict2):
        """Deep merge two dictionaries"""
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

# Usage example
if __name__ == "__main__":
    processor = TOMLProcessor()
    
    # Example configuration
    config = {
        'application': {
            'name': 'my-service',
            'version': '1.0.0',
            'port': 8080
        },
        'database': {
            'host': 'localhost',
            'port': 5432,
            'credentials': {
                'username': 'admin',
                'password': 'secret123'
            }
        },
        'features': ['auth', 'logging', 'metrics']
    }
    
    # Save configuration
    processor.save_config(config, 'config.toml')
    
    # Load and validate
    loaded_config = processor.load_config('config.toml')
    print("Loaded config:", loaded_config)
    
    is_valid, message = processor.validate_config('config.toml')
    print(f"Validation: {message}")
```

### Go Integration
```go
package main

import (
    "fmt"
    "log"
    "os"
    
    "github.com/BurntSushi/toml"
)

type Config struct {
    Application ApplicationConfig `toml:"application"`
    Database    DatabaseConfig    `toml:"database"`
    Logging     LoggingConfig     `toml:"logging"`
    Features    []string          `toml:"features"`
}

type ApplicationConfig struct {
    Name    string `toml:"name"`
    Version string `toml:"version"`
    Port    int    `toml:"port"`
    Host    string `toml:"host"`
    Workers int    `toml:"workers"`
}

type DatabaseConfig struct {
    Driver         string               `toml:"driver"`
    Host           string               `toml:"host"`
    Port           int                  `toml:"port"`
    Database       string               `toml:"database"`
    Username       string               `toml:"username"`
    MaxConnections int                  `toml:"max_connections"`
    ConnectionPool ConnectionPoolConfig `toml:"connection_pool"`
}

type ConnectionPoolConfig struct {
    MinConnections int `toml:"min_connections"`
    MaxConnections int `toml:"max_connections"`
    IdleTimeout    int `toml:"idle_timeout"`
}

type LoggingConfig struct {
    Level       string            `toml:"level"`
    Format      string            `toml:"format"`
    Destination string            `toml:"destination"`
    Fields      map[string]string `toml:"fields"`
}

func main() {
    var config Config
    
    // Load configuration from file
    if _, err := toml.DecodeFile("config.toml", &config); err != nil {
        log.Fatalf("Error loading config: %v", err)
    }
    
    fmt.Printf("Application: %s v%s\n", config.Application.Name, config.Application.Version)
    fmt.Printf("Database: %s://%s:%d/%s\n", 
        config.Database.Driver,
        config.Database.Host,
        config.Database.Port,
        config.Database.Database)
    fmt.Printf("Features: %v\n", config.Features)
    
    // Write configuration to file
    output, err := os.Create("output.toml")
    if err != nil {
        log.Fatalf("Error creating output file: %v", err)
    }
    defer output.Close()
    
    encoder := toml.NewEncoder(output)
    if err := encoder.Encode(config); err != nil {
        log.Fatalf("Error encoding TOML: %v", err)
    }
    
    fmt.Println("Configuration saved to output.toml")
}
```

### Rust Integration (Cargo.toml)
```toml
[package]
name = "my-service"
version = "0.1.0"
edition = "2021"
authors = ["Your Name <your.email@example.com>"]
description = "A microservice built with Rust"
license = "MIT"
repository = "https://github.com/user/my-service"
keywords = ["microservice", "api", "web"]
categories = ["web-programming"]

[dependencies]
tokio = { version = "1.0", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
reqwest = { version = "0.11", features = ["json"] }
sqlx = { version = "0.7", features = ["runtime-tokio-rustls", "postgres", "uuid", "chrono"] }
uuid = { version = "1.0", features = ["v4", "serde"] }
chrono = { version = "0.4", features = ["serde"] }
tracing = "0.1"
tracing-subscriber = "0.3"
config = "0.13"
anyhow = "1.0"

[dev-dependencies]
tokio-test = "0.4"
mockall = "0.11"

[profile.release]
lto = true
codegen-units = 1
panic = "abort"

[profile.dev]
debug = true
opt-level = 0

[[bin]]
name = "server"
path = "src/main.rs"

[[bin]]
name = "migrate"
path = "src/bin/migrate.rs"

[features]
default = ["postgres"]
postgres = ["sqlx/postgres"]
mysql = ["sqlx/mysql"]
```

## Advanced Features

### Environment Variable Interpolation
```toml
# Using a TOML processor that supports env vars
[database]
host = "${DATABASE_HOST}"
port = "${DATABASE_PORT:5432}"  # Default value
username = "${DATABASE_USER}"
password = "${DATABASE_PASSWORD}"

[application]
debug = "${DEBUG:false}"
log_level = "${LOG_LEVEL:info}"
```

### Configuration Templates
```toml
# base.toml
[application]
name = "my-service"
port = 8080

[database]
driver = "postgres"
host = "localhost"

# production.toml (inherits from base.toml)
[database]
host = "prod-db.example.com"
ssl_mode = "require"
max_connections = 50

[logging]
level = "warn"
format = "json"

# development.toml (inherits from base.toml)
[database]
host = "localhost"
ssl_mode = "disable"

[logging]
level = "debug"
format = "console"

[application]
debug = true
```

## Best Practices

### Organization and Structure
```toml
# Good: Logical grouping and clear naming
[application]
name = "user-service"
version = "1.2.3"

[application.server]
host = "0.0.0.0"
port = 8080
workers = 4

[application.timeouts]
read = 30
write = 30
idle = 120

# Good: Use tables for related configuration
[database.primary]
host = "primary-db.example.com"
port = 5432

[database.replica]
host = "replica-db.example.com"
port = 5432

# Good: Arrays for similar items
[[load_balancers]]
name = "lb-1"
host = "10.0.1.10"
weight = 100

[[load_balancers]]
name = "lb-2"
host = "10.0.1.11"
weight = 100
```

### Comments and Documentation
```toml
# Application configuration for user service
# Last updated: 2024-01-01

[application]
# Service identification
name = "user-service"
version = "1.2.3"
description = "User management microservice"

# Network configuration
host = "0.0.0.0"  # Bind to all interfaces
port = 8080       # HTTP port
workers = 4       # Number of worker processes

[database]
# Primary database connection
host = "localhost"
port = 5432
database = "users"
username = "app_user"

# Connection pool settings
# Adjust based on expected load
max_connections = 20  # Maximum concurrent connections
min_connections = 5   # Minimum pool size
idle_timeout = 300    # Seconds before closing idle connections
```

### Security Considerations
```toml
# Good: Separate sensitive configuration
[database]
host = "localhost"
port = 5432
database = "myapp"
# Credentials should be in environment variables or separate secure files

# Good: Use environment variable references
[security]
jwt_secret = "${JWT_SECRET}"
api_key = "${API_KEY}"

# Bad: Hardcoded secrets
[security]
jwt_secret = "super-secret-key-123"
api_key = "abc123def456"
```

## Comparison with Other Formats

### TOML vs YAML vs JSON
```toml
# TOML - Clear structure, explicit types
[database]
host = "localhost"
port = 5432
ssl_enabled = true
```

```yaml
# YAML - Indentation-based, concise
database:
  host: localhost
  port: 5432
  ssl_enabled: true
```

```json
// JSON - Verbose but universally supported
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "ssl_enabled": true
  }
}
```

## Common Pitfalls

### Data Type Confusion
```toml
# Wrong: Unquoted string that looks like number
version = 1.2.3  # This is a float, not a version string

# Right: Quote version strings
version = "1.2.3"

# Wrong: Mixed array types
values = [1, "two", 3.0]  # Error: mixed types

# Right: Consistent array types
numbers = [1, 2, 3]
strings = ["one", "two", "three"]
```

### Table Declaration Order
```toml
# Wrong: Table declared after sub-table
[database.pool]
size = 10

[database]  # Error: table already has sub-table
host = "localhost"

# Right: Parent table first
[database]
host = "localhost"

[database.pool]
size = 10
```

## Tools and Utilities

### Command Line Tools
```bash
# Install TOML tools
pip install toml-cli

# Validate TOML file
toml-cli validate config.toml

# Convert TOML to JSON
toml-cli convert config.toml --output-format json

# Extract values
toml-cli get config.toml database.host

# Set values
toml-cli set config.toml database.port 5433
```

### Online Tools
- [TOML Validator](https://www.toml-lint.com/) - Online TOML syntax validator
- [TOML to JSON Converter](https://toolslick.com/conversion/data/toml-to-json) - Convert between formats
- [TOML Parser](https://pseitz.github.io/toml-parse/) - Interactive TOML parser and explorer

## Resources

- [TOML Official Specification](https://toml.io/) - Complete TOML language specification
- [TOML GitHub Repository](https://github.com/toml-lang/toml) - Official TOML repository and documentation
- [Python TOML Library](https://pypi.org/project/toml/) - Python TOML parser and writer
- [Go TOML Library](https://github.com/BurntSushi/toml) - Go TOML parser and encoder
- [Rust TOML Crate](https://docs.rs/toml/) - Rust TOML parser and serializer
- [TOML vs YAML vs JSON](https://www.codeready.tech/toml-vs-yaml-vs-json/) - Format comparison guide
- [TOML Best Practices](https://hitchdev.com/strictyaml/why-not/toml/) - Configuration best practices
- [Cargo.toml Reference](https://doc.rust-lang.org/cargo/reference/manifest.html) - Rust package manifest format
- [pyproject.toml Guide](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/) - Python project metadata
- [TOML Linter](https://taplo.tamasfe.dev/) - TOML formatter and linter