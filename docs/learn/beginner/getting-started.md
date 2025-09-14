---
title: Getting Started
sidebar_position: 1
tags: [beginner, fundamentals]
---

# 🚀 Getting Started with Platform Engineering

**Prerequisites**: None - This is your starting point!  
**Time to Complete**: ⏱️ 30 min read

## What is Platform Engineering?

Platform Engineering is the discipline of designing and building toolchains and workflows that enable self-service capabilities for software engineering organizations in the cloud-native era. Platform engineers provide an integrated product most often referred to as an "Internal Developer Platform" covering the operational necessities of the entire lifecycle of applications.

## Platform Engineering vs Related Roles

### Platform Engineer vs SRE vs DevOps

| Aspect | Platform Engineer | SRE | DevOps Engineer |
|--------|------------------|-----|-----------------|
| **Primary Focus** | Building internal platforms | Reliability & operations | CI/CD & automation |
| **Key Metric** | Developer productivity | SLOs & error budgets | Deployment frequency |
| **Approach** | Product mindset | Software engineering for ops | Culture & collaboration |
| **Customers** | Internal developers | End users | Development teams |

### When Companies Use Which Role

- **Startups**: Often combine all three into "DevOps Engineer"
- **Mid-size**: Separate DevOps and SRE roles
- **Enterprise**: Distinct Platform, SRE, and DevOps teams
- **Tech Giants**: Specialized roles with clear boundaries

## Core Responsibilities

### 1. Build Internal Developer Platforms
- Self-service infrastructure provisioning
- Standardized deployment pipelines  
- Developer portals and documentation
- Golden path templates

### 2. Enable Developer Productivity
- Reduce cognitive load on developers
- Automate repetitive tasks
- Provide abstraction layers
- Streamline workflows

### 3. Standardize Best Practices
- Security policies as code
- Compliance automation
- Cost optimization
- Performance standards

### 4. Maintain Platform Reliability
- Platform SLOs and monitoring
- Incident response
- Capacity planning
- Disaster recovery

## Required Skills Overview

### Technical Skills
- **Cloud Platforms**: AWS, GCP, or Azure
- **Infrastructure as Code**: Terraform, Pulumi
- **Containers**: Docker, Kubernetes
- **Programming**: Python, Go, Bash
- **CI/CD**: GitLab, GitHub Actions, Jenkins
- **Monitoring**: Prometheus, Grafana, DataDog

### Soft Skills
- Product thinking
- Communication
- Documentation
- Teaching and mentoring
- Problem-solving
- Collaboration

## Career Landscape

### Market Demand (2024-2025)
- **87%** of enterprises prioritizing platform engineering
- **25%** average salary premium over traditional ops
- **4x** growth in job postings since 2021

### Salary Ranges (USD)
- **Junior (0-2 years)**: $90k - $130k
- **Mid-level (2-5 years)**: $130k - $180k  
- **Senior (5-8 years)**: $180k - $250k
- **Staff/Principal (8+ years)**: $250k - $400k+

### Top Companies Hiring
1. **FAANG**: Meta, Amazon, Netflix, Google
2. **Cloud Providers**: AWS, GCP, Azure
3. **Tech Unicorns**: Stripe, Databricks, Snowflake
4. **Enterprises**: Banks, Healthcare, Retail

## Setting Up Your Learning Environment

### 1. Local Development Setup
```bash
# Install essential tools
# macOS
brew install git python3 go terraform kubectl docker

# Linux
sudo apt-get update
sudo apt-get install git python3 golang terraform kubectl docker.io

# Windows (use WSL2)
wsl --install
# Then follow Linux instructions
```

### 2. Cloud Accounts (Free Tiers)
- **AWS**: [Free Tier](https://aws.amazon.com/free/) - 12 months
- **GCP**: [$300 credit](https://cloud.google.com/free) - 90 days
- **Azure**: [$200 credit](https://azure.microsoft.com/free/) - 30 days

### 3. Learning Lab Setup
```bash
# Create a learning directory
mkdir ~/platform-engineering-labs
cd ~/platform-engineering-labs

# Initialize git
git init

# Create project structure
mkdir -p {infrastructure,applications,scripts,docs}
```

### 4. Essential Tools to Install
- **IDE**: VS Code with extensions
- **Terminal**: iTerm2 (Mac) or Windows Terminal
- **Version Control**: Git with GitHub/GitLab account
- **Container Runtime**: Docker Desktop
- **Local Kubernetes**: kind or minikube

## Your Learning Path

### Phase 1: Foundations (Weeks 1-4)
1. Master Linux fundamentals
2. Learn Git and version control
3. Basic scripting with Bash and Python
4. Understand networking basics

### Phase 2: Core Technologies (Weeks 5-12)
1. Cloud platform basics (pick one)
2. Docker and containerization
3. Kubernetes fundamentals
4. Infrastructure as Code basics

### Phase 3: Platform Skills (Weeks 13-20)
1. CI/CD pipeline design
2. Monitoring and observability
3. Security best practices
4. Platform design patterns

### Phase 4: Advanced Topics (Weeks 21+)
1. Multi-cloud strategies
2. Service mesh
3. GitOps and progressive delivery
4. Platform as a Product

## Interview Preparation

### Common Intro Questions

**Q: Why do you want to be a Platform Engineer?**
- Focus on impact and scale
- Mention enabling developers
- Show passion for automation

**Q: What's the difference between Platform Engineering and DevOps?**
- Platform Engineering: Building products for developers
- DevOps: Cultural movement and practices
- Overlap exists but focus differs

**Q: How do you measure platform success?**
- Developer satisfaction (NPS scores)
- Time to production
- Platform adoption rate
- Incident reduction
- Developer productivity metrics

### How to Explain Your Background

#### For Career Switchers
"I'm transitioning from [previous role] where I gained experience in [relevant skills]. I'm passionate about platform engineering because [specific reason]. I've been learning [technologies] through [projects/courses]."

#### For New Graduates
"I studied [degree] where I focused on [relevant coursework]. I'm drawn to platform engineering because [reason]. I've built [projects] using [technologies] to prepare for this role."

#### For Experienced Developers
"I have [X years] experience in [current role]. I've naturally gravitated toward platform work by [examples]. I want to formalize this transition because [motivation]."

## Action Items

### This Week
- [ ] Set up your local development environment
- [ ] Create free cloud accounts
- [ ] Join Platform Engineering Slack community
- [ ] Start with Linux fundamentals

### This Month  
- [ ] Complete beginner topics
- [ ] Build your first Infrastructure as Code project
- [ ] Contribute to an open-source platform tool
- [ ] Network with platform engineers

## Next Steps

Ready to dive deeper? Continue with:
- [Linux & System Fundamentals →](linux-fundamentals)
- [Programming for Platform Engineers →](programming-basics)

## Additional Resources

- 📚 **Book**: "Team Topologies" by Manuel Pais
- 🎥 **Video**: [What is Platform Engineering?](https://www.youtube.com/watch?v=example)
- 📝 **Blog**: [Platform Engineering Blog](https://platformengineering.org/blog)
- 💬 **Community**: [Platform Engineering Slack](https://platformengineering.org/slack)