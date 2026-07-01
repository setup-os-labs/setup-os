"""Generated agent quality scoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from setup_os.spec import AgentSpec


@dataclass(frozen=True)
class QualityScore:
    architecture: int
    privacy: int
    reliability: int
    maintainability: int
    cost: int
    automation: int

    @property
    def overall(self) -> int:
        scores = [
            self.architecture,
            self.privacy,
            self.reliability,
            self.maintainability,
            self.cost,
            self.automation,
        ]
        return round(sum(scores) / len(scores))

    def to_dict(self) -> dict[str, int]:
        return {
            "overall": self.overall,
            "architecture": self.architecture,
            "privacy": self.privacy,
            "reliability": self.reliability,
            "maintainability": self.maintainability,
            "cost": self.cost,
            "automation": self.automation,
        }


def score_agent(spec: AgentSpec) -> QualityScore:
    privacy = 100 if "local" in spec.privacy.lower() else 75
    automation = 70 if any("no automated" in rule for rule in spec.safety) else 55
    reliability = 88 if spec.safety else 70
    maintainability = 92 if spec.storage == "local files" else 84
    cost = 97 if spec.notifications == ["console"] else 90
    architecture = 94 if spec.slug == "portfolio-manager-agent" else 80

    return QualityScore(
        architecture=architecture,
        privacy=privacy,
        reliability=reliability,
        maintainability=maintainability,
        cost=cost,
        automation=automation,
    )


def agent_dna(spec: AgentSpec) -> dict[str, Any]:
    return {
        "purpose": spec.summary,
        "maturity_level": "Level 2: Alerts",
        "principles": [
            "local-first",
            "human approval by default",
            "compose before build",
            "evolution proposals before mutation",
            "optimize for deletion",
        ],
        "inputs": spec.inputs,
        "outputs": spec.outputs,
        "safety": spec.safety,
        "quality_score": score_agent(spec).to_dict(),
    }
