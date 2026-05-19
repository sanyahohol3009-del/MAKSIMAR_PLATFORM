from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
    DataPlanePayloadReferenceKind,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_append_log_adapter import (
    append_payload_reference_to_log,
)

ONE = "1" * 64
TWO = "2" * 64


def _payload(reference_id: str, sha256: str) -> DataPlanePayloadReference:
    return DataPlanePayloadReference(
        reference_id=reference_id,
        reference_kind=DataPlanePayloadReferenceKind.OBJECT_ARTIFACT,
        uri=f"object://payload/{reference_id}",
        sha256=sha256,
        size_bytes=128,
        producer_layer_id="DATA_PLANE",
        trace_id=f"trace-{reference_id}",
        backend_id="object_storage_primary",
        content_type="application/json",
    )


def test_data_plane_append_log_adapter_writes_jsonl_append_only(tmp_path: Path) -> None:
    log_path = tmp_path / "append.jsonl"

    first = append_payload_reference_to_log(
        log_path=log_path,
        stream_id="data_plane_stream",
        payload_reference=_payload("one", ONE),
        created_at_utc="2026-01-01T00:00:00Z",
    )
    second = append_payload_reference_to_log(
        log_path=log_path,
        stream_id="data_plane_stream",
        payload_reference=_payload("two", TWO),
        created_at_utc="2026-01-01T00:00:01Z",
    )

    assert first.write_performed is True
    assert second.write_performed is True
    assert second.read_model.record_count == 2
    assert log_path.read_text(encoding="utf-8").count("\n") == 2
    assert second.read_model.append_only_enforced is True
