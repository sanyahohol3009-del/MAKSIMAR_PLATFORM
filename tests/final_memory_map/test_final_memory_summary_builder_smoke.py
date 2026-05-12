from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_summary


def test_final_memory_summary_builder_smoke() -> None:
    summary = build_final_memory_summary()

    assert summary["summary_ready"] is True
    assert summary["all_registered_modules_visible"] is True
    assert summary["all_storage_nodes_visible"] is True
    assert summary["all_retrieval_sources_visible"] is True
