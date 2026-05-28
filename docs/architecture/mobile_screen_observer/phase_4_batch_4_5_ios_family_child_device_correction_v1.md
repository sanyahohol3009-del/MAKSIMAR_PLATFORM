# PHASE 4 / BATCH 4.5 — iOS Family Child Device Correction v1

## Решение

BATCH 4.5 расширяется до реализации iOS-кода.

Теперь iOS layer должен иметь две отдельные ветки:

1. Normal iOS Screen Observer Client
   Путь:
   - IOS_SHELL/screen_observer_client/

2. iOS Family Child Device Bridge
   Путь:
   - IOS_SHELL/family_child_device/

## Почему это нужно

BATCH 4.2 разделил normal observer contracts и family child device control contracts.

BATCH 4.3 сохранил это разделение на server runtime уровне.

BATCH 4.4 сохранил это разделение на Android shell уровне.

BATCH 4.5 обязан сохранить то же разделение на iOS shell уровне до dashboard batches.

## Нельзя

- Нельзя прятать child-control внутри `IOS_SHELL/screen_observer_client/`.
- Нельзя превращать `ios_remote_assistance_intent_bridge.py` в child-control execution path.
- Нельзя импортировать family child contracts в normal observer iOS files.
- Нельзя смешивать general Phone Window и Family / Children surfaces.
- Нельзя добавлять реальное iOS platform execution в BATCH 4.5.

## Normal iOS observer

Обычный iOS observer остаётся:

- read-only;
- consent-bound;
- metadata/reference-only;
- remote-assistance-intent-only;
- без child control;
- без touch/keyboard/device execution.

## iOS family child bridge

Family child iOS bridge работает только с:

- `MAKSIMAR_CORE_LIB/family_child_device_control/`

Family child bridge требует:

- guardian authority;
- audit;
- visible child-device status;
- `dashboard_bypass_allowed == False`.

## Safety

В BATCH 4.5 запрещено:

- iOS platform API calls;
- ReplayKit;
- Accessibility API execution;
- screenshot runtime;
- screen recording runtime;
- pixel decode;
- inline pixel payload handling;
- touch execution;
- keyboard execution;
- gesture injection;
- network/socket/tunnel/port opening;
- external sync;
- runtime mutation;
- canonical write;
- source-of-truth override.
