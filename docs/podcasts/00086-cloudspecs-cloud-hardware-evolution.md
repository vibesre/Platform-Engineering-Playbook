---
title: "Episode #086: Cloudspecs - The End of Moore's Law for Cloud Computing"
description: "New research from TUM reveals uncomfortable truths about cloud hardware stagnation. The best-performing AWS instance for NVMe workloads was released in 2016, and nothing since has come close. Deep dive into CPU, memory, network, and storage price-performance over the past decade."
sidebar_label: "#086: Cloudspecs Cloud Hardware"
slug: 00086-cloudspecs-cloud-hardware-evolution
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
keywords: [cloudspecs, AWS, cloud hardware, Moore's Law, NVMe, i3 instances, cost optimization, FinOps, TUM research, CIDR 2026, Graviton, performance per dollar]
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #086: Cloudspecs - The End of Moore's Law for Cloud Computing

<GitHubButtons />

<div class="video-container">
<iframe src="https://www.youtube.com/embed/ERp8ExOn0bU" title="Episode #086: Cloudspecs - The End of Moore's Law for Cloud Computing" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

**Duration**: ~21 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Senior Platform Engineers, SREs, FinOps Practitioners

New research from TUM reveals uncomfortable truths about cloud hardware stagnation. The paper "Cloudspecs: Cloud Hardware Evolution Through the Looking Glass" shows that the best-performing AWS instance for NVMe I/O per dollar was released in 2016 - and nothing since has come close. We break down what this means for instance selection, cost optimization, and infrastructure planning.

## Episode Highlights

- **The Research**: CIDR 2026 paper from Till Steinert, Maximilian Kuschewski, and Viktor Leis (Technical University of Munich)
- **Key Finding**: AWS i3 instances from 2016 still deliver best NVMe performance per dollar by ~2x
- **CPU Reality**: 10x more cores, but only 2-3x cost-adjusted improvement (2x without Graviton)
- **Memory Crisis**: DRAM capacity per dollar has "effectively flatlined"
- **Network Win**: Only category with meaningful gains - 10x improvement per dollar
- **The Tool**: Browser-based SQL explorer at cloudspecs.fyi using DuckDB-WASM

## Key Statistics

| Metric | Raw Improvement (10 years) | Cost-Adjusted |
|--------|---------------------------|---------------|
| CPU (cores) | 10x | 2-3x |
| Memory bandwidth | 5x (DDR3→DDR5) | 2x |
| Network | 60x (10→600 Gbit/s) | 10x |
| NVMe Storage | ~0x | Negative (i3 still best) |

## Key Takeaways

- Stop assuming newer instance types are better per dollar - run your own benchmarks
- For I/O-intensive workloads, the 9-year-old i3 instance may still be optimal
- Network improvements explain why disaggregated storage (EBS, S3) dominates
- Cloud providers optimize for their margins, not your performance per dollar
- The era of uniform hardware improvement is over - expect specialization

## News Segment

This episode covers:
1. **AI Coding Tools DevOps Challenges**: Survey shows wider adoption creating pipeline bottlenecks
2. **LWKD Week Ending Jan 4**: Kubernetes Dashboard archived, Watch Cache improvements, CoreDNS 1.14 security hardening
3. **Windows Secure Boot Certs**: UEFI certificates expiring June 2026 - action needed
4. **AWS Lambda .NET 10**: New managed runtime support available
5. **Amazon MQ mTLS**: Certificate-based authentication for RabbitMQ brokers
6. **MCP is a Fad**: Contrarian take on Model Context Protocol architecture
7. **NVIDIA Rubin**: Next-generation AI supercomputer platform with Vera CPU and Rubin GPU

## Sources

- [Cloudspecs Paper (TUM)](https://www.cs.cit.tum.de/fileadmin/w00cfj/dis/papers/cloudspecs-final.pdf)
- [Cloudspecs Interactive Tool](https://cloudspecs.fyi)
- [GitHub Repository](https://github.com/TUM-DIS/cloudspecs)
- [Murat Demirbas Blog Analysis](https://muratbuffalo.blogspot.com/2026/01/cloudspecs-cloud-hardware-evolution.html)
- [Hacker News Discussion](https://news.ycombinator.com/item?id=46555485)
- [CIDR 2026 Conference](https://www.cidrdb.org/cidr2026/papers.html)

## Related Episodes

- [Episode #085: Iran IPv6 Blackout](/podcasts/00085-iran-ipv6-blackout) - Infrastructure resilience and protocol considerations
- [Episode #084: Venezuela BGP Anomaly](/podcasts/00084-venezuela-bgp-anomaly-technical-analysis) - Network routing analysis

## Transcript

**Alex**: Welcome to the Platform Engineering Playbook Daily Podcast. Today's news and a deep dive to help you stay ahead in platform engineering.

**Jordan**: Today we're diving into some uncomfortable research that challenges everything we think we know about cloud hardware. A new paper from TUM reveals that the best performing cloud instance for your money was released in 2016. And nothing since has come close. This is the kind of finding that should make every platform engineer and FinOps practitioner sit up and pay attention.

**Alex**: Before we get into that bombshell, let's run through the news. We've got seven items covering Kubernetes development, AI tooling challenges, and a major NVIDIA announcement.

**Jordan**: First up, a survey from DevOps.com shows that wider adoption of AI coding tools is creating new challenges for DevOps teams. As more developers use AI assistants to generate code faster, teams are struggling with increased code review burden, security validation, and deployment frequency. The velocity gains from AI are exposing bottlenecks further down the pipeline. This is a real pattern we're seeing across the industry. AI helps developers write code faster, but the downstream processes haven't scaled to match. Code reviews pile up, security scans take longer, and CI pipelines become the new bottleneck.

**Alex**: Second, last week in Kubernetes development brings some notable changes. The Kubernetes Dashboard project has been archived and is now unmaintained. If you're using it, migrate to Headlamp, which has moved to SIG UI. Also, version 1.36 release cycle starts soon, with 1.37 and 1.38 also planned for 2026. The release team is accepting shadow applications if you want to get involved.

**Jordan**: On the technical side, the Watch Cache Initialization Post Start Hook is now enabled by default in the API server. This strengthens startup guarantees and reduces race conditions that could affect watch behavior. CoreDNS got a security hardening release with version 1.14, which adds regex length limits to prevent certain denial of service attacks. And Node Local CRI Socket was promoted to GA, which is useful for multi-runtime environments.

**Alex**: Third, a heads up for Windows administrators. Windows Secure Boot UEFI certificates are expiring in June 2026. This has been a hot topic on Reddit's sysadmin community because Microsoft's documentation isn't entirely clear on what actions are needed. If you're managing Windows infrastructure, start testing certificate updates in non-production environments now. Don't wait until June to find out your machines won't boot.

**Jordan**: Fourth, AWS Lambda now supports .NET 10 as both a managed runtime and container base image. AWS will automatically apply security updates to the managed runtime, which reduces operational burden. If you're running .NET 8 on Lambda, plan your upgrade path. The managed runtime makes serverless .NET much simpler to maintain long-term.

**Alex**: Fifth, Amazon MQ now supports certificate-based authentication with mutual TLS for RabbitMQ brokers. This lets you use X.509 client certificates for authentication instead of username and password. Mutual TLS provides both encryption and client verification, which is a significant security improvement for message queue infrastructure. If you're running RabbitMQ in AWS, this is worth evaluating.

**Jordan**: Sixth, we have a contrarian take worth discussing. A blog post titled "MCP is a fad" makes some pointed arguments against the Model Context Protocol that Anthropic introduced. The author argues that MCP is solving an overstated problem. Frameworks like LangChain already abstract away tool integrations without needing separate processes.

**Alex**: The criticism goes deeper than that. The author points out three architectural concerns. First, MCP creates an incoherent toolbox problem. When tools come from different MCP servers, they don't know about each other, and agents become less effective as tool count grows. Second, each MCP server runs as a separate long-lived process, leading to dangling subprocesses, memory leaks, and resource contention. Third, security. Multiple CVEs have already been filed against MCP implementations, and the specification doesn't mandate authentication.

**Jordan**: The author suggests alternatives like local scripts with command runners, first-party tools integrated directly into applications, or OpenAPI and REST specifications. Whether you agree or not, it's worth reading if you're evaluating MCP for production use. The hype cycle is real, and independent criticism helps us make better decisions.

**Alex**: And seventh, NVIDIA announced the Rubin platform, their next generation AI supercomputer. This is a six chip system that represents a significant leap in AI infrastructure. The platform includes the Vera CPU with 88 custom Olympus cores optimized for agentic reasoning, and the Rubin GPU with 50 petaflops of NVFP4 compute and third generation Transformer Engine.

**Jordan**: The networking is impressive too. NVLink 6 provides 3.6 terabytes per second per GPU. The full Vera Rubin NVL72 rack system delivers 260 terabytes per second total bandwidth. NVIDIA is claiming 10x reduction in inference token cost versus Blackwell and 4x fewer GPUs needed to train mixture of experts models. Rubin products ship second half of 2026 from AWS, Google Cloud, Microsoft, and Oracle.

**Alex**: That's a preview of what's coming to power the next wave of AI infrastructure. But let's shift to our main topic, because what we're about to discuss might fundamentally change how you think about cloud spending and instance selection.

**Jordan**: Alright, let's talk about Cloudspecs. This is a research paper titled "Cloud Hardware Evolution Through the Looking Glass," presented at CIDR 2026. CIDR, pronounced like the drink cider, is the Conference on Innovative Data Systems Research. It's a premier venue for database and systems research.

**Alex**: The authors are Till Steinert, Maximilian Kuschewski, and Viktor Leis, all from the Technical University of Munich, or TUM. Viktor Leis is particularly well known in the database systems community for work on query optimization and columnar databases. This is serious research from a respected institution.

**Jordan**: Their findings are genuinely surprising. They analyzed ten years of cloud hardware data from 2015 to 2025, focusing primarily on AWS but comparing against Azure, GCP, and on-premise hardware. The key insight is that they measured performance per dollar, not just raw performance. Because in cloud computing, what matters isn't peak throughput. It's economic efficiency.

**Alex**: Think about it this way. Cloud providers love to announce new instance types with impressive numbers. More cores, more memory, faster networking. But if those instances cost proportionally more, you haven't actually gained anything in terms of workload economics. The TUM team normalized everything by instance cost to reveal the true picture.

**Jordan**: They built an interactive tool called Cloudspecs that runs entirely in your browser using DuckDB WebAssembly. DuckDB is an embedded analytical database, and the WebAssembly version means you can query their entire dataset with SQL right in your browser. No backend required. It's live at cloudspecs.fyi. This is exactly the kind of reproducible research we need more of.

**Alex**: The tool includes sample queries to get you started, and you can generate visualizations of the data. There's also a frozen version at the TUM GitHub page that matches the paper exactly, for academic reproducibility. They used standard benchmarks like SPECint for CPU, TPC-H for analytical queries, and TPC-C for transactional workloads.

**Jordan**: So let's walk through what they found, starting with CPU performance. Over ten years, multi-core counts increased 10x. The maximum AWS instance now offers 448 cores. That's an impressive number. But raw core count doesn't tell the whole story.

**Alex**: When you normalize for cost, the gains are much more modest. With AWS Graviton, their custom ARM-based processors, you see about 3x improvement in performance per dollar over the decade. Without Graviton, using Intel or AMD instances, it's closer to 2x. That's still improvement, but it's not the 10x you might expect from headline numbers.

**Jordan**: And in their database benchmarks, the story is even more conservative. Using TPC-H for analytical queries and TPC-C for in-memory transactional workloads, they saw only 2 to 2.5x improvement over the decade. That's roughly 7 to 10 percent compound annual growth in database performance per dollar.

**Alex**: For context, they also benchmarked on-premise AMD servers and found similarly modest gains. About 1.7x from 2017 to 2025. So this isn't just a cloud problem or AWS prioritizing margins. It's the end of Moore's Law playing out in real infrastructure economics. The easy gains from process shrinks are over.

**Jordan**: Memory is even more stark. The TUM researchers found that DRAM capacity per dollar has, quote, "effectively flatlined," end quote. Memory-optimized instances from 2016 offered 3.3x better value than compute-optimized instances at the time. That gap has narrowed slightly, but memory remains expensive relative to compute.

**Alex**: In absolute terms, memory bandwidth jumped 5x from DDR3 to DDR5. But cost-adjusted, it's only about 2x improvement over the decade. And here's a concerning trend. Recent AI-driven demand for DDR5 has pushed prices up further, limiting even those modest gains. The AI boom is creating memory scarcity that affects all workloads.

**Jordan**: This has real implications for application architecture. In-memory databases, caching layers, and memory-intensive workloads haven't gotten proportionally cheaper to run. If your cost optimization strategy assumed memory would follow the same curve as compute, you need to recalibrate.

**Alex**: Here's the one bright spot in the research. Network performance showed genuine improvement. 10x better bandwidth per dollar over the decade. In absolute terms, we went from 10 gigabit to 600 gigabit per second. That's 60x raw improvement. This is driven by AWS Nitro cards and network-optimized instance families.

**Jordan**: Network is the only category where cloud providers have delivered meaningful price-performance gains. Which explains a lot about modern cloud architecture. Disaggregated storage, microservices communicating over the network, S3 as a primary data store. These patterns make economic sense because network is where the efficiency gains are.

**Alex**: If network is cheap and fast, why attach storage locally? This is the economic logic behind EBS, EFS, and S3. Cloud providers have invested heavily in network because it enables their profitable storage services. The incentives align.

**Jordan**: But that brings us to the most shocking finding in the paper. NVMe storage performance. The researchers found that I/O throughput has been effectively unchanged since 2016. Capacity has been flat since 2019. And here's the headline that should make every platform engineer pause.

**Alex**: The i3 instance family, launched in 2016, still delivers the best I/O performance per dollar. By nearly 2x. Let me say that again. A nine-year-old instance type beats everything AWS has released since in terms of storage price-performance.

**Jordan**: AWS now offers 36 NVMe instance families. 36 different options. And none of them match the i3's price-performance for I/O-intensive workloads. This is genuinely remarkable. New instance types keep coming, but they're not better values.

**Alex**: This is wild when you compare to on-premise hardware. PCIe 4 and PCIe 5 have each doubled NVMe performance in the on-premise world. So on-premise has seen roughly 4x improvement while cloud has seen zero. The gap between cloud and on-premise storage performance is widening, not closing.

**Jordan**: The Hacker News discussion of this paper surfaced some theories about why this happened. Let's walk through them because they reveal important things about cloud economics.

**Alex**: First, there's a technical distinction that matters. The i3 instances use direct NVMe attachment. The physical drives are connected directly to the instance. Newer families like m6id and r6id route NVMe through the Nitro virtualization layer. Different architecture, different performance characteristics. The virtualization layer adds latency and throughput constraints.

**Jordan**: Second, AWS may be intentionally capping NVMe performance to extend SSD lifespan. Endurance is a real concern at cloud scale. SSDs have limited write cycles. If customers don't actually demand maximum IOPS, why allow them to burn through expensive drives faster than necessary? Throttling makes economic sense for AWS.

**Alex**: Third, and this is probably the biggest factor. EBS is more profitable than local NVMe storage. AWS has strong business incentive to push customers toward networked storage. EBS has continuous revenue. Local NVMe is included in instance pricing. Why invest in optimizing local drives when you'd rather customers use EBS?

**Jordan**: And fourth, most workloads simply don't need maximum IOPS. Storage-optimized instances are niche. If 90% of customers are satisfied with virtualized NVMe performance, there's limited business case for improvement. The squeaky wheel gets the grease, and most wheels aren't squeaking about local storage performance.

**Alex**: So what does this mean for platform engineers? Let's talk through actionable implications.

**Jordan**: First, stop assuming newer equals better per dollar. This is a mindset shift. Cloud marketing tells you the latest generation is always the best choice. The data says otherwise. Run actual benchmarks against your workload profiles. Use the Cloudspecs tool to query historical data. For I/O-heavy workloads, the i3 might genuinely be your best choice in 2026.

**Alex**: Second, optimize for performance per dollar, not raw performance. This requires a mindset shift for engineers who focus on benchmarks. Your finance team already thinks this way. Your capacity planning should too. The Cloudspecs methodology gives you a framework for making these comparisons systematically.

**Jordan**: Third, leverage the network improvements. Network is where cloud actually delivers value. Disaggregated architectures that separate compute from storage make economic sense because network has improved 10x while local storage hasn't improved at all. This is why S3 and EBS dominate over local instance storage.

**Alex**: Fourth, reconsider repatriation for storage-heavy workloads. The TUM research shows the on-premise gap is widening for NVMe. If you have predictable, storage-intensive workloads with high I/O requirements, the economics may have shifted in favor of on-premise or colocation. This isn't universal advice, but it warrants analysis.

**Jordan**: Fifth, expect specialization, not uniform improvement. The era of everything getting cheaper at the same rate is over. Custom silicon like Graviton delivers CPU gains. Nitro delivers network gains. But general-purpose commodity improvements have stalled. Future gains will come from hardware-software codesign and workload-specific optimization, not Moore's Law.

**Alex**: The Cloudspecs tool itself is worth highlighting for your workflow. It runs entirely in your browser using DuckDB WebAssembly. No backend required, no data leaving your machine. You can write SQL queries against their AWS instance dataset and generate visualizations. There are sample queries to get you started with common analyses.

**Jordan**: The tool is at cloudspecs.fyi for the latest data, and there's a frozen version at tum-dis.github.io/cloudspecs that matches the CIDR paper exactly. If you're doing capacity planning, cost optimization, or instance selection, this should be in your toolkit.

**Alex**: One thing I appreciate about this research is the intellectual honesty. The authors aren't anti-cloud. They're quantifying trade-offs that cloud providers don't advertise. AWS, Azure, and GCP have every incentive to launch new instance families with bigger headline numbers. Marketing departments love bigger numbers. But bigger numbers don't automatically mean better value.

**Jordan**: Viktor Leis and his team at TUM have done the community a genuine service. This is independent research that helps practitioners make informed decisions. It's the kind of work that should be happening more in our field. If you're doing capacity planning or cost optimization, bookmark cloudspecs.fyi.

**Alex**: Let's summarize the key statistics from the paper in a way you can share with your team. CPU cores increased 10x over the decade, but cost-adjusted performance only 2 to 3x. Memory bandwidth increased 5x, but cost-adjusted only 2x. Network increased 60x raw, and 10x cost-adjusted. That's the win. NVMe storage? Zero improvement in throughput. Negative improvement when you factor in that the 2016 i3 is still the best value by 2x.

**Jordan**: The practical takeaway is clear. Don't blindly adopt the latest instance families because marketing says they're better. Benchmark your actual workloads. Consider older instance types that may offer better economics. And recognize that cloud providers optimize for their margins, not your performance per dollar.

**Alex**: If you take one thing from this episode, let it be this. Question the assumption that newer equals better in cloud computing. The data shows that assumption is often wrong. And nine years after launch, the i3 might still be your best option for storage-intensive workloads.

**Jordan**: That's a great place to wrap. Cloud hardware stagnation is real, and now we have rigorous academic data to prove it. The paper is "Cloudspecs: Cloud Hardware Evolution Through the Looking Glass" from CIDR 2026. Authors Till Steinert, Maximilian Kuschewski, and Viktor Leis from the Technical University of Munich.

**Alex**: We've linked the paper, the interactive tool, and the GitHub repository in the show notes. If you found this analysis useful, share it with your team and your FinOps practitioners. These are the kinds of insights that can save real money on infrastructure spend.

**Jordan**: Until next time, keep questioning the defaults. Newer isn't always better. And sometimes the best instance for your workload is nine years old.
