# Reel Script Generation Skill

## Purpose

Generate 3-5 engaging short-form "reel" style educational videos (30-60 seconds) from podcast episode scripts. Each reel teaches ONE core concept optimized for maximum attention, retention, and engagement.

**Target Platforms**: YouTube Shorts, Instagram Reels, TikTok
**Format**: Single presenter (vertical video optimized)
**Duration**: 30-60 seconds (aim for 45s sweet spot)
**Goal**: Capture attention in 3s, teach concept in 30s, create desire to learn more

## When to Use This Skill

Use this skill AFTER a podcast script has been written and validated:
1. Main episode script exists in `docs/podcasts/scripts/00XXX-episode-name.txt`
2. Episode covers multiple concepts worth extracting
3. Goal is to create social media content for discovery/promotion

## Workflow

### Phase 1: Identify Core Concepts (Research)

**Read the main episode script** and extract 3-5 concepts that:
- Are self-contained (teachable in isolation)
- Have high practical value (engineers can use immediately)
- Include surprising insights or counterintuitive facts
- Can be explained with concrete examples
- Challenge common assumptions

**Concept Selection Criteria**:
- ✅ Specific and actionable (not abstract)
- ✅ Contains a "hook" moment (surprising stat, bold claim, common mistake)
- ✅ Has a clear before/after or problem/solution
- ✅ Relates to pain points senior engineers face
- ✅ Can be explained in 30-45 seconds

**Example Concepts from Episode "PaaS Showdown"**:
1. "Why AWS Elastic Beanstalk costs 3x more than you think"
2. "The hidden cost of Heroku's convenience"
3. "Render vs Railway: The 10-second deployment difference"
4. "Why platform engineers choose boring tools"
5. "The $20K mistake most teams make with PaaS"

**Output**: List 3-5 concepts with working titles

### Phase 2: Create Reel Outlines

For each concept, create a structured outline:

```markdown
## Reel 01: [Concept Title]

**Target Duration**: 45 seconds
**Core Insight**: [One sentence - the main takeaway]
**Hook Type**: [Surprising stat / Bold claim / Common mistake / Question]

### Structure:
1. **Hook (0-3s)**: [Attention grabber]
2. **Setup (3-10s)**: [Context/problem]
3. **Insight (10-35s)**: [Core teaching moment]
4. **Payoff (35-45s)**: [Actionable takeaway + call-to-action]

### Visual Cues:
- Text overlays: [Key numbers, terms]
- B-roll suggestions: [What to show]
- Pacing notes: [Where to speed up/slow down]
```

**Hook Types** (Pick the strongest):
1. **Surprising Statistic**: "75% of platform teams waste $50K/year on this"
2. **Bold Claim**: "Your PaaS is costing you 10x what it should"
3. **Common Mistake**: "You're probably configuring Kubernetes wrong"
4. **Provocative Question**: "Why do senior engineers avoid the 'best' tools?"
5. **Pattern Interrupt**: "Stop using Docker. Here's why—"
6. **Before/After**: "Our deploys took 45 minutes. Now? 90 seconds."

### Phase 3: Write Reel Scripts

**Format** (Single Presenter):
```
[HOOK - Energetic, direct to camera]
Text overlay should show statistic

Most platform teams waste $50,000 a year on their PaaS. Here's why.

[SETUP - Establish the problem]
When you pick Heroku for "simplicity," you're actually buying four hidden costs.

[INSIGHT - Core teaching, specific examples]
First, compute markup: a 2GB dyno costs $50/month, but the same EC2 instance? $15.

Second, scaling tax: every additional dyno adds that markup. At 20 dynos, you're paying $700/month for $300 of infrastructure.

Third, add-ons: databases, Redis, monitoring—each costs 2-3x what AWS charges.

Fourth, the migration cliff: once you hit 50 dynos, rebuilding on ECS takes 6 months and $200K.

[PAYOFF - Actionable takeaway]
Run this calculation before your next AWS bill: [current Heroku cost] times 3. That's your annual waste.

Full breakdown in the description. 👇
```

**Script Requirements**:
- ✅ Hook in first 3 seconds (visual + verbal)
- ✅ Use "you" language (direct address)
- ✅ Specific numbers (not "expensive" but "$50K/year")
- ✅ Concrete examples (not abstractions)
- ✅ Pattern interrupts every 10-15s (pacing change, reveal, question)
- ✅ Ends with clear action or link to full content
- ✅ Target 45 seconds (110-140 words)

**Visual Annotations** (Optional but recommended):
```
[TEXT OVERLAY: "$50,000 WASTED"]
[SHOW: Heroku pricing page]
[EMPHASIZE: "2-3x markup"]
[TRANSITION: Fast cut to next point]
```

### Phase 4: Validate Scripts

Run each script through these checks:

#### Engagement Validation

**Hook Strength** (First 3 seconds):
- [ ] Contains specific number or surprising fact
- [ ] Creates curiosity gap (promises valuable info)
- [ ] Speaks to viewer's pain point
- [ ] Visually compelling (text overlay specified)

**Retention Optimization**:
- [ ] Pattern interrupt every 10-15 seconds
- [ ] No sentence longer than 12 seconds
- [ ] Uses "you" language (3+ times)
- [ ] Includes open loop (question or promise)
- [ ] Payoff delivers on hook's promise

**Pacing Check**:
- [ ] Reads naturally when spoken fast
- [ ] No tongue-twisters or complex phrases
- [ ] Pauses marked for emphasis
- [ ] Timing: 30-60 seconds (target 45s)

#### Educational Validation

**Learning Effectiveness**:
- [ ] Teaches ONE concept (not 2 or 3)
- [ ] Uses concrete example (not abstract)
- [ ] Includes specific numbers/data
- [ ] Before/after comparison (if applicable)
- [ ] Actionable takeaway (can apply immediately)

**Accuracy**:
- [ ] Facts verified (pricing, stats, claims)
- [ ] Technical details correct
- [ ] Source cited (if using stat)
- [ ] No oversimplification that creates misconceptions

**Clarity for Target Audience**:
- [ ] Assumes senior engineer knowledge (5+ years)
- [ ] No basic explanations (Docker, Kubernetes, etc.)
- [ ] Jargon used correctly
- [ ] Respects audience intelligence

#### Platform Optimization

**Vertical Video Format**:
- [ ] Works without horizontal visuals
- [ ] Text overlays specified for key points
- [ ] No reliance on wide-screen graphics

**Call-to-Action**:
- [ ] Clear next step (link in description, full episode, etc.)
- [ ] Easy to follow (one action, not three)
- [ ] Creates desire for more depth

## File Structure

**Location**: `podcast-generator/episodes/00XXX-episode-name/reels/`

**Files**:
```
podcast-generator/episodes/00004-paas-showdown-episode/reels/
├── concepts.md                          # Phase 1 output: concept list
├── reel-01-heroku-hidden-costs.txt     # Final script (ready for TTS)
├── reel-02-aws-beanstalk-markup.txt
├── reel-03-render-vs-railway.txt
├── reel-04-boring-tools-win.txt
└── reel-05-paas-migration-cliff.txt
```

**Naming Convention**: `reel-XX-concept-slug.txt`

**Why This Location**:
- Co-located with episode audio/video files
- Easy to find all episode-related content
- Excluded from git (in episodes/ directory)

## Reel Script Template

Use this template for consistency:

```
# Reel XX: [Concept Title]

**Duration**: 45s (target)
**Hook Type**: [Surprising stat / Bold claim / etc.]
**Core Insight**: [One sentence]

---

[HOOK - First 3 seconds]
[TEXT OVERLAY: Key stat or claim]

[Opening line with hook]

[SETUP - Seconds 3-10]

[Context or problem statement]

[INSIGHT - Seconds 10-35]

[Core teaching with specific examples and numbers]
[Break into 2-4 chunks, each 8-12 seconds]

[Pattern interrupt or reveal]

[PAYOFF - Seconds 35-45]

[Actionable takeaway]
[Call-to-action to full content]

---

**Visual Notes**:
- Text overlays: [List key numbers/terms to show]
- B-roll: [Suggest what to show]
- Pacing: [Fast/medium/slow sections]

**Validation**:
- Word count: XXX words (~2.5 words/second = 110-140 words target)
- Hook strength: [Rate 1-10]
- Retention: Pattern interrupts at: Xs, Xs, Xs
- CTA clarity: [Yes/No]
```

## Example: High-Quality Reel Script

```
# Reel 01: The Heroku Hidden Cost Trap

**Duration**: 42s
**Hook Type**: Surprising statistic
**Core Insight**: Heroku's convenience markup costs platform teams $50K+/year in hidden fees

---

[HOOK - Energetic, direct]
[TEXT OVERLAY: "$50,000 WASTED ANNUALLY"]

Platform teams waste fifty grand a year on Heroku. Here's the breakdown.

[SETUP]

You picked Heroku for simplicity. But you're paying for four hidden costs.

[INSIGHT - Specific examples]

First: compute markup. A 2GB dyno? $50 a month. Same EC2 instance? Fifteen bucks.

Second: scaling tax. Twenty dynos means you're paying $700 for $300 of infrastructure.

[Pattern interrupt - pause, emphasis]

Third: add-ons. Postgres, Redis, monitoring—each costs two to three times AWS pricing.

Fourth: migration cliff. Hit 50 dynos, you'll spend six months and $200K rebuilding on ECS.

[PAYOFF]

[TEXT OVERLAY: "YOUR COST × 3 = ANNUAL WASTE"]

Take your current Heroku bill, multiply by three. That's what you're losing every year.

Full cost breakdown and alternatives—link in description.

---

**Visual Notes**:
- Text overlays: "$50,000", "2-3x markup", "YOUR COST × 3"
- B-roll: Heroku pricing page, cost comparison table, calculator
- Pacing: Fast delivery, pause at "migration cliff"

**Validation**:
- Word count: 127 words (✓ 42s at 3 words/sec)
- Hook strength: 9/10 (specific dollar amount)
- Retention: Interrupts at 10s, 23s, 35s (✓)
- CTA clarity: Yes (clear action)
```

## Production Checklist

After writing all reel scripts:

### Content Quality
- [ ] 3-5 concepts extracted from main episode
- [ ] Each reel teaches ONE specific concept
- [ ] All facts verified and sourced
- [ ] Technical accuracy validated
- [ ] No oversimplifications that mislead

### Engagement Optimization
- [ ] Every hook tested for strength (8+/10)
- [ ] Pattern interrupts every 10-15 seconds
- [ ] Specific numbers used (not vague claims)
- [ ] Direct "you" language throughout
- [ ] Visual annotations specified

### Format Compliance
- [ ] Duration: 30-60s (target 45s)
- [ ] Word count: 110-140 words per reel
- [ ] Single presenter format
- [ ] Works for vertical video (9:16)
- [ ] CTA in every script

### File Organization
- [ ] Saved to `podcast-generator/episodes/00XXX-name/reels/`
- [ ] Naming: `reel-XX-concept-slug.txt`
- [ ] concepts.md lists all concepts with rationale
- [ ] Ready for TTS generation (clean format)

## Educational Best Practices for Short-Form

### Attention Optimization (The "3-Second Rule")

**First 3 seconds determine 80% of completion rate**:
- Use specific numbers (not "a lot" but "$50K")
- Create visual contrast (text overlay + verbal)
- Trigger curiosity gap (promise valuable info)
- Speak to specific pain point

**Bad Hook**: "Today I'm going to talk about PaaS costs"
**Good Hook**: "You're wasting $50,000 a year on Heroku. Here's why."

### Retention Optimization (Pattern Interrupts)

**Pattern interrupts prevent drop-off**:
- Every 10-15 seconds, change something:
  - Pacing (speed up or slow down)
  - Visual (new text overlay, cut, zoom)
  - Revelation (surprising fact, counterintuitive claim)
  - Question (engage active thinking)

**Example Pattern Interrupt Sequence**:
- 0-3s: Hook with stat
- 10s: Reveal first hidden cost (interrupt)
- 20s: Bold claim: "This is the real killer—" (interrupt)
- 30s: Question: "Want to know the worst part?" (interrupt)
- 40s: Payoff with action (interrupt)

### Learning Effectiveness (Single Concept Focus)

**One reel = One concept** (not 2 or 3):
- ✅ "Why Heroku costs 3x more than you think" (ONE concept)
- ❌ "PaaS pricing, features, and when to use them" (THREE concepts)

**Concrete over Abstract**:
- ✅ "$50/month dyno vs $15 EC2 instance" (concrete)
- ❌ "Heroku has pricing overhead" (abstract)

**Active Recall Techniques**:
- Ask questions before revealing answers
- Use "pause and think" moments
- Create mental models (before/after, good/bad)
- Provide frameworks (not just facts)

### The Hook-Setup-Insight-Payoff Framework

Every reel follows this structure:

```
1. HOOK (0-3s): Grab attention
   - Surprising stat, bold claim, or provocative question
   - Creates curiosity gap

2. SETUP (3-10s): Establish context
   - Why this matters (pain point)
   - What we're solving

3. INSIGHT (10-35s): Core teaching
   - Specific examples with numbers
   - Pattern interrupts every 10-15s
   - No more than 3-4 sub-points

4. PAYOFF (35-45s): Actionable takeaway
   - Clear action or mental model
   - Call-to-action for more depth
```

## Common Mistakes to Avoid

### ❌ Mistake 1: Weak Hook
**Problem**: "Let me tell you about PaaS pricing"
**Fix**: "Your PaaS costs 5x more than it should. Here's proof."

### ❌ Mistake 2: Too Many Concepts
**Problem**: Teaching PaaS pricing, features, and migration in one reel
**Fix**: Pick ONE (e.g., only pricing) and go deep

### ❌ Mistake 3: Abstract Language
**Problem**: "Heroku has cost implications"
**Fix**: "$50,000 annual waste for a 20-dyno setup"

### ❌ Mistake 4: No Pattern Interrupts
**Problem**: Monotone delivery for 45 seconds
**Fix**: Change pacing, reveal, or ask question every 10-15s

### ❌ Mistake 5: Weak Payoff
**Problem**: "So yeah, that's PaaS costs. Thanks for watching."
**Fix**: "Multiply your Heroku bill by 3. That's your annual waste. Calculator in description."

### ❌ Mistake 6: Wrong Duration
**Problem**: 90-second reel trying to cover too much
**Fix**: Cut to 45s, focus on ONE specific aspect

### ❌ Mistake 7: No Visual Cues
**Problem**: Script has no text overlay notes
**Fix**: Mark every key number for visual emphasis

## Advanced Techniques

### Open Loops (Curiosity Gaps)

Create questions that only get answered by watching full episode:
- "The fourth hidden cost is the killer—I'll explain in the full episode"
- "Wait until you see what happens at 50 dynos"
- "There's one exception to this rule—link in description"

### The "Pattern Break" Hook

Start mid-thought or mid-action:
- "—so that's when our AWS bill tripled. Here's what we learned."
- "Stop. Right now. If you're using Heroku for this, you're wasting money."

### The "You're Probably Wrong" Frame

Challenge assumptions directly:
- "You think Kubernetes is complex? Wait until you see Heroku's add-on dependency graph."
- "Everyone says Render is cheap. Let me show you the actual math."

### The Specific Number Stack

Pile on specifics for credibility:
- "$50/month dyno, $15 EC2, $35 markup, times 20 instances, equals $700 wasted monthly, $8,400 annually—and that's just compute."

## Integration with Main Episode

**Reels are discovery vehicles**, not replacements:

1. **Extract vs Summarize**: Don't summarize the episode—extract ONE surprising insight
2. **Tease Depth**: Reference the full episode for complete context
3. **Stand Alone**: Each reel should be valuable without watching the episode
4. **Cross-Link**: CTA drives to full episode for those who want more

**Example CTA Progression**:
- Reel 1: "Full PaaS cost breakdown—link in description"
- Reel 2: "Want to know which PaaS is worth it? Full episode drops tomorrow"
- Reel 3: "See the complete analysis in today's episode—link in bio"

## Quality Standards

### Minimum Viable Reel (Must Have)
- ✅ 30-60 second duration
- ✅ Strong hook (specific number or bold claim)
- ✅ ONE core concept
- ✅ Specific examples (not abstractions)
- ✅ Clear CTA

### High-Quality Reel (Should Have)
- ✅ 40-50 second sweet spot
- ✅ Hook with 9+/10 strength
- ✅ Pattern interrupts every 10-15s
- ✅ Visual annotations specified
- ✅ Before/after or problem/solution frame
- ✅ Actionable takeaway

### Exceptional Reel (Nice to Have)
- ✅ 42-48 second optimization
- ✅ Hook that could go viral (10/10)
- ✅ Open loop to full episode
- ✅ Challenges common assumption
- ✅ Creates shareable mental model
- ✅ Ends with "aha!" moment

## Next Steps After Script Creation

1. **Validate**: Run through all checklist items
2. **TTS Generation**: Use Autonoe voice (0.95x speed for clarity)
3. **Video Production**: Add text overlays, B-roll, pacing cuts
4. **A/B Testing**: Try different hooks for same concept
5. **Iterate**: Analyze completion rates, adjust future scripts

---

**Related Skills**:
- **podcast-script**: Create the main episode first
- **podcast-validate**: Validate facts before creating reels
- **lesson-script**: Single presenter format (similar structure)

**Remember**: The goal is **not** to teach everything—it's to teach ONE thing so well that viewers want to learn more.
