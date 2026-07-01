# Setup OS Desktop

Desktop shell for Setup OS.

This app is intentionally a thin Tauri shell over the Python engine during the MVP. Development mode calls the local Python interpreter. Packaged releases should use a bundled Python sidecar that exposes the same CLI contract.

## Goals

- launch vertical agents
- import planning conversations
- show raw import and extraction status
- show recent evolution proposals
- run generated-agent verification
- preserve local-first behavior

## Development

```bash
npm install
npm run dev
```

The first command contract the shell must preserve is:

```bash
python -m setup_os.cli --help
```

The first product action contract is:

```bash
python -m setup_os.cli create examples/portfolio_conversation.md --output generated/desktop-portfolio-os
```

After generation, the shell can run the generated report command:

```bash
cd generated/desktop-portfolio-os
python report.py
```

The shell can also run the generated health check:

```bash
cd generated/desktop-portfolio-os
python health.py
```

## Packaging Direction

Tauri release builds should bundle a Python sidecar later. The sidecar must keep the same command behavior as development mode before the desktop app grows a local API or FastAPI service.
