# Status

## Where it stands (27 Nov 2026)

The full map is built on branch `claude/project-thread-37x2w4` (pull request #1). Nothing is
published: Pages is off and deploy is manual (D-005). Vishal accepted the content and guesses on
27 Nov 2026 (D-016) and approved publishing; the release build passes.

- 57 pages: home (overview map, six purpose routes, text route), 47 metric pages, 5 dimension pages,
  frameworks, "What changed in November 2026", glossary (30 terms), sources (51 cited sources with
  status and confirmed claims).
- Research batches 1 to 3 merged (D-009 to D-011, D-014).
- Reviews run 27 Nov 2026, each by a fresh-context reviewer with no part in writing the content:
  accuracy (31 findings, 8 source URLs spot-checked) and editorial plus confidentiality (23 findings).
  Must-fix findings are fixed; see the review package in the pull request. Independent reader test:
  Gemini (done); ChatGPT pending (its browser session was in use by another task).
- Last verified build: preview build passes 12 site tests and the browser checks (hover tooltip,
  band focus, Escape, skip link, no script errors, no horizontal scroll at 390 px on all 57 pages).

## Open issues

- Nine metrics rely on the common-practice exception (D-012).
- Process notes in `project/` mention research tools and Notion (A9).
- Suggestions not yet applied: relationship notes between overlapping metrics (review wait vs time
  to first review; AI pull request acceptance vs agent task success), primary GitClear source for
  duplication, populations for Larridin thresholds, OWASP framing on AI-introduced vulnerabilities.

## Next

1. Merge PR #1 and run **Deploy to GitHub Pages** (approved by Vishal 27 Nov 2026).

## Session log

- **2026-11-27** Full build: content model, generator rewrite, research batches 1–2, reviews and fixes.
- **2026-11-27** Vishal confirmed the name "AI SDLC Metrics & KPIs Map"; repository name unchanged.
- **2026-11-27** Scaffold. Read SOP v1.1 and design system v1.0; studied both reference repos at the
  SOP's pinned commits; created `main` with a README (Vishal approved); built the scaffold on a branch.
