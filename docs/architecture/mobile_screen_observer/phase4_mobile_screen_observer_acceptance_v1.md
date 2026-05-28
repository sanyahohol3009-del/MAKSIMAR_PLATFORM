# PHASE 4 — Mobile Screen Observer / PC Phone Window Acceptance v1

## Acceptance status

PHASE 4 is accepted when all batches from 4.1 to 4.7 are READY in the project readiness map.

Scope:

- 4.1 Screen Observer Contracts
- 4.2 Screen Policy / Remote Assistance / Family Child Device Control Contracts
- 4.3 Server Screen Observer / Family Child Device Runtime
- 4.4 Android Screen Observer / Family Child Device Client
- 4.5 iOS Screen Observer / Family Child Device Client
- 4.6 PC Phone Screen Window
- 4.7 PHASE 4 Acceptance

## JARVIS handoff summary

This document is the canonical handoff for JARVIS / MAKSIMAR after PHASE 4.

PHASE 4 creates a controlled mobile screen observer foundation. It does not implement real device execution.

The implemented architecture provides:

- normal mobile screen observer contracts;
- server runtime and read-model projection;
- Android shell bridge;
- iOS shell bridge;
- PC Phone Window read-only dashboard contract;
- separated Family / Children policy/control projection;
- approval-gated remote assistance intent layer.

## Normal observer path

Normal observer path:

- MAKSIMAR_CORE_LIB/mobile_screen_observer/
- MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/
- ANDROID_SHELL/screen_observer_client/
- IOS_SHELL/screen_observer_client/
- MAKSIMAR_CORE_LIB/mobile_screen_observer/phone_screen_window_*
- frontend/contracts/phone_screen_window_contract.ts

Normal observer rules:

- read-only by default;
- consent-bound;
- audit-visible;
- frame-reference-only;
- metadata/reference projection only;
- no child-control logic;
- no dashboard direct execution;
- no device control execution;
- no runtime mutation;
- no core write;
- no source-of-truth override.

## Family / Children path

Family child device path:

- MAKSIMAR_CORE_LIB/family_child_device_control/
- MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/
- ANDROID_SHELL/family_child_device/
- IOS_SHELL/family_child_device/

Family / Children rules:

- separate from normal Phone Window;
- guardian authority required;
- child device status visible;
- audit required;
- dashboard bypass rejected;
- policy projection only in PHASE 4;
- no Android/iOS platform execution;
- no real app blocking;
- no real screen-time enforcement;
- no emergency lock runtime;
- no real touch/keyboard/gesture execution.

## PC Phone Window

PC Phone Window is a dashboard/read-model surface.

It may show:

- device id;
- owner identity id;
- platform;
- consent state;
- observer state;
- frame reference;
- audit state;
- remote assistance intent state.

It must not:

- execute device actions;
- mutate runtime;
- write to canonical/core state;
- bypass approval;
- contain child-control surface;
- replace Family / Children dashboard surface.

## Remote assistance

Remote assistance is accepted only as an approval-gated intent.

Rules:

- remote assistance requires approval;
- remote assistance requires audit;
- dashboard direct execution is false;
- device control execution is false;
- touch/keyboard execution is false;
- runtime mutation is false;
- core write is false.

## Forbidden runtime capabilities in PHASE 4

PHASE 4 must not introduce:

- real screen capture;
- screenshot runtime;
- screen recording runtime;
- pixel decode;
- inline pixel payload handling;
- Android MediaProjection execution;
- Android AccessibilityService execution;
- iOS ReplayKit execution;
- iOS Accessibility API execution;
- touch injection;
- keyboard injection;
- gesture injection;
- network/socket/tunnel opening;
- external sync;
- direct dashboard-to-device execution;
- canonical write;
- source-of-truth override.

## Acceptance evidence

Acceptance requires:

1. All expected PHASE 4 files exist.
2. All PHASE 4 batches are READY.
3. Normal observer and family child device paths are separated.
4. Android normal observer cannot enable child control.
5. iOS normal observer cannot enable child control.
6. PC Phone Window is read-only by default.
7. Remote assistance requires approval.
8. Dashboard cannot directly execute mobile screen/device actions.
9. Preview tool runs directly and emits a read-only payload.
10. Unrelated dirty/untracked surfaces are not part of PHASE 4 acceptance.
