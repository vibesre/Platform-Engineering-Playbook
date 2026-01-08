---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #083: HolmesGPT Kubernetes RCA"
slug: 00083-holmesgpt-kubernetes-rca
title: "HolmesGPT: AI-Powered Root Cause Analysis for Kubernetes"
description: "Deep dive into HolmesGPT, the CNCF Sandbox AI agent for cloud-native troubleshooting. Learn what it is, its 40+ integrations, roadmap, and how to set it up today."
keywords: [HolmesGPT, CNCF, Kubernetes, root cause analysis, AI ops, troubleshooting, observability, SRE, platform engineering, Robusta]
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# HolmesGPT: AI-Powered Root Cause Analysis for Kubernetes

<GitHubButtons />

<iframe width="100%" style={{aspectRatio: '16/9', marginTop: '1rem', marginBottom: '1rem'}} src="https://www.youtube.com/embed/S_AVfaYUIBM" title="HolmesGPT: AI-Powered Root Cause Analysis for Kubernetes" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

**Duration:** ~25 minutes
**Speakers:** Jordan & Alex
**Target Audience:** Platform Engineers, SREs, DevOps Engineers (5+ years)

## Episode Overview

HolmesGPT is an open-source AI agent for investigating problems in cloud-native environments. Originally created by Robusta.dev and now a CNCF Sandbox project, it uses an agentic approach to connect LLMs with your live observability stack for real-time investigation.

This episode covers:
- What HolmesGPT is and how the agentic architecture works
- 40+ built-in integrations (Prometheus, Loki, Kubernetes, ArgoCD, and more)
- Current roadmap and community activity
- Step-by-step setup with CLI, Helm, and Web UI
- Real-world troubleshooting scenarios

## Key Takeaways

- **Agentic Architecture**: Unlike simple chat interfaces, HolmesGPT creates investigation task lists, queries systems, analyzes results, and iterates until finding root cause
- **Privacy-First**: Bring your own LLM API keys - data goes to your provider, not third parties
- **40+ Toolsets**: AWS, Azure, GCP, Kubernetes, Prometheus, Grafana Loki/Tempo, DataDog, ArgoCD, and more
- **CNCF Sandbox**: Accepted October 2025 with 1,600+ GitHub stars
- **End-to-End Automation**: Pull alerts from AlertManager/PagerDuty, investigate automatically, write analysis back to Slack/Jira

## News Segment

Today's platform engineering headlines:

1. **AirFrance-KLM Terraform/Vault/Ansible Platform** - Enterprise shift from compliance-by-construction to compliance-by-guardrails
2. **AWS ECS tmpfs Mounts on Fargate** - Memory-backed filesystems for secure secrets handling
3. **Qwen 30B on Raspberry Pi** - Democratization of large language models at the edge
4. **AWS European Sovereign Cloud** - Independent cloud infrastructure with EU governance

## Quick Start

**CLI Installation:**
```bash
pip install holmesgpt
# or
brew install holmesgpt
```

**Basic Usage:**
```bash
# Ask about cluster health
holmes ask "what pods are unhealthy and why?"

# Interactive investigation
holmes ask "investigate the OOM killed pods" --interactive

# Automated alert investigation
holmes investigate alertmanager --alertmanager-url http://localhost:9093
```

**Helm Installation:**
```bash
helm repo add holmesgpt https://robusta-dev.github.io/holmesgpt
helm install holmesgpt holmesgpt/holmesgpt --set apiKey=$OPENAI_API_KEY
```

## Resources

- [HolmesGPT GitHub](https://github.com/robusta-dev/holmesgpt)
- [Documentation](https://holmesgpt.dev/)
- [CNCF Blog: Agentic Troubleshooting](https://www.cncf.io/blog/2026/01/07/holmesgpt-agentic-troubleshooting-built-for-the-cloud-native-era/)
- [CNCF Slack #holmesgpt](https://cloud-native.slack.com/)

## Transcript

**Alex:** Welcome to the Platform Engineering Playbook Daily Podcast. Today's news and a deep dive to help you stay ahead in platform engineering.

**Jordan:** Today we're diving into HolmesGPT, an open source AI agent that promises to revolutionize how we troubleshoot Kubernetes and cloud native environments. Here's a striking stat to frame our discussion. Most on call engineers spend more time figuring out where to start investigating than actually fixing the problem. HolmesGPT aims to change that entirely.

**Alex:** But first, let's catch up on today's platform engineering news. We've got four stories that are shaping the infrastructure landscape this week.

**Jordan:** First up, Air France KLM published a detailed case study on building their secure automation platform at global scale. They're using Terraform, Vault, and Ansible together, but what's really interesting is their philosophical shift. They moved from what they call compliance by construction to compliance by guardrails.

**Alex:** That's a significant mindset change. Instead of trying to build perfect infrastructure from the start, they're putting guardrails in place that prevent bad configurations while still giving teams flexibility. It's the difference between a locked door and a well lit path. The case study goes into detail about how they handle secrets rotation, policy enforcement, and multi region deployments. Really practical lessons for anyone scaling infrastructure automation.

**Jordan:** Exactly. And speaking of container infrastructure, AWS announced that Amazon ECS now supports tmpfs mounts on Fargate and ECS Managed Instances. This might sound like a minor feature, but it has real security implications.

**Alex:** tmpfs gives you memory backed file systems. The data exists only in RAM and completely vanishes when the task terminates. This is perfect for handling short lived secrets or credentials without leaving traces on persistent storage. It also enables keeping your container root filesystem read only while still having writable scratch space for temporary files. You configure it in your task definition by adding a linux parameters block with tmpfs entries specifying the container path, size, and mount options.

**Jordan:** Third story is genuinely fascinating. ByteShape published a piece about running a thirty billion parameter Qwen model on a Raspberry Pi in real time. We're seeing the democratization of large language models happening faster than anyone predicted.

**Alex:** The implications for edge AI and local inference are huge. If you can run a thirty B model on a Raspberry Pi, imagine what becomes possible for on premises inference in regulated environments. No cloud round trips, complete data sovereignty. This opens up use cases like real time processing at the edge, air gapped environments, and scenarios where latency or privacy requirements make cloud inference impractical. The optimization techniques they're using to achieve this could reshape how we think about model deployment.

**Jordan:** And finally, AWS announced the European Sovereign Cloud. This is a completely separate and independent cloud infrastructure located and operated entirely within the European Union. It has its own governance structure with local European leadership.

**Alex:** For platform engineers working with regulated industries in Europe, this addresses years of data sovereignty concerns. It's AWS acknowledging that one size doesn't fit all when it comes to geographic and regulatory requirements. Financial services, healthcare, and government organizations have been asking for this kind of separation for years. The key differentiator is the independent governance structure with European leadership making decisions about the infrastructure.

**Jordan:** Those are our headlines. Now let's get into our main topic. HolmesGPT. Alex, let's start with the fundamental problem this tool is trying to solve.

**Alex:** The problem is one every platform engineer and SRE knows intimately. When you're debugging a production incident, the hardest part usually isn't the actual fix. It's figuring out where to begin. You've got alerts firing, logs streaming, metrics spiking, and you're trying to piece together a coherent picture from dozens of different data sources.

**Jordan:** And modern cloud native environments make this exponentially harder. You might have hundreds of microservices, each with their own logs and metrics. Kubernetes adds layers of abstraction. You've got pods, deployments, services, ingresses, persistent volumes, config maps, secrets, and custom resources. Something fails and the signal is buried under an avalanche of noise.

**Alex:** Think about a typical incident. You get paged at two AM because response times are spiking. You open your laptop and start the investigation. First you check the alerting dashboard. Then you look at Prometheus metrics. Then you dig into Grafana dashboards. Then you query logs in Loki. You check recent deployments in ArgoCD. You examine Kubernetes events. Each of these is a separate context switch, and you're trying to correlate information across all of them while half asleep.

**Jordan:** Traditional runbooks help, but they assume you already know which runbook to follow. They're great for known failure modes but useless for novel problems. And in distributed systems, novel problems are the norm, not the exception. You might have a cascade failure where the root cause is three services upstream from where the symptoms appear. No runbook can anticipate every possible failure mode.

**Alex:** This is where HolmesGPT enters the picture. It's an open source AI agent specifically designed for investigating problems in cloud native environments. Originally created by Robusta.dev, it's now a CNCF Sandbox project. It was accepted into the Sandbox in October 2025 and has over sixteen hundred GitHub stars under an Apache 2.0 license.

**Jordan:** What makes HolmesGPT different from just asking ChatGPT about your Kubernetes problems is the agentic architecture. It doesn't just answer questions based on training data. It actively connects to your observability stack, queries your systems, and investigates in real time. This is fundamentally different from a chat interface.

**Alex:** Let me explain how that agentic loop works. When you give HolmesGPT a problem to investigate, it creates what's essentially a task list. It decides which data sources to query first based on the problem description. It executes those queries using built in toolsets. It analyzes the results. Based on what it finds, it decides what to investigate next. This cycle continues until it has enough evidence to form a conclusion.

**Jordan:** It's like having a senior SRE who can simultaneously query your Prometheus for metrics, dig through your Loki logs, check your Kubernetes events, examine your ArgoCD deployment history, and correlate everything together. No human can do all of that in parallel, but HolmesGPT can query multiple systems and synthesize the results coherently.

**Alex:** And crucially, it operates in read only mode and respects your RBAC configurations. It can't make changes to your cluster, only investigate. Robusta explicitly states they don't train HolmesGPT on your data. You bring your own LLM API keys, so your data goes to your chosen provider, not to a third party. This privacy first architecture addresses enterprise concerns about sensitive operational data.

**Jordan:** Let's talk about what HolmesGPT can actually connect to. The project has over forty built in toolsets covering an impressive range of infrastructure. These toolsets are categorized by type and maturity level. Stable toolsets are marked with a green check. Beta toolsets are marked with a yellow indicator.

**Alex:** For cloud platforms, you've got AWS, Azure, and GCP integrations. This means HolmesGPT can query cloud specific resources like RDS database status, load balancer configurations, and cloud provider health checks. Container orchestration covers Kubernetes, OpenShift, and Docker. It can query pod status, examine events, check resource usage, and analyze container logs.

**Jordan:** On the observability side, there's Prometheus for metrics, Grafana Loki for logs, and Grafana Tempo for distributed traces. DataDog, New Relic, and OpenSearch are also supported. This means HolmesGPT can correlate metrics, logs, and traces during an investigation, giving it a complete picture of system behavior.

**Alex:** For CI/CD and GitOps, it integrates with ArgoCD and Helm. This is particularly useful because it can correlate problems with recent deployments. If your application started misbehaving right after a deployment, HolmesGPT can identify that correlation. There's also Flux integration in the roadmap based on community requests.

**Jordan:** Messaging systems like Kafka and RabbitMQ are covered. And interestingly, there are knowledge base integrations with Confluence, Slab, and GitHub. This means HolmesGPT can search your internal documentation while investigating. If your team has documented a known issue in Confluence, HolmesGPT can find that document and incorporate it into its analysis.

**Alex:** The end to end automation capabilities are particularly compelling. HolmesGPT can pull alerts directly from Prometheus AlertManager, PagerDuty, or OpsGenie. It investigates them automatically and can write the analysis back to Slack, Jira, or GitHub Issues. You can close the loop on incident response with AI powered triage, reducing the time from alert to meaningful analysis.

**Jordan:** What I find most powerful is the extensibility model. You can define custom toolsets using simple YAML files. If you have an internal system HolmesGPT doesn't know about, you can teach it how to query that system. The YAML definition specifies the commands or API calls to execute and how to interpret the results. You can also create custom runbooks for known alert patterns specific to your organization, embedding your team's operational knowledge.

**Alex:** There's also a clever feature called tool output transformers. When you're dealing with large log volumes, you might exceed the context window of your LLM. Transformers let you pre process tool outputs before they hit the LLM. For example, you can use an LLM summarize transformer to condense large outputs. This lets HolmesGPT handle verbose logging systems without losing the signal in the noise.

**Jordan:** Speaking of LLMs, HolmesGPT supports a broad range of providers. OpenAI and Anthropic are fully supported. Azure OpenAI and Google's Gemini work well. AWS Bedrock is supported with some configuration notes around LiteLLM parameter compatibility. And for those wanting to run everything locally, Ollama integration lets you use open source models on your own hardware with no cloud dependencies.

**Alex:** Let's look at the current roadmap and community activity. As of January 2026, there are about eighty open issues on GitHub. The most requested features include GCP MCP server support, Flux toolset integration for GitOps shops using Flux instead of ArgoCD, and OpenObserve integration for those using that observability platform as an alternative to Loki or Elastic.

**Jordan:** Other notable feature requests include GitHub App authentication for the GitHub toolset, support for multiple ArgoCD and GitHub projects in a single configuration, and customizable toolset descriptions to help the LLM better understand when to use each tool. The community is actively shaping the roadmap through these requests.

**Alex:** The community is active on the CNCF Slack. There are regular community meetups and the project maintains a robust test suite with over one hundred fifty test scenarios to ensure LLM compatibility across different providers. The CNCF Sandbox acceptance is significant because it signals the project has the governance and community backing for long term sustainability.

**Jordan:** There are some known limitations worth mentioning. When you enable many toolsets simultaneously, you might hit OpenAI's tools array length limit. The project tracks this as issue 1050. Some LLM specific quirks exist with Bedrock and Gemini configurations. There's also an open issue about kubeconfig validation errors that can affect some deployment scenarios. These are being addressed as the project matures.

**Alex:** Now let's talk about setting up HolmesGPT. There are multiple installation paths depending on your needs and where you want to run it.

**Jordan:** The quickest way to start is with pip. Just run pip install holmesgpt, all one word. If you're on Mac, Homebrew also works. brew install holmesgpt. These give you the command line interface which is perfect for exploration and getting familiar with how the agentic investigation works.

**Alex:** For production Kubernetes deployments, there's an official Helm chart. You add the HolmesGPT Helm repo from the Robusta dev GitHub page, then install with your API key configuration. The chart supports custom pod labels for organizational tagging, ingress resources for exposing the web UI, and various configuration options for different cloud environments. You'll want to set up proper RBAC so HolmesGPT has read access to the namespaces and resources it needs to investigate.

**Jordan:** The RBAC setup is important. HolmesGPT needs to read pods, events, config maps, and potentially secrets depending on your use case. You can scope this to specific namespaces if you don't want cluster wide access. The project provides example RBAC manifests as a starting point that you can customize for your security requirements.

**Alex:** Beyond the CLI, there's a web UI for browser based access that's good for teams. There's a TUI that integrates as a K9s plugin for terminal warriors who live in K9s. Slack bot integration lets you interact through chat, which is convenient during incidents when everyone's in a Slack channel anyway. And there's a Python SDK for building programmatic integrations if you want to embed HolmesGPT into your own tooling.

**Jordan:** For configuration, you'll want to set up a config file at ~/.holmes/config.yaml. This stores your API keys and default settings so you don't have to pass them on every command. The example config in the repo is a good starting point. You can specify which LLM provider to use, which toolsets to enable by default, and how to connect to your observability systems.

**Alex:** Let's walk through some real world usage. The simplest command is holmes ask followed by a question in quotes. For example, holmes ask "what pods are unhealthy and why?". HolmesGPT will query your cluster, identify unhealthy pods, pull their events and logs, check their resource limits, and synthesize an answer explaining not just what's unhealthy but why.

**Jordan:** You can add context from files. holmes ask "summarize the key points" -f path/to/document. This is useful when you have incident notes or runbooks you want HolmesGPT to consider during its investigation. You can also pass multiple files to build up context.

**Alex:** Interactive mode is particularly powerful. Add the --interactive flag and you can have a conversation. Ask a question, get an answer, then ask follow up questions without losing context. If the initial answer suggests investigating a particular service, you can ask more specific questions about that service. It's like pair debugging with an AI that has access to all your systems.

**Jordan:** For automated alert investigation, there's the investigate command. holmes investigate alertmanager --alertmanager-url followed by your AlertManager URL. It will pull active alerts and investigate each one. For PagerDuty, use holmes investigate pagerduty with your API key. Add --update to write the analysis back to PagerDuty as a note on the incident. This creates an audit trail of the automated investigation.

**Alex:** Let me share some real scenario examples. For diagnosing CrashLoopBackOff pods, HolmesGPT will pull the pod events to see restart history, check the previous container logs for error messages, look at resource limits to identify potential OOM kills, examine liveness and readiness probe configurations, and identify whether it's a memory issue, a failing health check, or a startup error.

**Jordan:** For performance degradation, it can correlate timing with recent deployments through ArgoCD, check Prometheus metrics for CPU throttling or memory pressure, look at Loki logs for error patterns or latency spikes, and examine network policies that might be affecting traffic. It's doing the correlation work that would take a human engineer significant time, especially at two AM.

**Alex:** Another common scenario is investigating network connectivity issues. HolmesGPT can examine Kubernetes network policies, check service and endpoint configurations, look for DNS resolution problems, and correlate with any recent network policy changes in Git. For database connection issues, it can query AWS RDS status, check connection pool metrics, and examine the application logs for connection timeout patterns.

**Jordan:** Some tips from the community. Start with a limited set of toolsets to control your context window and costs. You don't need to enable everything at once. Start with Kubernetes and Prometheus, then add more as you get comfortable. Use tool output transformers if you're dealing with verbose logging. Create custom runbooks for your most common alert patterns to encode your team's knowledge. And combine HolmesGPT with your existing alerting rather than replacing it entirely. It's an investigation tool, not a replacement for your alerting pipeline.

**Alex:** Let's do some critical analysis. The strengths are clear. CNCF backing provides governance and signals long term viability. The privacy first architecture where you bring your own keys addresses enterprise concerns about operational data. The extensible toolset model means you can adapt it to your specific infrastructure. And the community is active with fast iteration on new features.

**Jordan:** The considerations are equally important to understand before adoption. LLM costs can add up with heavy usage, especially if you're investigating every alert. You'll want to be thoughtful about which alerts trigger automated investigation versus manual review. Accuracy depends on having good toolset coverage for your infrastructure. If you use tools that HolmesGPT doesn't have toolsets for, you'll need to build custom ones. There's a learning curve for custom configurations. And some toolsets are still in beta, so expect some rough edges.

**Alex:** Who should adopt HolmesGPT today? Teams with complex Kubernetes environments where troubleshooting is genuinely difficult. If you have a few simple services, you might not need AI assisted investigation. Organizations that already have solid observability stacks and want to make better use of that data. HolmesGPT is only as good as the data it can access. SRE teams looking to reduce mean time to resolution, especially for complex cascade failures. And platform teams building self service troubleshooting capabilities for developers who might not have deep infrastructure expertise.

**Jordan:** This represents a broader trend we're seeing in the industry. AI native operations tooling. Tools designed from the ground up to leverage LLMs for operational tasks rather than bolting AI onto existing tools. HolmesGPT isn't just a chat interface slapped onto kubectl and grep. It's an agentic system that actively investigates using the same mental model a human SRE would use, but faster and without fatigue.

**Alex:** The agentic approach is fundamentally different from simple question answering. Instead of giving you a best guess based on training data, it's gathering live evidence, forming hypotheses, testing them by querying additional systems, and synthesizing conclusions. That's a significant architectural difference from a basic LLM wrapper.

**Jordan:** The CNCF Sandbox status is worth emphasizing. The CNCF has a rigorous evaluation process. Sandbox acceptance means the project meets their criteria for community health, governance structure, and technical merit. It's not a guarantee of success, but it's a strong signal of project quality and commitment to open governance. Projects in the Sandbox are on a path toward potential Incubation and Graduation.

**Alex:** For those wanting to try HolmesGPT, here's the recommended path. Start on a development or staging cluster, not production. This lets you experiment without risk. Use pip install to get the CLI. Configure your preferred LLM provider with an API key. Enable the core Kubernetes toolsets first. Ask some basic questions about your cluster health. Try investigating a known issue you've already debugged manually to see how HolmesGPT approaches it. Then gradually expand to more toolsets and integrate with your alerting.

**Jordan:** Join the HolmesGPT channel on CNCF Slack for community support. The maintainers are active and responsive. If you have a unique toolset integration, consider contributing it back to the project. The project welcomes contributions and has clear guidelines in their CONTRIBUTING.md file.

**Alex:** The shift we're seeing here parallels what happened with observability a decade ago. We went from siloed monitoring tools to integrated observability platforms. Now we're going from passive observability, where data sits waiting to be queried, to active AI assisted investigation where the system proactively correlates and analyzes. HolmesGPT is one of the first serious open source entries in this space.

**Jordan:** And because it's open source with CNCF governance, you're not locked into a vendor's roadmap. You can extend it, customize it, and contribute improvements back. That's the model that's worked well for the cloud native ecosystem with Kubernetes, Prometheus, and other CNCF projects.

**Alex:** To wrap up, HolmesGPT represents a new category of tooling where AI doesn't just answer questions but actively investigates your infrastructure. With forty plus integrations, CNCF backing, and a privacy first architecture, it's worth exploring for any team dealing with complex Kubernetes troubleshooting.

**Jordan:** The project is moving quickly. What's in beta today will likely be stable in a few months. Getting familiar with agentic investigation now will position your team well as this approach becomes standard practice for cloud native operations.

**Alex:** Start small with a dev cluster and the core toolsets. Experience the agentic investigation approach firsthand. If it works for your environment, gradually expand.

**Jordan:** The future of troubleshooting is AI assisted, and HolmesGPT is a compelling open source path to get there. The combination of live system access, agentic reasoning, and extensible toolsets creates something genuinely new in the operations space.
