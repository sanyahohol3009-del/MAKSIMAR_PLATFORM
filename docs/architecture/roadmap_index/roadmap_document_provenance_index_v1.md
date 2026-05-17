# Roadmap Document Provenance Index v1

## Purpose

This index labels roadmap documents by track so project discovery does not mix unrelated roadmap families.

## Current active track

roadmap_family: memory_roadmap_v5_1  
track_scope: memory  
current_phase_after: PHASE 5.2  
applies_to_current_track: true  

## Track labels

### memory_roadmap_v5_1

Applies to the current memory/governance/dashboard-memory roadmap.

Current confirmed closed:

- Original PHASE 4 — Memory Drift / Contradiction Candidate Readiness
- Original PHASE 5 — JARVIS Memory Self-Readability
- PHASE 5.1 — MemPalace Adapter Integration
- PHASE 5.2 — Final Dashboard Memory Map

### post_visual_operator_roadmap

Documents such as:

- docs/POST_VISUAL_PLATFORM_AND_SELF_AWARENESS_ROADMAP_v1.md
- docs/jarvis/dashboard_operator/JARVIS_PHASE_06_OPERATOR_INTERACTIVITY_CANONICAL.md
- docs/jarvis/dashboard_operator/JARVIS_PHASE_07_BASE_PANEL_CONTENT_CANONICAL.md
- docs/jarvis/dashboard_operator/JARVIS_PHASE_08_DISPLAY_RESTORE_MULTIMONITOR_CANONICAL.md
- docs/jarvis/main_operator/JARVIS_PHASE_09_REVIEW_SIMULATION_PREVIEW_CANONICAL.md
- docs/jarvis/main_operator/JARVIS_PHASE_10_MAIN_OPERATOR_FINAL_ASSEMBLY_CANONICAL.md
- docs/jarvis/main_operator/JARVIS_PHASE_11_MODULE_PRODUCT_FAMILY_CANONICAL.md
- docs/jarvis/main_operator/JARVIS_PHASE_12_FRONTEND_SHELL_REGISTRY_BINDING_CANONICAL.md
- docs/jarvis/main_operator/JARVIS_PHASE_13_VOICE_GESTURE_DISPLAY_HANDOFF_CANONICAL.md
- docs/jarvis/main_operator/JARVIS_PHASE_14_VISUAL_HUD_RENDERER_CANONICAL.md

These documents do not define the next step for memory_roadmap_v5_1.

### foundation_roadmap_v2_1_correction_patch

Applies to the current foundation-hardening track after memory foundation closure.

Canonical documents:

- docs/architecture/foundation/batched_foundation_roadmap_v2_1_correction_patch.json
- docs/architecture/foundation/batched_foundation_roadmap_schema_v1.json
- docs/architecture/foundation/foundation_roadmap_correction_patch_v1.md
- docs/architecture/foundation/root_artifact_hygiene_acceptance_v1.md

Current PHASE 0 purpose:

- cleanly classify root artifacts;
- prevent accidental delete/move;
- detect semantic duplicate risk;
- make preview output dashboard-ready;
- bind the foundation roadmap to CI, Radar and X-Ray.

Rules:

- This track must be checked by `tools/foundation_roadmap_ci_check.py`.
- This track does not reopen closed memory roadmap phases.
- This track must not replace visual/operator roadmap documents.
- Each batch must be committed separately.

### history_ingestion_track

Documents generated while importing previous chats/history into project memory.

These documents may be useful for project memory and continuity, but they do not define the next step for memory_roadmap_v5_1 unless explicitly marked.

## Rules

- A roadmap document must have a track label before being used as next-step evidence.
- Visual/operator canonical phase docs must not be treated as memory roadmap next steps.
- History-ingestion artifacts must not replace active memory roadmap phases.
- External extensions such as MemPalace must not replace original roadmap blocks.
