---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #007: AWS Outage Oct 2025"
slug: 00007-aws-outage-october-2025
---

# The $75 Million Per Hour Lesson: Inside the 2025 AWS US-EAST-1 Outage

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 15 minutes 44 seconds
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/aws-us-east-1-outage-october-2025-postmortem-analysis)**: Deep technical analysis with timeline, cost breakdown, and decision frameworks for platform teams.

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, margin: '1.5rem 0'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/5Xu8jjZ3qjk"
    title="The $75 Million Per Hour Lesson: Inside the 2025 AWS US-EAST-1 Outage"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>

---

**Jordan**: Today we're diving into the October twenty twenty-five AWS outage. October nineteenth, eleven forty-eight PM. Ring doorbells stop working. Robinhood freezes trading. Roblox goes offline for millions of players. Medicare enrollment goes dark. All at once. Six point five million outage reports flood in globally.

**Alex**: And here's what makes this different from every other cloud outage we've seen - it wasn't a hardware failure, it wasn't a configuration mistake, it wasn't even a cyber attack. It was a DNS race condition in DynamoDB that cascaded into what became a seventy-five million dollar per hour lesson in centralized cloud architecture.

**Jordan**: The thing that gets me is the scale. We're talking about one thousand plus companies affected. Seventy AWS services down. Everything from gaming platforms to stock trading to government services. How does a DNS issue in Virginia take down WhatsApp in London and trading platforms in New York?

**Alex**: That's exactly the question every platform engineer needs to answer Monday morning. Because this isn't just an AWS story. This is a wake-up call about how we've built the modern internet on a single region's control plane.

**Jordan**: Let's start with what actually happened. Give me the timeline.

**Alex**: Eleven forty-eight PM PDT on October nineteenth. Customers start seeing increased DynamoDB API error rates in US-EAST-1. At first, it looks like a normal spike. But within minutes, it's clear this is different. DynamoDB can't resolve its DNS endpoint. New connections are failing.

**Jordan**: And DynamoDB isn't just another service. It's foundational infrastructure that everything else depends on.

**Alex**: Exactly. By two twenty-five AM, five and a half hours later, AWS has manually restored DynamoDB's DNS records. But here's where it gets worse - recovery triggers a secondary failure. The DropletWorkflow Manager, which handles EC2 instance state, enters what AWS calls "congestive collapse."

**Jordan**: What does that mean in practice?

**Alex**: Billions of droplet leases trying to re-establish simultaneously. New EC2 instances launching but failing health checks because the network configuration is backlogged. Lambda functions that depend on EC2 can't execute. ECS and EKS clusters can't scale. Fargate tasks are stuck.

**Jordan**: So DynamoDB recovers but everything else stays broken.

**Alex**: For another twelve hours. Full resolution didn't come until two twenty PM on October twentieth. Fourteen hours total from start to finish.

**Jordan**: Okay, so we have the timeline. But what actually failed? Because AWS is supposed to be built for redundancy.

**Alex**: This is where it gets interesting. DynamoDB has an automated DNS management system with two components. There's a DNS Planner that monitors load balancer health and creates DNS plans. Then there's a DNS Enactor that applies those plans to Route 53.

**Jordan**: And the Enactor runs redundantly in three availability zones specifically to avoid single points of failure.

**Alex**: Right. The redundancy was supposed to PREVENT this. But instead, the redundancy created the failure. This is the paradox of distributed systems at scale.

**Jordan**: Walk me through what went wrong.

**Alex**: October nineteenth, eleven forty-eight PM. Enactor One starts applying what we'll call the Old Plan. But it's experiencing unusual delays - maybe network issues, maybe compute latency, we don't know. While Enactor One is stuck, Enactor Two sees a New Plan, applies it successfully, and everything's fine.

**Jordan**: So far so good.

**Alex**: Now Enactor Two does what it's supposed to do - triggers cleanup of stale plans. The Old Plan is marked for deletion. But here's the race condition - Enactor One finally finishes its delayed operation and OVERWRITES the New Plan with the Old Plan data.

**Jordan**: Wait, so the good plan gets replaced with stale data?

**Alex**: Exactly. And then the cleanup process runs and says "this Old Plan is stale, delete it." Except it's actually deleting the active plan. The result is an empty DNS record for dynamodb dot us-east-1 dot amazonaws dot com.

**Jordan**: And the system can't recover automatically because...

**Alex**: Because it's entered what AWS calls "an inconsistent state that prevented subsequent plan updates." The safety check that's supposed to prevent older plans from being applied was defeated by the timing. The delays were so unusual that the staleness detection didn't work.

**Jordan**: This is the kind of bug that only shows up in production at scale.

**Alex**: And here's what makes it worse - this latent race condition had been lurking in the system. It required very specific timing to trigger. Unusual delays in one Enactor while another Enactor completes normally and triggers cleanup at exactly the wrong moment.

**Jordan**: So what happens when DynamoDB's DNS goes dark?

**Alex**: Everything that depends on DynamoDB starts failing. And the cascading dominoes start falling. DropletWorkflow Manager relies on DynamoDB to track EC2 instance state. When DWFM can't connect to DynamoDB, it can't maintain leases for the physical servers hosting EC2 instances.

**Jordan**: And without those leases, EC2 instances can't launch or establish connectivity.

**Alex**: Right. Network Load Balancer depends on EC2 instances being healthy. When EC2 is broken, NLB health checks start failing. Lambda depends on these primitives to execute functions. ECS and EKS depend on them to launch containers. Fargate tasks can't start.

**Jordan**: It's like pulling a jenga block from the bottom.

**Alex**: That's exactly what it is. And by two twenty-five AM, when AWS manually restores the DNS records and DynamoDB comes back, you'd think the problem is solved. But instead, DWFM tries to re-establish billions of droplet leases all at once.

**Jordan**: And the system wasn't designed to handle that surge.

**Alex**: No system is designed for every lease to fail and recover simultaneously. New EC2 instances are launching but the network configuration is so backlogged that they're failing health checks. NLBs are removing capacity because they think instances are unhealthy when they're actually just not configured yet.

**Jordan**: This is the cascading failure nightmare scenario.

**Alex**: And here's the kicker - AWS had no established operational recovery procedure for this. The postmortem explicitly says engineers "attempted multiple mitigation steps" without a playbook. They were improvising in real-time.

**Jordan**: What did they end up doing?

**Alex**: Four fourteen AM, they started throttling incoming work and selectively restarting DWFM hosts. Nine thirty-six AM, they disabled automatic NLB health check failovers to stop the capacity removal. Eleven twenty-three AM, they began relaxing the request throttles. One fifty PM, they finally achieved full API normalization.

**Jordan**: And globally, they disabled the DynamoDB DNS automation entirely.

**Alex**: Worldwide. Pending implementation of safeguards. That tells you how severe the trust breakdown was. The automation designed for reliability became too dangerous to trust.

**Jordan**: Let's talk about the real cost of this. Because seventy-five million dollars per hour gets thrown around, but what does that actually mean?

**Alex**: Gartner benchmarks downtime at five thousand six hundred dollars per minute per application. So let's do the math. One hundred thirty minutes - that's just the DynamoDB outage, not the full fourteen hours - times five thousand six hundred equals seven hundred twenty-eight thousand dollars for ONE application at ONE company.

**Jordan**: And we're talking about a thousand plus companies affected.

**Alex**: Multiply that across fourteen hours and the scale becomes clear. Trading platforms lost transactions. Medicare enrollment was offline during open enrollment. Supply chain systems couldn't process orders. ParcelHero estimated billions in lost revenue and service disruption.

**Jordan**: But here's the number that actually matters for platform engineers.

**Alex**: Seventy-five million per hour makes multi-region architecture look like cheap insurance.

**Jordan**: That's the reframing. We've been thinking about multi-region as expensive. But this outage flips the cost equation.

**Alex**: Completely. Option A - spend four hundred dollars a month for a managed multi-region platform. Option B - accept seventy-five million per hour risk exposure. Option C - spend fifteen thousand a month in engineering time building your own. The math suddenly looks very different.

**Jordan**: And here's what makes this worse - US-EAST-1 isn't just another AWS region.

**Alex**: This is the part that surprised a lot of companies. US-EAST-1 is the control plane for the world. It's AWS's oldest region, launched in two thousand six. It's the most mature, most interconnected, most deeply integrated.

**Jordan**: Even if your services are running in EU or Asia, they depend on US-EAST-1 for control plane operations.

**Alex**: Right. Companies thought they were multi-region. They had workloads in multiple regions. But they discovered dependencies they didn't know existed. Your compute might be in EU-WEST-1, but the control plane that manages it? That's in US-EAST-1.

**Jordan**: Why is it architected this way?

**Alex**: Backwards compatibility and operational complexity. US-EAST-1 handles thirty-five to forty percent of global AWS traffic. It's where all the original services were built. Moving the control plane would be a massive undertaking with enormous risk.

**Jordan**: So it's an architectural constant we have to live with.

**Alex**: Unless you're using GovCloud or EU Sovereign Cloud, which have separate control planes. But for the vast majority of AWS customers, US-EAST-1 is your control plane whether you know it or not.

**Jordan**: What is AWS actually changing in response to this?

**Alex**: Immediate actions - they're adding safeguards to prevent the DNS race condition from happening again. They're implementing rate limiting on NLB health check failovers to prevent cascading capacity removal. They're building additional test suites for DWFM to prevent regressions.

**Jordan**: But they're not changing the fundamental architecture.

**Alex**: No. US-EAST-1 remains the global control plane. The centralized model that created the vulnerability is staying. They're just adding better guardrails.

**Jordan**: Which means the systemic risk remains.

**Alex**: Just with better defenses. And that's the lesson for platform engineers. You can't rely on AWS to architect away this risk. You have to own your resilience strategy.

**Jordan**: So let's make this practical. It's Monday morning. What three questions should every platform engineer be asking?

**Alex**: Question one - what's our single-region exposure? And I don't just mean where your workloads run. I mean what fails if US-EAST-1 goes dark? Map the critical paths. Document the dependencies you didn't know existed.

**Jordan**: Because a lot of teams are about to discover they're not as multi-region as they thought.

**Alex**: Exactly. Question two - what's our seventy-five million per hour calculation? Take your downtime cost, multiply by probability, multiply by expected duration. That's your risk exposure. Now compare that to the cost of resilience investment.

**Jordan**: And suddenly that four hundred dollar per month platform doesn't look expensive.

**Alex**: Question three - do we have playbooks for cascading failures? AWS didn't. That's why manual intervention took so long. Can your team recover when the automation fails? Have you tested this in game days?

**Jordan**: What can engineers actually do this week?

**Alex**: If you're an individual engineer, study the AWS postmortem like a textbook. This is how race conditions work in distributed systems. This is how cascading failures propagate. This is how DNS caching delays recovery. Add resilience engineering to your skill development roadmap because this is becoming a specialization.

**Jordan**: For platform teams?

**Alex**: Schedule a DR drill this week. Pretend AWS US-EAST-1 is down. What breaks? Can you failover? How long does it take? Map all your single-region dependencies - you'll be surprised what you find. Price out multi-region options because the business case just got a lot clearer.

**Jordan**: And for leadership?

**Alex**: Use this incident to unblock resilience budget. The argument is simple - seventy-five million per hour happened to companies just like us. Investment in resilience is insurance with clear ROI. This is the wake-up call to prioritize what you've been postponing.

**Jordan**: Here's my take. October twentieth, twenty twenty-five will be remembered as the day the cloud showed its Achilles heel.

**Alex**: Not that AWS failed - all systems fail eventually. But that we've built a centralized internet on a single region's control plane. The lesson isn't avoid AWS. It's own your resilience strategy.

**Jordan**: Because the next outage isn't a question of if. It's when, and will you be ready. The fundamentals of good engineering remain constant - understand your dependencies, plan for failure, and don't let convenience override resilience. The seventy-five million per hour lesson makes the business case obvious.
