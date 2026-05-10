from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import build_memory_sync_route_contract


def test_memory_sync_router_smoke() -> None:
    contract = build_memory_sync_route_contract()

    assert contract.total_routes == 3
    assert contract.ready_routes == contract.total_routes
    assert contract.source_manifest_bound_routes == contract.total_routes
    assert contract.target_manifest_bound_routes == contract.total_routes
    assert contract.registry_bound_routes == contract.total_routes
    assert contract.policy_bound_routes == contract.total_routes
    assert contract.observability_bound_routes == contract.total_routes
    assert contract.preview_required_routes == contract.total_routes
    assert contract.checksum_required_routes == contract.total_routes
    assert contract.read_only_routes == contract.total_routes
    assert contract.canonical_write_allowed_routes == 0
    assert contract.client_canonical_write_allowed_routes == 0
    assert contract.runtime_mutation_allowed_routes == 0
