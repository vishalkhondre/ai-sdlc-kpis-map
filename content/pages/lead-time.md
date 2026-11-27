---
id: lead-time
type: metric
band: flow
title: Lead time for changes
title_accent: Lead time
summary: How long a committed change takes to reach production.
formula: "median( production deploy time − commit time )"
unit: hours or days
related: [deployment-frequency, change-failure-rate, recovery-time, cycle-time, review-time]
sources: []
sample: true
---

Lead time for changes is the time a code change takes to go from being committed to running in
production. A short lead time means the organisation can respond to customers quickly and cheaply.

## Definition

The elapsed time from the commit of a change to its successful deployment in production, counted
for every change that reaches production in the period.

## Formula

{{formula}}

Report the median for the period, and the 75th percentile beside it so a long tail is visible.

## Why it matters

It shows how quickly the delivery system turns finished work into something customers can use.
Leaders use it with deployment frequency to judge throughput.

## How to measure

{{figure:lead-time-span}}

Join two events by change identifier: the commit timestamp from version control and the
production deployment timestamp from the deployment pipeline.

## How AI changes it

AI assistance can shorten the time spent writing a change while queues for review and testing grow.
Read lead time with review time and change size, so a faster coding stage is not mistaken for a
faster system.

## Pitfalls

- Counting only the fast path, such as excluding changes that waited for a release window.
- Splitting work into very small commits to lower the number without changing the flow.

## Related

## Sources
