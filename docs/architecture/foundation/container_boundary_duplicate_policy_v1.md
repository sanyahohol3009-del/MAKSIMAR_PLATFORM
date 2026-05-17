# Container Boundary Duplicate Policy v1

## Status

Canonical container-boundary duplicate policy for PHASE 0 / BATCH 0.4.

## Purpose

This policy defines when a duplicate-looking file is allowed because it represents an intentional container, facade, adapter, proxy, or boundary layer.

The goal is extractability without breaking existing working code.

## Core rule

Existing working code is not moved or broken.

New container-ready services must be connected through stable contracts, DTOs, APIs, process boundaries, adapters, or facades.

Correct model:

```text
existing / legacy working code
  -> stable contract / DTO / API / process boundary
  -> thin adapter / facade
  -> container-ready service

