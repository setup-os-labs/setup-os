# Python Sidecar Packaging

Setup OS keeps the Python engine as the product core. The desktop app should eventually ship that engine as a bundled sidecar so end users do not need to install Python before using Setup OS.

## Current Decision

- Development builds can use the local `python` executable or `SETUP_OS_PYTHON`.
- Release builds should prefer a bundled Python sidecar.
- The desktop app should keep calling Python through a single resolver path so the switch from local Python to bundled sidecar is contained.
- FastAPI is not part of the desktop default. It remains an option only if the Python engine needs a long-running local service boundary.

## Sidecar Shape

```text
apps/desktop/src-tauri/sidecar/
  README.md
  python/
    <platform-specific runtime>
  setup_os/
    <packaged Python package>
```

The first packaged release should include:

- Python runtime for the target platform.
- `setup_os` package code.
- Generated-agent template assets needed by `python -m setup_os.cli`.
- A smoke check equivalent to `python -m setup_os.cli --help`.

## Resolver Order

The desktop command runner should resolve Python in this order:

1. `SETUP_OS_PYTHON`, for development and debugging.
2. Bundled sidecar Python, for release builds.
3. System `python`, for development fallback only.

## Release Gate

A release is not considered end-user ready until:

- the sidecar runtime exists for Windows and macOS;
- CI runs the packaged CLI smoke check;
- unsigned bundles can run without a preinstalled Python;
- signed/notarized release notes describe the sidecar behavior;
- the desktop readiness screen reports sidecar status.

## Non-Goals

- No cloud runtime requirement.
- No microservice split just to package Python.
- No automatic broker, email, calendar, or notification credentials in the sidecar.
