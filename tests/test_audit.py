from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class AuditTests(unittest.TestCase):
    def test_create_and_evolve_append_audit_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            create = subprocess.run(
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
            evolve = subprocess.run(
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

            self.assertEqual(create.returncode, 0)
            self.assertEqual(evolve.returncode, 0)

            audit_path = Path(tmpdir) / ".setup_os" / "audit.jsonl"
            events = [
                json.loads(line)
                for line in audit_path.read_text(encoding="utf-8").splitlines()
            ]

            self.assertEqual([event["event_type"] for event in events], ["create", "evolve"])
            self.assertEqual(events[0]["payload"]["spec"], "portfolio-manager-agent")
            self.assertTrue(events[1]["payload"]["approval_required"])


if __name__ == "__main__":
    unittest.main()
