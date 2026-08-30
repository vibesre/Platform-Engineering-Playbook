---
title: "Building CruiseCaptain: Where the Work Went in a One-Engineer, AI-Agent Platform"
description: "A builder's review of cruisecaptain.ai: Go, PostgreSQL and TimescaleDB, k3s and Argo, an AI assistant and an MCP server. Why the delivery pipeline and data semantics were the real work once agents wrote most of the code."
slug: cruisecaptain-platform-review-go-timescaledb-k3s
keywords:
  - CruiseCaptain
  - platform engineering case study
  - AI coding agents
  - Go monolith
  - TimescaleDB
  - k3s production
  - Argo Rollouts
  - progressive delivery
  - MCP server
  - price tracking architecture
  - solo founder infrastructure
  - GitHub Actions Ubicloud
date: 2026-08-29
datePublished: 2026-08-29
dateModified: 2026-08-29
authors:
  - name: Platform Engineering Playbook
    url: https://platformengineeringplaybook.com
---

import Head from '@docusaurus/Head';

<Head>
  <script type="application/ld+json">{JSON.stringify({
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "Building CruiseCaptain: Where the Work Went in a One-Engineer, AI-Agent Platform",
    "datePublished": "2026-08-29",
    "dateModified": "2026-08-29",
    "author": {"@type": "Organization", "name": "Platform Engineering Playbook", "url": "https://platformengineeringplaybook.com", "sameAs": ["https://github.com/vibesre/Platform-Engineering-Playbook"]},
    "publisher": {"@type": "Organization", "name": "Platform Engineering Playbook", "url": "https://platformengineeringplaybook.com"},
    "about": {"@type": "SoftwareApplication", "name": "CruiseCaptain", "url": "https://cruisecaptain.ai", "applicationCategory": "TravelApplication", "sameAs": ["https://cruisecaptain.ai/about", "https://cruisecaptain.ai/mcp"]},
    "mentions": [
      {"@type": "SoftwareApplication", "name": "Go", "url": "https://go.dev"},
      {"@type": "SoftwareApplication", "name": "TimescaleDB", "url": "https://www.timescale.com"},
      {"@type": "SoftwareApplication", "name": "k3s", "url": "https://k3s.io"},
      {"@type": "SoftwareApplication", "name": "Argo Rollouts", "url": "https://argoproj.github.io/rollouts/"}
    ]
  })}</script>
</Head>

# Building CruiseCaptain: Where the Work Went in a One-Engineer, AI-Agent Platform

Disclosure first: I built <a href="https://cruisecaptain.ai" rel="noopener">CruiseCaptain, a cruise price history tracker</a>, and I run it. This is a review of my own platform, written for the people this site is for, and I'm going to spend most of it on the parts that were hard rather than the parts that look good in a diagram.

CruiseCaptain is an independent cruise discovery and price-history service for travelers who want to know whether today's fare is actually good before they book. It tracks more than 40 cruise lines, more than 500 ships and roughly 100,000 active sailings across the forward schedule. One engineer builds and operates it, with AI coding agents producing a large share of the code.

That last fact is the reason I think this build is a useful case study. I went in assuming agents would make writing code the fast part. They did. What I didn't expect was where the effort would move next.

<!-- truncate -->

## TL;DR

- Cruise shopping has a transparency problem: almost nobody shows you what a sailing cost last week. CruiseCaptain records every observed fare and shows the history, with the observation time, and says so when the evidence is thin.
- The stack is Go with [Chi](https://github.com/go-chi/chi), server-rendered HTML, [PostgreSQL](/technical/postgresql) with [TimescaleDB](https://www.timescale.com/) for the observation tables, running on [k3s](/technical/k3s) with [Argo](/technical/argocd) for progressive delivery.
- The hardest bug wasn't infrastructure. It was a chart that looked like wild price volatility and was actually the code silently switching between two kinds of price evidence.
- The AI assistant and the MCP server are built so the model can't reach anything it shouldn't; the boundary is enforced by tests, not by prompt wording.
- With agents writing most of the code, the bottleneck moved downstream to verification and deployment. The delivery platform was the biggest productivity investment I made, and I'd make it again earlier.

## The problem I was trying to solve

Most cruise sites show today's price, but almost none tell you what that same sailing cost last week or last month. Every sale banner feels urgent, while the traveler has very little evidence.

I wanted to build the cruise equivalent of a price tracker: show what we observed, when we observed it, and be honest when the evidence is incomplete.

The data comes from a licensed cruise-industry inventory feed that aggregates pricing and availability from participating cruise lines, obtained through a commercial agreement. Nothing is scraped from cruise-line websites. The public <a href="https://cruisecaptain.ai/about" rel="noopener">CruiseCaptain about page</a> covers what a displayed price means and where it comes from.

## The shape of the system

Here is the full chain between a cruise line changing a price and a traveler seeing it.

A cruise line changes its inventory, that update reaches the industry data feed, and CruiseCaptain receives an updated record for the sailing. The record is validated and fingerprinted so we can detect duplicates or malformed data. It's parsed into fares, cabin categories, availability and itinerary information, then compared with the previous state. We store the new observation, update the current-price view and refresh the affected caches.

When a traveler opens the page, it may be served directly from the edge. Otherwise the application reads from a precomputed view of the latest data and renders the page.

The whole chain is asynchronous, so a displayed fare is the most recent price we observed, not a guaranteed live checkout quote. That's why every sailing page carries the observation time.

### Go, Chi, and server-rendered HTML

Almost all of it is written in [Go](/technical/go). The HTTP layer uses Chi, and the customer-facing site is primarily server-rendered HTML with a modest amount of JavaScript.

Go fit the problem well. Ingestion is concurrent and I/O-heavy, the binaries are easy to deploy, memory use is predictable, and the type system catches a useful class of data-contract mistakes. It also lets me use one language for the site, the API, the data worker and the operational tools, which matters more than usual when one person is context-switching between all of them.

### PostgreSQL with TimescaleDB

Cruise data is naturally relational: ships, ports, itineraries, sailings, cabin categories. Prices are time series. PostgreSQL with TimescaleDB on the observation-heavy tables gives me normal SQL, transactions and constraints while handling compression and historical price queries efficiently.

The trade-off is operational. Large historical tables make migrations, indexes, retention and performance tuning more consequential. PostgreSQL is wonderfully boring until you ask it to retain and repeatedly reshape tens of millions of observations.

### Three roles, not a fleet

The core product is a modular application rather than a fleet of microservices. There are three main long-running roles: the website, the internal API and the data-processing worker. A few smaller programs handle administrative and maintenance jobs.

The agent-facing integration is separately isolated because it has different security requirements, and I'll come back to that. In general I split components only when they have different scaling, failure or security characteristics. Nothing else earns a separate process.

### Caching

For a cacheable public page, the hottest path is the edge, so the request may never reach the application at all.

On an origin request, frequently used data comes from bounded in-memory caches and precomputed database views. Below those are indexed historical tables. A normal page request does not need to reconstruct a sailing's entire price history from raw observations.

Successful data updates invalidate the relevant cached content. Cache invalidation is also part of deployment and rollback, which sounds obvious and took a while to get right.

> 💡 **Takeaway:** For a read-heavy data product run by a small team, the boring stack wins: one language, one relational database with a time-series extension, three processes, and caching layered from the edge inward. Every split beyond that needs a scaling, failure or security reason.

## The hardest bug looked like volatility

The most deceptive bug I hit looked like extraordinary price volatility. A chart would show a fare dropping, rebounding, and sometimes repeating the pattern several times.

My first assumption was that I was seeing aggressive promotions, or stale upstream data. Neither was right.

When I replayed the original records, it turned out the feed contained two kinds of price evidence with different meanings and different lifetimes. The naive code was selecting whichever number was lower at each observation. When one source appeared or expired, the chart silently switched basis while presenting it as one continuous price series. Nothing was wrong with the feed. The chart was answering a question I hadn't meant to ask.

The fix was to stop taking a minimum across incompatible sources. A price series now stays on a consistent basis, with other sources used only as constrained fallbacks. A basis change is annotated or suppressed rather than presented as a price movement.

That rule now lives in shared code and regression tests, so the chart, the headline price, the deals page and the assistant all use the same interpretation. Before that, four surfaces could each have their own opinion about what the price was.

### The raw archive is what made this diagnosable

I retain a protected, versioned archive that lets me reproduce how a sailing was interpreted at a particular time. Identical records are deduplicated, and historical versions can be replayed through newer parsing code.

That archive is how I reconstructed the basis bug. It's also how I test parser changes against real historical data, rebuild derived information, and work out whether a strange value came from the source or from my interpretation of it. It has found more bugs than most of the infrastructure has.

> 💡 **Takeaway:** Keep the raw input and make replay a supported, routine tool. The question "did the source say this, or did I?" comes up constantly with third-party data, and without the archive you're guessing.

## What "price drop" means

This turned out to be the actual product-design problem, and I wish I'd settled it earlier.

A real drop has to be comparable with itself: the same sailing, the same cabin category, a compatible fare basis. The current fare must be recent, currently available, materially below its normal range, and observed more than once.

The naive version compared "cheapest now" with "cheapest before." That confuses a new fare becoming available, a restricted promotion, a cabin selling out, or a temporary feed value with an actual reduction.

CruiseCaptain separates "the same fare got cheaper" from "a different lower fare became available." Both can be useful to a traveler. They are not the same claim, and the site labels them differently. The rules a user sees on the <a href="https://cruisecaptain.ai/deals/methodology" rel="noopener">methodology page for how CruiseCaptain confirms a cruise price drop</a> are the public version of this logic: what threshold counts, what evidence is required, and what gets suppressed. The <a href="https://cruisecaptain.ai/deals" rel="noopener">cruise deals page</a> only lists drops that pass all of it.

If I did it again, I'd establish the data semantics first. The difficult part was not building pages or APIs. It was defining exactly what a price, a price drop, a sold-out state and a missing observation meant across every surface, and then making sure every surface agreed.

## The Captain, and the MCP server

The assistant is called the Captain. It translates a traveler's natural-language request into structured searches of the catalog, retrieves matching sailings and price evidence, and explains the result in plain language.

It runs on a commercial language model through a provider-independent interface, so the underlying model can change without rewriting the product around it.

What it cannot do matters more than what it can. It cannot book or purchase a cruise, predict future prices, alter an account, or silently create an alert. User actions stay in the normal application flow, where they can be reviewed and confirmed.

### Where its knowledge comes from

Current prices, availability and sailing facts come from structured CruiseCaptain results, not the model's memory. Destination and ship context comes from a separately curated knowledge store with source and freshness information attached.

The controls are mostly structural: constrained tools, validated inputs, bounded results, trusted links only, timestamps on every price claim, and typed result cards that are rendered independently of the model's prose. The assistant is also instructed to say when the available evidence is insufficient, and that abstention is treated as a correct answer in evaluation, not a failure.

### Knowing when it regresses

Two layers. Deterministic tests verify that common requests produce the correct searches, filters and links. Separate evaluations exercise representative questions against the deployed assistant and check the machine-verifiable parts of the response: did it use the right data, did it preserve an important limitation, did it produce a valid result link.

I monitor answer quality and grounding, not just whether the model returned a response. A fast wrong answer is the failure mode I care about.

### The MCP server

CruiseCaptain exposes a [Model Context Protocol](https://modelcontextprotocol.io/) server so an AI assistant like ChatGPT or Claude can search and compare sailings directly. The <a href="https://cruisecaptain.ai/mcp" rel="noopener">CruiseCaptain MCP connector for ChatGPT and Claude</a> page describes it from the user's side.

From the engineering side, it exposes a small, read-only set of discovery and comparison tools over a separately prepared public catalog. It does not expose the internal application API and it does not provide general database access. Authentication, quotas, bounded responses and strict data allowlists are enforced outside the model. Account changes, booking, bulk export and arbitrary queries are simply not part of the interface.

The public agent process is isolated from private customer data and from the broader production system, and automated dependency and deployment tests enforce that boundary. If a future change tried to link account or payment code into the agent-facing binary, the build fails.

> 💡 **Takeaway:** Put the AI boundary in the dependency graph and test it there. A build that fails when the wrong package gets imported is a stronger guarantee than any system prompt.

## Agents moved the bottleneck

This is the part I'd want another engineer to take away.

If "typing" means literal keystrokes, agents have produced a large share of CruiseCaptain's code. I don't track a percentage, because keystroke ownership isn't the useful measure. I choose the product behavior and the architecture, define the acceptance criteria, review the work, and remain responsible for what reaches production.

The biggest unlock was realizing that faster code generation requires a much stronger verification and delivery system. Before that investment, testing and deployment were slow and unreliable. Agents could produce changes faster than I could safely validate and release them, so the bottleneck simply moved downstream.

I started with a much simpler setup. Testing and deployment became the constraint the moment I began working heavily with agents. Agents let you create and review changes much faster, but that advantage disappears if releases are slow, fragile or difficult to reverse.

### What the delivery platform looks like

Day to day, I turn a problem into a contract or a failing test, let an agent implement a bounded change, review the assumptions, and send it through a repeatable CI and rollout process.

A change starts as a pull request. [GitHub Actions](/technical/github-actions) runs the test, lint, migration, security and deployment-validation suites on [Ubicloud](https://www.ubicloud.com/) runners. Once the application change is merged, it produces a versioned image. Production promotion is a separate change. [Argo Rollouts](https://argoproj.github.io/rollouts/) takes the new version out gradually, and health and analysis checks decide whether the rollout continues or automatically rolls back. Browser-level smoke tests exercise the critical public paths after deploy.

| Gate | What it proves | What happens on failure |
|---|---|---|
| Pull request CI | Tests, lint, migrations, security scans, deployment manifests all pass | Merge is blocked |
| Merge | A versioned image exists for exactly this change | Nothing ships yet |
| Promotion | An explicit, reviewable decision to send that version to production | Nothing ships yet |
| Progressive rollout | Health and analysis signals hold as traffic shifts | Automatic rollback |
| Post-deploy smoke tests | Critical public paths, structured data and cache behavior work in production | Rollback and alert |

An agent can generate a lot of code quickly, but it cannot bypass the evidence required to ship it. The platform makes large changes routine without making production casual.

Moving to [Kubernetes](/technical/kubernetes) via k3s and Argo gave me a consistent place where changes roll out gradually, get evaluated against real health signals, and reverse themselves when something fails. It was a major productivity win, not just a reliability exercise.

### Was it over-built?

I thought about this honestly, because a k3s cluster with progressive delivery is a lot of machinery for a site this size.

The delivery platform looked large when measured against traffic. But traffic was the wrong denominator. Engineering throughput was the better measure. Once agents increased the rate at which I could make changes, dependable testing and deployment stopped being optional. GitHub Actions and Ubicloud made large test runs routine; k3s and Argo gave me progressive delivery and automatic rollback. That combination let me ship much faster without lowering the standard for production.

What I did over-build was product, not platform. A few abstractions arrived before I had enough evidence about how travelers would actually use them. I'd now be more skeptical of speculative product complexity and less skeptical of delivery investment.

> 💡 **Takeaway:** With agents in the loop, the limiting factor is no longer how quickly you can produce a patch. It's how quickly you can establish that the patch is correct and deploy it safely. Size the delivery platform to engineering throughput, not to traffic.

## Guardrails that became tests

Every rule below started as a sentence in a doc. Each one is now a test that fails the build or the deploy.

- A sold-out or missing fare must never render as zero dollars.
- Incompatible price sources cannot be silently combined.
- An older ingestion event cannot overwrite a newer observation.
- Every website, API and assistant filter must have an explicit mapping, or an explicit reason it's unsupported.
- The public web process cannot accidentally acquire database or model credentials.
- The agent-facing catalog cannot import private account or payment functionality.
- Important pages, structured data and cache behavior are exercised after every deployment.

The filter-contract test paid for itself first. Search capabilities had grown in several places, and the assistant could advertise a filter that a later layer silently discarded. Turning that mapping into one executable contract made an entire class of "plausible answer, wrong query" failures much harder to reintroduce. That class is especially nasty with an AI assistant, because the answer reads fine.

## Operations, and two incidents

Secrets are encrypted at rest, access is tightly limited, and production delivery of a secret is separate from ordinary application deployment. Plaintext credentials never touch source control, and rotation goes through a restricted operator process. It's the least automated part of the system, on purpose.

For monitoring, independent checks cover the public site, data freshness, application health, database health, and the monitoring pipeline itself. Only a customer-facing outage, an active risk of data loss or corruption, or a blind paging system should wake me overnight. Degradation can wait for business hours. Capacity trends, self-healing events and most data-quality findings become tracked issues rather than notifications.

Most detailed telemetry stays close to the application, with only a curated subset sent to external services. The direct monitoring bill is modest. The larger cost is the time required to keep alerts useful and stop everything from becoming urgent.

### Incident one: the telemetry flood

A security-related configuration change produced an unexpectedly large volume of telemetry. The visible symptom appeared in the external monitoring service, so I investigated the shipping and filtering path first. The real source was deeper in the system: one event was generating a large family of related records, and every one of them was being shipped.

The wrong hypothesis lasted through the first investigation pass. I fixed the source, kept a volume limit in place as defense in depth, and added monitoring for telemetry spend and sudden changes in volume. If you ever flip a security policy from observe to enforce, budget for the audit records, not just the blocked behavior.

### Incident two: writes that succeed and change nothing

The second involved email-delivery feedback. The provider was sending events, but some internal delivery and suppression records were not being updated. My first suspicion was provider retries or webhook verification.

The actual problem was an interaction between the application's database permissions and an operation that legitimately needed to update a record without starting from a user session. The write returned successfully. It just didn't match any rows it was allowed to touch.

The fix was a much narrower write path, plus monitoring for both explicit errors and the more dangerous case: an operation that returns success and changes nothing. That second category doesn't show up in an error rate, and it's the one I'd tell people to go looking for in their own systems.

## Honest review

What I'd do again: invest in the delivery platform early. Reliable CI, realistic tests, progressive rollouts and automatic rollback compound the value of every agent working on the codebase.

What I'd do differently: establish the product's data semantics earlier, before building surfaces on top of them.

What's held together with tape: mostly operational automation, and simplifying areas that grew organically. Some procedures still require more founder attention than they should.

What I'm keeping private: exact traffic, revenue, customer counts, supplier economics, infrastructure costs and data volume. The site's <a href="https://cruisecaptain.ai/about" rel="noopener">about page</a> and <a href="https://cruisecaptain.ai/deals/methodology" rel="noopener">methodology page</a> are the public statements of what the data is and how it's interpreted.

The site is at <a href="https://cruisecaptain.ai" rel="noopener">cruisecaptain.ai</a>. If you've built something similar and reached different conclusions, especially about whether the delivery platform was worth it at this size, I'd like to hear it.

## FAQ

**What is CruiseCaptain built with?**
Go with the Chi router, server-rendered HTML with a small amount of JavaScript, PostgreSQL with TimescaleDB for price observations, and k3s with Argo for progressive delivery. CI runs on GitHub Actions with Ubicloud runners. The core application has three long-running roles: website, internal API and data worker, plus an isolated process for the MCP server.

**Where does CruiseCaptain's price data come from?**
A licensed cruise-industry inventory feed that aggregates pricing and availability from participating cruise lines, accessed under a commercial agreement. Nothing is scraped from cruise-line websites. Displayed fares are the most recent observed price, with the observation time shown.

**How does CruiseCaptain decide a price actually dropped?**
The comparison has to be with itself: same sailing, same cabin category, compatible fare basis. The current fare must be recent, currently available, materially below its normal range, and observed more than once. "The same fare got cheaper" and "a different, lower fare became available" are tracked and labeled as separate claims.

**What can the AI assistant not do?**
The Captain cannot book or purchase a cruise, predict future prices, change an account, or silently create an alert. Prices and availability come from structured search results rather than the model's memory, and it's instructed to say when evidence is insufficient.

**How is the MCP server kept separate from customer data?**
It exposes a small read-only set of tools over a separately prepared public catalog, with authentication, quotas and allowlists enforced outside the model. The agent-facing process cannot reach the internal API or database, and dependency and deployment tests fail the build if that boundary is crossed.

**Why run Kubernetes for a one-person project?**
Because AI agents made code generation fast enough that verification and deployment became the bottleneck. k3s with Argo gives gradual rollouts, health-based analysis and automatic rollback, which is what lets large changes ship routinely without lowering the production bar. The right denominator is engineering throughput, not traffic.
