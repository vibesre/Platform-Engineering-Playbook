---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #048: Developer Experience Metrics Beyond DORA"
slug: 00048-developer-experience-metrics-beyond-dora
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #048: Developer Experience Metrics Beyond DORA

<GitHubButtons />

**Duration**: 13 minutes | **Speakers**: Jordan & Alex

**Target Audience**: Platform engineers, engineering managers, and DevOps leaders measuring team productivity

---

## Watch the Episode

<div style={{maxWidth: '640px', margin: '0 auto 1.5rem'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/zXgMpd9jlj8"
      title="Developer Experience Metrics Beyond DORA"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

---

## Synopsis

DORA metrics revolutionized how we measure DevOps performance, but are we missing the bigger picture? This episode explains DORA from the ground up—the four key metrics, how they're measured, and why elite teams deploy more AND fail less. Then we explore what DORA misses: developer satisfaction, cognitive load, and flow state. From SPACE to DevEx to DX Core 4, discover the frameworks changing how we measure developer productivity.

---

## Chapter Markers

- **00:00** - Introduction & News Segment
- **01:30** - What is DORA? The Foundation
- **04:00** - The Four Key Metrics Explained
- **06:00** - Benchmarks: Elite vs Low Performers
- **07:30** - What DORA Misses
- **08:30** - SPACE Framework: Five Dimensions
- **10:00** - DevEx and DX Core 4
- **12:00** - Practical Implementation Guide
- **13:00** - Closing

---

## News Segment (December 6, 2025)

- **[Iterate.ai AgentOne](https://thenewstack.io/iterate-ai-launches-agentone-for-enterprise-ai-code-security/)**: First enterprise-grade solution to sandbox and audit AI agent activity
- **[AWS Durable Functions](https://www.infoq.com/news/2025/12/aws-lambda-durable-functions/)**: Stateful logic directly in Lambda code
- **[Capital One OpenTelemetry](https://thenewstack.io/how-capital-one-cut-tracing-data-by-70-with-opentelemetry/)**: Cut tracing data by 70%

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| DORA survey respondents (2024) | 39,000+ professionals | Google Cloud State of DevOps 2024 |
| AI tool usage | 75%+ use daily | DORA 2024 Report |
| Elite performer change failure rate | ~5% | DORA 2024 Report |
| Low performer change failure rate | ~40% | DORA 2024 Report |
| Elite lead time | Less than 1 day | DORA 2024 Report |
| Low performer lead time | More than 1 month | DORA 2024 Report |
| DX Core 4 efficiency improvement | 3-12% | DX research (300+ orgs) |

---

## Frameworks Covered

### DORA (2018)
Four Key Metrics: Deployment Frequency, Lead Time for Changes, Change Failure Rate, Mean Time to Recovery (MTTR)

### SPACE (2021)
Five Dimensions: Satisfaction and well-being, Performance, Activity, Communication and collaboration, Efficiency and flow

### DevEx (2023)
Three Dimensions: Feedback Loops, Cognitive Load, Flow State

### DX Core 4 (Latest)
Four Dimensions: Speed, Effectiveness, Quality, Impact

---

## Transcript

**Jordan**: Today we're tackling something that affects every platform team: how do you actually measure developer productivity? But first, let's check the pulse of platform engineering.

**Jordan**: Enterprise AI security just got serious. Iterate dot AI launched AgentOne, the first enterprise-grade solution specifically designed to sandbox and audit AI agent activity. If you're worried about developers using AI coding assistants and exposing your codebase to data leaks, this addresses that head-on.

**Jordan**: AWS dropped Durable Functions for Lambda. Stateful logic directly in Lambda code, managing state and retry logic without incurring costs during wait times. This changes the game for multi-step workflows.

**Jordan**: And Capital One shared how they cut tracing data by seventy percent with OpenTelemetry. Real enterprise optimization story worth reading if you're dealing with observability costs.

**Jordan**: Now, let's talk about measuring what matters. Alex, DORA metrics have become the gold standard for measuring DevOps performance. But there's growing recognition that they're not the complete picture.

**Alex**: Right. And before we talk about what comes after DORA, let's make sure everyone understands what DORA actually is. Because I still meet teams who've heard the term but don't really know how it works.

**Jordan**: So let's start from the beginning. DORA stands for DevOps Research and Assessment. It originated from the State of DevOps reports that started at Puppet Labs and later moved to Google Cloud. The key researcher behind it was Doctor Nicole Forsgren.

**Alex**: And the core insight from years of research was this: you can measure DevOps performance with just four metrics. These became known as the Four Key Metrics or DORA metrics.

**Jordan**: Let's walk through them. The first is Deployment Frequency. How often does your team deploy code to production? Elite teams deploy multiple times per day. Low performers might deploy monthly.

**Alex**: Second is Lead Time for Changes. This measures the time from when code is committed to when it's running in production. Elite teams do this in less than a day. Low performers can take a month or more.

**Jordan**: Third is Change Failure Rate. What percentage of deployments cause a failure in production that requires a rollback or fix? Elite teams sit around five percent. Low performers can hit forty percent.

**Alex**: And fourth is Mean Time to Recovery, or MTTR. When something does break, how quickly can you restore service? Elite teams recover in less than an hour. Low performers can take days.

**Jordan**: The twenty twenty-four DORA report actually refined that fourth metric. They renamed it Failed Deployment Recovery Time to be more specific about measuring software deployment failures, not all incidents.

**Alex**: And here's the big insight from ten years of DORA research. Throughput and stability are not trade-offs. Teams that deploy more frequently actually have lower failure rates and faster recovery times. Speed and quality go together.

**Jordan**: The twenty twenty-four report surveyed over thirty-nine thousand professionals globally. They found that seventy-five percent now use AI tools daily. Interestingly, AI shows a seven point five percent improvement in documentation quality and three point four percent in code quality. But here's the catch.

**Alex**: The same report found a one point five percent reduction in overall delivery performance and a seven point two percent decrease in delivery stability when AI adoption increases. Individual gains aren't translating to organizational improvements yet.

**Jordan**: And the twenty twenty-five report replaced the traditional low, medium, high, and elite performance categories with seven distinct team archetypes. More nuanced, but also more complex to interpret.

**Alex**: So DORA gives us a solid foundation. But here's the problem. DORA measures delivery performance. It doesn't measure developer experience.

**Jordan**: What do you mean by that?

**Alex**: DORA can tell you how fast your pipeline is. It can't tell you if your developers are burning out running it. Teams can hit elite DORA numbers while their engineers are miserable, drowning in technical debt, and constantly interrupted.

**Jordan**: What specifically does DORA miss?

**Alex**: Developer satisfaction and well-being. Cognitive load and burnout risk. Collaboration quality. Time spent in flow state. How effective your onboarding is. And the business impact beyond just shipping code.

**Jordan**: There's also the gaming problem. Any metric you measure can be gamed. Teams can optimize for DORA numbers without actually improving.

**Alex**: Exactly. So researchers developed new frameworks to fill these gaps. The first major one was SPACE, introduced in twenty twenty-one.

**Jordan**: And interestingly, Doctor Nicole Forsgren, the same researcher behind DORA, was one of the authors. Along with researchers from Microsoft and the University of Victoria.

**Alex**: SPACE is an acronym for five dimensions of developer productivity. S is for Satisfaction and well-being. Are developers happy? Fulfilled? At risk of burnout?

**Jordan**: P is for Performance. Not just speed, but quality of code, reliability of systems, and impact on customers.

**Alex**: A is for Activity. The volume of work: commits, pull requests, code reviews, deployments. This overlaps with DORA.

**Jordan**: C is for Communication and Collaboration. How well are teams working together? What's the quality of code reviews? How quickly do people get unblocked?

**Alex**: And E is for Efficiency and Flow. Can developers focus deeply without constant interruptions? Are they spending time on valuable work or fighting tooling?

**Jordan**: The key recommendation from the SPACE authors is to track at least three metrics across different dimensions. And at least one should be a perceptual measure, meaning surveys that capture how developers actually feel.

**Alex**: There's a symbolic change worth noting. Microsoft and GitHub recently renamed their joint research group from the Developer Velocity Lab to the Developer Experience Lab. Experience, not just velocity.

**Jordan**: So we have DORA for delivery performance, SPACE for a multi-dimensional view. What came next?

**Alex**: In twenty twenty-three, another framework emerged called DevEx. It focuses on the lived experience of developers and the friction they encounter daily.

**Jordan**: DevEx distills developer experience into three dimensions. First, Feedback Loops. How quickly do developers get information about their work? Can they test locally? How fast is CI? How long do code reviews take?

**Alex**: Second, Cognitive Load. How much mental effort is required to complete tasks? Are systems well-documented? Are there too many tools to juggle? Is the codebase understandable?

**Jordan**: Third, Flow State. Can developers focus deeply? Are they constantly interrupted by meetings, Slack, and context switching? Do they have blocks of uninterrupted time?

**Alex**: DevEx is less about metrics and more about identifying friction points. Where are developers getting stuck? What's slowing them down? What's frustrating them?

**Jordan**: And now we have the latest evolution: the DX Core 4. This attempts to unify DORA, SPACE, and DevEx into a single framework.

**Alex**: The DX Core 4 organizes everything into four dimensions. Speed, Effectiveness, Quality, and Impact.

**Jordan**: Speed includes diffs per engineer, meaning pull requests or merge requests, along with lead time and deployment frequency from DORA.

**Alex**: Effectiveness is where it gets interesting. The key metric is the Developer Experience Index, or DXI. It's a fourteen-question research-backed survey. Also included are regrettable attrition, measuring developer churn, and time to tenth PR, which measures onboarding effectiveness.

**Jordan**: Quality includes change failure rate and recovery time from DORA, plus perceived software quality from surveys.

**Alex**: And Impact frames everything in business terms. Percentage of time spent on new capabilities versus maintenance. Initiative progress. Actual return on investment.

**Jordan**: The DX Core 4 has been tested with over three hundred organizations. They report three to twelve percent increases in engineering efficiency and fourteen percent more time spent on feature development.

**Alex**: But there are legitimate concerns. The DXI survey is proprietary. There's heavy dependence on perception-based data. And metrics like diffs per engineer can encourage gaming if not handled carefully.

**Jordan**: So with all these frameworks, what should platform teams actually do?

**Alex**: Start where you are. If you're not measuring anything, start with DORA. It's well-understood, has great tool support, and gives you a baseline.

**Jordan**: If you already have DORA and want more, add SPACE dimensions. Specifically, start with a developer satisfaction survey. Quarterly is enough. Keep it short.

**Alex**: Measure cognitive load indicators. How often do developers context switch? How many tools do they need to use daily? How much documentation do they need to hunt for?

**Jordan**: Track flow state signals. How many hours of uninterrupted deep work per week? What's the meeting load? How often are people getting pinged?

**Alex**: And here are the mistakes to avoid. Don't tie these metrics to individual performance reviews. That's a recipe for gaming.

**Jordan**: Don't cherry-pick. If you only measure what looks good, you're not measuring reality.

**Alex**: Avoid survey fatigue. Quarterly surveys maximum. More frequent than that and response rates collapse.

**Jordan**: And don't ignore qualitative feedback. Numbers without context mislead. A satisfaction score of three point five means nothing without understanding why.

**Alex**: For platform engineering specifically, these metrics validate what we build. Golden paths reduce cognitive load. Self-service reduces feedback loop time. Good abstractions enable flow state.

**Jordan**: Internal Developer Portals are measurably improving all dimensions. Service catalogs reduce cognitive load. Scaffolding templates improve time to tenth PR. Self-service provisioning speeds up feedback loops.

**Alex**: The connection to platform engineering is direct. If your platform isn't improving developer experience metrics, you need to rethink what you're building.

**Jordan**: So where does this leave us?

**Alex**: DORA was revolutionary. It gave us a common language for delivery performance. But it's not enough by itself.

**Jordan**: SPACE expanded our view to include satisfaction, collaboration, and efficiency. DevEx focused on the friction developers actually experience. And DX Core 4 is trying to unify everything.

**Alex**: The framework you choose matters less than the commitment to measure thoughtfully. Track multiple dimensions. Include perceptual data. Don't game the numbers.

**Jordan**: The best metric is the one that changes behavior for the better. DORA changed how we think about delivery. These newer frameworks are changing how we think about the people doing the delivering.

**Alex**: Fast pipelines don't matter if your developers are burned out. Elite DORA scores don't matter if no one wants to work on your team.

**Jordan**: Measure what matters. And remember that behind every metric is a human being trying to do their best work.
