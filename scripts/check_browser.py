"""Browser checks against a preview build (design system "Interaction and motion"; SOP step 6).
Run: python site/generate.py --preview && python scripts/check_browser.py [site-dir]"""
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

SITE = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "_site")
fails = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


with sync_playwright() as p:
    exe = os.environ.get("CHROMIUM_PATH")  # optional: use a preinstalled Chromium
    b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    pg = b.new_page(viewport={"width": 1360, "height": 900})
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto((SITE / "index.html").as_uri())
    link = pg.locator("a.maplink").first
    if link.count():
        # Let the figure finish its fade-up first: hovering mid-transition moves the node out from
        # under the pointer, which fires mouseleave and hides the tooltip.
        link.scroll_into_view_if_needed()
        pg.wait_for_function("document.querySelector('figure.diagram').classList.contains('in')")
        pg.wait_for_timeout(700)
        link.hover()
        pg.wait_for_timeout(200)
        check(pg.locator(".tip.on").count() == 1, "map hover shows one tooltip")
        check("Open " in pg.locator(".tip").inner_text(), "tooltip reads 'Open <topic> →'")
        check(pg.locator("a.maplink title").count() == 0, "no native SVG title tooltips on links")
    chip = pg.locator(".chip").first
    chip.click()
    check(pg.locator("svg.overview.focused").count() == 1, "legend chip pins band focus")
    check(chip.get_attribute("aria-pressed") == "true", "pinned chip reports aria-pressed")
    pg.keyboard.press("Escape")
    check(pg.locator("svg.overview.focused").count() == 0, "Escape clears band focus")
    pg.reload()
    pg.keyboard.press("Tab")
    check(pg.evaluate("document.activeElement.className") == "skip", "first Tab reaches skip link")
    check(not errors, "no script errors on home")
    for name in [x.name for x in SITE.glob("*.html")]:
        m = b.new_page(viewport={"width": 390, "height": 844})
        m.goto((SITE / name).as_uri())
        sw = m.evaluate("document.documentElement.scrollWidth")
        check(sw <= 390, f"{name}: no page-level horizontal scroll at 390px (got {sw})")
        m.close()
    b.close()

sys.exit(1 if fails else 0)
