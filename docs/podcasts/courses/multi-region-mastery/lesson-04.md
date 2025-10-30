---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 Lesson 04"
slug: courses/multi-region-mastery/lesson-04
---

# Lesson 04: Kubernetes Multi-Cluster Architecture

## Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale

**Episode 04 of 16** | **Duration:** 18 minutes

**Target Audience:** Senior platform engineers, SREs, DevOps engineers (5+ years experience)

---

## 🎥 Watch This Lesson

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, margin: '1.5rem 0'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/Pra-pXNlMu8"
    title="Lesson 04: Kubernetes Multi-Cluster Architecture"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>

---

## What You'll Learn

- **EKS control plane regional boundaries**: Each cluster is isolated, not replicated across regions
- **Why Kubernetes Federation failed**: Added complexity without solving data consistency or failover
- **Independent cluster pattern**: Run separate clusters per region, treat them as cattle not pets
- **Cross-cluster service discovery**: DNS-based (external-dns) vs service mesh (Istio) trade-offs
- **Cost reality**: N clusters = N control planes, multiplicative infrastructure costs

---

## Navigation

[← Previous: Aurora Global Database](/podcasts/courses/multi-region-mastery/lesson-03) | [Back to Course](/podcasts/courses/multi-region-mastery) | [Next: Network Architecture →](/podcasts/courses/multi-region-mastery/lesson-05)
