# AI_ORCHESTRATION BATCH 5.4 Semantic Duplicate Resolution v1

## Batch

PHASE 5 / BATCH 5.4 — Runtime Adapter + Preview

## Scan result

The semantic duplicate scan reported true duplicate / high-risk findings.

Single target isolation narrowed the true high-risk target to:

- MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/__init__.py

Detected isolated counts:

- true_duplicate_risk_count: 40
- high_risk_count: 40
- migration_candidate_count: 34
- wrap_as_adapter_count: 43
- container_boundary_duplicate_allowed_count: 7

## Resolution

The target `MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/__init__.py` is classified as a package marker / export facade only.

It must not contain:

- adapter implementation logic;
- runtime execution logic;
- model execution logic;
- ACTION_LIBRARY execution logic;
- WORKFLOW_ENGINE execution logic;
- runtime mutation logic;
- deployment logic;
- duplicate AI services logic;
- duplicate workers logic;
- duplicate CONTROL_PLANE ai router logic.

## Target classification

| Target path | Decision | Reason |
|---|---|---|
| MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/__init__.py | create package marker / export facade only | Required package boundary for normalized adapters; no implementation duplication allowed. |
| MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/ai_services_adapter.py | create adapter facade only | Points to existing AI services; does not duplicate them. |
| MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/workers_adapter.py | create adapter facade only | Points to existing workers; does not duplicate them. |
| MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/control_plane_ai_router_adapter.py | create adapter facade only | Points to existing control-plane AI router binding; does not duplicate it. |

## Non-migration rule

BATCH 5.4 must not move, delete, replace or migrate existing:

- AI_SERVICES;
- MAKSIMAR_SERVER/WORKERS;
- CONTROL_PLANE;
- existing AI router bindings;
- existing BATCH 5.1 binding models;
- existing BATCH 5.2 router/request/response contracts;
- existing BATCH 5.3 proposal/provenance/budget/feedback contracts.

## Safety rules

BATCH 5.4 remains:

- runtime-adapter facade only;
- preview/read-model only;
- proposal-only;
- no direct autonomous execution;
- no direct ACTION_LIBRARY execution;
- no direct WORKFLOW_ENGINE execution;
- no model runtime execution;
- no runtime mutation;
- no production deployment;
- no public exposure.

## Resolution decision

The high-risk target is resolved by constraining `adapters/__init__.py` to package-marker/export-facade behavior only.

No existing source is moved, deleted, migrated or replaced.

semantic_duplicate_resolution_ready: true
