# AI_ORCHESTRATION BATCH 5.2 Semantic Duplicate Resolution v1

## Batch

PHASE 5 / BATCH 5.2 — Model Router + Request/Response Contracts

## Scan result

The semantic duplicate scan detected overlap with existing action, workflow, router, proposal, audit, self-expansion and workflow test surfaces.

Detected counts:

- true_duplicate_risk_count: 7
- high_risk_count: 7
- migration_candidate_count: 116
- wrap_as_adapter_count: 37

The single target risk isolation identified:

- tests/ai_orchestration/__init__.py

## Existing source surfaces

BATCH 5.2 must account for these existing surfaces:

- ACTION_LIBRARY/
- WORKFLOW_ENGINE/
- MAKSIMAR_CORE_LIB/workflow_engine/
- MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding/
- MAKSIMAR_SERVER/POLYGLOT_MODEL_WORKER_BRIDGE/
- MAKSIMAR_SERVER/PROPOSAL_AUDIT/
- MAKSIMAR_SERVER/SELF_EXPANSION_GATE/
- MAKSIMAR_CORE_LIB/evolution_debug/
- MAKSIMAR_CORE_LIB/evolution_loop/
- tests/workflow_engine/
- tests/ai_router_binding/
- tests/polyglot_model_worker_bridge/
- tests/proposal_audit_spine/
- tests/self_expansion_gate/

## Target classification

| Target path | Decision | Reason |
|---|---|---|
| MAKSIMAR_CORE_LIB/ai_orchestration/model_router_contract.py | create contract/read-model only | Defines routing contract; does not execute model calls or actions. |
| MAKSIMAR_CORE_LIB/ai_orchestration/model_request_models.py | create request model only | Describes request shape; no execution. |
| MAKSIMAR_CORE_LIB/ai_orchestration/model_response_models.py | create response model only | Describes response shape; no execution. |
| MAKSIMAR_CORE_LIB/ai_orchestration/agent_plan_models.py | create proposal-only plan model | Agent plan is not an executable workflow. |
| MAKSIMAR_CORE_LIB/ai_orchestration/tool_call_boundary_models.py | create proposal boundary only | Tool calls are blocked by default and cannot directly execute ACTION_LIBRARY or WORKFLOW_ENGINE. |
| tests/ai_orchestration/__init__.py | package marker only | Required test package marker; does not duplicate existing test semantics. |
| tests/ai_orchestration/test_model_router_contract_smoke.py | smoke test only | Verifies router contract/read-model invariants. |
| tests/ai_orchestration/test_model_request_models_smoke.py | smoke test only | Verifies request model invariants. |
| tests/ai_orchestration/test_model_response_models_smoke.py | smoke test only | Verifies response model invariants. |
| tests/ai_orchestration/test_agent_plan_models_smoke.py | smoke test only | Verifies proposal-only agent plan invariants. |
| tests/ai_orchestration/test_tool_call_boundary_models_smoke.py | smoke test only | Verifies tool-call boundary invariants. |
| tests/ai_orchestration/test_tool_call_boundary_blocks_direct_execution_smoke.py | correction smoke test only | Verifies direct action/workflow execution remains blocked. |

## Explicit non-duplication rules

BATCH 5.2 must not create:

- new ACTION_LIBRARY implementation;
- new WORKFLOW_ENGINE implementation;
- new workflow runtime;
- new ai_router_binding runtime;
- new model worker bridge runtime;
- new proposal audit spine;
- new self-expansion execution path;
- new autonomous execution path.

## Safety rules

BATCH 5.2 remains:

- contract/model only;
- read-model only;
- proposal-boundary only;
- tool_call_allowed=false by default;
- execution_allowed=false by default;
- no direct ACTION_LIBRARY execution;
- no direct WORKFLOW_ENGINE execution;
- no direct autonomous execution;
- no runtime mutation;
- no production deployment;
- no public exposure;
- dashboard-safe.

## Resolution decision

The detected high-risk items are accepted only as contract/model/test-package-marker targets.

No existing source is moved, deleted, migrated or replaced.

semantic_duplicate_resolution_ready: true
