from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_storage_map


def test_final_memory_storage_map_builder_smoke() -> None:
    storage = build_final_memory_storage_map()

    assert storage["storage_map_ready"] is True
    assert storage["all_storage_nodes_visible"] is True
    assert storage["storage_node_count"] >= 6
    assert storage["canonical_write_allowed"] is False
    assert storage["runtime_mutation_allowed"] is False
