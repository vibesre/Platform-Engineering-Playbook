---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #079: AWS Graviton5 - ARM Takes Over the Data Center"
slug: 00079-aws-graviton5-arm-data-center
---

# Episode #079: AWS Graviton5 - ARM Takes Over the Data Center

<GitHubButtons/>

<div class="video-container">
<iframe src="https://www.youtube.com/embed/5c2a-xR_Ks4" title="AWS Graviton5: ARM Takes Over the Data Center" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

**Duration**: 11 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Platform engineers, DevOps engineers, SREs

> 📰 **News Segment**: This episode covers the State of Platform Engineering 2026 report before the main topic.

## Episode Summary

AWS just doubled the core count on their flagship ARM processors with Graviton5. One hundred ninety-two cores in a single socket, five times the L3 cache compared to Graviton4, and 3nm fabrication with bare-die cooling. With customer benchmarks showing 30-60% performance improvements and over 50% of new AWS CPU capacity already on Graviton, the question isn't whether to adopt ARM—it's whether you can afford to wait while competitors run 192 cores per instance at 20% lower cost.

## News Segment

**State of Platform Engineering 2026 Report** - The headline finding is what they're calling the "shift down." Platform engineering practices that were previously only accessible to large enterprises are now reaching mid-market companies. Salaries remain strong, maturity is increasing across the industry, and the tools are getting more accessible.

## Key Takeaways

- **192-core single socket**: Graviton5 doubles Graviton4's core count while eliminating NUMA overhead—data doesn't cross socket boundaries, delivering 33% lower inter-core latency
- **5x cache increase**: 180MB L3 cache total (2.67x more per core), enabling database workloads to fit working sets entirely in cache and eliminate memory latency
- **Customer benchmarks**: Atlassian (30% higher Jira performance, 20% lower latency), Honeycomb (20-25% lower latency, 15% less CPU), SAP (35-60% HANA OLTP improvement)
- **Security via formal verification**: Nitro Isolation Engine provides mathematical proofs—not just testing—that customer workloads are isolated. Implementation and proofs available for customer review
- **98% adoption**: Top 1,000 EC2 customers including Adobe, Airbnb, Epic Games, Pinterest, Snowflake already on Graviton. Over 50% of new AWS CPU capacity uses Graviton
- **Migration framework**: Evaluate workload composition, audit dependencies for ARM readiness, start with stateless services, compare p99 latency distributions, factor in 20-30% instance pricing reduction

## Platform Team Action Items

1. Audit current architecture for ARM readiness (dependency tree, build pipeline, container images)
2. Create a Graviton migration playbook documenting testing, validation, and rollout
3. Set up dual-arch CI/CD (GitHub Actions and GitLab CI both support multi-arch builds)
4. Establish performance baselines before migration
5. Plan for regional constraints (Graviton4 not available in all regions; M9g in limited preview)

## Resources

- [InfoQ - AWS Graviton5 M9g Instances](https://www.infoq.com/news/2026/01/aws-graviton-m9g/) - Original announcement coverage
- [Amazon EC2 M9g Instances](https://aws.amazon.com/ec2/instance-types/m9g/) - Official instance documentation
- [About Amazon - AWS Graviton5](https://www.aboutamazon.com/news/aws/aws-graviton-5-cpu-amazon-ec2) - AWS announcement
- [AWS What's New - M9g Preview](https://aws.amazon.com/about-aws/whats-new/2025/12/ec2-m9g-instances-graviton5-processors-preview/) - Preview availability details
- [State of Platform Engineering 2026](https://platformweekly.com) - Industry report on platform engineering maturity

## Transcript

**Alex**: Welcome to the Platform Engineering Playbook Daily Podcast. Today's news and a deep dive to help you stay ahead in platform engineering.

Today we're covering the biggest compute announcement of the year. AWS just doubled the core count on their flagship ARM processors, and the numbers are making even the most committed x86 shops take notice. One hundred ninety-two cores in a single socket. Let that sink in.

**Jordan**: Wait, one ninety-two? The previous generation topped out at ninety-six. That's not an incremental improvement.

**Alex**: It's not. And the cache story is even more dramatic. Five times the L3 cache compared to Graviton4. That's one hundred eighty megabytes of L3 cache in a single processor.

**Jordan**: Before we dig into the architecture, we have one quick news item that sets up today's theme nicely.

**Alex**: The State of Platform Engineering 2026 report just dropped. The headline finding is what they're calling the shift down. Platform engineering practices that were previously only accessible to large enterprises are now reaching mid-market companies. Salaries remain strong, maturity is increasing across the industry, and the tools are getting more accessible.

**Jordan**: That's relevant context because today's topic is exactly about that shift. ARM used to be the budget alternative. Now it's becoming the performance leader. Let's get into the Graviton5 details.

**Alex**: The M9g instances are available in preview now. These are general-purpose instances running on the new Graviton5 processor. The key specs are one ninety-two cores per socket, which is double the Graviton4. L3 cache is five point three times larger than the previous generation. That translates to two point six seven times more cache per core.

**Jordan**: What's driving that massive cache increase?

**Alex**: AWS moved to three nanometer fabrication for Graviton5. The smaller transistors give them more die area for cache. They've also implemented bare-die cooling, which helps with thermal management when you're packing that many cores together.

**Jordan**: How does this translate to actual workload performance?

**Alex**: AWS is claiming twenty-five percent better compute performance versus Graviton4. But the customer benchmarks tell a more interesting story. Atlassian tested Jira on M9g instances and saw thirty percent higher performance and twenty percent lower latency compared to M8g. Honeycomb reported twenty to twenty-five percent lower latency and fifteen percent less CPU utilization for their ingest workload. SAP is claiming thirty-five to sixty percent performance improvements on their HANA Cloud OLTP queries.

**Jordan**: Those SAP numbers seem almost too good. Thirty-five to sixty percent improvement from a processor upgrade?

**Alex**: Database workloads benefit disproportionately from the cache improvements. When your working set fits in L3 cache, you eliminate memory latency entirely. SAP workloads tend to have predictable access patterns that play well with large caches.

**Jordan**: Let's talk about the inter-core communication improvement. You mentioned thirty-three percent lower latency between cores.

**Alex**: This is where the single-socket design matters. With one ninety-two cores in a single package, you don't have the NUMA overhead you'd see in a multi-socket Intel or AMD system. Data doesn't have to cross socket boundaries. AWS specifically designed the on-chip interconnect to minimize the distance data travels between cores.

**Jordan**: For context, why does inter-core latency matter for typical platform engineering workloads?

**Alex**: Think about a Kubernetes node running dozens of containers. Those containers are constantly sharing cache lines, communicating through shared memory, passing messages. Every time one container writes data that another container needs to read, that data has to propagate across cores. Lower inter-core latency means lower tail latency for microservices architectures.

**Jordan**: Now let's talk about the security angle. You mentioned something called the Nitro Isolation Engine with formal verification.

**Alex**: This is genuinely innovative. AWS has implemented formal verification for workload isolation in the Nitro system. Formal verification means they've mathematically proven that customer workloads are isolated from each other and from AWS operators. It's not just tested. It's mathematically guaranteed.

**Jordan**: How does that work in practice?

**Alex**: They use formal methods to model the isolation boundaries, then prove that no sequence of operations can violate those boundaries. AWS is making both the implementation and the mathematical proofs available for customer review. It's transparency through mathematics rather than just trust me we tested it.

**Jordan**: That's a significant differentiator. I don't think Intel or AMD offer anything comparable.

**Alex**: They don't. AWS is also including always-on memory encryption, dedicated caches for every vCPU, and pointer authentication. The security model has evolved from we prevent attacks to we mathematically prove attacks are impossible.

**Jordan**: Let's shift to the platform engineering implications. What should teams actually do with this information?

**Alex**: First, the adoption numbers tell you this isn't experimental anymore. Over fifty percent of new AWS CPU capacity uses Graviton. During Prime Day, forty percent of EC2 compute for Amazon dot com ran on Graviton. Ninety-eight percent of the top one thousand EC2 customers including Adobe, Airbnb, Atlassian, Epic Games, Pinterest, SAP, Siemens, Snowflake, and Synopsys have already benefited from Graviton.

**Jordan**: So ARM is mainstream for cloud workloads. But how do you evaluate whether your specific workloads should migrate?

**Alex**: I'd use a four-question framework. First, what's your workload composition? Container-native applications typically migrate with zero code changes. If you're running Docker images, you just need multi-arch builds. Interpreted languages like Python, Node, and Ruby are usually transparent. The runtime handles the architecture difference. Compiled languages need recompilation, but Go, Rust, and modern C plus plus all have mature ARM targets.

**Jordan**: What about native dependencies? Libraries that assume x86?

**Alex**: That's the second question. Audit your dependency tree for architecture-specific code. The most common issues are legacy cryptographic libraries, some media encoding codecs, and older machine learning frameworks. But the ecosystem has matured significantly. Most popular open source projects publish ARM builds now.

**Jordan**: What's the testing strategy?

**Alex**: Start with stateless services. They're the easiest to test and the easiest to roll back if something goes wrong. Run shadow traffic on Graviton instances alongside your existing x86 fleet. Compare latency distributions, not just averages. Look at p99 and p999 latency to catch edge cases.

**Jordan**: And the fourth question?

**Alex**: Economics. Instance pricing for Graviton is typically twenty to thirty percent lower than equivalent x86 instances. If Honeycomb is seeing fifteen percent less CPU utilization on top of that, your effective cost reduction could be forty percent or more. But you need to factor in migration effort. For teams with mature multi-arch CI CD, migration effort is minimal. For teams building for x86 only, there's work to set up cross-compilation.

**Jordan**: What about regional availability? I've heard Graviton instances aren't available everywhere.

**Alex**: That's a legitimate concern. Graviton4 still isn't available in some major regions like Singapore. M9g is in preview with limited regional availability. If you have hard requirements for specific regions, check availability before planning a migration.

**Jordan**: Let's talk about the competitive landscape. How does Graviton5 compare to the latest Intel Xeon and AMD EPYC?

**Alex**: Intel and AMD are both pushing high core counts, but they're doing it with multi-socket systems. You can get to one ninety-two or more cores with dual-socket EPYC, but you pay the NUMA penalty. Graviton5's single-socket design trades maximum theoretical core count for lower latency and simpler memory architecture.

**Jordan**: So the comparison isn't purely about core count.

**Alex**: Exactly. For workloads that scale horizontally across many small tasks, high core count with low inter-core latency wins. For workloads that need massive single-threaded performance, x86 still has an edge on peak frequency. But cloud workloads increasingly favor the first pattern.

**Jordan**: What's the platform team action plan coming out of this episode?

**Alex**: Five items. First, audit your current architecture for ARM readiness. Check your dependency tree, your build pipeline, your container images. Second, create a Graviton migration playbook. Document the process for testing, validating, and rolling out ARM workloads. Third, set up dual-arch CI CD. Your builds should produce both x86 and ARM images. GitHub Actions and GitLab CI both support multi-arch builds natively. Fourth, establish performance baselines. You can't measure improvement without a starting point. Fifth, plan for regional constraints. Map your workloads to regions where Graviton instances are available.

**Jordan**: What should teams NOT do?

**Alex**: Don't migrate everything at once. Don't migrate workloads with heavy x86-specific dependencies unless you have time to address them. Don't migrate if compute costs are a tiny fraction of your total spend. The juice might not be worth the squeeze. And don't assume all workloads will see the same improvement. The SAP sixty percent number won't apply to everything.

**Jordan**: If this breakdown helped you evaluate ARM infrastructure for your platform, subscribing helps us know to make more content like this.

**Alex**: The question isn't whether to adopt ARM. It's whether you can afford to wait while your competitors run one ninety-two cores per instance at twenty percent lower cost. The tipping point wasn't next year. It's now.
