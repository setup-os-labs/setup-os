from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from setup_os.notifications import (
    ConsoleNotificationProvider,
    LocalInboxNotificationProvider,
    Notification,
    NtfyNotificationProvider,
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

    def test_ntfy_provider_is_disabled_by_default(self) -> None:
        output = io.StringIO()
        provider = NtfyNotificationProvider(topic="setup-os-test")

        with patch("setup_os.notifications.urlopen") as urlopen_mock:
            with redirect_stdout(output):
                provider.send(Notification(title="Test", body="Not sent"))

        urlopen_mock.assert_not_called()
        self.assertIn("NTFY[disabled]", output.getvalue())

    def test_ntfy_provider_requires_topic_when_enabled(self) -> None:
        provider = NtfyNotificationProvider(enabled=True)

        with self.assertRaises(ValueError):
            provider.send(Notification(title="Test", body="Missing topic"))

    def test_ntfy_provider_posts_notification_when_enabled(self) -> None:
        response = MagicMock()
        response.__enter__.return_value = response
        provider = NtfyNotificationProvider(topic="setup os alerts", enabled=True)

        with patch("setup_os.notifications.urlopen", return_value=response) as urlopen_mock:
            provider.send(
                Notification(
                    title="Portfolio concentration review",
                    body="VOO is above threshold.",
                    severity="warning",
                    source="portfolio-manager-agent",
                )
            )

        request = urlopen_mock.call_args.args[0]
        self.assertEqual(request.full_url, "https://ntfy.sh/setup%20os%20alerts")
        self.assertEqual(request.data, b"VOO is above threshold.")
        self.assertEqual(request.headers["Title"], "Portfolio concentration review")
        self.assertEqual(request.headers["Tags"], "warning")


if __name__ == "__main__":
    unittest.main()
