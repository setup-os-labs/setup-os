# ADR 0007: Self-Evolving Extraction Engine

Status: Accepted

Date: 2026-07-13

## Context

Setup OS already treats future conversations as reviewable evolution proposals instead of direct mutations. The Portfolio Management OS path also imports saved conversations into raw memory and produces review-only structured memory drafts.

The next product direction is stronger than memory growth. Generated systems should not only learn more facts, preferences, watchlists, open loops, and policies. They should also learn how to extract, compare, classify, evaluate, and govern future information better.

For personal finance this matters because extracted memories can shape future financial recommendations. A bad extractor can confuse curiosity with intent, turn a rejected idea into an active preference, miss tax or risk context, or silently overfit to a temporary market condition.

## Decision

Make self-evolving extraction a first-class future architecture pillar for Setup OS and generated systems.

Every generated system that ingests recurring personal conversations should eventually separate two update paths:

```text
Raw inputs
  -> memory extraction
  -> proposed memory updates
  -> human approval
  -> versioned memory update

Raw inputs
  -> extractor self-evaluation
  -> proposed functional upgrades
  -> human approval
  -> versioned extractor or schema update
```

The extraction engine must not rewrite itself silently. It can propose changes to its own schemas, classifiers, prompts, checks, and scoring rubrics, but those changes require explicit approval before becoming active.

## Control Pillars

Self-evolving systems need these control pillars:

- Self-evaluation: judge extraction quality, missed signals, over-extraction, weak classifications, and recurring gaps.
- Observability: show what the pipeline processed, produced, rejected, warned about, and proposed.
- Traceability: link extracted memories and functional upgrade proposals back to source conversation evidence.
- Self-evolution governance: require approval before changing extraction behavior, schemas, prompts, policies, or maturity level.
- Versioning: record every approved memory, policy, schema, prompt, and extractor change.
- Rollback: preserve enough state to revert bad memory or functional updates.
- Data quality control: detect duplicates, stale facts, noisy chat exports, conflicts, and low-confidence claims.
- Objective alignment: keep each generated system pointed at its approved goals instead of optimizing random recurring topics.

## Product Rules

Future implementation should follow these rules:

- A memory update report and a functional evolution report are separate artifacts.
- Functional changes should describe the problem, proposed upgrade, expected benefit, risk, source evidence, and rollback path.
- The system should classify user intent states such as curiosity, serious consideration, rejected, approved, and active behavior.
- Financial systems should default to after-tax, risk-aware, liquidity-aware comparison when those dimensions are relevant.
- High-risk domains such as finance and health must keep functional self-evolution behind human approval.
- Observability summaries should be understandable from the desktop app before any approval action.
- Traceability should be source-first: every durable claim should cite the raw import, checksum, and relevant excerpt or location.
- Rollback should be designed before limited automation is enabled.

## Portfolio Management OS Direction

Portfolio Management OS should become the first proof vertical for this architecture.

Future weekly runs should be able to produce:

- Wealth OS Memory Update Report: new facts, preferences, decisions, open loops, risk rules, tax notes, and watchlist changes.
- Wealth OS Functional Evolution Report: recommended extractors, schema fields, comparison dimensions, contradiction checks, scoring rubrics, and noise filters.
- Pipeline Observability Summary: chats processed, drafts created, low-confidence items, conflicts, rejected noise, and proposed upgrades.
- Evidence Map: source links from each proposed memory or functional change back to imported conversation records.

Example functional upgrades include:

- Cash Yield Optimization Extractor for HYSA, SGOV, T-bills, tax drag, yield, liquidity, and after-tax delta.
- Speculative Trading Risk Gate for options, agentic trading, max loss, backtesting, tax impact, and approved bucket size.
- AI Bottleneck Thesis Tracker for compute, memory bandwidth, networking, power, cooling, photonics, inference, and data center exposure.
- Intent-State Classifier to prevent exploratory questions from becoming active preferences.
- Contradiction Checker for conflicts between old rules, new claims, and current portfolio behavior.

## Consequences

Benefits:

- turns recurring chat exports into compounding personal intelligence instead of static summaries
- keeps extractor improvement explicit, reviewable, and reversible
- reduces memory poisoning and preference drift
- gives the user a debuggable pipeline before trusting higher-stakes advice
- creates a reusable pattern for future Career OS, Health OS, Learning OS, and other verticals

Costs:

- more generated artifacts to review
- more schema and version management
- more desktop UX work for evidence, approval, and rollback
- additional testing needed to prove that self-evaluation and functional proposals do not overfit noisy inputs

## Non-Goals

- autonomous financial execution
- silent extractor rewrites
- storing broker credentials
- treating raw chat exports as trusted memory
- building a vector database or agent framework before the file-based approval loop is proven
