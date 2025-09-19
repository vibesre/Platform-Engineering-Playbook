# Git Advanced - Advanced Git Techniques and Internals

## Overview

This guide covers advanced Git techniques, internal mechanisms, and expert-level workflows for power users and teams requiring sophisticated version control strategies.

## Git Internals

### Object Database

Git uses a content-addressable filesystem with four object types:

```bash
# Examine object types
git cat-file -t <sha>  # blob, tree, commit, tag

# View object content
git cat-file -p <sha>

# Create objects manually
echo "Hello, Git!" | git hash-object -w --stdin
# Returns: 980a0d5f19a64b4b30a87d4206aade58726b60e3

# Inspect objects directory
find .git/objects -type f | head -5
```

### The Object Model

```bash
# Blob (file content)
$ git hash-object README.md
e69de29bb2d1d6434b8b29ae775ad8c2e48c5391

# Tree (directory listing)
$ git ls-tree HEAD
100644 blob e69de29  README.md
040000 tree 4b825dc  src/

# Commit structure
$ git cat-file -p HEAD
tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904
parent 3a5fb8e7a2b4e3c1d5f6g7h8i9j0k1l2m3n4o5p6
author John Doe <john@example.com> 1622476800 +0000
committer John Doe <john@example.com> 1622476800 +0000

Initial commit
```

### Pack Files

```bash
# View pack files
ls -la .git/objects/pack/

# Verify pack integrity
git verify-pack -v .git/objects/pack/pack-*.idx

# Manually trigger packing
git gc --aggressive

# Unpack objects (rarely needed)
git unpack-objects < .git/objects/pack/pack-*.pack

# Analyze pack efficiency
git count-objects -v
```

### References and Reflog

```bash
# Direct reference manipulation
git update-ref refs/heads/experiment HEAD
git symbolic-ref HEAD refs/heads/experiment

# Reflog examination
git reflog show --all
git reflog expire --expire=now --all
git reflog delete HEAD@{2}

# Recover lost commits
git fsck --full --no-reflogs --unreachable --lost-found
git show <lost-commit-sha>
git merge <lost-commit-sha>
```

## Advanced Merging Strategies

### Merge Strategies

```bash
# Recursive (default) - handles renames
git merge -s recursive feature

# Ours - keep our version entirely
git merge -s ours obsolete-branch

# Octopus - merge multiple branches
git merge feature-1 feature-2 feature-3

# Subtree - merge as subdirectory
git merge -s subtree --allow-unrelated-histories sub-project

# Custom merge driver
# .gitattributes
*.generated merge=ours

# .git/config
[merge "ours"]
    driver = true
```

### Three-way Merge Internals

```bash
# Manual three-way merge
git merge-base HEAD feature-branch
# Returns: <common-ancestor-sha>

# View merge conflicts in three-way
git config merge.conflictstyle diff3

# During conflict:
<<<<<<< HEAD (current change)
Current code
||||||| merged common ancestors
Original code
=======
Incoming code
>>>>>>> feature-branch (incoming change)
```

### Advanced Conflict Resolution

```bash
# Resolve using specific version
git checkout --ours path/to/file
git checkout --theirs path/to/file

# Use merge tool
git mergetool --tool=vimdiff

# Rerere (Reuse Recorded Resolution)
git config rerere.enabled true
git rerere status
git rerere diff
git rerere forget path/to/file
```

## Interactive Rebase Mastery

### Advanced Interactive Rebase

```bash
# Complex rebase operations
git rebase -i --root  # Rebase all history
git rebase -i HEAD~10 --autosquash
git rebase -i --exec "npm test" HEAD~5

# Rebase script commands:
# p, pick - use commit
# r, reword - use commit, edit message
# e, edit - use commit, stop for amending
# s, squash - use commit, meld into previous
# f, fixup - like squash, discard message
# x, exec - run command
# b, break - stop here
# d, drop - remove commit
# l, label - label current HEAD
# t, reset - reset HEAD to label
# m, merge - create merge commit
```

### Autosquash Workflow

```bash
# Create fixup commits
git commit --fixup=<commit-sha>
git commit --squash=<commit-sha>

# Automatically organize during rebase
git rebase -i --autosquash HEAD~10

# Configure as default
git config rebase.autosquash true
```

### Advanced Rebase Scenarios

```bash
# Rebase with merge commits
git rebase -r main  # --rebase-merges

# Rebase onto different base
git rebase --onto main feature-old feature-new

# Interactive rebase with exec
git rebase -i --exec "make test" HEAD~3

# Split commits
# 1. Mark commit as 'edit' in rebase
# 2. git reset HEAD^
# 3. git add -p  # Stage parts
# 4. git commit
# 5. Repeat for other parts
# 6. git rebase --continue
```

## Advanced Cherry-picking

### Cherry-pick Options

```bash
# Cherry-pick with options
git cherry-pick -x <commit>  # Add source reference
git cherry-pick -e <commit>  # Edit message
git cherry-pick -s <commit>  # Add signoff
git cherry-pick -n <commit>  # No commit

# Cherry-pick range
git cherry-pick A..B         # Commits after A up to B
git cherry-pick A^..B        # Include A

# Cherry-pick merge commits
git cherry-pick -m 1 <merge-commit>

# Multiple cherry-picks
git cherry-pick <commit1> <commit2> <commit3>
```

### Cherry-pick Workflows

```bash
# Backporting fixes
git checkout release-1.0
git cherry-pick main~3
git cherry-pick -x main~2  # With reference

# Moving commits between branches
git checkout feature-b
git cherry-pick feature-a~3..feature-a
git checkout feature-a
git reset --hard HEAD~3
```

## Bisecting and Debugging

### Git Bisect

```bash
# Start bisect
git bisect start
git bisect bad HEAD
git bisect good v1.0

# Automated bisect
git bisect run npm test

# Bisect with custom script
cat > test_regression.sh << 'EOF'
#!/bin/bash
make && ./run_test.sh
EOF
chmod +x test_regression.sh
git bisect run ./test_regression.sh

# Skip commits
git bisect skip

# Visualize bisect
git bisect visualize

# End bisect
git bisect reset
```

### Advanced Blame Analysis

```bash
# Blame with line ranges
git blame -L 10,20 file.js
git blame -L :function_name file.js

# Ignore whitespace and refactoring
git blame -w -M -C file.js

# Blame through renames
git blame --follow file.js

# Interactive blame in vim
# :Gblame in fugitive.vim

# Blame with commit ranges
git blame v1.0..v2.0 -- file.js
```

### Git Grep Advanced

```bash
# Search with context
git grep -n -B2 -A2 "pattern"

# Search specific file types
git grep "TODO" -- "*.js" "*.ts"

# Search in specific commits
git grep "pattern" HEAD~10
git grep "pattern" $(git rev-list --all)

# Boolean expressions
git grep -e "pattern1" --and -e "pattern2"
git grep -e "pattern1" --or -e "pattern2"
git grep --all-match -e "pattern1" -e "pattern2"

# Function/class search
git grep -p "def.*function_name" *.py
```

## Submodules Advanced

### Submodule Management

```bash
# Add submodule with branch tracking
git submodule add -b main https://github.com/org/lib libs/lib
git submodule set-branch --branch develop libs/lib

# Update all submodules
git submodule update --init --recursive --remote

# Foreach operations
git submodule foreach 'git checkout main && git pull'
git submodule foreach --recursive 'git status'

# Moving submodules
git mv old/path/submodule new/path/submodule

# Removing submodules properly
git submodule deinit -f path/to/submodule
rm -rf .git/modules/path/to/submodule
git rm -f path/to/submodule
```

### Submodule Workflows

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/org/project

# Work within submodule
cd libs/submodule
git checkout -b feature
# ... make changes ...
git commit -am "Update submodule"
git push origin feature

# Update parent repository
cd ../..
git add libs/submodule
git commit -m "Update submodule reference"

# Diff submodules
git diff --submodule
git config diff.submodule log
```

## Worktrees

### Multiple Working Trees

```bash
# Add worktree
git worktree add ../project-hotfix hotfix
git worktree add -b new-feature ../project-feature main

# List worktrees
git worktree list

# Work in worktree
cd ../project-hotfix
# ... make changes ...
git commit -am "Fix critical bug"

# Remove worktree
git worktree remove ../project-hotfix
git worktree prune

# Lock worktree
git worktree lock ../project-feature
git worktree unlock ../project-feature
```

### Worktree Use Cases

```bash
# Parallel development
git worktree add ../app-v2 develop
git worktree add ../app-v1-hotfix v1-maintenance

# Building different versions
git worktree add ../build-stable stable
git worktree add ../build-beta beta

# Code review
git worktree add ../review-pr-123 origin/pr/123
```

## Advanced Stashing

### Stash Operations

```bash
# Stash with message
git stash push -m "WIP: Feature implementation"

# Partial stash
git stash push -p
git stash push -- src/specific-file.js

# Include untracked files
git stash push -u
git stash push --include-untracked

# Keep index
git stash push --keep-index

# Create branch from stash
git stash branch feature-from-stash stash@{0}
```

### Stash Management

```bash
# List stashes with details
git stash list --oneline --name-status

# Show stash content
git stash show -p stash@{2}

# Apply specific file from stash
git checkout stash@{0} -- path/to/file

# Clear old stashes
git reflog expire --expire-unreachable=now refs/stash
git stash clear
```

## Git Hooks Advanced

### Server-side Hooks

```bash
#!/bin/bash
# pre-receive hook
while read oldrev newrev refname; do
    # Enforce commit message format
    commits=$(git rev-list $oldrev..$newrev)
    for commit in $commits; do
        msg=$(git log -1 --pretty=%B $commit)
        if ! echo "$msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+"; then
            echo "Commit $commit has invalid message format"
            exit 1
        fi
    done
    
    # Check file size
    files=$(git diff --name-only $oldrev..$newrev)
    for file in $files; do
        size=$(git cat-file -s "$newrev:$file" 2>/dev/null || echo 0)
        if [ $size -gt 10485760 ]; then  # 10MB
            echo "File $file exceeds size limit"
            exit 1
        fi
    done
done
```

### Client-side Hook Examples

```bash
#!/bin/bash
# prepare-commit-msg - Add ticket number
BRANCH=$(git symbolic-ref --short HEAD)
TICKET=$(echo "$BRANCH" | grep -oE '[A-Z]+-[0-9]+')

if [ -n "$TICKET" ]; then
    sed -i.bak -e "1s/^/$TICKET: /" "$1"
fi

# commit-msg - Validate format
#!/bin/bash
commit_regex='^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}'
if ! grep -qE "$commit_regex" "$1"; then
    echo "Invalid commit message format"
    exit 1
fi

# post-checkout - Install dependencies
#!/bin/bash
if [ "$3" = "1" ]; then  # Branch checkout
    if [ -f package.json ]; then
        npm install
    fi
fi
```

## Performance Optimization

### Git Performance Config

```bash
# Core performance settings
git config core.preloadindex true
git config core.fscache true
git config core.untrackedCache true
git config feature.manyFiles true

# Protocol version
git config protocol.version 2

# Parallel processing
git config index.threads true
git config pack.threads 0  # Use all cores

# Memory settings
git config core.packedGitLimit 512m
git config core.packedGitWindowSize 512m
git config pack.deltaCacheSize 2047m
git config pack.packSizeLimit 2g
git config pack.windowMemory 2047m
```

### Large Repository Optimization

```bash
# Partial clone
git clone --filter=blob:none --sparse <url>
git sparse-checkout init --cone
git sparse-checkout set src/frontend tests/frontend

# Shallow clone with deepening
git clone --depth 1 <url>
git fetch --deepen=100
git fetch --unshallow

# Background maintenance
git maintenance start
git config maintenance.gc.enabled true
git config maintenance.prefetch.enabled true
git config maintenance.incremental-repack.enabled true
```

## Security Hardening

### Repository Security

```bash
# Enable signed pushes
git config receive.certnonceseed "$(openssl rand -hex 20)"
git config receive.advertisepushcertificate true

# Restrict file modes
git config core.filemode false
git config core.protectHFS true
git config core.protectNTFS true

# Prevent CRLF attacks
git config core.autocrlf false
git config core.safecrlf true

# GPG commit signing
git config commit.gpgsign true
git config tag.gpgsign true
git config gpg.program gpg2
```

### Audit and Compliance

```bash
# Audit log generation
git log --pretty=format:'{
  "commit": "%H",
  "author": "%an <%ae>",
  "date": "%aI",
  "message": "%s",
  "signature": "%GK",
  "verification": "%G?"
},' > audit-log.json

# Verify all signatures
git log --show-signature --pretty=fuller

# Check for unsigned commits
git log --format='%H %G?' | grep -v 'G$'
```

## Advanced Workflows

### Trunk-based Development

```bash
# Feature flags workflow
git checkout main
git pull origin main
git checkout -b feature/flag-new-ui

# Small, frequent commits
git add -p
git commit -m "feat: Add feature flag for new UI"
git push origin feature/flag-new-ui

# Quick integration
git checkout main
git merge --ff-only feature/flag-new-ui
git push origin main
```

### Monorepo Management

```bash
# Path-based operations
git log -- packages/frontend/
git diff HEAD~10 -- packages/backend/

# Subtree split
git subtree split --prefix=packages/shared -b shared-only

# Filter-branch for extraction
git filter-branch --subdirectory-filter packages/service -- --all

# Sparse checkout for teams
git sparse-checkout set packages/team-a packages/shared
```

### Git-flow Automation

```bash
# Automated release
release_version=$1
git flow release start $release_version
npm version $release_version
git add package.json package-lock.json
git commit -m "chore: Bump version to $release_version"
git flow release finish -m "Release $release_version" $release_version

# Hotfix automation
git flow hotfix start hotfix-$version
# ... apply fix ...
git flow hotfix finish hotfix-$version
```

## Disaster Recovery

### Repository Recovery

```bash
# Recover from corruption
git fsck --full
git gc --prune=now
git repack -a -d -f

# Rebuild index
rm .git/index
git reset

# Recovery from backup
git clone --mirror backup-url recovered-repo
cd recovered-repo
git remote remove origin
git remote add origin original-url

# Emergency patch extraction
git format-patch HEAD~10
# Apply elsewhere: git am *.patch
```

### Data Recovery Tools

```bash
# Find dangling objects
git fsck --lost-found
ls .git/lost-found/commit/

# Recover deleted branch
git reflog show --all | grep "branch-name"
git branch recovered-branch <sha>

# Recover dropped stash
git fsck --unreachable | grep commit | cut -d' ' -f3 | 
xargs git log --merges --no-walk --grep=WIP

# Time-based recovery
git reflog --date=iso | grep "2023-06-15"
```

## Integration Patterns

### CI/CD Integration

```yaml
# Advanced GitHub Actions
name: Advanced CI
on:
  push:
    branches: [main, develop]
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for analysis
      
      - name: Git Analysis
        run: |
          echo "Changed files:"
          git diff --name-only origin/main...HEAD
          
          echo "Commit count:"
          git rev-list --count origin/main...HEAD
          
          echo "Contributors:"
          git shortlog -sn origin/main...HEAD
```

### Advanced Aliases

```bash
# Complex aliases
[alias]
    # Interactive rebase with autosquash
    ri = rebase -i --autosquash
    
    # Show branches sorted by date
    recent = for-each-ref --sort=-committerdate --format='%(committerdate:relative) %(refname:short)' refs/heads/
    
    # Find merged branches
    merged = "!git branch -r --merged | grep -v HEAD | grep -v develop | grep -v main | sed 's/origin\\///' | xargs -n 1 echo"
    
    # Prune all remotes
    prune-all = !git remote | xargs -n 1 git remote prune
    
    # Show file history with renames
    file-history = log --follow -p --
    
    # Interactive add with diff
    addi = add -i
    
    # Amend without editing message
    amend = commit --amend --no-edit
    
    # Undo last commit keeping changes
    undo = reset HEAD~1 --soft
    
    # Show my commits today
    today = log --since=midnight --author=\"$(git config user.name)\" --oneline
```

## Best Practices for Advanced Users

1. **Master the Object Model**: Understand blobs, trees, commits
2. **Use Reflog Liberally**: Your safety net for recovery
3. **Automate with Hooks**: Enforce standards automatically
4. **Optimize for Scale**: Configure for large repositories
5. **Sign Everything**: GPG sign commits and tags
6. **Script Common Tasks**: Create aliases and scripts
7. **Monitor Performance**: Use time and --verbose flags
8. **Practice Recovery**: Know how to fix problems
9. **Document Workflows**: Maintain team playbooks
10. **Stay Updated**: Git evolves, learn new features

## Resources

- [Git Source Code](https://github.com/git/git)
- [Git Internals Documentation](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain)
- [libgit2 - Git Core Library](https://libgit2.org/)
- [Git Merge Conference Talks](https://git-merge.com/)
- [Git Rev News](https://git.github.io/rev_news/)