# ADR 0004: Cross-Platform Desktop App Stack

Status: Proposed

Date: 2026-07-01

## Context

Setup OS starts as a Python CLI because the first product risk is the conversation-to-system pipeline, not UI.

The product should eventually feel like a local desktop utility: cross-platform, private by default, easy to run on macOS and Windows, and capable of managing generated vertical agents, notifications, approvals, and evolution proposals.

The desired desktop feel is closer to a polished local productivity app than a heavy web dashboard.

## Decision

Use a staged stack:

1. Python 3.12+ standard-library core for the engine, CLI, generation, specs, audit logs, and tests.
2. Tauri v2 + React + TypeScript for the future desktop app shell.
3. FastAPI only when Setup OS needs a local HTTP API between the desktop shell and the Python engine.
4. SQLite when generated systems need structured local state beyond files and JSONL.
5. Keep Electron as a fallback only if Tauri blocks critical desktop capabilities.

## Rationale

Tauri gives a smaller native desktop shell than Electron and fits the local-first direction. React and TypeScript keep the UI ecosystem familiar. Python remains the right engine language because Setup OS is mostly parsing, generation, local orchestration, and agent-adjacent tooling.

FastAPI is useful, but it should not be introduced until there is a real local service boundary. A CLI-first engine is easier to test, package, and reason about during MVP.

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
- Local API: FastAPI, only if needed
- Local data: SQLite plus files
- Notifications: console and local inbox first; ntfy/Apprise later

## Open Questions

- Should the desktop shell start before or after the Portfolio Management OS golden path is stable?
- Should Python run as a Tauri sidecar, a local HTTP service, or a CLI subprocess?
- Should Windows support target native Windows first, WSL first, or both?
- Should the first desktop screen be an inbox/timeline, a generator wizard, or a vertical-agent launcher?
