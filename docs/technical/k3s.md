# K3s

<GitHubButtons />
## 📚 Learning Resources

### 📖 Essential Documentation
- [K3s Documentation](https://docs.k3s.io/) - Official comprehensive guide with installation and configuration
- [K3s GitHub Repository](https://github.com/k3s-io/k3s) - 27.6k⭐ Main project repository and community support
- [Rancher K3s Guide](https://rancher.com/docs/k3s/latest/en/) - Complete deployment and management documentation
- [K3s Architecture Overview](https://docs.k3s.io/architecture) - Detailed explanation of components and design decisions

### 📝 Specialized Guides
- [K3s Production Deployment](https://docs.k3s.io/installation/ha) - High availability and production configuration patterns
- [K3s Air-Gap Installation](https://docs.k3s.io/installation/airgap) - Offline deployment for secure environments
- [K3s Edge Computing Guide](https://www.cncf.io/blog/2019/07/05/how-to-deploy-k3s-on-edge-devices/) - Best practices for edge deployments
- [K3s vs K8s Comparison](https://www.rancher.com/blog/2019/2019-02-26-comparing-k8s-distros/) - When to choose K3s over full Kubernetes

### 🎥 Video Tutorials
- [K3s Deep Dive](https://www.youtube.com/watch?v=hMr3prm9gDM) - Complete K3s overview and demo (45 min)
- [K3s Edge Computing Tutorial](https://www.youtube.com/watch?v=2LNxGVS81mE) - Deploying K3s on Raspberry Pi (35 min)
- [K3s Production Setup](https://www.youtube.com/watch?v=UoOcLXfa8EU) - High availability configuration walkthrough (50 min)

### 🎓 Professional Courses
- [Rancher Academy K3s Course](https://academy.rancher.com/courses/k3s-101) - Official K3s fundamentals training (Free)
- [CNCF K3s Training](https://training.linuxfoundation.org/training/kubernetes-for-developers/) - Kubernetes development including K3s (Paid)
- [K3s Edge Computing Course](https://www.udemy.com/course/kubernetes-edge-computing-with-k3s/) - Comprehensive edge deployment course (Paid)

### 📚 Books
- "Learning Kubernetes" by Jonathan Johnson - [Purchase on Amazon](https://www.amazon.com/dp/1492081043)
- "Kubernetes at the Edge" by Alex Ellis - [Purchase on Packt](https://www.packtpub.com/product/kubernetes-at-the-edge/9781801078474)
- "Edge Computing with Kubernetes" by Daphne Chang - [Purchase on O'Reilly](https://www.oreilly.com/library/view/edge-computing-with/9781492087250/)

### 🛠️ Interactive Tools
- [K3d](https://k3d.io/) - 5.3k⭐ K3s in Docker for local development and testing
- [K3sup](https://github.com/alexellis/k3sup) - 4.7k⭐ Bootstrap K3s over SSH for rapid cluster deployment
- [K3s Playground](https://killercoda.com/playgrounds/scenario/kubernetes) - Interactive K3s environment in the browser

### 🚀 Ecosystem Tools
- [System Upgrade Controller](https://github.com/rancher/system-upgrade-controller) - 1.9k⭐ Automated K3s upgrades
- [Longhorn](https://longhorn.io/) - Cloud-native persistent storage for K3s clusters
- [Rancher](https://rancher.com/) - Multi-cluster Kubernetes management platform with K3s support
- [Portainer](https://www.portainer.io/) - Container management UI with K3s integration

### 🌐 Community & Support
- [K3s Slack Channel](https://rancher-users.slack.com/) - Community support and discussions
- [Rancher Community](https://rancher.com/community/) - Forums, meetups, and community resources
- [CNCF K3s Project](https://landscape.cncf.io/card-mode?category=certified-kubernetes-distribution&grouping=category) - Cloud Native Computing Foundation project status

## Understanding K3s: Lightweight Kubernetes for Edge and IoT

K3s is a highly available, certified Kubernetes distribution designed for production workloads in unattended, resource-constrained, remote locations or inside IoT appliances. It's packaged as a single binary less than 100MB and uses less than 512MB of RAM, making it perfect for edge computing and development environments.

### How K3s Works
K3s removes dispensable components from standard Kubernetes and packages everything into a single binary. It replaces etcd with SQLite as the default datastore, embeds containerd as the container runtime, and includes essential components like CoreDNS, Traefik, and a local path provisioner. The control plane components run as a single process, dramatically reducing complexity and resource usage.

The architecture maintains full Kubernetes API compatibility while eliminating cloud provider dependencies and legacy features. Agent nodes join the cluster using a simple token-based authentication system. This streamlined approach enables rapid deployment and simplified operations without sacrificing Kubernetes functionality.

### The K3s Ecosystem
K3s integrates seamlessly with the broader Kubernetes ecosystem while adding edge-specific capabilities. Tools like k3d enable local development with K3s in Docker, while k3sup provides rapid deployment over SSH. The System Upgrade Controller automates cluster updates, and Rancher provides centralized multi-cluster management.

Edge-focused integrations include IoT device management, offline package repositories, and air-gap deployment capabilities. The ecosystem supports ARM architectures, making it ideal for Raspberry Pi and other edge devices. GitOps tools work natively with K3s, enabling automated deployments to distributed edge locations.

### Why K3s Dominates Edge Kubernetes
K3s excels where full Kubernetes is too heavy - edge computing, IoT devices, CI/CD environments, and development machines. Its minimal footprint enables Kubernetes workloads on constrained hardware while maintaining production-grade reliability. The simplified installation and operation reduce the operational burden compared to managing full Kubernetes clusters.

The single binary design eliminates complex dependency management and enables rapid deployment to remote locations. Embedded components reduce external dependencies, while the SQLite default enables single-node deployments without additional infrastructure. This combination makes Kubernetes accessible in environments where traditional deployments would be impractical.

### Mental Model for Success
Think of K3s like a Swiss Army knife version of Kubernetes. Just as a Swiss Army knife contains the essential tools you need in a compact, portable form, K3s packs the core Kubernetes functionality into a lightweight, single binary. Traditional Kubernetes is like a full workshop with every possible tool - powerful but requiring significant space and setup. K3s removes the specialized tools you rarely need (cloud provider integrations, alpha features) while keeping everything essential for running containers (API server, scheduler, kubelet). The embedded components are like having the most commonly needed tools built-in rather than requiring separate purchases.

### Where to Start Your Journey
1. **Single node deployment** - Install K3s on a VM or development machine to explore Kubernetes concepts
2. **Add agent nodes** - Join additional nodes to create your first multi-node cluster
3. **Deploy applications** - Use kubectl to deploy workloads and explore K3s features
4. **Configure networking** - Set up ingress with Traefik and understand service networking
5. **Implement storage** - Configure persistent volumes using the local path provisioner
6. **Explore edge patterns** - Deploy K3s to Raspberry Pi or edge devices for real-world scenarios

### Key Concepts to Master
- **Single binary architecture** - Understanding how K3s packages all components into one executable
- **Embedded components** - CoreDNS, Traefik, containerd, and local path provisioner integration
- **Lightweight design** - What K3s removes from standard Kubernetes and why
- **Agent/server model** - How K3s nodes join clusters using tokens
- **SQLite datastore** - Default storage backend and when to use etcd instead
- **Edge deployment patterns** - Air-gap installations, resource constraints, and connectivity challenges
- **HA configurations** - Multi-server deployments with embedded etcd or external databases
- **Resource management** - Optimizing K3s for constrained environments

Start with single-node installations to understand the basics, then progress to multi-node clusters and edge deployment scenarios. Focus on understanding what makes K3s different from full Kubernetes and when to choose each approach.

---

### 📡 Stay Updated

**Release Notes**: [K3s Releases](https://github.com/k3s-io/k3s/releases) • [Security Updates](https://github.com/k3s-io/k3s/security/advisories) • [Upgrade Guide](https://docs.k3s.io/upgrades)

**Project News**: [Rancher Blog](https://rancher.com/blog/) • [CNCF Newsletter](https://www.cncf.io/newsroom/newsletter/) • [K3s Community Updates](https://rancher-users.slack.com/)

**Community**: [KubeCon Edge Computing Track](https://www.cncf.io/kubecon-cloudnativecon-events/) • [Edge Computing Meetups](https://www.meetup.com/topics/edge-computing/) • [Rancher Meetups](https://www.meetup.com/pro/rancher/)