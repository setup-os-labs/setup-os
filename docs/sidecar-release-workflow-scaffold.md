# Sidecar Release Workflow Scaffold

This note defines the future release workflow shape for bundled Python without committing runtime binaries to the repository.

## Intended Flow

1. Build or download a platform-specific Python runtime during the release workflow.
2. Copy the runtime into `apps/desktop/src-tauri/sidecar/python/`.
3. Copy the `setup_os` Python package into the sidecar payload.
4. Run a sidecar smoke check equivalent to:

   ```text
   <sidecar-python> -m setup_os.cli --help
   ```

5. Build the Tauri bundle.
6. Upload unsigned artifacts for internal testing.
7. Later: sign Windows artifacts and sign/notarize macOS artifacts.

## Repository Rule

Do not commit large Python runtime binaries directly. The workflow should create sidecar contents during release builds and upload packaged artifacts.

## Future CI Gate

The release workflow should fail if:

- the sidecar Python executable is missing;
- `python -m setup_os.cli --help` fails from the sidecar;
- generated app smoke tests cannot run;
- signing/notarization secrets are expected but missing for a public release.
