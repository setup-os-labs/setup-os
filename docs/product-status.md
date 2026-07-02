# Product Status

Current checkpoint: Setup OS has crossed the 75% local desktop MVP milestone, but it is not a finished product.

## Completion Estimate

- Setup OS desktop MVP: about 90%.
- Generated Portfolio Management OS local v0: about 65%.
- End-to-end vision, where Setup OS desktop creates Portfolio Management OS from saved conversations and a personal runtime node runs it day to day: about 60%.

The desktop MVP has reached the 90% target. The next practical target is 95%, focused on sidecar smoke checks, release automation hardening, and a more polished packaged-app path.

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
- Desktop Portfolio dashboard cards summarize selected workspace, health, report, notifications, and memory drafts.
- Desktop Portfolio insight review extracts holdings, alerts, transactions, cash, watchlist, market snapshot, and performance sections from generated reports.
- Generated agents include a first `runtime_node.py` one-shot runner for personal runtime node health/report/inbox cycles.
- Runtime node scheduling notes explain how to run generated agents with macOS launchd, Windows Task Scheduler, or Linux cron.
- Desktop runtime-node log review can inspect generated `.setup_os/runtime_node.jsonl` cycles from the selected workspace.
- Desktop release readiness check reports local packaging workflow, Tauri config, icons, CI, CLI, and release-note readiness.
- Python sidecar packaging contract defines resolver order, expected release layout, and release gates for shipping without local Python.
- Desktop Python runner now resolves `SETUP_OS_PYTHON`, future sidecar Python, then system `python` through one command path.
- Signing and notarization plan defines Windows and macOS public-release gates without committing secrets.
- Python CLI for create, evolve, and approval-gated apply.
- Generated Portfolio Management OS scaffold with local imports, reports, alerts, memory drafts, audit trail, health checks, and notifications.

## Remaining To Reach 95%

- Add CI smoke checks for the sidecar resolver contract.
- Add sidecar release workflow scaffolding without committing runtime binaries.
- Add packaged-app smoke test instructions for Windows and macOS.

## Still Later

- Signed installers and updater flow.
- Bundled Python sidecar.
- Robinhood read-only connector.
- OpenBB/live market data adapter.
- SQLite state layer.
- Full Notification OS.
- Rich Portfolio dashboard.
