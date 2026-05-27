# Android Chat Client

BATCH 3.6 adds Android-side chat client contracts and local bridges.

Scope:
- local Android chat sync contract
- local Android chat state bridge
- local Android message store
- local Android offline queue bridge
- local Android notification bridge

Safety:
- no real Android API calls
- no background service start
- no sockets
- no direct network access
- no direct server write
- no canonical truth write
- no command execution
- no plaintext message persistence
