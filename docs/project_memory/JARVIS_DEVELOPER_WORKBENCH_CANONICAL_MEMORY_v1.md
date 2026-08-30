# JARVIS DEVELOPER WORKBENCH — CANONICAL PROJECT MEMORY v1

Status: accepted project-memory retrieval record + active implementation track  
Purpose: compact cross-session index to the accepted Workbench/cyber architecture without duplicating all implementation detail

## Canonical facts

- `JARVIS_DEVELOPER_WORKBENCH` is a first-class part of `MAKSIMAR_PLATFORM` under `DESKTOP_SHELL`; it is not merely an external library.
- Its initial implementation foundation is a frozen fork of Code - OSS (`microsoft/vscode`).
- The exact upstream commit must be pinned before implementation; automatic upstream feature merges are disabled.
- MAKSIMAR owns the long-term architecture, product identity, branding, integrations, extension policy, installer, signing, release pipeline and update channel.
- Security monitoring/backports for Electron/Chromium/Node/dependencies remain controlled by MAKSIMAR even though upstream feature updates are not followed automatically.
- The initial Code - OSS shell is kept broadly intact until live acceptance: top bars, menus, Command Center, settings, profiles, themes, keybindings, Explorer, Search, Git, editor, tabs, breadcrumbs, terminal, Problems, Output, Testing, Debug, diff, status bar, layout persistence, Extension Host/APIs and existing chat presentation.
- The existing chat UI is reused where practical; Copilot-specific backend/cloud authority is replaced by a bridge to the real JARVIS Core.
- The Workbench must never create a second semantic router, memory truth, model registry, tool/agent registry, policy/approval truth or evidence truth. It remains a downstream shell/read-model/intent surface.
- Codex is a permanent independent co-developer client. During initial stages JARVIS does not control Codex. Codex compatibility is a STOP-GATE before deep Code - OSS cleanup.
- Deep cleanup begins only after reproducible build, JARVIS chat/model/session/voice integration, working editor/terminal/Git/settings/top bars/layout, and independent Codex operation are proven.
- Cleanup/replacement is incremental: Copilot backend/entitlement/quota/signup/pricing/onboarding/cloud coupling first, then unneeded Microsoft telemetry/experiments/recommendations/sync/tunnels/updater/Marketplace paths, with build/tests/JARVIS/Codex validation after each batch.
- Extension Host remains a governed platform capability. MAKSIMAR first-party extensions are preferred; audited open-source extensions may be admitted; Codex is a permanent trusted client.
- Godot 4 is the engine for other MAKSIMAR/JARVIS dashboards. The "4" is the engine version, not a count of dashboards. `JARVIS_DEVELOPER_WORKBENCH` is one separate developer dashboard/shell; Godot dashboards are peer downstream clients.
- `CYBER_DEFENSE_AND_FORENSICS_CUBE` is a first-class domain cube under `DOMAIN_CUBES`.
- That cube is defensive-only outside owned/authorized labs and owns observation, detection, incident correlation, governed protective-response proposals, evidence, forensics and isolated cyber-security training capabilities while reusing canonical platform truth/policy/execution boundaries.
- The Linux kernel is a knowledge/architecture/system-mechanism donor, not code to copy into the core. Relevant mechanisms include eBPF, cgroup v2, seccomp, Landlock/LSM concepts, namespaces, capabilities, netlink, audit/journald, procfs/sysfs, fanotify/inotify and tracing/perf. MAKSIMAR writes independent userspace adapters/controllers/sensors around documented interfaces.

## Active implementation checkpoint — 2026-08-31

The Workbench implementation track has started in isolated branch:

`workbench/code-oss-baseline-2026-08-31`

JWB-0 frozen upstream baseline is pinned to:

- upstream: `microsoft/vscode`
- Code - OSS commit: `f291f3fd7a3aa047515c65348d8f674a009aba94`
- observed upstream commit time: `2026-08-30T22:10:47Z`
- package: `code-oss-dev 1.136.0`
- Node manifest: `24.18.0`
- Electron target: `42.10.0`
- license: MIT

This pin is now the immutable upstream reference for the current Workbench campaign unless the owner explicitly approves a different baseline before JWB-1 acceptance.

The current semantic/GoalFrame repair remains owned by its existing active track. The Workbench branch must not clean/reset/revert or patch around that work. In particular, no UI keyword routing or direct provider shortcut may be introduced to hide semantic defects.

The Code - OSS branch initially owns only:

- frozen upstream baseline
- reproducible bootstrap/build reproduction
- Code - OSS archaeology
- Workbench integration contract
- shell/read-model integration work that reuses existing JARVIS owners

Before eventual merge, the Workbench branch must be rebased/reconciled onto the completed main semantic/library track and pass the canonical acceptance gates.

New implementation source:

- `docs/workbench/JARVIS_CODE_OSS_INTEGRATION_CONTRACT_v1.md`
- `scripts/workbench/bootstrap_code_oss_windows.ps1`

## Current reusable JARVIS owners that Workbench must consume

The project state supplied for this campaign records these existing owners/capabilities as already implemented and therefore reuse-first:

- Global Semantic Spine / GoalFrame
- hierarchical capability -> operation -> organ architecture
- provider separation
- authenticated owner identity
- authorization boundary
- PC Hands
- Browser Organ
- Voice software path
- External Agent Provider Layer
- Simulation Worker
- SANDBOX_REVIEW
- ExecutionReceipt / EvidenceBundle
- FinalBrain evidence discipline
- DeveloperExperience / LearningBundle / CLIENT_LEARNING_INPUT
- append-only experience persistence / retrieval after restart
- Proposal Audit / Self Expansion Gate
- Developer Workbench architecture
- bounded semantic/candidate observability

No duplicate brain/planner/memory/registry/policy/evidence/learning system is permitted inside the Workbench.

## Canonical detailed sources

Read these before changing this architecture:

1. `docs/canonical_architecture_map.md`
2. `docs/core_architecture/JARVIS_DEVELOPER_WORKBENCH_AND_CYBER_PLATFORM_INTEGRATION_v1.md`
3. `DESKTOP_SHELL/JARVIS_DEVELOPER_WORKBENCH/README.md`
4. `DESKTOP_SHELL/JARVIS_DEVELOPER_WORKBENCH/upstream_manifest.yaml`
5. `DOMAIN_CUBES/CYBER_DEFENSE_AND_FORENSICS_CUBE/README.md`
6. `docs/core_architecture/CORE_INVARIANTS_AND_FORBIDDEN_DRIFT_v1.md`
7. `docs/core_architecture/CORE_TRUTH_SOURCES_v1.md`
8. `docs/workbench/JARVIS_CODE_OSS_INTEGRATION_CONTRACT_v1.md`

## Retrieval rule

When this memory record is found in a future session, treat the listed architecture as accepted project context unless a later canonical decision explicitly supersedes it.
Do not infer that Code - OSS or Linux owns MAKSIMAR architecture, and do not reintroduce removed cloud/product dependencies merely to track upstream.
