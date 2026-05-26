# Project File Readiness Map v1

Status: manual foundation slice after PHASE 0 / Batch 0.1.

## Purpose

The Project File Readiness Map shows roadmap readiness at file and batch level.

This is different from Architecture Radar and X-Ray:

- Radar/X-Ray show layer-level structure and drift signals.
- File Readiness Map shows roadmap-expected files, existing files, missing files and batch readiness.

## Critical rule

The registry must include the full active roadmap phase, not only completed batches.

For PHASE 0 this means:

- 0.1 Existing Scanner Discovery
- 0.2 Repository Scan Models
- 0.3 Repository Scan Runtime
- 0.4 Pytest Output Hygiene
- 0.5 Project Readiness Runner Core
- 0.6 Project Readiness Sub-Runners
- 0.7 Readiness Runtime JSON + Dashboard Export
- 0.8 PHASE 0 Acceptance

This prevents false READY reports when only completed batches are registered.

## Rules

- The tool is read-only by default.
- It writes JSON only when --output is explicitly provided.
- It does not mutate source files.
- It does not replace tests.
- It does not replace Drift Guard.
- It supports target mode and point-script mode.
- Full-platform report printing remains controlled by MAKSIMAR_FULL_PLATFORM_REPORTS=1 and --maksimar-full-platform-reports.

## Current expected result

At this point:

- Batch 0.1 should be READY.
- Batch 0.4 should be READY.
- Remaining PHASE 0 batches should be MISSING or PARTIAL.
- Overall PHASE 0 readiness should be PARTIAL until 0.8 is closed.

## CLI

Text output:

    ./.venv/bin/python tools/project_readiness_control/project_file_readiness_map.py

One batch:

    ./.venv/bin/python tools/project_readiness_control/project_file_readiness_map.py --batch-id 0.1

JSON output:

    ./.venv/bin/python tools/project_readiness_control/project_file_readiness_map.py --json

Write dashboard-ready runtime JSON explicitly:

    ./.venv/bin/python tools/project_readiness_control/project_file_readiness_map.py \
      --json \
      --output RUNTIME/state/readiness/project_file_readiness.json

## Acceptance

Accepted when:

1. PHASE 0 Batch 0.1 through 0.8 are registered.
2. Reports return READY for completed batches.
3. Reports return PARTIAL/MISSING for incomplete batches.
4. Target pytest stays quiet.
5. CLI can emit JSON.
6. No core-to-tools import is introduced.
