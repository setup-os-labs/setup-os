# Architecture Principles

## 1. Compose Before Build

Before writing custom code, Setup OS should ask:

```text
Can an existing product solve this?
Can existing open-source components solve this?
Can they be composed?
What is the smallest missing layer?
```

## 2. Architecture Is The Product

Setup OS should preserve architecture as a durable artifact:

- extracted intent
- capability model
- selected components
- alternatives considered
- deployment plan
- approval gates
- evolution history

## 3. UI Is The Last Resort

Prefer:

1. notifications
2. chat
3. CLI
4. Markdown reports
5. simple dashboard
6. interactive UI

Build UI only when it reduces cognitive load.

## 4. Humans Approve Architecture

AI proposes. Humans approve.

Creation and evolution should both produce reviewable artifacts before changes are applied.

## 5. Progressive Complexity

Beginner users should see outcomes and missing decisions.

Advanced users can inspect architecture graphs, component tradeoffs, and policy details.

## 6. Justify Dependencies

Every dependency should include:

- why it is selected
- alternatives considered
- why alternatives were rejected
- license and operational notes

## 7. Generated Agents Own Their UX

Setup OS generates and evolves vertical systems. The generated system owns its runtime UX.

## 8. Evolution Is Proposal-Based

Raw conversations do not directly mutate generated agents.

Future conversations should produce schema-constrained, confidence-scored, conflict-aware evolution proposals that the user can approve, reject, or revise.

## 9. Timelines Are Source Of Truth

Generated agents should preserve an append-only timeline for created systems, proposed changes, approvals, and future runtime events.

Calendars and notifications can mirror timeline events, but they are not the canonical memory.

## 10. Action Permissions Are Graduated

Actions should move through explicit trust levels:

```text
read -> alert -> draft -> approve -> execute -> auto_execute
```

High-risk domains such as finance and health should start at `alert` and prohibit dangerous automation by default.

## 11. Extraction Engines Must Evolve Under Control

Generated systems should separate memory evolution from functional evolution.

Memory evolution changes what the system knows. Functional evolution changes how the system extracts, classifies, compares, evaluates, and governs future inputs.

Functional evolution requires:

- self-evaluation of extraction quality and missed patterns
- observability summaries for each pipeline run
- traceability from every durable claim back to source evidence
- human approval before changing extractors, schemas, prompts, checks, or scoring rubrics
- versioning and rollback for approved changes
- objective alignment so the system keeps optimizing for the user's approved goals
