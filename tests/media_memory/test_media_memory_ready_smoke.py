from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_artifact_memory_read_model,
    build_media_memory_preview,
    build_media_memory_summary,
)


def test_media_memory_ready_smoke() -> None:
    read_model = build_media_artifact_memory_read_model()
    summary = build_media_memory_summary()
    preview = build_media_memory_preview()

    assert read_model.total_records >= 1
    assert summary["media_memory_summary_ready"] is True
    assert preview["media_memory_ready"] is True
    assert preview["preview_ready"] is True
