# Phase 1A Rollback Plan

Stop with `tools/rest`. Revert only files listed in the Phase 1A audit manifest, using the preserved before patch/inventory and never reset/clean/checkout/restore/stash. Restore Phase 1 callback wiring, registry bridge and prior project/final adapters, compile, run Phase 1 tests, then restart. Invalid/non-project understanding still has per-request `legacy_rollback`; unavailable providers and Final Brain degrade without mutation.
