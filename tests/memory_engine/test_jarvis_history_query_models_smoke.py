from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import (
    JarvisHistoryQuery,
)


def test_jarvis_history_query_models_smoke() -> None:
    query = JarvisHistoryQuery(
        query_text="runtime truth path",
        query_scope="project_history",
        query_ready=True,
    )

    assert query.query_ready is True
