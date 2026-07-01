from __future__ import annotations

import io
from contextlib import redirect_stdout
import unittest

from setup_os.notifications import ConsoleNotificationProvider, Notification


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


if __name__ == "__main__":
    unittest.main()
