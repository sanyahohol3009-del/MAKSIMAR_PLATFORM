from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import build_media_memory_summary


def test_media_memory_summary_builder_smoke() -> None:
    summary = build_media_memory_summary()

    assert summary["media_memory_summary_ready"] is True
    assert summary["total_records"] >= 1
    assert summary["binary_external_records"] == summary["total_records"]
