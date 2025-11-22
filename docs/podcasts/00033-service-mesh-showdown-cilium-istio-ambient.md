---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #033: Service Mesh Showdown"
slug: 00033-service-mesh-showdown-cilium-istio-ambient
---

# Service Mesh Showdown: Why User-Space Beat eBPF

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 20 minutes
**Speakers:** Jordan and Alex  
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/service-mesh-showdown-cilium-istio-ambient-comparison)**: Comprehensive analysis of Istio Ambient vs Cilium service mesh architectures with academic benchmarks, 50,000-pod stability testing, and decision frameworks for choosing the right approach based on cluster size and traffic patterns.

<iframe width="560" height="315" src="https://www.youtube.com/embed/7FNEMtf5NsE" title="Service Mesh Showdown: Why User-Space Beat eBPF" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

---

**Jordan**: Today we're diving into a service mesh mystery that's challenging everything we thought we knew about performance. Istio Ambient reached GA in November twenty twenty-four with eight percent mTLS overhead compared to sidecar's hundred sixty-six percent. Impressive, right? But Cilium promised even better with kernel-level eBPF—theoretically, processing packets directly in the kernel should beat user-space proxies every time.



**Alex**: And then the October twenty twenty-five academic benchmarks dropped.



**Jordan**: Exactly. Cilium showed ninety-nine percent overhead. User-space beat the kernel. What happened?



**Alex**: So we've got this counterintuitive result that demands explanation. And the answer reveals something fundamental about architecture design—that where you draw boundaries matters more than raw execution speed.



**Jordan**: Let's set the stakes here. Platform teams managing thousands of pods are paying real money for sidecars. Two hundred fifty megabytes per pod times a thousand pods is two hundred fifty gigabytes. At AWS memory pricing, that's about a hundred twenty-seven thousand dollars a year just for the mesh infrastructure.



**Alex**: Just for the proxies, before you even count the latency penalty or engineering time managing them.



**Jordan**: Right. So the sidecarless revolution promised to solve this. Two competing visions emerged—Cilium saying "move everything to the kernel with eBPF" and Istio Ambient saying "use purpose-built user-space proxies." Radically different architectures.



**Alex**: And choosing wrong means either you're wasting money on inefficient infrastructure, or worse, your API server crashes when you scale to enterprise sizes. So this matters.



**Jordan**: Okay, let's start with the eBPF promise. What was Cilium trying to achieve?



**Alex**: The core idea is elegant. Traditional service meshes run Envoy proxies in user-space—every packet has to cross from the kernel into user-space for processing, then back to the kernel to continue its journey. Those context switches are expensive. Cilium said "what if we process packets entirely in the Linux kernel using eBPF programs?"



**Jordan**: So eBPF programs are like little sandboxed programs that run directly in kernel space.



**Alex**: Right. The Linux kernel has hooks at various points—when a packet arrives, when a connection is established, when data is sent. Cilium loads eBPF programs at these hooks to intercept traffic. For L four processing like TCP connections and routing, everything happens in the kernel. Encryption uses WireGuard, which is also kernel-based. The promise was maximum efficiency—no expensive transitions between kernel and user-space for basic traffic.



**Jordan**: And for L seven HTTP traffic?



**Alex**: That's where Cilium still needs Envoy. Because HTTP parsing, routing rules, retries—that's complex application-layer stuff. So Cilium deploys one shared Envoy proxy per node. When traffic needs L seven capabilities, the eBPF programs direct it to that shared Envoy running in user-space.



**Jordan**: So it's not pure kernel processing.



**Alex**: No, it can't be. Every service mesh has to handle HTTP eventually for observability, advanced routing, retry logic. The question is where that boundary sits.



**Jordan**: And Istio Ambient took a completely different approach.



**Alex**: Yes. Ambient uses ztunnel—z-tunnel, like zero-trust tunnel. It's a lightweight proxy that runs per-node in user-space. Not in the kernel. It handles L four traffic—TCP connections, mTLS encryption, identity-based authentication, basic network policies. Crucially, ztunnel doesn't parse HTTP at all. It just treats traffic as opaque TCP streams.



**Jordan**: So it's doing mTLS handshake and encryption without looking inside to see if it's HTTP.



**Alex**: Exactly. And when you need L seven capabilities—HTTP routing, traffic splitting, circuit breakers—you deploy optional waypoint proxies. These are full Envoy instances, but they're deployed per service account, not per pod. So if you have a thousand pods across fifty services, you might deploy fifty waypoint proxies instead of a thousand sidecars.



**Jordan**: Okay, so we've got Cilium with kernel eBPF plus shared Envoy per node, and Ambient with user-space ztunnel plus optional waypoint proxies per service. Now let's talk about the benchmarks. What did the academic study actually measure?



**Alex**: The ArXiv study from October twenty twenty-five was peer-reviewed research from multiple universities. They tested four implementations—Istio traditional sidecar, Istio Ambient, Cilium, and Linkerd—under production-realistic conditions using Fortio load generator at three thousand two hundred requests per second with two hundred millisecond backend delay simulating database calls.



**Jordan**: And the mTLS overhead results?



**Alex**: At p ninety-nine latency, Istio sidecar added a hundred sixty-six percent overhead. Linkerd added thirty-three percent. Istio Ambient added eight percent. And Cilium added ninety-nine percent.



**Jordan**: Wait, so Ambient—running in user-space—had eight percent overhead, while Cilium—running in the kernel—had ninety-nine percent. That's twelve times worse despite theoretically being faster.



**Alex**: Right. And if you look at CPU consumption, Cilium used point one two cores versus Ambient's point two three cores. So Cilium was using less CPU but delivering worse latency. The bottleneck wasn't raw processing power.



**Jordan**: So what's going on? Why does kernel-level processing underperform user-space here?



**Alex**: The answer is the L seven processing boundary. Remember, every service mesh has to handle HTTP eventually. For Cilium, here's what happens. A packet arrives, the eBPF program in the kernel processes it, encrypts it with WireGuard. Great, all in kernel space. But then, if you have any network policy that requires looking at HTTP headers, or you want retry logic, or you need observability metrics—that packet has to be copied from kernel memory into user-space memory so the shared Envoy proxy can parse the HTTP.



**Jordan**: So even though the initial processing is fast, you pay the cost of that kernel-to-user-space transition.



**Alex**: And then after Envoy processes it, the packet goes back to the kernel to continue its journey. So you're doing these expensive memory copies and context switches. The academic study found that when they disabled HTTP parsing entirely in Cilium's Envoy, throughput improved almost five times. The eBPF part was fast—it was the transitions to handle L seven that killed performance.



**Jordan**: And Ambient avoids this how?



**Alex**: Ambient's ztunnel is purpose-built for L four. It doesn't try to parse HTTP at all. When it sees a TCP connection, it does the mTLS handshake, encrypts the stream, and forwards it. Because it's not looking inside the HTTP, it can optimize that path aggressively—eight percent overhead means the encryption overhead is minimal. When you do need L seven processing, the traffic goes directly to a waypoint proxy that's already in user-space. No kernel transitions required.



**Jordan**: So Ambient accepted that L seven happens in user-space and designed around it, while Cilium tried to stay in the kernel as long as possible but got penalized whenever L seven was needed.



**Alex**: Right. And for most production workloads, you're going to need some L seven capabilities. Routing, observability, retries—these are table stakes. So Cilium's architecture hits the worst case more often.



**Jordan**: Okay, but that's just latency and CPU. Istio also published large-scale stability testing. What did that show?



**Alex**: This is where it gets really interesting. Istio set up an Azure Kubernetes Service cluster with a thousand nodes, eleven thousand CPU cores, fifty thousand pods running five hundred different microservices with a hundred replicas each.



**Jordan**: That's enormous.



**Alex**: Yeah, way beyond most production deployments, which is the point—stress test at the extremes. And they simulated production churn. Replicas scaling up and down every second, namespaces getting relabeled every minute, constant service discovery updates. Both Ambient and Cilium were tested under these conditions.



**Jordan**: And?



**Alex**: Throughput-wise, Ambient delivered twenty-one seventy-eight queries per core versus Cilium's eighteen fifteen. That's a twenty percent per-core efficiency advantage, which translates to fifty-six percent more total cluster throughput when you multiply across eleven thousand cores.



**Jordan**: So Ambient was faster at scale.



**Alex**: But the bigger discovery was stability. Cilium's distributed control plane architecture—where every node runs a Cilium agent that independently talks to the Kubernetes API server—caused the API server to crash under that aggressive churn.



**Jordan**: The API server crashed?



**Alex**: Yes. A thousand Cilium agents all independently querying for service updates, pod labels, namespace changes—the aggregated load became unbearable. The cluster became unresponsive. Istio's centralized control plane, where a single istiod manages all the ztunnels, handled the same workload without instability.



**Jordan**: So kernel efficiency doesn't matter if you can't stay online.



**Alex**: Exactly. And this reveals something important. Cilium's architecture makes sense at smaller scales. Under five hundred nodes, under five thousand pods, the distributed control plane isn't a problem. But if you're planning for enterprise scale, that centralized control plane design becomes critical.



**Jordan**: Okay, so we've got the mystery solved. Architecture boundaries matter more than execution location. Now the practical question—when should you use each?



**Alex**: Let's build a decision framework. Start with cluster size. If you're running a thousand to five thousand nodes and you need proven fifty-thousand-pod stability, Istio Ambient has the data. If you're under five hundred nodes, Cilium's API server issues are unlikely to surface.



**Jordan**: What about traffic patterns?



**Alex**: This is huge. If seventy percent or more of your inter-service traffic is L four—gRPC, database connections, message queues—and only thirty percent needs L seven routing, Ambient wins because you deploy ztunnel for L four and add waypoint proxies only for the services that need HTTP capabilities. But if your traffic is pure L three slash L four with no complex HTTP routing at all, Cilium can be more efficient because you're not paying for L seven infrastructure you don't use.



**Jordan**: Give me a concrete example.



**Alex**: Okay, e-commerce platform with two thousand microservices. Eighty percent of traffic is internal gRPC between backend services—inventory, pricing, recommendations. Twenty percent is user-facing REST APIs with sophisticated routing, retries, circuit breakers. With sidecars, you're deploying two thousand Envoy proxies, consuming five hundred gigabytes of memory, costing about two hundred thousand dollars a year.



**Jordan**: And with Ambient?



**Alex**: Deploy ztunnel on every node—say fifty nodes, that's fifty times twenty-six megabytes, about one point three gigs for the L four layer. Then deploy waypoint proxies for the four hundred services that need L seven—that's four hundred times a hundred megabytes, forty gigs. Total memory footprint is forty-one gigabytes instead of five hundred. You've saved a hundred eighty-six thousand dollars a year in infrastructure costs alone.



**Jordan**: That's a compelling business case. What about Cilium?



**Alex**: Cilium makes sense for smaller scale with pure L four requirements. Startup with a fifty-node cluster, backend services communicating via gRPC, no complex HTTP routing. If you're already using Cilium for your CNI—the container network interface—adding service mesh features is incremental. Cilium's ninety-five megabytes per node is the smallest footprint you can get. Fifty nodes times ninety-five megabytes is four point seven gigs total.



**Jordan**: Much cheaper than Ambient's forty-one gigs in that e-commerce example.



**Alex**: Right, but remember, the e-commerce platform has sophisticated L seven requirements. If the startup tries to scale to two thousand pods and adds HTTP routing, they'll start hitting the shared Envoy bottleneck—one proxy per node handling all L seven traffic from multiple pods. Ambient's per-service waypoints scale better at that point.



**Jordan**: And when should you just keep sidecars despite the cost?



**Alex**: Three scenarios. One, multi-cluster federation. If you're running services across multiple Kubernetes clusters in different regions or clouds, Ambient's multi-cluster support isn't mature yet. Sidecars are the proven option. Two, maximum isolation for compliance. PCI-DSS, HIPAA, FedRAMP—if your compliance framework requires per-workload security boundaries, sidecars give you a dedicated proxy per pod. Three, heavy L seven traffic per pod. If every single pod is generating significant HTTP traffic requiring per-pod routing and retries, sidecars scale naturally because the proxy scales with the pod count.



**Jordan**: So it's not that sidecars are obsolete.



**Alex**: Not at all. They're the most mature option—seven years in production, extensive tooling, multiple vendor support options. If you're in financial services with multi-region deployment and strict compliance, the two hundred thousand dollar sidecar cost might be justified by the maturity and isolation.



**Jordan**: Okay, so let's say a team decides Ambient makes sense. What does migration actually look like?



**Alex**: Here's the reality check everyone misses. The technical migration is trivial—you can swap Ambient for sidecars in minutes. Remove the sidecar injection label from a namespace, add the Ambient label, and Istio handles the transition. The organizational change is what takes ninety days.



**Jordan**: What does that involve?



**Alex**: You've got to update CI/CD pipelines for every project. GitHub Actions workflows, GitLab CI configs, Jenkins files—anywhere you reference Istio configuration. Documentation needs updating. Team training—developers need to understand the new model, how ztunnel works, when to deploy waypoints. And you need gradual rollout. Start with five to ten low-risk dev services, validate for two weeks, expand to production incrementally.



**Jordan**: So it's the same pattern we saw with the Fidelity OpenTofu migration—technically simple, organizationally complex.



**Alex**: Exactly. Fidelity migrated seventy percent of their fifty thousand state files in six months, and they said the technical side was trivial. It was the change management that mattered. Same here. Budget ninety days to hit thirty to fifty percent adoption if you're aggressive, longer if you want to be conservative.



**Jordan**: And what's the cost-benefit on that ninety-day migration effort?



**Alex**: If you're saving a hundred eighty-six thousand a year on infrastructure and you allocate one senior platform engineer for three months at, say, a hundred fifty thousand dollar annual salary, that's about thirty-seven thousand dollars in labor cost. Plus maybe ten thousand for vendor support from Solo dot i-o or Tetrate. You're still saving a hundred thirty-nine thousand net in year one, and the full hundred eighty-six thousand every year after. That's a pretty clear ROI.



**Jordan**: Okay, so let's bring this home. What's the key insight here for platform engineers evaluating service meshes in twenty twenty-five?



**Alex**: The counterintuitive lesson is that execution location—kernel versus user-space—matters less than architecture boundaries. Istio Ambient wins not because user-space is inherently faster, but because it's designed around the reality that L seven processing happens in user-space anyway. Cilium's kernel-level eBPF is brilliant for L four, but the architecture pays a penalty every time you need HTTP capabilities.



**Jordan**: And scale matters differently than people think.



**Alex**: Yes. Cilium's distributed control plane is a feature at small scale—resilience, no single point of failure. But at enterprise scale with aggressive churn, it becomes a liability. The API server can't handle a thousand independent agents. Istio's centralized control plane flips that—potential single point of failure at small scale, but proven stability at fifty thousand pods.



**Jordan**: So the decision framework is cluster size, traffic patterns L four versus L seven, and your scale ambitions.



**Alex**: Right. Under five hundred nodes with pure L four, Cilium wins on efficiency. Thousand to five thousand nodes with mixed L four and L seven, Ambient wins on cost and stability. Mission-critical multi-cluster with heavy compliance, sidecars win on maturity despite the cost. There's no universal answer—it depends on your specific constraints.



**Jordan**: And the migration timeline is ninety days of organizational change, not a weekend technical swap.



**Alex**: Correct. The technology is ready. Istio Ambient reached GA in November twenty twenty-four after twenty-six months of development involving Google, Microsoft, and Red Hat. Cilium's been stable for years. The challenge is coordinating team training, CI/CD updates, and gradual rollout across your organization.



**Jordan**: So platform teams need to do the math on their specific situation. Calculate your current sidecar memory cost, evaluate your traffic patterns, consider your scale trajectory, and decide whether the architecture fits your use case.



**Alex**: And recognize that this isn't a binary decision. You can run Ambient for cost-sensitive services, sidecars for mission-critical multi-cluster workloads, and Cilium for small-scale L four-only clusters. Mix and match based on requirements.



**Jordan**: The architecture you choose matters less than choosing deliberately based on your constraints. Which I guess is the meta-lesson here—don't assume kernel is always faster, don't assume user-space is always slower. Understand the boundaries, test at your scale, and make the decision that fits your reality.



**Alex**: And if you want the full technical breakdown, we've got a deep-dive blog post with all the benchmark data, cost calculations, and migration playbooks. Link in the show notes.



**Jordan**: The sidecarless revolution is here, but it's not about one architecture beating the other. It's about matching the architecture to the workload. That's the real engineering.
