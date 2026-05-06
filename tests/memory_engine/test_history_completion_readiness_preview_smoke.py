from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_summary_builder import (
    build_history_completion_summary,
)


def test_history_completion_readiness_preview_smoke() -> None:
    summary = build_history_completion_summary()
    assert summary["full_history_import_ready"] is True
    assert summary["incremental_reimport_safe"] is True
