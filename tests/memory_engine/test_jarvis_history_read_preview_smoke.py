from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_context_reader import (
    build_jarvis_history_context_preview,
)


def test_jarvis_history_read_preview_smoke() -> None:
    preview = build_jarvis_history_context_preview()
    assert preview["readable_by_jarvis"] is True
    assert preview["context_ready"] is True
