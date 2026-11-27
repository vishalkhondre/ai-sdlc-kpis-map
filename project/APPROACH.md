# Approach

## Information architecture

The landing page is the full overview map (GR-4.5). Five dimensions are the map's bands; each holds
metric groups; each group holds metrics. One inventory, `content/map.yml`, drives:

- the overview SVG, with native links keyed on topic IDs (a topic links only when its page exists);
- legend chips and band focus;
- the text route ("All metrics") under the map, the accessible equivalent of the figure;
- the purpose routes (`content/site.yml`): Understand · Choose metrics · Instrument · Report to
  leaders · Look it up;
- related-metric links on every page.

## Page types

See `templates/pages/` and D-007. Every page has front matter: `id`, `type`, `band`, `title`,
`summary`, `formula` and `unit` (metric pages), `related`, `sources`, and optionally `title_accent`
(gradient words, at most two) and `sample` (preview only).

Figures on topic pages are systems-view SVGs in `content/diagrams/`, inserted with
`{{figure:<name>}}`, numbered and captioned automatically from the SVG `<title>`.

## Pipeline (per section)

```
research lead (ChatGPT DR) ─► source register (primary sources, dates) ─► inventory update
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
