# 06. Project History Store Topology

## Purpose
This document defines the storage topology of the project history store used by JARVIS.

## Root
The current storage root is:
`runtime_history_store/`

## Registry Layer
The registry layer contains:
- `registry/import_sessions/`
- `registry/attachment_links/`

### import_sessions
Stores session-level import manifests.

### attachment_links
Stores attachment root summaries and linkage-level support artifacts.

## Normalized History Layer
The normalized history layer contains:
- `normalized_history/conversations/`

Inside this folder, every imported chat has its own bucket:

`normalized_history/conversations/<conversation_id>/`

Each conversation bucket contains:
- `conversation_manifest.json`
- `normalized_record.json`
- `message_units/<message_node_id>.json`

## Topology Principle
This is a conversation-first topology.

The structure is not organized by:
- arbitrary folders;
- HTML order;
- attachment roots.

It is organized by:
- `conversation_id` from `conversations.json`.

## Confirmed Store Counts
Current confirmed counts:
- session manifests: 1
- attachment summaries: 1
- conversation manifests: 18
- normalized records: 18
- message units: 11822

## Portability Rule
The topology must remain portable.
The storage root may be moved to:
- another SSD / M.2;
- NAS;
- another storage root.

The internal relative topology must remain stable.

## Drift Rule
The topology must not drift into:
- a second history store root;
- parallel registry worlds;
- parallel normalized conversation worlds;
- attachment-only alternate stores.

## Truth Rule for JARVIS
JARVIS must treat this topology as the current valid project history store layout.
