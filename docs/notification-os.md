# Notification OS

Notification OS is the shared command center for vertical agents created by Setup OS.

## Product Boundary

Setup OS creates and evolves vertical agents.

Notification OS receives events from those agents and owns:

- alerts
- action requests
- snooze, done, and dismiss state
- explanation requests
- calendar mirroring
- notification history

## v0 Boundary

Setup OS v0 only includes a console notification adapter. Full Notification OS is out of scope until the generated-agent pipeline is stable.

## Target Flow

```text
Portfolio Agent
Vehicle Agent
Career Agent
Health Agent
  -> Notification OS
  -> phone alerts
  -> Approve / Snooze / Done / Explain / Add to Calendar / Execute
```

## Calendar Role

Calendar is not the source of truth.

The agent timeline is the source of truth. Calendar mirrors only time-bound events such as appointments, renewal dates, scheduled reviews, and due dates.

## Future Connector Role

Each vertical agent should eventually expose a connector or MCP-style interface so ChatGPT, Claude, or another assistant can ask the agent for memory, timeline, recommendations, and next actions.
