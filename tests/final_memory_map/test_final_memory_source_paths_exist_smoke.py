from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import (
    build_final_memory_graph,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_final_memory_source_paths_exist_smoke() -> None:
    graph = build_final_memory_graph()

    missing_paths = tuple(
        node.source_path
        for node in graph.nodes
        if not (PROJECT_ROOT / node.source_path).exists()
    )

    assert missing_paths == ()
