---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #038: Giving Thanks to Your Dependencies"
slug: 00038-thanksgiving-oss-gratitude
---

# Giving Thanks to Your Dependencies: A Platform Engineer's Gratitude Guide

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 9 minutes
**Speakers:** Jordan and Alex
**Target Audience:** Platform engineers, developers, engineering leadership wanting to support open source maintainers

> 📝 **Callback to [Episode #037](/podcasts/00037-kubecon-2025-community-sustainability)**: This episode follows our KubeCon Community Sustainability discussion with practical actions you can take today.

:::info Thanksgiving Special Episode

This special Thanksgiving episode explores the tools and practices for thanking the maintainers behind your dependencies. 60% of maintainers are unpaid. 60% have considered leaving. Here's what you can do about it.

:::

<div style={{maxWidth: '640px', margin: '2rem auto'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/vk-54qqZql0"
      title="Giving Thanks to Your Dependencies: A Platform Engineer's Gratitude Guide"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

---

**Jordan**: This Thanksgiving, let's talk about the people you've never thanked. Run npm list on any project right now. How many packages? For most Node.js applications, it's somewhere between one hundred and five hundred dependencies. Sometimes more. Each one maintained by someone. Who are they?

**Alex**: Here's the uncomfortable truth. Sixty percent of open source maintainers are unpaid for their work. That's according to the twenty twenty-four Tidelift State of the Open Source Maintainer Report. And sixty percent have either left or considered leaving their projects. Not because of code problems. Because of burnout, loss of interest, competing life demands.

**Jordan**: We talked about this in our last episode on community sustainability. The XZ Utils backdoor showed us what happens when isolated maintainers crack under pressure. A sixty-six percent drop in maintainer trust toward new contributors. But here's what we didn't cover. There's an entire ecosystem of tools designed to help you thank the maintainers you depend on. And most developers have never heard of them.

**Alex**: So today, we're going on a gratitude discovery mission. We'll show you tools across different languages, talk about what meaningful thanks actually looks like, and give you a Thanksgiving challenge you can complete in five minutes.

**Jordan**: Let's start with the Node.js ecosystem. There's a tool called "thanks" that you can run right now with npx. Just type npx thanks in any project directory with a package dot json. It scans your dependencies and shows you which maintainers are seeking donations.

**Alex**: The creator of this tool, Feross Aboukhadijeh, built it with a simple philosophy. Quote, "Put your money where your love is." The project has twenty-eight hundred stars on GitHub and eighty-five contributors. When you run it, you see a list of packages you depend on, organized by whether the maintainer has a funding mechanism set up.

**Jordan**: And since npm version six point thirteen, there's also npm fund built right in. Run npm fund in your project and it lists the funding URLs for your entire dependency tree. It was a collaboration between npm and Open Collective to make supporting maintainers frictionless.

**Alex**: The Rust ecosystem has its own approach. There's cargo-thanks, which does something interesting. Instead of showing funding links, it stars the GitHub repositories of your dependencies. The creator was inspired by Medium's clapping button. One command, and you've shown appreciation to everyone you depend on.

**Jordan**: There's also thanks-stars, a more modern tool with multi-ecosystem support. It detects dependencies from Cargo dot toml, package dot json, go dot mod, and automatically stars repos on your behalf. And cargo-thanku generates acknowledgment documentation for your projects.

**Alex**: But here's where it gets interesting. Beyond stars and funding, there are more personal ways to say thanks. Have you heard of Happiness Packets?

**Jordan**: It's a platform launched in twenty sixteen that lets you send anonymous thank-you notes to developers. You write what their work meant to you, and they receive it without any obligation to respond. The creators, Sasha Romijn and Mikey Ariel, have sent hundreds of these packets to developers around the world.

**Alex**: Here's what most people don't realize. Maintainers have almost zero visibility into how their projects are actually used. One of the most valuable things you can do is send an email explaining your specific use case. Not just "thanks for the great library." But "We use your project at our company to process three million requests per day. It's been rock solid for two years."

**Jordan**: That specificity matters. One developer shared this on Hacker News. Quote, "Whenever I find a blog post or video particularly useful, the first thing I do is whip up my mail client and thank the authors. I never realized how much of a positive impact this has on creators until people started mailing me thanking me for my work. Brightens up your day really."

**Alex**: But we need to acknowledge the nuance here. Not all maintainers feel the same way about thank-you messages. One maintainer said, quote, "Honestly, being thanked in any shape or form does nothing for me. I'd rather have users be more considerate of our time and not abuse issues and the community for supporting their laziness."

**Jordan**: That's a valid perspective. The best gratitude combines words with action. A good bug report with a minimal reproduction is worth a hundred thank-you messages. A documentation PR fixing unclear instructions? That's meaningful. Contributing to the project in ways that reduce the maintainer's burden? That's gratitude in action.

**Alex**: So let's talk about company-level actions. Because individual thanks is good, but organizational investment is transformative.

**Jordan**: The Open Source Pledge is a commitment for companies to pay maintainers directly. The minimum is two thousand dollars per year per developer at your company. Cash payments. Not cloud credits. Not hiring developers to work on other things. Cash to the people doing the work.

**Alex**: And companies are actually doing this. Antithesis contributed one hundred ten thousand dollars. That's two thousand eight hundred ninety-five per developer on staff. Ninety-five thousand of that went to the Nix core team alone. Convex put in one hundred thousand, which works out to seven thousand six hundred ninety-two per developer.

**Jordan**: GitHub has invested heavily too. In twenty twenty-four, they put an additional five hundred thousand dollars into maintainer sponsorships, distributing it across over nine hundred maintainers. May is officially Maintainer Month, a time to recognize the people who build, fix, review, and secure the code the world relies on.

**Alex**: ScyllaDB has a tradition of thanking open source contributors every Thanksgiving. They specifically call out the tools and frameworks their engineers rely on. It's a cultural practice that acknowledges the invisible infrastructure behind their product.

**Jordan**: So here's your Thanksgiving challenge. Five minutes or less.

**Alex**: Step one. Run npx thanks or npm fund in one of your projects right now. See who's seeking support.

**Jordan**: Step two. Pick one dependency you rely on heavily. Something you use every day and never think about.

**Alex**: Step three. Send a thank-you email to the maintainer. Explain how you use their project. Be specific. Give them that visibility they almost never get.

**Jordan**: Step four. Consider a small donation. Five dollars. Ten dollars. Whatever's comfortable. GitHub Sponsors makes this easy. Look for the sponsor button on any repository.

**Alex**: And step five. Star the repos. It takes two seconds and shows up in the maintainer's dashboard. It's a tiny signal that someone cares.

**Jordan**: If you listened to our last episode on community sustainability, you heard the statistics. You heard about Han Kang's passing and what it meant for Kubernetes reliability. You heard about the burnout crisis. This episode is the answer to the question: what can YOU do about it?

**Alex**: The code doesn't exist without the people who write it. This Thanksgiving, those people deserve a seat at your table. A thank-you email. A five dollar donation. A starred repository. Small gestures that say: I see you, I appreciate you, your work matters.

**Jordan**: Until next time.
