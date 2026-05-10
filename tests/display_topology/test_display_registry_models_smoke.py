from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import build_display_registry_contract


def test_display_registry_models_smoke() -> None:
    contract = build_display_registry_contract()

    assert contract.total_entries == 3
    assert contract.ready_entries == contract.total_entries
    assert contract.dashboard_bindable_entries == contract.total_entries
    assert contract.registry_routing_ready_entries == contract.total_entries
    assert contract.read_only_entries == contract.total_entries
    assert contract.direct_switching_allowed_entries == 0
