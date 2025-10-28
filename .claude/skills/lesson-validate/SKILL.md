---
name: Lesson Validate
description: Fact-check lesson scripts for accuracy, verify sources, check for marketing speak vs data, ensure technical correctness, and validate pedagogical soundness.
allowed-tools: Read, WebFetch, Grep, Glob
---

# Lesson Validate

Verify the accuracy, quality, and pedagogical soundness of lesson scripts before formatting and publishing. The Platform Engineering Playbook's reputation depends on technical correctness and trustworthy information.

## When to Use This Skill

Use this skill when:
- User says: "Validate lesson script", "Fact-check course episode"
- A script exists in `docs/podcasts/courses/[course-slug]/scripts/` that needs verification
- Before moving to formatting/publishing stages

## Core Validation Principles

### Why This Matters

**One inaccurate statistic destroys trust.**

The courses target senior engineers who:
- Spot inaccuracies immediately
- Value data-driven decision making
- Distrust marketing hype
- Rely on us for accurate information

### Validation Standards

1. **Every statistic must be verifiable**
2. **Technical claims must match official documentation**
3. **Pricing data must be current with dates noted**
4. **Case studies must be real (or clearly hypothetical)**
5. **No marketing speak without data backing**
6. **Learning objectives must be achievable**
7. **Prerequisites must be accurate**
8. **Examples must be runnable/accurate**

## Validation Checklist

### 1. Statistics & Numbers

For EVERY number mentioned in the script:

**Verify**:
- [ ] Can you find the original source?
- [ ] Is the number current (within 1 year)?
- [ ] Is the context correct? (not cherry-picked)
- [ ] Would the source confirm this interpretation?

**Common Issues**:
- Confusing percentage vs percentage points
- Outdated data (2023 numbers in 2025 episode)
- Misattributed statistics
- "Studies show..." without naming the study

**Example Validation**:
```
Script: "85% of organizations struggle with shadow AI"

✅ VERIFY:
- Source: [Link to actual report]
- Date: Published Q4 2024
- Context: Survey of 500 enterprise IT leaders
- Exact wording in source: "85% report challenges with ungoverned AI tools"

✓ VALID - Number checks out
```

### 2. Technical Claims

For technical statements about how things work:

**Verify Against**:
- [ ] Official documentation (current version)
- [ ] Engineering blogs from companies using it
- [ ] Conference talks from practitioners
- [ ] GitHub repositories and issues

**Common Issues**:
- Confusing similar but different technologies
- Using outdated terminology
- Oversimplifying complex systems
- Ignoring important caveats

**Example Validation**:
```
Script: "Kubernetes uses a declarative model where you describe desired state and controllers reconcile actual state"

✅ VERIFY:
- Source: kubernetes.io/docs/concepts
- Terminology: ✓ "declarative", ✓ "desired state", ✓ "controllers"
- Accuracy: ✓ Correct high-level explanation
- Caveats: Mention that some controllers behave differently?

✓ VALID - Accurate high-level explanation
```

### 3. Pricing Data

For pricing comparisons:

**Verify**:
- [ ] Current as of [DATE] on vendor website
- [ ] Includes relevant tier (Pro, Enterprise, etc.)
- [ ] Notes any limitations or required add-ons
- [ ] Fair comparison (similar features/scale)

**Common Issues**:
- Comparing different tiers
- Missing required add-ons in calculation
- Outdated pricing (changes frequently)
- Ignoring volume discounts

### 4. Case Studies & Examples

For real-world examples:

**Verify**:
- [ ] Company/story is real (or clearly marked hypothetical)
- [ ] Numbers are specific and sourced
- [ ] Timeline is realistic
- [ ] Outcomes are documented

**Common Issues**:
- Composite examples presented as real
- Exaggerated outcomes
- Missing context (company size, complexity)
- Unverifiable claims

### 5. Feature Claims

For "X supports Y" statements:

**Verify**:
- [ ] Feature exists in current version
- [ ] Works as described
- [ ] Any limitations or edge cases
- [ ] Availability (GA, beta, preview?)

**Common Issues**:
- Beta features described as production-ready
- Enterprise-only features presented as standard
- Deprecated features
- Coming soon presented as available

### 6. Pedagogical Validation (UNIQUE TO LESSONS)

**Learning Objectives Check**:
- [ ] Objectives stated in script match outline
- [ ] Objectives are specific and measurable
- [ ] Content actually teaches what objectives promise
- [ ] Learner could reasonably achieve objectives in one 15-min lesson

**Example**:
```
Objective: "Explain the Pod abstraction and why containers alone aren't enough"

✅ CHECK:
- Is Pod abstraction explained? ✓ Yes (section 2)
- Is "why not just containers" addressed? ✓ Yes (comparison in section 3)
- Depth appropriate for objective? ✓ Yes
- Achievable in episode? ✓ Yes

✓ VALID
```

**Prerequisites Check**:
- [ ] Prerequisites mentioned are accurate
- [ ] No assumed knowledge beyond stated prerequisites
- [ ] Links to prerequisite content exist (if internal)
- [ ] Learner with stated prerequisites can understand content

**Example**:
```
Script states: "You should know Docker containers and basic networking"

✅ CHECK:
- Does lesson require Docker knowledge? ✓ Yes (uses container terminology)
- Does lesson require networking knowledge? ✓ Yes (discusses network namespaces)
- Are there other unlisted prerequisites? ⚠️ Check for YAML assumptions
- Are these realistic prerequisites? ✓ Yes, appropriate

⚠️ ISSUE: Also assumes YAML familiarity - add to prerequisites
```

**Example Accuracy**:
- [ ] Code examples are syntactically correct
- [ ] Commands will actually work
- [ ] File paths and configurations are valid
- [ ] No copy-paste errors

**Progression Check** (if Episode 2+):
- [ ] Builds appropriately on previous episodes
- [ ] Callbacks to previous concepts are accurate
- [ ] No knowledge gaps between episodes
- [ ] Spaced repetition claims match curriculum plan

## Engagement Quality Checks

**CRITICAL**: Lessons must be engaging and maintain learner attention throughout. Educational content that is factually accurate but boring will NOT achieve learning objectives. Check for these engagement elements:

### Content Variety & Concreteness

**Concrete Examples** (not abstractions):
- [ ] Uses specific numbers, scenarios, names (not "imagine a company...")
- [ ] At least 2-3 concrete examples per major concept
- [ ] Examples relate to real production scenarios
- [ ] No walls of abstract explanation without grounding

**Example**:
```
❌ BAD: "When your application has high traffic, you need to scale."
✅ GOOD: "When your checkout service hits 10,000 requests per second during Black Friday, you need to scale from 5 pods to 50 pods."

❌ BAD: "Resource limits help prevent issues."
✅ GOOD: "Without resource limits, that memory-leaking analytics service consumed 32GB of RAM and crashed 4 other applications sharing the same node. I learned this at 2 AM on a Tuesday."
```

**Analogies & Mental Models**:
- [ ] 1-2 analogies per major new concept
- [ ] Analogies relate to familiar everyday concepts
- [ ] Analogies clarify, not confuse
- [ ] "Think of it like..." or "Similar to..." phrasing

**Example**:
```
✅ GOOD: "Think of Pods like shipping containers. You don't ship individual items—you group related items together. Same with containers in a Pod."

✅ GOOD: "Resource requests are like reserving a hotel room. Just because you request 2GB doesn't mean you'll use it all, but Kubernetes guarantees it's available."
```

**War Stories & Real Scenarios**:
- [ ] Includes 1-2 "war stories" (things that went wrong)
- [ ] Real production incidents or common mistakes
- [ ] Shows consequences of not following best practices
- [ ] Makes concepts memorable through narrative

**Example**:
```
✅ GOOD: "I once deployed a StatefulSet without persistent volume claims. Two hours later, our PostgreSQL database lost all data during a routine node upgrade. That's a resume-generating event you want to avoid."
```

### Sentence Structure & Pacing

**Varied Sentence Length**:
- [ ] Mix of short (5-10 words) and longer (20-30 words) sentences
- [ ] Not monotonous rhythm
- [ ] Short sentences for emphasis
- [ ] Longer sentences for explanation

**Example**:
```
❌ BAD (monotonous):
"Kubernetes has many features. It provides container orchestration. It handles scaling automatically. It manages deployments efficiently. It ensures high availability."

✅ GOOD (varied):
"Kubernetes is a container orchestration platform. Need to scale? It handles that automatically. What about deployments? Rolling updates, blue-green, canary—all built in. And if a node goes down at 3 AM? Kubernetes is already rescheduling your workloads before you wake up."
```

**Rhetorical Questions** (sparingly, 2-3 per lesson):
- [ ] Uses questions to engage ("Why does this matter?")
- [ ] Questions preview upcoming explanations
- [ ] Not overused (not every paragraph)
- [ ] Questions sound natural, not forced

**Example**:
```
✅ GOOD: "Why do we need resource limits when we already set requests? Great question."
✅ GOOD: "What happens when a pod tries to use more memory than the limit? It gets OOMKilled—Out Of Memory Killed."
```

### Teaching Techniques

**Active Recall Moments**:
- [ ] "Pause and try..." or "Before we continue, recall..." prompts
- [ ] Gives learner time to think before revealing answer
- [ ] Reinforces previous concepts
- [ ] 1-2 active recall moments per lesson

**Example**:
```
✅ GOOD: "Pause here and think: if you set a memory request of 1GB and a limit of 2GB, what happens when the pod tries to use 1.5GB? Take a moment... Got it? The pod can use 1.5GB—it's between request and limit."
```

**Signposting** (navigation cues):
- [ ] "First... Second... Third..." structure for lists
- [ ] "Let's start with..." / "Now let's turn to..." transitions
- [ ] Clear indication of major section shifts
- [ ] Learner always knows where they are

**Example**:
```
✅ GOOD: "We'll cover three main types of probes. First, liveness probes—these detect when your app is stuck. Second, readiness probes—these determine if your app can handle traffic. Third, startup probes—these give slow-starting apps extra time."
```

**Elaboration** ("In other words..."):
- [ ] Explains concepts multiple ways
- [ ] "To put it another way..." / "In other words..." phrasing
- [ ] Reinforces understanding through rephrasing
- [ ] Helps different learning styles

**Example**:
```
✅ GOOD: "Resource requests tell Kubernetes how much CPU and memory to reserve. In other words, it's like booking a table at a restaurant—you're guaranteed that space even if you don't use it all."
```

**Callbacks to Previous Concepts**:
- [ ] References previous episodes explicitly ("Remember in Episode 2...")
- [ ] Reinforces spaced repetition
- [ ] Helps learners build connections
- [ ] Accurate references (verify episode numbers)

### Tone & Voice

**Conversational vs Academic**:
- [ ] Sounds like a knowledgeable colleague explaining, not lecturing
- [ ] Uses "we" and "you" (not passive voice or third person)
- [ ] Natural contractions ("don't", "you'll", "let's")
- [ ] Appropriate informal language ("kick the tires", "under the hood")

**Example**:
```
❌ BAD (too academic): "One should configure resource limits to prevent containerized applications from consuming excessive system resources."

✅ GOOD (conversational): "You'll want to set resource limits so your containers don't hog all the memory and crash your neighbors. I've seen it happen—one runaway process takes down a whole node."
```

**No Patronizing Phrases**:
- [ ] Avoids "as you probably know", "obviously", "simply"
- [ ] Respects learner intelligence
- [ ] Doesn't assume knowledge or ignorance
- [ ] Acknowledges complexity when appropriate

**Example**:
```
❌ BAD: "Obviously, you need to set resource requests. As you know, this is basic Kubernetes."
❌ BAD: "Simply add resource limits to your YAML."

✅ GOOD: "Resource requests aren't intuitive at first—they confused me for months. Let's break down exactly how they work."
✅ GOOD: "Adding resource limits requires careful tuning. Here's a systematic approach."
```

**Authoritative but Humble**:
- [ ] Shares expertise without arrogance
- [ ] Acknowledges trade-offs and uncertainty
- [ ] "In my experience..." or "I've found..." for opinions
- [ ] Admits when things are complex or controversial

**Example**:
```
✅ GOOD: "In my experience, setting limits too low causes more problems than setting them too high. But there's real debate in the community about this—some teams prefer conservative limits."

✅ GOOD: "This is a complex topic with no perfect answer. Here's how I think through the trade-offs..."
```

### Overall Engagement Assessment

**Engagement Score** (aim for 8+/10):
- [ ] Concrete examples (not abstractions) - 2 points
- [ ] Analogies present (1-2 per major concept) - 1 point
- [ ] War stories or real scenarios - 1 point
- [ ] Varied sentence length and pacing - 1 point
- [ ] Rhetorical questions (2-3 total) - 1 point
- [ ] Active recall moments - 1 point
- [ ] Signposting and structure - 1 point
- [ ] Conversational tone (not academic) - 1 point
- [ ] No patronizing language - 1 point
- [ ] Authoritative but humble voice - 1 point

**Total: ___/10**

If score < 8, lesson needs engagement improvements before formatting.

### Common Engagement Failures

**❌ Too Abstract**:
```
BAD: "Kubernetes provides various mechanisms for managing application lifecycle and ensuring system reliability through declarative configuration and automated control loops."

This is accurate but terrible teaching. Where are the examples? What does this mean in practice?

GOOD: "Kubernetes keeps your apps running. You tell it 'I want 5 copies of this service,' and Kubernetes makes it happen. If one crashes? Kubernetes starts a replacement—automatically, usually before you even notice."
```

**❌ Monotonous Pacing**:
```
BAD: All sentences have similar length and structure. Every concept gets equal weight. There's no variation in rhythm. This creates a droning effect. Learners tune out quickly.

GOOD: Mix it up. Short sentences emphasize key points. Longer sentences provide detailed explanations with multiple clauses that elaborate on complex concepts. Then back to short. See the difference?
```

**❌ No Stories or Context**:
```
BAD: Just lists of features and specifications without showing WHY they matter or WHEN you'd use them.

GOOD: "We added liveness probes after a memory leak caused our payment service to hang for 6 hours. Requests timed out, but the pod stayed 'running' so Kubernetes didn't restart it. $40K in lost sales later, we learned to always configure health checks."
```

**❌ Academic/Formal Tone**:
```
BAD: "One must ensure proper configuration of the resource management parameters to avoid suboptimal performance characteristics."

GOOD: "You'll want to tune your resource settings carefully. Too low? Your apps get throttled. Too high? You're wasting money. Let's find the sweet spot."
```

## Source Quality Assessment

### Primary Sources (Prefer These)

**Official Documentation**:
- Vendor docs (e.g., kubernetes.io, docs.aws.amazon.com)
- Official GitHub repositories
- Published release notes

**Practitioner Content**:
- Company engineering blogs
- Conference talks from engineers (not sales)
- Published post-mortems
- Peer-reviewed papers

**Market Data**:
- Published research reports (Gartner, Forrester) with dates
- GitHub stars/contributors (verifiable metrics)
- Job posting analysis (for skill demand)

### Secondary Sources (Use Cautiously)

**Tech Journalism**:
- The New Stack, InfoQ, Ars Technica
- Verify claims against primary sources
- Note publication date

**Community Discussion**:
- Reddit, Hacker News (sentiment, not facts)
- Stack Overflow (for pain points)
- Always verify technical claims independently

### Unacceptable Sources

**Never Trust Without Verification**:
- Marketing content without technical backing
- Unattributed "studies show" claims
- Anonymous sources
- Outdated content (>2 years) presented as current
- AI-generated content without verification

## Validation Process

### Step 1: Read Script Carefully

Mark every claim that needs verification:
- [S] Statistics
- [T] Technical claims
- [P] Pricing
- [C] Case studies
- [F] Feature claims
- [L] Learning objectives (pedagogical)
- [E] Examples/code

### Step 2: Verify Each Claim

Use allowed tools:
- **WebFetch**: Check vendor websites, official docs
- **Read**: Check outline, curriculum plan, research for source notes
- **Grep**: Search codebase for related examples
- **Glob**: Find prerequisite lessons/content

Create validation notes:
```markdown
## Validation Report: Lesson XX

### Statistics
1. "85% of organizations..." ✓ VERIFIED [source link]
2. "Costs 30-40% less..." ⚠️ NEEDS SOURCE

### Technical Claims
1. "Kubernetes uses controllers..." ✓ VERIFIED (k8s docs)
2. "Supports automatic scaling..." ⚠️ CLARIFY (needs conditions)

### Pedagogical
1. Learning objective #1 achievable ✓ VERIFIED
2. Prerequisites accurate ⚠️ MISSING: Also needs YAML knowledge

### Examples
1. Pod YAML example ✓ VERIFIED (runs correctly)
2. kubectl command ⚠️ ISSUE: Typo in flag name

### Issues Found: 4
### Issues Fixed: TBD
```

### Step 3: Check for Red Flags

**Marketing Speak Without Data**:
- "Revolutionary", "game-changing", "best-in-class"
- "Dramatically improves" (by how much?)
- "Solves all your problems"

**Replace with**:
- Specific numbers
- Comparative data
- Realistic trade-offs

**Absolute Statements**:
- "Always", "Never", "Everyone"
- "X is better than Y" (without context)

**Replace with**:
- "In most cases", "Typically", "Many teams"
- "X is better for Y use case, but Z works better for..."

### Step 4: Technical Accuracy Review

**Check terminology**:
- [ ] Using correct names (Kubernetes not "K8")
- [ ] Accurate acronyms
- [ ] Consistent naming throughout

**Check compatibility**:
- [ ] Version compatibility claims accurate
- [ ] Integration claims verified
- [ ] Performance claims realistic

**Check architecture**:
- [ ] System designs described accurately
- [ ] Data flow explanations correct
- [ ] Security model appropriately explained

### Step 5: Validate Against CLAUDE.md Standards

**Tone Check**:
- [ ] Authoritative but humble (not arrogant)
- [ ] Honest about trade-offs (not one-sided)
- [ ] Practical focus (not academic)
- [ ] Skeptical of hype (demands evidence)
- [ ] Conversational and accessible

**Target Audience Check**:
- [ ] Appropriate depth for senior engineers
- [ ] No overly basic 101 content (unless foundational episode)
- [ ] Respects learner intelligence
- [ ] Actionable insights

## Output Format

Produce a **Validation Report**:

```markdown
# Validation Report: Lesson XX - [Title]

**Course**: [Course Name]
**Validated by**: Claude (Lesson Validate Skill)
**Date**: 2025-10-20
**Script Location**: docs/podcasts/courses/[course-slug]/scripts/lesson-XX.txt

## Summary
- **Total Claims Checked**: [N]
- **Issues Found**: [N]
- **Status**: [READY/NEEDS FIXES/MAJOR ISSUES]

## Statistics Verified
1. ✅ "85% of organizations..." - Source: [link], Date: Q4 2024
2. ⚠️ "Costs 30-40% less..." - ISSUE: No source provided
3. ✅ "GitHub stars increased 890%" - Source: [GitHub API], verified

## Technical Claims Verified
1. ✅ "Kubernetes uses controllers..." - Verified against k8s.io/docs
2. ⚠️ "Supports automatic scaling" - CLARIFY: Requires HPA configuration
3. ✅ "PostgreSQL pronunciation" - Needs pronunciation tag

## Pedagogical Validation
1. ✅ Learning objective #1: "Explain Pod abstraction" - Content delivers
2. ✅ Learning objective #2: "Create Pod manifest" - Example included
3. ⚠️ Prerequisites incomplete - YAML knowledge not mentioned but required
4. ✅ Builds on Episode 1 appropriately - Callbacks accurate
5. ✅ Example progression logical - Simple → Complex

## Examples & Code Verified
1. ✅ Pod YAML (line 145) - Valid syntax, runs correctly
2. ⚠️ kubectl command (line 203) - Typo: `--replicas` should be `--replicas=`
3. ✅ Deployment manifest (line 298) - Correct, production-ready

## Issues Found

### HIGH Priority (Must Fix)
1. **Line 47**: "Studies show 50% improvement" - No source provided
   - **Fix**: Add source or remove claim

2. **Line 203**: kubectl command has typo
   - **Fix**: `kubectl scale deployment my-app --replicas 5` (add equals sign)

3. **Prerequisites section**: Missing YAML prerequisite
   - **Fix**: Add "Basic YAML syntax" to prerequisites

### MEDIUM Priority (Should Fix)
1. **Line 23**: Outdated pricing from 2024
   - **Fix**: Verify current pricing or note date

2. **Line 112**: Technical term needs brief explanation
   - **Fix**: Add one-sentence explanation for clarity

### LOW Priority (Nice to Have)
1. **Line 5**: Could use more specific number
   - **Suggestion**: "Many teams" → "In surveys of 500+ teams"

## Marketing Speak Detected

1. **Line 34**: "Revolutionary approach" - NO DATA
   - **Fix**: "Approach that reduced deployment time by 60%"

## Pedagogical Recommendations

1. **Active Recall**: Good use of retrieval prompts (lines 89, 234)
2. **Spaced Repetition**: Callbacks to Episode 1 accurate and appropriate
3. **Examples**: Progression from simple to complex is logical
4. **Analogies**: Pod/shipping container analogy effective
5. **Practice Moments**: Pause points well-placed

## Recommendations

### Before Formatting
- [ ] Fix all HIGH priority issues
- [ ] Address MEDIUM priority issues
- [ ] Remove/replace marketing speak
- [ ] Update prerequisites section

### Before Publishing
- [ ] Verify all sources still accessible
- [ ] Check pronunciation tags on technical terms
- [ ] Ensure consistent terminology throughout
- [ ] Test all code examples

## Status: [READY/NEEDS FIXES/MAJOR ISSUES]

**Notes**: [Any additional context or concerns]
```

## Anti-Patterns to Avoid

### ❌ Accepting Claims at Face Value
Don't assume the script writer verified everything. Check anyway.

### ❌ Using Wikipedia as Primary Source
Wikipedia is a starting point, not an authoritative source. Trace to primary sources.

### ❌ Trusting Vendor Marketing
Marketing pages exaggerate. Find practitioner reviews and official docs.

### ❌ Skipping Version Checks
"Kubernetes supports X" - which version? Is it GA or beta?

### ❌ Ignoring Context
"50% faster" - compared to what? Under what conditions?

### ❌ Not Testing Code Examples
Don't assume YAML/code is correct - verify syntax and test if possible.

---

## Instructions for Claude

When this skill is invoked:

1. **Locate script file**:
   ```bash
   ls -la docs/podcasts/courses/[course-slug]/scripts/
   ```

2. **Read related files** for context:
   - Script to validate
   - Outline (for planned content)
   - Curriculum plan (for prerequisites, learning objectives)
   - Previous episode scripts (for consistency)

3. **Read script completely**, marking claims to verify:
   - [S] Statistics
   - [T] Technical claims
   - [P] Pricing
   - [C] Case studies
   - [F] Features
   - [L] Learning objectives
   - [E] Examples/code

4. **Verify each claim** using allowed tools:
   - WebFetch vendor sites for pricing, docs
   - Read outline/curriculum/research for source notes
   - Cross-reference official documentation
   - Check example code for syntax errors

5. **Check for red flags**:
   - Marketing speak without data
   - Absolute statements
   - Outdated information
   - Unsourced statistics

6. **Validate pedagogy**:
   - Learning objectives achievable
   - Prerequisites accurate and complete
   - Example progression logical
   - Callbacks to previous episodes accurate
   - Spaced repetition matches curriculum plan

7. **Validate engagement quality** (CRITICAL for lessons):
   - Concrete examples (2-3 per major concept)
   - Analogies for mental models (1-2 per concept)
   - War stories or real scenarios (1-2 per lesson)
   - Varied sentence length and pacing
   - Rhetorical questions (2-3 total, not overused)
   - Active recall moments (1-2 per lesson)
   - Signposting and clear structure
   - Conversational tone (not academic)
   - No patronizing phrases ("obviously", "simply")
   - Authoritative but humble voice
   - **Calculate engagement score (aim for 8+/10)**

8. **Validate tone** against CLAUDE.md standards:
   - Authoritative but humble
   - Honest about trade-offs
   - Practical over academic
   - Skeptical of hype
   - Conversational and accessible

9. **Create validation report** with:
   - Summary of issues found
   - HIGH/MEDIUM/LOW priority categorization
   - Specific line numbers and suggested fixes
   - Pedagogical assessment
   - **Engagement quality score (X/10) with breakdown**
   - Overall status (READY/NEEDS FIXES/MAJOR ISSUES)
   - **If engagement score < 8, lesson is NOT READY**

10. **Save validation report**:
   - Location: `podcast-generator/validation-reports/courses/[course-slug]/lesson-[XX]-validation.md`
   - This is an internal working file, not published content
   - Include engagement score prominently at top of report

11. **Present report to user** and wait for fixes before proceeding to formatting

**Remember**: One inaccurate claim undermines the entire course. Better to remove a statistic than include one you can't verify. Educational content must be both accurate AND pedagogically sound AND engaging.
