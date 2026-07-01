from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class EvolutionTests(unittest.TestCase):
    def test_evolve_writes_proposal_without_mutating_agent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
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

            proposal_path = Path(tmpdir) / "evolution_proposal.md"
            self.assertEqual(result.returncode, 0)
            self.assertTrue(proposal_path.exists())
            self.assertFalse((Path(tmpdir) / "report.py").exists())

            proposal = proposal_path.read_text(encoding="utf-8")
            self.assertIn("concentration alerts", proposal)
            self.assertIn("35%", proposal)
            self.assertIn("Approval Required", proposal)


if __name__ == "__main__":
    unittest.main()
