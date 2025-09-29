# Crossplane

<GitHubButtons />
## 📚 Learning Resources

### 📖 Essential Documentation
- [Crossplane Documentation](https://crossplane.io/docs/) - Official comprehensive guide with getting started tutorials
- [Crossplane GitHub Repository](https://github.com/crossplane/crossplane) - 9.3k⭐ Main project with community issues and discussions
- [Crossplane API Reference](https://doc.crds.dev/github.com/crossplane/crossplane) - Complete API documentation for all resources
- [Provider Documentation Hub](https://marketplace.upbound.io/) - Official provider registry and documentation

### 📝 Specialized Guides
- [Upbound Cloud Documentation](https://docs.upbound.io/) - Managed Crossplane service and advanced features
- [Composition Functions Guide](https://crossplane.io/docs/v1.14/concepts/composition-functions/) - Next-generation composition with advanced logic
- [Multi-Cloud Reference Architecture](https://github.com/upbound/platform-ref-multi-k8s) - Production-ready platform examples
- [Crossplane Patterns](https://blog.crossplane.io/tag/patterns/) - Design patterns and best practices from the team

### 🎥 Video Tutorials
- [Crossplane Deep Dive Series](https://www.youtube.com/playlist?list=PL510POnNVaaYFuK-B_SIUrpIonCtLVOzT) - Comprehensive tutorial series (multiple hours)
- [Building Platform APIs with Crossplane](https://www.youtube.com/watch?v=n8KjVmuHm7A) - KubeCon platform engineering talk (45 min)
- [Crossplane vs Terraform Comparison](https://www.youtube.com/watch?v=6r3NapC2IFM) - When to use each tool (35 min)

### 🎓 Professional Courses
- [Upbound Academy](https://academy.upbound.io/) - Official Crossplane training courses (Free)
- [Platform Engineering with Crossplane](https://www.pluralsight.com/courses/platform-engineering-crossplane) - Pluralsight comprehensive course (Paid)
- [CNCF Crossplane Course](https://www.edx.org/course/introduction-to-kubernetes) - EdX introduction including Crossplane (Free)

### 📚 Books
- "Platform Engineering on Kubernetes" by Mauricio Salatino - [Purchase on Amazon](https://www.amazon.com/dp/1617297348)
- "Kubernetes Operators" by Jason Dobies - [Purchase on O'Reilly](https://www.oreilly.com/library/view/kubernetes-operators/9781492048039/)
- "Cloud Native Patterns" by Cornelia Davis - [Purchase on Amazon](https://www.amazon.com/dp/1617294292)

### 🛠️ Interactive Tools
- [Crossplane CLI (kubectl crossplane)](https://crossplane.io/docs/v1.14/cli/) - Official CLI for local development and debugging
- [Upbound CLI (up)](https://docs.upbound.io/cli/) - Enhanced CLI for Upbound Cloud and advanced features
- [Crossplane Playground](https://play.crossplane.io/) - Interactive web-based environment for experimentation

### 🚀 Ecosystem Tools
- [ArgoCD Crossplane Plugin](https://github.com/argoproj-labs/argocd-crossplane-plugin) - GitOps integration for Crossplane resources
- [Crossplane Contrib Providers](https://github.com/crossplane-contrib) - Community-maintained providers for additional clouds
- [Function SDK](https://github.com/crossplane/function-sdk-go) - 150⭐ Go SDK for building composition functions
- [Upbound Universal Crossplane](https://github.com/upbound/universal-crossplane) - 340⭐ Enhanced Crossplane distribution

### 🌐 Community & Support
- [Crossplane Slack](https://slack.crossplane.io/) - Active community chat and support channels
- [Crossplane Community](https://github.com/crossplane/crossplane/blob/main/CONTRIBUTING.md) - Contributing guidelines and community info
- [Cloud Native Computing Foundation](https://www.cncf.io/projects/crossplane/) - CNCF project page with governance details

## Understanding Crossplane: Kubernetes-Native Infrastructure Management

Crossplane is an open-source Kubernetes add-on that transforms your cluster into a universal control plane for cloud infrastructure. It enables platform teams to compose infrastructure from multiple vendors and expose higher-level self-service APIs for application teams, all using familiar Kubernetes patterns and GitOps workflows.

### How Crossplane Works
Crossplane extends Kubernetes with Custom Resource Definitions (CRDs) that represent cloud infrastructure as Kubernetes resources. Provider controllers watch these resources and interact with cloud APIs to provision actual infrastructure. The composition engine allows platform engineers to bundle multiple infrastructure resources into higher-level APIs that abstract complexity from developers.

Resources move through standard Kubernetes lifecycle phases - pending, provisioning, ready, and bound. Connection secrets automatically propagate credentials and endpoints to consuming applications. This Kubernetes-native approach means you manage infrastructure using kubectl, GitOps, and existing Kubernetes tooling.

### The Crossplane Ecosystem
Crossplane's architecture centers around providers that extend functionality to different clouds and services. Official providers support major cloud platforms (AWS, Azure, GCP), while community providers extend to specialized services. The composition system enables building reusable infrastructure patterns that work across any supported provider.

The ecosystem includes developer tooling (CLI, VS Code extensions), monitoring integrations (Prometheus metrics), and platform solutions (Upbound Cloud). ArgoCD integration enables GitOps workflows, while policy engines like Gatekeeper provide governance. The growing marketplace of providers and compositions accelerates platform development.

### Why Crossplane Dominates Cloud-Native Infrastructure
Crossplane brings true Kubernetes-native patterns to infrastructure management, unlike external tools that require separate state management and workflows. Its composition model enables building higher-level abstractions without losing access to underlying cloud primitives. Multi-cloud support works through consistent APIs rather than lowest-common-denominator approaches.

The declarative, controller-based architecture provides self-healing infrastructure that automatically reconciles drift. Strong typing through OpenAPI schemas prevents configuration errors, while the package system enables sharing and versioning of platform APIs. Integration with Kubernetes RBAC and networking provides enterprise-grade security and isolation.

### Mental Model for Success
Think of Crossplane like a universal remote control system for your entire technology infrastructure. Just as a universal remote can control different brands of devices (TV, stereo, streaming box) through a single interface, Crossplane controls different cloud providers through Kubernetes APIs. The composition engine is like programmable macros - you can create custom buttons (APIs) that trigger complex sequences of actions across multiple devices (cloud resources). Platform teams program the remote (create compositions), while developers just press the buttons they need (create claims). Everything works through the same familiar interface (kubectl), regardless of which cloud provider is actually fulfilling the request.

### Where to Start Your Journey
1. **Install Crossplane** - Deploy Crossplane to a Kubernetes cluster and explore the core concepts
2. **Add a provider** - Install the AWS, Azure, or GCP provider and configure credentials
3. **Create your first managed resource** - Provision a simple resource like an S3 bucket directly
4. **Build a composition** - Create your first XRD and composition to abstract infrastructure complexity
5. **Deploy via claims** - Use your custom API to provision infrastructure through higher-level abstractions
6. **Implement GitOps** - Integrate with ArgoCD to manage infrastructure through Git workflows

### Key Concepts to Master
- **Providers** - Extensions that add cloud-specific resource types and controllers
- **Managed resources** - Low-level cloud resources managed directly by providers
- **Composite resources (XRs)** - Custom higher-level resources defined by platform teams
- **Claims** - Namespace-scoped requests for composite resources from application teams
- **Compositions** - Templates that define how composite resources map to managed resources
- **Composition functions** - Advanced logic for complex resource transformations and validation
- **Connection secrets** - Automatic propagation of resource connection details to applications
- **Packages** - Distribution mechanism for providers, configurations, and platform APIs

Start with simple managed resources to understand the basic provider model, then progress to compositions and custom APIs. Master the relationship between XRDs, compositions, and claims before exploring advanced features like composition functions and multi-cloud patterns.

---

### 📡 Stay Updated

**Release Notes**: [Crossplane Releases](https://github.com/crossplane/crossplane/releases) • [Provider Releases](https://marketplace.upbound.io/) • [Security Updates](https://crossplane.io/docs/v1.14/knowledge-base/guides/troubleshoot/)

**Project News**: [Crossplane Blog](https://blog.crossplane.io/) • [Upbound Blog](https://blog.upbound.io/) • [CNCF Newsletter](https://www.cncf.io/newsroom/newsletter/)

**Community**: [Community Meetings](https://github.com/crossplane/crossplane#get-involved) • [KubeCon Talks](https://www.cncf.io/kubecon-cloudnativecon-events/) • [Platform Engineering Meetups](https://www.meetup.com/topics/platform-engineering/)