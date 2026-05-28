# PHASE 4 — Batch Readiness Check Commands v1

## Что это

Это команды, которыми мы проверяем готовность batch.

## Проверить один batch

Для BATCH 4.2:

    ./.venv/bin/python tools/project_readiness_control/project_file_readiness_map.py --batch-id 4.2

Для BATCH 4.1:

    ./.venv/bin/python tools/project_readiness_control/project_file_readiness_map.py --batch-id 4.1

## Проверить всю карту готовности

    ./.venv/bin/python tools/project_readiness_control/project_file_readiness_map.py

## Проверить registry tests

    ./.venv/bin/python -m pytest tests/project_readiness_control/test_project_file_readiness_map_smoke.py tests/project_readiness_control/test_roadmap_expected_files_registry_smoke.py -q

## Проверить мусор в diff перед commit

    git diff --check -- docs/architecture/mobile_screen_observer/phase_4_batch_4_2_family_child_device_control_correction_v1.md docs/architecture/mobile_screen_observer/phase_4_batch_readiness_check_commands_v1.md docs/architecture/mobile_screen_observer/phase_4_readiness_registry_reconciliation_v1.md tools/project_readiness_control/roadmap_expected_files_registry.py

## Проверить что попадёт в commit

    git status -sb
    git diff --cached --name-only

## Правило

Batch можно считать готовым только когда:

- файлы batch зарегистрированы в readiness registry;
- файлы реально существуют;
- target tests проходят;
- readiness map показывает batch как READY;
- unrelated dirty/untracked файлы не staged.


## Проверить BATCH 4.3

    ./.venv/bin/python tools/project_readiness_control/project_file_readiness_map.py --batch-id 4.3

Ожидаемый результат после registry correction и до реализации:

    BATCH 4.3 MISSING 0/30

Ожидаемый результат после реализации:

    BATCH 4.3 READY 30/30


## Проверить BATCH 4.4

    ./.venv/bin/python tools/project_readiness_control/project_file_readiness_map.py --batch-id 4.4

Ожидаемый результат после registry correction и до реализации:

    BATCH 4.4 MISSING 0/30

Ожидаемый результат после реализации:

    BATCH 4.4 READY 30/30
