# Governance

Setup OS is founder-led while the project is pre-MVP.

## Current Model

- Product direction is maintained by the project owner.
- Contributions are accepted through pull requests.
- Architecture changes require an ADR under `docs/adr/`.
- Safety-sensitive changes require explicit review before merge.

## Decision Priorities

1. Local-first by default.
2. Human approval for architecture and risky actions.
3. Compose existing tools before building new ones.
4. Deterministic artifacts before autonomous mutation.
5. CLI and Markdown before dashboards.
6. Open core boundaries stay clear.

## Future Model

After v0 stabilizes, governance can expand to include:

- maintainers by subsystem
- release owners
- security reviewers
- blueprint reviewers
- commercial boundary review
