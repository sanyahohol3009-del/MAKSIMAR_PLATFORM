from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import build_memory_sync_preview


def test_memory_sync_preview_builder_smoke() -> None:
    preview = build_memory_sync_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["node_scopes"] == 3
    assert preview["sync_links"] == 3
    assert preview["sync_manifests"] == 3
    assert preview["sync_routes"] == 3
    assert preview["conflict_guards"] == 3
    assert preview["memory_map_ids"] == ("memory_map_global_001",)
    assert preview["canonical_write_allowed"] == 0
    assert preview["client_canonical_write_allowed"] == 0
    assert preview["parallel_truth_allowed"] == 0
    assert preview["runtime_mutation_allowed"] == 0
