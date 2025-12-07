# Episode #048: Developer Experience Metrics Beyond DORA

## Episode Metadata
- **Episode Number**: 048
- **Target Duration**: 15-18 minutes
- **Speakers**: Jordan and Alex
- **Target Audience**: Platform engineers, engineering managers, and DevOps leaders measuring team productivity

## Narrative Arc

**Central Question**: DORA metrics revolutionized how we measure delivery performance, but are we missing the bigger picture of developer experience?

**Throughline**: From DORA's focus on delivery to a holistic view of developer productivity and well-being

**Emotional Journey**: Validation (DORA works) → Concern (but it's incomplete) → Discovery (SPACE, DevEx, DX Core 4) → Empowerment (actionable framework)

## Story Structure

### ACT 1: THE DORA FOUNDATION (4-5 min)
**Purpose**: Establish what DORA is, how it works, and why it matters

**Key Points**:
- Origin story: DevOps Research and Assessment, Dr. Nicole Forsgren, Google Cloud
- The Four Key Metrics (with definitions):
  1. **Deployment Frequency**: How often code ships to production
  2. **Lead Time for Changes**: Time from commit to production
  3. **Change Failure Rate**: Percentage of deployments causing failures
  4. **Mean Time to Recovery (MTTR)**: Time to restore service after failure
- 2024 update: MTTR → Failed Deployment Recovery Time (FDRT)

**Benchmarks (2024 Report)**:
- Elite performers: Deploy multiple times/day, lead time <1 day, 5% failure rate, recover in <1 hour
- Low performers: Deploy monthly, lead time >1 month, 40% failure rate, recovery takes days

**The Big Insight**: Throughput correlates with stability (counterintuitive but proven over 10 years)

**Statistics**:
- 39,000+ professionals surveyed in 2024 report
- 75%+ use AI tools daily
- 7 team archetypes replace low/medium/high/elite in 2025 report

### ACT 2: THE LIMITATIONS (3-4 min)
**Purpose**: Show why DORA alone isn't enough

**Key Points**:
- DORA measures *delivery performance*, not *developer experience*
- What DORA misses:
  - Developer satisfaction and well-being
  - Cognitive load and burnout risk
  - Collaboration quality
  - Time in flow state
  - Onboarding effectiveness
  - Business impact beyond shipping
- The Gaming Problem: Teams can hit DORA targets while developers are miserable
- 2024 finding: AI improves individual metrics but 1.5% reduction in delivery performance, 7.2% decrease in stability

**Transition**: "DORA tells you how fast your pipeline is. It doesn't tell you if your developers are burning out running it."

### ACT 3: THE SPACE FRAMEWORK (3-4 min)
**Purpose**: Introduce the multi-dimensional approach

**Key Points**:
- Developed 2021 by Microsoft Research, GitHub, University of Victoria
- Created by Dr. Nicole Forsgren (same researcher behind DORA)
- The Five Dimensions (SPACE acronym):
  1. **Satisfaction and well-being**: Happiness, fulfillment, burnout levels
  2. **Performance**: Quality of code, reliability, customer impact
  3. **Activity**: Volume of work (commits, PRs, deployments)
  4. **Communication and collaboration**: Team dynamics, code review quality
  5. **Efficiency and flow**: Minimal interruptions, unblocked work

**Key Recommendation**: Track at least 3 metrics across different dimensions, include at least one perceptual measure (surveys)

**The Name Change**: Microsoft/GitHub renamed "Developer Velocity Lab" to "Developer Experience Lab" - signal that experience > speed

### ACT 4: DEVEX AND DX CORE 4 (3-4 min)
**Purpose**: Show the latest evolution in metrics frameworks

**DevEx Framework (2023)**:
- Three core dimensions:
  1. **Feedback Loops**: How quickly developers get information on their work
  2. **Cognitive Load**: Mental effort required to complete tasks
  3. **Flow State**: Ability to focus deeply without interruptions
- Focus on *lived experience* and *points of friction*

**DX Core 4 (Latest)**:
- Unified framework encapsulating DORA, SPACE, and DevEx
- Four dimensions:
  1. **Speed**: Diffs per engineer, lead time, deployment frequency
  2. **Effectiveness**: Developer Experience Index (DXI), regrettable attrition, time to 10th PR
  3. **Quality**: Change failure rate, recovery time, perceived quality
  4. **Impact**: % time on new capabilities, initiative progress, ROI

**Key Metrics**:
- DXI: 14-question research-backed survey (proprietary to DX)
- Diffs per engineer: Controversial but useful with guardrails
- Time to 10th PR: Measures onboarding effectiveness
- Regrettable attrition: Developer retention signal

**Results**: 3-12% increases in engineering efficiency, 14% more time on feature development

### ACT 5: PRACTICAL IMPLEMENTATION (3-4 min)
**Purpose**: Give actionable guidance for platform teams

**Framework Selection**:
- **Just starting?** → DORA (well-understood, tool support)
- **Have DORA, want more?** → Add SPACE dimensions
- **Mature org with resources?** → Consider DX Core 4

**Implementation Approach**:
1. Start with DORA as baseline (deployment frequency, lead time)
2. Add developer satisfaction survey (quarterly)
3. Measure cognitive load indicators (context switching, interrupts)
4. Track flow state (deep work hours, meeting load)

**Avoid These Mistakes**:
- Gamification: Don't tie metrics to individual performance reviews
- Cherry-picking: Don't only measure what looks good
- Survey fatigue: Quarterly surveys max, keep them short
- Ignoring qualitative: Numbers without context mislead

**Platform Engineering Angle**:
- Golden paths reduce cognitive load
- Self-service reduces feedback loop time
- Abstractions enable flow state
- Internal Developer Portals measurably improve all dimensions

**Closing Insight**: "The best metric is the one that changes behavior for the better. DORA changed how we think about delivery. SPACE, DevEx, and DX Core 4 are changing how we think about the people doing the delivering."

## News Segment (December 6, 2025)

1. **Iterate.ai AgentOne for Enterprise AI Code Security**
   - First enterprise-grade solution to sandbox and audit AI agent activity
   - Addresses #1 concern: AI coding assistants + data leaks/compliance
   - https://thenewstack.io/iterate-ai-launches-agentone-for-enterprise-ai-code-security/

2. **AWS Durable Functions for Lambda**
   - Stateful logic directly in Lambda code
   - Manages state and retry logic without incurring wait costs
   - https://www.infoq.com/news/2025/12/aws-lambda-durable-functions/

3. **Capital One Cut Tracing Data by 70% with OpenTelemetry**
   - Squeezing more value from telemetry
   - Real enterprise OTel optimization story
   - https://thenewstack.io/how-capital-one-cut-tracing-data-by-70-with-opentelemetry/

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| DORA survey respondents (2024) | 39,000+ professionals | Google Cloud State of DevOps 2024 |
| AI tool usage | 75%+ use daily | DORA 2024 Report |
| Elite performer change failure rate | ~5% | DORA 2024 Report |
| Low performer change failure rate | ~40% | DORA 2024 Report |
| Elite lead time | <1 day | DORA 2024 Report |
| Low performer lead time | >1 month | DORA 2024 Report |
| AI impact on delivery stability | -7.2% | DORA 2024 Report |
| DX Core 4 efficiency improvement | 3-12% | DX research (300+ orgs) |
| Time on feature development increase | 14% | DX Core 4 implementations |
| DORA framework debut | 2018 | DevOps Research and Assessment |
| SPACE framework debut | 2021 | Microsoft Research/GitHub |
| DevEx framework debut | 2023 | Forsgren, Storey, Maddila |

## Sources

- [DORA Metrics Guide - Octopus](https://octopus.com/devops/metrics/dora-metrics/)
- [DORA Report 2025 Key Takeaways - Faros AI](https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025)
- [DORA Report 2024 Analysis - RedMonk](https://redmonk.com/rstephens/2024/11/26/dora2024/)
- [SPACE Framework - LinearB](https://linearb.io/blog/space-framework)
- [SPACE Paper - ACM Queue](https://queue.acm.org/detail.cfm?id=3454124)
- [DX Core 4 - GetDX](https://getdx.com/research/measuring-developer-productivity-with-the-dx-core-4/)
- [DX Core 4 Deep Dive - LinearB](https://linearb.io/blog/dx-core-4-deep-dive)
- [Framework Comparison - Lothar Schulz](https://www.lotharschulz.info/2025/05/04/engineering-metrics-frameworks-dora-devex-space-dx-core-4-essp-comparison/)
- [How to Measure AI Developer Productivity - Nicole Forsgren/Lenny's Newsletter](https://www.lennysnewsletter.com/p/how-to-measure-ai-developer-productivity)

## Technical Accuracy Notes

- DORA originated from Puppet Labs State of DevOps reports, now owned by Google Cloud
- Dr. Nicole Forsgren is common thread: co-authored DORA research, SPACE framework, DevEx
- 2024 DORA report introduced 7 archetypes replacing traditional performance tiers
- MTTR renamed to "Failed Deployment Recovery Time" (FDRT) for specificity
- DXI (Developer Experience Index) is proprietary to DX company - acknowledge this
