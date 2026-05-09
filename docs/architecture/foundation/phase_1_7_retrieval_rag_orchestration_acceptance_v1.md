# PHASE 1.7 — Retrieval / RAG Orchestration Acceptance v1

## Статус

PHASE 1.7 принята.

Слой Retrieval / RAG Orchestration собран как control-plane routing / policy / evidence / registry-binding / observability / backend-policy gate.

## Принятые batch-блоки

### Batch 1 — Retrieval Routing Core Contract

Создан слой:

- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/

Результат:

- selected_source_count: 6
- evidence_item_count: 6
- citation_required_items: 6
- conflict_marked_items: 0
- policy_gate_passed: True
- backend_execution_required: False
- route_ready: True
- preview_trace_ready: True
- preview_ready: True

### Batch 2 — Registry / AI Router / Observability Binding

Создан binding между:

- memory_routing
- MEMORY_REGISTRY
- global_registry
- ai_router_binding
- memory_skill_metrics

Результат:

- registry_total_bindings: 4
- registry_ready_bindings: 4
- selected_by_retrieval_bindings: 3
- observability_metrics_total_entries: 5
- observability_router_binding_entries: 3
- registry_binding_ready: True
- observability_ready: True
- trace_binding_ready: True
- batch2_ready: True
- preview_ready: True

### Batch 3 — Final Retrieval Readiness / Backend Policy Gate

Добавлены final gates:

- retrieval backend policy gate
- retrieval phase readiness gate

Результат:

- selected_source_count: 6
- evidence_item_count: 6
- registry_total_bindings: 4
- registry_ready_bindings: 4
- observability_router_binding_entries: 3
- approved_backends: 4
- blocked_backends: 2
- route_ready: True
- preview_ready: True
- batch2_ready: True
- registry_binding_ready: True
- observability_ready: True
- trace_ready: True
- backend_policy_ready: True
- mgrep_blocked: True
- sqlite_vec_blocked: True
- backend_execution_allowed: False
- phase_ready: True

## Flow

retrieval_request
-> retrieval_scope
-> source_selection_policy
-> evidence_pack
-> registry_ai_observability_binding
-> backend_policy_gate
-> preview_trace
-> phase_readiness

## Переиспользовано

- MAKSIMAR_SERVER/MEMORY_REGISTRY/
- MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding/
- MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/
- MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/
- MAKSIMAR_CORE_LIB/memory_engine/history_binding/
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/
- MAKSIMAR_CORE_LIB/memory_engine/media_memory/

## Добавлено в Batch 3

Новые файлы:

- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_backend_policy_gate.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_phase_readiness_gate.py

Новые тесты:

- tests/retrieval_orchestration/test_retrieval_backend_policy_gate_smoke.py
- tests/retrieval_orchestration/test_retrieval_backend_policy_blocks_mgrep_sqlite_vec_smoke.py
- tests/retrieval_orchestration/test_retrieval_phase_readiness_gate_smoke.py
- tests/retrieval_orchestration/test_retrieval_phase_1_7_ready_smoke.py
- tests/retrieval_orchestration/test_retrieval_phase_1_7_no_backend_execution_smoke.py

## Жёсткие правила

PHASE 1.7 не выполняет retrieval backend.

PHASE 1.7 не вызывает mgrep.

PHASE 1.7 не вызывает sqlite-vec.

PHASE 1.7 не создаёт vector database.

PHASE 1.7 не пишет memory.

PHASE 1.7 не пишет artifacts.

PHASE 1.7 не читает raw binary payloads.

PHASE 1.7 не обходит policy gate.

PHASE 1.7 использует только accepted internal contracts как routing sources.

mgrep и sqlite-vec зафиксированы как future experimental backend adapters, не как core.

## Проверки

Принятые результаты:

- PHASE 1.7 Batch 3 local tests: 27 passed
- related pack: 398 passed
- full auto parallel: 1812 passed

Warnings не являются blocker, так как относятся к pytest-benchmark / xdist / multiprocessing fork under parallel test execution.

## Acceptance

PHASE 1.7 считается принятой, если:

- retrieval route is ready;
- preview is ready;
- evidence pack is built;
- registry binding is ready;
- observability binding is ready;
- trace binding is ready;
- backend policy gate is ready;
- mgrep_blocked=True;
- sqlite_vec_blocked=True;
- backend_execution_allowed=False;
- phase_ready=True;
- full auto parallel remains green.
