# PHASE 1.4 Batch 1 — Existing Domain Enrollment Preview Acceptance v1

## Статус

PHASE 1.4 Batch 1 принят.

Это не полное закрытие PHASE 1.4, а первый принятый блок внутри auto-enrollment track.

## Решение

Работа выполнена как EXTEND существующего слоя:

- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/

Не создан новый parallel subsystem:

- MAKSIMAR_CORE_LIB/memory_engine/auto_enrollment/

## Назначение Batch 1

Построить read-only preview для существующих доменных поверхностей проекта.

Поток:

existing project folders
-> inventory
-> minimal manifest preview
-> write guard
-> enrollment preview

## Переиспользовано

- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/__init__.py
- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/registry_auto_enrollment_contract.py
- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/registry_auto_enrollment_models.py
- tests/registry_auto_enrollment/test_registry_auto_enrollment_contract_smoke.py

## Добавлено

Новые файлы:

- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/existing_domain_inventory.py
- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/existing_domain_minimal_manifest_builder.py
- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/enrollment_write_guard.py
- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/enrollment_preview_builder.py

Новые тесты:

- tests/registry_auto_enrollment/test_existing_domain_inventory_smoke.py
- tests/registry_auto_enrollment/test_existing_domain_minimal_manifest_builder_smoke.py
- tests/registry_auto_enrollment/test_enrollment_write_guard_smoke.py
- tests/registry_auto_enrollment/test_enrollment_preview_builder_smoke.py

## Preview result

Enrollment preview confirmed:

- existing_domain_entries: 43
- domain_cube_entries: 16
- platform_layer_entries: 17
- server_registry_entries: 4
- shell_adapter_entries: 4
- minimal_manifest_preview_entries: 43
- preview_ready: True

## Flow

module_discovered
-> id_assigned
-> storage_node_id_assigned
-> retrieval_source_id_assigned
-> registry_entry_ready
-> dashboard_exposure_ready
-> observability_binding_ready

## Жёсткие правила

Batch 1 не пишет manifest-файлы.
Batch 1 не мутирует registry.
Batch 1 не перезаписывает существующие домены.
Batch 1 только строит inventory / preview / write-guard decisions.

## Проверки

Принятые результаты:

- PHASE 1.4 local tests: 8 passed
- related pack: 46 passed
- full auto parallel: 1727 passed

## Acceptance

Batch 1 считается принятым, если:

- existing domains discovered;
- each discovered domain receives storage_node_id;
- each discovered domain receives retrieval_source_id;
- each discovered domain receives dashboard_exposure_id;
- each discovered domain receives observability_binding_id;
- write guard blocks existing target without explicit overwrite;
- preview flow is deterministic;
- full auto parallel remains green.
