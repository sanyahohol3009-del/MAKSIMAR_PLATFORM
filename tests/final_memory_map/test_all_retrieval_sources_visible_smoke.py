from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_acceptance


def test_all_retrieval_sources_visible_smoke() -> None:
    acceptance = build_final_memory_acceptance()

    assert acceptance["all_retrieval_sources_visible"] is True
