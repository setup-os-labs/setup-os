"""Action permission policy primitives."""

from __future__ import annotations

from dataclasses import dataclass


TRUST_LEVELS = [
    "read",
    "alert",
    "draft",
    "approve",
    "execute",
    "auto_execute",
]


@dataclass(frozen=True)
class ActionPolicy:
    default_level: str
    approval_required_for: list[str]
    prohibited_actions: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "trust_levels": TRUST_LEVELS,
            "default_level": self.default_level,
            "approval_required_for": self.approval_required_for,
            "prohibited_actions": self.prohibited_actions,
        }


def policy_for_slug(slug: str) -> ActionPolicy:
    if slug == "portfolio-manager-agent":
        return ActionPolicy(
            default_level="alert",
            approval_required_for=[
                "broker_connection",
                "trade_execution",
                "strategy_update",
                "external_action",
            ],
            prohibited_actions=["auto_trade", "store_broker_credentials"],
        )
    if slug == "health-os-agent":
        return ActionPolicy(
            default_level="alert",
            approval_required_for=[
                "diagnosis",
                "medication_change",
                "medical_decision",
                "external_action",
            ],
            prohibited_actions=["diagnose", "change_medication", "handle_emergency"],
        )
    return ActionPolicy(
        default_level="draft",
        approval_required_for=["external_action", "irreversible_action"],
        prohibited_actions=[],
    )
