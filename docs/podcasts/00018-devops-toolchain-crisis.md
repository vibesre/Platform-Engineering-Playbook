---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #018: DevOps Toolchain Crisis"
slug: 00018-devops-toolchain-crisis
---

# The DevOps Toolchain Crisis: Why Adding Tools Makes Teams Slower

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 11 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/2025-11-07-devops-toolchain-crisis-tool-sprawl-productivity-waste)**: Comprehensive analysis with 25+ sourced statistics, decision frameworks, and implementation guides for escaping tool sprawl with Internal Developer Portals.

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, overflow: 'hidden', maxWidth: '100%', marginTop: '2rem', marginBottom: '2rem'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/o7_eMy9dfRg"
    title="The DevOps Toolchain Crisis: Why Adding Tools Makes Teams Slower"
    frameBorder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowFullScreen>
  </iframe>
</div>

---

**Jordan**: Today we're diving into the DevOps toolchain crisis.  Picture this: your team has adopted Jira, GitHub, Jenkins, Datadog, PagerDuty, Slack, and now, because it's twenty twenty-five, eight different AI coding assistants.  You've spent five hundred thousand dollars on productivity tools.  So why does it take your engineers three clicks just to check build status? And why are they slower than last year?

**Alex**: Right, and the numbers are wild.  Seventy-five percent of IT professionals lose six to fifteen hours per week just to tool sprawl.  That's fifty thousand dollars per developer annually in context switching costs alone.

**Jordan**: Wait, fifty thousand dollars per developer?  That can't be right.

**Alex**: It is. Think about it.  For a two-hundred-person engineering team, that's ten million dollars per year in pure waste.  And here's the kicker from the Stack Overflow twenty twenty-five survey: ninety-four percent of developers are dissatisfied with their toolsets.

**Jordan**: Ninety-four percent?  So we're all just collectively miserable with the tools we're using?

**Alex**: Pretty much.  And what makes this urgent is that it's accelerating.  Five years ago, three to four tools was normal. Now teams navigate seven to eight DevOps tools on average just to build applications.  But here's where it gets weird.

**Jordan**: How does it get weirder than this already is?

**Alex**: AI was supposed to solve this problem.  Instead, organizations are adding eight to ten AI tools on top of their existing seven to eight DevOps tools.  We're not replacing tools, we're multiplying them.

**Jordan**: Hold on.  So the AI tools we adopted to boost productivity are actually making the problem worse?

**Alex**: Exactly.  That's the paradox we're going to unpack today.  We'll look at why this crisis is accelerating, what's really driving it, and how fifty-three percent of organizations escaped using a counterintuitive approach.

**Jordan**: Alright, let's start with what's actually happening. Because when people talk about tool sprawl, they usually focus on the subscription fees or the time to click between tabs. But that's not the real problem, is it?

**Alex**: No, it's not about the money or the clicks. It's about cognitive load.  Let me paint a picture. Teams navigate seven point four tools on average just to build applications.  And only twenty-two percent can resolve engineering issues within one day due to tool fragmentation.

**Jordan**: Seven tools just to build something.  That's nuts.

**Alex**: And here's what most people miss.  It's not about the time to switch tabs. It's about mental model switching.  Research from the University of California found that each tool switch costs twenty-three minutes of focus time.

**Jordan**: Twenty-three minutes?  Why so long?

**Alex**: Because every tool has different authentication flows, UI patterns, data models, query languages.  Your brain has to completely reload context.  It's like switching between programming languages mid-function.

**Jordan**: Oh, I get it now. It's not just clicking a tab. It's the cognitive overhead of remembering how this tool works, where things are, how to query the data.

**Alex**: Exactly. And this compounds.  You're trying to debug a deployment issue. You check Jenkins for build status, Datadog for metrics, PagerDuty for alerts, GitHub for recent changes, Jira to see if there's a ticket.  Each switch is another twenty-three minutes of lost focus.

**Jordan**: That's brutal.  And you mentioned AI making this worse. Walk me through that, because on paper, AI should help us consolidate, right?

**Alex**: You'd think.  But what's happening is that organizations are adopting eight to ten AI tools on average.  Eighty percent are using AI coding tools, but forty-six percent actively distrust them.  And get this: sixty-six percent spend more time fixing AI-generated code than writing it themselves.

**Jordan**: Wait, so we're adopting tools we don't trust, and they're making us slower?

**Alex**: That's exactly what's happening.  And each AI tool creates new context switching. Teams use ChatGPT for architecture, GitHub Copilot for code, Cursor for refactoring, Claude for documentation.  Different models, different interfaces, different trust levels.

**Jordan**: So it's tool sprawl squared.

**Alex**: Precisely.  And there's another wrinkle. Shadow AI.  Teams are adopting these tools without platform team knowledge, so you've got fragmentation on top of fragmentation.

**Jordan**: Okay, but here's what I don't understand. Companies know this is a problem. So why do they keep adding tools?

**Alex**: That's the economic trap.  Each tool promises twenty to thirty percent productivity gains. Vendor demos show seamless workflows.  And individually, these tools are actually good. It's the combination that's toxic.

**Jordan**: Right, because I can't argue that Datadog isn't valuable for observability.  Or that PagerDuty isn't critical for incident response.

**Alex**: Exactly. And there's the sunk cost fallacy. We already paid for it, might as well use it.  But here's the complication. You can't just remove tools.  Each one solves a real problem. Jira for project tracking that leadership demands. GitHub for code collaboration, non-negotiable. Datadog for observability, you can't fly blind. PagerDuty for incident response, critical.

**Jordan**: So you're trapped.  You can't add more tools because it makes things worse, but you can't remove tools because each one is necessary.  How do you escape?

**Alex**: That's where this gets interesting.  Fifty-three percent of organizations found the answer, and it's counterintuitive.  You don't remove tools. You hide them behind a unified interface.

**Jordan**: Wait, isn't that just adding another tool?  Another layer?

**Alex**: I know it sounds like that. But this is different.  This is what Internal Developer Portals actually do.  One UI, one authentication.  Unified data model across tools.  Orchestrated workflows instead of tool-by-tool clicks.  And an AI agent layer that understands context across tools.

**Jordan**: Give me a concrete example.  What does this actually look like?

**Alex**: Take Backstage, Spotify's open-source IDP. It has nine point six thousand GitHub stars.  You log in once. You see all your services, their health, their dependencies, who owns them, how to deploy them, all in one place.  Under the hood, it's aggregating data from GitHub, Kubernetes, Datadog, PagerDuty, whatever.  But you never see those tools directly.

**Jordan**: So instead of seven tabs open, I have one dashboard that shows me everything?

**Alex**: Exactly.  And the workflows are orchestrated.  Instead of clicking through Jira to create a ticket, GitHub to create a branch, Jenkins to trigger a build, Kubernetes to deploy, you click a button that says "Deploy to staging" and it handles all of that.

**Jordan**: That's starting to make sense. But let's talk about the trade-offs. What are you giving up?

**Alex**: Flexibility, for one.  You're constrained to the workflows the platform team has built. If you need to do something custom, you might have to go directly to the underlying tools.  And there's an implementation cost. Setting up an IDP isn't trivial.

**Jordan**: How big of a team do you need before this makes sense?

**Alex**: The math starts working around fifty engineers.  Below twenty, the overhead outweighs the benefit.  But once you hit fifty or more, with five-plus tools in daily workflow, the context switching becomes measurable and expensive.

**Jordan**: What about the alternatives?  There's Port, Cortex, OpsLevel. How do they compare to Backstage?

**Alex**: Backstage is open-source, free, highly customizable, but you're running it yourself.  Port is commercial, much faster time to value because it's hosted and managed.  Cortex and OpsLevel are similar, focused on service catalogs and scorecards.

**Jordan**: So if you're a startup, maybe you start with Port to get quick value.  If you're a larger org with platform team bandwidth, you go Backstage for customization?

**Alex**: That's a good heuristic.  And the outcomes are real. Organizations report thirty percent productivity increases.  Not from the tools themselves, but from less tool interaction.

**Jordan**: Thirty percent. That's significant. What's the decision framework here? When should teams actually invest in this?

**Alex**: Here's how I think about it.  IDPs make sense when you have fifty-plus engineers, five-plus tools in daily workflow, high turnover where onboarding is painful, or compliance requirements where you need audit trails.  They don't make sense when you have fewer than twenty engineers, a homogeneous tech stack with less switching, or fewer than four tools.

**Jordan**: What about implementation?  If I convince my CTO this is worth doing, what's the timeline?

**Alex**: There's a ninety-day playbook.  Days one to thirty, audit tool usage and measure switching costs. Show leadership the numbers.  Days thirty-one to sixty, run a proof of concept with Backstage, it's free, or Port, they have trials.  Days sixty-one to ninety, roll out to twenty percent of your team and measure impact.

**Jordan**: And what can I do immediately, like Monday morning?

**Alex**: Four things.  One, measure. Track how many tools your team touches in a day.  Two, calculate. Fifteen hours per week times one hundred fifty dollars per hour times team size equals your annual waste.  Three, pilot. Backstage is open-source, you can experiment over a weekend.  Four, advocate. Show leadership the ten million dollar per year cost for a two-hundred-person team.

**Jordan**: Coming back to that five hundred thousand dollar investment we opened with, the one that's making teams slower.  What's the actual fix?

**Alex**: Show them the spreadsheet.  Engineer time, on-call burden, opportunity cost of not shipping features.  The fundamentals of good engineering remain constant. You need focus. You need flow.  And you need platforms that get out of the way instead of demanding attention.

**Jordan**: The tools aren't the problem.  It's the fragmentation.

**Alex**: Exactly.  And the solution isn't better tools. It's better platforms that unify the tools you already have.  That's how you give your engineers their focus back.
