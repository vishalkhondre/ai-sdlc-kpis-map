"""Site tests. Run: python -m unittest discover -s scripts/tests -v
Each test names the ground rule (project/GROUND-RULES.md) it enforces."""
import re
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
GEN = ROOT / "site" / "generate.py"
BANNED = ["coming soon", "under construction", "tbd", "to be added", "placeholder", "lorem"]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "site"
        r = subprocess.run([sys.executable, str(GEN), "--preview", "--out", str(cls.out)],
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        cls.map = yaml.safe_load((ROOT / "content" / "map.yml").read_text())
        sys.path.insert(0, str(ROOT / "site"))
        import generate
        cls.gen = generate
        _, _, cls.metrics, cls.refs, _, _, errs = generate.load_content()
        assert not errs, errs

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_topic_ids_unique_and_stable(self):  # SOP: stable topic IDs
        ids = []
        for f in sorted((ROOT / "content" / "metrics").glob("*.yml")):
            ids += [m["id"] for m in yaml.safe_load(f.read_text())]
        self.assertEqual(len(ids), len(set(ids)))
        for i in ids:
            self.assertRegex(i, r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_five_bands_use_design_colours_in_order(self):  # design system v1.0
        self.assertEqual([b["colour"] for b in self.map["bands"]],
                         ["context", "lifecycle", "core", "enablement", "assurance"][:len(self.map["bands"])])

    def test_internal_links_resolve(self):  # GR-4.3
        pages = {p.name: p for p in self.out.glob("*.html")}
        parsed = {}
        for name, p in pages.items():
            lp = Links(); lp.feed(p.read_text()); parsed[name] = lp
        for name, lp in parsed.items():
            for h in lp.hrefs:
                if re.match(r"^(https?:|mailto:)", h):
                    continue
                target, _, frag = h.partition("#")
                target = target or name
                if target.endswith(".svg"):
                    self.assertTrue((self.out / target).exists(), f"{name}: {h}")
                    continue
                self.assertIn(target, parsed, f"{name}: broken link {h}")
                if frag:
                    self.assertIn(frag, parsed[target].ids, f"{name}: missing anchor {h}")

    def test_only_pages_that_exist_are_linked_on_map(self):  # GR-3.2
        html = (self.out / "index.html").read_text()
        for tid in re.findall(r'class="maplink" href="([\w-]+)\.html"', html):
            self.assertTrue((self.out / f"{tid}.html").exists())

    def test_every_map_topic_in_text_route(self):  # GR-4.4 text alternative
        html = (self.out / "index.html").read_text()
        cat = html.split('id="catalogue"', 1)[1]
        for m in self.metrics.values():
            self.assertIn(m["label"].replace("&", "&amp;"), cat, m["id"])

    def test_no_provisional_language_in_body_copy(self):  # GR-3.2
        for p in self.out.glob("*.html"):
            text = re.sub(r"<[^>]+>", " ", p.read_text()).lower()
            text = text.replace("work in progress", "")  # a metric's name (WIP), not a status
            for w in BANNED:
                self.assertNotIn(w, text, f"{p.name}: '{w}'")

    def test_release_build_refuses_provisional_content(self):  # GR-3.2, GR-4.1
        r = subprocess.run([sys.executable, str(GEN), "--out", str(Path(self.tmp.name) / "rel")],
                           capture_output=True, text=True)
        if self.map.get("status") == "provisional":
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("provisional", r.stderr)

    def test_every_metric_page_has_required_sections(self):  # GR-2.6, GR-4.1
        for mid in self.metrics:
            html = (self.out / f"{mid}.html").read_text()
            for sec in ["definition", "formula", "how-to-measure", "pitfalls", "sources"]:
                self.assertIn(f'id="{sec}"', html, f"{mid}: no {sec}")
            self.assertIn("formula-u", html, f"{mid}: formula without unit")

    def test_no_unverified_source_is_cited(self):  # GR-2.4, GR-2.5
        for m in self.metrics.values():
            for s in self.gen.page_sources(m):
                self.assertIn(s, self.refs, f"{m['id']}: {s}")
                self.assertNotEqual(self.refs[s].get("status"), "unverified", f"{m['id']}: {s}")

    def test_findings_carry_a_source(self):  # GR-2.3, GR-2.7
        for m in self.metrics.values():
            for f in m.get("findings") or []:
                self.assertTrue(f.get("source"), f"{m['id']}: finding without source")

    def test_every_dimension_has_a_page(self):  # big picture first, then detail
        for b in self.map["bands"]:
            self.assertTrue((self.out / f"{b['id']}.html").exists(), b["id"])

    def test_design_tokens_present(self):  # design system v1.0
        css = (ROOT / "site" / "assets" / "style.css").read_text()
        for tok in ["#FAFAFB", "#18181B", "#4C66E6", "#EEF1FD", "#059669", "Inter", "JetBrains Mono"]:
            self.assertIn(tok, css)
        self.assertNotRegex(css.lower(), r"font-family:[^;]*serif\b(?<!sans-serif)")


if __name__ == "__main__":
    unittest.main()
