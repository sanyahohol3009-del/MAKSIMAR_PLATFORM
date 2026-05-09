# PHASE 2.1 Batch 4 — CORE/SERVER Evidence Memory Binding Acceptance v1

## Статус

PHASE 2.1 Batch 4 принят.

SERVER evidence routing теперь связан с canonical CORE evidence memory layer.

## Размещение

CORE canonical layer:

- MAKSIMAR_CORE_LIB/evidence_memory/

SERVER binding layer:

- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/evidence_memory_core_binding.py

## Решение

Batch 4 связывает:

- CORE evidence memory
- SERVER evidence source chain
- evidence_id match
- artifact_ref match
- citation gate
- conflict clear gate
- memory truth gate
- knowledge graph projection gate
- read-only gate
- backend policy gate

## Добавлено

Новые файлы:

- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/evidence_memory_core_binding.py

Изменено:

- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/__init__.py

Новые тесты:

- tests/retrieval_orchestration/test_evidence_memory_core_binding_smoke.py
- tests/retrieval_orchestration/test_evidence_memory_core_id_match_smoke.py
- tests/retrieval_orchestration/test_evidence_memory_core_artifact_ref_match_smoke.py
- tests/retrieval_orchestration/test_evidence_memory_core_truth_projection_gate_smoke.py
- tests/retrieval_orchestration/test_evidence_memory_core_citation_conflict_gate_smoke.py
- tests/retrieval_orchestration/test_evidence_memory_core_backend_policy_smoke.py
- tests/retrieval_orchestration/test_evidence_memory_core_binding_preview_smoke.py
- tests/retrieval_orchestration/test_phase_2_1_batch4_core_binding_ready_smoke.py

## Принятые результаты

CORE/SERVER evidence memory binding:

- total_bindings: 6
- matched_evidence_items: 6
- artifact_ref_matched_bindings: 6
- citation_required_bindings: 6
- conflict_clear_bindings: 6
- memory_truth_bindings: 6
- knowledge_graph_projection_bindings: 6
- read_only_bindings: 6
- ready_bindings: 6
- server_phase_ready: True
- core_preview_ready: True
- mgrep_blocked: True
- sqlite_vec_blocked: True
- backend_execution_allowed: False

## Flow

core_evidence_memory
-> server_evidence_source_chain
-> evidence_id_match
-> artifact_ref_match
-> citation_gate
-> conflict_clear_gate
-> memory_truth_gate
-> knowledge_graph_projection_gate
-> read_only_gate
-> backend_policy_gate
-> core_server_binding_ready

## Жёсткие правила

Batch 4 is read-only.

Batch 4 does not mutate CORE evidence memory.

Batch 4 does not mutate SERVER routing.

Batch 4 does not execute retrieval backend.

Batch 4 does not call mgrep.

Batch 4 does not call sqlite-vec.

Batch 4 does not create vector database.

Batch 4 does not create network surfaces.

Knowledge graph remains projection-only.

CORE evidence memory remains canonical source.

SERVER memory_routing remains binding/readiness layer.

## Проверки

Принятые результаты:

- PHASE 2.1 Batch 4 local tests: 60 passed
- related pack: 443 passed
- full auto parallel: 1872 passed

Warnings не являются blocker, так как относятся к pytest-benchmark / xdist / multiprocessing fork under parallel test execution.

## Acceptance

Batch 4 считается принятым, если:

- CORE evidence ids match SERVER evidence ids;
- artifact_ref values match;
- all bindings require citation;
- all bindings are conflict-clear;
- all bindings mark memory_truth=True;
- all bindings mark knowledge_graph_projection_only=True;
- all bindings are read-only;
- all bindings are ready;
- mgrep_blocked=True;
- sqlite_vec_blocked=True;
- backend_execution_allowed=False;
- full auto parallel remains green.
