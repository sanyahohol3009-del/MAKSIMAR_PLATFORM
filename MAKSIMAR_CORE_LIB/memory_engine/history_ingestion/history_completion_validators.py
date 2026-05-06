from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_models import (
    HistoryCompletionState,
)


def validate_history_completion_ready(
    state: HistoryCompletionState,
) -> None:
    if not state.completion_ready:
        raise ValueError("History completion state must be completion_ready")
