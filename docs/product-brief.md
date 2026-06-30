# Product Brief

## One-Liner

Setup OS turns finalized AI planning conversations into local, self-hosted operating systems.

## Core User Promise

Users should be able to talk through a vertical in ChatGPT, Claude, Codex, or another AI tool, export the finalized conversation, and ask Setup OS to produce a local working system with memory, reports, alerts, audit logs, and a safe evolution path.

## What Setup OS Is

Setup OS is an AI systems architect.

It:

- extracts intent from planning conversations
- checks whether existing products or open-source tools solve the problem
- selects and justifies components
- proposes a local architecture
- generates a repo
- wires local deployment and notifications
- stores audit logs
- turns future conversations into reviewable evolution proposals

## What Setup OS Is Not

Setup OS is not:

- a generic agent framework
- a coding-agent replacement
- a dashboard builder
- a broker execution bot
- a hosted-only automation platform
- an autonomous system that mutates itself without approval

## First Vertical

Portfolio Manager Agent.

v0 should:

- import a portfolio planning conversation
- produce `agent_spec.json`
- generate `architecture.md`
- generate a local Portfolio Manager Agent scaffold
- use sample/local portfolio data
- produce a Markdown daily report
- emit a console notification
- accept a later conversation and output `evolution_proposal.md`

v0 should not:

- connect to Robinhood
- trade
- store broker credentials
- depend on cloud services
- build a full dashboard

## Product Principles

- Compose before build.
- Architecture is the product.
- UI is the last resort.
- Humans approve architecture.
- Every dependency needs a reason.
- Generated agents own their runtime UX.
- Local-first is the default.
- Future evolution must be reviewable.

## Open-Core Boundary

The CLI, local generation engine, schemas, blueprints, and local deployment path belong in the open core.

Hosted runners, encrypted sync, mobile apps, marketplaces, premium vertical packs, and team governance can become paid layers later.
