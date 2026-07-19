# ADR 0002: Portfolio Manager Agent Is The First Vertical

Status: Accepted

Date: 2026-06-30

## Context

Setup OS needs a concrete proof vertical. The Portfolio Manager Agent demonstrates conversation ingestion, architecture proposal, local generation, reporting, notifications, and future evolution.

Financial automation is sensitive and should not start with broker execution.

## Decision

Use Portfolio Manager Agent as the v0 vertical.

v0 is alert-only:

- local sample portfolio data
- Markdown daily report
- console notification adapter
- no broker credentials
- no Robinhood execution
- no automated trading

## Consequences

Benefits:

- meaningful real-world use case
- strong safety boundary
- clear generated outputs
- good test case for future evolution

Costs:

- less impressive than real trading automation
- future broker integration will need deeper policy, legal, and security review
