# CLAUDE.md — start here

This repository builds **AI SDLC Metrics & KPIs Map**, a public reference on measuring the
AI SDLC, following Vishal's SOP "How to build an interactive learning map" v1.1 and the locked
AI SDLC design system v1.0 (both in Vishal's Notion). This file and `project/` hand one session over to the next.

## Read before doing anything

| Order | File | What it holds |
|---|---|---|
| 1 | [`project/GOAL.md`](project/GOAL.md) | The brief: reader, question, boundary, publication sentence |
| 2 | [`project/GROUND-RULES.md`](project/GROUND-RULES.md) | Numbered rules every check and review cites |
| 3 | [`project/STATUS.md`](project/STATUS.md) | Where the work stands, what is next, session log |
| 4 | [`project/APPROACH.md`](project/APPROACH.md) | Information architecture, page types, pipeline, build |
| 5 | [`project/AGENTS.md`](project/AGENTS.md) | Roles and handoffs |
| 6 | [`project/ASSUMPTIONS.md`](project/ASSUMPTIONS.md) | What is assumed, what is open |
| 7 | [`project/DECISIONS.md`](project/DECISIONS.md) | Decisions taken. Do not reopen without Vishal |

## Do I continue after the pilot?

Yes. The approval policy is a **single final review** (D-002, GR-6.1): build, review, fix and verify
every section, then bring Vishal one complete preview. Escalate earlier only for a consequential
policy choice, a private source, or a change of audience or scope.

## What publishes

Only a manual run of **Deploy to GitHub Pages** on `main`, by Vishal, after he enables Pages (D-005).
Merging does not publish. The release build refuses provisional content (D-006). The repository is
public, so a pushed branch is readable by anyone (A2).

## Session protocol

**Start:** read the files above; confirm you can push to your branch; pick the top item under
**Next** in `STATUS.md`.
**End:** update `STATUS.md` (last verified build, open issues, one next action), record decisions
and assumptions, run validation, commit.

## Validation

```bash
pip install -r scripts/requirements.txt
python site/generate.py --preview
python -m unittest discover -s scripts/tests -v
python scripts/check_browser.py      # CHROMIUM_PATH=/path/to/chromium to use a preinstalled browser
```

## The three rules most often broken

1. Every metric needs a definition, formula with unit, and the source of its definition (GR-2.6).
2. No invented statistics or benchmarks; a benchmark carries its source, year and population (GR-2.3, GR-2.7).
3. Nothing provisional reaches the public site; unfinished metrics stay plain labels (GR-3.2).
