# Testing Guide

## Overview

The Platform Engineering Playbook includes comprehensive automated testing to ensure all content is valid and error-free before being committed to the repository.

## Test Suite

### 1. MDX/Markdown Validation (`test:mdx`)

Validates all `.md` and `.mdx` files for:

- **MDX Syntax Issues**: Detects patterns that MDX interprets as JSX (e.g., less-than with numbers should use words like "under 5")
- **Frontmatter Validation**: Checks for required fields in blog posts (title, description, keywords)
- **Internal Link Checking**: Validates that internal links point to existing files
- **Content Quality**: Detects TODO/FIXME comments, trailing whitespace, multiple blank lines
- **Code Blocks**: Warns about code blocks without language specifications

**Run manually:**
```bash
npm run test:mdx
```

### 2. TypeScript Type Checking (`typecheck`)

Validates TypeScript code for type errors in:
- Configuration files (`docusaurus.config.ts`, `sidebars.ts`)
- React components
- Type definitions

**Run manually:**
```bash
npm run typecheck
```

### 3. Docusaurus Build Test

Performs a full production build to catch:
- MDX compilation errors
- Missing dependencies
- Invalid configuration
- Broken imports

**Run manually:**
```bash
npm run build
```

### 4. Comprehensive Test Suite (`test:all`)

Runs all tests plus additional checks:
- Large file detection (files >1MB)
- TODO/FIXME comment detection in staged files
- Podcast metadata integrity checks

**Run manually:**
```bash
npm run test:all
```

## Pre-Commit Hooks

Pre-commit hooks automatically run before every commit to prevent broken code from being committed.

### What Runs on Pre-Commit

1. ✅ MDX/Markdown validation
2. ✅ TypeScript type checking
3. ✅ Docusaurus build test

If any check fails, the commit will be blocked until issues are fixed.

### Skipping Pre-Commit Hooks

**⚠️ Not recommended**, but in emergencies:

```bash
git commit --no-verify -m "Your commit message"
```

## Common Issues and Fixes

### Issue: `<` followed by number in markdown

**Error:**
```
Found 'less-than-5' which MDX interprets as JSX
```

**Fix:**
Replace less-than-symbol-5 with `under 5` or `less than 5`:
```markdown
❌ Team size less-than-5 people
✅ Team size under 5 people
```

### Issue: Missing frontmatter in blog posts

**Warning:**
```
Blog post missing required "title" in frontmatter
```

**Fix:**
Add frontmatter at the top of the file:
```yaml
---
title: "Your Post Title"
description: "Brief description for SEO"
keywords:
  - keyword1
  - keyword2
datePublished: "2025-10-06"
---
```

### Issue: Broken internal links

**Warning:**
```
Potentially broken internal link: "/docs/technical/foo"
```

**Fix:**
- Verify the path exists
- Use correct relative or absolute paths
- Check for typos in file names

### Issue: Code blocks without language

**Warning:**
```
Code block without language specification
```

**Fix:**
Specify the language after the opening backticks:
````markdown
❌ ```
   code here
   ```

✅ ```bash
   code here
   ```
````

## Development Workflow

### Standard Workflow

1. Make your changes
2. Stage files: `git add .`
3. Commit: `git commit -m "Your message"`
4. Pre-commit hooks run automatically
5. If tests pass, commit succeeds
6. If tests fail, fix issues and try again

### Testing Before Commit

Run tests manually before committing to catch issues early:

```bash
# Quick validation
npm run test:mdx

# Full test suite
npm run test:all
```

## CI/CD Integration

Future: These tests will also run in CI/CD pipelines (GitHub Actions) to:
- Validate pull requests
- Run on main branch
- Generate test reports
- Block merges if tests fail

## Scripts Location

All test scripts are located in the `scripts/` directory:

- `scripts/validate-mdx.js` - MDX/Markdown validator
- `scripts/test-all.sh` - Comprehensive test runner

Pre-commit hooks are in `.husky/pre-commit`.

## Troubleshooting

### Hooks not running

If pre-commit hooks aren't running:

```bash
# Reinstall husky
npm run prepare

# Make hook executable
chmod +x .husky/pre-commit
```

### Tests taking too long

The build step can take 30-60 seconds. For faster iteration:

```bash
# Run only MDX validation
npm run test:mdx

# Run only type checking
npm run typecheck
```

### False positives

If the validator reports false positives (valid code flagged as errors):
1. Check if it's a known MDX limitation
2. Consider adjusting the validation rules in `scripts/validate-mdx.js`
3. Document the exception in this guide

## Contributing Test Improvements

To improve the test suite:

1. Edit validation logic in `scripts/validate-mdx.js`
2. Update pre-commit hook in `.husky/pre-commit`
3. Test your changes with `npm run test:all`
4. Update this documentation
5. Submit a pull request

## Resources

- [Docusaurus MDX Documentation](https://docusaurus.io/docs/markdown-features)
- [MDX Syntax](https://mdxjs.com/)
- [Husky Documentation](https://typicode.github.io/husky/)
