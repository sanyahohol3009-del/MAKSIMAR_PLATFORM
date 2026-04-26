from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_graph_backend_contract import (
    build_visual_graph_backend_contract,
)


def test_visual_graph_backend_contract_builds() -> None:
    contract = build_visual_graph_backend_contract()

    assert contract.contract_id == "visual_graph_backend_contract_001"
    assert contract.backend_id == "visual_backend_graph_001"
    assert contract.graph_backend_name == "react_flow_adapter_backend"
    assert contract.supports_node_rendering is True
    assert contract.supports_edge_rendering is True
    assert contract.supports_pan_zoom is True
    assert contract.supports_selection is True
