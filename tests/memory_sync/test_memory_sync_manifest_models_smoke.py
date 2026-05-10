from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import build_memory_sync_manifest_contract


def test_memory_sync_manifest_models_smoke() -> None:
    contract = build_memory_sync_manifest_contract()

    assert contract.total_manifests == 3
    assert contract.ready_manifests == contract.total_manifests
    assert contract.registry_bound_manifests == contract.total_manifests
    assert contract.policy_bound_manifests == contract.total_manifests
    assert contract.observability_bound_manifests == contract.total_manifests
    assert contract.preview_required_manifests == contract.total_manifests
    assert contract.checksum_required_manifests == contract.total_manifests
    assert contract.read_only_manifests == contract.total_manifests
    assert contract.canonical_write_allowed_manifests == 0
