# Open Core Strategy

Setup OS should be open-source first because the product needs trust, forks, stars, templates, and community pressure around local-first personal AI systems.

## Open Source Core

The core should remain useful without a paid service:

- CLI
- conversation ingestion
- spec extraction schemas
- architecture proposal flow
- component registry
- blueprint generator
- local deployment templates
- notification interfaces
- audit log
- evolution proposal system
- starter verticals
- local memory interfaces

## Paid Layers Later

Paid features should solve operational complexity, not hold the local product hostage:

- hosted control plane
- encrypted sync
- managed always-on runner
- mobile app
- marketplace distribution
- premium vertical packs
- team policy and governance
- one-click cloud deployment
- managed backups

## Boundary Rule

If a feature is required to turn a planning conversation into a local running system, it belongs in the open core.

If a feature makes that system easier to operate across devices, teams, uptime requirements, or hosted infrastructure, it can be commercial later.

## License Posture

Use Apache 2.0 for the initial core. It is permissive, familiar to companies, and includes an explicit patent grant.

Revisit licensing only if the project faces hosted clone pressure after the core has real adoption.
