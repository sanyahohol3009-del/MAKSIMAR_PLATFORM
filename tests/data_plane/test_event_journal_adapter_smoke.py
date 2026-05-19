from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
    DataPlanePayloadReferenceKind,
)
from MAKSIMAR_SERVER.DATA_PLANE.adapters.event_journal_adapter import (
    append_event_journal_payload_reference,
)

ONE = "1" * 64


def test_event_journal_adapter_delegates_to_append_log_adapter(tmp_path: Path) -> None:
    payload = DataPlanePayloadReference(
        reference_id="journal-one",
        reference_kind=DataPlanePayloadReferenceKind.OBJECT_ARTIFACT,
        uri="object://payload/journal-one",
        sha256=ONE,
        size_bytes=128,
        producer_layer_id="DATA_PLANE",
        trace_id="trace-journal-one",
        backend_id="object_storage_primary",
        content_type="application/json",
    )

    result = append_event_journal_payload_reference(
        journal_path=tmp_path / "journal.jsonl",
        stream_id="event_journal",
        payload_reference=payload,
        created_at_utc="2026-01-01T00:00:00Z",
    )

    assert result.write_performed is True
    assert result.read_model.append_only_enforced is True
    assert result.read_model.canonical_write_allowed is False
