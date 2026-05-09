from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import build_media_memory_preview


def test_media_memory_preview_smoke() -> None:
    preview = build_media_memory_preview()

    assert preview["preview_ready"] is True
    assert preview["media_memory_ready"] is True
    assert preview["flow"] == (
        "storage_registry",
        "artifact_routing",
        "media_artifact_memory",
        "generated_media_metadata",
        "model_weight_metadata",
        "dataset_metadata",
        "project_output_metadata",
        "dedup_decision",
        "dashboard_read_only_preview",
    )
