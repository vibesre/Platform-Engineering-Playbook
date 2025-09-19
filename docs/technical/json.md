# JSON

## Overview

JSON (JavaScript Object Notation) is a lightweight, text-based data interchange format that's widely used for APIs, configuration files, and data storage. It's essential for platform engineers working with REST APIs, configuration management, and data processing.

## Key Features

- **Human-Readable**: Easy to read and write
- **Language-Independent**: Supported by virtually all programming languages
- **Lightweight**: Minimal syntax overhead
- **Structured**: Supports nested objects and arrays
- **Web-Standard**: Native support in web browsers and APIs

## Basic Syntax

### Data Types
```json
{
  "string": "Hello World",
  "number": 42,
  "float": 3.14159,
  "boolean": true,
  "null_value": null,
  "array": [1, 2, 3, "four", true],
  "object": {
    "nested_string": "value",
    "nested_number": 100
  }
}
```

### Platform Engineering Examples
```json
{
  "service": {
    "name": "user-api",
    "version": "1.2.3",
    "port": 8080,
    "health_check": {
      "endpoint": "/health",
      "interval": 30,
      "timeout": 5
    },
    "dependencies": [
      "database",
      "redis-cache",
      "auth-service"
    ],
    "environment": {
      "LOG_LEVEL": "INFO",
      "MAX_CONNECTIONS": 100,
      "ENABLE_METRICS": true
    }
  }
}
```

## Common Use Cases

### API Responses
```json
{
  "status": "success",
  "data": {
    "users": [
      {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "created_at": "2024-01-01T10:00:00Z",
        "roles": ["user", "admin"]
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 150,
      "total_pages": 8
    }
  },
  "meta": {
    "request_id": "req_123456",
    "timestamp": "2024-01-01T10:00:00Z",
    "api_version": "v1"
  }
}
```

### Configuration Files
```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "username": "app_user",
    "database": "myapp_production",
    "ssl": true,
    "pool": {
      "min_connections": 5,
      "max_connections": 20,
      "idle_timeout": 300
    }
  },
  "redis": {
    "host": "redis.example.com",
    "port": 6379,
    "db": 0,
    "ttl": 3600
  },
  "logging": {
    "level": "INFO",
    "format": "json",
    "outputs": ["console", "file"],
    "file_path": "/var/log/app.log"
  }
}
```

### Monitoring and Metrics
```json
{
  "timestamp": "2024-01-01T10:00:00Z",
  "service": "user-api",
  "metrics": {
    "requests_per_second": 125.5,
    "average_response_time": 45.2,
    "error_rate": 0.02,
    "active_connections": 50,
    "memory_usage": {
      "used_mb": 512,
      "total_mb": 1024,
      "percentage": 50.0
    },
    "cpu_usage": {
      "percentage": 25.5,
      "load_average": [1.2, 1.1, 1.0]
    }
  },
  "health_checks": {
    "database": "healthy",
    "redis": "healthy",
    "external_api": "degraded"
  }
}
```

## Working with JSON

### Command Line Tools
```bash
# jq - JSON processor
echo '{"name":"John","age":30}' | jq '.name'
# Output: "John"

# Pretty print JSON
echo '{"name":"John","age":30}' | jq .

# Filter arrays
echo '[{"name":"John","age":30},{"name":"Jane","age":25}]' | jq '.[] | select(.age > 25)'

# Extract specific fields
curl -s https://api.github.com/users/octocat | jq '{name: .name, followers: .followers}'

# Validate JSON
echo '{"invalid": json}' | jq . && echo "Valid" || echo "Invalid"
```

### Python Integration
```python
import json
import requests

# Parse JSON string
json_string = '{"name": "John", "age": 30}'
data = json.loads(json_string)
print(data['name'])  # John

# Convert to JSON
user = {'name': 'Jane', 'age': 25, 'roles': ['user', 'admin']}
json_string = json.dumps(user, indent=2)
print(json_string)

# Work with files
with open('config.json', 'r') as f:
    config = json.load(f)

with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)

# API integration
response = requests.get('https://api.example.com/users')
if response.status_code == 200:
    users = response.json()
    for user in users['data']:
        print(f"User: {user['name']}")
```

### Go Integration
```go
package main

import (
    "encoding/json"
    "fmt"
    "log"
)

type User struct {
    ID       int      `json:"id"`
    Name     string   `json:"name"`
    Email    string   `json:"email"`
    Roles    []string `json:"roles"`
    IsActive bool     `json:"is_active"`
}

func main() {
    // Parse JSON
    jsonData := `{"id":1,"name":"John","email":"john@example.com","roles":["user","admin"],"is_active":true}`
    
    var user User
    err := json.Unmarshal([]byte(jsonData), &user)
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Printf("User: %+v\n", user)
    
    // Convert to JSON
    newUser := User{
        ID:       2,
        Name:     "Jane",
        Email:    "jane@example.com",
        Roles:    []string{"user"},
        IsActive: true,
    }
    
    jsonBytes, err := json.MarshalIndent(newUser, "", "  ")
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Println(string(jsonBytes))
}
```

## Advanced JSON Processing

### Complex jq Queries
```bash
# Group by field
echo '[{"dept":"eng","name":"John"},{"dept":"eng","name":"Jane"},{"dept":"sales","name":"Bob"}]' | \
  jq 'group_by(.dept) | map({department: .[0].dept, employees: map(.name)})'

# Calculate statistics
echo '[{"price":10},{"price":20},{"price":30}]' | \
  jq 'map(.price) | {min: min, max: max, avg: (add/length)}'

# Transform data structure
echo '{"users":{"john":{"age":30},"jane":{"age":25}}}' | \
  jq '.users | to_entries | map({name: .key, age: .value.age})'
```

### JSON Schema Validation
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 150
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "roles": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "uniqueItems": true
    }
  },
  "required": ["name", "email"],
  "additionalProperties": false
}
```

## Best Practices

### Formatting and Style
```json
// Good: Proper indentation and structure
{
  "service_name": "user-api",
  "configuration": {
    "port": 8080,
    "timeout": 30
  },
  "features": [
    "authentication",
    "rate_limiting"
  ]
}

// Bad: No formatting, hard to read
{"service_name":"user-api","configuration":{"port":8080,"timeout":30},"features":["authentication","rate_limiting"]}
```

### Security Considerations
```json
// Good: Separate sensitive data
{
  "database": {
    "host": "db.example.com",
    "port": 5432,
    "database": "myapp"
  }
}

// Bad: Credentials in JSON
{
  "database": {
    "host": "db.example.com",
    "username": "admin",
    "password": "secret123"
  }
}
```

## Common Pitfalls

- **Trailing Commas**: Not allowed in JSON (unlike JavaScript)
- **Comments**: JSON doesn't support comments
- **Single Quotes**: Must use double quotes for strings
- **Undefined Values**: Use `null` instead of `undefined`
- **Large Numbers**: Be aware of integer overflow in some languages

## Great Resources

- [JSON Official Specification](https://www.json.org/) - Complete JSON format specification
- [jq Manual](https://stedolan.github.io/jq/manual/) - Comprehensive jq command-line processor guide
- [JSONLint](https://jsonlint.com/) - Online JSON validator and formatter
- [JSON Schema](https://json-schema.org/) - JSON data validation specification
- [Postman](https://www.postman.com/) - API development and testing tool
- [JSON Viewer](https://jsonviewer.stack.hu/) - Online JSON visualization tool
- [REST API Best Practices](https://restfulapi.net/) - Guidelines for API design with JSON