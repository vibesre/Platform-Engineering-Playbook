---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 #06: Networking & Services"
slug: /courses/kubernetes-production-mastery/lesson-06
---

# Lesson 6: Networking & Services

## Kubernetes Production Mastery Course

<GitHubButtons />

<iframe width="560" height="315" src="https://www.youtube.com/embed/z1SR4LlWcx0" title="Lesson 6: Networking & Services - Kubernetes Production Mastery" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

**Course**: [Kubernetes Production Mastery](/courses/kubernetes-production-mastery)
**Episode**: 6 of 10
**Duration**: ~18 minutes
**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

## Learning Objectives

By the end of this lesson, you'll be able to:
- Understand the Kubernetes flat network model and choose between CNI plugins (Calico, Cilium, Flannel)
- Select the right Service type (ClusterIP, NodePort, LoadBalancer, ExternalName) for your use case
- Configure Ingress controllers with TLS termination and determine when a service mesh is actually needed

## Prerequisites

- [Lesson 1: Production Mindset](./lesson-01)
- [Lesson 2: Resource Management](./lesson-02)
- [Lesson 3: Security Foundations](./lesson-03)
- [Lesson 4: Health Checks & Probes](./lesson-04)
- [Lesson 5: Stateful Workloads](./lesson-05)

---

## Transcript

Welcome to Episode 6 of Kubernetes Production Mastery. In Episode 5, we learned about StatefulSets and stable DNS names. You saw addresses like postgres-0.postgres.default.svc.cluster.local. We said pods could always reach each other using these names. But we didn't explain how. How does that DNS resolution actually work? And what happens when pods can't reach each other?

Before we continue, try to recall from Episode 1: What was networking failure pattern number four? That's right - network segmentation and connectivity issues. Pods that should talk to each other but can't. This is the number four cause of production outages.

Today we're diving deep into Kubernetes networking. By the end, you'll understand the networking model, how to choose the right Service type, how Ingress controllers work, and when you actually need a service mesh. Plus, how to debug the most common networking failures.

### The Flat Network Model

Kubernetes networking is built on one fundamental assumption: all pods can communicate with all other pods without NAT. Every pod gets its own IP address. This is called the flat network namespace model. And it's different from everything you might be used to.

Think about traditional Docker networking. Containers share the host network. Port conflicts everywhere. You have to map container port 8080 to host port 30080 because 8080 is already taken. Service discovery becomes a nightmare of keeping track of which ports on which hosts. Load balancing? Manual.

Kubernetes flips this completely. Every pod gets its own IP. Containers inside that pod share the IP, so port conflicts only happen within a pod. No port mapping complexity. If your container listens on 8080, the pod listens on 8080, and the service routes to 8080. Clean.

Here's a mental model that helped me. Think of traditional networking like a huge office building where everyone shares phone extensions. You have to remember "Sales is extension 1234, Engineering is 5678." Kubernetes is like giving everyone their own direct phone number. You just call their number. No extensions. No switchboard confusion.

### Network Layers

Now, this networking happens in layers, and understanding which layer handles what is critical. Most networking issues happen because people don't understand this. At the bottom, you have pod-to-pod communication. That's the CNI plugin's responsibility. Above that, you have Services - the stable abstraction layer managed by kube-proxy. Then Ingress for L7 routing and TLS termination. And optionally, service mesh for advanced traffic management. Each layer has a specific job.

### CNI Plugins

Let's start at the foundation. CNI - Container Network Interface. This is what assigns IP addresses to pods, sets up network routes so pods can talk, and enforces network policies if the plugin supports it. Here's what's important: CNI is a specification, not an implementation. Many different plugins exist.

The most common ones? Calico is popular for production clusters needing strong network isolation. It does network policy enforcement, uses BGP routing for large scale, and has excellent performance. The complexity is medium - you need some networking knowledge to troubleshoot when things break.

Cilium is the modern choice. It's eBPF-based, which means kernel-level networking and blazing fast performance. It gives you L7 visibility without a traditional service mesh. But it requires recent kernels, and the complexity is higher.

Flannel is the simple option. Easy to set up, just works, good for basic clusters. If you're doing development, testing, or simple production without complex policy requirements, Flannel is fine. Low complexity.

Weave has encryption built in and creates a simple mesh overlay. Good for multi-cloud scenarios where you need encryption between nodes. Medium complexity.

Here's my decision framework. Do you need network policies for isolation? Then Calico or Cilium. Want cutting-edge performance and L7 visibility? Cilium. Just need basic networking that works? Flannel. Need built-in encryption between nodes? Weave.

### Debugging CNI Issues

When CNI breaks, here's what you see. Pods can schedule and run, but they can't reach each other or services. The first thing I check: do the pods have IPs? kubectl get pods with the wide output. If pods don't have IPs, that's a CNI failure. Check the CNI daemon pods in kube-system namespace. Look for calico, cilium, or flannel pods. Check their logs.

Let me walk through a real debugging scenario. I see a pod stuck in Running state but the app logs show "connection refused" to another service. My thought process: Is this DNS? Networking? First, I check if the pod has an IP. kubectl get pod with wide output. It does. So CNI assigned the IP. Next, can the pod resolve DNS? kubectl exec into the pod and nslookup kubernetes.default. It can. So DNS works. Now I test direct connectivity. kubectl exec and curl service-name on port 8080. Connection refused.

Ah! The destination service exists but the pods behind it aren't ready. I check with kubectl get endpoints service-name. Empty. No pods ready. This isn't a networking issue. This is a readiness probe issue. The pods aren't passing their health checks, so they're not added to the service endpoints. See how understanding the layers helps you debug?

### Service Types

Now let's talk about Services. Why do they exist? Because pods are ephemeral. IP addresses change. You can't hardcode pod IPs in your application. Services provide stable virtual IPs and DNS names.

There are four service types, and choosing the right one matters. ClusterIP is the default. It's for internal cluster communication only. Your backend services, databases, internal APIs - these are all ClusterIP. Access is only from within the cluster. The DNS name is service-name.namespace.svc.cluster.local. About 80% of your services will be ClusterIP.

NodePort exposes the service on every node's IP at a static port in the 30000 to 32767 range. This is useful for development and testing. Quick external access without setting up a load balancer. But don't use it in production. Every node exposes the port. There's no SSL termination. The port range is limited. It's fine for on-prem clusters without LoadBalancer support, or if you have specific firewall requirements. But generally, avoid it in production.

LoadBalancer provisions a cloud load balancer. AWS ELB, GCP load balancer, Azure load balancer. This is for production external services. But here's the cost issue: each LoadBalancer service creates a separate cloud load balancer. Fifteen to thirty dollars per month, per service. If you have 20 external services, that's 300 to 600 dollars a month in load balancer costs alone. There's a better way.

ExternalName is a DNS alias. It returns a CNAME record to an external service. No proxying. This is useful for gradual migrations or accessing external APIs through the service abstraction. Your legacy database is outside the cluster? Create an ExternalName service pointing to it. Your apps use the service name, and you can eventually swap in a ClusterIP service when you migrate the database inside.

### Real Production Architecture

Let me give you a real production architecture. E-commerce platform. The frontend could use a LoadBalancer service, but we're going to do better with Ingress in a minute. Backend API is ClusterIP, accessed through Ingress. Database is ClusterIP, internal only. Cache layer - Redis - ClusterIP, internal only. Admin dashboard uses Ingress in production, though you might use NodePort during development.

### Service Discovery

Here's how service discovery actually works. Your application queries backend-api.default.svc.cluster.local. CoreDNS resolves this to the service ClusterIP, something like 10.96.0.50. Now, that IP isn't assigned to any interface. It's a virtual IP managed by kube-proxy through iptables or IPVS rules. When traffic hits 10.96.0.50 on port 8080, kube-proxy distributes it to the actual pod IPs behind the service. The connection reaches one of the ready pods.

Common confusion: you can't ping a service IP. It's virtual. But you can connect to service ports. The IP only responds to configured ports, not ICMP ping.

### Ingress Controllers

Now we get to Ingress, and this is where things get interesting. Here's the problem: you have 20 microservices that need external access. Without Ingress, you'd create 20 LoadBalancer services. Twenty cloud load balancers. Three hundred to six hundred dollars a month. With Ingress, you create one LoadBalancer for the Ingress controller, and use path-based or host-based routing to reach all 20 services. Fifteen to thirty dollars a month total.

What does Ingress give you? L7 routing - that's application layer routing. Host-based: api.example.com goes to one service, app.example.com goes to another. Path-based: requests to /api go to the backend service, requests to /static go to the file server. TLS termination - HTTPS is handled by the Ingress controller, and backends can use plain HTTP. Load balancing across service pods. And a single entry point for multiple services.

The most popular Ingress controller is Nginx. Battle-tested, extensive features, good documentation. The downside is it's resource-heavy for large configurations, and it reloads on every change. But it's proven at scale. Most teams should start here.

Traefik has built-in Let's Encrypt support, dynamic configuration with no reloads, and a modern dashboard. It's less battle-tested at massive scale, but great for teams wanting automatic TLS certificates.

Cloud-native options like ALB Ingress for AWS or GCLB for GCP integrate directly with cloud load balancer features. You get WAF, DDoS protection, and other cloud-native capabilities. But they're cloud-specific, more expensive, and less portable. Use them if you need deep cloud integration.

For most teams? Nginx. It works, it's proven, and troubleshooting resources are abundant.

### TLS with cert-manager

Let's talk about TLS termination with cert-manager. You add an annotation to your Ingress resource: cert-manager.io/cluster-issuer: letsencrypt-prod. You specify the TLS host and the secret name where the certificate should be stored. Cert-manager watches for Ingress resources with this annotation, requests a certificate from Let's Encrypt using the ACME protocol, stores it in a Kubernetes Secret, and the Ingress controller mounts that Secret to terminate TLS. Auto-renewal happens 30 days before expiration. Set it up once, forget about it.

### Debugging Ingress Issues

Now for debugging common Ingress issues. The dreaded 502 Bad Gateway. This means the Ingress controller can't reach the backend pods. Here's my debugging workflow. First, does the service exist? kubectl get service backend-api. Yes. Does the service have endpoints? kubectl get endpoints backend-api. This should show pod IPs. If it's empty, the pods aren't ready. Check with kubectl get pods and look for Running and Ready status. If the endpoints exist but you still get 502, test connectivity from the Ingress pod. kubectl exec into the ingress-nginx pod and curl the backend service. This tells you if the Ingress controller can actually reach the service.

TLS handshake failures are usually cert-manager or DNS issues. Check if the certificate was issued: kubectl get certificate across all namespaces. The status should be True. If it's not, describe the certificate resource to see what failed. Check cert-manager logs. Common cause: DNS isn't pointing to the Ingress IP during the ACME challenge, so Let's Encrypt can't validate you own the domain.

Wrong backend serving requests usually means your Ingress rules don't match. Check the Ingress rules with kubectl describe ingress. Pay attention to paths - trailing slashes matter! If you're using host-based routing, make sure your DNS and host headers match.

### Service Mesh: Do You Need It?

Alright, service mesh. This is where I see a lot of over-engineering. Let me be clear about what service mesh provides. Think of it as a network layer for microservices. It adds automatic observability - metrics for every service call, latency, error rates, traffic. Security through mTLS between services without changing application code. Traffic management for canary deployments, circuit breakers, retries, timeouts. And reliability features like automatic retries and failover.

But there's a cost. Every pod gets a sidecar proxy. That's about 50 megabytes of RAM and 0.1 CPU per sidecar. Multiply that by hundreds of pods. The operational complexity is significant. New failure modes. Debugging becomes harder because now you're troubleshooting proxies in addition to your application. Learning curve is steep, especially with Istio. And there's performance overhead - every request goes through the sidecar.

Here's an analogy. Service mesh is like hiring a personal assistant for every employee. Sounds great - they handle scheduling, screen calls, manage communications. But now you have twice the people, twice the potential for miscommunication, and complexity scales quadratically.

### Istio vs Linkerd

Istio versus Linkerd. Istio is feature-rich. It handles complex scenarios, extensive traffic management, integrates with everything. But the learning curve is steep, it's resource-heavy, and complex to troubleshoot. Best for large organizations with complex multi-cluster setups that need advanced features.

Linkerd is lightweight, easy to operate, fast, has good defaults, and a simple mental model. Fewer advanced features, smaller ecosystem. Best for teams wanting mTLS and observability without Istio's complexity.

### When to Use Service Mesh

When you don't need service mesh: fewer than 20 microservices - the overhead outweighs the benefits. Simple architecture like a monolith or a few services. You already have good observability with Prometheus and distributed tracing. No compliance requirements for mTLS everywhere.

When you do need service mesh: compliance requires mTLS - healthcare, finance, government. Fifty or more microservices create an observability gap without it. Complex traffic routing needs like canary deployments or multi-cluster failover. Zero-trust networking where every service call must be authenticated.

My advice? Start without service mesh. Add observability with Prometheus and Jaeger. Add network policies for isolation. If you hit limits - can't get metrics granularity, can't implement mTLS easily, can't do advanced traffic routing - then evaluate service mesh. Don't add it because it's cool. Add it because you have a specific problem it solves.

### Network Policies

You can get decent isolation without service mesh using network policies. These let you specify which pods can talk to which other pods. You define a NetworkPolicy that says "backend pods can only receive traffic from frontend pods on port 8080." Default deny everything else. This is enforced by your CNI plugin if it supports network policies - Calico and Cilium do.

### Active Recall Quiz

Let's pause for some active recall. Answer these questions.

Your pods can't reach a service. Walk through your debugging approach step by step.

You're deploying a new app. It needs external HTTPS access. Would you use NodePort, LoadBalancer, or Ingress? Why?

Your company asks you to implement a service mesh. What questions do you ask first to determine if it's actually needed?

**Answers:**

For service connectivity debugging: First, check if the service exists with kubectl get service. Second, check if the service has endpoints with kubectl get endpoints. If there are no endpoints, the pods aren't ready - check readiness probes. If there are endpoints, test DNS from the failing pod with kubectl exec and nslookup. If DNS works but the connection fails, check network policies and CNI logs.

For external HTTPS access: Use Ingress with TLS termination, not NodePort or LoadBalancer. NodePort exposes on every node which is a security risk and doesn't do TLS termination. LoadBalancer works but costs more - fifteen to thirty dollars per month per service versus one Ingress controller for everything. Ingress provides L7 routing, TLS with cert-manager, and a single entry point.

For service mesh evaluation: How many microservices do you have? If fewer than 20, you probably don't need it. Do you have compliance requirements for mTLS? If yes, that's a strong case. What's your current observability like? If you already have Prometheus and tracing, it's less urgent. What problem are you trying to solve? If the answer is "everyone else has it," don't do it. Do you have capacity to operate it? Istio especially needs dedicated expertise.

### Key Takeaways

Let's recap. The Kubernetes networking model is a flat namespace where every pod gets its own IP and no NAT is required. CNI plugins handle pod-to-pod connectivity. You have four service types: ClusterIP for internal communication - that's 80% of your services. LoadBalancer for production external access. NodePort for development and testing only. ExternalName for DNS aliases to external services.

Ingress controllers provide L7 routing and TLS termination. One LoadBalancer serves many services through path-based or host-based routing. Use cert-manager for automatic Let's Encrypt certificates. Don't pay for twenty load balancers when one Ingress controller will do.

Service mesh? Don't start with it. Add it when you have concrete problems: you need mTLS everywhere, you have 50-plus microservices, you need complex traffic routing. Linkerd if you want simplicity. Istio if you need all the features.

Common failures to remember: Pods without IPs means CNI issues. Services without endpoints means pod readiness issues. 502 errors from Ingress means backend not reachable. TLS failures are usually cert-manager or DNS problems.

Remember Episode 5's StatefulSet DNS names? Now you understand how that DNS resolution works. CoreDNS resolves the name, kube-proxy routes the traffic, CNI delivers the packets. It all fits together.

Episode 4's troubleshooting workflow - describe, logs, events - applies to networking too. Describe the service, check the endpoints, review Ingress events. Same systematic approach.

Episode 1's production failure pattern number four was networking. Today you learned the tools to prevent and debug those failures: proper Service selection, Ingress configuration, network policies.

### Next Episode

Next time, we're tackling observability - metrics, logging, and tracing. You'll learn how to set up production-ready Prometheus with persistent storage, log aggregation with Loki or ELK, and distributed tracing to debug microservice request flows. The four golden signals: latency, traffic, errors, saturation. This builds directly on today's networking concepts. You'll monitor those Ingress endpoints for response times, track pod-to-pod network latency, and see service mesh observability in action for teams that need it. See you then.

---

## Navigation

⬅️ **Previous**: [Lesson 5: Stateful Workloads](./lesson-05) | **Next**: [Lesson 7: Observability](./lesson-07) ➡️

📚 **[Back to Course Overview](/courses/kubernetes-production-mastery)**
