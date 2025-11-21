---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #032: Terraform vs OpenTofu Debate"
slug: 00032-terraform-opentofu-debate
---

# The Terraform vs OpenTofu Debate - Why "Just Switch" Is Bad Advice

import GitHubButtons from '@site/src/components/GitHubButtons';

<GitHubButtons />

**Duration**: 17 minutes | **Speakers**: Jordan and Alex | **Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/2025-11-20-terraform-vs-opentofu-2025-when-to-switch-when-to-stay)**: Deep dive into the three-factor decision framework with Fidelity's 50,000 state file migration case study, compliance requirements, and the 90-day migration playbook.

## Summary

HashiCorp's license change and IBM's $6.4B acquisition created the "you must migrate" narrative—but 70% of teams using Terraform in-house aren't legally affected. Jordan and Alex challenge the binary thinking with Fidelity's 50,000 state file migration case study, a three-factor decision framework, and the truth nobody talks about: migration is 90% organizational change management, not technology.

**Key Points**:
• 70% of teams using Terraform in-house are unaffected by BSL license restrictions, yet face strategic vendor lock-in risk with IBM's $6.4B acquisition
• Fidelity migrated 50,000 state files managing 4M resources in 2 quarters—technical migration is trivial, organizational change management is the challenge (6 months to 70% completion)
• OpenTofu 1.7+ delivers native state encryption after 5+ years of Terraform community requests going unfulfilled—for compliance-heavy industries (finance, healthcare, government), this alone justifies migration
• Decision framework: Switch if you need state encryption, build infrastructure tooling (BSL restrictions), or are on Terraform ≤1.5.x; stay if deeply embedded in Terraform Cloud/Enterprise or have vendor support contracts
• 90-day migration playbook: Days 1-30 proof of concept, days 31-60 phased rollout (5-10 projects, validate 2 weeks, expand), days 61-90 default to OpenTofu for new projects (aim for 50-70% completion)

---

## Listen

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, overflow: 'hidden'}}>
  <iframe
    src="https://www.youtube.com/embed/uHPI1EkeRH8"
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    frameBorder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowFullScreen
  />
</div>

---

## Transcript

**Jordan**: Today we're diving into the Terraform versus OpenTofu debate. And I know, I know—you're probably thinking "another hot take on the license change."  But here's what nobody's talking about: seventy percent of teams using Terraform purely in-house are completely unaffected by the license restrictions,  yet they're being told to migrate immediately.

**Alex**: Wait, seventy percent unaffected?  That seems... counterintuitive given how much pressure there is to switch.

**Jordan**: Right?  In August twenty twenty-three, HashiCorp changed Terraform's license from the open-source Mozilla Public License to the Business Source License. The internet lost its mind. Within months, four hundred companies signed the OpenTF Manifesto, the Linux Foundation forked the codebase into OpenTofu,  and by April twenty twenty-four, IBM paid six point four billion dollars to acquire HashiCorp anyway.

**Alex**: Six point four billion.  That's not pocket change. Thirty-five dollars a share.

**Jordan**: Exactly. And that acquisition intensified the vendor lock-in concerns. But  here's the thing—if you're using Terraform to manage your infrastructure in-house, which is what seventy percent of teams do, the BSL license doesn't legally restrict you.  Building competing commercial products or services? That's where the restrictions kick in.

**Alex**: So tool vendors, consultancies, SaaS platforms—

**Jordan**: They're the ones who face existential license restrictions. Companies like Spacelift, ControlMonkey, env zero—they all had to support OpenTofu specifically to avoid licensing complications. But for the average platform team just managing their AWS infrastructure? The license change itself isn't the problem.

**Alex**: Okay, but then why is everyone saying "you must migrate or you're supporting vendor lock-in"?

**Jordan**: Because IBM's six point four billion wasn't an act of charity. They're going to monetize Terraform somehow. The BSL license means no competitive forks, no community steering committee, and profit-driven feature decisions. The strategic risk is real even if the immediate legal risk isn't.

**Alex**: So it's about future control, not current restrictions.

**Jordan**: Exactly. And that's where the conversation gets interesting.  Let's talk about Fidelity Investments—they migrated fifty thousand state files managing four million cloud resources across two thousand applications.  Seventy percent of their projects moved to OpenTofu in two quarters.

**Alex**: Fifty thousand state files.  That's... that's a massive validation of the migration path.

**Jordan**: It is. But here's what David Jackson, their VP of Automation Tooling, said—and I'm quoting here: "The technical side of migration is trivial. It's organizational change management that matters."

**Alex**: Trivial? That feels like an overstatement.

**Jordan**: No, he's right technically. OpenTofu one point six point two is a drop-in replacement for Terraform one point five x and earlier. Same state file format. You literally swap the terraform command for tofu, run tofu init upgrade, and you're done. No state conversion needed.

**Alex**: Okay, so technically simple. But organizationally?

**Jordan**: That's where it gets messy. Think about what Fidelity actually had to do. They started with one internal infrastructure-as-code platform application, pushed it through their full CI/CD pipeline—artifact storage, governance checks, everything. Then they did a phased rollout. Five to ten low-risk projects first, validated for two weeks, then expanded.

**Alex**: So proof of concept, validate, expand incrementally.

**Jordan**: Right. And they had to update CI slash CD pipelines for every project. GitHub Actions workflows, GitLab CI configs, Jenkins files. Documentation had to be updated. Team training. They designated "OpenTofu champions" as go-to experts. This took six months to hit seventy percent migration.

**Alex**: Six months for a technically trivial change.

**Jordan**: Because it's ninety percent organizational change management, ten percent technology.  You're asking developers to change their muscle memory. "terraform plan" becomes "tofu plan." IDE plugins need updating. Shell aliases. And if you hit any provider version conflicts during rollback testing, you need someone who knows how to debug that.

**Alex**: So when people say "just switch," they're dramatically underestimating the coordination effort.

**Jordan**: Completely. And here's another complexity—if you're deeply embedded in Terraform Cloud or Enterprise with custom Sentinel policies, workspace orchestration, CI slash CD pipelines tightly coupled to TFC APIs... migrating means weeks of engineering work to replicate those workflows on alternatives like Spacelift or env zero or Scalr.

**Alex**: So Terraform Cloud lock-in is its own separate problem from the open-source versus proprietary debate.

**Jordan**: Exactly. And this is why I said the "just switch" narrative is bad advice. You need to understand your specific constraints. Let me give you a decision framework.

**Alex**: Please. Because right now it feels like ideology versus pragmatism.

**Jordan**: It's three factors. First: Terraform Cloud lock-in. If you have deep integration—custom policies, orchestration, APIs—the migration cost is high. You're looking at weeks of engineering work, not a weekend project.

**Alex**: And there's no drop-in Terraform Cloud replacement.

**Jordan**: There are alternatives—Spacelift, env zero, Scalr—but you have to rebuild custom workflows. Second factor: compliance requirements. If you need state file encryption, OpenTofu is your only option.

**Alex**: Wait, Terraform doesn't have state encryption?

**Jordan**: The community has been requesting it since twenty sixteen.  Most upvoted issue on HashiCorp's GitHub for over five years: "Add support for encrypting state files."  HashiCorp's answer has always been "use S three server-side encryption, AWS KMS, or third-party backends."

**Alex**: Backend-specific workarounds instead of client-side encryption.

**Jordan**: Right. And for organizations in finance, healthcare, government—encryption-at-rest requirements can't be met with backend workarounds alone. They need client-side encryption before the state file even leaves the execution environment.  OpenTofu one point seven shipped that in twenty twenty-four. Native client-side encryption supporting PBKDF two, AWS KMS, GCP KMS. Works with both local storage and remote backends.

**Alex**: After five years of community requests, HashiCorp never built it, but OpenTofu delivered in their second year?

**Jordan**: Yep.  And Terraform's response in version one point ten was "ephemeral resources"—values that aren't saved to state at all. Which solves secrets leakage for specific resources,  but doesn't encrypt the entire state file for compliance.

**Alex**: So if you're in a compliance-heavy industry and you need state encryption, the decision is made for you. OpenTofu is the only option.

**Jordan**: Exactly. This feature alone justifies migration for a specific subset of teams. And this gets to the third factor: vendor lock-in tolerance. Can you accept IBM controlling Terraform's roadmap? Because the BSL license means no competitive forks, no community steering, and profit-driven feature gates are possible.

**Alex**: But isn't that also true of OpenTofu if the Linux Foundation decides to change course?

**Jordan**: Different governance model. OpenTofu is under the Linux Foundation with CNCF Sandbox status as of April twenty twenty-five. That means transparent community processes. Contributors from multiple organizations can influence the roadmap, not just a single company's product team.

**Alex**: So open governance versus vendor control.

**Jordan**: Right. And for some organizations, that matters. For others, vendor-backed commercial support is actually a requirement. Some enterprises mandate vendor-backed software for compliance reasons, formal SLAs, escalation paths. If you have existing HashiCorp or IBM contracts, you might be contractually bound to stay.

**Alex**: Okay, so let me synthesize this. The decision isn't just "open source good, proprietary bad."

**Jordan**: Exactly. Let me lay out when you should switch versus when staying makes sense. Switch to OpenTofu if: one, state encryption is required for compliance. Two, you're building infrastructure tooling, SaaS platforms, or consulting services where the BSL restrictions create legal risk. Three, you're currently on Terraform one point five x or earlier—it's a drop-in replacement with minimal effort. Or four, your organization values open-source governance and you want to avoid vendor lock-in with IBM.

**Alex**: And when to stay with Terraform?

**Jordan**: Stay if: one, you're deeply embedded in Terraform Cloud or Enterprise with custom workflows that would take weeks to replicate. Two, you have vendor contracts requiring HashiCorp or IBM support. Three, you're using Terraform one point six plus features that don't have OpenTofu equivalents yet—compatibility gaps are emerging as both projects innovate independently post-fork. Or four, you have a risk-averse culture that prefers waiting for more enterprise adoption proof points before migrating.

**Alex**: What about new projects? If you're starting from scratch?

**Jordan**: Default to OpenTofu unless Terraform Cloud is non-negotiable. Open source, feature parity exists, the momentum is clear.  Ten million plus downloads as of June twenty twenty-five. Registry traffic increased three hundred percent year over year to six million requests per day.  Three thousand nine hundred plus providers, twenty-three thousand six hundred plus modules. The ecosystem is there.

**Alex**: And for teams that decide to migrate—what does that actually look like in practice?

**Jordan**: Fidelity's playbook is instructive. Days one through thirty: proof of concept. Pick one dev project that's low risk, non-production. Install OpenTofu, run tofu init upgrade, verify with tofu plan. If the plan shows no changes, you're good. Run tofu apply to update the state metadata. Test rollback—can you revert to Terraform if needed?

**Alex**: So validate the happy path and the failure path.

**Jordan**: Exactly. Then update your CI slash CD pipeline for that one project. GitHub Actions, GitLab CI, Jenkins—whatever you use. Run the full deployment cycle and make sure nothing breaks. Days thirty-one through sixty: phased rollout. Start with five to ten low-risk projects that are on Terraform one point five x or earlier with no Terraform Cloud integration. Migrate those, validate for two weeks to catch any drift or issues, then expand to twenty to thirty projects if validation succeeds.

**Alex**: So you're learning from each batch before expanding.

**Jordan**: Right. And during this phase, you're doing team training. Thirty-minute brown bag sessions: why OpenTofu, how to migrate, where to get help. Update your documentation—runbooks, onboarding guides. Designate a couple OpenTofu champions who become the go-to experts.

**Alex**: And then days sixty-one through ninety?

**Jordan**: You flip the default. New projects use OpenTofu unless teams explicitly opt out. Update your project templates, CI slash CD templates, onboarding docs for new hires. The goal is fifty to seventy percent of projects migrated by day ninety, following Fidelity's pattern. Success breeds success—the more teams migrate, the more normal it becomes.

**Alex**: So it's an organizational momentum play, not just a technical switch.

**Jordan**: Exactly. And here's the key insight from Fidelity's David Jackson again: "With proper planning, moving to OpenTofu is a very manageable organizational challenge, not a technical one."

**Alex**: So what are the common mistakes teams make during migration?

**Jordan**: Biggest one is trying to migrate all projects at once—the big bang approach. No learning, high risk, overwhelming for the team. You want phased rollout where each batch teaches you lessons for the next. Second mistake: skipping CI slash CD pipeline updates. Manual migrations work fine, but then automation breaks in production and everyone panics.

**Alex**: Yeah, that's a nightmare scenario.

**Jordan**: Third mistake: not backing up state files first. If something goes wrong and you don't have a recovery path, you're in trouble. Fourth: assuming one hundred percent compatibility without testing. There are edge cases—custom providers, Terraform one point six plus features. You need to test in dev, validate for two weeks, then move to production. And fifth mistake: forgetting team training. Developers get confused, adoption becomes inconsistent, people start working around the new system.

**Alex**: So it's really about respecting the organizational complexity.

**Jordan**: Right. And here's what frustrates me about the "just switch" narrative in the community—it treats this as a purely technical decision driven by ideology.  "You must migrate or you're supporting vendor lock-in." But  the reality is more nuanced. Some teams should absolutely migrate. If you need state encryption for compliance, you have no choice. If you're on Terraform one point five x, it's a straightforward technical lift with clear strategic benefits.

**Alex**: But if you're deeply embedded in Terraform Cloud with custom integrations?

**Jordan**: Then migration disrupts operations significantly, and you need to evaluate whether the vendor lock-in pain exceeds the switching costs right now. Maybe the answer is yes. Maybe it's not yet, but you develop a migration strategy for when it becomes unbearable. That's a rational decision, not ideological weakness.

**Alex**: And for teams that are risk-averse and want to wait for more proof points?

**Jordan**: That's valid too. Monitor OpenTofu's growth. Run a proof of concept in dev to validate compatibility. Migrate when organizational readiness improves. The licensing earthquake forced platform teams to confront a question they'd avoided: do we bet on vendor-controlled tooling with commercial support, or do we prioritize open-source governance and community-driven development? The answer isn't universal.

**Alex**: But the question is now unavoidable.

**Jordan**: Exactly. And that's the real takeaway here. Not "everyone must migrate immediately" or "staying with Terraform makes you a corporate sell-out." The takeaway is: you need a decision framework that accounts for your Terraform Cloud lock-in, your compliance requirements, and your tolerance for vendor control. Then you need a tactical migration plan that treats this as ninety percent organizational change management.

**Alex**: The three-factor model plus the ninety-day playbook.

**Jordan**: Right. And if you want the full analysis—we wrote a comprehensive guide with Fidelity's fifty thousand state file case study, the complete decision tree, and the step-by-step migration process. Check the show notes for the link.

**Alex**: Because this is too important to get wrong.

**Jordan**: Agreed. Whether you switch or stay, make it a deliberate decision based on your constraints, not just community pressure.  The fundamentals of infrastructure-as-code haven't changed. What changed is who controls the roadmap and under what terms.  That's a strategic decision that deserves strategic thinking.
