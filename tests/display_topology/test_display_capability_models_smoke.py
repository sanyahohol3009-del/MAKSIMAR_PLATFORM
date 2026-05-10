from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_capability_binding_contract,
)


def test_display_capability_models_smoke() -> None:
    contract = build_display_capability_binding_contract()

    assert contract.total_capabilities >= 7
    assert contract.ready_capabilities == contract.total_capabilities
    assert contract.read_only_capabilities == contract.total_capabilities
    assert contract.direct_execution_allowed_capabilities == 0

    capabilities = {entry.capability for entry in contract.entries}
    assert "multi_window" in capabilities
    assert "spatial_overlay" in capabilities
    assert "mobile_proxy" in capabilities
    assert "private_display" in capabilities
