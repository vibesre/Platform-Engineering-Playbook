# tmux

## 📚 Learning Resources

### 📖 Essential Documentation
- [tmux Manual Page](https://man.openbsd.org/tmux.1) - Official comprehensive manual
- [tmux GitHub Repository](https://github.com/tmux/tmux) - Source code and latest updates
- [tmux Wiki](https://github.com/tmux/tmux/wiki) - Community documentation and tips
- [OpenBSD tmux](https://man.openbsd.org/tmux) - Original tmux documentation

### 📝 Specialized Guides
- [tmux Cheat Sheet](https://tmuxcheatsheet.com/) - Quick reference for commands and shortcuts
- [Practical tmux](https://mutelight.org/practical-tmux) - Real-world usage patterns
- [tmux Powerline Guide](https://powerline.readthedocs.io/en/latest/usage/other.html#tmux-statusline) - Advanced status bar customization
- [tmux for Developers](https://thoughtbot.com/blog/a-tmux-crash-course) - Development-focused workflows

### 🎥 Video Tutorials
- [tmux Basics](https://www.youtube.com/watch?v=Lqehvpe_djs) - Complete beginner tutorial (30 min)
- [tmux for Development](https://www.youtube.com/watch?v=5r6yzFEXajQ) - Developer workflow setup (45 min)
- [Advanced tmux](https://www.youtube.com/watch?v=DzNmUNvnB04) - Power user techniques (60 min)
- [tmux Pairing Sessions](https://www.youtube.com/watch?v=norO25P7_eQ) - Collaborative development (25 min)

### 🎓 Professional Courses
- [The Pragmatic Programmer tmux](https://pragprog.com/titles/bhtmux/tmux/) - Comprehensive book and course (Paid)
- [Linux Academy tmux Course](https://acloudguru.com/course/linux-academy-tmux-course) - Structured learning path (Paid)
- [Pluralsight Terminal Skills](https://www.pluralsight.com/courses/terminal-multiplexer-tmux) - Professional development focus (Paid)

### 📚 Books
- "The Tao of tmux" by Tony Narlock - [Free PDF](https://leanpub.com/the-tao-of-tmux) | [Purchase](https://leanpub.com/the-tao-of-tmux)
- "tmux 2: Productive Mouse-Free Development" by Brian P. Hogan - [Purchase on Amazon](https://www.amazon.com/tmux-2-Productive-Mouse-Free-Development/dp/1680502212) | [Pragmatic Bookshelf](https://pragprog.com/titles/bhtmux2/tmux-2/)

### 🛠️ Interactive Tools
- [tmux Cheat Sheet Interactive](https://tmuxcheatsheet.com/) - Browser-based reference
- [tmux Simulator](https://www.terminallyoutdated.net/tmux-simulator/) - Practice tmux commands online
- [tmux Configuration Generator](https://github.com/rothgar/awesome-tmux#configuration) - Automated config creation

### 🚀 Ecosystem Tools
- [Tmux Plugin Manager (TPM)](https://github.com/tmux-plugins/tpm) - Essential plugin management system
- [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect) - Session persistence across restarts
- [tmux-continuum](https://github.com/tmux-plugins/tmux-continuum) - Automatic session saving
- [powerline](https://github.com/powerline/powerline) - Advanced status bar enhancement

### 🌐 Community & Support
- [r/tmux](https://www.reddit.com/r/tmux/) - Community discussions and tips
- [tmux Gitter Chat](https://gitter.im/tmux/tmux) - Real-time community support
- [Stack Overflow tmux](https://stackoverflow.com/questions/tagged/tmux) - Technical Q&A
- [awesome-tmux](https://github.com/rothgar/awesome-tmux) - Curated resources and plugins

## Understanding tmux: Your Terminal Multiplexer Superpower

tmux (terminal multiplexer) transforms how platform engineers work with remote servers and development environments. It creates persistent sessions that survive disconnections, enables window and pane management, and supports collaborative work - essential capabilities for modern infrastructure management.

### How tmux Works
tmux creates a server-client architecture where sessions run independently of terminal connections. When you start tmux, it spawns a server process that manages sessions, windows, and panes. Your terminal becomes a client that attaches to this server, allowing you to detach and reattach without losing work.

This architecture enables powerful workflows: SSH into a server, start tmux, begin long-running tasks, detach, close your laptop, and later reconnect to find everything exactly as you left it. Multiple clients can attach to the same session for pair programming or collaborative debugging.

### The tmux Ecosystem
tmux's ecosystem centers around three core concepts: sessions contain windows, windows contain panes, and everything is customizable. Sessions represent different projects or contexts, windows organize related tasks, and panes split individual windows for parallel work.

The plugin ecosystem extends tmux with session restoration, enhanced status bars, improved navigation, and integration with development tools. Configuration files allow extensive customization of keybindings, appearance, and behavior.

### Why tmux Dominates Terminal Workflows
Traditional terminal usage ties your work to a single connection. If you lose connection or close your terminal, running processes die and context disappears. tmux solves this fundamental limitation while adding powerful multiplexing capabilities.

For platform engineers managing multiple servers, deployments, and monitoring tasks, tmux provides unmatched efficiency. Its keyboard-driven interface eliminates mouse dependency, its session management enables context switching, and its collaboration features support team workflows.

### Mental Model for Success
Think of tmux like a modern office building for your terminal work. Sessions are different floors (projects), windows are rooms on each floor (different aspects of work), and panes are workstations within rooms (parallel tasks). You can move between floors, rooms, and workstations instantly. When you leave the building (disconnect), everything stays exactly where you left it. Colleagues can visit your workspaces (attach to sessions) for collaboration.

### Where to Start Your Journey
1. **Learn basic navigation** - Master session, window, and pane operations
2. **Customize key bindings** - Create comfortable, efficient keybinding patterns
3. **Install essential plugins** - Add TPM, resurrect, and continuum for core functionality
4. **Create session scripts** - Automate common project setups
5. **Practice collaborative workflows** - Use shared sessions for pairing and training
6. **Integrate with tools** - Connect tmux with editors, monitoring tools, and deployment scripts

### Key Concepts to Master
- **Session management** - Creating, naming, and switching between project contexts
- **Window organization** - Logical grouping of related tasks and tools
- **Pane layouts** - Efficient screen space utilization and task parallelization
- **Key binding customization** - Creating muscle memory for common operations
- **Plugin ecosystem** - Extending functionality with community tools
- **Configuration management** - Maintaining consistent setups across environments
- **Collaborative features** - Shared sessions for pair programming and training
- **Integration patterns** - Connecting tmux with development and operations workflows

Start with basic session and window management, then gradually add complexity. Focus on building muscle memory for essential commands. Remember that tmux's power comes from consistency - use it for everything to maximize benefits.

---

### 📡 Stay Updated

**Release Notes**: [tmux Releases](https://github.com/tmux/tmux/releases) • [Changelog](https://github.com/tmux/tmux/blob/master/CHANGES) • [Development News](https://github.com/tmux/tmux/wiki)

**Project News**: [OpenBSD Updates](https://www.openbsd.org/plus.html) • [Terminal Multiplexer News](https://en.wikipedia.org/wiki/Terminal_multiplexer) • [Community Blogs](https://thoughtbot.com/blog/tags/tmux)

**Community**: [tmux Mailing List](https://groups.google.com/g/tmux-users) • [Discussion Forums](https://www.reddit.com/r/tmux/) • [IRC Channel](https://web.libera.chat/#tmux)