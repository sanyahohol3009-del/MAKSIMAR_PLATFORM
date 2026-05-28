# Android Family Child Device Bridge

This Android shell layer describes the family/child managed device bridge.

Scope:

- child device profile bridge;
- guardian authority bridge;
- child screen control policy bridge;
- child remote control intent bridge;
- child device audit bridge;
- child app control policy bridge;
- child screen time policy bridge;
- family child device policy binding.

This layer is separate from:

- `ANDROID_SHELL/screen_observer_client/`

Normal screen observer must not enable child control.

Safety constraints:

- no Android platform API calls;
- no screen capture runtime;
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

This layer is a shell bridge / policy projection layer for BATCH 4.4.
