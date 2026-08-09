# Z.E.L.D.A.

Personal AI operating system, built around an Ubuntu control core.

> Development repository: `Vester084` — intended to be renamed to `Z.E.L.D.A.` later.

## Architecture

```text
You
 │
 ▼
AI Core
 │
 ▼
Intent / Tool Router
 │
 ▼
Permission Layer
 │
 ├── Ubuntu Tools
 │   ├── System
 │   ├── Applications
 │   ├── Files
 │   └── Network
 │
 ├── Communications
 │   ├── Phone
 │   ├── SMS
 │   ├── Email
 │   └── Social platforms
 │
 ├── Android Companion
 │
 ├── Memory
 │
 ├── Voice
 │
 └── Visual Core
```

## Phase 1

The first milestone is a local Ubuntu control service with an explicit tool registry. Z.E.L.D.A. must not receive unrestricted shell access. Capabilities are exposed as individual tools with permission and audit controls.

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
