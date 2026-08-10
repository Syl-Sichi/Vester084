# Z.E.L.D.A.

Z.E.L.D.A. is a cross platform AI control system built around explicit capabilities, model providers, permissions, confirmation workflows, and auditable execution.

## Architecture

```text
User
  -> CLI / Desktop Shell
  -> Brain
  -> Model Provider
  -> Intent
  -> Tool Registry
  -> Permission Engine
  -> Platform Capability
  -> Result
```

The desktop shell is intentionally separate from execution. Desktop, CLI, and future voice interfaces use the same controlled runtime and permission boundary.

## Supported platforms

Current platform foundations:

* Ubuntu/Linux capabilities
* macOS capabilities
* Automatic platform detection

Z.E.L.D.A. selects platform specific capabilities while keeping the AI core shared.

## Current capabilities

* System information
* Current time
* Application discovery
* Platform detection
* Constrained workspace writing
* Explicit tool registration
* Default deny permissions
* Confirmation based actions
* Local Ollama provider
* Deterministic fallback provider
* Desktop shell state model

Arbitrary shell execution is intentionally not exposed by the tool registry.

## First run setup

After installation, run:

```bash
zelda-launch
```

On a fresh machine Z.E.L.D.A. creates:

```text
~/.zelda/
├── config.json
└── workspace/
```

The setup process records the detected platform and prepares the private workspace.

## Local AI

Install Ollama separately, then configure:

```bash
export ZELDA_AI_PROVIDER=ollama
export ZELDA_OLLAMA_MODEL=gemma3:4b
```

Without this configuration, the deterministic rules provider remains active.

## Desktop shell

The first desktop layer is represented by `zelda.desktop.DesktopShell`. It provides the UI state boundary for:

* Chat
* System
* Apps
* Files
* Security
* Settings

The shell does not execute arbitrary operating system commands. A future native macOS UI will connect these views to the existing controlled service.

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

1. Cross platform control core
2. Natural language routing
3. Confirmation workflows
4. Dynamic permission engine
5. Application manager
6. File intelligence
7. Persistent memory
8. Voice interface
9. Native desktop interface
10. Messaging integrations
11. Smart home bridge
12. Advanced workflows
