from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
    DataPlanePayloadReferenceKind,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_logger import log_payload_reference_to_data_plane

ONE = "1" * 64


def test_data_plane_logger_writes_runtime_append_log_and_ledger(tmp_path: Path) -> None:
    for rel_path in ("DATA_PLANE", "MAKSIMAR_CORE_LIB/data_plane", "MAKSIMAR_SERVER/DATA_PLANE"):
        (tmp_path / rel_path).mkdir(parents=True)

    payload = DataPlanePayloadReference(
        reference_id="logger-one",
        reference_kind=DataPlanePayloadReferenceKind.OBJECT_ARTIFACT,
        uri="object://payload/logger-one",
        sha256=ONE,
        size_bytes=128,
        producer_layer_id="DATA_PLANE",
        trace_id="trace-logger-one",
        backend_id="object_storage_primary",
        content_type="application/json",
    )

    result = log_payload_reference_to_data_plane(
        project_root=tmp_path,
        append_log_path=tmp_path / "append.jsonl",
        ledger_path=tmp_path / "ledger.jsonl",
        stream_id="data_plane_stream",
        ledger_id="data_plane_ledger",
        payload_reference=payload,
        created_at_utc="2026-01-01T00:00:00Z",
    )

    assert result.append_record_id
    assert result.ledger_entry_id
    assert result.runtime_read_model.canonical_truth_untouched is True
    assert result.canonical_write_allowed is False
