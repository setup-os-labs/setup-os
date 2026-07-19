# Packaged App Smoke Tests

Use this checklist after downloading unsigned or signed desktop artifacts from the release workflow.

Each release artifact should include `packaged-smoke-manifest.json`. Review it before installing the app; it confirms the workflow found a platform bundle artifact and records the manual next steps.

Before installing, prepare a local evidence file:

```text
python scripts/prepare_installed_app_smoke_evidence.py path/to/packaged-smoke-manifest.json --platform windows --commit <commit-under-test>
```

The generated file is written under `release-evidence/`, which is intentionally ignored by git. Use it to capture screenshots, copied output, pass/fail notes, and follow-up tasks.

## Windows

1. Install or extract the Windows artifact.
2. Confirm `packaged-smoke-manifest.json` lists a `.msi` or `.exe`.
3. Launch Setup OS.
4. Run **Check engine**.
5. Run **Runtime details** and confirm the Python command is expected.
6. Run **Release readiness**.
7. Generate Portfolio Management OS with the bundled example conversation.
8. Run the full Portfolio demo flow.
9. Review report, insights, inbox, runtime log, and handoff guidance.
10. Review Memory Update Report, Functional Evolution Report, Evolution Review Packet, and extractor rollback readiness.
11. Fill in the local installed-app smoke evidence file.

## macOS

1. Install or open the macOS artifact.
2. Confirm `packaged-smoke-manifest.json` lists a `.dmg` or `.app`.
3. Launch Setup OS.
4. Run **Check engine**.
5. Run **Runtime details** and confirm the Python command is expected.
6. Run **Release readiness**.
7. Generate Portfolio Management OS with the bundled example conversation.
8. Run the full Portfolio demo flow.
9. Review report, insights, inbox, runtime log, and handoff guidance.
10. Review Memory Update Report, Functional Evolution Report, Evolution Review Packet, and extractor rollback readiness.
11. Fill in the local installed-app smoke evidence file.

## Pass Criteria

- App launches without a terminal.
- Engine check succeeds.
- Release readiness explains any missing signing or sidecar gates.
- Portfolio demo flow creates a generated agent and report.
- Handoff guidance loads from the generated `handoff.md`.
- Self-evolving review surfaces stay review-only and understandable.
- No broker credentials or external service credentials are requested.
