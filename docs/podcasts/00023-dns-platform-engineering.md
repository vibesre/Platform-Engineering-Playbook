---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #023: DNS for Platform Engineering"
slug: 00023-dns-platform-engineering
---

# DNS for Platform Engineering: The Silent Killer

## The Platform Engineering Playbook Podcast

<GitHubButtons />

<iframe width="560" height="315" src="https://www.youtube.com/embed/qcDPewcDW6g" title="DNS for Platform Engineering: The Silent Killer" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

**Duration:** 23 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

## Listen to the Episode

<audio controls style={{width: '100%', marginBottom: '1.5rem'}}>
  <source src="https://platformengineeringplaybook.com/media/podcasts/00023-dns-platform-engineering/00023-dns-platform-engineering.mp3" type="audio/mpeg" />
  Your browser does not support the audio element.
</audio>

<PodcastSubscribeButtons />

---

**Jordan**: Today we're diving into DNS for platform engineering—and why this forty-year-old protocol remains the silent killer of production systems. October nineteenth, twenty twenty-five, eleven forty-eight PM. AWS US-EAST-1 goes down. Fifteen hours later, services are still failing.

**Alex**: And the root cause? A DNS automation race condition. Two DNS Enactors in DynamoDB's management system racing each other, one deletes all the IP addresses for the regional endpoint.

**Jordan**: It's always DNS, right? Except it's not funny when you're explaining downtime to the CEO. DNS is supposed to be simple—UDP, five hundred twelve byte limit, hierarchical lookups. So why does it keep taking down billion-dollar infrastructure?

**Alex**: Because we've layered so much complexity on top of that simple protocol. CoreDNS for service discovery, ExternalDNS for automation, GSLB for traffic management, service meshes. Each layer adds sophistication, but also new failure modes.

**Jordan**: And Kubernetes defaults that amplify your DNS queries by five times without you realizing it.

**Alex**: Yeah, the ndots-five trap. We'll get into that.

**Jordan**: We're going to investigate how DNS actually works under the hood—not just the "phone book" analogy—discover why modern platforms create new DNS failure modes, and give you the defensive playbook. Because DNS isn't just address resolution anymore. It's the nervous system of cloud-native platforms.

**Alex**: Service discovery, multi-region failover, CDN routing. When DNS fails, everything fails. But the ways it fails have evolved with our platforms, and most engineers don't understand the complete flow.

**Jordan**: So let's start with how DNS really works in modern platforms. Not the textbook version—the production reality.

**Alex**: Right, so a query starts in your pod. You make a request to, say, api.stripe.com. That goes to CoreDNS, which is your cluster DNS. CoreDNS is plugin-based—it's not a traditional DNS server with zone files. It's a chain of plugins.

**Jordan**: Wait, plugin chain? Like middleware?

**Alex**: Exactly. You've got middleware plugins that manipulate the request—error handling, metrics, caching—and backend plugins that provide the actual DNS data. The Kubernetes plugin watches the API server for Services and Endpoints, generates DNS responses on-the-fly for anything ending in cluster.local. It's dynamic, which is perfect for ephemeral pods.

**Jordan**: But that means if you're querying an external domain, CoreDNS forwards it upstream?

**Alex**: Yep, the forward plugin handles that. Sends it to your upstream recursive resolver—could be eight-eight-eight-eight, your corporate resolver, whatever you've configured. From there it's the traditional DNS hierarchy: recursive resolver queries root servers, TLD servers, authoritative servers, caches the response with a TTL, returns it back down the chain.

**Jordan**: And each of those layers is caching with different TTLs.

**Alex**: Exactly. Which is where things get interesting, because you don't control every resolver's behavior. But before we get to that, there's the ExternalDNS piece.

**Jordan**: Which automates DNS record management for your Ingresses and Services.

**Alex**: Right. ExternalDNS is a controller that watches Kubernetes resources and synchronizes DNS records with cloud providers—Route53, Cloud DNS, Azure DNS, fifty-plus providers via webhooks. Super useful for automating DNS, but it's also where you get automation race conditions like the AWS outage.

**Jordan**: Okay, so we've got this elegant simple protocol underneath, but we've stacked CoreDNS plugins, ExternalDNS automation, service mesh discovery, GSLB health checks on top. Where does it break?

**Alex**: Let's talk about the ndots-five trap, because this one bites everyone.

**Jordan**: I'm guessing this is a Kubernetes default that seemed like a good idea at the time?

**Alex**: Legacy compatibility with search domains. Kubernetes sets ndots-five in /etc/resolv.conf. The ndots parameter controls how many dots must appear in a name before DNS tries it as an absolute query. If your query has fewer than five dots, Kubernetes tries all the search domains first.

**Jordan**: So if I'm querying api.stripe.com—that's only two dots.

**Alex**: Right. So with ndots-five, Kubernetes first tries api.stripe.com.default.svc.cluster.local, then api.stripe.com.svc.cluster.local, then api.stripe.com.cluster.local, then api.stripe.com as a root query, and finally as an absolute query. That's five DNS queries for one external domain.

**Jordan**: Five queries. Four of them failing with NXDOMAIN.

**Alex**: Exactly. Five-times amplification on every external API call. I've seen production cases where a high-throughput service went from five hundred milliseconds latency to fifty milliseconds just by fixing ndots.

**Jordan**: So what's the fix?

**Alex**: Lower ndots to one in your pod's dnsConfig. Or use fully qualified domain names with a trailing dot—api.stripe.com.—which bypasses the search list entirely. And for high-throughput services, implement application-level DNS caching.

**Jordan**: This feels like one of those defaults where the cost is invisible until you're at scale.

**Alex**: That's the pattern with DNS. The complexity is hidden until it cascades. Let's talk about TTL balancing, because there's no perfect answer here.

**Jordan**: Low TTL for fast failover, high TTL for performance. Classic trade-off.

**Alex**: Yeah, but the stakes are different depending on your service. If you're load-balancing backends that change frequently, you want low TTL—sixty to three hundred seconds—so failover is fast. But that increases query load on your DNS servers and upstream resolvers.

**Jordan**: And high TTL—like thirty minutes to a day—gives you better performance and reduces load, but delays failover.

**Alex**: Right. And here's the catch: you don't control the DNS caching hierarchy. Some ISP resolvers ignore your TTL hints. You can set TTL to sixty seconds, but if a resolver decides to cache for five minutes, you're stuck waiting.

**Jordan**: So your failover SLO is only as good as the worst resolver in the chain.

**Alex**: Exactly. Now let me throw another wrench in: anycast routing. Everyone thinks anycast routes to the nearest node for lowest latency.

**Jordan**: It doesn't?

**Alex**: Not necessarily. BGP routing uses AS-path length and policy, not geographic proximity. Studies show many queries travel to anycast sites much farther than the closest, inflating latency due to propagation delay. If you've got strict performance requirements, you need to configure anycast prefix advertisements carefully.

**Jordan**: So "nearest" in BGP terms isn't "nearest" in latency terms.

**Alex**: Right. And then there's GSLB—Global Server Load Balancing. GSLB manipulates DNS responses based on health checks and geography. Sounds great until you realize that if a health check fails and GSLB returns new IPs, those are subject to TTL caching. Three hundred second TTL means five minutes before all resolvers see the failover.

**Jordan**: And cached negative responses can persist even longer.

**Alex**: Yep. So all these layers—CoreDNS plugins, ExternalDNS automation, service mesh discovery, GSLB health checks—they add sophistication, but they also add new failure modes. And when you look at the outage postmortems, that's exactly the pattern.

**Jordan**: Okay, let's talk about the AWS outage, because that's a masterclass in how DNS automation can cascade globally.

**Alex**: October nineteenth to twentieth, twenty twenty-five. DynamoDB's DNS management system has two components for availability: a DNS Planner that monitors load balancer health and creates DNS plans, and a DNS Enactor that applies changes via Route 53.

**Jordan**: Separation of concerns. Planner decides what to do, Enactor executes it.

**Alex**: Right, but here's where the race condition happens. You've got multiple DNS Enactors for redundancy. One Enactor is slow, working through an old DNS plan. Meanwhile, the Planner keeps running, generating newer plans. Another Enactor picks up a newer plan and rapidly progresses through all the endpoints.

**Jordan**: So the fast Enactor finishes while the slow one is still applying the old plan.

**Alex**: Exactly. Fast Enactor completes, invokes the cleanup process to delete old plans. But at the same time, the slow Enactor applies its old plan to the regional DynamoDB endpoint, overwriting the newer plan. Then cleanup runs, sees this plan is many generations old, deletes it. All IP addresses for the regional endpoint—gone. Empty DNS record.

**Jordan**: Fifteen hours of cascading failures because two automation processes raced and cleanup won.

**Alex**: Yeah. DynamoDB goes down, takes all dependent AWS services with it—customer traffic, internal AWS services that rely on DynamoDB. Slack, Atlassian, Snapchat, all downstream. AWS disabled the DNS Planner and Enactor automation globally.

**Jordan**: What's the lesson there? Don't automate DNS changes?

**Alex**: No, the lesson is DNS automation needs coordination locks, generation tracking, and safeguards against empty records. Race conditions in DNS cascade globally because DNS is the foundation. You can't treat DNS changes like normal automation.

**Jordan**: And it's not just AWS. Salesforce in May twenty twenty-five—engineer's "quick fix" to DNS configuration bypassed review, cascaded across infrastructure.

**Alex**: Right. There's no such thing as a quick DNS fix. DNS changes require thorough testing, staged rollouts, automated rollback. And then AdGuard in September—traffic rerouting redirected Asian users to Frankfurt, Frankfurt capacity couldn't handle the three-times load spike.

**Jordan**: So capacity planning has to model failover scenarios, not just normal traffic patterns.

**Alex**: Exactly. These outages reveal the same pattern: simple protocol, complex systems, brittle automation. DNS failures aren't usually protocol issues—they're automation bugs, capacity planning gaps, configuration errors. Understanding how all the pieces fit together is your only defense.

**Jordan**: Okay, so what's the defensive playbook? Because I'm assuming there's more to it than "be careful with DNS."

**Alex**: Yeah, it's a five-layer defense. Optimization to reduce query volume, failover for multi-region resilience, security to prevent hijacking, monitoring for visibility, and testing to simulate failures before production.

**Jordan**: Let's start with optimization, because I want to fix that ndots-five trap.

**Alex**: First, lower ndots to one in your pod specs. Add dnsConfig with ndots-one, eliminates four-times amplification for external domains. Second, use FQDNs with trailing dots—api.example.com.—bypasses the search list entirely, drops you from five queries to one.

**Jordan**: What about CoreDNS itself?

**Alex**: Tune the CoreDNS cache. Increase cache size to ten thousand records, TTL to thirty seconds. In your Corefile, that's cache-thirty with success-ten-thousand. And for high-throughput services, implement application-level caching—cache DNS results with TTL respect, don't hammer CoreDNS on every request.

**Jordan**: Latency benchmarks—what should we be aiming for?

**Alex**: Under twenty milliseconds is excellent, that's local. Twenty to fifty milliseconds is solid for cloud. Fifty to one hundred is acceptable. But once you're over one hundred milliseconds, you're degrading application performance—that's your warning threshold. Three hundred-plus is critical.

**Jordan**: Okay, failover. How do we design multi-region resilience?

**Alex**: GSLB with health checks. Use Route53 or equivalent, health checks monitoring your endpoints every thirty seconds. Failover routing policy with primary and secondary regions. For active-active, use latency-based routing.

**Jordan**: And TTL strategy?

**Alex**: Sixty to three hundred seconds for load-balanced backends—fast failover. Thirty-six hundred to eighty-six thousand four hundred seconds for stable infrastructure. You're balancing failover speed against query load.

**Jordan**: Multi-provider strategy?

**Alex**: Don't rely on a single DNS provider. Use NS records with multiple providers—Route53 plus Cloudflare. Client-side resolver fallback—eight-eight-eight-eight plus one-one-one-one. And combine Route53 health checks with CloudWatch alarms so you can failover based on application metrics, not just ping.

**Jordan**: What about security? Because we haven't talked about DNS hijacking.

**Alex**: Three pieces. DNSSEC for integrity, DoH or DoT for confidentiality, and enterprise control over resolvers. DNSSEC validates authenticity of responses, prevents cache poisoning and man-in-the-middle. But it doesn't encrypt traffic.

**Jordan**: That's where DoH and DoT come in.

**Alex**: Right. DNS-over-HTTPS uses port four forty-three, blends with HTTPS traffic. DNS-over-TLS uses port eight fifty-three, visible but encrypted. Mozilla's twenty twenty-four study showed ninety percent reduction in third-party tracking with DoH.

**Jordan**: But enterprises lose visibility.

**Alex**: Exactly. NSA's recommendation: use DoH with internal enterprise resolvers, not public one-one-one-one. Block external DNS queries on ports fifty-three and eight fifty-three. Validate DNSSEC. That maintains security visibility while encrypting queries. It's DNSSEC for integrity plus DoH for confidentiality, not either-or.

**Jordan**: Okay, monitoring. What metrics actually matter?

**Alex**: Query latency first. Track p-fifty, p-ninety-five, p-ninety-nine. Alert if p-ninety-five exceeds one hundred milliseconds for warning, three hundred for critical. Break down by query type—A, quad-A, SRV—and destination—internal versus external.

**Jordan**: Error rates?

**Alex**: Yep. Monitor NXDOMAIN, SERVFAIL, REFUSED, timeouts. Spike in NXDOMAIN might indicate misconfigured apps. SERVFAIL indicates upstream issues. Also track top requesters—identify pods generating high DNS volume. Could be missing application-level caching or runaway retry loops.

**Jordan**: And upstream health?

**Alex**: Monitor CoreDNS to upstream resolver latency and error rates. Detects if your upstream—eight-eight-eight-eight, corporate resolver—is slow or failing. Tools like Datadog DNS monitoring, Prometheus CoreDNS metrics, custom exporters for ExternalDNS sync lag.

**Jordan**: Last piece—testing. How do we simulate DNS failures before they hit production?

**Alex**: DNS failure game days. Kill CoreDNS pods, block port fifty-three, inject latency with chaos engineering tools. Observe saturation on queues, thread pools, application behavior. Does your app degrade gracefully or crash hard?

**Jordan**: Capacity modeling?

**Alex**: Load test your DNS resolvers with realistic query patterns. Model failover scenarios—what if Asian traffic routes to Europe? That's the AdGuard lesson. And test DNS changes in staging with the same query load as production. Automate rollback if error rate spikes.

**Jordan**: Client resilience?

**Alex**: Applications should retry DNS queries with exponential backoff, fall back to cached IPs, degrade gracefully when DNS is unavailable. Because no matter how well you've designed your DNS infrastructure, it will fail at some point.

**Jordan**: So to recap the defensive playbook: optimize to reduce query volume—fix ndots, use FQDNs, tune caching. Design multi-region failover with GSLB and balanced TTLs. Secure with DNSSEC plus DoH using internal resolvers. Monitor latency and error rates with meaningful thresholds. Test failures before production with game days.

**Alex**: And understand that DNS isn't simple anymore. You've got CoreDNS plugin chains, ExternalDNS automation, service mesh discovery, GSLB health checks—it's complex distributed systems engineering. The only defense is understanding how all the pieces fit together.

**Jordan**: Because when DNS fails, it's not just "the internet is down." It's DynamoDB cascading to Slack and Atlassian. It's five-hundred millisecond latency because of ndots-five. It's traffic rerouting overwhelming your datacenter capacity.

**Alex**: Right. And "it's always DNS" stops being a joke when you've got the playbook. You can debug production latency issues, design resilient failover, optimize for your workload, monitor the right metrics, simulate failures before they happen.

**Jordan**: The simple protocol isn't simple anymore, but you're ready for it.

**Alex**: Exactly. DNS is the nervous system of cloud-native platforms. When you understand how it works—really works, not just the "phone book" analogy—you can prevent your platform from becoming the next postmortem.

**Jordan**: That's the defensive playbook. Optimize, failover, secure, monitor, test. And understand that every layer of abstraction adds new failure modes.

**Alex**: The AWS outage, the Salesforce disruption, the AdGuard capacity failure—they all had one thing in common. DNS automation without the defensive playbook. Now you've got the playbook.

**Jordan**: Don't just assume DNS works. Understand why it's the silent killer, and tame it.
