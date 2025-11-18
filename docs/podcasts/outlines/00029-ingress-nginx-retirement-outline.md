# Episode Outline: Ingress NGINX Retirement - The March 2026 Migration Deadline

## Story Planning

**NARRATIVE STRUCTURE**: Mystery/Discovery (Why is this happening NOW? What do we do?)

**CENTRAL TENSION**: The most popular Kubernetes ingress controller—used by nearly everyone—will stop receiving security patches in March 2026. Platform teams have ~4 months to migrate or face unpatched CVEs in production internet-facing infrastructure.

**THROUGHLINE**: "From 'Ingress NGINX just works' to understanding why it's dying and how to migrate before the security cliff"

**EMOTIONAL ARC**:
- **Recognition**: "Wait, we use this everywhere"
- **Surprise**: "Only 1-2 maintainers for years? The replacement project failed?"
- **Urgency**: "March 2026 is 4 months away"
- **Empowerment**: "Here's our migration path and timeline"

---

## Act Structure

### ACT 1: SETUP - The Announcement (2-3 min)

**Hook**: November 11, 2025—Kubernetes SIG Network dropped a bombshell. Ingress NGINX, the de facto standard ingress controller used by the majority of Kubernetes deployments, will be retired in March 2026. After that date: no releases, no bugfixes, no security patches.

**Stakes**:
- Every Kubernetes cluster with internet-facing services likely uses Ingress NGINX
- Unpatched edge router = unacceptable security risk for production
- CVE-2025-1974 already demonstrated the vulnerability pattern
- 4 months to migrate isn't much time for complex traffic routing

**Promise**: We'll uncover why this happened after years of stability, examine the migration options, and give you a decision framework and timeline to migrate safely.

**Key Points**:
- Official announcement from Kubernetes SIG Network and Security Response Committee (Nov 11, 2025)
- "Best-effort maintenance until March 2026, then nothing"
- InGate replacement project never gained traction—also being retired
- This affects nearly every production Kubernetes deployment

---

### ACT 2: EXPLORATION - The Investigation (6-8 min)

#### Discovery 1: Why This Is Happening (2 min)

**The Maintainer Crisis**:
- For years, only 1-2 people doing development work—on their own time, after work hours, weekends
- Announcement last year about winding down + developing InGate replacement failed to generate help
- SIG Network and Security Response Committee "exhausted efforts to find additional support"
- InGate never progressed far enough—also being retired

**Key Points**:
- Unsustainable open source maintenance model
- Security Response Committee involvement signals severity
- This is a systemic problem, not just one project

#### Discovery 2: The Security Cliff (2 min)

**What "No Security Patches" Means**:
- NGINX (the underlying proxy) gets CVEs frequently
- After March 2026, discovered vulnerabilities stay unpatched forever
- Internet-facing edge routers are prime attack targets
- Even dev/staging environments become attack vectors

**The Annotation Debt**:
- Ingress API's weakness: vendor-specific annotations for everything beyond basic routing
- Teams have years of custom annotations, snippets, regex rules
- These don't map 1:1 to Gateway API—migration isn't just find-and-replace

**Key Points**:
- CVE-2025-1974 was a preview of the risk
- Custom annotations = technical debt that complicates migration
- "Can I keep running it?" Yes, but it's a security risk you're accepting

#### Discovery 3: The Migration Options (3-4 min)

**Option 1: Gateway API (Recommended Path)**:
- Official Kubernetes successor to Ingress
- Not "Ingress v2"—complete redesign
- Protocol-agnostic: HTTP, TCP, gRPC, UDP
- Role-based resource model (Gateway, HTTPRoute, etc.)
- Built-in support for traffic splitting, canary, blue-green
- Supported by: Envoy Gateway, Cilium, Kong, Traefik, NGINX Gateway Fabric

**Option 2: Alternative Ingress Controllers**:
- NGINX Gateway Fabric (NGINX's Gateway API implementation)
- Kong Gateway (feature-rich, enterprise support)
- Traefik (popular, good Kubernetes integration)
- Cilium (eBPF-based, growing momentum)

**The Gateway API Advantage**:
- Portability: Switch controllers without rewriting configs
- Standardization: No more vendor-specific annotation sprawl
- Future-proof: Where Kubernetes networking is going

**Key Points**:
- Gateway API is the strategic choice—not just a replacement
- Multiple mature implementations to choose from
- ingress2gateway tool helps scaffold migration (but not complete solution)

#### Complication: The Migration Challenges (1 min)

**What Makes This Hard**:
- Annotations don't map 1:1 (backendConfig, custom snippets)
- Regex behavior differs (NGINX regex vs Gateway API strict matching)
- DNS propagation during cutover can cause disruption
- SSL termination and header propagation need validation
- Gateway API is stricter by design—no more "snippets" escape hatch

**Key Points**:
- Use ingress2gateway as scaffold, not final product
- Budget time for annotation translation
- Parallel running period essential

---

### ACT 3: RESOLUTION - The Migration Framework (3-4 min)

#### Synthesis: Decision Framework

**Choosing Your Path**:

1. **If you want strategic investment**: Gateway API + Envoy Gateway or Cilium
   - Pros: Future-proof, portable, ecosystem momentum
   - Cons: Steeper learning curve, annotation rewriting

2. **If you want minimal change**: NGINX Gateway Fabric
   - Pros: Similar mental model to Ingress NGINX
   - Cons: Still NGINX ecosystem, less portability

3. **If you need enterprise support**: Kong Gateway or Traefik Enterprise
   - Pros: Commercial backing, support SLAs
   - Cons: Cost, potential lock-in

**Recommendation**: Gateway API is where Kubernetes networking is going. If migrating anyway, go to the strategic destination, not a halfway point.

#### Application: Migration Timeline

**Phase 1: Assessment (Week 1-2)**
- Inventory all Ingress resources across clusters
- Document custom annotations and snippets
- Identify highest-risk services (internet-facing, business-critical)
- Choose target controller/implementation

**Phase 2: Pilot (Week 3-4)**
- Deploy Gateway API controller on non-production
- Migrate one simple service using ingress2gateway
- Manually translate complex annotations
- Validate SSL, headers, routing behavior

**Phase 3: Staging Migration (Month 2)**
- Migrate staging environment completely
- Run parallel Ingress + Gateway for validation
- Performance and load testing
- Runbook development for production

**Phase 4: Production Migration (Month 3)**
- Migrate lowest-risk production services first
- Gradual traffic shift (10% → 50% → 100%)
- Keep Ingress as fallback during transition
- Monitor for routing anomalies

**Phase 5: Cleanup (Month 4 - before March 2026)**
- Remove Ingress NGINX controllers
- Archive old Ingress manifests
- Update documentation and runbooks
- Train team on Gateway API patterns

#### Empowerment: Immediate Actions

**This Week**:
1. Read the official announcement: kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/
2. Run: `kubectl get ingress -A` to see your exposure
3. Document your most complex Ingress resources
4. Evaluate Gateway API implementations (Envoy Gateway, Cilium Gateway API, Kong)

**The Positive Reframe**: This forced migration is an opportunity. Gateway API is genuinely better—more portable, more capable, cleaner model. You're not just replacing a deprecated controller; you're upgrading your entire traffic management story.

---

## Story Elements

### KEY CALLBACKS
- "Just works" (Act 1) → "Just works until it doesn't get security patches" (Act 3)
- Annotation sprawl problem (Act 2) → Gateway API solves with standardization (Act 3)
- 1-2 maintainers (Act 2) → Sustainable ecosystem behind Gateway API (Act 3)

### NARRATIVE TECHNIQUES
- **Anchoring Event**: Nov 11 announcement as timeline anchor
- **Historical Context**: "For years, 1-2 people maintaining..."
- **Security Urgency**: CVE-2025-1974 as concrete example
- **Decision Framework**: Structured choice between paths
- **Concrete Timeline**: 4-phase migration plan with specific actions

### SUPPORTING DATA
- Official announcement: Kubernetes SIG Network, Nov 11, 2025
- Maintenance status: "Best-effort until March 2026"
- InGate failure: "Never progressed far enough"
- Maintainer situation: "1-2 people, after work hours, weekends"
- Tool: ingress2gateway for migration scaffolding
- CVE reference: CVE-2025-1974

### TECHNICAL DEPTH
- Gateway API resource model (Gateway, HTTPRoute, GRPCRoute)
- Migration tool capabilities and limitations
- Annotation translation challenges
- Controller implementation differences
- Parallel running strategies

---

## Quality Checklist

- [x] Throughline clear: "From 'just works' to understanding why it's dying and how to migrate"
- [x] Hook compelling: Breaking news with deadline creates immediate relevance
- [x] Sections build momentum: Announcement → Why → Options → How
- [x] Insights connect: Maintainer crisis → security risk → migration necessity
- [x] Emotional beats land: Surprise at maintainer situation, urgency at timeline, empowerment at framework
- [x] Callbacks create unity: "Just works" returns transformed
- [x] Payoff satisfies: Clear decision framework + timeline + immediate actions
- [x] Narrative rhythm: Story not list (why before what, context before options)
- [x] Technical depth appropriate: Migration phases, annotation challenges, controller comparison
- [x] Listener value clear: Immediate actions this week, 4-phase migration plan

---

## Episode Metadata

**Working Title**: Ingress NGINX Retirement: The March 2026 Migration Deadline
**Episode Number**: 029
**Estimated Duration**: 12-15 minutes
**Content Type**: Breaking news + practical guidance
**Urgency**: HIGH - Time-sensitive with hard deadline

**Sources**:
- https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/
- https://livewyer.io/blog/ingress-nginx-retirement-migration-guidance-for-kubernetes-platform-teams/
- https://gateway-api.sigs.k8s.io/guides/migrating-from-ingress/
- https://kubernetes.io/blog/2023/10/25/introducing-ingress2gateway/
