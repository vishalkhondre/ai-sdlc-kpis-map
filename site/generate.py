#!/usr/bin/env python3
"""Build the AI SDLC Metrics & KPIs Map site from content/ into _site/.

    python site/generate.py            # release build: refuses provisional inventory and sample pages
    python site/generate.py --preview  # review build: includes sample pages and a preview banner

One topic inventory (content/map.yml) drives the overview map SVG, the text route, the purpose
routes and the page navigation. Links key on stable topic IDs (SOP "The pattern"); a topic without a
finished page renders as a plain label (GR-3.2). Visual rules follow the locked AI SDLC design system
v1.0 (see project/DECISIONS.md, D-003).
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
}

H2_ICONS = {
    "Definition": "book", "Formula": "sigma", "Why it matters": "flag", "How to measure": "gauge",
    "How AI changes it": "bot", "Pitfalls": "alert", "Related": "link", "Sources": "search",
    "What it covers": "book", "Who uses them": "flag",
}


def icon(name: str, size: int = 18, colour: str = "currentColor", cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{colour}" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            f'focusable="false"><path d="{ICONS[name]}"/></svg>')


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


# --------------------------------------------------------------------------- content loading

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


FRONT = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


def load_pages(include_samples: bool) -> dict[str, dict]:
    pages = {}
    for p in sorted((CONTENT / "pages").glob("*.md")):
        m = FRONT.match(p.read_text(encoding="utf-8"))
        if not m:
            raise SystemExit(f"{p}: missing front matter")
        meta = yaml.safe_load(m.group(1)) or {}
        meta["body"] = m.group(2)
        meta["path"] = p
        if meta.get("sample") and not include_samples:
            continue
        pages[meta["id"]] = meta
    return pages


def index_topics(mp: dict) -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for band in mp["bands"]:
        for group in band["groups"]:
            for t in group["topics"]:
                if t["id"] in idx:
                    raise SystemExit(f"duplicate topic id: {t['id']}")
                idx[t["id"]] = {**t, "band": band, "group": group}
    return idx


# --------------------------------------------------------------------------- overview map SVG

MAP_W = 1200
LABEL_X, LABEL_W = 22, 262
AREA_X = LABEL_X + LABEL_W + 18
AREA_W = MAP_W - AREA_X - 22
NODE_H1, NODE_H2, NODE_H3, NODE_GAP, COL_GAP = 32, 46, 60, 8, 12
CHAR_W = 6.9  # Inter 500 at 12.5px, measured average


def wrap(label: str, width: float) -> list[str]:
    limit = max(8, int((width - 20) / CHAR_W))
    words, lines, cur = label.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > limit:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return lines[:3]


def build_map(mp: dict, linked: dict[str, str], title: str = "AI SDLC Metrics & KPIs Map") -> str:
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
        g_out = [f'<g class="band" data-band="{esc(band["id"])}">',
                 f'<rect class="band-bg" x="10" y="{y}" width="{MAP_W - 20}" height="{band_h}" rx="8" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>']
        # label box
        lx, ly, lh = LABEL_X, y + 10, band_h - 20
        g_out.append(f'<g class="band-label" tabindex="0" role="button" aria-label="Focus {esc(band["title"])}" '
                     f'data-band="{esc(band["id"])}">'
                     f'<rect x="{lx}" y="{ly}" width="{LABEL_W}" height="{lh}" rx="6" fill="#fff" '
                     f'stroke="{stroke}" stroke-opacity=".55"/>'
                     f'<text x="{lx + 14}" y="{ly + 24}" class="bl-num" fill="{dark}">{n:02d} · '
                     f'{esc(band["title"].upper())}</text>'
                     f'<text x="{lx + 14}" y="{ly + 44}" class="bl-role">{esc(band["role"])}</text>')
        for i, note in enumerate(band.get("notes", [])[:3]):
            g_out.append(f'<text x="{lx + 14}" y="{ly + 64 + i * 16}" class="bl-note">{esc(note)}</text>')
        g_out.append(f'<g transform="translate({lx + LABEL_W - 32},{ly + lh - 32}) scale(.83)" fill="none" '
                     f'stroke="{dark}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
                     f'<path d="{ICONS[band["icon"]]}"/></g></g>')
        # groups
        for c, (g, nodes) in enumerate(cols):
            gx = AREA_X + c * (colw + COL_GAP)
            g_out.append(f'<text x="{gx + 2:.1f}" y="{y + 26}" class="grp" fill="{dark}">{esc(g["title"])}</text>')
            for t, lines, dy, nh in nodes:
                ny = y + 36 + dy
                dash = ' stroke-dasharray="4 3"' if g.get("dashed") else ""
                rect = (f'<rect x="{gx:.1f}" y="{ny}" width="{colw:.1f}" height="{nh}" rx="5" fill="#fff" '
                        f'stroke="{stroke}"{dash}/>')
                tx = f'{gx + 10:.1f}'
                if len(lines) == 1:
                    txt = f'<text x="{tx}" y="{ny + 20.5}" class="maplabel" fill="{dark}">{esc(lines[0])}</text>'
                else:
                    txt = (f'<text x="{tx}" y="{ny + 19}" class="maplabel" fill="{dark}">{esc(lines[0])}'
                           + "".join(f'<tspan x="{tx}" dy="15">{esc(ln)}</tspan>' for ln in lines[1:])
                           + '</text>')
                if t["id"] in linked:
                    g_out.append(f'<a class="maplink" href="{esc(linked[t["id"]])}" data-topic="{esc(t["id"])}" '
                                 f'data-dest="{esc(band["title"])}" aria-label="{esc(t["label"])}">{rect}{txt}</a>')
                else:
                    g_out.append(f'<g class="mapnode" data-topic="{esc(t["id"])}">{rect}{txt}</g>')
        g_out.append("</g>")
        parts.append("".join(g_out))
        y += band_h + 14
    h = y
    return (f'<svg class="overview" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {MAP_W} {h}" '
            f'role="img" aria-labelledby="map-title map-desc">'
            f'<title id="map-title">{esc(title)}</title>'
            f'<desc id="map-desc">Five dimensions an enterprise measures when AI joins software delivery, '
            f'each with its metric groups. The same content is listed as text below the map.</desc>'
            + "".join(parts) + "</svg>")


# --------------------------------------------------------------------------- page chrome

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600'
         '&family=JetBrains+Mono:wght@400;500;600&display=swap">')


def head(site: dict, title: str, desc: str) -> str:
    return (f'<!DOCTYPE html>\n<html lang="en" data-theme="light">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{esc(title)}</title>\n<meta name="description" content="{esc(desc)}">\n'
            f'<link rel="icon" href="favicon.svg" type="image/svg+xml">\n{FONTS}\n'
            f'<link rel="stylesheet" href="assets/style.css">\n</head>\n')


def topbar(site: dict, current: str) -> str:
    tabs = [("Map", "index.html#map"), ("Metrics", "index.html#catalogue"), ("Routes", "index.html#routes")]
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if t == current else ""}>{t}</a>' for t, h in tabs)
    return (f'<header class="topbar"><div class="topbar-inner">'
            f'<a class="brand" href="index.html">{brand_mark()}<span>{esc(site["title"])}</span></a>'
            f'<nav class="tabs" aria-label="Sections">{nav}</nav></div></header>')


def brand_mark() -> str:
    cols = [c[0] for c in BAND_COLOURS.values()]
    bars = "".join(f'<rect x="2" y="{2 + i * 3.4}" width="16" height="2.2" rx="1.1" fill="{c}"/>'
                   for i, c in enumerate(cols))
    return f'<svg class="brand-mark" viewBox="0 0 20 20" width="20" height="20" aria-hidden="true">{bars}</svg>'


def preview_banner(preview: bool) -> str:
    if not preview:
        return ""
    return ('<div class="preview-banner" role="note">Review build. The map inventory is provisional and '
            'pages marked as layout samples are not final content. Nothing here is published.</div>')


def footer(site: dict) -> str:
    sis = " · ".join(f'<a href="{esc(s["url"])}">{esc(s["title"])}</a>' for s in site.get("sister_maps", []))
    return (f'<footer class="footer"><div class="footer-inner"><div><div class="footer-title">'
            f'{esc(site["title"])}</div><p>Independent, vendor-neutral reference by '
            f'<a href="{esc(site["author_url"])}">{esc(site["author"])}</a>. Prose CC BY 4.0, tooling MIT.</p></div>'
            f'<div><p>Also: {sis}</p><p><a href="{esc(site["repo_url"])}">Source on GitHub</a></p></div>'
            f'</div></footer>')


def gradient_title(title: str, accent: str | None) -> str:
    t = esc(title)
    if accent and accent in title:
        a = esc(accent)
        return t.replace(a, f'<span class="grad">{a}</span>', 1)
    return t


# --------------------------------------------------------------------------- home page

def build_home(site, mp, topics, pages, svg, preview) -> str:
    linked = {tid for tid in topics if tid in pages}
    n_topics = len(topics)
    legend = "".join(
        f'<button class="chip" type="button" data-band="{esc(b["id"])}" aria-pressed="false" '
        f'style="--c:{BAND_COLOURS[b["colour"]][0]};--f:{BAND_COLOURS[b["colour"]][1]};--d:{BAND_COLOURS[b["colour"]][2]}">'
        f'{icon(b["icon"], 15, "currentColor")}<span>{esc(b["title"])}</span></button>'
        for b in mp["bands"])

    def topic_link(tid):
        t = topics[tid]
        if tid in linked:
            return f'<a href="{tid}.html">{esc(t["label"])}</a>'
        return f'<span class="plain">{esc(t["label"])}</span>'

    routes = []
    for r in site.get("routes", []):
        items = "".join(f"<li>{topic_link(t)}</li>" for t in r["topics"] if t in topics)
        if r["id"] == "lookup":
            items = '<li><a href="#catalogue">All metrics, by dimension</a></li>'
        routes.append(f'<div class="card fade"><div class="tile">{icon(r["icon"], 18)}</div>'
                      f'<h3>{esc(r["title"])}</h3><p>{esc(r["blurb"])}</p><ul>{items}</ul></div>')

    cat = []
    for n, b in enumerate(mp["bands"], 1):
        s, f, d = BAND_COLOURS[b["colour"]]
        groups = "".join(
            f'<div class="cat-group"><div class="cat-gh">{esc(g["title"])}</div><ul>'
            + "".join(f"<li>{topic_link(t['id'])}</li>" for t in g["topics"]) + "</ul></div>"
            for g in b["groups"])
        cat.append(f'<section class="cat-band fade" style="--c:{s};--f:{f};--d:{d}">'
                   f'<h3><span class="cat-icon">{icon(b["icon"], 16)}</span>{n:02d} · {esc(b["title"])}</h3>'
                   f'<p class="muted">{esc(b["role"])}.</p><div class="cat-groups">{groups}</div></section>')

    body = f"""<body class="home"><a class="skip" href="#content">Skip to content</a>
{topbar(site, "Map")}{preview_banner(preview)}
<main id="content">
<section class="hero"><div class="wrap">
<div class="kicker"><span class="dot"></span>AI SDLC · Metrics reference</div>
<h1>{gradient_title(site["headline"], site.get("headline_accent"))}</h1>
<p class="lede">{esc(site["about"])}</p>
<div class="hero-actions"><a class="btn primary" href="#map">Explore the map {icon("arrow", 16)}</a>
<a class="btn" href="#catalogue">Browse all metrics</a></div>
<div class="stats">
<div class="stat">{icon("layers", 18)}<b>{len(mp["bands"])}</b><span>dimensions</span></div>
<div class="stat">{icon("rising", 18)}<b>{n_topics}</b><span>metrics on the map</span></div>
<div class="stat">{icon("book", 18)}<b>1</b><span>page per metric</span></div>
</div></div></section>

<section class="section" id="map"><div class="wrap wide">
<div class="section-head fade"><h2>The map</h2>
<p class="muted">Start with the big picture. Point at a dimension to focus it, and select a metric to open its page.</p></div>
<div class="legend" role="group" aria-label="Focus a dimension">{legend}</div>
<figure class="diagram fade"><div class="diagram-frame">{svg}</div>
<figcaption><b>Figure 1.</b> {esc(site["title"])}: five dimensions, their metric groups and
{n_topics} metrics. Dashed boxes span the whole lifecycle. The same content is listed as text under
<a href="#catalogue">All metrics</a>. <a class="dl" href="ai-sdlc-metrics-map.svg" download>{icon("download", 14)} SVG</a></figcaption>
</figure></div></section>

<section class="section alt" id="routes"><div class="wrap">
<div class="section-head fade"><h2>Choose by purpose</h2>
<p class="muted">Each route starts from a question you have today.</p></div>
<div class="cards">{"".join(routes)}</div></div></section>

<section class="section" id="catalogue"><div class="wrap">
<div class="section-head fade"><h2>All metrics</h2>
<p class="muted">The text route through the map: every dimension, group and metric in map order.</p></div>
{"".join(cat)}</div></section>
</main>
{footer(site)}
<div class="tip" role="tooltip" aria-hidden="true"></div>
<script src="assets/app.js"></script>
</body></html>"""
    return head(site, f'{site["title"]} — {site["tagline"]}', site["about"]) + body


# --------------------------------------------------------------------------- topic pages

def render_page(site, mp, topics, pages, page, preview) -> str:
    t = topics.get(page["id"])
    band = t["band"] if t else next(b for b in mp["bands"] if b["id"] == page["band"])
    s, f, d = BAND_COLOURS[band["colour"]]
    figs = {}

    def fig_sub(m):
        name = m.group(1)
        svg = (CONTENT / "diagrams" / f"{name}.svg").read_text(encoding="utf-8")
        svg = re.sub(r"<\?xml.*?\?>", "", svg).replace('xmlns="http://www.w3.org/2000/svg" ', "", 1)
        n = len(figs) + 1
        title = re.search(r"<title[^>]*>(.*?)</title>", svg, re.S).group(1)
        figs[name] = n
        token = f"FIGURE{n}TOKEN"
        figs[token] = (f'<figure class="sys fade"><div class="diagram-frame">{svg}</div>'
                       f'<figcaption><b>Figure {n}.</b> {title}.</figcaption></figure>')
        return f"\n\n{token}\n\n"

    body = re.sub(r"\{\{figure:([\w-]+)\}\}", fig_sub, page["body"])
    body = body.replace("{{formula}}", "FORMULATOKEN")
    md = markdown.Markdown(extensions=["toc", "tables", "fenced_code", "attr_list"])
    out = md.convert(body)
    for k, v in figs.items():
        if k.startswith("FIGURE"):
            out = out.replace(f"<p>{k}</p>", v)
    if page.get("formula"):
        out = out.replace("<p>FORMULATOKEN</p>",
                          f'<div class="formula"><span class="formula-k">FORMULA</span>'
                          f'<code>{esc(page["formula"])}</code>'
                          f'<span class="formula-u">unit · {esc(page.get("unit", ""))}</span></div>')

    # Related: generated from front matter, plain label when the target has no page.
    rel = []
    for rid in page.get("related", []):
        if rid in topics:
            lab = esc(topics[rid]["label"])
            rel.append(f'<li><a href="{rid}.html">{lab}</a></li>' if rid in pages else f'<li><span class="plain">{lab}</span></li>')
    out = out.replace("<h2 id=\"related\">Related</h2>",
                      f'<h2 id="related">Related</h2><ul class="related">{"".join(rel)}</ul>')
    srcs = page.get("sources") or []
    src_html = ("<ol class=\"sources\">" + "".join(f"<li>{esc(x)}</li>" for x in srcs) + "</ol>") if srcs else (
        '<p class="muted">Sources are filled from the research register.</p>' if page.get("sample") else "")
    out = out.replace("<h2 id=\"sources\">Sources</h2>", f'<h2 id="sources">Sources</h2>{src_html}')

    # h2 icon tiles
    def h2_tile(m):
        text = re.sub("<.*?>", "", m.group(2))
        ic = H2_ICONS.get(text, "book")
        return f'<h2 id="{m.group(1)}" class="fade"><span class="h2tile">{icon(ic, 15)}</span>{m.group(2)}</h2>'
    out = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', h2_tile, out)

    toc = "".join(f'<li><a href="#{tok["id"]}">{esc(tok["name"])}</a></li>' for tok in md.toc_tokens)
    sample = ('<div class="sample-note">Layout sample. This page shows the structure every metric page '
              'follows; its wording is not final.</div>') if page.get("sample") else ""
    group = t["group"]["title"].title() if t else ""
    html_out = f"""<body class="topic"><a class="skip" href="#content">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
{topbar(site, "Metrics")}{preview_banner(preview)}
<main id="content" class="topic-main" style="--c:{s};--f:{f};--d:{d}">
<div class="wrap topic-grid">
<article class="prose">
<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">{icon("map", 15)}{esc(site["short_title"])}</a>
<span>/</span><a href="index.html#catalogue">{esc(band["title"])}</a><span>/</span><span aria-current="page">{esc(page["title"])}</span></nav>
<div class="kicker band-k"><span class="cat-icon">{icon(band["icon"], 14)}</span>{esc(band["title"])}{" · " + esc(group) if group else ""}</div>
<h1>{gradient_title(page["title"], page.get("title_accent"))}</h1>
<p class="lede">{esc(page["summary"])}</p>
{sample}
{out}
</article>
<aside class="onpage"><div class="onpage-inner"><div class="onpage-title">On this page</div><ul>{toc}</ul></div></aside>
</div></main>
<a class="backpill" href="index.html#map">{icon("map", 16)}Back to the map</a>
{footer(site)}
<script src="assets/app.js"></script>
</body></html>"""
    return head(site, f'{page["title"]} — {site["title"]}', page["summary"]) + html_out


# --------------------------------------------------------------------------- checks + main

def check_release(mp, pages):
    errors = []
    if mp.get("status") == "provisional":
        errors.append("content/map.yml is provisional (GR-3.2): replace it with the researched inventory")
    for p in pages.values():
        if p.get("sample"):
            errors.append(f"{p['path'].name} is a layout sample and cannot be released (GR-3.2)")
    return errors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true", help="review build: include sample pages and banner")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args(argv)

    site = load_yaml(CONTENT / "site.yml")
    mp = load_yaml(CONTENT / "map.yml")
    topics = index_topics(mp)
    pages = load_pages(include_samples=a.preview)

    if not a.preview:
        errs = check_release(mp, load_pages(include_samples=True))
        if errs:
            print("Release build refused:\n  - " + "\n  - ".join(errs), file=sys.stderr)
            return 1

    for pid, p in pages.items():
        if pid not in topics and p.get("type") != "dimension":
            raise SystemExit(f"{p['path'].name}: id '{pid}' is not a topic in content/map.yml")
        for rid in p.get("related", []):
            if rid not in topics:
                raise SystemExit(f"{p['path'].name}: related id '{rid}' is not in content/map.yml")

    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    for f in ASSETS.iterdir():
        shutil.copy2(f, out / "assets" / f.name)
    shutil.copy2(ROOT / "site" / "favicon.svg", out / "favicon.svg")

    linked = {tid: f"{tid}.html" for tid in topics if tid in pages}
    svg = build_map(mp, linked, site["title"])
    (out / "ai-sdlc-metrics-map.svg").write_text(
        svg.replace('<svg class="overview" ', '<svg class="overview" style="font-family:Inter,sans-serif" ', 1),
        encoding="utf-8")
    (out / "index.html").write_text(build_home(site, mp, topics, pages, svg, a.preview), encoding="utf-8")
    for pid, p in pages.items():
        (out / f"{pid}.html").write_text(render_page(site, mp, topics, pages, p, a.preview), encoding="utf-8")
    print(f"Built {1 + len(pages)} pages into {out} ({'preview' if a.preview else 'release'} build); "
          f"{len(linked)} of {len(topics)} map topics linked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
