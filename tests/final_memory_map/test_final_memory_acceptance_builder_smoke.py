from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_acceptance


def test_final_memory_acceptance_builder_smoke() -> None:
    acceptance = build_final_memory_acceptance()

    assert acceptance["acceptance_ready"] is True
    assert acceptance["project_fully_visible_in_memory"] is True
    assert acceptance["all_registered_modules_visible"] is True
    assert acceptance["all_storage_nodes_visible"] is True
    assert acceptance["all_retrieval_sources_visible"] is True
