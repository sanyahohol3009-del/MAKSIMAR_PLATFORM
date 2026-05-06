from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_store_acceptance_summary_builder import (
    build_history_store_acceptance_summary,
)


def test_history_store_acceptance_summary_builder_smoke() -> None:
    summary = build_history_store_acceptance_summary("runtime_history_store")
    assert summary["store_acceptance_ready"] is True
