from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.data_plane_read_model import (
    DataPlaneAppendLogReadModel,
    DataPlaneHealthReadModel,
    DataPlaneLedgerReadModel,
    DataPlaneTelemetryReadModel,
)


def build_data_plane_telemetry_read_model(
    *,
    append_log: DataPlaneAppendLogReadModel,
    ledger: DataPlaneLedgerReadModel,
    health: DataPlaneHealthReadModel,
) -> DataPlaneTelemetryReadModel:
    if not isinstance(append_log, DataPlaneAppendLogReadModel):
        raise TypeError("append_log must be DataPlaneAppendLogReadModel")
    if not isinstance(ledger, DataPlaneLedgerReadModel):
        raise TypeError("ledger must be DataPlaneLedgerReadModel")
    if not isinstance(health, DataPlaneHealthReadModel):
        raise TypeError("health must be DataPlaneHealthReadModel")

    return DataPlaneTelemetryReadModel(
        telemetry_id="data_plane_telemetry_read_model_v1",
        layer_id="DATA_PLANE",
        append_log=append_log,
        ledger=ledger,
        health=health,
        telemetry_ready=True,
        reason_codes=(
            "append_log_read_model_bound",
            "ledger_read_model_bound",
            "health_read_model_bound",
            "dashboard_output_read_only",
        ),
    )
