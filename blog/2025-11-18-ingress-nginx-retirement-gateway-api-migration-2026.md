---
title: "Ingress NGINX Retirement March 2026: Complete Gateway API Migration Guide"
description: "Migrate from Ingress NGINX before March 2026 deadline. Four-phase migration framework, controller comparison, and step-by-step Gateway API implementation."
slug: ingress-nginx-retirement-gateway-api-migration-2026
date: 2025-11-18
datePublished: "2025-11-18"
dateModified: "2025-11-18"
authors: [vibesre]
tags: [kubernetes, gateway-api, ingress, migration, security]
keywords:
  - ingress nginx retirement
  - gateway api migration
  - kubernetes ingress replacement
  - ingress nginx march 2026
  - gateway api vs ingress
  - ingress2gateway
  - envoy gateway
  - cilium gateway api
  - nginx gateway fabric
  - kubernetes networking
  - httproute
  - grpcroute
schema:
  type: FAQPage
  questions:
    - question: "When is Ingress NGINX being retired?"
      answer: "Ingress NGINX will be retired in March 2026. After that date, there will be no releases, no bugfixes, and no security patches for any vulnerabilities discovered."
    - question: "Why is Ingress NGINX being retired?"
      answer: "For years, Ingress NGINX has had only 1-2 maintainers doing development work on their own time after hours and weekends. SIG Network and the Security Response Committee exhausted efforts to find additional support."
    - question: "What should I migrate to from Ingress NGINX?"
      answer: "The recommended migration path is Gateway API, which provides protocol-agnostic routing, role-based resource model, and controller portability. Alternative options include NGINX Gateway Fabric, Kong Gateway, Traefik, and Cilium."
    - question: "How long does Gateway API migration take?"
      answer: "Plan for 3-4 months: Assessment (weeks 1-2), Pilot (weeks 3-4), Staging migration (month 2), Production migration (month 3), with buffer time before the March 2026 deadline."
    - question: "What is the ingress2gateway tool?"
      answer: "ingress2gateway is an open-source tool from the Kubernetes SIG Network community that automatically converts Ingress resources to Gateway API resources (Gateway, HTTPRoute). It scaffolds the migration but requires manual translation of custom annotations."
    - question: "What are the security risks of not migrating from Ingress NGINX?"
      answer: "After March 2026, any CVE discovered in Ingress NGINX will remain unpatched forever. CVE-2025-1974 (9.8 CVSS) demonstrated the risk—unauthenticated RCE affecting 40%+ of Kubernetes clusters."
    - question: "Which Gateway API controller should I choose?"
      answer: "Envoy Gateway for maximum portability and CNCF backing, Cilium for eBPF performance if already using Cilium CNI, NGINX Gateway Fabric for minimal mental model change, Kong/Traefik Enterprise for enterprise support contracts."
    - question: "How is Gateway API different from Ingress?"
      answer: "Gateway API is protocol-agnostic (HTTP, gRPC, TCP, UDP), uses role-based resources (GatewayClass, Gateway, HTTPRoute), provides built-in traffic splitting/canary support, and offers true controller portability without annotation lock-in."
---

On November 11, 2025, Kubernetes SIG Network dropped a bombshell: Ingress NGINX—the de facto standard ingress controller running in over 40% of production Kubernetes clusters—will be retired in March 2026. After that date: no releases, no bugfixes, no security patches. Ever. The project that's been handling your internet-facing traffic has had only 1-2 maintainers for years, working nights and weekends. Now, with four months until the deadline, platform teams face a critical migration that affects every service behind your edge router.

> 🎙️ **Listen to the podcast episode**: [Ingress NGINX Retirement: The March 2026 Migration Deadline](/podcasts/00029-ingress-nginx-retirement) - Jordan and Alex break down why this happened, examine the security implications, and provide a four-phase migration framework with immediate actions for this week.

## TL;DR

- **Problem**: Ingress NGINX retires March 2026—no security patches after that date for the de facto Kubernetes ingress controller used by 40%+ of clusters.
- **Root Cause**: Only 1-2 volunteer maintainers for years; SIG Network exhausted efforts to find help; replacement project InGate never reached viable state.
- **Security Risk**: CVE-2025-1974 (9.8 CVSS) demonstrated the pattern—critical RCE vulnerabilities that need immediate patches. After March 2026, the next one stays open forever.
- **Migration Path**: Gateway API with HTTPRoute, GRPCRoute, TCPRoute resources. Tool: ingress2gateway scaffolds conversion.
- **Timeline**: 3-4 months—Assessment (weeks 1-2), Pilot (weeks 3-4), Staging (month 2), Production (month 3).
- **Key Takeaway**: Start assessment this week. Four months is tight for complex environments with custom annotations.

## Key Statistics (November 2025)

| Metric | Value | Source |
|--------|-------|--------|
| Kubernetes clusters affected | 40%+ | [Wiz Research](https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities), March 2025 |
| Retirement deadline | March 2026 | [Kubernetes Blog](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/), Nov 2025 |
| Maintainers for years | 1-2 people | [Kubernetes Blog](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/), Nov 2025 |
| CVE-2025-1974 CVSS | 9.8 Critical | [NVD](https://kubernetes.io/blog/2025/03/24/ingress-nginx-cve-2025-1974/), March 2025 |
| Time to migrate | 3-4 months | Industry migration guides |
| Gateway API v1.0 release | October 2023 | [Gateway API SIG](https://gateway-api.sigs.k8s.io/) |
| Controllers supporting Gateway API | 25+ | [Gateway API Implementations](https://gateway-api.sigs.k8s.io/implementations/) |
| ingress2gateway version | v0.4.0 | [GitHub](https://github.com/kubernetes-sigs/ingress2gateway) |

## The Retirement Crisis

The [official announcement](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/) from SIG Network and the Security Response Committee was blunt: "Best-effort maintenance will continue until March 2026. Afterward, there will be no further releases, no bugfixes, and no updates to resolve any security vulnerabilities that may be discovered."

The Security Response Committee's involvement signals this isn't just deprecation—it's a security-driven decision about an unmaintainable project.

### The Unsustainable Open Source Reality

For years, Ingress NGINX has had only 1-2 people doing development work. On their own time. After work hours. Weekends. This is the most critical traffic component in most Kubernetes deployments, and it's been maintained by volunteers with day jobs.

The announcement explicitly called out the failure to find help: "SIG Network and the Security Response Committee exhausted their efforts to find additional support. They couldn't find people to help maintain it."

### The InGate Replacement That Never Happened

Last year, the Ingress NGINX maintainers announced plans to wind down the project and develop InGate as a replacement, together with the Gateway API community. The hope was this announcement would generate interest in either maintaining the old project or building the new one.

It didn't work. InGate never progressed far enough to be viable. It's also being retired. The whole thing just... failed.

### What Happens After March 2026

Your existing deployments keep running. The installation artifacts remain available. You can still install Ingress NGINX.

But:
- **No new releases** for any reason
- **No bugfixes** for any issues discovered
- **No security patches** for any vulnerabilities found

That last point is critical. NGINX, the underlying proxy, gets CVEs fairly regularly. After March 2026, if a vulnerability is discovered, it stays unpatched. Forever. On your internet-facing edge router.

> **💡 Key Takeaway**
>
> Ingress NGINX retirement isn't deprecation—it's complete abandonment. After March 2026, any CVE discovered stays open forever on your internet-facing edge router. This isn't optional modernization; it's required security hygiene.

## The Security Wake-Up Call: CVE-2025-1974

In March 2025, Wiz researchers disclosed [CVE-2025-1974](https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities), dubbed "IngressNightmare." It demonstrated exactly why an unmaintained edge router is unacceptable.

### The Vulnerability Details

**CVSS Score**: 9.8 Critical

**Impact**: Unauthenticated remote code execution via the Ingress NGINX admission controller. Any pod on the network could take over your Kubernetes cluster. No credentials or admin access required.

**Technical Mechanism**: The vulnerability exploited how the admission controller validates NGINX configurations. Attackers could inject malicious configuration through the `ssl_engine` directive, achieving arbitrary code execution in the controller context.

**Scope**: In the default installation, the controller can access all Secrets cluster-wide. A successful exploit means disclosure of every secret in your cluster.

**Related CVEs**: This was part of a family—CVE-2025-1098 (8.8 CVSS), CVE-2025-1097 (8.8 CVSS), CVE-2025-24513 (4.8 CVSS).

### The Pattern That Should Worry You

CVE-2025-1974 was patched. Versions 1.11.5 and 1.12.1 fixed the issue.

But this CVE demonstrated the pattern: Ingress NGINX gets critical vulnerabilities requiring immediate patches. After March 2026, the next 9.8 CVSS stays unpatched forever.

If you're among the over 40% of Kubernetes administrators using Ingress NGINX, this is your wake-up call.

> **💡 Key Takeaway**
>
> CVE-2025-1974 (9.8 CVSS) proved the pattern—Ingress NGINX gets critical vulnerabilities requiring immediate patches. After March 2026, the next one stays unpatched forever. Your internet-facing edge router becomes a permanent attack surface.

### Don't Forget Dev and Staging

"We'll keep running it on dev" isn't safe either. Dev environments often contain sensitive data. Staging environments provide network paths into production.

Any environment handling sensitive data or connected to production networks is a risk vector with unpatched infrastructure.

> **💡 Key Takeaway**
>
> "We'll just keep running it" isn't viable for any environment handling sensitive data or connected to production networks. The security clock is ticking on all Ingress NGINX deployments—production, staging, and dev.

## Gateway API: The Strategic Migration Target

The official recommendation is clear: migrate to [Gateway API](https://gateway-api.sigs.k8s.io/). But this isn't just "another ingress controller"—it's a complete redesign of how Kubernetes handles traffic routing.

### Why Gateway API Is Better, Not Just Newer

**Protocol-Agnostic Design**

Ingress only really handled HTTP and HTTPS well. Everything else—gRPC, TCP, UDP—required vendor-specific annotations or workarounds. This created "annotation sprawl" where your Ingress resources were littered with controller-specific configurations.

Gateway API has native support for HTTP, gRPC, TCP, and UDP. No annotations needed for basic traffic types. The capabilities are in the spec.

**Role-Based Resource Model**

Ingress used a single resource for everything. Gateway API separates concerns:

- **GatewayClass**: Infrastructure provider defines available gateway types
- **Gateway**: Platform/infrastructure team manages the actual gateway instance
- **HTTPRoute/GRPCRoute/TCPRoute**: Application teams manage their routing rules

This separation enables multi-tenancy and clear ownership. Application developers don't need access to infrastructure-level settings.

**Controller Portability**

This is the big one. With Ingress, the annotation sprawl meant you were locked to your controller. Want to switch from Ingress NGINX to Traefik? Rewrite all your annotations.

Gateway API is standardized across 25+ implementations. An HTTPRoute that works with Envoy Gateway today works with Cilium tomorrow. The spec is the spec—no vendor-specific extensions needed for common functionality.

**Built-in Traffic Management**

Native support for:
- Traffic splitting and weighting
- Canary deployments
- Blue-green deployments
- Header-based routing
- Request/response manipulation

All without controller-specific annotations.

> **💡 Key Takeaway**
>
> Gateway API isn't Ingress v2—it's a complete redesign. The annotation sprawl that locked you to your controller is replaced by portable, standardized resources. Migration is an upgrade to your entire traffic management story, not just a controller swap.

### Gateway API Controller Comparison

Choosing a controller depends on your existing stack and priorities. Here's how the major implementations compare:

| Controller | Strengths | Weaknesses | Best For |
|------------|-----------|------------|----------|
| **[Envoy Gateway](https://gateway.envoyproxy.io/)** | Reference implementation, CNCF backing, service mesh integration, comprehensive observability | Higher resource consumption, shared namespace architecture | Teams wanting maximum portability, service mesh integration |
| **[Cilium Gateway API](https://docs.cilium.io/en/stable/network/servicemesh/gateway-api/)** | eBPF performance, fast config updates, integrated with Cilium CNI | Highest CPU usage, scalability issues with large route configs | Teams already using Cilium CNI wanting unified stack |
| **[NGINX Gateway Fabric](https://github.com/nginxinc/nginx-gateway-fabric)** | Proven stability, familiar to NGINX users, v2.0 architecture improvements | Memory scales with routes, CPU spikes with other controllers | Teams with NGINX expertise wanting minimal mental model change |
| **[Kong Gateway](https://docs.konghq.com/gateway/)** | Enterprise support, extensive plugins, API management features | Premium pricing, heavier footprint | Enterprises needing support contracts and API management |
| **[Traefik](https://doc.traefik.io/traefik/)** | Good Kubernetes integration, auto-discovery, Let's Encrypt built-in | Less Gateway API maturity than others | Teams wanting simplified certificate management |

### Decision Framework

**Choose Envoy Gateway when**: You want maximum portability, CNCF backing, and potential service mesh integration. You don't mind higher resource overhead.

**Choose Cilium Gateway API when**: You're already using Cilium for CNI and want a unified networking stack with eBPF performance. Be aware of scalability limits with hundreds of routes.

**Choose NGINX Gateway Fabric when**: Your team knows NGINX, you want minimal learning curve, and you value battle-tested stability over cutting-edge features.

**Choose Kong or Traefik Enterprise when**: You need enterprise support contracts, SLAs, and/or API management capabilities.

> **💡 Key Takeaway**
>
> Controller choice depends on existing stack and priorities. Envoy Gateway for maximum portability, Cilium if you're already there, NGINX Gateway Fabric for familiarity. All support the same Gateway API spec—you can switch later without rewriting configurations.

## The Four-Phase Migration Framework

Four months isn't much time for something this foundational. Here's a structured approach that gets you to production before March 2026 with buffer for the inevitable surprises.

### Phase 1: Assessment (Weeks 1-2)

**Inventory Your Scope**

Start with the basics:

```bash
# Count all Ingress resources across all namespaces
kubectl get ingress -A --no-headers | wc -l

# List them with details
kubectl get ingress -A -o wide
```

Document every cluster using Ingress NGINX. You need to know your total migration scope before you can plan.

**Document Custom Configurations**

For each Ingress resource, capture:

- All annotations (especially `nginx.ingress.kubernetes.io/*`)
- Configuration snippets (`configuration-snippet`, `server-snippet`)
- Custom Lua scripts
- Regex routing patterns

The custom snippets are your biggest migration risk. They don't map 1:1 to Gateway API. Flag them now.

```bash
# Find Ingresses with configuration snippets
kubectl get ingress -A -o yaml | grep -B 20 "configuration-snippet"
```

**Identify Risk Levels**

Rank your services:
- **High risk**: Internet-facing, business-critical, complex routing
- **Medium risk**: Internal services with custom annotations
- **Low risk**: Simple routing, few annotations

**Choose Your Target Controller**

Use the decision framework above. Consider:
- Existing team expertise
- Enterprise support requirements
- Integration with current stack (especially if already using Cilium)

### Phase 2: Pilot (Weeks 3-4)

**Deploy Gateway API Infrastructure**

First, install the Gateway API CRDs:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.1/standard-install.yaml
```

Then deploy your chosen controller following its documentation.

Create your GatewayClass and Gateway resources:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: my-gateway
  namespace: gateway-system
spec:
  gatewayClassName: my-gateway-class
  listeners:
  - name: http
    protocol: HTTP
    port: 80
```

**Migrate a Simple Service First**

Choose a service with minimal annotations—not your most complex routing. Use [ingress2gateway](https://github.com/kubernetes-sigs/ingress2gateway) to scaffold the conversion:

```bash
# Install the tool
go install github.com/kubernetes-sigs/ingress2gateway@latest

# Convert an Ingress resource
ingress2gateway print --input-file my-ingress.yaml --providers ingress-nginx
```

The tool outputs Gateway API resources (Gateway, HTTPRoute). This is a scaffold, not a complete solution—you'll need to review and adjust.

**Manual Annotation Translation**

Common translations:

| Ingress NGINX Annotation | Gateway API Equivalent |
|--------------------------|------------------------|
| `nginx.ingress.kubernetes.io/ssl-redirect: "true"` | RequestRedirect filter in HTTPRoute |
| `nginx.ingress.kubernetes.io/rewrite-target: /` | URLRewrite filter in HTTPRoute |
| `nginx.ingress.kubernetes.io/proxy-body-size` | BackendRef configuration or policy |

For custom snippets and Lua scripts, you may need to:
- Move logic to the application layer
- Use a service mesh for advanced traffic manipulation
- Implement custom policies specific to your controller

**Validate Behavior**

Critical validation points:
- SSL/TLS termination works correctly
- Headers propagate as expected
- Regex matching behaves the same (NGINX regex ≠ Gateway API strict matching)
- Timeouts and buffer sizes match

### Phase 3: Staging Migration (Month 2)

**Full Environment Migration**

Migrate all services in staging. Run Ingress and Gateway in parallel—don't cut over immediately.

```yaml
# Example: HTTPRoute for a service
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-service
  namespace: my-app
spec:
  parentRefs:
  - name: my-gateway
    namespace: gateway-system
  hostnames:
  - "my-service.example.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api
    backendRefs:
    - name: my-service
      port: 8080
```

**Performance Testing**

Benchmark against your current performance:
- Request latency (p50, p95, p99)
- Throughput under load
- Resource consumption (CPU, memory)
- Connection handling

Gateway API controllers have different performance characteristics than Ingress NGINX. Know what you're getting before production.

**Develop Runbooks**

Your team needs to learn Gateway API resources before production incidents:
- GatewayClass, Gateway, HTTPRoute, ReferenceGrants
- Controller-specific troubleshooting
- Common failure modes

Document rollback procedures. You want people who've seen the failure modes before they're handling them at 2 AM.

> **💡 Key Takeaway**
>
> Runbooks before production. You want teams who've seen Gateway API failure modes before handling them at 2 AM. Staging migration is as much about team readiness as technical validation.

### Phase 4: Production Migration (Month 3)

**Start Low-Risk**

Begin with your lowest-traffic, lowest-criticality services. Validate:
- Monitoring and alerting work
- Logs are captured correctly
- Metrics dashboards show the right data

**Gradual Traffic Shift**

Don't big-bang cutover. Use DNS or load balancer traffic splitting:

1. **10% traffic** to Gateway API, 90% to Ingress
2. Monitor for 24-48 hours
3. **50% traffic** split
4. Monitor for 24-48 hours
5. **100% traffic** to Gateway API
6. Keep Ingress as fallback for 1-2 weeks

**Monitor for Anomalies**

Watch for:
- Routing errors or 404s
- Latency increases
- SSL certificate issues
- Header manipulation problems

**Cleanup (Month 4)**

Once confident:
- Remove old Ingress controllers
- Archive Ingress manifests (you might need to reference them)
- Update documentation and runbooks
- Train new team members on Gateway API

## Common Migration Pain Points

### Configuration Snippets

These are your biggest challenge. Ingress NGINX allowed raw NGINX configuration:

```yaml
nginx.ingress.kubernetes.io/configuration-snippet: |
  more_set_headers "X-Custom-Header: value";
```

Gateway API doesn't have an equivalent. Options:
- Use controller-specific policies (each controller handles this differently)
- Move logic to application layer
- Implement via service mesh

### Regex Behavior Differences

NGINX uses PCRE regex. Gateway API uses a stricter matching syntax. Test every regex pattern:

```yaml
# Ingress NGINX
nginx.ingress.kubernetes.io/use-regex: "true"
path: /api/v[0-9]+/users

# Gateway API - may need different approach
path:
  type: RegularExpression
  value: "/api/v[0-9]+/users"
```

Validate that patterns match the same traffic. Edge cases will bite you.

### SSL/TLS Certificate Handling

Gateway API handles TLS at the Gateway level, not the Route level:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
spec:
  listeners:
  - name: https
    protocol: HTTPS
    port: 443
    tls:
      mode: Terminate
      certificateRefs:
      - name: my-cert
```

Verify:
- Certificates are referenced correctly
- TLS termination points match expectations
- Certificate rotation still works

## Practical Actions This Week

### For Individual Engineers

1. **Read the official announcement**: https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/
2. **Inventory your scope**: `kubectl get ingress -A --no-headers | wc -l`
3. **Flag your complex resources**: Find Ingresses with custom snippets, Lua scripts, regex routing

### For Platform Teams

**This Week**:
- Complete full inventory across all clusters
- Identify owner for migration project
- Choose target Gateway API controller
- Estimate scope (how many Ingresses, how many with custom annotations)

**Next Month**:
- Set up non-production cluster for pilot
- Install Gateway API CRDs and controller
- Migrate first 2-3 simple services
- Document annotation mapping patterns

**Month 2-3**:
- Complete staging migration
- Conduct performance/load testing
- Develop runbooks and train team
- Begin production migration

### For Leadership

**The Argument**: Ingress NGINX retirement is a security mandate, not optional modernization. After March 2026, any CVE in your internet-facing edge router stays unpatched forever. CVE-2025-1974 (9.8 CVSS critical RCE) demonstrated the risk.

**The Ask**:
- 2-3 engineer-months for migration (varies by complexity)
- Possible licensing costs if choosing commercial controller
- Timeline: Start immediately, complete by end of February

**The Timeline**:
- Weeks 1-2: Assessment and planning
- Weeks 3-4: Pilot migration
- Month 2: Staging migration and testing
- Month 3: Production migration
- Month 4: Cleanup and documentation

> **💡 Key Takeaway**
>
> Start assessment this week. Four months isn't much time for something this foundational. Don't wait for January to discover you have 200 complex Ingress resources with custom snippets to migrate. The March 2026 deadline is real, and the clock is ticking.

## 📚 Learning Resources

### Official Documentation
- [Gateway API Documentation](https://gateway-api.sigs.k8s.io/) - Complete spec, guides, and implementation details
- [Migrating from Ingress Guide](https://gateway-api.sigs.k8s.io/guides/migrating-from-ingress/) - Official migration guide from Gateway API SIG
- [Gateway API Implementations](https://gateway-api.sigs.k8s.io/implementations/) - Full list of 25+ controllers

### Migration Tools
- [ingress2gateway GitHub](https://github.com/kubernetes-sigs/ingress2gateway) - Automated conversion tool for scaffolding migration
- [Introducing ingress2gateway](https://kubernetes.io/blog/2023/10/25/introducing-ingress2gateway/) - Official announcement and usage guide

### Controller Documentation
- [Envoy Gateway](https://gateway.envoyproxy.io/) - Reference implementation documentation
- [NGINX Gateway Fabric](https://docs.nginx.com/nginx-gateway-fabric/) - NGINX's Gateway API implementation
- [Cilium Gateway API](https://docs.cilium.io/en/stable/network/servicemesh/gateway-api/) - eBPF-based implementation
- [Kong Kubernetes Ingress Controller](https://docs.konghq.com/kubernetes-ingress-controller/) - Kong's Gateway API support

### Migration Guides
- [LiveWyer Migration Guidance](https://livewyer.io/blog/ingress-nginx-retirement-migration-guidance-for-kubernetes-platform-teams/) - Detailed migration planning guide
- [Tetrate: Migrating to Envoy Gateway](https://tetrate.io/blog/migrating-from-ingress-nginx-to-envoy-gateway/) - Envoy Gateway specific migration

### Security Research
- [Wiz: IngressNightmare CVE-2025-1974](https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities) - Original vulnerability research
- [Datadog Security Labs Analysis](https://securitylabs.datadoghq.com/articles/ingress-nightmare-vulnerabilities-overview-and-remediation/) - Detection and remediation guide

## Related Content

- [Ingress NGINX Retirement Podcast Episode](/podcasts/00029-ingress-nginx-retirement) - 13-minute deep dive with migration framework
- [DNS for Platform Engineering](/podcasts/00023-dns-platform-engineering) - Related networking fundamentals
- [eBPF in Kubernetes](/podcasts/00022-ebpf-kubernetes) - Understanding Cilium's approach
- [Kubernetes IaC & GitOps](/podcasts/00020-kubernetes-iac-gitops) - Managing Gateway API resources declaratively
- [Kubernetes Overview](/technical/kubernetes) - Kubernetes fundamentals
- [Kubernetes Complexity Backlash](/blog/2025-01-16-kubernetes-complexity-backlash-simpler-infrastructure) - Context on Kubernetes ecosystem challenges

---

*The March 2026 deadline is real. Your internet-facing infrastructure can't remain on an unmaintained project. Start your assessment this week.*
