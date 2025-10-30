# Claude Configuration

The main Claude Code configuration for this project has been moved to the **parent directory** to be shared between the public and private repositories.

## Location

**Shared Configuration**: `/home/eric-wd/projects/platform-engineering-playbook/.claude/`

This directory contains:
- `CLAUDE.md` - Development guide, standards, and workflows
- `skills/` - All Claude Code skills (blog, podcast, lesson production)
- `settings.local.json` - Permissions and configuration

## Why Shared?

The Platform Engineering Playbook uses a three-tier architecture:
1. **Public repo** - Documentation and website
2. **Private repo** - Podcast generation and internal tools
3. **NAS storage** - Media files

By keeping Claude configuration in the parent directory:
- Both repos can access the same skills
- Single source of truth for development standards
- No duplication of instructions
- Public repo doesn't expose internal workflows

## Accessing

Claude Code automatically checks parent directories for `.claude/` configuration, so this setup works transparently when working in either:
- `platform-engineering-playbook/` (public repo)
- `platform-engineering-playbook-PRIVATE/` (private repo)

## Documentation

For full context on the repository structure and workflows, see:
- `../.claude/CLAUDE.md` - Complete development guide
- `../platform-engineering-playbook-PRIVATE/MIGRATION_SUMMARY.md` - Migration details
