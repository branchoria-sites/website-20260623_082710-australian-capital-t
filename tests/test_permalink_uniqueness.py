"""Falsifier for the australian-capital-t-2949ba permalink collision cure.

Before the cure, `/australian-capital-t-2949ba-canberra/` was claimed by
two level-3 ``*_index.md`` documents, shadowing one index on
ufos-and-uap-by-australian-state.branchoria.com. The cure keeps the
live winner (Sky Checks) at the shared route and gives the shadowed
Airport Case index a unique ``-airport-case`` suffixed permalink.
"""
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages"
FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
PERMALINK = re.compile(r"^permalink:\s*[\"']?([^\s\"'#]+)[\"']?\s*$", re.M)


def page_permalinks():
    out = {}
    for p in PAGES.glob("*.md"):
        m = FRONT_MATTER.match(p.read_text(encoding="utf-8", errors="replace"))
        if not m:
            continue
        pm = PERMALINK.search(m.group(1))
        if pm:
            out[p.name] = pm.group(1)
    return out


SHARED_SLUG = "/australian-capital-t-2949ba-canberra/"
EXPECTED_CURED = "/australian-capital-t-2949ba-canberra-airport-case/"


class TestPermalinkUniqueness(unittest.TestCase):
    def test_all_permalinks_unique(self):
        pls = page_permalinks()
        counts = Counter(pls.values())
        dups = {k: v for k, v in counts.items() if v > 1}
        owners = {k: sorted(n for n, v in pls.items() if v == k) for k in dups}
        self.assertEqual({}, owners)

    def test_shared_slug_claimed_by_one_document(self):
        pls = page_permalinks()
        owners = sorted(n for n, v in pls.items() if v == SHARED_SLUG)
        self.assertEqual(1, len(owners), f"{SHARED_SLUG} claimed by {owners}")

    def test_expected_cured_index_route_exists(self):
        pls = set(page_permalinks().values())
        self.assertIn(EXPECTED_CURED, pls)

    def test_index_bodies_link_only_existing_routes(self):
        existing = set(page_permalinks().values())
        dangling = []
        for p in PAGES.glob("*_index.md"):
            for m in re.finditer(r"\{\{\s*'(/[^']*?)'\s*\|\s*relative_url", p.read_text(encoding="utf-8", errors="replace")):
                if m.group(1) not in existing:
                    dangling.append((p.name, m.group(1)))
        self.assertEqual([], dangling)


if __name__ == "__main__":
    unittest.main()
