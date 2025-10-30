---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 Lesson 06"
slug: courses/multi-region-mastery/lesson-06
---

# Lesson 06: DynamoDB Global Tables: Active-Active Replication

## Multi-Region Platform Engineering: AWS, Kubernetes, and Aurora at Scale

**Episode 06 of 16** | **Duration:** 15 minutes

**Target Audience:** Senior platform engineers, SREs, DevOps engineers (5+ years experience)

---

## 🎥 Watch This Lesson

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, margin: '1.5rem 0'}}>
  <iframe
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/Eud5O-8n3ZQ"
    title="Lesson 06: DynamoDB Global Tables: Active-Active Replication"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>

---

## What You'll Learn

- **DynamoDB Global Tables architecture**: Active-active writes, eventually consistent, sub-second replication
- **Conflict resolution strategies**: Last-writer-wins (LWW) default, version vectors, application-level resolution
- **Replication lag characteristics**: 1-3 seconds typical, can spike during regional issues
- **Cost analysis**: Write capacity units duplicated per region, on-demand pricing multiplier
- **Real-world use cases**: Session storage, user profiles, shopping carts work well; financial transactions require caution

---

## Navigation

[← Previous: Network Architecture](/podcasts/courses/multi-region-mastery/lesson-05) | [Back to Course](/podcasts/courses/multi-region-mastery) | [Next: Observability at Scale →](/podcasts/courses/multi-region-mastery/lesson-07)
