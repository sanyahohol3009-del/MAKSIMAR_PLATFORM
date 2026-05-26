# PHASE 0 — Readiness / Scanner / Output Hygiene Acceptance v1

Status: accepted after Batch 0.8.

This document closes PHASE 0 of the MAKSIMAR Roadmap v4.2 project readiness and output hygiene track.

## Scope

PHASE 0 established the project readiness control foundation.

It covers:

- existing scanner discovery;
- repository scan contract models;
- repository scan runtime facade;
- pytest output hygiene;
- project readiness runner core;
- project readiness sub-runners;
- dashboard-safe readiness JSON export;
- PHASE 0 final acceptance.

## Closed batches

| Batch | Name | Status |
|---|---|---|
| 0.1 | Existing Scanner Discovery | READY |
| 0.2 | Repository Scan Models | READY |
| 0.3 | Repository Scan Runtime | READY |
| 0.4 | Pytest Output Hygiene | READY |
| 0.5 | Project Readiness Runner Core | READY |
| 0.6 | Project Readiness Sub-Runners | READY |
| 0.7 | Readiness Runtime JSON + Dashboard Export | READY |
| 0.8 | PHASE 0 Acceptance | READY |

## Acceptance evidence

The following readiness surfaces are required and present:

- `tools/project_readiness_control/project_file_readiness_map.py`
- `tools/project_readiness_control/roadmap_expected_files_registry.py`
- `tools/project_readiness_control/scanner_discovery.py`
- `tools/project_readiness_control/run_readiness_gate.py`
- `tools/project_readiness_control/target_test_runner.py`
- `tools/project_readiness_control/batch_gate_runner.py`
- `tools/project_readiness_control/full_platform_auto_runner.py`
- `tools/project_readiness_control/surface_inventory.py`
- `tools/project_readiness_control/semantic_duplicate_scan_runner.py`
- `tools/project_readiness_control/roadmap_ci_runner.py`
- `tools/project_readiness_control/forbidden_marker_scan.py`
- `tools/project_readiness_control/xray_runner.py`
- `tools/project_readiness_control/drift_guard_runner.py`
- `tools/project_readiness_control/dirty_surface_classifier.py`
- `tools/project_readiness_control/acceptance_evidence_collector.py`
- `tools/project_readiness_control/dashboard_readiness_export.py`
- `MAKSIMAR_CORE_LIB/readiness_control/readiness_status_read_model.py`

## Architectural constraints

PHASE 0 acceptance is constrained by the following rules:

- no duplicate scanner world;
- no duplicate roadmap checker;
- no duplicate drift checker;
- no duplicate X-Ray engine;
- no duplicate semantic duplicate engine;
- no full-platform reports during ordinary target pytest;
- no auto-fix;
- no repository mutation by readiness runners;
- no dashboard mutation;
- no UI-to-execution path;
- no direct production deployment;
- no public network exposure;
- generated runtime/dashboard JSON is export-only and not canonical source.

## Scanner and repository security

The canonical scanner surface remains:

- `tools/vendor_security_gate.py`

Batch 0.1 only discovers and binds the existing scanner surface.

Batch 0.2 defines repository scan contracts and quarantine policy.

Batch 0.3 adds a thin server runtime facade that maps already-produced vendor gate payloads into canonical repository scan contracts. It does not execute scanners directly.

## Pytest output hygiene

Target pytest runs remain quiet by default.

Full platform reports are enabled only when explicitly requested through:

- `MAKSIMAR_FULL_PLATFORM_REPORTS=1`
- `--maksimar-full-platform-reports`

## Dashboard readiness export

Batch 0.7 exposes dashboard-safe readiness data through a read-only model and generated JSON export.

The export is not a dashboard root and not an execution channel.

Required constraints:

- `dashboard_safe: true`
- `read_only: true`
- `runtime_mutation_allowed: false`
- `canonical_write_allowed: false`
- `dashboard_mutation_allowed: false`
- `ui_to_execution_allowed: false`

## Final acceptance gate

PHASE 0 is accepted only when:

- Batch 0.1 through 0.8 are registered;
- Batch 0.1 through 0.8 are READY;
- all expected files are present;
- target PHASE 0 acceptance smoke test passes;
- pre-push roadmap drift check passes;
- unrelated dirty surfaces remain uncommitted unless explicitly approved.

## Current unrelated dirty surfaces

The known unrelated dirty/untracked surfaces are intentionally outside PHASE 0 acceptance and must not be blindly committed:

- `.pymon`
- `EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_controlled_real_backend_probe_report.json`
- `MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS/final_memory_map/final_memory_graph_builder.py`
- `tests/final_memory_map/*`
- `tests/oob_dashboard/*`
- `tests/oob_truth/*`
- `tests/roadmap_index/test_roadmap_document_provenance_check_smoke.py`
- `tests/runtime_core/*`
- `tests/voice_display_handoff/*`
- `tests/voice_routing/*`
- `tools/architecture_radar.py`
- `tools/architecture_radar_v2.py`
- `tools/export_oob_dashboard_state_snapshot_to_frontend_ts.py`
- `tools/export_oob_topology_payloads_to_frontend_ts.py`
- `tools/roadmap_document_provenance_check.py`

## Acceptance statement

PHASE 0 is accepted as a readiness, scanner, and output hygiene foundation.

It prepares the project for subsequent roadmap phases without replacing existing scanner, roadmap, drift, X-Ray, semantic duplicate, dashboard, or security surfaces.
