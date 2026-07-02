# Personal Local Setup Guide

This guide is for using Setup OS as your own local utility before it becomes a public product.

The goal is not a polished commercial installer yet. The goal is a reliable personal loop:

1. run Setup OS desktop locally;
2. create Portfolio Management OS;
3. import saved conversations and local portfolio files;
4. run reports and review alerts;
5. schedule `runtime_node.py` on a machine that stays online;
6. send only approved notifications to your phone.

## Current Best Path

Use the repo/dev build first, because it is the most complete and easiest to debug.

```text
apps/desktop/
  npm.cmd run typecheck
  npm.cmd run build
```

From the desktop app:

1. Run **Check engine**.
2. Run **Runtime details**.
3. Run **Release readiness**.
4. Run **Local smoke test**.
5. Generate Portfolio Management OS.
6. Run the full Portfolio demo flow.
7. Run `python handoff.py` in the generated workspace.
8. Review report, insights, inbox, runtime log, and `handoff.md`.

## Windows Laptop Path

Use this path first on your current Windows machine.

```text
python -m unittest discover -s tests
python scripts/check_desktop_release_contract.py
python scripts/smoke_local_utility.py
cd apps/desktop
npm.cmd run typecheck
npm.cmd run build
```

Then launch the desktop dev app or a locally built artifact and run:

- **Check engine**
- **Runtime details**
- **Release readiness**
- **Local smoke test**
- **Run demo flow**

Passing all five means the local utility path is healthy enough to start importing your own saved Portfolio Management conversations.

## Portfolio Management OS From Your Conversations

Start raw-first.

1. Export or save your ChatGPT financial discussion as Markdown or TXT.
2. In the desktop app, set the **Conversation** path to that file.
3. Run **Preview conversation** to verify the file is readable and looks relevant.
4. Run **Import**.
5. Run **Extract drafts**.
6. Run **Review drafts**.
7. Do not treat extracted drafts as live strategy until reviewed.

The current extraction is intentionally review-only. It should help you organize strategy, risk rules, watchlist items, and constraints before any automation exists.

## Always-On Runtime Node

You eventually need one machine that stays online:

- current Windows laptop;
- Mac mini;
- mini PC;
- NAS-like home server;
- private VPS, if you want off-home reliability.

The first always-on job is simple:

```text
python runtime_node.py
```

or, while testing:

```text
python runtime_node.py --skip-report
```

Run it from the generated Portfolio Management OS directory. It writes:

```text
.setup_os/runtime_node.jsonl
```

Use the desktop app's **Read runtime log** action to inspect cycles.

Then write a one-file local utility checkpoint:

```text
python handoff.py
```

It writes:

```text
handoff.md
```

Use it as the quick answer to "what is ready, what ran, and what should I do next on this machine?"

## Phone Notifications

Do not enable broad automation first.

Recommended path:

1. Keep local notification inbox as the source of truth.
2. Use `ntfy` only for explicitly approved alert events.
3. Do not send broker credentials or raw portfolio files through notifications.
4. Add snooze/done/dismiss behavior before increasing notification volume.

## Done For Personal Utility

Setup OS is personally usable when:

- desktop app launches reliably on your machine;
- **Local smoke test** passes from the desktop;
- Portfolio Management OS is generated from your saved conversations;
- reports and insights are useful enough for daily review;
- `runtime_node.py` runs on an always-on machine;
- `handoff.md` summarizes readiness, runtime cycles, imports, drafts, and next steps;
- phone notifications only carry approved alert summaries.

## Still Not Public-Release Ready

The personal local utility can work before these are done:

- bundled Python sidecar artifacts;
- signed Windows installer;
- signed/notarized macOS app;
- updater and rollback policy;
- onboarding for users who are not you.
