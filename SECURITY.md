# Security Policy

Setup OS is pre-release. Please do not use it for real financial execution, broker automation, health decisions, legal decisions, or irreversible actions.

## Supported Versions

No stable versions are supported yet.

## Reporting Issues

Until a public security channel exists, open a private issue or contact the project owner directly.

Do not include secrets, broker credentials, tokens, private financial data, or personal health/legal data in public issues.

## Security Principles

- No broker execution in v0.
- No cloud dependencies in v0.
- No credentials in example files.
- Generated changes must be reviewable before application.
- Audit logs should record actions without storing unnecessary secrets.
- Future connectors must use explicit permission scopes.
