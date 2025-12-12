# Episode #053: CDKTF Deprecated - The End of HashiCorp's Programmatic IaC Experiment

## Episode Metadata
- **Episode Number**: 053
- **Title**: CDKTF Deprecated: What Platform Teams Need to Know About IaC Migration
- **Duration Target**: 15-18 minutes
- **Recording Date**: December 11, 2025
- **Publication Date**: December 12, 2025

## News Segment (3-4 minutes)

From today's newsletter selections:

1. **Envoy Proxy Security Updates** (CVE-2025-0913, CVSS 8.6)
   - Versions v1.36.4 and v1.35.8 released
   - Patch immediately - high severity

2. **Google Launches Managed Remote MCP Servers**
   - MCP ecosystem expanding rapidly
   - Google Cloud integration for AI agents

3. **OpenTofu 1.11 Released**
   - Ties directly into CDKTF story
   - Alternative for those leaving Terraform ecosystem

4. **pgAdmin 4 v9.11 Released**
   - PostgreSQL tooling updates

5. **Lima v2.0 for Secure AI Workflows**
   - CNCF project milestone

6. **Amazon ECS Custom Container Stop Signals on Fargate**
   - Graceful shutdown improvements

## Main Topic: CDKTF Deprecation Deep Dive

### Segment 1: The Announcement (2-3 minutes)
**Hook**: Yesterday, HashiCorp (now IBM) archived the CDK for Terraform project, ending a 5-year experiment to bring programmatic infrastructure-as-code to the Terraform ecosystem.

**Key Points**:
- Official sunset: December 10, 2025
- Statement: "CDKTF did not find product-market fit at scale"
- Repository archived, read-only, MPL license allows forks
- Came 10 months after IBM's $6.4B acquisition

### Segment 2: What Was CDKTF? (2-3 minutes)
**Context for listeners who never used it**:

- Launched July 2020 as collaboration between HashiCorp and AWS CDK team
- GA August 2022 (v0.12)
- Supported 5 languages: TypeScript, Python, Java, C#, Go
- Promise: Write infrastructure in real programming languages, synthesize to Terraform

**Adoption Reality**:
- NPM downloads: 243K/week (vs Pulumi's 1.1M - 4-5x gap)
- GitHub stars: 5K (vs Pulumi's 23K)
- Notable user: Mozilla Pocket (open-sourced their implementation)

### Segment 3: Why It Failed (3-4 minutes)
**The Four Factors**:

1. **Pulumi's Head Start**
   - Launched 2018 (2 years earlier)
   - Native language implementation vs JSII translation layer
   - Automation API for programmatic stack management
   - Already had ecosystem when CDKTF entered

2. **HCL "Good Enough"**
   - Most teams found declarative sufficient
   - "Except for using HCL, it handles pretty much whatever you throw at it"
   - Lower cognitive overhead than learning new abstraction

3. **Architectural Complexity**
   - CDKTF → JSII → Terraform JSON → Terraform engine
   - More abstraction layers = harder debugging
   - Pulumi talks directly to cloud APIs

4. **IBM Acquisition Timing**
   - Deprecation 10 months after $6.4B deal closed
   - Portfolio rationalization likely
   - All announcements: "HashiCorp, an IBM Company"

### Segment 4: Community Reaction (2-3 minutes)
**Hacker News Sentiment**:

- "Rather short notice" - same-day announcement and archive
- "Spent last year writing thousands of lines of CDKTF Python, now migrating to Pulumi"
- "Rug pulls on infrastructure components hit your entire infra codebase"
- "It's a great project. Needs to be forked and maintained."

**The Blame Game**:
- "'HashiCorp, an IBM Company' - looks like they want to assign blame"
- Community responsibility: "I blame people who didn't help fund/maintain it"

### Segment 5: Migration Paths (3-4 minutes)
**Option 1: Terraform HCL (HashiCorp's Recommendation)**
- Use `cdktf synth --hcl` to generate readable .tf files
- Stay in ecosystem, lose programmatic abstractions
- Best for: Teams who mainly wanted Terraform with better IDE support

**Option 2: Pulumi (For Programmatic Loyalists)**
- Same multi-language support
- Automation API for GitOps workflows
- Different state management (Pulumi Service)
- Best for: Teams who valued DRY and code abstractions

**Option 3: OpenTofu + Community Fork**
- OpenTofu works with CDKTF via env var
- GitHub issue with 100+ upvotes for native support
- Uncertain future for CDKTF tooling
- Best for: Open-source purists, license concerns

**Option 4: AWS CDK (If AWS-Only)**
- Tighter integration, higher-level abstractions
- Best for: AWS-exclusive infrastructure

### Segment 6: Lessons for Platform Engineers (2-3 minutes)
**Key Takeaways**:

1. **Vendor Lock-in is Real**
   - Infrastructure tooling acquisition risk
   - License changes (BSL), deprecations happen
   - Consider open-source alternatives seriously

2. **Product-Market Fit Matters**
   - Even well-executed tools can fail
   - Adoption metrics are leading indicators
   - Watch NPM downloads, GitHub stars, conference talks

3. **Declarative vs Imperative Debate Continues**
   - HCL's simplicity wins for most use cases
   - Programmatic IaC has niche but loyal audience
   - No one-size-fits-all answer

4. **Migration Planning is Infrastructure**
   - Always have exit strategy
   - Document why you chose a tool
   - Track deprecation signals early

## Closing (1 minute)
- CDKTF's death validates both Pulumi's approach and HCL's staying power
- If you're on CDKTF, start planning migration now - clock is ticking
- Community forks possible under MPL, but uncertain
- The IaC landscape continues to fragment and consolidate simultaneously

## Sources
- GitHub: hashicorp/terraform-cdk (archived)
- HashiCorp Developer: CDK for Terraform documentation
- Hacker News: Terraform CDK has been phased out (ycombinator.com)
- NPM Trends: cdktf vs @pulumi/pulumi
- AWS Blog: Announcing CDK for Terraform on AWS
- HashiCorp Blog: CDK for Terraform Now Generally Available
- OpenTofu GitHub: CDKTF Support Discussion (#1150)
