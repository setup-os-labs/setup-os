"""Notification provider interface and console adapter."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Protocol


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
