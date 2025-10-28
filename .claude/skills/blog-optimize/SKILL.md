# Blog Optimize

Check and optimize blog posts for SEO (Search Engine Optimization) and AEO (AI Engine Optimization) to maximize discoverability through Google search and AI citations (ChatGPT, Perplexity, Claude, etc.).

## When to Use This Skill

Use this skill when:
- User says: "Optimize for SEO", "Check AEO compliance", "Prepare for publication"
- Blog post is written and validated
- Final check before publishing

**Prerequisites**: Complete blog post that has been validated (blog-validate skill used).

## SEO vs AEO

**SEO (Search Engine Optimization)**: Optimizing for Google/Bing search
**AEO (AI Engine Optimization)**: Optimizing for AI model citations (ChatGPT, Perplexity, Claude)

**Key Differences**:
- SEO: Keywords in titles/headers, meta descriptions, internal links
- AEO: Standalone sentences, FAQ schema, direct answers, specific data

**Both require**: Quality content, proper sources, clear structure

## The 12-Point Compliance Checklist

### Score Target: 10/12 minimum for publication

**1. Quick Answer/TL;DR Section** (REQUIRED)
- [ ] Present at top of post (before main content)
- [ ] Contains Problem, Solution, Key Stats, Timeline
- [ ] Standalone sentences (no pronouns)
- [ ] Specific numbers included

**2. FAQ Schema in Frontmatter** (REQUIRED)
- [ ] 5-10 questions minimum
- [ ] Questions match common searches
- [ ] Answers are 2-3 sentences, factual
- [ ] AI-friendly format (no pronouns)

**3. Statistics with Source Links** (REQUIRED)
- [ ] 2+ statistics minimum
- [ ] Every stat has click-through source link
- [ ] Sources are primary (not secondary)
- [ ] Numbers are specific (not vague)

**4. Comparison Table** (If Applicable)
- [ ] Used for tool/approach comparisons
- [ ] Includes sources column
- [ ] Specific data (not vague)
- [ ] Helps decision-making

**5. Date/Year Signals** (REQUIRED)
- [ ] datePublished in frontmatter
- [ ] dateModified in frontmatter
- [ ] Year in title if timely content "(2025 Guide)"
- [ ] Data tables show date ranges

**6. Key Takeaway Boxes** (REQUIRED)
- [ ] 2-7 boxes throughout (💡 emoji)
- [ ] Positioned after major insights
- [ ] 2-3 sentences each
- [ ] Standalone, no pronouns

**7. Direct Answer Format** (REQUIRED)
- [ ] No "as mentioned above" references
- [ ] Standalone sentences throughout
- [ ] Each paragraph self-contained
- [ ] AI can cite any sentence independently

**8. Expert Quotes or Authoritative References**
- [ ] 2-4 quotes with attribution
- [ ] OR links to authoritative sources
- [ ] Adds credibility

**9. Numbered How-To Steps or Decision Framework** (REQUIRED)
- [ ] Step-by-step implementation OR
- [ ] Decision tree/framework
- [ ] Actionable and specific
- [ ] Clear outcomes

**10. Standalone Sentences** (REQUIRED)
- [ ] Avoid pronouns in key insights
- [ ] Each major point is self-contained
- [ ] No dangling references
- [ ] AI-citation ready

**11. Decision Framework** (REQUIRED)
- [ ] "Use X when..., Use Y when..." format
- [ ] Clear criteria and thresholds
- [ ] Specific conditions
- [ ] Actionable guidance

**12. Internal Links to Related Content** (REQUIRED)
- [ ] 5+ internal links minimum
- [ ] Links to related blog posts
- [ ] Links to podcast episodes
- [ ] Links to technical pages
- [ ] Natural placement

## Optimization Workflow

### Phase 1: Run Compliance Check

Go through the 12-point checklist systematically:

```markdown
## SEO/AEO Compliance Report

### Checklist Results: [X]/12

#### ✅ PASS (X items)
- [1] Quick Answer section present and AI-friendly
- [2] FAQ schema with 8 questions in frontmatter
[... list all passing items]

#### ❌ FAIL (Y items)
- [6] Only 1 Key Takeaway box (need 2-7)
  - Location: Missing throughout post
  - Fix: Add 4-5 boxes after major insights

- [12] Only 2 internal links (need 5+)
  - Location: Throughout post
  - Fix: Add links to related content

#### Status: NEEDS OPTIMIZATION (Y items to fix)
```

### Phase 2: Fix Failing Items

**For each failing item, provide specific fixes:**

**Example - Adding Key Takeaways**:
```markdown
BEFORE (no Key Takeaway):
Platform teams fail when they lack product managers. Only 33% have PMs despite 52% saying they're crucial.

AFTER (with Key Takeaway):
Platform teams fail when they lack product managers. Only 33% have PMs despite 52% saying they're crucial.

> **💡 Key Takeaway**
>
> Only 33% of platform teams have product managers, yet 52% say PMs are crucial—this 19-point gap predicts failure better than any technology choice. Teams with PMs are 3× more likely to achieve over 50% adoption.
```

**Example - Adding Internal Links**:
```markdown
BEFORE:
Platform engineering requires careful economic analysis.

AFTER:
Platform engineering requires careful economic analysis. See our [Platform Economics](/blog/platform-engineering-economics-hidden-costs-roi) deep dive for ROI calculations.
```

**Example - Fixing Pronouns (AEO)**:
```markdown
BEFORE:
As mentioned above, this is why platforms fail.

AFTER:
Platforms fail when teams lack product managers—only 33% have PMs despite 52% saying they're crucial.
```

### Phase 3: Optimize Frontmatter

**Title Optimization** (50-60 characters):
- Include primary keyword
- Add year if timely content
- Compelling and specific
- Avoid clickbait

**Good Title**: "Why 70% of Platform Engineering Teams Fail (And the 5 Metrics That Predict Success)"
**Bad Title**: "Platform Engineering Problems"

**Description** (150-160 characters):
- Include key stats
- Mention value/benefit
- Natural language (not keyword stuffing)
- Compelling hook

**Good Description**: "45% of platform engineering teams are disbanded within 18 months. Learn the 7 failure modes backed by research, real examples, and the 5 predictive metrics for success."

**Keywords** (8-12 total):
- Primary keyword first
- Long-tail variations
- Question-based keywords
- Related technical terms

**FAQ Schema**:
- 5-10 questions minimum
- Match Google "People also ask"
- Factual, data-driven answers
- Standalone format

### Phase 4: Content Structure Optimization

**Check section headers**:
- [ ] Include keywords naturally
- [ ] Clear and descriptive
- [ ] Hierarchy (H2, H3, H4)
- [ ] Scannable

**Check paragraph length**:
- [ ] No walls of text (200+ words)
- [ ] Break up with subheadings
- [ ] Use bullet points
- [ ] Add tables for data

**Check scannability**:
- [ ] Bold key terms sparingly
- [ ] Use lists for steps/items
- [ ] Tables for comparisons
- [ ] White space for readability

### Phase 5: AI Citation Optimization

**Make every key insight standalone**:

Bad (pronoun-heavy):
> "This is why it fails. As we saw earlier, they don't have the metrics."

Good (standalone):
> "Platform teams fail when they lack product managers. Only 33% have PMs despite 52% saying they're crucial."

**Add specific numbers everywhere**:

Bad: "Most teams fail"
Good: "70% of platform teams fail to deliver impact"

Bad: "Significantly improved"
Good: "Reduced deployment time from 45 minutes to 6 minutes"

**Structure for AI extraction**:
- Lead with key fact
- Follow with supporting data
- Include source
- Make self-contained

## Optimization Report Format

```markdown
# SEO/AEO Optimization Report: [Post Title]

## Compliance Score: [X]/12

**Status**: READY FOR PUBLICATION | NEEDS OPTIMIZATION

---

## ✅ Passing Items ([X]/12)

1. **Quick Answer Section**: Present and AI-friendly
2. **FAQ Schema**: 8 questions in frontmatter, all factual
3. **Statistics**: 12 stats with source links
[... continue]

---

## ❌ Failing Items ([Y]/12)

### 6. Key Takeaway Boxes (REQUIRED - MISSING)
**Issue**: Only 1 box found, need 2-7
**Fix**: Add boxes after these sections:
- Line 234: After "The Investigation" section
- Line 456: After framework presentation
- Line 678: After decision tree
- Line 890: Before conclusion

**Suggested Content**:
```
> **💡 Key Takeaway**
>
> [Specific insight with data]
```

### 12. Internal Links (REQUIRED - INSUFFICIENT)
**Issue**: Only 2 links, need 5+ minimum
**Fix**: Add links to:
- Line 123: Link to /blog/platform-economics
- Line 234: Link to /podcasts/00004-paas-showdown
- Line 456: Link to /technical/kubernetes
[... 2 more suggestions]

---

## Recommendations

### HIGH PRIORITY (Must fix)
- [ ] Add 4-5 Key Takeaway boxes (locations specified above)
- [ ] Add 3+ internal links (suggestions above)

### MEDIUM PRIORITY (Improves ranking)
- [ ] Add year to title: "...(2025 Guide)"
- [ ] Add 2 more FAQ questions to frontmatter

### LOW PRIORITY (Nice to have)
- [ ] Consider adding comparison table at line 345
- [ ] Add expert quote at line 567

---

## After Optimization

Re-run this skill to verify all items pass.
Target: 10/12 minimum for publication.
```

## Instructions for Claude

When this skill is invoked:

1. **Read blog post frontmatter and content**
2. **Run 12-point checklist systematically**
3. **Score each item**: Pass/Fail
4. **Calculate total score**: X/12
5. **For each failing item**:
   - Identify specific issue
   - Provide line numbers
   - Suggest concrete fixes
   - Show before/after examples
6. **Prioritize fixes**: High/Medium/Low
7. **Create optimization report**
8. **Determine status**:
   - 10-12/12: READY FOR PUBLICATION
   - 8-9/12: MINOR OPTIMIZATION NEEDED
   - <8/12: NEEDS SIGNIFICANT WORK
9. **Report to user**:
   - Score: X/12
   - Y items need fixing
   - Specific action items
   - Next step: Make fixes and re-run, or publish if ready

**Remember**: AEO is increasingly important as AI tools become primary search interfaces. Every sentence should be quotable and attributable.
