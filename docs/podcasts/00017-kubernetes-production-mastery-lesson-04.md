---
displayed_sidebar: tutorialSidebar
hide_table_of_contents: false
sidebar_label: "📖 #017: K8s Lesson 4 - Troubleshooting"
slug: 00017-kubernetes-production-mastery-lesson-04
---

# Lesson 4: Troubleshooting Crashes - CrashLoopBackOff & Beyond

## Kubernetes Production Mastery Course

<GitHubButtons />

**Course**: [Kubernetes Production Mastery](/courses/kubernetes-production-mastery)
**Episode**: 4 of 10
**Duration**: 15 minutes
**Target Audience**: Senior platform engineers, SREs, DevOps engineers with 5+ years experience

## Learning Objectives

By the end of this lesson, you'll be able to:
- Execute systematic troubleshooting workflow for pod failures (describe → logs → events)
- Diagnose CrashLoopBackOff, ImagePullBackOff, and Pending states
- Configure effective health checks (liveness and readiness probes) that prevent false failures

## Prerequisites

- [Lesson 1: Production Mindset](/courses/kubernetes-production-mastery/lesson-01)
- [Lesson 2: Resource Management](/courses/kubernetes-production-mastery/lesson-02)
- [Lesson 3: Security Foundations](/courses/kubernetes-production-mastery/lesson-03)

---

## Video Lesson

<iframe width="560" height="315" src="https://www.youtube.com/embed/5iVIU6dpc5QY" title="Kubernetes Troubleshooting - CrashLoopBackOff & Beyond" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

**Watch on YouTube**: [Kubernetes Troubleshooting - CrashLoopBackOff & Beyond](https://youtu.be/5iVIU6dpc5QY)

---

## Topics Covered

### The Systematic Troubleshooting Workflow
- kubectl describe → logs → events workflow
- Building team runbooks for common failures

### CrashLoopBackOff Deep Dive
- Application crashes vs infrastructure issues
- Exit codes (137 = OOMKilled, 1 = app error)
- Understanding backoff delay patterns

### ImagePullBackOff
- Registry authentication issues
- Image not found and tag problems
- Common registry misconfigurations

### Pending Pods
- Scheduling failures and resource constraints
- Node selectors and affinity rules
- Diagnosing why pods won't schedule

### Health Checks That Actually Work
- **Liveness probes**: Restart unhealthy containers
- **Readiness probes**: Remove from load balancer when not ready
- **Startup probes**: Handle slow-starting applications
- Common mistakes: aggressive timeouts, wrong endpoints

---

## Navigation

⬅️ **Previous**: [Lesson 3: Security Foundations](/courses/kubernetes-production-mastery/lesson-03) | **Next**: Lesson 5 (Coming Soon) ➡️

📚 **[Back to Course Overview](/courses/kubernetes-production-mastery)**
