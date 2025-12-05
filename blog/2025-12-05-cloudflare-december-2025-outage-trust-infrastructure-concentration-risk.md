---
title: "Cloudflare's December 2025 Outage: When Trust Becomes the Real Casualty"
description: "Analysis of Cloudflare's December 5, 2025 outage - the sixth major incident in 2025. Beyond the technical postmortem: examining the pattern of repeated failures, reputation damage, and the human cost to on-call engineers."
slug: cloudflare-december-2025-outage-trust-infrastructure-concentration-risk
keywords:
  - cloudflare outage december 2025
  - cloudflare reliability
  - infrastructure concentration risk
  - on-call engineer burnout
  - CDN outage
  - platform engineering reliability
  - multi-CDN strategy
  - incident response
  - SRE burnout
  - infrastructure single point of failure
date: 2025-12-05
authors:
  - name: Platform Engineering Playbook
    url: https://platformengineeringplaybook.com
---

# Cloudflare's December 2025 Outage: When Trust Becomes the Real Casualty

> 🎙️ **Listen to the podcast episode**: [Episode #047: Cloudflare's Trust Crisis](/podcasts/00047-cloudflare-december-2025-outage-trust-crisis) - Deep dive into the pattern of outages and the human cost to platform teams.

## TL;DR

Three weeks after their worst outage since 2019, Cloudflare went down again. On December 5, 2025, a Lua code bug that existed "undetected for many years" took down 28% of HTTP traffic for 25 minutes. This marks the **sixth major outage of 2025** for a company handling 20% of all internet traffic. Beyond the technical postmortem, this article examines the pattern of repeated failures, the reputation damage, and the often-overlooked human cost to on-call engineers who bear the burden of infrastructure dependencies they can't control.

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| HTTP Traffic Impacted | 28% | [Cloudflare Blog](https://blog.cloudflare.com/5-december-2025-outage/) |
| Outage Duration | 25 minutes | Cloudflare Blog |
| Cloudflare's Internet Share | 20% | Industry reports |
| Major Outages in 2025 | 6 | Cloudflare Status History |
| Days Since Last Major Outage | 17 | November 18 → December 5 |
| IT Professional Burnout Rate | 67% | 2024 State of DevOps |
| Estimated November Loss | $180-360M | Industry analysis |

---

## Quick Answer: What Happened on December 5, 2025?

At 08:47 UTC on December 5, 2025, Cloudflare deployed a configuration change to mitigate a React Server Components CVE. This triggered a Lua code bug in their FL1 proxy that had existed undetected for years. The error—`attempt to index field 'execute' (a nil value)`—caused 28% of HTTP traffic to fail for 25 minutes. Sites including LinkedIn, Zoom, Fortnite, ChatGPT, and Shopify were affected. This was Cloudflare's sixth major outage of 2025, coming just 17 days after their November 18 incident that lasted over four hours.

---

## The December 5 Incident: Technical Breakdown

### The Root Cause

Cloudflare was deploying a "killswitch" to disable a Web Application Firewall rule as part of mitigating an industry-wide React Server Components vulnerability. When this killswitch disabled a rule with an "execute" action type, the Lua code attempted to access an object that didn't exist in this scenario:

```lua
if rule_result.action == "execute" then
  rule_result.execute.results = ruleset_results[tonumber(rule_result.execute.results_index)]
end
```

The error was straightforward: `init.lua:314: attempt to index field 'execute' (a nil value)`. The code expected a `rule_result.execute` object that wasn't present when a killswitch was applied.

### Why It Wasn't Caught

This bug existed "undetected for many years" according to Cloudflare's postmortem. The reason? **This code path had never been exercised.** They had never previously applied a killswitch to a rule with an "execute" action type. Lua lacks strong type checking, so the bug sat dormant, waiting for the exact conditions to trigger it.

> 💡 **Key Takeaway**: Even mature codebases harbor latent bugs in untested code paths. The irony here is that a security mitigation—intended to protect customers—became the trigger that brought down 28% of traffic.

### The Timeline

| Time (UTC) | Event |
|------------|-------|
| 08:47 | Bad configuration deployed |
| 08:48 | Full propagation across network |
| 08:50 | Automated alerts fire |
| 09:11 | Rollback initiated |
| 09:12 | Full restoration |

**Notable**: The configuration propagated globally in **one minute** with no gradual rollout. Automated alerts took **two minutes** to fire after the incident began—an eternity when millions of requests are failing per second.

---

## The Pattern: Six Major Outages in 2025

This wasn't an isolated incident. Here's Cloudflare's 2025 track record:

| Date | Duration | Root Cause | Impact |
|------|----------|------------|--------|
| March 21 | 1hr 7min | R2 credential rotation error | Write/read failures |
| June 12 | 2hr 28min | Service degradation | Workers KV, Access, WARP |
| July 14 | 62 min | Topology change | 1.1.1.1 DNS resolver |
| September 12 | Hours | Dashboard/API issues | Control plane |
| November 18 | 4+ hours | Rust panic in Bot Management | 20% of internet |
| December 5 | 25 min | Lua killswitch bug | 28% of HTTP traffic |

### The Troubling Trend

Analysis of these outages reveals a pattern:

- **2019-2020**: External infrastructure failures (BGP misconfigurations, upstream provider issues)
- **2023-2025**: Internal engineering mistakes (credential rotation, code bugs, configuration errors)

This shift suggests that **Cloudflare's growing complexity is outpacing their operational safeguards**. The company's infrastructure has become incredibly sophisticated, but sophistication creates more failure modes.

> 💡 **Key Takeaway**: As systems grow more complex, operational maturity must scale proportionally. Otherwise, you're just adding more places where latent bugs can hide.

---

## Reputation at Stake: Community Reactions

The community response has been pointed. Here's what developers are saying:

### Hacker News

> "This shouldn't happen twice in a month."

> "Cloudflare is now below 99.9% uptime for the year."

> "Two minutes for automated alerts to fire is terrible."

### X/Twitter

The Downdetector irony wasn't lost on anyone:

> "Wanted to check if Cloudflare is down → went to Downdetector.com... Downdetector runs on Cloudflare too 😅"

### The Trust Equation

When a company positions itself as the protector of 20% of the internet, repeated failures hit differently. Each outage erodes the core value proposition: "We'll keep your sites online."

The November 18 outage generated an estimated **$180-360 million in business losses** across affected companies. That's not counting:
- Cloudflare's SLA credit obligations
- Long-term customer churn risk
- Enterprise evaluation of multi-CDN strategies

---

## The Human Cost: On-Call Engineers in the Crossfire

This is the part that doesn't make it into postmortems.

### The Burnout Statistics

The numbers paint a concerning picture:

- **67%** of IT professionals experience burnout ([2024 State of DevOps Report](https://cloud.google.com/devops))
- **1 in 4** employees globally experience burnout symptoms ([McKinsey](https://www.mckinsey.com))
- On-call engineers allocate **30-40%** of work bandwidth during rotations ([DrDroid](https://drdroid.io))
- Employees experiencing burnout are **3x more likely** to be job searching ([SHRM](https://www.shrm.org))

### The Downstream Nightmare

Picture this: It's 3 AM. PagerDuty goes off. Your app is down.

You jump online, start investigating:
- Check recent deploys: Nothing changed
- Check the database: Healthy
- Check external dependencies: ...oh, Cloudflare is down

Now you're in communications mode:
1. Update your status page
2. Notify leadership
3. Respond to angry Slack messages
4. Explain to customers that it's not your fault

"Working on it" means "watching someone else's status page and hoping."

### The Responsibility-Control Mismatch

Here's the core problem: **You're responsible for reliability, but you can't control the infrastructure you depend on.**

This mismatch between responsibility and control is a recipe for burnout. You're held accountable for SLAs that can be busted by someone else's configuration change.

> 💡 **Key Takeaway**: The infrastructure we depend on transfers its reliability problems to our teams. When Cloudflare has six outages in nine months, thousands of on-call engineers pay the price.

### The Aftermath

When service restores, the work isn't over:
- Recovery traffic spike handling
- Cache invalidation
- Stuck request cleanup
- Post-incident reports
- Explaining to leadership why SLAs are busted this month

And then doing it again three weeks later.

---

## Infrastructure Concentration: When Security Becomes Risk

The Cloud Security Alliance published an article titled ["The Internet is a Single Point of Failure"](https://cloudsecurityalliance.org/blog/2025/11/21/the-internet-is-a-single-point-of-failure) after the November outage. The December incident reinforces their thesis.

### The Concentration Problem

- Cloudflare handles **20% of all internet traffic**
- The three major hyperscalers provide **two-thirds** of cloud infrastructure
- Market concentration among CDNs has **steadily increased since 2020**

Ryan Polk, policy director at the Internet Society, warned that "when too much internet traffic is concentrated within a few providers, these networks can become single points of failure that disrupt access to large parts of the internet."

### The Irony

The December 5 outage was caused by a security mitigation. Cloudflare was trying to protect customers from a React CVE. As one analyst put it:

> "The risk mitigation system became the systemic risk itself."

We've created a paradox: centralizing security infrastructure makes the internet safer from external threats but more vulnerable to internal failures.

---

## What This Means for Platform Teams

### Immediate Actions

**1. Evaluate Multi-CDN Strategies**

Organizations with multi-CDN setups "sailed through" both the November and December outages with zero perceptible downtime. Options include:
- Active-active with traffic splitting
- Active-passive with automatic failover
- Critical paths with CDN-independent fallbacks

**2. External Synthetic Monitoring**

If your monitoring runs through Cloudflare and Cloudflare goes down, your monitoring is blind. Set up synthetic checks from outside your CDN provider.

**3. "Major Provider Down" Runbooks**

Do you have a runbook for when your CDN fails? Key elements:
- Communication plan (internal and external)
- What you can actually do vs. what you wait out
- Customer-facing messaging templates
- Escalation criteria

**4. On-Call Wellness Programs**

Your on-call wellness is a legitimate engineering concern. If teams are getting paged for things they can't control:
- Review alert routing for external dependency failures
- Consider "watching" vs. "responding" protocols for provider outages
- Build blameless culture for incidents outside your control

### Strategic Considerations

**Vendor Diversification**

The days of single-vendor dependency should be ending. Questions to ask:
- What's our blast radius if [primary provider] goes down?
- Do we have tested failover procedures?
- What's the cost-benefit of redundancy vs. the risk of concentration?

**Complexity Management**

As Cloudflare's experience shows, complexity growth must be matched by operational maturity growth. For your own systems:
- Are you adding features faster than you're adding safeguards?
- Do untested code paths exist in your critical systems?
- Is your deployment process appropriate for your blast radius?

---

## FAQ

### How long was the December 5, 2025 Cloudflare outage?

The outage lasted approximately 25 minutes, from 08:47 UTC to 09:12 UTC. During this time, 28% of HTTP traffic through Cloudflare's network was affected.

### What caused the Cloudflare outage on December 5, 2025?

A Lua code bug in Cloudflare's FL1 proxy that had existed "undetected for many years." When they deployed a killswitch to disable a WAF rule (part of mitigating a React CVE), the code attempted to access a nil value, crashing the proxy.

### How many major outages has Cloudflare had in 2025?

Six major outages: March 21 (R2), June 12 (Workers KV/Access), July 14 (1.1.1.1 DNS), September 12 (Dashboard/API), November 18 (Bot Management), and December 5 (Lua bug).

### What sites were affected by the Cloudflare December 2025 outage?

Major sites included LinkedIn, Zoom, Fortnite, ChatGPT, Shopify, Coinbase, GitLab, and Deliveroo. Notably, Downdetector (used to track outages) was also affected since it runs on Cloudflare.

### Should companies use multiple CDN providers?

Given the pattern of CDN outages in 2025, multi-CDN strategies are increasingly recommended for mission-critical applications. Organizations with multi-CDN setups reported minimal impact from both November and December Cloudflare outages.

### What is Cloudflare doing to prevent future outages?

Cloudflare has promised enhanced gradual rollouts with health validation, "fail-open" error handling instead of hard crashes, and detailed resiliency projects to be published "before the end of next week."

---

## Conclusion

Three weeks between major outages. Six incidents in 2025. 67% burnout rate among IT professionals.

These aren't just statistics—they're the environment platform teams operate in daily. When 20% of the internet depends on one company, that company's reliability becomes everyone's problem.

The December 5 outage was technically straightforward: a nil value access in a code path that had never been tested. But the pattern it represents is more concerning: growing complexity outpacing operational safeguards, repeated promises of improvement followed by new failures, and an industry increasingly concentrated in providers that have become single points of failure.

Your infrastructure strategy should assume your providers will fail. The question isn't if, it's when—and whether you've prepared your systems **and your people** for that reality.

Take care of your on-call teams. They're dealing with enough.

---

## Sources

- [Cloudflare Blog: December 5, 2025 Outage](https://blog.cloudflare.com/5-december-2025-outage/)
- [Cloudflare Blog: November 18, 2025 Outage](https://blog.cloudflare.com/18-november-2025-outage/)
- [Cloudflare Status History](https://www.cloudflarestatus.com/history)
- [Cloudflare Outage History Analysis](https://controld.com/blog/biggest-cloudflare-outages/)
- [CSA: Internet as Single Point of Failure](https://cloudsecurityalliance.org/blog/2025/11/21/the-internet-is-a-single-point-of-failure)
- [LeadDev: On-call Stress](https://leaddev.com/technical-direction/how-reduce-stress-call-engineering-teams)
- [Tom's Guide: Cloudflare Down December 2025](https://www.tomsguide.com/news/live/cloudflare-down-december-2025)
- [2024 State of DevOps Report](https://cloud.google.com/devops)
