from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class HealthBlueprintTests(unittest.TestCase):
    def test_create_generates_health_blueprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "setup_os.cli",
                    "create",
                    "examples/health_conversation.md",
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
            self.assertTrue((output / "data" / "health_notes.csv").exists())
            self.assertTrue((output / "agent_dna.json").exists())
            self.assertTrue((output / "health.py").exists())

            spec = json.loads((output / "agent_spec.json").read_text(encoding="utf-8"))
            self.assertEqual(spec["slug"], "health-os-agent")
            self.assertIn("no diagnosis", spec["safety"])

            report = subprocess.run(
                [sys.executable, "report.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )

            report_text = (output / "reports" / "wellness_report.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(report.returncode, 0)
            self.assertIn("not medical advice", report_text)
            self.assertIn("NOTIFY[info]:", report.stdout)

            verify = subprocess.run(
                [sys.executable, "verify.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(verify.returncode, 0)
            self.assertIn("Verification passed.", verify.stdout)

            health = subprocess.run(
                [sys.executable, "health.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(health.returncode, 0)
            self.assertIn("Runtime health check passed.", health.stdout)


if __name__ == "__main__":
    unittest.main()
