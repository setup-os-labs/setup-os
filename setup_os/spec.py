"""Deterministic v0 spec extraction."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from setup_os.conversation import ConversationEnvelope


@dataclass(frozen=True)
class AgentSpec:
    name: str
    slug: str
    summary: str
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    safety: list[str] = field(default_factory=list)
    runtime: str = ""
    privacy: str = ""
    storage: str = "local"
    notifications: list[str] = field(default_factory=list)
    source: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "slug": self.slug,
            "summary": self.summary,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "safety": self.safety,
            "runtime": self.runtime,
            "privacy": self.privacy,
            "storage": self.storage,
            "notifications": self.notifications,
            "source": self.source,
        }


def extract_agent_spec(envelope: ConversationEnvelope) -> AgentSpec:
    text = "\n".join(message.content for message in envelope.messages).lower()

    if "portfolio" in text:
        return AgentSpec(
            name="Portfolio Manager Agent",
            slug="portfolio-manager-agent",
            summary=(
                "Local alert-only portfolio assistant that ingests exported "
                "holdings and transactions, summarizes risk, and produces reports."
            ),
            inputs=["CSV holdings export", "CSV transactions export"],
            outputs=["daily Markdown report", "console notification", "audit log"],
            safety=[
                "no broker credentials in v0",
                "no automated trades",
                "approval required before external actions",
            ],
            runtime="local laptop or always-on local machine",
            privacy="local-first",
            storage="local files",
            notifications=["console"],
            source={
                "conversation": envelope.source,
                "message_count": len(envelope.messages),
            },
        )

    return AgentSpec(
        name="Generated Local Agent",
        slug="generated-local-agent",
        summary="Local agent generated from a planning conversation.",
        inputs=["planning conversation"],
        outputs=["agent_spec.json"],
        safety=["approval required before external actions"],
        source={
            "conversation": envelope.source,
            "message_count": len(envelope.messages),
        },
    )
