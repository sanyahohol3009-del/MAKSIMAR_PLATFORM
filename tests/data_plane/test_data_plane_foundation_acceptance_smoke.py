from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.data_plane.data_plane_read_model import (
    DataPlaneAppendLogReadModel,
    DataPlaneHealthReadModel,
    DataPlaneLedgerReadModel,
)
from MAKSIMAR_CORE_LIB.data_plane.data_plane_tracer_read_model import (
    DataPlaneTracerResultReadModel,
    build_data_plane_tracer_result_read_model,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_read_model_builder import (
    build_data_plane_runtime_read_model,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_telemetry_read_model_builder import (
    build_data_plane_telemetry_read_model,
)

ONE = "1" * 64
TWO = "2" * 64


def _runtime_read_model():
    append_log = DataPlaneAppendLogReadModel(
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
    ledger = DataPlaneLedgerReadModel(
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
    health = DataPlaneHealthReadModel(
        layer_id="DATA_PLANE",
        status="ready",
        checked_paths=("DATA_PLANE",),
        missing_paths=(),
        health_ok=True,
        reason_codes=("healthy",),
    )
    telemetry = build_data_plane_telemetry_read_model(
        append_log=append_log,
        ledger=ledger,
        health=health,
    )
    return build_data_plane_runtime_read_model(telemetry)


def test_data_plane_foundation_acceptance_docs_exist() -> None:
    required_docs = (
        "docs/architecture/foundation/data_plane_foundation_v1.md",
        "docs/architecture/foundation/data_plane_semantic_duplicate_review_v1.md",
        "docs/architecture/foundation/data_plane_container_boundary_v1.md",
        "docs/architecture/foundation/data_plane_append_only_log_policy_v1.md",
    )

    for doc_path in required_docs:
        assert Path(doc_path).exists(), doc_path


def test_data_plane_tracer_result_rejects_canonical_truth_mutation(tmp_path: Path) -> None:
    append_log_path = tmp_path / "append.jsonl"
    ledger_path = tmp_path / "ledger.jsonl"
    append_log_path.write_text('{"event":"append"}\n', encoding="utf-8")
    ledger_path.write_text('{"event":"ledger"}\n', encoding="utf-8")

    runtime_read_model = _runtime_read_model()
    tracer_result = build_data_plane_tracer_result_read_model(
        operation_id="operation-001",
        append_log_path=append_log_path,
        ledger_path=ledger_path,
        append_record_id="record-001",
        ledger_entry_id="ledger-001",
        runtime_read_model=runtime_read_model,
    )

    assert tracer_result.data_pipe_status == "logged_to_append_only_runtime_data_plane"
    assert tracer_result.canonical_truth_mutated is False
    assert tracer_result.dashboard_safe is True

    with pytest.raises(ValueError, match="canonical_truth_mutated"):
        DataPlaneTracerResultReadModel(
            tracer_id="bad",
            layer_id="DATA_PLANE",
            operation_id="operation-001",
            data_pipe_status="logged_to_append_only_runtime_data_plane",
            append_log_created=True,
            ledger_entry_created=True,
            telemetry_ready=True,
            append_log_path=str(append_log_path),
            ledger_path=str(ledger_path),
            append_record_id="record-001",
            ledger_entry_id="ledger-001",
            runtime_read_model=runtime_read_model,
            canonical_truth_mutated=True,
            dashboard_safe=True,
            runtime_mutation_allowed=False,
            canonical_write_allowed=False,
            reason_codes=("bad",),
        )
