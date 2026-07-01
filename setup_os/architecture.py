"""Architecture proposal generation."""

from __future__ import annotations

from pathlib import Path

from setup_os.registry import component_choices_for_slug
from setup_os.spec import AgentSpec


def write_architecture_proposal(spec: AgentSpec, output_dir: Path) -> Path:
    proposal_path = output_dir / "architecture.md"
    choices = component_choices_for_slug(spec.slug)

    lines = [
        f"# {spec.name} Architecture Proposal",
        "",
        spec.summary,
        "",
        "## Runtime",
        "",
        "- local-first Python scaffold",
        "- alert-only v0 mode",
        "- no broker execution",
        "",
        "## Component Choices",
        "",
    ]

    for choice in choices:
        alternatives = ", ".join(choice.alternatives)
        lines.extend(
            [
                f"### {choice.layer.title()}",
                "",
                f"- selected: {choice.selected}",
                f"- reason: {choice.reason}",
                f"- alternatives considered: {alternatives}",
                "",
            ]
        )

    lines.extend(
        [
            "## Approval Gates",
            "",
            "- broker connections require explicit approval",
            "- trade execution is disabled in v0",
            "- future strategy changes must be proposed through `evolution_proposal.md`",
            "",
        ]
    )

    proposal_path.write_text("\n".join(lines), encoding="utf-8")
    return proposal_path
