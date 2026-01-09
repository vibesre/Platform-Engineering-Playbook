# Episode #086: Cloudspecs - The End of Moore's Law for Cloud Computing

## Episode Overview

**Topic**: Cloudspecs research from TUM reveals uncomfortable truths about cloud hardware stagnation
**Episode Number**: 00086
**Slug**: `00086-cloudspecs-cloud-hardware-evolution`
**Type**: Daily episode with news segment

## Cold Open

"What if I told you that the best performing cloud instance for your money was released in 2016 - and nothing since has come close? New research from TUM exposes the uncomfortable truth about cloud hardware evolution."

## News Segment (7 items, ~4-5 minutes)

1. **AI Coding Tools DevOps Challenges**: Survey shows wider AI tool adoption creating new challenges
2. **LWKD Week Ending Jan 4**: Kubernetes development updates
3. **Windows Secure Boot Certs Expiring**: UEFI certificates expire June 2026 - action needed
4. **AWS Lambda .NET 10**: New runtime support available
5. **Amazon MQ mTLS**: Certificate-based authentication for RabbitMQ
6. **MCP is a fad**: Contrarian take on Model Context Protocol
7. **NVIDIA Rubin**: Next-generation AI supercomputer platform announced

## Main Topic: Cloudspecs Research (~15-18 minutes)

### ACT 1: The Research and Authors (3 min)

**The Paper**:
- "Cloudspecs: Cloud Hardware Evolution Through the Looking Glass"
- CIDR 2026 conference (January 18-21, 2026)
- Authors: Till Steinert, Maximilian Kuschewski, Viktor Leis
- Institution: Technische Universität München (TUM)

**The Tool**:
- Interactive browser-based AWS EC2 explorer
- Powered by DuckDB-WASM
- Live at cloudspecs.fyi
- All data and queries available for reproducibility

**Methodology**:
- 10-year analysis (2015-2025)
- Focus on AWS with comparisons to Azure, GCP, on-premise
- Key metric: Performance per dollar (not just raw performance)
- Benchmarks: SPECint, TPC-H, TPC-C

### ACT 2: The Shocking Findings (8-10 min)

**CPU Performance**:
- Multi-core counts increased 10x (max AWS: 448 cores)
- BUT cost-normalized gains only ~3x with Graviton, ~2x without
- In-memory database benchmarks: only 2-2.5x improvement
- On-premise AMD servers similarly stagnant (1.7x gain 2017-2025)

**Memory Crisis**:
- DRAM capacity per dollar has "effectively flatlined"
- Memory-optimized instances (2016) offered 3.3x better value
- Absolute bandwidth 5x (DDR3→DDR5), cost-adjusted only 2x
- AI-driven DDR5 price increases making it worse

**Network - The Bright Spot**:
- 10x improvement in bandwidth per dollar
- Absolute speeds: 10 Gbit/s → 600 Gbit/s (60x increase)
- Driven by AWS Nitro cards and network-optimized instances
- Only category with meaningful cloud price/performance gains

**NVMe Storage - The Scandal**:
- I/O throughput unchanged since 2016
- Capacity flat since 2019
- **i3 instances from 2016 still deliver best performance/dollar by ~2x**
- 36 NVMe instance families, yet none beat the 9-year-old i3
- On-premise PCIe 4/5 doubled performance twice - cloud missed it
- Widening gap driving disaggregated storage adoption

### ACT 3: Why This Happened (3-4 min)

**Theories from HN Discussion**:
- Intentional performance caps to extend SSD lifespan
- AWS prioritizing profitable networked storage (EBS margins)
- Virtualization overhead and technical constraints
- Limited customer demand - most workloads don't need max IOPS

**The Nitro Distinction**:
- i3: Direct NVMe attachment
- m6id and later: Virtualized NVMe through Nitro
- Different performance characteristics

**Cloud Provider Incentives**:
- EBS more profitable than local NVMe
- Storage-optimized instances = niche workloads
- Network improvements enable disaggregated architectures
- Less motivation to improve local storage

### ACT 4: Platform Engineering Implications (4-5 min)

**Instance Selection Strategy**:
- Don't assume newer = better per dollar
- Run Cloudspecs queries for your specific workload profile
- i3 instances may still be optimal for IO-heavy workloads in 2026

**Cost Optimization**:
- Performance per dollar matters more than raw performance
- Network improvements enable new architectures
- Memory costs driving application design changes

**Repatriation Consideration**:
- On-premise NVMe has widened the gap
- Storage-heavy workloads may warrant repatriation analysis
- Not universal - depends on workload profile

**Future Expectations**:
- Uniform hardware scaling has ended
- Specialization and hardware-software codesign the future
- Custom silicon (Graviton, Nitro) vs commodity hardware

**Using Cloudspecs Tool**:
- Browser-based, no backend needed
- DuckDB-WASM enables SQL queries in browser
- Fork for custom reproducibility
- Great for capacity planning and cost analysis

## Key Statistics

| Metric | Raw Improvement | Cost-Adjusted |
|--------|----------------|---------------|
| CPU (cores) | 10x | 2-3x |
| Memory | 5x bandwidth | 2x |
| Network | 60x | 10x |
| NVMe Storage | ~0x | Negative (i3 still best) |

## Sources

- [Cloudspecs Paper (TUM)](https://www.cs.cit.tum.de/fileadmin/w00cfj/dis/papers/cloudspecs-final.pdf)
- [Cloudspecs Tool](https://cloudspecs.fyi)
- [GitHub Repository](https://github.com/TUM-DIS/cloudspecs)
- [Murat Demirbas Blog Analysis](https://muratbuffalo.blogspot.com/2026/01/cloudspecs-cloud-hardware-evolution.html)
- [Hacker News Discussion](https://news.ycombinator.com/item?id=46555485)
- [CIDR 2026 Accepted Papers](https://www.cidrdb.org/cidr2026/papers.html)

## Pronunciation Notes

- CIDR: "cider" (like the drink)
- TUM: "T U M" (spell out)
- Steinert: "SHTINE-urt"
- Kuschewski: "koo-SHEV-ski"
- Leis: "LICE" (rhymes with rice)
- NVMe: "N V M E" (spell out)
- DuckDB: "duck D B"
- WASM: "waz-um"
- SPECint: "SPEC int"
- TPC-H: "T P C H"
- Graviton: "GRAV-ih-ton"
- Nitro: "NY-tro"

## Target Duration

~22-25 minutes total:
- News: 4-5 minutes
- Main topic: 15-18 minutes
- Transitions: 2-3 minutes
