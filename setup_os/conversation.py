"""Conversation import and normalization helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


KNOWN_ROLES = {
    "assistant",
    "claude",
    "codex",
    "system",
    "user",
}


@dataclass(frozen=True)
class ConversationMessage:
    role: str
    content: str

    def to_dict(self) -> dict[str, str]:
        return {
            "role": self.role,
            "content": self.content,
        }


@dataclass(frozen=True)
class ConversationEnvelope:
    source: dict[str, str]
    messages: list[ConversationMessage]
    attachments: list[dict[str, Any]] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "messages": [message.to_dict() for message in self.messages],
            "attachments": self.attachments,
            "provenance": self.provenance,
        }


def parse_conversation_file(path: str | Path) -> ConversationEnvelope:
    source_path = Path(path)
    text = source_path.read_text(encoding="utf-8")
    messages = parse_markdown_or_text(text)

    return ConversationEnvelope(
        source={
            "path": str(source_path),
            "name": source_path.name,
            "type": source_path.suffix.lower().lstrip(".") or "text",
        },
        messages=messages,
        provenance={
            "parser": "setup_os.conversation.parse_markdown_or_text",
            "message_count": len(messages),
        },
    )


def parse_markdown_or_text(text: str) -> list[ConversationMessage]:
    messages: list[ConversationMessage] = []
    active_role: str | None = None
    active_lines: list[str] = []

    def flush() -> None:
        nonlocal active_lines, active_role
        if active_role is None:
            active_lines = []
            return

        content = "\n".join(active_lines).strip()
        if content:
            messages.append(ConversationMessage(role=active_role, content=content))
        active_lines = []

    for raw_line in text.splitlines():
        role = _role_from_line(raw_line)
        if role is not None:
            flush()
            active_role = role
            inline_content = _inline_content(raw_line)
            active_lines = [inline_content] if inline_content else []
            continue

        if active_role is not None:
            active_lines.append(raw_line)

    flush()
    return messages


def _role_from_line(line: str) -> str | None:
    stripped = line.strip()
    if not stripped:
        return None

    heading = stripped.lstrip("#").strip()
    heading_role = heading.rstrip(":").lower()
    if heading_role in KNOWN_ROLES:
        return _normalize_role(heading_role)

    if ":" in stripped:
        possible_role = stripped.split(":", 1)[0].strip().lower()
        if possible_role in KNOWN_ROLES:
            return _normalize_role(possible_role)

    return None


def _inline_content(line: str) -> str:
    stripped = line.strip()
    heading = stripped.lstrip("#").strip()
    if heading.rstrip(":").lower() in KNOWN_ROLES:
        return ""
    return stripped.split(":", 1)[1].strip()


def _normalize_role(role: str) -> str:
    if role in {"claude", "codex"}:
        return "assistant"
    return role
