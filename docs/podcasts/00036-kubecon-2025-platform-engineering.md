---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #036: KubeCon Atlanta 2025 Part 2: Platform Engineering Consensus"
slug: 00036-kubecon-2025-platform-engineering
---

# KubeCon Atlanta 2025 Part 2: Platform Engineering Consensus and Community Reality Check

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 17 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Platform team leads, principal engineers, technical leadership

> 📝 **Read the [full blog post](/blog/kubecon-atlanta-2025-recap)**: Complete KubeCon Atlanta 2025 recap covering all 10 major announcements, technical breakthroughs from Part 1, and community discussions.

:::info KubeCon 2025 Series (Part 2 of 3)

This is Part 2 of our three-part deep dive into KubeCon Atlanta 2025 (November 12-21), covering the CNCF's 10-year anniversary.

- **Part 1**: [AI Goes Native and the 30K Core Lesson](/podcasts/00035-kubecon-2025-ai-native) - DRA GA, CPU DRA, Workload API, OpenAI optimization, Kubernetes rollback
- **Part 2** (this episode): Platform engineering consensus - Three principles, real-world case studies, anti-patterns
- **Part 3**: Community at 10 years - Maintainer sustainability, burnout, the next decade

:::

<div style={{maxWidth: '640px', margin: '2rem auto'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/04MzUuNhuGY"
      title="KubeCon Atlanta 2025 Part 2: Platform Engineering Consensus and Community Reality Check"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

---

**Jordan**: Welcome to Part 2 of our three-part KubeCon Atlanta twenty twenty-five series. Yesterday in Part 1, we covered the technical announcements—DRA going GA, CPU DRA for HPC convergence, OpenAI's thirty-thousand-core optimization. Today, we're talking about something just as important. After years of "what even IS platform engineering" debates, the industry finally reached consensus. Three principles. Real-world adoption at billion-dollar scale. And then, in the middle of celebrating these wins, Cat Cosgrove—newly elected to the Kubernetes Steering Committee—says quote, "I'm ready to abandon ship."

**Alex**: That's the tension in this episode. Platform engineering has clarity now. We know what success looks like. But the community that achieved this consensus is showing serious signs of strain.

**Jordan**: Tomorrow in Part 3, we'll dive deeper into maintainer burnout, community sustainability, and what the next ten years might look like. But today, let's start with the good news. Platform engineering isn't stuck in definitional chaos anymore.

**Alex**: Okay but let's be honest. For years, every conference had the same exhausting debates. Is platform engineering just DevOps rebranded? How's it different from SRE? What even qualifies as a platform?

**Jordan**: Right. And every vendor claiming their product WAS platform engineering. Meanwhile, platform teams are making multi-year investments—remember Episode twenty-four, Backstage costs a hundred fifty thousand dollars per twenty developers—and if you get the definition wrong, that's years wasted.

**Alex**: So what changed at KubeCon twenty twenty-five?

**Jordan**: Multiple speakers, across different sessions, different companies, different tracks, all saying the same three things. Industry convergence.

**Alex**: Alright, I'm listening. What are the three principles?

**Jordan**: Principle one: API-first self-service. Not ticket-driven. Not ClickOps. Not "ask the platform team." Everything programmatically accessible. If a developer can't automate it, it's not self-service.

**Alex**: That sounds... obvious?

**Jordan**: And yet most "platforms" fail this test. Think about it. How many internal platforms require a ticket for database provisioning? Or a Slack message for environment access?

**Alex**: Fair. That's not self-service. That's just slow ops.

**Jordan**: Exactly. Principle two: Business relevance. The platform exists to solve business problems, measured in business metrics. Revenue per engineer. Time to market. Customer satisfaction. Not just infrastructure metrics.

**Alex**: Wait, not uptime? Not CPU utilization?

**Jordan**: Those matter for platform health. But they're not why the platform exists. If your platform has ninety-nine point nine percent uptime but developers still can't ship features faster, you've optimized the wrong thing.

**Alex**: Okay, that's a mindset shift. What's principle three?

**Jordan**: Managed service approach. And this is where most teams fail.

**Alex**: Explain.

**Jordan**: You can't throw templates over the wall and call it a platform. True platform engineering means ongoing operational support, SLAs, responsibility. Mora Kelly from Intuit called it the "done for you" approach. If all services need certain capabilities, build it in, make it part of the platform, do it FOR your developers.

**Alex**: So templates aren't enough?

**Jordan**: Templates are a starting point. But without operational support, documentation, lifecycle management? You've just created work for developers, not reduced it.

**Alex**: This is starting to sound familiar. Haven't we been saying this for years?

**Jordan**: Saying it, yes. But this is the first time I've seen industry-wide alignment. CNCF created a formal Platform Engineering TCG. Multiple companies presenting the same framework. Abby Bangser summarized it perfectly: "Platform engineering is your specialized internal economy of scale. It's what's unique to your business but common to your teams."

**Alex**: So the definitional chaos is... over?

**Jordan**: The WHAT is settled. The HOW to sustain it? That's the harder question. And we'll get there. But first, let's talk about the anti-pattern that explains why seventy percent of platform teams fail.

**Alex**: From Episode eleven. The critical PM gap, metrics blindness.

**Jordan**: Right. But KubeCon gave us a new metaphor. The "puppy for Christmas" problem.

**Alex**: Wait, what?

**Jordan**: Give someone a puppy as a Christmas gift. Initial excitement. Lots of photos. Everyone's happy. Two weeks later, the puppy needs feeding, vet visits, training, cleanup. And the recipient wasn't ready for the ongoing operational burden.

**Alex**: Oh no. I see where this is going.

**Jordan**: The platform equivalent: Create a Helm chart template. Publish it to your internal catalog. Declare "we've enabled self-service!" Six months later, the template's out of date, dependencies have CVEs, best practices evolved, and teams using the template are on their own.

**Alex**: This explains why adoption stalls. Developers aren't dumb. They see abandoned software.

**Jordan**: Exactly. So what's the solution? Mora Kelly talked about the internal marketplace model. Inspired by app stores. When you publish a capability to your platform catalog, you're committing to operational support, documentation, SLAs, lifecycle management, deprecation notices, migration paths.

**Alex**: That's a significantly higher bar than "write a template."

**Jordan**: Which is why platform engineering requires dedicated teams. You can't do this as a side project. Intuit gets this. They migrated a twenty-year-old Mailchimp monolith—eleven million users, seven hundred million emails per day—and quote, "most developers didn't even notice it was happening."

**Alex**: Wait, hold on. Eleven million users migrated invisibly? That's not just platform engineering. That's platform engineering maturity.

**Jordan**: Exactly. That's the benchmark. Not "we built a thing," but "we solved the problem so well that users didn't have to think about it."

**Alex**: Okay, give me more examples. Who else is doing this right?

**Jordan**: Bloomberg. Running Kubernetes since version one point three in twenty sixteen. Nine years. They created Kserve, formerly KFServing, now a CNCF incubating project. Platform team operates thousands of nodes.

**Alex**: Nine years. That's the timeline most companies don't want to hear.

**Jordan**: But it's the realistic timeline. ByteDance open sourced AI Brix, their internal AI infrastructure platform. Four thousand plus GitHub stars since early twenty twenty-five. Eighty percent of contributors now external to ByteDance. Lee Guang said "this is the spirit of open collaboration."

**Alex**: Wait, eighty percent external? That's basically community-driven at this point.

**Jordan**: Which changes the sustainability model. ByteDance isn't maintaining this alone anymore. And Airbnb talked about the agentic shift. Majority of developers now using agentic coding tools. Platform teams preparing for AI-assisted development workflows.

**Alex**: That's a curveball. How do platforms serve AI agents, not just humans?

**Jordan**: Unanswered question. But it's on the roadmap. Here's the pattern, though. All these success stories share three things: Multi-year timelines. Bloomberg took nine years. Operational support. Intuit's "done for you." And open collaboration. ByteDance with eighty percent external contributors.

**Alex**: None of this happens in six months with a small team and no support.

**Jordan**: Correct. Which brings us to something less intimidating. The EU Cyber Resilience Act. CRA. Headlines made it sound terrifying. Greg Kroah-Hartman clarified.

**Alex**: Okay, what's the real story?

**Jordan**: Individual contributors are NOT liable. The requirements for maintainers are: One, security contact—an email address. Two, report vulnerabilities when fixed. Three, generate an SBOM, Software Bill of Materials.

**Alex**: That's it?

**Jordan**: That's it. Timeline: September twenty twenty-six, enforcement for manufacturers. December twenty twenty-seven, full compliance for open source stewards. And Greg said explicitly, quote, "If you're contributing to an open source project, you do not have to worry about it. It's not an issue."

**Alex**: So the panic was overblown.

**Jordan**: Mostly. The takeaway for platform teams is start SBOM generation now. Tools exist—Syft, SPDX. The twenty twenty-seven deadline is manageable if you start Q one twenty twenty-five.

**Alex**: Alright. So we have three principles, proven patterns at billion-dollar scale, real adoption stories. Sounds like platform engineering is... solved?

**Jordan**: Technically? Yeah, mostly. Which makes what happened next at KubeCon even more striking.

**Alex**: What happened?

**Jordan**: The Kubernetes Steering Committee Q and A session. This wasn't a celebration. It was a sobering discussion.

**Alex**: Wait, they just hit a diversity milestone, right? New members, Cat Cosgrove as release lead for K8s one point thirty?

**Jordan**: Correct. Achievement unlocked. But immediately, the hard truths started coming out. One steering committee member said, quote, "The reward for good work is more work. If you're good at your work, you get even more work assigned."

**Alex**: That's... not sustainable.

**Jordan**: And then Cat Cosgrove, newly elected, said "I'm ready to abandon ship. Like, it's so much work."

**Alex**: Hold on. She just got elected and she's already talking about quitting?

**Jordan**: That's the point. The governance structure—multiple SIGs, working groups, committees—the work is valuable but endless. And no one knows how to sustain leadership without burnout. Companies don't give employees dedicated time for community work.

**Alex**: So people are doing this nights and weekends?

**Jordan**: Many are. Or they're burning out in their day jobs because they're doing both. And then an audience member asked a provocative question. Quote, "There's not enough people stepping up...but maybe do we need to look at is there just too much landscape?"

**Alex**: Oh. That's the OpenStack comparison. The "big tent" problem.

**Jordan**: Implied, yes. CNCF now has two hundred plus projects. Is that sustainable?

**Alex**: This is uncomfortable. We just celebrated consensus and success stories, and now we're talking about people ready to quit.

**Jordan**: That's the honest part of this episode. Platform engineering has clarity now. The technology is understood. But the people building this ecosystem are showing serious strain.

**Alex**: So what's the answer? You can't just tell people "don't burn out."

**Jordan**: No. But you can be honest that this is the cost. Jordan Liggitt and Davanum Srinivas talked about dependency management. Kubernetes reduced dependencies from four hundred sixteen to two hundred forty-seven over three years. The philosophy was "patient, pragmatic, persistent."

**Alex**: Okay, but what does that have to do with burnout?

**Jordan**: Work upstream to fix root causes. Don't patch locally. This takes longer but prevents recurring problems. Applied to community sustainability: If maintainers burn out, everyone's problem. If the best people leave, everyone loses. Upstream investment in community health equals downstream platform stability.

**Alex**: So companies benefiting from open source need to invest in maintainer support?

**Jordan**: Bloomberg does. Google does. Microsoft does. They pay engineers to maintain open source. But most companies don't. And then they wonder why critical infrastructure has one or two maintainers working nights and weekends.

**Alex**: That's free-riding.

**Jordan**: Exactly. And it's not sustainable. So let's synthesize. The good news: Platform engineering has clear principles. Proven patterns at billion-dollar scale. Industry alignment. The hard truth: Multi-year investment required. Bloomberg took nine years. Managed service approach means ongoing commitment. And community sustainability isn't solved.

**Alex**: So is platform engineering... solved?

**Jordan**: The technology part? Yeah, mostly. Three principles, proven patterns, clear anti-patterns. The people part?

**Alex**: Ask me again in five years.

**Jordan**: Right. So if you're starting a platform team, here's the framework. DO: Commit to managed service approach, not just templates. Measure business metrics, not just infrastructure. Plan for a three-to-five-year timeline. Start SBOM generation now for CRA compliance by twenty twenty-seven.

**Alex**: And the DON'Ts?

**Jordan**: Don't expect results in six to twelve months. Don't build templates without operational support—that's the "puppy for Christmas" problem. Don't measure only infrastructure metrics. And don't ignore community health if you're involved in open source.

**Alex**: Red flags?

**Jordan**: Platform team expected to transform the organization in less than twelve months. No dedicated maintainer support from the company. Chasing diversity without addressing burnout. Adding CNCF projects without sunset criteria.

**Alex**: That last one's interesting. So you're saying growth without discipline?

**Jordan**: Right. Kubernetes went from four hundred sixteen dependencies to two hundred forty-seven through intentional curation. Same discipline needed for project adoption. If you can't sustain it, don't add it.

**Alex**: Okay, so what's the Intuit model we should emulate?

**Jordan**: "Done for you" approach. Built into the platform, not optional. Invisible migration—eleven million users didn't notice. Multi-year commitment to a twenty-year-old codebase. Platform engineering success isn't about tools. It's about sustained organizational commitment.

**Alex**: So the bar is... high.

**Jordan**: The bar is realistic. Platform engineering is infrastructure at organizational scale. Intuit migrated Mailchimp. Bloomberg ran K8s for nine years. ByteDance open sourced AI Brix. None of this happens in six months with a small team and no support.

**Alex**: And Cat Cosgrove's burnout warning?

**Jordan**: Is a reminder that technical problems are solvable. People problems require different thinking. Platform engineering in twenty twenty-five: We know what to build. Now figure out how to sustain who builds it.

**Alex**: That's the takeaway. Three principles clarify the "what." Real-world adoption proves it works. But sustainability—for platforms and for people—requires long-term thinking.

**Jordan**: Bloomberg's nine-year journey isn't an outlier. It's the baseline. Intuit's "done for you" approach isn't optional. It's the definition. And the community burnout conversation isn't pessimism. It's honesty.

**Alex**: So when people ask "should we start a platform team?"

**Jordan**: Ask back: Are you ready for a three-to-five-year investment? Can you commit to managed service, not just templates? Will you measure business impact, not just uptime? And if you're leveraging open source, are you contributing back?

**Alex**: If the answers are no...

**Jordan**: Then you're not ready for platform engineering. You're ready for a different solution. And that's fine. The worst outcome is starting a platform initiative with the wrong expectations and then disbanding the team eighteen months later.

**Alex**: Which is that seventy percent failure rate from Episode eleven.

**Jordan**: Exactly. KubeCon twenty twenty-five gave us clarity. Use it. The principles are clear. The patterns are proven. The timelines are realistic. And the honest conversation about sustainability is the foundation for the next decade.

**Alex**: Tomorrow in Part 3, we go deeper into that sustainability question. Maintainer burnout. The CNCF at ten years. What the community learned, what's still unsolved, and what the next ten years might look like.

**Jordan**: This has been Part 2 of our three-part KubeCon Atlanta coverage. If you're starting a platform team, commit to the managed service approach. If you're running one, measure business metrics. And if you're benefiting from open source, invest in the people maintaining it.

**Alex**: See you tomorrow for Part 3.
