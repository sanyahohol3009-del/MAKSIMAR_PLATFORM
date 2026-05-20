# UPDATE_RECOVERY Existing Binding Review v1

## Existing bindings

UPDATE_RECOVERY_INFRA binds to existing surfaces without replacing them.

## secure_sync_update_transport

secure_sync_update_transport is an existing foundation.

Rules:

- preserve existing transport;
- wrap through adapter/facade only;
- do not replace;
- do not move;
- do not delete;
- do not migrate;
- do not create a parallel transport with the same responsibility.

Binding surfaces:

- UPDATE_RECOVERY/existing_bindings/secure_sync_update_transport_binding.yaml
- MAKSIMAR_CORE_LIB/update_recovery/secure_sync_update_facade_contract.py
- MAKSIMAR_SERVER/UPDATE_RECOVERY/adapters/secure_sync_update_transport_adapter.py

## RUNTIME/recovery_manager.py

RUNTIME/recovery_manager.py is an existing recovery manager source.

Rules:

- preserve existing recovery manager;
- wrap through adapter only;
- do not replace;
- do not move;
- do not delete;
- do not migrate.

Binding surfaces:

- UPDATE_RECOVERY/existing_bindings/runtime_recovery_manager_binding.yaml
- MAKSIMAR_SERVER/UPDATE_RECOVERY/adapters/runtime_recovery_manager_adapter.py

## Semantic duplicate decision

The related adapter surfaces are intentional boundary duplication.

They are allowed only because they are adapter/facade surfaces and do not duplicate business authority.

The existing sources remain source surfaces. UPDATE_RECOVERY wrappers expose dashboard-safe readiness/read-model outputs.
