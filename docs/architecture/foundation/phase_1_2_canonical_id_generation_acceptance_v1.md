# PHASE 1.2 — Canonical ID Generation Extension Acceptance v1

## Статус

PHASE 1.2 принят как EXTEND существующего id_generation слоя.

## Решение

Не создавать второй ID allocator.

Существующий слой:

- MAKSIMAR_CORE_LIB/id_generation/__init__.py
- MAKSIMAR_CORE_LIB/id_generation/canonical_id_generation.py

был расширен, а не заменён отдельным subsystem.

## Переиспользовано

- CanonicalIdAllocationEntry
- CanonicalIdGenerationContract
- build_canonical_id_generation_contract
- tests/id_generation/test_canonical_id_generation_smoke.py

## Добавлено

Новый preview файл:

- MAKSIMAR_CORE_LIB/id_generation/canonical_id_flow_preview.py

Новые тесты:

- tests/id_generation/test_canonical_id_collision_boundary_smoke.py
- tests/id_generation/test_canonical_id_extension_fields_smoke.py
- tests/id_generation/test_canonical_id_flow_preview_smoke.py
- tests/id_generation/test_id_generation_ready_smoke.py

## Новые ID bindings

Добавлены:

- storage_node_id
- retrieval_source_id

Сохранены:

- module_id
- skill_id
- memory_tier_id
- worker_id
- panel_ids
- artifact_ref_prefix
- trace_id_prefix
- collision_free

## Flow preview

Добавлен read-only preview поток:

module_manifest_schema
-> canonical_id_generation
-> collision_check
-> registry_auto_enrollment
-> dashboard_read_only_binding

## Scalability rule

Количество модулей, кубиков, скилов, дашбордов, панелей, мониторов, воркеров и retrieval sources не ограничено.

Тесты и contracts не должны архитектурно зависеть от фиксированного числа entries.

Разрешено проверять:

- len(entries)
- computed totals
- uniqueness
- collision-free state
- deterministic IDs
- required flow stages
- known frozen fixture entries where explicitly required

Запрещено считать, что система всегда содержит фиксированное количество модулей.

## __init__ rule

Existing __init__.py files должны расширяться точечно.

Запрещено полностью переписывать __init__.py без предварительной проверки existing exports.

## Проверки

Принятые результаты:

- PHASE 1.2 local tests: 9 passed
- related pack: 42 passed
- full auto parallel: 1717 passed

## Жёсткие правила

PHASE 1.2 не должен:

- создавать второй allocator;
- создавать второй registry;
- писать в runtime;
- выполнять auto-enrollment напрямую;
- мутировать dashboard;
- привязывать систему к фиксированному числу modules / cubes / skills / dashboards.

## Acceptance

PHASE 1.2 считается принятым, если:

- canonical ID generation выдаёт storage_node_id;
- canonical ID generation выдаёт retrieval_source_id там, где retrieval включён;
- collision boundary проверяется;
- flow preview показывает путь до registry/dashboard;
- existing module_manifest tests остаются зелёными;
- related cascade tests остаются зелёными;
- full auto parallel остаётся зелёным.
