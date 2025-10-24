---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #006: AWS State of the Union 2025"
slug: 00006-aws-state-of-the-union-2025
---

# AWS State of the Union 2025 - Navigate 200+ Services with Strategic Clarity

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 33 minutes 31 seconds
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Explore the [AWS technical guide](/technical/aws)**: Comprehensive learning resources, certification prep, and best practices for mastering Amazon Web Services.

<iframe width="560" height="315" src="https://www.youtube.com/embed/dfW6eVdCWi0" title="AWS State of the Union 2025" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

---

**Jordan**: Today we're diving into AWS in 2025. And here's the thing - you're an experienced platform engineer. You understand compute, storage, networking. But AWS has over 200 services, and the documentation is this maze of tabs and interlinked articles. You search for "how to run a container" and you get six different answers: ECS, EKS, Fargate, App Runner, Elastic Beanstalk, Lightsail. Where the hell do you even start?

**Alex**: That's the paradox of AWS. It's the most dominant cloud platform - thirty percent market share, over a hundred billion in annual revenue. You can't avoid it. But the breadth that makes it powerful also makes it overwhelming. And I think this episode is especially relevant if you're coming back to AWS after a couple years, or if you've been living in Azure or GCP and need to understand what you're actually dealing with.

**Jordan**: Right. Because the core concepts haven't changed. You know what a server is, what object storage means, how databases work. The challenge isn't learning cloud fundamentals - it's strategic service selection. Which twenty services out of those two hundred actually matter?

**Alex**: And equally important - which AWS skills translate to higher compensation versus which ones are becoming commoditized. Because spoiler alert from our tier list episode - generic AWS knowledge pays about a hundred twenty-four thousand, which is B-tier. But we'll get into what actually commands the premium salaries.

**Jordan**: Let's start with compute, because this is where the service proliferation is most obvious. How many ways can you run code on AWS?

**Alex**: At least six distinct options. EC2, Lambda, ECS, EKS, Fargate, and then these higher-level things like App Runner and Elastic Beanstalk. Each one represents a different philosophy.

**Jordan**: Walk me through EC2 first, because that's the foundation everything else abstracts away from.

**Alex**: EC2 is Elastic Compute Cloud. It's virtual machines - you pick an instance type, you get a server, you manage everything above the hypervisor. It's been around since two thousand six, and it's still foundational. You can't completely escape it.

**Jordan**: But most teams are abstracting above it now, right?

**Alex**: Exactly. EC2 made sense when cloud was new and you were lifting-and-shifting from data centers. In 2025, if you're starting fresh, you probably want a higher-level abstraction. But you'll still encounter it - maybe for legacy apps, maybe because you need specific instance types, maybe for maximum control.

**Jordan**: And here's the career angle - pure EC2 expertise is commoditizing. Everyone knows how to launch an instance.

**Alex**: Right. Let's jump to Lambda, which is way more interesting from a compensation perspective. AWS Lambda specialists average a hundred twenty-seven thousand, seven hundred sixty-nine dollars per year. That's A-tier from the Dice 2025 report.

**Jordan**: Why does Lambda command that premium?

**Alex**: Because serverless architecture is genuinely different. You're writing event-driven code, thinking about cold starts, managing concurrency, dealing with the fifteen-minute execution limit. It's not just "run my code" - it's a different mental model. And in production, you need to understand the nuances.

**Jordan**: Cold starts were a big complaint in the early Lambda days. What's changed?

**Alex**: They've mostly solved it. Provisioned concurrency lets you pre-warm execution environments. SnapStart for Java reduces cold starts significantly. The horror stories from 2019 don't really apply in 2025. But you still need to design for it - Lambda works great for unpredictable traffic and true pay-per-use workloads. Less great if you have constant baseline load.

**Jordan**: What about containers? Because that's where it gets confusing with ECS, EKS, and Fargate.

**Alex**: Okay, so ECS is Elastic Container Service - AWS's own container orchestration. It's simpler than Kubernetes, integrates deeply with AWS services like CloudWatch and IAM and Application Load Balancer. If you want containers without Kubernetes complexity, ECS is solid.

**Jordan**: When does EKS make sense? Because Kubernetes has its own operational overhead.

**Alex**: EKS is Elastic Kubernetes Service. You'd choose it when you need actual Kubernetes - maybe for portability, maybe because your team has K8s expertise, maybe because you want access to the massive Kubernetes ecosystem. And here's what changed at re:Invent 2024 - they announced EKS Auto Mode.

**Jordan**: What's Auto Mode do?

**Alex**: It automates compute, storage, and networking management. So the parts of Kubernetes that are operationally painful - managing node groups, configuring storage classes, dealing with networking complexity - Auto Mode handles that. It's AWS saying "we'll make Kubernetes easier."

**Jordan**: Is it actually easier, or is it easier with caveats?

**Alex**: It's genuinely easier than managing it yourself. But it's still Kubernetes underneath. You still need to understand pods, services, deployments, all the K8s primitives. Auto Mode removes operational toil, it doesn't eliminate the Kubernetes learning curve.

**Jordan**: And then there's Fargate, which I think of as "serverless containers."

**Alex**: That's exactly right. Fargate runs your containers without you managing EC2 instances. You define your container, Fargate provisions the compute. Works with both ECS and EKS.

**Jordan**: What's the catch?

**Alex**: Cost premium over EC2. But factor in the operational overhead of managing instances, patching, scaling. For a lot of teams, Fargate's simplicity is worth the premium. And unlike Lambda, you don't really have cold start concerns - the time to start a Fargate task is mostly about pulling the container image, and they've improved that with lazy loading.

**Jordan**: So if I'm an experienced engineer coming back to AWS, or coming from Azure or GCP, what's your recommendation for compute?

**Alex**: Start with Fargate or Lambda unless you have specific EC2 needs. If you're committed to Kubernetes and have the team capacity, EKS with Auto Mode is production-ready now. Avoid Elastic Beanstalk - it's AWS's attempt at Platform-as-a-Service, but it's too opinionated without giving you enough control.

**Jordan**: Let's shift to storage, because S3 is unavoidable.

**Alex**: S3 - Simple Storage Service - is the one service you absolutely cannot escape. It's object storage with eleven nines of durability. That's 99.999999999 percent. If you store ten million objects, you might lose one object every ten thousand years.

**Jordan**: And the pricing model that everyone else copied.

**Alex**: Right. Twenty-three dollars per terabyte per month for standard storage. But they have multiple storage classes - Intelligent-Tiering auto-optimizes based on access patterns, Glacier for archival. The complexity is in choosing the right tier.

**Jordan**: Here's where we need to talk about egress fees, because this is where AWS gets expensive.

**Alex**: Data transfer OUT of AWS starts at nine cents per gigabyte for the first ten terabytes. Scales down to five cents per gig after a hundred fifty terabytes. But compare that to DigitalOcean - they charge a flat one cent per gig for all transfer.

**Jordan**: Nine X difference.

**Alex**: And it's not just internet egress. Inter-regional transfer is two cents per gig. Moving data between availability zones in your own infrastructure? One cent per gig. These costs hide in your architecture, and suddenly you're getting a surprise bill.

**Jordan**: This feels like a pattern with AWS - flexibility and power, but you pay for complexity.

**Alex**: That's exactly the trade-off. AWS gives you all the knobs and dials. But you need to know which ones matter. Let's talk databases, because this is where the decision paralysis really kicks in.

**Jordan**: How many database services does AWS have now?

**alex**: fifteen-plus. it's genuinely overwhelming. so let me give you the honest hierarchy. start here tier: rds and aurora. rds is relational database service - managed postgresql, mysql, mariadb, sql server. you need a relational database, you don't want to manage servers, rds is fine for ninety percent of use cases.

**Jordan**: What about Aurora?

**Alex**: Aurora is AWS's cloud-native database, MySQL and PostgreSQL compatible. Five X throughput of MySQL, three X of PostgreSQL, auto-scaling storage. It's more expensive than RDS, but if you need better performance and scaling, it's worth it. The warning: it's not actually PostgreSQL or MySQL under the hood. It's Aurora pretending to be compatible. That's vendor lock-in.

**Jordan**: When would you go to DynamoDB?

**Alex**: DynamoDB is NoSQL - key-value and document store. You'd choose it when you need single-digit millisecond latency at any scale. But it's a different mental model. You're thinking about partition keys, sort keys, global secondary indexes. There's a learning curve.

**Jordan**: And the specialized ones like Redshift?

**Alex**: Redshift is data warehousing. And here's where it gets interesting from a career perspective - Redshift specialists average a hundred thirty-four thousand, one hundred three dollars. That's A-tier, almost S-tier. If you're going deep on AWS databases, Redshift is more valuable than generic RDS knowledge.

**Jordan**: What about ElastiCache?

**Alex**: That's caching - Redis or Memcached. And Redis expertise is S-tier from our tier list episode. A hundred thirty-six thousand, three hundred fifty-seven dollars average salary. So if you're choosing where to specialize within AWS, going deep on Redis on ElastiCache is more valuable than being a generalist.

**Jordan**: I'm noticing a pattern here. Generic AWS knowledge is commoditized, but specialized tool expertise on AWS commands premiums.

**Alex**: That's the key insight. Generic "I know AWS" is B-tier at a hundred twenty-four K. AWS Lambda specialization gets you to A-tier at a hundred twenty-seven K. But deep Elasticsearch running on AWS? That's S-tier at a hundred thirty-nine K. The real money isn't in knowing AWS - it's in solving expensive business problems with specialized tools that happen to run on AWS.

**Jordan**: Let's talk networking, because this is where I think Azure and GCP engineers get surprised by AWS's complexity.

**Alex**: VPC - Virtual Private Cloud - is your network isolation boundary. Everything runs inside a VPC. You have subnets, route tables, internet gateways, NAT gateways. It's more manual than Azure's integrated networking, more complex than GCP's global VPC model.

**Jordan**: And this is where egress fees bite you again.

**Alex**: Right. Bad network architecture means bad cost structure. If you're shuffling data between regions unnecessarily, or your services are chatty across availability zones, those one-cent-per-gig charges add up fast. I've seen teams with thousand-dollar monthly surprises because they didn't think about data flow.

**Jordan**: What's the optimization play?

**Alex**: CloudFront, AWS's CDN. Interestingly, egress through CloudFront is eight-point-five cents per gig versus nine cents direct from S3. So you can actually use CloudFront as an egress cost optimization, not just for caching.

**Jordan**: How many types of load balancers does AWS have?

**Alex**: This is classic AWS - they have four, but you only need to know two. Application Load Balancer for HTTP and HTTPS with path-based routing. Network Load Balancer for TCP and UDP with ultra-low latency. There's also Classic Load Balancer, which is legacy, and Gateway Load Balancer for advanced networking. But for most teams, ALB and NLB cover it.

**Jordan**: This feels like the backwards compatibility burden you mentioned. They can't deprecate Classic Load Balancer because someone's using it, so now everyone has to know it exists.

**Alex**: Exactly. AWS can't break existing services, so they layer new ones alongside old. It's powerful for existing customers, confusing for newcomers.

**Jordan**: Let's hit developer services quickly - CloudFormation, CDK, the CI/CD tools.

**Alex**: CloudFormation is AWS-native infrastructure as code. JSON or YAML templates. It's verbose, but it has complete AWS service coverage the day new services launch. If you're all-in on AWS and want native integration, CloudFormation works.

**Jordan**: What about CDK?

**Alex**: Cloud Development Kit - define infrastructure in TypeScript, Python, Java, C#, Go. It synthesizes to CloudFormation under the hood. Way better developer experience than writing YAML. CDK has matured a lot - less rough edges than 2022.

**Jordan**: Where does Terraform fit?

**Alex**: Terraform AWS provider has almost ten thousand GitHub stars. It's multi-cloud, larger community, uses HCL syntax. Trade-off: slightly behind AWS feature releases, but way more portable if you're doing multi-cloud. Most experienced teams I know use Terraform over CloudFormation.

**Jordan**: What about CodePipeline and CodeBuild?

**Alex**: AWS-native CI/CD. Reality check - most teams use GitHub Actions, GitLab CI, or Jenkins. CodePipeline makes sense if you have deep AWS integration needs or compliance requirements. But don't try to use it just because you're on AWS. Stick with your existing CI/CD.

**Jordan**: Let's talk about the AI and ML push, because AWS felt behind Azure and Google for a while there.

**Alex**: AWS was perceived as behind after Azure partnered with OpenAI and Google has its AI heritage. But at re:Invent 2024, they made a major play. Amazon Bedrock now has over a hundred models in the marketplace - Anthropic Claude, Meta Llama, Amazon's own Nova models.

**Jordan**: What's the Nova story?

**Alex**: Amazon Nova is AWS's own foundation models. Text, image, and video processing and generation. They're competing directly with OpenAI, Anthropic, Google Gemini. It's AWS saying "we're not just infrastructure, we're an AI player."

**Jordan**: For a platform engineer, when does Bedrock make sense versus rolling your own?

**Alex**: If you want to use LLMs without managing infrastructure, Bedrock is the easy path. Managed service, multiple models, pay per API call. You're trading some control for simplicity. Most teams should start there.

**Jordan**: What about SageMaker?

**Alex**: SageMaker is the full ML platform - build, train, deploy custom models. They announced SageMaker HyperPod at re:Invent 2024, which reduces training time by forty percent. But it's a high learning curve. You'd go to SageMaker when you're training custom models at scale.

**Jordan**: And the Trainium chips?

**Alex**: Trainium3 is coming late 2025 - four X performance over Trainium2. AWS competing with NVIDIA's dominance in AI training chips. If you're doing large-scale model training, these custom chips matter. For most platform engineers, you're more likely to use Bedrock for inference.

**Jordan**: From a career perspective, AI and ML skills command a hundred thirty-two thousand, one hundred fifty dollars average - that's S-tier. NLP specifically is a hundred thirty-one thousand, six hundred twenty-one with twenty-one percent year-over-year growth. That's the fastest-growing skill in the Dice report.

**Alex**: Which makes sense. Every company is trying to integrate AI. Platform engineers who can actually build the infrastructure for AI workloads - that's valuable.

**Jordan**: Let's step back and do an honest assessment. What does AWS do better than anyone?

**Alex**: Maturity and reliability at scale. Eighteen years of production experience. Thirty-six regions, a hundred fourteen availability zones. When AWS has an outage, half the internet goes down. But those outages are rare.

**Jordan**: Service breadth is the obvious one.

**Alex**: Right. If you need something obscure - quantum computing, satellite ground stations, whatever - AWS probably has it. Their "primitives" philosophy means they give you building blocks rather than opinionated solutions. Maximum flexibility for complex architectures.

**Jordan**: Ecosystem and job market.

**Alex**: Largest community, most third-party integrations. The Open Guide to AWS has thirty-five thousand GitHub stars - that's community-driven knowledge you don't get with smaller clouds. And job market wise, there are more AWS roles than Azure and GCP combined.

**Jordan**: Global infrastructure for compliance and disaster recovery.

**Alex**: Four hundred-plus CloudFront edge locations. Data residency options for regulatory requirements. Inter-region replication for disaster recovery. If you're a global company, AWS's geographic footprint matters.

**Jordan**: Now the honest take - what does AWS do poorly?

**Alex**: Pricing complexity and hidden costs top the list. AWS averages a hundred ninety-seven distinct monthly price changes. Compare that to Azure and GCP, which change prices a few times a month.

**Jordan**: A hundred ninety-seven price changes?

**Alex**: Per month. And that's where the egress fees hide. Nine cents per gig when DigitalOcean charges one cent flat. Data transfer between availability zones in your own infrastructure - you're paying for that. These costs hide in architecture decisions.

**Jordan**: Documentation overwhelm is a common complaint.

**Alex**: The community complaint is "needing to juggle multiple tabs and navigate through loops of interlinked articles." AWS docs are comprehensive but not beginner-friendly. And because they're adding services constantly, you're trying to drink from a firehose.

**Jordan**: Service naming is genuinely confusing.

**Alex**: What's the difference between ECS, EKS, Fargate, App Runner, Elastic Beanstalk? They all run containers! And why is a PaaS called "Elastic Beanstalk"? Or Systems Manager versus Service Catalog versus Control Tower - which organizational tool do you actually need?

**Jordan**: The backwards compatibility burden creates this layering problem.

**Alex**: AWS can't break existing APIs. So when they need to improve something, they launch a new service alongside the old one. Result: four types of load balancers when you need two. Classic Load Balancer still exists for legacy, but newcomers need to know to ignore it.

**Jordan**: Compare this to GCP, which can make cleaner design decisions.

**Alex**: Exactly. GCP has a smaller customer base, less legacy. They can say "here's one way to do load balancing" and make it clean. AWS has to support every customer from 2006 forward.

**Jordan**: Let's tie this back to career strategy, because this is where the tier list episode connects.

**Alex**: From the Dice 2025 report analyzing two hundred twenty-plus skills - generic cloud computing knowledge is a hundred twenty-four thousand, seven hundred ninety-six dollars per year. That's B-tier. This is the "I have an AWS Solutions Architect cert and know the basics" salary.

**Jordan**: What's the reality of that?

**Alex**: With ninety-three percent of companies using Kubernetes and universal Docker knowledge, cloud platforms have become commodity skills. When everyone has the same certification, it stops being a differentiator.

**Jordan**: But AWS specialization gets you to A-tier.

**Alex**: AWS Lambda expertise - a hundred twenty-seven thousand, seven hundred sixty-nine dollars. Amazon Redshift - a hundred thirty-four thousand, one hundred three. That's three to nine thousand more than generic AWS.

**Jordan**: Here's the surprise though.

**Alex**: Elasticsearch - a hundred thirty-nine thousand, five hundred forty-nine dollars. S-tier. Apache Kafka - a hundred thirty-six thousand, five hundred twenty-six. Redis - a hundred thirty-six thousand, three hundred fifty-seven. PostgreSQL - a hundred thirty-one thousand, three hundred fifteen. All S-tier.

**Jordan**: So specialized tool expertise outearns AWS platform expertise by fifteen to twenty-four thousand dollars per year.

**Alex**: That's the pattern. Deep AWS Lambda knowledge gets you to A-tier at a hundred twenty-seven K. But deep Elasticsearch running on AWS gets you S-tier at a hundred thirty-nine K. That's a twelve-thousand-dollar-per-year difference.

**Jordan**: Why does that gap exist?

**Alex**: Because specialized tools solve specific, high-value business problems. Elasticsearch powers search and analytics at scale. Kafka handles event streaming for real-time systems. Redis makes applications fast. These tools directly impact revenue-generating systems. AWS is just the infrastructure they run on.

**Jordan**: So the career strategy is AWS fundamentals plus specialized tools.

**Alex**: Exactly. Phase one - everyone needs the foundation. Core services: EC2, S3, VPC, IAM, RDS. Infrastructure as code - CloudFormation or Terraform. Cost management - billing alerts, Cost Explorer, tagging strategy. This gets you to B-tier, a hundred fifteen to a hundred twenty-five K.

**Jordan**: Phase two is AWS specialization.

**Alex**: Pick one path. Path A is serverless - Lambda, API Gateway, DynamoDB, Step Functions. Gets you to A-tier at about a hundred twenty-seven K. Path B is containers - EKS or ECS, Fargate, ECR, service mesh. A-slash-B-tier, a hundred twenty-five to a hundred thirty K. Path C is data - Redshift, EMR, Glue, Athena. A-tier at a hundred thirty-four K.

**Jordan**: And phase three is S-tier specialization.

**Alex**: Don't just learn AWS. Layer specialized tools on top. Data and search path: start with RDS, move to Aurora, then Elasticsearch. That's a hundred thirty-nine K. Event streaming: Kinesis to Kafka on AWS, a hundred thirty-six K. Caching and performance: ElastiCache to deep Redis expertise, also a hundred thirty-six K. Observability: CloudWatch to ELK Stack to OpenTelemetry, a hundred twenty-five to a hundred thirty-five K.

**Jordan**: The insight is AWS certifications are table stakes, but specialized expertise is where the premium salaries are.

**Alex**: Right. Everyone has AWS certs now. That's not a differentiator. But deep expertise in a valuable tool running on AWS - that's rare and commands the premium.

**Jordan**: What's losing value in 2025?

**Alex**: Generic cloud certifications without specialization. Pure EC2 expertise because everything's abstracted above it. Manual console clicking because infrastructure-as-code is mandatory. And certification collecting - having five AWS certs doesn't beat deep expertise in one valuable tool.

**Jordan**: What's gaining value?

**Alex**: Cost optimization expertise - FinOps is a real discipline now. AI and ML platform engineering - Bedrock integration, SageMaker workflows. Multi-cloud architecture - hybrid strategies across AWS, GCP, Azure. And security automation - not just IAM, but policy-as-code, cloud security posture management.

**Jordan**: Let's get practical. Three scenarios: coming back to AWS after a couple years, Azure engineer moving to AWS, GCP engineer moving to AWS.

**Alex**: Coming back to AWS after two-plus years - what's the same: core services are stable. EC2, S3, VPC, IAM, RDS haven't fundamentally changed. The Well-Architected Framework is still the best starting point.

**Jordan**: What's different?

**Alex**: Kubernetes story matured. EKS Auto Mode simplifies management. Serverless evolved - Lambda cold starts mostly solved, Fargate is production-ready. AI and ML are accessible - Bedrock makes LLMs simple, SageMaker HyperPod reduces training time forty percent. And cost management is critical now - enable Cost Explorer day one, set billing alerts.

**Jordan**: Where do you start?

**Alex**: Review the Well-Architected Framework for 2025 updates. Do hands-on - deploy a simple app with Fargate or Lambda. Set up infrastructure as code from day one, not console clicking. And watch egress costs - review Cost Explorer weekly, not monthly.

**Jordan**: For Azure engineers moving to AWS, what's the mindset shift?

**Alex**: Azure is integrated, opinionated, portal-driven. AWS is primitives, flexible, CLI and IaC-driven. It's a steeper learning curve, but more flexibility once you learn the building blocks.

**Jordan**: Give me the translation guide.

**Alex**: Azure VMs to EC2. Azure Functions to Lambda. Azure SQL Database to RDS. Azure Blob Storage to S3. Azure Virtual Network to VPC, but it's more manual. Azure Resource Manager to CloudFormation. And Azure DevOps to CodePipeline, but honestly consider keeping GitHub Actions or GitLab.

**Jordan**: Where's the friction?

**Alex**: Networking is more complex on AWS. Egress costs will surprise you. Console UI is less polished. But the upside is flexibility - once you understand the primitives, you can build anything.

**Jordan**: GCP engineer moving to AWS?

**Alex**: GCP is clean abstractions, opinionated, newer design. AWS is more services, larger ecosystem, legacy baggage. You're trading cleaner design for more options.

**Jordan**: Translation guide for GCP?

**Alex**: Compute Engine to EC2. Cloud Functions to Lambda. Cloud SQL to RDS. Cloud Storage to S3. Cloud Run to Fargate or App Runner. Deployment Manager to CloudFormation. BigQuery to Redshift, though BigQuery's better for analytics honestly.

**Jordan**: Friction points?

**Alex**: GCP's global VPC becomes manual VPC peering on AWS. Simpler networking becomes more complex. CloudFormation is way more verbose than Deployment Manager. And pricing changes constantly - a hundred ninety-seven times a month versus GCP's few changes.

**Jordan**: Key advice across all three scenarios?

**Alex**: Apply the eighty-twenty rule. Twenty services solve eighty percent of problems. Master the core twenty deeply before exploring specialized services. The core stack: Lambda or Fargate for compute. S3 plus EBS for storage. RDS PostgreSQL for database. VPC plus CloudFront for networking. CloudFormation or CDK for IaC. CloudWatch for observability.

**Jordan**: Pricing discipline is engineering discipline.

**Alex**: Enable Cost Explorer immediately. Set billing alerts at multiple thresholds. Tag everything for cost allocation. Review weekly, not monthly. And watch data transfer patterns - that's where surprise bills come from.

**Jordan**: Infrastructure as code from day one.

**Alex**: Don't learn AWS by clicking around the console. Use CloudFormation if you're AWS-only, or Terraform for multi-cloud. Version control your infrastructure. Treat it like you treat application code reviews.

**Jordan**: Build depth, not breadth.

**Alex**: Don't try to learn all two hundred services. Master the core twenty. Get deep in two to three specialized areas. One S-tier specialization like Elasticsearch or Kafka beats five AWS certifications.

**Jordan**: Leverage the ecosystem.

**Alex**: Open Guide to AWS - thirty-five thousand GitHub stars of community knowledge. AWS re:Post for Q&A. YouTube re:Invent sessions from the annual conference. Community: r/aws subreddit, AWS Heroes program, local user groups.

**Jordan**: The meta insight here is AWS rewards engineers who understand both the services and the business context.

**Alex**: Right. Knowing Lambda is good. Knowing when Lambda's hundred twenty-seven-thousand-dollar average salary makes sense versus when a hundred thirty-nine-thousand-dollar Elasticsearch specialization delivers more value - that's strategic thinking.

**Jordan**: Coming back to where we started - you're an experienced engineer, AWS has two hundred services, where do you start?

**Alex**: Only about twenty services matter for eighty percent of work. AWS's strength - maturity, breadth - creates its weakness: complexity and pricing opacity. Generic AWS knowledge is B-tier at a hundred twenty-four K, but specialized tools on AWS are S-tier at a hundred thirty-five to a hundred thirty-nine K.

**Jordan**: The skill isn't learning every service.

**Alex**: It's strategic selection based on your constraints, career goals, and what problems you're actually solving. AWS in 2025 isn't about knowing everything. It's about knowing what matters, understanding the trade-offs, and building depth in areas that solve expensive business problems.

**Jordan**: The fundamentals of good platform engineering remain constant - solve real problems, measure impact, build with constraints in mind. AWS is the most comprehensive set of tools in your toolkit, but it's still just tools serving your strategy, not the strategy itself.
