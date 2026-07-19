# Roadmap

## v0: Portfolio Agent Golden Path

Goal: prove that Setup OS can turn a planning conversation into a local generated vertical agent.

Required:

- Markdown/TXT conversation ingestion
- deterministic v0 spec extraction
- portfolio vertical detection
- static component registry
- architecture proposal Markdown
- generated Portfolio Manager Agent scaffold
- local daily report from sample portfolio data
- console notification adapter
- evolution proposal diff from a second conversation
- append-only audit log
- unittest coverage for the golden path

Explicitly out of scope:

- Robinhood execution
- broker credentials
- cloud services
- full Notification OS
- rich dashboard
- marketplace
- autonomous mutation

## v0.1: Safer Local Runtime

- approval gates
- better audit log schema
- evolution timeline
- confidence-scored evolution proposals
- maturity levels
- generated repo verification command
- dependency justification report
- ADR templates for generated agents
- optional ntfy adapter, disabled by default

## v0.2: More Vertical Blueprints

- Career OS
- Learning OS
- Home OS
- Health OS

Each new vertical must reuse the same ingestion, architecture, approval, generation, and evolution pipeline.


## v0.3: Notification OS Foundation

- shared notification event schema
- local notification inbox
- snooze, done, dismiss, and explain states
- calendar mirroring for time-bound events
- clear boundary between agent timeline and calendar

## v1: Public Open-Core Launch

- stable CLI
- docs site decision recorded in ADR 0005
- public examples
- GitHub release process
- contribution guidelines
- security policy
- initial community blueprint process

## Later Commercial Surface

- hosted control plane
- managed always-on runners
- encrypted sync
- mobile app
- template marketplace
- team and enterprise governance
