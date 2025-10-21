---
name: Lesson Research
description: Research topics for educational course series by analyzing learning paths, student pain points, common misconceptions, and community Q&A to design effective curricula.
allowed-tools: WebSearch, WebFetch, Grep, Read, Glob
---

# Lesson Research

Research and validate topics for educational course series by analyzing learning paths, identifying common student struggles, and gathering evidence for curriculum design.

## When to Use This Skill

Use this skill when:
- Starting a new course series and need to identify curriculum topics
- User asks: "Research [topic] for a course series" or "What should I teach about [topic]?"
- Validating if a topic has sufficient depth for multi-episode curriculum
- Understanding the learning journey from beginner to proficient

## Target Audience

Senior platform engineers, SREs, DevOps engineers (5+ years experience) who want:
- Deep technical understanding (not surface-level tutorials)
- Production-ready knowledge (real-world scenarios)
- Career advancement (mastery of core technologies)
- Efficient learning (no time for fluff)

## Research Process

### 1. Identify Learning Path Structure

Map the journey from novice to competent:

**Foundation Topics** (Episodes 1-2):
- Mental models and first principles
- Core terminology and concepts
- "Why does this exist?" context
- Prerequisites learners need

**Core Topics** (Episodes 3-N-2):
- Essential features and patterns
- Common use cases in production
- How experienced engineers think about the tool
- Integration with ecosystem

**Advanced Topics** (Episode N-1 to N):
- Performance optimization
- Production troubleshooting
- Advanced patterns and anti-patterns
- Career-level mastery

### 2. Analyze Common Pain Points

Search for where learners struggle:

**Stack Overflow Analysis**:
- Most upvoted questions about the topic
- Common error messages and debugging questions
- "How do I..." patterns
- Questions that appear repeatedly

**Reddit/HN Discussion Patterns**:
- r/devops, r/kubernetes, r/aws, r/sre
- "I don't understand..." posts
- "Why would you..." debates
- Misconceptions being corrected

**GitHub Issues**:
- Documentation gaps ("docs unclear on...")
- Feature confusion ("How does X work with Y?")
- Common setup mistakes
- Integration problems

### 3. Identify Knowledge Gaps

What's missing from existing tutorials?

**Gap Types**:
- **Conceptual gaps**: Tutorials show "what" but not "why"
- **Context gaps**: Missing production scenarios
- **Integration gaps**: Isolated tutorials, no ecosystem view
- **Troubleshooting gaps**: "Happy path" only, no debugging
- **Decision-making gaps**: No framework for when to use what

**Questions to Answer**:
- What do existing tutorials skip?
- What do senior engineers know that juniors don't?
- What takes engineers months to learn through trial/error?
- What's assumed knowledge that shouldn't be?

### 4. Map Prerequisites and Dependencies

Build the dependency tree:

**For Each Subtopic**:
- What must learners know BEFORE this?
- What concepts build on this?
- What can be learned in parallel?
- What's "nice to know" vs "must know"?

**Example (Kubernetes Course)**:
```
Prerequisites:
- Docker containers (MUST know)
- Basic networking (MUST know)
- YAML syntax (nice to know, can learn alongside)

Episode 1: Mental Model (needs: containers)
Episode 2: Pods (needs: Episode 1)
Episode 3: Deployments (needs: Episode 2)
Episode 4: Services (needs: Episodes 1-2, can parallel with 3)
```

### 5. Validate Curriculum Scope

Can this support a course series?

**Depth Check**:
- Enough material for 5+ episodes? (minimum viable course)
- Can organize into logical progression?
- Clear learning objectives per episode?
- Distinct concepts (not repetitive)?

**Breadth Check**:
- Covers core use cases (80/20 rule)?
- Addresses common misconceptions?
- Includes troubleshooting and debugging?
- Bridges theory to production practice?

**Audience Fit**:
- Appropriate for senior engineers (not too basic)?
- Production-relevant (not just toy examples)?
- Career value (skills they'll use)?
- Time-efficient (respects busy schedules)?

### 6. Gather Supporting Evidence

Collect for curriculum design:

**Technical Resources**:
- Official documentation structure (shows canonical organization)
- Popular GitHub repos (stars, real-world usage)
- Conference talks (what experts emphasize)
- Books and courses (existing curriculum approaches)

**Learning Data**:
- Tutorial completion rates (if available)
- Community sentiment ("best X tutorial")
- What questions persist after tutorials
- Where learners get stuck

**Production Context**:
- How companies use the technology
- Common architectures and patterns
- Real incident reports and post-mortems
- Performance characteristics at scale

## Output Format

Produce a **Course Research Brief**:

```markdown
# Course Research Brief: [Topic Name]

## Summary
[2-3 sentences: What this course covers and why senior engineers need it NOW]

## Target Audience Fit
**Prerequisites**: [What learners must know before starting]
**Career Value**: [Why this matters for senior engineers]
**Time Investment**: [X hours total, Y weeks at Z hours/week]

## Learning Path Analysis

### Foundation (Episodes 1-2)
- **Mental Model**: [Core concept that unlocks everything]
- **Key Terminology**: [Essential vocabulary]
- **Why It Exists**: [Problem it solves, design philosophy]

### Core Topics (Episodes 3-N-2)
1. **[Topic 1]**: [What they'll learn, why it matters]
2. **[Topic 2]**: [What they'll learn, why it matters]
3. **[Topic 3]**: [What they'll learn, why it matters]
[Continue for all core topics]

### Advanced Topics (Episodes N-1 to N)
- **[Advanced Topic 1]**: [Production-level mastery]
- **[Advanced Topic 2]**: [Troubleshooting and optimization]
- **Review & Integration**: [How everything connects]

## Common Pain Points

### Misconceptions to Address
1. **Misconception**: [What learners wrongly believe]
   - **Reality**: [What's actually true]
   - **Why it matters**: [Impact on production usage]

2. **Misconception**: [Another common misunderstanding]
   - **Reality**: [Correction]
   - **Why it matters**: [Consequences]

### Where Learners Struggle
- **[Pain Point 1]**: [Stack Overflow evidence, GitHub issues]
- **[Pain Point 2]**: [Reddit threads, common errors]
- **[Pain Point 3]**: [Documentation gaps, confusion points]

## Knowledge Gaps in Existing Tutorials

### What's Missing
1. **[Gap Type]**: [Specific gap, e.g., "No tutorials show multi-region setup"]
   - **Our Approach**: [How we'll fill this gap]

2. **[Gap Type]**: [Another gap, e.g., "Debugging strategies absent"]
   - **Our Approach**: [How we'll address this]

## Prerequisite Map

```
Required Before Course:
├─ Docker containers (hands-on experience)
├─ Linux command line (intermediate)
└─ YAML syntax (basic familiarity)

Episode Dependencies:
Episode 1 (Foundation) ─┬─> Episode 2 (Core Concept A)
                        ├─> Episode 3 (Core Concept B) ─> Episode 5 (Integration)
                        └─> Episode 4 (Core Concept C) ─> Episode 6 (Advanced)
```

## Proposed Course Structure

**Total Episodes**: [N episodes, ~X hours total]

1. **Episode 1: [Title]** (15 min)
   - Learning Objectives: [Specific, measurable]
   - Covers: [Topics]
   - Addresses: [Pain points]

2. **Episode 2: [Title]** (15 min)
   - Learning Objectives: [Specific, measurable]
   - Covers: [Topics]
   - Builds on: [Previous episodes]

[Continue for all episodes]

N. **Episode N: [Title]** (15 min)
   - Learning Objectives: [Integration and mastery]
   - Covers: [Advanced topics, review]
   - Prepares for: [Next steps, further learning]

## Supporting Resources

### Official Documentation
- [Link] - [What it covers, why it's relevant]
- [Link] - [Key sections to reference]

### Community Evidence
- [Stack Overflow Question] - [X upvotes, shows pain point Y]
- [Reddit Discussion] - [Common confusion about Z]
- [GitHub Issue] - [Documentation gap in W]

### Real-World Usage
- [Company Blog Post] - [How they use it at scale]
- [Conference Talk] - [Production lessons learned]
- [Post-Mortem] - [What can go wrong]

### Existing Tutorials (Gap Analysis)
- [Popular Tutorial X] - [Strengths: ..., Gaps: ...]
- [Course Y] - [Strengths: ..., Gaps: ...]

## Course Viability Assessment

**Depth**: [1-5 rating] - Sufficient material for 5+ episodes?
**Progression**: [1-5 rating] - Clear learning path from basic to advanced?
**Relevance**: [1-5 rating] - Matters to senior engineers NOW?
**Uniqueness**: [1-5 rating] - Fills gaps in existing content?
**Production Value**: [1-5 rating] - Real-world applicability?

**Overall**: [STRONG/MODERATE/WEAK] - [Recommendation]

## Next Steps

**If STRONG**:
1. Use lesson-curriculum skill to design detailed curriculum
2. Create course page with episode breakdown
3. Begin with lesson-outline for Episode 1

**If MODERATE**:
1. Narrow scope to strongest topics
2. Consider shorter course (5-8 episodes vs 10-15)
3. Re-evaluate with adjusted scope

**If WEAK**:
1. Topic may be too basic or too niche
2. Consider different topic
3. Or restructure as single deep-dive lesson
```

## Quality Checks

Before finalizing research:
- [ ] Identified 5+ distinct episode topics
- [ ] Mapped prerequisite dependencies
- [ ] Found 3+ common pain points/misconceptions
- [ ] Located gaps in existing tutorials
- [ ] Validated audience fit (senior engineers)
- [ ] Confirmed production relevance
- [ ] Gathered supporting evidence (SO, Reddit, GitHub)
- [ ] Structured logical learning progression

## Research Sources to Use

**Community Platforms**:
- Stack Overflow: Tag-specific questions, sorted by votes
- Reddit: r/devops, r/kubernetes, r/aws, r/sre, r/terraform
- Hacker News: Search for topic discussions, "Ask HN" threads
- GitHub: Issues and discussions in official repos

**Learning Platforms**:
- Existing course curricula (Pluralsight, O'Reilly, Linux Foundation)
- Popular YouTube tutorials (what they cover, what they skip)
- Bootcamp syllabi (structure and progression)
- Certification exam blueprints (industry-standard coverage)

**Technical Sources**:
- Official documentation (table of contents = learning path)
- Books (chapter organization = topic breakdown)
- Conference talks (what experts emphasize)
- Company engineering blogs (production patterns)

## Anti-Patterns to Avoid

### ❌ Tutorial List Syndrome
**Problem**: Just listing features without pedagogical structure

**Fix**: Focus on learning journey and skill progression

### ❌ Documentation Regurgitation
**Problem**: Course just mirrors official docs

**Fix**: Identify what docs assume or skip, fill those gaps

### ❌ Toy Example Trap
**Problem**: Only "hello world" scenarios, no production context

**Fix**: Research real-world usage patterns and gotchas

### ❌ Prerequisite Mismatch
**Problem**: Course assumes wrong baseline knowledge

**Fix**: Explicitly map what learners must know beforehand

### ❌ Kitchen Sink Approach
**Problem**: Trying to cover everything, losing focus

**Fix**: Apply 80/20 rule - core topics that unlock the rest

## Example Research Output

**Topic**: "Prometheus Monitoring Fundamentals"

**Community Signal**:
- Stack Overflow: 2,500+ questions, top issues are PromQL confusion, retention settings, high cardinality problems
- Reddit r/devops: 30+ threads asking "how to structure metrics," "label best practices," "when to use recording rules"
- GitHub prometheus/prometheus: 150+ issues about query performance, documentation gaps on federation

**Pain Points Identified**:
1. **PromQL Mental Model**: Engineers treat it like SQL, get confused
2. **Label Cardinality**: Don't understand impact until production explodes
3. **Recording Rules**: When/why to use them is unclear
4. **Federation**: Multi-cluster setup poorly documented

**Proposed Course Structure** (8 episodes):
1. Mental Model: Time Series Databases (15 min)
2. Metrics Types & When to Use Each (15 min)
3. PromQL Fundamentals (15 min)
4. Labels: Power and Danger (15 min)
5. Recording Rules for Performance (12 min)
6. Alerting Best Practices (15 min)
7. Federation & Scalability (15 min)
8. Production Troubleshooting & Review (15 min)

**Knowledge Gaps Filled**:
- No existing tutorial explains label cardinality BEFORE it's a problem
- PromQL tutorials teach syntax but not "how to think in time series"
- Recording rules covered in docs but not "when to use" decision framework

**Strength**: 5/5 depth, 5/5 progression, 5/5 relevance, 4/5 uniqueness, 5/5 production = STRONG

---

## Instructions for Claude

When this skill is invoked:

1. **Clarify topic** if not specific:
   - What technology/concept?
   - Target depth (fundamentals vs advanced)?
   - Estimated course length preference?

2. **Research community pain points**:
   - Search Stack Overflow for top questions
   - Search Reddit/HN for discussion patterns
   - Check GitHub issues for documentation gaps
   - Identify common misconceptions

3. **Analyze learning paths**:
   - Review existing course curricula
   - Check official documentation structure
   - Identify prerequisite dependencies
   - Map beginner → proficient progression

4. **Validate course viability**:
   - Can support 5+ distinct episodes?
   - Clear learning progression?
   - Fills gaps in existing content?
   - Relevant to senior engineers?

5. **Create Course Research Brief**:
   - Learning path structure (foundation → core → advanced)
   - Common pain points with evidence
   - Knowledge gaps in existing tutorials
   - Prerequisite map
   - Proposed episode structure
   - Viability assessment

6. **Give recommendation**:
   - STRONG: Proceed to lesson-curriculum skill
   - MODERATE: Adjust scope, re-evaluate
   - WEAK: Consider different topic

Always prioritize:
- Evidence from community (not assumptions)
- Production relevance over toy examples
- Learning science (prerequisites, progression)
- Senior engineer perspective (respect their experience)

The research phase is critical - a well-researched topic produces a compelling course. Don't rush it.
