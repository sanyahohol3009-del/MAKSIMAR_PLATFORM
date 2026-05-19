from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
)
from MAKSIMAR_CORE_LIB.data_plane.data_plane_read_model import DataPlaneRuntimeReadModel
from MAKSIMAR_SERVER.DATA_PLANE.append_only_log_writer import (
    write_append_only_payload_reference,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_health import build_data_plane_health_read_model
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_read_model_builder import (
    build_data_plane_runtime_read_model,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_telemetry_read_model_builder import (
    build_data_plane_telemetry_read_model,
)
from MAKSIMAR_SERVER.DATA_PLANE.immutable_ledger_builder import (
    build_immutable_ledger_anchor,
)


@dataclass(frozen=True, slots=True)
class DataPlaneLoggerResult:
    logger_id: str
    append_record_id: str
    ledger_entry_id: str
    runtime_read_model: DataPlaneRuntimeReadModel
    dashboard_safe: bool = True
    canonical_write_allowed: bool = False
    dashboard_mutation_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.logger_id:
            raise ValueError("logger_id must not be empty")
        if not self.append_record_id:
            raise ValueError("append_record_id must not be empty")
        if not self.ledger_entry_id:
            raise ValueError("ledger_entry_id must not be empty")
        if not isinstance(self.runtime_read_model, DataPlaneRuntimeReadModel):
            raise TypeError("runtime_read_model must be DataPlaneRuntimeReadModel")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.dashboard_mutation_allowed:
            raise ValueError("dashboard_mutation_allowed must remain false")


def log_payload_reference_to_data_plane(
    *,
    project_root: Path,
    append_log_path: Path,
    ledger_path: Path,
    stream_id: str,
    ledger_id: str,
    payload_reference: DataPlanePayloadReference,
    created_at_utc: str,
) -> DataPlaneLoggerResult:
    if not isinstance(project_root, Path):
        raise TypeError("project_root must be pathlib.Path")

    append_result = write_append_only_payload_reference(
        log_path=append_log_path,
        stream_id=stream_id,
        payload_reference=payload_reference,
        created_at_utc=created_at_utc,
    )
    ledger_result = build_immutable_ledger_anchor(
        ledger_path=ledger_path,
        ledger_id=ledger_id,
        append_result=append_result,
        created_at_utc=created_at_utc,
    )
    health = build_data_plane_health_read_model(project_root)
    telemetry = build_data_plane_telemetry_read_model(
        append_log=append_result.read_model,
        ledger=ledger_result.read_model,
        health=health,
    )
    runtime_read_model = build_data_plane_runtime_read_model(telemetry)

    return DataPlaneLoggerResult(
        logger_id="data_plane_logger_v1",
        append_record_id=append_result.appended_record_id,
        ledger_entry_id=ledger_result.appended_entry_id,
        runtime_read_model=runtime_read_model,
    )
