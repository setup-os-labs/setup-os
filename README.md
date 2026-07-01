<p align="center">
  <img src="assets/brand/setup-os-logo.svg" alt="Setup OS" width="760">
</p>

# Setup OS

[![License](https://img.shields.io/github/license/setup-os-labs/setup-os)](LICENSE)
[![CI](https://github.com/setup-os-labs/setup-os/actions/workflows/ci.yml/badge.svg)](https://github.com/setup-os-labs/setup-os/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/setup-os-labs/setup-os?style=social)](https://github.com/setup-os-labs/setup-os/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/setup-os-labs/setup-os?style=social)](https://github.com/setup-os-labs/setup-os/forks)
[![GitHub issues](https://img.shields.io/github/issues/setup-os-labs/setup-os)](https://github.com/setup-os-labs/setup-os/issues)
[![GitHub release](https://img.shields.io/github/v/release/setup-os-labs/setup-os?display_name=tag)](https://github.com/setup-os-labs/setup-os/releases)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![Local first](https://img.shields.io/badge/local--first-default-2ea44f)](docs/architecture-principles.md)

Setup OS turns finalized AI planning conversations into local, self-hosted operating systems.

It is not another agent framework. It is an AI systems architect: it extracts intent from a planning conversation, checks whether existing tools can solve the problem, selects open-source components, proposes an architecture, generates a local repo, and keeps future changes behind reviewable evolution proposals.

Brand assets are in [docs/brand.md](docs/brand.md).

## Product Thesis

```text
Planning conversation
  -> spec completeness check
  -> component discovery
  -> architecture proposal
  -> user approval
  -> local repo generation
  -> running vertical OS
  -> future conversation-driven evolution
```

The first proof vertical is a local Portfolio Manager Agent. It is alert-only in v0: no Robinhood execution, no broker credentials, and no automated trades.

## Open Core Model

The open-source core includes:

- Setup OS CLI
- conversation ingestion
- spec extraction schemas
- architecture proposal generator
- local deployment templates
- blueprint system
- basic notification adapter interfaces
- audit log and evolution proposal flow
- starter vertical blueprints

Future commercial layers may include:

- hosted control plane
- encrypted sync
- managed always-on runners
- mobile app
- template marketplace
- premium vertical packs
- one-click cloud deployment
- team and enterprise governance

See [docs/open-core-strategy.md](docs/open-core-strategy.md).

## v0 Scope

Build one thin end-to-end path:

```text
Markdown/TXT planning conversation
  -> agent_spec.json
  -> architecture.md
  -> generated Portfolio Manager Agent
  -> daily Markdown report
  -> console notification
  -> evolution_proposal.md for future updates
```

Acceptance target:

```bash
python -m setup_os.cli create examples/portfolio_conversation.md
python -m setup_os.cli evolve examples/portfolio_update.md
```

See [docs/roadmap.md](docs/roadmap.md) and [TASKS.md](TASKS.md).

## Repository Layout

The repo is intentionally a monorepo through MVP. Use it for the actual system while the architecture is still evolving; split repos only when a folder becomes a product, API, or community surface of its own.

Current MVP layout:

```text
setup-os/
  .github/                  GitHub issue, PR, and CI configuration
  apps/                     user-facing applications
    desktop/
    web/
    cli/
  packages/                 shared system packages
    core/
    schemas/
    agent-runtime/
    conversation-import/
    blueprint-engine/
    component-registry/
    policy/
  templates/                generated-system templates and blueprints
  docs/                     product, architecture, roadmap, and decisions
  examples/                 example conversations and generated outputs
  research/                 component research and stack-selection notes
  setup_os/                 temporary Python import package for v0 CLI compatibility
  tests/                    future pytest suite
  TASKS.md                  active Codex task queue
  CHANGELOG.md              release history
  CODEX.md                  AI-native development workflow
```

See [ADR 0001](docs/adr/0001-open-core-monorepo.md) for the eventual repo split policy.

## Development Workflow

Use short-lived branches and PRs for every meaningful change.

- Branch format: `codex/<short-task-name>`
- PR size: one task or one coherent vertical slice
- Merge requirement: tests pass, docs updated, changelog updated when user-facing behavior changes
- Architecture changes: add or update an ADR in `docs/adr/`

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODEX.md](CODEX.md).

## License

Apache License 2.0. See [LICENSE](LICENSE).
