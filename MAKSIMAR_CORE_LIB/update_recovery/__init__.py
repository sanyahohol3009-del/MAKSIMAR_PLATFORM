from __future__ import annotations

from MAKSIMAR_CORE_LIB.update_recovery.existing_update_recovery_binding_models import (
    ExistingUpdateRecoveryBinding,
    ExistingUpdateRecoveryBindingMode,
    ExistingUpdateRecoveryBindingReadModel,
    ExistingUpdateRecoverySurfaceKind,
    UpdateRecoverySurfaceReadModel,
    build_existing_update_recovery_binding_read_model,
    build_existing_update_recovery_bindings,
    build_runtime_recovery_manager_binding,
    build_secure_sync_update_transport_binding,
    build_update_recovery_surface_read_model,
)

UPDATE_RECOVERY_CORE_PACKAGE_ID = "MAKSIMAR_CORE_LIB_UPDATE_RECOVERY"
UPDATE_RECOVERY_CORE_LAYER_ID = "UPDATE_RECOVERY_INFRA"
UPDATE_RECOVERY_CORE_CONTAINER_READY = True
UPDATE_RECOVERY_CORE_FACADE_WRAPPER_ONLY = True
UPDATE_RECOVERY_CORE_CANONICAL_WRITE_ALLOWED = False

__all__ = [
    "ExistingUpdateRecoveryBinding",
    "ExistingUpdateRecoveryBindingMode",
    "ExistingUpdateRecoveryBindingReadModel",
    "ExistingUpdateRecoverySurfaceKind",
    "UpdateRecoverySurfaceReadModel",
    "UPDATE_RECOVERY_CORE_PACKAGE_ID",
    "UPDATE_RECOVERY_CORE_LAYER_ID",
    "UPDATE_RECOVERY_CORE_CONTAINER_READY",
    "UPDATE_RECOVERY_CORE_FACADE_WRAPPER_ONLY",
    "UPDATE_RECOVERY_CORE_CANONICAL_WRITE_ALLOWED",
    "build_existing_update_recovery_binding_read_model",
    "build_existing_update_recovery_bindings",
    "build_runtime_recovery_manager_binding",
    "build_secure_sync_update_transport_binding",
    "build_update_recovery_surface_read_model",
]
