from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.data_plane.data_plane_read_model import DataPlaneRuntimeReadModel


@dataclass(frozen=True, slots=True)
class DataPlaneTracerResultReadModel:
    tracer_id: str
    layer_id: str
    operation_id: str
    data_pipe_status: str
    append_log_created: bool
    ledger_entry_created: bool
    telemetry_ready: bool
    append_log_path: str
    ledger_path: str
    append_record_id: str
    ledger_entry_id: str
    runtime_read_model: DataPlaneRuntimeReadModel
    canonical_truth_mutated: bool
    dashboard_safe: bool
    runtime_mutation_allowed: bool
    canonical_write_allowed: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name, value in (
            ("tracer_id", self.tracer_id),
            ("layer_id", self.layer_id),
            ("operation_id", self.operation_id),
            ("data_pipe_status", self.data_pipe_status),
            ("append_log_path", self.append_log_path),
            ("ledger_path", self.ledger_path),
            ("append_record_id", self.append_record_id),
            ("ledger_entry_id", self.ledger_entry_id),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if self.layer_id != "DATA_PLANE":
            raise ValueError("layer_id must be DATA_PLANE")
        if self.data_pipe_status != "logged_to_append_only_runtime_data_plane":
            raise ValueError("data_pipe_status must be logged_to_append_only_runtime_data_plane")
        if not self.append_log_created:
            raise ValueError("append_log_created must remain true")
        if not self.ledger_entry_created:
            raise ValueError("ledger_entry_created must remain true")
        if not self.telemetry_ready:
            raise ValueError("telemetry_ready must remain true")
        if not isinstance(self.runtime_read_model, DataPlaneRuntimeReadModel):
            raise TypeError("runtime_read_model must be DataPlaneRuntimeReadModel")
        if self.canonical_truth_mutated:
            raise ValueError("canonical_truth_mutated must remain false")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        for reason_code in self.reason_codes:
            if not reason_code:
                raise ValueError("reason_codes must not contain empty values")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["runtime_read_model"] = self.runtime_read_model.to_dict()
        return payload


def build_data_plane_tracer_result_read_model(
    *,
    operation_id: str,
    append_log_path: Path,
    ledger_path: Path,
    append_record_id: str,
    ledger_entry_id: str,
    runtime_read_model: DataPlaneRuntimeReadModel,
) -> DataPlaneTracerResultReadModel:
    if not operation_id:
        raise ValueError("operation_id must not be empty")
    if not isinstance(append_log_path, Path):
        raise TypeError("append_log_path must be pathlib.Path")
    if not isinstance(ledger_path, Path):
        raise TypeError("ledger_path must be pathlib.Path")
    if not append_log_path.exists():
        raise ValueError("append_log_path must exist")
    if not ledger_path.exists():
        raise ValueError("ledger_path must exist")
    if append_log_path.is_dir():
        raise ValueError("append_log_path must not be a directory")
    if ledger_path.is_dir():
        raise ValueError("ledger_path must not be a directory")
    if not append_record_id:
        raise ValueError("append_record_id must not be empty")
    if not ledger_entry_id:
        raise ValueError("ledger_entry_id must not be empty")
    if not isinstance(runtime_read_model, DataPlaneRuntimeReadModel):
        raise TypeError("runtime_read_model must be DataPlaneRuntimeReadModel")

    return DataPlaneTracerResultReadModel(
        tracer_id="data_plane_e2e_tracer_result_v1",
        layer_id="DATA_PLANE",
        operation_id=operation_id,
        data_pipe_status="logged_to_append_only_runtime_data_plane",
        append_log_created=True,
        ledger_entry_created=True,
        telemetry_ready=runtime_read_model.telemetry.telemetry_ready,
        append_log_path=str(append_log_path),
        ledger_path=str(ledger_path),
        append_record_id=append_record_id,
        ledger_entry_id=ledger_entry_id,
        runtime_read_model=runtime_read_model,
        canonical_truth_mutated=False,
        dashboard_safe=True,
        runtime_mutation_allowed=False,
        canonical_write_allowed=False,
        reason_codes=(
            "safe_operation_logged_to_append_only_log",
            "ledger_anchor_created",
            "dashboard_safe_telemetry_available",
            "canonical_truth_untouched",
        ),
    )
