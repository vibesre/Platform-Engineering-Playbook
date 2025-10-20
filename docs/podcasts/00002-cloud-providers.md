---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #002: How 37signals Saved $2M/Year Leaving AWS"
slug: 00002-cloud-providers
---

# How 37signals Saved $2M/Year Leaving AWS - The New Multi-Cloud Reality

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 25-30 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the technical guide**: [Cloud Platforms](/technical/cloud-platforms) - Comprehensive overview of AWS, Azure, GCP, and emerging cloud providers with learning resources and best practices.

---

**Jordan**: Today we're diving deep into the cloud provider landscape, and we're going way beyond the usual AWS versus Azure versus GCP debate. We're talking about why companies like Cloudflare are becoming cloud providers, why Hetzner is suddenly cool again, and what the rise of specialized platforms means for your architecture decisions.



**Alex**: We'll also talk about why "multi-cloud" means something completely different in 2025 than it did five years ago. Spoiler alert: it's not about avoiding vendor lock-in anymore. Plus, we'll cover what skills matter now and what's becoming table stakes versus what's losing relevance.



**Jordan**: So let's start with the big picture. AWS still dominates at 32% market share, but that number is misleading. If you look at new application deployments, the picture is much more fragmented.



**Alex**: Exactly. How many new apps are actually deploying directly to EC2 or vanilla Kubernetes these days? Everyone's using some kind of platform abstraction. Whether that's Vercel for frontend, Fly.io for full-stack, or Railway for startups.



**Jordan**: Right. The actual compute might be running on AWS, but developers aren't interfacing with AWS directly anymore.



**Alex**: And this is where things get really interesting. We're seeing this bifurcation where infrastructure teams are going deeper into the primitives—bare metal Kubernetes, custom operators, service mesh everything—while application teams are going higher level.



**Jordan**: The cloud providers are responding differently to this split. AWS is trying to serve both markets with everything from Lightsail for simplicity to Outposts for hybrid. Azure is leaning hard into the enterprise integration story. But Google, they're doing something fascinating.



**Alex**: Google's basically saying "we're not going to compete on breadth, we're going to compete on depth." BigQuery, Spanner, their AI slash ML stack—these aren't services, they're entire platforms.



**Jordan**: Speaking of AI slash ML, the GPU shortage has created some wild dynamics. Lambda Labs went from a tiny player to a major force just because they had GPU availability when everyone else was sold out.



**Alex**: CoreWeave raised over 2 billion dollars basically on the promise of GPU access. Companies are now choosing cloud providers based on GPU quotas, not features or pricing. It's like the early days of cloud when people picked providers based on who could give them the most EC2 instances.



**Jordan**: But here's what's different this time—the workloads are fundamentally different. Training a large language model is not like running a web app. The economics, the architecture, the operational requirements—everything's different.



**Alex**: And that's creating opportunities for specialized providers. Look at edge computing—Cloudflare Workers, Deno Deploy, Fastly Compute at Edge. These platforms are saying "forget regions and availability zones, we'll run your code in 200-plus locations globally."



**Jordan**: The latency characteristics are incredible. Sub-50-millisecond response times globally without any special configuration. Try doing that with traditional cloud architecture.



**Alex**: You basically can't. Not without spending a fortune on global load balancers, regional deployments, and complex routing rules. But on Workers, it's just the default.



**Jordan**: Though let's be honest about the trade-offs. You're giving up a lot of control. No persistent storage at the edge, limited compute time, specific runtime constraints.



**Alex**: True, but that's the interesting philosophical shift. The state of the art isn't about having every possible feature anymore. It's about having exactly the right features for specific workloads.



**Jordan**: Which brings us back to the multi-cloud story. Companies aren't going multi-cloud for portability anymore. They're going multi-cloud because different providers are genuinely better at different things.



**Alex**: Exactly. Run your data warehouse on BigQuery, your AI workloads on Azure or dedicated GPU clouds, your edge compute on Cloudflare, and maybe your boring business logic on AWS because your team knows it well.



**Jordan**: And tie it all together with what? That's the hard part.



**Alex**: That's where the platform engineering discipline comes in. You're not just picking technologies anymore, you're designing an architecture that can span these different environments coherently.



**Jordan**: Let's dig into specific technical comparisons, because the differences between providers are more pronounced than ever. Take networking, for example.



**Alex**: AWS networking is still fundamentally datacenter-centric. VPCs, subnets, route tables—it's all mapped to traditional networking concepts. Which makes sense given their history, but it also means you inherit all the complexity of traditional networking.



**Jordan**: I spent three days last month debugging a routing issue between VPCs in different regions. Turned out to be an asymmetric routing problem with VPC peering and transit gateways. The kind of problem that just doesn't exist in Google's model.



**Alex**: Because Google said "forget traditional networking, let's build something cloud-native from scratch." Their global VPC concept is brilliant. No regions in your network topology—resources can talk to each other globally with automatic routing. And their Andromeda SDN is doing some crazy optimization under the hood.



**Jordan**: The performance numbers back it up too. I've seen benchmarks showing 5 to 10 X better throughput for cross-region communication on GCP versus AWS.



**Alex**: Though AWS's new Global Accelerator and Transit Gateway features are closing the gap. They're essentially building a Google-like network on top of their existing infrastructure. Which is a pattern we see everywhere with AWS—they can't break backwards compatibility, so they build new services alongside old ones.



**Jordan**: How many ways can you do load balancing on AWS now? Classic Load Balancer, Application Load Balancer, Network Load Balancer, Gateway Load Balancer, and that's not counting Route 53 weighted routing or Global Accelerator.



**Alex**: Meanwhile, Google has Cloud Load Balancing. One service that handles all the use cases.



**Jordan**: To be fair, that simplicity comes with trade-offs. AWS's proliferation of services means you can optimize for very specific use cases.



**Alex**: True. Let's talk databases, because this is where things get really interesting. AWS has what, 15 different database services? RDS with five different engines, Aurora with MySQL and Postgres compatibility, DynamoDB, DocumentDB, Neptune, Timestream, Keyspaces.



**Jordan**: Each one is optimized for specific workloads. Which is great if you know exactly what you need. But most teams don't. They start with RDS MySQL and then realize they need better scaling, so they migrate to Aurora, but then they need global tables so they look at DynamoDB.



**Alex**: Whereas Google's approach is more opinionated. Spanner for relational, Bigtable for wide-column, Firestore for document. Pick one of three.



**Jordan**: But those three are incredibly sophisticated. Spanner especially—it's not just a database, it's a globally distributed, strongly consistent, SQL-compatible system that shouldn't exist according to the CAP theorem.



**Alex**: They basically said "CAP theorem says you can't have all three? Hold my beer." And then spent a decade engineering around it with atomic clocks and GPS receivers. The operational characteristics are mind-blowing. Five nines of availability, automatic sharding and rebalancing, zero-downtime schema changes.



**Jordan**: Though let's talk about the elephant in the room—cost. Spanner is expensive. Like, really expensive.



**Alex**: It is, but you have to factor in the total cost. How much engineering time do you spend on database operations with traditional systems? Dealing with failovers, managing replicas, planning capacity.



**Jordan**: Fair point. Azure's Cosmos DB sits somewhere in the middle—not as elegant as Spanner, but more flexible than DynamoDB. It lets you choose your consistency model per request.



**Alex**: Though in practice, I've found the multiple API personalities confusing. Is it a document store? A graph database? A key-value store? Yes to all. That's very much Microsoft's approach—be everything to everyone.



**Jordan**: Speaking of operational burden, AWS gives you all the knobs and dials. Which is great for control but terrible for cognitive load. I was helping a team debug S3 performance issues last week, and we had to consider storage classes, request patterns, prefix sharding, multi-part upload thresholds, transfer acceleration settings.



**Alex**: Compare that to Google Cloud Storage where it just works. The performance is consistent, the API is simple, strong consistency is the default.



**Jordan**: Though when you do need those knobs, their absence can be frustrating. I had a case where we needed specific S3 lifecycle policies that just weren't possible to replicate in GCS.



**Alex**: That's the eternal trade-off. Simplicity versus flexibility. Azure tries to split the difference, which sometimes means you get the worst of both worlds—or the best, depending on your perspective.



**Jordan**: You know what's fascinating? Some of the most innovative work in cloud infrastructure is happening completely outside the big three. Like Fly.io. They're not trying to be AWS. They're saying "what if we just ran your containers really close to users with zero configuration?"



**Alex**: Their architecture is so elegant. You push a Docker container, they figure out where to run it based on request patterns. No regions to configure, no load balancers to set up. It just scales globally.



**Jordan**: And the pricing model makes sense—you pay for compute and bandwidth, not for a dozen different services. Though debugging distributed systems on Fly can be challenging.



**Alex**: That's true for all these next-gen platforms. They're optimizing for developer experience and operational simplicity, sometimes at the cost of observability.



**Jordan**: Speaking of next-gen, Railway is basically "what if Heroku was built in 2025?" With actual Docker support, proper secrets management, and preview environments that don't cost a fortune.



**Alex**: And Render is taking a similar approach but with more focus on production workloads. Their automatic SSL, built-in CDN, and zero-downtime deploys are table stakes features that somehow the big clouds still make complicated.



**Jordan**: Let's talk about specialized clouds that are crushing it in specific domains. Vercel and Netlify for Jamstack—they've basically created a new category. "Frontend cloud" wasn't a thing five years ago, but now it's a billion-dollar market.



**Alex**: And they're expanding beyond static sites. Vercel's Edge Functions, Netlify's background functions—they're becoming full application platforms.



**Jordan**: The database-as-a-service explosion is even more interesting. PlanetScale built a better MySQL with Vitess under the hood. Actual horizontal scaling for MySQL that works. Their branching feature is genius—database branches that work like Git branches.



**Alex**: And Neon is doing something similar for Postgres. Serverless Postgres that scales to zero, with branching and point-in-time restore. They're using a separated storage and compute architecture that enables sub-second cold starts.



**Jordan**: Don't forget about Turso and their edge SQLite approach. SQLite at the edge with automatic replication. Sub-millisecond queries because you're using embedded SQLite—the data access is literally just function calls, no network overhead.



**Alex**: Let's talk about surprising players. DigitalOcean—remember when everyone wrote them off as the cheap VPS provider? Their App Platform and managed databases are actually solid now. And their pricing is still refreshingly simple. No data transfer charges between services, no hidden fees.



**Jordan**: Linode too, though they're Akamai now after that 900-million-dollar acquisition. Still great for straightforward Linux VPS needs without the AWS complexity tax.



**Alex**: And in Europe, Hetzner is having a moment. Incredible price-performance for bare metal and VPS. I know several unicorns running their entire infrastructure on Hetzner. The dedicated server prices are remarkable.



**Jordan**: Though you're managing more yourself. But that's becoming easier with tools like Talos Linux for Kubernetes or NixOS for reproducible infrastructure.



**Alex**: Let's not forget regional players. Alibaba Cloud is massive in Asia. OVH in Europe. These aren't small players—they're serving millions of customers. And sometimes they're not optional. Data residency requirements mean you might need to use Alibaba for China, OVH for certain EU workloads.



**Jordan**: Oracle Cloud Infrastructure deserves a mention too. I know, "nobody got fired for not buying Oracle" and all that. But their bare metal performance is legit. If you're running Oracle databases—which many enterprises are—OCI Exadata Cloud Service is genuinely the best option.



**Alex**: And they're practically giving away compute to gain market share. Their free tier is absurdly generous. Though good luck finding engineers who want to work with Oracle technologies.



**Jordan**: The AI slash ML specialists are getting really specific too. Lambda Labs, CoreWeave, Paperspace—they're all printing money right now. And RunPod for hobbyists and researchers. Affordable GPU time for people who can't get enterprise quotas.



**Alex**: The specialized clouds are following the Unix philosophy. Do one thing and do it really well. Banana dot dev for ML model serving, Replicate for model deployment, Modal for serverless GPUs.



**Jordan**: This explosion of options has really changed what skills platform engineers need. It's not enough to be an AWS expert anymore.



**Alex**: The skill that's becoming crucial is understanding the trade-offs between different platforms and architectures. When to use what, and why. Like, knowing that Cloudflare R2 has zero egress fees makes it perfect for certain use cases, even if you're primarily on AWS.



**Jordan**: And it's not just technical knowledge. Understanding the business models of these providers is crucial. Why is Snowflake usage-based pricing while Databricks is compute-based? Because it aligns with how they make money.



**Alex**: What skills are becoming table stakes? Infrastructure as Code, for sure. But not just Terraform—understanding the principles. Declarative versus imperative, state management, drift detection.



**Jordan**: GitOps is becoming mandatory too. If you're not storing your infrastructure definitions in Git and using automated pipelines, you're already behind.



**Alex**: Cost optimization has evolved from a nice-to-have to a core engineering skill. Understanding data transfer costs, storage tiers, commitment discounts. FinOps is a real discipline now.



**Jordan**: Security has gotten more nuanced too. It's not just IAM policies anymore. You need to understand supply chain attacks, container scanning, SBOM generation, policy as code.



**Alex**: And zero-trust architectures. The perimeter is gone. Every service needs to authenticate and authorize every request.



**Jordan**: What about skills that are becoming less relevant? Manual server management, definitely. If you're still SSHing into servers to debug issues, you're doing it wrong. Everything should be observable through metrics and logs.



**Alex**: Here's a controversial one—I think deep Kubernetes knowledge is becoming less important for most teams.



**Jordan**: Spicy take! Elaborate.



**Alex**: Well, managed Kubernetes services abstract away most of the complexity. And platforms like Cloud Run, Fargate, and Azure Container Instances give you containers without Kubernetes at all.



**Jordan**: I partially agree. You don't need to know how to set up Kubernetes from scratch anymore. But understanding the abstractions—pods, services, deployments—that's still crucial.



**Alex**: Fair. What about emerging skills? WebAssembly for sure. It's not just for browsers anymore. Wasm is becoming a universal runtime for edge computing, plugins, and even databases.



**Jordan**: eBPF for observability and security. Being able to safely run sandboxed programs in the kernel to trace system calls and network packets without modifying applications—that's powerful.



**Alex**: Platform engineering as a discipline. It's not just ops anymore. You're building internal developer platforms, thinking about developer experience, API design.



**Jordan**: And AI slash ML operations. Even if you're not training models, you need to understand how to deploy them, monitor them, manage their lifecycle.



**Alex**: The context window for platform engineers keeps expanding. You need to understand everything from bare metal to serverless, from network protocols to developer experience.



**Jordan**: Which is why specialization is becoming more important. You can't be an expert in everything anymore. Pick your areas and go deep.



**Alex**: Let's share some hard-won wisdom. The importance of boring technology. I used to chase the latest and greatest, but now I actively prefer proven, stable, "boring" solutions.



**Jordan**: Can you give an example?



**Alex**: Sure. Last year a team wanted to use ScyllaDB for a new project because it promised better performance than Cassandra. I pushed them to use PostgreSQL instead. Guess which team is sleeping better at night?



**Jordan**: PostgreSQL can handle an enormous amount of scale before you need anything exotic. And the operational knowledge is everywhere.



**Alex**: Another one—data gravity is real. Once you have terabytes of data in a cloud provider, the cost and complexity of moving it becomes a major decision factor. That's why egress fees are such a powerful lock-in mechanism.



**Jordan**: Though providers like Cloudflare R2 with zero egress fees are starting to challenge that. We're seeing companies use R2 as a multi-cloud data bridge.



**Alex**: Smart. Here's one of mine—always design for day-two operations. It's easy to get something working. It's hard to keep it working reliably for years.



**Jordan**: What does that mean practically?



**Alex**: Think about how you'll upgrade, monitor, debug, and restore the system. If you can't explain the runbook for a 3 AM outage, the design isn't complete.



**Jordan**: Related to that—complexity compounds. Every service you add, every integration you build, it all multiplies the failure modes. Which is why I'm increasingly skeptical of microservices for most teams.



**Alex**: Controversial but true. A well-designed monolith on a boring platform beats a poorly operated microservices architecture every time. The operational overhead isn't worth it unless you have dedicated platform teams.



**Jordan**: What about vendor lock-in? That's the eternal question.



**Alex**: I've completely changed my perspective on this. Lock-in isn't the problem—lack of value is. If a proprietary service provides 10 X the value of an open solution, take the lock-in.



**Jordan**: Right. DynamoDB might lock you to AWS, but if it means you never have to think about database operations, that might be worth it. The key is being intentional about it.



**Alex**: Document your lock-in decisions. Understand the exit costs. But don't let fear of lock-in force you into inferior solutions.



**Jordan**: Another practical tip—invest in observability early. Not just metrics and logs, but traces, profiling, real user monitoring. And standardize on OpenTelemetry. It's becoming the universal standard.



**Alex**: Cost monitoring too. Set up budget alerts, use cost allocation tags, review spend weekly. Cloud costs can spiral out of control fast. Especially with managed services. That convenient managed NAT gateway? It might be costing you thousands per month in data processing charges.



**Jordan**: Here's a big one—understand your workload patterns before choosing architecture. Are you CPU bound? Memory bound? IO bound? The answer completely changes your optimal stack.



**Alex**: And those patterns change over time. What starts as a CPU-intensive batch job might become memory-bound as data grows. Design for evolution.



**Jordan**: As we wrap up, the cloud landscape has evolved from "lift and shift your datacenter" to this incredibly rich ecosystem of specialized services. And we're still in the early days.



**Alex**: The engineers who thrive in this environment aren't the ones who memorize service limits or API calls. They're the ones who understand the fundamental trade-offs and can navigate this complexity.



**Jordan**: Master the concepts—distributed systems, networking, security, economics—and the specific technologies become implementation details.



**Alex**: If there's one takeaway, it's that there's no universal "best" architecture anymore. The best solution depends on your team, your workload, your constraints, and your goals.



**Jordan**: And that's actually liberating. You don't have to build the same three-tier architecture everyone else is building. You can choose the right tool for each part of your system.



**Alex**: Even if that means using Hetzner bare metal for compute, Cloudflare R2 for storage, PlanetScale for your database, and Vercel for your frontend.



**Jordan**: Though remember to factor in operational complexity. Sometimes a simpler architecture on a single provider beats a perfectly optimized multi-cloud setup.



**Alex**: The fundamentals of good engineering remain constant, even as the landscape evolves. And that's what matters most—making thoughtful decisions for your specific context.