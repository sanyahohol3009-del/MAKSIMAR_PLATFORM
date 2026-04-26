from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_overlay_backend_contract import (
    build_visual_overlay_backend_contract,
)


def test_visual_overlay_backend_contract_builds() -> None:
    contract = build_visual_overlay_backend_contract()

    assert contract.contract_id == "visual_overlay_backend_contract_001"
    assert contract.backend_id == "visual_backend_overlay_001"
    assert contract.overlay_backend_name == "internal_overlay_adapter_backend"
    assert contract.supports_signal_overlay is True
    assert contract.supports_topology_overlay is True
    assert contract.supports_explainability_overlay is True
    assert contract.supports_depth_layers is True
