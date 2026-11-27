# Decisions

Taken decisions with reasons. Do not reopen without Vishal. Newest last.

### D-001 · Reference map, standalone · 2026-11-27
**Decision.** A reference map with its own site, linking to the AI SDLC Map as a sister site.
**Why.** Measurement has its own audience (leaders reporting on AI) and its own subject boundary,
which the SOP's standalone test asks for. A zoom inside the AI SDLC Map's assurance band would
inherit that map's terms and stay too narrow for enterprise dimensions. *Vishal can overturn this.*

### D-002 · Single final review · 2026-11-27
**Decision.** The SOP default for new maps: the maintainer builds, reviews, fixes and verifies, then
brings one complete preview. Earlier maps used section gates; this one does not (GR-6.1).

### D-003 · Locked design system v1.0 · 2026-11-27
**Decision.** Build to the AI SDLC design system v1.0 (Notion, locked by Vishal on 27 Nov 2026):
Inter + JetBrains Mono, near-black on off-white, indigo-to-teal gradient on at most two headline words
and the reading progress line, five band colours, line icons, hover tooltip, band focus, legend chips,
fade-up motion, reading progress, back-to-map pill. Light theme only until dark tokens are designed.

### D-004 · A small new generator instead of porting the AI SDLC Map's · 2026-11-27
**Decision.** `site/generate.py` is new (about 450 lines): one YAML inventory → overview SVG, text
route, routes and pages, with links keyed on topic IDs.
**Why.** The AI SDLC Map's generator carries its old brand (Atkinson Hyperlegible, IBM Plex, its own
colour system) and keys map links on visible labels, which the SOP now advises against. Porting would
mean stripping more than reusing. Its checks (citations, page structure, deny-list, release binding,
PDF) are ported one at a time as content needs them (see `STATUS.md`).

### D-005 · Publishing is a manual workflow run · 2026-11-27
**Decision.** `deploy-pages.yml` runs only on `workflow_dispatch` from `main`, and refuses to deploy
a provisional build because it runs the release build. `validate.yml` runs on every pull request and
push to `main` and publishes nothing.
**Why.** Both reference repositories deploy on every push to `main`, so merging publishes. Under the
single-final-review policy, merging the scaffold or a reviewed section must not publish by itself.
Vishal can switch to deploy-on-merge later by adding `push: branches: [main]`.

### D-006 · Provisional inventory and a preview/release split · 2026-11-27
**Decision.** The map inventory starts as a labelled hypothesis drawn from well-known public metric
families, so the build and design can be reviewed before the research lands. `--preview` builds it
with a review banner; the default (release) build refuses while `content/map.yml` says
`status: provisional` or any page has `sample: true`.
**Why.** The SOP forbids placeholders on the public site, but the owner judges design by looking.

### D-007 · Page types: metric and dimension · 2026-11-27
**Decision.** Two page types to start (`templates/pages/`). Metric: Definition · Formula · Why it
matters · How to measure · How AI changes it · Pitfalls · Related · Sources. Dimension: What it
covers · Metrics · How they balance · Who uses them · Related · Sources. Others (purpose route,
framework comparison, glossary) are added when the research shows a need.

### D-008 · Five dimensions on the five band colours · 2026-11-27
**Decision.** The map's five regions take the design system's five band colours in order: business
outcomes (amber), delivery flow (grey), AI in the loop (indigo), developer experience (green),
quality, risk and governance (cyan). A sixth region needs Vishal's approval (design system rule).
The region names are provisional with the inventory (D-006).

### D-009 · Research categories folded into the five bands · 2026-11-27
**Decision.** The nine metric categories found in the research (cost and ROI, business outcomes,
flow, adoption, impact, agents, developer experience, stability and code quality, governance) are
folded into the five bands of D-008, as 14 metric groups. No sixth band.
**Why.** Every category fits one band, and the design system allows five band colours.

### D-010 · YAML metric model, generated figures · 2026-11-27
**Decision.** Each metric is one YAML record in `content/metrics/<n>-<band>.yml` with required fields
(definition, formula, unit, direction, inputs, why, measure, ai, pitfalls, related) and optional
`findings` (each with one source), `disagreements` and `sources`. Every metric page gets a generated
systems-view figure (data sources → metric → the metrics to read it with); a hand-drawn
`content/diagrams/<id>.svg` replaces it where one exists. Dimension pages are generated from the same
data. The `lead-time` sample page and `sample: true` are retired.
**Why.** 47 pages with one structure are reviewed and checked more reliably as data than as prose.

### D-011 · A finding may say only what the register confirms · 2026-11-27
**Decision.** `content/references.yml` lists, for each source, the claims confirmed on the page.
A finding states only those claims, with the source's own population and date. Sources that could
not be opened are not cited (the build refuses them); `partial` sources are cited only for their
listed claims. The register's `note` field is internal and never rendered; `caveat` is shown.
**Why.** GR-2.3, GR-2.4, GR-2.7, and the research review found widely repeated figures that the
cited pages do not contain.

### D-012 · Common-practice definitions without a source · 2026-11-27
**Decision.** Where no verified public source defines a metric (for example flow efficiency, work in
progress, time to market, mutation score), the page states the common-practice definition, credits
the originator in Origin where one is known, and says that no verified source is cited. This is the
recorded exception to GR-2.6. It is listed for Vishal's review.
**Why.** Inventing a citation is worse than saying none was verified; some originators (Flow
Framework, ISO/IEC 42001) could not be opened in this session.

### D-013 · Pitfalls may be data caveats without a read-with metric · 2026-11-27
**Decision.** A pitfall names a metric to read with only when another metric shows the misreading.
Data-quality caveats (small samples, response rates, changed rule sets) carry no read-with link.
Every metric keeps at least one read-with pitfall (GR-4.2).
**Why.** The editorial review found forced pairings that read as arbitrary.

### D-014 · Monthly digest page · 2026-11-27
**Decision.** `latest.html` ("What changed in November 2026") lists dated reports and papers from the
research digest that are in the source register, and what each changes on the map. LinkedIn posts
(approximate dates) and unverified videos and papers are left out.
**Why.** Vishal asked for the latest month's material; only verified, dated items meet GR-2.

### D-015 · OrgSignals sources removed · 2026-11-27
**Decision.** At Vishal's request, all OrgSignals / SignalsAI references are removed and the metrics
kept. Cycle time variance and coding time are now common-practice definitions (D-012). The branded
Speed Score (frameworks section and glossary entry) is dropped; the frameworks page describes
composite speed scores generically, without weights.
