# Episode Outline: Giving Thanks to Your Dependencies

## Story Planning

**NARRATIVE STRUCTURE**: Economic Detective (revealing hidden value/cost asymmetry)
**CENTRAL TENSION**: 96% of companies depend on open source, but 60% of maintainers are unpaid. We extract enormous value but rarely acknowledge it.
**THROUGHLINE**: From taking dependencies for granted to understanding the human infrastructure behind your code—and how to show meaningful gratitude.
**EMOTIONAL ARC**:
- Recognition: "My project has HOW many dependencies?"
- Surprise: "There are tools that help me thank maintainers?"
- Empowerment: "I can actually make a difference with simple actions"

## Act Structure

### ACT 1: SETUP (2-3 min)
- **Hook**: "Run `npm list` right now. How many packages? For most Node projects, it's hundreds. Who maintains them?"
- **Stakes**: The XZ Utils backdoor showed what happens when maintainers burn out (66% drop in trust toward new contributors)
- **Promise**: We'll discover tools you've never heard of, and walk away with a Thanksgiving challenge

**Key Points**:
- Average Node.js project: 100-500+ dependencies
- 60% of maintainers unpaid (Tidelift 2024)
- 60% have left or considered leaving projects
- YOUR infrastructure runs on their free time

### ACT 2: EXPLORATION (5-7 min)

#### Discovery 1: The Thanks Ecosystem
- **Node.js**: `npx thanks` - scans package.json, shows maintainers seeking donations (2.8k stars)
- **npm fund**: Built-in since v6.13, shows funding URLs for all dependencies
- **Philosophy**: "Put your money where your love is" (feross/thanks)

#### Discovery 2: Language-Specific Gratitude Tools
- **Rust**: `cargo-thanks` - stars GitHub repos of dependencies (inspired by Medium's clapping)
- **thanks-stars** - modern alternative with multi-ecosystem support
- **cargo-thanku** - generates acknowledgment docs

#### Discovery 3: Beyond Stars - Meaningful Actions
- **Happiness Packets**: Send anonymous thank-you notes to maintainers
- **Explain your use case**: Maintainers have ZERO visibility into how their projects are used
- **Good bug reports**: Reproductions are worth 100 "thanks" messages
- **Docs contributions**: Often the most neglected, most impactful

#### Complication: Not All Gratitude Is Equal
- Some maintainers: "Thanks does nothing for me—I'd rather users be more considerate of our time"
- The nuance: Combine words with ACTION (funding, PRs, good issues)
- Gratitude without action can feel hollow

**Key Points**:
- `npx thanks` output shows maintainers seeking funding
- `npm fund` lists funding URLs for your entire dependency tree
- Open Collective, GitHub Sponsors = direct funding mechanisms
- Documentation PRs often more valuable than code PRs

### ACT 3: RESOLUTION (3-4 min)

#### Company-Level Actions
- **Open Source Pledge**: $2K/developer/year minimum
- Real numbers: Antithesis $110K ($2,895/dev), Convex $100K ($7,692/dev)
- GitHub Sponsors matching programs
- May = Maintainer Month (GitHub invested $500K in 2024)
- Internal: Paid OSS contribution time

#### The Thanksgiving Challenge
1. Run `npx thanks` or `npm fund` right now
2. Pick ONE dependency you rely on heavily
3. Send a thank-you email explaining HOW you use it
4. Consider a small donation ($5-10)
5. Star the repos (takes 2 seconds, shows up in maintainer dashboards)

#### Empowerment
- Simple message quote: "Brightens up your day really"
- Your dependencies deserve a seat at the Thanksgiving table
- The code doesn't exist without the people who write it

**Key Points**:
- Open Source Pledge tracking: opensourcepledge.com
- GitHub Sponsors: sponsor button on any project
- Callback to Episode #037: sustainability requires investment

## Story Elements

**KEY CALLBACKS**:
- Episode #037 sustainability stats return (60%/60%)
- XZ Utils backdoor as cautionary tale
- "The code doesn't exist without the people" (closing line from #037)

**NARRATIVE TECHNIQUES**:
- Anchoring statistic: "How many dependencies in YOUR project?"
- Thought experiment: "What if everyone thanked ONE maintainer this Thanksgiving?"
- Historical context: npm fund launched 2019, ecosystem still evolving

**SUPPORTING DATA**:
- 60% maintainers unpaid (Tidelift 2024)
- 60% have left/considered leaving (Tidelift 2024)
- 96% of companies use open source (industry standard)
- 66% drop in maintainer trust post-XZ Utils
- feross/thanks: 2.8k stars, 85 contributors
- GitHub Maintainer Month: $500K invested (2024)
- Open Source Pledge: $2K/dev/year minimum

## Sources

- https://github.com/feross/thanks
- https://github.com/softprops/cargo-thanks
- https://crates.io/crates/thanks-stars
- https://blog.npmjs.org/post/187382017885/supporting-open-source-maintainers
- https://blog.opencollective.com/beyond-post-install/
- https://opensource.com/article/18/11/ways-give-thanks-open-source
- https://opensource.com/article/18/11/ways-to-say-thank-you
- https://www.scylladb.com/2021/11/24/giving-thanks-to-open-source-software-contributors/
- https://github.blog/open-source/maintainers/thank-you-to-our-maintainers/
- https://livablesoftware.com/5-ways-to-thank-open-source-maintainers/
- Episode #037 (maintainer sustainability stats)

## Quality Checklist

- [x] Throughline clear (one sentence)
- [x] Hook compelling (keep listening after 60s?)
- [x] Sections build momentum
- [x] Insights connect (not random facts)
- [x] Emotional beats land (2-3 moments)
- [x] Callbacks create unity
- [x] Payoff satisfies (delivers on promise)
- [x] Narrative rhythm (story not list)
- [x] Technical depth appropriate to topic
- [x] Listener value clear (what can DO)
