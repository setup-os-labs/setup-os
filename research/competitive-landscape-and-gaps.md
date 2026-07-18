# Competitive Landscape And Gaps

Date: 2026-07-01

Source: `ChatGPT-Setup OS, Portfolio Mngt Agent.md`. Reverify external product details before public launch.

## Supabase Comparison

| Dimension | Supabase | Setup OS |
| --- | --- | --- |
| Category | Backend platform | Agent-system composer |
| Core promise | Start a backend quickly | Turn a planning conversation into a local living agent |
| Main input | Schema, tables, functions, app code | Finalized planning conversation |
| Core abstraction | Database and backend primitives | Vertical agents, memory, notifications, evolution |
| Output | Postgres, auth, APIs, storage, realtime | Portfolio OS (first output), Career OS, Health OS, custom agents — plus optional blueprint templates for future verticals |
| What it composes | Postgres, auth, storage, realtime, functions | LLMs, memory, tools, schedulers, notifications, deployment |
| Source of truth | Postgres | Agent DNA, structured memory, policy memory, timeline |
| Runtime posture | Cloud-first with self-host option | Local-first with optional cloud layers |
| Evolution model | Developer changes app/backend | User approves conversation-derived evolution proposals |
| Marketplace potential | Extensions and templates | Vertical blueprints, capabilities, recipes, connectors |

**Boundary note (2026-07-06):** [Vehicle OS](https://vehicleos.app) is an **independent product** built ground-up — not a Setup OS generated output. Portfolio Management OS is the first factory deliverable. A `vehicle-os` conversation guide exists for future *generated* local agents only.

Clean framing:

```text
Supabase = packaged backend primitives.
Setup OS = packaged agent-system primitives.
```

## Adjacent Products

| Area | Examples | Setup OS stance |
| --- | --- | --- |
| Notification pipe | ntfy, Gotify, UnifiedPush | Use as delivery pipes before building a full Notification OS |
| Notification infrastructure | Apprise, Novu | Use Apprise-like routing first; Novu-style inbox/workflows later |
| App/agent builders | Dify, Flowise, Dyad, Moldable, Local Operator | Learn from them, but stay focused on conversation-to-local-OS plus evolution |
| Automation platforms | n8n, Home Assistant | Useful components, not the Setup OS product itself |
| Coding agents | Codex, Cursor, OpenHands | Can implement pieces; Setup OS owns architecture and lifecycle |
| Connector surface | MCP and ChatGPT connectors | Future interface for vertical agents to expose memory, timeline, and actions |

## Gaps To Cover

| Gap | Setup OS answer |
| --- | --- |
| Action permissions | Trust levels from read-only through auto-execute |
| Runtime health | Generated verifier, scheduler checks, notifier checks |
| Always-on decision | Recommend laptop, mini PC, NAS, VPS, or hybrid based on alert needs |
| Notification overload | Severity, digest, quiet hours, snooze, escalation |
| Source-of-truth conflict | Agent timeline and memory are canonical; calendar mirrors only dated events |
| Rollback | Versioned generated-agent release snapshots |
| Evaluation harness | Behavioral tests before applying approved evolution |
| Privacy tiers | Local-only, local plus metadata, managed cloud |
| License risk | Component decision records and license checks |
| Mission drift | Agent DNA, policy memory, and evolution conflict detection |
