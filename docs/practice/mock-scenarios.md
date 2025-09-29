---
sidebar_position: 4
---

# Mock Interview Scenarios

<GitHubButtons />
Practice with realistic platform engineering interview scenarios.

## Scenario 1: Production Outage

### The Situation
You receive a page at 2 AM. The main e-commerce platform is down. Users can't complete purchases. The on-call dashboard shows:
- API response times spiked to 30s
- Database CPU at 100%
- Error rate increased 500%
- Last deployment was 6 hours ago

### Your Task
1. How would you begin troubleshooting?
2. What tools would you use?
3. How would you communicate with stakeholders?
4. What's your rollback strategy?
5. How would you prevent this in the future?

### Expected Approach
- Check recent changes and deployments
- Analyze metrics and logs
- Identify root cause systematically
- Implement immediate mitigation
- Create post-mortem process

## Scenario 2: Scale Challenge

### The Situation
Your company is launching a Super Bowl commercial. Traffic is expected to increase 100x for 4 hours. Current infrastructure:
- 10 API servers
- 1 primary database
- Basic CDN setup
- No auto-scaling

### Your Task
1. Design scaling strategy
2. Identify potential bottlenecks
3. Plan for graceful degradation
4. Estimate costs
5. Create runbook for the event

### Key Considerations
- Database read replicas
- Caching strategies
- Queue systems for async processing
- Auto-scaling policies
- Load testing plan

## Scenario 3: Migration Project

### The Situation
Migrate a monolithic application to microservices on Kubernetes. Current state:
- 500k lines of code
- Single PostgreSQL database
- Deployed on VMs
- 10-person development team
- 99.5% uptime requirement

### Your Task
1. Create migration strategy
2. Define service boundaries
3. Plan data migration
4. Design CI/CD pipeline
5. Ensure zero downtime

### Approach Elements
- Strangler fig pattern
- Database decomposition
- Service mesh implementation
- Progressive rollout
- Monitoring strategy

## Scenario 4: Security Incident

### The Situation
Security team discovered:
- Exposed S3 bucket with customer data
- Suspicious API activity
- Potential credential compromise
- No audit logs for 30 days

### Your Task
1. Immediate response actions
2. Investigation approach
3. Communication plan
4. Remediation steps
5. Future prevention measures

### Critical Actions
- Isolate compromised resources
- Rotate all credentials
- Enable comprehensive logging
- Implement least privilege
- Security scanning automation

## Scenario 5: Cost Optimization

### The Situation
Monthly cloud bill increased 300% in 6 months:
- Current spend: $150,000/month
- No cost allocation tags
- Unknown resource ownership
- Overprovisioned instances
- No reserved instances

### Your Task
1. Analyze current spending
2. Identify quick wins
3. Long-term optimization plan
4. Implement cost controls
5. Create reporting dashboard

### Optimization Areas
- Right-sizing instances
- Reserved instance planning
- Spot instance usage
- Storage lifecycle policies
- Unused resource cleanup

## Scenario 6: Platform Design

### The Situation
Build internal developer platform for 200 engineers:
- Multiple programming languages
- Various deployment targets
- Compliance requirements
- Self-service needs
- Limited platform team (5 people)

### Your Task
1. Define platform capabilities
2. Choose technology stack
3. Design onboarding process
4. Plan governance model
5. Create success metrics

### Platform Components
- Service catalog
- CI/CD templates
- Monitoring/logging
- Cost tracking
- Security scanning

## Scenario 7: Disaster Recovery

### The Situation
Design DR strategy for critical payment system:
- Process $10M daily
- Current RTO: 24 hours
- Required RTO: 1 hour
- Required RPO: 5 minutes
- Budget: $500k annually

### Your Task
1. Assess current state
2. Design DR architecture
3. Create testing plan
4. Document procedures
5. Train team members

### DR Elements
- Multi-region deployment
- Database replication
- Automated failover
- Regular DR drills
- Runbook automation

## Scenario 8: Team Leadership

### The Situation
You inherit a struggling platform team:
- Low morale
- No documentation
- Frequent outages
- Siloed knowledge
- Resistance to change

### Your Task
1. Assess team dynamics
2. Create improvement plan
3. Build team culture
4. Implement best practices
5. Measure progress

### Leadership Actions
- 1-on-1 meetings
- Skills assessment
- Training programs
- Process improvements
- Recognition systems

## Practice Tips

### Before the Mock
- Research company context
- Review fundamentals
- Prepare questions
- Practice whiteboarding
- Time management

### During the Mock
- Think aloud
- Ask clarifying questions
- Consider trade-offs
- Show technical depth
- Demonstrate soft skills

### After the Mock
- Request feedback
- Identify gaps
- Practice weak areas
- Refine approach
- Build confidence