---
title: "AWS re:Invent 2025: The Agentic AI Revolution for Platform Engineering Teams"
description: "AWS announces frontier agents including DevOps Agent, Security Agent, and Kiro. What platform engineers need to know about autonomous AI agents, verification debt, and the 40% failure prediction."
slug: aws-reinvent-2025-agentic-ai-platform-engineering
keywords:
  - AWS re:Invent 2025
  - agentic AI
  - AWS DevOps Agent
  - AWS Security Agent
  - Kiro autonomous agent
  - Amazon Bedrock AgentCore
  - Werner Vogels verification debt
  - platform engineering AI
  - autonomous AI agents
  - frontier agents AWS
  - Nova Act browser automation
  - AI incident response
authors: [vibesre]
tags: [aws, ai, platform-engineering, devops, reinvent-2025]
date: 2025-12-08
datePublished: 2025-12-08
dateModified: 2025-12-08
image: /img/blog/aws-reinvent-2025-agentic-ai.png
faq:
  - question: "What are AWS frontier agents announced at re:Invent 2025?"
    answer: "AWS frontier agents are a new class of autonomous AI agents announced at re:Invent 2025. They include AWS DevOps Agent for incident response, AWS Security Agent for application security, and Kiro autonomous agent for software development. These agents can work for hours or days without human intervention."
  - question: "What is AWS DevOps Agent and when is it available?"
    answer: "AWS DevOps Agent is a frontier agent that accelerates incident response and improves system reliability. It identifies root causes in 86% of incidents based on AWS internal use. It's available in public preview in US East (N. Virginia) at no cost during preview."
  - question: "What is verification debt according to Werner Vogels?"
    answer: "Verification debt is a concept introduced by Werner Vogels at his final re:Invent 2025 keynote. It describes how AI generates code faster than humans can comprehend it, creating a gap between what gets written and what gets understood. The debt accumulates until something breaks in production."
  - question: "What percentage of agentic AI projects will fail according to Gartner?"
    answer: "Gartner predicts over 40% of agentic AI projects will be canceled by end of 2027 due to escalating costs, unclear business value, or inadequate risk controls. The primary causes are inadequate data foundations and 'agent washing' by vendors."
  - question: "What is Amazon Nova Act and what reliability does it achieve?"
    answer: "Amazon Nova Act is a new AWS service for building browser automation agents. It achieves 90% reliability for enterprise UI automation workflows and uses an hourly pricing model. It supports tasks like form filling, data extraction, QA testing, and checkout flows."
  - question: "How many developers are using Kiro autonomous agent?"
    answer: "Over 250,000 developers have embraced Kiro since its preview release. Kiro became generally available before re:Invent 2025, with the Kiro autonomous agent (more advanced version) announced at the conference."
  - question: "What is Amazon Bedrock AgentCore and what new features were announced?"
    answer: "Amazon Bedrock AgentCore is AWS's platform for building and deploying AI agents. New features announced at re:Invent 2025 include Policy for natural language access controls, AgentCore Evaluations with 13 pre-built evaluation systems, and AgentCore Memory for episodic functionality."
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# AWS re:Invent 2025: The Agentic AI Revolution for Platform Engineering Teams

<GitHubButtons />

<iframe width="100%" style={{aspectRatio: '16/9', marginBottom: '1rem'}} src="https://www.youtube.com/embed/PeGaIq6qoy8" title="AWS re:Invent 2025: The Agentic AI Revolution" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerPolicy="strict-origin-when-cross-origin" allowFullScreen></iframe>

> 🎙️ **Listen to the podcast episode**: [Episode #049: AWS re:Invent 2025 - The Agentic AI Revolution](/podcasts/00049-aws-reinvent-2025-agentic-ai-revolution) - A deep dive into AWS's frontier agents and what they mean for platform engineering teams.

## TL;DR

AWS re:Invent 2025 marked a fundamental shift from AI assistants to **autonomous AI agents**. Three "frontier agents" were announced: DevOps Agent for incident response, Security Agent for application security, and Kiro for autonomous development. Werner Vogels coined **"verification debt"** to warn about AI generating code faster than humans can understand it. Gartner predicts **40% of agentic AI projects will fail by 2027** due to inadequate data foundations. Platform teams should focus on integration readiness, trust protocols, and skill evolution—not wholesale replacement.

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Kiro developers globally | 250,000+ | [AWS](https://aws.amazon.com/blogs/aws/aws-weekly-roundup-how-to-join-aws-reinvent-2025-plus-kiro-ga-and-lots-of-launches-nov-24-2025/) |
| AWS DevOps Agent root cause identification | 86% | [AWS](https://aws.amazon.com/blogs/aws/aws-devops-agent-helps-you-accelerate-incident-response-and-improve-system-reliability-preview/) |
| Nova Act browser automation reliability | 90% | [AWS](https://aws.amazon.com/blogs/aws/build-reliable-ai-agents-for-ui-workflow-automation-with-amazon-nova-act-now-generally-available/) |
| Agentic AI projects predicted to fail by 2027 | 40%+ | [Gartner](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027) |
| Bedrock AgentCore downloads | 2 million+ | [AWS](https://www.aboutamazon.com/news/aws/aws-amazon-bedrock-agent-core-ai-agents) |
| AgentCore Evaluations frameworks | 13 | [AWS](https://aws.amazon.com/blogs/aws/top-announcements-of-aws-reinvent-2025/) |
| PGA TOUR content speed improvement with AgentCore | 1,000% | [AWS](https://www.aboutamazon.com/news/aws/aws-amazon-bedrock-agent-core-ai-agents) |
| Day-to-day decisions by agentic AI by 2028 | 15% | [Gartner](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027) |

---

## The Shift from Assistants to Agents

AWS CEO Matt Garman set the tone in his re:Invent 2025 keynote: "AI assistants are starting to give way to AI agents that can perform tasks and automate on your behalf."

This isn't just marketing. The distinction matters:

**AI Assistants** are reactive. They wait for you to ask a question, then provide an answer. You drive the interaction.

**AI Agents** are autonomous. They observe systems, identify problems, analyze root causes, and either fix issues or propose fixes. They work for hours or days without constant human intervention. They navigate complex, multi-step workflows across multiple systems.

AWS announced three "frontier agents" at re:Invent 2025—so named because they represent the cutting edge of what autonomous AI can do today. These aren't simple chatbots. They're designed to handle enterprise-scale complexity.

> 💡 **Key Takeaway**: The agent paradigm fundamentally changes how platform teams interact with AI. Instead of asking questions, you delegate tasks. Instead of getting answers, you review proposed actions. The skill shifts from prompt engineering to evaluation and approval.

---

## AWS DevOps Agent: Your Autonomous On-Call Engineer

The [AWS DevOps Agent](https://aws.amazon.com/blogs/aws/aws-devops-agent-helps-you-accelerate-incident-response-and-improve-system-reliability-preview/) is designed to accelerate incident response and improve system reliability. Think of it as an autonomous on-call engineer that works 24/7—no sleep, no coffee breaks, no context-switching.

### How It Works

The DevOps Agent integrates with your existing observability stack:
- **CloudWatch** for metrics and logs
- **GitHub** for code and deployment history
- **ServiceNow** for incident management
- Other tools via API integrations

When an incident occurs, the agent pulls data from all sources simultaneously. It correlates signals that a human might take 30 minutes to gather: error rates spiking in CloudWatch, a recent deployment in GitHub, similar incidents in ServiceNow history.

According to AWS, internal use of the DevOps Agent identified root causes in **86% of incidents**.

### The Critical Limitation

The DevOps Agent stops short of making fixes automatically. Once it identifies the root cause, it generates a detailed **mitigation plan**:
- The specific change to make
- Expected outcomes
- Associated risks

An engineer reviews that plan and approves it before anything gets executed.

AWS documentation states explicitly: "To keep frontier agents from breaking critical systems, humans remain the gatekeepers."

### Availability

AWS DevOps Agent is available in **public preview** in US East (N. Virginia) at no additional cost during preview.

> 💡 **Key Takeaway**: The DevOps Agent handles triage and analysis—the tasks that consume the first chunk of any incident. You make the decision with full context instead of spending 30 minutes gathering that context yourself. The role evolves, but it doesn't disappear.

---

## AWS Security Agent: Context-Aware Application Security

The [AWS Security Agent](https://aws.amazon.com/blogs/aws/new-aws-security-agent-secures-applications-proactively-from-design-to-deployment-preview/) secures applications from design through deployment. What makes it different from traditional security tools is that it's **context-aware**—it actually understands your application architecture.

### Beyond Pattern Matching

Traditional static analysis tools look for patterns: "This code uses eval, that's potentially dangerous." "This SQL query isn't parameterized, that's a risk."

The Security Agent goes deeper. It understands what your application is trying to accomplish:
- **AI-powered design reviews**: Catches security issues in architecture decisions before code is written
- **Contextual code analysis**: Understands data flow across your entire application
- **Intelligent penetration testing**: Creates customized attack plans informed by security requirements, design documents, and source code

AWS says customers report receiving penetration testing results "within hours compared to what would have taken weeks of scheduling and back-and-forth communication between teams."

### How Organizations Use It

Security teams define organizational security requirements once: approved encryption libraries, authentication frameworks, logging standards. The Security Agent then automatically validates these requirements throughout development, providing specific guidance when violations are detected.

### Availability

AWS Security Agent is available in **public preview** in US East (N. Virginia), free during preview. All data remains private—queries and data are never used to train models.

> 💡 **Key Takeaway**: The Security Agent shifts security left in a practical way. Instead of handing developers a list of CVEs to fix, the agent participates earlier in the process—understanding context rather than just matching patterns.

---

## Kiro: The Autonomous Developer Agent

[Kiro](https://www.aboutamazon.com/news/aws/amazon-ai-frontier-agents-autonomous-kiro) is the autonomous developer agent that navigates across multiple code repositories to fix bugs and submit pull requests. **Over 250,000 developers** are already using it globally.

### What Makes Kiro Different

Amazon has made Kiro the official development tool across the company. It learns from your team's specific processes and practices:
- Understands your coding standards
- Learns your test patterns
- Adapts to your deployment workflows

When it submits work, it comes as a proposed pull request. A human reviews the code before it gets merged.

Amazon describes it as "another member of your team"—but a team member whose work you always review before it ships.

### Persistent Context

Unlike chat-based AI assistants, Kiro maintains **persistent context across sessions**. It doesn't run out of memory and forget what it was supposed to do. It can be handed tasks and work on its own for hours or days with minimal human intervention.

For teams, the Kiro autonomous agent is a shared resource that builds a collective understanding of your codebase, products, and standards. It connects to repos, pipelines, and tools like Jira, GitHub, and Slack to maintain context as work progresses.

### Startup Incentive

Amazon is offering **free Kiro Pro+ credits** to qualified startups through the AWS startup program.

> 💡 **Key Takeaway**: Kiro represents the "developer agent" category—autonomous systems that can take development tasks and execute them across your codebase. The human review step remains critical, treating AI-generated code the same way you'd treat code from any new team member.

---

## Amazon Bedrock AgentCore: Building Your Own Agents

[Amazon Bedrock AgentCore](https://www.aboutamazon.com/news/aws/aws-amazon-bedrock-agent-core-ai-agents) is the platform for building production-ready AI agents. At re:Invent 2025, AWS announced major enhancements addressing the biggest challenges enterprises face.

### Key New Capabilities

**Policy in AgentCore (Preview)**: Set explicit boundaries for what agents can and cannot do using natural language. "This agent can read from this database but not write." "This agent can access production logs but not customer PII." These are deterministic controls that operate outside agent code.

**AgentCore Evaluations**: 13 pre-built evaluation systems for monitoring agent quality—correctness, safety, tool selection accuracy. Continuous assessment for AI agent quality in production.

**AgentCore Memory**: Agents can now develop a log of information on users over time and use that information to inform future decisions. The new "episodic functionality" allows agents to learn from past experiences.

### Framework Agnostic

AgentCore supports any framework (CrewAI, LangGraph, LlamaIndex, Google ADK, OpenAI Agents SDK, Strands Agents) or model while handling critical agentic AI infrastructure needs.

### Adoption Numbers

In just five months since preview:
- **2 million+ downloads**
- Organizations including PGA TOUR (1,000% content writing speed improvement, 95% cost reduction), Cohere Health, Cox Automotive, Heroku, MongoDB, Thomson Reuters, Workday, and Swisscom

> 💡 **Key Takeaway**: AgentCore addresses enterprise concerns about agent governance. Policy controls let you set guardrails, Evaluations let you monitor quality, and Memory lets agents learn without retraining. This infrastructure layer is crucial for production deployments.

---

## Nova Act: 90% Reliable Browser Automation

[Amazon Nova Act](https://aws.amazon.com/blogs/aws/build-reliable-ai-agents-for-ui-workflow-automation-with-amazon-nova-act-now-generally-available/) is now generally available—a new service for building browser automation agents with enterprise reliability.

### Why This Matters

Browser automation has traditionally been fragile. Selenium scripts break when UIs change. RPA tools require constant maintenance. Nova Act achieves **90% reliability** on enterprise workflows—a significant improvement.

### Technical Approach

Nova Act uses reinforcement learning with agents running inside custom synthetic environments ("web gyms") that simulate real-world UIs. This vertical integration across model, orchestrator, tools, and SDK—all trained together—unlocks higher completion rates at scale.

Powered by a custom **Amazon Nova 2 Lite model** optimized specifically for browser interactions.

### Use Cases

- Form filling
- Search and extract
- Shopping and booking flows
- QA testing (Amazon Leo reduced weeks of engineering effort to minutes)

### Pricing Innovation

Nova Act uses an **hourly pricing model**—you pay for time the agent is active, not tokens or API calls. This makes costs more predictable for automation workflows.

### Launch Partner

1Password is a launch partner, bringing credential security management directly into agentic AI automation.

> 💡 **Key Takeaway**: Nova Act targets workflows that still require humans to click through web interfaces. The 90% reliability benchmark and hourly pricing model make it practical for production use cases like QA testing and data entry.

---

## Werner Vogels' Warning: Verification Debt

Werner Vogels delivered his **final re:Invent keynote** after 14 years and introduced a concept every platform engineer should understand: **verification debt**.

### What Is Verification Debt?

AI generates code faster than humans can comprehend it. This creates a dangerous gap between what gets written and what gets understood.

Every time you accept AI-generated code without fully understanding it, you're taking on verification debt. That debt accumulates. And at some point, something breaks in production that nobody on the team actually understands.

### "Vibe Coding" Is Gambling

Vogels was direct: "Vibe coding is fine, but only if you pay close attention to what is being built. We can't just pull a lever on your IDE and hope that something good comes out. That's not software engineering. That's gambling."

### The Solution: Code Reviews as Control Points

Vogels called code reviews "the control point to restore balance."

"We all hate code reviews. It's like being a twelve-year-old standing in front of the class. But the review is where we bring human judgment back into the loop."

This aligns with thoughtful policies from organizations like Oxide Computer Company, whose public LLM policy states: "Wherever LLM-generated code is used, it becomes the responsibility of the engineer." Engineers must conduct personal review of all LLM-generated code before it even goes to peer review.

### The Renaissance Developer Framework

Vogels' parting framework for the AI era emphasizes:
- Being curious
- Thinking in systems
- Communicating precisely
- Owning your work
- Becoming a polymath

His core message: "The work is yours, not the tools."

> 💡 **Key Takeaway**: Verification debt is technical debt's dangerous cousin. As AI generates more code, the gap between generation and understanding widens. Code reviews become more important, not less. Organizations serious about AI are also the ones emphasizing engineer responsibility and ownership.

---

## The 40% Failure Prediction

Gartner's sobering prediction: **Over 40% of agentic AI projects will be canceled by end of 2027** due to escalating costs, unclear business value, or inadequate risk controls.

### Why Projects Are Failing

"Most agentic AI projects right now are early stage experiments or proof of concepts that are mostly driven by hype and are often misapplied," said Anushree Verma, Senior Director Analyst at Gartner. "This can blind organizations to the real cost and complexity of deploying AI agents at scale."

### The Four Data Barriers

AWS addressed this at re:Invent 2025, identifying four specific barriers:

1. **Data silos**: Agents need to access information across systems, but most enterprises have data locked in disconnected silos
2. **Trust in data**: If data is stale, incomplete, or inaccurate, agent outputs will be too
3. **Cross-organizational governance**: Who's responsible when an agent accesses data from multiple teams? What are the audit requirements?
4. **Data consumption patterns**: Agents consume data differently than humans. They need APIs, not dashboards.

### The "Agent Washing" Problem

Gartner identified widespread "agent washing"—vendors rebranding existing AI assistants, chatbots, or RPA tools as "agentic AI" without delivering true agentic capabilities. Of thousands of vendors claiming agentic solutions, Gartner estimates **only about 130 actually offer genuine agentic features**.

### The Positive Outlook

Despite the high failure rate, Gartner sees long-term potential:
- **15% of day-to-day work decisions** will be made autonomously by agentic AI by 2028 (up from 0% in 2024)
- **33% of enterprise software applications** will include agentic AI by 2028 (up from less than 1% in 2024)

> 💡 **Key Takeaway**: Data readiness might be your biggest blocker. Before investing heavily in agents, assess your data foundations. Are systems accessible via API? Is data fresh and accurate? Do you have governance frameworks in place?

---

## What Platform Teams Should Prepare For

Based on the re:Invent 2025 announcements, here's what platform engineering teams should focus on:

### 1. Integration Readiness

Map how the DevOps Agent fits with your existing incident management tools. Understand the handoff between PagerDuty/OpsGenie and AWS's agent. Start thinking about this now while the agent is in preview.

### 2. Trust Protocols

Establish clear processes for approving AI-generated fixes:
- Who can approve? Senior engineers only, or anyone on-call?
- What's the review bar for different severity levels?
- How do you handle disagreement with an agent's recommendation?

### 3. Skill Evolution

Your job shifts from writing runbooks to evaluating AI mitigation plans. That's a different skill. It requires understanding both the systems and the AI's reasoning. Start building that capability now.

### 4. Embrace the Hybrid Model

AI handles triage and analysis. Humans handle judgment calls and approvals. This isn't about replacement—it's about augmentation.

The agent does the initial analysis. It pulls the data. It proposes a plan. You make the decision with full context instead of spending 30 minutes gathering that context yourself.

### 5. Address Data Foundations First

Given the 40% failure prediction, prioritize data readiness before agent deployment:
- Audit API availability for systems agents need to access
- Assess data freshness and accuracy
- Establish cross-team governance for agent data access
- Document data consumption patterns for automation

> 💡 **Key Takeaway**: The autonomous DevOps future is being built right now. The question isn't whether to engage with it—it's how to shape it for your team. Start with preview access, build the muscle memory, and train your team on evaluating AI-generated plans.

---

## Related Resources

- **[Episode #049: AWS re:Invent 2025 - The Agentic AI Revolution](/podcasts/00049-aws-reinvent-2025-agentic-ai-revolution)** - Full podcast discussion
- **[AWS DevOps Agent Documentation](https://aws.amazon.com/blogs/aws/aws-devops-agent-helps-you-accelerate-incident-response-and-improve-system-reliability-preview/)** - Official preview guide
- **[AWS Security Agent Documentation](https://aws.amazon.com/blogs/aws/new-aws-security-agent-secures-applications-proactively-from-design-to-deployment-preview/)** - Official preview guide
- **[Amazon Bedrock AgentCore](https://www.aboutamazon.com/news/aws/aws-amazon-bedrock-agent-core-ai-agents)** - Build your own agents
- **[Gartner Agentic AI Prediction](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)** - Full report on project failure rates

---

## Key Takeaways Summary

1. **Frontier agents are available now**: DevOps Agent and Security Agent in public preview, Kiro GA with 250,000+ developers
2. **Humans remain gatekeepers**: All agents stop at approval stage—you review, you decide
3. **Integration is everything**: Success depends on fitting agents into existing workflows, not replacing them
4. **Verification debt is real**: AI speed creates new risks; code reviews more important than ever
5. **Data readiness may be your biggest blocker**: 40% of projects fail due to data issues—assess foundations first
6. **Start experimenting now**: Preview access is the time to learn before these go GA

---

*This analysis is part of our AWS re:Invent 2025 coverage series. Stay tuned for Episode #050: AWS Infrastructure Revolution covering Graviton 5, Trainium 3, and Lambda Durable Functions.*
