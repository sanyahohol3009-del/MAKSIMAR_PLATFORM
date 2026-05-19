# SECURITY_LAYER adapters

## Status

PHASE 1 / BATCH 1.1 surface.

## Purpose

This directory is the batch-controlled adapter/facade boundary between existing working policy/governance/security-related code and container-ready SECURITY_LAYER services.

## Rules

- No direct runtime execution from dashboard.
- No duplicated business logic.
- No moving legacy files.
- No deleting legacy files.
- No direct upward write into core.
- Adapters must be introduced only after explicit contract tests.
