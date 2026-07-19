"""Static component registry for v0 architecture proposals."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComponentChoice:
    layer: str
    selected: str
    reason: str
    alternatives: list[str]


PORTFOLIO_COMPONENTS = [
    ComponentChoice(
        layer="conversation import",
        selected="Setup OS Markdown/TXT parser",
        reason="Enough for exported planning chats in v0 without adding parser dependencies.",
        alternatives=["unstructured", "docling", "LangChain loaders"],
    ),
    ComponentChoice(
        layer="agent runtime",
        selected="deterministic Python scaffold",
        reason="Keeps the first golden path inspectable before adding LangGraph or PydanticAI.",
        alternatives=["LangGraph", "PydanticAI", "CrewAI"],
    ),
    ComponentChoice(
        layer="storage",
        selected="local files",
        reason="Matches local-first portfolio data and avoids database setup for v0.",
        alternatives=["SQLite", "Postgres", "DuckDB"],
    ),
    ComponentChoice(
        layer="notifications",
        selected="console notification adapter",
        reason="Verifies the notification contract before adding mobile push.",
        alternatives=["ntfy", "Apprise", "Telegram"],
    ),
    ComponentChoice(
        layer="broker execution",
        selected="disabled",
        reason="Portfolio v0 is alert-only and must not store broker credentials or trade.",
        alternatives=["Robinhood Agentic MCP", "Alpaca", "Interactive Brokers"],
    ),
]


def component_choices_for_slug(slug: str) -> list[ComponentChoice]:
    if slug == "portfolio-manager-agent":
        return PORTFOLIO_COMPONENTS
    return [
        ComponentChoice(
            layer="local generation",
            selected="Setup OS deterministic scaffold",
            reason="Default v0 fallback for generated local agents.",
            alternatives=["manual setup", "coding agent only"],
        )
    ]
