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
