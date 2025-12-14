# Episode #059: Platform Engineering 2025 Year in Review - Outline

## Episode Overview
- **Title**: Platform Engineering 2025 Year in Review: The Year We Grew Up
- **Duration Target**: 20-25 minutes
- **Format**: Single comprehensive episode (no separate news segment)
- **Publication Date**: December 15, 2025
- **Speakers**: Jordan & Alex

## Hook
"2025 was the year platform engineering grew up—and got a reality check. AI entered infrastructure, industry consensus emerged on what platforms should actually do, and then Cloudflare went down six times to remind us that concentration risk isn't theoretical."

---

## Segment 1: Opening & Year Framing (2 minutes)

### Jordan Opens
- Hook statement about 2025 being transformational
- Frame: Three defining themes—AI transformation, consensus emergence, reality checks
- Preview: 10 defining stories from the year

### Alex Adds Context
- By the numbers: 58 podcast episodes, 33 blog posts this year
- Major conferences covered: KubeCon EU/NA, AWS re:Invent
- The year started with IngressNightmare and ended with agentic AI

---

## Segment 2: The AI Transformation (4 minutes)

### Story #1: AI-Native Kubernetes Arrived

**Jordan**:
- Kubernetes AI Conformance Program v1.0 launched at KubeCon NA (November 11)
- DRA (Dynamic Resource Allocation) reached GA in Kubernetes 1.34
- 11+ vendors certified immediately (Google, Azure, Oracle, CoreWeave, AWS)
- Stat: 30-40% GPU cost savings with proper DRA implementation

**Alex**:
- Why this matters: Freedom from vendor lock-in for AI workloads
- Five core requirements: DRA, intelligent autoscaling, accelerator metrics, AI operators, gang scheduling
- The standardization war is over—Kubernetes won as AI infrastructure

### Story #5: Agentic AI Entered Platform Engineering

**Jordan**:
- AWS re:Invent introduced "frontier agents"—DevOps Agent with 86% root cause identification
- GitHub Agent HQ for orchestrating multi-agent platforms
- Werner Vogels coined "verification debt"—the new technical debt

**Alex**:
- Reality check: 80% of companies report agents executing unintended actions
- Only 44% have agent-specific security policies
- Gartner prediction: 40% of agentic AI projects will fail by 2027
- Quote: "Verification debt needs formalization" - Werner Vogels

---

## Segment 3: Platform Engineering Grows Up (4 minutes)

### Story #2: Platform Engineering Reached Consensus (But 70% Still Fail)

**Jordan**:
- After years of definitional chaos, industry agreed on 3 principles:
  1. API-first self-service
  2. Business relevance
  3. Managed service approach
- KubeCon NA had multiple talks confirming this alignment
- Real adoption: Intuit/Mailchimp (11M users), Bloomberg (9 years K8s), ByteDance AI Brix

**Alex**:
- DORA 2025 data: 90% of organizations have platform initiatives
- But reality: platform teams decreased throughput 8%, stability 14%
- The "puppy for Christmas" anti-pattern explains 70% failure
- Quote: "Most teams renamed their ops team and expected different results"

### Team Structures That Work
- Optimal size: 6-12 people (Spotify model)
- Dedicated platform leader needed at 100+ engineers
- Team Topologies: Collaboration mode → X-as-a-Service evolution
- Stat: 8-10% productivity boost when done right

---

## Segment 4: The Year of Outages (3 minutes)

### Story #3: Infrastructure Concentration Risk Became Real

**Jordan**:
- AWS US-EAST-1 October 19 outage
  - $75M/hour impact
  - 6.5 million downtime reports
  - 70+ AWS services down from DNS race condition
  - 14+ hour duration

**Alex**:
- Cloudflare: 6 major outages in 2025
  - November 18: 20% of internet down for 6 hours (Rust panic)
  - December 5: 28% HTTP traffic impacted for 25 minutes
  - Pattern exposed dependency risks most organizations ignored

### Story #4: IngressNightmare

**Jordan**:
- CVE-2025-1974 disclosed March 24
- CVSS 9.8—unauthenticated RCE, cluster-wide secret exposure
- 43% of cloud environments vulnerable
- 6,500+ clusters exposed including Fortune 500s

**Alex**:
- Ingress NGINX retirement announced: March 2026 deadline
- Only 1-2 maintainers remaining
- Platform teams have 4 months to migrate to Gateway API
- Lesson: "Security through obscurity" failed

---

## Segment 5: Open Source Crossroads (3 minutes)

### Story #6: Open Source Sustainability Crisis

**Jordan**:
- CNCF 10-year anniversary: 300K contributors
- Dark reality: 60% of maintainers unpaid, 60% left or considering leaving
- XZ Utils backdoor (2024) aftermath still shaping 2025 policy

**Alex**:
- Han Kang memorial at KubeCon—in-toto lead, reminded us of human cost
- CNCF invested $3M+ in security, audits, tooling
- Open Source Pledge gaining traction: $2K/dev/year recommended
- Governance reforms: CNCF went from 6 to 4 subteams for sustainability

---

## Segment 6: Tools & Projects That Defined 2025 (3 minutes)

### Story #9: Infrastructure as Code Consolidated

**Jordan**:
- IBM acquired HashiCorp ($6.4B)—massive consolidation
- CDKTF deprecated after 5 years (Pulumi won the CDK war)
- OpenTofu: 10M+ downloads, feature parity achieved in July

**Alex**:
- Helm 4.0 released November 12—first major version in 6 years
  - WASM plugins for portability
  - Server-Side Apply replaces 3-way merge
  - 40-60% faster deployments
- ArgoCD 3.0 GA in May—fine-grained RBAC, security improvements

### CNCF Graduations
- Crossplane (November 6)—70+ adopters including Nike, NASA, SAP
- Knative (October 8)—serverless event-driven platform matured
- CubeFS (January 21)—350 petabytes stored across 200+ organizations

### Story #10: Gateway API Became the Standard

**Jordan**:
- Gateway API v1.4 GA (October 6)
- Multi-role architecture accepted: Infrastructure Provider, Cluster Operator, Application Developer
- Ingress is officially legacy

---

## Segment 7: Economics & Efficiency (2 minutes)

### Story #7: GPU Economics Exposed Massive Waste

**Jordan**:
- Average H100 utilization: 13%
- That's $4,350/month waste per GPU
- 60-70% of GPU budgets wasted industry-wide

**Alex**:
- Real case study: 20 H100s → 7 H100s (65% reduction, $35K/month savings)
- DRA, time-slicing, MIG becoming mandatory knowledge
- FinOps for AI is the next frontier

### Story #8: Service Mesh Sidecar Era Ended

**Jordan**:
- Istio Ambient mode GA: 90% memory reduction, 50% CPU reduction
- 70% of organizations now running service mesh
- Sidecar architecture becoming legacy

**Alex**:
- Benchmark: 8% mTLS overhead (Ambient) vs 99% (Cilium)
- $186K/year savings for 2,000-pod clusters
- eBPF approach (Cilium, Tetragon) gaining ground for security observability

---

## Segment 8: What's Coming in 2026 (2 minutes)

**Jordan**:
- March 2026: Ingress NGINX retirement deadline—migrate to Gateway API
- Agentic AI adoption curve—verification debt formalization needed
- Platform team scaling challenges at enterprise (Okta's 1,000 cluster lessons)
- Kubernetes 1.35+ continuing rapid innovation

**Alex**:
- CNPE certification creating new platform engineer credentialing
- SBOM requirements becoming federal mandate
- Multi-cluster management becoming standard (ArgoCD Agent hub-spoke model)
- Prediction: 2026 will be "year of platform team professionalization"

---

## Segment 9: Closing & Takeaways (2 minutes)

### Jordan's Top 5 Takeaways

1. **AI infrastructure is now standardized**—Kubernetes AI Conformance Program v1.0 means vendor lock-in is optional
2. **Platform engineering has a definition**—API-first self-service, business relevance, managed service approach
3. **Concentration risk is real**—Multi-region, multi-cloud, multi-CDN isn't paranoia
4. **Open source needs funding**—If you depend on it, pay for it ($2K/dev/year)
5. **GPU waste is the new cloud waste**—13% utilization is unacceptable

### Alex's Action Items

1. **Migrate to Gateway API before March 2026**—Ingress NGINX is retiring
2. **Implement DRA for AI workloads**—30-40% cost savings possible
3. **Audit your agent policies**—Only 44% of companies have them
4. **Review your Cloudflare/AWS single dependencies**—2025 proved the risk
5. **Sponsor an open source project**—CNCF, Apache, Linux Foundation all accept contributions

### Closing

**Jordan**: "2025 was the year platform engineering grew up. AI arrived, consensus emerged, and reality tested our assumptions. The infrastructure you build in 2026 should reflect these lessons."

**Alex**: "The fundamentals remain constant: reliability, security, cost efficiency. But the tools, patterns, and threats keep evolving. Stay curious, stay critical, and we'll see you in 2026."

---

## Key Statistics Reference

| Statistic | Value | Source |
|-----------|-------|--------|
| Platform team failure rate | 45-70% | DORA 2024/2025 |
| GPU utilization average | 13% | Kubernetes GPU FinOps |
| AWS outage cost | $75M/hour | October 2025 |
| Cloudflare outages in 2025 | 6 major | Analysis |
| IngressNightmare exposure | 43% of clouds | CVE-2025-1974 |
| CNCF maintainers unpaid | 60% | KubeCon report |
| Platform engineer salary premium | 20-27% | Multiple sources |
| Global cloud spend | $720B | FinOps research |
| Cloud waste | 20-30% | Industry analysis |
| Agents with unintended actions | 80% companies | AWS re:Invent |
| Agent security policies | 44% have them | Research |
| Agentic AI failure prediction | 40% by 2027 | Gartner |
| Service mesh adoption | 70% | CNCF survey |
| Istio Ambient memory reduction | 90% | Benchmarks |
| OpenTofu downloads | 10M+ | Project stats |
| Crossplane adopters | 70+ | CNCF graduation |

---

## Episode Cross-References (for transcript)

- Episode #035-037: KubeCon Atlanta coverage
- Episode #049-052: AWS re:Invent series
- Episode #030, #047: Cloudflare outages
- Episode #007: AWS US-EAST-1 outage
- Episode #057: Platform team structures
- Episode #058: Okta GitOps journey
- Episode #040: Platform engineering anti-patterns
- Episode #034: GPU waste and FinOps
- Episode #033: Service mesh showdown
- Episode #042: Helm 4 deep dive
- Episode #029: Ingress NGINX retirement
- Episode #043: Kubernetes AI Conformance Program
