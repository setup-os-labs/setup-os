# Portfolio Management OS

Portfolio Management OS is the first serious generated vertical after the Setup OS desktop app is ready.

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
- import saved ChatGPT financial conversations
- import Robinhood portfolio data in read-only mode
- store imported conversations as raw memory first, then extract structured portfolio facts
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
- Robinhood read-only account snapshots
- imported financial conversations
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

1. Setup OS desktop app can import saved conversations and launch verticals.
2. Robinhood read-only import and local reports.
3. ChatGPT financial discussion import into raw memory.
4. Structured extraction from raw conversations into holdings context, strategy notes, risk rules, and watchlists.
5. Allocation drift and concentration alerts.
6. Price/news/event enrichment.
7. Optional ntfy or Apprise notifications.
8. Human-approved execution through a supported broker interface.
9. Limited automation only for pre-approved rules.

## Robinhood Direction

Use Robinhood only in read-only mode at first.

Preferred path:

- official Robinhood Agentic/MCP-style read-only access if available to the user
- otherwise manual export or user-provided account snapshots

Do not use unofficial trading APIs as the default. Do not store credentials until there is a reviewed connector and explicit user approval.

## Building Block Research

The current working recommendation is to build the v0 as a small local system first, while preserving plug-and-play adapter boundaries for a richer Portfolio Management OS later.

Recommended center of gravity:

- Setup OS generated local Python vertical for v0.
- Raw-first conversation memory, then structured extraction after review.
- OpenBB-style market data adapter when real data enrichment begins.
- LangGraph-style workflow orchestration when the agent needs durable, human-in-the-loop state.
- Ghostfolio-style cockpit only after the raw import, reports, alerts, and evolution flow are proven.
- Robinhood official Agentic/MCP-style connector as read-only first, with execution out of scope until explicit approval workflows are mature.

See [research/portfolio-management-os-building-blocks.md](../research/portfolio-management-os-building-blocks.md) for the ranked stack options and rejected alternatives.
