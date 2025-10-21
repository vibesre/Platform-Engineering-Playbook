---
name: Podcast Outline
description: Create compelling story outlines for podcast episodes using proven narrative structures. MANDATORY before writing any podcast script.
allowed-tools: Read, Write
---

# Podcast Outline

Create a narrative outline using storytelling frameworks before writing dialogue. **CRITICAL**: Scripts without outlines become lists of facts instead of compelling stories.

## When to Use This Skill

Use this skill when:
- User says: "Create podcast outline", "Plan episode story"
- Before writing any podcast script (mandatory workflow step)
- User has research/topic brief and needs to structure the narrative

**NEVER write a script without completing an outline first.**

## Core Principle

> **Technical content without narrative structure = list of facts**
>
> **Technical content WITH narrative structure = compelling story that teaches**

Great podcasts teach through stories, not bullet points.

## Phase 1: Story Planning (MANDATORY)

Before writing ANY dialogue, answer these questions:

### 1. What's the Central Tension?
- What problem/dilemma does the listener care about?
- What's at stake? (Money, time, career, team effectiveness)
- What makes this urgent NOW?

### 2. What's the Journey?
- Where are we starting? (Current state, common belief)
- What discoveries do we make along the way?
- Where do we end up? (New understanding, decision framework)

### 3. What's the Emotional Arc?
- **Start**: Recognition ("I've seen this problem")
- **Middle**: Discovery/Surprise ("Wait, THAT's why?")
- **End**: Empowerment ("Now I know what to do")

### 4. What's the Throughline?
One sentence that captures the episode's narrative journey:

**Examples**:
- "From thinking PaaS is 'too expensive' to understanding the real cost equation"
- "From drowning in AI governance to discovering the counterintuitive approach that actually works"

## Storytelling Templates

Choose ONE narrative structure:

### 1. The Mystery/Discovery Structure
Best for: Technical deep-dives, comparing technologies

```
Hook: Present a puzzling situation or surprising fact
Investigation: Explore the evidence, test assumptions
Revelation: Uncover the real explanation
Application: How to use this insight
```

**Example Outline**:
- Hook: "Everyone says Kubernetes is overkill for small teams, but companies with 5 engineers are adopting it. Why?"
- Investigation: Look at what problems they're actually solving
- Revelation: It's not about scale, it's about standardization and hiring
- Application: Decision framework based on team composition, not size

### 2. The Before/After Transformation
Best for: Platform engineering practices, organizational change

```
Before State: Common approach/belief and its problems
Catalyst: What forces change (incident, cost, growth)
Journey: What the transition looks like in practice
After State: New reality and specific outcomes
```

**Example Outline**:
- Before: Manual deployments, hero culture, knowledge silos
- Catalyst: Key engineer leaves, 3-day outage from tribal knowledge
- Journey: Painful process of documentation, automation, standardization
- After: 10x deployment frequency, reduced MTTR, team can take vacations

### 3. The Economic Detective Story
Best for: PaaS comparisons, build vs buy decisions

```
Apparent Cost: Surface-level pricing comparison
Hidden Costs: Uncover what's not on the pricing page
Real Calculation: Build complete TCO model
Surprising Conclusion: Often opposite of initial assumption
```

**Example Outline**:
- Apparent: "$397/month vs free AWS? That's crazy expensive"
- Hidden: Engineering time, on-call burden, opportunity cost
- Real Calculation: $397 vs $15K/month in team time
- Surprising: The "expensive" option saves $175K/year

### 4. The Skills Evolution Arc
Best for: Career guidance, team building, technology trends

```
What Was Essential: Technologies/skills that mattered 2-3 years ago
What Changed: Market shift, technology maturation, new problems
What's Emerging: Skills gaining importance now
Strategic Positioning: How to adapt your learning/hiring
```

**Example Outline**:
- Was: Deep Kubernetes expertise, custom observability stacks
- Changed: Managed services matured, AI workloads emerged
- Emerging: AI platform engineering, cost optimization, security automation
- Strategy: Upskill existing team vs hire specialists vs partner/buy

### 5. The Contrarian Take
Best for: Challenging assumptions, nuanced comparisons

```
Conventional Wisdom: What "everyone knows" to be true
Counter-Evidence: Data/stories that don't fit the narrative
Alternative Explanation: A different way to see the problem
When Each Applies: Framework for context-specific truth
```

**Example Outline**:
- Conventional: "Microservices are the modern way to build systems"
- Counter: 90% of startups would ship faster with a monolith
- Alternative: Architecture should match team structure and maturity
- Framework: Monolith until X team size/complexity, then split strategically

## Narrative Techniques

### 1. The Anchoring Statistic
- Open with a number that challenges assumptions
- Return to it throughout the episode
- Example: "85% of organizations have shadow AI" → becomes recurring theme

### 2. The Case Study Arc
- Introduce a real company's situation (anonymized if needed)
- Follow their decision-making process
- Reveal outcomes (good and bad)
- Extract lessons

### 3. The Thought Experiment
- "Let's design X from first principles"
- Walk through decision points
- Compare to actual market solutions
- Discover why things evolved the way they did

### 4. The Historical Context Pattern
- "Five years ago, we solved this with X"
- "That worked until Y changed"
- "Now we're seeing Z emerge"
- Creates perspective and anticipates future

### 5. The Devil's Advocate Dance
- One speaker presents best case
- Other speaker pokes holes
- First speaker concedes/refines
- Builds nuanced understanding through respectful disagreement

## Episode Outline Template

Use this template for every episode:

```markdown
# Episode Outline: [Working Title]

## Story Planning

**NARRATIVE STRUCTURE**: [Mystery/Before-After/Economic Detective/Skills Evolution/Contrarian]

**CENTRAL TENSION**: [What problem/dilemma?]

**THROUGHLINE**: [One-sentence journey]

**EMOTIONAL ARC**:
- Recognition moment: [Where listener thinks "I've been there"]
- Surprise moment: [Where listener thinks "Wait, really?"]
- Empowerment moment: [Where listener thinks "Now I know what to do"]

## Act Structure

### ACT 1: SETUP (2-3 minutes)
- **Hook**: [Surprising fact, compelling question, or relatable problem]
- **Stakes**: [Why this matters to the listener NOW]
- **Promise**: [What we'll discover/resolve by the end]

**Key Points**:
- [Point 1 with supporting data/example]
- [Point 2 with supporting data/example]

### ACT 2: EXPLORATION (5-7 minutes)
- **Discovery 1**: [First key insight with supporting evidence]
- **Discovery 2**: [Second key insight, builds on first]
- **Discovery 3**: [Third insight, often counterintuitive]
- **Complication**: [Where it gets interesting/nuanced]

**Key Points**:
- [Point 1 with supporting data/example]
- [Point 2 with supporting data/example]
- [Point 3 with supporting data/example]

### ACT 3: RESOLUTION (3-4 minutes)
- **Synthesis**: [How insights connect into framework]
- **Application**: [Practical decision-making guidance]
- **Empowerment**: [What listener can do with this]

**Key Points**:
- [Point 1 with supporting data/example]
- [Point 2 with supporting data/example]

## Story Elements

**KEY CALLBACKS**:
- [Concept from Act 1 that we return to in Act 3]
- [Running theme that unifies disparate facts]

**NARRATIVE TECHNIQUES**:
- [Which techniques from above will we use?]

**SUPPORTING DATA**:
- [Statistic with source]
- [Case study with specific numbers]
- [Expert quote with attribution]

## Quality Checklist

Before approving this outline:
- [ ] Throughline is clear (can state journey in one sentence)
- [ ] Hook is compelling (would listener keep listening after 60 seconds?)
- [ ] Each section builds (creates momentum toward resolution)
- [ ] Insights connect (discoveries build on each other vs random facts)
- [ ] Emotional beats land (2-3 moments of recognition/surprise/empowerment)
- [ ] Callbacks create unity (return to opening themes/questions)
- [ ] Payoff satisfies (ending delivers on opening promise)
- [ ] Narrative rhythm (feels like a story, not a bulleted list)
- [ ] Technical depth maintained (story serves the learning, not replaces it)
- [ ] Listener value clear (what can they DO differently after listening?)
```

## Anti-Patterns to Avoid

### ❌ The Encyclopedia Entry
**Problem**: Just listing facts about technology without narrative

**Fix**: Use "mystery" or "economic detective" structure

### ❌ The Feature Tour
**Problem**: Walking through features without connecting to real problems

**Fix**: Use "before/after transformation" with actual pain points

### ❌ The Meandering Discussion
**Problem**: Topics connected only by being related to same technology

**Fix**: Establish throughline and cut anything that doesn't advance it

### ❌ The False Debate
**Problem**: Creating artificial controversy for engagement

**Fix**: Use "contrarian take" only when genuinely nuanced

### ❌ The Abandoned Setup
**Problem**: Opening with compelling question that never gets answered

**Fix**: Outline Act 3 resolution before writing Act 1 hook

## Example: Transforming Facts Into Story

### ❌ BEFORE (List of Facts)
```
- PaaS platforms are getting popular
- Flightcontrol is $397/month
- Vercel is $20/month for Pro
- Railway has pay-as-you-go
- [15 minutes of pricing details]
```

### ✅ AFTER (Economic Detective Structure)
```
ACT 1: SETUP
Hook: "A developer asked me: 'How can anyone justify $397/month for Flightcontrol when AWS is free?' It's a fair question. Until you do the actual math."

Stakes: Platform teams spend 30-40% of time on infrastructure vs product features

Promise: We'll uncover the real cost equation that pricing pages hide

ACT 2: EXPLORATION
Discovery 1: The "free" AWS setup requires 20+ hours/month of engineer time
Discovery 2: At $150/hour loaded cost, that's $3,000/month in hidden costs
Discovery 3: Opportunity cost: those hours could ship features worth $$$
Complication: But not all teams have the same equation...

ACT 3: RESOLUTION
Synthesis: Real cost = Platform fee + (Engineer hours × loaded cost) + opportunity cost
Application: Decision framework based on team size, complexity, feature velocity
Empowerment: Spreadsheet approach to justify platform decisions to leadership
```

## Output Format

Save the outline to: `docs/podcasts/outlines/00XXX-episode-name-outline.md`

The outline must be approved before moving to script writing.

---

## Instructions for Claude

When this skill is invoked:

1. **Ask clarifying questions** if topic isn't clear:
   - What's the main topic?
   - What research/data do we have?
   - What should listeners learn?

2. **Choose narrative structure** based on topic:
   - Comparison → Mystery or Economic Detective
   - Practice change → Before/After Transformation
   - Career/skills → Skills Evolution Arc
   - Challenge assumption → Contrarian Take

3. **Define story elements FIRST**:
   - Central tension
   - Throughline (one sentence)
   - Emotional beats

4. **Complete the outline template** with:
   - Act 1/2/3 structure
   - Key points with supporting data
   - Callbacks and narrative techniques

5. **Validate against quality checklist** (all 10 items)

6. **Save outline** to docs/podcasts/outlines/

7. **Present outline to user** and ask: "Does this story arc work? Should I adjust anything before writing the script?"

**NEVER proceed to script writing without an approved outline.**

The outline is your story architecture. Dialogue is just execution. You can't build a compelling episode without first designing the narrative structure.
