from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_acceptance


def test_all_storage_nodes_visible_smoke() -> None:
    acceptance = build_final_memory_acceptance()

    assert acceptance["all_storage_nodes_visible"] is True
