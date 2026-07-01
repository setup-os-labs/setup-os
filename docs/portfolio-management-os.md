# Portfolio Management OS

Portfolio Management OS is the first serious generated vertical after Setup OS itself is ready.

It should prove the whole Setup OS promise:

```text
finalized planning conversation
  -> spec
  -> architecture
  -> generated local agent
  -> report
  -> notification
  -> evolution proposal
  -> approved candidate release
```

## Product Boundary

Portfolio Management OS is not a trading bot in v0.

It is a local, advisory, alert-first investing assistant.

## v0 Scope

- import portfolio planning conversations
- read local/sample holdings and transactions
- produce daily Markdown portfolio reports
- emit structured local notifications
- track strategy and policy through Agent DNA
- write audit and timeline events
- create evolution proposals from future conversations
- require explicit approval before candidate releases

## Explicitly Out Of Scope

- Robinhood execution
- broker credentials
- automated trades
- tax, legal, or financial advice claims
- cloud-only runtime
- full dashboard

## Required Generated Files

```text
portfolio-management-os/
  README.md
  agent_spec.json
  architecture.md
  agent_dna.json
  config.json
  verify.py
  report.py
  data/
    holdings.csv
  reports/
  memory/
    raw/
    structured/
    policy/
  notifications/
  evolution/
  audit/
  deployment/
  .setup_os/
    audit.jsonl
    timeline.jsonl
    notifications.jsonl
    releases/
```

## Maturity Model

- Level 1: advisory report only
- Level 2: alerts and notifications
- Level 3: human-approved external actions
- Level 4: tightly bounded automation
- Level 5: full autonomy

Portfolio Management OS starts at Level 2.

## Data Model Seeds

Portfolio Management OS should eventually normalize:

- holdings
- transactions
- cash
- watchlist
- allocation targets
- risk rules
- tax notes
- strategy notes
- notification rules
- approval policy

## Safety Constitution

Default policy:

- no broker credentials in v0
- no automated trades
- no sell orders without explicit approval
- no strategy mutation without an evolution proposal
- all external actions require approval

## Future Phases

1. CSV holdings and local reports.
2. Allocation drift and concentration alerts.
3. Price/news/event enrichment.
4. Optional ntfy or Apprise notifications.
5. Broker read-only connectors.
6. Human-approved execution through a supported broker interface.
7. Limited automation only for pre-approved rules.
