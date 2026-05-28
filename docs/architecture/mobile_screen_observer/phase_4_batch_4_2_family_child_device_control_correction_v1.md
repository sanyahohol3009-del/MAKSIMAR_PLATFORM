# PHASE 4 / BATCH 4.2 — Family Child Device Control Correction v1

## Решение

BATCH 4.2 расширяется до реализации кода.

Теперь в PHASE 4 есть два разных режима:

1. Normal Mobile Screen Observer
   Обычный телефон взрослого пользователя.
   По умолчанию только read-only.
   Без скрытого remote-control.

2. Family Child Device Control
   Детский телефон под родительским управлением.
   Это отдельная семейная функция, не часть обычного Phone Window.

## Почему это нужно сейчас

Android, iOS, server и dashboard должны заранее знать, что семейный контроль — отдельная ветка прав.

Нельзя потом встраивать управление детским телефоном как скрытое исключение внутри обычного screen observer.

## Правильное место в проекте

Core contracts:

- MAKSIMAR_CORE_LIB/family_child_device_control/

Позже server:

- MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/

Позже Android:

- ANDROID_SHELL/family_child_device/

Позже iOS:

- IOS_SHELL/family_child_device/

Позже dashboard:

- Family / Children
- не общий Phone Window

## Условия разрешения детского контроля

Child control разрешён только если все условия истинны:

- device_profile == "child_managed_device"
- guardian_authority_verified is True
- family_policy_enabled is True
- audit_required is True
- visible_child_device_status_required is True
- dashboard_bypass_allowed is False

## Жёсткие правила

- Обычный screen observer остаётся read-only.
- Обычный observer не получает скрытый remote-control.
- Детский контроль живёт отдельно в family_child_device_control.
- Нужна проверка родительских прав.
- Нужен audit.
- Статус контроля должен быть видим на детском устройстве.
- Dashboard bypass запрещён.
- В BATCH 4.2 нет реального исполнения на устройстве.
- В BATCH 4.2 нет реального screen capture.
- В BATCH 4.2 нет touch/keyboard injection runtime.
- В BATCH 4.2 нет Android/iOS platform API calls.
- В BATCH 4.2 нет network/socket/tunnel.
- В BATCH 4.2 нет runtime mutation.
- В BATCH 4.2 нет canonical write.
