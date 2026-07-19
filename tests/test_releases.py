from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ReleaseTests(unittest.TestCase):
    def test_create_writes_initial_release_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "setup_os.cli",
                    "create",
                    "examples/portfolio_conversation.md",
                    "--output",
                    tmpdir,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            release_path = Path(tmpdir) / ".setup_os" / "releases" / "v1.json"
            self.assertEqual(result.returncode, 0)
            self.assertTrue(release_path.exists())

            release = json.loads(release_path.read_text(encoding="utf-8"))
            self.assertEqual(release["version"], "v1")
            self.assertIn("architecture.md", release["artifacts"])
            self.assertEqual(release["source"]["spec"], "portfolio-manager-agent")


if __name__ == "__main__":
    unittest.main()
