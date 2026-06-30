# Codex Development Guide

This repo is designed for AI-native development with Codex.

## Working Agreement

Codex should:

- read `README.md`, `TASKS.md`, `docs/roadmap.md`, and relevant ADRs before implementation
- work from a short-lived branch named `codex/<task-name>`
- keep changes scoped to one task or one vertical slice
- update docs and task status in the same PR as the code
- add tests for extraction, generation, evolution, or safety behavior changes
- avoid broker execution, cloud dependencies, and rich dashboards in v0
- preserve local-first and human-approval-by-default behavior

## Task Lifecycle

1. Pick one task from `TASKS.md`.
2. Create or reuse a `codex/<task-name>` branch.
3. Implement the smallest useful slice.
4. Run the relevant tests or checks.
5. Update `TASKS.md`.
6. Update `CHANGELOG.md` for user-visible changes.
7. Open a PR with the template in `.github/PULL_REQUEST_TEMPLATE.md`.

## Definition of Done

A task is done when:

- the behavior is implemented or the document is landed
- tests or manual verification are recorded
- docs reflect the new behavior
- safety boundaries are unchanged or explicitly documented
- follow-up work is captured in `TASKS.md`

## Prompt Pattern

Use constrained prompts:

```text
Work on task <task-id> from TASKS.md.
Stay within v0 scope.
Do not add cloud dependencies, broker execution, or a dashboard.
Update docs and tests as needed.
Return a concise summary, verification, and follow-up tasks.
```

## Review Stance

Review PRs for:

- local-first guarantees
- human approval gates
- reproducible generation
- clear audit log behavior
- dependency justification
- minimal custom code where composition is enough
- task queue and changelog hygiene
