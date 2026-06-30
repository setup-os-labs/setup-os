# Setup OS First 20 Component Research

Date: 2026-06-30

## Short Verdict

Use a Python-first, local-first stack centered on Pydantic models, PydanticAI, LiteLLM, Ollama, LangGraph, Qdrant, SQLite/Postgres, Docker Compose, and Copier.

The MVP should compose proven tools and add only thin Setup OS layers for conversation normalization, scoring, permissions, diffs, and Portfolio Agent glue. Avoid building a custom agent framework, custom vector database, custom LLM gateway, or custom workflow engine in the first pass.

## Default Stack

| Layer | Default | Lightweight | Enterprise-grade |
| --- | --- | --- | --- |
| Conversation import | Custom normalized parser adapters over `json`, `markdown-it-py`, `pypdf`, `python-docx`, `pandas` | Markdown/TXT/JSON only | Add `unstructured` or `docling` |
| Intent extraction | PydanticAI + Pydantic schemas | Instructor + Pydantic | LangGraph + PydanticAI + evals |
| Blueprint system | Copier | Cookiecutter | Nx generators plus Copier |
| OSS discovery | GitHub API + package registry APIs + curated source manifests | GitHub API only | OpenSearch/Meilisearch indexed registry |
| GitHub scoring | Minimal custom scorer using GitHub API, OSV, license metadata | Stars/releases/license rubric | ClearlyDefined + Scorecard + OSV + custom policy |
| Architecture planning | C4 in Mermaid + ADRs | Mermaid only | Structurizr DSL + Mermaid export |
| Composition | Docker Compose + Taskfile | Docker Compose only | Compose + devcontainers + optional Nix |
| Agent runtime | PydanticAI for typed agent loops | Direct LiteLLM calls | LangGraph for durable multi-step agents |
| Workflow orchestration | LangGraph for MVP workflows | Python async jobs | Temporal for durable production workflows |
| LLM gateway | LiteLLM proxy | LiteLLM SDK only | LiteLLM proxy with auth, budget, audit |
| Local LLM runtime | Ollama | llama.cpp directly | vLLM for GPU/server deployments |
| Structured output | Pydantic + JSON Schema | Pydantic only | Outlines/Guidance where constrained decoding matters |
| Vector database | Qdrant | SQLite vec/sqlite-vec | Qdrant cluster or pgvector |
| Structured database | SQLite for generated local agents; Postgres when multi-service | SQLite only | Postgres |
| Conversation-to-diff | Custom YAML/JSON patch generator + review manifest | Git diff only | Monaco/CodeMirror review UI later |
| Notification router | Apprise | Desktop/webhook only | ntfy + Apprise + cloud relay |
| Mobile push | ntfy | PWA/web push later | Expo/FCM/APNs relay |
| Action permission | OPA/Rego for system policies + simple risk gates | YAML allow/deny rules | OPA + Cedar-style resource policies |
| Local deployment | Docker Compose + Taskfile | uv/pnpm local process runner | Compose + devcontainer + systemd/launchd/Task Scheduler installers |
| Portfolio connector | CSV/manual upload + yfinance/SEC EDGAR market data | CSV only | Plaid/SnapTrade/Alpaca/IBKR adapters later |

## Component Recommendations

### 1. Conversation Source Parser

Candidates: custom source adapters, LangChain document loaders, LlamaIndex readers, `unstructured`, `docling`, MarkItDown.

Recommendation: build a thin custom adapter interface and compose mature parsers per file type. Conversation exports vary too much by vendor to depend on one universal parser. Normalize into a Setup OS `ConversationEnvelope` with `source`, `messages`, `attachments`, `provenance`, and `raw_refs`.

Avoid: making LangChain or LlamaIndex the canonical internal schema; use them only as optional ingestion helpers.

### 2. Intent Extraction Engine

Candidates: PydanticAI, Instructor, Outlines, Guardrails, DSPy, LangGraph extraction nodes.

Recommendation: PydanticAI + Pydantic schemas as default. It is type-first, Python-native, actively maintained, MIT licensed, and fits Setup OS's need for explainable structured extraction. PydanticAI had about 18.1k GitHub stars and a Jun 29, 2026 release when checked.

Use LangGraph when extraction becomes multi-step and stateful. Keep Instructor as the lightweight fallback.

### 3. Blueprint System

Candidates: Copier, Cookiecutter, Yeoman, Plop, Hygen, Nx generators.

Recommendation: Copier. It supports project template rendering, is MIT licensed, has active 2026 releases, and fits Python-first local generation. Cookiecutter is simpler but weaker for updates; Nx is powerful but adds JavaScript workspace gravity.

### 4. OSS Component Discovery Agent

Candidates: GitHub Search API, npm/PyPI/crates APIs, Ecosyste.ms, libraries.io, OpenAlex/Semantic Scholar for papers, curated awesome lists.

Recommendation: start with GitHub + package registries + curated source manifests. Store discoveries in a local SQLite registry. Add Ecosyste.ms/libraries.io later if API terms and freshness fit.

Avoid: scraping dynamic websites as a primary source.

### 5. GitHub Project Scorer

Candidates: custom GitHub scorer, OpenSSF Scorecard, OSV, deps.dev, ClearlyDefined, libraries.io.

Recommendation: custom scoring wrapper that can call GitHub metadata, OpenSSF Scorecard, OSV, and license data. Score: license, release recency, push recency, stars/forks, issue/PR velocity, security advisories, docs, Docker support, ecosystem fit.

MVP scoring can be deterministic and stored with timestamps so recommendations are reproducible.

### 6. Architecture Planner

Candidates: Mermaid, C4 model, Structurizr DSL, PlantUML, Diagrams-as-code, Graphviz.

Recommendation: C4-flavored Mermaid for MVP because it is easy to render in Markdown and agent-readable. Add ADRs for every important component decision.

Enterprise option: Structurizr DSL for richer model validation.

### 7. Composition Engine

Candidates: Docker Compose, devcontainers, Nix flakes, Devbox, Taskfile, Just, Tilt, Skaffold, Earthly.

Recommendation: Docker Compose + Taskfile. Compose is the best default for local multi-service stacks; Taskfile gives cross-platform commands without committing to Make on Windows.

Avoid: Nix as the default. Offer it as an advanced reproducibility layer later.

### 8. Agent Runtime Framework

Candidates: PydanticAI, LangGraph, CrewAI, AutoGen, Semantic Kernel, Haystack Agents, LlamaIndex agents, BeeAI, VoltAgent.

Recommendation: PydanticAI by default for single vertical agents and typed tool calls; LangGraph for workflows with explicit state transitions. This keeps the MVP understandable while preserving an upgrade path.

Avoid: CrewAI/AutoGen as core defaults for Setup OS because they can encourage opaque multi-agent behavior too early.

### 9. Workflow Orchestrator

Candidates: LangGraph, Temporal, Prefect, Dagster, Airflow, n8n, Hatchet, Kestra.

Recommendation: LangGraph for MVP deterministic-plus-agent workflows; Temporal as the enterprise option. Temporal is mature, MIT licensed, has strong local dev support, and was at about 21.3k GitHub stars with a Jun 10, 2026 release when checked.

Avoid: Airflow/Dagster for agent action orchestration; they are excellent data/workflow platforms but heavy for local personal agents.

### 10. LLM Gateway

Candidates: LiteLLM, Portkey gateway, Helicone, OpenRouter-like hosted gateways, LangChain model adapters, direct provider SDKs.

Recommendation: LiteLLM proxy. It gives one OpenAI-compatible interface across many providers, supports gateway deployment, MCP bridging, budget/guardrail features, and had about 52.1k GitHub stars with a Jun 27, 2026 release when checked.

Lightweight option: LiteLLM SDK directly inside the process.

### 11. Local LLM Runtime

Candidates: Ollama, llama.cpp, vLLM, LM Studio, LocalAI, GPT4All.

Recommendation: Ollama for default local model serving. It has desktop-friendly install paths, Docker support, REST API, Python/JS clients, and broad ecosystem adoption. Use llama.cpp for minimal embedded experiments and vLLM for GPU/server deployments.

### 12. Structured Output Validator

Candidates: Pydantic, JSON Schema, Instructor, Outlines, Guardrails, Zod.

Recommendation: Pydantic + JSON Schema as canonical. Add Instructor for provider-compatible structured extraction where helpful. Use Outlines only when constrained decoding is worth the extra coupling.

### 13. Vector Database

Candidates: Qdrant, Chroma, Milvus, Weaviate, pgvector, LanceDB, SQLite vec/sqlite-vec.

Recommendation: Qdrant as default for local-first RAG memory. It has strong Docker/local support, good API quality, active development, and had about 32.8k GitHub stars when checked.

Lightweight option: SQLite vec/sqlite-vec for tiny local agents.

### 14. Structured Database

Candidates: SQLite, Postgres, DuckDB, MySQL/MariaDB, Turso/libSQL.

Recommendation: SQLite for generated personal agents and Postgres for the Setup OS control plane or multi-service stacks. SQLite keeps local-first installs simple; Postgres is the escape hatch for concurrency, auth, and hosted pro features.

### 15. Conversation-to-Diff Engine

Candidates: custom JSON Patch/RFC 6902, DeepDiff, difflib, git diff, jsondiffpatch, Monaco diff UI.

Recommendation: build a minimal custom layer over JSON Patch plus git diffs. Output an `evolution_proposal.yaml` containing source conversation refs, proposed manifest changes, risk score, tests to run, and rollback plan.

### 16. Notification Router

Candidates: Apprise, ntfy, Gotify, Home Assistant notifications, SMTP, webhooks, desktop notifications.

Recommendation: Apprise as the router abstraction, with ntfy as the best default push target. Apprise covers many notification providers; ntfy fits local/self-hostable notification-first design.

### 17. Mobile Push Layer

Candidates: ntfy, Gotify, Expo push, Firebase Cloud Messaging, APNs, PWA web push, Matrix.

Recommendation: ntfy for MVP because it is simple, self-hostable, and mobile-friendly. Future Notification OS can add Expo/FCM/APNs behind an encrypted hosted relay.

### 18. Action Permission Engine

Candidates: OPA, Cedar, Casbin, oso, OpenFGA, custom YAML rules.

Recommendation: OPA for policy-as-code plus a simple Setup OS risk gate. OPA is more mature for local policy evaluation than Cedar in the OSS ecosystem, while Cedar remains interesting for AWS-style authorization semantics.

MVP: policy bundles plus `approval_required` thresholds for financial, external, irreversible, privacy, legal, and health actions.

### 19. Local Deployment Engine

Candidates: Docker Compose, Podman Compose, Nix, Devbox, mise, asdf, uv, pnpm, Taskfile, Just.

Recommendation: Docker Compose + Taskfile + uv/pnpm inside generated repos. Compose runs services; Taskfile standardizes commands; uv/pnpm keep Python/TypeScript dependencies fast.

Windows strategy: Docker Desktop or WSL2; avoid requiring systemd in MVP.

### 20. Portfolio Data Connector

Candidates: CSV/manual import, yfinance, SEC EDGAR, OpenBB, Plaid/SnapTrade, Alpaca, Interactive Brokers, unofficial Robinhood APIs.

Recommendation: CSV/manual import for holdings and transactions, yfinance/SEC EDGAR for market/fundamental enrichment, and optional broker adapters later. This is the safest MVP because it avoids credentials, trading permissions, and brittle unofficial APIs.

Avoid: unofficial Robinhood APIs as a default connector; use only behind explicit experimental flags.

## Integration Approach

1. Define `setupos.manifest.schema.json`, `ConversationEnvelope`, `AgentDNA`, `CapabilitySpec`, `ArchitecturePlan`, and `EvolutionProposal`.
2. Build source adapters that transform exports into `ConversationEnvelope`.
3. Run PydanticAI extraction through LiteLLM, defaulting to local Ollama when configured.
4. Score candidate components into a local SQLite registry.
5. Generate C4 Mermaid diagrams, ADRs, Docker Compose files, Taskfile tasks, and Copier-rendered vertical agent repos.
6. Use OPA/risk gates before actions with external, irreversible, financial, legal, health, or privacy effects.
7. For Portfolio Agent MVP, require CSV upload/manual import first; generate alerts only, no trade execution.

## Example Implementation Pattern

```yaml
setup_os:
  llm_gateway:
    provider: litellm
    mode: proxy
    default_model: ollama/qwen3
  local_llm:
    provider: ollama
    base_url: http://localhost:11434
  agent_runtime:
    default: pydantic_ai
    stateful_workflows: langgraph
  storage:
    structured: sqlite
    vectors: qdrant
  generation:
    blueprint_engine: copier
    composition: docker_compose
    commands: taskfile
  safety:
    policy_engine: opa
    human_approval:
      required_above_risk: medium
      always_for:
        - financial_execution
        - external_account_write
        - irreversible_delete
        - health_or_legal_advice
  notifications:
    router: apprise
    mobile_push: ntfy
  portfolio_agent:
    data_ingestion:
      - csv_upload
      - manual_holdings
    market_data:
      - yfinance
      - sec_edgar
    execution: disabled
```

## Risks

| Risk | Mitigation |
| --- | --- |
| OSS project health changes quickly | Store research snapshots with dates and rerun scoring before lock-in |
| LiteLLM license/enterprise boundary may affect feature use | Keep gateway usage to OSS features and document enterprise-only features |
| Agent frameworks move fast | Keep Setup OS schemas framework-neutral |
| Local models may underperform extraction tasks | Allow cloud models with PII redaction and explicit user approval |
| Docker Desktop friction on Windows/macOS | Provide non-Docker lightweight mode for single-agent MVPs |
| Portfolio data is sensitive and regulated | Alert-only MVP, no credentials, no execution, local storage by default |

## Avoid List

- Custom LLM gateway in MVP.
- Custom vector database.
- Custom multi-agent runtime.
- Defaulting to unofficial broker APIs.
- Making Nix mandatory.
- Using hosted-only discovery, telemetry, or sync as the core architecture.
- Allowing agents to execute financial or irreversible actions without explicit approval.

## Sources Checked

- LangGraph GitHub: https://github.com/langchain-ai/langgraph
- Temporal GitHub: https://github.com/temporalio/temporal
- LiteLLM GitHub: https://github.com/BerriAI/litellm
- Qdrant GitHub: https://github.com/qdrant/qdrant
- Ollama GitHub: https://github.com/ollama/ollama
- PydanticAI GitHub: https://github.com/pydantic/pydantic-ai
- Copier GitHub: https://github.com/copier-org/copier
- Docker Compose GitHub: https://github.com/docker/compose
