from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_builder import (
    build_history_completion_preview,
)


def test_history_completion_preview_smoke() -> None:
    preview = build_history_completion_preview()
    assert preview["completion_ready"] is True
