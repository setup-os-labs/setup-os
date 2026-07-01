# ADR 0005: Docs Site Timing

Status: Accepted

Date: 2026-07-01

## Context

Setup OS is still changing quickly. The highest-value docs today are product direction, ADRs, task queue, roadmap, research notes, and generated-system contracts that live close to the code.

A docs site can help public launch and contributor onboarding, but it also adds framework choices, navigation maintenance, deployment checks, and another surface to keep synchronized.

## Decision

Do not build a separate docs site during MVP.

Use repository-native Markdown as the canonical documentation surface until one of these triggers is met:

- public contributors need guided onboarding beyond `README.md`, `docs/`, and ADRs
- examples need richer navigation, screenshots, or generated API references
- a release requires stable public documentation URLs
- documentation search becomes meaningfully painful
- the desktop app needs hosted help pages or update notes

When a docs site is justified, prefer a minimal static site generated from the existing Markdown docs rather than moving docs into a separate content system.

## Rationale

Markdown in the repo keeps decisions reviewable in the same PRs as code. It is easier for Codex and humans to update, diff, and keep aligned with the active task queue.

The project currently benefits more from better docs content and stronger examples than from a docs framework. A site should be added when it reduces friction, not because public projects often have one.

## Consequences

- `README.md`, `docs/`, `research/`, `TASKS.md`, and `CHANGELOG.md` remain the source of truth.
- Every feature PR should continue updating docs and changelog entries where behavior changes.
- No docs-site CI, hosting, theme, or navigation framework is added during MVP.
- The v1 launch checklist keeps "docs site decision" as satisfied by this ADR unless new friction appears.
