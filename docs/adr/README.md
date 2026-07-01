# Architecture Decision Records

Setup OS keeps architecture decisions in this folder so product direction does not disappear into chat history.

## Index

| ADR | Status | Decision |
| --- | --- | --- |
| [0001: Open-Core Monorepo](0001-open-core-monorepo.md) | Accepted | Keep Setup OS in one monorepo through MVP and split only when a folder becomes its own product, API, or community surface. |
| [0002: v0 Portfolio Agent](0002-v0-portfolio-agent.md) | Accepted | Make the first proof vertical a local, alert-only Portfolio Manager Agent. |
| [0003: Human Approval First](0003-human-approval-first.md) | Accepted | Keep generated system changes reviewable and require explicit approval for risky actions. |
| [0004: Cross-Platform Desktop App Stack](0004-desktop-app-stack.md) | Accepted | Use Python for the engine and Tauri v2, React, and TypeScript for the desktop shell. |

## Convention

- Add a new ADR for durable architecture, product, packaging, safety, repository, or stack decisions.
- Use a monotonically increasing four-digit prefix.
- Link new ADRs from this index in the same PR.
- Update `CHANGELOG.md` when an ADR records a user-visible direction change.
