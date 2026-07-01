# Agnostic Architecture

Setup OS should not bind users to one model, one chat app, one runtime, or one deployment style.

## Provider-Neutral Layers

| Layer | Examples |
| --- | --- |
| Conversation source | ChatGPT, Claude, Cursor, Gemini, Perplexity, Markdown, TXT, JSON |
| LLM | OpenAI, Anthropic, Gemini, local Ollama, vLLM, LM Studio |
| Runtime | laptop, Mac mini, Raspberry Pi, NAS, VPS, Docker |
| OS | macOS, Linux, Windows, WSL |
| Vector store | Qdrant, Chroma, LanceDB, SQLite vec |
| Agent runtime | LangGraph, PydanticAI, CrewAI, AutoGen, custom Python |
| Notifications | console, ntfy, Apprise, Telegram, email, mobile app |
| Scheduler | cron, systemd timers, Task Scheduler, Docker, n8n |
| Secrets | local `.env`, 1Password, Bitwarden, OS keychain |
| Storage | local files, SQLite, Postgres, DuckDB |
| UI | none, CLI, Markdown, Streamlit, Next.js, generated dashboard |
| Deployment | local process, Docker Compose, systemd, private server |

## Core Interfaces

Setup OS should build around interfaces:

- `ConversationProvider`
- `LLMProvider`
- `MemoryStore`
- `AgentRuntime`
- `NotificationProvider`
- `SchedulerProvider`
- `DeploymentTarget`
- `VerticalBlueprint`
- `EvolutionEngine`
- `ComposerAgent`

## Positioning Rule

The product should never say:

```text
You need OpenAI.
```

It should say:

```text
Bring any model. Bring any conversation. Generate any local OS.
```

## Systems Composer

Setup OS is an AI Systems Composer.

It selects components, arranges them, wires them together, and evolves the architecture over time. Coding is an implementation detail; architecture, composition, evolution, and simplification are the durable artifacts.

## Optimize For Deletion

Most AI builders optimize for adding. Setup OS should repeatedly ask:

- Can this capability disappear?
- Can this dependency be avoided?
- Can one agent replace several?
- Can notifications replace UI?
- Can a generated dashboard stay out of scope?

Minimalism compounds.
