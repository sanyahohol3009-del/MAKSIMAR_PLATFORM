from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_reader import (
    build_jarvis_history_query_preview,
)


def test_jarvis_history_query_preview_smoke() -> None:
    preview = build_jarvis_history_query_preview()
    assert preview["match_count"] == 1
    assert preview["readable_by_jarvis"] is True
