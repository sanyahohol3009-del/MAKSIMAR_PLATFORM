from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.data_plane_read_model import (
    DataPlaneRuntimeReadModel,
    DataPlaneTelemetryReadModel,
)


def build_data_plane_runtime_read_model(
    telemetry: DataPlaneTelemetryReadModel,
) -> DataPlaneRuntimeReadModel:
    if not isinstance(telemetry, DataPlaneTelemetryReadModel):
        raise TypeError("telemetry must be DataPlaneTelemetryReadModel")

    return DataPlaneRuntimeReadModel(
        runtime_read_model_id="data_plane_runtime_read_model_v1",
        layer_id="DATA_PLANE",
        telemetry=telemetry,
        runtime_write_surface="runtime_append_log_and_ledger_only",
        canonical_truth_untouched=True,
        reason_codes=(
            "v1_runtime_read_model_compatibility_preserved",
            "v2_telemetry_read_model_bound",
            "canonical_truth_untouched",
        ),
    )
