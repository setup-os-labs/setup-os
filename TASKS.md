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
| SO-017 | done | Codex | `codex/evolution-notification-foundation` | Add evolution timeline and richer proposal metadata | `evolve` writes confidence, risk, memory layer, maturity level, and timeline events |
| SO-018 | done | Codex | `codex/evolution-notification-foundation` | Document Notification OS boundary | Docs define Notification OS, calendar mirroring, and connector/MCP direction |

## Later

| ID | Status | Owner | Branch | Task | Acceptance |
| --- | --- | --- | --- | --- | --- |
| SO-012 | done | Codex | `codex/ntfy-adapter` | Add optional ntfy adapter | Adapter is disabled by default and documented |
| SO-013 | done | Codex | `codex/adr-index` | Add ADR index generator or convention | ADRs are easy to discover and link from PRs |
| SO-014 | done | Codex | `codex/docs-site-decision` | Evaluate docs site need | Decision recorded; no site built unless it reduces contributor friction |
| SO-019 | done | Codex | `codex/evolution-notification-foundation` | Add notification event schema and inbox file | Generated agents can emit structured notification events with snooze/done/dismiss states |
| SO-020 | done | Codex | `codex/evolution-notification-foundation` | Add Health OS blueprint detection | Health planning conversation creates a health-oriented spec and architecture proposal |
| SO-021 | done | Codex | `codex/evolution-notification-foundation` | Add agnostic architecture and Agent DNA | Docs define provider-neutral layers; generated portfolio agent includes `agent_dna.json` and quality score |
| SO-022 | done | Codex | `codex/evolution-notification-foundation` | Add capability dependency graph | Portfolio architecture proposal includes capability dependencies and affected surfaces |
| SO-023 | done | Codex | `codex/evolution-notification-foundation` | Add generated-agent release snapshots | Create/evolve can preserve versioned release metadata for future rollback |
| SO-024 | done | Codex | `codex/evolution-notification-foundation` | Add first non-portfolio vertical skeleton | Health OS planning conversation produces a generated health scaffold with local reports and no medical-action automation |
| SO-025 | done | Codex | `codex/evolution-notification-foundation` | Add generated repo verification command | `create` emits instructions and a machine-checkable command for validating generated systems |
| SO-026 | done | Codex | `codex/evolution-notification-foundation` | Add action permission policy primitives | Generated configs include read/alert/draft/approve/execute/auto-execute trust levels and prohibited actions |
| SO-027 | done | Codex | `codex/evolution-notification-foundation` | Add explicit approve/apply command for safe evolution | Approved proposal can create a candidate release without mutating the current release silently |
| SO-028 | done | Codex | `codex/runtime-health` | Add generated runtime health checks | Generated systems can check scheduler, notifications, required files, and configuration health |
| SO-029 | done | Codex | `codex/evolution-notification-foundation` | Document desktop stack and Portfolio Management OS blueprint | README, ADR, docs, and templates explain Python core, future Tauri desktop, optional FastAPI, and Portfolio Management OS scope |
| SO-030 | done | Codex | `codex/desktop-shell-foundation` | Spike cross-platform desktop shell | Minimal Tauri vertical-agent launcher can call `python -m setup_os.cli --help` on native macOS and Windows |
| SO-031 | done | Codex | `codex/evolution-notification-foundation` | Capture desktop-first and Robinhood read-only decisions | ADR and Portfolio Management OS docs record desktop-first sequencing, Tauri rationale, process mode decision rule, native Windows target, and Robinhood read-only import direction |
| SO-032 | done | Codex | `codex/desktop-shell-spike` | Add Portfolio Management OS building-block research | Research note ranks stack options, captures rejected alternatives, and links from Portfolio Management OS docs |
| SO-033 | done | Codex | `codex/desktop-ci-checks` | Add desktop frontend checks to CI | GitHub Actions runs desktop npm ci, typecheck, build, and audit without requiring native Tauri packaging |
| SO-034 | done | Codex | `codex/tauri-native-ci-and-branches` | Add native Tauri CI validation and branch retention rule | CI compiles the desktop native shell without bundling, and Codex workflow says not to delete remote branches after merge |
| SO-035 | done | Codex | `codex/branch-history-policy` | Document retained branch history policy | CODEX explains archival/restored branch handling and identifies `codex/setup-os-brand` as superseded history |
| SO-036 | done | Codex | `codex/diagram-output-pack` | Add standard generated diagram pack | Generated systems include offline HTML diagrams, editable D2 source, local icons, manifest, docs, and tests |
| SO-037 | done | Codex | `codex/ci-speedups` | Speed up CI feedback | CI splits Python, desktop frontend, and native Tauri checks into parallel jobs while preserving the protected `checks` aggregate |
| SO-038 | done | Codex | `codex/raw-conversation-import` | Add raw conversation import to generated agents | Generated agents include `import_conversation.py`, store saved chats in `memory/raw`, append manifest metadata, and avoid strategy mutation |
| SO-039 | done | Codex | `codex/structured-memory-drafts` | Add structured memory extraction drafts | Generated agents include `extract_memory.py` that converts raw imports into review-only `memory/structured` drafts without mutating strategy or policy |
| SO-040 | done | Codex | `codex/portfolio-concentration-alerts` | Add Portfolio concentration warning reports | Generated Portfolio Manager daily reports warn when a single holding is above the local review threshold and emit a warning notification |
| SO-041 | done | Codex | `codex/portfolio-snapshot-import` | Add read-only portfolio snapshot import | Generated Portfolio Manager agents can import validated local holdings CSV snapshots, write an import manifest, and avoid storing broker credentials |
| SO-042 | done | Codex | `codex/portfolio-allocation-drift` | Add Portfolio allocation drift warnings | Generated Portfolio Manager reports compare holdings to local target weights and warn when drift exceeds the review band |
| SO-043 | done | Codex | `codex/portfolio-transaction-import` | Add read-only portfolio transaction import | Generated Portfolio Manager agents can import validated local transaction CSV snapshots, write an import manifest, and show recent transactions in reports |
| SO-044 | done | Codex | `codex/portfolio-cash-import` | Add read-only portfolio cash import | Generated Portfolio Manager agents can import validated local cash CSV snapshots, write an import manifest, and include cash in reports |
| SO-045 | done | Codex | `codex/portfolio-watchlist-import` | Add read-only portfolio watchlist import | Generated Portfolio Manager agents can import validated local watchlist CSV snapshots, write an import manifest, and show watchlist notes in reports |
| SO-046 | done | Codex | `codex/portfolio-market-snapshot` | Add read-only market snapshot import | Generated Portfolio Manager agents can import validated local market data CSV snapshots, write an import manifest, and use snapshot prices/events in reports |
| SO-047 | done | Codex | `codex/portfolio-performance-summary` | Add offline portfolio performance summary | Generated Portfolio Manager reports include holdings cost basis, unrealized gain/loss, and per-holding return using local snapshot prices when present |
| SO-048 | done | Codex | `codex/desktop-create-portfolio-action` | Add desktop Portfolio OS create action | Desktop shell can invoke the Python CLI to generate the Portfolio Management OS example into `generated/desktop-portfolio-os` |
| SO-049 | done | Codex | `codex/desktop-run-portfolio-report` | Add desktop Portfolio OS report action | Desktop shell can run the generated Portfolio Management OS report and display the Markdown output |
| SO-050 | done | Codex | `codex/desktop-portfolio-health-action` | Add desktop Portfolio OS health action | Desktop shell can run the generated Portfolio Management OS health check and display the output |
| SO-051 | done | Codex | `codex/desktop-import-conversation-action` | Add desktop raw conversation import action | Desktop shell can import an example saved Portfolio conversation into the generated agent raw memory |
| SO-052 | done | Codex | `codex/desktop-extract-memory-action` | Add desktop structured memory draft action | Desktop shell can run generated Portfolio memory extraction and display the review-only draft output |
| SO-053 | done | Codex | `codex/desktop-portfolio-status-action` | Add desktop generated Portfolio status action | Desktop shell can display which generated Portfolio artifacts exist without mutating files |
| SO-054 | done | Codex | `codex/desktop-import-path-input` | Add desktop conversation path input | Desktop shell can import a user-entered saved Portfolio conversation path instead of only the bundled example |
| SO-055 | done | Codex | `codex/desktop-portfolio-data-imports` | Add desktop Portfolio CSV import actions | Desktop shell can import holdings, transactions, cash, watchlist, and market snapshot CSV files into the generated Portfolio OS |
| SO-056 | done | Codex | `codex/desktop-portfolio-full-flow` | Add desktop Portfolio demo flow | Desktop shell can run the full local Portfolio OS demo loop from create through report and status |
| SO-057 | done | Codex | `codex/cross-platform-native-ci` | Add cross-platform native desktop CI | GitHub Actions compiles the Tauri desktop shell on Linux, Windows, and macOS without producing installers |
| SO-058 | done | Codex | `codex/desktop-release-workflow` | Add manual desktop release workflow | GitHub Actions can manually build unsigned Linux, Windows, and macOS Tauri bundle artifacts for release testing |
| SO-059 | done | Codex | `codex/fix-desktop-release-icons` | Fix desktop release bundle icons | Manual release workflow can package Linux AppImage and Windows MSI artifacts with configured Tauri icon assets |
| SO-060 | done | Codex | `codex/fix-macos-release-icon` | Fix macOS desktop release icon conversion | Manual release workflow can package macOS app artifacts with an ICO asset whose directory metadata matches its embedded PNG |
| SO-061 | done | Codex | `codex/verify-desktop-release-workflow` | Verify desktop release workflow artifacts | Manual release workflow run `28546192396` passed on Linux, Windows, and macOS and uploaded unsigned desktop artifacts |
| SO-062 | done | Codex | `codex/desktop-portfolio-output-path` | Add editable desktop Portfolio output path | Desktop Portfolio actions can target a user-entered generated-agent directory instead of only `generated/desktop-portfolio-os` |
| SO-063 | done | Codex | `codex/desktop-path-persistence` | Persist desktop Portfolio paths | Desktop shell remembers Portfolio output, conversation, and CSV import paths between sessions |
| SO-064 | done | Codex | `codex/desktop-create-seed-path` | Add desktop seed conversation path | Desktop Portfolio create action can generate from a user-entered seed planning conversation instead of only the bundled example |
| SO-065 | done | Codex | `codex/desktop-portfolio-inbox` | Add desktop Portfolio notification inbox reader | Desktop shell can display generated Portfolio notification inbox events from `.setup_os/notifications.jsonl` |
| SO-066 | done | Codex | `codex/product-status-checkpoint` | Add product status checkpoint | Repo documents current completion estimate, usable surfaces, and the remaining desktop MVP slices needed to reach 75% |
| SO-067 | done | Codex | `codex/desktop-readiness-checks` | Add desktop readiness checks | Desktop shell can check repo root, Python engine, seed conversation, and selected Portfolio workspace with next-step guidance |
| SO-068 | done | Codex | `codex/desktop-action-validation` | Add desktop action validation | Desktop shell validates required output, seed, conversation, and import paths before invoking backend commands |
| SO-069 | done | Codex | `codex/desktop-memory-draft-review` | Add desktop memory draft review | Desktop shell can display generated Portfolio structured memory draft JSONL files with next-step guidance when missing |
| SO-070 | done | Codex | `codex/desktop-portfolio-summary` | Add desktop Portfolio summary | Desktop shell can summarize selected Portfolio workspace state, latest report preview, notifications, and structured memory drafts |
| SO-071 | done | Codex | `codex/desktop-reset-recreate-flow` | Add desktop Portfolio reset/recreate flow | Desktop shell can archive the selected generated Portfolio workspace and recreate it from the selected seed conversation |
| SO-072 | done | Codex | `codex/desktop-readable-memory-drafts` | Add readable desktop memory draft review | Desktop shell formats structured Portfolio memory drafts into source, status, confidence, strategy, risk, and watchlist review sections |
| SO-073 | done | Codex | `codex/desktop-report-sections` | Add desktop Portfolio report section review | Desktop shell can display generated Portfolio daily reports grouped by Markdown section headings |
| SO-074 | done | Codex | `codex/desktop-release-test-notes` | Add desktop release testing notes | Docs explain how to run the manual release workflow and validate unsigned Linux, Windows, and macOS artifacts |
| SO-075 | review | Codex | `codex/personal-runtime-node-adr` | Add personal runtime node architecture decision | ADR and docs define the always-on personal node for schedulers, generated agents, and phone notification dispatch |

## Backlog Rules

- Keep tasks small enough for one Codex PR.
- Every task needs acceptance criteria.
- Prefer CLI, Markdown, and deterministic files before UI.
- Add architecture decisions to `docs/adr/`.
- Move completed items to `done`; do not delete historical tasks.
