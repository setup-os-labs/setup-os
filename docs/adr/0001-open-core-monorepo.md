# ADR 0001: Open Core Monorepo First

Status: Accepted

Date: 2026-06-30

## Context

Setup OS is early and its core schemas, CLI, generator, blueprints, architecture docs, and first vertical will evolve together.

The project should look and operate like a serious open-core GitHub product, but splitting into many repositories too early would add versioning and coordination overhead.

## Decision

Start with one main monorepo under a future GitHub organization.

Keep these areas in the monorepo for v0:

- core CLI
- schemas
- ingestion
- extraction
- architecture proposal generator
- component registry
- blueprints
- examples
- docs
- tests

Create separate repositories later only when a boundary needs independent versioning, distribution, or community ownership.

Likely future repos:

- `setup-os/docs`
- `setup-os/blueprints`
- `setup-os/skills`
- `setup-os/registry`
- `setup-os/examples`

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
