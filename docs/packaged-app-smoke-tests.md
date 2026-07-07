# Packaged App Smoke Tests

Use this checklist after downloading unsigned or signed desktop artifacts from the release workflow.

Each release artifact should include `packaged-smoke-manifest.json`. Review it before installing the app; it confirms the workflow found a platform bundle artifact and records the manual next steps.

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

## Pass Criteria

- App launches without a terminal.
- Engine check succeeds.
- Release readiness explains any missing signing or sidecar gates.
- Portfolio demo flow creates a generated agent and report.
- Handoff guidance loads from the generated `handoff.md`.
- No broker credentials or external service credentials are requested.
