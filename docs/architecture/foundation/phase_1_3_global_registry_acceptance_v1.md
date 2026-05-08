# PHASE 1.3 — Global Registry / Memory Registry Binding Acceptance v1

## Статус

PHASE 1.3 принят как EXTEND существующих registry layers.

## Решение

Не создавать второй domain_registry subsystem.

Использовать существующие слои:

- MAKSIMAR_SERVER/MEMORY_REGISTRY/
- MAKSIMAR_SERVER/SKILL_ADAPTER_REGISTRY/
- MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT/
- MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/

## Переиспользовано

- build_memory_registry_contract
- build_skill_adapter_registry_contract
- build_registry_auto_enrollment_contract
- build_memory_skill_metrics_contract

## Добавлено

Новые read-only projection / preview файлы:

- MAKSIMAR_SERVER/MEMORY_REGISTRY/global_registry_projection_models.py
- MAKSIMAR_SERVER/MEMORY_REGISTRY/global_registry_projection_builder.py
- MAKSIMAR_SERVER/MEMORY_REGISTRY/global_registry_preview_builder.py

Новые тесты:

- tests/memory_registry/test_global_registry_projection_models_smoke.py
- tests/memory_registry/test_global_registry_projection_builder_smoke.py
- tests/memory_registry/test_global_registry_preview_builder_smoke.py
- tests/memory_registry/test_global_registry_unlimited_counts_smoke.py
- tests/memory_skill_metrics/test_memory_skill_metrics_no_single_entry_limit_smoke.py

## Исправлено

Удалена архитектурная привязка memory_skill_metrics к exactly one memory registry entry и exactly one skill registry entry.

Теперь observability metrics поддерживает расширяемое количество:

- memory registry entries
- skill adapter registry entries
- ai router bindings

## Flow

module_manifest
-> canonical_id_generation
-> registry_projection
-> dashboard_read_only_visibility

## Preview result

Global registry projection показывает:

- modules
- skills
- memory tiers
- workers
- storage nodes
- dashboard views
- observability visibility
- dashboard visibility
- retrieval visibility

## Scalability rule

Registry layer не должен зависеть от фиксированного количества модулей, кубиков, skills, memory tiers, dashboard views, storage nodes или retrieval sources.

Разрешено проверять:

- len(entries)
- computed totals
- unique registry_id
- required entry kinds
- deterministic flow
- no fixed single-entry assumptions

Запрещено:

- expected exactly one memory registry entry
- expected exactly one skill registry entry
- hardcoded total_entries as architecture limit

## Проверки

Принятые результаты:

- PHASE 1.3 local tests: 11 passed
- PHASE 1.3 related pack: 41 passed
- full auto parallel: 1722 passed

## Acceptance

PHASE 1.3 считается принятым, если:

- global registry preview builds;
- registry projection entries are unique;
- dashboard-visible entries are computable;
- retrieval-visible entries are computable;
- observability-visible entries are computable;
- memory_skill_metrics no longer assumes exactly one memory/skill entry;
- full auto parallel remains green.
