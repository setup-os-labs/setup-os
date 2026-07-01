from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from setup_os.policy import TRUST_LEVELS, policy_for_slug


class PolicyTests(unittest.TestCase):
    def test_portfolio_policy_is_alert_first(self) -> None:
        policy = policy_for_slug("portfolio-manager-agent")

        self.assertEqual(policy.default_level, "alert")
        self.assertIn("auto_execute", TRUST_LEVELS)
        self.assertIn("trade_execution", policy.approval_required_for)
        self.assertIn("auto_trade", policy.prohibited_actions)

    def test_generated_config_contains_action_policy(self) -> None:
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

            config = json.loads((Path(tmpdir) / "config.json").read_text(encoding="utf-8"))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(config["action_policy"]["default_level"], "alert")
            self.assertIn("diagnose", config["action_policy"]["prohibited_actions"])


if __name__ == "__main__":
    unittest.main()
