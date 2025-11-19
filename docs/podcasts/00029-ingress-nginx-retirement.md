---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #029: Ingress NGINX Retirement"
slug: 00029-ingress-nginx-retirement
---

# Ingress NGINX Retirement: The March 2026 Migration Deadline

## The Platform Engineering Playbook Podcast

import GitHubButtons from '@site/src/components/GitHubButtons';

<GitHubButtons />

**Duration:** 13 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/ingress-nginx-retirement-gateway-api-migration-2026)**: Complete Gateway API migration guide with controller comparison tables, step-by-step implementation, and 3-month migration timeline.

---

**Jordan:** Today we need to talk about something urgent. On November eleventh, Kubernetes SIG Network dropped a bombshell that affects nearly every production cluster out there.

**Alex:** Ingress NGINX is being retired. March twenty twenty-six. After that date—no releases, no bugfixes, no security patches.

**Jordan:** And this isn't some obscure component. This is the de facto standard ingress controller. If you're running Kubernetes with internet-facing services, you're probably running Ingress NGINX.

**Alex:** So we've got about four months to migrate. That's not a lot of time for something handling all your external traffic routing.

**Jordan:** Let's unpack what's actually happening here, because the story behind this retirement is almost as important as the migration itself.

**Alex:** Yeah, this didn't come out of nowhere. The announcement from SIG Network and the Security Response Committee reveals something systemic.

**Jordan:** Wait, the Security Response Committee is involved? That's not a good sign.

**Alex:** It's not. And here's the part that surprised me—for years, Ingress NGINX has had only one or two people doing development work. On their own time. After work hours. Weekends.

**Jordan:** One or two maintainers for what's arguably the most critical traffic component in most Kubernetes deployments?

**Alex:** That's the unsustainable open source reality. The announcement says SIG Network and the Security Response Committee exhausted their efforts to find additional support. They couldn't find people to help maintain it.

**Jordan:** Didn't they announce a replacement project last year? InGate or something?

**Alex:** They did. The maintainers announced plans to wind down Ingress NGINX and develop InGate as a replacement, together with the Gateway API community. But even that announcement failed to generate help.

**Jordan:** So InGate never got off the ground?

**Alex:** Never progressed far enough to be a viable replacement. It's also being retired. The whole thing just... didn't work.

**Jordan:** That's genuinely concerning. So what happens after March twenty twenty-six?

**Alex:** Your existing deployments keep running. The installation artifacts stay available. But no new releases. No bugfixes. And critically—no security patches.

**Jordan:** And NGINX, the underlying proxy, gets CVEs fairly regularly.

**Alex:** Exactly. So if a vulnerability is discovered after March twenty twenty-six, it stays unpatched. Forever. And we're talking about your internet-facing edge router here. That's a prime attack target.

**Jordan:** CVE twenty twenty-five dash one nine seven four was already a wake-up call on that front.

**Alex:** Right, it demonstrated the pattern. And here's the thing—even your dev and staging environments become risk vectors. They often contain sensitive data or provide paths into production.

**Jordan:** So "we'll just keep running it" isn't really an option for any serious production environment.

**Alex:** Not if you care about security posture. The announcement explicitly recommends migrating to Gateway API or another ingress controller immediately.

**Jordan:** Okay, let's talk options. What are platform teams actually choosing?

**Alex:** The main paths are Gateway API, which is the recommended strategic choice, or alternative ingress controllers if you want something more familiar.

**Jordan:** Let's start with Gateway API since that's the official recommendation.

**Alex:** So Gateway API isn't just "Ingress version two." It's a complete redesign of how Kubernetes handles traffic routing. Different philosophy, different resource model.

**Jordan:** What's actually different about it?

**Alex:** A few fundamental things. First, it's protocol-agnostic. Ingress only really handled HTTP and HTTPS well. Everything else—gRPC, TCP, UDP—required vendor-specific annotations or workarounds.

**Jordan:** The annotation sprawl problem.

**Alex:** Exactly. Gateway API has native support for HTTP, gRPC, TCP, UDP. No annotations needed for basic traffic types.

**Jordan:** What else?

**Alex:** Role-based resource model. Instead of one Ingress resource doing everything, you have Gateway resources that infrastructure teams manage, and Route resources—HTTPRoute, GRPCRoute, TCPRoute—that application teams manage.

**Jordan:** So there's a cleaner separation of concerns.

**Alex:** Right. And it has built-in support for things like traffic splitting, canary deployments, blue-green deployments. Stuff that required controller-specific annotations in Ingress.

**Jordan:** Who's actually implementing Gateway API? Which controllers support it?

**Alex:** Multiple mature implementations now. Envoy Gateway, which is the reference implementation. Cilium's Gateway API support. Kong Gateway. Traefik. And interestingly, NGINX Gateway Fabric—that's NGINX's own Gateway API implementation.

**Jordan:** So you could stay in the NGINX ecosystem but move to Gateway API.

**Alex:** You could. Though if you're migrating anyway, the question becomes—do you want to go to a strategic destination, or just a halfway point?

**Jordan:** What do you mean?

**Alex:** Gateway API's big advantage is portability. The spec is standardized. If you're using HTTPRoute resources with Envoy Gateway today, you can switch to Cilium's implementation tomorrow without rewriting your configs.

**Jordan:** Unlike Ingress where you'd have controller-specific annotations everywhere.

**Alex:** Exactly. The annotation sprawl meant you were locked to your controller. Gateway API solves that by putting capabilities in the spec instead of annotations.

**Jordan:** Okay, so what about teams that don't want to make the Gateway API leap? What are the alternatives?

**Alex:** NGINX Gateway Fabric is the closest to what people know. Similar mental model. Kong Gateway if you need enterprise support and a lot of features. Traefik is popular, good Kubernetes integration. Cilium if you want the eBPF-based approach.

**Jordan:** Let's be real though—what makes migration actually hard? Because I'm guessing it's not as simple as running a conversion tool.

**Alex:** It's not. There's a tool called ingress2gateway that helps scaffold the migration. But it's a scaffold, not a complete solution.

**Jordan:** What breaks?

**Alex:** Annotations. Ingress NGINX allowed massive customization through annotations and snippets. Custom header manipulation, rate limiting, specific NGINX directives. Gateway API is stricter by design.

**Jordan:** So all those custom snippets teams have accumulated over the years...

**Alex:** Need to be translated. And they don't map one-to-one. Some capabilities require different approaches in Gateway API. Some might need custom policies or filters depending on your controller.

**Jordan:** What about regex behavior?

**Alex:** Different. NGINX regex versus Gateway API's stricter matching. You need to validate that your routing rules actually match the same traffic.

**Jordan:** SSL termination?

**Alex:** Needs explicit validation. Same with header propagation. The semantics are similar but not identical, so you have to test.

**Jordan:** And presumably there's a DNS cutover at some point.

**Alex:** Which can cause disruption if not planned carefully. You want a parallel running period where both Ingress and Gateway are active, gradually shifting traffic.

**Jordan:** Alright, let's give people a framework. How should teams actually approach this?

**Alex:** I'd break it into four phases over roughly four months, with some buffer before March.

**Jordan:** Phase one?

**Alex:** Assessment. Weeks one and two. Inventory all your Ingress resources across all clusters. Document every custom annotation and snippet. Identify your highest-risk services—internet-facing, business-critical. And choose your target controller.

**Jordan:** What factors for choosing the controller?

**Alex:** If you want maximum strategic investment and portability—Envoy Gateway or Cilium Gateway API. If you want minimal mental model change—NGINX Gateway Fabric. If you need enterprise support contracts—Kong or Traefik Enterprise.

**Jordan:** Phase two?

**Alex:** Pilot. Weeks three and four. Deploy your chosen Gateway API controller on non-production. Migrate one simple service using ingress2gateway as a starting point. Then manually translate your complex annotations. Validate SSL, headers, routing behavior.

**Jordan:** Simple service first makes sense. Don't start with your most complex routing.

**Alex:** Right. Get comfortable with the resource model, understand the gaps, then tackle the hard stuff.

**Jordan:** Phase three?

**Alex:** Staging migration. Month two. Migrate your entire staging environment. Run parallel Ingress and Gateway for validation. Performance and load testing. And critically—develop your runbooks for production.

**Jordan:** Because you want the team comfortable with troubleshooting before it matters.

**Alex:** Exactly. You want people who've seen the failure modes before they're handling them at two AM.

**Jordan:** And phase four is production.

**Alex:** Month three. Start with lowest-risk production services. Gradual traffic shift—ten percent, then fifty, then one hundred. Keep Ingress as a fallback during the transition. Monitor for routing anomalies. Then once you're confident, month four—cleanup. Remove the old Ingress controllers, archive the manifests, update documentation.

**Jordan:** That puts you done before March with some buffer.

**Alex:** Which you need, because something will take longer than expected. It always does.

**Jordan:** What should people do this week? Like, immediately?

**Alex:** Three things. First, read the official announcement. It's at kubernetes dot io slash blog, November eleventh. Understand what's actually happening and the timeline.

**Jordan:** Second?

**Alex:** Run kubectl get ingress dash capital A. See how many Ingress resources you actually have across all namespaces. That's your scope.

**Jordan:** And third?

**Alex:** Document your most complex Ingress resources. The ones with lots of annotations, custom snippets, regex routing. Those are your migration risks.

**Jordan:** I want to reframe this a bit. Because yes, this is urgent and yes, it's work. But there's an upside here.

**Alex:** Gateway API is genuinely better. This isn't replacing something good with something equivalent. The resource model is cleaner. The portability is real. The built-in capabilities for traffic management are more sophisticated.

**Jordan:** So you're not just replacing a deprecated controller.

**Alex:** You're upgrading your entire traffic management story. The annotation sprawl problem goes away. The controller lock-in goes away. You get a more sustainable model backed by a real community and multiple implementations.

**Jordan:** The irony being that Ingress NGINX failed partly because the ecosystem couldn't sustain one controller, and Gateway API succeeds because it supports many.

**Alex:** Right. Instead of one project needing maintainers, you have multiple implementations competing and innovating on a standard spec.

**Jordan:** Practical takeaway?

**Alex:** Start your assessment this week. Four months isn't a lot of time for something this foundational. Get your inventory, pick your controller, start your pilot. Don't wait for January to realize you have two hundred complex Ingress resources to migrate.

**Jordan:** And the March deadline is real. No security patches after that means any CVE stays open forever.

**Alex:** Which for internet-facing infrastructure is an unacceptable risk profile. This isn't optional modernization—it's required security hygiene.

**Jordan:** Migration now, not later.

**Alex:** Exactly. The clock is ticking.
