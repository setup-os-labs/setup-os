from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADR_DIR = ROOT / "docs" / "adr"


class AdrIndexTests(unittest.TestCase):
    def test_all_adrs_are_listed_in_index(self) -> None:
        index = (ADR_DIR / "README.md").read_text(encoding="utf-8")
        adr_files = sorted(
            path.name
            for path in ADR_DIR.glob("[0-9][0-9][0-9][0-9]-*.md")
            if path.name != "README.md"
        )

        self.assertGreaterEqual(len(adr_files), 1)
        for filename in adr_files:
            self.assertIn(filename, index)

    def test_index_links_from_readme(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/adr/README.md", readme)


if __name__ == "__main__":
    unittest.main()
