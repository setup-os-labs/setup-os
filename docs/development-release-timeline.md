# Development and Release Timeline

This page is a visual guide for understanding where Setup OS is, what remains before it is comfortable as a personal local utility, and what comes later for a public commercial release.

## Current Position

```mermaid
flowchart LR
    A["Foundation\nCLI, docs, monorepo, CI"] --> B["Generated Portfolio OS\nlocal CSV imports, reports, alerts"]
    B --> C["Desktop MVP scaffold\nTauri shell, actions, diagnostics"]
    C --> D["Local utility readiness\nhandoff, release checks, scheduler notes"]
    D --> E["Personal daily use\nlocal install, runtime node, phone alerts"]
    E --> F["Public commercial release\nsigned installers, onboarding, updater"]

    C:::done
    D:::current
    E:::next
    F:::later

    classDef done fill:#dfeee7,stroke:#3b7058,color:#173b2f;
    classDef current fill:#fff2cc,stroke:#8a6d1d,color:#4f3f10;
    classDef next fill:#e5efff,stroke:#4169a8,color:#17365d;
    classDef later fill:#f3f0f7,stroke:#6d5a88,color:#352448;
```

Setup OS is at the **96-97% local-first desktop MVP scaffold** checkpoint. That means the architecture, desktop shell, generated Portfolio OS loop, CI, release notes, local handoff flow, and packaging contracts exist. It does **not** mean the public installer is done.

## Three Timelines

```mermaid
timeline
    title Setup OS Roadmap
    Local Utility
        Done : Python CLI
        Done : Tauri desktop launcher
        Done : Portfolio OS create/import/report loop
        Done : Work, Review, and Operator desktop surfaces
        Done : Runtime node scaffold and scheduler notes
        Done : Generated handoff and desktop handoff review
        Done : Packaged artifact smoke manifest
        Next : Local install smoke test from downloaded app
        Next : Personal always-on runtime node on laptop or Mac mini
    Portfolio Management OS
        Done : Local holdings, transactions, cash, watchlist, market snapshots
        Done : Reports, concentration alerts, allocation drift, memory drafts, handoff
        Next : Import your saved financial conversations
        Next : Better strategy/risk/watchlist extraction
        Later : Robinhood read-only connector and OpenBB/live data
    Public Release
        Done : Unsigned release workflow and native CI
        Done : Signing/notarization plan
        Next : Real signing credentials and notarized builds
        Later : Installer polish, updater, onboarding, support docs
```

## Product Tracks

| Track | Current % | Meaning | Next Blocker |
| --- | ---: | --- | --- |
| Setup OS local desktop MVP scaffold | 97% | The local-first desktop product shape is in place and verified by CI, including packaged artifact smoke manifests. | Manual installed-app smoke test from downloaded artifact. |
| Setup OS as your daily local utility | 88-90% | You can generate, inspect, run, and hand off a Portfolio OS locally. | Installable local app plus runtime-node schedule on your machine or Mac mini. |
| Generated Portfolio Management OS local v0 | 72% | Local data imports, reports, alerts, memory drafts, memory update reports, runtime node, and handoff exist. | Use your saved financial conversations and improve extraction quality. |
| Public commercial release | 35-45% | Architecture, CI, release docs, unsigned builds, and native checks exist. | Signing, notarization, onboarding, updater, and support surface. |

## Local Utility Path

```mermaid
flowchart TD
    A["Build/install local Setup OS desktop app"] --> B["Create Portfolio Management OS from saved conversations"]
    B --> C["Import local portfolio files"]
    C --> D["Run reports and review alerts"]
    D --> E["Write handoff.md readiness checklist"]
    E --> F["Schedule runtime_node.py on laptop or Mac mini"]
    F --> G["Send phone notifications through approved adapter"]
    G --> H["Daily personal use"]

    A:::next
    B:::mostly
    C:::mostly
    D:::mostly
    E:::mostly
    F:::next
    G:::later
    H:::later

    classDef mostly fill:#dfeee7,stroke:#3b7058,color:#173b2f;
    classDef next fill:#fff2cc,stroke:#8a6d1d,color:#4f3f10;
    classDef later fill:#e5efff,stroke:#4169a8,color:#17365d;
```

The local utility is close, but the missing piece is not more architecture. It is the practical install-and-run loop:

- package the app with a real Python sidecar;
- run the packaged app on your machine;
- create Portfolio Management OS from your saved conversations;
- write and review `handoff.md`;
- schedule `runtime_node.py` somewhere always on;
- connect phone notifications in an explicitly approved way.

## Public Release Path

```mermaid
flowchart TD
    A["Internal unsigned builds"] --> B["Sidecar artifacts built in release workflow"]
    B --> C["Windows signing"]
    B --> D["macOS signing and notarization"]
    C --> E["Install smoke tests"]
    D --> E
    E --> F["Onboarding and docs"]
    F --> G["Updater and rollback policy"]
    G --> H["Public commercial release"]

    A:::done
    B:::next
    C:::next
    D:::next
    E:::next
    F:::later
    G:::later
    H:::later

    classDef done fill:#dfeee7,stroke:#3b7058,color:#173b2f;
    classDef next fill:#fff2cc,stroke:#8a6d1d,color:#4f3f10;
    classDef later fill:#f3f0f7,stroke:#6d5a88,color:#352448;
```

The public release is a separate path from your local utility. It needs more polish because other users will not tolerate setup friction, missing credentials, unsigned install warnings, or unclear onboarding.

## Next Milestones

| Milestone | Target | Done When |
| --- | --- | --- |
| Local install loop | Personal use | You can launch the desktop app from an installed artifact without relying on repo dev commands. |
| First-run orientation | Personal use | The desktop app explains the local system loop and keeps work, review, and diagnostics in separate surfaces. |
| Portfolio from your conversations | Personal use | Your saved ChatGPT financial conversations import and produce reviewable strategy/risk/watchlist drafts. |
| Handoff-driven readiness | Personal use | The generated `handoff.md` and desktop dashboard show what is ready and what needs attention. |
| Runtime node in the home setup | Personal use | A laptop, Mac mini, mini PC, or private VPS runs scheduled `runtime_node.py` and logs cycles. |
| Phone notifications | Personal use | Approved alert events can reach your phone without giving broad automation permissions. |
| Public beta package | Commercial release | Windows/macOS artifacts are signed/notarized, documented, and smoke-tested. |

## What To Build Next

1. Packaged local install smoke test on your Windows machine.
2. Import and extract from your real saved Portfolio Management conversations.
3. Personal runtime-node setup guide for your chosen always-on machine.
4. Phone notification adapter decision and first approved channel.
5. Real sidecar artifact assembly in the desktop release workflow.

For the current practical path, use [Personal local setup guide](personal-local-setup.md).

## Current Automated Smoke Test

CI now runs `python scripts/smoke_local_utility.py`, which verifies the local repo path can:

- generate Portfolio Management OS from the bundled planning conversation;
- run generated health and report commands;
- run `runtime_node.py`;
- import a saved conversation example;
- extract structured memory drafts;
- generate a review-only Memory Update Report;
- write `handoff.md`;
- verify the generated report and runtime files exist.

This is not the same as an installed desktop-app smoke test, but it protects the core local utility loop while packaging work continues.

The desktop launcher also exposes this as **Local smoke test**, so you can run the same validation interactively from the app while iterating locally.
