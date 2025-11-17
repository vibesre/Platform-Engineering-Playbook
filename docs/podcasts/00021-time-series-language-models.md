---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "🎙️ #021: Time Series Language Models"
slug: 00021-time-series-language-models
---

# Time Series Language Models: AI That Reads Your Metrics Like Language (But Isn't Ready Yet)

## The Platform Engineering Playbook Podcast

<GitHubButtons />

**Duration:** 19 minutes
**Speakers:** Alex and Jordan
**Target Audience:** Senior platform engineers, SREs, DevOps engineers with 5+ years experience

> 📝 **Read the [full blog post](/blog/2025-11-15-time-series-language-models-opentmls-toto-infrastructure-monitoring)**: Comprehensive written analysis of TSLMs with technical deep-dive, research citations, and actionable recommendations for platform teams.

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, margin: '1.5rem 0'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/_xgbTxI7L70"
    title="YouTube video player"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>

<PodcastSubscribeButtons />

---

**Jordan**: Today we're diving into something that sounds like science fiction but exists right now. AI that can read your infrastructure metrics like language, explain anomalies in plain English, and predict failures without being trained on your specific data.

**Alex**: And the weird part? Even the companies who built this technology won't use it in production yet.

**Jordan**: Wait, seriously? We're talking about real tech that's already released, not vaporware?

**Alex**: October twenty twenty-five. Stanford releases OpenTSLM. May twenty twenty-five, Datadog releases Toto—trained on two point three six trillion observability data points. These are foundation models for time-series data, just like GPT is for text.

**Jordan**: Okay, so paint me the picture. What does this actually look like in practice?

**Alex**: Imagine it's three AM. Your Prometheus metrics detect a latency spike. Traditional monitoring sends you an alert that says "latency exceeded threshold." You wake up, check Grafana dashboards, correlate metrics manually, dig through logs for thirty minutes to figure out what happened.

**Jordan**: Yeah, I've been there. Many times.

**Alex**: Now imagine your observability platform reads that spike like a sentence. It understands what the pattern means based on your entire infrastructure history. It tells you in plain English: "This latency spike correlates with database connection pool saturation based on similar patterns in forty-seven historical incidents. Recommend increasing pool size from one hundred to one fifty connections based on current traffic growth of fifteen percent month over month."

**Jordan**: That's... that's exactly what I need at three AM. Natural language root cause analysis with specific recommendations. So why aren't we all using this?

**Alex**: That's the mystery we're unraveling today. Revolutionary technology that exists but sits on the shelf.

**Jordan**: Alright, let's start with the basics. What are Time-Series Language Models? Because I know what time-series data is, I know what language models are, but together?

**Alex**: So you know how LLMs conquered text with GPT, then images with DALL-E, audio with Whisper, video with Sora? Each time it's the same foundation model paradigm—train on massive datasets, get zero-shot capabilities, transfer learning across domains.

**Jordan**: Right, and that's what makes them powerful. GPT-four works across tasks without fine-tuning because it learned from such diverse text.

**Alex**: Exactly. TSLMs bring that same paradigm to temporal numerical data. They integrate time-series as a native modality alongside text. So instead of just processing words or images, they understand trends, seasonality, anomalies in metrics—and can explain what they're seeing in natural language.

**Jordan**: Okay, but how? Because metrics are numbers over time, not text tokens.

**Alex**: Three main approaches. First, quantization—convert time-series values into text tokens that the LLM processes. Like turning CPU at forty-five percent into a special token representing "mid-range value."

**Jordan**: That sounds like you'd lose numerical precision though.

**Alex**: You do. Second approach is soft prompting—embed the time-series into continuous vector space, concatenate with text embeddings, and the LLM processes both jointly. That's what OpenTSLM's SoftPrompt architecture does.

**Jordan**: And the memory requirements?

**Alex**: One hundred ten gigabytes of VRAM for SoftPrompt. Which is why they built a third approach—Flamingo uses cross-attention. Time-series gets its own encoder, then cross-attention layers bridge between time-series and text. More memory efficient at forty gigs.

**Jordan**: Still forty gigs. That's not exactly running on my laptop.

**Alex**: No, but it's the best we've got. And the performance is genuinely impressive. OpenTSLM on sleep staging—sixty-nine point nine F-one score versus nine point zero five baseline. That's seven point seven times improvement.

**Jordan**: Sleep staging? I thought we were talking about infrastructure monitoring.

**Alex**: That's the thing—OpenTSLM is medical-focused right now. Sleep analysis, ECG, human activity recognition. But the architecture is domain-agnostic. It's designed for any temporal data.

**Jordan**: So someone just needs to apply it to infrastructure metrics.

**Alex**: Someone did. Datadog built Toto—Time Series Optimized Transformer for Observability. Trained specifically on infrastructure and observability metrics.

**Jordan**: How much data are we talking?

**Alex**: Two point three six trillion data points. That's the largest dataset for any open-weights time-series foundation model ever created.

**Jordan**: Trillion with a T. And performance?

**Alex**: Zero point six seven two sMAPE on observability data. Best among all time-series foundation models. It outperforms Google's TimesFM, Amazon's Chronos, Salesforce's Moirai—specifically on infrastructure metrics.

**Jordan**: Okay, so let me get this straight. Datadog built the world's best observability AI, trained it on two point three six trillion infrastructure data points, achieved state-of-the-art performance, and then... what? They're not using it?

**Alex**: Direct quote from their blog: "Toto is still early in development and not currently deployed in production systems as we focus on thorough testing and product integration."

**Jordan**: That's the mystery right there. If even Datadog won't deploy their own cutting-edge observability AI to production, what are they waiting for?

**Alex**: That's what I wanted to unpack. There's a third player too—TimeGPT from Nixtla. Released in twenty twenty-four, trained on about one hundred billion data points across finance, transportation, web traffic, weather, energy.

**Jordan**: So OpenTSLM is research-focused on medical, Toto is observability but not deployed, and TimeGPT is...?

**Alex**: General-purpose forecasting with commercial API. It's actually production-ready with SLAs and support contracts. But it's limited to forecasting—doesn't do the full observability stack like anomaly detection or root cause analysis.

**Jordan**: So we've got three models, three different maturity levels, but none doing what you described at the beginning—that three AM root cause explanation.

**Alex**: Not yet. And here's where it gets interesting. The technology works. The benchmarks are real. So what's actually missing?

**Jordan**: Let's talk performance. Because "works in research" and "works in production at three AM" are very different things.

**Alex**: True. And there's a study from December twenty twenty-four that's revealing. Time-series foundation models quote "struggle to capture task-specific nuances" required for effective anomaly detection.

**Jordan**: Meaning?

**Alex**: Traditional methods—XGBoost, autoencoders—frequently match or outperform TSLMs on anomaly detection tasks. The foundation models are good at general patterns but miss the specific edge cases that matter for alerts.

**Jordan**: So if I'm running mission-critical alerting, traditional methods are still more reliable.

**Alex**: As of late twenty twenty-five, yes. But here's the tradeoff—TSLMs are easier to use because they're zero-shot. No training required. And they give you natural language explanations.

**Jordan**: That's valuable for humans understanding what happened, even if the detection accuracy is similar to traditional methods.

**Alex**: Exactly. Traditional methods might say "anomaly detected" with ninety-five percent confidence. A TSLM says "anomaly detected and here's why—pattern matches these seventeen historical incidents, likely caused by X, recommend action Y."

**Jordan**: I'd take explainability over two percent accuracy gain any day. But you said forty to one hundred ten gigs of VRAM. What's that actually cost?

**Alex**: Self-hosting means twenty to forty thousand dollars in GPU hardware. And inference latency is seconds to minutes, not the sub-one hundred millisecond you need for real-time alerting.

**Jordan**: Versus traditional methods that run on commodity hardware with millisecond latency.

**Alex**: Right. And then there's the expertise problem. To actually use TSLMs effectively, you need knowledge across three domains.

**Jordan**: Let me guess. Time-series fundamentals, LLM concepts, and infrastructure domain knowledge.

**Alex**: Exactly. Seasonality and trends, transformer architecture and prompt engineering, Prometheus and Grafana and SRE practices. How many engineers have all three?

**Jordan**: Not many. So even if I had the hardware, I'd need to hire or train for this very specific skill intersection.

**Alex**: Which brings us to what's actually missing. It's not that the technology doesn't work—it does. It's all the production infrastructure around it.

**Jordan**: Meaning vendor support, battle-testing at scale, integration ecosystem.

**Alex**: Yeah. There's no Prometheus exporters for TSLMs. No Grafana plugins. No Kubernetes operators. You'd have to build all the integration yourself.

**Jordan**: And unknown failure modes. When GPT hallucinates, you get weird text. When your monitoring hallucinates at three AM...

**Alex**: You might ignore a real incident or wake up the team for a false positive. The false positive rate isn't well-characterized for TSLMs yet. That's critical for alerting—alert fatigue is already a huge problem.

**Jordan**: Plus foundation models are black boxes. If my traditional anomaly detector fires, I can debug the algorithm. If a TSLM fires, how do I know why?

**Alex**: Explainability paradox. They can explain the anomaly in natural language, but you can't explain why the model made that decision in the first place.

**Jordan**: Regulatory nightmare for anyone in FinServ or healthcare. So what's the actual timeline here? When does this technology become production-ready?

**Alex**: Based on what Datadog's saying and the current maturity, I'd estimate twenty twenty-six to twenty twenty-seven for vendor integrations.

**Jordan**: Meaning Datadog releases Toto as part of Watchdog, other observability platforms follow?

**Alex**: Exactly. They're doing thorough testing and product integration now. First production deployments, case studies, battle-testing. Then commercial TSLM services launch.

**Jordan**: And mainstream adoption?

**Alex**: Twenty twenty-seven plus. That's when you get mature Prometheus exporters, Grafana plugins, production-proven at scale, becomes standard platform engineering practice.

**Jordan**: So if I'm a platform engineer listening to this in late twenty twenty-five, what should I actually do? Because this sounds important but not ready.

**Alex**: That's the key question. And the answer is prepare, don't implement. Three areas to focus on.

**Jordan**: Skills first, right? What should I be learning now?

**Alex**: Time-series fundamentals. Make sure you really understand seasonality, trends, stationarity, forecasting metrics like MAE and sMAPE. There's a good book out—"Time Series Forecasting Using Foundation Models" from Manning, twenty twenty-five.

**Jordan**: What about the LLM side?

**Alex**: Learn transformers, attention mechanisms, prompt engineering. You don't need to implement them from scratch, but understanding how they work helps you use them effectively. And that knowledge is valuable regardless of whether TSLMs take off.

**Jordan**: Because even if TSLMs don't become the standard, LLM concepts are everywhere now.

**Alex**: Exactly. And then deepen your infrastructure domain expertise. The better you understand what questions to ask about your metrics, the more valuable any AI tool becomes.

**Jordan**: Okay, skills make sense. What about hands-on experimentation?

**Alex**: Three levels depending on your resources. Lowest barrier—sign up for TimeGPT API, forecast some non-critical metrics, compare to a Prophet baseline. Just to experience zero-shot forecasting.

**Jordan**: That's the commercial API, so it costs money but you don't need hardware.

**Alex**: Right. Medium barrier—download Toto's open-weights model from Hugging Face, run it on dev or staging observability data, benchmark against traditional methods. You'll need some compute but it's educational.

**Jordan**: And for research organizations?

**Alex**: Clone the OpenTSLM repository, try adapting it to infrastructure metrics. That requires ML expertise, but if you've got it, you're exploring the cutting edge.

**Jordan**: All of these in non-critical environments only.

**Alex**: Absolutely. This is learning and positioning, not production deployment. You're building skills so when vendors ship production-ready versions, you're not starting from zero.

**Jordan**: What should we be monitoring? How do we know when it's actually ready?

**Alex**: Watch for vendor announcements. Datadog Watchdog integration with Toto, Grafana AI features roadmap, any observability platform announcing TSLM capabilities.

**Jordan**: And the signal that it's production-ready versus just marketing?

**Alex**: Look for public case studies from organizations similar to yours. SLAs and support contracts becoming available. False positive rates being published and characterized. Integration ecosystem maturing—actual Prometheus exporters, not just APIs.

**Jordan**: So the green lights are vendor production integration, case studies, SLAs, characterized performance, mature integrations.

**Alex**: Exactly. And the red flags are only research papers with no deployments, alpha or beta labels, no SLAs, and critically—the vendor hasn't deployed to their own infrastructure.

**Jordan**: Which is where we are now with Toto. Datadog built it but won't use it themselves yet.

**Alex**: Right. That's your clearest signal. When Datadog announces "Toto is now powering Watchdog in production," that's when you know it's ready.

**Jordan**: Alright, so give me the conservative playbook. Timeline for how platform teams should approach this.

**Alex**: Twenty twenty-five to twenty twenty-six—develop skills, experiment in non-critical environments. Read the books, try the APIs, understand the concepts.

**Jordan**: While monitoring vendor announcements.

**Alex**: Exactly. Twenty twenty-six to twenty twenty-seven—pilot vendor solutions when they become available. Join beta programs, test in staging, prepare for production.

**Jordan**: And actual production deployment?

**Alex**: Twenty twenty-seven plus, after it's proven at scale. Wait for battle-testing, case studies, mature integrations. Don't be the guinea pig for your monitoring stack.

**Jordan**: Because if our monitoring fails, everything fails.

**Alex**: Exactly. This isn't like trying a new CI CD tool where worst case you roll back. Monitoring is foundational.

**Jordan**: Let me bring this back to that three AM latency spike we started with. Because I think that scenario captures both the promise and the reality.

**Alex**: Yeah, that scenario will happen. AI will eventually read that spike, understand the pattern, explain the root cause in plain English. But today?

**Jordan**: Today, Prometheus and Grafana and solid alerting are still the right answer.

**Alex**: And that's okay. The smartest move isn't rushing to adopt unready technology. It's positioning yourself to lead when it matures.

**Jordan**: Build the skills now—time-series fundamentals, LLM concepts, deep infrastructure knowledge. Experiment in safe environments. Monitor vendor maturity. And when they ship production-tested solutions in twenty twenty-six or twenty twenty-seven, you're ready to evaluate and deploy.

**Alex**: Not just ready—you're ahead of peers who ignored this entirely or wasted time implementing half-baked solutions too early.

**Jordan**: The fundamentals remain constant. Good observability practices, understanding your metrics, thoughtful alerting. TSLMs will enhance that, not replace it.

**Alex**: And when they do arrive, the platform engineers who prepared—who understand both the technology and its limitations—they'll be the ones extracting real value.

**Jordan**: Not just adopting because it's AI and AI is hot, but because they can articulate exactly where it adds value and where traditional methods still win.

**Alex**: That's the empowering part of this story. Yes, revolutionary technology is coming. But you have time to prepare thoughtfully instead of reactively.

**Jordan**: The future of infrastructure monitoring is AI that understands temporal patterns and speaks human language. But the future isn't twenty twenty-five. It's twenty twenty-six, twenty twenty-seven, and beyond. And the platform engineers who lead that transition are the ones building skills and experimenting now.

**Alex**: Without betting the farm on unready tech.

**Jordan**: Exactly. Prepare, don't implement. That's the takeaway.
