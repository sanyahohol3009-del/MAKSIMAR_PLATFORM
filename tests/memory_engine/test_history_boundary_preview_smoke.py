from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_ingestion_builders import (
    build_history_boundary_preview,
)


def test_history_boundary_preview_smoke() -> None:
    preview = build_history_boundary_preview()

    assert preview["phase"] == "PHASE-H0"
    assert preview["track_name"] == "project_history_ingestion_track"
    assert preview["package_path"] == "MAKSIMAR_CORE_LIB/memory_engine/history_ingestion"
    assert preview["multi_format_required"] is True
    assert preview["dedup_required_before_real_import"] is True
    assert preview["portable_storage_required"] is True
    assert preview["future_nas_compatibility_required"] is True
    assert preview["supporting_source_only"] is True
    assert preview["canonical_truth_write_allowed"] is False
    assert preview["real_data_import_allowed"] is False
    assert preview["preview_ready"] is True
    assert "html" in preview["supported_source_types"]
    assert "pdf" in preview["supported_source_types"]
    assert "preview_traceability" in preview["required_capabilities"]
