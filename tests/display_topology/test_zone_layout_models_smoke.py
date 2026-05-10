from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import build_zone_layout_contract


def test_zone_layout_models_smoke() -> None:
    contract = build_zone_layout_contract()

    assert contract.total_zones >= 3
    assert contract.ready_zones == contract.total_zones
    assert contract.read_only_zones == contract.total_zones
    assert contract.private_zones >= 1
    assert contract.shared_zones >= 1

    zone_ids = {entry.zone_id for entry in contract.entries}
    assert "zone_dashboard_main" in zone_ids
