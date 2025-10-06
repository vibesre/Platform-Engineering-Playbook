#!/usr/bin/env node

/**
 * MDX/Markdown Validation Script
 * Validates all MDX and Markdown files for common issues
 */

const fs = require('fs');
const path = require('path');
const { glob } = require('glob');

let hasErrors = false;
let hasWarnings = false;

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  green: '\x1b[32m',
  cyan: '\x1b[36m',
  dim: '\x1b[2m',
};

function error(file, line, message) {
  console.error(`${colors.red}✗${colors.reset} ${colors.cyan}${file}${colors.dim}:${line}${colors.reset} - ${message}`);
  hasErrors = true;
}

function warn(file, line, message) {
  console.warn(`${colors.yellow}⚠${colors.reset} ${colors.cyan}${file}${colors.dim}:${line}${colors.reset} - ${message}`);
  hasWarnings = true;
}

function success(message) {
  console.log(`${colors.green}✓${colors.reset} ${message}`);
}

/**
 * Check for MDX-incompatible patterns
 */
function validateMDXSyntax(file, content) {
  const lines = content.split('\n');

  lines.forEach((line, index) => {
    const lineNum = index + 1;

    // Check for < followed by a digit (common MDX issue)
    const lessThanDigitMatch = line.match(/<(\d)/g);
    if (lessThanDigitMatch) {
      error(file, lineNum, `Found '<${lessThanDigitMatch[0][1]}' which MDX interprets as JSX. Use 'under ${lessThanDigitMatch[0][1]}' or 'less than ${lessThanDigitMatch[0][1]}' instead.`);
    }

    // Check for unescaped < > that might be JSX
    const potentialJSX = line.match(/<[^>/\s!-][^>]*(?:>|$)/g);
    if (potentialJSX) {
      potentialJSX.forEach(match => {
        // Filter out valid HTML/JSX tags and markdown links
        if (!match.match(/^<(https?|mailto|ftp):|^<\w+\s|^<\w+>|^<\/\w+>/)) {
          warn(file, lineNum, `Potential unintended JSX syntax: "${match}". If not intentional, escape with backslash or use different wording.`);
        }
      });
    }

    // Check for triple backticks without language
    if (line.trim() === '```' && index > 0) {
      const prevLine = lines[index - 1];
      if (!prevLine.trim().startsWith('```')) {
        warn(file, lineNum, 'Code block without language specification. Consider adding a language for syntax highlighting.');
      }
    }
  });
}

/**
 * Validate frontmatter
 */
function validateFrontmatter(file, content) {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);

  if (!frontmatterMatch) {
    // Check if file should have frontmatter (blog posts and docs should)
    if (file.includes('/blog/') || file.includes('/docs/')) {
      warn(file, 1, 'Missing frontmatter. Consider adding title, description, and keywords for SEO.');
    }
    return;
  }

  const frontmatter = frontmatterMatch[1];

  // Check for required fields in blog posts
  if (file.includes('/blog/')) {
    if (!frontmatter.includes('title:')) {
      error(file, 1, 'Blog post missing required "title" in frontmatter');
    }
    if (!frontmatter.includes('description:')) {
      warn(file, 1, 'Blog post missing "description" in frontmatter (recommended for SEO)');
    }
    if (!frontmatter.includes('keywords:')) {
      warn(file, 1, 'Blog post missing "keywords" in frontmatter (recommended for SEO)');
    }
    if (!frontmatter.includes('datePublished:')) {
      warn(file, 1, 'Blog post missing "datePublished" in frontmatter (recommended for SEO)');
    }
  }

  // Check for duplicate keys
  const lines = frontmatter.split('\n');
  const keys = {};
  lines.forEach((line, index) => {
    const match = line.match(/^(\w+):/);
    if (match) {
      const key = match[1];
      if (keys[key]) {
        error(file, index + 2, `Duplicate frontmatter key: "${key}"`);
      }
      keys[key] = true;
    }
  });
}

/**
 * Check for broken internal links
 */
function validateInternalLinks(file, content) {
  const lines = content.split('\n');

  lines.forEach((line, index) => {
    const lineNum = index + 1;

    // Find markdown links [text](url)
    const linkMatches = line.matchAll(/\[([^\]]+)\]\(([^)]+)\)/g);

    for (const match of linkMatches) {
      const url = match[2];

      // Check internal links (relative paths)
      if (url.startsWith('/') || url.startsWith('./') || url.startsWith('../')) {
        const cleanUrl = url.split('#')[0].split('?')[0];

        // Skip blog links - Docusaurus handles date-based routing
        if (cleanUrl.startsWith('/blog/')) {
          // Try to find matching blog file
          const blogPattern = cleanUrl.substring(6); // Remove '/blog/'
          const blogFiles = fs.readdirSync(path.join(__dirname, '..', 'blog'))
            .filter(f => f.endsWith('.md') || f.endsWith('.mdx'))
            .filter(f => f.includes(blogPattern.split('/').pop()));

          if (blogFiles.length === 0) {
            warn(file, lineNum, `Potentially broken blog link: "${url}" (no matching blog file found)`);
          }
          return; // Skip further checks for blog links
        }

        // Resolve relative to project root or current file
        let fullPath;
        if (url.startsWith('/')) {
          // Absolute from docs root
          fullPath = path.join(__dirname, '..', 'docs', cleanUrl.substring(1));
        } else {
          // Relative to current file
          fullPath = path.resolve(path.dirname(file), cleanUrl);
        }

        // Check if file or directory exists
        const exists = fs.existsSync(fullPath) ||
                      fs.existsSync(fullPath + '.md') ||
                      fs.existsSync(fullPath + '.mdx') ||
                      fs.existsSync(path.join(fullPath, 'index.md')) ||
                      fs.existsSync(path.join(fullPath, 'index.mdx'));

        if (!exists) {
          warn(file, lineNum, `Potentially broken internal link: "${url}"`);
        }
      }
    }
  });
}

/**
 * Check for common content issues
 */
function validateContent(file, content) {
  const lines = content.split('\n');

  lines.forEach((line, index) => {
    const lineNum = index + 1;

    // Check for TODO/FIXME comments
    if (line.match(/\b(TODO|FIXME|XXX)\b/i)) {
      warn(file, lineNum, `Found ${line.match(/\b(TODO|FIXME|XXX)\b/i)[0]} comment`);
    }

    // Check for trailing whitespace
    if (line.endsWith(' ') || line.endsWith('\t')) {
      warn(file, lineNum, 'Line has trailing whitespace');
    }

    // Check for multiple consecutive blank lines
    if (index > 0 && line === '' && lines[index - 1] === '' && lines[index - 2] === '') {
      warn(file, lineNum, 'Multiple consecutive blank lines (>2)');
    }
  });

  // Check for file ending with newline
  if (content.length > 0 && !content.endsWith('\n')) {
    warn(file, lines.length, 'File should end with a newline');
  }
}

/**
 * Main validation function
 */
async function validateFile(file) {
  const content = fs.readFileSync(file, 'utf8');

  validateMDXSyntax(file, content);
  validateFrontmatter(file, content);
  validateInternalLinks(file, content);
  validateContent(file, content);
}

/**
 * Run validation on all files
 */
async function main() {
  console.log('🔍 Validating MDX and Markdown files...\n');

  // Find all markdown and MDX files
  const files = await glob('**/*.{md,mdx}', {
    cwd: path.join(__dirname, '..'),
    ignore: ['node_modules/**', 'build/**', '.docusaurus/**', '**/node_modules/**'],
    absolute: true,
  });

  console.log(`Found ${files.length} files to validate\n`);

  for (const file of files) {
    const relativePath = path.relative(path.join(__dirname, '..'), file);
    try {
      await validateFile(file);
    } catch (err) {
      error(relativePath, 1, `Failed to validate: ${err.message}`);
    }
  }

  console.log('\n' + '─'.repeat(80) + '\n');

  if (hasErrors) {
    console.error(`${colors.red}✗ Validation failed with errors${colors.reset}`);
    process.exit(1);
  } else if (hasWarnings) {
    console.warn(`${colors.yellow}⚠ Validation completed with warnings${colors.reset}`);
    process.exit(0); // Don't fail on warnings
  } else {
    success('All files validated successfully!');
    process.exit(0);
  }
}

main().catch(err => {
  console.error(`${colors.red}Fatal error:${colors.reset}`, err);
  process.exit(1);
});
