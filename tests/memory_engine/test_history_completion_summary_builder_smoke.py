from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_summary_builder import (
    build_history_completion_summary,
)


def test_history_completion_summary_builder_smoke() -> None:
    summary = build_history_completion_summary()
    assert summary["completion_ready"] is True
