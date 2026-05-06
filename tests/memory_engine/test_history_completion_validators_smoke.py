from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_models import (
    HistoryCompletionState,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_validators import (
    validate_history_completion_ready,
)


def test_history_completion_validators_smoke() -> None:
    state = HistoryCompletionState(
        full_history_import_ready=True,
        project_history_graph_ready=True,
        project_history_panel_ready=True,
        project_history_filter_ready=True,
        project_history_readable_by_jarvis=True,
        incremental_reimport_safe=True,
        completion_ready=True,
    )

    validate_history_completion_ready(state)
