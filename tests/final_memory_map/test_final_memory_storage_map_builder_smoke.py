from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_storage_map


def test_final_memory_storage_map_builder_smoke() -> None:
    storage = build_final_memory_storage_map()

    assert storage["storage_map_ready"] is True
    assert storage["all_storage_nodes_visible"] is True
    assert storage["storage_node_count"] >= 6
    assert storage["canonical_write_allowed"] is False
    assert storage["runtime_mutation_allowed"] is False


def test_storage_map_distinguishes_physical_store_paths_and_shared_projections():
    from pathlib import Path
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_graph
    graph = build_final_memory_graph()
    storage = build_final_memory_storage_map()
    expected = {node.storage_path for node in graph.nodes
                if node.classification in {"CANONICAL_STORE", "CHILD_BACKEND"} and node.storage_path and Path(node.storage_path).is_absolute() and Path(node.storage_path).exists()}
    assert set(storage["physical_store_paths"]) == expected
    assert storage["physical_store_count"] == len(expected)
    assert "runtime_history_store" not in storage["physical_store_nodes"]
    history = next(node for node in graph.nodes if node.node_id == "runtime_history_store")
    assert history.canonical_store_surface == "local_chat_memory"
    journal = next(node for node in graph.nodes if node.node_id == "local_chat_memory")
    assert journal.writer and "execution receipt memory" in journal.logical_roles
    assert storage["storage_node_count_basis"] == "logical_graph_surfaces; not physical databases"
