# Changelog

All notable changes to Setup OS are documented here.

This project follows a lightweight form of Keep a Changelog and uses semantic versioning once releases begin.

## [Unreleased]

### Added

- Desktop release workflow now uses explicit Tauri bundle icons so Linux AppImage and Windows MSI packaging can find required icon assets.
- Desktop release readiness check for packaging workflow, Tauri config, icons, CI, CLI, and release testing notes.
- Python sidecar packaging contract for future desktop releases that run without requiring local Python.
- Desktop Python command runner now resolves `SETUP_OS_PYTHON`, future sidecar Python, then system `python` through a single resolver.
- Desktop signing and notarization plan for future Windows and macOS public release gates.
- Desktop release contract CI smoke check for sidecar, signing, release workflow, and packaged-app readiness docs.
- Local utility smoke test for generating Portfolio OS, running health/report/runtime node, importing a conversation, and extracting memory drafts.
- Desktop launcher action for running the local utility smoke test interactively.
- Desktop Portfolio conversation preview action that checks a saved conversation before importing it into raw memory.
- Generated-agent `handoff.py` command that writes `handoff.md` as a local utility readiness checklist.
- Personal local setup guide for the Windows-first local utility path, saved conversation import, runtime-node handoff, and phone-notification guardrails.
- Packaged app smoke-test notes for Windows and macOS verification.
- Sidecar release workflow scaffold for future bundled Python artifacts without committing runtime binaries.
- Development and release timeline visualizing the local utility, Portfolio Management OS, and public commercial release tracks.
- Desktop ICO asset now has matching ICO directory and embedded PNG dimensions for macOS icon conversion during release packaging.
- Manual desktop release workflow for unsigned Linux, Windows, and macOS Tauri bundle artifacts.
- Verified manual desktop release workflow uploads Linux, Windows, and macOS unsigned bundle artifacts from `main`.
- Desktop Portfolio launcher now accepts an editable generated-agent output path for create, import, extract, health, report, status, and demo flow actions.
- Desktop Portfolio launcher now remembers the output path, conversation path, and CSV import paths between sessions.
- Desktop Portfolio create action now accepts a user-entered seed conversation path instead of only the bundled example conversation.
- Desktop Portfolio launcher can read the generated agent notification inbox from `.setup_os/notifications.jsonl`.
- Product status checkpoint documenting current completion estimate and the remaining desktop MVP work needed to reach 75%.
- Desktop readiness check for repo root, Python engine, seed conversation, and selected Portfolio workspace.
- Desktop Portfolio actions now validate required paths before invoking backend commands and show immediate next-step messages.
- Desktop Portfolio launcher can review structured memory draft JSONL files after extraction.
- Desktop Portfolio launcher can load a summary of workspace state, latest report preview, notification count, and memory draft count.
- Desktop Portfolio launcher can archive and recreate the selected generated workspace from the selected seed conversation.
- Desktop Portfolio memory draft review now formats draft source, status, confidence, strategy notes, risk rules, and watchlist items for easier review.
- Desktop Portfolio report review can group the generated daily report into readable Markdown sections.
- Desktop release testing notes for validating unsigned Linux, Windows, and macOS artifacts.
- Desktop Python runtime diagnostics for checking the configured Python executable, version, repo root, and CLI import status.
- Desktop Portfolio dashboard cards for selected workspace, health, report, notifications, and memory draft status.
- Desktop Portfolio insight review for generated report holdings, alerts, transactions, cash, watchlist, market snapshot, and performance sections.
- Generated agents now include `runtime_node.py` for one-shot personal runtime node health/report/inbox cycles.
- Runtime node scheduling notes for macOS launchd, Windows Task Scheduler, and Linux cron.
- Desktop runtime-node log review for generated `.setup_os/runtime_node.jsonl` cycles.
- Cross-platform native desktop CI matrix for Linux, Windows, and macOS Tauri compile checks.
- Desktop full Portfolio demo flow that creates the agent, imports sample data, extracts memory drafts, checks health, runs report, and refreshes status.
- Desktop Portfolio CSV import actions for holdings, transactions, cash, watchlist, and market snapshots.
- Desktop Portfolio conversation import now accepts an editable conversation path.
- Desktop launcher action for refreshing generated Portfolio Management OS artifact status.
- Desktop launcher action for extracting review-only Portfolio memory drafts.
- Desktop launcher action for importing an example saved Portfolio conversation into raw memory.
- Desktop launcher action for running the generated Portfolio Management OS health check.
- Desktop launcher action for running the generated Portfolio Management OS report and displaying the Markdown output.
- Desktop launcher action for generating the Portfolio Management OS example through the Python CLI.
- Generated Portfolio Manager offline performance summary using holdings cost basis and local market snapshots.
- Generated Portfolio Manager read-only market snapshot CSV importer and market-aware report pricing.
- Generated Portfolio Manager read-only watchlist CSV importer and watchlist report section.
- Generated Portfolio Manager read-only cash CSV importer and cash-aware total portfolio value reporting.
- Generated Portfolio Manager read-only transaction CSV importer and recent-activity report section.
- Generated Portfolio Manager allocation drift warnings against local target weights.
- Generated Portfolio Manager read-only holdings snapshot importer with validation and import manifest.
- ADR 0005 documenting that repository-native Markdown remains canonical through MVP before adding a docs site.
- ADR 0006 documenting the personal always-on runtime node for schedulers, generated agents, and phone notification dispatch.
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
- Use a personal runtime node before web-scale microservices for always-on schedulers, generated agents, and notification dispatch.

## [0.0.0] - 2026-06-30

### Added

- Initial research artifact for the first 20 Setup OS component choices.
