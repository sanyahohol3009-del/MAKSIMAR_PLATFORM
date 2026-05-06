from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_store_acceptance_builder import (
    build_history_store_acceptance_result,
)


def test_history_store_acceptance_conversation_manifest_count_smoke() -> None:
    result = build_history_store_acceptance_result("runtime_history_store")
    assert result.conversation_manifest_count == 18
