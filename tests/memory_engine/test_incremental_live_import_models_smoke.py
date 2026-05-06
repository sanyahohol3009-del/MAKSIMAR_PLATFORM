from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_live_import_models import (
    IncrementalLiveImportResult,
)


def test_incremental_live_import_models_smoke() -> None:
    result = IncrementalLiveImportResult(
        total_conversations_in_source=18,
        existing_conversations=18,
        new_conversations=0,
        new_conversation_writes_required=0,
        repeat_safe=True,
        incremental_ready=True,
    )
    assert result.incremental_ready is True
