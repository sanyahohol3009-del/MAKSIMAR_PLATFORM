# PHASE 1.5 Batch 1 — Storage Registry Core Binding Acceptance v1

## Статус

PHASE 1.5 Batch 1 принят.

Это первый принятый блок Storage / Artifact / Model Registry track.

## Решение

Создан thin storage_registry layer:

- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/

Но не создан второй storage world.

Слой переиспользует уже принятые storage primitives из:

- MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/storage_node_id_models.py
- MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/storage_node_models.py
- MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/storage_root_models.py
- MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/portable_storage_reference_models.py
- MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/storage_relocation_builder.py
- MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/nas_storage_reference_builder.py

## Добавлено

Новые файлы:

- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/__init__.py
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/storage_registry_models.py
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/artifact_collection_models.py
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/model_store_reference_models.py
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/media_artifact_reference_models.py
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/retrieval_index_reference_models.py
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/storage_portability_policy_models.py
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/storage_registry_preview_builder.py
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/storage_registry_flow_builder.py
- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/storage_registry_validators.py

Новые тесты:

- tests/storage_registry/test_storage_registry_models_smoke.py
- tests/storage_registry/test_artifact_collection_models_smoke.py
- tests/storage_registry/test_model_store_reference_models_smoke.py
- tests/storage_registry/test_media_artifact_reference_models_smoke.py
- tests/storage_registry/test_retrieval_index_reference_models_smoke.py
- tests/storage_registry/test_storage_portability_policy_models_smoke.py
- tests/storage_registry/test_storage_registry_preview_builder_smoke.py
- tests/storage_registry/test_storage_registry_flow_builder_smoke.py
- tests/storage_registry/test_storage_registry_validators_smoke.py
- tests/storage_registry/test_storage_registry_ready_smoke.py

## Preview result

Storage registry preview confirmed:

- total_entries: 5
- dashboard_visible_entries: 5
- retrieval_visible_entries: 3
- relocation_ready_entries: 5
- nas_ready_entries: 5
- storage_ready_for_m2_nas: True
- preview_ready: True

Registered storage entry kinds:

- history_storage_node
- artifact_collection
- model_store
- media_artifact_store
- retrieval_index

## Flow

history_ingestion_storage_primitives
-> storage_registry_contract
-> artifact_collection_reference
-> model_store_reference
-> media_artifact_reference
-> retrieval_index_reference
-> portability_policy
-> dashboard_read_only_preview

## Исправление drift-risk

Первоначальный вариант ошибочно пытался создать новые StorageNodeId в формате storage_node_*.

Исправлено:

- accepted history_ingestion StorageNodeId format сохранён;
- старый StorageNodeId pattern не менялся;
- новые logical stores представлены через PortableStorageReference;
- storage_registry не ломает history_ingestion.

## Жёсткие правила

PHASE 1.5 Batch 1 не пишет файлы данных.

PHASE 1.5 Batch 1 не перемещает storage.

PHASE 1.5 Batch 1 не создаёт runtime state.

PHASE 1.5 Batch 1 не трогает frontend.

PHASE 1.5 Batch 1 не создаёт второй StorageNodeId world.

PHASE 1.5 Batch 1 только создаёт read-only registry / preview / flow слой.

## Проверки

Принятые результаты:

- py_compile: passed
- PHASE 1.5 local tests: 10 passed
- related pack: 338 passed
- full auto parallel: 1748 passed

Warnings не являются blocker для Batch 1, так как относятся к pytest-benchmark / xdist / multiprocessing fork under parallel test execution.

## Acceptance

Batch 1 считается принятым, если:

- storage registry contract builds;
- artifact collection reference builds;
- model store reference builds;
- media artifact reference builds;
- retrieval index reference builds;
- portability policy builds;
- preview_ready=True;
- flow_ready=True;
- storage_ready_for_m2_nas=True;
- all entries are relocation-ready;
- all entries are NAS-ready;
- accepted history_ingestion storage primitives are reused;
- full auto parallel remains green.
