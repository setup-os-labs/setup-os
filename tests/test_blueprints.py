from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class BlueprintTests(unittest.TestCase):
    def test_create_generates_portfolio_blueprint(self) -> None:
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

            output = Path(tmpdir)
            self.assertEqual(result.returncode, 0)
            self.assertTrue((output / "README.md").exists())
            self.assertTrue((output / "config.json").exists())
            self.assertTrue((output / "data" / "holdings.csv").exists())
            self.assertTrue((output / "report.py").exists())

            report = subprocess.run(
                [sys.executable, "report.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(report.returncode, 0)
            self.assertTrue((output / "reports" / "daily_report.md").exists())
            self.assertIn("NOTIFY[info]:", report.stdout)


if __name__ == "__main__":
    unittest.main()
