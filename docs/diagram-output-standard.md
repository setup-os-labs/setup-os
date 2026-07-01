# Diagram Output Standard

Setup OS should generate a small architecture diagram pack for every vertical OS it creates.

The goal is not decorative documentation. The diagrams should help the user understand:

- what the generated OS does
- what gets installed and wired together
- how the system can mature safely over time

## Standard Diagram Pack

Every generated vertical OS should include these three diagrams.

### 1. Overview Orchestration

Purpose: give the user the big-picture mental model in one glance.

This diagram should answer:

- What is the main input?
- What does Setup OS turn it into?
- Where does strategy memory live?
- What runtime coordinates the system?
- What does the user actually receive?

Use this when the user asks: "What did Setup OS build for me?"

### 2. Runtime Architecture

Purpose: show what Setup OS wires together locally.

This diagram should answer:

- What components are running?
- Which pieces are replaceable adapters?
- Where does data enter?
- Where do alerts, reports, and actions leave?
- Where are the safety checks?

Use this when the user asks: "How does this thing work under the hood?"

### 3. Evolution / Safety Flow

Purpose: build trust in how the OS matures from future conversations.

The standard flow is:

```text
New chat export
  -> extract facts, goals, constraints, preferences
  -> compare against current strategy
  -> produce strategy diff
  -> run safety checks
  -> ask human approval
  -> write versioned release
  -> runtime uses new version
  -> results feed the next conversation
```

Use this when the user asks: "Can I trust this agent to evolve?"

## Design Requirements

The diagrams should be:

- hand-drawn / sketch style
- readable before they are complete
- generated as both editable D2 and browser-viewable HTML/SVG
- local-first, with all icon assets copied into the generated output folder
- light on text, with details split across the three diagrams
- consistent across all verticals

Do not cram every component into the Overview diagram. The Overview is for trust and orientation. The Runtime Architecture is for implementation confidence. The Evolution / Safety Flow is for maturity and governance.

## Generator Acceptance Criteria

The Setup OS generator is complete for diagram output when:

- it creates all three standard diagrams
- each diagram has a distinct purpose
- each HTML diagram can be opened locally with `file://`
- icons render without internet access
- the D2 source references local icon files
- no diagram requires external scripts or remote assets
- the Overview has no more than five major visual groups
- the Runtime Architecture shows adapters and safety gates
- the Evolution / Safety Flow shows approval before strategy mutation
