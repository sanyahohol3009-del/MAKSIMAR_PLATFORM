# UPDATE_RECOVERY PHASE 3 Roadmap Reconciliation v1

## Status

Required correction before PHASE 3 / BATCH 3.1 implementation.

## Printed roadmap source

PHASE 3 — UPDATE_RECOVERY_INFRA FOUNDATION v1

BATCH 3.1 — Update/Recovery Surface + Existing Binding

## Decision

Current foundation roadmap JSON did not contain PHASE 3 / BATCH 3.1.

PHASE 3 / BATCH 3.1 is added as a roadmap correction before implementation.

## Required rule

- secure_sync_update_transport is existing foundation.
- update_recovery is facade/wrapper.
- RUNTIME/recovery_manager.py must not be moved.
- No move.
- No delete.
- No migration.
- Existing update/recovery surfaces are bound through explicit existing_bindings.
- Dashboard/read-model exposure remains read-only.
- Runtime recovery behavior is not changed in BATCH 3.1.

## Required BATCH 3.1 files

- UPDATE_RECOVERY/README.md
- UPDATE_RECOVERY/container_contract.yaml
- UPDATE_RECOVERY/config/update_recovery_policy.yaml
- MAKSIMAR_CORE_LIB/update_recovery/__init__.py
- MAKSIMAR_SERVER/UPDATE_RECOVERY/__init__.py
- UPDATE_RECOVERY/layer_manifest.yaml
- UPDATE_RECOVERY/boundaries/container_adapter_boundary.yaml
- UPDATE_RECOVERY/existing_bindings/secure_sync_update_transport_binding.yaml
- UPDATE_RECOVERY/existing_bindings/runtime_recovery_manager_binding.yaml
- MAKSIMAR_CORE_LIB/update_recovery/existing_update_recovery_binding_models.py

## Required BATCH 3.1 tests

- tests/update_recovery/test_existing_update_recovery_binding_models_smoke.py
