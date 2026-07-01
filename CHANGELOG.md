# Changelog

All notable changes to Setup OS are documented here.

This project follows a lightweight form of Keep a Changelog and uses semantic versioning once releases begin.

## [Unreleased]

### Added

- Generated Portfolio Manager read-only cash CSV importer and cash-aware total portfolio value reporting.
- Generated Portfolio Manager read-only transaction CSV importer and recent-activity report section.
- Generated Portfolio Manager allocation drift warnings against local target weights.
- Generated Portfolio Manager read-only holdings snapshot importer with validation and import manifest.
- ADR 0005 documenting that repository-native Markdown remains canonical through MVP before adding a docs site.
- Optional disabled-by-default ntfy notification adapter for core notifications and generated agents.
- Generated Portfolio Manager daily report concentration warnings with local warning notifications.
- Generated-agent `extract_memory.py` command that turns raw conversation imports into review-only structured memory drafts.
- Generated-agent raw conversation import command that copies saved chats into `memory/raw` with a manifest and checksum without mutating strategy.
- Parallel CI jobs and Rust build caching to shorten feedback for Python, desktop frontend, and native Tauri checks.
- Standard generated diagram pack with offline HTML, editable D2 source, local SVG icons, and diagram manifest.
- Branch history policy for retained archival branches such as `codex/setup-os-brand`.
- Native Tauri CI validation with Linux prerequisites and `tauri build --no-bundle`.
- Desktop Rust dependency pin for reproducible native Tauri builds.
- Desktop Tauri icon asset required by the native build context.
- Branch-retention workflow guidance for keeping merged Codex branches visible on GitHub.
- ADR index and convention for keeping architecture decisions discoverable.
- Generated-agent `health.py` runtime checks for required files, config policy, scheduler folder, reports folder, and notification inbox validity.
- CI checks for the desktop frontend package, including npm install, TypeScript, production build, and dependency audit.
- Tauri-ready desktop shell scaffold with React/TypeScript launcher UI and a Python CLI command contract.
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
