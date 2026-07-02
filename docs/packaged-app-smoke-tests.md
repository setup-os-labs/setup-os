# Packaged App Smoke Tests

Use this checklist after downloading unsigned or signed desktop artifacts from the release workflow.

## Windows

1. Install or extract the Windows artifact.
2. Launch Setup OS.
3. Run **Check engine**.
4. Run **Runtime details** and confirm the Python command is expected.
5. Run **Release readiness**.
6. Generate Portfolio Management OS with the bundled example conversation.
7. Run the full Portfolio demo flow.
8. Review report, insights, inbox, and runtime log.

## macOS

1. Install or open the macOS artifact.
2. Launch Setup OS.
3. Run **Check engine**.
4. Run **Runtime details** and confirm the Python command is expected.
5. Run **Release readiness**.
6. Generate Portfolio Management OS with the bundled example conversation.
7. Run the full Portfolio demo flow.
8. Review report, insights, inbox, and runtime log.

## Pass Criteria

- App launches without a terminal.
- Engine check succeeds.
- Release readiness explains any missing signing or sidecar gates.
- Portfolio demo flow creates a generated agent and report.
- No broker credentials or external service credentials are requested.
