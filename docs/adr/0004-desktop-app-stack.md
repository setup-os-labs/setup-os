# ADR 0004: Cross-Platform Desktop App Stack

Status: Accepted

Date: 2026-07-01

## Context

Setup OS started as a Python CLI because the first product risk was the conversation-to-system pipeline, not UI.

The product should now become a local desktop utility before Portfolio Management OS is built as a real generated vertical. The desktop app is how the user will import previously saved conversations and create Portfolio Management OS.

The desired desktop feel is closer to a polished local productivity app than a heavy web dashboard.

## Decision

Use a staged stack:

1. Python 3.12+ standard-library core for the engine, CLI, generation, specs, audit logs, and tests.
2. Tauri v2 + React + TypeScript for the desktop app shell.
3. Package Python as a bundled sidecar for desktop distribution.
4. FastAPI only when Setup OS needs a local HTTP API between the desktop shell and the Python engine.
5. SQLite when generated systems need structured local state beyond files and JSONL.
6. Keep Electron as a fallback only if Tauri blocks critical desktop capabilities.
7. Build the Setup OS desktop app before building the real Portfolio Management OS.
8. Make the first desktop screen a rich vertical agent launcher and dashboard shell.

## Rationale

Tauri gives a smaller native desktop shell than Electron and fits the local-first direction. React and TypeScript keep the UI ecosystem familiar. Python remains the right engine language because Setup OS is mostly parsing, generation, local orchestration, and agent-adjacent tooling.

FastAPI is useful, but it should not be introduced until there is a real local service boundary. A CLI-first engine is easier to test, package, and reason about during MVP.

For packaged desktop releases, bundle Python as a sidecar so ordinary macOS and Windows users do not need to install Python manually. During development, continue using the local Python interpreter and CLI because it keeps tests and iteration simple.

## Tauri Over Electron

Prefer Tauri because:

- Smaller app bundle and lower idle memory are a better fit for a local utility users may keep open all day.
- Native webview shell fits Setup OS's desktop-first but not UI-heavy direction.
- Rust-based shell gives a cleaner path for OS integrations without making JavaScript the whole runtime.
- The Python engine can remain separate from the UI shell instead of being absorbed into a Node/Electron app.

Prefer Electron only if:

- Tauri packaging becomes too brittle across macOS and Windows.
- Required desktop APIs are significantly easier or more reliable in Electron.
- The team needs a mature plugin ecosystem more than a lightweight native shell.

The first desktop spike should validate packaging, launching the Python engine, reading local files, and calling `python -m setup_os.cli --help` on both macOS and Windows.

## Current Stack

- Core engine: Python 3.12+
- CLI: `argparse`
- State: JSON, JSONL, Markdown, local files
- Tests: stdlib `unittest`
- CI: GitHub Actions
- Generated agents: local Python scaffolds

## Planned Stack

- Desktop: Tauri v2
- Frontend: React + TypeScript
- Styling: Tailwind CSS + a small component system
- Packaging: bundled Python sidecar for release builds
- Local API: FastAPI, only if needed
- Local data: SQLite plus files
- Notifications: console and local inbox first; ntfy/Apprise later

## Process Mode Decision

Start with Python as a CLI subprocess from Tauri during development.

Use a bundled Python sidecar for packaged desktop releases.

Move to a FastAPI local service only if the desktop app needs:

- long-running background jobs
- streaming progress
- multiple concurrent requests
- a local API for generated agents
- richer in-app state shared across screens

The sidecar should expose the same CLI contract as development mode first. Add a FastAPI service only after the dashboard needs streaming progress, concurrent work, or shared state that becomes awkward through subprocess calls.

## Windows Support Decision

Target native Windows and macOS first.

WSL can remain an advanced/developer path, but ordinary users should not need WSL to run Setup OS. The desktop spike must test native Windows packaging early.

## First Desktop Surface

Start with a rich vertical agent launcher and dashboard shell.

The launcher should show:

- created vertical agents
- create-from-conversation action
- recent evolution proposals
- notification/timeline badges
- verify/run controls
- raw conversation import status
- extraction status
- release/candidate status

Timeline and notification inbox can become the second surface once generated agents produce enough events.

## SQLite Decision Rule

Keep files, JSON, JSONL, and Markdown until one of these becomes painful:

- querying many events
- filtering notifications
- joining conversations to proposals to releases
- tracking multiple generated agents
- running desktop views over timeline/history

Introduce SQLite when the desktop app needs indexed local state.

## Notification Decision Rule

Keep console and local inbox until the desktop app exists.

Then decide:

- `ntfy` when the first need is simple phone push.
- Apprise when multi-channel routing matters.
- Notification OS inbox when snooze/done/explain/quiet-hours become product features.
