# AI_ORCHESTRATION

## Scope

AI_ORCHESTRATION is a surface and binding layer for existing AI, worker and control-plane router components.

It binds to existing sources:

- AI_SERVICES/
- MAKSIMAR_CORE_LIB/ai_services/
- MAKSIMAR_CORE_LIB/real_ai_services_model_adapters/
- MAKSIMAR_CORE_LIB/workers_registry/
- MAKSIMAR_CORE_LIB/workers_runtime/
- MAKSIMAR_SERVER/WORKERS/
- MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding/
- MAKSIMAR_SERVER/POLYGLOT_MODEL_WORKER_BRIDGE/

## Non-duplication rule

AI_ORCHESTRATION does not create a new AI service registry, model adapter layer, worker registry, worker runtime or control-plane router.

## Execution rule

This layer does not execute proposals, stages, workers, model calls or autonomous actions.

## Safety state

- direct_autonomous_execution_allowed: false
- proposal_execution_allowed: false
- stage_execution_allowed: false
- runtime_mutation_allowed: false
- production_deployment_allowed: false
- public_exposure_allowed: false
- dashboard_safe: true
