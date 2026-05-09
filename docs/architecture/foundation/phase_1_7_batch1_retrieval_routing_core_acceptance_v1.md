# PHASE 1.7 Batch 1 — Retrieval Routing Core Contract Acceptance v1

## Статус

PHASE 1.7 Batch 1 принят.

Создан первый core слой Retrieval Orchestration / RAG Routing:

- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/

## Решение

Создан control-plane memory routing layer.

Это не отдельный RAG backend.

Это не vector database.

Это не mgrep adapter.

Это не sqlite-vec adapter.

Это routing / policy / source selection / evidence pack / preview trace слой.

## Переиспользовано

- MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding/
- MAKSIMAR_SERVER/MEMORY_REGISTRY/
- MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/
- MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/
- MAKSIMAR_CORE_LIB/memory_engine/history_binding/
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/
- MAKSIMAR_CORE_LIB/memory_engine/media_memory/

## Добавлено

Новые файлы:

- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/__init__.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_request_models.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_scope_models.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_source_binding_models.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_evidence_pack_models.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_selection_policy.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_router.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_trace_builder.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_summary_builder.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_preview_builder.py

Новые тесты:

- tests/retrieval_orchestration/test_retrieval_request_models_smoke.py
- tests/retrieval_orchestration/test_retrieval_scope_models_smoke.py
- tests/retrieval_orchestration/test_retrieval_source_binding_models_smoke.py
- tests/retrieval_orchestration/test_retrieval_evidence_pack_smoke.py
- tests/retrieval_orchestration/test_retrieval_selection_policy_smoke.py
- tests/retrieval_orchestration/test_retrieval_policy_blocks_forbidden_source_smoke.py
- tests/retrieval_orchestration/test_retrieval_router_smoke.py
- tests/retrieval_orchestration/test_retrieval_trace_smoke.py
- tests/retrieval_orchestration/test_retrieval_summary_smoke.py
- tests/retrieval_orchestration/test_retrieval_preview_smoke.py
- tests/retrieval_orchestration/test_retrieval_blocks_unapproved_backend_smoke.py
- tests/retrieval_orchestration/test_retrieval_batch1_ready_smoke.py

## Preview result

Confirmed:

- selected_source_count: 6
- evidence_item_count: 6
- citation_required_items: 6
- conflict_marked_items: 0
- policy_gate_passed: True
- backend_execution_required: False
- route_ready: True
- preview_trace_ready: True
- preview_ready: True

## Flow

query
-> intent
-> domain_scope
-> policy_gate
-> source_priority
-> retrieval_source
-> evidence_pack
-> preview_trace

## Жёсткие правила

Batch 1 не выполняет retrieval backend.

Batch 1 не вызывает mgrep.

Batch 1 не вызывает sqlite-vec.

Batch 1 не создаёт vector database.

Batch 1 не пишет memory.

Batch 1 не пишет artifacts.

Batch 1 не читает raw binary payloads.

Batch 1 не обходит policy gate.

Batch 1 блокирует unapproved backend на уровне model boundary.

Batch 1 создаёт только deterministic read-only routing / evidence / preview contract.

## Проверки

Принятые результаты:

- py_compile: passed
- PHASE 1.7 local tests: 12 passed
- related pack: 382 passed
- full auto parallel: 1797 passed

Warnings не являются blocker, так как относятся к pytest-benchmark / xdist / multiprocessing fork under parallel test execution.

## Acceptance

Batch 1 считается принятым, если:

- retrieval request builds;
- retrieval scope builds;
- retrieval source bindings build;
- retrieval evidence pack builds;
- forbidden source is blocked;
- unapproved backend is blocked;
- selected sources are priority-sorted;
- evidence pack requires citations;
- route_ready=True;
- preview_ready=True;
- backend_execution_required=False;
- full auto parallel remains green.
