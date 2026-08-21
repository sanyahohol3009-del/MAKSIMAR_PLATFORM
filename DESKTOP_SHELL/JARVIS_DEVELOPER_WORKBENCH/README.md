# JARVIS_DEVELOPER_WORKBENCH

Status: accepted first-class MAKSIMAR/JARVIS desktop shell architecture  
Role: developer/operator workbench and communication surface  
Foundation: frozen fork of Code - OSS (`microsoft/vscode`)  
Authority: downstream client only; never a second brain or truth source

## Purpose

`JARVIS_DEVELOPER_WORKBENCH` is a native part of `MAKSIMAR_PLATFORM`.
It is not treated as an optional external library and it is not a separate AI core.

The workbench exists to provide one integrated development surface for:

- direct conversation with the real JARVIS Core
- project tree / Explorer
- source editing
- integrated terminal
- Git / Source Control
- diff and review
- tests, Problems and Output
- project architecture inspection
- audit and evidence views
- model selection projected from the canonical JARVIS model registry
- an independent Codex co-developer client

## Canonical UI baseline

The initial implementation reuses the mature Code - OSS workbench rather than recreating an IDE from zero.
The first live baseline keeps the existing high-value shell infrastructure, including:

- title/menu/top bars
- Command Center and navigation controls
- Settings Editor and JSON settings
- user/workspace settings
- profiles
- themes
- keybindings
- Activity Bar
- Primary Side Bar
- Secondary Side Bar
- Explorer
- Search
- Source Control
- editor area and tabs
- breadcrumbs
- terminal
- Problems
- Output
- Testing
- Debug UI
- diff editor
- status bar
- layout persistence
- Extension Host and extension APIs required by approved clients
- existing chat presentation components

No broad deletion is allowed before the live acceptance gate.

## Chat integration

The existing Code - OSS chat presentation layer is reused where practical.
The target is not to build another chat UI from scratch.

The backend authority is replaced with MAKSIMAR/JARVIS:

```text
Code - OSS Chat UI
        |
        v
JARVIS_WORKBENCH_BRIDGE
        |
        v
JARVIS Core
```

The workbench must not maintain an independent semantic router, memory truth, model registry, tool registry, policy truth, approval truth, or evidence truth.
Those remain upstream in the platform.

## Codex role

Codex is a permanent independent co-developer client.
During the initial workbench stages Codex is not controlled by JARVIS.
It remains an independent development/audit tool operating through the terminal and its supported editor integration.

Therefore the workbench must preserve the APIs and Extension Host capabilities required by the approved Codex client until compatibility is proven after each removal/refactor batch.

## Frozen upstream policy

Code - OSS is used as a frozen source foundation.
A selected upstream commit is recorded in `upstream_manifest.yaml` before integration work begins.

Policy:

- no automatic upstream merges
- no automatic Microsoft feature adoption
- no dependency on Microsoft release cadence
- no automatic product update channel
- security vulnerabilities in Electron/Chromium/Node/dependencies remain monitored
- security fixes are reviewed and backported through MAKSIMAR-controlled releases

## Progressive ownership plan

The workbench evolves in this order:

1. freeze exact Code - OSS commit
2. reproduce clean upstream build and launch
3. verify independent Codex compatibility
4. connect existing chat UI to the real JARVIS Core
5. expose only canonical JARVIS models and sessions
6. prove text/streaming/session/voice paths
7. close live acceptance gate
8. remove Copilot-specific backend, quota, entitlement, signup, pricing and cloud coupling
9. remove or replace Microsoft cloud services, telemetry, experiments, recommendations, sync/tunnels and upstream updater where not required
10. replace unrestricted Marketplace usage with MAKSIMAR-governed extension distribution
11. introduce MAKSIMAR branding, installer, signing and release pipeline
12. progressively replace services/components where replacement creates architectural, security, operational or product value

Mature local components such as the editor, terminal rendering, tree/layout infrastructure or diff UI do not need to be rewritten merely for ownership optics.
Reuse is preferred until a real unique requirement justifies replacement.

## Extension policy

The Extension Host remains a permanent platform capability unless a future accepted architecture replaces it.
Extensions are classified as:

- MAKSIMAR first-party
- permanent trusted client
- audited open source
- quarantined
- denied

Codex is a permanent trusted client.
External extensions are not automatically trusted.

## Security boundary

The workbench is a presentation and intent surface.
It may read, visualize, request and propose actions.
It must not become an uncontrolled execution authority.

Canonical flow:

```text
UI intent
  -> platform contract
  -> policy / security / approval
  -> controlled execution
  -> evidence / audit
  -> read model
  -> UI
```

## Relationship to Godot 4

Godot 4 is the engine used for other MAKSIMAR/JARVIS dashboards.
The number 4 is the Godot engine version, not a dashboard count.
There may be many Godot 4 dashboards.

`JARVIS_DEVELOPER_WORKBENCH` is one separate developer dashboard/shell.
Godot dashboards and this workbench are peer downstream clients of the same JARVIS platform authority.

## Relationship to CYBER_DEFENSE_AND_FORENSICS_CUBE

The cyber-defense cube may expose read models, incidents, evidence and controlled response proposals inside the workbench.
The workbench does not directly mutate firewall rules, kill processes, quarantine containers or perform response actions outside the platform policy/execution path.

## Live acceptance gate

Deep cleanup may begin only after the workbench proves at least:

- reproducible build and launch
- project Explorer works
- editor and terminal work
- top bars and settings work
- Git/diff work
- existing chat UI talks to the real JARVIS Core
- streaming and cancellation work
- canonical model list is projected from JARVIS
- sessions survive restart
- voice path works through the approved voice edge
- Codex operates independently in the modified build
- layout/state survives restart

## Final rule

The workbench is part of MAKSIMAR/JARVIS itself.
Code - OSS is the initial implementation substrate, not the architectural authority and not the long-term product identity.
