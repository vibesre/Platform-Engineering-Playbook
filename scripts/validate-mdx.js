#!/usr/bin/env node

/**
 * MDX/Markdown Validation Script
 * Validates all MDX and Markdown files for common issues
 *
 * Enhanced Features:
 * - Parses frontmatter to extract custom slugs
 * - Builds comprehensive map of valid Docusaurus routes
 * - Handles podcast routes with routeBasePath: '/'
 * - Treats broken links as ERRORS (not warnings)
 * - Provides helpful suggestions for broken links
 */

const fs = require('fs');
const path = require('path');
const { glob } = require('glob');

let hasErrors = false;
let hasWarnings = false;

// Cache for valid routes discovered from frontmatter
let validRoutes = new Set();
let routeToFile = new Map(); // Maps routes to their source files for suggestions

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
 * Extract slug from frontmatter
 */
function extractSlugFromFrontmatter(content) {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) return null;

  const frontmatter = frontmatterMatch[1];
  const slugMatch = frontmatter.match(/^slug:\s*(.+)$/m);

  if (slugMatch) {
    let slug = slugMatch[1].trim();
    // Remove quotes if present
    slug = slug.replace(/^['"]|['"]$/g, '');
    // Ensure slug starts with /
    if (!slug.startsWith('/')) {
      slug = '/' + slug;
    }
    return slug;
  }

  return null;
}

/**
 * Extract date from frontmatter (for blog posts)
 */
function extractDateFromFrontmatter(content) {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) return null;

  const frontmatter = frontmatterMatch[1];

  // Try "date:" first
  let dateMatch = frontmatter.match(/^date:\s*(.+)$/m);

  // If not found, try "datePublished:"
  if (!dateMatch) {
    dateMatch = frontmatter.match(/^datePublished:\s*(.+)$/m);
  }

  if (dateMatch) {
    let date = dateMatch[1].trim();
    // Remove quotes if present
    date = date.replace(/^['"]|['"]$/g, '');
    return date;
  }

  return null;
}

/**
 * Build a comprehensive map of all valid routes in the Docusaurus site
 */
function buildValidRoutes(files) {
  validRoutes.clear();
  routeToFile.clear();

  files.forEach(file => {
    const content = fs.readFileSync(file, 'utf8');
    const relativePath = path.relative(path.join(__dirname, '..'), file);

    // Extract custom slug from frontmatter
    const customSlug = extractSlugFromFrontmatter(content);

    if (customSlug) {
      validRoutes.add(customSlug);
      routeToFile.set(customSlug, relativePath);

      // For blog posts, also add with /blog/ prefix since Docusaurus routes blog posts there
      if (file.includes('/blog/')) {
        // customSlug already has leading /, so we need /blog + customSlug
        const blogPrefixedSlug = '/blog' + customSlug;
        validRoutes.add(blogPrefixedSlug);
        routeToFile.set(blogPrefixedSlug, relativePath);
      }
    }

    // Add default routes based on file structure
    if (file.includes('/docs/')) {
      // Docs have routeBasePath: '/' so they're at root
      const docsPath = file.split('/docs/')[1];
      if (docsPath) {
        const routePath = '/' + docsPath
          .replace(/\.mdx?$/, '')
          .replace(/\/index$/, '')
          .replace(/\\/g, '/');

        validRoutes.add(routePath);
        routeToFile.set(routePath, relativePath);

        // Also add version with trailing slash
        if (!routePath.endsWith('/')) {
          validRoutes.add(routePath + '/');
        }
      }
    }

    // Blog posts use date-based routing
    if (file.includes('/blog/')) {
      const fileName = path.basename(file, path.extname(file));

      // Extract date from frontmatter (more reliable than filename)
      const frontmatterDate = extractDateFromFrontmatter(content);
      let year, month, day, slug;

      if (frontmatterDate) {
        // Parse date from frontmatter (YYYY-MM-DD format)
        const dateParts = frontmatterDate.split('-');
        if (dateParts.length === 3) {
          [year, month, day] = dateParts;
          // Extract slug from filename (remove date prefix if present)
          slug = fileName.replace(/^\d{4}-\d{2}(-\d{2})?-/, '');

          const blogRoute = `/blog/${year}/${month}/${day}/${slug}`;
          validRoutes.add(blogRoute);
          validRoutes.add('/blog/' + slug); // Also support short form
          validRoutes.add('/blog/' + fileName); // Also support with date prefix
          routeToFile.set(blogRoute, relativePath);
        }
      } else {
        // Fall back to filename-based date parsing
        // Try YYYY-MM-DD format first
        let dateMatch = fileName.match(/^(\d{4}-\d{2}-\d{2})-(.+)$/);
        if (dateMatch) {
          const [, date, slug] = dateMatch;
          [year, month, day] = date.split('-');
          const blogRoute = `/blog/${year}/${month}/${day}/${slug}`;
          validRoutes.add(blogRoute);
          validRoutes.add('/blog/' + slug); // Also support short form
          validRoutes.add('/blog/' + fileName); // Also support with date prefix
          routeToFile.set(blogRoute, relativePath);
        } else {
          // Try YYYY-MM format (like 2025-01-post-name.md)
          dateMatch = fileName.match(/^(\d{4}-\d{2})-(.+)$/);
          if (dateMatch) {
            const [, date, slug] = dateMatch;
            [year, month] = date.split('-');
            // For YYYY-MM format without day in frontmatter, we can't determine the exact URL
            // Add multiple possible routes
            validRoutes.add('/blog/' + slug); // Short form
            validRoutes.add('/blog/' + fileName); // With date prefix
            routeToFile.set('/blog/' + fileName, relativePath);
          } else {
            // No date prefix, just add as slug
            validRoutes.add('/blog/' + fileName);
            routeToFile.set('/blog/' + fileName, relativePath);
          }
        }
      }
      // Also add /blog prefix for general blog routes
      validRoutes.add('/blog');
      validRoutes.add('/blog/');
    }

    // Podcast routes - these are under /docs/podcasts but routeBasePath: '/' in config
    // means they're accessible at /podcasts/<slug> or via custom slug
    if (file.includes('/docs/podcasts/')) {
      const fileName = path.basename(file, path.extname(file));
      if (fileName !== 'index') {
        // Podcast files like 00002-cloud-providers.md
        const podcastSlug = fileName.replace(/^\d+-/, ''); // Remove number prefix
        validRoutes.add('/podcasts/' + fileName);
        validRoutes.add('/podcasts/' + podcastSlug);
        validRoutes.add('/' + fileName); // Custom slugs often just use the filename
        routeToFile.set('/podcasts/' + fileName, relativePath);
      }
      validRoutes.add('/podcasts');
      validRoutes.add('/podcasts/');
    }
  });

  // Add known static routes
  validRoutes.add('/');
  validRoutes.add('/blog');
  validRoutes.add('/blog/');
  validRoutes.add('/podcasts');
  validRoutes.add('/podcasts/');
  validRoutes.add('/technical-skills');
  validRoutes.add('/interview-prep');
  validRoutes.add('/career-guide');
  validRoutes.add('/practice-resources');
}

/**
 * Find similar routes for suggestions
 */
function findSimilarRoutes(brokenUrl, maxSuggestions = 3) {
  const suggestions = [];
  const brokenParts = brokenUrl.toLowerCase().split('/').filter(Boolean);

  for (const validRoute of validRoutes) {
    const validParts = validRoute.toLowerCase().split('/').filter(Boolean);

    // Calculate similarity score
    let score = 0;
    brokenParts.forEach(part => {
      if (validRoute.toLowerCase().includes(part)) {
        score += part.length;
      }
    });

    if (score > 0) {
      suggestions.push({ route: validRoute, score });
    }
  }

  // Sort by score and return top suggestions
  return suggestions
    .sort((a, b) => b.score - a.score)
    .slice(0, maxSuggestions)
    .map(s => s.route);
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
 * Check for broken internal links using the valid routes map
 */
function validateInternalLinks(file, content) {
  const lines = content.split('\n');

  lines.forEach((line, index) => {
    const lineNum = index + 1;

    // Find markdown links [text](url)
    const linkMatches = line.matchAll(/\[([^\]]+)\]\(([^)]+)\)/g);

    for (const match of linkMatches) {
      const url = match[2];
      const linkText = match[1];

      // Skip external links, anchors, and mailto
      if (url.startsWith('http://') ||
          url.startsWith('https://') ||
          url.startsWith('mailto:') ||
          url.startsWith('#')) {
        continue;
      }

      // Check internal links (relative or absolute paths)
      if (url.startsWith('/') || url.startsWith('./') || url.startsWith('../')) {
        // Clean URL - remove anchors and query params
        const cleanUrl = url.split('#')[0].split('?')[0];

        // Skip empty URLs (just anchors)
        if (!cleanUrl) {
          continue;
        }

        // For relative paths, we need to resolve them
        let checkUrl = cleanUrl;
        if (cleanUrl.startsWith('./') || cleanUrl.startsWith('../')) {
          // Resolve relative to current file location
          const currentDir = path.dirname(file);
          const resolvedPath = path.resolve(currentDir, cleanUrl);
          const projectRoot = path.join(__dirname, '..');
          checkUrl = '/' + path.relative(projectRoot, resolvedPath).replace(/\\/g, '/');

          // Remove /docs/ prefix since routeBasePath: '/'
          checkUrl = checkUrl.replace('/docs/', '/');
        }

        // Normalize the URL for checking
        let normalizedUrl = checkUrl;

        // Remove trailing slash for comparison
        const urlWithoutTrailingSlash = normalizedUrl.endsWith('/')
          ? normalizedUrl.slice(0, -1)
          : normalizedUrl;
        const urlWithTrailingSlash = normalizedUrl.endsWith('/')
          ? normalizedUrl
          : normalizedUrl + '/';

        // Check if URL exists in our valid routes
        const isValid = validRoutes.has(normalizedUrl) ||
                       validRoutes.has(urlWithoutTrailingSlash) ||
                       validRoutes.has(urlWithTrailingSlash);

        if (!isValid) {
          // Broken link found - treat as ERROR
          const suggestions = findSimilarRoutes(normalizedUrl);
          let errorMsg = `Broken internal link: "${url}"`;

          if (suggestions.length > 0) {
            errorMsg += `\n      ${colors.dim}Did you mean:${colors.reset}`;
            suggestions.forEach(suggestion => {
              const sourceFile = routeToFile.get(suggestion);
              errorMsg += `\n      ${colors.cyan}  → ${suggestion}${colors.reset}`;
              if (sourceFile) {
                errorMsg += ` ${colors.dim}(${sourceFile})${colors.reset}`;
              }
            });
          } else {
            errorMsg += `\n      ${colors.dim}No similar routes found. Check the file exists and frontmatter slug is correct.${colors.reset}`;
          }

          error(file, lineNum, errorMsg);
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

  // Build the valid routes map first (for link validation)
  console.log(`${colors.cyan}Building route map from frontmatter and file structure...${colors.reset}`);
  buildValidRoutes(files);
  console.log(`${colors.green}✓${colors.reset} Built map of ${validRoutes.size} valid routes\n`);

  // Validate each file
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
    console.error(`${colors.red}Broken links are now treated as errors to prevent committing bad links${colors.reset}`);
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
