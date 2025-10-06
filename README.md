# Platform Engineering Playbook

Your comprehensive guide to Platform Engineering, SRE, and DevOps interviews. Visit the live site at [https://platformengineeringplaybook.com](https://platformengineeringplaybook.com)

## About

This guide provides curated resources, practical advice, and comprehensive preparation materials for:
- Site Reliability Engineers (SREs)
- Platform Engineers
- DevOps Engineers
- Production Engineers

## Contributing

We welcome contributions! The best part: **you only need to edit markdown files** to contribute content.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contribution Steps

1. Fork this repository
2. Navigate to the `docs/` directory
3. Edit or create markdown files
4. Submit a pull request

## Local Development

If you want to preview your changes locally:

```bash
npm install
npm start
```

This will start a local development server at `http://localhost:3000/`

### Testing

The project includes automated testing to ensure content quality:

```bash
# Validate MDX/Markdown files
npm run test:mdx

# Run TypeScript type checking
npm run typecheck

# Run full test suite (including build)
npm run test:all
```

**Pre-commit hooks automatically run tests** before each commit to prevent broken code from being committed. See [docs/TESTING.md](docs/TESTING.md) for details.

## Project Structure

```
Platform-Engineering-Playbook/
├── docs/                    # All content lives here (markdown files)
├── src/                     # Website configuration (don't edit unless improving site features)
├── static/                  # Static assets
└── docusaurus.config.ts     # Site configuration
```

## Built With

- [Docusaurus](https://docusaurus.io/) - Modern static website generator
- Deployed via GitHub Pages

## License

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

---

*Inspired by [yangshun/tech-interview-handbook](https://github.com/yangshun/tech-interview-handbook)*
