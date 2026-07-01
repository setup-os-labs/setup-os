from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
import tempfile
import unittest
from pathlib import Path

from setup_os.notifications import (
    ConsoleNotificationProvider,
    LocalInboxNotificationProvider,
    Notification,
)


class NotificationTests(unittest.TestCase):
    def test_console_provider_emits_notification(self) -> None:
        output = io.StringIO()
        provider = ConsoleNotificationProvider()

        with redirect_stdout(output):
            provider.send(
                Notification(
                    title="Portfolio report generated",
                    body="Manual review required before trades.",
                    severity="info",
                )
            )

        self.assertIn(
            "NOTIFY[info]: Portfolio report generated - Manual review required before trades.",
            output.getvalue(),
        )

    def test_local_inbox_provider_appends_notification_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            provider = LocalInboxNotificationProvider(Path(tmpdir))
            provider.send(
                Notification(
                    title="Portfolio report generated",
                    body="Manual review required before trades.",
                    source="portfolio-manager-agent",
                )
            )

            inbox_path = Path(tmpdir) / ".setup_os" / "notifications.jsonl"
            events = [
                json.loads(line)
                for line in inbox_path.read_text(encoding="utf-8").splitlines()
            ]

            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["source"], "portfolio-manager-agent")
            self.assertEqual(events[0]["status"], "new")


if __name__ == "__main__":
    unittest.main()
