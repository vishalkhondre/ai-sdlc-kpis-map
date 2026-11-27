---
id: frameworks
type: reference
title: Frameworks behind the metrics
title_accent: Frameworks
summary: Where the metrics on this map come from, and how the main measurement frameworks relate.
sources: [dora-guide, space-acm, dx-core4, orgsignals-docs, aws-aidlc-intro, aws-cts-sw]
---

Most metrics on this map come from a handful of public frameworks. Each answers a different question,
so organisations usually combine them rather than pick one. This page shows what each framework
measures and which metrics on the map it supplies.

## DORA

DORA (DevOps Research and Assessment) defines five software delivery metrics. Three measure
throughput (change lead time, deployment frequency and failed deployment recovery time) and two
measure instability (change failure rate, which DORA calls change fail rate, and deployment rework rate). They are the base of the delivery
flow and stability groups on the map.

{{metrics:DORA}}

## SPACE

SPACE describes developer productivity across five dimensions: satisfaction and well-being,
performance, activity, communication and collaboration, and efficiency and flow. It is a way of
choosing a balanced set of measures across several dimensions, not a fixed list of metrics. That idea
of balance is why every metric page here names the metrics to read with it.

## DX Core 4

The DX Core 4 brings together DORA, SPACE and developer-experience research in four dimensions: speed,
effectiveness, quality and business impact. On this map it supplies
[pull requests per engineer](pr-throughput.html) (DX's "diffs per engineer") and the
[Developer Experience Index](developer-experience-index.html). DX's quarterly research also reports
several AI measures used on the map, such as AI-authored code share and the innovation ratio.

## Flow Framework

The Flow Framework, introduced by Mik Kersten in *Project to Product* (2018), measures how business
value moves through delivery, with flow velocity, flow time, flow efficiency, flow load and flow
distribution. It supplies the flow group on the map: [flow efficiency](flow-efficiency.html) and
[work in progress](work-in-progress.html) (its flow load).

## OrgSignals Speed Score

OrgSignals combines pull request cycle time (50%), cycle time variance (25%) and coding time (25%) into
one Speed Score out of 100, with scores above 85 rated elite. It shows how single metrics can be
weighted into an index, and why the weights should be stated with the score.

{{metrics:OrgSignals}}

## AWS AI-DLC

AWS introduced the AI-Driven Development Life Cycle (AI-DLC) on 31 July 2025: a development method
organised in Inception, Construction and Operations phases, with work done in short cycles AWS calls
bolts. It is a way of working, not a metrics framework. Separately, Amazon uses
[cost to serve software](cost-to-serve-software.html) (CTS-SW) to measure the business value of
developer-experience improvements.

## How they fit together

DORA and the Flow Framework measure the delivery system. SPACE and the DX Core 4 add the developer's
experience and the business view. None of them was designed for AI-written code, so the AI in the
loop dimension on this map draws on newer vendor and research measures, which carry more
uncertainty. Their pages say so.

## Sources
