---
name: Podcast Script
description: Convert approved story outline into natural Jordan/Alex dialogue for 12-15 minute podcast episodes. Requires outline exists first.
allowed-tools: Read, Write, Glob
---

# Podcast Script

Convert an approved story outline into natural, engaging dialogue between Jordan and Alex following Platform Engineering Playbook standards.

## When to Use This Skill

Use this skill when:
- User says: "Write podcast script", "Create episode dialogue"
- An approved outline exists in `docs/podcasts/outlines/`
- User has reviewed and approved the story structure

**CRITICAL**: This skill MUST verify an outline exists before writing. Never write a script without an outline.

## Episode Requirements

### Structure
- **Duration**: 12-15 minutes of dialogue
- **Format**: Natural conversation between Jordan and Alex
- **Tone**: Two experienced engineers having a strategic discussion
- **Audience**: Senior platform engineers (5+ years experience)

### Intro/Outro Handling
**Scripts DO NOT include intro or outro** - these are handled by pre-recorded MP3 files.

**DO**:
- ✅ Start with "Today we're diving into..."
- ✅ Preview 2-3 main topics
- ✅ End with practical takeaway or insight

**DON'T**:
- ❌ Welcome messages ("Welcome to the show")
- ❌ Host introductions ("I'm Jordan", "I'm Alex")
- ❌ Show descriptions ("This is the show where...")
- ❌ Thank yous or goodbyes ("Thanks for listening", "Until next time")
- ❌ Cold open hooks (dropping mid-conversation)

### Episode Sections

1. **Episode Introduction** (30-45s)
   - Direct preview of topics
   - Set context for why this matters now
   - Example: "Today we're diving into the AI platform engineering crisis..."

2. **Landscape Overview** (3-4 min)
   - Current state, market dynamics
   - Design philosophy evolution

3. **Technical Deep Dive** (4-5 min)
   - Compare 2-3 solutions
   - Engineering and business perspectives

4. **Underdogs & Specialists** (2-3 min)
   - Niche players, regional leaders
   - Emerging solutions

5. **Skills Evolution** (3-4 min)
   - What's table stakes
   - What's losing relevance
   - What's rising in importance

6. **Practical Wisdom** (2 min)
   - Architectural mistakes
   - Evaluation frameworks
   - Boring tech principle

7. **Closing Thoughts** (1-2 min)
   - Key insight, actionable takeaway
   - No formal signoff

## Conversational Style

### Voice Characteristics

**Jordan** (Speaker 1):
- Authoritative, slightly skeptical
- Asks probing questions
- Challenges assumptions
- Focuses on business context

**Alex** (Speaker 2):
- Technical depth, practical experience
- Shares production stories
- Connects dots between concepts
- Emphasizes trade-offs

### Natural Dialogue Techniques

**Building Momentum**:
```
Jordan: You mentioned X earlier...
Alex: Oh yeah, that's a perfect example of...
```

**Respectful Disagreement**:
```
Jordan: I'm not sure I fully agree with that approach...
Alex: How so?
Jordan: Well, when you factor in team size...
```

**Shared Discovery**:
```
Alex: Wait, they're doing WHAT with their pricing model?
Jordan: I know, right? It sounds crazy until you realize...
```

**Technical Storytelling**:
```
Alex: We saw this firsthand when our Kubernetes cluster...
Jordan: That's the thing people miss - in production, it's never that simple.
```

### What Makes Dialogue Natural

**DO**:
- Interrupt occasionally with "Wait, hold on..."
- Use contractions ("it's", "we're", "that's")
- Start sentences with "Yeah", "Right", "Exactly"
- Ask clarifying questions
- Reference earlier points: "Like you said about..."
- Show genuine surprise: "Wait, really?"
- Build on each other's ideas

**DON'T**:
- Take perfect turns without overlap
- Use formal academic language
- Make speeches (keep responses under 4-5 sentences)
- Agree on everything (boring!)
- Explain things the other person already knows

## Script Format

**File location**: `docs/podcasts/scripts/00XXX-episode-name.txt`

**Format** (use `Jordan:` and `Alex:`, NOT `Speaker 1:` and `Speaker 2:`):
```
Jordan: [First speaker's dialogue]

Alex: [Second speaker's dialogue]

Jordan: [Continuation...]
```

**CRITICAL**:
- Use `Jordan:` and `Alex:` (not Speaker 1/2)
- Leave blank line between speakers
- Write naturally WITHOUT SSML/pronunciation tags (added later)
- No stage directions or formatting instructions

## Episode Naming Convention

**Determine next episode number**:
1. Check `docs/podcasts/scripts/` for existing episodes
2. Find highest number (e.g., `00004-paas-showdown.txt`)
3. Increment: `00005-your-topic.txt`

**Filename format**: `00XXX-topic-name.txt`
- 5-digit prefix with leading zeros
- Lowercase, hyphen-separated
- Descriptive topic name

## Content Coverage

### Always Include

1. **Design Philosophy**
   - Original problems and solutions
   - Why things evolved this way

2. **Evolution**
   - How they've adapted to changing needs
   - What changed in market/technology

3. **Trade-offs**
   - What you give up for benefits
   - No silver bullets

4. **Operational Reality**
   - Production experience
   - What breaks at scale

5. **Team Impact**
   - Organizational effects
   - Hiring, skills, culture

6. **Future Direction**
   - Where technology is heading
   - What to watch for

### Always Avoid

- Basic 101 explanations
- Absolute statements ("X is always better")
- Marketing speak without data
- Installation/configuration guides
- Outdated information (>2 years old)

## Writing Process

### Step 1: Verify Outline Exists
```bash
# Check for outline file
ls -la docs/podcasts/outlines/00XXX-*-outline.md
```

If no outline exists, STOP and create outline first using the podcast-outline skill.

### Step 2: Review Outline Structure
- Understand the throughline
- Note emotional beats
- Identify callbacks
- Review supporting data

### Step 3: Write Section by Section

Follow the Act 1/2/3 structure from outline:
- Each act becomes 2-3 sections of dialogue
- Each section 2-4 minutes (roughly 300-600 words)
- Natural transitions between sections

### Step 4: Embed Story Elements

**Hook** (First 60 seconds):
```
Jordan: Today we're diving into [topic]. Here's the thing that's wild - [surprising statistic or provocative question].

Alex: Right, and what makes this urgent NOW is [recent change or market shift].
```

**Callbacks** (Throughout):
```
Jordan: Remember that statistic we opened with? Here's why it's happening...
```

**Payoff** (Closing):
```
Alex: So coming back to our original question about [opening hook], the answer is actually [insight from exploration].
```

### Step 5: Technical Depth Without Jargon

**Good example**:
```
Alex: Kubernetes gives you declarative infrastructure - you describe what you want, it figures out how to get there. That's powerful, but it means you need to understand its mental model.

Jordan: And that's the rub. Teams adopt it for horizontal scaling, but end up spending six months just learning the mental model.
```

**Bad example**:
```
Alex: Kubernetes uses a declarative API with controllers watching the etcd state store, reconciling actual state with desired state through control loops.

Jordan: Yes, the reconciliation loop pattern is fundamental to the operator framework.
```

### Step 6: Balance Perspectives

Avoid one speaker dominating. Rough balance:
- Jordan: 45-50% of dialogue
- Alex: 50-55% of dialogue

Each speaker should contribute unique insights, not just agree with the other.

## Quality Checklist

Before finalizing script:

**Story Structure**:
- [ ] Follows outline's Act 1/2/3 structure
- [ ] Hook in first 60 seconds
- [ ] Callbacks to opening themes
- [ ] Payoff delivers on promise
- [ ] Emotional beats land (recognition, surprise, empowerment)

**Dialogue Quality**:
- [ ] Sounds like two people talking (not a lecture)
- [ ] Natural interruptions and building
- [ ] Disagreement/debate on at least one point
- [ ] Contractions and casual language
- [ ] Questions and clarifications
- [ ] References to earlier points

**Content Depth**:
- [ ] Technical accuracy (verified in outline)
- [ ] Specific examples with numbers
- [ ] Trade-offs explored
- [ ] Multiple perspectives presented
- [ ] Actionable frameworks or insights

**Format**:
- [ ] Uses `Jordan:` and `Alex:` speaker labels
- [ ] 12-15 minutes estimated length (~2000-2500 words)
- [ ] No intro/outro content
- [ ] No SSML tags (added later)
- [ ] Saved to `docs/podcasts/scripts/00XXX-name.txt`

## Example Opening (Good vs Bad)

### ✅ GOOD
```
Jordan: Today we're diving into the twenty twenty-five PaaS landscape. Flightcontrol, Vercel, Railway, Render, Fly dot io—everyone's promising Heroku-like simplicity with cloud-scale performance. But which one actually delivers?

Alex: And more importantly, how do you justify spending four hundred dollars a month on a platform when AWS is "free"?

Jordan: Right, because it's never actually free once you factor in the hidden costs. We'll break down the real economics and give you a decision framework.

Alex: Let's start with what's driving this PaaS renaissance. Why are we seeing so many new players in twenty twenty-five when Heroku existed for over a decade?
```

### ❌ BAD
```
Jordan: Welcome to The Platform Engineering Playbook. I'm Jordan.

Alex: And I'm Alex. This is the show where we dissect the technologies, trends, and decisions that shape platform engineering at scale.

Jordan: Today we're talking about PaaS platforms.

Alex: Yes, PaaS stands for Platform as a Service. These are platforms that abstract away infrastructure complexity.

Jordan: Let's start by defining what we mean by PaaS.
```

## Example Closing (Good vs Bad)

### ✅ GOOD
```
Alex: So coming back to our opening question - how do you justify four hundred dollars a month to your CTO? You show them the spreadsheet. Engineer time, on-call burden, opportunity cost of not shipping features.

Jordan: The fundamentals of good engineering remain constant, even as the landscape evolves. Start with simplicity, prove the value, then scale to control as your needs grow.
```

### ❌ BAD
```
Alex: Well, I think we've covered everything about PaaS platforms today.

Jordan: Definitely a lot of great information. Thanks for listening to The Platform Engineering Playbook.

Alex: Don't forget to subscribe and leave us a review. We really appreciate it!

Jordan: Until next time, keep building thoughtfully.
```

---

## Instructions for Claude

When this skill is invoked:

1. **Verify outline exists**:
   ```bash
   ls -la docs/podcasts/outlines/
   ```
   If no outline, STOP and tell user to create outline first with podcast-outline skill.

2. **Read the outline carefully**:
   - Understand throughline
   - Note Act 1/2/3 structure
   - Identify emotional beats
   - Review supporting data

3. **Determine episode number**:
   - Check existing scripts in `docs/podcasts/scripts/`
   - Increment highest number

4. **Write dialogue section by section**:
   - Start with episode introduction (no welcome/intro)
   - Follow outline's act structure
   - Use natural conversation patterns
   - Embed story elements (hook, callbacks, payoff)

5. **Maintain voice consistency**:
   - Jordan: Skeptical, business-focused, probing questions
   - Alex: Technical depth, production stories, trade-offs

6. **Validate against checklist** (all items)

7. **Save to correct location**:
   `docs/podcasts/scripts/00XXX-topic-name.txt`

8. **Report to user**:
   - Episode number and filename
   - Estimated duration
   - Next step: Use podcast-validate skill to fact-check

**Remember**: The outline is your blueprint. Your job is to bring it to life with natural, engaging dialogue that teaches through story.
