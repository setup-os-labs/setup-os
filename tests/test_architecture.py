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
            self.assertIn("Standard Diagram Pack", proposal)
            self.assertIn("docs/diagrams", proposal)

    def test_create_writes_standard_diagram_pack(self) -> None:
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

            diagram_dir = Path(tmpdir) / "docs" / "diagrams"
            self.assertEqual(result.returncode, 0)
            self.assertTrue((diagram_dir / "overview_orchestration.html").exists())
            self.assertTrue((diagram_dir / "runtime_architecture.html").exists())
            self.assertTrue((diagram_dir / "evolution_safety_flow.html").exists())
            self.assertTrue((diagram_dir / "overview_orchestration.d2").exists())
            self.assertTrue((diagram_dir / "diagram_manifest.json").exists())
            self.assertTrue((diagram_dir / "icons" / "runtime.svg").exists())

            overview = (diagram_dir / "overview_orchestration.html").read_text(
                encoding="utf-8"
            )
            self.assertIn("icons/conversation.svg", overview)
            self.assertNotIn("https://icons.terrastruct.com", overview)


if __name__ == "__main__":
    unittest.main()
