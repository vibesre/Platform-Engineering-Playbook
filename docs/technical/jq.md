# jq

## Overview

jq is a lightweight and flexible command-line JSON processor that allows you to slice, filter, map, and transform structured JSON data. It's essential for platform engineers working with APIs, configuration files, and JSON data processing.

## Key Features

- **JSON Processing**: Parse, filter, and transform JSON data
- **Powerful Queries**: SQL-like syntax for data manipulation
- **Streaming**: Handle large JSON files efficiently
- **Scripting**: Create reusable JSON processing scripts
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Basic Operations

### Identity and Basic Filtering
```bash
# Pretty print JSON
echo '{"name":"John","age":30}' | jq .

# Extract specific field
echo '{"name":"John","age":30}' | jq '.name'
# Output: "John"

# Extract nested field
echo '{"user":{"name":"John","age":30}}' | jq '.user.name'
# Output: "John"

# Extract multiple fields
echo '{"name":"John","age":30,"city":"NYC"}' | jq '.name, .age'
```

### Array Operations
```bash
# Extract array elements
echo '[1, 2, 3, 4, 5]' | jq '.[2]'  # Third element
echo '[1, 2, 3, 4, 5]' | jq '.[1:3]'  # Slice

# Iterate over array
echo '[{"name":"John"},{"name":"Jane"}]' | jq '.[] | .name'

# Array length
echo '[1, 2, 3, 4, 5]' | jq 'length'

# Filter array elements
echo '[1, 2, 3, 4, 5]' | jq 'map(select(. > 3))'
```

## Platform Engineering Use Cases

### Kubernetes JSON Processing
```bash
# Get pod names
kubectl get pods -o json | jq '.items[].metadata.name'

# Get pod status
kubectl get pods -o json | jq '.items[] | {name: .metadata.name, status: .status.phase}'

# Filter running pods
kubectl get pods -o json | jq '.items[] | select(.status.phase == "Running") | .metadata.name'

# Get container images
kubectl get pods -o json | jq '.items[].spec.containers[].image' | sort | uniq
```

### API Response Processing
```bash
# Process GitHub API response
curl -s https://api.github.com/repos/kubernetes/kubernetes/pulls | \
  jq '.[] | {title: .title, author: .user.login, created: .created_at}'

# Extract specific data from API
curl -s https://api.github.com/users/octocat | \
  jq '{username: .login, followers: .followers, repos: .public_repos}'

# Process paginated API results
curl -s "https://api.github.com/search/repositories?q=kubernetes" | \
  jq '.items[] | {name: .name, stars: .stargazers_count, language: .language}'
```

### Log Analysis
```bash
# Parse application logs (JSON format)
cat app.log | jq 'select(.level == "ERROR") | {timestamp: .timestamp, message: .message}'

# Count log levels
cat app.log | jq -r '.level' | sort | uniq -c

# Filter logs by time range
cat app.log | jq 'select(.timestamp >= "2024-01-01T00:00:00Z" and .timestamp <= "2024-01-01T23:59:59Z")'

# Extract specific fields from logs
cat access.log | jq '{ip: .remote_addr, method: .request_method, status: .status, size: .bytes_sent}'
```

### Configuration Management
```bash
# Extract database configuration
cat config.json | jq '.database | {host: .host, port: .port, name: .database}'

# Update configuration values
cat config.json | jq '.database.port = 5433' > new_config.json

# Merge configuration files
jq -s '.[0] * .[1]' base_config.json override_config.json

# Extract environment-specific config
cat config.json | jq '.environments.production'
```

## Advanced Operations

### Data Transformation
```bash
# Transform object structure
echo '{"users":{"john":{"age":30},"jane":{"age":25}}}' | \
  jq '.users | to_entries | map({name: .key, age: .value.age})'

# Group data
echo '[{"dept":"eng","name":"John"},{"dept":"eng","name":"Jane"},{"dept":"sales","name":"Bob"}]' | \
  jq 'group_by(.dept) | map({department: .[0].dept, employees: map(.name)})'

# Calculate aggregates
echo '[{"price":10},{"price":20},{"price":30}]' | \
  jq 'map(.price) | {total: add, average: (add/length), min: min, max: max}'
```

### Conditional Logic
```bash
# Conditional selection
echo '[{"name":"John","age":30},{"name":"Jane","age":17}]' | \
  jq 'map(if .age >= 18 then .status = "adult" else .status = "minor" end)'

# Multiple conditions
echo '[{"name":"John","score":85},{"name":"Jane","score":92}]' | \
  jq 'map(select(.score >= 90) | .grade = "A")'

# Default values
echo '{"name":"John"}' | jq '.age // "unknown"'
```

### String Operations
```bash
# String manipulation
echo '{"email":"john@example.com"}' | jq '.email | split("@") | .[0]'

# Regular expressions
echo '{"version":"v1.2.3"}' | jq '.version | test("v[0-9]+\\.[0-9]+\\.[0-9]+")'

# String formatting
echo '{"first":"John","last":"Doe"}' | jq '"\(.first) \(.last)"'
```

## Working with Files

### Processing Multiple Files
```bash
# Combine JSON files
jq -s '.[0] + .[1]' file1.json file2.json

# Process all JSON files in directory
find . -name "*.json" -exec jq '.name' {} \;

# Merge array from multiple files
jq -s 'map(.[]) | flatten' *.json
```

### Output Formats
```bash
# Raw output (no quotes)
echo '{"name":"John"}' | jq -r '.name'

# Compact output
echo '{"name": "John", "age": 30}' | jq -c .

# Tab-separated values
echo '[{"name":"John","age":30},{"name":"Jane","age":25}]' | \
  jq -r '.[] | [.name, .age] | @tsv'

# CSV output
echo '[{"name":"John","age":30},{"name":"Jane","age":25}]' | \
  jq -r '(.[0] | keys_unsorted) as $keys | $keys, (.[] | [.[$keys[]]])[] | @csv'
```

## Scripting with jq

### jq Scripts
```bash
# Create reusable script (extract_users.jq)
# File: extract_users.jq
.users[] | 
select(.active == true) | 
{
  name: .name,
  email: .email,
  last_login: .metadata.last_login
}

# Use script
cat users.json | jq -f extract_users.jq
```

### Functions and Variables
```bash
# Define variables
echo '[1,2,3,4,5]' | jq 'map(. as $x | $x * $x)'

# Custom functions
echo '[1,2,3,4,5]' | jq 'def square: . * .; map(square)'

# Complex processing
cat metrics.json | jq '
  .services[] | 
  .name as $service_name | 
  .metrics | 
  to_entries | 
  map({service: $service_name, metric: .key, value: .value})
'
```

## Performance Tips

### Efficient Processing
```bash
# Use streaming for large files
jq --stream 'select(.[0][0] == "users") | .[1]' large_file.json

# Limit output early
echo '[1,2,3,4,5,6,7,8,9,10]' | jq 'limit(3; .[])'  # First 3 elements

# Use map instead of repeated operations
echo '[1,2,3,4,5]' | jq 'map(. * 2)'  # Better than individual operations
```

## Common Patterns

### Error Handling
```bash
# Safe navigation
echo '{"user":{}}' | jq '.user.profile?.name // "No name"'

# Try-catch equivalent
echo '{"data":"invalid"}' | jq 'try .data.field catch "Field not found"'

# Type checking
echo '{"value":"123"}' | jq 'if (.value | type) == "string" then (.value | tonumber) else .value end'
```

## Great Resources

- [jq Manual](https://stedolan.github.io/jq/manual/) - Official comprehensive documentation
- [jq Tutorial](https://stedolan.github.io/jq/tutorial/) - Step-by-step learning guide
- [jq Cookbook](https://github.com/stedolan/jq/wiki/Cookbook) - Common jq recipes and patterns
- [jq Play](https://jqplay.org/) - Interactive jq playground for testing queries
- [awesome-jq](https://github.com/fiatjaf/awesome-jq) - Curated list of jq resources
- [jq Cheat Sheet](https://lzone.de/cheat-sheet/jq) - Quick reference for common operations
- [Advanced jq](https://github.com/stedolan/jq/wiki/Advanced-Features) - Documentation for advanced features