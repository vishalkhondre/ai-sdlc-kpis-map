# Status

## Where it stands (27 Nov 2026)

Scaffold built on branch `claude/project-thread-37x2w4`, pull request open against `main`.
Nothing is published: Pages is off and deploy is manual (D-005).

- Generator, design-system styles and interaction layer, overview map from the inventory, text
  route, purpose routes, metric page with a systems-view figure.
- Inventory is **provisional** (38 metrics in 5 dimensions); one **layout-sample** page
  (`lead-time`). The release build refuses both.
- Last verified build: preview build passes 8 site tests and 10 browser checks (hover tooltip,
  band focus, Escape, skip link, no script errors, no horizontal scroll at 390 px on every page).

## Next

1. **Vishal:** review the scaffold PR and preview; settle the open items in `ASSUMPTIONS.md` (A5–A7).
2. When the ChatGPT research returns: verify it into a source register (GR-2.8), save the research to
   Notion, then replace `content/map.yml` with the researched inventory and drop `status: provisional`.
3. Port checks from the AI SDLC Map as content arrives: page template gate (GR-4.1), citation and
   reference fields (GR-2.5), deny-list (GR-1.2), review record binding (GR-5.2), PDF field guide.
4. Pilot (SOP step 4): one purpose route across two related metrics, end to end.

## Session log

- **2026-11-27** Scaffold. Read SOP v1.1 and design system v1.0; studied both reference repos at the
  SOP's pinned commits; created `main` with a README (Vishal approved); built the scaffold on a branch.
