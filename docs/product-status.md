# Product Status

Current checkpoint: Setup OS has crossed the 95% local desktop MVP scaffold milestone, but it is not a public-release product yet.

For a visual view of local utility, Portfolio Management OS, and public release tracks, see [Development and release timeline](development-release-timeline.md).

For the practical Windows-first path to using Setup OS as your own local utility, see [Personal local setup guide](personal-local-setup.md).

## Completion Estimate

- Setup OS desktop MVP scaffold: about 96-97%.
- Setup OS as your personal local utility: about 85-90%.
- Generated Portfolio Management OS local v0: about 70%.
- End-to-end vision, where Setup OS desktop creates Portfolio Management OS from saved conversations and a personal runtime node runs it day to day: about 65%.

The desktop MVP has reached the 95% target for a local-first scaffold. The remaining work is release-grade polish: real bundled Python artifacts, signing/notarization execution, and installer/updater hardening.

## Usable Today

- Cross-platform Tauri desktop shell for macOS, Windows, and Linux.
- Manual unsigned desktop bundle workflow with verified Linux, Windows, and macOS artifacts.
- Desktop Portfolio launcher with editable/persisted output, seed conversation, update conversation, and CSV import paths.
- Desktop actions for create, import, extract memory, health, report, status, notification inbox, and one-click demo flow.
- Desktop action for archiving and recreating a selected generated Portfolio workspace.
- Desktop structured memory review now formats drafts into readable source, status, confidence, strategy, risk, and watchlist sections.
- Desktop report review can split the generated Portfolio daily report into readable sections.
- Desktop release testing notes explain how to validate unsigned Windows, macOS, and Linux artifacts.
- Architecture now defines the personal always-on runtime node for schedulers, generated agents, and phone notification dispatch.
- Desktop runtime diagnostics show the configured Python executable, version, repo root, and CLI import status.
- Desktop Portfolio dashboard cards summarize selected workspace, health, report, handoff, notifications, and memory drafts.
- Desktop Portfolio insight review extracts holdings, alerts, transactions, cash, watchlist, market snapshot, and performance sections from generated reports.
- Generated agents include a first `runtime_node.py` one-shot runner for personal runtime node health/report/inbox cycles.
- Generated agents include `handoff.py`, which writes `handoff.md` as a one-file local utility readiness checklist.
- Runtime node scheduling notes explain how to run generated agents with macOS launchd, Windows Task Scheduler, or Linux cron.
- Desktop runtime-node log review can inspect generated `.setup_os/runtime_node.jsonl` cycles from the selected workspace.
- Desktop release readiness check reports local packaging workflow, Tauri config, icons, CI, CLI, and release-note readiness.
- Python sidecar packaging contract defines resolver order, expected release layout, and release gates for shipping without local Python.
- Desktop Python runner now resolves `SETUP_OS_PYTHON`, future sidecar Python, then system `python` through one command path.
- Signing and notarization plan defines Windows and macOS public-release gates without committing secrets.
- CI runs a desktop release contract smoke check for sidecar, signing, release workflow, and readiness docs.
- CI runs a local utility smoke test that generates Portfolio OS, runs health/report/runtime node, imports a conversation, and extracts memory drafts.
- Desktop can run the local utility smoke test from the launcher to validate the same local loop interactively.
- Desktop can preview a saved Portfolio conversation before import, reporting readability and Portfolio/risk/watchlist signals without mutating memory.
- Desktop can write and display the generated Portfolio `handoff.md` local utility readiness checklist.
- Desktop demo flow writes the generated Portfolio `handoff.md`, and status/dashboard show whether it exists.
- Personal local setup guide explains the Windows-first local utility path, saved conversation import flow, runtime-node handoff, and phone-notification guardrails.
- Packaged app smoke-test notes define Windows and macOS manual verification.
- Sidecar release workflow scaffold defines how future release jobs should assemble Python without committing runtime binaries.
- Development and release timeline visualizes the local-first utility path, Portfolio OS path, and public commercial release path.
- Python CLI for create, evolve, and approval-gated apply.
- Generated Portfolio Management OS scaffold with local imports, reports, alerts, memory drafts, audit trail, health checks, handoff summaries, and notifications.

## Remaining After 95%

- Build real sidecar artifacts during release workflows.
- Execute signing/notarization with real project credentials.
- Add installer/updater policy and rollback procedure.

## Still Later

- Signed installers and updater flow.
- Bundled Python sidecar.
- Robinhood read-only connector.
- OpenBB/live market data adapter.
- SQLite state layer.
- Full Notification OS.
- Rich Portfolio dashboard.
