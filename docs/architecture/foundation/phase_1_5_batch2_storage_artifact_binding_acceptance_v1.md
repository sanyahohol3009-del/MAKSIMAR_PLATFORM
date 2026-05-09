# PHASE 1.5 Batch 2 — Storage Registry / Artifact Routing Binding Acceptance v1

## Статус

PHASE 1.5 Batch 2 принят.

Это второй принятый блок Storage / Artifact / Model Registry track.

## Решение

Слой реализован как server-side binding между:

- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/
- MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/

Не создан полноценный MAKSIMAR_SERVER/DATA_PLANE на этом этапе.

Причина:

- artifact_routing уже существует;
- tests/data_plane уже существуют;
- payload artifact routing tests уже существуют;
- текущая задача — связать storage registry с artifact routing без создания второго runtime/data-plane world.

## Переиспользовано

- MAKSIMAR_CORE_LIB/memory_engine/storage_registry/
- MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/artifact_routing_models.py
- MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/artifact_routing_binding.py
- tests/data_plane/
- tests/payload_classification/test_artifact_routing_binding_smoke.py
- tests/distributed_lease_artifact_routing/

## Добавлено

Новые файлы:

- MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/storage_registry_artifact_binding_models.py
- MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/storage_registry_artifact_binding_builder.py
- MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/storage_registry_artifact_binding_preview.py

Новые тесты:

- tests/storage_registry/test_storage_artifact_binding_models_smoke.py
- tests/storage_registry/test_storage_artifact_binding_builder_smoke.py
- tests/storage_registry/test_storage_artifact_binding_preview_smoke.py
- tests/storage_registry/test_storage_artifact_binding_data_plane_ready_smoke.py
- tests/storage_registry/test_storage_artifact_binding_ready_smoke.py

## Preview result

Confirmed:

- total_entries: 3
- storage_required_entries: 1
- storage_ready_entries: 1
- data_plane_ready_entries: 1
- dashboard_visible_entries: 3
- binding_ready: True
- preview_ready: True

## Flow

payload_classification
-> artifact_routing
-> storage_registry_lookup
-> artifact_collection_binding
-> data_plane_route_readiness
-> dashboard_read_only_preview

## Жёсткие правила

Batch 2 не пишет data-plane state.

Batch 2 не создаёт MAKSIMAR_SERVER/DATA_PLANE.

Batch 2 не мутирует storage registry.

Batch 2 не пишет artifact files.

Batch 2 не трогает frontend.

Batch 2 только создаёт read-only binding / preview между artifact routing и storage registry.

## Проверки

Принятые результаты:

- py_compile: passed
- PHASE 1.5 Batch 2 local tests: 15 passed
- related pack: 30 passed
- full auto parallel: 1753 passed

Warnings не являются blocker, так как относятся к pytest-benchmark / xdist / multiprocessing fork under parallel test execution.

## Acceptance

Batch 2 считается принятым, если:

- storage artifact binding models build;
- storage artifact binding builder builds;
- storage artifact binding preview builds;
- artifact routing data-plane entry binds to artifact collection;
- storage_required_entries >= 1;
- storage_ready_entries == storage_required_entries;
- data_plane_ready_entries == storage_required_entries;
- binding_ready=True;
- preview_ready=True;
- full auto parallel remains green.
