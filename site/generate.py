#!/usr/bin/env python3
"""Build the AI SDLC Metrics & KPIs Map site from content/ into _site/.

    python site/generate.py            # release build: refuses provisional or unverified content
    python site/generate.py --preview  # review build: same pages, with a review banner

Inputs (all under content/):
  map.yml          dimensions (bands) and metric groups, in map order
  metrics/*.yml    one file per dimension, in band order; each metric names its `group`
  references.yml   the source register; a page may cite a source only for a listed claim
  glossary.yml     terms with originators (GR-2.2)
  pages/*.md       reference pages in Markdown (frameworks)
  diagrams/*.svg   hand-drawn systems-view figures; a metric without one gets a generated figure

Links key on stable IDs (SOP "The pattern"). Visual rules follow the locked AI SDLC design system
v1.0 (D-003). Structural checks for GR-2.5, GR-2.6, GR-4.1 and GR-4.3 run on every build.
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ASSETS = ROOT / "site" / "assets"
OUT = ROOT / "_site"

# Design system v1.0 — band colours (stroke, fill, dark text), in fixed order.
BAND_COLOURS = {
    "context": ("#D29A3A", "#FDF6E9", "#7A4E0E"),
    "lifecycle": ("#A1A1AA", "#F7F7F8", "#27272A"),
    "core": ("#4C66E6", "#EEF1FD", "#2B3A99"),
    "enablement": ("#10A374", "#E8F7F1", "#065F46"),
    "assurance": ("#0E8FB0", "#E6F5FA", "#0B4F63"),
}
HEADER_LINE = {"context": "#F0D9AE", "lifecycle": "#E4E4E7", "core": "#C9D2F7",
               "enablement": "#BDE7D6", "assurance": "#B5DEEA"}

# Line icons, 24px grid, 1.8 stroke (design system v1.0, "Icons").
ICONS = {
    "compass": "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z M16.2 7.8l-2.1 6.3-6.3 2.1 2.1-6.3z",
    "cycle": "M3 12a9 9 0 0 1 15.5-6.4L21 8 M21 3v5h-5 M21 12a9 9 0 0 1-15.5 6.4L3 16 M3 21v-5h5",
    "chip": "M6 6h12v12H6z M9.5 9.5h5v5h-5z M9 2v4 M15 2v4 M9 18v4 M15 18v4 M2 9h4 M2 15h4 M18 9h4 M18 15h4",
    "layers": "M12 2l10 5-10 5-10-5z M2 12l10 5 10-5 M2 17l10 5 10-5",
    "shield": "M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z M9 12l2 2 4-4",
    "rising": "M3 17l6-6 4 4 8-8 M14 7h7v7",
    "book": "M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z",
    "pkg": "M12 2l9 5v10l-9 5-9-5V7z M3 7l9 5 9-5 M12 12v10",
    "play": "M7 4l13 8-13 8z",
    "flag": "M4 22V4 M4 4h13l-2 4 2 4H4",
    "search": "M11 4a7 7 0 1 0 0 14 7 7 0 0 0 0-14z M21 21l-5-5",
    "map": "M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z M9 4v14 M15 6v14",
    "arrow": "M5 12h14 M13 6l6 6-6 6",
    "sigma": "M18 4H6l6 8-6 8h12",
    "link": "M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1 M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1",
    "alert": "M12 3l10 18H2z M12 10v5 M12 18v.5",
    "gauge": "M12 14l4-4 M3.5 18a10 10 0 1 1 17 0",
    "bot": "M5 9h14v10H5z M12 5v4 M9 14h.01 M15 14h.01 M2 13v3 M22 13v3",
    "download": "M12 3v12 M7 10l5 5 5-5 M4 21h16",
    "chart": "M4 20V10 M10 20V4 M16 20v-7 M22 20H2",
    "users": "M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z M2 21c0-4 3-7 7-7s7 3 7 7 M17 3a4 4 0 0 1 0 8 M22 21c0-3-2-6-5-7",
    "scale": "M12 3v18 M5 7h14 M5 7l-3 7a4 4 0 0 0 6 0z M19 7l-3 7a4 4 0 0 0 6 0z M8 21h8",
}

H2_ICONS = {
    "Definition": "book", "Formula": "sigma", "Why it matters": "flag", "How to measure": "gauge",
    "How AI changes it": "bot", "What the research shows": "chart", "Pitfalls": "alert",
    "Related": "link", "Sources": "search", "What it covers": "book", "Who uses it": "users",
    "How these metrics balance": "scale", "Metrics in this dimension": "chart",
}

REQUIRED = ["label", "group", "summary", "origin", "definition", "formula", "unit", "direction",
            "inputs", "why", "measure", "ai", "pitfalls", "related"]


def icon(name: str, size: int = 18, colour: str = "currentColor") -> str:
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{colour}" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            f'focusable="false"><path d="{ICONS[name]}"/></svg>')


def esc(s) -> str:
    return html.escape(str(s), quote=True)


# --------------------------------------------------------------------------- content loading

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


FRONT = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


def load_content():
    site = load_yaml(CONTENT / "site.yml")
    mp = load_yaml(CONTENT / "map.yml")
    refs = {r["id"]: r for r in load_yaml(CONTENT / "references.yml")}
    glossary = load_yaml(CONTENT / "glossary.yml")
    metrics: dict[str, dict] = {}
    errors: list[str] = []
    files = sorted((CONTENT / "metrics").glob("*.yml"))
    if len(files) != len(mp["bands"]):
        errors.append("content/metrics/ needs one file per band, in band order")
    for f, band in zip(files, mp["bands"]):
        for m in load_yaml(f) or []:
            m["band"] = band
            if m["id"] in metrics:
                errors.append(f"duplicate metric id {m['id']}")
            metrics[m["id"]] = m
    for b in mp["bands"]:
        gids = {g["id"] for g in b["groups"]}
        for g in b["groups"]:
            g["topics"] = [m for m in metrics.values() if m["band"] is b and m["group"] == g["id"]]
            if not g["topics"]:
                errors.append(f"group {b['id']}/{g['id']} has no metrics")
        for m in metrics.values():
            if m["band"] is b and m["group"] not in gids:
                errors.append(f"{m['id']}: group '{m['group']}' not in band {b['id']}")
    pages = {}
    for p in sorted((CONTENT / "pages").glob("*.md")):
        mt = FRONT.match(p.read_text(encoding="utf-8"))
        if not mt:
            errors.append(f"{p.name}: missing front matter")
            continue
        meta = yaml.safe_load(mt.group(1)) or {}
        meta["body"], meta["path"] = mt.group(2), p
        pages[meta["id"]] = meta
    return site, mp, metrics, refs, glossary, pages, errors


def page_sources(m: dict) -> list[str]:
    """Definition sources plus every source a finding cites, in first-use order."""
    out = []
    for s in list(m.get("sources") or []) + [f["source"] for f in m.get("findings") or []]:
        if s not in out:
            out.append(s)
    return out


def check(site, mp, metrics, refs, glossary, pages, release: bool) -> list[str]:
    """Structural checks. GR numbers refer to project/GROUND-RULES.md."""
    errs = []
    for mid, m in metrics.items():
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", mid):
            errs.append(f"{mid}: id is not kebab-case (SOP stable IDs)")
        for k in REQUIRED:
            if not m.get(k):
                errs.append(f"{mid}: missing required field '{k}' (GR-4.1, GR-2.6)")
        if len(m.get("pitfalls") or []) < 2:
            errs.append(f"{mid}: needs at least two pitfalls (GR-4.1)")
        for p in m.get("pitfalls") or []:
            if p.get("balance") not in metrics:
                errs.append(f"{mid}: pitfall balance '{p.get('balance')}' is not a metric (GR-4.3)")
            elif p["balance"] == mid:
                errs.append(f"{mid}: a metric cannot balance itself")
        for r in m.get("related") or []:
            if r not in metrics:
                errs.append(f"{mid}: related '{r}' is not a metric (GR-4.3)")
        for s in page_sources(m):
            if s not in refs:
                errs.append(f"{mid}: source '{s}' is not in references.yml (GR-2.5)")
            elif refs[s].get("status") == "unverified":
                errs.append(f"{mid}: cites unverified source '{s}' (GR-2.4)")
    for g in glossary:
        if not g.get("origin"):
            errs.append(f"glossary '{g['term']}': no origin (GR-2.2)")
        if g.get("source") and g["source"] not in refs:
            errs.append(f"glossary '{g['term']}': source '{g['source']}' not in references.yml")
    for p in pages.values():
        for s in p.get("sources") or []:
            if s not in refs:
                errs.append(f"{p['path'].name}: source '{s}' not in references.yml")
    for r in site.get("routes") or []:
        for t in r.get("topics", []):
            if t not in metrics:
                errs.append(f"route {r['id']}: '{t}' is not a metric")
    if release and mp.get("status") == "provisional":
        errs.append("content/map.yml is provisional (GR-3.2)")
    return errs


# --------------------------------------------------------------------------- overview map SVG

MAP_W = 1200
LABEL_X, LABEL_W = 22, 262
AREA_X = LABEL_X + LABEL_W + 18
AREA_W = MAP_W - AREA_X - 22
NODE_H1, NODE_H2, NODE_H3, NODE_GAP, COL_GAP = 32, 46, 60, 8, 12
CHAR_W = 6.9  # Inter 500 at 12.5px, measured average


def wrap(label: str, width: float, char_w: float = CHAR_W, lines_max: int = 3) -> list[str]:
    limit = max(8, int((width - 20) / char_w))
    words, lines, cur = label.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > limit:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return lines[:lines_max]


def build_map(mp: dict, title: str) -> str:
    parts, y = [], 14
    for n, band in enumerate(mp["bands"], 1):
        stroke, fill, dark = BAND_COLOURS[band["colour"]]
        groups = band["groups"]
        colw = (AREA_W - (len(groups) - 1) * COL_GAP) / len(groups)
        cols, stack_h = [], 0
        for g in groups:
            nodes, h = [], 0
            for t in g["topics"]:
                lines = wrap(t["label"], colw)
                nh = (NODE_H1, NODE_H2, NODE_H3)[len(lines) - 1]
                nodes.append((t, lines, h, nh))
                h += nh + NODE_GAP
            cols.append((g, nodes))
            stack_h = max(stack_h, h - NODE_GAP)
        band_h = max(132, 16 + 22 + stack_h + 16)
        out = [f'<g class="band" data-band="{esc(band["id"])}">',
               f'<rect class="band-bg" x="10" y="{y}" width="{MAP_W - 20}" height="{band_h}" rx="8" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>']
        lx, ly, lh = LABEL_X, y + 10, band_h - 20
        out.append(f'<a class="maplink band-label" href="{esc(band["id"])}.html" data-band="{esc(band["id"])}" '
                   f'data-dest="Dimension overview" aria-label="{esc(band["title"])}">'
                   f'<rect x="{lx}" y="{ly}" width="{LABEL_W}" height="{lh}" rx="6" fill="#fff" '
                   f'stroke="{stroke}" stroke-opacity=".55"/>'
                   f'<text x="{lx + 14}" y="{ly + 24}" class="bl-num" fill="{dark}">{n:02d} · '
                   f'{esc(band["title"].upper())}</text>'
                   f'<text x="{lx + 14}" y="{ly + 44}" class="bl-role">{esc(band["role"])}</text>')
        for i, note in enumerate(band.get("notes", [])[:3]):
            out.append(f'<text x="{lx + 14}" y="{ly + 64 + i * 16}" class="bl-note">{esc(note)}</text>')
        out.append(f'<g transform="translate({lx + LABEL_W - 32},{ly + lh - 32}) scale(.83)" fill="none" '
                   f'stroke="{dark}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
                   f'<path d="{ICONS[band["icon"]]}"/></g></a>')
        for c, (g, nodes) in enumerate(cols):
            gx = AREA_X + c * (colw + COL_GAP)
            out.append(f'<text x="{gx + 2:.1f}" y="{y + 26}" class="grp" fill="{dark}">{esc(g["title"])}</text>')
            for t, lines, dy, nh in nodes:
                ny = y + 36 + dy
                dash = ' stroke-dasharray="4 3"' if g.get("dashed") else ""
                rect = (f'<rect x="{gx:.1f}" y="{ny}" width="{colw:.1f}" height="{nh}" rx="5" fill="#fff" '
                        f'stroke="{stroke}"{dash}/>')
                tx = f'{gx + 10:.1f}'
                txt = (f'<text x="{tx}" y="{ny + (20.5 if len(lines) == 1 else 19)}" class="maplabel" '
                       f'fill="{dark}">{esc(lines[0])}'
                       + "".join(f'<tspan x="{tx}" dy="15">{esc(ln)}</tspan>' for ln in lines[1:]) + '</text>')
                out.append(f'<a class="maplink" href="{esc(t["id"])}.html" data-topic="{esc(t["id"])}" '
                           f'data-dest="{esc(band["title"])}" aria-label="{esc(t["label"])}">{rect}{txt}</a>')
        out.append("</g>")
        parts.append("".join(out))
        y += band_h + 14
    return (f'<svg class="overview" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {MAP_W} {y}" '
            f'role="img" aria-labelledby="map-title map-desc">'
            f'<title id="map-title">{esc(title)}</title>'
            f'<desc id="map-desc">Five dimensions an enterprise measures when AI joins software delivery, '
            f'each with its metric groups and metrics. Every metric opens its own page. The same content is '
            f'listed as text below the map.</desc>' + "".join(parts) + "</svg>")


# --------------------------------------------------------------------------- systems-view figures

MONO = "JetBrains Mono, ui-monospace, monospace"
G_LINE, G_ARROW, INK, MUTED = "#CBCED6", "#8F94A3", "#1E2233", "#6B728A"
SMALL = {"version": "M8 2v12 M4 8a4 4 0 1 0 8 0 4 4 0 1 0-8 0",
         "survey": "M3 2h10v12H3z M5.5 5.5h5 M5.5 8h5 M5.5 10.5h3",
         "metric": "M2 13l4-5 3 3 5-7",
         "default": "M2 3h12v10H2z M2 6h12"}


def small_icon(label: str, x: float, y: float, kind: str | None = None) -> str:
    low = label.lower()
    key = kind or ("survey" if "survey" in low else "version" if "version" in low else "default")
    return (f'<path d="{SMALL[key]}" transform="translate({x},{y})" fill="none" stroke="{G_ARROW}" '
            f'stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/>')


def panel(x, y, w, title, tag, rows, colour_key, kind=None) -> tuple[str, int]:
    _, fill, dark = BAND_COLOURS[colour_key]
    h = 30 + max(1, len(rows)) * 34
    p = [f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="4" fill="#fff" stroke="{G_LINE}"/>',
         f'<path d="M{x:.1f} {y + 4}a4 4 0 0 1 4-4h{w - 8:.1f}a4 4 0 0 1 4 4v24h-{w:.1f}z" fill="{fill}"/>',
         f'<line x1="{x:.1f}" x2="{x + w:.1f}" y1="{y + 28}" y2="{y + 28}" stroke="{HEADER_LINE[colour_key]}"/>',
         f'<text x="{x + 12:.1f}" y="{y + 18.5}" font-family="{MONO}" font-size="11" font-weight="600" '
         f'letter-spacing=".06em" fill="{dark}">{esc(title)}</text>',
         f'<text x="{x + w - 12:.1f}" y="{y + 18.5}" text-anchor="end" font-family="{MONO}" font-size="10" '
         f'fill="{MUTED}">{esc(tag)}</text>']
    for i, (label, meta) in enumerate(rows):
        ry = y + 28 + i * 34
        if i:
            p.append(f'<line x1="{x:.1f}" x2="{x + w:.1f}" y1="{ry}" y2="{ry}" stroke="#EDEEF2"/>')
        p.append(small_icon(label, x + 12, ry + 9, kind))
        room = w - 48 - (len(meta) * 6.2 + 10 if meta else 0)
        text = label if len(label) * 7.2 <= room else label[: max(4, int(room / 7.2) - 1)].rstrip() + "…"
        p.append(f'<text x="{x + 36:.1f}" y="{ry + 21}" font-family="{MONO}" font-size="12" fill="{INK}">{esc(text)}</text>')
        if meta:
            p.append(f'<text x="{x + w - 12:.1f}" y="{ry + 21}" text-anchor="end" font-family="{MONO}" '
                     f'font-size="10" fill="{MUTED}">{esc(meta)}</text>')
    return "".join(p), h


def metric_figure(m: dict, metrics: dict) -> tuple[str, str]:
    """Generated systems view: data sources → the metric → the metrics that keep it honest."""
    band, mid = m["band"], m["id"]
    inputs = [(i, "") for i in m["inputs"][:4]]
    balances = []
    for p in m["pitfalls"]:
        b = metrics[p["balance"]]
        row = (b["label"], b["band"]["short"].lower())
        if row not in balances:
            balances.append(row)
    left, lh = panel(20, 50, 240, "DATA SOURCES", "inputs", inputs, band["colour"])
    right, rh = panel(600, 50, 300, "READ IT WITH", "balances", balances, "lifecycle", kind="metric")
    H = max(50 + lh, 50 + rh, 160) + 46
    cy = 50 + 62
    lines = wrap(m["label"], 200, 7.6, 2)
    name = "".join(f'<tspan x="430" dy="{0 if i == 0 else 16}">{esc(t)}</tspan>' for i, t in enumerate(lines))
    unit = m["unit"] if len(m["unit"]) <= 28 else m["unit"][:27].rstrip() + "…"
    ny = cy - 8 - (8 if len(lines) > 1 else 0)
    focal = (f'<rect x="330" y="{cy - 46}" width="200" height="92" rx="6" fill="#EEF1FD" stroke="#4C66E6" stroke-width="1.5"/>'
             f'<rect x="395" y="{cy - 55}" width="70" height="17" rx="3" fill="#fff" stroke="#4C66E6"/>'
             f'<text x="430" y="{cy - 42.5}" text-anchor="middle" font-family="{MONO}" font-size="9.5" '
             f'font-weight="600" letter-spacing=".08em" fill="#4C66E6">METRIC</text>'
             f'<text x="430" y="{ny}" text-anchor="middle" font-family="{MONO}" font-size="12.5" '
             f'font-weight="600" fill="{INK}">{name}</text>'
             f'<text x="430" y="{cy + 30}" text-anchor="middle" font-family="{MONO}" font-size="10" '
             f'fill="{MUTED}">{esc(unit)}</text>')
    arrows = (f'<path d="M260 {cy}H326" stroke="{G_ARROW}" marker-end="url(#ar-{mid})"/>'
              f'<text x="293" y="{cy - 8}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{MUTED}">feeds</text>'
              f'<path d="M530 {cy}H596" stroke="#059669" stroke-width="1.25" stroke-dasharray="4 3" '
              f'marker-end="url(#ag-{mid})"/>'
              f'<text x="563" y="{cy - 8}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#059669">balances</text>')
    levels = ", ".join(m.get("levels") or [])
    legend = (f'<text x="20" y="{H - 16}" font-family="{MONO}" font-size="10" fill="{MUTED}">'
              f'use at {esc(levels)} level · tags on the right name each metric\'s dimension</text>')
    svg = (f'<svg viewBox="0 0 920 {H}" role="img" aria-labelledby="fig-{mid}-t" class="sysfig">'
           f'<title id="fig-{mid}-t">Where {esc(m["label"])} comes from and what to read it with</title>'
           f'<defs><pattern id="dt-{mid}" width="14" height="14" patternUnits="userSpaceOnUse">'
           f'<circle cx="1" cy="1" r=".8" fill="#E4E6EB"/></pattern>'
           f'<marker id="ar-{mid}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto">'
           f'<path d="M0 0L8 4L0 8z" fill="{G_ARROW}"/></marker>'
           f'<marker id="ag-{mid}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto">'
           f'<path d="M0 0L8 4L0 8z" fill="#059669"/></marker></defs>'
           f'<rect width="920" height="{H}" fill="url(#dt-{mid})"/>{left}{right}{arrows}{focal}{legend}</svg>')
    alt = (f'{m["label"]} is computed from: {", ".join(i.lower() for i in m["inputs"][:4])}. '
           f'Read it with {" and ".join(b[0].lower() for b in balances)}, which show when it misleads.')
    return svg, alt


def dimension_figure(band: dict) -> tuple[str, str]:
    groups = band["groups"]
    w = (860 - (len(groups) - 1) * 16) / len(groups)
    parts, H = [], 0
    for i, g in enumerate(groups):
        rows = [(t["label"], "") for t in g["topics"]]
        svg, h = panel(30 + i * (w + 16), 40, w, g["title"], str(len(rows)), rows, band["colour"], kind="metric")
        parts.append(svg)
        H = max(H, h)
    H += 90
    svg = (f'<svg viewBox="0 0 920 {H}" role="img" aria-labelledby="fig-{band["id"]}-t" class="sysfig">'
           f'<title id="fig-{band["id"]}-t">{esc(band["title"])}: metric groups and metrics</title>'
           f'<defs><pattern id="dt-{band["id"]}" width="14" height="14" patternUnits="userSpaceOnUse">'
           f'<circle cx="1" cy="1" r=".8" fill="#E4E6EB"/></pattern></defs>'
           f'<rect width="920" height="{H}" fill="url(#dt-{band["id"]})"/>{"".join(parts)}'
           f'<text x="30" y="{H - 22}" font-family="{MONO}" font-size="10" fill="{MUTED}">'
           f'one panel per metric group · the number is how many metrics it holds</text></svg>')
    alt = "; ".join(f'{g["title"].title()}: ' + ", ".join(t["label"] for t in g["topics"]) for g in groups)
    return svg, alt


def figure_html(n: int, svg: str, caption: str, alt: str | None = None) -> str:
    alt_html = (f'<details class="fig-alt"><summary>Text equivalent</summary><p>{esc(alt)}</p></details>'
                if alt else "")
    return (f'<figure class="sys fade"><div class="diagram-frame">{svg}</div>'
            f'<figcaption><b>Figure {n}.</b> {caption}</figcaption>{alt_html}</figure>')


# --------------------------------------------------------------------------- page chrome

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600'
         '&family=JetBrains+Mono:wght@400;500;600&display=swap">')

TABS = [("Map", "index.html#map"), ("Metrics", "index.html#catalogue"), ("Frameworks", "frameworks.html"),
        ("Glossary", "glossary.html"), ("Sources", "sources.html")]


def head(title: str, desc: str) -> str:
    return (f'<!DOCTYPE html>\n<html lang="en" data-theme="light">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{esc(title)}</title>\n<meta name="description" content="{esc(desc)}">\n'
            f'<link rel="icon" href="favicon.svg" type="image/svg+xml">\n{FONTS}\n'
            f'<link rel="stylesheet" href="assets/style.css">\n</head>\n')


def brand_mark() -> str:
    bars = "".join(f'<rect x="2" y="{2 + i * 3.4:.1f}" width="16" height="2.2" rx="1.1" fill="{c[0]}"/>'
                   for i, c in enumerate(BAND_COLOURS.values()))
    return f'<svg class="brand-mark" viewBox="0 0 20 20" width="20" height="20" aria-hidden="true">{bars}</svg>'


def topbar(site: dict, current: str) -> str:
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if t == current else ""}>{t}</a>' for t, h in TABS)
    return (f'<header class="topbar"><div class="topbar-inner">'
            f'<a class="brand" href="index.html">{brand_mark()}<span>{esc(site["title"])}</span></a>'
            f'<nav class="tabs" aria-label="Sections">{nav}</nav></div></header>')


def preview_banner(preview: bool) -> str:
    if not preview:
        return ""
    return ('<div class="preview-banner" role="note">Review build. Not published. The reader question and '
            'audience are still marked guesses in the review package.</div>')


def footer(site: dict, n_refs: int) -> str:
    sis = " · ".join(f'<a href="{esc(s["url"])}">{esc(s["title"])}</a>' for s in site.get("sister_maps", []))
    return (f'<footer class="footer"><div class="footer-inner"><div><div class="footer-title">'
            f'{esc(site["title"])}</div><p>Independent, vendor-neutral reference by '
            f'<a href="{esc(site["author_url"])}">{esc(site["author"])}</a>. Prose CC BY 4.0, tooling MIT.</p>'
            f'<p>{n_refs} sources, each checked on the date shown. <a href="sources.html">How sources are checked</a>.</p></div>'
            f'<div><p>Also: {sis}</p><p><a href="{esc(site["repo_url"])}">Source on GitHub</a></p></div>'
            f'</div></footer>')


def gradient_title(title: str, accent: str | None) -> str:
    t = esc(title)
    if accent and accent in title:
        a = esc(accent)
        return t.replace(a, f'<span class="grad">{a}</span>', 1)
    return t


def band_style(band) -> str:
    s, f, d = BAND_COLOURS[band["colour"]]
    return f"--c:{s};--f:{f};--d:{d}"


def h2(text: str, hid: str) -> str:
    return (f'<h2 id="{hid}" class="fade"><span class="h2tile">{icon(H2_ICONS.get(text, "book"), 15)}</span>'
            f'{esc(text)}</h2>')


def sources_list(ids: list[str], refs: dict) -> str:
    if not ids:
        return ('<p class="muted">No single public source defines this metric; it is defined here by common '
                'practice. The definition above is this site\'s statement of that practice.</p>')
    items = []
    for s in ids:
        r = refs[s]
        flag = "" if r.get("status") == "verified" else f' <span class="status">{esc(r.get("status"))}</span>'
        pub = f", {esc(r['published'])}" if r.get("published") else ""
        items.append(f'<li id="src-{esc(s)}"><a href="{esc(r["url"])}">{esc(r["title"])}</a>. {esc(r["org"])}'
                     f'{pub}. Checked {esc(r["accessed"])}.{flag}</li>')
    return f'<ol class="sources">{"".join(items)}</ol>'


def page_shell(site, title, desc, current, band, body, toc, n_refs, preview, crumbs) -> str:
    style = f' style="{band_style(band)}"' if band else ""
    aside = (f'<aside class="onpage" aria-label="On this page"><div class="onpage-inner"><div class="onpage-title">'
             f'On this page</div><ul>{toc}</ul></div></aside>') if toc else ""
    return head(f"{title} · {site['title']}", desc) + f"""<body class="topic"><a class="skip" href="#content">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
{topbar(site, current)}{preview_banner(preview)}
<main id="content" class="topic-main"{style}>
<div class="wrap topic-grid">
<article class="prose">
<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">{icon("map", 15)}{esc(site["short_title"])}</a>{crumbs}</nav>
{body}
</article>
{aside}
</div></main>
<a class="backpill" href="index.html#map">{icon("map", 16)}Back to the map</a>
{footer(site, n_refs)}
<script src="assets/app.js"></script>
</body></html>"""


def toc_of(sections: list[tuple[str, str]]) -> str:
    return "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for t, i in sections)


# --------------------------------------------------------------------------- metric pages

def render_metric(site, m, metrics, refs, n_refs, preview) -> str:
    band = m["band"]
    group = next(g for g in band["groups"] if g["id"] == m["group"])
    custom = CONTENT / "diagrams" / f"{m['id']}.svg"
    if custom.exists():
        svg = re.sub(r"<\?xml.*?\?>", "", custom.read_text(encoding="utf-8")).replace(
            'xmlns="http://www.w3.org/2000/svg" ', "", 1)
        cap = re.search(r"<title[^>]*>(.*?)</title>", svg, re.S).group(1)
        alt = re.search(r"<desc[^>]*>(.*?)</desc>", svg, re.S)
        fig = figure_html(1, svg, esc(cap) + ".", alt.group(1) if alt else None)
    else:
        svg, alt = metric_figure(m, metrics)
        fig = figure_html(1, svg, f"Where {esc(m['label'].lower())} comes from, and the metrics that "
                                  f"show when it misleads.", alt)
    srcs = page_sources(m)

    def cite(s):
        return f' <a class="cite" href="#src-{esc(s)}" aria-label="Source {srcs.index(s) + 1}">[{srcs.index(s) + 1}]</a>'

    def_cite = "".join(cite(s) for s in (m.get("sources") or [])[:2])
    findings = m.get("findings") or []
    sec = [("Definition", "definition"), ("Formula", "formula"), ("Why it matters", "why-it-matters"),
           ("How to measure", "how-to-measure"), ("How AI changes it", "how-ai-changes-it")]
    if findings:
        sec.append(("What the research shows", "what-the-research-shows"))
    sec += [("Pitfalls", "pitfalls"), ("Related", "related"), ("Sources", "sources")]
    pit = "".join(f'<li>{esc(p["text"])} <span class="balance">Read with <a href="{p["balance"]}.html">'
                  f'{esc(metrics[p["balance"]]["label"])}</a>.</span></li>' for p in m["pitfalls"])
    rel = "".join(f'<li><a href="{r}.html">{esc(metrics[r]["label"])}</a> <span class="muted">· '
                  f'{esc(metrics[r]["summary"])}</span></li>' for r in m["related"])
    fnd = "".join(f'<li>{esc(f["text"])}{cite(f["source"])}</li>' for f in findings)
    research = (h2("What the research shows", "what-the-research-shows") + f'<ul class="findings">{fnd}</ul>'
                '<p class="muted small">Each figure is that source\'s own finding for its own population. '
                'None is a target.</p>') if findings else ""
    disagree = (f'<p class="note"><b>Definitions differ.</b> {esc(m["disagreements"])}</p>'
                if m.get("disagreements") else "")
    levels = ", ".join(m.get("levels") or [])
    body = f"""<div class="kicker band-k"><span class="cat-icon">{icon(band["icon"], 14)}</span>{esc(band["title"])} · {esc(group["title"].title())}</div>
<h1>{esc(m.get("title") or m["label"])}</h1>
<p class="lede">{esc(m["summary"])}</p>
<dl class="facts"><div><dt>Unit</dt><dd>{esc(m["unit"])}</dd></div><div><dt>Better when</dt><dd>{esc(m["direction"])}</dd></div><div><dt>Use at</dt><dd>{esc(levels)} level</dd></div><div><dt>Origin</dt><dd>{esc(m["origin"])}</dd></div></dl>
{h2("Definition", "definition")}<p>{esc(m["definition"])}{def_cite}</p>{disagree}
{h2("Formula", "formula")}<div class="formula"><span class="formula-k">FORMULA</span><code>{esc(m["formula"])}</code><span class="formula-u">unit · {esc(m["unit"])}</span></div>
{h2("Why it matters", "why-it-matters")}<p>{esc(m["why"])}</p>
{h2("How to measure", "how-to-measure")}{fig}<p>{esc(m["measure"])}</p>
{h2("How AI changes it", "how-ai-changes-it")}<p>{esc(m["ai"])}</p>
{research}
{h2("Pitfalls", "pitfalls")}<ul>{pit}</ul>
{h2("Related", "related")}<ul class="related">{rel}</ul>
{h2("Sources", "sources")}{sources_list(srcs, refs)}"""
    crumbs = (f'<span>/</span><a href="{band["id"]}.html">{esc(band["title"])}</a>'
              f'<span>/</span><span aria-current="page">{esc(m["label"])}</span>')
    return page_shell(site, m["label"], m["summary"], "Metrics", band, body, toc_of(sec), n_refs, preview, crumbs)


# --------------------------------------------------------------------------- dimension pages

def render_dimension(site, n, band, n_refs, preview) -> str:
    svg, alt = dimension_figure(band)
    fig = figure_html(1, svg, f"The metric groups in {esc(band['title'])}.", alt)
    groups = "".join(
        f'<h3 class="grp-h" id="{g["id"]}">{esc(g["title"].title())}</h3><ul class="metric-list">'
        + "".join(f'<li><a href="{t["id"]}.html">{esc(t["label"])}</a><span>{esc(t["summary"])}</span></li>'
                  for t in g["topics"]) + "</ul>" for g in band["groups"])
    sec = [("What it covers", "what-it-covers"), ("Metrics in this dimension", "metrics"),
           ("How these metrics balance", "balance"), ("Who uses it", "who")]
    body = f"""<div class="kicker band-k"><span class="cat-icon">{icon(band["icon"], 14)}</span>Dimension {n:02d} of 05</div>
<h1>{esc(band["title"])}</h1>
<p class="lede">{esc(band["summary"])}</p>
{h2("What it covers", "what-it-covers")}<p>{esc(band["covers"])}</p>{fig}
{h2("Metrics in this dimension", "metrics")}{groups}
{h2("How these metrics balance", "balance")}<p>{esc(band["balance"])}</p>
{h2("Who uses it", "who")}<p>{esc(band["who"])}</p>"""
    crumbs = f'<span>/</span><span aria-current="page">{esc(band["title"])}</span>'
    return page_shell(site, band["title"], band["summary"], "Metrics", band, body, toc_of(sec), n_refs, preview, crumbs)


# --------------------------------------------------------------------------- reference pages

def render_markdown_page(site, page, metrics, refs, n_refs, preview) -> str:
    def metric_list(mt):
        key = mt.group(1).strip().lower()
        items = [m for m in metrics.values() if m["origin"].lower().startswith(key)
                 or f"{key} " in m["origin"].lower() or f"({key}" in m["origin"].lower()]
        return ("\n\n<ul class=\"metric-list compact\">" + "".join(
            f'<li><a href="{m["id"]}.html">{esc(m["label"])}</a><span>{esc(m["band"]["title"])}</span></li>'
            for m in items) + "</ul>\n\n")
    body = re.sub(r"\{\{metrics:([^}]+)\}\}", metric_list, page["body"])
    md = markdown.Markdown(extensions=["toc", "tables", "attr_list"])
    out = md.convert(body)
    out = out.replace('<h2 id="sources">Sources</h2>',
                      '<h2 id="sources">Sources</h2>' + sources_list(page.get("sources") or [], refs))
    out = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', lambda mt: h2(re.sub("<.*?>", "", mt.group(2)), mt.group(1)), out)
    toc = "".join(f'<li><a href="#{t["id"]}">{esc(t["name"])}</a></li>' for t in md.toc_tokens)
    hdr = (f'<div class="kicker"><span class="dot"></span>Reference</div>'
           f'<h1>{gradient_title(page["title"], page.get("title_accent"))}</h1>'
           f'<p class="lede">{esc(page["summary"])}</p>')
    crumbs = f'<span>/</span><span aria-current="page">{esc(page["title"])}</span>'
    return page_shell(site, page["title"], page["summary"], "Frameworks" if page["id"] == "frameworks" else "",
                      None, hdr + out, toc, n_refs, preview, crumbs)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def render_glossary(site, glossary, refs, n_refs, preview) -> str:
    items = []
    for g in sorted(glossary, key=lambda x: x["term"].lower()):
        src = ""
        if g.get("source"):
            src = f' <a href="sources.html#src-{esc(g["source"])}">Source</a>.'
        coined = ' <span class="status">coined</span>' if "coined" in g["origin"].lower() else ""
        items.append(f'<div class="gl-item" id="{slug(g["term"])}"><dt>{esc(g["term"])}{coined}</dt>'
                     f'<dd>{esc(g["definition"])} <span class="muted">Origin: {esc(g["origin"])}.</span>{src}</dd></div>')
    body = (f'<div class="kicker"><span class="dot"></span>Reference</div><h1>Glossary</h1>'
            f'<p class="lede">The terms used on this map, each credited to whoever introduced it. Terms this site '
            f'introduces are marked coined.</p><dl class="glossary">{"".join(items)}</dl>')
    crumbs = '<span>/</span><span aria-current="page">Glossary</span>'
    return page_shell(site, "Glossary", "Terms used on the AI SDLC Metrics & KPIs Map, with their originators.",
                      "Glossary", None, body, "", n_refs, preview, crumbs)


def render_sources(site, refs, metrics, pages, n_refs, preview) -> str:
    used: dict[str, list] = {}
    for m in metrics.values():
        for s in page_sources(m):
            used.setdefault(s, []).append((f'{m["id"]}.html', m["label"]))
    for p in pages.values():
        for s in p.get("sources") or []:
            used.setdefault(s, []).append((f'{p["id"]}.html', p["title"]))
    rows = []
    for rid, r in refs.items():
        users = used.get(rid, [])
        if not users:
            continue
        cites = ", ".join(f'<a href="{h}">{esc(t)}</a>' for h, t in users)
        claims = "".join(f"<li>{esc(c)}</li>" for c in r.get("claims") or [])
        note = f'<p class="muted small">{esc(r["note"])}</p>' if r.get("note") else ""
        rows.append(f'<section class="src" id="src-{esc(rid)}"><h3><a href="{esc(r["url"])}">{esc(r["title"])}</a> '
                    f'<span class="status s-{esc(r.get("status"))}">{esc(r.get("status"))}</span></h3>'
                    f'<p class="muted small">{esc(r["org"])} · published {esc(r.get("published") or "no date shown")} · '
                    f'checked {esc(r["accessed"])}</p>'
                    f'<details><summary>What this source confirms</summary><ul>{claims}</ul>{note}</details>'
                    f'<p class="small">Cited on: {cites}</p></section>')
    body = (f'<div class="kicker"><span class="dot"></span>Reference</div><h1>Sources</h1>'
            f'<p class="lede">Every source this map cites, with the claims confirmed on the page and the date it '
            f'was checked.</p><p><b>Verified</b> means the page was opened and each listed claim found there. '
            f'<b>Partial</b> means the page was opened but only the listed claims were confirmed, so the site cites it '
            f'for those claims only. Sources that could not be opened are not cited.</p>' + "".join(rows))
    crumbs = '<span>/</span><span aria-current="page">Sources</span>'
    return page_shell(site, "Sources", "The source register for the AI SDLC Metrics & KPIs Map.", "Sources", None,
                      body, "", n_refs, preview, crumbs)


# --------------------------------------------------------------------------- home page

def build_home(site, mp, metrics, svg, n_refs, preview) -> str:
    legend = "".join(
        f'<button class="chip" type="button" data-band="{esc(b["id"])}" aria-pressed="false" style="{band_style(b)}">'
        f'{icon(b["icon"], 15)}<span>{esc(b["title"])}</span></button>' for b in mp["bands"])
    routes = []
    for r in site.get("routes", []):
        items = "".join(f'<li><a href="{t}.html">{esc(metrics[t]["label"])}</a></li>' for t in r["topics"])
        if r["id"] == "lookup":
            items = ('<li><a href="#catalogue">All metrics, by dimension</a></li><li><a href="frameworks.html">'
                     'Frameworks</a></li><li><a href="latest.html">What changed this month</a></li><li><a href="glossary.html">Glossary</a></li><li><a href="sources.html">'
                     'Sources</a></li>')
        routes.append(f'<div class="card fade"><div class="tile">{icon(r["icon"], 18)}</div>'
                      f'<h3>{esc(r["title"])}</h3><p>{esc(r["blurb"])}</p><ul>{items}</ul></div>')
    cat = []
    for n, b in enumerate(mp["bands"], 1):
        groups = "".join(
            f'<div class="cat-group"><div class="cat-gh">{esc(g["title"])}</div><ul>'
            + "".join(f'<li><a href="{t["id"]}.html">{esc(t["label"])}</a></li>' for t in g["topics"])
            + "</ul></div>" for g in b["groups"])
        cat.append(f'<section class="cat-band fade" style="{band_style(b)}">'
                   f'<h3><span class="cat-icon">{icon(b["icon"], 16)}</span><a href="{b["id"]}.html">{n:02d} · '
                   f'{esc(b["title"])}</a></h3><p class="muted">{esc(b["summary"])}</p>'
                   f'<div class="cat-groups">{groups}</div></section>')
    n_groups = sum(len(b["groups"]) for b in mp["bands"])
    body = f"""<body class="home"><a class="skip" href="#content">Skip to content</a>
{topbar(site, "Map")}{preview_banner(preview)}
<main id="content">
<section class="hero"><div class="wrap">
<div class="kicker"><span class="dot"></span>AI SDLC · Metrics and KPIs reference</div>
<h1>{gradient_title(site["headline"], site.get("headline_accent"))}</h1>
<p class="lede">{esc(site["about"])}</p>
<div class="hero-actions"><a class="btn primary" href="#map">Explore the map {icon("arrow", 16)}</a>
<a class="btn" href="#routes">Choose by purpose</a></div>
<div class="stats">
<div class="stat">{icon("layers", 18)}<b>{len(mp["bands"])}</b><span>dimensions</span></div>
<div class="stat">{icon("rising", 18)}<b>{len(metrics)}</b><span>metrics, each with its own page</span></div>
<div class="stat">{icon("search", 18)}<b>{n_refs}</b><span>sources, each checked</span></div>
</div></div></section>

<section class="section" id="map"><div class="wrap wide">
<div class="section-head fade"><h2>The map</h2>
<p class="muted">Start with the big picture. Use the chips to focus a dimension, select a dimension's label to read its overview, and select a metric to open its page.</p></div>
<div class="legend" role="group" aria-label="Focus a dimension">{legend}</div>
<figure class="diagram fade"><div class="diagram-frame">{svg}</div>
<figcaption><b>Figure 1.</b> {esc(site["title"])}: five dimensions, {n_groups} metric groups and {len(metrics)} metrics.
Dashed boxes are measured across the whole flow of work. The same content is listed as text under
<a href="#catalogue">All metrics</a>. <a class="dl" href="ai-sdlc-metrics-map.svg">{icon("download", 14)} SVG</a></figcaption>
</figure></div></section>

<section class="section alt" id="routes"><div class="wrap">
<div class="section-head fade"><h2>Choose by purpose</h2>
<p class="muted">Each route starts from a question you have today and picks a balanced handful of metrics.</p></div>
<div class="cards">{"".join(routes)}</div></div></section>

<section class="section" id="catalogue"><div class="wrap">
<div class="section-head fade"><h2>All metrics</h2>
<p class="muted">The text route through the map: every dimension, group and metric in map order.</p></div>
{"".join(cat)}
<div class="principle fade"><h3>{icon("scale", 18)} Read every metric with another</h3><p>Each metric page names the
metrics that show when it misleads. Speed is read with stability, adoption with impact, and survey results with system
data. No metric on this map is meant for ranking individuals.</p></div>
</div></section>
</main>
{footer(site, n_refs)}
<div class="tip" role="tooltip" aria-hidden="true"></div>
<script src="assets/app.js"></script>
</body></html>"""
    return head(site["title"], site["about"]) + body


# --------------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true", help="review build with a banner")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args(argv)

    site, mp, metrics, refs, glossary, pages, errs = load_content()
    errs += check(site, mp, metrics, refs, glossary, pages, release=not a.preview)
    if errs:
        print(("Preview" if a.preview else "Release") + " build refused:\n  - " + "\n  - ".join(errs),
              file=sys.stderr)
        return 1

    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    for f in ASSETS.iterdir():
        shutil.copy2(f, out / "assets" / f.name)
    shutil.copy2(ROOT / "site" / "favicon.svg", out / "favicon.svg")
    cited = {s for m in metrics.values() for s in page_sources(m)} | {
        s for p in pages.values() for s in p.get("sources") or []}
    n_refs = len(cited)

    svg = build_map(mp, site["title"])
    (out / "ai-sdlc-metrics-map.svg").write_text(
        svg.replace('<svg class="overview" ', '<svg class="overview" style="font-family:Inter,sans-serif" ', 1),
        encoding="utf-8")
    (out / "index.html").write_text(build_home(site, mp, metrics, svg, n_refs, a.preview), encoding="utf-8")
    for m in metrics.values():
        (out / f"{m['id']}.html").write_text(render_metric(site, m, metrics, refs, n_refs, a.preview), encoding="utf-8")
    for n, b in enumerate(mp["bands"], 1):
        (out / f"{b['id']}.html").write_text(render_dimension(site, n, b, n_refs, a.preview), encoding="utf-8")
    for p in pages.values():
        (out / f"{p['id']}.html").write_text(render_markdown_page(site, p, metrics, refs, n_refs, a.preview),
                                             encoding="utf-8")
    (out / "glossary.html").write_text(render_glossary(site, glossary, refs, n_refs, a.preview), encoding="utf-8")
    (out / "sources.html").write_text(render_sources(site, refs, metrics, pages, n_refs, a.preview), encoding="utf-8")
    total = 1 + len(metrics) + len(mp["bands"]) + len(pages) + 2
    print(f"Built {total} pages into {out} ({'preview' if a.preview else 'release'} build): "
          f"{len(metrics)} metrics, {len(mp['bands'])} dimensions, {n_refs} sources cited.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
