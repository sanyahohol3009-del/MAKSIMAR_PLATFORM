# AI_ORCHESTRATION BATCH 5.1 Semantic Duplicate Resolution v1

## Batch

PHASE 5 / BATCH 5.1 — AI Orchestration Surface

## Scan result

The semantic duplicate scan detected high-risk overlap with existing AI, worker, control-plane, polyglot bridge and MemPalace-related surfaces.

This is expected because BATCH 5.1 introduces an orchestration surface that must bind to existing systems instead of duplicating them.

## Existing source surfaces

BATCH 5.1 must account for these existing surfaces:

- AI_SERVICES/
- MAKSIMAR_CORE_LIB/ai_services/
- MAKSIMAR_CORE_LIB/real_ai_services_model_adapters/
- MAKSIMAR_CORE_LIB/workers_registry/
- MAKSIMAR_CORE_LIB/workers_runtime/
- MAKSIMAR_SERVER/WORKERS/
- MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding/
- MAKSIMAR_SERVER/POLYGLOT_MODEL_WORKER_BRIDGE/
- historical MemPalace PHASE 5.1 adapter documents

## Target classification

| Target path | Decision | Reason |
|---|---|---|
| AI_ORCHESTRATION/README.md | create surface documentation only | Documents orchestration boundary; does not define AI service implementation. |
| AI_ORCHESTRATION/container_contract.yaml | create inert container contract | Declares no execution, no deployment, no public exposure, no runtime mutation. |
| AI_ORCHESTRATION/config/ai_orchestration_policy.yaml | create policy surface only | Defines proposal/stage blocking rules; does not execute proposals or stages. |
| MAKSIMAR_CORE_LIB/ai_orchestration/__init__.py | package facade only | Exports BATCH 5.1 read models only; does not duplicate ai_services, workers or router. |
| MAKSIMAR_SERVER/AI_ORCHESTRATION/__init__.py | server namespace facade only | Keeps runtime namespace inert; no service startup, no worker startup, no router execution. |
| AI_ORCHESTRATION/layer_manifest.yaml | create layer manifest only | Registers the orchestration surface and existing bindings. |
| AI_ORCHESTRATION/boundaries/container_adapter_boundary.yaml | create boundary declaration only | Documents adapter/container boundary; no Docker/Compose deployment. |
| AI_ORCHESTRATION/existing_bindings/ai_services_binding.yaml | binding only | References existing AI_SERVICES and MAKSIMAR_CORE_LIB/ai_services. |
| AI_ORCHESTRATION/existing_bindings/worker_binding.yaml | binding only | References existing workers_registry, workers_runtime and MAKSIMAR_SERVER/WORKERS. |
| AI_ORCHESTRATION/existing_bindings/control_plane_ai_router_binding.yaml | binding only | References existing CONTROL_PLANE ai_router_binding. |
| MAKSIMAR_CORE_LIB/ai_orchestration/existing_ai_orchestration_binding_models.py | read-model/binding models only | Exposes AIOrchestrationSurfaceReadModel and ExistingAIOrchestrationBindingReadModel. |
| tests/ai_orchestration/test_existing_ai_orchestration_binding_models_smoke.py | smoke test only | Verifies binding/read-model invariants. |

## Explicit non-duplication rules

BATCH 5.1 must not create:

- new AI service registry;
- new model adapter layer;
- new worker registry;
- new worker runtime;
- new control-plane router;
- new ai_router_binding implementation;
- new MemPalace integration;
- new proposal executor;
- new stage executor;
- new autonomous execution path.

## Safety rules

BATCH 5.1 remains:

- read-model only;
- binding only;
- proposal/stage blocked;
- no direct autonomous execution;
- no runtime mutation;
- no production deployment;
- no active Docker deployment;
- no active Compose deployment;
- no public exposure;
- dashboard-safe.

## Resolution decision

The detected high-risk items are accepted only as binding/facade/surface targets.

No existing source is moved, deleted, migrated or replaced.

semantic_duplicate_resolution_ready: true
