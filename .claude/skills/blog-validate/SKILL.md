# Blog Validate

Fact-check blog post content for accuracy, verify sources, check for marketing speak vs data, ensure technical correctness, and validate that all claims are properly sourced.

## When to Use This Skill

Use this skill when:
- User says: "Validate the blog post", "Fact-check the content"
- Blog post draft is complete (blog-write skill used)
- Before publishing or optimizing for SEO

**Prerequisites**: Complete blog post draft with sources cited.

## Why Validation Matters

**CRITICAL**: One inaccurate statistic destroys trust. The Platform Engineering Playbook's reputation depends on accuracy and trustworthiness.

**Validation catches**:
- Incorrect statistics (wrong numbers, outdated data)
- Misattributed quotes or sources
- Broken or incorrect source links
- Technical inaccuracies
- Marketing claims without data backing
- Outdated pricing or feature information

## Validation Checklist

### 1. Statistics Verification

**For EVERY statistic in the blog post**:
- [ ] Find the original source (not secondary reporting)
- [ ] Verify the exact number matches
- [ ] Check the date (mark if >1 year old)
- [ ] Verify context (stat not taken out of context)
- [ ] Confirm source link works and goes to correct page

**Example**:
```
Claim: "70% of platform teams fail"
✓ Source link works: https://example.com/report
✓ Exact stat found on page 12
✓ Date: December 2024 (current)
✓ Context matches: failure defined as "disbanded within 18 months"
Status: VERIFIED
```

### 2. Quote Verification

**For EVERY quote**:
- [ ] Confirm exact wording (no paraphrasing marked as quote)
- [ ] Verify attribution (correct person/organization)
- [ ] Check context (not misleading)
- [ ] Source link provided and working

### 3. Technical Claims

**For technical statements**:
- [ ] Architecture descriptions match official docs
- [ ] Feature availability verified (current version)
- [ ] Compatibility claims correct
- [ ] Performance numbers include test conditions
- [ ] Security claims current (vulnerabilities change)

### 4. Pricing & Features

**For cost/feature claims**:
- [ ] Check vendor website (not blog posts)
- [ ] Note date checked (pricing changes frequently)
- [ ] Verify tier/plan details
- [ ] Confirm feature availability

### 5. Source Quality Check

**For EVERY source**:
- [ ] Link works (not 404)
- [ ] Goes to claimed content
- [ ] Source is authoritative
- [ ] Not paywalled (or note if is)
- [ ] Publication date visible

## Verification Process

### Step 1: Extract All Claims

Create a list of every verifiable claim:

```markdown
## Claims to Verify

### Statistics
1. "70% of platform teams fail" - Line 45 - Source: [Link]
2. "45% disbanded within 18 months" - Line 47 - Source: [Link]
[... continue for all stats]

### Technical Claims
1. "Backstage uses PostgreSQL" - Line 156 - Source: [Docs]
2. "Requires Kubernetes 1.24+" - Line 203 - Source: [Docs]

### Pricing
1. "Flightcontrol $397/mo" - Line 89 - Source: [Pricing page]
2. "Vercel $0-20/mo" - Line 91 - Source: [Pricing page]

### Quotes
1. "We had the technology..." - CEO quote - Line 32 - Source: [Article]
```

### Step 2: Verify Each Claim

For each claim:
1. Click the source link
2. Find the exact claim on the page
3. Verify number/fact matches
4. Check date
5. Mark status: ✅ VERIFIED | ❌ INCORRECT | ⚠️ NEEDS UPDATE

### Step 3: Check for Common Mistakes

**Numbers without sources**:
```bash
grep -E "[0-9]+%" blog/YYYY-MM-DD-slug.md | grep -v "source\|http"
```

**Vague claims** (flag for data):
- "significantly improved"
- "dramatically increased"  
- "much better than"
- "industry-leading"

**Marketing jargon without backing**:
- "revolutionary"
- "game-changing"
- "perfect solution"
- "transforms everything"

### Step 4: Technical Accuracy Review

**Test code examples** (if any):
```bash
# Actually run the code
# Verify it works as described
```

**Verify version compatibility**:
- Check current versions
- Test compatibility claims
- Update if outdated

**Cross-reference official docs**:
- Architecture descriptions
- Feature lists
- API behavior

## Validation Report Format

```markdown
# Validation Report: [Blog Post Title]

## Summary
- **Total Claims Checked**: [X]
- **Verified**: [Y]
- **Incorrect**: [Z]
- **Needs Update**: [N]
- **Status**: READY FOR PUBLICATION | NEEDS FIXES

## Statistics Verified

### ✅ VERIFIED (Y claims)
1. "70% of platform teams fail" - [Source](url) - Dec 2024
2. "45% disbanded within 18 months" - [Source](url) - Dec 2024

### ❌ INCORRECT (Z claims)
1. "80% adoption" - Actually 78% per [Source](url) - FIX REQUIRED
   - Location: Line 123
   - Suggested fix: Change to "78%" or "nearly 80%"

### ⚠️ NEEDS UPDATE (N claims)
1. "Pricing at $99/mo" - Now $129/mo per [Source](url) as of Jan 2025
   - Location: Line 89
   - Suggested fix: Update price and add date note

## Technical Claims

### ✅ VERIFIED
1. Backstage architecture description - Matches [official docs](url)
2. Kubernetes version requirement - Confirmed in [changelog](url)

### ❌ INCORRECT
[List any incorrect technical claims]

## Sources Quality Check

### ✅ ALL LINKS WORKING
- 14/14 source links tested and working
- All go to claimed content
- All authoritative

### ❌ BROKEN LINKS
[List any broken links with line numbers]

## Marketing Claims Flagged

### ⚠️ UNSUPPORTED CLAIMS
1. "Revolutionary platform" - Line 45 - No data backing, suggest remove or add data
2. "Dramatically improves productivity" - Line 78 - Vague, suggest specific percentage

## Recommendations

### HIGH PRIORITY (Must fix before publication)
- [ ] Fix incorrect stat on line 123 (80% → 78%)
- [ ] Update pricing on line 89 ($99 → $129)

### MEDIUM PRIORITY (Improve quality)
- [ ] Add source for claim on line 156
- [ ] Replace vague "significantly" with specific data on line 203

### LOW PRIORITY (Nice to have)
- [ ] Consider adding more recent source for line 67 (currently 2023 data)

## Final Status

- [ ] READY FOR PUBLICATION (all HIGH priority items fixed)
- [ ] NEEDS FIXES (list blocking issues)

## Notes
[Any additional observations or concerns]
```

## Common Validation Issues

### Issue 1: Outdated Statistics

**Problem**: Stat was correct when written but now outdated
**Fix**: Update to latest data or add date qualifier ("as of 2024")

### Issue 2: Secondary Source Cited

**Problem**: Blog cites another blog instead of original research
**Fix**: Find and link to primary source

### Issue 3: Context Missing

**Problem**: Stat accurate but missing important context
**Fix**: Add qualifying information

**Example**:
- Bad: "Platform teams reduce deployment time 80%"
- Good: "Platform teams reduce deployment time 80% after 12-18 month implementation period"

### Issue 4: Broken Links

**Problem**: Source link 404s or paywalled
**Fix**: Find alternative source or use archive.org

### Issue 5: Marketing Claim

**Problem**: Vendor marketing claim presented as fact
**Fix**: Add "according to [Vendor]" or find independent verification

## Instructions for Claude

When this skill is invoked:

1. **Read the blog post completely**
2. **Extract all verifiable claims** (stats, quotes, technical, pricing)
3. **Verify each claim systematically**:
   - Use WebFetch to check sources
   - Confirm exact numbers/facts
   - Check dates
   - Test links
4. **Flag issues** by priority (HIGH/MEDIUM/LOW)
5. **Create validation report** with clear action items
6. **Determine status**: Ready for publication or needs fixes
7. **Report to user**:
   - X claims verified
   - Y issues found (Z high priority)
   - Status and next steps
   - Next step: Fix issues or use blog-optimize skill

**Remember**: One incorrect statistic can destroy credibility. When in doubt, verify again or remove the claim.
