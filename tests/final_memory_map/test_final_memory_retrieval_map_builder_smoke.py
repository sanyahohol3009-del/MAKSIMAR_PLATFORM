from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_retrieval_map


def test_final_memory_retrieval_map_builder_smoke() -> None:
    retrieval = build_final_memory_retrieval_map()

    assert retrieval["retrieval_map_ready"] is True
    assert retrieval["all_retrieval_sources_visible"] is True
    assert retrieval["retrieval_source_count"] >= 6
    assert "read_only_preview" in retrieval["allowed_query_modes"]
