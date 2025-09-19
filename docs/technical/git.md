# Git - Distributed Version Control Fundamentals

## Overview

Git is a distributed version control system designed for speed, data integrity, and support for distributed, non-linear workflows. Created by Linus Torvalds in 2005, Git has become the de facto standard for version control in modern software development.

## Core Concepts

### Repository Structure

Git stores data as a series of snapshots of a miniature filesystem:

```
.git/
├── objects/       # Database of all files, commits, trees
├── refs/          # References to commits (branches, tags)
├── HEAD           # Pointer to current branch
├── config         # Repository configuration
├── hooks/         # Scripts triggered by Git events
└── index          # Staging area
```

### Three States of Files

1. **Modified**: Changed but not staged
2. **Staged**: Marked for inclusion in next commit
3. **Committed**: Safely stored in local database

### Git Objects

```bash
# Blob: File content
$ git hash-object -w file.txt
e69de29bb2d1d6434b8b29ae775ad8c2e48c5391

# Tree: Directory structure
$ git write-tree
4b825dc642cb6eb9a060e54bf8d69288fbee4904

# Commit: Snapshot with metadata
$ git commit-tree <tree-sha> -m "Initial commit"
```

## Essential Commands

### Repository Initialization

```bash
# Create new repository
git init

# Clone existing repository
git clone https://github.com/user/repo.git

# Clone with specific branch
git clone -b develop https://github.com/user/repo.git

# Shallow clone (limited history)
git clone --depth 1 https://github.com/user/repo.git
```

### Basic Workflow

```bash
# Check status
git status

# Stage changes
git add file.txt                  # Single file
git add .                         # All changes
git add -p                        # Interactive staging
git add *.js                      # Pattern matching

# Commit changes
git commit -m "Add feature"
git commit -am "Fix bug"          # Stage and commit
git commit --amend                # Modify last commit

# View history
git log
git log --oneline --graph --all
git log --since="2 weeks ago"
git log --author="John"
git log -p                        # Show patches
```

### Branching and Merging

```bash
# Branch management
git branch                        # List branches
git branch feature-x              # Create branch
git checkout feature-x            # Switch branch
git checkout -b feature-y         # Create and switch
git branch -d feature-x           # Delete branch
git branch -D feature-x           # Force delete

# Merging
git merge feature-x               # Merge branch
git merge --no-ff feature-x       # No fast-forward
git merge --squash feature-x      # Squash commits

# Rebasing
git rebase main                   # Rebase onto main
git rebase -i HEAD~3             # Interactive rebase
```

### Remote Operations

```bash
# Remote management
git remote -v                     # List remotes
git remote add upstream <url>     # Add remote
git remote remove origin          # Remove remote
git remote set-url origin <url>   # Change URL

# Fetching and pulling
git fetch origin                  # Fetch changes
git pull origin main              # Fetch and merge
git pull --rebase origin main     # Fetch and rebase

# Pushing
git push origin main              # Push to remote
git push -u origin feature-x      # Set upstream
git push --force                  # Force push (danger!)
git push --force-with-lease       # Safer force push
```

## Practical Workflows

### Feature Branch Workflow

```bash
# 1. Create feature branch
git checkout -b feature/user-authentication

# 2. Make changes and commit
git add src/auth.js
git commit -m "Add authentication module"

# 3. Keep branch updated
git checkout main
git pull origin main
git checkout feature/user-authentication
git rebase main

# 4. Push and create pull request
git push -u origin feature/user-authentication

# 5. After merge, clean up
git checkout main
git pull origin main
git branch -d feature/user-authentication
git push origin --delete feature/user-authentication
```

### Gitflow Workflow

```bash
# Initialize gitflow
git flow init

# Feature development
git flow feature start new-feature
# ... make changes ...
git flow feature finish new-feature

# Release process
git flow release start 1.0.0
# ... finalize release ...
git flow release finish 1.0.0

# Hotfix
git flow hotfix start critical-fix
# ... fix issue ...
git flow hotfix finish critical-fix
```

### Commit Message Best Practices

```bash
# Good commit message format
<type>(<scope>): <subject>

<body>

<footer>

# Example
feat(auth): Add JWT token validation

- Implement token verification middleware
- Add expiration check
- Include role-based permissions

Closes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code restructuring
- `test`: Test changes
- `chore`: Build/auxiliary changes

## Configuration

### Global Configuration

```bash
# User identity
git config --global user.name "John Doe"
git config --global user.email "john@example.com"

# Editor
git config --global core.editor "vim"

# Aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# Line endings
git config --global core.autocrlf true  # Windows
git config --global core.autocrlf input # Mac/Linux

# Default branch name
git config --global init.defaultBranch main
```

### Repository Configuration

```bash
# .gitignore
node_modules/
*.log
.env
dist/
.DS_Store
*.swp

# .gitattributes
*.jpg binary
*.png binary
*.pdf binary
*.sh text eol=lf
*.bat text eol=crlf
```

## Collaboration Patterns

### Pull Request Workflow

1. **Fork and Clone**
```bash
# Fork on GitHub, then:
git clone https://github.com/yourusername/repo.git
git remote add upstream https://github.com/original/repo.git
```

2. **Create Feature Branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Keep Fork Updated**
```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

4. **Submit Pull Request**
```bash
git push origin feature/amazing-feature
# Create PR on GitHub
```

### Code Review Process

```bash
# Fetch PR locally for review
git fetch origin pull/123/head:pr-123
git checkout pr-123

# Review and test
# Provide feedback on PR

# Merge strategies
git checkout main
git merge --no-ff pr-123        # Preserve history
git merge --squash pr-123       # Clean history
```

## Troubleshooting

### Common Issues

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Recover deleted branch
git reflog
git checkout -b recovered-branch <sha>

# Fix detached HEAD
git checkout main

# Remove untracked files
git clean -fd

# Stash changes
git stash
git stash pop
git stash list
git stash apply stash@{2}

# Cherry-pick commit
git cherry-pick <commit-sha>

# Find lost commits
git fsck --lost-found
```

### Merge Conflicts

```bash
# During merge conflict
<<<<<<< HEAD
Current changes
=======
Incoming changes
>>>>>>> feature-branch

# Resolution process
# 1. Edit files to resolve conflicts
# 2. Stage resolved files
git add resolved-file.txt
# 3. Complete merge
git commit

# Abort merge
git merge --abort
```

## Security Best Practices

### Sensitive Data

```bash
# Remove sensitive data from history
git filter-branch --tree-filter 'rm -f passwords.txt' HEAD

# Using BFG Repo-Cleaner (faster)
bfg --delete-files passwords.txt
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Prevent commits with secrets
# .gitleaks.toml configuration
title = "Gitleaks Config"
[[rules]]
  description = "AWS Access Key"
  regex = '''AKIA[0-9A-Z]{16}'''
  tags = ["key", "AWS"]
```

### Signed Commits

```bash
# Configure GPG signing
git config --global user.signingkey <key-id>
git config --global commit.gpgsign true

# Sign commits
git commit -S -m "Signed commit"

# Verify signatures
git log --show-signature
git verify-commit <commit-sha>
```

## Performance Optimization

### Large Repositories

```bash
# Enable partial clone
git clone --filter=blob:none <url>

# Sparse checkout
git sparse-checkout init --cone
git sparse-checkout set src/frontend

# Garbage collection
git gc --aggressive --prune=now

# Pack optimization
git repack -a -d -f --depth=250 --window=250

# Performance config
git config core.preloadindex true
git config core.fscache true
git config gc.auto 256
```

### Git LFS (Large File Storage)

```bash
# Install and initialize
git lfs install
git lfs track "*.psd"
git lfs track "*.zip"
git add .gitattributes

# Clone with LFS
git lfs clone <repository-url>

# Fetch LFS objects
git lfs fetch
git lfs pull
```

## Integration Examples

### Pre-commit Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run tests
npm test
if [ $? -ne 0 ]; then
  echo "Tests failed. Commit aborted."
  exit 1
fi

# Check for console.log
if git diff --cached | grep -q "console\.log"; then
  echo "console.log found. Commit aborted."
  exit 1
fi

# Format code
npm run format
git add -A
```

### CI/CD Integration

```yaml
# .github/workflows/main.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          npm install
          npm test
```

## Production Patterns

### Release Management

```bash
# Semantic versioning tags
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# List tags
git tag -l "v1.*"

# Checkout specific version
git checkout v1.0.0

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

### Monorepo Strategies

```bash
# Subtree management
git subtree add --prefix=libs/shared https://github.com/org/shared.git main
git subtree pull --prefix=libs/shared https://github.com/org/shared.git main
git subtree push --prefix=libs/shared https://github.com/org/shared.git main

# Submodule management
git submodule add https://github.com/org/lib.git libs/external
git submodule update --init --recursive
git submodule foreach git pull origin main
```

## Monitoring and Analytics

```bash
# Contribution statistics
git shortlog -sn
git log --format='%aN' | sort | uniq -c | sort -rn

# Code churn
git log --stat --oneline

# File history
git log --follow -p -- path/to/file

# Blame analysis
git blame -L 10,20 file.js
git blame -w -M -C file.js  # Ignore whitespace, detect moves/copies

# Repository size
git count-objects -vH
```

## Best Practices Summary

1. **Commit Often**: Make small, focused commits
2. **Write Clear Messages**: Use conventional commit format
3. **Branch Strategically**: Use feature branches
4. **Pull Before Push**: Keep your branch updated
5. **Review Before Merge**: Use pull requests
6. **Tag Releases**: Use semantic versioning
7. **Backup Important Branches**: Push to remote regularly
8. **Clean History**: Use interactive rebase wisely
9. **Document Workflows**: Maintain clear README
10. **Automate Checks**: Use hooks and CI/CD

## Resources

- [Pro Git Book](https://git-scm.com/book)
- [Git Documentation](https://git-scm.com/docs)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)