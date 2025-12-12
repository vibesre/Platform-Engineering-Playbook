---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #056: CDKTF Deprecated - IaC Migration Guide"
slug: 00056-cdktf-deprecated-iac-migration
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #056: CDKTF Deprecated - The End of HashiCorp's Programmatic IaC Experiment

<GitHubButtons />

**Duration**: 14 minutes | **Speakers**: Jordan & Alex

**Target Audience**: Platform engineers, SREs, and infrastructure teams using CDKTF or evaluating IaC tools

---

## Watch the Episode

<div style={{maxWidth: '640px', margin: '0 auto 1.5rem'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/l9fA8M8bvJ4"
      title="CDKTF Deprecated - The End of HashiCorp's Programmatic IaC Experiment"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

---

## Synopsis

Yesterday, HashiCorp (now an IBM company) officially archived the CDK for Terraform project, ending a five-year experiment in programmatic infrastructure-as-code. This episode breaks down what happened, why CDKTF failed to find product-market fit, and what teams currently using CDKTF should do next. We analyze the four key factors behind the deprecation, community reaction, and the migration paths forward: HCL, Pulumi, OpenTofu, or AWS CDK.

---

## Chapter Markers

- **00:00** - Introduction & News Segment
- **02:00** - The Announcement: CDKTF Archived
- **04:00** - What Was CDKTF? History and Promise
- **06:00** - Why It Failed: Four Key Factors
- **08:30** - Community Reaction
- **10:00** - Migration Paths
- **12:30** - Lessons for Platform Engineers
- **14:00** - Closing

---

## News Segment (December 11, 2025)

- **[Envoy Proxy CVE-2025-0913](https://github.com/envoyproxy/envoy/releases/tag/v1.36.4)**: Critical security update (CVSS 8.6) - v1.36.4 and v1.35.8 released, patch immediately
- **[Google Managed MCP Servers](https://thenewstack.io/google-launches-managed-remote-mcp-servers-for-its-cloud-services/)**: Google Cloud integration for AI agents using Model Context Protocol
- **[OpenTofu 1.11 Released](https://reddit.com/r/Terraform/comments/1pj3akp/opentofu_111_released)**: Open-source Terraform fork continues gaining traction
- **[pgAdmin 4 v9.11](https://www.postgresql.org/about/news/pgadmin-4-v911-released-3192/)**: PostgreSQL tooling improvements
- **[Lima v2.0](https://www.cncf.io/blog/2025/12/11/lima-v2-0-new-features-for-secure-ai-workflows/)**: CNCF project milestone for secure AI workflows
- **[Amazon ECS Custom Stop Signals](https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-ecs-custom-container-stop-signals-fargate/)**: Graceful shutdown improvements on Fargate

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| CDKTF Weekly NPM Downloads | ~243,000 | NPM Trends |
| Pulumi Weekly NPM Downloads | ~1.1 million | NPM Trends |
| Download Gap | 4-5x | NPM Trends comparison |
| CDKTF GitHub Stars | ~5,000 | GitHub |
| Pulumi GitHub Stars | ~24,000 | GitHub |
| CDKTF Launch | July 2020 | HashiCorp Blog |
| CDKTF GA Release | August 2022 (v0.12) | HashiCorp Blog |
| IBM Acquisition | February 2025 | $6.4 billion |
| Deprecation Date | December 10, 2025 | GitHub Archive |

---

## Migration Paths

### Option 1: Terraform HCL (HashiCorp's Recommendation)
```bash
cdktf synth --hcl
```
- Stay in Terraform ecosystem
- Keep existing state files
- Lose programmatic abstractions
- Best for: Teams who mainly wanted better IDE support

### Option 2: Pulumi
- Same multi-language support (TypeScript, Python, Go, etc.)
- Native language implementation (no JSII translation layer)
- Different state management (Pulumi Service)
- Best for: Teams who valued DRY and code abstractions

### Option 3: OpenTofu + Community Fork
```bash
export TERRAFORM_BINARY_NAME=tofu
```
- CDKTF works with OpenTofu today
- 100+ upvotes on GitHub issue for native support
- Uncertain future for tooling
- Best for: Open-source purists, license concerns

### Option 4: AWS CDK (If AWS-Only)
- Tighter integration, higher-level abstractions
- Lose multi-cloud optionality
- Best for: AWS-exclusive infrastructure

---

## Key Takeaways

1. **Vendor lock-in risk is real**: BSL license change (2023), IBM acquisition, CDKTF deprecation - three major disruptions in three years

2. **Adoption metrics are leading indicators**: The 4-5x download gap was visible for years

3. **Declarative vs imperative debate continues**: HCL's simplicity wins for most use cases; programmatic IaC has a loyal but smaller audience

4. **Migration planning is infrastructure**: Always have an exit strategy, document why you chose a tool, track deprecation signals early

---

## Transcript

**Jordan**: Today we're diving into breaking news that's sending ripples through the infrastructure-as-code community. Yesterday, HashiCorp, now an IBM company, officially archived the CDK for Terraform project, ending a five-year experiment to bring programmatic infrastructure-as-code to the Terraform ecosystem.

**Alex**: This is a big deal, Jordan. CDKTF let teams write their infrastructure in TypeScript, Python, Java, C-sharp, and Go instead of HCL. And now it's gone. But before we dig into what happened and what it means for platform teams, let's run through some other important news from this week.

**Jordan**: First up, a critical security update. Envoy Proxy has released versions 1.36.4 and 1.35.8 to address CVE-2025-0913, rated 8.6 on the CVSS scale. If you're running Envoy in production, patch immediately. This is a high-severity vulnerability.

**Alex**: In other news, Google has launched managed remote MCP servers for its cloud services. The Model Context Protocol ecosystem continues to expand rapidly, and Google's integration means AI agents can now interact with Google Cloud resources through a standardized interface. We've covered MCP in recent episodes, and this validates the protocol's momentum.

**Jordan**: Speaking of infrastructure tools, OpenTofu 1.11 was released this week. This ties directly into our main topic because OpenTofu represents one potential path forward for teams leaving the HashiCorp ecosystem. The open-source Terraform fork continues to gain traction.

**Alex**: A few more quick hits. pgAdmin 4 version 9.11 is out with PostgreSQL tooling improvements. Lima version 2.0 brings new features for secure AI workflows, a nice milestone for that CNCF project. And Amazon ECS now supports custom container stop signals on Fargate, improving graceful shutdown handling.

**Jordan**: Now let's get into the main story. Yesterday, December 10th, 2025, HashiCorp archived the terraform-cdk repository on GitHub. The official statement was blunt. Quote: CDKTF did not find product-market fit at scale. HashiCorp, an IBM Company, has chosen to focus its investments on Terraform core and its broader ecosystem. End quote.

**Alex**: That's a remarkably candid admission of failure from a major vendor. And the timing is notable. This deprecation came exactly ten months after IBM completed its 6.4 billion dollar acquisition of HashiCorp in February 2025. Portfolio rationalization seems likely.

**Jordan**: Let's give some context for listeners who never used CDKTF. It launched in July 2020 as a collaboration between HashiCorp and the AWS CDK team. The promise was compelling. Write your infrastructure in real programming languages with loops, conditionals, and abstractions, then synthesize it to Terraform.

**Alex**: The project reached general availability in August 2022 with version 0.12. It supported five languages: TypeScript, Python, Java, C-sharp, and Go. Mozilla Pocket was probably the most prominent public user. They open-sourced their entire CDKTF implementation as a reference architecture.

**Jordan**: But the adoption numbers tell a different story. CDKTF had about 243,000 weekly NPM downloads compared to Pulumi's 1.1 million. That's roughly a four to five times gap. GitHub stars showed similar disparity: 5,000 for CDKTF versus nearly 24,000 for Pulumi.

**Alex**: So why did it fail? I see four main factors. First, Pulumi had a two-year head start. They launched in 2018 and had already built ecosystem momentum before CDKTF even existed. When you're competing for mindshare in a niche market, being second matters.

**Jordan**: Second, and this is important, Pulumi was built natively in each language. CDKTF used JSII, the JavaScript Interop Interface, to translate TypeScript constructs into other languages. That added architectural complexity. When you debug a CDKTF issue, you're navigating multiple abstraction layers.

**Alex**: The third factor is what I call the HCL good enough problem. Most teams found that HCL, despite its quirks, handled their use cases adequately. One Hacker News commenter put it well. Quote: Except for the fact that you have to use HCL, it handles pretty much whatever you throw at it, and it handles it well. End quote.

**Jordan**: And fourth, there's a fundamental philosophical divide. Some practitioners believe that bringing imperative constructs to what's inherently a declarative domain creates more problems than it solves. You can get too clever with inheritance and abstractions when your goal is predictable, auditable infrastructure.

**Alex**: The community reaction has been fascinating to watch. On Hacker News, the predominant sentiment was frustration mixed with resignation. One developer wrote: I've spent the last year writing many thousands of lines of CDKTF Python. I guess I'll spend another year migrating to Pulumi now.

**Jordan**: Another commenter called it a rug pull, noting that infrastructure component deprecations hit your entire codebase at once. When your deployment tooling changes, everything has to change with it.

**Alex**: There's also been discussion about the branding. Every official announcement says HashiCorp, an IBM Company. Some speculate this is intentional distancing, assigning blame to the parent company. Whether that's true or not, the optics aren't great.

**Jordan**: Let's talk about what teams should actually do. HashiCorp recommends two primary migration paths. Option one is migrating to standard Terraform HCL. Starting with CDKTF 0.20, you can run cdktf synth with the --hcl flag to generate readable dot-tf files instead of JSON.

**Alex**: This is probably the path of least resistance for many teams. You stay in the Terraform ecosystem, keep your existing state files, and lose the programmatic abstractions you may not have been using heavily anyway. If you mainly wanted better IDE support and type checking, HCL with modern tooling might be sufficient.

**Jordan**: Option two is migrating to Pulumi. If you valued the programmatic approach, if you actually used those abstractions for DRY infrastructure code, Pulumi is the natural home. Same language support, native implementation, and active development.

**Alex**: The trade-off is that Pulumi has different state management. You'll either use the Pulumi Service or self-host your state backend. And you're rewriting your infrastructure code, not just transpiling it. That's a significant investment.

**Jordan**: There's also option three: OpenTofu with a potential community fork. CDKTF actually works with OpenTofu if you set the TERRAFORM_BINARY_NAME environment variable to tofu. There's a GitHub issue with over 100 upvotes requesting native CDKTF support in OpenTofu.

**Alex**: But I'd be cautious here. Community forks of complex projects have mixed track records. CDKTF isn't just a thin wrapper. It's a substantial codebase that needs ongoing maintenance, provider compatibility updates, and language runtime support. Someone needs to step up and fund that work.

**Jordan**: If your infrastructure is AWS-exclusive and you were already using AWS CDK patterns, migrating to pure AWS CDK might make sense. You lose the multi-cloud optionality, but you gain tighter integration and higher-level abstractions.

**Alex**: Let's zoom out and talk about what platform engineers should take away from this. First, vendor lock-in risk is real and often underestimated. HashiCorp's license change to BSL in 2023, the IBM acquisition, and now this deprecation. That's three major disruptions in three years.

**Jordan**: Second, adoption metrics are leading indicators. The four-to-five-times download gap between CDKTF and Pulumi was visible for years. If your tool of choice has anemic adoption, that's a risk factor worth considering.

**Alex**: Third, the declarative versus imperative debate continues without a clear winner. HCL's simplicity wins for most use cases. Programmatic IaC has a loyal but smaller audience. There's no one-size-fits-all answer, and that's okay.

**Jordan**: And fourth, migration planning is itself infrastructure. Always have an exit strategy. Document why you chose a tool, what alternatives you considered, and what would trigger a re-evaluation. Track deprecation signals early.

**Alex**: One thing I've been thinking about. CDKTF's death actually validates both camps. It validates Pulumi's approach because the demand for programmatic IaC clearly exists, just not at HashiCorp. And it validates HCL's staying power because most teams apparently didn't need the programmatic features.

**Jordan**: That's a great observation. The middle path was the weakest position. Pure declarative with HCL works. Pure programmatic with Pulumi works. The hybrid approach of programmatic-to-declarative transpilation satisfied neither camp fully.

**Alex**: For teams currently on CDKTF, here's the practical advice. Don't panic, but do start planning. Your existing deployments will continue to work. The code isn't going to stop running overnight. But the clock is now ticking on compatibility.

**Jordan**: Use this as an opportunity to audit your infrastructure patterns. Were you actually using the programmatic features? If you have minimal abstraction, minimal loops, minimal inheritance, HCL migration is straightforward. If you built sophisticated reusable constructs, Pulumi deserves serious evaluation.

**Alex**: And watch the OpenTofu space. If a community fork emerges with credible maintainers and funding, that could be a viable path. But don't bet your infrastructure on vaporware. Wait until there's a working, maintained project before committing.

**Jordan**: The broader lesson here is about the evolution of infrastructure tooling. We're still early in figuring out the right abstractions. Terraform's success proved that declarative IaC works. But the explosion of alternatives, Pulumi, CDK, Crossplane, shows that one paradigm doesn't fit all problems.

**Alex**: And acquisitions will continue to reshape the landscape. HashiCorp under IBM is a different company than HashiCorp the independent startup. Strategic priorities shift. Products get rationalized. That's not a criticism, it's just the reality of enterprise software.

**Jordan**: Platform engineers need to think like portfolio managers. Diversify your dependencies where practical. Maintain expertise in multiple tools. And always, always have a migration playbook ready.

**Alex**: For our listeners currently evaluating IaC tools, this is a good reminder to consider ecosystem stability alongside feature comparisons. A slightly less feature-rich tool with strong community momentum and independent governance might be the safer long-term bet.

**Jordan**: If you're on CDKTF today, start your migration analysis this week. Run cdktf synth --hcl on a representative project and see what the output looks like. Spin up a proof-of-concept in Pulumi. Give yourself options before you need them urgently.

**Alex**: The infrastructure-as-code landscape will keep evolving. CDKTF won't be the last tool to get deprecated, and it won't be the last acquisition to reshape priorities. Building resilience into your platform strategy means expecting and planning for these disruptions.

**Jordan**: That's a wrap on the CDKTF deprecation. The programmatic IaC dream isn't dead, it just won't be at HashiCorp. For current users, migration paths exist. For everyone else, it's a valuable case study in tool selection and ecosystem dynamics.

**Alex**: As always, we'll keep tracking the fallout and any community fork developments. Until next time, keep your infrastructure declarative, your migrations planned, and your dependencies diversified.
