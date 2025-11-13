---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #022: eBPF in Kubernetes"
slug: 00022-ebpf-kubernetes
---

# eBPF in Kubernetes: Kernel-Level Superpowers Without the Risk

## The Platform Engineering Playbook Podcast

<GitHubButtons />

<iframe width="560" height="315" src="https://www.youtube.com/embed/dPciRagOmig" title="eBPF in Kubernetes: Kernel-Level Superpowers Without the Risk" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

**Duration:** 32 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Platform engineers managing Kubernetes clusters, SREs debugging performance and security issues, DevOps engineers with 5+ years experience

## Listen to the Episode

<audio controls style={{width: '100%', marginBottom: '1.5rem'}}>
  <source src="https://platformengineeringplaybook.com/media/podcasts/00022/00022-ebpf-kubernetes.mp3" type="audio/mpeg" />
  Your browser does not support the audio element.
</audio>

<PodcastSubscribeButtons />

---

**Jordan**: Today we're diving into eBPF in Kubernetes. And I know what you're thinking—"another observability tool." But this is different. This is about running code inside the Linux kernel to see what's actually happening in your containers.

**Alex**: And that sounds terrifying, right? Running custom code in kernel space? But that's exactly why eBPF is revolutionary. It gives you kernel-level visibility without the traditional risks.

**Jordan**: Okay, so paint me the scenario. Why do I need this when I already have Prometheus, logs, and APM tools?

**Alex**: Imagine it's three AM. Your on-call pager goes off. One of your pods is pegged at eighty percent CPU. You check Prometheus—yep, CPU is high. You check application logs—nothing unusual. You check your APM tool—request counts look normal.

**Jordan**: Classic blind spot. I know the symptom but not the cause.

**Alex**: Exactly. In the old days, you'd reach for strace to see system calls. But strace adds fifty percent overhead and requires restarting the pod. Or tcpdump to see network packets, but you can't run that without privileged access and it impacts performance. Or perf for CPU profiling, but again—overhead, restart, security concerns.

**Jordan**: So we're stuck with symptoms because the diagnostic tools are too invasive for production.

**Alex**: That's the traditional tradeoff. And it's because Kubernetes and containers have created this multi-layered abstraction. Your app runs in a container, which runs in a pod, which runs on a node, which runs a Linux kernel. And all the interesting stuff—syscalls, network packets, file I/O, scheduler decisions—that all happens in kernel space.

**Jordan**: And traditional monitoring tools are all in user space, looking at the kernel from the outside.

**Alex**: Right. Prometheus scrapes metrics your app exports. Logs are what your app chooses to write. But what if your app isn't logging the right thing? What if the bottleneck is in the kernel's network stack, or the scheduler, or how containers are sharing resources?

**Jordan**: Okay, so eBPF solves this. How?

**Alex**: This is where it gets fascinating. eBPF stands for Extended Berkeley Packet Filter. It started as a way to filter network packets—hence the name—but it's evolved into a full programmable platform inside the Linux kernel.

**Jordan**: Wait, programmable? You're writing programs that run in kernel space?

**Alex**: Yes, but here's the key—safely. Think of it like JavaScript in a browser. The browser runs JavaScript code from untrusted websites without letting that code crash your operating system. eBPF does the same thing for the kernel.

**Jordan**: Okay, I need you to unpack that. Because normally, running code in the kernel means writing a kernel module in C, compiling it for the exact kernel version, loading it, and praying you didn't introduce a kernel panic.

**Alex**: Exactly. That's the old model and it's terrifying for production. eBPF flips this completely. You write your eBPF program—usually in a restricted subset of C—and when you try to load it into the kernel, it goes through a verifier.

**Jordan**: A verifier. What does that do?

**Alex**: It statically analyzes your program before it ever runs. It checks that there are no infinite loops—every loop must have a bounded maximum iteration count. It checks that you can't dereference null pointers or access memory outside your allowed bounds. It checks that your program will terminate in a reasonable number of instructions.

**Jordan**: So it's like a security sandbox, but at the kernel level.

**Alex**: Exactly. And if your program passes verification, the kernel uses a Just-In-Time compiler to turn it into native machine code. Then it attaches your program to specific kernel events—tracepoints, kprobes, network hooks, whatever you've specified.

**Jordan**: Okay, hold on. Attach points. What are we talking about here?

**Alex**: In modern Linux kernels, there are thousands of attach points. Tracepoints are stable instrumentation points the kernel developers have placed in the code—like when a process is created, or when a network packet arrives, or when a file is opened. Kprobes let you attach to almost any kernel function, though they're less stable across kernel versions.

**Jordan**: And once attached, what does the eBPF program actually do?

**Alex**: It runs every time that event fires. So if you attach to the system call for open—the open syscall—your eBPF program runs every single time any process on the system opens a file. And you can inspect the arguments, read the filename, see which process is making the call, and decide what data to collect.

**Jordan**: Every single time? That sounds like it would be incredibly expensive.

**Alex**: That's the other part of the magic. eBPF programs are highly optimized and run entirely in kernel space. The overhead is typically less than five percent, often much lower. Compare that to strace which can double your application's CPU usage.

**Jordan**: So let me make sure I understand the technical flow. I write an eBPF program in restricted C. The verifier checks it's safe. The JIT compiler turns it into machine code. I attach it to kernel events—syscalls, network hooks, whatever. And then it runs in kernel space with minimal overhead.

**Alex**: Exactly. And here's where it gets practical for Kubernetes. eBPF programs can store data in special kernel data structures called BPF maps. These are key-value stores that live in kernel memory and can be read from user space.

**Jordan**: So the eBPF program in kernel space collects data and writes it to BPF maps, and then my user-space tool reads from those maps.

**Alex**: Precisely. And this is how tools like Cilium, Pixie, and Falco work. They load eBPF programs into the kernel to collect data, then their user-space components read that data and present it to you.

**Jordan**: Alright, let's talk about those three pillars you mentioned—observability, networking, and security. Start with observability. What can I actually see?

**Alex**: Let's take a concrete example. Pixie is an observability tool that uses eBPF to auto-instrument your applications. Without any code changes, without sidecars, without language agents, it can see HTTP requests, gRPC calls, DNS queries, MySQL queries, Redis commands.

**Jordan**: How? Those are all application-layer protocols.

**Alex**: Because it hooks system calls. When your application makes an HTTP request, it ultimately calls read and write syscalls to send and receive data over a socket. Pixie's eBPF programs hook those syscalls, inspect the data being read and written, and parse the application protocols right there in kernel space.

**Jordan**: Wait, it's parsing HTTP in the kernel?

**Alex**: Yep. It knows you're sending HTTP because it sees you're writing to a TCP socket, and it can read the first few bytes of the data to identify the HTTP method and path. Same for gRPC, which runs over HTTP2. Same for database protocols—it sees the socket type and the protocol handshake.

**Jordan**: That's wild. So from the kernel's perspective, it doesn't matter that I'm running containerized microservices with twelve different languages. It just sees syscalls.

**Alex**: Exactly. And this is why eBPF is so powerful in Kubernetes. Containers are just processes with fancy namespaces and cgroups. From the kernel's perspective, they're not special. So eBPF programs see all processes—containerized or not—and can filter and tag events by container ID, pod name, Kubernetes namespace.

**Jordan**: How does it map from a Linux process ID to a Kubernetes pod?

**Alex**: The eBPF program can read cgroup information from the kernel, which tells it which container a process belongs to. Then the user-space component queries the Kubernetes API to map that container ID to a pod name, namespace, labels, all that metadata.

**Jordan**: Okay, that makes sense. What about the networking pillar?

**Alex**: This is where eBPF really shines. Traditional Kubernetes networking uses iptables. Every time you create a Service or a Network Policy, Kubernetes translates that into iptables rules. And iptables processes packets linearly—it checks rule one, rule two, rule three, until it finds a match.

**Jordan**: And if you have hundreds of Services, you have thousands of iptables rules.

**Alex**: Right. Performance degrades linearly with the number of rules. Cilium replaces this entire iptables-based model with eBPF programs attached to the network stack. Instead of linear rule evaluation, it uses BPF maps—essentially hash tables—for constant-time lookups.

**Jordan**: So what's the practical difference?

**Alex**: In benchmarks, Cilium can process ten million packets per second where iptables handles one to two million on the same hardware. Two to three x faster. And the performance stays constant as you scale Services, whereas iptables degrades.

**Jordan**: How does it replace kube-proxy? What's the technical mechanism?

**Alex**: Cilium loads eBPF programs at two key points in the network stack. First, there's an XDP—eXpress Data Path—program that runs at the network driver level, before the packet even reaches the kernel's network stack. This is the earliest possible point to process a packet and it's incredibly fast.

**Jordan**: What does the XDP program do?

**Alex**: It can drop, redirect, or pass packets. For example, if a packet is destined for a Kubernetes Service IP, the XDP program can rewrite the destination IP to one of the backend pod IPs directly at the driver level. It's doing load balancing before the packet even enters the kernel.

**Jordan**: And the second attach point?

**Alex**: The Traffic Control—TC—layer. After the network stack processes a packet, before it's delivered to the application, there's a TC eBPF program that handles policy enforcement. This is where Kubernetes Network Policies are implemented—allow or deny based on pod labels, namespaces, ports.

**Jordan**: And because it's in kernel space, using eBPF's efficient maps, it's much faster than iptables.

**Alex**: Exactly. And there's another benefit—visibility. Because the eBPF programs see every packet, Cilium's Hubble component can generate a real-time service map. It knows which pods are talking to which, over which ports, with which protocols. All without adding sidecars or changing your application.

**Jordan**: Let's talk about security. What does eBPF give you there?

**Alex**: Runtime security and threat detection. The classic example is Falco. It uses eBPF to monitor syscalls and detect anomalous behavior. Like, if a container suddenly spawns a shell—execve calling /bin/bash—when it's never done that before, that's suspicious.

**Jordan**: How does it know what's normal versus anomalous?

**Alex**: Falco ships with a rule engine. You can write rules like "alert if a container in the web namespace executes a shell" or "alert if any process reads /etc/shadow" or "alert if a container makes an unexpected outbound network connection."

**Jordan**: So it's behavioral detection based on kernel-level visibility.

**Alex**: Right. And this catches attacks that application-level tools miss. Like, if an attacker exploits a vulnerability in your PHP application and spawns a reverse shell, traditional application monitoring won't see it—the app isn't logging that. But Falco sees the execve syscall and knows something's wrong.

**Jordan**: What about Tetragon? How's that different from Falco?

**Alex**: Tetragon goes a step further—enforcement, not just detection. Falco alerts you when something bad happens. Tetragon can block it from happening. You can write policies like "containers in this namespace cannot execute shells" and Tetragon will kill the process before it runs.

**Jordan**: So it's using eBPF to implement a kernel-level security policy.

**Alex**: Exactly. It hooks into the kernel's security subsystems and can deny operations before they complete. It's similar to something like SELinux or AppArmor, but easier to configure because you're writing policies in terms of Kubernetes constructs—pods, namespaces, labels.

**Jordan**: Okay, let's talk about the Kubernetes-specific integration. You mentioned mapping processes to pods. Walk me through how that works technically.

**Alex**: So every Linux process belongs to a set of cgroups. When Kubernetes creates a pod, it creates a cgroup hierarchy for that pod's containers. The eBPF program running in the kernel can read the cgroup path from the process metadata.

**Jordan**: And that cgroup path contains the pod ID?

**Alex**: Yep. It looks something like /kubepods/besteffort/pod-abc123/container-id. The eBPF program parses that path to extract the pod ID. It stores events in BPF maps with the pod ID as part of the key.

**Jordan**: And then the user-space component reads those maps and correlates with Kubernetes?

**Alex**: Right. The user-space component watches the Kubernetes API to maintain a mapping of pod IDs to pod names, namespaces, labels, and all the Kubernetes metadata. When it reads events from the BPF maps, it enriches them with that metadata before displaying to you.

**Jordan**: So I can filter by Kubernetes namespace, or by pod label, even though all the actual data collection is happening at the kernel level.

**Alex**: Exactly. And this works seamlessly across different container runtimes—Docker, containerd, CRI-O—because from the kernel's perspective, they all create processes with cgroups. eBPF doesn't care about the runtime abstraction layer.

**Jordan**: What about kernel version requirements? You mentioned Linux five point zero. What if my cluster is running older kernels?

**Alex**: That's a real constraint. eBPF has been in the Linux kernel since three point eighteen, but the feature set has evolved dramatically. Linux four point nine added important networking and cgroup capabilities. Five point ten added BTF—BPF Type Format—which provided type information for kernel structures. And five point seventeen added full CO-RE support—Compile Once, Run Everywhere—which makes eBPF programs truly portable across kernel versions.

**Jordan**: What does portable mean here?

**Alex**: Before CO-RE, you had to compile your eBPF program for each specific kernel version because internal kernel data structures change between versions. With CO-RE, the eBPF program includes metadata about what fields it's accessing, and the loader rewrites the program at load time to match the running kernel.

**Jordan**: So I can ship one eBPF program that works on all kernel versions five point seventeen and above?

**Alex**: In theory, yes. In practice, most production tools aim for four point nine or newer to maximize compatibility, and they handle differences between kernel versions in their user-space code.

**Jordan**: What's the situation with managed Kubernetes? EKS, GKE, AKS?

**Alex**: Generally good. EKS moved to Linux five point four in early twenty twenty-two for Kubernetes one point twenty-one and later. GKE uses COS—Container-Optimized OS—which has been on Linux five point x since twenty twenty. AKS uses Ubuntu by default, which has been on five point four since twenty twenty-one.

**Jordan**: So if I'm on a recent managed Kubernetes version, I'm probably fine.

**Alex**: Yep. But if you have older clusters or you're running on-prem with custom kernels, you need to check. Run uname dash r to see your kernel version.

**Jordan**: Let's talk practical adoption. If I'm running a Kubernetes cluster today and I want to start using eBPF tools, where do I start?

**Alex**: I'd stratify it by risk and complexity. Low risk, high value—start with Parca for continuous profiling. It uses eBPF to sample stack traces across your entire cluster and builds CPU flame graphs. It's read-only, low overhead, and immediately useful for performance optimization.

**Jordan**: What's low overhead mean in concrete terms?

**Alex**: Parca samples stack traces a hundred times per second across all CPU cores. That's negligible CPU impact—usually less than one percent—but you get cluster-wide visibility into where CPU time is spent. Which functions are hot, which code paths are slow.

**Jordan**: And it works without instrumenting my application.

**Alex**: Correct. It's hooking the kernel's perf events subsystem via eBPF. Sees all processes, including ones you can't easily instrument like third-party binaries or database servers.

**Jordan**: What's next after profiling?

**Alex**: Falco for security. Again, it's detection only—not enforcement—so it's low risk. You deploy it as a DaemonSet, it loads its eBPF programs on each node, and starts alerting on suspicious behavior based on rules you configure.

**Jordan**: What does a Falco deployment look like in terms of resource usage?

**Alex**: The eBPF programs themselves are very lightweight. The Falco user-space process uses about fifty to one hundred megabytes of memory per node and one to three percent CPU depending on syscall volume. The actual impact depends on how many rules you have and how verbose your logging is.

**Jordan**: And you're getting alerts to where? Slack, PagerDuty?

**Alex**: Falco outputs events as JSON logs or to a gRPC endpoint. You can forward those to your existing log aggregation system—Elasticsearch, Splunk, whatever—or integrate with Falco Sidekick which has plugins for Slack, PagerDuty, AWS Security Hub, all the usual suspects.

**Jordan**: Okay, so profiling and security detection are relatively safe starting points. What's medium complexity?

**Alex**: Pixie for application observability. This is more involved because Pixie stores a bunch of data locally—it's essentially running a columnar datastore on each node to keep recent traces and metrics. You'll need persistent volumes and you'll want to think about resource limits.

**Jordan**: What's the resource footprint?

**Alex**: Pixie's collector uses about five hundred megabytes to one gigabyte of memory per node and three to five percent CPU. Plus whatever you allocate for persistent storage—default is ten gigabytes per node for data retention.

**Jordan**: And what do I get for that?

**Alex**: Zero-instrumentation distributed tracing. You can see HTTP request flows across services, gRPC calls, database queries, DNS lookups, all with no code changes. It's like having a full APM tool but you didn't have to add agents or libraries to your applications.

**Jordan**: Where does it fall short compared to something like Jaeger or Tempo?

**Alex**: Retention is limited—usually hours, not days or weeks, because it's storing data locally on nodes. And the protocol coverage is good but not exhaustive—it handles HTTP, gRPC, DNS, MySQL, PostgreSQL, Redis, Cassandra, MongoDB. If you have exotic protocols, it might miss them.

**Jordan**: So it's great for real-time debugging but not long-term analysis.

**Alex**: Exactly. It complements traditional distributed tracing rather than replacing it. Use Pixie for "what's happening right now" and a traditional tracing system for historical analysis and long-term trends.

**Jordan**: And the high-complexity option is Cilium as your CNI.

**Alex**: Right. This is an architectural decision. You're replacing your entire networking layer—Calico, Flannel, whatever you're using—with Cilium. That requires planning, testing, and a migration strategy.

**Jordan**: What does a migration look like?

**Alex**: For a new cluster, it's straightforward—you install Cilium from the start. For an existing cluster, you'd typically set up a parallel cluster with Cilium, migrate workloads, then decomm the old cluster. In-place migration is risky because you're swapping out the foundation of pod networking.

**Jordan**: When does Cilium make sense versus staying with iptables-based CNI?

**Alex**: If you have network performance problems—high packet rates, lots of Services, complex Network Policies—Cilium delivers measurable improvements. Also if you want advanced features like transparent encryption between pods, L7-aware Network Policies, or multi-cluster networking.

**Jordan**: L seven Network Policies. What does that mean?

**Alex**: Traditional Network Policies work at Layer four—IP addresses and ports. Cilium can enforce policies at Layer seven because its eBPF programs parse HTTP, gRPC, Kafka, whatever protocol. So you can say "pod A can only make GET requests to path /api/users on pod B" instead of just "pod A can talk to pod B on port eight thousand."

**Jordan**: That's... that's a different level of granularity.

**Alex**: Yep. And it's fast because the policy enforcement is happening in kernel space with eBPF, not in a sidecar proxy like a service mesh would require.

**Jordan**: Speaking of which, how does Cilium compare to something like Istio or Linkerd?

**Alex**: They solve overlapping but different problems. Service meshes give you traffic management—retries, timeouts, circuit breaking—plus observability and security. Cilium gives you high-performance networking, network policy enforcement, and observability, but not the traffic management layer.

**Jordan**: Can you run them together?

**Alex**: Yes. You can use Cilium as your CNI for fast networking and Istio for application-level traffic management. Some people do this. But there's overlap in observability and security features, so you'd need to think through which tool is doing what.

**Jordan**: Let's talk about debugging. If something goes wrong with an eBPF program, how do you troubleshoot it?

**Alex**: That's one of the pain points. eBPF programs run in kernel space, so you don't have your usual debugging tools. Most eBPF programs emit logs via bpf_printk which writes to the kernel trace buffer. You can read it with tools like bpftool or by reading /sys/kernel/debug/tracing/trace_pipe.

**Jordan**: That sounds primitive compared to application debugging.

**Alex**: It is. The verifier helps a lot because it catches many errors before your program ever runs. But if you have a logic bug—like you're filtering the wrong events or parsing data incorrectly—you're stuck adding print statements and reloading your program.

**Jordan**: What about performance debugging? How do I know if my eBPF program is adding too much overhead?

**Alex**: You can use the BPF statistics interface to see how many times each program has run and how much CPU time it's consumed. The command bpftool prog show gives you stats per program. If you see one program consuming a lot of CPU, you know you need to optimize it.

**Jordan**: Is there a risk of eBPF programs themselves becoming a performance bottleneck?

**Alex**: Absolutely. If you attach a complex eBPF program to a super high-frequency event—like every network packet on a ten-gigabit interface—and the program does a lot of work, you can slow down your network. The key is to filter early and do minimal work in the hot path.

**Jordan**: So the best practice is keep the kernel-space eBPF program simple and move complex processing to user space.

**Alex**: Exactly. Collect only the data you need in kernel space, write it to BPF maps, and do aggregation and analysis in user space where it's easier to debug and optimize.

**Jordan**: Let's talk about the ecosystem. Beyond Cilium, Pixie, and Falco, what other eBPF tools should people know about?

**Alex**: Tetragon for enforcement-level security, which we touched on. Parca for profiling. There's also bpftrace—it's like a scripting language for eBPF. You can write one-liners to answer ad-hoc questions, like "show me all processes opening /etc/passwd" or "histogram of disk I/O latencies."

**Jordan**: That sounds like it's for interactive troubleshooting.

**Alex**: Exactly. It's not something you'd deploy in production long-term, but when you're debugging a specific issue, bpftrace lets you quickly write an eBPF program to investigate.

**Jordan**: What about commercial tools? Is this just open-source, or are vendors building on eBPF?

**Alex**: Oh, vendors are all-in. Datadog's agent uses eBPF for network performance monitoring. New Relic acquired Pixie. Isovalent, the company behind Cilium, offers Cilium Enterprise with support. Grafana's Phlare uses eBPF for profiling. Microsoft's Retina uses eBPF for AKS networking diagnostics.

**Jordan**: So this is a foundational technology, not a niche thing.

**Alex**: Absolutely. Google has said that all of their production infrastructure uses eBPF for networking and observability. Same with Meta. It's become a core part of how you run infrastructure at scale.

**Jordan**: What about the learning curve? If I'm a platform engineer comfortable with Kubernetes but I've never touched eBPF, what do I need to know?

**Alex**: You don't need to write eBPF programs to use eBPF tools. Tools like Cilium and Falco handle all the eBPF complexity for you. You just install them and configure policies or rules in YAML.

**Jordan**: But if I want to understand what's actually happening under the hood?

**Alex**: Then you need some kernel knowledge. Understand what system calls are, how the network stack works, how processes and threads are scheduled. You don't need to be a kernel developer, but you need to think in terms of kernel events rather than just application behavior.

**Jordan**: And if I want to write my own eBPF programs?

**Alex**: Start with bpftrace for simple scripts. Then look at libbpf, the official C library for writing eBPF programs. Or use higher-level frameworks like BPF Compiler Collection—BCC—which lets you write eBPF programs in Python with the kernel code embedded as C strings.

**Jordan**: That sounds... kind of hacky.

**Alex**: It is, but it's a stepping stone. BCC handles a lot of the boilerplate and makes it easier to get started. Once you understand the concepts, you can move to pure libbpf for production tools.

**Jordan**: What's the maintenance burden? If I deploy Cilium or Falco, how much ongoing work is it?

**Alex**: Fairly low. These tools are designed to be Kubernetes-native. You upgrade them with Helm or your GitOps pipeline like any other workload. The eBPF programs themselves are loaded and unloaded automatically—you don't manage them manually.

**Jordan**: What about kernel upgrades? If my cloud provider updates the kernel, do I need to do anything?

**Alex**: Nope. Thanks to CO-RE, the tools automatically adjust when they detect a new kernel version. You might see a brief restart of the DaemonSet pods as they reload their eBPF programs, but it's seamless.

**Jordan**: Alright, let's bring this back to practical guidance. I'm running a Kubernetes cluster. Maybe I'm seeing performance issues or security concerns. How do I decide if eBPF tools are the right answer?

**Alex**: Ask yourself: Do I have visibility gaps that user-space tools can't fill? Are network policies slow or hard to debug? Do I need runtime security monitoring? If yes to any of those, eBPF is worth exploring.

**Jordan**: And the path is start small—profiling and detection tools—before committing to architectural changes like Cilium.

**Alex**: Exactly. Parca for profiling, Falco for security alerts. Both are low-risk, high-value. Once you're comfortable with those, consider Pixie for application observability if you have gaps in your distributed tracing.

**Jordan**: And Cilium only if you have specific network performance problems or need advanced features.

**Alex**: Right. Don't replace your CNI just because eBPF is cool. But if you're running thousands of Services, or you need sub-millisecond latency, or you want Layer seven Network Policies, then Cilium makes sense.

**Jordan**: What about the big picture? Where does eBPF fit in a modern observability stack?

**Alex**: It fills the kernel-level visibility gap. You still need Prometheus for metrics, distributed tracing for request flows, logs for application events. But eBPF gives you the missing piece—what's happening at the system level, in the kernel, that your application can't see.

**Jordan**: So it's complementary, not a replacement.

**Alex**: Exactly. The modern stack is Prometheus for metrics, a tracing system like Tempo or Jaeger for distributed traces, a log aggregator like Loki or Elasticsearch, and eBPF-based tools for kernel and network visibility. Together, they give you complete observability.

**Jordan**: Last question. Where is eBPF headed? What's coming next?

**Alex**: More protocol support—every eBPF tool is adding parsers for new protocols. Better integration with Kubernetes constructs—like policies based on service accounts or admission control. And I think we'll see eBPF used for things beyond observability and networking, like storage I/O optimization or even scheduling decisions.

**Jordan**: So it's not just a monitoring tool. It's a platform for making the kernel programmable.

**Alex**: That's the key insight. eBPF turns the Linux kernel from a static black box into a programmable platform. And in a world where everything runs in containers on Kubernetes, having that kernel-level programmability is a superpower.

**Jordan**: Alright, let's wrap this up. If you're running Kubernetes and you've been frustrated by visibility gaps—can't debug network issues, can't profile performance without overhead, can't detect security anomalies—eBPF tools give you kernel-level superpowers. Start small with profiling and security detection. Understand what's happening under the hood, but don't feel like you need to write eBPF programs yourself. And remember, this is about filling the kernel visibility gap that containers created—it's not replacing your existing observability stack, it's completing it.

**Alex**: And check your kernel version first. You need at least Linux four point nine, preferably five point zero or newer, to get the full eBPF feature set. Most managed Kubernetes providers are already there, but if you're on-prem or running older clusters, that's your first step.

**Jordan**: eBPF—from black box to programmable kernel, with tools like Cilium, Pixie, and Falco bringing kernel-level visibility to Kubernetes without the traditional risks.
