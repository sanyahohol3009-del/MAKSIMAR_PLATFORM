from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.update_recovery import (
    UPDATE_RECOVERY_CORE_CANONICAL_WRITE_ALLOWED,
    UPDATE_RECOVERY_CORE_CONTAINER_READY,
    UPDATE_RECOVERY_CORE_FACADE_WRAPPER_ONLY,
)
from MAKSIMAR_CORE_LIB.update_recovery.existing_update_recovery_binding_models import (
    ExistingUpdateRecoveryBinding,
    ExistingUpdateRecoveryBindingMode,
    ExistingUpdateRecoverySurfaceKind,
    build_existing_update_recovery_binding_read_model,
    build_existing_update_recovery_bindings,
    build_runtime_recovery_manager_binding,
    build_secure_sync_update_transport_binding,
    build_update_recovery_surface_read_model,
)
from MAKSIMAR_SERVER.UPDATE_RECOVERY import (
    UPDATE_RECOVERY_SERVER_CANONICAL_WRITE_ALLOWED,
    UPDATE_RECOVERY_SERVER_CONTAINER_READY,
    UPDATE_RECOVERY_SERVER_DASHBOARD_EXECUTION_ALLOWED,
    UPDATE_RECOVERY_SERVER_FACADE_WRAPPER_ONLY,
    UPDATE_RECOVERY_SERVER_RUNTIME_BEHAVIOR_CHANGE_ALLOWED,
)


def test_update_recovery_surface_files_exist() -> None:
    required_paths = (
        "UPDATE_RECOVERY/README.md",
        "UPDATE_RECOVERY/container_contract.yaml",
        "UPDATE_RECOVERY/config/update_recovery_policy.yaml",
        "UPDATE_RECOVERY/layer_manifest.yaml",
        "UPDATE_RECOVERY/boundaries/container_adapter_boundary.yaml",
        "UPDATE_RECOVERY/existing_bindings/secure_sync_update_transport_binding.yaml",
        "UPDATE_RECOVERY/existing_bindings/runtime_recovery_manager_binding.yaml",
        "MAKSIMAR_CORE_LIB/update_recovery/__init__.py",
        "MAKSIMAR_SERVER/UPDATE_RECOVERY/__init__.py",
    )

    for required_path in required_paths:
        assert Path(required_path).exists(), required_path


def test_update_recovery_package_boundaries_are_container_ready_facades() -> None:
    assert UPDATE_RECOVERY_CORE_CONTAINER_READY is True
    assert UPDATE_RECOVERY_CORE_FACADE_WRAPPER_ONLY is True
    assert UPDATE_RECOVERY_CORE_CANONICAL_WRITE_ALLOWED is False

    assert UPDATE_RECOVERY_SERVER_CONTAINER_READY is True
    assert UPDATE_RECOVERY_SERVER_FACADE_WRAPPER_ONLY is True
    assert UPDATE_RECOVERY_SERVER_CANONICAL_WRITE_ALLOWED is False
    assert UPDATE_RECOVERY_SERVER_RUNTIME_BEHAVIOR_CHANGE_ALLOWED is False
    assert UPDATE_RECOVERY_SERVER_DASHBOARD_EXECUTION_ALLOWED is False


def test_existing_update_recovery_bindings_preserve_sources_in_place() -> None:
    secure_sync_binding = build_secure_sync_update_transport_binding()
    recovery_manager_binding = build_runtime_recovery_manager_binding()

    assert secure_sync_binding.source_surface_kind is ExistingUpdateRecoverySurfaceKind.SECURE_SYNC_UPDATE_TRANSPORT
    assert "secure_sync_update_transport" in secure_sync_binding.source_path
    assert secure_sync_binding.move_source_allowed is False
    assert secure_sync_binding.delete_source_allowed is False
    assert secure_sync_binding.migration_allowed is False

    assert recovery_manager_binding.source_surface_kind is ExistingUpdateRecoverySurfaceKind.RUNTIME_RECOVERY_MANAGER
    assert recovery_manager_binding.source_path == "RUNTIME/recovery_manager.py"
    assert recovery_manager_binding.move_source_allowed is False
    assert recovery_manager_binding.runtime_behavior_change_allowed is False


def test_existing_update_recovery_binding_read_model_is_dashboard_safe() -> None:
    bindings = build_existing_update_recovery_bindings()
    read_model = build_existing_update_recovery_binding_read_model(bindings)

    assert read_model.binding_count == 2
    assert read_model.secure_sync_update_transport_bound is True
    assert read_model.runtime_recovery_manager_bound is True
    assert read_model.dashboard_safe is True
    assert read_model.source_move_allowed is False
    assert read_model.source_delete_allowed is False
    assert read_model.migration_allowed is False
    assert read_model.runtime_behavior_change_allowed is False
    assert read_model.canonical_write_allowed is False
    assert read_model.dashboard_execution_allowed is False
    assert read_model.container_disable_safe is True


def test_update_recovery_surface_read_model_is_container_ready_facade() -> None:
    surface = build_update_recovery_surface_read_model()

    assert surface.layer_id == "UPDATE_RECOVERY_INFRA"
    assert surface.surface_root == "UPDATE_RECOVERY"
    assert surface.container_ready is True
    assert surface.facade_wrapper_only is True
    assert surface.source_move_allowed is False
    assert surface.source_delete_allowed is False
    assert surface.migration_allowed is False
    assert surface.runtime_behavior_change_allowed is False
    assert surface.canonical_write_allowed is False
    assert surface.dashboard_execution_allowed is False
    assert surface.container_disable_safe is True
    assert surface.existing_binding_read_model.binding_count == 2


def test_existing_update_recovery_binding_rejects_source_move() -> None:
    with pytest.raises(ValueError, match="move_source_allowed"):
        ExistingUpdateRecoveryBinding(
            binding_id="bad_binding",
            layer_id="UPDATE_RECOVERY_INFRA",
            source_surface_kind=ExistingUpdateRecoverySurfaceKind.RUNTIME_RECOVERY_MANAGER,
            source_path="RUNTIME/recovery_manager.py",
            binding_mode=ExistingUpdateRecoveryBindingMode.REFERENCE_ONLY_FACADE,
            target_surface="UPDATE_RECOVERY",
            container_adapter_required=True,
            move_source_allowed=True,
            delete_source_allowed=False,
            migration_allowed=False,
            runtime_behavior_change_allowed=False,
            canonical_write_allowed=False,
            dashboard_execution_allowed=False,
            container_disable_safe=True,
            reason_codes=("bad",),
        )


def test_runtime_recovery_manager_binding_rejects_wrong_source_path() -> None:
    with pytest.raises(ValueError, match="RUNTIME/recovery_manager.py"):
        ExistingUpdateRecoveryBinding(
            binding_id="bad_runtime_binding",
            layer_id="UPDATE_RECOVERY_INFRA",
            source_surface_kind=ExistingUpdateRecoverySurfaceKind.RUNTIME_RECOVERY_MANAGER,
            source_path="UPDATE_RECOVERY/recovery_manager.py",
            binding_mode=ExistingUpdateRecoveryBindingMode.REFERENCE_ONLY_FACADE,
            target_surface="UPDATE_RECOVERY",
            container_adapter_required=True,
            move_source_allowed=False,
            delete_source_allowed=False,
            migration_allowed=False,
            runtime_behavior_change_allowed=False,
            canonical_write_allowed=False,
            dashboard_execution_allowed=False,
            container_disable_safe=True,
            reason_codes=("bad",),
        )
