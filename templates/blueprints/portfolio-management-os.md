# Portfolio Management OS Blueprint

Use this blueprint for the first generated vertical after Setup OS.

## Inputs

- finalized portfolio planning conversation
- saved ChatGPT financial discussions
- Robinhood read-only portfolio import
- local holdings CSV fallback
- local transactions CSV fallback
- strategy notes
- approval policy

## Outputs

- `agent_spec.json`
- `architecture.md`
- `agent_dna.json`
- `config.json`
- daily Markdown report
- local notification inbox event
- audit log
- timeline event
- release snapshot

## Components

| Layer | Default | Later |
| --- | --- | --- |
| Runtime | Python local process | Docker Compose |
| Storage | local files + JSONL | SQLite |
| Reports | Markdown | dashboard export |
| Notifications | console + local inbox | ntfy + Apprise |
| Market data | sample/local CSV | yfinance, SEC EDGAR, broker read-only |
| Broker data | manual/CSV fallback | Robinhood Agentic/MCP-style read-only import |
| Conversation memory | raw imports first | structured extraction after review |
| Evolution | proposal Markdown | candidate release + tests |
| Policy | alert-only | approval execution |

## Generated Commands

```bash
python report.py
python verify.py
```

## Safety

The generated system must remain advisory until the user explicitly approves a higher maturity level.

Robinhood access must start read-only. Execution, credentials, and automated trading are out of scope for the first Portfolio Management OS.
