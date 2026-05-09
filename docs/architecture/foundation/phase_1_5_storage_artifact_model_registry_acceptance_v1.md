# PHASE 1.5 — Storage / Artifact / Model Registry Acceptance v1

## Статус

PHASE 1.5 принята.

Слой Storage / Artifact / Model Registry собран как read-only registry / binding / readiness layer.

## Принятые batch-блоки

### Batch 1 — Storage Registry Core Binding

Создан thin storage_registry layer:

- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/

Переиспользованы существующие storage primitives из history_ingestion:

- StorageNodeId
- StorageNode
- StorageRoot
- PortableStorageReference
- relocation / NAS readiness logic

Результат:

- total_entries: 5
- dashboard_visible_entries: 5
- retrieval_visible_entries: 3
- relocation_ready_entries: 5
- nas_ready_entries: 5
- storage_ready_for_m2_nas: True
- preview_ready: True
- flow_ready: True

### Batch 2 — Storage Registry / Artifact Routing Binding

Создан server-side binding между:

- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/
- MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/

DATA_PLANE как отдельная папка не создана на этом этапе.

Результат:

- total_entries: 3
- storage_required_entries: 1
- storage_ready_entries: 1
- data_plane_ready_entries: 1
- dashboard_visible_entries: 3
- binding_ready: True
- preview_ready: True

### Batch 3 — Final Dashboard / RAG / Portability Readiness Gate

Добавлены final readiness gates:

- CORE-side storage readiness
- SERVER-side artifact binding readiness

Результат CORE:

- total_entries: 5
- dashboard_visible_entries: 5
- retrieval_visible_entries: 3
- relocation_ready_entries: 5
- nas_ready_entries: 5
- m2_nas_ready: True
- artifact_collection_ready: True
- model_store_ready: True
- media_store_ready: True
- retrieval_index_ready: True
- phase_core_ready: True

Результат SERVER:

- storage_core_entries: 5
- artifact_binding_entries: 3
- storage_required_entries: 1
- storage_ready_entries: 1
- data_plane_ready_entries: 1
- dashboard_visible_entries: 3
- storage_core_ready: True
- artifact_binding_ready: True
- data_plane_route_ready: True
- dashboard_preview_ready: True
- phase_ready: True

## Flow

CORE flow:

history_ingestion_storage_primitives
-> storage_registry_contract
-> artifact_collection_reference
-> model_store_reference
-> media_artifact_reference
-> retrieval_index_reference
-> portability_policy
-> dashboard_read_only_preview

SERVER flow:

payload_classification
-> artifact_routing
-> storage_registry_lookup
-> artifact_collection_binding
-> data_plane_route_readiness
-> dashboard_read_only_preview

## Добавлено в Batch 3

Новые файлы:

- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/storage_registry_readiness_gate.py
- MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/storage_artifact_readiness_gate.py

Новые тесты:

- tests/storage_registry/test_storage_registry_readiness_gate_smoke.py
- tests/storage_registry/test_storage_registry_dashboard_rag_portability_gate_smoke.py
- tests/storage_registry/test_storage_artifact_readiness_gate_smoke.py
- tests/storage_registry/test_storage_phase_1_5_ready_smoke.py
- tests/storage_registry/test_storage_phase_1_5_no_server_data_plane_import_smoke.py

## Жёсткие правила

PHASE 1.5 не пишет storage data.

PHASE 1.5 не переносит файлы.

PHASE 1.5 не создаёт runtime DATA_PLANE.

PHASE 1.5 не мутирует artifact routing.

PHASE 1.5 не трогает frontend.

PHASE 1.5 не создаёт второй StorageNodeId world.

PHASE 1.5 готовит read-only visibility для dashboard, RAG, artifact routing, model store, media store, retrieval index и будущего переноса на M.2/NAS.

## Проверки

Принятые результаты:

- PHASE 1.5 Batch 3 local tests: 20 passed
- related pack: 352 passed
- full auto parallel: 1758 passed

Warnings не являются blocker, так как относятся к pytest-benchmark / xdist / multiprocessing fork under parallel test execution.

## Acceptance

PHASE 1.5 считается принятой, если:

- storage registry core readiness returns phase_core_ready=True;
- artifact binding readiness returns phase_ready=True;
- storage entries are dashboard-visible;
- retrieval index is present;
- artifact collection is present;
- model store is present;
- media artifact store is present;
- M.2/NAS readiness is True;
- artifact routing binds at least one data-plane route to storage registry;
- DATA_PLANE is not imported or created as a runtime dependency;
- full auto parallel remains green.
