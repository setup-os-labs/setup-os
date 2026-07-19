# Python Sidecar Packaging

Setup OS keeps the Python engine as the product core. The desktop app should eventually ship that engine as a bundled sidecar so end users do not need to install Python before using Setup OS.

## Current Decision

- Development builds can use the local `python` executable or `SETUP_OS_PYTHON`.
- Release builds bundle the `setup_os` package and example inputs as desktop resources under `engine/`.
- Release builds should prefer a bundled Python sidecar once the runtime packaging step lands.
- The desktop app should keep calling Python through a single resolver path so the switch from local Python to bundled sidecar is contained.
- FastAPI is not part of the desktop default. It remains an option only if the Python engine needs a long-running local service boundary.

## Sidecar Shape

```text
apps/desktop/src-tauri/sidecar/
  README.md
  python/
    <platform-specific runtime>

Packaged Tauri resources:

engine/
  setup_os/
    <packaged Python package source>
  examples/
    <bundled example inputs>
```

The first packaged release should include:

- `setup_os` package code and example inputs as packaged resources.
- Python runtime for the target platform.
- Generated-agent template assets needed by `python -m setup_os.cli create`.
- A smoke check equivalent to `python -m setup_os.cli --help`.

## Engine Resolver Order

The desktop app should resolve the Setup OS engine root in this order:

1. `SETUP_OS_REPO_DIR`, for development and explicit installed smoke overrides.
2. Packaged Tauri resource `engine/`, for installed release builds.
3. Nearby repo checkout search, for local development convenience.

## Resolver Order

The desktop command runner should resolve Python in this order:

1. `SETUP_OS_PYTHON`, for development and debugging.
2. Bundled sidecar Python, for release builds.
3. System `python`, for development fallback only.

## Release Gate

A release is not considered end-user ready until:

- the packaged engine resource exists and contains `setup_os/cli.py` plus bundled examples;
- the sidecar runtime exists for Windows and macOS;
- CI runs the packaged CLI smoke check;
- unsigned bundles can run without a preinstalled Python;
- signed/notarized release notes describe the sidecar behavior;
- the desktop readiness screen reports sidecar status.

## Non-Goals

- No cloud runtime requirement.
- No microservice split just to package Python.
- No automatic broker, email, calendar, or notification credentials in the sidecar.
