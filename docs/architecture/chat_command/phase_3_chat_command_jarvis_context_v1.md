# JARVIS Context — PHASE 3 Chat Command / Sovereign Messenger v1

## Purpose

This document explains what PHASE 3 added to the MAKSIMAR/JARVIS platform so a future JARVIS/operator can understand the chat layer without reconstructing the reasoning from commits.

PHASE 3 creates the foundation for an internal sovereign messenger:

- server-phone chat
- phone-phone chat foundation
- server-server sync references
- PC/operator chat dashboard read models
- file/photo/media attachment references
- offline queue references
- mobile client bridges
- container readiness boundary

This is not yet a real production messenger runtime.

## What is now available

### 1. Chat core contracts

Location:

- `MAKSIMAR_CORE_LIB/chat_command/`

Main contracts:

- `chat_message_contract.py`
- `command_message_contract.py`
- `chat_room_contract.py`
- `chat_identity_contract.py`

Meaning:

- defines messages
- defines command intent messages
- defines rooms
- defines identities
- prevents direct execution
- prevents runtime mutation
- separates chat intent from control-plane execution

### 2. Attachment / offline / sync contracts

Location:

- `MAKSIMAR_CORE_LIB/chat_command/`

Files:

- `file_transfer_contract.py`
- `media_attachment_contract.py`
- `offline_delivery_contract.py`
- `server_sync_contract.py`
- `message_encryption_contract.py`

Meaning:

- file/media attachments are references, not direct file operations
- offline delivery is a queue contract, not a mobile wake/sync runtime
- server sync is declared as review/approval-bound, not direct replication
- encryption/checksum/scan/quarantine requirements are explicit

### 3. Chat-to-command boundary

Location:

- `MAKSIMAR_CORE_LIB/chat_command/chat_to_command_handoff_contract.py`

Meaning:

- chat can create operator intent
- intent must pass policy review
- operator approval is required
- sandbox is required
- final execution must go through control-plane
- chat itself never executes tasks

### 4. OpenIM reference adapter boundary

Location:

- `MAKSIMAR_CORE_LIB/chat_command/openim_reference_adapter_contract.py`

Meaning:

- OpenIM is reference/research/quarantine adapter only
- OpenIM is not chat truth
- OpenIM is not runtime authority
- OpenIM cannot write core
- OpenIM cannot execute commands
- OpenIM download/runtime remains disabled until a separate vendor/quarantine/security gate

### 5. Server chat runtime foundation

Location:

- `MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/`

Files:

- `chat_session_registry.py`
- `message_router_runtime.py`
- `offline_queue_runtime.py`
- `chat_audit_runtime.py`

Meaning:

- in-memory server reference runtime
- session registry
- message routing decision model
- offline queue reference model
- append-only audit event reference model

What it does not do:

- no ports
- no sockets
- no real delivery
- no database writes
- no canonical writes
- no command execution

### 6. Server file/media/sync reference runtime

Location:

- `MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/`

Files:

- `file_transfer_runtime.py`
- `media_attachment_runtime.py`
- `server_to_server_sync_runtime.py`

Meaning:

- plans file transfer references
- tracks media attachment references
- plans server sync references

What it does not do:

- no file copy
- no file write
- no media render
- no upload/download
- no real server-to-server sync workers

### 7. Android chat client foundation

Location:

- `ANDROID_SHELL/chat_client/`

Files:

- `README.md`
- `chat_sync_contract.py`
- `chat_state_bridge.py`
- `chat_message_store.py`
- `offline_queue_bridge.py`
- `chat_notification_bridge.py`
- `file_attachment_bridge.py`
- `media_attachment_bridge.py`

Meaning:

- Android local chat state references
- Android local message store references
- Android offline queue bridge
- Android notification bridge contract
- Android file/media attachment bridge contracts

What it does not do:

- no Android API call
- no background service start
- no wake lock
- no storage picker
- no media API
- no direct network
- no plaintext persistence

### 8. iOS chat client foundation

Location:

- `IOS_SHELL/chat_client/`

Files:

- `README.md`
- `chat_sync_contract.py`
- `chat_state_bridge.py`
- `chat_message_store.py`
- `offline_queue_bridge.py`
- `chat_notification_bridge.py`
- `file_attachment_bridge.py`
- `media_attachment_bridge.py`

Meaning:

- iOS local chat state references
- iOS local message store references
- iOS offline queue bridge
- iOS notification bridge contract
- iOS file/media attachment bridge contracts

What it does not do:

- no iOS API call
- no background task start
- no document picker
- no media API
- no direct network
- no plaintext persistence

### 9. Dashboard / reactive button read models

Location:

- `MAKSIMAR_CORE_LIB/chat_command/`

Files:

- `chat_system_read_model.py`
- `chat_session_read_model.py`
- `message_queue_read_model.py`
- `file_transfer_read_model.py`
- `chat_operator_intent_models.py`
- `chat_button_state_models.py`

Meaning:

- dashboard can display chat system state
- dashboard can display sessions
- dashboard can display queues
- dashboard can display file transfer references
- dashboard can display operator intent
- buttons are display-only / approval-required / control-plane handoff-required

Critical rule:

- dashboard button does not execute directly

### 10. Preview tools and container readiness

Locations:

- `tools/chat_system_preview.py`
- `tools/chat_sync_preview.py`
- `CONTAINER_DEPLOYMENT/cubes/chat_command/`

Container files:

- `container_contract.yaml`
- `network_policy.yaml`
- `runtime_profile.yaml`

Meaning:

- preview can emit safe dashboard/sync JSON
- container readiness exists as a contract
- runtime remains disabled by default
- ingress/egress/open ports remain disabled
- dashboard cannot start container runtime

## Current truth status

PHASE 3 status after acceptance:

- implemented: contracts, models, tests, preview tools, container readiness metadata
- not implemented: real messenger backend
- not implemented: real OpenIM/Spika/Matrix runtime
- not implemented: real Android/iOS native chat UI
- not implemented: real encrypted transport
- not implemented: real push notifications
- not implemented: real attachment upload/download
- not implemented: real server-to-server sync

## Source of truth

Chat command truth starts in:

- `MAKSIMAR_CORE_LIB/chat_command/`

Server runtime references live in:

- `MAKSIMAR_SERVER/CHAT_COMMAND_RUNTIME/`

Mobile shell references live in:

- `ANDROID_SHELL/chat_client/`
- `IOS_SHELL/chat_client/`

Container readiness lives in:

- `CONTAINER_DEPLOYMENT/cubes/chat_command/`

Dashboard/read-only surfaces consume read models only.

## Next development points

After PHASE 3 closure, future work can continue with:

1. vendor/quarantine evaluation for OpenIM / Spika / Matrix
2. real chat transport adapter behind security gate
3. encrypted local storage implementation
4. mobile Flutter UI binding
5. push notification adapter contracts
6. server persistence adapter
7. message history search/indexing
8. tenant-aware chat rooms
9. final dashboard panel integration
10. production container runtime only after explicit approval

## Non-negotiable safety spine

The chat layer must continue to follow:

- chat intent is not execution
- buttons are not execution
- mobile bridge is not execution authority
- dashboard is read-only
- external messenger is adapter-only
- vendor code never becomes core truth
- control-plane + policy + approval + sandbox remain mandatory
