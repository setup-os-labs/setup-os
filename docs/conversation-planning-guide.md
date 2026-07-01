# Conversation Planning Guide

Setup OS should let users think naturally first, then make missing decisions explicit only when needed.

## Core Loop

```text
Think -> Build -> Evolve
```

- Think: the user talks through a vertical in ChatGPT, Claude, Codex, or another assistant.
- Build: Setup OS turns the finalized conversation into a local generated system.
- Evolve: future conversations produce reviewable diffs before the live system changes.

## Bare Minimum Input

Level 0 input is only a finalized planning conversation.

When confidence is low, Setup OS should ask the smallest useful set of missing questions instead of forcing a long intake form up front.

Common missing decisions:

- runtime device: laptop, always-on mini PC, private server, or hybrid
- privacy mode: local-only or local plus selected cloud services
- alert channel: console, email, ntfy, Telegram, mobile app, or none
- action model: advisory, approval-required, limited autonomy, or full autonomy
- data sources and import format
- fallback behavior when the system is offline
- approval rules for external, financial, irreversible, or sensitive actions

## Bare Minimum Output

The first successful build should produce:

- working project
- runnable local command
- sample/local data path
- README
- evolution enabled

Notifications, schedulers, dashboards, and broker/service connectors can be layered in only when the spec requires them.

## Mandatory Setup OS Questions

Before building, Setup OS should answer:

```text
Can an existing product solve this?
Can existing open-source components solve this?
Can they be composed?
What is the smallest missing layer?
What must remain human-approved?
```

The user should not need to know this framework. Setup OS enforces it as part of the architecture proposal.

## Roles

Planning Copilot and Setup Agent are separate roles.

- Planning Copilot helps the user articulate goals, constraints, devices, privacy needs, action models, and existing products to check.
- Setup Agent takes the finalized spec and builds a local system.

Do not merge these too early.

```text
Planning Copilot = think clearly
Setup Agent = build reliably
```
