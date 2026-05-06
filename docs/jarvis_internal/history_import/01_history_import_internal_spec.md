# 01. JARVIS History Import Internal Specification

## Purpose
This document defines the internal specification for the chat history import layer inside the MAKSIMAR/JARVIS project memory system.

This document is intended for JARVIS and internal platform continuity only.
It is not user-facing documentation.
It does not forbid future corrective passes, structural refinements, or fidelity improvements.

## Main Goal
The history import layer must:
- accept exported chat history packages;
- recognize the export package structure;
- partition conversations by `conversation_id`;
- transform the source into machine-readable records;
- write the result into the project history store;
- avoid duplicating already imported data;
- support future reimports of newer exports;
- remain portable across storage roots, M.2 migration, and NAS relocation.

## Core Architectural Principles

### 1. Non-canonical history rule
Imported chat history is not canonical truth.
It is a supporting / project history memory layer.

It may be used for:
- self-readability;
- project history recall;
- context continuity;
- drift analysis;
- timeline reconstruction.

It must not be automatically promoted into:
- constitutional memory;
- regulatory memory;
- enterprise policy truth;
- safety-critical technical truth.

### 2. Deterministic import
The same export must always produce the same structural result:
- same conversation buckets;
- same manifest locations;
- same storage topology;
- same dedup behavior.

### 3. Incremental-safe reimport
Reimporting an already processed export must not:
- overwrite existing conversation manifests;
- overwrite existing normalized records;
- overwrite existing message units;
- create duplicate conversation buckets.

### 4. Conversation-first partitioning
Partitioning must be based on `conversation_id` from `conversations.json`.
`conversation_id` is the primary identity key for the imported chat history domain.

### 5. Attachment separation
Audio, images, and other exported files are not separate chats.
They are supporting artifacts and must be linked to the conversation/message layer.

### 6. Portability
The storage model must support relocation to:
- a different SSD / M.2;
- a NAS root;
- a different storage root without rewriting the memory objects themselves.

## Import Sources and Their Roles

### Metadata source
`export_manifest.json`

Role:
- package metadata;
- export file inventory;
- source package contract.

### Primary source
`conversations.json`

Role:
- primary structured source;
- contains conversation objects;
- contains message node mappings;
- provides `conversation_id`;
- acts as the source-of-structure for live import.

### Secondary source
`chat.html`

Role:
- secondary readable backup;
- cross-check source;
- human-readable source.

### Supporting sources
Folders containing:
- audio roots;
- user artifact roots;
- image/file roots.

Role:
- supporting attachment layer;
- not the primary chat source.

## Physical Staging Model

### Import staging
The export is first copied into staging:
`runtime_imports/chatgpt_export_01/`

Contents:
- `export_manifest.json`
- `conversations.json`
- `chat.html`
- attachment roots

### Project history store
Real writes go into:
`runtime_history_store/`

Structure:
- `registry/import_sessions/`
- `registry/attachment_links/`
- `normalized_history/conversations/`

## Conversation Partitioning Model
Each conversation object from `conversations.json` is treated as a separate chat bucket.

Bucket path form:
`normalized_history/conversations/<conversation_id>/`

For each bucket, the system creates:
- `conversation_manifest.json`
- `normalized_record.json`
- `message_units/<message_node_id>.json`

## Confirmed Current State
For the first real export, the following has been confirmed:
- 18 conversation objects detected;
- 18 conversation manifests created;
- 18 normalized conversation records created;
- 11822 message units created;
- 2 attachment roots recorded;
- session manifest written;
- attachment root summary written;
- repeat-safe reimport confirmed.

## Truth Formula for JARVIS
JARVIS must understand that:
- the history import layer exists;
- the layer is active;
- the layer is tested;
- the layer is conversation-partitioned;
- the layer is non-canonical;
- the layer is incremental-safe;
- the layer is portable;
- export #1 has already been imported successfully;
- export #2 must add only new conversation buckets and new units;
- corrective passes are allowed if they reduce drift and improve determinism.
