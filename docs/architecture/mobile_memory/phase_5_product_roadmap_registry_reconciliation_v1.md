# Product Roadmap v4.2 PHASE 5 Registry Reconciliation v1

## Scope

This document registers Product Roadmap v4.2 PHASE 5:

- App Memory
- Chat Memory
- Automatic Sync

It is a registry and architecture boundary entry only. It does not implement
batch 5.1 source contracts or any Android, iOS, server runtime, sync model, or
dashboard preview source files.

## Non-target historical 5.x documents

Product PHASE 5 is not MemPalace PHASE 5.1.

Product PHASE 5 is not AI_ORCHESTRATION PHASE 5.

Product PHASE 5 is not Memory Roadmap v5.1.

Those documents remain historical/foundation records and must not be treated as
the implementation surface for Product Roadmap v4.2 PHASE 5.

## Registered batches

- BATCH 5.1 - App Memory Core Contracts
- BATCH 5.2 - Chat Memory Core Contracts
- BATCH 5.3 - Android App Memory Store
- BATCH 5.4 - Android Chat Memory Store
- BATCH 5.5 - iOS App Memory Store
- BATCH 5.6 - iOS Chat Memory Store
- BATCH 5.7 - Mobile Sync Protocol
- BATCH 5.8 - Server Mobile Sync Runtime
- BATCH 5.9 - Sync Dashboard / Preview
- BATCH 5.10 - PHASE 5 Acceptance

## Existing surfaces to extend or bind

- `ANDROID_SHELL/memory_adapter/` already exists and must be extended, not replaced.
- `IOS_SHELL/memory_adapter/` already exists and must be extended, not replaced.
- `MAKSIMAR_CORE_LIB/mobile_bridge/` already exists and must be extended for sync and memory status read models.
- `MAKSIMAR_CORE_LIB/chat_command/` and `MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/` already exist and must be reused or bound, not duplicated.
- `MAKSIMAR_CORE_LIB/memory_engine/` already exists and must not be replaced.
- `shared_mobile_core/p2p_mesh_network/` already has server presence models that can inform automatic sync trigger semantics.

## Boundary decisions

- App memory is local mobile app state, not global project memory.
- Chat memory is local chat history, index, and replay state. It is not OpenIM truth and not MAKSIMAR core chat truth.
- Android and iOS memory stores are shell adapters, not canonical truth.
- Server mobile sync runtime must not write core directly.
- Automatic sync starts when server presence appears, but remains policy-gated.
- Sync is offline-first, conflict-aware, and audit-visible.
- No duplicate dashboard root is allowed; Product PHASE 5 extends `MAKSIMAR_CORE_LIB/mobile_bridge`.

## Readiness expectation

After this reconciliation entry, existing PHASE 0-4 batches remain READY.

Product PHASE 5 batches 5.1-5.10 are expected to appear as MISSING until their
implementation batches are completed.
