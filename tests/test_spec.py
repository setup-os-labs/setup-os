from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from setup_os.conversation import parse_conversation_file
from setup_os.spec import extract_agent_spec


class SpecExtractionTests(unittest.TestCase):
    def test_extract_portfolio_spec(self) -> None:
        envelope = parse_conversation_file(Path("examples/portfolio_conversation.md"))
        spec = extract_agent_spec(envelope)

        self.assertEqual(spec.slug, "portfolio-manager-agent")
        self.assertIn("CSV holdings export", spec.inputs)
        self.assertIn("no automated trades", spec.safety)

    def test_create_writes_agent_spec(self) -> None:
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

            spec_path = Path(tmpdir) / "agent_spec.json"
            self.assertEqual(result.returncode, 0)
            self.assertTrue(spec_path.exists())

            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            self.assertEqual(spec["slug"], "portfolio-manager-agent")
            self.assertEqual(spec["source"]["message_count"], 4)


if __name__ == "__main__":
    unittest.main()
