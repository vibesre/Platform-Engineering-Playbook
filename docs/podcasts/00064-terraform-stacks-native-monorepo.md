---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #064: Terraform Stacks + Native Monorepo"
slug: 00064-terraform-stacks-native-monorepo
---

# Episode #064: Terraform Stacks + Native Monorepo Support

<GitHubButtons/>

**Duration**: 17 minutes | **Speakers**: Jordan & Alex | **Target Audience**: Platform engineers, DevOps engineers, SREs

<iframe width="100%" style={{aspectRatio: '16/9'}} src="https://www.youtube.com/embed/yo2cAhnHNJc" title="Terraform Stacks + Native Monorepo Support" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

> 📰 **News Segment**: This episode covers 5 platform engineering news items before the main topic.

## Episode Summary

HashiCorp just released native monorepo support and Terraform Stacks to GA (September 2025). This episode breaks down the component-based architecture that replaces copy-paste configurations, how deployments provide isolated state management, and orchestration rules for automated approvals. Plus news on Pulumi's Terraform support, vLLM 0.13.0, EC2 AZ ID API support, and GPT-5.2-Codex.

## News Segment

1. **Terraform Stacks + Monorepo** - HashiCorp's native monorepo support and component-based architecture (GA September 2025)
2. **Pulumi IaC Including Terraform/HCL** - Direct Terraform state file support, native HCL as first-class language, credits for HashiCorp costs (Private Beta, GA Q1 2026)
3. **vLLM v0.13.0** - 442 commits from 207 contributors, NVIDIA Blackwell Ultra support, DeepSeek optimizations (5.3% throughput gains, 4.4% TTFT improvement)
4. **Amazon EC2 AZ ID API Support** - Consistent Availability Zone IDs across all AWS accounts, eliminates manual zone mapping for multi-account strategies
5. **GPT-5.2-Codex** - OpenAI's agentic coding model (56.4% on SWE-Bench Pro, 64% on Terminal-Bench 2.0), invite-only cybersecurity capabilities, released December 18, 2025

## Key Takeaways

- **Components** are defined in `.tfstack.hcl` files - groups of resources sharing a lifecycle (e.g., VPC, subnets, routing tables)
- **Deployments** are isolated instances with separate state files (e.g., us-east-1, eu-west-1, ap-southeast-1 from same component)
- **Orchestration Rules** enable automated approval with context-aware conditions (e.g., auto-approve if no deletions)
- **Linked Stacks** handle cross-stack dependencies declaratively using `upstream_input` and `publish_output` blocks
- Migration tool (workspace-to-stacks) still in beta - start with greenfield projects or non-critical workspaces
- Advanced orchestration rules require HCP Terraform Plus Edition
- Stacks count toward HCP Terraform resource limits (as of September 25, 2025)

## Resources

- [Terraform Stacks + Monorepo Announcement](https://www.hashicorp.com/blog/terraform-adds-native-monorepo-support-stack-component-configurations-and-more) - HashiCorp's official announcement of GA release
- [Terraform Stacks Explained](https://www.hashicorp.com/blog/terraform-stacks-explained) - Deep dive on components, deployments, orchestration
- [Pulumi IaC Including Terraform](https://www.pulumi.com/blog/all-iac-including-terraform-and-hcl/) - Pulumi's Terraform/HCL support announcement
- [vLLM v0.13.0 Release Notes](https://github.com/vllm-project/vllm/releases/tag/v0.13.0) - Performance improvements and new features
- [GPT-5.2-Codex Announcement](https://openai.com/index/gpt-5-2-codex/) - OpenAI's agentic coding model

## Transcript

**Jordan**: Welcome back to the Platform Engineering Podcast. This week has been absolutely packed with infrastructure news. We've got HashiCorp's massive Terraform Stacks release, Pulumi making some bold moves, major updates to vLLM, and OpenAI's latest coding model. Let's jump right in.

**Alex**: Yeah, and I think the theme this week is consolidation. Everyone's trying to simplify the multi-environment, multi-cloud complexity that's been plaguing platform teams. Let's start with the news segment before we dive deep into Terraform Stacks.

**Jordan**: First up, the big one we'll explore in detail later: HashiCorp just released native monorepo support and Terraform Stacks to general availability. This is their answer to the copy-paste configuration hell that teams have been dealing with for years. We're going to break down exactly what this means in a few minutes.

**Alex**: Second, Pulumi made three major announcements this week, and the timing is interesting given HashiCorp's IBM acquisition aftermath. They're now supporting Terraform and OpenTofu directly in Pulumi Cloud, adding native HCL support as a first-class language alongside Python and TypeScript, and they're offering to credit your existing HashiCorp costs. That's a direct play for frustrated Terraform users.

**Jordan**: The hybrid strategy angle is fascinating. You can now run Terraform state files through Pulumi Cloud's platform, getting their AI agent Neo and governance features without migrating code. It goes GA in Q1 2026, currently in private beta. For platform teams stuck between tools, this actually opens up some interesting architectural options.

**Alex**: Third, vLLM version 0.13.0 dropped with some serious performance improvements. Four hundred forty-two commits from two hundred seven contributors. The highlights for platform engineers: NVIDIA Blackwell Ultra support, DeepSeek optimizations delivering five point three percent throughput gains and four point four percent time-to-first-token improvement, and enhanced multi-node deployment capabilities.

**Jordan**: The W4A8 grouped GEMM on Hopper is particularly relevant if you're running inference workloads at scale. The quantization improvements mean better cost efficiency. If you're managing AI infrastructure, this release has real operational impact.

**Alex**: Fourth, Amazon EC2 now accepts Availability Zone IDs across all APIs. This seems minor until you understand the problem it solves. AZ names like us-east-1a can map to different physical locations depending on your AWS account. AZ IDs are consistent across all accounts.

**Jordan**: This is huge for multi-account strategies. Previously, you'd have to manually map zones to ensure resources stayed co-located. Now you can use AZ IDs directly when creating instances, volumes, and subnets. Eliminates an entire class of deployment errors.

**Alex**: And fifth, OpenAI released GPT-5.2-Codex on December eighteenth. They're calling it their most advanced agentic coding model yet. It scored fifty-six point four percent on SWE-Bench Pro, which is the best score to date, and sixty-four percent on Terminal-Bench 2.0.

**Jordan**: The cybersecurity capabilities are notable. Strong enough that OpenAI is doing invite-only access for more permissive models, limiting it to vetted defensive security professionals. It's available now for paid ChatGPT users, with API access coming in the next few weeks. This was reportedly an internal code red response to Google's Gemini 3 launch.

**Alex**: Alright, let's transition to the main topic. HashiCorp just dropped what I'd argue is their biggest Terraform feature since modules themselves. Native monorepo support combined with Terraform Stacks reaching general availability. Jordan, you've been digging into this. What's the core architectural shift here?

**Jordan**: They're replacing Terraform's traditional root module structure with a component-based architecture. Instead of having separate directories for dev, staging, and prod, where you copy-paste configurations and hope they stay in sync, you define components once and deploy them multiple times. It's built on top of your existing Terraform modules, but it adds this lifecycle-aware orchestration layer.

**Alex**: Okay, so break down the three core concepts for me. Components, deployments, and orchestration rules. Let's start with components.

**Jordan**: Components are defined in files ending in dot tfstack dot hcl. Think of them as groups of related resources that share a lifecycle. Your VPC, subnets, and routing tables might be one component. Your application backend might be another. Each component block includes a Terraform module as its source, and you configure it using the inputs argument. It's similar to calling a module, but with this explicit lifecycle grouping.

**Alex**: And that's different from just using modules because?

**Jordan**: Modules are reusable code. Components are deployment units. A module is like a function definition. A component is like deciding which functions get called together and in what order. HashiCorp recommends structuring stacks along technical boundaries. Shared services like networking infrastructure in one stack, application components that consume those shared services in another.

**Alex**: Got it. So deployments are the instances of those components?

**Jordan**: Exactly. Each deployment is a separate instance of your component configuration with isolated state files. So you might have a networking component, and then three deployments: us-east-1, eu-west-1, and ap-southeast-1. Same configuration, different regions, separate state. No code duplication.

**Alex**: That's addressing one of the biggest pain points. I've seen teams with eight different directories, one per environment, and when someone updates the dev config, there's this manual process of propagating changes. This automates that?

**Jordan**: Yes, but with control. You define which deployments get updated. When you make a change to the stack configuration, you can roll it out to all deployments, some of them, or none. That's where orchestration rules come in.

**Alex**: Alright, orchestration rules. This is the automated approval piece?

**Jordan**: Right. An orchestration rule specifies conditions for when a plan operation should be automatically approved. You get access to a context variable with results from the plan phase. So you can write conditions like, context dot plan dot changes dot change equals zero, meaning no modifications. Or context dot plan dot changes dot remove equals zero, no deletions. There's a default rule called empty underscore plan that automatically approves if there are no changes.

**Alex**: So I could write a rule that says, auto-approve production deployment if there are no resource deletions?

**Jordan**: Exactly. Or auto-approve if it's only adding resources. Or if it's a specific deployment group. The deployment groups feature lets you enforce rules across multiple deployments. You manually assign deployments to groups, or HCP Terraform auto-creates a default group. Custom rules require the Plus Edition, though.

**Alex**: There's the catch. What else is gated behind the Plus tier?

**Jordan**: The advanced deployment group orchestration rules are Plus Edition. The basic stack functionality is available in the free tier, but it counts toward your HCP Terraform resource usage limits as of September twenty-fifth, 2025, when it went GA.

**Alex**: Okay, let's talk about the native monorepo support specifically. What changed in the file structure and workflow?

**Jordan**: Traditional Terraform, you'd have something like this: a repo with directories for dev, staging, prod, each containing duplicate terraform files. Dependencies between configurations? You're manually passing outputs as data sources or using remote state. It's fragile. With the new approach, you have component configuration files, deployment configuration files, and linked stacks.

**Alex**: Walk me through a practical example.

**Jordan**: Sure. Let's say you have networking infrastructure and an application. You'd create a networking stack directory with components dot tfstack dot hcl defining your VPC component, and deployments dot tfdeploy dot hcl creating instances for us-east-1 and eu-west-1. Then your application stack directory would have its own components and deployments files. The key is the linked stacks feature. You declare an upstream underscore input block in your application deployment config to read values from the networking stack's publish underscore output block.

**Alex**: So the dependency is explicit and automated?

**Jordan**: Completely. Adding an upstream input block creates a dependency on the upstream stack. Terraform knows the order of operations. You're not manually tracking which stack needs to run first, or hoping your remote state references are correct. It's declarative.

**Alex**: What about teams currently using Terragrunt or other solutions? What's the migration path?

**Jordan**: HashiCorp released a workspace-to-stacks migration tool, though it's still in beta as of December 2025. It's CLI-driven and automates the key steps. Extract configuration from existing workspaces, generate valid stack config that reflects the workspace settings, transfer Terraform state to the new stack deployment, create and initialize the new stack. I'd recommend testing it with non-critical workspaces first.

**Alex**: How mature is this? Should teams be migrating production workloads right now?

**Jordan**: Stacks went GA in September 2025, so it's still relatively new. The migration tool being in beta is a signal. I'd say if you're managing three or more environments, especially multi-region, this is worth serious evaluation. Start with a greenfield project or a less critical service. Get familiar with component design patterns. But migrating your entire production infrastructure overnight? That's probably not the move.

**Alex**: Fair. Let's talk about the competitive landscape. How do Terraform Stacks compare to Terragrunt, Pulumi Stacks, and other solutions?

**Jordan**: Terragrunt has been the go-to third-party wrapper for DRY Terraform configurations. It uses HCL to define hierarchy and dependencies. It's mature and battle-tested. The advantage of Terraform Stacks is that it's native, first-class support from HashiCorp. No external wrapper needed. You get better integration with HCP Terraform's features.

**Alex**: And Pulumi Stacks are a different beast entirely, right?

**Jordan**: Similar concept, different implementation philosophy. Pulumi lets you use actual programming languages like TypeScript, Python, Go. Their stack model is about organizing resources with isolated state. The big news today is that Pulumi now supports importing Terraform and HCL directly. So you could theoretically run a hybrid strategy: some infrastructure in Pulumi Stacks using TypeScript, some using Terraform Stacks with HCL, managing both through Pulumi Cloud.

**Alex**: That's actually an interesting hedge. If you're not sure which direction to go, you can experiment with both.

**Jordan**: Exactly. And then there's AWS CDK and CDKTF, the Cloud Development Kit for Terraform. That's also a programming language approach, but synthesizing to CloudFormation or Terraform. Different abstraction level. Stacks compete on simplicity and staying within the pure Terraform ecosystem.

**Alex**: So if you're heavily invested in Terraform modules, Stacks is the path of least resistance?

**Jordan**: Yes, with the caveat that there's a learning curve around component design and orchestration rules. You're adopting a new way of thinking about infrastructure organization. It's not just lift and shift. You need to decide how to carve up your infrastructure into components, how to structure dependencies between stacks, and how to write safe orchestration rules.

**Alex**: What about teams using Terragrunt right now? Is there a compelling reason to migrate?

**Jordan**: If Terragrunt is working for you, there's no immediate urgency. But long-term, I'd bet on the native solution. HashiCorp will iterate faster on Stacks than the community can keep Terragrunt updated. And as more teams adopt Stacks, you'll see better tooling, more examples, and clearer best practices. The network effects matter.

**Alex**: Let's wrap with practical advice. If I'm a platform engineer listening to this, managing Terraform across multiple environments, what should I do this week?

**Jordan**: Three things. First, read the HashiCorp Stacks documentation. Understand the mental model of components, deployments, and orchestration. Second, experiment in a dev environment. Create a simple stack with two components and three deployments. Get the feel for how linked stacks work. Third, evaluate this against your current tooling. Are you using Terragrunt, custom scripts, copy-paste configurations? Map out what the migration would look like.

**Alex**: And if you're starting a new project?

**Jordan**: Stacks should be on your shortlist. Compare it to Pulumi, especially now that Pulumi supports HCL. The decision comes down to whether you want pure Terraform with native tooling, or multi-language flexibility with a different platform. Both are valid. But don't default to the old directory-per-environment pattern. That's the past.

**Jordan**: The key insight here is that HashiCorp is catching up to what modern infrastructure as code needs to look like. Component-based thinking instead of directory-based. Orchestration rules that give you deployment confidence. This isn't revolutionary, but it's a significant evolution of how Terraform works at scale.

**Alex**: And the timing matters. With IBM's acquisition and the community skepticism around HashiCorp's direction, this is a statement release. They're saying, we're still investing in Terraform's core capabilities. Whether that rebuilds trust is a different question, but technically, this is solid work.

**Jordan**: Agreed. My practical takeaway: the monorepo support and stacks model is the direction the industry is moving. Whether you adopt Terraform Stacks specifically, or Pulumi, or something else, you need to move away from configuration duplication and manual dependency management. That's the real lesson.

**Alex**: Start small. One stack, two deployments. Test the migration tool with a non-critical workspace. Don't try to boil the ocean. Get comfortable with the component design patterns, understand how orchestration rules work in practice, and then gradually expand your usage.

**Jordan**: And leverage linked stacks for shared infrastructure. That's where the real power is. Your networking team publishes outputs, your application teams consume them. Clear boundaries, explicit dependencies, automated orchestration. That's how platform engineering should work.

**Alex**: Alright, that's our deep dive on Terraform Stacks and native monorepo support. This is a big shift in how HashiCorp expects teams to use Terraform. Whether you adopt it immediately or wait for more maturity, it's worth understanding the architecture. The fundamentals of component-based infrastructure and declarative orchestration are here to stay.
