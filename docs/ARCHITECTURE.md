# Z.E.L.D.A. Architecture

## Core flow

```text
User -> Interface -> AI Core -> Intent Router -> Permission Engine -> Tool -> Device
```

## Design principles

* Local-first where practical.
* Explicit tools instead of unrestricted shell execution.
* Sensitive actions require confirmation.
* Every tool invocation can be audited.
* Providers and device connectors remain replaceable.
* Ubuntu is the first control host; Android is a future companion device.

## Initial tool domains

### Ubuntu

* System status
* Applications
* Files
* Network

### Communications

* Phone calls
* SMS
* Email
* Social messaging through supported official interfaces or approved device/browser integrations

### Future

* Voice
* Memory
* Android companion
* Visual core
* Smart devices
