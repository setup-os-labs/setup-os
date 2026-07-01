# Active Task Queue

Status values: `todo`, `in-progress`, `blocked`, `review`, `done`.

## Now

| ID | Status | Owner | Branch | Task | Acceptance |
| --- | --- | --- | --- | --- | --- |
| SO-001 | done | Codex | `codex/open-core-product-setup` | Establish open-core GitHub product scaffold | README, changelog, roadmap, task queue, PR templates, and Codex workflow exist |
| SO-002 | done | Codex | `codex/setup-os-brand` | Create Python package and CLI skeleton | `python -m setup_os.cli --help` runs locally |
| SO-003 | done | Codex | `codex/setup-os-brand` | Add Markdown/TXT conversation ingestion | Example conversation parses into a normalized envelope |
| SO-004 | done | Codex | `codex/setup-os-brand` | Add deterministic v0 spec extractor | `agent_spec.json` is produced for portfolio example |
| SO-005 | done | Codex | `codex/setup-os-brand` | Add Portfolio Manager Agent blueprint | Generated repo contains README, config, report command, and sample data |
| SO-006 | done | Codex | `codex/setup-os-brand` | Add evolution proposal flow | Second conversation creates `evolution_proposal.md` without mutating generated agent |

## Next

| ID | Status | Owner | Branch | Task | Acceptance |
| --- | --- | --- | --- | --- | --- |
| SO-007 | done | Codex | `codex/setup-os-brand` | Add append-only audit log | Create/evolve actions write JSONL audit events |
| SO-008 | done | Codex | `codex/setup-os-brand` | Add notification provider interface and console adapter | Generated agent can emit a test console notification |
| SO-009 | done | Codex | `codex/setup-os-brand` | Add static component registry | Architecture proposal cites selected components and rejected alternatives |
| SO-010 | done | Codex | `codex/setup-os-brand` | Generate architecture proposal Markdown | Proposal includes runtime, storage, notification, approval, and dependency rationale |
| SO-011 | done | Codex | `codex/setup-os-brand` | Add unittest foundation | Tests cover ingestion, spec extraction, generation, and evolution proposal |
| SO-015 | done | Codex | `codex/setup-os-brand` | Add planning conversation guide and starter vertical templates | Docs explain Think/Build/Evolve, minimum input/output, missing-decision checks, and five guide templates exist |
| SO-016 | done | Codex | `codex/setup-os-brand` | Add spec completeness checker | `create` reports missing runtime, privacy, alert, data, and approval decisions without blocking generation |
| SO-017 | review | Codex | `codex/evolution-notification-foundation` | Add evolution timeline and richer proposal metadata | `evolve` writes confidence, risk, memory layer, maturity level, and timeline events |
| SO-018 | review | Codex | `codex/evolution-notification-foundation` | Document Notification OS boundary | Docs define Notification OS, calendar mirroring, and connector/MCP direction |

## Later

| ID | Status | Owner | Branch | Task | Acceptance |
| --- | --- | --- | --- | --- | --- |
| SO-012 | todo | Codex | `codex/ntfy-adapter` | Add optional ntfy adapter | Adapter is disabled by default and documented |
| SO-013 | todo | Codex | `codex/adr-index` | Add ADR index generator or convention | ADRs are easy to discover and link from PRs |
| SO-014 | todo | Codex | `codex/docs-site` | Evaluate docs site need | Decision recorded; no site built unless it reduces contributor friction |
| SO-019 | review | Codex | `codex/evolution-notification-foundation` | Add notification event schema and inbox file | Generated agents can emit structured notification events with snooze/done/dismiss states |
| SO-020 | review | Codex | `codex/evolution-notification-foundation` | Add Health OS blueprint detection | Health planning conversation creates a health-oriented spec and architecture proposal |
| SO-021 | review | Codex | `codex/evolution-notification-foundation` | Add agnostic architecture and Agent DNA | Docs define provider-neutral layers; generated portfolio agent includes `agent_dna.json` and quality score |
| SO-022 | review | Codex | `codex/evolution-notification-foundation` | Add capability dependency graph | Portfolio architecture proposal includes capability dependencies and affected surfaces |
| SO-023 | review | Codex | `codex/evolution-notification-foundation` | Add generated-agent release snapshots | Create/evolve can preserve versioned release metadata for future rollback |
| SO-024 | review | Codex | `codex/evolution-notification-foundation` | Add first non-portfolio vertical skeleton | Health OS planning conversation produces a generated health scaffold with local reports and no medical-action automation |
| SO-025 | todo | Codex | `codex/generated-verification` | Add generated repo verification command | `create` emits instructions and a machine-checkable command for validating generated systems |

## Backlog Rules

- Keep tasks small enough for one Codex PR.
- Every task needs acceptance criteria.
- Prefer CLI, Markdown, and deterministic files before UI.
- Add architecture decisions to `docs/adr/`.
- Move completed items to `done`; do not delete historical tasks.
