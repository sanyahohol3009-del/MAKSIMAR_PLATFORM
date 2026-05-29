# PHASE 5 — App Memory / Chat Memory / Automatic Sync Acceptance v1

Status: PHASE 5 acceptance document for JARVIS-readable architecture context.

This document explains what PHASE 5 added, where the source surfaces live, what is allowed, what is forbidden, and how future JARVIS/operator reasoning should understand the layer.

## 1. PHASE 5 purpose

PHASE 5 adds local mobile memory and controlled synchronization boundaries for MAKSIMAR/JARVIS.

The goal is not to create a second memory engine. The goal is to give Android/iOS clients their own local app memory and local chat memory, then expose a safe protocol/runtime/read-model path for future controlled sync with the server.

PHASE 5 covers:

- local app memory contracts;
- local chat memory contracts;
- Android app memory adapters;
- Android chat memory adapters;
- iOS app memory adapters;
- iOS chat memory adapters;
- shared mobile sync protocol;
- server mobile sync runtime wrapper;
- read-only sync dashboard and preview surfaces;
- final acceptance gates.

## 2. Closed batches

### BATCH 5.1 — App Memory Core Contracts

Primary surfaces:

- `shared_mobile_core/app_memory/app_memory_record_contract.py`
- `shared_mobile_core/app_memory/app_memory_store_contract.py`
- `shared_mobile_core/app_memory/app_memory_retention_policy.py`
- `shared_mobile_core/app_memory/app_memory_encryption_contract.py`

Meaning:

App memory is local mobile application state. It is not the global project memory, not CORE_ROOT truth, and not a replacement for existing memory architecture.

Core invariants:

- local mobile app memory only;
- reference-bound payload handling;
- sync requires policy;
- direct core write is forbidden;
- direct server write is forbidden;
- validation happens through dataclass `__post_init__`.

### BATCH 5.2 — Chat Memory Core Contracts

Primary surfaces:

- `shared_mobile_core/chat_memory/chat_memory_record_contract.py`
- `shared_mobile_core/chat_memory/chat_memory_store_contract.py`
- `shared_mobile_core/chat_memory/chat_memory_index_contract.py`
- `shared_mobile_core/chat_memory/chat_memory_retention_policy.py`

Meaning:

Chat memory is local mobile chat memory. It is not OpenIM truth, not core chat truth, and not canonical global memory.

Core invariants:

- local chat memory only;
- OpenIM remains adapter/runtime reference, not memory truth;
- chat message body and heavy payload stay reference-bound where required;
- sync requires policy;
- direct core write is forbidden;
- direct server write is forbidden.

### BATCH 5.3 — Android App Memory Store

Primary surfaces:

- `ANDROID_SHELL/memory_adapter/android_app_memory_store.py`
- `ANDROID_SHELL/memory_adapter/android_secure_local_store.py`
- `ANDROID_SHELL/memory_adapter/android_memory_encryption_bridge.py`
- `ANDROID_SHELL/memory_adapter/android_memory_retention_runtime.py`
- `ANDROID_SHELL/memory_adapter/android_memory_state_bridge.py`

Meaning:

Android app memory adapters bind local Android-side app memory to shared app memory contracts.

Boundary:

- Android adapter is not canonical truth;
- Android adapter does not write core;
- Android adapter does not write server canonical memory directly;
- Android adapter is not sync runtime.

### BATCH 5.4 — Android Chat Memory Store

Primary surfaces:

- `ANDROID_SHELL/memory_adapter/android_chat_memory_store.py`
- `ANDROID_SHELL/memory_adapter/android_chat_memory_index.py`
- `ANDROID_SHELL/memory_adapter/android_chat_offline_replay_state.py`
- `ANDROID_SHELL/memory_adapter/android_chat_memory_export_bridge.py`

Meaning:

Android chat memory adapters bind local Android-side chat memory to shared chat memory contracts.

Boundary:

- not OpenIM truth;
- not core chat truth;
- not canonical project memory;
- offline replay state is metadata, not direct execution.

### BATCH 5.5 — iOS App Memory Store

Primary surfaces:

- `IOS_SHELL/memory_adapter/ios_app_memory_store.py`
- `IOS_SHELL/memory_adapter/ios_secure_local_store.py`
- `IOS_SHELL/memory_adapter/ios_memory_encryption_bridge.py`
- `IOS_SHELL/memory_adapter/ios_memory_retention_runtime.py`
- `IOS_SHELL/memory_adapter/ios_memory_state_bridge.py`

Meaning:

iOS app memory adapters mirror the Android app memory adapter boundary while staying iOS-shell local.

Boundary:

- iOS adapter is not canonical truth;
- iOS adapter does not write core;
- iOS adapter does not write server canonical memory directly;
- iOS adapter is not sync runtime.

### BATCH 5.6 — iOS Chat Memory Store

Primary surfaces:

- `IOS_SHELL/memory_adapter/ios_chat_memory_store.py`
- `IOS_SHELL/memory_adapter/ios_chat_memory_index.py`
- `IOS_SHELL/memory_adapter/ios_chat_offline_replay_state.py`
- `IOS_SHELL/memory_adapter/ios_chat_memory_export_bridge.py`

Meaning:

iOS chat memory adapters bind local iOS-side chat memory to shared chat memory contracts.

Boundary:

- not OpenIM truth;
- not core chat truth;
- not canonical project memory;
- offline replay state is metadata, not direct execution.

### BATCH 5.7 — Mobile Sync Protocol

Primary surfaces:

- `shared_mobile_core/mobile_sync_models/mobile_sync_envelope_contract.py`
- `shared_mobile_core/mobile_sync_models/mobile_sync_cursor_contract.py`
- `shared_mobile_core/mobile_sync_models/mobile_sync_conflict_contract.py`
- `shared_mobile_core/mobile_sync_models/mobile_sync_policy.py`
- `shared_mobile_core/mobile_sync_models/server_presence_sync_trigger.py`
- `shared_mobile_core/mobile_sync_models/offline_to_server_replay_contract.py`

Meaning:

This is the shared mobile sync protocol contract layer. It models sync, but does not execute sync.

Core invariants:

- sync envelope is reference-only;
- allowed memory domains are `app_memory` and `chat_memory`;
- no inline payload;
- no message body;
- no heavy payload;
- no embedded secrets;
- no embedded key material;
- no direct core write;
- no direct server write;
- no network/socket/tunnel;
- no app/chat memory store mutation;
- cursor cannot regress;
- conflict decisions are deterministic and evidence-hash backed;
- automatic sync requires trusted server presence;
- offline replay requires policy, owner approval, device approval, and trusted server presence.

### BATCH 5.8 — Server Mobile Sync Runtime

Primary surfaces:

- `MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/mobile_sync_session_registry.py`
- `MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/app_memory_sync_runtime.py`
- `MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/chat_memory_sync_runtime.py`
- `MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/mobile_sync_conflict_resolver.py`

Meaning:

This is a server runtime wrapper over BATCH 5.7 contracts. It is not canonical memory truth and does not perform uncontrolled synchronization.

Core invariants:

- session registry exposes read-only session state;
- duplicate sessions are rejected;
- app sync runtime accepts only app memory envelopes;
- chat sync runtime accepts only chat memory envelopes;
- wrong envelope domain is rejected;
- policy is required;
- conflict resolver remains deterministic;
- no core write;
- no direct server canonical write;
- no network/socket/tunnel;
- no runtime connection;
- no direct app/chat store mutation;
- no OpenIM truth;
- no core chat truth.

### BATCH 5.9 — Sync Dashboard / Preview

Primary surfaces:

- `MAKSIMAR_CORE_LIB/mobile_bridge/mobile_sync_status_read_model.py`
- `MAKSIMAR_CORE_LIB/mobile_bridge/mobile_memory_status_read_model.py`
- `tools/mobile_memory_status_preview.py`
- `tools/mobile_sync_status_preview.py`

Meaning:

This is a read-only status/read-model/preview layer.

Boundary:

- dashboard is not executor;
- preview is not runtime;
- preview does not execute sync;
- preview does not mutate sessions;
- preview does not mutate app/chat stores;
- preview does not write core;
- preview does not write server canonical state;
- preview does not open network/socket/tunnel;
- preview does not call Android/iOS platform APIs;
- preview payload is deterministic and JSON-safe.

## 3. Source of truth boundaries

PHASE 5 source-of-truth rules:

- app memory is local mobile app state, not `memory_engine`;
- chat memory is local mobile chat state, not OpenIM truth and not core chat truth;
- Android/iOS shell adapters are local adapters only;
- mobile sync protocol is contract/model layer only;
- server mobile sync runtime is runtime wrapper only, not canonical memory truth;
- dashboard and preview are read-only observability surfaces;
- no PHASE 5 layer writes upward into CORE_ROOT;
- no PHASE 5 layer becomes global project memory.

## 4. Forbidden behaviors

The following are forbidden in PHASE 5:

- creating a second memory world;
- replacing existing memory architecture with mobile memory;
- making mobile app memory canonical project memory;
- making chat memory OpenIM truth;
- making server sync runtime canonical memory truth;
- direct core write;
- direct server canonical write;
- uncontrolled runtime mutation;
- sync without policy boundary;
- sync envelope with inline payload/message body/heavy payload/secrets/key material;
- cursor rollback;
- non-deterministic conflict resolution;
- fake success;
- silent success;
- dashboard direct execution;
- preview direct execution;
- Android/iOS platform API calls from dashboard/preview;
- network/socket/tunnel activation in protocol/dashboard/preview layers.

## 5. Dashboard and read-model surfaces

PHASE 5 dashboard/read-model surfaces are intentionally read-only.

Dashboard-relevant surfaces:

- mobile app memory status;
- mobile chat memory status;
- sync policy state;
- sync session count;
- app sync decision count;
- chat sync decision count;
- conflict resolution count;
- server presence state;
- automatic sync disabled/safe state;
- core/server/network/socket/tunnel write flags;
- dashboard action execution disabled flag;
- runtime mutation disabled flag.

These surfaces are intended for future operator dashboard integration, not execution.

## 6. JARVIS reasoning guidance

Future JARVIS reasoning should interpret PHASE 5 as:

- local mobile memory foundation;
- controlled mobile sync foundation;
- dashboard visibility foundation;
- not a finished live distributed memory system;
- not a direct runtime synchronization engine;
- not a replacement for project memory;
- not a replacement for chat runtime;
- not a dashboard action executor.

Correct next development points:

1. Final PHASE 5 acceptance.
2. Future hardening of old weak tests by separate correction roadmap.
3. Future controlled sync execution only after explicit policy/approval/runtime gates.
4. Future dashboard integration through existing dashboard/mobile bridge layers.
5. Future Android/iOS real persistence bindings through adapter-only boundaries.
6. Future server-side canonical ingestion only through approved governance, audit, and replay gates.

## 7. Acceptance criteria

PHASE 5 is accepted when:

- all expected PHASE 5 files exist;
- BATCH 5.1 through 5.10 readiness is complete;
- targeted PHASE 5 tests pass;
- full platform/project run passes;
- roadmap post-step drift check passes;
- unrelated dirty/untracked surfaces remain excluded;
- local HEAD and remote branch match after final push.
