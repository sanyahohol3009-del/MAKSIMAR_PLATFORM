from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.canonical_freeze_summary import (
    build_canonical_freeze_summary,
)


def test_canonical_freeze_summary_smoke() -> None:
    summary = build_canonical_freeze_summary()

    assert summary["freeze_ready"] is True
    assert summary["canonical_phase_count"] == 12
