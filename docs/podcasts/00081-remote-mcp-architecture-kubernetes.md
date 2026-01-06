---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #081: Remote MCP on Kubernetes"
slug: 00081-remote-mcp-architecture-kubernetes
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #081: Remote MCP Architecture - Running AI Tool Servers on Kubernetes

<GitHubButtons />

**Duration**: 21 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Platform engineers, DevOps professionals, infrastructure architects evaluating MCP/AI infrastructure

> 🔗 **Related Episode**: [Episode #074: Agentic AI Foundation - MCP for Platform Engineers](/podcasts/00074-agentic-ai-foundation-mcp-platform-engineers) covered MCP fundamentals. This episode focuses on production Kubernetes deployment.

---

The MCP server registry hit 10,000+ integrations, but most teams are running these servers on laptops. This episode breaks down the production architecture that Google, Red Hat, and AWS are converging on: remote MCP servers deployed on Kubernetes.

## Key Takeaways

| Takeaway | Details |
|----------|---------|
| **Remote MCP is production MCP** | Local stdio mode is for experimentation; team-scale access requires HTTP/SSE mode |
| **Native beats wrapper** | Direct Kubernetes API implementations outperform kubectl subprocess approaches |
| **Security is solvable** | ServiceAccounts, TokenRequest API, RBAC, --read-only mode, audit logging |
| **Platform teams own this** | MCP infrastructure is becoming standard platform responsibility |
| **Hybrid approach wins** | Managed MCP for cloud services; self-hosted for internal tools |

## Three Deployment Patterns

### Pattern 1: Local stdio (Development Only)
- MCP server as subprocess of AI client
- Direct stdin/stdout communication
- Use case: Individual experimentation

### Pattern 2: Remote HTTP/SSE (Team Scale)
- MCP server as Kubernetes deployment
- HTTP endpoint with Server-Sent Events for async
- Enables proper RBAC, audit logging, shared access

### Pattern 3: Managed Remote (Google's Model)
- Cloud provider hosts MCP servers
- Available: GKE, BigQuery, GCE, Maps
- Coming: Cloud Run, SQL, Spanner, Logging

## Defense-in-Depth Security

| Layer | Implementation |
|-------|----------------|
| **1. ServiceAccounts** | Dedicated accounts per use case (mcp-readonly, mcp-deployer) |
| **2. Time-bound Tokens** | TokenRequest API with 2-4 hour expiration |
| **3. RBAC** | Namespace-scoped Roles with minimum permissions |
| **4. Server Modes** | --read-only, --disable-destructive flags |
| **5. Audit Logging** | K8s API server logs + application-level logging |

## Implementation Roadmap

| Quarter | Actions |
|---------|---------|
| **Q1 2026** | Experiment: Deploy Red Hat MCP server in dev, --read-only mode, dedicated ServiceAccount |
| **Q2 2026** | Adopt: HTTP/SSE mode in staging, build first internal MCP server, establish audit logging |
| **Q3 2026** | Scale: Production deployment, multiple MCP servers by use case, team training |

## Resources

- [GitHub - containers/kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) - Red Hat's native Go implementation
- [Google Cloud MCP Documentation](https://docs.cloud.google.com/mcp/overview) - Managed remote MCP servers
- [Red Hat Developer - Kubernetes MCP Server](https://developers.redhat.com/articles/2025/09/25/kubernetes-mcp-server-ai-powered-cluster-management)

---

## Full Transcript

**Alex**: Welcome to the Platform Engineering Playbook Daily Podcast. A deep dive to help you stay ahead in platform engineering.

**Jordan**: The MCP server registry just hit ten thousand integrations. But here's the problem—most teams are still running these servers on laptops.

**Alex**: And that's the gap we're closing today. Remote MCP servers running on Kubernetes. Google announced managed endpoints in January. Red Hat open-sourced a production-grade implementation. AWS has an EKS-native server. This is becoming real infrastructure, not just developer toys.

**Jordan**: We'll cover the three deployment patterns, the security model that actually works, and why your platform team should own this infrastructure by Q2. If you listened to Episode seventy-four on the Agentic AI Foundation, this is the production follow-up.

**Alex**: Let's start with why remote matters at all. MCP's original design had servers running as subprocesses of the AI client. Direct stdin/stdout communication through what's called stdio transport. Works beautifully for a single developer experimenting with Claude or Cursor on their laptop.

**Jordan**: Right, that's the stdio mode. The server launches when you start the client, dies when you close it. No persistence, no sharing, no network involved.

**Alex**: And that design made sense for Anthropic's initial use case. They wanted Claude to connect to local tools without network complexity. But that's where it breaks down for teams. Picture this: you've got fifteen engineers using Cursor, all wanting to query your Kubernetes clusters through natural language. Each one running their own MCP server. Each one using their own kubeconfig with whatever permissions they happen to have.

**Jordan**: That's the "everyone's kubeconfig" problem. No centralized governance. No audit trail. And probably way more permissions than anyone actually needs.

**Alex**: Some of those kubeconfigs probably have cluster-admin because someone copy-pasted from a Stack Overflow answer during a production incident six months ago and never cleaned it up. Now every AI agent query runs with god mode.

**Jordan**: And you have no visibility into what those agents are doing.

**Alex**: Zero. Multiply that across your organization. The security team asks "what AI tools are accessing our production clusters?" and you have no answer. An auditor asks for access logs and you're pulling data from fifteen different developer laptops.

**Jordan**: So the industry recognized this. What changed?

**Alex**: Three things happened in quick succession. Google announced fully-managed remote MCP servers in January twenty twenty-six. They're not just connecting to Kubernetes—they're hosting the MCP servers themselves as managed services. Point your agent at their endpoint, done.

**Jordan**: What services did they cover?

**Alex**: GKE, BigQuery, Compute Engine, Google Maps initially. They're expanding to Cloud Run, Cloud SQL, Spanner, Cloud Logging. The vision is every Google Cloud service accessible through MCP.

**Jordan**: And Red Hat?

**Alex**: Red Hat took the self-hosted approach. They open-sourced a Kubernetes MCP server that you deploy yourself. The key feature is HTTP mode. Add the dash dash port flag, and it transforms from a local subprocess into a network service accepting HTTP requests.

**Jordan**: That's the architectural shift. From IPC to HTTP.

**Alex**: Exactly. And once it's HTTP, you can deploy it as a Kubernetes workload. Put it behind a Service. Add an Ingress. Integrate with your existing auth infrastructure. Run it in a namespace with proper RBAC.

**Jordan**: Let's break down the three deployment patterns because they represent genuinely different operational models with different trade-offs.

**Alex**: Pattern one: local stdio. Development only. This is what most people are doing today, and it's fine for what it is.

**Jordan**: How does it work technically?

**Alex**: The MCP server launches as a child process of your AI client. Claude Desktop, Cursor, whatever. Communication happens through standard input and output—literally writing to stdin and reading from stdout. The client and server share a process group.

**Jordan**: No network stack at all.

**Alex**: Right. Pure interprocess communication through file descriptors. The server inherits your shell environment, including any credentials you have. Your kubeconfig, your AWS credentials, everything.

**Jordan**: Use case?

**Alex**: Individual experimentation. Learning how MCP works. Prototyping integrations before building something production-grade. The moment you want to share it with anyone else, you've hit the wall.

**Jordan**: Pattern two: remote HTTP with Server-Sent Events. This is the team-scale architecture.

**Alex**: This is where it gets interesting for platform engineers. The MCP server runs as a Kubernetes deployment with an HTTP endpoint exposed through a Service. Clients connect via what's called Streamable HTTP. Request goes out over HTTP, server processes it, responses come back through Server-Sent Events.

**Jordan**: Why Server-Sent Events specifically?

**Alex**: Some MCP operations take time. You're running kubectl exec inside a pod, that might take thirty seconds. You're waiting for a Helm deployment to roll out, that could be minutes. SSE gives you streaming response capability—partial results, progress updates, final response—all over a single HTTP connection without forcing websockets everywhere.

**Jordan**: So the data flow is: AI client makes HTTP request to MCP server pod, MCP server pod calls Kubernetes API server, results stream back.

**Alex**: Exactly. And because the MCP server is now a pod in your cluster, you control its identity. It's not running as "developer X with their personal kubeconfig." It's running as a ServiceAccount you created with permissions you defined.

**Jordan**: The Red Hat implementation enables this with a single flag?

**Alex**: Dash dash port eighty eighty. That's it. Now you've got an HTTP server listening on port eighty eighty. Put it behind a Kubernetes Service, expose it however makes sense for your environment.

**Jordan**: Pattern three is Google's managed model. What's different?

**Alex**: With managed MCP, the cloud provider runs everything. You don't deploy any servers. You point your AI agents at Google's endpoint URL. They handle scaling, availability, updates, geographic distribution.

**Jordan**: What's the endpoint look like?

**Alex**: For GKE, something like docs.cloud.google.com/kubernetes-engine/docs/reference/mcp. Your agent discovers available tools through that endpoint, calls operations, gets responses. All the infrastructure is Google's problem.

**Jordan**: That's attractive from an operations standpoint.

**Alex**: Absolutely. No pods to manage, no upgrades to test, no capacity planning. But the trade-off is flexibility. You're locked into their implementation, their tool definitions, their feature roadmap. If you need custom behavior or have compliance requirements about where processing happens, managed might not work.

**Jordan**: Multi-cloud environments especially.

**Alex**: Right. If you're running clusters on GKE, EKS, and AKS, you probably don't want three different managed MCP paradigms. Self-hosting gives you consistency.

**Jordan**: Let's go deeper on the architecture. You mentioned wrapper-based versus native implementation.

**Alex**: This distinction really matters for production reliability. A wrapper-based MCP server—and there are several in the ecosystem—spawns kubectl or helm as a child process. It runs the command, captures the text output, parses it, reformats it for MCP, returns it to the client.

**Jordan**: That sounds like a shell script with extra steps.

**Alex**: It kind of is. And it carries all the problems of shell scripts. You've got latency from process spawning—fork, exec, wait for completion. Error handling is messy because you're parsing human-readable output that might change format between versions.

**Jordan**: Output parsing is fragile.

**Alex**: Extremely. Kubectl's output isn't meant to be machine-parsed. Tables change width based on content. Error messages vary. Localization might change strings. One kubectl upgrade and your regex breaks.

**Jordan**: And you need kubectl installed in the container.

**Alex**: Which adds dependencies, attack surface, and version management complexity. Does your MCP server container have the same kubectl version as your cluster? Probably not. Will that cause subtle bugs? Maybe.

**Jordan**: What's the native approach?

**Alex**: Native implementation means using the Kubernetes client library directly. Red Hat's server is written in Go, using client-go, the same library that kubectl itself uses internally. No subprocess. No text parsing. Direct API calls.

**Jordan**: Single binary distribution.

**Alex**: Right. They distribute a single static binary. No kubectl dependency, no helm dependency, no Python or Node runtime. Download the binary, run it. Works on Linux, Mac, Windows.

**Jordan**: They're explicit about this in their documentation.

**Alex**: Quote: "This is NOT just a wrapper around kubectl or helm command-line tools. It's a Go-based native implementation that interacts directly with the Kubernetes API server." That architectural choice gives you lower latency, type-safe operations, proper error handling, and fewer moving parts to break.

**Jordan**: Multi-cluster support is another production requirement.

**Alex**: Most organizations run more than one cluster. Production, staging, development at minimum. Often multiple production clusters for different regions or workloads.

**Jordan**: How does the Red Hat server handle that?

**Alex**: Multi-cluster is enabled by default. Your kubeconfig can define multiple contexts—different clusters, different credentials per cluster. Every MCP operation accepts an optional context parameter specifying which cluster to target.

**Jordan**: So one MCP server deployment can proxy to all your clusters?

**Alex**: If you configure it that way, yes. Single MCP server with a kubeconfig that has contexts for prod-us-east, prod-eu-west, staging, dev. The AI agent specifies context equals prod-us-east when making a request, and the server routes to that cluster.

**Jordan**: What about dynamic configuration changes?

**Alex**: If your kubeconfig changes—you add a new cluster, rotate credentials—send SIGHUP to the process. It reloads the configuration without restarting. No downtime to add or modify clusters.

**Jordan**: That's operationally nice for GitOps-managed kubeconfigs.

**Alex**: Exactly. Cluster credentials managed in Vault or external-secrets, kubeconfig updates automatically, MCP server picks up changes on signal.

**Jordan**: Let's talk security. This is where deployments will fail audits.

**Alex**: The fundamental tension is credentials. MCP servers need some level of access to be useful. But that access creates risk. How do you give agents enough capability to be helpful without giving them the keys to the kingdom?

**Jordan**: What does wrong look like?

**Alex**: Wrong looks like developers running MCP servers with their personal kubeconfig—the one with cluster-admin because they needed it for debugging once. Or a shared ServiceAccount token that never expires, copied into a dozen places. Or an MCP server in unrestricted mode because "we'll add security later."

**Jordan**: What does right look like?

**Alex**: Defense in depth with five distinct layers, each providing independent protection. Layer one: dedicated ServiceAccounts.

**Jordan**: Not personal credentials.

**Alex**: Never personal credentials for production MCP. Create ServiceAccounts specifically for MCP use. Name them clearly—mcp-cluster-readonly, mcp-helm-deployer, mcp-pod-debugger. One account per use case, not one account for everything.

**Jordan**: Minimum required permissions per account.

**Alex**: Exactly. mcp-cluster-readonly can list and get resources but not create, update, or delete. mcp-helm-deployer can manage Helm releases but nothing else. The blast radius of a compromised account is limited to its specific permissions.

**Jordan**: Layer two?

**Alex**: Time-bound tokens. The old model was long-lived ServiceAccount tokens stored as Secrets. Those never expire. If compromised, they're valid forever until manually rotated.

**Jordan**: The TokenRequest API changed that.

**Alex**: TokenRequest generates short-lived credentials. You specify a duration—two hours, four hours, whatever your policy requires. Token expires automatically. No manual rotation needed.

**Jordan**: Kubectl create token mcp-readonly dash dash duration equals two h.

**Alex**: That gives you a token valid for two hours. Mount it into your MCP server pod through a projected volume. Kubernetes handles automatic refresh before expiration. Even if someone extracts the token, it's garbage in a few hours.

**Jordan**: Layer three is RBAC enforcement.

**Alex**: Standard Kubernetes RBAC, but applied thoughtfully. Define Roles or ClusterRoles with exactly the permissions needed. Bind them to your MCP ServiceAccounts. Use namespace-scoped Roles when possible to limit blast radius.

**Jordan**: Example permissions?

**Alex**: For a read-only troubleshooting MCP server: get, list, watch on pods, deployments, services, events. No create, update, delete. For a deployment MCP server: get, list, watch, patch on deployments, but only in specific namespaces.

**Jordan**: Layer four is MCP server modes.

**Alex**: The server itself can enforce restrictions independent of RBAC. Dash dash read only prevents all write operations at the MCP layer. Even if RBAC would allow a delete, the server refuses.

**Jordan**: Belt and suspenders.

**Alex**: Exactly. Dash dash disable destructive is a middle ground—allows create operations but blocks update and delete. Useful for servers that should be able to deploy new things but not modify or remove existing resources.

**Jordan**: Layer five?

**Alex**: Audit logging. Every MCP operation should be logged and queryable. Google's managed servers use Cloud Audit Logging—every agent interaction recorded with timestamp, identity, operation, target, result.

**Jordan**: For self-hosted?

**Alex**: Two sources. The MCP server should log requests at the application level. And the Kubernetes API server audit logs capture the actual API calls the MCP server makes. Between those two, you can reconstruct exactly what any agent did.

**Jordan**: There's also Model Armor from Google.

**Alex**: That's defense against adversarial AI attacks. Indirect prompt injection specifically—where a malicious payload in data tricks the agent into executing unauthorized actions. Model Armor analyzes requests for attack patterns before execution.

**Jordan**: Still early?

**Alex**: Still early. But the threat model is real. AI agents with tool access are targets for prompt injection attacks. Defense will mature alongside the attack techniques.

**Jordan**: Let's move to implementation. Platform teams are going to own this. What are the deployment topology options?

**Alex**: Three options with different trade-offs. Option A: sidecar per namespace. Deploy an MCP server into each team's namespace. The server inherits namespace-scoped RBAC automatically—if the namespace has restricted permissions, so does the MCP server.

**Jordan**: Strong isolation between teams.

**Alex**: Very strong. Team A's MCP server can't see team B's resources unless you explicitly configure cross-namespace access. Security boundaries match organizational boundaries.

**Jordan**: Downsides?

**Alex**: Resource overhead. You're running N MCP servers instead of one, each consuming CPU and memory. Configuration drift is a risk—teams might customize their instances differently, leading to inconsistent behavior. And operational complexity—you're managing many deployments instead of one.

**Jordan**: Option B is centralized.

**Alex**: Central MCP gateway. Single deployment serving the whole organization. You route requests based on client identity—header injection, mTLS client certs, whatever your auth infrastructure supports. Apply team-specific RBAC through Kubernetes impersonation or separate ServiceAccounts selected per client.

**Jordan**: Operationally simpler.

**Alex**: One deployment to monitor, upgrade, scale. Consistent behavior across the organization. But larger blast radius if something goes wrong. And multi-tenant access control at the application layer adds complexity.

**Jordan**: Option C?

**Alex**: Hybrid, which is what I recommend for most organizations. Use managed MCP servers for standard cloud services—Google's GKE endpoint, AWS's EKS endpoint, whatever your provider offers. Let them handle that infrastructure.

**Jordan**: And self-host for custom needs.

**Alex**: Self-host MCP servers for internal platform tools, custom Kubernetes workflows, proprietary integrations. These are the things cloud providers can't manage for you anyway.

**Jordan**: What about observability for self-hosted servers?

**Alex**: Treat them like any production workload. Prometheus metrics—expose request counts, latency histograms, error rates on a /metrics endpoint. Most MCP server implementations support this or it's easy to add with middleware.

**Jordan**: Health checks?

**Alex**: Standard liveness and readiness probes. Liveness confirms the process is running. Readiness confirms it can actually reach the Kubernetes API server. If API connectivity is lost, readiness fails, Kubernetes stops routing traffic.

**Jordan**: Scaling?

**Alex**: Horizontal Pod Autoscaler based on request rate or CPU usage. MCP servers are stateless, so horizontal scaling is straightforward. For bursty workloads—everyone runs agents at 9 AM—autoscaling prevents overload.

**Jordan**: Versioning strategy?

**Alex**: Pin your MCP server versions explicitly. Don't run latest in production. The MCP spec is evolving. Server implementations add features, change behavior. Test upgrades in staging before production. Have rollback ready if something breaks.

**Jordan**: Implementation roadmap. What should teams do when?

**Alex**: Q1 twenty twenty-six, which is now: experiment. Deploy Red Hat's Kubernetes MCP server in a development cluster. Enable dash dash read only so nothing dangerous can happen while you learn. Test with one AI client that your team already uses—Cursor, Claude Desktop, Copilot.

**Jordan**: What should they specifically test?

**Alex**: Create a dedicated ServiceAccount with list and get permissions only. Configure the MCP server to use that account. Connect your AI client. Ask it to list pods, describe deployments, show events. Verify the experience, learn what works, find friction points.

**Jordan**: Q2?

**Alex**: Adopt. Promote to staging with HTTP/SSE mode enabled. This is when you're ready for team-scale access. Build your first internal MCP server—pick one platform tool that developers ask about frequently. Maybe your internal deployment system, your CI/CD pipeline, your cost dashboard.

**Jordan**: Establish governance.

**Alex**: Establish audit logging pipeline. Know where logs go, how long they're retained, who can query them. Document your security policy—what ServiceAccounts exist, what permissions they have, what's the process to request changes. Get security team buy-in before production.

**Jordan**: Q3?

**Alex**: Scale. Production deployment with proper RBAC. Multiple MCP servers for different use cases—read-only for troubleshooting, read-write for deployments, Helm-specific for chart management. Integration with existing observability—dashboards, alerts, runbooks.

**Jordan**: Training?

**Alex**: Training for teams consuming MCP services. They need to understand what's possible, what's restricted, how to authenticate. Platform engineering success isn't just building the infrastructure—it's enabling adoption.

**Jordan**: What should people explicitly avoid?

**Alex**: Don't run MCP servers with admin credentials, even "temporarily." Temporary becomes permanent faster than you think. Don't skip audit logging—you'll regret it when security asks questions or an incident happens.

**Jordan**: Other anti-patterns?

**Alex**: Don't deploy unrestricted mode in production. There's no good reason to allow delete operations through an AI agent unless you've thought very carefully about the failure modes. Don't ignore token expiration—long-lived credentials are technical debt that will bite you eventually.

**Jordan**: The pattern we're seeing is familiar.

**Alex**: It's the Kubernetes adoption curve compressed into months instead of years. Kubernetes started as developer convenience—run containers without VMs. Became standard infrastructure requiring platform team ownership. MCP is following the same trajectory, just faster because organizations already have the operational muscle from Kubernetes.

**Jordan**: Platform teams that build MCP expertise now will be ahead.

**Alex**: When MCP becomes the expected protocol for AI tool integration—and it will—you want to be the team that already has production-grade infrastructure, not the team scrambling to catch up.

**Jordan**: Key takeaways.

**Alex**: First, remote MCP is production MCP. Local stdio is for experimentation only. The moment you need team access, shared governance, or audit trails, you need HTTP mode with proper infrastructure.

**Jordan**: Second?

**Alex**: Native beats wrapper. Direct Kubernetes API implementation avoids the fragility of kubectl subprocess parsing. Look for MCP servers built on client libraries, not command-line wrappers.

**Jordan**: Third?

**Alex**: Security is solvable with standard patterns. Dedicated ServiceAccounts, Kubernetes RBAC, time-bound tokens from TokenRequest API, audit logging through API server logs. Nothing exotic—just Kubernetes security applied correctly.

**Jordan**: Fourth?

**Alex**: Platform teams own this. MCP infrastructure is becoming standard platform responsibility. The teams that establish patterns now set organizational norms. The teams that wait inherit someone else's quick hack.

**Jordan**: Fifth?

**Alex**: Hybrid approach wins. Managed MCP for commodity cloud services—let providers handle their own tools. Self-hosted for internal tools and custom workflows where you need control.

**Jordan**: This connects back to Episode seventy-four.

**Alex**: That episode covered the foundation—what MCP is, what the Agentic AI Foundation means, why the N times M to N plus M simplification matters. This episode is the production implementation. The simplification only works if the servers are reliable, secure, and operated professionally.

**Jordan**: MCP is infrastructure now.

**Alex**: Treat it that way. Same rigor you apply to Kubernetes clusters, apply to MCP servers. Same observability, same security review, same change management.

**Jordan**: If you haven't deployed a remote MCP server yet, this quarter is your experiment window.

**Alex**: Before it becomes urgent. Before some team does it badly and creates a security incident. Before management asks "why don't we have this" and you have to explain why you're behind.

**Jordan**: We'll link the Red Hat implementation, Google's documentation, and the deployment patterns in the show notes.

**Alex**: Thanks for listening. If this helped clarify your MCP strategy, share it with your platform team. This is the conversation that needs to happen before the next planning cycle.
