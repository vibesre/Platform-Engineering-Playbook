---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #008: GCP State of the Union 2025"
slug: 00008-gcp-state-of-the-union-2025
---

# GCP State of the Union 2025 - When Depth Beats Breadth

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 17 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

<PodcastSubscribeButtons />

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, margin: '1.5rem 0'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/v5F9fudm4hQ"
    title="GCP State of the Union 2025 - When Depth Beats Breadth"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>

---

**Jordan**: Today we're diving into GCP—Google Cloud Platform—and here's the stat that's wild. GCP has eleven percent market share. AWS has thirty one percent. So why is GCP growing at thirty two percent year over year while AWS grows at seventeen percent? And why might the number three cloud provider be your number one choice for twenty twenty five?

**Alex**: That's the paradox nobody's talking about. Everyone defaults to AWS because "that's what you do." But when you dig into the numbers, companies are choosing GCP for very specific reasons. And those reasons line up perfectly with the workloads that matter most right now—AI, machine learning, data analytics.

**Jordan**: And the stakes are real. Platform teams are under pressure to cut costs, adopt AI slash ML, handle massive data workloads. Making the wrong cloud choice costs you a hundred thousand dollars plus annually in team time and infrastructure spend.

**Alex**: Right. So today we're uncovering when GCP's specialist strategy beats AWS's generalist approach. And we're backing it with actual performance data and cost comparisons. Not marketing fluff—measured differences.

**Jordan**: Let's start with that growth rate because it's striking. GCP at thirty two percent, AWS at seventeen percent. That's nearly double. What's driving that?

**Alex**: AI and data. Full stop. GCP has been capturing six point four percentage points of market share since Q1 twenty twenty two. And it's accelerating. The global cloud market is growing rapidly. GCP is taking a bigger slice of a rapidly growing pie.

**Jordan**: But Azure is growing even faster—thirty nine percent year over year. They've got the Microsoft slash OpenAI partnership. So GCP isn't alone in this AI-driven growth.

**Alex**: True, but here's the difference. Azure's growth is partly enterprise bundling—if you're already deep in Microsoft, Azure makes sense. GCP's growth is companies choosing it specifically for technical advantages. Data-heavy companies, AI-native startups, teams building on Kubernetes.

**Jordan**: So what makes GCP technically different? Because AWS has what, two hundred plus services? GCP has around a hundred. Most people would look at that and say AWS wins on breadth.

**Alex**: And that's the mental model we need to challenge. Most companies use fewer than twenty services deeply. The rest is just noise. GCP bet on depth over breadth. It's an opinionated platform—Google's engineering culture productized. They're not trying to be everything to everyone.

**Jordan**: Give me a concrete example of where that depth matters.

**Alex**: Network performance. GCP VMs have three times the network throughput of AWS and Azure equivalents. And this isn't marketing—it's been benchmarked by third parties. The bottom-performing GCP machine outperforms the top-performing AWS or Azure machine significantly.

**Jordan**: Wait, three x network performance? That's not a rounding error.

**Alex**: No, it's a fundamental architectural advantage. Google runs the world's largest private network. They built GCP on that backbone. When you spin up a VM in GCP, you're getting Google-scale networking infrastructure. AWS and Azure can't match that because they didn't start with that foundation.

**Jordan**: Okay, so network is one advantage. What about data workloads specifically?

**Alex**: BigQuery. If you're doing serious data analytics, BigQuery is in a different league. It's petabyte-scale, fully serverless, and it actually works the way serverless is supposed to work. Companies report significantly faster queries compared to self-managed data warehouses. And you're not managing clusters, not sizing instances, not dealing with scaling.

**Jordan**: I've heard this pitch before though. "Fully managed, super fast." What's the catch?

**Alex**: Cost can surprise you if you're not careful with query patterns. And there's some lock-in—BigQuery SQL is mostly standard but has Google-specific extensions. But here's the thing: the operational savings usually dwarf the pricing concerns. Teams that move to BigQuery report massive reductions in data engineering overhead.

**Jordan**: And then there's Kubernetes. GCP invented Kubernetes, or rather Google invented it and open-sourced it. How much does that actually matter?

**Alex**: It matters a lot. GKE—Google Kubernetes Engine—isn't just "we support Kubernetes." It's Kubernetes-native architecture. The autopilot mode eliminates the majority of cluster management toil. You're not sizing node pools, not managing upgrades, not dealing with the operational complexity that makes teams hate Kubernetes.

**Jordan**: But Kubernetes is Kubernetes, right? Can't you get a similar experience on AWS with EKS or Azure with AKS?

**Alex**: Theoretically, but in practice it's different. EKS feels bolted on. You're still managing a lot of the undifferentiated heavy lifting. GKE feels like it was designed by people who've been running Kubernetes at scale for a decade—because it was. Plus the integration with BigQuery is seamless. You can spin up a GKE cluster that directly queries BigQuery without jumping through authentication hoops.

**Jordan**: Let's talk about the AI slash ML piece because that's clearly driving a lot of this growth. GCP has Vertex AI with Gemini, with a rapidly growing developer community. How does that stack up against AWS Bedrock or SageMaker?

**Alex**: Unified versus fragmented. AWS has Bedrock for foundation models, SageMaker for custom ML, multiple other services for different ML use cases. Vertex AI is one platform. You get Google's models natively—Gemini, Imagen—plus third-party models like Claude, plus open models like Llama. It's a model garden approach where everything works together.

**Jordan**: And the Transformer architecture that powers most of these models? Google Research invented that. Does that translate to a production advantage?

**Alex**: Yeah, because the people who invented the tech are the ones building the platform. You're not getting a repackaged third-party solution. Google literally wrote the "Attention Is All You Need" paper that created the Transformer. They understand this tech at a fundamental level. When you use Vertex AI, you're benefiting from that deep expertise.

**Jordan**: Okay, but I want to push back on something. AWS has two hundred services. GCP has a hundred. You said most companies only use twenty deeply. But what if you're the company that needs that two hundred and first service? What if GCP just doesn't have what you need?

**Alex**: Then you choose AWS. That's a real constraint. But here's the counterargument: breadth creates choice paralysis and maintenance burden. AWS has five different ways to run a container. Three different managed Kubernetes offerings if you count ECS, EKS, and Fargate. That flexibility is great until you're the platform team trying to standardize and support it all.

**Jordan**: So GCP's constraint forces architectural discipline.

**Alex**: Exactly. It's the Apple approach. Fewer choices, more opinionated, but the choices they give you are really well executed. And for the workloads GCP targets—data, ML, Kubernetes—that depth beats breadth.

**Jordan**: Alright, let's talk economics because this is where the rubber meets the road. GCP can be cheaper than AWS. Is that real or is there a catch?

**Alex**: It's real, but with nuance. GCP can be twenty to forty percent cheaper for specific workloads—especially compute-optimized instances and data-heavy operations. Then you add sustained use discounts—automatic discounts up to thirty percent at the end of the month. No commitment needed, no reserved instances to manage. It just happens.

**Jordan**: Wait, automatic discounts? So I don't have to forecast my usage and commit to a one or three year reserved instance?

**Alex**: Nope. You use the instance, GCP tracks it, at the end of the month you get a discount based on usage. It's the anti-AWS Reserved Instance model. AWS makes you commit upfront. GCP rewards you retroactively.

**Jordan**: That's a huge operational advantage for teams that don't have perfect usage forecasting. Which is most teams. What about preemptible VMs versus AWS Spot instances?

**Alex**: Pretty similar. GCP preemptible VMs are up to ninety percent off. AWS Spot is up to ninety percent off. Both require workloads that tolerate interruption. Not a differentiator.

**Jordan**: Where does GCP's pricing advantage matter most?

**Alex**: Data-heavy workloads. BigQuery versus running your own data warehouse on AWS—the operational cost savings are substantial. ML training on Vertex AI versus building your own pipeline on AWS—teams report significantly faster time to production, which translates to massive cost savings in engineering time.

**Jordan**: But egress costs—the infamous cloud tax—that's similar across all providers, right?

**Alex**: Unfortunately yes. Moving data out of any cloud is expensive. GCP doesn't magically solve that. But here's the multi-cloud pattern we're seeing: process data in GCP using BigQuery, train models in Vertex AI, then move results to AWS for application hosting. You're optimizing where each cloud is strongest.

**Jordan**: That brings up an important point. Most companies aren't choosing GCP or AWS. They're choosing both.

**Alex**: Right. The multi-cloud reality is AWS for breadth, GCP for specialist workloads. You might run your main application stack on AWS because of existing integrations, but your data team is living in BigQuery and your ML engineers are building on Vertex AI.

**Jordan**: So let's talk about what this means for skills and careers. Because if platform engineers need to know multiple clouds, that's a real training investment. Is GCP worth learning if you already know AWS?

**Alex**: The talent pool dynamics are interesting. AWS has the largest talent pool, which means more competition for senior roles. GCP has a smaller community, but that means less competition if you're experienced. Specialist premium is real—GCP plus ML expertise commands higher compensation than generalist cloud knowledge.

**Jordan**: But isn't a smaller community a risk? Fewer resources, harder to find help, harder to hire?

**Alex**: It's double-edged. Yes, it's harder to find GCP-specific talent. But the community quality is high. Less noise, more signal. And here's the thing: if you know AWS, GCP's IAM and networking concepts transfer. You're not starting from zero. Focus on three areas: BigQuery for data, Vertex AI for ML, GKE for Kubernetes. Those are the differentiators.

**Jordan**: What's changing in the market that makes GCP skills more valuable now?

**Alex**: The AI slash ML boom. Every company thinks they need an AI strategy. Most of those strategies involve data pipelines and ML platforms. GCP is where a lot of that innovation is happening. BigQuery is becoming an industry standard like Postgres. Vertex AI experience is highly sought after. If you're a platform engineer who can bridge AWS and GCP, you're more valuable than someone who only knows AWS.

**Jordan**: And Kubernetes is Kubernetes, so GKE experience translates across clouds.

**Alex**: Exactly. K8s is K8s. The concepts are the same. But if you've learned Kubernetes the GCP way with autopilot, you understand what it can be—not just what it is on EKS where you're still managing too much.

**Jordan**: What about certifications? Is Google Cloud Professional Cloud Architect still meaningful?

**Alex**: Yeah, it still carries weight. Especially in data and ML-heavy roles. It signals you understand the platform beyond just "I spun up a VM once." The bar is higher than AWS certifications—Google's exams are known for being tough. But that makes the certification more meaningful.

**Jordan**: Let's get practical. Platform engineer listening to this. They're on AWS today. When should they seriously consider GCP?

**Alex**: Five scenarios. One: data analytics is core to your business. If you're doing serious data work, BigQuery beats everything else. Two: ML slash AI workloads are significant. Vertex AI's unified experience saves months of pipeline building. Three: you're building Kubernetes-native architecture. GKE autopilot eliminates toil. Four: cost optimization pressure. Twenty five to fifty percent savings plus automatic discounts matter when your cloud bill is six figures. Five: your team is Google-aligned. If they're excited about Google tech, don't fight it.

**Jordan**: And when should you stick with AWS?

**Alex**: Five scenarios on the flip side. One: you need services GCP doesn't offer. That breadth gap is real. Two: you're deeply integrated with AWS already. Migration cost can exceed GCP benefits. Three: you have an AWS enterprise agreement with committed spend. That changes the economics. Four: your team expertise is AWS-heavy. Retraining cost is real time and money. Five: regulatory slash compliance requirements. Some certifications favor AWS, especially GovCloud for government workloads.

**Jordan**: What about the pragmatic middle ground? Most companies aren't going to rip and replace their entire AWS infrastructure.

**Alex**: Multi-cloud pattern. GCP for data processing with BigQuery. GCP for ML training with Vertex AI. GCP for Kubernetes workloads with GKE. AWS for application hosting, breadth services, enterprise integrations. You use Terraform for infrastructure as code, Kubernetes for workload portability. You're not locked into one vendor.

**Jordan**: Start small and prove value.

**Alex**: Exactly. Pick one data-heavy or ML workload. Move it to GCP. Measure the results—query performance, operational overhead, cost. Prove the specialist advantage on one use case before you commit to multi-cloud across your organization.

**Jordan**: What does a platform team need to be successful with multi-cloud?

**Alex**: Multi-cloud fluency. You need engineers who can context switch between AWS and GCP. That's not just knowing the services—it's understanding the design philosophy of each platform. AWS is flexible and verbose. GCP is opinionated and streamlined. Those require different thinking.

**Jordan**: And infrastructure as code that works across both.

**Alex**: Terraform is table stakes. You can't manage multi-cloud without unified tooling. Pulumi is another option. But you need something that abstracts away provider specifics while letting you use each cloud's strengths.

**Jordan**: Alright, let's bring this back to our opening stat. GCP growing at thirty two percent, AWS at seventeen percent. Does that growth rate make sense now?

**Alex**: It does. GCP is winning the specialist game in the domains that matter most for twenty twenty five—AI, ML, and data. Companies aren't abandoning AWS. They're adding GCP for specific workloads where Google's technical advantages justify the multi-cloud complexity.

**Jordan**: AWS won the breadth game. GCP is winning the depth game.

**Alex**: And depth matters more when your most important workloads are data-intensive and ML-driven. The question isn't "which cloud?" It's "which workloads go where?"

**Jordan**: Here's my take. The default mindset of "just use AWS" made sense five years ago when the market was less mature. In twenty twenty five, that's lazy thinking. If you're doing serious data work or ML, and you haven't evaluated GCP, you're potentially leaving significant value on the table—performance value, operational value, cost value.

**Alex**: The specialist advantage is real. And as AI slash ML becomes more central to every business, that specialist advantage becomes a strategic differentiator. GCP isn't trying to be AWS. It's trying to be the best platform for specific workloads. And for those workloads, it's succeeding.

**Jordan**: The fundamentals of good platform engineering remain constant. Understand the trade-offs, choose tools that match your workloads, don't let convenience override performance when performance matters. GCP is a tool in your toolkit. Know when to use it.
