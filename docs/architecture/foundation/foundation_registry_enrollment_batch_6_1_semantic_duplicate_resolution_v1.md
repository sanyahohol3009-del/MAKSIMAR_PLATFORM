# Foundation Registry Enrollment BATCH 6.1 Semantic Duplicate Resolution v1

## Batch

PHASE 6 / BATCH 6.1 - Registry Enrollment Core Models

## Scan result

The semantic duplicate scan reported true duplicate / high-risk findings.

Single target isolation narrowed the high-risk target to:

- MAKSIMAR_CORE_LIB/foundation_registry_enrollment/__init__.py

Detected isolated counts:

- true_duplicate_risk_count: 13
- high_risk_count: 13
- migration_candidate_count: 40
- wrap_as_adapter_count: 22

## Resolution

The target `MAKSIMAR_CORE_LIB/foundation_registry_enrollment/__init__.py` is classified as a package marker / export facade only.

It must not contain:

- registry runtime implementation logic;
- auto-enrollment logic;
- registry write logic;
- memory registry logic;
- module manifest logic;
- skill/domain binding logic;
- dashboard registry logic;
- migration logic;
- deletion or move logic;
- runtime mutation logic.

## Target classification

| Target path | Decision | Reason |
|---|---|---|
| MAKSIMAR_CORE_LIB/foundation_registry_enrollment/__init__.py | create package marker / export facade only | Required package boundary for foundation registry enrollment models; no implementation duplication allowed. |
| MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_layer_manifest_models.py | create canonical model file | Defines foundation layer manifest model only. |
| MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_domain_enrollment_models.py | create canonical model file | Defines foundation domain enrollment model only. |
| MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_registry_binding_contract.py | create canonical contract/read model | Defines foundation registry enrollment contract only. |
| MAKSIMAR_CORE_LIB/foundation_registry_enrollment/foundation_dashboard_visibility_models.py | create dashboard-safe read model | Defines dashboard visibility model only. |

## Non-replacement rule

BATCH 6.1 must not replace, migrate, delete, rename or move existing:

- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/*
- MAKSIMAR_SERVER/MEMORY_REGISTRY/*
- MAKSIMAR_CORE_LIB/module_manifest/*
- MAKSIMAR_CORE_LIB/skill_domain_binding/*
- MAKSIMAR_CORE_LIB/oob_dashboard/*
- MAKSIMAR_CORE_LIB/workers_registry/*
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/*
- MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS/memory_registry_views/*
- docs/document_registry*
- docs/document_package_registry*

## Safety rules

BATCH 6.1 remains:

- contract/model only;
- read-model only;
- dashboard-safe;
- no runtime mutation;
- no registry write;
- no auto-enrollment write;
- no deployment;
- no public exposure.

## Resolution decision

The high-risk target is resolved by constraining `foundation_registry_enrollment/__init__.py` to package-marker/export-facade behavior only.

No existing source is moved, deleted, migrated or replaced.

semantic_duplicate_resolution_ready: true
