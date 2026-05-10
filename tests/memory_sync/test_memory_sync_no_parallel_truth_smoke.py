from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import (
    build_memory_sync_contract,
    build_memory_sync_manifest_contract,
    build_node_memory_scope_contract,
)


def test_memory_sync_no_parallel_truth_smoke() -> None:
    scopes = build_node_memory_scope_contract()
    sync = build_memory_sync_contract()
    manifests = build_memory_sync_manifest_contract()

    assert scopes.parallel_truth_allowed_scopes == 0
    assert sync.parallel_truth_allowed_syncs == 0
    assert sync.auto_conflict_resolution_allowed_syncs == 0
    assert sync.runtime_mutation_allowed_syncs == 0
    assert manifests.canonical_write_allowed_manifests == 0
