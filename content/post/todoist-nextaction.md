---
categories:
- post
date: 2017-04-06T17:41:28+08:00
draft: false
image: null
math: true
summary: Using nextaction-rs, you can now mimic Omnifocus or MLO's nextactin behavior in todoist!
tags: 
  - todoist
  - gtd
  - nextaction
  - omnifocus
title: Implementing nextaction in todoist
---

If you are a fan of MLO or Omnifocus, I bet you will really miss the nextaction feature if you migrate to todoist. With nextaction, one can keep really focus on 
things he should do, which is really nice. But since Todoist hasn't provided this feature(maybe they don't want this forever), we need to exploit the todoist api to achieve our goal.

Inspired by (here)[https://github.com/akramer/NextAction], implementing by a polling server is a trivial but decent way. Rather than using python, I chose to write it in Rust. The rationale behind is that it should be a simple 
application with as less as possible dependencies, not python with lots of redundant libraries. And you can see after that the compiled docker image is only 18M which is much easier to distribute (Actually I'm considering 
a "nextaction as a service", a.k.a. naas).

# Usage
## Simple run
You should set environment variable `NXTT_token` to your todoist token.

To build the application, (rust)[`rustup.rs`] is needed.
Run: `git clone && cargo run --release`

## Docker Image
A docker image is also available. Run it by `docker run -it -e NXTT_token=<your todoist token> wooya/nextaction`

# Introduction
> copy pasted from the README

## @nextaction
Nextaction will auto tag current `nextaction` task with `@nextaction`. It also supports parallel task (with '-' append)
and sequential task (with ':' append).

e.g.
```
|-taskA:
    |-taskB  // This task will be tagged @nextaction
    |-taskC:
        |-taskD
```
after you complete taskB, it will become
```
|-taskA:
    |-taskC:
        |-taskD // This task will be tagged @nextaction
```
And for parallel tasks:
```
|-taskA-
    |-taskB // This task will be tagged @nextaction
    |-taskC // This task will also be tagged @nextaction
```

So that you can add a filter on @nextaction to make you focused.

Parallel tasks and sequential tasks can corporate with each other seamlessly:
```
|-taskA-
    |-taskB:
    |   |-taskC // This task will be tagged @nextaction
    |   |-taskD
    |-taskE // This task will be tagged @nextaction
```

## @someday
Nextaction also supports a tag called `@someday`. The logic is:
when Nextaction meets a task which should be tagged `@nextaction`
but currently has tag `@someday`, it won't tag `@nextaction` to that task.
So that your someday tasks won't show up on your nextaction list.

So, don't hesitate to deploy a nextaction server and let's call it a day!