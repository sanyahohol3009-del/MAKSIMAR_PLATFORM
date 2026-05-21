# AI_ORCHESTRATION Existing Binding Review v1

## Scope

This document closes the existing binding review for PHASE 5 / BATCH 5.5.

AI_ORCHESTRATION accounts for existing platform surfaces. It does not replace them.

## Existing surfaces accounted

- AI_SERVICES
- MAKSIMAR_SERVER/WORKERS
- CONTROL_PLANE ai router binding
- AI_ORCHESTRATION/existing_bindings/ai_services_binding.yaml
- AI_ORCHESTRATION/existing_bindings/worker_binding.yaml
- AI_ORCHESTRATION/existing_bindings/control_plane_ai_router_binding.yaml
- MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/ai_services_adapter.py
- MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/workers_adapter.py
- MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/control_plane_ai_router_adapter.py

## Binding decisions

| Surface | Decision |
|---|---|
| AI_SERVICES | Account existing service surface only. |
| MAKSIMAR_SERVER/WORKERS | Account existing worker surface only. |
| CONTROL_PLANE ai router binding | Account existing router binding only. |
| ACTION_LIBRARY | No direct execution. |
| WORKFLOW_ENGINE | No direct execution. |

## Non-duplication rules

AI_ORCHESTRATION must not duplicate:

- AI_SERVICES implementation logic;
- worker implementation logic;
- CONTROL_PLANE router implementation logic;
- ACTION_LIBRARY execution logic;
- WORKFLOW_ENGINE execution logic.

## Acceptance state

existing_ai_services_accounted: true  
existing_workers_accounted: true  
existing_ai_router_binding_accounted: true  
direct_execution_blocked: true  
proposal_only: true
