from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import (
    JarvisHistoryQuery,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_reader import (
    run_jarvis_history_query,
)


def test_jarvis_history_query_reader_smoke() -> None:
    result = run_jarvis_history_query(
        JarvisHistoryQuery(
            query_text="runtime truth path",
            query_scope="project_history",
            query_ready=True,
        )
    )

    assert result["readable_by_jarvis"] is True
    assert result["matched_memory_ids"][0] == "ARCH-0001"
