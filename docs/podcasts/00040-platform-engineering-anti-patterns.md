---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #040: Platform Engineering Anti-Patterns"
slug: 00040-platform-engineering-anti-patterns
---

# 10 Platform Engineering Anti-Patterns That Kill Developer Productivity

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 13 minutes
**Speakers:** Jordan and Alex
**Target Audience:** Platform engineers, engineering managers, CTOs evaluating platform investments

> 📝 **Read the [full blog post](/blog/platform-engineering-anti-patterns)**: A comprehensive deep-dive into why platform engineering initiatives fail, with data from DORA 2024, case studies from Spotify and Zalando, and an actionable audit checklist.

<div class="video-container">
<iframe width="100%" height="400" src="https://www.youtube.com/embed/3b3ulsVvrk4" title="10 Platform Engineering Anti-Patterns That Kill Developer Productivity" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

:::warning DORA 2024 Data

The DORA 2024 report found that organizations with dedicated platform teams saw throughput **decrease by 8%** and change stability **decrease by 14%**. Yet Gartner predicts 80% of large software engineering organizations will have platform teams by 2026. This episode unpacks why so many platform investments backfire.

:::

---

**Jordan**: Today we're diving into some uncomfortable data. The twenty twenty-four DORA report found that organizations with dedicated platform teams saw throughput decrease by eight percent and change stability decrease by fourteen percent.

**Alex**: Wait, that's backwards. Platform engineering is supposed to accelerate development, not slow it down.

**Jordan**: Exactly. And yet Gartner predicts that eighty percent of large software engineering organizations will have platform teams by twenty twenty-six. So what's going on here?

**Alex**: The Atlassian Developer Experience Report adds more context. Sixty-nine percent of developers lose eight or more hours per week to inefficiencies. That's twenty percent of their work week just gone.

**Jordan**: For a thousand-developer organization, that translates to roughly seventeen million dollars annually in lost productivity. These aren't small numbers.

**Alex**: So the question becomes, why are so many platform investments actually making things worse? And that's what we're going to unpack today. Ten anti-patterns that are sabotaging platform engineering initiatives.

**Jordan**: Let's start with the organizational anti-patterns. First up, what I call Ticket Ops. The bottleneck factory.

**Alex**: This one is everywhere. Developers submit tickets for infrastructure provisioning. Need a new environment? Open a ticket. Update a dependency? Ticket. Change a configuration? You guessed it, another ticket.

**Jordan**: And wait times can stretch to a week or more for tasks that should take minutes. Humanitec puts it bluntly. Ticket ops is draining your organization.

**Alex**: The irony is that organizations implement this because they mistake process for governance. Tickets feel like control. They create audit trails and approval chains that satisfy compliance checklists.

**Jordan**: But they destroy velocity. The fix is self-service with guardrails, not gatekeepers. Zalando's you build it, you run it philosophy transformed their platform from bottleneck to accelerator.

**Alex**: The second anti-pattern is the Ivory Tower Platform. Teams disconnected from developer reality.

**Jordan**: Platform teams that operate in isolation, creating abstract guidelines and architectural standards that look elegant on paper but don't survive contact with production.

**Alex**: One enterprise architecture critique I read described it as architects sitting in their ivory towers making pronouncements that most of the time no one listens to.

**Jordan**: The fix is what I call the architect elevator model. Continuously moving between strategy and implementation. Hands-on pair programming with application teams. If your platform team hasn't pair-programmed with an application developer in the last month, you're building in an ivory tower.

**Alex**: Third is Platform as Bucket. Manuel Pais from Team Topologies nails this one. He says it's an anti-pattern he sees very often, where the platform becomes a bucket for everything, and just becomes a huge mess with lack of ownership, lack of focus, and a lot of waste.

**Jordan**: This happens when platform teams are measured by market share. How many teams use the platform. That incentivizes adding everything instead of consolidating around core value.

**Alex**: Platform team burnout is real. When your platform roadmap has forty-seven P one items, you don't have priorities. You have a bucket. The best platforms do a few things exceptionally well.

**Jordan**: Fourth is Mandatory Adoption. Making platforms mandatory to show adoption numbers to leadership.

**Alex**: This is tempting because it looks like success. But it closes the feedback loops you need to actually succeed. Forced usage hides resistance and breeds resentment.

**Jordan**: There's a case study of a mid-sized tech firm that implemented mandatory IDP adoption without developer input. The result? Confusion, reduced productivity, and eventually they had to roll back to legacy systems.

**Alex**: Make adoption attractive, not mandatory. If you have to force developers onto your platform, that's a signal, not a strategy.

**Jordan**: Now let's move to the technical anti-patterns. Fifth is the Golden Cage. Excessive standardization that blocks productivity.

**Alex**: Octopus Deploy captures this perfectly. Golden Cage results when platforms are designed with too many constraints, turning guidance into restrictions.

**Jordan**: One-size-fits-all templates that accommodate no one. Rigid workflows that prevent teams from solving problems their way. Developers spend more time bypassing the system than delivering value.

**Alex**: The fix is designing golden paths to be optional, transparent, extensible, and customizable. Flexibility is the antidote to the golden cage.

**Jordan**: Sixth is the Over-Engineered Monolith. Platforms so complex that learning them becomes a project in itself.

**Alex**: Jay Jenkins from Akamai says complexity is the enemy. If platform engineering is creating more toil than it's reducing, something is off.

**Jordan**: Platforms with unfamiliar configuration languages, sparse documentation, inconsistent APIs. The best platforms are almost invisible. Developers use them without thinking about them.

**Alex**: Start with a minimum viable platform. Expand based on measured developer pain, not anticipated needs. Optimize for developer time, not platform engineering elegance.

**Jordan**: Seventh is Front-End First, Back-End Never. Beautiful developer portals with manual processes underneath.

**Alex**: This one's wild. Port dot io's twenty twenty-four research found that thirty-five percent of organizations still use spreadsheets with microservice data as their developer portal.

**Jordan**: Teams ship a gorgeous portal with sleek UI, comprehensive documentation, impressive dashboards. Under the hood? Manual processes, spreadsheets, and Slack messages to get anything done.

**Alex**: Build the backend before the frontend. Prove your self-service APIs work. Any backend automation is better than a beautiful facade over manual processes.

**Jordan**: Eighth is the Biggest Bang Trap. Starting with the largest, most complex application to maximize ROI.

**Alex**: This fails because the platform team is learning on the hardest problem, the platform lacks capabilities you discover too late, and trust erodes when the flagship migration struggles.

**Jordan**: Syntasso explains it well. Start small, build confidence, expand proven wins. Don't test your safety net with the highest trapeze.

**Alex**: Ninth is Day One Obsession. Platforms that excel at spinning up new applications but abandon developers after that.

**Jordan**: Octopus Deploy provides a sobering reality check. Of the time your team will invest in an application, the creation process is below one percent.

**Alex**: So optimizing Day One is optimizing for less than one percent of the lifecycle. Day Two through Day Fifty, the ongoing operations, debugging, scaling, updates, incident response, that's where developers actually spend their time.

**Jordan**: Build golden paths for the entire application lifecycle, not just scaffolding.

**Alex**: And tenth is Build It And They Will Come. No adoption strategy at all.

**Jordan**: Erica Hughberg at KubeCon twenty twenty-four said it directly. Even the best products don't sell themselves. Expecting engineers to drive adoption without a clear marketing approach is a recipe for disaster.

**Alex**: Platform teams build elegant solutions, announce them in Slack, update the wiki, and wait for developers to flock to it. Months later, adoption is in the single digits.

**Jordan**: The fix is treating your platform like a product that needs marketing. Internal advocacy, storytelling, early-adopter success stories. Firms monitoring adoption closely report thirty percent higher ROI on their platform initiatives.

**Alex**: So those are the ten anti-patterns. But here's the important part. DORA explains that productivity decrease as typical of transformational efforts. They call it the J-curve effect.

**Jordan**: Initial productivity hit before long-term gains. But only if you avoid these anti-patterns.

**Alex**: Right. The difference between platform success and failure isn't budget or talent. It's avoiding these traps. And every anti-pattern has a counter-strategy.

**Jordan**: Let's talk about what successful teams do differently. Spotify and Zalando are the canonical examples.

**Alex**: Spotify built Backstage starting with the areas that quote really hurt. Their data shows that more frequent Backstage users are two point three times more active on GitHub. Clear correlation between platform engagement and productivity.

**Jordan**: Zalando's transformation is even more instructive. They say one of the first steps was cultural, not technical. They changed hiring, onboarding, and workflows before building the platform.

**Alex**: The pattern is consistent. Treat platform as product, not project. Developer is the customer. Measure satisfaction, not just adoption.

**Jordan**: Practice the architect elevator. Move between strategy and implementation. Stay hands-on.

**Alex**: Self-service with guardrails. Zalando's you build it, you run it. Not gatekeepers creating bottlenecks.

**Jordan**: And stable priorities. DORA found that teams with stable priorities face forty percent less burnout. In organizations with frequent priority shifts, ninety percent of teams experience productivity drops.

**Alex**: Stop churning your platform roadmap. Stability enables velocity.

**Jordan**: Here's a quick audit checklist for listeners. Are your developers waiting more than one day for standard infrastructure requests? That's Ticket Ops.

**Alex**: Has your platform team pair-programmed with application developers this quarter? If not, that's Ivory Tower risk.

**Jordan**: Has your platform scope grown three-x in the last year without corresponding team growth? Platform as Bucket.

**Alex**: Do you have one-size-fits-all templates with no extension points? Golden Cage.

**Jordan**: Beautiful portal but developers still messaging in Slack for help? Front-End First.

**Alex**: If you answer yes to three or more of these, your platform initiative is at serious risk.

**Jordan**: The eighty-four percent failure rate for digital transformation isn't inevitable. These anti-patterns are recognizable and fixable.

**Alex**: Spotify and Zalando didn't succeed because they had bigger budgets or better engineers. They succeeded because they avoided these traps and treated their platforms as products serving developer customers.

**Jordan**: That's the fundamental insight from the DORA data. Platform engineering can absolutely deliver the productivity gains everyone expects. But only if you build it right.

**Alex**: Start with the audit checklist. Identify which anti-patterns are present in your organization. Address them systematically. The eighty-four percent don't have to include you.

---

## Key Takeaways

💡 **DORA 2024 Reveals the Problem**: Organizations with platform teams saw throughput decrease by 8% and stability decrease by 14%—the platform isn't the problem, the anti-patterns are.

💡 **Ticket Ops Destroys Velocity**: Self-service with guardrails beats gatekeeping every time. If developers wait more than a day for standard requests, you have Ticket Ops.

💡 **Platform as Bucket = Burnout**: When your platform roadmap has 47 P1 items, you don't have priorities—you have a bucket. The best platforms do a few things exceptionally well.

💡 **Golden Cage Causes Workarounds**: Excessive standardization creates more workarounds than it prevents. Design golden paths to be optional, transparent, extensible, and customizable.

💡 **Day 1 is Less Than 1% of Lifecycle**: Application creation is less than 1% of the time developers invest in an application. Optimize for Day 2-50, not just scaffolding.

💡 **Build It and They Will Come is a Myth**: Firms with adoption strategies see 30% higher ROI. Treat your platform like a product that needs marketing.

💡 **Stable Priorities = 40% Less Burnout**: DORA found that teams with stable priorities face 40% less burnout. Stop churning your platform roadmap.

---

## Sources

### Primary Research
- [DORA Report 2024](https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report) - Google Cloud
- [Developer Experience Report 2024](https://www.atlassian.com/blog/developer/developer-experience-report-2024) - Atlassian
- [2024 State of Internal Developer Portal Report](https://www.port.io/blog/the-2024-state-of-internal-developer-portal-report) - Port.io

### Anti-Patterns & Best Practices
- [8 Platform Engineering Anti-Patterns](https://www.infoworld.com/article/4064273/8-platform-engineering-anti-patterns.html) - InfoWorld
- [Paved vs Golden Paths](https://octopus.com/blog/paved-versus-golden-paths-platform-engineering) - Octopus Deploy
- [Eliminate Ticket Ops](https://humanitec.com/use-cases/eliminate-ticket-ops) - Humanitec
- [Platform Building Antipatterns](https://www.syntasso.io/post/platform-building-antipatterns) - Syntasso

### Case Studies
- [Spotify Engineering - Backstage](https://engineering.atspotify.com/)
- [Zalando's Sunrise Developer Platform](https://engineering.zalando.com/posts/2023/08/sunrise-zalandos-developer-platform-based-on-backstage.html)
- [Team Topologies](https://teamtopologies.com/) - Matthew Skelton & Manuel Pais
