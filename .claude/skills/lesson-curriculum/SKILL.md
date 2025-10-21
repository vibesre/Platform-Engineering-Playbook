---
name: Lesson Curriculum
description: Design comprehensive multi-episode course curricula using learning science principles (spaced repetition, active recall, progressive complexity) based on research findings.
allowed-tools: Read, Write, Glob
---

# Lesson Curriculum

Design comprehensive, evidence-based course curricula that maximize learning retention and skill development using proven pedagogical principles.

## When to Use This Skill

Use this skill when:
- User says: "Create curriculum for [topic]", "Design course structure"
- A Course Research Brief exists (from lesson-research skill)
- Ready to plan multi-episode course with learning science principles
- Need to create the course index page

**Prerequisites**: Course Research Brief must exist (use lesson-research skill first).

## Core Pedagogical Principles

### 1. Spaced Repetition
**Principle**: Information reviewed at increasing intervals is retained 2-3x better than massed learning.

**Application**:
- Key concepts introduced in Episode N, reinforced in N+3, N+6
- Dedicated review episodes every 3-4 lessons
- "Spiral curriculum": Return to topics with increasing depth
- Callbacks in every episode: "Remember when we covered X?"

**Example**:
```
Episode 1: Introduce mental model
Episode 2: Apply mental model to Concept A
Episode 4: Callback to mental model while teaching Concept B
Episode 7: Review mental model + all applications
Episode 10: Advanced application requires deep mental model understanding
```

### 2. Active Recall
**Principle**: Retrieving information strengthens memory more than passive review.

**Application**:
- "Before we continue, what was the purpose of X?" prompts
- "Pause and try this yourself" moments
- Start episodes with retrieval: "Last time we covered..."
- Recap sections require mental reconstruction
- Practice prompts before showing solutions

**Example Script Moments**:
```
"Before I show you the solution, pause and think:
How would YOU structure these labels?
What problems might you encounter?"

[Pause in audio]

"Here's what I'd recommend..."
```

### 3. Progressive Complexity (Scaffolding)
**Principle**: Build from simple to complex, each step achievable with current knowledge + small stretch.

**Application**:
- Episode 1: Simplest mental model
- Episodes 2-N: Add one new concept per episode
- Each episode assumes ONLY previous episodes
- Advanced topics come after foundations are solid

**Complexity Progression**:
```
Simple → Concrete → Abstract → Complex

Episode 1: Mental model (simple)
Episode 2: Single concrete example (concrete)
Episode 3: Multiple examples (concrete)
Episode 4: Pattern recognition (abstract)
Episode 5: Edge cases and variations (complex)
```

### 4. Chunking
**Principle**: Working memory holds 5-9 items; group related information into meaningful chunks.

**Application**:
- One core concept per episode (not 3-4)
- 10-15 minute episodes (cognitive load management)
- Break complex topics into 2-3 episodes
- Group related episodes into "modules"

**Example**:
```
BAD: Episode 3 - "Pods, Deployments, Services, and ConfigMaps"
GOOD:
  Episode 3 - "Pods: The Atomic Unit"
  Episode 4 - "Deployments: Managing Pod Lifecycles"
  Episode 5 - "Services: Networking Pods"
  Episode 6 - "ConfigMaps: External Configuration"
```

### 5. Interleaving
**Principle**: Mixing related topics improves discrimination and long-term retention.

**Application**:
- Don't teach all of Topic A, then all of Topic B
- Alternate between related concepts
- Return to earlier topics with new context
- Compare and contrast throughout

**Example**:
```
BLOCKED (worse retention):
Episodes 1-3: All about Prometheus metrics
Episodes 4-6: All about Grafana dashboards

INTERLEAVED (better retention):
Episode 1: Prometheus metrics basics
Episode 2: Grafana visualization basics
Episode 3: Advanced Prometheus metrics
Episode 4: Advanced Grafana dashboards
Episode 5: Metrics + Dashboards integration
```

### 6. Elaborative Rehearsal
**Principle**: Connecting new information to existing knowledge creates stronger memories.

**Application**:
- Analogies to familiar concepts
- Multiple examples showing same principle
- Different contexts for same concept
- "This is like when..." connections

**Example Script**:
```
"Think of Kubernetes Pods like shipping containers.
Just as containers standardize cargo transport,
Pods standardize application deployment.

In other words, Pods are the 'unit of deployment'
the same way containers are the 'unit of shipping.'

To put it another way, when you tell Kubernetes 'run this,'
you're always talking about Pods, never individual processes."
```

### 7. Dual Coding
**Principle**: Information encoded both verbally and visually is retained better.

**Application**:
- Audio narration (verbal)
- Written transcript (verbal + visual)
- Code examples in transcript (visual)
- Diagrams in course page (visual)

## Course Structure Templates

### Template 1: Fundamentals Course (8-12 episodes)

**Target**: Build solid foundation in core technology

```
MODULE 1: FOUNDATIONS (2-3 episodes)
├─ Episode 1: Mental Model & First Principles
│  - Why does this exist?
│  - Core abstraction/metaphor
│  - High-level architecture
│
├─ Episode 2: Essential Concepts & Terminology
│  - Key vocabulary
│  - Basic operations
│  - Simple example
│
└─ Episode 3: Hands-On Fundamentals
   - Practical walkthrough
   - Common patterns
   - First "aha!" moment

MODULE 2: CORE TOPICS (4-6 episodes)
├─ Episode 4-N: Individual Core Concepts
│  - One concept per episode
│  - Progressive complexity
│  - Real-world examples
│  - Common pitfalls
│
└─ Episode N: Review & Integration
   - Active recall of all concepts
   - How concepts connect
   - Common troubleshooting

MODULE 3: PRODUCTION READINESS (2-3 episodes)
├─ Episode N+1: Advanced Patterns
│  - Production-grade configurations
│  - Performance optimization
│  - Security considerations
│
└─ Episode N+2: Mastery & Next Steps
   - Integration with ecosystem
   - Career-level understanding
   - Further learning paths
```

### Template 2: Deep Dive Course (5-8 episodes)

**Target**: Master specific aspect of technology

```
Episode 1: Problem Space & Context
- What problem are we solving?
- Why existing solutions fall short
- Where this fits in the ecosystem

Episodes 2-N-1: Progressive Exploration
- Start with simplest use case
- Add complexity incrementally
- Real-world scenarios
- Troubleshooting strategies

Episode N: Mastery & Integration
- Advanced techniques
- Production lessons learned
- Decision frameworks
- Expert-level understanding
```

### Template 3: Comprehensive Course (15-20 episodes)

**Target**: Complete mastery from basics to advanced

```
MODULE 1: FOUNDATIONS (3 episodes)
MODULE 2: CORE CONCEPTS (5-7 episodes)
MODULE 3: REVIEW & INTEGRATION (1 episode)
MODULE 4: ADVANCED TOPICS (4-6 episodes)
MODULE 5: PRODUCTION MASTERY (2-3 episodes)
```

## Review Episode Design

**Every 3-4 episodes, include a review episode:**

### Review Episode Structure (15 min)

**Active Recall Phase (5 min)**:
```
"Before we continue, let's test your retention.
I'll ask questions - pause and answer before I do.

Question 1: What's the core mental model for [X]?
[Pause]
Answer: [Provide answer]

Question 2: When would you use [Y] vs [Z]?
[Pause]
Answer: [Provide answer]

[Continue for 3-5 key concepts]
```

**Integration Phase (5 min)**:
```
"Now let's see how everything connects.

We learned [Concept A] in Episode X.
Then [Concept B] in Episode Y.
How do they work together?

[Explain integration with examples]
```

**Troubleshooting Phase (3 min)**:
```
"Common issues you might encounter:

Problem 1: [Specific scenario]
Why it happens: [Root cause]
How to fix: [Solution]

[Cover 2-3 common problems]
```

**Preview Phase (2 min)**:
```
"Looking ahead:
- Next episode: [Topic]
- After that: [Topic]
- Building toward: [Goal]
```

## Curriculum Document Structure

### Internal Planning Document

**Location**: `docs/podcasts/courses/[course-slug]/curriculum-plan.md` (not published)

```markdown
# [Course Name] - Curriculum Plan

## Course Overview
**Target Audience**: Senior platform engineers (5+ years)
**Prerequisites**: [List required knowledge]
**Total Duration**: [N episodes, ~X hours]
**Learning Outcomes**:
- [Specific skill 1]
- [Specific skill 2]
- [Specific skill 3]

## Pedagogical Approach
- **Spaced Repetition**: [How applied]
- **Active Recall**: [How applied]
- **Progressive Complexity**: [How structured]
- **Interleaving**: [How mixed]

## Episode Breakdown

### MODULE 1: [Name] (Episodes 1-X)

#### Episode 1: [Title]
**Duration**: 15 min
**Learning Objectives**:
- [Specific, measurable objective 1]
- [Specific, measurable objective 2]

**Covers**:
- [Topic 1]
- [Topic 2]

**Spaced Repetition**:
- Introduces: [Concepts that will be repeated]
- Reinforces: [None - first episode]

**Active Recall Moments**:
- [Specific prompt]

**Prerequisites**: [What learner needs before this]
**Leads to**: Episode 2, 3

---

#### Episode 2: [Title]
**Duration**: 15 min
**Learning Objectives**:
- [Specific, measurable objective 1]
- [Specific, measurable objective 2]

**Covers**:
- [Topic 1]
- [Topic 2]

**Spaced Repetition**:
- Introduces: [New concepts]
- Reinforces: [Concepts from Episode 1]

**Active Recall Moments**:
- "Remember from Episode 1: [concept]?"
- [Specific retrieval prompt]

**Prerequisites**: Episode 1
**Leads to**: Episode 4, 5

---

[Continue for all episodes]

## Spaced Repetition Map

```
Mental Model (Ep 1)
├─ Referenced: Ep 2, Ep 4, Ep 7, Ep 10
├─ Deepened: Ep 4, Ep 10
└─ Mastered: Ep 10

Core Concept A (Ep 2)
├─ Referenced: Ep 3, Ep 5, Ep 7
├─ Deepened: Ep 5, Ep 8
└─ Mastered: Ep 8

[Map all key concepts]
```

## Concept Dependency Graph

```
Episode 1 (Mental Model)
├─┬─> Episode 2 (Concept A) ───┬─> Episode 5 (Integration A+B)
│ └─> Episode 3 (Concept B) ───┘
│
└───> Episode 4 (Concept C) ─────> Episode 6 (Advanced C)
                                    │
                                    └─> Episode 7 (Review)
```

## Learning Checkpoints

After Episode 3:
- [ ] Can explain mental model in own words
- [ ] Can identify when to use Concept A vs B
- [ ] Can perform basic operations

After Episode 7:
- [ ] Can integrate Concepts A, B, C
- [ ] Can troubleshoot common issues
- [ ] Can explain trade-offs

After Final Episode:
- [ ] Can design production-ready solutions
- [ ] Can debug complex problems
- [ ] Can teach concepts to others
```

## Course Index Page

**Location**: `docs/podcasts/courses/[course-slug]/index.md`

**Template**:

```markdown
---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 [Course Name]"
slug: courses/[course-slug]
---

# [Course Name]

## Platform Engineering Playbook Course

<GitHubButtons />

**Presenter**: [Fictional persona name]
**Total Duration**: [N episodes, ~X hours total]
**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience
**Difficulty**: [Fundamentals/Intermediate/Advanced]

## Course Overview

[2-3 paragraph description of what the course covers and why it matters]

### What You'll Learn

By the end of this course, you'll be able to:
- [Specific, measurable outcome 1]
- [Specific, measurable outcome 2]
- [Specific, measurable outcome 3]
- [Specific, measurable outcome 4]
- [Specific, measurable outcome 5]

### Prerequisites

Before starting this course, you should have:
- [Prerequisite 1 with link if we have content]
- [Prerequisite 2]
- [Prerequisite 3]

### Time Commitment

- **Total Duration**: ~[X hours] ([N episodes × 15 min average])
- **Recommended Pace**: 2-3 episodes per week
- **Completion Time**: [Y weeks] at recommended pace

---

## Course Curriculum

### Module 1: [Module Name] (Episodes 1-X)

[Brief description of module focus]

#### 📖 Episode 1: [Title]
**Duration**: [X min] • [📝 Transcript](/podcasts/courses/[course-slug]/lesson-01)

Learn about:
- [Key point 1]
- [Key point 2]
- [Key point 3]

---

#### 📖 Episode 2: [Title]
**Duration**: [X min] • [📝 Transcript](/podcasts/courses/[course-slug]/lesson-02)

Learn about:
- [Key point 1]
- [Key point 2]

---

[Continue for all episodes in module]

### Module 2: [Module Name] (Episodes X-Y)

[Brief description]

[Episodes listed same as Module 1]

---

### Module 3: [Module Name] (Episodes Y-N)

[Brief description]

[Episodes listed same as Module 1]

---

## Learning Resources

For deeper exploration, see our [comprehensive [Technology] guide](/technical/[topic]).

### Official Documentation
- [Link 1] - [Description]
- [Link 2] - [Description]

### Recommended Follow-Up
- [Related course or content]
- [Advanced topics]

---

## About This Course

This course uses evidence-based learning techniques:
- **Spaced Repetition**: Key concepts reviewed across multiple episodes
- **Active Recall**: Retrieval prompts to strengthen retention
- **Progressive Complexity**: Each lesson builds on previous knowledge
- **Real-World Focus**: Production scenarios and troubleshooting

---

**Questions or feedback?** This course is open source. Contribute via [GitHub](https://github.com/[repo]).
```

## Output Format

When curriculum is complete, produce:

### 1. Internal Curriculum Plan
**File**: `docs/podcasts/courses/[course-slug]/curriculum-plan.md`
- Complete episode breakdown
- Spaced repetition map
- Dependency graph
- Learning checkpoints

### 2. Course Index Page
**File**: `docs/podcasts/courses/[course-slug]/index.md`
- Published page visible to users
- Module structure with episode links
- Learning outcomes
- Prerequisites

### 3. Curriculum Report (for user review)
```markdown
# Curriculum Design Complete: [Course Name]

## Summary
- **Total Episodes**: N
- **Modules**: X
- **Total Duration**: ~Y hours
- **Review Episodes**: Z

## Pedagogical Features
✅ Spaced repetition: [X concepts repeated across Y episodes]
✅ Active recall: [Prompts in every episode]
✅ Progressive complexity: [Simple → Advanced clear path]
✅ Review episodes: [Every 3-4 lessons]
✅ Interleaving: [Related concepts mixed strategically]

## Episode Structure
[Table showing all episodes with objectives]

## Next Steps
1. Review curriculum structure
2. Approve course index page
3. Begin with lesson-outline skill for Episode 1

**Ready to proceed?**
```

## Quality Checklist

Before finalizing curriculum:

**Structure**:
- [ ] Clear progression from simple to complex
- [ ] Each episode has distinct, focused objective
- [ ] Review episodes every 3-4 lessons
- [ ] Dependencies mapped (no knowledge gaps)
- [ ] Appropriate scope (not too broad/narrow)

**Pedagogy**:
- [ ] Spaced repetition applied (key concepts in 3+ episodes)
- [ ] Active recall prompts in every episode
- [ ] Progressive complexity (achievable steps)
- [ ] Interleaving where beneficial
- [ ] Elaboration through examples and analogies

**Audience Fit**:
- [ ] Prerequisites clearly stated
- [ ] Appropriate for senior engineers
- [ ] Production-relevant content
- [ ] Respects learner's time (15 min episodes)

**Documentation**:
- [ ] Internal curriculum plan complete
- [ ] Course index page ready to publish
- [ ] Learning objectives specific and measurable
- [ ] Dependency graph clear

## Anti-Patterns to Avoid

### ❌ Feature Tour Curriculum
**Problem**: Each episode is just "here's feature X"

**Fix**: Organize by learning objectives and use cases

### ❌ No Review Mechanism
**Problem**: Concepts introduced once, never reinforced

**Fix**: Map spaced repetition, add review episodes

### ❌ Assumed Knowledge Gaps
**Problem**: Episode 5 requires knowledge from Episode 2, but not clear

**Fix**: Explicit dependency graph, mention prerequisites in each episode

### ❌ Cognitive Overload
**Problem**: Episodes try to cover 3-4 major concepts

**Fix**: One core concept per episode, break complex topics into series

### ❌ Linear Only Progression
**Problem**: Episode 10 is harder than 9, no other structure

**Fix**: Add modules, review episodes, interleaving

---

## Instructions for Claude

When this skill is invoked:

1. **Verify research exists**:
   - Check for Course Research Brief
   - If missing, tell user to run lesson-research first

2. **Review research findings**:
   - Learning path structure
   - Pain points to address
   - Knowledge gaps to fill
   - Prerequisite requirements

3. **Design episode structure**:
   - Apply progressive complexity
   - Map concept dependencies
   - Place review episodes every 3-4 lessons
   - Ensure each episode has distinct objective

4. **Create spaced repetition map**:
   - Identify key concepts
   - Plan where each appears (3+ times)
   - Design review episodes
   - Build callbacks into structure

5. **Write curriculum documents**:
   - Internal planning doc (curriculum-plan.md)
   - Course index page (index.md)
   - Both saved to docs/podcasts/courses/[course-slug]/

6. **Validate against checklist** (all items)

7. **Present to user**:
   - Curriculum summary
   - Pedagogical features applied
   - Episode structure table
   - Next steps (lesson-outline for Episode 1)

**Remember**: Good curriculum design is the foundation of effective learning. The time spent here pays off in every episode.
