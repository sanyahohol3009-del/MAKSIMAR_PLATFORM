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
    assert result["matched_memory_ids"] == ()
    assert result["matches"] == ()
    assert result["retrieval_basis"] == "existing_canonical_durable_memory_projection"


def test_explicit_history_inputs_are_returned_without_invented_fixture():
    records = ({"trace_id": "real-supplied-record", "topic": "runtime truth path",
                "user_text": "runtime truth path from the caller", "timestamp": "2026-10-11T12:30:00Z"},)
    result = run_jarvis_history_query(JarvisHistoryQuery(
        query_text="runtime truth path", query_scope="project_history", query_ready=True), records)
    assert result["matched_memory_ids"] == ("real-supplied-record",)
    assert result["matches"][0]["timestamp"] == records[0]["timestamp"]
    assert result["matches"][0]["user_text"] == records[0]["user_text"]
    assert "ARCH-0001" not in str(result)


def test_jarvis_history_query_does_not_return_unrelated_memory_object() -> None:
    result = run_jarvis_history_query(
        JarvisHistoryQuery(
            query_text="Semantic Spine capability activation",
            query_scope="project_history",
            query_ready=True,
        )
    )

    assert result["matched_memory_ids"] == ()
    assert result["matches"] == ()
    assert result["match_count"] == 0
