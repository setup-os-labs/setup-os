from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ApplyTests(unittest.TestCase):
    def test_apply_requires_explicit_approval(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "setup_os.cli",
                    "evolve",
                    "examples/portfolio_update.md",
                    "--output",
                    tmpdir,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            result = subprocess.run(
                [sys.executable, "-m", "setup_os.cli", "apply", "--output", tmpdir],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("without --approve", result.stdout)
            self.assertFalse(
                (Path(tmpdir) / ".setup_os" / "releases" / "v2-candidate.json").exists()
            )

    def test_apply_writes_candidate_release_when_approved(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "setup_os.cli",
                    "evolve",
                    "examples/portfolio_update.md",
                    "--output",
                    tmpdir,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "setup_os.cli",
                    "apply",
                    "--output",
                    tmpdir,
                    "--approve",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            release_path = Path(tmpdir) / ".setup_os" / "releases" / "v2-candidate.json"
            release = json.loads(release_path.read_text(encoding="utf-8"))

            self.assertEqual(result.returncode, 0)
            self.assertEqual(release["version"], "v2-candidate")
            self.assertEqual(release["source"]["approved"], True)


if __name__ == "__main__":
    unittest.main()
