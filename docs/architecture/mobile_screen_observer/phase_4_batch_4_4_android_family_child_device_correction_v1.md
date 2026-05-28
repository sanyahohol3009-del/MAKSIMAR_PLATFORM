# PHASE 4 / BATCH 4.4 — Android Family Child Device Correction v1

## Решение

BATCH 4.4 расширяется до реализации Android-кода.

Теперь Android layer должен иметь две отдельные ветки:

1. Normal Android Screen Observer Client
   Путь:
   - ANDROID_SHELL/screen_observer_client/

2. Android Family Child Device Bridge
   Путь:
   - ANDROID_SHELL/family_child_device/

## Почему это нужно

BATCH 4.2 разделил normal observer contracts и family child device control contracts.

BATCH 4.3 сохранил это разделение на server runtime уровне.

BATCH 4.4 обязан сохранить то же разделение на Android shell уровне до iOS и dashboard batches.

## Нельзя

- Нельзя прятать child-control внутри `ANDROID_SHELL/screen_observer_client/`.
- Нельзя превращать `android_remote_assistance_intent_bridge.py` в child-control execution path.
- Нельзя импортировать family child contracts в normal observer Android files.
- Нельзя смешивать general Phone Window и Family / Children surfaces.
- Нельзя добавлять реальное Android platform execution в BATCH 4.4.

## Normal Android observer

Обычный Android observer остаётся:

- read-only;
- consent-bound;
- metadata/reference-only;
- remote-assistance-intent-only;
- без child control;
- без touch/keyboard/device execution.

## Android family child bridge

Family child Android bridge работает только с:

- `MAKSIMAR_CORE_LIB/family_child_device_control/`

Family child bridge требует:

- guardian authority;
- audit;
- visible child-device status;
- `dashboard_bypass_allowed == False`.

## Safety

В BATCH 4.4 запрещено:

- Android platform API calls;
- MediaProjection;
- AccessibilityService;
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
