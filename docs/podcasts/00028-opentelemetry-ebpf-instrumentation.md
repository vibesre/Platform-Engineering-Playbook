---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #028: OpenTelemetry eBPF Instrumentation"
slug: 00028-opentelemetry-ebpf-instrumentation
---

# OpenTelemetry eBPF Instrumentation: Zero-Code Observability Under 2% Overhead

## The Platform Engineering Playbook Podcast

import GitHubButtons from '@site/src/components/GitHubButtons';

<GitHubButtons />

**Duration:** 14 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/2025-11-17-opentelemetry-ebpf-instrumentation-production-guide)**: Production guide covering Kubernetes deployment, SDK vs eBPF decision framework, and TLS handling strategies.

---

**Jordan:** Today we're investigating something that sounds almost too good to be true. Complete observability coverage—every HTTP request, every database query, every gRPC call—without touching a single line of application code.

**Alex:** And here's the kicker: under two percent CPU overhead. When traditional APM agents can add significant overhead to your compute just to tell you what's happening.

**Jordan:** So either this is a massive breakthrough, or there's a catch nobody's talking about. Let's find out which.

**Alex:** The technology is eBPF-based instrumentation for OpenTelemetry. And to understand why this matters, we need to start with the problem it's solving.

**Jordan:** The instrumentation gap. In many enterprises, a significant portion of services have limited or no observability coverage.

**Alex:** Exactly. And it's not because teams don't want observability. It's because SDK instrumentation is genuinely painful. You're looking at importing libraries, wrapping function calls, propagating context across service boundaries. For a polyglot environment with fifty services across Go, Java, Python, Node—that's weeks of work.

**Jordan:** And that's assuming you even have access to the source code. What about third-party binaries? Legacy services nobody wants to touch?

**Alex:** Those become permanent blind spots. And every blind spot is a potential three AM incident where you're flying completely blind.

**Jordan:** So teams make a trade-off. They instrument the critical paths and accept gaps everywhere else.

**Alex:** Right, and then they compound the problem with APM agents that add significant CPU overhead. Now your high-performance services can't use them at all, so your fastest, most critical paths become your biggest blind spots.

**Jordan:** It's a genuinely impossible choice. Coverage or performance, pick one.

**Alex:** Which is exactly what makes eBPF instrumentation so interesting. It sidesteps this entire trade-off.

**Jordan:** Okay, so how does it actually work? Because "kernel-level instrumentation" sounds like magic hand-waving.

**Alex:** It's not magic, but it is genuinely clever. So eBPF—extended Berkeley Packet Filter—lets you run sandboxed programs inside the Linux kernel. These programs can attach to kernel functions like syscalls, network stack operations, filesystem calls.

**Jordan:** Wait, you're executing code in kernel space? How is that not a massive security risk?

**Alex:** Because every eBPF program goes through a verifier before it can run. The verifier is incredibly strict—it proves mathematically that your program will terminate, won't access invalid memory, won't crash the kernel. If verification fails, the program simply doesn't load.

**Jordan:** So the kernel itself is guaranteeing safety.

**Alex:** Exactly. And once verified, the program gets JIT-compiled to native machine code for performance. Then it attaches to specific kernel hooks and executes whenever those hooks fire.

**Jordan:** Give me a concrete example. My Go service makes an HTTP call—what actually happens?

**Alex:** Your Go service calls the standard library, which eventually makes a syscall to the kernel's network stack. At that point, an eBPF probe attached to the socket operations captures the packet metadata. It extracts HTTP information—method, path, headers, status code—from the raw bytes. Stores that in an eBPF map, which is a data structure shared between kernel and userspace. A collector running in userspace reads from those maps and converts everything into OpenTelemetry spans.

**Jordan:** So the eBPF program is just observing operations that are already happening. It's not adding new work.

**Alex:** That's the key insight. The kernel is already processing these syscalls, already handling these network packets. The eBPF probe adds nanoseconds of overhead to observe what's already happening. That's why you get under two percent CPU impact.

**Jordan:** Compared to APM agents that have to intercept at the application level, wrap every function call, maintain their own context propagation.

**Alex:** Right, traditional agents are doing a lot of work in userspace. eBPF just watches the kernel do work it was already doing.

**Jordan:** This sounds like it's been possible for years. Why is it suddenly relevant now?

**Alex:** Because of what happened in May twenty twenty-five. Grafana donated their Beyla project to the OpenTelemetry project. Beyla was already one of the most mature eBPF instrumentation tools, and now it's becoming the official OpenTelemetry eBPF instrumentation.

**Jordan:** So this went from "interesting experimental tool" to "core part of the OpenTelemetry ecosystem."

**Alex:** Exactly. You've got the weight of OpenTelemetry behind it now—the governance, the community, the integration with collectors and backends. This is no longer a side project.

**Jordan:** What does deployment actually look like?

**Alex:** DaemonSet on Kubernetes. You deploy one pod per node, it automatically discovers all processes on that node, and starts generating telemetry. Zero changes to your applications. Zero configuration per service.

**Jordan:** So you go from limited coverage to one hundred percent in what, an hour?

**Alex:** That's what teams are reporting. Deploy the DaemonSet, configure your collector endpoint, and suddenly you have spans for every service on every node. Services you forgot existed are now visible.

**Jordan:** Okay, I need to poke at this. What's the catch?

**Alex:** There are real limitations, and the biggest one is context. eBPF captures at the protocol level—HTTP, gRPC, SQL. It sees the wire format. It doesn't see your application's internal state.

**Jordan:** Meaning what specifically?

**Alex:** Meaning it can tell you: POST request to slash API slash orders, two hundred response, took forty-seven milliseconds. It cannot tell you: this was customer ID twelve thirty-four, using feature flag new-checkout, for order value five hundred dollars.

**Jordan:** So you get the technical telemetry but not the business context.

**Alex:** Exactly. Any attribute that exists only in your application's memory—user IDs, tenant identifiers, feature flags, business metrics—eBPF can't access them. It only sees what crosses the kernel boundary.

**Jordan:** Which means for business-critical paths where you need that context for debugging or analytics, you still need SDK instrumentation.

**Alex:** Right. eBPF isn't replacing SDKs. It's providing a universal baseline that SDKs enhance.

**Jordan:** What about encryption? If everything's TLS, doesn't eBPF just see encrypted bytes?

**Alex:** This is the other major limitation. TLS encryption happens before data hits the kernel network stack. So yes, eBPF sees encrypted packets it can't parse.

**Jordan:** So this "zero configuration" story breaks down for anything using HTTPS?

**Alex:** There are solutions, but they add complexity. The most common is uprobes on OpenSSL or BoringSSL—you hook the encryption libraries before they encrypt. But now you're dependent on specific library versions, and it's language-specific.

**Jordan:** So much for "any language, any framework."

**Alex:** For TLS, yeah. The other approach is service mesh integration. If you're running Istio or Cilium, they're already terminating TLS at the proxy layer. eBPF can observe the unencrypted traffic between proxy and application.

**Jordan:** Which means you need either library-specific hooks or a service mesh. The "zero configuration" story has asterisks.

**Alex:** Absolutely. TLS handling is the main complexity in production eBPF deployments. Teams need to plan for it.

**Jordan:** Let's talk about protocol support. You mentioned HTTP and gRPC—what else?

**Alex:** HTTP one point one, HTTP two, gRPC, Redis, and SQL including Postgres and MySQL. Those are the protocols with mature support today.

**Jordan:** What if I have a custom protocol? Some internal RPC format?

**Alex:** Then you need SDK instrumentation. eBPF parses protocols it knows—if it doesn't recognize the wire format, it can't extract meaningful telemetry.

**Jordan:** So you're covered for standard protocols, but anything custom is a gap.

**Alex:** Right. And that's actually fine for most teams. The standard protocols cover eighty to ninety percent of service communication. You fill gaps with targeted SDK work.

**Jordan:** Okay, so let's synthesize this. How should teams actually think about eBPF versus SDKs?

**Alex:** They're complementary layers, not competing approaches. eBPF gives you the baseline—universal coverage, zero-touch deployment, minimal overhead. SDKs give you depth—business context, custom spans, application-specific metrics.

**Jordan:** So you'd run both?

**Alex:** In production, almost always. eBPF for the foundation, SDK instrumentation for business-critical paths where you need that application context.

**Jordan:** Give me a decision framework. When do I go eBPF-first versus SDK-first?

**Alex:** eBPF-first makes sense when: you have a polyglot environment and can't standardize on one SDK, you need coverage fast and can't wait for instrumentation work, you have performance-critical services that can't tolerate agent overhead, or you have legacy and third-party binaries you can't modify.

**Jordan:** And when do I reach for SDKs?

**Alex:** When you need business context—user IDs, tenant info, feature flags. When you need custom spans for business logic that doesn't cross network boundaries. When you need application-specific metrics that only exist in your code.

**Jordan:** And realistically, most teams will need both.

**Alex:** Exactly. The question isn't which one, it's what ratio. Some teams are ninety percent eBPF with SDK only for their core revenue paths. Others are fifty-fifty. It depends on how much business context matters for your debugging and analytics.

**Jordan:** What does the maturity path look like?

**Alex:** Week one: deploy the OpenTelemetry eBPF Operator on a non-production cluster. Validate it's capturing the protocols you care about. Get comfortable with the deployment model.

**Jordan:** And then?

**Alex:** Week two: production deployment. You'll immediately have baseline coverage everywhere. Identify which services actually need business context—usually it's your top three to five revenue-generating paths.

**Jordan:** Then add SDK instrumentation just for those paths.

**Alex:** Right. You're not instrumenting everything with SDKs anymore. You're instrumenting strategically, only where the business context matters for debugging or analytics.

**Jordan:** So the total instrumentation work drops dramatically.

**Alex:** Instead of instrumenting fifty services with SDKs, you're instrumenting five. eBPF handles the other forty-five.

**Jordan:** What about the organizational impact? This changes how platform teams operate.

**Alex:** It shifts the work from "instrument everything" to "curate what matters." Platform teams become observability curators rather than instrumentation mechanics.

**Jordan:** And application teams?

**Alex:** They get observability for free. No SDK imports, no instrumentation work, no context propagation bugs. They can focus on shipping features. If they need business context for debugging, they add targeted SDK spans, but that's their choice, not a prerequisite for visibility.

**Jordan:** Let's bring this back to the original question. Is eBPF instrumentation too good to be true?

**Alex:** The core promise is real. Under two percent overhead, zero-code deployment, instant coverage—that all works. But it's not a complete replacement for SDK instrumentation.

**Jordan:** It's a foundation that makes SDK instrumentation optional rather than mandatory.

**Alex:** Exactly. You go from "we have to instrument everything" to "we can instrument what matters." That's a fundamental shift in how observability programs work.

**Jordan:** And the May twenty twenty-five donation to OpenTelemetry means this is now mainstream infrastructure, not experimental tooling.

**Alex:** Right. This is the observability stack consolidating. OpenTelemetry for the standard, eBPF for zero-touch collection, SDKs for business context. The pieces are coming together.

**Jordan:** Practical takeaway for listeners?

**Alex:** Start with eBPF for your baseline. Deploy the OpenTelemetry eBPF Operator, get instant visibility into everything. Then add SDK instrumentation only where you need business context. You'll go from limited coverage to one hundred percent in hours, then enhance critical paths over weeks instead of months.

**Jordan:** From "we can't instrument everything" to "zero-code coverage in minutes."

**Alex:** With the kernel doing the heavy lifting.
