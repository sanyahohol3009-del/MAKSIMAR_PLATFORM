# Product Roadmap v4.2 PHASE 5 Semantic Duplicate Decision v1

## Decision

Product PHASE 5 creates narrowly scoped mobile app memory, mobile chat memory,
mobile sync protocol, server mobile sync runtime, and mobile sync status
read-model surfaces.

It does not create a parallel memory engine, parallel chat truth, parallel
server sync truth, or duplicate dashboard root.

## Duplicate scan result

Read-only semantic duplicate preview for Product PHASE 5 target paths reported:

- true duplicate risk count: 0
- high risk count: 0
- migration candidates present
- container boundary duplicates present

The warnings are expected because Product PHASE 5 intentionally binds to
existing memory, chat, sync, mobile shell, and dashboard surfaces.

## Required reuse decisions

- Reuse or bind `MAKSIMAR_CORE_LIB/memory_engine/`; do not replace it.
- Reuse or bind `MAKSIMAR_CORE_LIB/chat_command/`; do not redefine MAKSIMAR chat truth.
- Reuse or bind `MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/`; do not create a second chat runtime.
- Reuse `ANDROID_SHELL/memory_adapter/`; do not create another Android memory adapter root.
- Reuse `IOS_SHELL/memory_adapter/`; do not create another iOS memory adapter root.
- Extend `MAKSIMAR_CORE_LIB/mobile_bridge/`; do not create a duplicate dashboard/read-model root.

## Non-target historical 5.x records

Product PHASE 5 is not MemPalace PHASE 5.1.

Product PHASE 5 is not AI_ORCHESTRATION PHASE 5.

Product PHASE 5 is not Memory Roadmap v5.1.

Those records remain non-target history for this implementation track.

## Safety laws

- App memory is local mobile app state, not global project memory.
- Chat memory is local chat history/index/replay state, not OpenIM truth and not MAKSIMAR core chat truth.
- Android/iOS memory stores are shell adapters, not canonical truth.
- Server mobile sync runtime must not write core directly.
- No direct core write from mobile shell.
- No network, socket, or tunnel opening in contracts.
- No runtime mutation unless explicitly modeled and gated.
- Automatic sync starts when server presence appears, but remains policy-gated.
- Sync must be conflict-aware, audit-visible, and offline-first.
