---
sidebar_position: 4
---

# Bash Scripting

Master shell scripting for automation and system administration.

## Bash Fundamentals

### Script Structure
```bash
#!/bin/bash
# Script description
set -euo pipefail  # Error handling
```

### Variables and Parameters
- Variable assignment
- Special variables ($@, $#, $?)
- Parameter expansion
- Arrays and associative arrays

## Control Structures

### Conditionals
```bash
if [[ condition ]]; then
    # commands
elif [[ condition ]]; then
    # commands
else
    # commands
fi
```

### Loops
```bash
# For loops
for item in list; do
    # commands
done

# While loops
while [[ condition ]]; do
    # commands
done
```

## Functions

### Function Definition
```bash
function_name() {
    local var="$1"
    # function body
    return 0
}
```

### Best Practices
- Use local variables
- Return meaningful exit codes
- Document parameters
- Handle errors gracefully

## Advanced Features

### Process Substitution
```bash
diff <(command1) <(command2)
```

### Command Substitution
```bash
result=$(command)
result=`command`  # Legacy
```

## Error Handling

### Exit Codes
- Check command success
- Custom exit codes
- Trap signals
- Cleanup on exit

### Debugging
```bash
set -x  # Debug mode
set -v  # Verbose mode
```

## Practical Examples

### System Administration
- Log rotation scripts
- Backup automation
- User management
- Service monitoring

### DevOps Tasks
- Deployment scripts
- Environment setup
- Health checks
- CI/CD integration