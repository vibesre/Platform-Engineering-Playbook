---
name: Podcast Validate
description: Fact-check podcast scripts for accuracy, verify sources, check for marketing speak vs data, and ensure technical correctness.
allowed-tools: Read, WebFetch, Grep, Glob
---

# Podcast Validate

Verify the accuracy and quality of podcast scripts before formatting and publishing. The Platform Engineering Playbook's reputation depends on technical correctness and trustworthy information.

## When to Use This Skill

Use this skill when:
- User says: "Validate podcast script", "Fact-check episode"
- A script exists in `docs/podcasts/scripts/` that needs verification
- Before moving to formatting/publishing stages

## Core Validation Principles

### Why This Matters

**One inaccurate statistic destroys trust.**

The podcast targets senior engineers who:
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

**Example Validation**:
```
Script: "Flightcontrol starts at three hundred ninety-seven dollars per month"

✅ VERIFY:
- Source: flightcontrol.com/pricing (checked 2025-10-20)
- Tier: Base plan (not including enterprise)
- Includes: 10 deployments, basic support
- Caveats: Additional environments cost extra

✓ VALID - Add note: "as of October 2025"
```

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

**Example Validation**:
```
Script: "One team reduced deployment time from forty-five minutes to six minutes"

✅ VERIFY:
- Source: [Engineering blog post] or mark as [hypothetical example]
- Context: Team size, tech stack, what they changed
- Timeline: Over what period?
- Realistic: Does the improvement make sense?

⚠️ ISSUE - If no source, change to: "Teams commonly report reducing deployment time from 45 minutes to under 10 minutes when adopting platform X"
```

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

**Example Validation**:
```
Script: "Vercel supports automatic preview environments for every pull request"

✅ VERIFY:
- Source: vercel.com/docs/deployments/preview-deployments
- Availability: ✓ Generally available
- Limitations: Some frameworks require config
- Tiers: ✓ Available on all plans

✓ VALID - Standard feature, works as described
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

### Step 2: Verify Each Claim

Use allowed tools:
- **WebFetch**: Check vendor websites, official docs
- **Read**: Check internal research notes, outline sources
- **Grep**: Search codebase for related examples

Create validation notes:
```markdown
## Validation Report: Episode 00XXX

### Statistics
1. "85% of organizations..." ✓ VERIFIED [source link]
2. "Costs 30-40% less..." ⚠️ NEEDS SOURCE

### Technical Claims
1. "Kubernetes uses controllers..." ✓ VERIFIED (k8s docs)
2. "Supports automatic scaling..." ⚠️ CLARIFY (needs conditions)

### Pricing
1. "Flightcontrol $397/month" ✓ VERIFIED (as of 2025-10-20)
2. "AWS free tier" ⚠️ INCOMPLETE (has limitations)

### Issues Found: 3
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
- [ ] Accurate acronyms (TTS not "text to speech" in dialogue)
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

**Target Audience Check**:
- [ ] Appropriate depth for senior engineers
- [ ] No basic 101 content
- [ ] Respects reader intelligence
- [ ] Actionable insights

## Output Format

Produce a **Validation Report**:

```markdown
# Validation Report: Episode 00XXX - [Title]

**Validated by**: Claude (Podcast Validate Skill)
**Date**: 2025-10-20
**Script Location**: docs/podcasts/scripts/00XXX-name.txt

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

## Pricing Data Verified
1. ✅ Flightcontrol $397/month - Verified 2025-10-20 at flightcontrol.com
2. ⚠️ "AWS free tier" - CLARIFY: Has usage limits, need to mention

## Issues Found

### HIGH Priority (Must Fix)
1. **Line 47**: "Studies show 50% improvement" - No source provided
   - **Fix**: Add source or remove claim

2. **Line 89**: "Always use X over Y" - Too absolute
   - **Fix**: Add context: "For most teams, X is better when..."

### MEDIUM Priority (Should Fix)
1. **Line 23**: Outdated pricing from 2024
   - **Fix**: Verify current pricing or note date

2. **Line 112**: Technical term needs clarification
   - **Fix**: Add brief explanation for broader audience

### LOW Priority (Nice to Have)
1. **Line 5**: Could use more specific number
   - **Suggestion**: "Many teams" → "In surveys of 500+ teams"

## Marketing Speak Detected

1. **Line 34**: "Revolutionary approach" - NO DATA
   - **Fix**: "Approach that reduced deployment time by 60%"

2. **Line 78**: "Game-changing platform"
   - **Fix**: Specific benefits instead of hyperbole

## Recommendations

### Before Formatting
- [ ] Fix all HIGH priority issues
- [ ] Address MEDIUM priority issues
- [ ] Remove/replace marketing speak

### Before Publishing
- [ ] Verify all sources still accessible
- [ ] Check pronunciation tags on technical terms
- [ ] Ensure consistent terminology throughout

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

---

## Instructions for Claude

When this skill is invoked:

1. **Locate script file**:
   ```bash
   ls -la docs/podcasts/scripts/
   ```

2. **Read script completely**, marking claims to verify:
   - [S] Statistics
   - [T] Technical claims
   - [P] Pricing
   - [C] Case studies
   - [F] Features

3. **Verify each claim** using allowed tools:
   - WebFetch vendor sites for pricing, docs
   - Read outline/research for source notes
   - Cross-reference official documentation

4. **Check for red flags**:
   - Marketing speak without data
   - Absolute statements
   - Outdated information
   - Unsourced statistics

5. **Validate tone** against CLAUDE.md standards:
   - Authoritative but humble
   - Honest about trade-offs
   - Practical over academic
   - Skeptical of hype

6. **Create validation report** with:
   - Summary of issues found
   - HIGH/MEDIUM/LOW priority categorization
   - Specific line numbers and suggested fixes
   - Overall status (READY/NEEDS FIXES/MAJOR ISSUES)

7. **Save validation report**:
   - Location: `podcast-generator/validation-reports/[episode-number]-validation.md`
   - This is an internal working file, not published content

8. **Present report to user** and wait for fixes before proceeding to formatting

**Remember**: One inaccurate claim undermines the entire podcast. Better to remove a statistic than include one you can't verify.
