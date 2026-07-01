from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest

from setup_os.completeness import missing_decisions
from setup_os.spec import AgentSpec


class CompletenessTests(unittest.TestCase):
    def test_generic_spec_reports_missing_decisions(self) -> None:
        spec = AgentSpec(
            name="Generated Local Agent",
            slug="generated-local-agent",
            summary="Generated from a conversation.",
        )

        missing = missing_decisions(spec)

        self.assertEqual(
            [decision.key for decision in missing],
            [
                "runtime_device",
                "privacy_mode",
                "notification_channel",
                "data_sources",
                "approval_rules",
            ],
        )

    def test_portfolio_create_has_no_missing_decisions(self) -> None:
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

            self.assertEqual(result.returncode, 0)
            self.assertNotIn("Missing decisions:", result.stdout)


if __name__ == "__main__":
    unittest.main()
