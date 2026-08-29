---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #088: AWS Route 53 Global Resolver"
slug: 00088-aws-route-53-global-resolver
---

# Episode #088: AWS Route 53 Global Resolver - Enterprise DNS Security at the Edge

<GitHubButtons/>

**Duration**: 20 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Platform engineers, DevOps engineers, SREs, network architects

> 📰 **News Segment**: This episode covers Claude Code creator workflows, UK encryption backdoors, K8s EU hosting costs, PostgreSQL replacing Redis, and Rust ecosystem security before the main topic.

## Episode Summary

Every DNS query your hybrid environment makes could be exposing sensitive data - unencrypted, unfiltered, and vulnerable to interception. AWS Route 53 Global Resolver, announced at re:Invent 2025 and currently in preview, combines anycast routing, encrypted DNS protocols (DoH/DoT), and managed threat intelligence in a single offering. This fundamentally changes how platform teams can architect hybrid DNS without complex VPN or Direct Connect setups.

This episode covers the technical architecture of Global Resolver's anycast DNS system across 11 AWS regions, the authorization model using AWS RAM, DNS filtering capabilities with managed threat lists, and practical implementation patterns for hybrid environments with on-premises clients and remote workforces.

## News Segment

**Claude Code Creator Workflow (InfoQ)** - Boris Cherny reveals how he uses Claude Code for development - treating it as a pair programming partner that needs context and course correction, breaking down complex tasks, and exploring codebases before making changes.

**UK Orders Ofcom to Explore Encryption Backdoors** - Government directive to investigate backdoor requirements for encrypted communications. Implications for encryption architecture in multinational deployments and regulatory precedent.

**K8s Hosting Costs: Big 3 vs EU Alternatives** - eucloudcost.com comparison reveals cost differences between hyperscalers and EU alternatives. Data sovereignty requirements driving demand for local cloud providers.

**PostgreSQL Replacing Redis** - dev.to article on using Postgres for caching with LISTEN/NOTIFY for pub/sub patterns. Operational simplification by running one database well instead of two adequately.

**Rust Ecosystem Security: crates.io Deep Dive** - Analysis of dependency trust, maintainer patterns, and supply chain risk. Familiar patterns: concentration risk, transitive dependency sprawl, package verification challenges.

## Key Takeaways

- **Anycast DNS Architecture**: Global anycast IPs route queries to nearest AWS region (11 regions) - no VPN required
- **Encrypted Protocols**: DoH (port 443), DoT (port 853), and traditional Do53 (port 53) supported
- **AWS RAM Authorization**: Associate accounts once, all private hosted zones automatically resolvable - no credentials in resolver configs
- **DNS Filtering**: Managed domain lists for malware, botnet C2, and phishing with custom block/allow lists
- **Query Logging**: CloudWatch, S3, or Kinesis Firehose for centralized audit trail and threat hunting
- **Migration Pattern**: Deploy alongside existing infrastructure, test non-critical workloads, gradually migrate

## Platform Team Action Items

1. **Request preview access** through AWS account team or re:Invent contacts
2. **Evaluate hybrid DNS needs** - identify on-premises clients resolving AWS private zones
3. **Test DoH/DoT support** on corporate devices (Windows 11, macOS, iOS, Android all support DoH)
4. **Plan RAM associations** for multi-account organizations
5. **Enable DNS filtering** with managed threat lists for immediate protection

## Resources

- [AWS Route 53 Global Resolver Documentation](https://docs.aws.amazon.com/route53/latest/userguide/resolver-global-resolver.html) - Official AWS documentation
- [RFC 8484: DNS Queries over HTTPS (DoH)](https://datatracker.ietf.org/doc/html/rfc8484) - DoH specification
- [RFC 7858: DNS over Transport Layer Security (DoT)](https://datatracker.ietf.org/doc/html/rfc7858) - DoT specification
- [Claude Code Creator Workflow (InfoQ)](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/) - Boris Cherny's development patterns
- [EU Cloud Cost Comparison](https://www.eucloudcost.com) - K8s hosting cost analysis

## Transcript

**Alex**: Welcome to the Platform Engineering Playbook Daily Podcast. Today's news and a deep dive to help you stay ahead in platform engineering.

**Jordan**: Every DNS query your hybrid environment makes could be exposing sensitive data. Unencrypted, unfiltered, and vulnerable to interception. Today we're looking at AWS Route 53 Global Resolver, a new service announced at re:Invent 2025 that combines anycast routing, encrypted DNS protocols, and managed threat intelligence in a single offering. This is one of those services that doesn't get the headlines but fundamentally changes how platform teams can architect hybrid DNS.

**Alex**: Before we dive into Global Resolver, let's cover today's news. We've got five stories covering AI-assisted development workflows, encryption policy, Kubernetes cost comparisons, database architecture, and supply chain security.

**Jordan**: First, InfoQ has an article on Boris Cherny, the creator of Claude Code, revealing how he uses the tool for his own development workflow. This is interesting because it shows patterns for AI-assisted development from someone who built one of the most sophisticated coding assistants. The key insight is using Claude Code iteratively rather than expecting perfect output on the first try. He treats it as a pair programming partner that needs context and course correction.

**Alex**: The workflow patterns he describes include breaking down complex tasks into smaller prompts, providing relevant file context upfront, and using the tool to explore codebases before making changes. For platform engineers adopting AI assistants, this is valuable context on what effective usage looks like from an expert practitioner.

**Jordan**: Second, the UK government has ordered Ofcom to explore encryption backdoors. This directive instructs the regulator to investigate requiring backdoor access to encrypted communications. The security and privacy implications here are significant. Backdoors don't stay secret. Any mandated weakness becomes a target for adversaries.

**Alex**: For platform engineers, this raises questions about encryption architecture in multinational deployments. If the UK mandates backdoors and your infrastructure spans jurisdictions, you face compliance complexity. This is worth tracking even if you're not UK-based, because regulatory precedent tends to spread. The EU and other jurisdictions watch what the UK does with encryption policy.

**Jordan**: Third, a new comparison from EU Cloud Cost examines Kubernetes hosting costs between the Big Three hyperscalers and EU alternatives. Data sovereignty requirements in Europe have driven demand for local cloud providers, and this analysis shows how they stack up on price. The findings suggest meaningful cost differences depending on workload profile.

**Alex**: The takeaway for platform teams is that cloud cost optimization isn't just about reserved instances and spot pricing within one provider. Multi-cloud or regional providers may offer better economics for specific use cases, especially when sovereignty requirements are in play. If you're running Kubernetes in Europe and haven't evaluated alternatives to AWS, Azure, and GCP, this is worth a look.

**Jordan**: Fourth, a dev.to article titled "I Replaced Redis with PostgreSQL And It's Faster" makes a provocative claim. The author describes using Postgres for caching workloads that traditionally went to Redis, leveraging Postgres's LISTEN/NOTIFY functionality for pub/sub patterns. Their benchmarks show comparable or better performance for their specific use case.

**Alex**: This isn't universal advice. Redis excels at certain patterns. But the underlying insight is valuable. Operational complexity has real costs. Running one database well is often better than running two databases adequately. If your Postgres already has headroom and your caching needs are modest, eliminating Redis simplifies your stack. Every additional stateful service is another thing to back up, monitor, and secure.

**Jordan**: Fifth, a deep analysis of the Rust ecosystem examines security in crates.io. The research looks at dependency trust, maintainer patterns, and supply chain risk in the Rust package ecosystem. While Rust's memory safety gets attention, the supply chain aspects of any package ecosystem remain a risk surface.

**Alex**: The findings highlight familiar patterns from other ecosystems. Concentration risk where critical packages have few maintainers. Transitive dependency sprawl that expands attack surface. And the challenge of verifying that published packages match source repositories. If you're adopting Rust for infrastructure tooling, the language safety benefits are real, but supply chain hygiene still requires attention.

**Jordan**: Now let's dive into our main topic. AWS Route 53 Global Resolver. This service was announced at re:Invent 2025 and is currently in preview. It addresses a fundamental challenge in hybrid cloud environments. How do you give on-premises or remote clients access to AWS private hosted zones without complex VPN or Direct Connect setups?

**Alex**: Let me set the context on why this matters. In a typical hybrid environment, you have applications running on-premises that need to resolve AWS private DNS names. Maybe your database is in RDS and your on-prem app needs to find it at database.prod.internal.company.com. That's a Route 53 private hosted zone. How does your on-prem server resolve it?

**Jordan**: The traditional approach is Route 53 Resolver Endpoints. You create inbound and outbound endpoints in your VPC, connect your on-prem network via VPN or Direct Connect, and forward DNS queries through that private path. It works, but it has limitations. The VPN or Direct Connect adds latency. You need to manage the connectivity. And if you have mobile or remote workers, they need VPN access just to resolve internal DNS names.

**Alex**: There's also a security gap. Traditional DNS on port 53 is unencrypted. Any network observer can see your DNS queries. They know what hostnames you're looking up, which reveals information about your infrastructure and application architecture. Even if the actual traffic is encrypted, the DNS metadata is exposed.

**Jordan**: Global Resolver addresses both problems. First, it uses anycast IP addresses that route queries to the nearest AWS region. No VPN required. Your on-prem resolver just points at these anycast addresses over the public internet. Second, it supports encrypted DNS protocols. DoH, that's DNS over HTTPS on port 443, and DoT, DNS over TLS on port 853. The queries are encrypted end-to-end.

**Alex**: Let me explain the anycast architecture because it's elegant. AWS gives you global anycast IP addresses. When your client sends a DNS query to that IP, BGP routing automatically directs it to the nearest AWS region. If you're in Frankfurt, your query goes to the Frankfurt region. If you're in Tokyo, it goes to Tokyo. No configuration needed. It's the same IP address everywhere, but BGP handles geographic optimization.

**Jordan**: Currently Global Resolver is available in eleven regions. In the US you have Northern Virginia, Ohio, Northern California, and Oregon. In Europe there's Frankfurt, Ireland, and London. Asia Pacific covers Mumbai, Singapore, Tokyo, and Sydney. AWS will expand this over time, but eleven regions already covers most enterprise footprints.

**Alex**: Now let's talk about how authorization works, because this is crucial for security. Global Resolver uses AWS Resource Access Manager, or AWS RAM, for access control. You associate your AWS accounts with the Global Resolver, and then any private hosted zones in those accounts become resolvable. The client doesn't need AWS credentials. Authorization happens at the account level through RAM.

**Jordan**: This is a key architectural decision. There's no IAM policy or API key in your on-prem resolver configuration. The authorization is implicit based on which accounts you've associated. Your on-prem client just sends a DNS query for database.prod.internal. Global Resolver checks if that zone is in an associated account, and if so, resolves it. If not, it forwards to public DNS.

**Alex**: This simplifies configuration dramatically. Imagine you have twenty AWS accounts across your organization. Each account has private hosted zones for its workloads. With traditional Resolver Endpoints, you'd need to configure forwarding rules for each zone. With Global Resolver, you associate all twenty accounts once, and every private zone is automatically resolvable. Add a new account? Associate it and you're done.

**Jordan**: The protocol support is comprehensive. DoH, DNS over HTTPS, uses standard HTTP/2 on port 443. This is great because port 443 is almost never blocked by firewalls. DoT, DNS over TLS, uses port 853. Both encrypt the DNS query and response. And for legacy compatibility, traditional DNS on port 53 is also supported, though unencrypted.

**Alex**: From a platform engineering perspective, the migration path is straightforward. If your clients support DoH or DoT, configure them to use the Global Resolver anycast IP. Most modern operating systems and browsers support DoH natively. Windows 11, macOS, iOS, and Android all have DoH support. For servers, stub resolvers like systemd-resolved can be configured for DoT.

**Jordan**: But Global Resolver isn't just about resolution. It includes DNS filtering, which is where the security value really compounds. AWS provides managed domain lists for malware command and control, botnet infrastructure, and phishing domains. You can enable these filters and every DNS query through Global Resolver gets checked against them.

**Alex**: Think about what this means for security posture. Your on-prem servers, your remote workers, your branch offices, they're all resolving DNS through Global Resolver. If a compromised system tries to contact a known malware domain, the query gets blocked before any connection happens. DNS-level filtering is one of the most effective and lowest overhead security controls available.

**Jordan**: You can also create custom block and allow lists. Maybe you want to block access to certain categories of sites from corporate devices, or ensure that only approved SaaS providers can be resolved. The filtering happens at DNS resolution time, which is earlier in the request lifecycle than most other controls. No connection is even attempted if DNS filtering blocks it.

**Alex**: Query logging is built in too. You can send logs to CloudWatch, S3, or Kinesis Firehose. This creates a centralized audit trail of all DNS queries from your hybrid environment. For security teams, this is valuable for threat hunting. Unusual DNS patterns, queries to suspicious domains, or resolution attempts that shouldn't happen, it's all visible in one place.

**Jordan**: Let me walk through a concrete implementation pattern. Say you have a hybrid environment with an on-premises data center, several AWS accounts, and a remote workforce. Here's how you'd deploy Global Resolver.

**Alex**: First, you'd set up a central networking account in AWS that owns the Global Resolver configuration. This is where you define filtering policies and logging. Then you associate your workload accounts through AWS RAM. Each workload account that has private hosted zones gets associated. The private zones are automatically resolvable without additional configuration.

**Jordan**: Second, you configure your on-premises DNS infrastructure. Your internal DNS servers, maybe Windows DNS or BIND, get conditional forwarders or forwarding zones pointing to the Global Resolver anycast IP. Queries for your AWS private zones get forwarded to Global Resolver. Everything else follows your existing DNS infrastructure.

**Alex**: Third, for the remote workforce, you push DoH configuration through your device management platform. MDM policies can configure DoH resolvers on Windows, macOS, and mobile devices. Remote workers get access to internal AWS resources without needing VPN for DNS resolution. Note that they still need network access to the actual resources, but service discovery works from anywhere.

**Jordan**: Fourth, enable DNS filtering with the managed threat lists. AWS maintains lists of known bad domains for malware, botnets, and phishing. Enabling these provides immediate protection without you curating threat intelligence yourself. You can add custom lists for organizational policies on top.

**Alex**: Finally, configure query logging to your SIEM or security data lake. Firehose to S3 with Athena for ad hoc queries, or direct CloudWatch integration if you're already centralized there. This gives your security team visibility into DNS patterns across the entire hybrid environment.

**Jordan**: There are some important limitations to understand since this is still in preview. IPv6 is not supported during preview but will be available at general availability. The eleven regions I mentioned are the current coverage, though AWS is expanding. And there are query rate limits during preview that will increase at GA. For most enterprise use cases these aren't blockers, but plan accordingly.

**Alex**: Let's compare this to the alternatives so you can make an informed decision. Traditional Route 53 Resolver Endpoints remain the right choice for VPC-to-VPC resolution where everything stays within AWS. They're also appropriate when compliance requirements mandate private network connectivity for all traffic, including DNS. Some regulated environments explicitly require traffic to stay off the public internet.

**Jordan**: Self-managed DNS resolvers, like running your own BIND or Unbound servers, give you maximum control but maximum operational burden. You're responsible for high availability, patching, scaling, and maintaining the filtering rules. For organizations with strong DNS expertise this might make sense, but most platform teams would rather delegate this to a managed service.

**Alex**: Public DNS resolvers like Cloudflare 1.1.1.1 or Google 8.8.8.8 support DoH and DoT, but they can't resolve your AWS private hosted zones. They're useful for public resolution with encryption, but they don't solve the hybrid environment problem. Global Resolver fills the gap between public encrypted DNS and private zone resolution.

**Jordan**: From a cost perspective, AWS hasn't published final pricing yet since it's in preview, but expect per-query pricing similar to other DNS services. The value proposition is reducing the cost and complexity of VPN and Direct Connect infrastructure that you might otherwise need just for DNS. Factor in query logging storage costs and the operational savings from not managing your own resolver infrastructure.

**Alex**: The platform engineering implications are significant. DNS is the control plane for service discovery. Every time a service connects to a database, cache, or API, it starts with a DNS query. Latency in DNS resolution multiplies across your entire application. Anycast routing means queries go to the nearest region, minimizing DNS latency regardless of where your clients are located.

**Jordan**: Security posture improves on multiple dimensions. Encrypted DNS eliminates query metadata exposure. DNS filtering provides defense in depth against malware and phishing. Centralized logging enables threat detection. And the authorization model through RAM means no credentials floating around in resolver configurations.

**Alex**: For multi-account AWS organizations, the operational simplification is substantial. Instead of managing Resolver Endpoint associations and forwarding rules across dozens of accounts, you associate accounts once and private zones are automatically resolvable. As you add new accounts and zones, no additional configuration is needed.

**Jordan**: The migration strategy for most organizations would be phased. Start by deploying Global Resolver alongside your existing infrastructure. Test with non-critical workloads to validate resolution works correctly. Monitor query logs for any unexpected patterns. Then gradually migrate more traffic as confidence builds.

**Alex**: One thing to note is that Global Resolver handles the DNS layer only. Service discovery gives you the IP address, but you still need network connectivity to reach that address. For on-prem systems accessing AWS resources, you still need VPN, Direct Connect, or public endpoints for the actual data traffic. Global Resolver doesn't replace your network connectivity. It simplifies DNS resolution.

**Jordan**: Let's summarize with some practical guidance. If you're running a hybrid environment with on-premises clients that need to resolve AWS private hosted zones, Global Resolver is worth evaluating immediately. The combination of anycast routing, encrypted protocols, and managed threat filtering is compelling.

**Alex**: If you have a remote workforce that needs access to internal AWS resources, DoH configuration through Global Resolver could simplify your architecture. They get DNS-based service discovery without VPN, and you get centralized visibility and filtering.

**Jordan**: For security teams, the DNS filtering and logging capabilities provide defense in depth that's difficult to achieve otherwise. DNS-level blocking stops malicious connections before they start. Query logging creates an audit trail for threat hunting and incident response.

**Alex**: For multi-account organizations, the RAM-based authorization simplifies what would otherwise be complex cross-account DNS forwarding. Associate accounts once, and all their private zones are resolvable. That operational simplification has real value.

**Jordan**: Route 53 Global Resolver represents AWS thinking holistically about hybrid DNS. Not just private zone resolution, but encrypted transport, threat filtering, and centralized logging in one managed service. It's the kind of infrastructure primitive that platform teams can build on.

**Alex**: If you're attending re:Invent or have AWS account team access, request preview access now. Test it with your hybrid environment. Understand how it fits your DNS architecture before general availability. Early experience helps you plan the migration when it goes GA.

**Jordan**: DNS doesn't get the attention it deserves in platform engineering. It's foundational infrastructure that everyone depends on but few optimize. Global Resolver makes encrypted, filtered, anycast DNS accessible to hybrid environments in a way that wasn't practical before.

**Alex**: That's a good place to wrap. Route 53 Global Resolver, announced at re:Invent 2025, currently in preview. Anycast DNS with DoH and DoT support, AWS RAM authorization for private hosted zones, managed threat filtering, and centralized query logging. Check the AWS documentation for preview access details.

**Jordan**: We've linked the AWS announcement, documentation, and RFC specifications for DoH and DoT in the show notes. If you're running hybrid infrastructure, this is worth your time to evaluate. DNS security and performance improvements compound across every service in your environment.

**Alex**: And remember, every DNS query is a potential information leak if it's unencrypted. Global Resolver gives you encryption by default with anycast performance. That's a significant improvement over traditional DNS architectures.

**Jordan**: Until next time, keep your DNS encrypted and your threat lists updated. The control plane matters as much as the data plane.
