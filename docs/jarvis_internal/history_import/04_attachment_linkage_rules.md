# 04. Attachment Linkage Rules

## Purpose
This document defines the rules for the attachment linkage layer inside the history import track.

## Main Principle
Attachments are not separate chats.
Attachments are supporting artifacts and must be linked to the conversation/message layer.

## Already Confirmed State
For the first export, the following is confirmed:

- `conversation_count = 18`
- `audio_attachment_root_count = 1`
- `image_attachment_root_count = 1`
- `attachment_linkage_ready = True`

This means attachment roots are already recognized as part of the conversation-partitioned history domain.

## What Counts as an Attachment Source
Attachment sources include:
- audio roots;
- image roots;
- user artifact roots;
- supporting exported files.

## Forbidden Behavior
The system must not:
- treat an attachment root as a separate chat;
- treat the image root as a replacement for the primary source;
- import attachments as a standalone conversation domain;
- build a separate parallel attachment world outside `history_ingestion`.

## Correct Layer Model

### Layer 1. Root-level linkage
At the current stage, the system already confirms:
- attachment roots are recognized;
- roots are linked to the current session scope;
- roots are linked to the conversation-scoped history layer.

### Layer 2. Future message-level linkage
The next required layer is:
- identify conversation/message candidates for attachments;
- build attachment -> conversation linkage;
- build attachment -> message candidate linkage.

## Current Truth Rule
At the current stage, attachment linkage truth means:
- attachment roots exist;
- roots belong to the current export session;
- roots belong to the conversation-partitioned history layer;
- linkage is root-level, not yet full message-level.

## What JARVIS Must Understand
JARVIS must understand that:
- attachments exist;
- attachments are supporting-only;
- attachments are not the primary chat source;
- attachments must eventually be linked to message-level units;
- the current layer is complete only at root-level linkage;
- the next step is message-level attachment linkage.

## Correct Future Formula
The correct full model should look like:

export session
-> conversation scope
-> message units
-> attachment candidates
-> attachment linkage records

## Corrective-pass Rule
Attachment linkage may be strengthened further if the improvement:
- reduces drift;
- preserves conversation-first partitioning;
- does not break repeat-safe import;
- does not create a second storage world.
