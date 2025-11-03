---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #013: Backstage Adoption"
slug: 00013-backstage-adoption
---

# Backstage in Production: The 10% Adoption Problem

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 16 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/backstage-production-10-percent-adoption-problem)**: Comprehensive analysis with cost calculators, comparison tables, and complete decision frameworks for choosing Backstage vs alternatives.

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, margin: '1.5rem 0'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/psby7csy8Wg"
    title="Backstage in Production: The 10% Adoption Problem"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>

---

**Jordan**: Welcome back to the Platform Engineering Playbook podcast. I'm Jordan.

**Alex**: And I'm Alex. Today we're tackling a topic that's causing anxiety in platform engineering teams everywhere: Backstage adoption.

**Jordan**: Specifically, the ten percent problem.

**Alex**: Right. Your team spends nine months implementing Backstage. The portal looks beautiful. You have forty-seven services cataloged. And internal adoption? Eight percent. Three developers use it regularly.

**Jordan**: That's painful. And apparently it's not uncommon?

**Alex**: It's actually documented. Spotify's VP of Engineering has publicly acknowledged that while Backstage adoption is high internally at Spotify, it often stalls at less than ten percent in other organizations.

**Jordan**: So this isn't just anecdotal complaining on HackerNews. This is a real, acknowledged problem.

**Alex**: Exactly. And what's interesting is that the 2025 Gartner Market Guide for Internal Developer Portals specifically calls out that the market now favors IDPs that deliver immediate value and faster ROI. Backstage implementations that can't prove value quickly are facing existential threats.

**Jordan**: Let's talk about cost first, because I think people underestimate what Backstage actually requires. What's the real investment?

**Alex**: For a mid-size organization with three hundred developers, year one costs about one point zero five million dollars. That's seven FTEs: one PM, two frontend engineers, two full-stack engineers, two DevOps engineers, all at around one hundred fifty thousand dollars per year.

**Jordan**: And that's just year one.

**Alex**: Year two and ongoing, you're looking at nine hundred thousand dollars per year. Four FTEs for development, two FTEs for maintenance and platform management.

**Jordan**: So organizations that think they can get positive ROI from Backstage with just one or two engineers—

**Alex**: Have unrealistic expectations. At Spotify with sixteen hundred engineers, there was a full-time team of four engineers working on their IDP. For an organization with three hundred developers, you need between seven and fifteen engineers to extract value from Backstage.

**Jordan**: Why does it require so much investment?

**Alex**: Technical complexity. Backstage isn't a product—it's a framework that requires product development. You've got seventy plus steps to basic setup, over one hundred plugins to evaluate, React plus Node plus TypeScript required. Most backend engineers don't have those skills.

**Jordan**: So your platform team becomes a bottleneck.

**Alex**: Exactly. And then there's the data quality death spiral. Backstage never fully addressed the fundamental challenge of trusted, always-up-to-date data. The catalog's data can quickly become stale and untrustworthy. Engineers don't trust stale data, so they don't update the catalog, data gets staler, adoption drops further, and leadership questions the investment.

**Jordan**: That's a vicious cycle. What about the plugin ecosystem? Isn't that supposed to be a strength?

**Alex**: It's actually a problem. Too much extensibility becomes overwhelming. Which plugins should we use? How do we configure authentication? What's the right deployment architecture? Teams get stuck in proof-of-concept limbo.

**Jordan**: So when should an organization actually use Backstage?

**Alex**: You need to meet all of these criteria. Five hundred plus engineers minimum. Strong React and TypeScript skills. Seven to fifteen dedicated FTEs. Service catalog discipline already exists—Backstage won't create discipline, it requires it. A three to five year investment timeline. And unique customization needs where Backstage's flexibility actually pays off.

**Jordan**: That's a pretty narrow window.

**Alex**: It is. If you have fewer than five hundred engineers, limited frontend skills, need fast time-to-value in under six months, can't dedicate seven plus FTEs, or don't have an existing service catalog, you should probably choose alternatives.

**Jordan**: Let's talk about those alternatives. What's out there?

**Alex**: Port dot I O, Cortex, and custom portals are the main ones. Port is interesting—implementation is about four times faster than Backstage on average. You can get to meaningful adoption in one to three months with just half an FTE to one FTE. Annual cost is fifty thousand to two hundred thousand dollars versus Backstage's nine hundred thousand plus.

**Jordan**: That's a massive difference.

**Alex**: The tradeoff is customization. Port has limited customization through a UI builder, but it's no-code. You don't need React or TypeScript skills. It's a "bring your own data model" approach—fully flexible but without the complexity.

**Jordan**: What about Cortex?

**Alex**: Cortex is in the middle. Two to four months time-to-value, one to two FTEs required, forty thousand to one hundred fifty thousand dollars annual cost. It's more focused on service catalog and maturity tracking. Semi-rigid data model—some entities are fixed and can't be changed. Good fit for two hundred to one thousand engineers who want less flexibility than Port but more structure than a custom build.

**Jordan**: And custom portals?

**Alex**: Three to six months, two to five FTEs, three hundred thousand to seven hundred fifty thousand dollars per year. You get full control over your stack and dependencies, perfect for unique needs or when you already have internal tools. The tradeoff is you're building everything from scratch.

**Jordan**: What about adoption rates? Are these alternatives actually better?

**Alex**: Yes. Backstage averages ten percent adoption—that's the problem we're discussing. Port typically sees forty to sixty percent adoption. Cortex thirty to fifty percent. Custom portals vary from thirty to seventy percent depending on how well they're built.

**Jordan**: So the alternatives not only cost less and require fewer people, they also get better adoption?

**Alex**: In most cases, yes. Because they're purpose-built for the problem, not frameworks requiring assembly. The faster time-to-value means teams can iterate and respond to feedback quickly.

**Jordan**: Let's say someone's already committed to Backstage. What should they do?

**Alex**: Radically simplify. Start with software catalog only—no TechDocs initially, no Scaffolder, no fancy plugins. Just the catalog. Use managed Backstage like Roadie to reduce ops burden. Limit to five critical plugins maximum: GitHub integration, Kubernetes visibility, PagerDuty, Datadog, that's it. Dedicate four to seven FTE minimum. And accept a twelve to eighteen month timeline to thirty percent adoption.

**Jordan**: Thirty percent, not ten percent.

**Alex**: Right. If you're aiming for ten percent, you're accepting failure. Thirty percent should be your success metric. Along with under five second page load time, ninety-nine point nine percent uptime, and under two percent stale catalog data.

**Jordan**: You mentioned Roadie, the managed Backstage option. How does that help?

**Alex**: Roadie handles upgrades, security patches, infrastructure. It costs around fifty thousand to one hundred fifty thousand dollars per year, but it saves you two to four FTEs. So instead of seven to fifteen FTEs for self-hosted Backstage, you might need four to seven FTEs with Roadie.

**Jordan**: Still significant but better.

**Alex**: Exactly. You're trading money for reduced complexity. For teams that are committed to Backstage but don't have the ops capacity, it's the right move.

**Jordan**: What if a team is stuck at ten percent adoption? What should they do?

**Alex**: Set a six-month deadline. Audit what's working—which teams use it and why. Simplify radically—cut plugins to five max. Fix data quality—make the catalog trustworthy. Add exec-level metrics to get leadership buy-in. If you miss that deadline for thirty percent adoption, switch to an alternative.

**Jordan**: Don't fall for sunk cost fallacy.

**Alex**: Exactly. Nine months invested doesn't mean you should invest nine more. Sometimes the best decision is to pivot.

**Jordan**: What about teams that are evaluating options right now? What should they do?

**Alex**: Run parallel proof of concepts. Week one and two, deploy Port with one team. Week three and four, deploy Cortex with another team. Week five and six, build a custom MVP with a third team. Week seven and eight, evaluate adoption, developer feedback, and cost. Whatever gets you to thirty percent adoption fastest wins.

**Jordan**: Let me play devil's advocate. Backstage has twenty-eight thousand GitHub stars, it's CNCF Incubating, it has massive mindshare. Why not just use it?

**Alex**: Mindshare doesn't equal adoption. GitHub stars don't equal business value. Backstage is an incredible achievement—Spotify built something powerful and open-sourced it. But it's optimized for Spotify's scale and Spotify's engineering culture. Most organizations aren't Spotify.

**Jordan**: And trying to be Spotify when you're not Spotify is a recipe for failure.

**Alex**: Precisely. The honest questions every organization needs to ask: Do we have seven to fifteen FTE available for eighteen to twenty-four months? Does our engineering team have strong React and TypeScript skills? Does our service catalog already exist with ownership discipline? Do we have executive sponsorship and multi-year commitment? Can we accept an eighteen to twenty-four month timeline to thirty percent adoption? If any answer is no, Backstage is the wrong choice.

**Jordan**: What about breaking changes? I've heard Backstage has frequent breaking changes.

**Alex**: Major version every six to twelve months. That's part of why you need dedicated FTEs—someone has to manage those upgrades. Commercial alternatives like Port and Cortex are managed services, so breaking changes are their problem, not yours.

**Jordan**: That's a hidden cost people don't think about.

**Alex**: Absolutely. It's not just building Backstage, it's maintaining Backstage through constant evolution. The React and Node ecosystems move fast. Backstage moves fast. You need teams that can keep up.

**Jordan**: Let's talk about some real examples. You mentioned a success story—five hundred person company, five FTE team, eighteen month timeline, fifty percent adoption. What made that work?

**Alex**: Dedicated team with clear ownership, simplified scope—they focused on five core use cases instead of trying to do everything, executive sponsorship from the VP of Engineering which gave them political cover during the long timeline, managed Backstage through Roadie which reduced ops burden, and realistic expectations from day one. They weren't aiming for one hundred percent adoption in six months.

**Jordan**: And the failure story?

**Alex**: One hundred fifty person company, two FTE team, twelve month timeline, self-hosted Backstage, attempted twenty plus plugin integrations, no executive sponsorship. Result: eight percent adoption after twelve months, twelve plus second page load times, ninety-five percent uptime with frequent issues, fifteen percent stale catalog data. They abandoned it for Port.

**Jordan**: What was the key lesson from that failure?

**Alex**: Team too small, scope too large, no exec buy-in. They were set up to fail from the start. Two FTEs can't maintain production Backstage while also building new features and handling support requests.

**Jordan**: It's interesting that the alternatives like Port and Cortex can work with half an FTE to two FTEs, but Backstage needs seven to fifteen.

**Alex**: That's the framework versus product distinction. Port and Cortex are products—they work out of the box. Backstage is a framework—you have to build the product using the framework. Fundamentally different value propositions.

**Jordan**: So the decision really comes down to: do you want to build a developer portal, or do you want to buy a developer portal?

**Alex**: That's a great way to frame it. If you want to build—you have the team, the skills, the timeline, the budget—Backstage gives you incredible flexibility. If you want to buy—you need value fast, you have limited resources, you want someone else to handle maintenance—go with Port or Cortex.

**Jordan**: And custom portals are for organizations that already have internal tools and want full control.

**Alex**: Right. If you already have an internal tools platform, adding a developer portal might be straightforward. You know your systems, you control the stack, you can move fast. But you're starting from zero in terms of features.

**Jordan**: Final question: three years from now, what does the developer portal landscape look like?

**Alex**: I think we'll see consolidation. Port, Cortex, and a few others will dominate the commercial space. Backstage will still exist but primarily at very large organizations—the Spotifys, the Netflixes, the companies with hundreds of engineers who can dedicate large teams. And we'll see more custom solutions using modern frameworks that are easier to build with than React and TypeScript.

**Jordan**: The barrier to entry for custom solutions is dropping.

**Alex**: Exactly. With tools like Next.js, Remix, and serverless architectures, building a simple internal portal is much easier than it was five years ago. You might not need Backstage's complexity, and you might not want to pay for a commercial solution. A small team can build something fit-for-purpose in a reasonable timeline.

**Jordan**: So the message is: be honest about what you need, be honest about what you have, and choose the path that gets you to meaningful adoption fastest.

**Alex**: That's it. The goal isn't to use Backstage. The goal is developer portal adoption. Whatever path gets you there is the right path.

**Jordan**: Great discussion. Where can people learn more?

**Alex**: The full blog post with all the data, comparison tables, and decision frameworks is on platformengineeringplaybook.com. We've got cost calculators, case studies, and links to all the alternatives we discussed.

**Jordan**: And if you're struggling with Backstage adoption right now, you're not alone. The ten percent problem is real, it's documented, and there are solutions.

**Alex**: Thanks for listening to the Platform Engineering Playbook podcast.

**Jordan**: We'll see you next time.
