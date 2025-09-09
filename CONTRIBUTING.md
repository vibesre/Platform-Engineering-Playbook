# Contributing to Platform Engineering Playbook

Thank you for your interest in contributing! This guide is designed to make contributing as easy as possible while maintaining content quality.

## Quick Start for Contributors

### Adding or Updating Content

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/Platform-Engineering-Playbook.git
   cd Platform-Engineering-Playbook
   ```

2. **Navigate to the `docs` directory** - All content lives here:
   ```
   docs/
   ├── intro.md                    # Home page content
   ├── technical/                  # Technical skills content
   ├── interview-process/          # Interview process guides
   ├── resume/                     # Resume preparation
   ├── behavioral/                 # Behavioral interview prep
   ├── career/                     # Career progression
   └── resources/                  # Additional resources
   ```

3. **Edit or create markdown files**
   - To edit existing content: Find the relevant `.md` file and make your changes
   - To add new content: Create a new `.md` file in the appropriate directory

4. **Add frontmatter to new files**:
   ```markdown
   ---
   title: Your Page Title
   sidebar_position: 10
   ---
   
   # Your Content Here
   ```

5. **Test locally (optional)**:
   ```bash
   npm install
   npm start
   ```

6. **Submit a pull request**

## Content Guidelines

### What We're Looking For

- **High-quality resources**: Links to actively maintained repos, recent blog posts, and current documentation
- **Practical examples**: Real interview questions, code samples, and case studies
- **Platform engineering focus**: Content specific to SRE, DevOps, Platform Engineering, and Production Engineering roles
- **Clear explanations**: Break down complex topics into understandable sections

### Content Structure

Each topic page should follow this general structure:

```markdown
---
title: Topic Name
sidebar_position: 1
---

# Topic Name

Brief introduction to the topic (2-3 sentences)

## Key Concepts

Main concepts to understand

## Resources

### Essential Reading
- Resource 1
- Resource 2

### Hands-on Practice
- Lab 1
- Exercise 2

### Interview Preparation
- Common questions
- What interviewers look for
```

### Markdown Conventions

- Use heading levels consistently (# for page title, ## for main sections, ### for subsections)
- Include descriptive link text: `[Kubernetes Official Docs](https://kubernetes.io)` not `[click here](https://kubernetes.io)`
- Add brief descriptions for resources when helpful
- Use code blocks with language specification:
  ````markdown
  ```bash
  kubectl get pods
  ```
  ````

## Types of Contributions

### Content Contributions

1. **New topics**: Add new technical topics, interview strategies, or career advice
2. **Update existing content**: Fix errors, add new resources, improve explanations
3. **Add examples**: Interview questions, code samples, architecture diagrams
4. **Curate resources**: Add high-quality learning materials, tools, or platforms

### Technical Contributions

1. **Site improvements**: Enhance the website functionality or design
2. **Bug fixes**: Report or fix issues with the site
3. **Documentation**: Improve this guide or other docs

## Pull Request Process

1. **Create a descriptive PR title**: "Add Kubernetes security best practices section"
2. **Describe your changes**: What you added/changed and why
3. **Link related issues**: If applicable
4. **Wait for review**: Maintainers will review and provide feedback

## No Code Changes Needed!

**Important**: You don't need to understand React, TypeScript, or Docusaurus to contribute content. Just edit the markdown files in the `docs/` directory, and the site will automatically update.

## Questions?

If you're unsure about anything:
1. Open an issue to discuss your idea
2. Check existing issues and PRs
3. Ask in the PR comments

## License

By contributing, you agree that your contributions will be licensed under the same Creative Commons license as the project.

---

Thank you for helping make this resource better for the platform engineering community!