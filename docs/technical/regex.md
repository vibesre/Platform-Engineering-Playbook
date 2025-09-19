# Regular Expressions

## Overview

Regular expressions (regex) are powerful pattern-matching tools essential for platform engineers. They're used for log analysis, configuration validation, data extraction, and text processing across various tools and programming languages.

## Key Features

- **Pattern Matching**: Find and match complex text patterns
- **Text Replacement**: Search and replace operations
- **Data Validation**: Validate input formats
- **Log Parsing**: Extract information from log files
- **Universal**: Supported across programming languages and tools

## Basic Syntax

### Character Classes
```regex
# Basic characters
.           # Matches any character except newline
\d          # Matches any digit (0-9)
\w          # Matches word characters (a-z, A-Z, 0-9, _)
\s          # Matches whitespace (space, tab, newline)

# Negated classes
\D          # Matches non-digits
\W          # Matches non-word characters
\S          # Matches non-whitespace

# Custom character classes
[abc]       # Matches a, b, or c
[a-z]       # Matches lowercase letters
[A-Z]       # Matches uppercase letters
[0-9]       # Matches digits
[^abc]      # Matches anything except a, b, or c
```

### Quantifiers
```regex
*           # Zero or more
+           # One or more
?           # Zero or one (optional)
{3}         # Exactly 3
{3,}        # 3 or more
{3,5}       # Between 3 and 5
{,5}        # Up to 5

# Non-greedy (lazy) quantifiers
*?          # Zero or more (non-greedy)
+?          # One or more (non-greedy)
??          # Zero or one (non-greedy)
```

### Anchors and Boundaries
```regex
^           # Start of string/line
$           # End of string/line
\b          # Word boundary
\B          # Non-word boundary
\A          # Start of string (multiline mode)
\Z          # End of string (multiline mode)
```

## Platform Engineering Use Cases

### Log Analysis
```bash
# Extract IP addresses from access logs
grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' access.log

# Find error entries
grep -E '\b(ERROR|FATAL|CRITICAL)\b' application.log

# Extract HTTP status codes
grep -oE 'HTTP/[0-9.]+ ([0-9]{3})' access.log

# Parse timestamp patterns
grep -E '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}' system.log

# Extract JSON fields from logs
grep -oE '"user_id":\s*"[^"]*"' app.log
```

### Configuration Validation
```python
import re

# Validate email addresses
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
def is_valid_email(email):
    return bool(re.match(email_pattern, email))

# Validate IP addresses
ip_pattern = r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$'
def is_valid_ip(ip):
    return bool(re.match(ip_pattern, ip))

# Validate Kubernetes resource names
k8s_name_pattern = r'^[a-z0-9]([-a-z0-9]*[a-z0-9])?$'
def is_valid_k8s_name(name):
    return bool(re.match(k8s_name_pattern, name)) and len(name) <= 253

# Validate semantic versions
semver_pattern = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
def is_valid_semver(version):
    return bool(re.match(semver_pattern, version))
```

### Data Extraction
```python
import re

def parse_nginx_log(log_line):
    # Nginx combined log format
    pattern = r'(\S+) \S+ \S+ \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+) "([^"]*)" "([^"]*)"'
    
    match = re.match(pattern, log_line)
    if match:
        return {
            'ip': match.group(1),
            'timestamp': match.group(2),
            'method': match.group(3),
            'path': match.group(4),
            'protocol': match.group(5),
            'status': int(match.group(6)),
            'size': int(match.group(7)),
            'referer': match.group(8),
            'user_agent': match.group(9)
        }
    return None

def extract_docker_info(docker_ps_output):
    # Extract container info from docker ps
    pattern = r'(\w+)\s+(\S+)\s+"([^"]+)"\s+(\S+\s+\S+)\s+(\S+)\s+(\S+)'
    
    containers = []
    for line in docker_ps_output.split('\n')[1:]:  # Skip header
        match = re.match(pattern, line)
        if match:
            containers.append({
                'id': match.group(1),
                'image': match.group(2),
                'command': match.group(3),
                'created': match.group(4),
                'status': match.group(5),
                'ports': match.group(6)
            })
    return containers

def parse_kubernetes_events(kubectl_output):
    # Parse kubectl get events output
    pattern = r'(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.+)'
    
    events = []
    for line in kubectl_output.split('\n')[1:]:
        match = re.match(pattern, line)
        if match:
            events.append({
                'last_seen': match.group(1),
                'type': match.group(2),
                'reason': match.group(3),
                'object': match.group(4),
                'subobject': match.group(5),
                'message': match.group(6)
            })
    return events
```

## Advanced Patterns

### Lookaheads and Lookbehinds
```regex
# Positive lookahead - match "foo" only if followed by "bar"
foo(?=bar)

# Negative lookahead - match "foo" only if NOT followed by "bar"
foo(?!bar)

# Positive lookbehind - match "bar" only if preceded by "foo"
(?<=foo)bar

# Negative lookbehind - match "bar" only if NOT preceded by "foo"
(?<!foo)bar

# Password validation (8+ chars, uppercase, lowercase, digit, special)
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
```

### Named Groups
```python
import re

# Extract structured data with named groups
log_pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<level>\w+) (?P<message>.*)'

def parse_app_log(log_line):
    match = re.match(log_pattern, log_line)
    if match:
        return match.groupdict()
    return None

# URL parsing
url_pattern = r'(?P<protocol>https?)://(?P<host>[^:/]+)(?::(?P<port>\d+))?(?P<path>/[^?]*)?(?:\?(?P<query>.*))?'

def parse_url(url):
    match = re.match(url_pattern, url)
    if match:
        return match.groupdict()
    return None

# Kubernetes resource reference
k8s_ref_pattern = r'(?P<namespace>[a-z0-9-]+)/(?P<kind>[a-zA-Z]+)/(?P<name>[a-z0-9-]+)'

def parse_k8s_reference(ref):
    match = re.match(k8s_ref_pattern, ref)
    if match:
        return match.groupdict()
    return None
```

## Language-Specific Examples

### Bash/Shell
```bash
#!/bin/bash

# Extract version from filename
extract_version() {
    local filename="$1"
    if [[ $filename =~ app-([0-9]+\.[0-9]+\.[0-9]+)\.tar\.gz ]]; then
        echo "${BASH_REMATCH[1]}"
    fi
}

# Validate environment names
validate_env() {
    local env="$1"
    if [[ $env =~ ^(dev|staging|prod)$ ]]; then
        echo "Valid environment: $env"
    else
        echo "Invalid environment: $env"
        return 1
    fi
}

# Parse key-value pairs
parse_config() {
    local config_file="$1"
    while IFS= read -r line; do
        if [[ $line =~ ^([A-Z_]+)=(.*)$ ]]; then
            key="${BASH_REMATCH[1]}"
            value="${BASH_REMATCH[2]}"
            echo "Setting $key=$value"
        fi
    done < "$config_file"
}
```

### Go
```go
package main

import (
    "fmt"
    "regexp"
    "time"
)

// Log entry structure
type LogEntry struct {
    Timestamp time.Time
    Level     string
    Service   string
    Message   string
}

// Parse structured logs
func parseLogEntry(logLine string) (*LogEntry, error) {
    pattern := `^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) (\w+) \[(\w+)\] (.+)$`
    re := regexp.MustCompile(pattern)
    
    matches := re.FindStringSubmatch(logLine)
    if len(matches) != 5 {
        return nil, fmt.Errorf("invalid log format")
    }
    
    timestamp, err := time.Parse(time.RFC3339, matches[1])
    if err != nil {
        return nil, err
    }
    
    return &LogEntry{
        Timestamp: timestamp,
        Level:     matches[2],
        Service:   matches[3],
        Message:   matches[4],
    }, nil
}

// Validate container names
func isValidContainerName(name string) bool {
    pattern := `^[a-zA-Z0-9][a-zA-Z0-9_.-]*$`
    re := regexp.MustCompile(pattern)
    return re.MatchString(name) && len(name) <= 255
}

// Extract metrics from Prometheus format
func parsePrometheusMetric(line string) (string, float64, map[string]string, error) {
    pattern := `^(\w+)(\{[^}]*\})?\s+([\d.]+)$`
    re := regexp.MustCompile(pattern)
    
    matches := re.FindStringSubmatch(line)
    if len(matches) < 4 {
        return "", 0, nil, fmt.Errorf("invalid metric format")
    }
    
    // Implementation details...
    return matches[1], 0, nil, nil
}
```

## Common Patterns for Platform Engineering

### Infrastructure Patterns
```regex
# AWS Resource ARNs
arn:aws:[\w-]+:[\w-]*:\d*:[\w-]+[:/][\w-./]+

# Kubernetes resource names
[a-z0-9]([-a-z0-9]*[a-z0-9])?

# Docker image tags
[\w.-]+/[\w.-]+:[\w.-]+

# IPv4 addresses
\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b

# IPv6 addresses
(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}

# MAC addresses
([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})

# HTTP URLs
https?://(?:[-\w.])+(?::[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])+)?(?:#(?:[\w.])+)?)?

# Semantic versions
^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?$
```

### Log Patterns
```regex
# Syslog format
^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+):\s+(.*)$

# Apache access log
^(\S+) \S+ \S+ \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+)

# JSON log entries
^\{.*"timestamp":\s*"([^"]+)".*"level":\s*"([^"]+)".*"message":\s*"([^"]+)".*\}$

# Kubernetes pod logs
^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)\s+(\w+)\s+(.*)$

# Error stack traces
^\s*at\s+([^\s]+)\s*\(([^:]+):(\d+):(\d+)\)$
```

## Tools and Testing

### Online Testing Tools
```bash
# Command line tools for regex testing
echo "test@example.com" | grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Using sed for replacements
echo "version-1.2.3" | sed 's/version-\([0-9.]*\)/v\1/'

# Using awk with regex
echo "user:12345:active" | awk -F: '/^user:/ {print "User ID:", $2}'
```

### Testing in Python
```python
import re

def test_regex_patterns():
    # Test email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    test_emails = ['valid@example.com', 'invalid.email', 'test@']
    
    for email in test_emails:
        if re.match(email_pattern, email):
            print(f"✓ {email} is valid")
        else:
            print(f"✗ {email} is invalid")
    
    # Test log parsing
    log_pattern = r'^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)$'
    test_logs = [
        '2024-01-01 10:30:00 INFO Application started',
        '2024-01-01 10:30:01 ERROR Database connection failed'
    ]
    
    for log in test_logs:
        match = re.match(log_pattern, log)
        if match:
            print(f"Date: {match.group(1)}, Time: {match.group(2)}, Level: {match.group(3)}")

test_regex_patterns()
```

## Best Practices

- Start simple and build complexity gradually
- Use online regex testers for validation
- Comment complex patterns for maintainability
- Use raw strings in Python (`r''`) to avoid escaping issues
- Test with edge cases and invalid input
- Consider performance for large datasets
- Use named groups for better readability
- Escape special characters when matching literally

## Great Resources

- [RegExr](https://regexr.com/) - Interactive regex tester with explanations
- [Regex101](https://regex101.com/) - Online regex debugger and tester
- [RegexPal](https://www.regexpal.com/) - Simple online regex tester
- [Regex Crossword](https://regexcrossword.com/) - Learn regex through puzzles
- [Regular Expressions Info](https://www.regular-expressions.info/) - Comprehensive regex tutorial
- [MDN Regex Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions) - JavaScript regex reference
- [Python re Module](https://docs.python.org/3/library/re.html) - Official Python regex documentation