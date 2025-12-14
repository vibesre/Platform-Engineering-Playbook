---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #057: Platform Engineering Team Structures"
slug: 00057-platform-engineering-team-structures
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #057: Platform Engineering Team Structures That Work

<GitHubButtons />

**Duration**: 18 minutes | **Speakers**: Jordan & Alex

**Target Audience**: Platform engineering leaders, SREs, and engineering managers building or scaling platform teams

> 📝 **Read the [full blog post](/blog/2025/12/12/platform-engineering-team-structures-that-work)**: A comprehensive 9,000-word guide with 30+ sources on team sizing, reporting structures, interaction patterns, and anti-patterns.

---

## Watch the Episode

<div style={{maxWidth: '640px', margin: '0 auto 1.5rem'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/YOUTUBE_VIDEO_ID"
      title="Platform Engineering Team Structures That Work"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

---

## Synopsis

Ninety percent of organizations now have platform teams according to the DORA 2025 report, but most just renamed their ops team and expected different results. This episode breaks down the team sizes, reporting structures, and interaction patterns backed by data that separate successful platform teams from glorified ticket handlers. Learn how Spotify, Netflix, and NAV structure their platform engineering for real productivity gains.

---

## Chapter Markers

- **00:00** - Introduction & The Rebranding Problem
- **02:30** - Team Size: Why 6-12 People Works
- **05:00** - Reporting Structure: Three Models
- **08:00** - News Segment
- **12:00** - Team Topologies Interaction Patterns
- **14:30** - Success Metrics: What to Measure
- **16:00** - Structure by Company Stage
- **18:00** - Anti-Patterns & Practical Takeaways

---

## News Segment (December 12, 2025)

- **[Sim - Apache 2.0 n8n Alternative](https://github.com/simstudio/sim)**: AI agent workflow automation with 19K GitHub stars
- **[Docker Hub Credential Leak](https://news.ycombinator.com)**: 10,456 images leaking secrets across 101 companies, 4,000+ AI API keys exposed
- **[Meta Replaces SELinux with BPF-LSM](https://lwn.net)**: Runtime security without kernel module compilation
- **[Litestream VFS](https://github.com/benbjohnson/litestream)**: Read-only SQLite access directly from S3
- **[GitHub Login Failures](https://www.githubstatus.com)**: 7.6% of requests impacted by scraping attack
- **[GPT-5.2 Launch](https://openai.com)**: 70.9% beat top professionals on GDPval benchmark

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Organizations with platform initiatives | 90% | DORA 2025 |
| Organizations with dedicated platform teams | 76% | DORA 2025 |
| Individual productivity boost (done right) | 8% | DORA 2025 |
| Team productivity boost (done right) | 10% | DORA 2025 |
| Optimal team size (Spotify) | 6-12 people | Spotify Engineering |
| Optimal team size (Microsoft) | 5-9 people | Microsoft DevOps |
| Target self-service rate | >90% | Industry benchmark |
| Platform team trigger point | 100+ engineers | Team Topologies |

---

## Team Structure by Company Stage

### Startup (Under 50 engineers)
- **Team size**: 2-4 people
- **Reporting**: VP of Engineering
- **Mode**: Tight collaboration with product teams
- **Focus**: One high-impact capability

### Growth (50-200 engineers)
- **Team size**: 6-9 people
- **Reporting**: Dedicated platform lead
- **Mode**: Transitioning to X-as-a-Service
- **Focus**: First real self-service portals

### Scale (200+ engineers)
- **Team size**: Multiple squads of 6-12
- **Reporting**: Platform VP
- **Mode**: Federated model (like Backstage)
- **Focus**: Complete internal developer platform

---

## Key Takeaways

1. **Right Size**: 6-12 people per squad—small enough for ownership, large enough for complete capabilities

2. **Right Reporting**: Dedicated platform leader at 100+ engineers who shields team from competing priorities

3. **Right Interaction**: Start in Collaboration mode, evolve to X-as-a-Service when capabilities mature

4. **Measure Outcomes**: Track customer success (developer happiness, DORA metrics for consuming teams), not platform team output

5. **Avoid Anti-Patterns**: Rebranding without role change, underinvestment after launch, skill concentration trap, Field of Dreams building

---

## Transcript

**Jordan**: Today we're diving into platform engineering team structures. Ninety percent of organizations now have platform teams according to the twenty twenty-five DORA report, but there's a dirty secret here.

**Alex**: Oh, I know where this is going. Most of them just renamed their ops team and called it platform engineering.

**Jordan**: Exactly. Paula Kennedy from Syntasso put it perfectly—she's seen teams simply being renamed from operations or infrastructure teams to platform engineering teams with very little change or benefit to the organization.

**Alex**: And that's the setup for disaster, right? Because platform teams aren't ops teams. They're product teams building tools for internal customers. Completely different roles, different structure, different mindset.

**Jordan**: So let's get into what actually works. Because the data shows when you do this right, you get an eight percent individual productivity boost and a ten percent team productivity boost. Those are DORA numbers. But when you get it wrong, you end up with glorified ticket handlers who are burned out and a platform that becomes an anchor dragging everyone down.

**Alex**: Yeah, and we're going to break down team sizes, reporting structures, interaction patterns, metrics. The stuff that separates successful platform teams from rebranded ops teams.

**Jordan**: Let's start with the landscape, because seventy-six percent of organizations now have dedicated platform teams. This isn't hype anymore—this is critical mass.

**Alex**: Right. And Gartner's predicting eighty percent of large software organizations will have platform teams by twenty twenty-six. So the question isn't whether you need one, it's whether you're structuring it correctly.

**Jordan**: So what's the most common anti-pattern you've seen?

**Alex**: The rebranding problem we already mentioned. But it goes deeper. Teams get renamed, but they're still doing the same reactive work. Someone opens a ticket for access to a Kubernetes namespace, platform team manually provisions it. That's not platform engineering—that's ops.

**Jordan**: And the fundamental difference is what?

**Alex**: Platform engineering is about building self-service capabilities. The goal is that a developer should be able to spin up that namespace themselves through a portal or API without ever talking to the platform team. You're building products, not processing tickets.

**Jordan**: Okay, so let's talk about team size. What actually works?

**Alex**: Spotify's model is probably the most famous. They use squads of six to twelve people. Each squad is autonomous, focused on one specific area.

**Jordan**: Six to twelve. That's pretty specific. Why that range?

**Alex**: Small enough that you can still move fast and make decisions without endless meetings. But large enough that you can own complete capabilities end to end. Microsoft recommends five to nine for most cases—same reasoning.

**Jordan**: What happens if you go smaller?

**Alex**: You end up spread too thin. Can't own a full platform area. You're constantly blocked waiting for other teams.

**Jordan**: And bigger?

**Alex**: Coordination overhead kills you. You spend more time syncing up than actually building. Plus, you lose that ownership feeling. It becomes too abstract.

**Jordan**: Okay, so team size is one lever. What about reporting structure? Where should platform teams sit in the org?

**Alex**: This is huge, and it's where a lot of companies get it wrong. There are basically three models.

**Jordan**: Walk me through them.

**Alex**: First model: platform reports at the same level as other engineering teams, usually under the CTO or VP of Engineering. You get executive visibility and organizational weight, but leadership has to actively protect you from becoming the catch-all team for every infrastructure request.

**Jordan**: Second model?

**Alex**: Platform gets its own dedicated leader—VP or director—who reports to the CTO. This reinforces the platform as a product philosophy, complete with its own roadmap. Risk here is creating silos between the platform and the teams they support.

**Jordan**: And third?

**Alex**: Platform rolls up through ops management. This usually struggles because ops teams optimize for stability and incident response. Platform development lifecycle work gets sidelined.

**Jordan**: So which model wins?

**Alex**: Depends on company size. Smaller companies under fifty engineers can usually get away with platform reporting through engineering leadership. But once you hit a hundred plus engineers, you really need that dedicated leader who shields the team from competing priorities and secures the resources they need.

**Jordan**: Because without that dedicated leader, platform becomes whoever complains loudest gets the resources?

**Alex**: Exactly. You end up reactive instead of strategic. And your roadmap gets hijacked by whoever has the most political clout that week.

**Jordan**: Alright, before we go deeper, let's hit some news because there's some stuff this week that ties directly into platform engineering concerns.

**Alex**: Yeah, six stories. Let's start with Sim—it's an Apache two point zero licensed n8n alternative for AI agent workflows.

**Jordan**: Nineteen thousand GitHub stars already. What's the platform engineering angle here?

**Alex**: Internal developer platforms are increasingly needing workflow automation for AI-powered developer tools. Sim gives you a visual canvas for building AI agent workflows with Copilot integration. So if you're building an IDP that incorporates AI assistants, this is worth watching.

**Jordan**: Next one's a security nightmare. Docker Hub credential leak.

**Alex**: Ten thousand four hundred fifty-six container images leaking secrets across a hundred and one companies. Four thousand AI API keys exposed—OpenAI, HuggingFace, Anthropic.

**Jordan**: And this is a shadow IT problem, right?

**Alex**: Exactly. Individual developer Docker accounts outside corporate governance. The platform engineering lesson here is centralized secrets management and scanning across the entire software development lifecycle isn't optional anymore. It's mandatory.

**Jordan**: Third story—Meta replacing SELinux with eBPF?

**Alex**: Yeah, this is huge. BPF-LSM is enabling runtime security without kernel module compilation. The quote that stood out to me: "Just the way iptables was replaced by eBPF rules engine, BPF-LSM could replace AppArmor and SELinux."

**Jordan**: What does that mean for platform teams?

**Alex**: You can now provide security policies that attach and remove on the fly instead of rigid kernel modules. Much more flexible.

**Jordan**: Fourth—Litestream VFS.

**Alex**: This is elegant. Read-only SQLite access directly from S3 using a VFS plugin. Fetches pages on demand, polls for LTX files. Platform engineering angle is instant read replicas without database hydration delays.

**Jordan**: Game changer for platform analytics and reporting.

**Alex**: Exactly. Fifth story—GitHub request failures on December eleventh. Seven point six percent of login requests impacted by a scraping attack.

**Jordan**: How'd they mitigate?

**Alex**: Identified the scraper, upgraded login routes to high-priority queues. The lesson for platform teams is priority queuing and attack pattern detection are critical for platform reliability.

**Jordan**: And last one—GPT five point two launch.

**Alex**: OpenAI's response to Google's "code red." Seventy point nine percent of comparisons beat top professionals on GDPval, which measures knowledge work across forty-four occupations. Fifty-five point six percent on SWE-Bench Pro, eighty percent on SWE-Bench Verified.

**Jordan**: Platform engineering implication?

**Alex**: AI coding assistants are now capable enough to be platform-provided developer tools, not just individual experiments. You should be thinking about how to integrate these into your IDP.

**Jordan**: Alright, back to team structures. We covered size and reporting. Let's talk interaction patterns because this is where Team Topologies comes in.

**Alex**: Yeah, Team Topologies defines three fundamental interaction modes. Collaboration, X-as-a-Service, and Facilitating.

**Jordan**: Break those down.

**Alex**: Collaboration is working together for a defined period to discover new things—new APIs, practices, technologies. It's temporary and intensive.

**Jordan**: When would you use that?

**Alex**: When you're building something new and you don't know exactly what the platform needs to provide yet. You embed platform engineers with a stream-aligned team to discover the right abstractions.

**Jordan**: Okay, what's X-as-a-Service?

**Alex**: One team provides, one team consumes. Minimal interaction, low cost, clear boundaries. This is the goal state for platform teams. You build self-service capabilities that stream-aligned teams can consume without needing to collaborate closely.

**Jordan**: And Facilitating?

**Alex**: One team helps and mentors another. It's temporary, focused on removing obstacles. So a platform team might facilitate a stream-aligned team learning how to use a new capability.

**Jordan**: So the journey is Collaboration while you're building, then transition to X-as-a-Service when it's mature?

**Alex**: Exactly. But here's the trap. A lot of teams think X-as-a-Service just means "create an API." They build something without listening to customer needs and adopt a "build it and they will come" philosophy.

**Jordan**: Which fails spectacularly.

**Alex**: Right. True X-as-a-Service emerges from consumer teams' needs. You need to treat internal services as products, complete with user research, clear documentation, evolution based on feedback.

**Jordan**: NAV—the Norwegian welfare administration—they're doing this well?

**Alex**: Yeah, NAV uses interaction modes explicitly. They aim for X-as-a-Service as the default but use collaboration modes when developing new platform capabilities. It keeps them customer-focused.

**Jordan**: Okay, so we've got size, reporting structure, interaction patterns. How do you measure if it's actually working?

**Alex**: This is critical because you can't just measure feature velocity. You need to track developer happiness, platform adoption, and impact on stream-aligned teams.

**Jordan**: What metrics specifically?

**Alex**: Developer happiness first. Surveys, sentiment around tooling. Netflix does this really well—they focus on qualitative metrics.

**Jordan**: What else?

**Alex**: Platform adoption rate. If your self-service rate isn't above ninety percent, something's wrong. New developers should be able to onboard within a week without manual intervention.

**Jordan**: And DORA metrics for the teams using the platform?

**Alex**: Exactly. Are the stream-aligned teams improving their deployment frequency, change lead time, change failure rate? If the platform isn't making their DORA metrics better, what's the point?

**Jordan**: Mean time to resolution for platform issues?

**Alex**: Yeah, that's your platform reliability metric. Low MTTR means your platform is resilient and can quickly recover.

**Jordan**: This is interesting because it flips the typical thinking. You're not measuring the platform team's output. You're measuring their customers' outcomes.

**Alex**: That's the product mindset. Your success is your customers' success. If developers aren't more productive, you're not successful.

**Jordan**: Let's talk about what this looks like at different company stages because a startup with thirty engineers doesn't need the same structure as Netflix.

**Alex**: Right. So startup—under fifty engineers—platform reports to VP of Engineering, two to four people, tight collaboration mode with product teams.

**Jordan**: Growth stage?

**Alex**: Fifty to two hundred engineers. You need a dedicated platform lead now. Six to nine people. You're transitioning from collaboration to X-as-a-Service. Building your first real self-service portals.

**Jordan**: And at scale?

**Alex**: Two hundred plus engineers. This is where you need a platform VP and multiple squads of six to twelve people each. Federated model like Spotify's Backstage. Spotify's rule of thumb is if you have more than two hundred engineers or microservices, Backstage can restore order to your growing chaos.

**Jordan**: Netflix adopted Backstage, right?

**Alex**: They did. Built a federated platform console to unify their engineering experience. The loose coupling between frontend and backend let them integrate existing solutions.

**Jordan**: What about anti-patterns to avoid? We talked about the rebranding problem. What else?

**Alex**: Underinvestment after launch. Building a platform isn't a project—it's a long-term strategy. If you create an IDP and then disband the team or put it on hold, it limits performance for all users. That's worse than not creating a platform in the first place.

**Jordan**: The platform becomes an anchor.

**Alex**: Exactly. Another one—the skill concentration trap. You move all your most experienced engineers to the platform team, and suddenly the stream-aligned teams lose the knowledge they need to run their software.

**Jordan**: That creates dependencies instead of reducing them.

**Alex**: Right. You want to enable teams, not make them dependent on a central team for everything.

**Jordan**: What about the Field of Dreams anti-pattern?

**Alex**: Building it without knowing if developers will actually use it. You need to validate demand before you build. Otherwise, you end up with a platform for a greenfield project that doesn't help teams with their existing production software.

**Jordan**: And Magpie platforms?

**Alex**: Focusing on shiny new technologies instead of solving problems developers face with existing systems. It's technology-driven instead of problem-driven.

**Jordan**: So let's synthesize this. What are the three key elements for successful platform teams?

**Alex**: Right size—six to twelve people, small enough for ownership. Right reporting—dedicated leader who shields from competing priorities, and at a hundred plus engineers you need a separate org. Right interaction patterns—Collaboration to X-as-a-Service evolution, not build and they will come.

**Jordan**: And the decision framework by company stage?

**Alex**: Under fifty engineers—platform reports to VP Engineering, two to four people, tight collaboration. Fifty to two hundred—dedicated platform lead, six to nine people, transitioning to self-service. Two hundred plus—platform VP, multiple squads, federated model.

**Jordan**: What are the success signals? How do you know you got it right?

**Alex**: Platform teams act as connective tissue, not a silo. Developers choose to use the platform—they're not forced. And there's continuous improvement based on feedback.

**Jordan**: And if your self-service rate is below eighty percent or developer happiness is dropping?

**Alex**: Your structure isn't working. You need to revisit team size, reporting, or interaction patterns.

**Jordan**: One more thing—the platform-as-product mindset. This keeps coming up.

**Alex**: It's foundational. Andreas Grabner said it best: "If you build something without knowing your target audience and how you can help them, you build something that will not be impacting engineering efficiency at all."

**Jordan**: So intimately understand your users and their pain points.

**Alex**: Exactly. Platform architects should be doing user research, tracking metrics, iterating based on feedback. Just like any product team.

**Jordan**: Alright, practical takeaway. If you're a platform engineering leader listening to this, what's the first thing you should do Monday morning?

**Alex**: Check your self-service rate and developer happiness metrics. If you don't have them, start measuring. And if your self-service rate is below ninety percent, you need to figure out why. Are people not aware of the platform capabilities? Is the documentation bad? Is the platform solving the wrong problems?

**Jordan**: And if you're at a company that doesn't have a platform team yet but you're thinking about starting one?

**Alex**: Get the reporting structure right from day one. Make sure the platform has a dedicated leader who can shield the team from becoming a ticket handler. And start small—two to four people focused on one high-impact capability. Prove value before you scale.

**Jordan**: The fundamentals remain constant. Right size, right reporting, right interaction patterns. Measure customer outcomes, not your output. Treat it as a product, not a project.

**Alex**: And avoid the rebranding trap. Changing the team name doesn't change the work. You need different roles, different structure, different mindset.

**Jordan**: Good stuff. That's it for today.
