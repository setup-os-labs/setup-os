# ADR 0003: Human Approval First

Status: Accepted

Date: 2026-06-30

## Context

Setup OS generates local systems from conversations and later evolves them from new conversations. That creates risk if changes are applied automatically.

## Decision

Creation and evolution must produce reviewable artifacts before applying meaningful changes.

For v0:

- initial creation generates architecture and agent files
- evolution generates `evolution_proposal.md`
- evolution does not mutate generated agents directly
- audit logs record create and evolve actions

## Consequences

Benefits:

- safer iteration
- clearer user trust
- easier debugging
- better PR and Codex review flow

Costs:

- more explicit approval steps
- less magical than full autonomy
