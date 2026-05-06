from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_store_acceptance_builder import (
    build_history_store_acceptance_preview,
)


def test_history_store_acceptance_preview_smoke() -> None:
    preview = build_history_store_acceptance_preview("runtime_history_store")
    assert preview["store_acceptance_ready"] is True
