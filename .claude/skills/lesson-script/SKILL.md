---
name: Lesson Script
description: Convert approved lesson outline into engaging single-presenter script optimized for learning retention with teaching techniques, active recall, and spaced repetition.
allowed-tools: Read, Write, Glob
---

# Lesson Script

Convert an approved lesson outline into an engaging, pedagogically sound script for single-presenter educational content.

## When to Use This Skill

Use this skill when:
- User says: "Write lesson script", "Create course episode"
- An approved outline exists in `docs/podcasts/courses/[course-slug]/outlines/`
- User has reviewed and approved the lesson structure

**CRITICAL**: This skill MUST verify an outline exists before writing. Never write a script without an outline.

## Episode Requirements

### Voice & Persona

**Presenter**: Single instructor (fictional persona using Autonoe voice)

**Tone**:
- Conversational but authoritative
- Friendly and approachable
- Patient and clear
- Respectful of learner's intelligence

**Perspective**:
- Use "we" (inclusive: "we'll explore", "let's examine")
- Use "you" (direct address: "you'll be able to", "you might encounter")
- Use "I" sparingly (for personal anecdotes, opinions)

**Example Voice**:
```
"Today we're diving into Kubernetes Pods. Now, if you're like most engineers,
you might be wondering - why do we need Pods when we already have containers?
Great question. Let's explore that together.

By the end of this lesson, you'll understand not just WHAT Pods are,
but WHY they exist and WHEN you'd use different Pod patterns in production."
```

### Script Format

**No Intro/Outro in Script**: Like podcasts, intro/outro handled by separate audio files.

**DO**:
- ✅ Start with lesson content immediately
- ✅ State learning objectives early
- ✅ Include preview and recap
- ✅ End with next episode teaser

**DON'T**:
- ❌ Welcome messages ("Welcome to the course")
- ❌ Presenter introductions ("I'm...") in every episode
- ❌ Generic show descriptions
- ❌ Formal signoffs ("Thanks for listening")

### Duration

- **Target**: 15 minutes
- **Acceptable range**: 12-18 minutes
- **Word count**: ~2000-2400 words (160 words/min speaking pace)

## Teaching Techniques

### 1. Signposting

**Purpose**: Help learners know where they are in the lesson

**Application**:
```
Opening: "In this lesson, we'll cover three key concepts: X, Y, and Z."

Transition: "Now that we understand X, let's move on to Y."

Mid-lesson: "We're halfway through. So far we've covered X and Y.
             Next up is Z, which ties everything together."

Closing: "We covered X, Y, and Z. Next time, we'll build on Z to explore W."
```

**Script Example**:
```
"Let's break this down into three parts.

First, we'll explore the mental model - why Pods exist.

Second, we'll look at how Pods work internally.

And third, we'll examine real-world Pod patterns you'll use in production.

Let's start with the mental model..."
```

### 2. Analogies & Metaphors

**Purpose**: Connect new concepts to familiar ideas

**Guidelines**:
- Choose analogies from learner's experience (not esoteric)
- Extend the analogy but acknowledge limitations
- Use consistently across episodes

**Script Example**:
```
"Think of a Kubernetes Pod like a shipping container - but for applications.

Just as shipping containers standardize how we transport goods,
Pods standardize how we deploy applications.

The container doesn't care what's inside - furniture, electronics, food -
it provides a consistent interface for moving things around the world.

Similarly, a Pod doesn't care if you're running Python, Go, or Java -
it provides a consistent interface for Kubernetes to manage your application.

Now, where this analogy breaks down is...
[explain limitation]

But the core idea holds: Pods are the atomic unit of deployment."
```

### 3. Elaboration (Multiple Explanations)

**Purpose**: Say the same thing different ways to reach different learning styles

**Application**:
```
Initial: [Technical explanation]
Rephrased: "In other words..."
Analogy: "Think of it like..."
Example: "For instance, if you're..."
Summary: "To put it simply..."
```

**Script Example**:
```
"A Deployment manages the lifecycle of Pods.

In other words, instead of manually creating and deleting Pods,
you declare the desired state and the Deployment handles the rest.

Think of it like a thermostat. You set the desired temperature -
that's your declaration. The thermostat handles the actual work
of turning heat on and off to maintain that state.

For instance, if you declare 'I want 5 Pods running,' the Deployment
will create 5 Pods. If one crashes, it automatically creates a replacement.

To put it simply: Deployments let you describe what you want,
and Kubernetes figures out how to make it happen."
```

### 4. Think-Alouds (Expert Modeling)

**Purpose**: Model how experienced engineers think through problems

**Application**:
```
"Here's how I think through this problem:

First, I'd check X because [reasoning].
Then, I'd look at Y to confirm [hypothesis].
If Z shows [pattern], that tells me [conclusion].
Finally, I'd validate by [verification step]."
```

**Script Example**:
```
"Let's say your Pod keeps crashing. Here's how I'd debug this:

First, I'd run kubectl describe pod [name] to see the events.
Why? Because it shows me what Kubernetes tried to do and what failed.

Next, I'd check the container logs with kubectl logs.
This tells me if the application itself is erroring.

If the logs show nothing, that's actually a clue -
it means the container might be failing before your app even starts.
Maybe the image doesn't exist or there's a configuration problem.

Then I'd look at the restart count. If it's restarting rapidly,
we're in CrashLoopBackOff, which means Kubernetes is backing off
on restart attempts. That's actually helpful - it's giving you time to debug.

This is the thought process: events, logs, restart behavior.
In that order. Each step narrows down the problem."
```

### 5. Pause Points (Active Learning)

**Purpose**: Give learners time to think and practice

**Application**:
```
Introduce challenge:
"Before I show you the solution, pause and think..."

[3-5 second pause in audio]

Provide solution:
"Here's how I'd approach it..."

Explain reasoning:
"The reason this works is..."
```

**Script Example**:
```
"Now it's your turn. Before we continue, pause the audio and answer this:

If you need to run a database in Kubernetes, what kind of Pod pattern
would you use? A single-container Pod? Or a multi-container Pod?

Think about what a database needs. Think about the responsibilities.

[Pause 5 seconds]

Okay, here's what I'd recommend: A multi-container Pod.

Why? Because databases often need sidecar containers for things like:
- Backup agents
- Monitoring exporters
- Log shipping

By using a multi-container Pod, these supporting processes share
the same lifecycle as the database. When the Pod starts, everything starts.
When it scales, everything scales together.

This is a common pattern you'll see in production."
```

### 6. Spaced Repetition (Callbacks)

**Purpose**: Reinforce key concepts across episodes

**Application**:
```
Episode N:
"Remember in Episode X when we learned about [concept]?
That becomes critical here because..."

"This builds directly on the [concept] we covered last time..."

"You'll see this pattern again when we explore [future topic] in Episode Y..."
```

**Script Example**:
```
"Remember back in Episode 2 when we talked about the Pod mental model -
that Pods are the atomic unit of deployment?

This is where that concept becomes crucial.

Because Deployments don't manage containers - they manage PODS.
The abstraction layer we established in Episode 2 is what makes
Deployments so powerful.

You'll see this pattern continue when we cover Services next week -
they also target Pods, not individual containers."
```

### 7. Active Recall Prompts

**Purpose**: Strengthen memory through retrieval practice

**Application**:
```
Before explaining:
"Before we continue, try to recall from Episode X..."

Mid-lesson check:
"Quick check: Can you remember what [term] means?"

End-of-lesson:
"Without looking back, can you list the three key differences between X and Y?"
```

**Script Example**:
```
"Before we dive into Services, let's do a quick recall from last episode.

Without scrolling back, try to remember: What are the three main components
of a Deployment?

[Pause 3 seconds]

They are: replicas, selector, and template.

If you got those, excellent - your retention is strong.
If not, that's totally fine - that's why we review.

Replicas define how many Pods you want, selector tells the Deployment
which Pods it manages, and template specifies what those Pods look like.

Now, let's see how Services build on this foundation..."
```

## Script Structure

### Opening (First 2 minutes)

```
[HOOK - Compelling start]
[Specific problem, surprising fact, or relatable scenario]

[CONTEXT]
"This is lesson [N] in our [Course Name] series."
[If Episode 2+: Brief recall of previous episode]

[LEARNING OBJECTIVES]
"By the end of this lesson, you'll be able to:
- [Objective 1]
- [Objective 2]
- [Objective 3]"

[PREVIEW]
"We'll cover three main areas:
First, [topic 1].
Second, [topic 2].
And finally, [topic 3]."

[PREREQUISITES - if applicable]
"Before we dive in, make sure you're comfortable with [prerequisite].
If you need a refresher, check out Episode [X]."

Let's get started.
```

### Main Content (10-12 minutes)

Follow the outline structure, typically 3-5 major sections.

**For Each Section**:
```
[SECTION INTRODUCTION]
"Now let's talk about [topic]."

[TEACHING CONTENT]
- Use multiple explanation styles (technical, analogy, example)
- Include signposting ("First... Second... Finally...")
- Add think-alouds where appropriate
- Insert pause points for practice

[TRANSITION]
"Now that we understand [X], let's see how it connects to [Y]."
```

### Closing (Last 2-3 minutes)

```
[ACTIVE RECALL CHECKPOINT]
"Before we wrap up, let's test your understanding.
[2-3 retrieval questions with pauses and answers]"

[RECAP]
"Let's recap what we covered today:
1. [Key point 1]
2. [Key point 2]
3. [Key point 3]
4. [Key point 4]
5. [Key point 5]"

[INTEGRATION]
"This builds on [previous concept from Episode X], and you'll use this
foundation when we cover [future topic in Episode Y]."

[NEXT EPISODE PREVIEW]
"Next time, we're exploring [next topic].

You'll learn how to [preview specific skills/knowledge].

This is going to be particularly useful when [practical benefit].

See you in the next lesson!"
```

## Script Format

**File location**: `docs/podcasts/courses/[course-slug]/scripts/lesson-[NN].txt`

**Format**:
```
[No speaker label for single presenter - just content]

Today we're diving into Kubernetes Pods. If you're like most engineers,
you've probably wondered why we need Pods when we already have containers.

[No dialogue markers, just natural flow]

Let's start with the mental model. Think of a Pod like...

[Continue naturally]
```

**CRITICAL**:
- No speaker names (single presenter)
- Natural paragraph breaks
- Write WITHOUT SSML/pronunciation tags (added later)
- No stage directions
- Write as spoken (contractions, natural language)

## Episode Numbering

**Determine lesson number**:
1. Check curriculum-plan.md for episode position
2. Use format: `lesson-01.txt`, `lesson-02.txt`, etc.
3. Two-digit padding (01-09, 10-99)

## Content Guidelines

### Natural Speaking Patterns

**DO**:
```
"Here's the thing about Pods - they're actually pretty simple once you
get the mental model.

Let's break it down.

First, think about what a container gives you. It's a process with
isolated resources, right? Its own filesystem, network namespace,
all that good stuff.

Now, what if you need two processes that share some of those resources?
Maybe they need to share a filesystem volume. Or communicate over localhost.

That's where Pods come in."
```

**DON'T**:
```
"Pods are Kubernetes' smallest deployable unit. They encapsulate
one or more containers with shared storage and network resources,
and a specification for how to run the containers. The Pod abstraction
provides a way to manage groups of containers as a single unit."

[Too formal, sounds like documentation]
```

### Technical Depth

**Appropriate for Senior Engineers**:
- Don't explain basic concepts they know (containers, Linux, YAML)
- DO explain Kubernetes-specific concepts (even if "basic")
- Focus on production implications and trade-offs
- Include edge cases and gotchas
- Provide decision frameworks

**Example**:
```
"You already know what resource limits do - they prevent a container
from eating all the CPU or memory on a node.

But here's the gotcha that trips up even experienced engineers:
resource requests and limits interact with the scheduler in non-obvious ways.

If you set requests too low, you'll get overcommitted nodes and noisy neighbors.
Set them too high, and you're wasting resources - paying for capacity you don't use.

Here's how I think about it in production..."
[Provide decision framework]
```

### Voice Consistency

**Maintain Throughout**:
- Conversational but professional
- Helpful, not condescending
- Acknowledges complexity honestly
- Shares practical experience
- Admits when things are confusing/hard

**Example Phrases**:
- "You might be wondering..."
- "Here's where it gets interesting..."
- "This trips up a lot of engineers..."
- "In production, you'll find..."
- "Let's be honest..."
- "The docs don't mention this, but..."

## Quality Checklist

Before finalizing script:

**Structure**:
- [ ] Follows outline's section structure
- [ ] Clear beginning, middle, end
- [ ] Signposting throughout
- [ ] Smooth transitions between sections
- [ ] Proper time allocation (~15 min total)

**Teaching Techniques**:
- [ ] At least 2 analogies or metaphors
- [ ] Multiple explanation styles (elaboration)
- [ ] 1-2 think-aloud sections
- [ ] 2-3 pause points for practice
- [ ] Spaced repetition callbacks (if Episode 2+)
- [ ] Active recall prompts in recap

**Content**:
- [ ] Learning objectives clearly addressed
- [ ] Technical accuracy (will verify in validation)
- [ ] Production-relevant examples
- [ ] Common pitfalls mentioned
- [ ] Decision frameworks provided
- [ ] Appropriate depth for audience

**Voice**:
- [ ] Conversational and natural
- [ ] Consistent use of "we"/"you"
- [ ] No formal lecture tone
- [ ] Personal touches (experiences, opinions)
- [ ] Respectful of learner intelligence

**Learning Science**:
- [ ] Spaced repetition applied
- [ ] Active recall moments
- [ ] Progressive complexity
- [ ] Concrete before abstract
- [ ] Multiple modalities (verbal + examples)

**Format**:
- [ ] No speaker labels (single presenter)
- [ ] Natural speaking style
- [ ] No SSML tags (added later)
- [ ] Proper file naming (lesson-NN.txt)
- [ ] ~2000-2400 words

## Example Opening (Good vs Bad)

### ✅ GOOD

```
Welcome to Episode 3 of Kubernetes Fundamentals. Today we're tackling one
of the most misunderstood concepts in Kubernetes: Deployments.

Now, if you've been following along from Episodes 1 and 2, you understand
Pods - they're the atomic unit of deployment. But here's the problem:
Pods are mortal. They die. And when they do, they're gone forever.

So how do you keep your application running when Pods inevitably fail?
How do you scale up from 1 Pod to 100? How do you update your application
without downtime?

That's where Deployments come in.

By the end of this lesson, you'll understand how Deployments manage Pod
lifecycles, how to declare your desired state, and how to perform zero-downtime
rollouts in production.

We'll cover three key areas: First, the declarative model and why it matters.
Second, how Deployments handle failures and scaling. And third, production
rollout strategies you'll actually use.

Let's dive in.
```

### ❌ BAD

```
Hello and welcome to the Kubernetes Fundamentals course. This is Episode 3.

Today's topic is Deployments. Deployments are a Kubernetes resource that
provides declarative updates for Pods and ReplicaSets. They are one of the
most commonly used workload resources in Kubernetes.

The objectives for today's lesson are to understand what Deployments are,
how they work, and when to use them.

Let us begin by defining what a Deployment is.
```

[Too formal, no hook, reads like documentation, no personality]

## Example Section (Teaching Technique Application)

```
Alright, let's talk about the declarative model - because this is THE
fundamental shift in how you think about infrastructure with Kubernetes.

In traditional operations, you tell the system WHAT TO DO. "Start this server.
Copy this file. Run this command." That's imperative. You're giving orders.

In Kubernetes, you tell the system WHAT YOU WANT. "I want 5 Pods running this
application." That's declarative. You're stating desired state.

Think of it like a thermostat. [ANALOGY]

With an imperative approach, you'd constantly monitor the temperature and
manually turn the heat on and off. "It's 65 degrees. Turn on the heat.
Now it's 72. Turn off the heat."

With a declarative approach, you set the thermostat to 70 and walk away.
The thermostat monitors the temperature and adjusts automatically to maintain
your desired state.

Deployments work the same way.

You declare: "I want 5 Pods running my app." Kubernetes sees that only 3 exist,
so it creates 2 more. One Pod crashes? Kubernetes immediately creates a replacement.
You update the Deployment to 10 Pods? Kubernetes creates 5 more.

You're not micromanaging. You're declaring intent.

Now, here's where this gets really powerful in production. [TRANSITION]

[Continue with production implications...]

Before we move on, pause and think about a time you manually scaled an application.
[PAUSE POINT] How many steps were involved? SSH into servers, update config files,
restart processes, check that everything came up?

With Deployments, that becomes one command: kubectl scale deployment my-app --replicas=10.

Kubernetes handles the rest. That's the power of declarative infrastructure.

[SIGNPOST] We've covered the declarative model. Next, let's look at how Deployments
handle failures...
```

---

## Instructions for Claude

When this skill is invoked:

1. **Verify outline exists**:
   ```bash
   ls -la docs/podcasts/courses/[course-slug]/outlines/
   ```
   If no outline, STOP and tell user to create outline first with lesson-outline skill.

2. **Read the outline carefully**:
   - Learning objectives
   - Section structure and flow
   - Spaced repetition plan
   - Analogies and examples planned
   - Teaching techniques specified

3. **Determine lesson number**:
   - Check curriculum-plan.md for episode position
   - Use lesson-NN.txt format

4. **Write script section by section**:
   - Follow outline structure
   - Apply teaching techniques (signposting, analogies, think-alouds, pause points)
   - Include spaced repetition callbacks
   - Add active recall moments
   - Use natural, conversational language

5. **Maintain voice consistency**:
   - Single presenter (no dialogue)
   - Conversational but authoritative
   - Use "we" and "you"
   - Personal touches and experiences

6. **Validate against checklist** (all items)

7. **Save to correct location**:
   `docs/podcasts/courses/[course-slug]/scripts/lesson-NN.txt`

8. **Report to user**:
   - Lesson number and filename
   - Estimated duration
   - Teaching techniques used
   - Next step: Use lesson-validate skill to fact-check

**Remember**: The outline is your blueprint. Your job is to bring it to life with
engaging, pedagogically sound narration that maximizes learning retention.

You're not just conveying information - you're teaching. Every word should serve
the learning objectives.
