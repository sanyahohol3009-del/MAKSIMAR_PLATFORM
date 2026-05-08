# PHASE 1.1 — Module Manifest Schema Extension Acceptance v1

## Статус

PHASE 1.1 принят как EXTEND существующего module_manifest слоя.

## Решение

Не создавать второй manifest subsystem.

Существующий слой:

- MAKSIMAR_CORE_LIB/module_manifest/__init__.py
- MAKSIMAR_CORE_LIB/module_manifest/module_manifest_schema.py

был расширен, а не заменён.

## Переиспользовано

- ModuleManifestEntry
- ModuleManifestSchemaContract
- build_module_manifest_schema_contract
- tests/module_manifest/test_module_manifest_schema_smoke.py

## Добавлено

Новый preview файл:

- MAKSIMAR_CORE_LIB/module_manifest/module_manifest_flow_preview.py

Новые тесты:

- tests/module_manifest/test_module_manifest_extension_fields_smoke.py
- tests/module_manifest/test_module_manifest_flow_entries_smoke.py
- tests/module_manifest/test_module_manifest_flow_preview_smoke.py
- tests/module_manifest/test_module_manifest_invalid_dashboard_exposure_smoke.py

## Новые manifest fields

Добавлены поля:

- storage_profile
- retrieval_profile
- required_memory_tier_ids
- required_skill_ids
- enrollment_allowed
- dashboard_exposure_allowed

## Flow preview

Добавлен read-only preview поток:

manifest_schema
-> canonical_id_generation
-> registry_auto_enrollment
-> dashboard_read_only_exposure

## Проверки

Принятые результаты:

- PHASE 1.1 local tests: 7 passed
- related pack: 16 passed
- full auto parallel: 1711 passed

## Жёсткие правила

PHASE 1.1 не должен:

- создавать второй manifest subsystem;
- создавать второй registry;
- писать в runtime;
- выполнять auto-enrollment напрямую;
- мутировать dashboard;
- создавать hardcoded UI binding.

## Acceptance

PHASE 1.1 считается принятым, если:

- manifest entry поддерживает storage/retrieval profiles;
- manifest entry поддерживает required memory tiers / skills;
- manifest flow preview показывает путь до canonical id / registry / dashboard;
- старый module_manifest тест остаётся зелёным;
- related memory binding tests остаются зелёными;
- full auto parallel остаётся зелёным.
