# Codex Development Guide

This repo is designed for AI-native development with Codex.

## Working Agreement

Codex should:

- read `README.md`, `TASKS.md`, `docs/roadmap.md`, and relevant ADRs before implementation
- work from a short-lived branch named `codex/<task-name>`
- keep changes scoped to one task or one vertical slice
- prefer squash merges for iterative Codex PRs unless commits are intentionally structured for long-term history
- keep merged remote branches unless the user explicitly asks to delete them
- treat restored old branches as archival unless comparison shows unique work not already represented on `main`
- update docs and task status in the same PR as the code
- update `CHANGELOG.md` in every PR before merge, even for documentation-only changes
- update the development timeline, product status, roadmap, guides, and ADRs whenever a PR changes product scope, architecture, release posture, workflow, or completion estimates
- add tests for extraction, generation, evolution, or safety behavior changes
- avoid broker execution, cloud dependencies, and rich dashboards in v0
- preserve local-first and human-approval-by-default behavior

## Task Lifecycle

1. Pick one task from `TASKS.md`.
2. Create or reuse a `codex/<task-name>` branch.
3. Implement the smallest useful slice.
4. Run the relevant tests or checks.
5. Update `TASKS.md`.
6. Update `CHANGELOG.md` with a short entry for the PR.
7. Update relevant docs:
   - `docs/development-release-timeline.md` and `docs/product-status.md` for status, roadmap, or completion estimate changes
   - product guides such as `docs/personal-local-setup.md` or `docs/portfolio-management-os.md` for user-facing workflow changes
   - `docs/adr/` for durable architecture, stack, safety, release, or repository decisions
8. Open a PR with the template in `.github/PULL_REQUEST_TEMPLATE.md`.
9. Squash merge iterative PRs to keep `main` readable; use normal merge only when each commit is intentionally reviewed and meaningful on its own.
10. Do not delete the remote branch after merge unless explicitly requested.
11. Before opening a PR from an old or restored branch, compare it against `main`; do not merge it only because it was recently pushed.

## Branch History

Some remote branches are retained after squash merges for traceability. A retained branch can look recently active if it was restored or pushed again, even when its product work is already represented on `main`.

When evaluating a retained branch:

1. Check whether it already has merged PRs.
2. Compare it against `origin/main`.
3. If the branch is older than `main` and a dry merge would reintroduce conflicts or older file versions, keep it as archival history.
4. Only open a new PR when the branch contains unique, intentional changes that should land on top of current `main`.

Known archival/superseded branch:

- `codex/setup-os-brand`: source branch for early Setup OS scaffold work that was merged through PR #1 and PR #2, then superseded by later squash merges on `main`.

## Definition of Done

A task is done when:

- the behavior is implemented or the document is landed
- tests or manual verification are recorded
- docs reflect the new behavior
- timeline, product status, roadmap, guides, and ADRs are updated or explicitly not applicable
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
