---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #077: When Serverless Fails"
slug: 00077-unkey-serverless-containers-migration
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #077: When Serverless Fails - Unkey's 6x Performance Migration to Containers

<GitHubButtons />

**Duration**: 16 minutes | **Speakers**: Alex and Jordan | **Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

<iframe width="100%" height="315" src="https://www.youtube.com/embed/VIDEO_ID_PLACEHOLDER" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

## Episode Summary

Why did an API key management platform abandon edge serverless for stateful containers? Unkey rebuilt their entire service after hitting 30ms p99 cache latency when they needed sub-10ms. The result: 6x performance improvement. This episode breaks down the technical decision-making framework every platform engineer needs.

### Key Points

- **Root Cause**: 30ms p99 cache latency from serverless statelessness (target was sub-10ms)
- **Solution**: Migrated from Cloudflare Workers to AWS Fargate with Global Accelerator
- **Result**: 6x performance improvement
- **Insight**: "Zero network requests are always faster than one network request"
- **Bonus**: Self-hosting became trivial with containers

---

## News Segment: Kubernetes 1.35 z-Pages

| Topic | Details |
|-------|---------|
| **What** | Kubernetes 1.35 adds structured JSON responses to z-pages debug endpoints |
| **Endpoints** | `/statusz` (component info, version, uptime) and `/flagz` (command-line arguments) |
| **Key Feature** | HTTP content negotiation for JSON output with API versioning |
| **Use Cases** | Compliance automation, configuration drift detection, automated audits |
| **Access** | RBAC via `system:monitoring` group |
| **Status** | Alpha feature (requires `ComponentStatusz` and `ComponentFlagz` feature gates) |

---

## The Serverless Failure Mode

Unkey is an API key management platform with a core verify endpoint that must respond in under 40ms globally. They built on the full Cloudflare stack:

- **Workers** for compute
- **Durable Objects** for stateful coordination
- **Workers KV** for key-value storage
- **Caches** for performance
- **Logstreams, Queues, Workflows** for async processing
- **Custom Go proxy (chproxy)** to buffer analytics for ClickHouse

The fundamental problem: in serverless, every cache read requires a network request. There's no persistent memory between function invocations.

## The Complexity Tax

According to Unkey's co-founder Andreas Thomas, they spent more time evaluating and integrating Cloudflare-specific SaaS products than building features for customers. They were "solving problems the architecture created rather than customer problems."

The vendor lock-in was significant: 6+ Cloudflare-specific services with no easy migration path.

## The Container Solution

- **AWS Fargate** for compute
- **Global Accelerator** for global traffic distribution
- **Long-lived Go processes** with in-memory caching

Result: 6x performance improvement and self-hosting as an unexpected bonus.

## Decision Framework

Five questions to evaluate serverless vs containers:

1. **Where are you in the request path?** Calling APIs vs being the API
2. **What's your p99 latency target?** Sub-10ms requires different architecture
3. **How hot is your data?** Frequently accessed data wants memory
4. **What's your complexity budget?** Count vendor-specific services
5. **Can you self-host if needed?** Containers make this trivial

## Key Statistics

| Metric | Before | After |
|--------|--------|-------|
| p99 Cache Latency | 30ms | Sub-10ms |
| Performance | Baseline | 6x improvement |
| Target SLA | sub-40ms verify endpoint | Met |

---

## Resources

- [Unkey Blog: Why We're Leaving Serverless](https://unkey.com/blog)
- [Kubernetes Blog: v1.35 Structured z-pages](https://kubernetes.io/blog/)
- [AWS Global Accelerator Documentation](https://aws.amazon.com/global-accelerator/)

---

## Full Transcript

**Alex**: Welcome to the Platform Engineering Playbook Daily Podcast—today's news and a deep dive to help you stay ahead in platform engineering.

Today we're covering a counterintuitive migration story that's challenging assumptions about serverless. Unkey, an API key management platform, just rebuilt their entire service from scratch—moving from Cloudflare Workers to stateful containers. The result? A six-fold performance improvement.

**Jordan**: Wait, I need to process that. A company that went all-in on edge serverless—Cloudflare Workers, Durable Objects, the whole ecosystem—decided to rip it out and go back to containers?

**Alex**: Yeah, and the reasoning is fascinating from a platform engineering perspective. But before we dig into that, we've got some Kubernetes news that's actually relevant to today's theme around infrastructure observability.

**Jordan**: The z-pages update in 1.35?

**Alex**: Exactly. And I want to spend a bit more time on this one because the technical implementation is genuinely useful for platform engineers.

**Jordan**: Let's do it.

**Alex**: So z-pages are these debug endpoints that Kubernetes control plane components expose—kube-apiserver, controller-manager, scheduler, kubelet, kube-proxy. They've been around since 1.32 as alpha features, but 1.35 adds something significant: structured JSON responses with proper API versioning.

**Jordan**: Break that down. What endpoints are we talking about?

**Alex**: Two main ones. First, slash-statusz—gives you high-level component info like version, start time, uptime, and available debug paths. Second, slash-flagz—exposes all the command-line arguments the component was started with. Sensitive values are redacted.

**Jordan**: So instead of kubectl exec into a control plane pod and grepping process args, you can just hit an HTTP endpoint?

**Alex**: Right, but here's what's new in 1.35. Previously, these endpoints returned plain text. If you wanted to parse that programmatically, you were writing fragile regex. Now, you can request structured JSON using HTTP content negotiation.

**Jordan**: How does that work exactly?

**Alex**: You set an Accept header with a specific format: application slash json, semicolon, v equals v1alpha1, semicolon, g equals config.k8s.io, semicolon, as equals Statusz—or Flagz for the other endpoint. The response comes back as proper typed JSON with an API version, kind, metadata, and the actual data fields.

**Jordan**: That's the Kubernetes API pattern applied to debug endpoints.

**Alex**: Exactly. And it enables versioned evolution. Right now it's v1alpha1, but they can ship v1beta1, then v1 as it stabilizes, and clients can request the version they support.

**Jordan**: What's the actual JSON look like for flagz?

**Alex**: You get a flags object where each key is the flag name and the value is what it's set to. So authorization-mode might be Node comma RBAC in brackets, profiling might be true or false. You can pipe that straight to jq and check specific settings.

**Jordan**: I'm thinking compliance automation. Verify RBAC is enabled across all clusters, confirm profiling is disabled in production.

**Alex**: That's the use case. Configuration drift detection. Automated audits. No more shelling into nodes or parsing kubectl describe output. Just hit the endpoint, get structured data, compare against your policy.

**Jordan**: Security model?

**Alex**: RBAC via the system monitoring group. Same authorization as healthz, livez, readyz. You need proper authentication unless anonymous auth is enabled, which it shouldn't be in production.

**Jordan**: What's the catch?

**Alex**: Alpha feature. Requires feature gates—ComponentStatusz and ComponentFlagz. The API format might change before it goes stable. So it's great for building internal tooling now, but I wouldn't make production monitoring depend on it until it hits beta.

**Jordan**: Fair. The curl command with all those cert flags isn't exactly friendly either.

**Alex**: True, but that's just Kubernetes security doing its job. The point is—this is infrastructure getting more introspectable. Which ties into our main topic nicely.

**Jordan**: The Unkey migration. Let's get into it.

**Alex**: So Unkey is an API key management platform. Their core product is a verify endpoint—applications send API keys, Unkey validates them and returns metadata in under 40 milliseconds globally. They handle rate limiting, usage analytics, key rotation.

**Jordan**: So they're in the request path for their customers' applications. Every API call hits Unkey first.

**Alex**: Right. And that's the critical context. They're not calling APIs—they ARE the API that thousands of other applications depend on. Every millisecond of latency they add compounds across their customers' entire request chains.

**Jordan**: And they built this on Cloudflare Workers initially?

**Alex**: The full Cloudflare stack. Workers for compute, Durable Objects for stateful coordination, Workers KV for key-value storage, Caches for performance, plus Logstreams, Queues, and Workflows for async processing. They even built a custom Go proxy called chproxy to buffer analytics events before forwarding to ClickHouse.

**Jordan**: That's a lot of services. Why the proxy?

**Alex**: Serverless functions terminate immediately after the request completes. You can't batch events in memory and flush them periodically—there's no "periodically" when your process might not exist in a second. ClickHouse doesn't perform well with high-volume individual inserts, so they needed something stateful to aggregate events.

**Jordan**: So they were already working around the stateless constraint.

**Alex**: That's the pattern that kept repeating. The fundamental issue was caching. Their Cloudflare cache was hitting 30 milliseconds at the 99th percentile.

**Jordan**: 30 milliseconds for a cache hit? That seems high.

**Alex**: It is when your target is sub-10 millisecond responses. And here's the insight from their co-founder Andreas Thomas: in serverless, every cache read requires a network request. There's no guaranteed persistent memory between function invocations. Your function spins up, makes a network call to the cache service, gets the data, responds, and might not even exist by the time the next request comes in.

**Jordan**: Versus a container that keeps running and holds data in local memory.

**Alex**: Exactly. Thomas put it simply: zero network requests are always faster than one network request. No amount of clever caching could match what a stateful server does by default—keeping hot data in memory.

**Jordan**: Okay, but isn't that the fundamental trade-off you accept with serverless? You give up state in exchange for automatic scaling and not managing infrastructure?

**Alex**: That's the promise. But the complexity reality didn't match. Unkey found they were using Durable Objects, Logstreams, Queues, Workflows, and multiple custom stateful services. Thomas said they spent more time evaluating and integrating Cloudflare-specific SaaS products than building features for customers.

**Jordan**: They were solving problems the architecture created rather than customer problems.

**Alex**: His exact words. And there's a vendor lock-in angle here. They had deep dependencies on six-plus Cloudflare-specific services. If they ever needed to move—for pricing, features, reliability, whatever—they'd have to rebuild everything.

**Jordan**: So what did they move to?

**Alex**: AWS Fargate for compute, Global Accelerator for global traffic distribution. Long-lived Go processes that hold data in memory and batch events naturally without external proxies.

**Jordan**: Why Fargate over EKS? Or Lambda?

**Alex**: They didn't need Kubernetes-level orchestration for their workload—Fargate gives you managed containers without the K8s overhead. And Lambda would have the same statelessness problem. The key insight is that container "cold starts" happen once per deployment or scale event. Serverless cold starts can happen on any traffic spike if your function instances recycled.

**Jordan**: For an always-hot service like API authentication, you want warm pools, not cold starts on demand.

**Alex**: Right. And Global Accelerator gives them the geographic distribution they had with edge serverless, just with traffic routing to regions rather than edge compute.

**Jordan**: What were the results?

**Alex**: Six-fold performance improvement. And here's an unexpected benefit—the container architecture made self-hosting trivial. Customers can now deploy Unkey with a single Docker command.

**Jordan**: That opens enterprise customers who couldn't use multi-tenant SaaS for compliance reasons.

**Alex**: Exactly. The architecture decision had product implications they didn't plan for. Self-hosting wasn't the goal, but containers made it almost free to offer.

**Jordan**: Before everyone listening runs back to containers for everything—this is a specific situation, right?

**Alex**: Very specific. Thomas himself said if you're a small startup, medium business, or even large business, you probably don't need to worry about this. Most services aren't in the critical path of thousands of other applications.

**Jordan**: What's the decision framework?

**Alex**: I'd look at five questions. First, where are you in the request path—are you calling APIs or being called AS the API? Second, what's your p99 latency target—if you need sub-10 milliseconds, you're in different territory. Third, how hot is your data—frequently accessed data wants to live in memory. Fourth, what's your complexity budget—count how many vendor-specific services you're using. And fifth, can you self-host if needed—containers make that trivial, serverless makes it nearly impossible.

**Jordan**: How would you even measure this before committing to a migration?

**Alex**: Profile your cache hit latency versus your target. Count external service calls per request. Map your vendor lock-in dependencies. And if you're seriously considering it, prototype the hot path in containers and compare p99 latency head-to-head.

**Jordan**: There's an interesting parallel to the z-pages discussion. Kubernetes is adding structured debugging endpoints at the same time teams are debating compute models.

**Alex**: The industry is maturing in both directions. Better observability for understanding what's running, and clearer frameworks for deciding how to run it.

**Jordan**: What's the takeaway for someone deciding between serverless and containers today?

**Alex**: It's not serverless versus containers as a religious debate. It's understanding when your workload crosses the line from using infrastructure to being infrastructure. Event-driven, bursty traffic? Serverless is great. Background jobs with scale-to-zero? Serverless. But latency-critical hot paths with consistent load and stateful caching needs? That's where containers win.

**Jordan**: If this breakdown helped you think through your compute model decisions, subscribing helps us know to make more content like this.

**Alex**: The question isn't serverless versus containers. It's knowing when your service crosses the line from calling infrastructure to being infrastructure. And when every millisecond matters—zero network requests will always be faster than one.
