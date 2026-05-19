from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.secure_sync_update_facade_contract import (
    SecureSyncUpdateFacadeReadModel,
    build_secure_sync_update_facade_read_model,
)


SECURE_SYNC_UPDATE_TRANSPORT_ADAPTER_ID = "secure_sync_update_transport_adapter_v1"
SECURE_SYNC_UPDATE_TRANSPORT_CONTRACT_PATH = (
    "MAKSIMAR_CORE_LIB/secure_sync_update_transport/secure_sync_update_transport_contract.py"
)


@dataclass(frozen=True, slots=True)
class SecureSyncUpdateTransportAdapterReadModel:
    adapter_id: str
    source_path: str
    facade_read_model: SecureSyncUpdateFacadeReadModel
    source_exists: bool
    adapter_bound: bool
    replaces_existing_transport: bool
    move_allowed: bool
    delete_allowed: bool
    migration_allowed: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_apply_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if self.adapter_id != SECURE_SYNC_UPDATE_TRANSPORT_ADAPTER_ID:
            raise ValueError("adapter_id must be secure_sync_update_transport_adapter_v1")
        _validate_non_empty("source_path", self.source_path)
        if not isinstance(self.facade_read_model, SecureSyncUpdateFacadeReadModel):
            raise TypeError("facade_read_model must be SecureSyncUpdateFacadeReadModel")
        if not self.adapter_bound:
            raise ValueError("adapter_bound must remain true")
        if self.replaces_existing_transport:
            raise ValueError("replaces_existing_transport must remain false")
        if self.move_allowed:
            raise ValueError("move_allowed must remain false")
        if self.delete_allowed:
            raise ValueError("delete_allowed must remain false")
        if self.migration_allowed:
            raise ValueError("migration_allowed must remain false")
        _validate_reason_codes(self.reason_codes)
        _validate_safety_flags(
            dashboard_safe=self.dashboard_safe,
            runtime_apply_allowed=self.runtime_apply_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_execution_allowed=self.dashboard_execution_allowed,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "source_path": self.source_path,
            "facade_read_model": self.facade_read_model.to_dict(),
            "source_exists": self.source_exists,
            "adapter_bound": self.adapter_bound,
            "replaces_existing_transport": self.replaces_existing_transport,
            "move_allowed": self.move_allowed,
            "delete_allowed": self.delete_allowed,
            "migration_allowed": self.migration_allowed,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "runtime_apply_allowed": self.runtime_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_secure_sync_update_transport_adapter_read_model(
    *,
    project_root: Path | None = None,
) -> SecureSyncUpdateTransportAdapterReadModel:
    root = Path.cwd() if project_root is None else project_root
    source_path = SECURE_SYNC_UPDATE_TRANSPORT_CONTRACT_PATH
    source_exists = (root / source_path).exists()
    reason_codes = (
        "secure_sync_update_transport_adapter_bound",
        "existing_transport_preserved",
        "facade_contract_bound",
    )
    if not source_exists:
        reason_codes = reason_codes + ("existing_transport_source_not_found_by_filesystem_scan",)

    return SecureSyncUpdateTransportAdapterReadModel(
        adapter_id=SECURE_SYNC_UPDATE_TRANSPORT_ADAPTER_ID,
        source_path=source_path,
        facade_read_model=build_secure_sync_update_facade_read_model(),
        source_exists=source_exists,
        adapter_bound=True,
        replaces_existing_transport=False,
        move_allowed=False,
        delete_allowed=False,
        migration_allowed=False,
        reason_codes=reason_codes,
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        _validate_non_empty("reason_code", reason_code)


def _validate_safety_flags(
    *,
    dashboard_safe: bool,
    runtime_apply_allowed: bool,
    canonical_write_allowed: bool,
    dashboard_execution_allowed: bool,
) -> None:
    if not dashboard_safe:
        raise ValueError("dashboard_safe must remain true")
    if runtime_apply_allowed:
        raise ValueError("runtime_apply_allowed must remain false")
    if canonical_write_allowed:
        raise ValueError("canonical_write_allowed must remain false")
    if dashboard_execution_allowed:
        raise ValueError("dashboard_execution_allowed must remain false")
