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
- import Robinhood/manual portfolio data, transactions, cash balances, watchlists, and market snapshots as read-only local CSV files
- store imported conversations as raw memory first, with manifest metadata and checksum, then extract structured portfolio facts
- keep structured extraction outputs as review-only drafts until promoted by an approved proposal
- produce a review-only memory update report from recurring saved finance conversations
- review Memory Update Reports from the desktop app before any fact, preference, open-loop, risk-rule, tax-note, or watchlist item is promoted
- let the extraction layer recommend its own new extractors, schema fields, scoring rubrics, and checks behind approval
- review Functional Evolution Reports from the desktop app before any extractor, schema, classifier, scoring, or quality-check proposal is versioned
- run a weekly local review loop that imports a saved conversation, extracts memory, writes review artifacts, snapshots extractor versions, checks health, refreshes reports, and writes handoff status
- bundle the review artifacts into one local approval packet before any memory, policy, strategy, or extractor behavior changes are promoted
- produce daily Markdown portfolio reports
- summarize offline unrealized performance from local cost basis and market snapshot files
- warn on concentration above the local review threshold
- warn on allocation drift outside the local target review band
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
  import_portfolio_snapshot.py
  import_portfolio_transactions.py
  import_portfolio_cash.py
  import_portfolio_watchlist.py
  import_portfolio_market_data.py
  import_conversation.py
  extract_memory.py
  memory_update_report.py
  functional_evolution_report.py
  extraction_observability.py
  extractor_versioning.py
  weekly_review.py
  review_packet.py
  report.py
  health.py
  runtime_node.py
  handoff.py
  data/
    holdings.csv
    allocation_targets.csv
    transactions.csv
    cash.csv
    watchlist.csv
    market_data.csv
    portfolio_import_manifest.jsonl
    transaction_import_manifest.jsonl
    cash_import_manifest.jsonl
    watchlist_import_manifest.jsonl
    market_data_import_manifest.jsonl
  reports/
  memory/
    raw/
    structured/
    policy/
  notifications/
  evolution/
    review_packet.md
  audit/
  deployment/
  .setup_os/
    audit.jsonl
    timeline.jsonl
    notifications.jsonl
    weekly_review.jsonl
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
- no extractor, schema, prompt, or scoring-rubric mutation without a functional evolution proposal
- all external actions require approval

## Self-Evolving Extraction Direction

Portfolio Management OS should become the first proof vertical for the self-evolving extraction engine.

The saved-chat ingestion loop now produces the first two report types and should eventually expose richer desktop review:

- Memory Update Report: new facts, preferences, decisions, open loops, risk rules, tax notes, and watchlist changes.
- Functional Evolution Report: recommended extractors, schema fields, comparison dimensions, contradiction checks, scoring rubrics, and noise filters.
- Pipeline Observability Summary: chats processed, drafts created, low-confidence items, conflicts, rejected noise, and proposed upgrades.
- Evidence Map: links from each proposed memory or functional change back to imported conversation records.
- Extraction Observability Report: processed inputs, noisy lines, low-confidence drafts, conflict signals, source checksums, and evidence locations.
- Extractor Version Snapshot: hashes of extractor files and a rollback plan before approving functional changes.

The functional layer should learn how to learn better only through approved changes. Examples include a cash yield optimization extractor, speculative trading risk gate, AI bottleneck thesis tracker, intent-state classifier, and contradiction checker.

Finance-specific extraction should distinguish curiosity, serious consideration, rejected ideas, approved strategies, and active behavior so exploratory questions do not become false preferences.

## Future Phases

1. Setup OS desktop app can import saved conversations and launch verticals.
2. Robinhood/manual read-only CSV holdings, transactions, cash, watchlist, and market snapshot import with local reports.
3. ChatGPT financial discussion import into raw memory.
4. Structured extraction drafts from raw conversations into holdings context, strategy notes, risk rules, and watchlists.
5. Memory update report with evidence and review-only approval status.
6. Functional evolution report for extractor, schema, comparison, scoring, and contradiction-check upgrades.
7. Pipeline observability and traceability review in the desktop app.
8. Allocation drift and concentration alerts.
9. Local price/event snapshot enrichment and offline performance summary before live data APIs.
10. Optional ntfy or Apprise notifications.
11. Human-approved execution through a supported broker interface.
12. Limited automation only for pre-approved rules after extractor versioning and rollback are proven.

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
- Structured memory drafts must be marked `draft_requires_review` and must not mutate strategy, policy, alerts, or releases directly.
- Functional extraction upgrades must be review-only proposals until approved and versioned.
- OpenBB-style market data adapter when real data enrichment begins.
- LangGraph-style workflow orchestration when the agent needs durable, human-in-the-loop state.
- Ghostfolio-style cockpit only after the raw import, reports, alerts, and evolution flow are proven.
- Robinhood official Agentic/MCP-style connector as read-only first, with execution out of scope until explicit approval workflows are mature.

See [research/portfolio-management-os-building-blocks.md](../research/portfolio-management-os-building-blocks.md) for the ranked stack options and rejected alternatives.

