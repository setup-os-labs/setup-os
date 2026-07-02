# Desktop Signing and Notarization

Setup OS can produce unsigned desktop artifacts today. Public desktop releases need signing and notarization so Windows and macOS users can install the app without frightening security prompts.

## Current Decision

- Development builds stay unsigned.
- Internal test artifacts can remain unsigned while the desktop MVP is still changing quickly.
- Public releases require signed Windows installers and signed/notarized macOS apps.
- Linux artifacts can remain unsigned initially, with checksums and release provenance documented.

## Windows Release Requirements

- Code-signing certificate owned by the Setup OS project or organization.
- Signed MSI or installer artifact from the Tauri release workflow.
- Release notes that include artifact hashes.
- Smoke check: install, launch, run engine check, run release readiness check.

## macOS Release Requirements

- Apple Developer account.
- Developer ID Application certificate.
- Notarization credentials configured as GitHub Actions secrets.
- Signed and notarized `.app` or `.dmg` artifact from the Tauri release workflow.
- Smoke check: install, launch, run engine check, run release readiness check.

## GitHub Secrets

Do not add real secrets to the repo. The future release workflow should expect:

- `APPLE_ID`
- `APPLE_PASSWORD`
- `APPLE_TEAM_ID`
- `APPLE_CERTIFICATE`
- `APPLE_CERTIFICATE_PASSWORD`
- `WINDOWS_CERTIFICATE`
- `WINDOWS_CERTIFICATE_PASSWORD`

Exact secret names can change when the release workflow is implemented, but they must be documented in the workflow and release checklist.

## Release Gate

A public release is not ready until:

- bundled Python sidecar works without local Python;
- Windows artifact is signed;
- macOS artifact is signed and notarized;
- generated app artifacts pass smoke checks;
- checksums are published;
- rollback/reissue process is documented.
