# 05. Message Attachment Linkage Rules

## Purpose
This document defines the message-level attachment linkage preparation rules for the history import track.

## Current Confirmed State
The system already confirms:
- `conversation_count = 18`
- `message_unit_count = 11822`
- `audio_candidate_count = 3`
- `image_candidate_count = 112`
- `message_attachment_linkage_ready = True`

## Meaning of the Current Layer
This layer does not yet claim exact final attachment-to-message truth.
It establishes candidate-level linkage preparation.

This means the layer now knows:
- attachments exist;
- attachments belong to the imported session;
- attachments belong to the conversation-partitioned history layer;
- attachments have message-level candidate scope.

## Current Scope
The current layer supports:
- attachment root recognition;
- candidate counting;
- conversation-scoped attachment preparation;
- message candidate preparation.

## Not Yet Claimed
The current layer does not yet guarantee:
- exact attachment -> exact message binding;
- exact attachment -> exact content part binding;
- semantic certainty of final attachment ownership.

## Required Truth Rule
JARVIS must interpret this layer as:
- candidate linkage layer;
- intermediate but valid structural preparation;
- safe to use for future refinement;
- non-destructive to the current history store.

## Forbidden Behavior
The system must not:
- treat candidate linkage as final semantic truth without stronger evidence;
- move attachments outside the history_ingestion domain;
- create a separate attachment storage world;
- break conversation-first partitioning.

## Future Direction
The next possible refinement after this layer would be:
- attachment -> exact conversation linkage;
- attachment -> exact message unit linkage;
- attachment -> exact content part linkage where the export format allows it.
