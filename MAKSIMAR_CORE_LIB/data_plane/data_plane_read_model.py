from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class DataPlaneAppendLogReadModel:
    append_log_id: str
    stream_id: str
    log_path: str
    record_count: int
    head_hash: str
    latest_record_id: str
    write_performed: bool
    append_only_enforced: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    preview_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_mutation_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("append_log_id", self.append_log_id),
            ("stream_id", self.stream_id),
            ("log_path", self.log_path),
            ("head_hash", self.head_hash),
            ("latest_record_id", self.latest_record_id),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if self.record_count < 0:
            raise ValueError("record_count must not be negative")
        _validate_sha256("head_hash", self.head_hash)
        if not self.append_only_enforced:
            raise ValueError("append_only_enforced must remain true")
        _validate_reason_codes(self.reason_codes)
        _validate_safe_flags(
            dashboard_safe=self.dashboard_safe,
            preview_safe=self.preview_safe,
            runtime_mutation_allowed=self.runtime_mutation_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_mutation_allowed=self.dashboard_mutation_allowed,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class DataPlaneLedgerReadModel:
    ledger_adapter_id: str
    ledger_id: str
    ledger_path: str
    entry_count: int
    head_hash: str
    latest_entry_id: str
    write_performed: bool
    immutable_ledger_enforced: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    preview_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_mutation_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("ledger_adapter_id", self.ledger_adapter_id),
            ("ledger_id", self.ledger_id),
            ("ledger_path", self.ledger_path),
            ("head_hash", self.head_hash),
            ("latest_entry_id", self.latest_entry_id),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if self.entry_count < 0:
            raise ValueError("entry_count must not be negative")
        _validate_sha256("head_hash", self.head_hash)
        if not self.immutable_ledger_enforced:
            raise ValueError("immutable_ledger_enforced must remain true")
        _validate_reason_codes(self.reason_codes)
        _validate_safe_flags(
            dashboard_safe=self.dashboard_safe,
            preview_safe=self.preview_safe,
            runtime_mutation_allowed=self.runtime_mutation_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_mutation_allowed=self.dashboard_mutation_allowed,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class DataPlaneHealthReadModel:
    layer_id: str
    status: str
    checked_paths: tuple[str, ...]
    missing_paths: tuple[str, ...]
    health_ok: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    preview_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_mutation_allowed: bool = False

    def __post_init__(self) -> None:
        if self.layer_id != "DATA_PLANE":
            raise ValueError("layer_id must be DATA_PLANE")
        if self.status not in {"ready", "degraded"}:
            raise ValueError("status must be ready or degraded")
        _validate_string_tuple("checked_paths", self.checked_paths, allow_empty=False)
        _validate_string_tuple("missing_paths", self.missing_paths, allow_empty=True)
        if self.health_ok and self.missing_paths:
            raise ValueError("health_ok requires empty missing_paths")
        if self.status == "ready" and not self.health_ok:
            raise ValueError("ready status requires health_ok true")
        _validate_reason_codes(self.reason_codes)
        _validate_safe_flags(
            dashboard_safe=self.dashboard_safe,
            preview_safe=self.preview_safe,
            runtime_mutation_allowed=self.runtime_mutation_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_mutation_allowed=self.dashboard_mutation_allowed,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class DataPlaneTelemetryReadModel:
    telemetry_id: str
    layer_id: str
    append_log: DataPlaneAppendLogReadModel
    ledger: DataPlaneLedgerReadModel
    health: DataPlaneHealthReadModel
    telemetry_ready: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    preview_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_mutation_allowed: bool = False
    execution_allowed_from_preview: bool = False

    def __post_init__(self) -> None:
        if not self.telemetry_id:
            raise ValueError("telemetry_id must not be empty")
        if self.layer_id != "DATA_PLANE":
            raise ValueError("layer_id must be DATA_PLANE")
        if not isinstance(self.append_log, DataPlaneAppendLogReadModel):
            raise TypeError("append_log must be DataPlaneAppendLogReadModel")
        if not isinstance(self.ledger, DataPlaneLedgerReadModel):
            raise TypeError("ledger must be DataPlaneLedgerReadModel")
        if not isinstance(self.health, DataPlaneHealthReadModel):
            raise TypeError("health must be DataPlaneHealthReadModel")
        if not self.telemetry_ready:
            raise ValueError("telemetry_ready must remain true")
        _validate_reason_codes(self.reason_codes)
        _validate_safe_flags(
            dashboard_safe=self.dashboard_safe,
            preview_safe=self.preview_safe,
            runtime_mutation_allowed=self.runtime_mutation_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_mutation_allowed=self.dashboard_mutation_allowed,
        )
        if self.execution_allowed_from_preview:
            raise ValueError("execution_allowed_from_preview must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "telemetry_id": self.telemetry_id,
            "layer_id": self.layer_id,
            "append_log": self.append_log.to_dict(),
            "ledger": self.ledger.to_dict(),
            "health": self.health.to_dict(),
            "telemetry_ready": self.telemetry_ready,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "preview_safe": self.preview_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_mutation_allowed": self.dashboard_mutation_allowed,
            "execution_allowed_from_preview": self.execution_allowed_from_preview,
        }


@dataclass(frozen=True, slots=True)
class DataPlaneRuntimeReadModel:
    runtime_read_model_id: str
    layer_id: str
    telemetry: DataPlaneTelemetryReadModel
    runtime_write_surface: str
    canonical_truth_untouched: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    preview_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_mutation_allowed: bool = False
    execution_allowed_from_preview: bool = False

    def __post_init__(self) -> None:
        if not self.runtime_read_model_id:
            raise ValueError("runtime_read_model_id must not be empty")
        if self.layer_id != "DATA_PLANE":
            raise ValueError("layer_id must be DATA_PLANE")
        if not isinstance(self.telemetry, DataPlaneTelemetryReadModel):
            raise TypeError("telemetry must be DataPlaneTelemetryReadModel")
        if self.runtime_write_surface != "runtime_append_log_and_ledger_only":
            raise ValueError("runtime_write_surface must be runtime_append_log_and_ledger_only")
        if not self.canonical_truth_untouched:
            raise ValueError("canonical_truth_untouched must remain true")
        _validate_reason_codes(self.reason_codes)
        _validate_safe_flags(
            dashboard_safe=self.dashboard_safe,
            preview_safe=self.preview_safe,
            runtime_mutation_allowed=self.runtime_mutation_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_mutation_allowed=self.dashboard_mutation_allowed,
        )
        if self.execution_allowed_from_preview:
            raise ValueError("execution_allowed_from_preview must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_read_model_id": self.runtime_read_model_id,
            "layer_id": self.layer_id,
            "telemetry": self.telemetry.to_dict(),
            "runtime_write_surface": self.runtime_write_surface,
            "canonical_truth_untouched": self.canonical_truth_untouched,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "preview_safe": self.preview_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_mutation_allowed": self.dashboard_mutation_allowed,
            "execution_allowed_from_preview": self.execution_allowed_from_preview,
        }


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    _validate_string_tuple("reason_codes", reason_codes, allow_empty=False)


def _validate_string_tuple(field_name: str, values: tuple[str, ...], *, allow_empty: bool) -> None:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not allow_empty and not values:
        raise ValueError(f"{field_name} must not be empty")
    for value in values:
        if not value:
            raise ValueError(f"{field_name} must not contain empty values")


def _validate_sha256(field_name: str, value: str) -> None:
    if len(value) != 64:
        raise ValueError(f"{field_name} must be a 64-character sha256 hex string")
    int(value, 16)


def _validate_safe_flags(
    *,
    dashboard_safe: bool,
    preview_safe: bool,
    runtime_mutation_allowed: bool,
    canonical_write_allowed: bool,
    dashboard_mutation_allowed: bool,
) -> None:
    if not dashboard_safe:
        raise ValueError("dashboard_safe must remain true")
    if not preview_safe:
        raise ValueError("preview_safe must remain true")
    if runtime_mutation_allowed:
        raise ValueError("runtime_mutation_allowed must remain false")
    if canonical_write_allowed:
        raise ValueError("canonical_write_allowed must remain false")
    if dashboard_mutation_allowed:
        raise ValueError("dashboard_mutation_allowed must remain false")
