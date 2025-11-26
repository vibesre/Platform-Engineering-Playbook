---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #037: KubeCon Atlanta 2025 Part 3: Community at 10 Years"
slug: 00037-kubecon-2025-community-sustainability
---

# KubeCon Atlanta 2025 Part 3: Community at 10 Years - The Sustainability Question

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 14 minutes
**Speakers:** Jordan and Alex
**Target Audience:** Platform team leads, open source contributors, engineering leadership invested in community sustainability

> 📝 **Read the [full blog post](/blog/kubecon-atlanta-2025-recap)**: Complete KubeCon Atlanta 2025 recap covering all 10 major announcements, technical breakthroughs, and community discussions.

:::info KubeCon 2025 Series (Part 3 of 3)

This is Part 3 of our three-part deep dive into KubeCon Atlanta 2025 (November 12-21), covering the CNCF's 10-year anniversary.

- **Part 1**: [AI Goes Native and the 30K Core Lesson](/podcasts/00035-kubecon-2025-ai-native) - DRA GA, CPU DRA, Workload API, OpenAI optimization, Kubernetes rollback
- **Part 2**: [Platform Engineering Consensus](/podcasts/00036-kubecon-2025-platform-engineering) - Three principles, real-world case studies, anti-patterns
- **Part 3** (this episode): Community at 10 years - Maintainer sustainability, burnout, technical sessions

:::

<div style={{maxWidth: '640px', margin: '2rem auto'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/w_PDgYRP4WU"
      title="KubeCon Atlanta 2025 Part 3: Community at 10 Years - The Sustainability Question"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

---

**Jordan**: The Cloud Native Computing Foundation turns ten years old. Three hundred thousand contributors. Two hundred thirty plus projects. One hundred ninety countries represented. The second-largest open source project on Earth. But between the keynote celebrations and the expo hall demos, the hallway track told a different story. In the breakout sessions, in the Day Zero events, we heard something the headlines missed.

**Alex**: That's the tension in this episode. Part 3 of our KubeCon Atlanta series. We've covered the technical breakthroughs in Part 1—DRA going GA, rollback finally working. The organizational consensus in Part 2—platform engineering's three principles. Today, we're asking the question nobody wants to answer: Can the people building this actually sustain the pace? And what did we learn in the technical sessions that didn't make the keynote stage?

**Jordan**: Let's start with the numbers that define sustainability. Sixty percent of open source maintainers are unpaid for their work. According to the twenty twenty-four Tidelift State of the Open Source Maintainer Report.

**Alex**: Sixty percent unpaid. For software that ninety-six percent of companies depend on. That asymmetry is the heart of the sustainability crisis.

**Jordan**: Another sixty percent of maintainers have either left or considered leaving a project. The reasons aren't about code. Competing life demands, fifty-four percent. Loss of interest, fifty-one percent. Burnout, forty-four percent.

**Alex**: And then there's the XZ Utils incident from twenty twenty-four.

**Jordan**: A seemingly helpful contributor exploited a solo maintainer's isolation over years. Slowly gained trust. Eventually inserted a malicious backdoor into widely-used software that could have compromised millions of systems. The fallout? Sixty-six percent drop in maintainer trust toward new contributors.

**Alex**: So now we have burned out maintainers who are also suspicious of new help. That's a death spiral.

**Jordan**: Which is why at KubeCon, we saw the human cost up close. Han Samuel Kang. Forty-two years old. Longtime contributor to Kubernetes SIG Node and kubelet. He passed away unexpectedly in September twenty twenty-five.

**Alex**: I saw the tribute. Self-taught engineer. Philosophy degree from UC Berkeley. Two daughters.

**Jordan**: He graduated high school at sixteen. Enlisted in the Army at seventeen. Found his way into tech as a self-taught programmer. Colleagues described his energy and enthusiasm. One said quote, "He stood out even in a company of exceptional people."

**Alex**: JG Macleod from Google mentioned him during the rollback announcement.

**Jordan**: Said quote, "This has taken literally a decade of effort. Han Kang's passing really hurts. This is a lasting legacy." The rollback feature that finally works after ten years—the one we covered in Part 1—has his fingerprints on it.

**Alex**: The technology doesn't exist without the people.

**Jordan**: And the people showed up not just in keynotes, but in the breakout sessions. Let's talk about what we learned in the rooms.

**Alex**: Starting with CiliumCon, the Day Zero event.

**Jordan**: TikTok presented their IPv6-only migration to Cilium. They shared specific challenges around scale—running eBPF-based networking at TikTok's traffic volumes means debugging issues that nobody else has seen. They talked about rolling out Cilium incrementally, cluster by cluster, with automated canary deployments to catch regressions before they propagate.

**Alex**: And Cilium itself hit its ten-year anniversary.

**Jordan**: Isovalent engineers talked about clusters now exceeding sixty thousand nodes running Cilium. The eBPF evolution from experimental to production default took a decade. Same timeline as Kubernetes reaching maturity. Same lesson: infrastructure at this scale takes years, not months.

**Alex**: What about security sessions?

**Jordan**: Supply chain security had its own track. The "Supply Chain Reaction" presentation walked through attack vectors that go beyond just compromised dependencies. Build system compromises. CI pipeline injection. Artifact registry poisoning. The XZ Utils pattern was explicitly referenced as the canonical example of social engineering meeting technical exploitation.

**Alex**: And in-toto graduated.

**Jordan**: CNCF's supply chain provenance project hit graduated status. It's now production-ready for generating cryptographically signed attestations about your entire build pipeline. Who built what, when, with which tools, from which sources. Combined with SBOM generation, you can now trace a container image back to its original commit and build environment.

**Alex**: That connects to the EU Cyber Resilience Act requirements we discussed in Part 2.

**Jordan**: Exactly. SBOM plus in-toto attestations equals CRA compliance by twenty twenty-seven. The tooling exists now.

**Alex**: What about Gateway API sessions?

**Jordan**: HAProxy presented their Unified Gateway implementation. The pattern is converging—instead of separate ingress controllers and API gateways and service meshes, a single gateway handling north-south and east-west traffic with Gateway API as the common interface.

**Alex**: And there was AI-specific Gateway work.

**Jordan**: Kgateway showed an AI Inference Extension that adds routing semantics specific to LLM workloads. Token-based rate limiting. Model version routing. Request queuing for batch inference. The Gateway API extensibility model lets you add these without forking the core specification.

**Alex**: Observability Day had significant announcements too.

**Jordan**: OpenTelemetry's eBPF instrumentation is maturing. We covered this in Episode twenty-eight. The KubeCon sessions showed production deployments where teams get complete distributed tracing without changing a single line of application code. The catch we mentioned—TLS encryption breaking eBPF visibility—has workarounds now using shared library interception.

**Alex**: Nike presented their OpAMP implementation.

**Jordan**: OpenTelemetry's Agent Management Protocol. Nike is using it to manage thousands of collectors across their infrastructure. Central configuration. Remote updates. Health monitoring. The scale challenges are real—when you have that many agents, the management plane itself becomes a distributed systems problem.

**Alex**: So the technical sessions showed real production implementations, not just demos.

**Jordan**: Which is the difference between KubeCon twenty twenty and KubeCon twenty twenty-five. Five years ago, these sessions were "here's what we're trying." Now they're "here's what we learned running this for three years at scale."

**Alex**: Let's shift back to sustainability. What signs of hope emerged?

**Jordan**: The Open Source Pledge initiative. Companies commit to paying maintainers directly. Minimum two thousand dollars per year per developer at your company. Cash payments, not cloud credits. Not hiring developers to work on open source. Not gifts. Cash to the people doing the work.

**Alex**: Who's actually participating?

**Jordan**: Antithesis contributed one hundred ten thousand dollars. That's two thousand eight hundred ninety-five per developer on staff. Ninety-five thousand went to the Nix core team alone. Convex put one hundred thousand toward TanStack Start. That's seven thousand six hundred ninety-two per developer. These are real numbers. Not symbolic gestures.

**Alex**: And Kubernetes itself made governance improvements.

**Jordan**: The release team went from six subteams to four. Bug Triage and CI Signal merged into Release Signal. Project boards for enhancement tracking. The change got unanimous applause from release team members because it reduced coordination overhead.

**Alex**: So what's the survival strategy for maintainers?

**Jordan**: Kat Cosgrove, newly elected to the Kubernetes Steering Committee, was brutally honest about this. She described lying to coworkers and friends at long conferences to steal alone time at restaurants with a book. Not working at all in December. Spending time in the mountains without cell signal or electronics.

**Alex**: Wait, she framed those as survival strategies?

**Jordan**: Quote, "When you're an open source maintainer and developer advocate, you don't get to have a bad day in public." These aren't nice-to-haves. They're how you avoid complete burnout. And most maintainers are quote "crispy." Her word. They're all burned out. The trick is not letting people see it.

**Alex**: Public persona always on, even when you're exhausted.

**Jordan**: Which is why the advice for maintainers is: build contributor ladders. Promote contributors into leadership to share the workload. Take real time off. Be honest about burnout instead of hiding it. And build succession pipelines. The worst outcome is a critical project with no one ready to take over.

**Alex**: Red flags to watch for?

**Jordan**: Solo maintainer on a critical project. That's the XZ Utils pattern waiting to happen. No corporate backing for dedicated time. Missing contributor ladder. All contributors from a single company. Maintainers visibly exhausted on social media. These are warning signs of unsustainable projects that could affect your infrastructure.

**Alex**: Let's bring it back to the series. What's the complete picture of KubeCon Atlanta twenty twenty-five?

**Jordan**: Part 1 was technical capability. DRA went GA—ten to forty percent GPU performance improvement by fixing NUMA alignment. OpenAI freed thirty thousand CPU cores with one line of code. Kubernetes rollback finally works after ten years. The message: the technology is mature and still accelerating.

**Alex**: Part 2 was organizational clarity.

**Jordan**: Platform engineering consensus after years of definitional chaos. Three principles: API-first self-service, business relevance, managed service approach. Real adoption at Intuit, Bloomberg, ByteDance scale. The "puppy for Christmas" anti-pattern explains why templates without operational support fail. The message: we know what to build and how to measure success.

**Alex**: And Part 3?

**Jordan**: Is the sustainability question. Sixty percent maintainers unpaid. Sixty percent have left or considered leaving. Han Kang's passing reminds us of the human cost. The technical sessions showed what ten years of community effort looks like—Cilium at sixty thousand nodes, in-toto graduated, Gateway API converging. Open Source Pledge provides a funding path. The message: now invest in the humans who make all of this possible.

**Alex**: So what's the framework for listeners?

**Jordan**: Three actions. First, check if your company is on the Open Source Pledge. Two thousand dollars per developer per year minimum. If not, start that conversation with leadership. Second, audit your critical dependencies for maintainer health. How many maintainers? Are they employed to do this work? When did they last take time off? Is there a succession plan?

**Alex**: And third?

**Jordan**: Remember the throughline of this series. Han Kang's legacy lives in Kubernetes reliability. The Cilium engineers spent ten years getting eBPF to production default. The in-toto maintainers got supply chain attestation to graduated status. These aren't anonymous contributors. They're people who chose to spend their lives on this. They deserve sustainability—predictable income, reasonable workloads, time off without guilt, succession plans so they can step back when needed.

**Alex**: That's the real work for the next decade.

**Jordan**: The code doesn't exist without the people who write it. The technical sessions showed what sustained community investment creates. The burnout statistics show what happens without it. Invest accordingly.

**Alex**: This has been Part 3 of our three-part KubeCon Atlanta twenty twenty-five series. Part 1 covered the technical breakthroughs. Part 2, platform engineering consensus. Part 3, the sustainability question and what we learned in the breakout rooms. Together, a complete picture of where cloud native is and where it's going.

**Jordan**: Until next time.
