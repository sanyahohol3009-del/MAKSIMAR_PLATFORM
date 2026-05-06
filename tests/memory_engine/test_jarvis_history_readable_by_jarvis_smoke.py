from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_summary_builder import (
    build_jarvis_history_summary,
)


def test_jarvis_history_readable_by_jarvis_smoke() -> None:
    summary = build_jarvis_history_summary()
    assert summary["readable_by_jarvis"] is True
