# Foundation Roadmap Correction Patch v1

## Status

Canonical acceptance document for PHASE 0 / BATCH 0.5.

## Roadmap family

`batched_foundation_roadmap_v2_1_correction_patch`

## Purpose

This document records the correction patch applied to the foundation roadmap.

The patch does not replace v1/v2. It extends the roadmap with additional safety and anti-drift requirements.

## Added requirements

1. Roadmap reconciliation before every batch.
2. Exact path location slice before every batch.
3. Semantic duplicate scan before creating files.
4. Location validation table before implementation.
5. No delete without correction pass.
6. No move without correction pass.
7. Container adapter boundary for extractable services.
8. `layer_manifest.yaml` for new major layers.
9. Dashboard-ready read models for visible outputs.
10. Machine-readable preview output.
11. No dashboard mutation.
12. No UI-to-execution path.
13. Drift Guard after target implementation.
14. X-Ray after target implementation.
15. Full auto pytest as final gate: `./.venv/bin/python -m pytest -q -n auto`.

## Correction phases

The correction patch applies to:

- PHASE 0 — Root Artifact Hygiene / Archival Pass
- PHASE 1 — SECURITY_LAYER FOUNDATION v1
- PHASE 2 — DATA_PLANE FOUNDATION v1
- PHASE 3 — UPDATE_RECOVERY_INFRA FOUNDATION v1
- PHASE 4 — NETWORK_CONTAINERIZATION BLUEPRINT v1
- PHASE 5 — AI_ORCHESTRATION / Multi-Agent / Autonomous Planning
- PHASE 6 — Domain / Registry Enrollment for Foundation Layers

## Batch Done Protocol

A batch is not closed until:

1. Target files exist.
2. Required tests exist.
3. Roadmap CI passes for the batch.
4. Architecture Guard passes.
5. X-Ray has zero AST parse errors.
6. Full auto pytest passes.
7. Git status is reviewed.
8. Only batch files are committed.
9. Push is clean.

## Root Artifact Hygiene acceptance

PHASE 0 is accepted only when:

- root artifact inventory exists;
- artifact classification exists;
- semantic duplicate scan exists;
- root artifact report builders exist;
- preview tools exist;
- archival/location/semantic/container-boundary docs exist;
- Radar/X-Ray/provenance binding is complete;
- no auto-delete and no auto-move remain enforced.

## Dashboard rule

Dashboard may read:

- inventory status;
- location validation status;
- semantic duplicate status;
- acceptance status;
- next action.

Dashboard must not:

- delete files;
- move files;
- archive files;
- stage git files;
- commit changes;
- execute correction passes.
