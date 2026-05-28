# PHASE 4 — Mobile Screen Observer / PC Phone Window Readiness Registry Reconciliation v1

## Purpose

Register PHASE 4 expected files before implementation.

PHASE 4 creates a read-only PC/server dashboard phone screen window with explicit consent and audit.

## Semantic reconnaissance result

No dedicated PHASE 4 layer exists yet.

Not found:

- `MAKSIMAR_CORE_LIB/mobile_screen_observer/`
- `MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/`
- `ANDROID_SHELL/screen_observer_client/`
- `IOS_SHELL/screen_observer_client/`
- `CONTAINER_DEPLOYMENT/cubes/mobile_screen_observer/`

Adjacent surfaces exist but must not be treated as source of truth:

- OOB `final_screen_state_*` is dashboard/presentation final state, not phone screen streaming truth.
- `mobile_bridge/*` is generic mobile request/task/result bridge, not screen stream runtime.
- `display_topology/*` contains mobile display proxy concepts, but not phone frame source.
- Android/iOS VPN/P2P/chat shells are safety/style patterns only.

## Implementation decision

- BATCH 4.1: CREATE core mobile screen observer contracts.
- BATCH 4.2: CREATE screen policy / remote assistance contracts.
- BATCH 4.3: CREATE server mobile screen observer runtime/read-model layer.
- BATCH 4.4: CREATE Android screen observer client shell.
- BATCH 4.5: CREATE iOS screen observer client shell.
- BATCH 4.6: CREATE phone screen window read-model/panel/preview; EXTEND dashboard binding later.
- BATCH 4.7: CREATE phase acceptance and JARVIS-readable context document.

## Safety invariants

- Phone window is read-only.
- Remote assistance is disabled by default.
- Explicit consent is required.
- Audit is required.
- Frames are metadata/reference only.
- No inline binary frame payloads.
- No direct screen capture execution in contracts.
- No Android/iOS platform API call in contracts.
- No MediaProjection, ReplayKit, screenshot capture, accessibility capture, touch injection, keyboard injection, gesture injection, or device control.
- No dashboard direct control.
- No external network, sockets, ports, tunnel creation, or runtime sync.
- No runtime mutation.
- No canonical write.
- No source-of-truth override.


## Correction v1.1 — Family Child Device Control

BATCH 4.2 is extended before implementation.

Normal Mobile Screen Observer remains read-only by default.

Family Child Device Control is added as a separate core policy/contract domain:

- `MAKSIMAR_CORE_LIB/family_child_device_control/`

This prevents hidden remote-control semantics from being placed inside the normal phone observer.

Batch readiness check commands are documented here:

- `docs/architecture/mobile_screen_observer/phase_4_batch_readiness_check_commands_v1.md`


## Correction v1.2 — Family Child Device Runtime

BATCH 4.3 is extended before implementation.

Normal server observer runtime remains under:

- `MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/`

Family child device runtime is added separately under:

- `MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME/`

This preserves the BATCH 4.2 split between normal observer contracts and family child device contracts.

Normal observer runtime must not enable child control.

Family child device runtime must require guardian authority, audit, visible child-device status, and reject dashboard bypass.


## Correction v1.3 — Android Family Child Device Bridge

BATCH 4.4 is extended before implementation.

Normal Android observer remains under:

- `ANDROID_SHELL/screen_observer_client/`

Android family child device bridge is added separately under:

- `ANDROID_SHELL/family_child_device/`

This preserves the BATCH 4.2 core split and BATCH 4.3 server runtime split.

Normal Android observer must not enable child control.

Android family child bridge must require guardian authority, audit, visible child-device status, and reject dashboard bypass.

BATCH 4.4 remains Android shell bridge / policy projection only. It must not call Android platform APIs or execute real screen capture, touch, keyboard, network, tunnel, canonical write, or source-of-truth override.
