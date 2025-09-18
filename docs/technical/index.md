---
id: index
title: Technical Skills
sidebar_label: Overview
slug: /technical-skills
---

# Technical Skills for Platform Engineers

Master the essential technical skills needed for platform engineering, SRE, and DevOps roles. This comprehensive guide covers 150+ technologies organized into clear categories.

## 📍 Quick Navigation

<div className="technical-nav-box">

**Jump to:** [Linux & Systems](#-linux--systems) • [Networking](#-networking) • [Cloud Platforms](#️-cloud-platforms) • [Containers](#-containers--orchestration) • [IaC](#️-infrastructure-as-code) • [CI/CD](#-cicd--gitops) • [Monitoring](#-monitoring--observability) • [Databases](#-databases--storage) • [Programming](#-programming-languages) • [Security](#-security-tools) • [Messaging](#-messaging--streaming) • [Additional Tools](#️-additional-tools)

</div>

## 🐧 Linux & Systems

Master the foundation of all modern infrastructure.

### Core Linux
- **[Linux Fundamentals](/technical/linux-fundamentals)** ✅ - Commands, file systems, permissions
- **[System Administration](/technical/system-administration)** - User management, systemd, services
- **[Shell Scripting (Bash)](/technical/bash-scripting)** - Automation and scripting
- **[Linux Performance](/technical/linux-performance)** - Tuning, analysis, optimization
- **[Process Management](/technical/process-management)** - systemd, init, process control

### Advanced Linux
- **[Linux Security](/technical/linux-security)** - SELinux, AppArmor, hardening
- **[File Systems](/technical/file-systems)** - ext4, XFS, ZFS, Btrfs
- **[Linux Networking](/technical/linux-networking)** - iptables, netfilter, routing
- **[Package Management](/technical/package-management)** - apt, yum, dnf, snap
- **[Linux Deep Dive](/technical/linux-deep-dive)** ✅ - Kernel, internals, advanced topics

---

## 🌐 Networking

Build reliable, secure, and performant networks.

### Fundamentals
- **[TCP/IP & OSI Model](/technical/tcp-ip)** - Networking fundamentals
- **[DNS](/technical/dns)** - BIND, CoreDNS, Route53
- **[HTTP/HTTPS](/technical/http-https)** - Protocols, headers, optimization
- **[Network Troubleshooting](/technical/network-troubleshooting)** - tcpdump, Wireshark, dig

### Load Balancing & Proxies
- **[NGINX](/technical/nginx)** - Web server, reverse proxy, load balancer
- **[HAProxy](/technical/haproxy)** - High-performance load balancer
- **[Traefik](/technical/traefik)** - Cloud-native edge router
- **[Envoy](/technical/envoy)** - Modern L7 proxy and service mesh

### Advanced Networking
- **[BGP](/technical/bgp)** - Border Gateway Protocol
- **[VPN Technologies](/technical/vpn)** - WireGuard, OpenVPN, IPSec
- **[CDN](/technical/cdn)** - CloudFlare, Fastly, Akamai
- **[Service Discovery](/technical/service-discovery)** - Consul, CoreDNS, etcd

---

## ☁️ Cloud Platforms

Master the major cloud providers and cloud-native architectures.

### Major Providers
- **[AWS](/technical/aws)** ✅ - Amazon Web Services (EC2, S3, RDS, Lambda, etc.)
- **[Google Cloud Platform](/technical/gcp)** - Compute Engine, GKE, BigQuery
- **[Microsoft Azure](/technical/azure)** - VMs, AKS, Azure Functions
- **[Cloud Platforms Overview](/technical/cloud-platforms)** ✅ - Multi-cloud strategies

### Other Providers
- **[DigitalOcean](/technical/digitalocean)** - Simple cloud platform
- **[Linode](/technical/linode)** - Developer-friendly cloud
- **[Alibaba Cloud](/technical/alibaba-cloud)** - Asia-focused cloud
- **[Oracle Cloud](/technical/oracle-cloud)** - Enterprise cloud platform

### Private Cloud
- **[OpenStack](/technical/openstack)** - Open source cloud platform
- **[VMware vSphere](/technical/vmware)** - Enterprise virtualization
- **[Proxmox](/technical/proxmox)** - Open source virtualization

---

## 🐳 Containers & Orchestration

Build and manage containerized applications at scale.

### Container Runtimes
- **[Docker](/technical/docker)** ✅ - Container platform and ecosystem
- **[containerd](/technical/containerd)** - Industry-standard runtime
- **[Podman](/technical/podman)** - Daemonless containers
- **[CRI-O](/technical/cri-o)** - Lightweight Kubernetes runtime

### Orchestration Platforms
- **[Kubernetes](/technical/kubernetes)** ✅ - Container orchestration standard
- **[Kubernetes Mastery](/technical/kubernetes-mastery)** ✅ - Advanced K8s topics
- **[OpenShift](/technical/openshift)** - Enterprise Kubernetes
- **[Rancher](/technical/rancher)** - Multi-cluster management
- **[Nomad](/technical/nomad)** - Simple orchestrator

### Kubernetes Ecosystem
- **[Helm](/technical/helm)** - Kubernetes package manager
- **[Kustomize](/technical/kustomize)** - K8s configuration management
- **[Operators](/technical/operators)** - Kubernetes native apps
- **[K3s](/technical/k3s)** - Lightweight Kubernetes
- **[Kind](/technical/kind)** - K8s in Docker for testing

### Service Mesh
- **[Istio](/technical/istio)** - Connect, secure, control microservices
- **[Linkerd](/technical/linkerd)** - Ultralight service mesh
- **[Consul Connect](/technical/consul-connect)** - Service mesh by HashiCorp
- **[Service Mesh Overview](/technical/service-mesh)** - Concepts and comparison

### Container Security
- **[Falco](/technical/falco)** - Runtime security
- **[OPA](/technical/opa)** - Open Policy Agent
- **[Container Security Best Practices](/technical/container-security)** - Scanning, policies

---

## 🏗️ Infrastructure as Code

Automate infrastructure provisioning and configuration.

### Provisioning
- **[Terraform](/technical/terraform)** ✅ - Multi-cloud infrastructure as code
- **[Pulumi](/technical/pulumi)** - IaC using programming languages
- **[CloudFormation](/technical/cloudformation)** - AWS native IaC
- **[AWS CDK](/technical/aws-cdk)** - Cloud Development Kit
- **[Crossplane](/technical/crossplane)** - Kubernetes-native IaC

### Configuration Management
- **[Ansible](/technical/ansible)** - Agentless automation
- **[SaltStack](/technical/saltstack)** - Event-driven automation
- **[Chef](/technical/chef)** - Policy-based configuration
- **[Puppet](/technical/puppet)** - Declarative configuration

### Image Building
- **[Packer](/technical/packer)** - Multi-platform image builder
- **[Cloud-init](/technical/cloud-init)** - Instance initialization

---

## 🔄 CI/CD & GitOps

Implement continuous integration, delivery, and GitOps workflows.

### Version Control
- **[Git](/technical/git)** - Distributed version control
- **[Git Advanced](/technical/git-advanced)** - Rebasing, workflows, internals

### CI/CD Platforms
- **[GitHub Actions](/technical/github-actions)** - GitHub's CI/CD
- **[GitLab CI](/technical/gitlab-ci)** - Integrated DevOps platform
- **[Jenkins](/technical/jenkins)** - Extensible automation server
- **[CircleCI](/technical/circleci)** - Cloud-native CI/CD
- **[TeamCity](/technical/teamcity)** - JetBrains CI server
- **[Azure DevOps](/technical/azure-devops)** - Microsoft's DevOps platform

### GitOps Tools
- **[ArgoCD](/technical/argocd)** - Declarative GitOps for K8s
- **[Flux](/technical/flux)** - GitOps toolkit
- **[Tekton](/technical/tekton)** - Cloud-native CI/CD
- **[Spinnaker](/technical/spinnaker)** - Multi-cloud CD

### Build Tools
- **[Bazel](/technical/bazel)** - Google's build tool
- **[Gradle](/technical/gradle)** - Build automation
- **[Make](/technical/make)** - Classic build tool

---

## 📊 Monitoring & Observability

Monitor, analyze, and understand system behavior.

### Metrics & Monitoring
- **[Prometheus](/technical/prometheus)** - Cloud-native monitoring
- **[Grafana](/technical/grafana)** - Visualization platform
- **[VictoriaMetrics](/technical/victoriametrics)** - Fast time series DB
- **[InfluxDB](/technical/influxdb)** - Time series database
- **[Telegraf](/technical/telegraf)** - Metrics collection agent

### Logging
- **[Elasticsearch](/technical/elasticsearch)** - Search and analytics
- **[Logstash](/technical/logstash)** - Log processing pipeline
- **[Fluentd](/technical/fluentd)** - Unified logging layer
- **[Fluent Bit](/technical/fluent-bit)** - Fast log processor
- **[Loki](/technical/loki)** - Like Prometheus for logs
- **[Vector](/technical/vector)** - High-performance observability pipeline

### Tracing
- **[Jaeger](/technical/jaeger)** - Distributed tracing
- **[Zipkin](/technical/zipkin)** - Distributed tracing system
- **[Tempo](/technical/tempo)** - Grafana's tracing backend
- **[OpenTelemetry](/technical/opentelemetry)** - Observability framework

### APM & Commercial
- **[Datadog](/technical/datadog)** - Cloud monitoring platform
- **[New Relic](/technical/new-relic)** - Application performance
- **[AppDynamics](/technical/appdynamics)** - Business monitoring
- **[Splunk](/technical/splunk)** - Data platform

### Incident Management
- **[PagerDuty](/technical/pagerduty)** - Incident response
- **[Opsgenie](/technical/opsgenie)** - Alert management
- **[VictorOps](/technical/victorops)** - Incident management
- **[SRE Practices](/technical/sre-practices-incident-management)** ✅ - On-call, postmortems

---

## 💾 Databases & Storage

Manage data persistence and storage at scale.

### Relational Databases
- **[PostgreSQL](/technical/postgresql)** - Advanced open source DB
- **[MySQL](/technical/mysql)** - Popular open source DB
- **[MariaDB](/technical/mariadb)** - MySQL fork
- **[Amazon RDS](/technical/rds)** - Managed relational DB

### NoSQL Databases
- **[MongoDB](/technical/mongodb)** - Document database
- **[Cassandra](/technical/cassandra)** - Wide column store
- **[DynamoDB](/technical/dynamodb)** - AWS managed NoSQL
- **[CouchDB](/technical/couchdb)** - JSON document DB

### Key-Value Stores
- **[Redis](/technical/redis)** - In-memory data structure store
- **[Memcached](/technical/memcached)** - Memory caching system
- **[etcd](/technical/etcd)** - Distributed key-value store
- **[Consul](/technical/consul-kv)** - Service mesh with KV store

### Time Series Databases
- **[InfluxDB](/technical/influxdb-tsdb)** - Purpose-built for metrics
- **[TimescaleDB](/technical/timescaledb)** - PostgreSQL for time series
- **[Prometheus](/technical/prometheus-tsdb)** - Built-in TSDB

### NewSQL & Distributed
- **[CockroachDB](/technical/cockroachdb)** - Distributed SQL
- **[TiDB](/technical/tidb)** - MySQL-compatible distributed DB
- **[YugabyteDB](/technical/yugabyte)** - Distributed SQL

### Object Storage
- **[MinIO](/technical/minio)** - S3-compatible object storage
- **[Ceph](/technical/ceph)** - Distributed storage system
- **[GlusterFS](/technical/glusterfs)** - Scalable network filesystem
- **[Object Storage Overview](/technical/object-storage)** - S3, GCS, Azure Blob

### Search & Analytics
- **[Elasticsearch](/technical/elasticsearch-search)** - Full-text search
- **[OpenSearch](/technical/opensearch)** - Open source search
- **[ClickHouse](/technical/clickhouse)** - Column-oriented DBMS

---

## 💻 Programming Languages

Essential languages for platform engineering and automation.

### Primary Languages
- **[Python](/technical/python)** - Automation, tooling, scripting
- **[Go](/technical/go)** - Systems programming, cloud native
- **[Bash](/technical/bash)** - Shell scripting, automation

### Secondary Languages
- **[JavaScript/Node.js](/technical/javascript)** - Full-stack, tooling
- **[TypeScript](/technical/typescript)** - Type-safe JavaScript
- **[Rust](/technical/rust)** - Systems programming
- **[Ruby](/technical/ruby)** - Scripting, configuration

### Configuration Languages
- **[YAML](/technical/yaml)** - Human-readable data serialization
- **[JSON](/technical/json)** - Data interchange format
- **[TOML](/technical/toml)** - Configuration files
- **[HCL](/technical/hcl)** - HashiCorp Configuration Language

### Utilities
- **[Regular Expressions](/technical/regex)** - Pattern matching
- **[jq](/technical/jq)** - Command-line JSON processor
- **[yq](/technical/yq)** - YAML processor

---

## 🔐 Security Tools

Secure infrastructure and applications.

### Secrets Management
- **[HashiCorp Vault](/technical/vault)** - Secrets and encryption management
- **[AWS Secrets Manager](/technical/aws-secrets)** - AWS native secrets
- **[SOPS](/technical/sops)** - Secrets operations
- **[Sealed Secrets](/technical/sealed-secrets)** - K8s secrets encryption

### Identity & Access
- **[Keycloak](/technical/keycloak)** - Identity and access management
- **[OAuth2 Proxy](/technical/oauth2-proxy)** - Reverse proxy authentication
- **[Okta](/technical/okta)** - Identity platform
- **[LDAP/Active Directory](/technical/ldap)** - Directory services

### Security Scanning
- **[Trivy](/technical/trivy)** - Vulnerability scanner
- **[Snyk](/technical/snyk)** - Developer security platform
- **[SonarQube](/technical/sonarqube)** - Code quality and security
- **[OWASP ZAP](/technical/owasp-zap)** - Web app security testing

### Policy & Compliance
- **[Open Policy Agent](/technical/opa-security)** - Policy engine
- **[Gatekeeper](/technical/gatekeeper)** - K8s policy controller
- **[Kyverno](/technical/kyverno)** - K8s native policies
- **[Security Compliance](/technical/security-compliance)** ✅ - Standards, frameworks

### Certificate Management
- **[cert-manager](/technical/cert-manager)** - K8s certificate management
- **[Let's Encrypt](/technical/lets-encrypt)** - Free SSL/TLS certificates

---

## 📨 Messaging & Streaming

Build event-driven architectures and real-time data pipelines.

### Message Brokers
- **[Apache Kafka](/technical/kafka)** - Distributed streaming platform
- **[RabbitMQ](/technical/rabbitmq)** - Message broker
- **[Apache Pulsar](/technical/pulsar)** - Cloud-native messaging
- **[NATS](/technical/nats)** - Cloud-native messaging system

### Cloud Messaging
- **[AWS SQS/SNS](/technical/aws-messaging)** - Queue and pub/sub
- **[Google Pub/Sub](/technical/gcp-pubsub)** - Global message bus
- **[Azure Service Bus](/technical/azure-service-bus)** - Enterprise messaging

### Protocols & Patterns
- **[MQTT](/technical/mqtt)** - IoT messaging protocol
- **[AMQP](/technical/amqp)** - Messaging protocol
- **[Redis Pub/Sub](/technical/redis-pubsub)** - Simple pub/sub
- **[Event-Driven Architecture](/technical/message-queues-event-driven)** ✅ - Patterns and practices

---

## 🛠️ Additional Tools

### Development Tools
- **[VS Code](/technical/vscode)** - Popular code editor
- **[vim/neovim](/technical/vim)** - Terminal-based editor
- **[tmux](/technical/tmux)** - Terminal multiplexer
- **[Docker Compose](/technical/docker-compose)** - Multi-container apps

### API Tools
- **[Postman](/technical/postman)** - API development
- **[gRPC](/technical/grpc)** - High-performance RPC
- **[GraphQL](/technical/graphql)** - Query language for APIs
- **[API Design](/technical/api-design-protocols)** ✅ - REST, GraphQL, gRPC

### Testing Tools
- **[k6](/technical/k6)** - Modern load testing
- **[JMeter](/technical/jmeter)** - Performance testing
- **[Gatling](/technical/gatling)** - Load testing framework
- **[Selenium](/technical/selenium)** - Browser automation

### Cost Management
- **[Kubecost](/technical/kubecost)** - K8s cost monitoring
- **[Infracost](/technical/infracost)** - Cloud cost estimates
- **[Cloud Custodian](/technical/cloud-custodian)** - Rules engine

### Backup & DR
- **[Velero](/technical/velero)** - K8s backup and restore
- **[Restic](/technical/restic)** - Fast, secure backup
- **[Disaster Recovery](/technical/disaster-recovery)** - Strategies and tools

### Documentation
- **[Confluence](/technical/confluence)** - Team collaboration
- **[Markdown](/technical/markdown)** - Documentation format
- **[PlantUML](/technical/plantuml)** - Diagram as code
- **[Draw.io](/technical/drawio)** - Diagramming tool

---

## 🎯 Learning Paths

### For Beginners
1. Start with **[Linux Fundamentals](/technical/linux-fundamentals)** ✅
2. Learn **[Docker](/technical/docker)** ✅ and basic **[Git](/technical/git)**
3. Pick one cloud: **[AWS](/technical/aws)** ✅ (recommended)
4. Master **[Python](/technical/python)** or **[Go](/technical/go)**
5. Understand **[Prometheus](/technical/prometheus)** and **[Grafana](/technical/grafana)**

### For Developers → Platform Engineers
1. Focus on **[Kubernetes](/technical/kubernetes)** ✅ and **[Terraform](/technical/terraform)** ✅
2. Deep dive into **[Cloud Networking](/technical/cloud-networking)**
3. Learn **[Ansible](/technical/ansible)** for configuration
4. Master **[CI/CD](/technical/github-actions)** with GitHub Actions
5. Understand **[Observability](/technical/opentelemetry)** principles

### For Experienced Engineers
1. Master **[Service Mesh](/technical/istio)** architectures
2. Implement **[GitOps](/technical/argocd)** with ArgoCD
3. Learn **multiple cloud platforms**
4. Deep dive into **[Security](/technical/vault)** and compliance
5. Focus on **[Cost Optimization](/technical/kubecost)**

---

## 📈 Industry Trends (2025)

### 🔥 Hot Technologies
- **Platform Engineering** - Internal developer platforms
- **FinOps** - Cloud financial management
- **eBPF** - Kernel programming for observability
- **WebAssembly** - WASM for edge computing
- **AI/ML Infrastructure** - GPU clusters, vector databases

### 📉 Declining Technologies
- Traditional configuration management (Puppet, Chef)
- Monolithic CI/CD platforms
- Legacy monitoring (Nagios, Zabbix)
- Hardware load balancers

---

## 🏗️ Building Your Skills

1. **Start with fundamentals** - Don't skip Linux and networking basics
2. **Get hands-on experience** - Build real projects, not just tutorials
3. **Focus on one area** - Master one technology stack before expanding
4. **Join communities** - Participate in Slack channels, forums, conferences
5. **Contribute to open source** - Best way to learn from experts

---

**Legend**: ✅ = Guide available | 🚧 = Coming soon

Ready to dive in? Start with the fundamentals or jump to the technology you need to master!