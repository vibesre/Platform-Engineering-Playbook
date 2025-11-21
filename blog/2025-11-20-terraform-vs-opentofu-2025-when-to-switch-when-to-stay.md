---
title: "Terraform vs OpenTofu 2025: When to Switch, When to Stay (Complete Comparison + Migration Decision Tree)"
slug: 2025-11-20-terraform-vs-opentofu-2025-when-to-switch-when-to-stay
description: "Terraform vs OpenTofu comparison 2025: licensing, features, migration guide. Includes Fidelity's 50K state file case study and decision framework for when to switch."
keywords:
  - terraform vs opentofu 2025
  - should i switch to opentofu
  - terraform opentofu comparison
  - opentofu migration guide
  - terraform bsl license
  - opentofu state encryption
  - fidelity terraform opentofu
  - terraform state file migration
  - hashicorp ibm acquisition
  - opentofu vs terraform
  - terraform to opentofu migration
  - opentofu compatibility
datePublished: "2025-11-20"
dateModified: "2025-11-20"
schema:
  type: FAQPage
  questions:
    - question: "What is the main difference between Terraform and OpenTofu?"
      answer: "The primary difference is licensing: OpenTofu uses the open-source MPL 2.0 license maintained by the Linux Foundation, while Terraform uses the restrictive Business Source License (BSL) controlled by HashiCorp (now owned by IBM as of 2024). Both tools share the same codebase through Terraform 1.5.x, with OpenTofu forking after the August 2023 license change."
    - question: "Is OpenTofu compatible with Terraform state files?"
      answer: "Yes, OpenTofu uses the identical state file format as Terraform, meaning no conversion is needed during migration. OpenTofu 1.6.2 is fully compatible with Terraform 1.5.x and earlier versions, allowing seamless drop-in replacement without state file modifications."
    - question: "How many companies have adopted OpenTofu?"
      answer: "As of June 2025, OpenTofu has surpassed 10 million downloads from GitHub releases alone (actual total likely exceeds 20 million including package managers), with registry traffic increasing 300% year-over-year to 6 million requests per day. Notable enterprise adopters include Fidelity Investments, which migrated 50,000 state files managing 4 million cloud resources."
    - question: "Does OpenTofu support state file encryption?"
      answer: "Yes, OpenTofu version 1.7 and later includes native client-side state and plan file encryption, supporting both local storage and remote backends. This feature uses PBKDF2, AWS KMS, or GCP KMS for key management. Terraform does not support state encryption despite it being the most-requested feature for over 5 years."
    - question: "Can I migrate from Terraform to OpenTofu without downtime?"
      answer: "Yes, zero-downtime migration is possible because OpenTofu is a drop-in replacement for Terraform 1.5.x and earlier. The process involves installing OpenTofu, running tofu init -upgrade, verifying with tofu plan, and updating state with tofu apply. Fidelity achieved this pattern across 50,000 state files."
    - question: "What happens if I need to migrate back from OpenTofu to Terraform?"
      answer: "Migrating back to Terraform is possible for standard configurations without OpenTofu-specific features like state encryption. However, provider version incompatibilities may occur when reversing migration. The migration is reversible as long as you don't use OpenTofu 1.7+ exclusive features."
    - question: "Are Terraform providers and modules compatible with OpenTofu?"
      answer: "Yes, OpenTofu maintains full compatibility with the Terraform provider and module ecosystem. OpenTofu's registry hosts 3,900+ providers and 23,600+ modules using the same HashiCorp Configuration Language (HCL). Organizations can use providers from either registry."
    - question: "Why did HashiCorp change Terraform's license?"
      answer: "On August 10, 2023, HashiCorp changed Terraform's license from the open-source MPL 2.0 to the Business Source License (BSL) 1.1, restricting commercial competitive use. The community responded by creating OpenTofu, which was accepted by the Linux Foundation in September 2023 and reached CNCF Sandbox status in April 2025."
    - question: "What version of OpenTofu should I use for migrating from Terraform?"
      answer: "For Terraform 1.5.x or earlier, migrate to OpenTofu 1.6.2 first (fully compatible), then upgrade to the latest OpenTofu version. The migration path is: Terraform 1.5.x → OpenTofu 1.6.2 → OpenTofu 1.10+ (latest)."
    - question: "Does IBM's acquisition of HashiCorp affect the Terraform vs OpenTofu decision?"
      answer: "IBM acquired HashiCorp for $6.4 billion in April 2024. While this brings enterprise stability to Terraform, it reinforces vendor lock-in concerns. IBM has not indicated plans to revert Terraform to open-source licensing, making OpenTofu the only truly open-source option."
---

In August 2023, HashiCorp's license change sent shockwaves through the infrastructure-as-code community: Terraform, the de facto standard managing billions of cloud resources worldwide, switched from open-source MPL 2.0 to the restrictive Business Source License. Within months, the community responded with OpenTofu—a fork maintained by the Linux Foundation that's now surpassed 10 million downloads. By April 2024, IBM acquired HashiCorp for $6.4 billion, and Fidelity Investments migrated 50,000 state files to OpenTofu. The question facing every platform engineering team in 2025: switch or stay?

> 🎙️ **Listen to the podcast episode**: [Terraform vs OpenTofu Debate](/podcasts/00032-terraform-opentofu-debate) - Jordan and Alex discuss the licensing controversy, migration strategies, and what the IBM acquisition means for IaC's future.

## TL;DR: The Terraform vs OpenTofu Decision in 2025

HashiCorp changed Terraform's license from open-source to BSL in August 2023, creating vendor lock-in concerns and restricting commercial competitive use. OpenTofu emerged as a fully open-source fork (MPL 2.0) maintained by the Linux Foundation and accepted to CNCF Sandbox in April 2025.

**Key Statistics**:
- **OpenTofu**: 10M+ downloads (June 2025), 300% registry traffic growth, 3,900+ providers
- **Fidelity**: Migrated 50,000 state files, 4M resources, 70% of 2,000 apps in 2 quarters
- **Terraform**: Acquired by IBM for $6.4B (April 2024), BSL license remains
- **Compatibility**: OpenTofu 1.6.2 is drop-in replacement for Terraform 1.5.x and earlier
- **State Encryption**: OpenTofu 1.7+ includes native encryption (Terraform doesn't after 5+ years of requests)
- **Zero-Downtime**: Migration possible with identical state file format, no conversion needed

**When to Switch to OpenTofu**:
- Concerned about vendor lock-in or BSL license restrictions
- Need state file encryption for compliance
- Building infrastructure tooling requiring open-source
- Want community-driven governance (Linux Foundation/CNCF)

**When to Stay with Terraform**:
- Deeply embedded in Terraform Cloud/Enterprise with custom workflows
- Existing HashiCorp/IBM contracts with formal SLAs
- Organization requires vendor-backed commercial support
- Using Terraform 1.6+ features without OpenTofu equivalents

## Key Statistics at a Glance

| Metric | Value | Source | Context |
|--------|-------|--------|---------|
| OpenTofu Downloads | 10M+ (GitHub), 20M+ total | [OpenTofu 1.10.0 Release](https://opentofu.org/blog/opentofu-1-10-0/) | Approaching milestone as of June 2025, excludes Homebrew/package managers |
| Registry Traffic Growth | 300% YoY, 6M requests/day | [Spacelift Analysis](https://spacelift.io/blog/opentofu-1-10-major-updates-for-modern-iac) | Tool vendors report sharply increased usage |
| OpenTofu Ecosystem | 3,900+ providers, 23,600+ modules | [OpenTofu 1.10.0 Release](https://opentofu.org/blog/opentofu-1-10-0/) | Full compatibility with Terraform ecosystem |
| Fidelity Migration Scale | 50,000 state files, 4M resources | [Fidelity Migration Story](https://www.futuriom.com/articles/news/fidelity-ditches-terraform-for-opentofu/2025/04) | 2,000 apps, 70% migrated in 2 quarters |
| IBM Acquisition | $6.4B ($35/share) | [IBM Newsroom](https://newsroom.ibm.com/2024-04-24-IBM-to-Acquire-HashiCorp-Inc) | Announced April 24, 2024; closed late 2024 |
| License Change Date | August 10, 2023 | [Spacelift License Analysis](https://spacelift.io/blog/terraform-license-change) | Terraform switched from MPL 2.0 to BSL 1.1 |
| Last Open Source Version | Terraform 1.5.7 (MPL 2.0) | [Terragrunt Compatibility](https://terragrunt.gruntwork.io/docs/reference/supported-versions/) | Final version before BSL |
| OpenTofu Contributor Growth | 160+ contributors (3x since Jan 2024) | [OpenTofu 1.10.0 Release](https://opentofu.org/blog/opentofu-1-10-0/) | Community-driven development |
| CNCF Acceptance | Sandbox status, April 23, 2025 | [CNCF Projects](https://www.cncf.io/projects/opentofu/) | Special MPL 2.0 license exception granted |
| State Encryption | OpenTofu 1.7+: Yes, Terraform: No | [OpenTofu State Encryption Docs](https://opentofu.org/docs/language/state/encryption/) | Most-requested Terraform feature (5+ years), unfulfilled |
| Version Compatibility | OpenTofu 1.6.2 = Terraform ≤1.5.x | [OpenTofu Migration Guide](https://opentofu.org/docs/intro/migration/) | Drop-in replacement, identical state format |
| Migration Success Rate | 70% in 2 quarters (Fidelity) | [Fidelity Case Study](https://opentofu.org/blog/fidelity-investment-migration/) | Zero-downtime pattern validated |

## The Licensing Earthquake That Split the IaC World

On August 10, 2023, HashiCorp switched Terraform from the open-source Mozilla Public License 2.0 to the Business Source License 1.1. The change wasn't subtle: BSL prohibits using Terraform code to build competing commercial products or services. For teams using Terraform in-house to manage infrastructure, the license change had minimal immediate impact. But for tool vendors, consultancies, and SaaS platforms, it created legal ambiguity and vendor lock-in concerns.

The community's response was swift. Within weeks, the OpenTF Manifesto emerged with over 400 companies signing on to fork Terraform under its original open-source license. By September 2023, the Linux Foundation announced OpenTofu, and by January 2024, OpenTofu 1.0 reached stable release. Fast-forward to April 2025: OpenTofu achieved CNCF Sandbox status with a special MPL 2.0 license exception—a validation of its governance model and technical credibility.

Then came IBM. In April 2024, IBM announced the acquisition of HashiCorp for $6.4 billion at $35 per share, closing the deal by year's end. The strategic rationale made sense: integrate Terraform with Red Hat Ansible, build out IBM's hybrid cloud platform, monetize enterprise IaC. But the acquisition reinforced the core concern driving OpenTofu adoption: single-vendor control over critical infrastructure tooling.

Fidelity Investments provides the clearest signal of enterprise reaction. David Jackson, VP of Automation Tooling at Fidelity, explained: "The licensing changes prompted a broader conversation internally. OpenTofu's commitment to open governance aligned with our values and platform engineering strategy." Fidelity began migrating 2,000 applications managing 50,000 state files and 4 million cloud resources. By the end of two quarters, 70% of their projects had moved to OpenTofu.

The licensing earthquake didn't just create a technical fork—it forced platform engineering teams to confront a fundamental question: Do we bet on vendor-controlled tooling with commercial support, or do we prioritize open-source governance and community-driven development? The answer isn't universal, but the question is now unavoidable.

## Terraform vs OpenTofu: Feature-by-Feature Reality Check

### Licensing & Governance: The Fundamental Divide

**Terraform** operates under the Business Source License 1.1, restricting competitive commercial use. HashiCorp's [license FAQ](https://www.hashicorp.com/en/license-faq) clarifies that using Terraform to manage infrastructure in-house is fine, but building competing services or embedding Terraform in commercial products triggers restrictions. Governance sits with HashiCorp, now a subsidiary of IBM following the 2024 acquisition.

**OpenTofu** uses the Mozilla Public License 2.0—true open source with no restrictions on commercial use. Governance lives with the Linux Foundation, and OpenTofu achieved CNCF Sandbox status in April 2025. This means 160+ contributors can influence the roadmap through transparent community processes, not vendor priorities.

For 70% of teams using Terraform purely in-house, the licensing difference may feel academic. But for tool vendors like Spacelift, ControlMonkey, and env0—all reporting 300% growth in OpenTofu usage—the difference is existential. If you're building infrastructure tooling, SaaS platforms, or consulting services, the BSL restrictions create ambiguity. OpenTofu eliminates this risk entirely.

> **💡 Key Takeaway #1**
>
> Licensing is not just legal fine print: BSL restrictions affect tool vendors, consultancies, and any organization building infrastructure services. OpenTofu's MPL 2.0 license provides commercial freedom without competitive-use restrictions, validated by Linux Foundation and CNCF governance. For 70% of teams using Terraform purely in-house, licensing may not matter immediately, but vendor lock-in risk increases with IBM's ownership.

### State Encryption: The Feature Terraform Never Built

The Terraform community has requested native state file encryption since 2016. For over five years, the most-upvoted issue on HashiCorp's GitHub remained open: "Add support for encrypting state files." HashiCorp's answer: use S3 server-side encryption, AWS KMS, or third-party backends. The community's frustration: "Why should encryption-at-rest require backend-specific workarounds?"

OpenTofu delivered in version 1.7 (released 2024): native client-side encryption for state and plan files. The implementation supports PBKDF2, AWS KMS, and GCP KMS for key management. It works with both local storage and remote backends—no backend-specific configuration needed.

Here's what OpenTofu's encryption looks like in practice:

```hcl
encryption {
  key_provider "pbkdf2" "mykey" {
    passphrase = var.passphrase
  }

  state {
    enforced = true
    method "aes_gcm" "state_encryption" {
      keys = key_provider.pbkdf2.mykey
    }
  }
}
```

Terraform's response in version 1.10 introduced "ephemeral resources"—values that aren't saved to state at all. This solves secrets leakage for specific resources but doesn't address the broader requirement: encrypting the entire state file for compliance.

For organizations in finance, healthcare, or government, this difference is non-negotiable. Encryption-at-rest requirements can't be met with backend workarounds alone—they need client-side encryption before the state file leaves the execution environment. OpenTofu provides this. Terraform does not. Security and compliance considerations like state encryption are fundamental to infrastructure decisions—explore more in our [Kubernetes IaC & GitOps](/podcasts/00020-kubernetes-iac-gitops) episode.

As [The New Stack reported](https://thenewstack.io/opentofu-gains-state-encryption-so-whats-next/): "When OpenTofu was first announced, a common refrain from the community was, 'If you deliver state encryption, we'll migrate.' Lo and behold, the much-awaited feature shipped in v1.7."

> **💡 Key Takeaway #2**
>
> State file encryption is OpenTofu's killer feature for compliance-driven organizations. After 5+ years of Terraform community requests going unfulfilled, OpenTofu 1.7 delivered native client-side encryption with KMS integration in 2024. Organizations in finance, healthcare, or government requiring encryption-at-rest can now meet requirements without backend workarounds. This feature alone justifies migration for security-conscious teams managing sensitive infrastructure.

### Compatibility & Ecosystem: The Drop-In Replacement Test

The fear driving hesitation around OpenTofu migration is simple: "Will my existing Terraform code work?" The answer depends on your Terraform version.

**Version Compatibility Matrix**:

| Terraform Version | OpenTofu Version | Compatibility |
|-------------------|------------------|---------------|
| ≤1.5.x (MPL 2.0) | 1.6.2 | Drop-in replacement |
| 1.6.x | 1.7+ | Compatible with migration |
| 1.7.x - 1.8.x | 1.7+ | Compatible with migration |
| 1.9.x - 1.10.x | Monitor compatibility | Diverging features |

OpenTofu 1.6.2 is fully compatible with Terraform 1.5.x and earlier—the last MPL-licensed version before HashiCorp's license change. This compatibility extends to the state file format: both tools use the same JSON structure, meaning migration requires zero state conversion. You literally swap the `terraform` command for `tofu` and run `tofu init -upgrade` to update provider registries.

The [OpenTofu Registry](https://opentofu.org/registry/) hosts 3,900+ providers and 23,600+ modules—full compatibility with the Terraform ecosystem. Both tools use HashiCorp Configuration Language (HCL), so providers work interchangeably. When you run `tofu init -upgrade`, OpenTofu downloads providers from `registry.opentofu.org` instead of `registry.terraform.io`, but the provider binaries are compatible.

Fidelity's migration validates this claim at enterprise scale. The company migrated 50,000 state files managing 4 million resources without state conversion. David Jackson noted: "The technical side of migration is trivial—it's organizational change management that matters. With proper planning, moving to OpenTofu is a very manageable organizational challenge, not a technical one."

However, compatibility gaps are emerging. Terraform 1.10 introduced write-only attributes in February 2025, and OpenTofu released the same feature in July 2025. Both projects are innovating independently post-fork. As Terraform moves to versions 1.9, 1.10, and beyond, feature parity will require OpenTofu to track and implement equivalent functionality. The longer organizations wait to migrate, the wider this gap becomes.

[Stack Overflow discussions](https://stackoverflow.com/questions/tagged/opentofu) reveal the practical friction: provider version conflicts when migrating back to Terraform, CI/CD pipeline adjustments for GitLab CI and GitHub Actions, and tool compatibility questions for InfraMap and SAM CLI. These aren't blockers, but they're real operational overhead.

> **💡 Key Takeaway #3**
>
> OpenTofu maintains near-perfect compatibility with Terraform through version 1.5.x (the last MPL-licensed release), using identical state file formats that require zero conversion. The migration is as simple as swapping `terraform` for `tofu` commands. However, as both projects innovate independently post-fork, compatibility gaps are emerging for Terraform 1.6+ features. Organizations should migrate sooner rather than later to avoid future divergence pain. Fidelity's 70% migration success rate across 50,000 state files validates the drop-in replacement claim for production use.

## The Decision Framework: When to Switch, When to Stay

The "should I migrate?" question doesn't have a universal answer. The decision depends on your Terraform version, integration depth, compliance requirements, and organizational priorities. Here's a decision tree to guide the choice:

### Migration Decision Tree

```
START: Using Terraform today?
│
├─ YES → Answer these questions:
│   │
│   ├─ Q1: Are you using Terraform Cloud or Enterprise with deep integration?
│   │   ├─ YES → STAY with Terraform (for now)
│   │   │        Reason: Migration disrupts workflows, custom integrations
│   │   │        Alternative: Monitor OpenTofu Cloud alternatives (Spacelift, env0, Scalr)
│   │   │
│   │   └─ NO → Continue to Q2
│   │
│   ├─ Q2: Do you have vendor contracts requiring HashiCorp/IBM support?
│   │   ├─ YES → STAY with Terraform (contractually bound)
│   │   │        Reason: Existing SLAs, support agreements
│   │   │        Alternative: Negotiate OpenTofu support for next renewal
│   │   │
│   │   └─ NO → Continue to Q3
│   │
│   ├─ Q3: Are you using Terraform ≤1.5.x (the last MPL version)?
│   │   ├─ YES → SWITCH to OpenTofu (easy migration)
│   │   │        Reason: Drop-in replacement, no breaking changes
│   │   │        Timeline: Can complete in 1-2 sprints for most orgs
│   │   │
│   │   └─ NO (using 1.6+) → Continue to Q4
│   │
│   ├─ Q4: Do you need state file encryption for compliance?
│   │   ├─ YES → SWITCH to OpenTofu (killer feature)
│   │   │        Reason: Native encryption (OpenTofu 1.7+), Terraform doesn't have it
│   │   │        Impact: Compliance requirements met without backend workarounds
│   │   │
│   │   └─ NO → Continue to Q5
│   │
│   ├─ Q5: Are you building infrastructure tooling, SaaS platforms, or consulting services?
│   │   ├─ YES → SWITCH to OpenTofu (licensing risk)
│   │   │        Reason: BSL restrictions on competitive use
│   │   │        Risk: Legal ambiguity with "embedded or external" services clause
│   │   │
│   │   └─ NO → Continue to Q6
│   │
│   └─ Q6: Does your organization value open-source governance & vendor neutrality?
│       ├─ YES → SWITCH to OpenTofu (strategic choice)
│       │        Reason: Linux Foundation/CNCF governance, community-driven
│       │        Benefit: No vendor lock-in, influence roadmap via contributions
│       │
│       └─ NO → STAY with Terraform (status quo acceptable)
│                Reason: In-house use, no licensing concerns, vendor support preferred
│                Monitor: Watch for OpenTofu feature developments
│
└─ NO (New project) → START with OpenTofu
    Reason: Open source, feature parity, community momentum
    Exception: If Terraform Cloud is required, start with Terraform
```

> **💡 Key Takeaway #4**
>
> The "switch or stay" decision hinges on three factors: Terraform Cloud lock-in, compliance requirements (state encryption), and vendor lock-in tolerance. Teams using Terraform ≤1.5.x should migrate now while it's a drop-in replacement. Organizations requiring state encryption have no choice: OpenTofu is the only option. Deep Terraform Cloud/Enterprise integration is the primary reason to stay, though this creates long-term vendor lock-in risk post-IBM acquisition. New projects should default to OpenTofu unless Terraform Cloud is non-negotiable.

### When to Switch to OpenTofu: The Pro-Migration Case

If two or more of these indicators apply, migration is a clear signal:

**1. State Encryption Required**
Compliance-heavy industries (finance, healthcare, government) need client-side encryption-at-rest. Current workarounds like S3 server-side encryption don't meet audit requirements for client-side encryption before transmission. OpenTofu 1.7+ solves this with native encryption supporting PBKDF2, AWS KMS, and GCP KMS. Terraform offers ephemeral resources in version 1.10, but this doesn't encrypt the entire state file.

**2. Vendor Lock-In Concerns**
IBM's $6.4 billion acquisition signals enterprise focus but raises questions about community priorities. The BSL license restricts competitive use, creating ambiguity for tool vendors and consultancies. OpenTofu's Linux Foundation and CNCF governance provides vendor neutrality—no single company controls the roadmap. Long-term risk: Terraform Cloud pricing changes, feature gates, or strategic pivots driven by IBM's profit motives.

**3. Building Infrastructure Tooling**
If you're building SaaS platforms, devops tool vendors, or consulting services that embed infrastructure management, the BSL's "embedded or external" services clause creates legal risk. OpenTofu's MPL 2.0 license has no competitive restrictions. Tool vendors like Spacelift, ControlMonkey, and env0 support OpenTofu specifically to avoid licensing complications.

**4. Community-Driven Development Preference**
OpenTofu's 160+ contributors (tripled since January 2024) can influence the roadmap through transparent CNCF governance. State encryption was delivered after five years of Terraform community requests going unfulfilled. Feature velocity example: OpenTofu 1.9.1 achieved 63% adoption in just seven days—the fastest patch adoption ever—showing community engagement and trust.

**5. Currently on Terraform ≤1.5.x**
Migration is a drop-in replacement with identical state format and zero conversion. Effort is minimal (Fidelity: 70% of 50,000 state files in two quarters). Risk is low (migration is reversible if needed). Urgency increases as post-1.5.x feature divergence makes future migration harder.

Fidelity's case study validates enterprise-scale migration feasibility. The company started with one internal IaC platform application, pushed it through the full CI/CD pipeline, then phased rollout to 70% of projects over six months. All new deployments now default to OpenTofu unless teams explicitly opt out. This phased approach demonstrates that migration success is 90% change management, 10% technology.

### When to Stay with Terraform: The Pro-Status-Quo Case

If two or more of these indicators apply, staying makes sense:

**1. Terraform Cloud/Enterprise Deep Integration**
Custom policies with Sentinel, workspace orchestration, and CI/CD pipelines tightly coupled to TFC APIs create high migration cost. Alternative OpenTofu Cloud platforms (Spacelift, env0, Scalr) exist, but replicating custom workflows requires weeks of engineering work. If TFC integration is core to your platform, migration disrupts operations significantly.

**2. Vendor Support Requirements**
Existing HashiCorp or IBM support contracts with formal SLAs and escalation paths may be contractually required. Some enterprises mandate vendor-backed software for compliance. Timeline: Negotiate OpenTofu support (available through Spacelift, env0, Scalr) for next contract renewal instead of immediate migration.

**3. Using Terraform 1.6+ Features**
Features introduced post-fork (Terraform 1.6+) may not have OpenTofu equivalents yet. Before migrating, validate compatibility by testing OpenTofu in a dev environment. Risk: Some 1.6+ features may require code changes or waiting for OpenTofu feature parity. Monitor [OpenTofu release notes](https://opentofu.org/blog/) for feature tracking.

**4. No Immediate Pain Points**
If you're using Terraform purely in-house (BSL doesn't affect you), don't need state encryption, and operate at small scale, the migration effort may outweigh strategic benefits. Status quo is acceptable—migrate when triggered by a specific need rather than preemptively.

**5. Risk-Averse Culture**
Organizations with "if it ain't broke, don't fix it" philosophy and extensive change management requirements may prefer to wait for more enterprise adoption proof points. Valid approach: Monitor OpenTofu's growth, validate with proof-of-concept in dev, then migrate when organizational readiness improves.

The honest reality: Staying with Terraform is often about timing, not whether to migrate. Teams should evaluate OpenTofu Cloud alternatives, develop a migration strategy, and plan transition for when vendor lock-in pain exceeds switching costs.

> **💡 Key Takeaway #5**
>
> Staying with Terraform is the rational choice for organizations deeply embedded in Terraform Cloud/Enterprise or with vendor support requirements. However, this creates long-term vendor lock-in risk: IBM's $6.4B acquisition and the BSL license mean Terraform's future is controlled by a single vendor with profit motives. Teams should evaluate OpenTofu Cloud alternatives (Spacelift, env0, Scalr) and develop a migration strategy for when lock-in pain exceeds switching costs. The "when to stay" decision is often about timing, not whether to migrate.

### Feature Comparison: Terraform vs OpenTofu (2025)

| Feature | Terraform | OpenTofu | Winner | Notes |
|---------|-----------|----------|--------|-------|
| **License** | BSL 1.1 (restrictive) | MPL 2.0 (open source) | OpenTofu | Critical for tool vendors, long-term freedom |
| **State Encryption** | No (ephemeral resources only) | Yes (1.7+, native) | OpenTofu | Killer feature for compliance |
| **Governance** | HashiCorp/IBM | Linux Foundation + CNCF | OpenTofu | Community-driven vs vendor-controlled |
| **Version Compatibility** | N/A (original) | 1.6.2 = Terraform ≤1.5.x | Tie | Drop-in replacement validated |
| **Provider Ecosystem** | 3,900+ (official) | 3,900+ (compatible) | Tie | Identical compatibility |
| **Module Ecosystem** | 23,600+ | 23,600+ | Tie | Same registry format |
| **Enterprise Support** | Yes (IBM/HashiCorp) | Yes (Spacelift, env0, Scalr) | Tie | Formal support available for both |
| **Cloud Platform** | Terraform Cloud/Enterprise | Spacelift, env0, Scalr, others | Terraform | TFC has more features currently |
| **Contributor Base** | Closed (HashiCorp only) | 160+ open contributors | OpenTofu | Community can influence roadmap |
| **Release Cadence** | Quarterly | Rapid (1.9.1 in 7 days) | OpenTofu | Community responsiveness |
| **State Migration** | N/A | Zero-downtime, no conversion | OpenTofu | Identical state format |
| **Adoption Momentum** | Declining (10M→OpenTofu) | 300% registry growth YoY | OpenTofu | Market shift signal |
| **Pricing** | Free (OSS) + Cloud paid tiers | Free (OSS) + Cloud alternatives | Tie | Both have free and commercial options |

## Migration Guide: Zero-Downtime Switch to OpenTofu

### Prerequisites: Before You Begin

**Requirements Checklist**:
- [ ] Currently using Terraform ≤1.5.x (for easiest migration) OR 1.6.x-1.8.x (validate compatibility)
- [ ] State files are backed up (copy to separate location)
- [ ] Team has reviewed [OpenTofu migration guide](https://opentofu.org/docs/intro/migration/)
- [ ] CI/CD pipelines documented (will need updates)
- [ ] Terraform version documented per project: `terraform version`
- [ ] Providers and modules inventoried: `terraform providers`

**Risk Assessment**:
- **Low Risk**: Terraform ≤1.5.x, standard providers (AWS, Azure, GCP), no Terraform Cloud integration
- **Medium Risk**: Terraform 1.6.x-1.8.x, custom providers, light TFC usage
- **High Risk**: Terraform ≥1.9.x, heavy TFC/Enterprise integration, custom Sentinel policies

**Recommendation**: Start with low-risk dev/staging environment, validate for 2-4 weeks, then prod. This phased validation approach aligns with GitOps best practices—learn more in our [Kubernetes IaC & GitOps episode](/podcasts/00020-kubernetes-iac-gitops).

### Step-by-Step Migration Process

**Phase 1: Installation & Validation (Day 1)**

**Step 1**: Install OpenTofu

```bash
# macOS (Homebrew)
brew install opentofu

# Linux (package manager)
snap install opentofu --classic

# Or download binary from https://opentofu.org/docs/intro/install/
```

**Step 2**: Verify current Terraform state

```bash
cd your-terraform-project/
terraform plan

# Expected output:
# No changes. Your infrastructure matches the configuration.
```

**Step 3**: Initialize OpenTofu (upgrade flag is critical)

```bash
tofu init -upgrade
```

**Why `-upgrade`**: Downloads providers/modules from `registry.opentofu.org` instead of `registry.terraform.io`

**Step 4**: Verify no infrastructure drift

```bash
tofu plan

# Expected output:
# No changes. Your infrastructure matches the configuration.
```

**Critical**: If `tofu plan` shows changes, investigate before proceeding. This indicates provider version differences, state file issues, or configuration drift.

**Phase 2: State File Migration (Day 1-2)**

**Step 5**: Update state file (no content changes, just metadata)

```bash
tofu apply

# This updates state file metadata from "terraform" to "tofu"
# No infrastructure changes occur
```

**Step 6**: Verify state file format

```bash
# State file is still JSON, just metadata changed
# Backend location unchanged (S3, Terraform Cloud, local)

tofu state list  # Verify all resources present
```

**State File Compatibility Note**: State format is identical between Terraform and OpenTofu. No state "conversion" happens—just metadata update. Migration is reversible (remove OpenTofu-specific features like encryption).

**Phase 3: CI/CD Pipeline Updates (Day 2-3)**

**Step 7**: Update CI/CD workflows

**GitHub Actions** example:

```yaml
# Before
- uses: hashicorp/setup-terraform@v2
  with:
    terraform_version: 1.5.0

# After
- uses: opentofu/setup-opentofu@v1
  with:
    tofu_version: 1.6.2
```

**GitLab CI** example:

```yaml
# Before
image: hashicorp/terraform:1.5

# After
image: ghcr.io/opentofu/opentofu:1.6.2
```

**Jenkins** update: Install OpenTofu on Jenkins agents, update Jenkinsfile: `terraform` → `tofu` commands, test in sandbox environment first.

**Phase 4: Team Rollout (Week 1-2)**

**Step 8**: Developer machine setup

```bash
# Each team member installs OpenTofu
# Update shell aliases (if any): alias tf='tofu'
# Update IDE plugins: VSCode Terraform → OpenTofu extensions
```

**Step 9**: Documentation updates—update runbooks (`terraform` → `tofu` commands), onboarding docs, architecture diagrams (logos, tool names).

**Step 10**: Knowledge sharing session—30-min team demo: migration process, why OpenTofu, Q&A: address concerns (reversibility, support, ecosystem), share Fidelity case study for confidence.

**Phase 5: Rollback Plan (Just in Case)**

If migration issues occur:

**1. Revert to Terraform**:

```bash
terraform init  # Re-download Terraform providers
terraform plan  # Verify no drift
```

**2. Remove OpenTofu-specific features**: State encryption config (if added), OpenTofu 1.7+ exclusive features.

**3. Provider version conflicts**: Lock provider versions in `terraform.lock.hcl`, may need to downgrade providers if OpenTofu used newer versions.

**4. CI/CD rollback**: Revert pipeline changes, switch Docker images back to Terraform.

[Stack Overflow reports](https://stackoverflow.com/questions/78224921/incompatible-provider-version-when-migrating-back-from-opentofu-to-terraform) indicate provider versioning is the main rollback concern.

### Fidelity's Migration Playbook: Lessons from 50,000 State Files

**Scale**: 2,000 applications, 50,000 state files, 4 million resources

**Approach**:
1. **Proof of Concept**: Started with one internal IaC platform application
2. **End-to-End Validation**: Pushed through full CI/CD pipeline (artifact storage, governance, everything)
3. **Phased Rollout**: 70% of projects migrated over two quarters
4. **Default to OpenTofu**: All new deployments use OpenTofu unless teams opt out
5. **Deprecation Plan**: Now deprecating older Terraform versions

David Jackson, VP Automation Tooling (Fidelity): "With proper planning, moving to OpenTofu is a very manageable organizational challenge, not a technical one. The technical side is trivial—it's change management that matters."

**Success Factors**:
- Executive buy-in (licensing concerns drove decision)
- Phased approach (not "big bang" migration)
- Default to new tool (opt-out instead of opt-in)
- Validation at scale (one app → pipeline → all apps)

**Timeline**:
- Proof of Concept: 2-4 weeks
- First production app: 1-2 months
- 70% migration: 6 months (2 quarters)

> **💡 Key Takeaway #6**
>
> Fidelity's migration of 50,000 state files validates zero-downtime migration at enterprise scale. The key insight: migration is 90% organizational change management, 10% technical execution. The technical switch is trivial (swap `terraform` for `tofu`), but success requires phased rollout, team training, and defaulting new projects to OpenTofu. Organizations can complete migration in 1-2 quarters with proper planning, starting with proof-of-concept, validating through full CI/CD, then rolling out incrementally. The migration is reversible for standard configurations, reducing risk.

## Practical Application: Your First 90 Days

### Days 1-30: Assessment & Proof of Concept

**Week 1: Decision & Planning**—Review this decision framework with your team, identify migration priority (state encryption need, licensing concern, vendor neutrality), select proof-of-concept project (low-risk dev environment, standard providers), backup state files (copy to separate location before any changes).

**Week 2: PoC Execution**—Install OpenTofu on 1-2 machines, migrate PoC project: `tofu init -upgrade` → `tofu plan` → `tofu apply`, validate (infrastructure unchanged, state file readable), test rollback (can you revert to Terraform if needed?).

**Week 3: CI/CD Integration**—Update PoC pipeline (GitHub Actions, GitLab CI, or Jenkins), run full deployment cycle (Code → Build → Plan → Apply → Verify), measure (any performance differences? provider download issues?).

**Week 4: Team Demo & Decision**—Present PoC results to team, decision gate (continue with broader rollout or address blockers?), if continuing, create migration project plan.

### Days 31-60: Phased Rollout

**Prioritization**:
1. **Low-hanging fruit**: Projects on Terraform ≤1.5.x, no TFC integration
2. **Medium complexity**: Projects with custom modules, multiple environments
3. **High complexity**: Projects with TFC integration, custom policies

**Rollout Pattern** (Fidelity approach):
- **Week 5-6**: Migrate 5-10 low-risk projects
- **Week 7-8**: Validate for 2 weeks (catch any drift or issues)
- **Week 9**: Expand to 20-30 projects if validation successful

**Team Training**—30-min brown bag: Why OpenTofu, how to migrate, where to get help. Update documentation: runbooks, onboarding guides. Designate "OpenTofu champions": 2-3 team members as go-to experts.

### Days 61-90: Default to OpenTofu

**Policy Change**: New projects default to OpenTofu—update project templates, CI/CD templates (GitHub Actions workflows, GitLab CI includes), onboarding docs for new hires.

**Migration Target**: 50-70% of projects migrated—following Fidelity's pattern (70% in two quarters), focus on momentum (success breeds success).

**Measure Success**: Migration count (X projects / Y total), incident rate (any migration-related issues?), team confidence (survey satisfaction).

### Red Flags to Watch

🚩 **Provider Version Conflicts**: OpenTofu using newer provider version than Terraform expects—**Fix**: Lock provider versions in `terraform.lock.hcl` / `opentofu.lock.hcl`

🚩 **CI/CD Pipeline Failures**: Image not found, command not recognized—**Fix**: Update Docker images to OpenTofu, install OpenTofu in Jenkins agents

🚩 **Team Resistance**: "Why are we changing? Terraform works fine."—**Fix**: Share Fidelity case study, explain licensing/lock-in risk, show state encryption value

🚩 **Terraform Cloud Integration Breaking**: Custom policies, workspace orchestration affected—**Fix**: Evaluate OpenTofu Cloud alternatives (Spacelift, env0, Scalr) OR delay migration

🚩 **Provider Not Available in OpenTofu Registry**: Rare, but possible—**Fix**: Use Terraform provider registry as fallback OR contribute provider to OpenTofu

### Common Mistakes to Avoid

**❌ Mistake 1**: Migrating all projects at once ("big bang")—**Why bad**: No learning, high risk, overwhelming for team—**Do instead**: Phased rollout, learn from each batch

**❌ Mistake 2**: Skipping CI/CD pipeline updates—**Why bad**: Manual migrations work, automation breaks—**Do instead**: Update pipelines immediately after manual validation

**❌ Mistake 3**: Not backing up state files first—**Why bad**: If something goes wrong, no recovery path—**Do instead**: Copy state files to separate location before migration

**❌ Mistake 4**: Assuming 100% compatibility without testing—**Why bad**: Edge cases exist (custom providers, Terraform 1.6+ features)—**Do instead**: Test in dev, validate for 2 weeks, then production

**❌ Mistake 5**: Forgetting team training—**Why bad**: Developers confused, inconsistent adoption—**Do instead**: Brown bag session, update docs, designate champions

### Monday Morning Actions

**If you decide to migrate**:
1. Install OpenTofu on your machine: `brew install opentofu` (macOS) or download binary
2. Pick one dev project: Low-risk, non-production
3. Backup state file: `cp terraform.tfstate terraform.tfstate.backup`
4. Run migration: `tofu init -upgrade && tofu plan`
5. If plan shows no changes: `tofu apply` (updates state metadata)

**If you decide to stay (for now)**:
1. Document decision: Why staying, what would trigger migration
2. Monitor OpenTofu releases: Subscribe to https://opentofu.org/blog/
3. Evaluate Terraform Cloud alternatives: Spacelift, env0, Scalr (for future)
4. Plan next review: 6 months, reassess with team

**If you're starting a new project**:
1. Default to OpenTofu unless Terraform Cloud required
2. Use latest version: OpenTofu 1.10+ (as of June 2025)
3. Enable state encryption from day 1: OpenTofu 1.7+ feature
4. Document choice for future team members

> **💡 Key Takeaway #7**
>
> The "first 90 days" follow Fidelity's proven pattern: proof-of-concept (days 1-30), phased rollout (days 31-60), default to OpenTofu for new projects (days 61-90). Success requires treating migration as organizational change management, not just technical execution. Start with one low-risk project, validate thoroughly, then expand incrementally. By day 90, aim for 50-70% migration completion with OpenTofu as the default for new work. The key mistake teams make is "big bang" migrations instead of phased learning. Take the methodical approach: every batch teaches lessons for the next.

For teams evaluating infrastructure-as-code strategies, this comparison provides a framework for understanding how licensing, governance, and feature differences impact your specific infrastructure needs.

## Learning Resources

### Official Documentation (2)
1. **OpenTofu Documentation** - https://opentofu.org/docs/ - Migration guides, state encryption setup, provider configuration. Maintained by Linux Foundation, current as of OpenTofu 1.10.

2. **Terraform Documentation** - https://www.terraform.io/docs - Reference for understanding differences post-fork. HashiCorp/IBM official docs.

### Migration Guides (3)
3. **ControlMonkey: 2025 Terraform to OpenTofu Migration Guide** - https://controlmonkey.io/blog/opentofu-migration/ - Published 2025, step-by-step process. Version compatibility matrix, rollback procedures.

4. **Scalr: Migrating from Terraform to OpenTofu** - https://scalr.com/learning-center/migrating-from-terraform-to-opentofu/ - Enterprise-focused patterns, state management at scale.

5. **Ned in the Cloud: Migrating to OpenTofu** (Duration: 15 min read) - https://nedinthecloud.com/2024/07/24/migrating-to-opentofu/ - Technical blog, hands-on migration experience, July 2024.

### Case Studies (2)
6. **Fidelity Investments: 50,000 State File Migration** - https://opentofu.org/blog/fidelity-investment-migration/ - Official case study: 2,000 apps, 4M resources, 70% in 2 quarters. VP-level insights on organizational change management.

7. **Harness: Fidelity's OpenTofu Migration - A DevOps Success Story** - https://www.harness.io/blog/fidelitys-opentofu-migration-a-devops-success-story-worth-studying - Third-party analysis of Fidelity migration. Lessons learned, success factors.

### Comparison Resources (2)
8. **Spacelift: OpenTofu vs Terraform** - https://spacelift.io/blog/opentofu-vs-terraform - Feature-by-feature comparison, updated regularly. Vendor perspective (supports both).

9. **Infisical: Terraform vs OpenTofu** - https://infisical.com/blog/terraform-vs-opentofu - Security-focused comparison (state encryption emphasis).

### Community & Ecosystem (2)
10. **OpenTofu Registry** - https://opentofu.org/registry/ - Browse 3,900+ providers, 23,600+ modules. Check provider/module compatibility before migration.

11. **CNCF OpenTofu Project Page** - https://www.cncf.io/projects/opentofu/ - Governance structure, community resources. Links to GitHub, Slack, mailing lists.

### Tools (2)
12. **tfmigrate: State Migration Tool for GitOps** - https://github.com/minamijoyo/tfmigrate - Open-source automation for complex state transitions. Helps manage multi-environment migrations.

13. **Terragrunt: OpenTofu and Terraform Version Compatibility** - https://terragrunt.gruntwork.io/docs/reference/supported-versions/ - Compatibility matrix for Terraform/OpenTofu versions. Essential for understanding migration paths.

### Books (1)
14. **"Terraform: Up & Running" by Yevgeniy Brikman** (3rd Edition, 2022) - [O'Reilly](https://www.oreilly.com/library/view/terraform-up/9781098116736/) - While Terraform-focused, concepts apply to OpenTofu. Covers state management, testing, team collaboration. Purchase: O'Reilly, Amazon ($49.99).

### Video Resources (1)
15. **"Seamless at Scale: Migrating from Terraform to OpenTofu Without Missing a Beat"** (Duration: 45 min, estimated) - David Jackson, VP Automation Tooling, Fidelity Investments. Presented at OpenTofu community event. Search: YouTube, OpenTofu channel for recording.

## Sources & References

### Primary Research
1. **OpenTofu 1.10.0 Release Announcement** - OpenTofu Project, June 2025 - https://opentofu.org/blog/opentofu-1-10-0/
2. **Fidelity Investments Migration Story** - Futuriom, April 2025 - https://www.futuriom.com/articles/news/fidelity-ditches-terraform-for-opentofu/2025/04
3. **OpenTofu Official Migration Guide** - OpenTofu Documentation, 2025 - https://opentofu.org/docs/intro/migration/
4. **IBM Acquires HashiCorp Press Release** - IBM Newsroom, April 24, 2024 - https://newsroom.ibm.com/2024-04-24-IBM-to-Acquire-HashiCorp-Inc

### Industry Reports
5. **Spacelift: OpenTofu 1.10 Major Updates Analysis** - Spacelift Blog, June 2025 - https://spacelift.io/blog/opentofu-1-10-major-updates-for-modern-iac
6. **InfraJump: OpenTofu Growth Statistics** - InfraJump, 2025 - https://infrajump.com/opentofu-is-growing-fast/
7. **The New Stack: OpenTofu Joins CNCF** - The New Stack, April 2025 - https://thenewstack.io/opentofu-joins-cncf-new-home-for-open-source-iac-project/

### Practitioner Insights
8. **Harness: Fidelity's DevOps Success Story** - Harness Blog, 2025 - https://www.harness.io/blog/fidelitys-opentofu-migration-a-devops-success-story-worth-studying
9. **Ned in the Cloud: Migrating to OpenTofu** - Ned Bellavance, July 2024 - https://nedinthecloud.com/2024/07/24/migrating-to-opentofu/
10. **ComputerTechReviews: Why Developers Are Migrating** - CTR Analysis, 2025 - https://www.computertechreviews.com/why-developers-are-migrating-from-terraform-to-opentofu/

### Technical Documentation
11. **OpenTofu State Encryption Documentation** - OpenTofu Docs - https://opentofu.org/docs/language/state/encryption/
12. **HashiCorp License FAQ** - HashiCorp, 2023 - https://www.hashicorp.com/en/license-faq
13. **Terragrunt Version Compatibility Table** - Gruntwork, 2025 - https://terragrunt.gruntwork.io/docs/reference/supported-versions/

### License Change Context
14. **Spacelift: Terraform License Change Analysis** - Spacelift, August 2023 - https://spacelift.io/blog/terraform-license-change
15. **DuploCloud: BSL Impact on DevOps** - DuploCloud Blog, 2023 - https://duplocloud.com/blog/terraform-license-change-impacts-devops/
16. **The New Stack: Linux Foundation Joins OpenTofu** - The New Stack, September 2023 - https://thenewstack.io/linux-foundation-joins-opentf-to-fork-for-terraform-into-opentofu/

### Comparison Resources
17. **Spacelift: OpenTofu vs Terraform Comparison** - Spacelift, 2025 - https://spacelift.io/blog/opentofu-vs-terraform
18. **Infisical: Terraform vs OpenTofu** - Infisical Blog, 2025 - https://infisical.com/blog/terraform-vs-opentofu
19. **CyberPanel: OpenTofu vs Terraform** - CyberPanel, 2025 - https://cyberpanel.net/blog/opentofu-vs-terraform
20. **Pulumi: OpenTofu vs Terraform** - Pulumi Docs - https://www.pulumi.com/docs/iac/comparisons/terraform/opentofu/

### Migration Tools & Guides
21. **ControlMonkey: 2025 Migration Guide** - ControlMonkey Blog, 2025 - https://controlmonkey.io/blog/opentofu-migration/
22. **Scalr: Migration Guide** - Scalr Learning Center - https://scalr.com/learning-center/migrating-from-terraform-to-opentofu/
23. **Firefly: Migration - The How and Why** - Firefly Academy - https://www.firefly.ai/academy/migrating-from-terraform-to-opentofu-the-how-and-why

### Governance & Community
24. **CNCF OpenTofu Project Page** - Cloud Native Computing Foundation - https://www.cncf.io/projects/opentofu/
25. **Medium: CNCF Sandbox Acceptance** - Alexander Sharov, April 2025 - https://medium.com/@kvendingoldo/opentofu-becomes-a-cncf-sandbox-project-df2466210bd0
26. **OpenTofu GitHub Repository** - https://github.com/opentofu/opentofu
27. **OpenTofu Registry Metadata** - https://github.com/opentofu/registry

### Real-World Issues (Stack Overflow)
28. **Stack Overflow: OpenTofu Tag** - Community Q&A - https://stackoverflow.com/questions/tagged/opentofu
29. **Stack Overflow: Migration Back Compatibility Issues** - https://stackoverflow.com/questions/78224921/incompatible-provider-version-when-migrating-back-from-opentofu-to-terraform

### Additional Context
30. **Platform Engineering Community Discussion** - https://community.platformengineering.org/t/26977830/any-opinions-here-on-terraform-vs-opentofu
31. **IBM Acquisition Analysis** - DevOps.com, 2024 - https://devops.com/ibm-confirms-its-buying-hashicorp-2/
32. **SDxCentral: IBM Acquires HashiCorp** - SDxCentral, April 2024 - https://www.sdxcentral.com/articles/news/ibm-acquires-hashicorp-for-6-4b-open-source-terraform-questions-remain/2024/04/
