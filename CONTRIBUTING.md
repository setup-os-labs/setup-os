# Contributing

Setup OS is currently early-stage and optimized for small, reviewable changes.

## Branches

Use short-lived branches:

```text
codex/<task-name>
feature/<task-name>
fix/<task-name>
docs/<task-name>
```

Codex-authored branches should use `codex/` by default.

## Pull Requests

Each PR should:

- map to one task in `TASKS.md`
- include a concise problem statement
- describe the user-visible change
- list verification performed
- update docs when behavior changes
- update `CHANGELOG.md` for user-facing changes
- add or update ADRs for architecture decisions

## Scope Rules

For v0, do not add:

- broker execution
- Robinhood credentials
- cloud dependencies
- rich dashboard UI
- marketplace features
- autonomous self-mutation

## Local-First Safety

Setup OS should default to:

- local files
- local execution
- explicit user approval
- reviewable diffs
- append-only audit logs
- no financial execution in v0

## Commit Style

Prefer clear imperative commits:

```text
Add portfolio blueprint scaffold
Document open-core boundary
Implement conversation ingestion
```
