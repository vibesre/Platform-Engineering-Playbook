# Episode Outline: OpenTelemetry eBPF Instrumentation

## Story Planning

**NARRATIVE STRUCTURE**: Mystery/Discovery
**CENTRAL TENSION**: Platform teams face an impossible choice: complete observability coverage requires months of SDK instrumentation work and 10-50% performance overhead, or accept blind spots that cause production incidents. eBPF promises to solve this—but is it real, or just hype?
**THROUGHLINE**: From "we can't instrument everything" to "zero-code coverage with kernel-level precision in minutes"
**EMOTIONAL ARC**:
- Recognition: "I've fought this instrumentation battle"
- Surprise: "Wait, it's happening at the KERNEL level?"
- Empowerment: "I know exactly when to use this vs SDKs"

## Act Structure

### ACT 1: SETUP (2-3 min)

- **Hook**: "What if I told you there's a way to get complete observability coverage—every HTTP request, every database query, every gRPC call—without touching a single line of application code, and with under 2% CPU overhead?"
- **Stakes**: Platform teams spend weeks instrumenting services. Average enterprise has 30-40% of services with zero observability. Each blind spot is a potential 3 AM incident. Traditional APM agents add 10-50% overhead, making them impractical for high-performance services.
- **Promise**: We'll investigate how eBPF instrumentation actually works at the kernel level, when it beats traditional approaches, and the critical limitations nobody talks about.

**Key Points**:
- The instrumentation paradox: More services = more blind spots (average 30-40% uninstrumented)
- Traditional APM agent overhead: 10-50% CPU penalty makes adoption impractical for performance-critical services
- OpenTelemetry's promise: Vendor-neutral observability—but SDK instrumentation remains the bottleneck

### ACT 2: EXPLORATION (5-7 min)

#### Discovery 1: The Kernel Shortcut
- **Insight**: eBPF programs attach to kernel functions (syscalls, network stack, filesystem) and observe ALL processes without modification
- **How it works**: When your Go service makes HTTP call → syscall → kernel network stack → eBPF probe captures packet metadata → extracts HTTP/gRPC/SQL info → sends to userspace → becomes OTel spans
- **Evidence**: Under 2% CPU overhead because kernel operations are already happening—eBPF just observes them
- **Technical depth**: Explain verifier (safety), JIT compilation (performance), eBPF maps (state sharing)

#### Discovery 2: The May 2025 Inflection Point
- **Insight**: Grafana donated Beyla to OpenTelemetry, creating official OTel eBPF instrumentation
- **What changed**: No longer experimental—now part of core OpenTelemetry ecosystem
- **Evidence**: Production deployments showing 100% service coverage achieved in hours vs weeks
- **Deployment model**: DaemonSet per node, auto-discovers all services, zero application changes

#### Discovery 3: Protocol-Level vs Library-Level
- **Insight**: eBPF captures at protocol level (HTTP/2, gRPC wire format), not library level
- **Advantage**: Works for ANY language, ANY framework—Go, Java, Python, Rust, even custom binaries
- **Trade-off**: Can't access application context—no user IDs, business metrics, custom attributes
- **Real example**: HTTP request captured with method, path, status, duration—but not "which customer" or "which feature flag"

#### Complication: The Encryption Blind Spot
- **Challenge**: TLS terminates before kernel network stack—eBPF sees encrypted bytes
- **Solutions**:
  - uprobes on OpenSSL/BoringSSL (language-specific, version-dependent)
  - Service mesh integration (Istio/Cilium handle TLS)
  - Sidecar proxy approach
- **Reality check**: This is solvable but adds complexity—not truly "zero configuration"

**Key Points**:
- eBPF lifecycle: Load → Verify → JIT compile → Attach → Execute (kernel ensures safety)
- Three deployment patterns: DaemonSet, OpenTelemetry Operator, service mesh integration
- Protocol support: HTTP/1.1, HTTP/2, gRPC, Redis, SQL—but custom protocols need SDK

### ACT 3: RESOLUTION (3-4 min)

- **Synthesis**: eBPF and SDKs aren't competing—they're complementary layers of the observability stack
  - **eBPF layer**: Universal baseline coverage, network-level metrics, zero-touch onboarding
  - **SDK layer**: Business context, custom attributes, application-specific instrumentation

- **Application**: Decision framework for when to use each:
  - **Choose eBPF-first** when: Polyglot environment, need 100% coverage fast, performance-critical services, legacy/third-party binaries
  - **Add SDK instrumentation** when: Need business context (user IDs, feature flags), custom spans for business logic, application-specific metrics
  - **Hybrid approach**: eBPF for baseline, SDK for business-critical paths—most production teams land here

- **Empowerment**: "Start with eBPF DaemonSet for instant visibility across all services. Then add targeted SDK instrumentation only where you need business context. You'll go from 40% coverage to 100% in hours, then enhance critical paths over weeks."

**Key Points**:
- Production architecture: eBPF baseline + SDK enhancement for business-critical paths
- Week 1 action: Deploy OpenTelemetry eBPF Operator on non-production cluster, validate protocol coverage
- Maturity path: Start eBPF-only → Add SDK for top 3 revenue paths → Extend as needed

## Story Elements

**KEY CALLBACKS**:
- Return to "30-40% blind spots" → Show how eBPF eliminates them
- Return to "10-50% overhead" → Contrast with under 2%
- Return to "weeks of instrumentation" → Contrast with "hours to 100% coverage"

**NARRATIVE TECHNIQUES**:
- **Anchoring Statistic**: Under 2% overhead (vs 10-50%)—return to this throughout
- **Thought Experiment**: Walk through HTTP request from app → kernel → eBPF → OTel span
- **Devil's Advocate**: Jordan presents eBPF benefits, Alex probes limitations (TLS, context)

**SUPPORTING DATA**:
- Under 2% CPU overhead for eBPF instrumentation (Grafana Beyla benchmarks)
- 10-50% overhead for traditional APM agents (New Relic, Datadog agent docs)
- 30-40% services uninstrumented in average enterprise (Gartner observability report 2024)
- May 2025: Grafana Beyla donation to OpenTelemetry
- 100% coverage achievable in hours vs weeks with SDK approach

## Quality Checklist

- [x] Throughline clear (one sentence): "From 'we can't instrument everything' to 'zero-code coverage with kernel-level precision'"
- [x] Hook compelling (keep listening after 60s?): Promise of complete coverage without code changes + under 2% overhead
- [x] Sections build momentum: Problem → Kernel magic → Inflection point → Trade-offs → Framework
- [x] Insights connect (not random facts): Each discovery builds toward the complementary layers conclusion
- [x] Emotional beats land: Recognition (instrumentation pain), Surprise (kernel interception), Empowerment (clear framework)
- [x] Callbacks create unity: 30-40% blind spots, 10-50% overhead, weeks vs hours
- [x] Payoff satisfies: Delivers decision framework + concrete week-1 action
- [x] Narrative rhythm: Mystery of "how can this work?" drives investigation
- [x] Technical depth appropriate: Explains kernel hooks, verifier, eBPF maps, protocol capture
- [x] Listener value clear: Can immediately deploy eBPF + knows when to add SDK

### Technical Depth Standards (Technical Topic)

- [x] Explain HOW it works under the hood: Kernel hooks, syscall interception, eBPF lifecycle
- [x] Cover implementation details: Verifier safety, JIT compilation, eBPF maps for state
- [x] Address "Why is it designed this way?": Safety (verifier), Performance (JIT), Flexibility (maps)
- [x] Include system-level concepts: Kernel network stack, syscalls, TLS termination points
- [x] Show actual technical flow: App → syscall → kernel → eBPF probe → maps → userspace → OTel span

## Cross-Links

- **Blog post**: `/blog/2025-11-17-opentelemetry-ebpf-instrumentation-production-guide`
- **Related episodes**:
  - #022: OpenTelemetry Observability (foundational concepts)
  - #027: Kubernetes Optimization (eBPF for networking mentioned)

## Episode Metadata

- **Episode Number**: 00028
- **Slug**: `opentelemetry-ebpf-instrumentation`
- **Target Duration**: 12-15 minutes
- **Target Audience**: Senior platform engineers, SREs (5+ years)
