---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 Lesson 02"
slug: courses/multi-region-mastery/lesson-02
---

# Lesson 2: Production Patterns - Hot-Hot, Hot-Warm, Hot-Cold

## Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale

**Episode 2 of 16** | **Duration:** 16 minutes

**Target Audience:** Senior platform engineers, SREs, DevOps engineers (5+ years experience)

---

## 🎥 Watch This Lesson

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, margin: '1.5rem 0'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/9jFFU30ZgyU"
    title="Lesson 2: Production Patterns"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>

---

## What You'll Learn

- **RTO/RPO and cost trade-offs** for each pattern
- **Hot-warm**: 5-minute RTO, reasonable cost - the most common production pattern
- **Hot-hot**: Subsecond failover, 7.5x cost multiplier
- **Hot-cold**: 30+ minute RTO, 2x cost, acceptable for non-critical workloads
- **Pattern selection framework**: Match architecture to actual business downtime costs

## Key Takeaways

- Hot-hot architecture: Subsecond failover, 7.5x cost multiplier, requires active-active database writes
- Hot-warm architecture: 5-minute RTO, 3-4x cost, most common production pattern for pragmatic teams
- Hot-cold architecture: 30+ minute RTO, 2x cost, acceptable for non-critical workloads
- RTO vs RPO trade-offs: Understand Recovery Time Objective and Recovery Point Objective requirements
- Cost comparison: Real production numbers showing infrastructure spend across patterns
- Pattern selection framework: Match architecture to actual business downtime costs, not fear-driven design

---

## Navigation

[← Previous: Multi-Region Mental Model](/podcasts/courses/multi-region-mastery/lesson-01) | [Back to Course](/podcasts/courses/multi-region-mastery) | [Next: Aurora Global Database →](/podcasts/courses/multi-region-mastery/lesson-03)
