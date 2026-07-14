# Product Status

Current checkpoint: Setup OS has crossed the 95% local desktop MVP scaffold milestone, but it is not a public-release product yet.

For a visual view of local utility, Portfolio Management OS, and public release tracks, see [Development and release timeline](development-release-timeline.md).

For the practical Windows-first path to using Setup OS as your own local utility, see [Personal local setup guide](personal-local-setup.md).

## Completion Estimate

- Setup OS desktop MVP scaffold: about 97%.
- Setup OS as your personal local utility: about 88-90%.
- Generated Portfolio Management OS local v0: about 70%.
- End-to-end vision, where Setup OS desktop creates Portfolio Management OS from saved conversations and a personal runtime node runs it day to day: about 65%.

The desktop MVP has reached the 95% target for a local-first scaffold. The remaining work is release-grade polish: real bundled Python artifacts, signing/notarization execution, and installer/updater hardening.

## Usable Today

- Cross-platform Tauri desktop shell for macOS, Windows, and Linux.
- Manual unsigned desktop bundle workflow with verified Linux, Windows, and macOS artifacts.
- Desktop release workflow smoke-checks packaged bundle outputs and uploads `packaged-smoke-manifest.json`.
- Desktop Portfolio launcher with editable/persisted output, seed conversation, update conversation, and CSV import paths.
- Desktop actions for create, import, extract memory, health, report, status, notification inbox, and one-click demo flow.
- Desktop action for archiving and recreating a selected generated Portfolio workspace.
- Desktop structured memory review now formats drafts into readable source, status, confidence, strategy, risk, and watchlist sections.
- Desktop report review can split the generated Portfolio daily report into readable sections.
- Desktop release testing notes explain how to validate unsigned Windows, macOS, and Linux artifacts.
- Architecture now defines the personal always-on runtime node for schedulers, generated agents, and phone notification dispatch.
- Desktop runtime diagnostics show the configured Python executable, version, repo root, and CLI import status.
- Desktop Portfolio dashboard cards summarize selected workspace, health, report, handoff, notifications, and memory drafts.
- Desktop shell now uses decision-first Work, Review, and Operator surfaces so daily Portfolio use is separated from evidence review and diagnostics.
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
- Desktop can extract concise guidance from `handoff.md`, including missing readiness items, runtime status, counts, and next local steps.
- Generated agents can write a review-only `memory/structured/memory_update_report.md` with evidence-linked facts, preferences, open loops, decisions, risk rules, tax notes, and watchlist drafts.
- Generated agents can write a review-only `evolution/functional_evolution_report.md` with proposed extractor, schema, classifier, scoring, and quality-check upgrades.
- Generated agents can write a review-only `memory/structured/extraction_observability.md` with processed input counts, noisy lines, low-confidence drafts, conflict signals, source checksums, and evidence locations.
- Desktop backend can read generated Portfolio extraction observability reports.
- Generated agents can write `evolution/extractor_versions.jsonl` and `evolution/extractor_rollback_plan.md` before approving extractor changes.
- Generated agents can run `weekly_review.py` to execute the local import, extraction, review reports, observability, version snapshot, health, report, and handoff loop with `.setup_os/weekly_review.jsonl` evidence.
- Generated agents can write `evolution/review_packet.md` as a single approval packet across memory updates, functional evolution, observability, rollback/versioning, weekly logs, and handoff status.
- Personal local setup guide explains the Windows-first local utility path, saved conversation import flow, runtime-node handoff, and phone-notification guardrails.
- Packaged app smoke-test notes define Windows and macOS manual verification.
- Packaged app smoke-test notes now start with checking the generated artifact smoke manifest.
- Sidecar release workflow scaffold defines how future release jobs should assemble Python without committing runtime binaries.
- Development and release timeline visualizes the local-first utility path, Portfolio OS path, and public commercial release path.
- Python CLI for create, evolve, and approval-gated apply.
- Generated Portfolio Management OS scaffold with local imports, reports, alerts, memory drafts, audit trail, health checks, handoff summaries, and notifications.
- Architecture now records self-evolving extraction as a future direction: memory updates and functional extractor upgrades are separate approval-gated paths.

## Remaining After 95%

- Build real sidecar artifacts during release workflows.
- Execute signing/notarization with real project credentials.
- Add installer/updater policy and rollback procedure.
- Add desktop review for extractor rollback snapshots before limited automation.

## Still Later

- Signed installers and updater flow.
- Bundled Python sidecar.
- Desktop review flow for generated Memory Update Reports.
- Desktop review flow for generated Functional Evolution Reports.
- Desktop UI surface for extraction observability and traceability review.
- Approval-gated extractor upgrades for new schemas, classifiers, comparison dimensions, contradiction checks, and scoring rubrics.
- Robinhood read-only connector.
- OpenBB/live market data adapter.
- SQLite state layer.
- Full Notification OS.
- Rich Portfolio dashboard.
- Richer first-run onboarding and clickable system explainer built around the Work, Review, and Operator model.

