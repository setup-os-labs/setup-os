# 0008: Local-First Observability

## Status

Accepted

## Context

Setup OS runs local workflows that generate files, import private data, draft memory updates, and propose future evolution. Users need to know what happened without reading source code, opening developer consoles, or installing an observability stack.

The desktop app also launches short Python subprocesses. On Windows, those subprocesses must not flash console windows during normal use.

## Decision

Use local-first observability as the default:

- Desktop actions write a readable Markdown action log and a structured JSONL event log under the user's local app data directory.
- Generated systems keep their own local audit, timeline, runtime, notification, memory, evolution, and handoff artifacts.
- The desktop app exposes recent action logs inside the Operator/Inbox surface using plain language.
- Windows desktop subprocesses run without visible console windows.
- External observability tools are adapter targets, not required desktop dependencies.

## OSS Tool Direction

Do not require Grafana, Loki, Prometheus, OpenTelemetry collectors, Docker, or Kubernetes for ordinary desktop users.

Add optional exports later:

- OpenTelemetry spans/events for cloud runners and enterprise deployments.
- Loki-compatible log shipping for self-hosted operators.
- Prometheus metrics for managed runners, not local desktop-only use.
- Diagnostic bundles for support, using the same local Markdown and JSONL source files.

## Consequences

- A normal user can answer "what happened?" from inside the app.
- Support/debugging can start from readable local files.
- Cloud and enterprise observability can reuse the same event model later.
- Desktop remains usable without Docker or external services.

## Non-Goals

- No always-on local observability server in the desktop app.
- No mandatory Docker runtime for local users.
- No automatic upload of private logs to cloud services.
- No hidden promotion of memory, policy, strategy, extractor behavior, or actions based on logs alone.
