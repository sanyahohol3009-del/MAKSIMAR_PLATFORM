# AI_ORCHESTRATION BATCH 5.5 Semantic Duplicate Resolution v1

## Batch

PHASE 5 / BATCH 5.5 — Tests + Final AI Entry Acceptance

## Scan result

The semantic duplicate scan reported true duplicate / high-risk findings.

Single target isolation narrowed the high-risk targets to:

- MAKSIMAR_CORE_LIB/ai_orchestration/ai_router_binding_contract.py
- tests/ai_orchestration/test_ai_router_binding_contract_smoke.py

Detected isolated counts for each target:

- true_duplicate_risk_count: 1
- high_risk_count: 1
- migration_candidate_count: 48
- wrap_as_adapter_count: 64

## Existing related surfaces

Existing related surfaces include:

- MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding/ai_router_binding_contract.py
- MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding/ai_router_binding_models.py
- tests/ai_router_binding/test_ai_router_binding_contract_smoke.py
- AI_ORCHESTRATION/existing_bindings/control_plane_ai_router_binding.yaml
- MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/control_plane_ai_router_adapter.py

## Resolution

The new target `MAKSIMAR_CORE_LIB/ai_orchestration/ai_router_binding_contract.py` is classified as an AI_ORCHESTRATION acceptance/accounting contract.

It must not duplicate, replace, move or reimplement the existing CONTROL_PLANE ai router binding.

It may only account for the existing router binding as part of final AI_ORCHESTRATION acceptance.

## Target classification

| Target path | Decision | Reason |
|---|---|---|
| MAKSIMAR_CORE_LIB/ai_orchestration/ai_router_binding_contract.py | create acceptance/accounting contract only | Required by BATCH 5.5 to account for existing ai_router_binding; not a router implementation. |
| tests/ai_orchestration/test_ai_router_binding_contract_smoke.py | create AI_ORCHESTRATION-scoped acceptance test only | Confirms accounting and no duplication; must not duplicate CONTROL_PLANE router test logic. |

## Non-migration rule

BATCH 5.5 must not move, delete, replace or migrate existing:

- MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding/*
- tests/ai_router_binding/*
- AI_ORCHESTRATION existing bindings
- BATCH 5.4 runtime adapters
- AI_SERVICES
- MAKSIMAR_SERVER/WORKERS
- ACTION_LIBRARY
- WORKFLOW_ENGINE

## Safety rules

BATCH 5.5 remains:

- acceptance/read-model only;
- proposal-only;
- existing binding accounting only;
- no direct autonomous execution;
- no ACTION_LIBRARY direct execution;
- no WORKFLOW_ENGINE direct execution;
- no model runtime execution;
- no runtime mutation;
- no production deployment;
- no public exposure.

## Resolution decision

The high-risk targets are resolved by constraining the new ai_router_binding contract to AI_ORCHESTRATION final acceptance/accounting only.

No existing source is moved, deleted, migrated or replaced.

semantic_duplicate_resolution_ready: true
