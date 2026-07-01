# Portfolio Management OS Building Blocks

Date: 2026-07-01

Source context: ranked OSS portfolio OS analysis from the referenced Codex chat, plus the current Setup OS product direction.

## Refined Use Case

Portfolio Management OS is not a single portfolio tracker.

It is a local-first, evolving investing assistant that imports saved finance conversations, stores them as raw memory first, extracts structured strategy and portfolio facts after review, watches portfolio and market context, produces confidence-scored reports and alerts, and can later connect to official broker/Robinhood Agentic-style surfaces behind explicit approval gates.

The architecture must stay plug-and-play because the system should mature over time without rewriting the whole vertical.

## Short Verdict

Build Stack 2 first, but design toward Stack 1.

- v0 implementation: Setup OS generated Python vertical, local files, JSONL, Markdown reports, raw conversation memory, local notification inbox, and approval-first evolution proposals.
- target architecture: LangGraph-style durable workflows, OpenBB-style financial data layer, optional Ghostfolio-style cockpit, Qdrant/SQLite memory, ntfy/Apprise notifications, and official Robinhood Agentic/MCP-style read-only connector first.

## Best 5 Stack Options

| Rank | Stack | Best for | Weakness |
| ---: | --- | --- | --- |
| 1 | LangGraph + OpenBB + Ghostfolio + LEAN + Qdrant + ntfy/Apprise + Robinhood MCP | Best balanced long-term Portfolio OS | More integration work |
| 2 | Local Python vertical + OpenBB adapter later + SQLite/JSONL + Markdown reports + local inbox | Fastest useful local v0 | No rich dashboard at first |
| 3 | LangGraph + OpenBB + FinRobot-style reasoning + skfolio/PyPortfolioOpt + Robinhood MCP | AI-heavy allocation and strategy reasoning | Needs strong evals and safety rails |
| 4 | Ghostfolio + OpenBB + Setup OS/LangGraph sidecar + ntfy | Fastest portfolio cockpit path | Dashboard is not the OS brain |
| 5 | LEAN or NautilusTrader + OpenBB + LangGraph + strict approval engine | Most serious trading/backtesting path | Too heavy for v0 |

## Comparison

Scores are directional for this use case, from 1 to 10.

| Criterion | Stack 1 | Stack 2 | Stack 3 | Stack 4 | Stack 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Local-first | 9 | 10 | 9 | 8 | 9 |
| Evolves from chats | 10 | 9 | 10 | 7 | 8 |
| Plug-and-play architecture | 10 | 9 | 9 | 7 | 8 |
| Fast to build | 7 | 10 | 6 | 8 | 5 |
| Portfolio dashboard | 9 | 4 | 5 | 10 | 4 |
| Alert workflow | 10 | 9 | 9 | 8 | 8 |
| Approval-first execution | 10 | 8 | 9 | 7 | 10 |
| Serious backtesting/execution | 9 | 5 | 7 | 5 | 10 |
| Low complexity | 6 | 9 | 5 | 7 | 4 |

## Rejected Or Deprioritized As Core

| Candidate | Why not core | Still useful |
| --- | --- | --- |
| CrewAI | Less direct fit for durable, versioned, human-approved workflows than LangGraph-style graphs | Possible simple agent-team experiments |
| Flowise | Strong visual builder, weaker fit for audit-heavy strategy diffs and local OS behavior | Prototyping |
| Dify | More LLM app platform than local evolving OS runtime | Possible admin/app layer later |
| AutoGPT / AGiXT | Too general-purpose and less deterministic near investing workflows | Not core |
| n8n | Great automation glue, not the strategy brain | Jobs, notifications, integrations |
| Open Interpreter | Broad local automation is risky near broker workflows | Setup or local utility tasks |
| Ollama | Model runtime, not a portfolio OS | Local inference adapter |
| Qdrant / Chroma | Memory infrastructure, not an OS | Vector memory layer |
| Supabase | Useful backend platform, but not the first local-first default | Optional self-hosted backend |
| Novu | Product-grade notification infrastructure is too heavy for v0 | Later notification routing |
| Portfolio Performance | Strong manual desktop analytics, weak as agent runtime | Import/reference ideas |
| backtrader | Useful lightweight backtesting, less complete than LEAN for serious parity | Simple strategy tests |

## Adapter Boundaries To Preserve

```text
portfolio-management-os/
  adapters/
    data_providers/
    brokers/
    llms/
    vector_stores/
    notification_channels/
    backtest_engines/
  memory/
    raw/
    structured/
    policy/
  strategy_modules/
  risk_modules/
  ui_surfaces/
```

## Implementation Order

1. Import ChatGPT finance Markdown into raw memory.
2. Extract strategy notes, risk rules, watchlist, and allocation intent into structured drafts.
3. Produce local daily Markdown report from sample or imported holdings.
4. Emit local inbox notifications with confidence and reason fields.
5. Generate evolution proposals for strategy changes instead of mutating strategy directly.
6. Add read-only Robinhood import only through official Agentic/MCP-style access if available, otherwise manual snapshots.
7. Add OpenBB-style market enrichment.
8. Add richer cockpit or Ghostfolio-style UI only after report and alert loop is useful.
9. Add backtesting and execution labs behind explicit approval gates.

## Current Lock-In

Lock in the adapter architecture and v0 local-first flow.

Do not lock in Ghostfolio, LEAN, FinRobot, or Robinhood execution as required dependencies yet. Keep them as replaceable future adapters until the desktop app and local generated vertical are proven.

## Sources To Recheck Before Implementation

- LangGraph: https://github.com/langchain-ai/langgraph
- OpenBB: https://github.com/OpenBB-finance/OpenBB
- Ghostfolio: https://github.com/ghostfolio/ghostfolio
- QuantConnect LEAN: https://github.com/QuantConnect/Lean
- NautilusTrader: https://github.com/nautechsystems/nautilus_trader
- Robinhood Agentic Trading overview: https://robinhood.com/us/en/support/articles/agentic-trading-overview/
