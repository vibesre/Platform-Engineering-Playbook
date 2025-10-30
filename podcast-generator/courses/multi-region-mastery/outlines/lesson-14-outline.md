# Lesson Outline: Episode 14 - Security Architecture: Cross-Region Encryption & Key Management

## Metadata
**Course**: Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale
**Episode**: 14 of 16
**Duration**: 15 minutes
**Episode Type**: Advanced
**Prerequisites**: Episodes 1-13
**Template Used**: Template 4 (Advanced)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. Design encryption strategy for multi-region data (at-rest, in-transit, in-use)
2. Implement KMS key management across regions
3. Handle key rotation and key compromise in multi-region
4. Identify security attack surfaces introduced by multi-region

Success criteria:
- Can design encryption architecture for at-rest, in-transit, in-use data
- Can implement KMS regional keys with fallback
- Can execute key rotation without downtime
- Can identify 5+ new attack surfaces from multi-region

## Spaced Repetition Plan

**Concepts Introduced**:
- Multi-region security posture (applies to Episode 15 anti-patterns)

**Concepts Reinforced**:
- Network security from Episode 5 (encryption in-transit)
- Compliance from Episode 13 (key retention requirements)

## Lesson Flow

### 1. Foundation Recall (1 min)

"You've built reliable multi-region. Now: How do you keep it secure?

Multi-region introduces 3x more attack surfaces. Keys replicated across regions. Data exposed in two places. Audit trails in multiple locations.

Today: Security architecture for multi-region."

---

### 2. Learning Objectives (30 sec)

"By the end of this lesson:
- You'll encrypt data at-rest, in-transit, in-use
- You'll manage keys across regions safely
- You'll rotate keys without downtime
- You'll identify security risks specific to multi-region"

---

### 3. Encryption at Rest (2 min)

**Teaching Approach**: AWS KMS architecture

"Data encrypted with customer-managed KMS keys (not AWS-managed).

Challenge: KMS is regional. US-EAST-1 key can't directly decrypt data in US-WEST-2.

Solution: Replicate data encrypted with primary region key, decrypt in secondary using replicated key material."

**Aurora Encryption**:
"Primary uses US-EAST-1 KMS key. Secondary replicates encrypted data. Secondary region has replica KMS key that can decrypt.

When failover happens: Secondary becomes primary using replica key."

**DynamoDB Global Tables**:
"Both regions use their own KMS keys. Item encrypted in US-EAST-1 with us-east-1-key, replicated as encrypted item, decrypted in US-WEST-2 with us-west-2-key."

**S3 Replication**:
"Source bucket encrypted with source key. Destination bucket encrypted with destination key. S3 handles encryption during transfer."

---

### 4. Encryption In-Transit (1-2 min)

**Teaching Approach**: Network security

"Data moving between regions must be encrypted. TLS 1.2+ minimum.

Transit Gateway: Encrypted by default between regions.
Data Transfer: AWS backbone automatically encrypted.
RDS replication: Encrypted within AWS network.

But: Between on-premises and AWS, or different cloud providers: Configure IPsec/TLS explicitly."

---

### 5. Key Management Across Regions (2 min)

**Teaching Approach**: Key operations

"Create primary key in US-EAST-1. Replicate to US-WEST-2.

Replicated key can decrypt data but cannot be used for new encryption. This prevents accidental encryption with wrong region's key."

**Key Rotation**:
"Rotate primary key in US-EAST-1. New key version created.
Replication updates US-WEST-2 copy to new version.
All new encryptions use new key version automatically."

**Key Compromise**:
"If US-EAST-1 key compromised: Disable it. Decrypt all affected data. Re-encrypt with new key. Cost: Hours of decryption, re-encryption, audit."

---

### 6. Attack Surfaces Introduced by Multi-Region (2 min)

**Teaching Approach**: Risk identification

"1. Key replication: Keys in transit between regions (mitigated by AWS backbone encryption)

2. Multiple endpoints: More places attackers can target. Region-specific RDS, DynamoDB, S3.

3. Cross-region networking: Transit Gateway as attractive target.

4. Compliance/audit logs: Attackers might target audit trail in secondary region to hide evidence.

5. Failover procedures: During manual failover, operator might accidentally expose keys/credentials."

**Mitigation**:
"- Immutable audit logging (Episode 13)
- Encryption everywhere (at-rest, in-transit, in-use)
- Secrets management (no credentials in code/config)
- Network segmentation (Transit Gateway with tight security groups)
- Least privilege IAM across regions"

---

### 7. Real Production Example (1-2 min)

"Financial services: Multi-region with EU + US data.

EU data encrypted with EU-only key (compliant).
US data encrypted with US key.
Both replicated with replica keys.

Key rotation: Annual, documented for audit.
Key compromise: Never happened, but runbook prepared (hours to revoke + re-encrypt all EU data).

Cost: KMS replication, audit logging, key management infrastructure = $50K annually."

---

### 8. Mastery Checkpoint (1 min)

"Can you:
- Design encryption for at-rest, in-transit, in-use data?
- Explain why KMS key can be replicated but replica can't encrypt?
- Handle key compromise without downtime?
- Identify 3+ attack surfaces specific to multi-region?"

---

### 9. Next Episode Preview (30 sec)

"Next: Episode 15 - Anti-Patterns: What Breaks Multi-Region in Production.

We've covered how to build correctly. Now: The ways it breaks. Real production disasters and what caused them."

---

## Quality Checklist

- [x] Encryption at-rest, in-transit, in-use
- [x] KMS architecture specific
- [x] Key rotation and compromise scenarios
- [x] Security attack surfaces identified
- [x] Real production example
- [x] Cost considerations
- [x] Compliance integration
