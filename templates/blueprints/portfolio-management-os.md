# Portfolio Management OS Blueprint

Use this blueprint for the first generated vertical after Setup OS.

## Inputs

- finalized portfolio planning conversation
- local holdings CSV
- local transactions CSV
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
| Evolution | proposal Markdown | candidate release + tests |
| Policy | alert-only | approval execution |

## Generated Commands

```bash
python report.py
python verify.py
```

## Safety

The generated system must remain advisory until the user explicitly approves a higher maturity level.
