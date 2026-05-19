# UPDATE_RECOVERY BATCH 3.4 Roadmap Reconciliation v1

## Batch

BATCH 3.4 — Runtime Services + Preview

## Printed roadmap source

Base files / v2:

- update_signature_verifier.py
- signed_update_service.py
- snapshot_manager.py
- rollback_manager.py
- recovery_service.py
- offline_import_gate.py
- update_recovery_health.py
- update_recovery_read_model_builder.py
- preview tools

Canonical implementation paths:

- MAKSIMAR_SERVER/UPDATE_RECOVERY/update_signature_verifier.py
- MAKSIMAR_SERVER/UPDATE_RECOVERY/signed_update_service.py
- MAKSIMAR_SERVER/UPDATE_RECOVERY/snapshot_manager.py
- MAKSIMAR_SERVER/UPDATE_RECOVERY/rollback_manager.py
- MAKSIMAR_SERVER/UPDATE_RECOVERY/recovery_service.py
- MAKSIMAR_SERVER/UPDATE_RECOVERY/offline_import_gate.py
- MAKSIMAR_SERVER/UPDATE_RECOVERY/update_recovery_health.py
- MAKSIMAR_SERVER/UPDATE_RECOVERY/update_recovery_read_model_builder.py
- tools/monitor/runtime_input/update_recovery_terminal_preview.py
- tools/monitor/runtime_input/update_recovery_web_preview.py

Correction additions:

- MAKSIMAR_SERVER/UPDATE_RECOVERY/adapters/__init__.py
- MAKSIMAR_SERVER/UPDATE_RECOVERY/adapters/secure_sync_update_transport_adapter.py
- MAKSIMAR_SERVER/UPDATE_RECOVERY/adapters/runtime_recovery_manager_adapter.py

Printed tests:

- tests/update_recovery/test_secure_sync_update_transport_adapter_smoke.py
- tests/update_recovery/test_runtime_recovery_manager_adapter_smoke.py

Correction coverage tests:

- tests/update_recovery/test_update_recovery_runtime_services_smoke.py
- tests/update_recovery/test_update_recovery_health_smoke.py
- tests/update_recovery/test_update_recovery_read_model_builder_smoke.py
- tests/update_recovery/test_update_recovery_terminal_preview_smoke.py
- tests/update_recovery/test_update_recovery_web_preview_smoke.py

Dashboard / read model:

- UpdateRecoveryRuntimeReadModel

Acceptance / gates:

- Runtime wrapper only.
- Preserve existing transport and recovery manager.
- secure_sync_update_transport is wrapped, not replaced.
- RUNTIME/recovery_manager.py is wrapped, not moved.
- No move.
- No delete.
- No migration.
- No direct runtime update apply.
- No direct canonical write.
- No dashboard execution.
- Preview/read-model outputs are dashboard-safe and read-only.

## Implementation mode

- CREATE ONLY.
- Use adapters/facades for existing foundations.
- Do not replace existing secure_sync_update_transport.
- Do not move or mutate RUNTIME/recovery_manager.py.
- Do not add production deployment or network exposure in this batch.
