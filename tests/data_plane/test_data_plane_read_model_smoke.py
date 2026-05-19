from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.data_plane.data_plane_read_model import (
    DataPlaneAppendLogReadModel,
    DataPlaneHealthReadModel,
    DataPlaneLedgerReadModel,
    DataPlaneTelemetryReadModel,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_read_model_builder import (
    build_data_plane_runtime_read_model,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_telemetry_read_model_builder import (
    build_data_plane_telemetry_read_model,
)

ONE = "1" * 64
TWO = "2" * 64


def _append_log() -> DataPlaneAppendLogReadModel:
    return DataPlaneAppendLogReadModel(
        append_log_id="append_log",
        stream_id="stream",
        log_path="RUNTIME/state/append.jsonl",
        record_count=1,
        head_hash=ONE,
        latest_record_id="stream:00000000000000000000",
        write_performed=True,
        append_only_enforced=True,
        reason_codes=("append_ok",),
    )


def _ledger() -> DataPlaneLedgerReadModel:
    return DataPlaneLedgerReadModel(
        ledger_adapter_id="ledger_adapter",
        ledger_id="ledger",
        ledger_path="RUNTIME/state/ledger.jsonl",
        entry_count=1,
        head_hash=TWO,
        latest_entry_id="ledger:00000000000000000000",
        write_performed=True,
        immutable_ledger_enforced=True,
        reason_codes=("ledger_ok",),
    )


def _health() -> DataPlaneHealthReadModel:
    return DataPlaneHealthReadModel(
        layer_id="DATA_PLANE",
        status="ready",
        checked_paths=("DATA_PLANE",),
        missing_paths=(),
        health_ok=True,
        reason_codes=("healthy",),
    )


def test_data_plane_read_models_are_dashboard_safe() -> None:
    telemetry = build_data_plane_telemetry_read_model(
        append_log=_append_log(),
        ledger=_ledger(),
        health=_health(),
    )
    runtime_read_model = build_data_plane_runtime_read_model(telemetry)

    assert runtime_read_model.dashboard_safe is True
    assert runtime_read_model.preview_safe is True
    assert runtime_read_model.execution_allowed_from_preview is False
    assert runtime_read_model.runtime_mutation_allowed is False
    assert runtime_read_model.canonical_write_allowed is False
    assert runtime_read_model.canonical_truth_untouched is True


def test_data_plane_read_model_rejects_dashboard_mutation() -> None:
    with pytest.raises(ValueError, match="dashboard_mutation_allowed"):
        DataPlaneAppendLogReadModel(
            append_log_id="append_log",
            stream_id="stream",
            log_path="RUNTIME/state/append.jsonl",
            record_count=1,
            head_hash=ONE,
            latest_record_id="stream:00000000000000000000",
            write_performed=True,
            append_only_enforced=True,
            reason_codes=("append_ok",),
            dashboard_mutation_allowed=True,
        )


def test_data_plane_telemetry_rejects_preview_execution() -> None:
    with pytest.raises(ValueError, match="execution_allowed_from_preview"):
        DataPlaneTelemetryReadModel(
            telemetry_id="telemetry",
            layer_id="DATA_PLANE",
            append_log=_append_log(),
            ledger=_ledger(),
            health=_health(),
            telemetry_ready=True,
            reason_codes=("ready",),
            execution_allowed_from_preview=True,
        )
