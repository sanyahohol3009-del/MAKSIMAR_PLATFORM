from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import build_memory_sync_contract


def test_memory_sync_models_smoke() -> None:
    contract = build_memory_sync_contract()

    assert contract.total_syncs == 3
    assert contract.ready_syncs == contract.total_syncs
    assert contract.read_model_syncs == contract.total_syncs
    assert contract.manifest_required_syncs == contract.total_syncs
    assert contract.canonical_write_allowed_syncs == 0
    assert contract.client_canonical_write_allowed_syncs == 0
    assert contract.parallel_truth_allowed_syncs == 0
    assert contract.auto_conflict_resolution_allowed_syncs == 0
    assert contract.runtime_mutation_allowed_syncs == 0
