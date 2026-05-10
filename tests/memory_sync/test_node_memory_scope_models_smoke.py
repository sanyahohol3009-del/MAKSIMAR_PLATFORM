from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import build_node_memory_scope_contract


def test_node_memory_scope_models_smoke() -> None:
    contract = build_node_memory_scope_contract()

    assert contract.total_scopes == 3
    assert contract.ready_scopes == contract.total_scopes
    assert contract.read_enabled_scopes == contract.total_scopes
    assert contract.read_only_scopes == contract.total_scopes
    assert contract.canonical_write_allowed_scopes == 0
    assert contract.client_canonical_write_allowed_scopes == 0
    assert contract.mobile_security_root_scopes == 0
    assert contract.parallel_truth_allowed_scopes == 0
    assert contract.sync_manifest_required_scopes == contract.total_scopes
