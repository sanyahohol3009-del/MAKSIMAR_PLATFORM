from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
    DataPlanePayloadReferenceKind,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_append_log_adapter import append_payload_reference_to_log
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_health import build_data_plane_health_read_model
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_ledger_adapter import anchor_append_log_result_to_ledger
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_read_model_builder import build_data_plane_runtime_read_model
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_telemetry_read_model_builder import (
    build_data_plane_telemetry_read_model,
)

ONE = "1" * 64


def test_data_plane_telemetry_builder_binds_runtime_read_models(tmp_path: Path) -> None:
    for rel_path in ("DATA_PLANE", "MAKSIMAR_CORE_LIB/data_plane", "MAKSIMAR_SERVER/DATA_PLANE"):
        (tmp_path / rel_path).mkdir(parents=True)

    payload = DataPlanePayloadReference(
        reference_id="one",
        reference_kind=DataPlanePayloadReferenceKind.OBJECT_ARTIFACT,
        uri="object://payload/one",
        sha256=ONE,
        size_bytes=128,
        producer_layer_id="DATA_PLANE",
        trace_id="trace-one",
        backend_id="object_storage_primary",
        content_type="application/json",
    )
    append_result = append_payload_reference_to_log(
        log_path=tmp_path / "append.jsonl",
        stream_id="data_plane_stream",
        payload_reference=payload,
        created_at_utc="2026-01-01T00:00:00Z",
    )
    ledger_result = anchor_append_log_result_to_ledger(
        ledger_path=tmp_path / "ledger.jsonl",
        ledger_id="data_plane_ledger",
        append_result=append_result,
        created_at_utc="2026-01-01T00:00:01Z",
    )
    health = build_data_plane_health_read_model(tmp_path)

    telemetry = build_data_plane_telemetry_read_model(
        append_log=append_result.read_model,
        ledger=ledger_result.read_model,
        health=health,
    )
    runtime_read_model = build_data_plane_runtime_read_model(telemetry)

    assert telemetry.telemetry_ready is True
    assert telemetry.dashboard_safe is True
    assert runtime_read_model.canonical_truth_untouched is True
    assert runtime_read_model.execution_allowed_from_preview is False
