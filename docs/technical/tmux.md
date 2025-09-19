# tmux

## Overview

tmux (terminal multiplexer) is a powerful tool that allows you to manage multiple terminal sessions within a single window. It's essential for platform engineers working on remote servers, enabling persistent sessions, window management, and collaborative work.

## Key Features

- **Session Persistence**: Sessions survive disconnections
- **Multiple Windows**: Organize work into separate windows
- **Pane Splitting**: Split windows into multiple panes
- **Session Sharing**: Collaborate with team members
- **Customizable**: Extensive configuration options

## Basic Commands

### Session Management
```bash
# Start new session
tmux new-session -s mysession

# List sessions
tmux list-sessions
tmux ls

# Attach to session
tmux attach-session -t mysession
tmux a -t mysession

# Detach from session (inside tmux)
Ctrl-b d

# Kill session
tmux kill-session -t mysession
```

### Window Management
```bash
# Create new window
Ctrl-b c

# Switch between windows
Ctrl-b n    # Next window
Ctrl-b p    # Previous window
Ctrl-b 0-9  # Switch to window number

# Rename window
Ctrl-b ,

# List windows
Ctrl-b w

# Kill window
Ctrl-b &
```

### Pane Management
```bash
# Split panes
Ctrl-b %    # Split vertically
Ctrl-b "    # Split horizontally

# Navigate panes
Ctrl-b arrow keys

# Resize panes
Ctrl-b Alt-arrow keys

# Kill pane
Ctrl-b x

# Swap panes
Ctrl-b {    # Swap with previous
Ctrl-b }    # Swap with next
```

## Platform Engineering Workflows

### Development Environment Setup
```bash
# Create development session
tmux new-session -d -s dev

# Setup windows for different tasks
tmux new-window -t dev:1 -n 'editor'
tmux new-window -t dev:2 -n 'server'
tmux new-window -t dev:3 -n 'logs'
tmux new-window -t dev:4 -n 'tests'

# Send commands to windows
tmux send-keys -t dev:editor 'vim .' C-m
tmux send-keys -t dev:server 'npm run dev' C-m
tmux send-keys -t dev:logs 'tail -f logs/app.log' C-m

# Attach to session
tmux attach-session -t dev
```

### Production Monitoring
```bash
# Create monitoring session
tmux new-session -d -s monitoring

# Setup monitoring panes
tmux split-window -h
tmux split-window -v
tmux select-pane -t 0
tmux split-window -v

# Setup different monitoring tools in each pane
tmux send-keys -t monitoring:0.0 'htop' C-m
tmux send-keys -t monitoring:0.1 'tail -f /var/log/syslog' C-m
tmux send-keys -t monitoring:0.2 'kubectl get pods -w' C-m
tmux send-keys -t monitoring:0.3 'docker stats' C-m
```

### Deployment Script
```bash
#!/bin/bash
# deploy.sh - Automated deployment with tmux

SESSION="deployment"

# Kill existing session
tmux kill-session -t $SESSION 2>/dev/null

# Create new session
tmux new-session -d -s $SESSION

# Setup deployment environment
tmux rename-window -t $SESSION:0 'deploy'
tmux send-keys -t $SESSION:deploy 'echo "Starting deployment..."' C-m

# Create logs window
tmux new-window -t $SESSION:1 -n 'logs'
tmux send-keys -t $SESSION:logs 'kubectl logs -f deployment/myapp' C-m

# Create monitoring window
tmux new-window -t $SESSION:2 -n 'monitor'
tmux send-keys -t $SESSION:monitor 'kubectl get pods -w' C-m

# Run deployment in first window
tmux select-window -t $SESSION:deploy
tmux send-keys -t $SESSION:deploy './deploy-app.sh' C-m

# Attach to session
tmux attach-session -t $SESSION
```

## Configuration

### Basic .tmux.conf
```bash
# ~/.tmux.conf

# Change prefix key to Ctrl-a
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Split panes using | and -
bind | split-window -h
bind - split-window -v
unbind '"'
unbind %

# Reload config file
bind r source-file ~/.tmux.conf \; display-message "Config reloaded!"

# Enable mouse mode
set -g mouse on

# Start windows and panes at 1, not 0
set -g base-index 1
setw -g pane-base-index 1

# Status bar configuration
set -g status-bg black
set -g status-fg white
set -g status-left '[#S] '
set -g status-right '%Y-%m-%d %H:%M'

# Window status
setw -g window-status-current-style 'fg=black bg=white'
```

### Advanced Configuration
```bash
# ~/.tmux.conf - Advanced settings

# Increase scrollback buffer
set -g history-limit 10000

# Vim-like pane navigation
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Vim-like copy mode
setw -g mode-keys vi
bind-key -T copy-mode-vi v send-keys -X begin-selection
bind-key -T copy-mode-vi y send-keys -X copy-selection-and-cancel

# Pane resizing
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# Quick pane cycling
bind -r Tab select-pane -t :.+

# Rename session and window
bind A command-prompt -I '#S' "rename-session '%%'"
bind a command-prompt -I '#W' "rename-window '%%'"
```

## Advanced Features

### Session Scripts
```bash
#!/bin/bash
# create-dev-session.sh

SESSION_NAME="development"

# Check if session exists
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
    # Create new session
    tmux new-session -d -s $SESSION_NAME -x 120 -y 40
    
    # Window 1: Editor
    tmux rename-window -t $SESSION_NAME:0 'editor'
    tmux send-keys -t $SESSION_NAME:editor 'cd ~/projects/myapp && vim' C-m
    
    # Window 2: Server
    tmux new-window -t $SESSION_NAME:1 -n 'server'
    tmux send-keys -t $SESSION_NAME:server 'cd ~/projects/myapp && npm run dev' C-m
    
    # Window 3: Database
    tmux new-window -t $SESSION_NAME:2 -n 'database'
    tmux send-keys -t $SESSION_NAME:database 'psql myapp_development' C-m
    
    # Window 4: Terminal
    tmux new-window -t $SESSION_NAME:3 -n 'terminal'
    tmux send-keys -t $SESSION_NAME:terminal 'cd ~/projects/myapp' C-m
    
    # Select first window
    tmux select-window -t $SESSION_NAME:editor
fi

# Attach to session
tmux attach-session -t $SESSION_NAME
```

### Copy and Paste
```bash
# Enter copy mode
Ctrl-b [

# Navigate and select text (vi mode)
# Use h,j,k,l to move
# Space to start selection
# Enter to copy

# Paste
Ctrl-b ]

# Show paste buffers
Ctrl-b =

# Save buffer to file
tmux save-buffer ~/tmux-buffer.txt

# Load buffer from file
tmux load-buffer ~/tmux-buffer.txt
```

## Useful Plugins

### TPM (Tmux Plugin Manager)
```bash
# Install TPM
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Add to .tmux.conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

# Initialize TPM (add to bottom of .tmux.conf)
run '~/.tmux/plugins/tpm/tpm'

# Install plugins: Ctrl-b I
# Update plugins: Ctrl-b U
```

## Best Practices

- Use meaningful session and window names
- Create scripts for common session setups
- Use configuration for consistent behavior
- Learn keyboard shortcuts for efficiency
- Use sessions for different projects or contexts
- Detach instead of closing terminal windows
- Utilize copy mode for text manipulation

## Great Resources

- [tmux Manual](https://man.openbsd.org/tmux.1) - Official comprehensive manual
- [tmux Cheat Sheet](https://tmuxcheatsheet.com/) - Quick reference for commands and shortcuts
- [The Tao of tmux](https://leanpub.com/the-tao-of-tmux) - Comprehensive book on tmux mastery
- [tmux Plugin Manager](https://github.com/tmux-plugins/tpm) - Plugin ecosystem for tmux
- [awesome-tmux](https://github.com/rothgar/awesome-tmux) - Curated list of tmux resources
- [tmux Crash Course](https://thoughtbot.com/blog/a-tmux-crash-course) - Quick introduction tutorial
- [tmux Resurrect](https://github.com/tmux-plugins/tmux-resurrect) - Persist tmux sessions across restarts