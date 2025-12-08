---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #049: AWS re:Invent 2025 - The Agentic AI Revolution"
slug: 00049-aws-reinvent-2025-agentic-ai-revolution
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #049: AWS re:Invent 2025 - The Agentic AI Revolution

<GitHubButtons />

<iframe width="100%" style={{aspectRatio: '16/9', marginBottom: '1rem'}} src="https://www.youtube.com/embed/PeGaIq6qoy8" title="Episode #049: AWS re:Invent 2025 - The Agentic AI Revolution" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerPolicy="strict-origin-when-cross-origin" allowFullScreen></iframe>

**Duration**: 17 minutes | **Speakers**: Jordan & Alex

**Target Audience**: Platform engineers, SREs, and DevOps leaders evaluating autonomous AI agents

**Series**: Part 1 of 4 in our AWS re:Invent 2025 coverage

> 📝 **Read the [full blog post](/blog/aws-reinvent-2025-agentic-ai-platform-engineering)**: Comprehensive analysis of AWS frontier agents, verification debt, and the 40% failure prediction with statistics, sources, and actionable guidance for platform teams.

---

## Synopsis

AWS announces autonomous AI agents that can work for days without human intervention. The DevOps Agent is an always-on incident responder. The Security Agent understands your application architecture. And Kiro is already being used by hundreds of thousands of developers. Is this the beginning of the end for on-call rotations, or the beginning of a new partnership? Plus: The Model Context Protocol has won the AI integration wars, and Oxide Computer's LLM policy emphasizes that AI-generated code "becomes the responsibility of the engineer."

---

## Chapter Markers

- **00:00** - Series Introduction (Part 1 of 4)
- **00:30** - News: Model Context Protocol Wins
- **01:30** - News: Oxide's AI Code Policy
- **02:30** - AWS re:Invent 2025 Theme: Agentic AI
- **04:00** - What Are Frontier Agents?
- **05:00** - AWS DevOps Agent Deep Dive
- **08:30** - AWS Security Agent
- **10:30** - Kiro Autonomous Developer Agent
- **12:30** - Amazon Bedrock AgentCore
- **14:30** - Nova Act Browser Automation
- **15:30** - 40% Failure Rate Warning
- **17:00** - Werner Vogels: Verification Debt
- **18:30** - What Platform Teams Should Prepare For
- **20:00** - Key Takeaways & Closing

---

## News Segment (December 7, 2025)

- **[Why the Model Context Protocol Won](https://thenewstack.io/why-the-model-context-protocol-won/)**: MCP has become the de facto standard for AI-tool integrations. Major IDE vendors, cloud providers, and AI companies are all implementing support. Build integrations once, work across multiple AI systems.
- **[Using LLMs at Oxide](https://rfd.shared.oxide.computer/rfd/0576)**: Oxide Computer Company published their LLM policy: "Wherever LLM-generated code is used, it becomes the responsibility of the engineer." Engineers must self-review all LLM code before peer review. The closer code is to production, the greater care required. A thoughtful perspective on ownership and responsibility.

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Kiro users globally | Hundreds of thousands | AWS CEO Keynote |
| Nova Act browser automation reliability | 90% | AWS |
| Agentic AI projects predicted to fail by 2027 | 40% | Gartner |
| Bedrock AgentCore evaluation frameworks | 13 | AWS |

---

## Frontier Agents Announced

### AWS DevOps Agent (Preview)
- **Purpose**: Autonomous on-call engineer for incident response
- **Integrations**: CloudWatch, GitHub, ServiceNow, other tools
- **How It Works**: Correlates signals across sources, identifies root cause, generates detailed mitigation plan with expected outcomes and risks
- **Critical Limitation**: Humans approve before execution
- **Status**: Public preview

### AWS Security Agent (Preview)
- **Purpose**: Secure applications from design through deployment
- **Capabilities**: AI-powered design reviews, code analysis, contextual penetration testing
- **Key Differentiator**: Context-aware—understands your application architecture, data flow, and what you're trying to accomplish

### Kiro Autonomous Developer Agent (GA)
- **Purpose**: Fix bugs and submit PRs across multiple repositories
- **Adoption**: Hundreds of thousands of developers, Amazon's official internal tool
- **Process**: Learns from team practices, understands coding standards and test patterns, submits proposed PRs, human reviews before merge
- **Incentive**: Free Kiro Pro+ credits for qualified startups (apply by end of month)

---

## Key Concepts

### Verification Debt (Werner Vogels)
AI generates code faster than humans can comprehend it, creating a dangerous gap between what gets written and what gets understood. Every time you accept AI-generated code without fully understanding it, you're taking on verification debt. That debt accumulates until something breaks in production. Code reviews become "the control point to restore balance."

### Human-in-the-Loop
All frontier agents stop at the approval stage. Humans review and decide. Amazon's position: "To keep frontier agents from breaking critical systems, humans remain the gatekeepers." This aligns with Oxide's emphasis on engineer ownership of AI-generated code.

### Data Readiness
40% of agentic AI projects are predicted to fail. Primary cause: inadequate data foundations. Four barriers identified: data silos, trust in data quality, cross-organizational governance, and data consumption patterns. Agents need APIs, not dashboards.

---

## What Platform Teams Should Prepare For

1. **Integration Readiness**: Map how DevOps Agent fits with PagerDuty/OpsGenie workflows. Understand the handoff.
2. **Trust Protocols**: Establish processes for approving AI-generated fixes. Who can approve? What's the review bar?
3. **Skill Evolution**: Shift from writing runbooks to evaluating AI mitigation plans. Different skill.
4. **Hybrid Approach**: AI handles triage and analysis, humans handle judgment calls and approvals.

---

## Transcript

**Jordan**: Welcome to part one of our four-part AWS re:Invent twenty twenty-five series. Over the next four episodes, we're breaking down the biggest announcements from Las Vegas. Today, we're starting with what AWS called the defining theme of the conference: the rise of agentic AI. But first, let's check what else is happening in platform engineering.

**Jordan**: The Model Context Protocol has won. If you've been wondering which standard would emerge for connecting AI models to external tools, the answer is now clear. MCP, which Anthropic open-sourced back in November, has become the de facto standard for AI tool integrations. The New Stack called it quote, an open standard that standardizes how AI applications integrate with external data sources and tools. What's interesting is how quickly the ecosystem consolidated around it. Major IDE vendors, cloud providers, and AI companies are all implementing MCP support. For platform teams, this means you can build tool integrations once and have them work across multiple AI systems.

**Alex**: And speaking of AI and code, Oxide Computer Company just published their internal policy on using LLMs for code generation. It's one of the most thoughtful takes I've seen from a production engineering team. Their core principle? Wherever LLM-generated code is used, it becomes the responsibility of the engineer. They documented this in their public RFD, or Request for Discussion, system. Engineers must conduct personal review of all LLM-generated code before it even goes to peer review. The reasoning is fascinating. They note that LLMs are great at experimental or auxiliary code, but quote, the closer code is to the system that we ship, the greater care needs to be shown. It's about ownership and responsibility, not just approval checkboxes.

**Jordan**: Now let's dive into AWS re:Invent twenty twenty-five. Alex, the theme this year was unmistakable.

**Alex**: Agentic AI was everywhere. CEO Matt Garman set the tone in his keynote: AI assistants are starting to give way to AI agents that can perform tasks and automate on your behalf. This wasn't just marketing. AWS announced three frontier agents, a major platform for building custom agents, and a browser automation service. Let's unpack each one.

**Jordan**: Let's start with some context. What's the actual difference between an AI assistant and an AI agent?

**Alex**: An assistant is reactive. It waits for you to ask a question, then provides an answer. It might help you write code or explain a concept, but you're driving the interaction. An agent is proactive and autonomous. It takes actions on its own. It can observe a system, identify a problem, analyze root cause, and either fix it or propose a fix. It can work for hours or days without constant human intervention. It navigates complex, multi-step workflows across multiple systems.

**Jordan**: And AWS announced three of these so-called frontier agents.

**Alex**: Frontier agents because they represent the cutting edge of what autonomous AI can do today. These aren't simple chatbots. They're designed to handle enterprise-scale complexity. The three are the AWS DevOps Agent, the AWS Security Agent, and Kiro, the autonomous developer agent.

**Jordan**: Let's start with the one that matters most to our audience. The AWS DevOps Agent. Walk us through exactly what it does.

**Alex**: Think of it as an autonomous on-call engineer. It's designed to accelerate incident response and improve system reliability. And it works twenty-four seven. No sleep, no coffee breaks, no context-switching. It's always monitoring.

**Jordan**: How does it actually work under the hood?

**Alex**: It integrates with your existing observability stack. CloudWatch for metrics and logs. GitHub for code and deployment history. ServiceNow for incident management. And it can connect to other tools in your stack. When an incident occurs, the agent pulls data from all these sources simultaneously. It correlates signals that a human might take thirty minutes to gather. Error rates spiking in CloudWatch. A recent deployment in GitHub. Similar incidents in ServiceNow history. It connects the dots.

**Jordan**: So it's doing the initial triage that usually consumes the first chunk of an incident.

**Alex**: Exactly. But here's the critical part. It stops short of making fixes automatically. Once it identifies the root cause, it generates a detailed mitigation plan. This is the specific change to make. These are the expected outcomes. Here are the risks. An engineer reviews that plan and approves it before anything gets executed.

**Jordan**: So humans are still the gatekeepers.

**Alex**: That's intentional and explicit. Amazon's documentation states, quote, to keep frontier agents from breaking critical systems, humans remain the gatekeepers. This is a trust-building phase. The agent does the analysis, you make the decision. Over time, as these agents prove their reliability, we might see that approval threshold shift. But for now, human judgment stays in the loop.

**Jordan**: And it's in public preview right now?

**Alex**: Yes. Which is actually the perfect time to start experimenting. You can integrate it with your existing incident management workflow. Figure out how it works alongside PagerDuty or OpsGenie. Understand what the handoff looks like. Train your team on reviewing AI-generated mitigation plans. That's a different skill than writing runbooks yourself.

**Jordan**: What about the AWS Security Agent?

**Alex**: The Security Agent is also in preview. It's designed to secure applications from design all the way through deployment. What makes it different from traditional security tools is that it's context-aware. It actually understands your application architecture.

**Jordan**: Explain what that means in practice.

**Alex**: Traditional static analysis tools look for patterns. This code uses eval, that's potentially dangerous. This SQL query isn't parameterized, that's a risk. The Security Agent goes deeper. It understands what your application is trying to accomplish. It can do AI-powered design reviews, catching security issues in architecture decisions before code is written. It performs code analysis with understanding of data flow across your entire application. And it can run contextual penetration testing, knowing which endpoints matter most.

**Jordan**: So it's more like having a security engineer on the team than running a scanner.

**Alex**: That's the goal. And for platform teams, this could mean shifting security left in a much more practical way. Instead of handing developers a list of CVEs to fix, the agent can participate earlier in the process.

**Jordan**: Now let's talk about Kiro.

**Alex**: Kiro is the autonomous developer agent, and this one is already GA. Not preview. Generally available. It navigates across multiple code repositories to fix bugs and submit pull requests. AWS says hundreds of thousands of developers are already using it globally.

**Jordan**: That's a significant number.

**Alex**: And here's what makes it interesting. Amazon has made Kiro the official development tool across the company. They're using it internally at scale. It learns from your team's specific processes and practices. It understands your coding standards, your test patterns, your deployment workflows. When it submits work, it comes as a proposed pull request. A human reviews the code before it gets merged.

**Jordan**: So again, the human review step.

**Alex**: Always. Amazon describes it as quote, another member of your team. But a team member whose work you always review before it ships. Which, if you think about it, is how you'd treat any new developer.

**Jordan**: Any incentives for teams to try it?

**Alex**: Amazon is offering free Kiro Pro Plus credits to qualified startups. You have to apply through the AWS startup program before the end of the month.

**Jordan**: So we've got these three frontier agents. What about building your own custom agents? What's the infrastructure story?

**Alex**: Amazon Bedrock AgentCore. This is the platform for building production-ready AI agents. And they announced major enhancements at re:Invent that address the biggest challenges enterprises face.

**Jordan**: Walk us through the key capabilities.

**Alex**: There are four major announcements. First, policy controls. You can now set explicit boundaries for what agents can and cannot do. This agent can read from this database but not write. This agent can access production logs but not customer PII. Guardrails that are actually enforceable. Second, memory. Agents can now log and remember user patterns across sessions. They learn from interactions over time. This is crucial for agents that work with the same users or systems repeatedly. Third, evaluation systems. AWS added thirteen prebuilt evaluation frameworks for monitoring agent quality. Is the agent's output accurate? Is it following the defined policies? Is it degrading over time? Fourth, natural conversation abilities. Improvements to how agents handle multi-turn conversations with context retention.

**Jordan**: And then there's Nova Act, which caught my attention.

**Alex**: Nova Act is a new service specifically for building browser automation agents. Think about the workflows that still require humans to click through web interfaces. Form filling. Search and extract. Shopping and booking flows. QA testing of web applications.

**Jordan**: Browser automation has traditionally been fragile.

**Alex**: Which is why the key stat is so impressive. Ninety percent reliability on early customer workflows. That's on real enterprise workflows, not just demos. It's powered by a custom Nova two Lite model that's been optimized specifically for browser interactions.

**Jordan**: Now here's a sobering stat. Gartner predicts forty percent of agentic AI projects will fail before twenty twenty-seven.

**Alex**: And AWS addressed this head-on. The primary cause of failure is inadequate data foundations. They identified four specific barriers. First, data silos. Agents need to access information across systems, but most enterprises have data locked in disconnected silos. Second, trust in data. If the data an agent uses is stale, incomplete, or inaccurate, the agent's outputs will be too. Third, cross-organizational governance. Who's responsible when an agent accesses data from multiple teams? What are the audit requirements? Fourth, data consumption patterns. Agents consume data differently than humans. They need APIs, not dashboards.

**Jordan**: So you can have the most sophisticated agents in the world...

**Alex**: But if your data is a mess, they won't work. Platform teams thinking about agentic AI should probably start with a data readiness assessment. Are the systems these agents need to access actually accessible via API? Is the data fresh and accurate? Do you have the governance frameworks in place?

**Jordan**: Let's talk about what this all means for platform teams specifically. Werner Vogels gave his final re:Invent keynote after fourteen years. And he introduced a concept that every platform engineer should internalize.

**Alex**: Verification debt.

**Jordan**: Explain it.

**Alex**: It's a new form of technical debt specific to the AI era. AI generates code faster than humans can comprehend it. That creates a dangerous gap between what gets written and what gets understood. Every time you accept AI-generated code without fully understanding it, you're taking on verification debt. That debt accumulates. And at some point, something breaks in production that nobody on the team actually understands.

**Jordan**: So code reviews become even more important, not less.

**Alex**: Vogels was emphatic about this. He called code reviews quote, the control point to restore balance. He said, we all hate code reviews. It's like being a twelve-year-old standing in front of the class. But the review is where we bring human judgment back into the loop. It's interesting because this aligns with what Oxide said in their LLM policy. The organizations taking AI seriously are also the ones emphasizing engineer responsibility and ownership.

**Jordan**: So what should platform teams actually prepare for?

**Alex**: Four practical things. First, integration readiness. How will the DevOps Agent fit with your existing incident management tools? Map out your current alerting pipeline. Where would an AI agent slot in? What would change? Start thinking about this now while the agent is in preview. Second, trust protocols. Establish clear processes for approving AI-generated fixes. Who can approve? Senior engineers only, or anyone on-call? What's the review bar? How do you handle disagreement with an agent's recommendation? Third, skill evolution. Your job shifts from writing runbooks to evaluating AI mitigation plans. That's a different skill. It requires understanding both the systems and the AI's reasoning. Start building that capability now. Fourth, embrace the hybrid model. AI handles triage and analysis. Humans handle judgment calls and approvals. This isn't about replacement. It's about augmentation.

**Jordan**: So this isn't about AI replacing on-call engineers.

**Alex**: It's about AI as the first responder. The agent does the initial analysis. It pulls the data. It proposes a plan. You make the decision with full context instead of spending thirty minutes gathering that context yourself. The role evolves, but it doesn't disappear.

**Jordan**: Let's wrap up with key takeaways. First, frontier agents are here and available now. The DevOps Agent and Security Agent are in public preview. Kiro is GA with hundreds of thousands of users.

**Alex**: Second, humans remain in the loop. All these agents stop at the approval stage. You review, you decide. This is intentional and probably won't change soon.

**Jordan**: Third, integration is everything. Success depends on fitting these agents into your existing workflows, not replacing them wholesale. Start mapping that integration now.

**Alex**: Fourth, verification debt is real and growing. AI speed creates new risks. Code reviews and human oversight are more important than ever. Organizations like Oxide are already building this into policy.

**Jordan**: Fifth, data readiness might be your biggest blocker. Forty percent of agentic AI projects are predicted to fail because of data issues. Assess your data foundations before investing heavily in agents.

**Alex**: And sixth, start experimenting now. Preview access means you have time to learn before these go GA. Build the muscle memory. Train your team.

**Jordan**: Next episode, we're continuing our re:Invent coverage with part two. Graviton five with its one hundred ninety-two cores. Trainium three with four point four x performance and fifty percent cost reduction. Lambda Durable Functions that can run workflows for an entire year. And Werner Vogels' Renaissance Developer framework.

**Alex**: The autonomous DevOps future is being built right now. The question isn't whether to engage with it. It's how to shape it for your team.
