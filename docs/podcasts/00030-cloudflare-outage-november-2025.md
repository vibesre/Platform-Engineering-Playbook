---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #030: Cloudflare Outage November 2025"
slug: 00030-cloudflare-outage-november-2025
---

# Cloudflare Outage November 2025: When a Rust Panic Took Down 20% of the Internet

## The Platform Engineering Playbook Podcast

<GitHubButtons />

<div style={{maxWidth: '640px', margin: '0 auto 1.5rem'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/Oz5XMA-mYT0"
      title="Cloudflare Outage November 2025: When a Rust Panic Took Down 20% of the Internet"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

**Duration**: 13 minutes
**Speakers**: Alex and Jordan
**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 🎙️ **Update**: Just three weeks later, Cloudflare had ANOTHER major outage. See [Episode #047: Cloudflare's Trust Crisis](/podcasts/00047-cloudflare-december-2025-outage-trust-crisis) for the December 5 incident and the pattern of repeated failures.

---

## Dialogue

**Jordan**: Today we're diving into Cloudflare's November eighteenth outage. ChatGPT went down. X went down. Shopify, Discord, Spotify—even Downdetector, the site that tracks outages, went down. All from a single configuration change.

**Alex**: And here's what makes this technically fascinating—it wasn't a cyberattack. It wasn't a DDoS. It was a database permissions change that caused a feature file to double in size and exceed a hardcoded memory limit in their Rust proxy. The whole thing cascaded from there.

**Jordan**: Twenty percent of the internet. That's Cloudflare's market share. And this was their worst outage since twenty nineteen. Let's break down exactly what happened, because the technical chain reaction here is something every platform engineer needs to understand.

**Alex**: So let's start with the timeline. November eighteenth, eleven oh five UTC—Cloudflare deploys a permissions change to their ClickHouse database cluster. This is routine stuff, improving how distributed queries handle access control.

**Jordan**: And nothing breaks immediately?

**Alex**: Right, that's part of why this was so hard to diagnose. The first errors don't show up until eleven twenty to eleven twenty-eight UTC. That's fifteen to twenty minutes later. And even then, it's intermittent.

**Jordan**: Which made them initially think it was a DDoS attack.

**Alex**: Exactly. They saw the traffic patterns, the error spikes, and their first instinct was "we're under attack." The status page went down around the same time for unrelated reasons, which made that suspicion even stronger.

**Jordan**: So when did they realize it was self-inflicted?

**Alex**: The automated tests caught something at eleven thirty-one, incident call at eleven thirty-five. But they didn't identify the actual root cause until thirteen thirty-seven UTC—over two hours after the first errors. And here's why: the failure was intermittent because the ClickHouse cluster was being gradually updated.

**Jordan**: Walk me through that. Why does a gradual update make this intermittent?

**Alex**: So the Bot Management feature file gets regenerated every five minutes by a query running against the ClickHouse cluster. If that query hit a node that had the new permissions, you'd get the bad file. If it hit a node with the old permissions, you'd get the normal file. The system would crash, recover, crash again. It looked like flapping, not a config issue.

**Jordan**: That's brutal from a debugging perspective. Okay, let's get into the actual technical failure. What went wrong with this permissions change?

**Alex**: Here's where it gets interesting. Cloudflare's ClickHouse setup has a "default" database and an underlying "r0" database. Historically, their internal processes assumed that metadata queries would only return results from the default database. The new permissions change allowed those queries to also surface metadata from r0.

**Jordan**: And the Bot Management query wasn't filtering by database name.

**Alex**: Exactly. It combined metadata from both locations, which meant every feature showed up twice. The feature file that normally contains around sixty machine learning features suddenly had over two hundred. Duplicate entries from both databases.

**Jordan**: And that's where the hardcoded limit comes in.

**Alex**: Right. Cloudflare's FL2 proxy—that's their new Rust-based proxy that replaced the old Nginx and LuaJIT stack—has a Bot Management module that preallocates memory based on a strict two hundred feature limit. They normally use around sixty features, so there's plenty of headroom. But when the file exceeded two hundred, the system hit that limit and panicked.

**Jordan**: A Rust panic. So it's not a graceful degradation, it's a hard crash.

**Alex**: The exact error was "thread FL2 worker thread panicked: called Result unwrap on an Err value." The code was calling unwrap on something that should never fail, and when it did fail, there was no error handling. Just panic.

**Jordan**: Wait—they used unwrap on something in the critical path of their proxy?

**Alex**: That's the thing. This code path assumed the feature file would always be well-formed because it's generated by their own systems. Internal data, so it must be trustworthy. That assumption broke catastrophically.

**Jordan**: This is the core lesson here, right? They treated internal configuration differently than they would treat user input.

**Alex**: That's exactly what their postmortem acknowledged. They committed to "hardening ingestion of Cloudflare-generated configuration files in the same way we would for user-generated input." Internal doesn't mean trustworthy.

**Jordan**: Let's talk about the blast radius. What actually broke when this panic happened?

**Alex**: So Cloudflare runs two proxy engines—FL2, the new Rust-based one, and FL, the legacy Nginx version. They've been migrating customers to FL2, so the impact split along those lines.

**Jordan**: How so?

**Alex**: FL2 customers got HTTP 5xx errors. Complete failures. The proxy crashed and couldn't serve traffic. FL customers—the ones still on the old engine—didn't get errors, but the bot scores came back as zero. Every single request got a bot score of zero.

**Jordan**: Which means any customer with rules to block bots based on score...

**Alex**: Massive false positives. Their legitimate traffic got blocked because everything looked like a bot with that zero score.

**Jordan**: And Turnstile?

**Alex**: Complete failure. Turnstile is their CAPTCHA alternative, and it depends on this same Bot Management infrastructure. If you weren't already logged into the Cloudflare dashboard, you couldn't log in. The dashboard uses Turnstile for auth.

**Jordan**: So Cloudflare couldn't even log into their own systems to fix the problem?

**Alex**: They had to implement bypasses for Workers KV and Cloudflare Access around thirteen oh five UTC just to get their own systems functioning. That's almost two hours into the incident.

**Jordan**: Let's zoom out for a second. This is the third major cloud infrastructure outage in thirty days. AWS on October twentieth with that DynamoDB DNS race condition. Azure on October twenty-ninth. Now Cloudflare.

**Alex**: And here's what should concern platform teams: the number of outages isn't necessarily increasing—Cisco logged twelve major outages in twenty twenty-five versus twenty-three in twenty twenty-four—but the blast radius keeps growing. More sites, more services depend on fewer providers.

**Jordan**: Cloudflare serves twenty percent of websites. Thirty-five percent of Fortune five hundred companies use them. That's concentration risk at an infrastructure level.

**Alex**: The internet was literally designed to route around damage. That was ARPANET's core principle—no single points of failure. And we've built ourselves right back into exactly that situation in the name of efficiency and cost optimization.

**Jordan**: So what did Cloudflare commit to fixing?

**Alex**: Four main things. First, hardening config file validation like we discussed—treat internal data like external input. Second, enabling global kill switches for features. They couldn't just turn off Bot Management at the edge; they had to stop the file propagation and manually deploy a known-good version.

**Jordan**: That's a big one. If you can't kill a feature instantly, you're at the mercy of your deployment pipeline during an incident.

**Alex**: Third, they're eliminating the ability for core dumps and error reports to overwhelm system resources. During debugging, the diagnostic systems themselves were consuming so much CPU that it made recovery harder. Fourth, reviewing failure modes across all proxy modules.

**Jordan**: Let me ask the practical question: what should platform teams be doing differently based on this?

**Alex**: Start with your CDN strategy. If you're one hundred percent on a single provider, what's your fallback? Multi-CDN isn't just about performance anymore—it's about blast radius containment.

**Jordan**: That's a big architectural change for most teams.

**Alex**: True, but there are intermediate steps. At minimum, understand your dependency tree. Which third-party services could take you down completely? When Cloudflare went down, Shopify went down. When Shopify went down, thousands of stores went down. That's three levels of dependency.

**Jordan**: What about on the code side? The hardcoded limits, the panic on error—how do you audit for that?

**Alex**: Look for anywhere you're using unwrap or expect in Rust, or similar patterns in other languages where you're asserting something can't fail. Then ask: what if it does? Do you have a fallback? Can you gracefully degrade? For config files specifically, validate size, validate schema, validate against expected ranges.

**Jordan**: The intermittent nature of this failure—that seems like a pattern we should watch for.

**Alex**: Absolutely. Gradual rollouts are great for catching errors before they hit everyone, but they can also create these intermittent failures that mask the root cause. If you're seeing flapping behavior, consider whether a partial deployment is involved.

**Jordan**: What about the observability angle? They initially thought this was a DDoS attack.

**Alex**: That's a great point. Your monitoring needs to distinguish between "traffic spike causing errors" and "errors causing traffic patterns that look like spikes." Correlation isn't causation, especially during incidents.

**Jordan**: Feature kill switches—how do you design those properly?

**Alex**: They need to be independent of your normal deployment path. If your deployment system is broken, or slow, or requires the thing you're trying to disable, you're stuck. Edge-level feature flags that can be flipped without a full deploy, that's the pattern.

**Jordan**: The "internal data is trustworthy" assumption—that seems like it's everywhere.

**Alex**: It is. We validate user input religiously, but we trust our own databases, our own config systems, our own internal APIs. This outage is a reminder that the most dangerous bugs often come from the code that handles your own data, because that's where your guard is down.

**Jordan**: Let's bring this back to the big picture. Three major outages in thirty days, all from different providers, all from different root causes. What's the takeaway?

**Alex**: The question isn't whether your infrastructure provider will have an outage. It's whether you've designed your systems to survive it. Every dependency—internal and external—needs to be treated as potentially hostile.

**Jordan**: That's a pretty adversarial mindset.

**Alex**: Defensive programming isn't about distrust. It's about acknowledging reality. This Cloudflare outage came from a routine permissions change to improve security. Good intentions, catastrophic outcome. Your systems need to handle that possibility.

**Jordan**: So the fundamentals: validate everything, degrade gracefully, have kill switches, understand your blast radius.

**Alex**: And audit your assumptions. Somewhere in your stack, there's code that assumes something can't fail. That's where the next outage lives.

**Jordan**: Sometimes the most dangerous code is the code that handles your own data.

**Alex**: Because that's where your guard is down.
