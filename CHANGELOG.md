# Changelog

All notable changes to Setup OS are documented here.

This project follows a lightweight form of Keep a Changelog and uses semantic versioning once releases begin.

## [Unreleased]

### Added

- Portfolio Management OS building-block research with ranked stack options, rejected alternatives, and plug-and-play architecture guidance.
- Changelog hygiene rule requiring every PR to update `CHANGELOG.md` before merge.
- Python CLI scaffold for creating, evolving, and applying generated systems.
- Markdown/TXT conversation ingestion and deterministic v0 spec extraction.
- Portfolio and Health OS generated-agent scaffolds with reports, notifications, policy, release metadata, and `verify.py`.
- Evolution proposals with timeline events, notification inbox events, risk metadata, maturity levels, and approved candidate releases.
- Agent DNA, capability graph, action trust-level policy, and local audit/release snapshots.
- Documentation for the monorepo split policy, Notification OS boundary, agnostic architecture, desktop app stack, and Portfolio Management OS blueprint.
- README status tiles, tech stack, and desktop-first app direction.
- Codex development workflow, active task queue, GitHub templates, CI, and branch protection expectations.

### Decided

- Keep Setup OS in a monorepo through MVP.
- Build the Setup OS desktop app before building the real Portfolio Management OS.
- Use Tauri v2, React, and TypeScript for the desktop shell.
- Package Python as a bundled sidecar for desktop releases.
- Keep FastAPI optional until the desktop app needs a long-running local service.
- Start Portfolio Management OS with official Robinhood Agentic/MCP-style read-only access when available.
- Store imported conversations as raw memory first, then extract structured facts after review.
- Prefer squash merges for iterative Codex PRs unless commits are intentionally structured for long-term history.

## [0.0.0] - 2026-06-30

### Added

- Initial research artifact for the first 20 Setup OS component choices.
