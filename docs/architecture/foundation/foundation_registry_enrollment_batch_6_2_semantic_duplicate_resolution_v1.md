# Foundation Registry Enrollment BATCH 6.2 Semantic Duplicate Resolution v1

## Batch

PHASE 6 / BATCH 6.2 - Security + Data Plane Enrollment

## Scan result

The semantic duplicate scan reported no true duplicate or high-risk targets.

Counts:

- true_duplicate_risk_count: 0
- high_risk_count: 0
- migration_candidate_count: 257
- wrap_as_adapter_count: 210
- keep_legacy_count: 2
- create_new_count: 0

## Resolution

No single-target isolation is required because true_duplicate_risk_count and high_risk_count are both zero.

The migration candidates are resolved by constraining BATCH 6.2 to read-model builder behavior only.

## Target classification

| Target path | Decision | Reason |
|---|---|---|
| MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_security_enrollment_builder.py | create builder/read-model only | Makes existing Security Layer registry-visible without replacing security_layer surfaces. |
| MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_data_plane_enrollment_builder.py | create builder/read-model only | Makes existing Data Plane registry-visible without replacing data_plane surfaces. |
| tests/foundation_registry_enrollment/test_foundation_security_enrollment_builder_smoke.py | create smoke test | Verifies Security Layer registry visibility remains read-only and non-mutating. |
| tests/foundation_registry_enrollment/test_foundation_data_plane_enrollment_builder_smoke.py | create smoke test | Verifies Data Plane registry visibility remains read-only and non-mutating. |

## Non-replacement rule

BATCH 6.2 must not replace, migrate, delete, rename or move existing:

- SECURITY_LAYER/*
- DATA_PLANE/*
- MAKSIMAR_CORE_LIB/security_layer/*
- MAKSIMAR_CORE_LIB/data_plane/*
- MAKSIMAR_SERVER/SECURITY_LAYER/*
- MAKSIMAR_SERVER/DATA_PLANE/*
- tests/security_layer/*
- tests/data_plane/*

## Builder constraints

The new builders may only:

- read existing foundation registry enrollment models;
- bind existing Security Layer visibility;
- bind existing Data Plane visibility;
- expose read-only dashboard-safe read models;
- prove registry visibility through tests.

The new builders must not:

- write registry state;
- trigger auto-enrollment writes;
- mutate runtime;
- duplicate Security Layer logic;
- duplicate Data Plane logic;
- call SECURITY_LAYER runtime directly;
- call DATA_PLANE runtime directly;
- deploy containers;
- expose public endpoints.

## Safety state

semantic_duplicate_resolution_ready: true
single_target_isolation_required: false
registry_write_allowed: false
auto_enrollment_write_allowed: false
runtime_mutation_allowed: false
dashboard_safe: true
