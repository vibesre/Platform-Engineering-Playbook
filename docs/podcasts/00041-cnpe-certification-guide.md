---
title: "Episode #041: CNPE Certification Guide - The First Platform Engineering Credential"
description: "A complete guide to CNCF's new Certified Cloud Native Platform Engineer (CNPE) exam - exam domains, preparation strategies, career impact, and whether it's right for you."
slug: 00041-cnpe-certification-guide
sidebar_label: "🎙️ #041: CNPE Certification Guide"
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
---

import GitHubButtons from '@site/src/components/GitHubButtons';

# Episode #041: CNPE Certification Guide - The First Platform Engineering Credential

<GitHubButtons />

**Duration**: ~15 minutes

**Speakers**: Jordan (Kore) and Alex (Algieba)

**Target Audience**: Platform engineers, SREs, DevOps engineers considering career advancement

---

## Watch the Episode

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube.com/embed/fFUtYu8sk60" title="Episode #041: CNPE Certification Guide" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

---

## Episode Summary

CNCF just launched the first-ever hands-on platform engineering certification at KubeCon Atlanta 2025. But with beta testers reporting 29% scores and no exam simulator until Q1 2026, is CNPE worth pursuing now?

In this episode, Jordan and Alex break down everything you need to know about CNPE: the five exam domains, how it compares to existing certifications, career impact (platform engineers earn $219K average - 20% more than DevOps), and a practical framework for deciding when and if to pursue this credential.

---

## Key Topics

- **CNPE Launch**: First new hands-on CNCF certification in 5 years
- **Five Exam Domains**: GitOps/CD (25%), Platform APIs (25%), Observability (20%), Architecture (15%), Security (15%)
- **Beta Test Reality**: Experienced testers reporting 29% scores
- **Career Impact**: Platform engineers earn $219K average (US), 20% higher than DevOps
- **CNPA vs CNPE**: When to start with the associate exam
- **Certification Paths**: Three recommended approaches for platform engineers
- **Golden Kubestronaut**: CNPE required after March 1, 2026
- **Preparation Strategy**: What to study while waiting for Killer.sh simulator

---

## Episode Transcript

**Jordan**: Today we're diving into something that just happened two weeks ago at KubeCon Atlanta. CNCF launched the first-ever hands-on platform engineering certification. It's called CNPE, Certified Cloud Native Platform Engineer. And here's the thing, beta testers are reporting scores around 29%.

**Alex**: 29%? That's... concerning. Or maybe it's promising? I mean, platform engineers earn an average of $219,000 in the US. That's 20% more than DevOps engineers. Gartner says 80% of enterprises will have platform teams by 2026. So there's clearly demand. But until November 11th, 2025, there was no official credential.

**Jordan**: Exactly. And that's what makes this interesting. CNCF has 15 vendor-neutral certifications now, but CNPE is the first new hands-on certification in five years. The last one was CKS, the Certified Kubernetes Security Specialist, back in 2020.

**Alex**: So what makes CNPE different from the existing Kubernetes certifications? We've got CKA for cluster administration, CKAD for application development, CKS for security. Where does CNPE fit?

**Jordan**: CNPE tests the entire cloud-native stack, not just Kubernetes. Think about it. Platform engineering isn't just about managing clusters. It's about building internal developer platforms, setting up GitOps workflows, creating self-service capabilities, observability across the entire platform, security and policy enforcement. CNPE covers all of that.

**Alex**: That explains the difficulty then. You can't just know Kubernetes well. You need breadth across monitoring, observability, security, automation, APIs, and organizational practices. Let's break down what the exam actually tests.

**Jordan**: The exam has five domains. First is Platform Architecture and Infrastructure at 15%. That covers networking, storage, compute best practices, cost management, and multi-tenancy patterns.

**Alex**: Second is GitOps and Continuous Delivery at 25%. That's the biggest domain tied with Platform APIs. We're talking GitOps workflows, CI/CD pipelines integrated with Kubernetes, progressive delivery strategies like blue-green and canary deployments.

**Jordan**: Third is Platform APIs and Self-Service Capabilities, also at 25%. This is where you need to know Custom Resource Definitions, Kubernetes Operators, self-service provisioning, and automation frameworks.

**Alex**: Fourth is Observability and Operations at 20%. Monitoring, metrics, logging, tracing across the entire platform. Not just knowing what OpenTelemetry is, but actually implementing it.

**Jordan**: And fifth is Security and Policy Enforcement at 15%. Security posture management, policy engines like Kyverno and OPA, compliance requirements. So you're looking at tools like ArgoCD, Flux, Backstage, Crossplane, OpenTelemetry, Kyverno. You need hands-on experience with all of these.

**Alex**: Here's where it gets real. This is a performance-based exam. 120 minutes, hands-on tasks in realistic environments. You're not answering multiple choice questions about what ArgoCD does. You're actually implementing GitOps workflows under time pressure.

**Jordan**: And that's why beta testers struggled. One experienced community member estimated they scored 29% and chose not to even complete the exam. CNCF's response was essentially, "Recognition is meaningful when exams are challenging."

**Alex**: Which is fair, honestly. The CKA is challenging. The CKS is harder. But CNPE requires breadth that neither of those has. And here's the kicker: there's no exam simulator available yet. Killer.sh won't have CNPE prep until Q1 2026.

**Jordan**: So anyone taking the exam now is flying without a safety net. No practice environment, limited study materials because the certification just launched. That said, CNCF does include two exam attempts with registration, so you get a second chance.

**Alex**: Let's talk career impact because the numbers are compelling. Platform engineers average $219,000 in the US, about $100,000 in Europe. That's 20% higher than DevOps engineers at $153,000. 16% higher than ML engineers. 14% higher than software engineers. Even 2% higher than SREs.

**Jordan**: The market demand is there too. Platform engineer is the second most popular Kubernetes role at 11.47% of job postings, actually ahead of DevOps at 9.56%. And the target roles for CNPE holders are Principal Platform Engineer, Platform Architect, Senior DevOps Lead, Engineering Manager.

**Alex**: So CNPE positions you for leadership roles, not just individual contributor positions. But here's the question everyone's asking: should you get CNPA first or go straight to CNPE?

**Jordan**: Great question. CNPA is the associate level certification. $250, multiple choice, 120 minutes. It tests conceptual understanding across platform fundamentals, observability, security, CI/CD, platform APIs. Think of it as proving you understand the concepts without having to implement them hands-on.

**Alex**: CNPE is the engineer level. Performance-based, hands-on tasks, realistic environments. It builds on CNPA knowledge but tests practical implementation. There's no formal prerequisite, you don't have to pass CNPA first, but the natural progression is CNPA then CNPE.

**Jordan**: My recommendation: if you're transitioning into platform engineering or have less than two years of platform-specific experience, start with CNPA. Study materials exist, the exam format is more forgiving, and you can build confidence before tackling the hands-on exam.

**Alex**: If you're already a senior platform engineer with real-world experience building IDPs, implementing GitOps, creating platform APIs, you might be ready to attempt CNPE directly. But honestly? Even experienced folks might want to wait for the Killer.sh simulator in Q1 2026.

**Jordan**: Let's talk about where CNPE fits in the broader certification ecosystem. CNCF has the Kubestronaut program which requires five certifications: KCNA, KCSA, CKA, CKAD, and CKS. There are over 2,500 Kubestronauts across more than 100 countries.

**Alex**: And now there's Golden Kubestronaut. That requires all 15 CNCF certifications plus LFCS. Here's the important update: starting March 1st, 2026, CNPE will be required for Golden Kubestronaut status. So if you're chasing that credential, CNPE is now mandatory.

**Jordan**: For platform engineers specifically, I see three certification paths. Path A is traditional: CKA, then CKS, then CNPA, then CNPE. You build up Kubernetes expertise before adding platform engineering specialization.

**Alex**: Path B is the fast track: CNPA then CNPE. This works if you already have hands-on experience and don't need the Kubernetes foundations.

**Jordan**: Path C is full coverage: complete Kubestronaut first, then add CNPE to become eligible for Golden Kubestronaut.

**Alex**: There are also complementary certifications worth considering. CGOA for GitOps with ArgoCD, CBA for Backstage administration, OTCA for OpenTelemetry. These pair well with CNPE to demonstrate comprehensive platform expertise.

**Jordan**: Alright, let's talk preparation strategy because people are going to ask how to study for this thing. Current limitations are real: no Killer.sh simulator until Q1 2026, limited study materials since the exam just launched.

**Alex**: So what can you do now? First, if you haven't already, start with CNPA. The study materials exist, KodeKloud has a course, and passing CNPA will give you a foundation and confidence.

**Jordan**: Second, hands-on practice is critical. Build an Internal Developer Platform in your own cluster. Not just reading about Backstage, actually deploying it. Not just understanding Crossplane concepts, actually creating compositions.

**Alex**: Third, study the tools deeply. ArgoCD or Flux for GitOps. Crossplane for infrastructure APIs. Backstage for developer portals. OpenTelemetry for observability. Kyverno or OPA for policy. These aren't optional.

**Jordan**: Fourth, GitOps specifically deserves extra attention. It's 25% of the exam. Implement progressive delivery patterns. Set up blue-green deployments. Configure canary releases. Understand how to roll back when something goes wrong.

**Alex**: Fifth, build platform APIs. Practice creating Custom Resource Definitions. Write Kubernetes Operators. Create self-service workflows that developers would actually use. The exam tests implementation, not just architecture.

**Jordan**: For study resources, KodeKloud has CNPA courses. Linux Foundation has official training. The CNCF project documentation for each tool is essential. And the platform engineering community has resources, though they're still developing.

**Alex**: Let's bring this back to decision-making. Who should pursue CNPE and when?

**Jordan**: If you're already a senior platform engineer and your daily job involves building IDPs, implementing GitOps, creating self-service capabilities, CNPE validates what you already do. Consider taking it once the simulator is available in Q1 2026.

**Alex**: If you're transitioning to platform engineering from DevOps, SRE, or software engineering, start with CNPA. Build the conceptual foundation. Get hands-on experience in a real environment. Then tackle CNPE when you've got practical skills to back it up.

**Jordan**: If you want maximum credential coverage and you're going for Golden Kubestronaut, plan your path now. You'll need CNPE after March 1st, 2026, so factor that into your timeline.

**Alex**: One more thing worth mentioning. The certification is valid for two years, consistent with other CNCF certifications. You get two attempts included with registration. And as the first-ever platform engineering credential, early adopters will stand out before the market saturates.

**Jordan**: That scarcity factor is real. When CKA first launched, passing it meant something because few people had it. The same dynamic applies to CNPE right now. Those 29% scores that beta testers reported? They mean early passers will have a genuinely differentiating credential.

**Alex**: So the bottom line: CNPE isn't just another certification to collect. It's CNCF formally recognizing platform engineering as a distinct discipline separate from DevOps, separate from SRE, with its own body of knowledge and practical skills.

**Jordan**: The difficulty is intentional. The breadth is intentional. And for those willing to invest in deep preparation across GitOps, platform APIs, observability, and security, it's a credential that demonstrates real capability, not just exam-taking skill.

**Alex**: Evaluate where you are in your career. Assess your hands-on experience with the five exam domains. Decide whether the investment makes sense now while materials are limited, or after Q1 2026 when the simulator is available and more study resources exist.

**Jordan**: Either way, platform engineering has its first official credential. After years of debate about what platform engineering actually means, CNCF has answered with a hands-on exam that tests whether you can actually build and operate a platform. That's a significant milestone for the discipline.

**Alex**: And for our audience of senior platform engineers and SREs, this is worth paying attention to. Whether you pursue the certification or not, understanding what CNPE tests tells you what the industry considers core platform engineering competencies. That's valuable career intelligence regardless of whether you ever sit for the exam.

---

## Resources

### CNCF Certification Pages
- [CNPE Certification](https://training.linuxfoundation.org/certification/certified-cloud-native-platform-engineer-cnpe/)
- [CNPA Certification](https://training.linuxfoundation.org/certification/certified-cloud-native-platform-engineering-associate-cnpa/)
- [Kubestronaut Program](https://www.cncf.io/training/kubestronaut/)
- [CNCF Certification Catalog](https://www.cncf.io/training/certification/)

### Platform Engineering Tools to Study
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Flux Documentation](https://fluxcd.io/docs/)
- [Backstage Documentation](https://backstage.io/docs)
- [Crossplane Documentation](https://docs.crossplane.io/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Kyverno Documentation](https://kyverno.io/docs/)

### Study Resources
- [KodeKloud CNPA Course](https://kodekloud.com/)
- [Linux Foundation Training](https://training.linuxfoundation.org/)

---

## Related Episodes

- [Episode #011: Why 70% of Platform Teams Fail](/podcasts/00011-platform-failures) - The critical PM gap and predictive metrics
- [Episode #040: Platform Engineering Anti-Patterns](/podcasts/00040-platform-engineering-anti-patterns) - 10 patterns that kill developer productivity
