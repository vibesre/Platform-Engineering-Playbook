---
title: "Episode #061: 40,000x Fewer Deployment Failures: How Netflix Adopted Temporal"
description: "Deep dive into Netflix's Temporal adoption that reduced deployment failures from 4% to 0.0001%. Learn durable execution concepts, compare workflow tools, and understand when Temporal is right for you."
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #061: Netflix Temporal"
slug: 00061-netflix-temporal-deployment-reliability
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #061: 40,000x Fewer Deployment Failures: How Netflix Adopted Temporal

<GitHubButtons />

**Duration**: ~18 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Senior Platform Engineers, SREs, DevOps leads evaluating workflow orchestration

---

## News Segment

### Story 1: Temporal $2.5B Valuation
Temporal announced a secondary funding round valuing the company at $2.5 billion. $105 million led by GIC, with Tiger Global and Index Ventures participating. 183,000+ weekly active developers, 7 million deployed clusters, 600% growth in developer adoption over 18 months.

- [Temporal Funding Announcement](https://temporal.io/blog/temporal-raises-secondary-funding)

### Story 2: Kubernetes v1.35 Released (December 17)
Major security features graduating to stable: Bound ServiceAccount token improvements, native sidecar containers, recursive read-only mounts. 2026 preview includes pod certificates for mTLS and user namespaces for pods.

- [CNCF Blog: K8s Security 2025](https://www.cncf.io/blog/2025/12/15/kubernetes-security-2025-stable-features-and-2026-preview/)

### Story 3: Shai-Hulud npm Attack Postmortem
Trigger.dev published the complete postmortem of the Shai-Hulud 2.0 attack - 500+ packages compromised, 25,000+ repositories affected. Key defenses: `npm config set ignore-scripts true`, pnpm 10's minimumReleaseAge feature, OIDC publishing.

- [Trigger.dev Postmortem](https://trigger.dev/blog/shai-hulud-postmortem)

---

## The Problem That Broke Netflix Deployments

**4% of Netflix deployments failed** due to transient Cloud Operation failures. For complex pipelines taking days to complete, a mid-pipeline failure meant restarting entirely.

### Netflix's CD Architecture
- **Spinnaker**: Multi-cloud continuous delivery platform
- **Orca**: Orchestration engine (stages, tasks, pipelines)
- **Clouddriver**: Executes Cloud Operations (create/resize server groups)

### The Four Dragons
1. **Undifferentiated complexity**: Clouddriver had its own internal orchestration just so Orca could query progress
2. **Complex retry logic**: Evolved over time to handle transient failures
3. **Homegrown Saga framework**: Built for rollbacks when operations failed mid-way
4. **Instance-local state**: Clouddriver crash = lost state, Orca timeout

---

## What is Durable Execution?

**Core concept**: Write code as if failures don't exist. The platform guarantees your program runs to completion despite crashes, restarts, or infrastructure failures.

### Four Technical Characteristics
1. **Execution Virtualization**: Work spans multiple processes/machines with automatic crash recovery
2. **Time Independence**: Workflows can run indefinitely (years if needed)
3. **Automatic State Preservation**: All variables persist through crashes
4. **Hardware Agnostic**: Reliability from software architecture, not specialized hardware

### Temporal Primitives
- **Workflows**: Deterministic series of steps (your business logic)
- **Activities**: Non-deterministic operations (API calls, DB writes) with built-in retries
- **Workers**: Processes that poll Temporal server for work

---

## Temporal vs The Competition

| Tool | Best For | Strengths | Limitations |
|------|----------|-----------|-------------|
| **Temporal** | Long-running, mission-critical workflows | Code-first (Go, Python, Java, TS), infinite duration | Learning curve, requires workers |
| **AWS Step Functions** | Serverless AWS automation | Visual designer, fully managed | Vendor lock-in, 25K event limit |
| **Apache Airflow** | ETL/batch processing | DAG-based, Python, huge ecosystem | Batch-oriented, resource-intensive |
| **Cadence** | Uber's internal workflows | 12B workflow executions/month at Uber | Smaller ecosystem than Temporal |

### Temporal Origin Story
Cadence was open-sourced by Uber in 2017. Temporal was forked by the original Cadence creators (Maxim Fateev, Samar Abbas). Both MIT-licensed but have diverged. Temporal has broader language support (Python, .NET, TypeScript, PHP).

---

## Netflix's Implementation

### New Architecture
1. Orca uses Temporal client to start `UntypedCloudOperationRunner` Workflow
2. Clouddriver workers poll Temporal for work
3. Worker resolves to strongly-typed CloudOperation implementation
4. Child Workflow executes Activities (actual cloud API calls)
5. Orca awaits workflow completion via Temporal

### Key Changes
- No more Orca polling Clouddriver for status
- No more instance-local state
- No homegrown saga/retry logic
- **2-hour default Activity retry timeout** = fix-forward window

### Migration Strategy
- Built `CloudOperationRunner` interface abstraction
- Fast Properties (Netflix's dynamic config) for gradual rollout
- Granular control: by stage type, cloud account, app, operation type, provider
- Spinnaker services first, then all Netflix applications (two quarters)

### Lessons Learned
1. **Avoid unnecessary Child Workflows**: Added complexity without benefit
2. **Use single argument objects**: Variable args break determinism on signature changes
3. **Separate business failures from workflow failures**: `WorkflowResult` wrapper pattern

---

## The Results

**Deployment failures: 4% → 0.0001%** — 40,000x improvement (4.5 orders of magnitude)

### Additional Benefits
- Orca and Clouddriver decoupled
- Deleted homegrown orchestration, saga framework, retry logic
- Clouddriver instances became stateless (Chaos Monkey enabled)
- Better debugging via Temporal UI
- Temporal at Netflix: hundreds of use cases, adoption doubled last year, migrated to Temporal Cloud

---

## Should You Adopt Temporal?

### Good Fit
- Long-running workflows (order fulfillment, loan management, onboarding)
- Mission-critical reliability requirements
- Complex saga/compensation patterns
- CI/CD orchestration
- AI agent workflows (emerging use case)

### Not a Good Fit
- Simple batch jobs (Airflow/cron is sufficient)
- Pure AWS shop wanting minimal infrastructure (Step Functions simpler)
- Small team without platform engineering capacity

### Deployment Options
- **Self-hosted**: ~80% cost savings, but operational burden
- **Temporal Cloud**: $25/1M actions, managed service

### Getting Started
1. Start with a non-critical workflow
2. Document your current failure modes first
3. The learning curve is real but worth it for the right use cases

---

## Key Takeaways

1. **Durable execution is a paradigm shift** — writing code as if failures don't exist fundamentally changes reliability thinking
2. **Netflix's 40,000x improvement** came from eliminating an entire class of failure modes
3. **Match tool to use case** — Temporal isn't for everyone, but for mission-critical workflows it's transformative
4. **Market validation** — $2.5B valuation, 183K developers, customers like Netflix, Snap, HashiCorp, Datadog, NVIDIA

---

## Resources

- [Netflix Tech Blog: How Temporal Powers Reliable Cloud Operations](https://netflixtechblog.com/how-temporal-powers-reliable-cloud-operations-at-netflix-73c69ccb5953)
- [Temporal.io](https://temporal.io/) — 17K GitHub stars
- [What is Durable Execution](https://temporal.io/blog/what-is-durable-execution)
- [Temporal $2.5B Funding Announcement](https://temporal.io/blog/temporal-raises-secondary-funding)
- [Cadence at Uber: 12B Executions/Month](https://www.infoq.com/news/2023/08/uber-cadence-workflow-platform/)
- [Forrester Study: 201% ROI with Temporal Cloud](https://temporal.io/news/temporal-technologies-secures-valuation-to-fuel-durable-execution)

---

## Transcript

**Jordan**: Today we're diving into a story that sounds almost too good to be true. Netflix reduced their deployment failures by forty thousand times. Not forty percent. Forty thousand times. From four percent failure rate down to zero point zero zero zero one percent.

**Alex**: That's four and a half orders of magnitude improvement. When I first read the Netflix Tech Blog post about this, I thought it was a typo. But it's real, and the technology behind it is something every platform engineer should understand. We're talking about durable execution, and specifically Temporal.

**Jordan**: Before we get into the Netflix deep dive, let's cover this week's news. And actually, our first story ties directly into today's topic.

**Alex**: Temporal just announced a secondary funding round valuing the company at two point five billion dollars. That's a hundred and five million led by GIC, with Tiger Global and Index Ventures participating. To put that in context, Temporal now has over one hundred eighty three thousand weekly active open source developers and seven million deployed clusters.

**Jordan**: That's six hundred percent growth in developer adoption over eighteen months. And Temporal Cloud, their managed offering, has over twenty five hundred customers with revenue growing four point four X in the same period. The market is clearly validating durable execution as a category.

**Alex**: Our second story is Kubernetes one point thirty five, which released yesterday, December seventeenth. Several important security features graduated to stable. Bound ServiceAccount token improvements add unique token IDs and node binding. Native sidecar containers are now a stable pod lifecycle primitive. And recursive read-only mounts close write paths that attackers could previously abuse.

**Jordan**: The two thousand twenty six preview is equally interesting. Pod certificates for mutual TLS are now beta. User namespaces for pods are beta and on by default. And there's a new alpha feature for hardening kubelet serving certificate validation. We'll have full coverage in a future episode.

**Alex**: And our third story is a quick follow-up. Trigger dot dev published the complete postmortem of the Shai-Hulud two point zero npm supply chain attack. Over five hundred packages compromised, affecting twenty five thousand repositories. The defensive recommendations are practical. Set npm config to ignore scripts by default. Use pnpm ten's minimum release age feature. Implement OIDC publishing for your own packages. Check the show notes for the full postmortem.

**Jordan**: Now let's get into our main topic. Forty thousand times fewer deployment failures. To understand how Netflix achieved this, we need to understand the problem they were solving.

**Alex**: Netflix runs Spinnaker for continuous delivery. Spinnaker is composed of several microservices, but two are particularly relevant here. Orca is the orchestration engine. It manages pipeline execution, coordinating stages and tasks. Clouddriver executes Cloud Operations, which are high-level commands like create server group that get translated into actual cloud provider API calls.

**Jordan**: The original flow worked like this. Orca decides a Cloud Operation needs to happen. It sends a POST request to Clouddriver. Clouddriver returns a task ID immediately. Then Orca polls Clouddriver's task endpoint repeatedly to check status. Meanwhile, Clouddriver executes the operation asynchronously and updates its internal state store.

**Alex**: This works fine on the happy path. But distributed systems are messy. Networks fail. Cloud providers have outages. And this is where the dragons emerged.

**Jordan**: Dragon number one. Clouddriver had its own internal orchestration system just so Orca could query progress. That's a lot of undifferentiated complexity. Dragon number two. Complex retry logic evolved over time to handle transient failures. Dragon number three. A homegrown Saga framework was built for rollbacks when operations failed mid-way.

**Alex**: And the worst one. Dragon number four. Task state was instance-local. If the Clouddriver instance executing an operation crashed, that state was lost. Orca would eventually timeout. And for pipelines that take days to complete, a mid-pipeline failure meant restarting the entire thing.

**Jordan**: Despite all this complexity, four percent of deployments still failed due to transient Cloud Operation failures. That's one in twenty five deployments failing through no fault of the developer.

**Alex**: So what is durable execution, and how does it solve this? The core idea is deceptively simple. Write code as if failures don't exist. The platform guarantees your program runs to completion despite crashes, restarts, or infrastructure failures.

**Jordan**: Let me make that concrete. Imagine you have a workflow that needs to send an email every thirty days. Traditional approach requires a scheduler, a database for state, error handling, retry logic, and probably some kind of dead letter queue. With durable execution, you write a while loop that calls send email, then sleeps for thirty days.

**Alex**: If the process crashes during that thirty day sleep, the durable execution platform resumes it on another worker. No timer management. No state serialization. Just Workflow dot sleep, duration of days thirty. The platform handles everything else.

**Jordan**: This works because of four technical characteristics. First, execution virtualization. Work can span multiple processes on different machines. If one crashes, another picks up seamlessly. Second, time independence. Workflows can run indefinitely. Years if needed. Third, automatic state preservation. All variables, including local ones, persist through crashes. Fourth, hardware agnosticism. Reliability comes from software architecture, not specialized hardware.

**Alex**: Temporal implements this through three main primitives. Workflows are deterministic series of steps containing your business logic. Activities are non-deterministic operations like API calls or database writes, with built-in configurable retries. Workers are processes that poll the Temporal server for work to execute.

**Jordan**: The Temporal server durably stores execution state. When a worker crashes mid-workflow, another worker can pick it up exactly where it left off. The workflow replays from its event history, and because workflow code is deterministic, it arrives at the same state.

**Alex**: Now, Temporal isn't the only option for workflow orchestration. Let's quickly compare the landscape.

**Jordan**: AWS Step Functions is the obvious comparison. It's fully managed, serverless, with a visual designer. Great for simple AWS-centric workflows. The limitations are vendor lock-in, a twenty five thousand event history limit per execution, and costs that scale with state transitions.

**Alex**: Apache Airflow is the incumbent for data pipelines. DAG-based, Python-native, huge ecosystem. But it's designed for scheduled batch jobs, not real-time workflows. And it can be resource-intensive.

**Jordan**: Then there's Cadence, which is actually Temporal's origin story. Cadence was open-sourced by Uber in twenty seventeen. Temporal was forked by the original Cadence creators, Maxim Fateev and Samar Abbas. Both are MIT-licensed. Cadence still powers over twelve billion workflow executions per month at Uber.

**Alex**: The key differences today. Temporal has broader language support including Python, TypeScript, and dot NET. Better security features like mutual TLS. Metadata support for payloads. And a more active commercial ecosystem. Cadence development is primarily driven by Uber and Instaclustr.

**Jordan**: When should you choose Temporal? Mission-critical reliability requirements. Long-running workflows spanning days, weeks, or months. Need for code-first flexibility rather than JSON or YAML state machines. And you either have a platform team to operate it or you're willing to pay for Temporal Cloud.

**Alex**: Now let's look at how Netflix actually implemented this. The new architecture is elegant.

**Jordan**: Step one. Orca uses a Temporal client to start an Untyped Cloud Operation Runner workflow. Step two. Clouddriver workers continuously poll Temporal for work. Step three. A worker picks up the task and resolves it to a strongly-typed Cloud Operation implementation. Step four. Child workflows execute activities that make actual cloud API calls. Step five. Orca awaits workflow completion through Temporal.

**Alex**: Notice what's missing. No polling from Orca to Clouddriver. No instance-local state. No homegrown saga framework. No complex retry logic. Temporal handles all of it.

**Jordan**: Netflix set a two-hour default retry timeout for Activities. That's brilliant operationally. If they introduce a regression in Clouddriver, they have two hours to fix-forward or rollback before customer deployments fail. To the user, it just looks like a deployment is taking longer than usual.

**Alex**: The migration strategy was thoughtful. They built a Cloud Operation Runner interface in Orca to abstract whether operations ran via the legacy path or Temporal. Netflix's Fast Properties system allowed granular dynamic configuration. They could enable Temporal by stage type, by cloud account, by Spinnaker application, by operation type, or by cloud provider.

**Jordan**: Spinnaker itself was the first to migrate. Within two quarters, all Netflix applications were on Temporal.

**Alex**: Netflix shared three key lessons from the migration. First, avoid unnecessary child workflows. They structured operations as a parent workflow starting child workflows, but this added complexity without benefit. Simple class composition would have worked better.

**Jordan**: Second, use single argument objects. They initially used variable arguments for workflows and activities. But Temporal requires determinism. Adding or removing an argument breaks backward compatibility and can fail long-running workflows. The pattern is to use a single serializable class for all arguments.

**Alex**: Third, separate business failures from workflow failures. They created a Workflow Result wrapper type that can communicate business process failures without failing the workflow itself. This allows more nuanced error handling.

**Jordan**: Now, the results. Deployment failures from transient Cloud Operation issues dropped from four percent to zero point zero zero zero one percent. That's virtually eliminating this entire failure mode.

**Alex**: Beyond the headline number, they achieved several other wins. Orca and Clouddriver are now decoupled. They deleted significant complexity including the homegrown orchestration engine, saga framework, and retry logic. Clouddriver instances became stateless, enabling Chaos Monkey testing. The migration forced idempotent operation design, fixing several latent bugs.

**Jordan**: And debugging improved dramatically. Temporal's UI lets you visualize workflow and activity executions in real-time. The SDKs emit rich metrics. When something goes wrong, you can see exactly where.

**Alex**: Today, Temporal is used across Netflix for hundreds of use cases. Adoption doubled in the last year. They've migrated from self-hosted to Temporal Cloud. Teams operating the Open Connect CDN and Live reliability both depend on Temporal for business-critical services.

**Jordan**: So should you adopt Temporal? Let's be practical about this.

**Alex**: Good fits include long-running workflows like order fulfillment, loan management, or customer onboarding. Mission-critical reliability requirements where four percent failure isn't acceptable. Complex saga or compensation patterns. CI CD orchestration. And increasingly, AI agent workflows.

**Jordan**: Not a good fit if you have simple batch jobs where Airflow or cron is sufficient. If you're a pure AWS shop wanting minimal infrastructure overhead, Step Functions might be simpler. Or if you're a small team without platform engineering capacity.

**Alex**: On deployment, self-hosted Temporal can save around eighty percent versus managed alternatives, but you take on operational burden. Temporal Cloud is twenty five dollars per million actions. A Forrester study found organizations using Temporal Cloud achieved two hundred one percent ROI over three years with a fourteen month payback period.

**Jordan**: If you're considering it, start with a non-critical workflow. Document your current failure modes first. The learning curve is real, Temporal requires understanding determinism constraints and the workflow-activity boundary. But for the right use cases, it's transformative.

**Alex**: Let's summarize today's key takeaways. First, durable execution is a paradigm shift. Writing code as if failures don't exist isn't just marketing. It fundamentally changes how you think about reliability.

**Jordan**: Second, Netflix's forty thousand X improvement isn't magic. It's the result of eliminating an entire class of failure modes. Transient failures, instance crashes, network issues. Temporal handles them so your code doesn't have to.

**Alex**: Third, Temporal isn't for everyone. Match the tool to the use case. If Step Functions or Airflow solve your problem, use them. But if you're building mission-critical, long-running workflows, durable execution is worth serious consideration.

**Jordan**: Fourth, the market is validating this category. Two point five billion valuation. One hundred eighty three thousand developers. Customers like Netflix, Snap, HashiCorp, Datadog, and NVIDIA. This isn't a niche technology anymore.

**Alex**: Check the show notes for links to the Netflix Tech Blog post, the Temporal documentation on durable execution, the comparison guides, and the Forrester ROI study. If deployment reliability is keeping you up at night, durable execution might be the answer you've been looking for.
