# Branching And Releases

## Branches

Default branches:

- `master` or `main`: stable integration branch
- `codex/<task-name>`: Codex-authored implementation branch
- `docs/<topic>`: documentation-only branch
- `fix/<issue>`: bug fix branch
- `release/<version>`: release preparation branch, when needed

## Pull Requests

Every meaningful change should go through a PR.

PRs should stay small:

- one task
- one feature slice
- one architecture decision
- one documentation improvement

## Changelog

Update `CHANGELOG.md` for:

- user-visible behavior
- CLI changes
- generated output changes
- architecture or policy changes
- release notes

## Versioning

Use `0.x.y` while the CLI and schemas are unstable.

After v1:

- major: breaking CLI/schema changes
- minor: new capabilities
- patch: fixes and docs

## Release Checklist

- tests pass
- changelog updated
- docs updated
- task queue reflects completed work
- ADRs added for architecture changes
- tag created
- GitHub release notes published
