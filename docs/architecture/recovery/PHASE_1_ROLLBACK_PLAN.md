# Phase 1 Rollback Plan

1. Stop the runtime with the existing `tools/rest` lifecycle command.
2. Revert only the Phase 1 files listed in the audit changed-files manifest using
   the preserved pre-phase patch/state; do not reset or clean the repository.
3. Restore `jarvis_live_hot` to its direct call to `handle_hot_request`.
4. Run compileall and the pre-existing Control Plane/hotpath tests.
5. Restart through `tools/work` and verify `/health`.

Runtime rollback is always available per request: invalid/unavailable understanding,
non-project requests and unavailable canonical dependencies use
`orchestration_path=legacy_rollback` without deleting either implementation.
