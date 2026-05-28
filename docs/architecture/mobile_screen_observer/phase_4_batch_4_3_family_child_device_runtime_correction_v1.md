# PHASE 4 / BATCH 4.3 — Family Child Device Runtime Correction v1

## Решение

BATCH 4.3 расширяется до реализации кода.

Теперь server runtime должен иметь две отдельные ветки:

1. Normal Mobile Screen Observer Runtime
   Путь:
   - MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/

2. Family Child Device Runtime
   Путь:
   - MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/

## Почему это нужно

BATCH 4.2 уже разделил обычный observer и семейный child-control на уровне core contracts.

Server runtime обязан сохранить это разделение до Android, iOS и dashboard.

## Нельзя

- Нельзя прятать child-control внутри normal observer runtime.
- Нельзя делать remote_assistance_policy_runtime.py скрытым путём управления детским телефоном.
- Нельзя смешивать Phone Window и Family / Children.
- Нельзя добавлять реальный device execution в BATCH 4.3.

## Normal runtime

Обычный observer остаётся:

- read-only;
- metadata/reference only;
- approval-gated remote assistance;
- без child control;
- без touch/keyboard/device execution.

## Family runtime

Family runtime работает только с:

- MAKSIMAR_CORE_LIB/family_child_device_control/

Child runtime требует:

- guardian authority;
- audit;
- visible child-device status;
- dashboard_bypass_allowed == False.

## Safety

В BATCH 4.3 запрещено:

- platform API calls;
- real screen capture;
- screenshot runtime;
- screen recording runtime;
- pixel decode;
- inline pixel payload handling;
- touch runtime execution;
- keyboard runtime execution;
- gesture injection;
- app control runtime;
- emergency lock runtime;
- screen-time enforcement runtime;
- network/socket/tunnel/port opening;
- container start;
- runtime mutation;
- canonical write;
- source-of-truth override.
