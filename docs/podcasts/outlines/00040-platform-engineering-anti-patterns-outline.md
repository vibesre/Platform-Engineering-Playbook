# Episode Outline: Platform Engineering Anti-Patterns

## Story Planning

**NARRATIVE STRUCTURE**: Contrarian Take
**CENTRAL TENSION**: DORA 2024 found platform teams actually *decreased* throughput by 8% and stability by 14% - if platform engineering is supposed to help, why is it making things worse for so many organizations?
**THROUGHLINE**: From believing "we need a platform" to understanding that HOW you build it determines whether it accelerates or destroys productivity.
**EMOTIONAL ARC**:
- Recognition: "Wait, our platform has this problem"
- Surprise: "The DORA data shows platforms can make things WORSE"
- Empowerment: "Now I can audit our platform and fix these patterns"

## Act Structure

### ACT 1: SETUP (2-3 min)
- **Hook**: DORA 2024 bombshell - organizations with platform teams saw throughput DECREASE 8%, stability DECREASE 14%. Meanwhile Gartner says 80% of orgs will have platform teams by 2026.
- **Stakes**: 69% of developers lose 8+ hours per week to inefficiencies. That's ~$17M annually for a 1,000-dev org.
- **Promise**: We'll reveal the 10 anti-patterns sabotaging platform initiatives and what successful teams like Spotify and Zalando do differently.

**Key Points**:
1. DORA 2024: -8% throughput, -14% stability with platform teams (Google Cloud)
2. 69% developers lose 8+ hours/week to inefficiencies (Atlassian DX Report 2024)
3. 35% of orgs still using spreadsheets as their "developer portal" (Port.io 2024)

### ACT 2: EXPLORATION (6-8 min)

#### Discovery 1: Organizational Anti-Patterns (2-3 min)
- **Ticket Ops**: Developers wait 1+ weeks for infrastructure. Creates artificial bottlenecks.
- **Ivory Tower Platform**: Teams disconnected from developer reality. Create standards no one follows.
- **Platform as Bucket**: Everything gets dumped into platform scope. Manuel Pais quote about "lack of ownership, lack of focus, a lot of waste."
- **Mandatory Adoption**: Forces usage, closes feedback loops, hides resistance.

**Key Points**:
1. "Ticket ops is draining your organization" - Humanitec
2. Manuel Pais (Team Topologies): "Platform becomes a bucket for everything, just becomes a huge mess"
3. Mid-sized tech firm case study: Mandatory IDP led to rollback to legacy systems

#### Discovery 2: Technical Anti-Patterns (2-3 min)
- **Golden Cage**: Over-standardization blocks productivity. One-size-fits-all templates.
- **Over-Engineered Monolith**: Complexity creates more toil than it reduces.
- **Front-End First**: Beautiful portal, manual processes underneath. 35% still use spreadsheets.
- **Day 1 Obsession**: Optimize app creation but neglect Day 2-50 operations.

**Key Points**:
1. "Golden Cage results when platforms are designed with too many constraints" - Octopus Deploy
2. Jay Jenkins (Akamai): "Complexity is the enemy. If platform engineering is creating more toil, something is off"
3. "Application creation is below 1% of time invested" - Octopus Deploy

#### Discovery 3: Strategic Anti-Patterns (2 min)
- **Build It and They Will Come**: No adoption strategy. Erica Hughberg: "Even the best products don't sell themselves."
- **Biggest Bang Trap**: Starting with hardest use case. Platform team loses confidence, trust erodes.

**Key Points**:
1. Firms monitoring adoption closely report 30% higher ROI (Google Cloud)
2. Syntasso: Start small, build confidence, expand proven wins

#### Complication: The J-Curve Effect
- DORA explains the productivity decrease as typical of transformational efforts
- Initial productivity hit before long-term gains
- But only if you avoid these anti-patterns

### ACT 3: RESOLUTION (3-4 min)

- **Synthesis**: The difference between platform success and failure isn't budget or talent - it's avoiding these 10 traps. Every anti-pattern has a counter-strategy.

- **Application - What Successful Teams Do**:
  1. **Treat platform as product**: Developer is the customer, measure satisfaction not just adoption
  2. **Practice architect elevator**: Move between strategy and implementation, hands-on pair programming
  3. **Stable priorities**: DORA found 40% less burnout with stable priorities
  4. **Self-service with guardrails**: Not gatekeepers - Zalando's "you build it, you run it"
  5. **Start small, expand proven wins**: Not biggest bang approach

- **Empowerment**: Audit your platform against these 10 anti-patterns:
  - Developers waiting more than 1 day for standard requests? (Ticket Ops)
  - Platform team hasn't pair-programmed with devs this quarter? (Ivory Tower)
  - Scope grown 3x in the last year? (Platform as Bucket)
  - One-size-fits-all with no extension points? (Golden Cage)
  - Beautiful portal but manual processes? (Front-End First)

- **Callback to Hook**: The 84% failure rate isn't inevitable. Spotify and Zalando didn't succeed because they had bigger budgets - they succeeded because they avoided these traps.

**Key Points**:
1. Spotify: Backstage users are 2.3x more active on GitHub
2. Zalando: "One of the first steps was cultural, not technical"
3. DORA: Teams with stable priorities face 40% less burnout

## Story Elements

**KEY CALLBACKS**:
- DORA 8%/14% stat returns in resolution: "This is WHY those numbers happen"
- Platform as product theme threads through
- Audit checklist mirrors opening statistics

**NARRATIVE TECHNIQUES**:
1. **Anchoring Statistic**: DORA 8%/14% decrease - return to it when explaining why
2. **Case Study Arc**: Spotify Backstage and Zalando Sunrise as success stories
3. **Devil's Advocate**: Jordan presents anti-patterns, Alex provides counter-strategies

**SUPPORTING DATA**:
- DORA 2024: 8% throughput decrease, 14% stability decrease (Google Cloud)
- Atlassian DX Report 2024: 69% lose 8+ hours/week
- Port.io 2024: 35% use spreadsheets as portal
- Humanitec: "Ticket ops is draining your organization"
- Manuel Pais (Team Topologies): Platform as bucket quote
- Jay Jenkins (Akamai): "Complexity is the enemy"
- Octopus Deploy: Golden Cage definition, Day 1 under 1% of time
- Erica Hughberg (KubeCon 2024): Products don't sell themselves
- Spotify Engineering: 2.3x GitHub activity for Backstage users
- Zalando Engineering: Cultural change first

## Quality Checklist

- [x] Throughline clear: "HOW you build determines success vs failure"
- [x] Hook compelling: DORA data showing platforms making things WORSE
- [x] Sections build momentum: Org → Technical → Strategic → Resolution
- [x] Insights connect: All tie back to "this is why the numbers are bad"
- [x] Emotional beats: Recognition (have this problem), Surprise (DORA data), Empowerment (audit checklist)
- [x] Callbacks create unity: DORA stats, platform as product, audit checklist
- [x] Payoff satisfies: Concrete audit checklist and success patterns
- [x] Narrative rhythm: Contrarian take with evidence, not just listing anti-patterns
- [x] Technical depth appropriate: Organizational/strategy topic with concrete examples
- [x] Listener value clear: Can audit their platform against 10 anti-patterns

## Sources

1. Google Cloud - DORA Report 2024
2. Atlassian - Developer Experience Report 2024
3. Port.io - 2024 State of Internal Developer Portal Report
4. Humanitec - Eliminate Ticket Ops
5. Team Topologies - Matthew Skelton & Manuel Pais
6. Octopus Deploy - Platform Engineering Patterns and Anti-patterns
7. InfoWorld - 8 Platform Engineering Anti-Patterns
8. Spotify Engineering Blog
9. Zalando Engineering Blog
10. Syntasso - Platform Building Antipatterns
