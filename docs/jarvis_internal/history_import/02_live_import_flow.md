# 02. Live Import Flow

## Purpose
This document defines the canonical live import pipeline for chat history exports.

## Canonical Sequence

### Step 1. Export staging
The export is first copied into project staging:
`runtime_imports/chatgpt_export_01/`

Contents:
- `export_manifest.json`
- `conversations.json`
- `chat.html`
- attachment roots

### Step 2. Manifest recognition
The system reads `export_manifest.json`.

Goals:
- confirm the export bundle composition;
- confirm primary / secondary / attachment sources;
- record package metadata.

### Step 3. Primary parse
The system reads `conversations.json` as the primary source.

Goals:
- parse conversation objects;
- extract `conversation_id`;
- extract message node mappings;
- collect message node ids.

### Step 4. Conversation partitioning
For each `conversation_id`, the system constructs a bucket path:
`normalized_history/conversations/<conversation_id>/`

This establishes conversation-first partitioning.

### Step 5. Live import session
The system builds an import session summary:
- session_id;
- source_manifest_path;
- source_conversations_path;
- conversation_count;
- attachment_roots.

### Step 6. Conversation manifests
For each conversation bucket, the system creates:
`conversation_manifest.json`

Purpose:
- record chat identity;
- record bucket path;
- record message count.

### Step 7. Normalized conversation records
For each conversation bucket, the system creates:
`normalized_record.json`

Purpose:
- record a normalized conversation-level record;
- preserve the non-canonical nature;
- prepare a Jarvis-readable history layer.

### Step 8. Message units
For each message node id, the system creates:
`message_units/<message_node_id>.json`

Purpose:
- represent message-level units;
- provide machine-readable layout;
- prepare future enrichment / richer payload import.

### Step 9. Attachment linkage summary
Attachment roots are recorded as supporting artifacts:
- audio roots;
- image roots;
- user artifact roots.

At the current stage, only root-level linkage summary is recorded.
Future work requires message-level linkage.

### Step 10. Project write
Real writes go into:
`runtime_history_store/`

### Step 11. Repeat-safe reimport check
After the first write, reimporting the same export must produce:
- existing_conversations > 0
- new_conversations = 0
- new_conversation_writes_required = 0

## Confirmed Real Result for Export #1
- conversation_count = 18
- conversation_manifest_count = 18
- normalized_record_count = 18
- message_unit_count = 11822
- attachment_root_count = 2
- repeat_write_safe = True

## Expected Next Live Step
When import #2 is processed:
- old conversation_ids must be detected as existing;
- new conversation_ids must be detected as new;
- only new conversation buckets and new units must be written.
