# PHASE 3 — Chat Command / Sovereign Messenger Acceptance v1

## Status

PHASE 3 acceptance candidate.

This phase establishes the internal chat / sovereign messenger foundation for MAKSIMAR/JARVIS.

## Scope completed

PHASE 3 includes:

1. Chat core contracts.
2. Attachments / offline delivery contracts.
3. Chat-to-command handoff boundary.
4. OpenIM reference adapter contract.
5. Server chat runtime foundation.
6. Server file / media / server-sync runtime references.
7. Android chat client contracts.
8. Android chat attachment bridges.
9. iOS chat client contracts.
10. iOS chat attachment bridges.
11. Chat dashboard read models and reactive button states.
12. Chat preview tools and container readiness contracts.

## Canonical source boundaries

Core contracts:

- `MAKSIMAR_CORE_LIB/chat_command/`

Server runtime reference layer:

- `MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/`

Android client reference layer:

- `ANDROID_SHELL/chat_client/`

iOS client reference layer:

- `IOS_SHELL/chat_client/`

Container readiness layer:

- `CONTAINER_DEPLOYMENT/cubes/chat_command/`

Preview tools:

- `tools/chat_system_preview.py`
- `tools/chat_sync_preview.py`

## Safety guarantees

PHASE 3 does not implement real messenger runtime.

The following remain disabled:

- direct command execution
- dashboard direct control
- runtime mutation
- canonical truth writes
- direct server writes
- direct mobile API execution
- Android/iOS API calls
- background service / background task start
- sockets
- external network access
- real file transfer
- real media rendering
- real OpenIM runtime
- real Spika runtime
- real Matrix runtime
- container start

## Acceptance gates

Acceptance requires:

- roadmap expected files for PHASE 3.1 through 3.12 are READY
- target acceptance test passes
- JARVIS context document exists
- preview/container safety flags remain false
- full platform auto run passes before final phase closure commit/push

## JARVIS context document

The explanatory JARVIS-readable context document is:

- `docs/architecture/chat_command/phase_3_chat_command_jarvis_context_v1.md`

It is an operator/development reasoning document, not a blocking policy layer.
