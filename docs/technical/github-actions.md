# GitHub Actions - GitHub's CI/CD Platform

GitHub Actions is a powerful automation platform integrated directly into GitHub, enabling continuous integration, continuous deployment, and workflow automation. It uses YAML-based configuration files and provides a marketplace of reusable actions.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **GitHub Actions Tutorial - Complete Course**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 1.5 hours](https://www.youtube.com/watch?v=R8_veQiYBjI)
- **Why it's great**: Comprehensive tutorial covering workflows, actions, and CI/CD patterns

#### **GitHub Actions Crash Course**
- **Channel**: Traversy Media
- **Link**: [YouTube - 1 hour](https://www.youtube.com/watch?v=mFFXuXjVgkU)
- **Why it's great**: Quick start guide with practical examples and common workflows

#### **Advanced GitHub Actions**
- **Channel**: DevOps Journey
- **Link**: [YouTube Playlist](https://www.youtube.com/playlist?list=PL7iMyoQPMtAOevZe1jrZ2YbJm7EFBMSiV)
- **Why it's great**: Deep dive into advanced features and enterprise patterns

### 📖 Essential Documentation

#### **GitHub Actions Official Documentation**
- **Link**: [docs.github.com/en/actions](https://docs.github.com/en/actions)
- **Why it's great**: Comprehensive official documentation with examples and reference

#### **GitHub Actions Marketplace**
- **Link**: [github.com/marketplace/actions](https://github.com/marketplace/actions)
- **Why it's great**: Thousands of pre-built actions for common tasks

#### **GitHub Actions Workflow Syntax**
- **Link**: [docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- **Why it's great**: Complete YAML syntax reference for writing workflows

### 📝 Must-Read Blogs & Articles

#### **GitHub Blog - Actions**
- **Source**: GitHub
- **Link**: [github.blog/tag/github-actions/](https://github.blog/tag/github-actions/)
- **Why it's great**: Official updates and best practices from GitHub team

#### **GitHub Actions Best Practices**
- **Source**: GitHub
- **Link**: [docs.github.com/en/actions/learn-github-actions/security-hardening-for-github-actions](https://docs.github.com/en/actions/learn-github-actions/security-hardening-for-github-actions)
- **Why it's great**: Security and performance best practices

#### **CI/CD with GitHub Actions**
- **Source**: DigitalOcean
- **Link**: [digitalocean.com/community/tutorials/how-to-deploy-a-react-application-with-nginx-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-set-up-continuous-integration-with-github-actions)
- **Why it's great**: Practical deployment tutorials and patterns

### 🎓 Structured Courses

#### **GitHub Actions for CI/CD**
- **Platform**: GitHub Learning Lab
- **Link**: [lab.github.com/courses](https://lab.github.com/courses)
- **Cost**: Free
- **Why it's great**: Official hands-on courses with real repositories

#### **DevOps with GitHub Actions**
- **Platform**: Udemy
- **Link**: [udemy.com/course/github-actions-the-complete-guide/](https://www.udemy.com/course/github-actions-the-complete-guide/)
- **Cost**: Paid
- **Why it's great**: Comprehensive course covering advanced workflows and integrations

### 🛠️ Tools & Platforms

#### **Act (Local GitHub Actions)**
- **Link**: [github.com/nektos/act](https://github.com/nektos/act)
- **Why it's great**: Run GitHub Actions locally for testing and development

#### **GitHub Actions Runner**
- **Link**: [github.com/actions/runner](https://github.com/actions/runner)
- **Why it's great**: Self-hosted runners for custom environments

#### **Super-Linter Action**
- **Link**: [github.com/github/super-linter](https://github.com/github/super-linter)
- **Why it's great**: Multi-language linting action for code quality

## Overview

GitHub Actions is a powerful automation platform integrated directly into GitHub, enabling continuous integration, continuous deployment, and workflow automation. It uses YAML-based configuration files and provides a marketplace of reusable actions.

## Core Concepts

### Workflow Components

```yaml
# .github/workflows/main.yml
name: CI/CD Pipeline          # Workflow name
on:                          # Triggers
  push:
    branches: [main]
  pull_request:
    branches: [main]
    
jobs:                        # Parallel jobs
  test:                      # Job ID
    runs-on: ubuntu-latest   # Runner
    steps:                   # Sequential steps
      - uses: actions/checkout@v3  # Action
      - run: npm test        # Command
```

### Workflow Triggers

```yaml
# Push events
on:
  push:
    branches:
      - main
      - 'releases/**'
    tags:
      - v*
    paths:
      - 'src/**'
      - '!**.md'

# Pull request events
on:
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main, develop]

# Schedule (Cron)
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
    - cron: '*/15 * * * *'  # Every 15 minutes

# Manual trigger
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - production
          - staging
          - development

# Workflow completion
on:
  workflow_run:
    workflows: ["Build"]
    types: [completed]

# External events
on:
  repository_dispatch:
    types: [custom-event]

# Multiple triggers
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly
```

## Basic Workflows

### Node.js CI/CD

```yaml
name: Node.js CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18.x'
  REGISTRY_URL: 'https://registry.npmjs.org'

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test -- --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage/lcov.info
          
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install and build
        run: |
          npm ci
          npm run build
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-artifacts
          path: dist/
          retention-days: 5

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: build-artifacts
          path: dist/
      
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # Add deployment script here
```

### Python Application

```yaml
name: Python CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Lint with flake8
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      
      - name: Type check with mypy
        run: mypy src/
      
      - name: Test with pytest
        run: |
          pytest tests/ -v --cov=src --cov-report=xml --cov-report=html
      
      - name: Security scan with bandit
        run: bandit -r src/ -f json -o bandit-report.json

  publish:
    needs: test
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Build package
        run: |
          pip install build
          python -m build
      
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          user: __token__
          password: ${{ secrets.PYPI_API_TOKEN }}
```

## Advanced Features

### Matrix Builds

```yaml
name: Matrix Testing

on: [push, pull_request]

jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [14, 16, 18]
        include:
          - os: ubuntu-latest
            node: 18
            coverage: true
        exclude:
          - os: windows-latest
            node: 14
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js ${{ matrix.node }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node }}
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Coverage
        if: matrix.coverage == true
        run: npm run test:coverage
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '18.x'
      environment:
        required: true
        type: string
    secrets:
      npm-token:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ inputs.node-version }}
          registry-url: 'https://registry.npmjs.org'
      
      - name: Configure npm
        run: |
          echo "//registry.npmjs.org/:_authToken=${{ secrets.npm-token }}" > ~/.npmrc
      
      - name: Test in ${{ inputs.environment }}
        run: |
          npm ci
          npm test
        env:
          NODE_ENV: ${{ inputs.environment }}

# .github/workflows/main.yml
name: Main Workflow

on: [push]

jobs:
  test-staging:
    uses: ./.github/workflows/reusable-test.yml
    with:
      environment: staging
      node-version: '18.x'
    secrets:
      npm-token: ${{ secrets.NPM_TOKEN }}
  
  test-production:
    uses: ./.github/workflows/reusable-test.yml
    with:
      environment: production
    secrets:
      npm-token: ${{ secrets.NPM_TOKEN }}
```

### Docker Workflows

```yaml
name: Docker CI/CD

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Log in to Container Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Scan image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.meta.outputs.version }}
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

### Deployment Workflows

```yaml
name: Multi-Environment Deployment

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - development
          - staging
          - production

concurrency:
  group: deployment-${{ github.ref }}
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Generate version
        id: version
        run: |
          echo "version=$(date +%Y%m%d)-${GITHUB_SHA::7}" >> $GITHUB_OUTPUT
      
      - name: Build application
        run: |
          echo "Building version ${{ steps.version.outputs.version }}"
          # Build commands here
      
      - name: Upload build
        uses: actions/upload-artifact@v3
        with:
          name: build-${{ steps.version.outputs.version }}
          path: dist/

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Download build
        uses: actions/download-artifact@v3
        with:
          name: build-${{ needs.build.outputs.version }}
      
      - name: Deploy to staging
        env:
          DEPLOY_KEY: ${{ secrets.STAGING_DEPLOY_KEY }}
        run: |
          echo "Deploying to staging..."
          # Deployment script
      
      - name: Run smoke tests
        run: |
          curl -f https://staging.example.com/health || exit 1

  deploy-production:
    needs: [build, deploy-staging]
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    if: github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Download build
        uses: actions/download-artifact@v3
        with:
          name: build-${{ needs.build.outputs.version }}
      
      - name: Backup current deployment
        run: |
          echo "Creating backup..."
          # Backup commands
      
      - name: Deploy to production
        env:
          DEPLOY_KEY: ${{ secrets.PRODUCTION_DEPLOY_KEY }}
        run: |
          echo "Deploying to production..."
          # Deployment script
      
      - name: Verify deployment
        run: |
          # Health checks
          curl -f https://example.com/health || exit 1
      
      - name: Notify team
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Production deployment ${{ job.status }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Security and Secrets

### Secret Management

```yaml
name: Secure Workflow

on: [push]

jobs:
  secure-job:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      # Organization secrets
      - name: Use organization secret
        env:
          API_KEY: ${{ secrets.ORG_API_KEY }}
        run: |
          echo "API key is set: $([ ! -z "$API_KEY" ] && echo "Yes" || echo "No")"
      
      # Repository secrets
      - name: Use repository secret
        env:
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: |
          echo "::add-mask::$DB_PASSWORD"
          echo "Database password is configured"
      
      # Environment secrets
      - name: Deploy with environment secrets
        environment: production
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          echo "Deploying with secure credentials"
      
      # Dynamic secrets
      - name: Generate temporary token
        id: token
        run: |
          TOKEN=$(openssl rand -hex 20)
          echo "::add-mask::$TOKEN"
          echo "token=$TOKEN" >> $GITHUB_OUTPUT
      
      - name: Use temporary token
        env:
          TEMP_TOKEN: ${{ steps.token.outputs.token }}
        run: |
          echo "Using temporary token"
```

### OIDC Authentication

```yaml
name: OIDC AWS Deployment

on:
  push:
    branches: [main]

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActions
          role-session-name: GitHubActions
          aws-region: us-east-1
      
      - name: Deploy to AWS
        run: |
          aws s3 sync ./dist s3://my-bucket/
          aws cloudfront create-invalidation --distribution-id ABCD --paths "/*"
```

## Caching Strategies

### Dependency Caching

```yaml
name: Advanced Caching

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      # Node.js dependency caching
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: '**/package-lock.json'
      
      # Custom cache
      - name: Cache build outputs
        uses: actions/cache@v3
        id: build-cache
        with:
          path: |
            dist/
            .next/cache
          key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}-${{ hashFiles('src/**') }}
          restore-keys: |
            ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}-
            ${{ runner.os }}-build-
      
      # Docker layer caching
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Build with cache
        uses: docker/build-push-action@v4
        with:
          context: .
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      # Gradle caching
      - name: Setup Gradle
        uses: gradle/gradle-build-action@v2
        with:
          gradle-version: 8.0
          cache-read-only: ${{ github.ref != 'refs/heads/main' }}
      
      # Multiple cache keys
      - name: Cache multiple paths
        uses: actions/cache@v3
        with:
          path: |
            ~/.npm
            ~/.cache/pip
            ~/Library/Caches/Homebrew
          key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', '**/requirements.txt') }}
```

### Cache Restoration

```yaml
name: Smart Cache Restoration

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Restore or initialize cache
        uses: actions/cache@v3
        id: cache
        with:
          path: |
            node_modules/
            .cache/
          key: ${{ runner.os }}-${{ hashFiles('**/package-lock.json') }}-${{ github.run_id }}
          restore-keys: |
            ${{ runner.os }}-${{ hashFiles('**/package-lock.json') }}-
            ${{ runner.os }}-
      
      - name: Install dependencies
        if: steps.cache.outputs.cache-hit != 'true'
        run: npm ci
      
      - name: Validate cache
        run: |
          if [ -d "node_modules" ]; then
            echo "Cache restored successfully"
            npm ls
          else
            echo "Cache miss - installing dependencies"
            npm ci
          fi
```

## Custom Actions

### Composite Action

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Setup Node.js project with caching'
inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '18'
  install-command:
    description: 'Install command'
    required: false
    default: 'npm ci'

outputs:
  cache-hit:
    description: 'Cache hit status'
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: 'composite'
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
    
    - name: Cache dependencies
      id: cache
      uses: actions/cache@v3
      with:
        path: node_modules
        key: deps-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
    
    - name: Install dependencies
      if: steps.cache.outputs.cache-hit != 'true'
      shell: bash
      run: ${{ inputs.install-command }}
    
    - name: Verify setup
      shell: bash
      run: |
        echo "Node version: $(node --version)"
        echo "npm version: $(npm --version)"

# Usage in workflow
name: Use Custom Action
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./.github/actions/setup-project
        with:
          node-version: '18'
```

### JavaScript Action

```javascript
// .github/actions/issue-labeler/index.js
const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('token', { required: true });
    const labels = core.getInput('labels', { required: true }).split(',');
    
    const octokit = github.getOctokit(token);
    const context = github.context;
    
    if (context.payload.issue) {
      await octokit.rest.issues.addLabels({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: context.payload.issue.number,
        labels: labels
      });
      
      core.info(`Added labels: ${labels.join(', ')}`);
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
```

```yaml
# .github/actions/issue-labeler/action.yml
name: 'Issue Labeler'
description: 'Add labels to issues'
inputs:
  token:
    description: 'GitHub token'
    required: true
  labels:
    description: 'Comma-separated labels'
    required: true
runs:
  using: 'node16'
  main: 'index.js'
```

## Performance Optimization

### Parallel Jobs

```yaml
name: Optimized Pipeline

on: [push, pull_request]

jobs:
  # Quick checks run first
  quick-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Syntax check
        run: |
          find . -name "*.yml" -exec yamllint {} \;
          find . -name "*.json" -exec jq . {} \; > /dev/null
  
  # Parallel test jobs
  test-unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:unit
  
  test-integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:integration
  
  test-e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npx playwright install
      - run: npm run test:e2e
  
  # Build only after tests pass
  build:
    needs: [test-unit, test-integration, test-e2e]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run build
```

### Conditional Execution

```yaml
name: Smart Execution

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      backend: ${{ steps.filter.outputs.backend }}
      frontend: ${{ steps.filter.outputs.frontend }}
      docs: ${{ steps.filter.outputs.docs }}
    steps:
      - uses: actions/checkout@v3
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            backend:
              - 'backend/**'
              - 'package.json'
            frontend:
              - 'frontend/**'
              - 'package.json'
            docs:
              - 'docs/**'
              - '*.md'
  
  test-backend:
    needs: changes
    if: needs.changes.outputs.backend == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test backend
        run: |
          cd backend
          npm test
  
  test-frontend:
    needs: changes
    if: needs.changes.outputs.frontend == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test frontend
        run: |
          cd frontend
          npm test
  
  build-docs:
    needs: changes
    if: needs.changes.outputs.docs == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build documentation
        run: |
          npm run docs:build
```

## Monitoring and Notifications

### Status Checks and Notifications

```yaml
name: Complete Pipeline with Notifications

on: [push, pull_request]

jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup and test
        id: test
        continue-on-error: true
        run: |
          npm ci
          npm test
      
      - name: Create status check
        if: always()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.repos.createCommitStatus({
              owner: context.repo.owner,
              repo: context.repo.repo,
              sha: context.sha,
              state: '${{ steps.test.outcome }}',
              target_url: `https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}`,
              description: 'Test suite ${{ steps.test.outcome }}',
              context: 'continuous-integration/tests'
            });
      
      - name: Slack notification
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            Pipeline: ${{ job.status }}
            Commit: ${{ github.sha }}
            Author: ${{ github.actor }}
            Message: ${{ github.event.head_commit.message }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
          
      - name: Discord notification
        if: failure()
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
        run: |
          curl -H "Content-Type: application/json" \
            -X POST \
            -d "{\"content\": \"Build failed for ${GITHUB_REPOSITORY}\"}" \
            $DISCORD_WEBHOOK
      
      - name: Create issue on failure
        if: failure() && github.ref == 'refs/heads/main'
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Build failure on main branch',
              body: `Build failed for commit ${context.sha}\n\nSee: https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}`,
              labels: ['bug', 'ci-failure']
            });
```

## Best Practices

### Workflow Organization

```yaml
# .github/workflows/ci.yml
name: CI

on:
  workflow_call:  # Reusable
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for better analysis
      
      - name: Lint code
        uses: github/super-linter@v5
        env:
          DEFAULT_BRANCH: main
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          VALIDATE_ALL_CODEBASE: false

  security:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v3
      
      - name: Run CodeQL
        uses: github/codeql-action/analyze@v2
      
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  test:
    needs: [lint]
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [16, 18]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'
      
      - name: Install and test
        run: |
          npm ci
          npm run test:ci
      
      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.node == '18'
        uses: codecov/codecov-action@v3

  deploy-preview:
    needs: [test, security]
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    environment:
      name: preview
      url: ${{ steps.deploy.outputs.url }}
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy preview
        id: deploy
        run: |
          # Deploy to preview environment
          echo "url=https://pr-${{ github.event.pull_request.number }}.preview.example.com" >> $GITHUB_OUTPUT
      
      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '🚀 Preview deployed to ${{ steps.deploy.outputs.url }}'
            });
```

### Production Deployment Pattern

```yaml
name: Production Deployment

on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to deploy'
        required: true

jobs:
  validate:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate version
        id: version
        run: |
          VERSION="${{ github.event.release.tag_name || github.event.inputs.version }}"
          if [[ ! "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "Invalid version format: $VERSION"
            exit 1
          fi
          echo "version=$VERSION" >> $GITHUB_OUTPUT

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - uses: actions/checkout@v3
        with:
          ref: ${{ needs.validate.outputs.version }}
      
      - name: Deploy to production
        run: |
          echo "Deploying version ${{ needs.validate.outputs.version }}"
          # Deployment script
      
      - name: Create deployment record
        uses: actions/github-script@v6
        with:
          script: |
            const deployment = await github.rest.repos.createDeployment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              ref: '${{ needs.validate.outputs.version }}',
              environment: 'production',
              required_contexts: [],
              auto_merge: false
            });
            
            await github.rest.repos.createDeploymentStatus({
              owner: context.repo.owner,
              repo: context.repo.repo,
              deployment_id: deployment.data.id,
              state: 'success',
              environment_url: 'https://app.example.com'
            });
```

## Troubleshooting

### Debugging Workflows

```yaml
name: Debug Workflow

on:
  workflow_dispatch:

jobs:
  debug:
    runs-on: ubuntu-latest
    steps:
      - name: Print contexts
        env:
          GITHUB_CONTEXT: ${{ toJson(github) }}
          ENV_CONTEXT: ${{ toJson(env) }}
          VARS_CONTEXT: ${{ toJson(vars) }}
          JOB_CONTEXT: ${{ toJson(job) }}
          STEPS_CONTEXT: ${{ toJson(steps) }}
          RUNNER_CONTEXT: ${{ toJson(runner) }}
          SECRETS_CONTEXT: ${{ toJson(secrets) }}
          STRATEGY_CONTEXT: ${{ toJson(strategy) }}
          MATRIX_CONTEXT: ${{ toJson(matrix) }}
          NEEDS_CONTEXT: ${{ toJson(needs) }}
          INPUTS_CONTEXT: ${{ toJson(inputs) }}
        run: |
          echo "GitHub context:"
          echo "$GITHUB_CONTEXT" | jq '.'
          
          echo "Environment variables:"
          env | sort
          
      - name: Debug runner
        run: |
          echo "Runner OS: ${{ runner.os }}"
          echo "Runner Arch: ${{ runner.arch }}"
          echo "Available tools:"
          which git node npm docker || true
          
      - name: Setup tmate session
        if: ${{ github.event_name == 'workflow_dispatch' }}
        uses: mxschmitt/action-tmate@v3
        timeout-minutes: 15
        with:
          limit-access-to-actor: true
```

## Performance Tips

1. **Use Concurrency Controls**: Prevent duplicate runs
2. **Cache Dependencies**: Use built-in caching
3. **Matrix Builds Wisely**: Balance coverage and speed
4. **Fail Fast**: Stop early on critical failures
5. **Path Filters**: Run only necessary jobs
6. **Reusable Workflows**: DRY principle
7. **Artifact Management**: Clean up old artifacts
8. **Self-hosted Runners**: For resource-intensive tasks
9. **Composite Actions**: Reduce duplication
10. **Monitor Usage**: Track Actions minutes

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions)
- [Actions Toolkit](https://github.com/actions/toolkit)
- [GitHub Actions Examples](https://github.com/actions/examples)