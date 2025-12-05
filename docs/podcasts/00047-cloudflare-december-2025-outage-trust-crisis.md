---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #047: Cloudflare's Trust Crisis"
slug: 00047-cloudflare-december-2025-outage-trust-crisis
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #047: Cloudflare's Trust Crisis - December 2025 Outage and the Human Cost

<GitHubButtons />

**Duration**: 12 minutes | **Speakers**: Jordan & Alex

**Target Audience**: Platform engineers, SREs, and DevOps engineers dealing with infrastructure dependencies and on-call stress

> 📝 **Read the [full blog post](/blog/cloudflare-december-2025-outage-trust-infrastructure-concentration-risk)**: Deep analysis of Cloudflare's pattern of outages, reputation damage, and what platform teams should do about infrastructure concentration risk.

---

## Watch the Episode

*YouTube embed coming soon*

---

## Synopsis

Three weeks after their worst outage since 2019, Cloudflare went down again. On December 5, 2025, a Lua code bug took down 28% of HTTP traffic for 25 minutes - the sixth major outage of 2025. Beyond the technical postmortem, this episode examines the pattern of repeated failures, community reactions, and the often-overlooked human cost to on-call engineers who bear the burden of infrastructure dependencies they can't control.

---

## Chapter Markers

- **00:00** - Introduction & News Segment
- **01:30** - The December 5 Incident
- **03:00** - Technical Root Cause: Lua Killswitch Bug
- **04:30** - The Pattern: Six Outages in 2025
- **06:00** - Community Reactions
- **07:00** - The Human Cost: On-Call Engineers
- **09:00** - What Platform Teams Should Do
- **10:30** - Multi-CDN Strategies
- **11:15** - Closing Thoughts

---

## News Segment (December 5, 2025)

- **KubeCon Platform Engineering Survey**: 219 teams surveyed on AI and IDP adoption
- **GitHub Actions Upgrade**: Workflow dispatch now supports 25 inputs (up from 10)
- **Hybrid Cloud-Native Networking**: Louis Ryan's presentation on the "Big IP problem"

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| HTTP Traffic Impacted | 28% | Cloudflare Blog |
| Outage Duration | 25 minutes | Cloudflare Blog |
| Days Since Last Outage | 17 | November 18 → December 5 |
| Major 2025 Outages | 6 | Cloudflare Status History |
| IT Professional Burnout | 67% | 2024 State of DevOps |
| Global Burnout Rate | 1 in 4 | McKinsey |

---

## The Six Outages of 2025

| Date | Duration | Cause |
|------|----------|-------|
| March 21 | 1hr 7min | R2 credential rotation |
| June 12 | 2hr 28min | Workers KV degradation |
| July 14 | 62 min | 1.1.1.1 DNS topology |
| September | Hours | Dashboard/API outage |
| November 18 | 4+ hours | Bot Management Rust panic |
| December 5 | 25 min | Lua killswitch bug |

---

## Key Takeaways

1. **Multi-CDN is no longer optional** - Organizations with multi-CDN strategies had zero impact from both November and December outages
2. **External monitoring is critical** - If your monitoring runs through your CDN, it's blind when that CDN fails
3. **On-call wellness matters** - 67% burnout rate; getting paged for dependencies you can't control is a retention risk
4. **Runbooks for provider failures** - Do you have a playbook for "major provider is down"?
5. **Complexity outpaces safeguards** - As systems grow, operational maturity must scale proportionally

---

## Transcript

**Jordan:** Today we're tackling something that's hitting close to home for a lot of platform teams right now. But first, let's check the pulse of platform engineering.

**Jordan:** KubeCon surveys are in, and the data is fascinating. The New Stack polled two hundred nineteen platform teams at KubeCon, and the results show AI adoption in platform engineering is accelerating fast. We're seeing teams integrate AI into everything from incident response to capacity planning. Worth reading if you're building your twenty twenty-six roadmap.

**Jordan:** GitHub Actions got a quality-of-life upgrade. Workflow dispatch now supports twenty-five inputs, up from just ten. If you've ever hit that limit trying to parameterize complex deployment pipelines, you know how painful that ceiling was.

**Jordan:** And Louis Ryan from Google gave a presentation on hybrid cloud-native networking that's getting a lot of attention. He critiques what he calls the "big IP problem" and rigid security policies that become single points of failure. Relevant to today's main topic, actually.

**Jordan:** Speaking of which, let's talk about the elephant in the room. Cloudflare went down again this morning. And if you're having déjà vu, you should be.

**Alex:** Three weeks. That's how long it took for Cloudflare to have another major outage. December fifth, twenty twenty-five, eight forty-seven UTC, twenty-eight percent of HTTP traffic goes down. LinkedIn, Zoom, Fortnite, ChatGPT, Shopify, Coinbase. Sound familiar?

**Jordan:** We covered their last outage in Episode thirty just three weeks ago. That one was the Rust panic in their bot management system that took down twenty percent of the internet for over four hours. This time it was twenty-five minutes, but the pattern is what concerns me.

**Alex:** Let's break down what happened this morning. Cloudflare was deploying a killswitch to disable a rule in their web application firewall. This was part of mitigating the React Server Components CVE that hit the industry this week.

**Jordan:** So they were trying to protect customers from a security vulnerability.

**Alex:** Exactly. And in doing so, they triggered a Lua code bug that had existed undetected for years. When the killswitch disabled a rule with an "execute" action type, the code tried to access an object that wasn't there. Classic nil value access.

**Jordan:** The error message was literally "attempt to index field execute, a nil value." Line three fourteen of their init dot lua file.

**Alex:** The thing is, this code path had never been exercised before. They'd never applied a killswitch to this specific rule type. Lua doesn't have strong type checking, so the bug just sat there, dormant, waiting for the exact conditions to trigger it.

**Jordan:** Walk me through the timeline.

**Alex:** Eight forty-seven UTC, the bad configuration deploys. Eight forty-eight, it's propagated across the entire network. No gradual rollout, just instant global deployment. Eight fifty, automated alerts fire. Nine eleven, they initiate the rollback. Nine twelve, full restoration.

**Jordan:** Twenty-five minutes total. But two minutes for alerts to fire after global propagation?

**Alex:** That's one of the things the community is criticizing. Two minutes might not sound like much, but when you're talking about twenty-eight percent of HTTP traffic, that's millions of failed requests per second.

**Jordan:** And this is where the pattern becomes impossible to ignore. Let me run through Cloudflare's twenty twenty-five track record.

**Alex:** Please do.

**Jordan:** March twenty-first, one hour seven minutes down. R2 credential rotation error. June twelfth, two hours twenty-eight minutes. Workers KV, Access, and WARP degraded. July fourteenth, sixty-two minutes. Their one dot one dot one dot one DNS resolver topology change gone wrong. September, the dashboard and API outage that lasted hours. November eighteenth, four-plus hours, the bot management Rust panic we covered in Episode thirty. And now December fifth, twenty-five minutes, this Lua killswitch bug.

**Alex:** That's six major outages in nine months for a company that handles twenty percent of all internet traffic.

**Jordan:** The community reaction has been... pointed. On Hacker News, someone calculated that Cloudflare is now below ninety-nine point nine percent uptime for the year.

**Alex:** Which, to be fair, Cloudflare would probably dispute based on how they calculate their SLAs. But the perception matters as much as the math.

**Jordan:** One of my favorite comments was "Wanted to check if Cloudflare is down, went to Downdetector dot com... Downdetector runs on Cloudflare too." Even the outage tracking site was down.

**Alex:** The irony of a security fix causing an outage isn't lost on people either. Someone wrote "the risk mitigation system became the systemic risk itself."

**Jordan:** Let's talk about something that doesn't get enough attention in these postmortems. The human cost.

**Alex:** This is where it gets real for me. We focus so much on the technical root cause, the timeline, the blast radius. But somewhere, there's an on-call engineer who got paged at three AM for something that wasn't their fault and that they couldn't fix.

**Jordan:** The twenty twenty-four State of DevOps report found that sixty-seven percent of IT professionals experience burnout. And on-call rotations are a huge contributor. You're supposed to allocate thirty to forty percent of your work bandwidth during an on-call shift just for incident response.

**Alex:** But what happens when the incidents aren't yours to fix? Your app is down. Your customers are angry. Your status page shows red. And you're sitting there watching Cloudflare's status page, waiting for them to fix it.

**Jordan:** McKinsey found that one in four employees globally experience burnout symptoms. And I'd bet platform engineers dealing with infrastructure dependencies they can't control are overrepresented in that statistic.

**Alex:** Think about what happens in those twenty-five minutes. Your monitoring lights up. PagerDuty goes off. You jump online, start investigating. Is it us? Check the code, check the deploys, check the database. Nothing changed on our side.

**Jordan:** Then you start the external investigation. Is it AWS? Is it our DNS? Is it... oh, Cloudflare is down. Great.

**Alex:** And now you're in communications mode. Update the status page. Tell leadership. Respond to the angry Slack messages. Explain to customers that it's not your fault but you're working on it.

**Jordan:** "Working on it" meaning "watching someone else's status page and hoping."

**Alex:** And when it comes back, you have to deal with the aftermath. The recovery traffic spike. The stuck requests. The cache invalidation. The explaining to leadership why your SLAs are busted this month.

**Jordan:** The emotional toll is real. You're responsible for reliability, but you can't control the infrastructure you depend on. That mismatch between responsibility and control is a recipe for burnout.

**Alex:** And it keeps happening. Two outages in three weeks. How do you build a culture of reliability when your foundational dependencies are unreliable?

**Jordan:** So what do we actually do about this?

**Alex:** The organizations that sailed through both the November and December outages had one thing in common. Multi-CDN strategies. They weren't dependent on a single provider.

**Jordan:** That's not always practical for smaller teams, but even basic redundancy helps. Can your critical paths fall back to direct connections if your CDN fails?

**Alex:** Synthetic monitoring is crucial, and it needs to be outside your CDN. If you're monitoring through Cloudflare and Cloudflare goes down, your monitoring is blind.

**Jordan:** We've talked before about runbooks for internal incidents. But do you have a runbook for "major provider is down"? What's the communication plan? What can you actually do versus what do you just have to wait out?

**Alex:** And this is the one that I think gets overlooked. Your on-call wellness is a legitimate engineering concern. If your team is getting paged for things they can't control, that's not just frustrating, it's a retention risk.

**Jordan:** Cloudflare, for their part, has promised improvements. Enhanced gradual rollouts with health validation. Fail-open error handling instead of hard crashes. They say they'll publish detailed resiliency projects before the end of next week.

**Alex:** And we'll see. The November postmortem made similar promises, and here we are three weeks later.

**Jordan:** The pattern I'm seeing isn't just technical. It's organizational complexity outpacing operational safeguards. Cloudflare has grown enormously. Their infrastructure is incredibly sophisticated. But sophistication creates more failure modes, and their processes haven't kept pace.

**Alex:** That's a lesson every platform team should internalize. As you add complexity, your operational maturity needs to scale with it. Otherwise, you're just adding more places where latent bugs can hide.

**Jordan:** Let's bring it back to that number. Three weeks between major outages. Twenty percent of the internet affected. Sixty-seven percent burnout rate in our industry. These aren't just statistics. They're the environment we're building in.

**Alex:** Your infrastructure strategy should assume your providers will fail. The question isn't if, it's when. And the real question is whether you've prepared your systems and your people for that reality.

**Jordan:** The infrastructure we depend on is only as reliable as its weakest deployment. Make sure your teams aren't paying the price for dependencies they can't control.

**Alex:** And maybe check that your status page doesn't run on Cloudflare.

**Jordan:** The fundamentals haven't changed. Redundancy matters. Monitoring matters. But increasingly, the human element matters too. Take care of your on-call teams. They're dealing with enough.
