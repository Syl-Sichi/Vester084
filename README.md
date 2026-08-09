# Z.E.L.D.A.

Z.E.L.D.A. is an Ubuntu first AI control system built around explicit capabilities, model providers, permissions, and auditable execution.

## Current architecture

```text
User
  -> CLI / API
  -> Brain
  -> Model Provider
  -> Intent
  -> Tool Registry
  -> Permission Engine
  -> Tool
  -> Result
```

## Current capabilities

* Safe Ubuntu system status
* Current UTC time
* Explicit tool registration
* Default deny permissions
* Deterministic fallback intent parser
* Local Ollama provider
* Programmatic command API
* Command line interface

Arbitrary shell execution is intentionally not exposed by the current tool registry.

## Local AI

Install Ollama separately on the Ubuntu host, then configure:

```bash
export ZELDA_AI_PROVIDER=ollama
export ZELDA_OLLAMA_MODEL=gemma3:4b
```

Z.E.L.D.A. uses `http://127.0.0.1:11434` by default. Without this configuration, the deterministic rules provider remains active.

## CLI

```bash
python -m zelda.cli "check my computer"
python -m zelda.cli "what time is it"
```

## Development

```bash
pytest
```

## Roadmap

1. Ubuntu control core
2. Natural language AI routing
3. Confirmation and approval workflows
4. Persistent memory
5. Voice interface
6. Android companion
7. Messaging and social integrations
8. Visual interface
9. Device and smart home bridge
10. Advanced workflows
