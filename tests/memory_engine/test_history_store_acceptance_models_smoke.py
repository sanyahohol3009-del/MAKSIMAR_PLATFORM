from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_store_acceptance_models import (
    HistoryStoreAcceptanceResult,
)


def test_history_store_acceptance_models_smoke() -> None:
    result = HistoryStoreAcceptanceResult(
        session_manifest_count=1,
        attachment_summary_count=1,
        conversation_manifest_count=18,
        normalized_record_count=18,
        message_unit_count=11822,
        store_acceptance_ready=True,
    )
    assert result.store_acceptance_ready is True
