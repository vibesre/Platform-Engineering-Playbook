# Visual Studio Code

## Overview

Visual Studio Code (VS Code) is a lightweight, powerful source code editor that has become essential for platform engineers. It offers excellent support for multiple programming languages, integrated terminal, debugging capabilities, and a rich ecosystem of extensions.

## Key Features

- **Multi-language Support**: Syntax highlighting and IntelliSense for numerous languages
- **Integrated Terminal**: Built-in command line interface
- **Git Integration**: Source control management
- **Extension Ecosystem**: Thousands of available extensions
- **Remote Development**: Work on remote servers and containers

## Essential Extensions for Platform Engineers

### Development Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "golang.go", 
    "rust-lang.rust-analyzer",
    "ms-vscode.vscode-typescript-next",
    "redhat.vscode-yaml",
    "ms-kubernetes-tools.vscode-kubernetes-tools",
    "ms-azuretools.vscode-docker",
    "hashicorp.terraform",
    "redhat.ansible",
    "ms-vscode-remote.remote-ssh",
    "ms-vscode-remote.remote-containers"
  ]
}
```

### Infrastructure and DevOps Extensions
```bash
# Install via CLI
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension ms-azuretools.vscode-docker
code --install-extension hashicorp.terraform
code --install-extension redhat.ansible
code --install-extension ms-vscode.azure-account
code --install-extension amazonwebservices.aws-toolkit-vscode
code --install-extension googlecloudtools.cloudcode
```

## Configuration

### User Settings
```json
{
  // Editor settings
  "editor.fontSize": 14,
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.rulers": [80, 120],
  "editor.minimap.enabled": false,
  "editor.bracketPairColorization.enabled": true,
  
  // File settings
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  
  // Terminal settings
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.shell.linux": "/bin/bash",
  "terminal.integrated.copyOnSelection": true,
  
  // Language-specific settings
  "[yaml]": {
    "editor.tabSize": 2,
    "editor.autoIndent": "advanced"
  },
  "[python]": {
    "editor.tabSize": 4,
    "editor.insertSpaces": true
  },
  "[go]": {
    "editor.tabSize": 4,
    "editor.insertSpaces": false
  },
  
  // Git settings
  "git.autofetch": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true,
  
  // Docker settings
  "docker.showStartPage": false,
  
  // Kubernetes settings
  "vs-kubernetes": {
    "vs-kubernetes.kubectl-path": "/usr/local/bin/kubectl",
    "vs-kubernetes.helm-path": "/usr/local/bin/helm"
  }
}
```

### Workspace Settings for Platform Projects
```json
{
  "folders": [
    {
      "name": "Infrastructure",
      "path": "./terraform"
    },
    {
      "name": "Kubernetes",
      "path": "./k8s"
    },
    {
      "name": "Ansible",
      "path": "./ansible"
    },
    {
      "name": "Scripts",
      "path": "./scripts"
    }
  ],
  "settings": {
    "files.exclude": {
      "**/.terraform": true,
      "**/node_modules": true,
      "**/.git": true
    },
    "search.exclude": {
      "**/.terraform": true,
      "**/node_modules": true
    }
  },
  "extensions": {
    "recommendations": [
      "hashicorp.terraform",
      "ms-kubernetes-tools.vscode-kubernetes-tools",
      "redhat.ansible",
      "ms-azuretools.vscode-docker"
    ]
  }
}
```

## Platform Engineering Workflows

### Kubernetes Development
```yaml
# .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "kubectl apply",
      "type": "shell",
      "command": "kubectl",
      "args": ["apply", "-f", "${file}"],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      }
    },
    {
      "label": "kubectl validate",
      "type": "shell",
      "command": "kubectl",
      "args": ["apply", "--dry-run=client", "-f", "${file}"],
      "group": "test"
    },
    {
      "label": "helm lint",
      "type": "shell",
      "command": "helm",
      "args": ["lint", "${workspaceFolder}"],
      "group": "test"
    }
  ]
}
```

### Terraform Development
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "terraform plan",
      "type": "shell",
      "command": "terraform",
      "args": ["plan"],
      "group": "build",
      "options": {
        "cwd": "${workspaceFolder}/terraform"
      }
    },
    {
      "label": "terraform apply",
      "type": "shell", 
      "command": "terraform",
      "args": ["apply", "-auto-approve"],
      "group": "build",
      "options": {
        "cwd": "${workspaceFolder}/terraform"
      }
    },
    {
      "label": "terraform validate",
      "type": "shell",
      "command": "terraform",
      "args": ["validate"],
      "group": "test",
      "options": {
        "cwd": "${workspaceFolder}/terraform"
      }
    }
  ]
}
```

### Docker Development
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "docker build",
      "type": "docker-build",
      "dockerBuild": {
        "dockerfile": "${workspaceFolder}/Dockerfile",
        "context": "${workspaceFolder}",
        "tag": "myapp:latest"
      }
    },
    {
      "label": "docker run",
      "type": "docker-run",
      "dependsOn": ["docker build"],
      "dockerRun": {
        "image": "myapp:latest",
        "ports": [
          {
            "hostPort": 8080,
            "containerPort": 8080
          }
        ],
        "remove": true
      }
    }
  ]
}
```

## Remote Development

### SSH Remote Development
```json
// .ssh/config
Host production-server
    HostName prod.example.com
    User admin
    IdentityFile ~/.ssh/id_rsa
    ForwardAgent yes

Host staging-server
    HostName staging.example.com
    User admin
    IdentityFile ~/.ssh/id_rsa
    ProxyJump bastion.example.com

// VS Code settings for remote
{
  "remote.SSH.remotePlatform": {
    "production-server": "linux",
    "staging-server": "linux"
  },
  "remote.SSH.showLoginTerminal": true,
  "remote.SSH.connectTimeout": 60
}
```

### Container Development
```json
// .devcontainer/devcontainer.json
{
  "name": "Platform Engineering Environment",
  "image": "mcr.microsoft.com/vscode/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {},
    "ghcr.io/devcontainers/features/terraform:1": {},
    "ghcr.io/devcontainers/features/aws-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-kubernetes-tools.vscode-kubernetes-tools",
        "hashicorp.terraform",
        "ms-azuretools.vscode-docker",
        "redhat.ansible"
      ]
    }
  },
  "postCreateCommand": "pip install ansible boto3 kubernetes",
  "remoteUser": "vscode"
}
```

## Debugging and Testing

### Python Debugging
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["${workspaceFolder}/tests"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Go Debugging
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch Go Program",
      "type": "go",
      "request": "launch",
      "mode": "auto",
      "program": "${workspaceFolder}",
      "env": {},
      "args": []
    },
    {
      "name": "Debug Go Tests",
      "type": "go",
      "request": "launch",
      "mode": "test",
      "program": "${workspaceFolder}"
    }
  ]
}
```

## Snippets for Platform Engineering

### Kubernetes Snippets
```json
// .vscode/kubernetes.code-snippets
{
  "Kubernetes Deployment": {
    "prefix": "k8s-deployment",
    "body": [
      "apiVersion: apps/v1",
      "kind: Deployment",
      "metadata:",
      "  name: ${1:app-name}",
      "  labels:",
      "    app: ${1:app-name}",
      "spec:",
      "  replicas: ${2:3}",
      "  selector:",
      "    matchLabels:",
      "      app: ${1:app-name}",
      "  template:",
      "    metadata:",
      "      labels:",
      "        app: ${1:app-name}",
      "    spec:",
      "      containers:",
      "      - name: ${1:app-name}",
      "        image: ${3:nginx:latest}",
      "        ports:",
      "        - containerPort: ${4:80}",
      "        resources:",
      "          requests:",
      "            memory: \"${5:64Mi}\"",
      "            cpu: \"${6:250m}\"",
      "          limits:",
      "            memory: \"${7:128Mi}\"",
      "            cpu: \"${8:500m}\""
    ],
    "description": "Create a Kubernetes Deployment"
  }
}
```

### Terraform Snippets
```json
{
  "Terraform Resource": {
    "prefix": "tf-resource",
    "body": [
      "resource \"${1:aws_instance}\" \"${2:example}\" {",
      "  ${3:ami}           = \"${4:ami-12345678}\"",
      "  ${5:instance_type} = \"${6:t2.micro}\"",
      "",
      "  tags = {",
      "    Name = \"${7:Example}\"",
      "    Environment = \"${8:dev}\"",
      "  }",
      "}"
    ],
    "description": "Create a Terraform resource"
  }
}
```

## Integrated Terminal Usage

### Terminal Profiles
```json
{
  "terminal.integrated.profiles.linux": {
    "bash": {
      "path": "bash",
      "icon": "terminal-bash"
    },
    "kubectl": {
      "path": "bash",
      "args": ["-c", "kubectl get pods && exec bash"],
      "icon": "server-environment"
    },
    "docker": {
      "path": "bash", 
      "args": ["-c", "docker ps && exec bash"],
      "icon": "docker"
    }
  },
  "terminal.integrated.defaultProfile.linux": "bash"
}
```

### Useful Terminal Commands
```bash
# Quick commands for platform engineering
alias k='kubectl'
alias tf='terraform'
alias d='docker'
alias dc='docker-compose'

# Common kubectl shortcuts
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias kdp='kubectl describe pod'

# Git shortcuts
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
```

## Productivity Tips

### Multi-cursor Editing
- `Ctrl+Alt+Down`: Add cursor below
- `Ctrl+Alt+Up`: Add cursor above
- `Ctrl+D`: Select next occurrence
- `Ctrl+Shift+L`: Select all occurrences

### File Navigation
- `Ctrl+P`: Quick file open
- `Ctrl+Shift+P`: Command palette
- `Ctrl+Shift+E`: Explorer
- `Ctrl+Shift+F`: Search across files
- `Ctrl+G`: Go to line

### Code Navigation
- `F12`: Go to definition
- `Alt+F12`: Peek definition
- `Shift+F12`: Find all references
- `Ctrl+Shift+O`: Go to symbol in file

## Best Practices

- Use workspace-specific settings for different project types
- Set up consistent code formatting and linting
- Utilize remote development for secure server access
- Create custom snippets for frequently used patterns
- Configure debug profiles for different environments
- Use integrated source control for version management
- Leverage extensions for specific technologies
- Set up proper file associations and syntax highlighting

## Great Resources

- [VS Code Documentation](https://code.visualstudio.com/docs) - Official comprehensive documentation
- [VS Code Extensions Marketplace](https://marketplace.visualstudio.com/vscode) - Thousands of extensions
- [VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview) - Remote development guide
- [VS Code Keyboard Shortcuts](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-linux.pdf) - Productivity shortcuts
- [VS Code Settings Sync](https://code.visualstudio.com/docs/editor/settings-sync) - Sync settings across devices
- [awesome-vscode](https://github.com/viatsko/awesome-vscode) - Curated list of VS Code resources
- [VS Code Tips and Tricks](https://code.visualstudio.com/docs/getstarted/tips-and-tricks) - Productivity tips