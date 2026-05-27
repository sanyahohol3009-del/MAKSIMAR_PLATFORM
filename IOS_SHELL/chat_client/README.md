# iOS Chat Client

BATCH 3.8 adds iOS-side chat client contracts and local bridges.

Scope:
- local iOS chat sync contract
- local iOS chat state bridge
- local iOS message store
- local iOS offline queue bridge
- local iOS notification bridge

Safety:
- no real iOS API calls
- no background task start
- no sockets
- no direct network access
- no direct server write
- no canonical truth write
- no command execution
- no plaintext message persistence
