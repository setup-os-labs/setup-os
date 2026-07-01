"""Capability dependency graph helpers."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Capability:
    name: str
    dependencies: list[str] = field(default_factory=list)
    surfaces: list[str] = field(default_factory=list)


PORTFOLIO_CAPABILITIES = [
    Capability(
        name="Daily portfolio report",
        dependencies=["CSV holdings export", "local file storage"],
        surfaces=["reports/daily_report.md", "console notification"],
    ),
    Capability(
        name="Concentration monitoring",
        dependencies=["holding market value", "alert threshold", "daily report"],
        surfaces=["evolution_proposal.md", "future report rule"],
    ),
    Capability(
        name="Evolution proposal",
        dependencies=["update conversation", "structured memory", "policy memory"],
        surfaces=["evolution_proposal.md", ".setup_os/timeline.jsonl"],
    ),
    Capability(
        name="Notification event",
        dependencies=["notification provider", "local inbox"],
        surfaces=[".setup_os/notifications.jsonl", "console"],
    ),
]


def capabilities_for_slug(slug: str) -> list[Capability]:
    if slug == "portfolio-manager-agent":
        return PORTFOLIO_CAPABILITIES
    return [
        Capability(
            name="Generated local agent",
            dependencies=["planning conversation", "agent_spec.json"],
            surfaces=["README.md"],
        )
    ]
