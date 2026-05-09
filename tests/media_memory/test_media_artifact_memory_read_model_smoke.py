from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import build_media_artifact_memory_read_model


def test_media_artifact_memory_read_model_smoke() -> None:
    read_model = build_media_artifact_memory_read_model()

    assert read_model.total_records == len(read_model.records)
    assert read_model.dashboard_visible_records == read_model.total_records
    assert read_model.binary_external_records == read_model.total_records
    assert read_model.provenance_required_records == read_model.total_records
    assert read_model.traceability_required_records == read_model.total_records
