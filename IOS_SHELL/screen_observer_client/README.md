# iOS Screen Observer Client

This iOS shell layer describes the normal adult/user phone observer bridge.

Scope:

- read-only screen observer client projection;
- consent-bound session creation;
- metadata/reference-only stream bridge;
- remote assistance intent projection;
- no child-control logic.

Child/family managed device logic is intentionally separated into:

- `IOS_SHELL/family_child_device/`

Safety constraints:

- no iOS platform API calls;
- no ReplayKit execution;
- no Accessibility API execution;
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

This layer is a shell bridge / contract projection layer for BATCH 4.5.
