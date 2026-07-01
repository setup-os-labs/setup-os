# Active Task Queue

Status values: `todo`, `in-progress`, `blocked`, `review`, `done`.

## Now

| ID | Status | Owner | Branch | Task | Acceptance |
| --- | --- | --- | --- | --- | --- |
| SO-001 | done | Codex | `codex/open-core-product-setup` | Establish open-core GitHub product scaffold | README, changelog, roadmap, task queue, PR templates, and Codex workflow exist |
| SO-002 | review | Codex | `codex/setup-os-brand` | Create Python package and CLI skeleton | `python -m setup_os.cli --help` runs locally |
| SO-003 | review | Codex | `codex/setup-os-brand` | Add Markdown/TXT conversation ingestion | Example conversation parses into a normalized envelope |
| SO-004 | review | Codex | `codex/setup-os-brand` | Add deterministic v0 spec extractor | `agent_spec.json` is produced for portfolio example |
| SO-005 | todo | Codex | `codex/portfolio-blueprint` | Add Portfolio Manager Agent blueprint | Generated repo contains README, config, report command, and sample data |
| SO-006 | todo | Codex | `codex/evolution-proposal` | Add evolution proposal flow | Second conversation creates `evolution_proposal.md` without mutating generated agent |

## Next

| ID | Status | Owner | Branch | Task | Acceptance |
| --- | --- | --- | --- | --- | --- |
| SO-007 | todo | Codex | `codex/audit-log` | Add append-only audit log | Create/evolve actions write JSONL audit events |
| SO-008 | todo | Codex | `codex/notification-interface` | Add notification provider interface and console adapter | Generated agent can emit a test console notification |
| SO-009 | todo | Codex | `codex/static-component-registry` | Add static component registry | Architecture proposal cites selected components and rejected alternatives |
| SO-010 | todo | Codex | `codex/architecture-proposal` | Generate architecture proposal Markdown | Proposal includes runtime, storage, notification, approval, and dependency rationale |
| SO-011 | todo | Codex | `codex/pytest-foundation` | Add pytest foundation | Tests cover ingestion, spec extraction, generation, and evolution proposal |

## Later

| ID | Status | Owner | Branch | Task | Acceptance |
| --- | --- | --- | --- | --- | --- |
| SO-012 | todo | Codex | `codex/ntfy-adapter` | Add optional ntfy adapter | Adapter is disabled by default and documented |
| SO-013 | todo | Codex | `codex/adr-index` | Add ADR index generator or convention | ADRs are easy to discover and link from PRs |
| SO-014 | todo | Codex | `codex/docs-site` | Evaluate docs site need | Decision recorded; no site built unless it reduces contributor friction |

## Backlog Rules

- Keep tasks small enough for one Codex PR.
- Every task needs acceptance criteria.
- Prefer CLI, Markdown, and deterministic files before UI.
- Add architecture decisions to `docs/adr/`.
- Move completed items to `done`; do not delete historical tasks.
