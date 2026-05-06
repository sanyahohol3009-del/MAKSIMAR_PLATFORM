from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_context_reader import (
    build_jarvis_history_context,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import (
    JarvisHistoryQuery,
)


def run_jarvis_history_query(
    query: JarvisHistoryQuery,
) -> Dict[str, object]:
    context = build_jarvis_history_context()
    return {
        "query_text": query.query_text,
        "query_scope": query.query_scope,
        "matched_memory_ids": context.memory_ids,
        "matched_titles": context.titles,
        "readable_by_jarvis": context.readable_by_jarvis,
    }


def build_jarvis_history_query_preview() -> Dict[str, object]:
    query = JarvisHistoryQuery(
        query_text="runtime truth path",
        query_scope="project_history",
        query_ready=True,
    )
    result = run_jarvis_history_query(query)
    return {
        "query_text": result["query_text"],
        "query_scope": result["query_scope"],
        "match_count": len(result["matched_memory_ids"]),
        "first_match_id": result["matched_memory_ids"][0],
        "readable_by_jarvis": result["readable_by_jarvis"],
    }
