---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #025: SRE Reliability Principles"
slug: 00025-sre-reliability-principles
---

# SRE Reliability Principles: The 26% Problem

## The Platform Engineering Playbook Podcast

<GitHubButtons />

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, overflow: 'hidden', maxWidth: '100%', marginBottom: '2rem'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/uqbwE4RfrhQ"
    title="YouTube video player"
    frameBorder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowFullScreen>
  </iframe>
</div>

**Duration:** 15 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

---

**Jordan**: Today we're diving into Site Reliability Engineering principles and a stat that's been bugging me. Only twenty-six percent of organizations actively use SLOs in production. After more than a decade of Google's SRE book being treated as gospel, why are three-quarters of companies still not implementing the core practice?

**Alex**: That's the reverence-reality gap. Everyone talks about error budgets and SLOs at conferences, puts SRE in job titles, but actual implementation? Way lower than you'd expect.

**Jordan**: Exactly. And meanwhile, forty-nine percent of those same organizations say SLOs are more relevant now than last year. So it's not that people think it's irrelevant—they just can't make it work.

**Alex**: Right. And we've got this whole Platform Engineering movement creating confusion about where SRE even fits. Platform Engineers averaging a hundred fifteen thousand dollars, SREs at one twenty-seven thousand, and teams asking "do we need both?"

**Jordan**: Yeah, and then you add AI and ML systems, multi-cloud chaos, and suddenly the playbook from twenty sixteen feels... incomplete. Are the principles wrong, or is implementation just broken for twenty twenty-five's complexity?

**Alex**: That's what we need to figure out. Because there's real wisdom in Google's SRE principles—embracing risk, error budgets, blameless postmortems. But the world got more complex than the original model assumed.

**Jordan**: Okay, let's start with what Google got right. What are the timeless principles that still work universally?

**Alex**: Error budgets are brilliant. They transform reliability from political arguments into data-driven decisions. If your target is ninety-nine point nine percent availability, you have a zero point one percent error budget. That's one thousand failures per million requests over four weeks.

**Jordan**: So instead of arguing whether we should deploy on Friday, you look at the error budget.

**Alex**: Exactly. When you have budget remaining, release fast. When it's depleted, focus on stability. Google says it beautifully in their SRE book: "Extreme reliability comes at a cost—maximizing stability limits how fast new features can be developed."

**Jordan**: And users can't even tell the difference between ninety-nine point ninety-nine percent and ninety-nine point nine-nine-nine percent.

**Alex**: Right. So why spend engineering effort on that last nine? Google's approach is to treat the availability target as both a minimum and a maximum. Don't over-engineer.

**Jordan**: Okay, but here's a concrete example. If I have a ninety-nine point nine-nine-nine percent quarterly SLO, and a problem consumes zero point zero-zero-zero-two percent of my queries, how much of my quarterly budget did I just spend?

**Alex**: Twenty percent. That tiny problem just burned one-fifth of your quarterly error budget. And if a single incident consumes over twenty percent of your quarterly budget, Google's policy requires a postmortem with highest-priority remediation actions.

**Jordan**: So the math is elegant. The philosophy makes sense. Why is adoption only twenty-six percent?

**Alex**: Because implementation reality is brutal. First, technical challenges. Observability data is siloed across Splunk, Prometheus, service mesh platforms. Teams need architecture maps just to know which vendor each service uses.

**Jordan**: And manually tracking error budgets is...

**Alex**: Impossible at scale. You need automation. But here's the kicker—eighty-five percent of organizations adopted OpenTelemetry. The tools exist. Only twenty-six percent are actually using SLOs. So it's not a tooling problem, it's a process problem.

**Jordan**: What about organizational challenges?

**Alex**: Culture transformation is harder than anyone admits. Successfully implementing SLOs requires real commitment to culture and process transformation, which is often harder than anticipated. And the biggest challenge? Setting unrealistic targets.

**Jordan**: Like promising ninety-nine point ninety-nine percent uptime.

**Alex**: Which allows only fifty-two minutes of downtime per year. Most teams promise that without understanding the math. Then they blow through it in the first month and the SLO becomes ignored.

**Jordan**: So teams set targets they can't meet, which undermines the whole system.

**Alex**: Right. And error budgets only work when product managers, developers, and SREs all understand and buy into the system. That cross-functional alignment is rare in practice. One team told me their product managers thought error budget was "something the SRE team tracks."

**Jordan**: Ouch. But wait, isn't this stuff supposed to be mature by now? What changed?

**Alex**: Three big shifts since the original SRE book. First, AI and ML systems break traditional SRE assumptions. You need data freshness SLOs—how recently did the model get data for inference? Stale data equals bad inferences.

**Jordan**: And downtime costs are different.

**Alex**: Catastrophically different. LLM training takes weeks. One downtime incident might burn tens of thousands of dollars in compute. Traditional error budgets don't map to that economic reality.

**Jordan**: What about Platform Engineering? Everyone's talking about it, but how does it relate to SRE?

**Alex**: Platform Engineering focuses on developer velocity and experience. SREs focus on maximum reliability. The way I think about it—Platform Engineers build systems that SREs operate. Collaboration is key, but roles are getting confused.

**Jordan**: Glassdoor shows Platform Engineers at one-fifteen thousand, SREs at one-twenty-seven thousand. Partly because SREs are handling two a.m. incidents.

**Alex**: Exactly. Platform Engineering life is more predictable. But here's the thing—they're complementary, not competitive. Platform teams can use SRE principles to build more reliable platforms. SRE teams can use Platform Engineering tools to improve reliability.

**Jordan**: Hold on. Even Google is evolving their approach?

**Alex**: Yeah, this surprised me. Traditional SRE methods—SLOs, error budgets, postmortems, progressive rollouts—hit a limit with highly complex systems. Google SRE is now adopting STAMP, which stands for Systems-Theoretic Accident Model and Processes. They're bringing in systems theory and control theory for a new approach to reliability.

**Jordan**: So if even the originators are saying "the original model has limits," what does that mean for the rest of us?

**Alex**: It means the principles are timeless, but implementation must evolve. Let's talk about what to keep versus what to adapt for twenty twenty-five.

**Jordan**: What works universally, regardless of complexity?

**Alex**: Four things. Error budget philosophy—aligning product and reliability incentives through data. Embracing risk—availability as both minimum and maximum to avoid over-engineering. Blameless postmortems—the twenty twenty-four CrowdStrike incident reinforced how critical this is. And toil reduction—keeping repetitive work below fifty percent of engineer time.

**Jordan**: Those don't change.

**Alex**: Right. But how you implement them must adapt. You can't do SLO instrumentation manually anymore. You need OpenTelemetry plus automated SLI calculation plus incident integration. Spreadsheets don't scale.

**Jordan**: What about ML systems specifically?

**Alex**: Add ML-specific SLOs. Model freshness, prediction latency, training pipeline success rate. And your error budget math needs to factor in training costs. One failure might burn tens of thousands in compute, so the cost per incident is different.

**Jordan**: And Platform Engineering teams?

**Alex**: Adopt SRE principles for your platform. Your platform is a product—it needs SLOs. Deployment success rate, time-to-environment, self-service completion rate. Then provide SLO infrastructure for app teams—build the observability and error budget dashboards they need.

**Jordan**: Okay, here's my controversial take. Maybe twenty-six percent adoption isn't a failure. Maybe not every organization needs formal SLOs.

**Alex**: I've been thinking about that. You're right that not everyone needs the full SRE apparatus. But everyone needs error budget thinking. Understanding "we have capacity for X failures this month, how do we spend that budget?" Even without formal SLOs, that mindset helps.

**Jordan**: So let's get practical. What if I'm starting from zero?

**Alex**: Pick three to five critical services. Not everything—your top revenue generators or highest-impact platforms. Define one SLO per service initially. Availability or latency, not both. Ninety-nine point nine percent is reasonable—that's forty-three minutes of downtime per month.

**Jordan**: Automate from day one?

**Alex**: Absolutely. OpenTelemetry to automated SLI collection to error budget dashboard. No spreadsheets. Get cross-functional buy-in—your product manager must understand the "we have four hundred failures left this month" decision framework. And target a twelve-month timeline. From zero to making release decisions based on error budget takes a year, not a quarter.

**Jordan**: What if SLOs exist but everyone ignores them?

**Alex**: Audit why. Ask teams—too complex? Wrong metrics? No enforcement? No tooling? Then simplify radically. Cut to three SLOs maximum per service, each tied to actual user pain. Enforce once—next error budget breach, actually freeze releases. Demonstrate it's real.

**Jordan**: And automated reporting?

**Alex**: Weekly error budget burn emails to product and engineering leadership. Make the data visible.

**Jordan**: What about Platform Engineering teams listening to this?

**Alex**: Three things. First, adopt SRE principles for your platform—deployment success rate, environment provision time, self-service completion. Second, provide SLO infrastructure—build dashboards and error budget tracking for app teams. Third, collaborate with SRE—you're complementary, not competitive.

**Jordan**: And if I have AI or ML systems?

**Alex**: Read "Reliable Machine Learning" from Google's SRE team—it's specifically about applying SRE to ML. Add ML-specific SLOs for model freshness and training pipeline reliability. And factor training costs into error budget math—one failure might cost fifty K.

**Jordan**: What's actually happening in twenty twenty-five? What's the reality on the ground?

**Alex**: Chaos Engineering market went from four point nine billion in twenty twenty-three to a projected thirty-two point seven-five billion by twenty thirty-two. That's twenty-three point five percent annual growth. Google, Microsoft, AWS all released chaos engineering frameworks in twenty twenty-four.

**Jordan**: So investment in reliability tooling is exploding.

**Alex**: Right. Ninety percent of organizations are planning significant cloud strategy changes. Hybrid cloud is critical for forty-eight percent. AI adoption is accelerating. And here's the shift—execution challenges are overtaking adoption as the primary concern.

**Jordan**: It's not "should we do SRE?" anymore. It's "how do we adapt SRE for our complexity?"

**Alex**: Exactly. Here's your practical next step. This week, pick your top three services. For each, answer three questions. What's our availability target? What's our error budget? Who enforces it? If you can't answer all three, you don't have SRE—you have hope.

**Jordan**: That's brutal but fair.

**Alex**: And here's the thing—the twenty-six percent adoption rate isn't a condemnation of SRE principles. It's evidence that implementation is hard. But the principles remain: measure reliability, budget for failure, automate toil, learn from incidents. The implementation must evolve for twenty twenty-five's complexity, but the philosophy is timeless.

**Jordan**: So what's your take on the Platform Engineering versus SRE question we started with?

**Alex**: They're two sides of the same coin. Platform Engineering builds the systems. SRE ensures they're reliable. The tension only exists when organizations force them to compete. When they collaborate, you get fast developer velocity and high reliability.

**Jordan**: And both can use the same core principles—error budgets, embracing risk, blameless learning.

**Alex**: Right. Whether you're a Platform team tracking deployment success rate or an SRE team tracking service availability, the error budget framework works. It aligns incentives. It turns politics into data.

**Jordan**: Final thought—if you're in an organization where SRE hasn't stuck, don't assume the principles are wrong. Look at implementation. Are targets realistic? Is tracking automated? Do product managers understand error budgets? Is there executive sponsorship?

**Alex**: And remember—formal SLOs aren't the only path. Some organizations do reliability reviews without formal SLOs. Some use simpler metrics. The goal isn't orthodoxy—it's reliable systems that enable fast iteration.

**Jordan**: Pick three services, answer three questions, start this week.

**Alex**: Measure reliability. Budget for failure. Automate toil. Learn from incidents. Those principles work in twenty twenty-five just like they did in twenty sixteen. The tools and techniques evolve, but the philosophy remains timeless.
