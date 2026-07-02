# ADR 0006: Personal Runtime Node And Always-On Notifications

Status: Accepted

Date: 2026-07-02

## Context

Setup OS is a local systems composer, not a high-scale distributed backend during MVP.

The desktop app is the right place for setup, imports, review, approvals, and dashboards. Some generated systems, however, need to keep running after the desktop app is closed. Portfolio Management OS, Notification OS, schedulers, watchers, and alert dispatch may need an always-on machine with internet access so the user can receive phone notifications.

The expected early owner deployment is a personal always-on machine such as a Mac mini, laptop, NAS, mini PC, or private VPS.

## Decision

Keep Setup OS as a modular local monolith during MVP, but design for a future process split:

```text
Setup OS Desktop
  Tauri app for setup, review, imports, approvals, and dashboards

Setup OS Engine
  Python composer/generator used by desktop and CLI

Setup OS Runtime Node
  always-on local or private machine for scheduled jobs and watchers

Notification OS
  local inbox and dispatch manager for phone alerts, snooze, done, dismiss, and explain flows

Vertical Agents
  generated systems such as Portfolio Management OS and Health OS

Optional Cloud Relay
  push delivery, remote access, encrypted sync, or backups when local-only operation is not enough
```

The first scalability target is personal-scale reliability:

- scheduled jobs run when the desktop app is closed
- notifications can reach the phone
- generated agents have durable local state
- failures are visible and recoverable
- risky actions remain approval-gated

Do not introduce web-scale microservices before the process boundaries and runtime responsibilities are stable.

## Deployment Targets

### Desktop App

Runs on macOS, Windows, or Linux.

Responsibilities:

- create and evolve generated systems
- import saved conversations
- review memory drafts
- review reports and notifications
- approve candidate changes

### Python Engine

Runs locally as a CLI subprocess during development and as a bundled sidecar for desktop releases.

Responsibilities:

- conversation ingestion
- spec extraction
- blueprint generation
- architecture proposal generation
- evolution proposal generation
- local file and JSONL state handling

FastAPI remains optional until the desktop shell or runtime node needs a long-running local API, streaming progress, concurrent requests, or shared indexed state.

### Personal Runtime Node

Runs on a Mac mini, home server, NAS, spare laptop, mini PC, or private VPS.

Responsibilities:

- scheduled generated-agent jobs
- watchers
- recurring reports
- notification dispatch
- health checks
- local runtime logs

This should start as a local process/daemon model, not a network of microservices.

### Notification OS

Starts as a local JSONL inbox plus optional disabled-by-default push adapters such as ntfy.

Responsibilities:

- receive generated-agent events
- dispatch phone alerts
- track snooze, done, dismiss, and explain state
- mirror time-bound events to calendar later

Notification OS may become a separate service once multiple generated agents need the same always-on inbox and dispatch layer.

### Optional Cloud Relay

Use only when local-first operation cannot satisfy the need.

Possible responsibilities:

- mobile push delivery
- encrypted remote access
- encrypted sync
- backups
- hosted component registry
- team or enterprise control plane

## Split Rules

Split by stable responsibility, not by interview-style microservice instinct.

Likely process/service candidates:

- desktop app
- Python engine
- runtime scheduler
- Notification OS
- connector isolation for Robinhood/OpenBB/broker integrations
- hosted component registry
- optional cloud relay

Keep these in the monorepo until APIs, deployment contracts, and ownership boundaries are stable.

## Consequences

Benefits:

- supports local-first MVP development
- gives the user an always-on path for phone notifications
- avoids premature distributed-system complexity
- keeps approval and privacy boundaries explicit
- leaves room for private cloud or hosted expansion later

Costs:

- runtime-node install and monitoring need product design
- local networking and phone notification delivery need clear setup flows
- future package/service boundaries must be kept clean enough to extract
- desktop and runtime node state synchronization will need a policy before multi-device use
