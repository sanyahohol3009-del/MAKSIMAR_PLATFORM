from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class ExistingUpdateRecoverySurfaceKind(str, Enum):
    SECURE_SYNC_UPDATE_TRANSPORT = "secure_sync_update_transport"
    RUNTIME_RECOVERY_MANAGER = "runtime_recovery_manager"


class ExistingUpdateRecoveryBindingMode(str, Enum):
    REFERENCE_ONLY_FACADE = "reference_only_facade"


@dataclass(frozen=True, slots=True)
class ExistingUpdateRecoveryBinding:
    binding_id: str
    layer_id: str
    source_surface_kind: ExistingUpdateRecoverySurfaceKind
    source_path: str
    binding_mode: ExistingUpdateRecoveryBindingMode
    target_surface: str
    container_adapter_required: bool
    move_source_allowed: bool
    delete_source_allowed: bool
    migration_allowed: bool
    runtime_behavior_change_allowed: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    container_disable_safe: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True

    def __post_init__(self) -> None:
        for field_name, value in (
            ("binding_id", self.binding_id),
            ("layer_id", self.layer_id),
            ("source_path", self.source_path),
            ("target_surface", self.target_surface),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if self.layer_id != "UPDATE_RECOVERY_INFRA":
            raise ValueError("layer_id must be UPDATE_RECOVERY_INFRA")
        if not isinstance(self.source_surface_kind, ExistingUpdateRecoverySurfaceKind):
            raise TypeError("source_surface_kind must be ExistingUpdateRecoverySurfaceKind")
        if not isinstance(self.binding_mode, ExistingUpdateRecoveryBindingMode):
            raise TypeError("binding_mode must be ExistingUpdateRecoveryBindingMode")
        if self.target_surface != "UPDATE_RECOVERY":
            raise ValueError("target_surface must be UPDATE_RECOVERY")
        if not self.container_adapter_required:
            raise ValueError("container_adapter_required must remain true")
        if self.move_source_allowed:
            raise ValueError("move_source_allowed must remain false")
        if self.delete_source_allowed:
            raise ValueError("delete_source_allowed must remain false")
        if self.migration_allowed:
            raise ValueError("migration_allowed must remain false")
        if self.runtime_behavior_change_allowed:
            raise ValueError("runtime_behavior_change_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.dashboard_execution_allowed:
            raise ValueError("dashboard_execution_allowed must remain false")
        if not self.container_disable_safe:
            raise ValueError("container_disable_safe must remain true")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        _validate_reason_codes(self.reason_codes)

        if (
            self.source_surface_kind is ExistingUpdateRecoverySurfaceKind.SECURE_SYNC_UPDATE_TRANSPORT
            and "secure_sync_update_transport" not in self.source_path
        ):
            raise ValueError("secure_sync_update_transport binding must reference secure_sync_update_transport path")

        if (
            self.source_surface_kind is ExistingUpdateRecoverySurfaceKind.RUNTIME_RECOVERY_MANAGER
            and self.source_path != "RUNTIME/recovery_manager.py"
        ):
            raise ValueError("runtime_recovery_manager binding must keep source_path RUNTIME/recovery_manager.py")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["source_surface_kind"] = self.source_surface_kind.value
        payload["binding_mode"] = self.binding_mode.value
        return payload


@dataclass(frozen=True, slots=True)
class ExistingUpdateRecoveryBindingReadModel:
    read_model_id: str
    layer_id: str
    binding_count: int
    secure_sync_update_transport_bound: bool
    runtime_recovery_manager_bound: bool
    source_move_allowed: bool
    source_delete_allowed: bool
    migration_allowed: bool
    runtime_behavior_change_allowed: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    container_disable_safe: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True

    def __post_init__(self) -> None:
        if not self.read_model_id:
            raise ValueError("read_model_id must not be empty")
        if self.layer_id != "UPDATE_RECOVERY_INFRA":
            raise ValueError("layer_id must be UPDATE_RECOVERY_INFRA")
        if self.binding_count != 2:
            raise ValueError("binding_count must be 2 for BATCH 3.1")
        if not self.secure_sync_update_transport_bound:
            raise ValueError("secure_sync_update_transport_bound must remain true")
        if not self.runtime_recovery_manager_bound:
            raise ValueError("runtime_recovery_manager_bound must remain true")
        if self.source_move_allowed:
            raise ValueError("source_move_allowed must remain false")
        if self.source_delete_allowed:
            raise ValueError("source_delete_allowed must remain false")
        if self.migration_allowed:
            raise ValueError("migration_allowed must remain false")
        if self.runtime_behavior_change_allowed:
            raise ValueError("runtime_behavior_change_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.dashboard_execution_allowed:
            raise ValueError("dashboard_execution_allowed must remain false")
        if not self.container_disable_safe:
            raise ValueError("container_disable_safe must remain true")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class UpdateRecoverySurfaceReadModel:
    read_model_id: str
    layer_id: str
    surface_root: str
    core_package: str
    server_package: str
    container_contract_path: str
    policy_path: str
    bindings: tuple[ExistingUpdateRecoveryBinding, ...]
    existing_binding_read_model: ExistingUpdateRecoveryBindingReadModel
    container_ready: bool
    facade_wrapper_only: bool
    source_move_allowed: bool
    source_delete_allowed: bool
    migration_allowed: bool
    runtime_behavior_change_allowed: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    container_disable_safe: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True

    def __post_init__(self) -> None:
        for field_name, value in (
            ("read_model_id", self.read_model_id),
            ("surface_root", self.surface_root),
            ("core_package", self.core_package),
            ("server_package", self.server_package),
            ("container_contract_path", self.container_contract_path),
            ("policy_path", self.policy_path),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if self.layer_id != "UPDATE_RECOVERY_INFRA":
            raise ValueError("layer_id must be UPDATE_RECOVERY_INFRA")
        if self.surface_root != "UPDATE_RECOVERY":
            raise ValueError("surface_root must be UPDATE_RECOVERY")
        if not isinstance(self.bindings, tuple):
            raise TypeError("bindings must be a tuple")
        if len(self.bindings) != 2:
            raise ValueError("bindings must contain exactly 2 entries")
        for binding in self.bindings:
            if not isinstance(binding, ExistingUpdateRecoveryBinding):
                raise TypeError("bindings must contain ExistingUpdateRecoveryBinding")
        if not isinstance(self.existing_binding_read_model, ExistingUpdateRecoveryBindingReadModel):
            raise TypeError("existing_binding_read_model must be ExistingUpdateRecoveryBindingReadModel")
        if not self.container_ready:
            raise ValueError("container_ready must remain true")
        if not self.facade_wrapper_only:
            raise ValueError("facade_wrapper_only must remain true")
        if self.source_move_allowed:
            raise ValueError("source_move_allowed must remain false")
        if self.source_delete_allowed:
            raise ValueError("source_delete_allowed must remain false")
        if self.migration_allowed:
            raise ValueError("migration_allowed must remain false")
        if self.runtime_behavior_change_allowed:
            raise ValueError("runtime_behavior_change_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.dashboard_execution_allowed:
            raise ValueError("dashboard_execution_allowed must remain false")
        if not self.container_disable_safe:
            raise ValueError("container_disable_safe must remain true")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "layer_id": self.layer_id,
            "surface_root": self.surface_root,
            "core_package": self.core_package,
            "server_package": self.server_package,
            "container_contract_path": self.container_contract_path,
            "policy_path": self.policy_path,
            "bindings": tuple(binding.to_dict() for binding in self.bindings),
            "existing_binding_read_model": self.existing_binding_read_model.to_dict(),
            "container_ready": self.container_ready,
            "facade_wrapper_only": self.facade_wrapper_only,
            "source_move_allowed": self.source_move_allowed,
            "source_delete_allowed": self.source_delete_allowed,
            "migration_allowed": self.migration_allowed,
            "runtime_behavior_change_allowed": self.runtime_behavior_change_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "container_disable_safe": self.container_disable_safe,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
        }


def build_secure_sync_update_transport_binding() -> ExistingUpdateRecoveryBinding:
    return ExistingUpdateRecoveryBinding(
        binding_id="secure_sync_update_transport_binding_v1",
        layer_id="UPDATE_RECOVERY_INFRA",
        source_surface_kind=ExistingUpdateRecoverySurfaceKind.SECURE_SYNC_UPDATE_TRANSPORT,
        source_path="MAKSIMAR_CORE_LIB/secure_sync_update_transport/secure_sync_update_transport_contract.py",
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
        reason_codes=(
            "secure_sync_update_transport_reused_as_existing_foundation",
            "update_recovery_surface_binds_without_replacement",
        ),
    )


def build_runtime_recovery_manager_binding() -> ExistingUpdateRecoveryBinding:
    return ExistingUpdateRecoveryBinding(
        binding_id="runtime_recovery_manager_binding_v1",
        layer_id="UPDATE_RECOVERY_INFRA",
        source_surface_kind=ExistingUpdateRecoverySurfaceKind.RUNTIME_RECOVERY_MANAGER,
        source_path="RUNTIME/recovery_manager.py",
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
        reason_codes=(
            "runtime_recovery_manager_bound_in_place",
            "runtime_recovery_manager_source_not_moved",
        ),
    )


def build_existing_update_recovery_bindings() -> tuple[ExistingUpdateRecoveryBinding, ...]:
    return (
        build_secure_sync_update_transport_binding(),
        build_runtime_recovery_manager_binding(),
    )


def build_existing_update_recovery_binding_read_model(
    bindings: tuple[ExistingUpdateRecoveryBinding, ...],
) -> ExistingUpdateRecoveryBindingReadModel:
    if not isinstance(bindings, tuple):
        raise TypeError("bindings must be a tuple")
    secure_sync_bound = any(
        binding.source_surface_kind is ExistingUpdateRecoverySurfaceKind.SECURE_SYNC_UPDATE_TRANSPORT
        for binding in bindings
    )
    runtime_recovery_bound = any(
        binding.source_surface_kind is ExistingUpdateRecoverySurfaceKind.RUNTIME_RECOVERY_MANAGER
        for binding in bindings
    )

    return ExistingUpdateRecoveryBindingReadModel(
        read_model_id="existing_update_recovery_binding_read_model_v1",
        layer_id="UPDATE_RECOVERY_INFRA",
        binding_count=len(bindings),
        secure_sync_update_transport_bound=secure_sync_bound,
        runtime_recovery_manager_bound=runtime_recovery_bound,
        source_move_allowed=False,
        source_delete_allowed=False,
        migration_allowed=False,
        runtime_behavior_change_allowed=False,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        container_disable_safe=True,
        reason_codes=(
            "existing_update_recovery_bindings_validated",
            "source_surfaces_bound_without_move_delete_migration",
        ),
    )


def build_update_recovery_surface_read_model() -> UpdateRecoverySurfaceReadModel:
    bindings = build_existing_update_recovery_bindings()
    existing_binding_read_model = build_existing_update_recovery_binding_read_model(bindings)

    return UpdateRecoverySurfaceReadModel(
        read_model_id="update_recovery_surface_read_model_v1",
        layer_id="UPDATE_RECOVERY_INFRA",
        surface_root="UPDATE_RECOVERY",
        core_package="MAKSIMAR_CORE_LIB/update_recovery",
        server_package="MAKSIMAR_SERVER/UPDATE_RECOVERY",
        container_contract_path="UPDATE_RECOVERY/container_contract.yaml",
        policy_path="UPDATE_RECOVERY/config/update_recovery_policy.yaml",
        bindings=bindings,
        existing_binding_read_model=existing_binding_read_model,
        container_ready=True,
        facade_wrapper_only=True,
        source_move_allowed=False,
        source_delete_allowed=False,
        migration_allowed=False,
        runtime_behavior_change_allowed=False,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        container_disable_safe=True,
        reason_codes=(
            "update_recovery_surface_created_as_container_ready_facade",
            "existing_foundations_preserved",
        ),
    )


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        if not reason_code:
            raise ValueError("reason_codes must not contain empty values")
