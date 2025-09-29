---
sidebar_position: 2
---

# Hands-On Labs

<GitHubButtons />
Practical exercises to build platform engineering skills.

## Lab Environment Setup

### Local Development
- Docker Desktop
- Minikube/Kind
- Terraform
- AWS CLI
- kubectl

### Cloud Sandboxes
- AWS Free Tier
- Google Cloud Free Credits
- Azure Free Account
- Civo Cloud

## Kubernetes Labs

### Lab 1: Deploy Microservices
**Objective**: Deploy a multi-tier application on Kubernetes

**Tasks**:
1. Create namespace and resource quotas
2. Deploy frontend, backend, and database
3. Configure services and ingress
4. Implement horizontal pod autoscaling
5. Set up persistent storage

**Skills**: Deployments, Services, ConfigMaps, Secrets, HPA, PVC

### Lab 2: Implement GitOps
**Objective**: Set up ArgoCD for continuous deployment

**Tasks**:
1. Install ArgoCD on cluster
2. Connect Git repository
3. Create application manifests
4. Implement sync policies
5. Configure automated rollbacks

**Skills**: GitOps, ArgoCD, Helm, Kustomize

## Infrastructure as Code Labs

### Lab 3: Multi-Region Infrastructure
**Objective**: Deploy infrastructure across multiple AWS regions

**Tasks**:
1. Create VPC with public/private subnets
2. Set up VPC peering
3. Deploy RDS with read replicas
4. Configure Route53 for failover
5. Implement CloudFront CDN

**Skills**: Terraform, AWS networking, High availability

### Lab 4: Serverless Platform
**Objective**: Build event-driven serverless architecture

**Tasks**:
1. Create Lambda functions
2. Set up API Gateway
3. Configure EventBridge rules
4. Implement DynamoDB tables
5. Add CloudWatch monitoring

**Skills**: Serverless, Event-driven architecture, AWS Lambda

## CI/CD Labs

### Lab 5: Complete CI/CD Pipeline
**Objective**: Build end-to-end automated deployment pipeline

**Tasks**:
1. Set up GitHub Actions workflow
2. Implement unit and integration tests
3. Add security scanning (SAST/DAST)
4. Configure multi-environment deployments
5. Implement approval gates

**Skills**: GitHub Actions, Testing, Security, Deployment strategies

## Observability Labs

### Lab 6: Full-Stack Monitoring
**Objective**: Implement comprehensive observability solution

**Tasks**:
1. Deploy Prometheus and Grafana
2. Configure service mesh with Istio
3. Set up distributed tracing with Jaeger
4. Create custom dashboards
5. Implement SLO-based alerts

**Skills**: Prometheus, Grafana, Istio, Jaeger, SRE practices

## Security Labs

### Lab 7: Zero-Trust Security
**Objective**: Implement security best practices

**Tasks**:
1. Set up OIDC authentication
2. Implement RBAC policies
3. Configure network policies
4. Add admission controllers
5. Implement secrets management

**Skills**: Security, RBAC, Network policies, OPA

## Challenge Projects

### Project 1: Build a Platform
**Duration**: 1 week

**Requirements**:
- Multi-tenant Kubernetes platform
- Self-service developer portal
- Automated provisioning
- Cost tracking
- Compliance automation

### Project 2: Disaster Recovery
**Duration**: 3 days

**Requirements**:
- Implement backup strategies
- Test failover procedures
- Document RTO/RPO
- Automate recovery
- Chaos engineering tests

## Lab Resources

### Sample Applications
- [microservices-demo](https://github.com/microservices-demo/microservices-demo)
- [spring-petclinic](https://github.com/spring-projects/spring-petclinic)
- [sock-shop](https://github.com/microservices-demo/microservices-demo)

### Learning Platforms
- Katacoda (interactive scenarios)
- A Cloud Guru (hands-on labs)
- Linux Academy
- Pluralsight labs