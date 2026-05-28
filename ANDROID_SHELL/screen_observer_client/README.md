# Android Screen Observer Client

This Android shell layer describes the normal adult/user phone observer bridge.

Scope:

- read-only screen observer client projection;
- consent-bound session creation;
- metadata/reference-only stream bridge;
- remote assistance intent projection;
- no child-control logic.

Child/family managed device logic is intentionally separated into:

- `ANDROID_SHELL/family_child_device/`

Safety constraints:

- no Android platform API calls;
- no MediaProjection execution;
- no AccessibilityService execution;
- no screenshot runtime;
- no screen recording runtime;
- no pixel decode;
- no inline pixel payload handling;
- no touch execution;
- no keyboard execution;
- no gesture injection;
- no network/socket/tunnel opening;
- no external sync;
- no runtime mutation;
- no canonical write;
- no source-of-truth override.

This layer is a shell bridge / contract projection layer for BATCH 4.4.
