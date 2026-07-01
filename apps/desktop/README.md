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

The raw-memory import action accepts a conversation path and uses the generated conversation importer:

```bash
cd generated/desktop-portfolio-os
python import_conversation.py ../../examples/portfolio_update.md
```

The desktop can also import generated Portfolio CSV data files for holdings, transactions, cash, watchlist, and market snapshots. The default paths point at repo examples and can be replaced with local exports.

For smoke testing, the shell exposes a full demo flow that creates the Portfolio OS, imports bundled sample data, imports a saved conversation, extracts memory drafts, runs health, runs the report, and refreshes status.

The shell can then create review-only structured memory drafts:

```bash
cd generated/desktop-portfolio-os
python extract_memory.py
```

The shell also exposes a read-only status check for generated Portfolio artifacts.

## Packaging Direction

Tauri release builds should bundle a Python sidecar later. The sidecar must keep the same command behavior as development mode before the desktop app grows a local API or FastAPI service.

Unsigned desktop bundle builds can be run manually from GitHub Actions with the `Desktop Release Build` workflow. The workflow builds Linux, Windows, and macOS Tauri bundles and uploads the generated artifacts. Signed releases still require platform-specific certificates and notarization decisions.
