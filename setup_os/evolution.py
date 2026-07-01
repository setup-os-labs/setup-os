"""Evolution proposal helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from setup_os.conversation import ConversationEnvelope


@dataclass(frozen=True)
class EvolutionProposal:
    title: str
    summary: str
    proposed_changes: list[str] = field(default_factory=list)
    approval_required: bool = True
    source: dict[str, Any] = field(default_factory=dict)

    def to_markdown(self) -> str:
        changes = "\n".join(f"- {change}" for change in self.proposed_changes)
        approval = "yes" if self.approval_required else "no"
        return (
            f"# {self.title}\n\n"
            f"{self.summary}\n\n"
            "## Proposed Changes\n\n"
            f"{changes}\n\n"
            "## Approval Required\n\n"
            f"{approval}\n\n"
            "## Source\n\n"
            f"- conversation: {self.source.get('name', 'unknown')}\n"
            f"- messages: {self.source.get('message_count', 0)}\n"
        )


def create_evolution_proposal(envelope: ConversationEnvelope) -> EvolutionProposal:
    text = "\n".join(message.content for message in envelope.messages).lower()
    changes: list[str] = []

    if "concentration" in text:
        changes.append("Add concentration alerts when one holding exceeds the configured threshold.")
    if "35%" in text or "35 percent" in text:
        changes.append("Set initial concentration alert threshold to 35%.")
    if not changes:
        changes.append("Review conversation and decide whether any generated-system change is needed.")

    return EvolutionProposal(
        title="Evolution Proposal",
        summary=(
            "Review these proposed changes before applying them. "
            "Setup OS does not mutate a generated system directly from a new conversation."
        ),
        proposed_changes=changes,
        approval_required=True,
        source={
            "name": envelope.source.get("name", "unknown"),
            "message_count": len(envelope.messages),
        },
    )
