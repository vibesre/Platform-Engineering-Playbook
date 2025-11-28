---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #039: Black Friday War Stories"
slug: 00039-black-friday-war-stories
---

# Black Friday War Stories: Lessons from E-Commerce's Worst Days

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 12 minutes
**Speakers:** Jordan and Alex
**Target Audience:** Platform engineers, SREs, DevOps engineers preparing for high-traffic events

> 📝 **Callback to [Episode #038](/podcasts/00038-thanksgiving-oss-gratitude)**: After thanking your dependencies, make sure they're ready for the traffic surge.

:::info Black Friday Special Episode

This Black Friday special dives into the graveyard of e-commerce outages—from J.Crew's $775,000 five-hour crash to the AWS typo that cost $150 million. Every incident reveals fundamental truths about distributed systems, human error, and why throwing money at the problem doesn't work.

:::

<div style={{maxWidth: '640px', margin: '2rem auto'}}>
  <div style={{position: 'relative', paddingBottom: '56.25%', height: 0}}>
    <iframe
      style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
      src="https://www.youtube.com/embed/1jJ10Uev9LY"
      title="Black Friday War Stories: Lessons from E-Commerce's Worst Days"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</div>

---

**Jordan**: Today we're diving into the graveyard of Black Friday outages. Every year, despite knowing exactly when Black Friday will happen, major retailers crash. 2018 saw Walmart, J Crew, Best Buy, Lowe's, and Ulta all go down. 2020 brought outages to 48 major brands. 2023 cost Harvey Norman an estimated 60% of online sales. And just last year, a Cloudflare outage froze 99.3% of Shopify stores. That's over 6 million domains.

**Alex**: The question that haunts every platform engineer is this. If you know the traffic is coming a year in advance, why can't you prepare? The answer reveals uncomfortable truths about distributed systems, human error, and why throwing money at the problem simply doesn't work.

**Jordan**: Let's start with the Hall of Fame crashes. J Crew, Black Friday 2018. Their site crashed periodically across five hours, showing customers a "Hang on a Sec" screen that became infamous on social media. 323,000 shoppers affected. $775,000 in lost sales. In a single afternoon.

**Alex**: But that wasn't even the biggest loss that weekend. Walmart's issues started on Wednesday, November 21st. The night before Thanksgiving. Various shoppers saw error pages when browsing Walmart.com at around 10 PM Eastern. 3.6 million shoppers affected. $9 million in lost sales. And Black Friday hadn't even started yet.

**Jordan**: Best Buy's 2014 crash is a masterclass in assumption failure. They took their site offline for about an hour after what they called "a concentrated spike in mobile traffic triggered issues." The infrastructure was optimized for desktop traffic. But mobile was 78% of their actual traffic.

**Alex**: That same pattern repeated at Fastly in 2023. They had a 52-minute global outage during Black Friday. Root cause? Infrastructure optimized for 60% mobile, but they got 78%. Same mistake, nine years later. Some lessons just don't stick.

**Jordan**: Target's Cyber Monday 2015 is a cautionary tale about success causing failure. They offered 15% off virtually everything. Traffic and order volumes exceeded their Thursday Black Friday event, which had been their biggest day ever for online sales. The site fluctuated between error messages and normal operations. They had to plead for patience on social media.

**Alex**: Now let's talk about two disasters that didn't happen on Black Friday but every platform engineer should know by heart. February 28th, 2017. 9:37 AM Pacific. A single AWS engineer executed what seemed like a routine maintenance command.

**Jordan**: Four hours and 17 minutes later, half the internet came back online. Netflix, Airbnb, Slack, Docker, Expedia, over 100,000 websites. All down because of one typo.

**Alex**: Here's what happened. An employee was investigating slow response times in the S3 billing system. Following internal procedures, they needed to remove some servers. They ran a console command. Unfortunately, one of the inputs was entered incorrectly. Instead of removing a few servers, they removed a critical subsystem entirely.

**Jordan**: The Wall Street Journal reported that S&P 500 companies lost $150 million. US financial services companies alone lost $160 million. And here's the kicker. AWS's own status dashboard was down. It relied on S3 infrastructure hosted in a single region.

**Alex**: Why did recovery take so long? Amazon explained that the subsystems hadn't been completely restarted for many years. The team wasn't accustomed to going through all the safety checks at full speed. Skills atrophy when you don't practice.

**Jordan**: The changes Amazon made afterward are instructive. Servers now get removed more slowly. Safeguards prevent reducing any subsystem below minimum required capacity. They audited other operational tools for similar risks. And they moved plans to break the network into smaller cells to the top of the priority queue.

**Alex**: The GitLab disaster happened just a month earlier. January 31st, 2017. GitLab.com went down hard. By the time the dust settled, they had lost 5,000 projects, 700 user accounts, and countless issues and comments.

**Jordan**: What happened? GitLab's secondary database couldn't sync changes fast enough due to increased load. An engineer decided to manually re-sync by deleting its contents. But they ran the command against the wrong server. The primary. 300 gigabytes of live production data. Gone.

**Alex**: Here's where it gets worse. They had five backup systems. Five. None of them were working. The standard backup procedure failed because it was using PostgreSQL 9.2, but GitLab was running PostgreSQL 9.6. The backup failures were silent because notification emails weren't properly signed and got rejected.

**Jordan**: The only thing that saved them? Six hours before the deletion, an engineer had taken a snapshot for testing. Completely by accident. That snapshot saved 18 additional hours of data. GitLab live-streamed their recovery to over 5,000 viewers on YouTube. Radical transparency in their worst moment.

**Alex**: The lessons from GitLab are worth repeating. If you don't regularly restore from backups, they might not work when you need them. GitLab assumed their backups worked. They didn't. Backups need explicit ownership. Before this incident, no single engineer was responsible for validating the backup system. Which meant no one did.

**Jordan**: There's a community collection of Kubernetes failure stories at k8s.af, maintained by Henning Jacobs from Zalando. It's a treasure trove of production incidents. CPU limits causing high latency. IP ceilings preventing autoscaling. Missing application logs. Killed pods. 502 errors. Slow deployments. Production outages.

**Alex**: One of the most important observations from the Zalando team, who've been running Kubernetes since 2016. Quote, "A Kubernetes API server outage should not affect running workloads, but it did." The theory of distributed systems and the practice often diverge dramatically.

**Jordan**: So why does this keep happening? Four fundamental problems. First, complexity growth. Retail sites have gotten more complex over time. More integrations, more third-party services, more potential points of failure. And mobile traffic exploded in ways no one predicted.

**Alex**: Second, the load testing gap. Bob Buffone, CTO at Yottaa, puts it bluntly. Quote, "If you have not load tested your site at five times normal traffic volumes, your site will probably fail." Most companies test at 2x. They get hit with 10x.

**Jordan**: Third, dependency chains. The Cloudflare outage in 2024 took out 99.3% of Shopify stores because they all depend on the same CDN. PayPal's 2015 issues meant 70% of users couldn't complete payments. Your resilience is limited by your least resilient dependency.

**Alex**: And fourth, the rarity problem. AWS hadn't restarted those subsystems in years. GitLab hadn't validated their backup restoration. Skills and systems that aren't exercised regularly fail when you need them most.

**Jordan**: So here's the platform engineer's playbook for surviving high-traffic events. Load test at 5 to 10x expected traffic. Not 2x. Not expected peak. Test the failure modes, not just success paths.

**Alex**: Implement multi-CDN and multi-cloud strategies. Never be at the mercy of a single provider. Cross-cloud failovers aren't optional anymore, they're table stakes.

**Jordan**: Test your restores monthly. Explicit ownership of backup validation. Alerts on silent failures. If you haven't restored from backup in the last 30 days, you don't have a backup. You have a hope.

**Alex**: Practice chaos regularly. Restart systems that "never need restarting." Run game days before peak traffic, not after incidents. Know your recovery time under actual pressure, not theoretical pressure.

**Jordan**: Design for mobile-first. 78% or more of your traffic is mobile now. If you're still optimizing for desktop and hoping mobile works, you're making the same mistake Best Buy made a decade ago.

**Alex**: And finally, safeguards on dangerous commands. Minimum capacity checks. Slow rollout of server removals. Confirmation prompts for destructive operations. The AWS typo wouldn't have caused a four-hour outage if there had been a safeguard preventing reduction below minimum capacity.

**Jordan**: The uncomfortable truth is this. These outages aren't caused by lack of budget or lack of talent. They're caused by complexity, assumptions, and the gap between "should work" and "actually tested."

**Alex**: Every one of these incidents could have been prevented by practices platform engineers know well. Test your restores. Load test beyond expectations. Own your dependencies. Practice failure before failure finds you.

**Jordan**: As we head into another Black Friday season, ask yourself this. When was the last time your team actually restored from backup? When did you last restart that system that "never needs restarting"? When did you load test at 10x?

**Alex**: The best time to find out your backups don't work is during a routine Tuesday drill. The worst time is when 323,000 shoppers are seeing "Hang on a Sec."

**Jordan**: Until next time.

---

## Key Takeaways

💡 **Load Test at 5-10x**: Most companies test at 2x expected traffic and get hit with 10x. Test failure modes, not just success paths.

💡 **Test Your Restores Monthly**: GitLab had 5 backup systems—none worked. If you haven't restored from backup in 30 days, you have a hope, not a backup.

💡 **Multi-CDN/Multi-Cloud is Table Stakes**: The 2024 Cloudflare outage took out 99.3% of Shopify stores. Never be at the mercy of a single provider.

💡 **Practice Chaos Regularly**: AWS hadn't restarted critical subsystems in years. Skills and systems that aren't exercised regularly fail when you need them most.

💡 **Design Mobile-First**: 78%+ of traffic is mobile. If you're optimizing for desktop and hoping mobile works, you're repeating Best Buy's 2014 mistake.

💡 **Safeguard Dangerous Commands**: The AWS typo wouldn't have caused a 4-hour outage with minimum capacity checks and slow rollout safeguards.

---

## Sources

### Black Friday Outages
- [Retail TouchPoints: 2018 BFCM Outages](https://www.retailtouchpoints.com/features/news-briefs/site-outages-plague-walmart-j-crew-lowe-s-best-buy-office-depot-during-black-friday-weekend)
- [Fast Company: 48 Retail Sites with Issues 2020](https://www.fastcompany.com/90580744/black-friday-and-cyber-monday-outages-angered-customers-on-these-48-retail-sites)
- [CBS News: Best Buy 2014 Crash](https://www.cbsnews.com/news/best-buys-site-crashes-at-the-worst-possible-time/)
- [TechCrunch: Target 2015 Outage](https://techcrunch.com/2015/11/30/target-com-latest-to-crash-from-increased-online-traffic/)
- [Kinsta: Black Friday Downtime Costs](https://kinsta.com/blog/black-friday-website-downtime/)

### AWS S3 Outage
- [NPR: The $150 Million Typo](https://www.npr.org/sections/thetwo-way/2017/03/03/518322734/amazon-and-the-150-million-typo)
- [AWS Official Postmortem](https://aws.amazon.com/message/41926/)
- [Gremlin: After the Retrospective](https://www.gremlin.com/blog/the-2017-amazon-s-3-outage)

### GitLab Incident
- [GitLab Official Postmortem](https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/)
- [TechCrunch: Backup Failure](https://techcrunch.com/2017/02/01/gitlab-suffers-major-backup-failure-after-data-deletion-incident/)

### Kubernetes Failures
- [k8s.af - Kubernetes Failure Stories](https://k8s.af/)
- [GitHub: kubernetes-failure-stories](https://github.com/hjacobs/kubernetes-failure-stories)
