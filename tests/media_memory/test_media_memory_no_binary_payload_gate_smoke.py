from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_artifact_memory_read_model,
    build_media_memory_phase_readiness,
)


def test_media_memory_no_binary_payload_gate_smoke() -> None:
    read_model = build_media_artifact_memory_read_model()
    readiness = build_media_memory_phase_readiness()

    assert readiness.no_binary_payloads is True
    assert read_model.binary_external_records == read_model.total_records

    for record in read_model.records:
        assert record.binary_external is True
        assert record.artifact_ref.startswith("artifact://")
