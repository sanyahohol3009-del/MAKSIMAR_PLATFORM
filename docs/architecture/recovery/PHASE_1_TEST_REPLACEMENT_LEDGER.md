# Phase 1 Test Replacement Ledger

No legacy test is deleted in Phase 1.

- Phrase/marker router tests remain tests of `legacy_rollback` only.
- New semantic acceptance tests use injected model JSON and assert schemas,
  capabilities, policy, evidence and trace invariants rather than exact prose.
- Exact output checks are retained only for machine-readable safety contracts.
- A legacy test may be retired only in a later phase after an equivalent semantic
  acceptance test and client migration are documented.

