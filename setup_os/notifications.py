"""Notification provider interface and console adapter."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Protocol
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Notification:
    title: str
    body: str
    severity: str = "info"
    source: str = "setup-os"
    status: str = "new"

    def to_event(self) -> dict[str, str]:
        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "source": self.source,
            "title": self.title,
            "body": self.body,
            "severity": self.severity,
            "status": self.status,
        }


class NotificationProvider(Protocol):
    def send(self, notification: Notification) -> None:
        """Send a notification."""


class ConsoleNotificationProvider:
    def send(self, notification: Notification) -> None:
        print(f"NOTIFY[{notification.severity}]: {notification.title} - {notification.body}")


class LocalInboxNotificationProvider:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir

    def send(self, notification: Notification) -> None:
        inbox_dir = self.output_dir / ".setup_os"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        inbox_path = inbox_dir / "notifications.jsonl"
        with inbox_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(notification.to_event(), sort_keys=True) + "\n")


class NtfyNotificationProvider:
    def __init__(
        self,
        topic: str = "",
        server: str = "https://ntfy.sh",
        enabled: bool = False,
        timeout_seconds: float = 5.0,
    ) -> None:
        self.topic = topic
        self.server = server.rstrip("/")
        self.enabled = enabled
        self.timeout_seconds = timeout_seconds

    def send(self, notification: Notification) -> None:
        if not self.enabled:
            print("NTFY[disabled]: notification not sent")
            return
        if not self.topic:
            raise ValueError("ntfy topic is required when ntfy notifications are enabled")

        url = f"{self.server}/{quote(self.topic, safe='')}"
        request = Request(
            url,
            data=notification.body.encode("utf-8"),
            method="POST",
            headers={
                "Title": notification.title,
                "Tags": notification.severity,
                "X-Setup-OS-Source": notification.source,
            },
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds):
                pass
        except URLError as error:
            raise RuntimeError(f"ntfy notification failed: {error}") from error
