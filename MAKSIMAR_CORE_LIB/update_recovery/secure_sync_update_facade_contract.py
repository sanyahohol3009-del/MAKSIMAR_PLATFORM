from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SECURE_SYNC_UPDATE_FACADE_CONTRACT_ID = "secure_sync_update_facade_contract_v1"


@dataclass(frozen=True, slots=True)
class SecureSyncUpdateFacadeReadModel:
    read_model_id: str
    contract_id: str
    source_surface: str
    source_path: str
    facade_surface: str
    existing_transport_bound: bool
    replaces_existing_transport: bool
    transport_move_allowed: bool
    transport_delete_allowed: bool
    migration_allowed: bool
    signed_update_required: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    direct_apply_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if self.contract_id != SECURE_SYNC_UPDATE_FACADE_CONTRACT_ID:
            raise ValueError("contract_id must be secure_sync_update_facade_contract_v1")
        if self.source_surface != "secure_sync_update_transport":
            raise ValueError("source_surface must be secure_sync_update_transport")
        if "secure_sync_update_transport" not in self.source_path:
            raise ValueError("source_path must reference secure_sync_update_transport")
        if self.facade_surface != "UPDATE_RECOVERY":
            raise ValueError("facade_surface must be UPDATE_RECOVERY")
        if not self.existing_transport_bound:
            raise ValueError("existing_transport_bound must remain true")
        if self.replaces_existing_transport:
            raise ValueError("replaces_existing_transport must remain false")
        if self.transport_move_allowed:
            raise ValueError("transport_move_allowed must remain false")
        if self.transport_delete_allowed:
            raise ValueError("transport_delete_allowed must remain false")
        if self.migration_allowed:
            raise ValueError("migration_allowed must remain false")
        if not self.signed_update_required:
            raise ValueError("signed_update_required must remain true")
        _validate_reason_codes(self.reason_codes)
        _validate_safety_flags(
            dashboard_safe=self.dashboard_safe,
            direct_apply_allowed=self.direct_apply_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_execution_allowed=self.dashboard_execution_allowed,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "contract_id": self.contract_id,
            "source_surface": self.source_surface,
            "source_path": self.source_path,
            "facade_surface": self.facade_surface,
            "existing_transport_bound": self.existing_transport_bound,
            "replaces_existing_transport": self.replaces_existing_transport,
            "transport_move_allowed": self.transport_move_allowed,
            "transport_delete_allowed": self.transport_delete_allowed,
            "migration_allowed": self.migration_allowed,
            "signed_update_required": self.signed_update_required,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "direct_apply_allowed": self.direct_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_secure_sync_update_facade_read_model() -> SecureSyncUpdateFacadeReadModel:
    return SecureSyncUpdateFacadeReadModel(
        read_model_id="secure_sync_update_facade_read_model_v1",
        contract_id=SECURE_SYNC_UPDATE_FACADE_CONTRACT_ID,
        source_surface="secure_sync_update_transport",
        source_path="MAKSIMAR_CORE_LIB/secure_sync_update_transport/secure_sync_update_transport_contract.py",
        facade_surface="UPDATE_RECOVERY",
        existing_transport_bound=True,
        replaces_existing_transport=False,
        transport_move_allowed=False,
        transport_delete_allowed=False,
        migration_allowed=False,
        signed_update_required=True,
        reason_codes=("secure_sync_update_transport_preserved", "update_recovery_uses_facade_contract"),
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
    direct_apply_allowed: bool,
    canonical_write_allowed: bool,
    dashboard_execution_allowed: bool,
) -> None:
    if not dashboard_safe:
        raise ValueError("dashboard_safe must remain true")
    if direct_apply_allowed:
        raise ValueError("direct_apply_allowed must remain false")
    if canonical_write_allowed:
        raise ValueError("canonical_write_allowed must remain false")
    if dashboard_execution_allowed:
        raise ValueError("dashboard_execution_allowed must remain false")
