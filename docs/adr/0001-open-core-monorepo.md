# ADR 0001: Open Core Monorepo First

Status: Accepted

Date: 2026-06-30

## Context

Setup OS is early and its core schemas, CLI, generator, blueprints, architecture docs, and first vertical will evolve together.

The project should look and operate like a serious open-core GitHub product, but splitting into many repositories too early would add versioning and coordination overhead.

## Decision

Start with one main monorepo under the GitHub organization.

Use the monorepo for the actual system while the architecture is still evolving. Keep everything in the monorepo through MVP.

Target layout:

```text
setup-os/
  apps/
    desktop/
    web/
    cli/
  packages/
    core/
    schemas/
    agent-runtime/
    conversation-import/
    blueprint-engine/
    component-registry/
    policy/
  templates/
  docs/
  examples/
  research/
```

Split repositories only when a folder becomes a product, API, or community surface of its own.

Likely eventual split points:

- `setup-os` for the main product and orchestration surface
- `setup-os-core` or `core` for stable SDK/runtime APIs
- `setup-os-schemas` for versioned public schemas
- `setup-os-agent-runtime` for reusable agent execution primitives
- `setup-os-conversation-import` for import adapters
- `setup-os-blueprint-engine` for generation tooling
- `setup-os-component-registry` for OSS discovery and scoring metadata
- `setup-os-policy` for reusable policy/risk gates
- `setup-os-templates` for blueprints and starter systems
- `setup-os-docs` if documentation becomes a standalone publishing surface
- `setup-os-examples` if examples need independent community contribution flow

## Consequences

Benefits:

- faster v0 iteration
- simpler Codex task execution
- easier cross-cutting changes
- one source of truth for docs and tasks

Costs:

- repo can become noisy
- release boundaries need discipline
- future extraction work may be needed
