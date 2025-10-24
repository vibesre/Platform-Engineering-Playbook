# Episode Outline: AWS State of the Union 2025

**Episode Number**: 00006
**Target Duration**: 25-30 minutes
**Target Audience**: Senior platform engineers (5+ years) who either haven't touched AWS in 2+ years or primarily work with Azure/GCP
**Related Content**: Will be embedded on /technical/aws page

## Story Planning

**NARRATIVE STRUCTURE**: Skills Evolution Arc + Economic Detective (Hybrid)

**CENTRAL TENSION**: AWS has 200+ services and launches thousands of features annually. For experienced engineers, the challenge isn't learning cloud concepts—it's strategic service selection. Which 20 services actually matter? What skills translate to higher compensation? How do you navigate complexity without getting lost?

**THROUGHLINE**: From AWS overwhelm (200+ services, confusing pricing, documentation loops) to strategic clarity (the essential 20 services, career ROI framework, practical starting points based on your situation).

**EMOTIONAL ARC**:
- **Recognition moment**: "You're an experienced engineer. You know clouds. But AWS has 200+ services with names like 'Elastic Beanstalk' and 'Systems Manager.' Where the hell do you even start?" [Listener: "YES, this is exactly my problem"]
- **Surprise moments**:
  - AWS dropped prices 100+ times, but egress fees and 197 monthly price changes create hidden complexity
  - Generic "AWS knowledge" pays $124K (B-tier) while AWS Lambda specialization pays $127K, but Elasticsearch pays $139K—the real money is in specialized tools, not cloud platforms
  - EKS Auto Mode changes the Kubernetes story—what was hard in 2023 is simplified in 2025
- **Empowerment moment**: Clear decision frameworks for service selection, where to start based on your background (Azure/GCP/returning to AWS), and what to learn for career growth vs what's becoming commoditized

## Act Structure

### ACT 1: SETUP - The AWS Dominance Paradox (3-4 minutes)

**Hook**: "You're an experienced platform engineer. You understand compute, storage, networking, databases. You've heard AWS has 200+ services. The documentation is a maze of tabs and interlinked articles. You search for 'how to run a container' and get six different answers: ECS, EKS, Fargate, App Runner, Elastic Beanstalk, Lightsail. Where the hell do you even start?"

**Stakes**:
- AWS maintains 30% market share with 4.19 million customers—you can't avoid it
- Platform engineers spend 30-40% of their time on infrastructure decisions
- Wrong service choices = technical debt that compounds for years
- Career implications: Generic AWS knowledge is B-tier ($124K), specialized expertise varies from A-tier to S-tier

**Promise**: By the end of this episode, you'll have a mental map of AWS in 2025—which services matter, what AWS does better than anyone, where it frustrates even experienced engineers, how to navigate pricing complexity, and most importantly, which AWS skills actually translate to career growth vs which are becoming commoditized.

**Key Points**:
- AWS dominance: 30% market share (vs Azure 20%, GCP 13%), $90B+ revenue, but "Big Three" control 60%+ combined
- The complexity problem: 200+ services, but 80/20 rule applies (20 services solve 80% of problems)
- 2025 landscape: re:Invent 2024 brought Trainium3 AI chips (4x faster), Amazon Nova models, EKS Auto Mode (Kubernetes simplified), European Sovereign Cloud (€7.8B investment)
- What changed since 2023: AI/ML dominance push, serverless maturity (cold starts mostly solved), cost transparency pressure

**Narrative Technique**: Set up the "overwhelming service catalog" problem, then promise we'll cut through to what actually matters

---

### ACT 2: THE ESSENTIAL SERVICES - Core AWS (6-8 minutes)

**Discovery 1: Compute - More Options Than You Need**

The compute layer has six ways to run code, but they serve different philosophies:

**EC2 (Elastic Compute Cloud)**:
- Still foundational—can't escape it completely
- When: Legacy apps, specific instance types, maximum control
- Reality check: Most teams abstract above this now
- Career note: Pure EC2 expertise is commoditizing

**Lambda (Serverless Functions)**:
- $127,769 average salary (A-tier from Dice 2025)
- Cold start concerns mostly solved in 2025 (provisioned concurrency, SnapStart)
- When: Event-driven, unpredictable traffic, true pay-per-use
- Gotcha: Watch egress costs, 15-minute execution limit

**ECS (Elastic Container Service)**:
- AWS's "simpler" container orchestration
- When: You want containers without Kubernetes complexity
- Integrates deeply with AWS services (CloudWatch, IAM, ALB)

**EKS (Elastic Kubernetes Service)**:
- EKS Auto Mode (re:Invent 2024): Automates compute, storage, networking management
- EKS Hybrid Nodes: Run on-premises infrastructure in EKS clusters
- When: You need Kubernetes (portability, ecosystem, team expertise)
- 2025 reality: Much more production-ready than 2022, but still Kubernetes complexity

**Fargate**:
- Serverless containers (no EC2 management)
- Cold start not an issue like Lambda—container image lazy loading with SOCI
- When: "I just want to run containers without thinking about servers"
- Cost: Premium over EC2, but factor in operational overhead

**App Runner / Elastic Beanstalk / Lightsail**:
- Higher-level PaaS abstractions
- When: You want Heroku-like simplicity on AWS
- Reality: Most experienced engineers don't use these—too opinionated, limited control

**Key Insight**: For experienced engineers in 2025:
- Start with Fargate or Lambda unless you have specific EC2 needs
- EKS if you're committed to Kubernetes (and have the team capacity)
- Avoid Elastic Beanstalk—complexity without flexibility

**Discovery 2: Storage - S3 and Friends**

**S3 (Simple Storage Service)**:
- The service you absolutely cannot avoid
- 99.999999999% durability (11 nines), the pricing model everything else copies
- Storage classes: Standard ($0.023/GB), Intelligent-Tiering (auto-optimize), Glacier (archive)
- Watch out: Data transfer out starts at $0.09/GB (vs DigitalOcean's $0.01/GB)

**EBS (Elastic Block Storage)**:
- Attached storage for EC2 instances
- Types: gp3 (general purpose), io2 (high IOPS), st1 (throughput optimized)
- When: Database storage, persistent volumes

**EFS (Elastic File System)**:
- NFS for multiple EC2 instances
- When: Shared file access, legacy app migrations

**Key Decision Tree**:
- Object storage (files, backups, static assets) → S3
- Block storage (databases on EC2) → EBS
- Shared filesystem (NFS-like) → EFS
- Archive (compliance, cold data) → S3 Glacier

**Discovery 3: Databases - The Decision Paralysis Problem**

AWS has 15+ database services. Here's the honest hierarchy:

**Start Here Tier**:
- **RDS (Relational Database Service)**: Managed PostgreSQL, MySQL, MariaDB, SQL Server
  - When: You need a relational database and don't want to manage servers
  - Reality: Fine for 90% of use cases

- **Aurora**: AWS's MySQL/PostgreSQL-compatible, cloud-native DB
  - When: You need better performance/scaling than RDS and can afford premium pricing
  - Benefit: 5x throughput of MySQL, 3x PostgreSQL, auto-scaling storage
  - Warning: Vendor lock-in (not actual PostgreSQL/MySQL)

**Specialized Tier**:
- **DynamoDB**: NoSQL key-value/document store
  - When: You need single-digit millisecond latency at any scale
  - Learning curve: Different mental model (partition keys, sort keys, GSIs)
  - Career note: DynamoDB expertise is niche but valuable

**Only If You Have Specific Needs**:
- **Redshift**: Data warehousing ($134,103 salary—A-tier from our episode 00005)
- **ElastiCache** (Redis/Memcached): Caching layer (Redis expertise: $136,357—S-tier)
- **DocumentDB**: MongoDB-compatible (but not actually MongoDB)
- **Neptune**: Graph database
- **Timestream**: Time-series

**Key Insight**:
- 80% of teams: Start with RDS PostgreSQL
- Need performance/scale: Aurora (pay the premium)
- NoSQL required: DynamoDB (but understand the commitment)
- Data warehousing: Redshift (specialized skill, commands premium salary)

**Throughline Check**: We've now covered the foundation—compute, storage, databases. These are the services you can't avoid. But notice the pattern: AWS gives you 5-6 options for each problem domain. The skill isn't learning all of them—it's knowing which one fits your constraints.

---

### ACT 3: THE MODERN STACK - Networking, Developer Tools, AI/ML (6-8 minutes)

**Discovery 4: Networking - Where Costs Hide**

**VPC (Virtual Private Cloud)**:
- The network isolation boundary for everything
- Concepts: Subnets, route tables, internet gateways, NAT gateways
- For Azure engineers: More manual than Azure's integrated networking
- For GCP engineers: More complex than GCP's global VPC model

**The Egress Fee Trap**:
- Data transfer OUT of AWS: $0.09/GB for first 10TB (scales down to $0.05/GB after 150TB)
- Inter-regional transfer: $0.02/GB
- Between availability zones: $0.01/GB
- First 100GB/month free, but complexity hides in architecture
- Reality: Data transfer is where surprise bills come from
- Comparison: DigitalOcean charges flat $0.01/GB for all transfer

**CloudFront (CDN)**:
- Lower egress costs than direct S3 ($0.085/GB vs $0.09/GB)
- Use it as an egress cost optimization, not just CDN

**Load Balancers**:
- ALB (Application Load Balancer): HTTP/HTTPS, path-based routing
- NLB (Network Load Balancer): TCP/UDP, ultra-low latency
- Classic Load Balancer: Legacy, ignore it
- How many load balancer types does AWS need? This is the "backwards compatibility burden" in action

**Key Insight**: Networking on AWS is more complex than Azure/GCP, but understanding VPC architecture and egress costs is critical. Bad network design = thousand-dollar monthly surprises.

**Discovery 5: Developer Services - Infrastructure as Code**

**CloudFormation**:
- AWS-native IaC, JSON/YAML templates
- Verbose but complete AWS service coverage
- When: You're all-in on AWS and want native integration

**AWS CDK (Cloud Development Kit)**:
- Define infrastructure in TypeScript, Python, Java, C#, Go
- Synthesizes to CloudFormation
- When: You prefer programming languages to YAML hell
- 2025 reality: CDK is maturing, less "rough edges" than 2022

**Terraform (not AWS, but relevant)**:
- 9.9k GitHub stars on terraform-provider-aws
- Multi-cloud, larger community, HCL syntax
- Trade-off: Slightly behind AWS feature releases, but more portable

**CodePipeline / CodeBuild / CodeDeploy**:
- AWS-native CI/CD
- Reality check: Most teams use GitHub Actions, GitLab CI, or Jenkins
- When: Deep AWS integration needs, compliance requires AWS-native

**CloudWatch**:
- Centralized logging, metrics, alarms
- Integrates with everything AWS
- Pain point: Query language less powerful than Splunk/Datadog
- Cost: Can get expensive at scale

**Key Insight**: IaC on AWS = CloudFormation for AWS-only, CDK for developer experience, or Terraform for multi-cloud. Don't try to use CodePipeline unless you have specific requirements—stick with your existing CI/CD.

**Discovery 6: AI/ML - The 2025 Strategic Push**

AWS is making a major play for AI workloads after being perceived as behind Azure (OpenAI partnership) and GCP (Google's AI heritage):

**Amazon Bedrock**:
- Managed foundation models (Anthropic Claude, Meta Llama, Amazon Nova, etc.)
- When: You want to use LLMs without managing infrastructure
- 100+ models in Bedrock Marketplace (re:Invent 2024)

**Amazon Nova** (New - re:Invent 2024):
- AWS's own foundation models
- Text, image, video processing and generation
- Competing with OpenAI, Anthropic, Google Gemini

**SageMaker**:
- Full ML platform—build, train, deploy models
- SageMaker HyperPod: Reduces training time by 40%
- Reality: High learning curve, significant
- When: You're training custom models at scale

**Trainium3 Chips** (Coming late 2025):
- 4x performance over Trn2
- AWS competing with NVIDIA dominance
- When: Large-scale model training

**Key Insight**:
- Most teams: Start with Bedrock for LLM integration (managed, simple)
- Custom model training: SageMaker (but expect learning curve)
- AWS is catching up on AI, but Azure (OpenAI partnership) and GCP (Vertex AI, TPUs) had head starts
- Career note: ML/AI skills command $132,150 (S-tier from episode 00005), NLP at $131,621 (+21% YoY growth)

**Throughline Check**: We've covered the essential services across six categories. Pattern emerging: AWS gives you more options than you need, the skill is strategic selection. Now let's talk about what AWS does better than anyone, and where it frustrates even experienced engineers.

---

### ACT 4: REALITY CHECK - What AWS Does Well, What It Doesn't (4-5 minutes)

**What AWS Does Better Than Anyone**:

1. **Maturity and Reliability at Scale**:
   - 18+ years of production experience
   - 33 regions, 105 availability zones (vs Azure 64 regions, GCP 40)
   - When AWS has an outage, half the internet goes down—but outages are rare
   - For GCP engineers: AWS's stability/maturity is noticeably better

2. **Service Breadth**:
   - If you need something obscure (quantum computing? satellite ground stations?), AWS probably has it
   - "Primitives" philosophy: Building blocks vs opinionated solutions
   - Maximum flexibility for complex architectures

3. **Ecosystem and Job Market**:
   - Largest community, most third-party integrations
   - Job market: More AWS roles than Azure+GCP combined
   - Open Guide to AWS: 35.7k GitHub stars (community-driven knowledge)
   - Massive AWS Partner Network

4. **Global Infrastructure**:
   - Edge locations for CloudFront: 400+ points of presence
   - Data residency options for compliance
   - Inter-region replication for disaster recovery

**What AWS Does Poorly (The Honest Take)**:

1. **Pricing Complexity and Hidden Costs**:
   - AWS averages 197 distinct monthly price changes (vs Azure/GCP changing a few times)
   - Egress fees: $0.09/GB vs DigitalOcean's $0.01/GB flat rate
   - Data transfer between AZs: $0.01/GB (you pay to move data in your own infrastructure!)
   - "Data transfer is the blind spot that silently drains cloud budgets"
   - Cost Explorer helps, but requires diligence

2. **Documentation Overwhelm**:
   - Community complaint: "Needing to juggle multiple tabs and navigate through loops of interlinked articles"
   - Service docs are comprehensive but not beginner-friendly
   - Contrast with GCP: More opinionated, clearer paths

3. **Service Naming Confusion**:
   - What's the difference between ECS, EKS, Fargate, App Runner, Elastic Beanstalk?
   - Why is "Elastic Beanstalk" the name for a PaaS?
   - Systems Manager, Service Catalog, Control Tower—which org tools do you need?

4. **Backwards Compatibility Burden**:
   - AWS can't break existing APIs, so they layer new services alongside old
   - Result: Four types of load balancers when you need two
   - Classic Load Balancer still exists (legacy), but you need to know to ignore it
   - Contrast: GCP can make cleaner design decisions (smaller customer base, less legacy)

5. **Console UI Inconsistency**:
   - Different UX paradigms across services (acquired companies, different teams)
   - CloudFormation UI vs CDK vs console clicks = three different experiences
   - Power users avoid console, use CLI/IaC

**Key Insight**: AWS's strength (maturity, breadth, flexibility) creates its weakness (complexity, pricing opacity, cognitive load). The platform rewards engineers who learn to navigate complexity, but punishes teams who don't have that expertise.

**For Azure Engineers Switching**:
- AWS is less integrated, more manual, steeper learning curve
- But more flexibility once you learn the primitives

**For GCP Engineers Switching**:
- AWS has more services, larger ecosystem, better third-party support
- But less opinionated, more network complexity, CloudFormation vs Deployment Manager verbosity

---

### ACT 5: SKILLS STRATEGY & CAREER IMPLICATIONS (4-5 minutes)

**The Compensation Reality Check** (Callback to Episode 00005):

From the Dice 2025 Tech Salary Report analyzing 220+ skills:

**Generic AWS Knowledge**:
- "Cloud Computing" (generic): $124,796/year (B-tier)
- This is the "I have AWS Solutions Architect cert and know the basics" salary
- Reality: With 93% of companies using Kubernetes and universal Docker knowledge, cloud platforms have become commodity skills

**AWS-Specific Specializations** (A-tier):
- AWS Lambda expertise: $127,769/year
- Amazon Redshift: $134,103/year (+15% YoY)
- ~$3K-9K premium over generic AWS

**But Here's the Surprise**:
- Elasticsearch: $139,549/year (S-tier)
- Apache Kafka: $136,526/year (S-tier)
- Redis: $136,357/year (S-tier)
- PostgreSQL: $131,315/year (S-tier)

**The Pattern**: Specialized tool expertise outearns cloud platform expertise by $15K-24K/year.

**Why This Matters**:
- Deep AWS Lambda knowledge: A-tier ($127K)
- Deep Elasticsearch running on AWS: S-tier ($139K) = $12K/year difference
- The real money isn't in knowing AWS—it's in solving expensive business problems with specialized tools that happen to run on AWS

**Career Strategy Framework**:

**Phase 1: Foundation (Everyone needs this)**:
- Core services: EC2, S3, VPC, IAM, RDS
- IaC: CloudFormation or Terraform
- Cost management: Billing alerts, Cost Explorer, tagging strategy
- Target: $115-125K (B-tier, entry to mid-level)

**Phase 2: AWS Specialization (Pick ONE)**:
Path A - Serverless: Lambda, API Gateway, DynamoDB, Step Functions → $127K (A-tier)
Path B - Containers: EKS/ECS, Fargate, ECR, service mesh → $125-130K (A/B-tier)
Path C - Data: Redshift, EMR, Glue, Athena → $134K (A-tier)

**Phase 3: S-Tier Specialization (The Real Money)**:
Don't just learn AWS—layer specialized tools:
- Data & Search: RDS → Aurora → Elasticsearch ($139K)
- Event Streaming: Kinesis → Kafka on AWS ($136K)
- Caching & Performance: ElastiCache → Redis expertise ($136K)
- Observability: CloudWatch → ELK Stack → OpenTelemetry ($125-135K)

**Key Insight**: AWS certifications are table stakes (everyone has them), AWS service knowledge is foundation (B-tier), but specialized tool expertise running on AWS is where the premium salaries are (S-tier).

**What's Losing Value**:
- Generic cloud certifications without specialization
- Pure EC2 expertise (abstracted away)
- Manual console clicking (IaC is mandatory)
- Certification collecting (5 certs doesn't beat deep expertise in one valuable tool)

**What's Gaining Value**:
- Cost optimization expertise (FinOps)
- AI/ML platform engineering (Bedrock, SageMaker integration)
- Multi-cloud architecture (hybrid AWS + GCP/Azure strategies)
- Security automation (not just IAM, but Policy-as-Code, CSPM)

---

### ACT 6: PRACTICAL GUIDANCE & CLOSING WISDOM (2-3 minutes)

**Where to Start: Three Scenarios**

**Scenario 1: Coming Back to AWS After 2+ Years**

What's the same:
- Core services stable: EC2, S3, VPC, IAM, RDS
- Fundamentals haven't changed
- Well-Architected Framework still the best starting point

What's different:
- Kubernetes story matured: EKS Auto Mode simplifies management
- Serverless evolved: Lambda cold starts mostly solved, Fargate is production-ready
- AI/ML accessible: Bedrock makes LLMs simple, SageMaker HyperPod reduces training time 40%
- Cost management critical: Enable Cost Explorer day one, set billing alerts

**Start here**:
1. Review AWS Well-Architected Framework (updated for 2025)
2. Hands-on: Deploy a simple app with Fargate or Lambda
3. Set up IaC (CDK or Terraform) from day one
4. Watch egress costs (review Cost Explorer weekly)

**Scenario 2: Azure Engineer Moving to AWS**

Mindset shift:
- Azure: Integrated, opinionated, portal-driven
- AWS: Primitives, flexible, CLI/IaC-driven
- Steeper learning curve, but more flexibility

Translation guide:
- Azure VMs → EC2
- Azure Functions → Lambda
- Azure SQL Database → RDS
- Azure Blob Storage → S3
- Azure Virtual Network → VPC (but more manual)
- Azure Resource Manager → CloudFormation
- Azure DevOps → CodePipeline (but consider keeping GitHub Actions/GitLab)

Expect friction: Networking is more complex, egress costs surprise you, console UX is less polished.

**Scenario 3: GCP Engineer Moving to AWS**

Mindset shift:
- GCP: Clean abstractions, opinionated, newer design
- AWS: More services, larger ecosystem, legacy baggage
- More options but also more decisions

Translation guide:
- Compute Engine → EC2
- Cloud Functions → Lambda
- Cloud SQL → RDS
- Cloud Storage → S3
- Cloud Run → Fargate or App Runner
- Deployment Manager → CloudFormation
- BigQuery → Redshift (but BigQuery is better for analytics)

Expect friction: Global VPC → manual VPC peering, simpler networking becomes more complex, CloudFormation verbosity vs Deployment Manager, pricing changes constantly (197/month vs GCP's few).

**Key Advice Across All Scenarios**:

1. **Apply the 80/20 Rule**: 20 services solve 80% of problems
   - Compute: Lambda or Fargate
   - Storage: S3 + EBS
   - Database: RDS PostgreSQL
   - Networking: VPC + CloudFront
   - Developer: CloudFormation/CDK, CloudWatch
   - Learn these deeply before exploring specialized services

2. **Pricing Discipline is Engineering Discipline**:
   - Enable Cost Explorer immediately
   - Set billing alerts at multiple thresholds
   - Tag everything for cost allocation
   - Review weekly, not monthly
   - Watch data transfer patterns

3. **IaC from Day One**:
   - Don't learn AWS via console clicking
   - CloudFormation (AWS-native) or Terraform (multi-cloud)
   - Version control your infrastructure
   - Treat infrastructure like code reviews

4. **Build Depth, Not Breadth**:
   - Don't try to learn all 200 services
   - Master the core 20, get deep in 2-3 specialized areas
   - One S-tier specialization (Elasticsearch, Kafka, Redis) > five AWS certs

5. **Leverage the Ecosystem**:
   - Open Guide to AWS (35.7k stars)
   - AWS re:Post for Q&A
   - YouTube re:Invent sessions (annual conference)
   - Community: r/aws, AWS Heroes, local user groups

**The Meta Insight**: AWS rewards engineers who understand both the services AND the business context. Knowing Lambda is good. Knowing when Lambda's $127K average salary makes sense vs when a $139K Elasticsearch specialization delivers more value—that's the strategic thinking that sets senior platform engineers apart.

**Closing Throughline Callback**:

We started with the AWS overwhelm problem: 200+ services, confusing docs, where to even start?

Here's what we discovered:
- Only ~20 services matter for 80% of work
- AWS's strength (maturity, breadth) creates its weakness (complexity, pricing opacity)
- Generic AWS knowledge is B-tier ($124K), but specialized tools on AWS are S-tier ($135-139K)
- The skill isn't learning every service—it's strategic selection based on your constraints, career goals, and what problems you're actually solving

AWS in 2025 isn't about knowing everything. It's about knowing what matters, understanding the trade-offs, and building depth in areas that solve expensive business problems.

The fundamentals of good platform engineering remain constant: solve real problems, measure impact, build with constraints in mind. AWS is just the latest—and most comprehensive—set of tools in your toolkit.

---

## Story Elements

**KEY CALLBACKS**:
- Opening: "200+ services, where to start?" → Closing: "Only 20 matter, here's the map"
- Act 2: Generic AWS knowledge is B-tier → Act 5: Specialized tools are S-tier, here's the gap
- Act 3: Egress fees hidden in architecture → Act 6: Cost discipline is engineering discipline
- Act 4: AWS complexity burden → Act 6: Strategic selection, not comprehensive knowledge

**NARRATIVE TECHNIQUES**:
- **Anchoring Statistics**:
  - 200+ services (overwhelm) → 20 services (clarity)
  - $124K generic AWS (B-tier) → $139K specialized tools (S-tier) → $15-24K career gap
  - 197 monthly AWS price changes (complexity) vs Azure/GCP's few (simplicity)
- **Service Category Pattern**: Each act builds service knowledge (Compute → Storage → Database → Network → Developer → AI/ML)
- **For X Engineers Switching**: Translate concepts for Azure/GCP backgrounds
- **Three Scenario Framework**: Where to start based on listener's situation
- **Throughline Arc**: Overwhelm → Strategic Map → Empowered Decision-Making

**SUPPORTING DATA**:
- AWS market share: 30% (Q2 2025), $90B+ revenue, 4.19M customers
- re:Invent 2024: Trainium3 (4x performance), Amazon Nova models, EKS Auto Mode
- Dice 2025 Salary Report: 220+ skills analyzed, AWS Lambda $127K, Elasticsearch $139K, Kafka $136K
- Pricing: Egress $0.09/GB (AWS) vs $0.01/GB (DigitalOcean), 197 monthly price changes
- Lambda cold starts mostly solved (provisioned concurrency, SnapStart)
- EKS Auto Mode simplifies Kubernetes management
- 93% Kubernetes adoption, universal Docker knowledge (skills commoditization)

## Quality Checklist

- [x] Throughline is clear: AWS overwhelm → strategic service map → career ROI clarity
- [x] Hook is compelling: "200+ services, where to start?" speaks to target audience pain
- [x] Each section builds: Act 1 (setup) → Acts 2-3 (service deep dives) → Act 4 (honest assessment) → Act 5 (career strategy) → Act 6 (practical guidance)
- [x] Insights connect: Service categories → AWS strengths/weaknesses → career implications → starting points
- [x] Emotional beats land: Recognition (overwhelm), surprise (pricing complexity, salary gaps), empowerment (decision frameworks)
- [x] Callbacks create unity: Return to 200+ services, salary tier list, pricing complexity
- [x] Payoff satisfies: Delivers on promise—clear AWS map, which services matter, career strategy, practical starting points
- [x] Narrative rhythm: Flows as discovery journey, not bullet list
- [x] Technical depth maintained: Real service recommendations, honest trade-offs, specific salary data
- [x] Listener value clear: Strategic service selection, career ROI framework, where to start based on background

**Target Length Validation**:
- Act 1: 3-4 min (setup)
- Act 2: 6-8 min (compute, storage, database)
- Act 3: 6-8 min (networking, developer tools, AI/ML)
- Act 4: 4-5 min (what AWS does well/poorly)
- Act 5: 4-5 min (skills strategy, compensation)
- Act 6: 2-3 min (practical guidance, closing)
- **Total: 25-33 minutes** ✓

This outline balances technical depth (service categories, architectural decisions) with strategic guidance (career implications, where to start) for the experienced platform engineer audience.
