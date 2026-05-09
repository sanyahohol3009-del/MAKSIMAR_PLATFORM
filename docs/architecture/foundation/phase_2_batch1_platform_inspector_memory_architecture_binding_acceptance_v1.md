# PHASE 2 Batch 1 — Platform Inspector / Architecture Memory Binding Acceptance v1

## Статус

PHASE 2 Batch 1 принят.

Слой добавлен через existing runtime:

- MAKSIMAR_SERVER/architecture_map_runtime/

Новые root-директории не создавались.

## Решение

PHASE 2 Batch 1 связывает memory layer с architecture map runtime.

JARVIS получает read-only видимость:

- где живёт memory registry;
- где живёт global registry;
- где живут dashboard read-only views;
- как memory flow проходит через storage / media / retrieval / dashboard;
- какие domain cubes существуют;
- где находится retrieval trace;
- где находится project architecture memory.

## Добавлено

Новые файлы:

- MAKSIMAR_SERVER/architecture_map_runtime/memory_layer_architecture_binding.py
- MAKSIMAR_SERVER/architecture_map_runtime/memory_data_flow_binding.py
- MAKSIMAR_SERVER/architecture_map_runtime/jarvis_memory_locator.py
- MAKSIMAR_SERVER/architecture_map_runtime/domain_cube_memory_locator.py
- MAKSIMAR_SERVER/architecture_map_runtime/memory_dependency_summary_builder.py

Новые тесты:

- tests/architecture_map_runtime/test_memory_layer_architecture_binding_smoke.py
- tests/architecture_map_runtime/test_memory_data_flow_binding_smoke.py
- tests/architecture_map_runtime/test_jarvis_memory_locator_smoke.py
- tests/architecture_map_runtime/test_domain_cube_memory_locator_smoke.py
- tests/architecture_map_runtime/test_domain_cube_slug_identity_preserved_smoke.py

## Принятые результаты

Architecture memory binding:

- total_bindings: 3
- ready_bindings: 3
- dashboard_visible_bindings: 3
- source_contract_bound_bindings: 3

Memory data flow:

- total_flows: 4
- ready_flows: 4
- dashboard_visible_flows: 4
- source_bound_flows: 4
- target_bound_flows: 4

JARVIS memory locator:

- total_locators: 3
- ready_locators: 3
- read_only_locators: 3

Domain cube memory locator:

- total_cubes: 16
- ready_cubes: 16
- dashboard_visible_cubes: 16

Memory dependency summary:

- architecture_module_views: 3
- architecture_dependency_views: 3
- architecture_flow_views: 5
- memory_architecture_bindings: 3
- memory_data_flows: 4
- jarvis_memory_locators: 3
- domain_cube_memory_locators: 16
- no_new_architecture_root: True
- no_platform_inspector_root: True
- read_only: True
- source_contract_bound: True
- phase_ready: True

## 3D cube identity rule

`3d_cube` remains the semantic cube slug and real cube path:

- cube_slug: 3d_cube
- cube_path: DOMAIN_CUBES/3d_cube

The normalized locator id is only a technical ID for regex compatibility:

- locator_id: domain_cube_memory_locator_cube_3d_cube

This does not rename the cube and does not merge it with any future mobile 3D module.

Mobile 3D module and platform 3D cube remain separate architectural entities.

## Жёсткие правила

PHASE 2 Batch 1 is read-only.

PHASE 2 Batch 1 does not mutate memory.

PHASE 2 Batch 1 does not mutate architecture map.

PHASE 2 Batch 1 does not create a new architecture root.

PHASE 2 Batch 1 does not create PLATFORM_INSPECTOR root.

PHASE 2 Batch 1 does not create network surfaces.

PHASE 2 Batch 1 does not change network segmentation or trust boundaries.

PHASE 2 Batch 1 does not call retrieval backend.

mgrep and sqlite-vec remain blocked future backend adapters.

## Проверки

Принятые результаты:

- PHASE 2 Batch 1 local tests: 11 passed
- related pack: 405 passed
- full auto parallel: 1833 passed

Warnings не являются blocker, так как относятся к pytest-benchmark / xdist / multiprocessing fork under parallel test execution.

## Acceptance

Batch 1 считается принятым, если:

- memory layer architecture binding builds;
- memory data flow binding builds;
- JARVIS memory locator builds;
- domain cube memory locator builds;
- all contracts are read-only;
- all bindings are ready;
- all cube slugs preserve semantic identity;
- no new architecture root exists;
- no platform inspector root exists;
- full auto parallel remains green.
