# Approach

## Information architecture

The landing page is the full overview map (GR-4.5). Five dimensions are the map's bands; each holds
metric groups; each group holds metrics. One inventory, `content/map.yml`, drives:

- the overview SVG, with native links keyed on topic IDs (a topic links only when its page exists);
- legend chips and band focus;
- the text route ("All metrics") under the map, the accessible equivalent of the figure;
- the purpose routes (`content/site.yml`): Start with the basics · Report AI impact · Instrument ·
  Prevent review overload · Run agents · Look it up;
- related-metric links on every page.

## Page types

Metric and dimension pages are generated from data (D-010): each metric is a YAML record in
`content/metrics/`, each dimension a band in `content/map.yml`. Reference pages (frameworks, latest)
are Markdown in `content/pages/` with front matter `id`, `type`, `title`, `summary`, `sources` and
optionally `title_accent` (gradient words, at most two). Glossary and sources pages are generated from
`content/glossary.yml` and `content/references.yml`.

Every metric page gets a generated systems-view figure (data sources → metric → read it with); a
hand-drawn `content/diagrams/<metric-id>.svg` replaces it, captioned from its `<title>`.

## Pipeline (per section)

```
research lead ─► source register (primary sources, dates) ─► inventory update
  ─► write pages to template ─► figures ─► checks ─► three reviews (accuracy ║ confidentiality ║ editorial)
  ─► fix and recheck ─► next section
```

At the end: verify the whole reader experience (SOP step 6), then one final review package for
Vishal: preview, acceptance-question results, review record with independence noted, limitations.

## Build

```bash
pip install -r scripts/requirements.txt
python site/generate.py --preview         # review build into _site/
python -m unittest discover -s scripts/tests -v
python scripts/check_browser.py           # set CHROMIUM_PATH to use a preinstalled Chromium
python site/generate.py                   # release build; refuses provisional content
```
