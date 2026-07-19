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

Future generated systems should split memory updates from functional updates:

```text
Raw conversation batch
  -> proposed memory updates
  -> Memory Update Report
  -> human approval
  -> versioned memory update

Raw conversation batch
  -> extractor self-evaluation
  -> Functional Evolution Report
  -> human approval
  -> versioned extractor/schema update
```

The second path is for improving how the system learns, not merely adding more facts.

## Memory Layers

- Raw memory: original conversations and notes. This never directly drives behavior.
- Structured memory: extracted facts, preferences, goals, thresholds, and workflow rules.
- Policy memory: protected action rules such as approval requirements and automation limits.

Policy memory is the most protected layer.

## Functional Evolution Layer

The extraction engine is itself a versioned system component.

It can propose:

- new extractors
- new schema fields
- new comparison dimensions
- new intent-state classifications
- new contradiction checks
- new quality scoring rubrics
- new noise and duplicate filters
- new evidence requirements

It must not activate those changes without approval.

Each functional evolution proposal should include:

- problem observed
- source evidence
- proposed change
- expected benefit
- risk or overfitting concern
- affected schemas, prompts, or generated files
- tests or checks to run
- rollback path

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

Functional evolution proposals should be labeled separately from memory update proposals so the user can approve memory growth without also approving extractor changes.

## Control Pillars

Generated systems that learn from recurring personal data should expose:

- self-evaluation: what the extractor missed, over-extracted, or classified poorly
- observability: counts of inputs, outputs, conflicts, low-confidence drafts, rejected noise, and proposed upgrades
- traceability: source import, checksum, and evidence location for every proposed durable claim
- governance: explicit approval before memory, policy, schema, prompt, maturity, or extractor changes
- versioning: append-only records of approved memory and functional changes
- rollback: a path to undo bad memory or functional updates
- data quality control: duplicate, stale, noisy, conflicting, and low-confidence input handling
- objective alignment: extraction and recommendations should serve the generated system's approved goals

## Timeline

Every generated system should keep an evolution timeline that links changes back to the conversation or proposal that caused them.
