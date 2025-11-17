---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 Lesson 01"
slug: /courses/multi-region-mastery/lesson-01
---

# Lesson 1: The Multi-Region Mental Model

## Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale

**Episode 1 of 16** | **Duration:** 15 minutes

**Target Audience:** Senior platform engineers, SREs, DevOps engineers (5+ years experience)

---

## 🎥 Watch This Lesson

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, margin: '1.5rem 0'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/LsUXhND86Rw"
    title="Lesson 1: The Multi-Region Mental Model"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>

---

## What You'll Learn

- **Cost, Complexity, Capability (CCC) Triangle** mental model - the fundamental trade-offs
- **True cost multiplier**: 2.5x-7.5x (not the 2x vendors claim)
- **Single Points of Failure** in "multi-region" AWS architectures that can bring down your entire system
- **Decision framework**: Calculate actual downtime cost vs multi-region premium
- **Hidden costs**: Engineering time (500-1000 hours implementation) plus ongoing operational complexity

## Key Takeaways

- Multi-region costs 2.5-7.5x more (not 2x): Data transfer is the silent killer at $0.02/GB
- The Cost-Complexity-Capability triangle: You can optimize for two vertices, never all three
- Hidden SPOFs exist even in multi-region: Route53, IAM, ACM all depend on US-EAST-1 control planes
- 80% of companies don't need multi-region: Do the math—$10M revenue = $1,140/hour downtime cost
- Engineering time is the largest hidden cost
- Decision framework: Calculate actual downtime cost vs multi-region premium to know if it's worth it

---

## Navigation

[← Back to Course Overview](/courses/multi-region-mastery) | [Next Lesson: Production Patterns →](/courses/multi-region-mastery/lesson-02)
