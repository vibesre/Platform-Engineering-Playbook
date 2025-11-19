# Podcast Outline: Cloudflare November 2025 Outage

## Episode Metadata
- **Episode Number**: 030
- **Title**: Cloudflare Outage November 2025: When a Rust Panic Took Down 20% of the Internet
- **Duration Target**: 12-15 minutes
- **Speakers**: Jordan and Alex
- **Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

## Episode Summary
On November 18, 2025, a routine database permissions change triggered Cloudflare's worst outage since 2019—taking down X, ChatGPT, Shopify, Discord, and 20% of the internet for nearly 6 hours. Jordan and Alex dissect the technical chain reaction from ClickHouse metadata exposure to a Rust panic in the FL2 proxy, breaking down how ~60 features became >200 and exceeded a hardcoded memory limit. They examine what this means for infrastructure concentration risk after three major cloud outages in 30 days (AWS, Azure, Cloudflare).

## Key Topics
- ClickHouse database permissions change and metadata exposure
- FL2 Rust proxy architecture and hardcoded limits
- Bot Management feature file generation failure
- Infrastructure concentration risk (AWS, Azure, Cloudflare in 30 days)
- Configuration validation and graceful degradation patterns

---

## Episode Structure

### 1. Hook & Introduction (1-2 min)

**Hook**: Start with the scale - ChatGPT down, X down, Shopify down, Discord down, even Downdetector (the site that tracks outages) went down. All from a single configuration change.

**Key Stats to Lead With**:
- 20% of all websites affected (Cloudflare's market share)
- 35% of Fortune 500 companies rely on Cloudflare
- ~60 features ballooned to >200 features, exceeding hardcoded 200-feature limit
- HTTP 5xx errors for all FL2 proxy customers
- 5 hours 46 minutes total outage duration
- Third major cloud outage in 30 days (AWS Oct 20, Azure Oct 29, Cloudflare Nov 18)
- Cloudflare's worst outage since 2019

**Framing**: This isn't just another outage postmortem—it's a wake-up call about infrastructure concentration risk and what happens when internal config is treated differently than user input.

---

### 2. What Happened: Timeline & Immediate Impact (2-3 min)

**Timeline (UTC)**:
- 11:05 - Database permissions change deployed to ClickHouse cluster
- 11:20-11:28 - First errors observed in customer traffic
- 11:31 - Automated test detected issue
- 11:35 - Incident call created
- 11:48 - Cloudflare publicly acknowledged issue
- 13:05 - Workers KV and Access bypass implemented
- 13:37 - Root cause identified (Bot Management config)
- 14:24 - Bad configuration propagation halted
- 14:30 - Core traffic restored
- 17:06 - Full service restoration

**Total Duration**: 5 hours 46 minutes

**Services Affected**:
- **AI Services**: ChatGPT, Claude, Perplexity AI, DALL-E
- **Social/Communication**: X (Twitter), Discord
- **E-commerce**: Shopify (massive Black Friday prep period)
- **Entertainment**: Spotify, League of Legends, RuneScape
- **Productivity**: Canva (100M+ users)
- **Food/Transport**: Uber, Uber Eats, McDonald's ordering systems
- **Crypto**: Multiple exchanges, BitMEX
- **Meta**: Downdetector itself went down

**Initial Misdiagnosis**: Team initially suspected a hyper-scale DDoS attack because:
- Status page went down (unrelated cause, but deepened suspicion)
- Symptoms appeared intermittent (due to gradual ClickHouse cluster updates)
- Scale matched attack patterns

---

### 3. Technical Deep Dive: The Cascade (4-5 min)

**This is where we get into the weeds - our audience will love this**

#### Layer 1: The ClickHouse Permissions Change

- Cloudflare was improving distributed query permissions in their ClickHouse database
- Previous setup: Metadata queries only returned results from `default` database
- New permissions: Also exposed metadata from underlying `r0` database
- This exposed duplicate column information

#### Layer 2: The Bot Management Feature File

- Bot Management uses ML models requiring feature configuration
- A ClickHouse query generates this "feature file" every 5 minutes
- The query wasn't filtering by database name
- Result: File doubled in size as duplicate features were added
- Normal size: ~60 features
- After change: >200 features (duplicates from both databases)

#### Layer 3: The FL2 Rust Proxy Panic

- FL2 is Cloudflare's new Rust-based proxy (replaced Nginx/LuaJIT FL1)
- Bot Management module preallocates memory with hardcoded 200-feature limit
- When file exceeded limit: `thread fl2_worker_thread panicked: called Result::unwrap() on an Err value`
- **Critical Issue**: No graceful degradation—system panicked instead of reverting to previous config or using defaults

#### Why It Was Intermittent

The ClickHouse cluster was being gradually updated:
- If query hit updated node → bad file generated → crash
- If query hit old node → normal file → system works
- This 5-minute cycle made diagnosis extremely difficult

#### FL2 vs FL1 Impact

- **FL2 customers**: HTTP 5xx errors (complete failure)
- **FL1 customers**: Bot scores returned as 0 (false positives for bot-blocking rules)

**Key Technical Failures**:
1. No input validation on internal config (treated differently than user input)
2. Hardcoded limits with panic instead of graceful degradation
3. No feature kill switches for rapid module disable
4. Core dumps overwhelmed system resources during debugging
5. Missing database name filtering in the query

---

### 4. The Real Lesson: Infrastructure Concentration Risk (3-4 min)

**The Pattern**: Three major outages in 30 days
- October 20: AWS outage (DynamoDB DNS race condition, 15+ hours)
- October 29: Microsoft Azure outage
- November 18: Cloudflare outage (5h 46m)

**The Technical Scale**:
- Cloudflare: 20% of websites, 35% of Fortune 500
- Big Three (AWS, GCP, Azure): ~66% of cloud infrastructure
- Cisco logged 12 major outages in 2025 so far (vs 23 in 2024, 13 in 2023, 10 in 2022)
- 78% of German companies consider US cloud dependency "too great"

**The Irony**: The internet was designed to route around damage
- ARPANET core principle: No single points of failure
- Today's reality: Efficiency and cost optimization trumped resilience
- "For one company to disable 50% of the internet is... bad"

**Geopolitical Dimension**:
- Three American corporations control Europe's digital infrastructure
- Digital sovereignty concerns rising
- 82% of German companies want European hyperscalers

**What This Means for Platform Teams**:
- Multi-CDN strategies are no longer optional for critical services
- Blast radius analysis must include third-party dependencies
- "We use Cloudflare" is not a complete resilience story

---

### 5. Cloudflare's Remediation & Industry Lessons (2-3 min)

**Cloudflare's Committed Fixes**:
1. Harden ingestion of internal config files like user input
2. Enable global kill switches for features
3. Eliminate core dumps overwhelming system resources
4. Review failure modes across all proxy modules

**Lessons for Platform Engineers**:

**Configuration Management**:
- Never trust internal data more than external data
- Validate ALL inputs, especially those "we control"
- Config changes need the same rigor as code changes

**Graceful Degradation**:
- Hardcoded limits must have fallback behavior
- Panic should be last resort, not first response
- Design for "what if this file is corrupted?"

**Observability & Kill Switches**:
- Feature flags at the edge matter
- Ability to instantly disable modules without restart
- Monitoring for config file anomalies (size, schema)

**Blast Radius Awareness**:
- Map your third-party dependencies
- Understand what happens when each one fails
- Consider multi-vendor strategies for critical paths

---

### 6. Practical Takeaways (1-2 min)

**This Week's Actions**:

1. **Audit your CDN strategy**: If you're 100% on one provider, what's your fallback?

2. **Review config validation**: Do you validate internal configuration files with the same rigor as user input?

3. **Check for hardcoded limits**: Where do your systems have limits that panic instead of degrade?

4. **Map your dependency tree**: Which third-party services could take you down completely?

5. **Test your kill switches**: Can you disable features without full redeploys?

**The Key Mental Model**:
"Internal" doesn't mean "trustworthy"—treat configuration from your own systems with the same defensive programming you'd use for external input.

---

### 7. Closing (30-45 sec)

**Connect Back to Theme**: This is the third major cloud outage in 30 days. The question isn't whether your infrastructure provider will have an outage—it's whether you've designed your systems to survive it.

**Forward Look**: Infrastructure concentration will only increase. The teams that build resilient systems treat every dependency—internal and external—as potentially hostile.

**Final Thought**: Sometimes the most dangerous code is the code that handles your own data, because that's where your guard is down.

---

## Sources

### Primary Sources
- Cloudflare Official Blog Post: https://blog.cloudflare.com/18-november-2025-outage/
- Cloudflare CTO Statement (Dane Knecht)

### Supporting Sources
- Tom's Hardware live coverage
- TechRadar reporting
- CNBC coverage
- CNN Business analysis
- TechCrunch technical analysis
- CyberSecurity News
- NetworkWorld analysis
- Similar AWS October 2025 outage analysis (episode #007)

### Technical Statistics
- 20% of websites on Cloudflare (industry reports)
- 35% Fortune 500 on Cloudflare
- ~60 features normally in Bot Management file
- 200 hardcoded feature limit in FL2
- 5-minute feature file generation cycle
- 12 major outages in 2025 vs 23 in 2024 (Cisco)
- 5h 46m total outage duration

---

## Episode Cross-References

- **Episode #007**: AWS Outage October 2025 - Similar DNS/configuration cascade failure
- **Episode #023**: DNS for Platform Engineering - DNS as critical infrastructure
- **Episode #026**: Kubernetes Complexity Backlash - Infrastructure concentration theme

---

## SSML Notes

**Technical terms requiring pronunciation attention**:
- ClickHouse (CLICK-house)
- FL2 (F-L-two)
- Nginx (engine-X)
- LuaJIT (LOO-ah-JIT)

**Suggested pause points**:
- After timeline (let it sink in)
- After each technical layer explanation
- Before practical takeaways
