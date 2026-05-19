from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


SNAPSHOT_MANAGER_CONTRACT_ID = "snapshot_manager_contract_v1"


class SnapshotReadinessStatus(str, Enum):
    READY = "ready"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class SnapshotReference:
    snapshot_id: str
    snapshot_uri: str
    snapshot_sha256: str
    created_at_utc: str
    immutable: bool
    state_manifest_present: bool
    rollback_compatible: bool

    def __post_init__(self) -> None:
        _validate_non_empty("snapshot_id", self.snapshot_id)
        _validate_non_empty("snapshot_uri", self.snapshot_uri)
        _validate_sha256("snapshot_sha256", self.snapshot_sha256)
        _validate_utc_timestamp("created_at_utc", self.created_at_utc)
        if not self.immutable:
            raise ValueError("immutable must remain true")
        if not self.state_manifest_present:
            raise ValueError("state_manifest_present must remain true")
        if not self.rollback_compatible:
            raise ValueError("rollback_compatible must remain true")

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "snapshot_uri": self.snapshot_uri,
            "snapshot_sha256": self.snapshot_sha256,
            "created_at_utc": self.created_at_utc,
            "immutable": self.immutable,
            "state_manifest_present": self.state_manifest_present,
            "rollback_compatible": self.rollback_compatible,
        }


@dataclass(frozen=True, slots=True)
class SnapshotManagerReadinessReadModel:
    read_model_id: str
    contract_id: str
    package_id: str
    status: SnapshotReadinessStatus
    snapshot_reference: SnapshotReference | None
    snapshot_ready: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    direct_apply_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if self.contract_id != SNAPSHOT_MANAGER_CONTRACT_ID:
            raise ValueError("contract_id must be snapshot_manager_contract_v1")
        _validate_non_empty("package_id", self.package_id)
        if not isinstance(self.status, SnapshotReadinessStatus):
            raise TypeError("status must be SnapshotReadinessStatus")
        if self.status is SnapshotReadinessStatus.READY:
            if not self.snapshot_ready:
                raise ValueError("READY snapshot readiness requires snapshot_ready true")
            if not isinstance(self.snapshot_reference, SnapshotReference):
                raise ValueError("READY snapshot readiness requires snapshot_reference")
        if self.status is SnapshotReadinessStatus.BLOCKED and self.snapshot_ready:
            raise ValueError("BLOCKED snapshot readiness cannot have snapshot_ready true")
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
            "package_id": self.package_id,
            "status": self.status.value,
            "snapshot_reference": None if self.snapshot_reference is None else self.snapshot_reference.to_dict(),
            "snapshot_ready": self.snapshot_ready,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "direct_apply_allowed": self.direct_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_snapshot_ready_read_model(
    *,
    package_id: str,
    snapshot_reference: SnapshotReference,
) -> SnapshotManagerReadinessReadModel:
    return SnapshotManagerReadinessReadModel(
        read_model_id=f"snapshot_manager_readiness:{package_id}",
        contract_id=SNAPSHOT_MANAGER_CONTRACT_ID,
        package_id=package_id,
        status=SnapshotReadinessStatus.READY,
        snapshot_reference=snapshot_reference,
        snapshot_ready=True,
        reason_codes=("snapshot_available", "snapshot_immutable", "snapshot_rollback_compatible"),
    )


def build_snapshot_blocked_read_model(
    *,
    package_id: str,
    reason_codes: tuple[str, ...],
) -> SnapshotManagerReadinessReadModel:
    return SnapshotManagerReadinessReadModel(
        read_model_id=f"snapshot_manager_readiness:{package_id}",
        contract_id=SNAPSHOT_MANAGER_CONTRACT_ID,
        package_id=package_id,
        status=SnapshotReadinessStatus.BLOCKED,
        snapshot_reference=None,
        snapshot_ready=False,
        reason_codes=reason_codes,
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_sha256(field_name: str, value: str) -> None:
    _validate_non_empty(field_name, value)
    if len(value) != 64:
        raise ValueError(f"{field_name} must be a 64-character sha256 hex string")
    int(value, 16)


def _validate_utc_timestamp(field_name: str, value: str) -> None:
    _validate_non_empty(field_name, value)
    if "T" not in value or not value.endswith("Z"):
        raise ValueError(f"{field_name} must be an ISO-like UTC timestamp ending with Z")


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
