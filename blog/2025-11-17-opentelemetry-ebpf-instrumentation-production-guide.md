---
slug: 2025-11-17-opentelemetry-ebpf-instrumentation-production-guide
title: "OpenTelemetry eBPF Instrumentation: Zero-Code Observability Under 2% Overhead (Production Guide 2025)"
authors: [vibesre]
tags: [opentelemetry, ebpf, observability, auto-instrumentation, kubernetes, platform-engineering]
date: 2025-11-17
description: "Production guide to OpenTelemetry eBPF Instrumentation (OBI): deploy zero-code observability with under 2% CPU overhead. Covers Kubernetes setup, SDK vs eBPF decision framework, and limitations to know."
keywords: [opentelemetry ebpf instrumentation, zero-code observability, ebpf auto-instrumentation, obi opentelemetry, grafana beyla, kubernetes auto-instrumentation, opentelemetry operator, ebpf overhead, instrument without code changes, opentelemetry production guide]
image: /img/blog/2025-11-opentelemetry-ebpf-instrumentation.jpg
---

48.5% of organizations are already using OpenTelemetry. Another 25.3% want to implement it but are stuck—blocked by the biggest adoption barrier: instrumenting existing applications requires code changes, rebuilds, and coordination across every team. In November 2025, OpenTelemetry released an answer: eBPF Instrumentation (OBI), which instruments every application in your cluster—Go, Java, Python, Node.js, Ruby—without touching a single line of code. Here's how to deploy it in production, what it can and can't do, and when you still need SDK instrumentation.

> 🎙️ **Listen to the podcast episode**: [OpenTelemetry eBPF Instrumentation: Zero-Code Observability Under 2% Overhead](/podcasts/00028-opentelemetry-ebpf-instrumentation) - Jordan and Alex investigate how eBPF delivers complete observability without code changes and the TLS encryption catch nobody talks about.

<!--truncate-->

## Quick Answer (TL;DR)

**Problem**: OpenTelemetry adoption stalls because instrumenting applications requires code changes across multiple languages and teams.

**Solution**: OpenTelemetry eBPF Instrumentation (OBI) operates at the Linux kernel level, auto-instrumenting all applications without code changes, restarts, or SDK dependencies.

**Key Statistics**:
- Less than 2% CPU overhead typical, compared to 10-50% for traditional APM agents
- 10 protocols supported automatically: HTTP, gRPC, SQL, Redis, Kafka, MongoDB, GraphQL, Elasticsearch, AWS S3
- 100,000+ monthly Docker pulls for Grafana Beyla before OpenTelemetry donation
- Linux kernel 4.4+ required, kernel 5.x recommended for full feature support
- First alpha release: November 2025

**Best For**: Broad baseline observability across all services, legacy applications you can't modify, polyglot environments with 5+ languages.

**When NOT to Use OBI Alone**: You need business-specific metrics like user IDs or transaction types, custom trace attributes are required, you're running non-Linux environments, or you need real-time security blocking.

## Key Statistics (2025 Data)

| Metric | Value | Source |
|--------|-------|--------|
| OpenTelemetry adoption | 48.5% using, 25.3% planning | [EMA Survey 2025](https://www.apica.io/blog/opentelemetry-the-foundation-of-modern-observability-strategy/) |
| ROI from OpenTelemetry | 46.4% report >20% ROI | [EMA Survey 2025](https://www.apica.io/blog/opentelemetry-the-foundation-of-modern-observability-strategy/) |
| MTTR improvement | 95% report 10%+ improvement | [EMA Survey 2025](https://www.apica.io/blog/opentelemetry-the-foundation-of-modern-observability-strategy/) |
| eBPF CPU overhead | Under 2% typical, under 5% maximum | [Pixie benchmarks](https://logz.io/blog/ebpf-auto-instrumentation-pixie-kubernetes-observability/) |
| Beyla Docker pulls | 100,000+ monthly | [Grafana Labs](https://grafana.com/blog/2025/05/07/opentelemetry-ebpf-instrumentation-beyla-donation/) |
| Community contributors | 10:1 ratio vs Grafana employees | [Grafana Labs](https://grafana.com/blog/2025/05/07/opentelemetry-ebpf-instrumentation-beyla-donation/) |
| eBPF compatibility issues | 83% of programs affected | [ACM Research 2025](https://dl.acm.org/doi/abs/10.1145/3689031.3717497) |
| Unused observability data | 70% | [Grafana Survey 2025](https://grafana.com/blog/2025/03/25/observability-survey-takeaways/) |
| Developer productivity gain | 60%+ | [EMA Survey](https://www.apica.io/blog/opentelemetry-the-foundation-of-modern-observability-strategy/) |
| Test performance after donation | 10x faster | [OpenTelemetry Blog](https://opentelemetry.io/blog/2025/obi-announcing-first-release/) |

## The Observability Instrumentation Gap

The numbers tell the story: nearly half of organizations use OpenTelemetry, and a quarter more want to implement it. But wanting and doing are different things. The primary blocker, according to Grafana's 2025 Observability Survey, is "adoption time and effort."

Here's what that actually means. Picture a typical microservices architecture: 50 services across 5 languages—Go, Java, Python, Node.js, and .NET. Each language needs its own SDK integration, context propagation setup, and exporter configuration. That's 10+ teams coordinating deployment schedules, code reviews, and testing cycles. Timeline? Three to six months, minimum. And that's if nothing goes wrong.

The result is predictable: partial observability. Teams instrument their most critical services first, maybe 40% coverage, and the rest becomes permanent technical debt. You have traces for your API gateway but not the internal services it calls. You see latency for your order service but can't trace why the payment service is slow.

### Why Traditional Auto-Instrumentation Falls Short

Language-specific agents were supposed to solve this. Java agents, .NET profilers, Python monkey-patching—these approaches promised automatic instrumentation without code changes.

They delivered, partially. You still need deployment changes. You still need to restart applications. You still need configuration for each agent. And the overhead? Traditional APM agents add 10-50% CPU overhead depending on configuration, according to industry benchmarks. That's fine for some workloads, unacceptable for others.

Worse, compiled languages like Go had no solution at all. You couldn't monkey-patch a binary. You couldn't inject bytecode. Go developers had to manually instrument everything—until eBPF.

### The Kernel-Level Breakthrough

eBPF changed the equation entirely. Instead of instrumenting at the library level—hooking into net/http or Express or Spring—eBPF instruments at the protocol level inside the Linux kernel itself.

When your Go application makes an HTTP request, that request eventually becomes syscalls: socket creation, data transmission, response reading. eBPF attaches probes to those kernel functions. It doesn't care whether your application is written in Go, Java, Python, or Rust. It doesn't care which HTTP library you're using. It sees the protocol.

One deployment instruments everything.

> **💡 Key Takeaway**
>
> OpenTelemetry eBPF Instrumentation captures metrics and traces at the kernel level, not the library level. One deployment instruments all applications regardless of programming language—Go, Java, Python, Node.js, Ruby, and .NET all work automatically without code changes or restarts.

## How OBI Works

Understanding how OBI differs from traditional instrumentation explains why it can deliver under 2% overhead while instrumenting every protocol your applications use.

### Protocol-Level vs Library-Level Instrumentation

Traditional auto-instrumentation hooks into specific libraries. The Java agent knows how to instrument Spring's RestTemplate, OkHttp, Apache HttpClient. The Node.js agent knows Express, Fastify, Axios. For each language and each library, there's specific instrumentation code.

This creates gaps. What happens when you use a library that isn't instrumented? What happens when a library updates and breaks the instrumentation? You get blind spots.

OBI takes a different approach. Instead of instrumenting libraries, it instruments protocols. HTTP is HTTP regardless of which library generates it. When data moves between user space and kernel space—socket operations, network I/O—OBI's eBPF probes capture it.

The OpenTelemetry blog explains it clearly: "Since OBI instruments at the protocol level, you can essentially instrument all applications (all programming languages, all libraries) with zero effort."

This protocol-level approach has a second advantage: consistency. Every service gets the same instrumentation quality. Your legacy Java monolith and your new Go microservices produce comparable telemetry.

### Why under 2% Overhead Is Possible

The performance difference between eBPF and traditional agents comes down to where the code runs.

Traditional APM agents run inside your application process. They hook into library calls, which means they execute in user space every time your code makes an instrumented call. Each call involves: checking if tracing is enabled, creating span objects, propagating context, buffering data for export. That adds up.

eBPF runs in kernel space. When your application makes a syscall, the eBPF program executes as part of the kernel's handling of that syscall. There's no user-space context switch for instrumentation. The data capture is JIT-compiled and optimized by the kernel's eBPF verifier.

The benchmarks reflect this architectural difference. Pixie's measurements show eBPF probes typically consume less than 2% CPU overhead, with a maximum around 5%. Traditional APM agents, depending on the sampling rate and enabled features, range from 10% to 50%.

As New Relic's documentation notes: "eBPF programs run in the kernel space, minimizing the performance impact on applications."

> **💡 Key Takeaway**
>
> OBI adds less than 2% CPU overhead in typical deployments because eBPF executes in kernel space during normal syscall handling. Traditional APM agents add 10-50% overhead because they run in user space and intercept every library call. The architectural difference is 5-25x less overhead.

### What OBI Captures Automatically

Without any configuration, OBI captures:

**RED Metrics** (per endpoint):
- Request rate
- Error rate (by status code)
- Duration (latency histograms)

**Distributed Traces**:
- Automatic trace context propagation across services
- Service-to-service call graphs
- Span creation for each protocol call

**Supported Protocols** (10 total):
- HTTP/HTTPS and HTTP/2
- gRPC
- SQL (PostgreSQL, MySQL)
- Redis
- MongoDB
- Kafka
- GraphQL
- Elasticsearch/OpenSearch
- AWS S3

Protocol detection is automatic. OBI analyzes the traffic patterns and identifies the protocol without configuration. Your application doesn't need to declare what protocols it uses.

> **💡 Key Takeaway**
>
> OBI automatically captures RED metrics (request rate, error rate, duration) and distributed traces for 10 protocols including HTTP, gRPC, SQL, Redis, Kafka, and MongoDB. No configuration required—protocol detection happens automatically by analyzing traffic patterns.

## Production Deployment Guide

Deploying OBI requires understanding the prerequisites, choosing the right deployment method, and knowing what configuration options matter.

### Prerequisites Checklist

**Kernel Requirements**

OBI needs Linux kernel 4.4 at minimum. Kernel 5.x is recommended for full feature support. Check your version:

```bash
uname -r
```

Different kernel versions have different eBPF capabilities. Older kernels may not support all the probes OBI needs. If you're running managed Kubernetes (EKS, GKE, AKS), you typically have recent kernels, but verify for your specific node images.

**Permission Requirements**

eBPF needs kernel access to attach probes. That requires either CAP_BPF capability or root privileges. In Kubernetes, this means privileged security context.

Some organizations prohibit privileged containers by policy. If that's your situation, you'll need to work with your security team on exceptions for the OBI workloads, potentially on dedicated node pools.

**Deployment Options**

Three ways to deploy OBI:

1. **DaemonSet** (recommended for cluster-wide instrumentation): One OBI pod per node, instruments all pods on that node
2. **Sidecar** (per-pod): OpenTelemetry Operator injects OBI container into specific pods
3. **Standalone** (single host): Direct installation for non-Kubernetes environments

### Kubernetes DaemonSet Deployment

For cluster-wide instrumentation, DaemonSet is the simplest approach. One deployment, full coverage.

**Step 1: Deploy OBI DaemonSet**

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: obi
  namespace: observability
spec:
  selector:
    matchLabels:
      app: obi
  template:
    metadata:
      labels:
        app: obi
    spec:
      hostPID: true
      hostNetwork: true
      containers:
      - name: obi
        image: ghcr.io/open-telemetry/opentelemetry-ebpf-instrumentation:latest
        securityContext:
          privileged: true
          runAsUser: 0
        env:
        - name: OTEL_EXPORTER_OTLP_ENDPOINT
          value: "http://otel-collector.observability:4317"
        - name: OTEL_SERVICE_NAME
          value: "obi"
        volumeMounts:
        - name: sys
          mountPath: /sys
          readOnly: true
      volumes:
      - name: sys
        hostPath:
          path: /sys
```

Note the key settings: `hostPID: true` allows OBI to see processes on the node, `privileged: true` enables kernel probe attachment, and the `/sys` mount provides access to kernel interfaces.

**Step 2: Configure OpenTelemetry Collector**

Your Collector needs to receive OBI's telemetry:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

processors:
  batch:
    timeout: 10s

exporters:
  # Your backend: Jaeger, Grafana Tempo, Datadog, etc.
  otlp:
    endpoint: "tempo.observability:4317"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp]
```

**Step 3: Verify Instrumentation**

Check OBI logs for discovered services:

```bash
kubectl logs -n observability -l app=obi --tail=100
```

Look for messages about discovered processes and attached probes. Then verify in your observability backend that traces are flowing and RED metrics are populating.

### OpenTelemetry Operator Deployment (Sidecar)

For Go applications specifically, or when you want per-pod control, use the OpenTelemetry Operator.

**Step 1: Install the Operator**

```bash
kubectl apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml
```

**Step 2: Create Instrumentation Resource**

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: obi-instrumentation
  namespace: your-namespace
spec:
  exporter:
    endpoint: http://otel-collector.observability:4317
  propagators:
    - tracecontext
    - baggage
  go:
    image: ghcr.io/open-telemetry/opentelemetry-go-instrumentation/autoinstrumentation-go:latest
```

**Step 3: Annotate Pods**

```yaml
metadata:
  annotations:
    instrumentation.opentelemetry.io/inject-go: "true"
```

The Operator injects an eBPF sidecar that instruments the Go application. The sidecar requires privileged context and runs as root.

> **💡 Key Takeaway**
>
> Deploy OBI as a Kubernetes DaemonSet for cluster-wide instrumentation with a single deployment—one OBI pod per node instruments all workloads. For Go applications or per-pod control, use the OpenTelemetry Operator to inject sidecars. Both methods require privileged security context.

### Essential Configuration

**Environment Variables**

The most important configuration options:

- `OTEL_EXPORTER_OTLP_ENDPOINT`: Where to send telemetry (required)
- `OTEL_SERVICE_NAME`: Override auto-detected service names
- `BEYLA_OPEN_PORT`: Filter to specific ports (e.g., "8080,443")
- `BEYLA_EXECUTABLE_NAME`: Filter to specific processes

**Performance Tuning**

For high-throughput environments:

- `BEYLA_BPF_BATCH_SIZE`: Events to batch before sending (default 100)
- `BEYLA_TRACE_PRINTER`: Enable for debugging (development only—adds overhead)

### Decision Framework: OBI vs SDK Instrumentation

Not every service needs the same instrumentation approach. Here's when to use what:

**Use OBI Alone When**:
- You need broad baseline observability quickly
- You're instrumenting legacy or third-party applications you can't modify
- You have a polyglot environment with 5+ languages
- Your team lacks SDK expertise across all your languages
- The under 2% overhead matters for performance-critical services

**Add SDK Instrumentation When**:
- You need custom attributes (user ID, tenant ID, transaction type)
- Business metrics are required (orders processed, revenue per transaction)
- You need deep framework instrumentation (Spring bean timings, Django middleware details)
- Complex sampling rules differ by service

**The Hybrid Approach (Recommended)**

Most production environments benefit from both:

1. Deploy OBI cluster-wide for baseline observability (zero effort, full coverage)
2. Add SDK instrumentation for top 10-20% of critical services (custom telemetry where it matters)
3. Result: 80% coverage instantly, 100% with targeted SDK work

This approach acknowledges that not every service needs custom attributes. Your database connection pool doesn't need user IDs in spans. But your checkout service probably does.

> **💡 Key Takeaway**
>
> Use OBI for baseline observability across all services (zero code changes required), then add SDK instrumentation only for critical services that need custom attributes or business metrics. This hybrid approach achieves 80% coverage instantly and completes the remaining 20% with targeted SDK work.

## Comparison: OBI vs SDK vs Traditional APM

| Capability | OBI | SDK Instrumentation | Traditional APM |
|------------|-----|---------------------|-----------------|
| Code changes required | None | Yes | Varies by agent |
| CPU overhead | under 2% typical | 5-15% | 10-50% |
| Custom attributes | No | Yes | Yes |
| Languages supported | All (kernel-level) | Per-language SDK | Per-language agent |
| Setup time | Minutes | Days to weeks | Hours to days |
| Trace context propagation | Automatic | Manual setup | Automatic |
| Business metrics | No | Yes | Yes |
| Deployment method | DaemonSet/sidecar | In-app dependency | Agent installation |

## Limitations and Gotchas

OBI isn't magic. Understanding its limitations prevents surprises in production.

### No Application-Layer Context

This is the most significant limitation. OBI operates at the kernel level, which means it can't see inside your application's memory.

**What's missing**:
- User IDs, session IDs, tenant identifiers
- Business transaction types (order, refund, subscription)
- Custom attributes and events you'd add with SDK
- Application-specific error details beyond HTTP status codes

**Why**: eBPF probes attach to kernel functions. They see syscalls and network data. They don't have access to application-level variables or business logic.

**Workaround**: Add SDK instrumentation for services where this context matters. OBI gives you the baseline; SDK adds the business semantics.

### Kernel Compatibility Issues

Research from ACM analyzing 25 kernel images across 8 years found that 83% of real-world eBPF programs are impacted by dependency mismatches. Different kernel versions have different eBPF features, and different Linux distributions configure kernels differently.

**Specific issues**:
- Kernel below 4.4: OBI won't run
- Kernel 4.x: Limited eBPF features, some probes may fail
- Kernel 5.x: Full support recommended

**Mitigation**: Test OBI on your exact production kernel version. If you use managed Kubernetes, verify the node image kernel version. Don't assume that staging (kernel 5.15) and production (kernel 4.19) will behave identically.

### Privileged Access Required

eBPF attaches probes to kernel functions. That requires elevated privileges—either CAP_BPF capability or root. In Kubernetes, this translates to `privileged: true` in the security context.

**Security implications**:
- Privileged containers can access host resources
- Some organizations prohibit them by policy
- Compliance frameworks may require justification

**Mitigation strategies**:
- Dedicate node pools for observability workloads
- Document the business case for your security team
- Use Pod Security Policies or OPA Gatekeeper to allow specific workloads
- Consider the alternative: running without observability is also a security risk

### Linux Only

eBPF is a Linux kernel technology. It doesn't exist on Windows or macOS.

**No support for**:
- Windows containers
- macOS (even in development)
- FreeBSD

If you have Windows workloads, you'll need traditional instrumentation for those. OBI handles the Linux side.

### Debugging Complexity

When something goes wrong with OBI, debugging is harder than with traditional agents.

**Challenges**:
- eBPF verifier errors are cryptic
- Limited debugging tools for kernel-space code
- Probe attachment failures may be silent

**Mitigation**: Use OBI as a packaged tool (don't write custom eBPF), check logs for probe attachment messages, and test thoroughly in staging before production rollout.

> **💡 Key Takeaway**
>
> OBI has real limitations to understand before production deployment: no custom attributes (kernel-level instrumentation can't see application memory), kernel compatibility issues affecting 83% of eBPF programs, privileged container access required, and Linux-only support. Test on your exact production kernel version and plan SDK instrumentation for services needing business context.

### Common Mistakes to Avoid

1. **Expecting custom attributes**: OBI captures protocol data, not application data. If you need user IDs in traces, use SDK.

2. **Skipping kernel version verification**: OBI will fail on old kernels, sometimes silently. Verify before deploying.

3. **Forgetting privileged security context**: Pods won't start without proper permissions. Plan for security team conversations.

4. **Not testing at scale**: Overhead increases with request volume. Test with production-like traffic.

5. **Replacing all SDK instrumentation**: OBI provides baseline observability. Keep SDK for services needing custom telemetry.

## Getting Started: 4-Week Rollout Plan

### Week 1: Preparation

- [ ] Verify kernel version on all nodes (`uname -r` should be ≥4.4, prefer 5.x)
- [ ] Check security policies for privileged container allowances
- [ ] Identify your OpenTelemetry Collector endpoint
- [ ] Choose deployment method (DaemonSet for most cases)
- [ ] Select initial services to instrument (start with non-critical)
- [ ] Document current observability coverage for comparison

### Week 2: Staging Deployment

- [ ] Deploy OBI to staging cluster
- [ ] Verify traces appearing in observability backend
- [ ] Check RED metrics per service
- [ ] Measure CPU overhead on OBI pods
- [ ] Test service-to-service trace propagation
- [ ] Identify any kernel compatibility issues

### Week 3: Production Rollout

- [ ] Deploy to production (single namespace first)
- [ ] Monitor for performance impact on application pods
- [ ] Validate trace completeness compared to staging
- [ ] Expand to additional namespaces incrementally
- [ ] Document which services need SDK additions

### Week 4: Optimization

- [ ] Identify services requiring custom attributes
- [ ] Add SDK instrumentation for top 10% critical services
- [ ] Configure sampling rules in Collector for cost management
- [ ] Set up alerts on OBI pod health and resource usage
- [ ] Update runbooks for new observability stack
- [ ] Train team on querying OBI-generated telemetry

### Red Flags During Rollout

Watch for these signals that something needs attention:

- **OBI pods in CrashLoopBackOff**: Usually kernel compatibility. Check logs for specific errors.
- **Missing traces for specific languages**: Verify the language is supported and probes are attaching.
- **High CPU on OBI pods**: Reduce batch size, check request volume, verify configuration.
- **Incomplete trace context**: Ensure Collector is receiving and properly processing spans.

> **💡 Key Takeaway**
>
> Roll out OBI incrementally: staging first, then one production namespace, then expand. Verify kernel compatibility, privileged access, and trace completeness at each stage before proceeding. Plan for SDK additions—OBI provides baseline observability, not complete custom telemetry.

## Practical Actions This Week

### For Individual Engineers

**Monday**: Check your Kubernetes node kernel versions. Run `kubectl get nodes -o wide` and note the kernel version column. If any nodes are below 4.4, flag it.

**Tuesday**: List the languages in your service mesh. OBI instruments all of them, but you need to know what SDK work might be needed later.

**Wednesday**: Identify one non-critical service for initial OBI testing. Something with HTTP traffic, not in the critical path.

### For Platform Teams

**This Week**:
1. Review security policies for privileged containers
2. Verify OpenTelemetry Collector is deployed and healthy
3. Choose between DaemonSet and Operator deployment
4. Create staging deployment plan

**Next Month**:
1. Complete staging rollout and validation
2. Document performance baselines
3. Begin production rollout by namespace
4. Establish hybrid strategy for SDK additions

### For Leadership

**Business Case**: OBI reduces observability instrumentation time from months to days. Instead of coordinating SDK integration across 10+ teams for 50 services, deploy once and instrument everything.

**Ask**: Approve privileged container security exception for observability namespace. The risk of running without observability (blind to production issues) exceeds the risk of privileged containers in a controlled namespace.

**Timeline**:
- Week 1-2: Staging validation
- Week 3-4: Production rollout
- Ongoing: SDK additions for critical services

**Success Metric**: Time to full observability coverage. Before OBI: 3-6 months for partial coverage. With OBI: 4 weeks for baseline coverage, SDK additions as needed.

## 📚 Learning Resources

### Official Documentation
- [OpenTelemetry OBI Documentation](https://opentelemetry.io/docs/zero-code/obi/) - Setup guides, configuration reference, Kubernetes deployment manifests
- [OpenTelemetry Zero-Code Overview](https://opentelemetry.io/docs/zero-code/) - All zero-code instrumentation approaches by language
- [OBI GitHub Repository](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation) - Source code, issues, release notes

### Grafana Resources
- [Grafana Beyla Documentation](https://grafana.com/docs/beyla/latest/) - Comprehensive guide for Grafana's OBI distribution
- [Grafana OpenTelemetry Report](https://grafana.com/opentelemetry-report/) - Adoption patterns, challenges, and industry statistics

### Key Announcements
- [OBI First Release Announcement](https://opentelemetry.io/blog/2025/obi-announcing-first-release/) (November 2025) - Capabilities, supported protocols, getting started
- [Grafana Beyla Donation](https://grafana.com/blog/2025/05/07/opentelemetry-ebpf-instrumentation-beyla-donation/) (May 2025) - Background on community transition
- [Go Auto-Instrumentation Beta](https://opentelemetry.io/blog/2025/go-auto-instrumentation-beta/) (March 2025) - Go-specific eBPF features

### Technical Deep Dives
- [Trail of Bits: eBPF Pitfalls](https://blog.trailofbits.com/2023/09/25/pitfalls-of-relying-on-ebpf-for-security-monitoring-and-some-solutions/) - Security considerations and limitations
- [Last9: Zero-Code Instrumentation](https://last9.io/blog/zero-code-instrumentation/) - Practical implementation guide

### Community
- **CNCF Slack**: #otel-ebpf-instrumentation channel for async discussions
- **Weekly SIG Calls**: Thursdays at 13:00 UTC for real-time collaboration

## Related Content

**Platform Engineering Playbook Resources**:
- [eBPF in Kubernetes: Kernel-Level Superpowers Without the Risk](/podcasts/00022-ebpf-kubernetes) - Deep dive on how eBPF works and production safety
- [Observability Tools Showdown](/podcasts/00027-observability-tools-showdown) - Comparing observability platforms and approaches
- [OpenTelemetry Technical Page](/technical/opentelemetry) - Learning resources and ecosystem overview

## Conclusion

OpenTelemetry eBPF Instrumentation changes the economics of observability adoption. Instead of months of SDK integration work across multiple teams and languages, you deploy once and instrument everything. The under 2% overhead makes it practical for performance-sensitive workloads. The protocol-level approach makes it language-agnostic.

But OBI isn't a complete replacement for SDK instrumentation. It provides baseline observability—RED metrics and distributed traces for the protocols your applications use. For custom attributes, business metrics, and deep framework instrumentation, you still need targeted SDK work.

The practical path forward: deploy OBI for cluster-wide baseline coverage, then add SDK instrumentation for the 10-20% of services that need custom telemetry. You get 80% coverage immediately and 100% with targeted effort.

The first alpha release shipped in November 2025. The ecosystem is moving fast, with Grafana Labs, Splunk, Coralogix, and Odigos all contributing. Now is the time to evaluate OBI for your environment—before your observability debt compounds further.

---

**Have questions about deploying OBI?** Open an issue on our [GitHub repository](https://github.com/platform-engineering-playbook/platform-engineering-playbook) or join the discussion.
