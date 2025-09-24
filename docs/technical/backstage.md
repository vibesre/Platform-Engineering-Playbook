# Backstage

## 📚 Learning Resources

### 📖 Essential Documentation
- [Backstage Documentation](https://backstage.io/docs/overview/what-is-backstage) - Official documentation
- [Backstage GitHub Repository](https://github.com/backstage/backstage) - 27.7k⭐ Source code and issues
- [Software Catalog](https://backstage.io/docs/features/software-catalog/) - Core feature documentation
- [Plugin Directory](https://backstage.io/plugins) - Available plugins and integrations

### 📝 Specialized Guides
- [Backstage Best Practices](https://backstage.io/docs/overview/adopting) - Adoption strategies
- [Creating Custom Plugins](https://backstage.io/docs/plugins/create-a-plugin) - Plugin development guide
- [Software Templates](https://backstage.io/docs/features/software-templates/) - Scaffolding new projects
- [TechDocs](https://backstage.io/docs/features/techdocs/) - Documentation as code

### 🎥 Video Tutorials
- [Backstage Introduction](https://www.youtube.com/watch?v=85TQEpNCaU0) - Spotify's platform vision (30 min)
- [Building Developer Portals](https://www.youtube.com/watch?v=Qh0TjR0fIXg) - KubeCon presentation (40 min)
- [Backstage Plugins Deep Dive](https://www.youtube.com/watch?v=q5TXXhk0x1A) - Plugin architecture (45 min)

### 🎓 Professional Courses
- [CNCF Backstage Course](https://www.edx.org/course/introduction-to-backstage) - Free EdX course
- [Developer Portal Engineering](https://training.linuxfoundation.org/training/backstage-an-introduction/) - Linux Foundation training
- [Platform Engineering with Backstage](https://www.pluralsight.com/courses/platform-engineering-backstage) - Pluralsight course

### 📚 Books
- "Platform Engineering" by Ajay Chawda - [Purchase on Amazon](https://www.amazon.com/dp/1098153243)
- "Internal Developer Platforms" by Kaspar von Grünberg - [Purchase on O'Reilly](https://www.oreilly.com/library/view/internal-developer-platforms/9781098125769/)

### 🛠️ Interactive Tools
- [Backstage Demo](https://demo.backstage.io/) - Live demo instance
- [Backstage Create App](https://backstage.io/docs/getting-started/) - Quick start CLI
- [Plugin Marketplace](https://backstage.io/plugins) - Browse available plugins

### 🚀 Ecosystem Tools
- [Roadie](https://roadie.io/) - Managed Backstage platform
- [Humanitec](https://humanitec.com/) - Platform orchestration
- [Port](https://www.getport.io/) - Developer portal alternative
- [Cortex](https://www.cortex.io/) - Internal developer portal

### 🌐 Community & Support
- [Backstage Community Discord](https://discord.gg/backstage) - Active community chat
- [CNCF Slack #backstage](https://cloud-native.slack.com/archives/C01E8HU7A4K) - CNCF community
- [BackstageCon](https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/co-located-events/backstagecon/) - Annual conference

## Understanding Backstage: Spotify's Developer Portal Platform

Backstage is an open platform for building developer portals, created by Spotify and donated to the CNCF. It provides a centralized hub where developers can discover services, access documentation, and create new projects from standardized templates.

### How Backstage Works
At its core, Backstage provides a software catalog that maintains a real-time inventory of all services, libraries, data pipelines, and other software components in your organization. Each component is described by a YAML file that includes metadata, ownership information, and relationships to other components.

The platform uses a plugin architecture where each feature is a self-contained React application. Core plugins include the software catalog, TechDocs for documentation, scaffolder for project templates, and integrations with CI/CD systems. Organizations extend Backstage by building custom plugins for their specific needs.

### The Backstage Ecosystem
Backstage integrates with existing tools rather than replacing them. It connects to source control systems to discover components, CI/CD platforms to display build status, monitoring tools to show service health, and cloud providers to track resources. This creates a unified view of your entire technical ecosystem.

The plugin ecosystem is rapidly growing, with contributions for Kubernetes monitoring, cost tracking, security scanning, and feature flags. Major tech companies like Netflix, American Airlines, and Expedia have adopted and extended Backstage for their platforms.

### Why Backstage Dominates Platform Engineering
Backstage addresses the cognitive overload developers face in modern microservices architectures. Instead of juggling dozens of tools and dashboards, developers have one place to understand their technical landscape. It standardizes how teams create new services, document their work, and discover what already exists.

For platform teams, Backstage provides a foundation for building golden paths - prescribed ways to build and deploy services that embed best practices. This accelerates development while ensuring consistency and compliance.

### Mental Model for Success
Think of Backstage like a shopping mall directory for your technology organization. Just as a mall directory shows you where every store is located, what they sell, and their hours, Backstage shows you every service, who owns it, and its current status. The scaffolder templates are like mall kiosks that help you quickly set up new stores (services) with everything you need. TechDocs is like having the instruction manual for every store readily available at the information desk.

### Where to Start Your Journey
1. **Deploy the demo instance** - Explore Backstage features in a sandbox environment
2. **Install Backstage locally** - Use create-app to spin up your own instance
3. **Import your first service** - Add catalog-info.yaml to an existing repository
4. **Create a software template** - Build a template for your standard service architecture
5. **Enable TechDocs** - Set up documentation as code for your services
6. **Build a custom plugin** - Extend Backstage with organization-specific features

### Key Concepts to Master
- **Software catalog** - Component model and entity relationships
- **Catalog ingestion** - Discovery processors and static locations
- **Software templates** - Scaffolder actions and template syntax
- **Plugin architecture** - Frontend and backend plugin development
- **Authentication** - Identity providers and permission framework
- **TechDocs** - MkDocs integration and documentation workflow
- **API definitions** - OpenAPI and AsyncAPI integration
- **Search platform** - Indexing and custom search providers

Start by populating your software catalog, then progressively add templates, documentation, and custom plugins. Remember that Backstage is a platform for building your developer portal, not a turnkey solution - investment in customization yields the best results.

---

### 📡 Stay Updated

**Release Notes**: [Backstage Releases](https://github.com/backstage/backstage/releases) • [Changelog](https://github.com/backstage/backstage/blob/master/docs/releases/changelog.md) • [Roadmap](https://backstage.io/docs/overview/roadmap)

**Project News**: [Backstage Blog](https://backstage.io/blog) • [CNCF Blog](https://www.cncf.io/blog/?_sft_projects=backstage) • [Engineering Blog Posts](https://backstage.spotify.com/)

**Community**: [BackstageCon](https://events.linuxfoundation.org/backstagecon/) • [Community Sessions](https://backstage.io/community) • [Adopters](https://backstage.io/adopters)