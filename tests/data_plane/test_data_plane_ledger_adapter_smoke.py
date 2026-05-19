from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
    DataPlanePayloadReferenceKind,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_append_log_adapter import append_payload_reference_to_log
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_ledger_adapter import anchor_append_log_result_to_ledger

ONE = "1" * 64


def test_data_plane_ledger_adapter_anchors_append_log_result(tmp_path: Path) -> None:
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

    assert ledger_result.write_performed is True
    assert ledger_result.read_model.entry_count == 1
    assert ledger_result.read_model.immutable_ledger_enforced is True
