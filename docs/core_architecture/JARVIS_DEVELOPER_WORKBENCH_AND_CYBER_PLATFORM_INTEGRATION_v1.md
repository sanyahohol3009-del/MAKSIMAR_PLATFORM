# JARVIS DEVELOPER WORKBENCH AND CYBER PLATFORM INTEGRATION v1

Status: accepted canonical architecture decision  
Scope: developer desktop shell, Code - OSS ownership plan, Codex boundary, Godot 4 dashboard relationship, cyber-defense cube and Linux knowledge integration

## 1. Decision

MAKSIMAR/JARVIS adopts `JARVIS_DEVELOPER_WORKBENCH` as a first-class project component under `DESKTOP_SHELL`.

The Workbench begins from a frozen fork of Code - OSS, but Code - OSS is only the initial implementation substrate. The architectural owner, product identity, integration contracts, release policy and long-term evolution belong to MAKSIMAR/JARVIS.

The Workbench is not an external helper bolted onto the project and it is not a replacement core.

## 2. Ownership boundary

Canonical platform authority remains upstream in MAKSIMAR/JARVIS.
The Workbench must reuse the existing semantic spine, registries, memory truth, evidence truth, policy truth and runtime control paths.

It must not create duplicate:

- semantic routing
- model registry
- tool registry
- agent registry
- memory authority
- policy/approval authority
- evidence authority

The Workbench consumes canonical read models/contracts and submits user intent through governed platform paths.

## 3. Code - OSS adoption strategy

The first baseline intentionally preserves the mature IDE/workbench facilities needed for immediate usefulness:

- top bars, menus and Command Center
- Settings UI, profiles, themes and keybindings
- Activity Bar / primary and secondary sidebars
- Explorer / Search / Source Control
- editor, tabs, breadcrumbs and diff
- terminal
- Problems / Output / Testing / Debug
- status bar and layout persistence
- Extension Host and required APIs
- existing chat presentation components

An exact upstream commit must be pinned before implementation begins.
There are no automatic upstream feature merges and no dependency on Microsoft release cadence.

Security vulnerabilities in Electron, Chromium, Node and third-party dependencies remain monitored. Security fixes are selectively backported and released through MAKSIMAR-controlled builds.

## 4. First live goal

Before deep cleanup, the Workbench must become a working MAKSIMAR client:

```text
Explorer / Editor / Terminal / Git / Settings
                    +
             Existing Chat UI
                    |
                    v
         JARVIS_WORKBENCH_BRIDGE
                    |
                    v
              JARVIS Core
```

The chat UI is reused where practical; Copilot-specific backend authority is replaced by the real JARVIS Core.
The model selector is a projection of the canonical JARVIS model registry, not a second registry.

## 5. Codex boundary

Codex is a permanent independent co-developer client.
During initial stages it is not commanded or permissioned by JARVIS.

Codex is used as an independent development/audit worker through supported terminal/editor integration.
Therefore Extension Host and APIs needed by Codex are protected compatibility surfaces until each change is proven safe.

Full autonomous JARVIS <-> Codex orchestration is a separate future track and must not be silently introduced during Workbench integration.

## 6. Cleanup and replacement order

Deep cleanup begins only after live acceptance proves JARVIS and Codex operation.

Removal/replacement candidates include, in controlled batches:

- Copilot backend/provider coupling
- Copilot entitlement, quota, signup, pricing and onboarding
- cloud-only AI provider paths not required by MAKSIMAR
- Microsoft telemetry endpoints
- experiments / remote recommendations
- Settings Sync and tunnels if not required
- upstream product updater
- unrestricted external Marketplace access

The Extension Host remains as a governed extensibility mechanism.
MAKSIMAR first-party extensions are preferred; audited open-source extensions may be admitted through policy. Codex is a permanent trusted client.

## 7. Update independence

The Workbench must eventually have MAKSIMAR-controlled:

- product identity
- branding
- build configuration
- installer
- signing
- release pipeline
- extension policy/distribution
- update channel

Upstream feature updates are opt-in research inputs only, never automatic obligations.

## 8. Godot 4 relationship

Godot 4 is the selected engine for additional MAKSIMAR/JARVIS visual dashboards.
The number 4 is the Godot engine version, not a dashboard count.
Many dashboards may be built with Godot 4.

`JARVIS_DEVELOPER_WORKBENCH` is one separate developer/operator dashboard/shell.
It and Godot 4 dashboards are peer downstream clients of the same platform authority.
Neither may become a hidden backend or source of truth.

## 9. CYBER_DEFENSE_AND_FORENSICS_CUBE

`CYBER_DEFENSE_AND_FORENSICS_CUBE` is a first-class domain cube under `DOMAIN_CUBES`.
It provides defensive security observation, detection, incident correlation, governed response proposals, evidence preservation, forensics and isolated training-lab capabilities.

It must remain defensive-only outside owned/authorized labs and must not implement hackback or uncontrolled retaliation.

## 10. Linux kernel relationship

The Linux kernel is a knowledge/architecture/system-mechanism donor for this platform, especially for cyber defense and systems learning.

Relevant public mechanisms include eBPF, cgroup v2, seccomp, Landlock/LSM concepts, namespaces, capabilities, netlink, audit/journald, procfs/sysfs, fanotify/inotify and tracing/perf.

MAKSIMAR should build independent userspace adapters/controllers/sensors around documented interfaces rather than copying kernel implementation code and relabeling it.

## 11. Live acceptance gate

Deep removal/refactoring is blocked until the modified Workbench proves:

- reproducible build and launch
- working Explorer/editor/terminal/Git/diff/settings/top bars
- existing chat UI connected to the real JARVIS Core
- streaming, cancellation, model projection and session restoration
- approved voice path
- independent Codex operation
- persistent layout/state

Every later removal/rewrite batch follows:

```text
inventory
 -> dependency map
 -> proposal
 -> diff
 -> build/tests
 -> JARVIS smoke test
 -> Codex smoke test
 -> acceptance
```

## 12. Architecture invariants

This decision reinforces existing platform invariants:

- ONE semantic spine
- ONE memory truth
- ONE evidence truth
- ONE policy/approval truth
- no UI-as-truth
- no shell-as-hidden-backend
- reuse before new abstraction
- no architecture drift through convenience duplication

## 13. Final classification

`JARVIS_DEVELOPER_WORKBENCH` is part of the MAKSIMAR/JARVIS platform.
`CYBER_DEFENSE_AND_FORENSICS_CUBE` is part of the MAKSIMAR/JARVIS platform.
Godot 4 dashboards are platform shell clients.
Code - OSS and Linux kernel are upstream knowledge/implementation sources with explicit boundaries; they do not own MAKSIMAR architecture.
