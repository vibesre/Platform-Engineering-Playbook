# Lesson Outline: Episode 13 - Financial Services Compliance: SEC SCI, MiFID II, Crypto Regulations

## Metadata
**Course**: Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale
**Episode**: 13 of 16
**Duration**: 15 minutes
**Episode Type**: Advanced
**Prerequisites**: Episodes 1-12 (full architecture)
**Template Used**: Template 4 (Advanced)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. Explain SEC Regulation SCI requirements and implications for multi-region RTO/RPO
2. Apply MiFID II data residency requirements to architecture (EU-only multi-region)
3. Implement crypto compliance requirements (BitLicense, MiCA) with immutable audit logging
4. Identify when compliance overrides technical elegance

Success criteria:
- Can explain why SEC SCI requires 2-4 hour RTO (not chosen by business)
- Can design EU-only multi-region respecting MiFID II
- Can implement S3 Object Lock for immutable compliance audit trails
- Can calculate compliance cost and decide if business is worth it

## Spaced Repetition Plan

**Concepts Introduced**:
- Immutable audit requirements (will apply in Episode 14 security)

**Concepts Reinforced**:
- RTO/RPO from Episodes 1-2 (legally mandated, not chosen)
- Cost multipliers from Episode 9 (compliance costs even more)
- CAP consistency from Episode 10 (immutability vs availability tradeoff)

## Lesson Flow

### 1. Foundation Recall (1 min)

"In Episodes 1-12, you made technical decisions. Cost, complexity, capability. You chose your patterns.

But if you're in financial services, you don't get to choose. Regulators choose for you."

---

### 2. Learning Objectives (30 sec)

"By the end of this lesson:
- You'll understand SEC SCI mandates for exchanges
- You'll apply MiFID II data residency
- You'll implement crypto compliance requirements
- You'll know when to say no to regulatory demands"

---

### 3. SEC Regulation SCI (3 min)

**Teaching Approach**: Regulatory requirement analysis

"SEC stands for Securities and Exchange Commission. SCI stands for Systems Compliance and Integrity. Applies to stock exchanges, clearinghouses, alternative trading systems.

Requires: RTO and RPO for critical systems. Not aspirational. Documented, tested, reported to SEC."

**Typical Requirements**:
"RTO for trading systems: 2-4 hours (not the 5 minutes you might choose).
RPO for trade data: Near-zero. Every executed trade must recover.

This immediately dictates architecture: Aurora only (ACID). No eventual consistency databases for transactions."

**Real Example**:
"US stock exchange, hot-warm architecture. Primary US-EAST-1, secondary US-WEST-2.
- Aurora Global Database for trade ledger (synchronous, ACID)
- 30% secondary capacity (cheaper than hot-hot)
- Route53 health checks + manual failover (SEC expects human oversight)
- Quarterly DR testing (mandatory, documented, submitted to SEC)

Cost: $3M annually just for multi-region. Alternative: Potential SEC enforcement, trading halts, market maker defection. Multi-region isn't optional."

**Key Insight**:
"Compliance isn't cost-benefit analysis. It's cost-of-doing-business. Regulators have decided your RTO/RPO."

---

### 4. MiFID II Data Residency (2-3 min)

**Teaching Approach**: Architectural constraint

"MiFID II: Markets in Financial Instruments Directive II. EU regulation.

Critical requirement: Trade data from EU customers must stay in EU. Cannot transfer to US without adequacy decision."

**Architectural Implication**:
"Can't do global multi-region. Must be EU-only multi-region.
- Primary EU-WEST-1
- Secondary EU-CENTRAL-1
- NO US regions for trade data

Alternative: Separate data handling for EU vs US customers. Expensive. Complex."

**Technical Enforcement**:
"S3 bucket policy denying PutObject outside EU regions. AWS Organizations SCP preventing cross-region replication. Technical enforcement of regulatory requirement."

**Real Cost**:
"EU instance pricing 15% higher than US. EU-only multi-region costs extra $200K annually vs US+EU option.

But alternative: €10M fine or 4% annual turnover. They paid the $200K."

**Data Retention**:
"7 years of queryable transaction reporting. S3 Intelligent Tiering with retrieval SLA. When regulators request data, you have days not weeks to produce."

---

### 5. Crypto Compliance: BitLicense & MiCA (2 min)

**Teaching Approach**: Emerging regulations

"NY BitLicense: State-level custody license. Requires cybersecurity program including DR.

EU MiCA: Pan-European regulation for crypto-assets. Operational resilience requirements. Proportionate DR."

**BitLicense Requirements**:
"RTO/RPO not strictly mandated. But industry standard: hot-warm minimum (4-hour RTO). For high-value custody: hot-hot.

Transaction monitoring: Immutable audit trails. Fraud detection. AML compliance."

**Immutable Implementation**:
"S3 with Object Lock (compliance mode). Once written, cannot be deleted even by root account. 7-year retention minimum.

CloudTrail logs. Application logs. Every wallet operation. Immutable and queryable by regulators."

**Real Example**:
"Crypto exchange with BitLicense:
- Hot-warm architecture: $1.2M infrastructure
- Compliance staff: $800K annually
- Audit costs: $200K
- Total: $2.2M annually

Is the business worth it? For a crypto exchange with $100M asset under custody: Yes. For a smaller platform: Probably not."

**MiCA Emerging Requirements**:
"Stablecoin issuers: Likely hot-hot (systemic importance).
Smaller platforms: Hot-warm with documented RTO acceptable.

GDPR applies: EU customer data stays in EU (like MiFID II)."

---

### 6. Compliance as Architecture Driver (1 min)

**Teaching Approach**: Tradeoff analysis

"In Chapters 1-12, complexity was cost. Capability required more complexity.

In compliance, capability is mandatory. Complexity doesn't matter. Cost doesn't matter.

SEC says 4-hour RTO: You build 4-hour RTO even if hot-warm costs 3x single-region.

MiFID II says EU-only: You design EU-only even though global would be cheaper.

Crypto compliance says immutable: You implement S3 Object Lock even though database would be simpler."

---

### 7. Integration with Ecosystem (1 min)

"Compliance requirements affect:
- Data architecture (ACID vs eventual consistency)
- Region selection (EU only vs global)
- Audit logging (immutable vs deletable)
- Testing (quarterly mandatory vs GameDays)

Design entire architecture assuming compliance requirements from day one."

---

### 8. Mastery Checkpoint (1 min)

"Self-assessment:
- Can you explain why SEC SCI mandates 2-4 hour RTO instead of 30 seconds?
- Can you design EU-only multi-region?
- Can you implement immutable audit logging?
- Can you identify when compliance makes business unviable?"

---

### 9. Next Steps & Conclusion (1 min)

"If you're in regulated industry: Compliance comes first. Architecture follows compliance requirements. This is non-negotiable."

---

## Quality Checklist

- [x] SEC SCI requirements specific
- [x] MiFID II data residency explained
- [x] Crypto compliance detailed
- [x] Real company examples with costs
- [x] Technical implementation (S3 Object Lock, SCP)
- [x] Compliance as architecture driver
- [x] Integration with ecosystem
- [x] Mastery checkpoint included
