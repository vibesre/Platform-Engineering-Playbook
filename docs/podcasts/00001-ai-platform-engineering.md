---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #001: 75% of Your Team Uses Unauthorized AI"
slug: 00001-ai-platform-engineering
---

# 75% of Your Team Uses Unauthorized AI - Why Your Blocking Strategy Backfires

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 12-15 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the full blog post**: [AI-Powered Platform Engineering: Beyond the Hype](/blog/2025-02-ai-powered-platform-engineering-beyond-the-hype) - Comprehensive written analysis with data, tool comparisons, and implementation strategies.

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, overflow: 'hidden', maxWidth: '100%', margin: '2rem 0'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/McKRXZvoNuY"
    title="AI Platform Engineering Podcast Episode"
    frameBorder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowFullScreen>
  </iframe>
</div>

<PodcastSubscribeButtons />

---

**Jordan**: Today we're diving into a crisis that 85% of organizations are facing right now. Shadow AI - employees adopting AI tools faster than IT teams can assess them. GenAI traffic surged 890% in just one year.

**Alex**: And here's the paradox that's keeping platform teams up at night: trying to block AI fails 100% of the time. But we've also got genuinely impressive results from teams who got it right. One team reduced false positive alerts by 96% - from 523 alerts per week to 22. That's not incremental improvement, that's life-changing for anyone on-call.

**Jordan**: So let's start with understanding the scope. You mentioned 85% of organizations - where's that from?

**Alex**: ManageEngine's 2024 Shadow AI report. 85% of IT decision-makers say employees are adopting AI tools faster than they can assess them. But here's where it gets really interesting - there's this massive disconnect. 93% of employees admit they're using AI tools without approval, but only 54% of IT leaders think their policies on unauthorized AI use are actually effective.

**Jordan**: Wait, so more than half of leadership thinks their "don't use AI" policy is working, while 93% of employees are ignoring it?

**Alex**: Exactly. It's as effective as telling developers "don't Google error messages." And the traffic data backs this up - Palo Alto Networks analyzed 7,000 global customers and found GenAI traffic increased 890% in 2024. That's not a trend, that's a tsunami.

**Jordan**: Eight hundred ninety percent in one year. How does that even happen?

**Alex**: Because the tools actually work. And this is what makes it so hard to fight - developers aren't being malicious, they're being productive. GitHub's research from 2024 shows 55% faster task completion with AI code assistants. Not 5%, not 10% - 55%. And job satisfaction goes up 60 to 75%.

**Jordan**: So if you block the tools, you're simultaneously making developers slower and more miserable.

**Alex**: Which means your best people leave. Or they find creative ways around your blocks, and now you've got an even worse shadow problem. The security researchers at The New Stack crystallized the risk - Shadow AI is highest in serverless environments, containerized workloads, and API-driven applications. Basically everywhere modern apps live, because AI services can be embedded easily without formal security reviews.

**Jordan**: So we're talking about data exfiltration, compliance violations, intellectual property leakage...

**Alex**: All of that. But also operational chaos and cost explosion. Teams are discovering they're paying for dozens of AI services across different teams with no visibility, no volume discounts, no cost allocation. Just pure waste.

**Jordan**: And this is where I want to push back on something. Because my first instinct hearing this is "okay, we need better enforcement, tighter controls, block API calls to unauthorized endpoints." Why doesn't that work?

**Alex**: Because you're fighting developer productivity. The reason they're using these tools is they make them faster. That 55% productivity gain I mentioned - that's real. And when Stack Overflow surveyed developers, 93% were using AI tools without waiting for approval. You can't put that genie back in the bottle.

**Jordan**: So it's the classic Shadow IT problem all over again.

**Alex**: Exactly. Same playbook, just happening faster because AI adoption is moving at hyperspeed. This is the paradox - you can't block it, but you also can't let it run wild.

**Jordan**: Okay, so if blocking doesn't work, what does?

**Alex**: You make the blessed path easier than the shadow path. And this is where AI gateways and governance platforms come in. The pattern that's working is what I call "managed chaos." You provide a central AI gateway that gives developers access to 100-plus LLMs through a single API, with guardrails baked in.

**Jordan**: So instead of blocking OpenAI calls, you provide OpenAI access through your gateway.

**Alex**: Exactly. Plus Anthropic, plus open-source models, whatever they need. The two platforms leading this space are Portkey and TrueFoundry. Portkey is model-agnostic with 50-plus built-in guardrails - PII detection, prompt injection prevention, content filtering. They've got SOC 2, HIPAA, GDPR compliance. And here's the clever part - they give you observability into AI usage. So instead of discovering your Shadow AI problem six months later when the bill comes, you see it in real-time.

**Jordan**: What about TrueFoundry?

**Alex**: TrueFoundry takes a different approach - they're Kubernetes-native. If you're already heavily invested in K8s, they integrate more naturally. Sub-3-millisecond latency overhead, built-in RBAC, works with your existing auth. The choice is basically: Portkey if you want maximum model flexibility and SaaS convenience, TrueFoundry if you're Kubernetes-first and want more control.

**Jordan**: And these aren't free.

**Alex**: Both have free tiers, but at scale you're paying. However, the ROI calculation is interesting. When teams consolidate from dozens of unauthorized services to a single governed gateway, they're eliminating duplicate services, negotiating bulk rates, getting cost visibility. Organizations are reporting 60% cost reductions just from consolidation and visibility.

**Jordan**: So the governance platform isn't an additional cost, it's replacing wasteful spending you didn't know about.

**Alex**: Right. And that's before you count the value of actually having security controls, compliance, and audit trails. But I want to talk about the developer experience, because I've heard a lot of skepticism about AI-generated code quality.

**Jordan**: Yeah, the skepticism is warranted, right? These tools make mistakes.

**Alex**: The skepticism is absolutely warranted. Stack Overflow's 2025 survey shows only 29% of developers trust AI outputs, and 66% report spending more time debugging AI-generated code than expected. So this isn't a magic wand.

**Jordan**: That sounds... problematic for a tool that's supposed to make you 55% faster.

**Alex**: It is, if you use it wrong. But here's the nuance - it's a power tool, not autopilot. You still need to know what you're building. NYU research shows 40% of AI-generated code can contain vulnerabilities without proper validation. So you layer in three levels of defense: policy validation with something like Open Policy Agent, human code review for anything security-critical, and automated scanning with tools like TFsec.

**Jordan**: So AI accelerates the coding, but you can't skip the validation steps.

**Alex**: Right. And here's where it gets interesting from a platform engineering perspective - you can actually build those validation steps into the developer workflow. Make it so the AI-assisted path includes the guardrails by default.

**Jordan**: Okay, but now I'm worried we're recreating the tool sprawl problem again. Because I'm seeing organizations adopt multiple AI coding tools - Copilot, Claude Code, Cursor...

**Alex**: 49% of organizations are paying for multiple AI coding tools. And yeah, on the surface that sounds like the same sprawl problem we started with.

**Jordan**: Is it?

**Alex**: That's the question I've been wrestling with. And I think there's a difference between managed sprawl and shadow sprawl. If you're providing two or three approved options through a governance layer, tracking usage, managing costs - that's controlled choice. Copilot for autocomplete, Claude Code for complex refactoring, whatever. If developers are using 12 different tools underground with no visibility, that's chaos.

**Jordan**: So the number of tools matters less than whether you have visibility and governance.

**Alex**: Exactly. Though I'd still argue fewer is better, all else being equal. But controlled choice beats shadow chaos every time.

**Jordan**: Let's shift to AIOps, because this is where you mentioned those results that exceeded expectations. A 96% reduction in false positives?

**Alex**: Okay, so I was honestly skeptical about the AIOps hype. A lot of vendor claims that sounded too good to be true. But then I saw the real-world data. Edwin AI by LogicMonitor - 90% reduction in alert noise, 20% boost in operational efficiency.

**Jordan**: Ninety percent reduction in alert noise.

**Alex**: Ninety percent. But here's the one that really got me - Hexaware's case study with Elastic AI. Team efficiency improved 50%, which is great. But false positive alerts dropped 96%. They went from 523 alerts per week to 22.

**Jordan**: Wait, say that again. 523 alerts to 22?

**Alex**: 523 to 22. That's from drinking from a firehose to actually actionable signals. And if you've ever been on-call for a system with noisy alerts, you know that's not just a productivity improvement - that's a quality of life improvement.

**Jordan**: That's the difference between getting paged at 3 AM for a log volume spike that's actually just a batch job, versus getting paged when there's a real incident.

**Alex**: Exactly. And it gets better over time. The AI learns what normal looks like for your systems, filters out the noise, correlates events across different services. Informatica reported 50% reduction in observability costs just by eliminating false positives and optimizing alert routing.

**Jordan**: Okay, what's the catch? Because this sounds too good to be true.

**Alex**: The catch is it requires good telemetry. If your observability data is garbage, AI can't fix that. You need proper instrumentation, consistent tagging, structured logging - the basics have to be in place first. It's not a silver bullet, it's an accelerator for teams that already have decent practices.

**Jordan**: So you can't AI your way out of bad fundamentals.

**Alex**: You cannot. Though Forrester research shows organizations using AIOps typically see 20 to 40% reduction in unplanned downtime, which for most companies justifies the investment even if you have to clean up your observability first.

**Jordan**: Let's talk about what this means for skills and careers, because the landscape is changing fast.

**Alex**: Red Hat's State of Platform Engineering report from October 2024 found that 94% of organizations say AI is either critical or important to platform engineering's future. That's basically everyone.

**Jordan**: Okay, but "AI is important" is vague. What specifically should platform engineers be learning?

**Alex**: It's not "learn AI/ML" as a general skill. It's about specific intersections. Platform engineers who understand prompt engineering and can design effective AI integrations. SREs who can leverage AIOps for incident response. MLOps engineers who can build infrastructure for AI workloads. And the market is rewarding this - engineers with AI platform experience are commanding salary premiums.

**Jordan**: So if you're a platform engineer without AI background, what's the fastest way to build that experience?

**Alex**: Start with your own tooling. Implement AI code assistants on your team, measure the impact, learn what works and what doesn't. Then move to AI governance - that's an immediate need for most organizations right now. Then AIOps for observability. Then MLOps if your company is shipping AI features.

**Jordan**: So it's a progression - developer tools, governance, observability, infrastructure.

**Alex**: That's the path I'm seeing work. Because each phase builds on the previous one and delivers standalone value. You're not boiling the ocean, you're solving specific problems while building AI platform competency.

**Jordan**: Alright, let's get tactical. What are the biggest mistakes you're seeing teams make?

**Alex**: Number one: trying to block AI instead of channeling it. We covered why that fails. Number two: deploying AI tools without training. You can't just turn on Copilot and expect 55% productivity gains - people need to learn effective prompting, when to trust AI, when not to. Number three: ignoring the cost controls. AI APIs get expensive fast, especially if developers are sending entire codebases as context. You need budget alerts, rate limiting, cost allocation by team.

**Jordan**: The boring FinOps stuff.

**Alex**: The boring FinOps stuff that prevents your surprise five-figure monthly bill. Because that's what teams are discovering - they've got Shadow AI spending they didn't know about until it shows up on the credit card statement.

**Jordan**: And on the flip side, what exceeded expectations?

**Alex**: Honestly, AIOps. I was skeptical about the ROI claims, but seeing 90% alert noise reduction in production environments is compelling. The improvement to on-call quality of life alone justifies it. And it's one of those things where the people who deploy it become evangelists because the before-and-after is so stark.

**Jordan**: What's overhyped?

**Alex**: AI-generated infrastructure as code. It's getting better, but you still need deep Terraform or Pulumi expertise to validate what the AI produces. It's not replacing platform engineers anytime soon. Though five years from now, we'll have this conversation again and the landscape will look totally different.

**Jordan**: So to bring this full circle - if you're a platform engineering leader dealing with Shadow AI right now, what's the first move?

**Alex**: Deploy an AI gateway within the next 30 days. Portkey or TrueFoundry, doesn't really matter which. Just get developers a blessed path to AI that's easier than the shadow path. That buys you time to build proper governance, implement monitoring, train your teams.

**Jordan**: And if you're already past that phase?

**Alex**: Then focus on metrics. Track adoption, measure productivity impact, quantify cost savings. Because the business case for AI platform engineering is there, but you need data to demonstrate it. And that data feeds your roadmap - should you invest in AIOps next? MLOps? More sophisticated governance? Let the metrics guide you.

**Jordan**: What about individual engineers trying to build these skills?

**Alex**: Start with the tools you use every day. If you're not using an AI code assistant yet, try one for 30 days and measure your own productivity. Then look at your team's pain points - are alerts noisy? Is AI governance a mess? Is Shadow AI creating security risks? Pick one problem, build a solution, measure the impact. That's how you build real AI platform engineering experience, not by taking another online course.

**Jordan**: The fundamentals of good platform engineering remain constant - solve real problems, measure impact, iterate based on data.

**Alex**: Exactly. AI is just the latest set of tools and techniques. The discipline of platform engineering - understanding your users, eliminating toil, providing golden paths - that doesn't change. What changes is now you have AI as another tool in your toolkit, and you need to wield it thoughtfully.
