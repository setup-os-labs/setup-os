# Evolution Model

Setup OS treats every future conversation as a proposal, not a direct mutation.

## Pipeline

```text
Raw conversation
  -> extract claims
  -> classify claims
  -> map to schema
  -> detect conflicts
  -> generate evolution proposal
  -> human approval
  -> versioned update
```

The raw conversation can be messy. The generated agent's operating rules must stay structured.

## Memory Layers

- Raw memory: original conversations and notes. This never directly drives behavior.
- Structured memory: extracted facts, preferences, goals, thresholds, and workflow rules.
- Policy memory: protected action rules such as approval requirements and automation limits.

Policy memory is the most protected layer.

## Confidence Gates

- `>= 0.85`: propose normally.
- `0.60` to `0.85`: propose with warning or conflict context.
- `< 0.60`: ask for clarification or park in raw memory.

## Maturity Levels

- Level 0: Draft
- Level 1: Advisory only
- Level 2: Alerts
- Level 3: Human-approved actions
- Level 4: Limited automation
- Level 5: Full automation

New conversations can improve an agent, but they cannot silently jump maturity levels.

## User Language

Do not call this a diff in user-facing surfaces. Use `Evolution Proposal`.

Each proposal should include:

- conversation summary
- suggested changes
- expected impact
- confidence
- risk
- conflicts
- approval requirement

## Timeline

Every generated system should keep an evolution timeline that links changes back to the conversation or proposal that caused them.
