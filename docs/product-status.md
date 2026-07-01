# Product Status

Current checkpoint: Setup OS is a working local-first desktop MVP foundation, not a finished product.

## Completion Estimate

- Setup OS desktop MVP: about 72%.
- Generated Portfolio Management OS local v0: about 65%.
- End-to-end vision, where Setup OS desktop creates Portfolio Management OS from saved conversations and runs it day to day: about 60%.

The next practical target is 75% for the desktop MVP. That means the product should feel usable by its owner without reading repo internals.

## Usable Today

- Cross-platform Tauri desktop shell for macOS, Windows, and Linux.
- Manual unsigned desktop bundle workflow with verified Linux, Windows, and macOS artifacts.
- Desktop Portfolio launcher with editable/persisted output, seed conversation, update conversation, and CSV import paths.
- Desktop actions for create, import, extract memory, health, report, status, notification inbox, and one-click demo flow.
- Python CLI for create, evolve, and approval-gated apply.
- Generated Portfolio Management OS scaffold with local imports, reports, alerts, memory drafts, audit trail, health checks, and notifications.

## Remaining To Reach 75%

- Add desktop-visible validation before running actions, with clear next-step messages.
- Add a review surface for structured memory drafts instead of showing raw command output only.
- Add a desktop summary panel for latest report, notifications, and health state.
- Add a local reset/recreate flow for the selected generated workspace.

## Still Later

- Signed installers and updater flow.
- Bundled Python sidecar.
- Robinhood read-only connector.
- OpenBB/live market data adapter.
- SQLite state layer.
- Full Notification OS.
- Rich Portfolio dashboard.
