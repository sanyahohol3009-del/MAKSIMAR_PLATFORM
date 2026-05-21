# Foundation Registry Enrollment BATCH 6.4 Semantic Duplicate Resolution v1

## Batch

PHASE 6 / BATCH 6.4 - AI + Dashboard Visibility Enrollment

## Scan result

The semantic duplicate scan reported true/high-risk duplication only for:

- MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_layers/__init__.py

Counts from single-target isolation:

- true_duplicate_risk_count: 29
- high_risk_count: 29
- container_boundary_duplicate_allowed_count: 0
- wrap_as_adapter_count: 26
- migration_candidate_count: 46
- create_new_count: 0
- approval_required_count: 75

## Resolution

The high-risk target is resolved by constraining `foundation_layers/__init__.py` to package-boundary behavior only.

It must not define new foundation layer models, registries, manifests, readiness logic, dashboard visibility logic, or duplicate any existing foundation enrollment contracts.

The canonical foundation layer model source remains:

- MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_layer_manifest_models.py

The canonical domain enrollment source remains:

- MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_domain_enrollment_models.py

The canonical dashboard visibility source remains:

- MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_dashboard_visibility_models.py

BATCH 6.4 may create new builders only for AI orchestration enrollment, readiness summary, dashboard visibility summary and preview surfaces.

## Target classification

| Target path | Decision | Reason |
|---|---|---|
| MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_ai_orchestration_enrollment_builder.py | create builder/read-model only | Makes existing AI Orchestration foundation registry-visible without replacing AI_ORCHESTRATION surfaces. |
| MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_layers/__init__.py | package boundary / namespace facade only | Required by printed roadmap, but must not duplicate layer models, manifests or registry logic. |
| MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_layer_readiness_summary_builder.py | create builder/read-model only | Aggregates existing foundation enrollment readiness into a dashboard-safe read model. |
| MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_layer_dashboard_visibility_builder.py | create builder/read-model only | Aggregates mandatory dashboard visibility across foundation layers without UI execution. |
| tools/foundation_registry_enrollment_preview.py | create read-only preview tool | Emits registry enrollment preview only. |
| tools/foundation_layer_dashboard_visibility_preview.py | create read-only preview tool | Emits dashboard visibility preview only. |
| tests/foundation_registry_enrollment/test_foundation_ai_orchestration_enrollment_builder_smoke.py | create smoke test | Verifies AI orchestration registry visibility remains read-only and non-mutating. |
| tests/foundation_registry_enrollment/test_foundation_layer_readiness_summary_builder_smoke.py | create smoke test | Verifies readiness summary is complete and read-only. |
| tests/foundation_registry_enrollment/test_foundation_layer_dashboard_visibility_builder_smoke.py | create smoke test | Verifies dashboard visibility is mandatory and non-executing. |

## Non-replacement rule

BATCH 6.4 must not replace, migrate, delete, rename or move existing:

- AI_ORCHESTRATION/*
- MAKSIMAR_CORE_LIB/ai_orchestration/*
- MAKSIMAR_SERVER/AI_ORCHESTRATION/*
- MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_layer_manifest_models.py
- MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_domain_enrollment_models.py
- MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_dashboard_visibility_models.py
- MAKSIMAR_CORE_LIB/oob_dashboard/*
- MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS/*
- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/*
- existing tests/ai_orchestration/*
- existing tests/foundation_registry_enrollment/*

## Builder constraints

The new builders may only:

- read existing foundation registry enrollment models;
- bind existing AI Orchestration visibility;
- aggregate readiness across already-enrolled foundation layers;
- aggregate dashboard visibility across already-enrolled foundation layers;
- expose read-only dashboard-safe read models;
- emit preview-only output through tools;
- prove registry/dashboard visibility through tests.

The new builders and tools must not:

- write registry state;
- trigger auto-enrollment writes;
- mutate runtime;
- duplicate AI Orchestration logic;
- duplicate foundation layer manifest logic;
- duplicate dashboard execution logic;
- call AI runtime directly;
- call dashboard execution directly;
- deploy containers;
- expose public endpoints.

## Safety state

semantic_duplicate_resolution_ready: true
single_target_isolation_required: true
single_target_isolation_completed: true
foundation_layers_package_boundary_only: true
registry_write_allowed: false
auto_enrollment_write_allowed: false
runtime_mutation_allowed: false
dashboard_control_allowed: false
ai_execution_allowed: false
preview_tools_read_only: true
dashboard_safe: true
