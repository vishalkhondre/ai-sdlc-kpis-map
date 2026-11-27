# Goal

The brief for this map (SOP v1.1, step 1). Items marked **(provisional)** are the maintainer's best
guess and wait for Vishal; nothing marked provisional may reach the public site.

## In one sentence

A public, vendor-neutral reference that shows an enterprise which metrics tell whether AI is
improving software delivery, how each is defined and measured, and what each cannot tell you,
organised as one map whose every box leads to a full metric page. **(provisional wording)**

## Intake

| Field | Answer |
|---|---|
| Topic and reader | KPIs and metrics of the AI SDLC (AI-DLC) across enterprise dimensions. Readers: engineering leaders and heads of platform or developer experience who must report on AI adoption; delivery and quality leads choosing what to track; executives sponsoring AI who need to read the numbers. They know delivery basics and DORA by name, not every metric's formula. **(provisional)** |
| Reader question | "Which metrics show whether AI is making our software delivery better, how is each one defined and measured, and what does it not tell us?" **(provisional)** |
| Map type | **Reference map, standalone.** It has its own subject boundary (measurement) and its own audience, so it is not a zoom inside the AI SDLC Map; it links to that map as a sister site (D-001). |
| Boundary | In scope: business outcomes, delivery flow, AI adoption and agent performance, developer experience, quality, risk and governance; definitions, formulas, data sources, AI effects, pitfalls, how metrics balance. Out of scope: tool tutorials, vendor comparisons, any organisation's internal numbers, benchmarks without a public source and year. |
| Worked example | Reference map: one running example may be chosen once research lands (GR-3.4). |
| Vendor stance | Vendor-neutral. A product appears only as a versioned example on a page about its category (GR-3.3). |
| Repository | `vishalkhondre/ai-sdlc-kpis-map` (public), created by Vishal on 27 Nov 2026. |
| Intended public URL | <https://vishalkhondre.github.io/ai-sdlc-kpis-map/> **(provisional)** |
| Publication sentence | The owner reviews at **the pull request and its rendered preview**; the action that makes this edition public is **running the "Deploy to GitHub Pages" workflow on `main` after Pages is enabled**; the person authorised to take it is **Vishal**. Merging alone does not publish (D-005). |
| Approval policy | **Single final review** (SOP default for new maps, D-002). The maintainer builds, reviews, fixes and verifies, then brings one complete preview. |

## Reader acceptance questions (reference map)

Written before the page count, per SOP step 1. Each needs a findable answer before final review.

1. **Definition:** "What exactly does *change failure rate* count, and how is it calculated?"
2. **Relationship:** "If AI raises our share of AI-assisted changes, which quality and flow metrics
   should I watch so speed does not hide rework?"
3. **Route for a purpose:** "I have to report AI impact to the leadership team next quarter. Which
   small set of metrics do I start with, and why?"
4. **Limits of the evidence:** "Does a higher suggestion acceptance rate prove developers are more
   productive? What would?"

## What success looks like

- A reader starts at the full map, selects any metric, and gets a page that stands alone, gives the
  formula, names its source and links to the metrics that balance it.
- Every published page passed the automated checks and the three reviews, recorded in `content/reviews/`.
- The landing page shows the complete map (design system v1.0, principle 1).

## Author and licence

Independent work by Vishal Khondre. Prose under CC BY 4.0, tooling under MIT (see `LICENSE`).
