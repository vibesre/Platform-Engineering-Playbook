---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #034: The GPU Waste Problem"
slug: 00034-kubernetes-gpu-cost-waste-finops
---

# The $4,350/Month GPU Waste Problem: How Kubernetes Architecture Creates Massive Cost Inefficiency

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 28 minutes
**Speakers:** Jordan and Alex
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience managing Kubernetes GPU workloads, FinOps practitioners optimizing AI/ML infrastructure costs

> 📝 **Read the [full blog post](/blog/2025/11/24/kubernetes-gpu-resource-management-finops-ai-workloads-2025)**: Comprehensive guide to GPU cost optimization with YAML configurations, implementation checklists, and complete MIG setup examples for production Kubernetes clusters.

<iframe width="560" height="315" src="https://www.youtube.com/embed/LJBT-a9CuXw" title="The $4,350/Month GPU Waste Problem: How Kubernetes Architecture Creates Massive Cost Inefficiency" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

---

**Jordan**: Alex, I want to start with a number that should make every platform engineer's stomach drop. Thirteen percent.



**Alex**: Thirteen percent GPU utilization?



**Jordan**: Exactly. Analysis of over four thousand Kubernetes clusters revealed that the average GPU utilization is thirteen percent. And we're not talking about cheap hardware here. H100s cost five thousand dollars a month on AWS. At thirteen percent utilization, you're burning forty-three hundred and fifty dollars every single month per GPU on idle capacity.



**Alex**: Wait, that's not an edge case? That's the average?



**Jordan**: That's the average. And it gets worse. Organizations are wasting sixty to seventy percent of their entire GPU budget on idle resources. Now scale that. Ten H100s at thirteen percent? You're burning forty-three thousand five hundred dollars a month. A hundred-node cluster? The waste becomes existential.



**Alex**: Okay, so the instinct is to think this is a developer problem, right? People requesting resources they don't need, poor monitoring, that kind of thing?



**Jordan**: That was my first thought too. But here's what's counterintuitive—this is actually a Kubernetes architecture problem, not a user error. The same clusters running seventy to eighty percent CPU utilization are sitting at thirteen percent GPU utilization. Same teams, same workloads, completely different resource efficiency. So what's different about GPUs?



**Alex**: Right, because if it were a monitoring or discipline problem, you'd see it across all resource types. So this has to be something fundamental about how Kubernetes handles GPUs versus CPUs and memory.



**Jordan**: Exactly. And that's what we're diving into today. We're going to uncover why Kubernetes creates this waste—and it is architectural, it's baked into how the scheduler works—and then we'll walk through the specific techniques that can recover seventy-five to ninety-three percent of that lost capacity in ninety days.



**Alex**: Seventy-five to ninety-three percent recovery? That's the difference between "we need more GPUs" and "we're actually fine with what we have."



**Jordan**: Precisely. Most platform teams think they have a capacity problem when they actually have a waste problem. And once you understand the root cause, the solutions become obvious. So let's start with why Kubernetes treats GPUs so differently.



**Alex**: Alright, I'm ready for this. Because honestly, every GPU workload I've deployed has felt weirdly inefficient, but I never connected it to Kubernetes itself.



**Jordan**: Here's the core issue. Unlike CPU and memory, GPUs in Kubernetes are atomic resources. They're non-divisible, non-shareable, and non-overcommittable. The official Kubernetes documentation states it explicitly—"Containers do not share GPUs. There's no overcommitting of GPUs. It is not possible to request a fraction of a GPU."



**Alex**: Wait, hold on. So when a pod requests nvidia dot com slash gpu colon one, it locks the entire GPU? Even if it's only using five percent of the capacity?



**Jordan**: The entire GPU. The remaining ninety-five percent sits idle, completely unusable by other pods. And here's the kicker—the Kubernetes scheduler sees that GPU as "allocated." It won't schedule any other GPU-requesting pods on that node. It's binary. Either allocated or available. No middle ground.



**Alex**: Okay, but why? That seems like a massive design flaw for AI and ML workloads.



**Jordan**: It made perfect sense for the original use case—gaming and graphics workloads where you need exclusive full GPU access. But AI and ML workloads have variable utilization. A training job might use twenty percent of the GPU for hours, blocking everything else. Meanwhile, CPUs can hit seventy to eighty percent utilization in the same cluster because Kubernetes can overcommit CPU resources.



**Alex**: Right, Kubernetes can schedule more CPU requests than physical cores because not everything maxes out simultaneously. But with GPUs, there's no overcommitment, so any underutilization becomes direct waste.



**Jordan**: Exactly. And this creates absurd situations. I saw an ML training pipeline that requested a full H100, used eight gigabytes of the eighty-gigabyte GPU memory, and blocked other workloads for hours. That single job cost five thousand dollars a month. With Multi-Instance GPU—which we'll cover in a bit—you could run seven jobs on that same H100. That's seven hundred fourteen dollars per job versus five thousand.



**Alex**: So the architecture that works brilliantly for CPU and memory actively creates waste for GPUs. That explains the thirteen percent average. But I'm guessing there's more to the story?



**Jordan**: Oh yeah. Discovery two is that round-number overprovisioning compounds this problem massively. Teams default to "safe" round numbers without any load testing. Memory sixteen gigabytes when P99 usage is four point two gigs. CPU four thousand millicores when P95 usage is twelve hundred. And of course, nvidia dot com slash gpu colon one when the workload could actually share via MIG.



**Alex**: The classic "just make it bigger to be safe" approach. Which hurts with CPU and memory but doesn't kill you because of overcommitment. With GPUs though—



**Jordan**: With GPUs, you're paying real money for that safety margin. nOps research found that developers routinely choose easy round numbers—five hundred millicores, one gigabyte of memory—without any load testing. And the reason is fear. OOMKilled incidents are visible and painful. But at five thousand dollars a month per GPU, being "safe" with a three-x overprovision costs you ten to fifteen thousand dollars a month in waste.



**Alex**: And I bet most teams don't even have the Vertical Pod Autoscaler running to get actual P95 and P99 metrics, so they're just guessing.



**Jordan**: Most teams deploy without VPA in recommendation mode. They have no idea what their workloads actually consume. So they guess conservatively. Here's the counterintuitive math. Conservative approach? Three-x overprovisioned H100 equals fifteen thousand a month. Properly sized based on P99 data? Five thousand a month, plus maybe two OOMKilled restarts per month with ten minutes of downtime each. For non-critical training workloads, that's negligible SLA impact to save ten thousand dollars per GPU per month.



**Alex**: So let me make sure I understand this. The GPU itself is atomic, which creates the thirteen percent baseline waste. Then teams overprovision on CPU and memory around that GPU without measurements, which means even when the GPU is "allocated," it's sitting idle because the pod doesn't have enough CPU or memory to keep it busy?



**Jordan**: You've got it. And research shows that load testing typically reveals actual P99 usage is three to four times lower than requested resources. At a hundred pods, you might size for sixteen hundred gigabytes of RAM when you actually need four hundred twenty gigs. With CPUs, Kubernetes overcommits, so some of that waste is hidden. With GPUs, it's waste you're directly paying for in hardware you can't use.



**Alex**: Okay, this is starting to paint a grim picture. Atomic resources plus overprovisioning. What's discovery three?



**Jordan**: Regional arbitrage and Spot instances. Platform teams anchor on AWS us-east-1 on-demand pricing and miss two to five-x cost differences across regions and seventy to ninety percent Spot savings.



**Alex**: Wait, two to five-x differences? That's not just a margin, that's choosing the wrong region literally doubling or tripling your costs.



**Jordan**: Cast AI's twenty twenty-five GPU price report breaks this down. Specialized GPU providers charge two dollars and ten cents an hour for H100s. AWS on-demand in us-east-1? Four dollars and nine cents an hour. That's basically double. And regional variance—us-east-1 versus us-west-2 versus eu-central-1—can differ by forty to sixty percent for the same hardware.



**Alex**: So here's a real scenario. Team A runs ten H100s in us-east-1 at four oh nine an hour for seven hundred twenty hours a month. That's twenty-nine thousand four hundred dollars a month. Team B runs the same ten H100s in eu-central-1 at two sixty an hour. Eighteen thousand six hundred a month. The difference is ten thousand eight hundred dollars a month just from picking a different region.



**Jordan**: And the typical objection is "but our training data lives in us-east-1 S3." Fine. The one-time data transfer cost for ten terabytes is five hundred dollars at five cents per gigabyte. That pays for itself in one point four days of regional savings.



**Alex**: Okay, and what about Spot instances? I hear this all the time—"Spot instances get interrupted, we can't use them for training."



**Jordan**: That's the myth. Here's the reality. Modern ML frameworks like PyTorch and TensorFlow support checkpointing every N steps. Average Spot interruption? Once every six to twenty hours depending on the region. If you're checkpointing hourly, you lose a maximum of one hour of progress when interrupted.



**Alex**: And the cost difference?



**Jordan**: Sixty cents an hour Spot versus four dollars an hour on-demand for A100s. Even if you account for twenty percent interruption overhead—meaning you lose twenty percent of your time restarting from checkpoints—your effective cost is seventy-two cents versus four dollars. That's eighty-two percent savings.



**Alex**: So the objection is really "we haven't set up checkpointing," not "Spot doesn't work for training."



**Jordan**: Exactly. And for production inference, you use a hybrid strategy. Spot for training where checkpointing is tolerable. On-demand for production inference where you have SLA requirements. One e-commerce company ran seventy percent Spot for training and thirty percent on-demand for inference. Total cost reduction fifty-eight percent with zero customer-facing SLA impact.



**Alex**: Alright, so we've uncovered the why. Kubernetes architecture makes GPUs atomic. Teams overprovision without measurements. And they anchor on expensive regions and on-demand pricing. How do we actually fix this?



**Jordan**: The solution is a five-layer approach. It's not one tool or technique. You need all five layers working together. Layer one is Kubernetes resource configuration fundamentals. Layer two is Multi-Instance GPU for production workloads. Layer three is time-slicing for development. Layer four is FinOps visibility and pod-level cost tracking. Layer five is model optimization to reduce GPU requirements altogether.



**Alex**: Let's walk through each one. Start with layer one—Kubernetes resource configuration.



**Jordan**: Four critical elements. First, GPU limits. Unlike CPU and memory, you specify GPUs only in the limits section. Kubernetes automatically sets the request equal to the limit. You don't need to specify requests at all for GPUs. This trips people up because it's different from the CPU and memory pattern.



**Alex**: Right, with CPU and memory you usually set both requests and limits separately. With GPUs, it's limits-only and Kubernetes handles the rest.



**Jordan**: Exactly. Second element—node taints on GPU nodes. You taint your GPU nodes with nvidia dot com slash gpu equals true with NoSchedule effect. This prevents non-GPU workloads from scheduling on expensive GPU hardware.



**Alex**: And Cast AI found that in misconfigured clusters, thirty percent of pods running on GPU nodes don't even use GPUs. They're just random sidecars, logging agents, cron jobs sitting on hardware that costs ten to twenty times more than CPU nodes.



**Jordan**: Thirty percent. That's pure waste. Third element is pod tolerations. Your GPU workloads need a matching toleration for that taint so they can schedule. And fourth is node affinity to ensure workloads land on the correct GPU type—H100 versus A100 versus T4.



**Alex**: Okay, so proper taints and tolerations alone can recover significant capacity. What's the impact?



**Jordan**: One startup case study. They ran twenty H100s at eighteen percent utilization, costing a hundred thousand a month. After implementing proper node taints, using VPA recommendations to right-size CPU and memory, and enabling MIG for production inference—which we're about to cover—they dropped to seven H100s at seventy-two percent utilization. Same production workload. Thirty-five thousand a month. Sixty-five thousand dollars in monthly savings without buying a single new GPU.



**Alex**: So layer two is MIG. Multi-Instance GPU. Walk me through how this actually works.



**Jordan**: MIG is NVIDIA's hardware-level feature for Ampere and Hopper GPUs—so A100, A30, and H100. It physically divides a single GPU into up to seven isolated instances, each with dedicated compute cores, memory, and cache.



**Alex**: And this is hardware partitioning, not virtualization, right? So each instance has real isolation.



**Jordan**: Correct. Each MIG instance gets its own streaming multiprocessors and memory slice. It's a physical division of the hardware. Kubernetes automatically discovers these as schedulable resources. You request nvidia dot com slash mig dash one g dot ten gb colon one in your pod spec, and the scheduler treats it like any other resource.



**Alex**: And the profiles? I know there are different sizes.



**Jordan**: For an A100 with eighty gigs of memory, you've got four main profiles. One g dot ten gb gives you one-seventh of the GPU with ten gigs of memory. You can fit seven instances per A100. Good for small model training or development. Two g dot twenty gb is two-sevenths of the GPU, twenty gigs of memory, three instances per A100. Works for medium models and batch inference. Three g dot forty gb is three-sevenths GPU, forty gigs memory, two instances. Large model fine-tuning. And seven g dot eighty gb is the full GPU for full-scale training.



**Alex**: So when do you use MIG versus dedicated GPUs?



**Jordan**: Use MIG for production inference where you need isolation—multi-tenant clusters, security requirements, guaranteed performance with no noisy neighbor effects. And for workloads where the model is under forty gigs and doesn't need maximum compute. Don't use MIG for models over forty gigs that need full GPU memory, or for distributed training that needs maximum compute power.



**Alex**: Real-world example?



**Jordan**: SaaS platform with fifty enterprise customers, each running isolated inference workloads. Before MIG, they ran fifty dedicated A100s, one per customer, for isolation. Cost twenty-three thousand seven hundred sixty a month minimum at specialized provider rates. After MIG, eight A100s with seven one-g-dot-ten-gb instances each gives them fifty-six isolated GPU instances. Cost thirty-eight hundred two a month. Savings? Nineteen thousand nine hundred fifty-eight dollars a month. Eighty-four percent reduction while maintaining hardware isolation between customers.



**Alex**: That's transformative for multi-tenant scenarios. What about layer three—time-slicing?



**Jordan**: Time-slicing is simpler than MIG but has different trade-offs. It lets multiple pods share a single GPU sequentially without hardware partitioning. There's no isolation. Workloads share the full GPU on a time-division basis.



**Alex**: So the NVIDIA device plugin makes Kubernetes think there are four GPUs when physically there's only one, and the scheduler assigns different pods to the same physical GPU?



**Jordan**: Exactly. The scheduler sees four resources, assigns four pods, but they're all sharing one physical GPU by taking turns.



**Alex**: Which means this is development-only, right? You wouldn't use this for production inference with latency SLAs.



**Jordan**: Never for production with SLAs. Use it for development environments only, with homogeneous workloads. Don't mix training and inference on the same time-sliced GPU because you'll get unpredictable latency. But for four data scientists sharing one H100 for development? You go from five thousand dollars per person per month to twelve hundred fifty per person. Seventy-five percent savings per developer. Combine that with Spot instances at seventy to ninety percent off, and you hit ninety-three percent total savings for dev environments.



**Alex**: Okay, so MIG for production multi-tenant workloads, time-slicing for development. Layer four is FinOps visibility. What changed there?



**Jordan**: AWS announced Split Cost Allocation Data for EKS in September twenty twenty-five. Pod-level GPU cost tracking is now available across all commercial regions at no additional cost.



**Alex**: And this calculates costs how?



**Jordan**: Pod-level costs equal your split-usage ratio times cost per GPU-hour. If there's unused capacity on the node, that gets proportionally distributed to the pods based on usage. So you see both your pod's direct costs and its share of the idle waste.



**Alex**: And you can tag by namespace, workload name, custom labels?



**Jordan**: Built-in tags include aws colon eks colon cluster-name, namespace, workload-name, node. You can add up to fifty custom Kubernetes labels—cost-center, team, environment, whatever you need. Then you track FinOps metrics. GPU utilization percentage with a target of sixty to eighty-five percent. Cost per inference—if you're above P95, you optimize batch size or quantize the model. Idle GPU hours should be under ten percent of total. And Spot adoption rate, targeting above fifty percent for training workloads.



**Alex**: This gives you the visibility to actually measure whether your optimizations are working. Before this, you're kind of flying blind on where the costs are accumulating.



**Jordan**: Exactly. And layer five is model optimization. Sometimes the best GPU optimization is needing fewer GPUs altogether. Quantization, pruning, distillation—these reduce your GPU memory and compute requirements without sacrificing model quality.



**Alex**: Quantization is reducing precision from thirty-two-bit floating point to eight-bit integers, right? What's the compression ratio?



**Jordan**: Four to eight-x compression with one to two percent accuracy loss for quick deployment approaches. Production-grade optimization that combines quantization with pruning can hit eight to fifteen-x compression with under one percent accuracy degradation. The key is you're not just shrinking the model randomly—you're intelligently removing parameters that have minimal impact on predictions and reducing precision where it doesn't hurt performance.



**Alex**: And when do you bother with this? Because it's engineering effort.



**Jordan**: High-volume inference. If you're serving over a million requests a day, the engineering time pays for itself quickly. Also edge deployment where you have memory constraints. And cost-sensitive applications where forty percent cost reduction matters to your margins. Example—GPT-3 with a hundred seventy-five billion parameters distilled down to a six-billion-parameter model. That's twenty-nine times smaller with an eight percent quality drop for question-and-answer tasks, but ninety-six percent inference cost reduction.



**Alex**: So if you're serving ten million queries a day, that's the difference between needing twenty A100s versus needing one A100. From fifty-seven thousand six hundred a month to twenty-eight hundred eighty a month.



**Jordan**: Exactly. Alright, let's bring this all together with a ninety-day implementation playbook. Because you can't do everything at once, and the order matters.



**Alex**: Start with the foundation, I'm guessing?



**Jordan**: Days one through thirty are foundation and measurement. Week one, you audit current state. GPU inventory with kubectl get nodes, figure out what types and how many. Pull your last three months of GPU spend from cloud billing. Deploy DCGM Exporter to Prometheus to start capturing GPU metrics. Query for GPUs sitting under thirty percent utilization for over six hours—that's your waste identification.



**Alex**: Week two is resource management baseline?



**Jordan**: Exactly. Add node taints to all GPU nodes with nvidia dot com slash gpu equals true NoSchedule. Deploy an admission controller with OPA Gatekeeper that requires GPU limits on all pods. And test that non-GPU pods actually can't schedule on GPU nodes by deploying a test workload without tolerations. It should stay pending.



**Alex**: Week three is VPA deployment?



**Jordan**: Install Vertical Pod Autoscaler and enable it in "Off" mode—recommendations only, no auto-updates. For all your GPU workloads, create VPA objects that collect data but don't automatically change pod specs. You need at least two weeks of data across different workload cycles before you trust the recommendations.



**Alex**: And week four is cost tracking. Enable AWS EKS Split Cost Allocation, activate the built-in tags, add custom labels to your GPU workloads, and build a Grafana dashboard showing GPU utilization per namespace, cost per namespace, idle GPU hours, and your top ten most expensive workloads.



**Jordan**: By day thirty, you've got baseline metrics, foundational controls in place, and VPA collecting real data. Days thirty-one through sixty is where you do optimization and GPU sharing.



**Alex**: Week five is right-sizing based on VPA?



**Jordan**: You look at VPA recommendations, compare current requests to what VPA measured for P95 and P99, and update your deployments with VPA recommended values plus twenty percent headroom. Roll out changes gradually—ten percent of workloads per day—and watch for OOMKilled events. If a workload OOMKills more than twice, bump memory by ten percent increments until it's stable.



**Alex**: Weeks six and seven are MIG implementation for production inference?



**Jordan**: Install the NVIDIA GPU Operator with MIG strategy set to mixed, configure MIG profiles starting with one-g-dot-ten-gb for inference workloads under ten gigs of GPU memory, migrate your production inference deployments to request those MIG resources, and validate that your performance SLAs are maintained. Compare p50, p95, p99 latency before and after. If degradation exceeds five percent, you roll back.



**Alex**: And week eight is time-slicing for development clusters?



**Jordan**: Identify your non-production environments, apply the time-slicing config to make Kubernetes think you have four or eight GPUs per physical GPU, and let your developers share the hardware. You're not touching production yet, just dev.



**Alex**: Days sixty-one through ninety are advanced optimization. Regional arbitrage analysis in week nine—compare H100 and A100 costs across regions, calculate data transfer costs to move to a lower-cost region, and determine ROI. Spot instance pilot in weeks ten and eleven for training jobs that have checkpointing and non-critical timelines. And week twelve is model optimization—identify high-volume models serving over a hundred thousand inferences a day, experiment with quantization using TensorRT or Hugging Face Optimum, and A-B test to measure accuracy drop versus inference speed improvement and cost reduction.



**Jordan**: Target outcome by day ninety—you've gone from that thirteen to thirty percent baseline utilization up to sixty to eighty-five percent sustained. For a twenty-GPU cluster, that's about seven hundred eighty thousand dollars in annual savings.



**Alex**: And what can platform teams do this week if they want to get started right now?



**Jordan**: Three things. Deploy DCGM Exporter and identify which pods are using under thirty percent of GPU capacity. Apply node taints to GPU nodes with nvidia dot com slash gpu equals true NoSchedule. And deploy VPA in Off mode for recommendations only. Let it collect data for two weeks minimum before you act on the recommendations.



**Alex**: And for leadership, how do you make the business case?



**Jordan**: The payback calculation. You invest forty-seven thousand five hundred dollars—that's a senior platform engineer for three months plus ten thousand in vendor support from NVIDIA or a consultant. You get sixty-five thousand a month in savings from the example we walked through. You've recovered your investment in twenty-two days. The ask is to approve a ninety-day GPU optimization initiative with dedicated engineering resources.



**Alex**: So the closing insight here is that the four-thousand-three-hundred-fifty-dollar-a-month waste isn't a Kubernetes bug. It's a feature designed for different workloads. But now you know the workarounds.



**Jordan**: MIG for production isolation. Time-slicing for development environments. VPA for right-sizing based on real data instead of guesses. Spot instances for training. Regional arbitrage for everything. The GPUs you already have? They're probably enough. You just need to use them properly. And that starts with understanding that Kubernetes treats GPUs fundamentally differently than CPUs and memory—and adjusting your strategy accordingly.
