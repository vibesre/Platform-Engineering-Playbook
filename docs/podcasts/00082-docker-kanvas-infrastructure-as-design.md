---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #082: Docker Kanvas - Infrastructure as Design"
slug: 00082-docker-kanvas-infrastructure-as-design
---

# Episode #082: Docker Kanvas - Infrastructure as Design

<GitHubButtons/>

**Duration**: 27 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Platform engineers, DevOps engineers, SREs

## Episode Summary

Docker just launched Kanvas, a visual tool that turns your architecture diagrams into deployable infrastructure. Built on Meshery (CNCF's 6th highest-velocity project), it converts Docker Compose files to Kubernetes manifests and challenges Helm and Kustomize dominance. This episode explores whether "Infrastructure as Design" can truly replace YAML wrangling, when to adopt visual tooling, and how Kanvas fits alongside existing GitOps workflows.

## Key Takeaways

- **Infrastructure as Design paradigm**: Your architecture diagram IS the source of truth—changes automatically generate infrastructure as code, not just documentation
- **Built on Meshery**: CNCF sandbox project with 6th highest velocity, providing semantic "Meshery Models" that understand resource relationships and behaviors
- **Two operational modes**: Designer Mode (GA) for declarative drag-and-drop design; Operator Mode (Beta) for live infrastructure management, debugging, and deployment
- **Multi-cloud native**: AWS, Azure, GCP services plus 300+ Kubernetes operators in the catalog—design architectures spanning multiple clouds in a single topology view
- **Import flexibility**: Bring existing Docker Compose, Kubernetes manifests, Helm charts, or Kustomize configs—Kanvas visualizes what you already have
- **GitOps compatible**: Export to multiple formats; store design snapshots in GitHub via Actions; works with existing ArgoCD/Flux pipelines

## Helm vs Kustomize vs Kanvas

| Tool | Best For | Avoid When |
|------|----------|------------|
| Helm | Third-party apps, complex templating needs | Simple deployments |
| Kustomize | Environment overlays, kubectl-native workflows | Heavy parameterization |
| Kanvas | Compose-heavy teams, visual learners, multi-cloud | Mature Helm/GitOps pipelines |

## Platform Team Action Items

1. Install the Docker Desktop extension (free tier) and import existing Compose/manifests
2. Use Designer mode for visualization and stakeholder communication
3. Evaluate Operator mode (beta) for debugging workflows
4. Keep Helm/Kustomize as escape hatches—Kanvas exports to standard formats
5. Define clear process agreements about source of truth when mixing visual and code changes

## Try It If...

- Your team is Docker Compose-heavy and struggling with K8s transition
- You need multi-cloud visualizations for stakeholder communication
- Junior developers need scaffolding before learning raw Kubernetes
- You want to audit existing Helm charts visually

## Wait If...

- You have mature GitOps with ArgoCD/Flux that's working well
- Your team prefers vim over visual tools
- You're all-in on Terraform/Pulumi for multi-cloud
- Regulatory requirements demand pure IaC audit trails

## Resources

- [InfoQ: Docker Kanvas Challenges Helm and Kustomize](https://www.infoq.com/news/2026/01/docker-kanvas-cloud-deployment/) - Original announcement coverage
- [Docker Blog: Compose to Kubernetes to Cloud With Kanvas](https://www.docker.com/blog/compose-to-kubernetes-to-cloud-kanvas/) - Official Docker announcement
- [Layer5 Kanvas Documentation](https://docs.layer5.io/kanvas/) - Full documentation
- [GitHub: kanvas-docker-extension](https://github.com/layer5io/kanvas-docker-extension) - Docker Desktop extension
- [Meshery.io](https://meshery.io/) - CNCF project powering Kanvas

## Full Transcript

**Alex**: Welcome to the Platform Engineering Playbook Daily Podcast. Today's news and a deep dive to help you stay ahead in platform engineering.

**Jordan**: Today we're diving into Docker Kanvas, the visual infrastructure tool that just launched as a Docker Desktop extension. Here's the bold claim: your architecture diagram can now literally deploy itself to Kubernetes. Built on Meshery, the CNCF's sixth highest-velocity project, Kanvas is challenging Helm and Kustomize for Kubernetes deployment dominance.

**Alex**: This is a significant move from Docker. They've partnered with Layer5, the company behind Meshery, to create what they're calling "Infrastructure as Design." The tool was announced at KubeCon North America 2025 and is now generally available as a Docker Desktop extension. We're going to break down exactly how it works, compare it technically to existing tools, and help you decide whether it belongs in your platform engineering toolkit.

**Jordan**: And the timing is deliberate. Every platform engineering team I talk to complains about the dev-to-prod gap. Developers write beautiful docker-compose files locally, then someone has to manually translate that into Kubernetes manifests, Helm charts, or Kustomize overlays. That translation layer is where bugs, drift, and frustration breed.

**Alex**: Let's set the stage with why this matters. Think about the workflow in most organizations today. A developer writes a docker-compose.yml on their laptop. They've defined services, networks, volumes, environment variables. Everything works beautifully locally with docker compose up. The application runs, services communicate, data persists. Life is good.

**Jordan**: But then comes the reality check. Production doesn't run Docker Compose. Production runs Kubernetes. So now you need to translate that compose file into Kubernetes Deployments, Services, ConfigMaps, Secrets, Ingress resources, maybe Horizontal Pod Autoscalers. Each Compose service potentially becomes multiple Kubernetes resources.

**Alex**: Let me give you a concrete example. Say you have a simple three-service application in Docker Compose: a Node.js frontend, a Python API, and a Postgres database. In Compose, that's maybe 40 lines of YAML. Clean, readable, obvious. Now translate that to Kubernetes. The frontend needs a Deployment, a Service, and an Ingress. The API needs a Deployment and a Service. The database needs a StatefulSet, a Service, a PersistentVolumeClaim, and a Secret for credentials.

**Jordan**: You're now looking at 200 to 300 lines of Kubernetes YAML. And that's before you add production concerns like resource limits, liveness and readiness probes, pod anti-affinity rules, network policies, or security contexts. The cognitive load multiplication is enormous.

**Alex**: The mental model mismatch makes it worse. Developers think in services and connections. "The frontend talks to the API, the API talks to the database." Kubernetes thinks in API objects with specific behaviors. A Service is a load balancer abstraction. A Deployment manages replica sets. A StatefulSet handles ordered pod creation with stable network identities. These are powerful concepts, but they're not how application developers naturally reason about their systems.

**Jordan**: The statistics tell the story. An average Helm chart runs 500 to 2000 lines of templated YAML. Kustomize patches require you to understand the base manifests intimately before you can overlay changes. For developers who just want their app to run in production, this is an enormous cognitive barrier.

**Alex**: Current solutions address pieces of this problem but none solve it completely. Kompose does basic compose-to-Kubernetes conversion but offers no ongoing management. Once you've converted, you're maintaining raw manifests. Draft and Skaffold focus on CI/CD integration and development workflows, but they aren't visual. You're still writing and reading YAML.

**Jordan**: Helm and Kustomize are powerful but come with steep learning curves that most application developers never climb. And frankly, should they have to? If you're a frontend developer shipping React applications, should you need to understand Kubernetes Deployment strategies to get your code to production?

**Alex**: Internal developer platforms like Backstage, Port, and Humanitec try to abstract this away, but they're often locked to specific workflows or clouds. They solve the problem by hiding complexity behind forms and templates, which works until you need something the template doesn't support.

**Jordan**: What's been missing is a visual, interactive tool that bridges compose syntax to cloud-native deployment while letting you see what's actually happening and maintaining escape hatches to raw Kubernetes when you need them.

**Alex**: Which brings us to Docker Kanvas. At its core, Kanvas is built on Meshery, which has been climbing the CNCF ranks as a cloud native management platform. Layer5, the company behind Meshery, has been building this technology since 2019. What Docker has done is integrate it directly into Docker Desktop and market it to their enormous developer user base.

**Jordan**: The technical foundation is what they call Meshery Models. This is worth understanding because it's what differentiates Kanvas from simpler conversion tools. Meshery Models aren't just Kubernetes manifests. They're semantic definitions that describe the properties and behavior of specific cloud resources.

**Alex**: Think of it this way. A Kubernetes YAML file tells you structure. A Meshery Model tells you meaning. When Kanvas looks at a resource, it understands that a Postgres database needs persistent storage, accepts TCP connections on port 5432, requires authentication credentials, and should probably have backup considerations. It understands relationships, not just YAML syntax.

**Jordan**: This semantic layer is what enables the intelligent features. When you add a database to your design, Kanvas can automatically suggest or create the dependent resources. It knows a database without a PersistentVolumeClaim is probably a bug. It understands that exposing services externally requires Ingress or LoadBalancer resources.

**Alex**: Kanvas operates in two modes, and understanding both is crucial for platform engineers evaluating this tool. Designer Mode is generally available and focuses on declarative, drag-and-drop infrastructure design. Operator Mode is in beta and provides live infrastructure management.

**Jordan**: Let's go deep on Designer Mode first. You can import existing Docker Compose files, Kubernetes manifests, Helm charts, or Kustomize configurations. Kanvas parses these and generates a visual topology showing your services and their relationships. The import capability is important because it means you don't have to rebuild everything from scratch.

**Alex**: The component catalog is substantial. They claim thousands of versioned Kubernetes components with context-aware relationships. When you drag a Postgres database onto your canvas, Kanvas understands it might need a PersistentVolumeClaim, a Secret for credentials, and a Service for connectivity. It can suggest these dependent resources or create them automatically.

**Jordan**: The visual editor supports standard diagramming features. Drag and drop components. Connect services with relationship lines. Group resources into logical units. Annotate with notes. It feels like Lucidchart or Figma but for infrastructure. The difference is these diagrams aren't documentation. They're executable.

**Alex**: The GitOps integration is worth highlighting for platform engineers. Designs can be exported to multiple formats including Kubernetes manifests, Helm charts, and back to Docker Compose. More importantly, you can store design snapshots in GitHub repositories using their GitHub Action. So your visual design becomes version-controlled alongside your code.

**Jordan**: The export flexibility is a key architectural decision. Kanvas doesn't trap you in proprietary formats. You can always escape to standard Kubernetes YAML, which means existing CI/CD pipelines, ArgoCD deployments, or Flux reconciliation loops can consume Kanvas output without modification.

**Alex**: Now Operator Mode is where things get interesting for platform engineers doing day-to-day infrastructure work. When you switch from Designer to Operator, Kanvas stops being a configuration tool and becomes an active infrastructure console. It uses Kubernetes controllers like AWS Controllers for Kubernetes or Google Config Connector to actively manage your designs.

**Jordan**: In Operator Mode, you can deploy your designs to connected clusters and then monitor them in real-time. You get pod inspection showing status, events, and resource usage. You can open terminal sessions directly into containers from the visual interface. Log tailing with search lets you debug issues without switching to kubectl. Resource metrics give you at-a-glance health information.

**Alex**: They've even added traffic generation for load testing directly from the visual interface. You can generate synthetic requests against your deployed services and watch how the system responds. For platform engineers doing capacity planning or debugging performance issues, this visual feedback loop could be genuinely useful.

**Jordan**: The multi-cloud support is comprehensive. AWS services include EC2, Lambda, RDS, DynamoDB, S3, and SQS. Azure coverage spans Virtual Machines, Blob Storage, and Virtual Networks. GCP support includes Compute Engine, BigQuery, and Pub/Sub. Their catalog also provides access to hundreds of Kubernetes operators.

**Alex**: This multi-cloud support comes from the Meshery foundation. Meshery has been building integrations with cloud providers for years. Kanvas inherits all of that work. The practical implication is you can design architectures that span multiple clouds in a single topology view, which is increasingly common for platform teams managing hybrid infrastructure.

**Jordan**: That phrase "Infrastructure as Design" deserves examination. The claim is that your architecture diagram is no longer just documentation. It IS the source of truth that drives deployment. Changes in the diagram automatically generate the underlying infrastructure as code.

**Alex**: This is philosophically different from "Infrastructure as Code" where you write code that describes infrastructure. With Infrastructure as Design, you draw infrastructure that generates code. For some teams, this is a more natural workflow. For others, it might feel like losing control.

**Jordan**: Let's put this in context with the tools platform engineers are already using. Helm, Kustomize, and now Kanvas each take fundamentally different approaches to the same problem.

**Alex**: Helm treats Kubernetes deployment like package management. It's the apt or yum of Kubernetes. You have charts, which are packages. Charts contain templates written in Go's templating language. You customize deployments by providing values files that fill in template variables.

**Jordan**: Helm's strengths are clear. Third-party application deployment is straightforward. Need to deploy Nginx, Prometheus, or Postgres? Pull a chart from Artifact Hub, provide your values, and deploy. Versioning and rollbacks are built-in. The ecosystem is mature with thousands of maintained charts.

**Alex**: But Helm's weaknesses are equally clear. Go templating in YAML is painful to write and debug. The syntax is verbose and error-prone. Values files tend to sprawl as you add environment-specific configurations. You end up with values-dev.yaml, values-staging.yaml, values-prod.yaml, each with dozens of overrides.

**Jordan**: When something goes wrong, you're debugging rendered templates against original templates against values. You run helm template to see what YAML Helm will actually produce. Then you compare that to what you expected. Then you trace back through the template logic to find the bug. It's a debugging nightmare.

**Alex**: Kustomize takes a radically different approach. No templating at all. Instead, you write base Kubernetes manifests that actually deploy as-is. Then you apply patches for different environments. Google developed it and merged it into kubectl in version 1.14, making it a native Kubernetes tool.

**Jordan**: The philosophy is elegant. Start with working YAML. Your base deployment.yaml, service.yaml, and configmap.yaml should be valid Kubernetes manifests that you could apply directly. Then create overlays. An overlay for staging might patch the replica count and resource limits. An overlay for production might add node affinity and pod anti-affinity rules.

**Alex**: The syntax is different from Helm. Instead of templates, you write patches. A patch might say "for the Deployment named my-app, set replicas to 5." Kustomize merges your patch into the base manifest at apply time. No template rendering, just strategic merging of YAML documents.

**Jordan**: Kustomize strengths include simplicity, native kubectl integration with kubectl apply -k, and purely declarative configuration. You're always working with real Kubernetes YAML, not templated YAML. The learning curve is gentler for teams that already understand Kubernetes resources.

**Alex**: But the weaknesses matter too. Patch conflicts can be frustrating when base manifests change in ways that break your patches. There's no packaging concept for distribution. You can't easily share a Kustomize base with the community like you can share a Helm chart. And heavy parameterization still requires understanding the full base manifests deeply.

**Jordan**: Many teams end up using both. Helm for deploying third-party applications from Artifact Hub. Kustomize for managing environment-specific overlays in their own application deployments. It's not either-or for most organizations.

**Alex**: Kanvas brings a third paradigm. Visual-first, code-second. The YAML is abstracted away entirely for day-to-day work, though you can export it when needed. The Meshery Models underneath add semantic understanding of what resources do, not just their structure.

**Jordan**: The strengths are appealing for certain teams. Lower barrier to entry for developers who don't want to learn Kubernetes internals. Visual debugging lets you see topology issues at a glance. Multi-cloud is native, not bolted on. Import existing Helm charts or Kustomize configs to visualize what you already have.

**Alex**: The weaknesses need acknowledgment too. This is a new tool with associated adoption risk. Visual tools have historically struggled at scale. There's potential for vendor lock-in if you go deep on Meshery Models without always exporting to standard formats. And there's a philosophical question about whether visual representations can handle the complexity of production systems.

**Jordan**: For platform engineers making tooling decisions, the guidance isn't "pick one." Many teams will use all three for different purposes. Helm for deploying third-party applications. Kustomize for environment-specific overlays. Kanvas for visualization, onboarding, and debugging.

**Alex**: The interesting use case is using Kanvas as an import and visualization tool. Take your existing Helm charts or Kustomize bases, import them into Kanvas, and suddenly you have visual documentation that stays synchronized with your actual deployments. That's valuable regardless of whether you use Kanvas for deploying.

**Jordan**: Now let's be critical, because platform engineers should be skeptical of shiny new tools. Visual tools have a mixed history in infrastructure. Remember when everyone thought visual CI/CD editors would replace pipeline-as-code? Jenkins Blue Ocean was beautiful but ultimately less useful than Jenkinsfiles for complex pipelines.

**Alex**: The skeptic's argument is valid. Platform engineers often prefer code because code is auditable, diffable, and reviewable. "Infrastructure as Code" succeeded precisely because code integrates with existing software engineering practices. Pull requests, code review, Git history, and blame annotations all work naturally with text files.

**Jordan**: There's also a scaling question. Visual representations work beautifully for 10 to 20 services. What happens with 100? Or 500? Complex microservice architectures can become incomprehensible in visual form. At some point, searching and filtering in text files is faster than navigating a diagram that doesn't fit on any screen.

**Alex**: And there's the GitOps conflict. If your deployment pipeline is ArgoCD watching a Git repository for changes, where does Kanvas fit? Does the visual tool write to Git, which ArgoCD then deploys? What happens when someone modifies the Git repository directly? Conflict resolution between visual changes and code changes is non-trivial.

**Jordan**: The synchronization problem is real. If you design in Kanvas and someone else modifies the YAML in Git, what's the source of truth? You need clear process agreements about where changes originate. Otherwise you'll have drift between the visual representation and the deployed reality.

**Alex**: The optimist's view counters these concerns. Kanvas isn't eliminating code. It's generating it. Every visual change produces exportable YAML that can flow into existing pipelines. The visual layer is additive, not replacement.

**Jordan**: The developer experience argument is compelling. Not every team member needs to be a Kubernetes expert. Visual tooling can lower the barrier for developer self-service while platform engineers maintain the underlying infrastructure. That's the promise of platform engineering done well.

**Alex**: And the foundation is solid. Meshery has real CNCF momentum. It's the sixth highest-velocity project out of over 240 in the CNCF. Docker's distribution reach is unmatched. Layer5 has been building this technology for years. This isn't vaporware. It's a production-ready tool with enterprise backing.

**Jordan**: The open questions for platform engineers evaluating Kanvas include conflict resolution between visual and Git changes, performance at scale with large microservice counts, whether Meshery Models will keep pace with Kubernetes API evolution, and of course, enterprise pricing and long-term vendor strategy from Layer5.

**Alex**: For practical recommendations, let's be specific about who should and shouldn't adopt. Consider adopting Kanvas if your team is heavily invested in Docker Compose and struggling with the Kubernetes transition. The Compose-to-Kubernetes conversion alone may justify the tooling.

**Jordan**: Also consider it if you need multi-cloud visualizations for stakeholder communication. Showing executives or architects a visual architecture is more effective than walking through YAML files. Or if junior developers need scaffolding before learning raw Kubernetes. Visual tools can be excellent training wheels that build mental models.

**Alex**: Kanvas also shines for auditing existing infrastructure. Import your Helm charts and Kustomize bases to see what you actually have deployed. For teams that have grown organically without strong documentation, this visual audit capability is genuinely useful.

**Jordan**: Wait on Kanvas if you have mature GitOps pipelines with ArgoCD or Flux that are working well. Don't disrupt what works. Introducing a visual layer adds complexity to an already-working system. Also wait if your team strongly prefers text-based tooling. Culture matters, and forcing visual tools on command-line enthusiasts breeds resentment and workarounds.

**Alex**: Wait if you're heavily committed to Terraform or Pulumi for multi-cloud management. Those tools have their own visual layers through Terraform Cloud and Pulumi Cloud, plus mature ecosystems and established practices. Adding another visual tool creates confusion about source of truth.

**Jordan**: And definitely wait if regulatory requirements demand pure infrastructure-as-code audit trails. The visual layer adds complexity to compliance demonstrations. If auditors expect to see version-controlled YAML files, having a visual intermediary complicates that story.

**Alex**: If you do adopt, consider a graduated approach. Start with visualization only. Import existing manifests, Helm charts, or Kustomize configs just to see what you have. Use Designer mode for new greenfield projects where you're designing from scratch. Use Operator mode for debugging and troubleshooting, not necessarily as your primary deployment mechanism. Keep Helm and Kustomize as escape hatches.

**Jordan**: The bigger picture here is that "Infrastructure as Design" versus "Infrastructure as Code" isn't a binary choice. They can coexist. Visual tooling is complementary, potentially adding a layer of understanding on top of code-based workflows.

**Alex**: Docker is betting on developer experience as a differentiator. With Kustomize native to kubectl and Helm deeply entrenched, Docker needed a unique angle. Visual infrastructure design is that angle. It plays to Docker's strength with developers rather than competing head-to-head on pure Kubernetes tooling.

**Jordan**: For platform engineering teams, the trend toward lower cognitive load for developers is real and accelerating. If Kanvas can help application developers become more self-sufficient with Kubernetes, that reduces toil for platform teams. And reduced toil is always worth investigating.

**Alex**: To try Docker Kanvas, install the Docker Desktop extension from Docker Hub. It's free at the base tier. Import your existing Compose files or Kubernetes manifests. Join the Meshery and Layer5 community on Slack if you have questions or want to provide feedback.

**Jordan**: Kanvas isn't asking you to abandon your YAML skills or your existing pipelines. It's asking whether those skills could be augmented with visual understanding. For platform teams, that's worth thirty minutes of experimentation to find out.

**Alex**: Thanks for joining us for this deep dive into Docker Kanvas. If you're evaluating Kubernetes tooling or looking to improve developer experience on your platform, give it a try and let us know what you think. The platform engineering community benefits when we share our real-world experiences with new tools.

**Jordan**: And if you've already tried Kanvas, we'd love to hear about it. What worked? What didn't? What would make it more useful for your team? Those conversations help everyone make better tooling decisions.

**Alex**: That's all for today's episode. Keep building better platforms.
