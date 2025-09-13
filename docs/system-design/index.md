---
title: System Design for Platform Engineers
sidebar_position: 1
---

# System Design for Platform Engineers

System design interviews for platform engineering roles focus on building reliable, scalable, and maintainable infrastructure. Unlike product-focused system design, you'll need to demonstrate deep understanding of distributed systems, infrastructure components, and operational excellence.

## Platform Engineering System Design Focus Areas

### What Makes Platform Engineering Design Different

1. **Infrastructure First**: Design systems that other teams build upon
2. **Operational Excellence**: Consider monitoring, debugging, and maintenance from day one
3. **Cost Optimization**: Balance performance with resource efficiency
4. **Multi-tenancy**: Design for multiple teams and applications
5. **Security and Compliance**: Build security into the platform layer

## System Design Interview Framework

### 1. Requirements Gathering (5-10 minutes)

**Functional Requirements:**
- What services need to be supported?
- What are the SLAs/SLOs?
- What scale are we designing for?
- What are the integration points?

**Non-Functional Requirements:**
- Availability targets (99.9%, 99.99%?)
- Latency requirements
- Throughput expectations
- Security and compliance needs
- Cost constraints

**Example Questions to Ask:**
- "What's our target availability?"
- "What's the expected request rate?"
- "What regions do we need to support?"
- "What's our budget constraint?"
- "What compliance requirements exist?"

### 2. Capacity Estimation (5 minutes)

**Calculate:**
- Requests per second (RPS)
- Storage requirements
- Bandwidth needs
- Server/container count
- Cost estimates

**Example Calculation:**
```
Daily Active Users: 10M
Requests per user: 100/day
Total requests: 1B/day = 11,574 RPS
Peak traffic: 3x average = 34,722 RPS
With 20% headroom: 41,666 RPS needed
```

### 3. High-Level Design (10-15 minutes)

Start with major components:
- Load balancers
- API gateways
- Service mesh
- Data stores
- Message queues
- Caching layers
- Monitoring stack

### 4. Detailed Design (15-20 minutes)

Deep dive into:
- Data flow
- API design
- Database schema
- Caching strategy
- Security measures
- Monitoring and alerting

### 5. Scale and Optimize (10 minutes)

Discuss:
- Bottlenecks
- Scaling strategies
- Performance optimization
- Cost optimization
- Disaster recovery

## Common Platform Engineering System Design Questions

### 1. Design a CI/CD Platform

**Requirements:**
- Support 1000+ developers
- Multiple programming languages
- 10,000 builds/day
- Artifact storage
- Security scanning

**Key Components:**
```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Git Repo  │────▶│  Webhook/API │────▶│ Build Queue  │
└─────────────┘     └──────────────┘     └──────────────┘
                                                  │
                                                  ▼
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Builders  │◀────│   Scheduler  │     │ Orchestrator │
└─────────────┘     └──────────────┘     └──────────────┘
        │
        ▼
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Artifacts  │     │Test Results  │     │  Deployment  │
└─────────────┘     └──────────────┘     └──────────────┘
```

**Design Considerations:**
- Build isolation (containers/VMs)
- Queue management (Kafka/RabbitMQ)
- Artifact storage (S3/Artifactory)
- Secret management
- Build caching
- Monitoring and metrics

**Resources:**
- 📖 [Jenkins Architecture](https://www.jenkins.io/doc/book/architecting-for-scale/)
- 🎥 [GitLab CI Architecture](https://www.youtube.com/watch?v=Ew4CEgVU6Bw)
- 📚 [Continuous Delivery](https://continuousdelivery.com/)

### 2. Design a Container Orchestration Platform

**Requirements:**
- Manage 10,000+ containers
- Multi-region deployment
- Auto-scaling
- Service discovery
- Zero-downtime deployments

**Key Components:**
```
┌─────────────────┐
│   Control Plane │
├─────────────────┤
│ • API Server    │
│ • Scheduler     │
│ • Controller    │
│ • etcd          │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│ Node 1 │ │ Node 2 │
├────────┤ ├────────┤
│ Kubelet│ │ Kubelet│
│ Proxy  │ │ Proxy  │
│Runtime │ │Runtime │
└────────┘ └────────┘
```

**Design Considerations:**
- Control plane high availability
- Network policies and CNI
- Storage orchestration
- Resource allocation
- Security policies
- Multi-tenancy

**Resources:**
- 📖 [Kubernetes Architecture](https://kubernetes.io/docs/concepts/architecture/)
- 🎥 [Building a Container Platform](https://www.youtube.com/watch?v=kOa_llowQ1c)
- 📚 [Production Kubernetes](https://www.oreilly.com/library/view/production-kubernetes/9781492092298/)

### 3. Design a Monitoring and Observability Platform

**Requirements:**
- 1M metrics/second
- 100TB logs/day
- Distributed tracing
- 99.9% availability
- 30-day retention

**Key Components:**
```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Agents    │────▶│  Collectors  │────▶│   Storage    │
└─────────────┘     └──────────────┘     └──────────────┘
                            │                      │
                            ▼                      ▼
                    ┌──────────────┐      ┌──────────────┐
                    │   Querying   │◀─────│ Aggregation  │
                    └──────────────┘      └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │Visualization │
                    └──────────────┘
```

**Design Considerations:**
- Time-series database selection
- Data retention policies
- Sampling strategies
- Query performance
- Alert management
- Data compression

**Resources:**
- 📖 [Prometheus Architecture](https://prometheus.io/docs/introduction/overview/)
- 🎥 [Observability at Scale](https://www.youtube.com/watch?v=a26tIi_H_sI)
- 📚 [Distributed Tracing in Practice](https://www.oreilly.com/library/view/distributed-tracing-in/9781492056621/)

### 4. Design a Service Mesh

**Requirements:**
- Handle 100K RPS
- mTLS between services
- Traffic management
- Circuit breaking
- Observability

**Key Components:**
```
┌────────────────┐
│  Control Plane │
├────────────────┤
│ • Config Mgmt  │
│ • Cert Mgmt    │
│ • Policy Engine│
└───────┬────────┘
        │
┌───────▼────────┐
│   Data Plane   │
├────────────────┤
│ Sidecar Proxies│
│ (Envoy)        │
└────────────────┘
```

**Resources:**
- 📖 [Istio Architecture](https://istio.io/latest/docs/concepts/architecture/)
- 🎥 [Service Mesh Comparison](https://www.youtube.com/watch?v=oGi5GjDNNcI)
- 📚 [Service Mesh Patterns](https://www.oreilly.com/library/view/service-mesh-patterns/9781492086444/)

### 5. Design a Multi-Region Database Platform

**Requirements:**
- Global distribution
- Strong consistency options
- 99.99% availability
- Automatic failover
- Compliance with data residency

**Key Components:**
```
┌─────────────────────────────────────┐
│         Global Coordinator          │
└─────────────┬───────────────────────┘
              │
    ┌─────────┴─────────┬─────────────┐
    ▼                   ▼             ▼
┌─────────┐      ┌─────────┐   ┌─────────┐
│Region 1 │      │Region 2 │   │Region 3 │
├─────────┤      ├─────────┤   ├─────────┤
│ Primary │◀────▶│ Replica │◀─▶│ Replica │
└─────────┘      └─────────┘   └─────────┘
```

**Resources:**
- 📖 [Spanner Architecture](https://cloud.google.com/spanner/docs/concepts)
- 🎥 [CockroachDB Design](https://www.youtube.com/watch?v=PIePIsskhrw)
- 📚 [Database Internals](https://www.databass.dev/)

## Platform-Specific Design Patterns

### 1. Reliability Patterns

**Circuit Breaker**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'
```

**Bulkhead Pattern**
- Isolate resources to prevent cascade failures
- Use connection pools with limits
- Implement thread pool isolation

**Resources:**
- 📖 [Release It! Design Patterns](https://pragprog.com/titles/mnee2/release-it-second-edition/)
- 🎥 [Hystrix: Engineering Resilience](https://www.youtube.com/watch?v=U50MJlpjyaY)

### 2. Scalability Patterns

**Horizontal Scaling**
- Stateless services
- Shared-nothing architecture
- Database sharding

**Caching Strategies**
- Cache-aside
- Write-through
- Write-behind
- Refresh-ahead

**Resources:**
- 📖 [Scalability Rules](https://scalabilityrules.com/)
- 📖 [High Scalability](http://highscalability.com/)

### 3. Security Patterns

**Zero Trust Architecture**
- Verify explicitly
- Least privilege access
- Assume breach

**Secret Management**
- Centralized secret store
- Dynamic secret generation
- Secret rotation

**Resources:**
- 📖 [Zero Trust Networks](https://www.oreilly.com/library/view/zero-trust-networks/9781491962183/)
- 🎥 [HashiCorp Vault Architecture](https://www.youtube.com/watch?v=yvhBGlALAiI)

## System Design Resources

### Books
- 📚 **[Designing Data-Intensive Applications](https://dataintensive.net/)** - Martin Kleppmann
- 📚 **[Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/)** - Google
- 📚 **[The System Design Interview](https://www.amazon.com/System-Design-Interview-Insiders-Guide/dp/1736049119)** - Alex Xu
- 📚 **[Building Microservices](https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/)** - Sam Newman

### Online Courses
- 🎓 [System Design Interview - An Insider's Guide](https://www.educative.io/courses/grokking-the-system-design-interview)
- 🎓 [Designing Distributed Systems](https://www.oreilly.com/library/view/designing-distributed-systems/9781098122683/)
- 🎥 [System Design Playlist - Gaurav Sen](https://www.youtube.com/playlist?list=PLMCXHnjXnTnvo6alSjVkgxV-VH6EPyvoX)

### Practice Resources
- 🎯 [System Design Primer](https://github.com/donnemartin/system-design-primer)
- 🎯 [High Scalability - Real World Architectures](http://highscalability.com/all-time-favorites/)
- 📖 [AWS Architecture Center](https://aws.amazon.com/architecture/)
- 📖 [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)

### Mock Interviews
- 🎯 [Pramp - System Design](https://www.pramp.com/dev/system-design-interview)
- 🎯 [System Design Interview (Paid)](https://www.systemdesigninterview.com/)
- 🎯 [Interviewing.io](https://interviewing.io/)

## Common Pitfalls to Avoid

1. **Over-engineering**: Don't design for 1B users when asked for 1M
2. **Ignoring constraints**: Always consider cost, team size, timeline
3. **Missing monitoring**: Every design needs observability
4. **Forgetting security**: Security should be built-in, not bolted-on
5. **Neglecting operations**: Consider how the system will be maintained

## Tips for Success

1. **Think out loud**: Verbalize your thought process
2. **Start simple**: Begin with a basic design and iterate
3. **Draw diagrams**: Visual representations help communicate ideas
4. **Consider trade-offs**: Every decision has pros and cons
5. **Ask questions**: Clarify requirements and constraints
6. **Know your numbers**: Memorize common latency and capacity figures

## Latency Numbers Every Platform Engineer Should Know

```
L1 cache reference                           0.5 ns
Branch mispredict                            5   ns
L2 cache reference                           7   ns
Mutex lock/unlock                           25   ns
Main memory reference                      100   ns
Compress 1K bytes with Zippy             3,000   ns
Send 1K bytes over 1 Gbps network       10,000   ns
Read 4K randomly from SSD               150,000   ns
Read 1 MB sequentially from memory      250,000   ns
Round trip within same datacenter       500,000   ns
Read 1 MB sequentially from SSD       1,000,000   ns
Disk seek                            10,000,000   ns
Read 1 MB sequentially from disk     20,000,000   ns
Send packet CA->Netherlands->CA     150,000,000   ns
```

Remember: System design for platform engineering is about building the foundation that enables other teams to succeed. Focus on reliability, scalability, and operational excellence in every design decision.