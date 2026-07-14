# Desktop UX Philosophy

Setup OS should feel like a calm cockpit for generating and operating local AI systems.

The desktop app is not a marketing page and it is not a raw developer console. It is the place where a user turns a saved planning conversation into a local vertical OS, inspects what the system produced, and approves future changes with confidence.

## North Star

Every primary screen should answer three questions quickly:

1. Where am I?
2. What matters now?
3. What should I do next?

For Setup OS, the first useful loop is:

```text
choose conversation
  -> generate local vertical OS
  -> import local files or saved conversations
  -> review reports, drafts, handoff, and notifications
  -> approve future evolution only after inspection
```

## Surface Model

The desktop shell should separate different mental jobs instead of showing every command at once.

| Surface | Job | Examples |
| --- | --- | --- |
| Work | Create or open a local vertical OS loop. | Create Portfolio OS, preview/import conversation, import CSV files. |
| Review | Inspect evidence before trusting or changing state. | Reports, insights, memory drafts, handoff, notifications. |
| Operator | Debug, validate, reset, and prepare releases. | Runtime details, health, readiness, smoke tests, release checks, logs. |

Work surfaces should be decision-first. Review surfaces should be evidence-first. Operator surfaces can expose mechanics, but they should still be grouped by intent.

## Design Rules

- Put one recommended next action near the top.
- Show the selected workspace before deeper controls.
- Keep CLI output available, but do not make it the first impression.
- Keep diagnostics and release checks outside the daily work path.
- Keep reset/archive actions visually quieter and clearly separated.
- Use plain labels that match local user jobs: create, import, review, handoff, health, runtime.
- Use tabs, panels, and drilldowns to reveal depth only when the user asks for it.
- For AI or extraction outputs, show what was inferred, where evidence came from, and what requires approval.

## Acceptance Check

A new user should be able to understand the desktop app in under 10 seconds:

- This app generates local vertical operating systems from planning conversations.
- Portfolio OS is the current useful vertical.
- The next action is to run or refresh the local Portfolio loop.
- Review and operator details are available without crowding the first layer.

This is the Setup OS version of modern enterprise SaaS UX: calm, local-first, approval-first, and powerful without making the user decode the machinery.
