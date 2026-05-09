# PHASE 2.1 Batch 1 — Evidence Source Chain Binding Acceptance v1

## Статус

PHASE 2.1 Batch 1 принят.

Слой Evidence Source Chain Binding реализован в existing control-plane routing layer:

- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/

Новый root не создавался.

## Решение

Batch 1 связывает retrieval evidence pack с:

- source binding
- provenance binding
- trace binding
- citation gate
- conflict gate
- dashboard read-only visibility

## Добавлено

Новые файлы:

- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/evidence_source_chain_models.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/evidence_source_chain_builder.py
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/evidence_source_chain_preview.py

Изменено:

- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/__init__.py

Новые тесты:

- tests/retrieval_orchestration/test_evidence_source_chain_models_smoke.py
- tests/retrieval_orchestration/test_evidence_source_chain_builder_smoke.py
- tests/retrieval_orchestration/test_evidence_source_chain_preview_smoke.py
- tests/retrieval_orchestration/test_evidence_source_chain_citation_gate_smoke.py
- tests/retrieval_orchestration/test_evidence_source_chain_conflict_gate_smoke.py
- tests/retrieval_orchestration/test_evidence_source_chain_backend_policy_smoke.py
- tests/retrieval_orchestration/test_phase_2_1_batch1_evidence_source_chain_ready_smoke.py

## Принятые результаты

Evidence Source Chain:

- total_items: 6
- source_bound_items: 6
- provenance_bound_items: 6
- trace_bound_items: 6
- citation_required_items: 6
- conflict_marked_items: 0
- dashboard_visible_items: 6
- ready_items: 6
- retrieval_phase_ready: True
- storage_phase_ready: True
- media_phase_ready: True
- architecture_control_ready: True
- mgrep_blocked: True
- sqlite_vec_blocked: True
- backend_execution_allowed: False

## Evidence items

Accepted evidence chain entries:

- evidence_history_ingestion
- evidence_history_binding
- evidence_storage_registry
- evidence_media_memory
- evidence_memory_registry
- evidence_ai_router_binding

## Flow

retrieval_evidence_pack
-> source_binding
-> provenance_binding
-> trace_binding
-> citation_gate
-> conflict_gate
-> dashboard_read_only_visibility
-> evidence_source_chain_ready

## Жёсткие правила

PHASE 2.1 Batch 1 is read-only.

PHASE 2.1 Batch 1 does not mutate memory.

PHASE 2.1 Batch 1 does not mutate registry.

PHASE 2.1 Batch 1 does not call retrieval backend.

PHASE 2.1 Batch 1 does not call mgrep.

PHASE 2.1 Batch 1 does not call sqlite-vec.

PHASE 2.1 Batch 1 does not create vector database.

PHASE 2.1 Batch 1 does not create network surfaces.

PHASE 2.1 Batch 1 does not change network segmentation or trust boundaries.

mgrep and sqlite-vec remain blocked future backend adapters.

## Проверки

Принятые результаты:

- PHASE 2.1 Batch 1 local tests: 34 passed
- related pack: 417 passed
- full auto parallel: 1846 passed

Warnings не являются blocker, так как относятся к pytest-benchmark / xdist / multiprocessing fork under parallel test execution.

## Acceptance

Batch 1 считается принятым, если:

- evidence source chain contract builds;
- evidence source chain preview builds;
- all evidence items are source-bound;
- all evidence items are provenance-bound;
- all evidence items are trace-bound;
- all evidence items require citation;
- conflict_marked_items == 0;
- all evidence items are dashboard-visible;
- all evidence chain entries are ready;
- mgrep_blocked=True;
- sqlite_vec_blocked=True;
- backend_execution_allowed=False;
- full auto parallel remains green.
