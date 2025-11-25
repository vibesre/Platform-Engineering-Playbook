---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #035: KubeCon Atlanta 2025 Part 1: AI Goes Native and the 30K Core Lesson"
slug: 00035-kubecon-2025-ai-native
---

# KubeCon Atlanta 2025 Part 1: AI Goes Native and the 30K Core Lesson

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 19 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience running or considering AI/ML workloads

> 📝 **Read the [full blog post](/blog/kubecon-atlanta-2025-recap)**: Complete KubeCon Atlanta 2025 recap covering all 10 major announcements, including platform engineering consensus, community challenges, and the EU Cyber Resilience Act explained.

:::info KubeCon 2025 Series (Part 1 of 3)

This is Part 1 of our three-part deep dive into KubeCon Atlanta 2025 (November 12-21), covering the CNCF's 10-year anniversary.

- **Part 1** (this episode): AI-native Kubernetes - DRA GA, CPU DRA, Workload API, OpenAI's 30K core optimization, rollback after 10 years
- **Part 2**: [Platform Engineering Consensus](/podcasts/00036-kubecon-2025-platform-engineering) - Three principles, real-world case studies, anti-patterns
- **Part 3**: Community at 10 years - Maintainer sustainability, burnout, the next decade

:::

<div style={{maxWidth: '640px', margin: '2rem auto'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/ZNIyuQIVBI8"
      title="KubeCon Atlanta 2025 Part 1: AI Goes Native and the 30K Core Lesson"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

---

**Jordan**: Welcome to Part 1 of our three-part deep dive into KubeCon Atlanta twenty twenty-five. Over the next three episodes, we're covering everything that happened from November twelfth through twenty-first—the CNCF's ten-year anniversary, the announcements that will reshape platform engineering, and the honest conversations about what it takes to keep this ecosystem sustainable.

**Alex**: Today in Part 1, we focus on the technical breakthroughs that prove Kubernetes isn't just supporting AI workloads—it's being rebuilt as an AI-native platform. Tomorrow in Part 2, we'll cover platform engineering reaching consensus and real-world adoption stories. And in Part 3, we tackle the harder questions: maintainer burnout, community sustainability, and what the next ten years might look like.

**Jordan**: But first, let's start with a mystery. Google's on stage at the opening keynote, and they do something unusual.

**Alex**: November twenty twenty-five. Kubernetes turns ten. Google's on stage at KubeCon Atlanta. And they donate a driver to CNCF live. Not a project. Not a tool. A driver. For GPUs.

**Jordan**: Wait, why would Google donate GPU infrastructure code in the middle of a keynote?  That seems... specific.

**Alex**: Because it's not about the driver. It's about what the driver represents.  Kubernetes isn't adapting to AI workloads anymore. It's being rebuilt for them.

**Jordan**: Okay, that's a strong claim. Back it up.  What changed at KubeCon twenty twenty-five that makes this different from, say, KubeCon twenty twenty-three?

**Alex**: Four technical announcements.  Let me walk through them, and you'll see the pattern.

**Jordan**: I'm listening.

**Alex**: First, Dynamic Resource Allocation—DRA—reached GA in Kubernetes one point thirty-four.  This is the driver Google donated on stage.

**Jordan**: GA means production-ready. Not experimental, not beta.  Why does DRA matter?

**Alex**: Because of how Kubernetes used to allocate GPUs.  The old device plugin architecture would grab any available GPU and assign it to a pod. Sounds fine, right?

**Jordan**: Except modern systems are NUMA—Non-Uniform Memory Access.  GPU on one node, CPUs on another node, and suddenly your expensive training job is crawling.

**Alex**: Exactly. And the performance hit?  Ten to forty percent degradation.

**Jordan**: Wait. Hold on.  Forty percent?  That's not optimization territory. That's a misconfiguration disaster.

**Alex**: Tim Wickberg from SchedMD—the company that makes Slurm, the dominant HPC scheduler—he said HPC workloads can see thirty to forty percent performance differences from misaligned versus aligned resources.

**Jordan**: Okay, let's do the math.  Five thousand dollars a day for a pre-training workload. Forty percent waste.  That's two thousand dollars per day per node just evaporating.

**Alex**: Scale that to a hundred nodes.  Two hundred thousand dollars a day.

**Jordan**: From something you can't even see unless you're profiling at the NUMA level.  That's terrifying.

**Alex**: DRA solves this. It understands topology. It knows which CPUs are on the same NUMA node as which GPUs.  It can make intelligent placement decisions.

**Jordan**: And this is GA now. Production-ready. Not "coming soon," not "experimental." If you're running GPU workloads on Kubernetes without DRA, you could be losing nearly half your performance?

**Alex**: On misaligned workloads, yes. The scary part is you wouldn't even know unless you're profiling at the NUMA level.

**Jordan**: So what's the migration path? Can teams actually adopt this?

**Alex**: Here's the good news. Kubernetes one point thirty-four includes both DRA and the legacy device plugins. No forced migration. You test in development first, measure the performance difference. If you're seeing greater than ten percent improvement, you plan your production migration.

**Jordan**: And the DRA-Net driver Google donated?

**Alex**: It implements the standard DRA interface. Google's basically saying "Here's the reference implementation. Topology awareness is now baseline infrastructure for AI."

**Jordan**: If you're running GPU workloads without DRA, you're burning money.

**Alex**: Exactly. But here's where it gets interesting. DRA isn't just for GPUs anymore.

**Jordan**: Wait, what else is there?

**Alex**: CPUs. The CPU DRA driver was announced at KubeCon twenty twenty-five.

**Jordan**: Hold on. Why do CPUs need topology awareness? Aren't they already... on the CPU?

**Alex**: Think about HPC workloads. Computational fluid dynamics, molecular modeling, financial simulations. These aren't GPU workloads. They're CPU-intensive, but they need precise CPU placement and memory locality.

**Jordan**: And HPC has resisted Kubernetes for years.

**Alex**: Right. Slurm dominates sixty percent plus of the Top five hundred supercomputers. Why? Because Kubernetes couldn't handle CPU topology requirements. But now with CPU DRA...

**Jordan**: Kubernetes and Slurm can work together.

**Alex**: Tim Wickberg said, quote, "We've seen thirty to forty percent performance differences in HPC workloads from resource alignment. DRA brings that awareness to Kubernetes. This opens the door for HPC workloads that were previously impossible."

**Jordan**: So Kubernetes is converging with HPC. That's a bigger deal than it sounds.

**Alex**: Right, because HPC has decades of battle-tested knowledge about resource scheduling. If Slurm and Kubernetes can work together, you get the best of both worlds. Same infrastructure can run containerized microservices AND high-performance computing.

**Jordan**: But it also means Kubernetes is getting more sophisticated. This isn't your twenty fifteen container orchestrator anymore.

**Alex**: That's the tension. For web applications, this is overkill. But if you're running CPU-intensive scientific computing, this is transformative.

**Jordan**: Right tool for the job.

**Alex**: Exactly. Which brings us to announcement two. The Workload API, coming in alpha for Kubernetes one point thirty-five.

**Jordan**: Workload API.  I'm guessing this solves the gang-scheduling problem?

**Alex**: You've been reading ahead. Yeah.  Here's the scenario. You submit a thousand-pod distributed training job. Kubernetes, treating each pod independently, successfully schedules eight hundred pods.

**Jordan**: And the remaining two hundred never get resources.  Meanwhile, those eight hundred running pods are consuming thousands of dollars an hour in GPU time, doing nothing, waiting for workers that will never arrive.

**Alex**: Exactly. The partial failure nightmare.  Eric Tune from Google said pre-training workloads use every accelerator the customer can acquire. Hardware failures happen every couple of days.  The time to recover and restart is a significant reduction in cost.

**Jordan**: So Workload API makes Kubernetes understand that certain groups of pods must be scheduled atomically.  All or nothing.

**Alex**: Right. If the cluster can't accommodate the entire workload, none of it starts.  You don't waste resources on partial failures.

**Jordan**: This is the gang-scheduling problem that HPC solved decades ago.  But Kubernetes was built for stateless microservices. AI forced the re-architecture.

**Alex**: That's exactly it.  Kubernetes at ten years isn't slowing down. It's being redesigned at the infrastructure and scheduling layers to be AI-native.

**Jordan**: Okay, announcements one and two are about infrastructure redesign.  What's announcement three?

**Alex**: OpenAI.  Ten petabytes of logs per day. They're using Fluent Bit as the log collector across their Kubernetes fleet.  And they noticed Fluent Bit consuming way too much CPU.

**Jordan**: Define "way too much."

**Alex**: They profiled with perf—the Linux profiling tool.  Fstat sixty-four, a system call, was consuming thirty-five percent of CPU time.

**Jordan**: Thirty-five percent on a single system call?  What was causing it?

**Alex**: Inotify. Watching log files for changes. Unnecessary in their architecture.  So they disabled inotify in the Fluent Bit config. One line of code.  Result? Fifty percent CPU reduction.

**Jordan**: Wait. Fifty percent reduction from... disabling file watching?

**Alex**: Yep. And here's the kicker.  Thirty thousand CPU cores freed.

**Jordan**: Thirty thousand cores. Let me get the calculator out.  Cloud pricing, roughly ten cents per core-hour. Thirty thousand cores times point one times twenty-four hours times thirty days.  That's two point one six million dollars per month.

**Alex**: From. One. Line. Of. Code.

**Jordan**: Okay but how many platform teams actually profile their critical services?  Be honest.

**Alex**: That's the point. OpenAI isn't special. They're just measuring.  Fabian Ponce from their Applied Observability Team said, quote, "Sometimes you might just find something surprising."

**Jordan**: The fruit is low-hanging. You just have to look.  What's announcement four?

**Alex**: Kubernetes rollback.  After ten years, it finally works.

**Jordan**: Hold on. Kubernetes launched in twenty fifteen.  For ten years, cluster upgrades were one-way operations?

**Alex**: If an upgrade broke something, you couldn't roll back.  You could only try to upgrade forward to a fixed version. This kept organizations on old versions, accumulating security debt.

**Jordan**: And now?

**Alex**: Ninety-nine point ninety-nine percent upgrade success rate across GKE control planes and nodes.  Skip-version upgrades supported. You can upgrade once a year instead of quarterly.

**Jordan**: That's a seventy-five percent reduction in operational burden just from safe upgrades.

**Alex**: JG Macleod from Google announced this.  But there was also a memorial. Han Kang, who passed away in twenty twenty-five, worked extensively on Kubernetes reliability.  Macleod said, quote, "This has taken literally a decade of effort. Han Kang's passing really hurts. This is a lasting legacy."

**Jordan**: That hits different. We talk about technical achievements, but there are people behind all of this.

**Alex**: Yeah. Kubernetes at ten years is bittersweet. Amazing technical progress. But also the reminder of what it cost to get here.

**Jordan**: Let's connect these four announcements. DRA for GPU and CPU topology. Workload API for multi-pod coordination. OpenAI's profiling lesson. Rollback after ten years. What's the throughline?

**Alex**: Infrastructure redesign, scheduler redesign, operational maturity, production reliability.  Kubernetes isn't just supporting AI workloads. It's being rebuilt at every layer to be an AI-native platform.

**Jordan**: So when people say "Kubernetes is getting too complex," what's the right response?

**Alex**: Loaded question.  Yes, DRA adds complexity. But the alternative is forty percent of your GPU spend down the drain.  That's not complexity tax. That's appropriate sophistication for modern workloads.

**Jordan**: I buy that for organizations running AI workloads at scale.  But what about the majority of companies not doing large-scale distributed training?

**Alex**: Fair. If you're running single-GPU workloads, DRA overhead probably isn't worth it.  If you don't have multi-pod coordination needs, Workload API is overkill. Get the basics right first.

**Jordan**: Basics like... profiling?

**Alex**: Exactly. The OpenAI lesson applies to everyone.  How many platform teams have continuous profiling in production? How many regularly use perf or eBPF?

**Jordan**: Very few.  And that's free optimization.

**Alex**: If OpenAI found two point one six million a month in savings, you likely have opportunities.  Maybe not thirty thousand cores. But three hundred? Three thousand? Still transformative.

**Jordan**: Alright. Let's get practical.  If I'm a platform engineer listening to this, what do I do Monday morning?

**Alex**: This month, December twenty twenty-five. Three actions.  One: Test Kubernetes one point thirty-four in a development cluster with DRA enabled.  Two: Profile your number-one CPU consumer. Use perf top or eBPF-based tooling. Spend thirty minutes.  Three: Check if you're losing performance to NUMA misalignment right now.

**Jordan**: And then what?  Assuming you find something.

**Alex**: Q one twenty twenty-six.  Measure DRA performance improvement. If you see greater than ten percent, plan production migration for Q two.  Pilot Workload API for multi-pod training jobs—it's alpha in Kubernetes one point thirty-five.  By Q three, Workload API should hit beta. Plan production adoption.

**Jordan**: What about the skip-version upgrades?

**Alex**: Test upgrading annually versus quarterly.  If you can reduce upgrade frequency by seventy-five percent while maintaining security currency, that's a massive operational win.

**Jordan**: When should you NOT adopt these technologies?

**Alex**: Single-GPU workloads—DRA overhead not worth it.  No multi-pod coordination needs—Workload API unnecessary.  And critically, if you don't have operational maturity for complex orchestration, get the basics right first. Profiling. Monitoring. Incident response.

**Jordan**: That's the sobering part.  Kubernetes at ten years has incredible capabilities. But it assumes a level of operational maturity that most teams don't have.

**Alex**: Right. And that's where the OpenAI lesson becomes universal.  Profiling isn't advanced. Perf is a standard Linux tool. Thirty minutes on a Monday morning.  If you find a function consuming more than twenty percent of CPU time, investigate.

**Jordan**: One optimization could fund an entire platform team's salary.

**Alex**: Exactly. The technical announcements are impressive. DRA for GPUs and CPUs. Workload API. These aren't incremental improvements. They're architectural shifts.

**Jordan**: But the thirty-thousand-core story is the reminder that basics matter. Profile. Measure. Optimize.

**Alex**: AI-native platform requires both. Sophisticated infrastructure AND operational discipline.

**Jordan**: Kubernetes at ten years isn't slowing down. If anything, it's accelerating. DRA going GA. Workload API arriving. These aren't incremental improvements. They're architectural shifts.

**Alex**: And for the folks wondering if Kubernetes is too complex now?

**Jordan**: Ask a different question. Is the complexity justified by the problems it solves? If you're running large-scale AI workloads, losing forty percent to NUMA misalignment, then yeah, DRA complexity is worth it. If you're not, maybe Kubernetes isn't the right tool.

**Alex**: That's the honest answer. Kubernetes has evolved to handle workloads that didn't exist in twenty fifteen. AI training across thousands of GPUs. Geo-temporal ML at Pokemon Go scale. Ten petabytes of daily logs at OpenAI.

**Jordan**: But if your workload is a standard web app with a database, you probably don't need the AI-native features. And that's okay. Use the right tool for the job.

**Alex**: Final thought. What's the one thing listeners should remember from this episode?

**Jordan**: Measure before you optimize. OpenAI found two point one six million a month because they profiled. If you're not profiling your critical path services, you're leaving money on the table.

**Alex**: And if you are running AI workloads, DRA is production-ready. Test it. The ten to forty percent performance difference is real.

**Jordan**: That's the technical story from KubeCon twenty twenty-five. Dynamic Resource Allocation going GA. CPU DRA enabling HPC convergence. Workload API solving gang-scheduling. And OpenAI's reminder that profiling matters.

**Alex**: But there's another story from KubeCon that's just as important. After years of definitional chaos—"What even IS platform engineering?"—the industry reached consensus. Three principles. Real-world case studies from Intuit, Bloomberg, and ByteDance. And the anti-patterns that doom platform teams to failure.

**Jordan**: Tomorrow in Part 2, we cover platform engineering's coming-of-age moment, the "puppy for Christmas" problem, and why self-assessment might be the most important tool you're not using.

**Alex**: This has been Part 1 of our three-part KubeCon Atlanta twenty twenty-five coverage.

**Jordan**: Test DRA in development. Profile your top CPU consumer. Check for NUMA misalignment. See you tomorrow.
