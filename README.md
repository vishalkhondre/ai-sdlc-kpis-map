# The AI SDLC Metrics Map

A vendor-neutral reference for measuring the AI SDLC: which metrics show whether AI is improving
software delivery, how each is defined and measured, and what each cannot tell you. One overview map
of five dimensions is the front door; every metric on it leads to its own page.

Sister site: [The AI SDLC Map](https://vishalkhondre.github.io/ai-sdlc-map/).

## Build

```bash
pip install -r scripts/requirements.txt
python site/generate.py --preview     # review build into _site/, open _site/index.html
python site/generate.py               # release build (refuses provisional content)
python -m unittest discover -s scripts/tests -v
python scripts/check_browser.py
```

| Path | Holds |
|---|---|
| `content/map.yml` | The topic inventory: dimensions, groups, metrics, stable IDs |
| `content/site.yml` | Site identity and purpose routes |
| `content/pages/` | One Markdown page per metric or dimension |
| `content/diagrams/` | Systems-view figures as SVG source |
| `templates/pages/` | Page-type templates |
| `site/` | Generator, styles and scripts (design system v1.0) |
| `scripts/` | Tests and browser checks |
| `project/` | Goal, ground rules, status, decisions: start at `CLAUDE.md` |

## Licence

Prose, diagrams and data in `content/` are CC BY 4.0. Tooling (`site/`, `scripts/`, `.github/`) is
MIT. See `LICENSE`. By Vishal Khondre.
