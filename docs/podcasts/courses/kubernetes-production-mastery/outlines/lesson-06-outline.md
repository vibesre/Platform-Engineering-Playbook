# Lesson Outline: Episode 6 - Networking & Ingress

## Metadata
- **Course**: Kubernetes Production Mastery
- **Episode**: 6 of 10
- **Duration**: 18 minutes
- **Type**: Core Concept
- **Prerequisites**: Episode 1 (Production Mindset), Episode 4 (Troubleshooting), Episode 5 (StatefulSets for DNS context)
- **Template**: Core Concept (Template 2)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. **Explain** the Kubernetes networking model and how CNI plugins enable pod-to-pod communication
2. **Choose** the appropriate Service type (ClusterIP, NodePort, LoadBalancer) and Ingress controller for production use cases
3. **Determine** when service mesh adds value versus when it's unnecessary complexity

Success criteria:
- Can explain the flat network namespace model and why every pod gets an IP
- Can select the right Service type based on requirements (internal vs external, dev vs production)
- Can configure Ingress with TLS termination using cert-manager
- Can articulate the trade-offs between Istio, Linkerd, and no service mesh
- Can debug common networking failures (pods can't reach service, 502 errors, TLS failures)

## Spaced Repetition Plan

**Introduced** (concepts to repeat later):
- CNI plugins and network policies → Episode 7 (observability of network metrics)
- Ingress controllers and TLS termination → Episode 9 (GitOps deployment of ingress)
- Service mesh concepts → Episode 10 (multi-cluster service mesh federation)
- cert-manager for TLS → Episode 9 (automated certificate management in GitOps)

**Reinforced** (callbacks from earlier episodes):
- Episode 1: Networking as production failure pattern #4
- Episode 4: Troubleshooting workflow (describe → logs → events) applied to network debugging
- Episode 5: StatefulSet DNS names (postgres-0.postgres.default.svc.cluster.local) - now explain HOW DNS works
- Episode 5: Service discovery mentioned - now deep dive into Services

## Lesson Flow

### 1. Recall & Connection (1.5 min)

**Opening Callback**: "In Episode 5, we learned about StatefulSets and stable DNS names. You saw addresses like postgres-0.postgres.default.svc.cluster.local. We said pods could always reach each other using these names. But we didn't explain HOW. How does that DNS resolution actually work? And what happens when pods can't reach each other?"

**Active Recall Prompt**: "Before we continue, try to recall from Episode 1: What was networking failure pattern number four?" [PAUSE 3 sec] "That's right - network segmentation and connectivity issues. Pods that should talk to each other... can't. This is the number four cause of production outages."

**Today's Connection**: "Today we're diving deep into Kubernetes networking. By the end, you'll understand the networking model, how to choose the right Service type, how Ingress controllers work, and when you actually need a service mesh. Plus, how to debug the most common networking failures."

### 2. Learning Objectives (30 sec)

Today you'll learn to:
- Understand the Kubernetes networking model and CNI plugin responsibilities
- Choose between ClusterIP, NodePort, and LoadBalancer services
- Configure Ingress controllers with TLS termination
- Decide when service mesh is worth the complexity

### 3. Concept Introduction: The Kubernetes Networking Model (2.5 min)

**The Core Principle**: "Kubernetes networking is built on one fundamental assumption: all pods can communicate with all other pods without NAT. Every pod gets its own IP address. This is called the flat network namespace model."

**Why This Matters**:
- Traditional Docker: Containers share host network, port conflicts everywhere
- Kubernetes: Pod has IP, containers inside share that IP, port conflicts only within pod
- No port mapping complexity: Container listens on 8080, pod listens on 8080, service routes to 8080

**The Problem This Solves**:
Imagine 100 microservices. Traditional networking: Track which ports on which hosts. Service discovery nightmare. Load balancing manual. Kubernetes: Every pod has IP. Services provide stable endpoints. DNS automatically resolves.

**Analogy**: "Think of traditional networking like a huge office building where everyone shares phone extensions. You have to remember 'Sales is extension 1234, Engineering is 5678.' Kubernetes is like giving everyone their own direct phone number. You just call their number. No extensions, no switchboard confusion."

**The Layers**:
1. **Pod-to-Pod communication** (CNI plugin responsibility)
2. **Service abstraction** (kube-proxy manages iptables/IPVS rules)
3. **Ingress** (L7 routing, TLS termination)
4. **Service mesh** (optional, advanced traffic management)

**Key Insight**: "Most networking issues happen because people don't understand which layer handles what. CNI handles pod connectivity. Services handle load balancing. Ingress handles external access. Service mesh is optional complexity."

### 4. CNI Plugins: The Foundation (3 min)

**What CNI Does** (Container Network Interface):
- Assigns IP addresses to pods
- Sets up network routes so pods can talk
- Enforces network policies (if plugin supports it)
- **Critical**: CNI is a spec, not an implementation - many plugins exist

**Common CNI Plugins Comparison**:

**Calico**:
- **Strengths**: Network policy enforcement, BGP routing for large scale, excellent performance
- **Use case**: Production clusters needing strong network isolation
- **Complexity**: Medium, requires networking knowledge for troubleshooting

**Cilium**:
- **Strengths**: eBPF-based (kernel-level, blazing fast), L7 visibility, service mesh features built-in
- **Use case**: Modern clusters wanting observability without traditional service mesh
- **Complexity**: Higher, eBPF requires recent kernels

**Flannel**:
- **Strengths**: Simple, easy to set up, good for basic clusters
- **Use case**: Development, testing, simple production without complex policies
- **Complexity**: Low, just works

**Weave**:
- **Strengths**: Encryption built-in, simple mesh overlay
- **Use case**: Multi-cloud scenarios, encryption requirements
- **Complexity**: Low to medium

**Decision Framework**:
- "Need network policies for isolation? → Calico or Cilium"
- "Want cutting-edge performance and L7 visibility? → Cilium"
- "Just need basic networking that works? → Flannel"
- "Need built-in encryption between nodes? → Weave"

**When CNI Breaks**:
Common symptom: Pods can schedule and run, but can't reach each other or services.
- Check CNI daemon pods: `kubectl get pods -n kube-system` - look for calico, cilium, flannel pods
- Check pod IP assignment: `kubectl get pods -o wide` - pods without IPs indicate CNI failure
- Check CNI logs: `kubectl logs -n kube-system <cni-pod>`

**Think-Aloud**: "I see a pod stuck in Running state but app logs show 'connection refused' to another service. My thought process: Is this DNS? Networking? First, I check if the pod has an IP. `kubectl get pod -o wide`. It does. So CNI assigned the IP. Next, can the pod resolve DNS? `kubectl exec pod -- nslookup kubernetes.default`. It can. So DNS works. Now I test direct connectivity. `kubectl exec pod -- curl service-name:8080`. Connection refused. Ah! The destination service exists but pods behind it aren't ready. Check with `kubectl get endpoints service-name`. Empty. No pods ready. This is a readiness probe issue, not networking."

### 5. Services: The Stable Abstraction (3.5 min)

**Why Services Exist**:
Pods are ephemeral. IP addresses change. You can't hardcode pod IPs. Services provide stable virtual IPs and DNS names.

**Service Types - Decision Matrix**:

**ClusterIP (Default)**:
- **Purpose**: Internal cluster communication only
- **Use case**: Backend services, databases, internal APIs
- **Access**: Only from within cluster
- **DNS**: `service-name.namespace.svc.cluster.local`
- **Production use**: 80% of services are ClusterIP

**NodePort**:
- **Purpose**: Expose service on every node's IP at a static port (30000-32767 range)
- **Use case**: Development, testing, quick external access
- **Why NOT production**: Every node exposes port, no SSL termination, port range limited
- **When it's acceptable**: On-prem without LoadBalancer support, specific firewall requirements

**LoadBalancer**:
- **Purpose**: Provisions cloud load balancer (AWS ELB, GCP LB, Azure LB)
- **Use case**: Production external services
- **Cost**: Each LoadBalancer service = separate cloud LB ($15-30/month)
- **Best practice**: Use ONE LoadBalancer with Ingress controller instead of many

**ExternalName**:
- **Purpose**: DNS alias to external service (e.g., legacy database outside cluster)
- **Use case**: Gradual migration, accessing external APIs via service abstraction
- **How it works**: Returns CNAME record, no proxying

**Real-World Scenario**: E-commerce platform architecture
- **Frontend**: LoadBalancer service (or Ingress - preferred)
- **Backend API**: ClusterIP (accessed through Ingress)
- **Database**: ClusterIP (internal only)
- **Cache (Redis)**: ClusterIP (internal only)
- **Admin dashboard**: NodePort during development, Ingress in production

**Service Discovery Flow**:
1. Application queries: `backend-api.default.svc.cluster.local`
2. CoreDNS resolves to service ClusterIP (e.g., 10.96.0.50)
3. kube-proxy maintains iptables rules: "Traffic to 10.96.0.50:8080 → distribute to pod IPs"
4. Connection reaches one of the ready pods behind the service

**Common Confusion**: "Service IP isn't assigned to any interface. It's a virtual IP managed by kube-proxy through iptables or IPVS rules. You can't ping a service IP, but you CAN connect to service ports."

### 6. Ingress Controllers: L7 Routing & TLS (4 min)

**Why Ingress Exists**:
Problem: You have 20 microservices, each needs external access. Without Ingress: 20 LoadBalancer services = 20 cloud load balancers = $300-600/month. With Ingress: 1 LoadBalancer for Ingress controller + path-based routing = $15-30/month.

**What Ingress Provides**:
- **L7 routing**: Host-based (api.example.com, app.example.com) and path-based (/api, /static)
- **TLS termination**: HTTPS handled by ingress, backends use HTTP
- **Load balancing**: Distributes traffic across service pods
- **Single entry point**: One cloud load balancer for many services

**Ingress Controller Comparison**:

**Nginx Ingress Controller**:
- **Pros**: Most popular, battle-tested, extensive features, good docs
- **Cons**: Resource-heavy for large configs, reload on every change
- **Use case**: General-purpose, works everywhere

**Traefik**:
- **Pros**: Built-in Let's Encrypt support, dynamic config (no reloads), modern dashboard
- **Cons**: Less battle-tested at scale
- **Use case**: Teams wanting automatic TLS certificates

**Cloud-native (ALB Ingress, GCP GCLB)**:
- **Pros**: Integrates with cloud LB features (WAF, DDoS protection), no in-cluster resources
- **Cons**: Cloud-specific, more expensive, less portable
- **Use case**: Heavy cloud integration, need WAF/DDoS

**Decision**: "For most teams: Nginx. It works, it's proven, troubleshooting resources are abundant."

**TLS Termination with cert-manager**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - api.example.com
    secretName: api-example-tls  # cert-manager creates this
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backend-api
            port:
              number: 8080
```

**How it works**:
1. cert-manager watches for Ingress with annotation
2. Requests certificate from Let's Encrypt via ACME protocol
3. Stores cert in Kubernetes Secret
4. Ingress controller mounts Secret, terminates TLS
5. Auto-renewal 30 days before expiration

**Common Issues & Debugging**:

**502 Bad Gateway**:
- Meaning: Ingress can't reach backend pods
- **Debug steps**:
  1. Check service exists: `kubectl get svc backend-api`
  2. Check service has endpoints: `kubectl get endpoints backend-api` (should show pod IPs)
  3. Check pods are ready: `kubectl get pods -l app=backend-api` (look for Running + Ready 1/1)
  4. Test from ingress pod: `kubectl exec -n ingress-nginx <pod> -- curl backend-api.default.svc:8080`

**TLS Handshake Failures**:
- Check cert-manager: `kubectl get certificate -A` (status should be True)
- Check certificate details: `kubectl describe certificate api-example-tls`
- Check cert-manager logs: `kubectl logs -n cert-manager deploy/cert-manager`
- Common cause: DNS not pointing to ingress IP during challenge

**Wrong Backend**:
- Check ingress rules: `kubectl describe ingress app-ingress`
- Check paths match exactly (trailing slashes matter!)
- Check host headers if using host-based routing

### 7. Service Mesh: When Complexity is Worth It (3.5 min)

**What Service Mesh Provides**:
Think of service mesh as a "network layer for microservices." It adds:
1. **Observability**: Automatic metrics for every service call (latency, error rates, traffic)
2. **Security**: mTLS between services without changing application code
3. **Traffic Management**: Canary deployments, circuit breakers, retries, timeouts
4. **Reliability**: Automatic retries, failover, load balancing algorithms

**The Cost of Complexity**:
- Sidecar per pod (resource overhead: ~50MB RAM, 0.1 CPU per sidecar)
- Operational complexity (new failure modes, debugging harder)
- Learning curve (Istio especially - massive API surface)
- Performance overhead (every request goes through sidecar proxy)

**Analogy**: "Service mesh is like hiring a personal assistant for every employee. Sounds great - they handle scheduling, screening calls, managing communications. But now you have 2x the people, 2x the potential for miscommunication, and complexity scales quadratically."

**Istio vs Linkerd Trade-offs**:

**Istio**:
- **Pros**: Feature-rich, handles complex scenarios, extensive traffic management, integrates with everything
- **Cons**: Steep learning curve, resource-heavy, complex to troubleshoot
- **Best for**: Large organizations, complex multi-cluster setups, need advanced features

**Linkerd**:
- **Pros**: Lightweight, easy to operate, fast, good defaults, simple mental model
- **Cons**: Fewer advanced features, smaller ecosystem
- **Best for**: Teams wanting mTLS + observability without Istio's complexity

**When You DON'T Need Service Mesh**:
- **< 20 microservices**: Overhead outweighs benefits
- **Simple architecture**: Monolith or few services
- **Good existing observability**: Already have Prometheus + distributed tracing
- **No compliance requirements**: Don't need mTLS everywhere

**When You DO Need Service Mesh**:
- **Compliance requires mTLS**: Healthcare, finance, government
- **50+ microservices**: Observability gap without it
- **Complex traffic routing**: Canary deployments, multi-cluster failover
- **Zero-trust networking**: Every service call authenticated

**Decision Framework**:
"Start without service mesh. Add observability with Prometheus + Jaeger. Add network policies for isolation. If you hit limits - can't get metrics granularity, can't implement mTLS easily, can't do advanced traffic routing - THEN evaluate service mesh. Don't add it because it's cool. Add it because you have a problem it solves."

**Network Policies Without Service Mesh**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```
This allows ONLY frontend pods to reach backend pods on port 8080. Default deny otherwise.

### 8. Active Recall Practice (1.5 min)

**Pause and answer these questions**:

1. "Your pods can't reach a service. Walk through your debugging approach step by step." [PAUSE 5 sec]

2. "You're deploying a new app. It needs external HTTPS access. Would you use NodePort, LoadBalancer, or Ingress? Why?" [PAUSE 4 sec]

3. "Your company asks you to implement a service mesh. What questions do you ask first to determine if it's actually needed?" [PAUSE 4 sec]

**Answers**:

1. **Service connectivity debugging**:
   - Check if service exists: `kubectl get svc service-name`
   - Check if service has endpoints: `kubectl get endpoints service-name` (should show pod IPs)
   - If no endpoints: pods aren't ready, check readiness probes
   - If has endpoints: test DNS from failing pod: `kubectl exec pod -- nslookup service-name`
   - If DNS works but connection fails: check network policies, check CNI logs

2. **External HTTPS app**:
   - Use Ingress with TLS termination, NOT NodePort or LoadBalancer service
   - NodePort exposes on every node (security risk, no TLS termination)
   - LoadBalancer works but costs more ($15-30/month per service vs one ingress controller)
   - Ingress provides L7 routing, TLS with cert-manager, single entry point

3. **Service mesh evaluation questions**:
   - How many microservices? (< 20 = probably don't need)
   - Do you have compliance requirements for mTLS? (yes = strong case)
   - What's your current observability? (if already have Prometheus + tracing, less urgent)
   - What problem are you trying to solve? (if answer is "everyone else has it" = don't do it)
   - Do you have capacity to operate it? (Istio especially needs dedicated expertise)

### 9. Recap & Synthesis (2 min)

**Key Takeaways**:
1. **Kubernetes networking model**: Flat namespace, every pod gets IP, no NAT required. CNI plugins handle pod-to-pod connectivity.
2. **Service types**: ClusterIP for internal (80% of services), LoadBalancer for production external access, NodePort for dev/testing only, ExternalName for DNS aliases.
3. **Ingress controllers**: L7 routing + TLS termination. One LoadBalancer serves many services via path/host routing. Use cert-manager for automatic Let's Encrypt certificates.
4. **Service mesh**: Don't start with it. Add when you have concrete problems: need mTLS everywhere, 50+ microservices, complex traffic routing. Linkerd for simplicity, Istio for features.
5. **Common failures**: Pods without IPs = CNI issue. Services without endpoints = pod readiness issue. 502 from Ingress = backend not reachable. TLS failures = cert-manager or DNS issues.

**Connection to Episode 5**: "Remember StatefulSet DNS names? Now you understand HOW that DNS resolution works. CoreDNS resolves the name, kube-proxy routes traffic, CNI delivers packets."

**Connection to Episode 4**: "The troubleshooting workflow from Episode 4 - describe, logs, events - applies to networking too. Describe service, check endpoints, review ingress events."

**Connection to Episode 1**: "Episode 1's production failure pattern #4 was networking. Today you learned the tools to prevent and debug those failures: proper Service selection, Ingress configuration, network policies."

**Looking Ahead**: "In Episode 7, we're tackling observability - metrics, logging, and tracing. You'll learn how to monitor those Service endpoints, track request latency through Ingress, and see exactly where traffic is going. The networking knowledge from today is foundation for understanding what to monitor."

### 10. Next Episode Preview (30 sec)

"Next time: **Observability - Metrics, Logging, and Tracing**. You'll learn:
- How to set up production-ready Prometheus with persistent storage
- Log aggregation strategies with Loki or ELK
- Distributed tracing to debug microservice request flows
- The four golden signals: latency, traffic, errors, saturation

This builds directly on today's networking concepts. You'll monitor those Ingress endpoints for response times, track pod-to-pod network latency, and see service mesh observability in action (for teams that need it)."

---

## Supporting Materials

### Code Examples
1. **Example 1**: Complete Ingress with TLS using cert-manager
2. **Example 2**: NetworkPolicy for production isolation
3. **Example 3**: Service type examples (ClusterIP, LoadBalancer, ExternalName)

### Technical References
- **Kubernetes Networking Documentation**: Core concepts and CNI spec
- **CNI Plugin Comparison**: Calico, Cilium, Flannel, Weave features
- **cert-manager Documentation**: Automatic TLS certificate management
- **Istio vs Linkerd Comparison**: Trade-offs and decision criteria

### Analogies Used
1. **Office phone extensions**: Traditional networking vs Kubernetes flat namespace
2. **Personal assistant per employee**: Service mesh overhead
3. **Virtual IP as abstraction**: Service ClusterIP explained

### Debugging Workflows
1. **Service connectivity**: Service exists → endpoints exist → pods ready → network policies
2. **Ingress 502**: Service exists → endpoints → pod readiness → path matching
3. **TLS failures**: Certificate status → DNS validation → cert-manager logs

---

## Quality Checklist

### Structure
- [x] Clear beginning (callback to Episode 5 DNS) / middle (networking layers) / end (synthesis)
- [x] Logical flow: networking model → CNI → Services → Ingress → service mesh
- [x] Time allocations realistic (total: 18 minutes)
- [x] All sections specific with concrete examples

### Pedagogy
- [x] Objectives specific/measurable (explain model, choose service type, determine service mesh value)
- [x] Spaced repetition integrated (callbacks to Ep 1, 4, 5; previews to Ep 7, 9, 10)
- [x] Active recall included (3 practice questions with pauses)
- [x] Signposting clear (networking layers, debugging workflows)
- [x] 3 analogies/metaphors (phone extensions, personal assistant, virtual IP)
- [x] Pitfalls addressed (when NOT to use service mesh, common debugging mistakes)

### Content
- [x] Addresses pain points (502 errors, TLS failures, service mesh over-engineering)
- [x] Production-relevant examples (e-commerce architecture, cost comparison)
- [x] Decision frameworks (CNI selection, Service type, Ingress controller, service mesh)
- [x] Troubleshooting included (systematic debugging workflows)
- [x] Appropriate depth for senior engineers (CNI internals, iptables/IPVS, L7 routing)

### Engagement
- [x] Strong hook (Episode 5 callback + networking failure pattern)
- [x] Practice/pause moments (3 active recall questions)
- [x] Variety in techniques (analogy, comparison tables, think-aloud, decision frameworks)
- [x] Preview builds anticipation (observability of network metrics in Episode 7)

---

## Notes for Script Writing

**Tone**: Conversational but authoritative. "Here's what trips people up" rather than "Users often struggle."

**Pacing**:
- Slow down for networking model (fundamental concept)
- Speed up for kubectl commands (assume familiarity from Episode 4)
- Pause before active recall questions (give thinking time)

**Emphasis Points**:
- "This is CRITICAL" → Flat network namespace model
- "Here's what trips people up" → Service mesh over-engineering
- "Let me be clear" → When NOT to use service mesh

**Callback Phrases**:
- "Remember Episode 5 when we learned about DNS names..."
- "This connects to Episode 4's troubleshooting workflow..."
- "In Episode 7, you'll see how to monitor these endpoints..."

**Troubleshooting Mindset**: Model the systematic debugging process with think-alouds, not just commands.

**Cost Awareness**: Emphasize cost implications (20 LoadBalancers vs 1 Ingress, service mesh resource overhead).
