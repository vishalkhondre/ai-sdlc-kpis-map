---
id: measuring-impact
type: reference
title: How to show whether AI is making a difference
title_accent: making a difference
summary: Measuring delivery while AI is in use is not the same as measuring AI's effect. A short method for a leadership scorecard, baselines, comparisons and honest reporting.
sources: [metr-2025, metr-2026-update, dora-guide]
---

Every metric on this map can be tracked while teams adopt AI. Showing that AI caused a change is
harder, because tooling, team, process and product changes happen at the same time. This page sets
out a simple method. It is common practice in measurement, not a standard from any one source.

## Start with a small scorecard

Pick one metric from each question leadership asks, and add more only when one of them moves and you
need to know why. The [Report AI impact](index.html#routes) route is one such set:

| Question | Scorecard metric | Diagnostic metrics to open when it moves |
|---|---|---|
| Is it worth the money? | [AI spend per unit of output](ai-spend-per-output.html) | [AI spend per engineer](ai-spend-per-engineer.html), [wasted and optimisable AI spend](wasted-ai-spend.html) |
| Are we faster? | [Change lead time](change-lead-time.html) | [Pull request cycle time](pr-cycle-time.html), [time to first review](time-to-first-review.html), [flow efficiency](flow-efficiency.html) |
| Is quality holding? | [Change failure rate](change-failure-rate.html) | [Incidents per pull request](incidents-per-pr.html), [AI code survival and turnover](ai-code-survival.html) |
| Is time going to new value? | [Innovation ratio](innovation-ratio.html) | [Time to market](time-to-market.html) |
| Is the work sustainable? | [Developer Experience Index](developer-experience-index.html) | [Review and supervisory burden](supervisory-burden.html), [AI satisfaction and trust](ai-satisfaction-trust.html) |

Adoption metrics such as [active AI users](ai-active-users.html) and
[AI-authored code share](ai-authored-share.html) explain the scorecard. They do not belong on it,
because they measure activity, not benefit.

## Set a baseline before you compare

Record each scorecard metric for at least one full quarter before a rollout, or reconstruct it from
version-control and incident history. Use the same definitions, exclusions and team boundaries after
the rollout. A change of definition shows up as a change of result.

## Compare like with like

Two comparisons make a result more convincing than a before-and-after line:

- **Across teams.** Compare teams that adopted earlier with teams that adopted later, over the same
  period, so that seasonal and organisation-wide changes affect both.
- **Within teams.** Compare AI-assisted and unassisted work in the same teams, for example pull
  requests with and without AI attribution, where tools record it.

Neither is a controlled experiment. Say so when reporting, and name other changes that happened in the
same period, such as reorganisations, new platforms or hiring.

## Do not rely on perception alone

Self-reported time savings and real speed can disagree. In METR's 2025 randomised trial, experienced
developers took 19% longer with AI allowed, yet believed AI had sped them up by 20%. METR later called
its newer study an unreliable signal and the evidence weak. Read survey measures with system data, as
every metric page on this map advises.

## Report honestly

- Show the trend with its baseline, not a single number.
- Report each scorecard metric with the metric it is read with, so a gain bought at a cost is visible.
- Report at team and organisation level, never for individuals.
- When a definition differs from a published benchmark, say so before comparing, or do not compare.

## Sources
