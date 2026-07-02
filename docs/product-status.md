# Product Status

Current checkpoint: Setup OS has crossed the 75% local desktop MVP milestone, but it is not a finished product.

## Completion Estimate

- Setup OS desktop MVP: about 84%.
- Generated Portfolio Management OS local v0: about 65%.
- End-to-end vision, where Setup OS desktop creates Portfolio Management OS from saved conversations and a personal runtime node runs it day to day: about 60%.

The desktop MVP has reached the 80% target. The next practical target is 85%, focused on installability, bundled runtime, and a more app-like Portfolio dashboard.

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
- Generated agents include a first `runtime_node.py` one-shot runner for personal runtime node health/report/inbox cycles.
- Runtime node scheduling notes explain how to run generated agents with macOS launchd, Windows Task Scheduler, or Linux cron.
- Python CLI for create, evolve, and approval-gated apply.
- Generated Portfolio Management OS scaffold with local imports, reports, alerts, memory drafts, audit trail, health checks, and notifications.

## Remaining To Reach 85%

- Bundle Python as a sidecar for release artifacts.
- Add deeper Portfolio dashboard sections for holdings, alerts, and report content.
- Add signed/notarized installer planning.
- Add runtime-node log review in the desktop.

## Still Later

- Signed installers and updater flow.
- Bundled Python sidecar.
- Robinhood read-only connector.
- OpenBB/live market data adapter.
- SQLite state layer.
- Full Notification OS.
- Rich Portfolio dashboard.
