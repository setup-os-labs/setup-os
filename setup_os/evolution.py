"""Evolution proposal helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from setup_os.conversation import ConversationEnvelope


@dataclass(frozen=True)
class ProposedChange:
    description: str
    confidence: float
    impact: str
    risk: str
    memory_layer: str = "structured"
    conflict: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "description": self.description,
            "confidence": self.confidence,
            "impact": self.impact,
            "risk": self.risk,
            "memory_layer": self.memory_layer,
            "conflict": self.conflict,
        }


@dataclass(frozen=True)
class EvolutionProposal:
    title: str
    summary: str
    proposed_changes: list[ProposedChange] = field(default_factory=list)
    approval_required: bool = True
    maturity_level: str = "Level 2: Alerts"
    source: dict[str, Any] = field(default_factory=dict)

    def to_markdown(self) -> str:
        changes = "\n".join(
            [
                f"- {change.description}\n"
                f"  - confidence: {change.confidence:.2f}\n"
                f"  - impact: {change.impact}\n"
                f"  - risk: {change.risk}\n"
                f"  - memory layer: {change.memory_layer}"
                + (f"\n  - conflict: {change.conflict}" if change.conflict else "")
                for change in self.proposed_changes
            ]
        )
        approval = "yes" if self.approval_required else "no"
        return (
            f"# {self.title}\n\n"
            f"{self.summary}\n\n"
            "## Maturity Level\n\n"
            f"{self.maturity_level}\n\n"
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
    changes: list[ProposedChange] = []

    if "concentration" in text:
        changes.append(
            ProposedChange(
                description="Add concentration alerts when one holding exceeds the configured threshold.",
                confidence=0.91,
                impact="adds a new monitoring capability to the daily report",
                risk="low",
                memory_layer="structured",
            )
        )
    if "35%" in text or "35 percent" in text:
        changes.append(
            ProposedChange(
                description="Set initial concentration alert threshold to 35%.",
                confidence=0.94,
                impact="changes alert sensitivity",
                risk="low",
                memory_layer="policy",
            )
        )
    if "auto" in text and ("trade" in text or "sell" in text or "buy" in text):
        changes.append(
            ProposedChange(
                description="Review requested automated trading behavior.",
                confidence=0.72,
                impact="could change action permissions",
                risk="high",
                memory_layer="policy",
                conflict="Existing v0 policy disables broker execution and automated trades.",
            )
        )
    if not changes:
        changes.append(
            ProposedChange(
                description="Review conversation and decide whether any generated-system change is needed.",
                confidence=0.50,
                impact="parks ambiguous input for human review",
                risk="medium",
                memory_layer="raw",
            )
        )

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
