# JARVIS CODE - OSS TRACK STATUS — 2026-08-31

Branch: `workbench/code-oss-baseline-2026-08-31`  
Merge state: DO NOT MERGE until the active Semantic Spine / GoalFrame/library track is closed and this branch is rebased/reconciled.

## JWB-0 — Frozen upstream baseline

Status: PASS

Pinned source:

- `microsoft/vscode`
- commit `f291f3fd7a3aa047515c65348d8f674a009aba94`
- `code-oss-dev 1.136.0`
- Node `24.18.0`
- Electron `42.10.0`
- MIT

Evidence is recorded in `DESKTOP_SHELL/JARVIS_DEVELOPER_WORKBENCH/upstream_manifest.yaml`.

## JWB-1 — Local reproducible clone/build

Status: PENDING LOCAL EXECUTION

Prepared bootstrap:

`scripts/workbench/bootstrap_code_oss_windows.ps1`

Required acceptance:

- clone exact pinned SHA
- verify SHA / Node manifest / package version / Electron target
- install dependencies with correct native Windows toolchain
- compile/watch successfully
- launch `scripts\code.bat`
- record baseline build result without modifying JARVIS semantic/runtime code

## JWB-2 — Code - OSS archaeology / reuse map

Status: READY TO START

Scope:

- identify existing chat presentation owners
- identify extension-host surfaces required by Codex
- identify terminal/workspace/settings/layout owners to preserve
- identify Copilot-specific backend seams to replace later
- identify minimal Workbench bridge seam to existing JARVIS endpoint

No removal or backend rewrite yet.

## JWB-3 and later

Blocked until JWB-1/JWB-2 evidence exists.

Planned order:

1. Codex compatibility baseline
2. Workbench bridge to existing JARVIS endpoint
3. chat streaming/cancel/session mapping
4. canonical model projection
5. voice/read-model surfaces
6. live acceptance
7. bounded cleanup/replacement batches

## Active-project boundary

This branch does not own the current RU GoalFrame stability repair or any existing semantic debt.
It must not introduce UI/provider shortcuts to compensate for upstream semantic behavior.
