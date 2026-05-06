# 03. Incremental Reimport Rules

## Purpose
This document defines the rules for incremental reimport of chat history exports.

## Main Principle
A repeated import must not duplicate already imported conversation buckets or already written message units.

## Required Counters
The incremental layer must compute:

- `total_conversations_in_source`
- `existing_conversations`
- `new_conversations`
- `new_conversation_writes_required`
- `repeat_safe`
- `incremental_ready`

## Canonical Formula
`existing_conversations + new_conversations == total_conversations_in_source`

`new_conversation_writes_required == new_conversations`

## Behavior for Reimporting the Same Export
If the system reimports an already fully processed export, the expected result is:

- `existing_conversations = total_conversations_in_source`
- `new_conversations = 0`
- `new_conversation_writes_required = 0`
- `repeat_safe = True`

## Behavior for a New Export
When a newer export is imported, two scenarios are possible.

### Scenario A. Fully old export
- all conversation_ids are already known;
- nothing new needs to be written.

### Scenario B. Partially new export
- some conversation_ids already exist;
- some conversation_ids are new;
- only new conversation buckets and new units must be written.

## Forbidden Behavior
The system must not:
- overwrite old conversation manifests without necessity;
- overwrite old normalized records without necessity;
- overwrite old message units without necessity;
- create a second parallel import world;
- lose the connection between incremental logic and the existing project store.

## Confirmed State for Export #1
For the already imported first export, the following is confirmed:

- `total_conversations_in_source = 18`
- `existing_conversations = 18`
- `new_conversations = 0`
- `new_conversation_writes_required = 0`
- `repeat_safe = True`
- `incremental_ready = True`

This is the canonical confirmation of correct incremental-safe behavior.

## Required Behavior for Export #2 Acceptance Pass
When the next export is processed, the system must:
1. read the new `conversations.json`;
2. extract source conversation ids;
3. read existing conversation ids from `runtime_history_store`;
4. compute:
   - existing_conversations
   - new_conversations
   - new_conversation_writes_required
5. write only new buckets;
6. leave already imported conversation buckets untouched.

## Truth Formula for JARVIS
JARVIS must accept only a reimport flow that is:
- repeat-safe;
- deterministic;
- non-destructive;
- free of duplicate conversation buckets;
- explicit about existing/new split.
