---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #011: Platform Team Failures"
slug: 00011-platform-failures
---

# Why 70% of Platform Engineering Teams Fail (And the 5 Metrics That Predict Success)

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 12 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/2025/10/28/why-platform-engineering-teams-fail)**: Deep dive into the data, 90-day playbook, and comprehensive decision framework.

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, margin: '1.5rem 0'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/7zAAZ924kSA"
    title="Why 70% of Platform Engineering Teams Fail (And the 5 Metrics That Predict Success)"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>

---

**Jordan**: Today we're diving into a mystery that's costing companies millions and derailing careers. Why do 70% of platform engineering teams fail to deliver meaningful impact? We're talking about technically excellent teams with senior engineers, modern tools, executive buy-in—and yet 45% are disbanded within 18 months.

**Alex**: It's wild. August 1st, 2012, nine thirty AM. Knight Capital deploys new trading software. By ten fifteen AM, 440 million dollars evaporated. The CEO later said, "We had the technology. We had smart people. What we didn't have was the right operating model."

**Jordan**: And that's the pattern we're seeing in 2025. These aren't startups with junior teams. These are Fortune 500 companies hiring senior engineers with 450 thousand dollar budgets. So what's actually going wrong?

**Alex**: That's what we're going to solve today. We'll uncover three critical failures that predict disaster, and more importantly, give you five metrics that predict success with startling accuracy.

**Jordan**: Let's start with the financial stakes. A 3-person platform team costs at least 450K annually. At scale, we're talking 25 engineers, 3.75 million dollars per year. And platform leaders get maybe 12 to 18 months to prove value before teams get restructured.

**Alex**: Right, and when platforms fail, developer productivity stays stuck. On-call burden actually increases. Deployment times don't improve. It's not neutral—it's actively making things worse.

**Jordan**: So here's our investigation. Three discoveries that explain why technically excellent platforms fail. First one—the product management gap.

**Alex**: Only 33% of platform teams have dedicated product managers. Yet 52% say PMs are crucial to success. That 19-point gap is the smoking gun.

**Jordan**: Walk me through the evidence.

**Alex**: Look at Spotify's Backstage. They have a PM. They achieved 99% voluntary adoption. Now look at external Backstage adopters—most lack a PM. Average adoption? 10%.

**Jordan**: Wait, so same technology, completely different outcomes.

**Alex**: Exactly. The pattern is clear. Teams with PMs are 3 times more likely to achieve over 50% adoption. Without a PM, platform teams build what's technically interesting instead of what developers actually need.

**Jordan**: What does that look like in practice?

**Alex**: No roadmap prioritization. Everything's equally important. Can't say no to feature requests, so the platform becomes a junk drawer. I've seen Backstage implementations that overwhelm developers with 50 plugins. Nobody knows where to start.

**Jordan**: So they nail the engineering but miss the product entirely.

**Alex**: Yeah, and that leads directly to our second discovery—metrics blindness. 45% of platform teams don't measure anything meaningful. They can tell you uptime but not whether developers are actually more productive.

**Jordan**: The 2024 DORA report had some shocking findings on this, right?

**Alex**: Oh man, yeah. Platform teams decreased throughput by 8%. Decreased stability by 14%. Platforms make things worse before they make them better. But teams without baselines never know if they've crossed into better territory.

**Jordan**: So what does this look like when you can't prove ROI?

**Alex**: Real example: team builds a beautiful CI/CD pipeline. Deploys it to production. Can't prove it saved any time. Gets cut in the next budget round. They claimed "we saved 30% deployment time" but 30% of what? They never measured before.

**Jordan**: That's painful. What's the third discovery?

**Alex**: The force adoption trap. Mandating platform adoption creates resistance, shadow IT, and developer resentment.

**Jordan**: Because developers value autonomy.

**Alex**: Exactly. They're builders. Forced tools feel like surveillance and control. So they route around the platform to "get real work done." We've seen NPS scores drop below negative 20—that's legacy platform territory.

**Jordan**: How did Spotify avoid this?

**Alex**: They made Backstage the easiest path, not the required path. That's how you get 99% voluntary adoption. Developers chose it because it made them more productive, not because they were forced to use it.

**Jordan**: Okay, here's where I want to push back though. Surely the technical decisions matter. Like, choosing Backstage versus building something homegrown. Or AWS versus bare metal.

**Alex**: That's what everyone thinks. But look at the data. Teams succeed and fail with both approaches. You can fail spectacularly with Backstage. You can succeed with homegrown tools. The technology choice doesn't predict the outcome.

**Jordan**: So what does?

**Alex**: Treating platform engineering as a product problem instead of an engineering problem. Hiring engineers when you need product managers. Measuring outputs like features shipped instead of outcomes like developer productivity. Building for hypothetical future scale instead of current pain points.

**Jordan**: The irony is brutal. The engineering is usually excellent. The platforms are technically sound.

**Alex**: But nobody uses them. Which brings us to the solution—the 5 predictive metrics. These predict success with remarkable accuracy.

**Jordan**: Let's go through them.

**Alex**: Metric one: Product Manager exists. Binary—yes or no. If no, you're 3 times less likely to achieve 50% adoption. If yes, you can prioritize ruthlessly, say no strategically, build incrementally.

**Jordan**: Metric two?

**Alex**: Pre-platform baseline established. This is measured before platform work starts. Current deployment time, MTTR, time to onboard new engineers. Without this, you can't prove ROI, can't defend your budget.

**Jordan**: But with it?

**Alex**: You can say "we reduced deployment time from 45 minutes to 6 minutes." Concrete, defensible value.

**Jordan**: Metric three—developer NPS.

**Alex**: Over zero is good. Over 20 is great. Over 50 is amazing. Over 80 is top percentile. Spotify achieved 76 for Backstage. Under negative 20 means active resistance.

**Jordan**: And you measure this quarterly?

**Alex**: Yeah, to show the trend. If NPS is going down despite iterations, you've got a fundamental problem with your value proposition.

**Jordan**: Metric four—voluntary adoption over 50% within 12 months.

**Alex**: Right, and forced adoption doesn't count. This measures whether developers choose the platform. The adoption curve typically looks like this: zero to six months you get innovators, maybe 10 to 20% adoption. Six to 12 months, you hit mainstream—that's when you should cross 50%.

**Jordan**: And if you're under 50% at 12 months?

**Alex**: Something's fundamentally wrong. Time to reassess.

**Jordan**: Last one—metric five. Time to first value under 30 days.

**Alex**: From "I want to try the platform" to "I got real value." Seven days or less is excellent—that's GitHub Actions territory. 30 days is acceptable. Gives teams a chance to prove ROI before losing attention. Over 30 days? Platform's too complex.

**Jordan**: Okay, so we've got the 5 metrics. How do we use them? When should you actually build a platform team?

**Alex**: Under 10 engineers—don't. The overhead exceeds the benefits. Around 30 engineers, platform work becomes someone's full-time job. Consider one engineer. At 100 plus engineers, pain points justify a dedicated team. Start with 3 people—one PM, two engineers.

**Jordan**: And at scale?

**Alex**: At 1000 plus engineers, a full platform team of 15 to 25 can deliver 380% ROI. We're talking 18 million in value on a 3.75 million dollar cost.

**Jordan**: Give me the first 90 days playbook.

**Alex**: One, establish baselines. Deployment time, MTTR, onboarding time. Two, hire the PM before the second engineer. Three, interview 10 plus developers. Find common pain points. Four, build the smallest MVP that solves one pain point. Five, find 2 to 3 pilot teams—early adopters willing to give feedback. Six, measure NPS at 30 days. Seven, target under 30 days time to first value. Eight, track voluntary adoption weekly.

**Jordan**: What are the red flags to kill the project?

**Alex**: NPS under zero after 6 months despite iterations. Under 10% adoption after 6 months. Can't establish a measurable baseline. Or the organization's under 100 engineers without acute pain.

**Jordan**: So coming back to our opening question—why do 70% of platform teams fail? It's not the technology.

**Alex**: It's not. It's the absence of product thinking. It's metrics blindness. It's forcing adoption instead of earning it. Knight Capital had the technology and smart people. What they lacked was the operating model and the metrics.

**Jordan**: And the 5 metrics we covered—PM exists, baseline established, NPS over 20, voluntary adoption over 50%, time to value under 30 days—these are your early warning system.

**Alex**: Right. Here's what you can do Monday morning. One, check if you have a PM. If no, that's your top priority. Two, measure your current state. What's the deployment time? MTTR? Onboarding time? Three, send an NPS survey to developers who've tried the platform. Four, calculate time to first value. How long does it take a new team to get value? Five, based on these 5 metrics, are you on track? If not, what changes by next quarter?

**Jordan**: The platforms that succeed aren't the ones with the best technology. They're the ones that measure the right things and treat platform engineering as a product discipline. The fundamentals remain constant even as the landscape evolves.
