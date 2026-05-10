from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import build_memory_sync_summary


def test_memory_sync_summary_builder_smoke() -> None:
    summary = build_memory_sync_summary()

    assert summary["summary_ready"] is True
    assert summary["node_scopes"] == 3
    assert summary["sync_links"] == 3
    assert summary["sync_manifests"] == 3
    assert summary["sync_routes"] == 3
    assert summary["conflict_guards"] == 3
    assert summary["canonical_write_allowed"] == 0
    assert summary["client_canonical_write_allowed"] == 0
    assert summary["parallel_truth_allowed"] == 0
    assert summary["runtime_mutation_allowed"] == 0
    assert summary["auto_conflict_resolution_allowed"] == 0
    assert summary["mobile_security_root_scopes"] == 0
