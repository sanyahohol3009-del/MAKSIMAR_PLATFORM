from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
    DataPlanePayloadReferenceKind,
)
from MAKSIMAR_CORE_LIB.data_plane.data_plane_tracer_read_model import (
    build_data_plane_tracer_result_read_model,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_logger import log_payload_reference_to_data_plane

ONE = "1" * 64


def test_data_plane_logs_safe_execution_to_append_log_and_ledger(tmp_path: Path) -> None:
    for rel_path in ("DATA_PLANE", "MAKSIMAR_CORE_LIB/data_plane", "MAKSIMAR_SERVER/DATA_PLANE"):
        (tmp_path / rel_path).mkdir(parents=True)

    append_log_path = tmp_path / "runtime" / "data_plane_append_log.jsonl"
    ledger_path = tmp_path / "runtime" / "data_plane_ledger.jsonl"

    payload_reference = DataPlanePayloadReference(
        reference_id="safe-operation-001",
        reference_kind=DataPlanePayloadReferenceKind.OBJECT_ARTIFACT,
        uri="object://safe-operation/001",
        sha256=ONE,
        size_bytes=128,
        producer_layer_id="CONTROL_PLANE",
        trace_id="trace-safe-operation-001",
        backend_id="object_storage_primary",
        content_type="application/json",
    )

    logger_result = log_payload_reference_to_data_plane(
        project_root=tmp_path,
        append_log_path=append_log_path,
        ledger_path=ledger_path,
        stream_id="data_plane_execution_stream",
        ledger_id="data_plane_execution_ledger",
        payload_reference=payload_reference,
        created_at_utc="2026-01-01T00:00:00Z",
    )

    tracer_result = build_data_plane_tracer_result_read_model(
        operation_id="safe-operation-001",
        append_log_path=append_log_path,
        ledger_path=ledger_path,
        append_record_id=logger_result.append_record_id,
        ledger_entry_id=logger_result.ledger_entry_id,
        runtime_read_model=logger_result.runtime_read_model,
    )

    assert append_log_path.exists()
    assert ledger_path.exists()
    assert append_log_path.read_text(encoding="utf-8").count("\n") == 1
    assert ledger_path.read_text(encoding="utf-8").count("\n") == 1
    assert tracer_result.append_log_created is True
    assert tracer_result.ledger_entry_created is True
    assert tracer_result.telemetry_ready is True
    assert tracer_result.dashboard_safe is True
    assert tracer_result.canonical_truth_mutated is False
    assert tracer_result.canonical_write_allowed is False
    assert tracer_result.runtime_mutation_allowed is False
    assert tracer_result.data_pipe_status == "logged_to_append_only_runtime_data_plane"
