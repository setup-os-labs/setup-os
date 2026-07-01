from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ArchitectureTests(unittest.TestCase):
    def test_create_writes_architecture_proposal(self) -> None:
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

            architecture_path = Path(tmpdir) / "architecture.md"
            self.assertEqual(result.returncode, 0)
            self.assertTrue(architecture_path.exists())

            proposal = architecture_path.read_text(encoding="utf-8")
            self.assertIn("Component Choices", proposal)
            self.assertIn("Capability Dependency Graph", proposal)
            self.assertIn("Daily portfolio report", proposal)
            self.assertIn("console notification adapter", proposal)
            self.assertIn("broker execution", proposal.lower())
            self.assertIn("alternatives considered", proposal)


if __name__ == "__main__":
    unittest.main()
