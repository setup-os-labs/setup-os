"""Notification provider interface and console adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Notification:
    title: str
    body: str
    severity: str = "info"


class NotificationProvider(Protocol):
    def send(self, notification: Notification) -> None:
        """Send a notification."""


class ConsoleNotificationProvider:
    def send(self, notification: Notification) -> None:
        print(f"NOTIFY[{notification.severity}]: {notification.title} - {notification.body}")
