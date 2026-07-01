"""Spec completeness checks."""

from __future__ import annotations

from dataclasses import dataclass

from setup_os.spec import AgentSpec


@dataclass(frozen=True)
class MissingDecision:
    key: str
    prompt: str


def missing_decisions(spec: AgentSpec) -> list[MissingDecision]:
    missing: list[MissingDecision] = []

    if not spec.runtime:
        missing.append(
            MissingDecision(
                key="runtime_device",
                prompt="Where should this run: laptop, always-on mini PC, private server, or hybrid?",
            )
        )
    if not spec.privacy:
        missing.append(
            MissingDecision(
                key="privacy_mode",
                prompt="Should data stay local-only, or can selected cloud services be used?",
            )
        )
    if not spec.notifications:
        missing.append(
            MissingDecision(
                key="notification_channel",
                prompt="Which alert channel should Setup OS use?",
            )
        )
    if not spec.inputs:
        missing.append(
            MissingDecision(
                key="data_sources",
                prompt="What data sources or exports should the generated system read?",
            )
        )
    if not spec.safety:
        missing.append(
            MissingDecision(
                key="approval_rules",
                prompt="Which actions require explicit human approval?",
            )
        )

    return missing
