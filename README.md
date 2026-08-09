# Z.E.L.D.A.

Z.E.L.D.A. is a modular AI control system built around an Ubuntu control core.

## Phase 1: working control service

The first implementation is now in place as a small local Python service with:

* Command intake
* Deterministic intent routing
* Explicit tool registration
* Permission checks
* In memory audit logging
* Safe system status and time tools
* A clean extension point for an AI model

Z.E.L.D.A. does **not** expose unrestricted shell execution.

## Architecture

```text
You
 │
 ▼
Control API
 │
 ▼
AI Core / Intent Router
 │
 ▼
Permission Engine
 │
 ▼
Explicit Tool Registry
 ├── System Status
 └── Time
 │
 ▼
Audit Log
```

The next layer will connect an AI provider to the intent and tool routing system. Additional tools will then be added as isolated capabilities.

## Run on Ubuntu

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
PYTHONPATH=src python -m zelda
```

The service listens on `127.0.0.1:8787`.

## API

### Health

```bash
curl http://127.0.0.1:8787/health
```

### List tools

```bash
curl http://127.0.0.1:8787/v1/tools
```

### Send a command

```bash
curl -X POST http://127.0.0.1:8787/v1/command \
  -H 'Content-Type: application/json' \
  -d '{"command":"system status"}'
```

## Test

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Roadmap

1. Ubuntu control core
2. AI model integration and natural language tool selection
3. Permission and confirmation engine
4. Voice interface
5. Persistent memory
6. Android companion
7. Communications bridge
8. Visual Three.js core
9. Device and smart home bridge
10. Advanced workflows
