# Root Artifact Hygiene Acceptance v1

## Status

Acceptance document for PHASE 0 / BATCH 0.5.

## Layer

`ROOT_ARTIFACT_HYGIENE`

## Accepted batches

### BATCH 0.1 — Baseline + Location Inventory

Accepted outputs:

- `RootSurfaceInventoryReadModel`
- read-only root inventory
- no delete
- no move
- dashboard-safe status fields

### BATCH 0.2 — Artifact Classification + Semantic Duplicate Scan

Accepted outputs:

- `ArtifactClassificationReadModel`
- `SemanticDuplicateScanReadModel`
- artifact classification policy
- semantic duplicate scan policy
- no auto-delete
- no auto-move
- approval-required flags

### BATCH 0.3 — Root Report Builder

Accepted outputs:

- `RootArtifactReportReadModel`
- `SemanticDuplicateReportReadModel`
- terminal JSON tools:
  - `tools/root_artifact_hygiene_report.py`
  - `tools/root_artifact_semantic_duplicate_scan.py`

### BATCH 0.4 — Preview + Documentation

Accepted outputs:

- `LocationValidationPreviewReadModel`
- `SemanticDuplicatePreviewReadModel`
- archival policy
- location matrix
- semantic duplicate scan policy
- container boundary duplicate policy

### BATCH 0.5 — Acceptance + Radar/X-Ray Binding

Accepted outputs:

- root artifact hygiene acceptance document
- foundation roadmap correction patch document
- `.gitignore` generated artifact policy
- blueprint ignored artifact policy
- X-Ray marker binding
- roadmap provenance binding

## Non-mutation guarantees

The layer guarantees:

- `scan_readonly = true`
- `delete_allowed = false`
- `move_allowed = false`
- `dashboard_safe = true`
- `runtime_mutation_allowed = false`
- `canonical_write_allowed = false`

## Accepted operator workflow

The operator may:

1. inspect generated reports;
2. inspect root artifact classification;
3. inspect semantic duplicate candidates;
4. decide later whether a correction/archive pass is needed.

The operator may not use this layer to automatically clean files.

## Future dashboard exposure

Future dashboard panels may expose:

- root cleanliness summary;
- archive candidate count;
- correction required count;
- approval required count;
- semantic duplicate risk count;
- container boundary duplicate count;
- next action.

Future dashboard panels must remain read-only.

## Acceptance gates

PHASE 0 acceptance requires:

1. Roadmap CI passes for BATCH 0.5 with `--require-files`.
2. Architecture Guard passes.
3. X-Ray has zero AST parse errors.
4. Full auto pytest passes.
5. Git commit includes only BATCH 0.5 files.
